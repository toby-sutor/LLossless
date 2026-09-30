#!/usr/bin/env python3
"""The number-format check (`llossless.numerals`), seeded both ways.

The check flags a numeral a merge drifted from its source value, or one
written with decimal punctuation that disagrees with the document's own
language. This module holds it to that rule in three ways:

  1. **must fire**: `voyager`'s four planted format errors, a tie document's
     ambiguous numerals, a merge that rewrites a settled source value, and a
     document whose numerals all go against its language -- `voyager`'s
     `source_a.md` with its one decimal point ("6.4") taken out, a short
     English text written with decimal commas, and a German one written with
     decimal points;
  2. **must not fire**: `voyager`'s `reference.md`, a German document written
     with decimal commas, the German documents of `gold_de_en` and
     `mahjongg`, decimal commas in a text of unknown or mixed language, years,
     times, versions, dates and addresses, and every document in
     `tests/fixtures/`, `tests/pairs/`, `tests/handwritten/` and the recorded
     merge cassettes -- where the only firings are the planted ones, pinned by
     name;
  3. **seeded**: each rule the probes depend on is broken in a copy of the
     *shipped* module's source, and at least one probe must go red on each.
     A probe that stays green with its rule removed tests nothing.

Offline, no model, no network. Run with `python3 tests/test_numerals.py`.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless import numerals  # noqa: E402

SHIPPED = ROOT / "src" / "llossless" / "numerals.py"
VOYAGER = ROOT / "tests" / "handwritten" / "voyager"
CORPORA = ("fixtures", "pairs", "handwritten")
MERGED_NAMES = ("merged.md", "ideal.md", "reference.md")

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# Probe documents. Inline rather than on disk: a file under tests/fixtures/
# would enter three registered globs (tests/test_handwritten.py's note).
# --------------------------------------------------------------------------

GERMAN = """# Messbericht

Die Anlage wurde im Jahr 2024 in Betrieb genommen und läuft seitdem ohne \
Unterbrechung. Der Durchfluss liegt bei 4,5 Litern pro Sekunde, und der Druck \
beträgt 2,75 bar. Das Becken fasst 12.500 Liter, die Leitung ist 1.250 Meter \
lang. Insgesamt wurden 1.000.000 Liter gefördert, das sind 12.345,67 Euro an \
Kosten. Die Wartung beginnt um 15.30 Uhr.
"""

# Everything the check must read past, in a German document, where any of
# them read as a decimal point would be written in the other convention.
GERMAN_NOT_NUMBERS = """# Hinweise zur Installation

Die Steuerung läuft mit Version 3.2 der Software und mit Python 3.12, das \
Protokoll ist HTTP/1.1 und die Adresse ist 192.168.1.1 für den Zugang. Die \
Freigabe 2.4.1 wurde am 24.09.2026 um 17:59 eingespielt, siehe Abschnitt 4.2 \
und Seite 3.5 der Anleitung. Der Wert `3.5` steht in der Datei, und der Link \
<https://example.com/v/3.5> zeigt auf die Quelle. Die Kosten liegen bei 4,5 \
Euro pro Stück.

```python
ratio = 3.5
```
"""

ENGLISH_NOT_NUMBERS = """# Release notes

The update shipped in 1986 and again in 2026, at 17:59 UT on each day, and \
the firmware moved from v1.2 to 2.4.1 while it kept kernel 5.10 in place. The \
meeting starts at 3.30 pm and the report is in section 4.2. The route is \
4.5 miles, and the budget is 1,250 dollars.
"""

# No stop word in either language, one vote each way: nothing can decide, so
# both ambiguous numerals are questions.
TIE = """| item | value |
|---|---|
| alpha | 4,5 |
| beta | 3.2 |
| gamma | 17.560 |
| delta | 1,250 |
"""

# A document whose numerals outvote its language: every decimal written the
# other way, and nothing written the language's way to split the vote.
ENGLISH_COMMAS = ("The pump moves 4,5 litres per second at a pressure of 2,75 "
                  "bar, and the tank holds 12,5 cubic metres. It was installed "
                  "in 2024 and has run without a stop since then.\n")
GERMAN_POINTS = ("Die Anlage läuft seit dem Jahr 2024 und ist nicht ausgefallen. "
                 "Der Durchfluss liegt bei 4.5 Litern und der Druck bei 2.75 "
                 "bar, und das ist für die Anlage auch genug.\n")
# The same decimal commas where the language is not known: no stop word at
# all, and a mix of the two languages, 14 English stop words to 9 German, too
# even for either to decide. Nothing is contradicted.
UNKNOWN_COMMAS = "| item | value |\n|---|---|\n| alpha | 4,5 |\n| beta | 2,5 |\n"
MIXED_COMMAS = ("The pump is on the roof and it runs for the whole day, and the "
                "tank is next to it. Die Pumpe ist auf dem Dach und läuft den "
                "ganzen Tag. It moves 4,5 litres, und der Druck ist 2,75 bar.\n")
GERMAN_CORPUS = (("gold_de_en", "source_a.md"), ("mahjongg", "source_a.md"),
                 ("mahjongg", "source_b.md"), ("mahjongg", "source_c.md"),
                 ("mahjongg", "reference.md"))

SETTLED_SOURCE = ("The depot lies 17,560 miles from the base, and the first "
                  "leg of the trip takes 4.5 hours by road.\n")
SETTLED_MERGE = ("The depot lies 17.560 miles from the base, and the first "
                 "leg of the trip takes 4.5 hours by road.\n")
GERMAN_SOURCE = ("Die Strecke von der Basis zum Depot ist 17.560 km lang, "
                 "und die Fahrt dauert 4,5 Stunden mit dem Wagen.\n")
ENGLISH_MERGE = ("The route from the base to the depot is 17.560 km long, and "
                 "the drive takes 4.5 hours by car.\n")
# One source value, a second numeral with the same digits in another role:
# "is" is shared and names nothing, so the two must not be paired.
SAME_DIGITS_SOURCE = "The fee for the permit is 1,250 dollars and it is paid once.\n"
SAME_DIGITS_MERGE = ("The fee for the permit is 1,250 dollars and it is paid "
                     "once. The plate is 1.250 millimetres thick and 4.5 wide.\n")


def voyager() -> tuple[dict[str, str], str]:
    sources = {name: (VOYAGER / name).read_text(encoding="utf-8")
               for name in ("source_a.md", "source_b.md")}
    return sources, (VOYAGER / "reference.md").read_text(encoding="utf-8")


def voyager_without_its_point() -> str:
    """`voyager`'s `source_a.md` with "6.4 days" written in words.

    Its one unambiguous decimal point is what splits its vote and lets the
    language decide; without it the two planted decimal commas are unanimous.
    """
    text = (VOYAGER / "source_a.md").read_text(encoding="utf-8")
    if text.count("6.4 days") != 1:
        raise AssertionError("voyager's source_a.md no longer carries '6.4 days' "
                             "once; the must-fire probe would go vacuous")
    return text.replace("6.4 days", "six days")


def fired(result, kind: str | None = None) -> list[str]:
    """The numerals the findings name, in order, optionally of one kind."""
    return [f.detail.split("'")[1] for f in result.findings
            if kind is None or f.kind == kind]


# --------------------------------------------------------------------------
# The probes, as functions of a module, so the seeded copies run them too
# --------------------------------------------------------------------------

def probes(module) -> list[str]:
    """Every probe's failure message against `module`. Empty is pass."""
    problems: list[str] = []

    def expect(condition: bool, message: str) -> None:
        if not condition:
            problems.append(message)

    sources, reference = voyager()
    planted = module.check(sources, None, "merged.md")
    expect(fired(planted) == ["4,5", "2,5", "17.560", "28.260"],
           f"voyager's sources must fire on the four planted format errors "
           f"and nothing else: {fired(planted)}")
    expect(fired(planted, module.OTHER_CONVENTION) == ["4,5", "2,5"]
           and fired(planted, module.READABLE_TWO_WAYS) == ["17.560", "28.260"],
           f"4,5 and 2,5 are the other convention, 17.560 and 28.260 readable "
           f"two ways: {[(f.kind, f.detail[:30]) for f in planted.findings]}")
    by_name = {c.document: c for c in planted.conventions}
    expect(by_name["source_a.md"].convention == module.POINT
           and by_name["source_a.md"].decided_by == module.BY_LANGUAGE,
           "voyager source_a votes 2 comma to 1 point; its language must decide")

    alone = module.check({"reference.md": reference}, None, "merged.md")
    expect(not alone.findings,
           f"voyager's reference.md is clean: {fired(alone)}")
    as_merge = module.check(sources, reference, "merged.md")
    merge_rows = [f for f in as_merge.findings if f.segment.startswith("m")]
    expect([f.kind for f in merge_rows] == [module.READING_RESOLVED] * 2
           and not as_merge.faults,
           f"the reference merge settles two flagged source values and is no "
           f"fault: {[(f.kind, f.detail[:40]) for f in merge_rows]}")

    german = module.check({"source_a.md": GERMAN}, None, "merged.md")
    expect(not german.findings and german.conventions[0].convention == module.COMMA
           and german.conventions[0].decided_by == module.BY_VOTES,
           f"a German decimal-comma document is clean and decided by its "
           f"numerals: {fired(german)} {german.conventions[0].as_dict()}")

    for name, text in (("German", GERMAN_NOT_NUMBERS),
                       ("English", ENGLISH_NOT_NUMBERS)):
        result = module.check({"source_a.md": text}, None, "merged.md")
        expect(not result.findings,
               f"years, times, versions, dates and addresses never fire "
               f"({name}): {fired(result)}")
        texts = [n.text for c in result.conventions for n in c.numerals]
        expect(not any(t in texts for t in ("3.2", "3.12", "1.1", "2.4.1",
                                            "5.10", "3.30", "4.2", "3.5",
                                            "15.30")),
               f"no designation, time or version is read as a numeral "
               f"({name}): {texts}")

    tie = module.check({"source_a.md": TIE}, None, "merged.md")
    expect(tie.conventions[0].decided_by == module.UNDECIDED
           and fired(tie) == ["17.560", "1,250"]
           and all(f.kind == module.READABLE_TWO_WAYS for f in tie.findings),
           f"a tie with no language flags both ambiguous numerals and nothing "
           f"else: {fired(tie)} {tie.conventions[0].as_dict()}")

    changed = module.check({"source_a.md": SETTLED_SOURCE}, SETTLED_MERGE,
                           "merged.md")
    expect([f.kind for f in changed.faults] == [module.READING_CHANGED]
           and "1,000 times smaller" in changed.faults[0].detail,
           f"a settled source value rewritten 1,000 times smaller is a fault: "
           f"{[(f.kind, f.detail) for f in changed.findings]}")
    expect(len(changed.findings) == 1,
           f"the rewritten numeral is named once, as the fault: "
           f"{[f.kind for f in changed.findings]}")

    crossed = module.check({"source_a.md": GERMAN_SOURCE}, ENGLISH_MERGE,
                           "merged.md")
    expect([f.kind for f in crossed.faults] == [module.READING_CHANGED],
           f"German 17.560 km merged into English as 17.560 km is the same "
           f"characters and a thousandth of the value: "
           f"{[(f.kind, f.detail) for f in crossed.findings]}")

    same = module.check({"source_a.md": SAME_DIGITS_SOURCE}, SAME_DIGITS_MERGE,
                        "merged.md")
    expect(not same.faults,
           f"a shared function word pairs nothing: "
           f"{[(f.kind, f.detail) for f in same.faults]}")

    # Against the language: must fire, once per document, naming every
    # numeral that outvoted it, and never a fault.
    for label, text, named in (
            ("voyager's source_a.md without 6.4", voyager_without_its_point(),
             ("'4,5' (line 3)", "'2,5' (line 9)")),
            ("an English text with decimal commas", ENGLISH_COMMAS,
             ("'4,5' (line 1)", "'2,75' (line 1)", "'12,5' (line 1)")),
            ("a German text with decimal points", GERMAN_POINTS,
             ("'4.5' (line 1)", "'2.75' (line 1)"))):
        result = module.check({"source_a.md": text}, None, "merged.md")
        rows = [f for f in result.findings if f.kind == module.AGAINST_LANGUAGE]
        expect(len(rows) == 1 and all(n in rows[0].detail for n in named),
               f"{label}: one row against its language, naming {named}: "
               f"{[(f.kind, f.detail) for f in result.findings]}")
        expect(not result.faults,
               f"{label}: a document against its language is a warning, never "
               f"a fault: {[f.kind for f in result.faults]}")
        expect(not fired(result, module.OTHER_CONVENTION),
               f"{label}: the numerals keep the decision, so none of them is "
               f"in the other convention: {fired(result)}")
    stripped = module.check({"source_a.md": voyager_without_its_point()}, None,
                            "merged.md")
    expect([f.kind for f in stripped.findings]
           == [module.AGAINST_LANGUAGE] + [module.READABLE_TWO_WAYS] * 2
           and fired(stripped, module.READABLE_TWO_WAYS) == ["50,640", "81,500"],
           f"voyager's source_a.md without 6.4: its row, then its two English "
           f"thousands read under the decimal comma the numerals decided: "
           f"{[(f.kind, f.detail[:40]) for f in stripped.findings]}")
    english = "\n".join(f.detail for f in module.check(
        {"source_a.md": ENGLISH_COMMAS}, None, "merged.md").findings)
    expect("English writes a decimal point" in english
           and "an English reader takes '4,5' for 45" in english,
           f"the row says what the language writes and how its reader "
           f"misreads the first numeral: {english}")

    # Against the language: must not fire where the numerals agree with it,
    # where the language is unknown or mixed, or where a split vote let the
    # language decide. The two unknown texts are decimal-comma documents by
    # their votes, so only the language stands between them and a row.
    for label, text in (("no language", UNKNOWN_COMMAS),
                        ("mixed language", MIXED_COMMAS)):
        decided = module.check({"source_a.md": text}, None,
                               "merged.md").conventions[0]
        expect(decided.convention == module.COMMA and not decided.language
               and (label == "no language" or
                    decided.english_words and decided.german_words),
               f"the {label} probe must be a decimal-comma document whose "
               f"language is unknown, or it tests nothing: {decided.as_dict()}")
    for label, documents in (
            ("voyager's reference.md", {"reference.md": reference}),
            ("a German text with decimal commas", {"source_a.md": GERMAN}),
            ("a text with no language", {"source_a.md": UNKNOWN_COMMAS}),
            ("a text of mixed language", {"source_a.md": MIXED_COMMAS}),
            ("voyager's sources, 6.4 kept", sources),
            *((f"{pair}/{name}",
               {name: (ROOT / "tests" / "handwritten" / pair / name).read_text(
                   encoding="utf-8")})
              for pair, name in GERMAN_CORPUS)):
        result = module.check(documents, None, "merged.md")
        expect(not fired(result, module.AGAINST_LANGUAGE),
               f"{label} is not against its language: "
               f"{[(f.kind, f.detail) for f in result.findings]} "
               f"{[c.as_dict() for c in result.conventions]}")
    return problems


def test_the_probes_hold_on_the_shipped_module() -> None:
    for problem in probes(numerals):
        check(False, problem)


def test_shapes() -> None:
    """The rule's first clause, token by token."""
    cases = {
        "4,5": ("decimal", "comma"), "0,25": ("decimal", "comma"),
        "3.14": ("decimal", "point"), "3,1415": ("decimal", "comma"),
        "0,560": ("decimal", "comma"), "1234.567": ("decimal", "point"),
        "1,000,000": ("grouped", "point"), "1.000.000": ("grouped", "comma"),
        "12.345,67": ("grouped", "comma"), "12,345.67": ("grouped", "point"),
        "17.560": ("ambiguous", ""), "50,640": ("ambiguous", ""),
        "1986": ("", ""), "2.4.1": ("malformed", ""),
        "24.09.2026": ("malformed", ""), "1,2,3": ("malformed", ""),
        "1.2,3": ("malformed", ""),
    }
    for token, expected in cases.items():
        got = numerals._shape(token)
        check(got == expected, f"{token!r} is {expected}, got {got}")
    check(numerals.read("4,5", numerals.POINT) == 45
          and numerals.read("4,5", numerals.COMMA) == numerals.Decimal("4.5")
          and numerals.read("17.560", numerals.COMMA) == 17560
          and numerals.read("1.000.000", numerals.POINT) is None,
          "read() is the careless reader of each convention")


def test_language() -> None:
    english = "The report is on the desk and it has been read by the team."
    german = "Der Bericht liegt auf dem Tisch und er ist von dem Team gelesen worden."
    check(numerals.language(english)[0] == "en", "English is recognised")
    check(numerals.language(german)[0] == "de", "German is recognised")
    check(numerals.language(english + " " + german)[0] == "",
          "an even mix of the two is unknown")
    check(numerals.language("Le rapport est sur la table.")[0] == "",
          "a third language is unknown, never guessed")


def test_every_corpus_file() -> None:
    """Every document in the three corpora; the planted pair fires, nothing else.

    Measured 2026-09-25 over 130 documents: 16 fixtures, 9 pairs and 19
    hand-written pairs, sources and merges both:
    six findings, all in `voyager` -- the four planted format errors in the
    sources, and the two its reference resolves. Pinned by name, so a new
    firing is read rather than absorbed.
    """
    seen = 0
    firing: dict[str, list[tuple[str, str]]] = {}
    for corpus in CORPORA:
        for folder in sorted(p for p in (ROOT / "tests" / corpus).iterdir()
                             if p.is_dir()):
            sources = {p.name: p.read_text(encoding="utf-8")
                       for p in sorted(folder.glob("source_*.md"))}
            merged_path = next((folder / n for n in MERGED_NAMES
                                if (folder / n).is_file()), None)
            merged = (merged_path.read_text(encoding="utf-8")
                      if merged_path else None)
            result = numerals.check(sources, merged, "merged.md")
            seen += len(sources) + (merged is not None)
            if result.findings:
                firing[f"{corpus}/{folder.name}"] = [
                    (f.kind, f.detail.split("'")[1]) for f in result.findings]
    check(seen == 130, f"130 corpus documents were measured; now {seen}, so "
                       f"re-measure the firings rather than update this blind")
    check(firing == {"handwritten/voyager": [
        ("other_convention", "4,5"), ("other_convention", "2,5"),
        ("readable_two_ways", "17.560"), ("readable_two_ways", "28.260"),
        ("reading_resolved", "17.560"), ("reading_resolved", "28.260")]},
        f"only voyager fires, on its planted numerals: {firing}")


def test_every_recorded_merge() -> None:
    """The 115 merged documents the cassettes hold: none fires.

    Sources rebuilt from each request by `test_reconcile._recorded_merges`,
    the same reader used to measure its own must-not-fire corpus. 151 and 82
    numerals until the 27B import replaced `m7/`'s qwen3:8b merges.
    """
    import test_reconcile

    corpus = test_reconcile._recorded_merges()
    check(len(corpus) == 115, f"115 recorded merges; now {len(corpus)}, so "
                              f"re-measure rather than update this blind")
    counted = 0
    for label, sources, merged in corpus:
        result = numerals.check(sources, merged, "merged.md")
        counted += sum(len(c.numerals) for c in result.conventions)
        check(not result.findings,
              f"{label} fired: {[(f.kind, f.detail) for f in result.findings]}")
    check(counted == 67, f"67 separator-carrying numerals were read; now "
                         f"{counted}: the silence must be over the same text")


def test_the_command_says_it_on_every_surface() -> None:
    """`llossless verify`, as an operator runs it, at both depths.

    `attribution_invented`'s sources and its honest merge (the attribution
    corrected, so the attribution check is quiet), with the model half
    scripted by `test_cli`'s own script. One sentence is appended to source B
    and to the merge, and only the merge's numeral varies:

      planted  "17.560 requests": the source's settled 17560 read as 17.56,
               a fault, exit 1, named on every surface;
      control  "17,560 requests": the same value, clean, exit 0, and no
               surface mentions the number format at all.
    """
    import json

    import test_cli
    from llossless import config, report

    fixture = test_cli.ATTRIBUTION_FIXTURE
    line = "\nThe relay accepts up to {} requests in each burst.\n"
    source_b = (fixture / "source_b.md").read_text(encoding="utf-8") + line.format("17,560")
    honest = (fixture / "merged.md").read_text(encoding="utf-8").replace(
        "According to the Operator Guide", "According to the Deployment Notes")
    for depth in config.VERIFY_DEPTHS:
        for label, value in (("planted", "17.560"), ("control", "17,560")):
            with test_cli.workspace(test_cli._attribution_script()) as (home, url):
                (home / "source_a.md").write_text(
                    (fixture / "source_a.md").read_text(encoding="utf-8"),
                    encoding="utf-8")
                (home / "source_b.md").write_text(source_b, encoding="utf-8")
                (home / "merged.md").write_text(honest + line.format(value),
                                                encoding="utf-8")
                code, out, err = test_cli.invoke(
                    home, url, "verify", str(home / "source_a.md"),
                    str(home / "source_b.md"), str(home / "merged.md"),
                    "--verify-depth", depth, "--json", str(home / "r.json"),
                    "--html", str(home / "r.html"))
                data = json.loads((home / "r.json").read_text(encoding="utf-8"))
                page = (home / "r.html").read_text(encoding="utf-8")
            block = data.get("number_format", {})
            said = {
                "verdict": f"In the numbers: 1 value(s) {report.NUMBER_CHANGED_WORDS}" in out,
                "section": "## Number format" in out,
                "cards": page.count('data-kind="reading_changed"') == 1,
                "terminal": report.NUMBER_CHANGED_WORDS in test_cli.strip(err),
                "json": [f["kind"] for f in block.get("findings", [])]
                        == ["reading_changed"],
            }
            where = f"{label} at {depth}"
            check(block.get("ran") is True and len(block.get("documents", [])) == 3,
                  f"{where}: the check runs on verify and decides three "
                  f"documents: {block}")
            if label == "planted":
                check(code == 1, f"{where}: a changed value exits 1, got {code}; "
                                 f"{err[-300:]!r}")
                check(all(said.values()), f"{where}: every surface says it: {said}")
            else:
                check(code == 0 and not block.get("findings"),
                      f"{where}: the same value is clean: {code} {block}")
                check(not any(said.values()) and "Number format" not in page,
                      f"{where}: and no surface mentions it: {said}")


def test_a_document_against_its_language_reaches_every_surface() -> None:
    """`llossless verify` where a source's numerals outvote its language.

    `attribution_invented`'s English source A has no numeral that votes, so
    one sentence with a decimal comma makes it a decimal-comma document by a
    unanimous vote. The merge carries the same sentence beside source B's
    "1.2", so its vote splits, its language decides, and its "4,5" is the
    other convention. Two warnings, no fault: exit 0, and every surface names
    the document row by its own words.
    """
    import json

    import test_cli
    from llossless import config, report

    fixture = test_cli.ATTRIBUTION_FIXTURE
    added = "\nThe relay drains 4,5 requests per second on average.\n"
    source_a = (fixture / "source_a.md").read_text(encoding="utf-8") + added
    honest = (fixture / "merged.md").read_text(encoding="utf-8").replace(
        "According to the Operator Guide", "According to the Deployment Notes")
    words = report._NUMBER_KIND_WORDS[numerals.AGAINST_LANGUAGE]
    for depth in config.VERIFY_DEPTHS:
        with test_cli.workspace(test_cli._attribution_script()) as (home, url):
            (home / "source_a.md").write_text(source_a, encoding="utf-8")
            (home / "source_b.md").write_text(
                (fixture / "source_b.md").read_text(encoding="utf-8"),
                encoding="utf-8")
            (home / "merged.md").write_text(honest + added, encoding="utf-8")
            code, out, err = test_cli.invoke(
                home, url, "verify", str(home / "source_a.md"),
                str(home / "source_b.md"), str(home / "merged.md"),
                "--verify-depth", depth, "--json", str(home / "r.json"),
                "--html", str(home / "r.html"))
            data = json.loads((home / "r.json").read_text(encoding="utf-8"))
            page = (home / "r.html").read_text(encoding="utf-8")
        block = data.get("number_format", {})
        kinds = [f["kind"] for f in block.get("findings", [])]
        where = f"against its language at {depth}"
        check(code == 0, f"{where}: two warnings and no fault exit 0, got "
                         f"{code}; {err[-300:]!r}")
        first = (block.get("findings") or [{}])[0].get("detail", "")
        check(kinds == [numerals.AGAINST_LANGUAGE, numerals.OTHER_CONVENTION]
              and "source_a.md is English" in first and "'4,5' (line 7)" in first,
              f"{where}: source A's row names its numeral, then the merge's "
              f"other-convention row: {block.get('findings')}")
        said = {
            "verdict": "2 number-format warning(s), on numerals that could be "
                       "misread" in out,
            "section": f"- **{words}** " in out,
            "cards": page.count(f'data-kind="{numerals.AGAINST_LANGUAGE}"') == 1,
            "terminal": "2 number-format warning(s)" in test_cli.strip(err),
        }
        check(all(said.values()), f"{where}: every surface says it: {said}")


# --------------------------------------------------------------------------
# Seeded: each rule removed from a copy of the shipped source
# --------------------------------------------------------------------------

SEEDS = (
    ("the majority decides a split vote, as first agreed, not the language",
     "    elif spoken:\n",
     "    elif spoken and len(points) == len(commas):\n"),
    ("an ambiguous numeral is never flagged under a winner",
     "    if not decided or DECIMAL_MARK[decided] in numeral.text:",
     "    if not decided:"),
    ("every ambiguous numeral is flagged under a winner",
     "    if not decided or DECIMAL_MARK[decided] in numeral.text:",
     "    if True:"),
    ("a flagged source value rewritten is a fault, not resolved",
     "resolved = bool(_flag(source, convention)) and mine <= source.plausible()",
     "resolved = False"),
    ("designation words are read as decimals",
     "            if word_before in _DESIGNATIONS:\n                continue\n",
     ""),
    ("clock times are read as decimals",
     "            if word_after in _TIME_WORDS or word_after.rstrip(\".\") in _TIME_WORDS:\n"
     "                continue\n",
     ""),
    ("a function word pairs numerals",
     "if mine and mine == theirs and mine not in _FUNCTION_WORDS:",
     "if mine and mine == theirs:"),
    ("three digits after one separator votes",
     "        return _DECIMAL, votes\n    return _AMBIGUOUS, \"\"",
     "        return _DECIMAL, votes\n    return _DECIMAL, votes"),
    ("the merge's warning is not suppressed under its reading finding",
     "if _flag(numeral, whole) and numeral not in paired]",
     "if _flag(numeral, whole)]"),
    ("a document against its language is never reported",
     "    if not spoken or LANGUAGE_CONVENTION[spoken] == convention.convention:\n",
     "    if True:\n"),
    ("a document is reported wherever its numerals decided, agreeing or not",
     "    if not spoken or LANGUAGE_CONVENTION[spoken] == convention.convention:\n",
     "    if not spoken or convention.decided_by != BY_VOTES:\n"),
    ("a language the count left unknown is guessed from the larger count",
     "    spoken = convention.language\n",
     "    spoken = convention.language or (\n"
     "        \"en\" if convention.english_words > convention.german_words else \"\")\n"),
    ("a document against its language moves the exit code",
     "FAULTS = frozenset({READING_CHANGED})",
     "FAULTS = frozenset({READING_CHANGED, AGAINST_LANGUAGE})"),
    ("the row names only the first numeral",
     "    listed = [f\"{n.text!r} (line {n.line})\" for n in named]",
     "    listed = [f\"{n.text!r} (line {n.line})\" for n in named[:1]]"),
)


def seeded(old: str, new: str):
    """A fresh module from the shipped source with one rule replaced."""
    source = SHIPPED.read_text(encoding="utf-8")
    if source.count(old) != 1:
        return None
    name = "llossless._numerals_seeded"
    spec = importlib.util.spec_from_loader(name, loader=None)
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "llossless"
    sys.modules[name] = module
    try:
        exec(compile(source.replace(old, new), str(SHIPPED), "exec"),
             module.__dict__)
    finally:
        sys.modules.pop(name, None)
    return module


def test_each_seeded_break_is_caught() -> None:
    for label, old, new in SEEDS:
        module = seeded(old, new)
        check(module is not None,
              f"seed {label!r}: its anchor is not in the shipped source once; "
              f"the seed has drifted and would pass vacuously")
        if module is None:
            continue
        check(bool(probes(module)),
              f"seed {label!r}: every probe stays green with the rule removed")


def test_numerals_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and not k.endswith("_offline")
             and callable(v)]
    for test in tests:
        test()
    if failures:
        print(f"numerals: FAILED ({len(failures)} failing)")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"numerals: {len(tests)} checks pass, {len(SEEDS)} seeded breaks "
          f"each caught")
    return 0


if __name__ == "__main__":
    sys.exit(main())
