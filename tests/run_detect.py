#!/usr/bin/env python3
"""Half 1 of the model sweep: does the installed CLI find each fixture's plant?

The instrument is `llossless verify` as an operator runs it -- a subprocess, so
the graded exit status is the number the shell saw rather than one recomputed
from the report. Every other harness in this directory is a library caller and
grades its own return values; none of them can tell you what `echo $?` prints,
and that is the thing an operator acts on.

The document under test is the fixture's own `merged.md`, not a
generated one. That is what makes detection measurable at all: `expected.json`
describes the planted defect in *that* file, so there is an answer key. A merge
this tool generated has no key, and its measurable properties live in
`run_merge.py` instead.

Graded, per fixture, exactly as pre-registered
before any arm ran:

  exit code      the process's real exit status against expected_exit_code.strict
  detected       a probe with a non-`none` expected_finding is detected when some
                 entry in the report's `findings` carries every token of that
                 probe's anchor in the claim text, span or evidence -- or,
                 for a finding no model made, in the merged sentence it is
                 about (`attributions`, which reads the texts alone)
  invented       a finding no such probe accounts for. A finding anchored in a
                 probe another finding already detected is a second report of
                 that defect, recorded in the probe's entry and not invented:
                 a misattribution can be reported by the
                 reverse pass and by `attributions` both, and one defect
                 reported twice is still one defect

An exit 2 or a run that wrote no report is `errored`: the
run did not finish, so it took no reading of the model. It is excluded from
the detection and exit-code denominators, disqualifies nothing, and is listed
by `finish()` to be retried (a failure outside the model's control is not
scored).

Harvested and not graded: extraction counts and the anchored ratio, the
grounding rate, schema repairs, calls, wall time, tier and served window.

Usage:
    python3 tests/run_detect.py --out results.json -- --model qwen3.8:27b \
        --field-order schema
    python3 tests/run_detect.py --out results.json --fixture dedup -- --dry-run
    python3 tests/run_detect.py --regrade RUN_DIR --out REGRADED_DIR

Everything after `--` is passed to `llossless verify` unchanged. That is not
laziness about argument parsing: this script must not own a second opinion about
what the flags mean, because the whole point of running the CLI in a subprocess
is that the arm is configured the way the operator configures it.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import fixture_semantics  # noqa: E402
import socket_guard  # noqa: E402

# This module makes no socket of its own -- the subprocess does. The guard is
# installed anyway, so that the rule `tests/test_socket_guard.py` enforces has
# no exception in this directory, and so that a future refactor that pulls a
# call in-process does not silently acquire an unguarded socket.
socket_guard.install()

FIXTURES_DIR = ROOT / "tests" / "fixtures"
# Run as `python -m llossless`, not the installed `.venv/bin/llossless`:
# a benchmark clone pinned at one commit has no `.venv` of its
# own, and its `.venv/bin/llossless` -- if anyone symlinked or reused one --
# would be an editable install of whatever tree it points at, not this one.
# `python -m` plus `PYTHONPATH` pointed at this tree's own `src/` (`_child_env`,
# below) always runs this checkout's code, and `check_provenance` then proves
# it: a report whose own `claimcheck_commit` disagrees with this tree's HEAD
# means the interpreter found `llossless` somewhere else first.


def fixture_names() -> list[str]:
    """Every fixture on disk. What `--fixture` is checked against."""
    return sorted(p.name for p in FIXTURES_DIR.iterdir()
                  if p.is_dir() and (p / "expected.json").is_file())


# Thirteen fixtures were pre-registered, and every
# published detection figure is over these thirteen. It is a list rather than a
# rule because it is not a property of any fixture: `list_structure` is the
# fourteenth, written to fail under a rendering since replaced, so
# including it in a scored comparison would guarantee the result.
# `held_out` cannot express that -- six of the thirteen are held out too.
#
# A hand-written list is a second place for the set to be wrong, so it is not
# trusted: `test_fixtures.check_preregistered_block` requires it to equal the
# fixture set of every `paper/records/half1-*.json`, which is the block as it
# was actually run, and to name only fixtures that exist.
PREREGISTERED_BLOCK = (
    "attribution_invented", "attribution_swapped", "conflict_surfaced",
    "contradiction", "dedup", "disjoint_domains", "disjoint_sources",
    "dropped_claim", "hallucination", "numeric_drift", "ordering_only",
    "paraphrase", "structure_added",
)


def block_names() -> list[str]:
    """The scored block. `--fixture` still reaches anything on disk."""
    return list(PREREGISTERED_BLOCK)


def load_expected(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name / "expected.json").read_text(encoding="utf-8"))


def planted(expected: dict) -> list[dict]:
    """The probes that name a defect. Empty for a clean fixture, by construction."""
    return [p for p in expected["probes"] if (p.get("expected_finding") or "none") != "none"]


def guard_probes(expected: dict) -> list[dict]:
    """The probes that name no defect: every guard fixture's probe, and the
    control probes on a defect fixture. `expected_verdict` is what they assert;
    a defect fixture's disqualifier already covers false alarms on these, so
    what this adds is the check nothing else made: that the model actually
    reached the declared verdict on the claim, not merely that it filed no
    finding. `plants: 0` on a guard fixture's record is
    `planted()` doing exactly what it says -- this is the list that answers the
    question `planted()` cannot."""
    return [p for p in expected["probes"] if (p.get("expected_finding") or "none") == "none"]


def anchored_in(probe: dict, haystack: str) -> bool:
    tokens = (probe.get("anchor") or {}).get("all_of") or []
    if not tokens:
        return False
    low = haystack.lower()
    return all(t.lower() in low for t in tokens)


def described(finding: dict) -> dict:
    """One finding as a record reads it, whichever family filed it.

    A mechanical finding carries `kind`, `merge_text` and `detail` where a
    verdict carries `finding`, `evidence` and `rationale`. Keyed on
    presence, not truth, so a verdict's empty rationale stays the empty
    string it was in every stored record. The invented list read the verdict
    keys alone at first, and recorded both of `attribution_swapped`'s
    mechanical findings on 2026-09-24 as five `None`s, which is how they were
    first taken for the reverse verdicts.
    """
    return {
        "claim_id": finding.get("claim_id"),
        "finding": finding["finding"] if "finding" in finding else finding.get("kind"),
        "direction": finding.get("direction"),
        "evidence": finding["evidence"] if "evidence" in finding else finding.get("merge_text"),
        "rationale": finding["rationale"] if "rationale" in finding else finding.get("detail"),
    }


def claim_text(report: dict) -> dict[str, str]:
    """claim id -> everything about the claim a finding could be matched on."""
    return {c["id"]: " \n ".join(str(c.get(k) or "") for k in ("text", "span"))
            for c in report.get("claims", [])}


def grade(expected: dict, report: dict, code: int) -> dict:
    """Per probe, not just per fixture. A count says whether a plant was found;
    it cannot say what the model wrote, so a detected/missed integer is not an
    audit record. Every probe below carries its own verdict: the finding that
    matched it, in full, or an explicit statement that none did.

    A miss is checked against `report["verdicts"]`, not just `report["findings"]`,
    before it is called that. `findings` is `verdicts` filtered down to what
    moves the exit code (`report.exit_code`, `Verdict.finding`) -- a probe whose
    `also_acceptable` list includes a label the schema maps to `finding: "none"`
    (numeric_drift's a-max-connections: SUPPORTED is defensible
    and files nothing) is not a probe the model missed. It is one the model
    answered, on a reading the fixture itself sanctions, that this measurement
    was never wired to see. Recording the verdict that was actually there is
    the only way a reader can tell the two apart after the fact.
    """
    texts = claim_text(report)
    # `attributions`: a mechanical finding about one merged
    # sentence, made on `verify` at either depth. Absent from every report
    # written before it existed, so a regrade of those reads what it always
    # read.
    findings = list(report.get("findings", [])) + list(
        report.get("structural", {}).get("findings", [])) + list(
        report.get("attributions", {}).get("findings", []))
    all_verdicts = list(report.get("verdicts", []))

    def haystack_of(item: dict) -> str:
        # `merge_text` is a mechanical finding's span: the merged sentence it
        # is about, which is what a claim's text and span are to a verdict. A
        # verdict carries no such key, so its haystack is what it always was.
        return " \n ".join([
            texts.get(item.get("claim_id", ""), ""),
            str(item.get("evidence") or ""),
            str(item.get("rationale") or ""),
            str(item.get("merge_text") or ""),
        ])

    finding_haystacks = {id(f): haystack_of(f) for f in findings}
    verdict_haystacks = {id(v): haystack_of(v) for v in all_verdicts}

    # `accounted` holds each probe's detecting finding, and is what the guard
    # probes below exclude. `repeated` holds every other finding anchored in a
    # detected probe: a second report of the same defect, which is not
    # invented. It is kept apart on purpose, and the guard loop does not read it:
    # a second report that also lands on a guard probe's own claim is still a
    # false alarm there. Finding the seeded defect licenses reporting it again;
    # it does not license reporting a different one.
    probe_verdicts, accounted, repeated = [], set(), set()
    for probe in planted(expected):
        hits = [f for f in findings if anchored_in(probe, finding_haystacks[id(f)])]
        if hits:
            hit = hits[0]
            accounted.add(id(hit))
            repeated.update(id(f) for f in hits[1:])
            probe_verdicts.append({
                "probe_id": probe["probe_id"],
                "expected_finding": probe.get("expected_finding"),
                "anchor": probe.get("anchor"),
                "verdict": "detected",
                # The detecting finding, the first in report order, as every
                # stored record has it. A mechanical finding is read by its own
                # keys, so a detection says what detected it rather than
                # `None`, which is what the first live run with them wrote.
                **described(hit),
                # Every finding anchored in this probe, the detector first, so
                # a reader sees both families when both reported it.
                "matched_findings": [described(f) for f in hits],
            })
            continue

        # Not a finding. Before calling it missed, look for the verdict itself --
        # it may have been answered and simply filed as `finding: "none"`.
        seen = next((v for v in all_verdicts if anchored_in(probe, verdict_haystacks[id(v)])), None)
        if seen is None:
            probe_verdicts.append({
                "probe_id": probe["probe_id"],
                "expected_finding": probe.get("expected_finding"),
                "anchor": probe.get("anchor"),
                "verdict": "missed",
                "claim_id": None,
                "finding": None,
                "direction": None,
                "evidence": None,
                "rationale": None,
            })
        else:
            also_acceptable = probe.get("also_acceptable") or []
            soft = seen.get("verdict") in also_acceptable
            probe_verdicts.append({
                "probe_id": probe["probe_id"],
                "expected_finding": probe.get("expected_finding"),
                "anchor": probe.get("anchor"),
                "verdict": "acceptable_no_finding" if soft else "missed",
                "claim_id": seen.get("claim_id"),
                "finding": seen.get("finding"),
                "direction": seen.get("direction"),
                "evidence": seen.get("evidence"),
                "rationale": seen.get("rationale"),
                "model_verdict": seen.get("verdict"),
            })

    invented = [described(f) for f in findings
                if id(f) not in accounted and id(f) not in repeated]
    second_reports = [described(f) for f in findings
                      if id(f) in repeated and id(f) not in accounted]

    # `planted()` alone leaves a guard fixture's entire probe
    # list ungraded: expected_finding is "none" on every one of them, by
    # definition, so none ever entered the loop above. That is not a softer
    # check, it is no check -- an arm answering every claim wrong in directions
    # that cancel would file nothing, exit clean, and this record could not
    # tell the difference from an arm that got them right. Every probe in
    # `guard_probes()` is graded here against the verdict the report actually
    # gave the claim, not merely against whether a finding was filed.
    # A probe's anchor is content, not a claim id, and two claims on the same
    # attribute -- a contradiction's winning value and its losing claim's
    # evidence for why it lost, a plain value here against the same value
    # under a swapped attribution there -- can share every anchor token. A
    # search over direction alone still let a guard probe be matched to a
    # different claim's finding whose *rationale* happened to recite the right
    # number while explaining why some other claim was wrong. Both collisions
    # showed up as identical false positives on all three independent arms at
    # once (`attribution_swapped`'s read-timeout probes across direction,
    # `contradiction`'s `b-connect-timeout` within it), which is what a
    # coincidence in the corpus looks like rather than three models agreeing on
    # the same mistake. The anchor is trusted first against the claim's own
    # text -- what the probe actually names -- and only falls back to the
    # fuller evidence/rationale haystack when nothing owns the anchor outright.
    def own_direction(items, haystacks, probe, exclude=frozenset()):
        want = probe.get("direction")
        pool = [x for x in items if id(x) not in exclude and x.get("direction") == want
                and anchored_in(probe, haystacks[id(x)])]
        exact = [x for x in pool if anchored_in(probe, texts.get(x.get("claim_id", ""), ""))]
        return exact or pool

    guard_verdicts = []
    for probe in guard_probes(expected):
        # A finding already claimed by a planted probe (`accounted`) is the
        # planted defect being correctly reported, not a false alarm on this
        # guard probe's own claim -- `contradiction`'s losing claim cites the
        # winning value in its own rationale, which is the disagreement doing
        # its job, not this probe's claim answered wrong.
        alarm = next(iter(own_direction(findings, finding_haystacks, probe, accounted)), None)
        if alarm is not None:
            guard_verdicts.append({
                "probe_id": probe["probe_id"], "expected_verdict": probe.get("expected_verdict"),
                "anchor": probe.get("anchor"), "verdict": "false_alarm",
                "claim_id": alarm.get("claim_id"), "finding": alarm.get("finding"),
                "evidence": alarm.get("evidence"), "rationale": alarm.get("rationale"),
            })
            continue
        seen = next(iter(own_direction(all_verdicts, verdict_haystacks, probe)), None)
        if seen is None:
            guard_verdicts.append({
                "probe_id": probe["probe_id"], "expected_verdict": probe.get("expected_verdict"),
                "anchor": probe.get("anchor"), "verdict": "unclaimed",
                "claim_id": None, "model_verdict": None,
            })
            continue
        also_acceptable = probe.get("also_acceptable") or []
        model_verdict = seen.get("verdict")
        right = model_verdict == probe.get("expected_verdict") or model_verdict in also_acceptable
        guard_verdicts.append({
            "probe_id": probe["probe_id"], "expected_verdict": probe.get("expected_verdict"),
            "anchor": probe.get("anchor"), "verdict": "confirmed" if right else "wrong_verdict",
            "claim_id": seen.get("claim_id"), "model_verdict": model_verdict,
            "evidence": seen.get("evidence"), "rationale": seen.get("rationale"),
        })

    declared = expected["expected_exit_code"]
    wanted = declared["strict"]
    # Three outcomes, not two. `matched` and `missed` between them assert that
    # the fixture took a reading; a fixture that sanctions two readings which
    # exit differently did not, and calling that a miss scores correct behaviour
    # as a failure. `fixture_semantics.outcome` is the one definition of when
    # the third applies, and it is deliberately narrow -- see its docstring.
    result = fixture_semantics.outcome(declared, code, len(invented), probe_verdicts,
                                       reported=bool(report))
    return {
        "expected_exit_code": wanted,
        "expected_exit_code_lenient": declared["lenient"],
        "exit_code": code,
        "exit_code_matches": code == wanted,
        "outcome": result,
        "plants": len(planted(expected)),
        "probes": probe_verdicts,
        "detected": [p["probe_id"] for p in probe_verdicts if p["verdict"] == "detected"],
        # `acceptable_no_finding` still counts as missed for the detection rate:
        # the defect was not flagged, whatever reading justified that. It is kept
        # out of `missed`'s plain reading only in `probes`, where the distinction
        # from a true miss is recorded.
        "missed": [p["probe_id"] for p in probe_verdicts
                   if p["verdict"] in ("missed", "acceptable_no_finding")],
        "invented_findings": invented,
        # Findings anchored in a probe another finding detected: the same
        # defect reported again, by the other family or the same one.
        "second_reports": second_reports,
        "findings_total": len(findings),
        "guard_probes": guard_verdicts,
        "guard_confirmed": [p["probe_id"] for p in guard_verdicts if p["verdict"] == "confirmed"],
        "guard_wrong": [p["probe_id"] for p in guard_verdicts
                        if p["verdict"] in ("wrong_verdict", "false_alarm")],
        "guard_unclaimed": [p["probe_id"] for p in guard_verdicts if p["verdict"] == "unclaimed"],
    }


def harvest(report: dict) -> dict:
    """The descriptive figures, read off the report rather than recomputed."""
    claims = report.get("claims", [])
    coverage = report.get("coverage", {})
    provenance = report.get("provenance") or {}
    counts = provenance.get("counts", {})
    graded = coverage.get("graded", 0)
    return {
        "extracted": coverage.get("extracted", {}),
        "claims_total": len(claims),
        # Reported as a count beside its denominator, never as a bare ratio: an
        # anchored ratio of 1.0 over 3 claims and over 300 is the same float and
        # not the same measurement.
        "anchored": sum(1 for c in claims if c.get("anchored")),
        "graded": graded,
        "grounded": coverage.get("grounded", 0),
        "forward_verdicts": coverage.get("forward_verdicts", 0),
        "reverse_verdicts": coverage.get("reverse_verdicts", 0),
        "errored": coverage.get("errored", 0),
        "calls": counts.get("calls"),
        "schema_repairs": counts.get("schema_repairs"),
        "completion_tokens": counts.get("completion_tokens"),
        "model_loads": counts.get("model_loads"),
        "duration_seconds": provenance.get("duration_seconds"),
        "models": provenance.get("models"),
        "structured_output": provenance.get("structured_output"),
        "decoding": provenance.get("decoding"),
        "endpoint": provenance.get("endpoint"),
    }


def _child_env() -> dict[str, str]:
    """This tree's own `src/` first on `PYTHONPATH`, ahead of anything already set.

    A prepend, not a replace: a caller with its own `PYTHONPATH` (there is none
    in this suite today, but a future one is not owed a silent override) keeps
    it, just not first.
    """
    env = dict(os.environ)
    src = str(ROOT / "src")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src if not existing else f"{src}{os.pathsep}{existing}"
    return env


def tree_commit() -> str:
    """This tree's own HEAD, 12 hex characters -- `provenance.git_commit`'s own format."""
    done = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True, timeout=10)
    if done.returncode != 0:
        raise SystemExit(f"run_detect: git rev-parse HEAD failed in {ROOT}: "
                         f"{done.stderr.strip()}")
    return done.stdout.strip()[:12]


def check_provenance(name: str, report: dict) -> None:
    """Refuse a report that was not produced by this tree's own code.

    `_child_env` points the child's `PYTHONPATH` at this tree's `src/`, but an
    editable install a `.pth` file put on `sys.path` ahead of it, or a stray
    `llossless` package installed some other way, would shadow it silently --
    the failure this whole file exists to catch had exactly that shape. The
    report's own `provenance.claimcheck_commit` is what the run was actually
    produced by, so every report is checked against this tree's HEAD before
    anything in it is trusted. A `-dirty`/`-unknown` suffix, if the field ever
    carries one, is stripped before comparing: what is pinned here is the
    commit, not whether this tree happened to be clean when it ran.
    """
    got = str((report.get("provenance") or {}).get("claimcheck_commit") or "").split("-")[0]
    want = tree_commit()
    if got != want:
        raise SystemExit(
            f"run_detect: {name}'s report was produced by commit {got!r}, not this "
            f"tree's HEAD {want!r} -- `llossless` did not resolve to this tree's "
            f"src/ (a stale .venv install, or another copy earlier on sys.path). "
            f"Refusing to score a report of unknown provenance.")


def run_one(name: str, passthrough: list[str], reports_dir: Path | None) -> dict:
    directory = FIXTURES_DIR / name
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "report.json"
        command = [
            sys.executable, "-m", "llossless", "verify",
            str(directory / "source_a.md"), str(directory / "source_b.md"),
            str(directory / "merged.md"),
            "--no-cache", "--json", str(out),
        ] + passthrough
        started = time.monotonic()
        completed = subprocess.run(command, capture_output=True, text=True,
                                   env=_child_env())
        seconds = time.monotonic() - started
        report = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else {}
        if report:
            check_provenance(name, report)

        # The full report is otherwise thrown away with `tmp` -- graded down
        # to a handful of summary fields with nothing left to check them
        # against. Copied out before the directory closes, so "what did the
        # model actually say" has an answer after this process exits.
        report_ref = None
        if reports_dir is not None and report:
            reports_dir.mkdir(parents=True, exist_ok=True)
            report_ref = reports_dir / f"{name}.json"
            report_ref.write_text(json.dumps(report, indent=2), encoding="utf-8")

    return record_of(name, report, completed.returncode,
                     wall_seconds=round(seconds, 1),
                     report_ref=str(report_ref) if report_ref else None,
                     stderr_tail=completed.stderr.strip().splitlines()[-3:])


def record_of(name: str, report: dict, code: int, *, wall_seconds: float | None,
              report_ref: str | None, stderr_tail: list[str]) -> dict:
    """One fixture's record, graded. Shared by a run and by `--regrade`, so a
    regraded record is built by the same code as the one it stands beside."""
    expected = load_expected(name)
    record = {
        "fixture": name,
        "kind": expected["kind"],
        "wall_seconds": wall_seconds,
        "report_written": bool(report),
        "report_ref": report_ref,
        "stderr_tail": stderr_tail,
    }
    record.update(grade(expected, report, code))
    record["harvest"] = harvest(report)
    return record


def disqualified(records: list[dict]) -> list[str]:
    """The pre-registered disqualifier. Computed, never eyeballed.

    Both clauses now read the outcome first. Neither could before, and both
    were structurally blind to the one case they most needed to see:

    * Clause 1 asked `kind == "defect"`, a field the probes cannot contradict,
      and rejected exit 0 without consulting them. `numeric_drift` sanctions a
      reading that exits 0, so an arm taking it was disqualified for behaving
      correctly. It now reads the strict code the probes imply -- equivalent to
      `kind` on every fixture, because `test_fixtures.py` requires the two to
      agree, but derived rather than declared -- and it does not fire on a
      fixture that did not take a reading.
    * Clause 2 fired only where a fixture declares exit 0, and
      `conflict_surfaced` declared 1 while planting nothing, so the one invented
      finding the study could then see reached the exit code the study wanted
      and was scored as a match. The fixture is repaired.
      Repairing it closed the instance and left the class open: the clause
      still could not fire on any fixture expecting exit 1, so an arm could
      invent freely on the six fixtures that plant a defect and be scored as
      matching them. It now reads `invented_findings` on every measured fixture, whatever
      exit code the fixture expects. Finding the seeded defect
      does not license reporting a different one beside it. Reporting the same
      one twice is not a different one: a finding anchored in a probe
      another finding detected is a second report, not an invention.
    * Clause 3 is new, not repaired: before `guard_probes()`
      existed, a guard fixture's own answer key was never read by anything, so
      there was nothing here for it to be blind to. An arm can only be
      disqualified on a claim its own record shows it graded; `unclaimed`
      (the model never reached a verdict on the claim at all) is left alone,
      same as `UNMEASURED` above it, because there was no reading to reject.

    An unmeasured fixture disqualifies nothing. That is the point of the state:
    no reading was taken, so there is nothing to reject the arm on. An errored
    one (exit 2, or no report) disqualifies nothing either, for the same
    reason: the run never finished.
    """
    out = []
    for r in records:
        if r.get("outcome") in (fixture_semantics.UNMEASURED, fixture_semantics.ERRORED):
            continue
        if r["expected_exit_code"] == 1 and r["exit_code"] == 0:
            out.append(f"{r['fixture']}: a seeded defect exited clean")
        if r["invented_findings"]:
            count = len(r["invented_findings"])
            out.append(
                f"{r['fixture']}: a clean fixture failed with "
                f"{count} invented finding(s)"
                if r["expected_exit_code"] == 0 else
                f"{r['fixture']}: {count} invented finding(s) beside the "
                f"seeded defect")
        if r.get("guard_wrong"):
            out.append(f"{r['fixture']}: {len(r['guard_wrong'])} guard probe(s) "
                       f"graded wrong against their own answer key -- "
                       f"{', '.join(r['guard_wrong'])}")
    return out


def line_of(record: dict) -> str:
    """The one line a fixture prints, during a run and during a regrade."""
    mark = {fixture_semantics.MATCHED: "ok  ",
            fixture_semantics.UNMEASURED: "UNM ",
            fixture_semantics.MISSED: "MISS",
            fixture_semantics.ERRORED: "ERR "}[record["outcome"]]
    return (f"  {mark} {record['fixture']:<22} exit {record['exit_code']} "
            f"(want {record['expected_exit_code']})  "
            f"detected {len(record['detected'])}/{record['plants']}  "
            f"invented {len(record['invented_findings'])}  "
            f"guard {len(record['guard_confirmed'])}/{len(record['guard_probes'])}"
            f" ({len(record['guard_wrong'])} wrong)  "
            f"{record['wall_seconds']}s")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--fixture", action="append", metavar="NAME",
                        help="grade only this fixture; repeatable (default: all)")
    parser.add_argument("--out", type=Path, required=True,
                        help="write the graded results here; with --regrade, "
                             "a directory that gets one <arm>.json per arm")
    parser.add_argument("--label", default="",
                        help="arm label, copied into the results unchanged")
    parser.add_argument("--regrade", type=Path, metavar="DIR",
                        help="grade the reports a run already saved, "
                             "<DIR>/<arm>-reports/*.json, and call nothing")
    parser.add_argument("passthrough", nargs="*", metavar="-- FLAGS",
                        help="flags handed to `llossless verify` unchanged")
    args = parser.parse_args(argv)

    if args.regrade is not None:
        if args.fixture or args.passthrough or args.label:
            print("--regrade grades what was saved; --fixture, --label and "
                  "verify flags do not apply", file=sys.stderr)
            return 2
        return regrade(args.regrade, args.out)

    if not (ROOT / "src" / "llossless" / "__main__.py").is_file():
        print(f"no llossless package at {ROOT / 'src' / 'llossless'}", file=sys.stderr)
        return 2

    names = args.fixture or block_names()
    unknown = [n for n in names if n not in fixture_names()]
    if unknown:
        print(f"no such fixture: {', '.join(unknown)}", file=sys.stderr)
        return 2

    reports_dir = args.out.parent / f"{args.out.stem}-reports"
    records = []
    for name in names:
        record = run_one(name, list(args.passthrough), reports_dir)
        records.append(record)
        print(line_of(record), flush=True)

    return finish(records, args.label, list(args.passthrough), args.out)


def regrade(directory: Path, out: Path) -> int:
    """Grade the reports a run saved, with this file's `grade`, and call nothing.

    Reads `<directory>/<arm>-reports/*.json`, which is where a run copies each
    report (`run_one`), and writes `<out>/<arm>.json` in the run's own format.
    The exit status graded is the one the run recorded in `<directory>/<arm>`,
    the process's real status; only where that record is missing does it fall
    back to the report's own `exit_code`, and each record says which it used.
    Nothing is written under `directory`: the saved run is the evidence a
    regrade stands beside, never something it replaces.
    """
    directory, out = directory.resolve(), out.resolve()
    arms = sorted(p for p in directory.glob("*-reports") if p.is_dir())
    if not arms:
        print(f"no <arm>-reports directory in {directory}", file=sys.stderr)
        return 2
    if out == directory or directory in out.parents:
        print(f"--out {out} is inside {directory}; a regrade does not write "
              "beside the run it regrades", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    worst = 0
    for reports in arms:
        arm = reports.name[:-len("-reports")]
        stored_path = directory / arm
        stored = (json.loads(stored_path.read_text(encoding="utf-8"))
                  if stored_path.is_file() else None)
        kept = {r["fixture"]: r for r in (stored or {}).get("records", [])}
        paths = {p.stem: p for p in reports.glob("*.json")}
        order = [n for n in kept if n in paths] + sorted(set(paths) - set(kept))
        print(f"\n=== {arm}: regraded from {reports}")
        records = []
        for name in order:
            report = json.loads(paths[name].read_text(encoding="utf-8"))
            old = kept.get(name)
            code = old["exit_code"] if old else report.get("exit_code")
            record = record_of(
                name, report, code,
                wall_seconds=old.get("wall_seconds") if old else None,
                report_ref=str(paths[name]),
                stderr_tail=old.get("stderr_tail", []) if old else [])
            record["exit_code_from"] = "run record" if old else "report"
            records.append(record)
            print(line_of(record), flush=True)
        summary = (stored or {}).get("summary", {})
        label = f"{summary.get('label') or arm} (regraded)"
        code = finish(records, label, summary.get("passthrough", []), out / f"{arm}.json",
                      extra={"regraded_from": str(reports),
                             "as_run": {k: summary.get(k) for k in (
                                 "plants_detected", "invented_total",
                                 "guard_wrong_total", "disqualified")}
                             if stored else None})
        if stored:
            print("\n  as run, from the saved record:")
            print(f"    plants detected {summary.get('plants_detected')}, "
                  f"invented {summary.get('invented_total')}, "
                  f"guard wrong {summary.get('guard_wrong_total')}")
            for line in summary.get("disqualified") or ["not disqualified"]:
                print(f"    - {line}")
        worst = max(worst, code)
    return worst


def finish(records: list[dict], label: str, passthrough: list[str], out: Path,
           extra: dict | None = None) -> int:
    """Summarise, write and print one arm. The rule and the format are one
    definition for a run and for a regrade."""
    stop = disqualified(records)
    by = {name: [r for r in records if r["outcome"] == name]
          for name in fixture_semantics.OUTCOMES}
    matched = by[fixture_semantics.MATCHED]
    unmeasured = by[fixture_semantics.UNMEASURED]
    errored = by[fixture_semantics.ERRORED]
    # An errored fixture took no reading of anything: not of the plants, not of
    # the guards, not of what it invented. It is named and left out of every
    # figure below except `plants_total`, the corpus count.
    scored = [r for r in records if r["outcome"] != fixture_semantics.ERRORED]
    measured = [r for r in scored if r["outcome"] != fixture_semantics.UNMEASURED]
    summary = {
        "label": label,
        "passthrough": list(passthrough),
        "fixtures": len(records),
        "exit_code_matched": sorted(r["fixture"] for r in matched),
        # A fixture that could not take a reading on this arm. Listed, not
        # folded into either column: a blank cell beside a pass reads as a pass.
        "exit_code_unmeasured": sorted(r["fixture"] for r in unmeasured),
        "exit_code_missed": sorted(r["fixture"] for r in by[fixture_semantics.MISSED]),
        # A run that did not finish: exit 2 or no report. Not the model's
        # result; retried, never scored.
        "exit_code_errored": sorted(r["fixture"] for r in errored),
        "fixtures_measured": len(measured),
        # `plants_total` stays the corpus figure so it is comparable across
        # arms; what varies per arm is how many of them the arm was measured on.
        "plants_total": sum(r["plants"] for r in records),
        "plants_unmeasured": sum(r["plants"] for r in unmeasured),
        "plants_errored": sum(r["plants"] for r in errored),
        "plants_detected": sum(len(r["detected"]) for r in measured),
        "invented_total": sum(len(r["invented_findings"]) for r in scored),
        "second_reports_total": sum(len(r.get("second_reports", [])) for r in scored),
        "invented_on_unmeasured": sum(len(r["invented_findings"]) for r in unmeasured),
        "guard_probes_total": sum(len(r["guard_probes"]) for r in scored),
        "guard_confirmed_total": sum(len(r["guard_confirmed"]) for r in scored),
        "guard_wrong_total": sum(len(r["guard_wrong"]) for r in scored),
        "guard_unclaimed_total": sum(len(r["guard_unclaimed"]) for r in scored),
        "disqualified": stop,
        **(extra or {}),
    }
    out.write_text(json.dumps({"summary": summary, "records": records},
                              indent=2) + "\n", encoding="utf-8")
    print(f"\n  exit codes matched {len(matched)}/{summary['fixtures_measured']} measured"
          f" of {len(records)}, "
          f"plants detected {summary['plants_detected']}/"
          f"{summary['plants_total'] - summary['plants_unmeasured'] - summary['plants_errored']}"
          f" measured of {summary['plants_total']}, "
          f"invented findings {summary['invented_total']}"
          + (f", second reports {summary['second_reports_total']}"
             if summary["second_reports_total"] else ""))
    if unmeasured:
        print("\n  UNMEASURED -- the fixture sanctions two readings that exit"
              " differently, and\n  this arm took the second. Not a pass and not"
              " a failure:")
        for r in unmeasured:
            print(f"    - {r['fixture']}: exit {r['exit_code']}, strict"
                  f" {r['expected_exit_code']}, lenient"
                  f" {r['expected_exit_code_lenient']}")
    if errored:
        print("\n  ERRORED -- the run did not finish (exit 2, or no report). Not"
              " scored, not in any\n  denominator above; retry these:")
        for r in errored:
            tail = " | ".join(r.get("stderr_tail") or []) or "no stderr kept"
            print(f"    - {r['fixture']}: exit {r['exit_code']}, report "
                  f"{'written' if r['report_written'] else 'not written'}: {tail[:200]}")
    if stop:
        print("\n  DISQUALIFIED, on the pre-registered rule:")
        for line in stop:
            print(f"    - {line}")
    print(f"  -> {out}")
    # 1 is "measured, and something failed"; 0 is "measured, nothing failed";
    # 2 is "nothing failed, but not everything was measured: retry the errored
    # fixtures". None is a verdict on the arm: the
    # pre-registered disqualifier is.
    if stop or summary["exit_code_missed"]:
        return 1
    return 2 if errored else 0


if __name__ == "__main__":
    sys.exit(main())
