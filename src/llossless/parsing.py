"""Turn whatever a model actually said into a validated object, or an error.

This layer runs on the output of all three structured-output tiers, and it is
the reason the tool is portable. Tier 1 endpoints hand back clean JSON and none
of this does any work; tier 3 endpoints hand back a reasoning block, a markdown
fence, and a sentence of preamble, and this is what makes that usable. Because
the same code runs either way, a tier-1 endpoint's output has been through the
same checks as a tier-3 endpoint's, so a run cannot be quietly more trustworthy
on one provider than another.

The one rule that matters more than the rest: never repair by guessing. A
missing verdict is not MISSING, a truncated array is not a short array, and an
unparseable verify response is an ERROR rather than a finding. Every function
here either returns what the model said or raises; none of them invents.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass

from .config import DEFAULT_FIELD_ORDER, FIDELITY_LEVELS

OPENERS = {"{": "}", "[": "]"}
THINK_TAGS = ("think", "thinking", "reasoning", "scratchpad")

# A reasoning block is a *preamble*, and the rule is anchored to say so. The
# pattern matches only at the head of the content, past leading whitespace, and
# it is applied to the original string -- never to `text.lower()`, because
# lowering is not length-preserving (U+0130 becomes two characters) and every
# offset after one such character would be wrong.
LEADING_REASONING = re.compile(
    r"\A\s*<\s*(" + "|".join(THINK_TAGS) + r")\s*>", re.IGNORECASE)


class ParseError(ValueError):
    """The response could not be turned into a valid object.

    Carries a `feedback` string written for the model rather than for a human:
    it is what gets appended to the second attempt, so it has to name the fault
    precisely enough to be actionable and say nothing else.
    """

    def __init__(self, message: str, feedback: str | None = None, *,
                 order_only: bool = False, looping: bool = False) -> None:
        super().__init__(message)
        self.feedback = feedback or message
        # Every fault in this response was a field emitted in the wrong place.
        # The caller uses it to decide whether asking again is worth a second
        # generation; see `client.complete`. False for anything built by hand,
        # which is the honest default: a caller that did not measure the
        # question has not answered it.
        self.order_only = order_only
        # At least one fault was a claim restated past `CLAIM_REPEAT_LIMIT` at
        # one place -- a generation loop. `any` rather than `all`, unlike
        # `order_only`: a looping response usually has other faults too, and the
        # reason the caller asks is the cost of the *generation*, which is
        # already paid whatever else was wrong with it.
        self.looping = looping


# --------------------------------------------------------------------------
# Steps 1-4: text in, object out
# --------------------------------------------------------------------------


def strip_reasoning(text: str) -> str:
    """Drop a <think>-style block from the *head* of a response, and only there.

    Small reasoning models emit these even when asked not to, and some
    endpoints pass them through in `content` rather than a separate field. An
    unterminated opener means the response was truncated mid-thought: there is
    no JSON after it, and saying so early gives a better error than a bracket
    counter running off the end of the string.

    **Only a leading block, because the payload is allowed to mention the
    tags.** This used to scan the whole string and delete everything between
    the first opener and its closer wherever they sat. A document that told an
    operator to "wrap your reasoning in <think> and </think> tags" therefore
    had that sentence deleted out of the merged output on the way through the
    parser, and the reconciler downstream never saw it go: the text was gone
    before anything counted it. A bare mention with no closer truncated the
    response at that point instead.

    So the rule is anchored. Past leading whitespace, a block opener is a
    preamble and is removed with its closer; the first character that is not
    one ends the scan, and nothing after it is examined. Consecutive leading
    blocks are all preamble. An unterminated leading block still yields "",
    which is what makes `loads` report a truncation rather than a syntax error.
    """
    while True:
        opener = LEADING_REASONING.match(text)
        if opener is None:
            return text.strip()
        closer = re.compile(r"<\s*/\s*" + re.escape(opener.group(1)) + r"\s*>",
                            re.IGNORECASE).search(text, opener.end())
        if closer is None:
            return ""  # truncated mid-thought; nothing usable follows
        text = text[closer.end():]


def strip_fences(text: str) -> str:
    """Remove ```json ... ``` wrappers, terminated or not."""
    text = text.strip()
    if not text.startswith("```"):
        return text
    newline = text.find("\n")
    if newline < 0:
        return text
    text = text[newline + 1 :]
    closing = text.rfind("```")
    return (text[:closing] if closing >= 0 else text).strip()


def extract_json(text: str) -> str:
    """Return the outermost balanced JSON object or array in `text`.

    Bracket counting rather than a regex, because a regex cannot count. The
    string-and-escape tracking is not optional: fixture prose contains braces
    and the health-check path `/-/healthy`, and a naive counter that ignores
    string context closes the object in the middle of a value.
    """
    start = next((i for i, ch in enumerate(text) if ch in OPENERS), -1)
    if start < 0:
        raise ParseError(
            "response contains no JSON object or array",
            "Your response contained no JSON. Reply with the JSON object only.",
        )

    closer = OPENERS[text[start]]
    depth = 0
    in_string = False
    escaped = False

    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch in OPENERS:
            depth += 1
        elif ch in ("}", "]"):
            depth -= 1
            if depth == 0:
                if ch != closer:
                    raise ParseError(
                        f"mismatched brackets: opened with {text[start]!r}, closed with {ch!r}"
                    )
                return text[start : i + 1]

    raise _unterminated(text, start, closer, depth, in_string)


def _unterminated(text: str, start: int, closer: str, depth: int, in_string: bool) -> ParseError:
    """Ran out of input, or lost track of the string? They are different faults.

    The scan above ends unbalanced for two unrelated reasons and used to report
    both as "the response was probably cut off", which sends the reader to
    max_tokens. That is right for exactly one of them.

    A complete document is the other, and one was recorded on a real run: it
    has `finish_reason: "stop"`, six braces against six, ending on its own
    `}` -- and it reads
    `"claim\\n },\\n {\\n "claim_id": ...`: a string opened and left unclosed at a
    raw newline. Every quote after it is read with inverted parity, three
    closing braces are swallowed as string content, and the scan runs off the
    end holding depth 3. The budget was never the problem, and the token
    ceiling is the wrong place to send anyone.

    The completeness test is a naive bracket count over the same text. It is a
    heuristic and only ever chooses wording: a document whose *string values*
    contain unmatched braces would count as incomplete, but such a document
    parses and never reaches here.
    """
    tail = text[start:].rstrip()
    opener = text[start]
    balanced = tail.count(opener) == tail.count(closer)
    complete = balanced and tail.endswith(closer)

    if in_string and complete:
        return ParseError(
            f"JSON is unterminated: a string value was opened and never closed. "
            f"The response is not truncated -- it ends on its own {closer!r} and "
            f"its {opener!r}/{closer!r} counts balance at {tail.count(opener)} -- "
            f"so a quote or newline inside a string value is unescaped.",
            'Your JSON had a string value that was never closed. Inside a string, '
            'write \\" for a quote and \\n for a newline. Reply with the complete '
            "JSON object and nothing else.",
        )
    if in_string:
        return ParseError(
            "JSON is unterminated: the response ended inside a string value.",
            "Your JSON stopped in the middle of a string value. Reply with the "
            "complete JSON object and nothing else.",
        )
    return ParseError(
        f"JSON is unterminated: the response ran out with {depth} bracket(s) still "
        f"open; it was probably cut off.",
        f"Your JSON was incomplete: {depth} bracket(s) were never closed. Reply "
        f"with the complete JSON object and nothing else.",
    )


def loads(text: str) -> object:
    """Steps 1-4, in order."""
    candidate = extract_json(strip_fences(strip_reasoning(text)))
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise ParseError(
            f"invalid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}",
            f"Your response was not valid JSON: {exc.msg}. Reply with valid JSON only.",
        ) from exc


# --------------------------------------------------------------------------
# Step 5: a validator small enough to read
# --------------------------------------------------------------------------

TYPES: dict[str, type | tuple[type, ...]] = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
}


def validate(value: object, schema: dict, path: str = "$") -> list[str]:
    """Check `value` against the subset of JSON Schema this project emits.

    Supported: type, required, properties, additionalProperties: false, items,
    enum, maxLength, minItems. That is every keyword used by the schemas in
    this repository, and adding a dependency to cover keywords nobody writes
    would spend a third of the budget on nothing.

    Returns a list of human-readable errors; empty means valid.
    """
    errors: list[str] = []
    expected = schema.get("type")

    if expected:
        wanted = TYPES.get(expected)
        # bool is a subclass of int in Python; JSON Schema does not agree.
        ok = isinstance(value, wanted) and not (
            expected in ("integer", "number") and isinstance(value, bool)
        )
        if not ok:
            return [f"{path}: expected {expected}, got {type(value).__name__}"]

    if "enum" in schema and value not in schema["enum"]:
        allowed = ", ".join(json.dumps(option) for option in schema["enum"])
        errors.append(f"{path}: {json.dumps(value)} is not one of [{allowed}]")

    if isinstance(value, str) and "maxLength" in schema and len(value) > schema["maxLength"]:
        errors.append(f"{path}: {len(value)} characters, maximum is {schema['maxLength']}")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                errors.append(f"{path}: missing required property {name!r}")
        if schema.get("additionalProperties") is False:
            for name in value:
                if name not in properties:
                    errors.append(f"{path}: unexpected property {name!r}")
        for name, subschema in properties.items():
            if name in value:
                errors.extend(validate(value[name], subschema, f"{path}.{name}"))

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: {len(value)} items, minimum is {schema['minItems']}")
        if "items" in schema:
            for i, item in enumerate(value):
                errors.extend(validate(item, schema["items"], f"{path}[{i}]"))

    return errors


# --------------------------------------------------------------------------
# Step 6: semantic checks the schema cannot express
# --------------------------------------------------------------------------

# PARTIAL was added last, because that is where both verify prompts list
# it. It is the label for a claim the reference text states part of and does not
# contradict the rest of, and it exists because the two places it could have
# been folded into are both wrong in a way that matters. Folded into MISSING it
# overstates loss: a fact carried with one detail missing is not a fact that did
# not survive. Folded into SUPPORTED it hides the failure this tool is for — a
# merge that adds one detail to a real fact reads as a real fact, and on the
# reverse pass that is the quietest invention there is.
VERDICTS = ("SUPPORTED", "CONTRADICTED", "MISSING", "PARTIAL")

# The fifth label, and it exists at one fidelity level only. `high` may combine
# complementary facts into a statement neither document makes on its own, and
# the reverse pass needs a way to say "no single source states this and the
# sources state it together" that is neither SUPPORTED -- which
# would claim one span carries it -- nor MISSING, which would call a licensed
# combination an invention.
#
# **It is level-aware because the schema is the enforcement.** The alternative
# considered and rejected was teaching every level the label and forbidding it
# in prose at three of them. That leaves a model at `off` holding a label it
# must never emit and nothing but an instruction stopping it, and `off` is the
# strict mode five registrations hold constant -- changing what that model is
# told changes the instrument under every registered measurement. Here a model
# at `off` that emits DERIVED is rejected by the schema it was given, which is
# a stronger guarantee than the rule it replaces and costs those levels
# nothing: their label set, their schema and their cassette keys are the ones
# they had before this existed.
DERIVED = "DERIVED"

# The levels that may emit it, as a set rather than as `== "high"`.
#
# The equality test was the one place a fifth level would have failed
# **silently**: `open` keeps every licence `high` has, including joint
# derivation, and would have been handed the four-label `off` schema with no
# error anywhere -- the model simply never offered the label, the reverse pass
# reading every licensed combination as an invention, and nothing to say why.
# Every other table a level must appear in is guarded by an import-time assert
# and fails loudly; this one did not, which made it the dangerous one.
#
# Written as membership so the next level joins by being named here, and
# asserted below against `FIDELITY_LEVELS` so a level that is *not* named is a
# deliberate omission rather than a forgotten one. `sourced` is named because
# it keeps every licence `open` has, joint derivation included; what it
# changes is where a *declared* statement came from, which is a question about
# `additions` and not about this label set.
DERIVES = frozenset({"high", "open", "sourced"})
assert DERIVES <= set(FIDELITY_LEVELS)


def verdicts_for(fidelity: str = "off") -> tuple[str, ...]:
    """The closed label set a model at this level may emit.

    Defaulting to `off` is deliberate rather than convenient: every caller
    that has no fidelity to hand gets the strict set, so a path that forgets
    to thread the level through refuses DERIVED rather than admitting it.
    """
    return VERDICTS + (DERIVED,) if fidelity in DERIVES else VERDICTS


def evidenced_for(fidelity: str = "off") -> tuple[str, ...]:
    """Labels that owe a span, at this level.

    DERIVED owes one for the same reason SUPPORTED does, and more so: it
    asserts the sources carry the claim jointly, so a DERIVED with nothing
    quoted is the one shape that would let an invention through as a
    combination nobody has to point at.
    """
    return EVIDENCED + (DERIVED,) if fidelity in DERIVES else EVIDENCED

# The verify result contract, in emission order. Order is checked, not just
# membership: see verify.VERDICT_SCHEMA for why the model is made to commit to
# a label before it writes the argument for one.
VERDICT_FIELDS = ("claim_id", "verdict", "evidence", "evidence_source", "rationale")

# The fused coverage pass emits one record per claim carrying both halves:
# `decompose`'s three fields and then the verdict's, minus `claim_id`. There is
# no id in the contract because the claims come back in document order and are
# numbered by position, exactly as `decompose` numbers them, so the same claim
# gets the same id at either verification depth and one report can be read
# against the other.
COVERAGE_FIELDS = ("text", "line", "span") + VERDICT_FIELDS[1:]

# Which verdicts assert that the reference text says something, and therefore
# owe a span and a filename. MISSING is the complement and the only one: it
# asserts an absence, and there is nothing to quote for one. PARTIAL is on this
# side of the line because the part it says is stated is stated somewhere, and a
# PARTIAL nobody can point at is indistinguishable from a hedge.
EVIDENCED = ("SUPPORTED", "CONTRADICTED", "PARTIAL")

# How long a rationale may be. Must match the number both verify prompts state.
#
# An earlier corpus is what put a truncation check here. Three of 240 recorded
# rationales sat exactly at the cap, all the same probe, all cut mid-sentence,
# and all of them spent the budget arguing away from the label they had already
# filed. Raising the cap was the obvious response and is not the one taken: a
# rationale that needs a thousand characters is a model deliberating, and
# deliberation belongs before the label, not after it. The verdict now comes
# first in the schema and the prompt says so, so the argument can no longer
# reach back and change it. Truncation stays an error because a cut-off
# sentence is still unreadable — it just no longer costs a finding.
RATIONALE_MAX = 400

# The merge's disposition contract, and the five values a departure can
# take. `retained` is deliberately not among them: silence *is* the claim of
# verbatim retention, so a segment with no record is asserting that it survived
# character for character, and a string comparison checks it. Adding `retained`
# would make the model write a record per segment, turn the output from a list
# of departures into a list of everything, and — the part that matters — move
# the absent-and-undeclared case from a set difference to a judgement.
DISPOSITIONS = ("reworded", "superseded", "subsumed", "duplicate", "dropped",
                "reconciled")

# Which of them owe a replacement span. `dropped` is the complement and the only
# one: it asserts the content is gone and nothing carries it, so there is
# nothing to point at. Every other value names text the merge does contain, and
# a declared departure whose replacement cannot be found is treated downstream
# as an undeclared drop — worse than declaring nothing, which the prompt says in
# those words so a model that games it has been warned in its own instructions.
REPLACED = tuple(value for value in DISPOSITIONS if value != "dropped")

# Both merge record contracts, in emission order. Order is checked rather than
# just membership, for the reason VERDICT_FIELDS is: the model commits to the
# value before it writes the justification for one. `disposition` before
# `replacement` before `reason`, and `chosen` before `reason`.
class OrderFault(str):
    """A validation message about field order, and nothing else about it.

    A marker class rather than a suffix to grep for. These messages read the
    same as every other one, join the same way and reach the model the same
    way; the type is only there so `parse` can tell "the answer is right and
    the keys are in the wrong sequence" from "the answer is wrong". The two
    call for different responses -- the first is a property of the model's
    serializer and asking again produces it again -- and a string comparison
    would tie that decision to the wording of an error message.
    """


def order_fault(message: str, emitted: tuple[str, ...],
                fields: tuple[str, ...]) -> str:
    """`message`, marked as an order fault when order is all that is wrong.

    `emitted` lists the contract's fields in the order the record gave them,
    so it differs from `fields` in two quite different situations: the record
    has them all and shuffled, or the record is missing some. Only the first is
    an order fault. The second is a field that is not there, which no amount of
    reordering fixes and which a second attempt might well fix.
    """
    return OrderFault(message) if set(emitted) == set(fields) else message


DISPOSITION_FIELDS = ("segment", "disposition", "replacement", "reason")
DECISION_FIELDS = ("slot", "candidates", "chosen", "reason")

# What the merge says about a statement it added from outside the documents.
# `open` alone may emit these, and the list is what buys the
# softer treatment: an addition the merge did not declare is a hallucination
# by every test this tool has, and stays one.
#
# Order is the same convention as the other two records -- the value, then
# what it relates to, then the justification -- so a grammar-constrained model
# commits to the statement before it writes the argument for it.
#
# `corrects` may be empty. A merge that extends the documents with something
# they do not discuss corrects nothing, and forcing it to name a victim would
# make it invent one. Where it is filled it quotes the document's own words,
# so the record holds what was changed *from* beside what it was changed *to*
# and a reader can see the swap without going back to the sources.
#
# `basis` and `source` are the pair that carries the operator's second ask --
# *"provide sources when it replaces a statement"* -- and they are two fields
# rather than one for the reason the whole feature is dangerous: models
# fabricate citations at high rates, and a single free-text `source` field
# makes "I am going on my own knowledge" look like a failure to fill it in. A
# required enum with `own-knowledge` as a first-class member is a field the
# model can answer honestly. See `BASES`.
ADDITION_FIELDS = ("statement", "corrects", "basis", "source", "reason")

# What a declared addition may say it rests on. Closed, required, and with no
# default -- the discriminating field is on every record or the record is
# refused, because a basis this tool guessed at would be this tool inventing
# the very thing it exists to catch.
#
# Exactly two members, and the second is not an escape hatch. `own-knowledge`
# is the *expected* answer for most corrections and the prompt says so: the
# alternative to making it respectable is a model that writes a plausible URL
# to fill a field that felt like it wanted one. A fabricated citation in a
# report a reader trusts is worse than no citation at all, because it launders
# a guess into something that looks checkable.
#
# Neither value means verified. Nothing in this package resolves, fetches or
# checks a citation, and the reports say so in the section that lists them.
BASES = ("citation", "own-knowledge")
CITATION, OWN_KNOWLEDGE = BASES


def decision_fields(may_choose: bool | None = None) -> tuple[str, ...]:
    """The decision fields a level must emit, in order. One source of truth.

    The schema and the emptiness check became level-aware, but left the
    field-order check demanding all four, so a model handed a schema saying
    `chosen` was optional had its record refused for omitting it -- at `off`,
    `low` and `mid`, which is nearly every merge. The lesson is not that a
    third site was missed but that three sites were each deciding this for
    themselves: what a level requires is asked here now, by everything.

    `may_choose=None` means the level was not threaded, and the strictest
    answer applies, for `decision_item`'s reason: a path that forgets the
    level must fail closed rather than accept a record the level forbids.
    """
    if may_choose is False:
        return tuple(f for f in DECISION_FIELDS if f != "chosen")
    return DECISION_FIELDS
CANDIDATE_FIELDS = ("text", "document")

# How long a merge record's reason may be. A fifth of the verify cap, and lower
# on purpose: a rationale argues a label it might be wrong about, while a reason
# names which of two wordings was taken. The prompt asks for one sentence.
#
# Cut from 200, which is the larger half of the resulting budget saving: the
# reason is charged twice per segment, once in `PER_DISPOSITION` and once in
# `per_decision`, so 120 characters off each is 240 off every segment, and
# that arithmetic is what the cut was worth against the budget.
#
# The objection this overrules is that a shorter reason degrades the review
# queue. It does not, because the reason is not what the reviewer reads: the
# queue hands them the segment id, the source text, the disposition and the
# replacement anchor, and the reason points at which of those to look at. 80
# characters is a sentence naming a slot and a choice, which is the whole job.
REASON_MAX = 80

# How long a `replacement` may be, and how a longer span is pointed at.
#
# The field names a span of the merged document, and a span can be a paragraph.
# Unbounded, one record per segment means the merge may be asked to restate
# itself entirely inside its own declarations, and `merge.budget_tokens` has to
# reserve output for that. So a replacement longer than the cap is given as its
# two ends -- the first and last `ANCHOR_HALF` characters, joined by `ELISION` --
# which is enough for `reconcile` to resolve it against the merge and enough for
# a reader to see which span is meant.
#
# The figure is argued, not measured: no recorded run carries a replacement to
# measure, because the report's `declarations` are the graded view and drop the
# field. It is `REASON_MAX` plus room, on the reasoning that a replacement quotes
# a sentence where a reason writes one, and quoting a whole sentence unelided
# should be the ordinary case rather than the exception. What the cap is worth
# against the budget turned out to be less than the earlier estimate assumed.
# How long the merge's mismatch warning may be. Its own cap, not
# `REASON_MAX`: that one is sized for "name the slot and the choice" in a
# decision record, and reusing it here cut a real sentence dead at 80
# characters -- *"...in different, non"* -- because a vendor enforcing
# `maxLength` during constrained decoding stops mid-word. What this field has
# to do is explain to a person why two documents may not belong together, and
# that is a different length of job.
MISMATCH_MAX = 200

# How long a declared addition's `source` may be. Its own cap for the reason
# `MISMATCH_MAX` is: this field holds a URL, a specification name and section,
# or a title and date, and `REASON_MAX`'s 80 characters cuts a real URL in
# half. It is not `REPLACEMENT_MAX` either, because nothing resolves this
# string against the merged document and an unbounded one is just a bigger
# thing to render.
SOURCE_MAX = 200

REPLACEMENT_MAX = 640
ELISION = " [...] "
ANCHOR_HALF = (REPLACEMENT_MAX - len(ELISION)) // 2


def anchor(span: str) -> str:
    """This span as a replacement: itself, or its two ends with the middle out."""
    if len(span) <= REPLACEMENT_MAX:
        return span
    return span[:ANCHOR_HALF] + ELISION + span[-ANCHOR_HALF:]


def anchor_parts(replacement: str) -> tuple[str, ...]:
    """The pieces of a replacement that must each be found, in this order.

    One piece for an unelided replacement, which is the common case and the
    reason this is a tuple rather than a pair. Empty pieces are dropped so a
    replacement that is nothing but the marker resolves against nothing rather
    than against everything.
    """
    return tuple(part for part in replacement.split(ELISION) if part.strip())


# What a finished sentence ends with, allowing a closing quote or bracket after
# the mark.
FINISHED = re.compile(r"[.!?][)\]\"'”’]*$")


def unfinished(rationale: str) -> bool:
    """Was this rationale cut off mid-thought?

    Asked of the text and not of its length, which is the whole point. Length
    was the first version of this check and it only caught truncation that
    happened to land exactly on the cap — a rationale stopped one character
    early, or stopped by a `max_tokens` limit, or stopped by an endpoint that
    trims, all read as a short answer and passed. What actually identifies a
    cut-off rationale is how it ends: mid-word, or mid-clause, or anywhere that
    is not the end of a sentence.

    Measured against 240 recorded rationales from an earlier corpus, this
    fires on exactly the three known-truncated ones and on nothing else, so
    the stricter rule costs no false rejections on real output. Measured
    again later across all three bake-off arms, against 6,181 real reasons
    and rationales and 74,172 constructed cuts of them: 99.5% recall at a
    0.1% false-positive rate, which no candidate replacement beat on both
    axes. The nearest rival, "the last word is not one the corpus uses",
    takes no false positives at all and finds barely half the cuts — a cut
    lands on a word boundary often enough that shape alone cannot see it.
    The predicate is right; where it is *asked* is what moved — see
    `_cap_field`, which gates it on the field's cap for the same reason
    `_check_reason` and `check_verdicts` used to: each field has exactly one
    truncation path and it lands on the cap. Pass B moved the call itself
    out of the semantic checks and into the pre-pass, but not the gate.

    An empty rationale is not this function's business; it is a missing answer
    rather than an interrupted one.
    """
    text = rationale.strip()
    return bool(text) and not FINISHED.search(text)


class RepeatFault(str):
    """A validation message about one claim restated at one place, and nothing else.

    A marker class rather than a suffix to grep for, on the same reasoning as
    `OrderFault`: the message reads like every other defect and reaches the
    model the same way, and the type exists only so `client.complete` can tell
    "the model is in a repetition loop" from "the model got a field wrong". The
    two call for a different number of attempts, and a string comparison would
    tie that decision to the wording of an error message.
    """


# How many claims one response may offer for one place before the response is
# read as a generation loop rather than as an extraction.
#
# ## The property, which is not a number
#
# A claim is evidence about a place in a document. The same claim text, offered
# again for the same line, carries no second piece of evidence: it is the
# response restating itself. A document that genuinely repeats a fact -- a
# changelog, a table of limits, a merge that concatenates two sources saying the
# same thing -- repeats it in *different places*, so honest repetition arrives as
# one claim per line and this counter never leaves 1. A loop arrives as one line
# counted hundreds of times. That is why the place is part of the key: the
# duplicate-claim check at the reconcile layer excludes same-line repeats for the
# opposite reason and both are right, because they are asking about different
# documents.
#
# ## The number, and the margin on both sides
#
# Measured over every decompose response recorded in this tree -- 1,359 of them,
# eleven models from qwen3:4b to claude-opus-5, gpt-5-1, kimi-k2 and
# deepseek-r1:70b, the largest 67 claims -- the deepest any clean response ever
# goes is **2**, on 9 responses of the 1,359. `tests/pairs/library_holds/ideal.md`,
# the near-total concatenation the operator has confirmed correct, has nine
# recorded decomposes across three models and reaches **1**. The degenerate
# response this guard was written for reached **450**: 489 claims of which 41
# were unique, one sentence 449 times on one line.
#
# So the limit is set at 8: four times the worst honest observation, and a
# fifty-sixth of the defect. It is deliberately not the midpoint of 2 and 450 --
# a threshold that splits the difference is fitted to the two measurements it
# was shown, and this project has twice shipped one of those. What the figure
# has to be is far enough above 2 that a model nobody has measured yet is not
# failed for restating a fact eight times, and far enough below 450 that a loop
# cannot hide under it. Both hold with an order of magnitude to spare, and
# `test_client.py` holds the low side against the recorded corpus rather than
# against this comment.
CLAIM_REPEAT_LIMIT = 8


def not_an_object(payload: object, wanted: str = "") -> list[str]:
    """The one complaint a response that is not a JSON object earns.

    Every semantic checker below reads its payload with `.get`, and a model
    that answers with a bare array -- an ordinary thing for a model to do --
    used to reach them as an `AttributeError` out of the parser rather than as
    a defect. A checker's contract is to return complaints, never to raise, so
    the shape fault is one of them: the run reaches the repair loop and the
    model is told which shape it should have answered in instead of the run
    ending on a traceback.

    Worded as `validate`'s type fault, because both reach the model through
    the same repair loop and a second vocabulary for one fault would read to
    it as two different faults. The checkers cannot simply defer to `validate`
    instead of carrying this: they are public, they are called directly, and a
    schema that does not state a top-level `type` gives the schema walk
    nothing to refuse -- which is exactly when the semantic check is the only
    thing left holding the shape.

    `wanted` names the key the shape is missing, because "expected object" on
    its own tells a model what it did and not what to do. Empty where the
    caller cannot name one, which is `parse` reading an arbitrary schema.
    """
    named = f" with a {wanted!r} key" if wanted else " with the keys the schema names"
    return [f"$: expected object, got {type(payload).__name__}; the response is "
            f"a JSON object{named}, not that value on its own"]


def _place(claim: dict) -> tuple[str, object]:
    """The (text, line) a claim is evidence about, normalised for comparison.

    Whitespace and case only, like `decompose.normalise`: values are untouched,
    because "512" and "512." are different claims and must stay so. `line` is
    taken raw rather than coerced -- a loop that emits no line at all still
    groups, under the same key, which is what a missing field should do here.
    """
    return re.sub(r"\s+", " ", str(claim.get("text", ""))).strip().lower(), claim.get("line")


def check_claims(payload: dict) -> list[str]:
    """Decompose output: every claim needs text, a span to anchor it, and a place of its own."""
    if not isinstance(payload, dict):
        return not_an_object(payload, "claims")
    errors: list[str] = []
    # The schema walk has already run and it requires every item to be an
    # object, so this list is the response as the caller will read it. Indices
    # are the payload's own, which is what `$.claims[i]` means to the model.
    claims = list(payload.get("claims", []))
    for i, claim in enumerate(claims):
        if not str(claim.get("text", "")).strip():
            errors.append(f"$.claims[{i}].text is empty")
        if not str(claim.get("span", "")).strip():
            errors.append(f"$.claims[{i}].span is empty; copy the sentence from the document")

    # Counted over the whole response before anything is reported, so the
    # message carries the full depth rather than the limit plus one: an operator
    # reading "450 times" knows what happened, and "9 times" would not say it.
    # Claims with no text are already reported above and are not counted here;
    # a blank repeated is a blank, not a loop.
    depth = Counter(_place(claim) for claim in claims if str(claim.get("text", "")).strip())
    repeats: list[str] = []
    for (text, line), count in depth.items():
        if count <= CLAIM_REPEAT_LIMIT:
            continue
        first = next(i for i, claim in enumerate(claims) if _place(claim) == (text, line))
        repeats.append(RepeatFault(
            f"$.claims[{first}] is repeated {count} times in this response, "
            f"every one of them for line {line!r}, and {len(claims)} claims were "
            f"returned in all. A line states a fact once, so one line cannot "
            f"yield the same claim more than "
            f"{CLAIM_REPEAT_LIMIT} times. Extract each fact once and stop."
        ))
    # Ahead of the field-level faults, not after them. `parse_error` quotes the
    # first five defects to the operator and the first ten to the model, and a
    # looping response can carry hundreds of other complaints; the fault that
    # ends the attempt ladder has to be one of the ones that gets said.
    return repeats + errors


# A resolver: given the `slot` string a decision names, how many candidates the
# source documents offered for it -- or None where that cannot be determined
# from the documents, which is not the same answer and must not be rounded to
# one. `merge.available_candidates` builds one.
AvailableCandidates = Callable[[str], int | None]


def _short_of_available(available: AvailableCandidates | None, record: dict) -> bool:
    """Is a decision naming one candidate short of what the documents offered?

    True keeps the error. `None` for the resolver, or `None` from it, keeps
    today's behaviour rather than silently passing: a slot that resolves to no
    heading in either document is not evidence of one candidate, it is evidence
    that the slot is not a heading, and a rule that read the two the same way
    would stop checking the case it was written for.
    """
    if available is None:
        return True
    offered = available(str(record.get("slot", "")))
    return offered is None or offered >= 2


def merge_checker(available: AvailableCandidates | None = None,
                  may_choose: bool | None = None):
    """`check_merge` with the documents' availability bound to it.

    `client.complete` takes `semantic` as a one-argument callable, so the
    resolver reaches the check by closure rather than by a second parameter
    threaded through the client.
    """
    return lambda payload: check_merge(payload, available, may_choose)


def check_merge(payload: dict, available: AvailableCandidates | None = None,
                may_choose: bool | None = None) -> list[str]:
    """Merge output: a document, and two record lists that are the right shape.

    A merge is a free-form string, so every content question about it — did a
    fact survive, was a value altered, was a disagreement surfaced — belongs to
    the verify pass and not here. The one case verify could not report honestly
    is an empty document: every claim would come back MISSING, and a coverage
    table showing 0/81 dropped facts is indistinguishable from a merge model
    that answered with "".

    An earlier version gave the merge two record lists as well, `open` added a third,
    and this function checks their *shape* and nothing else. **Where the line falls matters, because everything
    said here is fed back verbatim on retry and is therefore a prompt.** A
    replacement that does not resolve in the merged document, a segment id that
    was never issued, a disposition the active fidelity level does not permit —
    those are findings about the merge, decided by the reconciler, and asking
    the model to fix them would be the tool negotiating its own result away.
    What is repairable is a record that could not be read: a missing field, a
    value outside the closed set, a reason so long it was cut off, a replacement
    on a `dropped` or missing from anything else.

    The field-order checks exist because the schema only enforces order on a
    tier with grammar support, and the tier ladder is allowed to fall back.

    `available` answers "how many candidates did the *sources* offer for this
    slot?" and is what keeps the candidate-count check from charging the model
    for a choice the documents never offered. It is passed in rather than
    computed here because resolving a slot needs the segmenter and the
    reconciler, and this module imports neither -- it is a leaf, and a leaf that
    reaches upward is a cycle. `None` keeps the unconditional rule, so every
    caller that has no documents to hand is unaffected.
    """
    if not isinstance(payload, dict):
        return not_an_object(payload, "merged_document")
    errors = []
    if not str(payload.get("merged_document", "")).strip():
        errors.append(
            "$.merged_document is empty; return the whole merged document as a "
            "single string, with every fact from both sources in it"
        )

    seen: set[str] = set()
    for i, record in enumerate(payload.get("dispositions", [])):
        at = f"$.dispositions[{i}]"
        emitted = tuple(key for key in record if key in DISPOSITION_FIELDS)
        if emitted != DISPOSITION_FIELDS:
            errors.append(order_fault(
                f"{at} gives {', '.join(emitted) or 'nothing'}; give "
                f"{', '.join(DISPOSITION_FIELDS)}, in that order",
                emitted, DISPOSITION_FIELDS))

        segment = str(record.get("segment", "")).strip()
        if not segment:
            errors.append(f"{at}.segment is empty; name the segment id this record is about")
        elif segment in seen:
            errors.append(
                f"{at}.segment repeats {segment}; one record per departed segment, "
                f"and none at all for a segment carried over unchanged"
            )
        else:
            seen.add(segment)

        disposition = str(record.get("disposition", "")).strip()
        if disposition not in DISPOSITIONS:
            errors.append(
                f"{at}.disposition is {disposition or 'empty'!r}; use one of "
                f"{', '.join(DISPOSITIONS)}"
            )

        replacement = str(record.get("replacement", "")).strip()
        if disposition == "dropped" and replacement:
            errors.append(
                f"{at} is dropped and names a replacement; dropped means nothing "
                f"in the merge carries this content, so leave replacement empty"
            )
        elif disposition in REPLACED and not replacement:
            errors.append(
                f"{at} is {disposition} and names no replacement; copy the span of "
                f"your merged document that now carries this content"
            )

        errors += _check_reason(record, at)

    for i, record in enumerate(payload.get("decisions", [])):
        at = f"$.decisions[{i}]"
        wanted = decision_fields(may_choose)
        emitted = tuple(key for key in record if key in wanted)
        if emitted != wanted:
            errors.append(order_fault(
                f"{at} gives {', '.join(emitted) or 'nothing'}; give "
                f"{', '.join(wanted)}, in that order",
                emitted, wanted))
        if not str(record.get("slot", "")).strip():
            errors.append(f"{at}.slot is empty; name what was being chosen")
        # `chosen` is required where the level may choose and optional where it
        # may not. At `off`, `low` and `mid` the merge is forbidden to pick a
        # winner, so a decision record there is how a disagreement gets
        # recorded *without* one -- the slot and the candidates, and nothing
        # taken. Demanding `chosen` at those levels would make the only record
        # of a conflict impossible to emit, which is the gap this function closes.
        # `None` means the level was not threaded here, and then the strict
        # reading applies: a record with no choice is a record of nothing.
        if may_choose is not False and not str(record.get("chosen", "")).strip():
            errors.append(f"{at}.chosen is empty; give the candidate you took")

        candidates = record.get("candidates") or []
        # A decision is a record of a choice, so one candidate is not a
        # decision. This is shape rather than judgement: nothing here says which
        # candidate was right, only that a choice needs something to choose from.
        #
        # But "list every candidate the documents offered" is a demand about the
        # documents, and until `available` existed this function had no way to
        # read them -- so it charged the model whenever the count was short,
        # including when the sources offered exactly one. That was the dominant
        # attrition cause measured in one earlier run: five decisions rejected,
        # four of them on slots where a second candidate did not exist to be
        # named, exactly the false rejections `available` exists to prevent.
        #
        # Zero is still always an error: a decision that names nothing chose
        # nothing, whatever the documents held.
        if not candidates:
            errors.append(
                f"{at}.candidates is empty; a decision records a choice, so list "
                f"every candidate the documents offered"
            )
        elif len(candidates) < 2 and _short_of_available(available, record):
            errors.append(
                f"{at}.candidates has {len(candidates)}; a decision records a "
                f"choice, so list every candidate the documents offered"
            )
        for j, candidate in enumerate(candidates):
            emitted = tuple(key for key in candidate if key in CANDIDATE_FIELDS)
            if emitted != CANDIDATE_FIELDS:
                errors.append(order_fault(
                    f"{at}.candidates[{j}] gives {', '.join(emitted) or 'nothing'}; "
                    f"give {', '.join(CANDIDATE_FIELDS)}, in that order",
                    emitted, CANDIDATE_FIELDS))
            for name in CANDIDATE_FIELDS:
                if not str(candidate.get(name, "")).strip():
                    errors.append(f"{at}.candidates[{j}].{name} is empty")

        errors += _check_reason(record, at)

    # A third list, and only at a level whose schema offers the key. At
    # every other level `additions` is absent and this loop does not run, which
    # is why nothing here tests the fidelity: the schema has already decided
    # whether the model was allowed to speak, and a payload carrying the key
    # where it should not was rejected by `validate` before reaching this
    # function.
    #
    # Shape only, like the two loops above. Whether a declared statement is
    # *true* is the one question in this file that nothing can answer -- the
    # documents are all the tool checks against, and an addition is by
    # definition not in them.
    for i, record in enumerate(payload.get("additions", [])):
        at = f"$.additions[{i}]"
        emitted = tuple(key for key in record if key in ADDITION_FIELDS)
        if emitted != ADDITION_FIELDS:
            errors.append(order_fault(
                f"{at} gives {', '.join(emitted) or 'nothing'}; give "
                f"{', '.join(ADDITION_FIELDS)}, in that order",
                emitted, ADDITION_FIELDS))

        if not str(record.get("statement", "")).strip():
            errors.append(
                f"{at}.statement is empty; give the statement you added, copied "
                f"from your merged document. A declaration with nothing in it "
                f"declares nothing"
            )
        # `corrects` is deliberately not checked for emptiness. An addition may
        # extend documents that are thin rather than wrong, and a rule forcing
        # every one to name what it corrects would be a rule telling the model
        # to invent a victim.
        errors += _check_basis(record, at)
        errors += _check_reason(record, at)

    return errors


def _check_reason(record: dict, at: str) -> list[str]:
    """The `reason` both merge record types carry. Present, and that is all.

    Length used to be checked here too, both the over-cap case and the
    at-cap-and-cut-mid-sentence case `unfinished` finds. Both moved to
    `parsing.parse`'s pre-pass (`_truncate_capped_fields`), which runs before
    this function ever sees the record: a `reason` this function reads has
    already been capped to `REASON_MAX` if it needed to be, and the
    mid-sentence case is now a `Truncation`, not a defect, so a response is
    never rejected for a fault this pass already fixed.
    """
    reason = str(record.get("reason", "")).strip()
    if not reason:
        return [f"{at}.reason is empty; one sentence saying why"]
    return []


def _check_basis(record: dict, at: str) -> list[str]:
    """`basis` and `source`, and the dependency between them.

    Shape, like everything else this file checks. Whether a cited source says
    what the record claims it says is unanswerable here and unanswerable
    anywhere in this package: nothing opens a socket, so no citation is ever
    resolved, fetched or checked. What is checkable is that the model has
    said which of two quite different things it is doing.

    The dependency runs both ways and both halves matter.

    `citation` with nothing in `source` is a record claiming a reader can go
    and check it while naming nothing to check -- the worst of the two
    failures, because the word `citation` is what a reader weighs.

    `own-knowledge` with something in `source` is the failure this field was
    built to stop, arriving one step later. A model that has answered "no
    source" and then writes a URL beside it has produced exactly the artefact
    the enum exists to prevent, and letting it through would make the enum
    decorative. Both are repairable by rewriting the record, which is the test
    for whether a check belongs in this file at all.
    """
    basis = str(record.get("basis", "")).strip()
    source = str(record.get("source", "")).strip()
    if basis not in BASES:
        return [
            f"{at}.basis is {basis!r}; give one of {', '.join(BASES)}. Use "
            f"{CITATION!r} when you can name something a reader could go and "
            f"look at, and {OWN_KNOWLEDGE!r} when you are going on what you "
            f"know. {OWN_KNOWLEDGE!r} is a complete answer and the expected "
            f"one -- do not name a source you are not sure exists"
        ]
    if basis == CITATION and not source:
        return [
            f"{at}.source is empty under basis {CITATION!r}; name the source "
            f"-- a URL, a specification and section, a title and date. If you "
            f"cannot name one, the basis is {OWN_KNOWLEDGE!r}"
        ]
    if basis == OWN_KNOWLEDGE and source:
        return [
            f"{at}.source is filled under basis {OWN_KNOWLEDGE!r}; leave it "
            f"empty. {OWN_KNOWLEDGE!r} means there is nothing for a reader to "
            f"go and look at, and a source written beside it says the opposite"
        ]
    return []


def check_coverage(payload: dict, sources: tuple[str, ...] = (),
                   fidelity: str = "off") -> list:
    """The fused pass's output: a claim that is also a verdict.

    Both halves are checked by the checks that already own them rather than by
    a third implementation -- `check_claims` for text, span and the repetition
    limit, and the same field-order rule `check_verdicts` applies, read off
    `COVERAGE_FIELDS`. A second implementation of a check is a second answer.

    **The verdict half is the same verdict half, and it was not checked at
    all.** This function used to stop at "a verdict is present", so every rule
    `verdict_defects` applies to the label and to the evidence coupling went
    unapplied at `--verify-depth coverage`: a SUPPORTED with no span, a
    SUPPORTED naming no file, a span attributed to a document the model was
    never given, a MISSING quoting evidence. The consequence was not a missing
    warning but a *better* result -- the same reply scored `grounded` here and
    `attribution_error` at `full`, and "evidence grounded" is a ratio this
    tool publishes. The cheaper depth is allowed to ask fewer questions; it is
    not allowed to mark the ones it does ask more leniently.

    `sources` and `fidelity` are threaded for the reasons `check_verdicts`
    gives, and the second one is not optional in practice: `evidenced_for`
    adds DERIVED at `high` and `open`, so a caller that drops the level would
    demand a span for a label the level does not even have. Both default the
    strict way -- no filenames means shape-only, `off` means the narrow label
    set -- so a caller that forgets them checks more, never less.
    """
    if not isinstance(payload, dict):
        return not_an_object(payload, "claims")
    errors = list(check_claims(payload))
    for i, record in enumerate(payload.get("claims", [])):
        if not isinstance(record, dict):
            continue
        at = f"$.claims[{i}]"
        label = str(record.get("verdict", "")).strip()
        allowed = verdicts_for(fidelity)
        if not label:
            errors.append(f"{at}.verdict is empty; every claim this "
                          f"pass extracts is also judged, and an unjudged "
                          f"claim is indistinguishable from one it never found")
        elif label not in allowed:
            errors.append(
                f"{at}.verdict is {label!r}; must be one of {', '.join(allowed)}")
        else:
            errors.extend(_check_evidence(at, label, record, sources, fidelity))
        emitted = tuple(k for k in record if k in COVERAGE_FIELDS)
        if emitted != COVERAGE_FIELDS:
            errors.append(order_fault(
                f"{at} gives {', '.join(emitted) or 'nothing'}; give "
                f"{', '.join(COVERAGE_FIELDS)}, in that order",
                emitted, COVERAGE_FIELDS))
    return errors


def check_verdicts(payload: dict, sources: tuple[str, ...] = (),
                   fidelity: str = "off") -> list[str]:
    """Verify output: closed label set, unique ids, evidence where it is owed.

    `sources` is the filenames the prompt handed the model. Empty means the
    caller had none to give, and `evidence_source` is then checked for shape
    only — never silently accepted as correct.

    Everything here is repairable by rewriting the response, and none of it
    tells the model which label to pick. That line matters: this function's
    errors are fed back verbatim on retry, so anything said here is a prompt.
    An error saying "you answered MISSING but quoted a span" is a request to
    make the answer self-consistent; it does not say which half to change. See
    `rationale_conflicts` for the check that deliberately does not go here.

    Nothing is ever coerced. An inconsistent result is an error and goes back
    for repair; filling in the field the model left out would be the tool
    deciding the finding, which is the one thing it must not do.
    """
    return [error for _, error in verdict_defects(payload, sources, fidelity)[0]]


def verdict_defects(
    payload: dict, sources: tuple[str, ...] = (), fidelity: str = "off"
) -> tuple[list[tuple[int | None, str]], set[int]]:
    """`check_verdicts`, with each defect kept next to the record that caused it.

    Same checks, same messages, same order — the only difference is that every
    defect arrives paired with the index of the verdict it belongs to, or
    `None` where it belongs to the response as a whole. `check_verdicts` is the
    flattening of this and is what the repair loop still uses, so nothing about
    what gets sent back to a model changes here.

    The pairing is what Pass C reads. A defect with
    an index is a fault in one record and says nothing about the other records
    in the batch; a defect with `None` is a fault in the answer as a whole, and
    no subset of it can be trusted. Deriving that split here, from the check
    that raised the defect, is the point: recovering it downstream would mean
    parsing `$.verdicts[7]` back out of an English sentence, and a message
    reworded for a model would silently change what the tool grades.

    Only one defect is response-level today — the field-order fault, which
    `parse` already handles as a class of its own (`order_only`, no retry) and
    which `--field-order any` is the sole supported way to accept. Everything
    else here is a property of one record.

    The second return value holds the positions that are unusable *without* a
    message of their own: today, the first copy of a duplicated `claim_id`,
    whose message is emitted at the second copy. It is returned apart rather
    than given an invented message because the messages here are a prompt —
    they go back to the model verbatim on retry — and adding a sentence to
    that prompt to carry an internal bookkeeping fact would change what the
    model is asked, to say something it has already been told.
    """
    if not isinstance(payload, dict):
        # Response-level, so `None`: there is no record to blame a payload
        # that has no records for Pass C to salvage around.
        return [(None, message) for message in not_an_object(payload, "verdicts")], set()
    defects: list[tuple[int | None, str]] = []
    seen: dict[str, int] = {}
    duplicated: set[int] = set()
    for i, verdict in enumerate(payload.get("verdicts", [])):
        claim_id = str(verdict.get("claim_id", "")).strip()
        if not claim_id:
            defects.append(
                (i, f"$.verdicts[{i}].claim_id is empty; echo the id you were given"))
        elif claim_id in seen:
            defects.append((i, f"$.verdicts[{i}].claim_id {claim_id!r} appears twice"))
            # Both copies, not just the second. Which of the two was meant for
            # the claim is exactly what cannot be told from here, and picking
            # the earlier one because it came first would be the tool deciding
            # the verdict -- the one thing `check_verdicts` says it must not do.
            duplicated.update((seen[claim_id], i))
        else:
            seen[claim_id] = i

        emitted = tuple(k for k in verdict if k in VERDICT_FIELDS)
        if emitted != VERDICT_FIELDS:
            defects.append((None, order_fault(
                f"$.verdicts[{i}] emits {', '.join(emitted)}; emit exactly "
                f"{', '.join(VERDICT_FIELDS)}, in that order",
                emitted, VERDICT_FIELDS)))

        label = verdict.get("verdict")
        allowed = verdicts_for(fidelity)
        if label not in allowed:
            defects.append((
                i,
                f"$.verdicts[{i}].verdict is {label!r}; must be one of {', '.join(allowed)}"
            ))
        else:
            defects.extend(
                (i, error)
                for error in _check_evidence(
                    f"$.verdicts[{i}]", label, verdict, sources, fidelity))

    return defects, duplicated


def _check_evidence(
    at: str, label: str, verdict: dict, sources: tuple[str, ...],
    fidelity: str = "off"
) -> list[str]:
    """evidence and evidence_source are present together or absent together.

    Which one it is follows from the label and nothing else. SUPPORTED,
    CONTRADICTED and PARTIAL all assert the reference text says something, so
    all three owe the span and the file it came from. MISSING asserts the
    opposite, and a span quoted in support of an absence is not evidence of
    anything — it is a result whose two halves disagree, and there is no way to
    tell from here which half the model meant.

    PARTIAL owes its span for a second reason on top of that one. The span is
    what makes the verdict reviewable: it is the difference between "part of
    this is stated" and a pointer to *which* part, and only the second can be
    checked by the person reading the report.

    `at` is the path of the record being judged rather than an index, because
    the fused coverage pass keeps these four fields under `$.claims[i]` while
    the unfused one keeps them under `$.verdicts[i]`. The rules do not differ
    by which list a record arrived in, and the one thing that must never
    differ is *which* rules ran: `check_coverage` reached this function through
    nothing at all until a later fix, so a coverage run graded an unattributed
    span as grounded and a `full` run over the same reply called it an
    attribution error. Parameterising the path is what makes one
    implementation serve both; a second copy would be a second answer.
    """
    errors = []
    evidence = str(verdict.get("evidence", "")).strip()
    named = str(verdict.get("evidence_source", "")).strip()

    if label in evidenced_for(fidelity):
        if not evidence:
            errors.append(
                f"{at} is {label} but quotes no evidence; quote the "
                f"exact span of the reference text that makes it {label}"
            )
        if not named:
            errors.append(
                f"{at} is {label} but names no evidence_source; give "
                f"the filename you quoted from"
            )
        elif sources and named not in sources:
            errors.append(
                f"{at}.evidence_source is {named!r}, which was not one "
                f"of the documents you were given; use one of {', '.join(sources)}"
            )
    else:
        if evidence:
            errors.append(
                f"{at} is MISSING but quotes evidence; MISSING means "
                f"the reference text does not state the claim, so leave evidence "
                f"empty, or change the verdict to match what you quoted"
            )
        if named:
            errors.append(
                f"{at} is MISSING but names {named!r} as evidence_source; "
                f"leave evidence_source empty for MISSING"
            )
    return errors


def rationale_conflicts(payload: dict) -> list[str]:
    """Verdicts whose rationale names a label other than the one in `verdict`.

    Deliberately **not** part of check_verdicts, and so deliberately not part of
    the retry loop. Every other semantic error is quoted back to the model to
    repair, and repairing this one would mean telling a model that has answered
    MISSING that its own reasoning says CONTRADICTED. It would change its
    answer, and the changed answer would then be scored — a nudge toward
    whichever label the grader wanted, inside the corpus built to measure what
    the model does unprompted.

    So it is a diagnostic. The run surfaces it, the number moves for nobody, and
    a human reads it: a model that reasons its way to one label and reports
    another is telling you something about the prompt that its accuracy figure
    is not.
    """
    conflicts = []
    for i, verdict in enumerate(payload.get("verdicts", [])):
        named = conflicting_labels(
            verdict.get("verdict"), str(verdict.get("rationale", ""))
        )
        if named:
            conflicts.append(
                f"$.verdicts[{i}] is {verdict.get('verdict')} but its rationale "
                f"names {', '.join(named)}"
            )
    return conflicts


def conflicting_labels(label: object, rationale: str) -> tuple[str, ...]:
    """Which other verdict labels this rationale names. Empty means consistent.

    Case-sensitive on purpose. The labels are uppercase tokens, so this matches
    a model citing the vocabulary and not one writing the English word — "the
    value is missing from the reference text" is a rationale for MISSING, not a
    conflict with it.
    """
    if label not in VERDICTS:
        return ()
    return tuple(other for other in VERDICTS if other != label and other in rationale)


@dataclass(frozen=True)
class Truncation:
    """A field that was over its cap, or exactly at it and cut mid-sentence.

    `path` names the field the way an error message would
    (`$.dispositions[0].reason`). `original_length` is what the model wrote
    before this pass touched it, kept so a report can say how far over the
    model went rather than just that it went over.
    """

    path: str
    original_length: int
    cap: int


def _cap_field(record: dict, field: str, cap: int, at: str, *,
                anchor_fn: Callable[[str], str] | None = None) -> Truncation | None:
    """Cap `record[field]` in place if it needs it, and say so if it did.

    Three outcomes: under the cap and untouched; over the cap and truncated
    (`anchor_fn` if the field has a two-ended form, a hard cut otherwise); or
    exactly at the cap and cut mid-sentence, which is not this pass's doing
    and is not mutated, only reported, since there is nothing left to trim. A
    non-string value is left for `validate` to reject; this only ever
    shortens a string that is already the right type.
    """
    value = record.get(field)
    if not isinstance(value, str):
        return None
    if len(value) > cap:
        record[field] = anchor_fn(value) if anchor_fn is not None else value[:cap]
        return Truncation(f"{at}.{field}", len(value), cap)
    if anchor_fn is None and len(value) == cap and unfinished(value):
        return Truncation(f"{at}.{field}", len(value), cap)
    return None


def _truncate_capped_fields(payload: dict) -> list[Truncation]:
    """Every over-cap or cut-mid-sentence field, capped in place, and logged.

    Run before `validate`, so a field this pass has already shortened never
    reaches the schema's `maxLength` check, and a response is never rejected
    for a fault this function has just fixed. `replacement` is capped with
    `anchor`, the two-ended form the prompt already documents; `reason` and
    `rationale` have no such form and are cut hard, which is why only they
    are also checked for landing on the cap mid-sentence — `anchor` has no
    mid-sentence failure mode of its own to detect.

    Silent about shapes it does not recognise: a payload missing
    `dispositions`, `decisions` or `verdicts` entirely, or a record that is
    not a dict, is `decompose`'s or a malformed response's business, not
    this pass's.
    """
    if not isinstance(payload, dict):
        # A response that is not an object at all, which is the widest case of
        # the shape this pass is already silent about. Nothing here can be
        # capped and the fault is `parse`'s to report.
        return []
    truncations: list[Truncation] = []
    for i, record in enumerate(payload.get("dispositions") or []):
        if not isinstance(record, dict):
            continue
        at = f"$.dispositions[{i}]"
        capped = _cap_field(record, "replacement", REPLACEMENT_MAX, at, anchor_fn=anchor)
        if capped is not None:
            truncations.append(capped)
        capped = _cap_field(record, "reason", REASON_MAX, at)
        if capped is not None:
            truncations.append(capped)
    for i, record in enumerate(payload.get("decisions") or []):
        if not isinstance(record, dict):
            continue
        capped = _cap_field(record, "reason", REASON_MAX, f"$.decisions[{i}]")
        if capped is not None:
            truncations.append(capped)
    # `statement` is cut hard rather than anchored, unlike `replacement`.
    # Both are pieces of the merged document, but they are read differently:
    # a replacement is *located* in it, where a statement is matched against
    # the claims decomposed from it. An anchored form elides the middle, and
    # a claim drawn from that middle would stop matching -- so the two-ended
    # form would quietly narrow what a declaration covers instead of
    # shortening it. A hard cut narrows it too, and says so in a Truncation.
    for i, record in enumerate(payload.get("additions") or []):
        if not isinstance(record, dict):
            continue
        at = f"$.additions[{i}]"
        capped = _cap_field(record, "statement", REPLACEMENT_MAX, at)
        if capped is not None:
            truncations.append(capped)
        # `source` is capped here for the reason every other free-text field
        # is: a vendor enforcing `maxLength` during constrained decoding cuts
        # mid-word in silence, and a half URL that nobody said was cut reads
        # as a source the tool mangled rather than one the model overran.
        capped = _cap_field(record, "source", SOURCE_MAX, at)
        if capped is not None:
            truncations.append(capped)
        capped = _cap_field(record, "reason", REASON_MAX, at)
        if capped is not None:
            truncations.append(capped)
    # The merge's mismatch warning, capped and declared rather than clipped in
    # silence. A vendor enforcing `maxLength` cuts mid-word and hands
    # back a sentence that reads as a fault in the tool; cutting it here logs
    # a `Truncation` the report can show, and the schema's larger cap now
    # makes reaching it unlikely rather than routine.
    said = payload.get("mismatch")
    if isinstance(said, str):
        capped = _cap_field(payload, "mismatch", MISMATCH_MAX, "$")
        if capped is not None:
            truncations.append(capped)
    for i, record in enumerate(payload.get("verdicts") or []):
        if not isinstance(record, dict):
            continue
        capped = _cap_field(record, "rationale", RATIONALE_MAX, f"$.verdicts[{i}]")
        if capped is not None:
            truncations.append(capped)
    # The coverage pass puts its rationales under `claims`, not `verdicts`,
    # because one record carries both halves. Reaching them from here rather
    # than from a second pre-pass is the point: a field with a `maxLength` in
    # the schema and no cap here is a field a vendor clips mid-word in silence,
    # and that has already happened once.
    for i, record in enumerate(payload.get("claims") or []):
        if not isinstance(record, dict) or "rationale" not in record:
            continue
        capped = _cap_field(record, "rationale", RATIONALE_MAX, f"$.claims[{i}]")
        if capped is not None:
            truncations.append(capped)
    return truncations


def forgiven(errors: list, field_order: str = DEFAULT_FIELD_ORDER) -> list:
    """Drop the faults `field_order` says are not faults. One rule, two readers.

    `parse` applies it to both the schema walk and the semantic check, and
    `client.complete` applies it again to decide which of those two stages a
    non-empty defect list came from. That decision has to use the same rule
    parse used or it reads the wrong stage, so the rule lives here rather than
    once inside each caller.
    """
    if field_order != "any":
        return errors
    return [error for error in errors if not isinstance(error, OrderFault)]


def parse(text: str, schema: dict, semantic=None, *,
          field_order: str = DEFAULT_FIELD_ORDER,
          ) -> tuple[dict, list[str], list[Truncation]]:
    """The whole of PART C. Returns `(payload, defects, truncations)`.

    Raises nothing of its own — `defects` is empty on a clean response and
    non-empty otherwise, and it is the caller's job to decide what a non-empty
    list means. Every caller today raises `ParseError` on any defect at all,
    so today's observable behaviour is unchanged; `defects` exists so a future
    caller can act on a subset of the list instead of the whole thing.

    `truncations` is a record of every field `_truncate_capped_fields` had to
    shorten before validation ran, in payload order. It is never a defect: a
    length violation stops being fatal here, which is the whole point of
    Pass B — the document, and the record naming it, both survive; only
    the field that overran its cap is capped and logged. Empty on a
    response that needed no capping.

    Under `field_order="any"` an order fault is not a fault: the message is
    dropped before anything is counted, so a record whose keys are shuffled and
    otherwise complete goes on to the semantic checks like any other. Nothing
    else is relaxed. `order_fault` has already ruled out the record that is
    shuffled *and* short of a field, so what gets dropped here is only ever a
    sequence, never a value.
    """
    def allowed(found):
        return forgiven(found, field_order)

    payload = loads(text)
    # A response that is not a JSON object at all stops here. Everything
    # below reads the payload with `.get` -- the capping pre-pass first, then
    # the schema walk's property loop, then the semantic checker -- so a model
    # that answered with a bare array used to leave this function as an
    # `AttributeError` three frames down instead of as a defect. It is an
    # ordinary thing for a model to produce and the repair loop is what it is
    # owed: returning the fault sends the shape back to the model to fix.
    #
    # The schema walk's own type fault where the schema states a top-level
    # type, which is every schema this project emits, so the model sees one
    # wording and not two. `not_an_object` covers the schema that does not.
    # The payload itself is dropped rather than returned: the caller raises on
    # any defect, and `parse` promises a dict.
    if not isinstance(payload, dict):
        return {}, allowed(validate(payload, schema)) or not_an_object(payload), []
    truncations = _truncate_capped_fields(payload)
    # Both sources, because both check order: the schema walk orders the top
    # level and `semantic` orders the records inside it, and the switch that
    # forgave one and not the other would be a switch that forgives nothing a
    # real model does.
    errors = allowed(validate(payload, schema))
    if not errors and semantic is not None:
        errors = allowed(semantic(payload))
    assert isinstance(payload, dict)
    return payload, errors, truncations


def parse_error(schema: dict, errors: list[str]) -> ParseError:
    """The `ParseError` `parse()` used to raise directly, built from its `defects`."""
    listed = "; ".join(errors[:5])
    return ParseError(
        f"response does not match the schema: {listed}",
        "Your previous response was rejected:\n"
        + "\n".join(f"- {error}" for error in errors[:10])
        + "\n\nReply again with JSON matching this schema exactly, and nothing else:\n"
        + json.dumps(schema, indent=2),
        # Over every fault, not the five that get quoted: a
        # response is only in the wrong order if nothing else is wrong
        # with it.
        order_only=all(isinstance(error, OrderFault) for error in errors),
        looping=any(isinstance(error, RepeatFault) for error in errors),
    )
