#!/usr/bin/env python3
"""The six audience-coherence pairs, and the audit that says they are the
fixture the check does not exist for yet.

An earlier write-up names a defect the recorded corpus caught by accident and
scored as a pass: arm C's `bike_docks` at `off` welds a support-desk procedure
under a field-crew title, loses nothing, declares nothing, and comes back clean
on every metric the reconciler rewards. One example is not a corpus. The design
calls for two pairs of the shape that must fire and one of each of the four
shapes that must not, and that is what is here.

**These pairs are not in `tests/pairs/`, and the reason is arithmetic.** The
primary denominator is 7 pairs x 2 levels x 1 title not taken = 14, registered
before any arm ran and asserted in `tests/test_pairs.py`. Adding six pairs
there would make that 26 and would retroactively change what the recorded
arms were measured against.

A later change has since added two pairs to `tests/pairs/` and kept the recorded
denominator at 14 by naming the original seven in `tests/run_arm.py` as `M9_PAIRS`.
That mechanism did not exist when the reasoning above was written, so the
arithmetic above is no longer the reason these six live here - the reason now
is that they are a different corpus with a different question and a fifth
file, `inverted.md`, that `tests/pairs/` has no place for. That conclusion
stands; its argument was replaced rather than repeated.

What this module can and cannot check today:

    the ideal merge is answerable       checked, same audit as test_pairs.py
    the inverted merge is answerable    checked -- and that is the finding
    the inverted merge is wrong         NOT checked; no predicate exists

The middle line is the point. `inverted.md` instructs an on-call engineer to
approve customer communications, and a courier to break a tamper seal their own
document forbids them to touch, and the reconciler returns zero findings at both
fidelity levels on both of them. This module asserts that blindness rather than
working around it, so that the day a predicate is written the assertion fails
here first and whoever wrote it has to come and say what changed.

Run with `python3 tests/test_attribution.py`, or collect with pytest.
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

from llossless import config, parsing, reconcile  # noqa: E402
from llossless.segment import segment_document  # noqa: E402

PAIRS = ROOT / "tests" / "attribution"
SOURCES = ("source_a.md", "source_b.md")
LEVELS = ("off", "high")
POLICY = "keep-base"
BASE = "source_a.md"

# The recommended shape mix, held as data so that dropping a shape has to be a
# deliberate edit here. Two that must fire is the two-event floor
# applied to fixtures: one pair firing is not evidence a predicate works.
EXPECTED_SHAPES = [1, 1, 6, 7, 8, 9]

# The same margin test_pairs.py uses.
TITLE_HEADROOM = 16

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def names() -> tuple[str, ...]:
    return tuple(sorted(p.name for p in PAIRS.iterdir() if p.is_dir()))


def sources_of(pair: str) -> dict[str, str]:
    return {name: (PAIRS / pair / name).read_text(encoding="utf-8") for name in SOURCES}


def shape_of(pair: str) -> dict:
    return json.loads((PAIRS / pair / "shape.json").read_text(encoding="utf-8"))


def merge_of(pair: str, stem: str) -> tuple[str, tuple[dict, ...]]:
    merged = (PAIRS / pair / f"{stem}.md").read_text(encoding="utf-8")
    payload = json.loads((PAIRS / pair / f"{stem}.json").read_text(encoding="utf-8"))
    return merged, tuple(payload["dispositions"])


def merges_of(pair: str) -> tuple[str, ...]:
    """Every merged document this pair carries. The inverted one only exists on
    the pairs that have something to invert."""
    return ("ideal", "inverted") if (PAIRS / pair / "inverted.md").is_file() else ("ideal",)


def test_there_are_six_pairs_and_each_is_complete() -> None:
    check(len(names()) == 6,
          f"the attribution audit asks for six pairs; found {len(names())}")
    for pair in names():
        wanted = [*SOURCES, "ideal.md", "ideal.json", "shape.json"]
        if shape_of(pair)["must_fire"]:
            wanted += ["inverted.md", "inverted.json"]
        for name in wanted:
            check((PAIRS / pair / name).is_file(), f"{pair}/{name} is missing")


def test_the_shapes_are_the_recommended_ones() -> None:
    """Two that must fire, four controls, and the controls are all different.

    A corpus of six positives would prove a predicate fires and nothing about
    what it fires on; four distinct controls is what makes silence readable.
    """
    got = sorted(shape_of(pair)["shape"] for pair in names())
    check(got == EXPECTED_SHAPES,
          f"shapes present are {got}; the audit recommends {EXPECTED_SHAPES}")
    firing = [pair for pair in names() if shape_of(pair)["must_fire"]]
    check(len(firing) == 2,
          f"{len(firing)} pair(s) must fire; the two-event floor needs exactly 2")
    for pair in names():
        must = shape_of(pair)["must_fire"]
        check(must == (shape_of(pair)["shape"] == 1),
              f"{pair} sets must_fire={must} on shape {shape_of(pair)['shape']}; "
              "only shape 1 fires")


def test_every_pair_carries_two_distinct_source_titles() -> None:
    for pair in names():
        titles = []
        for name, text in sources_of(pair).items():
            found = reconcile.titles_of(segment_document(text, name[-4], name).segments)
            check(len(found) == 1, f"{pair}/{name} has {len(found)} titles; expected one")
            titles += [item.text for item in found]
        check(len(set(titles)) == 2,
              f"{pair} has {len(set(titles))} distinct source title(s); expected two")


def test_no_source_title_comes_near_the_reason_cap() -> None:
    """A title long enough to clip the reason that quotes
    it turns a fixture into a test of `REASON_MAX`."""
    ceiling = parsing.REASON_MAX - TITLE_HEADROOM
    for pair in names():
        for name, text in sources_of(pair).items():
            for item in reconcile.titles_of(segment_document(text, name[-4], name).segments):
                check(len(item.text) <= ceiling,
                      f"{pair}/{name}'s title is {len(item.text)} characters, within "
                      f"{TITLE_HEADROOM} of REASON_MAX ({parsing.REASON_MAX})")


def test_every_merged_document_is_a_well_formed_payload() -> None:
    for pair in names():
        for stem in merges_of(pair):
            merged, dispositions = merge_of(pair, stem)
            errors = parsing.check_merge({"merged_document": merged,
                                          "dispositions": list(dispositions)})
            check(not errors, f"{pair}/{stem}.json is not a valid merge payload: {errors}")


def test_the_ideal_merge_draws_no_findings_at_either_level() -> None:
    """The answerability audit, unchanged from `test_pairs.py`. A pair whose
    correct answer cannot reach zero would charge every arm equally."""
    for pair in names():
        merged, dispositions = merge_of(pair, "ideal")
        result = reconcile.reconcile(sources_of(pair), merged)
        for level in LEVELS:
            got = reconcile.findings(result, dispositions, fidelity=level,
                                     title_policy=POLICY, base=BASE,
                                     budget=config.DEFAULT_DECLARED_LOSS_BUDGET,
                                     )
            check(not got.findings,
                  f"{pair}/ideal.md at fidelity {level} is not satisfiable: "
                  + "; ".join(f"{f.kind} {f.segment} {f.detail}" for f in got.findings))
            check(not reconcile.over_budget(len(got.declared_drops), got.segments, config.DEFAULT_DECLARED_LOSS_BUDGET),
                  f"{pair}/ideal.md at {level} declares {len(got.declared_drops)} of "
                  f"{got.segments} dropped, over the budget")


def test_the_dispositions_are_all_valid_at_the_stricter_level() -> None:
    allowed = set(reconcile.PERMITTED["off"]) | {"dropped"}
    for pair in names():
        for stem in merges_of(pair):
            _, dispositions = merge_of(pair, stem)
            used = {str(record.get("disposition", "")) for record in dispositions}
            check(used <= allowed,
                  f"{pair}/{stem}.json uses {sorted(used - allowed)}, refused at off")


def test_the_inverted_merge_is_the_defect_and_scores_clean() -> None:
    """The finding this corpus exists to record, asserted rather than described.

    `inverted.md` is the same union of the same two documents as `ideal.md`,
    minus the headings that say whose each half is. It loses nothing, invents
    nothing, declares its title honestly, and comes back with **zero findings at
    both fidelity levels** - while telling its stated reader to do a thing they
    are not authorised to do. That is `bike_docks` reproduced deliberately.

    This assertion is expected to fail the day an audience predicate lands, and
    failing here is the correct behaviour: the plan puts the predicate after
    the pairs, so the pairs have to be able to notice
    it arriving.
    """
    for pair in names():
        if not shape_of(pair)["must_fire"]:
            continue
        documents = sources_of(pair)
        merged, dispositions = merge_of(pair, "inverted")
        result = reconcile.reconcile(documents, merged)
        # Measured against the ideal merge rather than against `total`: both
        # leave the superseded source title out of the body, which is correct
        # and declared. The claim is that the inversion loses nothing the
        # correct merge does not also lose, so coverage cannot separate them.
        ideal = reconcile.reconcile(documents, merge_of(pair, "ideal")[0])
        check(result.present == ideal.present == result.total - 1,
              f"{pair}/inverted.md covers {result.present}/{result.total} against "
              f"the ideal merge's {ideal.present}; an inversion that loses content "
              "is caught by coverage and does not demonstrate the gap")
        for level in LEVELS:
            got = reconcile.findings(result, dispositions, fidelity=level,
                                     title_policy=POLICY, base=BASE,
                                     budget=config.DEFAULT_DECLARED_LOSS_BUDGET,
                                     )
            check(not got.findings,
                  f"{pair}/inverted.md at {level} now draws "
                  + "; ".join(f"{f.kind} {f.segment}" for f in got.findings)
                  + " -- if a new check did that deliberately, move this pair to the "
                    "positive side of the audit and record why")


def test_the_giveaway_sentence_belongs_to_the_other_audience() -> None:
    """What makes an inversion an inversion, checked against the files.

    The sentence `shape.json` names has to be in the merged document, and it has
    to have come from the source whose title was **not** taken. A giveaway that
    is in the title's own document is not an inversion, it is a document being
    itself, and the pair would be scoring the predicate on nothing.
    """
    for pair in names():
        shape = shape_of(pair)
        if not shape["must_fire"]:
            continue
        giveaway = reconcile.flatten(shape["giveaway"])
        documents = sources_of(pair)
        merged, _ = merge_of(pair, shape["merged_under_audit"].replace(".md", ""))
        check(giveaway in reconcile.flatten(merged),
              f"{pair}: the giveaway sentence is not in {shape['merged_under_audit']}")
        other = SOURCES[1] if BASE == SOURCES[0] else SOURCES[0]
        in_base = giveaway in reconcile.flatten(documents[BASE])
        in_other = giveaway in reconcile.flatten(documents[other])
        check(in_other and not in_base,
              f"{pair}: the giveaway is in {BASE}={in_base} {other}={in_other}; "
              "it must come from the source whose title was not taken")


def test_no_finding_kind_claims_to_do_this_yet() -> None:
    """An old rule, applied forwards for once.

    The three instances of that pattern were all found after the fact. This is
    the same class of mistake caught before it happens: if a finding kind
    appears whose name suggests it answers the audience question, either it does
    - in which case the two inverted merges above should be firing and the
    assertion there will already have failed - or it does not, and the name is
    the misleading part.
    """
    claimed = [kind for kind in reconcile.FINDING_KINDS
               if any(word in kind for word in ("audience", "scope", "coheren"))]
    check(not claimed,
          f"{claimed} names an audience or scope check. If it is real, the "
          "inverted merges must fire and this corpus moves to the positive side; "
          "if it is not, rename it: a name must not claim a check that does not run.")


def test_the_two_firing_pairs_are_two_different_defects() -> None:
    """Shape 1 is two defects, and a predicate that catches one is not half done.

    `sample_intake` is a self-contradiction: the merged document forbids what it
    instructs, and both sentences are in it. Nothing outside the text is needed
    to see that. `incident_pager` is an authority mismatch: no sentence
    contradicts another, and the only thing wrong is that the stated reader
    lacks the standing to do what the document tells them to do - a fact that is
    in neither source and comes from knowing what an on-call engineer is.

    Without this split a predicate scoring 1 of 2 reads as a coin flip. With it,
    which one it caught is the finding.
    """
    firing = [pair for pair in names() if shape_of(pair)["must_fire"]]
    kinds = sorted(shape_of(pair)["defect"] for pair in firing)
    check(len(set(kinds)) == len(firing),
          f"the {len(firing)} firing pairs carry defects {kinds}; two pairs of "
          "one defect is one example twice, not two events")
    needs = sorted(pair for pair in firing
                   if shape_of(pair)["audience_model_required"])
    check(len(needs) == 1,
          f"{len(needs)} of {len(firing)} firing pairs need an audience model; "
          "one of each is the point - a checker that reads only the merged text "
          "should catch exactly one of them, and which one is diagnostic")


def test_the_inversion_differs_from_the_ideal_in_one_variable() -> None:
    """`inverted.md` is `ideal.md` with the heading qualifiers stripped. Only.

    They used to differ in section order as well, which left a predicate free to
    score on order and call it audience coherence. Same line count, and every
    line that differs is a `##` heading whose ideal form is the inverted form
    plus a trailing parenthesis. Anything else - a reordered section, an edited
    sentence, a heading renamed rather than qualified - fails here.
    """
    for pair in names():
        if not shape_of(pair)["must_fire"]:
            continue
        ideal = merge_of(pair, "ideal")[0].splitlines()
        inverted = merge_of(pair, "inverted")[0].splitlines()
        check(len(ideal) == len(inverted),
              f"{pair}: ideal.md has {len(ideal)} lines and inverted.md "
              f"{len(inverted)}; the inversion may only strip qualifiers")
        differing = [(n, a, b) for n, (a, b)
                     in enumerate(zip(ideal, inverted), start=1) if a != b]
        check(bool(differing), f"{pair}: inverted.md is identical to ideal.md")
        for n, ideal_line, inverted_line in differing:
            check(ideal_line.startswith("## ") and inverted_line.startswith("## "),
                  f"{pair}:{n} differs outside a heading: "
                  f"{inverted_line!r} against {ideal_line!r}")
            check(ideal_line.startswith(inverted_line)
                  and ideal_line[len(inverted_line):].startswith(" ("),
                  f"{pair}:{n} is not a stripped qualifier: "
                  f"{inverted_line!r} against {ideal_line!r}")
        check("only)" not in "\n".join(inverted),
              f"{pair}: inverted.md still marks a section for its reader")


def test_the_two_payloads_are_byte_identical_where_both_exist() -> None:
    """The corpus's central claim, guarded rather than frozen.

    `ideal.json` and `inverted.json` say the same thing because the honest merge
    and the defective one declare the same thing: one `superseded` record for
    source B's title, which both of them supersede. That withdrew the claim
    that honesty costs declarations on the strength of this. It was unguarded
    when it was written, which is how the opposite claim survived a commit.

    If a later edit makes them differ, that is not necessarily wrong - but it
    ends the argument above, and this is where it should be noticed.
    """
    for pair in names():
        if not shape_of(pair)["must_fire"]:
            continue
        ideal = (PAIRS / pair / "ideal.json").read_bytes()
        inverted = (PAIRS / pair / "inverted.json").read_bytes()
        check(ideal == inverted,
              f"{pair}: ideal.json and inverted.json differ. The inversion now "
              "declares something the honest merge does not, or the reverse, so "
              "the measurement this corpus was built on no longer holds and needs redoing")


def test_the_only_uncovered_segment_is_the_superseded_title() -> None:
    """What the coverage denominator is, and what the one gap in it is.

    `total` is every segment of both sources - 15 + 14 for `incident_pager`,
    14 + 14 for `sample_intake` - so a merge that keeps everything scores
    `total - 1`. The one that is not kept is `b1`, source B's title, which the
    merge superseded because `keep-base` told it to. Asserted so that a *claim*
    going missing can never hide inside the same arithmetic: any second gap, or
    a gap on a segment that is not a title, fails here.
    """
    for pair in names():
        documents = sources_of(pair)
        expected = sum(len(segment_document(text, name[-4], name).segments)
                       for name, text in documents.items())
        for stem in merges_of(pair):
            result = reconcile.reconcile(documents, merge_of(pair, stem)[0])
            check(result.total == expected,
                  f"{pair}/{stem}: total is {result.total}, sources hold {expected}")
            unkept = [item for coverage in result.coverages
                      for item in coverage.located
                      if item.verdict != reconcile.PRESENT]
            check(len(unkept) == 1,
                  f"{pair}/{stem}: {len(unkept)} segments not kept verbatim, "
                  f"expected exactly the superseded title: "
                  f"{[item.segment.id for item in unkept]}")
            for item in unkept:
                check(item.segment.id == "b1" and item.segment.kind == reconcile.TITLE,
                      f"{pair}/{stem}: {item.segment.id} is a "
                      f"{item.segment.kind} and is not kept; only source B's "
                      "title may be missing, and a missing claim is a defect")
                declared = [record["segment"] for record in merge_of(pair, stem)[1]]
                check(item.segment.id in declared,
                      f"{pair}/{stem}: {item.segment.id} is not kept and not "
                      "declared")


def test_the_order_members_that_point_the_wrong_way_are_pinned() -> None:
    """A tripwire, not a requirement.

    Two `Order` members are known to mislead on this corpus. `stapled` is True
    of every shape-1 merge, correct and inverted alike, because a two-audience
    merge grouped by audience is legitimately one block per source. `attributed`
    is *lower* on the correct merge - 11 against 13, 13 against 14 - because
    marking a section lengthens its heading past `comparable`'s length floor.

    Both are reported and never judged, so neither costs anything
    today. The rule here is that no `Order` member may be promoted out
    of that state without being scored here first, and these are the numbers it
    would be scored against. If they move, the promotion argument moves with
    them and someone has to come and say so.
    """
    pinned = {
        ("incident_pager", "ideal"): (True, 13),
        ("incident_pager", "inverted"): (True, 14),
        ("sample_intake", "ideal"): (True, 11),
        ("sample_intake", "inverted"): (True, 13),
        ("parking_permits", "ideal"): (True, 14),
    }
    for (pair, stem), (stapled, attributed) in sorted(pinned.items()):
        order = reconcile.reconcile(sources_of(pair), merge_of(pair, stem)[0]).order
        check(order.stapled == stapled,
              f"{pair}/{stem}: stapled is {order.stapled}, pinned at {stapled}")
        check(order.attributed == attributed,
              f"{pair}/{stem}: attributed is {order.attributed}, pinned at "
              f"{attributed}")


def test_attribution_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_attribution_offline" \
                and callable(function):
            function()
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    merged = sum(len(merges_of(pair)) for pair in names())
    print(f"attribution: {checks} checks pass over {len(names())} pair(s), "
          f"{merged} merged document(s), 0 predicates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
