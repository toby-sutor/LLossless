#!/usr/bin/env python3
"""Offline checks for the instrument. No network, no model.

`reconcile` is what this benchmark measures the corpus with, so its own errors
become findings about the merge model unless they are pinned here. Four of
these checks exist because the instrument was wrong first and the corpus said
so — each names the merge that caught it, since a regression will show up as
that fixture changing verdict and the reader should be able to go and look:

    disjoint_sources-off-0    a hand-built staple, reported non-monotone
                              because the heading `Times` is contained in
                              `He also lost his orientation several times.`
    attribution_swapped-off-0 a correct merge, reported stapled on an evidence
                              base of one attributed segment per source
    structure_added-off-0     a conflict-resolving merge, reported stapled on
                              run grouping alone, though it states source B's
                              material out of source B's order
    dropped_claim-on-0        a genuine partial concatenation that must stay
                              flagged: it is the defect this milestone exists to catch

Run with `python3 tests/test_reconcile.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import re
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

from llossless import config, parsing, reconcile, segment  # noqa: E402
from llossless.cassette import MissingCassette  # noqa: E402
from llossless.decompose import Claim  # noqa: E402
from llossless.reconcile import (  # noqa: E402
    ABSENT,
    NEAR_MATCH,
    PRESENT,
    REWORDED,
)
from llossless.segment import LIST_ITEM, TITLE, document_id, segment_document  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"
MERGES = ROOT / "tests" / "responses" / "m4" / "merges"
PROMPTS = ROOT / "prompts"
SOURCES = ("source_a.md", "source_b.md")
# The decompose corpus: three samples of each document of the sixteen fixtures.
# `test_restatements_fire_on_restated_alone_among_recorded_claim_sets` says why
# this is a pinned number rather than a skip.
#
# The count was 14 until the endpoint guard that was refusing the recording of
# `concatenated` and `restated` was removed and they moved out of the `local/`
# overlay. Since the 27B import all sixteen are in the root corpus, one
# recording, and the overlay is gone.
SAMPLES = 3
RECORDED_DOCUMENTS = 16 * 3 * SAMPLES

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def sources_of(fixture: str) -> dict[str, str]:
    return {name: (FIXTURES / fixture / name).read_text(encoding="utf-8") for name in SOURCES}


def recorded(stem: str) -> reconcile.Reconciliation:
    """The instrument's own output for one merge already on disk."""
    fixture = stem.rsplit("-", 2)[0]
    merged = (MERGES / f"{stem}.md").read_text(encoding="utf-8")
    return reconcile.reconcile(sources_of(fixture), merged)


# --------------------------------------------------------------------------
# The primitives


def test_flatten_collapses_whitespace_and_takes_notation_off() -> None:
    """The two normalisations, and the fence that is exempt from the second.

    `flatten` gained the notation half when `render_sources`
    started showing the merge model the document's markers. Both sides of every
    comparison here are `Segment.text`, which never carried notation; the merge
    now does, and this is where it comes off. Folded into one function on
    purpose, so a comparison cannot be added that normalises one side only.
    """
    check(reconcile.flatten("  a\n\tb  c ") == "a b c", "flatten did not collapse whitespace")
    check(reconcile.flatten("A. B!") == "A. B!", "flatten altered punctuation or case")
    check(reconcile.flatten("## Defaults") == "Defaults", "a heading marker survived")
    check(reconcile.flatten("- Listen port: 8443") == "Listen port: 8443", "a bullet survived")
    check(reconcile.flatten("> quoted") == "quoted", "a blockquote arrow survived")
    check(reconcile.flatten("| Port | 8443 |") == "Port | 8443", "table pipes survived")
    fenced = "```yaml\n- a: 1\n# comment\n```"
    check(reconcile.flatten(fenced) == "```yaml - a: 1 # comment ```",
          f"a fence's own content must be left alone: {reconcile.flatten(fenced)!r}")


def test_a_merge_that_keeps_the_markdown_covers_its_sources() -> None:
    """The regression the rendering change could have caused, asserted.

    Shown notation, a merge writes notation back, so every coverage and token
    comparison meets a haystack the sources' stripped segment texts are not
    literally in. The two forms of the same merge must reconcile identically:
    if they do not, the reconciler is measuring markdown rather than content.
    """
    sources = sources_of("dedup")
    marked = (FIXTURES / "dedup" / "merged.md").read_text(encoding="utf-8")
    stripped = "\n".join(
        line for line in reconcile.plain(marked).splitlines()
    )
    check(marked != stripped, "the sample merge must actually carry notation")

    with_notation = reconcile.reconcile(sources, marked)
    without = reconcile.reconcile(sources, stripped)
    for left, right in zip(with_notation.coverages, without.coverages):
        check([item.verdict for item in left.located] == [item.verdict for item in right.located],
              f"{left.document.filename}: the same merge in two notations must locate "
              f"the same segments")
    check(len(with_notation.missing) == len(without.missing),
          f"and lose the same tokens: {len(with_notation.missing)} against "
          f"{len(without.missing)}")
    check(not with_notation.missing,
          f"the reference merge loses none: {[m.text for m in with_notation.missing]}")


def test_occurs_tolerates_only_the_leading_capital() -> None:
    haystack = reconcile.flatten("source_a.md states that the read timeout is 30 seconds.")
    check(
        reconcile.occurs("The read timeout is 30 seconds.", haystack),
        "a segment folded into an attributing sentence was not found",
    )
    check(
        not reconcile.occurs("The read timeout is 30 s.", haystack),
        "occurs matched text the merge does not contain",
    )


def test_token_present_respects_word_boundaries() -> None:
    """`30 seconds` shortened to `30s` is a changed token, not a present one."""
    check(reconcile.token_present("8443", "listens on port 8443."), "8443 not found")
    check(not reconcile.token_present("30 seconds", "the read timeout is 30s."), "30s accepted")
    check(not reconcile.token_present("512", "at most 5120 connections"), "512 matched 5120")


def test_comparable_is_derived_from_the_near_threshold() -> None:
    """The length guard is not a second constant: it follows from NEAR_MATCH.

    difflib's ratio cannot exceed 2m/(M+m), so two texts further apart in
    length than the floor could never have reached NEAR_MATCH by similarity
    either, and letting containment call them counterparts would contradict it.
    """
    check(
        abs(reconcile.LENGTH_FLOOR - NEAR_MATCH / (2 - NEAR_MATCH)) < 1e-12,
        "LENGTH_FLOOR is no longer derived from NEAR_MATCH",
    )
    short, long = "Times", "He also lost his orientation several times."
    check(not reconcile.comparable(short, long), "a heading was comparable to a whole sentence")
    check(
        reconcile.occurs(short, long),
        "the containment this guard exists to reject no longer happens",
    )
    ceiling = 2 * len(short) / (len(short) + len(long))
    check(ceiling < NEAR_MATCH, f"similarity could have reached {ceiling:.3f}, above the threshold")


# --------------------------------------------------------------------------
# Coverage, and its denominator


def test_coverage_denominator_is_the_source_segment_count() -> None:
    result = recorded("dropped_claim-off-0")
    for coverage in result.coverages:
        check(
            coverage.total == len(coverage.document.segments),
            f"{coverage.document.filename}: coverage total is not the segment count",
        )
        check(
            coverage.present + coverage.reworded + coverage.absent == coverage.total,
            f"{coverage.document.filename}: the three verdicts do not sum to the denominator",
        )


def test_a_dropped_heading_is_not_found_inside_a_sentence() -> None:
    """`## Limits` gone, and `Concurrency limits apply` is not it.

    Goes through `reconcile` rather than calling `locate` directly, so the
    assertion is on the code the CLI runs and not on a copy of its rule. The
    sentences either side are asserted too: the fix is to how labels are
    looked for, and a change that also moved prose would be a different one.
    """
    a = "# Runbook\n\nThe relay listens on port 8443.\n"
    b = "# Runbook\n\n## Limits\n\nConcurrency limits apply during peak windows.\n"
    merged = ("# Runbook\n\nThe relay listens on port 8443.\n\n"
              "Concurrency limits apply during peak windows.\n")
    result = reconcile.reconcile({"source_a.md": a, "source_b.md": b}, merged)
    verdicts = {item.segment.id: item.verdict
                for coverage in result.coverages for item in coverage.located}
    check("Limits" not in merged,
          "the fixture is only a fixture if the heading really is gone")
    check(verdicts["b2"] == reconcile.ABSENT,
          f"a heading the merge does not have must be absent, got {verdicts['b2']!r}")
    for identifier in ("a2", "b3"):
        check(verdicts[identifier] == reconcile.PRESENT,
              f"{identifier} is a sentence the merge carries verbatim and must "
              f"stay present, got {verdicts[identifier]!r}")

    found = reconcile.findings(result, (), fidelity="off", title_policy="keep-base",
                               base="source_a.md", budget=0.05)
    check(any(item.kind == reconcile.UNDECLARED_ABSENCE for item in found.findings),
          f"the dropped heading must reach the report, got "
          f"{[item.kind for item in found.findings]}")


def test_a_list_item_folded_into_prose_is_still_present() -> None:
    """The other half of that ruling, and the reason `LABEL_KINDS` stops at two.

    A merge that flattens a list into one sentence has kept every item. This is
    the shape `merge-639edb26f70bc957` has on the recorded corpus, and treating
    list items as labels called that merge five absences.
    """
    a = "# Env\n\nSomething else entirely.\n"
    b = "# Env\n\n- Product: Ledger\n- Version: 4.4\n- Platform: Cloud\n"
    merged = "# Env\n\nSomething else entirely.\n\nProduct: Ledger, Version: 4.4, Platform: Cloud\n"
    result = reconcile.reconcile({"source_a.md": a, "source_b.md": b}, merged)
    verdicts = {item.segment.id: item.verdict
                for coverage in result.coverages for item in coverage.located}
    kinds = {item.segment.id: item.segment.kind
             for coverage in result.coverages for item in coverage.located}
    folded = [i for i, kind in kinds.items() if kind == LIST_ITEM]
    check(len(folded) == 3, f"the fixture must carry three list items, got {kinds}")
    for identifier in folded:
        check(verdicts[identifier] == reconcile.PRESENT,
              f"{identifier} was folded into prose, not lost, and must stay "
              f"present, got {verdicts[identifier]!r}")


# --------------------------------------------------------------------------
# The supersession fan-in blind spot, closed 2026-09-18. Read the docstring first.
# --------------------------------------------------------------------------

# Two sources, eight segments, 341 characters; a merge of 104. Every non-title
# segment is declared away against the merge's one sentence, and this is
# recorded rather than repaired.
B5_SOURCE_A = ("# Release notes\n\nThe scheduler now retries failed jobs before giving up.\n"
               "Operators may pause a queue without draining it.\n"
               "Audit entries record who approved each override.\n")
B5_SOURCE_B = ("# Release notes\n\nSupport for read-only replicas has been withdrawn.\n"
               "The archive tier no longer accepts new writes.\n"
               "Nightly compaction runs during the maintenance window.\n")
B5_MERGED = ("# Release notes\n\nThis release changes scheduling, queues, auditing, "
             "replicas, archiving and compaction.\n")

# Every level, and the disposition each one *typically* uses. `off`'s row is
# `superseded` because that is the only combining move `off` permits, not
# because `off` is the default, which it is not: `config.DEFAULT_FIDELITY` is
# `high`. This table varies the disposition along with the level, which
# answers "what does each level usually do" and not "is this level-specific".
# A separate probe holds the disposition constant and asks the second
# question, and it gets a different answer there.
B5_LEVELS = (("off", "superseded"), ("low", "reworded"),
             ("mid", "reworded"), ("high", "subsumed"))


def test_b5_declaring_your_way_past_the_checks_still_works() -> None:
    """A KNOWN BLIND SPOT, asserted open. This test passing is not good news.

    Seventy per cent of the source text is declared away and the
    model-independent layer says nothing, at every fidelity level including the
    default. The mechanism: check 2 stands down on the mere
    existence of a disposition record and delegates the record's validity to
    check 3, whose question -- `resolves(replacement, merged_flat)` -- has no
    parameter for the segment and so returns the same answer for all six.

    **If this test fails, read the failure before fixing it.** A non-zero
    finding count here means something closed the blind spot, which is the outcome wanted.
    The right response is to retire the blind spot from the record of known
    blind spots, where it is written up with the mechanism above, and not to
    re-baseline the number so that this test
    goes quiet again. The count is asserted as exactly zero rather than as an
    upper bound for that reason: a partial fix that produced one finding at
    `high` and none at `off` must be loud, not rounded off.
    """
    result = reconcile.reconcile({"source_a.md": B5_SOURCE_A,
                                  "source_b.md": B5_SOURCE_B}, B5_MERGED)
    identifiers = [s.id for c in result.coverages for s in c.document.segments]
    replacement = B5_MERGED.split("\n\n")[1].strip()

    # The reconciler's own verdict on the same six segments, which is what
    # makes this a blind spot rather than a disagreement about the merge: it
    # can see they are gone, and the declarations are what stop it saying so.
    absent = [item.segment.id for c in result.coverages for item in c.located
              if item.verdict == reconcile.ABSENT]
    check(sorted(absent) == ["a2", "a3", "a4", "b2", "b3", "b4"],
          f"the fixture only demonstrates the blind spot while the six non-title segments "
          f"are absent on the reconciler's own reading; got {sorted(absent)}")

    for level, disposition in B5_LEVELS:
        declared = tuple(
            {"segment": i, "disposition": disposition,
             "replacement": replacement, "reason": "folded"}
            for i in identifiers if i not in ("a1", "b1")
        )
        declared += ({"segment": "b1", "disposition": "superseded",
                      "replacement": "Release notes", "reason": "same title"},)
        found = reconcile.findings(result, declared, fidelity=level,
                                   title_policy="keep-base", base="source_a.md",
                                   budget=0.05)
        # RETIRED 2026-09-18. This pinned the blind spot open
        # for six milestones; check 6a (supersession fan-in) closes it at every
        # level, so the assertion is inverted rather than deleted -- a closed
        # blind spot that silently re-opens must be as loud as one that closed.
        check(len(found.findings) == 1 and len(found.declared_drops) == 0,
              f"THE SUPERSESSION BLIND SPOT HAS RE-OPENED at fidelity {level!r}: "
              f"{len(found.findings)} finding(s), {len(found.declared_drops)} "
              f"declared drop(s), where check 6a should now produced 0 "
              f"and 0. This is the wanted outcome and it is NOT a regression. "
              f"Retire the blind spot from the record "
              f"of known blind spots "
              f"rather than re-baselining "
              f"this assertion.")


# The narrow fix, seeded both ways. One merge, one pair of sources, one pair
# of absent tokens; the **only** thing that varies between the two
# directions is the replacement string, and both of them resolve in the
# merge. Holding everything else constant is the rule for a fixture pair: a
# two-variable pair would credit the wrong mechanism.
NARROW_A = "# Limits\n\nThe timeout is 30 seconds.\nThe retry limit is 5.\n"
NARROW_B = "# Limits\n\nThe timeout is 60 seconds.\nThe retry limit is 9.\n"
# A's wording, kept whole. B's `60` and `9` are the tokens that do not survive.
NARROW_MERGED = "# Limits\n\nThe timeout is 30 seconds.\nThe retry limit is 5.\n"


def _narrow_violations(replacements: dict[str, str]) -> dict[str, list[str]]:
    """Check 5's findings for these `superseded` records, at every level."""
    result = reconcile.reconcile({"source_a.md": NARROW_A,
                                  "source_b.md": NARROW_B}, NARROW_MERGED)
    declared = tuple({"segment": segment, "disposition": "superseded",
                      "replacement": replacement, "reason": "A's wording was kept"}
                     for segment, replacement in replacements.items())
    out = {}
    for level in config.FIDELITY_LEVELS:
        got = reconcile.findings(result, declared, fidelity=level,
                                 title_policy="keep-base", base="source_a.md",
                                 budget=config.DEFAULT_DECLARED_LOSS_BUDGET)
        out[level] = sorted(f.segment for f in got.findings
                            if f.kind == reconcile.VERBATIM_VIOLATION)
    return out


def test_superseded_excuses_a_token_only_for_another_source_segments_wording() -> None:
    """The narrow fix, at every level. The must-fire half of the blind-spot probe.

    `prompts/merge.md:85` says `superseded` means this segment was superseded
    *by another source's version*, so the replacement has to be that version.
    Before this fix any span that merely resolved discharged check 5, which let a
    merge delete a segment outright, point `superseded` at a sentence of its
    own prose, and silence the verbatim core -- at every level, because check 5
    consults no level and `superseded` is permitted at all four.

    This is the seeded positive that the blind-spot test above cannot be: that
    one is prose-only and stays silent by design, so on its own it would report
    a dead check as healthy.
    """
    carried = _narrow_violations({"b2": "The timeout is 30 seconds.",
                                  "b3": "The retry limit is 5."})
    check(all(not v for v in carried.values()),
          f"a replacement that IS another source segment's wording is what "
          f"`superseded` licenses and must stay exempt at every level: {carried}")

    # Same sources, same merge, same absent tokens. Only the pointer moved, to
    # a span of the merge's own text that no single source segment carries.
    composite = "The timeout is 30 seconds. The retry limit is 5."
    attacked = _narrow_violations({"b2": composite, "b3": composite})
    check(all(v == ["b2", "b3"] for v in attacked.values()),
          f"a `superseded` pointer at the merge's own composite span is not "
          f"another source's version, so the tokens it discharged must fire at "
          f"every level: {attacked}")


def test_the_narrow_superseded_rule_is_not_one_to_one() -> None:
    """The explicit limit: many-to-one is the operator's own usage.

    `tests/pairs/rate_limits/ideal.json` uses `superseded` many-to-one nine
    times and `bike_docks` folds three segments into one sentence, so a rule
    reading `superseded` as one-to-one would contradict the ground truth the
    corpus is graded against. Two segments discharged against the same other
    source segment is therefore exempt, and this pins that it stays exempt.
    """
    shared = _narrow_violations({"b2": "The timeout is 30 seconds.",
                                 "b3": "The timeout is 30 seconds."})
    check(all(not v for v in shared.values()),
          f"two segments naming one source segment's wording must not become a "
          f"finding: the narrow fix is a containment test against the sources, "
          f"not a uniqueness condition: {shared}")


# --------------------------------------------------------------------------
# Check 2's third kind, seeded both ways from the corpus
# --------------------------------------------------------------------------

# A real recorded merge over a real in-repo pair, not a fixture written to make
# the point. The cassette supplies the merged document and the thirty
# disposition records the model actually emitted; the sources are the pair on
# disk. Nothing here is reconstructed, so nothing here can be an artefact of a
# harness -- which the first measurement of this defect was: reconstructing the
# sources from the prompt's rendered segment lines moved one record between the
# two classes below.
FALSE_DEPARTURE_CASSETTE = ROOT / "tests" / "responses" / "pairs" / "merge-639edb26f70bc957.json"
FALSE_DEPARTURE_PAIR = ROOT / "tests" / "pairs" / "index_429"

# Both counts are the measurement, pinned. The must-fire set is what the
# converse direction of `prompts/merge.md:53-56` catches on this merge; the
# must-not-fire pair is the cross-source exclusion doing its job, and it is the
# control that matters, because a rule that fired on those would accuse a merge
# of two documents that share a heading.
MUST_FIRE = ("b10", "b11", "b15", "b16", "b17", "b18", "b19", "b20",
             "b25", "b27", "b29", "b30", "b7", "b8", "b9")
MUST_NOT_FIRE = ("b6", "b12")


def _false_departure_run():
    payload = json.loads(FALSE_DEPARTURE_CASSETTE.read_text(encoding="utf-8"))
    body = json.loads(json.loads(payload["response"]["raw"])
                      ["choices"][0]["message"]["content"])
    sources = {
        "source_a.md": (FALSE_DEPARTURE_PAIR / "source_a.md").read_text(encoding="utf-8"),
        "source_b.md": (FALSE_DEPARTURE_PAIR / "source_b.md").read_text(encoding="utf-8"),
    }
    result = reconcile.reconcile(sources, body["merged_document"])
    found = reconcile.findings(result, tuple(body["dispositions"]), fidelity="high",
                               title_policy="keep-base", base="source_a.md",
                               budget=0.05)
    return result, body, found


def test_a_declared_departure_the_merge_did_not_take_is_a_finding() -> None:
    """The must-fire half. Declared subsumed, carried unchanged, nowhere else."""
    result, body, found = _false_departure_run()
    fired = sorted(item.segment for item in found.findings
                   if item.kind == reconcile.FALSE_DEPARTURE)
    check(fired == sorted(MUST_FIRE),
          f"the seeded must-fire set moved: expected {sorted(MUST_FIRE)}, got {fired}")

    # Each one is the contradiction and not something else: a record says the
    # content departed, and the merge has the segment verbatim.
    verdicts = {item.segment.id: item.verdict
                for coverage in result.coverages for item in coverage.located}
    records = {str(r["segment"]): str(r["disposition"]) for r in body["dispositions"]}
    for identifier in fired:
        check(verdicts[identifier] == reconcile.PRESENT,
              f"{identifier} must be PRESENT for this kind to be the right "
              f"accusation, got {verdicts[identifier]!r}")
        check(records[identifier] in reconcile.DEPARTED,
              f"{identifier} must carry a departure disposition, got "
              f"{records[identifier]!r}")


def test_a_segment_another_source_also_carries_is_not_a_false_departure() -> None:
    """The must-not-fire half, and the reason the exclusion exists.

    `superseded` means another document's version was used instead. When an
    identical segment sits in another source, the text in the merge is that
    document's copy and this one did depart, so the record is true. Without
    this the check would fire on any merge of two documents sharing a heading.
    """
    result, body, found = _false_departure_run()
    fired = {item.segment for item in found.findings
             if item.kind == reconcile.FALSE_DEPARTURE}
    verdicts = {item.segment.id: item.verdict
                for coverage in result.coverages for item in coverage.located}
    texts = {item.segment.id: reconcile.flatten(item.segment.text)
             for coverage in result.coverages for item in coverage.located}
    records = {str(r["segment"]): str(r["disposition"]) for r in body["dispositions"]}

    for identifier in MUST_NOT_FIRE:
        # The control is only a control while it would otherwise have fired:
        # a departure disposition, and present in the merge.
        check(records[identifier] in reconcile.DEPARTED
              and verdicts[identifier] == reconcile.PRESENT,
              f"{identifier} no longer meets the predicate the exclusion is "
              f"there to override, so it has stopped being a negative control "
              f"({records.get(identifier)!r}, {verdicts.get(identifier)!r})")
        elsewhere = [c.document.id for c in result.coverages
                     if c.document.id != identifier[:1]
                     and texts[identifier] in {reconcile.flatten(s.text)
                                               for s in c.document.segments}]
        check(elsewhere,
              f"{identifier} must be carried by another source for the "
              f"exclusion to apply; found none")
        check(identifier not in fired,
              f"{identifier} is carried by source {elsewhere} as well and must "
              f"not be accused of a false departure")


def test_coverage_line_always_prints_the_denominator() -> None:
    """The first lesson worth asserting rather than remembering."""
    coverage = recorded("dropped_claim-off-0").coverages[0]
    line = coverage.line()
    check(f"/{coverage.total}" in line, f"no denominator in {line!r}")


def test_a_verbatim_copy_of_both_sources_loses_nothing() -> None:
    """The instrument's floor: everything present, nothing absent, no token gone."""
    documents = sources_of("dropped_claim")
    merged = "\n\n".join(documents.values())
    result = reconcile.reconcile(documents, merged)
    check(result.absent == 0, f"{result.absent} segment(s) absent from a verbatim concatenation")
    check(result.present == result.total, f"only {result.present}/{result.total} present")
    check(not result.missing, f"{len(result.missing)} invariant token(s) lost by a copy")


def test_a_dropped_sentence_is_absent_and_not_reworded() -> None:
    """`dropped_claim`'s planted omission, which is what ABSENT has to mean."""
    result = recorded("dropped_claim-on-0")
    absent = {
        item.segment.text
        for coverage in result.coverages
        for item in coverage.of(ABSENT)
    }
    for text in ("The default connect timeout is 30 seconds.", "The default read timeout is 120 seconds."):
        check(text in absent, f"{text!r} was not reported absent from dropped_claim-on-0")


def test_every_verdict_is_one_of_the_three() -> None:
    verdicts = {
        item.verdict
        for coverage in recorded("paraphrase-on-0").coverages
        for item in coverage.located
    }
    check(verdicts <= {PRESENT, REWORDED, ABSENT}, f"unexpected verdict(s): {verdicts}")


# --------------------------------------------------------------------------
# The invariant core


def test_a_changed_number_is_reported_as_a_missing_token() -> None:
    documents = sources_of("dropped_claim")
    merged = "\n\n".join(documents.values()).replace("port 8443", "port 8444")
    result = reconcile.reconcile(documents, merged)
    check(result.missing, "changing 8443 to 8444 lost no invariant token")
    check(
        all("8443" in item.text for item in result.missing),
        f"the wrong token(s) were reported: {[item.text for item in result.missing]}",
    )


def test_the_token_denominator_is_reported_beside_the_losses() -> None:
    result = recorded("dropped_claim-on-0")
    check(result.tokens > 0, "no invariant-core tokens were checked at all")
    check(
        len(result.missing) <= result.tokens,
        f"{len(result.missing)} missing out of {result.tokens} checked",
    )


# --------------------------------------------------------------------------
# Duplication


def test_a_sentence_stated_twice_is_reported_once() -> None:
    documents = sources_of("dropped_claim")
    sentence = "The relay listens on port 8443 by default."
    merged = f"{sentence}\n\nSomething else entirely happens here.\n\n{sentence}\n"
    duplicates = reconcile.duplication(segment_document(merged, "m").segments)
    check(len(duplicates) == 1, f"{len(duplicates)} duplicate(s) reported, expected 1")
    if duplicates:
        check(duplicates[0].count == 2, f"count {duplicates[0].count}, expected 2")
        check(duplicates[0].exact, "an identical repeat was not reported as exact")


def test_repeated_headings_are_not_duplication() -> None:
    """Two sections may share a heading without the merge saying anything twice."""
    merged = "## Limits\n\nOne fact here.\n\n## Limits\n\nA different fact here.\n"
    check(not reconcile.duplication(segment_document(merged, "m").segments), "a heading counted")


# --------------------------------------------------------------------------
# Four merges, four different answers.


def test_a_partial_concatenation_is_flagged() -> None:
    """dropped_claim-on-0: A's sections, then B's, with two sentences gone.

    The case this check exists for. The old ratio predicate does not fire on it: that
    disagreement is the finding, so it is asserted rather than described.
    """
    order = recorded("dropped_claim-on-0").order
    check(order.stapled, "the partial concatenation dropped_claim-on-0 was not flagged")
    check(order.monotone, "dropped_claim-on-0 is source order twice over; it reads non-monotone")
    check(order.conclusive, "dropped_claim-on-0's evidence base is too small to conclude from")


def test_a_hand_built_staple_keeps_each_source_in_order() -> None:
    """disjoint_sources-off-0: two unrelated stories, one after the other.

    This one is *correctly* a staple — nothing connects the two documents — so
    the assertion is about the instrument, not the merge. It reported
    non-monotone before the length guard, on headings contained in sentences.
    """
    order = recorded("disjoint_sources-off-0").order
    check(order.monotone, "disjoint_sources-off-0 read as reordering its own sources")
    check(order.runs == 2, f"runs {order.runs}, expected 2 for two stories set end to end")
    check(order.attributed > 20, f"only {order.attributed} segment(s) attributed, expected 20+")


def test_reordered_source_material_is_not_a_staple() -> None:
    """structure_added-off-0: resolves the conflict, and moves B's material.

    Grouping alone would call this stapled. It states source B's TLS line
    before source B's health-check line, which a concatenation cannot do.
    """
    order = recorded("structure_added-off-0").order
    check(not order.monotone, "structure_added-off-0 no longer reads as reordered")
    check(not order.stapled, "a merge that reorders a source was called a concatenation")


def test_an_evidence_base_that_admits_one_answer_concludes_nothing() -> None:
    """attribution_swapped-off-0: correct merge, one attributed segment each.

    Both shared sentences belong to neither document and are excluded, so the
    sequence is `ab` — and `ab` is two runs of one however the merge was built.
    """
    order = recorded("attribution_swapped-off-0").order
    check(not order.conclusive, f"sequence {''.join(order.sequence)} was called conclusive")
    check(not order.stapled, "a staple was declared on evidence that admits no other answer")


def test_content_both_sources_state_is_attributed_to_neither() -> None:
    """The exclusion the staple predicate rests on, checked on its own."""
    documents = sources_of("dropped_claim")
    shared = "Vandrell Relay is a fictional HTTP relay."
    check(
        all(shared in text for text in documents.values()),
        "the fixture no longer shares this sentence between both sources",
    )
    order = reconcile.reconcile(documents, f"{shared}\n").order
    check(order.attributed == 0, f"{order.attributed} segment(s) attributed from shared text alone")


def test_heading_survival_counts_titles_and_headings_only() -> None:
    result = recorded("dropped_claim-on-0")
    expected = sum(
        1
        for coverage in result.coverages
        for item in coverage.located
        if item.segment.kind in ("heading", TITLE)
    )
    check(
        result.order.headings_total == expected,
        f"headings_total {result.order.headings_total}, expected {expected}",
    )
    check(
        result.order.headings_present <= result.order.headings_total,
        "more headings survived than existed",
    )


# --------------------------------------------------------------------------
# The whole instrument, over the whole corpus


def test_no_recorded_merge_reports_more_than_its_denominator() -> None:
    """Over all 72 merges: every count stays inside the segment count."""
    for path in sorted(MERGES.glob("*.md")):
        result = recorded(path.stem)
        check(
            result.present + result.reworded + result.absent == result.total,
            f"{path.stem}: verdicts do not sum to {result.total}",
        )
        check(
            len(result.order.sequence) <= len(result.merged),
            f"{path.stem}: attributed more merge segments than the merge has",
        )


def test_reconcile_is_a_pure_function_of_the_two_texts() -> None:
    documents = sources_of("contradiction")
    merged = (MERGES / "contradiction-off-0.md").read_text(encoding="utf-8")
    first = reconcile.reconcile(documents, merged)
    second = reconcile.reconcile(documents, merged)
    check(first.order.sequence == second.order.sequence, "the sequence is not deterministic")
    check(
        (first.present, first.absent, first.tokens) == (second.present, second.absent, second.tokens),
        "the counts are not deterministic",
    )


def test_document_letters_follow_the_order_the_merge_was_given() -> None:
    documents = sources_of("contradiction")
    result = reconcile.reconcile(documents, "nothing here\n")
    check(
        [coverage.document.id for coverage in result.coverages] == [document_id(0), document_id(1)],
        "the source letters do not follow the documents' order",
    )


# --------------------------------------------------------------------------
# The mechanical reconciliation
# --------------------------------------------------------------------------
#
# A hand-built pair rather than a fixture, because every one of these checks is
# about a *disposition record*, and no fixture has one: the corpus on disk was
# recorded under an earlier prompt, which had no such field. The pair is six
# segments -- two titles, a line both documents share, and a distinct fact each
# -- which is the smallest thing that can be right or wrong in all nine ways.

TITLED_A = (
    "# Relay Handbook\n\n"
    "The relay listens on port 8443.\n"
    "The connect timeout is 30 seconds.\n"
)
TITLED_B = (
    "# Relay Notes\n\n"
    "The relay listens on port 8443.\n"
    "The read timeout is 45 seconds.\n"
)
PAIR = {"source_a.md": TITLED_A, "source_b.md": TITLED_B}
CLEAN_MERGE = (
    "# Relay Handbook\n\n"
    "The relay listens on port 8443.\n"
    "The connect timeout is 30 seconds.\n"
    "The read timeout is 45 seconds.\n"
)
# b1's title lost to the base's, b2 says what a2 already said. a2, a3 and b3
# carry no record at all, which is the claim that they survived character for
# character -- and the claim `findings` checks by string containment.
CLEAN_DISPOSITIONS = (
    {"segment": "b1", "disposition": "superseded",
     "replacement": "Relay Handbook", "reason": "the base document's title"},
    {"segment": "b2", "disposition": "duplicate",
     "replacement": "The relay listens on port 8443.", "reason": "a2 states this"},
)


def reconciled(merged=CLEAN_MERGE, dispositions=CLEAN_DISPOSITIONS, *,
               sources=None, fidelity="off", title_policy="keep-base",
               base="source_a.md", budget=config.DEFAULT_DECLARED_LOSS_BUDGET):
    documents = PAIR if sources is None else sources
    return reconcile.findings(
        reconcile.reconcile(documents, merged), dispositions,
        fidelity=fidelity, title_policy=title_policy, base=base, budget=budget,
    )


def kinds(result) -> list[str]:
    return sorted(item.kind for item in result.findings)


def test_reconciled_is_permitted_at_high_and_refused_everywhere_else() -> None:
    """The disposition that declares a combination, and the
    only level allowed to make one.

    Seeded both ways rather than asserted once. The must-fire case is a
    `reconciled` record at `off`, `low` and `mid`, which has to reach
    `DISPOSITION_NOT_PERMITTED`; the must-not-fire case is the same record at
    `high`, which has to be quiet about that kind. A test that only checked
    the permission would pass just as well against a matrix that permitted it
    everywhere, which is the failure this pair exists to exclude.

    `mid` is the row worth having. It gained `subsumed` in the same brief, so
    it can now combine two statements that are both already stated; what it
    still cannot do is write one that neither document makes. Those two look
    alike from a distance, and the disposition is the whole of what separates
    them.
    """
    check("reconciled" in parsing.DISPOSITIONS,
          "reconciled must be in the contract before any level can permit it")
    check("reconciled" in reconcile.PERMITTED["high"],
          f"high must permit reconciled: {reconcile.PERMITTED['high']}")
    for level in ("off", "low", "mid"):
        check("reconciled" not in reconcile.PERMITTED[level],
              f"{level} must refuse reconciled: {reconcile.PERMITTED[level]}")

    # Through `findings`, not only the table: the matrix is the rule and
    # `findings` is what applies it, and a run consults the second.
    record = ({"segment": "a3", "disposition": "reconciled",
               "replacement": CLEAN_MERGE.strip().splitlines()[-1],
               "reason": "combined with b3"},)
    for level in ("off", "low", "mid"):
        got = kinds(reconciled(dispositions=record, fidelity=level))
        check(reconcile.DISPOSITION_NOT_PERMITTED in got,
              f"a reconciled record at {level} must be refused, got {got}")
    got = kinds(reconciled(dispositions=record, fidelity="high"))
    check(reconcile.DISPOSITION_NOT_PERMITTED not in got,
          f"a reconciled record at high must be permitted, got {got}")


def test_a_verbatim_violation_names_the_readable_token() -> None:
    """A finding is read by a human, so it must not print `_mask`'s NULs.

    A must-fire, and it once fired for the wrong reason: the link
    span's own text held the NULs that masked the code span inside it, so
    `token_present` searched the merge for a needle no document can contain and
    the violation was unconditional. Both halves are asserted here -- that the
    finding fires when the link really is gone, and that it names the link.
    """
    link = "[the `relay` guide](https://example.test/docs/relay.md)"
    sources = {
        "source_a.md": f"# Relay Notes\n\nSee {link} for detail.\n",
        "source_b.md": "# Relay Notes\n\nThe relay listens on port 8443.\n",
    }
    kept = reconcile.findings(
        reconcile.reconcile(
            sources,
            f"# Relay Notes\n\nSee {link} for detail.\n\n"
            "The relay listens on port 8443.\n",
        ),
        (), fidelity="off", title_policy="keep-base", base="source_a.md",
        budget=config.DEFAULT_DECLARED_LOSS_BUDGET,
    )
    check(not [item for item in kept.findings if item.kind == "verbatim_violation"],
          f"a merge that kept the link loses no token: "
          f"{[item.detail for item in kept.findings]}")

    dropped = reconcile.findings(
        reconcile.reconcile(sources, "# Relay Notes\n\nThe relay listens on port 8443.\n"),
        (), fidelity="off", title_policy="keep-base", base="source_a.md",
        budget=config.DEFAULT_DECLARED_LOSS_BUDGET,
    )
    violations = [item for item in dropped.findings if item.kind == "verbatim_violation"]
    check(any(link in item.detail for item in violations),
          f"the finding must name the link as it was written: "
          f"{[item.detail for item in violations]}")
    for item in dropped.findings:
        check("\x00" not in item.detail, f"a finding printed a mask byte: {item.detail!r}")


def test_a_correct_merge_produces_no_finding_at_all() -> None:
    """The floor. Without this every check below could be passing vacuously."""
    result = reconciled()
    check(result.findings == (), f"a correct merge must produce no finding, got {kinds(result)}")
    check(result.segments == 6, f"the denominator is the six source segments, got {result.segments}")
    check(result.declared_drops == (), "a merge that dropped nothing declares no drop")
    check(result.loss == 0.0, f"no drops is no loss, got {result.loss}")


# Both distinct facts removed, not one. The pair's two timeout lines resemble
# each other at 0.80, well over `NEAR_MATCH`, so a merge that drops one and
# keeps the other leaves the dropped segment a near neighbour to score against
# and check 2 calls it a rewording -- see the registered case below. Taking both
# is what makes this fixture an absence rather than an argument about which kind
# it is.
NEITHER_TIMEOUT = CLEAN_MERGE.replace(
    "The connect timeout is 30 seconds.\n", "").replace(
    "The read timeout is 45 seconds.\n", "")


def test_an_absence_nobody_declared_is_the_finding_the_design_exists_for() -> None:
    """Silence is the claim of verbatim retention, and this is where it is checked."""
    result = reconciled(NEITHER_TIMEOUT)
    found = [item for item in result.findings if item.kind == reconcile.UNDECLARED_ABSENCE]
    check([(item.segment, item.document) for item in found]
          == [("a3", "source_a.md"), ("b3", "source_b.md")],
          f"two segments were left silently, so two findings naming a3 and b3; got "
          f"{[(item.kind, item.segment, item.document) for item in result.findings]}")
    check(not any(item.kind == reconcile.UNDECLARED_REWORDING for item in result.findings),
          f"nothing was reworded here; both sentences are gone, got {kinds(result)}")

    # One of the two absences declared. It leaves findings entirely and becomes
    # a drop on the review queue; the other is untouched, which is what makes
    # this a per-segment suppression rather than a switch.
    declared = CLEAN_DISPOSITIONS + (
        {"segment": "a3", "disposition": "dropped", "replacement": "",
         "reason": "the connect timeout is not a fact about this relay"},
    )
    owned = reconciled(NEITHER_TIMEOUT, declared)
    check([item.segment for item in owned.findings
           if item.kind == reconcile.UNDECLARED_ABSENCE] == ["b3"],
          f"a declared drop is not an undeclared absence, and b3 is still one; "
          f"got {kinds(owned)}")
    check(len(owned.declared_drops) == 1,
          f"it is a declared drop, and the reconciler must carry it, got {owned.declared_drops}")


def test_a_surviving_near_twin_makes_a_deletion_look_like_a_rewording() -> None:
    """A registered limitation of the split, not a behaviour worth having.

    `Located.verdict` is `REWORDED` when *some* merge segment scores over
    `NEAR_MATCH` against the source segment. Nothing requires that segment to be
    this one's counterpart, and here it is not: delete `The connect timeout is 30
    seconds.` and `The read timeout is 45 seconds.` is still there, 0.80 alike,
    so a3 is reported reworded when it is simply gone. The kinds were split
    on this verdict because it is the discriminator the recorded data was graded
    with; it did not make the verdict better, and this is what it costs.

    The obvious guard -- refuse the nearest segment if it is verbatim some other
    source segment -- was measured on the recorded sweep before being left out:
    it moves nothing on A1 or B1, whose six rewordings all score 0.97-0.99
    against merge segments that are nobody's verbatim copy, and it would misfile
    a genuine rewording of a line the two sources share. A rule that changes no
    real case and can be wrong on one is not worth its own paragraph in the
    method. The number is pinned here so it cannot drift in silence.
    """
    one_gone = CLEAN_MERGE.replace("The connect timeout is 30 seconds.\n", "")
    result = reconciled(one_gone)
    check([(item.kind, item.segment) for item in result.findings
           if item.kind in (reconcile.UNDECLARED_ABSENCE, reconcile.UNDECLARED_REWORDING)]
          == [(reconcile.UNDECLARED_REWORDING, "a3")],
          f"the registered misfiling changed; got {kinds(result)}")
    ratio = reconcile.similarity("The connect timeout is 30 seconds.",
                                 "The read timeout is 45 seconds.")
    check(round(ratio, 2) == 0.80 and ratio >= reconcile.NEAR_MATCH,
          f"the twin scores {ratio:.3f}; this case is registered at 0.80 over "
          f"NEAR_MATCH={reconcile.NEAR_MATCH}")


def test_a_rewording_that_was_not_declared_is_not_called_an_absence() -> None:
    """`reworded` is not `present`, and it is not `absent` either.

    A merge that quietly improved a sentence has departed from it, and at `off`
    the departure is not permitted in the first place -- so it is still a finding
    from the same check, on the same string comparison, with no separate "was it
    reworded" test. What it is not is material the merge lost, and while the two
    shared one kind a count of that kind read as loss whichever it was made of.
    The sentence below is still in the merge; anyone reading `undeclared_absence`
    over it was being told something false.

    The pair is the registration: one edit that must fire `undeclared_rewording`
    and never `undeclared_absence`, one deletion that must do the reverse. A
    single-sided probe would pass on a checker that had merely renamed the kind.
    """
    reworded = CLEAN_MERGE.replace(
        "The connect timeout is 30 seconds.",
        "The connect timeout is set to 30 seconds.",
    )
    result = reconciled(reworded)
    check([(item.kind, item.segment) for item in result.findings]
          == [(reconcile.UNDECLARED_REWORDING, "a3")],
          f"the rewritten segment is reworded and undeclared, got {kinds(result)}")
    check(reconcile.similarity(
              "The connect timeout is 30 seconds.",
              "The connect timeout is set to 30 seconds.") >= reconcile.NEAR_MATCH,
          "this edit must score above NEAR_MATCH or the fixture is testing absence")
    detail = result.findings[0].detail
    check("reworded in the merge" in detail and "not in the merge" not in detail,
          f"the detail must say what happened rather than claim the text is gone: {detail!r}")

    # The other side, on the fixture that removes both near twins so that no
    # surviving segment can stand in for either -- the case the test below
    # registers is what happens when one does.
    gone = reconciled(NEITHER_TIMEOUT)
    check(not any(item.kind == reconcile.UNDECLARED_REWORDING for item in gone.findings),
          f"removed segments must not be reported as reworded, got {kinds(gone)}")


def test_an_invented_segment_id_is_an_error() -> None:
    """Check 1. A record pointing at nothing cannot be checked, so it is reported."""
    result = reconciled(dispositions=CLEAN_DISPOSITIONS + (
        {"segment": "a9", "disposition": "duplicate",
         "replacement": "The relay listens on port 8443.", "reason": "invented"},
    ))
    found = [item for item in result.findings if item.kind == reconcile.INVENTED_SEGMENT]
    check([item.segment for item in found] == ["a9"],
          f"a9 is in neither source and must be reported, got {kinds(result)}")


def test_a_replacement_that_is_not_in_the_merge_is_an_error() -> None:
    """Check 3. The prompt says the pointer must resolve, so a dangling one is warned-of."""
    result = reconciled(dispositions=(
        CLEAN_DISPOSITIONS[0],
        {"segment": "b2", "disposition": "duplicate",
         "replacement": "The relay listens on port 9999.", "reason": "a2 states this"},
    ))
    found = [item for item in result.findings if item.kind == reconcile.UNRESOLVED_REPLACEMENT]
    check([item.segment for item in found] == ["b2"],
          f"the pointer resolves to nothing in the merge, got {kinds(result)}")

    # A `dropped` record names no replacement and must not be read as a dangling
    # one. Empty is the correct value there, not a missing one.
    dropped = reconciled(
        CLEAN_MERGE.replace("The connect timeout is 30 seconds.\n", ""),
        CLEAN_DISPOSITIONS + (
            {"segment": "a3", "disposition": "dropped", "replacement": "", "reason": "gone"},
        ),
    )
    check(not any(item.kind == reconcile.UNRESOLVED_REPLACEMENT for item in dropped.findings),
          f"an empty replacement on a drop is correct, not dangling, got {kinds(dropped)}")


def test_a_replacement_over_the_cap_is_given_as_its_two_ends() -> None:
    """Check 3 still asks the same question.

    A capped `replacement` cannot name a long span whole, so it names both ends
    and the middle is elided. Both ends must be found, and the second only after
    the first: two ends taken from unrelated places in the merge point at no
    span at all, which is the failure this check exists to catch.
    """
    span = ("The relay accepts connections on port 8443 and holds each one open "
            "until the read timeout expires, which is 45 seconds by default and "
            "is not configurable per connection in this release; a connection "
            "that idles past the timeout is closed without notice to the client. "
            "Operators who need a longer window raise it for the whole process "
            "and restart, because the value is read once at startup and is not "
            "re-read on reload. The relay writes one line per closed connection "
            "to the access log, naming the peer, the byte counts in each "
            "direction and whether the close was orderly, and it writes nothing "
            "at all for a connection that never completed its handshake, which "
            "is the gap operators most often mistake for a dropped log line.")
    check(len(span) > parsing.REPLACEMENT_MAX,
          f"the fixture span must be over the cap to test the cap, it is {len(span)}")
    long_pair = {"source_a.md": "# Relay Handbook\n\nThe relay listens on port 8443.\n",
                 "source_b.md": f"# Relay Notes\n\n{span}\n"}
    merged = f"# Relay Handbook\n\nThe relay listens on port 8443.\n{span}\n"
    kept = ({"segment": "b1", "disposition": "superseded",
             "replacement": "Relay Handbook", "reason": "the base document's title"},)

    def with_replacement(text):
        return reconciled(merged, kept + (
            {"segment": "b2", "disposition": "duplicate",
             "replacement": text, "reason": "the merge carries it"},
        ), sources=long_pair)

    anchored = with_replacement(parsing.anchor(span))
    check(reconcile.UNRESOLVED_REPLACEMENT not in kinds(anchored),
          f"an anchored replacement must resolve like a whole one, got "
          f"{[(item.kind, item.detail) for item in anchored.findings]}")

    ends = parsing.anchor(span).split(parsing.ELISION)
    check(len(ends) == 2, f"the anchor is two ends, got {len(ends)}")
    backwards = with_replacement(parsing.ELISION.join(reversed(ends)))
    check(reconcile.UNRESOLVED_REPLACEMENT in kinds(backwards),
          f"the ends in the wrong order name no span, got {kinds(backwards)}")

    elsewhere = with_replacement(ends[0] + parsing.ELISION + "on port 9999.")
    check(reconcile.UNRESOLVED_REPLACEMENT in kinds(elsewhere),
          f"an end that is not in the merge must still be caught, got {kinds(elsewhere)}")

    # And the primitive itself, since the two negatives above could both be
    # passing on the first end alone.
    check(reconcile.resolves("one [...] three", "one two three"),
          "two ends in order resolve")
    check(not reconcile.resolves("three [...] one", "one two three"),
          "order is part of the question, not only membership")
    check(reconcile.resolves("one two three", "one two three"),
          "an unelided replacement is the one-part case and must still resolve")


def test_a_disposition_the_level_does_not_permit_is_an_error() -> None:
    """Check 4, and the matrix is the one thing here that reads a flag."""
    at_off = reconciled(dispositions=(
        CLEAN_DISPOSITIONS[0],
        {"segment": "b2", "disposition": "subsumed",
         "replacement": "The relay listens on port 8443.", "reason": "folded in"},
    ))
    found = [item for item in at_off.findings
             if item.kind == reconcile.DISPOSITION_NOT_PERMITTED]
    check([item.segment for item in found] == ["b2"],
          f"subsumed at off is an error, not a judgement call, got {kinds(at_off)}")

    at_high = reconciled(dispositions=(
        CLEAN_DISPOSITIONS[0],
        {"segment": "b2", "disposition": "subsumed",
         "replacement": "The relay listens on port 8443.", "reason": "folded in"},
    ), fidelity="high")
    check(at_high.findings == (),
          f"the same record at high is the expected behaviour, got {kinds(at_high)}")


WORDS = ("Alpha", "Bravo", "Charlie", "Delta", "Echo",
         "Foxtrot", "Golf", "Hotel", "India", "Juliett")

# Twenty segments and not a digit among them. The invariant-core check reads no
# disposition record at all, so a segment carrying a number becomes a
# verbatim violation the moment it leaves the merge, declared or not -- which is
# correct, and is asserted where it belongs, but would be noise in a test about
# the loss budget.
TWENTY = {
    "source_a.md": "".join(f"{word} is recorded here.\n" for word in WORDS),
    "source_b.md": "".join(f"{word} is also noted here.\n" for word in WORDS),
}


def twenty(dropped: int, fidelity: str = "high",
           budget: float = config.DEFAULT_DECLARED_LOSS_BUDGET):
    """The twenty-segment pair with the first `dropped` of source B declared gone."""
    merged = TWENTY["source_a.md"] + "".join(
        f"{word} is also noted here.\n" for word in WORDS[dropped:]
    )
    records = tuple(
        {"segment": f"b{index + 1}", "disposition": "dropped",
         "replacement": "", "reason": "not carried"}
        for index in range(dropped)
    )
    return reconcile.findings(
        reconcile.reconcile(TWENTY, merged), records,
        fidelity=fidelity, title_policy="keep-base", base="source_a.md",
        budget=budget,
    )


def test_a_declared_drop_is_never_also_an_impermissible_disposition() -> None:
    """One inconsistency between two design notes, resolved in favour of the budget rule.

    A design note calls `dropped` "never permitted"; this module instead sends a declared
    drop to the review queue and make it a finding only over the aggregate
    budget. If both were enforced every declared drop would be two findings and
    the split that makes declaring worth doing would be gone.
    """
    check(not any("dropped" in row for row in reconcile.PERMITTED.values()),
          "dropped is in no row of the matrix")
    # Budget pinned rather than inherited: this asks whether a declared drop is
    # *also* an impermissible disposition, which is independent of where the
    # ceiling sits. Inheriting the default made it fail when the default was lowered
    # to 3%, where one in twenty is 5% and over -- a true statement about the
    # new default, and nothing to do with what this test is for.
    result = twenty(1, budget=0.05)
    check(result.findings == (),
          f"one drop in twenty is under budget and carries no other defect, "
          f"got {kinds(result)}")
    check(len(result.declared_drops) == 1,
          f"and it is still on the review queue, got {result.declared_drops}")


def test_the_declared_loss_budget_is_three_percent_and_strictly_greater() -> None:
    """The boundary, at the default it was lowered to: 3%, strictly greater.

    The spec registered 5%. That was lowered on measurement: over the
    36-cell matrix, 5% fired only on `claude-haiku-4-5`, and
    `claude-sonnet-5` dropping both `{internal-notes}` markers on `index_429`
    -- 2 of 63 segments, 3.17% -- passed under it. The spec figure is
    superseded by the measurement.
    """
    check(config.DEFAULT_DECLARED_LOSS_BUDGET == 0.03,
          "the registered default budget is 3%, lowered on measurement from the "
          "original specification's 5%")

    exact = twenty(1)
    check(exact.segments == 20, f"the denominator must be 20 segments, got {exact.segments}")
    check(exact.loss == 0.05, f"one of twenty is exactly 5%, got {exact.loss}")
    check(any(item.kind == reconcile.DECLARED_LOSS_OVER_BUDGET for item in exact.findings),
          f"5% is over the 3% default now, got {kinds(exact)}")

    over = twenty(2)
    check(over.loss == 0.10, f"two of twenty is 10%, got {over.loss}")
    found = [item for item in over.findings if item.kind == reconcile.DECLARED_LOSS_OVER_BUDGET]
    check(len(found) == 1, f"10% is over the budget, got {kinds(over)}")
    check(any("2 of 20" in item.detail and "3%" in item.detail for item in found),
          f"the finding must carry the figure and the budget, it says "
          f"{[item.detail for item in found]}")


def test_the_boundary_is_strictly_greater_at_every_budget_not_just_five_percent() -> None:
    """The refactor gave `over_budget` a parameter; this is the
    proof it did not also give it a new comparison.

    The test above pins the boundary at the registered default, where a bug
    that read `>=` and a bug that read `>` differ by one drop in twenty. That
    is one point on one curve. Here the same property is asserted at four
    ceilings including 0.0 and 1.0: at budget B over N segments, exactly B*N
    drops passes and one more fails. If the comparison had slipped to `>=`,
    every one of the eight `passes` rows below would fail.

    B*N is chosen integral at each row so that "exactly the budget" is a
    reachable state rather than a rounding accident.
    """
    for budget, segments, allowed in ((0.0, 20, 0), (0.05, 20, 1),
                                      (0.25, 24, 6), (0.5, 24, 12)):
        check(not reconcile.over_budget(allowed, segments, budget),
              f"{allowed} of {segments} is exactly {budget}, and the rule is "
              f"strictly greater, so it must pass")
        check(reconcile.over_budget(allowed + 1, segments, budget),
              f"but {allowed + 1} of {segments} is over a ceiling of {budget}")

    # A ceiling of 1.0 cannot be exceeded: every segment dropped is 100%, which
    # is not strictly greater than 100%. That is what makes 1.0 the off switch
    # `report.budget_disables_check` reports rather than a very high ceiling.
    check(not reconcile.over_budget(20, 20, 1.0),
          "at a ceiling of 1.0 even a total loss is inside the budget")

    # The other two semantics the docstring names, at a non-default budget so
    # that neither can be satisfied by the constant it used to read.
    check(not reconcile.over_budget(5, 0, 0.25),
          "a zero denominator must decline to fire, not divide by zero")
    check(not reconcile.over_budget(0, 0, 0.0),
          "including at a ceiling of zero, where the quotient is undefined too")


def test_the_budget_counts_dropped_and_not_subsumed() -> None:
    """The declared-loss budget's scope note. At `high`, compression is the requested behaviour."""
    merged = TWENTY["source_a.md"] + "Every one of them is also noted here.\n"
    records = tuple(
        {"segment": f"b{index + 1}", "disposition": "subsumed",
         "replacement": "Every one of them is also noted here.",
         "reason": "folded into one sentence"}
        for index in range(10)
    )
    result = reconcile.findings(
        reconcile.reconcile(TWENTY, merged), records,
        fidelity="high", title_policy="keep-base", base="source_a.md",
        budget=config.DEFAULT_DECLARED_LOSS_BUDGET,
    )
    check(result.findings == (),
          f"ten of twenty subsumed at high is 0% declared loss, got {kinds(result)}")
    check(result.loss == 0.0, f"subsumed is not dropped, got {result.loss}")


def test_the_invariant_core_is_checked_at_every_level_and_reads_no_record() -> None:
    """The invariant core, and check 5: this one consults no disposition and no level.

    `30 seconds` rendered as `30s` is exactly the abbreviation the rule forbids,
    and the merge is free to say it declared the rewrite -- the invariant core is
    outside the slider, so the declaration buys nothing at any of the four
    levels.
    """
    abbreviated = CLEAN_MERGE.replace("The connect timeout is 30 seconds.",
                                      "The connect timeout is 30s.")
    for level in reconcile.PERMITTED:
        result = reconciled(abbreviated, CLEAN_DISPOSITIONS + (
            {"segment": "a3", "disposition": "reworded",
             "replacement": "The connect timeout is 30s.", "reason": "shortened"},
        ), fidelity=level)
        found = [item for item in result.findings
                 if item.kind == reconcile.VERBATIM_VIOLATION]
        check(len(found) == 1 and "'30'" in found[0].detail,
              f"at {level} the lost token must be reported, got "
              f"{[item.detail for item in found]}")
        check(found and found[0].document == "source_a.md" and found[0].segment == "a3",
              f"at {level} the finding must name where the token came from, got {found}")

    # A declared drop is the one shelter, and here is why. This check used
    # to fire here too — the number leaves the merge with the sentence — and
    # that was harmless only while `findings` reached no exit code. Wired into
    # the pipeline it makes every declared drop of a segment carrying a number,
    # unit, URL or fenced block a finding, which is most segments worth
    # dropping, and the findings-versus-review-queue split and the loss budget would never decide anything.
    # A withdrawn token has not drifted; it went with the segment, and the
    # review queue owns it.
    dropped = reconciled(
        CLEAN_MERGE.replace("The connect timeout is 30 seconds.\n", ""),
        CLEAN_DISPOSITIONS + (
            {"segment": "a3", "disposition": "dropped", "replacement": "", "reason": "gone"},
        ),
        fidelity="high",
    )
    check(reconcile.VERBATIM_VIOLATION not in kinds(dropped),
          f"a declared drop withdraws its token rather than losing it, got "
          f"{kinds(dropped)}")

    # The shelter is exactly as wide as the record, and the record is the whole
    # test — not "and the segment really is absent". `Located.verdict` calls a
    # segment `reworded` on a similarity score, and it does so here: with a3
    # removed outright, its nearest merge segment still scores above the
    # threshold. Gating the exemption on `ABSENT` would therefore not even fire
    # on this document, and gating it on `REWORDED` would put a heuristic inside
    # the one part of the module that is meant to be checkable by hand.
    #
    # So a `dropped` record that is a lie buys silence here, and is caught in
    # two other places instead: `grade_declarations` rejects it, because the
    # claims of a segment the merge kept do not come back MISSING, and a value
    # that changed in a kept segment is a CONTRADICTED claim and a finding on
    # its own. Check 2 already makes exactly this trade for any record at all.
    check("a3" not in {item.segment for item in dropped.findings},
          f"a `dropped` record silences this check on its own segment and on no "
          f"other; got {[(i.kind, i.segment) for i in dropped.findings]}")
    kept = reconciled(
        CLEAN_MERGE.replace("The connect timeout is 30 seconds.",
                            "The connect timeout here is 30s."),
        CLEAN_DISPOSITIONS,
        fidelity="high",
    )
    violations = [item for item in kept.findings
                  if item.kind == reconcile.VERBATIM_VIOLATION]
    check(len(violations) == 1 and "'30'" in violations[0].detail,
          f"an undeclared segment whose number changed is still a finding, which "
          f"is what the exemption above is narrower than; got {kinds(kept)}")


def test_the_merged_title_is_copied_from_a_source_and_never_written() -> None:
    """Title policy's load-bearing half, and the only thing that can catch a lost title.

    `decompose.md` is told to skip headings, so no claim is ever extracted from
    a title, so neither verify pass can fail a dropped one at any level.
    """
    invented = reconciled(CLEAN_MERGE.replace("# Relay Handbook",
                                              "# Relay Handbook and Notes"))
    check(reconcile.TITLE_NOT_FROM_SOURCE in kinds(invented),
          f"a combined title is written, not copied, got {kinds(invented)}")

    untitled = reconciled("The relay listens on port 8443.\n"
                          "The connect timeout is 30 seconds.\n"
                          "The read timeout is 45 seconds.\n")
    found = [item for item in untitled.findings if item.kind == reconcile.TITLE_NOT_FROM_SOURCE]
    check(len(found) == 1 and any("no title" in item.detail for item in found),
          f"a merge that dropped both titles must be caught, got "
          f"{[(item.kind, item.detail) for item in untitled.findings]}")

    # And the case where there is nothing to check: two untitled sources cannot
    # produce a title finding in either direction.
    plain = {"source_a.md": "The relay listens on port 8443.\n",
             "source_b.md": "The read timeout is 45 seconds.\n"}
    neither = reconciled("The relay listens on port 8443.\nThe read timeout is 45 seconds.\n",
                         (), sources=plain)
    check(neither.findings == (),
          f"no source title means no title rule to break, got {kinds(neither)}")

    # The case that raised this, and the reason the early return went. Same two
    # untitled sources, but the merge writes a heading anyway. Nothing else can
    # see it: no claim is ever drawn from a title, so if these checks return
    # early here, a title invented from nothing is the one kind of invention
    # under no constraint at all.
    from_nothing = reconciled("# Relay Handbook\n\nThe relay listens on port 8443.\n"
                              "The read timeout is 45 seconds.\n", (), sources=plain)
    found = [item for item in from_nothing.findings
             if item.kind == reconcile.TITLE_NOT_FROM_SOURCE]
    # The wording was narrowed with the condition: firing now means the text
    # is in no source *at all*, which is what the earlier case was protecting
    # against. A title the tool cannot see but the merge carried unchanged is quiet.
    check(len(found) == 1 and "occurs in no source document" in found[0].detail,
          f"a title invented where no source has one must be a finding, got "
          f"{[(item.kind, item.detail) for item in from_nothing.findings]}")

    # The same merge under `synthesise`, which is the one policy that permits a
    # written title. Nothing fires: the title is graded as a claim by
    # `merge.verify_title`, and that call *is* made here, because its only
    # short-circuit is `merged_title in candidates` and there are no candidates.
    #
    # The early return this sits beside predates that fix and did not know about the
    # policy, so it fired the earlier case's shape rule on exactly the output
    # `synthesise` exists to produce. `TITLE_NOT_FROM_SOURCE` is a document
    # finding, so a correct synthesised title over sources carrying no heading
    # exited 1 -- and untitled sources are the ordinary case for pasted text,
    # which is what the web interface receives.
    written = reconciled(
        "# Relay Handbook\n\nThe relay listens on port 8443.\n"
        "The read timeout is 45 seconds.\n", (), sources=plain,
        title_policy="synthesise")
    check(not [item for item in written.findings
               if item.kind == reconcile.TITLE_NOT_FROM_SOURCE],
          f"under synthesise a written title is graded as a claim by "
          f"verify_title, not as a string here, got {kinds(written)}")

    # The must-fire half, so the exemption cannot spread: `choose-best` never
    # writes a title, so the same merge is still invention under it.
    chosen = reconciled(
        "# Relay Handbook\n\nThe relay listens on port 8443.\n"
        "The read timeout is 45 seconds.\n", (), sources=plain,
        title_policy="choose-best")
    check([item for item in chosen.findings
           if item.kind == reconcile.TITLE_NOT_FROM_SOURCE],
          f"choose-best may not write a title, so this stays a finding, got "
          f"{kinds(chosen)}")


def test_keep_base_takes_the_base_title_and_choose_best_takes_any() -> None:
    """The two policies differ on one question and agree on everything else."""
    other = CLEAN_MERGE.replace("# Relay Handbook", "# Relay Notes")
    superseding_a = (
        {"segment": "a1", "disposition": "superseded",
         "replacement": "Relay Notes", "reason": "names the subject more fully"},
        CLEAN_DISPOSITIONS[1],
    )

    under_keep = reconciled(other, superseding_a)
    found = [item for item in under_keep.findings if item.kind == reconcile.TITLE_NOT_FROM_SOURCE]
    check(len(found) == 1 and any("Relay Handbook" in item.detail for item in found),
          f"keep-base requires the base's title, got "
          f"{[(item.kind, item.detail) for item in under_keep.findings]}")

    under_best = reconciled(other, superseding_a, title_policy="choose-best")
    check(under_best.findings == (),
          f"choose-best permits any document's title, got {kinds(under_best)}")

    # The invariant holds under every policy that decides the question here: a
    # title neither document carries is a finding. `synthesise` is excluded by
    # name rather than by a filter, because the exclusion is the design and a
    # filter would hide a policy added later that quietly stopped being checked.
    BYTE_IDENTICAL = tuple(p for p in config.TITLE_POLICIES if p != "synthesise")
    check(set(BYTE_IDENTICAL) == {"keep-base", "choose-best"},
          f"a new title policy must declare whether `reconcile` decides its "
          f"titles; got {config.TITLE_POLICIES}")
    for policy in BYTE_IDENTICAL:
        invented = reconciled(CLEAN_MERGE.replace("# Relay Handbook", "# Relay Overview"),
                              title_policy=policy)
        check(reconcile.TITLE_NOT_FROM_SOURCE in kinds(invented),
              f"under {policy} an invented title is still invented, got {kinds(invented)}")

    # And `synthesise` does not lose the invariant, it relocates it:
    # `reconcile` grades no claims, so an invented title there is caught by
    # `merge.verify_title` against the sources instead. Asserted so the
    # coverage cannot go missing silently, the deterministic stand-in was
    # falsified, and an exclusion with nothing behind it would read like a passed check.
    under_synth = reconciled(CLEAN_MERGE.replace("# Relay Handbook", "# Relay Overview"),
                             title_policy="synthesise")
    check(reconcile.TITLE_NOT_FROM_SOURCE not in kinds(under_synth),
          f"synthesise leaves the title to the semantic check, got {kinds(under_synth)}")
    import merge_title_guard  # noqa: F401  -- the probe that holds the other half


def test_keep_base_falls_back_when_the_base_has_no_title() -> None:
    """Title policy's carve-out: the one case where keep-base is plainly wrong."""
    sources = {"source_a.md": "The relay listens on port 8443.\n", "source_b.md": TITLED_B}
    merged = "# Relay Notes\n\nThe relay listens on port 8443.\nThe read timeout is 45 seconds.\n"
    result = reconciled(merged, (), sources=sources)
    check(result.findings == (),
          f"with no base title the first non-empty one is taken, got {kinds(result)}")

    wrong = reconciled(merged.replace("# Relay Notes", "# Relay Digest"), (), sources=sources)
    check(reconcile.TITLE_NOT_FROM_SOURCE in kinds(wrong),
          f"the fallback is still a copy, not a licence, got {kinds(wrong)}")


def test_a_title_that_lost_must_say_so() -> None:
    """Title policy: a title is never dropped in silence. The silence was the failure."""
    silent = reconciled(dispositions=(CLEAN_DISPOSITIONS[1],))
    found = [item for item in silent.findings if item.kind == reconcile.TITLE_NOT_SUPERSEDED]
    check([(item.segment, item.document) for item in found] == [("b1", "source_b.md")],
          f"b1's title lost and said nothing, so one finding naming it in source_b.md; got "
          f"{[(item.kind, item.segment, item.document) for item in silent.findings]}")

    wrong_kind = reconciled(dispositions=(
        {"segment": "b1", "disposition": "duplicate",
         "replacement": "Relay Handbook", "reason": "same title"},
        CLEAN_DISPOSITIONS[1],
    ))
    check(reconcile.TITLE_NOT_SUPERSEDED in kinds(wrong_kind),
          f"a losing title needs a superseded record specifically, got {kinds(wrong_kind)}")

    # Title policy names the pointer as well as the verb, the record replaces the
    # losing title *with the chosen one*. A superseded record aimed at some
    # other span of the merge satisfies check 3 and still loses the title.
    misdirected = reconciled(dispositions=(
        {"segment": "b1", "disposition": "superseded",
         "replacement": "The read timeout is 45 seconds.", "reason": "folded in"},
        CLEAN_DISPOSITIONS[1],
    ))
    check(reconcile.TITLE_NOT_SUPERSEDED in kinds(misdirected),
          f"a superseded title must be replaced by the merged title, got {kinds(misdirected)}")

    # And the notation around it is not the pointer: `# Relay Handbook` names
    # the same title as `Relay Handbook`.
    marked = reconciled(dispositions=(
        {"segment": "b1", "disposition": "superseded",
         "replacement": "# Relay Handbook", "reason": "the base document's title"},
        CLEAN_DISPOSITIONS[1],
    ))
    check(marked.findings == (),
          f"a heading marker is notation, not a different pointer, got {kinds(marked)}")

    # Two documents carrying the identical title need no record from either:
    # nothing lost, so nothing to declare.
    same = {"source_a.md": TITLED_A, "source_b.md": TITLED_A.replace(
        "The connect timeout is 30 seconds.", "The read timeout is 45 seconds.")}
    result = reconciled(CLEAN_MERGE, (CLEAN_DISPOSITIONS[1],), sources=same)
    check(not any(item.kind == reconcile.TITLE_NOT_SUPERSEDED for item in result.findings),
          f"an identical title lost nothing, got {kinds(result)}")


def test_a_staple_of_two_titled_sources_loses_a_title_and_is_charged_for_it() -> None:
    """The primary is immune to concatenation.

    Forward coverage rewards a glued merge with 100% — every source segment is
    present, because nothing was touched. The one thing a staple cannot do is
    keep both titles, and it declares nothing, so `title_not_superseded` fires
    on exactly the merge that coverage cannot fault. That is the property the
    task-42 primary is chosen for, so it is asserted here rather than described
    in the pre-registration alone.
    """
    for fixture in ("dedup", "conflict_surfaced", "attribution_swapped", "paraphrase"):
        sources = sources_of(fixture)
        titles = {
            title.text
            for text in sources.values()
            for title in reconcile.titles_of(segment_document(text, "s").segments)
        }
        check(len(titles) == 2,
              f"{fixture} must carry two distinct source titles for this case; got {titles}")

        glued = sources["source_a.md"].rstrip() + "\n\n" + sources["source_b.md"].lstrip()
        result = reconcile.reconcile(sources, glued)
        check(result.present == result.total,
              f"{fixture}: a staple keeps every segment, so coverage is "
              f"{result.total}/{result.total}; got {result.present}/{result.total}")
        check(result.order.stapled, f"{fixture}: a glued merge was not read as a staple")

        found = reconcile.findings(result, (), fidelity="off",
                                   title_policy="keep-base", base="source_a.md",
                                   budget=config.DEFAULT_DECLARED_LOSS_BUDGET)
        charged = [item for item in found.findings
                   if item.kind == reconcile.TITLE_NOT_SUPERSEDED]
        check(len(charged) == 1,
              f"{fixture}: one title lost in silence, so one finding; got "
              f"{[(item.kind, item.segment) for item in found.findings]}")


def test_the_permitted_matrix_agrees_with_what_the_model_is_told() -> None:
    """One rule, written twice: the same lesson, so the second copy is checked.

    `reconcile.PERMITTED` is what the reconciler enforces and each
    `prompts/fidelity/*.merge.md` fragment is what the model is asked for. They
    were ported from one table and nothing but this holds them together.
    """
    for level, permitted in reconcile.PERMITTED.items():
        text = " ".join((PROMPTS / "fidelity" / f"{level}.merge.md").read_text(
            encoding="utf-8").split())
        match = re.search(r"((?:\w+, )*\w+(?: and \w+)?) (?:are|remains a?) defects?", text)
        check(match is not None,
              f"{level}.merge.md must name what is a defect at its level; nothing matched")
        if match is None:
            continue
        named = set(re.findall(r"\w+", match.group(1))) & set(parsing.DISPOSITIONS)
        check(named == set(parsing.DISPOSITIONS) - set(permitted),
              f"{level}.merge.md calls {sorted(named)} defects; the matrix permits "
              f"{sorted(permitted)}, so it should call "
              f"{sorted(set(parsing.DISPOSITIONS) - set(permitted))} defects")


def test_a_fact_the_merge_states_twice_is_a_finding() -> None:
    """Check 9. The value was always computed; this is it being reported."""
    twice = CLEAN_MERGE + "The read timeout is 45 seconds.\n"
    result = reconciled(twice)
    found = [item for item in result.findings if item.kind == reconcile.DUPLICATED_CONTENT]
    check(len(found) == 1, f"one repeated line is one finding, got {kinds(result)}")
    if found:
        check("2 times" in found[0].detail,
              f"the detail must say how many times, got {found[0].detail!r}")
        check("read timeout is 45 seconds" in found[0].detail.lower(),
              f"the detail must quote the repeated text, got {found[0].detail!r}")
        check(found[0].segment == "" and found[0].document == "",
              "the fault is in the merge, which is not a source and carries no segment id")


def test_a_near_repeat_is_measured_and_deliberately_not_a_finding() -> None:
    """`NEAR_MATCH` was sized for the coverage pass and does not carry here.

    The pair below is what `duplication` calls a near repeat -- two different
    values in one sentence template. Promoting that half would make a finding
    out of the shape `tests/fixtures/contradiction` is built on.
    """
    paraphrased = CLEAN_MERGE + "The read timeout is 90 seconds.\n"
    measured = reconcile.reconcile(PAIR, paraphrased)
    near = [item for item in measured.duplicates if not item.exact]
    check(len(near) == 1,
          f"the near pass must still measure it, got {[d.text for d in measured.duplicates]}")
    check(not any(item.exact for item in measured.duplicates),
          "a paraphrase is not an exact repeat")
    result = reconciled(paraphrased)
    check(not [item for item in result.findings if item.kind == reconcile.DUPLICATED_CONTENT],
          f"a near repeat must not become a finding, got {kinds(result)}")


def test_two_sections_with_the_same_heading_are_not_a_duplication_finding() -> None:
    """Structure is not a fact stated twice, at the findings layer as well."""
    headed = (
        "# Relay Handbook\n\n"
        "## Timeouts\n\n"
        "The relay listens on port 8443.\n"
        "The connect timeout is 30 seconds.\n\n"
        "## Timeouts\n\n"
        "The read timeout is 45 seconds.\n"
    )
    result = reconciled(headed)
    check(not [item for item in result.findings if item.kind == reconcile.DUPLICATED_CONTENT],
          f"a repeated heading is structure, not duplication; got {kinds(result)}")


def test_the_duplication_finding_fires_on_nothing_the_corpus_calls_correct() -> None:
    """The false-positive floor for check 9, asserted rather than remembered.

    Twenty-five documents: the nine answer keys in `tests/pairs` and the sixteen
    fixture merges. The argument for promoting the exact half and not the
    near half rests on this number, so the suite has to hold it rather than
    a findings file having once measured it. The set has grown over time,
    from 20 to 21, 23, 24 and 25, and each time it grew the floor was
    re-measured here rather than carried forward.

    Two of the twenty-five are members the corpus does *not* call correct --
    `concatenated`, a hand-written concatenation of two overlapping sources, and
    `restated`, a real `--fidelity low` merge that keeps both sources' wording of
    every fact. Both belong in this floor and their presence is the sharper form
    of the same claim: check 9's exact pass does not fire even on the two
    documents the corpus keeps as examples of the defect, because in each the two
    copies are two wordings rather than one repeated string. The claim-level half
    is what fires on `restated`, and it reads claims rather than segments.
    """
    controls = sorted((ROOT / "tests" / "pairs").glob("*/ideal.md"))
    controls += sorted(FIXTURES.glob("*/merged.md"))
    check(len(controls) == 25,
          f"expected 9 answer keys and 16 fixture merges, got {len(controls)}")
    fired = []
    for path in controls:
        merged = segment_document(path.read_text(encoding="utf-8"), reconcile.MERGE_LETTER)
        if any(item.exact for item in reconcile.duplication(merged.segments)):
            fired.append(f"{path.parent.name}/{path.name}")
    check(not fired, f"check 9 must not accuse a document the corpus calls correct; fired on {fired}")


def test_a_duplication_finding_never_reaches_the_model_as_retry_feedback() -> None:
    """The boundary at `parsing.py`'s `check_merge` docstring, asserted.

    A reconciler finding is the tool's verdict on the merge. `check_merge`'s
    output is fed back verbatim on retry and is therefore a prompt, so putting
    check 9 there would be the tool asking the model to negotiate its own
    result away. The kind must not be reachable from the leaf module.
    """
    leaf = (ROOT / "src" / "llossless" / "parsing.py").read_text(encoding="utf-8")
    check(reconcile.DUPLICATED_CONTENT not in leaf,
          "parsing.py must not name the duplication finding; it would become retry feedback")
    for kind in reconcile.FINDING_KINDS:
        check(kind not in leaf, f"parsing.py names {kind!r}; reconciler findings are not prompts")


def test_the_reconciler_asks_nothing_of_a_model() -> None:
    """The acceptance criterion, and it is a property of the source rather than a run.

    Asserted by reading the module: `findings` and everything it calls live in
    a file that imports no client, names no model and opens no socket. The
    socket guard installed at the top of this file is the other half -- it would
    have failed the whole module had any check above reached the network.
    """
    source = (ROOT / "src" / "llossless" / "reconcile.py").read_text(encoding="utf-8")
    for forbidden in ("client", "Client", "complete(", "requests", "urllib", "socket"):
        check(forbidden not in source,
              f"reconcile.py must not mention {forbidden!r}; the reconciliation is mechanical")
    check(reconcile.FINDING_KINDS == tuple(sorted(set(reconcile.FINDING_KINDS),
                                                  key=reconcile.FINDING_KINDS.index)),
          "the finding kinds must be distinct")
    check(len(reconcile.FINDING_KINDS) == 12,
          f"twelve kinds: the original nine, the rewording half of check 2 "
          f"split off from absence, the false-departure half of it added later, "
          f"and the prompt-example leak, which this module names but "
          f"does not produce; got {len(reconcile.FINDING_KINDS)}")
    check(reconcile.CHECKS == 9,
          f"check 2 gaining a third kind must not move the check count: the two "
          f"directions of one contract sentence are one check, got "
          f"{reconcile.CHECKS}")
    # The one kind here that `findings()` never emits, pinned in both directions
    # so neither drifts: no numbered check may construct it, and the module must
    # still name it, because the renderers key off `FINDING_KINDS` to print it.
    check(reconcile.PROMPT_EXAMPLE_LEAK in reconcile.FINDING_KINDS,
          "the leak kind must stay in FINDING_KINDS or the report cannot render it")
    code = [line for line in source.splitlines() if not line.lstrip().startswith("#")]
    # Was a line count of two -- the definition and the `FINDING_KINDS` entry --
    # until every kind gained a family and made it three. A count was
    # the wrong instrument anyway: it fails on a line that merely mentions the
    # name, and would pass on an emission that replaced a mention. What the
    # rule forbids is *construction*, so that is what is asserted now, with
    # the mentions held to the three places entitled to hold one.
    mentions = [line for line in code if "PROMPT_EXAMPLE_LEAK" in line]
    built = [line for line in mentions if "Finding(" in line]
    check(not built,
          f"reconcile.py must never construct the leak kind; that belongs to "
          f"merge.example_content_leaks, wired in cli.py. Got {built}")
    check(reconcile.PROMPT_EXAMPLE_LEAK in reconcile.DOCUMENT_FINDINGS,
          "the leak kind is filed as a document finding; a kind in "
          "neither family silently stops moving the exit code")
    check(len(mentions) == 3,
          f"the leak kind belongs in exactly three places -- its definition, "
          f"FINDING_KINDS, and one family. Got {mentions}")
    # The count the reader is shown, which stopped being the count of names when
    # check 2 was split. Read off the module's own numbering rather than from a
    # second list, so a tenth check cannot be added and left uncounted.
    numbered = {
        int(part)
        for match in re.findall(r"^    # (\d+(?: and \d+)?)[.,]", source, re.M)
        for part in match.split(" and ")
    }
    check(numbered == set(range(1, reconcile.CHECKS + 1)),
          f"findings() numbers its checks {sorted(numbered)}, which is not "
          f"1..{reconcile.CHECKS}; reconcile.CHECKS and the code disagree")
    check(reconcile.CHECKS == 9,
          f"nine checks, the first being the integrity check that the other "
          f"eight presume; "
          f"got {reconcile.CHECKS}")


def test_a_block_of_one_segment_is_not_a_block() -> None:
    """The `blocked` guard, on the two reference merges that motivated it.

    `runs == distinct` is satisfied for free by a source that contributed one
    segment, so before this guard the predicate called two *correct* merges
    concatenations: `attribution_invented` on the sequence `aab` and
    `structure_added` on `abb`. The docstring on `Order` reasons about
    `structure_added-off-0`'s a, b, b already and excludes it by `monotone` --
    which works on the recorded merge and not on the reference one, because
    that exclusion depends on the order of B's two segments rather than on
    there being only one of A's.
    """
    for fixture, sequence in (("attribution_invented", "aab"), ("structure_added", "abb")):
        order = reconcile.reconcile(
            sources_of(fixture),
            (FIXTURES / fixture / "merged.md").read_text(encoding="utf-8"),
        ).order
        check("".join(order.sequence) == sequence,
              f"{fixture}: sequence is {''.join(order.sequence)!r}, expected {sequence!r}; "
              f"the fixture changed and this guard is no longer being exercised")
        check(not order.blocked, f"{fixture}: {sequence} has a source contributing one segment")
        check(not order.stapled, f"{fixture}: a correct merge was called a concatenation")


def test_a_superseded_numeral_carried_by_the_surviving_wording_is_not_a_violation() -> None:
    """Three directions, because the carve-out has a condition.

    `merge.md` wants a numeral copied character for character and the rule wants one
    wording to survive. Where two sources write "two billion" against
    "2,000,000,000" both cannot hold: keeping either loses a numeral, keeping
    both states the fact twice. The verbatim rule yields exactly there, and
    only where the declared replacement resolves -- which is the evidence that
    the content survived rather than the claim that it did.
    """
    sources = {"source_a.md": "# G\n\nIt has over two billion adherents.\n",
               "source_b.md": "# G\n\nIt has over 2,000,000,000 followers.\n"}
    merged = "# G\n\nIt has over two billion adherents.\n"

    def violations(dispositions):
        result = reconcile.reconcile(sources, merged)
        return [f for f in reconcile.findings(
            result, dispositions, fidelity="off", title_policy="keep-base",
            base="source_a.md",
            budget=config.DEFAULT_DECLARED_LOSS_BUDGET).findings
            if f.kind == reconcile.VERBATIM_VIOLATION]

    carried = ({"segment": "b2", "disposition": "superseded",
                "replacement": "It has over two billion adherents.",
                "reason": "A's wording was kept"},)
    dangling = ({"segment": "b2", "disposition": "superseded",
                 "replacement": "a span that is nowhere in the merge",
                 "reason": "A's wording was kept"},)
    check(not violations(carried),
          f"a superseded numeral whose replacement resolves is carried by the "
          f"surviving wording: {violations(carried)}")
    check(violations(dangling),
          "a superseded record whose replacement does not resolve is no "
          "evidence the content survived, so the token is still a finding")
    check(violations(()),
          "with no record at all the numeral simply vanished and must fire")


def test_trailing_punctuation_is_not_part_of_a_numeral() -> None:
    """Trailing only: interior separators are the value.

    `AD 30-33,` is one token with an ASCII hyphen and two with an en dash,
    which the range pattern does not know: `30` and `33,`, the second carrying
    the sentence comma. At `high` the model split the sentence, the comma
    became a stop, and `33,` was reported as a numeral that did not survive.
    """
    en_dash = [span.text for span in segment.find_spans("around AD 30\u201333, whose")]
    check("33" in en_dash and "33," not in en_dash,
          f"the sentence comma is not part of the number: {en_dash}")
    for text, token in (("with over 2,000,000,000 followers", "2,000,000,000"),
                        ("handles 1,000 connections.", "1,000"),
                        ("around AD 30-33, whose", "30-33")):
        spans = [span.text for span in segment.find_spans(text)]
        check(token in spans,
              f"interior separators are part of the value and must not move: "
              f"expected {token!r} in {spans}")


def test_a_title_the_tool_cannot_see_is_not_an_invented_one() -> None:
    """Both directions, on documents with no heading markup at all.

    The title heuristic wants a short unpunctuated line *standing alone*. A
    plain-text source whose first line runs straight into the body has no title
    segment; a merge that puts a blank line after the same line has one. The
    line was carried unchanged and reported as invented -- a finding about this
    module's own definition rather than about the merge. The earlier protection
    is what had to survive: a title in no source at all is still invention.
    """
    sources = {
        "source_a.md": "How to keep bees\nStart with two hives, not one.\n",
        "source_b.md": "Beekeeping basics\nTwo hives let you compare.\n",
    }
    carried = "How to keep bees\n\nStart with two hives, not one.\n"
    invented = "A Complete Guide To Bees\n\nStart with two hives, not one.\n"

    def titles(merged: str) -> list[str]:
        result = reconcile.reconcile(sources, merged)
        return [f.kind for f in reconcile.findings(
            result, {}, fidelity="off", title_policy="keep-base",
            base="source_a.md",
            budget=config.DEFAULT_DECLARED_LOSS_BUDGET).findings
            if f.kind == reconcile.TITLE_NOT_FROM_SOURCE]

    check(not titles(carried),
          f"a first line carried from a source must not read as invented just "
          f"because no source line stood alone: {titles(carried)}")
    check(titles(invented) == [reconcile.TITLE_NOT_FROM_SOURCE],
          f"a title in neither source is still invention and must fire: "
          f"{titles(invented)}")


def test_the_staple_predicate_fires_on_nothing_the_corpus_calls_correct() -> None:
    """The same 24-document floor check 9 is held to, applied to `order.stapled`.

    Two documents fire and they are the two disjoint controls, whose
    reference merges are byte-exactly `source_a + source_b` because in
    each case the two sources share no subject. Both firings are
    correct, which is precisely why `stapled` is not a finding kind:
    the corpus contains documents the predicate is right about and
    requires to exit 0.

    The set now also contains `concatenated`, and `restated`, which *are*
    the defect: two overlapping sources glued together whole, and which
    this predicate does **not** fire on, because in both the sources
    alternate paragraph by paragraph (`order.sequence` `aababababab` on
    `concatenated`) instead of arriving in two blocks. So the two firings
    here are still the two correct staples, and the absence of a third
    and a fourth is the measured blind spot rather than a clean bill of health.
    """
    controls = sorted((ROOT / "tests" / "pairs").glob("*/ideal.md"))
    controls += sorted(FIXTURES.glob("*/merged.md"))
    check(len(controls) == 25,
          f"expected 9 answer keys and 16 fixture merges, got {len(controls)}")
    fired = []
    for path in controls:
        documents = {
            name: (path.parent / name).read_text(encoding="utf-8")
            for name in SOURCES
        }
        if reconcile.reconcile(documents, path.read_text(encoding="utf-8")).order.stapled:
            fired.append(path.parent.name)
    check(fired == ["disjoint_domains", "disjoint_sources"],
          f"the staple predicate fired on {fired}; the two disjoint controls are the "
          f"corpus's only correct staples")


def test_a_correct_concatenation_produces_no_finding() -> None:
    """The two disjoint controls are the reason the measurement is not promoted.

    Each `expected.json` requires exit 0 in both strict and lenient modes, and
    `report.exit_code` returns 1 for any structural finding at all. A tenth
    finding kind reading `order.stapled` would therefore contradict two fixtures
    registered `"kind": "guard"` -- guards whose whole purpose is that the tool
    must not punish the correct merge of two unrelated documents. Held over both
    rather than over `disjoint_sources` alone: one control is one
    document, and a rule that survives one document is not yet a rule.
    """
    for name in ("disjoint_sources", "disjoint_domains"):
        fixture = FIXTURES / name
        expected = json.loads((fixture / "expected.json").read_text(encoding="utf-8"))
        check(expected["kind"] == "guard", f"{name} is no longer registered as a guard")
        check(expected["expected_exit_code"] == {"strict": 0, "lenient": 0},
              f"{name} no longer requires exit 0: {expected['expected_exit_code']}")
        result = reconcile.reconcile(
            sources_of(name),
            (fixture / "merged.md").read_text(encoding="utf-8"),
        )
        check(result.order.stapled,
              f"{name}' reference merge no longer reads as a staple")
        kinds = {finding.kind for finding in reconcile.findings(
            result, {}, fidelity="off", title_policy="keep-base", base="source_a.md",
            budget=config.DEFAULT_DECLARED_LOSS_BUDGET).findings}
        check("stapled" not in kinds and "staple" not in " ".join(kinds),
              f"a staple finding reached {name}, which the corpus requires to exit 0: "
              f"{sorted(kinds)}")


def test_the_order_measurement_is_not_a_finding_kind() -> None:
    """The boundary, asserted rather than left for the reader to infer.

    Everything in `FINDING_KINDS` is a verdict `report.exit_code` counts. The
    order analysis is reported beside them and must never join them, because a
    concatenation is the correct answer whenever the sources had nothing to
    interleave and no mechanical test tells that case from a weld.
    """
    for kind in reconcile.FINDING_KINDS:
        check("staple" not in kind and "order" not in kind and "concat" not in kind,
              f"{kind!r} looks like the order measurement promoted to a verdict")
    heading_source = (ROOT / "src" / "llossless" / "report.py").read_text(encoding="utf-8")
    check("def order_line(" in heading_source,
          "report.py no longer renders the order measurement; it is back to being computed "
          "and never read, which is exactly what it must not be")


def test_added_line_breaks_are_counted_and_not_judged() -> None:
    """The count exists; it is not a finding and it is not vacuous.

    An earlier change made an interior line break recorded notation rather than a segment
    boundary, so that the partition could not move. The cost is that a merge
    which rewraps its sources adds structure no source carries and nothing in
    the tool says so -- `high.merge.md` licenses restructuring, so there is no
    rule to break and therefore no check to write. A count is what is left.

    Three assertions, because a counter is easy to ship blind: it fires on a
    merge that joined two lines, it stays at zero on a merge that kept the
    sources' own breaks, and it is nowhere near `FINDING_KINDS`.
    """
    # One source, one segment, two lines. Both merges carry the same facts.
    source = {"a.md": "The read timeout is 45 seconds\nand the write timeout is 10."}
    kept = reconcile.reconcile(
        source, "The read timeout is 45 seconds\nand the write timeout is 10.")
    check(kept.added_breaks == (),
          f"a merge that kept the source's own break added nothing: {kept.added_breaks}")

    joined = reconcile.reconcile(
        source, "The read timeout is 45 seconds and the write timeout is 10.")
    check(joined.added_breaks == (),
          f"removing a break is not adding one: {joined.added_breaks}")

    moved = reconcile.reconcile(
        source, "The read timeout is 45\nseconds and the write timeout is 10.")
    check(moved.added_breaks == (("45", "seconds"),),
          f"a break the source does not carry must be counted once, between the "
          f"two words it sits between: {moved.added_breaks}")

    # Not a verdict. The count rides in `structure`, beside the title block and
    # the decisions, and must never reach the block that drives the exit code.
    for kind in reconcile.FINDING_KINDS:
        check("break" not in kind,
              f"{kind!r} looks like the break count promoted to a verdict")
    check(reconcile.CHECKS == 9,
          f"the count is not a tenth check: {reconcile.CHECKS}")
    rendered = (ROOT / "src" / "llossless" / "report.py").read_text(encoding="utf-8")
    check("breaks_added_by_the_merge" in rendered,
          "the count is computed and never published; a measurement must reach the report")


def test_reconcile_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def test_check_five_is_byte_exact_inside_a_fence() -> None:
    """`flatten` collapsed the whitespace check 5 promises to preserve.

    The invariant core makes a fenced block invariant byte for byte, and check 5 is the
    check that enforces it. It compared the block through `flatten`, which
    collapses every run of whitespace, so a YAML block re-indented from four
    spaces to two -- which changes what it means -- produced no finding at all.
    """
    source = ("# Config\n\nThe relay listens on port 8443.\n\n"
              "```yaml\nserver:\n    host: relay\n    port: 8443\n```\n")
    reindented = source.replace("    host", "  host").replace("    port", "  port")

    fired = reconcile.reconcile({"source_a.md": source}, reindented)
    check([m for m in fired.missing if m.kind == "code_block"],
          f"a re-indented fence must fire check 5: {fired.missing}")

    quiet = reconcile.reconcile({"source_a.md": source}, source)
    check(not quiet.missing,
          f"an identical block must not fire: {quiet.missing}")

    crlf = reconcile.reconcile({"source_a.md": source}, source.replace("\n", "\r\n"))
    check(not crlf.missing,
          f"a CRLF-only difference is not a change to the block: {crlf.missing}")


# --------------------------------------------------------------------------
# Check 9's claim-level half
# --------------------------------------------------------------------------


def claim(text: str, line: int, anchored: bool = True) -> Claim:
    return Claim("X-001", "merged.md", text, line, text, anchored)


def test_a_restatement_is_one_claim_from_two_lines_and_nothing_else() -> None:
    """Every clause of the predicate, in both directions.

    Each `check` below is one clause of `reconcile.restatements`' docstring,
    and each was chosen against a measured case rather than a guess: the
    same-line pair is `toby-test-2 mid` and `disjoint_domains/source_b.md`,
    both of which repeat a claim without the document saying anything twice;
    the near-miss pair is why the predicate is equality and not similarity,
    since measurement found eight correct documents above the one positive a
    threshold would have to reach.
    """
    two_lines = [claim("The read timeout is 30 seconds.", 3),
                 claim("The read timeout is 30 seconds.", 7)]
    found = reconcile.restatements(two_lines)
    check([(f.text, f.lines) for f in found]
          == [("The read timeout is 30 seconds.", (3, 7))],
          f"one claim from two lines is a restatement, got {found}")
    check(len(reconcile.restated_findings(two_lines)) == 1,
          "a restatement must produce exactly one finding")
    check(all(f.kind == reconcile.DUPLICATED_CONTENT
              for f in reconcile.restated_findings(two_lines)),
          "the claim-level half widens DUPLICATED_CONTENT; it does not add a kind")

    one_line = [claim("The read timeout is 30 seconds.", 3),
                claim("The read timeout is 30 seconds.", 3)]
    check(not reconcile.restatements(one_line),
          "a decomposer emitting one fact twice from one line is noise, not a finding")

    nearly = [claim("The read timeout is 30 seconds.", 3),
              claim("The read timeout is thirty seconds.", 7)]
    check(not reconcile.restatements(nearly),
          "the predicate is equality: no similarity threshold separates the corpus")

    unanchored = [claim("The read timeout is 30 seconds.", 3, anchored=False),
                  claim("The read timeout is 30 seconds.", 7, anchored=False)]
    check(not reconcile.restatements(unanchored),
          "an unanchored line is the model's unchecked hint and may not carry a finding")

    half = [claim("The read timeout is 30 seconds.", 3),
            claim("The read timeout is 30 seconds.", 7, anchored=False)]
    check(not reconcile.restatements(half),
          "both copies must be anchored; one verified line does not make two")


def test_the_restatement_check_fires_on_the_merge_the_tool_passed() -> None:
    """The must-fire probe, and it is real output rather than a construction.

    `tests/fixtures/restated/merged.md` is byte for byte what
    `merge --fidelity low` returned for the two sources beside it,
    and the run that produced it exited **0 with no finding** -- that run's own
    report is where `recorded-claims.json` comes from. So this is the defect
    that stayed unclaimed until now, measured on the instrument that now claims it.

    The hand-written `concatenated` fixture cannot do this job and the corpus
    says so: three live samples of its `merged.md` returned ten byte-identical
    claims and zero cross-line repeats, because its two wordings of a fact are
    too far apart for a decomposer to resolve to one sentence. A detector whose
    must-fire probe has never fired is unproven, which is why this file is here.
    """
    recorded = json.loads(
        (FIXTURES / "restated" / "recorded-claims.json").read_text(encoding="utf-8"))
    claims = {name: [Claim(**item) for item in items]
              for name, items in recorded["claims"].items()}

    check(recorded["recorded_by"]["exit_code"] == 0
          and recorded["recorded_by"]["findings"] == 0
          and recorded["recorded_by"]["structural_findings"] == 0,
          f"the probe is a merge the tool passed clean; {recorded['recorded_by']}")

    found = reconcile.restatements(claims["merged.md"])
    check(len(found) == 23,
          f"the recorded merge states 23 facts twice; check 9 found {len(found)}")
    check(all(len(f.lines) == 2 for f in found),
          f"every repeat is one fact on two lines: {[f.lines for f in found]}")
    check(all(abs(f.lines[1] - f.lines[0]) == 1 for f in found),
          f"the two copies are always on consecutive lines -- A's paragraph then "
          f"B's: {[f.lines for f in found]}")

    for name in SOURCES:
        check(not reconcile.restatements(claims[name]),
              f"{name} states nothing twice; only the merge does")

    # The arithmetic, published beside the finding and never as the trigger
    # (decompose returned 18 claims on one run and 22 on the next
    # for an identical request). 65 > 30 + 33 is impossible for a merge that
    # states each fact once, and it is evidence rather than a test.
    merged, a, b = (len(claims["merged.md"]), len(claims["source_a.md"]),
                    len(claims["source_b.md"]))
    check((merged, a, b) == (65, 30, 33),
          f"the recorded run extracted 65 claims from the merge against 30 + 33 "
          f"from the sources; got {merged} against {a} + {b}")

    # And the half that must stay silent: two wordings are two strings, so the
    # exact segment pass sees nothing here. Both halves reading the same
    # document is what makes this fixture the pair of `concatenated`.
    document = segment_document(
        (FIXTURES / "restated" / "merged.md").read_text(encoding="utf-8"),
        reconcile.MERGE_LETTER)
    check(not [d for d in reconcile.duplication(document.segments) if d.exact],
          "the exact half must stay silent on a merge that repeats itself in "
          "two wordings; that blindness is why the claim-level half exists")


def test_restatements_fire_on_restated_alone_among_recorded_claim_sets() -> None:
    """Check 9's claim-level half over every claim the repository has recorded.

    Must fire: `restated/merged.md`, in every sample. It is the defect the half
    exists for -- a merge that keeps both sources' wordings, so the document
    says everything twice -- and its fixture is `guard` only because its verify
    probes imply exit 0 (its own `note` says so). Until the 27B import the
    corpus could not show this: qwen3:8b's claim lists for that document
    repeated nothing, so the recorded half was must-not-fire only and the
    firing lived in `recorded-claims.json`. The 27B's own lists repeat on two
    lines each, as the predicate requires.

    Must not fire: every other recorded document, which the corpus calls
    correct. The population is the recordings and not the fixtures,
    deliberately: iterating fixtures and skipping the ones that miss would be a
    sweep quietly shrinking its own denominator, so the count is pinned
    (`RECORDED_DOCUMENTS`) and a document with no recording is a failure.

    What this cannot cover is measured elsewhere: the
    nine `tests/pairs/*/ideal.md` answer keys have no cassettes at all, and were
    measured live on 2026-09-15 -- three samples each bar `index_429`, which
    completed one of 489 claims, and all nine silent.
    `library_holds` and `freezer_alarm` are the two that matter, since both are
    near-total concatenations of complementary documents that the corpus
    asserts are correct, and a predicate that fired on them would be useless.
    """
    import argparse

    from llossless.client import Client
    from llossless.decompose import decompose_text
    from llossless import prompts as prompt_files

    import replay_models

    try:
        model_argv = replay_models.replay_argv(roles=("decompose",))
    except AssertionError as exc:
        check(False, f"an offline replay has to be pinned to the model id the "
                     f"recordings were made with: {exc}")
        return
    parser = argparse.ArgumentParser()
    config.add_arguments(parser)
    # The cache goes to a scratch directory, not the package's default. One
    # 27B decompose cassette is a schema repair's second attempt, and replaying
    # it keeps the first attempt's raw body in `cache_dir/failures` even
    # offline; under `rehearse_publication` the default is the publication
    # copy's root, where a runtime cache is a refusal, as test_verify's
    # sweep test says for verify.
    import os
    import tempfile
    scratch = tempfile.TemporaryDirectory(prefix="llossless-reconcile-")
    was = os.environ.get("LLOSSLESS_CACHE_DIR")
    os.environ["LLOSSLESS_CACHE_DIR"] = scratch.name
    try:
        settings = config.resolve(parser.parse_args(["--offline", *model_argv]))
    finally:
        if was is None:
            del os.environ["LLOSSLESS_CACHE_DIR"]
        else:
            os.environ["LLOSSLESS_CACHE_DIR"] = was
    client = Client(settings)
    prompt = prompt_files.load("decompose")

    documents = [(name.name, document)
                 for name in sorted(FIXTURES.iterdir()) if name.is_dir()
                 for document in SOURCES + ("merged.md",)]
    recorded, missing, fired, restated = 0, [], [], []
    for sample in range(SAMPLES):
        client.sample = sample
        for fixture, document in documents:
            text = (FIXTURES / fixture / document).read_text(encoding="utf-8")
            try:
                claims = decompose_text(client, text, document, prompt)
            except MissingCassette:
                missing.append(f"{fixture}/{document}")
                continue
            recorded += 1
            found = reconcile.restatements(claims)
            if (fixture, document) == ("restated", "merged.md"):
                restated.append(len(found))
            elif found:
                fired.append(f"{fixture}/{document} sample {sample}: "
                             f"{[(f.text, f.lines) for f in found]}")
    scratch.cleanup()

    check(len(restated) == SAMPLES and all(restated),
          f"MUST FIRE: check 9's claim-level half must find repeats in "
          f"restated/merged.md in all {SAMPLES} samples; found {restated}")
    check(not fired,
          f"check 9's claim-level half must not accuse a document the corpus "
          f"calls correct; fired on {fired}")
    check(recorded == RECORDED_DOCUMENTS,
          f"the floor is {RECORDED_DOCUMENTS} recorded documents "
          f"({RECORDED_DOCUMENTS // SAMPLES} documents x {SAMPLES} samples); "
          f"replayed {recorded}, and {sorted(set(missing))} have no recording")


def test_open_excuses_a_covering_value_built_only_from_source_numbers() -> None:
    """Check 5's one exemption, and the three things that keep it narrow.

    Two documents giving a figure as 30-45% and 35-50% disagree about its
    edges. Carrying either alone asserts something the other document denies;
    carrying 30-50% asserts what both support -- and destroys two source tokens
    doing it, which check 5 refuses at every level below `open`.

    The exemption asks one question and it is not arithmetic: is every number
    in the replacement a number some document wrote? Nothing in this package
    parses a numeric value and this does not start. 30-60% is refused not
    because 60 is too large, which this cannot know, but because no document
    wrote it.

    Registered against the operator's own case (`toby-test-8`), where the
    reference merge took the union and scoring found it to be two violations
    plus a hallucination.
    """
    sources = {"source_a.md": "Weaker resale value (~30–45% after two years).\n",
               "source_b.md": "Weaker resale value (roughly 35–50% after two years).\n"}

    def violations(level: str, merged: str, disposition: str = "reconciled") -> int:
        records = tuple({"segment": seg, "disposition": disposition,
                         "replacement": merged.strip(), "reason": "covers both"}
                        for seg in ("a1", "b1"))
        result = reconciled(merged, records, sources=sources,
                            title_policy="keep-base", fidelity=level)
        return len([f for f in result.findings if f.kind == reconcile.VERBATIM_VIOLATION])

    union = "Weaker resale value (30–50% after two years).\n"

    check(violations("open", union) == 0,
          "a covering value whose every number is a number a document wrote is "
          "excused at open; this is the case the exemption exists for")
    check(violations("open", "Weaker resale value (35–45% after two years).\n") == 0,
          "the intersection is covered too -- both its edges are stated, and "
          "the rule is containment rather than which direction it moved")

    # The level. No level below open inherits this, or the exemption has
    # widened the one check that sits outside the slider.
    for level in ("off", "low", "mid", "high"):
        check(violations(level, union) > 0,
              f"{level} must still refuse a covering value; check 5 is outside "
              f"the slider and this exemption is the only hole in it")

    # The containment. A number no document wrote is an invention whatever the
    # record says, and this is the half a model could otherwise declare away.
    check(violations("open", "Weaker resale value (30–60% after two years).\n") > 0,
          "60 is in no source, so the widened range is not covered and stays a "
          "violation however confidently it was declared")
    check(violations("open", "Weaker resale value (32–48% after two years).\n") > 0,
          "neither edge is stated, so a plausible-looking narrowing is refused "
          "for the same reason a widening is")

    # The disposition. Only a declared reconciliation reaches the exemption; a
    # segment declared something else, or nothing, is unaffected.
    check(violations("open", union, disposition="reworded") > 0,
          "a reworded record earns nothing here -- the exemption is for a "
          "reconciliation, which is the record that names both candidates")


def test_an_undeclared_addition_still_fails_the_run() -> None:
    """The load-bearing test of the `open` level, and the one that must not bend.

    What a declaration buys is that a statement the sources do not carry is
    *listed* rather than reported as an invention. If an undeclared one were
    also excused, `open` would be a way to declare your way to a clean exit --
    the same hole the declared-loss budget exists to close one layer down, and
    the reason `Run.findings` subtracts a set of claim ids rather than
    filtering on whether any declaration exists.

    Three cases, and the third is the one a careless implementation passes: a
    merge that declared *something* must not thereby excuse a statement it did
    not declare.
    """
    from llossless.report import Run
    from llossless.verify import Verdict, MERGED_TO_SOURCES
    from llossless.decompose import Claim

    text = "Solar generation is now cheaper than new coal in most markets."
    claim = Claim(id="M-001", source="merged.md", text=text, line=3,
                  span=text, anchored=True)
    verdict = Verdict("M-001", "MISSING", "", "", "in no source",
                      MERGED_TO_SOURCES, "not_graded")

    def findings(additions) -> list[str]:
        run = Run(command="merge", claims={"merged.md": [claim]},
                  reverse=[verdict], additions=additions)
        return [v.finding for v in run.findings]

    check(findings(()) == ["hallucinated"],
          "an addition nobody declared is an invention, which is what it was "
          "before this level existed and what it must stay")

    declared = ({"statement": text, "corrects": "", "reason": "well established"},)
    check(findings(declared) == [],
          "the declared one is excused from the exit code and listed instead")

    other = ({"statement": "Wind generation fell in price again in 2024.",
              "corrects": "", "reason": "well established"},)
    check(findings(other) == ["hallucinated"],
          "a merge that declared a different statement has not declared this "
          "one; the excusal is per claim, never per run")

    # And the excused claim is still *reported*. An exemption that also hid the
    # statement would be worse than no exemption, because the reader would have
    # no way to review what the tool stopped checking.
    run = Run(command="merge", claims={"merged.md": [claim]},
              reverse=[verdict], additions=declared)
    check([v.claim_id for v in run.declared_additions] == ["M-001"],
          "an excused addition is listed, or the reader cannot review the one "
          "thing the tool has stopped checking")

    # A contradiction is not an addition. The sources denying a statement is a
    # different thing from their being silent about it, and no declaration
    # makes the first reportable-but-clean.
    denied = Verdict("M-001", "CONTRADICTED", "x", "source_a.md", "denied",
                     MERGED_TO_SOURCES, "grounded")
    run = Run(command="merge", claims={"merged.md": [claim]},
              reverse=[denied], additions=declared)
    check([v.finding for v in run.findings] != [],
          "a claim the sources contradict stays a finding however it was "
          "declared; the queue takes omissions and never assertions")


def test_one_declaration_covering_many_claims_is_attributed() -> None:
    """A blob declaration is permitted and must be *visible* as one.

    `added_claims` matches by containment both ways, so a single declared
    statement long enough to contain several claims excuses all of them. That
    is not a hole -- `open` reports additions rather than charging for them,
    and the banner counts the claims excused rather than the records declared,
    so the count a reader sees is the real one. What it would be is invisible:
    a section showing one row beside a banner saying four, with nothing tying
    them together and no way to tell one declaration covering four claims from
    four declarations covering one each.

    The second is what the level is for. The first is worth a second look, and
    a reader can only give it one if the report says which claims each
    declaration covered.
    """
    from llossless.report import Run, addition_sentence, additions_section
    from llossless.verify import Verdict, MERGED_TO_SOURCES
    from llossless.decompose import Claim

    texts = ("Solar is cheaper than coal.", "Wind fell in price in 2024.",
             "Grid storage doubled last year.", "Nuclear restarted in Japan.")
    claims, verdicts = [], []
    for i, text in enumerate(texts, 1):
        claim_id = f"M-{i:03d}"
        claims.append(Claim(id=claim_id, source="merged.md", text=text, line=i,
                            span=text, anchored=True))
        verdicts.append(Verdict(claim_id, "MISSING", "", "", "in no source",
                                MERGED_TO_SOURCES, "not_graded"))

    blob = " ".join(texts)
    run = Run(command="merge", claims={"merged.md": claims}, reverse=verdicts,
              additions=({"statement": blob, "corrects": "",
                          "reason": "one declaration"},))

    check(run.covering(blob) == ("M-001", "M-002", "M-003", "M-004"),
          f"the section must attribute every claim the blob covered: "
          f"{run.covering(blob)}")
    check("4 statement(s)" in addition_sentence(run),
          "the banner counts claims excused, not records declared, or one blob "
          "would report as one addition while excusing four")
    row = additions_section(run).splitlines()[-1]
    for claim_id in ("M-001", "M-002", "M-003", "M-004"):
        check(claim_id in row,
              f"{claim_id} was excused by this row and must appear on it: {row!r}")

    # The ordinary case: one statement, one claim, and the column does not
    # invent company for it.
    one = Run(command="merge", claims={"merged.md": claims[:1]},
              reverse=verdicts[:1],
              additions=({"statement": texts[0], "corrects": "",
                          "reason": "well established"},))
    check(one.covering(texts[0]) == ("M-001",),
          f"a single declaration covers the single claim: {one.covering(texts[0])}")

    # A declaration that bought nothing says so rather than going blank. Over-
    # declaring is not a defect -- the merge said it added something the
    # sources turn out to carry -- but a reader comparing the section to the
    # banner needs to see that this row moved no verdict.
    idle = Run(command="merge", claims={"merged.md": claims[:1]},
               reverse=verdicts[:1],
               additions=({"statement": "Something else entirely.",
                           "corrects": "", "reason": "unrelated"},))
    check(idle.covering("Something else entirely.") == (),
          "a declaration matching no claim covers nothing")
    check("*none*" in additions_section(idle).splitlines()[-1],
          "a row that excused nothing must say so, not leave the column empty")


def test_the_report_says_what_was_done_about_a_source_in_all_three_states() -> None:
    """Searched, did not search, unmeasured, and never the wrong one.

    "Nothing here has been checked against anything" was true while a model on
    this path could not reach the network. It is false about a run where the
    model searched, and saying it anyway would be misleading in the direction
    that matters least; saying "the model looked this up" about a run where it
    did not would be misleading in the direction that matters most. So the
    report states two facts and keeps them apart: what *this tool* did, which
    is nothing and never changes, and what the *model* did, which is a
    measurement with three values.

    `unmeasured` is not `not-searched`, and the fallback for a run carrying no
    provenance at all -- a fixture, a `verify` over somebody else's merge --
    has to land on the first. A run that never measured saying "the model made
    no web request" is this tool inventing a measurement, which is the one
    thing the whole feature is built against.
    """
    from llossless.report import NOT_RESOLVED, Run, sourcing_sentence
    from llossless.usage import Searches

    # The real shape, mirrored rather than shortened: `Run.searches` reads
    # `provenance.client.usage.searches`, and a fake that flattened a level
    # would pass over a reader looking in the wrong place.
    class FakeUsage:
        def __init__(self, searches): self.searches = searches

    class FakeClient:
        def __init__(self, searches): self.usage = FakeUsage(searches)

    class FakeProvenance:
        def __init__(self, searches): self.client = FakeClient(searches)

    blank = Run(command="merge")
    check(blank.searches is None,
          "a run with no provenance measured nothing, and says so by holding "
          "nothing rather than by holding a zero")
    check("unmeasured" in sourcing_sentence(blank),
          f"and the sentence for it is the unmeasured one: "
          f"{sourcing_sentence(blank)}")

    for block, state, must, must_not in (
            ({"server_tool_use": {"web_search_requests": 0,
                                  "web_fetch_requests": 0}},
             "not-searched", "no web request", "unmeasured"),
            ({"server_tool_use": {"web_search_requests": 2,
                                  "web_fetch_requests": 0}},
             "searched", "2 web request(s)", "no web request"),
            ({"input_tokens": 9}, "unmeasured", "unmeasured", "no web request"),
    ):
        tally = Searches()
        tally.add({"usage": block})
        run = Run(command="merge", provenance=FakeProvenance(tally))
        check(run.searches.state == state,
              f"{block} must read as {state}: {run.searches.state}")
        said = sourcing_sentence(run)
        check(must in said, f"the {state} sentence must say {must!r}: {said}")
        check(must_not not in said,
              f"and must not say {must_not!r}: {said}")
        check(NOT_RESOLVED in said,
              f"and every one of them carries the constant half -- this tool "
              f"fetched, resolved and checked nothing, whatever the model did: "
              f"{said}")


def test_a_declared_correction_is_listed_and_still_charged() -> None:
    """The finding decision: the same one already made for a covering value.

    An addition the documents are *silent* about is excused: they cannot deny
    it, and the declaration is what makes it reviewable instead of reported as
    an invention. A *correction* is the other case. The merged document now
    asserts something a source denies, and `Run.accounted_for`'s rule is that
    the queue takes omissions and never assertions -- "a reader who trusts the
    merge is misinformed however well the swap was declared".

    So the correction stays a finding and stays chargeable, and the section
    says why it is there. That is deliberately consistent with the covering
    value one licence over and deliberately not an exception carved for
    the feature that produced it: nothing in this package can tell a
    correction from a corruption, and a level that could declare its way past
    a contradiction would be a level that exits 0 on a corrupted document.
    """
    from llossless.report import Run, additions_section
    from llossless.verify import Verdict, MERGED_TO_SOURCES
    from llossless.decompose import Claim

    text = "The word list is published under the MIT licence."
    claim = Claim(id="M-001", source="merged.md", text=text, line=3,
                  span=text, anchored=True)
    record = {"statement": text, "corrects": "published under the GPL",
              "basis": "citation", "source": "the OSI-approved MIT licence text",
              "reason": "the reference implementation ships that licence"}

    denied = Verdict("M-001", "CONTRADICTED", "the GPL", "source_a.md",
                     "the source says otherwise", MERGED_TO_SOURCES, "grounded")
    run = Run(command="merge", claims={"merged.md": [claim]},
              reverse=[denied], additions=(record,))
    check([v.finding for v in run.findings] != [],
          "a claim the sources contradict stays a finding however well the "
          "correction was declared; declaring is not a way to exit 0")
    check(run.corrections == [record],
          f"and the record is recognised as a correction, because it names "
          f"what it corrects: {run.corrections}")

    section = additions_section(run)
    check("1 of them correct(s)" in section,
          f"the section counts the corrections, so a reader who declared one "
          f"and got a finding is not left inferring a bug: {section[:400]!r}")
    check("moves the exit code" in section,
          "and says plainly that it moves the exit code")
    check("published under the GPL" in section,
          "with what it replaced beside what it now asserts")

    # The other half, and the one that must not move: an addition the sources
    # are merely silent about is excused and is not counted as a correction.
    silent = Verdict("M-001", "MISSING", "", "", "in no source",
                     MERGED_TO_SOURCES, "not_graded")
    extend = {**record, "corrects": ""}
    quiet = Run(command="merge", claims={"merged.md": [claim]},
                reverse=[silent], additions=(extend,))
    check([v.finding for v in quiet.findings] == [],
          "an addition the sources do not deny is excused, exactly as before")
    check(quiet.corrections == [],
          "and it is not a correction, because it corrects nothing")
    check("correct(s)" not in additions_section(quiet),
          "so the section does not tell a reader about a finding they do not "
          "have")


def test_an_addition_record_is_capped_like_every_other_record() -> None:
    """`statement` and `reason` are cut by the pre-pass, and the cut is logged.

    Every other record type with free text carries a cap: `replacement` at
    `REPLACEMENT_MAX`, `reason` at `REASON_MAX`, `rationale` at
    `RATIONALE_MAX`. An addition's fields had none, which mattered more here
    than elsewhere, because a `statement` is what claims are matched against:
    an uncapped one is an unbounded excusal, and the longer it runs the more
    claims fall inside it.

    The cap is not the defence -- 640 characters still holds several short
    claims, and `test_one_declaration_covering_many_claims_is_attributed`
    carries that part. This is the consistency: an addition is a record like
    the others, and an over-long field is shortened and declared rather than
    silently carried or loudly rejected.
    """
    from llossless import parsing
    from llossless.merge import addition_item

    item = addition_item()
    check(item["properties"]["statement"]["maxLength"] == parsing.REPLACEMENT_MAX,
          "the schema must carry the statement cap, so a grammar-constrained "
          "model is stopped at it rather than cut afterwards")
    check(item["properties"]["reason"]["maxLength"] == parsing.REASON_MAX,
          "and the reason cap, the same one every other record's reason gets")

    payload = {"additions": [{"statement": "S" * (parsing.REPLACEMENT_MAX + 50),
                              "corrects": "", "reason": "R" * 200}]}
    truncations = parsing._truncate_capped_fields(payload)
    record = payload["additions"][0]
    check(len(record["statement"]) == parsing.REPLACEMENT_MAX,
          f"an over-long statement is capped in place: {len(record['statement'])}")
    check(len(record["reason"]) == parsing.REASON_MAX,
          f"and so is an over-long reason: {len(record['reason'])}")
    paths = sorted(item.path for item in truncations)
    check(paths == ["$.additions[0].reason", "$.additions[0].statement"],
          f"both cuts are logged, each naming its own field the way an error "
          f"message would: {paths}")
    over = {item.path.rsplit(".", 1)[1]: item.original_length for item in truncations}
    check(over["statement"] == parsing.REPLACEMENT_MAX + 50,
          f"the record keeps how far over the model went, not merely that it "
          f"went over: {over}")
    caps = {item.path.rsplit(".", 1)[1]: item.cap for item in truncations}
    check(caps == {"statement": parsing.REPLACEMENT_MAX, "reason": parsing.REASON_MAX},
          f"and which cap did the cutting: {caps}")

    # A record inside the caps is untouched, and logs nothing. A pass that
    # reported a truncation on every addition would make the real ones
    # unfindable.
    short = {"additions": [{"statement": "Solar is cheaper than coal.",
                            "corrects": "", "reason": "well established"}]}
    check(parsing._truncate_capped_fields(short) == [],
          "a record within its caps is not reported as truncated")
    check(short["additions"][0]["statement"] == "Solar is cheaper than coal.",
          "and is not modified")


def _recorded_merges() -> list[tuple[str, dict[str, str], str]]:
    """Every merge a cassette in this repository holds, with the sources it saw.

    The sources are rebuilt from the request rather than looked up on disk:
    fixtures have been revised since some of these were recorded, and every
    Vandrell fixture opens with the same sentence, so matching a merge to a
    fixture by its text misfiles it. Two renderings: one with `<document>` blocks
    with `a1| ` prefixes, another with `source_a.md:` headers.

    `tests/responses/` only, every file of which is tracked and published.
    `tests/eval/*/` is gitignored -- on one machine and in no published copy
    -- and a pinned figure that counted it failed the publication rehearsal
    the first time it ran.
    """
    import json
    out = []
    for path in sorted((ROOT / "tests" / "responses").rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            request = data["request"]
            if request.get("role") != "merge":
                continue
            answer = json.loads(data["response"]["raw"])["choices"][0]["message"]["content"]
            merged = json.loads(answer)["merged_document"]
        except (ValueError, KeyError, TypeError, IndexError):
            continue
        content = "".join(m.get("content", "") for m in request.get("messages", [])
                          if isinstance(m, dict))
        blocks = re.findall(r'<document [^>]*filename="([^"]+)"[^>]*>\n(.*?)\n</document>',
                            content, re.S)
        sources = {name: "\n".join(re.sub(r"^[a-z]+\d+\| ?", "", line)
                                   for line in body.splitlines())
                   for name, body in blocks}
        if not sources:
            tail = content.split("Nothing else.", 1)[-1]
            sources = {name: body.strip("\n") for name, body in re.findall(
                r"^(source_[a-z]+\.md):\n(.*?)(?=\n\n\nsource_[a-z]+\.md:\n|\Z)",
                tail, re.S | re.M)}
        if sources:
            out.append((str(path.relative_to(ROOT)), sources, merged))
    return out


def test_a_misattribution_fires_on_its_fixtures_and_on_nothing_correct() -> None:
    """`attribution_findings`, seeded both ways over everything on disk.

    Must fire: `attribution_invented`'s one plant and `attribution_swapped`'s
    two, each on the planted sentence.

    Must not fire: every other fixture, every pair's ideal merge, and every
    merged document a tracked cassette holds -- 115 of them, carrying 67
    sentences of the attribution shape, all 67 resolving to one source, so the
    silence is measured on real attributions rather than on documents that
    never cite anything. All 67 are in `m4/`: the 27B's 45 `m7/` merges write
    no sentence of that shape at all, so the real attributions
    this rests on are qwen3:8b's.

    It does fire on three recorded merges, and each is a genuine misattribution:
    qwen3:8b, merging `attribution_invented`'s two sources, wrote "source_a.md
    states that the minimum TLS version is 1.2" and three more like it, each
    crediting one document with the other's fact. Pinned as the three they
    are, so a fourth is a regression or a new finding and either way is read.

    The numbers are pinned rather than skipped for `RECORDED_DOCUMENTS`'
    reason: a cassette added to the corpus moves them, and whoever adds it
    re-measures rather than assumes.
    """
    fired = {name: len(reconcile.attribution_findings(sources_of(name),
                                                      (FIXTURES / name / "merged.md")
                                                      .read_text(encoding="utf-8")))
             for name in sorted(p.name for p in FIXTURES.iterdir()
                                if (p / "merged.md").is_file())}
    check(fired.pop("attribution_invented") == 1 and fired.pop("attribution_swapped") == 2,
          f"the planted fixtures must fire once and twice: {fired}")
    check(not any(fired.values()),
          f"no other fixture may fire: {[n for n, k in fired.items() if k]}")

    finding = reconcile.attribution_findings(
        sources_of("attribution_invented"),
        (FIXTURES / "attribution_invented" / "merged.md").read_text(encoding="utf-8"))[0]
    check(finding.kind == reconcile.MISATTRIBUTED
          and "According to the Operator Guide" in finding.merge_text
          and finding.document == "source_a.md"
          and finding.source_text == "The minimum TLS version is 1.2.",
          f"the finding must name the sentence, the source it wrongs and the "
          f"source that does say it: {finding}")

    # The hand-written references are held to the same must-not-fire in their
    # own module, which is the one entitled to read that corpus.
    for folder in sorted((ROOT / "tests" / "pairs").iterdir()):
        if not (folder / "ideal.md").is_file():
            continue
        sources = {p.name: p.read_text(encoding="utf-8")
                   for p in sorted(folder.glob("source_*.md"))}
        found = reconcile.attribution_findings(
            sources, (folder / "ideal.md").read_text(encoding="utf-8"))
        check(not found, f"pairs/{folder.name} fired: {[f.detail for f in found]}")

    shaped = resolved = 0
    firing: dict[str, int] = {}
    corpus = _recorded_merges()
    for label, sources, merged in corpus:
        names = {n: reconcile._names_of(n, t) for n, t in sources.items()}
        for item in segment_document(merged, reconcile.MERGE_LETTER).segments:
            text = reconcile.flatten(item.text)
            match = (reconcile._ACCORDING_TO.match(text)
                     or reconcile._STATES_THAT.match(text))
            if match is None:
                continue
            shaped += 1
            key = reconcile._name_key(match.group("name"))
            resolved += sum(1 for n in sources if key in names[n]) == 1
        found = reconcile.attribution_findings(sources, merged)
        if found:
            firing[label] = len(found)
    check(len(corpus) == 115,
          f"the recorded-merge corpus is 115 merges; it is now {len(corpus)}, "
          f"so re-measure the figures below rather than update them blind")
    check((shaped, resolved) == (67, 67),
          f"67 shaped sentences and 67 resolving to one source were measured; "
          f"got {(shaped, resolved)}")
    check(sorted(firing.values()) == [4, 4, 4],
          f"three recorded merges misattribute, four sentences each: {firing}")
    for label, sources, merged in corpus:
        if label in firing:
            check("source_a.md states that the minimum TLS version is 1.2." in merged
                  and "minimum TLS version" not in sources.get("source_a.md", "x"),
                  f"{label} fired and is not the known qwen3:8b misattribution")


def test_each_bound_on_a_misattribution_holds() -> None:
    """The four conditions, each seeded, on one pair of sources.

    One sentence varied at a time against the same two documents, so a probe
    that stops firing or starts firing names the condition that moved.
    """
    sources = {
        "source_a.md": "# Vandrell Relay - Operator Guide\n\n"
                       "The read timeout is 30 seconds.\n"
                       "According to the Deployment Notes, the relay is fast.\n",
        "source_b.md": "# Vandrell Relay - Deployment Notes\n\n"
                       "The minimum TLS version is 1.2.\n",
    }

    def fires(sentence, shown=None):
        merged = "# Vandrell Relay\n\n" + sentence + "\n"
        return len(reconcile.attribution_findings(sources, merged, shown=shown))

    # Must fire, both shapes, by title part and by filename, and by the name
    # the operator gave the file.
    check(fires("According to the Operator Guide, the minimum TLS version is 1.2.") == 1,
          "the planted shape, by a part of the title")
    check(fires("The Operator Guide states that the minimum TLS version is 1.2.") == 1,
          "the second shape")
    check(fires("According to source_a.md, the minimum TLS version is 1.2.") == 1,
          "by canonical filename")
    check(fires("According to guide.md, the minimum TLS version is 1.2.",
                {"source_a.md": "docs/guide.md", "source_b.md": "notes.md"}) == 1,
          "by the name the operator gave the file")
    check(fires("According to the Deployment Notes, the read timeout is 30 seconds.") == 1,
          "the other direction")

    # Must not fire: each bound, one at a time.
    check(fires("According to the Deployment Notes, the minimum TLS version is 1.2.") == 0,
          "a correct attribution")
    # Source A quotes the Deployment Notes on something they do not say. The
    # merge carrying A's sentence as written has invented nothing, and only
    # bound 2 keeps it silent: the name resolves and the content is A's alone.
    check(fires("According to the Deployment Notes, the relay is fast.") == 0,
          "an attribution a source already carries as written (bound 2)")
    check(fires("According to the Vandrell Relay, the minimum TLS version is 1.2.") == 0,
          "a name both titles share (bound 3)")
    check(fires("According to the Release Plan, the minimum TLS version is 1.2.") == 0,
          "a name no source carries (bound 3)")
    check(fires("According to the Operator Guide, the maximum payload is 4 MB.") == 0,
          "content no source carries is the reverse pass's, not this (bound 4)")
    check(fires("According to the Operator Guide, TLS must be at least 1.2.") == 0,
          "a paraphrase cannot be told from a misquotation (bound 4)")
    check(fires("The relay says hello to the minimum TLS version is 1.2.") == 0,
          "`that` is required in the second shape")
    check(fires("The minimum TLS version is 1.2.") == 0,
          "an unattributed sentence")


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_reconcile_offline" and callable(function):
            function()
            checks += 1

    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    merges = len(list(MERGES.glob("*.md")))
    print(f"reconcile: {checks} checks pass over {merges} recorded merge(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
