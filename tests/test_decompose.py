#!/usr/bin/env python3
"""Offline checks for the decompose pass. No network, no model, no dependencies.

Everything here exercises the deterministic half of pass 2: line numbering,
span anchoring, claim ids, prompt loading, and the grading the fixture runner
does. The model's judgement is not testable this way and is not meant to be —
that is what tests/run_decompose.py measures.

The client is stubbed with a canned response, so the parse-and-anchor path that
turns a model's JSON into Claim objects is covered end to end without inference.

Run with `python3 tests/test_decompose.py`, or collect with pytest.
"""

from __future__ import annotations

import contextlib
import json
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs, so a test that points a
# socket anywhere but the configured endpoint fails loudly instead of
# succeeding quietly. tests/test_socket_guard.py asserts every module does this.
socket_guard.install()

from llossless import config, parsing, prompts  # noqa: E402
from llossless.client import Client, Completion  # noqa: E402
from llossless.decompose import (  # noqa: E402
    ANCHOR_RADIUS,
    Claim,
    anchor,
    claim_id,
    decompose_text,
    number_lines,
)

import run_decompose  # noqa: E402
# The model an offline run replays with, read from the corpus rather than the
# machine: `models.local.json` names a model only until the next re-record.
import replay_models  # noqa: E402

DOC = "\n".join(
    [
        "# Vandrell Relay — Operator Guide",  # 1
        "",  # 2
        "## Networking",  # 3
        "",  # 4
        "The relay listens on port 8443 by default.",  # 5
        "The default connect timeout is 30 seconds.",  # 6
        "The relay accepts at most 512 concurrent",  # 7
        "connections.",  # 8
    ]
)

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


class StubClient(Client):
    """A Client that returns a canned payload. Never opens a socket."""

    # Never opens a socket, so there is no served window to preflight
    # against and nothing for the guard to protect.
    sends_nothing = True

    def __init__(self, payload: dict) -> None:
        super().__init__(config.Settings(models={"verify": "stub"}, use_cache=False))
        self.payload = payload
        self.prompt: str | None = None

    def complete(self, *, messages, **_) -> Completion:
        self.prompt = messages[-1]["content"]
        return Completion(self.payload)


def test_number_lines() -> None:
    numbered = number_lines(DOC).splitlines()
    check(len(numbered) == 8, "number_lines dropped or added lines")
    check(numbered[0] == "1 | # Vandrell Relay — Operator Guide", "line 1 mislabelled")
    check(numbered[1] == "2 | ", "blank lines must be numbered, not skipped")
    check(numbered[7].startswith("8 | "), "final line mislabelled")

    wide = number_lines("\n".join(str(i) for i in range(1, 12))).splitlines()
    check(wide[0].startswith(" 1 | "), "line numbers must be right-aligned to a fixed width")
    check(wide[10].startswith("11 | "), "widest line number mislabelled")


def test_anchor() -> None:
    lines = DOC.splitlines()

    check(anchor("The relay listens on port 8443 by default.", 5, lines) == (5, True),
          "exact span on the reported line should anchor there")
    check(anchor("the RELAY listens on PORT 8443", 5, lines) == (5, True),
          "anchoring must ignore case")
    check(anchor("The default connect timeout is 30 seconds.", 99, lines) == (6, True),
          "a wrong line hint must not stop the span being found")
    check(anchor("The relay accepts at most 512 concurrent connections.", 7, lines) == (7, True),
          "a span wrapping a line break must anchor to the window's first line")

    line, anchored = anchor("The relay supports SOCKS5 proxies.", 4, lines)
    check((line, anchored) == (4, False),
          "an unfindable span must keep the hint and report anchored=False")
    check(anchor("", 3, lines) == (3, False), "an empty span cannot anchor")

    # Nearest-to-hint tie-break: the fixtures share one fact pool, so a short
    # span can honestly occur twice.
    repeated = ["port 8443", "filler", "filler", "filler", "port 8443"]
    check(anchor("port 8443", 5, repeated) == (5, True), "must pick the occurrence nearest the hint")
    check(anchor("port 8443", 1, repeated) == (1, True), "must pick the occurrence nearest the hint")


def test_claim_id() -> None:
    check(claim_id("source_a.md", 1) == "A-001", "source_a claims are A-prefixed")
    check(claim_id("source_b.md", 14) == "B-014", "source_b claims are B-prefixed")
    check(claim_id("merged.md", 7) == "M-007", "merged claims are M-prefixed")
    check(claim_id("notes.md", 3) == "N-003", "an unknown document falls back to its initial")
    # A third source needs no entry anywhere, because the letter is read
    # off the canonical name rather than looked up in a table of two.
    check(claim_id("source_c.md", 2) == "C-002", "source_c claims are C-prefixed")
    check(claim_id("source_aa.md", 1) == "AA-001",
          f"past z the prefix is the whole letter, got {claim_id('source_aa.md', 1)!r}")


def test_decompose_parses_and_anchors() -> None:
    client = StubClient(
        {
            "claims": [
                {
                    "text": "The relay listens on port 8443 by default.",
                    "line": 5,
                    "span": "The relay listens on port 8443 by default.",
                },
                {
                    # The model miscounted. The span is what fixes it.
                    "text": "The default connect timeout is 30 seconds.",
                    "line": 2,
                    "span": "The default connect timeout is 30 seconds.",
                },
                {
                    # The model paraphrased instead of copying: unanchored.
                    "text": "The relay accepts at most 512 concurrent connections.",
                    "line": 7,
                    "span": "at most 512 simultaneous connections",
                },
                {"text": "   ", "line": 1, "span": "# Vandrell Relay"},  # dropped: no text
                {"text": "Out of range.", "line": 900, "span": "nothing"},  # line clamped
            ]
        }
    )
    claims = decompose_text(client, DOC, "source_a.md")

    check(len(claims) == 4, f"empty claim text must be dropped, got {len(claims)} claims")
    check([c.id for c in claims] == ["A-001", "A-002", "A-003", "A-004"],
          "claim ids must be contiguous after a claim is dropped")
    check(claims[0].line == 5 and claims[0].anchored, "correct line should stay put")
    check(claims[1].line == 6 and claims[1].anchored, "a miscounted line must be corrected by span")
    check(not claims[2].anchored, "a paraphrased span must report anchored=False")
    check(claims[3].line == len(DOC.splitlines()),
          "an out-of-range line must be clamped to the document")
    check(all(c.source == "source_a.md" for c in claims), "source must be recorded on every claim")

    assert client.prompt is not None
    check("5 | The relay listens" in client.prompt,
          "the prompt must present the document with line numbers")
    check("{document}" not in client.prompt, "the document placeholder must be substituted")


class CheckingStubClient(StubClient):
    """A StubClient that runs the semantic check its caller handed it.

    `StubClient` answers whatever it was constructed with and asks nothing of
    it, which is right for the anchoring tests and useless for this one: the
    question here is whether `decompose_text` passes the claim checks to the
    client at all. A stub that ignores `semantic=` would pass whether the
    argument were there or not, which is how a check comes to be written, tested
    and never called.
    """

    def complete(self, *, messages, schema, semantic=None, **_) -> Completion:
        self.prompt = messages[-1]["content"]
        payload, defects, _truncations = parsing.parse(
            json.dumps(self.payload), schema, semantic)
        if defects:
            raise parsing.parse_error(schema, defects)
        return Completion(payload)


def looping_response(unique: int = 41, repeats: int = 449) -> dict:
    """The response that first exposed the loop, rebuilt: 489 claims of which 41 are unique.

    Constructed rather than recorded. The original needed a live model and has
    never been reproduced offline; a fixture is the honest way to exercise a
    guard against a response *shape*, and the shape is what the finding
    recorded — one sentence repeated 449 times, all of it for one line, inside
    a response that is otherwise complete and schema-valid.
    """
    looped = {
        "text": "The gateway returns HTTP 429 when the client exceeds its quota.",
        "line": 12,
        "span": "The gateway returns HTTP 429 when the client exceeds its quota.",
    }
    claims = [dict(looped) for _ in range(repeats)]
    claims += [{"text": f"Fact {i} is stated once.", "line": 20 + i,
                "span": f"Fact {i} is stated once."} for i in range(unique - 1)]
    return {"claims": claims}


def test_a_looping_decompose_response_is_refused_not_absorbed() -> None:
    """MUST FIRE. The claim count is not allowed to absorb 449 copies of one sentence."""
    payload = looping_response()
    check(len(payload["claims"]) == 489, "the probe must be the response the finding recorded")
    check(len({c["text"] for c in payload["claims"]}) == 41,
          "489 claims, 41 unique: that is the measurement, not a round number")

    faults = [f for f in parsing.check_claims(payload) if isinstance(f, parsing.RepeatFault)]
    check(len(faults) == 1, f"one repeated place, one fault, got {len(faults)}")
    check(faults and "449 times" in faults[0],
          f"the fault must carry the depth an operator can act on, got {faults[:1]}")

    client = CheckingStubClient(payload)
    try:
        claims = decompose_text(client, DOC, "source_a.md")
    except parsing.ParseError as exc:
        check(exc.looping, "a repeat fault must mark the error as a loop, or nothing bounds the re-asks")
    else:
        failures.append(
            f"decompose_text returned {len(claims)} claims for a response that is "
            f"449 copies of one sentence; the guard is not wired into the call")


def test_a_document_that_repeats_itself_is_not_a_loop() -> None:
    """MUST NOT FIRE. One fact per place, however many places, is an extraction."""
    # A changelog, a table of limits, a merge that concatenates two sources
    # saying the same thing: the same claim, once for each line that states it.
    repetitive = {"claims": [
        {"text": "The fee is 5 GBP.", "line": line, "span": "The fee is 5 GBP."}
        for line in range(1, 41)
    ]}
    check(parsing.check_claims(repetitive) == [],
          "40 copies of one fact on 40 different lines is a repetitive document, not a loop")

    client = CheckingStubClient(repetitive)
    claims = decompose_text(client, "The fee is 5 GBP.\n" * 40, "source_a.md")
    check(len(claims) == 40, f"every claim must survive, got {len(claims)}")

    # The deepest repetition at one place that recorded output has ever shown:
    # two, on 9 of the 1,359 decompose responses in this tree, one of them from
    # the 27B. Pinned to the measurement rather than to the constant, so a limit
    # tightened to 1 fails here instead of quietly failing a real model.
    twice = {"claims": [
        {"text": "The fee is 5 GBP.", "line": 3, "span": "The fee is 5 GBP."},
        {"text": "The fee is 5 GBP.", "line": 3, "span": "the fee is 5 GBP"},
    ]}
    check(parsing.check_claims(twice) == [],
          "a model restating one claim once is not a loop; the corpus does it")

    at_the_limit = {"claims": [
        {"text": "The fee is 5 GBP.", "line": 3, "span": "The fee is 5 GBP."}
    ] * parsing.CLAIM_REPEAT_LIMIT}
    check(parsing.check_claims(at_the_limit) == [],
          f"{parsing.CLAIM_REPEAT_LIMIT} at one place is the limit and must pass")
    over = {"claims": at_the_limit["claims"] + [dict(at_the_limit["claims"][0])]}
    check([f for f in parsing.check_claims(over) if isinstance(f, parsing.RepeatFault)],
          f"{parsing.CLAIM_REPEAT_LIMIT + 1} at one place is over the limit and must fail")


def test_no_recorded_response_looks_like_a_loop() -> None:
    """MUST NOT FIRE, on real output rather than on a fixture.

    Every decompose response this repository has recorded, re-graded by the
    shipped predicate. It is the control set the threshold was chosen against,
    and it is checked here rather than quoted in a comment so that lowering the
    limit fails the suite instead of a report.
    """
    graded = 0
    fired: list[str] = []
    deepest = 0
    for path in sorted((ROOT / "tests" / "responses").rglob("decompose-*.json")):
        recorded = json.loads(path.read_text(encoding="utf-8"))
        content = json.loads(recorded["response"]["raw"])["choices"][0]["message"].get("content")
        if not content:
            continue
        payload = json.loads(content)
        claims = payload.get("claims")
        if not isinstance(claims, list) or not claims:
            continue
        graded += 1
        places: dict[tuple, int] = {}
        for claim in claims:
            key = parsing._place(claim)
            places[key] = places.get(key, 0) + 1
        deepest = max(deepest, max(places.values()))
        if [f for f in parsing.check_claims(payload) if isinstance(f, parsing.RepeatFault)]:
            fired.append(path.name)

    check(graded >= 100, f"the control set must be the recorded corpus, graded {graded}")
    check(not fired, f"the guard fired on recorded output: {fired}")
    check(deepest < parsing.CLAIM_REPEAT_LIMIT,
          f"the deepest honest repetition on record is {deepest} and the limit is "
          f"{parsing.CLAIM_REPEAT_LIMIT}; a limit at or under it has no margin left")


def test_prompt_loading() -> None:
    prompt = prompts.load("decompose")
    check(len(prompt.sha256) == 64, "prompt hash must be a full sha256")
    check("{document}" in prompt.text, "decompose.md must carry a {document} placeholder")
    check(prompt.render(document="X").endswith("X\n") or "X" in prompt.render(document="X"),
          "render must substitute the document")

    try:
        prompt.render(nonsense="X")
    except KeyError:
        pass
    else:
        failures.append("render must reject a placeholder the prompt does not have")

    try:
        prompts.load("does_not_exist")
    except FileNotFoundError:
        pass
    else:
        failures.append("a missing prompt must be fatal, never substituted")


def test_runner_grading() -> None:
    """The fixture runner's grading, exercised without a model."""
    claims = [
        Claim("A-001", "source_a.md", "The relay listens on port 8443 by default.", 5, "", True),
        Claim("A-002", "source_a.md", "The default connect timeout is 30 seconds.", 20, "", True),
    ]
    probes = [
        {"probe_id": "listen-port", "document": "source_a.md", "line": 5, "must_extract": True,
         "match": {"all_of": ["listens on port", "8443"]}},
        {"probe_id": "connect-timeout", "document": "source_a.md", "line": 6, "must_extract": True,
         "match": {"all_of": ["connect timeout", "30 seconds"]}},
        {"probe_id": "log-format", "document": "source_a.md", "line": 9, "must_extract": True,
         "match": {"all_of": ["JSON Lines"]}},
        {"probe_id": "ignored", "document": "source_a.md", "line": 1, "must_extract": False,
         "match": {"all_of": ["Vandrell"]}},
    ]

    result = run_decompose.DocumentResult("stub", "source_a.md", claims, (1, 5))
    run_decompose.grade(result, probes)

    check(result.unmatched == ["log-format"], f"one probe should be unextracted, got {result.unmatched}")
    check("connect-timeout" in result.misplaced,
          f"a line {ANCHOR_RADIUS + 1}+ away should be flagged misplaced, got {result.misplaced}")
    check("listen-port" not in result.misplaced, "a correct line must not be flagged")
    check("ignored" not in result.matched, "must_extract=False probes are not graded")
    check(result.in_band and not result.ok, "a fixture with unmatched probes is not ok")

    clean = run_decompose.DocumentResult("stub", "source_a.md", claims[:1], (1, 5))
    run_decompose.grade(clean, probes[:1])
    check(clean.ok, "a document meeting every assertion must be ok")

    narrow = run_decompose.DocumentResult("stub", "source_a.md", claims[:1], (4, 9))
    run_decompose.grade(narrow, probes[:1])
    check(not narrow.in_band and not narrow.ok, "a count outside the band must fail")


def test_forbidden_reads_the_span_and_fails_the_document() -> None:
    """must_not_extract is an assertion, not an observation, and it sees the span.

    Both halves have been wrong. The pattern used to be matched against `text`
    alone, which missed the one defect it was written for — `ordering_only`
    returns the claim text `512` with a span reading `510` — and the sampled
    `ok` used to ignore violations entirely, so a tripped assertion printed in
    red and scored the document clean.
    """
    assertion = [{
        "assertion_id": "no-wrong-count",
        "pattern": r"(?i)\bat most (?!512\b)[\d,]+ concurrent connections",
    }]
    good = "The relay accepts at most 512 concurrent connections."
    bad = "The relay accepts at most 510 concurrent connections."

    clean = run_decompose.DocumentResult(
        "stub", "merged.md", [Claim("M-001", "merged.md", good, 7, good, True)], (1, 5))
    run_decompose.grade_forbidden(clean, assertion)
    check(not clean.forbidden, f"the correct count must not trip the assertion: {clean.forbidden}")

    # The defect as it actually appears: right text, wrong receipt.
    spanned = run_decompose.DocumentResult(
        "stub", "merged.md", [Claim("M-001", "merged.md", good, 7, bad, False)], (1, 5))
    run_decompose.grade_forbidden(spanned, assertion)
    check("no-wrong-count" in spanned.forbidden,
          "a correct claim text with a misrendered span must trip the assertion")
    check(spanned.forbidden["no-wrong-count"].startswith("span:"),
          f"the report must name which field tripped, got {spanned.forbidden['no-wrong-count']!r}")

    texted = run_decompose.DocumentResult(
        "stub", "merged.md", [Claim("M-001", "merged.md", bad, 7, good, True)], (1, 5))
    run_decompose.grade_forbidden(texted, assertion)
    check(texted.forbidden["no-wrong-count"].startswith("text:"),
          "a misrendered claim text must still trip, and be named as text")

    # Sampled over three runs, a violation in any one of them fails the document.
    samples = run_decompose.DocumentSamples([clean, spanned, clean])
    check("no-wrong-count" in samples.forbidden, "any-run violation must survive sampling")
    check(not samples.ok, "a document tripping must_not_extract must not be scored clean")
    check(run_decompose.DocumentSamples([clean, clean, clean]).ok,
          "a document tripping nothing must still be clean")


def test_modal_extraction() -> None:
    """Three runs of one document collapse to one outcome per probe."""
    probes = [
        {"probe_id": "listen-port", "document": "source_a.md", "line": 5, "must_extract": True,
         "match": {"all_of": ["listens on port", "8443"]}},
        {"probe_id": "log-format", "document": "source_a.md", "line": 9, "must_extract": True,
         "match": {"all_of": ["JSON Lines"]}},
    ]
    port = Claim("A-001", "source_a.md", "The relay listens on port 8443 by default.", 5, "", True)
    logs = Claim("A-002", "source_a.md", "Access logs use JSON Lines.", 9, "", True)

    def run(claims, band=(1, 5)):
        result = run_decompose.DocumentResult("stub", "source_a.md", list(claims), band)
        run_decompose.grade(result, probes)
        return result

    # log-format found twice out of three; listen-port found every time.
    doc = run_decompose.DocumentSamples([run([port, logs]), run([port]), run([port, logs])])
    check(doc.extracted("listen-port"), "a probe found in every run is extracted")
    check(doc.extracted("log-format"), "two runs out of three carry the probe")
    check(doc.unstable_probes == ["log-format"],
          f"only the probe that moved is unstable, got {doc.unstable_probes}")
    check(doc.unmatched == [], "a probe extracted by majority is not reported as unmatched")

    lost = run_decompose.DocumentSamples([run([port, logs]), run([port]), run([port])])
    check(not lost.extracted("log-format"), "one run out of three does not carry a probe")
    check(lost.unmatched == ["log-format"], "a probe missed by majority is unmatched")
    check(lost.unstable_probes == ["log-format"],
          "a probe can be both unmatched and unstable; they answer different questions")

    counts = run_decompose.DocumentSamples([run([port, logs]), run([port]), run([port, logs])])
    check(counts.counts == [2, 1, 2], f"claim counts are kept per run, got {counts.counts}")
    check(counts.count_range == "1-2", f"the range is reported, got {counts.count_range}")
    check(not counts.count_stable, "a claim count that moved is not stable")
    check(run_decompose.DocumentSamples([run([port]), run([port])]).count_stable,
          "a claim count that held is stable")

    # Band membership is a majority too: in band twice, out once.
    banded = run_decompose.DocumentSamples(
        [run([port, logs], (2, 5)), run([port], (2, 5)), run([port, logs], (2, 5))]
    )
    check(banded.in_band, "in band in two runs out of three is in band")
    check(not banded.band_stable, "a band verdict that moved is flagged")
    outvoted = run_decompose.DocumentSamples(
        [run([port, logs], (2, 5)), run([port], (2, 5)), run([port], (2, 5))]
    )
    check(not outvoted.in_band,
          "in band in one run out of three is out of band, not in it")

    # A probe whose line was right in the run that found it, wrong in another.
    drifted = Claim("A-002", "source_a.md", "Access logs use JSON Lines.", 40, "", True)
    mixed = run_decompose.DocumentSamples([run([port, logs]), run([port, drifted]), run([port, logs])])
    check(mixed.placed("log-format"), "right line in two runs of three is placed")
    check(not run_decompose.DocumentSamples(
        [run([port, drifted]), run([port, drifted]), run([port, logs])]
    ).placed("log-format"), "wrong line in two runs of three is misplaced")


def test_aggregate_zips_by_document() -> None:
    """N sweeps become one record per (fixture, document)."""
    def sweep(count):
        results = []
        for fixture in ("f1", "f2"):
            for document in ("source_a.md", "merged.md"):
                claims = [
                    Claim(f"X-{i}", document, f"claim {i}", 1, "", True) for i in range(count)
                ]
                results.append(run_decompose.DocumentResult(fixture, document, claims, (1, 9)))
        return results

    aggregated = run_decompose.aggregate([sweep(2), sweep(3), sweep(2)])
    check(len(aggregated) == 4, f"two fixtures x two documents, got {len(aggregated)}")
    check(all(len(d.runs) == 3 for d in aggregated), "every document carries all three runs")
    check(all(d.counts == [2, 3, 2] for d in aggregated), "counts are kept in run order")
    check([(d.fixture, d.document) for d in aggregated][0] == ("f1", "source_a.md"),
          "document order follows the first sweep")

    single = run_decompose.aggregate([sweep(2)])
    check(all(d.count_stable and d.count_range == "2" for d in single),
          "one sample degenerates to that sample, reported as stable")


def test_fixture_probes_are_matchable() -> None:
    """Every fixture probe must be matchable by its own text.

    Cheap, and it catches a match.all_of that only anchors to the document while
    being impossible for any reasonably-worded claim to satisfy.
    """
    import json

    for directory in sorted((ROOT / "tests" / "fixtures").iterdir()):
        if not directory.is_dir():
            continue
        expected = json.loads((directory / "expected.json").read_text())
        for probe in expected["probes"]:
            stand_in = Claim("X-001", probe["document"], probe["text"], probe["line"], "", True)
            check(
                run_decompose.match_probe(stand_in, probe["match"]["all_of"]),
                f"{expected['fixture']}/{probe['probe_id']}: "
                f"match.all_of does not match the probe's own text",
            )


def test_one_bad_call_errors_one_document_and_not_the_run() -> None:
    """Forward direction: containment.

    Previously only SchemaFailure was contained. Anything else - a dropped
    connection, an HTTP 500, a tier refusal - unwound to the outer handler and
    returned 2 with no report at all, so the more recoverable fault cost less
    than the less recoverable one.
    """
    calls: list[str] = []

    def fails_once(client, text, document, prompt):
        calls.append(document)
        if len(calls) == 1:
            raise RuntimeError("connection reset by peer")
        return original(client, text, document, prompt)

    original = run_decompose.decompose_text
    run_decompose.decompose_text = fails_once
    printed = io.StringIO()
    try:
        with contextlib.redirect_stdout(printed):
            code = run_decompose.main(
                ["--offline", "--no-colour", "--samples", "1"]
                + replay_models.replay_argv(roles=("decompose",)))
    finally:
        run_decompose.decompose_text = original

    output = printed.getvalue()
    check(len(calls) > 1,
          f"a failed call must not end the sweep; it made {len(calls)} call(s)")
    check(code == 2, f"a run with an errored document exits 2, got {code}")
    check("ERRORED" in output, "the errored document must be reported, not silently dropped")
    # The type survives into the message. "the endpoint answered nothing" and
    # "the model answered something unparseable" read alike once they are
    # strings, and they are different diagnoses.
    check("RuntimeError" in output, "the failure's type must reach the report; only its text did")
    check("ABANDONED" not in output, "one failure is not three")


def test_the_decompose_sweep_gives_up_after_three_consecutive_failures() -> None:
    """Other direction: contained is not the same as never abort."""
    def always_fails(*_args, **_kwargs):
        raise RuntimeError("endpoint gone")

    original = run_decompose.decompose_text
    run_decompose.decompose_text = always_fails
    printed = io.StringIO()
    try:
        with contextlib.redirect_stdout(printed):
            code = run_decompose.main(
                ["--offline", "--no-colour", "--samples", "3"]
                + replay_models.replay_argv(roles=("decompose",)))
    finally:
        run_decompose.decompose_text = original

    output = printed.getvalue()
    fixtures = len([p for p in (ROOT / "tests" / "fixtures").iterdir() if p.is_dir()])
    missing = fixtures * 3 - run_decompose.CONSECUTIVE_ERROR_LIMIT
    check(code == 2, f"an abandoned run exits 2, got {code}")
    check("ABANDONED" in output,
          "the operator must be told the sweep stopped early, not left to infer it")
    report = output[output.index("Decompose over the fixture set"):]
    check("ABANDONED" in report,
          "the abandonment must reach the report block, not only the sweep log")
    check(str(missing) in report,
          f"the report must name the {missing} units missing from every figure in it")
    check(report.index("ABANDONED") < report.index("Claims extracted"),
          "the warning must come before the coverage it qualifies, not after")


def test_a_dry_run_is_not_an_errored_document() -> None:
    """DryRun is why this was not the copy-and-paste it was described as.

    `client.complete` raises it from inside the call, so a catch-by-exclusion
    that did not name it in FATAL_TO_THE_RUN would swallow the signal, mark
    every document errored, and print a sweep report for a run that made no
    request. `run_merge.py`, whose tuple this one was copied from, has no
    dry-run path through a call and so could not have caught this.
    """
    check(run_decompose.DryRun in run_decompose.FATAL_TO_THE_RUN,
          "DryRun must end the run; contained, it becomes 36 errored documents")
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        code = run_decompose.main(
            ["--offline", "--no-colour", "--dry-run"] + replay_models.replay_argv(roles=("decompose",)))
    output = printed.getvalue()
    check(code == 0, f"a dry run exits 0, got {code}")
    check("dry run:" in output and "No request was made." in output,
          f"a dry run must report the plan; it printed {output[-200:]!r}")
    check("ERRORED" not in output and "ABANDONED" not in output,
          "a dry run measured nothing and must not be reported as a failed sweep")


class CeilingStubClient(StubClient):
    """A StubClient that keeps the `max_tokens` `decompose_text` asked for."""

    def __init__(self, payload: dict, **settings) -> None:
        super().__init__(payload)
        from dataclasses import replace
        self.settings = replace(self.settings, **settings)
        self.max_tokens: list = []

    def complete(self, *, messages, max_tokens=None, **_) -> Completion:
        self.max_tokens.append(max_tokens)
        return super().complete(messages=messages)


def test_the_ceiling_is_in_the_request_and_sized_from_the_document() -> None:
    """On the wire, from the document, and only where a profile wants one.

    The body is read off a real endpoint rather than a stub's arguments: a
    ceiling computed and never sent would pass a stub and bound nothing.
    """
    import tempfile
    from fake_endpoint import FakeEndpoint, envelope
    from llossless import decompose, merge, structured

    body = json.dumps({"claims": [{"text": "The relay listens on port 8443 by default.",
                                   "line": 5, "span": "The relay listens on port 8443 by default."}]})
    with tempfile.TemporaryDirectory() as raw:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(body)))
        with endpoint as base_url:
            client = Client(config.Settings(base_url=base_url, models={"verify": "test-model"},
                                            cache_dir=Path(raw) / "cache", use_cache=False))
            decompose_text(client, DOC, "source_a.md")
        asked = [r for r in endpoint.requests
                 if "DOCUMENT:" in (r.get("messages") or [{}])[-1].get("content", "")]
    want = decompose.budget_tokens(DOC, thinking=False)
    check(bool(asked) and all(r.get("max_tokens") == want for r in asked),
          f"the decompose request must carry max_tokens {want}, got "
          f"{[r.get('max_tokens') for r in asked]}")

    # Sized from the document: a longer one gets more, and never a fixed figure.
    longer = "\n".join([DOC] * 20)
    check(decompose.budget_tokens(longer, thinking=False) > want,
          "a longer document must get a larger ceiling")
    expected = (-(-int(decompose.CLAIM_COPIES * merge.escaped_length(longer)
                        / merge.CHARS_PER_TOKEN) // merge.BUDGET_STEP) * merge.BUDGET_STEP
                + merge.BUDGET_STEP)
    check(decompose.budget_tokens(longer, thinking=False) == expected,
          "the ceiling is CLAIM_COPIES of the escaped document in whole steps, plus one step")
    check(decompose.budget_tokens(DOC, thinking=True) == want + merge.REASONING_ALLOWANCE,
          "thinking on must add the reasoning allowance, and thinking off must not")

    # Through decompose_text: thinking on reaches the ceiling, and a
    # `CEILING_MODEL` profile sends none, as merge does.
    thinking = CeilingStubClient({"claims": []}, thinking=frozenset({"decompose"}))
    decompose_text(thinking, DOC, "source_a.md")
    check(thinking.max_tokens == [want + merge.REASONING_ALLOWANCE],
          f"a thinking-on decompose must be allowed its reasoning, got {thinking.max_tokens}")
    frontier = [name for name, profile in structured.PROFILES.items()
                if profile.output_ceiling == structured.CEILING_MODEL]
    for name in frontier:
        stub = CeilingStubClient({"claims": []}, profile=name)
        decompose_text(stub, DOC, "source_a.md")
        check(stub.max_tokens == [None], f"profile {name} must send no ceiling, got {stub.max_tokens}")
    check(bool(frontier), "at least one profile must leave the ceiling to the endpoint")


def recorded_decompose_answers() -> list[tuple[str, str, int, str | None]]:
    """Every recorded decompose answer: (file, document, completion tokens, finish reason).

    The document is rebuilt from the rendered prompt the way `decompose_text`
    built it: the text after `DOCUMENT:`, less the template's closing newline,
    with each `N | ` prefix taken off.
    """
    import re
    prefix = re.compile(r"^\s*\d+ \| ?")
    out = []
    for path in sorted((ROOT / "tests" / "responses").rglob("decompose-*.json")):
        recorded = json.loads(path.read_text(encoding="utf-8"))
        rendered = recorded["request"]["messages"][0]["content"]
        if "DOCUMENT:\n" not in rendered:
            continue
        block = rendered.split("DOCUMENT:\n", 1)[1]
        block = block[:-1] if block.endswith("\n") else block
        document = "\n".join(prefix.sub("", line, count=1) for line in block.split("\n"))
        response = json.loads(recorded["response"]["raw"])
        usage = response.get("usage") or {}
        if usage.get("completion_tokens") is None:
            continue
        out.append((str(path.relative_to(ROOT)), document, usage["completion_tokens"],
                    response["choices"][0].get("finish_reason")))
    return out


def over_ceiling(answers, ceiling) -> list[str]:
    """The recorded answers `ceiling(document)` would have cut."""
    return [f"{name}: {tokens} tokens against {ceiling(document)}"
            for name, document, tokens, _ in answers if tokens > ceiling(document)]


def test_no_recorded_answer_is_one_the_ceiling_would_cut() -> None:
    """MUST NOT FIRE, on real output: the ceiling against every recorded decompose answer.

    The control set the constant was checked against, graded
    by the shipped function, so a lower `CLAIM_COPIES` fails the suite rather
    than a recording. After the 27B import this is the new corpus, and it
    also holds that none of it was recorded truncated.
    """
    from llossless import decompose, window

    answers = recorded_decompose_answers()
    check(len(answers) >= 100, f"the control set must be the recorded corpus, got {len(answers)}")
    shipped = lambda text: decompose.budget_tokens(text, thinking=False)  # noqa: E731
    cut = over_ceiling(answers, shipped)
    check(not cut, f"the ceiling would have cut recorded answers: {cut[:3]}")
    truncated = [name for name, _, _, finish in answers if finish == "length"]
    check(not truncated, f"recorded decompose answers ended on the length limit: {truncated[:3]}")

    # MUST FIRE: the same check, handed a quarter of the ceiling, finds answers
    # it would cut -- so an empty list above is a measurement, not a blind spot.
    check(over_ceiling(answers, lambda text: shipped(text) // 4),
          "a quarter of the ceiling must cut something, or the check cannot fire")

    # The corpus's longest document still fits the re-record's declared window
    # with its whole ceiling beside the prompt, so the cut to the window
    # does not bite on it and the ceiling goes out uncut.
    longest = max(answers, key=lambda a: len(a[1]))
    rendered = prompts.load("decompose").render(document=number_lines(longest[1]))
    needed = len(rendered) // window.CHARS_PER_TOKEN + shipped(longest[1])
    check(needed <= 32768,
          f"the longest recorded document ({longest[0]}, {len(longest[1])} chars) needs "
          f"{needed} tokens with its ceiling, over the 32768 the re-record declares")


# A document of exactly 15,000 characters, the size of the operator's own that
# an earlier preflight refused at 32,768: prose lines of fixture length.
LONG_DOC = "\n".join(
    f"Setting {i} of the relay defaults to {i * 7} and is read once at start-up."
    for i in range(1, 400))[:15000]


def decompose_requests(endpoint) -> list[dict]:
    """The decompose calls a FakeEndpoint received, as sent."""
    return [r for r in endpoint.requests
            if "DOCUMENT:" in (r.get("messages") or [{}])[-1].get("content", "")]


def prompt_estimate(text: str) -> int:
    """The prompt figure the preflight charges for decomposing `text`."""
    from llossless import window
    rendered = prompts.load("decompose").render(document=number_lines(text))
    return len(rendered) // window.CHARS_PER_TOKEN


def decompose_at(text: str, tokens: int, raw: Path, **settings):
    """Decompose `text` through a real endpoint at a stated window.

    Returns (the decompose requests the endpoint received, the refusal or None).
    """
    from fake_endpoint import FakeEndpoint, envelope
    from llossless import window

    refused = None
    endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(json.dumps({"claims": []}))))
    with endpoint as base_url:
        client = Client(config.Settings(base_url=base_url, models={"verify": "test-model"},
                                        cache_dir=raw / "cache", use_cache=False,
                                        window=tokens, **settings))
        try:
            decompose_text(client, text, "source_a.md")
        except window.BudgetExceedsWindow as exc:
            refused = exc
    return decompose_requests(endpoint), refused


def test_a_document_the_window_holds_is_sent_with_its_ceiling_cut_to_fit() -> None:
    """MUST FIRE: a 15,000-character document at 32,768 is admitted.

    The preflight used to charge the whole ceiling and refuse this before the
    call, although the window holds the prompt with room to answer. The
    ceiling is a runaway cap and the window is one too, so the ceiling is cut
    to what the window leaves, on the wire.
    """
    import tempfile
    from llossless import decompose

    ceiling = decompose.budget_tokens(LONG_DOC, thinking=False)
    prompt = prompt_estimate(LONG_DOC)
    check(len(LONG_DOC) == 15000 and prompt + ceiling > 32768,
          f"the probe must be one the whole ceiling cannot fit: {len(LONG_DOC)} chars, "
          f"prompt {prompt} + ceiling {ceiling}")
    with tempfile.TemporaryDirectory() as raw:
        asked, refused = decompose_at(LONG_DOC, 32768, Path(raw))
    check(refused is None, f"a 15,000-character document must be admitted at 32,768, got: {refused}")
    sent = [r.get("max_tokens") for r in asked]
    check(sent == [32768 - prompt],
          f"max_tokens must be cut to the window less the prompt ({32768 - prompt}), "
          f"not the ceiling ({ceiling}); sent {sent}")


def test_a_prompt_the_window_cannot_hold_is_still_refused() -> None:
    """MUST FIRE: the prompt, and a minimum answer beside it, are still charged.

    Refused before anything is sent, at the boundary on both sides: a window
    one token short of the prompt, and one that leaves less than a
    `BUDGET_STEP` to answer in. One token more is admitted, with that step as
    its ceiling.
    """
    import tempfile
    from llossless import merge

    prompt = prompt_estimate(DOC)
    reserve = merge.BUDGET_STEP
    with tempfile.TemporaryDirectory() as raw:
        for tokens, why in ((prompt - 1, "the prompt alone overflows"),
                            (prompt + reserve - 1, "no room is left to answer in")):
            asked, refused = decompose_at(DOC, tokens, Path(raw))
            check(refused is not None and not asked,
                  f"at a {tokens}-token window ({why}) the call must be refused and "
                  f"nothing sent; refused={refused is not None}, sent {len(asked)}")
        asked, refused = decompose_at(DOC, prompt + reserve, Path(raw))
        check(refused is None and [r.get("max_tokens") for r in asked] == [reserve],
              f"a window that leaves exactly {reserve} tokens must send the call with "
              f"max_tokens {reserve}; refused={refused}, sent "
              f"{[r.get('max_tokens') for r in asked]}")
        # A document well past the window, not only a boundary.
        big = "\n".join([LONG_DOC] * 3)
        asked, refused = decompose_at(big, 8192, Path(raw))
        check(refused is not None and not asked,
              f"a {len(big)}-character document must be refused at 8,192")


def fixture_documents() -> list[Path]:
    """Every document the recording runners decompose from the repository."""
    return sorted([p for p in (ROOT / "tests" / "fixtures").glob("*/*.md")]
                  + [p for p in (ROOT / "tests" / "pairs").glob("*/*.md")])


def test_the_fixtures_keep_their_cassette_keys() -> None:
    """The cut to the window must not re-key the corpus it is recorded on.

    `max_tokens` is a key component. Recorded at the re-record's 32,768
    window, every fixture document must go out with its whole ceiling and
    replay with no window, where the ceiling is sent as is.
    MUST FIRE: the 15,000-character document, whose ceiling is cut at 32,768,
    recorded the same way, misses on that replay.
    """
    import tempfile
    from fake_endpoint import FakeEndpoint, envelope
    from llossless import decompose, window
    from llossless.cassette import MissingCassette

    documents = {str(p.relative_to(ROOT)): p.read_text(encoding="utf-8")
                 for p in fixture_documents()}
    check(len(documents) >= 75, f"the fixture set must be the corpus's, got {len(documents)}")
    documents["LONG_DOC"] = LONG_DOC
    common = dict(models={"verify": "test-model"}, use_cache=False,
                  profile="openai-compatible", structured="json_schema", pinned=True,
                  field_order="any")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(json.dumps({"claims": []}))))
        uncut, refused = [], []
        with endpoint as base_url:
            recording = Client(config.Settings(base_url=base_url, cache_dir=tmp / "cache",
                                               record_dir=tmp / "rec", window=32768, **common))
            for name, text in documents.items():
                before = len(decompose_requests(endpoint))
                try:
                    decompose_text(recording, text, "source_a.md")
                except window.BudgetExceedsWindow:
                    refused.append(name)
                    continue
                sent = [r.get("max_tokens") for r in decompose_requests(endpoint)[before:]]
                if name != "LONG_DOC" and sent != [decompose.budget_tokens(text, thinking=False)]:
                    uncut.append(f"{name}: sent {sent}, ceiling "
                                 f"{decompose.budget_tokens(text, thinking=False)}")
        check(not refused, f"documents refused at 32,768: {refused[:3]}")
        check(not uncut, f"a fixture document went out with a cut ceiling at 32,768: {uncut[:3]}")

        replaying = Client(config.Settings(base_url="http://127.0.0.1:1/v1", cache_dir=tmp / "c2",
                                           replay_dir=tmp / "rec", **common))
        missed = []
        for name, text in documents.items():
            try:
                decompose_text(replaying, text, "source_a.md")
            except MissingCassette:
                missed.append(name)
        check([m for m in missed if m != "LONG_DOC"] == [],
              f"fixture documents recorded at 32,768 must replay with no window: {missed[:3]}")
        check("LONG_DOC" in missed,
              "the cut 15,000-character document must miss with no window, or the replay "
              "check cannot tell a changed key from an unchanged one")


def test_decompose() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_decompose" and callable(function):
            function()

    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("decompose: all offline checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
