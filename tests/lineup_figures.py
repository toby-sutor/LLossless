#!/usr/bin/env python3
"""The fair-lineup figures, formed from one run's cells by `figure_rules`. No model call.

`tests/run_lineup.py` writes one run directory: `REGISTRATION.md` (whose
machine block names the rows and sets), `cells.jsonl` (one end record per
attempt) and the raw cells under `cells/`. This program is that run's
`derived_by`, in the two layers the other figure scripts
have:

  1. **Scored cells, from the raw runs.** One record per registered cell, its
     final attempt: the pairs through `rank_matrix.cell_figures` (no model a
     judge, formatting moves nothing), the fixtures through `run_detect.grade`,
     the planted-error pairs through `score_planted`. Money and seconds are read
     off the report by `figure_rules.exact_usd` (the answering attempt's priced
     cost) and `figure_rules.answer_seconds`; the billed upper bound is the
     report's answering, excluded and unruled cost together; a `claude` route's
     money is its CLI envelopes' API-equivalent, answering calls apart from
     every call, beside the same tokens at the uncached list price.
     `--check` requires these to give back `scored.json` field for field.
  2. **Rows, from the scored cells**, by `figure_rules.lineup_groups`:
     one figure per (row, pair), its lowest-numbered counted draw; the
     spread pairs' further draws as min, median and max. The common pairs are
     every registered pair: nothing shrinks them. A row's own result on a
     pair -- its exit 2, a window its registration cannot hold, a refusal
     (flagged "refused (prompt or guardrail)"), an unruled cell (a model
     failure on a vendor row, `limit` or `config` on a self-hosted one), an
     endpoint that failed while the reference worked -- and a pair it was not
     measured on, never shrink another row's set: the row is incomplete, "exit
     2 on k of N", with its figures over the pairs it completed. A call a
     retry reused from the cell's own earlier attempt (`reuse.json`) is
     counted once at its original time and cost. The priced answering cost is the headline, the billed
     upper bound beside it; answering seconds. Then disqualify-then-rank:
     silent loss on a counted common pair disqualifies; the complete rows are
     ranked by deviations per pair, a tie shared unless every row in it is
     list-priced (then list dollars, then seconds); the incomplete
     rows follow every complete row. The registered floors (byte-concatenation,
     a mechanical union, base-only) are scored from the sources with no model
     call, and a row no better than the union on its own pairs is flagged.
     With one draw a cell this is an order by the rule, not a ranking claim.
     `--check` requires these to give back `figures.json`.

Nothing is typed. The fixtures and planted-error tables are formed alongside
(S2: detection over the fixtures every headline row measured; S3: fixed,
kept and other per draw, and mahjongg's false corrections).

**A run with an audit is published under two scorings.** The release run was
amended on 2026-10-12, after its results were known (its registration's
Amendment 3): an audit by reading found that most segments the registered rule
counts as silent loss are still in the merge. Where a run directory holds
`audit/audit.json`, everything above stays as it is, `scored.json` and the
registered block byte for byte, and a second scoring is formed beside it from
the same stored cells under the amended rule (`AMENDED_RULE`):
`scored-amended.json`, the list of every segment whose count differs
(`differences.json`), the segments the similarity rule alone calls reworded
(`reworded-by-similarity.json`), and in `figures.json` the amended block as
`S1` with the registered one as `S1_registered`, the audit's tallies, the
amendment's eight properties with their outcome, and the order by the ruling:
a row is disqualified when the audit found content gone on a first run
(`verdict_of`), not on its count of silent loss, and the others are ranked by
amended deviations per pair. `audit.json` is an input and is validated against
the stored runs. `--check` re-derives all of it, and also requires the
generated lines the two hand-written pages carry: the outcome of the
properties in `REGISTRATION.md` and the tables in `audit/README.md`
(`--texts` prints them).

**The audit holds two kinds of case** since the registration's Amendment 4, of
the same day. The first audit read the segments the registered scoring had
counted as silent loss. A sentence that lost a clause and still resembles the
original is called reworded by the similarity rule, so it was not read, and
with no record it is as silent as a missing one. The audit therefore also
holds every segment on a first run that the similarity rule alone calls
reworded and that no record of the merge names. `audit_problems` requires
`audit.json` to hold exactly both sets, each case marked with its `group`, and
`verdict_of` runs over both. Amendment 4 changes no count and no scoring: who
is disqualified, and with it the order, is all that moves. In `figures.json`
the keys the audit's block had before still count the counted segments and
nothing else; the second group and the two together stand beside them
(`audit_summary`).

    python3 tests/lineup_figures.py --run-dir DIR            print the tables
    python3 tests/lineup_figures.py --run-dir DIR --score    write scored.json
    python3 tests/lineup_figures.py --run-dir DIR --write    write scored.json,
                                                             figures.json and
                                                             figures.md
    python3 tests/lineup_figures.py --run-dir DIR --check    re-derive both
                                                             layers; exit 1 on
                                                             any difference
    python3 tests/lineup_figures.py --run-dir DIR --texts    print the generated
                                                             lines of the two
                                                             hand-written pages
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import json  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import figure_rules  # noqa: E402
import fixture_semantics  # noqa: E402
import rank_matrix  # noqa: E402
import run_detect  # noqa: E402
import run_lineup  # noqa: E402
import score_planted  # noqa: E402
from llossless import reconcile, segment  # noqa: E402
from llossless.web import catalogue as _catalogue  # noqa: E402

# The rule every figure published from this run was scored with, one of
# `reconcile.RULES`. Named here and passed to every scorer call, because the
# scorer has no default: a script that followed whatever the scorer does
# today would move a published figure without a line of its own changing.
# `scored.json` and its `--check` are the registered scoring. A run that was
# amended after its results is scored a second time, beside it and never in
# its place, under `AMENDED_RULE` below.
RULE = "registered"
# The reference merge each scoring reads (`rank_matrix.reference_file`). The
# registered scoring reads the references the run was registered with. The
# amended scoring's counts read them as they stand: bike_docks' was corrected
# on 2026-10-15, after the results (Amendment 5), and only its counts move.
REGISTERED_REFERENCE = rank_matrix.AS_REGISTERED
AMENDED_REFERENCE = rank_matrix.CURRENT

# The committed lineup run this script derives the published figures from: the
# release benchmark of 2026-09-27; `--run-dir` names any other.
EVIDENCE: Path | None = ROOT / "arms" / "2026-09-27" / "lineup"
PLANTED = ("voyager", "bip39")
CONTROL = "mahjongg"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def final_attempts(run_dir: Path) -> dict[str, dict]:
    """cell id -> the end record of its last attempt (counted cells only, no pilot)."""
    records = run_lineup.Journal(run_dir / "cells.jsonl").read()
    out: dict[str, dict] = {}
    for cell_id, attempts in run_lineup.ends(records).items():
        attempts = [a for a in attempts if a.get("kind", "cell") == "cell"]
        if attempts:
            out[cell_id] = {**attempts[-1], "attempts": len(attempts)}
    return out


def _reuse(cell_dir: Path) -> dict:
    """What the runner recorded this attempt reused of the cell's earlier answers."""
    path = cell_dir / "reuse.json"
    return load(path) if path.is_file() else {}


def _merge_usage(into: dict, per_model: dict) -> dict:
    for model, usage in (per_model or {}).items():
        slot = into.setdefault(model, {})
        for key, value in (usage or {}).items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                slot[key] = slot.get(key, 0) + value
    return into


def _money(row: dict, report: dict, cell_dir: Path) -> dict:
    """The cell's cost figures, read off its own files.

    A call this attempt reused from the cell's own earlier attempt is
    counted once, at its original cost. An HTTP report already prices it by
    its tokens (the same tokens); a `claude` route's reused call never reached
    the wrapper, so its earlier envelope's cost (`reuse.json`) is added here.
    """
    reuse = _reuse(cell_dir)
    if row["route"]["kind"] == "claude":
        equiv = run_lineup.api_equivalent(run_lineup.read_calls(cell_dir / "calls"))
        cli = reuse.get("cli") or {}
        per_model = _merge_usage(_merge_usage({}, equiv["per_model"]), cli.get("per_model"))
        extra = float(cli.get("usd") or 0.0)
        return {"usd": equiv["answering_usd"] + extra, "billed": equiv["all_usd"] + extra,
                "uncached_list_usd": figure_rules.uncached_list_usd(per_model),
                "tokens_sent": sum(int(u.get(k) or 0) for u in per_model.values()
                                   for k in ("inputTokens", "cacheReadInputTokens",
                                             "cacheCreationInputTokens", "outputTokens"))}
    prov = report.get("provenance") or {}
    usd = figure_rules.exact_usd(report)
    billed = None
    if usd is not None:
        billed = sum(float(block.get("usd_exact") or 0.0) for block in (
            prov.get("answering_cost"), (prov.get("excluded") or {}).get("cost"),
            (prov.get("unruled") or {}).get("cost")) if block)
    answering = [r for r in prov.get("ledger") or [] if r.get("outcome") != "ceiling"]
    tokens = None
    if answering and all(isinstance(r.get("prompt_tokens"), int)
                         and isinstance(r.get("completion_tokens"), int) for r in answering):
        tokens = sum(r["prompt_tokens"] + r["completion_tokens"] for r in answering)
    return {"usd": usd, "billed": billed, "tokens_sent": tokens}


def _served(report: dict) -> list[str]:
    """Every model id the report says answered (`models_answered`, `served_model`)."""
    prov = report.get("provenance") or {}
    found = set()
    for block in (prov.get("models_answered") or {}).values():
        found |= set((block or {}).get("models") or [])
        if (block or {}).get("output"):
            found.add(block["output"])
    for r in prov.get("ledger") or []:
        if r.get("served_model"):
            found.add(r["served_model"])
        found |= set(((r.get("answered_by") or {}).get("models")) or [])
    return sorted(found)


def _planted(item: str, merged: str, report: dict, cell_dir: Path) -> dict:
    if item in PLANTED:
        key = score_planted.planted(item)
        outcomes = score_planted.score_text(merged, key)
        records = list(report.get("additions") or []) + list(report.get("declarations") or [])
        named = score_planted.declared(records, key)
        count = {k: sum(1 for o in outcomes if o["outcome"] == k)
                 for k in ("fixed", "kept", "other")}
        licence = [o for o, e in zip(outcomes, key.errors, strict=True)
                   if "MIT" in e.original]
        return {"total": len(key.errors), **count,
                "declared": None if named is None else len(named),
                "licence_restored": (all(o["outcome"] == "fixed" for o in licence)
                                     if licence else None),
                "outcomes": [{"error": o["error"], "outcome": o["outcome"]}
                             for o in outcomes]}
    if item == CONTROL:
        # A report copy whose `merged_written_to` names this cell's own merge:
        # `score_planted.load` would otherwise follow a path from the run.
        with tempfile.TemporaryDirectory() as tmp:
            copy = dict(report, merged_written_to=str((cell_dir / "merged.md").resolve()))
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps(copy), encoding="utf-8")
            found = score_planted.false_corrections(path, item)
        return {key: found[key] for key in ("sentences", "verbatim", "false_corrections",
                                            "false_corrections_changed",
                                            "false_corrections_declared",
                                            "declared_naming_a_change")}
    raise SystemExit(f"lineup_figures: no planted-error scorer for {item!r}")


def score(run_dir: Path) -> list[dict]:
    """Layer 1: one scored record per registered cell, in run order."""
    reg, _ = run_lineup.parse_registration(run_dir / "REGISTRATION.md")
    rows = {row["id"]: row for row in reg["rows"]}
    finals = final_attempts(run_dir)
    out = []
    for cell in run_lineup.plan(reg):
        row = rows[cell.row]
        spec = reg["sets"][cell.set]
        end = finals.get(cell.id)
        state = end["state"] if end else "not_run"
        excluded = "" if state == "ok" else state
        if state == "unruled":
            # Counted against the row, as a model failure on a
            # vendor row, as `limit` or `config` on a self-hosted one.
            excluded = f"unruled_{(end or {}).get('unruled_as') or 'model_failure'}"
        record = {"cell": cell.id, "row": cell.row, "model": row["model"], "set": cell.set,
                  "pair": cell.item, "draw": cell.draw, "state": state,
                  "excluded": excluded,
                  "attempts": end["attempts"] if end else 0,
                  "exit_code": end.get("exit_code") if end else None,
                  "started_at": end.get("started_at") if end else None,
                  "claimcheck_commit": end.get("claimcheck_commit") if end else None}
        if end and end.get("flag"):
            record["flag"] = end["flag"]
        cell_dir = run_dir / end["dir"] if end and end.get("dir") else None
        report = None
        if cell_dir is not None and (cell_dir / "report.json").is_file():
            report = load(cell_dir / "report.json")
        if spec["score"] == "detect":
            graded = run_detect.grade(run_detect.load_expected(cell.item),
                                      report if state == "ok" and report else {},
                                      end.get("exit_code") if state == "ok" else 2)
            record["detect"] = graded
            if graded["outcome"] == fixture_semantics.ERRORED and state == "ok":
                record["excluded"] = "errored"
        if state == "ok":
            merged = (cell_dir / "merged.md").read_text(encoding="utf-8") \
                if spec["kind"] == "merge" else ""
            if spec["score"] == "pairs":
                record.update(rank_matrix.cell_figures(cell.item, merged, report,
                                                       rule=RULE, reference=REGISTERED_REFERENCE))
            elif spec["score"] == "planted":
                record["planted"] = _planted(cell.item, merged, report, cell_dir)
            record.update(_money(row, report, cell_dir))
            reuse = _reuse(cell_dir)
            # A reused call keeps its original measured time, counted once.
            record["seconds"] = figure_rules.answer_seconds(report) + float(
                reuse.get("answer_ms") or 0) / 1000
            if reuse.get("served"):
                record["reused_calls"] = reuse["served"]
            record["served_models"] = _served(report)
            record["duration_seconds"] = (report.get("provenance") or {}).get(
                "duration_seconds")
            # A completed run keeps its unruled calls beside it.
            unruled = ((report.get("provenance") or {}).get("unruled") or {}).get("calls")
            if unruled:
                record["unruled_calls"] = dict(unruled)
        out.append(record)
    return out


# --- layer 2 ---------------------------------------------------------------------------

def cost_unit(row: dict) -> str:
    # A command route's figure is the CLI's own `total_cost_usd`, priced by the
    # CLI whether or not pricing.py has a row (Fable): an API-equivalent.
    if row["route"]["kind"] == "claude":
        return "api_equivalent"
    if row.get("unpriced"):
        return "unpriced"
    return "list" if run_lineup.metered(row) else "paid_tier_equivalent"


def rules_of(reg: dict) -> dict:
    """The registration's headline rules, defaults filled in."""
    return {**run_lineup.RULE_DEFAULTS, **(reg.get("rules") or {})}


# The row's own results: each counts against the row and shrinks nobody.
OWN_REASONS = ("model_failure", "window", "refused", "endpoint_failure", "unruled_model_failure",
               "unruled_limit", "unruled_config", "harness_timeout")


def treatment(reg: dict):
    """cell -> DONE, OWN or LOST. Nothing is held apart any more."""
    def treat(cell: dict) -> str:
        reason = cell["excluded"]
        if not reason:
            return figure_rules.DONE
        if reason in OWN_REASONS or reason == "unruled":
            return figure_rules.OWN
        # platform, unclassified, interrupted, halted, usage_limit, infrastructure,
        # not_run, errored: not measured, and the row's alone
        return figure_rules.LOST
    return treat


# What a row's own missing pairs are called in the tables.
MISSING_WORDS = {"model_failure": "exit 2", "window": "window",
                 "refused": run_lineup.REFUSED_FLAG,
                 "endpoint_failure": run_lineup.ENDPOINT_FLAG,
                 "unruled": "model failure (unruled)",
                 "unruled_model_failure": "model failure (unruled)",
                 "unruled_limit": "limit (self-hosted, the model's own)",
                 "unruled_config": "CONFIG (self-hosted, the registration is wrong)",
                 "harness_timeout": "CONFIG (harness timeout, not the model)"}


def missing_text(missing: dict[str, str], of: int) -> str:
    """{pair: reason} as "exit 2 on 1 of 9; window on 2 of 9"."""
    counts: dict[str, int] = {}
    for reason in missing.values():
        word = MISSING_WORDS.get(reason, f"not measured ({reason})")
        counts[word] = counts.get(word, 0) + 1
    return "; ".join(f"{word} on {n} of {of}" for word, n in sorted(counts.items()))


def _empty_quality(group: dict) -> dict:
    """A row with nothing counted on the common pairs: listed, with no figure (N9)."""
    return {"silent_loss": None, "silent_loss_per_pair": None, "deviations": None,
            "deviations_per_pair": None, "pairs": 0, "pairs_completed": len(group["all_cells"]),
            "silent_loss_all_completed": sum(c["silent"] for c in group["all_cells"]),
            "deviations_all_completed": sum(figure_rules.deviations(c)
                                            for c in group["all_cells"]),
            "pairs_not_completed": [f"{pair} ({why})"
                                    for pair, why in group["not_completed"].items()],
            "model_confirmed_declarations": 0, "absent_behind_rejected_declarations": 0}


def _pairs_rows(reg: dict, scored: list[dict], members: list[str],
                pairs: list[str]) -> tuple[list[str], dict, dict]:
    """(the common pairs, each row's figures, the pairs left out and why) for one group."""
    rows = {row["id"]: row for row in reg["rows"]}
    cells = [c for c in scored if c["row"] in members]
    formed = figure_rules.lineup_groups(cells, tuple(members), "row", pairs,
                                        treat=treatment(reg))
    common = formed["common"]
    out = {}
    for rid in members:
        group = formed["rows"][rid]
        mine = [c for c in cells if c["row"] == rid]
        head = group["cells"]
        figures = figure_rules.quality(group) if head else _empty_quality(group)
        out[rid] = {
            "model": rows[rid]["model"],
            "cost_unit": cost_unit(rows[rid]),
            "usd_per_merge": figure_rules.per_merge([c.get("usd") for c in head],
                                                    figure_rules.USD_PLACES),
            "billed_upper_bound_usd_per_merge": figure_rules.per_merge(
                [c.get("billed") for c in head], figure_rules.USD_PLACES),
            "seconds_per_merge": figure_rules.per_merge([c["seconds"] for c in head],
                                                        figure_rules.SECONDS_PLACES),
            # The registered prediction is on tokens sent, not dollars.
            "tokens_sent_per_merge": _whole(figure_rules.per_merge(
                [c.get("tokens_sent") for c in head], 0)),
            "route": rows[rid]["route"]["kind"],
            "effort": run_lineup.effort_label(rows[rid]),
            # The ids each row's reports say answered, so a
            # subscription served by another model than its API row is visible.
            "served_models": sorted({m for c in group["all_cells"]
                                     for m in c.get("served_models") or []}),
            "reused_calls": sum(c.get("reused_calls") or 0 for c in head),
            **figures,
            "headline_draws": {c["pair"]: c["draw"] for c in head},
            # A row's own results and its pairs not measured on the
            # common pairs (it is incomplete and listed after every complete row).
            "incomplete": [f"{pair} ({why})" for pair, why in group["incomplete"].items()],
            "incomplete_text": missing_text(group["incomplete"], len(common)),
            "spread_draws": group["spread_draws"],
            "model_failures": sorted(f"{c['pair']} d{c['draw']}" for c in mine
                                     if c["state"] == "model_failure"),
            "refused": sorted(f"{c['pair']} d{c['draw']}" for c in mine
                              if c["state"] == "refused"),
            "endpoint_failures": sorted(f"{c['pair']} d{c['draw']}" for c in mine
                                        if c["state"] == "endpoint_failure"),
            "excluded": sorted(f"{c['pair']} d{c['draw']} ({c['state']})" for c in mine
                               if c["state"] not in ("ok", "model_failure", "unruled",
                                                     "refused", "window", "endpoint_failure",
                                                     "harness_timeout")),
            "harness_timeouts": sorted(f"{c['pair']} d{c['draw']}" for c in mine
                                       if c["state"] == "harness_timeout"),
            "unruled": sorted(f"{c['pair']} d{c['draw']} ({c['excluded']})" for c in mine
                              if c["state"] == "unruled"),
            # Completed cells that carried an unruled call, counted.
            "unruled_calls": sum(sum((c.get("unruled_calls") or {}).values()) for c in head),
            "measured_on": min(c["started_at"] for c in group["all_cells"])[:10]
            if group["all_cells"] else None,
            "claimcheck_commit": figure_rules.commit_of(group["all_cells"],
                                                        f"tool commit for {rid}")
            if group["all_cells"] else None,
        }
        if cost_unit(rows[rid]) == "api_equivalent":
            out[rid]["uncached_list_usd_per_merge"] = figure_rules.per_merge(
                [c.get("uncached_list_usd") for c in head], figure_rules.USD_PLACES)
    return common, out


# --- the floors ---------------------------------------------------------------------

def union_text(documents: dict[str, str], order: list[str]) -> str:
    """A mechanical union: the base, then every paragraph of the others not already in
    the base (whitespace aside), their titles dropped; nothing else is deduplicated.
    The bug hunt's definition (`2026-09-27-bughunt2/exp/union_baseline.py`)."""
    base = documents[order[0]]
    seen = {" ".join(p.split()) for p in base.split("\n\n")}
    extra = [paragraph for name in order[1:] for paragraph in documents[name].split("\n\n")
             if paragraph.strip() and not paragraph.lstrip().startswith("# ")
             and " ".join(paragraph.split()) not in seen]
    return base.rstrip("\n") + "\n\n" + "\n\n".join(extra) + "\n"


def baseline_texts(pair: str, base: str) -> dict[str, str]:
    """Concatenation, the mechanical union and base-only for one pair, from its sources."""
    documents = rank_matrix.pair_docs(pair)
    order = [base] + sorted(name for name in documents if name != base)
    return {"concatenation": "\n\n".join(documents[n].rstrip("\n") for n in order) + "\n",
            "union": union_text(documents, order),
            "base_only": documents[base]}


def baselines(pairs: list[str], base: str, *, rule: str,
              reference: str = rank_matrix.CURRENT) -> dict:
    """Each floor scored by `rank_matrix.cell_figures` with no report: per pair, and summed.

    `rule` is the scorer's and has no default here either: the floors are
    published figures, and the model picker's colour bands are derived from
    one of them. `reference` is which reference merge they are scored against
    (`rank_matrix.reference_file`).
    """
    out: dict = {}
    for pair in pairs:
        for name, text in baseline_texts(pair, base).items():
            figures = rank_matrix.cell_figures(pair, text, {}, rule=rule, reference=reference)
            out.setdefault(name, {})[pair] = {"silent": figures["silent"],
                                             "deviations": figure_rules.deviations(figures),
                                             "lost": figures["lost"],
                                             "bloat": figures["bloat"]}
    return out


def _floor(per_pair: dict, pairs: list[str]) -> dict:
    silent = sum(per_pair[p]["silent"] for p in pairs)
    dev = sum(per_pair[p]["deviations"] for p in pairs)
    n = len(pairs)
    return {"pairs": n, "silent_loss": silent, "deviations": dev,
            "silent_loss_per_pair": round(silent / n, figure_rules.RATE_PLACES) if n else None,
            "deviations_per_pair": round(dev / n, figure_rules.RATE_PLACES) if n else None}


# --- the order ---------------------------------------------------------------------------

def order(rows: dict, audited: dict[str, str] | None = None) -> dict:
    """Disqualify, then rank the complete rows, then list the incomplete ones.

    `audited` is None for the registered order, and everything below is that
    order. For the amended order it maps each row the audit disqualifies to
    the reason: the rows it names are the disqualified ones, whatever their
    count of silent loss, and the result also states every tie (`ties`).

    Silent loss on any counted common pair disqualifies, complete or not. The
    complete rows (every common pair counted, or held apart by a rule) are
    ranked by deviations per pair; equal deviations share a rank unless every
    row in the tie is list-priced, where list dollars and then seconds break it
    (N8: an API-equivalent, paid-tier-equivalent or unpriced figure is compared
    with no list price, and a cross-unit comparison is not transitive, so a tie
    that holds one is shared whole). The incomplete rows follow every complete
    row, fewest missing pairs first, then deviations per pair.
    """
    def dev(rid):
        value = rows[rid]["deviations_per_pair"]
        return float("inf") if value is None else value

    def listed(rid):
        return rows[rid]["cost_unit"] == "list" and rows[rid]["usd_per_merge"] is not None

    def secs(rid):
        value = rows[rid]["seconds_per_merge"]
        return float("inf") if value is None else value

    disqualified = sorted((rid for rid, r in rows.items()
                           if ((r["silent_loss"] or 0) > 0 if audited is None
                               else rid in audited)),
                          key=lambda rid: (rows[rid]["silent_loss_per_pair"], dev(rid), rid))
    rest = [rid for rid in rows if rid not in disqualified]
    complete = [rid for rid in rest if not rows[rid]["incomplete"] and rows[rid]["pairs"]]
    incomplete = [rid for rid in rest if rid not in complete]
    survivors, ranks, position = [], {}, 1
    ties = []
    for value in sorted({dev(rid) for rid in complete}):
        tie = [rid for rid in complete if dev(rid) == value]
        if len(tie) > 1:
            broken = all(listed(rid) for rid in tie)
            ties.append({"rows": sorted(tie), "deviations_per_pair": value,
                         "rank": position, "shared": not broken,
                         "decided_by": "list dollars, then seconds" if broken
                         else "shared: not every row in the tie is list-priced",
                         "cost_unit": {rid: rows[rid]["cost_unit"] for rid in sorted(tie)},
                         "usd_per_merge": {rid: rows[rid]["usd_per_merge"]
                                           for rid in sorted(tie)},
                         "seconds_per_merge": {rid: rows[rid]["seconds_per_merge"]
                                               for rid in sorted(tie)}})
        if len(tie) > 1 and all(listed(rid) for rid in tie):
            tie.sort(key=lambda rid: (rows[rid]["usd_per_merge"], secs(rid), rid))
            for rid in tie:
                same = [o for o in tie if (rows[o]["usd_per_merge"], secs(o))
                        == (rows[rid]["usd_per_merge"], secs(rid))]
                ranks[rid] = position + tie.index(same[0])
        else:
            tie.sort(key=lambda rid: (not listed(rid), rows[rid]["usd_per_merge"]
                                      if listed(rid) else 0.0, rid))
            for rid in tie:
                ranks[rid] = position
        survivors += tie
        position += len(tie)
    incomplete.sort(key=lambda rid: (len(rows[rid]["incomplete"]), dev(rid), rid))
    for rid in incomplete:
        ranks[rid] = position
        position += 1
    shared = sorted({rank for rank in ranks.values()
                     if sum(1 for r in survivors if ranks[r] == rank) > 1})
    formed = {"survivors": survivors, "ranks": ranks, "shared_ranks": shared,
              "incomplete": [{"row": rid, "reason": rows[rid]["incomplete_text"]
                              or "nothing counted on the common pairs"} for rid in incomplete],
              "disqualified": [{"row": rid, "reason": f"silent loss {rows[rid]['silent_loss']} "
                                f"on the common pairs" if audited is None else audited[rid]}
                               for rid in disqualified]}
    if audited is not None:
        formed["ties"] = ties
    return formed


def _detect_rows(reg: dict, scored: list[dict], set_id: str) -> dict:
    """S2 by the same rule as S1: a row's own result never shrinks the others' fixtures."""
    spec = reg["sets"][set_id]
    block = list(spec.get("headline_items") or spec["items"])
    members = [r["id"] for r in reg["rows"] if set_id in r["sets"]]
    cells = [c for c in scored if c["set"] == set_id and c["pair"] in block]
    formed = figure_rules.lineup_groups(cells, tuple(members), "row", block,
                                        treat=treatment(reg))
    common = formed["common"]
    graded = {(c["row"], c["pair"], c["draw"]): c for c in scored if c["set"] == set_id}
    rows = {}
    for rid in members:
        group = formed["rows"][rid]
        use = [dict(c["detect"], fixture=c["pair"], kind=run_detect.load_expected(
            c["pair"])["kind"]) for c in group["cells"]]
        ok_measured = [r for r in use if r["outcome"] != fixture_semantics.UNMEASURED]
        guards = [c for (row, name, draw), c in sorted(graded.items())
                  if row == rid and name not in block and draw == 1]
        rows[rid] = {
            "fixtures_common": len(common),
            "fixtures_measured": len(use),
            "exit_code_matched": sum(1 for r in use if r["outcome"] == fixture_semantics.MATCHED),
            "measured": len(ok_measured),
            "plants_detected": sum(len(r["detected"]) for r in ok_measured),
            "plants_measured": sum(r["plants"] for r in ok_measured),
            "invented_findings": sum(len(r["invented_findings"]) for r in use),
            "guard_wrong": sum(len(r["guard_wrong"]) for r in use),
            "disqualified": run_detect.disqualified(use),
            "errored": sorted(c["pair"] for c in cells if c["row"] == rid
                              and c["detect"]["outcome"] == fixture_semantics.ERRORED),
            "incomplete": [f"{name} ({why})" for name, why in group["incomplete"].items()],
            "incomplete_text": missing_text(group["incomplete"], len(common)),
            "held_out_guards": {c["pair"]: {"outcome": c["detect"]["outcome"],
                                            "invented": len(c["detect"]["invented_findings"])}
                                for c in guards},
            # N14: over the same fixtures as the detection figures.
            "usd_per_fixture": figure_rules.per_merge([c.get("usd") for c in group["cells"]],
                                                      figure_rules.USD_PLACES),
            "seconds_per_fixture": figure_rules.per_merge(
                [c["seconds"] for c in group["cells"]], figure_rules.SECONDS_PLACES),
        }
    complete = [rid for rid in members if not rows[rid]["incomplete"]
                and rows[rid]["fixtures_measured"]]
    return {"common_fixtures": common, "rows": rows,
            "order": complete + [rid for rid in members if rid not in complete]}


def _planted_rows(reg: dict, scored: list[dict], set_id: str) -> dict:
    rows = {}
    for rid in [r["id"] for r in reg["rows"] if set_id in r["sets"]]:
        mine = [c for c in scored if c["set"] == set_id and c["row"] == rid]
        if not mine:
            continue
        entry = {}
        for item in reg["sets"][set_id]["items"]:
            done = [c for c in mine if c["pair"] == item and c["state"] == "ok"]
            left = sorted(f"d{c['draw']} ({c['state']})" for c in mine
                          if c["pair"] == item and c["state"] != "ok")
            if item in PLANTED:
                entry[item] = {
                    "draws": len(done),
                    "fixed": figure_rules.spread([c["planted"]["fixed"] for c in done])
                    if done else None,
                    "kept": figure_rules.spread([c["planted"]["kept"] for c in done])
                    if done else None,
                    "total": done[0]["planted"]["total"] if done else None,
                    "licence_restored": [c["planted"]["licence_restored"] for c in done],
                    "not_completed": left}
            else:
                entry[item] = {
                    "draws": len(done),
                    "false_corrections_changed": [c["planted"]["false_corrections_changed"]
                                                  for c in done],
                    "false_corrections_declared": [c["planted"]["false_corrections_declared"]
                                                   for c in done],
                    "not_completed": left}
        rows[rid] = entry
    return {"rows": rows}


def rows(reg: dict, scored: list[dict]) -> dict:
    """Layer 2: every table, formed from the scored cells alone."""
    out: dict = {"pin": reg["pin"], "rules": rules_of(reg)}
    for set_id, spec in reg["sets"].items():
        if spec["score"] == "pairs":
            pairs = list(spec["items"])
            members = [r["id"] for r in reg["rows"] if set_id in r["sets"]]
            headline = [r["id"] for r in reg["rows"] if set_id in r["sets"]
                        and r.get("headline", True)]
            mine = [c for c in scored if c["set"] == set_id]
            common, head = _pairs_rows(reg, mine, headline, pairs)
            floors = baselines(pairs, reg["settings"]["base"], rule=RULE,
                               reference=REGISTERED_REFERENCE)
            for r in head.values():
                # N5: the union's deviations over the very pairs this row's figure is over.
                on = sorted(r["headline_draws"])
                r["union_deviations"] = sum(floors["union"][p]["deviations"] for p in on) \
                    if on else None
                r["no_better_than_union"] = bool(on) and r["deviations"] is not None and \
                    r["deviations"] >= r["union_deviations"]
            block = {"common_pairs": common, "rows": head,
                     "order": order(head),
                     "baselines": {name: _floor(per, common) for name, per in floors.items()},
                     "side": {}}
            for rid in members:
                row = next(r for r in reg["rows"] if r["id"] == rid)
                if row.get("headline", True):
                    continue
                partner = row.get("compare_with")
                group = [rid] + ([partner] if partner else [])
                side_common, side = _pairs_rows(reg, mine, group,
                                                run_lineup.items_of(reg, row, set_id))
                block["side"][rid] = {"compared_with": partner, "common_pairs": side_common,
                                      "rows": side}
            out[set_id] = block
        elif spec["score"] == "detect":
            out[set_id] = _detect_rows(reg, scored, set_id)
        elif spec["score"] == "planted":
            out[set_id] = _planted_rows(reg, scored, set_id)
    return out


def _rank_text(block: dict, rid: str) -> str:
    rank = block["order"]["ranks"].get(rid)
    if rank is None:
        return "DQ"
    return f"{rank}=" if rank in block["order"]["shared_ranks"] else str(rank)


def _rate(value) -> str:
    return "-" if value is None else f"{value:.2f}"


def _count(value) -> str:
    return "-" if value is None else str(value)


def _pairs_lines(set_id: str, block: dict, title: str = "") -> list[str]:
    """One pairs set as registered: the table, the floors, the rows, the spread, the side table.

    `title` replaces the heading and nothing else, so that a run published
    under two scorings shows this block, line for line, under a heading that
    says which scoring it is.
    """
    common = block.get("common_pairs") or []
    lines = [title or f"## {set_id}: the pairs, lowest counted draw, over the {len(common)} "
             f"common pairs", "",
              "Disqualify, then rank: silent loss disqualifies; the complete rows by "
              "deviations per pair, equal deviations sharing a rank unless every row "
              "in the tie is list-priced (then list dollars, then seconds). A row's "
              "own exit 2, window cell, refusal, unruled cell or failed endpoint, and "
              "a pair it was not measured on, never shrink another row's pairs: it is "
              "listed after every complete row with its figures over the pairs it "
              "completed. One draw a cell: an order by the rule, not a ranking claim "
              "(plan 9.3).", ""]
    lines += ["| # | row | pairs | silent | /pair | dev | /pair | vs union | $ / merge "
              "| unit | billed $ | s / merge | tokens / merge | model-conf | incomplete | "
              "excluded | unruled calls | reused calls | not completed |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
              "---|---|"]
    ranked = (block["order"]["survivors"]
              + [d["row"] for d in block["order"]["incomplete"]]
              + [d["row"] for d in block["order"]["disqualified"]])
    for rid in ranked:
        r = block["rows"][rid]
        versus = "-" if r["union_deviations"] is None else (
            f"NO BETTER ({r['union_deviations']})" if r["no_better_than_union"]
            else f"below ({r['union_deviations']})")
        lines.append(
            f"| {_rank_text(block, rid)} | {rid} | {r['pairs']} of {len(common)} | "
            f"{_count(r['silent_loss'])} | {_rate(r['silent_loss_per_pair'])} | "
            f"{_count(r['deviations'])} | {_rate(r['deviations_per_pair'])} | "
            f"{versus} | {_money_text(r['usd_per_merge'])} | {r['cost_unit']} | "
            f"{_money_text(r['billed_upper_bound_usd_per_merge'])} | "
            f"{_num(r['seconds_per_merge'])} | {_count(r['tokens_sent_per_merge'])} | "
            f"{r['model_confirmed_declarations']} | "
            f"{r['incomplete_text'] or '-'} | "
            f"{len(r['excluded'])} | {r['unruled_calls']} | {r['reused_calls']} | "
            f"{', '.join(r['pairs_not_completed']) or '-'} |")
    for name, floor in (block.get("baselines") or {}).items():
        lines.append(
            f"| base | {name} | {floor['pairs']} of {len(common)} | "
            f"{floor['silent_loss']} | {_rate(floor['silent_loss_per_pair'])} | "
            f"{floor['deviations']} | {_rate(floor['deviations_per_pair'])} | - | - | "
            f"no model | - | - | - | - | - | - | - | - | - |")
    flagged = [rid for rid in ranked if block["rows"][rid]["no_better_than_union"]]
    lines += ["", "Floors (plan 4), scored by the same scorer from the sources with no "
              "model call: byte-concatenation, a mechanical union (the base, then every "
              "paragraph of the other not already in it, its title dropped) and "
              "base-only. `vs union` holds each row against the union on the same "
              "pairs; "
              + (f"no better than a mechanical union: {', '.join(flagged)}."
                 if flagged else "every counted row is below the union.")]
    lines += ["", "Rows (688, rulings 10 and 11): the route, the effort as run, and "
              "every model id the row's reports say answered (a subscription row "
              "served by another model than its API row shows here).", "",
              "| row | route | effort | answered as |", "|---|---|---|---|"]
    for rid in ranked:
        r = block["rows"][rid]
        lines.append(f"| {rid} | {r['route']} | {r['effort']} | "
                     f"{', '.join(r['served_models']) or '-'} |")
    config_cells = [f"{rid}: {u}" for rid in ranked for u in block["rows"][rid]["unruled"]
                    if "unruled_config" in u]
    config_cells += [f"{rid}: {u} (harness timeout)" for rid in ranked
                     for u in block["rows"][rid].get("harness_timeouts") or []]
    if config_cells:
        lines += ["", "CONFIG (688, ruling 5): the registration set a ceiling, a window "
                  "or a timeout below what the model or its card needs, or the numbers "
                  "do not say; never the model's failure. Each is documented in the run "
                  "report (SELF-HOSTED-LIMITS.md lists the numbers): "
                  + "; ".join(config_cells) + "."]
    spread = [(rid, pair, d) for rid in ranked
              for pair, d in block["rows"][rid]["spread_draws"].items()]
    if spread:
        lines += ["", "Spread pairs, every counted draw (min / median / max):", "",
                  "| row | pair | draws | silent | deviations |", "|---|---|---|---|---|"]
        for rid, pair, d in spread:
            lines.append(f"| {rid} | {pair} | {d['draws']} | {_spread(d['silent_loss'])} "
                         f"| {_spread(d['deviations'])} |")
    for rid, side in (block.get("side") or {}).items():
        lines += ["", f"Side table, {rid}"
                  + (f" against {side['compared_with']}" if side['compared_with']
                     else " (not in the headline)")
                  + f", over {len(side['common_pairs'])} common pair(s):", "",
                  "| row | pairs | silent | dev | $ / merge | unit | s / merge | "
                  "incomplete | not completed |", "|---|---|---|---|---|---|---|---|---|"]
        for sid, r in side["rows"].items():
            lines.append(f"| {sid} | {r['pairs']} of {len(side['common_pairs'])} | "
                         f"{_count(r['silent_loss'])} | {_count(r['deviations'])} | "
                         f"{_money_text(r['usd_per_merge'])} | {r['cost_unit']} | "
                         f"{_num(r['seconds_per_merge'])} | "
                         f"{r['incomplete_text'] or '-'} | "
                         f"{', '.join(r['pairs_not_completed']) or '-'} |")
    return lines


def render(reg: dict, formed: dict) -> str:
    """figures.md: the tables a reader sees, from figures.json alone."""
    rules = formed.get("rules") or rules_of(reg)
    lines = [f"# Lineup figures, pin {formed['pin'][:12]}", "",
             f"Rules (688): refusal_counts {rules['refusal_counts']} (a refusal counts "
             f"against its row, flagged \"{run_lineup.REFUSED_FLAG}\"); an unruled cell "
             f"counts against its row (a model failure on a vendor row; `limit` or `config` "
             f"on a self-hosted row); a cell still failing after every retry pass is the "
             f"row's \"{run_lineup.ENDPOINT_FLAG}\" when the reference route answered; "
             f"nothing shrinks the common pairs.", ""]
    for set_id, spec in reg["sets"].items():
        block = formed.get(set_id) or {}
        if spec["score"] == "pairs":
            registered = formed.get(f"{set_id}_registered")
            if registered is None:
                lines += _pairs_lines(set_id, block)
            else:
                lines += _amended_lines(set_id, block, formed)
                lines += [""] + _pairs_lines(
                    set_id, registered,
                    f"## {set_id} as registered and run: the scoring of the registration, "
                    f"unchanged, over the {len(registered.get('common_pairs') or [])} "
                    f"common pairs")
                lines += [""] + _difference_lines(set_id, formed)
        elif spec["score"] == "detect":
            lines += ["", f"## {set_id}: detection, over the {len(block['common_fixtures'])} "
                      f"common fixtures", "",
                      "A row's own exit 2 on a fixture never shrinks another row's fixtures "
                      "(684); such a row follows the complete ones, over what it measured.",
                      "", "| row | fixtures | exit codes matched | plants detected | invented | "
                      "guards wrong | incomplete | disqualified |",
                      "|---|---|---|---|---|---|---|---|"]
            for rid in block.get("order") or list(block["rows"]):
                r = block["rows"][rid]
                lines.append(f"| {rid} | {r['fixtures_measured']} of {r['fixtures_common']} | "
                             f"{r['exit_code_matched']}/{r['fixtures_measured']} | "
                             f"{r['plants_detected']}/{r['plants_measured']} | "
                             f"{r['invented_findings']} | {r['guard_wrong']} | "
                             f"{r['incomplete_text'] or '-'} | {len(r['disqualified'])} |")
        elif spec["score"] == "planted":
            lines += ["", f"## {set_id}: planted errors (fixed, min / median / max over draws)",
                      "", "| row | " + " | ".join(spec["items"]) + " |",
                      "|---|" + "---|" * len(spec["items"])]
            for rid, entry in block["rows"].items():
                cells = []
                for item in spec["items"]:
                    e = entry.get(item) or {}
                    missing = f" (not completed: {', '.join(e['not_completed'])})" \
                        if e.get("not_completed") else ""
                    if item in PLANTED:
                        cells.append((f"{_spread(e.get('fixed'))} of {e.get('total')}, "
                                      f"{e.get('draws')} draw(s)" if e.get("fixed") else "-")
                                     + missing)
                    else:
                        cells.append((f"false corrections {e.get('false_corrections_changed')}"
                                      if e.get("draws") else "-") + missing)
                lines.append(f"| {rid} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def _whole(value):
    """A mean already rounded to a whole number, as one."""
    return None if value is None else int(value)


def _money_text(value) -> str:
    return "-" if value is None else f"{value:.3f}"


def _num(value) -> str:
    return "-" if value is None else f"{value:.1f}"


def _spread(value) -> str:
    if not value:
        return "-"
    return f"{value['min']} / {value['median']} / {value['max']}"


# --- the second scoring: the registration's Amendment 3 of 2026-10-12 ---------------
#
# A run whose directory holds `audit/audit.json` is published under two
# scorings. The registered one is everything above, unchanged: `scored.json`,
# and the block `rows` forms from it. The amended one is formed here from the
# same stored cells with the amended rule (`AMENDED_RULE`), and the audit by
# reading decides who is disqualified. Nothing here calls a model.
#
# What is written, beside `scored.json` and never into it:
#
#   scored-amended.json          every pairs cell, every floor and every
#                                reference merge under the amended rule
#   differences.json             per cell, every segment whose count differs
#                                between the two scorings: its text, which
#                                step decided, and the merge text it was
#                                found in
#   reworded-by-similarity.json  per cell, every segment the similarity rule
#                                alone calls reworded, which the amendment
#                                neither adds to nor removes from
#   figures.json, figures.md     both scorings, the amended one first
#   audit/cases.md               the audit's cases, rendered from audit.json
#
# `audit/audit.json` is an input and is validated: its cases are exactly the
# segments the registered scoring counted as silent loss, cell by cell, and the
# segments on first runs that the similarity rule alone calls reworded and no
# record names.
AMENDED_RULE = "amended"
AMENDMENT = "Amendment 3, 2026-10-12"
# The amendment that extends the audit, and with it who is disqualified. It
# changes no count and neither scoring.
AUDIT_AMENDMENT = "Amendment 4, 2026-10-12"
# The amendment that corrects bike_docks' reference merge. It moves the amended
# scoring's deviations on that pair and nothing else.
REFERENCE_AMENDMENT = "Amendment 5, 2026-10-15"
AUDIT_DIR = "audit"
AMENDED_SCORED = "scored-amended.json"
DIFFERENCES = "differences.json"
SIMILARITY = "reworded-by-similarity.json"
# The audit's classes. The first two are content gone, wholly or in part, and
# are what disqualifies; the other two are content that is still there.
LOSS_CLASSES = ("gone", "partly")
AUDIT_CLASSES = (*LOSS_CLASSES, "present", "not_content")
CLASS_WORDS = {"gone": "gone", "partly": "partly gone", "present": "present",
               "not_content": "not content"}
# The two kinds of case the audit holds, a case's `group`. A segment the
# registered scoring counted as silent loss, read in every run that has one;
# and a segment on a first run that the similarity rule alone calls reworded
# and that no record of the merge names, which that scoring never counted.
COUNTED = "counted_missing"
REWORDED = "reworded_no_record"
GROUPS = (COUNTED, REWORDED)
GROUP_WORDS = {COUNTED: "counted as silent loss", REWORDED: "reworded with no record"}
# Where figures.json's `audit` block holds the two groups together.
BOTH = "both_groups"
# What the amendment names in its property 5: the headings of source B that
# base only does not have and that leave the count of silent loss, because at
# least one segment of their section is in source A.
BASE_ONLY_UNTAKEN = {
    "bike_docks": ["Escalating E4"],
    "loading_dock": ["Requesting a slot", "When to request", "On the day", "Late finishes"],
    "rate_limits": ["What the client does", "Other kinds of refusal"],
    "trace_names": ["Resolution"],
}
# And in its property 7: the one segment of a reference merge that changes
# side, and what that does to the floors' lost and bloat.
REFERENCE_MOVES = [("bike_docks", "b10", "phrase")]
FLOOR_MOVES = {"concatenation": ("bloat", 65, 64), "union": ("bloat", 65, 64),
               "base_only": ("lost", 66, 67)}
# The columns of a scored cell that are sets of source segments.
SET_COLUMNS = ("silent", "headings_untaken", "decl", "lost", "bloat", "model_confirmed",
               "absent_rejected")


def has_amendment(run_dir: Path) -> bool:
    """Is this run published under both scorings? It is when it carries an audit."""
    return (run_dir / AUDIT_DIR / "audit.json").is_file()


def load_audit(run_dir: Path) -> dict:
    return load(run_dir / AUDIT_DIR / "audit.json")


def _case_key(case: dict) -> tuple:
    return (case["configuration"], case["pair"], case["draw"], case["segment"])


def _document_names(pair: str) -> dict[str, str]:
    """document id -> file name, for one pair's sources."""
    return {reconcile.document_id(index): name
            for index, name in enumerate(rank_matrix.pair_docs(pair))}


def _counts(formed: dict) -> dict:
    """The amended record of one merge: every count, the untaken headings among them."""
    return {key: formed[key] if isinstance(formed[key], int) else len(formed[key])
            for key in ("silent", "headings_untaken", "decl", "lost", "bloat", "dup",
                        "near_dup", "model_confirmed", "absent_rejected")}


def _reference_declarations(pair: str) -> dict:
    """The reference merge's own records, in the shape the scorer reads a report in.

    The reference as registered: this is the reading of the rule change
    (Amendment 3), which is made on the reference the run was registered with.
    """
    data = load(rank_matrix.reference_file(pair, ".json", REGISTERED_REFERENCE))
    return {"declarations": [{"segment": record["segment"]}
                             for record in data["dispositions"]]}


def _both(pair: str, merged: str, report: dict) -> tuple[dict, dict]:
    """One merge scored under the registered and the amended rule, as sets.

    Both against the reference as registered, so that what differs between
    the two is the rule and nothing else. The amended scoring's published
    counts are against the corrected reference (`_amended_counts`).
    """
    return (rank_matrix.cell_sets(pair, merged, report, rule=RULE,
                                  reference=REGISTERED_REFERENCE),
            rank_matrix.cell_sets(pair, merged, report, rule=AMENDED_RULE,
                                  reference=REGISTERED_REFERENCE))


def _amended_counts(pair: str, merged: str, report: dict) -> dict:
    """One merge's counts as the amended scoring publishes them (Amendment 5).

    The amended rule against the reference merge as it stands. It differs from
    `_both`'s amended reading only on a pair whose reference was corrected
    after the run, which is bike_docks' (2026-10-15).
    """
    return _counts(rank_matrix.cell_sets(pair, merged, report, rule=AMENDED_RULE,
                                         reference=AMENDED_REFERENCE))


def _words_stand_as_a_run(item, plain) -> bool:
    """A second reading of one clearing, apart from `reconcile.locate`'s own.

    The segment's words (its content words, for the containment step) must
    occur in the words of the merge text it was found in as one unbroken run.
    """
    needle = reconcile.words(plain(reconcile.flatten(item.segment.text)))
    haystack = reconcile.words(item.window_text)
    if item.step == reconcile.STEP_CONTAINMENT:
        needle, haystack = reconcile.content_words(needle), reconcile.content_words(haystack)
    size = len(needle)
    return bool(size) and any(haystack[at:at + size] == needle
                              for at in range(len(haystack) - size + 1))


def _segment_differences(pair: str, registered: dict, amended: dict,
                         reference: dict) -> list[dict]:
    """Every segment of one merge whose count differs between the scorings.

    For each: its text, the columns it is counted in under each scoring,
    which step decided, and the merge text it was found in. A sentence the
    amended rule found is decided by `phrase` or `containment` and shown with
    the run; a heading counted apart is decided by `heading` and shown with
    what became of its section; a segment whose own verdict is unchanged
    moved because the reference merge keeps it under one rule and not the
    other (`reference`), and is shown with where the reference has it.
    """
    names = _document_names(pair)
    out = []
    for identifier, item in amended["located"].items():
        before = [column for column in SET_COLUMNS if identifier in registered[column]]
        after = [column for column in SET_COLUMNS if identifier in amended[column]]
        if before == after:
            continue
        old = registered["located"][identifier]
        entry = {"segment": identifier, "kind": item.segment.kind,
                 "document": names[item.segment.document], "text": item.segment.text,
                 "registered": before, "amended": after,
                 "verdict": {"registered": old.verdict, "amended": item.verdict}}
        if item.verdict != old.verdict:
            entry["decided_by"] = item.step
            entry["found_in"] = {"merge_segments": list(item.window),
                                 "text": item.window_text}
        elif identifier in amended["headings_untaken"]:
            entry["decided_by"] = "heading"
            declared = registered["decl"] | amended["decl"]
            entry["section"] = [
                {"segment": member, "text": amended["located"][member].segment.text,
                 "state": (amended["located"][member].verdict
                           if amended["located"][member].verdict != reconcile.ABSENT
                           else "absent, with a record" if member in declared
                           else "absent, no record")}
                for member in item.section]
        else:
            entry["decided_by"] = "reference"
        moved = reference.get(identifier)
        if moved:
            entry["reference"] = moved
        if "decided_by" not in entry or (entry["decided_by"] == "reference" and not moved):
            raise SystemExit(f"lineup_figures: {pair} {identifier}: counted differently "
                             f"under the two scorings and nothing explains it")
        out.append(entry)
    return out


def _reference_moves(registered: dict, amended: dict) -> tuple[dict, dict]:
    """(what one reference merge scores to under each rule, its segments that move).

    The second maps a segment id to how the reference merge has it under each
    rule, for every segment the two rules read differently in `ideal.md`.
    """
    moved = {}
    for identifier, item in amended["located"].items():
        old = registered["located"][identifier]
        if item.verdict != old.verdict:
            moved[identifier] = {"registered": old.verdict, "amended": item.verdict,
                                 "decided_by": item.step,
                                 "found_in": {"merge_segments": list(item.window),
                                              "text": item.window_text}}
    figures = {RULE: {"silent": len(registered["silent"]), "headings_untaken": 0},
               AMENDED_RULE: {"silent": len(amended["silent"]),
                              "headings_untaken": len(amended["headings_untaken"])}}
    return figures, moved


def _similarity_found(amended: dict, merged: str) -> list[tuple[dict, str]]:
    """The segments of one merge that the similarity rule calls reworded, each with a step.

    `similarity_alone` is true where neither of the amended rule's two steps
    would have found the segment as a run of its words: the similarity score
    is then the only thing that says it is still there. The step beside each
    entry is the run step that would have found it, or `reconcile.STEP_NONE`.
    """
    plain = rank_matrix.inline_plain

    def norm(text: str) -> str:
        return plain(reconcile.flatten(text))

    segments = segment.segment_document(rank_matrix.merge_side(merged),
                                        reconcile.MERGE_LETTER).segments
    body = reconcile._Body(segments, norm)
    out = []
    for identifier, item in amended["located"].items():
        if item.step != reconcile.STEP_RATIO:
            continue
        step = (body.find(item.segment, norm)[0]
                if item.segment.kind in reconcile.BODY_KINDS else reconcile.STEP_NONE)
        out.append(({"segment": identifier, "kind": item.segment.kind,
                     "text": item.segment.text, "similarity": round(item.ratio, 3),
                     "nearest_merge_segment": item.nearest,
                     "nearest_text": item.nearest_text,
                     "similarity_alone": step == reconcile.STEP_NONE}, step))
    return out


def _similarity_entries(amended: dict, merged: str) -> list[dict]:
    """`_similarity_found`'s entries, as `reworded-by-similarity.json` lists them."""
    return [entry for entry, _ in _similarity_found(amended, merged)]


def derive_amended(run_dir: Path, reg: dict, scored: list[dict]) -> dict:
    """Everything the second scoring is made of, from the stored cells. No model call.

    `scored` is the registered layer. Every pairs cell in it that completed
    is scored again from its own `merged.md` and `report.json` under both
    rules; the registered figures must give its stored record back, or this
    refuses, so that the two scorings are known to be of the same merge.
    """
    finals = final_attempts(run_dir)
    pair_sets = [set_id for set_id, spec in reg["sets"].items() if spec["score"] == "pairs"]
    pairs = sorted({item for set_id in pair_sets for item in reg["sets"][set_id]["items"]})
    base = reg["settings"]["base"]
    references, reference_moves = {}, {}
    cells, differing, similar, facts = [], [], [], {"runs": 0, "problems": []}
    silent_registered: dict[tuple, list[str]] = {}
    counted: dict[tuple, dict] = {}
    # What a merge wrote no record for and the registered scoring did not
    # count: per run, the segments the similarity rule alone calls reworded
    # (the audit's second group, on first runs), those it calls reworded whose
    # words also stand in the merge as a run, and the source titles the merge
    # does not have. A title is left out of silent loss by the registration.
    reworded_no_record: dict[tuple, list[str]] = {}
    reworded: dict[tuple, dict] = {}
    run_no_record: dict[tuple, dict[str, str]] = {}
    titles_no_record: dict[tuple, list[str]] = {}
    cleared = {reconcile.STEP_PHRASE: 0, reconcile.STEP_CONTAINMENT: 0}

    def audit_one(where: str, pair: str, merged: str, registered: dict, amended: dict) -> None:
        """Properties 2, 6 and 8 on one merge; every breach is named."""
        facts["runs"] += 1
        old, new = registered["located"], amended["located"]
        if not amended["silent"] <= registered["silent"]:
            facts["problems"].append(f"property 2: {where} gains silent loss "
                                     f"{sorted(amended['silent'] - registered['silent'])}")
        for identifier, item in new.items():
            was = old[identifier]
            if item.verdict == reconcile.ABSENT and was.verdict != reconcile.ABSENT:
                facts["problems"].append(f"property 2: {where} {identifier} is absent under "
                                         f"the amended rule only")
            if (item.verdict == reconcile.PRESENT) != (was.verdict == reconcile.PRESENT):
                facts["problems"].append(f"property 2: {where} {identifier} is carried under "
                                         f"one rule only")
            if (item.step == reconcile.STEP_RATIO) != (was.step == reconcile.STEP_RATIO):
                facts["problems"].append(f"property 8: {where} {identifier} is reworded by "
                                         f"the similarity rule under one rule only")
            if item.verdict != was.verdict:
                if item.step not in reconcile.RUN_STEPS or not item.window_text \
                        or not _words_stand_as_a_run(item, rank_matrix.inline_plain):
                    facts["problems"].append(f"property 6: {where} {identifier} is cleared "
                                             f"and its words are not shown as one run")
                else:
                    cleared[item.step] += 1

    for pair in pairs:
        text = rank_matrix.reference_file(pair, ".md", REGISTERED_REFERENCE).read_text(
            encoding="utf-8")
        registered, amended = _both(pair, text, _reference_declarations(pair))
        references[pair], reference_moves[pair] = _reference_moves(registered, amended)
        audit_one(f"reference merge of {pair}", pair, text, registered, amended)

    for record in scored:
        if record["set"] not in pair_sets or record["state"] != "ok":
            continue
        cell_dir = run_dir / finals[record["cell"]]["dir"]
        merged = (cell_dir / "merged.md").read_text(encoding="utf-8")
        report = load(cell_dir / "report.json")
        registered, amended = _both(record["pair"], merged, report)
        again = {key: value for key, value in _counts(registered).items()
                 if key != "headings_untaken"}
        if any(record.get(key) != value for key, value in again.items()):
            raise SystemExit(f"lineup_figures: {record['cell']}: the registered scoring of "
                             f"the stored merge is not its record in scored.json; the two "
                             f"scorings would not be of the same merge")
        head = {"cell": record["cell"], "row": record["row"], "set": record["set"],
                "pair": record["pair"], "draw": record["draw"]}
        cells.append({**head, **_amended_counts(record["pair"], merged, report)})
        silent_registered[(record["row"], record["pair"], record["draw"])] = sorted(
            registered["silent"])
        for identifier in registered["silent"]:
            item = registered["located"][identifier]
            counted[(record["row"], record["pair"], record["draw"], identifier)] = {
                "dir": finals[record["cell"]]["dir"], "nearest": item.nearest or "none",
                "ratio": item.ratio, "nearest_text": item.nearest_text}
        audit_one(record["cell"], record["pair"], merged, registered, amended)
        moved = _segment_differences(record["pair"], registered, amended,
                                     reference_moves[record["pair"]])
        if moved:
            differing.append({**head, "segments": moved})
        found = _similarity_found(amended, merged)
        if found:
            similar.append({**head, "segments": [entry for entry, _ in found]})
        run = (record["row"], record["pair"], record["draw"])
        named = rank_matrix.declarations(report)
        reworded_no_record[run] = sorted(
            entry["segment"] for entry, _ in found
            if entry["similarity_alone"] and entry["segment"] not in named)
        run_no_record[run] = {entry["segment"]: step for entry, step in found
                              if not entry["similarity_alone"]
                              and entry["segment"] not in named}
        titles_no_record[run] = sorted(
            identifier for identifier, item in registered["located"].items()
            if item.segment.kind == segment.TITLE and item.verdict == reconcile.ABSENT
            and identifier not in named)
        for identifier in reworded_no_record[run]:
            item = amended["located"][identifier]
            reworded[(*run, identifier)] = {
                "dir": finals[record["cell"]]["dir"], "nearest": item.nearest or "none",
                "ratio": item.ratio, "nearest_text": item.nearest_text}

    floors: dict = {}
    floor_differences = []
    headings_still_silent = 0
    for pair in pairs:
        for name, text in baseline_texts(pair, base).items():
            registered, amended = _both(pair, text, {})
            floors.setdefault(name, {})[pair] = _amended_counts(pair, text, {})
            if name == "base_only":
                headings_still_silent += sum(
                    1 for identifier in amended["silent"]
                    if amended["located"][identifier].segment.kind == segment.HEADING)
            audit_one(f"{name} of {pair}", pair, text, registered, amended)
            moved = _segment_differences(pair, registered, amended, reference_moves[pair])
            if moved:
                floor_differences.append({"baseline": name, "pair": pair, "segments": moved})
    return {
        "scored": {"rule": AMENDED_RULE, "cells": cells, "baselines": floors,
                   "references": references},
        "differences": {
            "cells": differing, "baselines": floor_differences,
            "references": [{"pair": pair, "segment": identifier, **moved}
                           for pair in pairs
                           for identifier, moved in reference_moves[pair].items()]},
        "similarity": {"cells": similar},
        "silent_registered": silent_registered,
        "counted": counted,
        "reworded_no_record": reworded_no_record,
        "reworded": reworded,
        "unread": {"as_a_run": run_no_record, "titles": titles_no_record},
        "facts": {**facts, "cleared": cleared,
                  "reworded_by_similarity": sum(len(cell["segments"]) for cell in similar),
                  "base_only_headings_still_silent": headings_still_silent,
                  "similarity_alone": sum(1 for cell in similar for entry in cell["segments"]
                                          if entry["similarity_alone"])},
    }


def first_runs_of(formed: dict) -> dict[str, dict]:
    """row id -> {pair: draw}: the run of each pair that the audit calls a first run.

    The lowest counted draw of the pair, which is the draw the order reads:
    for every headline row, and for a side row that is not one of them. It is
    the same under both scorings, because whether a draw is counted does not
    depend on the rule that scores it; `with_amended` refuses if it is not.
    """
    block = formed["S1"]
    out = {rid: row["headline_draws"] for rid, row in block["rows"].items()}
    for side in block["side"].values():
        for rid, row in side["rows"].items():
            out.setdefault(rid, row["headline_draws"])
    return out


def audit_problems(audit: dict, amended: dict, first: dict[str, dict]) -> list[str]:
    """`audit.json` against the stored runs: exactly the segments it has to hold.

    Its cases marked `counted_missing` are the segments the registered scoring
    counted as a silent loss, in every run, and every such segment is a case.
    Its cases marked `reworded_no_record` are the segments on first runs
    (`first`, from `first_runs_of`) that the similarity rule alone calls
    reworded and that no record of the merge names, and every such segment is
    a case. No case is anything else or stands twice, each case's text is the
    segment's own, every class is one the audit has, and a case of the second
    kind carries both readings.
    """
    out = []
    expected = {
        COUNTED: {(row, pair, draw, identifier)
                  for (row, pair, draw), ids in amended["silent_registered"].items()
                  for identifier in ids},
        REWORDED: {(row, pair, draw, identifier)
                   for (row, pair, draw), ids in amended["reworded_no_record"].items()
                   if first.get(row, {}).get(pair) == draw for identifier in ids}}
    held: dict[str, set] = {name: set() for name in GROUPS}
    seen: set[tuple] = set()
    for case in audit.get("cases") or []:
        key = _case_key(case)
        if key in seen:
            out.append(f"audit.json holds {key} twice")
        seen.add(key)
        group = case.get("group")
        if group not in GROUPS:
            out.append(f"audit.json {key}: its group is {group!r}, not one of "
                       f"{', '.join(GROUPS)}")
        else:
            held[group].add(key)
        for name in ("first_reading", "second_reading"):
            reading = case.get(name)
            if reading is None and name == "second_reading":
                if group == REWORDED:
                    out.append(f"audit.json {key}: a case that is {GROUP_WORDS[REWORDED]} "
                               f"carries two readings, and this one has no second reading")
                continue
            if not isinstance(reading, dict) or reading.get("class") not in AUDIT_CLASSES \
                    or reading.get("alternative") not in (None, *AUDIT_CLASSES):
                out.append(f"audit.json {key}: {name} has no class the audit knows")
    for key in sorted(held[COUNTED] - expected[COUNTED]):
        out.append(f"audit.json holds {key}, which the registered scoring did not count as "
                   f"a silent loss")
    for key in sorted(expected[COUNTED] - held[COUNTED]):
        out.append(f"the registered scoring counted {key} as a silent loss and audit.json "
                   f"has no case for it")
    for key in sorted(held[REWORDED] - expected[REWORDED]):
        out.append(f"audit.json holds {key} as {GROUP_WORDS[REWORDED]} on a first run, and "
                   f"the stored runs do not give that: on a first run the similarity rule "
                   f"alone must call it reworded and no record may name it")
    for key in sorted(expected[REWORDED] - held[REWORDED]):
        out.append(f"{key} is on a first run, the similarity rule alone calls it reworded "
                   f"and no record names it, and audit.json has no case for it")
    texts: dict[str, dict] = {}
    for case in audit.get("cases") or []:
        pair = case["pair"]
        if pair not in texts:
            texts[pair] = {item.id: item for document in rank_matrix.sources_of(
                rank_matrix.pair_docs(pair)) for item in document.segments}
        item = texts[pair].get(case["segment"])
        if item is None or item.text != case.get("text") or item.kind != case.get("kind"):
            out.append(f"audit.json {_case_key(case)}: its text or kind is not the "
                       f"segment's own")
    return out


def _loss_range(cases: list[dict]) -> list[int]:
    """[fewest, most] cases gone or partly gone, were every borderline case read the other way."""
    def lost(name) -> bool:
        return name in LOSS_CLASSES

    firm = [case["first_reading"] for case in cases]
    fewest = sum(1 for r in firm if lost(r["class"])
                 and not (r["alternative"] and not lost(r["alternative"])))
    most = sum(1 for r in firm if lost(r["class"]) or lost(r["alternative"]))
    return [fewest, most]


def _tally(cases: list[dict], reading: str) -> dict:
    """How many of `cases` one reading put in each class."""
    return {name: sum(1 for case in cases if case[reading]["class"] == name)
            for name in AUDIT_CLASSES}


def _borderline_loss(reading: dict) -> bool:
    """A reading of loss that names an alternative on the other side of the line.

    The line is between content gone, wholly or in part, and content that is
    still there (present, or not content). A loss whose alternative is the
    other loss class is no borderline loss: read either way, it is a loss.
    """
    return (reading["class"] in LOSS_CLASSES and bool(reading["alternative"])
            and reading["alternative"] not in LOSS_CLASSES)


def verdict_of(cases: list[dict]) -> dict:
    """One configuration's verdict from the audit's cases on its first runs.

    The rule that turns readings into a verdict, and the whole of it: a
    configuration has audited loss on a first run if the first reading classed
    at least one of its first-run cases as gone or partly gone. Where a second
    reading was made of its first-run cases and comes to the other verdict by
    the same rule, the configuration is marked `readings_disagree`; the
    verdict is still the first reading's. The cases are of both kinds the
    audit holds.

    Beside the verdict, and changing nothing of it: `lost_borderline` counts
    the cases of loss whose first reading names an alternative on the other
    side of the line (`_borderline_loss`), and `rests_only_on_borderline` says
    whether the verdict of loss has no other case to stand on.
    """
    first = _tally(cases, "first_reading")
    read_twice = [case for case in cases if case.get("second_reading")]
    second = _tally(read_twice, "second_reading") if read_twice else None
    lost = sum(first[name] for name in LOSS_CLASSES)
    borderline = sum(1 for case in cases if _borderline_loss(case["first_reading"]))
    out = {"cases": len(cases), "first_reading": first, "lost": lost,
           "audited_loss": lost > 0, "lost_borderline": borderline,
           "rests_only_on_borderline": lost > 0 and borderline == lost,
           "second_reading": second,
           "second_reading_cases": len(read_twice), "readings_disagree": False}
    if second is not None:
        out["readings_disagree"] = (sum(second[name] for name in LOSS_CLASSES) > 0) \
            != out["audited_loss"]
    return out


def audit_verdicts(audit: dict, head: dict) -> dict:
    """row id -> its verdict, over the audit's cases on the draws its figures count."""
    out = {}
    for rid, row in head.items():
        first_runs = [case for case in audit["cases"] if case["configuration"] == rid
                      and row["headline_draws"].get(case["pair"]) == case["draw"]]
        out[rid] = verdict_of(first_runs)
    return out


def _borderline_words(verdict: dict) -> str:
    """ "its one case is borderline", where a verdict of loss has no other case; else ""."""
    if not verdict["rests_only_on_borderline"]:
        return ""
    return ("its one case is borderline" if verdict["lost"] == 1
            else f"its {verdict['lost']} cases are all borderline")


def _audit_reason(verdict: dict) -> str:
    words = _borderline_words(verdict)
    return (f"audited loss on a first run: {verdict['lost']} of {verdict['cases']} segments "
            f"read gone or partly gone" + (f"; {words}" if words else "")
            + (" (readings disagree)" if verdict["readings_disagree"] else ""))


def _amended_cells(scored: list[dict], amended: dict) -> list[dict]:
    """The registered records with every count replaced by its amended one."""
    by_cell = {cell["cell"]: cell for cell in amended["cells"]}
    out = []
    for record in scored:
        mine = by_cell.get(record["cell"])
        if mine is None:
            out.append(record)
            continue
        counts = {key: value for key, value in mine.items()
                  if key not in ("cell", "row", "set", "pair", "draw")}
        out.append({**record, **counts})
    return out


def _floor_amended(per_pair: dict, pairs: list[str]) -> dict:
    """A floor under the amended rule: `_floor`'s figures and the untaken headings."""
    shaped = {p: {"silent": per_pair[p]["silent"],
                  "deviations": figure_rules.deviations(per_pair[p])} for p in pairs}
    return {**_floor(shaped, pairs),
            "headings_untaken": sum(per_pair[p]["headings_untaken"] for p in pairs),
            "lost": sum(per_pair[p]["lost"] for p in pairs),
            "bloat": sum(per_pair[p]["bloat"] for p in pairs)}


def amended_block(reg: dict, scored: list[dict], amended: dict, audit: dict,
                  set_id: str) -> dict:
    """One pairs set under the amended scoring: the rows, the floors and the order.

    The rows are formed by the same code as the registered ones, from the
    same cells with their amended counts. The order is the ruling's: a row is
    disqualified when the audit found content gone, wholly or in part, among
    its counted segments on a first run; the others are ranked by amended
    deviations per pair, a tie decided as the registered order decides it.
    """
    spec = reg["sets"][set_id]
    pairs = list(spec["items"])
    cells = [c for c in _amended_cells(scored, amended) if c["set"] == set_id]
    members = [r["id"] for r in reg["rows"] if set_id in r["sets"]]
    headline = [r["id"] for r in reg["rows"] if set_id in r["sets"] and r.get("headline", True)]
    floors = amended["baselines"]

    def finish(rows_: dict, common: list[str]) -> None:
        for rid, r in rows_.items():
            on = sorted(r["headline_draws"])
            mine = {(c["pair"], c["draw"]): c for c in cells if c["row"] == rid}
            r["headings_untaken"] = sum(mine[(p, r["headline_draws"][p])]["headings_untaken"]
                                        for p in on)
            r["union_deviations"] = sum(figure_rules.deviations(floors["union"][p])
                                        for p in on) if on else None
            r["no_better_than_union"] = bool(on) and r["deviations"] is not None and \
                r["deviations"] >= r["union_deviations"]

    common, head = _pairs_rows(reg, cells, headline, pairs)
    finish(head, common)
    verdicts = audit_verdicts(audit, head)
    for rid, r in head.items():
        r["audit"] = verdicts[rid]
        r["disqualified"] = verdicts[rid]["audited_loss"]
    block = {"scoring": AMENDED_RULE, "common_pairs": common, "rows": head,
             "order": order(head, {rid: _audit_reason(v) for rid, v in verdicts.items()
                                   if v["audited_loss"]}),
             "baselines": {name: _floor_amended(per, common) for name, per in floors.items()},
             "side": {}}
    for rid in members:
        row = next(r for r in reg["rows"] if r["id"] == rid)
        if row.get("headline", True):
            continue
        partner = row.get("compare_with")
        group = [rid] + ([partner] if partner else [])
        side_common, side = _pairs_rows(reg, cells, group,
                                        run_lineup.items_of(reg, row, set_id))
        finish(side, side_common)
        for sid, verdict in audit_verdicts(audit, side).items():
            side[sid]["audit"] = verdict
            side[sid]["disqualified"] = verdict["audited_loss"]
        block["side"][rid] = {"compared_with": partner, "common_pairs": side_common,
                              "rows": side}
    return block


def _case_brief(case: dict) -> dict:
    """One case as a sentence about it needs it: where it is, its text, both classes."""
    second = case.get("second_reading") or {}
    return {"configuration": case["configuration"], "pair": case["pair"],
            "draw": case["draw"], "segment": case["segment"], "kind": case["kind"],
            "text": case["text"], "group": case["group"],
            "first": case["first_reading"]["class"],
            "first_alternative": case["first_reading"]["alternative"],
            "second": second.get("class"), "second_alternative": second.get("alternative")}


def _audit_part(cases: list[dict], is_first) -> dict:
    """One set of cases in figures: one of the audit's two groups, or both together.

    `first_runs` and `all_runs` count the first reading, for the set and per
    configuration; `second_reading` counts the cases read twice and how many
    of them both readings class alike; `borderline` counts the cases whose
    first reading names an alternative, and how far the count of loss moves
    with each of them read the other way; `first_runs_lost` names the
    first-run cases of loss.
    """
    firsts = [case for case in cases if is_first(case)]
    twice = [case for case in cases if case.get("second_reading")]
    differing = [case for case in twice
                 if case["first_reading"]["class"] != case["second_reading"]["class"]]
    borderline = [case for case in cases if case["first_reading"]["alternative"]]
    configurations = list(dict.fromkeys(case["configuration"] for case in cases))
    per = {}
    for rid in configurations:
        mine = [case for case in cases if case["configuration"] == rid]
        mine_first = [case for case in mine if is_first(case)]
        per[rid] = {"first_runs": {"cases": len(mine_first),
                                   **_tally(mine_first, "first_reading")},
                    "all_runs": {"runs": len({(c["pair"], c["draw"]) for c in mine}),
                                 "cases": len(mine), **_tally(mine, "first_reading")}}
    return {
        "cases": len(cases),
        "runs": len({(c["configuration"], c["pair"], c["draw"]) for c in cases}),
        "configurations": per,
        "first_runs": {"cases": len(firsts), **_tally(firsts, "first_reading")},
        "all_runs": {"cases": len(cases), **_tally(cases, "first_reading")},
        "first_runs_lost": [_case_brief(case) for case in firsts
                            if case["first_reading"]["class"] in LOSS_CLASSES],
        "borderline": {
            "cases": len(borderline),
            "first_runs": sum(1 for case in borderline if is_first(case)),
            "lost_range": {"first_runs": _loss_range(firsts),
                           "all_runs": _loss_range(cases)}},
        "second_reading": {
            "cases": len(twice), **_tally(twice, "second_reading"),
            "same_class": len(twice) - len(differing),
            "different": [{"configuration": c["configuration"], "pair": c["pair"],
                           "draw": c["draw"], "segment": c["segment"],
                           "first": c["first_reading"]["class"],
                           "first_alternative": c["first_reading"]["alternative"],
                           "second": c["second_reading"]["class"],
                           "second_alternative": c["second_reading"]["alternative"]}
                          for c in differing],
            "lost_per_configuration": {
                rid: {"cases": sum(1 for c in twice if c["configuration"] == rid),
                      "lost": sum(1 for c in twice if c["configuration"] == rid
                                  and c["second_reading"]["class"] in LOSS_CLASSES)}
                for rid in configurations
                if any(c["configuration"] == rid for c in twice)}},
    }


def _per_row(keys, is_first) -> dict:
    """row id -> how many of `keys` (row, pair, draw, ...) are on a repeated run."""
    out: dict[str, int] = {}
    for key in keys:
        if not is_first({"configuration": key[0], "pair": key[1], "draw": key[2]}):
            out[key[0]] = out.get(key[0], 0) + 1
    return dict(sorted(out.items()))


def audit_summary(audit: dict, first: dict[str, dict], amended: dict) -> dict:
    """The audit in figures: each of its two groups, and the two together.

    No key of this block changes what it counts when the audit is extended.
    The keys it had when the audit held the counted segments and nothing else
    (`cases`, `runs`, `configurations`, `first_runs`, `all_runs`,
    `borderline`, `second_reading`, `amended_filing`, `runs_with_silent_loss`)
    still count those segments, and so does `first_runs_lost` beside them: a
    sentence written against one of them stays as true as it was. The second
    group stands beside them under its own name (`reworded_no_record`) and
    the two groups together under `both_groups`, each in the shape
    `_audit_part` gives. `covers` says so in the file.

    One thing follows the verdict and not the group, because it is a
    statement about the verdict: `verdict_depends_on_one`, the configurations
    whose verdict would change with a borderline case read the other way. The
    verdict runs over both groups, so the list does, and it stands in
    `borderline` here and in `both_groups`, the same list.

    `first` is `first_runs_of`: which draw of a pair is a first run.
    `amended_filing` holds, for each class of the first reading of a counted
    segment, what the amended scoring makes of its cases: still silent loss,
    found as reworded, or counted as an untaken heading. `unread` counts what
    has no record and is in neither group, so that the audit's page can say
    exactly what was not read.
    """
    cases = audit["cases"]
    amended_cells = {(c["row"], c["pair"], c["draw"]): c for c in amended["scored"]["cells"]}
    left = {}
    for cell in amended["differences"]["cells"]:
        for entry in cell["segments"]:
            if "silent" in entry["registered"] and "silent" not in entry["amended"]:
                left[(cell["row"], cell["pair"], cell["draw"], entry["segment"])] = (
                    "untaken_heading" if "headings_untaken" in entry["amended"]
                    else "reworded")

    def filing(selected: list[dict], reading: str) -> dict:
        out = {name: {"silent": 0, "reworded": 0, "untaken_heading": 0}
               for name in AUDIT_CLASSES}
        for case in selected:
            out[case[reading]["class"]][left.get(_case_key(case), "silent")] += 1
        return out

    def is_first(case: dict) -> bool:
        return first.get(case["configuration"], {}).get(case["pair"]) == case["draw"]

    def on_first(run: tuple) -> bool:
        return is_first({"configuration": run[0], "pair": run[1], "draw": run[2]})

    counted = [case for case in cases if case["group"] == COUNTED]
    reworded = [case for case in cases if case["group"] == REWORDED]
    whole = _audit_part(cases, is_first)
    # The configurations whose verdict would change with a borderline case
    # read the other way: loss by one reading of them, none by the other.
    depends = [rid for rid in whole["configurations"]
               if len({count > 0 for count in _loss_range(
                   [case for case in cases
                    if is_first(case) and case["configuration"] == rid])}) > 1]
    whole["borderline"]["verdict_depends_on_one"] = depends
    first_group = _audit_part(counted, is_first)
    first_group["borderline"]["verdict_depends_on_one"] = depends
    unread = amended["unread"]
    on_repeats = _per_row([(*run, identifier)
                           for run, ids in amended["reworded_no_record"].items()
                           for identifier in ids], is_first)
    as_a_run = {(*run, identifier): step for run, found in unread["as_a_run"].items()
                for identifier, step in found.items() if on_first(run)}
    titles = [(*run, identifier) for run, ids in unread["titles"].items()
              for identifier in ids if on_first(run)]
    twice = [case for case in counted if case.get("second_reading")]
    return {
        "date": audit["date"],
        "covers": (f"The audit holds two groups of cases. This block's own keys (cases, "
                   f"runs, configurations, first_runs, all_runs, first_runs_lost, "
                   f"borderline, second_reading, amended_filing, runs_with_silent_loss) "
                   f"count the first group and nothing else, the segments the registered "
                   f"scoring counted as silent loss, as they did before the audit was "
                   f"extended. `{REWORDED}` counts the second group, the segments on first "
                   f"runs that the similarity rule alone calls reworded and that no record "
                   f"names. `{BOTH}` counts the two together, which is what a row's "
                   f"verdict runs over. `verdict_depends_on_one` is about the verdict, so "
                   f"it is over both groups wherever it stands."),
        **first_group,
        "amended_filing": {"all_runs": filing(counted, "first_reading"),
                           "first_runs": filing([case for case in counted if is_first(case)],
                                                "first_reading"),
                           "second_reading": filing(twice, "second_reading")},
        "runs_with_silent_loss": {
            "registered": sum(1 for ids in amended["silent_registered"].values() if ids),
            "amended": sum(1 for cell in amended_cells.values() if cell["silent"])},
        REWORDED: _audit_part(reworded, is_first),
        BOTH: whole,
        "unread": {
            # Reworded by the similarity rule alone, no record, on a repeated
            # run: the second group's kind of segment, where it was not read.
            "reworded_no_record_on_repeated_runs": {
                "cases": sum(on_repeats.values()), "configurations": on_repeats},
            # Called reworded by the similarity rule, no record, on a first
            # run, and its words also stand in the merge as one unbroken run.
            "reworded_as_a_run_no_record_on_first_runs": {
                "cases": len(as_a_run),
                **{step: sum(1 for found in as_a_run.values() if found == step)
                   for step in reconcile.RUN_STEPS}},
            # A source title the merge does not have and wrote no record for,
            # on a first run. Left out of silent loss by the registration.
            "titles_absent_no_record_on_first_runs": {
                "cases": len(titles),
                "configurations": dict(sorted(
                    {rid: sum(1 for key in titles if key[0] == rid)
                     for rid in {key[0] for key in titles}}.items()))}},
    }


def properties(reg: dict, formed: dict, amended: dict, audit: dict) -> list[dict]:
    """The amendment's eight properties, each with whether it holds and its figures.

    Stated in the registration before the amended rule was run on this run's
    cells; this is what the re-scoring found. A property that fails names
    what it fails on.
    """
    summary, facts = formed["audit"], amended["facts"]
    filing = summary["amended_filing"]
    scored, differences = amended["scored"], amended["differences"]
    lost_classes = {name: filing["all_runs"][name] for name in LOSS_CLASSES}
    cleared_losses = sum(counts["reworded"] + counts["untaken_heading"]
                         for counts in lost_classes.values())
    second_moved = sum(filing["second_reading"][name][kind] for name in LOSS_CLASSES
                       for kind in ("reworded", "untaken_heading"))
    out = [{
        "property": 1, "name": "No loss is cleared", "holds": cleared_losses == 0,
        "figures": {"gone": filing["all_runs"]["gone"], "partly": filing["all_runs"]["partly"],
                    "present": filing["all_runs"]["present"],
                    "not_content": filing["all_runs"]["not_content"],
                    "first_runs": {name: filing["first_runs"][name] for name in AUDIT_CLASSES},
                    "second_reading_loss_cases_no_longer_silent": second_moved}}]
    two = [problem for problem in facts["problems"] if problem.startswith("property 2")]
    total = {"registered": sum(len(ids) for ids in amended["silent_registered"].values()),
             "amended": sum(cell["silent"] for cell in scored["cells"]),
             "headings_untaken": sum(cell["headings_untaken"] for cell in scored["cells"])}
    out.append({"property": 2, "name": "Only clearings", "holds": not two,
                "figures": {"merges_checked": facts["runs"], "cells": len(scored["cells"]),
                            "silent_loss": total,
                            "runs_with_silent_loss": summary["runs_with_silent_loss"]},
                "failures": two})
    references = scored["references"]
    clean = all(figures[rule] == {"silent": 0, "headings_untaken": 0}
                for figures in references.values() for rule in (RULE, AMENDED_RULE))
    out.append({"property": 3, "name": "The reference merges stay clean", "holds": clean,
                "figures": {"reference_merges": len(references),
                            "silent": sum(f[AMENDED_RULE]["silent"] + f[RULE]["silent"]
                                          for f in references.values()),
                            "headings_untaken": sum(f[AMENDED_RULE]["headings_untaken"]
                                                    for f in references.values())}})
    floors = {name: {"registered": formed["S1_registered"]["baselines"][name],
                     "amended": formed["S1"]["baselines"][name]}
              for name in formed["S1"]["baselines"]}
    four = all(floors[name][rule]["silent_loss"] == 0
               for name in ("concatenation", "union") for rule in ("registered", "amended"))
    out.append({"property": 4, "name": "Concatenation and the mechanical union stay at "
                "zero silent loss", "holds": four,
                "figures": {name: {rule: floors[name][rule]["silent_loss"]
                                   for rule in ("registered", "amended")}
                            for name in ("concatenation", "union")}})
    base_moved = [(entry["pair"], segment_) for entry in differences["baselines"]
                  if entry["baseline"] == "base_only" for segment_ in entry["segments"]
                  if "silent" in segment_["registered"] and "silent" not in segment_["amended"]]
    refiled: dict[str, list[str]] = {}
    for pair, segment_ in base_moved:
        if segment_["decided_by"] == "heading":
            refiled.setdefault(pair, []).append(segment_["text"])
    body_cleared = [f"{pair} {segment_['segment']}" for pair, segment_ in base_moved
                    if segment_["decided_by"] != "heading"]
    base = floors["base_only"]
    five = (not body_cleared and refiled == BASE_ONLY_UNTAKEN
            and (base["registered"]["silent_loss"], base["amended"]["silent_loss"])
            == (129, 121))
    out.append({"property": 5, "name": "Base only keeps its losses", "holds": five,
                "figures": {"silent_loss": {"registered": base["registered"]["silent_loss"],
                                            "amended": base["amended"]["silent_loss"]},
                            "headings_untaken": base["amended"]["headings_untaken"],
                            "headings": refiled, "sentences_cleared": len(body_cleared),
                            "headings_still_silent":
                                facts["base_only_headings_still_silent"]},
                "failures": body_cleared})
    six = [problem for problem in facts["problems"] if problem.startswith("property 6")]
    out.append({"property": 6, "name": "Every clearing can be read", "holds": not six,
                "figures": {"cleared": sum(facts["cleared"].values()), **facts["cleared"],
                            "merges_checked": facts["runs"]},
                "failures": six})
    moves = [(entry["pair"], entry["segment"], entry["decided_by"])
             for entry in differences["references"]]
    floor_moves = {name: (column, formed["floor_bands"][name]["registered"][column],
                          formed["floor_bands"][name]["amended"][column])
                   for name, (column, _, _) in FLOOR_MOVES.items()}
    out.append({"property": 7, "name": "The band moves a little and in a known place",
                "holds": moves == REFERENCE_MOVES and floor_moves == FLOOR_MOVES,
                "figures": {"reference_segments_moved": [list(move) for move in moves],
                            "floors": {name: {"column": column, "registered": before,
                                              "amended": after}
                                       for name, (column, before, after)
                                       in floor_moves.items()}}})
    eight = [problem for problem in facts["problems"] if problem.startswith("property 8")]
    out.append({"property": 8, "name": "The registered rule's own clearings are untouched "
                "and are not vouched for", "holds": not eight,
                "figures": {"reworded_by_similarity": facts["reworded_by_similarity"],
                            "similarity_alone_in_the_cells": facts["similarity_alone"],
                            "merges_checked": facts["runs"]},
                "failures": eight})
    return out


def cut_short_control(pairs: list[str]) -> dict:
    """The second defect the amendment names and does not address, measured.

    Every sentence, list item and table row of the pairs' sources that has at
    least six words and stands once in its document, with its last two words
    cut and nothing put in their place, located in its own document under the
    registered rule. `reworded` is how many of them the similarity rule then
    calls reworded although two words of the sentence are gone. The amended
    rule is additive and leaves every one of them as it is.
    """
    import dataclasses

    sentences = reworded = 0
    for pair in pairs:
        for text in rank_matrix.pair_docs(pair).values():
            document = segment.segment_document(text, "a", "source_a.md")
            flat = reconcile.flatten(text)
            for item in document.segments:
                if item.kind not in reconcile.BODY_KINDS \
                        or len(reconcile.words(item.text)) < 6 \
                        or text.count(item.text) != 1 \
                        or flat.count(reconcile.flatten(item.text)) != 1:
                    continue
                bare = item.text.rstrip(".!?:;,")
                pieces = bare.split(" ")
                if len(pieces) < 6 or not reconcile.content_words(
                        reconcile.words(" ".join(pieces[-2:]))):
                    continue
                cut = text.replace(item.text, " ".join(pieces[:-2])
                                   + (item.text[len(bare):] or "."), 1)
                found = reconcile.locate(
                    dataclasses.replace(document, segments=(item,)), reconcile.flatten(cut),
                    segment.segment_document(cut, reconcile.MERGE_LETTER).segments,
                    rule=RULE).located[0]
                sentences += 1
                reworded += found.verdict == reconcile.REWORDED
    return {"sentences": sentences, "last_two_words_cut_read_as_reworded": reworded}


def with_amended(reg: dict, scored: list[dict], formed: dict, amended: dict,
                 audit: dict) -> dict:
    """figures.json for a run published under both scorings, the amended one first.

    `formed` is the registered layer as `rows` gives it. Each pairs set `S`
    moves to `S_registered`, unchanged, and `S` becomes the amended block.
    """
    out: dict = {"pin": formed["pin"], "rules": formed["rules"],
                 "scoring": {"shown_first": AMENDED_RULE, "amendment": AMENDMENT,
                             "audit_amendment": AUDIT_AMENDMENT,
                             "amended": "S1", "registered": "S1_registered",
                             "disqualified_by": "audited loss on a first run "
                                                "(audit/audit.json), not the count of "
                                                "silent loss"}}
    stored = amended["scored"]
    if [s for s, spec in reg["sets"].items() if spec["score"] == "pairs"] != ["S1"]:
        raise SystemExit("lineup_figures: the amended scoring is written for a registration "
                         "whose one pairs set is S1")
    for set_id, spec in reg["sets"].items():
        if spec["score"] == "pairs":
            out[set_id] = amended_block(reg, scored, stored, audit, set_id)
            out[f"{set_id}_registered"] = formed[set_id]
        else:
            out[set_id] = formed[set_id]
    pairs = out["S1"]["common_pairs"]
    # What the rule change alone does to the floors (Amendment 3's property 7):
    # both rules on the references as registered, so that a later correction
    # to a reference (Amendments 5 and 6) does not pass for an effect of the rule.
    registered_floors = _floor_parts(pairs, reg["settings"]["base"], RULE)
    amended_floors = _floor_parts(pairs, reg["settings"]["base"], AMENDED_RULE)
    out["floor_bands"] = {
        name: {"registered": {"lost": registered_floors[name]["lost"],
                              "bloat": registered_floors[name]["bloat"]},
               "amended": {"lost": amended_floors[name]["lost"],
                           "bloat": amended_floors[name]["bloat"]},
               "amended_deviations_per_pair": amended_floors[name]["deviations_per_pair"]}
        for name in out["S1"]["baselines"]}
    first = first_runs_of(out)
    if first != first_runs_of({"S1": out["S1_registered"]}):
        raise SystemExit("lineup_figures: the two scorings do not read the same draw of "
                         "every pair, so `a first run` would mean two things")
    out["audit"] = audit_summary(audit, first, amended)
    out["properties"] = properties(reg, out, amended, audit)
    out["second_defect"] = cut_short_control(pairs)
    return out


def _floor_parts(pairs: list[str], base: str, rule: str) -> dict:
    """Each floor's lost and bloat under `rule`, on the references as registered, summed over `pairs`."""
    floors = baselines(pairs, base, rule=rule, reference=REGISTERED_REFERENCE)
    return {name: {"lost": sum(per[p]["lost"] for p in pairs),
                   "bloat": sum(per[p]["bloat"] for p in pairs),
                   "deviations_per_pair": _floor(per, pairs)["deviations_per_pair"]}
            for name, per in floors.items()}


# --- the amended scoring and the audit, as a reader sees them --------------------------

def _audit_text(verdict: dict) -> str:
    """One row's audit cell: what the reading found among the segments it read there."""
    if not verdict["cases"]:
        return "-"
    words = _borderline_words(verdict)
    return (f"{verdict['lost']} of {verdict['cases']} gone or partly gone"
            + (f": disqualified; {words}" if words else "")
            + ("; readings disagree" if verdict["readings_disagree"] else ""))


def _tie_lines(block: dict) -> list[str]:
    """Every tie of the amended order in a sentence, and how it was decided."""
    ties = block["order"].get("ties") or []
    if not ties:
        return ["Ties: no two ranked rows have the same deviations per pair."]
    out = []
    for tie in ties:
        names = " and ".join(tie["rows"])
        detail = "; ".join(
            f"{rid}: {tie['cost_unit'][rid]} {_money_text(tie['usd_per_merge'][rid])} dollars, "
            f"{_num(tie['seconds_per_merge'][rid])} seconds a merge" for rid in tie["rows"])
        if tie["shared"]:
            out.append(f"Ties: {names} have {_rate(tie['deviations_per_pair'])} deviations per "
                       f"pair and share rank {tie['rank']}. Cost and then speed decide a tie "
                       f"only where every row in it is list-priced, and these are not "
                       f"({detail}), so the tie is stated and not broken.")
        else:
            out.append(f"Ties: {names} have {_rate(tie['deviations_per_pair'])} deviations per "
                       f"pair; every row in the tie is list-priced, so list dollars and then "
                       f"seconds decide ({detail}).")
    return out


def _amended_lines(set_id: str, block: dict, formed: dict) -> list[str]:
    """The amended scoring of one pairs set: the table, the ties, the spread, the side table."""
    common = block.get("common_pairs") or []
    lines = [f"## {set_id}: the pairs under the amended scoring, lowest counted draw, over "
             f"the {len(common)} common pairs", "",
             f"The scoring shown first. It was made after every call of this run and after "
             f"its results were known (`REGISTRATION.md`, {AMENDMENT}); the scoring as "
             f"registered and run follows it, unchanged. Disqualify, then rank: a row is "
             f"disqualified (`DQ`) when the audit by reading found content gone, wholly or in "
             f"part, on one of its first runs (`audit/README.md`). The audit read every "
             f"source segment there that the merge does not carry word for word and wrote no "
             f"record for: the segments the registered scoring counted as silent loss and, "
             f"since {AUDIT_AMENDMENT}, the segments the similarity rule alone calls "
             f"reworded. The column `audit, first run` gives what it found of how many it "
             f"read, and says so where a row's disqualification rests on borderline cases "
             f"only. "
             f"`silent` is the program's count under the amended rule, source segments it "
             f"could not find in the merge and that no record explains; it does not "
             f"disqualify. `untaken` counts source headings the merge did not take and did "
             f"not record while their sections survived. The other rows are ranked by "
             f"deviations per pair, equal deviations sharing a rank unless every row in the "
             f"tie is list-priced (then list dollars, then seconds), as registered. A row "
             f"that did not complete every pair is listed after every complete row with its "
             f"figures over the pairs it completed. One draw a cell: an order by the rule, "
             f"not a ranking claim.", "",
             "| # | row | pairs | silent | /pair | untaken | audit, first run | dev | /pair | "
             "vs union | $ / merge | unit | billed $ | s / merge | tokens / merge | "
             "model-conf | incomplete | excluded | unruled calls | reused calls | "
             "not completed |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
             "---|---|"]
    ranked = (block["order"]["survivors"]
              + [d["row"] for d in block["order"]["incomplete"]]
              + [d["row"] for d in block["order"]["disqualified"]])
    for rid in ranked:
        r = block["rows"][rid]
        versus = "-" if r["union_deviations"] is None else (
            f"NO BETTER ({r['union_deviations']})" if r["no_better_than_union"]
            else f"below ({r['union_deviations']})")
        lines.append(
            f"| {_rank_text(block, rid)} | {rid} | {r['pairs']} of {len(common)} | "
            f"{_count(r['silent_loss'])} | {_rate(r['silent_loss_per_pair'])} | "
            f"{r['headings_untaken']} | {_audit_text(r['audit'])} | "
            f"{_count(r['deviations'])} | {_rate(r['deviations_per_pair'])} | "
            f"{versus} | {_money_text(r['usd_per_merge'])} | {r['cost_unit']} | "
            f"{_money_text(r['billed_upper_bound_usd_per_merge'])} | "
            f"{_num(r['seconds_per_merge'])} | {_count(r['tokens_sent_per_merge'])} | "
            f"{r['model_confirmed_declarations']} | {r['incomplete_text'] or '-'} | "
            f"{len(r['excluded'])} | {r['unruled_calls']} | {r['reused_calls']} | "
            f"{', '.join(r['pairs_not_completed']) or '-'} |")
    for name, floor in (block.get("baselines") or {}).items():
        lines.append(
            f"| base | {name} | {floor['pairs']} of {len(common)} | "
            f"{floor['silent_loss']} | {_rate(floor['silent_loss_per_pair'])} | "
            f"{floor['headings_untaken']} | - | "
            f"{floor['deviations']} | {_rate(floor['deviations_per_pair'])} | - | - | "
            f"no model | - | - | - | - | - | - | - | - | - |")
    lines += [""] + _tie_lines(block)
    flagged = [rid for rid in ranked if block["rows"][rid]["no_better_than_union"]]
    lines += ["", "Floors, scored by the same scorer under the amended rule from the sources "
              "with no model call: byte-concatenation, a mechanical union (the base, then "
              "every paragraph of the other not already in it, its title dropped) and "
              "base-only. `vs union` holds each row against the union on the same pairs; "
              + (f"no better than a mechanical union: {', '.join(flagged)}."
                 if flagged else "every counted row is below the union.")
              + " The route, the effort and the model ids of each row do not depend on the "
              "scoring and are in the table under the registered scoring."]
    spread = [(rid, pair, d) for rid in ranked
              for pair, d in block["rows"][rid]["spread_draws"].items()]
    if spread:
        lines += ["", "Spread pairs under the amended scoring, every counted draw "
                  "(min / median / max):", "",
                  "| row | pair | draws | silent | deviations |", "|---|---|---|---|---|"]
        for rid, pair, d in spread:
            lines.append(f"| {rid} | {pair} | {d['draws']} | {_spread(d['silent_loss'])} "
                         f"| {_spread(d['deviations'])} |")
    for rid, side in (block.get("side") or {}).items():
        lines += ["", f"Side table under the amended scoring, {rid}"
                  + (f" against {side['compared_with']}" if side['compared_with']
                     else " (not in the headline)")
                  + f", over {len(side['common_pairs'])} common pair(s):", "",
                  "| row | pairs | silent | untaken | dev | $ / merge | unit | s / merge | "
                  "incomplete | not completed |", "|---|---|---|---|---|---|---|---|---|---|"]
        for sid, r in side["rows"].items():
            lines.append(f"| {sid} | {r['pairs']} of {len(side['common_pairs'])} | "
                         f"{_count(r['silent_loss'])} | {r['headings_untaken']} | "
                         f"{_count(r['deviations'])} | "
                         f"{_money_text(r['usd_per_merge'])} | {r['cost_unit']} | "
                         f"{_num(r['seconds_per_merge'])} | "
                         f"{r['incomplete_text'] or '-'} | "
                         f"{', '.join(r['pairs_not_completed']) or '-'} |")
    return lines


def _counted_alone(formed: dict) -> list[str]:
    """The rows with loss among the counted segments on a first run, as the order lists rows.

    Who the audit disqualified while it held the counted segments and nothing
    else, which is what the registration's Amendment 3 names.
    """
    lost = {case["configuration"] for case in formed["audit"]["first_runs_lost"]}
    block = formed["S1"]
    return sorted((rid for rid in block["rows"] if rid in lost),
                  key=lambda rid: (block["rows"][rid]["silent_loss_per_pair"],
                                   float("inf") if block["rows"][rid]["deviations_per_pair"]
                                   is None else block["rows"][rid]["deviations_per_pair"], rid))


def _difference_lines(set_id: str, formed: dict) -> list[str]:
    """What differs between the two scorings and why, in one paragraph."""
    two = next(p for p in formed["properties"] if p["property"] == 2)["figures"]
    counted = formed["audit"]
    reworded = formed["audit"][REWORDED]
    first = counted["first_runs"]
    more = reworded["first_runs"]
    before = [d["row"] for d in formed[f"{set_id}_registered"]["order"]["disqualified"]]
    between = _counted_alone(formed)
    after = [d["row"] for d in formed[set_id]["order"]["disqualified"]]
    return [f"## What differs between the two scorings of {set_id}, and why", "",
            f"The registered scoring counts a source segment as silent loss when its text is "
            f"not in the merge word for word, no record names it and no single merge segment "
            f"is at least 0.68 similar to it, and it disqualifies a row on that count. An "
            f"audit by reading of every segment counted this way ({counted['cases']} "
            f"over {counted['runs']} runs, {first['cases']} of them on first runs) "
            f"found most of them still in the merge: on first runs "
            f"{first['gone'] + first['partly']} gone or partly gone, {first['present']} "
            f"present in other words and {first['not_content']} not content, which are "
            f"headings the merge did not take (`audit/README.md`). The amended scoring (`REGISTRATION.md`, "
            f"{AMENDMENT}) also finds a sentence whose words stand in the merge as one "
            f"unbroken run, counts an untaken heading apart from lost content, reads the "
            f"reference merge by the same rule, and disqualifies on what the audit found gone "
            f"and not on the program's count: over the {two['cells']} scored cells the "
            f"counted silent losses go from {two['silent_loss']['registered']} to "
            f"{two['silent_loss']['amended']}, with {two['silent_loss']['headings_untaken']} "
            f"counted as untaken headings, the runs with a counted silent loss from "
            f"{two['runs_with_silent_loss']['registered']} to "
            f"{two['runs_with_silent_loss']['amended']}, and the disqualified rows from "
            f"{len(before)} ({', '.join(before)}) to {len(between)} ({', '.join(between)}). "
            f"The audit was then extended ({AUDIT_AMENDMENT}) to the segments on first runs "
            f"that the similarity rule alone calls reworded and that no record names, which "
            f"neither scoring counts: {more['cases']} segments, {more['gone'] + more['partly']} "
            f"of them gone or partly gone. That changes no count and no figure of either "
            f"scoring; the disqualified rows are now {len(after)} ({', '.join(after)}). "
            f"Every segment whose count differs is listed with the merge text it was found "
            f"in, in `{DIFFERENCES}`."]


def _class_cells(tally: dict) -> str:
    return " | ".join(str(tally[name]) for name in AUDIT_CLASSES)


def _named(names: list[str]) -> str:
    """ "a", "a and b", "a, b and c"."""
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def _counts_by_row(counts: dict) -> str:
    """ "`row` 8, `other` 5": most first, then by name."""
    return ", ".join(f"`{rid}` {count}" for rid, count in sorted(
        counts.items(), key=lambda item: (-item[1], item[0])))


def _alternative_words(case: dict) -> str:
    """Which reading of one case names an alternative class, in words; "" where neither does."""
    first, second = case["first_alternative"], case["second_alternative"]
    if first and first == second:
        return f"both readings name {CLASS_WORDS[first]} as the alternative"
    parts = [f"the {name} reading names {CLASS_WORDS[alternative]} as the alternative"
             for name, alternative in (("first", first), ("second", second)) if alternative]
    return " and ".join(parts)


def _loss_case_words(case: dict, configuration: bool = True) -> str:
    """One case of loss in a sentence: where it is, its text, its class, its alternatives."""
    if case["second"] in (None, case["first"]):
        found = CLASS_WORDS[case["first"]]
    else:
        found = (f"{CLASS_WORDS[case['first']]} by the first reading, "
                 f"{CLASS_WORDS[case['second']]} by the second")
    words = _alternative_words(case)
    return ((f"`{case['configuration']}`, " if configuration else "")
            + f"`{case['pair']}`, segment `{case['segment']}`, {_quoted(case['text'])}: "
            + found + (f" ({words})" if words else ""))


def audit_tables(formed: dict) -> str:
    """The audit's result in tables and sentences, as `audit/README.md` must carry them.

    Generated, so that no figure in that page is typed: `--check` requires
    this text in the page, line for line.
    """
    counted = formed["audit"]
    rows_ = formed["S1"]["rows"]
    reworded, summary = counted[REWORDED], counted[BOTH]
    groups = {COUNTED: counted, REWORDED: reworded}
    per = summary["configurations"]
    empty = {"cases": 0}

    def by_cases(part: dict, scope: str) -> list[str]:
        per_ = part["configurations"]
        return sorted((rid for rid in per_ if per_[rid][scope]["cases"]),
                      key=lambda rid: (per_[rid][scope]["cases"], rid))

    def in_group(group: str, rid: str) -> int:
        return groups[group]["configurations"].get(rid, {"first_runs": empty})[
            "first_runs"]["cases"]

    lines = ["### Result on first runs", "",
             "The runs the order counts: the first counted draw of each pair. Every case on "
             "them was read twice, and the classes in these tables are the first reading's. "
             "`read` is how many segments of a configuration the audit read there: those the "
             "registered scoring counted as silent loss (`counted`), and those the "
             "similarity rule alone called reworded and no record of the merge names "
             "(`reworded, no record`). `audited loss` is the verdict.", "",
             "| configuration | read | counted | reworded, no record | gone | partly gone | "
             "present | not content | audited loss |", "|---|---|---|---|---|---|---|---|---|"]
    for rid in by_cases(summary, "first_runs"):
        tally = per[rid]["first_runs"]
        verdict = rows_[rid]["audit"]
        words = _borderline_words(verdict)
        word = ("yes" if verdict["audited_loss"] else "no") + (
            f": disqualified; {words}" if words else "") + (
            " (readings disagree)" if verdict["readings_disagree"] else "")
        lines.append(f"| {rid} | {tally['cases']} | {in_group(COUNTED, rid)} | "
                     f"{in_group(REWORDED, rid)} | {_class_cells(tally)} | {word} |")
    lines.append(f"| all | {summary['first_runs']['cases']} | {counted['first_runs']['cases']} "
                 f"| {reworded['first_runs']['cases']} | "
                 f"{_class_cells(summary['first_runs'])} | |")
    for group, column in ((COUNTED, "counted"), (REWORDED, "reworded, no record")):
        lines += ["", f"The segments {GROUP_WORDS[group]}, on first runs:", "",
                  f"| configuration | {column} | gone | partly gone | present | not content |",
                  "|---|---|---|---|---|---|"]
        for rid in by_cases(groups[group], "first_runs"):
            tally = groups[group]["configurations"][rid]["first_runs"]
            lines.append(f"| {rid} | {tally['cases']} | {_class_cells(tally)} |")
        lines.append(f"| all | {groups[group]['first_runs']['cases']} | "
                     f"{_class_cells(groups[group]['first_runs'])} |")
    lost = summary["first_runs_lost"]
    lines += ["", f"The {len(lost)} first-run cases the first reading classed gone or partly "
              f"gone:" if lost else "No first-run case is classed gone or partly gone.", ""]
    lines += [f"- {GROUP_WORDS[case['group']][0].upper()}{GROUP_WORDS[case['group']][1:]}: "
              f"{_loss_case_words(case)}." for case in lost]
    lines += ["", "### Result over all runs, repeats included", "",
              f"The segments {GROUP_WORDS[COUNTED]}, in every run that had one. The segments "
              f"{GROUP_WORDS[REWORDED]} were read on first runs only and are not in this "
              f"table.", "",
              "| configuration | runs | counted | gone | partly gone | present | "
              "not content |", "|---|---|---|---|---|---|---|"]
    for rid in by_cases(counted, "all_runs"):
        tally = counted["configurations"][rid]["all_runs"]
        lines.append(f"| {rid} | {tally['runs']} | {tally['cases']} | {_class_cells(tally)} |")
    lines.append(f"| all | {counted['runs']} | {counted['all_runs']['cases']} | "
                 f"{_class_cells(counted['all_runs'])} |")
    second = summary["second_reading"]
    lines += ["", "### The two readings", "",
              f"Every first-run case was read twice: {second['cases']} cases. "
              + " ".join(
                  f"Of the {groups[group]['second_reading']['cases']} segments "
                  f"{GROUP_WORDS[group]}, both readings give the same class to "
                  f"{groups[group]['second_reading']['same_class']}." for group in GROUPS),
              "",
              "| configuration | cases | gone or partly gone, first reading | gone or partly "
              "gone, second reading | same verdict |", "|---|---|---|---|---|"]
    for rid in sorted(second["lost_per_configuration"],
                      key=lambda rid: (second["lost_per_configuration"][rid]["cases"], rid)):
        mine = second["lost_per_configuration"][rid]
        verdict = rows_[rid]["audit"]
        lines.append(f"| {rid} | {mine['cases']} | {verdict['lost']} | {mine['lost']} | "
                     f"{'no' if verdict['readings_disagree'] else 'yes'} |")
    lines += [""]
    for case in second["different"]:
        lines.append(
            f"- Differs: `{case['configuration']}`, `{case['pair']}`, draw {case['draw']}, "
            f"segment `{case['segment']}`. First reading: {CLASS_WORDS[case['first']]}"
            + (f", with {CLASS_WORDS[case['first_alternative']]} as the alternative"
               if case["first_alternative"] else "")
            + f". Second reading: {CLASS_WORDS[case['second']]}"
            + (f", with {CLASS_WORDS[case['second_alternative']]} as the alternative"
               if case["second_alternative"] else "") + ".")
    disagree = [rid for rid in rows_ if rows_[rid]["audit"]["readings_disagree"]]
    lines += ["", ("The two readings come to the same verdict for every configuration."
                   if not disagree else "The two readings come to different verdicts for: "
                   + ", ".join(disagree) + ".")]
    border = summary["borderline"]
    low, high = border["lost_range"]["first_runs"]
    low_all, high_all = counted["borderline"]["lost_range"]["all_runs"]
    lines += ["", f"{border['cases']} of the {summary['cases']} classifications of the first "
              f"reading are marked borderline, {border['first_runs']} of them on first runs. "
              f"With every borderline case read the other way, gone plus partly gone is "
              f"{low} to {high} on first runs, and {low_all} to {high_all} over all runs of "
              f"the segments {GROUP_WORDS[COUNTED]}. "
              + ("No configuration's verdict depends on a borderline case."
                 if not border["verdict_depends_on_one"] else
                 "The verdict depends on a borderline case for: "
                 + ", ".join(border["verdict_depends_on_one"]) + ".")]
    for rid in rows_:
        words = _borderline_words(rows_[rid]["audit"])
        if words:
            mine = [case for case in lost if case["configuration"] == rid]
            lines += ["", f"`{rid}` is disqualified; {words}: "
                      + "; ".join(_loss_case_words(case, configuration=False)
                                  for case in mine) + "."]
    filing = counted["amended_filing"]["all_runs"]
    lines += ["", f"### What the amended scoring makes of the segments "
              f"{GROUP_WORDS[COUNTED]}", "",
              "| first reading | cases | still counted as silent loss | found, reworded | "
              "counted as an untaken heading |", "|---|---|---|---|---|"]
    for name in AUDIT_CLASSES:
        mine = filing[name]
        lines.append(f"| {CLASS_WORDS[name]} | {sum(mine.values())} | {mine['silent']} | "
                     f"{mine['reworded']} | {mine['untaken_heading']} |")
    lines += ["", f"The {reworded['cases']} segments {GROUP_WORDS[REWORDED]} are not in this "
              f"table: both scorings call them reworded, and neither counts them."]
    unread = counted["unread"]
    repeats = unread["reworded_no_record_on_repeated_runs"]
    as_a_run = unread["reworded_as_a_run_no_record_on_first_runs"]
    titles = unread["titles_absent_no_record_on_first_runs"]
    lines += ["", "### What has no record and was not read", "",
              f"- On repeated runs: {repeats['cases']} segments that the similarity rule "
              f"alone calls reworded and that no record names"
              + (f" ({_counts_by_row(repeats['configurations'])})." if repeats["cases"]
                 else "."),
              f"- On first runs: {as_a_run['cases']} segments that the similarity rule calls "
              f"reworded and that no record names, whose words also stand in the merge as one "
              f"unbroken run, in order: {as_a_run[reconcile.STEP_PHRASE]} with every word, "
              f"punctuation and capitals aside, and {as_a_run[reconcile.STEP_CONTAINMENT]} "
              f"with every word but small connecting words. The audit takes these as carried "
              f"word for word.",
              f"- On first runs: {titles['cases']} source titles that are not in the merge "
              f"and that no record names"
              + (f" ({_counts_by_row(titles['configurations'])})." if titles["cases"] else ".")
              + " The registration leaves a title out of silent loss."]
    return "\n".join(lines) + "\n"


def _quoted(text: str) -> str:
    return '"' + " ".join(text.split()) + '"'


def _reading_words(reading: dict) -> str:
    """ "partly gone, with present as the alternative. <evidence>" """
    return (CLASS_WORDS[reading["class"]]
            + (f", with {CLASS_WORDS[reading['alternative']]} as the alternative"
               if reading["alternative"] else "") + f". {reading['evidence']}")


def render_cases(run_dir: Path, audit: dict, amended: dict, formed: dict) -> str:
    """audit/cases.md: every audited case with its quotations, and the second reading's table.

    Run by run. A case of the first group is shown as the first reading found
    it, with the second reading's line where there is one; a case of the
    second group is shown with both readings in full.
    """
    info_of = {COUNTED: amended["counted"], REWORDED: amended["reworded"]}
    left = {}
    for cell in amended["differences"]["cells"]:
        for entry in cell["segments"]:
            left[(cell["row"], cell["pair"], cell["draw"], entry["segment"])] = entry
    first_draws = first_runs_of(formed)
    groups = {COUNTED: formed["audit"], REWORDED: formed["audit"][REWORDED]}
    lines = ["# The audited cases", "",
             f"Generated by `tests/lineup_figures.py` from `audit.json` and the stored runs; "
             f"`--check` requires this page back. {len(audit['cases'])} cases, run by run. "
             f"{groups[COUNTED]['cases']} are source segments the registered scoring of this "
             f"benchmark counted as silent loss, each with what the first reading found in "
             f"the merged document of that run; the second reading's table of the first-run "
             f"cases among them is at the end. {groups[REWORDED]['cases']} are segments on "
             f"first runs that the similarity rule alone called reworded and that no record "
             f"of the merge names, each with both readings; their titles say "
             f"`{GROUP_WORDS[REWORDED]}`. `README.md` beside this page says what was read, by "
             f"whom and how the classes were applied.", ""]
    previous = None
    # Run by run, each run's cases in the order audit.json has them.
    ordered = sorted(audit["cases"], key=lambda case: (case["configuration"], case["pair"],
                                                       case["draw"]))
    for case in ordered:
        key = _case_key(case)
        row, pair, draw, identifier = key
        group = case["group"]
        info = info_of[group][key]
        run = (row, pair, draw)
        if run != previous:
            previous = run
            first = first_draws.get(row, {}).get(pair) == draw
            lines += [f"## {row}, {pair}, draw {draw} "
                      f"({'first run, counted by the order' if first else 'repeat'})", "",
                      f"The run: `{info['dir']}/`.", ""]
        reading = case["first_reading"]
        title = CLASS_WORDS[reading["class"]]
        if reading["alternative"]:
            title += f" (borderline, could be read as {CLASS_WORDS[reading['alternative']]})"
        lines += [f"### {row} / {pair} / d{draw} / `{identifier}`"
                  + (f", {GROUP_WORDS[REWORDED]}" if group == REWORDED else "")
                  + f": {title}", ""]
        span = case["source_lines"]
        where = f"line {span[0]}" if span[0] == span[1] else f"lines {span[0]} to {span[1]}"
        lines.append(f"- Source segment ({case['kind'].replace('_', ' ')}), "
                     f"`tests/pairs/{pair}/{case['document']}`, {where}: "
                     f"{_quoted(case['text'])}")
        if group == REWORDED:
            lines.append(f"- As both scorings have it: reworded, by the similarity rule "
                         f"alone, and no record of the merge names it. The nearest merge "
                         f"segment, {info['nearest']}, is {info['ratio']:.3f} similar: "
                         f"{_quoted(info['nearest_text'])}")
            lines.append(f"- First reading: {_reading_words(reading)}")
            lines.append(f"- Second reading: {_reading_words(case['second_reading'])}")
            lines.append("")
            continue
        lines.append(f"- As the registered scoring counted it: not in the merge word for "
                     f"word, no record, and the nearest merge segment, {info['nearest']}, is "
                     f"{info['ratio']:.3f} similar: {_quoted(info['nearest_text'])}")
        entry = left.get(key)
        if entry is None or "silent" in entry["amended"]:
            lines.append("- Under the amended scoring: still counted as silent loss.")
        elif "headings_untaken" in entry["amended"]:
            lines.append("- Under the amended scoring: counted as an untaken heading, not as "
                         "lost content.")
        else:
            lines.append(f"- Under the amended scoring: found, its words stand as one run in "
                         f"merge segment(s) {', '.join(entry['found_in']['merge_segments'])}: "
                         f"{_quoted(entry['found_in']['text'])}")
        label = ("What stands in its place" if reading["class"] == "not_content"
                 else "In the merge")
        for quote in reading["quotes"]:
            lines.append(f"- {label}, `merged.md` line {quote['line']}: "
                         f"{_quoted(quote['text'])}")
        for carrier in reading["carriers"]:
            lines.append(f"- Merge segment {carrier['merge_segment']} scores "
                         f"{carrier['similarity']:.2f} against the segment; with lengths of "
                         f"{carrier['segment_chars']} and {carrier['merge_chars']} characters "
                         f"the score could not exceed {carrier['bound']:.2f} whatever the "
                         f"wording.")
        if reading["gone"]:
            lines.append(f"- What is gone: {reading['gone']}")
        if reading["note"]:
            lines.append(f"- Why: {reading['note']}")
        if reading["alternative"]:
            lines.append(f"- Borderline because: {reading['why_alternative']}.")
        second = case.get("second_reading")
        if second:
            lines.append(f"- Second reading: {_reading_words(second)}")
        lines.append("")
    twice = [case for case in audit["cases"]
             if case["group"] == COUNTED and case.get("second_reading")]
    lines += ["## The second reading's table", "",
              f"The {len(twice)} first-run cases {GROUP_WORDS[COUNTED]}, as the second "
              f"reading classed them. `L` and a number is a line of the run's `merged.md`. "
              f"The second reading of a case that is {GROUP_WORDS[REWORDED]} stands with the "
              f"case, above.", "",
              "| # | configuration | pair | segment | segment text (first 80 characters) | "
              "class | alternative | evidence |", "|---|---|---|---|---|---|---|---|"]
    ordered = sorted(twice, key=lambda case: (case["pair"], case["configuration"],
                                             case["segment"]))
    for number, case in enumerate(ordered, 1):
        second = case["second_reading"]
        lines.append(
            f"| {number} | {case['configuration']} | {case['pair']} | {case['segment']} | "
            f"{case['text'][:80].replace('|', chr(92) + '|')} | {CLASS_WORDS[second['class']]} | "
            f"{CLASS_WORDS[second['alternative']] if second['alternative'] else '-'} | "
            f"{second['evidence'].replace('|', chr(92) + '|')} |")
    return "\n".join(lines) + "\n"


def ruling_line(formed: dict) -> str:
    """Amendment 3's sentence that names who is disqualified, as it was written.

    Amendment 3 stands as written, and when it was written the audit held the
    counted segments and nothing else. So this is who has loss among those on
    a first run (`_counted_alone`); who is disqualified now is Amendment 4's
    sentence, `extension_lines`.
    """
    names = [f"`{name}`" for name in sorted(_counted_alone(formed))]
    if not names:
        return "On this lineup no row is disqualified."
    return f"On this lineup the disqualified rows are {_named(names)}."


def extension_lines(formed: dict) -> dict[str, str]:
    """The sentences Amendment 4 must carry, each by a name a refusal can say.

    Amendment 4 extends the audit to the segments on first runs that the
    similarity rule alone calls reworded and that no record names. Every
    figure in it and every row it names is one of these sentences, so that
    none of it is typed: `--check` requires each one in that amendment.
    """
    counted = formed["audit"]
    reworded = counted[REWORDED]
    block = formed["S1"]
    rows_ = block["rows"]
    per = {rid: figures["first_runs"]["cases"]
           for rid, figures in reworded["configurations"].items()
           if figures["first_runs"]["cases"]}
    others = len(rows_) - len(per)
    out = {"the audit's scope": (
        f"the {counted['first_runs']['cases']} segments the registered scoring counted as "
        f"silent loss there, and the {reworded['first_runs']['cases']} that the similarity "
        f"rule alone calls reworded and that no record names ({_counts_by_row(per)}, none on "
        f"the other {others} rows)")}
    tally, second = reworded["first_runs"], reworded["second_reading"]
    classes = (f"{tally['present']} present, {tally['not_content']} not content, "
               f"{tally['partly']} partly gone and {tally['gone']} gone")
    out["what the two readings found"] = (
        f"gave every one of the {second['cases']} the same class: {classes}"
        if second["same_class"] == second["cases"] == reworded["cases"] else
        f"gave the same class to {second['same_class']} of the {second['cases']}; the first "
        f"of them classed {classes}")
    for case in reworded["first_runs_lost"]:
        out[f"the case of loss {case['configuration']} {case['pair']} {case['segment']}"] = \
            _loss_case_words(case)
    for rid in rows_:
        words = _borderline_words(rows_[rid]["audit"])
        if words:
            out[f"that the verdict of {rid} rests on borderline cases only"] = (
                f"`{rid}` is disqualified; {words}")
    names = [f"`{name}`" for name in sorted(
        entry["row"] for entry in block["order"]["disqualified"])]
    out["the disqualified rows"] = (
        "On this lineup no row is disqualified." if not names else
        f"On this lineup the disqualified rows are now {_named(names)}.")
    ranks, shared = block["order"]["ranks"], block["order"]["shared_ranks"]
    places = []
    for rank in sorted({ranks[rid] for rid in block["order"]["survivors"]}):
        tied = [f"`{rid}`" for rid in block["order"]["survivors"] if ranks[rid] == rank]
        places.append(f"{rank}, {_named(tied)}"
                      + (", tied and not broken" if rank in shared else ""))
    out["the order"] = "The other complete rows in order: " + "; ".join(places) + "."
    two = next(p for p in formed["properties"] if p["property"] == 2)["figures"]
    eight = next(p for p in formed["properties"] if p["property"] == 8)["figures"]
    out["the unchanged counts"] = (
        f"over the {two['cells']} cells {two['silent_loss']['registered']} counted silent "
        f"losses registered and {two['silent_loss']['amended']} amended, with "
        f"{two['silent_loss']['headings_untaken']} untaken headings")
    repeats = counted["unread"]["reworded_no_record_on_repeated_runs"]
    out["what is read and unread of outcome 8"] = (
        f"Of those {eight['similarity_alone_in_the_cells']} it has now read the "
        f"{reworded['cases']} that are on a first run and have no record. The "
        f"{repeats['cases']} on repeated runs that have no record are still unread")
    return out


def second_defect_line(formed: dict) -> str:
    """The measured sentence about the defect the amendment does not address."""
    figures = formed["second_defect"]
    return (f"Measured on the sources of the nine pairs: of {figures['sentences']} "
            f"sentences, list items and table rows of at least six words, each with its "
            f"last two words cut and nothing put in their place, "
            f"{figures['last_two_words_cut_read_as_reworded']} read as reworded under the "
            f"registered rule.")


def outcome_lines(formed: dict, amended: dict, audit: dict) -> list[str]:
    """ "Outcome of the properties", as the registration's amendment must carry it.

    One line a property: whether it holds, and its figures. Generated, so
    that no figure in that section is typed; `--check` requires every line in
    `REGISTRATION.md`.
    """
    by = {p["property"]: p for p in formed["properties"]}

    def holds(number: int) -> str:
        return "Holds" if by[number]["holds"] else "FAILS"

    one = by[1]["figures"]
    firsts = one["first_runs"]
    moved = []
    for cell in amended["differences"]["cells"]:
        for entry in cell["segments"]:
            key = (cell["row"], cell["pair"], cell["draw"], entry["segment"])
            case = next((c for c in audit["cases"]
                         if _case_key(c) == key and c["group"] == COUNTED), None)
            if case and case.get("second_reading") \
                    and case["second_reading"]["class"] in LOSS_CLASSES \
                    and "silent" in entry["registered"] and "silent" not in entry["amended"]:
                moved.append(
                    f"`{key[0]}`, `{key[1]}`, segment `{key[3]}`, the {case['kind']} "
                    f"{_quoted(case['text'])}, which the second reading classed "
                    f"{CLASS_WORDS[case['second_reading']['class']]} and the first "
                    f"{CLASS_WORDS[case['first_reading']['class']]}, and which the amended "
                    f"scoring "
                    + ("finds as reworded" if "headings_untaken" not in entry["amended"]
                       else "counts as an untaken heading"
                       + (", because every segment of its section that is not in the merge "
                          "has a record" if all(member["state"] != "absent, no record"
                                                for member in entry.get("section") or [])
                          else "")))
    # Amendment 3 was written when the audit held the counted segments and
    # nothing else, and its text stays as it was written. So its lines are
    # derived from that group alone, which is what the block's own keys count.
    counted = formed["audit"]
    second = counted["second_reading"]
    second_lost = second["gone"] + second["partly"]
    lines = [
        f"1. {holds(1)}. Of the {counted['cases']} audited segments, the "
        f"{sum(one['gone'].values())} classed gone and the {sum(one['partly'].values())} "
        f"classed partly gone are still counted as silent loss "
        f"({one['gone']['silent']} and {one['partly']['silent']}). Of the "
        f"{sum(one['present'].values())} classed present, {one['present']['silent']} are "
        f"still counted and {one['present']['reworded']} are found as reworded; of the "
        f"{sum(one['not_content'].values())} classed not content, "
        f"{one['not_content']['untaken_heading']} are counted as untaken headings. On first "
        f"runs: {firsts['partly']['silent']} of {sum(firsts['partly'].values())} partly gone "
        f"still counted; of {sum(firsts['present'].values())} present, "
        f"{firsts['present']['silent']} still counted and {firsts['present']['reworded']} "
        f"found; {firsts['not_content']['untaken_heading']} of "
        f"{sum(firsts['not_content'].values())} not content counted as untaken headings. "
        f"The property names the audit, which is the first reading. Held against the second "
        f"reading of the {second['cases']} first-run cases as well, {second_lost} are gone "
        f"or partly gone there and {second_lost - len(moved)} of them are still counted"
        + ("." if not moved else "; the other: " + "; ".join(moved) + ".")]
    two = by[2]["figures"]
    lines.append(
        f"2. {holds(2)}. Over {two['merges_checked']} merges ({two['cells']} cells, the "
        f"three floors on the nine pairs and the nine reference merges) no segment is absent "
        f"under the amended rule that is not absent under the registered one, the carried "
        f"segments are the same, and no cell gains a silent loss. Counted silent losses over "
        f"the {two['cells']} cells: {two['silent_loss']['registered']} registered, "
        f"{two['silent_loss']['amended']} amended, with "
        f"{two['silent_loss']['headings_untaken']} counted as untaken headings. Runs with a "
        f"counted silent loss, repeats included: "
        f"{two['runs_with_silent_loss']['registered']} registered, "
        f"{two['runs_with_silent_loss']['amended']} amended.")
    three = by[3]["figures"]
    lines.append(f"3. {holds(3)}. {three['reference_merges']} reference merges: "
                 f"{three['silent']} silent loss and {three['headings_untaken']} untaken "
                 f"headings under both scorings.")
    four = by[4]["figures"]
    lines.append(f"4. {holds(4)}. Concatenation: {four['concatenation']['registered']} "
                 f"registered and {four['concatenation']['amended']} amended. Mechanical "
                 f"union: {four['union']['registered']} and {four['union']['amended']}. "
                 f"On all nine pairs.")
    five = by[5]["figures"]
    named = "; ".join(f"`{pair}` " + ", ".join(_quoted(text) for text in texts)
                      for pair, texts in five["headings"].items())
    lines.append(
        f"5. {holds(5)}. Base only: {five['silent_loss']['registered']} silent losses "
        f"registered, {five['silent_loss']['amended']} amended. "
        f"{five['sentences_cleared']} sentences, list items or table rows of source B are "
        f"cleared against source A alone. The {five['headings_untaken']} that leave the "
        f"count are the headings named: {named}. {five['headings_still_silent']} other "
        f"headings stay silent losses.")
    six = by[6]["figures"]
    lines.append(
        f"6. {holds(6)}. {six['cleared']} segments over the {six['merges_checked']} merges "
        f"move from absent to reworded, {six['phrase']} by step (1) and "
        f"{six['containment']} by step (2). Each was read a second time by a routine of the "
        f"figure script that is not the scorer's, which found the segment's words as one run "
        f"in the merge text named for it. `{DIFFERENCES}` shows the run for every segment "
        f"whose count differs.")
    seven = by[7]["figures"]
    moves = "; ".join(f"`{pair}` {identifier} (step {'(1)' if step == 'phrase' else '(2)'})"
                      for pair, identifier, step in seven["reference_segments_moved"])
    floors = seven["floors"]
    lines.append(
        f"7. {holds(7)}. The reference merges move "
        f"{len(seven['reference_segments_moved'])} segment between the rules: {moves}. "
        f"Concatenation and the union go from {floors['concatenation']['registered']} bloat "
        f"to {floors['concatenation']['amended']}, base only from "
        f"{floors['base_only']['registered']} lost to {floors['base_only']['amended']}. "
        f"Deviations per pair of the union: "
        f"{_rate(formed['S1_registered']['baselines']['union']['deviations_per_pair'])} "
        f"registered, {_rate(formed['floor_bands']['union']['amended_deviations_per_pair'])} "
        f"amended.")
    eight = by[8]["figures"]
    lines.append(
        f"8. {holds(8)}. In every one of the {eight['merges_checked']} merges the segments "
        f"the similarity rule calls reworded are the same under both rules. In the "
        f"{two['cells']} cells that is {eight['reworded_by_similarity']} segments, "
        f"{eight['similarity_alone_in_the_cells']} of them by the similarity rule alone "
        f"(neither step of the amended rule finds their words as a run); "
        f"`{SIMILARITY}` lists and marks them. The audit did not read them.")
    return lines


# --- catalogue.json's release-benchmark rows ---------------------------------
#
# `src/llossless/web/catalogue.json` publishes measured figures for five
# model rows and four command routes from this run: S1's headline rows for
# the five hosted models and all four of the routes (three plain, one,
# fable-sub, a side comparison, not a headline row). This is
# those rows' `derived_by`, alongside the two layers above: `catalogue_problems`
# checks the published rows against this run's own committed `figures.json`
# (never recomputed here -- `check()` above already holds that file to the
# run's cells), so a catalogue figure that drifts from what the run measured
# is caught the same way a scored cell that drifts from a raw run is.
CATALOGUE_MODELS = {
    "opus-5.5-api": "claude-opus-5-5",
    "sonnet-5-api": "claude-sonnet-5",
    "haiku-4.5-api": "claude-haiku-4-5",
    "gpt-6-sol-api": "gpt-6-sol",
    "gpt-6-luna-api": "gpt-6-luna",
}
# opus-5.5-sub joined here later (operator ruling: Opus 5 is not Opus 5.5
# and is no longer credible on the card). Until then it was deliberately
# left out: folding it into command_routes.claude-opus.measured would have
# rewritten the alias_now/measured_by_effort/pinned_by_effort history that
# route carried while its own figures were still Claude Opus 5's, from
# 2026-09-24 (see tests/subscription_figures.py's module docstring for what
# superseded it). The alias and this row's resolved_model now agree, so
# alias_now is gone (the schema forbids the two being equal) and
# measured_by_effort, Opus 5's own K=3 grid, is gone with it;
# pinned_by_effort already measured claude-opus-5-5 directly and stays.
CATALOGUE_ROUTES = {
    "sonnet-5-sub": "claude-sonnet",
    "haiku-4.5-sub": "claude-haiku",
    "opus-5.5-sub": "claude-opus",
}
# fable-sub is not a headline row: its figures live in S1's side
# comparison against opus-5.5-sub, not in S1's rows.
CATALOGUE_SIDE_ROUTES = {"fable-sub": "claude-fable"}

# The fields a catalogue measured block carries from a lineup row, verbatim.
# Model rows also carry `usd_per_merge` and `billed_upper_bound_usd_per_merge`
# (the list price, MODEL_COST_FIELDS below); a command route's calls are not
# priced per call (`validate_command_routes`), and this schema's only field
# for a route's usage in dollars, `api_equivalent_usd`, lives inside a
# multi-level effort grid this single-level run did not run -- so a route's
# real dollars-per-merge figure (this run's own `usd_per_merge` on the S1 or
# side row) is left out of the catalogue on purpose rather than forced
# into a field that does not fit it; it stays readable in this run's own
# `figures.json` and `figures.md`.
CATALOGUE_FIELDS = ("seconds_per_merge", "silent_loss", "silent_loss_per_pair",
                    "deviations", "deviations_per_pair", "pairs", "pairs_completed",
                    "silent_loss_all_completed", "deviations_all_completed",
                    "pairs_not_completed", "model_confirmed_declarations",
                    "absent_behind_rejected_declarations", "spread_draws",
                    "measured_on", "claimcheck_commit")
MODEL_COST_FIELDS = ("usd_per_merge", "billed_upper_bound_usd_per_merge")
# Since the registration's Amendment 3 the catalogue shows the amended scoring,
# which is `S1` in figures.json. So the fields above are the amended figures,
# and a measured block carries four more, each held to the same file:
# `scoring` (the rule its figures were scored under), `headings_untaken`,
# `audited_loss` (whether the audit by reading disqualifies the row; since
# Amendment 4 the audit also holds the segments reworded with no record) and
# `registered`, the four quality figures of the scoring as registered and run,
# published beside the amended ones and never in their place.
CATALOGUE_REGISTERED_FIELDS = ("silent_loss", "silent_loss_per_pair", "deviations",
                               "deviations_per_pair")


def _lineup_row(figures: dict, row_id: str, side: bool, block: str = "S1") -> dict:
    if side:
        return figures[block]["side"]["fable-sub"]["rows"][row_id]
    return figures[block]["rows"][row_id]


def catalogue_extras(figures: dict, row_id: str, side: bool) -> dict:
    """What a catalogue block says about the two scorings, from figures.json."""
    row = _lineup_row(figures, row_id, side)
    as_run = _lineup_row(figures, row_id, side, "S1_registered")
    return {"scoring": figures["scoring"]["shown_first"],
            "headings_untaken": row["headings_untaken"],
            "audited_loss": row["disqualified"],
            "registered": {key: as_run[key] for key in CATALOGUE_REGISTERED_FIELDS}}


def catalogue_note(figures: dict, row_id: str, side: bool) -> str:
    """The sentences a catalogue row's notes must carry about the two scorings.

    Generated, so that no figure of either scoring is typed into a note:
    `catalogue_problems` requires this text in the row's `notes`.
    """
    row = _lineup_row(figures, row_id, side)
    as_run = _lineup_row(figures, row_id, side, "S1_registered")
    audit = row["audit"]
    # The audit as it stands since the amendment that extended it: it reads
    # the segments counted as silent loss and the segments reworded with no
    # record, so a note says "it read", not "counted".
    reader = f"the audit by reading (extended by {AUDIT_AMENDMENT})"
    if not audit["cases"]:
        verdict = (f"not disqualified: {reader} had nothing of this row to read, because on "
                   f"its first runs no segment was counted as silent loss and none is "
                   f"reworded with no record")
    elif audit["audited_loss"]:
        words = _borderline_words(audit)
        verdict = (f"disqualified: {reader} found {audit['lost']} of the "
                   f"{audit['cases']} segments it read on this row's first runs gone or "
                   f"partly gone" + (f"; {words}" if words else ""))
    else:
        verdict = (f"not disqualified: {reader} found none of the "
                   f"{audit['cases']} segments it read on this row's first runs gone")
    if audit["readings_disagree"]:
        verdict += " (the two readings disagree)"

    def union(figure: dict) -> str:
        return (f" against a mechanical union of {figure['union_deviations']}"
                if figure.get("union_deviations") is not None else "")

    return (f"The figures are the amended scoring of the release benchmark (its Amendments "
            f"3, 2026-10-12, and 5 and 6, 2026-10-15, made after the results were known: a "
            f"new rule for finding a segment, and corrected reference merges for two pairs): "
            f"silent loss "
            f"{row['silent_loss']}, which counts source segments the program could not find "
            f"and no record explains, untaken headings {row['headings_untaken']}, deviations "
            f"{row['deviations']}{union(row)} over {row['pairs']} pair(s); {verdict}. As "
            f"registered and run: silent loss {as_run['silent_loss']}, deviations "
            f"{as_run['deviations']}{union(as_run)}, "
            + ("disqualified on that count." if as_run["silent_loss"]
               else "not disqualified."))


def catalogue_problems(data: dict, figures: dict) -> list[str]:
    """The catalogue's release-benchmark rows against this run's figures.json."""
    if "S1_registered" not in figures:
        return ["figures.json carries one scoring; the catalogue's rows are held to the "
                "amended one beside the registered one"]
    out = []
    published = {e.get("id"): e for e in data.get("models") or []}
    for row_id, model_id in CATALOGUE_MODELS.items():
        entry = published.get(model_id)
        if entry is None:
            out.append(f"catalogue.json has no model row for {model_id}")
            continue
        measured = entry.get("measured")
        if not isinstance(measured, dict):
            out.append(f"{model_id} has no measured block for the release benchmark's "
                       f"{row_id}")
            continue
        row = {**_lineup_row(figures, row_id, side=False),
               **catalogue_extras(figures, row_id, side=False)}
        for key in (*CATALOGUE_FIELDS, *MODEL_COST_FIELDS, *catalogue_extras(
                figures, row_id, side=False)):
            if measured.get(key, "absent") != row[key]:
                out.append(f"{model_id}.measured.{key}: catalogue.json says "
                           f"{json.dumps(measured.get(key, 'absent'))}, {row_id} gives "
                           f"{json.dumps(row[key])}")
        if catalogue_note(figures, row_id, side=False) not in str(entry.get("notes")):
            out.append(f"{model_id}.notes does not carry the two scorings of {row_id} as "
                       f"derived")
    published_routes = {e.get("route"): e for e in data.get("command_routes") or []}
    route_rows = ([(row_id, route_id, False) for row_id, route_id in CATALOGUE_ROUTES.items()]
                  + [(row_id, route_id, True)
                     for row_id, route_id in CATALOGUE_SIDE_ROUTES.items()])
    for row_id, route_id, side in route_rows:
        entry = published_routes.get(route_id)
        if entry is None:
            out.append(f"catalogue.json has no command route for {route_id}")
            continue
        measured = entry.get("measured")
        if not isinstance(measured, dict):
            out.append(f"{route_id} has no measured block for the release benchmark's "
                       f"{row_id}")
            continue
        if measured.get("usd_per_merge") is not None:
            out.append(f"{route_id}.measured.usd_per_merge is not null; a command "
                       f"route's calls are not priced per call")
        row = {**_lineup_row(figures, row_id, side),
               **catalogue_extras(figures, row_id, side)}
        for key in (*CATALOGUE_FIELDS, *catalogue_extras(figures, row_id, side)):
            if measured.get(key, "absent") != row[key]:
                out.append(f"{route_id}.measured.{key}: catalogue.json says "
                           f"{json.dumps(measured.get(key, 'absent'))}, {row_id} gives "
                           f"{json.dumps(row[key])}")
        if catalogue_note(figures, row_id, side) not in str(entry.get("notes")):
            out.append(f"{route_id}.notes does not carry the two scorings of {row_id} as "
                       f"derived")
        # A route's `merge_effort` has no field of that name in
        # figures.json, only the free-text `effort` REGISTRATION.md states.
        # Every route in this run was asked for the merge at medium (opus,
        # sonnet and fable state it in `effort` verbatim; haiku's own effort
        # text names its one thinking toggle instead, and carried "medium"
        # here before this run too, unchanged) -- "medium" is the one value
        # this program can hold every route's merge_effort to.
        if measured.get("merge_effort") != "medium":
            out.append(f"{route_id}.measured.merge_effort: catalogue.json says "
                       f"{json.dumps(measured.get('merge_effort'))}, this run measured "
                       f"every route's merge at medium")
    return out


def _plain(value):
    """A derived structure as it reads back from a file: JSON types only."""
    return json.loads(json.dumps(value))


def _dump(path: Path, value, ascii_only: bool = True) -> None:
    path.write_text(json.dumps(value, indent=1, ensure_ascii=ascii_only) + "\n",
                    encoding="utf-8")


def amended_problems(run_dir: Path, reg: dict, formed: dict, amended: dict,
                     audit: dict) -> list[str]:
    """Every file of the second scoring against what the stored cells derive.

    The three derived files beside `scored.json`, the cases page, the audit's
    tables in its README, and the amendment's outcome in the registration.
    A property of the amendment that does not hold is a difference too, and
    so is a sentence of the amendment that extends the audit.
    """
    found = []
    for name, part in ((AMENDED_SCORED, "scored"), (DIFFERENCES, "differences"),
                       (SIMILARITY, "similarity")):
        path = run_dir / name
        if not path.is_file():
            found.append(f"{name} is missing")
        elif load(path) != _plain(amended[part]):
            found.append(f"the stored cells no longer give {name}")
    for item in formed["properties"]:
        if not item["holds"]:
            found.append(f"property {item['property']} of {AMENDMENT} does not hold "
                         f"({item['name']}): {item.get('failures') or item['figures']}")
    pages = run_dir / AUDIT_DIR
    cases = pages / "cases.md"
    if not cases.is_file() or cases.read_text(encoding="utf-8") != render_cases(
            run_dir, audit, amended, formed):
        found.append(f"{AUDIT_DIR}/cases.md is not what audit.json and the cells render")
    readme = pages / "README.md"
    if not readme.is_file() or audit_tables(formed) not in readme.read_text(encoding="utf-8"):
        found.append(f"{AUDIT_DIR}/README.md does not carry the audit's tables as derived")
    registration = (run_dir / "REGISTRATION.md").read_text(encoding="utf-8")
    start = registration.find(f"**{AMENDMENT}")
    later = registration.find(f"**{AUDIT_AMENDMENT}")
    if start < 0:
        found.append(f"REGISTRATION.md has no {AMENDMENT}")
    else:
        # Each amendment is held to its own sentences: a line of the later
        # one must not pass for a line of the earlier one, nor the reverse.
        section = registration[start:later] if later > start else registration[start:]
        for line in outcome_lines(formed, amended, audit):
            if line not in section.splitlines():
                found.append(f"REGISTRATION.md, {AMENDMENT}, does not carry the outcome of "
                             f"property {line.split('.', 1)[0]} as derived")
        if second_defect_line(formed) not in section:
            found.append(f"REGISTRATION.md, {AMENDMENT}, does not carry the measured "
                         f"sentence about the second defect as derived")
        if ruling_line(formed) not in section:
            found.append(f"REGISTRATION.md, {AMENDMENT}, does not name the disqualified "
                         f"rows as the audit of the counted segments has them")
    if later < 0:
        found.append(f"REGISTRATION.md has no {AUDIT_AMENDMENT}")
    elif later < start:
        found.append(f"REGISTRATION.md has {AUDIT_AMENDMENT} above {AMENDMENT}")
    else:
        for name, line in extension_lines(formed).items():
            if line not in registration[later:]:
                found.append(f"REGISTRATION.md, {AUDIT_AMENDMENT}, does not carry {name} as "
                             f"derived")
    return found


def figures_problems(formed: dict, published: dict) -> list[str]:
    """figures.json against what the scored cells form: any difference, by its top key."""
    if formed == published:
        return []
    keys = sorted(k for k in set(formed) | set(published)
                  if formed.get(k) != published.get(k))
    return [f"scored.json no longer forms figures.json (differs under {keys})"]


def check(run_dir: Path) -> list[str]:
    """Both layers against the committed files. Every difference, named."""
    found = []
    now_scored = score(run_dir)
    then = load(run_dir / "scored.json")
    if len(now_scored) != len(then):
        found.append(f"the cells score to {len(now_scored)} records, scored.json holds "
                     f"{len(then)}")
    else:
        moved = [a["cell"] for a, b in zip(now_scored, then, strict=True)
                 if json.loads(json.dumps(a)) != b]
        if moved:
            found.append(f"the raw cells no longer give scored.json: {moved[:6]}")
    reg, _ = run_lineup.parse_registration(run_dir / "REGISTRATION.md")
    formed = json.loads(json.dumps((rows(reg, then))))
    amended = None
    if has_amendment(run_dir):
        try:
            amended = derive_amended(run_dir, reg, then)
        except SystemExit as refusal:
            found.append(f"the amended scoring cannot be formed: {refusal}")
    elif run_dir == EVIDENCE:
        found.append(f"the committed run has no {AUDIT_DIR}/audit.json: it is published "
                     f"under two scorings and the second one needs the audit")
    if amended is not None:
        audit = load_audit(run_dir)
        refused = audit_problems(audit, amended, first_runs_of(formed))
        found += refused
        if refused:
            # An audit that is not this run's is not formed into figures: a
            # case of a kind the summary does not know would stop it, and the
            # refusal above already says what is wrong.
            return found
        formed = _plain(with_amended(reg, then, formed, amended, audit))
        found += amended_problems(run_dir, reg, formed, amended, audit)
    published = load(run_dir / "figures.json")
    found += figures_problems(formed, published)
    if (run_dir / "figures.md").read_text(encoding="utf-8") != render(reg, published):
        found.append("figures.md is not what figures.json renders")
    if run_dir == EVIDENCE:
        # catalogue.json's rows are pinned to this specific committed
        # run, never to whatever --run-dir a caller passes.
        found += catalogue_problems(_catalogue.load(), published)
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run-dir", type=Path, default=EVIDENCE)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--score", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--texts", action="store_true",
                      help="print the generated lines REGISTRATION.md (both amendments "
                           "of 2026-10-12) and audit/README.md must carry, from the files "
                           "--write wrote")
    args = parser.parse_args(argv)
    if args.run_dir is None or not (args.run_dir / "cells.jsonl").is_file():
        print("UNMEASURED: no lineup run to derive figures from (pass --run-dir, or set "
              "EVIDENCE once the run is committed)")
        return 2
    run_dir = args.run_dir.resolve()
    reg, _ = run_lineup.parse_registration(run_dir / "REGISTRATION.md")
    if args.texts:
        if not has_amendment(run_dir):
            print("lineup_figures: this run has no audit, so no second scoring")
            return 2
        stored = load(run_dir / "figures.json")
        differing = {"differences": load(run_dir / DIFFERENCES)}
        print(f"--- REGISTRATION.md, {AMENDMENT}, outcome of the properties ---")
        print("\n".join(outcome_lines(stored, differing, load_audit(run_dir))))
        print("--- the same amendment, the second defect ---")
        print(second_defect_line(stored))
        print("--- the same amendment, who is disqualified, as it was written ---")
        print(ruling_line(stored))
        print(f"--- REGISTRATION.md, {AUDIT_AMENDMENT}, each sentence it must carry ---")
        for name, line in extension_lines(stored).items():
            print(f"[{name}] {line}")
        print(f"--- {AUDIT_DIR}/README.md ---")
        print(audit_tables(stored), end="")
        return 0
    if args.check:
        found = check(run_dir)
        for line in found:
            print(f"  DIFFERS  {line}")
        print(f"lineup_figures: {'clean' if not found else f'{len(found)} difference(s)'} -- "
              f"{run_dir}")
        return 1 if found else 0
    scored = score(run_dir)
    if args.score or args.write:
        (run_dir / "scored.json").write_text(json.dumps(scored, indent=1) + "\n",
                                             encoding="utf-8")
        print(f"wrote {run_dir / 'scored.json'}")
    formed = (rows(reg, json.loads(json.dumps(scored))))
    amended = audit = None
    if has_amendment(run_dir) and not args.score:
        audit = load_audit(run_dir)
        amended = derive_amended(run_dir, reg, _plain(scored))
        refused = audit_problems(audit, amended, first_runs_of(formed))
        if refused:
            for line in refused:
                print(f"  REFUSED  {line}")
            print(f"lineup_figures: {AUDIT_DIR}/audit.json is not the audit of this run: "
                  f"its cases must be the segments the registered scoring counted as "
                  f"silent loss and the segments on first runs that the similarity rule "
                  f"alone calls reworded and no record names; nothing amended was written")
            return 1
        formed = with_amended(reg, _plain(scored), formed, amended, audit)
    if args.write:
        (run_dir / "figures.json").write_text(json.dumps(formed, indent=1) + "\n",
                                              encoding="utf-8")
        (run_dir / "figures.md").write_text(render(reg, json.loads(json.dumps(formed))),
                                            encoding="utf-8")
        print(f"wrote {run_dir / 'figures.json'} and figures.md")
        if amended is not None:
            _dump(run_dir / AMENDED_SCORED, amended["scored"])
            _dump(run_dir / DIFFERENCES, amended["differences"], ascii_only=False)
            _dump(run_dir / SIMILARITY, amended["similarity"], ascii_only=False)
            (run_dir / AUDIT_DIR / "cases.md").write_text(
                render_cases(run_dir, audit, amended, _plain(formed)), encoding="utf-8")
            print(f"wrote {AMENDED_SCORED}, {DIFFERENCES}, {SIMILARITY} and "
                  f"{AUDIT_DIR}/cases.md")
            failing = [item for item in formed["properties"] if not item["holds"]]
            for item in failing:
                print(f"  FAILS  property {item['property']} ({item['name']}): "
                      f"{item.get('failures') or item['figures']}")
            if failing:
                return 1
        return 0
    if not args.score:
        print(render(reg, json.loads(json.dumps(formed))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
