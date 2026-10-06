#!/usr/bin/env python3
"""Public text names no commit (2026-09-28).

A narrower version of this check already covers two documents this way --
the README's results intro and `docs/benchmark.md` may not name the release
benchmark's own pinned commit -- because the published repository starts a
fresh history and a hash from this one resolves to nothing there; the date is
what a reader of the published copy can act on. This file is the general form
of the same rule, over every page in `docs/` and over the web interface's own
texts, and lives in its own file rather than that one because this project is
worked by more than one agent at a time and that file is somebody else's.

Two shapes, because the two kinds of text quote a hash two different ways.
`docs/*.md` prose follows this repository's own convention for a short hash:
backtick code spans, seven to ten hex characters (the same shape the
narrower check looks for). The web interface's strings are not Markdown, so nothing
would ever wrap a hash in backticks there; a bare run of seven to ten hex
characters is what `measured {date} with LLossless {commit}` used to produce.
Neither shape is enough alone -- a prompt digest or a content digest is the
same alphabet and often the same length (`c33344d1450b` in `docs/results.md`
is twelve hex characters in backticks, one word this file's `docs/*.md` regex
does not even reach, and unrelated hex could coincidence into either shape by
chance) -- so every candidate is additionally asked of `git`: does it name a
real commit in this repository. A digest that happens to look like a short
hash and is not one of this repository's commits passes silently, which is
correct, because that is the whole reason the check exists rather than a
denylist of specific hashes: a denylist would go stale the day a *different*
commit gets pasted into a sentence, and this does not.

Run with `python3 tests/test_no_commit_ids.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# This module shells out to git and reads files; the guard is
# here because "and nothing else" is the part that needs a witness.
socket_guard.install()

DOCS = ROOT / "docs"
LOCALES = ROOT / "src" / "llossless" / "web" / "locales"

# This repository's own convention for a short hash in prose: a code span,
# seven to ten hex characters -- the same shape a companion check's own
# pattern looks for, so every page that quotes a hash is held to one rule.
BACKTICK_HASH = re.compile(r"`([0-9a-f]{7,10})`")

# The web interface's strings carry no Markdown, so a leaked hash there would
# not be backtick-quoted -- it would just be the value substituted into a
# sentence, as `models.measured.when` used to produce it. Word-bounded so a
# longer hex run (a sha256 digest) and a shorter one do not partially match.
BARE_HASH = re.compile(r"(?<![0-9a-fA-F])([0-9a-f]{7,10})(?![0-9a-fA-F])")

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def resolves_to_a_commit(candidate: str) -> bool:
    """Whether `candidate` names a real commit in this repository's history.

    The same idiom `audit_docs.py`'s `test_every_commit_hash_names_a_commit`
    uses: `git cat-file -e <hash>^{commit}` exits zero only when the prefix is
    unambiguous and the object it names is a commit, not a tree or a blob that
    happens to share the prefix.
    """
    found = subprocess.run(
        ["git", "cat-file", "-e", f"{candidate}^{{commit}}"],
        cwd=ROOT, capture_output=True,
    )
    return found.returncode == 0


def commit_ids_in(text: str, pattern: re.Pattern) -> list[str]:
    return sorted({c for c in set(pattern.findall(text)) if resolves_to_a_commit(c)})


def commit_id_problems(name: str, text: str, pattern: re.Pattern) -> list[str]:
    return [f"{name} names commit `{candidate}` in text meant for a reader who "
            f"will never hold this repository's history"
            for candidate in commit_ids_in(text, pattern)]


# Any Markdown heading. The probes below plant their text on the first one a
# page has, whatever it says, so renaming a heading cannot break a check that
# is about commit ids and nothing else.
HEADING = re.compile(r"^#{1,6} .*$", re.M)


def planted(page: str, addition: str) -> str:
    """`page` with `addition` put at the end of its first heading.

    A page with no heading at all gets the addition as a line of its own at
    the top, so the probe takes on any text it is handed.
    """
    heading = HEADING.search(page)
    if heading is None:
        return f"{addition.lstrip(' ,')}\n\n{page}"
    return page[:heading.end()] + addition + page[heading.end():]


def docs_probe_problems(sample: str, head: str) -> list[str]:
    """What is wrong with the two docs probes on `sample`, as sentences.

    Returned and not recorded, so the same two probes can be asked of a page
    whose headings were renamed and of one that has none.
    """
    problems = []
    # Must-fire: a real, resolvable commit (this repository's own HEAD)
    # planted into a copy of a real page.
    seeded = planted(sample, f", tool commit `{head}`")
    if seeded == sample or f"`{head}`" not in seeded:
        problems.append("the docs probe did not take")
    if not any(f"`{head}`" in problem
               for problem in commit_id_problems("seed", seeded, BACKTICK_HASH)):
        problems.append("seeded check: a real commit id planted in a docs page "
                        "passed")

    # Must-not-fire: a made-up hex string of the same shape, in backticks,
    # that names no commit (a digest or a placeholder) must not fire, or
    # this check would be a denylist of one specific hash by another name.
    # Planted at the same place, so the two probes differ in the hash alone.
    fake = planted(sample, ", ref `abc1234`")
    if fake == sample or "`abc1234`" not in fake:
        problems.append("the docs must-not-fire probe did not take")
    if commit_id_problems("seed", fake, BACKTICK_HASH) != commit_id_problems(
            "seed", sample, BACKTICK_HASH):
        problems.append("seeded check: a non-resolving, made-up hex string in "
                        "backticks wrongly fired")
    return problems


def test_no_commit_ids_in_docs() -> None:
    for path in sorted(DOCS.glob("*.md")):
        for problem in commit_id_problems(str(path.relative_to(ROOT)),
                                          path.read_text(encoding="utf-8"),
                                          BACKTICK_HASH):
            check(False, problem)

    head = subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    sample = (DOCS / "results.md").read_text(encoding="utf-8")
    problems = docs_probe_problems(sample, head)
    check(not problems, f"docs/results.md: {problems}")


def test_the_docs_probes_do_not_depend_on_a_heading() -> None:
    """Renaming every heading of the probed page leaves both probes working.

    The probes used to plant their text by replacing one heading of
    `docs/results.md` by name, so renaming that heading failed this file for a
    reason that has nothing to do with commit ids. Asked here of the real
    page with every heading reworded, of the page with its headings removed,
    and of an empty page: the must-fire probe still fires and the
    must-not-fire probe still does not.
    """
    head = subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    sample = (DOCS / "results.md").read_text(encoding="utf-8")
    renamed = HEADING.sub(lambda m: m.group(0).split(" ", 1)[0] + " Renamed", sample)
    check(renamed != sample and "## Renamed" in renamed,
          "the renaming did not take, so this check has nothing to stand on")
    for label, page in (("every heading renamed", renamed),
                        ("no heading", HEADING.sub("", sample)),
                        ("an empty page", "")):
        problems = docs_probe_problems(page, head)
        check(not problems, f"{label}: {problems}")

    # And the probes are still probes: with the lookup that decides what a
    # commit is switched off, the must-fire half has to report that it passed.
    real = globals()["resolves_to_a_commit"]
    try:
        globals()["resolves_to_a_commit"] = lambda candidate: False
        blind = docs_probe_problems(renamed, head)
        globals()["resolves_to_a_commit"] = lambda candidate: True
        eager = docs_probe_problems(renamed, head)
    finally:
        globals()["resolves_to_a_commit"] = real
    check(any("planted in a docs page passed" in problem for problem in blind),
          f"seeded check: a scan that finds no commit passed the must-fire "
          f"probe: {blind}")
    check(any("wrongly fired" in problem for problem in eager),
          f"seeded check: a scan that calls every hex string a commit passed "
          f"the must-not-fire probe: {eager}")


def test_no_commit_ids_in_the_web_ui() -> None:
    for path in sorted(LOCALES.glob("*.json")):
        strings = json.loads(path.read_text(encoding="utf-8"))["strings"]
        for key, value in strings.items():
            if not isinstance(value, str):
                continue
            for problem in commit_id_problems(f"{path.name}:{key}", value, BARE_HASH):
                check(False, problem)

    head = subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    seeded = f"measured 2026-09-29 with LLossless {head}"
    check(bool(commit_id_problems("seed", seeded, BARE_HASH)),
          "seeded check: a real commit id planted in a web UI string passed")

    fake = f"measured 2026-09-29 with LLossless {head[::-1]}"
    # A reversed hex string is still hex and still the right length; it is
    # exceedingly unlikely to also resolve as a commit, which is the point --
    # shape alone must not be enough to fail this check.
    if not resolves_to_a_commit(head[::-1]):
        check(not commit_id_problems("seed", fake, BARE_HASH),
              "seeded check: a non-resolving hex string of commit-hash shape "
              "wrongly fired")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_no_commit_ids" and callable(function):
            function()
    if failures:
        print(f"no commit ids: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"no commit ids: {checks} checks pass")
    return 0


def test_no_commit_ids() -> None:
    """pytest entry point."""
    assert main() == 0, "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
