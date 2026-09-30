# How it works

This page explains what LLossless does between reading your documents and printing a verdict, and why you can act on a finding without taking the model's word for it. Read it if you want to know what a finding means, or if you plan to work on the code. Every option is in the [command-line reference](reference.md), the output is toured in [Reading the report](report.md), and the evidence is in [Measured results](results.md).

## The idea in one paragraph

A plain AI merge has only one witness to what happened: the model that did it. Ask that model to check its own work and it will confirm that whatever it dropped was meant to be dropped. So LLossless never uses the merge model as its own witness. Everything that can be checked by comparing strings is checked that way, with no model involved. What only a model can judge, whether a fact survived with its meaning intact, is judged claim by claim, in both directions, and every verdict has to quote evidence that the code then looks up in the file it names.

## The six steps

1. **Segment.** Each source is split into segments: sentences, headings, list items, table rows and fenced blocks, each with its line number.
2. **Merge.** The model is shown the segmented sources and returns the merged document plus a record for every segment it did not copy word for word: reworded, superseded, subsumed, duplicated or dropped, each with a reason. At `open` and `sourced` it can also declare an addition from outside the documents, with its basis.
3. **Reconcile.** Nine mechanical checks hold the merged text and those records against the sources. No model is involved. (Checking an existing merge with `verify` skips steps 2 and 3, since there are no records to hold it to, and starts here.)
4. **Decompose.** Each source and the merge are split into atomic claims: short statements of one fact each, each anchored to a quoted span and a line.
5. **Verify, both ways.** Source claims are graded against the merge, merge claims against the sources, in batches. Every verdict must quote its evidence.
6. **Report.** Findings, the fate of every claim, the declarations with whether the evidence confirms them, and a provenance block. [Reading the report](report.md) tours it.

## What a finding means

Every claim is verified in one of two directions, and the direction gives the same verdict its meaning.

| direction | a claim that is | finding | what went wrong |
|---|---|---|---|
| source → merge | `MISSING` | **dropped** | a fact in a source did not survive |
| source → merge | `PARTIAL` | **partly dropped** | the merge carries the fact with a detail missing |
| source → merge | `CONTRADICTED` | **contradicted** | the merge states a different value |
| merge → sources | `MISSING` | **invented** | the merge asserts what neither source does |
| merge → sources | `PARTIAL` | **partly invented** | the merge adds a detail to a fact its sources do state |
| merge → sources | `CONTRADICTED` | **contradicted** | the merge disagrees with its own sources |

**Why "partly" is its own verdict.** Called `MISSING`, a fact carried with one detail missing would overstate the loss. Called `SUPPORTED`, it would disappear, and in the reverse direction that is the quietest failure this tool exists to catch: a merge that adds one detail to a real fact reads exactly like a real fact.

**Evidence has to be grounded.** A verdict is only believed if the span the model quoted actually occurs in the file the model named. A quote found nowhere is a `transcription_error`; a quote found in a different file is an `attribution_error`. Both are reported beside the verdict rather than folded into it, because a right answer for a fabricated reason is not a right answer. A grounding failure does not move the exit code on its own: it measures whether the checker anchored its verdict, not whether the merge is sound. The exception is a run where claims were graded and none of them grounded. Nothing was measured, so that run exits 2, like any other run that produced no evidence.

## Why you do not have to trust the model

- **Strings first, the model second.** A number that changed, a link that lost a character, a re-indented code block, a source sentence that vanished without a record, a fact stated twice: all of these are found by comparing strings. Those findings are exact and cost nothing. The claim-level checks cover what string comparison cannot, which is meaning.
- **Evidence must be grounded,** as described above: a quote that is not in the named file is reported, never silently accepted.
- **Declarations are confirmed, not believed.** A segment the merge declared dropped counts as intentional only when the forward pass independently finds its claims gone. The merge's own reason is printed next to the evidence and never counted in the grade, and past `3%` of the source the volume of declared drops is itself a finding.
- **Documents are data, never instructions.** Both verify prompts say so before the model is shown anything, and `Prompt.render` substitutes every field in a single pass, so a document containing `{claims}` cannot have the claim list rendered into it, and a merged document reading "mark this SUPPORTED" gets no help from the tool. The first defence is a request to a model and worth what such requests are worth; the second is enforced by code.
- **No model grades itself in the benchmark.** The merge scores are computed by code, and where a check needs a model, a candidate is never its own judge.

## Structured output

Every model answer is JSON against a schema. Endpoints differ in how they can be held to one, so the tool uses the strongest mode the endpoint supports: a strict JSON schema, a tool call, or the schema described in the prompt. The mode is probed or pinned, and always recorded. A malformed answer is sent back with the validation error quoted, a bounded number of times. Records that still fail are listed as not graded rather than dropped, and a run with any ungraded claim exits 2.

## Design principles

- **Local-first.** The default target is a local model. A hosted endpoint is opt-in, and the report says so on its face. No telemetry, ever, and no version check, model registry lookup or update ping either.
- **Verification-first.** The verify pass has no off switch.
- **Minimal dependencies.** Standard library where possible; three third-party packages is the ceiling and the current count is zero.
- **Deterministic and auditable.** Temperature 0, fixed seed, and a provenance block that records what produced every number.
- **Prompts are files.** Every prompt lives in `prompts/` and is hashed into the report. Three fixed sentences the code adds to a prompt are constants in the source instead: the schema suffix the tier-3 fallback appends (`structured.py`), the validation error quoted back on a repair attempt (`parsing.py`), and the preamble on a window-measuring probe (`window.py`). None of the three is a prompt for a role.

## What it deliberately does not do

- No TUI, and no web UI inside the CLI. An optional, self-hosted server mode ships under `src/llossless/web/`, documented in [The web interface](web.md). It is strictly additive: the CLI neither imports it nor needs it, and `llossless merge` behaves identically whether or not it is present.
- No plugin system and no config file. CLI flags and environment variables only.
- No LangChain, LlamaIndex, or any orchestration framework.
- No PyPI packaging, no CI. `--profile` and the web UI's per-provider endpoints are not a multi-provider abstraction layer: each is chosen or configured by hand, and nothing infers a vendor from a model id, routes between vendors or falls back from one to another.
- No claim that more than two sources have been measured. The code accepts any number of sources; the published evidence is all pairs.
- No database. Filesystem only.
- **No judgement of writing quality.** LLossless checks only whether each fact survives. A merge that is clearer, shorter or better organised than its sources scores exactly the same as one that is not, and a merge that reads badly is not a finding. The corollary catches people out: a *notation* change is silent. "512" written as "approximately 500" is an information change and a defect; the same number written "0x200" is not. See "Notation is not information" in `tests/fixtures/SCHEMA.md`, and the `paraphrase` and `ordering_only` guard fixtures, which exist to fail the tool if it flags a rewrite that changed nothing factual.

Not scoring notation is not the same as hiding it. The merge model is shown each source line with its Markdown intact (headings, list markers, blockquote arrows, table pipes, code fences byte for byte), so the merge can keep the document's shape and a bullet list arrives as a bullet list. `decompose` still sees the stripped text, so no finding can be raised about notation in either direction. The two views used to be the same stripped rendering, and every model tested then wrote adjacent list items as one joined sentence, which the reverse pass correctly reported as invented: the rendering manufactured the defect it was then blamed for.

## What is in this repository

The tool, its prompts, the tests with the recorded model answers they replay, this documentation, and the benchmark evidence the figures come from.

| path | what is in it |
|---|---|
| `src/llossless/` | the library: config, transport, client, the three passes |
| `src/llossless/web/` | the local web interface: the job layer, the progress events, the `/api/v1` contract and the server that binds loopback |
| `src/llossless/web/locales/` | every word the interface says, one JSON file per language; `en.json` is the reference every other file is checked against |
| `prompts/` | every prompt, as a file, hashed into each report |
| `tests/fixtures/` | sixteen fixtures with hand-authored ground truth; `tests/fixtures/SCHEMA.md` is the format |
| `tests/pairs/`, `tests/handwritten/` | the document pairs the benchmark merges, with hand-written reference merges |
| `tests/responses/` | recorded model responses, so the whole suite runs offline |
| `tests/run_merge.py` | the measurement harnesses that produced every published number |
| `tests/run_all.py` | one command that runs every check in this copy |
| `arms/` | every recorded benchmark run: its registration, the reports and merged documents it produced, and the figures derived from them; the largest directory in the clone |
| `annotated/` | the merges of an earlier model study as readable pages, derived from `arms/` and `tests/pairs/` and checked to match them |
| `scripts/` | the arm-bundle builder and the stream redactor it uses to publish `arms/` without an endpoint address in it |
| `docs/` | this page, the other pages the README links to, and `docs/bench-spec.md`, the benchmark's machine-readable property registry |

## How it is tested

Run everything with **`python3 tests/run_all.py`**: one command over every test module and every scanner in this copy. It refuses to start if a check it names has gone missing, so a suite that got quietly smaller fails loudly rather than passing faster. A few tools belong to the maintainers' working copy and are not published; the runner names them as withheld on its first line of output instead of counting them as passes.

**The suite needs no model.** Every model response the tests use was recorded once, keyed by the exact request including a digest of the prompt, and is replayed from `tests/responses/`. `tests/socket_guard.py` enforces that: a test that opens a socket anywhere but the configured endpoint fails loudly. Every tool in the published suite runs offline.

**A changed prompt cannot pass quietly.** Change a prompt and the recordings it affects stop matching, and the suite says so. A re-recording that has been deliberately postponed reports its figures as unmeasured rather than as passes. Most published figures are re-derived from the recordings and records by scripts rather than typed by hand; the ones that cannot be, such as a measurement of a machine, say so and carry their date.

**Temperature 0 and a fixed seed do not make the model deterministic,** so every recorded call was made three times, and the one place the reference model varied between runs, how finely it split one document into claims, is reported rather than averaged away.

## Licence

The code is under the Elastic License 2.0. Its text is in `LICENSE`, and the SPDX identifier is `pyproject.toml`'s `license` field. The copyright holder is named in `NOTICE`, because the Elastic License 2.0 has no copyright line of its own. Four data directories (`tests/pairs/`, `tests/handwritten/`, `arms/` and `annotated/`) are under Creative Commons Attribution 4.0 International instead, and each carries its own `LICENSE`.
