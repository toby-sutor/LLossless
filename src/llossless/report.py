"""The Markdown report, and the exit code that has to agree with it.

Separate from `cli.py` because it is the one part of the command with no I/O in
it: given a finished `Run` it returns a string, so every claim the report makes
can be asserted without a subprocess, an endpoint or a temporary directory.

Two rules shape the whole file.

**The denominator comes before the finding.** A findings list is not evidence
of anything until you know how much was examined to produce it, and the failure
mode this project exists to catch — a check that examined nothing and therefore
passed — is invisible in any report that leads with "no faults found". Coverage
is section two of four and the verdict line above it never says "clean" without
saying over what.

**A ratio with a zero denominator is not printed as a ratio.** `0/0` reads as a
measurement; it is the absence of one. Where a pass errored before it graded
anything the cell says so in words, because a reader skimming for numbers will
take `0/0` for a perfect score often enough to matter.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import config, merge, numerals, parsing, usage
from . import reconcile as reconcile_module
from .decompose import Claim
from .provenance import Provenance
from .reconcile import (
    CHECKS,
    DOCUMENT_FINDINGS,
    DUPLICATED_CONTENT,
    FINDING_KINDS,
    PROMPT_EXAMPLE_LEAK,
    RECORD_FINDINGS,
    Finding,
    Order,
    Reconciled,
    flatten,
    occurs,
    over_budget,
)
from .verify import (
    CONFIRMED,
    FINDINGS,
    GROUNDED,
    MERGED,
    MERGED_TO_SOURCES,
    NOT_GRADED,
    REJECTED,
    SOURCE_TO_MERGED,
    Graded,
    Unusable,
    Verdict,
)

# Findings, in the order they are reported. Dropped first: it is the failure the
# tool was built for, and the one a reader is least able to spot unaided. Each
# partial sits directly under the whole-claim failure it is the quiet version
# of, because that is the pair a reader has to tell apart.
FINDING_ORDER = (
    "dropped",
    "partially_dropped",
    "contradicted",
    "hallucinated",
    "partially_invented",
)

HEADINGS = {
    "dropped": "Dropped — in a source, not in the merge",
    "partially_dropped": "Partly dropped — the merge carries some of this claim",
    "contradicted": "Contradicted — the merge states something different",
    "hallucinated": "Invented — in the merge, in neither source",
    "partially_invented": "Partly invented — the sources carry some of this claim",
}

# The report names every finding the verify layer can produce. A finding class
# with no heading would print as a KeyError at the moment someone most needs the
# report, so the two are checked against each other here rather than trusted.
assert set(HEADINGS) == set(FINDING_ORDER) == set(FINDINGS.values()) - {"none"}

# The reconciler's ten kinds, reported in `reconcile.FINDING_KINDS` order, which
# is `docs/M7-prompts/NOTES.md`'s order, so the section and the rules it enforces
# can be read side by side. These are failures of *structure* rather than of
# claims: no model produced any of them and none of them came out of a verdict.
# Twelve kinds from nine checks -- `reconcile.CHECKS` is the number the prose
# below quotes, and the two are not interchangeable.
STRUCTURAL_HEADINGS = {
    "undeclared_absence": (
        "Absent and undeclared — in a source, not in the merge, and no record explains it"
    ),
    "undeclared_rewording": (
        "Reworded and undeclared — in the merge in altered wording, and no record explains it. "
        "At off this also covers layout: a segment whose source line breaks the merge ran "
        "together is altered and undeclared, and 380 reuses this kind rather than moving "
        "FINDING_KINDS off 12"
    ),
    # Reads as the opposite of the two above on purpose: those are the merge
    # saying nothing where it owed an account, this is the merge giving an
    # account of something that did not happen. Says "still here" rather than
    # anything about absence, because the operator's first question on seeing
    # this is whether they have lost the segment, and they have not.
    "false_departure": (
        "Declared gone, still here — a record says the content departed and the "
        "merge carries the segment unchanged"
    ),
    "invented_segment": "Invented segment — a record names a segment neither source has",
    "unresolved_replacement": (
        "Unresolved replacement — a record points at text the merge does not contain"
    ),
    "disposition_not_permitted": (
        "Not permitted here — the merge declared something this fidelity level forbids"
    ),
    "verbatim_violation": "Verbatim violation — an invariant-core token did not survive unchanged",
    "declared_loss_over_budget": "Over budget — declared loss past the ceiling",
    "title_not_from_source": "Title not from a source — the merged title was written, not kept",
    "title_not_superseded": (
        "Title dropped in silence — a source title is gone and no record names what replaced it"
    ),
    # One heading, two halves: a whole segment repeated character for character,
    # and one claim extracted from two different lines. The second is what a
    # merge that keeps both sources' wordings of the same fact looks like, and
    # it is the reason the heading no longer says "character for character" on
    # its own.
    "duplicated_content": (
        "Stated twice — the merged document says the same thing more than once, "
        "either as a repeated segment or as one claim drawn from two lines"
    ),
    "prompt_example_leak": (
        "Prompt example returned — the merge carries a word from `merge.md`'s "
        "worked example and from neither source"
    ),
}

# Same guard as above, for the same reason: a kind added to `reconcile` and not
# to this table would raise a KeyError while rendering the very finding it names.
assert set(STRUCTURAL_HEADINGS) == set(FINDING_KINDS)

# What each direction's findings are called in the inventory tables, where the
# subject is one claim rather than a class of failure. `HEADINGS` above names
# the failure and reads as an accusation; a table has a row for every claim,
# most of which are fine, so the same five findings need a word that fits a
# clean row too. The words are the report's own: the verdict line already says
# "carried only in part" and the coverage table already says "supported only in
# part".
#
# `partially_dropped` reads "partly kept", the page's word too (717, 720).
#
# Two tables and not one because the same finding means opposite things by
# direction. `contradicted` is the only label that reads the same either way.
FORWARD_STATUS = {
    "none": "carried",
    "partially_dropped": "partly kept",
    "dropped": "dropped",
    "contradicted": "contradicted",
}

REVERSE_STATUS = {
    "none": "supported",
    "partially_invented": "supported in part",
    "hallucinated": "invented",
    "contradicted": "contradicted",
}

# Neither table may be missing a finding the direction can actually produce: a
# gap would be a KeyError rendering the row of the one claim it applies to.
# Derived from `FINDINGS` rather than listed again, so a sixth label added
# there fails at import instead of at the report.
assert set(FORWARD_STATUS) == {
    finding for (_, direction), finding in FINDINGS.items()
    if direction == SOURCE_TO_MERGED
}
assert set(REVERSE_STATUS) == {
    finding for (_, direction), finding in FINDINGS.items()
    if direction == MERGED_TO_SOURCES
}

# The order the counts are summarised in, per direction, and the order the
# rows are grouped in below. Findings first, clean last: a reader looking at a
# 40-row table wants the four rows that went wrong at the top of it.
FORWARD_ORDER = ("dropped", "contradicted", "partially_dropped", "none")
REVERSE_ORDER = ("hallucinated", "contradicted", "partially_invented", "none")
assert set(FORWARD_ORDER) == set(FORWARD_STATUS)
assert set(REVERSE_ORDER) == set(REVERSE_STATUS)

# What a claim nothing came back about is called. Not a finding and not a pass:
# the pass errored or was skipped, and a table that left the row out would have
# a claim count above it that its own rows do not add up to.
NOT_CHECKED = "not checked"

# What a step's outcome means for the run. `planned` is --dry-run: the call was
# counted and not made, which is neither an answer nor a fault.
OK, ERRORED, PLANNED, SKIPPED = "ok", "errored", "planned", "skipped"


# How `cli.step` records a unit the web server's cancel stopped (639): the
# exception's class name, then its message. `verdict_line` reads it.
CANCELLED_PREFIX = "Cancelled:"


@dataclass
class Step:
    """One unit of work, and what became of it.

    The step list is the report's own denominator: without it a run that made
    two calls and a run that made five are indistinguishable from their output,
    which is the whole complaint this file opens with.
    """

    name: str
    state: str
    detail: str = ""


@dataclass
class Run:
    """Everything the report needs, and nothing that would let it make a call."""

    command: str
    # Canonical name -> the path the caller actually gave. The prompts are shown
    # `source_a.md` because that is the configuration every published figure was
    # measured under; the report is shown a short name built from the caller's
    # own path (see `display`), because a report of caller-supplied absolute
    # paths is one nobody can scan.
    paths: dict[str, str] = field(default_factory=dict)
    steps: list[Step] = field(default_factory=list)
    claims: dict[str, list[Claim]] = field(default_factory=dict)
    forward: list[Verdict] = field(default_factory=list)
    reverse: list[Verdict] = field(default_factory=list)
    merged: str | None = None
    merged_written_to: str | None = None
    # Carried from the merge result to the provenance block, which is built
    # after the pipeline has run and cannot ask the merge what it did. None on
    # `verify`, where no merge happened and there is nothing to name.
    base: str | None = None
    base_chosen: str | None = None
    # What the merge declared it did to its sources, graded against the forward
    # verdicts. Empty on `verify`, where no merge ran and nothing was declared —
    # which is why `declarations_section` keys off the command rather than off
    # the length of this, since an empty list means two different things.
    declarations: tuple[Graded, ...] = ()
    # What the merge said it chose between, carried unread. At `high` a
    # decision records a choice; at `off`, `low` and `mid` the merge may not
    # choose, so a decision with no `chosen` is how a disagreement is recorded
    # at all -- the document may not carry a marker and the reconciler cannot
    # derive one (383). Ungraded here for the same reason `Graded.reason` is:
    # whether the conflict is real is a judgement, and nothing in this module
    # makes judgements.
    decisions: tuple[dict, ...] = ()
    # What the merge said it added from outside the documents, carried unread
    # and gradeable by nothing here (482). Empty at every level but `open`.
    #
    # Ungraded is the honest state rather than a gap: the sources are the only
    # ground truth this tool has, so a statement they do not carry cannot be
    # checked against them. What the declaration buys is that the statement is
    # *listed* instead of being reported as an invention -- an addition the
    # merge did not declare is still `hallucinated` and still exits 1.
    additions: tuple[dict, ...] = ()
    # One sentence from the merge saying these documents may not belong
    # together (497). Reported, never graded, and it moves no exit code: the
    # operator asked for "a friendly hint", not a fourth failure class.
    mismatch: str = ""
    # The title policy in force, and how many sources gave it something to
    # name. Zero is not a defect: a plain-text document whose first line runs
    # straight into the body has no title segment, so `keep-base` has no
    # referent and the report says so rather than the reconciler firing (386).
    title_policy: str = ""
    sources_with_a_title: int = 0
    # How many segments the sources were cut into, which is the denominator of
    # the declared-loss budget (§2.6) and of nothing else. Set by the pipeline
    # because it is a fact about the input documents, which this object does not
    # hold; 0 on a `verify` run, where nothing declared anything and the budget
    # has nothing to be a fraction of.
    segments: int = 0
    # Line breaks the merge introduced that no source segment carries (391).
    # A count, not a verdict: `high.merge.md` licenses restructuring and no
    # level forbids adding a break, so there is nothing here for a check to
    # fail. It is published because 378 made an interior break recorded
    # notation rather than a segment boundary, which is what keeps the
    # partition fixed and is also what makes added structure invisible.
    added_breaks: tuple[tuple[str, str], ...] = ()
    # (document name, line, reason) for a fence that was opened and never
    # closed. Reported, never repaired: everything after the opener is one
    # code block, which is what the document literally says.
    unclosed_fences: tuple[tuple[str, int, str], ...] = ()
    # The ceiling `segments` is measured against, as it was in force for this
    # run -- not the registered default. It is a field rather than a lookup
    # because a report is read long after the run, and `over_budget: false`
    # cannot be told from a generous ceiling without it. Written into the
    # record by `declared_loss` below.
    declared_loss_budget: float = config.DEFAULT_DECLARED_LOSS_BUDGET
    # What the reconciler made of the merge, or None when it did not run. The
    # difference matters more here than anywhere else in this object: an empty
    # `Reconciled` means nine checks were made and found nothing, and None
    # means nothing was checked. Collapsing the two into an empty tuple would
    # print "no structural finding" over a merge nobody examined, which is the
    # exact failure this file's opening paragraph is about. M7 task 36.
    reconciled: Reconciled | None = None
    # `merge.md`'s worked-example words found in the merged document, one
    # `Finding` each, or empty on any run that produced no merge. Set by the
    # pipeline rather than by the reconciler, which has never read a prompt and
    # would have to be handed the word list to do this.
    #
    # A finding and not a raised error, unlike the sibling assertion over
    # extracted claims in `tests/fixtures/GLOBAL.json`: a document carrying
    # `marlbrook` is wrong in a way the operator has to see, and a merge command
    # that dies rather than writing its report leaves them nothing to look at.
    # It goes into `structural` below, so it moves `exit_code` and prints
    # everywhere the reconciler's findings print; it stays out of the JSON
    # `structural` block, whose `checks` denominator counts only the nine.
    leaks: tuple[Finding, ...] = ()
    # Facts the merged document states twice, one `Finding` each — check 9's
    # claim-level half (`reconcile.restated_findings`). Empty on `verify`, where
    # it is not run, and on any merge whose decompose did not complete.
    #
    # Here rather than in `reconciled.findings` for the same reason `leaks` is:
    # the reconciler had finished before the claims existed, and the JSON
    # `structural` block publishes `checks: 9` as its denominator. It joins
    # `structural` below, so it moves `exit_code` and prints under the same
    # heading as the exact half it widens.
    restated: tuple[Finding, ...] = ()
    # Sentences crediting a source with content it does not carry (569), off
    # `reconcile.attribution_findings`. A family of their own and not part of
    # `structural`: they run on `verify` as well as `merge`, read no
    # disposition record, and are no kind the page partitions. A document
    # fault, so they move the exit code to 1. `attributions_checked` is the
    # denominator's other half -- False where no merged document existed.
    attributions: tuple[Finding, ...] = ()
    attributions_checked: bool = False
    # How each document writes its decimals, and the numerals that break it
    # (DECISIONS 601, `numerals`). Its own family for 569's reasons: it runs on
    # `verify` too and reads no disposition record. Only `reading_changed` --
    # a settled source value the merge now states differently -- moves the
    # exit code; the other kinds are warnings about a text, shown and
    # published and never charged. `conventions` is every document's decision
    # and its evidence, so a reader can redo the call.
    number_format: tuple[Finding, ...] = ()
    number_format_checked: bool = False
    conventions: tuple[numerals.Convention, ...] = ()
    # `reason` or `replacement` fields the merge overran its cap on, capped in
    # place and logged rather than rejected. Empty on `verify`, where no merge
    # ran, and on a `merge` that needed no capping. Deliberately not part of
    # `reconciled.findings`: capping is a fact about what `parsing.parse` had
    # to do to the response, not one of the reconciler's nine measurements
    # against the source texts, and does not move `exit_code`. DECISIONS.md
    # entry 190.
    truncations: tuple[parsing.Truncation, ...] = ()
    # What the merge did with its sources' *ordering*, or None where the
    # reconciler did not run. Reported and never judged, on the precedent
    # `verify.Verdict.rationale_names` sets: no finding kind reads it, no exit
    # code moves on it, and `disjoint_sources` is why. That fixture's reference
    # merge is a byte-exact concatenation, `order.stapled` is True of it and
    # correctly so, and its `expected.json` requires exit 0 — a staple is the
    # right answer when the sources had nothing to interleave, and this
    # measurement cannot tell that case from a weld. See DECISIONS 58.
    order: Order | None = None
    # Claims submitted to a verify pass whose record came back unusable and was
    # dropped rather than graded. Pass C, `DECISIONS.md` entry 194. Unlike
    # `truncations`, this *does* move the exit code, and to 2 rather than 1:
    # the tool has no verdict for these claims, so a run carrying any of them
    # has not examined everything it was given, which is what `exit_code`
    # already means by inconclusive. Empty on every run where the model
    # answered every record usably, which is nearly all of them.
    #
    # A list, and mutable on purpose: `pipeline` hands this very object to
    # `verify_claims` as its accumulator rather than collecting into a local
    # and copying it over at the end. There is then no copy step to forget on
    # a path out of the pipeline that someone adds later -- which is the exact
    # shape of the defect entry 24 records, a mechanism that was built, tested
    # and never called.
    unusable: list[Unusable] = field(default_factory=list)
    # Which questions this run was configured to ask. `pipeline` writes it
    # from the same argument that decides the shape of the run, so no call
    # site has to remember to set it twice.
    #
    # The field is the depth and not the flag derived from it, because the
    # depth is what the run was told and the flag is what follows. Defaulting
    # to `full` matches `pipeline`'s own default and is the direction that
    # cannot make a report claim more than the run checked: a `Run` built by
    # hand and never given a depth describes a pipeline that asked both
    # questions, which is what every `Run` in this repository did until 503.
    verify_depth: str = config.DEFAULT_VERIFY_DEPTH
    provenance: Provenance | None = None

    @property
    def detects_invention(self) -> bool:
        """Whether anything in this run read the merged document back.

        A capability, read out of `config.VERIFY_DEPTH_SHAPES`, and never a
        comparison against the string `coverage`. That is the rule the web
        page already keeps (`app.js`'s `suspendedGuarantee`, W1): a surface
        that decides this by name is carrying vocabulary it should be reading,
        and goes quietly wrong the day a third depth arrives -- quietly
        because the failure is a verdict that over-claims, which looks exactly
        like a verdict that is right.

        An unknown depth answers False. The only way to reach that is a `Run`
        carrying a depth this build does not define, and the safe reading of
        "I do not know what this run asked" is that it did not ask.
        """
        shape = config.VERIFY_DEPTH_SHAPES.get(self.verify_depth)
        return bool(shape and shape.detects_invention)

    @property
    def checked_for_invention(self) -> bool:
        """Whether this run asked the question, rather than whether it could.

        `detects_invention` is a property of the depth and is what decides
        which guarantee the verdict suspends. This is a property of the run and
        is what decides whether a headline may rule invention out: a depth that
        reads the merged document back has not read it back when the merge
        yielded no claims to read, and "0 merge claim(s) checked against the
        sources" is literally true and read by nobody as "this pass did not
        run".

        The two came apart because the fix for the `coverage` verdict (505) was
        shaped like the depth, and `app.js`'s `cleanAdvice` was not -- it keys
        on the reverse count and its comment argues that the count is the more
        general statement. It was, and the page was the only surface that had
        it (528).

        Submitted rather than returned. A pass that was given claims and errored
        has not cleared them either, but that run is inconclusive by then and
        never reaches a clean headline; counting verdicts here would instead
        make a pass that ran and found nothing look like a pass that never ran.
        """
        return self.detects_invention and self.submitted("reverse") > 0

    @property
    def errored(self) -> list[Step]:
        return [step for step in self.steps if step.state == ERRORED]

    @property
    def planned(self) -> list[Step]:
        return [step for step in self.steps if step.state == PLANNED]

    @property
    def verdicts(self) -> list[Verdict]:
        return self.forward + self.reverse

    @property
    def accounted_for(self) -> set[str]:
        """Claim ids whose loss a confirmed `dropped` declaration owns. M7 task 27.

        Confirmed only. A rejected declaration is the merge describing itself
        wrongly, and nothing it said about that segment is worth acting on —
        `grade_declarations` lists only the *falsifying* claims on a rejected
        record, so the ones that did come back MISSING appear in no list here
        and stay findings, which is the conservative reading and the right one.

        `dropped` only, and this is the decision task 27 exists to make. Of the
        five dispositions, three predict SUPPORTED and produce no finding to
        route anywhere; the two that can produce one are `dropped` (MISSING)
        and `superseded` (CONTRADICTED or PARTIAL). A declared drop is an
        **omission the merger owned**: the fact is absent, the reason is on the
        page, and a reader can put it back. A confirmed `superseded` that came
        back CONTRADICTED is not an omission — the merged document now asserts
        something a source denies, and a reader who trusts the merge is
        misinformed however well the swap was declared. §2.1 and §2.5 both name
        drops and only drops, and the principle under that wording is that the
        queue takes omissions and never assertions.
        """
        return {
            claim_id
            for item in self.declarations
            if item.disposition == "dropped" and item.grade == CONFIRMED
            for claim_id in item.claims
        }

    @property
    def covering_contradictions(self) -> list[Verdict]:
        """CONTRADICTED verdicts a confirmed covering reconciliation explains.

        **Reported, and still charged.** This is the one place 489's TODO
        direction was not followed, and the reason is a principle this file
        already states one property up: `accounted_for` takes omissions and
        never assertions, because "the merged document now asserts something a
        source denies, and a reader who trusts the merge is misinformed however
        well the swap was declared". A covering value is exactly that -- it
        asserts a range the narrower source denies at one edge -- so
        un-charging it would be carving an exception into the rule rather than
        applying it.

        The second reason is that the tool cannot tell which case it has.
        `reconcile.covers_the_sources` asks whether every number came from some
        source, with no arithmetic anywhere in the package, and by that test a
        *narrowing* to `35-45%` is indistinguishable from a covering to
        `30-50%`. Un-charging would clear both, and the operator's own reading
        is that narrowing violates a source.

        So what 489 actually fixed is the other half: the declaration is
        confirmed, because the merge's account of itself was accurate. The
        finding stays, and this list exists so the report can say *why* it is
        there rather than leaving a reader to think the merge went wrong.

        `confirmed` plus `reconciled` plus a CONTRADICTED claim is only
        reachable through the covering widening in `verify._covering` -- the
        unwidened prediction is SUPPORTED alone -- so no extra state has to be
        carried to identify these.
        """
        covering = {
            claim_id
            for item in self.declarations
            if item.disposition == "reconciled" and item.grade == CONFIRMED
            for claim_id in item.claims
        }
        return [v for v in self.verdicts
                if v.finding == "contradicted" and v.claim_id in covering]

    @property
    def added_claims(self) -> set[str]:
        """Claim ids the reverse pass could not place and the merge declared.

        The addition half of `accounted_for`, and it works the same way: a set
        of ids, subtracted in `findings`, so an *undeclared* addition in the
        same run as a declared one is still a finding and the two are told
        apart by whose id is in here.

        Matched by containment in both directions, because a decomposed claim
        and the sentence a merge declared are rarely the same string: the claim
        may be one fact out of a longer statement, or the statement may be one
        clause of a longer claim. `occurs` is the comparison the rest of this
        project uses for "is this text in that text" and it is used here rather
        than a new one.

        **Only MISSING is eligible.** A merged claim the sources *contradict*
        is not an addition to them, it is a statement they deny, and no
        declaration makes that reportable-but-clean -- which is the same line
        `accounted_for` draws when it takes omissions and never assertions.
        """
        if not self.additions:
            return set()
        declared = [flatten(text) for record in self.additions
                    if (text := str(record.get("statement", "")).strip())]
        if not declared:
            return set()
        found = set()
        for verdict in self.verdicts:
            if verdict.finding != "hallucinated":
                continue
            claim = flatten(self.claim_text(verdict.claim_id))
            if not claim:
                continue
            if any(occurs(claim, statement) or occurs(statement, claim)
                   for statement in declared):
                found.add(verdict.claim_id)
        return found

    def covering(self, statement: str) -> tuple[str, ...]:
        """The excused claim ids this one declared statement is what covers.

        `added_claims` answers the same question for the run as a whole,
        because the exit code is a property of the run. The report needs it
        per record: one declaration covering a dozen claims and a dozen
        declarations covering one each produce the same banner count and are
        not the same thing, and only the second is what this level was built
        for. Neither is refused -- `open` reports rather than charges (482) --
        but a reader cannot weigh the first if the section shows one row while
        the banner counts twelve.

        A claim covered by two declarations is listed against both. The column
        is an attribution rather than a partition, so its total may exceed the
        banner, and over-reporting which declaration might have covered a
        claim is the safe direction for a section whose whole purpose is
        review.
        """
        declared = flatten(statement.strip())
        if not declared:
            return ()
        added = self.added_claims
        found = []
        for verdict in self.verdicts:
            if verdict.claim_id not in added:
                continue
            claim = flatten(self.claim_text(verdict.claim_id))
            if claim and (occurs(claim, declared) or occurs(declared, claim)):
                found.append(verdict.claim_id)
        return tuple(found)

    def claim_text(self, claim_id: str) -> str:
        """The text of a claim by id, or empty when this run has no such claim.

        `claims` is keyed by source document, so this flattens rather than
        indexing -- the same shape three other readers in this module build.
        """
        for claims in self.claims.values():
            for claim in claims:
                if claim.id == claim_id:
                    return claim.text
        return ""

    @property
    def declared_additions(self) -> list[Verdict]:
        """The verdicts `added_claims` excused. Reported, never charged."""
        added = self.added_claims
        return [v for v in self.verdicts if v.claim_id in added]

    @property
    def verify_batch(self) -> int:
        """How many claims one verify call of *this* run carries.

        `searches` one property down's mechanism, for a setting rather than a
        measurement: read off the run's own provenance, because the figure
        depends on which backend is about to answer and the plan has no other
        way to know. `config.DEFAULT_VERIFY_BATCH` where there is no provenance
        to ask -- a fixture, or a `Run` built by hand -- which is the same
        figure the sentence printed unconditionally before this existed.

        It exists because 551 gave a command backend its own batch and left
        two dry-run sentences saying 25 to an operator whose next real run
        would send 100 (558). A plan that states the wrong unit is worse than
        one that states none: it is the only number on the page.
        """
        settings = getattr(self.provenance, "settings", None)
        return getattr(settings, "verify_batch", config.DEFAULT_VERIFY_BATCH)

    @property
    def searches(self):
        """Whether the model went and looked anything up, or None if unknown.

        Read off the run's own provenance rather than carried as a field,
        because it is a fact about the calls this run made and the client is
        what made them. `None` on a Run with no provenance -- a fixture, a
        `verify` over somebody else's merge -- and every reader treats that
        the same way it treats a reported absence, which is `unmeasured`.

        Never a question put to the model. `server_tool_use` is a count the
        serving side wrote down; "did you search?" is a claim (537).
        """
        client = getattr(self.provenance, "client", None)
        return getattr(getattr(client, "usage", None), "searches", None)

    @property
    def turns(self):
        """Whether the model used a tool, or None if nothing reported (548).

        `searches` one property up asks the same question of
        `server_tool_use`, which counts Anthropic's server-side web tools and
        cannot see a command backend's local `WebFetch` -- measured, on a call
        that fetched and reported zero. This reads `num_turns`, which counts
        the round trip a tool call costs and does see it.

        Both are published and neither is dropped. They disagree on this
        backend by construction, and a report that carried only the one that
        happens to be zero would be publishing the blind instrument.
        """
        client = getattr(self.provenance, "client", None)
        return getattr(getattr(client, "usage", None), "turns", None)

    @property
    def fidelity(self) -> str:
        """The level this run was written at, or `` where there was no policy.

        Read off the provenance for `searches`' reason. The sourcing sentence
        needs it: a run with no tool use is an ordinary result at `open` and is
        the *interesting* one at `sourced`, where every citation in it is then
        a recollection despite the level having asked for retrieval.
        """
        settings = getattr(self.provenance, "settings", None)
        return str(getattr(settings, "fidelity", "") or "")

    @property
    def number_faults(self) -> tuple[Finding, ...]:
        """The number-format findings that move the exit code (601)."""
        return tuple(finding for finding in self.number_format
                     if finding.kind in numerals.FAULTS)

    @property
    def number_warnings(self) -> tuple[Finding, ...]:
        """The number-format findings that are shown and never charged (601)."""
        return tuple(finding for finding in self.number_format
                     if finding.kind not in numerals.FAULTS)

    @property
    def corrections(self) -> list[dict]:
        """Declared additions that name something in the documents they fix.

        The split that decides what the exit code does, and it is not a new
        rule (537). An addition the documents are *silent* about is excused by
        `added_claims`: the sources cannot deny it and the declaration is what
        makes it reviewable. A correction is the other case -- the merge now
        asserts something a source denies -- and `Run.accounted_for`'s rule
        already answers it: the queue takes omissions and never assertions,
        "because the merged document now asserts something a source denies,
        and a reader who trusts the merge is misinformed however well the swap
        was declared" (490). Nothing in this package can tell a correction
        from a corruption, so the finding stays and this property is what lets
        the report say why it is there.
        """
        return [record for record in self.additions
                if str(record.get("corrects", "")).strip()]

    @property
    def queued(self) -> list[Verdict]:
        """Declared drops the forward pass confirmed: reported, never charged.

        The `finding == "dropped"` test is the third of three filters and the
        one that makes the other two individually unfalsifiable: a rejected
        `dropped` record lists only its non-MISSING claims, and no *confirmed*
        non-`dropped` disposition can hold a MISSING one, so removing either
        half of `accounted_for`'s condition alone changes no output. Removing
        both does — a rejected `subsumed` over a segment that really was dropped
        is the reachable case, and it is the one worth guarding, so all three
        stay and the test drives that combination rather than each in turn.
        """
        accounted = self.accounted_for
        return [
            v
            for v in self.verdicts
            if v.finding == "dropped" and v.claim_id in accounted
        ]

    @property
    def findings(self) -> list[Verdict]:
        """Everything that moves the exit code, and nothing that does not.

        §2.5 in one property: do not let the review queue into the exit code,
        and do not hide findings inside it. The second half is why this
        subtracts a set of claim ids rather than filtering on a declaration —
        an undeclared drop in the same run as a declared one is still a finding,
        and the two are told apart by whose id is in `accounted_for`.
        """
        accounted = self.accounted_for
        added = self.added_claims
        return [
            v
            for v in self.verdicts
            if v.finding != "none"
            and not (v.finding == "dropped" and v.claim_id in accounted)
            and not (v.finding == "hallucinated" and v.claim_id in added)
        ]

    @property
    def structural(self) -> list[Finding]:
        """What was found without asking a model, and it moves the exit code.

        Kept apart from `findings` rather than merged into it because the two
        are different objects answering different questions — a `Verdict` is a
        model's judgement about one claim, a `Finding` is arithmetic over two
        texts — and a single list would have to lose one of those shapes. They
        are added, never summed into a `Verdict` count: the verdict line prints
        both totals and names which is which.

        The reconciler's nine checks plus `leaks` and `restated`, neither of
        which is one of them. All three belong in one list here because
        everything downstream — the verdict line, the terminal summary, the
        Markdown and HTML sections — asks this object one question, "what is
        wrong with this merge that needed no model", and all three answer it.
        `restated` answers it having read the merged document's claims, which
        cost model calls to produce; what it did with them is still arithmetic
        over two strings, and the claims were extracted for the reverse pass
        whether or not this reads them. Where they must not be one list is the
        JSON `structural` block, which publishes `checks: 9` as their
        denominator; that block reads `reconciled.findings` directly, and
        `leaks` and `restated` each have their own.

        Empty when the reconciler ran and found nothing, and also empty when it
        did not run at all. The exit code is allowed to conflate those two; the
        report is not, which is why `structural_section` reads `reconciled`
        rather than this.
        """
        found = [] if self.reconciled is None else list(self.reconciled.findings)
        return found + list(self.leaks) + list(self.restated)

    @property
    def capped_verdicts(self) -> list[Verdict]:
        """Verdicts whose rationale ran over `RATIONALE_MAX` and was capped.

        Informational, the way `rationale_names` is: it says the argument for
        a label may have been cut short, not that the label is wrong, so it is
        no part of `findings` and moves nothing. `capping_section` is what
        reads this.
        """
        return [v for v in self.verdicts if v.rationale_capped]

    @property
    def declared_drops(self) -> int:
        """Every declared drop, including the ones no claim was drawn from.

        The queue counts claims; this counts records, and the difference is the
        whole reason §2.6 exists. `decompose.md` skips headings and boilerplate,
        so a merge can declare thirty drops of segments no claim will ever come
        out of. Task 42 fix 4 means most of those are now graded on where the
        reconciler found their text rather than left `unchecked`, but a grade is
        still not a budget: a drop can be confirmed as a drop and still be the
        thirtieth. They appear in no queue and, under budget, in no finding, and
        this is the only thing that counts them.
        """
        return len([item for item in self.declarations if item.disposition == "dropped"])

    @property
    def over_budget(self) -> bool:
        """§2.6, asked of `reconcile` rather than reimplemented here."""
        return over_budget(self.declared_drops, self.segments,
                           self.declared_loss_budget)

    @property
    def budget_disables_check(self) -> bool:
        """Is the ceiling set where §2.6 can no longer fire?

        At 1.0 a merge may declare away every segment it was given and stay
        inside the budget, because `drops / segments` cannot exceed 1. That is
        a permitted setting -- an operator triaging a known-lossy merge has a
        use for it -- but it makes `over_budget: false` mean "not asked"
        rather than "asked and passed", and those two are the same sentence
        in a report that does not distinguish them.

        A disabled check that reads as a passed check is this project's
        most-repeated failure class, so the report says this out loud instead
        of leaving it to be inferred from a number in the provenance block.
        """
        return self.declared_loss_budget >= 1.0

    def submitted(self, direction: str) -> int:
        """Claims handed to a pass, whether or not it came back with anything.

        Kept apart from the number of verdicts so an errored pass reports what
        it was supposed to examine rather than quietly shrinking to nothing.
        """
        if direction == "forward":
            return sum(len(c) for name, c in self.claims.items() if name != MERGED)
        return len(self.claims.get(MERGED, []))

    def sources(self) -> list[str]:
        """The source documents, in canonical order. The merge is not one."""
        return [name for name in sorted(self.claims) if name != MERGED]

    def unexamined_sources(self) -> list[str]:
        """Sources whose decomposition returned no claims at all.

        Zero claims and "the call failed" look identical in a coverage table
        and mean opposite things, which is why `decompose` raises rather than
        returning an empty list. This is the third case: the call succeeded and
        the model found nothing checkable. Nothing about that source was
        examined at the claim level, so a clean verdict over it is a verdict
        about an examination that did not happen.
        """
        return [name for name in self.sources() if not self.claims.get(name)]

    def forward_by_source(self) -> dict[str, dict[str, int]]:
        """Per source: claims extracted, checked, accounted for, partly kept.

        M7 task 26. The forward ratio above this one has a single denominator
        covering every source, and a pooled denominator is the defect this
        milestone exists to refuse. Two sources of six claims each, one carried
        whole and one dropped whole, report `6/12` — the same figure a merge
        that lost one claim from each of six sources would print. The shape of
        the loss is the finding, and pooling makes it invisible: a source that
        was ignored entirely reads as a merge that was 50% careless.

        Keyed on the claim id, which `decompose.claim_id` builds from the
        document's canonical letter (`A-001`, `B-014`), and the CLI renames
        every input to a canonical name before decompose sees it. So two
        sources in one run cannot issue the same id, and this mapping is exact
        rather than a best effort. A verdict whose id belongs to no source is
        counted under the empty key and printed rather than dropped — it cannot
        happen through the pipeline, and if it ever does the per-source rows
        would otherwise sum to less than the pooled row with nothing saying so.
        """
        owner = {
            claim.id: name for name in self.sources() for claim in self.claims[name]
        }
        counts = {
            name: {
                "extracted": len(self.claims[name]),
                "checked": 0,
                "accounted": 0,
                "partial": 0,
            }
            for name in self.sources()
        }
        for verdict in self.forward:
            name = owner.get(verdict.claim_id, "")
            row = counts.setdefault(
                name, {"extracted": 0, "checked": 0, "accounted": 0, "partial": 0}
            )
            row["checked"] += 1
            if verdict.finding == "none":
                row["accounted"] += 1
            if verdict.finding == "partially_dropped":
                row["partial"] += 1
        return counts

    def display(self, canonical: str) -> str:
        """A name a human can scan, not the caller's (often absolute) path.

        Two files sharing a basename must still be told apart, so the parent
        directory is prefixed only when the bare name collides with another
        document in this run.
        """
        path = self.paths.get(canonical, canonical)
        name = Path(path).name
        others = [Path(p).name for key, p in self.paths.items() if key != canonical]
        if name not in others:
            return name
        parent = Path(path).parent.name
        return f"{parent}/{name}" if parent else name


# The exit code for a run whose only faults are in its account of itself.
# Deliberately 3 and not 1: `README.md` has documented 0/1/2 since the first
# release and a caller testing `!= 0` keeps working, while a caller testing
# `== 1` now means "the document" and gets what it asked for. Entry 420.
RECORD_ONLY = 3

# Every code `exit_code` can return. One tuple so a renderer that maps codes to
# words can assert it has them all: `html_report.BANNER` did not, and entry
# 420's split of `3` out of `1` reached it as `KeyError: 3` at the end of a
# finished run (500). A bare subscript is fine when something guarantees the
# key exists; this is that something.
EXIT_CODES = (0, 1, 2, RECORD_ONLY)


def exit_code(run: Run) -> int:
    """0 clean, 1 the document, 3 only the record, 2 inconclusive.

    **Entry 420 split what 1 used to mean.** A finding was a finding, so a
    merge that mis-declared work it had done correctly ranked with a merge that
    lost content. On the operator's `universe` pair those two came apart and
    pointed opposite ways: `off` copied the sources verbatim, declared 23
    dispositions, got every one of them right and exited **0** with a document
    matching 6 of 23 sentences of the answer key; `low`, `mid` and `high`
    corrected the typos, matched 23 of 23, and exited **1** on four
    `false_departure` findings apiece. A reader trusting the code shipped the
    26% document and rejected the 100% one.

    So the two questions get two codes. 1 means `reconcile.DOCUMENT_FINDINGS`:
    the merged document is missing, inventing, altering, repeating or shedding
    content. 3 means `reconcile.RECORD_FINDINGS` and nothing worse: the
    document is sound as far as this tool looked, and the merge's account of
    itself is not. 3 is still a failure and still non-zero, so making record
    findings cheaper did not make them free -- which was the risk in this
    change.

    **It does not close B5, and an earlier version of this docstring said it
    did.** "A merge cannot declare its way to 0" is false, and entry 426
    reproduces the counter-example: declarations that are internally consistent
    -- every segment `superseded`, every replacement genuinely present in the
    merge -- pass all nine checks with 70% of the source gone, and exit 0 at
    every level. What 3 bounds is a merge whose bookkeeping is *detectably*
    wrong. A merge whose bookkeeping is undetectably wrong is B5's subject and
    is still open.

    Measured before landing, over the operator's 19 saved runs: **3 change**,
    and they are exactly the three that produced the inversion. The other 16
    keep the code they had, because a document finding was present in every one
    of them. Every fixture that pre-registers a non-zero exit registers 1, and
    all of them are document defects, so the registered corpus is unmoved.

    Severity orders 2 > 1 > 3 > 0: an inconclusive run outranks any finding,
    and a document fault outranks a bookkeeping one. A run with both is 1.

    A run that verified nine claims of twelve and found no fault has not found
    no fault, so an errored unit outranks whatever the units that did answer
    happened to say. The ordering is here rather than in `main` so the report
    and the exit code are computed from one object by one rule.

    `run.findings` already excludes the review queue (M7 task 27), so a declared
    and confirmed drop does not reach 1. `run.over_budget` is the ceiling that
    keeps that from being a way of declaring your way to a clean exit: past §2.6
    the queue stops being a queue and the run has a finding of its own, which is
    the volume of loss rather than any single claim in it.

    `run.unusable` reaches 2 by the same rule and for the literal case the
    first paragraph describes. Pass C (entry 194) grades the eleven records a
    batch got right instead of discarding all twelve over the one it got
    wrong, and the twelfth claim is then submitted, unanswered and named. That
    is a better report than the zero-byte one it replaces and it is not a
    better result: a run that could not grade a claim has not found no fault
    about that claim, so it cannot exit 0, and it must not exit 1 either --
    1 means a finding was made, and here the tool is saying it could not make
    one. Salvage never improves an exit code; it only ever adds detail to a
    report that had none.

    `run.structural` is M7 task 36 and it makes this stricter: a merge that
    dropped a title, moved a digit or left a source segment out with no record
    explaining it now exits 1, where before it exited 0 because no *claim* was
    lost. Runs that passed before this line existed can fail now, and that is
    the point — `prompts/decompose.md` skips headings and formatting, so those
    defects were never in a verdict to be counted. `DECISIONS.md` entry 9.
    """
    if run.errored or run.unusable:
        return 2
    # A source that produced no claims was not examined at the claim level, and
    # on `verify` the claim level is the whole examination -- there is no
    # reconciler result standing behind it. Reporting a clean verdict over an
    # unexamined source is the pattern this project exists to catch, so it is
    # an error rather than a finding: findings are things the tool saw, and
    # this is a thing it did not look at.
    if run.command == "verify" and run.unexamined_sources():
        return 2
    # Grounding is reported and does not move the exit code. It measures
    # whether the judge anchored its verdict in the source, not whether the
    # merge is sound, and treating a vague judge as a bad merge would put the
    # tool's weakest measurement into its loudest output (318).
    #
    # One exception, and it is a measurement rule rather than a grading one:
    # claims were graded and *none* of them grounded. Then no verdict rests on
    # anything shown to exist, and the run has produced no evidence at all --
    # the same situation as a source that yielded no claims, four lines up, and
    # the same answer.
    graded = [v for v in run.verdicts if v.grounding != NOT_GRADED]
    if graded and not any(v.grounding == GROUNDED for v in graded):
        return 2
    # A `sourced` merge that retrieved nothing did not do the one thing the
    # level exists for (665). 568 reported it on every surface and kept it off
    # the exit code, "neither is a failure of the documents"; that left a run
    # recalled from memory exiting 1 like any sourced run, and a script or a
    # benchmark that reads the code counted it as a sourced draw. Measured
    # 2026-09-26: after the CLI moved from 2.1.274 to 2.1.283, five of five
    # Sonnet voyager merges made no retrieval and nothing downstream stopped.
    # It is the unexamined-source rule four lines up in other words: the run
    # has not established what it was asked to establish, so 2, and it
    # outranks any finding, which is what makes it loud on the runs that have
    # findings -- nearly every sourced run. `not-retrieved` only: `unmeasured`
    # is not "did not retrieve" (568), and 568 refuses in advance the command
    # that cannot report. A `verify` run makes no merge call and is not judged.
    if sourced_not_delivered(run):
        return 2
    # `run.findings` is claim-level -- a verdict saying the merged document
    # misstates or drops a source claim -- so it is a document fault by
    # construction and needs no kind lookup. `run.over_budget` is the §2.6
    # ceiling, which is content genuinely gone, and is filed the same way.
    if run.findings or run.over_budget:
        return 1
    # An attribution the sources contradict is the merged document telling a
    # reader something false about where a fact came from (569).
    if run.attributions:
        return 1
    # A settled source value the merge states differently: "17,560 miles"
    # written "17.560 miles" under a decimal point (601). The warnings beside
    # it -- a numeral in the other convention, one readable two ways -- are
    # about a text, not a fault in the merge, and do not reach here.
    if run.number_faults:
        return 1
    kinds = {finding.kind for finding in run.structural}
    if kinds & DOCUMENT_FINDINGS:
        return 1
    if kinds & RECORD_FINDINGS:
        return RECORD_ONLY
    # A kind in neither family cannot reach here -- `reconcile` asserts the
    # partition at import -- but a finding list that is non-empty and matched
    # nothing would otherwise return 0, which is the one way this function
    # could go quiet. Say so instead.
    if run.structural:
        raise AssertionError(f"findings of unfiled kinds: {sorted(kinds)}")
    return 0


def ratio(numerator: int, denominator: int, missing: str) -> str:
    """`n/d`, or the reason there is no ratio. Never `0/0`."""
    if denominator == 0:
        return missing
    return f"**{numerator}/{denominator}**"


def budget_sentence(run: Run) -> str:
    """§2.6 in one sentence, or nothing. Used by the verdict and by the queue."""
    return (
        f"The merge declared **{run.declared_drops}** drop(s) of "
        f"{run.segments} source segment(s), {loss_rate(run)}, over the "
        f"{run.declared_loss_budget * 100:g}% budget: past that share the omissions are "
        f"the finding, whatever each one says about itself."
    )


def loss_rate(run: Run) -> str:
    """The share of source segments the merge declared gone, as a percentage.

    Both numbers were already printed and the reader had to divide (488). A
    run at 0.4% and a run at 2.9% read identically against a 3% ceiling, and
    they are not the same run: one is nowhere near the limit and the other is
    about to fail. Naming the achieved figure beside the configured one is
    what makes the ceiling mean anything to somebody who did not set it.

    No segments is no rate. `0.0%` would say a merge dropped nothing out of
    something, and the honest answer is that the question does not arise.
    """
    if not run.segments:
        return "no source segments"
    return f"**{run.declared_drops / run.segments * 100:.1f}%**"


def loss_row(run: Run) -> str:
    """Achieved against configured, for a run that is *not* over budget.

    `budget_sentence` says this only when the ceiling was crossed, which is
    the one case a reader does not need telling -- the run already failed and
    said why. The case that needed it is the clean one, where the report used
    to say nothing at all about how close the merge came.
    """
    return (
        f"{run.declared_drops} of {run.segments} source segment(s) declared "
        f"gone, {loss_rate(run)} against a "
        f"{run.declared_loss_budget * 100:g}% ceiling"
        + (" — the ceiling check was off for this run"
           if run.budget_disables_check else "")
    )


def queue_sentence(run: Run) -> str:
    """What the queue is, said wherever a count of it is printed."""
    return (
        f"**{len(run.queued)}** dropped claim(s) are in the review queue below: "
        f"the merge declared those segments dropped and the forward pass agrees "
        f"they are gone. They are reported and not charged — a declared omission "
        f"is a decision to review, not an error to fail on."
    )


def covering_sentence(run: Run) -> str:
    """Why a covering value is a finding, said where the finding is.

    Without this the report is telling the truth and reading as a fault. The
    merge was asked for the safest reading of two disagreeing figures, gave
    one, declared it, had the declaration confirmed -- and the run exits 1
    with a `contradicted` finding against the source whose edge the covering
    value crosses. Every one of those steps is correct and the combination
    looks like a bug.

    It also says the thing the tool genuinely cannot do, because a reader
    deciding whether to accept this needs it: nothing here parses a number, so
    a covering `30-50%` and a *narrowing* `35-45%` are the same shape to every
    check in the package. The finding is what makes the difference visible to
    a person, which is why it is reported rather than excused.
    """
    n = len(run.covering_contradictions)
    return (
        f"**{n} contradiction(s) below are covering values the merge declared "
        f"and this tool confirmed.** At fidelity `open` a merge may carry a "
        f"value spanning two disagreeing figures, and such a value asserts an "
        f"edge the narrower source denies -- so the contradiction is what the "
        f"licence produces, not evidence the merge went wrong. It stays a "
        f"finding because nothing here parses a number: a covering value and "
        f"a *narrowing* one are the same shape to every check in this tool, "
        f"and only a reader can tell them apart."
    )


def mismatch_sentence(run: Run) -> str:
    """The merge's warning that these documents may not belong together (497).

    Deliberately not a finding. The operator's words were "we do not need to
    fail but we should provide a friendly hint that they probably end up
    doing something undesired", and the distinction is the whole point: a
    merge of a C# file and a Java file can be flawless by every check this
    tool has -- every claim survives, nothing is invented, no token moves --
    and still be a thing nobody wanted. That is not a defect in the merge, so
    it must not be scored as one; it is a fact about the *inputs*, which the
    exit code has never been about.

    Quoted rather than paraphrased, and attributed. The sentence is the
    model's, nothing here checks it, and a reader deciding whether to take it
    seriously needs to know both of those things.
    """
    return (
        f"**The merge flagged these documents as possibly not belonging "
        f"together:** \u201c{run.mismatch}\u201d This is the merge model's own "
        f"warning about your *inputs*, not a fault in the output, and nothing "
        f"in this report checks it. Every other number here still holds; if "
        f"the two documents really are unrelated, a clean result means they "
        f"were combined faithfully, which may not be what you wanted."
    )


def addition_sentence(run: Run) -> str:
    """What a declared addition is, and what the verdict above no longer means.

    The other sentences in this file narrow a clean verdict. This one suspends
    part of it, and says so in those words, because at `open` the reverse pass
    can no longer tell a declared addition from a hallucination -- the sources
    are the only ground truth this tool has, and these statements are not in
    them. Every other check still ran; this is the one guarantee that is off.

    Said on every verdict rather than only on the clean one. A reader who
    selected this level is owed the sentence whatever the exit code, and a
    notice that appears only when nothing else went wrong is a notice that is
    missing from every report anyone reads carefully.
    """
    n = len(run.declared_additions)
    return (
        f"**{n} statement(s) in the merge came from outside your documents and "
        f"could not be checked against them.** The merge declared each of them "
        f"and they are listed below. This is what fidelity `open` permits and "
        f"it is the one thing this tool cannot verify: for these statements, a "
        f"clean verdict means the merge said it was adding them, not that they "
        f"are true. An addition the merge had *not* declared would still be "
        f"reported as invented."
    )


# What this tool did about a citation, said in one form everywhere (537).
#
# Two facts, and both belong. The first never changes: nothing in this package
# opens a socket, so no `source` a merge wrote was fetched, resolved or
# checked, whatever it says. The second is a measurement and does change --
# whether the *model* went and looked, read off `server_tool_use` and never
# asked of the model, which would be a claim rather than a count.
#
# Stating either alone is misleading in one direction or the other. "Nothing
# here has been checked against anything" is false about a run where the model
# searched; "the model looked this up" is false about what this tool then did
# with it.
NOT_RESOLVED = (
    "LLossless did not fetch, resolve or check any source listed here. "
    "LLossless itself opens no socket to do it."
)

# What a `basis` says in words, in the page's words (544).
#
# The column printed the enum: `citation` and `own-knowledge`, straight off the
# record, while the page put the same column through `t("basis." + value)` and
# printed *cited* and *the model's own knowledge*. One column, two vocabularies,
# and which one a reader got depended on whether they were looking at the page
# or at the report they downloaded from it -- which is 504's defect exactly, in
# a table rather than in a verdict.
#
# The words are the catalogue's and `tests/test_contract_parity.py` pins them
# to `basis.*` in `web/locales/en.json`, the way `advice.noinvention` is pinned.
# Copied rather than imported because `report` may not read `web/`: the CLI does
# not ship the server, and a Markdown report is rendered on machines where no
# locale file exists.
BASIS_WORDS = {
    "citation": "cited",
    "own-knowledge": "the model's own knowledge",
}


def basis_word(value: str) -> str:
    """One `basis` value as a reader's phrase, or unchanged if it is neither.

    Unknown values pass through rather than becoming a blank or a guess. The
    enum is closed by the schema and `parsing._check_basis` refuses anything
    else, so a value arriving here that is not in the table is a record this
    build did not produce -- and printing it is how somebody finds that out.
    """
    return BASIS_WORDS.get(value, value)

_SEARCHING = {
    "searched": (
        "The model made {n} web request(s) of its own while merging, so a "
        "citation here may have been looked up. Which one it belongs to is "
        "not recorded, and the statement is still the model's."
    ),
    "not-searched": (
        "The model made no web request while merging, so every source here "
        "is recalled rather than looked up."
    ),
    "unmeasured": (
        "Whether the model made any web request is unmeasured -- this "
        "endpoint does not report it -- which is not the same as none."
    ),
}

# The turn counter's three states, said in turns (548). A separate table from
# `_SEARCHING` because it is a separate instrument: that one counts web
# requests off `server_tool_use` and is blind to a command backend's local
# tool, this one counts the round trip a tool call costs and can see it. Where
# both reported they are both printed, because a run where they disagree is a
# run whose reader needs to know they disagreed.
#
# Never the word *fetch* and never a fetch count. `num_turns` is a count of
# turns; what a turn past `usage.MOST_TURNS_WITHOUT_RETRIEVAL` was spent on is
# not in the number.
# What the blind counter is allowed to say once the other one has spoken (548).
#
# **This is a defect the first live run printed.** `_SEARCHING["not-searched"]`
# ends *"so every source here is recalled rather than looked up"*, and on a run
# where the turn counter saw three calls use a tool that sentence sat
# immediately beside one saying the opposite -- and its half is the false one.
# A conclusion drawn from `server_tool_use` is only available where nothing
# better reported: the counter is blind to a command backend's local tool, so
# its zero means "this instrument saw nothing", not "nothing happened".
#
# The count is still published, because a reader comparing two runs needs to
# know which instrument wrote which figure. What is withdrawn is the
# conclusion.
SEARCH_COUNTER_BLIND = (
    "The endpoint's own web-request counter reported none, which on this "
    "backend means it could not see one rather than that none was made: it "
    "counts a vendor's server-side tools and a command-line tool runs in the "
    "model's own process."
)

_TOOL_USE = {
    # No turn figure in either sentence: what a retrieval costs depends on the
    # argv the call ran under -- three turns through the shipped one, two
    # under the isolation -- and `Turns.add` applies the right floor (610).
    "tool-use": (
        "The model took more turns on {n} call(s) than a call that retrieves "
        "nothing can take, so it used a tool it was granted at least that "
        "often. It is a count of turns rather than of fetches, and which "
        "statement a retrieval belongs to is not recorded."
    ),
    "no-tool-use": (
        "No call the model made took more turns than a call that retrieves "
        "nothing can take, so it retrieved nothing and every source here is "
        "recalled rather than looked up."
    ),
    "unmeasured": (
        "Whether the model used a tool is unmeasured -- this backend reports "
        "no turn count -- which is not the same as none."
    ),
}

# What a `sourced` run that retrieved nothing has to say for itself, in the
# section that lists its citations (548). The level asked the model to go and
# look, the run says it did not, and a report that averaged that away would
# leave a reader believing the citations were checked. The interesting case is
# the quiet one, so it is the one with a sentence of its own.
SOURCED_WITHOUT_RETRIEVAL = (
    "**This run was made at fidelity sourced, which asks the model to "
    "retrieve rather than recall, and nothing was retrieved.** Every source "
    "listed here is therefore a recollection, exactly as it would be at open."
)


# What a `sourced` run says about retrieval where a reader decides whether to
# trust it: the verdict, on every exit code (568). Before this the report said
# what was *permitted* -- "WebFetch permitted" and a turn count in the
# provenance table -- and left the reader to work out what was *achieved*,
# and the one state that most needed saying was the one it never said: an
# operator ran for hours on routes that reported no turn count, and every
# report looked normal.
#
# Three states and three sentences, and `unmeasured` is never folded into
# either of the others. It is the only one that can be printed over a run that
# really did retrieve.
RETRIEVAL_SAID = {
    usage.RETRIEVED: (
        "**The model retrieved.** This run was made at fidelity sourced, and "
        "{n} of the {m} {calls} that reported a turn count took the turns a "
        "retrieval costs. Which statement a retrieval backs is not recorded, "
        "and each is still the model's."
    ),
    usage.NOT_RETRIEVED: (
        "**Nothing was retrieved.** This run was made at fidelity sourced, "
        "which asks the model to retrieve rather than recall, and none of its "
        "{m} {calls} took the turns a retrieval costs, so every source it names "
        "is a recollection, exactly as it would be at open."
    ),
    usage.UNMEASURED: (
        "**Whether anything was retrieved is unmeasured.** This run was made at "
        "fidelity sourced, and {k} of its {calls} reported no turn count, so "
        "this report cannot say whether the model looked anything up -- which "
        "is not the same as saying it did not. Treat every source it names as "
        "unchecked."
    ),
}
assert set(RETRIEVAL_SAID) == set(usage.RETRIEVAL_STATES)


def retrieval_outcome(run: Run) -> str:
    """`retrieved`, `not-retrieved` or `unmeasured` at `sourced`; `` below it (568).

    Empty below `sourced` rather than a fourth state: no other level promised
    retrieval, so there is nothing to have kept. A `sourced` run with no turn
    tally at all is `unmeasured`, never `not-retrieved`.
    """
    if config.canonical_fidelity(run.fidelity) != config.SOURCED:
        return ""
    turns = retrieval_turns(run)
    return usage.UNMEASURED if turns is None else turns.retrieval


def retrieval_turns(run: Run):
    """The turn tally `sourced` is judged on: the merge's calls, on a merge (665).

    The grant is run-wide, so at `sourced` decompose and verify calls may
    retrieve as well, and a run-wide tally then reads "retrieved" over a merge
    that recalled every source it names: measured on CLI 2.1.274, five of
    seven low-effort decompose and verify calls of one voyager run took 2-5
    turns. The citations a `sourced` run reports are the merge's, so a merge
    run is judged on the merge role's calls alone. A merge run whose tally
    carries roles but no merge call -- the merge errored before any envelope --
    is judged on an empty tally, which reads `unmeasured`, never on the other
    roles'.

    Pooled, as before 665, for a `verify` run, which makes no merge call, and
    for a tally fed without roles (every recording and test written before
    it), so those read exactly as they did. None where nothing was tallied.
    """
    turns = run.turns
    if turns is None or run.command != "merge" or not getattr(turns, "roles", None):
        return turns
    return turns.roles.get("merge") or usage.Turns()


def retrieval_calls_word(run: Run) -> str:
    """"merge call(s)" where the tally is the merge's, "call(s)" where pooled (665).

    The counts in every retrieval sentence are `retrieval_turns`' counts, and
    "none of its 1 call(s)" over a run that made six would be a false sentence
    with a true number in it.
    """
    turns = run.turns
    judged = retrieval_turns(run)
    return ("merge call(s)" if judged is not None and judged is not turns
            else "call(s)")


def _judged_tool_use(run: Run) -> dict | None:
    """`sourcing.tool_use`: the judged tally at `sourced`, the run's below it."""
    turns = retrieval_turns(run) if retrieval_outcome(run) else run.turns
    return None if turns is None else turns.as_dict()


def sourced_not_delivered(run: Run) -> bool:
    """A `sourced` merge whose merge calls reported and none retrieved (665).

    What moves `exit_code` to 2. Read off `retrieval_outcome`, so it is the
    merge role's tally on a merge and `not-retrieved` alone: never over an
    unmeasured call, and never on a `verify` run, which writes no citation.
    """
    return (run.command == "merge"
            and retrieval_outcome(run) == usage.NOT_RETRIEVED)


def inconclusive_for_retrieval_alone(run: Run) -> bool:
    """Whether `sourced_not_delivered` is the only reason this run exits 2 (665).

    The surfaces that explain a 2 -- the verdict line, the terminal -- were
    written for a run whose work did not finish. A run that finished and
    recalled instead of retrieving needs its own sentence, and only where no
    other reason for a 2 is present, because those still say what they say.
    """
    if not sourced_not_delivered(run) or run.errored or run.unusable:
        return False
    if run.command == "verify" and run.unexamined_sources():
        return False
    graded = [v for v in run.verdicts if v.grounding != NOT_GRADED]
    return not (graded and not any(v.grounding == GROUNDED for v in graded))


# The verdict for a run that exits 2 on `sourced_not_delivered` alone (665).
# Its own sentence: the one for an errored unit says the model "could not be
# made to answer usably", and this model answered; what it did not do is look.
NOT_SOURCED = (
    "**Inconclusive: not a sourced merge.** This run was made at fidelity "
    "sourced, which asks the merge to look its facts up, and the merge "
    "retrieved nothing, so it did not do what the level asks and its result "
    "is a merge from recall, as one made at open would be. Re-run it, or read "
    "it as a merge at open."
)


def retrieval_lead(outcome: str) -> str:
    """The bold opening of `RETRIEVAL_SAID[outcome]`, unmarked (568).

    What the terminal says first, so the three surfaces a reader can move
    between open on the same words rather than on three paraphrases of them.
    """
    return RETRIEVAL_SAID[outcome].split("**")[1]


def retrieval_sentence(run: Run) -> str:
    """The verdict-line sentence for `retrieval_outcome`, or `` below `sourced`."""
    outcome = retrieval_outcome(run)
    if not outcome:
        return ""
    turns = retrieval_turns(run)
    measured = 0 if turns is None else turns.calls
    silent = 0 if turns is None else turns.unmeasured
    return RETRIEVAL_SAID[outcome].format(
        n=0 if turns is None else turns.with_tools, m=measured,
        # A run with no tally at all has no count of silent calls to give, and
        # "0 of its calls" would read as none being silent.
        k=silent if silent else "all", calls=retrieval_calls_word(run))


def recall_only(run: Run) -> bool:
    """Was this run asked to retrieve, and did it retrieve nothing? (548)

    The question the report cannot leave a reader to work out. `sourced` is the
    level that expects retrieval; a run there whose turn counter reports no
    tool use has produced citations that are recollections, and it is
    indistinguishable from a run that retrieved unless something says so.

    False where anything went unreported, and deliberately: `unmeasured` is not
    "no tool use", and claiming recall over an absent measurement would be the
    same inversion `usage.py` refuses everywhere else. Since 568 that includes
    a run where *some* calls reported and some did not -- the silent one may be
    the one that retrieved -- so this is `retrieval_outcome` and nothing else.
    """
    return retrieval_outcome(run) == usage.NOT_RETRIEVED


def sourcing_sentence(run: Run) -> str:
    """What was and was not done about the sources this merge cited.

    In the section that lists them, never in a footnote elsewhere: a reader
    weighing a citation is doing it here, and a caveat on another page is a
    caveat they meet after they have decided.

    Three facts and they are kept apart (548). What *this tool* did is first,
    is constant, and is false to omit under any level: it opens no socket, so
    nothing here was fetched, resolved or checked. What the *model* did is two
    measurements rather than one, because the two counters answer the same
    question through instruments that disagree on a command backend -- and the
    blind one reporting zero is exactly the reading a reader must not be given
    alone.
    """
    searches = run.searches
    state = "unmeasured" if searches is None else searches.state
    total = 0 if searches is None else (searches.total or 0)
    outcome = retrieval_outcome(run)
    # At `sourced`, the tally the level is judged on (665): the citations
    # listed here are the merge's, and a verify call's retrieval backs none of
    # them. Below it nothing is judged and the run-wide tally reads as before.
    turns = retrieval_turns(run) if outcome else run.turns
    measured = turns is not None and turns.known
    said = [NOT_RESOLVED]
    if not measured and outcome and state == usage.NOT_SEARCHED:
        # A `sourced` run is a command run by construction -- the level refuses
        # an HTTP endpoint -- and on a command backend this counter is blind.
        # Its zero may not conclude "recalled" beside a turn count that was
        # never reported (568).
        said.append(SEARCH_COUNTER_BLIND)
        said.append(_TOOL_USE[usage.UNMEASURED])
    elif not measured:
        # Unchanged for every run that reports no turn count, which is every
        # HTTP run and every recorded figure in this project.
        said.append(_SEARCHING[state].format(n=total))
        if outcome:
            said.append(_TOOL_USE[usage.UNMEASURED])
    else:
        # The instrument that can see this backend leads, and the blind one
        # loses its conclusion rather than its number. A `not-searched` zero
        # beside a turn counter that saw tool use is two sentences a reader
        # can only read as a contradiction, and the false one is the zero's.
        #
        # A run where some calls reported and some did not is `no-tool-use`
        # off the ones that did, and the sentence for that says "retrieved
        # nothing" -- over a silent call that may be the one that retrieved.
        # So a partial absence is said as unmeasured (568).
        key = (usage.UNMEASURED
               if turns.retrieval == usage.UNMEASURED else turns.state)
        said.append(_TOOL_USE[key].format(n=turns.with_tools))
        if state == usage.SEARCHED:
            said.append(_SEARCHING[state].format(n=total))
        elif state == usage.NOT_SEARCHED and turns.state == usage.TOOL_USE:
            said.append(SEARCH_COUNTER_BLIND)
        if recall_only(run):
            said.append(SOURCED_WITHOUT_RETRIEVAL)
    return " ".join(said)


def judged_against(run: Run, direction: str) -> str:
    """Which document a verdict in this direction was read against, named.

    The operator's question, verbatim: *"What is the 'reference' here? Source
    document 1?"* -- and then, over a second finding, *"it appears that the
    reference is the merged document? Or is that outside knowledge?"* Both
    were forward verdicts, so in both cases the answer was `merged.md`, and
    the report gave them no way to know that.

    The word comes from the prompt. `prompts/verify.md` opens *"The reference
    text is the merged document {target_filename}"*; `prompts/verify_reverse.md`
    frames the same role as the source documents. So "the reference" means
    opposite documents depending on the direction, the rationale is the model's
    own prose and the report prints it verbatim -- and nothing beside it said
    which frame it was written in.

    This names the document instead of the role. It is `verify.target_files`'s
    answer, rebuilt from the `Run` rather than imported from it: `verify` reads
    a `documents` mapping that the report does not have, and both are derived
    from the same rule -- forward reads the merge, reverse reads every source.

    Not the same thing as `evidence_source`, and they are printed side by side
    on purpose. This is the document the pass was *given*; `evidence_source` is
    the document the model *said* it quoted, and a verdict where the two
    disagree is exactly an `attribution_error`.
    """
    return join_names([f"`{name}`" for name in judged_against_names(run, direction)])


def judged_against_names(run: Run, direction: str) -> list[str]:
    """The same answer as display names, unquoted and unjoined.

    Two functions because the HTML report may not take the Markdown one: a
    filename is a value that came from the caller, `inline` honours `**` and
    backticks in the prose it is given, and `tests/test_html_report.py` holds
    a filename carrying both as a must-fire probe. So the renderer that
    escapes gets the names and builds its own markup around them.
    """
    if direction == "source_to_merged":
        return [run.display(MERGED)]
    return [run.display(name) for name in run.sources()]


def join_names(names: list[str]) -> str:
    """`a`, `b` and `c`, or the sentence for a run that has none of them."""
    if not names:
        return "the source documents"
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " and " + names[-1]


# What a reader has to know before they can weigh a rationale, said once per
# report rather than once per finding.
#
# It answers the operator's second question -- *"Or is that outside
# knowledge?"* -- and it answers it honestly, which means not claiming more
# than this tool checks. `prompts/verify.md` and `prompts/verify_reverse.md`
# both say *"Judge only against the reference text. Ignore outside
# knowledge."*, and that is an instruction, not a guarantee: nothing in this
# pipeline can tell a verdict reached from the document apart from one reached
# from what the model already knew about the subject. Writing "nothing was
# judged against outside knowledge" would be this report asserting a property
# it has no check for, which is the one thing it refuses everywhere else.
#
# The quoted span is what makes the difference checkable by a person, so the
# sentence points at it. A grounded span located in the named document is
# evidence the verdict came from the document; a rationale with no span behind
# it is the reader's to weigh.
REFERENCE_NOTE = (
    "Each finding below names the document it was judged against. The model is "
    "told to use that document alone and to ignore anything it knows from "
    "elsewhere, and nothing here can prove it did -- so a rationale that reads "
    "like general knowledge is one to check against the span it quoted."
)


def invention_sentence(run: Run) -> str:
    """The guarantee a run that never read the merge back does not carry.

    The second sentence in this file that suspends part of a verdict rather
    than narrowing it, and it sits beside `addition_sentence` for the reason
    that one gives: it goes on every exit code, because a caveat that appears
    only on a clean run is missing from the report anyone reads carefully.

    Worded from `advice.noinvention` in `web/locales/en.json`, which the page
    has said since W1. Two surfaces describing the same suspended guarantee in
    two sets of words is how a reader comes to believe they mean two different
    things, and this project has the worked example: at `coverage` the page
    said the run had checked "in both directions" two words before saying
    nothing had read the merge back (504).

    Keyed on `Run.detects_invention` and never on a depth's name, for the
    reason that property's own docstring gives.
    """
    return (
        "**This run checked only that your documents' content survived.** "
        "Nothing read the merged document back, so nothing here asked whether "
        "the merge added anything your documents do not contain: a clean "
        "result means content was carried across, not that nothing was "
        "invented."
    )


def lost_classes(run: Run) -> str:
    """The failure classes a clean headline is entitled to rule out.

    `invented` is in that list only when something went looking for invention.
    It was in it unconditionally, so a `coverage` run -- which makes no
    reverse pass at all and says so two steps earlier in the same report --
    opened with a sentence ruling out the one thing it had not examined. The
    rest of the list is what the forward pass answers and is true at either
    depth.

    M7 task 13's rule, applied to the axis it did not have: a headline must
    not be broader than the check behind it.

    Keyed on `checked_for_invention` rather than on `detects_invention`, which
    is the narrower of the two and was the one this read first. A depth that
    *can* read the merge back has not read it back when there was nothing to
    read: the page has keyed its version of this sentence on the reverse count
    since W1 and argued there that the count is the more general statement, and
    it is right -- but the fix landed on the page and this function kept the
    depth-shaped half of it (528).
    """
    if not run.checked_for_invention:
        return "or carried only in part"
    return "invented, or carried only in part"


def directions_checked(run: Run) -> str:
    """How many claims each direction actually carried, in one clause.

    One clause in three branches of `verdict_line`, because all three used to
    write it out and all three therefore said "N merge claim(s) checked
    against the sources" over a `coverage` run that never asked -- literally
    true at N=0 and read by nobody as "this pass did not run". `advice.clean.
    forward` is the page's version of the same repair.

    The clause is not a sentence and carries no full stop: every caller
    continues it.

    On `checked_for_invention` for the reason `lost_classes` gives one function
    up, and for this one's own: "0 merge claim(s) checked against the sources"
    is the exact sentence the first paragraph calls literally true and read by
    nobody as "this pass did not run".
    """
    forward = f"{run.submitted('forward')} source claim(s) checked against the merge"
    if not run.checked_for_invention:
        return forward + ", and none in the other direction"
    return (f"{forward}, {run.submitted('reverse')} merge claim(s) checked "
            f"against the sources")


def scope_sentence(run: Run) -> str:
    """What a clean verdict covers. M7 task 13, and then task 36 narrowed it again.

    Task 13 added the caveat because the headline was broader than the check
    behind it: `prompts/decompose.md` skips headings and formatting, so a merge
    that dropped both titles was reported clean. Wiring the reconciler closed
    that gap for `merge` runs, and leaving the caveat in place would now
    understate the run — which is the same defect pointing the other way, and
    just as much a reason not to trust the number beside it.
    """
    if run.reconciled is None:
        return (
            "This covers the claims that were extracted, not the documents: "
            "titles, headings and formatting are not claims and were not checked."
        )
    return (
        f"The {CHECKS} mechanical checks under Structure below cover what "
        f"the claims do not: titles, invariant-core tokens, and all "
        f"{run.reconciled.segments} source segment(s) — including the ones no claim "
        f"was drawn from."
    )


def counted_findings(run: Run) -> tuple[list[str], list[str]]:
    """What was found, as "3 dropped" phrases: the claims' first, the structure's.

    Split out of `verdict_section` so the closing block on stderr can say what
    the verdict line says. A run that ends `Finished, with problems` and names
    nothing sends its operator to the report to find out whether one link lost a
    character or forty claims went missing, and those are not the same news.
    Counted once here so the two channels cannot disagree.
    """
    claims = [
        f"{len([v for v in run.findings if v.finding == kind])} "
        f"{kind.replace('_', ' ')}"
        for kind in FINDING_ORDER
        if any(v.finding == kind for v in run.findings)
    ]
    structural = [
        f"{len([f for f in run.structural if f.kind == kind])} "
        f"{kind.replace('_', ' ')}"
        for kind in FINDING_KINDS
        if any(f.kind == kind for f in run.structural)
    ]
    return claims, structural


def what_was_found(run: Run) -> list[str]:
    """The findings as sentences, for a terminal rather than for a document.

    One line per kind: how many, and the same gloss the report prints as a
    heading, which is where the reader would otherwise have to go to learn that
    `verbatim_violation` means a token that had to survive unchanged did not.
    The heading tables are the source, so a kind cannot be explained here in
    words the report contradicts three sections down.
    """
    lines = []
    for kind in FINDING_ORDER:
        hits = [v for v in run.findings if v.finding == kind]
        if hits:
            lines.append(f"{len(hits)} {_plain_heading(HEADINGS[kind])}"
                         f" (see `## Findings`)")
    for kind in FINDING_KINDS:
        hits = [f for f in run.structural if f.kind == kind]
        if hits:
            lines.append(f"{len(hits)} {_plain_heading(STRUCTURAL_HEADINGS[kind])}"
                         f" (see `## Structure`)")
    if run.attributions:
        lines.append(f"{len(run.attributions)} statement(s) "
                     f"{MISATTRIBUTED_WORDS} (see `## Attributions`)")
    if run.number_faults:
        lines.append(f"{len(run.number_faults)} value(s) "
                     f"{NUMBER_CHANGED_WORDS} (see `## Number format`)")
    return lines


def _plain_heading(heading: str) -> str:
    """`Dropped - in a source, not in the merge`, lower-cased after the dash.

    The heading is a title in the report and a sentence on the terminal, and the
    part after the dash is already the sentence. Taking it rather than writing a
    second gloss is the point: two glosses drift.
    """
    name, _, gloss = heading.partition(" \u2014 ")
    return f"{name.lower()}: {gloss}" if gloss else name.lower()


def verdict_line(run: Run) -> str:
    """The headline, in one sentence, before any renderer sees it.

    Split out of `verdict_section` for the reason `counted_findings` was split
    out of it one function up: the sentence is now printed by two renderers and
    the terminal, and a headline that differed between the Markdown report and
    the HTML one would be two verdicts on one run.
    """
    code = exit_code(run)
    cancelled = [step for step in run.errored
                 if step.detail.startswith(CANCELLED_PREFIX)]
    if code == 2 and cancelled:
        # Stopped on purpose (639), which is not "the model could not be made
        # to answer": the sentence below would blame the model for a cancel.
        # Still a 2, and still a partial reading, said as one.
        return (
            f"**Cancelled.** The run was stopped during "
            f"{cancelled[0].name}, before it finished, so it does not establish "
            f"anything about the claims it did not reach. What ran is listed "
            f"below, and the calls it made are counted in the provenance."
        )
    if code == 2 and inconclusive_for_retrieval_alone(run):
        # 665. Finished and recalled; the errored-unit sentence below would
        # blame the model for not answering, and it answered.
        line = NOT_SOURCED
        found = (len(run.findings) + len(run.structural)
                 + len(run.attributions) + len(run.number_faults))
        if found:
            line += (f" What the checks found in it: {found} finding(s); see "
                     f"below.")
    elif code == 2:
        # Two ways to be inconclusive and they are not the same sentence. A
        # unit of work that errored produced nothing at all; a record Pass C
        # dropped came out of a unit that did produce something, and the rest
        # of it was graded. A run can be both. Entry 194.
        parts = []
        if run.errored:
            which = ", ".join(step.name for step in run.errored)
            parts.append(
                f"{len(run.errored)} unit(s) of work errored ({which})")
        if run.unusable:
            parts.append(
                f"{len(run.unusable)} claim(s) came back with a record that "
                f"could not be graded")
        line = (
            f"**Inconclusive.** {'; '.join(parts)}. The model could not be made "
            f"to answer usably, so this run does not establish that the claims "
            f"it did check are the only ones there were."
        )
        # What the gradeable part did say, if it said anything. Suppressing it
        # would make a salvaged run indistinguishable from one that produced
        # no report at all, which is the entire difference Pass C makes; but it
        # goes after the inconclusive sentence and never in place of it,
        # because a finding count under a 2 is a partial reading and has to be
        # read as one.
        found = (len(run.findings) + len(run.structural)
                 + len(run.attributions) + len(run.number_faults))
        if found:
            line += (
                f" Of what could be graded, {found} finding(s); see below. "
                f"That total is over the graded part only."
            )
    elif code == 1:
        # The reconciler's are counted in the headline rather than left to the
        # section below. A total that excluded them would be a number smaller
        # than the list underneath it, and the two are added rather than merged
        # because a claim a model judged and a token that moved are not the same
        # kind of thing — so the sentence names which of them is which.
        counts, structural = counted_findings(run)
        total = (len(run.findings) + len(run.structural)
                 + len(run.attributions) + len(run.number_faults))
        # Over budget with nothing else wrong is a real exit 1, and it has no
        # findings to enumerate. Saying "0 finding(s)" above a failing exit code
        # would be the report disagreeing with the command, so the breach gets
        # the headline in that case and is appended to it otherwise.
        if total:
            line = f"**{total} finding(s).**"
            if counts:
                line += " In the claims: " + ", ".join(counts) + "."
            if structural:
                line += " In the structure: " + ", ".join(structural) + "."
            if run.attributions:
                line += (f" In the attributions: {len(run.attributions)} "
                         f"{MISATTRIBUTED_WORDS}.")
            if run.number_faults:
                line += (f" In the numbers: {len(run.number_faults)} value(s) "
                         f"{NUMBER_CHANGED_WORDS}.")
        else:
            line = "**Declared loss over budget.**"
        # One or the other, never both: `queue_sentence` says the queued claims
        # are not charged, which is true of each of them and false of the run
        # once the volume is the finding. Printing both would put "not charged"
        # in the same paragraph as the reason the run failed.
        if run.over_budget:
            line += " " + budget_sentence(run)
            if run.queued:
                line += (
                    f" The {len(run.queued)} claim(s) they cost are listed in "
                    f"the review queue below."
                )
        elif run.queued:
            line += " " + queue_sentence(run)
    elif code == RECORD_ONLY:
        # Entry 420. Without this branch a 3 would fall through to the clean
        # sentence below and the report would contradict the code it printed --
        # the same defect the comment fifteen lines up guards against for the
        # over-budget case.
        #
        # The sentence has to do two things at once and the order matters. It
        # says what is wrong, because a record fault is a real fault; and it
        # says what is *not* wrong, because the reader's next question is
        # whether they can ship the document, and on this code the answer as
        # far as the tool looked is yes. Leading with the reassurance would bury
        # the finding; omitting it would leave a reader to assume 3 means the
        # merge is bad, which is the misreading this split exists to end.
        counts, structural = counted_findings(run)
        total = len(run.structural)
        line = (
            f"**{total} finding(s), all in the merge's account of itself.**"
        )
        if structural:
            line += " " + ", ".join(structural).capitalize() + "."
        line += (
            f" The merged document itself carries no finding: "
            f"{directions_checked(run)}, and none of the reconciler's checks "
            f"found content missing, invented, altered or repeated. What is "
            f"wrong is what the merge said it did. "
        ) + scope_sentence(run)
        if run.queued:
            line += " " + queue_sentence(run)
    elif run.queued:
        # The clean sentence would be false here: claims *were* dropped, and the
        # only reason the run passes is that the merge said so first. M7 task 27.
        # Printing the usual line and letting the queue section correct it below
        # would put the strongest wording in the report next to the one figure it
        # is wrong about, which is how §2.5's split turns into a lie by layout.
        line = (
            f"**No undeclared claim was dropped, contradicted, "
            f"{lost_classes(run)}.** "
            f"{directions_checked(run)}. "
            + queue_sentence(run)
            + " "
            + scope_sentence(run)
        )
    else:
        # M7 task 13. The sentence this replaces was "No claim was dropped,
        # contradicted, or invented", and on 2026-08-10 it was printed over a
        # merge that was a concatenation and had dropped both titles and both
        # summary fields. Every figure beside it was right; the sentence was
        # broader than any of them. What is measured is the claims decompose
        # extracted, and `prompts/decompose.md` skips headings, formatting and
        # boilerplate by design — so titles and structure are outside this
        # denominator, and the verdict now says which question it answered.
        # "or carried only in part" is M7 task 24's addition and belongs in this
        # sentence rather than only in the table: PARTIAL is the verdict a clean
        # run would previously have absorbed into SUPPORTED, and a headline that
        # still listed three failure classes would be narrower than the check
        # that produced it — the same defect task 13 fixed in this very line.
        line = (
            f"**No extracted claim was dropped, contradicted, "
            f"{lost_classes(run)}.** "
            f"{directions_checked(run)}. "
            + scope_sentence(run)
        )
    # Said last so it cannot be read past. A source that yielded no claims was
    # not examined, and the sentence above is about the claims that were: on
    # `verify` there is no reconciler result behind it, so coverage for that
    # source is not weakly established, it is unestablished. On `merge` the
    # reconciler did check it structurally, so the claim is narrower rather
    # than absent -- and the report says which of the two it is.
    # Before the unexamined-sources sentence, because that one narrows the
    # denominator and this one suspends a guarantee. Ordering them the other
    # way would put the weaker caveat last, where a skimming reader stops.
    if run.declared_additions:
        line += " " + addition_sentence(run)

    # Whether the level that promised retrieval delivered it, beside the
    # additions it qualifies and on every exit code (568). Empty below
    # `sourced`, so every other run's verdict is unchanged.
    retrieval = retrieval_sentence(run)
    if retrieval:
        line += " " + retrieval

    # The second suspension, next to the first and in the order the page puts
    # them (`app.js`: advice, then additions, then the suspended guarantee).
    # Two surfaces that agree about a caveat's *place* as well as its words
    # are two surfaces a reader can move between.
    if not run.detects_invention:
        line += " " + invention_sentence(run)

    # After the addition notice, because that one suspends a guarantee and
    # this one explains a finding the reader can see. Ordering them the other
    # way would put the explanation where the suspension belongs.
    if run.covering_contradictions:
        line += " " + covering_sentence(run)

    # The number-format warnings (601), on every exit code. They move nothing,
    # so a clean headline stays clean, but a reader told "clean" over a
    # document that writes 4,5 in English has been told less than the tool
    # knows.
    if run.number_warnings:
        line += " " + number_warning_sentence(run)

    # Last of the three, and the only one that is not about the merge at all.
    # A reader who has just been told the run is clean needs this before they
    # act on it.
    if run.mismatch:
        line += " " + mismatch_sentence(run)

    unexamined = run.unexamined_sources()
    if unexamined:
        named = ", ".join(f"`{name}`" for name in unexamined)
        if run.command == "verify":
            line += (f" **{named} produced no claims, so nothing about "
                     f"{'them was' if len(unexamined) > 1 else 'it was'} "
                     f"examined and coverage for "
                     f"{'them' if len(unexamined) > 1 else 'it'} is "
                     f"unestablished.**")
        else:
            line += (f" **{named} produced no claims, so coverage for "
                     f"{'them rests' if len(unexamined) > 1 else 'it rests'} "
                     f"on the reconciler's structural check alone.**")
    return line


def verdict_section(run: Run) -> str:
    return f"## Verdict\n\n{verdict_line(run)}\n"


def coverage_section(run: Run) -> str:
    graded = [v for v in run.verdicts if v.grounding != NOT_GRADED]
    grounded = [v for v in graded if v.grounding == GROUNDED]
    forward_submitted = run.submitted("forward")
    reverse_submitted = run.submitted("reverse")

    rows = [
        (f"Claims extracted from `{run.display(name)}`", str(len(run.claims[name])))
        for name in sorted(run.claims)
    ]
    rows += [
        (
            "Forward — source claims accounted for in the merge",
            ratio(
                len([v for v in run.forward if v.finding == "none"]),
                len(run.forward),
                f"not checked ({forward_submitted} claim(s) extracted)",
            ),
        ),
        # Its own row, next to the ratio it is missing from, because both ways
        # of hiding it are wrong. Counted in the numerator above it would say a
        # claim carried in part was carried; left out of the table entirely, the
        # ratio reads as full loss and overstates the damage. The row is printed
        # at zero for the same reason the errored row is: a reader has to be able
        # to see that it was looked for.
        (
            "Forward — carried only in part",
            str(len([v for v in run.forward if v.finding == "partially_dropped"])),
        ),
    ]
    # One row per source, each against its own claims. The pooled row above is
    # kept and kept first: it is the figure every published number was measured
    # as, and the per-source rows are what say whether it is an average of two
    # similar things or of a success and a failure.
    by_source = run.forward_by_source()
    for name in sorted(by_source):
        row = by_source[name]
        if not name:
            # Unreachable through the pipeline; see `forward_by_source`. Printed
            # only when it fires, because a permanent zero row here would be a
            # standing invitation to read a harness invariant as a measurement.
            rows.append(("Forward — claims matching no source", str(row["checked"])))
            continue
        value = ratio(
            row["accounted"],
            row["checked"],
            "no claims extracted — nothing to check"
            if row["extracted"] == 0
            else f"not checked ({row['extracted']} claim(s) extracted)",
        )
        if row["partial"]:
            value += f" ({row['partial']} in part)"
        rows.append((f"Forward — `{run.display(name)}` claims accounted for", value))
    rows += [
        (
            "Reverse — merge claims found in a source",
            ratio(
                len([v for v in run.reverse if v.finding == "none"]),
                len(run.reverse),
                f"not checked ({reverse_submitted} claim(s) extracted)",
            ),
        ),
        (
            "Reverse — supported only in part",
            str(len([v for v in run.reverse if v.finding == "partially_invented"])),
        ),
        (
            "Evidence grounded",
            ratio(len(grounded), len(graded), "no verdict quoted a span"),
        ),
        ("Units of work errored", str(len(run.errored))),
        # Printed at zero for the reason the errored row above it is: the
        # numerator of every ratio in this table counts claims that came back
        # with a verdict, and a reader has to be able to see that the ones
        # that did not were looked for and counted. Entry 194.
        ("Claims submitted but not graded", str(len(run.unusable))),
    ]

    lines = ["## Coverage", "", "| | |", "|---|---|"]
    lines += [f"| {label} | {value} |" for label, value in rows]

    # One naming system, not two: every row above and every finding below uses
    # `run.display`, a short name built from the caller's own path (entry 411).
    # There is nothing left here to reconcile against a canonical name.

    if run.errored:
        for step in run.errored:
            lines += ["", f"> **{step.name} errored.** {step.detail}"]
    return "\n".join(lines) + "\n"


def elsewhere(run: Run) -> str:
    """Where a run's findings are when none of them is in the claims.

    `findings_section`'s sentence, and the HTML page's with its markup taken
    off, so the two cannot say it differently. The attributions (569) are the
    second place a finding can be and the first that exists on `verify` too.
    """
    structural, attributions = len(run.structural), len(run.attributions)
    if run.number_faults:
        return _elsewhere_with_numbers(run)
    if not attributions:
        return (f"None in the claims. The {structural} finding(s) this run "
                f"reports are structural and are listed under `## Structure` "
                f"below.")
    moved = (f"statement(s) {MISATTRIBUTED_WORDS}, listed under "
             f"`## Attributions` below")
    if not structural:
        return (f"None in the claims. The {attributions} finding(s) this run "
                f"reports are {moved}.")
    return (f"None in the claims. Of the {structural + attributions} finding(s) "
            f"this run reports, {structural} are structural and are listed under "
            f"`## Structure` below, and {attributions} are {moved}.")


def findings_section(run: Run) -> str:
    lines = ["## Findings"]
    if not run.findings:
        # "None." under a verdict that opened "1 finding(s)" is the report
        # contradicting itself on the one page a reader checks first. It happens
        # whenever every finding is structural: those are listed further down,
        # under a heading this section never mentions. So the sentence says
        # which question it answered and where the rest of the answer is —
        # `verdict_section` already counts both, and this is the section that
        # was silent about the difference.
        if run.structural or run.attributions or run.number_faults:
            lines += ["", elsewhere(run)]
        else:
            lines += ["", "None."]
        return "\n".join(lines) + "\n"

    lines += ["", REFERENCE_NOTE]
    by_id = {claim.id: claim for claims in run.claims.values() for claim in claims}
    for kind in FINDING_ORDER:
        hits = [v for v in run.findings if v.finding == kind]
        if not hits:
            continue
        lines += ["", f"### {HEADINGS[kind]}", ""]
        for verdict in hits:
            claim = by_id.get(verdict.claim_id)
            where = (
                f"`{run.display(claim.source)}:{claim.line}`" if claim else "unknown line"
            )
            text = claim.text if claim else verdict.claim_id
            if kind == "contradicted":
                # Both halves, labelled by side. A contradiction is the one
                # finding class where the reader's question is "which of these
                # two do I believe", and until this section printed the two
                # statements next to each other under the names of the files
                # they came from, it printed one of them and a sentence about
                # the other. Both were already on the verdict.
                #
                # No line saying which side is right. The merge declared no
                # such choice -- `parsing.DISPOSITION_FIELDS` has no slot for
                # one -- so any such line would be this tool writing the
                # justification it exists to check. That is a merge-contract
                # change and it is registered rather than guessed at.
                lines.append(f"- **{verdict.claim_id}** -- the two documents disagree")
                lines.append(f"  - {where} says: {text}")
                if verdict.evidence:
                    lines.append(
                        f"  - `{run.display(verdict.evidence_source)}` says: "
                        f"{verdict.evidence!r} "
                        f"({'grounded' if verdict.grounded else verdict.grounding})"
                    )
                else:
                    lines.append(
                        "  - the other side quoted nothing, so what it says "
                        "instead is not on the record"
                    )
                # Before the rationale, not after it. The rationale is the
                # prose that says "the reference", so the line naming the
                # reference has to have been read first.
                lines.append(
                    f"  - checked against: {judged_against(run, verdict.direction)}"
                )
                if verdict.rationale:
                    lines.append(f"  - why this was read as a contradiction: "
                                 f"{verdict.rationale}")
                continue
            lines.append(f"- **{verdict.claim_id}** ({where}) — {text}")
            if verdict.evidence:
                lines.append(
                    f"  - evidence: {verdict.evidence!r} in "
                    f"`{run.display(verdict.evidence_source)}` "
                    f"({'grounded' if verdict.grounded else verdict.grounding})"
                )
            lines.append(
                f"  - checked against: {judged_against(run, verdict.direction)}"
            )
            if verdict.rationale:
                # Whose words these are, not just that they exist (717): the
                # operator read "Reason" beside a sentence like "the text
                # attributes the collecting to Chris, not Christ" and asked
                # which text -- the source, or the generated merge. The
                # sentence itself is the checking model's own prose, straight
                # out of `prompts/verify.md`'s `rationale` field, and cannot be
                # reworded without re-keying every recorded cassette that
                # produced one, so the label says whose voice it is instead.
                lines.append(f"  - why it was flagged, in the checker's own "
                             f"words: {verdict.rationale}")
    return "\n".join(lines) + "\n"


def cell(text: str) -> str:
    """One claim, whole, in a Markdown table cell.

    Escaping, never shortening. A pipe would end the cell early and a newline
    would end the row, so both are rewritten into forms Markdown renders back
    as themselves -- and that is the whole of what happens to the text. This
    project's own finding is that a claim bundling three facts can be scored
    covered by a merge that dropped one; a report that then abbreviated the
    claim would hide the second half of exactly that failure. The cell wraps
    instead. It is the reader's window that is too narrow, not the claim.
    """
    return text.replace("|", "\\|").replace("\n", "<br>").strip()


def where_line(run: Run, claim: Claim) -> str:
    """The line a claim sits on, and whether anybody checked that it does.

    `decompose.anchor` returns `anchored=False` when it could not find the span
    in the document, which means the model paraphrased rather than copied and
    the number beside it is the model's own estimate. A report renders an
    unverified line with exactly the authority of a verified one, so the two
    cannot look the same here.
    """
    return str(claim.line) if claim.anchored else f"{claim.line} (unverified)"


def evidence_note(verdict: Verdict | None, run: Run) -> str:
    """What was quoted, from where, and whether it was found there.

    Printed on clean rows as well as findings, and that is the point of the
    column. A table whose carried rows were blank could not be told apart from
    a table whose carried rows were never examined, which is the failure this
    whole report is arranged around.

    An ungrounded quote is marked in the row it sits in. `grounding` has three
    non-grounded outcomes and they are different faults: the span exists
    nowhere, or it exists in a file the model did not name, or there was no
    span to locate because the verdict was MISSING. The first two are printed
    as the words `verify` uses for them; the third prints no quote at all,
    because there is none, and says so.
    """
    if verdict is None:
        return "the pass did not report on this claim"
    if verdict.grounding == NOT_GRADED or not verdict.evidence:
        return verdict.rationale
    mark = "" if verdict.grounded else f", **{verdict.grounding}**"
    quote = (f"{verdict.evidence!r} in `{run.display(verdict.evidence_source)}`"
             f"{mark}")
    return f"{quote} -- {verdict.rationale}" if verdict.rationale else quote


def tally(statuses: list[str], order: tuple[str, ...], names: dict[str, str]) -> str:
    """`6 carried, 1 dropped`, counted from the rows and from nothing else.

    The argument is the list of statuses the table actually printed, so the
    heading cannot disagree with the rows under it however the rows were
    built. `NOT_CHECKED` is appended last and only when it fired: a permanent
    zero would invite a reader to treat a harness invariant as a measurement.
    """
    parts = [f"{statuses.count(names[kind])} {names[kind]}" for kind in order]
    missing = statuses.count(NOT_CHECKED)
    if missing:
        parts.append(f"{missing} {NOT_CHECKED}")
    return ", ".join(parts)


def forward_inventory(run: Run, name: str) -> tuple[list[str], list[str]]:
    """One source document, every claim drawn from it, and what became of it.

    Returns the lines and the statuses, so the caller can hold the statuses
    against the coverage table rather than trust that two functions counting
    the same verdicts agree.
    """
    verdicts = {v.claim_id: v for v in run.forward}
    claims = run.claims.get(name, [])
    rows, statuses = [], []
    for index, claim in enumerate(claims, start=1):
        verdict = verdicts.get(claim.id)
        status = FORWARD_STATUS[verdict.finding] if verdict else NOT_CHECKED
        statuses.append(status)
        rows.append((index, claim, status, verdict))
    # Findings first. `sorted` is stable, so within a status the claims stay in
    # the order they were extracted, which is the order they appear in the file.
    rank = {FORWARD_STATUS[kind]: i for i, kind in enumerate(FORWARD_ORDER)}
    rows.sort(key=lambda row: rank.get(row[2], len(rank)))

    lines = [
        "",
        f"### `{run.display(name)}` -- {len(claims)} claim(s): "
        f"{tally(statuses, FORWARD_ORDER, FORWARD_STATUS)}",
        "",
        # The Note column prints the model's rationale verbatim, and that prose
        # says "the reference" without ever saying which file it means. The
        # caption says it once for the whole table instead of once per row.
        f"Each claim below was read against "
        f"{judged_against(run, 'source_to_merged')}.",
        "",
        "| # | Claim | Line | Status | Note |",
        "|---|---|---|---|---|",
    ]
    for index, claim, status, verdict in rows:
        lines.append(
            f"| {index} | {cell(claim.text)} | {where_line(run, claim)} | "
            f"{status} | {cell(evidence_note(verdict, run))} |"
        )
    if not claims:
        # The caption and the two header rows go together: "each claim below
        # was read against X" over an empty table would describe a reading
        # that did not happen, which is the sentence class this report spends
        # most of its length refusing.
        lines[-4:] = ["No claim was extracted from this document, so the merge "
                      "was checked against nothing from it."]
    return lines, statuses


def reverse_inventory(run: Run) -> tuple[list[str], list[str]]:
    """The merged document's own claims, and which source each was found in.

    The mirror of the tables above and it has to be read as one: a merge can
    carry every source claim and still assert things no source does, and that
    failure is invisible in any table keyed on the sources.
    """
    verdicts = {v.claim_id: v for v in run.reverse}
    claims = run.claims.get(MERGED, [])
    rows, statuses = [], []
    for index, claim in enumerate(claims, start=1):
        verdict = verdicts.get(claim.id)
        status = REVERSE_STATUS[verdict.finding] if verdict else NOT_CHECKED
        statuses.append(status)
        rows.append((index, claim, status, verdict))
    rank = {REVERSE_STATUS[kind]: i for i, kind in enumerate(REVERSE_ORDER)}
    rows.sort(key=lambda row: rank.get(row[2], len(rank)))

    lines = [
        "",
        f"### `{run.display(MERGED)}` -- {len(claims)} claim(s): "
        f"{tally(statuses, REVERSE_ORDER, REVERSE_STATUS)}",
        "",
        f"Each claim below was read against "
        f"{judged_against(run, 'merged_to_sources')}.",
        "",
        "| # | Claim | Status | Found in | Note |",
        "|---|---|---|---|---|",
    ]
    for index, claim, status, verdict in rows:
        # The file the model said it found support in, which is the answer to
        # "where does this come from" and the one column a KB editor reading a
        # merged article actually needs. Blank when nothing was found, rather
        # than naming a file: an invented claim is in no source, and printing
        # one would be the report inventing a provenance for it.
        found = (
            f"`{run.display(verdict.evidence_source)}`"
            if verdict and verdict.evidence_source and verdict.finding != "hallucinated"
            else "--"
        )
        lines.append(
            f"| {index} | {cell(claim.text)} | {status} | {found} | "
            f"{cell(evidence_note(verdict, run))} |"
        )
    if not claims:
        lines[-4:] = ["No claim was extracted from the merged document, so "
                      "nothing in it was checked back against the sources."]
    return lines, statuses


class InventoryDisagrees(Exception):
    """The tables and the coverage table counted the same verdicts differently.

    Raised rather than logged. Two figures for one quantity in one document is
    the defect this report exists to refuse, and a reader cannot tell which of
    them to believe -- so the run comes back inconclusive instead of printing
    both. It cannot fire on any path through `pipeline`: both figures are read
    off `run.forward`. It exists for the next caller who builds a `Run` by hand.
    """


def inventory_section(run: Run) -> str:
    """Every claim, carried or not. The exceptions are above; this is the whole.

    The findings list answers "what went wrong". It cannot answer "was this
    fact carried over", which is the question somebody merging two knowledge
    base articles is actually holding, and an exception-only report answers it
    only by silence. Silence is what this project refuses everywhere else: a
    check that examined nothing produces the same empty findings list as a
    check that examined everything.

    Every count in every heading is `.count()` over the statuses the rows were
    printed with. Nothing here asks a model for a total, and nothing here
    recomputes one from the verdicts a second time -- the coverage table
    already did that, and the two are held against each other below rather
    than left free to drift.
    """
    lines = ["## Inventory", "",
             "Every claim that was extracted, and what became of it. The "
             "sections above list only the exceptions; this lists all of them, "
             "so a claim that is not here was never checked."]
    by_source = run.forward_by_source()
    for name in run.sources():
        rows, statuses = forward_inventory(run, name)
        lines += rows
        row = by_source.get(name)
        if row is None:
            continue
        counted = {
            "extracted": len(statuses),
            "checked": len([s for s in statuses if s != NOT_CHECKED]),
            "accounted": statuses.count(FORWARD_STATUS["none"]),
            "partial": statuses.count(FORWARD_STATUS["partially_dropped"]),
        }
        if counted != row:
            raise InventoryDisagrees(
                f"{name}: the inventory rows count {counted} and the coverage "
                f"table counts {row}. One report, two answers."
            )
    if MERGED in run.claims:
        rows, statuses = reverse_inventory(run)
        lines += rows
        accounted = len([v for v in run.reverse if v.finding == "none"])
        if statuses.count(REVERSE_STATUS["none"]) != accounted:
            raise InventoryDisagrees(
                f"{run.display(MERGED)}: the inventory counts "
                f"{statuses.count(REVERSE_STATUS['none'])} supported and the "
                f"coverage table counts {accounted}. One report, two answers."
            )
    return "\n".join(lines) + "\n"


def leak_lines(run: Run) -> list[str]:
    """The findings the reconciler did not make, for the not-reconciled path.

    The prompt leaks and the restated claims: both are set by the pipeline, both
    move the exit code, and neither needs a reconciliation to have succeeded.
    The reconciled path needs nothing of the kind: its loop already walks
    `FINDING_KINDS` over `run.structural`, which carries these, so they render
    under the same headings this builds. This exists only so that a merge whose
    reconcile step errored still shows what it is exiting 1 for.
    """
    lines: list[str] = []
    for kind, found in ((PROMPT_EXAMPLE_LEAK, run.leaks), (DUPLICATED_CONTENT, run.restated)):
        if not found:
            continue
        lines += ["", f"### {STRUCTURAL_HEADINGS[kind]}", ""]
        lines += [f"- {finding.detail}" for finding in found]
    return lines


def structural_section(run: Run) -> str:
    """The reconciler's nine checks, and what they found. M7 task 36.

    Its own section rather than rows in Findings, because the two carry
    different evidence and a reader has to be able to tell them apart. A finding
    above is a model's verdict on one claim, with a rationale and an evidence
    span that may be wrong. Everything here is arithmetic over two strings — a
    set difference, a containment, a division or an equality test — and can be
    checked by hand against the documents without asking anything. Mixing them would put the
    weakest and the strongest evidence in the tool under one heading.

    It sits directly below Findings and above the review queue, because both are
    failures and the queue is not.
    """
    lines = ["## Structure", ""]
    if run.reconciled is None:
        # Not "None." — the reconciler did not run, so there is no denominator
        # and no result. Printing the empty case would report a check that
        # examined nothing as a check that found nothing, which is the one
        # confusion this whole file is written to prevent.
        lines.append(
            "**Not checked.** The reconciler did not run over this merge, so "
            "nothing below the claim level was examined: no title, no "
            "invariant-core token, and no source segment that produced no claim."
        )
        # Except the leak check, which needs no reconciliation and may have run
        # anyway. Printing "not checked" over a finding that is already setting
        # the exit code would be the report contradicting the command.
        return "\n".join(lines + leak_lines(run)) + "\n"

    lines.append(
        f"**{CHECKS}** mechanical check(s) over **{run.reconciled.segments}** "
        f"source segment(s) and what the merge declared about them. No model was "
        f"asked anything: every check here is a set difference, a string "
        f"containment or a division."
    )
    # Said before any count, because it changes what the counts are counting: a
    # document whose fence never closes has everything after the opener in one
    # code block, so prose that follows it is scored as code. The tool does not
    # close the fence -- that would be deciding what the author meant -- so the
    # reader is told where it opened and decides.
    for name, line, reason in run.unclosed_fences:
        lines.append("")
        lines.append(
            f"**Unclosed fence in `{name}`.** A fence opened at line {line} and "
            f"is never closed, so every line after it is one code block and any "
            f"prose among them is compared as code. Nothing here closed it: the "
            f"segmentation is what the document says, not what it probably "
            f"meant."
        )
    if run.merged is not None:
        # Its own sentence, and outside the count above. The nine hold the merge
        # against its sources; this one holds it against the prompt, and folding
        # it into the denominator would make `checks: 9` in the JSON disagree
        # with the number printed here.
        lines.append(
            f"Separately, and not one of those {CHECKS}: the merged text was "
            f"searched for `merge.md`'s worked-example words "
            f"({', '.join(f'`{w}`' for w in merge.EXAMPLE_MARKERS)}), which "
            f"belong to no source document."
        )
        # The second thing outside the denominator, and the arithmetic beside
        # it. The counts are evidence and not the test: `decompose` is not
        # reproducible at temperature 0 -- 18 claims one run and 22 the next on
        # an identical request (entry 400) -- so a merge whose claim count
        # exceeds its sources' has probably said something twice, and a check
        # that fired on that alone would fire and miss at random. The repeated
        # claims are the finding; this line is what makes one legible.
        if MERGED in run.claims:
            from_merge = len(run.claims[MERGED])
            from_sources = sum(
                len(claims) for name, claims in run.claims.items() if name != MERGED
            )
            lines.append(
                f"Separately again: the **{from_merge}** claim(s) extracted from "
                f"the merged document were checked for one claim appearing on two "
                f"different lines, which is a merge that kept both sources' "
                f"wordings of one fact. The sources yielded **{from_sources}**. "
                f"The two counts are reported, not compared: claim extraction is "
                f"a sample, so a merge count above a source count is evidence and "
                f"never the finding."
            )
    lines += ["", order_line(run)]
    if not run.structural:
        lines += ["", "No structural finding."]
        return "\n".join(lines) + "\n"
    # Once, above the findings, and only where one of them will use it. A
    # legend for a notation nothing in this report uses is a line that teaches
    # a reader to skip the hints (552).
    if any(finding.difference for finding in run.structural):
        lines += ["", DIFF_LEGEND]

    for kind in FINDING_KINDS:
        hits = [f for f in run.structural if f.kind == kind]
        if not hits:
            continue
        lines += ["", f"### {STRUCTURAL_HEADINGS[kind]}", ""]
        for finding in hits:
            where = " ".join(
                part
                for part in (
                    f"`{finding.segment}`" if finding.segment else "",
                    f"(`{run.display(finding.document)}`)" if finding.document else "",
                )
                if part
            )
            lines.append(f"- {where + ' — ' if where else ''}{finding.detail}")
            block = evidence_lines(finding)
            # A blank line between the sentence and the fence, and the blank
            # line is empty rather than indented: two spaces at the end of a
            # Markdown line is a hard break, which is a rule nobody sees until
            # a renderer obeys it.
            if block:
                lines += [""] + ["  " + line for line in block]
    return "\n".join(lines) + "\n"


# What a finding's two sides are called wherever they are shown (552). Written
# once because three surfaces print them and a fourth name for the same field
# is how the page came to say *cited* where the report said `citation` (544).
EVIDENCE_LABELS = {
    "source": "In the source",
    "merge": "In the merge",
    "difference": "What changed",
}

# How the word diff is introduced on a surface that cannot colour it. The
# notation is `reconcile.REMOVED`/`ADDED`, and a reader meeting `[-x-] {+y+}`
# for the first time needs one clause to read it by -- once per section, not
# once per row.
DIFF_LEGEND = (
    "`[-...-]` is what the source said and `{+...+}` is what the merge says."
)


def stacked_lines(finding) -> list[str]:
    """One finding's two sides, one directly above the other, then the diff.

    **The operator asked to read down a column rather than along a sentence**
    (561): *"they want the source line and the merged line shown one directly
    above the other ... so the difference can be read by scanning down"*. That
    is a layout, and a layout only survives in plain text if the labels are the
    same width -- so they are padded here, once, and every surface stacks the
    same three lines.

    This supersedes half of 552. That entry showed the diff **instead of** the
    two texts wherever a diff existed, on 531's brevity grounds; the operator
    has since asked for both, and they are right that a diff alone makes the
    reader reconstruct two texts from one line. The diff stays, as the third
    line, because it is the only one of the three that says *where* to look.

    Nothing is returned for a finding with no second side, which is most of
    them: a declared-loss ceiling is arithmetic over the whole merge and has no
    pair of strings to show.
    """
    rows = []
    if finding.source_text:
        rows.append((EVIDENCE_LABELS["source"], finding.source_text))
    if finding.merge_text:
        rows.append((EVIDENCE_LABELS["merge"], finding.merge_text))
    if not rows:
        return []
    shown = reconcile_module.difference(finding.source_text, finding.merge_text)
    if shown:
        rows.append((EVIDENCE_LABELS["difference"], shown))
    width = max(len(label) for label, _ in rows)
    return [f"{label + ':':<{width + 1}} {value}" for label, value in rows]


# The plain-text stack goes inside a fence, and the fence is what makes the
# column real: a Markdown reader renders the block monospaced, and a terminal
# reading the same file was monospaced already. As list items the three lines
# would be proportionally spaced in every rendered view, so the padding above
# would buy an alignment only the raw file has -- which is the surface the
# operator is least likely to read it on.
FENCE = "```"


def evidence_lines(finding) -> list[str]:
    """`stacked_lines` as Markdown: a fenced block, or nothing."""
    stack = stacked_lines(finding)
    if not stack:
        return []
    return [FENCE + "text"] + stack + [FENCE]


# How a misattribution is named to a reader (569). One phrase, so the verdict
# line, the terminal and the section cannot call it three things.
MISATTRIBUTED_WORDS = "credited to a source that does not state it"

# What the section is, said once above its rows. The predicate is the whole of
# what makes a row fair to print: a reader is being told the merge misquotes
# one of their documents, and this is how they can check that by hand.
ATTRIBUTIONS_NOTE = (
    "Each sentence below credits a named source with a statement that source "
    "does not contain, while another source contains it word for word. The "
    "name was matched to one source by its title or its filename, and no model "
    "was asked anything. A sentence the merge copied from a source as written "
    "is never listed, and neither is one whose statement no source contains "
    "or whose name fits two sources."
)


def attributions_section(run: Run) -> str:
    """The merge's misattributions, or `` where it made none (569).

    Printed on either command and only when something was found, so every
    report without one reads exactly as before. Its own section and not a
    heading under Structure: on `verify` there is no Structure section, and
    this is the only place a reader of a `coverage` run can learn that the
    merge put a fact in the wrong document's mouth.
    """
    if not run.attributions:
        return ""
    lines = ["## Attributions", "", ATTRIBUTIONS_NOTE, ""]
    for finding in run.attributions:
        lines.append(f"- `{finding.segment}` (`{run.display(finding.document)}`) "
                     f"- {finding.detail}")
        block = evidence_lines(finding)
        if block:
            lines += [""] + ["  " + line for line in block]
    return "\n".join(lines) + "\n"



# How a number-format fault is named to a reader (601). One phrase, for the
# verdict line, the terminal and the section, as `MISATTRIBUTED_WORDS` is.
NUMBER_CHANGED_WORDS = "written by the merge with a different value than its source"

# Said once above the section's rows: what was decided, from what, and which
# rows are faults.
NUMBER_FORMAT_NOTE = (
    "Each document's decimal convention is decided from its own numerals that "
    "can only be read one way, when they all agree; otherwise from its "
    "language (English writes a decimal point, German a decimal comma); "
    "otherwise from the majority of its numerals; and on a tie with no "
    "language, not at all. A numeral written in the other convention is "
    "listed, as is a separator before exactly three digits that the "
    "document's own convention reads as a fraction (17.560 under a decimal "
    "point), because the other convention reads it as thousands. A document "
    "whose numerals all use the convention its language does not write is "
    "listed once, naming them. Only a "
    "merged numeral that states a settled source value differently is a "
    "fault; every other row is a warning, and none of them moves the exit "
    "code. No number was rewritten and no model was asked."
)

_NUMBER_KIND_WORDS = {
    numerals.OTHER_CONVENTION: "other convention",
    numerals.READABLE_TWO_WAYS: "readable two ways",
    numerals.READING_RESOLVED: "reading resolved by the merge",
    numerals.READING_CHANGED: "value changed by the merge",
    numerals.AGAINST_LANGUAGE: "against its language",
}


def number_warning_sentence(run: Run) -> str:
    """The warnings in one sentence for the verdict line: counted, not charged."""
    count = len(run.number_warnings)
    # No `## ` heading in it: the verdict line is shared with the HTML page,
    # and no other sentence in it cites a section by its Markdown marker.
    # Warnings, not numerals: one row against a document's language names
    # every numeral that outvoted it.
    return (f"{count} number-format warning(s), on numerals that could be "
            f"misread, are listed under Number format below and do not move "
            f"the exit code.")


def _elsewhere_with_numbers(run: Run) -> str:
    """`elsewhere`'s sentence where a number-format fault is among the findings."""
    parts = []
    if run.structural:
        parts.append(f"{len(run.structural)} are structural and are listed "
                     f"under `## Structure`")
    if run.attributions:
        parts.append(f"{len(run.attributions)} are statement(s) "
                     f"{MISATTRIBUTED_WORDS}, listed under `## Attributions`")
    parts.append(f"{len(run.number_faults)} are value(s) {NUMBER_CHANGED_WORDS}, "
                 f"listed under `## Number format`")
    total = len(run.structural) + len(run.attributions) + len(run.number_faults)
    joined = parts[0] if len(parts) == 1 else (
        ", ".join(parts[:-1]) + ", and " + parts[-1])
    return (f"None in the claims. Of the {total} finding(s) this run reports, "
            f"{joined} below.")


def _convention_row(run: Run, convention: numerals.Convention) -> str:
    points = ", ".join(convention.point_votes) or "none"
    commas = ", ".join(convention.comma_votes) or "none"
    decided = numerals.NAMES.get(convention.convention, "none")
    language = {"en": "English", "de": "German"}.get(convention.language, "unknown")
    return (f"| `{run.display(convention.document)}` | {decided} | "
            f"{convention.decided_by} | {points} | {commas} | {language} "
            f"({convention.english_words} / {convention.german_words}) |")


def number_format_section(run: Run) -> str:
    """Each document's convention and every numeral flagged, or `` (601).

    Printed on either command and only when something was flagged, so every
    report without one reads as before. The faults first, then the warnings,
    each naming the numeral, its document and line, and both readings.
    """
    if not run.number_format:
        return ""
    lines = ["## Number format", "", NUMBER_FORMAT_NOTE, "",
             "| document | convention | decided by | votes, decimal point | "
             "votes, decimal comma | language (stop words en / de) |",
             "|---|---|---|---|---|---|"]
    lines += [_convention_row(run, convention) for convention in run.conventions]
    for heading, rows in (("Faults", run.number_faults),
                          ("Warnings", run.number_warnings)):
        if not rows:
            continue
        lines += ["", f"### {heading}", ""]
        for finding in rows:
            lines.append(f"- **{_NUMBER_KIND_WORDS[finding.kind]}** "
                         f"`{finding.segment}` "
                         f"(`{run.display(finding.document)}`) - {finding.detail}")
            if finding.merge_text:
                block = evidence_lines(finding)
                if block:
                    lines += [""] + ["  " + line for line in block]
    return "\n".join(lines) + "\n"

def capping_section(run: Run) -> str:
    """Every field a model overran its cap on, capped rather than rejected.

    Its own section and not a row in Structure or Findings, because it is
    neither of those measurements: nothing here compares the merge against a
    source text or a verdict against a claim, it reports what `parsing.parse`
    had to shorten before either of those checks ever ran. Nothing here moves
    `exit_code` (Pass B, `DECISIONS.md` entry 190) — nothing here is even
    checkable against the source texts, since the field's content past the cap
    is exactly what this section says was thrown away.
    """
    lines = ["## Length capped", ""]
    if not run.truncations and not run.capped_verdicts:
        lines.append("None.")
        return "\n".join(lines) + "\n"
    for item in run.truncations:
        lines.append(
            f"- `{item.path}` was {item.original_length} characters, over the "
            f"{item.cap}-character cap; capped to fit"
        )
    for verdict in run.capped_verdicts:
        lines.append(
            f"- `{verdict.claim_id}` rationale ({verdict.direction}) ran to the "
            f"{parsing.RATIONALE_MAX}-character cap and was cut off"
        )
    return "\n".join(lines) + "\n"


def unusable_section(run: Run) -> str:
    """Claims the tool refused to grade. Pass C, `DECISIONS.md` entry 194.

    Its own section and above the inventory, because it is the one thing in
    the report a reader must not miss: every table below counts the claims
    that were graded, and this is the list of the ones that are not in any of
    them. A count that silently shrank its own denominator is the failure the
    whole file's opening paragraph is about, and Pass C would introduce
    exactly that failure without this section.

    The defect text is the checker's own words, verbatim and unabridged --
    the same sentences the model was sent on each repair attempt. Summarising
    them here would put the tool's paraphrase of a fault where the fault
    itself belongs, and the reader's question is what was actually wrong.
    """
    lines = ["## Not graded", ""]
    if not run.unusable:
        lines.append("None. Every claim submitted came back with a usable verdict.")
        return "\n".join(lines) + "\n"
    lines.append(
        f"**{len(run.unusable)}** record(s) could not be graded and were dropped. "
        f"The model was asked again for each and did not produce a usable answer; "
        f"the rest of the batch was graded and stands. These claims have no "
        f"verdict, in either direction, and the run is inconclusive because of it."
    )
    lines.append("")
    for item in run.unusable:
        named = f"`{item.claim_id}`" if item.claim_id else "_no claim id_"
        lines.append(f"- {named} ({item.direction}, record {item.index}):")
        for defect in item.defects:
            lines.append(f"  - {defect}")
    return "\n".join(lines) + "\n"


def order_line(run: Run) -> str:
    """How the merge laid its sources out. A measurement, not a verdict.

    Printed inside Structure and phrased so that it cannot be read as a finding:
    no bold, no heading, and the sentence states what the sequence was rather
    than what it means. The denominator travels with it for the reason
    `as_dict` gives -- `stapled` over 3 attributed segments and over 39 are the
    same boolean and different evidence.

    A concatenation is not always wrong. `tests/fixtures/disjoint_sources` is
    two documents with nothing in common and its correct merge is exactly a
    staple, so this line reports the shape and leaves the judgement to a reader
    who knows whether the sources had anything to interleave.
    """
    order = run.order
    if order is None or not order.attributed:
        return ("Ordering: no merged segment could be attributed to a single "
                "source, so nothing can be said about the layout.")
    shape = ("each source in one unbroken block" if order.stapled
             else "sources interleaved" if order.interleaved
             else "sources in blocks, at least one out of its source order"
             if not order.monotone else "not conclusive on this evidence base")
    return (
        f"Ordering: {order.runs} run(s) over {order.attributed} attributed "
        f"segment(s) — {shape}. {order.headings_present} of "
        f"{order.headings_total} source heading(s) survive. This is a "
        f"measurement, not a finding: whether this shape is right depends on "
        f"whether the sources had anything to interleave, which this tool "
        f"does not measure."
    )


def review_queue_section(run: Run) -> str:
    """Losses the merge owned: everything above this line is what it did not.

    §2.5's split, made visible. Findings are failures; this is work. The two are
    separate sections rather than one list with a column because a reader who
    skims the Findings heading and stops has to be reading only the things that
    went wrong, and a reader who acts on this list is doing something else with
    it — putting facts back, or agreeing they should stay out.

    **Not the page's "what needs your attention" list**, which shares the word
    and is a different feature (545). That list is an index over sections the
    page already renders, and it exists because a page is a set of collapsible
    panels; this is a section with a membership rule. The page's counterpart to
    this one is `Omitted content`, which is wider on purpose -- it lists every
    `dropped` declaration where this takes only the ones the forward pass
    confirmed, because the page shows the grade beside each row and a report
    read months later is better served by one list that means one thing.

    The budget line lives here rather than under Declarations because it is the
    one thing that can make this section a finding. It counts declared `dropped`
    records, including the ones no claim was drawn from, so it can fire over an
    empty queue — which is exactly the run it exists for: a merge that declared
    away half its input and lost nothing a claim was ever extracted from.
    """
    lines = ["## Review queue", ""]
    if run.queued:
        # Not `queue_sentence`, which says "below" and is the verdict line's
        # pointer at this section. Repeating it here would be the report telling
        # a reader who is already looking at the list to go and look at the list.
        lines += [
            f"**{len(run.queued)}** claim(s) the merge declared dropped and the "
            f"forward pass confirms are gone. Each is a decision to review — put "
            f"the fact back, or agree it stays out — and none of them is counted "
            f"as a finding above.",
            "",
        ]
        by_id = {claim.id: claim for claims in run.claims.values() for claim in claims}
        # Which record owns which claim, so each entry can name the segment it
        # was declared under and quote the merge's own reason for it. `queued`
        # is built from `accounted_for`, which is built from these same lists,
        # so every queued claim has exactly one owner here.
        owner = {
            claim_id: item
            for item in run.declarations
            if item.disposition == "dropped" and item.grade == CONFIRMED
            for claim_id in item.claims
        }
        for verdict in run.queued:
            claim = by_id.get(verdict.claim_id)
            where = (
                f"`{run.display(claim.source)}:{claim.line}`" if claim else "unknown line"
            )
            text = claim.text if claim else verdict.claim_id
            item = owner.get(verdict.claim_id)
            # Three lines, and they answer three different questions in the
            # order a reader asks them: what is missing, why the merge says it
            # is missing, and whether anything checked. The middle line is the
            # merge's own words and is not graded here -- it is the argument
            # the reader is being asked to accept or overturn. The last line is
            # the tool's, and it is what makes the middle line safe to print.
            lines.append(f"- **{verdict.claim_id}** ({where}) — {text}")
            lines.append(
                f"  - left out of: `{item.segment}`" if item and item.segment
                else "  - left out of: a segment the record did not name"
            )
            lines.append(
                f"  - the merge's reason: {item.reason}" if item and item.reason
                else "  - the merge's reason: none was recorded"
            )
            lines.append(
                f"  - confirmed absent: the forward pass looked for this claim "
                f"in `{run.display(MERGED)}` and did not find it"
                + (f" -- {verdict.rationale}" if verdict.rationale else "")
            )
    else:
        lines.append(
            "None. Every claim the forward pass found missing is a finding above, "
            "and no declared drop accounts for one."
        )
    if run.over_budget:
        lines += ["", f"> **Over budget.** {budget_sentence(run)}"]
    return "\n".join(lines) + "\n"


def declarations_section(run: Run) -> str:
    """What the merge said it did, and whether the forward pass agrees.

    Separate from Findings, and below it, for the reason §2.5 gives: a rejected
    declaration is the merge describing itself wrongly, which is not the same
    thing as a dropped fact and must not be counted as one. It changes no
    verdict above. It reaches the exit code in exactly two ways, both task 27's:
    a confirmed `dropped` moves a claim out of Findings and into the review
    queue, and the count of declared drops against §2.6's budget can fail the
    run on its own. Nothing else here is scored.

    The empty case is printed rather than omitted, because under §2.1 silence is
    itself the claim: a merge that declared nothing has said every source
    segment survives character for character, and that is a strong statement to
    leave off the page.
    """
    lines = ["## Declarations", ""]
    # Before the counts, and on the empty path too: at a ceiling of 100% §2.6
    # cannot fire, so `over_budget: false` further down means "not asked"
    # rather than "asked and passed". A disabled check that reads as a passed
    # check is this project's most-repeated failure class, so it is stated
    # rather than left to be inferred from the provenance block.
    if run.budget_disables_check:
        lines += [
            "> **Declared-loss budget disabled.** The ceiling for this run was "
            "100% of the source segments, at which the §2.6 check cannot fire. "
            "The declared loss below was recorded, not judged.",
            "",
        ]
    if not run.declarations:
        lines.append(
            "The merge declared no departures from its sources, which under the "
            "disposition model is itself a claim: every source segment is asserted "
            "to survive into the merge character for character."
        )
        return "\n".join(lines) + "\n"

    counts = {
        grade: len([d for d in run.declarations if d.grade == grade])
        for grade in (CONFIRMED, REJECTED)
    }
    unchecked = len(run.declarations) - counts[CONFIRMED] - counts[REJECTED]
    lines += [
        f"The merge declared **{len(run.declarations)}** departure(s) from its "
        f"sources. Checking them confirms {counts[CONFIRMED]}, rejects "
        f"{counts[REJECTED]}, and leaves {unchecked} unchecked — a declaration is "
        f"unchecked when no claim was drawn from the segment it names *and* the "
        f"reconciler's location of that text settles nothing about what was "
        f"declared, and that is not agreement.",
        "",
        # Achieved beside configured, on every run and not only the failing
        # one (488). `budget_sentence` says this when the ceiling is crossed,
        # which is the case a reader least needs telling -- the run already
        # failed and named the reason. The clean run is where the report used
        # to say nothing at all about how close the merge came.
        f"Declared loss: {loss_row(run)}.",
        "",
        # Two columns for two voices. `The merge's reason` is what the merger
        # wrote and nothing in this tool checks it; `On what evidence` is how
        # the grade beside it was reached. One column holding both would let a
        # merge's own argument be read as the tool agreeing with it.
        "| Segment | Declared | The merge's reason | Confirmed? | On what evidence |",
        "|---|---|---|---|---|",
    ]
    for item in run.declarations:
        claims = ", ".join(f"`{c}`" for c in item.claims) or "no claim traced to it"
        lines.append(
            f"| `{item.segment}` | {item.disposition} | "
            f"{cell(item.reason) or '*none recorded*'} | **{item.grade}** | "
            f"{cell(item.detail)} ({claims}) |"
        )
    return "\n".join(lines) + "\n"


def additions_section(run: Run) -> str:
    """Every statement the merge brought from outside the documents.

    Its own section rather than a row in Findings, for the reason declarations
    have one: a declared addition is not a defect and listing it among defects
    would say it was. It is also not a *finding the tool made* -- the tool
    found nothing here, it was told. The section exists so the reader can do
    the one thing the tool cannot, which is decide whether each statement is
    true.

    Columns, and none of them is a grade. `The merge's reason` is what the
    merger wrote and nothing checks it; `Corrects` is what it says it is fixing
    and may be empty, because a merge that extends the documents corrects
    nothing and forcing it to name a victim would make it invent one.

    `Basis` and `Source` are the merge's account of what it went on (537), and
    they are rendered flat -- `Source` is never a link. A link is an invitation
    that reads as a check somebody has already made, and nothing here has
    checked it. `sourcing_sentence` says so above the table, in the section
    that lists them, so a reader weighing a citation meets the caveat before
    the citation rather than after it.

    `own-knowledge` rows are the ordinary case and are shown as plainly as the
    cited ones. A table that made the empty column look like an omission would
    push the next merge into filling it.
    """
    if not run.additions:
        return ""
    lines = [
        "## Added from outside the documents",
        "",
        f"The merge declared {len(run.additions)} statement(s) that your "
        f"documents do not contain. **Nothing here has been verified against "
        f"them**, because they are the only thing this tool checks against. "
        f"Each is the model's own claim, and reviewing them is the reader's "
        f"job rather than the tool's.",
        "",
        sourcing_sentence(run),
    ]
    corrections = run.corrections
    if corrections:
        # Said here because this is where the reader meets the row that caused
        # it. A correction departs from a source deliberately, every check
        # downstream reads that as a departure, and a reader who declared one
        # and got exit 1 is owed the reason rather than left to infer a bug.
        lines += [
            "",
            f"{len(corrections)} of them correct(s) something a document "
            f"states. A correction is a departure from your documents, so it "
            f"is also reported as a finding and it moves the exit code: "
            f"nothing here can tell a correction from a corruption, and the "
            f"declaration buys you this row rather than a clean run.",
        ]
    lines += [
        "",
        "| Statement | Corrects | Basis | Source | The merge's reason "
        "| Claims it covers |",
        "|---|---|---|---|---|---|",
    ]
    for record in run.additions:
        statement = cell(str(record.get("statement", "")))
        covers = run.covering(str(record.get("statement", "")))
        basis = cell(basis_word(str(record.get("basis", ""))))
        lines.append(
            f"| {statement or '*nothing recorded*'} | "
            f"{cell(str(record.get('corrects', ''))) or '*nothing named*'} | "
            f"{basis or '*none recorded*'} | "
            f"{cell(str(record.get('source', ''))) or '*no source*'} | "
            f"{cell(str(record.get('reason', ''))) or '*none recorded*'} | "
            f"{', '.join(covers) or '*none*'} |"
        )
    return "\n".join(lines) + "\n"


def dry_run_section(run: Run) -> str:
    """What --dry-run can honestly say, which is less than a total.

    The calls after the first decompose depend on how many claims come back,
    and the only way to learn that is to make the call. Printing an estimate
    would be the report inventing a number, so the plan states what it counted
    and names what it could not.
    """
    lines = ["## Planned calls", ""]
    for step in run.steps:
        if step.state == PLANNED:
            lines.append(f"- {step.name}")
    counted = len(run.planned)
    lines += [
        "",
        f"**{counted} call(s) planned, none made.** The rest of the run cannot be "
        f"counted from here: one verify call covers {run.verify_batch} claims, "
        f"and how many claims these documents hold is what the decompose calls "
        f"above were going to find out.",
    ]
    return "\n".join(lines) + "\n"


def render(run: Run) -> str:
    """The whole report, in the order the README specifies."""
    if run.planned:
        parts = [dry_run_section(run)]
        if run.provenance is not None:
            parts.append(run.provenance.as_markdown())
        return "\n".join(parts)

    # Exceptions first, then the whole inventory. A reader who stops after the
    # first screen has to have read what went wrong; a reader who came to find
    # out what happened to one particular fact reads on to the tables.
    parts = [verdict_section(run), coverage_section(run), findings_section(run)]
    # Beside the model's findings and above everything that is not a finding,
    # on either command. Empty unless the merge misattributed something (569).
    if run.attributions:
        parts.append(attributions_section(run))
    # Beside it, for the same reasons, and only where something was flagged.
    if run.number_format:
        parts.append(number_format_section(run))
    parts += [capping_section(run), unusable_section(run), inventory_section(run)]
    # Only where a merge actually produced a document. On `verify` the sources
    # were merged by something else, which declared nothing to this tool, and a
    # section reporting no declarations would read as a merge that made none.
    if run.command == "merge" and run.merged is not None:
        parts += [
            structural_section(run),
            review_queue_section(run),
            declarations_section(run),
            additions_section(run),
        ]
    if run.provenance is not None:
        parts.append(run.provenance.as_markdown())
    if run.merged is not None and run.merged_written_to is None:
        parts.append(f"## Merged document\n\n{_fenced(run.merged.rstrip())}\n")
    return "\n".join(parts)


BACKTICK_RUN = re.compile(r"`+")


def _fenced(text: str) -> str:
    """`text` inside a fence no run of backticks in it can close early.

    Unfenced, this was `run.merged` pasted straight under a `##` heading: a
    merged document that itself contained a `#`-heading -- a level a source
    document is licensed to use -- became a heading in *this* report, splitting
    the section a reader was told to expect into several, and one that opened
    with three backticks closed the fence early and read the rest of the
    report as the code block's contents. Three backticks is the default and
    right for ordinary prose; the fence only grows past that for a merged
    document that itself quotes a longer run, which is the case this function
    exists for.
    """
    longest = max((len(run) for run in BACKTICK_RUN.findall(text)), default=0)
    fence = "`" * max(longest + 1, 3)
    return f"{fence}markdown\n{text}\n{fence}"


def as_dict(run: Run) -> dict:
    """The same report, for a machine. Same fields, nothing summarised away."""
    graded = [v for v in run.verdicts if v.grounding != NOT_GRADED]
    return {
        "command": run.command,
        "exit_code": exit_code(run),
        "documents": dict(sorted(run.paths.items())),
        "steps": [{"name": s.name, "state": s.state, "detail": s.detail} for s in run.steps],
        "coverage": {
            "extracted": {name: len(claims) for name, claims in sorted(run.claims.items())},
            "forward_submitted": run.submitted("forward"),
            "forward_verdicts": len(run.forward),
            "forward_partial": len(
                [v for v in run.forward if v.finding == "partially_dropped"]
            ),
            # Per source, with its own denominator, for the reason the markdown
            # rows give. Always present and always keyed by every source, so a
            # consumer reading a source's coverage as 0 is reading a measurement
            # rather than an absent key.
            "forward_by_source": dict(sorted(run.forward_by_source().items())),
            "reverse_submitted": run.submitted("reverse"),
            "reverse_verdicts": len(run.reverse),
            "reverse_partial": len(
                [v for v in run.reverse if v.finding == "partially_invented"]
            ),
            "graded": len(graded),
            "grounded": len([v for v in graded if v.grounding == GROUNDED]),
            "errored": len(run.errored),
            # The claims that went in and did not come back. Inside `coverage`
            # rather than beside it because that is where the denominators
            # live: `forward_submitted` minus `forward_verdicts` is this
            # number, and a consumer that reads the two without it would see a
            # gap with no name. Pass C, `DECISIONS.md` entry 194.
            "ungraded": len(run.unusable),
        },
        "claims": [claim.as_dict() for claims in run.claims.values() for claim in claims],
        "verdicts": [verdict.as_dict() for verdict in run.verdicts],
        "findings": [verdict.as_dict() for verdict in run.findings],
        # Disjoint from `findings` by construction, and both are subsets of
        # `verdicts` — a consumer that wants every dropped claim regardless of
        # who owned it reads `verdicts`, not the sum of these two, because
        # summing them is the arithmetic §2.5 exists to stop being implicit.
        "review_queue": [verdict.as_dict() for verdict in run.queued],
        "declarations": [item.as_dict() for item in run.declarations],
        # Carried whole and ungraded. A reader's tooling needs the same three
        # fields the merge wrote, and a `graded` key here would imply something
        # graded them.
        "additions": [dict(record) for record in run.additions],
        # The merge's warning about its inputs, verbatim and ungraded (497).
        # Empty string rather than null for an ordinary run, so a consumer
        # tests one thing rather than two.
        "mismatch": run.mismatch,
        # Which claims each declaration excused, in the same order as
        # `additions`. Beside the records rather than inside them: those three
        # fields are the merge's own words, and this is the tool's account of
        # what they bought, which is a different kind of thing and belongs
        # under a different key. A consumer wanting the flat set unions these;
        # one wanting to know whether a single declaration covered a dozen
        # claims reads the rows, which is the question a bare count hides.
        "additions_cover": [list(run.covering(str(record.get("statement", ""))))
                            for record in run.additions],
        # What this tool did about the sources those records cite, and what
        # the model did while producing them (537). Two facts and both
        # published, because either alone misleads: `resolved` is constant and
        # false, because nothing here opens a socket; `state` is a measurement
        # off `server_tool_use` and has three values, of which `unmeasured` is
        # not `not-searched`.
        "sourcing": {
            "resolved": False,
            "fetched": False,
            **(run.searches.as_dict() if run.searches is not None
               else {"state": "unmeasured", "measured_calls": 0,
                     "unmeasured_calls": 0}),
            # The second instrument, under a key of its own (548). Not merged
            # into `state` above and not allowed to overwrite it: that one
            # counts web requests off `server_tool_use` and this one counts
            # turns off `num_turns`, they disagree on a command backend by
            # construction, and a consumer has to be able to see which reading
            # came from which. `retrieval_permitted` is the third fact and the
            # one neither counter carries -- whether the run was granted a
            # tool at all, which is what separates "did not look" from "could
            # not".
            #
            # At `sourced` this is the tally the level is judged on, the merge
            # role's on a merge (665), so `retrieval` below and the counts a
            # page prints beside it come from one set of calls.
            # `provenance.retrieval.tool_use` keeps the run-wide account.
            "tool_use": (_judged_tool_use(run) if _judged_tool_use(run) is not None
                         else {"state": "unmeasured", "retrieval": "unmeasured",
                               "turns": 0, "calls_with_tool_use": 0,
                               "measured_calls": 0, "unmeasured_calls": 0}),
            "retrieval_judged_on": ("merge" if retrieval_calls_word(run)
                                    == "merge call(s)" else "all"),
            "retrieval_permitted": list(config.granted_web_tools(
                getattr(getattr(run.provenance, "settings", None), "command", "")
                or "")),
            # The one reading a consumer must not have to derive: this run was
            # made at a level that expects the model to retrieve, and it
            # retrieved nothing -- so every source it cites is a recollection.
            # A boolean rather than a level name, so the page that renders it
            # needs no fidelity vocabulary and a seventh level would not
            # silently stop it firing.
            "recall_only": recall_only(run),
            # What the level that promised retrieval achieved, in three words
            # (568): `retrieved`, `not-retrieved` or `unmeasured`, and `` below
            # `sourced`, where nothing was promised. Beside `recall_only`, which
            # is the second of the three as a boolean and stays for the page
            # that already reads it.
            "retrieval": retrieval_outcome(run),
            # Whether this run's exit 2 is `sourced_not_delivered` and nothing
            # else (665): the run finished and looked nothing up. A boolean for
            # the page, which picks its own inconclusive sentence by it rather
            # than the one for a run whose work did not complete.
            "inconclusive_not_sourced": inconclusive_for_retrieval_alone(run),
        },
        # `ran` first and always, because `findings: []` answers two different
        # questions and a consumer reading only the list cannot tell which one
        # it got. `checks` and `segments` are the denominator; without them an
        # empty list is a claim with nothing behind it.
        "structural": {
            "ran": run.reconciled is not None,
            "checks": CHECKS,
            "segments": run.reconciled.segments if run.reconciled is not None else 0,
            # `reconciled.findings` and not `run.structural`: the latter carries
            # the prompt-leak findings too, and they are not one of the `checks`
            # above. They are published in `prompt_leaks` below with their own
            # denominator. A consumer wanting everything the tool found without
            # a model reads both, the way it already reads `findings` and
            # `structural` as two lists.
            "findings": [
                finding.as_dict()
                for finding in ([] if run.reconciled is None
                                else run.reconciled.findings)
            ],
        },
        # The merge held against `merge.md`'s worked example rather than against
        # its sources — `merge.EXAMPLE_MARKERS`, the words that mean the model
        # returned the illustration instead of the documents. `ran` first for
        # the same reason `structural` has it: an empty list means "checked,
        # clean" on a merge and "no merge to check" on a verify, and a consumer
        # reading only the list cannot tell those apart. Moves `exit_code` to 1,
        # via `Run.structural`.
        # `not_checked` rides beside the findings for the reason `markers`
        # does: a reader of an empty list is owed what was looked for, and
        # after 370 they are owed what was not. Both halves are exact-string,
        # so a model that follows the example's shape in its own words is
        # outside them, and that is the common case rather than the exotic one
        # -- on the run that produced 370 it was seven reasons of eight.
        # Published rather than left in a docstring, because the person who
        # needs it is reading a green result and not the source.
        # Model-authored and ungraded, and labelled so in the block itself.
        # `report.py`'s two-voice rule applies: this is the merger's account of
        # what it chose between, and nothing here checks that the conflict is
        # real. A consumer reading `resolved: false` is reading the merge's
        # claim that two values disagreed, not the tool's agreement that they do.
        "decisions": {
            "ran": run.merged is not None,
            "authored_by": "the merge",
            "graded": False,
            "note": (
                "what the merge says it chose between. At off, low and mid the "
                "merge may not choose, so a record with no chosen value is the "
                "only place a disagreement is written down: the merged document "
                "may not carry a marker and the reconciler cannot derive one. "
                "Nothing here checks that the conflict is real"
            ),
            "records": [
                {
                    "slot": str(d.get("slot", "")),
                    "candidates": list(d.get("candidates") or ()),
                    "chosen": str(d.get("chosen", "")),
                    "resolved": bool(str(d.get("chosen", "")).strip()),
                    "reason": str(d.get("reason", "")),
                }
                for d in run.decisions
            ],
        },
        # `keep-base` names the base document's title, and a plain-text source
        # whose first line runs into the body has no title segment for it to
        # name. That is a fact about the input, not a defect in the merge, so
        # it is reported beside the policy rather than as a finding (386).
        "title": {
            "policy": run.title_policy,
            "sources_with_a_title": run.sources_with_a_title,
            "has_referent": run.sources_with_a_title > 0,
            "note": (
                "no source document has a title segment, so the title policy "
                "has nothing to name. A first line that runs straight into the "
                "body is not read as a title; this is a property of the input"
                if run.sources_with_a_title == 0 and run.merged is not None else ""
            ),
        },
        # Reported, not judged (391). See `Run.added_breaks`.
        "structure": {
            "breaks_added_by_the_merge": len(run.added_breaks),
            "between": [list(pair) for pair in run.added_breaks],
            "graded": False,
            "note": (
                "a line break inside a merged segment that no source segment "
                "carries. Permitted at every level, so this is a description "
                "of the merge and not a finding against it"
            ),
        },
        "prompt_leaks": {
            "ran": run.merged is not None,
            "markers": list(merge.EXAMPLE_MARKERS),
            "reason_clauses": len(merge.example_reason_clauses()),
            "not_checked": (
                "a record that follows the worked example's shape in its own "
                "words rather than repeating it: both halves are exact-string, "
                "so a slot-filled template is outside them. On the run this "
                "was written for, one reason of eight was verbatim and seven "
                "were not"
            ),
            "findings": [finding.as_dict() for finding in run.leaks],
        },
        # A statement credited to a source that does not carry it (569). Its own
        # block for `restated_claims`' reason: not one of the nine `checks`,
        # and `ran` first so an empty list is "checked, clean" only where a
        # merged document existed to check. Runs on `verify` as well.
        "attributions": {
            "ran": run.attributions_checked,
            "predicate": (
                "a merged sentence of the shape 'according to NAME, CONTENT' or "
                "'NAME states that CONTENT', not in any source as written, whose "
                "NAME is the title, a separated part of the title or the "
                "filename of exactly one source, and whose CONTENT is in another "
                "source and not in that one"
            ),
            "findings": [finding.as_dict() for finding in run.attributions],
        },
        # The number format (601). `ran` first for the reason every block here
        # has it. `faults` names the kinds that moved the exit code, so a
        # consumer does not have to know which of four kinds are warnings;
        # `documents` is each document's convention and the evidence for it.
        "number_format": {
            "ran": run.number_format_checked,
            "predicate": numerals.PREDICATE,
            "faults": sorted(numerals.FAULTS),
            "findings": [finding.as_dict() for finding in run.number_format],
            "documents": [convention.as_dict() for convention in run.conventions],
        },
        # Check 9's claim-level half. `ran` first for the reason `structural`
        # and `prompt_leaks` have it: an empty `findings` means "checked, found
        # nothing" on a merge that was decomposed and "not checked" on a verify
        # run or a merge whose decompose failed, and a consumer reading only
        # the list cannot tell those apart.
        #
        # `claims` and `source_claims` are the arithmetic that makes a firing
        # legible -- a merge that extracts more claims than both its sources
        # together has probably stated something twice. They are published
        # beside the findings and are not part of the predicate: entry 400
        # measured `decompose` returning 18 claims on one run and 22 on the
        # next for an identical request at temperature 0, so the comparison is
        # a sample and a check resting on it would fire and miss at random.
        "restated_claims": {
            "ran": bool(run.command == "merge" and MERGED in run.claims),
            "claims": len(run.claims.get(MERGED, [])),
            "source_claims": sum(
                len(claims) for name, claims in run.claims.items() if name != MERGED
            ),
            "predicate": (
                "one claim text extracted from two different lines of the merged "
                "document, both copies anchored to a span found in it. Same-line "
                "repeats are decomposer noise and are not counted; near matches "
                "are not counted either, because no similarity threshold "
                "separates a restated merge from a correct one in this corpus"
            ),
            "counts_are_evidence_not_the_test": True,
            "findings": [finding.as_dict() for finding in run.restated],
        },
        "declared_loss": {
            "drops": run.declared_drops,
            "segments": run.segments,
            "budget": run.declared_loss_budget,
            # What the merge actually did, beside what was asked of it. Both
            # numbers were already here and the reader had to divide; a
            # configured ceiling with no achieved figure next to it tells
            # nobody whether the run was close to it or nowhere near (488).
            #
            # `None` when there are no segments, never 0.0. No segments is a
            # ratio that does not exist, and zero would read as a merge that
            # dropped nothing out of something.
            "ratio": (run.declared_drops / run.segments
                      if run.segments else None),
            # So a stored record can be told apart from one that passed. False
            # here plus `over_budget: false` is a merge inside its ceiling;
            # true plus false is a ceiling that could not be exceeded.
            "check_disabled": run.budget_disables_check,
            "over_budget": run.over_budget,
        },
        # Claims submitted whose record was refused. Always present, so an
        # empty list is a measurement rather than an older schema. Unlike
        # `truncations` directly below, this *does* move `exit_code`, to 2.
        "unusable": [
            {
                "claim_id": item.claim_id,
                "direction": item.direction,
                "index": item.index,
                "defects": list(item.defects),
            }
            for item in run.unusable
        ],
        # Merge-side (`reason`, `replacement`) truncations. Verify-side
        # (`rationale`) ones are already in `verdicts`/`findings` as
        # `rationale_capped`, not duplicated here. Never moves `exit_code`.
        "truncations": [
            {"path": t.path, "original_length": t.original_length, "cap": t.cap}
            for t in run.truncations
        ],
        # A measurement, deliberately outside `structural`. Everything in that
        # block is a verdict the exit code is computed from; nothing here is.
        # Kept whole rather than reduced to `stapled`, because the boolean is
        # the least useful part: 2 runs over 39 attributed segments and 2 over
        # 3 are the same boolean and not the same observation, and a reader
        # cannot see the difference without the denominator.
        "order": None if run.order is None else {
            "sequence": "".join(run.order.sequence),
            "runs": run.order.runs,
            "attributed": run.order.attributed,
            "interleaved": run.order.interleaved,
            "monotone": run.order.monotone,
            "conclusive": run.order.conclusive,
            "blocked": run.order.blocked,
            "stapled": run.order.stapled,
            "headings_present": run.order.headings_present,
            "headings_total": run.order.headings_total,
        },
        "merged_written_to": run.merged_written_to,
        "provenance": run.provenance.as_dict() if run.provenance else None,
    }
