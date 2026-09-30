"""Pass 1 — combine several source documents into one that carries every fact.

The least important of the three passes, and the one the rest of the tool
exists to check. Nothing here decides anything: the merge is asked to surface
disagreements rather than resolve them, and whether it did is a question for
verify, not for this module. There is no conflict detection here and no
refusal — a merge this pass produced is evidence, not a verdict.

Sources by name and not by accident, and now two or more of them. `merge.md` has
always been written for N documents and takes a rendered `{sources}` list, and
`segment.render_sources` has always emitted one `<document>` block per document,
so the prompt was never the gate. This module was, and that changed: a
mapping is checked against canonical names derived from its own length instead
of against a pair. The names stay this module's rather than the operator's
filenames, because a disposition record points at a document by the name it was
shown and the same pair merged from two directories must render one prompt.

Two remains the only number that has been *tested*. Every fixture is a pair, the
whole recorded corpus is pairs, and the conflict rule the prompt states — "state
both values and name the document each came from" — is written for two; three
sources can disagree three ways and no sentence in `merge.md` covers that. What
N buys is the plumbing: naming, ordering, the reconciler's denominators, and a
`max_tokens` that counts candidate slots per document rather than charging two.
What it does not buy is evidence that a model merges five documents well, and no
figure in this repository claims it.

What the model is shown is segmented, not raw. Every line carries a segment id,
and silence about a segment is a claim that it survived character for character
— which is what lets the reconciler check the merge by set membership and string
containment instead of by asking a second model. The merge prompt and the
coverage checker must consume one segmentation or they compare two different
denominators, so both go through `segment.segment_sources`.

The document comes back inside a JSON string rather than as plain text. That
costs some escaping and buys three things: the tier ladder, the cassette key,
the repair loop and the replay path all already assume a schema, so no new path
through `client.py` is needed; and truncation becomes self-detecting. A
document cut off at `max_tokens` is an unterminated JSON string, which fails
`parsing.extract_json`, fails the repair attempt, and errors the unit of work.
Returned as plain text it would arrive as a merge that simply stops, and every
fact after the cut would be reported as dropped by the merge model rather than
by the budget.
"""

from __future__ import annotations

import itertools
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass

from . import (config, decompose, parsing, prompts, reconcile, segment,
               structured, window)
from .client import Client


@dataclass(frozen=True)
class MergePolicy:
    """What the merge is *allowed* to do, separated from where it runs.

    A small object rather than passing `Settings` around, because the two things
    that consume this consume nothing else from the runtime configuration. The
    merge call needs it to choose a prompt fragment; the reconciler needs it to
    decide which dispositions are permitted, and a reconciler that took
    `Settings` would be a pure function holding an endpoint, a model map and an
    API key variable name it can never use.

    It is also the thing a report has to print. A coverage figure means something
    different at `off` than at `high` — at `off` a rewording is a defect and at
    `high` it is the requested behaviour — so a number published without the
    level beside it is not interpretable, in the same way one published without
    its model is not.
    """

    fidelity: str = config.DEFAULT_FIDELITY
    title_policy: str = config.DEFAULT_TITLE_POLICY
    declared_loss_budget: float = config.DEFAULT_DECLARED_LOSS_BUDGET

    def __post_init__(self) -> None:
        # The alias is resolved here as well as in `config.settings_for`,
        # because this object is built directly by tests, bench runners and
        # anything that never touched an argument parser -- and a policy
        # holding `verbatim` would reach the prompt loader as a filename that
        # does not exist. Written back onto the frozen instance so there is one
        # spelling from here on; `config.fidelity_name` is the way back.
        object.__setattr__(self, "fidelity", config.canonical_fidelity(self.fidelity))
        if self.fidelity not in config.FIDELITY_LEVELS:
            raise config.ConfigError(
                f"fidelity {self.fidelity!r} is not one of "
                f"{', '.join(config.FIDELITY_CHOICES)}"
            )
        if self.title_policy not in config.TITLE_POLICIES:
            raise config.ConfigError(
                f"title policy {self.title_policy!r} is not one of "
                f"{', '.join(config.TITLE_POLICIES)}"
            )
        # Bounded here as well as in `from_env`, because this object can be
        # built directly -- by a test, a bench runner, or a caller that never
        # touched the environment -- and an out-of-range ceiling reaching the
        # reconciler would silently decide an exit code. Not a second copy of
        # the declared-loss budget: the rule stays in `reconcile.over_budget`, and this only
        # refuses a value that is not a fraction. `not (0 <= x <= 1)` is the
        # form that also rejects NaN, which fails every comparison it is asked.
        if not 0.0 <= self.declared_loss_budget <= 1.0:
            raise config.ConfigError(
                f"declared loss budget {self.declared_loss_budget!r} is not a "
                f"fraction between 0.0 and 1.0 inclusive"
            )

    @classmethod
    def from_settings(cls, settings: config.Settings) -> MergePolicy:
        return cls(
            fidelity=settings.fidelity,
            title_policy=settings.title_policy,
            declared_loss_budget=settings.declared_loss_budget,
        )

    def fragment(self, role: str = "merge") -> prompts.Prompt:
        """The rules text for this level, for the prompt of the given role.

        One level names three fragments — `merge`, `verify` and `verify_reverse`
        — because the level has to be told to the passes that *grade* the merge
        as well as to the one that writes it. A reverse pass that does not know
        the level reads every legitimate `high` rewrite as invention.

        The mapping from level to filename lives here rather than at each call
        site, so the three roles cannot drift into three spellings of it.
        """
        return prompts.load(f"fidelity/{self.fidelity}.{role}")


@dataclass(frozen=True)
class MergeResult:
    """What one merge call produced: the document, and what the merger declared.

    The three travel together because the declarations are only meaningful
    against the document they describe. A `replacement` is a span of *this*
    merged document, and a disposition is a claim about a segment that this
    merge either carried or did not — so returning the string alone would leave
    the reconciler holding pointers into a document it was handed separately and
    has no way to check it was given the right one.

    `dispositions` covers departures only. A segment with no record is claiming
    it survived character for character, and that claim is checked by set
    difference against the segmentation rather than read off this list.

    `base` and `base_chosen` are here rather than left to the caller because
    this is where the default is applied, and the report has to name the
    document that governed the structure. They come from the arguments and not
    from the payload — the model is told which document is the base and is not
    asked to say which one it was.
    """

    document: str
    decisions: tuple[dict, ...] = ()
    dispositions: tuple[dict, ...] = ()
    # Statements the merge says it brought from outside the documents, at the
    # one level that permits any. Empty at every other level, and empty
    # at `open` for a merge that added nothing -- which is the ordinary case
    # and the one a reader should be able to see at a glance.
    additions: tuple[dict, ...] = ()
    # The merge's warning that the documents may not belong together.
    # Empty on the ordinary run, which is nearly all of them.
    mismatch: str = ""
    base: str = ""
    base_chosen: str = ""
    # A `reason` or `replacement` the model overran its cap on, capped and
    # logged rather than rejected -- `parsing.parse`'s pre-pass, threaded
    # through `client.Completion`. Empty on the ordinary case, a merge that
    # needed no capping.
    truncations: tuple[parsing.Truncation, ...] = ()

    @classmethod
    def from_payload(
        cls, payload: dict, base: str = "", base_chosen: str = "",
        truncations: tuple[parsing.Truncation, ...] = (),
    ) -> MergeResult:
        return cls(
            document=payload["merged_document"],
            decisions=tuple(payload.get("decisions") or ()),
            dispositions=tuple(payload.get("dispositions") or ()),
            additions=tuple(payload.get("additions") or ()),
            mismatch=str(payload.get("mismatch") or "").strip(),
            base=base,
            base_chosen=base_chosen,
            truncations=truncations,
        )

    def added(self) -> tuple[str, ...]:
        """The statements this merge declared it added, in the order declared.

        Blank statements are dropped rather than carried: a record with nothing
        in it declares nothing, and letting one through would excuse a claim by
        matching the empty string against it.
        """
        return tuple(text for record in self.additions
                     if (text := str(record.get("statement", "")).strip()))

    def declared(self) -> set[str]:
        """The segment ids this merge declared a departure for."""
        return {str(record.get("segment", "")).strip()
                for record in self.dispositions
                if str(record.get("segment", "")).strip()}


# The smallest merge that means anything. The names themselves come from
# `segment.source_name`, which owns the letter they carry: a command line hands
# over paths, but the prompt shows names and a disposition record points at a
# document by the name it was shown, so the names have to be the tool's and not
# the operator's — otherwise the same pair merged from two directories renders
# two prompts and fills two cassettes.
MIN_SOURCES = 2

# The largest merge whose segment ids are still unambiguous, derived rather than
# written down. `segment.document_id` emits `[a-z]+`, and two other letters are
# already spoken for: `reconcile.MERGE_LETTER` labels the merge's own segments
# and `decompose.MERGED_LETTER` labels its claims. At thirteen sources the
# thirteenth is `m`, so its segments are `m1, m2...` and its claims `M-001...` —
# the merge's own ids exactly, in every finding detail and every
# `Located.nearest` pointer, with nothing to tell a reader which document a line
# came from. Asked of the letters rather than spelled as 12, because a number
# here would be the second copy of the rule `source_names` warns about; the
# first colliding index *is* the largest safe count, since a merge of `count`
# sources uses indices `0..count - 1`.
MAX_SOURCES = next(
    index for index in itertools.count()
    if segment.document_id(index) == reconcile.MERGE_LETTER
    or segment.document_id(index).upper() == decompose.MERGED_LETTER
)

# How the base was arrived at, for the record. Two words rather than a boolean,
# because this is read by a person in a report header and `base_chosen: false`
# answers a question nobody asked. `DEFAULTED` is the one that has to be
# visible: the default is `names[0]`, which is *alphabetically* first, so with
# no explicit base the document governing the merged structure and — under
# `keep-base` — its title is decided by what the files happened to be called.
# That is defensible when it is recorded and indefensible when it is not.
EXPLICIT = "explicit"
DEFAULTED = "defaulted"


def source_names(count: int) -> tuple[str, ...]:
    """The canonical filenames for `count` sources, in the order the prompt shows them.

    The upper bound is not a policy about how many documents anyone should
    merge -- `budget_tokens` still answers that with a number rather than a
    refusal, and it is the thing that stops a caller merging fifty files. This
    one is narrower: past `MAX_SOURCES` the letters run into the merge's own,
    and the ids in a report stop identifying the document they came from. An
    earlier version of this docstring said there was no upper bound on purpose,
    on the grounds that a second ceiling would drift from `segment.document_id`.
    That reasoning stands and `MAX_SOURCES` honours it by being derived from the
    letters rather than written as a number; what it did not cover is that two
    of those letters were already taken.
    """
    if count < MIN_SOURCES:
        raise MergeError(
            f"merge needs at least {MIN_SOURCES} sources and was given {count}; "
            "one document is not a merge"
        )
    if count > MAX_SOURCES:
        raise MergeError(
            f"merge takes at most {MAX_SOURCES} sources and was given {count}; "
            f"source {MAX_SOURCES + 1} would be called "
            f"{segment.source_name(MAX_SOURCES)!r} and its segment ids would be "
            f"the merged document's own. Merge in stages instead: combine some "
            f"of them first, then merge that result with the rest."
        )
    return tuple(segment.source_name(index) for index in range(count))


# Property order is emission order, and it is load-bearing here for the same
# reason it is in `verify.VERDICT_SCHEMA`: a grammar-constrained model fills the
# fields in the order the schema lists them, so the model names the value before
# it writes the justification for one. `disposition` then `replacement` then
# `reason`; `chosen` then `reason`. With the reason first, the record is
# whatever the argument's last clause happened to be.
_CANDIDATE_ITEM = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "document": {"type": "string"},
    },
    "required": list(parsing.CANDIDATE_FIELDS),
    "additionalProperties": False,
}

# Which levels may choose between two values that cannot both be true. `high`
# chooses and declares; the levels below it keep both statements and may
# not pick a winner, so at those levels a decision record is how a conflict is
# *recorded without being resolved*. That is the only place a disagreement is
# written down at all: the document may not carry a marker and the reconciler
# cannot derive one, because judging two statements incompatible is not a set
# operation.
#
# `open` chooses too, and may additionally carry a value that covers both
# candidates rather than being one of them. That is a wider licence for
# the same record rather than a different authority, so it reads True here for
# the same reason `high` does: the run emits a decision record either way, and
# what changed is what `chosen` is allowed to hold.
# `sourced` reads True for `open`'s reason and adds nothing of its own here.
# What that level changes is where a declared statement came from, not what a
# decision record may hold.
MAY_CHOOSE = {"off": False, "low": False, "mid": False, "high": True,
              "open": True, "sourced": True}

assert set(MAY_CHOOSE) == set(config.FIDELITY_LEVELS)


# Which levels may state something the documents do not. Two levels, and
# it is the whole of what separates `open` from `high` on the axis that
# matters: every level below treats a fact the sources do not carry as an
# invention, and `open` lets the merge own one instead.
#
# A table rather than `fidelity == "open"`, for `parsing.DERIVES`' reason: an
# equality test is how a sixth level joins the ladder without anyone deciding
# whether it may add. `sourced` is that sixth level and it adds, and **the
# record contract it adds under is `open`'s, unchanged.** The expectation
# moves (retrieve rather than recall) and the schema does not, so an undeclared
# factual change is `hallucinated` there exactly as it is here and still moves
# the exit code.
ADDS = {"off": False, "low": False, "mid": False, "high": False, "open": True,
        "sourced": True}

assert set(ADDS) == set(config.FIDELITY_LEVELS)
# Adding implies choosing. A level trusted to bring a fact from outside is
# certainly trusted to pick between two the documents already carry, and the
# reverse reading -- a level that adds but must keep both sides of every
# conflict -- is not a coherent instrument.
assert all(not adds or MAY_CHOOSE[level] for level, adds in ADDS.items())


def decision_item(fidelity: str | None = None) -> dict:
    """The decision record's shape, with `chosen` required only where it can be.

    Built per call rather than held as four constants, for `verdict_schema`'s
    reason: a mutable dict shared between levels is a defect waiting to be
    written. `fidelity=None` means the level was not threaded to this call, and
    then the **strictest** variant applies -- `chosen` required -- so a path
    that forgets to pass the level fails closed rather than silently accepting
    a record the level would have forbidden.
    """
    may_choose = None if fidelity is None else MAY_CHOOSE[fidelity]
    required = list(parsing.decision_fields(may_choose))
    # `properties` is filtered to `required`, not carried whole. A
    # property that is absent from `required` is exactly what OpenAI's strict
    # `json_schema` mode refuses, and the refusal is silent: the tier ladder
    # reads it as "this endpoint cannot do json_schema", steps down to
    # `prompt`, and the run finishes at the weakest rung having been told
    # nothing. Every `off`, `low` and `mid` run against that vendor did this,
    # while `high` -- whose four fields are all required -- got `json_schema`.
    # Six runs in `toby-test-9`, six matches, no exceptions.
    #
    # Dropping the key rather than requiring it empty is the same answer
    # `merge_schema` gives for `additions` directly below: a model at a level
    # that forbids choosing is not handed a field it must never fill.
    return {
        "type": "object",
        "properties": {name: shape
                       for name, shape in _DECISION_ITEM["properties"].items()
                       if name in required},
        "required": required,
        "additionalProperties": False,
    }


def merge_schema(fidelity: str | None = None) -> dict:
    """`MERGE_SCHEMA` with the decision item this level is allowed to emit."""
    schema = {k: v for k, v in MERGE_SCHEMA.items() if k != "properties"}
    schema["properties"] = dict(MERGE_SCHEMA["properties"])
    schema["properties"]["decisions"] = {
        "type": "array", "items": decision_item(fidelity)}
    # `additions` exists only where the level permits one, and `required`
    # grows with it. The key is absent from the schema at every other level,
    # so a model there is not holding a field it must never fill -- the same
    # argument `parsing.DERIVED` makes for keeping the label out of the lower
    # levels' verdict enum, and it has the same consequence: those levels'
    # schemas, and their cassette keys, are the ones they had before this
    # existed.
    if fidelity is not None and ADDS[fidelity]:
        schema["properties"]["additions"] = {
            "type": "array", "items": addition_item()}
        schema["required"] = list(schema["required"]) + ["additions"]
    return schema


def addition_item() -> dict:
    """One declared addition's shape. See `parsing.ADDITION_FIELDS`.

    `basis` is an enum rather than a free string, and that is the single most
    load-bearing decision in this record. A grammar-constrained model
    cannot write anything but one of the two members, so "my own knowledge, no
    source" is a token it can emit rather than a sentence it has to compose
    under a field that looks like it wants a URL. The field that makes "no
    source" feel like a failure is the field that manufactures fake sources.

    `source` is required, like every other property here, because a property
    outside `required` costs the whole `json_schema` tier on a strict vendor
    and the ladder degrades in silence. Required and *empty* is the
    answer under `own-knowledge`, and `parsing._check_basis` is what enforces
    the dependency the schema cannot express -- the same division of labour
    `replacement` and `dropped` already have one record type up.

    This whole item exists only at `open`: `merge_schema` adds `additions` to
    `properties` at that level and nowhere else, so no level below is handed
    these two new fields either.
    """
    return {
        "type": "object",
        "properties": {
            "statement": {"type": "string",
                          "maxLength": parsing.REPLACEMENT_MAX},
            "corrects": {"type": "string",
                         "maxLength": parsing.REPLACEMENT_MAX},
            "basis": {"type": "string", "enum": list(parsing.BASES)},
            "source": {"type": "string", "maxLength": parsing.SOURCE_MAX},
            "reason": {"type": "string", "maxLength": parsing.REASON_MAX},
        },
        "required": list(parsing.ADDITION_FIELDS),
        "additionalProperties": False,
    }


_DECISION_ITEM = {
    "type": "object",
    "properties": {
        "slot": {"type": "string"},
        "candidates": {"type": "array", "items": _CANDIDATE_ITEM},
        "chosen": {"type": "string"},
        "reason": {"type": "string", "maxLength": parsing.REASON_MAX},
    },
    "required": list(parsing.DECISION_FIELDS),
    "additionalProperties": False,
}

_DISPOSITION_ITEM = {
    "type": "object",
    "properties": {
        "segment": {"type": "string"},
        "disposition": {"type": "string", "enum": list(parsing.DISPOSITIONS)},
        # A string, not nullable: `dropped` gives "" rather than null, so the
        # field is always the same type and "empty" is one condition to check
        # rather than two. `parsing.check_merge` enforces which values may fill
        # it, because the schema can express neither the dependency nor the
        # emptiness. The cap it can express, and does: a grammar-constrained
        # model is stopped at the bound rather than corrected after it, and the
        # tiers that have no grammar are covered because `check_merge` repeats
        # it there.
        "replacement": {"type": "string", "maxLength": parsing.REPLACEMENT_MAX},
        "reason": {"type": "string", "maxLength": parsing.REASON_MAX},
    },
    "required": list(parsing.DISPOSITION_FIELDS),
    "additionalProperties": False,
}

# The three fields, in the order `merge.md` asks for them: the document first,
# then what was chosen, then what happened to each segment that departed.
#
# `decisions` and `dispositions` are required rather than optional even though
# an empty list is a legitimate answer for either. An absent key and an empty
# list mean the same thing to a reader and different things to a checker: with
# the key required, "no departures" is a claim the model made, and the
# reconciler can hold it to the claim that every segment therefore survives
# character for character. Optional, it would be indistinguishable from a model
# that ignored the instruction.
MERGE_SCHEMA = {
    "type": "object",
    "properties": {
        "merged_document": {"type": "string"},
        "decisions": {"type": "array", "items": _DECISION_ITEM},
        "dispositions": {"type": "array", "items": _DISPOSITION_ITEM},
        # The merge's own warning that these documents may not belong together
        # Empty is the ordinary answer and the one a model should give
        # unless it is *sure*; a sentence here is a hint to the operator, not
        # a finding, and it moves no exit code.
        #
        # At every level, unlike `additions`: this is about the inputs rather
        # than about what the level licenses, and two source files in
        # different programming languages are as badly matched at `off` as at
        # `open`. Required, so a strict `json_schema` endpoint accepts the
        # schema, and so silence is an answer rather than an omission.
        "mismatch": {"type": "string", "maxLength": parsing.MISMATCH_MAX},
    },
    "required": ["merged_document", "decisions", "dispositions", "mismatch"],
    "additionalProperties": False,
}

# One source of truth for each contract, checked rather than duplicated: the
# schema is what the model is told and `parsing` is what it is graded against.
assert tuple(_DISPOSITION_ITEM["properties"]) == parsing.DISPOSITION_FIELDS
assert tuple(_DECISION_ITEM["properties"]) == parsing.DECISION_FIELDS
assert tuple(_CANDIDATE_ITEM["properties"]) == parsing.CANDIDATE_FIELDS
# The third record type had no such assertion when it was added, and adding
# two fields to it is exactly the edit that would have needed one: the schema
# is what the model is told and `parsing.ADDITION_FIELDS` is what the
# field-order check grades it against, so the two drifting apart is a refusal
# on every well-formed record.
assert tuple(addition_item()["properties"]) == parsing.ADDITION_FIELDS

# Words that appear in `merge.md`'s worked example and in no fixture document.
# A generated merge containing one of them is the model returning the prompt's
# illustration instead of merging its inputs — the failure that took down
# qwen3:4b under decompose, where only span
# anchoring noticed. `GLOBAL.json`'s `no-prompt-example-marlbrook` asserts the
# same thing over extracted claims; this is the raw-text half of the pair, and
# it runs before decompose so it cannot be defeated by how the copy was
# segmented.
EXAMPLE_MARKERS = ("marlbrook", "funicular")

# How `max_tokens` is sized for one merge. Deliberately a-priori and
# per-fixture: a flat ceiling either truncates the longest document in the
# suite or spends four minutes of GPU on the shortest.
#
# Three characters per token is the usual figure for English prose, and the
# lengths are JSON-escaped because that is what the model actually emits — the
# document arrives inside a string. The reasoning allowance is flat, and
# identical whether or not thinking is on, because the reasoning is charged
# against `max_tokens` like any other output. *Where* it arrives depends on the
# server: `parsing.strip_reasoning` exists because some endpoints put the
# `<think>` block inside `message.content`, and ollama returns it in a
# `reasoning` field beside it — but measured on qwen3.8:27b, the same question
# billed 50 completion tokens with thinking off and 168 with it on, so the
# ceiling has to cover it either way. Sizing the budget to the payload
# alone would truncate the thinking-on condition and only the thinking-on
# condition, and the comparison would report a budget artefact as "thinking
# makes the merge worse".
#
# ## One copy per field that carries document text, and one per document
#
# Until an earlier version, the budget was one document at 1.5x headroom,
# sized for a response whose only field was the document. The v2 schema
# has four more places a span of a source can land, and measurement showed what that costs:
# on the largest recorded merge the old figure ran out at roughly half the
# declared fraction, and at `high` nearly every segment is declared. Truncation
# is self-detecting — an unterminated JSON string fails `parsing.extract_json`,
# fails the repair attempt and errors the unit — but self-detecting at hour
# three of a recording run is still a burned recording run.
#
# So the payload is charged as whole documents, one per field that can hold
# copied text. Three of the fields are fixed and one of them is per document:
#
#   1. `merged_document`             — every source, if nothing is dropped
#   2. `decisions[].candidates[i]`   — one slot per document, each holding a
#                                      span of that document, so this column
#                                      grows with the number of sources rather
#                                      than with the number of decisions
#   3. `decisions[].chosen`          — the winner, restated in full
#
# `FIXED_COPIES + len(documents)` in all, which is four for a pair.
#
# `dispositions[].replacement` was a fifth, and is now charged on its own line
# below, because it is the one field with a cap. Its charge is the smaller of
# the document copy it used to be and `parsing.REPLACEMENT_MAX` times the record
# count: the cap is a proof (nothing longer parses), the copy only an argument
# (two records may point at overlapping spans, so "the sum is at most the
# document again" reads what a sensible model does). The cap lowers the charge
# only on a pair with more characters per segment than the cap; on the ~10 kB
# pair the bound was decided for, the copy is still what is charged.
# Every copy is charged at `HEADROOM` where the level permits composing, which
# pays for a merge restating a disputed value under two attributions; the next
# section says which copies keep it at a level that can only select. Nothing in
# the schema bounds the other copies, so no budget here is a proof. This one is
# pessimistic in a way that is stated rather than tuned, and `test_merge.py`
# holds it against a constructed worst-case payload rather than an estimate.
#
# ## What the level moves, and what it does not
#
# An earlier version sized all of that without asking which level was running, and at `off`
# that provisions for a response `off` forbids. `reconcile.PERMITTED` is the
# rule, and it is the same object the reconciler enforces and the four
# `prompts/fidelity/*.merge.md` fragments state in prose, so the budget is
# derived from it rather than from a second table that would drift.
#
# Only one question is asked of it: **may this level compose a replacement?**
# `reworded` and `subsumed` are the two dispositions whose replacement is
# wording the model wrote. `superseded` and `duplicate` point at wording that
# already exists in some source, and `dropped` points at nothing. So at a level
# permitting neither, every copy above but one can only ever hold text that was
# selected, and `HEADROOM` — which pays for composed prose — buys nothing on
# them. Only `merged_document` keeps it, because restating a disputed value
# under two attributions is structural and legal at every level.
#
# What the level does *not* move is the record count. `dropped` is declarable at
# every level (a review-queue entry under the disposition model, not an illegal answer), so every
# segment can carry a record whatever the slider says, and the per-segment term
# below is level-invariant by construction. That term is the larger half of the
# budget on a real pair, so the four figures are closer together than the
# argument for separating them suggests — which is itself the answer to whether
# `replacement` needs a schema-level bound. The numbers bear this out: on the
# ~10 kB pair the field is **5.6% of the budget at `off`** and the per-record
# scaffolding is **66.5%**, so the bound is a correctness guard and not a way
# into a context window.
#
# The cost of this: `fidelity` now reaches `max_tokens`, so two levels of one
# fixture differ in the cassette key by two components rather than one. That is
# a real loss of tidiness and it is bought deliberately. `num_ctx` is a KV cache
# the operator allocates up front, so an `off` run budgeted for `high` makes
# them provision memory the default level cannot use.
CHARS_PER_TOKEN = 3
HEADROOM = 1.5
FIXED_COPIES = 2
# Flat, and identical whether thinking is on or off, so that the only difference
# between the two conditions is the flag itself. Raised from 2048 on 2026-08-17
# after the first live measurement of an actual trace: sized from the worst
# *utilisation* observed over thirteen units rather than from the largest trace,
# because a trace sized against the largest trace refuses the incumbent model's
# window on a real pair while buying headroom the measurement says is already
# there.
REASONING_ALLOWANCE = 6144
BUDGET_STEP = 256

# The dispositions whose `replacement` is composed rather than selected. Named
# here and intersected with `reconcile.PERMITTED` below, so adding a sixth
# disposition to the contract forces a decision about which side it falls on.
GENERATED = ("reworded", "subsumed")
assert set(GENERATED) < set(parsing.DISPOSITIONS)

# Values in a record that are not spans of a source, and so are not covered by
# the copies above. Both are generous ceilings on a short string: a segment id
# is a letter and a line number, and a slot label names the thing chosen between.
SEGMENT_ID_MAX = 8
SLOT_MAX = 40


class MergeError(ValueError):
    """The mapping handed to this pass is not a set of sources. Fatal, never merged."""


def escaped_length(text: str) -> int:
    """Characters this text costs once it is inside a JSON string."""
    return len(json.dumps(text)) - 2  # the quotes are not part of the document


def _record_chars(fields: tuple[str, ...]) -> int:
    """What one JSON record of these fields costs before any value goes into it."""
    return len(json.dumps({name: "" for name in fields})) + 1  # + the separating comma


# Scaffolding per declared record: braces, field names, quotes, commas, and the
# values that are not copied text. Derived from `parsing`'s field tuples rather
# than counted by hand, so a field added to the contract is charged for here
# without anyone remembering to.
PER_DISPOSITION = (
    _record_chars(parsing.DISPOSITION_FIELDS)
    + SEGMENT_ID_MAX
    + max(len(value) for value in parsing.DISPOSITIONS)
    + parsing.REASON_MAX
)
def per_decision(names: tuple[str, ...]) -> int:
    """Scaffolding per decision record, for a merge of these documents.

    Scales with the document count rather than charging two: a decision lists
    the candidates it chose between, one per document that offered wording, and
    three documents can offer three. The name lengths are the documents' own
    because `candidates[].document` carries a filename and not a letter.
    """
    per_candidate = (
        _record_chars(parsing.CANDIDATE_FIELDS) + max(len(name) for name in names)
    )
    return (
        _record_chars(parsing.DECISION_FIELDS)
        + len(names) * per_candidate
        + SLOT_MAX
        + parsing.REASON_MAX
    )

# `PER_DISPOSITION` charges the longest disposition word, and that figure is the
# same at every level rather than by oversight: `superseded` is the longest of
# the five and is permitted in every row.
assert all(
    max(len(value) for value in row + ("dropped",))
    == max(len(value) for value in parsing.DISPOSITIONS)
    for row in reconcile.PERMITTED.values()
)


def composes(fidelity: str) -> tuple[str, ...]:
    """The dispositions this level may answer with that carry written wording."""
    if fidelity not in reconcile.PERMITTED:
        raise MergeError(
            f"unknown fidelity level {fidelity!r}; expected one of {config.FIDELITY_CHOICES}"
        )
    return tuple(value for value in GENERATED if value in reconcile.PERMITTED[fidelity])


# Which of the copies still needs `HEADROOM` at a level that can only select.
# Two of them do, and for different reasons:
#
#   merged_document             yes -- stating both sides of a disputed value
#                                      under two attributions lengthens the
#                                      merge, and that counts as selection, not copy-editing, so
#                                      it is legal at `off`
#   decisions[].candidates[i]   no  -- each a span of its own document
#   decisions[].chosen          yes -- the *longest* of the candidates each
#                                      time, so the column is not bounded by any
#                                      one document even with nothing composed
#
# The second was measured, not reasoned: charging `chosen` flat put `off` 64
# characters under `disjoint_sources`' worst case, and the acceptance test in
# `test_merge.py` caught it. It is two whatever the document count is: the
# candidate slots are the column that grows, and they are the flat ones.
SELECTED_HEADROOM_COPIES = 2


def document_copies(fidelity: str, count: int) -> tuple[int, int]:
    """How the copies split for `count` sources at this level.

    Returns (charged headroom, charged flat). `count` is the document count and
    not the fixed two, because `decisions[].candidates` has one slot per
    document: a five-source merge can restate five alternatives per decision,
    and a budget that charged two would truncate the response that did.

    `dispositions[].replacement` is not among these. It is the one copy with a
    cap, so `budget_tokens` charges it directly rather than as a share of a
    document.
    """
    total = FIXED_COPIES + count
    if composes(fidelity):
        return total, 0
    return SELECTED_HEADROOM_COPIES, total - SELECTED_HEADROOM_COPIES


def replacements(document: int, segments: int, fidelity: str) -> int:
    """What every `replacement` in one response can cost, in characters.

    The smaller of two bounds that are not the same kind of thing. The cap times
    the record count is arithmetic: `parsing.check_merge` refuses a longer one
    and the schema stops a grammar-constrained model from writing it, so nothing
    that parses can exceed it. The document copy is the older argument -- each
    replacement is a span of the merged document, so the sum is that document
    again, at `HEADROOM` where the level permits composing one -- and it is an
    argument rather than a bound, since two records may point at overlapping
    spans.

    Taking the min means the cap only helps where it binds: on sources with more
    characters per segment than `REPLACEMENT_MAX`. On the ~10 kB pair, at 54
    characters a segment, it does not bind and this term is exactly what it was
    before it was split out on its own, which is why this function
    exists as a named term rather than being folded into the copy count.
    """
    copies = int(document * HEADROOM) if composes(fidelity) else document
    return min(copies, segments * parsing.REPLACEMENT_MAX)


def verify_title(client: Client, merged_title: str, documents: dict[str, str],
                 candidates: tuple[str, ...]) -> reconcile.Finding | None:
    """Check a written title against the sources, as a claim.

    Only `synthesise` reaches here, and only for a title that is not already a
    source title byte for byte: taking one unchanged is correct at every policy
    and costs no call. So the model pays for a title it chose to write, and for
    nothing else.

    **Why a model call for one short string.** A title is a claim, and a claim
    cannot be graded by the words it is made of. "A motorbike is more stable
    than a quad" is assembled entirely from the vocabulary of sources that say
    the quad is the stable one; every deterministic stand-in this project tried
    accepted it. `reconcile` cannot help -- it grades no claims by design --
    so the title goes to the pass that reads both texts.

    A `SUPPORTED` title passes. Anything else is a finding: `CONTRADICTED` is
    the inversion this exists to catch, and `MISSING` is a title the documents
    neither state nor contradict, which is the invention the byte-identical
    rule used to make impossible.
    """
    # Imported here, not at module scope: `verify` imports `MergePolicy` from
    # this module, so a top-level import is a cycle.
    from . import verify

    if merged_title in candidates:
        return None
    claim = verify.Claim(id="title", source="merged.md", text=merged_title,
                         line=1, span=merged_title, anchored=True)
    verdicts = verify.verify_claims(
        client, [claim], documents, direction=verify.MERGED_TO_SOURCES
    )
    if not verdicts:
        return None
    verdict = verdicts[0]
    if verdict.verdict == "SUPPORTED":
        return None
    return reconcile.Finding(
        reconcile.TITLE_NOT_FROM_SOURCE,
        f"the written title {merged_title!r} is {verdict.verdict} against the "
        f"source documents"
        + (f": {verdict.rationale}" if verdict.rationale else "")
        + ". A title this project did not copy is checked as a claim, because "
          "one assembled from the documents' own words can still state what "
          "they contradict",
    )


# One capped sentence, plus the key, the quotes and the comma around it. The
# model may fill it on any response, so every response is budgeted for it.
PER_MISMATCH = parsing.MISMATCH_MAX + len('"mismatch": "",')

# And it is granted as a whole step, added *after* the rounding, for two
# reasons that both come from this being a fixed cost rather than a scaling
# one.
#
# Rounded *in*, it gave one fixture a whole 256-token step and its neighbour
# none, which broke the registered tie between `disjoint_domains` and
# `disjoint_sources` -- a control pair held to one size class, whose diverging
# budgets would be two measurements under one label. Added as a raw 72 tokens
# it left every budget off-step, and `budget_tokens` promises whole steps.
#
# One step is 1,024 characters against the 215 this needs, which is generous
# and deliberately so: the alternative is arithmetic that has to be redone
# every time the cap moves.
MISMATCH_ALLOWANCE = BUDGET_STEP


def budget_tokens(documents: dict[str, str], fidelity: str) -> int:
    """`max_tokens` for merging these sources at this level.

    `fidelity` has no default on purpose. A caller that omitted it would get a
    ceiling for some other level than the one it is about to ask for, and the
    failure — a response truncated mid-string — arrives hours later inside a
    recording run rather than here.

    **Every budget figure, reported or asserted, goes through `source_names()`.**
    This function charges the filename length: `per_decision` adds
    `max(len(name))` once per candidate slot, and the pipeline renames the
    sources to `source_a.md`/`source_b.md` before merging, so a figure computed
    from the documents' real filenames is a figure for a merge that never runs.
    Two 8-character names give a `per_decision` of 373 against 379, which is
    enough to land a pair one `BUDGET_STEP` below its true ceiling. The error is
    not confined to a misreported number: `max_tokens` is a cassette-key
    component, so a budget measured under the wrong names re-keys every cassette
    recorded against it.
    """
    document = escaped_length("".join(documents.values()))
    segments = sum(len(source.segments) for source in segment.segment_sources(documents))
    written, selected = document_copies(fidelity, len(documents))
    body = (
        int(document * HEADROOM) * written
        + document * selected
        + replacements(document, segments, fidelity)
        + segments * (PER_DISPOSITION + per_decision(tuple(documents)))
    )
    rounded = -(-int(body / CHARS_PER_TOKEN) // BUDGET_STEP) * BUDGET_STEP
    # `mismatch` is added *after* the rounding, like `REASONING_ALLOWANCE` and
    # for the same reason: it is a fixed cost per response that does not
    # scale with the document, so rounding it in gives one fixture a whole
    # 256-token step and its neighbour none. That broke the registered tie
    # between `disjoint_domains` and `disjoint_sources`, which are held to one
    # size class deliberately -- a control pair whose budgets diverge is two
    # measurements under one label.
    return rounded + REASONING_ALLOWANCE + MISMATCH_ALLOWANCE


def request_tokens(rendered: str, budget: int) -> int:
    """Everything one merge call occupies in the context window, end to end.

    Prompt plus ceiling, because both come out of the same allocation and the
    failure modes differ only in which half overran. An output that will not fit
    is truncated mid-string and errors the unit of work; a *prompt* that will not
    fit is silently trimmed from the front by the server, and the model then
    answers confidently about a document whose beginning it was never shown.
    Nothing downstream can tell that happened, which is why it is charged here
    rather than left to the ceiling alone.

    The prompt is converted at `CHARS_PER_TOKEN`, the same conversion the budget
    uses, and the rendered string is the one about to be sent -- not the raw
    documents. Estimating it from the sources understates it by around 9% on the
    canonical pair, because the rules, the worked example and the segment
    scaffolding are all prompt too, and 9% was the entire margin the last time
    this number was argued about.
    """
    return -(-len(rendered) // CHARS_PER_TOKEN) + budget


def check_sources(documents: dict[str, str]) -> tuple[str, ...]:
    """Two or more sources, canonically named and ordered, none of them empty.

    Returns the names rather than nothing, so a caller that needs them does not
    rebuild the list from a count that may not be the count this checked.
    """
    names = tuple(documents)
    expected = source_names(len(names))
    if names != expected:
        raise MergeError(
            f"merge takes its sources under canonical names, in order: expected "
            f"{', '.join(expected)}, got {', '.join(names) or '(nothing)'}"
        )
    empty = [name for name in names if not documents[name].strip()]
    if empty:
        raise MergeError(
            f"merge needs every source to say something; missing or empty: "
            f"{', '.join(empty)}"
        )
    return names


def compose_prompt(
    policy: MergePolicy,
    prompt: prompts.Prompt | None = None,
) -> tuple[prompts.Prompt, str, str, str]:
    """The merge prompt and the two fragments that go into it, hashed together.

    Returned as a triple rather than rendered here because the caller still has
    to supply the sources, and because the digest has to be composed from the
    same fragment texts that get substituted — computing them twice is how the
    report ends up naming a level the model was not given.

    Order is fidelity then title, matching the order the placeholders appear in
    `merge.md`. It is fixed rather than incidental: `prompts.compose` hashes the
    sequence, so swapping the two would silently re-key every merge cassette.
    """
    prompt = prompt or prompts.load("merge")
    fidelity = policy.fragment()
    example = policy.fragment("example")
    title = prompts.load(f"title/{policy.title_policy}")
    return (prompts.compose(prompt, fidelity, example, title),
            fidelity.text, example.text, title.text)


WHITESPACE = re.compile(r"\s+")
SLOT_PREFIX = re.compile(r"^(section|heading)\s*:\s*", re.IGNORECASE)


def _slot_text(text: str) -> str:
    """A slot or a heading, reduced to what the two can be compared on.

    Case-folded, whitespace-collapsed, and with a `section: ` prefix stripped.
    The slot is prose the model wrote and the heading is prose the author wrote;
    exact equality would answer "no second candidate" for a slot that differs
    from its heading by a capital letter.
    """
    return WHITESPACE.sub(" ", SLOT_PREFIX.sub("", str(text)).strip()).casefold()


def available_candidates(
    sources: tuple[segment.Document, ...]
) -> parsing.AvailableCandidates:
    """How many candidates the sources offered for a slot a decision names.

    Returns a resolver for `parsing.merge_checker`, closed over the segmented
    documents. **The question is asked of the sources, never of the merge** — a
    merge that dropped one of two competing headings would otherwise report that
    only one was ever available, which is the defect being checked for.

    Three answers, and the third is not the second:

    - `title`: the case the prompt is explicit about. Counted through
      `reconcile.titles_of` so this uses the same notion of a title the
      reconciler grades against. Two documents with distinct titles offer two;
      two documents sharing a title, or one document carrying the only title,
      offer one.
    - a slot naming a heading: the documents carrying that heading. A section in
      both offered two candidates, a section in one offered one.
    - anything else: `None`, meaning undeterminable. A slot like "which of two
      wordings" is defined by the model, and a number invented for it would be a
      judgement wearing a measurement's clothes. `parsing.check_merge` keeps the
      unconditional rule for that answer.
    """
    titles = {
        source: {_slot_text(item.text) for item in reconcile.titles_of(source.segments)}
        for source in sources
    }
    headings = {
        source: {_slot_text(item.text) for item in source.segments
                 if item.kind == segment.HEADING and item.text.strip()}
        for source in sources
    }

    def resolve(slot: str) -> int | None:
        wanted = _slot_text(slot)
        if wanted == "title":
            # `or None` for the same reason the heading branch has it: no title
            # in either document is not one candidate, it is a slot that does
            # not resolve, and the unconditional rule keeps applying to it.
            return len({text for texts in titles.values() for text in texts}) or None
        offering = sum(1 for texts in headings.values() if wanted in texts)
        return offering or None

    return resolve


def merge_documents(
    client: Client,
    documents: dict[str, str],
    prompt: prompts.Prompt | None = None,
    max_tokens: int | None = None,
    thinking: bool | None = None,
    policy: MergePolicy | None = None,
    base: str | None = None,
) -> MergeResult:
    """Merge several sources into one document. One model call, schema-constrained.

    `MergeResult.document` is exactly what the model wrote, byte for byte — no
    stripping, no normalisation, no trailing newline added. Everything
    downstream grounds evidence spans against this string, so a character
    changed here is a character verify would then fail to find. The declared
    decisions and dispositions come back with it rather than beside it, because
    a replacement pointer is only checkable against the document it points into.

    The sources reach the prompt segmented, not raw. The merge model and the
    reconciler have to consume the same segmentation or they compare two
    different denominators — and the ids are what let a disposition record be
    checked by set membership instead of by asking a second model.

    `base` names the document whose structure the merge follows, and defaults to
    the first source. It is a filename because that is what a command line will
    hand it, and it is checked against the documents rather than trusted. The
    default is stated here and not relied on at the boundary: `cli.py` requires
    `--base` and refuses to pick, because with three sources on a command line
    "the first one" is a coin toss the operator did not know they had made.

    Whichever way it was arrived at comes back on the result, as `base` and
    `base_chosen`. The default stays, because requiring the argument would break
    library call sites for a safety the record can supply instead — but only if
    the record actually carries it, which is why this is returned rather than
    recomputed by a caller that would have to guess.

    Raises client.SchemaFailure if the model could not be made to answer in a
    usable form, and MergeError if the mapping is not two or more canonically
    named non-empty sources. Neither is
    swallowed into an empty document: "the merge is empty" and "the merge call
    failed" look identical in a coverage table and mean opposite things.
    """
    names = check_sources(documents)
    policy = policy or MergePolicy()
    base_chosen = EXPLICIT if base else DEFAULTED
    base = base or names[0]
    prompt, fidelity_rules, fidelity_example, title_rule = compose_prompt(
        policy, prompt)
    # Bound to a local rather than left as an intermediate: the availability
    # resolver closes over the same segmentation the prompt shows the model, so
    # the check and the model are answering about one set of segments.
    segmented = segment.segment_sources(documents)
    sources = segment.render_sources(segmented, base)
    rendered = prompt.render(
        fidelity_rules=fidelity_rules,
        fidelity_example=fidelity_example,
        title_rule=title_rule,
        base_filename=base,
        sources=sources,
    )
    # An explicit `max_tokens` still wins. Otherwise the profile
    # decides: `CEILING_MODEL` sends no ceiling and the endpoint applies its
    # own, because a flat `REASONING_ALLOWANCE` cannot hold for a model that
    # scales reasoning with difficulty. `budget` is therefore `None` on the
    # frontier profiles, and `structured.build_body` omits the field entirely
    # when it is (the guard in `build_body`).
    if max_tokens is not None:
        budget = max_tokens
    elif (structured.profile_for(client.settings.profile).output_ceiling
          == structured.CEILING_MODEL):
        budget = None
    else:
        budget = budget_tokens(documents, policy.fidelity)

    # The budget is computed from the documents and the level; whether
    # it fits is a property of the server, and until now nothing compared the
    # two. Asked here because this is the only place a merge budget is turned
    # into a request, and asked *before* the request, because the two failures
    # it prevents are both silent-ish and both expensive: a trimmed prompt is
    # never reported at all, and a truncated answer is reported only after the
    # generation has been paid for. `served_window` returns None for three
    # reasons now, not two: replay, dry run, or an endpoint that does not
    # expose `/api/ps` at all. The first two send
    # nothing and need no guard of either kind; the third takes the call for
    # real with no preflight guard in front of it, and the check below is what
    # stands in its place.
    what = f"merging {len(documents)} sources at fidelity {policy.fidelity}"
    served = client.served_window("merge")
    if served is not None:
        # With no ceiling the output half cannot be charged in advance, but the
        # *prompt* half is the protection that matters here and is unaffected:
        # an oversized prompt is silently trimmed from the front by the server
        # and the model then answers confidently about a document whose
        # beginning it never saw, which nothing downstream can detect. So the
        # guard still runs; only the output term drops to zero.
        window.guard(
            needed=request_tokens(rendered, budget or 0),
            window=served,
            what=what,
        )

    completion = client.complete(
        role="merge",
        prompt=prompt,
        messages=[{"role": "user", "content": rendered}],
        schema=merge_schema(policy.fidelity),
        schema_name="emit_merge",
        semantic=parsing.merge_checker(available_candidates(segmented),
                                       MAY_CHOOSE[policy.fidelity]),
        max_tokens=budget,
        thinking=thinking,
    )
    payload = completion.payload

    # `served` is `None` for two different reasons and only
    # one of them needs a check here: a replay or dry run sent nothing, so
    # there is nothing to have been truncated, but an endpoint that could not
    # say what it serves (`window_mechanism` starts "post-hoc") just took a
    # real call with no preflight guard in front of it. This reads the ledger
    # row that call just wrote rather than taking a second measurement, per
    # the ledger being the one place the run already carries these counts
    # exactly.
    #
    # A **stated** window takes this check too, and that is the point of it
    # being a third mechanism rather than a second kind of preflight. The
    # preflight ran, against a figure nobody confirmed; if the figure is larger
    # than what the endpoint serves, the guard passed a request that does not
    # fit, and this is the only thing downstream that would notice. It costs a
    # comparison of two numbers the ledger row already carries.
    #
    # Read off the mechanism rather than off `served`, so the four cases stay
    # separate: replay and dry run carry no mechanism at all and are skipped,
    # `preflight` is skipped because it was measured, and `post-hoc` and
    # `stated` both run.
    if client.usage.window_mechanism.get("merge", "").startswith(
            ("post-hoc", window.STATED)):
        window.assert_untruncated(client.usage.ledger[-1] if client.usage.ledger else {},
                                  what=what)

    # The prompt side, and unconditionally rather than only where the window
    # could not be measured. `assert_untruncated` above answers the vendor
    # case, where nothing preflighted at all; this one answers that *and* the
    # case a successful preflight still leaves open, because `measured()`
    # confirms its figure to only `PROBE_FILL` of itself and a prompt in the
    # top of that band passes the guard unverified. Costs a
    # comparison of two numbers the ledger row already carries.
    window.assert_prompt_not_trimmed(
        client.usage.ledger[-1] if client.usage.ledger else {}, what=what)

    return MergeResult.from_payload(
        payload, base=base, base_chosen=base_chosen, truncations=completion.truncations)


def example_content_leaks(text: str) -> list[str]:
    """Which of `merge.md`'s worked-example markers this document contains.

    Case-insensitive raw substring search over the generated text, run before
    decompose. Empty is the only passing answer.

    Scoped to the merged document and to content words, which is the whole of
    what it claims. A model can reproduce the example without either marker --
    see `example_reason_leaks`, which is the other half and was added after a
    leak this one was never asked about.
    """
    lowered = text.lower()
    return [marker for marker in EXAMPLE_MARKERS if marker in lowered]


def _flatten(text: str) -> str:
    """Whitespace-collapsed, lowercased, trailing stop removed."""
    return " ".join(text.split()).strip().rstrip(".").lower()


def example_reason_clauses() -> tuple[str, ...]:
    """The reason clauses `merge.md`'s worked example teaches, read from it.

    Derived from the prompt rather than listed here, so it cannot fall behind
    the example it guards: the example is the only place these sentences are
    written down, and a list beside it would be a second copy to forget. Every
    level's example is read, not just the level in play, because a reason that
    quotes any of them is reproducing the prompt either way and the scan does
    not know which level produced the record.
    `test_merge.py` pins that the derivation returns something, because a
    reworded example that this stops parsing would otherwise go quiet.

    Scoped to the *reason* clauses rather than to every sentence of the
    example, and the disagreement block is why. "The documents disagree and
    this merge does not choose between them" is the output shape the base
    rules prescribe, so a merge that copies it is obeying the prompt, not
    leaking it. A scan over the whole example would fire on correct output and
    would then need a length floor to quiet it, which is a threshold fitted to
    nothing. Reasons carry no prescribed wording, so they need no floor.
    """
    found: set[str] = set()
    for level in config.FIDELITY_LEVELS:
        flat = " ".join(prompts.load(f"fidelity/{level}.example").text.split())
        found |= {_flatten(m.group(1))
                  for m in re.finditer(r"\bbecause\s+(.+?)\.(?:\s|$)", flat)}
    return tuple(sorted(clause for clause in found if clause))


def example_reason_leaks(records: Iterable[dict]) -> list[tuple[str, str]]:
    """(field, clause) for every record whose own words are the example's.

    The leak `example_content_leaks` cannot see: the model merged the real documents,
    so no marker reached the merged text, and then wrote the example's reason
    sentence into its own `reason` field. Exact-string containment, because a
    reason that quotes the example is reproducing it whatever surrounds it.

    `reason` is the only free text a record carries. `segment` and
    `disposition` are drawn from fixed vocabularies the parser already checks,
    and `replacement` is required to be a span of the merged document, so
    example text arriving there has already reached the text `example_content_leaks`
    reads.
    """
    clauses = example_reason_clauses()
    found: list[tuple[str, str]] = []
    for record in records:
        reason = _flatten(str(record.get("reason", "")))
        if not reason:
            continue
        for clause in clauses:
            if clause in reason:
                found.append((str(record.get("segment") or record.get("slot") or "?"),
                              clause))
    return found
