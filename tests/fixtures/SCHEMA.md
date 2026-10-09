# Fixture format

This page is the format of the test fixtures in `tests/fixtures/`. Read it before you add a fixture or change one. It says what the files are, lists the sixteen fixtures, defines every field of `expected.json` with the values it allows, says which test reads which field, and names the fixtures that are easy to break by editing. To check a fixture you have just written, run `python3 tests/test_fixtures.py`.

## What a fixture is

A fixture is one small test case: two source documents, a merge of them, and an answer key that says what LLossless must report about that merge. Each fixture is a directory under `tests/fixtures/` with four files.

| file | what it is |
|---|---|
| `source_a.md` | one of the two input documents |
| `source_b.md` | the other input document |
| `merged.md` | a merge of the two, written for the fixture, with a defect planted in it or with none |
| `expected.json` | the answer key: the statements to check, the verdict each must get, and the exit code that follows |

`tests/fixtures/GLOBAL.json` is not a fixture. It holds assertions that apply to every document of every fixture and is described under [`GLOBAL.json`](#globaljson).

**The fixtures are ground truth.** The documents are written for the fixture, the answer key is written from the documents alone, before any model under test sees them, and neither is ever edited to make a result look better. If the tool and a fixture disagree, either the tool is wrong or the fixture was wrong about its own documents from the start. A fixture that is merely inconvenient is neither.

**Who wrote them.** With the one exception below, AI coding agents wrote the fixtures, sources, merges and answer keys alike, under the direction of the project's author, who reviewed them.

**One fixture's merge comes from a run of the tool.** The `merged.md` of `restated` is a merge a model really produced when the tool ran, and the directory carries a fifth file, `recorded-claims.json`. Its two sources are the documents of `tests/handwritten/christianity/`. That is deliberate and happens once: see [`restated`](#restated-is-real-model-output-and-the-corpuss-only-one). Every other fixture is four files written for it, and a new one should be too.

**What the documents are about.** Twelve fixtures describe Vandrell Relay, an invented HTTP relay, and draw on one pool of facts: listen port, connect timeout, read timeout, maximum concurrent connections, retry limit, minimum TLS version, access log format and health check path. They read as variants of one document, so a difference in results comes from the planted defect and not from the subject. Write a new fixture from the same pool unless the thing it tests is the kind of text. The four fixtures outside the pool are under [Special fixtures](#special-fixtures).

## The sixteen fixtures

`kind` is `defect` when a flaw is planted in `merged.md` and `guard` when there is nothing to find and the fixture catches a tool that reports something anyway. The exit code is what `llossless verify` must return on the fixture's three documents: `0` for nothing found, `1` for a finding.

| fixture | kind | what it tests | exit code |
|---|---|---|---|
| `attribution_invented` | defect | The merge keeps a fact but credits it to the source that never states it. | 1 |
| `attribution_swapped` | defect | The merge shows both values of a disagreement and credits each to the wrong source. | 1 |
| `concatenated` | guard | Two sources that state the same facts are glued together paragraph by paragraph, so every fact is stated twice. `verify` finds nothing, and the fixture records that. | 0 |
| `conflict_surfaced` | guard | The same disagreement as `contradiction`, with both values shown and attributed. It must not be reported. | 0 |
| `contradiction` | defect | The sources disagree on a value and the merge silently keeps one. | 1 |
| `dedup` | guard | Facts stated in both sources appear once in the merge. They must not be reported as dropped, or as cited from the wrong file. | 0 |
| `disjoint_domains` | guard | The same test as `disjoint_sources` on a second subject, with the same shape line for line. | 0 |
| `disjoint_sources` | guard | Two unrelated stories are merged by placing one after the other, which is correct here. Nothing may be reported, and no claim may link the two stories. | 0 |
| `dropped_claim` | defect | A fact stated in a source is missing from the merge. | 1 |
| `hallucination` | defect | The merge states a fact that neither source states. | 1 |
| `list_structure` | guard | Both sources are bullet lists. Separate list items must stay separate claims, and none may be lost. | 0 |
| `numeric_drift` | defect | One source says "approximately 500", the other says 512, and the merge silently keeps 512. | 1 strict, 0 lenient |
| `ordering_only` | guard | The same facts with the sections in a different order. It must not be reported. | 0 |
| `paraphrase` | guard | The same facts in three different wordings, with every value identical. It must not be reported. | 0 |
| `restated` | guard | A merge a model really produced, which keeps both sources' wording of every fact. `verify` finds nothing, and the fixture records that. | 0 |
| `structure_added` | guard | A correct merge that adds headings, a table of contents and a provenance note. None of that may be extracted as a fact. | 0 |

Six fixtures are defects and ten are guards. `concatenated` and `restated` are guards only because their answer keys expect exit 0: neither merge is a good one, as their sections below explain.

The published detection figures count thirteen of the sixteen. `list_structure`, `concatenated` and `restated` are outside the block that was registered before the benchmark ran (`PREREGISTERED_BLOCK` in `tests/run_detect.py`), and so is any fixture added later.

## How to add a fixture

1. **Decide the one thing the fixture tests.** Hold everything else constant. A fixture that varies two things cannot say which of them moved a result.
2. **Create `tests/fixtures/<name>/`** and write `source_a.md` and `source_b.md` from the fact pool. Write each value the same way in every document unless the difference is the defect (see [Notation is not information](#notation-is-not-information)).
3. **Write `merged.md` yourself; do not take it from a run of the tool.** For a defect fixture, plant exactly one kind of defect. For a guard, write a correct merge.
4. **Write `expected.json` from the three documents, before any model under test has seen them.** Use the [field reference](#expectedjson-field-reference). Give each planted defect at least one probe, and add control probes for facts that survive. Give a guard probes in both directions, so that a reverse check that reports correctly merged content as invented fails it.
5. **Derive, do not choose, three fields.** `expected_finding` follows from the verdict and the direction, `expected_exit_code` follows from the probes, and `kind` must agree with both. The rules are under [Deriving `expected_finding`](#deriving-expected_finding) and [Deriving the exit code](#deriving-the-exit-code).
6. **Pin how the new documents are segmented:** `python3 tests/test_segment.py --pin`. It adds a digest for each new document to `tests/segment_pins.json` and never rewrites an existing one.
7. **Record model answers for the new documents.** Run with `--offline`, the harnesses replay recorded answers, and a recording is keyed by the document text, so a new document has none. `tests/responses/README.md` has the commands.
8. **Run `python3 tests/test_fixtures.py`** until your fixture's line reads `ok`. Then run `python3 tests/run_all.py`: it fails on every test that counts the fixtures on purpose, which is the list of places to update.

**To change an existing fixture, expect the same costs.** Any change to a source or to `merged.md` invalidates the recordings made from that document and its segmentation pin, and moves line numbers that probes refer to. A change to `expected.json` changes the answer key, and is right only when the key was wrong about its own documents, never because a model answered differently. The existing fixtures record such a repair, with its date and reason, in a `note`.

## `expected.json` field reference

The validator rejects an unknown key at the top level and in a `must_not_extract` entry. It does not check probe and conflict entries for unknown keys, so a misspelt optional field there passes silently and asserts nothing.

### Top level

| field | type | required | allowed values | meaning |
|---|---|---|---|---|
| `schema_version` | integer | yes | `4` | The version of this format. |
| `fixture` | string | yes | the directory name | The fixture's name. |
| `kind` | string | yes | `defect`, `guard` | `defect`: a flaw is planted and the probes imply exit 1. `guard`: nothing is planted and the probes imply exit 0. The validator rejects a `kind` that disagrees with the probes. |
| `held_out` | boolean | yes | `true`, `false` | `true` means no prompt was tuned against this fixture: it was written after the prompts it grades and was not read while they were edited. It is declared because it is a statement about history, which no file can show. |
| `description` | string | yes | not empty | What the fixture tests. |
| `plants` | list of strings | yes | not empty for `defect`, `[]` for `guard` | Each planted defect, in words. |
| `merged` | string | yes | `merged.md` | The name of the merged document. |
| `prompts` | object | yes | `source_to_merged`: `prompts/verify.md`; `merged_to_sources`: `prompts/verify_reverse.md` | The prompt each direction is verified with. Every direction a probe uses needs an entry. `tests/test_verify.py` fails if the file does not exist or is not the prompt the tool uses for that direction. |
| `claim_count_band` | object | yes | one `[lo, hi]` pair of integers for each of `source_a.md`, `source_b.md` and `merged.md`, with 1 <= lo <= hi | How many claims the decompose step may extract from each document, bounds included. |
| `probes` | list | yes | not empty | The statements to check. See [Probe](#probe). |
| `must_not_extract` | list | yes | may be `[]` | Patterns no extracted claim may match. See [`must_not_extract` entry](#must_not_extract-entry). |
| `expected_conflicts` | list | yes | may be `[]` | Pairs of probes that state incompatible values. See [`expected_conflicts` entry](#expected_conflicts-entry). |
| `expected_exit_code` | object | yes | exactly `strict` and `lenient`, each `0` or `1` | The exit code of `llossless verify` on this fixture. The validator derives both values from the probes and rejects a mismatch. |
| `note` | string | no | any | What a reader needs to know that `description` and `plants` do not say. |

### Probe

A probe is one statement in one document, with the verdict the tool must give it.

| field | type | required | allowed values | meaning |
|---|---|---|---|---|
| `probe_id` | string | yes | kebab-case, unique in the fixture | The probe's name. |
| `direction` | string | yes | `source_to_merged`, `merged_to_sources` | Which check the probe belongs to. There is no default. |
| `document` | string | yes | `source_a.md` or `source_b.md` for `source_to_merged`; `merged.md` for `merged_to_sources` | The document the statement comes from. |
| `line` | integer | yes | 1 to the number of lines in `document` | The line the statement is on. Line 1 is the first line, and blank lines count. |
| `text` | string | yes | not empty | The statement, as a careful person would write it. The verify harness sends this text to the model as the claim. |
| `must_extract` | boolean | yes | `true`, `false` | `true`: the decompose step must extract a claim that contains every `match.all_of` substring, on a line within 2 of `line`. `false`: decompose is not graded on this probe. |
| `anchor.all_of` | list of strings | yes | not empty | Substrings that must all occur in `document` within the [anchoring window](#the-anchoring-window) around `line`. It catches a line number that has drifted. The detection harness also uses these substrings to recognise the tool's finding about this probe. |
| `match.all_of` | list of strings | yes | not empty | Substrings an extracted claim must all contain to count as this probe's claim. Each must also occur in the probe's own `text`. |
| `expected_verdict` | string | yes | `SUPPORTED`, `CONTRADICTED`, `MISSING` | The verdict the tool must return. |
| `also_acceptable` | list of strings | yes | any of the three verdicts except `expected_verdict`; usually `[]` | Other verdicts that are a defensible reading of the documents. See [`strict` and `lenient`](#strict-and-lenient). |
| `expected_finding` | string | yes | `none`, `contradicted`, `dropped`, `hallucinated` | What the report files for the expected verdict. It must equal the derived value. |
| `expected_evidence_contains` | list of strings | no | substrings of the target | Substrings the evidence the model quotes must all contain. See [Evidence expectations](#evidence-expectations). |
| `expected_evidence_source` | list of strings | no | filenames of the target, none twice | The files the model may name as the source of its evidence. Any one of them is a correct answer. |
| `notes_evidence` | string | only when either evidence list is `[]` | not empty | Why the probe deliberately asserts nothing about evidence. |
| `prompt` | string | no | a prompt path | Stands in for the `prompts` entry of this probe's direction. No fixture uses it and no harness reads it. |
| `note` | string | no | any | Why the probe expects what it expects. |

Substring comparisons ignore case. An id is kebab-case when it is lowercase letters and digits joined by single hyphens, such as `a-read-timeout`.

**`document` and target.** `document` is where the statement comes from. The target is what it is verified against. Both follow from `direction`.

| `direction` | `document` | target |
|---|---|---|
| `source_to_merged` | `source_a.md` or `source_b.md` | `merged.md` |
| `merged_to_sources` | `merged.md` | `source_a.md` and `source_b.md` |

The two are easy to swap. `anchor.all_of` is checked against `document`. `expected_evidence_contains` and `expected_evidence_source` are checked against the target, because the model quotes its evidence from the text it verified the claim against. A probe with `"document": "source_b.md"` therefore carries evidence that must be found in `merged.md`.

### The anchoring window

The `anchor.all_of` substrings must all be found in lines `line - 2` to `line + 2` of `document`. The window stops at the first and last line of the document, and its lines are joined before the search, so a substring may run across a line break. When a document is edited and a statement moves, the probe fails here and does not quietly point at nearby text. The decompose harness uses the same radius for the line of an extracted claim.

### `anchor.all_of` and `match.all_of`

They are two fields because they are compared with two different texts. `anchor.all_of` is compared with the document's own wording, to prove the probe still points at its line. `match.all_of` is compared with a claim a model extracted, to decide which claim answers this probe.

On about two thirds of the probes the two lists are the same. They differ where a claim cannot be expected to repeat the document's wording: the anchor then quotes the document, and the match keeps only the words every correct claim must contain. `paraphrase/b-retry-limit` anchors on the list item `Retry attempts per request` and matches on `request` and `3`, because a claim extracted from that line reads "A request is retried at most 3 times" and shares no other wording with it.

**Do not narrow `match.all_of` to the claims one model happened to produce.** Widening `anchor.all_of` to the document's exact wording is safe, because it is checked against a file in the repository. Narrowing `match.all_of` until one model's claims are the ones that match fits the answer key to that model.

### Evidence expectations

Every verdict the tool returns has five fields in a fixed order: `claim_id`, `verdict`, `evidence`, `evidence_source`, `rationale`. `evidence` is a span quoted from the target and `evidence_source` is the file it was quoted from. Every verdict except `MISSING` must carry both. `MISSING` asserts an absence and must leave both empty. Two optional probe fields make assertions about them.

- **`expected_evidence_contains`** lists substrings the quoted evidence must all contain. On a `SUPPORTED` probe it is a spot check that the model read the right sentence.
- **On a `CONTRADICTED` probe, a span must not occur in the probe's own `text`.** The validator enforces this. A model can answer `CONTRADICTED` and quote the claim's own value back, which proves nothing. Only the other document's value shows that the conflict was found: `contradiction/a-connect-timeout` claims 30 seconds and expects `["60"]`.
- **`expected_evidence_source`** is a list because a fact stated in both sources has no single correct citation. In `dedup`, the listen port expects `["source_a.md", "source_b.md"]`, and the read timeout, which only one source states, expects `["source_a.md"]`.
- **When a probe declares both,** every span must occur in at least one named file and in no target file outside the list. A fixture that says a fact comes from one file, when the phrase that proves it is in both, is rejected.
- **An empty list asserts nothing,** exactly as leaving the field out does, and it needs a `notes_evidence` that says the silence is deliberate. `attribution_invented/m-tls-attributed` is the one probe that does this: its two acceptable verdicts owe different evidence.
- **A `MISSING` answer is not graded on evidence.** It owes no span and no file, and its verdict is already scored.

The tool also looks up every returned span in the file the model named and files one of four grounding outcomes. The verify harness reports them apart from `expected_evidence_source`: grounding asks whether the span is in the named file, and `expected_evidence_source` asks whether that was a correct file to name.

| grounding outcome | meaning |
|---|---|
| `grounded` | the span is in the file the model named |
| `transcription_error` | the span is in none of the target files: invented, or paraphrased while claiming to quote |
| `attribution_error` | the span is real, and it is in a target file other than the one named |
| `not_graded` | the verdict is `MISSING`, so there is no span to look for |

### `must_not_extract` entry

`must_extract` says a claim has to be extracted. A `must_not_extract` entry says a claim must not be: it catches a decompose step that produces a claim its document never made. An entry applies to the whole document and has no line.

| field | type | required | allowed values | meaning |
|---|---|---|---|---|
| `assertion_id` | string | yes | kebab-case, unique in the fixture, and not an id used in `GLOBAL.json` | The assertion's name. |
| `document` | string | yes | `source_a.md`, `source_b.md`, `merged.md` | The document whose extracted claims the pattern applies to. |
| `basis` | string | yes | `absent`, `not_a_claim` | Why a matching claim is wrong. `absent`: the text is not in the document, so a matching claim is invented. `not_a_claim`: the text is in the document and is not a statement about its subject, such as a provenance note. |
| `pattern` | string | yes | a Python regular expression | Searched in each extracted claim with `re.search`. Write case-insensitivity into the pattern with `(?i)`. |
| `reason` | string | yes | not empty | Why a matching claim would be wrong, in a reviewer's words. |

An entry from `disjoint_sources/expected.json`:

```json
{
  "assertion_id": "no-princess-to-forest",
  "document": "merged.md",
  "basis": "absent",
  "pattern": "(?i)\\bprincess\\b[^.]*\\b(old lady|forest|witch|herbs?|villagers?|medicine)\\b",
  "reason": "the two sources share no content; a claim linking the princess to the forest story is invented, not merged"
}
```

The validator cannot know what a model will extract. It checks that the entry does not ask for the impossible:

- **The pattern must not match a `must_extract` probe's `text` on the same document.** Otherwise the fixture requires and forbids the same claim.
- **With `basis: "absent"`, the pattern must not match the document's own text.** If it did, a faithful extraction would produce a matching claim and the fixture would punish correct behaviour.
- **With `basis: "not_a_claim"`, the pattern must match the document's own text.** If it matched nothing, there would be no text for a model to turn into a claim by mistake, and the entry could never fire.

`document` is declared and never assumed to be `merged.md`: `dropped_claim` forbids a JSON Lines claim from `merged.md`, where that fact is the planted omission, and requires one from `source_b.md`, where the fact is stated.

### `expected_conflicts` entry

An entry records that two or more probes state incompatible values for one attribute, which a person has to decide between.

| field | type | required | allowed values | meaning |
|---|---|---|---|---|
| `conflict_id` | string | yes | kebab-case, unique in the fixture | The conflict's name. |
| `attribute` | string | yes | not empty; snake_case by convention | The attribute the probes disagree about, such as `read_timeout`. |
| `probes` | list of strings | yes | at least two `probe_id` values from this fixture | The probes that disagree. |
| `reason` | string | yes | any | Why the statements are incompatible. |
| `human_decision_required` | boolean | yes | `true` in every fixture | The tool never picks a winner. |
| `note` | string | no | any | Context for a reader. |

**Nothing grades this list today.** The validator checks its shape, no harness reads it, and it does not enter the exit code. The tool finds a conflict through a verdict: one side comes back `CONTRADICTED`. A check that compares the two values directly does not exist. `numeric_drift` shows the gap: if a model reads 512 as consistent with "approximately 500", both probes come back `SUPPORTED`, and only a comparison of the values under their shared `attribute` could still see the disagreement. The entries are kept so that such a check has an answer key when it is built.

### `GLOBAL.json`

`tests/fixtures/GLOBAL.json` holds `must_not_extract` entries that apply to every document of every fixture. It is for claims no fixture document could ever produce, where an entry in one fixture would leave the others unguarded. Today it forbids the worked examples of `prompts/decompose.md` and `prompts/merge.md`: a model that returns the prompt's own illustration, and not a claim from the document, matches one of the three entries.

| field | type | required | allowed values | meaning |
|---|---|---|---|---|
| `schema_version` | integer | yes | `4` | The same version as the fixtures. |
| `description` | string | yes | not empty | What the file is for. |
| `must_not_extract` | list | yes | not empty | Entries with `assertion_id`, `basis`, `pattern` and `reason`, as in a fixture. There is no `document`. |

Two rules differ from a fixture's own entries:

- **`basis` must be `absent`.** `not_a_claim` says the text is present in one particular document, which no statement about all documents can say.
- **Each pattern is checked against all three documents of every fixture.** A phrase that turns up as real text in a later fixture fails the validator at once, and does not later turn that fixture's correct extraction into a violation.

### A complete example

This is `attribution_swapped/expected.json`, the shortest in the directory, with its lists written on one line and its three optional `note` texts left out. Its documents come first, because the line numbers refer to them.

`source_a.md`:

```
# Vandrell Relay - Operator Guide

The relay listens on port 8443.
The read timeout is 30 seconds.
The health check path is /healthz.
```

`source_b.md` is the same with the title `# Vandrell Relay - Deployment Notes` and a read timeout of 60 seconds. `merged.md`:

```
# Vandrell Relay - Merged Configuration

The relay listens on port 8443.
The health check path is /healthz.

Unresolved: read timeout.
According to the Deployment Notes, the read timeout is 30 seconds.
According to the Operator Guide, the read timeout is 60 seconds.
```

```json
{
  "schema_version": 4,
  "fixture": "attribution_swapped",
  "kind": "defect",
  "held_out": true,
  "description": "Both sources state a read timeout and they disagree. merged.md surfaces both values instead of picking a winner, which is the rewarded behaviour, but attaches each value to the wrong source document: the Deployment Notes are credited with source_a.md's 30 seconds and the Operator Guide with source_b.md's 60 seconds. Every value survives, so the forward probes are clean and the defect is only reachable from merged.md.",
  "plants": ["attribution swapped between the two named sources"],
  "merged": "merged.md",
  "prompts": {
    "source_to_merged": "prompts/verify.md",
    "merged_to_sources": "prompts/verify_reverse.md"
  },
  "claim_count_band": {
    "source_a.md": [3, 5],
    "source_b.md": [3, 5],
    "merged.md": [4, 7]
  },
  "probes": [
    {
      "probe_id": "a-read-timeout",
      "direction": "source_to_merged",
      "document": "source_a.md",
      "line": 4,
      "text": "The read timeout is 30 seconds.",
      "must_extract": true,
      "anchor": { "all_of": ["read timeout is 30 seconds"] },
      "match": { "all_of": ["read timeout is 30 seconds"] },
      "expected_verdict": "SUPPORTED",
      "also_acceptable": [],
      "expected_finding": "none",
      "expected_evidence_contains": ["30 seconds"]
    },
    {
      "probe_id": "b-read-timeout",
      "direction": "source_to_merged",
      "document": "source_b.md",
      "line": 4,
      "text": "The read timeout is 60 seconds.",
      "must_extract": true,
      "anchor": { "all_of": ["read timeout is 60 seconds"] },
      "match": { "all_of": ["read timeout is 60 seconds"] },
      "expected_verdict": "SUPPORTED",
      "also_acceptable": [],
      "expected_finding": "none",
      "expected_evidence_contains": ["60 seconds"]
    },
    {
      "probe_id": "m-notes-timeout-attribution",
      "direction": "merged_to_sources",
      "document": "merged.md",
      "line": 7,
      "text": "The Deployment Notes state the read timeout is 30 seconds.",
      "must_extract": false,
      "anchor": { "all_of": ["According to the Deployment Notes", "read timeout is 30 seconds"] },
      "match": { "all_of": ["Deployment Notes", "read timeout is 30 seconds"] },
      "expected_verdict": "CONTRADICTED",
      "also_acceptable": [],
      "expected_finding": "contradicted",
      "expected_evidence_contains": ["60"],
      "expected_evidence_source": ["source_b.md"]
    },
    {
      "probe_id": "m-guide-timeout-attribution",
      "direction": "merged_to_sources",
      "document": "merged.md",
      "line": 8,
      "text": "The Operator Guide states the read timeout is 60 seconds.",
      "must_extract": false,
      "anchor": { "all_of": ["According to the Operator Guide", "read timeout is 60 seconds"] },
      "match": { "all_of": ["Operator Guide", "read timeout is 60 seconds"] },
      "expected_verdict": "CONTRADICTED",
      "also_acceptable": [],
      "expected_finding": "contradicted",
      "expected_evidence_contains": ["30"],
      "expected_evidence_source": ["source_a.md"]
    }
  ],
  "must_not_extract": [],
  "expected_conflicts": [
    {
      "conflict_id": "read-timeout",
      "attribute": "read_timeout",
      "probes": ["a-read-timeout", "b-read-timeout"],
      "reason": "source_a.md states 30 seconds and source_b.md states 60 seconds for the same attribute",
      "human_decision_required": true
    }
  ],
  "expected_exit_code": {
    "strict": 1,
    "lenient": 1
  }
}
```

How to read it:

- **The two forward probes are `SUPPORTED`** because both timeouts survive into `merged.md`. They are the controls: they show the values were kept, so the defect is the attribution alone.
- **The two reverse probes are `CONTRADICTED`.** Line 7 of `merged.md` credits 30 seconds to the Deployment Notes, and `source_b.md`, which is the Deployment Notes, states 60.
- **Each `CONTRADICTED` probe expects the other value as evidence.** The first claims 30 and expects a span containing `60`, quoted from `source_b.md`. `60` does not occur in the probe's own text, as the rule requires.
- **`kind` and the exit code follow from the probes.** Two probes file a `contradicted` finding and neither accepts another verdict, so both exit codes are 1 and the fixture is a `defect`.

## Vocabulary

These are the values a verdict and a finding can take, and the two ways of scoring them. The other closed sets (`kind`, `direction`, `document` and `basis`) are listed with their values in the field reference above.

### Verdicts

A fixture may declare three verdicts, in `expected_verdict` and `also_acceptable`.

| verdict | meaning |
|---|---|
| `SUPPORTED` | the target states the claim, in the same words or in different words with the same meaning |
| `CONTRADICTED` | the target states something incompatible with the claim |
| `MISSING` | the target neither states nor contradicts the claim |

The tool itself can return two more. `PARTIAL` means the target states part of the claim and does not contradict the rest. `DERIVED` exists only at the fidelity levels `high`, `open` and `sourced`, and marks a merge claim that no single source states and that several source statements carry together. No fixture expects either one, and the validator rejects both in a fixture. A probe that needs one of them needs a new schema version, with the tables below widened to match.

### Deriving `expected_finding`

`expected_finding` follows from `expected_verdict` and `direction`. The validator enforces this table, so a hand-edited fixture that declares `MISSING` with `contradicted` is rejected.

| `expected_verdict` | `direction` | `expected_finding` | what went wrong |
|---|---|---|---|
| `SUPPORTED` | either | `none` | nothing |
| `CONTRADICTED` | either | `contradicted` | the merge states a different value |
| `MISSING` | `source_to_merged` | `dropped` | a fact in a source did not reach the merge |
| `MISSING` | `merged_to_sources` | `hallucinated` | the merge states a fact that no source states |

**`MISSING` means two different things.** In the forward direction the merge lost a fact. In the reverse direction the merge invented one. It is the same label for opposite failures, filed in different sections of the report, and that is why `direction` is required on every probe and has no default.

The tool files two more findings, for the `PARTIAL` verdict that no fixture declares: `partially_dropped` in the forward direction and `partially_invented` in the reverse.

**The finding follows the verdict that came back, not the one that was declared.** `numeric_drift/a-max-connections` declares `CONTRADICTED` and also accepts `SUPPORTED`. A run in which `SUPPORTED` comes back files `none` for that probe, and that is correct.

### `strict` and `lenient`

These are two ways of scoring the same answers. Under strict scoring a probe is right when the returned verdict is `expected_verdict`. Under lenient scoring it is also right when the verdict is one of `also_acceptable`. Neither mode makes the tool report more or less.

The modes differ only on a probe whose `also_acceptable` is not empty. Two probes have one:

| probe | declared | also accepts | why |
|---|---|---|---|
| `numeric_drift/a-max-connections` | `CONTRADICTED` | `SUPPORTED`, `MISSING` | 512 can be read as consistent with "approximately 500", as a different number for the same attribute, or as a figure the vague claim neither states nor denies. |
| `attribution_invented/m-tls-attributed` | `MISSING` | `CONTRADICTED` | No source makes the attributed statement, so it is missing. The sources do state the fact without that attribution, so the merge can also be read as contradicting them. |

**When to use `also_acceptable`.** Add a verdict only when it is a defensible reading of the documents themselves. A model returning it is not a reason. Keep `expected_verdict` on the reading the fixture was written for, so that the strict score still shows the difference. Do not write a second probe that accepts all three verdicts: it cannot fail, so it measures nothing, and `numeric_drift` already marks that boundary.

### What a fixture cannot declare

An answer key speaks about claims only. The findings the mechanical checks make on a merge the tool produced, such as `verbatim_violation` or `duplicated_content`, have no field here, and neither have the exit codes 2 and 3. [Reading the report](../../docs/report.md#structure) lists those findings under the headings the report prints, such as "Verbatim violation" and "Stated twice".

Two mechanical checks do run on `llossless verify`, and so on every fixture: one reports a statement credited to a source that does not carry it ([Attributions](../../docs/report.md#attributions)), and one reports a source number that the merge writes so that it reads as a different value, such as "17,560" written "17.560" ([Number format](../../docs/report.md#number-format)). Neither has a field here and either can move the exit code, so a fixture's documents must not trip one unless that is the planted defect.

## Which pass checks which assertion

A fixture carries assertions for different tests. Each test reads only its own fields, so an unmet assertion in one test is not a failure of another.

| assertion | checked by | how |
|---|---|---|
| every field's shape, and that the answer key agrees with itself and with its documents | `tests/test_fixtures.py` | offline, no model |
| `must_extract` with `match.all_of` and `line` | `tests/run_decompose.py` | some extracted claim contains every `match.all_of` substring and sits within 2 lines of `line` |
| `claim_count_band` | `tests/run_decompose.py` | the number of extracted claims is inside the band |
| `must_not_extract`, and `GLOBAL.json` | `tests/run_decompose.py` | no extracted claim's text or quoted span matches the pattern |
| `expected_verdict`, `also_acceptable` | `tests/run_verify.py` | the probe's `text` is verified as a claim and the verdict is scored strict and lenient |
| `expected_evidence_contains`, `expected_evidence_source` | `tests/run_verify.py` | against the evidence and the file name the model returned |
| `expected_exit_code`, `expected_finding`, `anchor.all_of` | `tests/run_detect.py` | runs `llossless verify` on the fixture and compares its real exit code and its findings |
| the `text` of every forward probe; `must_not_extract` entries on `merged.md` that transfer; `GLOBAL.json` | `tests/run_merge.py` | on a merge the model generates: every forward probe must come back `SUPPORTED`, and no claim extracted from the merge may match a pattern; see [the transfer rule](#which-mergedmd-assertions-transfer-to-a-generated-merge) |
| `expected_conflicts` | nothing | shape only |

**The decompose and verify harnesses run every call three times by default and report the answer most runs gave.** `must_not_extract` is the exception: an assertion counts as violated if any run violated it, and the report says how many did. A claim the document never made is a defect the first time it appears.

**The verify harness does not use the decompose step.** It sends the answer key's probe texts as claims, so that a claim the decompose step failed to extract is not scored as a verify failure.

**The detection harness finds a probe's finding by its anchor.** A probe whose `expected_finding` is not `none` counts as detected when some finding in the report contains every `anchor.all_of` substring in its claim, its quoted span, its evidence or its rationale. A finding that no such probe accounts for counts as invented. Choose anchor substrings that the defect's own sentence contains and its neighbours do not.

**The merge harness never opens a fixture's `merged.md`.** It has the model merge the two sources and grades that merge. `expected_verdict`, `also_acceptable` and `expected_evidence_contains` describe the fixture's own `merged.md`, so it ignores all three and holds every forward probe to one rule: the verdict must be `SUPPORTED`. That is why `dropped_claim` fails under the verify harness and passes under the merge harness on the same probe. The first scores a merge with a planted omission, and the second scores a merge that has to carry the fact.

### Deriving the exit code

`expected_exit_code` is not chosen. The validator computes both values from the probes and rejects a fixture that declares anything else.

- **`strict` is 1** if any probe's `expected_verdict` files a finding, which means it is not `SUPPORTED`. Otherwise it is 0.
- **`lenient` is 0** if every probe has `SUPPORTED` as its `expected_verdict` or among its `also_acceptable`. Otherwise it is 1.
- **`kind` must agree:** a `defect` has `strict` 1 and a `guard` has `strict` 0.
- **`expected_conflicts` plays no part.** A listed conflict does not make the exit code 1.

`lenient` is never stricter than `strict`. The two differ only where an accepted verdict files nothing while the declared one files a finding, which today is `numeric_drift` alone.

**How the detection harness reads the two values.** It compares the real exit code of `llossless verify` with `strict`.

| outcome | when |
|---|---|
| `matched` | the exit code equals `strict` |
| `unmeasured` | `strict` and `lenient` differ, the run exited with `lenient`, it invented no finding, and every planted probe got a verdict the fixture accepts. The model took a reading the fixture itself allows, so the run is neither a pass nor a miss. |
| `missed` | any other exit code of 0 or 1 |
| `errored` | the run exited 2 or wrote no report. It is left out of the figures and run again. |

**Exit 2 is never an expectation.** `llossless verify` exits 2 when it could not finish: a claim got no usable answer, a source yielded no claims, or none of the quoted evidence could be found in the files it was said to come from. Such a run says nothing about the fixture, so no fixture may declare 2 and no figure counts it. The exit code 3, for a merge whose own records are wrong, cannot occur on `verify`. All four codes are in the [command-line reference](../../docs/reference.md#exit-codes).

### Which `merged.md` assertions transfer to a generated merge

A `must_not_extract` entry on `merged.md` describes the fixture's own merge. The merge harness grades a generated merge instead, so it applies an entry only when the entry is true of any correct merge. The rule is computed by `transferable` in `tests/run_merge.py`, not kept as a list:

> A `merged.md` entry with `basis: "absent"` transfers if and only if its pattern matches neither source.

- **If the pattern matches a source,** a correct merge must carry that text, and the entry would punish it. `dropped_claim/no-restored-log-format` forbids a JSON Lines claim because the fixture's own merge omits the log format. A generated merge is required to keep it, so the entry does not transfer.
- **If the pattern matches neither source,** the text is absent from everything the model was shown, and a claim of it is invented in any merge.
- **`basis: "not_a_claim"` never transfers.** It is a statement about text in one particular document. All three such entries are in `structure_added`.

Today the rule transfers nine of the ten `absent` entries on `merged.md`: two each in `disjoint_sources` and `disjoint_domains`, four in `list_structure` and one in `ordering_only`. `GLOBAL.json` applies to every generated merge.

## Notation is not information

A merge may change how a fact is worded. It may not change what the fact says. Every answer key in this directory is drawn on that line, and two different parts of the tool check its two halves.

**Wording is not information: the claim checks are silent about it.** The verify step asks whether the other side states the claim, in the same words or in different words with the same meaning. If it does, the verdict is `SUPPORTED` and nothing is filed: not a finding, not a warning, not a note. A reworded sentence, a reordered section and a list turned into prose are all wording. These checks have no rule about notation either: they judge meaning, and the verify prompt's rule is that different wording with the same meaning is `SUPPORTED`. `paraphrase` and `ordering_only` fail a run that reports a rewording. The silence matters: a report that lists harmless rewordings teaches its reader to skim, and the next finding skimmed is a real one.

**A change in what is known is information, however small the edit.** In `numeric_drift` one source says "approximately 500 concurrent connections" and the merge says 512. That is not rounding: a reader who needs the exact figure is now reading a number that source never committed to.

**Exact values are not wording: the mechanical checks compare them character by character.** This applies to a merge the tool made with `llossless merge`. Where a source sentence is kept, these parts of it must arrive unchanged, at every fidelity level and even if the merge declared the sentence reworded: numbers written in digits, including times and percentages, URLs, paths, version strings, inline code, link targets and fenced code blocks. A number rewritten in another notation is therefore a finding. "512" written as "0x200" is a `verbatim_violation`, and so is "30 seconds" written as "30s", or "02:00 till 15:30" written as "2 am till 3:30 pm". The check compares strings and does not ask whether two notations mean the same number, because a model that may change a format will sooner or later change a value, and the output does not show which it did.

**In a fixture, write every value the same way in all three documents.** `llossless verify`, which grades the fixtures' own merges, has no merge records and does not run the mechanical comparison, so an answer key speaks about claims only. A value written in another notation would be judged there by meaning alone, and no fixture tests how a model judges it, while the same change is a finding in a merge the tool made. So a change of notation must not stand in for a harmless paraphrase. `paraphrase` keeps every value identical for this reason.

## Special fixtures

Six fixtures do a job that a well-meant edit can destroy. Each entry says what the fixture is and what not to do to it.

### `disjoint_sources`

Two short fairy tales, one about a princess and her rose garden and one about an old woman in a forest, with no fact in common. Its `merged.md` is byte for byte `source_a.md`, a newline, then `source_b.md`, and that is the correct merge: there is nothing to combine. It guards against a tool that treats every concatenation as a lazy merge, and its two `must_not_extract` entries forbid any claim that links the stories.

- **Do not give the two stories a shared fact.** That they share nothing is what makes a linking claim an invention and the concatenation correct.
- **Do not change `merged.md`.** `tests/analyse_merges.py` compares it with the joined sources to decide whether a concatenated merge of this fixture is a defect, and `tests/test_reconcile.py` expects the tool's measurement of "one source after the other, in two blocks" to fire on the two disjoint fixtures and on no other.
- **Do not split its long sentences into one fact per line.** The Vandrell Relay documents state one fact per line, so on them copying each line and extracting each claim give the same output. Compound narrative sentences are where the two differ.
- **Do not tidy its odd values or its near-matches.** "From 02:00 till 15:30" is bait: a model that rewrites the time fails the probe that requires the span as written. The stories also share surface words (work, seasons, transport) that tempt a model to connect them.

### `disjoint_domains`

The same test on a second subject: a fire door inspection round at a depot, and a lunchtime chess club. It matches `disjoint_sources` in line count, word count, number of segments and sequence of segment kinds, and its probes have the same shape, so a measurement that scores the two differently is reading the subject and not the form.

- **Keep the two fixtures the same shape.** An edit to one that changes a line count or a sentence structure ends the comparison.
- **Do not reword either source to make a failure go away.** The awkward parts are deliberate: a 24-hour time range that a model tends to rewrite, and attributes that look alike across the two unrelated documents (rounds and ladders, a seasonal closure, a weekly rhythm, the word "board"). They are what a model misquotes or wrongly connects. Smooth them out, or drop the fixture, and the grounding and invention figures improve because nothing is testing them any more. The loss shows up as an improvement.

### `concatenated` is a guard that records a blind spot

Two accounts of one village bell tower, a parish record and a recollection, state the same five facts in different words. `merged.md` alternates them paragraph by paragraph and keeps both versions of every fact. That is a bad merge: the reader gets everything twice. All fifteen probes are still `SUPPORTED`, and correctly: every source claim is carried and every merge claim has a source. The claim checks do not ask how often the merge says a thing. The mechanical checks of a `merge` run do not catch this document either: the sources alternate, so it is not two blocks, and the two wordings of each fact are too far apart to count as a repeat.

- **`kind` is `guard` because the probes imply exit 0,** not because the merge is correct. The validator rejects `defect` here.
- **Do not plant a claim-level defect to make it a `defect`.** The fixture would then vary two things, and the redundancy could no longer be measured on its own.
- **Do not move the two wordings closer together.** If a later check catches this document as it stands, that is a result to report, and the format then needs a field to expect it in. Editing the text until today's checks fire removes the only document with this shape that was written for the purpose.

It is outside the fact pool because a pool document cannot hold two wordings of one fact: restating "The read timeout is 30 seconds." gives the same sentence back.

### `restated` is real model output, and the corpus's only one

A general-knowledge pair about Christianity, the same two documents as `tests/handwritten/christianity/`. Its `merged.md` is, unedited, what `llossless merge --fidelity low` returned for them on 2026-09-15 with the model `qwen3.8:27b`. That run exited 0 with no finding, and the merge states every fact twice. The fifth file, `recorded-claims.json`, holds the claims that run extracted from the three documents and a `recorded_by` block describing the run. Neither file is an answer key. `expected.json` still is.

The fixture exists because a check for repeated claims needs claims a model really produced, and `concatenated` does not supply them: its two wordings of a fact do not come back as the same claim. `tests/test_reconcile.py` reads `recorded-claims.json` and requires the repeat check to find 23 repeated claim texts in the merge and none in either source. That check runs on `merge` only, so `verify`, which grades this fixture, still finds nothing, and the fixture is a `guard` for the same reason as `concatenated`.

- **Never edit `merged.md` or `recorded-claims.json`.** They record one run. An edited copy no longer shows that the check fires on real output.
- **Do not add other merges from a run of the tool to `tests/fixtures/`.** An answer key is independent of the tool only while the tool did not produce the documents it grades. This one exception exists because its evidence had to come from a real run and could not be written for the purpose.

### `conflict_surfaced`

It has the same two sources as `contradiction`, byte for byte, and differs only in `merged.md`: the disagreement is shown, with both values attributed, and not settled. All eleven probes are `SUPPORTED` and the exit code is 0, because showing a conflict is what the tool rewards. Without this fixture, a tool that answers `CONTRADICTED` for one side of any disagreement would pass `contradiction` and fail every merge that got it right.

- **Edit the sources of both fixtures together or not at all.** The validator fails `conflict_surfaced` when its sources differ from `contradiction`'s.
- **If it fails, read the prompt before blaming the model.** It passes only because `prompts/verify.md` says that an attributed statement still counts as stated, and that several attributed values for one attribute are each `SUPPORTED`.
- **Keep its reverse probes.** Two of the three sit on attributed sentences ("According to the Operator Guide, ..."), where a reverse check most easily reports correct content as invented.

### `numeric_drift`

The only fixture whose two exit codes differ, 1 strict and 0 lenient, because its planted probe accepts all three verdicts (see [`strict` and `lenient`](#strict-and-lenient)). When a model answers `SUPPORTED` there, `llossless verify` exits 0 and the detection harness records the fixture as `unmeasured`, not as a miss.

- **Do not narrow `also_acceptable` to make the fixture decisive.** Whether 512 contradicts "approximately 500" is a real disagreement between careful readers, and the answer key says so.
- **Do not set `lenient` to 1.** The validator derives it from the probes and rejects the mismatch.

## Validation

```
python3 tests/test_fixtures.py
```

It reads the files in `tests/fixtures/` and nothing else. It needs no network, no model and no third-party package, and it exits 0 when everything is valid and 1 otherwise.

**What it checks:**

- every fixture has its four files, and `expected.json` parses;
- every required field is present, has the right type and holds an allowed value, as the tables above list them;
- each probe's `line` exists, its `anchor.all_of` substrings are in the anchoring window, and its `match.all_of` substrings are in its own `text`;
- `expected_finding`, `expected_exit_code` and `kind` agree with what the probes imply;
- evidence spans occur in the target, a span on a `CONTRADICTED` probe does not occur in the probe's own text, and spans agree with the files `expected_evidence_source` names;
- every `must_not_extract` entry, the fixture's own and the global ones, can be satisfied by a correct extraction;
- `conflict_surfaced` has the same sources as `contradiction`;
- none of the thirteen fixtures in the registered detection block has been removed.

**What it does not check.** It does not judge whether an expected verdict is right, it does not compare a probe's `text` with the document beyond the substrings, and it never calls a model. Whether a model agrees with the answer key is what the harnesses measure.

**What the output looks like.** One line per check, `ok` or `FAIL`, and under a failing fixture one line per problem:

```
  attribution_swapped ............. FAIL
      - expected_exit_code[strict] is 0 but this fixture's own probes imply 1. The probes win: an answer key that disagrees with itself scores the arm on the disagreement.
  ...

  18/19 fixtures valid, 1 failing
```

The total is three more than the number of fixtures. The first three lines are not fixtures: `GLOBAL.json`, a self-test of the exit code derivation, and a check that the registered detection block names only fixtures that exist. `python3 tests/run_merge.py --dry-run` counts the two apart and prints `16 fixtures (+1 GLOBAL)`.
