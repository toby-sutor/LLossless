#!/usr/bin/env python3
"""The merge-measuring scripts read every source a pair has. Offline; no call.

`tests/measure_merges.py`, `tests/analyse_merges.py` and `tests/rank_arms.py`
each read `source_a.md` and `source_b.md` by name. When `tests/handwritten/`
gained two three-source pairs, `treecreeper` and `mahjongg`, the documented
recipe measured their merges against two of three sources and said nothing:
the third source's segments were missing from the denominator, a merge that
dropped it whole scored no loss, and `mahjongg`'s reference read as a staple.


So each check here builds a three-source directory in a temporary tree and
drives the shipped code, not a copy of it: a merge that drops the third source
must report its segments absent, a staple of all three must read as three runs,
and the ranking must count the third source's loss. A directory with a gap is
refused, including the gap the old code could not see, `source_d.md` without
`source_c.md`.

Run with `python3 tests/test_measure_merges.py`, or collect with pytest.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless import reconcile  # noqa: E402

import analyse_merges  # noqa: E402
import measure_merges  # noqa: E402
import rank_arms  # noqa: E402

failures: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


# Three documents on three subjects, so no sentence of one is near a sentence
# of another and every segment belongs to exactly one source.
SOURCES = {
    "source_a.md": "# Lighthouses\n\nThe tower at Point Arden was lit in 1871.\n"
                   "Its lamp burned whale oil for the first decade.\n"
                   "A keeper and two assistants lived on the island.\n",
    "source_b.md": "# Canals\n\nThe Wexley canal carries barges between two rivers.\n"
                   "Its locks raise boats a total of forty metres.\n"
                   "Traffic peaked in the years before the railway opened.\n",
    "source_c.md": "# Orchards\n\nThe valley grows eleven varieties of apple.\n"
                   "Picking starts in late August and ends in October.\n"
                   "Most of the crop is pressed for cider.\n",
}
STAPLE = "\n".join(SOURCES.values())
WITHOUT_C = SOURCES["source_a.md"] + "\n" + SOURCES["source_b.md"]


def tree(root: Path, name: str, sources: dict[str, str]) -> Path:
    here = root / name
    here.mkdir(parents=True)
    for filename, text in sources.items():
        (here / filename).write_text(text, encoding="utf-8")
    return here


def run(main, argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


def test_every_source_is_read_in_order() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        tree(root, "tri", SOURCES)
        read = analyse_merges.sources_of("tri", root)
        check(tuple(read) == ("source_a.md", "source_b.md", "source_c.md"),
              f"sources_of read {tuple(read)}, not all three in order")


def test_a_dropped_third_source_is_reported_absent() -> None:
    """The silent case: a merge of a and b alone scored as losing nothing."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        tree(root, "tri", SOURCES)
        merges = root / "merges"
        merges.mkdir()
        (merges / "tri-ref-0.md").write_text(WITHOUT_C, encoding="utf-8")

        row = measure_merges.measure(merges / "tri-ref-0.md", root)
        by_name = {c.document.filename: c for c in row["result"].coverages}
        check(set(by_name) == set(SOURCES),
              f"measure() reconciled against {sorted(by_name)}, not all three sources")
        third = by_name.get("source_c.md")
        check(third is not None and third.total > 0 and third.absent == third.total,
              "a merge that drops source_c.md whole must report every one of its "
              f"segments absent; got {third.absent if third else None} of "
              f"{third.total if third else None}")

        # The command, not only the function: the totals line carries the
        # denominator, and it must count the third source's segments.
        expected = reconcile.reconcile(dict(SOURCES), WITHOUT_C).total
        code, out, err = run(measure_merges.main,
                             ["--fixtures-root", str(root), "--merges", str(merges)])
        check(code == 0, f"measure_merges exited {code}: {err.strip()}")
        check(f"/{expected} present" in out,
              f"measure_merges' coverage line is not over all three sources' "
              f"{expected} segments")


def test_a_staple_of_three_reads_as_three_runs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        here = tree(root, "tri", SOURCES)
        (here / "merged.md").write_text(STAPLE, encoding="utf-8")
        merges = root / "merges"
        merges.mkdir()
        (merges / "tri-ref-0.md").write_text(STAPLE, encoding="utf-8")

        row = measure_merges.measure(merges / "tri-ref-0.md", root)
        order = row["result"].order
        check(order.runs == 3 and order.stapled,
              f"a staple of three sources read as runs {order.runs}, "
              f"stapled {order.stapled}")
        check(row["ratio"] >= analyse_merges.CONCATENATION,
              f"the ratio against all three sources stapled is {row['ratio']:.3f}, "
              f"below {analyse_merges.CONCATENATION}")
        check(row["reference_stapled"],
              "a hand merge that is the three sources joined by newlines must read "
              "as a concatenation")


def test_a_gap_is_refused_not_skipped() -> None:
    cases = {
        # The gap the old code could not see: it read a and b and never
        # looked for c, so d was dropped without a word.
        "past_c": ({"source_a.md": "A.\n", "source_b.md": "B.\n", "source_d.md": "D.\n"},
                   ("source_c.md", "source_d.md")),
        "no_b": ({"source_a.md": "A.\n", "source_c.md": "C.\n"},
                 ("source_b.md",)),
        "stray": ({"source_a.md": "A.\n", "source_b.md": "B.\n", "source_x.md": "X.\n"},
                  ("source_x.md",)),
        "one": ({"source_a.md": "A.\n"}, ("at least",)),
    }
    for name, (sources, named) in sorted(cases.items()):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tree(root, name, sources)
            try:
                analyse_merges.sources_of(name, root)
            except Exception as exc:  # noqa: BLE001 - the type is what is checked
                check(isinstance(exc, getattr(analyse_merges, "SourceGap", ())),
                      f"{name}: refused with {type(exc).__name__}, not SourceGap")
                for word in named:
                    check(word in str(exc), f"{name}: the refusal does not name {word}: {exc}")
            else:
                check(False, f"{name}: sources {sorted(sources)} were read, not refused")

            merges = root / "merges"
            merges.mkdir()
            (merges / f"{name}-ref-0.md").write_text("A.\n", encoding="utf-8")
            try:
                code, out, err = run(measure_merges.main,
                                     ["--fixtures-root", str(root), "--merges", str(merges)])
            except Exception as exc:  # noqa: BLE001 - a crash is not a refusal
                code, out, err = None, "", f"{type(exc).__name__}: {exc}"
            check(code == 2 and "refused" in err and out == "",
                  f"{name}: measure_merges exited {code} with {err.strip()!r}; "
                  "a gap must refuse before anything prints")


def test_rank_arms_counts_a_dropped_third_source() -> None:
    """`rank_arms.main` over one recorded cell whose merge drops source_c.md."""
    saved = (rank_arms.CORPUS, rank_arms.PAIRS, rank_arms.RUNS)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        here = tree(root / "corpus", "tri", SOURCES)
        (here / "reference.md").write_text(STAPLE, encoding="utf-8")
        run_dir = root / "run"
        cell = run_dir / "t-1-high-armx"
        cell.mkdir(parents=True)
        (run_dir / "results.json").write_text("[]", encoding="utf-8")
        (cell / "report.json").write_text(json.dumps({"declarations": []}), encoding="utf-8")
        (cell / "merged.md").write_text(WITHOUT_C, encoding="utf-8")
        third = next(c for c in reconcile.reconcile(dict(SOURCES), WITHOUT_C).coverages
                     if c.document.filename == "source_c.md")
        try:
            rank_arms.CORPUS, rank_arms.PAIRS, rank_arms.RUNS = (
                root / "corpus", {"t-1": "tri"}, [run_dir])
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rank_arms.main()
        finally:
            rank_arms.CORPUS, rank_arms.PAIRS, rank_arms.RUNS = saved
        rows = [line.split() for line in out.getvalue().splitlines()
                if line.startswith("armx") and "t-1" in line]
        check(len(rows) == 1, f"rank_arms printed {len(rows)} per-cell rows for the cell")
        if rows:
            silent, lost = int(rows[0][2]), int(rows[0][4])
            check(silent == third.total and lost == third.total,
                  f"rank_arms counts silent {silent} and lost {lost}; the merge "
                  f"dropped all {third.total} of source_c.md's segments")


def test_measure_merges_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_measure_merges_offline" and callable(function):
            try:
                function()
            except Exception as exc:  # noqa: BLE001 - a crashing check is a failing check
                failures.append(f"{name} raised {type(exc).__name__}: {exc}")
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"measure_merges: {checks} checks pass over a three-source directory")
    return 0


if __name__ == "__main__":
    sys.exit(main())
