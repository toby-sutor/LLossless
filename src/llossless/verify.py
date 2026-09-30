"""Pass 3 — decide, for each claim, whether the reference text supports it.

This is the pass the tool exists for. Everything else is preparation: decompose
produces the claims, merge produces the text, and this is where a dropped fact
becomes a finding rather than an absence nobody noticed.

Two things here are load-bearing and both are about refusing to guess.

The first is that every claim sent must come back with exactly one verdict. A
model that silently returns nine verdicts for ten claims must not have the tenth
filled in as MISSING, because MISSING is a *finding* — it means "the reference
text does not contain this" — and inventing it from a short response would
manufacture the exact result this tool reports to humans. A short response is a
parse error, and a parse error that survives two attempts errors the batch.

The second is that a SUPPORTED or CONTRADICTED verdict quoting evidence nobody
checked is worth less than no evidence at all. Both labels assert that the
reference text says something, so both are asked for the span that says it, and
both have that span located. A model that labels SUPPORTED and fabricates the
span is the worst failure mode this pass has, because it is the one that looks
most like success — and CONTRADICTED is where a wrong finding is most expensive,
because that is the one a human is asked to act on.

Locating a span asks two questions, and they have different answers. `evidence`
is what was quoted; `evidence_source` is which file it was quoted from. A span
that appears nowhere is a transcription error — the model wrote a quotation that
does not exist. A span that appears, but in a file other than the one named, is
an attribution error — the quote is real and the claim about where it came from
is not. Rolling the two together into "ungrounded" would hide that difference,
and in the reverse direction, where the target is every source, the second is
the one that decides whether a claim was invented.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace

from . import config, parsing, prompts, reconcile, segment, structured, window
from .client import Client, Completion, SchemaFailure
from . import decompose
from .decompose import Claim, normalise
from .merge import (BUDGET_STEP, CHARS_PER_TOKEN, REASONING_ALLOWANCE, MergePolicy,
                    escaped_length)

SOURCE_TO_MERGED = "source_to_merged"
MERGED_TO_SOURCES = "merged_to_sources"
DIRECTIONS = (SOURCE_TO_MERGED, MERGED_TO_SOURCES)

# Which prompt file each direction uses, which placeholder holds the reference
# text in it, and which holds the list of filenames that text is made of. The
# two prompts are separate files rather than one file with a swapped heading
# because the rules genuinely differ: the reverse pass reads every source and
# has to say that support from either is enough, which would be wrong in the
# forward direction.
#
# The filename placeholder is not decoration. `evidence_source` is graded
# against the set of names the prompt handed over, so the prompt has to have
# handed them over — a model cannot name a file it was never shown, and marking
# it wrong for guessing would be measuring the harness.
#
# There is no fourth element for the fidelity fragment, and that is deliberate:
# the fragment is `fidelity/<level>.<prompt name>.md`, so the first element
# already names it. A fourth column would be the same two strings written twice
# and free to disagree — and the one thing worse than a prompt that never hears
# the level is a prompt handed the fragment written for the other direction.
PROMPTS = {
    SOURCE_TO_MERGED: ("verify", "merged_output", "target_filename"),
    MERGED_TO_SOURCES: ("verify_reverse", "sources", "source_filenames"),
}

# The one name a `documents` mapping reserves; everything else in it is a
# source. That is what lets SCHEMA.md's target table be a rule rather than a
# list — the forward pass checks against the merge, the reverse against every
# source there is. A list would have had to say how many, and this module is not
# the one that knows.
MERGED = segment.MERGED_NAME

# What locating a quoted span can conclude. Three outcomes, not a boolean,
# because "not found" and "found somewhere else" are different faults with
# different fixes — see the module docstring.
GROUNDED = "grounded"
TRANSCRIPTION_ERROR = "transcription_error"  # the span exists in no target file
ATTRIBUTION_ERROR = "attribution_error"  # the span exists, in a file not named
NOT_GRADED = "not_graded"  # MISSING asserts no span, so there is none to locate

# The brief's finding vocabulary, derived from (verdict, direction) exactly as
# tests/fixtures/SCHEMA.md specifies. Same label, different failure class: a
# claim missing from the merge was dropped; a claim missing from the sources was
# invented. They land in different sections of the report.
#
# PARTIAL gets a name per direction for the same reason MISSING
# does, and the asymmetry is sharper here than anywhere else in this table: a
# source claim the merge states only part of is a *fact with a piece missing*,
# and a merge claim the sources state only part of is a *fact with a piece
# added*. Reading a report that called both "partial" would tell you a detail
# was in play and not whether the merge lost it or made it up.
#
# Both are findings — `finding != "none"` — and that is a decision rather than a
# default. The whole argument for the label is that neither SUPPORTED nor
# MISSING describes it, so mapping it to "none" would be folding it back into
# SUPPORTED through the back door and passing the run. Whether a finding of this
# class belongs in the exit code or in a review queue is still an open
# question; until then it counts, which is the direction that fails
# loudly rather than quietly.
FINDINGS = {
    ("SUPPORTED", SOURCE_TO_MERGED): "none",
    ("SUPPORTED", MERGED_TO_SOURCES): "none",
    ("CONTRADICTED", SOURCE_TO_MERGED): "contradicted",
    ("CONTRADICTED", MERGED_TO_SOURCES): "contradicted",
    ("MISSING", SOURCE_TO_MERGED): "dropped",
    ("MISSING", MERGED_TO_SOURCES): "hallucinated",
    ("PARTIAL", SOURCE_TO_MERGED): "partially_dropped",
    ("PARTIAL", MERGED_TO_SOURCES): "partially_invented",
    # DERIVED is reachable at `high` only, and in practice only on the reverse
    # pass: it answers "does anything support this merged claim", and a claim
    # taken *from* a source is never derived from two. The forward pair is
    # mapped anyway rather than left out, because `Verdict.finding` indexes
    # this table directly and a missing pair is a KeyError in the middle of a
    # run -- the same reason the assert below exists. Both are "none": a
    # licensed combination is not a defect, which is the whole point of giving
    # it a label instead of letting it arrive as MISSING.
    ("DERIVED", SOURCE_TO_MERGED): "none",
    ("DERIVED", MERGED_TO_SOURCES): "none",
}

# Every label, both directions, and no pair left to a KeyError at report time.
# `Verdict.finding` indexes this with a label the parser has already checked
# against parsing.VERDICTS, so a label added there and forgotten here is a crash
# in the middle of a run rather than at import.
assert set(FINDINGS) == {
    (label, direction)
    for label in parsing.verdicts_for("high")
    for direction in (SOURCE_TO_MERGED, MERGED_TO_SOURCES)
}

# How many claims go in one call. Verifying claims one at a time would be
# cleaner to reason about and is what the accuracy literature does, but it costs
# one round trip per claim, and on a paced local endpoint that is the difference
# between a run of minutes and a run of hours. Batching is a stated trade: the
# whole batch shares a fate, and a batch that cannot be parsed errors every
# claim in it rather than some -- which is what Pass C's salvage narrows to a
# single record.
#
# **The figure is the backend's, not this module's**.
# It is now resolved from `Settings.verify_batch`, because a command backend's
# cost per call is ~26-30 s of fixed plus ~1.3-1.5 s a claim -- measured, four
# batch sizes -- so time per claim falls as the batch grows and 25 there pays
# the fixed part four times where 100 pays it once. This name is the HTTP
# figure and is re-exported rather than moved: two recording harnesses pass it
# explicitly so the corpus keeps the size it was made at, and `config` owns
# the constant for `COMMAND_TIMEOUT`'s reason.
DEFAULT_BATCH = config.DEFAULT_VERIFY_BATCH

# The verify role's output ceiling, sized per batch before the call, the way
# `decompose.budget_tokens` sizes decompose's from the document. Without one,
# a runaway was bounded only by the platform's cut: the 27B's reverse call on
# `attribution_invented` ran for about 275 s and 11,000 characters before it
# was stopped.
#
# What an answer writes is known from the prompt, one record per claim: the
# claim id echoed, a verdict label, an evidence span quoted from the reference
# text, a filename, and a rationale the prompt and the schema cap at
# `parsing.RATIONALE_MAX` characters. The span is sized from the claim it
# answers, as sent (`render_claims`, id included): `EVIDENCE_COPIES` copies,
# one for the id and the span and one because a span is the whole sentence a
# claim may be only part of. `RECORD_SCAFFOLD` is the rest of a record: the
# five key names with their quotes, colons, commas and indentation as the
# recorded answers pretty-print them (137 characters), the braces, and the
# longest verdict label, rounded up to 160.
#
# Checked against every recorded verify answer, not fitted to them: the 334
# in `tests/responses/` (553 with the gitignored `tests/eval/` corpora), none
# cut, the smallest margin 2.64x, the 27B's 1,261 tokens against 3,328
# (`test_verify.test_no_recorded_verify_answer_is_one_the_ceiling_would_cut`).
# `attribution_invented`'s reverse batch, the runaway case above, gets 768 tokens.
EVIDENCE_COPIES = 2
RECORD_SCAFFOLD = 160


def budget_tokens(claims: list[Claim], *, thinking: bool) -> int:
    """`max_tokens` for verifying one batch of `claims`, sized before the call.

    `decompose.budget_tokens`' shape: the answer's expected characters over
    `CHARS_PER_TOKEN`, rounded up to a whole `BUDGET_STEP`, plus one more step
    as the per-response floor, plus `REASONING_ALLOWANCE` with thinking on so
    a reasoning model is not cut while it reasons. A runaway, the
    failure this exists for, stops here instead of at the platform's cut.

    `max_tokens` is a cassette-key component, so this re-keys every verify
    recording made without it: they read UNMEASURED until the operator
    orders the re-record.
    """
    body = sum(EVIDENCE_COPIES * escaped_length(render_claims([claim]))
               + parsing.RATIONALE_MAX + RECORD_SCAFFOLD
               for claim in claims)
    rounded = -(-int(body / CHARS_PER_TOKEN) // BUDGET_STEP) * BUDGET_STEP
    return rounded + BUDGET_STEP + (REASONING_ALLOWANCE if thinking else 0)


def ceiling_for(client: Client, claims: list[Claim]) -> int | None:
    """The ceiling a verify call sends, before the window cut: none on a `CEILING_MODEL` profile.

    Merge's rule for which profiles get one, which decompose follows:
    such a profile sends no ceiling and the endpoint applies its own.
    """
    if (structured.profile_for(client.settings.profile).output_ceiling
            == structured.CEILING_MODEL):
        return None
    return budget_tokens(claims, thinking=client.thinking_for("verify", None))

# Property order is the emission order, and it is load-bearing rather than
# cosmetic. A grammar-constrained model fills these fields in the order the
# schema lists them, so this is the sequence in which the model commits: it
# names the label, then quotes the span that justifies it, then says which file
# the span came from, and only then explains itself. Reasoning last is the
# point. With the rationale first, the argument is written before the label and
# the label is whatever the argument's last clause happened to be — and if the
# argument overruns its cap it is whatever the truncation left behind.
#
# parsing.check_verdicts enforces that the model actually emitted them in this
# order, because a tier without grammar support will not.
def _verdict_item(fidelity: str = "off") -> dict:
    return {
        "type": "object",
        "properties": {
            "claim_id": {"type": "string"},
            "verdict": {"type": "string",
                        "enum": list(parsing.verdicts_for(fidelity))},
            "evidence": {"type": "string"},
            "evidence_source": {"type": "string"},
            "rationale": {"type": "string", "maxLength": parsing.RATIONALE_MAX},
        },
        "required": list(parsing.VERDICT_FIELDS),
        "additionalProperties": False,
    }


def verdict_schema(fidelity: str = "off") -> dict:
    """The schema the endpoint is given, for a run at this level.

    The enum is the level's label set, which is what makes the level-aware
    vocabulary an enforcement rather than an instruction: a model at `off`
    cannot emit DERIVED, because the grammar it was handed has no such value.
    The prose in the fidelity fragment says the same thing, and the prose is
    now the explanation rather than the guarantee.

    Built per call rather than held as four constants because it is small and
    because a mutable dict shared between levels is a defect waiting to be
    written. `VERDICT_SCHEMA` below is the `off` schema and is byte-identical
    to the one that existed before levels were a thing -- that identity is
    what keeps the 373 cassettes at off, low and mid on their existing keys,
    and `test_verify.py` asserts it rather than trusting it.
    """
    return {
        "type": "object",
        "properties": {"verdicts": {"type": "array",
                                    "items": _verdict_item(fidelity)}},
        "required": ["verdicts"],
        "additionalProperties": False,
    }


# One source of truth for the contract, checked rather than duplicated: the
# schema is what the model is told, parsing.VERDICT_FIELDS is what it is graded
# against, and they cannot be allowed to drift apart silently.
assert tuple(_verdict_item()["properties"]) == parsing.VERDICT_FIELDS

# The strict-mode schema, and the default. Every caller that does not name a
# level gets this one, so a path that forgets to thread fidelity through asks
# for the four labels rather than the five.
VERDICT_SCHEMA = verdict_schema()


@dataclass(frozen=True)
class Verdict:
    """The brief's verdict contract, plus what it takes to trust the evidence.

    claim_id, verdict, evidence, evidence_source and rationale are the contract,
    in the order the model emits them. direction and grounding are how the
    verdict earns belief: `finding` is meaningless without knowing which way the
    check ran, and an evidence span nobody located is a claim about the
    reference text rather than a quote from it.

    rationale_names is a diagnostic, not a judgement. It records the other
    labels this verdict's own rationale mentioned, and nothing downstream is
    allowed to change the verdict because of it — see parsing.rationale_conflicts.
    """

    claim_id: str
    verdict: str
    evidence: str
    evidence_source: str
    rationale: str
    direction: str
    grounding: str
    rationale_names: tuple[str, ...] = ()
    # True when this rationale overran RATIONALE_MAX and parsing.parse's
    # pre-pass had to cap it. Informational, not a finding: the label and its
    # grounding are unaffected, so this does not route through `finding` or
    # `FINDINGS` -- it says the argument for the label may have been cut
    # short, not that the label is wrong.
    rationale_capped: bool = False

    @property
    def finding(self) -> str:
        return FINDINGS[(self.verdict, self.direction)]

    @property
    def grounded(self) -> bool:
        """Located, in the file it said. Both halves, or it is not grounded.

        NOT_GRADED is false here on purpose. A MISSING verdict is not grounded;
        it is not the kind of thing grounding applies to, and callers that need
        that distinction read `grounding` rather than this.
        """
        return self.grounding == GROUNDED

    def as_dict(self) -> dict:
        return {**asdict(self), "finding": self.finding, "grounded": self.grounded}


@dataclass(frozen=True)
class Unusable:
    """One verdict the tool refused to grade, and why. Pass C.

    Not a verdict and not a finding. It is the record that a claim was
    submitted and came back unusable, kept so the claim cannot quietly leave
    the denominator: `Run.submitted` counts what a pass was asked, the verdict
    list counts what it answered gradeably, and this is the difference with a
    reason attached.

    `claim_id` is what the record said, which is `""` where it said nothing and
    may name a claim nobody asked about -- it is the model's word, not a
    resolved key, and treating it as one is how an invented id would get
    grafted onto a real claim. `index` is the position in the batch, which is
    what the defect messages already point at.
    """

    claim_id: str
    direction: str
    index: int
    defects: tuple[str, ...]


def target_files(direction: str, documents: dict[str, str]) -> dict[str, str]:
    """The files the target is made of, per SCHEMA.md's target table.

    Returned as a mapping rather than one blob because `evidence_source` is
    graded per file: the reverse pass has every source, and "which of them" is
    the whole question when deciding whether the merge invented something.

    The reverse target is "the mapping minus the merge" rather than a named
    list, so a third source is a target by arriving rather than by being added
    here. That makes an unknown key a source instead of an error, which is the
    trade: `merge.check_sources` is the gate that names them, and it runs first.
    """
    if direction not in PROMPTS:
        raise KeyError(direction)
    if direction == SOURCE_TO_MERGED:
        return {MERGED: documents[MERGED]}
    sources = {name: text for name, text in documents.items() if name != MERGED}
    if not sources:
        raise KeyError(
            f"the reverse direction verifies against the sources and {MERGED} "
            "was the only document given"
        )
    return sources


def reference_text(direction: str, documents: dict[str, str]) -> str:
    """Render the target as the prompt shows it.

    The reverse direction's sources are labelled with their file names,
    because a merged document that correctly surfaces a disagreement says
    *which* source said what, and a claim of that shape is uncheckable against
    an unlabelled blob. The forward direction's single file is not labelled
    here: verify.md prints the name in its own heading, and a second heading
    inside the text would be one more line for a model to quote as evidence.
    """
    files = target_files(direction, documents)
    if direction == SOURCE_TO_MERGED:
        return files["merged.md"]
    return "\n".join(f"--- {name} ---\n{text}" for name, text in files.items())


def render_claims(claims: list[Claim]) -> str:
    """One claim per line, id first. The id is the join key and must come back."""
    return "\n".join(f"{claim.id}: {claim.text}" for claim in claims)


def _checker(expected_ids: list[str], sources: tuple[str, ...],
             fidelity: str = "off"):
    """Semantic check bound to the claims that were actually sent.

    parsing.check_verdicts enforces the closed label set, the field order and
    the evidence coupling, but it cannot know which claims were asked about or
    which files the prompt showed. This adds both, and it is the check that
    stops a short response from becoming a silent MISSING.

    Order is checked, not only membership. A model that answers the right ten
    claims in the wrong order has still read the list as a set, and the next
    thing it drops will be a claim rather than a position — the reorder is the
    cheap, early symptom of that.
    """

    def check(payload: dict) -> list[str]:
        return [error for _, error
                in _split(expected_ids, sources, fidelity)(payload)[0]]

    return check


def _split(expected_ids: list[str], sources: tuple[str, ...],
           fidelity: str = "off"):
    """`_checker`, with every defect paired to the verdict index it belongs to.

    The structured form of the same checks, on `parsing.verdict_defects`'
    terms: an index means one record is at fault, `None` means the answer is.
    `_checker` is the flattening of this and is what the repair loop sends
    back, so a model sees exactly what it saw before. Pass C reads the pairing.

    Two of the three checks added here are response-level and stay that way.
    A claim with no verdict at all is the case the docstring above exists for
    -- it is what stops a short answer becoming a silent MISSING -- and there
    is no record to blame it on, so a batch missing a claim is not salvageable
    at all. Answering the right claims in the wrong sequence is the same shape:
    the fault is in the list, not in any row of it. An invented claim_id is the
    exception, and it is the one that has a record: that row answers a question
    nobody asked, and dropping it leaves the rest of the batch untouched.
    """

    def split(payload: dict) -> tuple[list[tuple[int | None, str]], set[int]]:
        defects, tainted = parsing.verdict_defects(payload, sources, fidelity)
        # `verdict_defects` has already said what a payload that is not an
        # object is, in the wording the repair loop feeds back; the three
        # checks below read it with `.get` and would raise on the way to
        # repeating that. Its complaint is returned as it stands.
        if not isinstance(payload, dict):
            return defects, tainted
        items = [item for item in payload.get("verdicts", []) if isinstance(item, dict)]
        returned = [str(item.get("claim_id", "")).strip() for item in items]
        for missing in sorted(set(expected_ids) - set(returned)):
            defects.append((
                None,
                f"no verdict for claim {missing}; return exactly one verdict "
                f"for every claim id you were given"
            ))
        for invented in sorted(set(returned) - set(expected_ids) - {""}):
            defects.append((
                returned.index(invented),
                f"$.verdicts contains claim_id {invented!r}, which was not in the claim list"
            ))
        if not defects and returned != expected_ids:
            defects.append((
                None,
                f"$.verdicts answers the claims in the wrong order; return one "
                f"verdict per claim in the order given: {', '.join(expected_ids)}"
            ))
        return defects, tainted

    return split


def locate(evidence: str, named: str, files: dict[str, str]) -> str:
    """Where the quoted span actually is, against where the model said it is.

    Three outcomes and a fourth for "not applicable"; see the module docstring
    for why this is not a boolean. Both comparisons are whitespace- and
    case-insensitive, because a model re-wrapping a quote across a line break
    has still quoted it. Anything looser would start accepting paraphrase as
    quotation, which is the thing being measured.

    An empty quote is a transcription error rather than a special case. Nothing
    was located because nothing was offered, and a verdict that owes evidence
    and gives none has failed the same way as one that invented it.
    """
    needle = normalise(evidence)
    if not needle:
        return TRANSCRIPTION_ERROR
    if named in files and needle in normalise(files[named]):
        return GROUNDED
    if any(needle in normalise(text) for text in files.values()):
        return ATTRIBUTION_ERROR
    return TRANSCRIPTION_ERROR


def grounding_of(label: str, evidence: str, named: str, files: dict[str, str],
                 fidelity: str = "off") -> str:
    """locate(), except that MISSING has nothing to locate.

    **`fidelity` decides which labels owe a span, and reading the fixed tuple
    instead was a live hole.** This tested `parsing.EVIDENCED`, which is the
    three-label constant, rather than `parsing.evidenced_for(fidelity)`, which
    adds `DERIVED` at `high`. So every `DERIVED` verdict answered `NOT_GRADED`
    and its quoted span was never located in any file -- and because
    `FINDINGS[("DERIVED", MERGED_TO_SOURCES)]` is `"none"`, a `high` run could
    emit `DERIVED` over a fabricated span and exit 0.

    That is the failure this module's own docstring calls the worst one this
    pass has, "because it is the one that looks most like success".
    `parsing.evidenced_for` was written to prevent exactly it and had one
    caller, which was not this one.

    Defaulting to `off` rather than to the permissive set, for the reason
    `verdicts_for` gives: a caller that forgets to thread the level through
    refuses to grade `DERIVED` rather than grading it against a set that
    silently excuses it.
    """
    if label not in parsing.evidenced_for(fidelity):
        return NOT_GRADED
    return locate(evidence, named, files)


def compose_prompt(
    direction: str,
    policy: MergePolicy,
    prompt: prompts.Prompt | None = None,
) -> tuple[prompts.Prompt, str]:
    """One direction's prompt and the fidelity note that goes into it, hashed together.

    The mirror of `merge.compose_prompt`, and separate from it for the reason
    the two prompts are separate files: the note a grader is given differs by
    direction. `mid.verify.md` says a claim should still be stated in one place;
    `mid.verify_reverse.md` says a claim broader than any single source sentence
    is not covered by the licence. Handing either prompt the other's note would
    describe the same permission from the wrong side.

    Returned as a pair, prompt and text, so the digest is composed from the same
    string that gets substituted. Computing them twice is how a report ends up
    naming a level the model was not shown — which is the failure this task
    exists to close, and worth not reintroducing on the way.

    Only one fragment, so no order question arises here, unlike the merge prompt
    which substitutes fidelity and title and where the sequence is load-bearing.
    """
    name = PROMPTS[direction][0]
    prompt = prompt or prompts.load(name)
    fragment = policy.fragment(name)
    return prompts.compose(prompt, fragment), fragment.text


def salvage(
    failure: SchemaFailure,
    split,
    direction: str,
    index_base: int = 0,
) -> tuple[dict, tuple[parsing.Truncation, ...], tuple[Unusable, ...]] | None:
    """Grade what is gradeable, or nothing. Pass C.

    Returns the payload with the unusable records removed and a record of each
    one removed, or `None` where nothing can be salvaged and the batch must
    fail as it always has.

    **Three conditions, all of them necessary.** There has to be a payload at
    all, which means the last attempt got as far as a schema-valid object --
    a response that was not JSON, or was JSON of the wrong shape, has no
    records to pick over. Every remaining defect has to name a record: one
    that names the response instead is a statement about the answer as a
    whole, and no subset of an answer like that is worth more than the whole
    of it. And at least one record has to survive, since an empty salvage is
    a failed batch described at greater length.

    **What this is not.** It is not a repair and it is not a second chance.
    The model was asked `SCHEMA_ATTEMPTS` times, told exactly what was wrong
    each time in the words of the check that found it, and did not fix it;
    that outcome is unchanged and still reaches the exit code as 2, through
    `Run.unusable`. What changes is only that the eleven records it got right
    stop being destroyed along with the one it got wrong. Nothing is coerced,
    nothing is inferred, and no unusable record contributes a label: the
    difference between the old behaviour and this one is a report that says
    which claim could not be graded instead of a run that says nothing about
    any claim.
    """
    if not isinstance(failure.payload, dict):
        return None
    verdicts = failure.payload.get("verdicts")
    if not isinstance(verdicts, list):
        return None

    defects, tainted = split(failure.payload)
    # The split is a pure function of the payload and `semantic` was built from
    # the same closure, so these are the same defects the repair loop reported,
    # re-derived with their positions attached. Asserted rather than assumed:
    # if the two ever disagree, the tool would be dropping records on the
    # strength of a check that is not the one that failed the batch.
    assert [str(message) for _, message in defects] == list(failure.defects), (
        "salvage re-derived a different defect list than the one that failed "
        f"the batch: {[str(m) for _, m in defects]!r} != {list(failure.defects)!r}")
    if any(index is None for index, _ in defects):
        return None

    by_index: dict[int, list[str]] = {i: [] for i in tainted}
    for index, message in defects:
        by_index.setdefault(index, []).append(str(message))
    if not by_index or set(by_index) >= set(range(len(verdicts))):
        return None

    unusable = tuple(
        Unusable(
            claim_id=str(verdicts[i].get("claim_id", "")).strip()
            if isinstance(verdicts[i], dict) else "",
            direction=direction,
            index=index_base + i,
            defects=tuple(by_index[i]),
        )
        for i in sorted(by_index)
        if 0 <= i < len(verdicts)
    )
    kept = [item for i, item in enumerate(verdicts) if i not in by_index]
    # Renumber, do not merely filter. A `Truncation.path` is a position in the
    # list it was measured against, and dropping a record ahead of it moves
    # every later record up one. The payload handed on is the renumbered list,
    # so a path left pointing at the old slot marks the wrong verdict
    # `rationale_capped`. Truncations on the dropped records go with them: a
    # field capped on a record nobody graded is not a fact about the document.
    moved = {old: new for new, old in enumerate(
        i for i in range(len(verdicts)) if i not in by_index)}
    survived = tuple(
        replace(t, path=f"$.verdicts[{moved[old]}]"
                        + t.path[len(f"$.verdicts[{old}]"):])
        for t, old in ((t, _verdict_index(t.path)) for t in failure.truncations)
        if old in moved
    )
    return {**failure.payload, "verdicts": kept}, survived, unusable


def _verdict_index(path: str) -> int | None:
    """The `N` in `$.verdicts[N]...`, or None for a path outside that list."""
    if not path.startswith("$.verdicts["):
        return None
    closing = path.find("]")
    digits = path[len("$.verdicts["):closing]
    return int(digits) if closing > 0 and digits.isdigit() else None


def verify_claims(
    client: Client,
    claims: list[Claim],
    documents: dict[str, str],
    direction: str,
    prompt: prompts.Prompt | None = None,
    batch_size: int | None = None,
    policy: MergePolicy | None = None,
    unusable: list[Unusable] | None = None,
) -> list[Verdict]:
    """Verify claims against one direction's target. One call per batch.

    `documents` is the fixture's files by name; which of them make up the target
    follows from `direction`. It is passed whole rather than pre-rendered
    because grounding needs the files separately — an evidence span has to be
    looked for in the file the model named, not in the concatenation.

    `policy` is what the merge was *allowed* to do, and both passes have to be
    told it. Without it the reverse pass reads every legitimate rewrite at
    `high` as invention and the tool contradicts the instructions it gave the
    merger; the forward pass has the milder version of the same problem, marking
    a generalisation MISSING because it went looking for the sentence. It
    defaults to `MergePolicy()` — level `off` — which is the same default
    `merge_documents` applies, so a caller that never mentions fidelity has both
    halves agreeing rather than one half guessing.

    Returns verdicts in the order the claims were given, not the order the model
    happened to answer in. Raises client.SchemaFailure if a batch could not be
    made to answer usably; that propagates rather than degrading to MISSING.

    `unusable` is Pass C's opt-in. Left `None`, this
    function behaves exactly as it always has: one unusable record fails the
    batch and the `SchemaFailure` propagates. Given a list, an unusable record
    is dropped, appended to that list, and the rest of the batch is graded --
    and the returned verdicts are then *shorter* than `claims`, which is the
    caller's signal that some claim went unanswered. Salvage is impossible
    without somewhere to write the record down, on purpose: a mechanism that
    can discard a claim silently is worse than one that fails loudly, and
    making the accumulator the switch means the two can never come apart.
    """
    if direction not in PROMPTS:
        raise ValueError(f"unknown direction {direction!r}; expected one of {DIRECTIONS}")
    if not claims:
        return []

    name, text_field, names_field = PROMPTS[direction]
    # The level decides the label set, so it has to be read here rather than
    # left to the schema's default: `verdict_schema()` answers `off`, and a
    # `high` run given the `off` schema could not emit DERIVED at all.
    level = (policy or MergePolicy()).fidelity
    prompt, fidelity_note = compose_prompt(direction, policy or MergePolicy(), prompt)
    files = target_files(direction, documents)
    reference = reference_text(direction, documents)
    sources = tuple(files)
    # Resolved from the backend where the caller stated nothing, which is the
    # pipeline's case. A stated figure is used exactly as stated on
    # either backend -- the two recording harnesses state 25 so the corpus
    # keeps the size it was made at -- and `Settings.verify_batch` is the one
    # place the two defaults differ, the way `call_timeout` already is.
    resolved = (client.settings.verify_batch if batch_size is None
                else batch_size)
    size = max(1, resolved)

    found: dict[str, Verdict] = {}
    for start in range(0, len(claims), size):
        batch = claims[start : start + size]
        split = _split([claim.id for claim in batch], sources)
        messages = [
                {
                    "role": "user",
                    "content": prompt.render(
                        **{
                            text_field: reference,
                            names_field: ", ".join(sources),
                            "claims": render_claims(batch),
                            # The note went last because `render` used to
                            # rescan what it had already substituted, so
                            # whatever went first was exposed to every later
                            # field. `render` became single-pass and the
                            # ordering stopped being load-bearing: the document
                            # above is untrusted and was the field that
                            # mattered, not this one. Kept last anyway, because
                            # the fragment is hand-written in a file where a
                            # stray `{claims}` is a plausible thing to type and
                            # a second reader should not have to re-derive that
                            # it is now harmless.
                            "fidelity_note": fidelity_note,
                        }
                    ),
                }
        ]
        # Same preflight as decompose, and absent here for the same reason it
        # was absent there: only the merge call was ever guarded. A verify
        # prompt carries the merge and a batch of claims, so it is the larger
        # of the two and the likelier to overrun.
        #
        # The ceiling is cut to what the window leaves and the preflight
        # charges the prompt plus one step, on decompose's rule and with its
        # function: the ceiling is a runaway cap, so it must not refuse
        # a batch the window can answer. A replay knows no window and sends
        # the ceiling as is.
        budget = ceiling_for(client, batch)
        if not client.sends_nothing:
            served = client.served_window("verify")
            needed, budget = decompose.fit_to_window(
                budget,
                prompt_tokens=sum(len(str(m.get("content") or "")) for m in messages)
                // window.CHARS_PER_TOKEN,
                served=served)
            window.preflight(
                served,
                needed=needed,
                what=f"verifying a batch of {len(batch)} claim(s)",
                role="verify",
            )
        try:
            completion = client.complete(
                role="verify",
                prompt=prompt,
                messages=messages,
                schema=verdict_schema(level),
                schema_name="emit_verdicts",
                semantic=_checker([claim.id for claim in batch], sources, level),
                max_tokens=budget,
                refuse_at_ceiling=True,
            )
        except SchemaFailure as failure:
            # Pass C. Off unless the caller gave somewhere to record what it
            # refused to grade, and re-raised untouched whenever the answer as
            # a whole is the thing at fault. `start` is added to the index so
            # a record's position names its place in the claim list rather
            # than in whichever batch it happened to land in.
            recovered = (
                None if unusable is None
                else salvage(failure, split, direction, index_base=start)
            )
            if recovered is None:
                raise
            payload, truncations, dropped = recovered
            completion = Completion(payload, truncations)
            unusable.extend(dropped)
            client.usage.salvaged += 1
            client.console.detail(
                f"verify: {len(dropped)} of {len(batch)} record(s) could not be "
                f"graded and were dropped; the rest of the batch stands")
        payload = completion.payload
        capped = {t.path for t in completion.truncations}
        for i, item in enumerate(payload["verdicts"]):
            claim_id = str(item.get("claim_id", "")).strip()
            evidence = str(item.get("evidence", "")).strip()
            evidence_source = str(item.get("evidence_source", "")).strip()
            label = item["verdict"]
            rationale = str(item.get("rationale", "")).strip()
            found[claim_id] = Verdict(
                claim_id=claim_id,
                verdict=label,
                evidence=evidence,
                evidence_source=evidence_source,
                rationale=rationale,
                direction=direction,
                grounding=grounding_of(label, evidence, evidence_source, files, level),
                rationale_names=parsing.conflicting_labels(label, rationale),
                rationale_capped=f"$.verdicts[{i}].rationale" in capped,
            )

    # _checker guarantees the id sets match, so this is a reorder, not a lookup
    # that can miss. Keeping the assertion makes that guarantee visible here.
    # With salvage on, the guarantee weakens in one direction only: a claim can
    # be absent because its record was refused, but nothing may appear that was
    # never asked about. Pass C.
    asked = {claim.id for claim in claims}
    if unusable is None:
        assert found.keys() == asked
    else:
        assert found.keys() <= asked, found.keys() - asked
    return [found[claim.id] for claim in claims if claim.id in found]


# --------------------------------------------------------------------------
# Grading what the merge declared
# --------------------------------------------------------------------------
#
# The rule: the merger declares, the verifier checks. `reconcile.findings` already
# holds a declaration against the two texts — the segment exists, the
# replacement resolves, the disposition is permitted at this level — and every
# one of those is a set difference or a string containment. What none of them
# can ask is whether the *fact* survived, because that is a judgement, and the
# reconciler asks nothing of a model on purpose.
#
# The forward pass has already answered exactly that question, once, for every
# claim. So this grades declarations against verdicts that exist rather than
# going back to the model for a second opinion on the same text.
#
# Nothing here originates a disposition. `Verdict` has no disposition field,
# neither verify prompt names one of `parsing.DISPOSITIONS`, and the function
# below takes no `Client` — three separate statements of the same property,
# because "verify never originates" is true of the whole pass and any one
# assertion would only cover the piece it points at. `tests/test_verify.py`
# checks all three.

CONFIRMED = "confirmed"
REJECTED = "rejected"
UNCHECKED = "unchecked"
GRADES = (CONFIRMED, REJECTED, UNCHECKED)

# What each disposition predicts the forward pass will say about a claim drawn
# from the segment it names. Read off each disposition's own one-line
# definition and nothing else.
#
# `superseded` is the only row with more than one label, and the reason is worth
# stating as a principle: it is the
# only one of the five that describes *where the text came from* rather than
# what happened to the content. The other four each promise something about the
# content — same content in other words, content survives inside a broader
# statement, another segment already carries this content, nothing carries it —
# and a promise about content is falsifiable by a verdict about content.
# `superseded` promises only that another document's version was used instead,
# and that promise is compatible with the replacement saying the same thing
# (SUPPORTED), saying a different value for the same attribute (CONTRADICTED),
# or saying some of it and not contradicting the rest (PARTIAL). Demanding
# SUPPORTED there would reject every correctly-resolved conflict in the suite.
#
# So PARTIAL confirms `superseded` and rejects the other four, and that is the
# whole of what this table decides.
#
# **It rejects `subsumed` deliberately, against the reading that looks obvious.**
# "Survives inside a broader or combined statement" is the shape PARTIAL has, so
# accepting it there is the tempting default — and it is exactly the hole. It
# would make `subsumed` the one declaration that confirms itself by losing
# content: declare it, fold half the fact away, and the grade says the merge
# described itself correctly. This is already flagged: the declared-loss
# budget counts `dropped` only and excludes `subsumed`, and says in as many
# words that if quiet loss turns out to be hiding in `subsumed` it wants its own
# threshold, measured. A PARTIAL against a subsumed segment is the first
# instrument this project has ever had that can see that loss, and confirming it
# would be reading the instrument and throwing away the reading.
#
# Confirming `superseded` on a PARTIAL costs nothing, because a grade is not a
# suppression. The PARTIAL is still a `partially_dropped` finding on the page
# and in the exit code above; the grade says only that the merge's account of
# itself was accurate. Those are two different questions about the same claim
# and this table answers the second one.
#
# `dropped` is the only row predicting absence, and that asymmetry is the point.
# A drop that turns out to be present is a merge describing itself wrongly, and
# it is invisible to the declared-loss budget, which counts records rather than
# checking them. PARTIAL falsifies it as surely as SUPPORTED does: "nothing in
# the merge carries this content" is not true of content the merge carries half
# of.
PREDICTED = {
    "reworded": ("SUPPORTED",),
    "superseded": ("SUPPORTED", "CONTRADICTED", "PARTIAL"),
    "subsumed": ("SUPPORTED",),
    "duplicate": ("SUPPORTED",),
    "dropped": ("MISSING",),
    # A reconciled segment fed a statement built from it and another. Forward,
    # the claim drawn from this segment still has to survive in that statement,
    # so SUPPORTED is what confirms it -- the same prediction `subsumed` makes,
    # because from this segment's side the two look alike. DERIVED is not here:
    # it is what the *reverse* pass says about the combined claim, and this
    # table is about what the forward pass should find for a source segment.
    # Keeping them apart is the point -- a disposition predicts what happens to
    # the segment it names, not what the merged sentence is labelled.
    "reconciled": ("SUPPORTED",),
}

assert tuple(PREDICTED) == parsing.DISPOSITIONS
# Every verdict label appears in at least one row, which means a label cannot be
# added to `parsing.VERDICTS` without someone deciding, per disposition, whether
# it confirms. That is exactly what this assert is for, and it stays for the next
# label rather than being retired now that it has fired once.
assert set().union(*PREDICTED.values()) == set(parsing.VERDICTS)


@dataclass(frozen=True)
class Graded:
    """One declaration, and what the forward pass said about it.

    `claims` carries the ids rather than a count. A rejected declaration a
    reader cannot trace back to a claim is an accusation, and the disposition
    model exists so that a merge can be argued with.

    `reason` and `detail` are two different voices and are kept apart on
    purpose. `reason` is what the merge wrote in its own record -- why it says
    it did this -- and nothing here checks it. `detail` is this module's
    account of how the grade was reached. A reader deciding whether to put a
    dropped fact back needs the first; a reader auditing the grade needs the
    second; and folding either into the other would let the tool's arithmetic
    be read as the merge's argument, or the merge's argument as a finding.
    """

    segment: str
    disposition: str
    grade: str
    detail: str
    claims: tuple[str, ...] = ()
    reason: str = ""
    # The span the merge said now carries this content. Persisted, because
    # every check that reads a declaration turns on it and
    # the report did not keep it: re-scoring a saved report showed every record
    # as "replacement missing", which is indistinguishable from a model that
    # really omitted one. Two defects were mis-diagnosed that way in one
    # session. A report that cannot answer the question its own checks ask is
    # not an audit trail.
    replacement: str = ""

    def as_dict(self) -> dict:
        return asdict(self)


def attribute(claims: list[Claim], documents: list[segment.Document]) -> dict[str, str]:
    """Claim id -> the one segment of its own source whose text contains its span.

    Mechanical, and it refuses ties. A span that flattens into two segments of
    the same document attributes to neither: picking one would decide a
    declaration's grade by list order, and a grade assigned by list order is
    worse than no grade, which is a thing this function is allowed to return.

    `claim.anchored` is not consulted. It records whether `decompose.anchor`
    found the span in a line of the source, which is a stricter search than this
    one — `flatten` collapses the line wrapping that makes it fail — so a claim
    landing in exactly one segment here has been located whatever that flag says.
    """
    by_file = {document.filename: document for document in documents}
    found: dict[str, str] = {}
    for claim in claims:
        document = by_file.get(claim.source)
        needle = reconcile.flatten(claim.span)
        if document is None or not needle:
            continue
        hits = [
            item.id
            for item in document.segments
            if reconcile.occurs(needle, reconcile.flatten(item.text))
        ]
        if len(hits) == 1:
            found[claim.id] = hits[0]
    return found


# What a disposition predicts about the *text* of the segment it names, for the
# declarations no claim reaches. `reconcile.locate` puts every source segment in
# one of three states against the merge, and two of them are observations: a
# segment is `present` because its flattened text was found in the merged text,
# and `absent` because it was not. `reworded` is neither — it is a similarity
# score above a threshold, and it decides nothing here, which is why every row
# below leaves it out.
#
# Only the rows a location can settle are here. `superseded` and `subsumed` are
# absent on purpose: both say the content survives inside some other segment's
# words, so neither is falsified by this segment's text being gone nor confirmed
# by it being there. A title declared `superseded` is not left to this table —
# `reconcile._title_checks` decides it, on the merged title itself, and
# `TITLE_NOT_SUPERSEDED` is where that answer is reported.
#
# `reconciled` is absent for exactly that reason and not a new one, which is
# why this comment is extended rather than joined by a second. It says the
# content survives inside a statement built from this segment and another, so
# the segment's own text being gone is what it predicts and its being present
# refutes nothing. What a location cannot settle here is not a gap: the
# Declarations table reads `unchecked` for it, and `unchecked` is the honest
# answer, because whether a combination is *sound* is an entailment question
# and nothing in this module reads meaning. The mechanical half is checked
# elsewhere and in full -- `UNRESOLVED_REPLACEMENT` requires the declared
# replacement to resolve in the merged document, and check 1 requires every
# segment a record names to exist -- so a reconciliation that was invented
# rather than performed is still caught. Soundness belongs to the reverse
# pass, where `DERIVED` is the label for it, and that pass asks a model.
#
# The three rows above are the whole of what a location can decide.
LOCATED = {
    # declared     confirmed by         rejected by
    "dropped":    (reconcile.ABSENT,    reconcile.PRESENT),
    "duplicate":  (reconcile.PRESENT,   reconcile.ABSENT),
    # A segment declared reworded and found in the merge unchanged was not
    # reworded. The other direction does not follow: text that is gone from the
    # merge as written is what a rewrite looks like to a string comparison, so
    # absence confirms nothing.
    "reworded":   ("",                  reconcile.PRESENT),
}
assert set(LOCATED) <= set(parsing.DISPOSITIONS)


def _by_title(
    record_id: str,
    disposition: str,
    titles: dict[str, str],
    merged_title: str,
    charged: set[str],
) -> Graded | None:
    """Grade one declaration on a source title, using the check that already ran.

    `reconcile._title_checks` is the only thing in the package that can see a
    title -- `decompose.md` is told to skip headings, so no claim is ever drawn
    from one -- and it visits every source title that is not the merged title,
    emitting `TITLE_NOT_SUPERSEDED` unless the segment carries a `superseded`
    record whose replacement resolves to the title that was kept. That is a
    decision, made mechanically, about exactly the declaration being graded
    here, and leaving it `unchecked` reported the answer as absent while it sat
    in the findings list.

    So this reads that answer rather than recomputing it: charged means the
    check rejected the declaration, and not charged means it visited the segment
    and passed it. The `merged_title` guard is what makes the second half true.
    A title the merge kept is skipped by that loop, so its absence from
    `charged` means nothing was asked, not that something passed.

    The same rule `LOCATED` applies: read what already ran, never recompute it.
    """
    text = titles.get(record_id)
    if text is None or not merged_title or text == merged_title:
        return None
    if record_id in charged:
        return Graded(record_id, disposition, REJECTED,
                      f"no claim is drawn from a title, and the title check rejected "
                      f"this one: it is not the merged title and its {disposition!r} "
                      f"record does not name the title that replaced it")
    if disposition != "superseded":
        return None
    return Graded(record_id, disposition, CONFIRMED,
                  f"no claim is drawn from a title, and the title check passed this "
                  f"one: it is superseded by {merged_title!r} and says so")


def _by_text(record_id: str, disposition: str, located: dict) -> Graded | None:
    """Grade one claimless declaration on where its text ended up, or decline to.

    Returns `None` when the location says nothing about this disposition, which
    leaves the caller to report it `unchecked` in its own words. Declining is
    the common case and has to stay cheap to reach: this is a second-choice
    grader, and the reason it exists is that the first choice cannot see a
    heading at all.
    """
    item = located.get(record_id)
    if item is None or disposition not in LOCATED:
        return None
    confirms, rejects = LOCATED[disposition]
    where = (
        f"its text is in the merge" if item.verdict == reconcile.PRESENT
        else f"its text is not in the merge"
        if item.verdict == reconcile.ABSENT
        else f"the nearest merge segment matches it at {item.ratio:.2f}, which is a "
             f"reading of a similarity score and not an observation"
    )
    if item.verdict == confirms:
        return Graded(record_id, disposition, CONFIRMED,
                      f"no claim was drawn from this segment, and {where}, which is "
                      f"what {disposition!r} says happened to it")
    if item.verdict == rejects:
        return Graded(record_id, disposition, REJECTED,
                      f"declared {disposition!r}, and {where}")
    return None


def _covering(disposition: str, replacement: str, fidelity: str,
              documents: dict[str, str]) -> bool:
    """Is this record a covering reconciliation, by check 5's own test?

    Three conditions, and all three are the ones `reconcile.verbatim` already
    applies, asked through the same function so the two cannot drift: the
    level permits covering, the disposition is `reconciled`, and every number
    in the replacement is a number some source states.

    The third is what keeps this from becoming a way to declare a
    contradiction away. A merge that narrows `30-45%` and `35-50%` to
    `35-45%`, or widens them to `30-60%`, fails it -- the first because
    narrowing is a loss rather than a covering, the second because no document
    wrote 60 -- and both are charged as they were before.
    """
    if disposition != "reconciled" or not reconcile.COVERS.get(fidelity):
        return False
    return reconcile.covers_the_sources(replacement, documents)


def grade_declarations(
    dispositions: tuple[dict, ...],
    verdicts: list[Verdict],
    claims: list[Claim],
    documents: dict[str, str],
    located: reconcile.Reconciliation | None = None,
    findings: tuple[reconcile.Finding, ...] | None = None,
    fidelity: str = "off",
) -> tuple[Graded, ...]:
    """Confirm or reject each declared disposition. Never originate one.

    `dispositions` is what the merge said it did, `verdicts` and `claims` are
    what the forward pass found, and `documents` is the mapping both were built
    from. The sources come out of it by `target_files`, which is already the
    module's rule for which documents are sources, so this is not a second
    opinion about that.

    Three outcomes and not two. `unchecked` is what a declaration gets when no
    claim was drawn from the segment it names — decompose skips headings,
    formatting and boilerplate by design, so a superseded title has no claim and
    never will — and calling that confirmed would turn every unexamined
    declaration into a pass. It is the same failure the coverage section exists
    to prevent, one level down.

    `located` is the reconciler's own measurement of the same two texts, and it
    is asked only about the declarations the forward pass cannot reach. It is
    not a second opinion: `LOCATED` lists the three dispositions a string
    comparison can settle, and a declaration it does not settle stays
    `unchecked` with the reason it already had. Without it the grader behaves
    exactly as before, which is what `verify` runs on, since nothing there
    declared anything.

    Declarations come back in the order they were declared, one per record.
    First record per segment wins, as in `reconcile.findings`: `parsing.check_merge`
    rejects a duplicate segment id before this runs, so a second one means
    unchecked output, and taking the last would make the applicable rule depend
    on ordering.
    """
    graded = {
        item.claim_id: item for item in verdicts if item.direction == SOURCE_TO_MERGED
    }
    where_text = {} if located is None else {
        item.segment.id: item
        for coverage in located.coverages
        for item in coverage.located
    }
    titles: dict[str, str] = {} if located is None or findings is None else {
        item.id: item.text
        for coverage in located.coverages
        for item in reconcile.titles_of(coverage.document.segments)
    }
    merged_titles = () if located is None else reconcile.titles_of(located.merged)
    merged_title = merged_titles[0].text if merged_titles else ""
    charged = {
        finding.segment for finding in (findings or ())
        if finding.kind == reconcile.TITLE_NOT_SUPERSEDED and finding.segment
    }
    where = attribute(claims, segment.segment_sources(target_files(MERGED_TO_SOURCES, documents)))
    by_segment: dict[str, list[str]] = {}
    for claim_id, segment_id in sorted(where.items()):
        if claim_id in graded:
            by_segment.setdefault(segment_id, []).append(claim_id)

    out: list[Graded] = []
    seen: set[str] = set()
    for record in dispositions:
        identifier = str(record.get("segment", "")).strip()
        disposition = str(record.get("disposition", ""))
        # The merge's own words, carried through ungraded. `parsing.check_merge`
        # has already refused a record without one, so an empty string here is a
        # `verify` run or a hand-built record rather than a merge that stayed
        # silent -- and the report says which of those it is.
        reason = str(record.get("reason", "")).strip()
        # Kept on the record so a saved report can answer the question
        # the checks ask of it. `.get(key, "")` does not protect against a
        # key present with a null value, which every model writes.
        _raw_replacement = record.get("replacement")
        replacement = str(_raw_replacement) if _raw_replacement is not None else ""
        if identifier in seen:
            continue
        seen.add(identifier)
        expected = PREDICTED.get(disposition)
        # A covering reconciliation predicts a wider set than a combining one.
        # `PREDICTED` is read off each disposition's own definition and says
        # `reconciled` promises the segment's claim survives -- SUPPORTED --
        # which is right when two documents state complementary halves of one
        # fact. It is wrong for the other thing this disposition carries at
        # `open`: a value covering two disagreeing ranges asserts a range the
        # *narrower* source denies at one edge, so that source's claim comes
        # back CONTRADICTED **by construction**. Demanding SUPPORTED rejects
        # every correctly-covered conflict, which is the same argument the
        # `superseded` row already makes one table up, and that is exactly
        # what one live run found: the prompt granted the licence, check 5
        # honoured it, and this line refused it.
        #
        # Narrow on purpose, and on the same three conditions check 5 uses:
        # the level, the disposition, and the replacement actually being built
        # from figures the documents wrote. A `reconciled` record whose
        # replacement carries a number no document states widens nothing and
        # is charged exactly as before.
        if _covering(disposition, replacement, fidelity, documents):
            expected = tuple(dict.fromkeys(expected + ("CONTRADICTED",)))
        supporting = tuple(by_segment.get(identifier, ()))
        if expected is None:
            out.append(Graded(
                identifier, disposition, UNCHECKED,
                f"{disposition!r} is not one of {', '.join(parsing.DISPOSITIONS)}, so "
                f"there is nothing it predicts; parsing.check_merge rejects this "
                f"before a graded run can reach here",
                reason=reason, replacement=replacement,
            ))
        elif not supporting:
            unchecked = Graded(
                identifier, disposition, UNCHECKED,
                f"no claim was drawn from this segment, so the forward pass says "
                f"nothing about whether {disposition!r} is what happened to it"
                + ("; the reconciler did not locate it either"
                   if located is not None and identifier not in where_text else ""),
                reason=reason, replacement=replacement,
            )
            decided = (
                _by_title(identifier, disposition, titles, merged_title, charged)
                or _by_text(identifier, disposition, where_text)
            )
            out.append(unchecked if decided is None
                       else replace(decided, reason=reason,
                                    replacement=replacement))
        else:
            wrong = tuple(
                claim_id for claim_id in supporting
                if graded[claim_id].verdict not in expected
            )
            if wrong:
                out.append(Graded(
                    identifier, disposition, REJECTED,
                    f"declared {disposition!r}, which predicts "
                    f"{' or '.join(expected)}; "
                    + ", ".join(f"{c} came back {graded[c].verdict}" for c in wrong),
                    claims=wrong, reason=reason, replacement=replacement,
                ))
            else:
                out.append(Graded(
                    identifier, disposition, CONFIRMED,
                    f"declared {disposition!r} and every claim from it came back "
                    f"{' or '.join(expected)}",
                    claims=supporting, reason=reason, replacement=replacement,
                ))
    return tuple(out)


# ---------------------------------------------------------------------------
# The coverage pass: one call per source, extraction and judgement together.
#
# `--verify-depth coverage` trades the reverse pass and the separate decompose
# calls for a single call per source. It is the shape the prior art this tool
# was written against uses, and the reason to have it is cost: decompose alone
# is 28-41% of a run's spend, measured on two vendor runs.
#
# What it cannot do is the whole point of naming it `coverage` rather than
# `fast`. It only ever asks whether source content survived into the merge.
# Nothing asks whether the merge asserts anything its sources do not, so
# invention is not detected at all -- not detected less well, not detected
# sometimes. The report has to say so where the verdict is read.
#
# The nine mechanical checks in `reconcile` run in both depths. They cost no
# model call, and they are most of what a clean run proves.

COVERAGE = "coverage"
FULL = "full"
DEPTHS = (FULL, COVERAGE)

# The fused pass judges a source claim against the merged document, which is
# exactly what the forward pass does, so it is handed the forward pass's own
# fidelity fragment rather than a fifth set of files. The judging rules are
# identical and two copies of them would be free to disagree; the extraction
# rules, which are the half that differs, are in the base prompt where no
# level varies them.
COVERAGE_FRAGMENT_ROLE = SOURCE_TO_MERGED

# `claim_id` is not in the model's contract. The claims come back in document
# order and are numbered by position, the way `decompose` numbers them, so a
# run at either depth produces the same id for the same claim and a report can
# be read across the two.
COVERAGE_FIELDS = parsing.COVERAGE_FIELDS


def _coverage_item(fidelity: str = "off") -> dict:
    """One extracted-and-judged claim.

    The first three fields are `decompose`'s, character for character, and the
    rest are `_verdict_item`'s minus `claim_id`. Reusing both sets rather than
    inventing a third is what lets `Claim` and `Verdict` be built from this
    payload without a translation layer that could quietly disagree with either.
    """
    return {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "line": {"type": "integer"},
            "span": {"type": "string"},
            "verdict": {"type": "string",
                        "enum": list(parsing.verdicts_for(fidelity))},
            "evidence": {"type": "string"},
            "evidence_source": {"type": "string"},
            "rationale": {"type": "string", "maxLength": parsing.RATIONALE_MAX},
        },
        "required": list(COVERAGE_FIELDS),
        "additionalProperties": False,
    }


# Same contract as the two it is made of, asserted rather than trusted.
assert tuple(_coverage_item()["properties"]) == COVERAGE_FIELDS
assert COVERAGE_FIELDS[:3] == ("text", "line", "span")
assert COVERAGE_FIELDS[3:] == parsing.VERDICT_FIELDS[1:]


def coverage_schema(fidelity: str = "off") -> dict:
    return {
        "type": "object",
        "properties": {"claims": {"type": "array",
                                  "items": _coverage_item(fidelity)}},
        "required": ["claims"],
        "additionalProperties": False,
    }


def verify_coverage(
    client: Client,
    text: str,
    source: str,
    documents: dict[str, str],
    prompt: prompts.Prompt | None = None,
    policy: MergePolicy | None = None,
) -> tuple[list[Claim], list[Verdict]]:
    """Extract this source's claims and judge each against the merge. One call.

    Returns the claims and the verdicts as two lists in the same order, rather
    than one list of pairs, because every reader downstream already takes those
    two shapes. A claim with no verdict cannot occur here: the model emits them
    together or the call fails, which is the one real advantage of fusing them.

    Raises `SchemaFailure` if the model could not be made to answer usably,
    for `decompose_text`'s reason -- zero claims and a failed call look
    identical in a coverage table and mean opposite things.

    **No `unusable` accumulator, and that is a decision rather than an
    omission**. Pass C drops the record a verify
    batch could not grade and keeps the rest; here the record *is* the claim,
    so dropping it would delete the evidence that the claim was ever extracted
    and renumber every claim after it -- `decompose.claim_id` numbers by
    position, so a report at this depth would stop being readable against a
    report at `full`, which is the one property the fused pass is built to
    keep. `decompose_text` has never salvaged either, for the same reason and
    with the same cost: one unusable record loses the source. `verify.salvage`
    refuses this payload outright, since it looks for `$.verdicts`.
    """
    policy = policy or MergePolicy()
    level = policy.fidelity
    merged = documents.get(MERGED, "")
    prompt, fidelity_note = compose_prompt(
        COVERAGE_FRAGMENT_ROLE, policy, prompt or prompts.load("verify_coverage"))
    rendered = prompt.render(
        source_filename=source,
        document=decompose.number_lines(text),
        target_filename=MERGED,
        merged_output=merged,
        fidelity_note=fidelity_note,
    )
    # This prompt carries two whole documents, so it is the largest thing this
    # tool sends after the merge itself. The forward pass guards its batches
    # and `decompose` guards its document; fusing them without the guard would
    # drop the check exactly where it is most needed.
    if not client.sends_nothing:
        window.preflight(
            client.served_window("verify"),
            needed=len(rendered) // window.CHARS_PER_TOKEN,
            what=f"covering {source or 'a document'} against {MERGED}",
            role="verify",
        )
    # The one file the prompt showed, under the name the prompt gave it: the
    # only filename an `evidence_source` may name and the only text a span may
    # be located in. Read before the call rather than after it, because the
    # semantic check needs it -- `check_coverage` given no filenames checks
    # the shape of an attribution and not its truth, which is the weaker half
    # of the same check.
    #
    # Built from `merged` rather than through `target_files`, which
    # subscripts `documents[MERGED]`. Under `--dry-run` there is no merged
    # document to subscript -- the merge was planned, not made -- and a
    # KeyError here would turn a planned step into an errored one. The mapping
    # is what `target_files(SOURCE_TO_MERGED, ...)` returns on every run that
    # has one.
    files = {MERGED: merged}
    completion = client.complete(
        role="verify",
        prompt=prompt,
        messages=[{"role": "user", "content": rendered}],
        schema=coverage_schema(level),
        schema_name="emit_coverage",
        semantic=lambda payload: parsing.check_coverage(
            payload, tuple(files), level),
    )
    payload = completion.payload
    # Kept rather than discarded with the rest of the `Completion`. A capped
    # rationale is a fact about the answer and the report has a section for
    # it; taking `.payload` alone made `rationale_capped` False on every
    # coverage verdict and printed "None." under a run that had capped one.
    # The distinction matters: a rationale capped here must still read as capped.
    capped = {t.path for t in completion.truncations}

    lines = text.splitlines()
    claims: list[Claim] = []
    verdicts: list[Verdict] = []
    for i, item in enumerate(payload["claims"]):
        if not isinstance(item, dict):
            continue
        claim_text = str(item.get("text", "")).strip()
        span = str(item.get("span", "")).strip()
        if not claim_text:
            continue

        reported = item.get("line")
        reported = reported if isinstance(reported, int) else 0
        reported = max(1, min(reported, len(lines))) if lines else 1
        line, anchored = decompose.anchor(span, reported, lines)

        identifier = decompose.claim_id(source, len(claims) + 1)
        claims.append(Claim(id=identifier, source=source, text=claim_text,
                            line=line, span=span, anchored=anchored))

        label = str(item.get("verdict", "")).strip()
        evidence = str(item.get("evidence", ""))
        # Taken as given, with no fallback. This used to read `or MERGED`,
        # which turned "the model named no file" into "the model named the
        # merge" -- and `locate` then found the span in the file the tool had
        # supplied, so an unattributed quote came back `grounded`. The same
        # reply at `full` came back `attribution_error`, because
        # `verify_claims` keeps the empty string and lets the check fail it.
        # A missing attribution is a finding; supplying the only plausible
        # answer on the model's behalf is the tool deciding the result.
        named = str(item.get("evidence_source", "")).strip()
        rationale = str(item.get("rationale", ""))
        verdicts.append(Verdict(
            claim_id=identifier,
            verdict=label,
            evidence=evidence,
            evidence_source=named,
            rationale=rationale,
            direction=SOURCE_TO_MERGED,
            grounding=grounding_of(label, evidence, named, files, level),
            rationale_capped=f"$.claims[{i}].rationale" in capped,
        ))
    return claims, verdicts
