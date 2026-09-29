"""One input, every fidelity level, one report. M7 task 30.

**The report requires live inference and this module will not fake one.** One
merge per level, and a merge is a model call; there is no offline
substitute, because the thing being measured is what the model does differently
when the policy changes. The replay directory `tests/responses/` holds 130
`decompose-*` and 90 `verify-*` cassettes and **no merge cassette**, so the
sweep cannot be replayed either. `tests/responses/m7/` holds 45, all at `high`,
so a sweep replayed from there would miss on every other level.
`tests/responses/m4/` holds 66 more, and they are not a way round this
either: their schema has one property, `merged_document`, their prompt
predates the disposition model, and the cassette key is over both -- so no
merge this tool makes today can hit one. `refuse_before_running` says all of that at the point of
refusal rather than leaving the caller to infer it from an empty table.

The other half of the same rule is `incomplete`. A sweep is a comparison, and a
comparison across the levels where one of them errored is not a partial result -
it is a different and much weaker claim wearing the same table's clothes. So
nothing is written at all unless every level settled. The failure mode this
avoids is a `report.json` on disk with three rows in it, read six months later
by someone who has no reason to count them.

Which levels a sweep runs is decided per backend, before a call is made, by
`plan` (577). A level whose own refusal would fire -- `sourced`, on a backend
that cannot retrieve or cannot say whether it did -- is left out, and said to
be left out: on stderr before the first level, under the table with the
refusal's reason, and in the JSON as `left_out`. `incomplete` then counts
against the levels the plan kept, so leaving one out is never a refusal and
losing one that was planned always is.

What the report is not: a fidelity-loss *curve*. That is task 31, it needs more
than one input, and this module deliberately stops at one. A single pair's rows
are an observation, and calling one document's points a curve is the artefact
M9 §8.2 spent an appendix on.
"""

from __future__ import annotations

import textwrap

from . import config

LEVELS = config.FIDELITY_LEVELS

# The metrics a level is compared on, in the order the table prints them. Held
# as data so that adding one cannot change a row's meaning silently: every
# level is read through the same list or none is.
COLUMNS = (
    ("exit", "exit_code"),
    ("segments", "segments"),
    ("declared drops", "drops"),
    ("claims", "claims"),
    ("graded", "graded"),
    ("grounded", "grounded"),
    ("verify findings", "verify_findings"),
    ("structural", "structural_findings"),
    ("calls", "calls"),
)


def refuse_before_running(settings, fidelity_given: bool, output) -> str | None:
    """Every reason the sweep cannot produce its deliverable, checked first.

    Before anything runs, so a refusal costs no call and no half-written file.
    The counts are the plan's, because a sentence about how many merges a sweep
    makes is about this backend's sweep and not about the ladder.
    """
    levels = list(plan(settings)[0])
    if settings.mode == "dry-run":
        return ("--sweep-fidelity needs live inference and --dry-run makes no "
                "call, so there would be nothing to compare the levels on. "
                f"A dry run of a sweep is a dry run of one merge, "
                f"{len(levels)} times: use "
                "`--fidelity LEVEL --dry-run` if that is what you want.")
    if settings.mode == "replay":
        return ("--sweep-fidelity cannot be replayed: the replay directory "
                "tests/responses/ holds decompose and verify cassettes and no "
                "merge cassette, so all but one level have no recorded "
                "merge to replay and the rest would be coincidence. The 66 "
                "in tests/responses/m4/ are keyed to a pre-disposition prompt "
                "and schema and cannot be hit. Record the corpus first.")
    if fidelity_given:
        return ("--sweep-fidelity runs every level this backend can run, "
                f"{', '.join(config.fidelity_name(lv) for lv in levels)}, so "
                "--fidelity has nothing left to choose. Pass one or the other.")
    if output is not None:
        return (f"--sweep-fidelity produces one merged document per level and "
                f"-o names one path, which would leave the last level "
                f"overwriting the other {len(levels) - 1} in silence. Use "
                f"--sweep-dir DIR to keep them all, or drop -o.")
    return None


def settings_for(settings, level: str):
    """The same settings at one level, as a run at that level resolves them.

    Through `config.at_fidelity`, the step `config.resolve` takes, so a row is
    granted and refused exactly as a single run at its level would be (577).
    The fidelity is the only thing that differs between rows, except at
    `sourced`, where the automatic grant is on the command. Raises
    `ConfigError` where that level refuses this backend; `plan` is the caller
    that turns the refusal into a stated exclusion.
    """
    if level not in LEVELS:
        raise ValueError(f"unknown fidelity level {level!r}; expected one of "
                         f"{', '.join(LEVELS)}")
    return config.at_fidelity(settings, level)


def plan(settings) -> tuple[dict, dict[str, str]]:
    """The levels this backend can run, each at its settings, and why any cannot.

    Two maps, in `LEVELS` order: level to the settings its row runs with, and
    level to the refusal that keeps it out. Pure, and called before any call
    is made, so a sweep that could only ever be partial costs nothing (577).

    A refused level is left out rather than refusing the whole sweep, because
    the refusal is about that level on this backend and says nothing about the
    others: an HTTP endpoint, the common case, runs every level but `sourced`.
    Leaving it out is never silent. `cli.run_sweep` says so on stderr before the
    first level, `render` prints it under the table with this reason, and
    `as_dict` carries it as `left_out`.
    """
    runs: dict = {}
    left_out: dict[str, str] = {}
    for level in LEVELS:
        try:
            runs[level] = settings_for(settings, level)
        except config.ConfigError as exc:
            left_out[level] = str(exc)
    return runs, left_out


def row(level: str, reported: dict) -> dict:
    """One level's row, read out of the report the level already produced.

    Read from `report.as_dict` output rather than recomputed from the `Run`, so
    a row cannot disagree with the per-level report sitting beside it in the
    same file.
    """
    coverage = reported["coverage"]
    provenance = reported.get("provenance") or {}
    counts = provenance.get("counts") or {}
    return {
        "fidelity": level,
        "exit_code": reported["exit_code"],
        "settled": reported["structural"]["ran"] and not coverage["errored"],
        "errored_steps": [s["name"] for s in reported["steps"]
                          if s["state"] == "errored"],
        "segments": reported["declared_loss"]["segments"],
        "drops": reported["declared_loss"]["drops"],
        "over_budget": reported["declared_loss"]["over_budget"],
        "claims": sum(coverage["extracted"].values()),
        "graded": coverage["graded"],
        "grounded": coverage["grounded"],
        "verify_findings": len(reported["findings"]),
        "structural_findings": len(reported["structural"]["findings"]),
        "structural_kinds": sorted(f["kind"] for f in reported["structural"]["findings"]),
        "calls": counts.get("calls"),
        # Not a metric. A row-comparability guard: the structured-output tier
        # latches down when an endpoint rejects a schema, and it does not latch
        # back up, so two levels can be answered under two different decoding
        # regimes. A difference between such rows is a tier difference wearing
        # a fidelity label. `refuse_after_running` will not let it be published.
        "structured": (provenance.get("structured_output") or {}).get("mode"),
    }


def incomplete(rows: list[dict], levels) -> list[str]:
    """Which planned levels did not settle. Non-empty means write nothing at all.

    `levels` is what `plan` kept, required rather than defaulted to `LEVELS`:
    a level the plan left out is not missing, and one it kept always is.
    """
    seen = {r["fidelity"] for r in rows}
    missing = [lv for lv in levels if lv not in seen]
    failed = [r["fidelity"] for r in rows if not r["settled"]]
    return missing + [lv for lv in failed if lv not in missing]


def tiers_disagree(rows: list[dict]) -> dict[str, str]:
    """Levels answered under different structured-output tiers, if any.

    Empty when every level shares one tier, which is the only case in which a
    difference between two rows can be attributed to fidelity.
    """
    seen = {r["fidelity"]: r.get("structured") for r in rows if r.get("settled")}
    return {} if len(set(seen.values())) <= 1 else seen


def refuse_after_running(rows: list[dict], levels) -> str | None:
    """A sweep missing a planned level is a different claim, not a smaller one."""
    mixed = tiers_disagree(rows)
    if mixed:
        return ("refusing to write a sweep whose levels were not decoded alike. "
                "The structured-output tier latched down part-way through, so "
                "the rows differ by tier as well as by fidelity and nothing "
                "here can be attributed to the policy:\n"
                + "\n".join(f"  {lv}: {tier}" for lv, tier in sorted(mixed.items()))
                + "\nRe-run with --structured pinned to the lowest of these.")
    bad = incomplete(rows, levels)
    if not bad:
        return None
    detail = []
    for level in bad:
        got = next((r for r in rows if r["fidelity"] == level), None)
        if got is None:
            detail.append(f"  {level}: did not run")
        else:
            why = ", ".join(got["errored_steps"]) or "the reconciler did not run"
            detail.append(f"  {level}: {why}")
    return ("refusing to write a partial sweep. A comparison across "
            f"{len(levels)} levels with {len(bad)} missing is not a weaker "
            "version of the same result, it is a different one, and a file on "
            "disk does not carry that distinction:\n" + "\n".join(detail))


def render(rows: list[dict], left_out: dict[str, str]) -> str:
    """The comparison table. One input, so these are points and not a curve.

    `left_out` is `plan`'s second map, printed under the table with each
    refusal's own reason, so a table with a level missing says why (577).
    """
    order = {lv: i for i, lv in enumerate(LEVELS)}
    rows = sorted(rows, key=lambda r: order[r["fidelity"]])
    heads = ["fidelity"] + [label for label, _ in COLUMNS]
    table = [heads]
    for r in rows:
        # Published name in the table a person reads; `as_dict` below keeps the
        # wire spelling, because the JSON is keyed by it and recorded runs are
        # written in it (437).
        table.append([config.fidelity_name(r["fidelity"])]
                     + [str(r[key]) for _, key in COLUMNS])
    widths = [max(len(row[i]) for row in table) for i in range(len(heads))]
    counted = (f"{len(rows)} levels" if not left_out
               else f"{len(rows)} of {len(LEVELS)} levels")
    lines = [f"Fidelity sweep, one input, {counted}", ""]
    for n, cells in enumerate(table):
        lines.append("  " + "  ".join(c.ljust(w) for c, w in zip(cells, widths)).rstrip())
        if n == 0:
            lines.append("  " + "  ".join("-" * w for w in widths))
    kinds = {r["fidelity"]: r["structural_kinds"] for r in rows if r["structural_kinds"]}
    lines.append("")
    if kinds:
        for level, found in kinds.items():
            lines.append(f"  {config.fidelity_name(level)}: " + ", ".join(found))
    else:
        lines.append("  no structural finding at any level")
    for level, reason in left_out.items():
        lines.append("")
        lines += textwrap.wrap(
            f"{config.fidelity_name(level)}: left out, not run. {reason}",
            width=78, initial_indent="  ", subsequent_indent="    ")
    lines.append("")
    lines += textwrap.wrap(
        f"{len(rows)} points from one input. What each notch costs in "
        "verifiable fidelity is task 31 and needs a corpus; this is one "
        "observation.", width=78, initial_indent="  ", subsequent_indent="  ")
    return "\n".join(lines) + "\n"


def as_dict(rows: list[dict], reports: dict[str, dict], paths: dict[str, str],
            left_out: dict[str, str]) -> dict:
    """The machine-readable sweep: the comparison, and every level under it.

    `levels` is what ran, and `left_out` is every level `plan` kept out with
    the refusal that kept it out, so the file says which rows are absent and
    why rather than leaving a reader to count them (577).
    """
    order = {lv: i for i, lv in enumerate(LEVELS)}
    return {
        "sweep": "fidelity",
        "levels": [lv for lv in LEVELS if lv not in left_out],
        "left_out": {lv: left_out[lv] for lv in LEVELS if lv in left_out},
        "documents": dict(sorted(paths.items())),
        "comparison": sorted(rows, key=lambda r: order[r["fidelity"]]),
        # Whole, not summarised. The comparison above is derived from these and
        # must be checkable against them without re-running anything.
        "reports": {lv: reports[lv] for lv in LEVELS if lv in reports},
    }
