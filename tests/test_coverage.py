#!/usr/bin/env python3
"""The fused coverage pass: one call per source, extraction and judgement together.

`--verify-depth coverage` exists to cost less. What it must not do is cost less
by quietly grading less carefully than the pass it replaces, so the checks here
are mostly about sameness: the same claim ids, the same verdict vocabulary per
level, the same fidelity fragment, the same grounding rule.

The one thing it genuinely does not do is look for invention. That is not a
defect to be fixed here and it is not tested here either -- it is a property of
the depth, asserted where the depth is chosen and stated where the verdict is
read.

Offline throughout. A stub client returns a fixed payload; what is under test
is the wiring and the contract, not a model.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless import config, decompose, merge, parsing, verify, window  # noqa: E402
from llossless.client import SchemaFailure  # noqa: E402

SOURCE = "The kiln fired for eleven hours and the glaze cracked in three places.\n"
MERGED = "The kiln fired for eleven hours.\n"
DOCUMENTS = {"source_a.md": SOURCE, "merged.md": MERGED}
WINDOW = window.Window(tokens=32000, source="stated", model="test-model")

PAYLOAD = {"claims": [
    {"text": "The kiln fired for eleven hours.", "line": 1,
     "span": "The kiln fired for eleven hours", "verdict": "SUPPORTED",
     "evidence": "The kiln fired for eleven hours",
     "evidence_source": "merged.md", "rationale": "Stated in the merge."},
    {"text": "The glaze cracked in three places.", "line": 1,
     "span": "the glaze cracked in three places", "verdict": "MISSING",
     "evidence": "", "evidence_source": "", "rationale": "Absent from the merge."},
]}

failures: list[str] = []
notes: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


class _Completion:
    def __init__(self, payload, truncations=()):
        self.payload, self.truncations = payload, list(truncations)


class Stub:
    """A client that records what it was asked and answers with `payload`.

    The capping pre-pass runs here because it runs in `client.complete`, ahead
    of the semantic check and ahead of the return: a stub that skipped it
    would hand back a `Completion` with no truncations on a payload the real
    client would have cut, and the caller's handling of them would be untested
    against anything.
    """

    sends_nothing = False

    def __init__(self, payload=None):
        self.payload = payload if payload is not None else PAYLOAD
        self.calls: list[dict] = []

    def served_window(self, role):
        return WINDOW

    def complete(self, *, role, prompt, messages, schema, schema_name, semantic):
        truncations = parsing._truncate_capped_fields(self.payload)
        self.calls.append({
            "role": role, "schema_name": schema_name, "schema": schema,
            "prompt": prompt, "content": messages[0]["content"],
            "errors": semantic(self.payload),
        })
        return _Completion(self.payload, truncations)


def run(level: str = "off", payload=None, client: Stub | None = None):
    client = client or Stub(payload)
    claims, verdicts = verify.verify_coverage(
        client, SOURCE, "source_a.md", DOCUMENTS,
        policy=merge.MergePolicy(fidelity=level))
    return client, claims, verdicts


def test_one_source_costs_exactly_one_call() -> None:
    """The whole reason the depth exists.

    At `full` this source costs one decompose call plus one verify call per
    batch of 25 claims. Here it is one, and if that ever stops being true the
    depth has no purpose left.
    """
    client, claims, verdicts = run()
    check(len(client.calls) == 1,
          f"one source must cost one call, not {len(client.calls)}")
    # And that 1 is the same 1 the web picker prices this depth with. The page
    # shows the depth's cost for the documents actually loaded, formed from
    # `calls_per_source`; measuring one here and publishing the other
    # separately would be two numbers that happen to agree today.
    check(len(client.calls)
          == config.VERIFY_DEPTH_SHAPES[config.COVERAGE_DEPTH].calls_per_source,
          f"the published per-source cost is "
          f"{config.VERIFY_DEPTH_SHAPES[config.COVERAGE_DEPTH].calls_per_source}"
          f" and the measured one is {len(client.calls)}")
    check(len(claims) == len(verdicts) == 2,
          f"every extracted claim carries a verdict: {len(claims)} claims, "
          f"{len(verdicts)} verdicts")
    check(client.calls[0]["role"] == "verify",
          f"the call is charged to the verify role, not a fourth one: "
          f"{client.calls[0]['role']!r}")
    notes.append(f"coverage prompt for a {len(SOURCE)}-byte source against a "
                 f"{len(MERGED)}-byte merge: {len(client.calls[0]['content'])} chars")


def test_claim_ids_match_the_full_depth_numbering() -> None:
    """A report at one depth has to be readable against a report at the other.

    `decompose.claim_id` is the only place that decides what a claim is called.
    Numbering these by position with that same function is what lets the two
    depths be compared claim by claim instead of only in total.
    """
    _, claims, verdicts = run()
    expected = [decompose.claim_id("source_a.md", i + 1) for i in range(len(claims))]
    check([c.id for c in claims] == expected,
          f"ids {[c.id for c in claims]} are not decompose's: {expected}")
    check([v.claim_id for v in verdicts] == expected,
          "each verdict must name the claim it answers")


def test_the_pass_is_forward_and_says_so() -> None:
    """Direction is not cosmetic: it decides what a verdict *means*.

    `MISSING` forward is a dropped claim; `MISSING` reverse is a hallucination.
    A coverage run only ever asks the forward question, so every verdict it
    produces must carry the forward direction or the report will read its
    omissions as inventions.
    """
    _, _, verdicts = run()
    check(all(v.direction == verify.SOURCE_TO_MERGED for v in verdicts),
          f"directions: {[v.direction for v in verdicts]}")
    check(verify.COVERAGE in verify.DEPTHS and verify.FULL in verify.DEPTHS,
          f"both depths must be named in DEPTHS: {verify.DEPTHS}")


def test_the_verdict_vocabulary_follows_the_level() -> None:
    """The schema is the enforcement; the prose only explains it.

    `off` cannot emit DERIVED because the grammar it is handed has no such
    value. A coverage run that received the `off` schema at `high` would be
    marking legitimate `high` rewrites as unsupported, which is the same
    failure mode found on the other axis.
    """
    for level in ("off", "low", "mid", "high", "open"):
        client, _, _ = run(level)
        enum = client.calls[0]["schema"]["properties"]["claims"]["items"] \
                                       ["properties"]["verdict"]["enum"]
        check(tuple(enum) == parsing.verdicts_for(level),
              f"{level}: schema offers {enum}, level allows "
              f"{parsing.verdicts_for(level)}")


def test_the_level_reaches_the_prompt_and_rekeys_it() -> None:
    """The fused pass is handed the forward pass's own fidelity fragment.

    Not a fifth set of files: the judging rules are identical, and two copies
    would be free to disagree. The test that this actually happened is that
    the composed prompt digest moves with the level -- which is also what keeps
    a cassette recorded at one level from answering at another.
    """
    digests = {}
    for level in ("off", "high"):
        client, _, _ = run(level)
        digests[level] = client.calls[0]["prompt"].sha256
        fragment = merge.MergePolicy(fidelity=level).fragment("verify").text
        opening = fragment.strip().splitlines()[0]
        check(opening in client.calls[0]["content"],
              f"{level}: the level's own verify fragment is not in the prompt")
    check(digests["off"] != digests["high"],
          "the composed prompt must differ by level, or one cassette answers "
          "for two levels")


def test_a_fabricated_span_is_not_reported_as_grounded() -> None:
    """Grounding is located, not believed.

    The model names a span and the file it came from; `grounding_of` goes and
    finds it. A span that is in no file is the shape of a confident wrong
    answer, and reporting it as grounded would launder exactly the failure this
    tool exists to catch.
    """
    invented = {"claims": [dict(PAYLOAD["claims"][0],
                                evidence="The kiln fired for forty hours")]}
    _, _, verdicts = run("high", invented)
    check(verdicts[0].grounding != "grounded",
          f"a span that appears in no document was reported "
          f"{verdicts[0].grounding!r}")
    _, _, honest = run("high")
    check(honest[0].grounding == "grounded",
          f"and a real span must still ground: {honest[0].grounding!r}")


def test_the_contract_is_the_two_it_is_made_of() -> None:
    """`COVERAGE_FIELDS` is assembled, not typed out.

    Half of it is `decompose`'s claim fields and half is the verdict's minus
    `claim_id`. Writing the seven names out would be a third place for the
    contract to live and the first place it would go stale.
    """
    check(parsing.COVERAGE_FIELDS[:3] == ("text", "line", "span"),
          f"the claim half moved: {parsing.COVERAGE_FIELDS[:3]}")
    check(parsing.COVERAGE_FIELDS[3:] == parsing.VERDICT_FIELDS[1:],
          f"the verdict half moved: {parsing.COVERAGE_FIELDS[3:]} against "
          f"{parsing.VERDICT_FIELDS[1:]}")
    check(verify.COVERAGE_FIELDS is parsing.COVERAGE_FIELDS,
          "verify must not keep its own copy of the field order")
    item = verify.coverage_schema()["properties"]["claims"]["items"]
    check(tuple(item["properties"]) == parsing.COVERAGE_FIELDS,
          f"the schema emits {tuple(item['properties'])}")
    check(tuple(item["required"]) == parsing.COVERAGE_FIELDS,
          "every field is required; an optional property costs the whole "
          "structured-output tier")


def test_the_semantic_check_refuses_what_it_should() -> None:
    """Three shapes, two of which a schema walk cannot see.

    Field order and an empty verdict both satisfy the JSON schema. They are
    caught here, in the same pass that catches them for the unfused verdicts,
    reading the same field tuple.
    """
    good = PAYLOAD
    check(not parsing.check_coverage(good), "a well-formed payload must pass")

    record = PAYLOAD["claims"][0]
    reordered = {"claims": [{"verdict": record["verdict"],
                             **{k: v for k, v in record.items() if k != "verdict"}}]}
    check(parsing.check_coverage(reordered),
          "a record emitting verdict first must be refused")

    unjudged = {"claims": [dict(record, verdict="   ")]}
    check(parsing.check_coverage(unjudged),
          "a claim with no verdict must be refused: it is indistinguishable "
          "from a claim the pass never found")

    blank = {"claims": [dict(record, span="")]}
    check(parsing.check_coverage(blank),
          "an empty span must be refused, as it is for decompose")


def test_an_over_long_rationale_is_capped_and_declared() -> None:
    """The fused payload keeps its rationales under `claims`, not `verdicts`.

    A field with a `maxLength` in the schema and no cap in the pre-pass is a
    field a vendor clips mid-word in silence. That happened once already,
    on `mismatch`, and the fix was to declare the cut rather than discover it
    in a report.
    """
    long = dict(PAYLOAD["claims"][0], rationale="x" * (parsing.RATIONALE_MAX + 40))
    payload = {"claims": [long]}
    truncations = parsing._truncate_capped_fields(payload)
    check(bool(truncations),
          "an over-long rationale in the fused payload was not declared")
    check(len(payload["claims"][0]["rationale"]) <= parsing.RATIONALE_MAX,
          f"and it must be cut: "
          f"{len(payload['claims'][0]['rationale'])} characters remain")


def test_the_evidence_rules_are_the_same_rules_at_either_depth() -> None:
    """The half of the verdict contract the fused pass was not checking at all.

    `check_coverage` ran `check_claims`, tested that a verdict was non-empty
    and checked the field order. Every rule `verdict_defects` applies to the
    *judgement* went unapplied: the label vocabulary, and the four evidence
    couplings -- an EVIDENCED label with no span, one naming no file, one
    naming a file the model was never given, and a MISSING that quotes
    evidence anyway.

    Asserted as a parity, record for record, rather than as a list of cases
    this module keeps its own copy of. The rule is not "coverage refuses these
    four shapes"; it is "coverage refuses what verify refuses", and a copy of
    the list here would be the second implementation the function's own
    docstring says not to write.
    """
    good = dict(PAYLOAD["claims"][0])
    broken = {
        "no span": dict(good, evidence=""),
        "no file": dict(good, evidence_source=""),
        "a file nobody gave it": dict(good, evidence_source="notes.md"),
        "MISSING with evidence": dict(good, verdict="MISSING"),
        "outside the vocabulary": dict(good, verdict="PROBABLY"),
    }
    for why, record in broken.items():
        fused = parsing.check_coverage({"claims": [record]}, ("merged.md",))
        unfused = parsing.check_verdicts(
            {"verdicts": [{"claim_id": "A-001",
                           **{k: v for k, v in record.items()
                              if k in parsing.VERDICT_FIELDS}}]},
            ("merged.md",))
        check(bool(fused) == bool(unfused) and bool(fused),
              f"{why}: the fused pass reports {len(fused)} defect(s) and the "
              f"unfused one {len(unfused)}; the cheaper depth must not grade "
              f"more leniently, it must only ask less")
    check(not parsing.check_coverage(PAYLOAD, ("merged.md",)),
          "and a well-formed payload must still pass with the filenames given")


def test_an_unattributed_span_is_not_laundered_into_a_grounded_one() -> None:
    """The defect that made the cheap depth *look* better than the full one.

    `verify_coverage` read `evidence_source` as `... or MERGED`, so a record
    that named no file was handed the only filename there was, `locate` found
    the span in it, and the verdict came back `grounded`. The identical reply
    at `full` came back `attribution_error`, because `verify_claims` keeps the
    empty string and lets the check fail it. "Evidence grounded" is a ratio
    this tool publishes, so the depth was quietly improving it.

    Both ends are asserted. The grading must not launder, and the semantic
    check must refuse the record in the first place -- a reply like this one
    goes back to the model for repair rather than being graded at all, and
    only the second assertion says so.
    """
    unattributed = {"claims": [dict(PAYLOAD["claims"][0], evidence_source="")]}
    client, _, verdicts = run(payload=unattributed)
    check(verdicts[0].grounding != verify.GROUNDED,
          f"a span attributed to nothing was reported "
          f"{verdicts[0].grounding!r}; the same record at `full` is an "
          f"attribution error")
    check(verdicts[0].evidence_source == "",
          f"and the missing attribution must reach the report as missing, not "
          f"as {verdicts[0].evidence_source!r}")
    check(client.calls[0]["errors"],
          "the semantic check must refuse it too: a record the grader marks "
          "down is a record the model should have been asked to fix")


def test_a_capped_rationale_is_declared_at_this_depth_too() -> None:
    """`Completion.truncations` reached the caller at `full` and nowhere else.

    `verify_coverage` took `.payload` off the completion and dropped the rest,
    so `Verdict.rationale_capped` was False on every coverage verdict and the
    report's capping section printed "None." over a run that had cut one.
    The rule is that a cap is declared rather than discovered, and that was
    said of this pass before it was true of it.
    """
    long = dict(PAYLOAD["claims"][0],
                rationale="x" * (parsing.RATIONALE_MAX + 40))
    _, _, verdicts = run(payload={"claims": [long]})
    check(verdicts[0].rationale_capped,
          "an over-long rationale was capped and the verdict does not say so")
    _, _, honest = run()
    check(not honest[0].rationale_capped,
          "and a rationale nobody cut must not be marked as cut")


def test_salvage_refuses_a_fused_payload_and_that_is_the_decision() -> None:
    """Pass C does not apply here, and the reason is not that nobody wired it.

    `verify_claims` takes an `unusable` accumulator: one ungradeable record is
    dropped, recorded, and the other twenty-four are graded. `verify_coverage`
    takes none, by design. The short form is that
    the record *is* the claim: dropping it would delete the evidence that the
    claim was ever extracted and renumber every claim after it, because
    `decompose.claim_id` numbers by position -- so a coverage report would
    stop being readable against a full one, which is the property this pass
    exists to keep. `decompose_text` has never salvaged either, at the same
    cost.

    Asserted mechanically rather than left in prose: `salvage` looks for
    `$.verdicts` and a fused payload has none, so it refuses this shape by
    construction. A future edit that generalised it would fail here and have
    to argue with this design.
    """
    failure = SchemaFailure(
        "verify", "unusable", None,
        payload={"claims": [dict(PAYLOAD["claims"][0], evidence_source="")]},
        defects=("$.claims[0] is SUPPORTED but names no evidence_source; give "
                 "the filename you quoted from",))
    rescued = verify.salvage(
        failure,
        lambda payload: (
            [(0, d) for d in parsing.check_coverage(payload, ("merged.md",))],
            set()),
        verify.SOURCE_TO_MERGED)
    check(rescued is None,
          "salvage accepted a fused payload; it must not, and "
          "a claim dropped here vanishes rather than going ungraded")

    import inspect
    taken = inspect.signature(verify.verify_coverage).parameters
    check("unusable" not in taken,
          f"`verify_coverage` grew an `unusable` parameter: {sorted(taken)}. "
          f"That reverses a deliberate ruling, which is a decision to record "
          f"rather than a signature to widen")


def test_every_caller_of_the_pipeline_chooses_a_depth() -> None:
    """`depth` has a default, and the default is the trap.

    `pipeline(..., depth=config.DEFAULT_VERIFY_DEPTH)` means a call site that
    forgets it does not fail -- it runs `full` and reports `full`, which is
    indistinguishable from working. That is exactly what happened: the two
    call sites in `cli.py` were wired and `web/jobs.py` was not, so the
    setting meant nothing through the server and an operator who set
    `LLOSSLESS_VERIFY_DEPTH` would have been told the run checked for
    invention when it had.

    Asserted over the source rather than by running each path, because the
    point is to catch the *fourth* call site, which does not exist yet.
    """
    import ast

    sites = []
    for name in ("src/llossless/cli.py", "src/llossless/web/jobs.py"):
        tree = ast.parse((ROOT / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            called = getattr(node.func, "attr", getattr(node.func, "id", ""))
            if called != "pipeline":
                continue
            sites.append((name, node.lineno,
                          "depth" in [k.arg for k in node.keywords]))

    check(len(sites) >= 3,
          f"expected at least the three known call sites, found {len(sites)}; "
          f"if `pipeline` moved, this test is looking in the wrong files")
    missing = [f"{n}:{line}" for n, line, ok in sites if not ok]
    check(not missing,
          f"these call sites let the depth default silently: {missing}. A run "
          f"that forgets the depth reports `full` and looks correct.")
    notes.append(f"pipeline call sites passing depth: {len(sites)}/{len(sites)}")


def main() -> int:
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and not k.endswith("_offline")]
    for test in tests:
        test()
    for note in notes:
        print(f"note: {note}")
    if failures:
        print(f"coverage: FAILED ({len(failures)} failing)")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"coverage: {len(tests)} checks pass; one call per source, "
          f"decompose's ids, the level's own fragment")
    return 0


def test_coverage_offline() -> None:
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
