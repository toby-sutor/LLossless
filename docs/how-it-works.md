# How it works

This page explains what LLossless does between reading your documents and printing a verdict, and why you can act on a finding without taking the model's word for it. Read it if you want to know what a finding means, or if you plan to work on the code. Every option is in the [command-line reference](reference.md), the output is toured in [Reading the report](report.md), and the evidence is in [Measured results](results.md).

## The idea in one paragraph

A plain AI merge has only one witness to what happened: the model that did it. Ask that model to check its own work and it will confirm that whatever it dropped was meant to be dropped. So LLossless never uses the merge model as its own witness. Everything that can be checked by comparing strings is checked that way, with no model involved. What only a model can judge, whether a fact survived with its meaning intact, is judged claim by claim, in both directions, and every verdict has to quote evidence that the code then looks up in the file it names.

## The six steps

1. **Segment.** Each source is split into segments: sentences, headings, list items, table rows and fenced blocks, each with its line number.
2. **Merge.** The model is shown the segmented sources and returns the merged document. It must also return a record for every segment it did not copy word for word, saying what happened to it and why: reworded, replaced by another source's version, folded into a broader sentence, combined with another segment into a new statement, a duplicate, or dropped. At the fidelity levels `open` and `sourced` it can also declare a statement that comes from outside the documents, with what it rests on.
3. **Reconcile.** Nine mechanical checks hold the merged text and those records against the sources. No model is involved.
4. **Decompose.** Each source and the merge are split into atomic claims: short statements of one fact each, each anchored to a quoted span and a line.
5. **Verify, both ways.** Source claims are graded against the merge (the forward check), and merge claims against the sources (the reverse check), in batches. Every verdict must quote its evidence. At `--verify-depth coverage` only the forward check runs.
6. **Report.** Findings, the fate of every claim, the merge's records with whether the evidence confirms them, and a provenance block that says which model, settings and prompts produced the run. [Reading the report](report.md) tours it.

`llossless verify` checks a merge that already exists, however it was made. There are no records to hold it to, so it skips steps 2 and 3 and starts at step 4. Two mechanical checks need no records and run on both commands: one for a statement credited to a source that does not carry it, and one for numbers whose decimal mark can be read two ways.

## What a finding means

Every claim is checked in one of two directions, and the direction decides what a verdict means.

| direction | verdict | reported as | what went wrong |
|---|---|---|---|
| source → merge | `MISSING` | **dropped** | a fact in a source did not survive |
| source → merge | `PARTIAL` | **partly dropped** | the merge carries the fact with a detail missing |
| source → merge | `CONTRADICTED` | **contradicted** | the merge states a different value |
| merge → sources | `MISSING` | **invented** | the merge asserts what no source does |
| merge → sources | `PARTIAL` | **partly invented** | the merge adds a detail to a fact its sources do state |
| merge → sources | `CONTRADICTED` | **contradicted** | the merge disagrees with its own sources |

Two verdicts are not findings. `SUPPORTED` means the other side states the claim, in the same or in different words. `DERIVED` exists only at the fidelity levels `high`, `open` and `sourced`, where the merge may join facts: it marks a merge claim that no single source states and that two or more source statements, taken together, do.

**Why "partly" is its own verdict.** Called `MISSING`, a fact carried with one detail missing would overstate the loss. Called `SUPPORTED`, it would disappear, and in the reverse direction that is the quietest failure this tool exists to catch: a merge that adds one detail to a real fact reads exactly like a real fact.

**Evidence has to be grounded.** A verdict is only believed if the span the model quoted actually occurs in the file the model named. A quote found nowhere is a `transcription_error`; a quote found in a different file is an `attribution_error`. Both are reported beside the verdict rather than folded into it, because a right answer for a fabricated reason is not a right answer. A grounding failure does not move the exit code on its own: it measures whether the checker anchored its verdict, not whether the merge is sound. The exception is a run where claims were graded and none of them grounded. Nothing was measured, so that run exits 2, like any other run that produced no evidence.

## Why you do not have to trust the model

- **Strings first, the model second.** A number that changed, a link that lost a character, a re-indented code block, a source sentence that vanished without a record, a fact stated twice: all of these are found by comparing strings. Those findings are exact and cost nothing. The claim-level checks cover what string comparison cannot, which is meaning.
- **Evidence must be grounded,** as described above: a quote that is not in the named file is reported, never silently accepted.
- **The merge's records are confirmed, not believed.** Each kind of record predicts what the forward check should find, and a record the evidence contradicts is reported as rejected. A segment the merge declared dropped counts as intentional only when the forward check independently finds its claims gone. The merge's own reason is printed next to the evidence and never counted in the grade, and past `3%` of the source segments the volume of declared drops is itself a finding (`--loss-budget` changes the share).
- **Documents are data, never instructions.** The merge prompt and every verify prompt say so before the model is shown a document. The code also substitutes every field of a prompt in a single pass, so a document containing `{claims}` cannot have the claim list rendered into it. The first defence is a request to a model and worth what such requests are worth; the second is enforced by code.
- **No score comes from a model grading itself.** In the [benchmark](benchmark.md), every headline figure is computed by code: from the merged text and the merge's own records, the hand-written answer keys and the exit codes.

## Structured output

Every model answer is JSON that must match a schema. Endpoints differ in how they can be held to one, so the tool uses the strongest of three *tiers* the endpoint supports: `json_schema` (the endpoint enforces the schema), `tool_call` (the schema is the parameter list of a function the model must call), or `prompt` (the schema is only described in the prompt). The tier is probed, or pinned with `--structured`, and the report always records it. On every tier the answer is validated, and a malformed one is sent back with the validation error quoted, up to four times. Records that still fail are listed as not graded rather than dropped, and a run with any ungraded claim exits 2.

## Design principles

- **It runs on your machine and talks only to the endpoints you configure.** The command line's default endpoint is a local Ollama address, `http://localhost:11434/v1`, and the web interface listens on `127.0.0.1` unless told otherwise. A hosted model is used only when you point the tool at one, and the report then says that document content left the machine. There is no telemetry, no update check and no call to any other service. At the fidelity level `sourced` the model itself may search the web.
- **A merge is always checked.** There is no flag that turns the forward check or the mechanical checks off; the one adjustable threshold among them is the declared-loss budget, `--loss-budget`. `--verify-depth coverage` skips the reverse check only, so that depth cannot catch an invention, and every report of such a run says so.
- **Minimal dependencies.** Standard library where possible; three third-party packages is the ceiling and the current count is zero.
- **Repeatable where the endpoint allows it, and always auditable.** Temperature 0 and seed 0 are sent wherever the request profile allows. The default `openai-compatible` profile sends both. `openai-reasoning` sends the seed, and temperature 0 only with reasoning off. The `anthropic`, `google` and `subscription` profiles send neither, so two runs there can differ. Either way the provenance block records what produced every number.
- **Prompts are files.** Every prompt that instructs a role is a file in `prompts/`, and the report records the digest of each prompt the run used. Beyond those files and your documents, the code adds only a few fixed sentences of its own, kept as constants in the source: the schema text on the `tool_call` and `prompt` tiers, the error quoted back on a retry, and the filler text of the probe that measures a context window.

## What it deliberately does not do

- **It does not judge writing quality.** LLossless checks only whether each fact survives. A merge that is clearer, shorter or better organised than its sources scores exactly the same as one that is not, and a merge that reads badly is not a finding. Within what the fidelity level allows, rewording, reordering and restructuring are silent for the same reason: the `paraphrase` and `ordering_only` fixtures exist to fail the tool if it flags a rewrite that changed nothing factual, and "Notation is not information" in `tests/fixtures/SCHEMA.md` draws the line. A change in what is known is a finding: "512" written as "approximately 500" is a defect.
- **It does not choose a vendor.** On the command line you set the endpoint and its request profile (`--profile`) by hand. In the web interface a model goes to the endpoint stored for its provider and nowhere else. Nothing guesses a vendor from a model name, and nothing falls back from one vendor to another.
- **No plugin system and no orchestration framework** such as LangChain or LlamaIndex. Configuration is command-line flags, environment variables and one optional file that names the models, `models.local.json`.
- **No database.** The response cache, and the web server's runs, accounts and keys, are plain files.
- **No terminal user interface.** The command line prints a report; the optional web interface is started with `llossless serve` and described in [The web interface](web.md). `merge` and `verify` never load it.
- **No PyPI packaging, no CI.** LLossless is installed from a clone of the repository, and the test suite is one command that is run by hand.
- **No claim about three or more sources.** The code accepts any number of sources. Almost all published evidence is from two: the one exception is the three-source `mahjongg` control document in the release benchmark.

**Markdown markers are shown to the merge and ignored by the checks.** The merge model sees each source line with its Markdown intact: heading markers, list bullets, quote arrows, table pipes, and code fences byte for byte. That lets the merge keep the document's shape, so a bullet list arrives as a bullet list. The mechanical checks then take the same line-leading markers off both sides before they compare, so changing a bullet to a numbered item is never a finding. Some things are compared exactly at every fidelity level, because a merge must copy them and not restyle them: fenced code blocks, inline code, link targets, URLs, paths, version strings and numbers. In a merge the tool made, "512" rewritten as "0x200" is therefore a finding (`verbatim_violation`).

## What is in this repository

The tool, its prompts, the tests with the recorded model answers they replay, this documentation, and the benchmark evidence the figures come from.

| path | what is in it |
|---|---|
| `src/llossless/` | the tool: configuration, the HTTP client, segmenting, the merge, the mechanical checks, claim extraction, verification and the report |
| `src/llossless/web/` | the web interface and its JSON API, started with `llossless serve` |
| `src/llossless/web/locales/` | every word the web interface says, one JSON file per language; `en.json` is the reference the others are checked against |
| `prompts/` | every prompt, as a file |
| `tests/fixtures/` | sixteen small test cases with hand-written answer keys; `tests/fixtures/SCHEMA.md` is the format |
| `tests/pairs/` | the nine document pairs the benchmark merges, each with a hand-written reference merge |
| `tests/handwritten/` | nineteen more hand-written document sets, among them the benchmark's planted-error documents |
| `tests/responses/` | recorded model answers, so the whole suite runs offline |
| `tests/run_merge.py`, `tests/run_verify.py`, `tests/run_decompose.py`, `tests/run_detect.py` | the harnesses that replay the recordings and print the figures on [Measured results](results.md) |
| `tests/run_lineup.py`, `tests/lineup_figures.py` | the release benchmark's runner, and the script that re-derives its figures from `arms/` |
| `tests/run_all.py` | one command that runs every check in this copy |
| `arms/` | every recorded benchmark run: its registration, the reports and merged documents it produced, and the figures derived from them; the largest directory in the clone |
| `annotated/` | the merges of an earlier model study as readable pages, derived from `arms/` and `tests/pairs/` |
| `scripts/` | the script that builds `arms/` from a run directory, and the redactor it uses to keep endpoint addresses, credentials and home paths out of it |
| `docs/` | this page, the other pages the README links to, and `docs/bench-spec.md`, an earlier benchmark specification that `tests/run_bench.py` reads |

## How it is tested

Run everything with **`python3 tests/run_all.py`**: one command over every test module and every scanner in this copy. It refuses to start if a check it names has gone missing, so a suite that got quietly smaller fails loudly rather than passing faster. A few tools belong to the maintainers' working copy and are not published; the runner names them as withheld at the top of its output instead of counting them as passes.

**The suite needs no model.** Every model answer the tests use was recorded from a real model, keyed by the exact request including a digest of the prompt, and is replayed from `tests/responses/`. `tests/socket_guard.py` enforces that: a test that opens a socket anywhere but the configured endpoint fails loudly. Every tool in the published suite runs offline.

**A changed prompt cannot pass quietly.** Change a prompt and the recordings it affects stop matching, and the suite says so. A re-recording that has been postponed reports its figures as unmeasured rather than as passes. That is the state today for the verify recordings: both verify prompts changed on 2026-09-26, so the figures that depend on them read UNMEASURED until they are recorded again. Most published figures are re-derived from the recordings and run records by scripts rather than typed by hand; the ones that cannot be, such as a measurement of a machine, say so and carry their date.

**Temperature 0 and a fixed seed do not make the model deterministic,** so every call was recorded three times. In the current recordings every first answer came back the same in all three samples. The one difference is a retry that split one document into more claims than the first answers did, and it is reported rather than averaged away.

## Licence

The code is under the Elastic License 2.0. Its text is in `LICENSE`, and the SPDX identifier is `pyproject.toml`'s `license` field. The copyright holder is named in `NOTICE`, because the Elastic License 2.0 has no copyright line of its own. Four data directories (`tests/pairs/`, `tests/handwritten/`, `arms/` and `annotated/`) are under Creative Commons Attribution 4.0 International instead, and each carries its own `LICENSE`. Inside them, four document sets in `tests/handwritten/` (`gold_de_en`, `mahjongg`, `sepia` and `treecreeper`) are adapted from Wikipedia articles. Those sets, and the benchmark runs under `arms/` that merged `mahjongg`, are under Creative Commons Attribution-ShareAlike 4.0 International: anything built from them must credit the Wikipedia contributors and carry the same licence. `NOTICE` lists them, and `tests/handwritten/LICENSE-CC-BY-SA` names each article.
