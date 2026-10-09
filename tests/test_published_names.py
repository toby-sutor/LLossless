#!/usr/bin/env python3
"""One sweep over every published file: no old name, no commit id, no pointer into unpublished material.

The rename was checked surface by surface, which is exactly the shape of gap
that leaves a stray mention behind: fourteen source comments and fourteen
model-card notes still named the tool's old name or a commit, found only by
reading every file. And a published page kept pointing its reader at the
working repository's withheld directory, whose files that reader will never
hold. This file is the general form of all four rules, over every file the
publication manifest publishes (`published_files()` below), text files only.

Four things fail it:

  1. The tool's old name, "claimcheck", in any case, anywhere in a file's text.
  2. A hex string that resolves to a real commit in this repository's history
     (`tests/test_no_commit_ids.py`'s own git-verified method: shape alone is
     not enough, because a content digest or a prompt hash is the same
     alphabet and often the same length). A published copy is a file copy
     into a fresh repository, so its reader holds none of these commits.
  3. A pointer into `internal/`, the directory the manifest withholds whole:
     the decision log, the development write-ups, the working records and the
     maintainers' own tooling. A published file may name it only where the
     code has to cope with it being absent, and each such file is listed in
     `INTERNAL_POINTER_EXCEPTIONS` with the reason.
  4. A citation of the development record that the published copy does not
     hold, in the shapes that can be matched without a flood of false
     positives (`RECORD_POINTERS`): the word DECISIONS, "entry N", a
     "Brief XX" label, a "§N" section reference outside a line that names a
     published prompt, and a "task N" or "M7 task" label. A bare number used as
     a citation is judged by reading, not by a pattern: HTTP codes, sizes and
     counts share its shape.

**Exceptions live in the lists below, and nothing else is exempt.** Each entry
is a fact a publication reader would accept on sight, not a way to make a
sentence pass:

  (a) The data field names the rename left as machine keys: `claimcheck_commit`,
      `claimcheck_source`, `claimcheck_commit_end`, `claimcheck_commit_changed`.
      Matched exactly, as a whole word, wherever they appear: renaming them is
      a format change and is deferred, so a report written today still reads
      `claimcheck_commit` back, and prose that names the field has to say so.
  (b) The retired `CLAIMCHECK_` environment-variable prefix (`config.py`'s
      `DROPPED_ENV_PREFIXES`) and every test that sets a variable under it to
      prove the safety filter still drops it. Matched by exact case: nothing
      in this project shouts the tool's name in upper case for any other
      reason, so every real occurrence of that shape is this one family,
      prefix or full variable name or a test's own name built from one.
  (c) Recorded evidence, data rather than prose, skipped by directory, whole,
      for rules 1 and 2: `arms/` (every recorded run: raw reports,
      registrations, pins, commit ids captured verbatim, and old absolute
      paths from checkouts named "claimcheck"), `tests/responses/` (recorded
      model-response cassettes) and `paper/records/` (the graded run records
      the paper cites, recorded byte for byte). Rule 3 skips the same
      directories but reads the prose pages that live in them
      (`EVIDENCE_PROSE`): a README inside an evidence directory is written
      for a reader, not recorded.
  (d) File-scoped exceptions below, each naming exactly what the file does
      with the word, the id or the path, and why that is not prose about the
      product.

Run with `python3 tests/test_published_names.py`, or collect with pytest.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# This module shells out to git and reads files; the guard is here because
# "and nothing else" is the part that needs a witness.
socket_guard.install()

# The working repository's manifest auditor defines `published_files()` and
# `is_binary()` too, but it is withheld from publication, and a published file
# may not depend at runtime on a withheld one, so this file cannot import it
# and stay published. The two functions below are the same logic, kept in step
# by the same manifest they both read: `MANIFEST` and `BINARY_SNIFF` are that
# auditor's own names.
MANIFEST = ROOT / "publication-manifest.txt"
BINARY_SNIFF = 8192


def _git_ls_files() -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                         capture_output=True, text=True, check=True).stdout
    return sorted(p for p in out.splitlines() if p)


def _read_manifest() -> tuple[list[str], list[str]]:
    """(published entries, NOT-PUBLISHED entries). Comments and blanks dropped."""
    published, withheld = [], []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("NOT-PUBLISHED"):
            withheld.append(line.split(None, 1)[1])
        else:
            published.append(line)
    return published, withheld


def published_files() -> list[str]:
    """The tracked files the manifest publishes, withheld subtrees removed.

    The manifest auditor's own `published_files()`, ported rather than
    imported: the longer manifest entry is the more specific ruling and wins,
    so a file can be named more specifically than the directory that withholds
    it.
    """
    files = _git_ls_files()
    published, withheld = _read_manifest()
    entries = [(e, True) for e in published] + [(e, False) for e in withheld]
    out = []
    for f in files:
        matches = [(e, pub) for e, pub in entries if f == e or f.startswith(e + "/")]
        if not matches:
            continue
        _, pub = max(matches, key=lambda m: len(m[0]))
        if pub:
            out.append(f)
    return sorted(out)


def is_binary(path: Path) -> bool:
    """True when the file's head holds a NUL byte. Unreadable counts as binary."""
    try:
        with open(path, "rb") as handle:
            return b"\0" in handle.read(BINARY_SNIFF)
    except OSError:
        return True

# (a) exact field names ------------------------------------------------------

FIELD_NAME_EXCEPTIONS = frozenset({
    "claimcheck_commit",
    "claimcheck_source",
    "claimcheck_commit_end",
    "claimcheck_commit_changed",
})

# (b) the retired env-var prefix family --------------------------------------

UPPER_TOKEN = "CLAIMCHECK"

# (c) recorded-evidence directories, skipped whole ---------------------------

EXEMPT_DIRECTORIES = (
    "arms/",
    "tests/responses/",
    "paper/records/",
)

# (d) file-scoped name exceptions -------------------------------------------
#
# Each of these is a test proving the current code ignores or rejects a
# retired identifier, or a real path this task does not control. None of
# them is narrative prose about the product; each reason says what the file
# actually does with the word.
FILE_NAME_EXCEPTIONS: dict[str, str] = {
    "tests/test_web_accounts.py":
        "sets the retired cookie name `claimcheck_session` on a request to "
        "prove it no longer authenticates",
    "tests/test_web_credentials.py":
        "sets the retired header `X-Claimcheck-Token` on a request to prove "
        "it no longer authenticates",
    "tests/test_web_commands.py":
        "builds a temporary directory literally named `claimcheck`, and "
        "asserts the word never reaches stderr, proving the pre-rename "
        "config location is neither read nor mentioned",
    "tests/test_client.py":
        "builds a temporary directory and cache literally named `claimcheck`"
        "/`.claimcheck-cache`, and asserts the word never reaches stderr or "
        "a scratch directory's name, proving the pre-rename config, cache "
        "and scratch locations are neither read nor mentioned",
    "tests/test_cli.py":
        "runs the CLI as a subprocess with argv[0] literally set to "
        "`claimcheck`, proving the removed alias's program name changes "
        "nothing",
    "tests/test_web_static.py":
        "sets and asserts absent the retired `claimcheck.` localStorage key "
        "prefix, proving app.js no longer reads or writes it",
    "tests/annotate_merges.py":
        "this checkout is really named `claimcheck` (kept on purpose, per "
        "this project's own folder); an old absolute path recorded in an "
        "`arms/` report is re-rooted onto a clone by splitting on that real "
        "directory name, a path operation rather than prose",
    "tests/run_arm.py":
        "names the external artifact directory `claimcheck-run-artifacts/`, "
        "a path on disk kept by the same ruling that keeps this "
        "repository's own folder name",
    "tests/score_planted.py":
        "labels one input shape `\"claimcheck report\"` in this scorer's own "
        "`--json` diagnostic output, never rendered into a published document",
    # This file. Its own exception list and docstrings have to name the
    # identifiers they exclude to explain why: the file is the check, not
    # a claim about the product, and a reader auditing the list is reading
    # this file directly, not being told a fact by it.
    "tests/test_published_names.py":
        "this file's own exceptions and docstrings, which is what the list "
        "above and the probes below are for",
}

# commit ids that are recorded machine data, file-scoped ---------------------

COMMIT_ID_FILE_EXCEPTIONS: dict[str, str] = {
    "src/llossless/web/catalogue.json":
        "every commit id here is a `claimcheck_commit` field's own value",
    "tests/fixtures/restated/recorded-claims.json":
        "the recorded run's own `claimcheck_commit` value, the same kind of "
        "evidence as the field itself",
    "paper/generated/numbers.json":
        "generated, never typed: each figure's value beside the record it was "
        "read from. Its commit ids are the paper's own build stamp and values "
        "read from recorded data (a `claimcheck_commit`, a registration's pin), "
        "which are exempt in the files they are read from",
    "paper/generated/numbers.tex":
        "the same generated figures as numbers.json, as LaTeX macros",
    "tests/benchmark_matrix.py":
        "two hardcoded provenance commits, for the two rows (D3/D4, X8) "
        "with no committed record to read one from structurally; they feed "
        "`arms/BENCHMARK-MATRIX.md`, already exempt as recorded evidence",
    "tests/effort_figures.py":
        "the `PINNED` constant, the registered commit this arm was captured "
        "at (REGISTRATION.md), used only to validate the recording against "
        "it, never rendered into a published document",
    "tests/test_published_names.py":
        "this file's own docstrings and exception reasons cite examples",
    # Two evidence pages, read by rule 2 since the prose pages inside the
    # evidence directories are read for rules 3 and 4.
    "arms/BENCHMARK-MATRIX.md":
        "generated; its commit column is each run's recorded provenance "
        "(`claimcheck_commit` in the committed records), not a citation",
    "arms/README.md":
        "names the directory `k5c/discarded-pre-2bbd02f/`, whose name carries "
        "a commit id; a path on disk, not a citation",
}

# (3) pointers into `internal/` ----------------------------------------------

# A path into the withheld directory: `internal/` not glued to a longer word or
# path on its left, so `non-internal/` and `/x/internal/` inside some URL are
# not read as one. Case-sensitive: the directory is lower case.
INTERNAL_POINTER = re.compile(r"(?<![A-Za-z0-9_.-])internal/")

# Prose pages inside the evidence directories. Rules 1 and 2 skip these with
# their directory, because they quote recorded data; rule 3 reads them, because
# a pointer into `internal/` on a page written for a reader is prose.
EVIDENCE_PROSE = (
    "arms/README.md",
    "arms/BENCHMARK-MATRIX.md",
    "tests/responses/README.md",
)

# (4) citations of the unpublished development record -----------------------

# The shapes, each with the name a finding reports. Case-sensitive: the log is
# `DECISIONS.md`, and "decisions" in lower case is an ordinary word and a field
# name (`decisions[]`). "Entry" needs its number, so "an entry in the ledger"
# is not one; "Brief" needs a one- or two-letter capital label after it and no
# lower-case letter after that, so "Brief answers" is not one. A task label
# followed by " - " is the benchmark's own task heading in `docs/bench-spec.md`
# ("Task 1 - detect"), a published name rather than a citation.
RECORD_POINTERS = (
    ("DECISIONS", re.compile(r"\bDECISIONS\b")),
    ("an entry number", re.compile(r"\b[Ee]ntr(?:y|ies) \d{1,3}\b")),
    ("a brief label", re.compile(r"\bBrief [A-Z]{1,2}(?: v\d)?\b(?![a-z])")),
    ("a section reference", re.compile(r"§\s?\d")),
    ("a task label", re.compile(r"\bM\d{1,2} task\b|\b[Tt]asks? \d{1,2}\b(?! - )")),
)

# A section sign on a line that names a published prompt points into that
# prompt, which the reader holds.
PROMPT_REFERENCE = re.compile(r"prompts/[\w./-]+\.md")

# The files that must cite the record, each with the reason. Each must still
# carry a match, or the entry fails as stale.
RECORD_POINTER_EXCEPTIONS: dict[str, str] = {
    "publication-manifest.txt":
        "the manifest records each publication ruling beside the decision that "
        "made it; it is the one published file whose job is to cite that record",
    "paper/generated/numbers.json":
        "the three `blindspot.*` keys name the unpublished decision log as their "
        "record, which the paper states in its text; no decision number appears",
    "tests/repo_paths.py":
        "defines the path of the decision log, `DECISIONS.md`, for the withheld "
        "maintainers' tooling that imports this module; a path, not a citation",
    "tests/mahjongg_figures.py":
        "`DECISION`, the rescoring stamp written into the committed arm records "
        "(`scored.json`, `tables.md`) and checked against them byte for byte",
    "tests/regrade_guard_probes.py":
        "the note it writes into its graded record, reproduced byte for byte "
        "from the committed record it regenerates",
    "tests/test_web_static.py":
        "the page's jargon scanner, whose pattern and must-fire seed name the "
        "word DECISIONS so that a decision number can never reach the page",
    "tests/test_published_names.py":
        "this file: its rule, its exception list and its probes have to spell "
        "the shapes they exclude",
}

# The files that must name `internal/` because the code copes with it being
# absent in a published copy, or because the file is the rule itself.
INTERNAL_POINTER_EXCEPTIONS: dict[str, str] = {
    "publication-manifest.txt":
        "the manifest is the list of what is withheld; `NOT-PUBLISHED internal` "
        "is the entry that withholds the directory",
    ".gitignore":
        "ignores `/internal/assets/`, the untracked source documents, so a clone "
        "that has them cannot add them by accident",
    "tests/run_all.py":
        "names the withheld tools by path so that a published copy, where they "
        "are absent, reports them as withheld instead of failing",
    "paper/Makefile":
        "runs the withheld number generator and number check where they are "
        "present, and says so and builds from the committed figures where not",
    "scripts/build_arm_bundle.py":
        "imports the withheld provider-name detector by path where it is present "
        "and runs the other four detectors, saying so, where it is not",
    "tests/test_catalogue.py":
        "the same import of the withheld provider-name detector, and the SKIP "
        "line it prints when the detector is absent",
    "tests/run_lineup.py":
        "refuses a pinned clone that carries `internal/assets`, the untracked "
        "source documents, so the path is the thing being checked for",
    "tests/test_run_lineup.py":
        "plants `internal/assets` in a scratch clone to prove that refusal fires",
    "tests/effort_figures.py":
        "names the withheld scoring pipeline in the UNMEASURED line that says "
        "re-scoring cannot be done from a published copy",
    "tests/opus55_effort_figures.py":
        "the same UNMEASURED line, for the 2026-09-26 run's withheld pipeline",
    "tests/test_published_names.py":
        "this file: its rule, its exception list and its probes have to name "
        "the directory they exclude",
}


# detection -------------------------------------------------------------------

# The whole alnum-or-underscore run touching a "claimcheck" match, so a field
# name or an env var is checked as one token rather than a substring of it.
# `\_` normalises first (below): LaTeX escapes every literal underscore, so
# `claimcheck\_commit` reads the same as `claimcheck_commit` once that is
# undone, and nowhere else does this repository write a bare `\_`.
NAME_WORD = re.compile(r"[A-Za-z0-9_]*claimcheck[A-Za-z0-9_]*", re.IGNORECASE)

# This repository's convention for a short hash in prose (backtick code
# spans, `tests/test_no_commit_ids.py`'s `BACKTICK_HASH`) covers `docs/*.md`
# only; the rest of the published set, JSON, Python, LaTeX, quotes a hash
# bare or in backticks or inside a string literal, so this looks for the
# digits alone, from a short hash (7) up to a full sha256 (well past a git
# object id, so nothing here is under-matched for want of length).
BARE_HASH = re.compile(r"(?<![0-9a-fA-F])([0-9a-f]{7,40})(?![0-9a-fA-F])")

_commit_cache: dict[str, bool] = {}


def resolves_to_a_commit(candidate: str) -> bool:
    """Whether `candidate` names a real commit in this repository's history.

    `tests/test_no_commit_ids.py`'s own idiom: `git cat-file -e <hash>^{commit}`
    exits zero only when the prefix is unambiguous and the object it names is
    a commit, not a tree or a blob that happens to share the prefix.
    """
    if candidate not in _commit_cache:
        found = subprocess.run(
            ["git", "cat-file", "-e", f"{candidate}^{{commit}}"],
            cwd=ROOT, capture_output=True,
        )
        _commit_cache[candidate] = (found.returncode == 0)
    return _commit_cache[candidate]


def name_problems(rel_path: str, text: str) -> list[str]:
    """Every unexempted "claimcheck" in `text`, named by `rel_path`."""
    if rel_path in FILE_NAME_EXCEPTIONS:
        return []
    normalised = text.replace("\\_", "_")
    out = []
    for match in NAME_WORD.finditer(normalised):
        word = match.group(0)
        if word in FIELD_NAME_EXCEPTIONS:
            continue
        if UPPER_TOKEN in word:
            continue
        start = max(0, match.start() - 20)
        end = min(len(normalised), match.end() + 20)
        out.append(f"{rel_path}: the old name appears as {word!r} "
                   f"(...{normalised[start:end]!r}...)")
    return out


def commit_problems(rel_path: str, text: str) -> list[str]:
    """Every commit id resolving in this repository's history, named by `rel_path`."""
    if rel_path in COMMIT_ID_FILE_EXCEPTIONS:
        return []
    out = []
    for candidate in sorted(set(BARE_HASH.findall(text))):
        if resolves_to_a_commit(candidate):
            out.append(f"{rel_path}: names commit `{candidate}` in text meant "
                       f"for a reader who will never hold this repository's history")
    return out


def internal_problems(rel_path: str, text: str) -> list[str]:
    """Every pointer into `internal/` in `text`, named by `rel_path` and line."""
    if rel_path in INTERNAL_POINTER_EXCEPTIONS:
        return []
    out = []
    for number, line in enumerate(text.splitlines(), 1):
        if INTERNAL_POINTER.search(line):
            out.append(f"{rel_path}:{number}: points into internal/, which a "
                       f"reader of the published copy does not have: "
                       f"{line.strip()[:120]!r}")
    return out


def record_problems(rel_path: str, text: str) -> list[str]:
    """Every citation of the unpublished record in `text`, by `rel_path` and line."""
    if rel_path in RECORD_POINTER_EXCEPTIONS:
        return []
    out = []
    for number, line in enumerate(text.splitlines(), 1):
        for name, pattern in RECORD_POINTERS:
            if name == "a section reference" and PROMPT_REFERENCE.search(line):
                continue
            if pattern.search(line):
                out.append(f"{rel_path}:{number}: cites the development record "
                           f"({name}), which a reader of the published copy does "
                           f"not hold: {line.strip()[:120]!r}")
                break
    return out


def scan(rel_path: str, text: str) -> list[str]:
    return (name_problems(rel_path, text) + commit_problems(rel_path, text)
            + internal_problems(rel_path, text) + record_problems(rel_path, text))


failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def test_every_exception_is_used() -> None:
    """A stale entry hides nothing; it just clutters the list. A wrong one
    silently defeats the sweep, so every exempted file still exists and every
    exempted directory still holds a published file, or the list has drifted
    from what it describes."""
    files = published_files()
    file_set = set(files)
    for rel_path in FILE_NAME_EXCEPTIONS:
        if rel_path == "tests/test_published_names.py":
            continue
        check(rel_path in file_set,
              f"FILE_NAME_EXCEPTIONS names {rel_path}, which is not a published file")
    for rel_path in COMMIT_ID_FILE_EXCEPTIONS:
        if rel_path == "tests/test_published_names.py":
            continue
        check(rel_path in file_set,
              f"COMMIT_ID_FILE_EXCEPTIONS names {rel_path}, which is not a published file")
    check(any(f.startswith(d) for f in files for d in EXEMPT_DIRECTORIES),
          "EXEMPT_DIRECTORIES names nothing that is actually published")
    # On disk rather than in `file_set`: a published copy is a fresh
    # repository, and its root `.gitignore` swallows new root `*.txt` files,
    # so the manifest is on disk there without being tracked.
    for rel_path in INTERNAL_POINTER_EXCEPTIONS:
        check((ROOT / rel_path).is_file(),
              f"INTERNAL_POINTER_EXCEPTIONS names {rel_path}, which is not in this tree")
        if (ROOT / rel_path).is_file() and rel_path != "tests/test_published_names.py":
            text = (ROOT / rel_path).read_text(encoding="utf-8", errors="ignore")
            check(bool(INTERNAL_POINTER.search(text)),
                  f"INTERNAL_POINTER_EXCEPTIONS names {rel_path}, which no longer "
                  f"points into internal/; the exception is stale")
    for rel_path in EVIDENCE_PROSE:
        check(rel_path in file_set,
              f"EVIDENCE_PROSE names {rel_path}, which is not a published file")
    for problem in stale_record_exceptions(ROOT):
        check(False, problem)


def stale_record_exceptions(root: Path) -> list[str]:
    """Rule 4's exceptions that no longer name a file, or no longer need to.

    On disk, like rule 3's, for the same reason. Split out so the probe below
    can run it against a scratch tree holding one genuinely stale entry.
    """
    out = []
    for rel_path in RECORD_POINTER_EXCEPTIONS:
        path = root / rel_path
        if not path.is_file():
            out.append(f"RECORD_POINTER_EXCEPTIONS names {rel_path}, which is not in this tree")
            continue
        if rel_path == "tests/test_published_names.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not any(pattern.search(text) for _, pattern in RECORD_POINTERS):
            out.append(f"RECORD_POINTER_EXCEPTIONS names {rel_path}, which no longer "
                       f"cites the record; the exception is stale")
    return out


def test_the_published_set_names_no_old_name_and_no_commit() -> None:
    """The real sweep: every published text file, exceptions applied."""
    files = published_files()
    scanned = 0
    for rel_path in files:
        if any(rel_path.startswith(d) for d in EXEMPT_DIRECTORIES):
            if rel_path in EVIDENCE_PROSE:
                text = (ROOT / rel_path).read_text(encoding="utf-8", errors="ignore")
                for problem in (commit_problems(rel_path, text)
                                + internal_problems(rel_path, text)
                                + record_problems(rel_path, text)):
                    check(False, problem)
            continue
        path = ROOT / rel_path
        if is_binary(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        scanned += 1
        for problem in scan(rel_path, text):
            check(False, problem)
    check(scanned > 400, f"only {scanned} files were scanned; published_files() "
         f"looks broken, or a new EXEMPT_DIRECTORIES entry has swallowed too much")


def test_a_planted_old_name_and_commit_id_are_caught() -> None:
    """Must-fire: a real published text file, copied to scratch, with the old
    name and this repository's own HEAD dropped into its prose."""
    sample_rel = "README.md"
    sample = (ROOT / sample_rel).read_text(encoding="utf-8")
    head = subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    with tempfile.TemporaryDirectory() as raw:
        scratch = Path(raw) / sample_rel
        seeded = sample + (f"\n\nThis tool, formerly ClaimCheck, was rebuilt "
                           f"at commit {head} for this release; the reasons are "
                           f"in internal/docs/DECISIONS.md.\n")
        scratch.write_text(seeded, encoding="utf-8")
        found = scan(sample_rel, scratch.read_text(encoding="utf-8"))
    check(any("old name" in p for p in found),
          "seeded check: a planted mention of the old name passed")
    check(any("names commit" in p for p in found),
          "seeded check: a planted real commit id passed")
    check(any("points into internal/" in p for p in found),
          "seeded check: a planted pointer into internal/ passed")


def test_a_pointer_into_internal_is_caught_in_evidence_prose() -> None:
    """Must-fire: the carve-back works. A pointer planted into a prose page
    inside an evidence directory fires, even though rules 1 and 2 skip that
    directory."""
    sample_rel = "arms/README.md"
    seeded = ((ROOT / sample_rel).read_text(encoding="utf-8")
              + "\n\nThe scorer is `internal/arms/score_grid.py`.\n")
    found = internal_problems(sample_rel, seeded)
    check(len(found) == 1,
          f"seeded check: one pointer planted into {sample_rel} gave {len(found)} finding(s)")


def test_words_that_only_look_like_internal_do_not_fire() -> None:
    """Must-not-fire: the word and its neighbours, and a longer path that
    merely contains the name, are not pointers into the withheld directory."""
    sample_rel = "README.md"
    seeded = ((ROOT / sample_rel).read_text(encoding="utf-8")
              + "\n\nThe report is internally consistent. `internal_score`, "
                "`non-internal/` and `internal_notes/` are other names, and "
                "`internals/` is another directory.\n")
    found = internal_problems(sample_rel, seeded)
    check(not found,
          f"seeded check: words that are not a pointer into internal/ fired: {found}")
    exempt = "tests/run_all.py"
    check(not internal_problems(exempt, "see internal/tests/rehearse_publication.py\n"),
          "seeded check: a file on INTERNAL_POINTER_EXCEPTIONS fired")


# One must-fire and one must-not-fire line per rule-4 shape. Each must-fire line
# carries exactly one shape, so a finding names the shape that fired it.
RECORD_MUST_FIRE = (
    ("DECISIONS", "The ceiling was raised (see DECISIONS 608)."),
    ("an entry number", "The default moved to 3%, as entry 446 records."),
    ("a brief label", "Brief AL item 2 wants the guard checked afterwards."),
    ("a brief label", "Brief DS stage 3 declares a combination."),
    ("a section reference", "The budget rule of §2.6 is what fails the run."),
    ("a task label", "PARTIAL has been a verdict since task 24."),
    ("a task label", "Written for the M7 task that wired the exit code."),
)
RECORD_MUST_NOT_FIRE = (
    "The merge records its decisions in `decisions[]`, one per conflict.",
    "Every cache entry in the ledger is keyed by the request digest.",
    "Brief answers are allowed; a Brief overview comes first.",
    "The endpoint answered (404) and then (200); a title is capped at (120).",
    "for index in range(10): the loop runs over 10 items of 2,048 bytes.",
    "The rule is in `prompts/merge.md` §3, which every level renders.",
    "The recordings live in `tests/responses/m4/`; the task at hand is smaller.",
    "## 2. Task 1 - detect",
)


def test_a_citation_of_the_record_is_caught_in_each_shape() -> None:
    """Must-fire: each shape, planted into a published page, fires as that shape;
    and the carve-back: it fires in an evidence prose page too."""
    sample = (ROOT / "README.md").read_text(encoding="utf-8")
    for name, line in RECORD_MUST_FIRE:
        found = record_problems("README.md", sample + "\n\n" + line + "\n")
        check(len(found) == 1 and f"({name})" in found[0],
              f"seeded check: {line!r} should fire once as {name}, got {found}")
    arms = (ROOT / "arms" / "README.md").read_text(encoding="utf-8")
    found = record_problems("arms/README.md", arms + "\n\nSee DECISIONS 608.\n")
    check(len(found) == 1,
          f"seeded check: a citation planted into arms/README.md gave {len(found)} finding(s)")


def test_words_that_only_look_like_a_citation_do_not_fire() -> None:
    """Must-not-fire: the ordinary words, HTTP codes, sizes, a prompt section and
    a published directory name that share the shapes' letters."""
    sample = (ROOT / "README.md").read_text(encoding="utf-8")
    for line in RECORD_MUST_NOT_FIRE:
        found = record_problems("README.md", sample + "\n\n" + line + "\n")
        check(not found, f"seeded check: {line!r} is not a citation and fired: {found}")
    check(not record_problems("publication-manifest.txt", "DECISIONS 34.\n"),
          "seeded check: a file on RECORD_POINTER_EXCEPTIONS fired")


def test_a_stale_record_exception_is_caught() -> None:
    """Must-fire: an exception whose file no longer cites the record, and one
    whose file is gone, are both reported; a live one is not."""
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        for rel_path in RECORD_POINTER_EXCEPTIONS:
            (root / rel_path).parent.mkdir(parents=True, exist_ok=True)
            (root / rel_path).write_text("cites DECISIONS 1\n", encoding="utf-8")
        check(not stale_record_exceptions(root),
              "seeded check: live exceptions were reported as stale")
        (root / "tests" / "repo_paths.py").write_text("no citation here\n", encoding="utf-8")
        (root / "tests" / "mahjongg_figures.py").unlink()
        found = stale_record_exceptions(root)
        check(len(found) == 2 and any("tests/repo_paths.py" in p and "stale" in p for p in found)
              and any("tests/mahjongg_figures.py" in p and "not in this tree" in p for p in found),
              f"seeded check: a stale and a missing exception must both fire, got {found}")


def test_an_exempt_field_name_does_not_fire() -> None:
    """Must-not-fire: the exact machine key, in prose, must not trip the sweep."""
    sample_rel = "README.md"
    sample = (ROOT / sample_rel).read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as raw:
        scratch = Path(raw) / sample_rel
        seeded = sample + ("\n\nEvery report before the rename carries "
                           "claimcheck_commit in its provenance block.\n")
        scratch.write_text(seeded, encoding="utf-8")
        found = scan(sample_rel, scratch.read_text(encoding="utf-8"))
    check(not found,
          f"seeded check: the exempt field name claimcheck_commit wrongly fired: {found}")


def test_a_non_resolving_hex_string_does_not_fire() -> None:
    """Must-not-fire: a content digest of the right shape, not a commit, must pass."""
    sample_rel = "README.md"
    sample = (ROOT / sample_rel).read_text(encoding="utf-8")
    head = subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    fake = head[::-1]
    if resolves_to_a_commit(fake):
        return  # astronomically unlikely; skip rather than risk a false red
    with tempfile.TemporaryDirectory() as raw:
        scratch = Path(raw) / sample_rel
        seeded = sample + f"\n\nThe fixture's digest is {fake}.\n"
        scratch.write_text(seeded, encoding="utf-8")
        found = scan(sample_rel, scratch.read_text(encoding="utf-8"))
    check(not found,
          f"seeded check: a non-resolving hex string of commit-hash shape wrongly fired: {found}")


def ignored_published_files(files: list[str]) -> list[str]:
    """The published files the tree's own .gitignore would swallow.

    A published copy is staged into a fresh repository by adding every file,
    and an ignored file is silently left out of that add, so a published file
    the root .gitignore matches never reaches the public repository.
    """
    out = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "--no-index", "--stdin"],
                         input="\n".join(files), capture_output=True, text=True)
    return out.stdout.split()


def test_no_published_file_is_ignored() -> None:
    files = published_files()
    ignored = ignored_published_files(files)
    check(not ignored, f"the root .gitignore swallows published file(s) {ignored}; "
                       "a fresh repository staged with `git add -A` would leave them out")
    probe = ignored_published_files(["a-new-root-merge.md", "README.md"])
    check(probe == ["a-new-root-merge.md"],
          f"a new root .md must be ignored and README.md must not; got {probe}")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_published_names" and callable(function):
            function()
    if failures:
        print(f"published names: {len(failures)} of {checks} checks failed")
        for failure in failures[:50]:
            print(f"  - {failure}")
        if len(failures) > 50:
            print(f"  ... and {len(failures) - 50} more")
        return 1
    print(f"published names: {checks} checks pass")
    return 0


def test_published_names() -> None:
    """pytest entry point."""
    assert main() == 0, "\n".join(failures[:20])


if __name__ == "__main__":
    sys.exit(main())
