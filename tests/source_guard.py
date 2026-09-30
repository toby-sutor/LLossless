#!/usr/bin/env python3
"""What a paid vendor is allowed to see. Enforced on the call path, not remembered.

The constraint has been standing since the first hosted arm was planned: a
third-party endpoint sees synthetic material only - the fixtures and pairs
committed under `tests/` - and never a private document, nor anything derived
from one. Until now it was a sentence in a brief. A sentence is not a control,
and this repository has already learned twice over that a check nobody runs
passes.

Why content and not path. "Only send files from `tests/`" is defeated by the
single most likely accident: copying a private document into `tests/` to make a
run work, then forgetting. So the question this asks is not *where did you read
it from* but *is this exact byte sequence something the repository already
committed*. Every document offered must sha256-match a blob tracked under
`tests/` at HEAD. That makes three different mistakes fail identically:

  - a file that was never committed          - no matching blob
  - a tracked file edited in the working tree - content differs from HEAD
  - a file from outside `tests/`              - no matching blob

Reading blobs from HEAD rather than from disk is deliberate. The working tree is
what a mistake edits; HEAD is what a human reviewed.

Fail closed. If provenance cannot be established the answer is no, not yes: git
unavailable, HEAD unborn, an empty tracked set, an unreadable blob, a document
of an unexpected type, or an empty document list all abort. Unknown is not
clean, the same way unknown is not zero one level down in `llossless.usage`.
A call that genuinely carries no document says so by name -
`NO_DOCUMENT` - because a bare `[]` is what a filter returns when it has gone
wrong, and the two must not look alike.

Scope: paid vendors only. Local ollama and the user's own pod are not third
parties and are not gated here. Nothing in `src/llossless/` imports this
module, and `self_test` asserts that, so no local run can be broken by it.

What this does NOT cover, stated because the limit is the part worth knowing: it
checks what leaves at call time, not what was committed. A private document
committed under `tests/` would hash to a tracked blob and pass. That direction
is the release scan's and the publication manifest's job, not this one.

Usage:
    python3 tests/source_guard.py --self-test
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tests"))
import repo_paths  # noqa: E402

# The directory whose committed contents are the whole of what may be sent.
APPROVED_TREE = "tests"


class UnapprovedSource(RuntimeError):
    """A document offered to a paid vendor is not committed synthetic material.

    Raised for the fail-closed cases too: an inability to answer the question is
    reported as a refusal, never as an approval.
    """


class _NoDocument:
    """Sentinel: this call carries no document at all (a SKU or tier probe)."""

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return "NO_DOCUMENT"


NO_DOCUMENT = _NoDocument()

_CACHE: dict[tuple[str, str], dict[str, str]] = {}


def _git(args: list[str], repo: Path) -> bytes:
    """Run git, or refuse. A git that will not answer is not a green light."""
    try:
        proc = subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, check=False)
    except OSError as exc:
        raise UnapprovedSource(
            f"cannot establish document provenance: git would not run ({exc}). "
            f"Refusing rather than assuming the documents are approved.") from exc
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip().splitlines()
        raise UnapprovedSource(
            f"cannot establish document provenance: `git {' '.join(args)}` exited "
            f"{proc.returncode} ({detail[0] if detail else 'no stderr'}). Refusing.")
    return proc.stdout


def head_digests(*, repo: Path | None = None) -> dict[str, str]:
    """sha256 of every blob tracked under `tests/` at HEAD -> the path it sits at.

    Cached per (repo, HEAD): the set cannot change without a commit, and this is
    consulted once per paid call.
    """
    root = (repo or REPO).resolve()
    head = _git(["rev-parse", "HEAD"], root).decode().strip()
    key = (str(root), head)
    if key in _CACHE:
        return _CACHE[key]

    listing = _git(["ls-tree", "-r", "-z", "HEAD", "--", APPROVED_TREE + "/"], root)
    entries: list[tuple[str, str]] = []
    for record in listing.split(b"\0"):
        if not record:
            continue
        meta, _, path = record.partition(b"\t")
        fields = meta.split()
        if len(fields) != 3:
            raise UnapprovedSource(
                f"cannot establish document provenance: unparseable ls-tree record "
                f"in {APPROVED_TREE}/ at {head[:12]}. Refusing.")
        if fields[1] == b"blob":
            entries.append((fields[2].decode(), path.decode("utf-8", "surrogateescape")))
    if not entries:
        raise UnapprovedSource(
            f"cannot establish document provenance: nothing is tracked under "
            f"{APPROVED_TREE}/ at {head[:12]}, so no document could be approved. "
            f"Refusing rather than treating an empty allow-set as permissive.")

    # Two entries can share a sha256 only by being byte-identical, so a
    # collision here loses nothing: either path is a truthful answer.
    digests = dict(zip(_git_batch([oid for oid, _ in entries], root),
                       (path for _, path in entries)))
    _CACHE[key] = digests
    return digests


def _git_batch(oids: list[str], repo: Path) -> list[str]:
    """sha256 of each object, in the order asked. Any short or malformed read aborts."""
    try:
        proc = subprocess.run(["git", "-C", str(repo), "cat-file", "--batch"],
                              input=("\n".join(oids) + "\n").encode(),
                              capture_output=True, check=False)
    except OSError as exc:
        raise UnapprovedSource(
            f"cannot establish document provenance: git cat-file would not run "
            f"({exc}). Refusing.") from exc
    if proc.returncode != 0:
        raise UnapprovedSource(
            "cannot establish document provenance: git cat-file exited "
            f"{proc.returncode}. Refusing.")

    out, at, digests = proc.stdout, 0, []
    for oid in oids:
        end = out.find(b"\n", at)
        if end < 0:
            raise UnapprovedSource(
                f"cannot establish document provenance: cat-file stopped before "
                f"{oid[:12]}. Refusing on a short read rather than on what arrived.")
        header = out[at:end].split()
        if len(header) != 3 or header[1] != b"blob":
            raise UnapprovedSource(
                f"cannot establish document provenance: {oid[:12]} did not read back "
                f"as a blob. Refusing.")
        size = int(header[2])
        start = end + 1
        if start + size + 1 > len(out):
            raise UnapprovedSource(
                f"cannot establish document provenance: {oid[:12]} is {size} bytes but "
                f"only {len(out) - start} arrived. Refusing.")
        digests.append(hashlib.sha256(out[start:start + size]).hexdigest())
        at = start + size + 1
    return digests


def approve(documents, *, repo: Path | None = None) -> list[str]:
    """Return the tracked path of each document, or refuse the whole call.

    Never quotes a document. A refusal names its index, its length and twelve
    hex characters, because the diagnostic for "this must not leave the machine"
    must not itself be a way of putting it in a log.
    """
    if documents is NO_DOCUMENT:
        return []
    if isinstance(documents, (str, bytes, bytearray)):
        raise UnapprovedSource(
            "documents must be a sequence of documents, not one document. A bare "
            "string is ambiguous between a path and a body; refusing.")
    offered = list(documents)
    if not offered:
        raise UnapprovedSource(
            "an empty document list is not the same as a call that carries no "
            "document: it is what a filter returns when it has gone wrong. Pass "
            "source_guard.NO_DOCUMENT to declare a document-free call.")

    digests = head_digests(repo=repo)
    approved: list[str] = []
    for index, document in enumerate(offered):
        if isinstance(document, str):
            blob = document.encode("utf-8")
        elif isinstance(document, (bytes, bytearray)):
            blob = bytes(document)
        else:
            raise UnapprovedSource(
                f"document {index} is {type(document).__name__}, not text or bytes. "
                f"Refusing rather than guessing how to hash it.")
        sha = hashlib.sha256(blob).hexdigest()
        path = digests.get(sha)
        if path is None:
            raise UnapprovedSource(
                f"document {index} ({len(blob)} bytes, sha256 {sha[:12]}) does not "
                f"match anything tracked under {APPROVED_TREE}/ at HEAD. Only "
                f"committed synthetic material may be sent to a paid vendor; an "
                f"uncommitted file, an edited one, or one from outside "
                f"{APPROVED_TREE}/ all land here.")
        approved.append(path)
    return approved


# -- probes -----------------------------------------------------------------
#
# Seeded both ways, per the standing rule. The must-not-fire side reads a real
# tracked pair; the must-fire side is the point of the module and gets three
# shapes - a private document if one is on this machine, an untracked stand-in
# if not, and a one-byte edit of an approved file.

def self_test() -> int:
    failures = []

    def check(condition, message):
        if not condition:
            failures.append(message)

    tracked = head_digests()
    check(len(tracked) > 100,
          f"the approved set should be the whole of {APPROVED_TREE}/, got {len(tracked)}")

    # must-not-fire: a real committed pair goes through, and reports its path.
    pair = REPO / "tests" / "pairs" / "index_429"
    bodies = sorted(p for p in pair.glob("*.md")) if pair.is_dir() else []
    check(bool(bodies), f"expected committed pair documents under {pair}")
    if bodies:
        texts = [p.read_text(encoding="utf-8") for p in bodies]
        try:
            named = approve(texts)
            check(len(named) == len(texts) and all(n.startswith("tests/") for n in named),
                  f"an approved pair must report tracked paths, got {named}")
        except UnapprovedSource as exc:
            failures.append(f"a committed pair was refused: {exc}")

    # must-fire, shape 1: material that is not in the repository at all. If a
    # private document is on this machine it is read in memory, read-only, and
    # never copied anywhere - it is the exact case the gate exists for. If not,
    # a synthesised untracked stand-in stands in; the assertion is the same.
    private = (sorted(repo_paths.ASSETS.glob("*.txt"))
               if repo_paths.ASSETS.is_dir() else [])
    if private:
        # Named by class, never by filename: a private document's name is
        # itself private vocabulary, and console output reaches logs.
        body, origin = private[0].read_bytes(), "a private document on this machine"
    else:
        body, origin = b"untracked stand-in, never committed\n" * 40, "an untracked stand-in"
    try:
        approve([body])
        failures.append(f"{origin} was approved for a paid vendor")
    except UnapprovedSource as exc:
        check("does not match anything tracked" in str(exc),
              f"{origin} was refused for the wrong reason: {exc}")
        # The refusal must not become the leak. Nothing of the body, in any
        # window long enough to be recognisable, may appear in the message.
        text, message = body.decode("utf-8", "replace"), str(exc)
        windows = [text[i:i + 24] for i in range(0, max(1, len(text) - 24), 7)]
        leaked = [w for w in windows if w.strip() and w in message]
        check(not leaked, f"the refusal for {origin} quoted the document itself")

    # must-fire, shape 2: an approved file with one byte changed. This is the
    # path check's blind spot and the reason the gate hashes content.
    if bodies:
        edited = bodies[0].read_text(encoding="utf-8") + " "
        try:
            approve([edited])
            failures.append("a one-space edit of a tracked pair was approved")
        except UnapprovedSource:
            pass

    # must-fire, shape 3: the empty list, which is what a broken filter returns.
    try:
        approve([])
        failures.append("an empty document list was approved")
    except UnapprovedSource as exc:
        check("NO_DOCUMENT" in str(exc), f"the empty-list refusal must name the sentinel: {exc}")

    # must-not-fire: the declared document-free call, for SKU and tier probes.
    try:
        check(approve(NO_DOCUMENT) == [], "NO_DOCUMENT must approve nothing, not refuse")
    except UnapprovedSource as exc:
        failures.append(f"NO_DOCUMENT was refused: {exc}")

    # fail-closed: no repository, no answer, no call. `git -C` walks upwards, so
    # the probe has to sit somewhere that is genuinely outside this tree.
    with tempfile.TemporaryDirectory() as outside:
        try:
            head_digests(repo=Path(outside))
            failures.append("a directory outside any repository yielded an approved set")
        except UnapprovedSource as exc:
            check("cannot establish document provenance" in str(exc),
                  f"an unanswerable tree must refuse by name, got: {exc}")

    # Scope: the tool itself must not import this, or the next
    # local ollama run breaks for a constraint that is about vendors.
    importers = [p.relative_to(REPO) for p in (REPO / "src").rglob("*.py")
                 if "source_guard" in p.read_text(encoding="utf-8")]
    check(not importers,
          f"src/ must not reach the vendor gate - local runs are not gated: {importers}")

    # And it must be on the call path, not beside it: the source probe lives in
    # tests/test_spend.py, which reads spend.py and requires the call site.

    for line in failures:
        print(f"  FAIL {line}")
    if failures:
        return 1
    print(f"  source guard: {len(tracked)} blobs approved under {APPROVED_TREE}/ at HEAD; "
          f"refuses {origin}, a one-byte edit and an empty list; "
          f"admits a committed pair and NO_DOCUMENT; src/ does not import it")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.parse_args()
    return self_test()


if __name__ == "__main__":
    raise SystemExit(main())
