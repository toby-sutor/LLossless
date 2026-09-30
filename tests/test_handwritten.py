#!/usr/bin/env python3
"""Shape checks for `tests/handwritten/`, and the boundaries it must not cross.

The corpus is nineteen document pairs a person wrote by hand, fifteen with a
`reference.md` the same person wrote. What makes it worth having is exactly
what makes it dangerous to wire in carelessly: these merges break rules the
other two corpora keep. `sepia/reference.md` is a byte concatenation and
`treecreeper/reference.md` is a three-way one -- the defect `reconcile`'s
staple predicate exists to catch -- and `curry`'s reference drops 22 of 60
segments. Two pairs, `treecreeper` and `mahjongg`, carry three sources rather
than two, named `source_a.md` through `source_c.md`.

So this module checks two different things:

  1. that every pair is complete and its `meta.json` says what it is, and
  2. that admitting the corpus moved no registered denominator and put
     nothing into a control set that is registered by name.

The second half is the one that matters. `tests/test_pairs.py:123` pins nine
pairs, `tests/test_merge.py:1074` pins sixteen fixtures, and
`tests/test_reconcile.py:1595` and `:1819` pin their union at twenty-five with
the staple predicate registered as firing on exactly two of them. A corpus
added to any of those globs would void a registration rather than fail a test,
which is the quiet kind of wrong.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless import reconcile  # noqa: E402
from llossless.segment import segment_document, SENTENCE  # noqa: E402

CORPUS = ROOT / "tests" / "handwritten"
# Every pair has at least these two. `treecreeper` and `mahjongg` also have a
# third; CANONICAL_SOURCES is the full run a pair's sources must be a
# contiguous prefix of, checked by source_files() below.
SOURCES = ("source_a.md", "source_b.md")
CANONICAL_SOURCES = ("source_a.md", "source_b.md", "source_c.md")

# What `sepia/reference.md` puts between the two documents it staples
# together. A blank line, which is why the byte count is two over the sum of
# the sources and not equal to it.
JOINER = b"\n\n"
KINDS = ("merge", "refusal")
META_REQUIRED = ("pair", "kind", "description", "origin")
ORIGIN_REQUIRED = ("source_a", "source_b", "reference")

# Registered elsewhere, restated here so that admitting a pair to the wrong
# directory fails in the module that did the admitting.
PAIRS_COUNT = 9
FIXTURES_COUNT = 16
CONTROLS_COUNT = 25

failures: list[str] = []
notes: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def names() -> list[str]:
    return sorted(p.name for p in CORPUS.iterdir() if p.is_dir())


def meta(pair: str) -> dict:
    return json.loads((CORPUS / pair / "meta.json").read_text(encoding="utf-8"))


def source_files(pair: str) -> list[str]:
    """The pair's own source filenames, in canonical order, as found on disk.

    Two sources for every pair but `treecreeper` and `mahjongg`, which have
    three. Reading the glob rather than assuming `SOURCES` is what lets the
    rest of this module -- and anything that iterates a pair's sources the
    same way -- see a third source instead of silently merging only two.
    """
    return sorted(p.name for p in (CORPUS / pair).glob("source_*.md"))


def test_every_pair_is_complete_and_declares_what_it_is() -> None:
    for pair in names():
        here = CORPUS / pair
        for name in SOURCES + ("meta.json",):
            check((here / name).is_file(), f"{pair}: {name} is missing")
        if not (here / "meta.json").is_file():
            continue
        payload = meta(pair)
        for field in META_REQUIRED:
            check(field in payload, f"{pair}: meta.json has no {field!r}")
        check(payload.get("pair") == pair,
              f"{pair}: meta.json names {payload.get('pair')!r}")
        check(payload.get("kind") in KINDS,
              f"{pair}: kind {payload.get('kind')!r} is not one of {KINDS}")
        check(bool(str(payload.get("description", "")).strip()),
              f"{pair}: description is empty, so nothing records what this pair is")
        origin = payload.get("origin", {})
        for field in ORIGIN_REQUIRED:
            check(field in origin,
                  f"{pair}: origin has no {field!r}; the original filename is the "
                  f"only link back to the operator's own copy")
        # `treecreeper` and `mahjongg` name a third source in origin too; a
        # two-source pair names no more than that. Either direction of
        # mismatch -- a source on disk origin does not mention, or an origin
        # entry for a source that is not there -- loses the link back to the
        # operator's own copy just as silently as a missing field does.
        on_disk = {Path(name).stem for name in source_files(pair)}
        in_origin = {key for key in origin if key.startswith("source_")}
        check(on_disk == in_origin,
              f"{pair}: sources on disk are {sorted(on_disk)}, origin names "
              f"{sorted(in_origin)}")


def test_a_reference_is_present_exactly_when_the_pair_is_mergeable() -> None:
    """`kind` is not decoration: it says whether a correct answer exists.

    A `refusal` pair has no reference because the correct output is a declined
    merge, and `meta.json`'s description is the operator's statement of why.
    Writing one for it would be inventing an answer key, which is the thing
    this corpus is here to avoid.
    """
    for pair in names():
        kind = meta(pair).get("kind")
        present = (CORPUS / pair / "reference.md").is_file()
        check(present == (kind == "merge"),
              f"{pair}: kind={kind!r} but reference.md "
              f"{'exists' if present else 'is missing'}")


def test_the_refusal_pairs_keep_the_operators_own_words() -> None:
    """The description of a refusal is evidence, not a summary of evidence.

    These four sentences are the only statement anywhere of what the right
    answer is for a pair that should not be merged. Paraphrasing one would
    quietly replace the operator's judgement with mine.
    """
    refusals = [p for p in names() if meta(p).get("kind") == "refusal"]
    check(len(refusals) == 4,
          f"expected four refusal pairs, got {len(refusals)}: {refusals}")
    for pair in refusals:
        text = meta(pair)["description"]
        check("not be merged" in text or "refuse" in text,
              f"{pair}: the description no longer says the merge should be "
              f"declined, which is the whole content of this pair: {text!r}")


def test_admitting_the_corpus_moved_no_registered_count() -> None:
    """The three denominators this corpus was kept out of.

    Each is asserted in its own module too. They are repeated here because the
    failure mode is additive: somebody promotes a pair, the count moves, and
    the module that owns the count is the one that goes red -- a long way from
    the change that caused it.
    """
    pairs = sorted(p for p in (ROOT / "tests" / "pairs").iterdir() if p.is_dir())
    fixtures = sorted(p for p in (ROOT / "tests" / "fixtures").iterdir() if p.is_dir())
    check(len(pairs) == PAIRS_COUNT,
          f"tests/pairs/ holds {len(pairs)}, registered at {PAIRS_COUNT}")
    check(len(fixtures) == FIXTURES_COUNT,
          f"tests/fixtures/ holds {len(fixtures)}, registered at {FIXTURES_COUNT}")

    controls = sorted((ROOT / "tests" / "pairs").glob("*/ideal.md"))
    controls += sorted((ROOT / "tests" / "fixtures").glob("*/merged.md"))
    check(len(controls) == CONTROLS_COUNT,
          f"the check-9 and staple control set holds {len(controls)}, "
          f"registered at {CONTROLS_COUNT} in tests/test_reconcile.py:1595")
    # Globbing `pairs/` and `fixtures/` and then looking for a hand-written
    # file among the results would be a tautology -- it cannot be there. The
    # way this actually goes wrong is somebody widening the glob in
    # `test_reconcile.py` itself, so the assertion is over that file's source.
    owner = (ROOT / "tests" / "test_reconcile.py").read_text(encoding="utf-8")
    check("handwritten" not in owner,
          "tests/test_reconcile.py now mentions the hand-written corpus. Its "
          "control set is registered as firing the staple predicate on exactly "
          "two members (:1829); sepia/reference.md and treecreeper/reference.md "
          "are both staples and would make it four, which voids the "
          "registration rather than failing it.")


def test_sepia_is_the_staple_the_registration_would_have_caught() -> None:
    """The must-fire half: the hazard is real, not hypothetical.

    `test_admitting_the_corpus_moved_no_registered_count` asserts that no
    hand-written document is in the control set. On its own that is
    indistinguishable from the predicate having been broken, so this end
    proves the exclusion is load-bearing: run the same predicate on
    `sepia/reference.md` directly and it fires.
    """
    here = CORPUS / "sepia"
    documents = {name: (here / name).read_text(encoding="utf-8") for name in SOURCES}
    result = reconcile.reconcile(documents, (here / "reference.md").read_text(encoding="utf-8"))
    check(result.order.stapled,
          "sepia/reference.md no longer reads as a staple. Either the document "
          "changed or the predicate did; until that is understood, the "
          "exclusion above is asserting nothing.")
    # Asserted, not printed. The note below said "9,211 = 3,408 + 5,801" in
    # `meta.json`, and that sum is 9,209: the two
    # newlines that join the documents are the difference. The figures were
    # in this function the whole time, in a `notes.append` nothing compares.
    # A concatenation is the one claim about this file that a reader
    # can check without reading it, so it is the one that has to hold.
    sizes = tuple(len(documents[n].encode()) for n in SOURCES)
    reference = (here / "reference.md").read_bytes()
    total = len(reference)
    joined = documents[SOURCES[0]].encode() + JOINER + documents[SOURCES[1]].encode()
    check(reference == joined,
          f"sepia/reference.md is no longer source_a + {JOINER!r} + source_b, "
          f"so the arithmetic below describes a file that no longer exists")
    check(total == sum(sizes) + len(JOINER),
          f"sepia: {total:,} bytes against {sizes[0]:,} + {sizes[1]:,} = "
          f"{sum(sizes):,} plus {len(JOINER)} joining byte(s)")
    notes.append(f"sepia: reference {total:,} bytes against sources "
                 f"{sizes[0]:,} + {sizes[1]:,} = {sum(sizes):,}, plus the "
                 f"{len(JOINER)} newline(s) that join them")


def test_treecreeper_is_also_a_staple() -> None:
    """The second must-fire: `treecreeper/reference.md` is a staple too.

    Found while adding the three-source pairs, and now stated in both
    `treecreeper/meta.json` and `README.md`. `reconcile.reconcile` reads the
    reference as its three sources joined in source order under their own
    headings -- `order.stapled` fires and `order.runs` is 3, one run per
    source, the three-source shape of what sepia's two-source test above
    checks.
    """
    here = CORPUS / "treecreeper"
    sources = source_files("treecreeper")
    documents = {name: (here / name).read_text(encoding="utf-8") for name in sources}
    result = reconcile.reconcile(documents, (here / "reference.md").read_text(encoding="utf-8"))
    check(result.order.stapled,
          "treecreeper/reference.md no longer reads as a staple, so "
          "meta.json and README.md both need correcting, not just this test")
    check(result.order.runs == 3,
          f"treecreeper: order.runs is {result.order.runs}, expected 3 -- "
          f"one run per source")


def test_mahjongg_is_not_read_as_a_staple() -> None:
    """The must-not-fire half beside treecreeper's must-fire.

    `mahjongg/meta.json` states that every one of `reference.md`'s sentences
    is verbatim from some source (179/179, measured with the same segmenter
    `test_every_source_survives_segmentation` uses) and yet, unlike sepia and
    treecreeper, `order.stapled` does not fire for it: the reference reorders
    its sources' sections rather than keeping source order. If that ever
    flips, the contrast `meta.json` draws with treecreeper is wrong and needs
    rewriting, not a silently stale claim.
    """
    here = CORPUS / "mahjongg"
    sources = source_files("mahjongg")
    documents = {name: (here / name).read_text(encoding="utf-8") for name in sources}
    result = reconcile.reconcile(documents, (here / "reference.md").read_text(encoding="utf-8"))
    check(not result.order.stapled,
          "mahjongg/reference.md now reads as a staple, so meta.json's "
          "contrast with treecreeper is no longer accurate")
    check(result.order.runs == 3,
          f"mahjongg: order.runs is {result.order.runs}, expected 3 -- one "
          f"run per source, even though source order is not kept")


def _normalise_notation(text: str) -> str:
    """Collapse whitespace and drop heading markers, for a verbatim check.

    The same normalisation `tests/analyse_merges.py:normalise` applies, kept
    local here rather than imported so this module has no dependency on a
    file outside `tests/handwritten/` and `tests/test_handwritten.py`.
    """
    return " ".join(text.replace("#", " ").split())


def test_mahjongg_reference_sentences_are_all_verbatim() -> None:
    """The 179/179 figure `meta.json` states.

    `meta.json`'s claim that mahjongg carries no seeded errors rests on this:
    every sentence of `reference.md` -- `segment.SENTENCE`, the unit
    `test_every_source_survives_segmentation` already uses -- traces
    verbatim, whitespace-normalised, to at least one source. A number cited
    in two files and checked in neither is exactly the quiet kind of wrong
    `test_admitting_the_corpus_moved_no_registered_count`'s docstring warns
    about for counts; this is that same warning applied to a count of
    sentences instead of directories.
    """
    here = CORPUS / "mahjongg"
    reference = (here / "reference.md").read_text(encoding="utf-8")
    doc = segment_document(reference, reconcile.MERGE_LETTER)
    sentences = [s.text for s in doc.segments if s.kind == SENTENCE]
    sources_norm = [_normalise_notation((here / name).read_text(encoding="utf-8"))
                     for name in source_files("mahjongg")]
    present = sum(1 for s in sentences
                  if any(_normalise_notation(s) in hay for hay in sources_norm))
    check(len(sentences) == 179,
          f"mahjongg/reference.md now segments to {len(sentences)} sentences, "
          f"not the 179 meta.json states")
    check(present == len(sentences),
          f"mahjongg: {present}/{len(sentences)} reference sentences are "
          f"verbatim in some source, not all of them as meta.json states")
    notes.append(f"mahjongg: {present}/{len(sentences)} reference sentences "
                 f"verbatim in some source")


def test_no_reference_is_read_as_an_answer_key() -> None:
    """A `reference.md` may be scored against, never scored as correct.

    `tests/measure_merges.py` decides whether a corpus has a reference by
    looking for `merged.md`, and this corpus deliberately has none of those --
    the file is called `reference.md` precisely so that `measure_merges.py` does
    not pick it up as ground truth. If a `merged.md` ever appears here, that
    protection is gone silently.
    """
    strays = sorted(p for p in CORPUS.glob("*/merged.md"))
    check(not strays,
          f"{strays} would be read as an answer key by measure_merges.py; this "
          f"corpus names its references reference.md for that reason")
    strays = sorted(CORPUS.glob("*/ideal.md")) + sorted(CORPUS.glob("*/expected.json"))
    check(not strays, f"{strays} belong to tests/pairs/ and tests/fixtures/")


def test_every_source_survives_segmentation() -> None:
    """These are real documents, so they carry what invented ones do not.

    Two of them are code, one is German, one is a 9k concatenation. If any
    of that cannot be segmented the corpus cannot be measured at all, and the
    failure would otherwise turn up inside a scored run. Iterates
    `source_files(pair)` rather than the fixed two-source `SOURCES`, so
    `treecreeper` and `mahjongg`'s third source is checked too.
    """
    for pair in names():
        for name in source_files(pair):
            text = (CORPUS / pair / name).read_text(encoding="utf-8")
            result = segment_document(text, reconcile.MERGE_LETTER)
            check(bool(result.segments),
                  f"{pair}/{name} segments to nothing")


def test_sources_are_named_contiguously() -> None:
    """`source_a`, `source_b`, then optionally `source_c` -- never a gap.

    `segment.document_letter` reads a segment's letter straight from its
    source filename. A pair holding `source_a.md` and `source_c.md` with no
    `source_b.md` would still segment without error, just under the wrong
    letter for the second document -- silent, and exactly the kind of thing
    `test_every_source_survives_segmentation` cannot catch because it only
    checks that segmentation succeeds, not that it is labelled correctly.
    """
    for pair in names():
        found = tuple(source_files(pair))
        expected = CANONICAL_SOURCES[:len(found)]
        check(found == expected,
              f"{pair}: sources on disk are {found}, not a contiguous prefix "
              f"of {CANONICAL_SOURCES}")


def test_no_reference_credits_a_source_with_what_it_does_not_say() -> None:
    """The invented-attribution must-not-fire, over the one corpus `test_reconcile.py` may not read.

    Every reference is a merge a person wrote and checked, so a misattribution
    reported in one is the check being wrong about a correct document.
    """
    from llossless import reconcile

    for folder in sorted(p for p in CORPUS.iterdir() if p.is_dir()):
        if not (folder / "reference.md").is_file():
            continue
        sources = {p.name: p.read_text(encoding="utf-8")
                   for p in sorted(folder.glob("source_*.md"))}
        found = reconcile.attribution_findings(
            sources, (folder / "reference.md").read_text(encoding="utf-8"))
        check(not found, f"{folder.name}/reference.md fired: "
                         f"{[finding.detail for finding in found]}")


def main() -> int:
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and not k.endswith("_offline")]
    for test in tests:
        test()
    for note in notes:
        print(f"note: {note}")
    if failures:
        print(f"handwritten: FAILED ({len(failures)} failing)")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    merges = sum(1 for p in names() if meta(p).get("kind") == "merge")
    print(f"handwritten: {len(tests)} checks pass over {len(names())} pair(s) "
          f"({merges} with a reference, {len(names()) - merges} refusals)")
    return 0


def test_handwritten_offline() -> None:
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
