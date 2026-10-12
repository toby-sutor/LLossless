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
from llossless import reconcile  # noqa: E402
import vendor_figures  # noqa: E402

failures: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


PAIR = "payroll_cutoff"


def under_both_rules(case):
    """Run one case of the pairs scorer under the registered rule and under the amended one.

    The scorer has no default rule, so a case has to name one, and every rule
    this section holds the scorer to is a property of the scoring and not of
    how "reworded" is told from "absent": it must hold under both. A failure
    says which rule it failed under.
    """
    def run() -> None:
        for rule in reconcile.RULES:
            before = len(failures)
            case(rule)
            failures[before:] = [f"[{rule} rule] {message}" for message in failures[before:]]
    run.__name__, run.__doc__ = case.__name__, case.__doc__
    return run


def ideal(pair: str = PAIR) -> str:
    return (rank_matrix.P / pair / "ideal.md").read_text(encoding="utf-8")


def kept_sentence(pair: str = PAIR, *, rule: str, accept=lambda item: True):
    """A sentence segment `ideal.md` keeps verbatim, and `ideal.md` without it.

    Chosen so that removing it makes that one segment absent and nothing else:
    the seeds below vary one thing (fixtures-must-vary-one-thing). `accept`
    narrows the choice for a seed that needs more of the sentence than that.
    """
    docs = rank_matrix.pair_docs(pair)
    habs, hkept, titles = rank_matrix.ideal_sets(pair, rule=rule)
    text = ideal(pair)
    flat = " ".join(text.split())
    for document in rank_matrix.sources_of(docs):
        for item in document.segments:
            if (item.kind == "sentence" and item.id in hkept and len(item.text) > 40
                    and flat.count(item.text) == 1 and accept(item)):
                pattern = r"\s+".join(re.escape(w) for w in item.text.split())
                removed, n = re.subn(pattern, "", text, count=1)
                if n == 1 and rank_matrix.sets(docs, removed, rule=rule)[0] - habs == {item.id}:
                    return item, removed
    raise AssertionError(f"{pair}: no verbatim kept sentence to remove on its own")


def declared(segment_id: str, disposition: str, grade: str, claims: list[str]) -> dict:
    return {"declarations": [{"segment": segment_id, "disposition": disposition,
                              "grade": grade, "claims": claims, "detail": ""}]}


# --- the pairs scorer ----------------------------------------------------------

@under_both_rules
def test_a_model_judged_confirmation_forgives_nothing(rule: str) -> None:
    """Must fire: confirmed by a model verdict, the loss stays lost and is
    counted apart. Must not fire: confirmed mechanically, it is forgiven."""
    target, merged = kept_sentence(rule=rule)
    base = rank_matrix.cell_figures(PAIR, ideal(), {}, rule=rule)
    by_model = rank_matrix.cell_figures(PAIR, merged, declared(target.id, "reworded",
                                                               "confirmed", ["S-004"]), rule=rule)
    by_text = rank_matrix.cell_figures(PAIR, merged, declared(target.id, "reworded",
                                                              "confirmed", []), rule=rule)
    check(by_model["lost"] == base["lost"] + 1 and by_model["model_confirmed"] == 1,
          f"a model-confirmed declaration forgave the loss: {by_model} against {base}")
    check(by_text["lost"] == base["lost"] and by_text["model_confirmed"] == 0,
          f"a mechanically confirmed declaration was not forgiven: {by_text}")
    check(by_model["silent"] == base["silent"] and by_model["decl"] == base["decl"] + 1,
          "a declared segment is not silent, whoever confirmed it")


@under_both_rules
def test_a_declared_drop_is_never_forgiven(rule: str) -> None:
    """Must fire: `dropped`, even confirmed mechanically, is lost."""
    target, merged = kept_sentence(rule=rule)
    base = rank_matrix.cell_figures(PAIR, ideal(), {}, rule=rule)
    got = rank_matrix.cell_figures(PAIR, merged, declared(target.id, "dropped",
                                                          "confirmed", []), rule=rule)
    check(got["lost"] == base["lost"] + 1 and got["model_confirmed"] == 0,
          f"a confirmed `dropped` was forgiven: {got}")


@under_both_rules
def test_a_title_is_out_of_every_axis(rule: str) -> None:
    """Must not fire: a synthesised title, undeclared, charges no axis.
    Must fire: a real sentence removed beside it is still silent and lost."""
    text = ideal()
    first = text.splitlines()[0]
    check(first.startswith("# "), "the title probe's anchor has moved")
    synthesised = "\n".join(["# A different, synthesised title"] + text.splitlines()[1:])
    base = rank_matrix.cell_figures(PAIR, text, {}, rule=rule)
    got = rank_matrix.cell_figures(PAIR, synthesised, {}, rule=rule)
    check(got == base, f"a replaced title moved a figure: {got} against {base}")
    _, merged = kept_sentence(rule=rule)
    both = rank_matrix.cell_figures(
        PAIR, "\n".join(["# A different, synthesised title"] + merged.splitlines()[1:]), {}, rule=rule)
    check(both["silent"] == base["silent"] + 1 and both["lost"] == base["lost"] + 1,
          f"a removed sentence beside a replaced title was not charged: {both}")


@under_both_rules
def test_dup_counts_exact_repeats_only(rule: str) -> None:
    """Must not fire: `ideal.md` has no exact repeat on any pair. Must
    fire: a sentence stated twice word for word is one."""
    for pair in sorted(p.name for p in rank_matrix.P.iterdir() if (p / "ideal.md").is_file()):
        got = rank_matrix.cell_figures(pair, ideal(pair), {}, rule=rule)
        check(got["dup"] == 0, f"{pair}: ideal.md scored dup {got['dup']}")
    target, _ = kept_sentence(rule=rule)
    twice = ideal() + "\n\n" + target.text + "\n"
    check(rank_matrix.cell_figures(PAIR, twice, {}, rule=rule)["dup"] == 1,
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


@under_both_rules
def test_formatting_moves_nothing(rule: str) -> None:
    """Must not fire: every pair's ideal.md wrapped at 72 columns, or with
    its numbers in bold, scores as ideal.md. Must fire: a sentence deleted
    from the wrapped, bolded ideal is still silent and lost."""
    for pair in sorted(p.name for p in rank_matrix.P.iterdir() if (p / "ideal.md").is_file()):
        base = rank_matrix.cell_figures(pair, ideal(pair), {}, rule=rule)
        for name, style in (("wrapped at 72", lambda t: hard_wrap(t, 72)),
                            ("numbers in bold", bold_numbers)):
            got = rank_matrix.cell_figures(pair, style(ideal(pair)), {}, rule=rule)
            check(got == base, f"{pair}: ideal.md {name} scored {got}, not {base}")
    _, merged = kept_sentence(rule=rule)
    base = rank_matrix.cell_figures(PAIR, ideal(), {}, rule=rule)
    got = rank_matrix.cell_figures(PAIR, bold_numbers(hard_wrap(merged, 72)), {}, rule=rule)
    check(got["silent"] == base["silent"] + 1 and got["lost"] == base["lost"] + 1,
          f"a deleted sentence was hidden by formatting: {got}")


@under_both_rules
def test_an_absence_behind_a_rejected_declaration_is_its_own_column(rule: str) -> None:
    """Must fire: absent and rejected is counted, and not as
    silent. Must not fire: absent and confirmed is not counted."""
    target, merged = kept_sentence(rule=rule)
    base = rank_matrix.cell_figures(PAIR, ideal(), {}, rule=rule)
    rejected = rank_matrix.cell_figures(PAIR, merged, declared(target.id, "reworded",
                                                               "rejected", ["S-001"]), rule=rule)
    confirmed = rank_matrix.cell_figures(PAIR, merged, declared(target.id, "reworded",
                                                                "confirmed", []), rule=rule)
    check(rejected["absent_rejected"] == 1 and rejected["silent"] == base["silent"],
          f"an absence behind a rejected declaration: {rejected}")
    check(confirmed["absent_rejected"] == 0, f"a confirmed one was counted: {confirmed}")


# --- the rule is an argument, and it is named ----------------------------------

def joined(sentence: str) -> str:
    """The sentence kept word for word and joined to a clause three times its length.

    Long enough that no similarity ratio can reach the sentence inside it
    (2m/(m+M) is 0.5 at M = 3m), so that what clears it can only be the
    amended rule's run of words.
    """
    clause = ("the control added this clause, which says nothing that either document "
              "says, so that no line of the merge is close to the sentence in length")
    tail = clause
    while len(tail) < 3 * len(sentence):
        tail += ", and " + clause
    return sentence.rstrip(".!?:;,") + "; " + tail + "."


def test_a_joined_sentence_is_a_silent_loss_under_the_registered_rule_only() -> None:
    """The two scorings differ exactly where they are meant to.

    Must not fire under the amended rule: a sentence `ideal.md` keeps, kept
    word for word and joined to a long clause, is not silent and not lost.
    Under the registered rule the same merge is one silent loss and one lost
    segment, which is the published scoring and has to stay reproducible.
    Must fire under both: the same join with the sentence's last two words
    cut is silent and lost whichever rule scores it.
    """
    def cuttable(item) -> bool:
        """At least eight words, and the last two are both content words."""
        pieces = item.text.rstrip(".!?:;,").split()
        return len(pieces) >= 8 and len(
            reconcile.content_words(reconcile.words(" ".join(pieces[-2:])))) == 2

    target, _ = kept_sentence(rule=reconcile.REGISTERED, accept=cuttable)
    words = target.text.rstrip(".!?:;,").split()
    pattern = r"\s+".join(re.escape(word) for word in target.text.split())
    whole, n = re.subn(pattern, lambda _: joined(target.text), ideal(), count=1)
    cut, m = re.subn(pattern, lambda _: joined(" ".join(words[:-2])), ideal(), count=1)
    check(n == 1 and m == 1, "the probe's sentence is no longer in ideal.md once")
    for rule, silent_whole in ((reconcile.REGISTERED, 1), (reconcile.AMENDED, 0)):
        base = rank_matrix.cell_figures(PAIR, ideal(), {}, rule=rule)
        got = rank_matrix.cell_figures(PAIR, whole, {}, rule=rule)
        check((got["silent"] - base["silent"], got["lost"] - base["lost"])
              == (silent_whole, silent_whole),
              f"[{rule} rule] a sentence kept and joined: silent and lost moved by "
              f"{got['silent'] - base['silent']} and {got['lost'] - base['lost']}, "
              f"expected {silent_whole} and {silent_whole}")
        shortened = rank_matrix.cell_figures(PAIR, cut, {}, rule=rule)
        check((shortened["silent"] - base["silent"], shortened["lost"] - base["lost"]) == (1, 1),
              f"[{rule} rule] MUST FIRE: the joined sentence with its last two words cut is "
              f"silent and lost, got {shortened} against {base}")


def test_an_untaken_heading_is_a_column_of_its_own_under_the_amended_rule() -> None:
    """Base only, source A alone, over the nine pairs: 129 registered, 121 and 8 amended.

    Must fire: the 121 are real losses and stay silent losses under the
    amended rule. Must not fire as a loss: the 8 headings of source B whose
    sections have something left in source A are counted apart, in
    `headings_untaken`, and the registered record has no such field at all, so
    a stored record of a published run is still given back field for field.
    """
    totals = {rule: {"silent": 0, "headings_untaken": 0} for rule in reconcile.RULES}
    for pair in PAIRS9:
        base_only = rank_matrix.pair_docs(pair)["source_a.md"]
        for rule in reconcile.RULES:
            got = rank_matrix.cell_figures(pair, base_only, {}, rule=rule)
            check(("headings_untaken" in got) == (rule == reconcile.AMENDED),
                  f"[{rule} rule] {pair}: the record's fields are {sorted(got)}")
            for key in totals[rule]:
                totals[rule][key] += got.get(key, 0)
    check(totals == {reconcile.REGISTERED: {"silent": 129, "headings_untaken": 0},
                     reconcile.AMENDED: {"silent": 121, "headings_untaken": 8}},
          f"base only over the nine pairs: {totals}")
    registered = rank_matrix.cell_figures(PAIR, ideal(), {}, rule=reconcile.REGISTERED)
    check(sorted(registered) == ["absent_rejected", "bloat", "decl", "dup", "lost",
                                 "model_confirmed", "near_dup", "silent"],
          f"the registered record's fields moved: {sorted(registered)}")


def test_the_counts_are_the_sizes_of_the_sets_they_are_published_from() -> None:
    """`cell_figures` is `cell_sets`, counted, under both rules.

    The list of segments that differ between the two scorings, and the
    audit's validation, read the sets; the published figures are the counts.
    Must fire: a count that is not the size of its set would let the list
    and the figure disagree in silence, so both are formed here from one
    merge and compared, and the two scorings must differ on the control that
    is built to make them differ.
    """
    def cuttable(item) -> bool:
        return len(item.text.rstrip(".!?:;,").split()) >= 8

    target, _ = kept_sentence(rule=reconcile.REGISTERED, accept=cuttable)
    pattern = r"\s+".join(re.escape(word) for word in target.text.split())
    merged, n = re.subn(pattern, lambda _: joined(target.text), ideal(), count=1)
    check(n == 1, "the probe's sentence is no longer in ideal.md once")
    seen = {}
    for rule in reconcile.RULES:
        formed = rank_matrix.cell_sets(PAIR, merged, {}, rule=rule)
        figures = rank_matrix.cell_figures(PAIR, merged, {}, rule=rule)
        for key, value in figures.items():
            size = formed[key] if isinstance(formed[key], int) else len(formed[key])
            check(size == value, f"[{rule} rule] {key}: the set has {size}, the figure "
                                 f"says {value}")
        check(set(formed["located"]) >= formed["silent"] | formed["lost"] | formed["bloat"],
              f"[{rule} rule] a counted segment is not among the located ones")
        seen[rule] = formed
    check(target.id in seen[reconcile.REGISTERED]["silent"]
          and target.id not in seen[reconcile.AMENDED]["silent"]
          and seen[reconcile.AMENDED]["located"][target.id].step in reconcile.RUN_STEPS
          and seen[reconcile.AMENDED]["located"][target.id].window_text,
          "MUST FIRE: the joined sentence is in the registered set of silent losses and "
          "not in the amended one, where it is found as a run with the text it stands in")


# Every function that scores, by the module that defines it. Each takes `rule`
# by keyword and none may default it.
SCORERS = {
    "rank_matrix": ("located_of", "sets", "ideal_sets", "cell_sets", "cell_figures",
                    "cells_of"),
    "rank_arms": ("sets", "band", "cell_figures", "collect"),
    "lineup_figures": ("baselines",),
}
# The tools that re-derive a figure published so far, and the rule each names.
# Everything published up to 2026-10-12 was scored under the registered rule.
# Two things changed on that date, both by the release benchmark's Amendment
# 3. `lineup_figures.py` still names the registered rule as `RULE`, for
# `scored.json` and the registered tables, and names the amended one beside it
# as `AMENDED_RULE`, for the second scoring it publishes. And
# `rank_scale_floor.py` scores the model picker's band under the amended rule,
# because the picker shows that benchmark's rows under the amended scoring.
PUBLISHED_UNDER = {
    "rank_matrix.py": "registered", "rank_arms.py": "registered",
    "matrix_figures.py": "registered", "vendor_figures.py": "registered",
    "subscription_figures.py": "registered", "google_figures.py": "registered",
    "phase4_figures.py": "registered", "lineup_figures.py": "registered",
    "rank_scale_floor.py": "amended",
}
# And the tools that reach the rule through `reconcile.reconcile` itself,
# whose default is the tool's own rule and not the published one.
RECONCILES_RECORDED = ("league_table.py", "measure_merges.py", "annotate_merges.py",
                       "regrade_check2.py", "run_bench.py", "rank_arms.py")


def unnamed_rule_calls(source: str, filename: str) -> list[str]:
    """Scoring calls in one program that do not pass `rule=`, as `file, line N: name`.

    A scorer function called through its module (`rank_matrix.cell_figures(`),
    or by its bare name inside the module that defines it; and, in a program
    that is not a test, `reconcile.reconcile(` and `reconcile.locate(`. A test
    may call `reconcile.reconcile` with no rule: that is the tool's default
    and testing it is the point.
    """
    import ast

    module = filename.removesuffix(".py")
    is_tool = not filename.startswith("test_")
    out = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        if isinstance(function, ast.Attribute) and isinstance(function.value, ast.Name):
            owner, name = function.value.id, function.attr
            scores = name in SCORERS.get(owner, ()) or (
                is_tool and owner == "reconcile" and name in ("reconcile", "locate"))
        elif isinstance(function, ast.Name):
            owner, name = module, function.id
            scores = name in SCORERS.get(module, ())
        else:
            continue
        if scores and not any(keyword.arg == "rule" for keyword in node.keywords):
            out.append(f"{filename}, line {node.lineno}: {owner}.{name}")
    return out


def test_the_scorer_has_no_default_rule() -> None:
    """Must fire: a scoring call that names no rule is an error, not a figure.

    A default here is how a published figure moves in silence: the tool's own
    rule changed on 2026-10-12, and a scorer that followed it would have
    re-scored every published run without one figure script changing.
    """
    import importlib
    import inspect

    for module_name, names in SCORERS.items():
        module = importlib.import_module(module_name)
        for name in names:
            parameter = inspect.signature(getattr(module, name)).parameters.get("rule")
            check(parameter is not None and parameter.kind is inspect.Parameter.KEYWORD_ONLY
                  and parameter.default is inspect.Parameter.empty,
                  f"{module_name}.{name} must take `rule` by keyword with no default; "
                  f"it has {parameter!r}")
    for call in (lambda: rank_matrix.cell_figures(PAIR, ideal(), {}),
                 lambda: rank_matrix.sets(rank_matrix.pair_docs(PAIR), ideal()),
                 lambda: rank_matrix.ideal_sets(PAIR)):
        try:
            call()
            check(False, "a scorer call without a rule returned a figure")
        except TypeError:
            pass
    try:
        rank_matrix.cell_figures(PAIR, ideal(), {}, rule="strict")
        check(False, "an unknown rule was scored")
    except ValueError:
        pass
    # The tool's own entry point does have a default, the tool's own rule, and
    # it is not the published one. That difference is why the tools below
    # must not lean on it.
    default = inspect.signature(reconcile.reconcile).parameters["rule"].default
    check(default == reconcile.AMENDED != reconcile.REGISTERED,
          f"reconcile.reconcile defaults to {default!r}")


def test_every_figure_script_names_the_rule_it_scores_with() -> None:
    """Must not fire: no program under `tests/` scores without `rule=`.
    Must fire: a seeded call without it is reported, and a seeded script
    whose `RULE` is not the published one is too."""
    import importlib

    tests = ROOT / "tests"
    unnamed = []
    scoring = set()
    own = []
    for path in sorted(tests.glob("*.py")):
        source = path.read_text(encoding="utf-8")
        found = unnamed_rule_calls(source, path.name)
        if path.name == Path(__file__).name:
            own = found
        else:
            unnamed += found
        if unnamed_rule_calls(source.replace("rule=", "ruled="), path.name):
            scoring.add(path.name)
    # This file is the one exemption, and it is pinned: the three calls
    # without a rule that `test_the_scorer_has_no_default_rule` makes in
    # order to be refused. A fourth here is a fourth to explain.
    check([entry.split(": ", 1)[1] for entry in own]
          == ["rank_matrix.cell_figures", "rank_matrix.sets", "rank_matrix.ideal_sets"],
          f"this file's own calls without a rule are {own}; exactly the three "
          f"must-fire probes are exempt")
    check(not unnamed,
          f"these calls score without naming their rule, so they follow whatever the "
          f"scorer or the tool does today: {unnamed}")
    for name in (*PUBLISHED_UNDER, *RECONCILES_RECORDED):
        check(name in scoring, f"{name} is listed as scoring and has no scoring call")
    tools = {name for name in scoring if not name.startswith("test_")}
    check(tools == set(PUBLISHED_UNDER) | set(RECONCILES_RECORDED) | {"benchmark_matrix.py"},
          f"the programs that score are {sorted(tools)}; each has to be listed here with "
          f"the rule its published figures were scored under")
    for name, rule in PUBLISHED_UNDER.items():
        module = importlib.import_module(name.removesuffix(".py"))
        check(getattr(module, "RULE", None) == rule,
              f"{name} must name its rule as `RULE = {rule!r}`; it has "
              f"{getattr(module, 'RULE', None)!r}")
        source = (tests / name).read_text(encoding="utf-8")
        check("rule=RULE" in source, f"{name} does not pass its `RULE` to the scorer")
    for name in RECONCILES_RECORDED:
        source = (tests / name).read_text(encoding="utf-8")
        check("rule=reconcile.REGISTERED" in source or "rule=rule" in source,
              f"{name} re-derives recorded figures and must name the registered rule")
    # The one program that publishes two scorings names both, and scores the
    # second with the name it gave it and never with a literal.
    lineup = importlib.import_module("lineup_figures")
    source = (tests / "lineup_figures.py").read_text(encoding="utf-8")
    check(getattr(lineup, "AMENDED_RULE", None) == reconcile.AMENDED
          and "rule=AMENDED_RULE" in source and 'rule="' not in source
          and "rule=reconcile." not in source,
          "lineup_figures.py must score its second scoring as `rule=AMENDED_RULE` and "
          "name no rule in any other way")

    seeded = ("import rank_matrix\n"
              "figures = rank_matrix.cell_figures(pair, merged, report)\n"
              "named = rank_matrix.cell_figures(pair, merged, report, rule=RULE)\n"
              "result = reconcile.reconcile(documents, merged)\n")
    check(unnamed_rule_calls(seeded, "some_figures.py")
          == ["some_figures.py, line 2: rank_matrix.cell_figures",
              "some_figures.py, line 4: reconcile.reconcile"],
          f"MUST FIRE: {unnamed_rule_calls(seeded, 'some_figures.py')}")
    check(unnamed_rule_calls(seeded, "test_something.py")
          == ["test_something.py, line 2: rank_matrix.cell_figures"],
          "a test may use the tool's default; it may not score without a rule")
    inside = "def sets(docs, text, *, rule):\n    return 1\n\nx = sets(docs, text)\n"
    check(unnamed_rule_calls(inside, "rank_matrix.py")
          == ["rank_matrix.py, line 4: rank_matrix.sets"],
          "MUST FIRE: a bare call inside the defining module")


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
