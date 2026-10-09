# Benchmark specification

*The frozen rules a benchmark run is scored under, for readers who want to check a result against its registration. [The benchmark](benchmark.md) is the plain-language overview.*

> **Status: a historical specification, frozen on 2026-08-30 (this note was added on 2026-10-05).**
>
> - **What this is.** The rule set, version 1.0.0, that the project's study of open-weight models was scored under: three models, `qwen3.8:27b`, `deepseek-r1:70b` and `gpt-oss:120b`, in August and September 2026. The raw outputs of those runs are in `arms/2026-08-30/` and `arms/2026-09-03/`. It is kept because those results were scored against it, and because `tests/run_bench.py` still reads the registry in section 8.
> - **What it is not.** It is not the rule set of the release benchmark of 2026-09-27, the one behind the README's results table. That benchmark has its own registration, [`arms/2026-09-27/lineup/REGISTRATION.md`](../arms/2026-09-27/lineup/REGISTRATION.md), and its rules are described in [The benchmark](benchmark.md).
> - **Some values are the values of 2026-08-30.** The declared-loss budget is 0.05 here; the tool's default today is 0.03, and `tests/run_bench.py` scores with the tool's default. Section 2 says 13 fixtures carry an `expected.json`; today all 16 do, and the 13 that are scored are listed in `tests/run_detect.py`. Section 2 gives `conflict_surfaced` an expected exit code of 1; its answer key today says 0. The version number fixes the list of properties in section 8, not the code that computes them, which has changed since.
> - **Words used below.** An *arm* is one model configuration under test, and a *draw* is one run of it. The *candidate* is the model that writes the merge, and the *judge* is the model that splits documents into claims and grades them. A *pod* is a rented GPU server. "The paper" in sections 1 and 2 is the project's write-up. Its sources and its graded records are in `paper/`.

**Version 1.0.0, frozen 2026-08-30.** Nothing below is amended in place. Changes go in section 9 as a dated entry, and a run states the version it was scored under.

This file is the registration. It is also machine-readable: section 8 is a registry that `tests/run_bench.py` parses, and the runner refuses to score anything if the set of properties it computed is not the set registered here. That refusal is the point of writing the spec as a file rather than as a habit. A summariser's PASS column is not a registration - it can report a green over a subset of what was registered, and did, on 2026-08-27.

## 0. What is being measured, and what is not

Two tasks over one tool.

**Detect** is a gate. Given a document with a planted defect and an answer key describing the plant, does the installed CLI find it and exit accordingly? An arm either clears the gate or is rejected; there is no partial credit and no ranking within a pass.

**Merge** is descriptive. Given two source documents, the tool produces a merge; the merge is then held to what it declared. There is no answer key - a generated merge has none - so nothing here is graded against an ideal text. It is graded against the sources it came from.

Not measured: whether a merge reads well, whether a summary is faithful in the sense a summarisation benchmark means, or whether the tool is useful. Those are questions this instrument cannot answer and section 7 says so again.

## 1. Judge-free and judge-dependent

Every metric below is marked **judge-free** or **judge-dependent**.

A judge-free metric is computed by `src/llossless/reconcile.py` and `src/llossless/segment.py` from text alone: segmentation, span location, and the disposition records the merge itself declared. No model is called, the same input gives the same output on any machine, and a disagreement about the number is a disagreement about the code.

A judge-dependent metric needs the decompose and verify roles, which are model calls. Its value moves with the judge, and comparing two candidates scored by different judges compares three things.

**The paper's primary numbers are judge-free metrics only** - the detection gate and the deterministic structural and honesty metrics. Claim-level coverage is reported as secondary, always with the judge named, and never as the basis of a ranking without a judge-sensitivity note: the same corpus scored 225 and then 212 a day apart on the same configuration, and that variation is the corpus's, not the candidate's.

**A candidate is never its own judge.** The runner refuses. A model that scores its own merge is measuring its agreement with itself, and the failure is silent: the numbers look like the others.

## 2. Task 1 - detect

Corpus: `tests/fixtures/`, 16 fixture directories, 13 of which carry an `expected.json` graded by this task. The instrument is `llossless verify` run as a subprocess, so the graded exit status is what a shell saw.

Per fixture, exactly as `tests/run_detect.py` computes it:

| Metric | Formula | Kind |
| --- | --- | --- |
| detection rate | `plants_detected / plants_total`, where a probe with a non-`none` expected finding is detected when some entry in the report's `findings` carries every token of that probe's anchor in the claim text, the span or the evidence | judge-dependent |
| false-finding rate | `invented_total / findings_total`, where an invented finding is one no probe accounts for. The count is reported alongside the rate, because the denominator is small | judge-dependent |
| exit-code agreement | `exit_code_matched / fixtures`, against `expected_exit_code.strict`, from the process's real exit status | judge-dependent |

All three are judge-dependent: detection runs the verify role. They are still the gate, because a gate has to be about what the tool does, and what the tool does involves a model. What they are not is a *primary paper number* - a ranking built on them carries the judge in it, and section 1 says so.

**The two disqualifiers.** An arm is rejected outright if either of the following happens on any fixture:

- a seeded-defect fixture (`dropped_claim`, `contradiction`, `hallucination`, `numeric_drift`, `attribution_invented`, `attribution_swapped`) exits 0;
- a fixture whose `expected_exit_code.strict` is 0 (`dedup`, `disjoint_domains`, `disjoint_sources`, `ordering_only`, `paraphrase`, `structure_added`) exits non-zero carrying an invented finding.

`conflict_surfaced` is a guard whose `expected_exit_code.strict` is 1 and is graded on matching that, not on exiting clean.

A model that misses a planted defect, or plants one of its own, is not a model for LLossless. Being the larger model earns nothing here.

## 3. Task 2 - merge

Corpus: the pairs named by the run's configuration, at the fidelity levels it names. The tool produces the merge; the reconciler holds it to what it declared.

| Metric | Formula | Kind |
| --- | --- | --- |
| undeclared absence per segment | `undeclared_absence findings / source segments`. The denominator is source segments, never claims | judge-free |
| declared-loss honesty | `declared drops / (declared drops + undeclared_absence findings)`. Reported `n/a` when the denominator is 0 - a merge that lost nothing is not honest, it is complete | judge-free |
| invention | `invented_segment findings / merged segments` | judge-free |
| structural findings | the reconciler's findings, **counted by kind and never summed into one number**. A merge with one over-budget declared loss and a merge with eighteen undeclared absences do not have comparable totals | judge-free |
| declared loss over budget | whether `declared drops / source segments > 0.05`, strictly greater | judge-free |
| forward coverage | source claims returning SUPPORTED against the merge | judge-dependent |
| invented claims | claims from the merge supported by neither source | judge-dependent |

Honesty is the metric this benchmark exists for, and it is the one that separates two failures a byte count cannot. A merge that drops a section and says so is over budget and legible. A merge that drops it silently is clean by every length-based measure. The 2026-08-28 session recorded one arm dropping 18 of 24 segments with 0 declared.

**Baselines, scored in every merge-task run.** Both are judge-free, need no model, and are computed by the runner itself:

- **byte-concatenation**: `source_a` + a blank line + `source_b`. Loses nothing, so its undeclared absence is 0 and its honesty is `n/a`; it fails on duplication and on the title checks. It is the floor that any length-based or coverage-based metric mistakes for a good merge, which is why it is scored every time rather than argued about once.
- **base-only**: `source_a` alone. Loses all of `source_b` and declares nothing, so it is the maximum undeclared absence the corpus admits.

A candidate that does not beat both on the judge-free metrics has not merged anything.

## 4. Draws, and how they are aggregated

**K = 3 by default.** K = 5 for any model where non-determinism has been observed at temperature 0. That is a property of the model, established by replaying one configuration and comparing sha256, and it is recorded per model rather than assumed. `gpt-oss:120b` is on 5: config-matched reruns across two pods gave different merges at temperature 0 with a fixed seed, so a rerun of it is a fresh sample and not a check.

**Aggregation is the median, reported with the min and the max.** Never the mean: three draws and an outlier is a mean nobody should read. Never a bare median either - a spread of 0 and a spread of 12 are different results and the median hides which one happened.

**Per stage, never one blended number.** Merge, decompose and verify are reported separately. An earlier comparison of a 4B and an 8B model found a step where verify barely moved while decompose collapsed; one aggregate would have hidden exactly the thing this measurement is for.

**A series that does not move is reported as its max and its min**, never as a correlation. A rank correlation over a constant is undefined.

## 5. Provenance

Every scored record carries: the endpoint id, the working-tree commit, the served context window read back from the endpoint, the structured-output tier actually reached, the thinking set per role read back per unit rather than trusted from the launch flags, the model for each of the three roles, the judge, the draw index, and the spec version above.

Read back, not trusted: an arm's registered configuration and the configuration its records show are two assertions, and the second is the one that happened.

The working tree is clean at launch and no commit is made until the arm closes. The provenance stamp is taken once at `Client.__init__`; a moving HEAD splits one arm into two differently-labelled halves.

## 6. PASS

PASS is not a summary judgement. It is the conjunction of the registered properties in section 8, each evaluated mechanically, and the runner asserts that the set of properties it evaluated equals the set registered. A property that did not run is not a property that passed.

Every property is stated so that its negation is observable. "The merge is good" is not a property. "No `undeclared_absence` finding fires on a member of the must-not-fire set that does not also fire for the control in the same session" is one.

**A control clause needs a same-session baseline.** Any property phrased against "the control" means the control arm run in the same session, on the same pod, against the same corpus. A figure from another day is a fourth confound.

## 7. What this specification cannot answer

- Whether a merge is good to read. Nothing here measures prose.
- Whether the corpus is representative. It is 16 fixtures and 9 pairs, one language, one document family.
- Whether a ranking generalises past this corpus and these draws.
- Whether the judge is right. It measures agreement with a judge, and section 1 is why judge-dependent numbers are not the primary ones.

## 8. The property registry

Read by `tests/run_bench.py`. Tab-separated, one property per row: id, task, kind, role, and the assertion. **The runner refuses to score if the set of properties it evaluated is not exactly this set.**

```registry
id	task	kind	role	assertion
detect.no_seeded_defect_exits_clean	detect	judge-dependent	disqualifier	No seeded-defect fixture exits 0.
detect.no_invented_finding_on_clean	detect	judge-dependent	disqualifier	No fixture whose expected_exit_code.strict is 0 exits non-zero carrying an invented finding.
detect.matches_at_least_the_control	detect	judge-dependent	gate	The arm matches expected_exit_code.strict on at least the set of fixtures the control matches in the same session.
merge.beats_concatenation_on_absence	merge	judge-free	gate	Undeclared absence per segment is no worse than the byte-concatenation baseline scored in the same run.
merge.beats_base_only_on_absence	merge	judge-free	gate	Undeclared absence per segment is strictly better than the base-only baseline scored in the same run.
merge.no_invented_segment	merge	judge-free	gate	No invented_segment finding fires on any pair.
merge.declared_loss_within_budget	merge	judge-free	descriptive	Declared drops over source segments is not strictly greater than 0.05. Over budget is a declared loss and is reported, not disqualifying.
merge.honesty_reported	merge	judge-free	descriptive	Declared-loss honesty is reported per pair, or n/a where nothing was lost.
run.candidate_is_not_the_judge	both	judge-free	gate	The candidate model is not the judge model for decompose or verify.
run.provenance_read_back	both	judge-free	gate	Every unit's recorded configuration matches the arm as registered, read back from the record.
```

## 9. Amendments

Appended and dated. No clause above is edited.

- 2026-09-27: for publication, three pointers to files that are not published (the model-support notes in section 2, and the model-matrix records in section 4 and section 10) now name those files in words instead of by path. No property, disqualifier, formula or threshold changed.
- 2026-09-30: for publication, the remaining references to unpublished records (the model-support notes in section 2, the model-matrix records and an internal milestone name in section 4, the model-matrix records in section 10) are removed or restated in words a reader of this copy can follow, and a one-line pointer to the overview is added above the version line. No property, disqualifier, formula or threshold changed.
- 2026-10-05: for publication, a status note is added above the version line. It says which runs this specification governed, where the registration of the 2026-09-27 release benchmark is, which values here have since changed in the tool (the declared-loss budget, the fixtures that carry an answer key, the expected exit code of `conflict_surfaced`), what the terms arm, draw, candidate, judge and pod mean, and that "the paper" is a write-up not included in this copy. This entry also records two earlier edits that were made in place without an entry: on 2026-09-15 the fixture count in sections 2 and 7 was updated from 14 to 16 when two fixtures were added, and on 2026-09-26 the tool's name in paths and commands followed its renaming. No property, disqualifier, formula, threshold or registry row changed.
- 2026-10-09: the paper is published with the repository from this date, so the status note now says where it is (`paper/`) instead of saying that it is not included in this copy. No property, disqualifier, formula, threshold or registry row changed.

## 10. Pre-registration template

Copied into each block's registration file, filled in **before** the session, and never edited afterwards - a correction is an amendment with a date.

```
### Block <name>, registered <date>

Question:        <the one thing this block isolates, in one sentence>
Arms:            <label: model, field-order, thinking set, K> ...
Control:         <the arm in this same session that the gate properties compare to>
Held constant:   <temperature, seed, corpus, fidelity levels, title policy, base>
Not held:        <every confound, named. An unnamed confound is a claimed control>
Corpus:          <fixtures and pairs, by name>
Baselines:       byte-concatenation, base-only
Spec version:    <the version of docs/bench-spec.md this is scored under>
Registered PASS: <the property ids from section 8 that apply, by id>
Predicted:       <what the block is expected to show, written before it runs>
Falsified by:    <the observation that would make the prediction wrong>
```

`Predicted` and `Falsified by` are not decoration. A block whose prediction cannot be falsified by an observation is a block that will be read as confirming whatever it produces.
