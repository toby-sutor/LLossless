# Recorded model responses

Every file in this directory is a real response from a real model, captured
once and committed. Nothing here is hand-written, edited, or synthesised. That
is the point: the measurements grade a model's actual output, so if these files
were touched the numbers they print would be numbers about me rather than about
the model.

Replaying them makes every result reproducible on a machine with no GPU, no
network, and no endpoint. The root corpus and `m7/` were recorded against
`Qwen/Qwen3.8-27B-FP8`, and a replay has to name that model, because the model
is in the cassette key (`tests/replay_models.py` reads it from the cassettes
for the tests and audits that replay them):

```sh
M=Qwen/Qwen3.8-27B-FP8
python3 tests/run_decompose.py --offline --model $M   # exits 1: 9/16 fixtures clean
python3 tests/run_verify.py    --offline --model $M   # exits 3: every probe UNMEASURED (re-record held back)
python3 tests/run_merge.py --condition off --offline --model $M --merge-model $M   # exits 3: verify UNMEASURED (re-record held back)
```

Decompose exits 1 on purpose. The runner reports the fixtures the model does not
satisfy rather than passing, and an exit 0 there would mean the count bands had
been loosened to fit the model, which is the one thing this corpus exists to
prevent, and which has not been done. Seven fixtures miss one or two probes
each, nine in all, and `disjoint_sources/source_a.md` comes back under its
count band.

**Since 2026-09-26 the verify cassettes do not replay.** The field-order
line of both verify prompts now names `claim_id`, which moves them to
`prompts/verify.md` `9f352020c25f` and `prompts/verify_reverse.md` `021f9beb4a23`,
and the verify role sends an output ceiling. Both re-key every verify call,
and the operator has held the re-record back. So every replay reports the
verify probes UNMEASURED with that reason, and the merge harness replays its
merges and decomposes and reports its three verify figures UNMEASURED
(`tests/stale_corpus.py`). The verify and merge figures below are what these
cassettes measured before that change.

Verify exits 3, the suite's code for "could have been checked and was not".
Every probe it measured is right, 164/164 strict. The two it did not measure
are `attribution_invented`'s merged-document probes: that reverse call ran
away on the 27B in 7 of 8 attempts and was cut by the platform, so it has no
cassette. `tests/run_verify.py` names its three sample keys in `UNRECORDABLE`,
and every replay reports the two probes UNMEASURED, never as a pass and never
as a miss to fix by re-recording.

Merge exits 1. Its forward coverage is 314/363 at thinking off, the only
condition recorded. Seven fixtures fall short, and read the reason before the
count: `conflict_surfaced`, `contradiction`, `attribution_swapped` and
`numeric_drift` lose the value the merge did not choose, which is what a merge
at `high` is licensed to do; `disjoint_domains` and `disjoint_sources` carry
none of source B's six probes, in all three samples; `concatenated` is
unresolved across its three samples. The exit code says a probe was missed; it does not
say the merges that passed were good.

`--offline` is `--replay tests/responses`. A replayed run never imports
`llossless.transport` — `tests/test_client.py` asserts that in a subprocess
rather than taking it on trust. Replay reproduces the recording run's result
blocks exactly; only the provenance header differs, and it is *required* to,
since it records run mode and call counts.

## Every call was recorded three times

A single recorded run produces a number that cannot be checked, only believed.
Temperature 0 and a fixed seed are supposed to make a model deterministic and do
not: the same request to the same endpoint can come back different. So each
call was made three times and every figure below is over the **modal** answer,
with the spread reported alongside it.

Three mechanisms make that measurement honest rather than decorative:

- **`sample` is part of the cassette key.** It is the one key component that
  determines nothing about the request — it never reaches the request body, and
  the endpoint cannot tell samples apart. It exists so that three identical
  requests are three recordings instead of one recording served three times.
  Without it a repeat run would look perfectly stable by construction.
- **The dedupe cache is reset between sweeps.** Byte-identical fixture documents
  are decomposed once per sweep, never once per session. Sharing that cache
  across sweeps would serve sample 1's claims as sample 2's answer for every
  duplicated document and manufacture the stability being measured — the same
  trap the `sample` key closes, one level up.
- **The mode is a strict majority, not a plurality.** Two of three agreeing is a
  verdict; three different answers is `NO-MAJORITY`, which is graded as failing
  both strict and lenient scoring rather than being resolved by tie-break.
  Grounding is pessimistic in the same spirit: a probe counts as grounded only
  if *every* run that produced the modal verdict located its evidence.

**Result, on the 27B: verdicts were fully stable and claim segmentation was
not, on one document.** Verify's verdict stability is 164/164, every measured
probe returning the same label in all three runs. Decompose is stable at the
probe level, 164/164, but **one document out of 48 returned a different number
of claims between runs**: `restated/merged.md`, at 43, 50 and 43.

- It is the one fixture document a model wrote. `restated`'s merge is real
  model output that states every fact twice, in two people's wordings, and it
  is the positive check 9's claim-level half exists for: the 27B's claim lists
  repeat 13, 15 and 13 claim texts on two lines each, and
  `tests/test_reconcile.py` holds that as its recorded must-fire.
- **Samples 1 and 3 are identical**, claim for claim. Sample 2 is the outlier,
  with 50 claims, 32 of them identical to sample 1's in text and line.
- Only the count moved. No probe changed its extracted/not-extracted status
  anywhere in the corpus, which is why probe stability is 164/164 while claim
  counts are 47/48.

**On `qwen3:8b` it was a different document, and always the same fixture.**
Three three-sample `qwen3:8b` corpora were recorded across two prompt versions
before this one, and every one of them moved on exactly one document, always in
`disjoint_sources`, while probe stability held at 107/107:

| corpus | claims | claim counts stable | the document that moved |
|---|---|---|---|
| old, recorded 2026-08-08 | 676 | 35/36 | `disjoint_sources/merged.md`: 17, 18, 17 |
| delimited | 670 | 35/36 | `disjoint_sources/source_b.md` — 13, 12, 12 |
| reverted | 677 | 35/36 | `disjoint_sources/merged.md` — 18, 17, 18 |

The last of those is the corpus the 27B replaced, where the narrative fixture's
merged document came back at 18, 17 and 18. On the 27B that document did not
move. The history of those corpora is in the sections below and in git; their
cassettes are deleted and nothing replays them.

## What the runs measured

Decompose, three runs per document, at `prompts/decompose.md` `b4ec1e0c7ead`:

```
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

`python3 tests/run_decompose.py --offline --model Qwen/Qwen3.8-27B-FP8`
reproduces all of it: 0 live, 0 cached, 130 replayed.

Verify, over the modal verdict of three runs:

```
UNMEASURED: attribution_invented/m-tls-attributed, attribution_invented/m-read-timeout -- a runaway on the 27B; not recordable: it ran away in 7 of 8 attempts and the platform cut it
Strict accuracy ....... 164/164 (100%)
Lenient accuracy ...... 164/164 (100%)
Findings derived ...... 164/164 (100%)
Evidence grounded ..... 162/162 (100%)  (of SUPPORTED and CONTRADICTED)
  transcription error . 0  (span is in no target file)
  attribution error ... 0  (span is real, wrong file named)
Evidence as declared .. 84/84 (100%)
Source file named ..... 28/28 (100%)  (of probes declaring one)
Verdict stability ..... 164/164 (100%)  (identical across 3 run(s))
source_to_merged      121/121 (100%) strict
merged_to_sources     43/43 (100%) strict
Guard fixtures clean .. 10/10 (100%)  (no over-flagging)
Fixtures clean ........ 15/15 (100%)  (1 partly unmeasured, not counted)
```

0 live, 0 cached, 90 replayed: every verify cassette in this directory.
Read `Fixtures clean` before the percentages, and read its note: a fixture is
the unit a defect is planted in, and `attribution_invented` is in neither half
of that figure, because two of its probes were never read.

Merge, from `m7/`, three samples of each fixture at thinking off:

```
Forward coverage
  thinking off      .... 314/363 (87%)
Prompt-example leaks .. 0 unit(s)
must_not_extract ...... 0 unit(s) violating   (any-run, not modal)
Evidence grounded ..... 324/327 (99%)
  transcription error   3
  attribution error     0
Reverse (advisory) .... 0 claim(s) in neither source, of 441 extracted

Unresolved (the samples would not settle it)
  concatenated

Fixtures clean ........ 9/16 (56%)
```

0 live, 0 cached, 199 replayed. The `qwen3:8b` figures these replaced predate
2026-09-25 and are not in this copy; the first decompose and verify runs are described below.

## What was recorded

| | |
|---|---|
| Model | `Qwen/Qwen3.8-27B-FP8` |
| Server | vLLM, OpenAI-compatible `/v1/chat/completions`, a 32768-token window |
| Endpoint | `1ce4c8ef780f` — hosted, named once through `CLAIMCHECK_ENDPOINT_LABEL` (id scheme 2), one id across all 407 |
| Structured output tier | `json_schema`, **pinned**; field order `any`, stamped on every cassette as `meta.field_order` |
| Decoding | temperature 0, seed 0, thinking **off** for every role, merge included |
| Samples | 3 per call |
| Source | a clean tree of 2026-09-24: master of that day plus the decompose output ceiling and a revised verify conflict example; one `claimcheck_source` across all 407 |
| `decompose-*` | 130 cassettes, `prompts/decompose.md` `b4ec1e0c7ead` — recorded 2026-09-24, 129 calls and 1 schema-repair second attempt, 0 errors, 4681 s unpaced |
| `verify-*` | 90 cassettes — `prompts/verify.md` at `b9ab404dd514` and `prompts/verify_reverse.md` at `7ba80700b114`, the prompts before the change of 2026-09-26, composing at `off` to the reported `2c2a9a0ee6dd` and `7f655f15e201` — recorded 2026-09-25, 87 calls and 3 schema-repair second attempts, 5485 s unpaced. Three planned calls have no cassette: `attribution_invented`'s reverse call, once per sample (below) |
| `m7/` | 187 cassettes in a subdirectory of their own — 45 `decompose-*`, 45 `merge-*`, 97 `verify-*` — `prompts/merge.md` recorded against `c33344d1450b`, the other three prompts as above, verify composing at `high` to `5afca8163bfa` and `cb2face6b7f4` — recorded 2026-09-25 at thinking off only, 184 live calls and 15 answered from the recording cache, 7 repairs, 0 errors, 7231 s unpaced; plus `merges/`, the 48 merged documents, and `journal.jsonl`, 192 records |
| `m4/` | 264 cassettes in a subdirectory of their own, `prompts/merge.md` at `f2a441dedc46` plus the three above, unchanged; recorded 2026-08-08, 194 live steps, 3 repairs, 0 errors, 4 h 40 min across five attempts |
| `pairs/` | 26 cassettes, `qwen3:8b`, recorded 2026-08-30 against a labelled pod of its own; nothing here re-recorded them |

Cassettes are named for the role that made the call, so the two passes share
this directory without colliding.

**`m7/` is the merge corpus, and it supersedes `m4/` for replay but not as the
record of the `m4/` run.** `tests/run_merge.py`'s `CASSETTES` points here, and `--offline`
replays all of it, decompose, merge and verify. It holds 48 merge units over 45
merge keys: `conflict_surfaced` and `contradiction` share both sources, so
their merge requests are byte-identical and three cassettes answer six units.
There is no thinking-on condition: merge thinking was ruled off, so
`run_merge.py --offline` needs `--condition off`, its default being `both`.
`m4/` stays on disk unchanged: it is what the `m4/` merge run, described below,
was measured against.

**One request is not recordable.** `attribution_invented`'s reverse verify call,
over its two merged-document probes (`m-tls-attributed`, `m-read-timeout`), ran
away on the 27B in 7 of 8 attempts: about 11,000 characters of content, no
finish reason, cut by the platform at about 275 s. The eighth, outside the
recording, answered cleanly once. It was not retried further and has no
cassette, in any of its three sample keys. `tests/run_verify.py` names those
keys in `UNRECORDABLE`, and a replay that misses on one reports the two probes
UNMEASURED with the reason, never as a pass and never as a miss to fix by
re-recording; a miss on any other key is still fatal. The fixture's forward call
was recorded and is graded. A runaway was bounded at recording time only by the
platform's cut; the output ceiling the verify role now sends bounds it, and is
one of the changes that re-keyed every verify cassette.

Three recorded properties are deliberate. The endpoint was named once through
`CLAIMCHECK_ENDPOINT_LABEL`, so that a restart mid-run could not stamp two ids
into one directory. It was recorded **unpaced**, because `--min-interval` is
the local card's thermal gap and not a project setting, and
serially. And the tier was **pinned** with `--structured json_schema` rather
than probed, so that a single rejection could not latch the whole run down to a
weaker decoding mode part-way through.

**What this replaced.** Until 2026-09-25 the root corpus and `m7/` were
`qwen3:8b`, Q4_K_M, on Ollama: root 111 `decompose-*` and 84 `verify-*`,
`m7/` 72 `decompose-*`, 81 `merge-*` and 144 `verify-*` over both thinking
conditions, and a read-time overlay, `local/`, of 18 and 18 for `concatenated`
and `restated`. All 528 were deleted on purpose on 2026-09-25: the model is in
the cassette key, so nothing replaying the 27B corpus could reach them, and
keeping them would have kept a second model under one directory's replay.
Their recording records, the mixed-source and `-dirty` provenance stamps, and
the prompt moves that orphaned the corpora before them are kept in the
project's git history.

**The `m4/` corpus is a subdirectory, and a different recording from the one
above in everything but temperature, seed and samples.** `Store._load_index`
globs `*.json` non-recursively, so `tests/responses/` does not see `m4/` and
neither corpus becomes a mixture of the other. It is `qwen3:8b` on the local
card, at the 4096-token window Ollama served then. Within it: the tier was
**pinned** with `--structured json_schema` rather than probed, after a probe
latched to a weaker rung mid-run and split a previous attempt's corpus in half;
thinking is **both** conditions rather than off, since the merge step is the
thing that run compares; and it is the only one in this project recorded across
more than one process.

**The `m4/` merge cassettes no longer replay, and the digest above is history
rather than a claim about the current tree.** A later revision rewrote the merge prompt for
segmented sources and a fidelity level, which moves `prompt_sha256` and so moves
every merge key — the orphaning the milestone planned for, not a fault.
A later edit then moved the file a second time, cutting the reason cap to 80
characters and widening the verbatim numeric rule to numbers that carry no
unit, reaching `ee7340edb62a`. Two further edits moved it a third and a
fourth time, adding the superseded case to the worked example, reaching
`adad9b4b86a2`. A fifth raised the replacement cap to 640 characters.
A sixth rewrote three sentences in the invariant block that stated as true
of every level what the new `open` level permits. A seventh added the
`mismatch` field and the paragraph telling a model when to fill it.
An eighth named the sixth fidelity level in the invariant block that
partitions the ladder by what joint support means, so the tree now holds
`prompts/merge.md` `c33344d1450b`. None of these later moves changes
reachability, since these keys were already unreachable, but each orphans a
later merge corpus.
The other 198 keep their keys and lose their inputs: a decompose or verify
call in this directory is keyed on messages carrying the merged document a
merge call produced, and that document will not be produced again. All 264
are still on disk and still readable; what they are not is
reachable.
`run_merge.py --offline` replays `m7/` instead.

130, not 144. The cassette key is computed over the rendered prompt, so
byte-identical document text is one cassette per sample however many fixtures
point at it. Sixteen fixtures hold 48 documents but only 43 distinct ones:

- `conflict_surfaced/source_a.md` = `contradiction/source_a.md` =
  `dropped_claim/source_a.md`
- `conflict_surfaced/source_b.md` = `contradiction/source_b.md`
- `attribution_invented/source_a.md` = `attribution_swapped/source_a.md`
- `dedup/source_b.md` = `structure_added/source_b.md`

43 × 3 = 129, and the 130th is the one schema repair's second attempt. The
first group is asserted by `tests/test_fixtures.py`, because the whole point of
the `contradiction` / `conflict_surfaced` pair is that it differs in
`merged.md` alone. The other three are incidental reuse of the shared fact
pool.

### Thinking is off, and had to be forced off

qwen3 reasons by default. On Ollama 0.32's `/v1` layer, neither `think: false`
nor `chat_template_kwargs.enable_thinking` has any effect — the only field that
actually suppresses it is `reasoning_effort: "none"`, which takes a decompose
call from ~13.5 s to ~2.0 s of generation. Ollama returns any reasoning in a
separate `reasoning` field rather than inline `<think>` tags, and does not count
those tokens in `completion_tokens`, so a run with thinking left on looks
cheaper in the usage numbers than it is.

Decompose and verify are extraction and entailment tasks with a fixed output
shape. Thinking is off for both. Whether it helps the *merge* pass is an open
question that the `m4/` run answered for `qwen3:8b` by running it both ways; that is why
`thinking` is part of the cassette key, so the two variants cannot collide.

The 27B corpus is off for every role, merge included, and it carries no
reasoning: none of its 407 recorded messages has a reasoning field.

## File format

One JSON file per call, named `<role>-<first 16 hex of key>.json`. The key is a
sha256 over role, model, tier, prompt hash, messages, schema, temperature, seed,
max_tokens, thinking and sample — so any change to the prompt, the schema, or the
fixture text is a cache miss rather than a stale hit.

```json
{
  "schema_version": 2,
  "recorded_at": "...",
  "key": "...",
  "request":  { "role", "model", "tier", "messages", "schema", "temperature" },
  "response": { "raw", "http_status" },
  "meta":     { "endpoint_id", "endpoint_id_scheme", "claimcheck_source",
                "latency_ms", "attempt", "field_order" }
}
```

`response.raw` is the response body verbatim, exactly as it came off the wire.

`meta.field_order` is the field order the recording run read the answer under,
`schema` or `any`. A replay reads each answer no more strictly than its
recording did, so the 27B corpus, stamped `any`, replays with no flag.

`meta.claimcheck_source` is the revision that recorded the file: a short commit
hash, `-dirty` if tracked files had uncommitted edits at the time, `-unknown` if
git could not be asked. It answers a question the key cannot. The key covers
everything that reaches the model, so it is the right thing to invalidate a
response on; it says nothing about the scoring, reporting and grounding code
that turned the response into a number. Two cassettes with the same key can
still have been measured by different tools.

**No secrets.** `meta.endpoint_id` is `sha256` of the endpoint's scheme, host,
port and path, truncated to twelve characters — never the address itself, never
the full URL, never a header, never an API key. The only question anything asks
of it is whether two recordings came from the same deployment, and an equality
test does not need an address. Cassettes are committed, so this is enforced in
code (`llossless/cassette.py`) and checked by `tests/test_client.py`, not left
to reviewer discipline.

**`meta.endpoint_id_scheme` says which rule made that id**, and absent means
rule 1. The 27B cassettes of the root corpus and `m7/` are rule 2; `m4/` and
`pairs/` are rule 1, `sha256` of the hostname alone: the marker was added with
rule 2 on 2026-09-17 and the ids already there cannot be
converted to it, because a cassette records the id and never the URL. So the same box recorded before and after that date carries
two different ids and counts as two entries in `Store.endpoints()`. Nothing
replays differently for it — `endpoint_id` is not a component of
`cassette.key_for` and never was — and the census is what pays.

## Re-recording

Recording is deliberately awkward, because a casual re-record silently replaces
the ground truth the measurement rests on.

```sh
# needs a running endpoint; --min-interval paces the GPU (see below)
python3 tests/run_decompose.py --samples 3 --record tests/responses --min-interval 30
```

By default `--record` will not overwrite an existing cassette; pass `--force` to
replace them. Re-record only when the prompt, the schema, or a fixture changes.

The invariant is that every cassette here was produced by the prompt file at the
hash the header records, so a reported number is attributable to a state of the
repo. That does not always mean re-recording everything: a prompt hash is part of
the cassette key, so editing `prompts/verify.md` misses the forward cassettes
that use it and leaves the ones using `prompts/verify_reverse.md` untouched. Record the
misses, then **delete the superseded files** — leaving them turns the directory
into two prompt versions wearing one header, which is the failure this rule
exists to prevent.

Since `schema_version: 2` this is enforced rather than asked for. Every cassette
records the revision that made it, and `--record` refuses to write into a
directory whose cassettes name a different one, printing the mixture it found.
A dirty tree is its own revision, so the second sweep after an uncommitted edit
is refused too: commit, then measure. Untracked files are excluded from that
judgement — a recording sweep writes untracked cassettes as it goes, and
counting them would make every sweep dirty by its own second call.

`--mixed-sources` overrides it. That is the honest flag to reach for when the
edit provably cannot reach the model or the score — a rename, a docstring — and
it makes accepting two provenances a decision someone typed rather than a
default. Cassettes written before the field existed count as `unrecorded`, which
is one more distinct provenance and not a wildcard.

**Every re-record so far was forced by a key change, not chosen.** Adding
`sample` to the key orphaned the first corpus. Rewriting all three prompts
orphaned the second: 98 files, deleted wholesale on 2026-08-07 rather than
left to rot beside their replacements. Delimiting the decompose worked
examples orphaned the 93 decompose cassettes of the third, which is why this
directory's two passes now carry two revisions. Reverting that edit orphaned
the delimited 93 in turn: 93 files, deleted on 2026-08-08 on the same proof,
that every one of them carried `=== BEGIN EXAMPLES ===` in its request body
and no run at the restored prompt hash can produce their keys. The fourth has
the same shape: three successive edits moved both verify prompts and re-keyed
the same 66 cassettes three times, so the 66 were deleted here too rather than
left beside the 78 that replaced them. The fifth was chosen rather than forced:
the 27B re-record of 2026-09-24 and 25 changed the model, which re-keys
everything, and the 528 `qwen3:8b` cassettes it replaced were deleted in the
same way.

The check that a superseded cassette is dead rather than merely old is worth
repeating each time: replay against the directory and confirm the runner reports
`replay miss: no recorded response for role 'decompose', key …` rather than
serving a stale answer. A cassette that still answers is not orphaned, whatever
the prompt hash says.

The superseded corpora are not in this copy: committed on 2026-08-07, one at 61/64
strict and one at 63/64, they replay only from the history they were recorded in. Changing the model means a
different corpus and a different reported number; say so in the commit message.
Whatever the change, commit the run that motivated it before the change, so the
number being improved on stays replayable from git rather than being overwritten
by the number that replaced it.

`--min-interval` is not rate limiting, and it is not a project-wide setting. It
defaults to 0, and it exists for the local development box, whose GPU overheats
under back-to-back inference and powers the machine off mid-run. The interval is
a thermal mitigation for that one card, and the figure is the machine owner's to
set rather than something to tune for throughput. A hosted endpoint with real
cooling takes no interval at all: omit the flag and record at full speed. Cache
hits and replays never wait either way.

The paced runs on record cost what pacing costs, and those numbers stand as
records of what was done. Three samples means three times the paced calls. The
verify sweep took 48 minutes for 66 calls at `--min-interval 30`; the decompose
sweep took 45 minutes for 93 at `--min-interval 15`, of which about 23 minutes
was the model sitting idle to cool down. Budget the interval plus roughly 14
seconds of inference per paced call and the estimate will be close — but budget
it at whatever interval you have been given, not the one that would finish
soonest. Unpaced, the second term is the whole estimate.

Unpaced never means parallel. Ollama splits `CONTEXT_LENGTH` across
`NUM_PARALLEL` slots at server startup, so concurrency shrinks the window the
prompt-budget findings were measured against. Every recording run in this
directory was serial and the next one must be too.

Check what a run would cost before making it:

```sh
python3 tests/run_decompose.py --samples 3 --dry-run
```

## What the first decompose run found

History: this section and the verify one describe `qwen3:8b` corpora the 27B
replaced. Their cassettes are deleted and their figures do not replay.

### `disjoint_sources`: the model still copies lines instead of splitting claims

All three missed count bands are this one fixture, in all three runs: 9 claims
against a band of `[16, 32]`, 12–13 against `[20, 38]`, 15 against `[36, 70]`.
Nothing marginal about it — the extraction is around half the floor, and on
`merged.md` it is well under half.

The cause is visible in the claim text. The model emits one claim per source
line, verbatim, rather than decomposing it. `prompts/decompose.md` says "One
assertion per claim. Split compound sentences." Sentences carrying three
assertions come back as one claim.

The other eleven fixtures hide this completely, and it is worth being precise
about why: they are configuration documentation, already written one fact per
line, so "copy each line" and "extract each claim" produce the same output. They
cannot tell a decomposer from a line splitter. `disjoint_sources` is narrative
prose — two short stories with no overlapping content — and it is the only
document set in the corpus where those two behaviours differ.

**The bands were not loosened.** Widening `[16, 32]` to admit 9 would make the
fixture agree with the model, which is fitting the ruler to the object being
measured. The band is what a careful human decomposition of that text yields; the
model is under it; the fixture reports that.

The counts move whenever the prompt moves and never far enough to matter: 8 / 11
/ 11 two prompt versions ago, 9 / 12 / 17–18 one version ago, 9 / 12–13 / 15 now.
`merged.md` has been as high as 18 and as low as 11 and its floor is 36. All
three documents miss in every sample of every corpus. Three rewrites that change
the numbers without changing the outcome are evidence that the shortfall is a
property of the model rather than of a particular wording.

### Three `must_extract` probes were not extracted

104 of 107. The misses:

| fixture | document | probe |
|---|---|---|
| `conflict_surfaced` | `merged.md` | `merged-attributed-timeout-a` |
| `conflict_surfaced` | `merged.md` | `merged-attributed-timeout-b` |
| `disjoint_sources` | `source_a.md` | `a-ownership` |

The `conflict_surfaced` pair is the interesting one. That merge surfaces a
disagreement — it records both timeout values and attributes each to its source
— and the fixture expects decompose to yield *two* attributed claims from it.
The model yields one. The same two probes pass verify cleanly in the reverse
direction, so this is a granularity failure in that run, not a comprehension failure:
the content is there, it is not split.

### Three unanchored spans, and the nine that a prompt edit added and gave back

668 of 677 spans were found verbatim in their document — **98.7%**. The rate is
the comparable figure rather than the fraction, because the corpora being
compared below extracted different numbers of claims and so have different
denominators.

The nine misses are three distinct spans, each returned in all three runs:

| document | line | document says | span says | runs |
|---|---|---|---|---|
| `conflict_surfaced/merged.md` | 8 | `120` | `12,0` | 3/3 |
| `ordering_only/merged.md` | 7 | `512` | `513` | 3/3 |
| `disjoint_sources/merged.md` | 13 | `it turned back to life and color` | `The rosegarden turned back to life and color.` | 3/3 |

Three samples buy something a single run cannot: each of these is 3-of-3, so
none is a sampling accident.

The first two are the numeric defect: a three-digit number whose third digit is
corrupted or comma-separated, in a field specified to be a character-for-character
copy. Across four corpora and ten runs that line has come back as `513` five
times, `510` three times and `51,2` twice — **never once as `512`** — and
`conflict_surfaced/merged.md:8` has returned `12,0` in every sample of every
corpus. Whether the cause is tokenisation or the neighbouring lines is not
settled by these recordings.

That line is the strongest argument in the corpus for checking spans rather than
trusting them. The verdict attached to it is correct, the claim text is correct;
only the quoted receipt is wrong, and nothing at the verdict level would ever
show it. It is now asserted against by pattern in
`tests/fixtures/ordering_only/expected.json`, so it fails the document instead of
being rediscovered each time.

The third is paraphrase rather than misquotation — the model wrote a fluent
sentence with the right content and offered it as a quotation, resolving the
pronoun `it` to `The rosegarden` on the way. This is the same document that
returns half the claims its band asks for, and the two failures are plausibly one
behaviour: a model summarising narrative prose it will not decompose.

**A prompt edit moved this number and undoing it moved it back.** Between these
two states sat a corpus recorded against `498e6bab6f07`, which wrapped the
decompose prompt's worked examples in delimiters. Nothing in that edit concerned
span copying. It cost nine spans anyway, all on `disjoint_sources/merged.md`:

| | before, 3× | delimited, 3× | after revert, 3× |
|---|---|---|---|
| spans anchored | 667/676 = 98.7% | 652/670 = **97.3%** | 668/677 = 98.7% |
| `disjoint_sources/merged.md` claims | 17, 18, 17 | 15, 15, 15 | 18, 17, 18 |
| …its unanchored spans | 3/52 = 5.8% | 12/45 = **26.7%** | 3/53 = **5.7%** |

Two separate effects, worth reading separately: the document gave back **fewer
claims** and a **larger share of them** was unanchored. Quoting "3 misses, then
12" alone would credit the whole change to the second effect while the
denominator was moving underneath it.

The three added spans were all the same behaviour, on lines 37, 42 and 43 —
each a clause rewritten into a standalone sentence with its pronoun or determiner
resolved, which is exactly what the prompt's "Do not correct anything" forbids.
All three are absent again after the revert.

All three columns are three samples, so this is a like-for-like comparison
rather than a rate read against a single run. On those three lines the count is
9 unanchored spans under the delimited prompt — 3 lines × 3 runs, every run — and
**0 in both corpora recorded at `b4ec1e0c7ead`**, the one before the edit and the
one after the revert. An effect that appears at 3-of-3, disappears when the edit
is undone, and takes the claim count with it in both directions is reproduced,
not sampled.

This is what the delimiters cost on `qwen3:8b`; what they fixed on `qwen3:4b`
is not recorded in this corpus.

### Two things only span anchoring caught

Span anchoring is the cheapest check in the pipeline — a substring test against a
file already in memory — and it is twice now the only check that noticed a real
defect. Both are worth stating together, because they are different faults:

1. **"He took him days".** The previous corpus returned a 129-character span in
   which one word was changed, in all three of three runs. The claim was right,
   the verdict on it was right, the line number was right; a single pronoun in the
   quoted evidence was wrong. Nothing that grades verdicts could see it.
2. **`qwen3:4b` returning the prompt's worked example as its extraction.** On four
   documents, three samples of three, the model emitted claims about a kiln firing
   for eleven hours and a garden with eleven rose beds — the two examples in
   `prompts/decompose.md` — as valid, schema-conforming, confidently-numbered
   JSON. Every structural check passed: the schema was satisfied, the line numbers
   were integers, the claim count was in band on some documents. Span anchoring
   failed them because a kiln appears in no fixture.

The second is the more alarming, because it is what a model failure looks like
when it is *not* a degradation. A 4b model scoring slightly worse than an 8b one
is a judgement call about whether the difference matters. A 4b model answering a
question about the wrong document entirely is not, and the only reason it is in
this README rather than in the quality table is that one cheap check was looking
at the text instead of at the shape of the text. `tests/fixtures/GLOBAL.json` now
asserts the absence of that example text on every document of every fixture, so a
recurrence fails loudly instead of being caught by inspection.

## What the first verify run found

History, as above: `qwen3:8b`, not the corpus in this directory now.

**107/108 strict, 108/108 lenient, and 108/108 stable.** The previous corpus
scored 61/64, then 63/64 after one prompt revision, then 79/80 once
`disjoint_sources` was added. Four fixtures and 28 probes later it is 107/108
against a probe set that is more adversarial than any of those numbers were
measured on.

Two long-standing failures closed, and the honest reading of each differs:

- **`conflict_surfaced` stays fixed.** Both attributed-timeout probes return
  `SUPPORTED` with the attributed sentence as evidence, grounded, three of three.
  This was fixed deliberately, by adding the conflict rule to the prompt as a
  worked example rather than as prose.
- **`numeric_drift/a-max-connections` now returns `CONTRADICTED`**, the fixture's
  declared expectation, three of three — where the previous corpus returned a
  stable `MISSING` that was carried for weeks as an open, undiagnosed bug. This
  was **not** fixed deliberately and the cause is confounded: the verify prompts
  and the response schema both changed between the two runs, so the change
  cannot be attributed to either. The correct reading is that the
  old stable `MISSING` is no longer reproducible under the current
  configuration, not that anything was repaired.

### Evidence grounding is now clean

106 evidenced spans, 106 grounded, **zero transcription errors and zero
attribution errors**. The previous corpus scored 74/76 on a weaker version of
this check — one that searched the whole reference blob instead of the file the
model named.

This is the one place where verify and decompose diverge sharply, and reporting
them together would flatter both. The same model, quoting the same documents in
the same run, copies spans perfectly in verify and gets nine of them wrong in
decompose. Whatever the verbatim-copy instruction is doing in
`prompts/verify.md`, it is not doing it in `prompts/decompose.md`.

### The one strict miss: `attribution_invented/m-tls-attributed`

The fixture expects `MISSING`. The model returned `CONTRADICTED` three times out
of three, with this rationale each time:

> The claim attributes the TLS version to the Operator Guide, but it is stated in
> the Deployment Notes.

That is a precise and correct description of the planted defect. `merged.md`
credits `source_b.md`'s TLS fact to the Operator Guide, which is `source_a.md`
and never mentions TLS. The model located the real source, quoted it verbatim
from the right file, and named the defect in one sentence.

**So this is a labelling disagreement, not a detection failure.** Both labels
produce a finding: per the `FINDINGS` table in `src/llossless/verify.py`,
`CONTRADICTED` under `merged_to_sources` derives `contradicted` and `MISSING`
derives `hallucinated`. Either way the defect is reported and the exit code is 1.
Only the report section differs.

Both readings are defensible, which is what makes it a fixture question:

- `MISSING` — no source states the attributed conjunction. `source_a.md` is
  silent on TLS, and silence is not denial.
- `CONTRADICTED` — a reader of the sources can determine the claim is *false*,
  not merely unsupported. `source_a.md` demonstrably does not say this.

**The fixture has since been changed, on 2026-08-08, and the order of events is
the point.** It was left alone through the run that produced the numbers above,
which is why they still read 107/108 strict. It was widened afterwards, once a
second model had been asked: `qwen3:8b` and `qwen3:4b` both return
`CONTRADICTED` three of three, independently, with the same reading. Two models
agreeing is not proof the fixture was wrong, but it is the difference between
"the model failed" and "the label was underspecified", and the second is what the
evidence supports.

`also_acceptable` is now `["CONTRADICTED"]`. `expected_verdict` stays `MISSING`
and `expected_finding` stays `hallucinated`, because the declared reading has not
changed — only the admission that a second one exists. Strict scoring still
counts this as a miss, and that is deliberate: strict is the mode that refuses to
be talked round, and a fixture that scores 12/12 in both modes would have lost
the record of the disagreement entirely.

The schema question that blocked this is settled rather than sidestepped. An
empty `expected_evidence_contains` used to be ambiguous between "must be empty"
and "not checked"; it now means **not checked**, and a probe that leaves it empty
must say why in a `notes_evidence` field or fail validation. This probe says why:
the two accepted labels owe *different* evidence — `MISSING` owes none,
`CONTRADICTED` owes a span from `source_b.md` — and asserting evidence
conditional on the observed verdict is a harness mechanism that does not exist yet.
So it asserts nothing, deliberately and in writing, rather than asserting
something false in either direction.

### Evidence as declared: 45/45, source named: 14/14

Both figures lost their denominator rather than gaining a pass. Before the
revision they read 45/46 and 14/15, and both misses were the same probe:
`m-tls-attributed` declared empty evidence expectations because it expected
`MISSING`, and a `CONTRADICTED` verdict arrived carrying a span and a filename.
One disagreement, counted three times because it tripped three different
assertions. Under the settled semantics that probe now declares nothing and is
not counted at all, so the ratios are clean because the check was withdrawn, not
because it started passing. There is no second defect hiding in those
denominators, and there is no new pass in them either.

### `CONTRADICTED` was unauditable until the schema said `evidence_source`

Grounding originally searched for the quoted span in the whole reference blob —
`merged.md` forward, both sources concatenated in reverse. For `SUPPORTED` that
is nearly enough. For `CONTRADICTED` it is not, and the reverse direction is
where it breaks: a claim contradicted by `source_a.md` and a claim contradicted
by `source_b.md` are different findings, and a search over the concatenation
cannot tell them apart. The tool would report a real disagreement without being
able to say which document was on the other side of it — and a merge conflict
that names no document is not something a person can act on.

Worse, it could not distinguish a model that quoted the right sentence from the
wrong file from one that quoted the right sentence from the right file. Both
were `grounded`.

The schema now requires `evidence_source` on every verdict that asserts the
reference text says something, the validator requires it to name one of the
files actually passed into that prompt, and grounding is looked up **in that
file**. The outcome is three-way rather than a boolean:

| outcome | means |
|---|---|
| `grounded` | the span is in the file the model named |
| `transcription_error` | the span is in none of the target files — the quote was invented or mistyped |
| `attribution_error` | the span is real, but it is in a different file than the one named |

They are counted separately in the report, because they are different faults
with different fixes. A transcription error is the model paraphrasing while
claiming to quote; an attribution error is the model reading correctly and
filing it wrong. Folding the second into "ungrounded" would have hidden it
behind the first.

`MISSING` is graded `not_graded` and owes no evidence at all — it asserts the
absence of text, and there is no span to check. That coupling runs both ways in
the validator: `MISSING` with a quote attached is as much a failure as
`CONTRADICTED` without one. Neither is coerced into shape; the response is
rejected and repair attempt 2 gets a description of the fault. Three responses in
this corpus needed that second attempt; all three succeeded, and no call errored.

### Field order is part of the contract

The verify schema lists its properties as `claim_id, verdict, evidence,
evidence_source, rationale`, the prompts state that order in words, and the
validator rejects a result whose keys arrive in any other order.

That is not tidiness. Under constrained decoding the model fills fields in
schema order, so putting `verdict` before `rationale` makes it commit to a label
and then explain it, rather than talk itself somewhere and label the destination.
`evidence` before `evidence_source` puts the span first and the filename after,
which is the order in which the model can actually check the second against the
first. The order is checked rather than assumed because the tiers below
`json_schema` do not enforce it, and a prompted-JSON model that reorders the
fields is telling you it is not following the schema at all.

The rationale-versus-verdict consistency check built for the previous corpus is
still in place, as a **diagnostic rather than a validation error**. It reads the
rationale for a verdict label other than the one emitted and reports every hit in
a section of its own. It found none in this run. It does not trigger a repair
attempt, and the distinction is not a small one: a repair error is fed back to
the model verbatim, so failing the response here would put "your rationale says
CONTRADICTED but your verdict says MISSING" into the second-attempt prompt. That
is a leading question, and the second answer would no longer be evidence of
anything.

## What the `m4/` merge run found

264 cassettes in `tests/responses/m4/`, 72 units of work,
twelve fixtures × two thinking conditions × three samples, one process,
`--structured json_schema`, seed 0, temperature 0. The generated documents are
beside them in `tests/responses/m4/merges/` as 72 `.md` files, because recovering
a document from a cassette means finding one key among 264 and
un-escaping one JSON field, and that is not a review path. What follows is what
the recorded bodies show.

**One thing about this corpus is recorded nowhere in it.** `timeout` is not part
of `cassette.key_for`, appears in no cassette `meta` and is not a journal field,
so the two timeout settings the sweep spans are invisible to every file here: 19
of the 72 units were replayed from `.claimcheck-cache/` byte for byte, their
bodies generated under `--timeout 120`, and the other 53 ran live under
`--timeout 300`. It changes no token count, tier, verdict or coverage figure — a
timeout yields a whole answer or no record at all, never a shortened one — and
the 19 are journalled `cached: true`, which the timing summary already drops.
The journal has carried `timeout` on every record since; this corpus
predates that.

### The document that scores full marks is the two sources pasted together

`contradiction`, thinking off, sample 0: 8/8 forward probes
`SUPPORTED`, every span correctly grounded, and the merged document is —
after collapsing whitespace and dropping `#` markers, both of which `README.md`
says LLossless does not score — **character for character**
`source_a.md + "\n" + source_b.md`. `difflib` ratio 1.0000. Against the literal
concatenation the diff is nine lines: two titles lost their `#`, five blank lines
went.

It states the 30-second connect timeout and the 60-second one in two separate
`## Networking` sections, attributes neither, and repeats the port, the read
timeout and the boilerplate line twice each. Forward coverage cannot see any of
that: it asks whether every source fact survived, and in a concatenation every
source fact survives by construction. 14 of 66 eligible
merges in this corpus are concatenations.

### The one that merged properly lost two facts doing it

`dropped_claim`, thinking on: a real merge — one title spanning both documents,
the shared boilerplate stated once instead of twice, the connection limit stated
once instead of twice — and the connect timeout and read timeout are simply
gone, taking `30` and `120` with them. Every other number survived: `1.2`, `100`,
`3`, `512`, `8443`. It scored 8/10 against the concatenation's
10/10.

The merging is narrower than it looks. Both conditions keep all six headings from
the two documents, and both still state the port line twice. Of the three lines
both sources give word for word, thinking on states two once and the port line
twice; that and the two lost facts are the whole of the difference.

**Those two facts are not the fixture's plant.** `dropped_claim` plants the JSON
Lines log format at `source_b.md:13`, and the generated merge restores it in all
six units. What went missing is `source_a.md` lines 8 and 9 — adjacent, both
*"The default X timeout is N seconds."*, and the only facts in A's `##
Networking` section that B does not also state. The model repaired the planted
omission and made an unplanted one.

Both readings are correct. The concatenation dropped nothing and the merge
dropped two facts, and a recall metric is right to score them that way. Recorded
here because the pair is the clearest thing in the corpus: on this suite, not
merging is the dominant strategy.

### A third thing: 0 of 66 against 5 of 76

**Every response this project has ever recorded that failed to parse or failed
its schema was produced without a schema.** Across all 945
cassettes on disk (the decompose, verify and `m4/` corpora, the smoke and probe corpora) the split is
absolute:

| tier | constrained? | cassettes | rejected by parse or schema validation |
|---|---|---|---|
| `json_schema` | yes | 835 | **0** |
| `tool_call` | yes | 34 | **0** |
| `prompt` | no | 76 | **5** |

Every response body was re-read from disk, `strip_reasoning`-ed, passed through
`parsing.extract_json` and validated against the schema its own request declared.
The `tool_call` row is `claude-sonnet-4-5` from the early cross-model sweep, the one
model in this repository that took the middle rung.

The project-wide figure shows the pattern is not a cherry-pick. The controlled
one is inside a single run: **66 against 76**, same model, same endpoint, same
prompts, same temperature, same seed, one process, one afternoon.

**Nobody designed that comparison, and that is what makes it worth quoting.** It
is not an A/B built to make a point; it is the wreckage of a production run. On
2026-08-08 a defect in `client.py` demoted the request shape from `json_schema`
to `prompt` partway through an `m4/` sweep and never raised it again. Everything
else was held fixed by accident rather than
by design. A demonstration would have been cheaper to build and easier to
disbelieve.

Three units errored outright on those five bodies — `dedup [on]` sample 1,
`hallucination [off]` sample 1, `hallucination [on]` sample 1, all at the
`verify_reverse` step. Their responses were kept in a gitignored exploratory
corpus under `tests/eval/`, which is not in this copy.

The two cases above are failures of *content* that every structural check passed.
This is the converse, and it belongs beside them because it settles what the
structured-output tier is for.

**The five failures are one failure, at one field.** In every case the model
damaged the key `claim_id`, and only that key, in the middle of an otherwise
clean document:

```
    {
      "claim
    },
    {
      "claim_id": "M-003",
```

It opens a verdict object, writes a partial key, abandons it with a raw newline
*inside the string literal*, closes the object and carries on correctly to the
end. Four of the five fail this way — the three preserved dumps break on
`"claim` once and on `"ver` twice. The fifth does not break the syntax at all:
it emits a fourth verdict whose key is `"claim,"`, a well-formed JSON object
that fails validation on a missing required property.

None of this is truncation. Every body carries `finish_reason: "stop"`, ends
`}\n  ]\n}`, and balances its braces — 6 against 6 in the first dump, 9 against 9
in the other two.

**A grammar-constrained decoder cannot produce any of it.** JSON has no
production for an unescaped newline inside a string, and a schema with
`required: ["claim_id", ...]` and `additionalProperties: false` has no state in
which `"claim,"` is an acceptable key. Masked to that grammar the tokens are
unreachable. Asked for the same thing in prose, the model produced output that
survives a human skim and is not JSON. That is the case for the schema tier
stated as a measurement rather than a preference: it does not make this class of
error rarer, it makes it impossible.

**The parser's diagnosis is wrong, and this is worth fixing.** `json.loads` says
`Invalid control character at: line 18 column 13`, which is right.
`parsing.extract_json` says **"JSON is unterminated; the response was probably cut
off"** (`parsing.py:124`), which is not. The scanner tracks whether it is inside a
string by counting quotes, and the unescaped newline leaves the quote count odd —
83 in the first dump, 147 in the other two — so its in-string parity is inverted
for the rest of the document. Every structural brace after that point is read as
string content and never counted, the depth counter never returns to zero, and
the scanner falls through to its truncation message. The response was complete;
the message sends a reader to look at `max_tokens`. Recorded here rather than
patched mid-run: that branch should distinguish "ran out of
input" from "lost track of the string", and the repair hint it sends back to the
model should say which.
