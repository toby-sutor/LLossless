#!/usr/bin/env python3
"""The fixture pairs, and the audit that says they are answerable.

An earlier comparison tied because the violation every arm produced was an input
property: one byte-identical `title_not_superseded` finding, reproduced by three
models because the fixture left them no other move. A metric measured over an
unsatisfiable construct measures the construct. So before these nine pairs are
scored against anything, this module proves that a correct answer exists:
`ideal.md` is a merge of the two sources that `ideal.json` declares honestly,
and the pair passes if that merge draws **zero findings at both fidelity
levels**. A pair that cannot reach zero is a pair that would charge every arm
equally, and it is a fixture defect, not a model result.

The three properties this module requires, one pair each and named here so a reader
can check the claim rather than take it:

    payroll_cutoff  a genuine title supersession -- the 2025 schedule is
                    replaced by the 2026 one, and both times survive
    loading_dock    correct behaviour requires declaring loss: source B books
                    dock slots by phone on a line source A says is retired
    badge_access    two near-identical documents, so a staple of them scores
                    full coverage -- what the concatenation-immune primary is
                    there to bite on
    rate_limits     the long pair, 9,772 bytes of source against the other
                    six at 1,571-2,109, and the only one carrying non-ASCII
                    characters, kept rather than folded to their ASCII look-alikes

Two more pairs were added on 2026-08-30, after the arms had already been
recorded:

    index_429       a real-article-scale pair whose two Environment sections
                    disagree about scope: one says every release on every
                    platform, the other lists one managed deployment. A merge
                    that takes either alone loses the other
    trace_names     a short near-duplicate pair in support-ticket prose, whose
                    source B states its workaround and its resolution word for
                    word -- the `duplicate` disposition's worked example

They are not in the original denominator. `run_arm.M9_PAIRS` names the seven the arms
ran, so what those arms were measured against did not move when this directory
grew; that boundary was fixed earlier and held again when the two more arrived.

The staple check runs over all nine, because all nine turned out to have the
property: concatenation costs nothing the reconciler can see except the title
and whatever a source states twice. That is the primary's whole basis, so it is
measured rather than assumed.

Run with `python3 tests/test_pairs.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import run_arm  # noqa: E402
import socket_guard  # noqa: E402

# Nothing here opens a socket; the guard is how that is stated.
socket_guard.install()

from llossless import config, parsing, reconcile  # noqa: E402
from llossless.segment import TITLE, segment_document  # noqa: E402

PAIRS = ROOT / "tests" / "pairs"
SOURCES = ("source_a.md", "source_b.md")
LEVELS = ("off", "high")
# The pairs run under the policy the corpus runs under, so the audit answers
# the question the sweep will ask and not an easier one.
POLICY = "keep-base"
BASE = "source_a.md"

# How much room a title-supersession reason needs beside the title it
# quotes: a reason is capped at `parsing.REASON_MAX`, and the shortest useful
# phrasing around a quoted title is a verb and two quotation marks. Sixteen is
# the margin the register was set at, not a measurement of any real reason.
TITLE_HEADROOM = 16

# The non-ASCII characters this corpus keeps, and what a normaliser would fold them to.
NON_ASCII = re.compile(r"[^\x00-\x7f]")
FOLDS = {"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"', "\u2014": "-"}

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def names() -> tuple[str, ...]:
    return tuple(sorted(path.name for path in PAIRS.iterdir() if path.is_dir()))


def sources_of(pair: str) -> dict[str, str]:
    return {name: (PAIRS / pair / name).read_text(encoding="utf-8") for name in SOURCES}


def ideal_of(pair: str) -> tuple[str, tuple[dict, ...]]:
    merged = (PAIRS / pair / "ideal.md").read_text(encoding="utf-8")
    payload = json.loads((PAIRS / pair / "ideal.json").read_text(encoding="utf-8"))
    return merged, tuple(payload["dispositions"])


def test_there_are_nine_pairs_and_each_is_complete() -> None:
    """Nine, and every one of them four files. The denominators depend on it.

    Seven pairs were required at first and two more were added later. The number is asserted
    rather than derived so that a pair appearing stops the suite here, where
    somebody has to re-base the counts below on purpose, instead of quietly
    moving them.
    """
    check(len(names()) == 9, f"the pair corpus is nine directories; found {len(names())}")
    for pair in names():
        for name in (*SOURCES, "ideal.md", "ideal.json"):
            check((PAIRS / pair / name).is_file(), f"{pair}/{name} is missing")


def test_every_pair_carries_two_distinct_source_titles() -> None:
    """One title per source, different from each other, so exactly one
    is not taken -- which is what makes the primary's denominator a-priori."""
    for pair in names():
        titles = []
        for name, text in sources_of(pair).items():
            found = reconcile.titles_of(segment_document(text, name[-4], name).segments)
            check(len(found) == 1, f"{pair}/{name} has {len(found)} titles; expected one")
            titles += [item.text for item in found]
        check(len(set(titles)) == 2,
              f"{pair} has {len(set(titles))} distinct source title(s); expected two")


def test_the_ideal_merge_is_a_well_formed_merge_payload() -> None:
    """`check_merge` first: a payload the parser rejects never reaches the
    reconciler, so a fixture that fails here would be untestable rather than
    failing."""
    for pair in names():
        merged, dispositions = ideal_of(pair)
        errors = parsing.check_merge({"merged_document": merged,
                                      "dispositions": list(dispositions)})
        check(not errors, f"{pair}/ideal.json is not a valid merge payload: {errors}")


def test_the_ideal_merge_draws_no_findings_at_either_level() -> None:
    """The audit itself. Zero findings, `off` and `high`, for all nine.

    Both levels because `off` permits only `superseded` and `duplicate` (plus
    `dropped`, which check 4 exempts unconditionally), so a fixture whose only
    correct answer needs `reworded` or `subsumed` is answerable at `high` and
    unanswerable at `off` -- and the sweep runs both.
    """
    for pair in names():
        merged, dispositions = ideal_of(pair)
        result = reconcile.reconcile(sources_of(pair), merged)
        for level in LEVELS:
            got = reconcile.findings(result, dispositions, fidelity=level,
                                     title_policy=POLICY, base=BASE,
                                     budget=config.DEFAULT_DECLARED_LOSS_BUDGET,
                                     )
            check(not got.findings,
                  f"{pair} at fidelity {level} is not satisfiable: "
                  + "; ".join(f"{f.kind} {f.segment} {f.detail}" for f in got.findings))
            check(not reconcile.over_budget(len(got.declared_drops), got.segments, config.DEFAULT_DECLARED_LOSS_BUDGET),
                  f"{pair} at fidelity {level} declares {len(got.declared_drops)} of "
                  f"{got.segments} dropped, over the budget")


def test_the_ideal_dispositions_are_all_valid_at_the_stricter_level() -> None:
    """Stated as a set rather than left to the level check to imply.

    `off` is the binding constraint, and it admits three values. Writing an
    ideal that used a fourth would be writing a fixture that scores an arm on
    the fidelity slider instead of on the merge.
    """
    allowed = set(reconcile.PERMITTED["off"]) | {"dropped"}
    for pair in names():
        _, dispositions = ideal_of(pair)
        used = {str(record.get("disposition", "")) for record in dispositions}
        check(used <= allowed,
              f"{pair}/ideal.json uses {sorted(used - allowed)}, which fidelity off refuses")


# How many body lines a staple of each pair states twice, character for
# character, so check 9 fires on the staple as well as the title check. Held as
# data rather than derived, because the point of the assertion below is that
# this set cannot change without someone saying so: a pair leaving it would
# silently weaken the staple test.
#
# The name used to be `SHARE_A_LINE` and the comment used to say "share a body
# line between their two sources", which was true of the first three and is not
# true of the fourth. `trace_names` source B states its workaround and its
# resolution in identical words, so a staple repeats that line without the two
# sources sharing anything. What is registered here is the repeat
# count in the staple, whichever side of the pair it came from.
STAPLE_REPEATS = {"badge_access": 9, "loading_dock": 2, "payroll_cutoff": 2,
                  "trace_names": 1}


def test_a_staple_scores_full_coverage_and_costs_the_title_and_its_repeats() -> None:
    """Why the primary is concatenation-immune, measured on these nine.

    Gluing the two sources together retains every source segment character for
    character, so coverage, the verbatim core and the declared-loss budget all
    come back clean. Two things it cannot do: choose between two titles, and
    avoid stating twice anything already stated once. Those are the findings
    left standing, and both are concatenation-immune.

    Check 9 is the second of them. On four of the nine pairs it
    fires on a staple; on the other five nothing is repeated verbatim, so there
    is nothing for it to see. That is a property of this corpus and not of
    stapling, which is why the primary is still the title check and this is
    still a secondary.
    """
    for pair in names():
        documents = sources_of(pair)
        staple = documents[SOURCES[0]].rstrip("\n") + "\n\n" + documents[SOURCES[1]]
        result = reconcile.reconcile(documents, staple)
        check(result.present == result.total,
              f"{pair}: a staple covers {result.present}/{result.total} segments, "
              f"so this pair does not test what the primary is immune to")
        got = reconcile.findings(result, (), fidelity="off", title_policy=POLICY, base=BASE, budget=config.DEFAULT_DECLARED_LOSS_BUDGET)
        kinds = sorted(finding.kind for finding in got.findings)
        repeats = kinds.count(reconcile.DUPLICATED_CONTENT)
        expected = ([reconcile.DUPLICATED_CONTENT] * STAPLE_REPEATS.get(pair, 0)
                    + [reconcile.TITLE_NOT_SUPERSEDED])
        check(kinds == sorted(expected),
              f"{pair}: a staple draws {kinds}; expected {sorted(expected)}")
        check(repeats == STAPLE_REPEATS.get(pair, 0),
              f"{pair}: a staple repeats {repeats} line(s); the registered count is "
              f"{STAPLE_REPEATS.get(pair, 0)}. A pair that stopped repeating a line "
              f"has quietly stopped exercising check 9 against a concatenation.")
    check(set(STAPLE_REPEATS) <= set(names()),
          f"STAPLE_REPEATS names a pair that does not exist: "
          f"{sorted(set(STAPLE_REPEATS) - set(names()))}")


def title_events(pairs: tuple[str, ...]) -> int:
    """Source titles that cannot be the merged title, x the levels. One rule, two callers."""
    events = 0
    for pair in pairs:
        merged, _ = ideal_of(pair)
        chosen = reconcile.titles_of(segment_document(merged, "m", "ideal.md").segments)
        check(len(chosen) == 1, f"{pair}/ideal.md has {len(chosen)} titles; expected one")
        for name, text in sources_of(pair).items():
            for item in segment_document(text, name[-4], name).segments:
                if item.kind == TITLE and item.text != chosen[0].text:
                    events += len(LEVELS)
    return events


def test_the_recorded_denominator_is_still_fourteen_and_the_corpus_is_eighteen() -> None:
    """Two numbers, because there are now two corpora. Counted, not asserted.

    The count is the number of source titles that cannot be the merged title,
    which is fixed by the fixtures before a model is asked anything. That is
    what makes it a-priori: an arm that returns nothing at all still has this
    denominator, so a silent arm scores 0 out of it rather than being excluded.

    **The recorded figure is the one that must not move.** Seven pairs x 2
    levels x 1 title not taken = 14 was registered before any arm ran, and
    every recorded result is a fraction of it. Two pairs were added later to
    this directory, so the second line here is a new number and the first is the
    old one still holding: `run_arm.M9_PAIRS` is what keeps them apart, and this
    is where that separation is checked rather than trusted.
    """
    check(title_events(run_arm.M9_PAIRS) == 14,
          f"the registered arms' a-priori denominator is {title_events(run_arm.M9_PAIRS)}; "
          f"the registration fixed 14 and no later fixture may move it")
    check(title_events(names()) == 18,
          f"the whole corpus's a-priori denominator is {title_events(names())}; "
          f"nine pairs at two levels is 18")
    check(set(run_arm.M9_PAIRS) < set(names()),
          f"run_arm.M9_PAIRS is not a proper subset of tests/pairs/: "
          f"{sorted(set(run_arm.M9_PAIRS) - set(names()))} missing")


def test_no_source_title_comes_near_the_reason_cap() -> None:
    """A title within a reason's length of `REASON_MAX` is a trap.

    A value at exactly the cap is closed at generation time and arrives inside
    well-formed JSON with `finish_reason` still `stop`.
    The natural phrasing of a title-supersession reason quotes the title it
    chose, so a source title at or near the cap clips the reason, `_check_reason`
    rejects the record, and the pair scores `title_not_superseded` for a schema
    reason rather than a model one. That is the run's own primary, fired by the
    fixture.

    The pair that first hit this was `rate_limits`, whose source A arrived at
    exactly 80 and was shortened to 56 with the human's approval. That document
    has since been withdrawn and its replacement was written to the
    same ceiling. The margin below is what keeps a later fixture from
    reintroducing the trap in silence; it is not a claim about any real reason's
    length, only about the room one has to work in.
    """
    ceiling = parsing.REASON_MAX - TITLE_HEADROOM
    for pair in names():
        for name, text in sources_of(pair).items():
            for item in reconcile.titles_of(segment_document(text, name[-4], name).segments):
                check(len(item.text) <= ceiling,
                      f"{pair}/{name}'s title is {len(item.text)} characters, within "
                      f"{TITLE_HEADROOM} of REASON_MAX ({parsing.REASON_MAX}); a reason "
                      f"quoting it would be clipped at generation and read as a finding")


def test_non_ascii_survives_segmentation_and_the_comparison() -> None:
    """This corpus keeps the supplied text's non-ASCII rather than folding it.

    Three places a normaliser could sit, so three claims. Segmentation returns
    every codepoint it was given; `flatten` is whitespace-only and returns them
    too; and the comparison the reconciler runs is byte-sensitive about them, so
    a fold anywhere upstream shows up as findings rather than passing silently.

    The third is the one worth having. The em dashes and curly quotes are not
    invariant-core spans -- those are numerics, code, links and paths -- so a
    fold does not read as a verbatim violation. It reads as coverage loss and
    unresolved replacements, which is a harder thing to trace back to its cause
    once an arm is recorded.
    """
    for pair in names():
        for name, text in sources_of(pair).items():
            want = Counter(NON_ASCII.findall(text))
            segments = segment_document(text, name[-4], name).segments
            got = Counter(character for item in segments
                          for character in NON_ASCII.findall(reconcile.flatten(item.text)))
            for character, count in want.items():
                check(got[character] == count,
                      f"{pair}/{name} has {count} U+{ord(character):04X} but "
                      f"{got[character]} survive segmentation and flatten")

    # The negative direction, on the one pair that has the characters to lose.
    documents = sources_of("rate_limits")
    merged, dispositions = ideal_of("rate_limits")
    folded = merged
    for character, plain in FOLDS.items():
        folded = folded.replace(character, plain)
    check(folded != merged, "rate_limits/ideal.md carries no non-ASCII to fold")
    got = reconcile.findings(reconcile.reconcile(documents, folded), dispositions,
                             fidelity="off", title_policy=POLICY, base=BASE,
                             budget=config.DEFAULT_DECLARED_LOSS_BUDGET,
                             )
    check(bool(got.findings),
          "folding rate_limits' non-ASCII to its ASCII lookalikes draws no findings, "
          "so the comparison is not byte-sensitive about them and a normalising step "
          "anywhere in the pipeline would pass unnoticed")


def test_a_duplicate_record_names_a_byte_identical_segment() -> None:
    """`prompts/fidelity/off.merge.md` states the rule; this is where it is checked.

    At `off`, duplicate requires the two segments to be identical character for
    character apart from surrounding whitespace -- which is what separates it
    from superseded, where a version was chosen between two that differ. An
    ideal merge that used duplicate loosely would be teaching the looser reading
    to everything scored against it.
    """
    for pair in names():
        sources = sources_of(pair)
        texts = [item.text.strip()
                 for name, text in sources.items()
                 for item in segment_document(text, name[-4], name).segments]
        by_id = {item.id: item
                 for name, text in sources.items()
                 for item in segment_document(text, name[-4], name).segments}
        for record in ideal_of(pair)[1]:
            if str(record.get("disposition", "")) != "duplicate":
                continue
            item = by_id.get(str(record.get("segment", "")))
            check(item is not None and texts.count(item.text.strip()) > 1,
                  f"{pair}/{record.get('segment')} is declared duplicate, but no other "
                  f"source segment is byte-identical to it")


def test_pairs_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_pairs_offline" and callable(function):
            function()
            checks += 1

    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    segments = sum(
        len(segment_document(text, name[-4], name).segments)
        for pair in names() for name, text in sources_of(pair).items()
    )
    print(f"pairs: {checks} checks pass over {len(names())} pair(s), {segments} source segments")
    return 0


if __name__ == "__main__":
    sys.exit(main())
