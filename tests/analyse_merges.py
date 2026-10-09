#!/usr/bin/env python3
"""Post-hoc, exploratory analysis of generated merges. **Not a pre-registered metric.**

The pre-registered metrics were fixed before the sweep ran, and this is not one
of them. Nothing here is graded, nothing here moves a coverage number, and this
script makes no model call and never exits non-zero on a finding. It exists
because the 2026-08-08 smoke pass produced a result the pre-registered metrics
cannot see: `qwen3:8b` returned its two sources concatenated, and scored 20/20
on forward coverage for it.

That score is not wrong. Every fact from both sources really is present, which
is what forward coverage asks. It is just a low bar, and the pre-registration
argues -- correctly, but narrowly -- that surfacing needs no metric of its own
because a merge that silently picks one value leaves the other MISSING. The
converse does not hold. Both values present is not both values *surfaced*, and
the headline cannot tell a merge from a staple.

Three counters, and each expectation is **derived from the fixture data** rather
than listed here, the same way `run_merge.transferable` derives which
`must_not_extract` assertions survive:

  concatenation   Is this merge just its sources end to end, source_a first
                  (source_a then source_b, for a pair)? A defect --
                  *except* where the fixture's own reference merge is a
                  concatenation too. `disjoint_sources` is that case: two
                  documents with no shared subject have nothing to interleave,
                  and its `merged.md` is byte-exactly `source_a + "\\n" +
                  source_b`. A global concatenation count would mark the one
                  fixture where the model was right.

  duplication     Content lines appearing more than once. A defect wherever the
                  two sources state a fact in the same words, since rule 4 asks
                  for it once. `disjoint_sources` shares no line with itself,
                  so it cannot duplicate and is not asked to.

  attribution     Where the sources give different values for one attribute,
                  rule 3 asks the merge to state both and name the document each
                  came from. Counted only for fixtures that have such a
                  disagreement, found two ways: a shared line prefix with
                  different tails (`... connect timeout is 30/60 seconds`), and
                  a shared trailing phrase with different numbers (`approximately
                  500 / 512 concurrent connections`). Those two rules select
                  attribution_swapped, conflict_surfaced, contradiction and
                  numeric_drift, and nothing else.

## What these counters cannot see

Stated here rather than discovered by a reader, because in both cases the
counter returns a clean-looking zero rather than an error.

**Duplication is matched on identical lines, so paraphrased duplication is
invisible.** A merge that states a fact once in prose and again as a bullet has
duplicated it, and `duplicates()` reports 0. The suite has a fixture built on
exactly that: `paraphrase` gives both sources the same eight facts in different
wording -- prose in A, a bullet list in B -- and their only identical line is the
boilerplate disclaimer. So `paraphrase` reads `dup 0` whether the model
deduplicated or restated everything twice, and a concatenation of its two
sources, which duplicates all eight facts, still reads `dup 1`. The rows this
affects are flagged `dup-blind`, derived rather than named: **every number in
one source appears in the other, while fewer than half the lines match.** Same
attributes, different words. That selects `paraphrase` alone -- `ordering_only`
is the control, sharing all its numbers *and* all its lines, and
`disjoint_sources` shares no numbers because it genuinely has nothing in common.

**Attribution by filename and attribution by title are counted separately.**
Rule 3 asks the merge to "name the document", and `prompts/merge.md` passes the
filenames precisely so the model has a name to use -- but a model that writes
"the Operator Guide says 30 seconds" has complied, and scoring only
`source_a.md` marks it zero. Titles are matched on the distinguishing tail of
each source's H1 (`Operator Guide`, `Deployment Notes`), not the whole heading,
since every Vandrell source shares the `Vandrell Relay` stem. A title counts only
when it sits inside a longer line: a line that is nothing but the title is
structure the model carried over, and the `#` marker does not reliably survive
to tell them apart.

One further caveat travels with the title figure, which is why it is a separate
column and not folded into the filename one. In `ordering_only` both sources
carry the same H1, so no title there can name one document rather than the
other; that fixture is marked title-ambiguous and its title columns are
suppressed regardless of what the merge says. It has no disagreements, so
nothing is lost.

The bare-line rule was not a precaution. Scored on the `#` marker instead, the
three smoke merges read as two inline attributions apiece, and `contradiction`
-- a verbatim concatenation that cites nothing -- came out compliant.

Read the numbers as description, not as a grade. One sample per cell says what
a model did once.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import itertools
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "src"))

import journal  # noqa: E402  - after the path insert
from llossless.merge import MergeError, source_names  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"
CONDITIONS = ("off", "on")

# How close to `source_a + source_b` counts as concatenation. Not 1.0: the smoke
# pass's merges dropped the sources' `#` markers and re-broke a few lines while
# reproducing every word in order, which is concatenation by any reading that
# matters. Measured after whitespace and heading markers are normalised away.
CONCATENATION = 0.98

# A shared prefix this long between two differing lines is one attribute with
# two values, not a coincidence. Below it, ordinary English repeats itself.
PREFIX = 20

# Thresholds for the `dup-blind` flag: near-total numeric overlap with weak line
# overlap. Measured across the suite, the gap they sit in is wide -- the two
# fixtures at 1.00 numeric overlap split 0.11 / 1.00 on lines, and the next
# numeric figure down is 0.75. Nothing is balanced on a decimal place.
BLIND_NUMBERS = 0.9
BLIND_LINES = 0.5

# Sources are titled `Vandrell Relay - Operator Guide`, and the stem is shared by
# every source in every Vandrell fixture. Only the tail names a document.
TITLE_SPLIT = re.compile(r"\s+[-–—]\s+")


def content_lines(text: str) -> list[str]:
    """Non-empty, non-heading lines, stripped. What a merge is asked to carry."""
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def heading_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip().startswith("#")]


def normalise(text: str) -> str:
    """Collapse whitespace and drop heading markers.

    Both are notation, and `README.md` is explicit that LLossless does not
    score notation. A merge that writes `The pretty Rosegarden` where its source
    wrote `# The pretty Rosegarden` has not changed a fact.
    """
    return " ".join(text.replace("#", " ").split())


def numbers(line: str) -> list[str]:
    return re.findall(r"\b\d[\d,.]*\b", line)


def trailing(line: str, words: int = 2) -> str:
    return " ".join(line.rstrip(".").split()[-words:]).lower()


def words_of(text: str) -> set[str]:
    """Lowercase alphanumeric words, punctuation and dashes discarded.

    Comparing lines by word set rather than by string is what makes the
    bare-title test survive rewording of the separator. Half the suite's sources
    title themselves with an em dash and half with a hyphen, and a model is free
    to swap one for the other while copying a heading across -- which under an
    exact match reads as a line the model composed, i.e. as a citation.
    """
    return set(re.findall(r"[a-z0-9]+", text.lower()))


class SourceGap(ValueError):
    """A directory whose sources do not run `source_a.md` onward without a gap."""


def source_files(directory: Path) -> tuple[str, ...]:
    """Every `source_<letter>.md` in `directory`, in canonical order.

    Read from the directory, never assumed. This used to be a two-name
    constant here and `source_names(2)` in `measure_merges.py`, and when
    `tests/handwritten/` gained `treecreeper` and `mahjongg` with a
    `source_c.md` each, both scripts measured a three-source merge against two
    sources and said nothing. The third source's content read as
    unexplained text in the merge, and `mahjongg`'s reference read as a staple.

    A gap is refused rather than skipped: `source_a.md` and `source_c.md`
    without `source_b.md` is a corpus with a document missing, and measuring
    what is left is the same silent drop in another place. So is any other
    name the glob finds, and so is a directory with fewer than two.
    """
    found = {path.name for path in directory.glob("source_*.md")}
    try:
        expected = source_names(len(found))
    except MergeError as exc:
        raise SourceGap(f"{directory}: {exc}") from None
    if found != set(expected):
        missing = [name for name in expected if name not in found]
        stray = sorted(found - set(expected))
        raise SourceGap(
            f"{directory}: sources must run from source_a.md with no gap; "
            f"found {', '.join(sorted(found))}"
            + (f"; missing {', '.join(missing)}" if missing else "")
            + (f"; not a canonical source name: {', '.join(stray)}" if stray else ""))
    return expected


def sources_of(fixture: str, fixtures_root: Path = FIXTURES) -> dict[str, str]:
    """Every source of one fixture, in canonical order. See `source_files`."""
    here = fixtures_root / fixture
    return {name: (here / name).read_text(encoding="utf-8")
            for name in source_files(here)}


def reference_is_concatenation(fixture: str, fixtures_root: Path = FIXTURES) -> bool:
    """Is the fixture's own `merged.md` a concatenation of its sources?

    True for exactly one fixture in the suite. Checked byte-for-byte against the
    three plausible joins rather than by similarity, because this decides whether
    a concatenated *generated* merge is a defect or the correct answer, and that
    is not a judgement to make on a ratio.

    `fixtures_root` is a parameter rather than always `FIXTURES` so a second
    corpus can be measured with the same function; a corpus with no fixture
    `merged.md` (`tests/handwritten/` deliberately carries none) has
    nothing for this predicate to read, and the caller is expected to check
    that file exists before calling this rather than have this function guess
    what a missing reference means.
    """
    documents = sources_of(fixture, fixtures_root)
    hand = (fixtures_root / fixture / "merged.md").read_text(encoding="utf-8")
    joined = tuple(documents.values())
    return any(separator.join(joined) == hand for separator in ("", "\n", "\n\n"))


def shared_lines(fixture: str) -> list[str]:
    """Lines two or more sources state in the same words. These are what rule 4 is about.

    With two sources, the lines both state.
    """
    documents = sources_of(fixture)
    stated = Counter(line for text in documents.values() for line in set(content_lines(text)))
    return sorted(line for line, n in stated.items() if n > 1)


def titles_of(fixture: str) -> dict[str, tuple[str, str]]:
    """Each source's H1 and its distinguishing tail: `(full heading, tail)`.

    Both are needed. The tail is what identifies a document -- every Vandrell
    source shares the `Vandrell Relay` stem -- but recognising a *bare title
    line* means comparing against the whole heading. Falls back to the whole
    heading as its own tail where there is no separator to split on, as in
    `disjoint_sources`, whose two stories share no stem to strip.
    """
    found: dict[str, tuple[str, str]] = {}
    for name, text in sources_of(fixture).items():
        headings = heading_lines(text)
        if not headings:
            continue
        title = headings[0].lstrip("#").strip()
        parts = TITLE_SPLIT.split(title)
        found[name] = (title, parts[-1].strip() if len(parts) > 1 else title)
    return found


def titles_are_ambiguous(fixture: str) -> bool:
    """Do both sources carry the same title, so that naming one names neither?

    True for `ordering_only`, whose two sources are the same document reordered
    and share the H1 `Vandrell Relay - Configuration Reference`.
    """
    found = titles_of(fixture)
    tails = {tail for _, tail in found.values()}
    return len(found) < len(sources_of(fixture)) or len(tails) < len(found)


def duplication_is_blind(fixture: str) -> bool:
    """Would paraphrased duplication escape the identical-line counter here?

    Derived, per the module docstring: near-total numeric overlap says the two
    sources describe the same attributes; weak line overlap says they do not use
    the same words for them. Both together mean a merge can restate every fact
    twice and `duplicates()` will report nothing.
    """
    documents = sources_of(fixture)
    for first, second in itertools.combinations(documents.values(), 2):
        lines = [content_lines(first), content_lines(second)]
        sets = [{n for line in group for n in numbers(line)} for group in lines]
        if not all(sets) or not all(lines):
            continue
        numeric = len(sets[0] & sets[1]) / min(len(sets[0]), len(sets[1]))
        shared = set(lines[0]) & set(lines[1])
        textual = len(shared) / min(len(lines[0]), len(lines[1]))
        # Any two sources that paraphrase each other are enough: a merge can
        # restate those two's facts twice whatever a third source says.
        if numeric >= BLIND_NUMBERS and textual < BLIND_LINES:
            return True
    return False


def disagreements(fixture: str) -> list[tuple[str, str]]:
    """Line pairs giving one attribute two values, by either derivation.

    Over every two sources, in source order; with two sources, the one pair.
    """
    documents = sources_of(fixture)
    found: list[tuple[str, str]] = []
    for first, second in itertools.combinations(
            [content_lines(text) for text in documents.values()], 2):
        found += _disagreements(first, second)
    return found


def _disagreements(first: list[str], second: list[str]) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for left in first:
        for right in second:
            if left == right:
                continue
            prefix = os.path.commonprefix([left, right])
            if len(prefix) >= PREFIX and prefix.split()[-1].lower() != "the":
                found.append((left, right))
            elif (
                trailing(left) == trailing(right)
                and numbers(left)
                and numbers(right)
                and numbers(left) != numbers(right)
            ):
                found.append((left, right))
    return found


def concatenation_ratio(fixture: str, merged: str, fixtures_root: Path = FIXTURES) -> float:
    """How close this merge is to all its sources stapled together, in order."""
    documents = sources_of(fixture, fixtures_root)
    stapled = normalise("\n".join(documents.values()))
    return difflib.SequenceMatcher(None, stapled, normalise(merged)).ratio()


def duplicates(merged: str) -> list[tuple[str, int]]:
    """Content lines this merge states more than once, and how often."""
    counted = Counter(content_lines(merged))
    return sorted(((line, n) for line, n in counted.items() if n > 1), key=lambda p: -p[1])


def attribution(fixture: str, merged: str) -> dict:
    """How the merge names its sources, by filename and by title, kept apart.

    `titles_inline` is the compliance figure: a title used *inside* a longer
    line, which is what citing a source looks like. `titles_standalone` counts
    lines that are nothing but the title -- structure the model carried over,
    not a citation it chose.

    The split is on line content, not on the `#` marker, because the marker does
    not survive. The smoke pass produced both spellings of the same structural
    heading: `# The pretty Rosegarden` thinking-on, and a bare `The pretty
    Rosegarden` thinking-off. Keying on the marker scored the second as an
    attribution, which it plainly is not.

    Both figures are suppressed where the fixture's two sources share a title.
    """
    files = sum(1 for name in sources_of(fixture) if name in merged)
    ambiguous = titles_are_ambiguous(fixture)
    inline = standalone = 0
    if not ambiguous:
        for full, tail in titles_of(fixture).values():
            title_words = words_of(full) | words_of(tail)
            for line in merged.splitlines():
                stripped = line.strip().lstrip("#").strip()
                if not stripped or tail not in stripped:
                    continue
                if words_of(stripped) - title_words:
                    inline += 1
                else:
                    standalone += 1
    return {
        "files": files,
        "titles_inline": inline,
        "titles_standalone": standalone,
        "titles_ambiguous": ambiguous,
    }


def analyse(path: Path) -> dict:
    """Every counter for one generated merge, with its fixture's expectations."""
    fixture, condition, sample = path.stem.rsplit("-", 2)
    merged = path.read_text(encoding="utf-8")
    ratio = concatenation_ratio(fixture, merged)
    concatenated = ratio >= CONCATENATION
    reference_stapled = reference_is_concatenation(fixture)
    repeated = duplicates(merged)
    pairs = disagreements(fixture)
    named = attribution(fixture, merged)
    blind = duplication_is_blind(fixture)
    return {
        "fixture": fixture,
        "condition": condition,
        "sample": int(sample),
        "ratio": ratio,
        "concatenated": concatenated,
        # A concatenation is a defect unless the reference merge is one too.
        "concatenation_defect": concatenated and not reference_stapled,
        "reference_stapled": reference_stapled,
        "shared": len(shared_lines(fixture)),
        "duplicates": sum(n - 1 for _, n in repeated),
        # Only a fixture whose sources repeat themselves can fail rule 4, and
        # only where those repetitions are word-for-word can this counter see it.
        "duplication_defect": bool(repeated) and bool(shared_lines(fixture)),
        "duplication_blind": blind,
        "disagreements": len(pairs),
        "both_values": sum(1 for left, right in pairs if left in merged and right in merged),
        **named,
        # Rule 3 wants both halves, and either kind of name satisfies the second.
        "attribution_defect": bool(pairs) and named["files"] == 0 and named["titles_inline"] == 0,
    }


# Short labels for the structured-output tier, so the column fits beside the
# counters. `MIXED` is the one that matters: a unit whose four steps did not all
# resolve at the same tier changed request shape mid-pipeline.
TIER_LABEL = {"json_schema": "schema", "tool_call": "tool", "prompt": "prompt"}


def tiers_of(records: list[dict]) -> dict[tuple[str, str, int], str]:
    """Per unit, the tier its steps resolved at -- `MIXED` if they disagreed.

    Printed as a column rather than left in the journal because a tier descent is
    silent by construction: `Client.tier` only ever moves down the ladder, the
    move is persisted to `.llossless-cache/capabilities.json`, and the rungs
    that refused leave no cassette and no journal record. One such descent, on
    2026-08-08, put 88 of a run's 164 steps -- 73 of them live calls -- into a
    different request shape than the 76 before it, and it was found by counting
    the journal afterwards. A column makes the next one visible as it happens.
    """
    steps: dict[tuple[str, str, int], set[str]] = defaultdict(set)
    for record in records:
        tier = record.get("tier")
        if tier:
            steps[(record["fixture"], record["condition"], record["sample"])].add(tier)
    resolved = {}
    for unit, found in steps.items():
        if len(found) == 1:
            resolved[unit] = TIER_LABEL.get(next(iter(found)), next(iter(found)))
        else:
            resolved[unit] = "MIXED:" + "/".join(sorted(TIER_LABEL.get(t, t) for t in found))
    return resolved


def table(rows: list[dict], tiers: dict | None = None) -> None:
    print("\nPost-hoc counters over generated merges. Exploratory, not a graded metric.")
    print("Expectations are derived per fixture: see the module docstring.\n")
    header = (
        f"  {'fixture':22} {'cond':4} {'s':>1} {'tier':6}  {'cat%':>5} {'dup':>4} "
        f"{'dis':>3} {'both':>4} {'file':>4} {'ttl':>3} {'hd':>3}  notes"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))
    for row in sorted(rows, key=lambda r: (r["fixture"], r["condition"], r["sample"])):
        notes = []
        if row["concatenation_defect"]:
            notes.append("CONCATENATED")
        elif row["concatenated"]:
            notes.append("concatenated (correct here)")
        if row["duplication_defect"]:
            notes.append(f"{row['duplicates']} duplicated")
        if row["duplication_blind"]:
            notes.append("dup-blind")
        if row["attribution_defect"]:
            notes.append("both values, neither attributed")
        if row["titles_ambiguous"]:
            notes.append("titles ambiguous")
        elif row["titles_standalone"] and not row["titles_inline"]:
            notes.append("titles carried as structure, not cited")
        title_cell = "  -" if row["titles_ambiguous"] else f"{row['titles_inline']:3d}"
        head_cell = "  -" if row["titles_ambiguous"] else f"{row['titles_standalone']:3d}"
        tier = (tiers or {}).get((row["fixture"], row["condition"], row["sample"]), "-")
        if tier.startswith("MIXED"):
            notes.append(f"TIER CHANGED MID-UNIT ({tier.split(':', 1)[1]})")
        print(
            f"  {row['fixture']:22} {row['condition']:4} {row['sample']:1d} {tier:6}  "
            f"{100 * row['ratio']:5.1f} {row['duplicates']:4d} "
            f"{row['disagreements']:3d} {row['both_values']:4d} {row['files']:4d} "
            f"{title_cell} {head_cell}  {', '.join(notes)}"
        )

    print("\n  tier = structured-output tier every step of that unit resolved at")
    print("  file = source filename named   ttl = title cited inside a line (compliance)")
    print("  hd   = bare title line (structure carried over, not a citation)\n")
    for label, key, pool in (
        ("Concatenated where that is a defect", "concatenation_defect", "reference_stapled"),
        ("Duplicated a fact both sources state", "duplication_defect", "shared"),
        ("Stated both values, named no document", "attribution_defect", "disagreements"),
    ):
        hit = [r for r in rows if r[key]]
        if pool == "reference_stapled":
            eligible = [r for r in rows if not r[pool]]
        else:
            eligible = [r for r in rows if r[pool]]
        print(f"  {label:46} {len(hit):3d} / {len(eligible)} eligible merge(s)")
    blind = {r["fixture"] for r in rows if r["duplication_blind"]}
    if blind:
        print(f"\n  dup figures uninformative for: {', '.join(sorted(blind))}")
        print("  (same facts, different words -- identical-line matching cannot see it)")


# The pre-registration promised that any call landing within 10% of its token
# ceiling would be flagged as possibly budget-limited rather than
# quality-limited. It is checked here rather than in `run_merge.py` because the
# runner has no such check, and a promise kept in an exploratory script is worth
# more than one kept nowhere.
BUDGET_LIMIT = 0.9


def reasoning_floors(cassettes: Path) -> dict[str, dict]:
    """Per merge cassette key, the input-prompt size and whether it is exact.

    Read from the cassettes rather than the journal because the journal records
    `completion_tokens` only -- there is no `prompt_tokens` field in it, and the
    reasoning trace is billed to exactly the number it does not carry.

    The endpoint bills the reasoning trace to `prompt_tokens`, so the reported
    prompt size of a thinking-on call is the input *plus* the thinking. The
    input alone is recoverable without estimating from a characters-per-token
    ratio: the off and on calls of a pair send byte-identical `messages` and
    differ in one body field (`reasoning_effort: "none"`, `structured.py:105`),
    and the off call carries no reasoning. So the smallest `prompt_tokens`
    reported across a group of identical `messages` **is** the input prompt.

    A group with no thinking-off member has no floor to subtract and its own
    figure is used, which overstates the input and understates the reasoning.
    Those keys are flagged inexact so a caller can refuse to publish them
    rather than average them in.
    """
    groups: dict[str, list[dict]] = defaultdict(list)
    for path in sorted(cassettes.glob("merge-*.json")):
        body = json.loads(path.read_text(encoding="utf-8"))
        # `response.raw` is the endpoint's body kept verbatim, as a string.
        raw = json.loads(body["response"]["raw"])
        usage = raw.get("usage") or {}
        if usage.get("prompt_tokens") is None or usage.get("completion_tokens") is None:
            continue
        message = raw["choices"][0]["message"]
        digest = hashlib.sha256(
            json.dumps(body["request"]["messages"], sort_keys=True).encode("utf-8")
        ).hexdigest()
        groups[digest].append({
            "key": body["key"],
            "prompt": usage["prompt_tokens"],
            "completion": usage["completion_tokens"],
            "reasoned": bool(message.get("reasoning")),
        })

    floors: dict[str, dict] = {}
    for members in groups.values():
        floor = min(m["prompt"] for m in members)
        exact = any(not m["reasoned"] for m in members)
        for m in members:
            floors[m["key"]] = {**m, "floor": floor, "exact": exact}
    return floors


def budget(records: list[dict], cassettes: Path | None = None) -> None:
    """Whether any merge call ran into its token ceiling.

    Only merge steps carry `max_tokens` in the journal -- decompose and verify
    take a role default from config that is not journalled -- so this covers the
    document-sized budgets, which is where the pre-registration's concern was.

    Cached steps are excluded for the reason `latency_summary` excludes them: a
    replay reports zero completion tokens, so counting one is a ratio against
    the disk. Including them dropped the thinking-on mean from 22% to 2% on a
    corpus that was three-quarters replay.

    **The pre-registered check cannot be evaluated for thinking on.** It was
    written against `completion_tokens`, and this endpoint's `usage` block holds
    exactly `prompt_tokens`, `completion_tokens` and `total_tokens` -- there is
    no distinct reasoning-token field anywhere in the response. Ollama bills the
    reasoning trace to `prompt_tokens` and returns its text in a field of its
    own, so `completion_tokens` on a thinking-on call omits the entire trace.
    The ratio it produces is not a lenient reading of the ceiling; it is a
    number about a different quantity, and reporting it as a pass would be
    reporting that the check ran when it did not. It prints UNVERIFIABLE.

    A derived figure is printed underneath it, from `reasoning_floors`, and is
    labelled as derived. It rests on the pairing assumption, so it is evidence
    and not the assertion.
    """
    merges = [r for r in journal.steps(records, "merge") if r.get("max_tokens")]
    if not merges:
        return
    print("\n  Merge token budget, against the per-fixture ceiling")
    for condition in CONDITIONS:
        group = [r for r in merges if r["condition"] == condition]  # already live-only
        if not group:
            continue
        ratios = [r["completion_tokens"] / r["max_tokens"] for r in group]
        worst = max(group, key=lambda r: r["completion_tokens"] / r["max_tokens"])
        print(
            f"    billed completion, thinking {condition:3} ... {len(group):3d} merge(s)  "
            f"mean {100 * sum(ratios) / len(ratios):5.1f}%  max {100 * max(ratios):5.1f}%  "
            f"({worst['fixture']} sample {worst['sample']}: "
            f"{worst['completion_tokens']}/{worst['max_tokens']})"
        )

    off = [r for r in merges if r["condition"] == "off"]
    tight = [r for r in off if r["completion_tokens"] >= BUDGET_LIMIT * r["max_tokens"]]
    margin = f"{100 - 100 * BUDGET_LIMIT:.0f}%"
    if tight:
        print(f"    FLAGGED  thinking off: {len(tight)} merge(s) within {margin} of the "
              "ceiling -- possibly budget-limited, not quality-limited:")
        for r in tight:
            print(f"      {r['fixture']} sample {r['sample']}: "
                  f"{r['completion_tokens']}/{r['max_tokens']}")
    else:
        print(f"    ok            thinking off: no merge within {margin} of its ceiling "
              f"({len(off)} merge(s); with no reasoning trace, billed completion is the "
              "whole generation)")

    print("    UNVERIFIABLE  thinking on: the endpoint reports no distinct reasoning-token")
    print("                  field, so billed completion omits the trace entirely and the")
    print("                  pre-registered check has no number to read. Not a pass.")

    if cassettes is None:
        return
    floors = reasoning_floors(cassettes)
    on = [r for r in merges if r["condition"] == "on" and r["cassette_key"] in floors]
    usable = [r for r in on if floors[r["cassette_key"]]["exact"]]
    if not usable:
        print("    derived figure unavailable: no thinking-on merge has a paired "
              "thinking-off call")
        return
    spend = {}
    for r in usable:
        seen = floors[r["cassette_key"]]
        spend[r["cassette_key"]] = (
            r, max(0, seen["prompt"] - seen["floor"]) + seen["completion"]
        )
    ratios = [total / r["max_tokens"] for r, total in spend.values()]
    worst_row, worst_total = max(spend.values(), key=lambda p: p[1] / p[0]["max_tokens"])
    print(f"    derived, not reported: reasoning recovered by differencing the paired "
          f"thinking-off call")
    print(f"      {len(spend)} paired merge(s)  mean {100 * sum(ratios) / len(ratios):5.1f}%  "
          f"max {100 * max(ratios):5.1f}%  ({worst_row['fixture']} sample "
          f"{worst_row['sample']}: {worst_total}/{worst_row['max_tokens']})")
    near = [(r, t) for r, t in spend.values() if t >= BUDGET_LIMIT * r["max_tokens"]]
    if near:
        print(f"      {len(near)} within {margin} of the ceiling on derived total spend:")
        for r, total in near:
            print(f"        {r['fixture']} sample {r['sample']}: {total}/{r['max_tokens']}")
    else:
        print(f"      none within {margin} of the ceiling on derived total spend")
    if len(on) > len(usable):
        print(f"      {len(on) - len(usable)} thinking-on merge(s) excluded: no paired "
              "thinking-off call, so their input size is an over-estimate")


def census(records: list[dict], path: Path) -> None:
    """Per fixture/condition/step, how many of the samples were live calls.

    A cassette or cache replay returns the recorded bytes, so two replays of one
    key agree exactly and always will. Averaging that into a spread figure
    reports the property of a file as though it were a property of the endpoint.
    Any cell with fewer than two live calls therefore has its spread suppressed
    here rather than qualified in prose.
    """
    cells: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for record in journal.steps(records, include_recorded=True):  # counting them is the job
        cells[(record["fixture"], record["condition"], record["step"])].append(record)

    print(f"\nLive vs cached, from {path}. A spread over cache replays is not a measurement.\n")
    header = f"  {'fixture':22} {'cond':4} {'step':14} {'live':>4} {'cached':>6}  spread"
    print(header)
    print("  " + "-" * (len(header) - 2))
    suppressed = 0
    for key in sorted(cells):
        group = cells[key]
        cached = sum(1 for r in group if r.get("cached"))
        live = len(group) - cached
        verdict = "measurable" if live >= 2 else "SUPPRESSED (needs 2 live)"
        if live < 2:
            suppressed += 1
        print(f"  {key[0]:22} {key[1]:4} {key[2]:14} {live:4d} {cached:6d}  {verdict}")

    total = sum(len(g) for g in cells.values())
    live_total = total - sum(1 for r in records if r.get("cached"))
    print(f"\n  {total} step(s) over {len(cells)} cell(s); {live_total} live, {total - live_total} cached")
    print(f"  {suppressed} cell(s) have too few live calls to carry a spread figure")

    off_reasoned = [r for r in records if r["condition"] == "off" and r.get("reasoned")]
    off_total = sum(1 for r in records if r["condition"] == "off")
    print(f"\n  off-condition records: {off_total}, of which reasoned: {len(off_reasoned)}")
    if off_reasoned:
        print("  THINKING-OFF FAILED -- no condition comparison is valid")
        for r in off_reasoned[:5]:
            print(f"    {r['fixture']} sample {r['sample']} step {r['step']}")
    else:
        print("  thinking-off held: no off-condition call produced a reasoning block")

    seen = Counter(r["tier"] for r in records if r.get("tier"))
    print(f"\n  structured-output tier over {sum(seen.values())} step(s): "
          + ", ".join(f"{tier} {n}" for tier, n in seen.most_common()))
    if len(seen) > 1:
        print("  TIER DESCENT -- the corpus spans more than one request shape.")
        print("  A descent is one-way and persisted; the rungs that refused left no record.")
        ordered = [r for r in records if r.get("tier")]
        for index, record in enumerate(ordered):
            if index and record["tier"] != ordered[index - 1]["tier"]:
                print(f"    step {index}: {ordered[index - 1]['tier']} -> {record['tier']} "
                      f"at {record['fixture']} [{record['condition']}] "
                      f"sample {record['sample']} {record['step']}")
    else:
        print("  one tier throughout: no descent, every call had the same request shape")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--merges",
        type=Path,
        default=ROOT / "tests" / "responses" / "m4" / "merges",
        help="directory of <fixture>-<condition>-<sample>.md files",
    )
    # Defaulted rather than optional. The tier column and the descent check are
    # the reason this script exists in the form it does, and both are silent
    # without a journal -- an operator running it bare would see a `-` in the
    # column meant to make the next tier descent visible, which is worse than
    # not having the column. It sits beside `--merges` in the corpus, so the
    # default is derivable; passing `--journal ""` opts out.
    parser.add_argument(
        "--journal",
        type=Path,
        default=ROOT / "tests" / "responses" / "m4" / "journal.jsonl",
        help="sweep journal; prints the live/cached census and the thinking-off check",
    )
    parser.add_argument("--fixture", action="append", help="restrict to this fixture; repeatable")
    args = parser.parse_args(argv)

    if not args.merges.is_dir():
        print(f"no such directory: {args.merges}", file=sys.stderr)
        return 2
    paths = sorted(args.merges.glob("*.md"))
    if args.fixture:
        paths = [p for p in paths if p.stem.rsplit("-", 2)[0] in set(args.fixture)]
    if not paths:
        print(f"no merges in {args.merges}", file=sys.stderr)
        return 2

    records: list[dict] = []
    if args.journal:
        if not args.journal.is_file():
            print(f"no such journal: {args.journal}", file=sys.stderr)
            return 2
        records = journal.records(args.journal)

    # A fixture whose sources have a gap is refused before anything prints:
    # it is a corpus with a document missing, not a finding.
    try:
        rows = [analyse(path) for path in paths]
    except SourceGap as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2

    # The label leads the output as well as trailing it. These counters were
    # written after reading the corpus, so a reader who scrolls into the middle
    # of a table must not have to infer their status from a commit message.
    print("=" * 78)
    print("  EXPLORATORY, POST-HOC. Not a pre-registered metric.")
    print("  Written after reading the corpus these counters describe. Nothing here")
    print("  is graded, nothing moves a coverage number, and this script always")
    print("  exits 0. A counter invented to describe data it has already seen is")
    print("  description, not evidence about that data.")
    print("=" * 78)

    table(rows, tiers_of(records))
    print(f"\n  {len(rows)} merge(s) from {args.merges}")

    if records:
        census(records, args.journal)
        budget(records, args.journal.parent)

    print("\n  EXPLORATORY, POST-HOC: this script grades nothing and always exits 0.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
