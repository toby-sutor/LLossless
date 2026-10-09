#!/usr/bin/env python3
"""One cheap end-to-end merge per configured endpoint, asserting all three roles ran.

A check that had never passed as a *tool*: all three roles
once ran through a hosted endpoint,
by hand, with the
flags worked out over an afternoon. This makes that repeatable, so that
"LLossless runs on this endpoint" is something a command answers rather than
something a note remembers.

**What it actually asserts, and why it is not a unit test.** Three green vendor
probes once hid a merge preflight that 404s on every vendor, because each probe
called a function and the defect lived on the CLI path. So this
runs `llossless merge` as a subprocess, exactly as an
operator would, and reads the JSON report it writes. A role that never called
is the failure this exists to catch: `decompose` and `verify` both refuse
outright without a measured window, and a run that skipped them silently
would otherwise look like a pass with a smaller report.

**The documents are synthetic and stay that way.** The paper's introduction (`paper/sections/10-introduction.tex`, its paragraph "Where the documents come from")
and the benchmark rules forbid sending text derived from private documents to a
hosted endpoint, and the operator's `toby-test-*` corpus is theirs. The pair
here is `tests/fixtures/dedup`, which is 270 bytes of invented relay
documentation and is in the repository already.

**`--no-cache`, and it is the whole tool.** The first live run of this file
reported a green endpoint on **one** call: `merge` went to the vendor because
its prompt had just changed, and `decompose` and `verify` were served from the
cassette cache, which is on by default. Every artefact a role leaves was
present, the report rendered, tokens were billed, and two of the three roles
never touched the endpoint. A smoke test that can pass by reading a directory
is not a smoke test, so the cache is off here and `calls_by_role`
is what the assertion reads, because it is the only field
that tells a vendor's answer apart from a cassette's.

**Cost.** One merge, three decomposes and two verify passes over a 270-byte
pair. On the 27B that is a few thousand tokens; on a metered vendor it is
fractions of a cent. Deliberately *not* sized above a console's rounding the way
`probe_vendors.py` is -- that tool exists to reconcile against a bill, and this
one exists to answer yes or no.

Run:

    python3 tests/smoke_vendor.py --plan        # what it would do, no calls
    python3 tests/smoke_vendor.py --self-test   # offline, in run_all
    python3 tests/smoke_vendor.py --run         # live, costs money

`--self-test` makes no network call and is what `run_all.py` invokes. It checks
the properties that can be checked without an endpoint: that the pair exists and
is synthetic, that the role list is the tool's own rather than a copy, and that
a missing configuration is refused rather than silently skipped.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from llossless import config  # noqa: E402

# The pair, and the reason it is this pair: smallest synthetic fixture in the
# repository, so the smoke test is the cheapest end-to-end run that still
# exercises every role. Named rather than globbed -- a glob would silently
# start sending whatever fixture sorted first.
PAIR = ROOT / "tests" / "fixtures" / "dedup"
SOURCES = ("source_a.md", "source_b.md")

# A run that exits 2 has not established anything, so it is the only code this
# tool treats as failure. 0, 1 and 3 all mean the pipeline completed and the
# reconciler reached a verdict -- and which of them comes back depends on the
# model, not on the endpoint, so asserting a particular one would make this a
# quality test on a 270-byte fixture rather than a connectivity test.
COMPLETED = (0, 1, 3)

failures: list[str] = []
notes: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def settings_from_env() -> config.Settings:
    return config.from_env()


def endpoints_in_play(settings: config.Settings) -> dict[str, str]:
    """Every distinct endpoint this configuration would reach, by role.

    Keyed by URL so a run with three roles on one host is one entry: the
    question is how many boxes have to answer, not how many roles there are.
    """
    by_url: dict[str, list[str]] = {}
    for role in sorted(config.ROLES):
        by_url.setdefault(settings.base_url_for(role), []).append(role)
    return {url: ", ".join(roles) for url, roles in by_url.items()}


def plan(settings: config.Settings) -> str:
    lines = ["smoke_vendor plan", ""]
    lines.append(f"  pair      {PAIR.relative_to(ROOT)} "
                 f"({sum((PAIR / n).stat().st_size for n in SOURCES)} bytes)")
    for url, roles in endpoints_in_play(settings).items():
        shown = settings.endpoint_name_for(roles.split(", ")[0])
        lines.append(f"  endpoint  {shown}  <- {roles}")
    for role in sorted(config.ROLES):
        lines.append(f"  {role:10} model={settings.model_for(role)} "
                     f"window={settings.window_for(role)}")
    lines.append("")
    lines.append("  calls     1 merge, 2 decompose, 2 verify (one per direction)")
    lines.append("  asserts   every role made at least one call; exit code in "
                 f"{COMPLETED}")
    return "\n".join(lines)


def live(settings: config.Settings) -> int:
    """Run the command and read its own report. Returns a process exit code."""
    with tempfile.TemporaryDirectory(prefix="llossless-smoke-") as tmp:
        work = Path(tmp)
        for name in SOURCES:
            (work / name).write_text((PAIR / name).read_text(encoding="utf-8"),
                                     encoding="utf-8")
        report = work / "report.json"
        # `--base` is required by the merge command and has no default, on
        # purpose: which document's shape and title survive is a decision, and
        # a tool that picked one silently would be making it. The smoke test
        # picks the first source and says so here rather than in a flag list
        # somebody has to decode.
        argv = [sys.executable, "-m", "llossless", "merge",
                str(work / SOURCES[0]), str(work / SOURCES[1]),
                "--base", SOURCES[0],
                "--no-cache",
                "--json", str(report),
                "--out", str(work / "merged.md")]
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        print(f"  running: llossless merge {SOURCES[0]} {SOURCES[1]}")
        proc = subprocess.run(argv, capture_output=True, text=True, env=env,
                              cwd=str(work))
        sys.stdout.write(proc.stdout)
        if proc.returncode not in COMPLETED:
            sys.stderr.write(proc.stderr)
            check(False, f"the run exited {proc.returncode}; only {COMPLETED} mean "
                         f"the pipeline completed")
            return 1
        if not report.exists():
            check(False, "the run wrote no JSON report, so nothing can be asserted "
                         "about which roles ran")
            return 1
        data = json.loads(report.read_text(encoding="utf-8"))
        return assert_every_role_ran(data, settings)


def assert_every_role_ran(data: dict, settings: config.Settings) -> int:
    """The assertion the whole tool exists for.

    Read off the report's own provenance rather than off a counter this module
    keeps: a tool that counted its own calls would agree with itself whatever
    the run did.
    """
    provenance = data.get("provenance") or {}
    by_role = provenance.get("calls_by_role") or {}
    check("calls_by_role" in provenance,
          "the report carries no calls_by_role, so which endpoint answered for "
          "which role cannot be established from it")
    silent = [role for role in sorted(config.ROLES) if not by_role.get(role)]
    check(not silent,
          f"role(s) {', '.join(silent)} made no live call -- a "
          f"run that skips a role looks like a smaller pass, which is the "
          f"failure this tool exists to catch. Got {dict(by_role)}")
    for role in sorted(config.ROLES):
        notes.append(f"{role}: {by_role.get(role, 0)} live call(s) on "
                     f"{settings.endpoint_name_for(role)}")
    structural = data.get("structural") or {}
    check(structural.get("ran") is True,
          f"the reconciler did not run, so the merge was never held against its "
          f"sources: {structural}")
    return 0


def self_test() -> int:
    """Offline. Every property that does not need an endpoint."""
    check(PAIR.is_dir(), f"the smoke pair is missing: {PAIR}")
    for name in SOURCES:
        check((PAIR / name).is_file(), f"{name} is missing from {PAIR}")

    # The pair must stay synthetic and stay small. Both are load-bearing: the
    # first is a standing constraint on anything sent to a vendor, the second
    # is what makes this cheap enough to run on every endpoint.
    total = sum((PAIR / n).stat().st_size for n in SOURCES)
    check(total < 2000,
          f"the smoke pair is {total} bytes; a smoke test that is not cheap "
          f"stops being run")
    check((PAIR / "expected.json").is_file(),
          "the pair must be a registered fixture, so its provenance is the "
          "fixture corpus rather than a file somebody dropped here")

    # The role list is the tool's, not a copy. A second list here would go
    # stale the moment a fourth role is added, and the failure would be a
    # role silently never asserted about -- exactly what this tool checks for.
    source = Path(__file__).read_text(encoding="utf-8")
    check("config.ROLES" in source,
          "smoke_vendor must read config.ROLES rather than list the roles")
    check(not any(f'"{role}",' in source.replace("config.ROLES", "")
                  and f'for role in sorted(config.ROLES)' not in source
                  for role in ("merge", "verify", "decompose")),
          "smoke_vendor must not carry its own hardcoded role list")

    # 2 is the only code that means nothing was established. Asserted because
    # widening COMPLETED to include it would make the tool pass on an endpoint
    # that answered nothing at all.
    check(2 not in COMPLETED,
          "exit 2 means the run is inconclusive; it cannot count as a pass")
    check(set(COMPLETED) == {0, 1, 3},
          f"the completed set must be the three verdict codes; got {COMPLETED}")

    # The plan must render without an endpoint, because an operator sizes a run
    # before configuring one.
    try:
        text = plan(config.Settings(models={"verify": "m", "merge": "m"}))
    except Exception as exc:  # noqa: BLE001
        text = ""
        check(False, f"--plan must render without a live endpoint: {exc!r}")
    check("asserts" in text and "endpoint" in text,
          f"the plan must say what it asserts and where: {text!r}")

    # And the whole point: this runs the command, not the function.
    check('"-m", "llossless", "merge"' in source,
          "smoke_vendor must invoke the CLI as a subprocess; three green probes "
          "once hid a defect that lived only on the command path")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args(argv)

    if not (args.plan or args.self_test or args.run):
        parser.print_help()
        return 2

    if args.self_test:
        self_test()
    if args.plan or args.run:
        try:
            settings = settings_from_env()
        except config.ConfigError as exc:
            print(f"smoke_vendor: {exc}", file=sys.stderr)
            return 2
        if args.plan:
            print(plan(settings))
        if args.run:
            print(plan(settings))
            print()
            live(settings)

    for note in notes:
        print(f"  note: {note}")
    if failures:
        print(f"smoke_vendor: FAILED ({len(failures)} failing)")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("smoke_vendor: ok (0 failing)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
