# The benchmark evidence

This directory holds every recorded benchmark run: the document each model wrote, the report LLossless made about it, and the scores computed from those files. Use it to check a published figure against the files it came from, or to read what a model did on a test document. The README's results table and the model scorecard in the web interface are computed from this directory by scripts under `tests/`, and each script can re-derive its figures offline.

> **In short**
>
> - **The evidence for the README's results table** is in [`2026-09-27/lineup/`](2026-09-27/lineup/). Start with [`figures.md`](2026-09-27/lineup/figures.md).
> - **To check a figure**, run the script for its run with `--check`. It needs no model and no network. See [Checking a figure](#checking-a-figure).
> - **Every other dated directory is an earlier run**, kept as history. [Earlier runs](#earlier-runs-newest-first) says what each one is and whether a published figure still rests on it.
> - **You can re-score these runs, but you cannot replay them.** They were made against live models, so repeating one needs that model and gives a new sample.

Three terms recur. A *row* (in older runs, an *arm*) is one model configuration under test. A *draw* is one run of it. A *cell* is one row on one test document.

Every run took published inputs: the pairs in `tests/pairs/`, the fixtures in `tests/fixtures/`, or the document sets in `tests/handwritten/`.

- [The release benchmark, 2026-09-27](#the-release-benchmark-2026-09-27)
- [Checking a figure](#checking-a-figure)
- [Earlier runs, newest first](#earlier-runs-newest-first)
- [What a run directory holds](#what-a-run-directory-holds)
- [What is not here](#what-is-not-here)
- [What was redacted](#what-was-redacted)
- [Licence](#licence)

## The release benchmark, 2026-09-27

This is the run behind the README's results table: nine rows and 295 runs, made with one pinned version of the tool in one session that started on 2026-09-27 and ended shortly after midnight UTC. [The benchmark](../docs/benchmark.md) explains the rules it was scored under.

| Path under `2026-09-27/lineup/` | What it is |
|---|---|
| `REGISTRATION.md` | The lineup, the settings, the rules for failures and the spending caps, written before the first call. Two dated amendments follow the original text. It holds no predictions. |
| `run.json` | The hashes of the input files and the prompts, written at the first start. |
| `cells.jsonl` | The runner's log: a `begin` and an `end` line for each run, and the runner's own events. |
| `scored.json` | One scored record per run, 295 in all. |
| `figures.md`, `figures.json` | The tables derived from `scored.json`. The README's results table is taken from them. |
| `cells/<row>/<set>/<item>/d<n>/a1/` | One directory per run. `d<n>` is the draw. See [What a run directory holds](#what-a-run-directory-holds). |
| `lane-*.log`, `*.pid`, `sub-then-fable.*`, `prompts-observed.json` | The runner's console logs, its process ids and launch script, and the prompt hashes it saw during the run. |

**The rows.** `gpt-6-sol-api` and `gpt-6-luna-api` ran through the vendor's API. `opus-5.5`, `sonnet-5` and `haiku-4.5` each ran twice, as `-api` and as `-sub` (a Claude subscription through the `claude` command line). Those are the eight rows of the README's table. The ninth, `fable-sub`, is Fable 5.1 on three documents and is outside that table.

**The sets.**

| Set | Input | Runs per row |
|---|---|---|
| `S1` | The nine pairs in `tests/pairs/`, merged at `--fidelity high`. | 15: one draw of each pair, and two more of `badge_access`, `trace_names` and `rate_limits`. `sonnet-5-api` and `haiku-4.5-api` ran one draw of every pair, so 9. |
| `S2` | The sixteen fixtures in `tests/fixtures/`, checked with `llossless verify`. | 16. The detection figures count the thirteen fixtures that were registered in advance. |
| `S3` | `voyager`, `bip39` and `mahjongg` in `tests/handwritten/`, merged at `--fidelity open`. | 7: three draws of `voyager` and three of `bip39`, which carry planted errors, and one of `mahjongg`, the control that carries none. |

That makes 38 runs for six rows, 32 for two, and 3 for `fable-sub` (`index_429` and `rate_limits` of `S1`, `voyager` of `S3`).

**The two failures.** `haiku-4.5-api` on `bike_docks` and `haiku-4.5-sub` on `mahjongg` ended as model failures. Both directories are kept. The second is the one run without a `merged.md`.

**The pilot.** `2026-09-27/lineup-pilot/` holds the 25 runs that tested the runner before the counted run, in the same layout, with a `PILOT-REPORT.md`. No published figure uses it.

## Checking a figure

Each command below runs offline from the repository root. It re-derives the scores from the run's files, compares them with the committed figures, and exits 1 on any difference.

| Published figure | Evidence | Command |
|---|---|---|
| The README's results table. In the web scorecard: GPT-6 Sol, GPT-6 Luna, Claude Opus 5.5, Claude Sonnet 5, Claude Haiku 4.5 and the four subscription routes. | `2026-09-27/lineup/` | `python3 tests/lineup_figures.py --check` |
| Scorecard: GPT-5.6 Terra | `2026-09-18/matrix/` | `python3 tests/matrix_figures.py --check` |
| Scorecard: Gemini 3.5 Flash-Lite | `2026-09-25/google/` | `python3 tests/google_figures.py --check` |
| Scorecard: Qwen3 8B and Qwen3.8 27B | `2026-09-16/phase4/` | `python3 tests/phase4_figures.py --check` |
| Merge-effort figures of the Sonnet 5 and Haiku 4.5 subscription routes | `2026-09-25/subscription-comparison/` | `python3 tests/effort_figures.py --check` |
| Merge-effort figures of the Opus 5.5 subscription route | `2026-09-26/opus-max/` | `python3 tests/opus55_effort_figures.py --check` |
| The `mahjongg` false-correction counts of those two runs | both | `python3 tests/mahjongg_figures.py --check` |
| Verification-depth figures (the `verify_depth` block of `src/llossless/web/catalogue.json`) | `2026-09-24/depth/` | `python3 tests/depth_figures.py --check` |

The scorecard and the merge-effort figures are read from `src/llossless/web/catalogue.json`; the web interface shows them.

**From a figure to its files.** Each record in `scored.json` names its row, set, pair and draw, which together are the path of its run directory under `cells/`. For example, the README gives GPT-6 Sol 4.11 deviations per pair. That is 37 deviations over nine pairs: the sum of `lost`, `bloat` and `dup` over the nine first-draw `S1` records of `gpt-6-sol-api`.

**Planted-error counts can be re-scored one draw at a time.** `python3 tests/score_planted.py --pair voyager <run directory>/merged.md` prints how many of the planted errors that merge fixed, kept or left in another state (`--pair bip39` for the other document, `--pair mahjongg --control` for the control). The two merge-effort checks do not do this for `voyager` and `bip39`: they take those outcomes from `scored.json` as given, and print a line starting `UNMEASURED` to say so.

**Two checks also read the paper's graded records.** `python3 tests/benchmark_matrix.py --check` rebuilds the benchmark matrix and compares it with [`BENCHMARK-MATRIX.md`](BENCHMARK-MATRIX.md). `python3 tests/annotate_merges.py --check` rebuilds the seven pages in `annotated/` and compares them. Both read the graded records in `paper/records/` as well as this directory. In a copy made without those records, the first prints `UNMEASURED` and exits 3, and the second checks the three merge pages and reports the three detection pages and the index as `UNMEASURED`.

## Earlier runs, newest first

These runs are kept as history. Each was scored under the rules of its day, so rows from different runs are not directly comparable.

[`BENCHMARK-MATRIX.md`](BENCHMARK-MATRIX.md) lists every measurement made up to 2026-09-26, 65 run groups, each with its settings, its headline figures and the reason it cannot be set beside its neighbours. The release benchmark is not in it, and its status column describes the day it was generated: a row marked `current` there may have been replaced by the release benchmark since. The file is generated by `tests/benchmark_matrix.py`; do not edit it by hand. The ids below (`P9`, `H1`, ...) are its row ids.

| Directory | What ran | On what | Runs | Published figure that rests on it | Script under `tests/` whose `--check` re-derives it |
|---|---|---|---|---|---|
| `2026-09-26/opus-max/` | Opus 5.5 by subscription at `sourced`, merge effort `xhigh` and `max` | `voyager`, `mahjongg` | 6 | Merge-effort figures of the Opus 5.5 subscription route | `opus55_effort_figures.py`, `mahjongg_figures.py` |
| `2026-09-26/safemode-spot/` | Sonnet 5 and Haiku 4.5 by subscription, repeated in safe mode | 3 of the nine pairs at `high`, `voyager` at `sourced` | 10, and 3 diagnostic | None | None |
| `2026-09-26/sourced-2183/` | Probes and replays on three versions of the `claude` command line | One captured merge prompt | Not scored | None | None |
| `2026-09-26/sourced-fix/` | Sonnet 5, Opus 5.5 and Haiku 4.5 by subscription at `sourced`, after a prompt change | `voyager`, `bip39` | 4 | None | None. `score_planted.py` scores one merge. |
| `2026-09-25/subscription-comparison/` | The `opus`, `sonnet` and `haiku` subscription routes at `sourced`, merge effort `low` to `xhigh` | `voyager`, `bip39`, `mahjongg` | 60 draws, 61 attempts | Merge-effort figures of the Sonnet 5 and Haiku 4.5 subscription routes | `effort_figures.py`, `mahjongg_figures.py` |
| `2026-09-25/vendor/` | GPT-6 Sol, GPT-6 Luna and Opus 5.5 by API | The nine pairs at `high` | 27, and 3 probes and 3 refused cells | None since the release benchmark | `vendor_figures.py` |
| `2026-09-25/google/` | Gemini 3.5 Flash-Lite on the free tier | The nine pairs at `high` | 9, of which 8 completed, and 1 probe | Scorecard row for Gemini 3.5 Flash-Lite | `google_figures.py` |
| `2026-09-24/subscription/` | The `haiku`, `sonnet` and `opus` subscription routes | The nine pairs at `high` | 27 | None since the release benchmark | `subscription_figures.py` |
| `2026-09-24/depth/` | `llossless verify` at depth `full` and `coverage`, Qwen3.8 27B | 13 fixtures | 26 | Verification-depth figures | `depth_figures.py` |
| `2026-09-18/matrix/` | Opus 5, Sonnet 5, Haiku 4.5 and GPT-5.6 Terra by API | The nine pairs at `high` | 36 | Scorecard row for GPT-5.6 Terra | `matrix_figures.py` |
| `2026-09-17/` and `2026-09-18/gaps/` | The same four models by API | Pairs from `tests/handwritten/` | 34 cell directories and 1 | None | None |
| `2026-09-16/phase4/` | qwen3:8b and Qwen3.8 27B on a rented endpoint | Three pairs from `tests/handwritten/` at `low` and `high` | 12 | Scorecard rows for Qwen3 8B and Qwen3.8 27B | `phase4_figures.py` |
| `2026-09-03/` | Detection by three open-weight models | 13 fixtures | 39 | None | None |
| `2026-08-30/` | Merges by the same three models | `tests/pairs/index_429` at fidelity `off` | 25 draws | None. `annotated/` shows the merges as readable pages. | `annotate_merges.py`, for the three merge pages |

The two merge-effort scripts take the `voyager` and `bip39` outcomes as given: see [Checking a figure](#checking-a-figure).

Runs from 2026-09-24 on carry a `REGISTRATION.md`, written before the first call, that names the version of the tool and the settings; corrections are dated amendments below the original text. `sourced-2183` and `sourced-fix` are diagnostics and have none.

### 2026-09-26

**`opus-max/`** (matrix row E5). `REGISTRATION.md`, `results.json` (one row per run), `scored.json` (each run scored), `tables.md`, and `runs/d<n>/<pair>-<effort>/a1/`. Two draws of `voyager` at `xhigh`, three at `max`, and one of the `mahjongg` control at `max`. Every run used version 2.1.281 of the `claude` command line, because the installed 2.1.274 refused the model: `probe-2.1.274/` holds that refusal and `probe/` the accepted call.

**`safemode-spot/`**. Safe mode runs `claude` without the user's own instructions, skills and tools; the subscription runs of 2026-09-24 and 2026-09-25 did not use it. This check repeats three pairs of the 2026-09-24 Sonnet and Haiku rows in safe mode (`runs/A-*`), and two draws of the 2026-09-25 Sonnet `voyager` cell at `sourced` (`runs/B-*`). Each of those two draws was attempted twice (`a1`, `a2`) and all four attempts exited 2. `tables.md` compares old and new. `diag/` holds three further runs that vary the command-line version and safe mode, and a web-search probe.

**`sourced-2183/`**. The diagnosis of why Sonnet 5 stopped looking facts up at `sourced` on version 2.1.283 of the command line. `cap/` holds one captured command and merge prompt, `replay/` that prompt replayed per version and model, `init/`, `probe/` and `sysprobe/` the start-up records and probes per version, `order/` runs that vary the field order of the verify prompt, and `full-283/` one full run. Nothing here is scored.

**`sourced-fix/`**. `prompt-round1.diff` is the change to the two `sourced` prompt files that followed from that diagnosis, and `runs/r1/` holds four runs made with it: two of Sonnet 5 and one of Opus 5.5 on `voyager`, one of Haiku 4.5 on `bip39`. `scored.json` holds the counts `tests/score_planted.py` gives.

### 2026-09-25

**`subscription-comparison/`** (E1 to E3). `REGISTRATION.md`, `results.json` (one row per attempt), `scored.json` (one record per counted draw), `tables.md`, and `runs/d<n>/<pair>-<model>-<effort>/a<n>/`. Three draws of each cell: `opus` and `sonnet` at four effort levels on `voyager` and `bip39` and at `medium` on `mahjongg`, `haiku` at `medium` on `voyager` and `bip39`. On that day the `opus` alias answered as Claude Opus 5, not Opus 5.5.

**`vendor/`** (P1 to P4). `REGISTRATION.md`, `results_<model>.json`, `scored.json`, `ledger_<vendor>.json` (every paid call, probes included) and `cells/<pair>-high-<model>-d1/`. One draw per pair and model. The three `claude-opus-5` cells hold no report: that model refused every merge call, and each directory keeps the console output and the rejected answers as the evidence. `diag/` holds the request bodies that isolated the refusal. One `trace_names` attempt of GPT-6 Sol was interrupted and left no directory; it has a row in `results_gpt-6-sol.json` and a record in `scored.json`, marked `interrupted`.

**`google/`** (P5). The same layout. Gemini 3.5 Flash-Lite completed eight of the nine pairs; `freezer_alarm` exited 2. The run was paced to stay inside the free tier, and `REGISTRATION.md` and its amendments say how far it got. Gemini 3.8 Flash was registered and produced no cell.

### 2026-09-24

**`subscription/`** (P6 to P8). `REGISTRATION.md`, `results.json`, `scored.json`, and one directory per cell, `<pair>-high-claude-<alias>/`. One draw each. `RESOLVED.json` and `haiku.json`, `sonnet.json`, `opus.json` record which model answered each alias: `opus` answered as Claude Opus 5.

**`depth/`** (D1, D2). `r1/full` and `r1/coverage` are the two run records with the scores the run printed, and `r1/<depth>-reports/` holds the thirteen per-fixture reports of each. `regraded/<depth>.json` scores the same reports under the current rule, which does not count a second report of a detected plant as an invented finding. The published figures use `regraded/`. `python3 tests/run_detect.py --regrade arms/2026-09-24/depth/r1 --out <dir>` writes it again.

### 2026-09-16 to 18

Each is the run directory as its runner wrote it: one `<pair>-<fidelity>-<model>/` per cell, one or more `results*.json` with a row per attempt, the runner script and its log.

| Directory | Matrix rows | Contents |
|---|---|---|
| `2026-09-18/matrix/` | P9 to P12 | 36 cells. `scored.json` has 59 records: 23 earlier attempts are kept and marked `superseded`. |
| `2026-09-18/gaps/` | the fourth cell of H9 | GPT-5.6 Terra on `toby-test-1`. |
| `2026-09-17/ladder-high/` | H6, H7 | Opus 5 and Sonnet 5 at `high` on four pairs from `tests/handwritten/`: 8 cells. |
| `2026-09-17/frontier-thinking/` | H3, H4, and the `high` cells of H8, H9 | Haiku 4.5 and GPT-5.6 Terra with reasoning on: 12 cells. |
| `2026-09-17/frontier/` | H5 | Void: every model was told not to reason. Stopped after 13 of 24 planned cells. |
| `2026-09-16/phase4/` | H1, H2 | 12 cells, 11 with a report. |

These runs name the pairs from `tests/handwritten/` as the corpus was named then. `toby-test-1` is `tests/handwritten/birthday/`, `toby-test-2` is `chickens/`, `toby-test-4` is `christianity/` and `toby-test-5` is `curry/`. The copies of the sources in the cell directories are byte-identical to the tracked ones, and each pair's `meta.json` names the original files. Each merge is scored against that pair's `reference.md`.

### 2026-09-03

`<arm>/detect-reports/` holds thirteen per-fixture reports for each of three arms: `A-27b` (`qwen3.8:27b`), `B-70b` (`deepseek-r1:70b`) and `C-120b` (`gpt-oss:120b`). Matrix rows D12 to D14. Only the reports are here; their scores are the graded records `detect-2026-09-03-<arm>.json` in `paper/records/`.

### 2026-08-30

The merges of the same three models on one pair, `tests/pairs/index_429`. Matrix rows I1 to I4 and I6 to I10. One directory per draw, named `<arm>-<size>-<mode>[-d<n>]`: `A`, `B` and `C` are the three models. `1` (`default`) asks for reasoning in the merge step only, which was the tool's default then, and `2` (`think`) asks for it in all three steps.

| Directory | Files | Draws |
|---|---|---|
| `2026-08-30/k3/` | 93 | A and B arms, 3 draws each (12 draw dirs) |
| `2026-08-30/k5c/` | 136 | C arms, 5 draws each (10 draw dirs), and two `discarded-*/` directories |
| `2026-08-30/2c/` | 33 | one draw of A1, B1 and C2 (3 draw dirs) |

Each block also holds its runner scripts, its logs and a `graded.json` with one record per arm, numbers only.

**`C1`'s five draws have no `merged.md` and no `report.json`.** `C1` is `gpt-oss:120b` at the default. All five draws stopped at the first step, which ran with reasoning off: the endpoint answered 200 with an empty body three times, so no merge was attempted. That is the arm's result, and it is reported as unmeasurable, not as a score. `C2`, the same model with reasoning in every step, completed all five.

**`k5c/discarded-*/`** are draws that were taken and set aside, kept so that a discarded draw leaves a trace. `discarded-pre-2bbd02f/` holds one draw whose console output named the endpoint's address. `discarded-no-cache-absent/` holds six draws from a session in which one draw was answered from the response cache.

**`merged_bytes` in `graded.json` counts characters, not bytes.** For `C2-120b-think` in `k5c/graded.json` it reads 5690, and every `merged.md` of that arm is 5692 bytes: the merge holds one three-byte character. The benchmark matrix lists the same 5690 as an evidence gap of row I10.

## What a run directory holds

| File | What it is |
|---|---|
| `merged.md` | The document the model produced. |
| `report.json` | The tool's full machine-readable report for that run. [Reading the report](../docs/report.md) explains it. |
| `report.md` | The same report as a person reads it. |
| `stderr.log` | The run's console output. `stderr.txt` and `stdout.txt` in the oldest runs. |
| `argv.json` | The command line the run used. |
| `calls.json`, or a `calls/` directory | Subscription runs only: for each call to the `claude` command line, its arguments and the envelope it returned (tokens, model ids, turns, API-equivalent cost). In `calls.json` the answer text is left out, because it is in `merged.md` and `report.json`. |
| `env_names.json` | The names, never the values, of the environment variables the run saw (release benchmark). |
| `source_a.md`, `source_b.md`, ... | A copy of the inputs, where the runner kept one. |
| `discards/`, `failures/` | The raw answers the tool rejected, in a run that failed. |
| `window.json` | The context window the endpoint served, probed before the run (2026-08-30). |
| `ps-before.json`, `ps-after.json` | The endpoint's table of loaded models before and after the run (2026-08-30). |
| `cache-before.txt`, `cache-after.txt` | The state of the response cache before and after the run (`k5c`). |

**Older records carry the tool's earlier name.** Console output up to 2026-09-25 prints it, and the field `claimcheck_commit` keeps it in runs of every date. That field, a `COMMIT` file and the pin in a registration name the version of the tool the run used. They identify a commit of the development history, which is not part of the published repository, so they cannot be checked out here.

## What is not here

- **The graded records of the open-weight study.** The scores of the 2026-09-03 detection reports and of an earlier detection run, and the sweep and re-score records of the 2026-08-30 merges, are not in this directory. They are in `paper/records/`, beside the paper that cites them. The benchmark matrix names them as the score files of rows D6 to D14 and I5, and the two checks named under [Checking a figure](#checking-a-figure) read them.
- **The scorer's per-draw text output for the planted-error runs.** For `2026-09-25/subscription-comparison/`, `2026-09-26/opus-max/`, `safemode-spot/` and `sourced-fix/`, the scripts that ran the scorer over every draw are withheld with what they wrote, which for the first two includes their own copies of `results.json`, `scored.json` and `tables.md`. That output quotes, draw by draw, the planted wording each merge was scored on and the `mahjongg` sentences behind its false corrections. It is withheld so that this release does not carry a ready-made list of the planted errors. The copies here carry the counts and each error's outcome by number. The scorer itself, `tests/score_planted.py`, is published.
- **What is not run output.** The pinned copies of the tool, the binaries of the `claude` command line (227 MB) and the text extracted from them for the `sourced-2183` diagnosis (155 MB).
- **Runs whose output was never kept.** The "Evidence gaps" section of [`BENCHMARK-MATRIX.md`](BENCHMARK-MATRIX.md) lists every measurement whose raw output is missing, and says why.

## What was redacted

Every file passed through one scrub on the way in, `scrub` in `scripts/stream_redact.py`. It only ever replaces text with one of two markers.

**`<home>` stands for a home directory path.** It appears wherever a file recorded an absolute path, which includes every `report.json`.

**`<redacted>` stands for an address or a credential shape that the release scan refuses.** It appears in these places:

| Where | What it replaces |
|---|---|
| 21 of the 262 files of `2026-08-30/`: 13 in `k3`, 6 in `2c`, and in `k5c` `assert_draw.py` and the `stderr.log` under `discarded-pre-2bbd02f/` | The address of the rented machine. An early version of the console banner printed it in the first line, and the window probe repeated it. |
| `k3/run_arm.sh`, `k5c/run_arm.sh` and `2026-09-16/phase4/run_matrix.py` | The name of the company the hardware was rented from. The two `run_arm.sh` files export an endpoint label (`CLAIMCHECK_ENDPOINT_LABEL`, the variable's name at the time) that now reads `<redacted>-2026-08-30` and `<redacted>-2026-08-31`. |
| 18 `report.json` of the `sourced` runs (10 in `subscription-comparison`, 6 in `opus-max`, 2 in `sourced-fix`), and the 8 `report.md` beside the last two groups | Web addresses the model cited as its source for a correction. |
| Probe and replay outputs under `safemode-spot/diag/` and `sourced-2183/`, `pilot/pilot_state.json` and `selftest_retry.py` of `2026-09-25/google/`, and one line of the release registration and of the pilot's | Web addresses in search results, in a vendor's error messages and in a documentation link. |

**No `merged.md` was changed.** None of them holds either marker.

**A `report.json` was changed in three ways.** Home paths read `<home>`. The 18 reports above have web addresses replaced. The reports of `2026-09-16/phase4/` and `2026-09-24/depth/`, the two runs on a rented serverless endpoint, have `provenance.endpoint` removed; in those runs `endpoint_id` is also null in every row of `phase4/results.json`, and `harvest.endpoint` in every record of the depth run.

**Two things were dropped.** The `rate_limit_event` lines of the stream output in `sourced-2183/`, and the answer text in `calls.json` (see [What a run directory holds](#what-a-run-directory-holds)).

**Scripts and logs were scrubbed like everything else.** A path inside a runner script reads `<home>`, so the script documents how the run was made and will not run as it stands. Paths in a run's log still name the scratch directory the run was written to. Where a run directory has a `build_evidence.py`, that is the script that made this copy, and it states what it left out.

**To check that nothing slipped through:**

    python3 scripts/build_arm_bundle.py --check arms

It refuses if any file carries an address, a credential shape or a compute provider's name. `--self-test` plants one of each into a temporary copy and requires the refusal, so a clean result comes from a check that has been shown to fire. The detector for the provider's name is not published, because it has to contain the name. A copy without it runs the other four detectors and says in its output that the fifth did not run.

## Licence

The contents of this directory are published under **CC BY 4.0** (<https://creativecommons.org/licenses/by/4.0/>), with one exception. The code in this repository is under the Elastic License 2.0; see `LICENSE` at the root.

**The exception: every run directory for the `mahjongg` set is under CC BY-SA 4.0** (<https://creativecommons.org/licenses/by-sa/4.0/>). That set is adapted from the German Wikipedia article "Mah-Jongg", and a model's merge of it, with the reports that quote it, is an adaptation of the same text. Anything built from those files must credit the Wikipedia contributors and carry the same licence. The directories are `2026-09-25/subscription-comparison/runs/d<n>/mahjongg-<model>-<effort>/`, `2026-09-26/opus-max/runs/d<n>/mahjongg-<effort>/` and `2026-09-27/lineup/cells/<row>/S3/mahjongg/`; [`LICENSE-CC-BY-SA`](LICENSE-CC-BY-SA) has the details.

The outputs under `2026-08-30/`, `2026-09-03/`, `2026-09-16/` and `2026-09-24/depth/` were produced by open-weight models on rented hardware. The other directories hold the output of vendor models, obtained through their APIs and through a subscription.
