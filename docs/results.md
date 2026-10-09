# Measured results

This page reports how well LLossless's own checks worked on sixteen small test cases written for the project (two short source documents and a merge each, several with defects planted on purpose), run with one open-weight model, Qwen3.8 27B, and recorded so that anyone can replay them. It does not compare models: for which model to use, see the README's [results of 2026-09-27](../README.md#results-2026-09-27) and [The benchmark](benchmark.md). The short answer is that the checks' evidence is real, they found nothing invented, and they repeat, but the headline coverage figure cannot tell a real merge from two documents stapled together, and the test set is too small to predict how the tool will do on your documents.

> **In short**
>
> - **Findings can be checked by hand.** Of 327 verdicts whose evidence was graded, 324 quote evidence that is really in the file it names.
> - **Nothing invented was found.** The reverse check found no claim in the model's merges without support in a source, 0 of 441.
> - **Verdicts repeat.** Three runs of the same check gave the same answer on all 164 test statements.
> - **Coverage is 87%, and not on its own a quality score.** At the default settings, forward coverage is 314 of 363 source claims. It rewards keeping content, so two sources stapled together would score perfectly. [See below](#the-number-not-to-quote-alone).
> - **The test set is small.** Sixteen small test cases, written inside this project and checked with one model, show that the pipeline works end to end. They do not predict results on documents the tool has never seen.

## The figures

| Figure | Value | What it tells you |
|---|---|---|
| Forward coverage, thinking off | **314/363** (87%) | How much of the sources survived into the model's merges, as the checker judged it. Part of the gap is expected: where two sources conflict, a merge keeps one value and drops the other. It does not say the merge is good; see the next section. |
| Evidence grounded | **324/327** (99%) | Whether a finding can be checked by hand. Every verdict must quote its evidence, and almost every quote is really in the file it names. |
| Reverse pass - claims in neither source | **0** of 441 extracted | Whether the merges added anything. No claim in the model's merges lacked support in a source. |
| Verify verdict stability across 3 runs | **164/164** (100%) | Whether the checking verdict repeats. Each test statement got the same verdict in every run. |
| Decompose probe stability across 3 runs | **164/164** (100%) | Whether the split into claims repeats. Each test statement was extracted, or missed, the same way in every run. |

A test statement (a "probe") is one statement in a test document whose correct verdict was written down before the run. The first four rows were recorded before the checking prompts changed on 2026-09-26: they are the figures as measured, but an offline replay against today's prompts cannot re-derive them and reports them as UNMEASURED until they are re-recorded. The last row still replays as printed.

## The number not to quote alone

The headline is 314/363, and on its own it says less than it seems. Forward coverage is a recall measure: it asks whether each source claim is somewhere in the merge. A document that staples source A to source B drops nothing, contradicts nothing and invents nothing, so it scores perfectly.

This happens in practice. In the recorded merges of an earlier, smaller model (`qwen3:8b`, in `tests/responses/m4/`), a similarity-ratio test finds that **14 of 66 eligible merges are concatenations**, across four fixtures (`tests/analyse_merges.py` prints the census). That is an undercount: the ratio only fires on a near-total copy, so it misses a merge that stapled the sources and then dropped things, which is the case worth catching. Counting how many contiguous blocks each merge falls into by source finds **23 of 66**, the ratio's fourteen plus nine partial concatenations (`tests/measure_merges.py` prints both counts). The counts leave out `disjoint_sources`, whose two sources share no subject and where stapling is the correct merge. Worse, the metric prefers the concatenation: on `dropped_claim`, the stapled document outscores the one that genuinely tried to merge.

What the tool does about it today: the report's Structure section prints how many contiguous runs the merge falls into by source, as a measurement rather than a finding, and a merge that keeps two sources' wordings of one fact gets a `duplicated_content` finding. A staple of two documents that share no sentences is still not failed on its shape alone: a check that fails a concatenation outright is planned and not built. Until it is, read the Structure section beside the coverage figure: one run per source means the sources were stapled together.

## Known limits

### Known limitation: claims coarsen as documents get longer

Measured over 80 documents from the recorded corpus on 2026-08-24: as documents get longer, each extracted claim carries more source text, **32, 45 and 48 bytes per claim** across three size bands, while the claims still cover about the same share of the document, **0.80, 0.80 and 0.75**, and their number rises from 4 to 8 to 12. The model keeps covering the document, in coarser units.

**The consequence is for the verification pass**, not for the extraction count: a claim that bundles three facts can be scored as covered by a merge that dropped one of them, and how often that hides a real loss has not been measured. The planned fix is a claim-atomicity check (one assertion per claim, with a claim that crosses a sentence boundary as the cheapest sign of a bundle), and **it is not built**; no threshold or expected result was changed because of this measurement. Until it exists, treat a clean result on a long document as weaker evidence than one on a short document.

### Known limitation: a document that is source code is treated as prose

On a pair of FizzBuzz programs, one C and one C++ (`tests/handwritten/fizzbuzz_c_cpp/`, measured 2026-09-20), the merge kept the C version, dropped the C++ one entirely and flattened the indentation (source indents `0, 0, 4, 8, 12, ...` came out as `0, 0, 1, 1, 1, ...`, four of sixteen lines unchanged), yet **the run exited 0 with 13/13 source claims accounted for.** The two programs make the same behavioural claims, so the loss was of form, which this tool does not check, and a code file is read as a title followed by sentences, so nothing protects its line breaks. The verbatim checks protect code only inside fenced blocks: a Markdown document with fenced code is the supported case, while a `.c` file, or a document that is nothing but unfenced code, is not protected. **Do not use this tool to merge source files.**

### Known limitation: unrelated documents are merged, not refused

LLossless does not check whether two documents are about the same subject, and it will merge a travelogue with a film essay if asked. That is deliberate: deciding that two documents do not belong together is an editorial judgement the tool cannot defend, so the decision is yours to make before running it. What it does is report: on `tests/handwritten/unrelated/` (a Japan travelogue against a Chaplin essay) at `high`, measured 2026-09-20, one document was dropped whole and the declared-loss check caught it, *17 declared drops of 78 source segments, over the 3% budget*, so the run failed loudly rather than quietly.

## Details for reviewers

### How the figures were produced

**The figures were measured by the test harnesses, not by the `llossless` command.** Every figure in the table comes from `tests/run_merge.py`, `tests/run_verify.py` and `tests/run_decompose.py` replaying the recorded corpus. The command runs the same three passes over the same prompts and is tested in `tests/test_cli.py`. `tests/run_detect.py` runs the installed command itself, as a subprocess, over thirteen of the sixteen fixtures: the thirteen that were registered in advance for the detection benchmark.

**Every row comes from one recording session**, 2026-09-24 to 25: one hosted endpoint serving `Qwen/Qwen3.8-27B-FP8` through vLLM, the sixteen fixtures in `tests/fixtures/`, three samples each, thinking off for every role and the structured-output tier pinned to `json_schema`. `Qwen/Qwen3.8-27B-FP8` is the full id of the Qwen3.8 27B model as it was served; under Ollama the same model is tagged `qwen3.8:27b`, and this section calls it "the 27B". That session recorded `tests/responses/` and `tests/responses/m7/` whole. The first three rows were measured against `prompts/merge.md` at `c33344d1450b`, the prompt's content digest (the first twelve hex characters of its SHA-256) that `tests/responses/m7/` was recorded against. The verify row covers 164 of the fixtures' 166 probes: on this model the first answer of the reverse check on `attribution_invented` was rejected by validation, and the retry kept generating until it was cut off in 7 of 8 attempts. The retry has no recording, so every replay reports the check's two probes UNMEASURED rather than counting them either way.

**The evidence base is sixteen fixtures written for this project, two models, three endpoints, three samples each.** All sixteen fixtures carry decompose, merge and verify recordings from the session above, except the one reverse call just named. One merged document, `restated`'s, is the real output of a run of the tool, where the others were written for their fixtures. The second model is `qwen3:8b`, an earlier and smaller model, on the other two endpoints. Its recordings are `tests/responses/m4/`, made on a local graphics card, and `tests/responses/pairs/`, made on a hosted endpoint. No row in the table comes from them; `m4/` is the source of the concatenation counts above and of the latency figures below. The counts in this paragraph are derived from the recordings, so they move when the corpus is recorded again.

**What that base can and cannot show.** The documents and their answer keys were written for this repository by AI coding agents under the author's direction, with the defects planted deliberately, and the author reviewed them. That is enough to show the pipeline runs end to end, and enough to find the hole in its own headline metric described above. These figures are not a benchmark: the fixtures are short, the domain is narrow, nobody outside the project has reviewed the answer keys, and no figure here predicts what the tool will do on a document it has never seen.

### Reproducing the figures

Every figure on this page is a property of a recorded corpus, and it reproduces by `--offline` replay, not by calling the endpoint again. The replay commands, and what each one prints, are in `tests/responses/README.md`. A live run is a new sample and can differ: a live re-run of the earlier `qwen3:8b` configuration at thinking off, on the same endpoint at the same settings a day apart, returned **212/243** against the recorded 225/243.

The first four rows do not replay today. On 2026-09-26 the field-order line of both verify prompts was changed to name `claim_id`, and the verify role began sending an output ceiling. Both changes alter the key of every recorded verify call, and the verify calls have not been recorded again, so every replay reports those four rows UNMEASURED. The decompose row still replays.

### Reference configuration

Every figure in the table was measured against **`Qwen/Qwen3.8-27B-FP8`**, served by vLLM on a hosted endpoint with a 32768-token window, at temperature 0, seed 0, the tier pinned to `json_schema`, and thinking off for every role including merge, which is the default. Changing any of these changes the figures. Until 2026-09-25 the reference was `qwen3:8b`, Q4_K_M, on an Ollama endpoint; that is what `tests/responses/m4/` and `tests/responses/pairs/` hold, and what the thinking measurements below were made on.

#### Thinking

**Thinking is off by default, for every role.** `--thinking ROLE` (repeatable) or `LLOSSLESS_THINKING` (comma-separated) names the roles that may reason. Either one replaces the default set and does not add to it, so `--thinking merge` turns merge on and leaves the other two roles off, and `LLOSSLESS_THINKING=` (set, but empty) turns every role off explicitly.

**What the default rests on.** With merge thinking on, the 27B spent its whole output budget on reasoning and returned no content, three times out of three. Its recordings therefore hold no thinking-on condition, and what thinking does on this model is not measured. The hosted frontier models in [the benchmark](benchmark.md) were run with reasoning on for all three roles: for them, set it as the README shows.

**What was measured, on `qwen3:8b`.** Every decompose and verify recording has thinking off. Of the 115 recorded merge calls, 37 carry a reasoning block, all of them `qwen3:8b`'s in `m4/` and `pairs/`; the 27B's 45 carry none. Forward coverage on the twelve fixtures common to every `qwen3:8b` recording, before and after the merge prompt was rewritten to take segmented sources:

| | thinking off | thinking on |
|---|---|---|
| old prompt, local card | 243/243 | 237/243 |
| old prompt, hosted endpoint | 237/243 | not measured |
| new prompt, hosted endpoint | 225/243 recorded, 212/243 on a live re-run | 240/243 |

The first row is 72 units: twelve fixtures x two conditions x three samples. Every measured cell is at or above 97.5% except new-prompt thinking-off. No measurement attributed that dip to the prompt or to the endpoint, so these figures show where each configuration sat, not a cause.

**Reasoning is not free.** Merge latency measured both ways on a local Ollama endpoint: mean 24.5 s off against 67.7 s on, median 23.0 s against 46.9 s, so **2.76x mean latency** for the merge step. That endpoint counts reasoning as `prompt_tokens` and leaves it out of `completion_tokens`, and the reasoning trace was 46.6-93.4% of generation, a median 78.1% of thinking-on generation, so a `completion_tokens` budget does not see it and `max_tokens` understates a thinking-on call. The recordings behind these figures are `tests/responses/m4/`.

#### Repeatability

**Temperature 0 and a fixed seed do not make the model deterministic**, so every call was recorded three times and every figure is over the modal answer. On the 27B, verify was fully stable, 164/164 verdicts identical across all three runs. Decompose was stable at the probe level, 164/164, but one document out of 48 came back with a different number of claims: `restated/merged.md`, the one fixture document a model wrote, at 43, 50 and 43. The 50 is the answer to a retry. In that sample the first answer held the same 43 claims as the other two, one of them without its line number, so validation rejected it and the model was asked again. Every first answer on the 27B repeated; what moved was a retry. On `qwen3:8b` the document that moved was the narrative fixture, `disjoint_sources/merged.md`, at 18, 17 and 18; on the 27B it did not move. The claim counts are reported as they came, not averaged away.

### Other measurements this page does not use

The table replaces earlier `qwen3:8b` figures and is not comparable with them: the model changed, two fixtures joined the set (`concatenated` and `restated`), and the prompts changed. The last `qwen3:8b` recording read 273/303 forward coverage at thinking off, 576/585 grounded and 166/166 verify-stable.

A separate study ran three open-weight models (`qwen3.8:27b`, `deepseek-r1:70b` and `gpt-oss:120b`) live on rented hardware in August and September 2026. Its outputs are in `arms/2026-08-30/` and `arms/2026-09-03/`, and no figure on this page is drawn from it.

### Where the evidence is

- `tests/responses/` and `tests/responses/m7/`: the recorded 27B corpus the table replays. `tests/responses/README.md` has the replay commands and the per-fixture detail.
- `tests/responses/m4/` and `tests/responses/pairs/`: the `qwen3:8b` recordings; the latency measurements are in `m4/`.
- `tests/analyse_merges.py` and `tests/measure_merges.py`: the two concatenation counts.
- `tests/handwritten/fizzbuzz_c_cpp/` and `tests/handwritten/unrelated/`: the two limitation cases.
- [`arms/BENCHMARK-MATRIX.md`](../arms/BENCHMARK-MATRIX.md): every model measurement made before the release benchmark, with its settings, headline figures and status, generated from the recorded runs by `tests/benchmark_matrix.py`.
- `arms/2026-08-30/` and `annotated/`: what each model in the open-weight study wrote, raw and as readable pages.
- [`arms/2026-09-27/lineup/figures.md`](../arms/2026-09-27/lineup/figures.md): the cross-vendor release benchmark behind the README's results, described in [The benchmark](benchmark.md).
