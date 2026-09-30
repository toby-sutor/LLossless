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

    python3 tests/lineup_figures.py --run-dir DIR            print the tables
    python3 tests/lineup_figures.py --run-dir DIR --score    write scored.json
    python3 tests/lineup_figures.py --run-dir DIR --write    write scored.json,
                                                             figures.json and
                                                             figures.md
    python3 tests/lineup_figures.py --run-dir DIR --check    re-derive both
                                                             layers; exit 1 on
                                                             any difference
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
from llossless.web import catalogue as _catalogue  # noqa: E402

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
                record.update(rank_matrix.cell_figures(cell.item, merged, report))
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


def baselines(pairs: list[str], base: str) -> dict:
    """Each floor scored by `rank_matrix.cell_figures` with no report: per pair, and summed."""
    out: dict = {}
    for pair in pairs:
        for name, text in baseline_texts(pair, base).items():
            figures = rank_matrix.cell_figures(pair, text, {})
            out.setdefault(name, {})[pair] = {"silent": figures["silent"],
                                             "deviations": figure_rules.deviations(figures)}
    return out


def _floor(per_pair: dict, pairs: list[str]) -> dict:
    silent = sum(per_pair[p]["silent"] for p in pairs)
    dev = sum(per_pair[p]["deviations"] for p in pairs)
    n = len(pairs)
    return {"pairs": n, "silent_loss": silent, "deviations": dev,
            "silent_loss_per_pair": round(silent / n, figure_rules.RATE_PLACES) if n else None,
            "deviations_per_pair": round(dev / n, figure_rules.RATE_PLACES) if n else None}


# --- the order ---------------------------------------------------------------------------

def order(rows: dict) -> dict:
    """Disqualify, then rank the complete rows, then list the incomplete ones.

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

    disqualified = sorted((rid for rid, r in rows.items() if (r["silent_loss"] or 0) > 0),
                          key=lambda rid: (rows[rid]["silent_loss_per_pair"], dev(rid), rid))
    rest = [rid for rid in rows if rid not in disqualified]
    complete = [rid for rid in rest if not rows[rid]["incomplete"] and rows[rid]["pairs"]]
    incomplete = [rid for rid in rest if rid not in complete]
    survivors, ranks, position = [], {}, 1
    for value in sorted({dev(rid) for rid in complete}):
        tie = [rid for rid in complete if dev(rid) == value]
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
    return {"survivors": survivors, "ranks": ranks, "shared_ranks": shared,
            "incomplete": [{"row": rid, "reason": rows[rid]["incomplete_text"]
                            or "nothing counted on the common pairs"} for rid in incomplete],
            "disqualified": [{"row": rid, "reason": f"silent loss {rows[rid]['silent_loss']} "
                              f"on the common pairs"} for rid in disqualified]}


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
            floors = baselines(pairs, reg["settings"]["base"])
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
            common = block.get("common_pairs") or []
            lines += [f"## {set_id}: the pairs, lowest counted draw, over the {len(common)} "
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


def _lineup_row(figures: dict, row_id: str, side: bool) -> dict:
    if side:
        return figures["S1"]["side"]["fable-sub"]["rows"][row_id]
    return figures["S1"]["rows"][row_id]


def catalogue_problems(data: dict, figures: dict) -> list[str]:
    """The catalogue's release-benchmark rows against this run's figures.json."""
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
        row = _lineup_row(figures, row_id, side=False)
        for key in (*CATALOGUE_FIELDS, *MODEL_COST_FIELDS):
            if measured.get(key, "absent") != row[key]:
                out.append(f"{model_id}.measured.{key}: catalogue.json says "
                           f"{json.dumps(measured.get(key, 'absent'))}, {row_id} gives "
                           f"{json.dumps(row[key])}")
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
        row = _lineup_row(figures, row_id, side)
        for key in CATALOGUE_FIELDS:
            if measured.get(key, "absent") != row[key]:
                out.append(f"{route_id}.measured.{key}: catalogue.json says "
                           f"{json.dumps(measured.get(key, 'absent'))}, {row_id} gives "
                           f"{json.dumps(row[key])}")
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
    published = load(run_dir / "figures.json")
    if formed != published:
        keys = sorted(k for k in set(formed) | set(published)
                      if formed.get(k) != published.get(k))
        found.append(f"scored.json no longer forms figures.json (differs under {keys})")
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
    args = parser.parse_args(argv)
    if args.run_dir is None or not (args.run_dir / "cells.jsonl").is_file():
        print("UNMEASURED: no lineup run to derive figures from (pass --run-dir, or set "
              "EVIDENCE once the run is committed)")
        return 2
    run_dir = args.run_dir.resolve()
    reg, _ = run_lineup.parse_registration(run_dir / "REGISTRATION.md")
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
    if args.write:
        (run_dir / "figures.json").write_text(json.dumps(formed, indent=1) + "\n",
                                              encoding="utf-8")
        (run_dir / "figures.md").write_text(render(reg, json.loads(json.dumps(formed))),
                                            encoding="utf-8")
        print(f"wrote {run_dir / 'figures.json'} and figures.md")
        return 0
    if not args.score:
        print(render(reg, json.loads(json.dumps(formed))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
