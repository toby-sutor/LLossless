#!/usr/bin/env python3
"""Rank the full matrix over the repository's own pairs, each against its `ideal.md`.

Same ranking as `tests/rank_arms.py` -- silent loss, then band deviation, then
cost, then speed -- but over `tests/pairs`, which carry `ideal.md` and
`ideal.json` and are the corpus named as safe for a
third-party endpoint.

The band is two-sided on purpose. `lost` is content the reference kept and the
model dropped; `bloat` is content the reference dropped and the model kept. A
one-sided figure would rank a literal merge first, because it cannot drop what
the reference kept.

**`cell_figures` is the pairs scorer**: silent loss and
deviations computed mechanically from the merged text and the merge's own
declarations. It holds to that sentence -- no model is a
judge:

- A declaration forgives a segment from `lost` only when the tool confirmed
  it **mechanically** (the title check or the text itself, a record whose
  `claims` is empty). A confirmation reached by the tested model's own verify
  verdicts is counted apart, `model_confirmed`, and forgives nothing.
- A declared `dropped` is never forgiven: dropping content the ideal kept is
  the deviation, whoever confirms that it was dropped.
- The title is governed by `title_policy`, not by the band, and is left out of
  silent loss, `decl`, lost and bloat alike.
- `dup` counts exact repeats only. The near-repeat pass decides
  nothing (`reconcile.duplication`) and is reported as `near_dup`
  beside it.
- Formatting moves nothing. The merge is read as `merge_side` gives
  it: inline emphasis and code marks (`*`, `_`, backticks) off every line, its
  block notation kept (`unmark`), then a single newline inside a paragraph
  read as a space (`unwrap`), so a merge hard-wrapped at 72 columns, or with
  every number in bold, is segmented as the same merge. The same marks come
  off the sources' side of every comparison too (`inline_plain`), because the
  comparison is an exact substring search and a source that carries its own
  bold (`index_429`) would otherwise read as absent from a merge that kept
  it. The sources are segmented as the tool segments them, untouched, so a
  declaration still names the segment it named. Not covered: curly against
  straight quotes, a heading demoted to a bold line, and a wrap that puts a
  list marker at the start of a line (which is then a list item).
- `absent_rejected` counts absent segments behind a declaration the tool
  itself rejected. Silent loss keeps its definition (a declared segment is
  not silent); this is its own column.

**The rule is an argument and has no default.** Whether a segment that is not
in the merge word for word is reworded or absent is decided by
`reconcile.locate`, the tool's own function, under one of `reconcile.RULES`:
the registered rule, under which every figure published up to 2026-10-12 was
scored, or the amended rule of that date. `sets`, `located_of`, `ideal_sets`,
`cell_sets`, `cell_figures` and `cells_of` all take `rule` by keyword and none
of them defaults it, so a program that re-derives a published figure has to say which
scoring it is re-deriving, and one that does not fails instead of moving the
figure. Under the amended rule "kept" still means one thing: the merge and
`ideal.md` are both read with it, so `lost` and `bloat` are formed from the
amended verdicts on both sides, silent loss is `reconcile.is_silent_loss`,
and an untaken heading that is not lost content is counted in a column of its
own, `headings_untaken`, which is not part of silent loss.

`main` ranks a matrix run by `figure_rules`: one figure per (model, pair),
headline rates over the pairs every counted model completed, exit 2 and other
exclusions as their own column, exact cost and one seconds source.
"""
import dataclasses
import functools
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tests"))
from llossless import reconcile, segment  # noqa: E402

import figure_rules  # noqa: E402

P = REPO / "tests" / "pairs"

# Which reference merge a merge is scored against. A pair's `ideal.md` is the
# reference as it stands. Where a reference was corrected after runs had been
# scored against it, the one those runs were registered with is kept beside it
# as `ideal-as-registered.md` (with its `.json`), so that a published scoring
# can still be given back: bike_docks', corrected on 2026-10-15, kept the
# support desk's count of 3 that a merge at the default level is told to choose
# away. `AS_REGISTERED` reads that file where there is one and `ideal.md`
# elsewhere; `CURRENT` always reads `ideal.md`.
CURRENT = "current"
AS_REGISTERED = "as-registered"
REFERENCES = (CURRENT, AS_REGISTERED)


def reference_file(pair, suffix, reference):
    """The reference merge of `pair` (`suffix` ".md" or ".json") that `reference` names."""
    if reference not in REFERENCES:
        raise ValueError(f"reference must be one of {REFERENCES}, not {reference!r}")
    kept = P / pair / f"ideal-as-registered{suffix}"
    if reference == AS_REGISTERED and kept.is_file():
        return kept
    return P / pair / f"ideal{suffix}"
# The 2026-09-18 matrix, published. `MATRIX_DIR` points
# it at another run of the same shape. `tests/matrix_figures.py` forms the
# catalogue rows from the same cells by the same selection and arithmetic.
R = Path(os.environ.get("MATRIX_DIR") or REPO / "arms" / "2026-09-18" / "matrix")

# Inline marks a merge may add or drop without changing a word.
_INLINE_MARKS = re.compile(r"[*_`]")


def inline_plain(text: str) -> str:
    """Emphasis and code marks off, whitespace collapsed. Applied to both sides."""
    return " ".join(_INLINE_MARKS.sub("", text).split())


def unwrap(text: str) -> str:
    """A single newline inside a paragraph or a list item is a space. Merge side only.

    What starts a block for `segment.segment_document` still starts one here:
    a blank line, a fence (copied byte for byte), a heading, a rule, a bullet,
    a table row, a comment, a setext heading. A continuation line joins the
    paragraph or list item above it, a quoted line only a quoted one.
    """
    lines = text.splitlines()
    out: list[str] = []
    fence = ""
    joinable = quoted = False
    for index, raw in enumerate(lines):
        if fence:
            out.append(raw)
            if raw.strip().startswith(fence):
                fence = ""
            continue
        opener = segment._FENCE.match(raw)
        if opener:
            fence = opener.group("marker")[0] * 3
            out.append(raw)
            joinable = False
            continue
        arrow = segment._QUOTE.match(raw)
        body = raw[arrow.end():] if arrow else raw
        setext_next = index + 1 < len(lines) and bool(segment._SETEXT.match(lines[index + 1]))
        if segment._is_block_start(body) or setext_next or segment._SETEXT.match(body):
            out.append(raw)
            joinable = bool(segment._BULLET.match(body)) and not setext_next
            quoted = bool(arrow)
            continue
        if joinable and quoted == bool(arrow):
            out[-1] = out[-1].rstrip() + " " + body.strip()
            continue
        out.append(raw)
        joinable, quoted = True, bool(arrow)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


# What may open a line as block notation, kept when a line's inline marks come
# off: quote arrows, then a heading's hashes, a bullet or a table pipe.
_LEAD = re.compile(r"^(\s*(?:>\s?)*(?:#{1,6}\s+|(?:[-*+]|\d{1,9}[.)])\s+|\|)?)")


def unmark(text: str) -> str:
    """Inline emphasis and code marks off each line, the line's block notation kept.

    Merge side, before the merge is segmented: bold around a number moves the
    sentence splitter (`**0**. Bring` is not split where `0. Bring` is), so a
    comparison that strips marks only after segmenting still scores the bold.
    Fences and rules are copied as they are.
    """
    out: list[str] = []
    fence = ""
    for raw in text.splitlines():
        if fence:
            out.append(raw)
            if raw.strip().startswith(fence):
                fence = ""
            continue
        opener = segment._FENCE.match(raw)
        if opener:
            fence = opener.group("marker")[0] * 3
            out.append(raw)
            continue
        if segment._RULE.match(raw):
            out.append(raw)
            continue
        lead = _LEAD.match(raw).group(1)
        out.append(lead + _INLINE_MARKS.sub("", raw[len(lead):]))
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def merge_side(text: str) -> str:
    """The merge as the scorer reads it: inline marks off, then paragraphs unwrapped.

    Marks first: `**1**) Rename` is a numbered item once its bold is off, and
    unwrapping first would have joined it to the line above as prose.
    """
    return unwrap(unmark(text))


def _flat(item: segment.Segment) -> str:
    return inline_plain(reconcile.flatten(item.text))


def sources_of(docs: dict) -> list:
    """The sources segmented exactly as the tool segments them: ids are the tool's."""
    return [segment.segment_document(text, reconcile.document_id(index), name)
            for index, (name, text) in enumerate(docs.items())]


def located_of(docs, text, *, rule):
    """(every source segment located in one merge, the merge's segments).

    `reconcile.locate` itself, under `rule`, over `inline_plain` text on both
    sides and the `merge_side` of the merge. This is the scorer's only reading
    of "carried, reworded or absent"; there is no second copy of the rule
    here to keep in step with the tool's.
    """
    merged_text = merge_side(text)
    merged = segment.segment_document(merged_text, reconcile.MERGE_LETTER).segments
    haystack = inline_plain(reconcile.flatten(merged_text))
    located = [item for document in sources_of(docs)
               for item in reconcile.locate(document, haystack, merged, rule=rule,
                                            plain=inline_plain).located]
    return located, merged


def sets(docs, text, *, rule):
    """(absent ids, kept ids, exact repeats, near repeats) of one merge against its sources.

    The verdicts are `located_of`'s: a label is looked for among the merge's
    labels, anything else in the whole flattened merge, and what is not found
    is `absent` unless `rule` calls it reworded.
    """
    located, merged = located_of(docs, text, rule=rule)
    absent = {item.segment.id for item in located if item.verdict == reconcile.ABSENT}
    kept = {item.segment.id for item in located if item.verdict != reconcile.ABSENT}
    repeats = reconcile.duplication(tuple(dataclasses.replace(item, text=_flat(item))
                                          for item in merged))
    return (absent, kept, sum(1 for d in repeats if d.exact),
            sum(1 for d in repeats if not d.exact))


def pair_docs(pair):
    return {"source_a.md": (P / pair / "source_a.md").read_text(encoding="utf-8"),
            "source_b.md": (P / pair / "source_b.md").read_text(encoding="utf-8")}


@functools.lru_cache(maxsize=None)
def ideal_sets(pair, *, rule, reference=CURRENT):
    """(ideal-absent ids, ideal-kept ids, source title ids) for one pair, under `rule`.

    Cached per (pair, rule): the reference merge is read with the same rule as
    the merge it is compared with, so "kept by the reference" and "kept by the
    model" are one meaning of kept.
    """
    docs = pair_docs(pair)
    habs, hkept, _, _ = sets(docs, reference_file(pair, ".md", reference).read_text(
        encoding="utf-8"), rule=rule)
    titles = {item.id for document in sources_of(docs) for item in document.segments
              if item.kind == segment.TITLE}
    return frozenset(habs), frozenset(hkept), frozenset(titles)


def declarations(rep) -> dict:
    """segment id -> its declaration record, first record per segment (as the tool grades)."""
    out = {}
    for record in rep.get("declarations") or []:
        segment_id = record.get("segment")
        if segment_id and segment_id not in out:
            out[segment_id] = record
    return out


def cell_sets(pair, merged, rep, *, rule, reference=CURRENT):
    """The segment ids behind every count `cell_figures` gives, under one of `reconcile.RULES`.

    The one place the pairs scoring is formed. `cell_figures` is the length of
    each set here and nothing else, so a program that has to say which
    segments a count is made of (the list of what differs between the two
    scorings, the audit's validation) reads the same sets the published count
    was taken from, and cannot drift from it.

    `silent`, `decl`, `lost`, `bloat`, `model_confirmed` and `absent_rejected`
    are sets of source segment ids, `headings_untaken` too (empty under the
    registered rule, which has no such column), `dup` and `near_dup` are
    counts of repeats in the merge, and `located` maps every source segment id
    to its `reconcile.Located` in this merge.

    The result is kept per (pair, merge text, records, rule), because a
    program that publishes two scorings of one run asks for the same merge
    more than once. It is read and never changed by its callers.
    """
    return _cell_sets(pair, merged, json.dumps(rep.get("declarations") or [],
                                               sort_keys=True), rule, reference)


@functools.lru_cache(maxsize=512)
def _cell_sets(pair, merged, declared, rule, reference):
    rep = {"declarations": json.loads(declared)}
    docs = pair_docs(pair)
    habs, hkept, titles = ideal_sets(pair, rule=rule, reference=reference)
    located, merged_segments = located_of(docs, merged, rule=rule)
    mabs = {item.segment.id for item in located if item.verdict == reconcile.ABSENT}
    mkept = {item.segment.id for item in located if item.verdict != reconcile.ABSENT}
    repeats = reconcile.duplication(tuple(dataclasses.replace(item, text=_flat(item))
                                          for item in merged_segments))
    dup = sum(1 for d in repeats if d.exact)
    near = sum(1 for d in repeats if not d.exact)
    decls = declarations(rep)
    forgiven, judged = set(), set()
    for segment_id, record in decls.items():
        if record.get("grade") != "confirmed" or record.get("disposition") == "dropped":
            continue
        if "claims" not in record:
            raise SystemExit(f"rank_matrix: {pair}: a confirmed declaration of "
                             f"{segment_id} carries no `claims`, so whether a model "
                             f"verdict confirmed it cannot be told")
        (judged if record["claims"] else forgiven).add(segment_id)
    rejected = {s for s, record in decls.items() if record.get("grade") == "rejected"}
    absent = mabs - titles
    lost = (absent & hkept) - forgiven
    by_id = {item.segment.id: item for item in located}
    sets_ = dict(silent=absent - set(decls), decl=absent & set(decls),
                 lost=lost, bloat=(mkept & habs) - titles, dup=dup,
                 near_dup=near, model_confirmed=lost & judged,
                 absent_rejected=absent & rejected, headings_untaken=set(),
                 located=by_id)
    if rule == reconcile.REGISTERED:
        return sets_
    silent = {item.segment.id for item in located
              if reconcile.is_silent_loss(item, by_id, decls)}
    untaken = {item.segment.id for item in located
               if reconcile.is_untaken_heading(item, by_id, decls)}
    if silent | untaken != absent - set(decls) or silent & untaken:
        raise SystemExit(f"rank_matrix: {pair}: lost content and untaken headings do not "
                         f"split the absent, undeclared segments: "
                         f"{sorted((silent | untaken) ^ (absent - set(decls)))}")
    sets_["silent"] = silent
    sets_["headings_untaken"] = untaken
    return sets_


# The columns of a scored record, in the order a stored record carries them.
_COUNTED = ("silent", "decl", "lost", "bloat", "dup", "near_dup", "model_confirmed",
            "absent_rejected")


def cell_figures(pair, merged, rep, *, rule, reference=CURRENT):
    """One merge of one pair against its `ideal.md`, under one of `reconcile.RULES`.

    `silent`, `decl`, `lost`, `bloat`, `dup` as the module docstring defines
    them, plus three columns that never enter a headline: `near_dup`,
    `model_confirmed` (lost segments the tested model's own verifier confirmed
    as declared) and `absent_rejected` (absent segments behind a declaration
    the tool rejected). The whole of the pairs scoring, as a function so that
    another run's figures are formed by the same code. Each figure is the size
    of the set `cell_sets` forms.

    Under the registered rule the record has exactly the fields it always
    had, so a stored record of a published run is given back field for field.
    Under the amended rule the absent, undeclared segments that are not titles
    are split in two: `silent` is lost content (`reconcile.is_silent_loss`),
    and `headings_untaken` is the headings the merge did not take and did not
    declare while their sections survived. The two sum to what `silent` would
    have been from the same verdicts.
    """
    formed = cell_sets(pair, merged, rep, rule=rule, reference=reference)
    figures = {key: formed[key] if isinstance(formed[key], int) else len(formed[key])
               for key in _COUNTED}
    if rule != reconcile.REGISTERED:
        figures["headings_untaken"] = len(formed["headings_untaken"])
    return figures


def cells_of(run: Path, *, rule) -> list[dict]:
    """One record per runner row of a matrix-shaped run, excluded or scored under `rule`.

    The last runner row for an (arm, pair) is the cell and the earlier ones are
    `superseded`; a cell with exit 2 or no report is excluded and named.
    """
    rows = []
    for name in ("results_anthropic.json", "results_openai.json"):
        if (run / name).exists():
            rows.extend(json.loads((run / name).read_text(encoding="utf-8")))
    last = {(r["arm"], r["pair"]): i for i, r in enumerate(rows)}
    out = []
    for i, row in enumerate(rows):
        where = run / f"{row['pair']}-high-{row['arm']}"
        cell = {"arm": row["arm"], "pair": row["pair"], "exit_code": row.get("exit_code")}
        if last[(row["arm"], row["pair"])] != i:
            cell["excluded"] = "superseded"
        elif not (where / "merged.md").exists() or not (where / "report.json").exists():
            cell["excluded"] = "no_report"
        elif row.get("exit_code") == 2:
            # Exit 2 is inconclusive: the run did not complete, and a truncated
            # report still contains a `merged.md` and an empty `declarations`
            # list. Scoring one reads as catastrophic silent loss that the model
            # never committed -- an Opus cell cut off by an account limit scored
            # 36 silent losses this way, against 0 on the same pair in a run
            # that finished.
            cell["excluded"] = "exit_2"
        else:
            cell["excluded"] = ""
        if not cell["excluded"]:
            rep = json.loads((where / "report.json").read_text(encoding="utf-8"))
            cell.update(cell_figures(row["pair"], (where / "merged.md").read_text(encoding="utf-8"),
                                     rep, rule=rule, reference=AS_REGISTERED))
            cell["usd"] = figure_rules.exact_usd(rep, recorded=row.get("cost_usd"))
            cell["billed"] = max(row.get("cost_usd") or 0, row.get("cost_usd_billed") or 0)
            cell["seconds"] = figure_rules.answer_seconds(rep)
            cell["commit"] = (rep.get("provenance") or {}).get("claimcheck_commit")
            cell["fan"] = [f.get("detail", "")[:90]
                           for f in ((rep.get("structural") or {}).get("findings") or [])
                           if f.get("kind") == "declared_loss_over_budget"]
        out.append(cell)
    return out


# The rule `main` ranks under. The matrix it ranks by default is a published
# run, and every figure published for it was scored under the registered rule.
RULE = reconcile.REGISTERED


def main():
    cells = cells_of(R, rule=RULE)
    arms = tuple(sorted({c["arm"] for c in cells}))
    pairs_run = sorted({c["pair"] for c in cells})
    groups = figure_rules.groups(cells, arms, "arm", pairs_run, registered_k1=True)
    counted = [c for c in cells if not c["excluded"]]
    commits = {c["commit"] for c in counted}

    named = [(c["arm"], c["pair"], c["excluded"]) for c in cells
             if c["excluded"] not in ("", "superseded")]
    print(f"\nEXCLUDED (their own column, never scored): {named or 'none'}")
    print(f"PROVENANCE: {len(commits)} distinct commit(s) across {len(counted)} cells -> "
          f"{sorted(x for x in commits if x)}")
    if len(commits) > 1:
        print("  WARNING: cells graded by different code. Not a clean comparison.")
    common = next(iter(groups.values()))["common"] if groups else []
    print(f"COMMON PAIRS (every counted model completed): {len(common)} of {len(pairs_run)}")

    by = {(c["arm"], c["pair"]): c for c in counted}
    print("\nBAND DEVIATION per pair (lost + bloat + exact repeats; lower is closer to ideal.md)\n")
    print(f"{'pair':<16}{'segs':>5}{'ref drop':>9}  " + "".join(f"{a:>18}" for a in groups))
    for p in pairs_run:
        habs, hkept, _ = ideal_sets(p, rule=RULE, reference=AS_REGISTERED)
        devs = {a: figure_rules.deviations(by[(a, p)]) for a in groups if (a, p) in by}
        best = min(devs.values()) if devs else None
        line = f"{p:<16}{len(habs)+len(hkept):>5}{len(habs):>9}  "
        for a in groups:
            if a not in devs:
                line += f"{'-':>18}"
            else:
                mark = "*" if devs[a] == best else " "
                line += f"{str(devs[a]) + ('!' if by[(a, p)]['silent'] else '') + mark:>18}"
        print(line)
    print("   * best on the pair   ! silent loss present (disqualifying)")

    rows = {}
    for arm, group in groups.items():
        row = figure_rules.quality(group)
        row["usd"] = figure_rules.per_merge([c["usd"] for c in group["cells"]],
                                            figure_rules.USD_PLACES)
        row["secs"] = figure_rules.per_merge([c["seconds"] for c in group["cells"]],
                                             figure_rules.SECONDS_PLACES)
        rows[arm] = row
    print(f"\nRANKED over the {len(common)} common pairs: silent loss, then deviation, "
          f"then cost, then speed\n")
    print(f"{'model':<20}{'pairs':>6}{'SILENT':>7}{'/pair':>7}{'dev':>5}{'/pair':>7}"
          f"{'$/merge':>9}{'s/merge':>9}{'model-conf':>11}{'rej-abs':>8}  not completed")
    for arm, r in sorted(rows.items(), key=lambda kv: (
            kv[1]["silent_loss_per_pair"], kv[1]["deviations_per_pair"],
            kv[1]["usd"] if kv[1]["usd"] is not None else float("inf"), kv[1]["secs"])):
        usd = "-" if r["usd"] is None else f"{r['usd']:.3f}"
        print(f"{arm:<20}{r['pairs']:>6}{r['silent_loss']:>7}{r['silent_loss_per_pair']:>7.2f}"
              f"{r['deviations']:>5}{r['deviations_per_pair']:>7.2f}{usd:>9}{r['secs']:>9.1f}"
              f"{r['model_confirmed_declarations']:>11}"
              f"{r['absent_behind_rejected_declarations']:>8}  "
              f"{', '.join(r['pairs_not_completed']) or '-'}")

    fan = [(c["arm"], c["pair"], d) for c in counted for d in c["fan"]]
    print(f"\nCHECK 6a (supersession fan-in) fired in {len(fan)} of {len(counted)} cells"
          + (":" if fan else " - no real model funnelled content into one replacement."))
    for a, p, d in fan:
        print(f"   {a} / {p}: {d}")


if __name__ == "__main__":
    main()
