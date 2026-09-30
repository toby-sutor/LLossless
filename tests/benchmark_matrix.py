#!/usr/bin/env python3
"""The benchmark matrix: every measured run group, its settings, its headline
figures and the committed evidence behind it. No model call.

The question it answers is the operator's: "for the benchmarks to be
defensible do we have a detailed matrix with all the different tests we ran
across the different tests and fixtures?" Before this file the answer was no.
The runs were described in a dozen places -- `catalogue.json`, five
`*_figures.py` programs, `paper/records/`, the arm READMEs, and prose that is
not published -- and no one place said which run used which settings, which
of them left raw output in the repository, and which left nothing.

What is derived and what is declared, so nobody has to guess:

  * **Derived from committed files, every time:** each headline figure, each
    date and tool commit where a record carries one, and each row's evidence
    level. The figures come from the same functions the catalogue's own
    `--check`s use (`vendor_figures.rows`, `google_figures.rows`,
    `subscription_figures.rows`, `effort_figures.blocks`,
    `depth_figures.block`, `matrix_figures.rows`, `phase4_figures.rows`),
    from `rank_arms.collect` and `league_table.league` over the published
    runs, or straight from `paper/records/`, the arm directories'
    `graded.json`, `tests/league_table.json` and the cassettes.
    The evidence level is `git ls-files` against the paths a row names: a row
    that says its raw output is committed and whose path matches nothing is a
    failure here, not a line in a table.
  * **Declared in this file:** what no record states in one field -- the route,
    the settings a registration fixed, the status, why a row does not compare,
    and where a figure lives when it is not in the repository. Each declared
    row cites the decision-log entry it rests on.
  * **Never printed:** a figure no committed record carries. A run whose
    numbers exist only in a note or outside the repository gets "not
    derivable here" in its headline and an entry in the gap list, never a
    number typed from memory.

Usage:
    python3 tests/benchmark_matrix.py            # print the matrix
    python3 tests/benchmark_matrix.py --write    # write arms/BENCHMARK-MATRIX.md
    python3 tests/benchmark_matrix.py --check    # must-fire probes, then fail if
                                                 # the committed file differs
"""

from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
import statistics
import subprocess
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import depth_figures  # noqa: E402
import effort_figures  # noqa: E402
import opus55_effort_figures  # noqa: E402
import google_figures  # noqa: E402
import league_table  # noqa: E402
import matrix_figures  # noqa: E402
import phase4_figures  # noqa: E402
import rank_arms  # noqa: E402
import stale_corpus  # noqa: E402
import subscription_figures  # noqa: E402
import vendor_figures  # noqa: E402

OUT = ROOT / "arms" / "BENCHMARK-MATRIX.md"
CATALOGUE = ROOT / "src" / "llossless" / "web" / "catalogue.json"
RECORDS = ROOT / "paper" / "records"
AUG = ROOT / "arms" / "2026-08-30"
LEAGUE = ROOT / "tests" / "league_table.json"
CASSETTES = ROOT / "tests" / "responses"
# `run_all.UNMEASURED_EXIT`: declined, not failed, beside an `UNMEASURED:` line.
UNMEASURED_EXIT = 3

# The date the evidence was read. A constant, not today's date: the file must
# regenerate byte for byte on any later day until the evidence moves.
AS_OF = "2026-09-26"

# ---------------------------------------------------------------------------
# Vocabulary

TEST_SETS = {
    "pairs9": ("tests/pairs (9)", "the nine pairs in `tests/pairs/`, merged and "
               "scored against each pair's hand-written `ideal.md`"),
    "handref": ("hand-written reference", "the author's hand-written pairs "
                "(named `toby-test-*` when run, now in `tests/handwritten/`), "
                "scored against the author's own `reference.md`"),
    "planted": ("planted errors", "`tests/handwritten/` `voyager` (44 planted "
                "errors) and `bip39` (14), plus `mahjongg` as the "
                "false-correction control"),
    "fixtures": ("tests/fixtures (13)", "the 13-fixture detection block in "
                 "`tests/fixtures/`: seeded defects and clean guards, "
                 "`verify` run on each fixture's hand-written `merged.md`"),
    "index429": ("tests/pairs/index_429", "the one public pair "
                 "`tests/pairs/index_429`, merged and checked (the August "
                 "local-model study)"),
    "pairs2": ("tests/pairs (2, recorded)", "`index_429` and `trace_names` from "
               "`tests/pairs/`, replayed from `tests/responses/pairs/`"),
    "cassettes": ("tests/fixtures (recorded)", "the fixtures replayed from "
                  "recorded responses in `tests/responses/`"),
    "early": ("early fixtures", "the fixtures as they stood in the first "
              "week of August (8 for the cross-model sweep, 12 for the "
              "`qwen3:4b` comparison); most were later revised"),
    "probe": ("probe", "one hand-written prompt, not a test set"),
}

# The coverage grid's columns: the test sets a model can be compared on. The
# rest (a recorded pair corpus, the early fixtures, a probe)
# go in one "other" column, since a gap there is not a gap anyone would fill.
GRID = ("pairs9", "handref", "planted", "fixtures", "index429", "cassettes")
# The sets a current model is listed as never run on.
OPEN_SETS = ("pairs9", "handref", "planted", "fixtures")

STATUS = {
    "current": "the configuration a reader can pick today, measured at the date shown",
    "retired": "the model is withdrawn; the row is kept, dated, and cannot be picked",
    "superseded": "a newer model or corpus replaced it; kept as measured",
    "frozen": "part of the August-September local-model study, frozen as history",
    "best effort": "a free-tier reference with no commitment to re-run it",
    "void": "the run measured a configuration nobody would deploy and is not read as a result",
    "exploratory": "an early one-sample look, never a registered measurement",
}

EVIDENCE = {
    "raw": "the model's own output (merged documents, reports or cassettes) is committed at the path shown",
    "scores": "only scored records are committed; the raw output is not in the repository",
    "history": "the raw output was committed and later replaced; it is in git history, not at HEAD",
    "none": "nothing is committed; the figures, where any exist, are in a note or outside the repository",
}

# ---------------------------------------------------------------------------
# Rows


@dataclass
class Row:
    id: str
    section: str
    models: tuple[str, ...]
    route: str
    test_set: str
    k: str
    status: str
    refs: str
    # fidelity, verify depth, merge effort, thinking, structured tier, safe mode
    settings: tuple[str, str, str, str, str, str]
    comparable: str
    raw: tuple[str, ...] = ()
    scores: tuple[str, ...] = ()
    history: bool = False
    elsewhere: str = ""       # where the figures or output live, when not here
    gap: str = ""             # a partial gap on a row whose raw output is here
    date: str = "?"
    commit: str = "?"
    headline: str = ""
    evidence: str = ""        # computed
    extra: dict = field(default_factory=dict)


SECTIONS = {
    "P": "Merge quality on the nine pairs",
    "H": "Merge quality on the hand-written reference pairs",
    "E": "Planted errors, through a subscription at `sourced`",
    "D": "Detection and verification on the fixtures",
    "I": "The single pair `tests/pairs/index_429`",
    "C": "Recorded response corpora (`tests/responses/`)",
    "X": "Exploratory and probe measurements",
}

NOT_DERIVABLE = "not derivable here: no committed record"

API_A = "API (Anthropic)"
API_O = "API (OpenAI)"
SUB = "subscription (`claude` CLI)"
SERVERLESS = "serverless GPU (vLLM)"
POD = "rented pod (Ollama)"

PRE_503 = "full (the only depth before 2026-09-21)"
PRE_610 = "no (before 2026-09-25)"


def rows() -> list[Row]:
    """Every run group. Order is the order of the published tables."""
    vendor_sub = ("high", "full", "API default (medium)", "on, all roles",
                  "prompt, pinned", "n/a")
    sub_high = ("high", "full", "merge medium, checks low", "on, all roles",
                "prompt", PRE_610)
    matrix_0918 = ("high", PRE_503, "API default", "model default",
                   "json_schema, probed", "n/a")
    effort_grid = ("sourced", "full", "merge varied, checks low", "on, all roles",
                   "prompt", PRE_610)
    local = lambda thinking, order: ("off", PRE_503, "n/a", thinking,  # noqa: E731
                                     f"json_schema, pinned; field order {order}", "n/a")
    fixtures_27b = lambda depth: ("n/a (verify only)", depth, "n/a",  # noqa: E731
                                  "model default", "json_schema, pinned", "n/a")
    aug_detect = lambda thinking: ("n/a (verify only)", PRE_503, "n/a",  # noqa: E731
                                   thinking, "json_schema", "n/a")
    unknown = ("?", "?", "?", "?", "?", "?")

    V = "arms/2026-09-25/vendor"
    G = "arms/2026-09-25/google"
    S = "arms/2026-09-24/subscription"
    SC = "arms/2026-09-25/subscription-comparison"
    DP = "arms/2026-09-24/depth"
    OM = "arms/2026-09-26/opus-max"
    MX = "arms/2026-09-18/matrix"
    P4 = "arms/2026-09-16/phase4"
    FR = "arms/2026-09-17/frontier"
    FT = "arms/2026-09-17/frontier-thinking"
    LH = "arms/2026-09-17/ladder-high"
    GP = "arms/2026-09-18/gaps"

    out = [
        # --- P: the nine pairs ------------------------------------------------
        Row("P1", "P", ("claude-opus-5-5",), API_A, "pairs9", "1", "current", "620, 621",
            vendor_sub, "K = 1; tier `prompt` where the 2026-09-18 rows ran `json_schema` "
            "(a 2026-09-25 probe found the schema carried either way); newer commit than P6-P12",
            raw=(f"{V}/cells/*-high-claude-opus-5-5-d1/merged.md",), scores=(f"{V}/scored.json",)),
        Row("P2", "P", ("gpt-6-sol",), API_O, "pairs9", "1", "current", "619",
            vendor_sub, "K = 1; $/merge is the priced cost of the answered calls, and "
            "the billed upper bound beside it charges a timed-out call its full "
            "estimate; newer commit than P6-P12",
            raw=(f"{V}/cells/*-high-gpt-6-sol-d1/merged.md",), scores=(f"{V}/scored.json",)),
        Row("P3", "P", ("gpt-6-luna",), API_O, "pairs9", "1", "current", "619",
            vendor_sub, "K = 1; newer commit than P6-P12",
            raw=(f"{V}/cells/*-high-gpt-6-luna-d1/merged.md",), scores=(f"{V}/scored.json",)),
        Row("P4", "P", ("claude-opus-5",), API_A, "pairs9", "1", "retired", "617, 618",
            vendor_sub, "no figures: every merge was refused, so there is nothing to compare",
            raw=(f"{V}/cells/*-high-claude-opus-5-d1/stderr.log", f"{V}/diag/*"),
            scores=(f"{V}/results_claude-opus-5.json",)),
        Row("P5", "P", ("gemini-3.5-flash-lite",), "free tier (Google)", "pairs9", "1",
            "best effort", "624, 625, 630, 658",
            ("high", "full", "model default", "on, all roles", "prompt, pinned", "n/a"),
            "K = 1; 8 of 9 pairs (a per-pair figure only); free tier, paced, so seconds "
            "exclude the waits; another commit than P1-P3",
            raw=(f"{G}/cells/*-high-gemini-3.5-flash-lite-d1/merged.md",),
            scores=(f"{G}/scored.json",)),
        Row("P6", "P", ("claude-haiku-4-5",), SUB + ", alias `haiku`", "pairs9", "1",
            "current", "597, 610, 616",
            sub_high, "K = 1, no temperature or seed; before safe mode (2026-09-25): the CLI "
            "loaded the author's own instructions and offered its full tool set",
            raw=(f"{S}/*-high-claude-haiku/merged.md",), scores=(f"{S}/scored.json",)),
        Row("P7", "P", ("claude-sonnet-5",), SUB + ", alias `sonnet`", "pairs9", "1",
            "current", "597, 610, 616",
            sub_high, "as P6",
            raw=(f"{S}/*-high-claude-sonnet/merged.md",), scores=(f"{S}/scored.json",)),
        Row("P8", "P", ("claude-opus-5",), SUB + ", alias `opus`", "pairs9", "1",
            "superseded", "597, 609, 610, 616",
            sub_high, "as P6; the alias answered as `claude-opus-5`, the model P4 "
            "retired, so the row describes an older model than the alias serves now",
            raw=(f"{S}/*-high-claude-opus/merged.md",), scores=(f"{S}/scored.json",)),
        Row("P9", "P", ("claude-opus-5",), API_A, "pairs9", "1", "retired", "618, 619",
            matrix_0918, "tier `json_schema` against the 2026-09-25 rows' `prompt`; "
            "before the merge-prompt paragraph of 2026-09-19 that later made this model refuse",
            raw=(f"{MX}/*-high-claude-opus-5/merged.md",),
            scores=(f"{MX}/scored.json", f"{MX}/results_anthropic.json")),
        Row("P10", "P", ("claude-sonnet-5",), API_A, "pairs9", "1", "current", "619, 621",
            matrix_0918, "as P9",
            raw=(f"{MX}/*-high-claude-sonnet-5/merged.md",),
            scores=(f"{MX}/scored.json", f"{MX}/results_anthropic.json")),
        Row("P11", "P", ("claude-haiku-4-5",), API_A, "pairs9", "1", "current", "619, 621",
            matrix_0918, "as P9",
            raw=(f"{MX}/*-high-claude-haiku-4-5/merged.md",),
            scores=(f"{MX}/scored.json", f"{MX}/results_anthropic.json")),
        Row("P12", "P", ("gpt-5.6-terra",), API_O, "pairs9", "1", "superseded", "619",
            ("high", PRE_503, "API default", "model default", "prompt, pinned", "n/a"),
            "superseded by GPT-6 Sol and Luna (P2, P3)",
            raw=(f"{MX}/*-high-gpt-5.6-terra/merged.md",),
            scores=(f"{MX}/scored.json", f"{MX}/results_openai.json")),

        # --- H: hand-written reference pairs -------------------------------
        Row("H1", "H", ("qwen3:8b",), SERVERLESS, "handref", "1", "superseded", "427, 442",
            ("low and high", PRE_503, "n/a", "?", "?", "n/a"),
            "3 pairs, not the nine; the catalogue figure is at `high` over 2 completed "
            "pairs, scored as H6-H9 (`rank_arms.cell_figures`); the league figure is over "
            "all 6 runs",
            raw=(f"{P4}/*-8b/merged.md",),
            scores=(f"{P4}/scored.json", "tests/league_table.json")),
        Row("H2", "H", ("Qwen/Qwen3.8-27B-FP8",), SERVERLESS, "handref", "1", "current",
            "427, 442",
            ("low and high", PRE_503, "n/a", "?", "?", "n/a"),
            "as H1, 3 completed pairs at `high`",
            raw=(f"{P4}/*-27b-fp8/merged.md",),
            scores=(f"{P4}/scored.json", "tests/league_table.json")),
        Row("H3", "H", ("claude-haiku-4-5",), API_A, "handref", "1", "superseded",
            "441, 442",
            ("low and high", PRE_503, "API default", "on, all roles",
             "json_schema, pinned", "n/a"),
            "tier pinned to the thinking-off comparator's rung; superseded by "
            "the 2026-09-18 rows",
            raw=(f"{FT}/*-claude-haiku-4-5/merged.md",),
            scores=(f"{FT}/results.json", "tests/league_table.json")),
        Row("H4", "H", ("gpt-5.6-terra",), API_O, "handref", "1", "superseded", "441, 442",
            ("low and high", PRE_503, "API default", "on, all roles", "prompt, pinned", "n/a"),
            "as H3",
            raw=(f"{FT}/*-gpt-5.6-terra/merged.md",),
            scores=(f"{FT}/results.json", "tests/league_table.json")),
        Row("H5", "H", ("claude-sonnet-5", "gpt-5.6-terra", "claude-haiku-4-5"),
            "API (Anthropic, OpenAI)",
            "handref", "1", "void", "440",
            ("low and high", PRE_503, "none sent", "suppressed", "?", "n/a"),
            "void: every model was told not to reason; stopped at 13 of 24 arms",
            raw=(f"{FR}/*/report.json", f"{FR}/*/stderr.txt"),
            scores=(f"{FR}/results.json",)),
        Row("H6", "H", ("claude-opus-5",), API_A, "handref", "1", "retired", "444",
            ("high", PRE_503, "API default", "model default", "json_schema", "n/a"),
            "4 pairs; a different corpus and reference than P9-P12",
            raw=(f"{LH}/*-high-claude-opus-5/merged.md",), scores=(f"{LH}/results.json",)),
        Row("H7", "H", ("claude-sonnet-5",), API_A, "handref", "1", "superseded", "444",
            ("high", PRE_503, "API default", "model default", "json_schema", "n/a"),
            "as H6",
            raw=(f"{LH}/*-high-claude-sonnet-5/merged.md",), scores=(f"{LH}/results.json",)),
        Row("H8", "H", ("claude-haiku-4-5",), API_A, "handref", "1", "superseded", "444",
            ("high", PRE_503, "API default", "model default", "json_schema", "n/a"),
            "as H6; 3 pairs; the three cells are H3's `high` cells",
            raw=(f"{FT}/*-high-claude-haiku-4-5/merged.md",), scores=(f"{FT}/results.json",)),
        Row("H9", "H", ("gpt-5.6-terra",), API_O, "handref", "1", "superseded", "444",
            ("high", PRE_503, "API default", "model default", "prompt", "n/a"),
            "as H6; three of the four cells are H4's `high` cells",
            raw=(f"{FT}/*-high-gpt-5.6-terra/merged.md", f"{GP}/*-high-gpt-5.6-terra/merged.md"),
            scores=(f"{FT}/results.json", f"{GP}/results.json")),

        # --- E: planted errors ------------------------------------------------
        Row("E1", "E", ("claude-opus-5",), SUB + ", alias `opus`", "planted", "3 per level",
            "superseded", "594, 600, 609, 610, 616",
            effort_grid, "before safe mode (2026-09-25); the alias answered as `claude-opus-5`, "
            "since retired; draws at one effort level overlap, so only non-overlapping "
            "ranges separate",
            raw=(f"{SC}/runs/*/*-opus-*/*/merged.md",),
            scores=(f"{SC}/scored.json", f"{SC}/tables.md"),
            gap="the pipeline that ran the published scorer (`score_planted.py`) over "
            "each draw, `score_grid.py`, is withheld with its per-error outcome text, "
            "so the voyager and bip39 outcomes in `scored.json` are taken as "
            "given and cannot be re-derived from the runs; the mahjongg control is "
            "rescored from the runs by `tests/mahjongg_figures.py --check`"),
        Row("E2", "E", ("claude-sonnet-5",), SUB + ", alias `sonnet`", "planted",
            "3 per level", "current", "594, 600, 609, 610, 616",
            effort_grid, "as E1",
            raw=(f"{SC}/runs/*/*-sonnet-*/*/merged.md",),
            scores=(f"{SC}/scored.json", f"{SC}/tables.md"), gap="as E1"),
        Row("E3", "E", ("claude-haiku-4-5",), SUB + ", alias `haiku`", "planted",
            "3", "current", "609, 610, 616",
            effort_grid, "as E1; `medium` only, the registered lower anchor; no mahjongg",
            raw=(f"{SC}/runs/*/*-haiku-*/*/merged.md",),
            scores=(f"{SC}/scored.json", f"{SC}/tables.md"), gap="as E1"),
        Row("E4", "E", ("claude-opus-5", "claude-sonnet-5"), SUB, "planted", "18 runs, mixed",
            "superseded", "562, 563, 594",
            ("sourced", "full and coverage", "low to xhigh, mixed", "mixed", "?", PRE_610),
            "mixed settings, some unrecorded; scored against a typed 22-error key, "
            "re-scored on 2026-09-24 against a key derived by diff",
            elsewhere="the 18 stored runs are outside the repository"),

        Row("E5", "E", ("claude-opus-5-5",), SUB + ", pinned `--model claude-opus-5-5`",
            "planted", "2 at xhigh, 3 at max", "current", "661",
            ("sourced", "full", "merge xhigh and max, checks low", "on, all roles",
             "prompt", "yes"),
            "voyager only; Claude Code 2.1.281, since 2.1.274 refuses the model; "
            "the mahjongg control ran once at max and is not in the headline; "
            "not comparable with E1 (another model, before safe mode)",
            raw=(f"{OM}/runs/*/*/*/merged.md",),
            scores=(f"{OM}/scored.json", f"{OM}/tables.md"),
            gap="the pipeline that ran the published scorer (`score_planted.py`) over "
            "each run, `score_max.py`, is withheld with its per-error outcome text, "
            "so the voyager outcomes in `scored.json` are taken as given and "
            "cannot be re-derived from the runs; the mahjongg control is rescored from "
            "its run by `tests/mahjongg_figures.py --check`"),

        # --- D: fixtures ------------------------------------------------------
        Row("D1", "D", ("Qwen/Qwen3.8-27B-FP8",), SERVERLESS, "fixtures", "1", "current",
            "569, 582, 585", fixtures_27b("full"),
            "K = 1 (every 2026-09-22 figure was identical over K = 3); scored under the "
            "2026-09-24 rule on a plant reported twice, the as-run scoring kept beside it",
            raw=(f"{DP}/r1/full-reports/*.json",),
            scores=(f"{DP}/regraded/full.json", f"{DP}/r1/full")),
        Row("D2", "D", ("Qwen/Qwen3.8-27B-FP8",), SERVERLESS, "fixtures", "1", "current",
            "569, 582, 585", fixtures_27b("coverage"),
            "as D1; `coverage` has no reverse pass, so the hallucination plant is "
            "outside it by construction and left out of its rate",
            raw=(f"{DP}/r1/coverage-reports/*.json",),
            scores=(f"{DP}/regraded/coverage.json", f"{DP}/r1/coverage")),
        Row("D3", "D", ("Qwen/Qwen3.8-27B-FP8",), SERVERLESS, "fixtures", "3", "superseded",
            "547, 585", fixtures_27b("full"),
            "before the mechanical attribution check of 2026-09-24; superseded by D1",
            elsewhere="the 2026-09-22 registration and draws are outside the repository"),
        Row("D4", "D", ("Qwen/Qwen3.8-27B-FP8",), SERVERLESS, "fixtures", "3", "superseded",
            "547, 585", fixtures_27b("coverage"),
            "as D3; superseded by D2", elsewhere="as D3"),
        Row("D5", "D", ("claude-haiku-4-5",), SUB, "fixtures", "?", "superseded", "547",
            ("n/a (verify only)", "?", "?", "?", "prompt", PRE_610),
            "one fixture (`attribution_invented`) only, run to tell a harness miss "
            "from a model miss",
            elsewhere="figures not published",
            extra={"coverage": "1 fixture"}),
        Row("D6", "D", ("qwen3.8:27b",), POD, "fixtures", "1", "frozen", "112, 223",
            aug_detect("merge only"), "scored against fixtures two of which were "
            "later repaired on 2026-09-03; regraded figures beside the as-run ones",
            scores=("paper/records/half1-A-27b.json", "paper/records/regrade-detect.json"),
            elsewhere="the 2026-08-29 per-fixture reports are not committed"),
        Row("D7", "D", ("deepseek-r1:70b",), POD, "fixtures", "1", "frozen", "112, 223",
            aug_detect("all roles"), "as D6",
            scores=("paper/records/half1-B-70b.json", "paper/records/regrade-detect.json"),
            elsewhere="as D6"),
        Row("D8", "D", ("gpt-oss:120b",), POD, "fixtures", "1", "frozen", "112, 223",
            aug_detect("all roles"), "as D6",
            scores=("paper/records/half1-C-120b.json", "paper/records/regrade-detect.json"),
            elsewhere="as D6"),
        Row("D9", "D", ("qwen3.8:27b",), POD, "fixtures", "1", "frozen", "112",
            aug_detect("merge only"), "forward probes graded against SUPPORTED alone",
            scores=("paper/records/half2-A-27b.json",),
            elsewhere="the 2026-08-29 per-fixture reports are not committed"),
        Row("D10", "D", ("deepseek-r1:70b",), POD, "fixtures", "1", "frozen", "112",
            aug_detect("all roles"), "as D9",
            scores=("paper/records/half2-B-70b.json",), elsewhere="as D9"),
        Row("D11", "D", ("gpt-oss:120b",), POD, "fixtures", "1", "frozen", "112",
            aug_detect("all roles"), "as D9",
            scores=("paper/records/half2-C-120b.json",), elsewhere="as D9"),
        Row("D12", "D", ("qwen3.8:27b",), POD, "fixtures", "1", "frozen", "223, 241",
            aug_detect("merge only"), "scored by regrade-inventions: an invented "
            "finding disqualifies on every fixture",
            raw=("arms/2026-09-03/A-27b/detect-reports/*.json",),
            scores=("paper/records/detect-2026-09-03-A-27b.json",
                    "paper/records/regrade-inventions.json")),
        Row("D13", "D", ("deepseek-r1:70b",), POD, "fixtures", "1", "frozen", "223, 241",
            aug_detect("all roles"), "as D12",
            raw=("arms/2026-09-03/B-70b/detect-reports/*.json",),
            scores=("paper/records/detect-2026-09-03-B-70b.json",
                    "paper/records/regrade-inventions.json")),
        Row("D14", "D", ("gpt-oss:120b",), POD, "fixtures", "1", "frozen", "223, 241, 547",
            aug_detect("all roles"), "as D12",
            raw=("arms/2026-09-03/C-120b/detect-reports/*.json",),
            scores=("paper/records/detect-2026-09-03-C-120b.json",
                    "paper/records/regrade-inventions.json")),

        # --- I: index_429 ----------------------------------------------------
        Row("I1", "I", ("qwen3.8:27b",), POD, "index429", "1", "frozen", "149, 151",
            local("merge only", "schema"), "temperature 0, seed 0; one public pair",
            raw=("arms/2026-08-30/2c/A1-27b-default/merged.md",),
            scores=("arms/2026-08-30/2c/graded.json",), extra={"dir": "2c", "arm": "A1-27b-default"}),
        Row("I2", "I", ("deepseek-r1:70b",), POD, "index429", "1", "frozen", "149, 151",
            local("merge only (reasons anyway)", "any"), "as I1",
            raw=("arms/2026-08-30/2c/B1-70b-default/merged.md",),
            scores=("arms/2026-08-30/2c/graded.json",), extra={"dir": "2c", "arm": "B1-70b-default"}),
        Row("I3", "I", ("gpt-oss:120b",), POD, "index429", "1", "frozen", "149, 151, 153",
            local("all roles", "schema"), "as I1; one draw of a model that does not "
            "repeat at temperature 0; I5 found it was the minority draw",
            raw=("arms/2026-08-30/2c/C2-120b-think/merged.md",),
            scores=("arms/2026-08-30/2c/graded.json",), extra={"dir": "2c", "arm": "C2-120b-think"}),
        Row("I4", "I", ("qwen3.8:27b",), POD, "index429", "3", "frozen", "156, 159",
            local("merge only", "schema"), "as I1",
            raw=("arms/2026-08-30/k3/A1-27b-default-d*/merged.md",),
            scores=("arms/2026-08-30/k3/graded.json", "paper/records/regrade-pair429.json"),
            extra={"dir": "k3", "arm": "A1-27b-default"}),
        Row("I5", "I", ("gpt-oss:120b",), POD, "index429", "5", "frozen", "152, 153",
            local("all roles", "schema"), "as I1; registered at K = 5 because the model "
            "does not repeat at temperature 0",
            scores=("paper/records/bench-k5replication.json",),
            elsewhere="the five draws' merged documents and reports are not committed; "
            "the record keeps each draw's sha256 and figures"),
        Row("I6", "I", ("qwen3.8:27b",), POD, "index429", "3", "frozen", "156, 159",
            local("all roles", "schema"), "as I1",
            raw=("arms/2026-08-30/k3/A2-27b-think-d*/merged.md",),
            scores=("arms/2026-08-30/k3/graded.json", "paper/records/regrade-pair429.json"),
            extra={"dir": "k3", "arm": "A2-27b-think"}),
        Row("I7", "I", ("deepseek-r1:70b",), POD, "index429", "3", "frozen", "156, 159",
            local("merge only (reasons anyway)", "any"), "as I1",
            raw=("arms/2026-08-30/k3/B1-70b-default-d*/merged.md",),
            scores=("arms/2026-08-30/k3/graded.json", "paper/records/regrade-pair429.json"),
            extra={"dir": "k3", "arm": "B1-70b-default"}),
        Row("I8", "I", ("deepseek-r1:70b",), POD, "index429", "3", "frozen", "156, 159, 341",
            local("all roles", "any"), "as I1; the flag is inert on this model, so I7 "
            "and I8 are one condition measured twice",
            raw=("arms/2026-08-30/k3/B2-70b-think-d*/merged.md",),
            scores=("arms/2026-08-30/k3/graded.json", "paper/records/regrade-pair429.json"),
            extra={"dir": "k3", "arm": "B2-70b-think"}),
        Row("I9", "I", ("gpt-oss:120b",), POD, "index429", "5", "frozen", "160, 163, 185, 197",
            local("merge only", "schema"), "no figures: no draw produced a report",
            raw=("arms/2026-08-30/k5c/C1-120b-default-d*/stderr.log",),
            scores=("arms/2026-08-30/k5c/graded.json",),
            extra={"dir": "k5c", "arm": "C1-120b-default"}),
        Row("I10", "I", ("gpt-oss:120b",), POD, "index429", "5", "frozen", "160, 163",
            local("all roles", "schema"), "as I1",
            raw=("arms/2026-08-30/k5c/C2-120b-think-d*/merged.md",),
            scores=("arms/2026-08-30/k5c/graded.json", "paper/records/sweep-pair429.json"),
            gap="`paper/records/sweep-pair429.json` records `merged_bytes` 5690 for this "
            "arm; every committed draw is 5692 bytes and no committed file is 5690 "
            "(`arms/README.md`)",
            extra={"dir": "k5c", "arm": "C2-120b-think"}),
        Row("I11", "I", ("claude-haiku-4-5",), API_A, "index429", "6", "frozen", "181, 192, 199",
            ("high", PRE_503, "?", "off and on", "json_schema", "n/a"),
            "5 of 6 draws failed the schema; the comparison built on them was "
            "retracted and the outputs are excluded from the paper",
            elsewhere="the failed attempts sat in a local cache; nothing is committed"),
        Row("I12", "I", ("claude-sonnet-5", "claude-haiku-4-5"), API_A, "index429",
            "1, then 3", "superseded", "446, 447",
            ("high", PRE_503, "API default", "model default", "?", "n/a"),
            "one question (are the `{internal-notes}` markers kept) before and after "
            "a prompt change; a finding about the prompt, not a model ranking",
            elsewhere="figures not published"),

        # --- C: cassette corpora --------------------------------------------
        Row("C1", "C", ("Qwen/Qwen3.8-27B-FP8",), SERVERLESS, "cassettes", "3 samples",
            "current; 1 request unrecordable", "583, 587-589, 608",
            ("?", "full", "n/a", "off, all roles", "json_schema, pinned", "n/a"),
            "replaces the `qwen3:8b` corpus; not comparable with it (model, prompts "
            "and two fixtures changed)",
            raw=("tests/responses/decompose-*.json", "tests/responses/verify-*.json",
                 "tests/responses/m7/*.json"),
            gap="one request, `attribution_invented`'s reverse verify call, ran away "
            "in 7 of 8 attempts and has no cassette; replays report its two probes "
            "UNMEASURED"),
        Row("C2", "C", ("qwen3:8b",), "local card (Ollama)", "cassettes", "3 samples",
            "superseded", "M4",
            ("?", PRE_503, "n/a", "?", "json_schema", "n/a"),
            "kept for its latency record; nothing replays it",
            raw=("tests/responses/m4/*.json",)),
        Row("C3", "C", ("qwen3:8b",), POD, "pairs2", "3 samples", "superseded", "150",
            ("?", PRE_503, "n/a", "off", "json_schema", "n/a"),
            "the public pairs' recordings, re-recorded under an endpoint label",
            raw=("tests/responses/pairs/*.json",)),
        Row("C4", "C", ("qwen3:8b",), "local card and pod (Ollama)", "cassettes",
            "3 samples", "superseded", "608",
            ("?", PRE_503, "n/a", "off and on", "json_schema", "n/a"),
            "the reference corpus before 2026-09-25; 528 cassettes deleted then on purpose",
            history=True,
            elsewhere="in git history before the 2026-09-25 replacement, replayable from the commit "
            "that recorded it; not at HEAD"),

        # --- X: exploratory, probe -------------------------------------------
        *[Row(f"X{i}", "X", (m,), route, "early", "1", "exploratory", "M3 addendum",
              ("n/a (verify only)", PRE_503, "n/a", "?", "probed", "n/a"),
              "one sample per model, 8 fixtures that were revised afterwards, prompts "
              "that match neither the committed corpus nor today's" if i == 1 else "as X1",
              elsewhere="cassettes gitignored under `tests/eval/`; figures "
              "not published" if i == 1 else "as X1")
          for i, (m, route) in enumerate((
              ("gpt-5-1", "hosted gateway (OpenAI-compatible)"),
              ("claude-sonnet-4-5", "hosted gateway (OpenAI-compatible)"),
              ("claude-opus-5", "hosted gateway (OpenAI-compatible)"),
              ("kimi-k2", "hosted gateway (OpenAI-compatible)"),
              ("kimi-k3", "hosted gateway (OpenAI-compatible)"),
              ("qwen3:8b", "local card (Ollama)")), start=1)],
        Row("X7", "X", ("qwen3:4b",), "local card (Ollama)", "early", "3 samples",
            "exploratory", "M3",
            ("n/a", PRE_503, "n/a", "off", "probed", "n/a"),
            "12 fixtures of 2026-08-08; unusable on decompose (returned the prompt's "
            "example)",
            elsewhere="cassettes gitignored under `tests/eval/`; figures "
            "not published"),
        Row("X8", "X", ("qwen3:8b",), "local card (Ollama)", "early", "3 samples",
            "superseded", "M3",
            ("n/a", PRE_503, "n/a", "off", "probed", "n/a"),
            "the comparator of X7",
            history=True,
            elsewhere="the corpus committed at `af36c70`, since re-recorded; in git "
            "history, not at HEAD"),
        Row("X9", "X", ("gpt-oss:20b",), "local card (Ollama)", "probe", "1 per shape",
            "exploratory", "345, 346",
            ("n/a", "n/a", "n/a", "off and on", "none, then json_schema", "n/a"),
            "an advisory probe, run at a 4,096-token window where the registration "
            "said 40,960",
            elsewhere="figures not published"),
    ]
    return out


# ---------------------------------------------------------------------------
# Loading


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True,
                         check=True).stdout.decode("utf-8")
    return [p for p in out.split("\0") if p]


def span(values: list) -> str:
    """Median (min-max), whole numbers where the values are whole."""
    med = statistics.median(values)
    med = int(med) if float(med).is_integer() else med
    return f"{med} ({min(values)}-{max(values)})"


def pairs_headline(m: dict) -> str:
    """One pairs row's headline. A row `figure_rules` formed also names the
    columns that never enter it; a hand-written-pair row (`rank_arms`)
    carries none of them."""
    usd = m.get("usd_per_merge")
    cost = f"${usd:.3f}/merge" if usd is not None else "no $ figure"
    billed = m.get("billed_upper_bound_usd_per_merge")
    if billed is not None:
        cost += f" (billed upper bound ${billed:.3f})"
    missing = m.get("pairs_not_completed") or []
    text = (f"silent loss {m['silent_loss']} ({m['silent_loss_per_pair']:.2f}/pair); "
            f"deviations {m['deviations']} ({m['deviations_per_pair']:.2f}/pair); "
            f"{m['pairs']} pairs"
            + (f" (not completed: {', '.join(missing)})" if missing else "")
            + f"; {cost}; {m['seconds_per_merge']:.0f} s/merge")
    if "model_confirmed_declarations" in m:
        text += (f"; beside it: {m['model_confirmed_declarations']} lost segments the "
                 f"model's own verifier confirmed as declared, "
                 f"{m['absent_behind_rejected_declarations']} absent behind a rejected "
                 f"declaration")
    return text


def headline_pairs(rs: dict[str, Row]) -> None:
    vendor = vendor_figures.rows(vendor_figures.load(vendor_figures.SCORED))
    for rid, model in (("P1", "claude-opus-5-5"), ("P2", "gpt-6-sol"), ("P3", "gpt-6-luna")):
        m = vendor[model]
        rs[rid].headline = pairs_headline(m)
        rs[rid].date, rs[rid].commit = m["measured_on"], m["claimcheck_commit"][:7]
    refused = [r for r in vendor_figures.load(vendor_figures.SCORED)
               if r["arm"] == "claude-opus-5"]
    exits = sorted({r["exit_code"] for r in refused})
    rs["P4"].headline = (f"{len(refused)} of {len(refused)} attempted cells refused "
                         f"(exit {', '.join(map(str, exits))}); no report, no figure")
    rs["P4"].date = one_value({r["started_at"][:10] for r in refused}, "P4 date")
    # A refused cell writes no report, so its record carries no commit; the
    # run's pinned clone does (`COMMIT`, written before the first call).
    rs["P4"].commit = (vendor_figures.EVIDENCE / "COMMIT").read_text(encoding="utf-8").strip()[:7]

    google = google_figures.rows(google_figures.load(google_figures.SCORED))
    m = google["gemini-3.5-flash-lite"]
    excluded = [e for e in google_figures.excluded(google_figures.load(google_figures.SCORED))
                if "probe" not in e]
    rs["P5"].headline = pairs_headline(m).replace("no $ figure", "free tier, $0.00 billed")
    if not excluded:
        raise SystemExit("benchmark_matrix: P5 names no excluded cell")
    rs["P5"].date, rs["P5"].commit = m["measured_on"], m["claimcheck_commit"][:7]

    sub = subscription_figures.rows(subscription_figures.load(subscription_figures.SCORED),
                                    subscription_figures.load(subscription_figures.RESULTS))
    for rid, route in (("P6", "claude-haiku"), ("P7", "claude-sonnet"), ("P8", "claude-opus")):
        m = sub[route]
        rs[rid].headline = pairs_headline(m).replace("no $ figure", "no $ (subscription)")
        rs[rid].date, rs[rid].commit = m["measured_on"], m["claimcheck_commit"][:7]

    cat = {m["id"]: m for m in load(CATALOGUE)["models"]}
    formed = matrix_figures.rows(matrix_figures.load(matrix_figures.SCORED))
    for rid, model in (("P9", "claude-opus-5"), ("P10", "claude-sonnet-5"),
                       ("P11", "claude-haiku-4-5"), ("P12", "gpt-5.6-terra")):
        # The run-attribution check only holds while catalogue.json
        # still names this row to matrix_figures.py -- claude-sonnet-5 and
        # claude-haiku-4-5 were superseded by the release benchmark and
        # now carry arms/2026-09-27/lineup/'s run; their P9-P12 headline
        # below still reads this run's own committed cells regardless.
        # claude-opus-5 was removed from the card entirely, by ruling,
        # not superseded (matrix_figures.REMOVED_FROM_CARD): `cat` has no
        # entry for it at all, so there is nothing to check the run against;
        # P9's headline still reads this run's own committed cells the same
        # way.
        entry = cat.get(model)
        measured = entry["measured"] if entry is not None else None
        if measured is not None and matrix_figures.SCRIPT in str(measured.get("derived_by")) \
                and measured["run"] != "2026-09-18-matrix":
            raise SystemExit(f"benchmark_matrix: {rid} expects catalogue row {model} "
                             f"from 2026-09-18-matrix, found {measured['run']}")
        m = formed[model]
        rs[rid].headline = pairs_headline(m)
        rs[rid].date, rs[rid].commit = m["measured_on"], m["claimcheck_commit"][:7]


def headline_handwritten(rs: dict[str, Row]) -> None:
    cat = {m["id"]: m for m in load(CATALOGUE)["models"]}
    league = {r["model"]: r for r in load(LEAGUE)["disqualified"] + load(LEAGUE)["survivors_ranked"]}

    def league_text(name: str) -> str:
        r = league[name]
        dq = "; ".join(r["disqualifiers"]) or "none"
        return (f"league (6 runs, `low` and `high`): coverage {r['present'] + r['near']}/"
                f"{r['segments']} ({r['coverage'] * 100:.1f}%), silent loss "
                f"{r['silent_loss']} segments, duplicates {r['dup']}, runs "
                f"{r['runs_measured']}/{r['runs_expected']}; disqualified: {dq}")

    formed = phase4_figures.rows(phase4_figures.load(phase4_figures.SCORED))
    for rid, cat_id, lg in (("H1", "qwen3-8b", "8b"), ("H2", "qwen3.8-27b-fp8", "27b-fp8")):
        if cat[cat_id]["measured"]["run"] != "2026-09-16-phase4":
            raise SystemExit(f"benchmark_matrix: {rid} expects {cat_id} from "
                             f"2026-09-16-phase4, found {cat[cat_id]['measured']['run']}")
        m = formed[cat_id]
        rs[rid].headline = ("catalogue (`high`): " + pairs_headline(m) + "; "
                            + league_text(lg))
        rs[rid].date = m["measured_on"]
        rs[rid].commit = commits(ROOT / "arms" / "2026-09-16" / "phase4", f"-{lg}")
    for rid, lg in (("H3", "claude-haiku-4-5"), ("H4", "gpt-5.6-terra")):
        rs[rid].headline = league_text(lg)
        rs[rid].date = "2026-09-17"
        rs[rid].commit = commits(ROOT / "arms" / "2026-09-17" / "frontier-thinking", f"-{lg}")
    # The league figures are re-derived from the published runs, not read.
    survivors, disqualified = league_table.league()
    if league_table.to_json(survivors, disqualified) != load(LEAGUE):
        raise SystemExit("benchmark_matrix: tests/league_table.json is not what the "
                         "published runs give (python3 tests/league_table.py --check)")

    frontier = ROOT / "arms" / "2026-09-17" / "frontier"
    runs = load(frontier / "results.json")
    refused = sum(1 for r in runs if r.get("exit_code") == 2)
    by_arm = ", ".join(f"`{a}` {sum(1 for r in runs if r['arm'] == a)}"
                       for a in sorted({r["arm"] for r in runs}))
    rs["H5"].headline = (f"{len(runs)} arms run before the stop ({by_arm}); {refused} "
                         f"ended at exit 2; no quality figure (void)")
    rs["H5"].date = "2026-09-17"
    rs["H5"].commit = commits(frontier, "")

    cells, agg = rank_arms.collect()
    for rid, arm in (("H6", "claude-opus-5"), ("H7", "claude-sonnet-5"),
                     ("H8", "claude-haiku-4-5"), ("H9", "gpt-5.6-terra")):
        tot, n = agg[arm], agg[arm]["n"]
        dev = tot["lost"] + tot["bloat"] + tot["dup"]
        rs[rid].headline = pairs_headline({
            "silent_loss": tot["silent"], "silent_loss_per_pair": tot["silent"] / n,
            "deviations": dev, "deviations_per_pair": dev / n, "pairs": n,
            "usd_per_merge": tot["cost100"] / 100 / n, "seconds_per_merge": tot["secs"] / n})
        rs[rid].date = "2026-09-18"
        rs[rid].commit = ", ".join(sorted({c["commit"] for c in cells if c["arm"] == arm}))


def commits(run: Path, suffix: str) -> str:
    """Every tool commit the reports of `run`'s cells ending in `suffix` record."""
    found = set()
    for report in sorted(run.glob(f"*{suffix}/report.json")):
        found.add(str((load(report).get("provenance") or {}).get("claimcheck_commit"))[:7])
    return ", ".join(sorted(found)) or "?"


def headline_planted(rs: dict[str, Row]) -> None:
    scored = effort_figures.load(effort_figures.SCORED)
    blocks = effort_figures.blocks(scored, effort_figures.load(effort_figures.RESULTS))
    for rid, route, alias in (("E1", "claude-opus", "opus"), ("E2", "claude-sonnet", "sonnet"),
                              ("E3", "claude-haiku", "haiku")):
        b = blocks[route]
        levels = b["levels"]
        parts = []
        for pair in effort_figures.PAIRS:
            planted = one_value({lv["pairs"][pair]["planted"] for lv in levels.values()},
                                f"{rid} {pair} planted")
            cells = ", ".join(f"{name} {fmt_spread(lv['pairs'][pair]['fixed'])}"
                              for name, lv in levels.items())
            parts.append(f"{pair} fixed of {planted}, median (min-max): {cells}")
        lic = ", ".join(f"{name} {lv['pairs']['bip39']['licence_fixed']}/"
                        f"{lv['pairs']['bip39']['draws']}" for name, lv in levels.items())
        parts.append(f"bip39 licence fixed: {lic}")
        ret = ", ".join(f"{name} {lv['searched']}/{lv['runs']}" for name, lv in levels.items())
        parts.append(f"runs that retrieved: {ret}")
        control = [r for r in scored if r["pair"] == "mahjongg" and r["model"] == alias]
        if control:
            # Rescored by `mahjongg_figures`, whose check `effort_figures
            # --check` runs; the count first published stays beside it.
            now = [r["false_corrections"] for r in control]
            first = [r["rescored"]["first_scored"]["false_corrections"] for r in control]
            said = ("unchanged" if first == now else f"first published as {span(first)}")
            parts.append(f"mahjongg false corrections (`medium`, {len(now)} draws): "
                         f"{span(now)}, rescored on 2026-09-27 with the corrected "
                         f"scorer, {said}")
        rs[rid].headline = "; ".join(parts)
        rs[rid].date, rs[rid].commit = b["measured_on"], b["claimcheck_commit"][:7]
        rs[rid].extra["resolved"] = b["resolved_model"]
    rs["E4"].date = "2026-09-23 to 24"
    b = opus55_effort_figures.block(opus55_effort_figures.load(opus55_effort_figures.SCORED),
                                    opus55_effort_figures.load(opus55_effort_figures.RESULTS))
    cells = ", ".join(f"{name} {fmt_spread(lv['pairs']['voyager']['fixed'])}, "
                      f"{lv['pairs']['voyager']['seconds']['median']:g} s, "
                      f"${lv['api_equivalent_usd']['median']:.2f} API-equivalent "
                      f"(${lv['uncached_list_usd']['median']:.2f} at uncached list price)"
                      for name, lv in b["levels"].items())
    rs["E5"].headline = f"voyager fixed of {one_value({lv['pairs']['voyager']['planted'] for lv in b['levels'].values()}, 'E5 planted')}, median (min-max): {cells}"
    rs["E5"].date, rs["E5"].commit = b["measured_on"], b["claimcheck_commit"][:7]
    rs["E5"].extra["resolved"] = b["resolved_model"]


def fmt_spread(s: dict) -> str:
    return f"{s['median']} ({s['min']}-{s['max']})"


def headline_fixtures(rs: dict[str, Row]) -> None:
    block = depth_figures.block()
    depths = {d["value"]: d for d in block["depths"]}
    for rid, name in (("D1", "full"), ("D2", "coverage")):
        d = depths[name]
        fwd, rev = d["source_to_merged"], d["merged_to_sources"]
        unreachable = sum(c["plants"] for c in d["cannot_detect"])
        reach = f" of those it can reach ({unreachable} unreachable)" if unreachable else ""
        guards_graded = fwd["guards_graded"] + rev["guards_graded"]
        guards_wrong = fwd["guards_wrong"] + rev["guards_wrong"]
        text = (f"plants detected {fwd['plants_detected'] + rev['plants_detected']}/"
                f"{fwd['plants'] + rev['plants']}{reach} (source to merged "
                f"{fwd['plants_detected']}/{fwd['plants']}, merged to sources "
                f"{rev['plants_detected']}/{rev['plants']}, "
                f"{fwd['plants_detected_mechanically'] + rev['plants_detected_mechanically']}"
                f" by the mechanical check); guards wrong {guards_wrong} of "
                f"{guards_graded} graded; {d['model_calls']} model calls, "
                f"{d['seconds']:.0f} s")
        if "speedup" in d:
            text += f"; {d['speedup']}x faster than `{block['comparator']}`"
        rs[rid].headline = text
    cat = load(CATALOGUE)["verify_depth"]
    for rid in ("D1", "D2"):
        rs[rid].date, rs[rid].commit = cat["measured_on"], cat["claimcheck_commit"][:7]
        if cat["model"] != block["model"]:
            raise SystemExit("benchmark_matrix: depth model disagrees with the catalogue")
    for rid in ("D3", "D4"):
        # Declared: no committed
        # record of that run carries its commit.
        rs[rid].date, rs[rid].commit = "2026-09-22", "9f1d5d4"
    rs["D5"].date = "2026-09-23"

    regrade = {a["arm"]: a for a in load(RECORDS / "regrade-detect.json")["arms"]}
    for rid, arm in (("D6", "A-27b"), ("D7", "B-70b"), ("D8", "C-120b")):
        rec = load(RECORDS / f"half1-{arm}.json")
        s = rec["summary"]
        g = regrade[arm]
        dq = "; ".join(s["disqualified"]) or "none"
        rs[rid].headline = (
            f"as run: exit codes matched {len(s['exit_code_matched'])}/{s['fixtures']}, "
            f"plants {s['plants_detected']}/{s['plants_total']}, invented findings "
            f"{s['invented_total']}, disqualified: {dq}; regraded: matched "
            f"{g['matched']}/{g['fixtures_measured']} measured, {g['unmeasured']} unmeasured")
        rs[rid].extra["model"] = passthrough_model(s["passthrough"])
        rs[rid].date = "2026-08-29"
        rs[rid].commit = load(RECORDS / f"half2-{arm}.json")["provenance"]["claimcheck_commit"][:7]
    for rid, arm in (("D9", "A-27b"), ("D10", "B-70b"), ("D11", "C-120b")):
        rec = load(RECORDS / f"half2-{arm}.json")
        f = rec["forward"]
        rs[rid].headline = (f"forward probes supported {f['supported']}/{f['probes_measured']} "
                            f"measured of {f['probes_declared']}")
        rs[rid].extra["model"] = rec["provenance"]["models"]["verify"]
        rs[rid].date = rec["provenance"]["generated_at"][:10]
        rs[rid].commit = rec["provenance"]["claimcheck_commit"][:7]

    inv = {a["arm"]: a for a in load(RECORDS / "regrade-inventions.json")["arms"]}
    guards = {a["arm"]: a for a in load(RECORDS / "regrade-guard-probes.json")["arms"]}
    for rid, arm in (("D12", "A-27b"), ("D13", "B-70b"), ("D14", "C-120b")):
        a, g = inv[arm], guards[arm]
        matched = a["fixtures"] - len(a["exit_code_missed"]) - len(a["exit_code_unmeasured"])
        dq = sorted({d.split(":")[0] for d in a["disqualified"]})
        rs[rid].headline = (
            f"exit codes matched {matched}/{a['fixtures']}"
            + (f" ({len(a['exit_code_unmeasured'])} unmeasured)" if a["exit_code_unmeasured"] else "")
            + f"; plants {a['plants_detected']}/{a['plants_total']}; invented findings "
            f"{a['invented_total']}; guard probes wrong {g['guard_wrong_total']}/"
            f"{g['guard_probes_total']}; disqualified on: {', '.join(dq) or 'none'}")
        rec = load(RECORDS / f"detect-2026-09-03-{arm}.json")
        rs[rid].extra["model"] = passthrough_model(rec["summary"]["passthrough"])
        reports = sorted((ROOT / "arms" / "2026-09-03" / arm / "detect-reports").glob("*.json"))
        prov = [load(p)["provenance"] for p in reports]
        rs[rid].date = one_value({p["generated_at"][:10] for p in prov}, f"{rid} date")
        rs[rid].commit = one_value({p["claimcheck_commit"][:7] for p in prov}, f"{rid} commit")


def passthrough_model(argv: list[str]) -> str:
    return argv[argv.index("--model") + 1]


def one_value(values: set, what: str):
    if len(values) != 1:
        raise SystemExit(f"benchmark_matrix: expected one {what}, found {sorted(map(str, values))}")
    return next(iter(values))


def arm_headline(g: dict) -> str:
    if g.get("status") == "error":
        return (f"exit {g['exit_code']} in {g['draws_errored']}/{g['draws_k']} draws, "
                f"failed at {', '.join(g['failed_at_stage'])}; no report written")
    kinds = g["structural"]["by_kind"]
    loss = g["declared_loss"]
    text = (f"exit {g['exit_code']}; undeclared absence {kinds.get('undeclared_absence', 0)}; "
            f"verbatim violations {kinds.get('verbatim_violation', 0)}; declared drops "
            f"{loss['drops']} of {loss['segments']} segments (over budget: "
            f"{'yes' if loss['over_budget'] else 'no'}); verify findings {g['findings']}")
    if "findings_grounded" in g:
        text += f" ({g['findings_grounded']} grounded)"
    return text


def headline_index429(rs: dict[str, Row]) -> None:
    regrade = {r["arm"]: r for r in load(RECORDS / "regrade-pair429.json")}
    for rid in ("I1", "I2", "I3", "I4", "I6", "I7", "I8", "I9", "I10"):
        row = rs[rid]
        d, arm = row.extra["dir"], row.extra["arm"]
        graded = {g["arm"]: g for g in load(AUG / d / "graded.json")}[arm]
        text = arm_headline(graded)
        draws = graded.get("draws")
        draw_dirs = sorted(p for p in (AUG / d).glob(f"{arm}*") if p.is_dir())
        merged = [p / "merged.md" for p in draw_dirs if (p / "merged.md").is_file()]
        if draws and merged:
            distinct = len({hashlib.sha256(p.read_bytes()).hexdigest() for p in merged})
            text += (f"; draws {draws['k']}, merged.md distinct {distinct} of {len(merged)}, "
                     f"whole record identical to draw 1 in {draws['identical_to_shown']}")
        if graded.get("varies"):
            text += f"; varied across draws: {', '.join(sorted(graded['varies']))}"
        if d != "2c" and arm in regrade and graded.get("status") != "error":
            s = regrade[arm]["structural"]["by_kind"]
            text += (f"; regraded (regrade-pair429): absent {s['undeclared_absence']}, "
                     f"reworded {s['undeclared_rewording']}")
        row.headline = text
        if graded.get("model") and graded["model"] not in row.models:
            raise SystemExit(f"benchmark_matrix: {rid} names {row.models}, "
                             f"graded.json says {graded['model']}")
        reports = sorted(p / "report.json" for p in draw_dirs if (p / "report.json").is_file())
        if reports:
            prov = [load(p)["provenance"] for p in reports]
            row.date = one_value({p["generated_at"][:10] for p in prov}, f"{rid} date")
            row.commit = one_value({p["claimcheck_commit"][:7] for p in prov}, f"{rid} commit")
        else:
            row.date = "2026-08-31"   # k5c/arms.log: the chain closed 2026-08-31
    bench = load(RECORDS / "bench-k5replication.json")
    h = bench["scores"]["honesty_k5"]
    absent = ", ".join(str(d["undeclared_absence"]) for d in bench["draws"])
    rs["I5"].headline = (f"draws declaring a drop {h['draws_declaring_drop']}/{h['draws']} "
                         f"(declared drops {h['declared_drops']['min']}-"
                         f"{h['declared_drops']['max']}); over budget "
                         f"{h['draws_over_budget']}/{h['draws']}; distinct merges "
                         f"{h['distinct_merges']}; undeclared absence per draw {absent}")
    rs["I5"].commit = one_value({d["commit"][:7] for d in bench["draws"]}, "I5 commit")
    rs["I5"].date = "2026-08-30"
    rs["I11"].date = "2026-08-31"
    rs["I12"].date = "2026-09-19"


def headline_cassettes(rs: dict[str, Row], files: list[str]) -> None:
    census: dict[str, dict[str, int]] = {}
    models: dict[str, set] = {}
    dates: dict[str, set] = {}
    sources: dict[str, set] = {}
    for f in files:
        if not (f.startswith("tests/responses/") and f.endswith(".json")):
            continue
        parts = f.split("/")
        sub = parts[2] if len(parts) > 3 else "root"
        blob = load(ROOT / f)
        if not isinstance(blob, dict) or "request" not in blob:
            continue
        req = blob["request"]
        census.setdefault(sub, {}).setdefault(req["role"], 0)
        census[sub][req["role"]] += 1
        models.setdefault(sub, set()).add(req["model"])
        dates.setdefault(sub, set()).add(blob["recorded_at"][:10])
        sources.setdefault(sub, set()).add((blob.get("meta") or {}).get("claimcheck_source", "?"))

    def text(subs: tuple[str, ...]) -> str:
        out = []
        for sub in subs:
            roles = ", ".join(f"{n} {r}" for r, n in sorted(census[sub].items()))
            out.append(f"`{'tests/responses/' if sub == 'root' else 'tests/responses/' + sub + '/'}` "
                       f"{roles}")
        return "; ".join(out)

    def dated(subs: tuple[str, ...]) -> str:
        ds = sorted(set().union(*(dates[s] for s in subs)))
        return ds[0] if len(ds) == 1 else f"{ds[0]} to {ds[-1][-2:]}"

    for rid, subs in (("C1", ("root", "m7")), ("C2", ("m4",)), ("C3", ("pairs",))):
        row = rs[rid]
        seen = set().union(*(models[s] for s in subs))
        if len(seen) != 1 or not {m.replace("qwen/", "") for m in seen} & set(row.models):
            raise SystemExit(f"benchmark_matrix: {rid} names {row.models}, the cassettes "
                             f"say {sorted(seen)}")
        row.headline = text(subs) + " cassettes"
        row.date = dated(subs)
        src = set().union(*(sources[s] for s in subs)) - {"?"}
        row.commit = one_value({s[:7] for s in src}, f"{rid} source") if len(src) == 1 else "?"
    unrecordable = unrecordable_keys()
    rs["C1"].headline += (f"; {unrecordable} request keys unrecordable (a runaway), "
                          f"their probes reported UNMEASURED")
    # The verify half predates a prompt change whose re-record the
    # operator has held back. Derived from the cassettes, so the row goes back
    # to "current" by itself in the commit that imports the re-record.
    held = held_back_verify()
    if held:
        rs["C1"].status = "current; verify stale by ruling, 1 request unrecordable"
        rs["C1"].refs += ", 668"
        rs["C1"].headline += (f"; the {held} verify cassettes predate the 2026-09-26 "
                              f"prompt change and replay UNMEASURED until the held-back "
                              f"re-record")

    rs["C4"].headline = NOT_DERIVABLE + " at HEAD (the corpus is in git history)"
    rs["C4"].date = "2026-08 to 09"


def held_back_verify() -> int:
    """How many C1 verify cassettes are stale by the operator's ruling, 0 if none."""
    found = [stale_corpus.survey(CASSETTES / sub, "verify") for sub in ("", "m7")]
    return sum(sum(n for _, n in f.held) for f in found if f is not None and f.deferred)


def unrecordable_keys() -> int:
    """`run_verify.UNRECORDABLE`, read without importing the harness."""
    tree = ast.parse((ROOT / "tests" / "run_verify.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "UNRECORDABLE":
            return len(node.value.keys)  # type: ignore[union-attr]
    raise SystemExit("benchmark_matrix: tests/run_verify.py has no UNRECORDABLE")


def headline_rest(rs: dict[str, Row]) -> None:
    for rid in ("X1", "X2", "X3", "X4", "X5", "X6"):
        rs[rid].date = "2026-08-07"
    for rid in ("X7", "X8"):
        rs[rid].date = "2026-08-08"
    rs["X8"].commit = "af36c70"
    rs["X9"].date = "2026-09-12"
    for row in rs.values():
        if not row.headline:
            row.headline = NOT_DERIVABLE


# ---------------------------------------------------------------------------
# Evidence


def evidence_level(row: Row, files: list[str], problems: list[str]) -> str:
    def matches(pattern: str) -> list[str]:
        return [f for f in files if fnmatch(f, pattern)]

    for pattern in row.raw + row.scores:
        if not matches(pattern):
            problems.append(f"{row.id}: names `{pattern}` as committed evidence and "
                            f"no tracked file matches it")
    if row.raw:
        return "raw"
    if row.history:
        return "history"
    if row.scores:
        return "scores"
    return "none"


# ---------------------------------------------------------------------------
# Models

# (id, what it is, status, note). The routes and rows are derived from ROWS.
MODELS = [
    ("claude-opus-5-5", "current", "Replaced Opus 5 on the page. Measured "
     "through the subscription by its full id, which needs Claude Code 2.1.280 or "
     "newer; the `opus` alias answers as this model since 2026-09-26, "
     "on 2.1.283."),
    ("gpt-6-sol", "current", ""),
    ("gpt-6-luna", "current", ""),
    ("gemini-3.5-flash-lite", "best effort", "Free tier only."),
    ("claude-sonnet-5", "current", "API rows date from 2026-09-18 and its "
     "subscription rows from 2026-09-24 and 25."),
    ("claude-haiku-4-5", "current", "Resolved id `claude-haiku-4-5-20251001` on "
     "every route."),
    ("claude-opus-5", "retired", "Retired 2026-09-25; refuses every merge "
     "through the API at master. The subscription alias `opus` still "
     "answered as this model on 2026-09-25, so P8 and E1 describe it too; since "
     "2026-09-26 it answers as `claude-opus-5-5`."),
    ("gpt-5.6-terra", "superseded", "By GPT-6 Sol and Luna; its catalogue row stays, "
     "dated 2026-09-18."),
    ("Qwen/Qwen3.8-27B-FP8", "current", "The reference model of the recorded corpus "
     "since 2026-09-25 and of the depth benchmark; served by vLLM on a metered serverless "
     "endpoint. The same model family as `qwen3.8:27b` below, at another "
     "quantisation and server, so the two are listed apart."),
    ("qwen3:8b", "superseded", "The first reference model; its root and `m7/` "
     "corpus was replaced by the 27B's. `m4/` and `pairs/` still carry it."),
    ("qwen3.8:27b", "frozen", "Arm A of the August study."),
    ("deepseek-r1:70b", "frozen", "Arm B of the August study; rejected by the 2026-08-29 verdicts on a "
     "missed plant, a disqualifier the regrade of that run no longer fires."),
    ("gpt-oss:120b", "frozen", "Arm C of the August study; see the section below."),
    ("gpt-oss:20b", "frozen", "Probed only; its Block 4 arm never ran."),
    ("qwen3:4b", "exploratory", "Measured once against the 8b; never an arm."),
    ("gpt-5-1", "exploratory", "One sample in the 2026-08-07 sweep."),
    ("claude-sonnet-4-5", "exploratory", "One sample in the 2026-08-07 sweep."),
    ("kimi-k2", "exploratory", "One sample in the 2026-08-07 sweep."),
    ("kimi-k3", "exploratory", "Verify measured, decompose did not (HTTP 504)."),
]

# Named, never measured. Each is a model a reader might expect to find above.
NEVER_MEASURED = [
    ("gemini-3.8-flash", "Registered with Flash-Lite; the free tier's 20 "
     "requests a day were spent by the pilot. In progress on its own schedule, "
     "best effort. The pilot's logs are at `arms/2026-09-25/google/pilot/`."),
    ("claude-fable (subscription alias)", "Not run: the author did not want the "
     "most expensive model used. Its resolved id is not known."),
    ("gpt-5.6-luna", "Registered in Block 5, which never ran."),
    ("qwen3:14b, llama3.3:70b, gemma3:27b, mistral-small", "Registered in Blocks 1-3 "
     "of the August study, never served; frozen on 2026-09-15."),
    ("qwen-3-5-397b", "Two attempts on 2026-08-07, both HTTP 504 at the gateway; no "
     "answer was ever recorded."),
    ("gemini-2.5-flash", "The free-tier run's named fallback; answers 404 to the key."),
]

GPT_OSS_120B = """\
**What ran.** `gpt-oss:120b` was arm C of the August local-model study, on a
rented 80 GB pod through Ollama at temperature 0, seed 0 and the `json_schema`
tier: the detection block on 2026-08-29 (D8, D11), the public pair
`index_429` on 2026-08-30 and 31 (I3, I5, I9, I10), and the detection re-run
of 2026-09-03 (D14). It has not run since 2026-09-03.

**Verdicts, in order.**

- **2026-08-29: supported, with caveats.** The detection block, D8:
  {d8}. The verdict carried six caveats: the most invented findings of the
  three arms, one exit code produced by a finding no probe anchors, no
  reproducibility at temperature 0 across pods, a hard dependency on thinking
  in all three roles, 2.1x the control's wall clock, and one
  `invented_claims` firing in half 2.
- **2026-08-30: K = 5, and not Block 4's control.** This model does
  not repeat at temperature 0 with a fixed seed, so a rerun of it is a fresh
  sample, not a check. Its arms on the public pair were therefore drawn five
  times (I5, I9, I10) and reported as rates, never as a median; and its
  measurements may not be reused as the control of Block 4 (`gpt-oss:20b`
  against it), which never ran.
- **2026-08-30: honesty settles in halves.** I5: {i5}. Declaring a drop
  reproduces as a rate; going over the loss budget does not reproduce at all.
  The single public draw before it (I3) had sampled the minority draw.
- **2026-08-31: the thinking axis.** With thinking at merge only,
  I9: {i9}. With thinking on every role, I10: {i10}.
- **2026-08-31 to 09-02: the empty body.** On 2026-08-31 no surviving raw
  response could tell a harness defect from a model property, and the paper's
  reading was put under review. On 2026-09-02 the endpoint's own envelope
  settled it: `content` empty, no reasoning field of either
  spelling, 996 completion tokens billed. The model generated and stopped; the
  tokens are discarded above the tool, so it is not a harness defect. A
  hand-written probe (X9) found `gpt-oss:20b` did not reproduce it, and a run
  through the tool's own decompose path reversed that, where the 20B emptied
  its body too (on an off-configuration window). The same mechanism was later
  seen on the 27B at the merge role, so it is not specific to this model.
- **2026-09-03 re-run: disqualified.** D14: {d14}. A finding of 2026-09-23
  later showed `attribution_invented` undetectable by construction under the
  decompose prompt of that date; it re-scored nothing, and on 2026-09-03 the
  27B did detect that plant (D12). The other two disqualifying fixtures do not
  depend on it.

**Non-determinism at temperature 0.** Measured two ways: two distinct merges
in the five draws of I5; and in I10, five byte-identical merges whose
downstream records still differed ({i10_varies}).

**Why it is not in the current catalogue.** It was never retired. The catalogue
reports silent loss and deviation on the nine pairs, a design that began on
2026-09-16, and this model was never run on it: the study it belongs to was
frozen as history on 2026-09-15, its hardware was a rented pod that no
longer exists, and I9 shows it answers nothing with thinking off at decompose,
so any future run needs thinking on every role. It is unmeasured on the current
design, not ruled out.
"""


# ---------------------------------------------------------------------------
# Rendering


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def table(header: tuple[str, ...], body: list[tuple[str, ...]]) -> list[str]:
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(cell(c) for c in r) + " |" for r in body]
    return out


def evidence_cell(row: Row) -> str:
    paths = row.raw or row.scores
    where = ", ".join(f"`{p}`" for p in paths[:2])
    if row.evidence == "raw" and row.scores:
        where += f"; scores `{row.scores[0]}`"
    return f"**{row.evidence}**" + (f": {where}" if where else "")


def render(all_rows: list[Row]) -> str:
    by = {r.id: r for r in all_rows}
    out = [
        "# Benchmark matrix",
        "",
        f"Every model measurement this project has made, as of **{AS_OF}**: one row",
        "per run group, with its settings, its headline figures in the units its",
        "source uses, its status and the committed evidence behind it.",
        "",
        "Generated by `python3 tests/benchmark_matrix.py --write`; do not edit it by",
        "hand. `python3 tests/benchmark_matrix.py --check` rebuilds it from the",
        "committed records and fails if this file differs, and `tests/run_all.py`",
        "runs that check. Every figure here is derived from a committed file; a run",
        "whose figures live only in a note or outside the repository says",
        f"\"{NOT_DERIVABLE}\" and is listed under [Evidence gaps](#evidence-gaps).",
        "Rows whose evidence is under `paper/records/` cite graded records that are",
        "withheld with the paper in this release; in a copy without them the check",
        "says UNMEASURED instead of rebuilding this file.",
        "",
        f"**{len(all_rows)} run groups.** Rows are not a leaderboard: read the",
        "comparability column before setting two rows side by side.",
        "",
        "## Legend",
        "",
        "**Status.**",
        "",
    ]
    out += [f"- `{k}`: {v}." for k, v in STATUS.items()]
    out += ["", "**Evidence.**", ""]
    out += [f"- `{k}`: {v}." for k, v in EVIDENCE.items()]
    out += [
        "",
        "**Settings.** Fidelity is the merge's `--fidelity` level. Verify depth is",
        "`--verify-depth`; before 2026-09-21 `full` was the only",
        "depth. Merge effort is the reasoning effort sent for the merge role. Thinking",
        "is which roles were asked to reason. Tier is the structured-output rung and",
        "whether it was pinned or probed. Safe mode applies to the `claude` CLI only:",
        "every subscription row here but E5 ran before the 2026-09-25 change that isolated it. `?` means",
        "no committed file records the value; `n/a` means the setting does not apply.",
        "",
        "**Units.** Silent loss counts segments missing from a merge that the merge",
        "did not declare. Deviations are lost, bloat and duplicate segments against",
        "the pair's reference, two-sided. Planted-error rows count errors fixed of",
        "those planted, median and range over draws. Detection rows count exit codes",
        "matched, plants detected and findings invented. `K` is draws per cell.",
        "A date in a setting, as in \"before 2026-09-25\", is the day that setting changed.",
        "",
        "**Test sets.**",
        "",
    ]
    used = {r.test_set for r in all_rows}
    out += [f"- {TEST_SETS[k][0]}: {TEST_SETS[k][1]}." for k in TEST_SETS if k in used]
    out.append("")

    out += ["## Run groups", ""]
    for key, title in SECTIONS.items():
        section = [r for r in all_rows if r.section == key]
        if not section:
            continue
        out += [f"### {key}. {title}", ""]
        out += table(("ID", "Model", "Route", "Test set", "K", "Date", "Commit", "Headline",
                      "Status", "Evidence"),
                     [(r.id, ", ".join(f"`{m}`" for m in r.models), r.route,
                       TEST_SETS[r.test_set][0], r.k, r.date, ", ".join(f"`{c}`" for c in r.commit.split(", ")) if r.commit != "?" else "?",
                       r.headline, r.status, evidence_cell(r)) for r in section])
        out += ["", "Settings and comparability:", ""]
        out += table(("ID", "Fidelity", "Verify depth", "Merge effort", "Thinking", "Tier",
                      "Safe mode", "Not comparable because"),
                     [(r.id, *r.settings, r.comparable) for r in section])
        out.append("")

    out += ["## Evidence gaps", "",
            "Every row whose raw output is not in the repository, and every partial gap",
            "on a row whose raw output is. Nothing here is papered over: a row listed",
            "here is either cited with this caveat or not cited.", ""]
    n = 0
    for r in all_rows:
        if r.evidence == "raw" and not r.gap:
            continue
        n += 1
        models = ", ".join(f"`{m}`" for m in r.models)
        what = {"scores": "scores committed, raw output not",
                "history": "in git history only",
                "none": "no committed evidence",
                "raw": "raw output committed, with a partial gap"}[r.evidence]
        detail = r.gap if r.evidence == "raw" else r.elsewhere
        detail = resolve_as(detail, by, "gap" if r.evidence == "raw" else "elsewhere")
        out.append(f"{n}. **{r.id}** {models}, {r.date}, {TEST_SETS[r.test_set][0]}: "
                   f"{what}. {detail[:1].upper() + detail[1:]}.")
    out.append("")

    out += ["## Models", "",
            "Every model this project has run, with the rows that measured it.", ""]
    routes: dict[str, list[str]] = {}
    ids: dict[str, list[str]] = {}
    for r in all_rows:
        for m in r.models:
            ids.setdefault(m, []).append(r.id)
            route = route_of(m, r.route)
            if route not in routes.setdefault(m, []):
                routes[m].append(route)
    out += table(("Model", "Routes", "Rows", "Status", "Note"),
                 [(f"`{m}`", "; ".join(routes[m]), ", ".join(ids[m]), status, note)
                  for m, status, note in MODELS])
    out += ["", "**Named but never measured:**", ""]
    out += [f"- `{m}`: {why}" for m, why in NEVER_MEASURED]
    out += ["", "### `gpt-oss:120b`", "", gpt_oss_120b(by).rstrip(), ""]

    out += ["## Coverage", "",
            "Model against test set: the rows that measured each combination, `-` where",
            "none did. A `-` is a combination never run, not a result. \"Other\" holds",
            "the recorded pair corpus, the early fixtures and the probe.",
            ""]
    header = ("Model",) + tuple(TEST_SETS[k][0] for k in GRID) + ("other",)

    def hits(m: str, sets: tuple[str, ...]) -> str:
        found = [r.id + (f" ({r.extra['coverage']})" if "coverage" in r.extra else "")
                 for r in all_rows if m in r.models and r.test_set in sets]
        return ", ".join(found) or "-"

    others = tuple(k for k in TEST_SETS if k not in GRID)
    body = [(f"`{m}`", *(hits(m, (k,)) for k in GRID), hits(m, others))
            for m, _, _ in MODELS]
    out += table(header, body)
    out += ["", "**Never run, for the models a reader can pick today** (status `current`",
            "or `best effort`), on the four sets the current rows are measured on:", ""]
    for m, status, _ in MODELS:
        if status not in ("current", "best effort"):
            continue
        missing = [TEST_SETS[k][0] for k in OPEN_SETS
                   if not any(m in r.models and r.test_set == k for r in all_rows)]
        partial = [f"{TEST_SETS[r.test_set][0]} ({r.id}: {r.extra['coverage']} only)"
                   for r in all_rows if m in r.models and "coverage" in r.extra
                   and not any(m in o.models and o.test_set == r.test_set
                               and "coverage" not in o.extra for o in all_rows)]
        text = ", ".join(missing) if missing else "none"
        if partial:
            text += "; partly: " + ", ".join(partial)
        out.append(f"- `{m}`: {text}")
    out.append("")
    return "\n".join(out)


def route_of(model: str, route: str) -> str:
    """A row's route as it applies to one of its models, alias detail dropped."""
    route = route.split(", alias")[0]
    if route == "API (Anthropic, OpenAI)":
        return API_A if model.startswith("claude") else API_O
    return route


def resolve_as(text: str, by: dict[str, Row], attr: str) -> str:
    """`as P9` in a declared field means P9's text; the gap list spells it out."""
    seen = set()
    while text.startswith("as ") and text[3:] in by and text not in seen:
        seen.add(text)
        text = getattr(by[text[3:]], attr)
    return text.rstrip(".")


def gpt_oss_120b(by: dict[str, Row]) -> str:
    varies = by["I10"].headline.split("varied across draws: ")[-1].split(";")[0]
    return GPT_OSS_120B.format(d8=by["D8"].headline, i5=by["I5"].headline,
                               i9=by["I9"].headline, i10=by["I10"].headline,
                               d14=by["D14"].headline, i10_varies=varies)


# ---------------------------------------------------------------------------
# Build and check


def build() -> tuple[str, list[str], list[Row]]:
    files = tracked()
    all_rows = rows()
    by = {r.id: r for r in all_rows}
    problems: list[str] = []
    if len(by) != len(all_rows):
        problems.append("two rows share an id")
    headline_pairs(by)
    headline_handwritten(by)
    headline_planted(by)
    headline_fixtures(by)
    headline_index429(by)
    headline_cassettes(by, files)
    headline_rest(by)
    for r in all_rows:
        r.evidence = evidence_level(r, files, problems)
        if r.evidence != "raw" and not r.elsewhere:
            problems.append(f"{r.id}: evidence is {r.evidence} and the row does not say "
                            f"where its output or figures are")
        if r.status.split(";")[0] not in STATUS:
            problems.append(f"{r.id}: unknown status {r.status!r}")
        # A model a detection record names must be the row's model.
        named = r.extra.get("model")
        if named and named not in r.models:
            problems.append(f"{r.id}: names {r.models}, its record says {named}")
    known = {m for m, _, _ in MODELS}
    for r in all_rows:
        for m in r.models:
            if m not in known:
                problems.append(f"{r.id}: model {m} is not in MODELS")
    if {r.id for r in all_rows if r.route.startswith("subscription") and r.settings[5] != PRE_610} != {"E5"}:
        problems.append("the legend says E5 is the one subscription row not run before safe mode")
    for m in known:
        if not any(m in r.models for r in all_rows):
            problems.append(f"MODELS lists {m} and no row measured it")
    return render(all_rows), problems, all_rows


def differs(committed: str, fresh: str) -> list[str]:
    return list(difflib.unified_diff(committed.splitlines(), fresh.splitlines(),
                                     "committed", "regenerated", lineterm="", n=0))


def must_fire(fresh: str) -> list[str]:
    """The check is shown able to fail before it is trusted to pass."""
    failed = []
    # 1. A tampered figure in a published row.
    target = next(line for line in fresh.splitlines() if line.startswith("| P1 |"))
    tampered = fresh.replace(target, target.replace("silent loss 0", "silent loss 9", 1), 1)
    if tampered == fresh or not differs(tampered, fresh):
        failed.append("a tampered P1 row was not reported as a difference")
    # 2. A tampered evidence level.
    tampered = fresh.replace(target, target.replace("**raw**", "**scores**", 1), 1)
    if tampered == fresh or not differs(tampered, fresh):
        failed.append("a tampered evidence level was not reported as a difference")
    # 3. A row naming raw evidence that is not tracked.
    probe = Row("Z1", "X", ("gpt-oss:120b",), POD, "probe", "1", "frozen", "-",
                ("n/a",) * 6, "-", raw=("arms/no-such-directory/*.md",))
    found: list[str] = []
    evidence_level(probe, tracked(), found)
    if not found:
        failed.append("a row naming untracked raw evidence was not refused")
    # 4. The untouched text passes.
    if differs(fresh, fresh):
        failed.append("the untouched text was reported as different")
    return failed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true", help=f"write {OUT.relative_to(ROOT)}")
    ap.add_argument("--check", action="store_true",
                    help="run the must-fire probes, then fail if the committed file differs")
    args = ap.parse_args(argv)

    # A published copy withholds `paper/` whole, and a third of the rows are
    # read from its graded records, so the matrix can be neither regenerated
    # nor compared there. Said, and declined, rather than crashing on the
    # first missing record or passing over rows it never rebuilt.
    if not RECORDS.is_dir():
        print(f"UNMEASURED: {RECORDS.relative_to(ROOT)}/ is not in this copy, so "
              f"{OUT.relative_to(ROOT)} cannot be regenerated or checked here")
        return UNMEASURED_EXIT if args.check else 1

    fresh, problems, all_rows = build()
    if problems:
        for p in problems:
            print(f"benchmark_matrix: {p}", file=sys.stderr)
        return 1
    if args.write:
        OUT.write_text(fresh + "\n", encoding="utf-8")
        print(f"benchmark_matrix: wrote {OUT.relative_to(ROOT)} ({len(all_rows)} rows)")
        return 0
    if args.check:
        failed = must_fire(fresh)
        if failed:
            for f in failed:
                print(f"benchmark_matrix: must-fire probe failed: {f}", file=sys.stderr)
            return 1
        if not OUT.is_file():
            print(f"benchmark_matrix: {OUT.relative_to(ROOT)} is missing; run --write",
                  file=sys.stderr)
            return 1
        diff = differs(OUT.read_text(encoding="utf-8").rstrip("\n"), fresh)
        if diff:
            print(f"benchmark_matrix: {OUT.relative_to(ROOT)} differs from a fresh "
                  f"generation ({len(diff)} diff lines); rerun with --write if the "
                  f"evidence moved on purpose", file=sys.stderr)
            print("\n".join(diff[:40]), file=sys.stderr)
            return 1
        print(f"benchmark_matrix: clean -- {len(all_rows)} run groups re-derived from "
              f"committed records, 3 must-fire probes fired and 1 must-pass held")
        for sub in ("", "m7"):
            reason = stale_corpus.deferred_reason(CASSETTES / sub, "verify")
            if reason:
                print(f"UNMEASURED: C1's verify replay -- {reason}")
        return 0
    print(fresh)
    return 0


if __name__ == "__main__":
    sys.exit(main())
