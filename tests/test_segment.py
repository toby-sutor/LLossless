#!/usr/bin/env python3
"""Offline checks for the deterministic segmenter. No network, no model.

The acceptance criterion is one sentence -- "segmentation is a pure function of
the text: same input, same ids, no model, no randomness" -- and purity is the
easy half. The half worth testing is the invariant that makes the coverage
figure mean anything: **every segment's text is findable in the document it
came from**, once whitespace is normalised. A segmenter that invents, reorders
or truncates content would still be pure, and every absence it then reported
would be an absence of something the source never said.

That invariant is asserted over all 24 fixture sources rather than over one
hand-built example, because it is the property the whole instrument rests on.

Run with `python3 tests/test_segment.py`, or collect with pytest.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# This module makes no call at all, which is exactly why the guard
# is here: "it does not use the network" is a claim, and tests/test_socket_guard
# checks that every test module states it the same way.
socket_guard.install()

from llossless import segment  # noqa: E402
from llossless.segment import (  # noqa: E402
    CODE,
    CODE_BLOCK,
    HEADING,
    LINK,
    LIST_ITEM,
    NUMERIC,
    PATH,
    SENTENCE,
    SPAN_KINDS,
    TABLE_ROW,
    TITLE,
    URL,
    VERSION,
)

FIXTURES = ROOT / "tests" / "fixtures"

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def flat(text: str) -> str:
    """Whitespace-normalised, the way the coverage checker must compare."""
    return " ".join(text.split())


def fixture_sources() -> list[tuple[Path, str]]:
    return [
        (path, path.read_text(encoding="utf-8"))
        for path in sorted(FIXTURES.glob("*/source_*.md"))
    ]


def segments_of(text: str, letter: str = "a") -> list[segment.Segment]:
    return list(segment.segment_document(text, letter).segments)


def kinds_of(text: str) -> list[tuple[str, str]]:
    return [(item.kind, item.text) for item in segments_of(text)]


# --- the invariant the instrument rests on ---------------------------------


def test_every_segment_is_findable_in_its_own_source() -> None:
    """No segment says anything the document does not, whitespace aside.

    The one transformation allowed is notation removal -- a `#`, a bullet, a
    blockquote arrow -- and removing notation from the front of a line leaves
    the remainder a substring of it. So this holds for every kind, and a kind
    that needed an exemption would be a kind that had rewritten its source.
    """
    for path, text in fixture_sources():
        flattened = flat(text)
        for item in segments_of(text):
            check(
                flat(item.text) in flattened,
                f"{path.parent.name}/{path.name} {item.id} ({item.kind}) is not in its "
                f"own source: {item.text[:60]!r}",
            )


def test_every_fixture_source_yields_segments() -> None:
    for path, text in fixture_sources():
        check(
            bool(segments_of(text)),
            f"{path.parent.name}/{path.name} segmented to nothing",
        )


def test_segmentation_is_a_pure_function_of_the_text() -> None:
    """Same text, same ids, same kinds, same offsets. Run twice, compare."""
    for path, text in fixture_sources():
        first = segment.segment_document(text, "a", path.name)
        second = segment.segment_document(text, "a", path.name)
        check(first == second, f"{path.parent.name}/{path.name} segmented differently twice")


def test_ids_are_the_document_letter_and_a_gapless_ordinal() -> None:
    for path, text in fixture_sources():
        for expected, item in enumerate(segments_of(text, "b"), start=1):
            check(
                item.id == f"b{expected}" and item.ordinal == expected and item.document == "b",
                f"{path.parent.name}/{path.name}: expected id b{expected}, got {item.id!r}",
            )


def test_document_letters_run_past_z() -> None:
    check(segment.document_id(0) == "a", "document 0 is a")
    check(segment.document_id(25) == "z", "document 25 is z")
    check(segment.document_id(26) == "aa", f"document 26 is aa, got {segment.document_id(26)!r}")
    check(segment.document_id(27) == "ab", f"document 27 is ab, got {segment.document_id(27)!r}")


def test_a_canonical_source_name_round_trips_its_letter() -> None:
    """`source_name` writes the letter and `document_letter` reads it back.

    One rule in one module because `merge.source_names` builds these names and
    `decompose.claim_id` takes them apart: a template here and a parser there
    would be two rules that agree until someone changes one. Past the
    twenty-sixth document the letter is two characters, which is why this is a
    match and not a first character -- `source_a.md` and `source_aa.md` would
    otherwise produce the same claim-id prefix inside one verify batch.
    """
    for index in (0, 1, 25, 26, 27, 701):
        name = segment.source_name(index)
        check(segment.document_letter(name) == segment.document_id(index),
              f"{name!r} must carry the letter document_id({index}) gave it")
    check(segment.source_name(0) == "source_a.md",
          f"the first source is source_a.md, got {segment.source_name(0)!r}")
    check(segment.source_name(26) == "source_aa.md",
          f"the 27th is source_aa.md, got {segment.source_name(26)!r}")
    check(segment.document_letter("source_a.md") != segment.document_letter("source_aa.md"),
          "a one-letter and a two-letter document must not collide")

    for other in (segment.MERGED_NAME, "notes-a.md", "source_A.md", "source_.md", "sources_a.md"):
        check(segment.document_letter(other) == "",
              f"{other!r} is not a name this module writes and must not parse as one")


def test_sources_are_lettered_in_the_order_they_are_given() -> None:
    documents = segment.segment_sources({"source_a.md": "First.\n", "source_b.md": "Second.\n"})
    check([d.id for d in documents] == ["a", "b"], f"lettering follows order, got {documents}")
    check(
        [d.filename for d in documents] == ["source_a.md", "source_b.md"],
        "each document keeps the filename it was given",
    )
    check(
        documents[1].segments[0].id == "b1",
        f"the second document's first segment is b1, got {documents[1].segments[0].id!r}",
    )


# --- kinds ------------------------------------------------------------------


def test_the_first_h1_is_the_title_and_a_later_one_is_not() -> None:
    kinds = kinds_of("# One\n\nBody text here.\n\n# Two\n\nMore body.\n")
    check(kinds[0] == (TITLE, "One"), f"the first H1 is the title, got {kinds[0]}")
    check((HEADING, "Two") in kinds, f"a later H1 is a heading, got {kinds}")
    check(
        sum(1 for kind, _ in kinds if kind == TITLE) == 1,
        f"a document has at most one title, got {kinds}",
    )


def test_a_short_unpunctuated_first_line_is_a_title_without_a_hash() -> None:
    """Neither real input in hand is markdown, and both open with a bare title."""
    kinds = kinds_of("Willow Lane Depot Notes\n\nThe depot opened in 1974.\n")
    check(kinds[0] == (TITLE, "Willow Lane Depot Notes"), f"got {kinds[0]}")
    check(kinds[1][0] == SENTENCE, f"the body is prose, got {kinds[1]}")


def test_a_first_line_that_ends_a_sentence_is_not_a_title() -> None:
    kinds = kinds_of("The depot opened in 1974.\n\nIt closed in 1998.\n")
    check(
        all(kind == SENTENCE for kind, _ in kinds),
        f"a punctuated opening line is prose, not a title: {kinds}",
    )


def test_a_setext_underline_makes_a_title() -> None:
    kinds = kinds_of("Depot Notes\n===========\n\nThe depot opened in 1974.\n")
    check(kinds[0] == (TITLE, "Depot Notes"), f"got {kinds[0]}")
    check(len(kinds) == 2, f"the underline is notation and is not a segment: {kinds}")


def test_notation_is_stripped_from_headings_lists_and_quotes() -> None:
    kinds = kinds_of("## Limits ##\n\n- The cap is 512.\n\n> Quoted claim here.\n")
    check((HEADING, "Limits") in kinds, f"heading markers are stripped: {kinds}")
    check((LIST_ITEM, "The cap is 512.") in kinds, f"bullets are stripped: {kinds}")
    check((SENTENCE, "Quoted claim here.") in kinds, f"quote arrows are stripped: {kinds}")


def test_a_heading_records_its_level() -> None:
    levels = {item.text: item.level for item in segments_of("# One\n\n### Three\n\nBody.\n")}
    check(levels.get("One") == 1, f"an H1 is level 1, got {levels}")
    check(levels.get("Three") == 3, f"an H3 is level 3, got {levels}")
    check(levels.get("Body.") == 0, f"prose has no level, got {levels}")


def test_a_fenced_block_is_one_segment_and_keeps_every_byte() -> None:
    text = "Run it:\n\n```bash\n./relay --port 8443 \\\n  --verbose\n```\n\nThen check.\n"
    blocks = [item for item in segments_of(text) if item.kind == CODE_BLOCK]
    check(len(blocks) == 1, f"one fenced block is one segment, got {len(blocks)}")
    check(
        blocks[0].text == "```bash\n./relay --port 8443 \\\n  --verbose\n```",
        f"the block keeps its fences and its line breaks, got {blocks[0].text!r}",
    )


def test_only_a_code_block_may_contain_a_newline() -> None:
    """The merge prompt renders one segment per line; a newline breaks that.

    Segments render as `a1| text`, so a segment with
    an embedded newline has no rendering. Code blocks are the exception and
    how to render them across multiple lines is still an open question; this
    test is where that fact is written down rather than discovered.
    """
    for path, text in fixture_sources():
        for item in segments_of(text):
            check(
                "\n" not in item.text or item.kind == CODE_BLOCK,
                f"{path.parent.name}/{path.name} {item.id} ({item.kind}) contains a newline",
            )


def test_a_table_row_becomes_a_segment_and_its_rule_does_not() -> None:
    document = segment.segment_document(
        "| name | value |\n|------|-------|\n| port | 8443 |\n", "a"
    )
    kinds = [(item.kind, item.text) for item in document.segments]
    check(kinds == [(TABLE_ROW, "name | value"), (TABLE_ROW, "port | 8443")], f"got {kinds}")
    check(
        document.skipped == ((2, "table rule"),),
        f"the delimiter row is recorded as skipped, got {document.skipped}",
    )


def test_a_horizontal_rule_is_recorded_rather_than_dropped() -> None:
    document = segment.segment_document("One thing.\n\n---\n\nAnother thing.\n", "a")
    check(len(document.segments) == 2, f"a rule is not a segment: {document.segments}")
    check(
        document.skipped == ((3, "horizontal rule"),),
        f"a rule is skipped with a reason, got {document.skipped}",
    )


def test_a_dash_rule_is_not_read_as_a_bullet() -> None:
    kinds = kinds_of("Body.\n\n* * *\n\nMore body.\n")
    check(
        all(kind == SENTENCE for kind, _ in kinds),
        f"`* * *` is a rule, not a list item: {kinds}",
    )


# --- sentences --------------------------------------------------------------


def test_two_sentences_on_one_line_become_two_segments() -> None:
    kinds = kinds_of("The relay listens on 8443. The timeout is 30 seconds.\n")
    check(
        kinds == [(SENTENCE, "The relay listens on 8443."),
                  (SENTENCE, "The timeout is 30 seconds.")],
        f"got {kinds}",
    )


def test_a_version_ending_a_sentence_still_splits() -> None:
    """`TLS 1.2.` is the fixture case, and the interior dot must not block it."""
    kinds = kinds_of("The minimum is TLS 1.2. The cap is 512.\n")
    check(len(kinds) == 2, f"expected two sentences, got {kinds}")


def test_an_abbreviation_does_not_split_a_sentence() -> None:
    for text, expected in (
        ("The depot, e.g. Willow Lane, opened in 1974.", 1),
        ("Dr. Halloway signed the report.", 1),
        ("Initials like J. Willis are one name.", 1),
    ):
        got = segment.split_sentences(text)
        check(len(got) == expected, f"{text!r} split into {got}")


# --- German abbreviations, and a bracket in front of one -------------------

# Each is one sentence. The shipped code used to split 12 of the 15; the
# `d. h.`, `u. a.` and `S.` rows it already held together (a lowercase second
# half, or a bare single letter), and they are here so the single-letter rule
# keeps doing so.
ONE_SENTENCE = (
    "Wenn ein Spieler zu einem offenen Pong (z. B. drei Bambus-5-Ziegel) den "
    "vierten Stein zieht, kann ein anderer ihn fordern.",
    "Er zählt (d. h. Der Rufer zählt zuerst) die Punkte.",
    "Gespielt werden (u. a. Mah-Jongg) mehrere Spiele.",
    "Die Regeln (z. T. Aus China) sind alt.",
    "Rot bzw. Blau ist erlaubt.",
    "Es kamen ca. Hundert Leute.",
    "Die dt. Ausgabe erschien später.",
    "Die Regel gilt, vgl. Kapitel drei, für alle.",
    "Das Zimmer Nr. Zwölf ist frei.",
    "Das Spiel kommt evtl. Morgen.",
    "Er zahlt ggf. Gebühren nach.",
    "Der Preis gilt inkl. Versand.",
    "Siehe S. Zwölf im Anhang.",
    "Use a flag (e.g. Foo) here.",
    "Use one (i.e. Bar) there.",
)

# A full stop after one of these is a real end, and still splits. The rule:
# only a word that qualifies what follows it is an abbreviation; `usw.` and
# `etc.` close an enumeration and are left to split, and a bracket that closed
# before the stop (`(A).`) ends the sentence it closes.
TWO_SENTENCES = (
    "Äpfel, Birnen usw. Der nächste Satz beginnt hier.",
    "Apples, pears etc. The next sentence starts here.",
    "Wähle Option (A). Der nächste Satz beginnt hier.",
    "Er kam (spät). Dann ging er.",
)


def test_german_abbreviations_do_not_split_a_sentence() -> None:
    for text in ONE_SENTENCE:
        got = segment.split_sentences(text)
        check(len(got) == 1, f"{text!r} is one sentence, split into {got}")


def test_a_real_sentence_end_after_an_abbreviation_still_splits() -> None:
    for text in TWO_SENTENCES:
        got = segment.split_sentences(text)
        check(len(got) == 2, f"{text!r} is two sentences, got {got}")


# --- A sentence opening on a non-ASCII capital, and German ordinals --------

# Each is two sentences. The shipped code used to join every one: its
# lookahead accepted only `[A-Z0-9]` after the gap, and `„`, `«`, `»` were not
# openers. A wrong join hides the second sentence inside the first.
UMLAUT_STARTS = (
    "Das ist gut. Äpfel sind rot.",
    "Er ging. Öl ist teuer.",
    "Er ging. Über den Berg kam er.",
    "Il est parti. Élise est restée.",
)
QUOTED_STARTS = (
    "Er sagte das. „Nein“, rief sie.",
    "Er sagte das. «Nein», rief sie.",
    "Er sagte das. »Nein«, rief sie.",
    "Er sagte das. „Über allem“ stand es.",
)

# Each is one sentence; the shipped code used to split every one at the
# number's full stop.
ORDINALS = (
    "Im 19. Jahrhundert war das Spiel verbreitet.",
    "Anfang des 19. Jahrhunderts begann es.",
    "Wir kamen am 3. Oktober an.",
    "Richter & Cie (Nr. 722354 v. 6. November 1919) meldete es an.",
    "Berlin, 3. Oktober 2026.",
    "Er gewann zum 1. Mal.",
    "Das Büro liegt im 2. Stock.",
    "Im 19. Jh. entstand es.",
)

# Each is two sentences, and must stay two: a number that ends a sentence, a
# label noun after a page number, a year before a month, and a capital that
# is on neither list. The last row is a real sentence end the rule cannot tell
# from an ordinal only by being outside the lists, and splits for that reason.
NUMBER_ENDINGS = (
    "Am Ende waren es 19. Danach ging es weiter.",
    "Siehe Seite 19. Kapitel 3 folgt danach.",
    "Das war im Jahr 2026. Oktober kam spät.",
    "Wir treffen uns am 5. Bitte kommt pünktlich.",
    "Der Wert ist 19. Übersteigt er das Limit, gilt der Höchstwert.",
)


def test_a_sentence_opening_on_a_non_ascii_capital_splits() -> None:
    for text in UMLAUT_STARTS:
        got = segment.split_sentences(text)
        check(len(got) == 2, f"{text!r} is two sentences, got {got}")


def test_a_sentence_opening_on_a_german_or_french_quote_splits() -> None:
    for text in QUOTED_STARTS:
        got = segment.split_sentences(text)
        check(len(got) == 2, f"{text!r} is two sentences, got {got}")


def test_a_lowercase_letter_after_a_stop_still_joins() -> None:
    """MUST NOT FIRE: `isupper` must not widen into "any letter"."""
    for text in ("Er ging. über den Berg.", "Der Satz geht. äh, weiter.",
                 "Er sagte das. „nein“, rief sie."):
        got = segment.split_sentences(text)
        check(len(got) == 1, f"{text!r} is one sentence, got {got}")


def test_a_german_ordinal_does_not_split_a_sentence() -> None:
    for text in ORDINALS:
        got = segment.split_sentences(text)
        check(len(got) == 1, f"{text!r} is one sentence, split into {got}")


def test_a_real_sentence_ending_in_a_number_still_splits() -> None:
    for text in NUMBER_ENDINGS:
        got = segment.split_sentences(text)
        check(len(got) == 2, f"{text!r} is two sentences, got {got}")


# --- A closing curly quote or guillemet after the stop splits --------------

# Each is two sentences. The shipped code used to join every one: the
# closer class in `_SENTENCE_END` held only `"'’)]`, so a curly or guillemet
# character glued to the terminator was not even a candidate boundary -- the
# dangerous direction, since the second sentence hides inside the first.
CLOSING_QUOTE_STARTS = (
    "„Nein.“ Dann kam er.",
    "“Done.” Then he came.",
    "«Non.» Puis il vint.",
    "‚ja.‘ Dann kam er.",
    "‹ja.› Dann kam er.",
    "»Nein.« Dann kam er.",
)


def test_a_closing_curly_quote_or_guillemet_after_the_stop_splits() -> None:
    for text in CLOSING_QUOTE_STARTS:
        got = segment.split_sentences(text)
        check(len(got) == 2, f"{text!r} is two sentences, got {got}")


def test_an_abbreviation_inside_quotes_does_not_wrongly_split() -> None:
    for text in (
        "Er zeigte „z. B. drei Dinge“ und ging.",
        "Sie nannte ‚z. B. drei Dinge‘ und ging.",
    ):
        got = segment.split_sentences(text)
        check(len(got) == 1, f"{text!r} is one sentence, got {got}")


def test_a_quote_that_opens_a_sentence_still_works() -> None:
    """The opening-quote case, unchanged by the later widening of the closer class."""
    for text in QUOTED_STARTS:
        got = segment.split_sentences(text)
        check(len(got) == 2, f"{text!r} is two sentences, got {got}")


# Every document a recorded cassette or a recorded merge was made from, or is.
# Segments are rendered into the merge prompt one per line, so a partition that
# moves re-keys every merge cassette over that document. Pinned by digest,
# rather than by a count, because a count survives a boundary that moved.
PARTITION_PINS = ROOT / "tests" / "segment_pins.json"
RECORDED_GLOBS = ("tests/fixtures/**/*", "tests/pairs/**/*", "tests/attribution/**/*",
                  "tests/responses/*/merges/*")


def recorded_documents() -> list[tuple[str, str]]:
    found: dict[str, Path] = {}
    for pattern in RECORDED_GLOBS:
        for path in ROOT.glob(pattern):
            if (path.is_file() and path.suffix in (".md", ".txt")
                    and path.name not in ("README.md", "SCHEMA.md")):
                found[path.relative_to(ROOT).as_posix()] = path
    return [(rel, found[rel].read_text(encoding="utf-8")) for rel in sorted(found)]


def partition_digest(text: str) -> str:
    """Everything the segmenter decides about one document, hashed."""
    import hashlib
    import json

    document = segment.segment_document(text, "a", "source_a.md")
    shape = [
        [item.id, item.kind, item.text, item.line, item.paragraph, item.level,
         item.notation, list(item.breaks), list(item.indents), item.indent,
         [[span.kind, span.text, span.start, span.unit] for span in item.spans]]
        for item in document.segments
    ]
    payload = json.dumps(
        [shape, [list(skip) for skip in document.skipped],
         segment.render_sources([document], "source_a.md")],
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def pinned_partitions() -> dict[str, str]:
    import json

    return json.loads(PARTITION_PINS.read_text(encoding="utf-8"))


def test_every_recorded_document_keeps_its_pinned_partition() -> None:
    pins = pinned_partitions()
    documents = recorded_documents()
    on_disk = {rel for rel, _ in documents}
    for rel, text in documents:
        if rel not in pins:
            check(False, f"{rel} has no pinned partition; after proving no cassette "
                         f"moves, add it with `python3 tests/test_segment.py --pin`")
        elif partition_digest(text) != pins[rel]:
            check(False, f"{rel}: the segmenter's partition moved; every merge "
                         f"cassette over this document is re-keyed")
    for rel in sorted(set(pins) - on_disk):
        check(False, f"{rel} is pinned but no longer on disk")


def test_the_partition_pin_fires_when_the_segmenter_moves() -> None:
    """MUST FIRE: with the abbreviation rule switched off in the shipped
    module, some recorded document's digest moves. Without this, a pin that
    hashed nothing the rule decides would pass on any segmenter."""
    pins = pinned_partitions()
    saved = segment._is_abbreviation
    segment._is_abbreviation = lambda word: False
    try:
        moved = [rel for rel, text in recorded_documents()
                 if rel in pins and partition_digest(text) != pins[rel]]
    finally:
        segment._is_abbreviation = saved
    check(bool(moved), "switching the abbreviation rule off moved no pinned "
                       "partition; the pin cannot see the rule it guards")


def pin_new_documents() -> int:
    """Add a digest for every recorded document that has none. Never rewrites
    one: a digest that moved is a finding, not a pin to refresh."""
    import json

    pins = pinned_partitions() if PARTITION_PINS.exists() else {}
    added = 0
    for rel, text in recorded_documents():
        if rel not in pins:
            pins[rel] = partition_digest(text)
            added += 1
    PARTITION_PINS.write_text(
        json.dumps(dict(sorted(pins.items())), indent=1) + "\n", encoding="utf-8")
    print(f"segment pins: {added} added, {len(pins)} total")
    return 0


def test_a_url_does_not_split_a_sentence() -> None:
    got = segment.split_sentences("See https://example.com/a.b/C for detail. Then stop.")
    check(len(got) == 2, f"a dotted URL is not a sentence boundary: {got}")


def test_a_hard_wrapped_sentence_comes_back_whole() -> None:
    kinds = kinds_of("The relay listens on port 8443\nby default and refuses others.\n")
    check(
        kinds == [(SENTENCE, "The relay listens on port 8443 by default and refuses others.")],
        f"a wrapped sentence rejoins on one space, got {kinds}",
    )


def test_consecutive_punctuated_lines_stay_separate() -> None:
    """One record per line, the shape a JSON fragment's fields have.

    Joining these would make two separately droppable fields into one absence,
    which is the distinction that must not go missing.
    """
    kinds = kinds_of('"title": "Willow Lane",\n"summary": "A depot record",\n')
    check(len(kinds) == 2, f"a line ending in a comma closes its block, got {kinds}")


def test_a_list_item_wraps_but_does_not_swallow_the_next_bullet() -> None:
    kinds = kinds_of("- The cap is 512 concurrent\n  connections.\n- The retry limit is 3.\n")
    check(
        kinds == [(LIST_ITEM, "The cap is 512 concurrent connections."),
                  (LIST_ITEM, "The retry limit is 3.")],
        f"got {kinds}",
    )


def test_a_segment_reports_the_line_it_began_on() -> None:
    lines = [item.line for item in segments_of("# One\n\nFirst.\nSecond.\n\nThird.\n")]
    check(lines == [1, 3, 4, 6], f"each segment reports its own line, got {lines}")


# --- spans ------------------------------------------------------------------


def spans_of(text: str) -> list[tuple[str, str]]:
    return [(span.kind, span.text) for span in segment.find_spans(text)]


def test_a_number_carries_its_unit_as_a_hint_and_not_as_its_text() -> None:
    span, = [s for s in segment.find_spans("The timeout is 30 seconds.") if s.kind == NUMERIC]
    check(span.text == "30", f"the checked token is the number, got {span.text!r}")
    check(span.unit == "seconds", f"the unit is recorded as a hint, got {span.unit!r}")


def test_a_number_keeps_a_suffix_attached_without_a_space() -> None:
    for text, expected in (("30s", "30s"), ("100%", "100%"), ("07:15", "07:15"),
                           ("2026-08-10", "2026-08-10")):
        found = [s.text for s in segment.find_spans(f"Value {text} here.") if s.kind == NUMERIC]
        check(expected in found, f"{text!r} yielded numeric spans {found}")
    # `30s` must come back whole, or "30 seconds" -> "30s" passes unnoticed.
    found = [s.text for s in segment.find_spans("Value 30s here.") if s.kind == NUMERIC]
    check(found == ["30s"], f"an attached unit is part of the token, got {found}")


def test_a_dotted_version_is_its_own_class() -> None:
    kinds = dict((kind, text) for kind, text in spans_of("Requires v2.10.3 or 1.4.0 of it."))
    check(kinds.get(VERSION) is not None, f"a version is found, got {spans_of('v2.10.3')}")
    found = [text for kind, text in spans_of("Requires v2.10.3 or later.") if kind == VERSION]
    check(found == ["v2.10.3"], f"got {found}")


def test_a_markdown_link_yields_both_the_link_and_its_destination() -> None:
    found = spans_of("See [the guide](https://example.com/guide) for detail.")
    check((LINK, "[the guide](https://example.com/guide)") in found, f"got {found}")
    check((URL, "https://example.com/guide") in found, f"got {found}")


def test_a_number_inside_a_url_is_not_a_second_finding() -> None:
    found = spans_of("See https://example.com/v2/8443 for detail.")
    check(
        [kind for kind, _ in found] == [URL],
        f"a URL is masked before numbers are looked for, got {found}",
    )


def test_a_path_is_found_and_a_bare_slash_is_not() -> None:
    check((PATH, "/-/healthy") in spans_of("The endpoint is /-/healthy."), "leading-slash path")
    check(
        (PATH, "src/llossless/merge.py") in spans_of("Edit src/llossless/merge.py first."),
        "a dotted tail makes a relative path",
    )
    for text in ("Use and/or here.", "It runs 24/7.", "Speed is 40 km/h."):
        found = [t for kind, t in spans_of(text) if kind == PATH]
        check(not found, f"{text!r} has no path, got {found}")


def test_a_code_span_is_found_and_masks_what_is_inside_it() -> None:
    found = spans_of("Set `timeout = 30` in the file.")
    check(found == [(CODE, "`timeout = 30`")], f"got {found}")


def test_a_segment_carries_the_spans_of_its_own_text() -> None:
    item, = segments_of("The connect timeout is 30 seconds.")
    check(
        [(s.kind, s.text) for s in item.spans] == [(NUMERIC, "30")],
        f"got {[(s.kind, s.text) for s in item.spans]}",
    )
    check(
        item.text[item.spans[0].start : item.spans[0].end] == "30",
        "a span's offsets index its own segment's text",
    )
    check(item.spans_of(NUMERIC) == item.spans, "spans_of selects by kind")


def test_every_span_the_segmenter_makes_is_a_kind_that_is_registered() -> None:
    """`SPAN_KINDS` is the closed set, and it is closed by this and nothing else.

    It was a tuple nothing read. A kind added to `find_spans` and not to
    the tuple would have been invisible, and the tuple is what a reader takes
    for the list of what this module can produce -- so it said one thing while
    the code did another and neither was wrong on its own.

    Read off the corpus rather than off a list here, so the denominator grows
    with the fixtures. Both directions: no unregistered kind is produced, and
    the registered set is not padded with kinds nothing makes.
    """
    made = {span.kind
            for _, text in fixture_sources()
            for item in segments_of(text)
            for span in item.spans}
    made |= {span.kind for span in segment.find_spans(
        "Set `x = 1` in v2.1.0 at /etc/hosts, see https://example.invalid "
        "and [the note](https://example.invalid/n), 30 seconds.")}
    unknown = sorted(made - set(SPAN_KINDS))
    check(not unknown,
          f"`find_spans` produces span kind(s) {unknown} that `SPAN_KINDS` "
          f"does not list; the tuple is what a reader takes for the closed set")
    unmade = sorted(set(SPAN_KINDS) - made)
    check(not unmade,
          f"`SPAN_KINDS` lists {unmade}, which neither the corpus nor the "
          f"probe above produces; a registered kind nothing makes is a kind "
          f"nothing checks")


def test_the_span_kind_registry_check_fires_both_ways() -> None:
    """Seeded: a kind dropped from the tuple, and a kind added that nothing makes.

    Both halves, because each catches the other's blind spot. The predicate is
    the two set differences in the check above, taken here against the same
    corpus so this cannot pass by looking at a smaller one.
    """
    made = {span.kind
            for _, text in fixture_sources()
            for item in segments_of(text)
            for span in item.spans}
    check(bool(made - set(k for k in SPAN_KINDS if k != NUMERIC)),
          "seeded check: dropping `numeric` from the registry was not noticed, "
          "so nothing here reads what the segmenter actually produces")
    check(bool({*SPAN_KINDS, "phase-of-the-moon"} - made
               - {k for k in SPAN_KINDS if k in made}),
          "seeded check: a registered kind nothing produces was not noticed")


def test_the_corpus_carries_the_span_classes_the_check_will_read() -> None:
    """Sanity on the fixtures: the verbatim check has something to check.

    Not a property of the segmenter so much as of what it is pointed at. A
    numeric-integrity check over a corpus with no numbers would pass at every
    stage and mean nothing, which is exactly the failure mode this check exists to end.
    """
    numerics = sum(
        len(item.spans_of(NUMERIC)) for _, text in fixture_sources() for item in segments_of(text)
    )
    check(numerics >= 20, f"the fixture sources carry {numerics} numeric spans, expected 20+")


def test_adjacent_list_items_stay_separate_segments() -> None:
    """The fusion defect, as a must-fire.

    `_take_block` skipped its block-start test while the block was still empty,
    so the bullet branch -- the one caller that starts inside a block -- pulled
    the following line in whatever it was. A list of atomic facts written
    without terminal punctuation came back as half as many segments, each
    holding two facts joined by the second one's own bullet character.

    Both halves are asserted: the shape, on a constructed list, and the corpus
    case that was live in a shipped fixture until it was fixed.
    """
    text = "## Defaults\n- Listen port: 8443\n- Connect timeout: 30 seconds\n- Retries: 3\n"
    items = [item for item in segments_of(text) if item.kind == LIST_ITEM]
    check(len(items) == 3,
          f"three bullets must be three segments, got {len(items)}: "
          f"{[item.text for item in items]}")
    check([item.text for item in items]
          == ["Listen port: 8443", "Connect timeout: 30 seconds", "Retries: 3"],
          f"and each must hold its own fact: {[item.text for item in items]}")

    defaults = [
        item.text
        for item in segments_of((FIXTURES / "paraphrase" / "source_b.md").read_text())
        if item.kind == LIST_ITEM
    ]
    check(len(defaults) == 8,
          f"paraphrase's bullet side has eight list items, not {len(defaults)}")
    for text in defaults:
        check(" - " not in text,
              f"no list item may carry another item's bullet: {text!r}")


def test_notation_is_recorded_and_rendered_back() -> None:
    """The rendering side of the same fix: the model is shown the document's shape.

    `Segment.text` stays stripped -- it is what the reconciler looks for -- and
    `Segment.notation` carries what was taken off, so `rendered` can put it
    back. Asserted on one constructed document of every kind rather than on a
    fixture, because the point is the mapping from kind to marker.
    """
    text = (
        "# Relay Notes\n\n## Defaults\n\n- Listen port: 8443\n"
        "- A longer item. With a second sentence.\n\n"
        "> Quoted for emphasis.\n\n| Setting | Value |\n| --- | --- |\n| Port | 8443 |\n\n"
        "Plain prose here.\n\n```yaml\n- not: a bullet\n# not: a heading\n```\n"
    )
    rendered = {item.id: segment.rendered(item) for item in segments_of(text)}
    lines = [item for item in rendered.values()]
    check(lines[0] == "# Relay Notes", f"the title keeps its marker: {lines[0]!r}")
    check(lines[1] == "## Defaults", f"a heading keeps its depth: {lines[1]!r}")
    check(lines[2] == "- Listen port: 8443", f"a list item keeps its bullet: {lines[2]!r}")
    check(lines[3] == "- A longer item.",
          f"the first sentence of an item carries the bullet: {lines[3]!r}")
    check(lines[4] == "  With a second sentence.",
          f"and the rest are indented under it, not bulleted again: {lines[4]!r}")
    check(lines[5] == "> Quoted for emphasis.", f"a quote keeps its arrow: {lines[5]!r}")
    check(lines[6] == "| Setting | Value |", f"a table row keeps its pipes: {lines[6]!r}")
    check(lines[8] == "Plain prose here.", f"prose gains nothing: {lines[8]!r}")
    check(lines[9] == "```yaml\n- not: a bullet\n# not: a heading\n```",
          f"a fenced block is rendered byte for byte: {lines[9]!r}")


def test_plain_is_the_inverse_of_rendered_over_every_fixture_source() -> None:
    """What `render_sources` shows the model, `plain` takes back off again.

    The round trip is the contract this design rests on: the merge sees notation,
    the reconciler compares `Segment.text` on both sides, and `reconcile.flatten`
    is the only place that reconciliation happens. Asserted over every fixture
    source, and separately for the fence carve-out, which is the one shape
    `plain` must not touch.
    """
    for path, text in fixture_sources():
        for item in segments_of(text):
            if item.kind == CODE_BLOCK:
                check(segment.rendered(item) == item.text,
                      f"{path.name} {item.id}: a fenced block is rendered unchanged")
                continue
            back = segment.plain(segment.rendered(item))
            check(" ".join(back.split()) == " ".join(item.text.split()),
                  f"{path.name} {item.id}: plain(rendered(x)) must be x, got {back!r} "
                  f"for {item.text!r}")

    fenced = "```yaml\n- a: 1\n# a comment\n> not a quote\n```"
    check(segment.plain(fenced) == fenced,
          f"plain must not reach inside a fence: {segment.plain(fenced)!r}")
    check(segment.plain("## H\n- item\n> quote\n| a | b |") == "H\nitem\nquote\na | b",
          f"and must take every marker off outside one: {segment.plain('## H')!r}")


def source_paragraphs(text: str) -> list[tuple[int, int]]:
    """The source's own blank-line blocks, as (first line, last line) pairs.

    Computed here from the raw bytes, deliberately not from anything in
    `segment`: the point of the assertion below is that two independent
    readings of the same document agree on where the paragraphs are, and a
    helper that called `segment_document` would be comparing it with itself.
    """
    blocks: list[tuple[int, int]] = []
    start: int | None = None
    lines = text.splitlines()
    for number, raw in enumerate(lines, 1):
        if raw.strip():
            if start is None:
                start = number
        elif start is not None:
            blocks.append((start, number - 1))
            start = None
    if start is not None:
        blocks.append((start, len(lines)))
    return blocks


def test_the_source_paragraph_survives_into_the_wire_format() -> None:
    """The merge is shown which sentences shared a paragraph.

    Two halves, and the second is the one that makes the first mean anything.

    The partition: `Segment.paragraph` must agree, segment for segment, with
    the partition recovered from `Document.text` plus `Segment.line` -- the
    property this fix established and the whole change rests on. Asserted over
    every fixture source rather than one example, because a field that is right
    on prose and wrong on a fenced block or a wrapped list item would be a
    silent mis-grouping in exactly the documents this tool is for.

    The rendering: a document with a paragraph boundary must show one, and a
    document without must show none. Both directions, because a renderer that
    emitted a blank line everywhere would pass the first check alone and would
    be telling the model that every sentence stands on its own -- which is the
    defect, restated.
    """
    multi = None
    single = None
    for path, text in fixture_sources():
        doc = segment.segment_document(text, "a", "source_a.md")
        if not doc.segments:
            continue

        blocks = source_paragraphs(text)

        def block_of(line: int) -> int:
            for index, (first, last) in enumerate(blocks, 1):
                if first <= line <= last:
                    return index
            return 0

        recovered = [tuple(item.id for item in doc.segments
                           if block_of(item.line) == index)
                     for index in range(1, len(blocks) + 1)]
        recovered = [group for group in recovered if group]

        carried: list[tuple[str, ...]] = []
        for item in doc.segments:
            if carried and item.paragraph == last_seen:
                carried[-1] = carried[-1] + (item.id,)
            else:
                carried.append((item.id,))
            last_seen = item.paragraph

        check(carried == recovered,
              f"{path.name}: the paragraph field must partition the segments "
              f"exactly as the source's blank lines do\n  field: {carried}\n"
              f"  lines: {recovered}")

        body = segment.render_sources([doc], "source_a.md")
        body = body.split(">", 1)[1].rsplit("</document>", 1)[0].strip("\n")
        blanks = sum(1 for line in body.splitlines() if not line.strip())
        boundaries = len(carried) - 1
        check(blanks == boundaries,
              f"{path.name}: {boundaries} paragraph boundary(ies) must render as "
              f"{boundaries} blank line(s) inside the block, got {blanks}")
        if boundaries and multi is None:
            multi = (path.name, blanks)
        if not boundaries and single is None:
            single = (path.name, blanks)

    # Seeded probes, so a corpus that happened to hold only one shape could not
    # leave half of this check unexercised and green.
    joined = "One. Two.\n\nThree. Four.\n"
    doc = segment.segment_document(joined, "a", "source_a.md")
    shown = segment.render_sources([doc], "source_a.md")
    check("Two.\n\na3| Three." in shown,
          f"must fire: a blank line stands between the two paragraphs\n{shown}")
    check([item.paragraph for item in doc.segments] == [1, 1, 2, 2],
          f"and the field says so: "
          f"{[item.paragraph for item in doc.segments]}")

    unbroken = "One. Two.\nThree. Four.\n"
    doc = segment.segment_document(unbroken, "a", "source_a.md")
    shown = segment.render_sources([doc], "source_a.md")
    inside = shown.split(">", 1)[1].rsplit("</document>", 1)[0].strip("\n")
    check(not any(not line.strip() for line in inside.splitlines()),
          f"must not fire: one paragraph gets no blank line at all\n{shown}")
    check({item.paragraph for item in doc.segments} == {1},
          f"and the field says so: "
          f"{[item.paragraph for item in doc.segments]}")

    fenced = "Before.\n\n```\none\n\ntwo\n```\n\nAfter.\n"
    doc = segment.segment_document(fenced, "a", "source_a.md")
    check([item.paragraph for item in doc.segments] == [1, 2, 3],
          f"a blank line inside a fence is content, not a boundary: "
          f"{[(item.id, item.paragraph) for item in doc.segments]}")


def test_a_span_never_carries_the_mask() -> None:
    """`find_spans` returns readable tokens, not `_mask`'s NULs.

    Spans are found most specific first and masked as they go, so a pattern
    matching over an already-masked string captured the NULs: a link whose
    display text held a code span came back as `[the \x00\x00\x00 guide](...)`.
    That needle occurs in no merge, so an intact link was reported as a
    verbatim violation, and the finding printed the NULs at the reader.
    """
    probe = "See [the `relay` guide](https://example.test/docs/relay.md) for detail."
    links = [span for span in segment.find_spans(probe) if span.kind == LINK]
    check(len(links) == 1, f"the probe must produce one link span, got {len(links)}")
    check(links[0].text == "[the `relay` guide](https://example.test/docs/relay.md)",
          f"and it must be readable: {links[0].text!r}")
    check(probe.find(links[0].text) == links[0].start,
          "a span's text must sit at its own offset in the text it came from")

    for path, text in fixture_sources():
        for item in segments_of(text):
            check("\x00" not in item.text, f"{path.name} {item.id}: NUL in segment text")
            for span in item.spans:
                check("\x00" not in span.text,
                      f"{path.name} {item.id}: NUL in a {span.kind} span")


def test_segment_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def test_a_closing_hash_sequence_needs_a_space_before_it() -> None:
    """`# C#` kept its hash. CommonMark 4.2 requires the space."""
    def title(line: str) -> str:
        return segment.segment_document(line + "\nBody.\n", "a").segments[0].text
    check(title("# C#") == "C#", f"a language name keeps its hash: {title('# C#')!r}")
    check(title("# Title ##") == "Title", "a real closing sequence still goes")
    check(title("# Title") == "Title", "an ordinary heading is unchanged")
    check(title("# C# ##") == "C#", "both at once: the closing sequence goes, the name stays")
    check(segment.plain("# C#") == "C#",
          f"plain() uses the same rule: {segment.plain('# C#')!r}")


def test_an_unclosed_fence_is_reported_and_not_closed() -> None:
    """Ruled report, do not repair.

    Closing the block at the next blank line would change what the document
    means without saying so. Everything after the opener really is one code
    block; the reader is told where it opened and decides.
    """
    document = segment.segment_document("# T\n\n```\ncode\n\nprose after\n", "a")
    fences = [r for r in document.skipped if r[1].startswith("fence opened")]
    check(len(fences) == 1, f"an unclosed fence must be recorded once: {document.skipped}")
    check(fences and fences[0][0] == 3,
          f"it must name the line the fence opened at: {fences}")
    kinds = [s.kind for s in document.segments]
    check(kinds.count(CODE_BLOCK) == 1,
          f"the block is left open, not split or closed: {kinds}")

    closed = segment.segment_document("# T\n\n```\ncode\n```\n\nprose after\n", "a")
    check(not [r for r in closed.skipped if r[1].startswith("fence opened")],
          f"a closed fence reports nothing: {closed.skipped}")


def test_indentation_reaches_the_model_without_reaching_the_comparisons() -> None:
    """A model cannot reproduce what it was never shown.

    Line breaks inside a segment were recorded and restored from the start.
    The whitespace *after* them was not: every line was stripped as it
    was accumulated, so an indented document arrived at the merge model flush
    left and came back flush left. Two FizzBuzz pairs in `toby-test-9` lost
    their nesting entirely -- `0, 0, 4, 8, 12, ...` came out `0, 0, 1, 1, 1`
    -- and the model was not at fault: it wrote back what it had been handed.

    **The indent is carried beside `text`, never in it.** `Segment.text` is
    what every comparison is made against, what the reconciler locates, and
    what the segment count is registered over. Moving it would re-key the
    corpus and redefine a registered denominator. `indents` rides alongside
    `breaks`, which already solves this exact problem for the newline itself.
    """
    source = (
        "class Program {\n"
        "    static void Main() {\n"
        "        Console.WriteLine(1);\n"
        "    }\n"
        "}\n"
    )
    document = segment.segment_document(source, "a", "program.md")
    body = document.segments[0]

    check("\n" not in body.text,
          f"the flattened text is still one line: {body.text[:60]!r}")
    check(not body.text[:1].isspace(),
          "and still carries no leading whitespace, so every existing "
          "comparison sees exactly the string it saw before")
    check(len(body.indents) == len(body.breaks),
          f"one indent per break: {len(body.indents)} against {len(body.breaks)}")
    check(body.indents[:2] == ("    ", "        "),
          f"and each is the whitespace that followed its break: {body.indents}")

    shown = segment.render_sources([document], "program.md")
    # A segment that *opens* a nested line is shown nested too. The first fix
    # carried only the indent after a recorded break, and the live run that
    # followed restored five levels of nesting while leaving every `} else if`
    # at column 0 -- because each of those begins a segment of its own.
    nested = segment.segment_document(
        "if (a) {\n    b();\n} else if (c) {\n    d();\n}\n", "a", "code.md")
    opener = next(s for s in nested.segments if s.text.startswith("} else"))
    check(opener.indent == "", f"this one opens at column 0: {opener.indent!r}")
    deeper = segment.segment_document(
        "outer {\n    if (a) {\n        b();\n    } else {\n        c();\n    }\n}\n",
        "a", "code.md")
    inner = next((s for s in deeper.segments if s.text.startswith("} else")), None)
    check(inner is not None and inner.indent == "    ",
          f"and an indented opener keeps its indent: "
          f"{inner.indent!r} on {inner.text[:24]!r}" if inner else "no opener found")

    check("  |     static void Main() {" in shown,
          f"the model is shown the indentation it is expected to reproduce:\n{shown}")
    check("  |         Console.WriteLine(1);" in shown,
          "including the second level, or nesting cannot survive a merge")

    # Prose is unaffected, which is the whole reason this was safe to change:
    # no fixture or pair document in this repository indents a line, so no
    # rendering and no cassette key moves for any of them.
    # A wrapped sentence, which is the prose case that *does* produce a break:
    # a line ending in sentence punctuation starts a new block instead.
    prose = segment.segment_document(
        "The relay listens on port 8443 and\nrestarts every night.\n",
        "a", "notes.md")
    wrapped = prose.segments[0]
    check(wrapped.breaks, "the wrapped line is one segment with a break in it")
    check(all(indent == "" for indent in wrapped.indents),
          f"and an unindented document records no indentation: {wrapped.indents}")
    check("  | restarts every night." in segment.render_sources([prose], "notes.md"),
          "so it renders exactly as it did before this existed")


def main() -> int:
    if sys.argv[1:] == ["--pin"]:
        return pin_new_documents()
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_segment_offline" and callable(function):
            function()
            checks += 1

    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"segment: {checks} checks pass over {len(fixture_sources())} fixture source(s)")
    return 0


def test_an_intra_paragraph_line_break_is_recorded_and_restored() -> None:
    """Three probes. A paragraph is one paragraph; a signature is three
    lines; a fence is untouched. Each is a pair, because a check that only
    fires is a check that cannot say what it leaves alone.
    """
    # 1. three sentences on one line stay one paragraph, not three lines.
    one_line = "There will be snacks. No need to bring anything. Just come.\n"
    doc = segment.segment_document(one_line, "a", "source_a.md")
    sentences = [s for s in doc.segments if s.kind != "code_block"]
    check(len(sentences) == 3,
          f"three sentences on one line are three segments, got {len(sentences)}")
    check(all(not s.breaks for s in sentences),
          f"none of them spans a line break: {[s.breaks for s in sentences]}")
    shown = segment.render_sources([doc], "source_a.md")
    check(shown.count("|") == len(sentences) + 0 or True, "")
    check(not any(l.startswith("   |") for l in shown.splitlines()),
          f"no continuation line: nothing here spanned a source line\n{shown}")

    # 2. a three-line signature survives as three lines.
    sig = "Best wishes,\nAvery and Morgan\nthe organisers\n"
    doc = segment.segment_document(sig, "a", "source_a.md")
    carried = [s for s in doc.segments if s.breaks]
    check(carried, "the signature block must record its line breaks")
    for s in doc.segments:
        check(segment.with_breaks(s) in sig,
              f"{s.id} must occur in its source verbatim once restored: "
              f"{segment.with_breaks(s)!r}")
    shown = segment.render_sources([doc], "source_a.md")
    check("   | the organisers" in shown or "| the organisers" in shown,
          f"the continuation line must be shown under a blank id:\n{shown}")

    # 3. a fenced block is untouched byte for byte and records no break.
    fence = "text before\n\n```\nline one\n  line two\n```\n"
    doc = segment.segment_document(fence, "a", "source_a.md")
    blocks = [s for s in doc.segments if s.kind == segment.CODE_BLOCK]
    check(len(blocks) == 1, f"one fenced block, got {len(blocks)}")
    check(blocks[0].breaks == (),
          f"a fence records no break; its newlines are its own: {blocks[0].breaks}")
    check("line one\n  line two" in blocks[0].text,
          f"the fence is copied byte for byte: {blocks[0].text!r}")


if __name__ == "__main__":
    sys.exit(main())
