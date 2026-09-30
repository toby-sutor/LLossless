"""The half of the title policy that `reconcile` cannot hold: a written title is a claim.

`test_reconcile.py` asserts that `synthesise` emits no `TITLE_NOT_FROM_SOURCE`.
On its own that assertion is indistinguishable from the check having been
dropped, so this module holds the other end: the same invented title that the
byte-identical policies reject deterministically must still be rejected under
`synthesise`, by `merge.verify_title`, against the sources.

It cannot be done deterministically. The short form:

    sources: "a quad feels more stable at walking pace"
    title:   "A motorbike is more stable than a quad"

Every word of that title is in the sources and the claim is inverted. A
vocabulary check accepts it. So the title goes to the pass that reads both
texts, and this module proves the call is made and its verdict is honoured --
offline, with a stub, because what is under test is the wiring and not the
model.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless import merge, verify  # noqa: E402

DOCUMENTS = {
    "source_a.md": "# Motorbike vs. quad (ATV)\n\nA quad feels more stable at walking pace.\n",
    "source_b.md": "# Quad or Motorbike\n\nA motorbike must be balanced by the rider.\n",
}
CANDIDATES = ("Motorbike vs. quad (ATV)", "Quad or Motorbike")

failures: list[str] = []


class _SentinelClient:
    """Stands in for a `Client` and raises on the first thing asked of it."""

    def __getattr__(self, name: str):
        raise _Reached(name)


_SENTINEL_CLIENT = _SentinelClient()


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


class _Reached(Exception):
    """Raised by the sentinel client, to prove the call got that far."""


def _stub(verdict: str, seen: list[tuple[str, str]]):
    def _verify(client, claims, documents, direction, **kwargs):
        # A stub that accepts an argument the real function rejects is not a
        # stand-in for it. `direction="reverse"` lived here and at
        # `merge.py:739` for as long as this module has existed, and this
        # module stayed green throughout.
        if direction not in verify.DIRECTIONS:
            raise ValueError(
                f"unknown direction {direction!r}; "
                f"expected one of {verify.DIRECTIONS}")
        seen.append((claims[0].text, direction))
        return [verify.Verdict(
            claim_id="title", verdict=verdict, evidence="",
            evidence_source="source_a.md",
            rationale="the sources say the quad is the stable one",
            direction=direction, grounding="")]
    return _verify


def main() -> int:
    original = verify.verify_claims
    cases = (
        # title, stub verdict, call expected, finding expected, why
        ("Motorbike vs. quad (ATV)", "SUPPORTED", False, False,
         "a copied title costs no call and is never a finding"),
        ("Quad or Motorbike (ATV vs. Motorcycle)", "SUPPORTED", True, False,
         "a written title the sources support is permitted"),
        ("A motorbike is more stable than a quad", "CONTRADICTED", True, True,
         "the inversion every deterministic stand-in accepted"),
        ("Quad maintenance schedule", "MISSING", True, True,
         "a subject the documents neither state nor contradict"),
    )
    try:
        for title, verdict, wants_call, wants_finding, why in cases:
            seen: list[tuple[str, str]] = []
            verify.verify_claims = _stub(verdict, seen)
            finding = merge.verify_title(None, title, DOCUMENTS, CANDIDATES)
            check(bool(seen) == wants_call,
                  f"{title!r}: expected call={wants_call}, made={bool(seen)} ({why})")
            check((finding is not None) == wants_finding,
                  f"{title!r}: expected finding={wants_finding}, "
                  f"got={finding is not None} ({why})")
            check(all(d == verify.MERGED_TO_SOURCES for _, d in seen),
                  f"{title!r}: the title is a claim of the merged document and "
                  f"is checked against the sources, so the direction must be "
                  f"{verify.MERGED_TO_SOURCES!r}, got {[d for _, d in seen]}")
    finally:
        verify.verify_claims = original

    # The stub above can only prove the direction the caller passes. That the
    # real `verify_claims` accepts it is a separate question, and the one that
    # was wrong: a bad direction raises before any model call, so every merge
    # that wrote a new title errored its title step and exited 2.
    try:
        merge.verify_title(_SENTINEL_CLIENT, "Quad maintenance schedule",
                           DOCUMENTS, CANDIDATES)
    except _Reached:
        check(True, "")
    except ValueError as error:
        check(False, f"the real verify_claims refused the direction "
                     f"merge.verify_title passes: {error}")
    except Exception as error:  # noqa: BLE001 - any other failure is a real one
        check(False, f"merge.verify_title did not reach the model call: "
                     f"{type(error).__name__}: {error}")
    else:
        check(False, "merge.verify_title returned without reaching the "
                     "model call; the sentinel client was never used")

    for note in ():
        pass
    if failures:
        print(f"merge title guard: FAILED ({len(failures)} failing)")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"merge title guard: {len(cases) * 3 + 1} checks pass; a written title is "
          f"verified as a claim and a copied one costs no call")
    return 0


if __name__ == "__main__":
    sys.exit(main())
