#!/usr/bin/env python3
"""The planted-error scorers' keys are derived, and every control holds. Offline; no call.

`tests/score_planted.py` scores merges of the two `tests/handwritten`
pairs with planted errors, `voyager` and `bip39`, against a key computed by
diffing each pair's `reference.md` with its sources, and scores `mahjongg`,
which has none, for false corrections. `score_voyager.py` is kept as that
module with the pair fixed to voyager. The file keeps its name because
`tests/run_all.py` names it.

A key nobody typed still needs the checks a typed one never had, per pair:

- scoring `reference.md` itself must find **every** error fixed;
- scoring the plain concatenation of the sources must find **none** fixed
  (and every one kept).

The counting rule is one error per changed unit: a date or
timestamp is one, a number with its unit is one, anything else is a word. The
grouping is pinned on the cases the operator ruled on. The mahjongg control
must report nothing for its own reference and for a merge that only drops or
respaces, and must report a changed number and a declared correction.

By design, the style of a merge moves nothing, both ways: each
reference hard-wrapped, with its numbers in bold or in NFD, still scores
every error fixed, and each concatenation hard-wrapped still scores none.
Deleting a planted insertion with the word before it ("and Bianca II") is
not a fix. The control counts a change the merge declared once, not twice.

Run with `python3 tests/test_score_voyager.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "tests"
SCRIPT = SCRIPTS / "score_planted.py"
SHIM = SCRIPTS / "score_voyager.py"
sys.path.insert(0, str(SCRIPTS))

import socket_guard  # noqa: E402

socket_guard.install()

import score_planted as sp  # noqa: E402
import score_voyager as sv  # noqa: E402

PAIRS = ROOT / "tests" / "handwritten"
# Pinned, not derived: the rule's output on the operator's files as they are.
# If a pair or the counting rule changes, this fails and says by how much,
# which is the point -- a key that drifts silently is a typed key again.
# The one-per-word rule gave 47 and 15.
EXPECTED = {"voyager": (44, 37, 47), "bip39": (14, 14, 15)}

failures: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


def concatenation(pair: str) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in sp.sources(PAIRS / pair))


def counts(outcomes: list[dict]) -> dict[str, int]:
    return {k: sum(1 for o in outcomes if o["outcome"] == k) for k in ("fixed", "kept", "other")}


def test_the_key_counts_what_the_diff_finds() -> None:
    for pair, (total, spans, word_rule) in EXPECTED.items():
        key = sp.planted(pair)
        check(len(key.errors) == total and key.spans == spans
              and key.word_rule_total == word_rule,
              f"{pair}: the derived key has {len(key.errors)} errors in {key.spans} spans "
              f"({key.word_rule_total} by word), pinned at {total} in {spans} ({word_rule})")
        reference = (PAIRS / pair / "reference.md").read_text(encoding="utf-8")
        joined = sp.planted_text(PAIRS / pair)
        for e in key.errors:
            check(e.original in reference and e.planted in joined,
                  f"{pair} error {e.number}: {e.original!r} / {e.planted!r} is not text of the pair")


def test_the_units_are_the_operators() -> None:
    """The rulings of 2026-09-25, each pinned on the error it was made about."""
    key = sp.planted("voyager")
    by_original = {e.original.rstrip(".,"): e for e in key.errors}
    expected = {
        "Nov. 4, 1985": ("date", 3),                  # a date is one error
        "17:59 UT Jan. 24, 1986": ("date", 2),        # a timestamp, time zone and all
        "5.5 hours": ("quantity", 2),                 # number and unit together
        "450 miles per hour": ("quantity", 1),        # one span, two quantities
        "(724 kilometers per hour)": ("quantity", 1),
        "50,640 miles": ("quantity", 1),              # the unit swap is two quantities
        "(81,500 kilometers)": ("quantity", 1),
        "4.5 years": ("quantity", 1),                 # a format change is an error
        "2's": ("word", 1),                           # "Voyager 2's long-range" is two
        "long-range": ("word", 1),
    }
    for original, (kind, pieces) in expected.items():
        e = by_original.get(original)
        check(e is not None and e.kind == kind and len(e.pieces) == pieces,
              f"{original!r} should be one {kind} error of {pieces} piece(s): "
              f"{None if e is None else (e.kind, len(e.pieces), e.planted)}")
    names = [e for e in key.errors if e.original.rstrip(",") in
             ("Puck", "Portia", "Juliet", "Cressida", "Rosalind", "Cordelia")]
    check(len(names) == 6 and all(len(e.pieces) == 1 for e in names),
          f"each altered moon name is one error: {[e.original for e in names]}")
    split = [e for e in key.errors if any(p.part for p in e.pieces)]
    check(len(split) == 2 and {e.pieces[0].span for e in split} == {24},
          f"only the speed span is split, into its two quantities: "
          f"{[(e.original, e.pieces[0].span) for e in split]}")
    bip = {e.original.rstrip(".,"): e for e in sp.planted("bip39").errors}
    check(bip.get("128-256 bits") is not None and len(bip["128-256 bits"].pieces) == 2,
          "bip39's range and its unit are one quantity")


def test_the_join_drops_the_repeated_title_and_no_heading_is_an_error() -> None:
    key = sp.planted("voyager")
    joined = sp.planted_text(PAIRS / "voyager")
    check(joined.count("# Voyager 2 at Uranus") == 1,
          "the joined sources should carry the shared title once, as the reference does")
    check(not any("#" in e.planted or "Voyager 2 at Uranus" in e.planted for e in key.errors),
          "a heading was counted as a planted error: the join artefact is back")
    check(sp.planted_text(PAIRS / "bip39").count("# BIP: 39") == 1,
          "a second source with no title of its own is joined whole")


def test_the_key_moves_with_the_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        pair = Path(tmp)
        for name in ("reference.md", "source_a.md", "source_b.md"):
            shutil.copy(PAIRS / "voyager" / name, pair / name)
        b = (pair / "source_b.md").read_text(encoding="utf-8")
        (pair / "source_b.md").write_text(b.replace("Desdemona", "Desdemono"), encoding="utf-8")
        moved = sp.planted(pair)
        total = EXPECTED["voyager"][0]
        check(len(moved.errors) == total + 1,
              f"one more planted change gave {len(moved.errors)} errors, not {total + 1}")
        check(any(e.original == "Desdemona," and e.planted == "Desdemono," for e in moved.errors),
              "the extra planted change is not in the key derived from the changed pair")


def test_the_reference_scores_every_error_fixed() -> None:
    for pair, (total, _, _) in EXPECTED.items():
        reference = (PAIRS / pair / "reference.md").read_text(encoding="utf-8")
        outcomes = sp.score_text(reference, sp.planted(pair))
        wrong = [(o["error"], o["outcome"]) for o in outcomes if o["outcome"] != "fixed"]
        check(len(outcomes) == total and not wrong,
              f"{pair}: reference.md should score {total}/{total} fixed; not fixed: {wrong}")


def test_the_concatenated_sources_score_none_fixed() -> None:
    for pair in EXPECTED:
        outcomes = sp.score_text(concatenation(pair), sp.planted(pair))
        fixed = [o["error"] for o in outcomes if o["outcome"] == "fixed"]
        not_kept = [(o["error"], o["outcome"]) for o in outcomes if o["outcome"] != "kept"]
        check(not fixed, f"{pair}: the unmerged sources scored errors {fixed} fixed")
        check(not not_kept, f"{pair}: the unmerged sources should keep every error; "
                            f"not kept: {not_kept}")


def test_a_unit_is_fixed_only_whole() -> None:
    """A date with its year still wrong is not a fixed date, and not a kept one."""
    key = sp.planted("voyager")
    date = next(e for e in key.errors if e.original.startswith("Nov. 4, 1985"))
    reference = (PAIRS / "voyager" / "reference.md").read_text(encoding="utf-8")
    half = reference.replace("Nov. 4, 1985", "Nov. 4, 1987")
    check(half != reference, "the probe's anchor has moved")
    outcome = next(o for o in sp.score_text(half, key) if o["error"] == date.number)
    check(outcome["outcome"] == "other" and "kept" in outcome["found"],
          f"a date fixed in part must be `other`, saying what was kept: {outcome}")
    speed = reference.replace("450 miles per hour", "450 km/h")
    got = {o["error"]: o["outcome"] for o in sp.score_text(speed, key)}
    first = next(e for e in key.errors if e.original == "450 miles per hour")
    second = next(e for e in key.errors if e.original == "(724 kilometers per hour)")
    check(got[first.number] == "kept" and got[second.number] == "fixed",
          f"the two quantities of one span are scored apart: {got[first.number]}, "
          f"{got[second.number]}")


def test_a_short_heading_is_not_found_in_a_long_sentence() -> None:
    """bip39's "## Generating the memonic" shares its three words with a sentence
    of the Abstract. Taking that sentence as the heading's place scored the
    plain sources `other` there, both wordings found; the region's fallback now
    needs a third of the candidate's own words as well."""
    key = sp.planted("bip39")
    heading = next(e for e in key.errors if e.planted == "memonic")
    outcome = next(o for o in sp.score_text(concatenation("bip39"), key)
                   if o["error"] == heading.number)
    check(outcome["outcome"] == "kept", f"the unfixed heading must read kept: {outcome}")


def test_the_declared_column_is_not_the_score() -> None:
    """A run is scored on its text; what it claims is a second column."""
    total = EXPECTED["voyager"][0]
    claims = {"merged_document": concatenation("voyager"),
              "additions": [{"statement": "Voyager 2 had fulfilled its goals",
                             "corrects": "Voyager 3 had fulfilled", "reason": "no Voyager 3"}]}
    silent = {"merged_document": (PAIRS / "voyager" / "reference.md").read_text(encoding="utf-8"),
              "additions": []}
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "claims.json").write_text(json.dumps(claims), encoding="utf-8")
        (Path(tmp) / "silent.json").write_text("Here is the merge.\n```json\n"
                                               + json.dumps(silent) + "\n```\n", encoding="utf-8")
        a = sv.score(Path(tmp) / "claims.json")
        b = sv.score(Path(tmp) / "silent.json")
    check(a["fixed"] == 0 and a["declared"] == 1 and a["declared_not_fixed"] == [1],
          f"a declared fix the text does not carry must score 0 fixed, 1 declared: {a['fixed']}, "
          f"{a['declared']}, {a['declared_not_fixed']}")
    check(b["fixed"] == total and b["declared"] == 0,
          f"a silent, correct merge must score {total} fixed, 0 declared: "
          f"{b['fixed']}, {b['declared']}")


def test_the_command_scores_a_file() -> None:
    """The command, not only the function: the controls through `main`'s path,
    for each pair, and through the voyager shim."""
    for pair, (total, _, _) in EXPECTED.items():
        for script, argv in ((SCRIPT, ["--pair", pair]), (SHIM, [])):
            if script == SHIM and pair != "voyager":
                continue
            with tempfile.TemporaryDirectory() as tmp:
                concat = Path(tmp) / "concat.md"
                concat.write_text(concatenation(pair), encoding="utf-8")
                out = subprocess.run([sys.executable, str(script), *argv,
                                      str(PAIRS / pair / "reference.md"), str(concat)],
                                     capture_output=True, text=True, timeout=120)
            lines = [line.split() for line in out.stdout.splitlines()
                     if line.strip().startswith("fixed ")]
            where = f"{script.name} {pair}"
            check(out.returncode == 0 and len(lines) == 2,
                  f"{where}: did not score two files: exit {out.returncode}, "
                  f"{out.stderr.strip()[-200:]}")
            if len(lines) == 2:
                check(lines[0][1] == f"{total}/{total}" and lines[1][1] == f"0/{total}",
                      f"{where}: printed fixed {lines[0][1]} for the reference and "
                      f"{lines[1][1]} for the sources, not {total}/{total} and 0/{total}")


def control(text: str, records: list[dict] | None = None) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "merge.json"
        path.write_text(json.dumps({"merged_document": text, "additions": records or []}),
                        encoding="utf-8")
        return sp.false_corrections(path, "mahjongg")


def test_the_false_correction_control() -> None:
    """mahjongg has nothing to correct, so every correction is false.

    Must not fire: its own reference, and a merge that only drops a
    parenthetical and fixes a missing space (the operator's own merge did
    both). Must fire: one number changed, and one declared correction.
    """
    reference = (PAIRS / "mahjongg" / "reference.md").read_text(encoding="utf-8")
    clean = control(reference)
    check(clean["false_corrections"] == 0 and clean["verbatim"] == clean["sentences"],
          f"the reference must hold no false correction: {clean['false_corrections']}, "
          f"{clean['verbatim']}/{clean['sentences']}")
    anchor = "Um die einzelnen Spiele und Runden mitzuzählen, wird eine kleine Dose (Mingg)"
    check(anchor in reference and "Ersatzziegel (siehe unten)" in reference,
          "the probes' anchors have moved")
    tidied = (reference.replace("(Mingg)verwendet", "(Mingg) verwendet")
              .replace("Ersatzziegel (siehe unten) genommen", "Ersatzziegel genommen"))
    tidy = control(tidied)
    check(tidy["false_corrections"] == 0 and len(tidy["dropped"]) == 1,
          f"a drop and a respacing are not corrections: {tidy['false_corrections']}, "
          f"dropped {len(tidy['dropped'])}")
    number = next(n for n in ("144", "136") if f"{n} " in reference)
    changed = control(reference.replace(f"{number} ", "150 ", 1))
    check(changed["false_corrections"] == 1 and changed["changed"][0]["numeric"],
          f"a changed number is one false correction, marked numeric: "
          f"{changed['false_corrections']}, {changed['changed'][:1]}")
    declared = control(reference, [{"statement": "x", "corrects": "y", "basis": "citation"}])
    check(declared["false_corrections"] == 1 and len(declared["declared"]) == 1,
          f"a declared correction is a false correction here: {declared['false_corrections']}")


def hard_wrap(text: str, width: int) -> str:
    """Every paragraph line wrapped at `width`, headings and blank lines as they were."""
    out = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith(("#", "|", "```")):
            out.append(line)
            continue
        out += textwrap.wrap(line, width=width) or [""]
    return "\n".join(out) + "\n"


def bold_numbers(text: str) -> str:
    return re.sub(r"(?<![\w*])(\d[\d.,:]*\d|\d)(?![\w*])", r"**\1**", text)


STYLES = {"wrapped at 80": lambda t: hard_wrap(t, 80), "wrapped at 60": lambda t: hard_wrap(t, 60),
          "numbers in bold": bold_numbers,
          "NFD": lambda t: unicodedata.normalize("NFD", t)}


def test_style_moves_nothing_either_way() -> None:
    """Must not fire on style: every reference still all fixed;
    must still fire on the errors: every concatenation still none fixed."""
    for pair, (total, _, _) in EXPECTED.items():
        key = sp.planted(pair)
        reference = (PAIRS / pair / "reference.md").read_text(encoding="utf-8")
        for name, style in STYLES.items():
            fixed = sum(o["outcome"] == "fixed" for o in sp.score_text(style(reference), key))
            check(fixed == total, f"{pair}: reference.md {name} scored {fixed}/{total} fixed")
            kept = [o["error"] for o in sp.score_text(style(concatenation(pair)), key)
                    if o["outcome"] == "fixed"]
            check(not kept, f"{pair}: the sources {name} scored errors {kept} fixed")
    key = sp.planted("voyager")
    reference = (PAIRS / "voyager" / "reference.md").read_text(encoding="utf-8")
    check("2's" in reference, "the emphasis probe's anchor has moved")
    fixed = sum(o["outcome"] == "fixed"
                for o in sp.score_text(reference.replace("2's", "**2**'s"), key))
    check(fixed == EXPECTED["voyager"][0],
          f"emphasis inside a token (**2**'s) moved voyager to {fixed}")


def test_deleting_an_insertion_is_not_a_fix() -> None:
    """Voyager's planted "Bianca II": the fix reads fixed, a merge
    that deletes "and Bianca II" drops a moon and reads other."""
    key = sp.planted("voyager")
    insertion = next(e for e in key.errors if e.kind == "insertion")
    planted = key.planted
    check("Ophelia, and Bianca II" in planted, "the insertion probe's anchor has moved")
    outcome = {label: next(o for o in sp.score_text(text, key)
                           if o["error"] == insertion.number)["outcome"]
               for label, text in (("fix", planted.replace("Bianca II", "Bianca", 1)),
                                   ("delete", planted.replace(", and Bianca II", "", 1)),
                                   ("as planted", planted))}
    check(outcome == {"fix": "fixed", "delete": "other", "as planted": "kept"},
          f"insertion error {insertion.number}: {outcome}")


def test_a_declared_change_is_one_false_correction() -> None:
    """A changed number is one false correction whether or not the
    merge declared it; a declaration of a different change is a second one."""
    reference = (PAIRS / "mahjongg" / "reference.md").read_text(encoding="utf-8")
    number = next(n for n in ("144", "136") if f"{n} " in reference)
    changed_text = reference.replace(f"{number} ", "150 ", 1)
    silent = control(changed_text)
    named = control(changed_text, [{"statement": "150", "corrects": number,
                                    "basis": "knowledge"}])
    other = control(changed_text, [{"statement": "x", "corrects": "Mingg",
                                    "basis": "knowledge"}])
    check(silent["false_corrections"] == 1 and named["false_corrections"] == 1
          and named["false_corrections_changed"] == 1
          and named["false_corrections_declared"] == 1
          and named["declared_naming_a_change"] == 1,
          f"a declared change must count once: silent {silent['false_corrections']}, "
          f"declared {named['false_corrections']} ({named['false_corrections_changed']} changed, "
          f"{named['false_corrections_declared']} declared)")
    check(other["false_corrections"] == 2 and other["declared_naming_a_change"] == 0,
          f"a declaration of something else is a second correction: {other['false_corrections']}")


def test_score_voyager_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_score_voyager_offline" and callable(function):
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
    keys = ", ".join(f"{pair} {total}" for pair, (total, _, _) in EXPECTED.items())
    print(f"score_planted: {checks} checks pass; the keys are derived by diff ({keys} "
          f"errors), each reference scores all fixed and its sources none, and the "
          f"mahjongg control fires on a changed number and a declared correction only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
