# Command-line reference

This page is for looking things up: what each `llossless` command does, what each exit code means and what to do about it, every flag and environment variable with its default, and what the tool stores, sends and prints. If you are new, start with the [README](../README.md). The web interface has [its own page](web.md), and [Reading the report](report.md) explains the output.

- [Most used](#most-used)
- [Commands](#commands)
- [Exit codes](#exit-codes)
- [Merge policy](#merge-policy): [fidelity](#fidelity), [verification depth](#verification-depth), [title policy](#title-policy), [loss budget](#loss-budget), [checking a merge made elsewhere](#checking-a-merge-made-elsewhere)
- [Options](#options): [endpoint and model](#endpoint-and-model), [one endpoint per role](#one-endpoint-per-role), [answering through a program](#answering-through-a-program), [effort](#effort), [timeouts](#timeouts), [compatibility controls](#compatibility-controls), [run control](#run-control)
- [Cache, keys and the network](#cache-keys-and-the-network)
- [What it tells you while it runs](#what-it-tells-you-while-it-runs)
- [Context windows](#context-windows)
- [Notes for local models](#notes-for-local-models)
- [For contributors](#for-contributors)

## Most used

First say which model answers. Then merge, or check a merge you already have. The settings below are environment variables; all but the key also exist as flags.

**With an API key from a model vendor.** The example is OpenAI:

```sh
export LLOSSLESS_API_KEY='<your API key>'
export LLOSSLESS_BASE_URL=https://api.openai.com/v1
export LLOSSLESS_PROFILE=openai-reasoning
export LLOSSLESS_MODEL=gpt-6-luna
export LLOSSLESS_WINDOW=200000                    # the model's context window, in tokens
export LLOSSLESS_THINKING=merge,decompose,verify  # let the model reason before it answers
```

For Anthropic, the address is `https://api.anthropic.com/v1` and the profile is `anthropic`. For Google, the address is `https://generativelanguage.googleapis.com/v1beta/openai` and the profile is `google`. [Endpoint and model](#endpoint-and-model) explains each line.

**With a local Ollama.** This is the built-in default endpoint and needs no key, only a model name:

```sh
export LLOSSLESS_MODEL=qwen3:8b
```

Start Ollama with a larger context window first: see [Notes for local models](#notes-for-local-models).

**With a Claude subscription** instead of an API key: see [Answering through a program](#answering-through-a-program).

Then:

```sh
# merge two documents, check the result, keep both
llossless merge a.md b.md --base a.md -o merged.md > report.md

# check a merge you already have
llossless verify a.md b.md merged.md > report.md

# count the model calls first, without making any
llossless merge a.md b.md --base a.md --dry-run

# watch each step, and also get the report as one HTML page
llossless merge a.md b.md --base a.md -o merged.md --html report.html -v > report.md
```

The exit code says how it went: `0` nothing found, `1` a problem in the merged document, `3` the document is sound but the merge misdescribed what it did, `2` the run could not finish. Details are under [Exit codes](#exit-codes).

## Commands

```
llossless merge SOURCE SOURCE... --base PATH [options]
llossless verify SOURCE SOURCE... MERGED [options]
llossless serve [options]
```

| command | what it does |
|---|---|
| `merge` | Has a model write one merged document from the sources, then checks that document against every source. |
| `verify` | Checks a merged document you already have, whoever or whatever wrote it. It makes no merge call, so it costs less than `merge`. The merged document goes last on the line. |
| `serve` | Runs the web interface on this machine. Its flags are listed under [Run control](#run-control) and explained in [The web interface](web.md). |

`llossless` with no arguments prints the short help and exits 0. `llossless merge --help` and `llossless verify --help` list every flag.

**Two sources at least, twelve at most.** Sources are UTF-8 text, markdown or plain. One source, or more than twelve, is refused before any file is opened. The model sees your files as `source_a.md`, `source_b.md`, `source_c.md` and so on, in the order you gave them. The report uses your own file names, apart from its `Base document` row and some error messages.

**`--base` is required on `merge`, and names one of the sources.** The merged document follows the base document's structure, and takes its title under `--title-policy keep-base`. Naming a file that is not a source is an error, and so is giving the same file twice. `./a.md` and `a.md` are the same document. `verify` refuses `--base`, because it writes no document.

**Almost everything measured is a merge of two sources.** The published results come from pairs of documents, apart from one test set with three sources (`tests/handwritten/mahjongg`). A merge of more sources runs, but how well a model handles it has not been measured.

**The report goes to stdout.** Progress and errors go to stderr, so `> report.md` captures the report and nothing else.

```
llossless merge notes-a.md notes-b.md --base notes-a.md > report.md
```

**The merged document goes to `-o`.** Without `-o`, the merged document is included in the report under a `## Merged document` heading, and no other file is written.

```
llossless merge notes-a.md notes-b.md --base notes-a.md -o merged.md > report.md
```

**No output ever overwrites an input.** If `-o`, `--json`, `--html` or `--sweep-dir` names one of the sources, or two of them name the same file, the run is refused before the first model call. `-o` on `verify` is also an error, because `verify` writes no merged document.

## Exit codes

| code | meaning | what to do |
|---|---|---|
| **0** | Nothing found. Every claim in the sources is accounted for in the merge, nothing in the merge conflicts with a source, and nothing was invented. | Use the merged document. If the closing lines mention a review queue, read it: those are passages the merge said it left out. At `--verify-depth coverage`, 0 says nothing about invention. |
| **1** | A problem in the merged document. At least one claim was dropped, contradicted, invented or carried only in part; or a structural check failed (content missing with no record of it, a changed number, URL or code block, a title the sources do not support, content stated twice, a statement credited to the wrong source); or the merge declared more drops than the [loss budget](#loss-budget) allows. | Read the findings in the report. Each one quotes the passage and gives its line number. Fix the merged document, or merge again, then run `verify` on the result. |
| **3** | Only the merge's record is wrong. The merged document has no finding, but the merge misdescribed what it did: it declared a change that did not happen, pointed to replacement text that is not there, declared a kind of change the fidelity level forbids, or dropped a title without recording it. | The document passed every check that ran. Read the report's `## Structure` section to see which record is wrong, and decide whether that matters to you. A script can treat 3 as "document passed, record did not". |
| **2** | The run could not finish, or could not check everything: a bad setting, an endpoint that cannot be reached, a step the model did not answer in a usable form, a source that produced no claims on `verify`, graded claims none of whose quotes was found in the file named, an output file that could not be written, a report refused because two of its counts disagree, or a `sourced` merge in which the model looked nothing up. | Read the closing lines on stderr, which name the step that failed. Fix the cause and run again. Do not use a partial report as a pass. |

**When several apply, the worst wins: 2 over 1 over 3.** A run that checked nine claims out of twelve and found no fault has not shown that there is none, so it exits 2. A run with a document finding and a record finding exits 1.

**A declared drop is not a finding, up to a limit.** A merge may say that it left a passage out, and why. If the check agrees the passage is gone, it is listed in the report's `## Review queue` and the run can still exit 0: putting it back is your decision. Once the declared drops exceed the [loss budget](#loss-budget), 3% of the source segments by default, the run exits 1. Losses the merge did not declare are always findings.

**One replacement can stand in for at most 3 passages.** A merge may also declare that a passage was replaced by a sentence that covers it. If more than three passages that are gone from the merge all point to the same replacement, that counts as a loss and the run exits 1.

## Merge policy

Four settings decide what the merge may do and how it is checked. They mean the same on every endpoint, and the report prints them.

| flag | env var | default | what it sets |
|---|---|---|---|
| `--fidelity LEVEL` | `LLOSSLESS_FIDELITY` | `high` | How freely the merge may reword and combine the sources. See [Fidelity](#fidelity). |
| `--verify-depth DEPTH` | `LLOSSLESS_VERIFY_DEPTH` | `full` | Whether the merge is checked in both directions (`full`) or only for lost content (`coverage`). See [Verification depth](#verification-depth). |
| `--title-policy POLICY` | `LLOSSLESS_TITLE_POLICY` | `synthesise` | Which title the merged document takes. See [Title policy](#title-policy). |
| `--loss-budget FRACTION` | `LLOSSLESS_LOSS_BUDGET` | `0.03` | The share of the source segments a merge may declare it dropped. See [Loss budget](#loss-budget). |

### Fidelity

Fidelity is how much editing the merge is allowed. Each level allows everything the level above it in this table allows, and more.

| level | what the merge may do | where two documents disagree |
|---|---|---|
| `verbatim` | Only copy sentences from the sources, exactly. It chooses which to keep and in what order. Typos stay. | Both statements stay. |
| `low` | Also fix spelling, grammar slips and punctuation. Each sentence stays recognisably the original. | Both statements stay. |
| `mid` | Also rewrite single sentences for clarity, and fold a short detail into the sentence it belongs to. Every folded detail is listed in the report. | Both statements stay. |
| `high` | Rewrite freely, like a careful editor: state a repeated point once, and join facts from several documents into one statement. | The merge picks one value and says which and why. Check that choice. |
| `open` | Everything `high` does. It may also correct a fact from what the model knows, or give a range that covers two figures the documents disagree about. Each such addition is listed in the report. | As at `high`, or a range covering both. |
| `sourced` | Like `open`, but the model is asked to look facts up on the web instead of recalling them. The report says whether it did. | As at `open`. |

The default is `high`. The level is printed on every report, because the same result means different things at different levels.

**Rules that hold at every level:**

- Numbers, URLs, links, file paths, version strings, inline code and fenced code blocks must survive exactly. A changed one is a finding. A command or a unit is protected where it is written as code or is part of the number it belongs to.
- Whatever the merge leaves out, it has to declare, and the declarations are checked.
- A statement in the merge that no source supports is reported as invented, at `--verify-depth full`. At `open` and `sourced` the merge may add such a statement only as a declared addition, which the report lists under `## Added from outside the documents`. The tool checks only against your documents, so a declared addition rests on the model's word and reviewing it is your job.

**`sourced` needs a model that can search the web, and refuses otherwise.** It works through a program (see [Answering through a program](#answering-through-a-program)): `claude` is given the `WebSearch` and `WebFetch` tools automatically, and any other program must carry `--allowed-tools WebSearch,WebFetch` in its own command. It also needs the JSON result envelope (`--output-format json` in the command and `LLOSSLESS_COMMAND_ENVELOPE=result`), because that is how the tool learns whether the model searched. An HTTP endpoint cannot run `sourced`: use `open` there. Text from your documents can leave the machine in a search or a page request. A `sourced` merge in which the model looked nothing up exits 2, because it is not a sourced merge.

**`off` is an older name for `verbatim`.** `--fidelity off` still works and gives the same run. Reports print `verbatim`; the JSON report keeps `off`. `verbatim` is the strictest level, not the absence of one: it turns rewriting off, not checking.

**To compare the levels on your own documents**, `--sweep-fidelity` runs the same merge once at every level the endpoint can run and prints one table. Add `--sweep-dir DIR` to keep each level's merged document and JSON report. A sweep makes live calls for every level, and it cannot be combined with `--fidelity`, `-o`, `--html` or `--dry-run`.

### Verification depth

| depth | what it checks | model calls for a merge of N sources |
|---|---|---|
| `full` (default) | Both directions: everything in the sources made it into the merge, and the merge says nothing the sources do not. | At least N + 4. |
| `coverage` | Only that everything in the sources made it into the merge. The merge is never read back, so an invented statement goes unnoticed. | Exactly N + 1. |

The structural checks that need no model run at either depth. At `full` the count is a minimum, because claims are checked in batches: 25 per call over HTTP, 100 per call through a program.

**What `coverage` costs in detection was measured once, on a small test set.** Over 13 test cases with 7 planted defects, checked by one model (`Qwen/Qwen3.8-27B-FP8`) in one run, `coverage` caught 6 of the 7 and missed the one invented statement, which it cannot reach. `full` caught all 7. Neither depth flagged a correct statement, and `coverage` ran 2.04 times faster. Read this as a guide, not a guarantee for your documents. The run is in `arms/2026-09-24/depth/`, and `tests/depth_figures.py --check` derives the figures from it.

A report made at `coverage` says in its verdict that invention was not checked.

### Title policy

| policy | the merged document's title |
|---|---|
| `synthesise` (default) | The merge may write a title of its own. A written title is checked against the sources as a claim, the same way a merged sentence is. |
| `keep-base` | The base document's title. If the base has none, the first title found in the other sources, in the order given. |
| `choose-best` | Whichever source title names the subject most clearly. Never a new one. |

Under `keep-base` and `choose-best` the title must be an exact copy of a source title.

### Loss budget

The loss budget is the share of the source segments a merge may declare it dropped before the run exits 1. A segment is one unit of a source document: a sentence, a heading, a list item, a table row or a code block.

- It is a fraction between `0.0` and `1.0`, not a percentage. `--loss-budget 5` is rejected.
- The run fails when the share is greater than the budget. At the default `0.03`, three declared drops in a hundred segments pass and four fail.
- `0.0` is the strict setting: one declared drop fails.
- `1.0` turns the check off. A report written at `1.0` says that the budget was disabled.

### Checking a merge made elsewhere

**On a `verify` run, pass the fidelity level the merge was written at.** The checker is told the level, because what counts as a fault depends on what the merge was allowed to do. Without `--fidelity`, `verify` assumes `high`. If the merge was made at a stricter level, say so: otherwise the checker excuses a rewrite that the stricter level forbids.

## Options

The four flags that shape the result are under [Merge policy](#merge-policy) above. This section covers the rest: where requests go, and how a run behaves.

**A flag beats an environment variable, which beats `models.local.json`.** In the tables, "-" in the flag column means the setting has no flag.

### Endpoint and model

| flag | env var | default | what it sets |
|---|---|---|---|
| `--base-url URL` | `LLOSSLESS_BASE_URL` | `http://localhost:11434/v1` | Where requests go: any OpenAI-compatible endpoint. The default is a local Ollama. A URL with no path gets `/v1` appended. |
| `--model ID` | `LLOSSLESS_MODEL` | from `models.local.json` | The model, for every role. There is no built-in default: without a model the run stops and says where it looked. |
| `--merge-model ID` | `LLOSSLESS_MERGE_MODEL` | the `--model` value | A different model for the merge only. |
| - | `LLOSSLESS_API_KEY` | unset | The API key. Leave it unset for an endpoint that needs none. |
| - | `LLOSSLESS_API_KEY_ENV` | `LLOSSLESS_API_KEY` | The name of the variable that holds the key, if the key already lives in another variable. |
| `--profile NAME` | `LLOSSLESS_PROFILE` | `openai-compatible` | Which request fields the endpoint accepts. See [request profiles](#compatibility-controls). |
| `--window TOKENS` | `LLOSSLESS_WINDOW` | unset: the tool asks the endpoint | The model's context window. State it for every hosted endpoint. See [Context windows](#context-windows). |
| `--thinking ROLE` | `LLOSSLESS_THINKING` | none | Which roles may reason before answering. Repeat the flag per role, or list the roles in the variable, separated by commas. |
| - | `LLOSSLESS_CA_BUNDLE` | system trust store | A CA bundle file, for a network that intercepts TLS. |

**The three roles.** A run uses a model for three jobs: `merge` writes the merged document, `decompose` splits a document into single claims, and `verify` checks each claim. One model can do all three. `--merge-model` lets a stronger model write the merge while a cheaper one checks it.

**With an API key, set six things.** The default endpoint is a local Ollama, so a hosted model needs the address, the key, the model, the profile, the window and the thinking roles: the six lines under [Most used](#most-used). The web interface can also write the command for you: set up a run there and open "Run this from the command line".

**`models.local.json`** is an optional file that names a model per role, for example `{ "merge": "qwen3:8b", "verify": "qwen3:8b" }`. `decompose` uses the `verify` model unless the file names one for it. In the cloned repository the file sits in the top folder; `models.local.example.json` is a template. For an installed `llossless` it is read from the current directory, then from `~/.config/llossless/` (or `$XDG_CONFIG_HOME/llossless/`).

**`--model` on the command line sets all three roles.** It overrides the file and both model variables, so add `--merge-model` on the same line to keep a different model for the merge. The variable `LLOSSLESS_MODEL` is narrower: it replaces only the file's `verify` entry.

**Thinking** is off for every role by default. `--thinking` and `LLOSSLESS_THINKING` replace the set of roles, so `--thinking merge` turns reasoning on for the merge and leaves the other two off. `LLOSSLESS_THINKING=` (set, but empty) turns every role off. Three things to know:

- The published benchmark ran hosted models with reasoning on for all three roles (`arms/2026-09-27/lineup/REGISTRATION.md`).
- The `google` and `subscription` profiles cannot turn reasoning off, so with them every role must be listed, or the first call is refused.
- Reasoning costs time. The measured cost on a local model is in [Measured results](results.md).

### One endpoint per role

Each role can have its own endpoint, key and context window. This lets one model on one service write the merge while a cheaper or local model does the checking. These settings are environment variables only.

| env var | default | what it sets |
|---|---|---|
| `LLOSSLESS_BASE_URL_<ROLE>` | the role uses `LLOSSLESS_BASE_URL` | The endpoint for this role. |
| `LLOSSLESS_API_KEY_ENV_<ROLE>` | the role uses `LLOSSLESS_API_KEY_ENV` | The name of the variable that holds this role's key. A name, never the key itself. |
| `LLOSSLESS_WINDOW_<ROLE>` | the role uses `LLOSSLESS_WINDOW` | The context window of this role's endpoint. |

`<ROLE>` is `MERGE`, `VERIFY` or `DECOMPOSE`.

```sh
# the merge on a hosted endpoint, the checks on the local machine
export LLOSSLESS_BASE_URL=http://localhost:11434
export LLOSSLESS_MODEL=qwen3:8b
export LLOSSLESS_BASE_URL_MERGE=https://your-endpoint.example/v1
export LLOSSLESS_MERGE_MODEL=Qwen/Qwen3.8-27B-FP8
export LLOSSLESS_API_KEY_ENV_MERGE=MY_VENDOR_KEY
export LLOSSLESS_WINDOW_MERGE=32768
```

- A role with no entry of its own uses the run-wide setting.
- `decompose` uses the `verify` model by default, but not the `verify` endpoint. To move both checking roles, set both `LLOSSLESS_BASE_URL_VERIFY` and `LLOSSLESS_BASE_URL_DECOMPOSE`.
- The request profile and the structured-output mode are set once for the whole run, so every endpoint in a run must accept the same profile.
- `-vv` prints which role goes to which endpoint before the run starts.

### Answering through a program

`--answer-with COMMAND` sends each prompt to a program's standard input and reads the answer from its standard output, instead of calling an HTTP endpoint. This is how a flat-rate subscription, such as a Claude subscription through the `claude` command line, can do the work of a metered API.

| flag | env var | default | what it sets |
|---|---|---|---|
| `--answer-with COMMAND` | `LLOSSLESS_COMMAND` | unset: answer over HTTP | The program and its arguments. |
| - | `LLOSSLESS_COMMAND_ENVELOPE` | `raw` | How the program answers. `raw`: its whole output is the answer. `result`: its output is a JSON envelope with the answer in a `result` field, which is what `claude --output-format json` prints. |
| - | `LLOSSLESS_COMMAND_LABEL` | unset | A name for this route, shown in the opening line and in the report. Display only. |

A complete setup for a Claude subscription:

```sh
export LLOSSLESS_COMMAND='claude --print --output-format json --model sonnet'
export LLOSSLESS_COMMAND_ENVELOPE=result
export LLOSSLESS_PROFILE=subscription
export LLOSSLESS_MODEL=sonnet                     # the name the report uses
export LLOSSLESS_WINDOW=200000
export LLOSSLESS_THINKING=merge,decompose,verify

llossless merge a.md b.md --base a.md -o merged.md > report.md
```

What a program route needs, and what changes with it:

- **A stated context window.** A program cannot be asked for one, so `--window` or `LLOSSLESS_WINDOW` is required and the run is refused without it.
- **The `subscription` profile and thinking on for every role.** A program takes a prompt and nothing else, so there is no request field that could carry a schema, a seed or a "do not reason" instruction.
- **An envelope setting that matches the command.** A command with `--output-format json` needs `LLOSSLESS_COMMAND_ENVELOPE=result`, and a command without it needs `raw`. A mismatch is refused before the first call. With `result`, the report also names the model version that really answered, for example `opus -> claude-opus-5-5`.
- **No price and no repeatability.** The report gives the cost of these calls as unmeasured. The same run can give a different answer next time, because no seed or temperature can be set.
- **The report says the documents were handed to a program.** The tool cannot see what a program does with them, so treat the content as having left the machine unless you wrote the program.
- **The program gets a reduced environment.** Variables that start with `LLOSSLESS_`, `ANTHROPIC`, `OPENAI`, `OPEN_AI`, `GOOGLE_AI` or `GEMINI`, and `GOOGLE_API_KEY`, are not passed to it, so an API key in your shell cannot switch a subscription run to metered billing or hand another vendor's key to the program. `CLAUDE_CODE_OAUTH_TOKEN` is passed through.
- **`claude` runs isolated.** The tool adds `--safe-mode` and a `--tools` list to every `claude` call. The run does not load your personal Claude Code instructions, skills, plugins or MCP servers, and the model gets no tools, except the two web tools at `--fidelity sourced`. A flag you wrote into the command yourself is never changed.

### Effort

`--effort` sets how hard a program route is asked to think, per role. It applies to `claude` only: the tool appends `--effort LEVEL` to the command. An HTTP endpoint has no such setting.

| flag | env var | levels |
|---|---|---|
| `--effort LEVEL` or `--effort ROLE=LEVEL` | `LLOSSLESS_EFFORT`, `LLOSSLESS_EFFORT_<ROLE>` | `low`, `medium`, `high`, `xhigh`, `max` |

The defaults depend on the model the command names with its own `--model`:

| the command's `--model` | merge | decompose and verify |
|---|---|---|
| `opus` | `high` | `low` |
| `sonnet`, any other name, or none | `medium` | `low` |
| `haiku`, or an id starting `claude-haiku-` | no level is sent | no level is sent |

Haiku has a single level, so no level is sent for it even if you ask for one.

**To override:** `--effort high` sets every role, and `--effort merge=max` sets one. The flag can be repeated, and the later one wins. `LLOSSLESS_EFFORT` and `LLOSSLESS_EFFORT_<ROLE>` do the same from the environment. A level written into the command itself beats all of these and is never changed.

A level asked for where it cannot apply (an HTTP endpoint, a program other than `claude`, Haiku) is ignored, and the report's Decoding row says so. The same row shows the level each role really ran at.

**Where the defaults come from:** a comparison of 2026-09-25 that varied the merge effort through a subscription, in `arms/2026-09-25/subscription-comparison/` (`tables.md` has the results). The checks stay at `low` because they grade the merge's work and write none of their own.

### Timeouts

| flag | env var | default |
|---|---|---|
| `--timeout SECONDS` | `LLOSSLESS_TIMEOUT` | `120` over HTTP, `890` through a program |

The two defaults measure different things. Over HTTP the answer arrives in pieces and every piece restarts the clock, so the timeout limits silence, not the length of the call. A program gives no partial output, so there the timeout limits the whole call; so does HTTP with `LLOSSLESS_STREAM=false`. A large pair of documents or a slow model can need more than either default.

### Compatibility controls

Settings that adapt the tool to a particular endpoint. Most runs need none of them beyond `--profile`, which is listed under [Endpoint and model](#endpoint-and-model) and described below.

| flag | env var | default | what it sets |
|---|---|---|---|
| `--structured MODE` | `LLOSSLESS_STRUCTURED` | `auto` | How the model is held to the answer format: `json_schema`, `tool_call` or `prompt`. `auto` tries them in that order and remembers which one the endpoint accepted. Naming one skips the trial. |
| `--field-order MODE` | `LLOSSLESS_FIELD_ORDER` | `schema` | `schema`: an answer must list its fields in the order the format declares. `any`: a complete, valid answer is accepted in any field order. Use `any` for an endpoint that reorders JSON keys. |
| - | `LLOSSLESS_STREAM` | `true` | `false` turns off streamed answers. Streaming is on because some hosted endpoints drop a request that has not started answering within about two minutes. The answer is the same either way. |
| - | `LLOSSLESS_MAX_TOKENS` | unset | An upper limit on the length of the merge's answer, in tokens. Unset, the profile decides: `openai-compatible` sizes a limit from the documents, and the other profiles send none and leave it to the endpoint. |
| `--min-interval SECONDS` | `LLOSSLESS_MIN_INTERVAL` | `0` | A pause between model calls. See [Notes for local models](#notes-for-local-models). |
| - | `LLOSSLESS_ENDPOINT_LABEL` | unset | A name for the endpoint. With a label, progress and error messages show an id made from the label instead of the endpoint's host name. Reports never contain the address either way. |

**Request profiles.** Every endpoint the tool has been run against speaks the OpenAI chat format, but they differ in which fields they accept. A profile is the set of fields sent. It is always your choice and is never guessed from the model name.

| profile | use it for | answer length field | `temperature` 0 | `seed` 0 | reasoning off |
|---|---|---|---|---|---|
| `openai-compatible` (default) | Ollama, vLLM and other OpenAI-compatible servers | `max_tokens` | sent | sent | `reasoning_effort: "none"` |
| `openai-reasoning` | OpenAI's reasoning models | `max_completion_tokens` | sent only with reasoning off | sent | `reasoning_effort: "none"`, and never together with `tool_call` |
| `anthropic` | Anthropic's API | `max_tokens` | not sent | not sent | `reasoning_effort: "none"` |
| `google` | Google's Gemini API | `max_completion_tokens` | not sent | not sent | not possible: list every role in `--thinking` |
| `subscription` | a program, with `--answer-with` | none | not sent | not sent | not possible: list every role in `--thinking` |

- **Repeatability.** Where `temperature` and `seed` are not sent, the endpoint is free to answer the same request differently each time. A run under `anthropic`, `google` or `subscription`, or under `openai-reasoning` with reasoning on, is not repeatable.
- **`subscription` answers in `prompt` mode only**, so its results are not directly comparable with the figures in [Measured results](results.md), which were measured in `json_schema` mode.
- **Gemini support is best effort.** It was measured on Google's free tier as a reference and is not re-tested with every change.
- A profile other than the default, and a field order other than `schema`, are printed in the report's Provenance block.

### Run control

For `merge` and `verify`:

| flag | what it does |
|---|---|
| `-o PATH`, `--output PATH` | Write the merged document here. `merge` only. |
| `--json PATH` | Also write the report as JSON, for a program to read. |
| `--html PATH` | Also write the report as one self-contained HTML page: the same content and the same verdict, laid out for reading. The page loads nothing from the network. |
| `--dry-run` | Build every prompt and count the planned calls. Make no request. Exits 0. |
| `--max-calls N` | Stop before making more than N model calls. Default 200. |
| `--cache` | Use the response cache. See [What the cache holds, and where](#what-the-cache-holds-and-where). |
| `--no-cache` | Ignore the cache and keep nothing from this run. Wins over `--cache`. |
| `--sweep-fidelity` | `merge` only. Run the merge at every fidelity level the endpoint can run and print one table. An HTTP endpoint runs five levels and leaves `sourced` out; a `claude` program route runs all six. |
| `--sweep-dir DIR` | With `--sweep-fidelity`, write `merged.LEVEL.md` and `report.LEVEL.json` for each level into DIR. |
| `--sample N` | A repeat number. It changes nothing in the request, only the cache entry, so a repeated run is answered by the model again and not by the cache. |
| `-v`, `-vv` | Say what is happening, on stderr. See [What it tells you while it runs](#what-it-tells-you-while-it-runs). |
| `--colour WHEN`, `--color WHEN` | `auto` (the default), `always` or `never`. |
| `-V`, `--version` | Print the version and exit. On `llossless` itself, before the command. |

For `serve`, with the details in [The web interface](web.md):

| flag | default | what it sets |
|---|---|---|
| `--port PORT` | `8765` | The port to listen on. `0` picks a free one and prints it. |
| `--host HOST` | `127.0.0.1` | The address to listen on. Any address other than this machine's own needs an account or an access token, or the server refuses to start. |
| `--work-dir DIR` | a `web` folder in the cache directory | Where submitted documents and their reports are kept. |
| `--workers N` | `1` | How many merges may run at once. |
| `--retention SECONDS` | `172800` (48 hours) | How long a finished run's files are kept. `0` keeps them until they are deleted by hand. `LLOSSLESS_RETENTION` sets the same. |

## Cache, keys and the network

### What leaves your machine

- The command line sends your documents to the endpoints you configure, and makes no other network request.
- With a local endpoint, nothing leaves the machine.
- With a hosted endpoint, the report says so in a note: "Document content left this machine."
- With a program route, the report says the documents were handed to that program.
- At `--fidelity sourced`, text from your documents can also appear in a web search or a page request made by the model.

### What the cache holds, and where

The response cache stores what was sent and what came back: each prompt, which contains your documents, and each answer, which contains the merge. A later run with an identical request is answered from the cache without a model call.

| how you run it | cache default | where it is |
|---|---|---|
| from the cloned repository, as in the README's install steps | on | `.llossless-cache/` in the repository folder |
| installed as a package | off | `~/.cache/llossless`, or `$XDG_CACHE_HOME/llossless` |

- `--cache` turns the cache on. `--no-cache` turns it off, and wins if both are given.
- `LLOSSLESS_CACHE_DIR` moves the cache to another folder.
- With the cache off, the run keeps nothing in the cache folder. An answer the tool could not read is still saved for debugging, in a temporary folder made for that one run, and the path is printed on stderr.
- One small file is written to the cache folder either way: `capabilities.json`, which records the answer format each endpoint accepted. It holds nothing from your documents.

If you work with confidential documents from the cloned repository, pass `--no-cache`.

### Keys and TLS

- **The key is read when a request is sent, and used only as that request's `Authorization` header.** It is never written to a report, a log line, the cache or an error message.
- **The key can stay where it already is.** `LLOSSLESS_API_KEY_ENV` names the variable that holds it, so a key that already lives in another variable does not have to be copied.
- **A key is never sent unencrypted to another machine.** If a key is set and the address is `http://` on any host other than this machine, the run is refused before the first call. Use the endpoint's `https://` address. `http://localhost` is exempt, because a local Ollama takes no key.
- **TLS verification cannot be turned off.** There is no `--insecure` flag. For a network that intercepts TLS, point `LLOSSLESS_CA_BUNDLE` at its CA bundle.
- **Redirects are not followed**, so a key cannot be forwarded to a host you did not configure.
- The standard proxy variables (`HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY`) are honoured.

## What it tells you while it runs

**The report is the only thing on stdout.** Everything in this section goes to stderr, so `> report.md` still leaves you something to watch, and the file is the same with or without it.

**Every run ends with a few lines that say what happened**, in words, including the exit code. A merge that failed, with stdout redirected:

```
Could not complete. Part of this run did not finish, so the report does not establish that the claims it did check are all there were.
  merge did not finish: merge: model did not return a usable response after 5 attempts: response contains no JSON object or array
  raw response written to /tmp/llossless-run-ioetucne/failures/20261005T173757Z-merge-0005-attempt5.txt
  nothing was written to merged.md: the merge step did not produce a document
  the full report went to stdout; exit code 2
```

A run that finished with a finding:

```
Finished, with problems. The report lists what was found.
  1 verbatim violation: an invariant-core token did not survive unchanged (see `## Structure`)
  merged document written to merged.md
  the full report went to stdout; exit code 1
```

The lines name what was found and how many, where the merged document went, and anything that limits the result: passages the merge declared it dropped, additions from the model's own knowledge, or a check that did not run.

**Verbosity:**

| flag | what you see |
|---|---|
| none | Only the closing lines, warnings and errors. |
| `-v` | Each step and each model call as it starts and finishes, with the time it took: reading the documents, the merge, one decompose per document, the two checking passes. |
| `-vv` | Also which file is which source, the full endpoint address, the fidelity level, cache hits and pauses. |

One line is printed even without `-v` when it changes what a clean result means: `depth coverage`, when the reverse check is off, and the web tools granted at `--fidelity sourced`.

**Colour** is `auto` by default: on when the stream is a terminal, off when it is redirected or piped, off when `NO_COLOR` is set to anything, and off under `TERM=dumb`. It is decided separately for stderr and stdout, so messages on a terminal are coloured while a redirected report stays plain. Errors are red. `--colour always` forces colour on, including in a redirected report. `--colour never` turns it off.

## Context windows

A model reads a limited amount of text per request: its context window, counted in tokens. The prompt and the answer have to fit in it together. A request that does not fit is a real risk, because some servers cut the start off an oversized prompt and answer anyway, without saying so.

**The tool checks before it sends.** It estimates the size of each request and compares it with the window. A request that does not fit is refused, and nothing is sent.

**Where the window figure comes from:**

| endpoint | what to do | what the tool does |
|---|---|---|
| a hosted API | State the window: `--window TOKENS` or `LLOSSLESS_WINDOW`. | Checks every request against your figure. It does not test whether the figure is true, so state the real one. The report's Provenance block marks the window as stated. |
| a local Ollama | Nothing, unless the window is too small. | Asks the server which window it serves, confirms the answer with one test request, then checks every request against it. |
| a program (`--answer-with`) | State the window. It is required. | Checks every request against your figure. |

**If the window cannot be established**, because the endpoint cannot be asked and no window was stated, the checking steps are refused:

```
UNMEASURED: the served context window for decompose could not be established, so decomposing source_a.md cannot be checked against it.
```

State the window with `--window`.

**If a request is too large for the window**, the run stops before sending it:

```
merging 2 sources at fidelity high needs 22256 tokens and 16384 tokens (measured) for qwen3:8b leaves room for 16384. Over by 5872. Nothing has been sent.
```

There are two ways out: serve a larger window (for Ollama, see [Notes for local models](#notes-for-local-models)), or split the documents. `--fidelity verbatim` reserves a little less room for the answer than the other levels, which helps only when the request is just over.

**How large a window a merge needs.** Under the default `openai-compatible` profile the tool reserves room for the longest answer the merge could give, which is several times the size of the documents. The figures below are the tool's own estimate for five published test pairs at the default fidelity `high`:

| pair | words in both documents | window the merge needs, in tokens |
|---|---|---|
| `tests/fixtures/structure_added` | 42 | 14,435 |
| `tests/handwritten/bip39` | 358 | 22,256 |
| `tests/handwritten/curry` | 483 | 28,877 |
| `tests/pairs/index_429` | 887 | 38,687 |
| `tests/pairs/rate_limits` | 1,809 | 55,667 |

Even the smallest pair needs more than 14,000 tokens, because the instructions and the reserved answer have a fixed part. Under the `anthropic`, `openai-reasoning` and `google` profiles no room is reserved for the answer, so only the prompt is checked: under 10,000 tokens for each of these pairs.

After a merge call, where the endpoint reports token counts, the tool also compares them with what it sent. An answer that used up the whole limit, or a prompt the endpoint counted at half its size or less, stops the run with an error instead of a report on a cut-off document.

## Notes for local models

These notes apply to a local Ollama, the default endpoint. A local model is the default because it needs no key, not because it merges best: see the results in the [README](../README.md) before relying on a small one.

- **Raise the context window.** Ollama's default window is usually too small for a merge. Start the server with a larger one, for example `OLLAMA_CONTEXT_LENGTH=32768`, which covers the first three pairs in the [table above](#context-windows). Ollama reads the variable once at startup, so restart the server after changing it.
- **Keep one request slot.** Ollama splits the window between parallel request slots (`OLLAMA_NUM_PARALLEL`). The tool sends one request at a time, so more than one slot only makes each request's share smaller.
- **A model that is not loaded yet is loaded for you.** The tool sends one empty request to load it, says so on stderr, and continues. The report's Provenance block then has a `Model loads` row. The load is not counted against `--max-calls`.
- **A model that is not fully on the GPU gets a warning.** The run continues, but expect it to be much slower. Behind a proxy, a model running on the CPU usually shows up as a proxy timeout.
- **If back-to-back calls overheat the graphics card**, `--min-interval SECONDS` adds a pause between calls. Leave it at 0 for a hosted endpoint.
- **Raise `--timeout` for long merges.** An error saying the endpoint "took the request and did not finish answering within 120s" means the model was too slow for the default. If the request was also too large for the window, raise the context window as well.

## For contributors

- **Where the defaults live.** Every default on this page is a constant in `src/llossless/config.py`, and the `--help` text is built from the same constants. The request profiles are the `PROFILES` table in `src/llossless/structured.py`.
- **How the merge's answer limit is sized.** `budget_tokens` in `src/llossless/merge.py` computes it from the documents and the fidelity level; `request_tokens` adds the prompt. These two produce the figures under [Context windows](#context-windows). Both count three characters as one token and do not run the model's tokenizer, so a vendor's own token count for the same request will differ.
- **Recording and replay flags are not on the installed command.** The test harnesses add them to build and replay the recorded corpus. `tests/responses/README.md` describes the corpus and its record format, including the endpoint id stored with each recording.
- **`--sample N`** is part of a recording's key and never of the request, which is how the harnesses record several samples of one request.
