# Fixture format

This page is for contributors writing or changing a fixture: what the files
are, what each field in `expected.json` means, and how the validator holds
them to it.

Every fixture is a directory under `tests/fixtures/` containing four files:

```
source_a.md    one of the two input documents
source_b.md    the other input document
merged.md      a hand-written merge, with a defect planted in it (or not)
expected.json  ground truth: what LLossless must say about this fixture
```

The fixtures are hand-written and are the ground truth the tool is measured
against. They are written before the tool exists, and are never edited to make
a result look better. If a fixture and the tool disagree, either the tool is
wrong or the fixture was wrong from the start - "the fixture is inconvenient"
is not a third option.

**One fixture breaks both halves of that, on purpose and once.** `restated`'s
`merged.md` is not hand-written: it is real model output, copied byte for byte
from a merge run, and it carries a fifth file, `recorded-claims.json`, holding
the claims that run extracted. Neither is ground truth and neither is graded as
ground truth - `expected.json` is still the answer key - but a detector that
fires on claims needs a probe made of claims a model really produced, and no
hand-written document in this corpus produces them. The section
"`restated` is real model output, and the corpus's only one" is the whole
argument. Every other fixture is four files and hand-written, and a new fixture
should be too.

## Fixture text

All fixture prose describes **Vandrell Relay**, an HTTP relay that does not
exist. The name was checked against public sources and matches no software
product, company, or project. Nothing in any fixture derives from a real
product, employer, customer, or internal system.

Every fixture but four draws on the same fact pool - listen port, connect
timeout, read timeout, maximum concurrent connections, retry policy, TLS
minimum version, access log format, health check path - so they read as
variants of one document rather than as unrelated toys. The four exceptions
are `disjoint_sources`, `disjoint_domains`, `concatenated` and `restated`, and
each has a section below saying why it had to leave the pool.

### `disjoint_sources` is outside the fact pool, deliberately

It is narrative prose: two short fairy tales, one about a princess with a rose
garden and one about an old woman in a forest, sharing no content at all.
Nothing in it is about Vandrell Relay and nothing in it uses the pool.

The exception is not an oversight, and the reason is a measurement failure the
other seven could not have surfaced. Configuration documentation is already
written one fact per line, so "copy each line" and "extract each claim" produce
the same output on it. A fixture set made only of such documents **cannot tell a
decomposer from a line splitter**, and the first decompose run over the original seven scored
a clean sweep while the model was doing the latter. Narrative prose is the first
place the two behaviours diverge, because its sentences are compound.

Two further properties come with the genre and are used:

- **Disjointness is an assertion.** The two sources share no facts, so any claim
  linking them is invented rather than merged. That is what `must_not_extract`
  checks, and it is the only fixture where the assertion is meaningful.
- **Long sentences make evidence grounding bite.** A model quoting a
  twelve-word configuration line either gets it right or obviously does not. A
  model quoting a twenty-five-word narrative sentence can alter one word inside
  it and still look correct, which is exactly what the corpus caught.

A new fixture does **not** need to leave the fact pool. This one does because
genre, not subject matter, is what it varies.

### `concatenated` is outside the fact pool for a mechanical reason

It is narrative prose too - two short accounts of the same village bell tower,
one a parish record and one a recollection - and it is outside the pool because
a pool document cannot express what this fixture is for.

The fixture needs one fact stated by both sources **in two different wordings**.
A pool document states a fact as `The read timeout is 30 seconds.`, and the
other document's version of that same fact is the same sentence: restating a
configuration line gives you the configuration line back. Two sources that
agree in the pool therefore agree character for character, a merge that keeps
both copies repeats a string, and `reconcile`'s check 9 already fires on that.
The case the fixture exists for is the one where the two copies are two
wordings, so check 9 is silent and nothing else is looking - and prose is the
only genre in which two wordings of one fact exist at all.

Genre, not subject matter, again. Nothing else about the fixture varies: it
plants no verify-level defect, drops nothing, contradicts nothing and invents
nothing.

### `restated` is real model output, and the corpus's only one

Every other fixture in this directory is written by hand, including
`concatenated`, which was built to be the must-fire probe for a duplicate-claim
check. Measured live, three samples, it does not fire one: its ten claims come
back byte-identical every time and no two of them collide, because its two
wordings of a fact are too far apart for a decomposer to resolve to one
sentence. A probe that has never fired proves nothing about the detector it is
supposed to prove, so the probe had to be a document a model really produced.

`restated` is that document. Its `merged.md` is byte for byte what
`merge --fidelity low` returned for the two sources beside it, on a
27B model, on 2026-09-15; `source_a.md` and `source_b.md` are the operator's own
pair, also unedited. The run it came from **exited 0 with no finding of any
kind** - that is the defect, not a side note. `recorded-claims.json` is that
run's own decompose output for all three documents, copied out of its JSON
report with nothing added and nothing left out, and
`reconcile.restatements` finds 23 claim texts in the merge extracted from two
different lines each, and none at all in either source.

Why it is outside the fact pool: it was not written for the pool, or for this
corpus, or by this project. It is a general-knowledge pair about Christianity,
written by the project's author to try the tool on real-looking documents, and
released for use here. Rewriting it into the pool would destroy the one
property that makes it worth having - that a model, not an author, produced the
merge.

Why it is registered `guard`, like `concatenated` and for the same reason: every
probe really is `SUPPORTED` in both directions, so its own probes imply exit 0,
and `kind` must agree with them. The section "`concatenated` is a guard that
records a blind spot" sets out that argument in full and all four of its bullets
apply here unchanged. The one difference is which half of check 9 fires: nothing
in `concatenated` fires either half, and `restated`'s claim-level half fires 23
times - but only on a `merge` run, which is not the command
`tests/run_detect.py` grades this corpus with.

What this fixture must **not** become: a licence to add model output to
`tests/fixtures/`. It is here because a claim-level detector needs claim-level
evidence and this corpus had none. Everything else stays hand-written, which is
what keeps an answer key independent of the instrument.

## Which pass checks which assertion

A fixture carries assertions for different passes of the pipeline. Running a
fixture through the verify harness alone and seeing its `expected_conflicts`
unmet is not a verify failure: conflict detection belongs to the report layer.

| assertion | checked by |
|---|---|
| `must_extract`, `claim_count_band` | decompose |
| `expected_verdict`, `also_acceptable`, `expected_evidence_contains` | verify |
| `expected_finding` | verify for the label, the report for where it is filed |
| `expected_conflicts`, `expected_exit_code` | **the report and the exit code** |
| `must_not_extract` scoped to `merged.md` | decompose for the hand-written merge, **the merge harness** for a generated one, under the transfer rule below |

**The merge harness adds no assertion of its own, and ignores three.** The merge
pass generates `merged.md` rather than reading the committed one, so
`expected_verdict`, `also_acceptable` and `expected_evidence_contains` - all
three of which describe the hand-written document - are not applied to a
generated merge. Every forward probe is graded against one rule, `SUPPORTED`,
plus the computed grounding check. This is why `dropped_claim` fails under the
verify harness and passes under the merge harness on the same probe: the first
scores a merge with a planted omission, the second scores one that has to carry
the fact. The two are not in conflict because they are not looking at the same
document.

**Value-level conflict detection belongs to the report layer.** There are two
ways to find a conflict: verdict diffing (paired claims from different sources
producing differing verdicts) and value comparison (two sources asserting
incompatible values for the same attribute). The second needs claim pairing plus
value comparison, a substantially harder mechanism than diffing verdicts, so it
sits with the report and the exit code.

This matters for `numeric_drift`. Under lenient scoring both of its probes may
legitimately come back `SUPPORTED`, and the conflict is then reachable *only*
through the value-comparison path. Without this note `numeric_drift` reads as
a fixture the verify harness cannot pass.

## Vocabulary

### `document` vs `target`

`document` is where a claim *comes from*. `target` is what the claim is
*verified against*. Both follow from `direction`:

| `direction` | `document` must be | `target` is |
|---|---|---|
| `source_to_merged` | `source_a.md` or `source_b.md` | `merged.md` |
| `merged_to_sources` | `merged.md` | `source_a.md` + `source_b.md`, concatenated |

`anchor.all_of` anchors against **`document`**. `expected_evidence_contains` is
checked against **`target`**. These are different files, and the distinction is
easy to get backwards: a probe with `document: "source_b.md"` carries evidence
that must be found in `merged.md`, because that is where the verify pass reads
its evidence span from.

`match.all_of` is checked against neither. It is checked against the probe's own
`text` offline, and against an LLM-extracted claim at measurement time.

### `expected_evidence_contains` on a `CONTRADICTED` probe

A list of substrings, all of which must appear in the evidence span the model
returns. It is optional, and on `SUPPORTED` probes it is a spot check: cheap
insurance against a label handed out without reading anything, not worth
carrying on every probe.

On a `CONTRADICTED` probe it does a different and harder job, and the fixtures
that have one carry it deliberately:

| fixture | probe | spans |
|---|---|---|
| `contradiction` | `a-connect-timeout` | `["60"]` |
| `numeric_drift` | `a-max-connections` | `["512"]` |
| `attribution_swapped` | `m-notes-timeout-attribution` | `["60"]` |

Each takes a claim from one document and verifies it against another that
asserts a different value for the same attribute - 30 against 60 seconds,
approximately 500 against 512. A model can return `CONTRADICTED` and quote the
claim's *own* value back, which reads like evidence and proves nothing: it shows
the model found the sentence it was already given, not that it found the value
that contradicts it. Only a span carrying the other document's number shows the
conflict was actually located.

So each span is the **shortest substring that the claim itself does not
satisfy**, and the validator enforces the discrimination rather than trusting
the fixture author to have got it right: a span on a `CONTRADICTED` probe that
also occurs in the probe's own `text` is a fixture error, not a strict
assertion. That is why the spans are bare numbers. Adding the unit would make
the assertion no stronger and would make it fail on a model that quoted
correctly and wrote `60s`.

The claim, specifically, and not the whole document the claim came from. Those
are the same test on `contradiction` and `numeric_drift`, and they come apart on
`attribution_swapped`, where `merged.md` surfaces both sides of the
disagreement - "According to the Deployment Notes, the read timeout is 30
seconds" on one line and "According to the Operator Guide, the read timeout is
60 seconds" on the next. Surfacing a conflict instead of silently resolving it
is the behaviour this project rewards, so a document-wide exclusion would rule
out every span such a fixture could name and make the rule unsatisfiable
precisely where the merge was right. What the rule is actually for is catching a
model that echoes the claim, and the claim is what it now checks.

An **empty list** is not an expectation. It asserts nothing, exactly as
omitting the field does, and a probe that writes one must carry a
`notes_evidence` saying why the silence is deliberate - otherwise it is
indistinguishable from a probe somebody stopped writing halfway through.
Until `schema_version: 4` it meant the opposite, that the evidence had to come
back empty. That reading was redundant, because `parsing.py` already rejects a
`MISSING` verdict that quotes a span or names a file, and it was actively wrong
on `attribution_invented/m-tls-attributed`, whose two acceptable labels owe
different evidence and therefore have no single expectation to state.

Where a probe expects a span and the model answers `MISSING` anyway, the span is
**not graded**. The label is already wrong under strict scoring, and counting it
again as an evidence failure would report one mistake twice. This is what lets
`numeric_drift/a-max-connections` accept `MISSING` as one of three defensible
readings while still declaring the span that the other two owe.

### Notation is not information

The line every fixture in this set is drawn on. A merge may change how a fact is
written; it may not change what the fact says. Changing the notation is
`SUPPORTED` and must be silent. Changing the information is a defect and must be
reported.

Three fixtures are the worked examples, and they are worth reading together
because the difference is not always obvious from the size of the edit:

- **`paraphrase`** - the same facts in three different wordings across
  `source_a.md`, `source_b.md` and `merged.md`. Rewording, reordering a
  sentence, expanding or abbreviating a unit: all notation. Every probe is
  `SUPPORTED` in both directions, and a run that flags any of them has confused
  the two.
- **`numeric_drift`** - `source_a.md` says "approximately 500 concurrent
  connections", `merged.md` says 512. This looks like a rounding convention and
  is not one: "approximately 500" and "512" are different states of knowledge
  about the same attribute, and a reader who needs the exact figure is now
  reading a number the source never committed to. Information. The fixture
  declares a conflict, and no label the model returns makes that conflict go
  away.
- **`disjoint_sources`** - its time-format probe is the case in the other
  direction, and the one most likely to be got wrong. `07:15 till 19:45` and
  "quarter past seven in the morning until quarter to eight in the evening" are
  the same information in different notation, so a merge that rewrites one as
  the other has changed nothing and the probe is `SUPPORTED`. Extend either end
  by fifteen minutes and it is a defect. The reason `prompts/decompose.md`
  insists on copying time formats exactly is not that the format is a fact - it
  is that a model allowed to normalise the format will eventually normalise the
  value, and there is no way to tell from the output which it did.

The practical consequence, and the reason this is in the spec rather than left
to judgement: **a notation difference is not a finding of any severity.** It is
not a warning, not an informational note, not a low-confidence flag. It is
silence. A report that lists "merged.md writes 30s where source_a.md writes 30
seconds" has taught its reader to skim the findings list, and the next thing
skimmed is a real one.

### `expected_evidence_source`, and what a list of files means

The files the returned `evidence_source` may name. Always a list, and read as
**any one of these is a correct answer** - naming any listed file passes,
naming anything else fails.

A list rather than a single filename because a fact stated in both sources has
no single correct citation. `dedup` is built on exactly that: its listen port
and health-check path appear in `source_a.md` and `source_b.md` alike, so
`["source_a.md", "source_b.md"]` says the fact is genuinely shared and either
answer is right, while its read timeout carries `["source_a.md"]` and is graded
down to the one file that states it. Forcing a single value would have made the
fixture invent a preference its own documents do not express, and would then
have scored a coin toss.

An **empty list** means the same thing one field along: no expectation, and
`notes_evidence` required to say the silence was chosen. See
`expected_evidence_contains` above for why it stopped meaning "name no file".

It is declared where a claim's origin is actually determinate:

| fixture | probes | what it asserts |
|---|---|---|
| `disjoint_sources` | four reverse probes | two unrelated stories share no facts, so every merged claim traces to exactly one source |
| `attribution_invented` | `m-tls-plain`, `m-read-timeout` | the fact is present in one named source, which is what makes the sibling attribution probe's `MISSING` about the attribution alone |
| `attribution_swapped` | `m-notes-timeout-attribution` | the model must have read the Deployment Notes, the file whose value the merge misattributes |
| `dedup`, `structure_added` | all reverse probes | shared facts list both files, single-source facts list one |

Most other fixtures draw both sources from one shared fact pool without
asserting which is which, and stay silent rather than grade a coin toss.

This is graded **apart from grounding**, because they answer different
questions. Grounding asks whether the span is in the file the model named;
`expected_evidence_source` asks whether that was an acceptable file. A verdict
can be `grounded` and still name the wrong source - it only takes quoting a
phrase that occurs in both - and the report counts the two separately for that
reason.

Where a probe declares spans as well, the validator checks the mapping offline:
every span must be in at least one named file, and in no target outside the
list. On a one-element list that is exactly "in that file and nowhere else"; on
a list naming every target it is vacuous, which is right, because such a fixture
is asserting the fact really is shared. A fixture claiming a fact comes from one
file, when the phrase proving it appears in both, is wrong about its own
documents and is rejected. Probes with no declared spans assert the mapping by
hand and it is graded at measurement time only.

As with spans, a probe that expects a source and gets `MISSING` back is not
graded on it. `MISSING` owes no filename.

### The verdict contract, and what `target` means once a file is named

A verify result is five fields, and both the schema and the prompts fix their
order:

```
claim_id, verdict, evidence, evidence_source, rationale
```

The order is a contract, not a formatting preference, and the validator rejects
a result that arrives in any other order. Under constrained decoding a model
fills fields in schema order: `verdict` before `rationale` makes it commit to a
label and then explain it, rather than reason its way somewhere and label
wherever it arrived. Checking the order is how a weaker structured-output tier -
prompted JSON, no grammar - gets caught not following the schema.

`evidence` and `evidence_source` are required exactly when the verdict asserts
that the reference text says something, which is `SUPPORTED` and `CONTRADICTED`.
`MISSING` asserts an absence, has nothing to quote, and must carry `""` for
both. The coupling is checked in both directions and never coerced: a `MISSING`
carrying a quote and a `CONTRADICTED` carrying none are both rejected, and the
fault description goes to the model as a repair attempt.

`evidence_source` must name one of the files passed into that prompt -
`merged.md` forward, `source_a.md` or `source_b.md` in reverse. This is what
makes `target` in the table above a *set* of files rather than one blob. The
reverse direction concatenates the sources for the model to read, but the
grounding check does not search the concatenation; it searches the file the
model named. A contradiction that cannot say which document disagrees is not
actionable, and before `evidence_source` existed the tool could not say.

Grounding therefore has three outcomes, not two, and the report counts them
apart:

| outcome | means |
|---|---|
| `grounded` | the span is present in the file `evidence_source` names |
| `transcription_error` | the span is in none of the target files: invented, or paraphrased while claiming to quote |
| `attribution_error` | the span is real, but it lives in a different target file than the one named |
| `not_graded` | the verdict is `MISSING`, so there is no span to look for |

`expected_evidence_contains` is checked against `target` in the fixture
validator, which stays a whole-`target` substring test - it is an assertion
about what the fixture text contains, made offline with no model in the loop.
The named-file check is a property of a *returned* verdict and belongs to the
verify pass.

### `line`

1-based, counting every line of `document` including blank lines. Line 1 is the
first line of the file.

### The anchoring window

A probe's `anchor.all_of` substrings must all be found in lines
`[line-2, line+2]` of `document`. Those five lines are clamped to the
document's bounds, joined with newlines into a single string, and searched
case-insensitively.

Joining matters because a probe's substrings may straddle a line break.
Clamping matters because a probe on line 1 or on the final line must validate
normally rather than crashing or silently searching a truncated window.

The window exists to catch line-reference drift. When a fixture is edited and a
claim moves, the reference must fail loudly rather than point at nearby prose
that happens to still parse.

### `strict` and `lenient`

These are **scoring modes over label sets, not sensitivity levels**.

- **strict** grades a probe against `expected_verdict` alone.
- **lenient** grades against `{expected_verdict} ∪ also_acceptable`.

The two modes differ only on probes with a non-empty `also_acceptable`. On
every other probe they are the same check - which today means seven of the
eight fixtures score identically either way, `numeric_drift` being the one
exception. Neither mode means "more flags" or "fewer flags".

## `expected.json`

```json
{
  "schema_version": 4,
  "fixture": "contradiction",
  "kind": "defect",
  "description": "A and B assert incompatible values for the same attribute; the merge silently takes B.",
  "plants": ["source_a says a 30 second connect timeout; source_b says 60 seconds"],
  "merged": "merged.md",
  "prompts": {
    "source_to_merged": "prompts/verify.md",
    "merged_to_sources": "prompts/verify_reverse.md"
  },
  "claim_count_band": {
    "source_a.md": [8, 14],
    "source_b.md": [8, 14],
    "merged.md": [8, 14]
  },
  "probes": [
    {
      "probe_id": "connect-timeout-a",
      "direction": "source_to_merged",
      "document": "source_a.md",
      "line": 12,
      "text": "The default connect timeout is 30 seconds.",
      "must_extract": true,
      "anchor": { "all_of": ["connect timeout", "30 seconds"] },
      "match": { "all_of": ["connect timeout", "30 seconds"] },
      "expected_verdict": "CONTRADICTED",
      "also_acceptable": [],
      "expected_finding": "contradicted",
      "prompt": "prompts/verify.md",
      "note": "merged.md carries B's 60 second value, so this must be CONTRADICTED, not MISSING."
    }
  ],
  "must_not_extract": [],
  "expected_conflicts": [
    {
      "conflict_id": "connect-timeout",
      "attribute": "default_connect_timeout",
      "probes": ["connect-timeout-a", "connect-timeout-b"],
      "reason": "incompatible values for the same attribute",
      "human_decision_required": true
    }
  ],
  "expected_exit_code": { "strict": 1, "lenient": 1 }
}
```

### Fixture-level fields

| field | notes |
|---|---|
| `schema_version` | `4`. `1` -> `2` was the `anchor`/`match` split and the arrival of `must_not_extract`. `2` -> `3` is `held_out`, the `basis` field on a `must_not_extract` assertion, and `expected_evidence_source` becoming a list. `3` -> `4` is `notes_evidence`, the reversed meaning of an empty evidence list, and `GLOBAL.json`. All four change what a valid fixture looks like. |
| `fixture` | Must equal the directory name. |
| `kind` | `defect` - a flaw is planted, and `plants` describes it. `guard` - the merge is correct and the fixture exists to catch over-flagging; `plants` is `[]`. |
| `held_out` | Boolean, required. `true` means no prompt was tuned against this fixture: it was written after the prompts it grades and has never been read while editing them. A number from the held-out set and a number from the rest are different claims, and the field is what lets a report say which it is. Declared, never inferred - the claim is about history, and history is not derivable from the file. |
| `description` | One sentence. Required, non-empty. |
| `plants` | List of the specific defects planted. Non-empty iff `kind` is `defect`. |
| `merged` | Always `merged.md`. Present so nothing has to hardcode the name. |
| `prompts` | Prompt file path per `direction`. Overridable per probe. Paths are **declared, not resolved** - the validator does not check that the file exists, because a prompt may be named before it is written. |
| `claim_count_band` | `[lo, hi]` per document, required for **all three** documents even where nothing currently decomposes `merged.md`. A conditional rule would be one more thing to reason about; two unused numbers are cheaper. |
| `probes` | Non-empty. |
| `must_not_extract` | Required on every fixture, may be `[]`. Patterns no extracted claim may match, each declaring the `basis` on which it is forbidden. See below. |
| `expected_conflicts` | May be empty. |
| `expected_exit_code` | Always a `{strict, lenient}` map, never a bare integer. |
| `note` | Optional. What the fixture as a whole is for, where that is not obvious from `description` and `plants`. |

### Probe fields

| field | notes |
|---|---|
| `probe_id` | Unique within the fixture, kebab-case. |
| `direction` | `source_to_merged` or `merged_to_sources`. **Required on every probe, including coverage ones.** There is no default: a missing `direction` is a validation error, not an implied `source_to_merged`. |
| `document` | Must be in the domain `direction` allows (see the table above). |
| `line` | 1-based line in `document`. |
| `text` | The claim, written the way a careful human would write it. |
| `must_extract` | Decompose assertion: decompose must produce a claim matching this probe. |
| `anchor.all_of` | Case-insensitive substrings that must appear in `document` near `line`. Catches line-reference drift. Never matched against model output. |
| `match.all_of` | Case-insensitive substrings that must appear in this probe's `text`, and that an extracted claim must contain to be aligned to this probe. Not a verdict, and not evidence. |
| `expected_verdict` | Closed set: `SUPPORTED`, `CONTRADICTED`, `MISSING`. |
| `also_acceptable` | Additional labels that are genuinely defensible for this probe. Disjoint from `expected_verdict`. Usually `[]`. |
| `expected_finding` | Closed set: `dropped`, `contradicted`, `hallucinated`, `none`. Derived - see below. |
| `expected_evidence_contains` | Optional. A list of substrings the returned evidence span must **all** contain, checked against the `target`. `[]` asserts nothing at all, exactly as omitting the field does, and must be accompanied by `notes_evidence`. Required to discriminate on `CONTRADICTED` probes - see below. |
| `expected_evidence_source` | Optional. A **list** of target filenames, any one of which the returned `evidence_source` may name. `[]` asserts nothing, on the same terms as an empty `expected_evidence_contains`. See below. |
| `notes_evidence` | Optional, and **required** when either evidence list is `[]`. Why this probe deliberately asserts nothing about evidence. See below. |
| `prompt` | Optional per-probe override of the direction-level prompt. |
| `note` | Optional. Why this probe expects what it expects. |

### `must_not_extract`

`must_extract` says a claim has to be produced. `must_not_extract` says a claim
must not be, and it catches the opposite defect: not a decomposer that drops a
fact, but one that produces a claim its document never made.

```json
"must_not_extract": [
  {
    "assertion_id": "no-princess-to-forest",
    "document": "merged.md",
    "basis": "absent",
    "pattern": "(?i)\\bprincess\\b[^.]*\\b(old lady|forest|witch|herbs?)\\b",
    "reason": "the two sources share no content; a claim linking the princess to the forest story is invented, not merged"
  }
]
```

| field | notes |
|---|---|
| `assertion_id` | Unique within the fixture, kebab-case. |
| `document` | Which document's claims the pattern applies to. Declared, never assumed to be `merged.md`. |
| `basis` | Why the pattern is forbidden. `absent` - the text is not in the document, so a matching claim would be invented. `not_a_claim` - the text *is* in the document but is not an assertion about its subject. Required, because the two need opposite offline checks and nothing in the pattern says which is meant. |
| `pattern` | A Python regular expression, matched with `re.search` against each extracted claim's text. Case-insensitivity is written into the pattern rather than implied, because these are hand-tuned and a silent flag is one more thing to remember. |
| `reason` | Why this claim would be wrong, in the terms a human reviewer would use. |

Everything here is a **whole-fixture** assertion, not a probe. There is no
`line`, because the assertion is that no such claim exists anywhere in that
document's output.

#### The validator checks the assertion is satisfiable

An offline check cannot know whether a model will produce a forbidden claim.
What it can check is that the fixture is not asking for something impossible,
and there are three ways a `must_not_extract` entry can be a trap rather than an
assertion. The first is the same whatever the basis:

- **The pattern matches a `must_extract` probe on the same document.** Then the
  fixture requires and forbids the same claim.

The other two are the reason `basis` is a declared field, because they are
opposite checks and the pattern alone does not say which one applies:

- `basis: "absent"` - **the pattern must not match the document's own prose.**
  It matching means a faithful decomposition would produce a claim that matches,
  and the fixture would punish correct behaviour. `dropped_claim` forbids a JSON
  Lines claim from `merged.md`, where the log format is its planted omission,
  while requiring one from `source_b.md`, where the fact genuinely is. Those two
  do not collide, and a validator that assumed `merged.md` could not have told
  that - which is also why `document` is declared rather than assumed.
- `basis: "not_a_claim"` - **the pattern must match the document's own prose.**
  Here the text being present is the whole point: it is there and must not
  become a claim. `structure_added/merged.md` opens with "Merged from
  source_a.md and source_b.md on 2026-08-07", which is a fact about the merge
  and not about the relay, and `prompts/decompose.md` tells the model to skip
  exactly this. A pattern matching nothing in the document is inert - there is
  no prose for a decomposer to wrongly turn into a claim - so the validator
  rejects it, the same way it rejects a `must_extract` probe whose line
  reference has drifted.

#### A violation is not put to a majority vote

Every other figure the decompose runner reports is over the modal outcome of several
runs. This one is not: an assertion counts as violated if **any** run tripped
it, and the report says how many did.

A claim the document never made is a defect the first time it appears. A
decomposer that invents one in one run of three is not two-thirds trustworthy.
Majority voting exists to keep a noisy measurement from reporting noise as
signal, and this is not a measurement of degree.

#### Global assertions: `GLOBAL.json`

`tests/fixtures/GLOBAL.json` holds `must_not_extract` assertions that apply to
every document of every fixture. It exists for claims no document in the suite
could ever legitimately produce, where scoping the assertion to one fixture
would leave the other eleven unguarded. Its entries have the same fields as a
fixture's own minus `document`, since they apply to all three, and
`assertion_id` must be unique across the global file and every fixture together.

Two rules make a global assertion different from a local one:

- **`basis` must be `absent`.** `not_a_claim` asserts the text *is* present in a
  particular document and must not become a claim. Presence is a property of one
  file, so no assertion about the whole set can make it.
- **The pattern is checked against all three documents of every fixture**, not
  against one. A phrase that becomes legitimate prose in a future fixture fails
  the validator there and then, rather than quietly turning that fixture's
  correct decomposition into a violation.

What is in it today is the `prompts/decompose.md` worked examples. `qwen3:4b`
returned the prompt's kiln-and-glaze illustration as its extraction for four
documents, in three samples of three, with valid JSON and a plausible line
number; nothing but span anchoring noticed. The assertions turn a recurrence of
that into a named failure on the document it happened to, in any model.


#### Which `merged.md` assertions transfer to a *generated* merge

A `must_not_extract` entry scoped to `merged.md` describes the committed
hand-written merge. The merge harness generates that document instead of reading it, so most of
those assertions do not survive the move - `dropped_claim/no-restored-log-format`
forbids a JSON Lines claim precisely because the hand-written merge omits the log
format, while a correct generated merge is *required* to carry it.

The rule is derived rather than kept as an exclusion list
(`tests/run_merge.py:249`):

> A `merged.md` `absent` assertion transfers **iff its pattern matches neither
> source.**

If the pattern matches a source, a correct merge must carry that text and the
assertion contradicts the merge rules. If it matches neither, the text is absent
from everything the model was shown, so a claim of it is invention either way and
the assertion is about the model rather than about one document.

`basis: not_a_claim` never transfers. It asserts that text present in one
particular document must not become a claim, which is a statement about that
document's prose, not about a merge of it. All three in the suite are in
`structure_added`.

Applied to the suite this selects three of the four `merged.md` `absent`
assertions: `disjoint_sources`'s two cross-story assertions and
`ordering_only/no-misrendered-max-connections-merged` transfer;
`no-restored-log-format` is dropped. `GLOBAL.json` applies unconditionally in
every milestone.

### Conflict fields

| field | notes |
|---|---|
| `conflict_id` | Unique within the fixture, kebab-case. |
| `attribute` | The shared attribute the probes disagree about, in snake_case. This is what value-level conflict detection pairs on in the report layer, and it is the only field that lets a conflict be found when both probes come back `SUPPORTED`. |
| `probes` | At least two `probe_id`s, all declared in this fixture. A conflict between fewer than two claims is not a conflict. |
| `reason` | Why these claims are incompatible, in the terms a human reviewer would use. |
| `human_decision_required` | Always `true` today. The tool never picks a winner; the field exists so the report does not have to infer that. |
| `note` | Optional. Implementation context, such as which milestone can actually detect this conflict. |

### `anchor.all_of` and `match.all_of` - two jobs, two fields

Until `schema_version: 2` this was one field doing both jobs:

1. **Anchoring.** The offline validator checks substrings against the
   `document`'s own prose, in the window around `line`. This catches a line
   reference that has drifted.
2. **Alignment.** The decompose and verify harnesses check substrings against an LLM-*extracted* claim,
   to decide which probe that claim answers to.

The two agree while a document writes its facts as sentences. They pull apart
when it writes them as a list or a table, because a claim extracted from
`- Retry attempts per request: 3` reads "a request is retried at most 3 times"
and shares almost no wording with the line it came from. Morphology is why a
substring rule cannot do better: *Retry* and *retried* share no whole word.
Fuzzy matching is not the fix - a fixture that matches approximately stops being
ground truth.

| field | checked against | job |
|---|---|---|
| `anchor.all_of` | `document`, in the window around `line` | catch line-reference drift |
| `match.all_of` | the probe's own `text` offline; an extracted claim at run time | align a claim to a probe |

Both are required on every probe. Both are non-empty lists of non-empty strings,
matched case-insensitively, and all substrings must be present.

**The offline check on `match.all_of` is the one that was missing.** Under
`schema_version: 1` only the anchoring job was verified offline; nothing checked
that the substrings were sayable by a claim, so a probe could be written that no
extracted claim could ever match and it would validate. The rule now is that
every `match.all_of` substring must appear in the probe's own `text` - the
minimum evidence that some claim of this fact can match it.

**What the split does not license.** `match.all_of` must not be tightened
against recorded model output. Widening `anchor.all_of` to the document's exact
wording is free, because it is graded offline against a file that is checked in.
Tightening `match.all_of` until the claims a particular model happened to
produce are the ones that match is fitting the fixture to the model, which is
the failure the whole corpus exists to prevent.

At the v2 migration exactly one probe had genuinely compromised substrings -
`paraphrase/b-retry-limit`, the list-row case above. Its anchor became the
document's own `Retry attempts per request`; its `match` was left at the weak
`request` + `3` it has always had. Every other probe's two fields are identical
today, and that is the expected steady state: the split exists so they *can*
diverge without one job silently degrading the other, not because they usually
do.

### Deriving `expected_finding`

`expected_finding` is fully determined by `(expected_verdict, direction)`:

| `expected_verdict` | `direction` | `expected_finding` |
|---|---|---|
| `SUPPORTED` | either | `none` |
| `CONTRADICTED` | either | `contradicted` |
| `MISSING` | `source_to_merged` | `dropped` |
| `MISSING` | `merged_to_sources` | `hallucinated` |

The field is written out rather than computed at read time because it is what
the report renders, and because it survives a change to the verdict vocabulary
of the verify pass. Because it is derivable, the validator **enforces** this table rather
than trusting the value. A hand-edited fixture declaring `MISSING` with
`contradicted` is an error.

Under **lenient** scoring the expected finding is re-derived from whichever
acceptable label actually came back. For `numeric_drift`, an observed
`SUPPORTED` implies `none`, not the declared `contradicted`. That is the only
reading consistent with the table above.

### `MISSING` means two different things

Under `source_to_merged`, `MISSING` is a **dropped** claim: the merge lost a
fact that a source asserted. Under `merged_to_sources`, `MISSING` is a
**hallucinated** claim: the merge invented a fact neither source asserted.

Same verdict label, opposite failure class, different severity, different
section of the report. This is the reason `expected_finding` exists as a field
and the reason `direction` may never be defaulted.

## Deriving the exit code

The exit code is not stored independently of the probes - it is cross-checked
against them, in both modes:

- `strict == 0` iff every probe's `expected_verdict` is `SUPPORTED` **and**
  `expected_conflicts` is empty. Otherwise `1`.
- `lenient == 0` iff every probe has `SUPPORTED` in
  `{expected_verdict} ∪ also_acceptable` **and** `expected_conflicts` is empty.
  Otherwise `1`.

This is what stops a fixture with a `MISSING` probe from being marked exit 0.

### Exit 2 supersedes both, and means "did not measure"

`expected_exit_code` describes a run in which every call was answered in a
usable form. A run where some were not is a different kind of outcome, and the
schema does not try to predict it.

A probe has a fourth possible status, alongside the three verdicts:

| status | meaning |
|---|---|
| `SUPPORTED` / `CONTRADICTED` / `MISSING` | the model judged the claim |
| `error` | the model could not be made to answer in a usable form |

`error` is not a verdict and is never one. It is what the tool reports when two
schema attempts both failed. The rules:

- Any probe with status `error` makes the whole run **inconclusive**.
- An inconclusive run **exits 2**, whatever the coverage and conflicts were.
  Exit 2 overrides the `{strict, lenient}` values in every fixture.
- Coverage is computed over non-errored probes only, and the denominator is
  printed next to it. Errored probes are never counted as covered and never
  counted as missing.

The distinction being protected: "the claim is absent from the merge" and "the
model failed to answer" are different facts about the world. Folding the second
into the first would let a broken endpoint report clean coverage, which is the
exact failure this tool exists to catch in someone else's merge. A fixture that
exits 2 has not failed - it has not been measured, and the number it would have
produced does not exist.

## Defect fixtures and guard fixtures

Six fixtures plant a defect. Ten are guards: the merge is correct, and the
fixture exists to catch a tool that flags anyway. Sixteen in total, and the
split is uneven by accident rather than by design - no rule requires it, and
adding a seventeenth fixture would not need a matching one on the other side.

Two of the ten are guards on a technicality and the sections after the table say
so: `concatenated` and `restated` carry `"kind": "guard"` because their own
probes imply exit 0 and `kind` has to agree with them, not because their merges
are correct.

These counts and the table below are derived from the tree, not recalled: the
row set must equal the fixture directories, and the two `kind` tallies must
equal what the `expected.json` files say. They said six and six for as long as
there were twelve fixtures, and stayed there through two additions.

| fixture | kind | what it catches |
|---|---|---|
| `dropped_claim` | defect | a fact present in a source and absent from the merge |
| `contradiction` | defect | the merge silently picking one side of a disagreement |
| `hallucination` | defect | the merge asserting a fact from neither source |
| `numeric_drift` | defect | "approximately 500" against "512" |
| `paraphrase` | guard | flagging a restatement as missing |
| `ordering_only` | guard | flagging reordered content as missing |
| `conflict_surfaced` | guard | flagging a correctly-surfaced disagreement |
| `disjoint_sources` | guard | flagging a correct concatenation of two unrelated documents as a defect |
| `attribution_invented` | defect | a preserved fact credited to a source that never states it |
| `attribution_swapped` | defect | both values surfaced, each credited to the wrong source |
| `structure_added` | guard | extracting headings, a table of contents or a provenance note as fact |
| `dedup` | guard | flagging a correctly deduplicated fact as dropped, or as coming from the wrong file |
| `disjoint_domains` | guard | the same guard as `disjoint_sources` against a second subject matter - matched to it on line, segment, kind and word count, so a measurement that scores the two differently is reading the subject, not the shape |
| `list_structure` | guard | fusing separate atomic list items, or losing one, where both sources state their facts as bullets |
| `concatenated` | guard | nothing, and that is the point: two overlapping sources glued together whole, which every probe the schema can express calls correct |
| `restated` | guard | the same as `concatenated`, on output a model really produced: a real `--fidelity low` merge that keeps both sources' wording of every fact, and that the tool passed clean |

`disjoint_sources` has carried `"kind": "guard"` in its own `expected.json`
since it was written; this row once said `defect`, and nothing
validated the two against each other. The fixture is a guard, and the reading is
the guard reading: its two sources share no subject, so there is nothing to
interleave and its `merged.md` is byte-exactly `source_a + "\n" + source_b`. A
tool that treats concatenation as evidence of a lazy merge must not fire here,
because here it is the correct output. That is also what makes the fixture the
one exclusion in the post-hoc concatenation counter (`tests/analyse_merges.py`), which reads the reference
merge rather than a threshold.

### `concatenated` is a guard that records a blind spot

`concatenated` is the other side of that coin and the two must be read together.
`disjoint_sources` is a concatenation that is **right**, because its sources
share no subject. `concatenated` is a concatenation that is **wrong**, because
its two sources state the same five facts and the merge keeps both copies of
every one of them. Concatenation is not the defect; concatenating sources that
overlap is.

It carries `"kind": "guard"` and `expected_exit_code {0, 0}`, and neither says
the merge is correct. They say what the schema at version 4 is able to say:

- Every probe is `SUPPORTED` in both directions, and every one of them is
  **right**. Each source claim really is carried into the merge, and each merge
  claim really is grounded in a source. The verify pass is not being fooled; it
  is answering the question it was asked, correctly, and that question does not
  cover how many times the merge said a thing.
- `kind` has to agree with what the probes imply - `tests/test_fixtures.py`
  enforces it, and a `defect` whose probes imply exit 0 has nothing to detect.
  So the fixture cannot be registered `defect` without a verify-level defect
  planted beside the redundancy, which would make it a two-variable fixture and
  destroy the comparison it exists to make.
- There is no field for the assertion it would rather make.
  `tests/fixture_semantics.py` says so in as many words: `report.exit_code`
  returns 1 for a structural finding, "neither is declarable in a fixture, so
  neither is derivable here". `expected_exit_code` describes the findings path.
- And `llossless verify`, which is what `tests/run_detect.py` runs over this
  corpus, does not run the reconciler at all - `src/llossless/cli.py` reaches
  it only when a merge was generated. So the exit code this fixture declares
  could not have seen a document-level finding even if one existed.

What the fixture is for, then, is the record. It holds the shape still so that a
predicate can be measured against it, and it is the corpus's only member with
that shape:

- `order.sequence` is `aababababab`. The sources alternate, so `runs` exceeds
  the number of distinct documents and `reconcile.Order.stapled` is **false** -
  the staple detector is blind to an interleaved concatenation, which is what
  the two disjoint guards could never have shown.
- The two copies of each fact are two wordings, so check 9's exact pass is
  silent. Their character similarity runs 0.291 to 0.692, which sits inside the
  range the corpus's *correct* documents already occupy, so no `NEAR_MATCH`
  separates them either.
- Merged body length is exactly the sum of the two sources' - nothing was
  collapsed and nothing was added.
- The reconciler reports **two** findings on it, both about source B's title.
  Only four fixtures score lower - `list_structure` and `ordering_only` at 0
  and the two disjoint controls at 1 - and every other fixture in the corpus
  scores 5 or more. By the tool's own arithmetic the concatenation is among the
  cleanest-looking merges in the set.

`conflict_surfaced` uses source documents byte-identical to `contradiction`'s
and differs only in `merged.md`, where the disagreement is surfaced rather than
silently resolved. Its signature is distinct from `contradiction`'s: both
probes `SUPPORTED`, the conflict still reported, the exit code still 1. Without
it, a tool that reflexively returns `CONTRADICTED` for one side of any
disagreement passes `contradiction` cleanly and fails on every document the
merge model got right. The brief's rule is that the tool must never silently
pick a winner - surfacing is the rewarded behaviour, so surfacing needs a
fixture where it scores clean.

It is also the fixture that tests the *prompt's* precision rather than only the
model's. Its `merged.md` states both values under attribution, so a verify
prompt saying no more than "a different value for the same attribute is
CONTRADICTED" makes the fixture unpassable by a model that follows it
faithfully - both probes would come back `CONTRADICTED`, and the failure would
read as a model deficiency when it is a specification gap. Two rules in
`prompts/verify.md` close it: attributed content still counts as stated, and
several attributed values for one attribute leave each of them `SUPPORTED`,
with the disagreement recorded as a conflict rather than as a contradiction of
either side. That second rule is where "never silently pick a winner" is
expressed at the verdict level.

**The guard fixtures must be clean in both directions.** `paraphrase`,
`ordering_only` and `conflict_surfaced` each carry `merged_to_sources` probes
alongside their forward ones. Without those, `hallucination` would be the only
fixture exercising the reverse direction, and it only ever asks the reverse
pass to flag something - so a reverse pass that flagged legitimately merged
content as hallucinated would pass every fixture in the set.

`conflict_surfaced` carries the reverse probes that matter most: two of its
three sit on attributed sentences. "X states that P" does not classically
entail "P", reported speech is a known hard case in entailment work, and
attribution is exactly where a reverse pass over-flags. The attributions are
grounded - `source_a.md` genuinely is titled *Vandrell Relay - Operator Guide*
and `source_b.md` *Vandrell Relay - Deployment Notes* - so a reverse flag on
either is a false positive, not an invented entity. No other fixture exercises
this.

### Considered and not created: `abbreviation`

Proposed while planning the merge harness and deliberately left out. It would probe whether
writing `30s` for `30 seconds` is a notation change - silent, per the notation
rule above - or an information change.

That is the boundary `numeric_drift` already sits on. Two probes in the suite
carry an `also_acceptable` list - `attribution_invented/m-tls-attributed` admits
one alternative, and `numeric_drift/a-max-connections` admits two, which makes it
**the only probe in the suite where all three verdicts are acceptable**:
`CONTRADICTED` declared, `also_acceptable: ["SUPPORTED", "MISSING"]`, widened on
2026-08-07 after a one-sample sweep of six models split 4 `CONTRADICTED` /
1 `SUPPORTED` / 1 `MISSING`, its own note concluding the probe is genuinely soft
rather than the models failing. A probe that accepts every verdict discriminates
nothing, and a second fixture on the same boundary would add more of them.

Recorded because the absence is a decision. The next reader counting fixtures
against the notation rule will otherwise ask the same question and re-derive the
same answer.

## Validation

`python3 tests/test_fixtures.py` checks the fixtures structurally. It parses
what is committed and nothing else: no network, no model call, no third-party
dependency.

It deliberately does **not** judge whether an expected verdict is *right*, does
not compare probe `text` against document prose, and does not call a model.
Those are what the decompose and verify harnesses measure. The moment this script starts having opinions
about verdicts, it has stopped being a fixture check.

**The validator counts one unit more than there are fixtures.** That extra unit
is `GLOBAL.json`, which has no sources, no `merged.md` and no probes, and
contributes nothing to any probe denominator. The two numbers are not a
discrepancy, and the sweep runners print `N fixtures (+1 GLOBAL)` so they cannot
be read as one. Neither number is written down here: the count has changed three
times and a figure in prose goes stale silently.

## `disjoint_domains` carries two jobs, and only one of them is in its `kind`

The fixture is a concatenation control: its two sources share no subject matter,
so the correct merge is the two documents one after the other and a tool that
merely concatenates cannot be told from one that merges. That is what it was
added for and it is what `kind` records.

The second job was not designed and is not in any field. Because the correct
merge rewrites nothing, any rewriting at all is a defect on this input, and that
makes it the only fixture in the suite on which the reverse pass can see a
transcription error or an invented claim. On the thirteen-fixture run all 12
transcription errors and 6 of the 7 invented claims are this fixture, and it is
the sole reason the all-thirteen grounding figure is 535/547 and not 100%; it is
simultaneously perfect forward, 36/36 in both thinking conditions. Every other
fixture permits some legitimate rewording, and a reworded span cannot be
separated from a transcription slip by an answer key that did not anticipate the
wording.

Practical consequence for anyone editing fixtures: **rewording either source of
`disjoint_domains`, or dropping it, removes the suite's entire coverage of two
failure classes and the loss shows up as an improvement** - grounding returns to
100% because nothing is looking any more.
