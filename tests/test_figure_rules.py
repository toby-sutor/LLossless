#!/usr/bin/env python3
"""The pairs scorer and the headline rules, each with a must-fire and a must-not-fire case. Offline.

How every pairs headline is scored and formed changed. Each rule
below is held to a seeded case that fails on the rule it replaced and a case
that must stay quiet:

- A declaration confirmed by the tested model's own verify verdicts
  forgives nothing; one confirmed mechanically still does.
- Formatting moves nothing (a hard-wrapped, bold-numbered `ideal.md`
  scores as `ideal.md`, and a sentence deleted from it is still lost); a
  declared `dropped` is never forgiven; a title is out of silent loss as well
  as lost and bloat; `dup` is exact repeats only.
- An absent segment behind a rejected declaration is counted in
  its own column, and silent loss keeps its definition.
- One figure per (model, pair), draw 1; the common-pairs rule; exit 2 as
  its own column; (model, pair, draw) unique.
- Dollars from exact values, rounded once, with the billed ledger
  beside the priced cost and never in its place; one seconds source.
- The uncached list price of a CLI envelope's tokens.
- An unmeasured fixture's plants and an errored fixture's everything are
  out of the depth block.

Run with `python3 tests/test_figure_rules.py`, or collect with pytest.
"""
from __future__ import annotations

import copy
import json
import re
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import depth_figures  # noqa: E402
import figure_rules  # noqa: E402
import fixture_semantics  # noqa: E402
import rank_matrix  # noqa: E402
import vendor_figures  # noqa: E402

failures: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


PAIR = "payroll_cutoff"


def ideal(pair: str = PAIR) -> str:
    return (rank_matrix.P / pair / "ideal.md").read_text(encoding="utf-8")


def kept_sentence(pair: str = PAIR):
    """A sentence segment `ideal.md` keeps verbatim, and `ideal.md` without it.

    Chosen so that removing it makes that one segment absent and nothing else:
    the seeds below vary one thing (fixtures-must-vary-one-thing).
    """
    docs = rank_matrix.pair_docs(pair)
    habs, hkept, titles = rank_matrix.ideal_sets(pair)
    text = ideal(pair)
    flat = " ".join(text.split())
    for document in rank_matrix.sources_of(docs):
        for item in document.segments:
            if (item.kind == "sentence" and item.id in hkept and len(item.text) > 40
                    and flat.count(item.text) == 1):
                pattern = r"\s+".join(re.escape(w) for w in item.text.split())
                removed, n = re.subn(pattern, "", text, count=1)
                if n == 1 and rank_matrix.sets(docs, removed)[0] - habs == {item.id}:
                    return item, removed
    raise AssertionError(f"{pair}: no verbatim kept sentence to remove on its own")


def declared(segment_id: str, disposition: str, grade: str, claims: list[str]) -> dict:
    return {"declarations": [{"segment": segment_id, "disposition": disposition,
                              "grade": grade, "claims": claims, "detail": ""}]}


# --- the pairs scorer ----------------------------------------------------------

def test_a_model_judged_confirmation_forgives_nothing() -> None:
    """Must fire: confirmed by a model verdict, the loss stays lost and is
    counted apart. Must not fire: confirmed mechanically, it is forgiven."""
    target, merged = kept_sentence()
    base = rank_matrix.cell_figures(PAIR, ideal(), {})
    by_model = rank_matrix.cell_figures(PAIR, merged, declared(target.id, "reworded",
                                                               "confirmed", ["S-004"]))
    by_text = rank_matrix.cell_figures(PAIR, merged, declared(target.id, "reworded",
                                                              "confirmed", []))
    check(by_model["lost"] == base["lost"] + 1 and by_model["model_confirmed"] == 1,
          f"a model-confirmed declaration forgave the loss: {by_model} against {base}")
    check(by_text["lost"] == base["lost"] and by_text["model_confirmed"] == 0,
          f"a mechanically confirmed declaration was not forgiven: {by_text}")
    check(by_model["silent"] == base["silent"] and by_model["decl"] == base["decl"] + 1,
          "a declared segment is not silent, whoever confirmed it")


def test_a_declared_drop_is_never_forgiven() -> None:
    """Must fire: `dropped`, even confirmed mechanically, is lost."""
    target, merged = kept_sentence()
    base = rank_matrix.cell_figures(PAIR, ideal(), {})
    got = rank_matrix.cell_figures(PAIR, merged, declared(target.id, "dropped",
                                                          "confirmed", []))
    check(got["lost"] == base["lost"] + 1 and got["model_confirmed"] == 0,
          f"a confirmed `dropped` was forgiven: {got}")


def test_a_title_is_out_of_every_axis() -> None:
    """Must not fire: a synthesised title, undeclared, charges no axis.
    Must fire: a real sentence removed beside it is still silent and lost."""
    text = ideal()
    first = text.splitlines()[0]
    check(first.startswith("# "), "the title probe's anchor has moved")
    synthesised = "\n".join(["# A different, synthesised title"] + text.splitlines()[1:])
    base = rank_matrix.cell_figures(PAIR, text, {})
    got = rank_matrix.cell_figures(PAIR, synthesised, {})
    check(got == base, f"a replaced title moved a figure: {got} against {base}")
    _, merged = kept_sentence()
    both = rank_matrix.cell_figures(
        PAIR, "\n".join(["# A different, synthesised title"] + merged.splitlines()[1:]), {})
    check(both["silent"] == base["silent"] + 1 and both["lost"] == base["lost"] + 1,
          f"a removed sentence beside a replaced title was not charged: {both}")


def test_dup_counts_exact_repeats_only() -> None:
    """Must not fire: `ideal.md` has no exact repeat on any pair. Must
    fire: a sentence stated twice word for word is one."""
    for pair in sorted(p.name for p in rank_matrix.P.iterdir() if (p / "ideal.md").is_file()):
        got = rank_matrix.cell_figures(pair, ideal(pair), {})
        check(got["dup"] == 0, f"{pair}: ideal.md scored dup {got['dup']}")
    target, _ = kept_sentence()
    twice = ideal() + "\n\n" + target.text + "\n"
    check(rank_matrix.cell_figures(PAIR, twice, {})["dup"] == 1,
          "a sentence stated twice word for word was not a repeat")


def hard_wrap(text: str, width: int) -> str:
    out = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith(("#", "|", "```")):
            out.append(line)
            continue
        found = re.match(r"^(\s*(?:[-*+]|\d+[.)])\s+)", line)
        prefix = found.group(1) if found else ""
        wrapped = textwrap.wrap(line[len(prefix):], width=width - len(prefix),
                                break_long_words=False, break_on_hyphens=False) or [""]
        out.append(prefix + wrapped[0])
        out += [" " * len(prefix) + w for w in wrapped[1:]]
    return "\n".join(out) + "\n"


def bold_numbers(text: str) -> str:
    return re.sub(r"(?<![\w*])(\d[\d.,:]*)(?![\w*])", r"**\1**", text)


def test_formatting_moves_nothing() -> None:
    """Must not fire: every pair's ideal.md wrapped at 72 columns, or with
    its numbers in bold, scores as ideal.md. Must fire: a sentence deleted
    from the wrapped, bolded ideal is still silent and lost."""
    for pair in sorted(p.name for p in rank_matrix.P.iterdir() if (p / "ideal.md").is_file()):
        base = rank_matrix.cell_figures(pair, ideal(pair), {})
        for name, style in (("wrapped at 72", lambda t: hard_wrap(t, 72)),
                            ("numbers in bold", bold_numbers)):
            got = rank_matrix.cell_figures(pair, style(ideal(pair)), {})
            check(got == base, f"{pair}: ideal.md {name} scored {got}, not {base}")
    _, merged = kept_sentence()
    base = rank_matrix.cell_figures(PAIR, ideal(), {})
    got = rank_matrix.cell_figures(PAIR, bold_numbers(hard_wrap(merged, 72)), {})
    check(got["silent"] == base["silent"] + 1 and got["lost"] == base["lost"] + 1,
          f"a deleted sentence was hidden by formatting: {got}")


def test_an_absence_behind_a_rejected_declaration_is_its_own_column() -> None:
    """Must fire: absent and rejected is counted, and not as
    silent. Must not fire: absent and confirmed is not counted."""
    target, merged = kept_sentence()
    base = rank_matrix.cell_figures(PAIR, ideal(), {})
    rejected = rank_matrix.cell_figures(PAIR, merged, declared(target.id, "reworded",
                                                               "rejected", ["S-001"]))
    confirmed = rank_matrix.cell_figures(PAIR, merged, declared(target.id, "reworded",
                                                                "confirmed", []))
    check(rejected["absent_rejected"] == 1 and rejected["silent"] == base["silent"],
          f"an absence behind a rejected declaration: {rejected}")
    check(confirmed["absent_rejected"] == 0, f"a confirmed one was counted: {confirmed}")


# --- the headline rules ----------------------------------------------------------

PAIRS9 = vendor_figures.PAIRS


def cell(arm: str, pair: str, draw: int, silent: int, dev: int, usd: float = 0.01,
         excluded: str = "") -> dict:
    return {"arm": arm, "pair": pair, "draw": draw, "excluded": excluded, "silent": silent,
            "lost": dev, "bloat": 0, "dup": 0, "model_confirmed": 0, "absent_rejected": 0,
            "usd": usd, "ledger_usd": usd * 3, "seconds": 60.0, "fidelity": "high",
            "started_at": "2026-10-01T00:00:00", "claimcheck_commit": "0123456789ab"}


def test_the_common_pairs_rule_and_exit_2_as_a_column() -> None:
    """Must fire, through the shipped `vendor_figures.rows`: a model that
    exits 2 on rate_limits cannot read better for it. Both headlines are over
    the eight pairs both completed."""
    sol, luna = "gpt-6-sol", "gpt-6-luna"
    cells = []
    for pair in PAIRS9:
        loss = 1 if pair == "rate_limits" else 0
        cells.append(cell(sol, pair, 1, loss, 1))
        cells.append(cell(luna, pair, 1, loss, 1,
                          excluded="exit_2" if pair == "rate_limits" else ""))
    rows = vendor_figures.rows(cells)
    a, b = rows[sol], rows[luna]
    check(a["pairs"] == b["pairs"] == 8 and a["silent_loss"] == b["silent_loss"] == 0,
          f"the headline is not over the common pairs: {a['pairs']}, {b['pairs']}")
    check(a["silent_loss_all_completed"] == 1 and a["pairs_completed"] == 9,
          f"the full row beside the headline: {a}")
    check(b["pairs_not_completed"] == ["rate_limits (exit_2)"] and a["pairs_not_completed"] == [],
          f"exit 2 must be its own column: {b.get('pairs_not_completed')}")
    whole = vendor_figures.rows([c for c in cells if c["arm"] == sol])
    check(whole[sol]["pairs"] == 9 and whole[sol]["silent_loss"] == 1,
          f"must not fire: a model alone that completed every pair is over all nine: {whole}")


def test_draws_are_never_pairs() -> None:
    """Must fire, through `vendor_figures.rows`: K = 3 on the spread pairs
    weighs each pair once; the further draws are min, median and max beside
    the headline."""
    arm = "gpt-6-sol"
    cells = [cell(arm, pair, draw, draw - 1 if pair == "rate_limits" else 0, 1)
             for pair in PAIRS9
             for draw in ((1, 2, 3) if pair in figure_rules.SPREAD_PAIRS else (1,))]
    row = vendor_figures.rows(cells)[arm]
    check(row["pairs"] == 9 and row["silent_loss"] == 0 and row["deviations"] == 9,
          f"draws were counted as pairs: {row}")
    spread = row.get("spread_draws") or {}
    check(spread.get("rate_limits", {}).get("silent_loss") == {"min": 0, "median": 1, "max": 2}
          and set(spread) == set(figure_rules.SPREAD_PAIRS),
          f"the spread draws are not reported apart: {spread}")


def test_a_duplicate_cell_is_refused() -> None:
    """Must fire: two counted cells for one (model, pair, draw). Must not
    fire: the same with one of them excluded."""
    arm = "gpt-6-sol"
    cells = [cell(arm, pair, 1, 0, 1) for pair in PAIRS9] + [cell(arm, PAIRS9[0], 1, 5, 5)]
    try:
        vendor_figures.rows(cells)
        check(False, "two counted cells for one (model, pair, draw) were accepted")
    except SystemExit:
        pass
    cells[-1]["excluded"] = "interrupted"
    check(vendor_figures.rows(cells)[arm]["silent_loss"] == 0,
          "an excluded duplicate reached the figure")


def test_money_is_exact_and_the_billed_ledger_is_not_the_headline() -> None:
    """Must fire: nine merges at $0.0049 read $0.005, not $0.000,
    and a phantom-charged ledger never becomes the headline. Must not fire:
    the exact mean of the committed vendor cells is what the rows publish."""
    check(figure_rules.per_merge([0.0049] * 9, figure_rules.USD_PLACES) == 0.005,
          "a sub-cent merge was rounded per cell before averaging")
    scored = vendor_figures.load(vendor_figures.SCORED)
    rows = vendor_figures.rows(scored)
    for arm, row in rows.items():
        cells = [c for c in scored if c["arm"] == arm and not c["excluded"]]
        exact = sum(c["usd"] for c in cells) / len(cells)
        billed = sum(c["ledger_usd"] for c in cells) / len(cells)
        check(row["usd_per_merge"] == round(exact, 3),
              f"{arm}: usd_per_merge {row['usd_per_merge']} is not the exact mean {exact}")
        check(row["billed_upper_bound_usd_per_merge"] == round(billed, 3),
              f"{arm}: the billed upper bound is not the ledger's mean")
    sol = rows["gpt-6-sol"]
    check(sol["usd_per_merge"] < sol["billed_upper_bound_usd_per_merge"],
          "Sol's phantom-charged ledger reached the headline")


def test_a_cell_is_priced_from_its_own_ledger() -> None:
    """Must not fire: a recompute that rounds to the report's own figure,
    and an exact field when the report carries one. Must fire: a report whose
    recorded cost the table no longer gives."""
    ledger = [{"model": "gpt-6-luna", "prompt_tokens": 10000, "completion_tokens": 2000}]
    exact = figure_rules.exact_usd({"provenance": {"ledger": ledger, "cost": {}}})
    check(exact is not None and exact > 0, "a priced ledger gave no figure")
    same = {"provenance": {"ledger": ledger,
                           "cost": {"state": "priced", "usd": round(exact, 4)}}}
    check(figure_rules.exact_usd(same) == exact, "the recompute disagreed with itself")
    given = {"provenance": {"ledger": ledger, "cost": {"state": "priced", "usd": 9.0,
                                                       "usd_exact": 0.123456}}}
    check(figure_rules.exact_usd(given) == 0.123456, "usd_exact was not preferred")
    moved = {"provenance": {"ledger": ledger, "cost": {"state": "priced", "usd": 9.0}}}
    try:
        figure_rules.exact_usd(moved)
        check(False, "a report the table no longer prices to was re-priced silently")
    except figure_rules.RuleBroken:
        pass
    unmeasured = [{"model": "gpt-6-luna"}]
    check(figure_rules.exact_usd({"provenance": {"ledger": unmeasured}}) is None,
          "an unmeasured call was priced")


def test_seconds_are_the_runs_own_less_its_waits() -> None:
    """One seconds source: the report's duration, less recorded waits."""
    report = {"provenance": {"duration_seconds": 100.0,
                             "ledger": [{"waited_ms": 5000}, {"latency_ms": 1}],
                             "discarded_calls": [{"latency_ms": 2000}]}}
    check(figure_rules.answer_seconds(report, harness_waits=3.0) == 90.0,
          "waits were not taken off the run's own duration")
    check(figure_rules.answer_seconds({"provenance": {"duration_seconds": 7.5}}) == 7.5,
          "a report with no waits did not read as its duration")


def test_681_fields_are_preferred_when_present() -> None:
    """A later follow-up: `answering_seconds.total` and `answering_cost`
    are preferred over the duration-minus-waits recompute and the plain
    `cost` block, but only once they carry a real figure -- an untimed
    report (a replay, a cache hit) still falls back to the run's own
    duration, and an older report with neither block behaves exactly as
    before.
    """
    # Must fire: a report that carries both new blocks reads them, not the
    # duration-minus-waits arithmetic -- built to disagree with it so a
    # regression that ignored the new fields would show as the old number.
    report = {"provenance": {
        "duration_seconds": 100.0,
        "ledger": [{"waited_ms": 5000}],
        "answering_seconds": {"total": 12.5},
        "cost": {"state": "priced", "usd": 9.0, "usd_exact": 9.0},
        "answering_cost": {"state": "priced", "usd": 0.5, "usd_exact": 0.5},
    }}
    check(figure_rules.answer_seconds(report) == 12.5,
          "answering_seconds.total was not preferred over duration minus waits")
    check(figure_rules.exact_usd(report) == 0.5,
          "answering_cost.usd_exact was not preferred over the plain cost block")

    # Must fire: answering_cost present but not priced reads as unpriced,
    # the same rule the plain cost block already follows -- no silent
    # recompute from the ledger behind an authoritative "not priced".
    unpriced = {"provenance": {
        "ledger": [{"model": "gpt-6-luna", "prompt_tokens": 10, "completion_tokens": 1}],
        "cost": {"state": "priced", "usd_exact": 0.001},
        "answering_cost": {"state": "unmeasured", "usd_exact": None},
    }}
    check(figure_rules.exact_usd(unpriced) is None,
          "an unpriced answering_cost was re-priced from the ledger instead of read as None")

    # Must not fire: an untimed report (replay, cache hit) falls back to the
    # run's own duration, and a report with neither new block behaves as it
    # always did.
    untimed = {"provenance": {
        "duration_seconds": 50.0,
        "ledger": [{"waited_ms": 1000}],
        "answering_seconds": {"total": None, "untimed_calls": 1},
    }}
    check(figure_rules.answer_seconds(untimed) == 49.0,
          "an untimed answering_seconds block was not skipped in favour of duration")
    older = {"provenance": {"duration_seconds": 7.5,
                            "ledger": [{"model": "gpt-6-luna", "prompt_tokens": 10,
                                       "completion_tokens": 1}]}}
    check(figure_rules.answer_seconds(older) == 7.5,
          "an older report without answering_seconds changed its seconds")
    check(figure_rules.exact_usd(older) is not None and figure_rules.exact_usd(older) > 0,
          "an older report without answering_cost lost its ledger-priced cost")


def test_the_uncached_list_price() -> None:
    """Cache reads and writes at the input rate, output at the output rate;
    an unpriced model gives no figure."""
    from llossless import pricing
    price = pricing.PRICES[pricing.sku_for("claude-opus-5-5")]
    usage = {"claude-opus-5-5": {"inputTokens": 10, "outputTokens": 1000,
                                 "cacheReadInputTokens": 100, "cacheCreationInputTokens": 1000}}
    want = (1110 * price.input + 1000 * price.output) / 1_000_000
    check(abs(figure_rules.uncached_list_usd(usage) - want) < 1e-12,
          f"uncached list price {figure_rules.uncached_list_usd(usage)} != {want}")
    check(figure_rules.uncached_list_usd({"no-such-model": usage["claude-opus-5-5"]}) is None,
          "an unpriced model was priced")


def test_a_dirty_stamp_is_refused() -> None:
    """Must fire: a `-dirty` commit is not cut to the pin's length and passed."""
    cells = [cell("a", p, 1, 0, 0) for p in PAIRS9]
    check(figure_rules.commit_of(cells, "a") == "0123456789ab", "a clean stamp was refused")
    cells[3]["claimcheck_commit"] = "0123456789ab-dirty"
    try:
        figure_rules.commit_of(cells, "a")
        check(False, "a -dirty stamp was accepted")
    except figure_rules.RuleBroken:
        pass


def test_the_catalogue_writer_touches_only_what_it_writes() -> None:
    """A no-op write changes no byte; a new field lands before `run`; a value
    that does not read back is refused."""
    text = (ROOT / "src" / "llossless" / "web" / "catalogue.json").read_text(encoding="utf-8")
    data = json.loads(text)
    index = figure_rules.entry_index(data, "models", "id", "gpt-6-luna")
    where = ["models", index, "measured"]
    check(figure_rules.set_field(text, where, "pairs", data["models"][index]["measured"]["pairs"])
          == text, "a no-op write changed the file")
    added = figure_rules.set_field(text, where, "probe_field", [1, 2])
    blob = json.loads(added)
    keys = list(blob["models"][index]["measured"])
    check(keys.index("probe_field") == keys.index("run") - 1
          and blob["models"][index]["measured"]["probe_field"] == [1, 2],
          "a new field did not land before `run`")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "catalogue.json"
        path.write_text(text, encoding="utf-8")
        check(not figure_rules.write_catalogue(path, [(where, "pairs", 9)]),
              "an unchanged value was reported as a change")


# --- the depth block --------------------------------------------------------

def test_an_unmeasured_plant_is_not_a_miss() -> None:
    """Must fire: a fixture taken on its sanctioned lenient reading leaves
    the plants denominator, as run_detect's own count does; an errored one
    leaves everything. Must not fire: the committed block is unchanged."""
    blob = depth_figures.committed("full")
    _, before, _ = depth_figures.depth_entry("full", copy.deepcopy(blob))
    lenient = copy.deepcopy(blob)
    for r in lenient["records"]:
        if r["fixture"] == "numeric_drift":
            plants = r["plants"]
            r.update(outcome=fixture_semantics.UNMEASURED, exit_code=0, detected=[])
            for p in r["probes"]:
                p["verdict"] = "acceptable_no_finding"
    lenient["summary"].update(plants_unmeasured=plants,
                              plants_detected=blob["summary"]["plants_detected"] - plants)
    _, after, _ = depth_figures.depth_entry("full", lenient)
    measured = lambda e: e["source_to_merged"]["plants"] + e["merged_to_sources"]["plants"]  # noqa: E731
    check(measured(after) == measured(before) - plants,
          f"an unmeasured fixture's plants stayed in the denominator: "
          f"{measured(after)} of {measured(before)}")
    errored = copy.deepcopy(blob)
    for r in errored["records"]:
        if r["fixture"] == "dedup":
            r["outcome"] = fixture_semantics.ERRORED
            gone = len(r["guard_probes"]), r["harvest"]["calls"]
    errored["summary"].update(
        guard_probes_total=blob["summary"]["guard_probes_total"] - gone[0],
        guard_wrong_total=blob["summary"]["guard_wrong_total"])
    _, cut, _ = depth_figures.depth_entry("full", errored)
    guards = lambda e: e["source_to_merged"]["guards"] + e["merged_to_sources"]["guards"]  # noqa: E731
    check(guards(cut) == guards(before) - gone[0]
          and cut["model_calls"] == before["model_calls"] - gone[1],
          "an errored fixture's guards or calls stayed in the block")


def test_figure_rules_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_figure_rules_offline" and callable(function):
            try:
                function()
            except Exception as exc:  # noqa: BLE001 - a crashing check is a failing check
                failures.append(f"{name} raised {type(exc).__name__}: {exc}")
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"figure_rules: {checks} checks pass -- the pairs scorer, the headline rules, "
          f"the cost and seconds sources and the depth block, each seeded both ways")
    return 0


if __name__ == "__main__":
    sys.exit(main())
