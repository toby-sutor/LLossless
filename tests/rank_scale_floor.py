#!/usr/bin/env python3
"""The scorecard's `deviations_per_pair` band, anchored to the mechanical-union floor.

The operator accepted, 2026-09-28, the recommendation to anchor the
scorecard's deviations-per-pair band to the mechanical-union floor,
replacing the interim `good: 5, poor: 8` set from
where the shipped catalogue's own rows happened to sit.

The floor is `lineup_figures.baselines`/`_floor`'s union row over the nine
registered pairs (`run_lineup.PAIRS`), base `source_a.md`, scored with
`rank_matrix.cell_figures` and no report -- the same arithmetic
`tests/run_lineup.py figures` already runs, with no model call. This program
only imports and calls those functions; it does not edit them.

The band rule (stated once more, beside `RANK_SCALES` in `app.js`): `poor`
starts AT the floor -- a merge no better than a mechanical union of the two
sources is poor, not fair -- and `good` is at or below half the floor; `fair`
is the gap between. Halving is the only floor-derived split available with
no second reference point, so it is the rule rather than a second
measurement.

The numbers are never typed into `app.js` by hand: this is their `derived_by`.

    python3 tests/rank_scale_floor.py            print the derived good/poor
    python3 tests/rank_scale_floor.py --check    compare with app.js; exit 1
                                                 on any difference
    python3 tests/rank_scale_floor.py --write    write good/poor into app.js
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import figure_rules  # noqa: E402
import lineup_figures  # noqa: E402
import run_lineup  # noqa: E402

APP_JS = ROOT / "src" / "llossless" / "web" / "static" / "app.js"
BASE = "source_a.md"

# Matches the shipped line whether or not it already carries `poorInclusive`,
# so `--check`/`--write` work on both shapes alike.
LINE_RE = re.compile(
    r"  deviations_per_pair: \{ good: [\d.]+, poor: [\d.]+"
    r"(?:, poorInclusive: true)?, ideal: 0 \},\n")


def floor() -> float:
    """The union floor: deviations per pair a mechanical union of each pair's two
    sources leaves silent, over the nine registered pairs. No model call."""
    floors = lineup_figures.baselines(run_lineup.PAIRS, BASE)
    value = lineup_figures._floor(floors["union"], run_lineup.PAIRS)["deviations_per_pair"]
    if value is None:
        raise RuntimeError("lineup_figures._floor gave no deviations_per_pair for the union")
    return value


def derive() -> dict[str, float]:
    """`poor` is the floor; `good` is at or below half the floor; `fair` is the gap
    between -- the one-sentence rule the operator asked for, applied here."""
    poor = floor()
    good = round(poor / 2, figure_rules.RATE_PLACES)
    return {"good": good, "poor": poor}


def render(values: dict[str, float]) -> str:
    return (f"  deviations_per_pair: {{ good: {values['good']}, poor: {values['poor']}, "
            f"poorInclusive: true, ideal: 0 }},\n")


def shipped() -> dict[str, float] | None:
    """The good/poor pair `app.js` currently ships, or None if the line is not found."""
    text = APP_JS.read_text(encoding="utf-8")
    m = re.search(r"deviations_per_pair: \{ good: ([\d.]+), poor: ([\d.]+)", text)
    return {"good": float(m.group(1)), "poor": float(m.group(2))} if m else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="compare with app.js and exit 1 on any difference")
    mode.add_argument("--write", action="store_true",
                      help="write the derived good/poor into app.js")
    args = parser.parse_args(argv)
    values = derive()

    if args.write:
        text = APP_JS.read_text(encoding="utf-8")
        if not LINE_RE.search(text):
            print("rank_scale_floor: the deviations_per_pair line was not found "
                  f"in {APP_JS.relative_to(ROOT)}", file=sys.stderr)
            return 2
        new_text = LINE_RE.sub(lambda _: render(values), text, count=1)
        changed = new_text != text
        if changed:
            APP_JS.write_text(new_text, encoding="utf-8")
        print(f"{'wrote' if changed else 'unchanged:'} {APP_JS.relative_to(ROOT)} "
              f"good={values['good']} poor={values['poor']}")
        return 0

    if not args.check:
        print(f"good={values['good']} poor={values['poor']}")
        return 0

    got = shipped()
    if got != values:
        print(f"  DIFFERS  app.js has {got}, the union floor derives {values}")
        print("rank_scale_floor: 1 difference(s)")
        return 1
    print(f"rank_scale_floor: clean -- good={values['good']} poor={values['poor']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
