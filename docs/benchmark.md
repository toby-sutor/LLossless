# The benchmark

Every LLossless run produces a report that says, with evidence, what a model dropped, changed or made up while merging. Most of those figures are computed from text by code, not by asking a model, so the same documents can be run through several models and the results compared on the same terms. This page explains how that comparison is set up: what is measured, how to read a result row, the rules that keep it fair, and what it cannot tell you. The results themselves are in the README, under ["Results, 2026-09-27"](../README.md#results-2026-09-27).

## The release benchmark of 2026-09-27

**When it ran, and how big it was.** The cross-vendor release benchmark ran on 2026-09-27: 295 runs over five models, GPT-6 Sol, GPT-6 Luna, Opus 5.5, Sonnet 5 and Haiku 4.5. The two GPT models ran through the vendor's API, and the three Claude models through both the API and a Claude subscription, which makes eight result rows. Fable 5.1 ran on three documents only and is outside the main table. There were two model failures, both Haiku 4.5 (one per route).

**Where the results are.** The README has the table and the per-model notes. Everything behind them is in `arms/2026-09-27/lineup/`: [`REGISTRATION.md`](../arms/2026-09-27/lineup/REGISTRATION.md) is the registration written before the first call, [`figures.md`](../arms/2026-09-27/lineup/figures.md) holds the derived tables, and `cells/` holds the merged document and the report of every run. [`arms/README.md`](../arms/README.md) describes the layout.

**What was registered but not measured.** Gemini 3.8 Flash: during the run its free tier answered every call with "high demand".

**Where earlier runs are.** [`arms/BENCHMARK-MATRIX.md`](../arms/BENCHMARK-MATRIX.md) lists every measurement made before this one, each with its settings and the reasons it is not directly comparable with its neighbours. Read that file as a record of what was measured, not as a leaderboard.

## What it measures

Three test sets, all in this repository:

| set | what runs | what it measures |
|---|---|---|
| **Merge quality** | the nine document pairs in `tests/pairs/`, merged at `--fidelity high` with full verification | *silent loss*: source sentences missing from the merge that the merge did not declare; *deviations*: sentences lost, wrongly kept or repeated when the merge is held against a hand-written merge of the same pair (`ideal.md`) |
| **Detection** | the 13 pre-registered fixtures in `tests/fixtures/`, each a hand-written merge with a known defect or none, checked by `llossless verify` | planted defects found; findings that no answer key accounts for; exit codes matched |
| **Planted errors** | three document sets in `tests/handwritten/`, merged at `--fidelity open`: `voyager` and `bip39` have factual errors planted in them (44 and 14), and `mahjongg` has none and is the control | errors the merge corrects from what the model knows (`voyager`, `bip39`), and true facts it "corrects" wrongly (`mahjongg`) |

`tests/fixtures/` holds sixteen fixtures. All sixteen were run, and the detection figures count the thirteen that were registered in advance.

Silent loss and deviations are computed mechanically from the merged text and the merge's own records. No model judges them. A deviation count has two sides on purpose: a one-sided figure would rank a copy-everything merge first, because it cannot lose what the reference kept.

## How to read a result row

A row is one model on one route: the vendor's API, or a Claude subscription through the `claude` command line. The [README's table](../README.md#results-2026-09-27) shows these figures for each row, and explains them under "How to read the columns":

| column | what it counts | better is |
|---|---|---|
| Silent loss | source sentences missing from the merge and not declared, summed over the nine pairs | lower, and only 0 keeps a model in the ranking |
| Deviations per pair | sentences lost, wrongly kept or repeated against the hand-written merge, averaged over the pairs | lower; the mechanical union, a script with no model, scores 7.78 |
| Planted errors fixed | how many of the 44 errors in `voyager` and the 14 in `bip39` the merge corrected, as the median of three runs | higher |
| $ per merge | the price of one merge with all its checks | lower |

Most pairs ran once. On six of the eight rows, three of the pairs ran three times, and for those the table counts the first run and [`figures.md`](../arms/2026-09-27/lineup/figures.md) shows the spread. A single run can move a model by several sentences, so treat a small difference between two rows as no difference.

## The fairness rules

- **Disqualify, then rank. Never a composite.** A model that loses content silently on any counted pair is disqualified before anything is ranked. The rest are ranked on quality (deviations per pair), and cost and then speed only break ties. A weighted score would let a cheap model buy back lost facts with its price, and that is the trade this tool exists to refuse.
- **The same work for everybody.** One pinned version of the tool, byte-identical input files whose hashes are recorded beside the registration (`run.json`), the same flags stated explicitly on every call, the same structured-output tier and one scorer for every model. No answer is shared between runs: a retried run may reuse only its own earlier answers, so nothing is paid twice. All rows ran in one session, and the models of a route took turns pair by pair, so a bad hour at a vendor hits its models alike.
- **Common pairs.** Every model is scored on every registered pair. A model that fails a pair keeps that failure as its own result ("exit 2 on 1 of 9") and is listed after the models that completed everything; its failure never removes the pair from anybody else's score.
- **Failures outside a model's control are not charged to it.** A blank answer, a timeout or a platform error is retried. If a run still fails, a cheap reference run is made against a second vendor. If that one works, the failure counts against the row as a failed endpoint. If it fails too, the fault is the infrastructure's: the run is repeated later and the failure is never scored. A refusal to do the task, whether from the prompt or a safety guardrail, is the model's own result and is flagged as one.
- **No model grades itself.** The merge scores are computed by code. Each model does run LLossless's own checks on its merge, but what its checker concludes cannot improve its score: a lost sentence that the tested model's own verifier confirmed as intentional forgives nothing, and is reported beside the score, not subtracted from it.
- **Thinking is configuration, not something that is compared.** Every model ran with reasoning on for all three roles. The API rows ran at the vendor's default reasoning effort and the subscription rows at `medium`; Haiku 4.5 has one level. The setting is in the registration, and reasoning is never switched off to make a model cheaper.
- **Baselines with no model in them.** Three texts are scored with the same scorer: the two sources concatenated, a mechanical union (one source, then every paragraph of the other that it does not already contain), and one source alone. A model whose deviations are not below the mechanical union's is flagged "no better than a mechanical union" beside its rank.
- **Registered before it runs.** The lineup, the settings, the rules for failures and the spending caps are written into a registration file whose hash is recorded before the first call. Corrections afterwards are dated amendments below the original text, never edits.

## Cost as one comparable figure

The headline cost is the vendor's list price per merge, the checks included, read on the day of the run. A subscription route has no per-call price, so its cost is shown as the API-equivalent figure its own CLI reports, labelled as such, and never as a price or as zero.

## What it cannot tell you

This is a small benchmark: nine pairs, thirteen fixtures, two planted-error documents and one control, mostly English, most of them run once. A difference smaller than the spread between runs is reported as no difference. The result is a dated snapshot of what each model did on this task, and a model released after the lineup is frozen goes into the next snapshot.

## The earlier specification

[`bench-spec.md`](bench-spec.md) is an older rule set, version 1.0.0, frozen on 2026-08-30. It governed the study of three open-weight models in August and September 2026, whose raw outputs are in `arms/2026-08-30/` and `arms/2026-09-03/`, and `tests/run_bench.py` still reads its property registry. The release benchmark of 2026-09-27 was not scored under it. Its rules are the ones on this page, and its registration is [`arms/2026-09-27/lineup/REGISTRATION.md`](../arms/2026-09-27/lineup/REGISTRATION.md).
