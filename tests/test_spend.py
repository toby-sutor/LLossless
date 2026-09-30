#!/usr/bin/env python3
"""Run the spend caps' own probes as part of the suite.

`tests/spend.py` is a library the API harness imports, so its probes live
beside the code they exercise. This file exists so they are not opt-in: a cap
whose self-test nobody invokes is a cap that has never fired, which is the
state every control in this project has been caught in at least once.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import socket_guard  # noqa: E402

# The caps are the thing standing between a retry loop and the user's money, so
# "these probes make no call" is exactly the claim that has to be enforced
# rather than stated. The pacing probe runs on a fake clock and the ledger
# never opens a socket; the guard is what makes that checkable.
socket_guard.install()

import spend  # noqa: E402


def test_spend() -> None:
    """pytest entry point."""
    assert spend.self_test() == 0


def main() -> int:
    # `self_test` is not a gate on the clauses below. A seeded defect that
    # trips one of spend.py's own probes would, with an early return, also
    # stop every probe in this file from running - so one red clause would
    # hide the rest, and a must-fire probe cannot fire from behind it.
    inner = spend.self_test()
    caps = spend.FIRST_PASS
    failures = []
    if caps.spend != {"openai": 7.50, "anthropic": 7.50, "google": 0.00}:
        failures.append(f"the registered first-pass caps moved: {caps.spend}")
    for vendor in caps.spend:
        if vendor not in caps.interval:
            failures.append(f"{vendor} has a spend cap and no pacing entry")
    # Every priced SKU carries its provenance, for the same reason every
    # citation does: a price with no date cannot be checked and the run that
    # used it cannot be re-costed.
    for sku, price in spend.PRICES.items():
        if not price.source or not price.read_on:
            failures.append(f"{sku} is priced with no source or date")
    failures += gate_is_on_the_call_path()
    failures += range_reconciliation()
    for line in failures:
        print(f"  FAIL {line}")
    if failures or inner:
        return 1
    print(f"  spend caps: openai ${caps.spend['openai']:.2f}, anthropic "
          f"${caps.spend['anthropic']:.2f}, google ${caps.spend['google']:.2f}; "
          f"{caps.calls} calls, {caps.tokens:,} tokens; "
          f"{len(spend.PRICES)} SKU(s) priced; the vendor gate is the first "
          f"statement of Ledger.call and its argument has no default")
    return 0


# A value probe proves the guard refuses. It does not prove the guard is
# reached. `spend.self_test` covers the reach behaviourally, but a behavioural
# probe can be satisfied by a second copy of the check somewhere convenient, so
# this reads the shipped source and pins the call site itself: delete the line
# from `Ledger.call` and this goes red even if every other probe still passes.

def gate_is_on_the_call_path() -> list[str]:
    """Assert `Ledger.call` approves its documents before it does anything else."""
    found = []
    tree = ast.parse(Path(spend.__file__).read_text(encoding="utf-8"))
    ledger = next((n for n in tree.body
                   if isinstance(n, ast.ClassDef) and n.name == "Ledger"), None)
    if ledger is None:
        return ["tests/spend.py no longer defines a Ledger class"]
    call = next((n for n in ledger.body
                 if isinstance(n, ast.FunctionDef) and n.name == "call"), None)
    if call is None:
        return ["Ledger no longer defines call(), so nothing enforces the caps"]

    args = call.args
    named = [a.arg for a in args.kwonlyargs]
    if "documents" not in named:
        found.append("Ledger.call does not take a keyword-only `documents` argument")
    else:
        default = args.kw_defaults[named.index("documents")]
        if default is not None:
            found.append("Ledger.call gives `documents` a default, so a caller can "
                         "issue a paid call without declaring what it sends")

    # First statement after the docstring, and before the concurrency check, the
    # cost estimate, the caps and the yield. Position is the claim: nothing can
    # be spent or sent ahead of it.
    body = [n for n in call.body if not (isinstance(n, ast.Expr)
                                         and isinstance(n.value, ast.Constant))]
    if not body:
        return found + ["Ledger.call has no body"]
    first = ast.dump(body[0])
    if "source_guard" not in first or "approve" not in first or "documents" not in first:
        found.append("the first statement of Ledger.call is not "
                     "source_guard.approve(documents) - the vendor gate is not on "
                     "the call path, and a paid call can be issued without it")
    return found


# A ledger row for a call that failed before reporting usage is charged its
# estimate, and the vendor may or may not bill it. The comparison therefore has
# two bounds and the console may sit anywhere between. Seeded both ways, and at
# a width where a pass stops meaning very much.

def _snapshot(vendor: str, rows: list[tuple[float, bool]]) -> dict:
    return {
        "dollars": {vendor: sum(d for d, _ in rows)},
        "must_not_be_billed": [],
        "rows": [{"vendor": vendor, "dollars": d, "measured": m} for d, m in rows],
    }


def range_reconciliation() -> list[str]:
    found: list[str] = []

    def verdict(snap, charged):
        return {l.vendor: l for l in spend.reconcile(snap, charged)}["v"]

    # $0.40 measured, $0.20 booked as estimate for a call that raised. The
    # console may legitimately read anywhere in $0.40..$0.60.
    snap = _snapshot("v", [(0.40, True), (0.20, False)])
    low, high = spend.bounds(snap)["v"]
    if (round(low, 6), round(high, 6)) != (0.40, 0.60):
        found.append(f"bounds should be 0.40..0.60, got {low}..{high}")

    # MUST PASS: inside the range, including both ends and the middle.
    for figure in (0.40, 0.50, 0.60):
        line = verdict(snap, {"v": figure})
        if line.verdict != spend.AGREES:
            found.append(f"a console figure of ${figure:.2f} sits inside the "
                         f"${low:.2f}..${high:.2f} ledger range and must reconcile; "
                         f"got {line.verdict}")

    # MUST FAIL: outside it by more than the band, on either side. Below the
    # lower bound is the dangerous direction - it means the tool billed itself
    # for work the vendor has no record of.
    for figure in (0.20, 0.95):
        line = verdict(snap, {"v": figure})
        if line.verdict != spend.DISAGREES:
            found.append(f"a console figure of ${figure:.2f} is outside "
                         f"${low:.2f}..${high:.2f} and must not reconcile; "
                         f"got {line.verdict}")

    # A range no wider than one display unit is not a range worth reporting,
    # and the note should stay the plain one rather than inventing a caveat.
    narrow = _snapshot("v", [(0.40, True), (0.001, False)])
    if "range" in verdict(narrow, {"v": 0.401}).note:
        found.append("a sub-resolution range should read as a point comparison")

    # THE WIDE CASE. $0.01 measured, $0.03 of estimate: the range is 3x the
    # measured spend, so a console reading double the measured figure lands
    # inside it. That has to pass - it is genuinely inside - but the note must
    # say what the pass is worth, or a wide AGREES reads like a narrow one.
    wide = _snapshot("v", [(0.01, True), (0.03, False)])
    line = verdict(wide, {"v": 0.02})
    if line.verdict != spend.AGREES:
        found.append(f"a figure inside a wide range must still reconcile; "
                     f"got {line.verdict}")
    else:
        note = line.note
        for phrase in ("does NOT exclude an error", "3.0x the measured spend"):
            if phrase not in note:
                found.append(f"a pass at a range {line.width:.4f} wide must state "
                             f"what it does not certify; the note lacks {phrase!r}: "
                             f"{note!r}")

    # And the width has to come from the data, not be assumed: an all-measured
    # ledger collapses to the point comparison this replaced.
    clean = _snapshot("v", [(0.40, True), (0.20, True)])
    if tuple(round(b, 6) for b in spend.bounds(clean)["v"]) != (0.60, 0.60):
        found.append("an all-measured ledger must collapse to a point")
    if verdict(clean, {"v": 0.40}).verdict != spend.DISAGREES:
        found.append("with nothing unmeasured there is no range to hide in; "
                     "$0.40 against $0.60 must disagree")
    return found

if __name__ == "__main__":
    raise SystemExit(main())
