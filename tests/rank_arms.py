#!/usr/bin/env python3
"""Rank every recorded arm the way the operator asked: silent loss, then band, then cost, then speed.

Silent loss is primary because it is the tool's core feature - dropping content
and declaring it is acceptable behaviour, dropping it silently is the defect.

The band is the operator's own `reference.md`, tracked at
`tests/handwritten/<pair>/`, which is what they would expect at `high`
fidelity. It is a REFERENCE, not an oracle: their merges themselves
drop content (22 of 60 segments on `curry`), so deviation is scored in both
directions and neither 0% nor 100% coverage is the target.

    lost  = {model absent} & {editor kept}    over-dropping
    bloat = {model kept}   & {editor absent}  failure to edit, the literal merge

A one-sided figure would rank the literal merge first: it cannot drop what the
editor kept because it drops nothing. Both are scored, and a silent-loss of 0 is
read beside the declared count so a no-op merge cannot game the primary axis.
"""
import json, sys, collections, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from llossless import reconcile
# Every `source_<letter>.md` a pair has, from `a` with no gap, refused if there
# is one. Reading `source_a.md` and `source_b.md` by name was right for every
# pair in `PAIRS` and would have dropped a third source silently.
from analyse_merges import sources_of

# The recorded arms are published under `arms/`. An
# override root (the scratch mirror they were first written to) still works:
# `LLOSSLESS_ARTEFACTS_ROOT` names the directory holding the original
# `2026-09-17-frontier-thinking`, `2026-09-17-ladder-high` and `2026-09-18-gaps`.
# Run directories are still named for the corpus as it was when the arms ran,
# so the keys stay `toby-test-N`; the documents they name are tracked at
# `tests/handwritten/<pair>/`.
CORPUS = REPO / "tests" / "handwritten"
PAIRS = {"toby-test-1": "birthday",
         "toby-test-2": "chickens",
         "toby-test-4": "christianity",
         "toby-test-5": "curry"}
_B = os.environ.get("LLOSSLESS_ARTEFACTS_ROOT")
RUNS = ([Path(_B)/"2026-09-17-frontier-thinking", Path(_B)/"2026-09-17-ladder-high",
         Path(_B)/"2026-09-18-gaps"] if _B else
        [REPO/"arms"/"2026-09-17"/"frontier-thinking", REPO/"arms"/"2026-09-17"/"ladder-high",
         REPO/"arms"/"2026-09-18"/"gaps"])

def sets(docs, text):
    r = reconcile.reconcile(docs, text)
    ab = {L.segment.id for c in r.coverages for L in c.located if L.verdict == "absent"}
    kp = {L.segment.id for c in r.coverages for L in c.located if L.verdict != "absent"}
    return ab, kp, len(r.duplicates), r.order.runs

def band(name):
    """(sources, reference-absent ids, reference-kept ids) for one hand-written pair."""
    docs = sources_of(name, CORPUS)
    habs, hkept = sets(docs, (CORPUS/name/"reference.md").read_text())[:2]
    return docs, habs, hkept


def cell_figures(name, merged, rep):
    """One merge of hand-written pair `name` against its `reference.md`.

    The whole of this ranking's scoring, as a function so that another run's
    figures are formed by the same code (`tests/phase4_figures.py`). Unlike
    `rank_matrix.cell_figures` it does not forgive confirmed declarations or
    the title: this is the scoring the catalogue's
    2026-09-16 rows were made with.
    """
    docs, habs, hkept = band(name)
    mabs, mkept, dup, _runs = sets(docs, merged)
    decl = {x["segment"] for x in (rep.get("declarations") or []) if x.get("segment")}
    return dict(silent=len(mabs-decl), declared=len(mabs&decl), lost=len(mabs&hkept),
                bloat=len(mkept&habs), dup=dup)


def collect(runs=None):
    """(cells, per-arm totals) over the `high` cells of `runs`."""
    bands = {pair for pair, name in PAIRS.items() if (CORPUS/name/"reference.md").exists()}
    agg = collections.defaultdict(lambda: collections.Counter())
    cells = []
    for root in (RUNS if runs is None else runs):
        rp = root/"results.json"
        if not rp.exists(): continue
        rows = {(r["pair"], r["fidelity"], r["arm"]): r for r in json.loads(rp.read_text())}
        for cell in sorted(os.listdir(root)):
            d = root/cell
            if not (d/"report.json").exists() or not (d/"merged.md").exists(): continue
            pair = next((p for p in PAIRS if cell.startswith(p)), None)
            if pair is None or pair not in bands: continue
            fid = "high" if "-high-" in cell else "low"
            if fid != "high":     # high is the product; low is the literal-merge control
                continue
            arm = cell[len(pair)+len(fid)+2:]
            rep = json.loads((d/"report.json").read_text())
            row = rows.get((pair, fid, arm), {})
            cost = max(row.get("cost_usd") or 0.0, row.get("cost_usd_billed") or 0.0)
            rec = dict(arm=arm, pair=pair,
                       **cell_figures(PAIRS[pair], (d/"merged.md").read_text(), rep),
                       cost=cost, secs=row.get("wall_seconds") or 0.0,
                       commit=str((rep.get("provenance") or {}).get("claimcheck_commit"))[:7])
            cells.append(rec)
            t = agg[arm]
            for k in ("silent","declared","lost","bloat","dup"): t[k] += rec[k]
            t["n"] += 1; t["cost100"] += int(round(cost*100)); t["secs"] += int(rec["secs"])
    return cells, agg


def main():
    cells, agg = collect()

    print("PER CELL (high fidelity only)\n")
    print(f"{'arm':<20}{'pair':<13}{'SILENT':>7}{'decl':>6}{'lost':>6}{'bloat':>7}{'dup':>5}{'$':>8}{'s':>8}")
    for c in sorted(cells, key=lambda c:(c["arm"], c["pair"])):
        print(f"{c['arm']:<20}{c['pair']:<13}{c['silent']:>7}{c['declared']:>6}{c['lost']:>6}"
              f"{c['bloat']:>7}{c['dup']:>5}{c['cost']:>8.3f}{c['secs']:>8.1f}")

    print("\nRANKED: silent loss, then band deviation (lost+bloat+dup), then cost, then speed\n")
    print(f"{'model':<20}{'pairs':>6}{'SILENT':>7}{'decl':>6}{'lost':>6}{'bloat':>7}{'dup':>5}{'$/merge':>9}{'s/merge':>9}")
    for arm, t in sorted(agg.items(), key=lambda kv: (kv[1]["silent"],
                                                      kv[1]["lost"]+kv[1]["bloat"]+kv[1]["dup"],
                                                      kv[1]["cost100"]/max(kv[1]["n"],1),
                                                      kv[1]["secs"]/max(kv[1]["n"],1))):
        n = max(t["n"], 1)
        print(f"{arm:<20}{t['n']:>6}{t['silent']:>7}{t['declared']:>6}{t['lost']:>6}"
              f"{t['bloat']:>7}{t['dup']:>5}{t['cost100']/100/n:>9.3f}{t['secs']/n:>9.1f}")
    print("\n  Denominators differ where an arm covers fewer pairs - compare per-cell, not just totals.")
    print("  silent=0 with a low declared count and high bloat is a merge that did not edit,")
    print("  not an honest one. Read the two together.")

if __name__ == "__main__":
    sys.exit(main())
