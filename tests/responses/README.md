# Recorded model responses

This directory holds real answers from real models, one file per model call, saved exactly as they arrived and never edited. The tests and the three measurement harnesses replay these files instead of calling a model, so the suite runs with no model, no network and no GPU, and the figures in [Measured results](../../docs/results.md) can be checked against the files that produced them. This page says what is recorded, how to replay it, what the recordings show, how to read one file, and how to record again.

> **In short**
>
> - **697 recordings in four sets.** The current set is this directory plus `m7/`: 407 recordings of `Qwen/Qwen3.8-27B-FP8` ("the 27B"), made on 2026-09-24 and 25 over the sixteen fixtures in `tests/fixtures/`, three samples of every call. `m4/` and `pairs/` are earlier recordings of `qwen3:8b`.
> - **The decompose recordings replay today.** One offline command prints the decompose figures in full.
> - **The verify recordings do not replay.** Both verify prompts changed on 2026-09-26 and the verify calls have not been recorded again. A replay reports every figure that needs a verify answer as UNMEASURED, which means not checked: it is neither a pass nor a failure.
> - **Nothing replays `m4/` or `pairs/`.** They stay on disk because published figures were derived from them.
> - **One call has no usable recording.** A retry in the `attribution_invented` fixture never finished on the 27B, so two of the 166 verify probes were never measured. See [the call that could not be recorded](#the-call-that-could-not-be-recorded).

Four terms are used throughout. A **fixture** is one test case in `tests/fixtures/`: two short source documents, a merged document, and the expected results in `expected.json`. A **probe** is one statement in a fixture whose correct result was written down before any run. A **role** is one of the three jobs the model is given: `decompose` splits a document into claims, `merge` writes the merged document, and `verify` checks claims against a document, in both directions. A **recording** is one saved model call; the code and the harnesses' messages call it a cassette.

## How to replay the recordings

The three harnesses replay with `--offline`. A replay must name the model the recordings were made with, because the model id is part of every recording's key.

```sh
M=Qwen/Qwen3.8-27B-FP8
python3 tests/run_decompose.py --offline --model $M
python3 tests/run_verify.py    --offline --model $M
python3 tests/run_merge.py     --offline --model $M --merge-model $M --condition off
```

What each command does today, as run on 2026-10-06:

| Command | Reads | What it prints | Exit code |
|---|---|---|---|
| `tests/run_decompose.py` | the 130 decompose recordings in this directory | A result for each fixture and the full summary: 155 of 164 probes extracted, 9 of 16 fixtures clean. | **1** |
| `tests/run_verify.py` | nothing: no verify recording matches today's prompts | All 166 probes as UNMEASURED, and every summary figure as `0/0`. | **3** |
| `tests/run_merge.py` | the merge and decompose recordings in `m7/` | The claim count of each recorded merge. Forward coverage, evidence grounding and the reverse pass are UNMEASURED for all 48 merges. | **3** |

The exit codes mean the same in all three harnesses. They are the harnesses' own codes; the `llossless` command's exit codes are different and are in the [command reference](../../docs/reference.md#exit-codes).

| Code | Meaning |
|---|---|
| 0 | Everything was measured and every fixture passed. |
| 1 | Everything was measured and at least one fixture fell short. |
| 2 | The run did not measure: a recording was missing, the settings were wrong, or a call failed. |
| 3 | Nothing that was measured fell short, but something could not be measured. |

**Decompose exits 1, and that is the expected result.** Seven fixtures miss one or two probes each, and one document comes back with fewer claims than its fixture expects. The harness reports where the model falls short of the fixtures; the fixtures are not adjusted to the model. The summary it prints:

```
Decompose over the fixture set
  3 run(s) per document; probe figures are over the modal outcome.
  Claims extracted ...... 1582 over 3 run(s)
  Probes extracted ...... 155/164 (95%)
  Line refs correct ..... 155/155 (100%)  (within +/-2)
  Spans anchored ........ 1582/1582 (100%)
  Count bands met ....... 47/48 (98%)
  Nothing invented ...... 163/163 (100%)  (must_not_extract, any run)
  Fixtures clean ........ 9/16 (56%)
  Probe stability ....... 164/164 (100%)  (extracted or not, identically across 3 run(s))
  Claim counts stable ... 47/48 (98%)  (documents whose claim count never moved)
```

**Verify and merge exit 3 because the verify recordings are older than the verify prompts.** On 2026-09-26 the line in both verify prompts that states the field order was changed to name `claim_id`, and the verify role began sending an output limit. Both changes alter the key of every verify call, so no recorded verify answer matches a request made today. The harnesses detect this and report it instead of failing. `tests/run_verify.py` prints:

```
  UNMEASURED: 166 probe(s) across 16 fixture(s) -- prompt changed after recording; re-record deferred by operator ruling of 2026-09-26 -- 90 of 90 verify cassette(s) in tests/responses predate it: prompts/verify.md, now 9f352020c25f (51); prompts/verify_reverse.md, now 021f9beb4a23 (39)
```

`tests/run_merge.py` prints:

```
  UNMEASURED: forward coverage, evidence grounded and the reverse pass, over 48 of 48 unit(s) -- prompt changed after recording; re-record deferred by operator ruling of 2026-09-26 -- 97 of 97 verify cassette(s) in tests/responses/m7 predate it: prompts/verify.md, now 9f352020c25f (51); prompts/verify_reverse.md, now 021f9beb4a23 (46)
  Prompt-example leaks .. 0 unit(s)
  must_not_extract ...... 0 unit(s) violating   (any-run, not modal)

  Fixtures clean ........ 0/16 (0%)  (16 unmeasured, not counted)
```

Things to know when replaying:

- **`--offline` names the directory for you.** It is short for `--replay tests/responses`, and in `tests/run_merge.py` for `--replay tests/responses/m7`. `--replay DIR` replays any other directory.
- **`tests/run_merge.py` needs `--condition off`.** `m7/` holds merges made with thinking off only, and the harness's default is to run both conditions. Without the flag the run stops on the first thinking-on merge with exit code 2.
- **A missing recording stops the run.** The message starts `replay miss: no recorded response for role` and names the key and the file it looked for. A replay never falls back to calling a model.
- **A replay opens no connection.** `tests/test_client.py` checks that a replayed run does not even load the module that makes requests.
- **`--fixture NAME` runs one fixture**, and may be repeated. `--out FILE` writes the full result as JSON.
- **Every run ends with a Provenance block.** It states the run mode, the model, the decoding settings, the prompts, and how many calls were live, cached or replayed.

## What is recorded

Each set is one directory. A replay reads the files of one directory and not its subdirectories, so the sets cannot mix. The one exception is a subdirectory named `local/`, which a replay also searches when the directory itself has no answer. None exists today.

| Directory | Model | Recorded (UTC) | Recordings by role | Prompts it was recorded against | Replays today |
|---|---|---|---|---|---|
| `tests/responses/` | `Qwen/Qwen3.8-27B-FP8` | 2026-09-24 to 25 | 130 decompose, 90 verify | `prompts/decompose.md` `b4ec1e0c7ead`, which is today's file. `prompts/verify.md` at `b9ab404dd514` and `prompts/verify_reverse.md` at `7ba80700b114`, both since changed. | decompose: yes. verify: no. |
| `m7/` | `Qwen/Qwen3.8-27B-FP8` | 2026-09-25 | 45 decompose, 45 merge, 97 verify | `prompts/merge.md` recorded against `c33344d1450b`, which is today's file. Decompose and verify as in the row above. | merge and decompose: yes. verify: no. |
| `m4/` | `qwen3:8b` | 2026-08-08 | 65 decompose, 66 merge, 133 verify | `prompts/merge.md` at `f2a441dedc46`, `prompts/verify.md` at `bc987d3fb394`, `prompts/verify_reverse.md` at `cc3bbe9d49f5`, and today's decompose prompt. | no |
| `pairs/` | `qwen3:8b` | 2026-08-30 | 8 decompose, 4 merge, 14 verify | not stated in the directory | no |

A prompt digest is the first twelve hex characters of the SHA-256 of the prompt file, so `sha256sum prompts/merge.md` shows today's. Today's four prompts are `prompts/decompose.md` `b4ec1e0c7ead`, `prompts/merge.md` `c33344d1450b`, `prompts/verify.md` `9f352020c25f` and `prompts/verify_reverse.md` `021f9beb4a23`. The first line of every harness run prints these digests, cut to eight characters. The Provenance block at the end prints another value for the merge and verify prompts: there the file is hashed together with the fidelity-level rules that are inserted into it.

**The current set is the first two rows, 407 recordings from one session.** They share one endpoint id and one revision stamp, and the stamp carries no `-dirty` mark. Every one was made at temperature 0 and seed 0, with the structured-output tier `json_schema`, with thinking off for every role, and with answers read under field order `any`. None of the 407 answers contains a reasoning block. [Measured results](../../docs/results.md#reference-configuration) describes the endpoint.

**This directory holds the decompose and verify measurements.** Each fixture's three documents were decomposed, and each fixture's hand-written merged document was verified against its sources. `tests/run_decompose.py` and `tests/run_verify.py` replay it.

**`m7/` holds the merge measurement.** The model merged each fixture's two sources, and that merge was decomposed and verified. `tests/run_merge.py` replays it. Beside the recordings it has:

- `m7/merges/`: the 48 merged documents the model wrote, as Markdown, named `<fixture>-off-<sample>.md`;
- `m7/journal.jsonl`: 192 lines, one for each step of each merge (merge, decompose, verify forward, verify reverse), with the recording's key, the sample number, the output limit sent and the seconds the step took.

## What the recordings show

[Measured results](../../docs/results.md) is the published account of these figures and says what they do and do not prove. This section gives the detail behind them, fixture by fixture.

| Measurement | Figures | Reproducible today |
|---|---|---|
| Decompose, this directory | 155/164 probes extracted, 1582/1582 quoted spans found in their document, 47/48 documents with a claim count in the expected band, none of 163 statements that must not be extracted was extracted, 164/164 probes the same in all three samples | yes |
| Verify, this directory | 164/164 probes with the expected verdict, 162/162 quotes found in the file the verdict names, 164/164 verdicts the same in all three samples, 2 probes not measured | no: these are the figures as measured at recording |
| Merge, `m7/` | forward coverage 314/363, 324/327 quotes found in the file the verdict names and 3 found in no file, 0 of 441 claims of the merges in neither source, 9 of 16 fixtures clean | no: these are the figures as measured at recording |

Every figure is over the modal answer of three samples: the answer at least two of the three gave. Three different answers count as a failure, not as a tie to break.

### Fixture by fixture

Decompose counts the probes extracted over the fixture's three documents. Merge counts the source probes the model's merge carried, for samples 0, 1 and 2.

| Fixture | Decompose | Merge, as recorded | Where it fell short |
|---|---|---|---|
| `attribution_invented` | 6/7 | 5/5, 5/5, 5/5 | Decompose missed `m-tls-attributed` in the merged document. Two of its verify probes were never measured; see [below](#the-call-that-could-not-be-recorded). |
| `attribution_swapped` | 2/2 | 1/2, 1/2, 1/2 | The sources disagree on the read timeout. The merge kept one value, so `b-read-timeout` is contradicted. |
| `concatenated` | 15/15 | 9/10, 10/10, 10/10 | Sample 0 carried `b-casting-year` only in part. The samples disagree, so the harness calls the fixture unresolved. |
| `conflict_surfaced` | 9/11 | 7/8, 7/8, 7/8 | Decompose missed both attributed timeout statements in the merged document. The merge kept one connect timeout. |
| `contradiction` | 8/8 | 7/8, 7/8, 7/8 | The merge kept one connect timeout, so `b-connect-timeout` is contradicted. |
| `dedup` | 10/10 | 6/6, 6/6, 6/6 | |
| `disjoint_domains` | 14/16 | 6/12, 6/12, 6/12 | Decompose missed one probe in each source. The merge is source A alone: all six probes from source B are missing. |
| `disjoint_sources` | 15/16 | 6/12, 6/12, 6/12 | Decompose missed `a-winter-dormant` and returned 14 claims for `disjoint_sources/source_a.md`, below its band of 16 to 32. The merge is source A alone. |
| `dropped_claim` | 10/10 | 10/10, 10/10, 10/10 | |
| `hallucination` | 8/8 | 5/5, 5/5, 5/5 | |
| `list_structure` | 10/11 | 8/8, 8/8, 8/8 | Decompose missed `a-retry-attempts`. |
| `numeric_drift` | 5/5 | 4/5, 4/5, 4/5 | The sources disagree on the connection limit. The merge kept one value. |
| `ordering_only` | 10/11 | 8/8, 8/8, 8/8 | Decompose missed `merged-backoff`. |
| `paraphrase` | 10/11 | 8/8, 8/8, 8/8 | Decompose missed `b-log-format`. |
| `restated` | 15/15 | 10/10, 10/10, 10/10 | |
| `structure_added` | 8/8 | 4/4, 4/4, 4/4 | |
| **All sixteen** | **155/164** | **104 + 105 + 105 = 314 of 363** | Nine fixtures are clean in each measurement, and they are not the same nine. |

Merge coverage is 49 short of 363. In the four fixtures whose sources disagree on a value, the merge kept one value and the other source's probe reads as contradicted: 12 of the 49. That is what a merge at the default fidelity level `high` is asked to do, so it is not a defect of the merge. The two `disjoint` fixtures are a real loss, 36 of the 49: the model returned one source and left the other out. The last one is the partly carried probe in `concatenated`.

Verify, as recorded, gave the expected verdict on every measured probe of every fixture.

### Why every call was recorded three times

Temperature 0 and a fixed seed do not make a model repeat itself, so each call was made three times and the samples are compared. In the current set:

- **Decompose:** 42 of the 43 distinct fixture documents got the same answer, byte for byte, in all three samples.
- **The one that differed is `restated/merged.md`,** the only fixture document a model wrote. Its claim count came back at 43, 50 and 43. In sample 2 the first answer held the same 43 claims as the other two samples, but one claim lacked its line number, so validation rejected it. The retry returned 50 claims. The count that moved is the answer to a retry, not a different answer to the same request.
- **Verify:** every request got the same answer in all three samples.
- **Merge:** the model wrote the same merged document in all three samples for 15 of the 16 fixtures. For `concatenated` it wrote two different ones.

### The call that could not be recorded

In `attribution_invented`, the reverse check covers two probes, `m-tls-attributed` and `m-read-timeout`. The 27B's first answer is recorded in all three samples. It gives the verdict `CONTRADICTED` for the first probe and quotes no evidence, which validation rejects. The retry that follows such a rejection ran until the hosting platform cut it off, in 7 of 8 attempts, so the retry has no recording and the two probes have no verdict.

`tests/run_verify.py` lists the retry's three keys, one per sample, in `UNRECORDABLE` and reports the two probes as UNMEASURED. That is why the verify figures cover 164 of the 166 probes, and why `attribution_invented` is counted neither as a clean fixture nor as a failed one. The verify role now sends an output limit, so the same runaway would be cut at that limit.

### What a reviewer should know before counting files

- **Byte-identical documents are decomposed once per sample.** The sixteen fixtures have 48 documents but 43 distinct ones, because fixtures share sources: `conflict_surfaced/source_a.md`, `contradiction/source_a.md` and `dropped_claim/source_a.md` are one text, as are `conflict_surfaced/source_b.md` and `contradiction/source_b.md`, `attribution_invented/source_a.md` and `attribution_swapped/source_a.md`, and `dedup/source_b.md` and `structure_added/source_b.md`. So 43 x 3 = 129 decompose calls, plus one retry, make the 130 files.
- **Two fixtures share their merge requests.** `conflict_surfaced` and `contradiction` have the same two sources and differ only in their hand-written merged document. In `m7/`, 45 merge recordings therefore answer 48 merges.
- **A retry is a recording of its own.** When validation rejects an answer, the next attempt is a new request with the rejection appended, and it gets its own key and file with `meta.attempt` 2. The current set holds eleven: one decompose and three verify in this directory, seven verify in `m7/`.
- **The three samples of one request have identical `request` blocks.** The sample number is in the key and not in the file. `m7/journal.jsonl` maps each key to its fixture and sample.

## What one recording holds

One JSON file per call, named `<role>-<first 16 hex characters of the key>.json`.

```json
{
  "schema_version": 2,
  "recorded_at": "2026-09-24T22:30:58+00:00",
  "key": "<64 hex characters>",
  "request":  { "role": "decompose", "model": "Qwen/Qwen3.8-27B-FP8", "tier": "json_schema",
                "messages": [ ... ], "schema": { ... }, "temperature": 0.0 },
  "response": { "raw": "<the response body, as text>", "http_status": 200 },
  "meta":     { "endpoint_id": "1ce4c8ef780f", "endpoint_id_scheme": 2, "claimcheck_source": "<revision>",
                "latency_ms": 11696, "attempt": 1, "field_order": "any" }
}
```

| Field | What it holds |
|---|---|
| `schema_version` | `2`. A file with another version is not read. |
| `recorded_at` | When the file was written, in UTC. |
| `key` | The identity of the request. See [the key](#the-key). A replay finds a recording by this field, not by the file name. |
| `request.role` | `decompose`, `merge` or `verify`. Both verify directions are recorded under `verify`. |
| `request.model` | The model id as it was sent. |
| `request.tier` | How structured output was requested: `json_schema`, `tool_call` or `prompt`. Every recording here is `json_schema`. |
| `request.messages` | The messages sent, with the prompt already filled in. A retry has a second message that quotes the rejection. |
| `request.schema` | The JSON schema the answer had to satisfy. |
| `request.temperature` | `0.0` in every recording here. |
| `response.raw` | The response body exactly as the endpoint returned it, before any parsing. For these endpoints it is a chat-completion object, as text. |
| `response.http_status` | `200` in every recording here. A failed call is not recorded. |
| `meta.endpoint_id`, `meta.endpoint_id_scheme` | An opaque id for the endpoint that answered. See [the endpoint id](#the-endpoint-id). |
| `meta.claimcheck_source` | The revision of the code that made the recording. It ends in `-dirty` if tracked files had uncommitted changes, and in `-unknown` if git could not be asked. The field keeps the name it was given before the tool was renamed. |
| `meta.latency_ms` | How long the call took, in milliseconds. |
| `meta.attempt` | `1` for a first answer, and a higher number for a retry after a rejected answer. No recording here is above `2`. |
| `meta.field_order` | `schema` or `any`: whether the recording run required the answer's fields in the schema's order. A replay never reads an answer more strictly than its recording run did. The current set is stamped `any`; `m4/` and `pairs/` predate the field, and for them the replaying run's own setting applies. |

The code that writes and reads these files is `src/llossless/cassette.py`.

### The key

The key is the SHA-256 of these eleven values, written as compact JSON with sorted names: the role, the model id, the tier, the SHA-256 of the prompt, the messages, the schema, the temperature, the seed, the output limit (`max_tokens`), whether thinking was on, and the sample number. The prompt's hash covers the prompt file and, for the merge and verify prompts, the fidelity-level and title rules inserted into it.

- **Any change to what is sent changes the key.** Edit a prompt, a schema or a fixture document and the old recording no longer matches. The run reports a replay miss and never serves the old answer.
- **Five of the eleven are not stored in the file:** the prompt's hash, the seed, the output limit, the thinking flag and the sample number. A file therefore cannot be re-keyed from its own contents alone.
- **The sample number changes nothing in the request.** It is in the key so that three identical requests are three recordings, and not one recording served three times.
- **Two more values enter the key only when they are not the default:** the request profile, and a digest of the command when a program answers in place of an endpoint. Every recording here was made with the defaults.
- **The endpoint is not in the key.** The same request to another machine has the same key.

### The endpoint id

`meta.endpoint_id` is twelve hex characters. It answers one question, whether two recordings came from the same endpoint, without publishing an address. No recording contains an address, a URL, a header or an API key; `tests/test_client.py` checks that.

The id has been made by two rules, and `meta.endpoint_id_scheme` says which:

| Scheme | In the file | The id is the start of the SHA-256 of | Used by |
|---|---|---|---|
| 2 | `"endpoint_id_scheme": 2` | the endpoint's scheme, host, port and path | this directory and `m7/` |
| 1 | the field is absent | the host name alone | `m4/` and `pairs/` |

Under both rules, a name given in `LLOSSLESS_ENDPOINT_LABEL` is hashed in place of the address, so that an endpoint whose address changes on restart keeps one id. A scheme 1 id cannot be converted to scheme 2, because a recording holds the id and never the address, so the two kinds cannot be compared. The three ids on disk are `1ce4c8ef780f` for the current set, `49960de5880e` for `m4/`, which is the scheme 1 id of `localhost`, and `1c859caa0f73` for `pairs/`.

## How to record again

Record again when a prompt, a schema or a fixture document changes, or to add a fixture. Recording needs a running OpenAI-compatible endpoint that serves the model; the [command reference](../../docs/reference.md) says how to point the tool at one, and documents every flag used below that is not in the table. The flags in the table exist only in the harnesses under `tests/`, not in the installed `llossless` command.

```sh
M=<model id>
python3 tests/run_decompose.py --record tests/responses --model $M --structured json_schema --no-cache
python3 tests/run_verify.py    --record tests/responses --model $M --structured json_schema --no-cache
python3 tests/run_merge.py     --record tests/responses/m7 --journal tests/responses/m7/journal.jsonl \
    --model $M --merge-model $M --condition off --structured json_schema --no-cache
```

| Flag | What it does |
|---|---|
| `--record DIR` | Writes each answer to `DIR`. If a file for the same key is already there, that file is kept and the new answer is not written. |
| `--force` | With `--record`, overwrites the existing file. |
| `--mixed-sources` | With `--record`, allows writing into a directory whose recordings carry another revision stamp. |
| `--replay DIR`, `--offline` | Serve every call from recordings. See [How to replay the recordings](#how-to-replay-the-recordings). |
| `--samples N` | How many times each call is made. The default is 3. |
| `--fixture NAME` | Runs one fixture only. It may be repeated. |
| `--condition off` | `tests/run_merge.py` only. Whether merge thinking is `off`, `on` or `both`. The default is `both`. |
| `--journal FILE` | `tests/run_merge.py` only. Appends one line per step to `FILE`, and on a restart skips every merge the file lists as finished. |

**What a run costs.** Add `--dry-run` to a command first: it prints how many calls the run plans and makes no request. Today it plans 144 decompose calls, 87 verify calls and at most 216 calls for the merge run. The merge plan is above the default limit of 200 calls a run, so raise `--max-calls` for it. The current set was recorded against a hosted endpoint with no pause between calls. Going by the first and last `recorded_at` of each run, the decompose run took about 78 minutes, the verify run about 91 minutes and the merge run about two hours. A single call averaged 27 to 45 seconds, depending on the role.

Rules for a recording run, each with its reason:

1. **Commit first, and do not commit again until every run into one directory is done.** Each run stamps its recordings with the revision it started from, and `--record` refuses a directory that already holds recordings with another stamp. The refusal reads `holds cassettes recorded by another revision`. A tree with uncommitted changes is stamped `-dirty`, which counts as another revision.
2. **Fix the tier with `--structured json_schema`.** Without it the tier is probed, and a refusal in the middle of a run moves the run down to a weaker tier. The tier is part of the key, so the directory would then hold two halves that do not replay together.
3. **Record three samples.** The figures are modal answers of three, and a single sample cannot show whether an answer repeats.
4. **Use `--no-cache` for a fresh recording.** Without it, a request that is already in the local response cache is answered from there and written to the directory as if it had just been made. That is how an interrupted run resumes, and it is wrong for a recording meant to be new.
5. **Do not expect `--record` to fill gaps.** It never reads the directory it writes to: every call is made again. In this directory the decompose and verify runs are independent, so one role can be recorded again alone: delete that role's files and run its harness with `--mixed-sources`, because the other role's files carry an older stamp. In `m7/` the roles depend on each other: decompose and verify run on the merge the model has just written, and a new merge can differ from the recorded one. Record `m7/` whole, from an empty directory.
6. **Remove the old journal before recording `m7/` again.** Given the journal that is in `m7/` today, the harness would skip all 48 merges as finished.
7. **Add `--field-order any` for a server that returns fields in another order than the schema's.** The current set was recorded that way: its answers list their fields alphabetically. Each recording is stamped with the setting, so a replay reads it the same way.
8. **Run the harnesses one after another.** Each sends one request at a time, and a local model server shares its context window between parallel requests. For a local graphics card that overheats, `--min-interval SECONDS` adds a pause between calls.
9. **Keep one model in a directory, and delete the recordings that new ones replace.** The tests read the model id from the recordings and replay a directory under that one id, so recordings of a second model for the same role make the replay impossible. A replaced recording is never served, but the checks that read the whole directory still count its model, its revision and its prompt.
10. **Never edit a recording, and never change a fixture's expected results to fit a model.** A harness that exits 1 is reporting a result.

**To bring the verify recordings up to date,** record verify again in this directory and record `m7/` whole, as rule 5 describes. `tests/stale_corpus.py` lists the two prompt changes that are waiting for it in `HELD_BACK`, and those entries are removed when the new recordings arrive. The three keys in `UNRECORDABLE` in `tests/run_verify.py` belong to the old prompts.

**To add a fixture,** record it with the model the directory already holds, `Qwen/Qwen3.8-27B-FP8`: add `--fixture NAME` and `--mixed-sources` to the commands above. Here the journal in `m7/` stays: the new fixture's merges are not in it, so they run and are appended.

## Earlier recordings

### `m4/`

`m4/` is the merge measurement of 2026-08-08, made with `qwen3:8b` on a local Ollama server: the twelve fixtures that existed then, with merge thinking off and on, three samples each, so 72 merges. Half of its 66 merge recordings carry a reasoning block.

Nothing replays it. Its merge prompt has been rewritten since, so no run asks for its merge keys, and its decompose and verify recordings were made on merged documents that only those merges produced. `tests/test_client.py` checks both that six of its merge keys no longer resolve and that the files are still there.

What it is still used for:

- **The concatenation counts in [Measured results](../../docs/results.md#the-number-not-to-quote-alone).** `tests/analyse_merges.py` reads the 72 merged documents in `m4/merges/` and finds that 14 of 66 eligible merges are the two sources placed one after the other. `tests/measure_merges.py` reads the same documents and counts 23 of 66.
- **The latency and reasoning figures on that page.** `m4/journal.jsonl` has 288 lines, one for each step of each merge, with the seconds each took.
- **Its own result.** `tests/responses/m4/sweep.json` is the graded result of the run: forward coverage 243/243 with thinking off and 237/243 with thinking on.

Three things to know when reading it:

- **Two `.json` files in `m4/` are not recordings:** `sweep.json` and `sweep-attempt5.json` are results written by the harness. Together with `sweep.log`, `sweep-attempt3-aborted.log` and the empty marker `FINISHED` they are the record of how the run went.
- **The run took several attempts, and later ones resumed from the response cache.** 94 of the 288 journal lines are marked `cached`: the answer came from the cache, not from a new call.
- **`conflict_surfaced` and `contradiction` share their merge requests here too,** so 66 merge recordings answer the 72 merges.

### `pairs/`

`pairs/` holds 26 recordings of `qwen3:8b` from 2026-08-30, made on a hosted endpoint for two of the document pairs in `tests/pairs/`: `index_429` and `trace_names`. All four of its merge recordings carry a reasoning block. Its revision stamp ends in `-dirty`, so it was recorded from a tree with uncommitted changes. Nothing replays it. [Measured results](../../docs/results.md) counts its four merge recordings among the recorded merge calls that carry a reasoning block.

### Recordings that were replaced

Until 2026-09-25 this directory and `m7/` held recordings of `qwen3:8b`, 528 files in all. They were deleted when the 27B set replaced them, because a directory replays under one model. Their figures cannot be reproduced from this copy. [Measured results](../../docs/results.md#other-measurements-this-page-does-not-use) quotes the last of them and says why they are not comparable with the current ones. Its paragraph on repeatability adds one more: on `qwen3:8b` the document whose claim count moved between samples was `disjoint_sources/merged.md`, at 18, 17 and 18.
