#!/usr/bin/env python3
"""Two implementations of one contract, and the assertions that keep them in step.

Run directly:

    python3 tests/test_contract_parity.py

Exits 0 when every check passes, 1 otherwise. Stdlib only, no network, no model
call.

Every defect found in this repository in the two days before this file was
written had one shape: **two things that must agree, with nothing asserting that
they do.** `parsing.check_coverage` applied three of the rules
`parsing.verdict_defects` applies, so one model reply scored `grounded` at one
verification depth and `attribution_error` at the other. The clean verdict ruled
out invention over a run with no reverse pass; it was fixed on the web page and
left wrong in the Markdown report, the HTML report and the terminal, all three of
which share one function. A sentence the report and the page are meant to say in
the same words was asserted equal for one pair and left unasserted for the rest.

None of those is a missing test of a function, and volume does not find them --
this repository already carries more test than source. Each is a missing test
*between* two functions. So nothing here checks that a rule is right. Everything
here checks that two places which must say the same thing do.

**The seed that matters is deleting a rule from one side only.** A parity test
that stays green under that is decoration, so the matrix below is guarded from
both ends:

  - every shared rule must fire on *both* paths at least once across the matrix,
    which is what goes red when a rule is deleted from the shared implementation
    or is made unreachable from one caller;
  - every message either path emits must be classified by the registry, which is
    what goes red when a rule is *added* to one path alone.

Neither of those is a coverage number. They are registrations: the property is
named before the run, and an unregistered firing is a failure rather than a
line in a report nobody reads.

Offline throughout, and by construction rather than by stubbing: the inputs are
malformed records built here and `Run`s built by hand. What is under test is
agreement between two checkers and between four renderers, and a fixture
produced by a model would make that agreement move for reasons that have nothing
to do with either.
"""

from __future__ import annotations

import ast
import html as html_entities
import io
import json
import re
import sys
from dataclasses import dataclass, field
from types import SimpleNamespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# This module opens no socket. Same reasoning as its neighbours: the guard turns
# that sentence into something that fails when it stops being true.
socket_guard.install()

from llossless import (  # noqa: E402
    cli, config, html_report, parsing, prompts, report, usage,
)
from llossless import merge as merge_module  # noqa: E402
from llossless.decompose import Claim  # noqa: E402
from llossless import reconcile as reconcile_module  # noqa: E402
from llossless.reconcile import Finding, Reconciled  # noqa: E402
from llossless.report import Run, Step  # noqa: E402
from llossless.verify import (  # noqa: E402
    GROUNDED,
    MERGED,
    MERGED_TO_SOURCES,
    NOT_GRADED,
    SOURCE_TO_MERGED,
    Verdict,
)

PARSING = ROOT / "src" / "llossless" / "parsing.py"
APP_JS = ROOT / "src" / "llossless" / "web" / "static" / "app.js"
EN = ROOT / "src" / "llossless" / "web" / "locales" / "en.json"

failures: list[str] = []
notes: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# 1. the verification contract: one record, two checkers
# --------------------------------------------------------------------------

# Which of the two lists a rule belongs to. `BOTH` is the parity set -- a rule
# either path applies to a verdict half, and therefore a rule the other path
# must apply to the same verdict half. The other two are the rules that are
# path-specific *by contract*, not by accident: a coverage record has no
# `claim_id` (claims come back in document order and are numbered by position)
# and a verdict record has no `text`, `line` or `span` of its own.
#
# The distinction is written down rather than inferred, because "this rule fires
# on one path only" is exactly what the defect looks like, and a test that
# decided for itself which of those was fine would decide the thing it is here
# to check.
BOTH, VERDICTS_ONLY, CLAIMS_ONLY = "both", "verdicts", "claims"


@dataclass(frozen=True)
class Rule:
    """One rule of the verify contract, and how to recognise it being raised.

    `markers` are matched against the message rather than against the code
    because the message is the artefact both paths produce and the only thing a
    caller can compare. `order_fault` discriminates the two field-order results:
    `parsing.order_fault` returns an `OrderFault` when the fields were merely
    shuffled and a plain string when one is missing, and `parse` treats those
    differently -- a shuffle is not retried, a missing field is. Two paths that
    raised different *types* for one record shape would send one of them back to
    the model and not the other, which is a parity failure a message comparison
    alone would miss.
    """

    id: str
    paths: str
    markers: tuple[str, ...]
    order_fault: bool | None = None

    def matches(self, message: str) -> bool:
        if not any(marker in message for marker in self.markers):
            return False
        if self.order_fault is None:
            return True
        return isinstance(message, parsing.OrderFault) is self.order_fault


# The registry. Every rule either checker applies, with the list it belongs to.
#
# Adding a rule to `parsing` without adding it here fails
# `test_every_defect_message_is_classified`, which is the point: the registry is
# the place where somebody has to say, out loud, whether a new rule belongs to
# one path or to both. That sentence is the whole defence. A rule that arrives
# with no entry here is a rule nobody decided the scope of.
RULES = (
    Rule("label", BOTH,
         ("must be one of", ".verdict is empty;")),
    Rule("evidence-missing", BOTH, ("quotes no evidence",)),
    Rule("evidence-source-missing", BOTH, ("names no evidence_source",)),
    Rule("evidence-source-unknown", BOTH,
         ("was not one of the documents you were given",)),
    Rule("evidence-under-missing", BOTH, ("but quotes evidence",)),
    Rule("evidence-source-under-missing", BOTH, ("as evidence_source",)),
    Rule("field-order", BOTH, ("in that order",), order_fault=True),
    Rule("field-incomplete", BOTH, ("in that order",), order_fault=False),
    Rule("claim-id-missing", VERDICTS_ONLY, ("claim_id is empty",)),
    Rule("claim-id-duplicate", VERDICTS_ONLY, ("appears twice",)),
    Rule("claim-text-missing", CLAIMS_ONLY, (".text is empty",)),
    Rule("claim-span-missing", CLAIMS_ONLY, (".span is empty",)),
    Rule("claim-repeated", CLAIMS_ONLY, ("is repeated",)),
)


@dataclass(frozen=True)
class Row:
    """One deliberately malformed record, in the shape both checkers take.

    `half` is the verdict half and is shared byte for byte between the two
    payloads. That is what makes the comparison meaningful: the records differ
    only in the fields the two contracts genuinely do not share, so a difference
    in what is raised is a difference in the rules, never in the input.
    """

    name: str
    half: dict
    reorder: bool = False
    drop: tuple[str, ...] = ()
    copies: int = 1
    same_id: bool = False
    blank_anchor: bool = False


# The anchor fields a coverage record carries and a verdict record does not.
ANCHOR = {"text": "The kiln fired for eleven hours.", "line": 1,
          "span": "The kiln fired for eleven hours."}
SUPPLIED = ("merged.md",)


def evidenced(label: str = "SUPPORTED", **over) -> dict:
    half = {"verdict": label, "evidence": "The kiln fired for eleven hours",
            "evidence_source": "merged.md", "rationale": "Stated in the merge."}
    half.update(over)
    return half


def absent(**over) -> dict:
    half = {"verdict": "MISSING", "evidence": "", "evidence_source": "",
            "rationale": "Absent from the merge."}
    half.update(over)
    return half


ROWS = (
    # The two clean shapes. A parity test whose every row is malformed proves
    # only that two checkers complain together; these prove they stay quiet
    # together, which is the half that a checker made stricter on one path alone
    # would break.
    Row("clean-evidenced", evidenced()),
    Row("clean-missing", absent()),
    Row("evidenced-without-evidence", evidenced(evidence="")),
    Row("evidenced-without-source", evidenced(evidence_source="")),
    Row("evidenced-naming-a-document-not-supplied",
        evidenced(evidence_source="notes-c.md")),
    Row("missing-quoting-evidence", absent(evidence="The kiln fired")),
    Row("missing-naming-a-source", absent(evidence_source="merged.md")),
    Row("empty-verdict", evidenced(label="")),
    Row("unknown-verdict", evidenced(label="PROBABLY")),
    # DERIVED is the level-dependent label: a member of the vocabulary at `high`
    # and `open` and outside it everywhere else (`parsing.DERIVES`), and it owes
    # a span at the levels that have it (`parsing.evidenced_for`). Both paths
    # have to agree about that twice over -- about the vocabulary and about the
    # span -- which is why it gets two rows and why the whole matrix runs at
    # every level.
    Row("derived", evidenced(label="DERIVED")),
    Row("derived-without-evidence", evidenced(label="DERIVED", evidence="")),
    Row("fields-in-the-wrong-order", evidenced(), reorder=True),
    Row("a-field-missing-entirely", evidenced(), drop=("evidence_source",)),
    Row("blank-anchor", evidenced(), blank_anchor=True),
    Row("the-same-record-twice", evidenced(), copies=2, same_id=True),
    Row("one-place-many-claims", evidenced(),
        copies=parsing.CLAIM_REPEAT_LIMIT + 1),
)


def shaped(record: dict, fields: tuple[str, ...], row: Row) -> dict:
    """One record, with `row`'s mutations applied in the contract's own order.

    Key order is what the field-order rule reads, so it is built rather than
    left to the order the literals happened to be written in.
    """
    for name in row.drop:
        record.pop(name, None)
    keys = [key for key in fields if key in record]
    if row.reorder:
        keys.reverse()
    return {key: record[key] for key in keys}


def verdict_payload(row: Row) -> dict:
    records = []
    for index in range(row.copies):
        record = {"claim_id": "" if row.blank_anchor
                  else f"C-{1 if row.same_id else index + 1:03d}"}
        record.update(row.half)
        records.append(shaped(record, parsing.VERDICT_FIELDS, row))
    return {"verdicts": records}


def coverage_payload(row: Row) -> dict:
    records = []
    for _ in range(row.copies):
        record = dict(ANCHOR)
        if row.blank_anchor:
            record.update({"text": "", "span": ""})
        record.update(row.half)
        records.append(shaped(record, parsing.COVERAGE_FIELDS, row))
    return {"claims": records}


def classify(message: str) -> tuple[str, ...]:
    """Which rules this message belongs to. One, or the test says so."""
    return tuple(rule.id for rule in RULES if rule.matches(message))


def fired(messages, paths: str | None = None) -> set[str]:
    """The rule ids these messages raised, optionally filtered to one list."""
    ids = set()
    for message in messages:
        for rule in RULES:
            if rule.matches(message) and (paths is None or rule.paths == paths):
                ids.add(rule.id)
    return ids


def both_paths(row: Row, level: str, sources: tuple[str, ...]):
    """The same row down both checkers. Returns the two message lists."""
    defects, _ = parsing.verdict_defects(verdict_payload(row), sources, level)
    return ([message for _, message in defects],
            list(parsing.check_coverage(coverage_payload(row), sources, level)))


def test_the_two_checkers_raise_the_same_shared_rules() -> None:
    """The defect this module exists for, stated as a set comparison.

    `check_coverage` reached `_check_evidence` through nothing at all until
    a fix landed: a SUPPORTED with no span, a span attributed to a document the
    model was never given and a MISSING quoting evidence were all defects at
    `--verify-depth full` and none of them at `coverage`. The consequence was
    not a missing warning but a *better* result -- the same reply scored
    `grounded` on the cheap path -- and "evidence grounded" is a ratio this tool
    publishes.

    The fix was to parameterise the record's path so one implementation serves
    both callers. Nothing asserted that it stays that way, and a second copy of
    a check is a second answer, so this is the assertion: for one record shape,
    the set of shared rules raised is the same down both paths.

    Run at every fidelity level and with and without the filenames, because both
    change what the rules mean -- `evidenced_for` adds DERIVED at `high` and
    `open`, and an empty `sources` makes `evidence_source` a shape check rather
    than a membership one. A parity that held at `off` alone would be a parity
    that held where the vocabulary is smallest.
    """
    compared = 0
    for level in config.FIDELITY_LEVELS:
        for sources in ((), SUPPLIED):
            for row in ROWS:
                verdicts, claims = both_paths(row, level, sources)
                left, right = fired(verdicts, BOTH), fired(claims, BOTH)
                compared += 1
                check(left == right,
                      f"{row.name} at fidelity {level} with "
                      f"{len(sources)} filename(s): the verdict path raises "
                      f"{sorted(left) or ['nothing']} and the coverage path "
                      f"raises {sorted(right) or ['nothing']}. A rule one path "
                      f"applies and the other does not is the whole reason "
                      f"this file exists.")
    notes.append(f"contract parity: {compared} record shapes compared down "
                 f"both checkers")


def test_every_shared_rule_fires_on_both_paths() -> None:
    """The registration. A rule nothing exercises is a rule nothing protects.

    Set equality between two paths is satisfied by two paths that raise nothing
    at all, so deleting a rule from `_check_evidence` -- which both callers now
    share -- leaves the comparison above perfectly green. This is the half that
    catches it: every rule in the registry must fire, on every list it is
    declared to belong to, somewhere in the matrix.

    It is a must-fire probe in the sense this project means it (`scanners need
    seeded positives`), and it fails in both directions. A registry entry for a
    rule that no longer exists goes red here too, which is what stops the
    registry silently becoming a list of rules that used to be.
    """
    seen: dict[str, set[str]] = {rule.id: set() for rule in RULES}
    for level in config.FIDELITY_LEVELS:
        for sources in ((), SUPPLIED):
            for row in ROWS:
                verdicts, claims = both_paths(row, level, sources)
                for rule_id in fired(verdicts):
                    seen[rule_id].add("verdicts")
                for rule_id in fired(claims):
                    seen[rule_id].add("claims")
    for rule in RULES:
        want = {"verdicts", "claims"} if rule.paths == BOTH else {rule.paths}
        check(seen[rule.id] == want,
              f"rule {rule.id!r} is registered for {sorted(want)} and fired on "
              f"{sorted(seen[rule.id]) or ['nothing']}. Either the matrix no "
              f"longer reaches it -- in which case the parity check above is "
              f"green over a rule it never exercised -- or the rule is gone.")


def test_every_defect_message_is_classified() -> None:
    """A rule added to one path alone, caught before anyone has to notice it.

    The set comparison can only compare rules it knows about. A new check in
    `verdict_defects` with no counterpart in `check_coverage` would raise a
    message this registry does not recognise, both sets would come back
    unchanged, and the comparison would pass over the exact defect it was
    written for.

    So an unrecognised message is a failure, and the remedy is not to widen a
    pattern: it is to decide, in `RULES`, whether the new rule belongs to one
    list or to both. Two rules matching one message is equally a failure --
    overlapping markers would let a rule be credited by another rule's firing.

    **The limit, because a check is worth what its blind spot leaves.** This
    sees a new rule only if the matrix provokes one. A rule about a field no row
    varies is invisible here, which is why the rows above carry whole records
    rather than only their defects -- and it is not hypothetical: the first
    attempt at seeding this check added a rule keyed on a rationale ending in a
    comma, no row had one, and nothing fired.
    """
    unknown: list[str] = []
    ambiguous: list[str] = []
    for level in config.FIDELITY_LEVELS:
        for sources in ((), SUPPLIED):
            for row in ROWS:
                for messages in both_paths(row, level, sources):
                    for message in messages:
                        matched = classify(message)
                        if not matched:
                            unknown.append(f"{row.name}/{level}: {message}")
                        elif len(matched) > 1:
                            ambiguous.append(f"{message} -> {matched}")
    check(not unknown,
          f"{len(unknown)} defect message(s) match no rule in the registry; "
          f"the first is {unknown[0] if unknown else ''!r}. A rule nobody "
          f"filed is a rule the parity comparison cannot see.")
    check(not ambiguous,
          f"{len(ambiguous)} message(s) match more than one rule: "
          f"{ambiguous[:2]}. Overlapping markers let one rule be credited by "
          f"another rule's firing.")


def test_one_implementation_serves_both_callers() -> None:
    """Read from the source, not inferred from behaviour.

    The behavioural checks above would pass over two implementations that
    happened to agree today, and two implementations that agree today are the
    state this contract was already in once -- `check_coverage` had its own
    verdict half, and it agreed with `verdict_defects` about everything it
    checked. It just checked less.

    So the structural half is asserted too: both callers reach the evidence
    rules through the same function. Deleting the call from either one fails
    here as well as in the matrix, and this is the failure that says why.
    """
    tree = ast.parse(PARSING.read_text(encoding="utf-8"))
    calls: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        calls[node.name] = {
            getattr(inner.func, "id", getattr(inner.func, "attr", ""))
            for inner in ast.walk(node) if isinstance(inner, ast.Call)
        }
    for caller in ("check_coverage", "verdict_defects"):
        check(caller in calls, f"`parsing.{caller}` is gone; this file is "
                               f"testing a contract that has moved")
        check("_check_evidence" in calls.get(caller, set()),
              f"`parsing.{caller}` no longer calls `_check_evidence`. One "
              f"implementation serving both callers is the fix; a second copy "
              f"is a second answer.")
    check("check_verdicts" in calls and "verdict_defects" in calls["check_verdicts"],
          "`check_verdicts` must stay the flattening of `verdict_defects`, or "
          "the repair loop and Pass C grade by two different rules")


def test_the_flattening_loses_nothing() -> None:
    """`check_verdicts` is what the repair loop sends back to a model.

    It is documented as `verdict_defects` with the indices dropped. If it ever
    stops being that, the messages a model is asked to repair and the messages
    Pass C files against a record come apart, and the two are read by different
    halves of the tool over one response.
    """
    for level in config.FIDELITY_LEVELS:
        for row in ROWS:
            payload = verdict_payload(row)
            defects, _ = parsing.verdict_defects(payload, SUPPLIED, level)
            flat = parsing.check_verdicts(payload, SUPPLIED, level)
            check([message for _, message in defects] == flat,
                  f"{row.name} at {level}: `check_verdicts` is not the "
                  f"flattening of `verdict_defects`")


# --------------------------------------------------------------------------
# 2. one run, four surfaces
# --------------------------------------------------------------------------

# A phrase that appears in the report's suspended-guarantee sentence, in the
# page's, and in the terminal's shorter version of it. One literal, pinned to
# two shipped artefacts below (`test_the_report_and_the_page_share_their
# _sentences`), because the terminal says the fact in its own fewer words and
# there is no shipped string to take it from.
SUSPENSION = "read the merged document back"

ADDED_STATEMENT = "Kilns are usually fired in batches."


def a_claim(claim_id: str, source: str, text: str) -> Claim:
    return Claim(id=claim_id, source=source, text=text, line=1, span=text,
                 anchored=True)


def a_verdict(claim_id: str, label: str, direction: str, *, evidence: str = "",
              source: str = "", rationale: str = "the reference settles it"
              ) -> Verdict:
    return Verdict(claim_id=claim_id, verdict=label, evidence=evidence,
                   evidence_source=source, rationale=rationale,
                   direction=direction,
                   grounding=GROUNDED if evidence else NOT_GRADED)


def a_run(code: int, depth: str, *, additions: bool = False,
          reverse_pass: bool = True) -> Run:
    """One run, built to reach `code` at `depth`. Nothing here came from a model.

    `reverse_pass` is the fourth axis and the one that is not in the brief's
    list: a run at `full` whose merged document yielded no claims has made no
    reverse pass either, and every sentence about invention is in exactly the
    position it is in at `coverage`. The page already says so -- `cleanAdvice`
    keys on the reverse count and its comment argues that this is the more
    general statement -- and the report did not.
    """
    run = Run(command="merge",
              paths={"source_a.md": "source_a.md", "merged.md": "merged.md"},
              steps=[Step("decompose source_a.md", report.OK)],
              merged="The kiln fired for eleven hours.\n",
              segments=1, verify_depth=depth)
    run.claims = {"source_a.md": [a_claim("A-001", "source_a.md",
                                          "The kiln fired for eleven hours.")]}
    run.forward = [a_verdict("A-001", "SUPPORTED", SOURCE_TO_MERGED,
                             evidence="The kiln fired for eleven hours",
                             source="merged.md")]
    if depth == config.FULL_DEPTH and reverse_pass:
        run.claims[MERGED] = [a_claim("M-001", MERGED,
                                      "The kiln fired for eleven hours.")]
        run.reverse = [a_verdict("M-001", "SUPPORTED", MERGED_TO_SOURCES,
                                 evidence="The kiln fired for eleven hours",
                                 source="source_a.md")]
        if additions:
            # A declared addition is a merged claim the reverse pass could not
            # place and the merge declared, so it exists only where there is a
            # reverse pass to fail to place it.
            run.claims[MERGED].append(a_claim("M-002", MERGED, ADDED_STATEMENT))
            run.reverse.append(a_verdict("M-002", "MISSING", MERGED_TO_SOURCES,
                                         rationale="not in the sources"))
            run.additions = [{"statement": ADDED_STATEMENT, "corrects": "",
                              "reason": "general background"}]
    if code == 1:
        run.claims["source_a.md"].append(
            a_claim("A-002", "source_a.md", "The glaze cracked in three places."))
        run.forward.append(a_verdict("A-002", "MISSING", SOURCE_TO_MERGED,
                                     rationale="absent from the merge"))
    if code == 2:
        run.steps.append(Step("verify (forward)", report.ERRORED,
                              "the endpoint refused the connection"))
    if code == 3:
        run.reconciled = Reconciled(
            findings=(Finding(kind="false_departure",
                              detail="the text it names is still in the merge",
                              segment="a1", document="source_a.md"),),
            declared_drops=(), segments=1)
    return run


SCENARIOS = tuple(
    (f"{depth}/exit-{code}/{'with' if adds else 'no'}-additions", code, depth, adds)
    for depth in (config.FULL_DEPTH, config.COVERAGE_DEPTH)
    for code in (0, 1, 2, 3)
    for adds in (False, True)
)


def flat(text: str) -> str:
    """One line. The Markdown report wraps, and a wrapped sentence is the same
    sentence: a probe that reads raw output finds the short claims and misses
    the long ones, which is the wrong way round."""
    return " ".join(text.split())


def bare(text: str) -> str:
    """Emphasis markers removed. The report writes `**bold**`, `*not*` and
    `` `open` ``; the HTML renderer turns all three into tags that carry no text
    of their own, so the two surfaces are comparable only with the markers gone."""
    return flat(text.replace("**", "").replace("*", "").replace("`", ""))


def dashed(text: str) -> str:
    """`--` collapsed to `-`, and nothing else touched.

    The Markdown report writes `--` where a catalogue string writes `-`. That
    is a rendering convention on each side rather than two statements, and it
    is the only difference this comparison forgives.
    """
    return text.replace("--", "-")


def visible(page: str) -> str:
    """The HTML report as a reader sees it: tags dropped, entities resolved."""
    return bare(html_entities.unescape(re.sub(r"<[^>]+>", " ", page)))


def strings() -> dict:
    return json.loads(EN.read_text(encoding="utf-8"))["strings"]


def js_function(name: str, source: str) -> str:
    """One function's body, read out of `app.js` as text.

    The page cannot be executed here -- there is no JavaScript engine in this
    suite and adding one would put a third-party dependency behind a test -- so
    the mirror below is Python and this is what stops it being fiction.
    """
    start = source.index(f"function {name}(")
    end = source.index("\n}", start)
    return source[start:end]


def page_keys(run: Run) -> list[str]:
    """The catalogue keys `renderVerdict` would join, for this run's payload.

    A mirror of three functions in `app.js`, driven by `report.as_dict` -- the
    very payload the server sends -- rather than by the `Run`, so anything the
    JSON does not carry cannot reach it here either. `detects_invention` is read
    off the run because that is what `/api/v1/config` serves the page from
    (`web/api.py`: the depth rows are built straight out of
    `config.VERIFY_DEPTH_SHAPES`, which is `Run.detects_invention`'s only
    source).

    A mirror is a claim about somebody else's code, so it is pinned:
    `test_the_page_mirror_matches_the_shipped_page` asserts every branch below
    appears in the function it was copied from. That is weaker than running the
    page and stronger than nothing, and it is honest about which it is.
    """
    data = report.as_dict(run)
    code, coverage = data["exit_code"], data["coverage"]
    keys = []
    if code == 0:
        forward = coverage["forward_submitted"]
        reverse = coverage["reverse_submitted"]
        if not forward and not reverse:
            keys.append("advice.clean.nothing")
        elif not reverse:
            keys.append("advice.clean.forward")
        else:
            keys.append("advice.clean")
    elif code == 2:
        # The served flag picks the sourced-specific sentence.
        keys.append("advice.notsourced"
                    if data["sourcing"].get("inconclusive_not_sourced")
                    else "advice.inconclusive")
    elif code == 3:
        keys.append("advice.record")
    else:
        # One plain sentence for every run that exits 1: `adviceFor`
        # used to choose between this and `advice.look.named`, naming
        # whichever sections held something, until the review list itself
        # started naming and jumping to each item's own section and doing so
        # twice became the defect ("Konflikte, Ausgelassene Inhalte" read as
        # a German grammar mistake, mid-sentence).
        keys.append("advice.look")
    if sum(len(ids) for ids in data["additions_cover"]):
        keys.append("advice.additions")
    # `retrievalAdvice`: the served outcome picks the sentence, and an outcome
    # the table does not name -- the empty one below `sourced` -- picks none.
    outcome = data["sourcing"]["retrieval"]
    if outcome in PAGE_RETRIEVAL_KEYS:
        keys.append(PAGE_RETRIEVAL_KEYS[outcome])
    if not run.detects_invention:
        keys.append("advice.noinvention")
    return keys


# The page's `RETRIEVAL_KEYS`, mirrored, and pinned to `app.js` below.
PAGE_RETRIEVAL_KEYS = {
    usage.RETRIEVED: "advice.retrieval.retrieved",
    usage.NOT_RETRIEVED: "advice.retrieval.notretrieved",
    usage.UNMEASURED: "advice.retrieval.unmeasured",
}


def page_sourcing_keys(data: dict) -> list[str]:
    """The catalogue keys `renderAdditions` says about the sources, in order.

    A mirror of that function's sourcing paragraphs, driven by the served
    `sourcing` block, and pinned to the shipped function by
    `test_the_page_mirror_matches_the_shipped_page`. It exists for one
    question the verdict mirror cannot ask: does the page conclude "recalled"
    on exactly the runs the report does?
    """
    sourcing = data["sourcing"]
    state = sourcing.get("state", "unmeasured")
    tool = sourcing.get("tool_use") or {}
    tool_state = tool.get("state", "unmeasured")
    outcome = sourcing.get("retrieval", "")
    keys = ["section.additions.sourcing"]
    if tool_state == "unmeasured" and outcome and state == "not-searched":
        keys.append("section.additions.blindcounter")
    elif tool_state == "unmeasured":
        keys.append({"searched": "section.additions.searched",
                     "not-searched": "section.additions.notsearched"}.get(
                         state, "section.additions.unmeasured"))
    elif state == "searched":
        keys.append("section.additions.searched")
    elif state == "not-searched":
        keys.append("section.additions.blindcounter")
    if tool_state == "unmeasured" and outcome:
        keys.append("toolstate.unmeasured")
    if tool_state != "unmeasured":
        keys.append("toolstate.unmeasured" if tool.get("retrieval") == "unmeasured"
                    else f"toolstate.{tool_state}")
        if sourcing.get("recall_only"):
            keys.append("section.additions.sourcednothing")
    return keys


def surfaces(run: Run) -> dict[str, str]:
    """The same run as four readers meet it."""
    code = report.exit_code(run)
    terminal = io.StringIO()
    cli.summarise(run, code, output=None, coloured=False, piped=False,
                  stream=terminal)
    said = strings()
    return {
        "markdown": bare(report.render(run)),
        "html": visible(html_report.render(run)),
        "terminal": flat(terminal.getvalue()),
        "page": bare(" ".join(said[key] for key in page_keys(run))),
    }


def claims_invention_was_ruled_out(rendered: dict[str, str], run: Run) -> dict[str, bool]:
    """Per surface: does it tell a reader that invention was looked for and not found?

    Every probe is read off the shipped code rather than typed here, so a
    reworded claim moves its probe with it instead of leaving a probe that can
    no longer fire. `report.lost_classes` writes the three report surfaces'
    version; `cli.OUTCOME[0]` writes the terminal's. The page is probed on the
    key it chose, which is the strongest of the four: `advice.clean` is the
    sentence that says "in both directions" and `advice.clean.forward` is the
    one that does not.

    The terminal's probe is the whole clause and not the word `invented`, which
    is the mistake this function made first. The caveat that says invention was
    *not* checked contains that word too, so the loose probe fired on the
    sentence written to say the opposite -- a detector that reads a denial as
    the claim it denies.
    """
    wide = report.lost_classes(a_run(0, config.FULL_DEPTH))
    said = bare(cli.OUTCOME[0][1]).rstrip(".")
    return {
        "markdown": wide in rendered["markdown"],
        "html": wide in rendered["html"],
        "terminal": said in rendered["terminal"],
        "page": "advice.clean" in page_keys(run),
    }


def carries_the_suspended_guarantee(rendered: dict[str, str], run: Run) -> dict[str, bool]:
    """Per surface: does it say that nothing read the merged document back?"""
    return {
        "markdown": SUSPENSION in rendered["markdown"],
        "html": SUSPENSION in rendered["html"],
        "terminal": SUSPENSION in rendered["terminal"],
        "page": "advice.noinvention" in page_keys(run),
    }


def carries_the_addition_caveat(rendered: dict[str, str], run: Run) -> dict[str, bool]:
    """Per surface: does it say that some statements could not be checked at all?"""
    return {
        "markdown": "could not be checked" in rendered["markdown"],
        "html": "could not be checked" in rendered["html"],
        "terminal": "could not be checked" in rendered["terminal"],
        "page": "advice.additions" in page_keys(run),
    }


class _SourcedProvenance:
    """What a `Run` reads its level and its two tallies off, at `sourced`."""

    def __init__(self, *turn_counts) -> None:
        searches = usage.Searches()
        searches.add({"usage": {"server_tool_use": {
            "web_search_requests": 0, "web_fetch_requests": 0}}})
        turns = usage.Turns()
        for count in turn_counts:
            turns.add(None if count is None else {"usage": {"num_turns": count}})
        self.settings = SimpleNamespace(fidelity=config.SOURCED)
        self.client = SimpleNamespace(
            usage=SimpleNamespace(searches=searches, turns=turns))

    def as_dict(self) -> dict:
        """Nothing the page mirrors reads from the provenance block."""
        return {}


def _code_of(js: str) -> str:
    """`js` with `//` and `/* */` comments removed. Rough, and only a hook probe."""
    js = re.sub(r"/\*.*?\*/", " ", js, flags=re.S)
    return "\n".join(line.split("//", 1)[0] if "http" not in line else line
                     for line in js.splitlines())


def test_every_surface_says_what_sourced_retrieval_achieved() -> None:
    """A `sourced` run's retrieval outcome, on every surface a reader meets.

    The probe is each sentence's bold lead, read off `report.RETRIEVAL_SAID`
    rather than typed here, so a reworded sentence moves its probe with it.
    The Markdown and HTML verdicts, the terminal and the page are asserted; the
    page through `page_keys`, the mirror pinned to `retrievalAdvice` below.

    And the sources' own paragraph, which is where the page said the opposite
    of the verdict: over an unmeasured turn count the blind web-request counter
    concluded "every source here is recalled". The page concludes recall on
    exactly the runs `report.sourcing_sentence` does -- the must-fire is the
    run that retrieved nothing, the must-not-fire is both unmeasured runs.
    """
    said = strings()
    leads = {state: re.match(r"\*\*(.+?)\*\*", sentence).group(1)
             for state, sentence in report.RETRIEVAL_SAID.items()}
    recall = ("recalled", "recollection")
    for counts, state in (((1, 3), usage.RETRIEVED),
                          ((1, 2), usage.NOT_RETRIEVED),
                          ((None,), usage.UNMEASURED),
                          ((2, None), usage.UNMEASURED)):
        run = a_run(0, config.FULL_DEPTH)
        run.provenance = _SourcedProvenance(*counts)
        terminal = io.StringIO()
        cli.summarise(run, 0, output=None, coloured=False, piped=False,
                      stream=terminal)
        rendered = {
            "markdown": bare(report.verdict_section(run)),
            "html": visible("".join(html_report.verdict_block(run))),
            "terminal": flat(terminal.getvalue()),
            "page": bare(" ".join(said[key] for key in page_keys(run))),
        }
        for surface, text in rendered.items():
            check(bare(leads[state]) in text,
                  f"{surface} does not say {leads[state]!r} for turns {counts}: "
                  f"{text[:300]!r}")
        for other, lead in leads.items():
            if other != state:
                check(all(bare(lead) not in text for text in rendered.values()),
                      f"a {state} run also says {lead!r}")

        data = report.as_dict(run)
        page = " ".join(said[key] for key in page_sourcing_keys(data))
        written = report.sourcing_sentence(run)
        concluded = {"page": any(word in page for word in recall),
                     "report": any(word in written for word in recall)}
        check(concluded["page"] == concluded["report"],
              f"turns {counts} ({state}): the page "
              f"{'concludes' if concluded['page'] else 'does not conclude'} "
              f"recall and the report "
              f"{'does' if concluded['report'] else 'does not'}:\n"
              f"  page:   {page!r}\n  report: {written!r}")
        check(concluded["page"] is (state == usage.NOT_RETRIEVED),
              f"turns {counts} ({state}): recall concluded on the page is "
              f"{concluded['page']}; only a run that retrieved nothing may say it")


def test_no_surface_claims_invention_was_checked_without_a_reverse_pass() -> None:
    """The one claim that must never outrun the run behind it.

    At `--verify-depth coverage` nothing reads the merged document back. The
    verdict said *"No extracted claim was dropped, contradicted, invented, or
    carried only in part"* anyway, in bold, two steps below a skipped step whose
    stated reason was that invention had not been checked. It was found by
    driving the page, fixed on the page, and left standing in `report.py` --
    which is the Markdown report, the HTML report and the terminal, three
    surfaces and one function.

    Stated here as one rule over all four: a surface may rule invention out only
    on a clean run that actually submitted claims in the other direction. That
    is the page's rule (`cleanAdvice` keys on the reverse count, not on the
    depth's name), and it is more general than keying on the depth -- a `full`
    run whose merged document yielded no claims is in the identical position and
    was not covered by the depth-shaped fix.

    Both halves are asserted. A run that did check gets the claim on all four
    surfaces, or the probes here are dead and the other half proves nothing.
    """
    for name, code, depth, adds in SCENARIOS:
        run = a_run(code, depth, additions=adds)
        rendered = surfaces(run)
        said = claims_invention_was_ruled_out(rendered, run)
        want = report.exit_code(run) == 0 and run.submitted("reverse") > 0
        for surface, claimed in said.items():
            check(claimed is want,
                  f"{name}: the {surface} "
                  f"{'does not rule' if want else 'rules'} invention "
                  f"{'out' if want else 'out'} and "
                  f"{run.submitted('reverse')} claim(s) were submitted in the "
                  f"reverse direction at exit {report.exit_code(run)}")
    # The axis the brief's matrix does not have, and the one the depth-shaped
    # fix misses: `full`, clean, and no claims came back from the merged
    # document, so no reverse pass ran.
    starved = a_run(0, config.FULL_DEPTH, reverse_pass=False)
    check(report.exit_code(starved) == 0 and starved.submitted("reverse") == 0,
          "the starved run must be clean and reverse-empty for this to mean "
          "anything")
    said = claims_invention_was_ruled_out(surfaces(starved), starved)
    check(not any(said.values()),
          f"a `full` run whose reverse pass had nothing to check still claims "
          f"invention was ruled out on: "
          f"{sorted(s for s, v in said.items() if v)}. The depth was capable of "
          f"the question; this run did not ask it.")


def test_every_surface_carries_the_suspended_guarantee() -> None:
    """A caveat that appears only on a clean exit is missing from every report
    anyone reads carefully.

    `report.invention_sentence` and `app.js`'s `suspendedGuarantee` both say so
    in those words and both go on every exit code. The terminal said it on exit
    0 alone, so the reader most likely to act -- the one whose run just failed
    -- was the one not told which guarantee was suspended.

    Keyed on `detects_invention` and not on the reverse count, deliberately, and
    not the same rule as the check above. This sentence is about what the depth
    can do; that one is about what the run did. The page draws the line in
    exactly that place, and two surfaces that agree about a caveat's wording but
    not about when it appears are still two surfaces.
    """
    for name, code, depth, adds in SCENARIOS:
        run = a_run(code, depth, additions=adds)
        said = carries_the_suspended_guarantee(surfaces(run), run)
        want = not run.detects_invention
        for surface, carried in said.items():
            check(carried is want,
                  f"{name}: the {surface} "
                  f"{'omits' if want else 'carries'} the suspended-guarantee "
                  f"sentence over a run whose depth "
                  f"{'cannot' if want else 'can'} detect invention")


def test_every_surface_carries_the_addition_caveat() -> None:
    """The second suspended guarantee, and the same question asked of it.

    At `open` the merge may add statements from the model's own knowledge. They
    are declared, they are reported, and they are the one thing this tool cannot
    check -- so a clean verdict over them means the merge said it was adding
    them, not that they are true. The report says that and the page says that.
    The terminal said *"Nothing was dropped, contradicted or invented."* and
    stopped, which is the same over-claim as the invention one, reached by the
    same route: a caveat that lives in one renderer.
    """
    for name, code, depth, adds in SCENARIOS:
        run = a_run(code, depth, additions=adds)
        said = carries_the_addition_caveat(surfaces(run), run)
        want = bool(run.declared_additions)
        for surface, carried in said.items():
            check(carried is want,
                  f"{name}: the {surface} "
                  f"{'omits' if want else 'carries'} the declared-addition "
                  f"caveat over a run with {len(run.declared_additions)} "
                  f"excused claim(s)")


def test_every_surface_listing_a_source_says_nothing_resolved_it() -> None:
    """The not-checked statement goes where the sources are listed.

    Not in a footnote elsewhere and not on one renderer. A reader weighing a
    citation is doing it in front of the row that carries it, and a caveat on
    another page is a caveat they meet after they have decided. This is the
    same failure the addition caveat above exists for, one field further in
    and with a sharper edge: a fabricated citation in a trusted report
    launders a guess into something that looks checkable.

    Asserted over the three surfaces that render the section. The terminal is
    excluded deliberately -- it prints the same Markdown, which is what
    `surfaces` reads for "markdown".
    """
    for name, code, depth, adds in SCENARIOS:
        if not adds:
            continue
        run = a_run(code, depth, additions=adds)
        run.additions = [{"statement": ADDED_STATEMENT, "corrects": "",
                          "basis": "citation", "source": "RFC 2119",
                          "reason": "the term is defined there"}]
        rendered = surfaces(run)
        for surface in ("markdown", "html"):
            check("did not fetch, resolve or check any source"
                  in rendered[surface],
                  f"{name}: the {surface} lists a source and does not say "
                  f"that nothing fetched, resolved or checked it")
            check("RFC 2119" in rendered[surface],
                  f"{name}: the {surface} must show the source itself, or the "
                  f"reader cannot go and check what the tool did not")
        # Read off the shipped `renderAdditions` rather than off `page_keys`,
        # which mirrors `renderVerdict` and is a different function. Grepping
        # the file is how this module pins its other claim about the page, and
        # it is the only honest way to say the section carries the key.
        source = APP_JS.read_text(encoding="utf-8")
        section = source.split("function renderAdditions(")[-1].split("\nfunction ")[0]
        for key in ("section.additions.sourcing", "detail.basis", "detail.source",
                    "detail.source.none", "section.additions.corrections"):
            check(f'"{key}"' in section,
                  f"{name}: the shipped renderAdditions does not use {key}; "
                  f"the page would list a source without the statement every "
                  f"other surface carries")
        for locale in ("en", "de"):
            strings = json.loads(
                (ROOT / "src" / "llossless" / "web" / "locales"
                 / f"{locale}.json").read_text(encoding="utf-8"))["strings"]
            check("did not fetch, resolve or check" in strings[
                      "section.additions.sourcing"]
                  or locale != "en",
                  f"{name}: the {locale} statement must say what was not done")
            check("section.additions.unmeasured" in strings,
                  f"{name}: {locale} has no unmeasured sentence, so the page "
                  f"would have to report an absence it never measured")

        # The measurement beside it, and `unmeasured` is not `not-searched`.
        # These runs carry no provenance, so nothing measured, and a surface
        # that said "the model made no web request" would be this tool
        # inventing a measurement it never took.
        for surface in ("markdown", "html"):
            check("unmeasured" in rendered[surface],
                  f"{name}: the {surface} must say whether the model searched "
                  f"is unmeasured, not report it as none")
            check("made no web request" not in rendered[surface],
                  f"{name}: the {surface} reports an absence it never measured")


def test_a_run_with_no_reverse_pass_can_have_no_declared_addition() -> None:
    """Why the matrix's additions axis is empty at `coverage`, said rather than
    left to look like an oversight.

    A declared addition is a merged claim the reverse pass could not place. With
    no reverse pass there is no such claim, whatever the merge declared, so both
    the report's count and the page's are zero by construction. Asserted because
    "zero here" and "zero because nothing looked" are the two readings this
    project spends most of its time keeping apart, and because a future depth
    that reads the merge back differently would land here first.
    """
    run = a_run(0, config.COVERAGE_DEPTH, additions=True)
    run.additions = [{"statement": ADDED_STATEMENT, "corrects": "",
                      "reason": "general background"}]
    check(not run.declared_additions,
          "a coverage run reported a declared addition; nothing read the merge "
          "back, so nothing could have found one")
    check(not sum(len(ids) for ids in report.as_dict(run)["additions_cover"]),
          "`additions_cover` is non-empty on a run with no reverse pass; the "
          "page would show a caveat the report cannot")


def test_the_page_mirror_matches_the_shipped_page() -> None:
    """The mirror above is a claim about `app.js`. This is where it is falsifiable.

    Nothing here runs the page. What it does is assert that every branch the
    mirror takes is present in the function it was copied from, so a page that
    stops keying its clean sentence on the reverse count, or starts deciding the
    suspended guarantee by the depth's name, fails here rather than leaving a
    Python mirror quietly describing a page that no longer exists.
    """
    source = APP_JS.read_text(encoding="utf-8")
    advice = js_function("adviceFor", source)
    for key in ("advice.inconclusive", "advice.notsourced", "advice.record",
                "advice.look"):
        check(key in advice, f"`adviceFor` no longer chooses {key!r}")
    check("sourcing || {}).inconclusive_not_sourced" in advice,
          "`adviceFor` no longer picks `advice.notsourced` by the served "
          "`sourcing.inconclusive_not_sourced`; the mirror assumes it")
    check("advice.look.named" not in advice and "where.push" not in advice,
          "`adviceFor` names sections again in prose above the review "
          "list, which now names and jumps to each item's own section itself")
    check("cleanAdvice(" in advice and "code === 0" in advice,
          "`adviceFor` must still route the clean exit to `cleanAdvice`")

    clean = js_function("cleanAdvice", source)
    check("advice.clean.nothing" in clean and "advice.clean.forward" in clean
          and 't("advice.clean"' in clean,
          "`cleanAdvice` no longer has the three clean sentences the mirror "
          "chooses between")
    check("if (!reverse)" in clean,
          "`cleanAdvice` no longer keys on the reverse count. That is the rule "
          "the report was brought into line with; if the page has moved, the "
          "parity above is being asserted against the wrong side.")
    check("reverse_submitted" in clean and "forward_submitted" in clean,
          "`cleanAdvice` reads its counts from somewhere the mirror does not")

    guarantee = js_function("suspendedGuarantee", source)
    check("detects_invention" in guarantee and "advice.noinvention" in guarantee,
          "`suspendedGuarantee` must decide by the served flag and say it with "
          "the catalogue string")
    check("verify_depth" not in guarantee.split("detects_invention")[1],
          "`suspendedGuarantee` decides by the depth's name after reading the "
          "flag; the mirror assumes the flag alone")

    banner = js_function("renderVerdict", source)
    for call in ("adviceFor(report)", "suspendedGuarantee(report)",
                 't("advice.additions"', "retrievalAdvice(report)"):
        check(call in banner,
              f"`renderVerdict` no longer joins {call}; the mirror builds the "
              f"banner from all four")

    # The outcome is the served one and the keys are the mirror's.
    retrieval = js_function("retrievalAdvice", source)
    check("sourcing.retrieval" in retrieval and "RETRIEVAL_KEYS[" in retrieval,
          "`retrievalAdvice` no longer picks its sentence by the served "
          "`sourcing.retrieval`")
    table = source[source.index("const RETRIEVAL_KEYS = {"):]
    table = table[:table.index("};")]
    for outcome, key in PAGE_RETRIEVAL_KEYS.items():
        check(re.search(r'["\']?' + re.escape(outcome) + r'["\']?:\s*"'
                        + re.escape(key) + '"', table) is not None,
              f"`RETRIEVAL_KEYS` no longer maps {outcome} to {key}")

    # And the sources' paragraph: every branch `page_sourcing_keys` takes.
    additions = js_function("renderAdditions", source)
    for piece in ('const blind = toolState === "unmeasured" && outcome '
                  '&& state === "not-searched";',
                  'String(sourcing.retrieval || "")',
                  'if (toolState === "unmeasured" && outcome) {',
                  't("toolstate.unmeasured")',
                  "t(toolSentenceKey(toolUse),",
                  "if (sourcing.recall_only) {"):
        check(piece in additions,
              f"`renderAdditions` no longer has {piece!r}; the mirror "
              f"`page_sourcing_keys` describes a page that no longer exists")
    chooser = js_function("toolSentenceKey", source)
    check('=== "unmeasured"' in chooser and '"toolstate.unmeasured"' in chooser
          and "retrieval" in chooser,
          "`toolSentenceKey` no longer says unmeasured over a partial count")


# Locale strings whose report counterpart is meant to be the same sentence, and
# the function that writes it. One entry today -- that is not a small table by
# accident, it is what the surfaces genuinely share -- and the completeness
# assertion below is what stops the second one being added to only one side.
PAIRED = {
    "advice.noinvention": lambda: report.invention_sentence(
        a_run(0, config.COVERAGE_DEPTH)),
}

# Every other `advice.*` key, with the reason it has no report counterpart.
# Enumerated because there is no naming convention to find them by, and the key
# set is asserted complete below, so a new string cannot join the catalogue
# without somebody deciding which of these two tables it belongs in.
UNPAIRED = {
    "advice.clean": "the page states a clean result affirmatively and with its "
                    "denominators; the report's headline is the negative "
                    "sentence plus a scope clause, and that combination was "
                    "chosen on purpose",
    "advice.clean.forward": "the forward-only form of the sentence above",
    "advice.clean.nothing": "a clean run with nothing to check; the report says "
                            "this through `unexamined_sources`, per source, "
                            "rather than in one sentence",
    "advice.inconclusive": "the report names the units that errored and the "
                           "records that could not be graded; the page has one "
                           "line and links to the report",
    "advice.notsourced": "exit 2 on a `sourced` merge that looked "
                         "nothing up and nothing else; the report's "
                         "NOT_SOURCED says it with the level named and the "
                         "re-run advice, the page in two plain sentences",
    "advice.look": "an instruction to the reader of a page with a review list "
                   "to scroll to; a document has no equivalent",
    "advice.record": "exit 3 in one line; the report's version carries the "
                     "counts and the scope sentence. The terminal says this "
                     "sentence word for word, asserted in test_exit_3_says_"
                     "one_thing_on_every_surface",
    "advice.retrieval.retrieved": "the report's RETRIEVAL_SAID sentence "
                                  "with the level described rather than "
                                  "named, `section.additions.sourcednothing`'s "
                                  "rule -- the page holds no fidelity "
                                  "vocabulary. The bold lead is the same words "
                                  "on all four surfaces, asserted in "
                                  "test_every_surface_says_what_sourced_"
                                  "retrieval_achieved",
    "advice.retrieval.notretrieved": "the same, for the second outcome",
    "advice.retrieval.unmeasured": "the same, for the third; 'this page' where "
                                   "the report says 'this report'",
    "advice.additions": "deliberately shorter than "
                        "`report.addition_sentence`: the page shows it in a "
                        "banner beside the verdict and the report has the "
                        "section underneath it. The two are held together by "
                        "when they appear, which is asserted above, rather "
                        "than by their words",
}


# The same registry for the declared-additions section, which later gained a
# second vocabulary that was never held to the first.
#
# `advice.*` was the only family filed here, so `section.additions.*` and
# `basis.*` were word-parallel with `report.py` by somebody's care and by
# nothing else -- and `basis.*` had already diverged: the page said *cited*
# where the report printed `citation`, in the same column of the same table.
#
# A dash is normalised before comparing. The Markdown report writes `--` where
# the catalogue writes `-`, which is a rendering convention on each side and
# not two statements; every other character has to match.
ADDITION_PAIRED = {
    "basis.citation": lambda: report.basis_word("citation"),
    "basis.own-knowledge": lambda: report.basis_word("own-knowledge"),
    "section.additions.sourcing": lambda: report.NOT_RESOLVED,
    "section.additions.searched": lambda: report._SEARCHING["searched"],
    "section.additions.notsearched": lambda: report._SEARCHING["not-searched"],
    "section.additions.unmeasured": lambda: report._SEARCHING["unmeasured"],
    # The second instrument's three states, held to the first's rule.
    # They are a separate family because they are a separate measurement --
    # `_SEARCHING` counts web requests off `server_tool_use` and these count
    # turns off `num_turns` -- and the two disagree on a command backend by
    # construction, so a page that paraphrased one into the other's words
    # would publish the disagreement as a wording accident.
    "toolstate.tool-use": lambda: report._TOOL_USE["tool-use"],
    "toolstate.no-tool-use": lambda: report._TOOL_USE["no-tool-use"],
    "toolstate.unmeasured": lambda: report._TOOL_USE["unmeasured"],
    # What the blind counter may still say once the other has reported: its
    # number, never its conclusion.
    "section.additions.blindcounter": lambda: report.SEARCH_COUNTER_BLIND,
}

ADDITION_UNPAIRED = {
    "section.additions.note": "the report's version counts the records and the "
                              "page's does not: the page has the list beside "
                              "it and the report is read where the table may "
                              "be pages away. They also address different "
                              "readers -- 'your documents' on the page you "
                              "submitted them to, 'the reader's job' in a file "
                              "that gets forwarded",
    "section.additions.corrections": "same sentence, and the report's is built "
                                     "with the count already substituted; it "
                                     "is compared below with the placeholder "
                                     "filled rather than as a literal",
    "section.additions.sourcednothing":
        "the report names the level and the page must not: the ladder is "
        "served from `/config` and the page holds no fidelity vocabulary at "
        "all, so its version says what the level asks for rather than what it "
        "is called. Same fact, and the page's phrasing survives a seventh "
        "level where a copy of the report's sentence would not",
}


def test_the_addition_section_says_the_same_thing_on_both_surfaces() -> None:
    """`section.additions.*` and `basis.*`, held the way `advice.*` is.

    The page rendered `basis` through the catalogue and the report printed the
    enum, so one column of one table read *cited* on screen and `citation` in
    the file saved from that screen. Nothing could see it: the completeness
    registry covered `advice.*` and no other family, and the key-set check
    holds the two catalogues to each other rather than to `report.py`.

    Every key in both families is filed in exactly one of the two tables, so a
    string added to the section cannot join one surface alone.
    """
    said = strings()
    catalogue = {key for key in said
                 if key.startswith("section.additions.")
                 or key.startswith("basis.")
                 or key.startswith("toolstate.")}
    filed = set(ADDITION_PAIRED) | set(ADDITION_UNPAIRED)
    check(catalogue == filed,
          f"the addition-section catalogue and the two tables here disagree: "
          f"{sorted(catalogue - filed)} unfiled, {sorted(filed - catalogue)} "
          f"filed and gone")
    check(not (set(ADDITION_PAIRED) & set(ADDITION_UNPAIRED)),
          "a key cannot be both paired and unpaired")

    for key, sentence in sorted(ADDITION_PAIRED.items()):
        check(key in said, f"{key} has gone from the catalogue")
        written = dashed(bare(sentence()))
        check(written == dashed(said.get(key, "")),
              f"the report and the page describe the same thing differently:\n"
              f"  report: {written!r}\n  page:   {said.get(key, '')!r}")

    # The one paragraph that is the same sentence with the count already in it.
    # Rendered through the shipped section rather than re-quoted, so a reword
    # in `report.py` fails here instead of passing against a copy.
    run = a_run(0, config.FULL_DEPTH)
    run.additions = [{"statement": "S", "corrects": "C", "basis": "citation",
                      "source": "somewhere", "reason": "R"}]
    rendered = bare(report.additions_section(run))
    page = dashed(said["section.additions.corrections"].replace("{n}", "1"))
    check(page in dashed(rendered),
          f"the report's corrections paragraph is no longer the page's:\n"
          f"  page: {page!r}\n  report: {rendered!r}")

    # And the column itself, end to end: the words, not the enum, in both
    # renderers. The seed is the enum value, which is what used to be printed.
    from llossless import html_report
    for surface, text in (("markdown", report.additions_section(run)),
                          ("html", visible(html_report.render(run)))):
        check(said["basis.citation"] in bare(text),
              f"the {surface} additions table does not print "
              f"{said['basis.citation']!r} for a cited record")
        check("citation" not in bare(text),
              f"the {surface} additions table still prints the enum value "
              f"`citation`; the column is the page's words now")


def test_the_attributions_section_says_what_the_report_says() -> None:
    """The page's Attributions section in the report's own words.

    The note above the rows is the predicate, and it is what makes a row fair
    to print: a reader is being told the merge misquotes one of their
    documents, and the note is how they check that by hand. So it is the same
    sentence on both surfaces, and the row's label is the report's one phrase
    for the finding, capitalised as a label.
    """
    said = strings()
    check(dashed(said.get("section.attributions.note", ""))
          == dashed(bare(report.ATTRIBUTIONS_NOTE)),
          f"the page and the report describe the Attributions section "
          f"differently:\n  report: {report.ATTRIBUTIONS_NOTE!r}\n"
          f"  page:   {said.get('section.attributions.note', '')!r}")
    label = said.get("kind.misattributed", "")
    check(label[:1].isupper() and label.lower() == report.MISATTRIBUTED_WORDS.lower(),
          f"the page calls a misattribution {label!r} and the report calls it "
          f"{report.MISATTRIBUTED_WORDS!r}")


def test_the_basis_column_check_fires_on_the_defect_it_was_written_for() -> None:
    """Seeded with the state that shipped: `BASIS_WORDS` empty, the enum printed.

    Against the shipped renderers rather than a copy of their expression --
    emptying the table is how `report.additions_section` and
    `html_report.render` behaved before an earlier fix, so this drives the real defect
    through the real code and puts it back.
    """
    from llossless import html_report

    run = a_run(0, config.FULL_DEPTH)
    run.additions = [{"statement": "S", "corrects": "", "basis": "citation",
                      "source": "somewhere", "reason": "R"}]
    kept = dict(report.BASIS_WORDS)
    report.BASIS_WORDS.clear()
    try:
        markdown = bare(report.additions_section(run))
        page = visible(html_report.render(run))
    finally:
        report.BASIS_WORDS.update(kept)
    for surface, text in (("markdown", markdown), ("html", page)):
        check("citation" in text and "cited" not in text,
              f"seeded check: with BASIS_WORDS emptied the {surface} table did "
              f"not fall back to the enum, so this gate is not reading the "
              f"column it claims to read")
    check(bare(report.additions_section(run)).count("cited") == 1,
          "the table did not go back to the reader's word after the seed; "
          "BASIS_WORDS was not restored")


def test_the_report_and_the_page_share_their_sentences() -> None:
    """Asserted by equality, for every pair rather than for one hand-picked pair.

    Two surfaces describing one suspended guarantee in two sets of words is how
    a reader comes to believe they mean two different things, and this project
    has the worked example: at `coverage` the page said the run had checked "in
    both directions" two words before saying nothing had read the merge back.

    The completeness check is the part that makes this more than the single
    assertion it replaces. Every `advice.*` key must appear in exactly one of
    the two tables, so the next sentence the page and the report are both given
    cannot be added to one side alone -- it arrives as a red line asking which
    table it belongs in.
    """
    said = strings()
    catalogue = {key for key in said if key.startswith("advice.")}
    filed = set(PAIRED) | set(UNPAIRED)
    check(catalogue == filed,
          f"the advice catalogue and the two tables here disagree: "
          f"{sorted(catalogue - filed)} unfiled, {sorted(filed - catalogue)} "
          f"filed and gone. Every sentence the page says about a verdict is "
          f"either one the report also says, in the same words, or one with a "
          f"reason it is not.")
    check(not (set(PAIRED) & set(UNPAIRED)),
          "a key cannot be both paired and unpaired")
    for key, sentence in PAIRED.items():
        check(key in said, f"{key} is gone from the catalogue")
        written = bare(sentence())
        check(written == said.get(key, ""),
              f"the report and the page describe the same thing differently:\n"
              f"  report: {written!r}\n  page:   {said.get(key, '')!r}")
    # The one literal in this half of the file, pinned to both artefacts it is
    # used against. The terminal's version of the sentence is shorter and is
    # written in `cli.py` rather than taken from either, so a probe for it
    # cannot be derived -- this is what keeps it from being a probe that can no
    # longer fire.
    check(SUSPENSION in bare(report.invention_sentence(
              a_run(0, config.COVERAGE_DEPTH))),
          f"{SUSPENSION!r} is no longer in the report's sentence; the "
          f"terminal's probe is aimed at nothing")
    check(SUSPENSION in said.get("advice.noinvention", ""),
          f"{SUSPENSION!r} is no longer in the page's sentence")


def test_the_help_names_every_exit_code_the_tool_returns() -> None:
    """The fifth surface, and the one nobody re-reads: `--help`.

    It is not a per-run description, so it is not in the matrix above -- but it
    is a claim about what a code means, and a claim about what a code means can
    go stale in exactly the same way. Two were: `exit 0` read *"nothing was
    dropped, contradicted or invented"*, unconditionally, three months after
    `coverage` made the last third of that depth-dependent; and `exit 3` had
    been split out of 1 later and never reached the help at all, so the
    one code a reader is most likely to be surprised by was the one the tool
    would not explain.

    Asserted against `report.exit_code`'s own vocabulary rather than a list
    here, so the next code to be split out arrives as a red line.
    """
    text = cli.build_parser().format_help()
    for code in (0, 1, 2, report.RECORD_ONLY):
        check(f"exit {code}" in text,
              f"`--help` does not say what exit {code} means, and it is a code "
              f"this tool returns")
    check("coverage" in text.split("exit 0")[1].split("exit 1")[0],
          "the help says what exit 0 means without saying that `coverage` "
          "changes it; a clean run at that depth rules out nothing about "
          "invention")


# What every surface says about exit 3, as the clause they share. The one
# literal in this test, pinned below to each artefact it is probed against, so
# a rewording on any side arrives as a red line rather than a probe that can no
# longer fire.
RECORD_ONLY_CLAUSE = "the merge's account of itself"


def test_exit_3_says_one_thing_on_every_surface() -> None:
    """The terminal described a record-only run as one that did not finish.

    `cli.summarise` looked its sentence up with `OUTCOME.get(code, OUTCOME[2])`
    and `OUTCOME` had no row for 3, so the terminal said "Could not complete.
    Part of this run did not finish" over a finished run whose merged document
    the tool had found sound. The matrix above rendered that run on all four
    surfaces and asserted nothing about exit 3 itself.

    The page and the terminal now say one sentence, asserted by equality. The
    reports carry the counts and a scope sentence, so they are held to the
    shared clause instead, and no surface may call the run unfinished.
    """
    said = strings()
    check(report.RECORD_ONLY in cli.OUTCOME,
          "cli.OUTCOME has no row for exit 3; the terminal borrows another "
          "code's sentence")
    headline, gloss = cli.OUTCOME.get(report.RECORD_ONLY, ("", ""))
    check(gloss == said.get("advice.record"),
          f"the terminal and the page describe exit 3 differently:\n"
          f"  terminal: {gloss!r}\n  page:     {said.get('advice.record')!r}")
    check(set(cli.OUTCOME) == set(report.EXIT_CODES),
          f"cli.OUTCOME covers {sorted(cli.OUTCOME)}, the tool returns "
          f"{sorted(report.EXIT_CODES)}")
    check(headline.rstrip(".").lower().endswith(
              html_report.BANNER[report.RECORD_ONLY][1].lower()),
          f"the terminal's headline {headline!r} and the HTML banner "
          f"{html_report.BANNER[report.RECORD_ONLY][1]!r} name exit 3 two ways")
    help_text = " ".join(cli.build_parser().format_help().split())
    check(RECORD_ONLY_CLAUSE in help_text.split("exit 3")[-1],
          f"{RECORD_ONLY_CLAUSE!r} is no longer in --help's exit 3 line")
    unfinished = cli.OUTCOME[2][0]
    for depth in (config.FULL_DEPTH, config.COVERAGE_DEPTH):
        run = a_run(3, depth)
        check(report.exit_code(run) == report.RECORD_ONLY,
              f"the {depth} scenario must reach exit 3")
        check("advice.record" in page_keys(run),
              f"the page mirror chose {page_keys(run)} for exit 3 at {depth}")
        check(RECORD_ONLY_CLAUSE in bare(report.verdict_line(run)),
              f"{RECORD_ONLY_CLAUSE!r} is no longer in the report's exit 3 "
              f"verdict at {depth}")
        for surface, text in surfaces(run).items():
            check(RECORD_ONLY_CLAUSE in text,
                  f"{surface} does not say {RECORD_ONLY_CLAUSE!r} for exit 3 "
                  f"at {depth}")
            check(unfinished not in text and "did not finish" not in text,
                  f"{surface} calls a finished exit 3 run unfinished at "
                  f"{depth}")


def test_every_level_is_described_for_a_person_in_both_languages() -> None:
    """The picker's copy is written for a reader, and there is one of it.

    **The defect it replaces:** `web/api.fidelity_levels` served the opening
    paragraph of `prompts/fidelity/<level>.merge.md`, so a person choosing a
    setting read text addressed to the model -- *"you are expected to look a
    fact up"*, *"you have been given a web tool for this run"*. Every level had
    it. A prompt and a picker are two registers with two audiences and one
    string cannot be both.

    Three rules, and each has a seed below it:

    1. Every level has all three fields in **both** catalogues, checked by set
       equality so a seventh level cannot ship with a blank under the slider.
    2. `en.json` is `config.FIDELITY_SHAPES` byte for byte, which is the table
       `--fidelity`'s help renders from -- so the command line and the page
       cannot describe one level two ways.
    3. No served description addresses the model, and none is a paragraph of
       the fragment it replaced.

    The German catalogue is agent-authored, like every other German string in
    this repository, and is checked for structure rather than for meaning:
    every key present, no placeholder invented, and not a copy of the English.
    """
    said = strings()
    german = json.loads(
        (EN.parent / "de.json").read_text(encoding="utf-8"))["strings"]

    wanted = {f"fidelity.{level}.{part}"
              for level in config.FIDELITY_LEVELS
              for part in ("summary", "buys", "costs")}
    for name, catalogue in (("en", said), ("de", german)):
        found = {key for key in catalogue if key.startswith("fidelity.")}
        check(found == wanted,
              f"{name}.json's level descriptions and config.FIDELITY_LEVELS "
              f"disagree: {sorted(wanted - found)} missing, "
              f"{sorted(found - wanted)} left over")

    for level, shape in config.FIDELITY_SHAPES.items():
        for part in ("summary", "buys", "costs"):
            key = f"fidelity.{level}.{part}"
            check(said.get(key) == getattr(shape, part),
                  f"{key} is not config.FIDELITY_SHAPES'; the page and "
                  f"`--fidelity --help` would describe {level} two ways:\n"
                  f"  help: {getattr(shape, part)!r}\n"
                  f"  page: {said.get(key)!r}")
            check(german.get(key) and german[key] != said.get(key),
                  f"{key} is missing from de.json or is the English string")

    # Written for a person. The cheap, honest form: no second person about the
    # model, and no paragraph lifted out of the fragment.
    banned = ("you are expected", "you have been given", "this run")
    for level, shape in config.FIDELITY_SHAPES.items():
        fragment = prompts.load(f"fidelity/{level}.merge").text
        paragraphs = {" ".join(block.split())
                      for block in fragment.split("\n\n") if block.strip()}
        for part in ("summary", "buys", "costs"):
            written = getattr(shape, part)
            for phrase in banned:
                check(phrase not in written.lower(),
                      f"{level}.{part} says {phrase!r}, which addresses the "
                      f"model rather than the reader: {written!r}")
            check(written not in paragraphs,
                  f"{level}.{part} is a paragraph of the prompt fragment; UI "
                  f"copy and prompt text are two registers: {written!r}")

    # Seeded, and the seed is the real defect rather than an invented one:
    # what this endpoint used to serve is the fragment's opening paragraph,
    # and it fails both rules.
    opening = " ".join(
        prompts.load("fidelity/sourced.merge").text.split("\n\n")[0].split())
    check(any(phrase in opening.lower() for phrase in banned),
          "seeded check: the fragment no longer addresses the model in the "
          "second person, so the first rule above is measuring nothing")
    seeded = {" ".join(block.split())
              for block in prompts.load("fidelity/sourced.merge").text.split("\n\n")
              if block.strip()}
    check(opening in seeded,
          "seeded check: the opening paragraph is not one of the fragment's "
          "paragraphs, so the second rule above cannot fire")

    # And the one thing the level tables must agree about with the copy: a
    # level that permits an addition has to say so in its `costs`, because
    # that is the guarantee a reader gives up by choosing it.
    for level, adds in merge_module.ADDS.items():
        if not adds:
            continue
        costs = config.FIDELITY_SHAPES[level].costs.lower()
        check("model" in costs and ("your job" in costs or "claim" in costs),
              f"{level} permits an undeclared-free addition and its cost "
              f"sentence does not say the claim rests on the model: "
              f"{config.FIDELITY_SHAPES[level].costs!r}")


def depth_and_title_copy() -> dict[str, str]:
    """The English each depth and title policy is described in, from its source.

    A depth's name and sentence are `config.VERIFY_DEPTH_SHAPES`, which
    `--verify-depth`'s help renders; a title policy's sentence is the first
    paragraph of its prompt fragment, which `/config` serves (`api.
    title_policies`). Formed here from those two sources, never from `en.json`.
    """
    from llossless import prompts as prompt_files
    from llossless.web import api as web_api
    copy = {}
    for value, shape in config.VERIFY_DEPTH_SHAPES.items():
        copy[f"depth.{value}.name"] = shape.name
        copy[f"depth.{value}.explains"] = shape.explains
    for policy in config.TITLE_POLICIES:
        copy[f"title.{policy}.explains"] = web_api.first_paragraph(
            prompt_files.load(f"title/{policy}").text)
    return copy


def depth_and_title_problems(said: dict, german: dict) -> list[str]:
    """`en.json` is the source byte for byte; `de.json` has its own for each."""
    found = []
    wanted = depth_and_title_copy()
    for name, catalogue in (("en", said), ("de", german)):
        have = {key for key in catalogue
                if key.startswith("depth.") or key.startswith("title.")}
        if have != set(wanted):
            found.append(f"{name}.json's depth and title copy and the sources disagree: "
                         f"{sorted(set(wanted) - have)} missing, {sorted(have - set(wanted))} "
                         f"left over")
    for key, text in sorted(wanted.items()):
        if said.get(key) != text:
            found.append(f"{key} is not its source's text; the command line and the "
                         f"page would describe it two ways:\n  source: {text!r}\n"
                         f"  page:   {said.get(key)!r}")
        if not german.get(key) or german.get(key) == said.get(key):
            found.append(f"{key} is missing from de.json or is the English string")
    return found


def test_the_depths_and_title_policies_are_described_in_both_languages() -> None:
    """The depth picker and the title explanation, through the catalogue.

    `/config` serves each depth's `name` and `explains` and each title
    policy's `explains` in English, and the page rendered them as served, so
    a German page showed two English paragraphs. The page now renders
    `depth.<value>.name`, `depth.<value>.explains` and
    `title.<policy>.explains` from the catalogue, the way the depth copy moved
    `fidelity.*`, and `en.json` is held to the English sources here.

    Must-fire: one English word changed, one German string made English, and
    a policy dropped from German are each caught.
    """
    said = strings()
    german = json.loads((EN.parent / "de.json").read_text(encoding="utf-8"))["strings"]
    for problem in depth_and_title_problems(said, german):
        check(False, problem)
    seeded = dict(said)
    seeded["depth.coverage.explains"] = seeded.get("depth.coverage.explains", "").replace(
        "invention", "inventions")
    check(bool(depth_and_title_problems(seeded, german)), "an English drift is not caught")
    seeded = dict(german)
    seeded["title.synthesise.explains"] = said.get("title.synthesise.explains", "")
    check(bool(depth_and_title_problems(said, seeded)), "English left in de.json is not caught")
    seeded = {key: text for key, text in german.items() if key != "title.keep-base.explains"}
    check(bool(depth_and_title_problems(said, seeded)), "a policy missing from de.json is not caught")


def catalogue_notes_problems(said: dict, german: dict) -> list[str]:
    """`en.json`'s `models.catalogue.notes` is the shipped catalogue's own
    `notes` text, byte for byte; `de.json` has its own, distinct translation."""
    from llossless.web import catalogue as catalogue_module
    found = []
    source_text = catalogue_module.load().get("notes") or ""
    if not source_text:
        found.append("the shipped catalogue.json carries no top-level notes; "
                      "this test's source has moved")
        return found
    key = "models.catalogue.notes"
    if said.get(key) != source_text:
        found.append(f"{key} is not catalogue.json's own notes text; the page and "
                     f"the file would describe the list two ways:\n"
                     f"  catalogue.json: {source_text!r}\n"
                     f"  en.json:        {said.get(key)!r}")
    if not german.get(key) or german.get(key) == said.get(key):
        found.append(f"{key} is missing from de.json or is the English string")
    return found


def test_the_catalogue_s_top_level_note_is_described_in_both_languages() -> None:
    """`/config` serves `catalogue.notes` in English: it is part of the
    served contract, other clients may read it -- and `renderScorecard` used
    to print it as served, so "About this list" showed one English paragraph
    on the German page (the same leak fixed earlier for the verify depths and
    title policies, found by the same UI pass). The page now reads
    `models.catalogue.notes` from the locale catalogue, held here to the
    shipped `catalogue.json`'s own `notes` field so the two cannot drift, with
    `de.json` carrying its own translation.

    Must-fire: `en.json`'s copy changed a word, and `de.json` left in the
    English string, are each caught.
    """
    said = strings()
    german = json.loads((EN.parent / "de.json").read_text(encoding="utf-8"))["strings"]
    for problem in catalogue_notes_problems(said, german):
        check(False, problem)
    seeded = dict(said)
    seeded["models.catalogue.notes"] = seeded.get("models.catalogue.notes", "").replace(
        "exhaustive", "complete")
    check(bool(catalogue_notes_problems(seeded, german)), "an English drift is not caught")
    seeded_de = dict(german)
    seeded_de["models.catalogue.notes"] = said.get("models.catalogue.notes", "")
    check(bool(catalogue_notes_problems(said, seeded_de)), "English left in de.json is not caught")


def test_a_rewording_finding_shows_the_difference_on_every_surface() -> None:
    """Issue, source, merge and why, in one row, on all three surfaces.

    The operator's report is the requirement twice over. Once about this kind:
    *"it would be very helpful to highlight how it was reworded. So that the
    user can directly see the difference."* And once in general: *"the user
    does not need to refer to sections or the documents but gets the full
    understanding of the claims directly in one row. Issue, source, merge, why
    it is how it is."*

    A `detail` sentence alone answered only the why, so a reader met "this is
    reworded" and went looking for both texts. The reconciler holds both
    strings and the similarity already, so the difference costs no new
    comparison.

    **Three surfaces, and the terminal decides the form.** There is no colour
    guarantee there, so the notation has to survive being plain -- `[-was-]`
    and `{+is+}`, which every surface can print as text. Seeded by removing
    each of the three things a row must carry.
    """
    source = "The breeding areas have July isotherms between 14 and 16 degrees."
    merged = "Breeding areas have July isotherms between 14 and 16 degrees C."
    finding = Finding("undeclared_rewording",
                      f"{source!r} is reworded in the merge and no disposition "
                      f"record explains it (nearest merge segment m38 at 0.99)",
                      segment="c8", document="source_c.md",
                      source_text=source, merge_text=merged)
    shown = finding.difference
    check(shown, "the two sides must diff to something at 0.99 similarity")
    check("[-" in shown and "{+" in shown,
          f"the notation must carry itself without colour: {shown!r}")
    check("isotherms" in shown and shown.count("isotherms") == 1,
          f"an unchanged word appears once, not once per side: {shown!r}")

    run = a_run(1, config.FULL_DEPTH)
    run.reconciled = Reconciled(findings=(finding,), declared_drops=(), segments=1)

    markdown = report.structural_section(run)
    page_source = (ROOT / "src" / "llossless" / "web" / "static" / "app.js").read_text(
        encoding="utf-8")
    html = "\n".join(html_report.structural_block(run))

    # 1. the why, which is what a row always carried.
    for name, text in (("markdown", markdown), ("html", visible(html))):
        check("reworded in the merge" in text,
              f"{name}: the row lost the sentence saying what is wrong")

    # 2. the difference, which is what the two sides are for.
    for name, text in (("markdown", markdown), ("html", visible(html))):
        check(shown in bare(text),
              f"{name}: the difference is not on the row: {text[:300]!r}")
        check(report.DIFF_LEGEND.replace("`", "") in bare(text),
              f"{name}: the notation is used and never explained")

    # 3. the page renders the same served string rather than diffing again.
    check("finding.difference" in page_source,
          "the page must render the difference the engine published, or it is "
          "a second implementation of the rendering rule")
    check("detail.insource" in page_source and "detail.inmerge" in page_source,
          "and must fall back to the two texts where no diff is available")
    check("section.difference.legend" in page_source,
          "and must explain the notation it prints")

    # Seeded: remove each of the three and the checks above fail.
    bare_finding = Finding(finding.kind, finding.detail, finding.segment,
                           finding.document)
    check(not bare_finding.difference,
          "seeded check: a finding with no second side must offer no diff, or "
          "the fallback above is never reached")
    quiet = a_run(1, config.FULL_DEPTH)
    quiet.reconciled = Reconciled(findings=(bare_finding,), declared_drops=(),
                                  segments=1)
    check(report.DIFF_LEGEND.replace("`", "") not in bare(report.structural_section(quiet)),
          "seeded check: the legend is printed over a run that uses no diff")

    # And the far-apart case: two texts this would diff into noise show as two
    # texts instead, which is the honest long form.
    far = Finding("undeclared_rewording", "detail", segment="c9",
                  source_text="One short sentence about kilns.",
                  merge_text="Something else entirely, concerning ferries.")
    check(not far.difference,
          f"two unrelated texts must not be diffed: {far.difference!r}")
    run_far = a_run(1, config.FULL_DEPTH)
    run_far.reconciled = Reconciled(findings=(far,), declared_drops=(), segments=1)
    written = report.structural_section(run_far)
    check("One short sentence about kilns." in written
          and "concerning ferries" in written,
          f"both texts must be printed where a diff would mislead: {written!r}")


def test_a_one_space_difference_is_shown_as_one_space() -> None:
    """The operator's own case, which an earlier word diff could not show.

    Their finding, verbatim::

        Um die einzelnen Spiele und Runden mitzuzaehlen, wird eine kleine Dose
        [-(Mingg)verwendet.-] {+(Mingg) verwendet.+}

    The whole difference is **one space**, and a word diff renders it as two
    whole tokens swapped -- so a one-character change reads as a rewritten
    clause and the reader has to compare the tokens letter by letter
    themselves, which is the work the diff exists to do.

    Words still decide *what* changed; characters now say *where inside it*.
    That earlier judgement about a character diff over whole prose stands and is
    asserted below on the same example, which keeps its word-level form for
    the run that would read worse marked.
    """
    spaced = ("Um die einzelnen Spiele und Runden mitzuzaehlen, wird eine "
              "kleine Dose (Mingg) verwendet.")
    unspaced = spaced.replace("(Mingg) verwendet", "(Mingg)verwendet")
    shown = reconcile_module.difference(unspaced, spaced)
    check("{+ +}" in shown,
          f"a one-space difference must be shown as one space: {shown!r}")
    check("[-" not in shown,
          f"nothing was removed, so nothing may be marked removed: {shown!r}")
    check(shown.count("verwendet") == 1,
          f"the unchanged word appears once, not once per side: {shown!r}")
    # And the direction the operator saw it in, which is the same difference.
    back = reconcile_module.difference(spaced, unspaced)
    check("[- -]" in back and "{+" not in back,
          f"the other direction removes the one space: {back!r}")

    # The earlier example: the run that reads worse marked keeps its word form, and
    # the run that reads better marked gets the fine one. Both in one string,
    # which is the whole argument for refining per run rather than per diff.
    older = reconcile_module.difference(
        "The breeding areas have July isotherms between 14 and 16 degrees.",
        "Breeding areas have July isotherms between 14 and 16 degrees C.")
    check("[-The breeding-] {+Breeding+}" in older,
          f"a run where most of the letters would be bracketed stays whole: "
          f"{older!r}")
    check("degrees{+ C+}." in older,
          f"and a run with a difference in it is marked inside: {older!r}")

    # Seeded: the floor and the share are what decide it, so move each.
    check(reconcile_module._refine("abcdefghij", "abcdefghix") is not None,
          "seeded check: a one-letter change in ten must refine, or the "
          "clauses above are measuring nothing")
    # The floor's own case, and it took a search to find one: the share clause
    # measures the *widest* changed region, so a short run that is a scattered
    # subsequence of a much longer one gets past it with every region small
    # while the pair is nothing like each other. That is exactly what the floor
    # is for, and without this pair the clause would be a guard no check
    # reaches -- the seeded run that first tried `"abcdefghij"` against
    # `"qrstuvwxyz"` stayed green with the floor deleted, because the share
    # clause caught it instead.
    scattered = ("bcbaaac", "bcbcccbccccabcbacbbbbccaaccaaaaccacbc")
    check(reconcile_module.similarity(*scattered) < reconcile_module.CHAR_FLOOR,
          "seeded check: the pair below has to be under the floor, or it is "
          "testing a different clause")
    check(reconcile_module._refine(*scattered) is None,
          "seeded check: two runs this far apart must not be marked inside; "
          "that is the case judged earlier")
    check(reconcile_module._refine("abcdef", "abqrst") is None,
          "seeded check: half the run inside markers is a rewrite, and a "
          "rewrite is legible as two whole texts")

    # And the cap, which the finer diff made newly dangerous. The word diff truncates on
    # a word boundary because *"a `[-` with no `-]` after it reads as a broken
    # renderer rather than as a truncation"*. A refined run puts markers inside
    # a word and can mark a space -- `{+ +}` is the operator's own case -- so
    # the last space before the cap can now be the one *inside* a marker, and
    # `rsplit` then cuts exactly there.
    #
    # Swept rather than sampled: the offending cut is wherever the marker
    # happens to fall, so the marker is slid one character at a time across
    # the cap. Measured on this sweep, the word-boundary rule alone breaks at
    # 25 of the 120 positions; the shipped rule breaks at none.
    tail = (" Wer die hoechste Karte legt, nimmt den Stich und spielt als "
            "naechster aus. Am Ende werden die Punkte zusammengezaehlt und "
            "die Partie dem Spieler mit der hoechsten Summe gutgeschrieben.")
    truncated = 0
    for pad in range(540, 660):
        head = ("ab " * 400)[:pad]
        one = reconcile_module.difference(head + "Dose(Mingg)verwendet." + tail,
                                          head + "Dose (Mingg) verwendet." + tail)
        if not one:
            continue
        if one.endswith(" ..."):
            truncated += 1
        check(reconcile_module._balanced(one),
              f"a truncated diff left a marker open at pad {pad}: "
              f"{one[-40:]!r}")
    check(truncated > 100,
          f"seeded check: the sweep has to reach the cap, or it is asserting "
          f"balance on strings that were never cut: {truncated} of 120")


def test_a_findings_two_sides_stack_on_every_surface() -> None:
    """One directly above the other, in plain text as well as in a browser.

    The operator: they want the source line and the merged line *"one directly
    above the other ... so the difference can be read by scanning down a column
    rather than along a sentence"*.

    **The stacked form has to be the plain-text form too.** The Markdown report
    and the terminal have no lightbox, and a finding legible only in a browser
    is useless in a downloaded audit. So there is one renderer,
    `report.stacked_lines`, and the column is real: the labels are padded to
    one width and the block is fenced, because a fence is what makes a Markdown
    reader show it monospaced.

    This supersedes half of the earlier finding, which showed the diff **instead of** the two
    texts. Both are shown now; the diff stays as the third line, because it is
    the only one of the three that says where to look.
    """
    source_text = ("Um die einzelnen Spiele und Runden mitzuzaehlen, wird eine "
                   "kleine Dose (Mingg)verwendet.")
    merge_text = source_text.replace("(Mingg)verwendet", "(Mingg) verwendet")
    finding = Finding("undeclared_rewording", "reworded in the merge",
                      segment="a3", document="source_a.md",
                      source_text=source_text, merge_text=merge_text)

    stack = report.stacked_lines(finding)
    check(len(stack) == 3,
          f"three lines: the source, the merge and what changed: {stack!r}")
    check(stack[0].startswith(report.EVIDENCE_LABELS["source"])
          and stack[1].startswith(report.EVIDENCE_LABELS["merge"])
          and stack[2].startswith(report.EVIDENCE_LABELS["difference"]),
          f"in that order, source first: {stack!r}")
    starts = {line.index(source_text[:20]) if source_text[:20] in line
              else line.index(merge_text[:20]) for line in stack}
    check(len(starts) == 1,
          f"the three texts must start in the same column, or the stack is "
          f"three sentences: {stack!r}")

    run = a_run(1, config.FULL_DEPTH)
    run.reconciled = Reconciled(findings=(finding,), declared_drops=(), segments=1)
    markdown = report.structural_section(run)
    check("```text" in markdown,
          f"the Markdown stack is fenced, or the padding buys an alignment "
          f"only the raw file has: {markdown!r}")
    for line in stack:
        check("  " + line in markdown,
              f"the markdown lost a stacked line: {line!r}")

    html = "\n".join(html_report.structural_block(run))
    check('<pre class="stack">' in html,
          f"the HTML stack is a monospaced box for the same reason: {html!r}")
    # Read out of the `<pre>` rather than through `visible`, which collapses
    # whitespace runs: the padding *is* the thing under test here, and a
    # helper that normalises it would compare the stack against itself with
    # the alignment removed.
    inside = html_entities.unescape(
        html[html.index('<pre class="stack">') + len('<pre class="stack">'):])
    inside = inside[:inside.index("</pre>")]
    check(inside.split("\n") == stack,
          f"the html stack must be the same three lines, spacing included: "
          f"{inside!r}")

    # The page builds the same three rows in the same order, with the labels
    # localised -- which is why it is the shape that is asserted here and the
    # strings that are asserted in `test_web_static`.
    page = (ROOT / "src" / "llossless" / "web" / "static" / "app.js").read_text(
        encoding="utf-8")
    body = page[page.index("function stackPanel("):]
    body = body[:body.index("\n}\n")]
    check(body.index('t("detail.insource")') < body.index('t("detail.inmerge")')
          < body.index('t("detail.changed")'),
          "the page stacks source, merge, difference, in that order")
    check("padEnd" in body,
          "and pads the labels, or its column is not a column")

    # Seeded: a finding with one side has nothing to stack, and a finding with
    # no side has no block at all.
    one = Finding("undeclared_absence", "gone", source_text=source_text)
    check(len(report.stacked_lines(one)) == 1,
          "seeded check: one side stacks to one line")
    none = Finding("declared_loss_over_budget", "arithmetic")
    check(report.stacked_lines(none) == [] and report.evidence_lines(none) == [],
          "seeded check: a finding with no second side prints no block; an "
          "empty one would teach a reader to skip the ones that carry something")


def main() -> int:
    tests = [value for name, value in sorted(globals().items())
             if name.startswith("test_") and not name.endswith("_offline")]
    for test in tests:
        test()
    for note in notes:
        print(f"note: {note}")
    if failures:
        print(f"contract parity: FAILED ({len(failures)} failing)")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"contract parity: {len(tests)} checks pass; two checkers agree on "
          f"{len(ROWS)} record shapes at {len(config.FIDELITY_LEVELS)} levels, "
          f"four surfaces agree on {len(SCENARIOS)} runs")
    return 0


def test_contract_parity_offline() -> None:
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
