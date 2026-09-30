#!/usr/bin/env python3
"""The sweep driver's three guards, each proved to refuse. Offline; no call.

`tests/run_arm.py` exists because arm X passed every assertion the scratchpad
driver had and started live GPU work anyway. The guards it grew in response
protect a sweep that is now finished, so none of them will fire in a real run
again, which is precisely the condition under which a guard rots unnoticed.
An earlier reconciler is the local precedent: eight checks written, seven never
called, and a check that does not run passes.

So each guard is exercised here against the case it was written for, not
against a case it is bound to survive. The negative controls matter as much as
the positive ones: a guard that refuses everything is as useless as one that
refuses nothing, and half of these assert that the legitimate invocation is
allowed through.

Run with `python3 tests/test_run_arm.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Nothing here opens a socket; the guard is how that is stated.
socket_guard.install()

import run_arm  # noqa: E402

failures: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


# -- layer 1: no live call without --record ---------------------------------

def test_layer1_a_bare_invocation_dry_runs_every_unit() -> None:
    for label in sorted(run_arm.ARMS):
        for pair, level, sample in run_arm.plan_for(label):
            argv = run_arm.unit_argv(label, pair, level, sample, Path("/nowhere"),
                                     record=False)
            check("--dry-run" in argv,
                  f"layer 1: {label} {pair}/{level}/s{sample} without --record "
                  f"built a command with no --dry-run")
            check(not run_arm.live_calls_permitted(argv),
                  f"layer 1: {label} {pair}/{level}/s{sample} without --record "
                  f"is reported as permitted to make live calls")


def test_layer1_record_is_the_only_way_to_a_live_call() -> None:
    argv = run_arm.unit_argv("B", "badge_access", "off", 0, Path("/nowhere"),
                             record=True)
    check("--dry-run" not in argv, "layer 1: --record still appended --dry-run")
    check(run_arm.live_calls_permitted(argv),
          "layer 1: --record did not produce a command permitted to call live")


def test_layer1_the_arm_carries_its_own_thinking_roles() -> None:
    """A.11: arm T is the merge role only, and the size arms carry none."""
    t = run_arm.unit_argv("T", "badge_access", "off", 0, Path("/nowhere"), record=True)
    check(t.count("--thinking") == 1 and t[t.index("--thinking") + 1] == "merge",
          f"arm T did not pass --thinking merge exactly once: {t}")
    for label in ("A", "B", "C"):
        argv = run_arm.unit_argv(label, "badge_access", "off", 0, Path("/nowhere"),
                                 record=True)
        check("--thinking" not in argv, f"size arm {label} passed --thinking")


# -- layer 2: the arm label is closed ---------------------------------------

def test_layer2_refuses_the_label_that_started_arm_x() -> None:
    """`X` was well-formed in shape. Shape was never the question."""
    refusal = run_arm.guard_known_arm("X", "qwen3:8b", 40960)
    check(refusal is not None and "unknown arm" in refusal,
          f"layer 2: arm X was not refused by name, got {refusal!r}")


def test_layer2_refuses_a_known_label_pointed_at_another_model() -> None:
    refusal = run_arm.guard_known_arm("B", "qwen3.8:27b", 40960)
    check(refusal is not None and "qwen3:8b" in refusal,
          f"layer 2: arm B at the 27B model was not refused, got {refusal!r}")


def test_layer2_refuses_a_known_label_at_another_window() -> None:
    """Size and window are two axes; A.8:682 pins arm B's at 40960."""
    refusal = run_arm.guard_known_arm("B", "qwen3:8b", 65536)
    check(refusal is not None and "40960" in refusal,
          f"layer 2: arm B at 65536 was not refused, got {refusal!r}")


def test_layer2_admits_each_arm_as_it_actually_ran() -> None:
    for label, spec in sorted(run_arm.ARMS.items()):
        refusal = run_arm.guard_known_arm(label, spec["model"], spec["num_ctx"])
        check(refusal is None,
              f"layer 2: arm {label} as registered was refused: {refusal!r}")


# -- layer 3: an arm that already has records ------------------------------

def test_layer3_predicate_is_never_the_journal() -> None:
    """Arm A's journal held 26 rows over 28 unit artifacts.

    A restart skips a finished unit and appends nothing, so the journal
    undercounts by exactly the population this guard exists to protect. The
    directory below reproduces that: a journal claiming the arm is empty, over
    a unit record that says otherwise.
    """
    with tempfile.TemporaryDirectory() as tmp:
        arm = Path(tmp) / "arms" / "B"
        (arm / "off").mkdir(parents=True)
        (arm / "journal.jsonl").write_text("", encoding="utf-8")
        (arm / "off" / "badge_access.json").write_text('{"exit_code": 1}',
                                                       encoding="utf-8")
        found = run_arm.unit_artifacts(arm)
        check([p.name for p in found] == ["badge_access.json"],
              f"layer 3: unit_artifacts missed the record, saw {found}")
        refusal = run_arm.guard_settled_arm(arm, record=True, append=False)
        check(refusal is not None and "1 unit artifact" in refusal,
              f"layer 3: an empty journal over a real record was not refused, "
              f"got {refusal!r}")


def test_layer3_refuses_on_the_sentinel_alone() -> None:
    """The sentinel refuses even where no unit record survived the run."""
    with tempfile.TemporaryDirectory() as tmp:
        arm = Path(tmp) / "arms" / "C"
        arm.mkdir(parents=True)
        (arm / "sentinel.json").write_text(json.dumps(
            {"arm": "C", "units_planned": 28, "units_settled": 28,
             "finished_at": "2026-08-23T01:12:00Z"}), encoding="utf-8")
        refusal = run_arm.guard_settled_arm(arm, record=True, append=False)
        check(refusal is not None and "already settled" in refusal,
              f"layer 3: a settled sentinel was not refused, got {refusal!r}")


def test_layer3_allows_a_fresh_arm_and_an_explicit_append() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        arm = Path(tmp) / "arms" / "A"
        arm.mkdir(parents=True)
        check(run_arm.guard_settled_arm(arm, record=True, append=False) is None,
              "layer 3: an empty arm directory was refused")
        (arm / "off").mkdir()
        (arm / "off" / "badge_access.json").write_text("{}", encoding="utf-8")
        check(run_arm.guard_settled_arm(arm, record=True, append=True) is None,
              "layer 3: --append was refused")
        check(run_arm.guard_settled_arm(arm, record=False, append=False) is None,
              "layer 3: a dry run over a settled arm was refused")


# -- the terminal sentinel --------------------------------------------------

def test_the_sentinel_answers_the_question_mtimes_were_answering() -> None:
    """Arm name, unit count, exit status, UTC timestamp, in one read."""
    with tempfile.TemporaryDirectory() as tmp:
        arm = Path(tmp) / "arms" / "T"
        (arm / "off").mkdir(parents=True)
        (arm / "off" / "badge_access.json").write_text("{}", encoding="utf-8")
        path = run_arm.write_sentinel(arm, "T", run_arm.ARMS["T"], 12,
                                      "complete", 0, "2026-08-23T01:12:00Z")
        state = json.loads(path.read_text(encoding="utf-8"))
        for key in ("arm", "model", "num_ctx", "units_planned", "units_settled",
                    "status", "exit_code", "started_at", "finished_at", "observed"):
            check(key in state, f"sentinel is missing {key}: {sorted(state)}")
        check(state["units_planned"] == 12 and state["units_settled"] == 1,
              f"sentinel counted {state.get('units_settled')} of "
              f"{state.get('units_planned')}, expected 1 of 12")
        check(state["finished_at"].endswith("Z") and "T" in state["finished_at"],
              f"sentinel timestamp {state['finished_at']!r} is not UTC ISO-8601")
        check(state["observed"] is True,
              "a sentinel written by the driver must be marked observed")


# -- the plan ---------------------------------------------------------------

def test_the_plan_is_the_pre_registered_denominators() -> None:
    """The plan's denominators are pre-registered. A moved denominator stops the arm."""
    for label in ("A", "B", "C"):
        units = run_arm.plan_for(label)
        scored = [u for u in units if u[2] == 0]
        check((len(scored), len(units)) == (14, 28),
              f"arm {label} plans {len(scored)} scored of {len(units)}, want 14 of 28")
    units = run_arm.plan_for("T")
    check(len(units) == 12, f"arm T plans {len(units)} units, want 12")
    check(all(p != "rate_limits" for p, _, _ in units),
          "arm T planned `rate_limits`, which A.11 excluded as out of capability")


def test_out_of_repository_is_enforced_by_main() -> None:
    """2.4 MB of model output must not land one `git add -A` from tests/."""
    try:
        run_arm.main(["B", "qwen3:8b", "--num-ctx", "40960",
                      "--out", str(ROOT / "tests")])
    except SystemExit as exc:
        check(isinstance(exc.code, str) and "inside the repository" in exc.code,
              f"--out inside the repo exited with {exc.code!r}")
    else:
        check(False, "--out inside the repository was accepted")


def _populated_arm(root: Path) -> Path:
    """An arm directory with the shape a settled arm has: three subdirectories."""
    arm = root / "arms" / "B"
    for sub, name in (("off", "badge_access"), ("high", "badge_access"),
                      ("var", "badge_access.s1")):
        (arm / sub).mkdir(parents=True, exist_ok=True)
        (arm / sub / f"{name}.json").write_text('{"exit_code": 1}', encoding="utf-8")
        (arm / sub / f"{name}.md").write_text("# merged\n", encoding="utf-8")
    (arm / "journal.jsonl").write_text('{"pair": "badge_access"}\n', encoding="utf-8")
    return arm


def test_a_complete_mirror_verifies() -> None:
    """The control. Without it, `verified: false` proves nothing about the check."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        arm = _populated_arm(tmp / "out")
        dest = tmp / "mirror" / "arms" / "B"
        shutil.copytree(arm, dest)
        got = run_arm.verify_mirror(arm, dest)
        check(got["verified"], f"a byte-identical copy must verify: {got}")
        check(got["source_files"] == got["dest_files"] == 7,
              f"the fixture arm holds 7 files, saw {got}")
        check(got["missing_total"] == 0 and got["differing_total"] == 0, str(got))


def test_a_truncated_mirror_reports_not_verified() -> None:
    """The case mirror.sh actually produces: the copy stops part-way and is quiet.

    A copy process that died early prints nothing further, so its silence reads
    exactly like success. This is the assertion that separates the two.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        arm = _populated_arm(tmp / "out")
        dest = tmp / "mirror" / "arms" / "B"
        shutil.copytree(arm, dest)
        (dest / "var" / "badge_access.s1.json").unlink()
        (dest / "var" / "badge_access.s1.md").unlink()
        got = run_arm.verify_mirror(arm, dest)
        check(not got["verified"], f"a truncated mirror must not verify: {got}")
        check(got["missing_total"] == 2, f"two files were removed, saw {got}")
        check(any("badge_access.s1" in m for m in got["missing"]),
              f"the refusal must name what is missing: {got}")


def test_a_corrupt_mirror_reports_not_verified() -> None:
    """Present and wrong is a different failure from absent, and both must fire."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        arm = _populated_arm(tmp / "out")
        dest = tmp / "mirror" / "arms" / "B"
        shutil.copytree(arm, dest)
        (dest / "off" / "badge_access.json").write_text('{"exit_code": 0}',
                                                        encoding="utf-8")
        got = run_arm.verify_mirror(arm, dest)
        check(not got["verified"], f"a differing file must not verify: {got}")
        check(got["missing_total"] == 0 and got["differing_total"] == 1,
              f"nothing is missing and one file differs, saw {got}")


def test_an_absent_mirror_is_not_a_pass() -> None:
    """A destination that was never written must read as loss, not as nothing to do."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        arm = _populated_arm(tmp / "out")
        got = run_arm.verify_mirror(arm, tmp / "mirror" / "arms" / "B")
        check(not got["verified"], f"an absent mirror must not verify: {got}")
        check(got["dest_files"] == 0 and got["missing_total"] == 7, str(got))


def test_the_sentinel_carries_the_mirror_verdict_separately_from_the_status() -> None:
    """`complete` and `preserved` are two fields, and neither is read off the other."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        arm = _populated_arm(tmp / "out")
        dest = tmp / "mirror" / "arms" / "B"
        shutil.copytree(arm, dest)
        (dest / "high" / "badge_access.md").unlink()
        run_arm.write_sentinel(arm, "B", run_arm.ARMS["B"], 28, "complete", 0,
                               "2026-08-23T00:00:00Z",
                               mirror=run_arm.verify_mirror(arm, dest))
        state = json.loads((arm / "sentinel.json").read_text(encoding="utf-8"))
        check(state["status"] == "complete",
              f"the run did complete and the sentinel must say so: {state['status']}")
        check(state["mirror"]["verified"] is False,
              "a complete run with a truncated mirror must still report the loss")
        check(state["mirror"]["missing_total"] == 1, str(state["mirror"]))


def test_a_sentinel_written_without_a_mirror_records_null_not_true() -> None:
    """No mirror named is a third state. Absence of a check is not a passing check."""
    with tempfile.TemporaryDirectory() as tmp:
        arm = _populated_arm(Path(tmp) / "out")
        run_arm.write_sentinel(arm, "B", run_arm.ARMS["B"], 28, "complete", 0,
                               "2026-08-23T00:00:00Z")
        state = json.loads((arm / "sentinel.json").read_text(encoding="utf-8"))
        check("mirror" in state, "the field must always be present, so it can be read")
        check(state["mirror"] is None,
              f"an unmirrored run records null, not a verdict: {state['mirror']!r}")


def test_a_mirror_inside_the_repository_is_refused() -> None:
    """Same reason as `--out`: the record corpus is not a tracked artefact."""
    try:
        run_arm.main(["B", "qwen3:8b", "--num-ctx", "40960",
                      "--out", "/tmp/llossless-mirror-test-out",
                      "--mirror", str(run_arm.ROOT / "tests")])
    except SystemExit as exc:
        check(isinstance(exc.code, str) and "inside the repository" in exc.code,
              f"--mirror inside the repo exited with {exc.code!r}")
    else:
        check(False, "--mirror inside the repository was accepted")


def test_run_arm_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_run_arm_offline" and callable(function):
            function()
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"run_arm: {checks} checks pass over {len(run_arm.ARMS)} registered arms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
