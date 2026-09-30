#!/usr/bin/env python3
"""`run_detect.grade` and `--regrade`, on synthetic reports. Offline; no call.

A registered depth re-run on 2026-09-24 scored `full` as `attribution_swapped:
detected 2/2, invented 2`, which trips the pre-registered disqualifier. The two
"inventions" were the same two misattributions reported twice: once by the
model's reverse pass, once by `reconcile.attribution_findings`. `grade()`
accounted only the first finding anchored in each probe, so the second family's
report of the defect it had just credited was scored as a different
defect entirely.

Each check below holds one thing constant and varies the defect, and each is
seeded against the code it guards: the first fails on the old rule; the second
on a fix that stops counting inventions once a plant is found; the third on a
fix that lets a second report hide from the guard probes. The last drives the
command a regrade is run with, over a saved run it must not touch.

The last two are not synthetic: a benchmark clone pinned at one commit has no
`.venv` of its own, and `run_detect.py` used to shell out to
`ROOT/.venv/bin/llossless` -- the *working* repo's editable install -- so a
pinned run silently graded master's code under the clone's commit label.
`run_one` now runs `python -m llossless` with the clone's own
`src/` first on `PYTHONPATH`, and `check_provenance` refuses a report whose
own `provenance.claimcheck_commit` disagrees with this tree's HEAD. The
must-fire check reproduces the shape of the original bug -- a second copy of
`llossless`, its own commit, resolved ahead of this tree's -- with a real
subprocess and a real (if disposable) git repository, not a mocked one; the
must-not-fire check is `run_one` against this tree's own fixtures, unchanged.

The two `errored` checks grade an exit 2 as what it is, a run
that took no reading, rather than as a miss: the must-fire is every fixture
of the block lost to a 429, the must-not-fire a clean run and a plain miss.

Run with `python3 tests/test_run_detect.py`, or collect with pytest.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import run_detect  # noqa: E402

failures: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


# One planted misattribution and one guard claim, in `attribution_swapped`'s
# shape but none of its text.
EXPECTED = {
    "kind": "defect",
    "expected_exit_code": {"strict": 1, "lenient": 1},
    "probes": [
        {"probe_id": "m-notes-attribution", "expected_finding": "contradicted",
         "direction": "merged_to_sources", "expected_verdict": "CONTRADICTED",
         "anchor": {"all_of": ["According to the Field Notes", "pump runs at 40 litres"]}},
        {"probe_id": "a-valve", "expected_finding": "none",
         "direction": "source_to_merged", "expected_verdict": "SUPPORTED",
         "anchor": {"all_of": ["valve opens at 3 bar"]}},
    ],
}
CLAIMS = [
    {"id": "M-001", "text": "According to the Field Notes, the pump runs at 40 litres a minute.",
     "span": "According to the Field Notes, the pump runs at 40 litres a minute."},
    {"id": "S-001", "text": "The valve opens at 3 bar.", "span": "The valve opens at 3 bar."},
    {"id": "M-002", "text": "The tank holds 900 litres.", "span": "The tank holds 900 litres."},
]
# The reverse pass's report of the plant.
REVERSE = {"claim_id": "M-001", "verdict": "CONTRADICTED", "finding": "contradicted",
           "direction": "merged_to_sources", "evidence": "The pump runs at 25 litres a minute.",
           "rationale": "The Field Notes give 25 litres a minute, not 40."}
# `reconcile.attribution_findings`' report of the same sentence.
MECHANICAL = {"kind": "misattributed", "segment": "m1", "document": "source_b.md",
              "detail": "the merge credits the pump rate to the Field Notes, which do not state it",
              "source_text": "The pump runs at 40 litres a minute.",
              "merge_text": "According to the Field Notes, the pump runs at 40 litres a minute.",
              "difference": ""}
GUARD_VERDICT = {"claim_id": "S-001", "verdict": "SUPPORTED", "finding": "none",
                 "direction": "source_to_merged", "evidence": "The valve opens at 3 bar.",
                 "rationale": ""}


def report(findings: list[dict], mechanical: list[dict], verdicts: list[dict]) -> dict:
    return {"claims": CLAIMS, "findings": findings, "verdicts": verdicts,
            "attributions": {"findings": mechanical}}


def test_two_families_reporting_one_plant_invent_nothing() -> None:
    graded = run_detect.grade(EXPECTED, report([REVERSE], [MECHANICAL], [REVERSE, GUARD_VERDICT]), 1)
    check(graded["detected"] == ["m-notes-attribution"],
          f"the plant must be detected: {graded['detected']}")
    check(graded["invented_findings"] == [],
          f"a second report of a detected plant is not an invention: {graded['invented_findings']}")
    probe = next(p for p in graded["probes"] if p["probe_id"] == "m-notes-attribution")
    matched = [(m["finding"], m["claim_id"]) for m in probe.get("matched_findings", [])]
    check(matched == [("contradicted", "M-001"), ("misattributed", None)],
          f"the probe must record both families that matched it, detector first: {matched}")
    check([s["finding"] for s in graded.get("second_reports", [])] == ["misattributed"],
          f"the second report must be listed as one: {graded.get('second_reports')}")
    check(graded["outcome"] == "matched" and not run_detect.disqualified(
              [{**graded, "fixture": "synthetic"}]),
          f"one plant reported twice must not disqualify: {graded['outcome']}")


def test_a_finding_anchored_in_no_probe_is_still_invented() -> None:
    """Finding the plant licenses reporting it again, not reporting something else."""
    stray = {"claim_id": "M-002", "verdict": "CONTRADICTED", "finding": "contradicted",
             "direction": "merged_to_sources", "evidence": "The tank holds 800 litres.",
             "rationale": "The sources give 800 litres."}
    stray_mechanical = {"kind": "misattributed", "segment": "m2", "document": "source_a.md",
                        "detail": "the merge credits the tank size to the wrong document",
                        "source_text": "The tank holds 800 litres.",
                        "merge_text": "The tank holds 900 litres.", "difference": ""}
    graded = run_detect.grade(
        EXPECTED, report([REVERSE, stray], [MECHANICAL, stray_mechanical],
                         [REVERSE, stray, GUARD_VERDICT]), 1)
    invented = [(i["finding"], i["claim_id"], i["evidence"]) for i in graded["invented_findings"]]
    check(invented == [("contradicted", "M-002", "The tank holds 800 litres."),
                       ("misattributed", None, "The tank holds 900 litres.")],
          f"both unanchored findings must be invented, each read by its own family's "
          f"keys: {invented}")
    check(any("invented finding(s) beside the seeded defect" in line
              for line in run_detect.disqualified([{**graded, "fixture": "synthetic"}])),
          "an invention beside a detected plant must still disqualify")


def test_a_second_report_on_a_guard_claim_is_still_guard_wrong() -> None:
    """Whatever else it matched, a finding on a guard probe's own claim is a false alarm there."""
    both = {"claim_id": "S-001", "verdict": "CONTRADICTED", "finding": "contradicted",
            "direction": "source_to_merged", "evidence": "The valve opens at 3 bar.",
            "rationale": "The merge says: According to the Field Notes, the pump runs "
                         "at 40 litres a minute; it drops the valve."}
    graded = run_detect.grade(
        EXPECTED, report([REVERSE, both], [MECHANICAL], [REVERSE, both]), 1)
    probe = next(p for p in graded["probes"] if p["probe_id"] == "m-notes-attribution")
    check(("contradicted", "S-001") in [(m["finding"], m["claim_id"])
                                        for m in probe.get("matched_findings", [])],
          "the fixture proves nothing unless the finding is anchored in the plant too")
    check(graded["guard_wrong"] == ["a-valve"],
          f"a finding on the guard's own claim must grade it wrong: {graded['guard_wrong']}")
    guard = next(p for p in graded["guard_probes"] if p["probe_id"] == "a-valve")
    check(guard["verdict"] == "false_alarm" and guard["claim_id"] == "S-001",
          f"the guard must be wrong by that finding, as a false alarm: {guard}")
    check(any("guard probe(s) graded wrong" in line
              for line in run_detect.disqualified([{**graded, "fixture": "synthetic"}])),
          "a guard graded wrong must still disqualify")
    # The same finding with no verdict behind it, as a report carrying only
    # its findings would have it. Only the false-alarm path can see it here, so
    # a rule that hid second reports from the guard probes leaves it unclaimed.
    graded = run_detect.grade(EXPECTED, report([REVERSE, both], [MECHANICAL], [REVERSE]), 1)
    check(graded["guard_wrong"] == ["a-valve"],
          f"with no verdict to fall back on, the finding alone must grade the guard "
          f"wrong: {graded['guard_wrong']}")


def digest(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def test_regrade_reads_a_saved_run_and_writes_nothing_beside_it() -> None:
    saved = run_detect.FIXTURES_DIR
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fixtures = root / "fixtures" / "synthetic"
        fixtures.mkdir(parents=True)
        (fixtures / "expected.json").write_text(json.dumps(EXPECTED), encoding="utf-8")
        run = root / "run"
        (run / "full-reports").mkdir(parents=True)
        body = report([REVERSE], [MECHANICAL], [REVERSE, GUARD_VERDICT])
        (run / "full-reports" / "synthetic.json").write_text(json.dumps(body), encoding="utf-8")
        # The run's own record, graded under the old rule: two inventions.
        (run / "full").write_text(json.dumps({
            "summary": {"label": "full-x", "passthrough": ["--model", "m"],
                        "plants_detected": 1, "invented_total": 1, "guard_wrong_total": 0,
                        "disqualified": ["synthetic: 1 invented finding(s) beside the seeded defect"]},
            "records": [{"fixture": "synthetic", "exit_code": 1, "wall_seconds": 9.5,
                         "stderr_tail": []}]}), encoding="utf-8")
        before = digest(run)
        out = root / "regraded"
        try:
            run_detect.FIXTURES_DIR = root / "fixtures"
            sink = io.StringIO()
            with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
                code = run_detect.main(["--regrade", str(run), "--out", str(out)])
                inside = run_detect.main(["--regrade", str(run), "--out", str(run / "x")])
        finally:
            run_detect.FIXTURES_DIR = saved
        check(code == 0, f"the regrade exited {code}: {sink.getvalue()[-400:]}")
        check(inside == 2 and not (run / "x").exists(),
              "an --out inside the regraded directory must be refused")
        check(digest(run) == before, "the regrade changed the saved run")
        written = out / "full.json"
        check(written.is_file(), f"no {written.name} written: {sorted(p.name for p in out.glob('*'))}")
        if written.is_file():
            result = json.loads(written.read_text(encoding="utf-8"))
            summary, record = result["summary"], result["records"][0]
            check(summary["invented_total"] == 0 and summary["disqualified"] == [],
                  f"regraded summary: {summary}")
            check(summary.get("as_run", {}).get("invented_total") == 1,
                  "the regrade must carry the run's own scoring beside its own")
            check(record["exit_code"] == 1 and record["exit_code_from"] == "run record"
                  and record["wall_seconds"] == 9.5,
                  f"the exit status graded must be the one the run recorded: {record}")


def _init_fake_tree(root: Path) -> str:
    """A second, disposable copy of `llossless`, its own git repository.

    A *copy*, not a symlink: `config.ROOT` is `Path(__file__).resolve().parents[2]`,
    and `.resolve()` follows a symlink back to the real file, which would quietly
    give the real tree's commit and prove nothing. Prompts come with it --
    `llossless` looks for `<root>/prompts` beside its own package, and a
    `--dry-run` call that cannot find them never gets far enough to write a
    report. Returns the fake tree's own HEAD, 12 hex characters.
    """
    shutil.copytree(ROOT / "src" / "llossless", root / "src" / "llossless",
                    ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "prompts", root / "prompts")
    git = lambda *args: subprocess.run(  # noqa: E731
        ["git", *args], cwd=root, capture_output=True, text=True, check=True)
    git("init", "-q")
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "test")
    git("add", "-A")
    git("commit", "-q", "-m", "fake tree")
    return git("rev-parse", "HEAD").stdout.strip()[:12]


def test_run_one_must_not_fire_on_this_trees_own_report() -> None:
    """The normal case: this tree's own code, checked against this tree's own HEAD.

    `--model` is named explicitly (`test_cli.py`'s own convention for a
    `--dry-run` subprocess): an unconfigured environment -- the one this suite
    runs under in a publication rehearsal -- has none, `llossless` then exits
    2 before writing a report, and `run_one`'s `if report:` guard means
    `check_provenance` is never reached at all. A must-not-fire probe that
    passes for that reason proves nothing.
    """
    record = run_detect.run_one("dedup", ["--dry-run", "--model", "test-model"], None)
    check(record.get("report_written") is True,
          f"a clean --dry-run against this tree must write a report, "
          f"or `check_provenance` was never reached: {record}")


def test_check_provenance_must_fire_on_a_foreign_tree() -> None:
    """The stale-install bug, reproduced: a report from a DIFFERENT tree's copy of `llossless`
    -- resolved first on `PYTHONPATH`, exactly how a stale `.venv` install
    would shadow this tree's own `src/` -- must be refused, loudly, not scored
    under this tree's commit."""
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp) / "fake"
        fake_commit = _init_fake_tree(fake)
        check(fake_commit != run_detect.tree_commit(),
              f"the fixture must vary the commit from this tree's own: both "
              f"{fake_commit!r}")

        def foreign_env() -> dict[str, str]:
            env = dict(os.environ)
            env["PYTHONPATH"] = str(fake / "src")
            return env

        real_child_env = run_detect._child_env
        run_detect._child_env = foreign_env
        try:
            raised = None
            record = None
            try:
                record = run_detect.run_one(
                    "dedup", ["--dry-run", "--model", "test-model"], None)
            except SystemExit as exc:
                raised = exc
        finally:
            run_detect._child_env = real_child_env
        check(raised is not None,
              f"a report from a foreign tree must raise, not return a record: {record}")
        check(raised is not None and "not this tree's HEAD" in str(raised)
              and fake_commit in str(raised),
              f"the refusal must name the foreign commit it found: {raised}")


def _finish(records: list[dict]) -> tuple[int, dict, str]:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "arm.json"
        sink = io.StringIO()
        with contextlib.redirect_stdout(sink):
            code = run_detect.finish(records, "arm", [], out)
        return code, json.loads(out.read_text(encoding="utf-8"))["summary"], sink.getvalue()


def test_an_exit_2_is_errored_not_missed() -> None:
    """Must fire. An arm whose every call hit a 429 read "missed 13/13,
    plants 0/7" and stayed in both denominators; it took no reading at all."""
    records = [run_detect.record_of(name, {}, 2, wall_seconds=1.0, report_ref=None,
                                    stderr_tail=["HTTP 429 Too Many Requests"])
               for name in run_detect.block_names()]
    check(all(r["outcome"] == "errored" for r in records),
          f"exit 2 with no report must be errored: {[r['outcome'] for r in records]}")
    code, summary, printed = _finish(records)
    check(summary["exit_code_missed"] == [] and summary["fixtures_measured"] == 0
          and len(summary["exit_code_errored"]) == len(records)
          and summary["plants_errored"] == summary["plants_total"]
          and summary["plants_detected"] == 0 and summary["disqualified"] == [],
          f"an errored fixture must leave every denominator and disqualify nothing: {summary}")
    check(code == 2, f"finish() must say `retry` (2) for an arm that only errored, got {code}")
    check("ERRORED" in printed and "HTTP 429" in printed,
          "finish() must list the errored fixtures with their stderr")
    # A partial report behind an exit 2: its findings are not read.
    partial = run_detect.record_of(
        "dedup", {"claims": CLAIMS, "findings": [REVERSE], "verdicts": [REVERSE]}, 2,
        wall_seconds=1.0, report_ref=None, stderr_tail=[])
    _, summary, _ = _finish([partial])
    check(partial["outcome"] == "errored" and summary["invented_total"] == 0,
          f"an exit 2 with a partial report is errored and invents nothing: "
          f"{partial['outcome']}, {summary['invented_total']}")
    # And a report-less run that did not exit 2 (killed, say) is errored too.
    killed = run_detect.record_of("hallucination", {}, -9, wall_seconds=1.0,
                                  report_ref=None, stderr_tail=[])
    check(killed["outcome"] == "errored", f"no report is errored: {killed['outcome']}")


def test_a_finished_run_is_never_errored() -> None:
    """Must not fire: a run that exited 0 or 1 with a report is graded."""
    clean = run_detect.record_of("dedup", {"claims": [], "findings": [], "verdicts": []}, 0,
                                 wall_seconds=1.0, report_ref=None, stderr_tail=[])
    missed = run_detect.record_of("hallucination", {"claims": [], "findings": [],
                                                    "verdicts": []}, 0,
                                  wall_seconds=1.0, report_ref=None, stderr_tail=[])
    check(clean["outcome"] == "matched", f"a clean exit on a guard fixture: {clean['outcome']}")
    check(missed["outcome"] == "missed",
          f"a seeded defect that exited clean is still missed: {missed['outcome']}")
    code, summary, _ = _finish([clean, missed])
    check(code == 1 and summary["exit_code_errored"] == [] and summary["fixtures_measured"] == 2,
          f"no errored fixture, one miss: exit {code}, {summary}")


def test_run_detect_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_run_detect_offline" and callable(function):
            try:
                function()
            except Exception as exc:  # noqa: BLE001 - a crashing check is a failing check
                failures.append(f"{name} raised {type(exc).__name__}: {exc}")
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"run_detect: {checks} checks pass on synthetic reports")
    return 0


if __name__ == "__main__":
    sys.exit(main())
