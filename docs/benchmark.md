# The benchmark

LLossless is also an instrument. Every run produces a report that says, with evidence, what a model dropped, changed or made up while merging, and most of those figures are computed from text by code rather than by asking a model. That makes it possible to run the same merges through several models and compare them on the same terms. This page describes how that comparison is set up: what is measured, the rules that keep it fair, and what it cannot tell you. Read it to know what a row in the README's results table means.

**Results, 2026-09-27.** The cross-vendor release benchmark ran on 2026-09-27: 295 runs, two model failures, both Haiku 4.5 (one per route). Every report and the derived figures are in [`arms/2026-09-27/lineup/figures.md`](../arms/2026-09-27/lineup/figures.md); the README's "Results, 2026-09-27" section under "Which model to use" carries the table and the per-model notes. Gemini 3.8 Flash was registered but not measured: its free tier answered "high demand" throughout. Earlier runs remain in [`arms/BENCHMARK-MATRIX.md`](../arms/BENCHMARK-MATRIX.md), each with its settings and the reasons it is not directly comparable with its neighbours. Read that file as a record of what was measured, not as a leaderboard.

## What it measures

Three test sets, all in this repository:

| set | what runs | what it measures |
|---|---|---|
| **Merge quality** | the nine document pairs in `tests/pairs/`, merged at `--fidelity high` with full verification | *silent loss*: source content missing from the merge that the merge did not declare; *deviations*: content lost, added or duplicated against a hand-written ideal merge of the pair (`ideal.md`), counted in both directions |
| **Detection** | the 13 pre-registered fixtures in `tests/fixtures/`, each a hand-written merge with a known defect or none, checked by `llossless verify` | planted defects found, per direction; correct statements wrongly flagged; exit codes matched |
| **Planted errors** | two documents with factual errors planted in them (`tests/handwritten/`), plus a clean control document | errors the merge corrects from what the model knows, and true facts it "corrects" wrongly |

Silent loss and deviations are computed mechanically from the merged text and the merge's own declarations. No model judges them. A deviation count has two sides on purpose: a one-sided figure would rank a copy-everything merge first, because it cannot lose what the reference kept.

## The fairness rules

- **Disqualify, then rank. Never a composite.** A model that loses content silently on any counted pair is disqualified before anything is ranked. The rest are ranked on quality (deviations per pair), and cost and then speed only break ties. A weighted score would let a cheap model buy back lost facts with its price, and that is the trade this tool exists to refuse.
- **The same work for everybody.** One pinned tool commit, byte-identical input files whose hashes are written into the registration, the same flags stated explicitly on every call, the same structured-output mode and one scorer version for every model. No answer is shared between runs: a retried run may reuse only its own earlier live answers, so nothing is paid twice. The runs happen inside one short window, interleaved pair by pair, so a bad afternoon hits every model equally.
- **Common pairs.** Every model is scored on every registered pair. A model that fails a pair keeps that failure as its own result ("exit 2 on 1 of 9") and is listed after the models that completed everything; its failure never removes the pair from anybody else's score.
- **Failures outside a model's control are not charged to it.** A timeout, a server error or a rate limit is retried; a cell that still fails is checked against a second vendor, and if that fails too the fault is the infrastructure's and is never scored. A refusal to do the task, whether from the prompt or a safety guardrail, is the model's own result and is flagged as one.
- **No model grades itself.** The merge scores need no model at all. Where a check does need one, a candidate is never its own judge, and a lost segment that the tested model's own verifier confirmed as intentional forgives nothing: it is reported beside the score, not subtracted from it.
- **Thinking is configuration, not an axis.** Every frontier model runs at its own default reasoning setting and the setting is documented; reasoning is never switched off to make a model cheaper.
- **Baselines with no model in them.** Three texts are scored with the same scorer: the two sources concatenated, a mechanical union (one source, then every paragraph of the other that it does not already contain), and one source alone. A model whose deviations are not below the mechanical union's is flagged "no better than a mechanical union" beside its rank.
- **Registered before it runs.** The lineup, the settings and the predictions are written into a registration file whose hash is recorded before the first call. Corrections afterwards are dated amendments, never edits. A prediction names a property ("model A loses no content"), not a number, so the result cannot be fitted to it afterwards.

## Cost as one comparable figure

The headline cost is the vendor's list price per merge, the checks included, read on the day of the run. A subscription route has no per-call price, so its cost is shown as the API-equivalent figure its own CLI reports, labelled as such, and never as a price or as zero.

## What it is not

A small benchmark. Nine pairs, thirteen fixtures and three planted-error documents, mostly English, most cells one draw. A difference smaller than the spread between draws is reported as no difference. The result is a dated snapshot of what each model did on this task, and a model released after the lineup is frozen goes into the next snapshot.

## Earlier specification

[`bench-spec.md`](bench-spec.md) is the first frozen benchmark specification, version 1.0.0 of 2026-08-30, and the property registry that `tests/run_bench.py` reads. It fixes the judge-free and judge-dependent split this page relies on.
