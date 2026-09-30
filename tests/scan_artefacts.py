#!/usr/bin/env python3
"""Refuse an artefact that carries a credential. The backstop, not the control.

The control is that the key is never put anywhere: it is read at send time from
the variable `LLOSSLESS_API_KEY_ENV` names, it is not a field on `Settings`,
and `transport` builds the `Authorization` header at the socket and stores
nothing. This program exists because a control nobody checks is a belief, and
because the failure it guards against is silent - a key in a report is readable
by everyone who reads the report, and nothing about the report looks wrong.

Different scan from `acceptance_7_no_secrets_committed` in `test_client.py`,
and both are needed. That one reads `git ls-files` and is a commit gate: it
catches a key pasted into a document. This one reads a *directory of output* -
cassettes, Markdown reports, HTML reports, JSON exports, log files, captured
stderr - because the artefacts a run produces are mostly untracked, are the
things that get attached to a message or copied to a mirror, and are invisible
to a scan over tracked files.

Two kinds of finding, and the first is the one that matters:

  literal    a value that is actually in this machine's environment right now,
             or in `.env`. No pattern involved and no false-negative shape: if
             the string is there, it is there. This is what catches a vendor
             whose key format nobody anticipated.
  shaped     the published key prefixes - OpenAI `sk-`, Anthropic `sk-ant-`,
             Google `AIza` - and a literal `Authorization` header. This is what
             catches a key that belongs to somebody else, or to a run made on
             another machine, which the literal scan cannot see.

**No finding ever prints the secret.** It names the file, the byte offset and
which rule fired. A scanner that echoes what it found turns every log of a
scan into a second copy of the leak.

Usage:
    python3 tests/scan_artefacts.py DIR [DIR ...]
    python3 tests/scan_artefacts.py --self-test
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Which environment variables might be holding a credential. Deliberately wider
# than the one variable this tool reads: the point is to catch a key that
# reached an artefact by any route, including a vendor SDK's own variable that
# something else on this machine set.
SECRET_NAMES = re.compile(r"(API_?KEY|_KEY$|^KEY$|TOKEN|SECRET|PASSWORD|CREDENTIAL)",
                          re.IGNORECASE)

# Short values are skipped. A four-character secret would be unsearchable
# anyway -- every file contains every four-character string eventually -- and a
# variable set to `1` or `true` would flag the whole tree. Real keys from all
# three vendors are far longer than this.
MIN_SECRET = 12

# Published prefixes, not guesses. `sk-ant-` is listed before `sk-` so an
# Anthropic key is named as one; the scan reports every rule that fires, so the
# order is for legibility rather than correctness.
# `(?<![A-Za-z0-9])` rather than `\b`, and it is not a nicety: `\bsk-` does not
# fire inside `ask-before-...`, because `a` and `s` are both word characters, so
# there is no boundary there -- but it does not *help* either, and the first
# real run of this scan flagged a memory filename for exactly that reason. A
# lookbehind for an alphanumeric is what actually excludes a prefix glued to
# the end of a word. Both near misses are canaries below.
BOUNDARY = r"(?<![A-Za-z0-9])"

SHAPES = {
    "an Anthropic key prefix": re.compile(BOUNDARY + r"sk-ant-[A-Za-z0-9_-]{8,}"),
    "an OpenAI key prefix": re.compile(BOUNDARY + r"sk-(?!ant-)[A-Za-z0-9_-]{16,}"),
    "a Google key prefix": re.compile(BOUNDARY + r"AIza[A-Za-z0-9_-]{20,}"),
    # `[^$\s]` on the first character of the token: `Bearer $OPENAI_API_KEY` is
    # a shell expansion recorded in a transcript, and the thing after the
    # dollar is the *name* of the variable. The value is what leaks; the name
    # is documentation. This too came from the first real run.
    "an Authorization header": re.compile(
        r"[Aa]uthorization\"?\s*[:=]\s*\"?\s*Bearer\s+[^$\s]\S{8,}"),
    "a bearer token": re.compile(r"Bearer\s+(?!\$)[A-Za-z0-9._-]{16,}"),
}

# Files that hold the canaries by construction, plus the environment file the
# needles are read *from*. Nothing else belongs here: when this scan trips on
# an artefact the fix is at the pattern or at the code that wrote the artefact,
# never at this set. `.env` is not an artefact this tool writes -- it is the
# input, and it is gitignored.
EXEMPT_NAMES = {".env", "tests/scan_artefacts.py", "tests/test_client.py"}
EXEMPT_PARTS = {".git", "__pycache__", ".llossless-cache"}

# Artefact kinds. Anything else in the directory is read too -- a `.log` and a
# `.txt` and a stderr capture with no extension are all the same problem -- so
# this list is only used to report what the scan covered, never to skip a file.
BINARY = {".png", ".jpg", ".jpeg", ".ico", ".pdf", ".gz", ".zip"}


def environment_secrets(environ: dict[str, str] | None = None,
                        dotenv: Path | None = None) -> dict[str, str]:
    """Value -> the variable it came from, for every plausible credential here.

    `.env` is read as well as the live environment because a run made from a
    shell that sourced it has the value in memory and this process may not.
    The file is never written to, never echoed, and the value is used only as a
    needle.
    """
    found: dict[str, str] = {}
    for name, value in (environ if environ is not None else os.environ).items():
        if SECRET_NAMES.search(name) and value and len(value) >= MIN_SECRET:
            found[value] = name
    path = ROOT / ".env" if dotenv is None else dotenv
    if path.is_file():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip().removeprefix("export ").strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, _, value = line.partition("=")
            name, value = name.strip(), value.strip().strip("'\"")
            if SECRET_NAMES.search(name) and len(value) >= MIN_SECRET:
                found[value] = f"{name} (.env)"
    return found


def scan_text(name: str, text: str, secrets: dict[str, str]) -> list[str]:
    """Findings for one file. Never includes the matched string."""
    findings = []
    for value, variable in secrets.items():
        at = text.find(value)
        if at >= 0:
            findings.append(f"{name}: byte {at}: the literal value of ${variable}")
    for label, pattern in SHAPES.items():
        match = pattern.search(text)
        if match:
            findings.append(f"{name}: byte {match.start()}: {label}")
    return findings


def scan_paths(paths: list[Path], secrets: dict[str, str]) -> tuple[list[str], int]:
    findings: list[str] = []
    scanned = 0
    for root in paths:
        files = sorted(root.rglob("*")) if root.is_dir() else [root]
        for path in files:
            if not path.is_file() or path.suffix.lower() in BINARY:
                continue
            if EXEMPT_PARTS & set(path.parts):
                continue
            try:
                shown = str(path.relative_to(ROOT))
            except ValueError:
                shown = str(path)
            if shown in EXEMPT_NAMES:
                continue
            scanned += 1
            text = path.read_text(encoding="utf-8", errors="replace")
            findings += scan_text(shown, text, secrets)
    return findings, scanned


# -- the scanner's own probes ------------------------------------------------
#
# Standing rule, and the reason this file exists at all: a detector
# with no positive has never been observed to fire, and a dead detector and a
# clean tree both report zero. One must-fire per rule, and a must-not-fire that
# is deliberately made of near misses.
#
# The fake keys below are visibly synthetic and belong to nobody. A canary made
# from a real key would be the leak it is meant to catch.
MUST_FIRE = {
    "an OpenAI key prefix": 'sk-proj-CANARY0000000000000000notreal',
    "an Anthropic key prefix": 'sk-ant-api03-CANARY0000000notreal',
    "a Google key prefix": 'AIzaCANARY0000000000000notreal',
    "an Authorization header": '"Authorization": "Bearer CANARY000000000notreal"',
    "a bearer token": 'Bearer CANARY0000000000000notreal',
}

# Near misses, and the last two are not hypothetical: the first real run of
# this scan reported both, out of a tracked transcript, and both are the same
# defect class -- a pattern that fires on the *name* of a secret rather than
# its value. That run found no leak and two bugs in the scanner, which is the
# result a first run should be expected to produce.
MUST_NOT_FIRE = """
The endpoint reads its key from the variable LLOSSLESS_API_KEY_ENV names.
An Authorization header is built at the socket and stored nowhere: sk- is the
OpenAI prefix, sk-ant- is Anthropic's, AIza is Google's, and none of those
three fragments is a key. Bearer tokens are sent, never written.
memory/ask-before-hosted-api-endpoint.md is a filename, not an OpenAI key.
curl "$BASE/models" -H "Authorization: Bearer $LLOSSLESS_API_KEY" is a command
that reads a variable, and the variable name is documentation.
"""


def self_test() -> int:
    failures = []
    for label, probe in MUST_FIRE.items():
        found = scan_text("probe", f"prose around {probe} and more prose", {})
        if not any(label in line for line in found):
            failures.append(f"must-fire probe for {label} did not fire")
    quiet = scan_text("probe", MUST_NOT_FIRE, {})
    if quiet:
        failures.append(f"must-not-fire probe fired: {quiet}")

    # The literal rule, separately: it takes no pattern, so a shape probe
    # cannot exercise it. A vendor whose key format nobody anticipated is
    # exactly what it is for, so its canary deliberately looks like nothing.
    secrets = {"qwertyuiopasdfgh": "CANARY_API_KEY"}
    if not scan_text("probe", "a report saying qwertyuiopasdfgh out loud", secrets):
        failures.append("the literal-value rule did not fire on a value from the environment")
    if scan_text("probe", "a report saying qwertyuiopasdfg out loud", secrets):
        failures.append("the literal-value rule fired on a near miss")

    # And the finding must not repeat the secret, or a scan log becomes a
    # second copy of it.
    line = scan_text("probe", "qwertyuiopasdfgh", secrets)[0]
    if "qwertyuiopasdfgh" in line:
        failures.append(f"a finding printed the secret it found: {line!r}")
    if "CANARY_API_KEY" not in line:
        failures.append(f"a finding must name the variable instead: {line!r}")

    # `.env` parsing, which is its own code path and would otherwise be
    # exercised only on a machine that has one.
    with tempfile.TemporaryDirectory() as tmp:
        dotenv = Path(tmp) / ".env"
        dotenv.write_text('# a comment\nexport OPENAI_API_KEY="CANARYvalue0000000"\n'
                          'LLOSSLESS_BASE_URL=http://example.invalid/v1\n')
        read = environment_secrets(environ={}, dotenv=dotenv)
        if read != {"CANARYvalue0000000": "OPENAI_API_KEY (.env)"}:
            failures.append(f"the .env reader took the wrong things: {read}")

    # Reach, not shape. Everything above tests `scan_text` on a string that
    # was handed to it. This tests that a real file on disk is handed over at
    # all -- `scan_paths` had no probe of its own, so a skip rule that swallowed
    # a whole artefact kind would have left every check above green.
    #
    # The subject is the per-call ledger inside `report.json`,
    # because it is the newest surface and the one carrying per-call strings.
    # Nothing here is special-cased for it: the scan globs, so passing this is
    # evidence about every artefact kind, and the ledger is the witness.
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.json"
        row = {"role": "verify", "model": "test-model", "tier": "json_schema",
               "source": "live", "prompt_tokens": 100, "completion_tokens": 50}
        clean = {"provenance": {"ledger": [dict(row)]}}
        report.write_text(json.dumps(clean, indent=2), encoding="utf-8")
        found, scanned = scan_paths([Path(tmp)], {})
        if scanned != 1:
            failures.append(f"the scan did not read the report at all: {scanned} file(s)")
        if found:
            failures.append(f"a clean ledger must stay quiet: {found}")

        planted = {"provenance": {"ledger": [
            dict(row, model="sk-ant-api03-CANARY0000000notreal")]}}
        report.write_text(json.dumps(planted, indent=2), encoding="utf-8")
        found, _ = scan_paths([Path(tmp)], {})
        if not found:
            failures.append("a canary planted in a ledger row did not fire")

        # And against a value from the environment rather than a known shape,
        # which is the rule that has no pattern to match on.
        report.write_text(json.dumps(clean, indent=2).replace(
            '"test-model"', '"zxcvbnmasdfghjkl"'), encoding="utf-8")
        found, _ = scan_paths([Path(tmp)], {"zxcvbnmasdfghjkl": "CANARY_API_KEY"})
        if not found:
            failures.append("an environment secret in a ledger row did not fire")

    for line in failures:
        print(f"  FAIL {line}")
    if failures:
        return 1
    print(f"  self-test: {len(MUST_FIRE)} shape probe(s) fire, the literal rule fires "
          f"and stays quiet on a near miss, no finding repeats a secret, and a "
          f"canary planted in a report's ledger is reached on disk")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if self_test():
        return 1
    if args.self_test:
        return 0
    if not args.paths:
        ap.error("name at least one directory of artefacts, or --self-test")

    secrets = environment_secrets()
    findings, scanned = scan_paths(args.paths, secrets)
    for line in findings:
        print(f"  FAIL {line}")
    if findings:
        print(f"\n  {len(findings)} finding(s). A credential reached an artefact. "
              f"Fix the code path that wrote it; this scan is the backstop.")
        return 1
    print(f"  artefacts: {scanned} file(s) clean against {len(SHAPES)} shape rule(s) "
          f"and {len(secrets)} live secret(s) from the environment")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
