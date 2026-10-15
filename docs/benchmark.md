# The benchmark

Every LLossless run produces a report that says, with evidence, what a model dropped, changed or made up while merging. Most of those figures are computed from text by code, not by asking a model, so the same documents can be run through several models and the results compared on the same terms. This page explains how that comparison is set up: what is measured, what the count of silent loss means, the audit that decides which model is disqualified, how to read a result row, the rules that keep it fair, and what it cannot tell you. The results themselves are in the README, under ["Results, 2026-09-27"](../README.md#results-2026-09-27).

## The release benchmark of 2026-09-27

**When it ran, and how big it was.** The cross-vendor release benchmark ran on 2026-09-27, in one session that ended shortly after midnight UTC: 295 runs over five models, GPT-6 Sol, GPT-6 Luna, Opus 5.5, Sonnet 5 and Haiku 4.5. The two GPT models ran through the vendor's API, and the three Claude models through both the API and a Claude subscription, which makes eight result rows. Fable 5.1 ran on three documents only and is outside the main table. There were two model failures, both Haiku 4.5 (one per route).

**Where the results are.** The README has the table and the per-model notes. Everything behind them is in `arms/2026-09-27/lineup/`: [`REGISTRATION.md`](../arms/2026-09-27/lineup/REGISTRATION.md) is the registration written before the first call, [`figures.md`](../arms/2026-09-27/lineup/figures.md) holds the derived tables, [`audit/`](../arms/2026-09-27/lineup/audit/README.md) holds the audit described below, and `cells/` holds the merged document and the report of every run. [`arms/README.md`](../arms/README.md) describes the layout.

**The scoring was amended afterwards.** On 2026-10-12, after every call had been made and the results were known, the rule that counts silent loss was amended and the nine merge pairs were scored a second time from the stored runs. This page describes the amended scoring, which is the one the README shows. The scoring as registered stays published beside it. [Two scorings](#two-scorings) says what changed and why. On the same day, and also after the results, the audit that decides who is disqualified was extended to sentences it had not read at first, and a third row was disqualified. [The audit](#the-audit-and-what-disqualifies) says what was read.

**What was registered but not measured.** Gemini 3.8 Flash: during the run its free tier refused every call.

**Where earlier runs are.** [`arms/BENCHMARK-MATRIX.md`](../arms/BENCHMARK-MATRIX.md) lists every measurement made before this one, each with its settings and the reasons it is not directly comparable with its neighbours. Read that file as a record of what was measured, not as a leaderboard.

## What it measures

Three test sets, all in this repository:

| set | what runs | what it measures |
|---|---|---|
| **Merge quality** | the nine document pairs in `tests/pairs/`, merged at `--fidelity high` with full verification | *silent loss*: source sentences that a program could not find in the merge and that no record of the merge explains; *untaken headings*: source headings the merge did not take and did not record, while their sections are still there; *deviations*: sentences lost, wrongly kept or repeated when the merge is held against the reference merge written for the pair (`ideal.md`) |
| **Detection** | the 13 pre-registered fixtures in `tests/fixtures/`, each a merge written for the test with a known defect or none, checked by `llossless verify` | planted defects found; findings that no answer key accounts for; exit codes matched |
| **Planted errors** | three document sets in `tests/handwritten/`, merged at `--fidelity open`: `voyager` and `bip39` have factual errors planted in them (44 and 14), and `mahjongg` has none and is the control | errors the merge corrects from what the model knows (`voyager`, `bip39`), and true facts it "corrects" wrongly (`mahjongg`) |

`tests/fixtures/` holds sixteen fixtures. All sixteen were run, and the detection figures count the thirteen that were registered in advance.

**Who wrote the test material.** AI coding agents wrote the nine pairs, their reference merges, the fixtures and their answer keys, under the author's direction, and the author reviewed them. The `voyager` sources are adapted from NASA's page on the Voyager 2 mission, and the `bip39` sources were written by the author together with an AI assistant. The author planted the errors in both. The `voyager` reference is the NASA text that the two sources were split from, and the author wrote the `bip39` reference merge alone. `mahjongg` is adapted from a Wikipedia article. [`tests/pairs/README.md`](../tests/pairs/README.md), [`tests/fixtures/SCHEMA.md`](../tests/fixtures/SCHEMA.md) and [`tests/handwritten/README.md`](../tests/handwritten/README.md) say more.

Silent loss, untaken headings and deviations are computed mechanically from the merged text and the merge's own records. No model judges them. A deviation count has two sides on purpose: a one-sided figure would rank a copy-everything merge first, because it cannot lose what the reference kept.

Whether a sentence is really gone is a different question, and a program cannot answer it: it counts sentences that are still there, and it passes sentences that lost a part. It was answered by reading, and that reading, not the count, decides which model is disqualified. The next two sections explain the count and the reading.

## Silent loss is a count, not a verdict

Silent loss is what a program counts. A source segment (a sentence, a list item, a table row or a heading) is counted when the program cannot find it in the merge and no record of the merge says what became of it. The program looks for a segment in three ways:

- the same text, word for word;
- one segment of the merge that is at least 0.68 similar to it;
- its words standing in the merge as one unbroken run, in order: either every word, or every word but a few small connecting words such as "the" or "is", inside two neighbouring sentences of the merge. This finds a sentence that was kept and joined to its neighbour, or split cleanly in two.

The third way is the amendment of 2026-10-12. Amendment 3 in [`REGISTRATION.md`](../arms/2026-09-27/lineup/REGISTRATION.md) has the exact rule.

A count above zero is a flag for a person to look at. It is not proof that content is gone, and a count of zero is not proof that nothing is:

- **The program still counts a sentence that the merge says in other words.** No program here can recognise that. On the first runs of this benchmark the amended rule counts 10 segments, and a reading found 7 of them in the merge.
- **It can also miss a loss.** A sentence that was cut short passes the similarity test as "reworded" when a little more than half of it is left. With the last two words cut from each, 173 of 181 sentences, list items and table rows of at least six words in the sources of the nine pairs pass. The tool still reports such a sentence as a finding and prints the difference, but it is not counted as silent loss. The amendment does not address this. The audit does, in part: on first runs it read every segment that passed by this test alone and that no record of the merge names, and it found lost content in 3 of those 19.

**Untaken headings.** Two sources often give the same section different headings, and a merge takes one of them. A source heading that the merge did not take and did not record is counted in a column of its own, *untaken headings*, when the section under it is still in the merge or the merge accounted for it. It is not silent loss and it disqualifies nobody. A heading stays silent loss when its whole section is missing with it, or when it carries a number, a link or a code value that the merge does not have. In the tool itself an untaken heading is the finding "Heading dropped in silence", with exit code 3.

## The audit, and what disqualifies

The audit is a reading, made on 2026-10-12 after the benchmark was finished. It asks of a source segment what the program cannot: is its content really gone from the merge? Each segment was read against the whole merged document of its run and put in one of four classes. *Gone*: the fact or instruction is nowhere in the merge. *Partly gone*: part of it is there and part is not, such as a clause, a number, a name, a condition or a link. *Present*: the merge states it, in other words, split in two, or joined to another sentence. *Not content*: a heading whose section is in the merge under another heading, or the like.

**What was read.** Two groups of segments.

- **The segments counted as silent loss** by the scoring as registered: 65 segments in 18 runs, 25 of them on the first runs that the ranking counts. Most pairs ran once, and where a pair ran three times its first run is the one that counts.
- **The segments reworded with no record.** On a first run, a segment that only the similarity test finds, and that no record of the merge names: 19 segments. Neither scoring counts them, and at first the audit did not read them. But a sentence that lost a clause passes that test, and with no record its loss is as silent as a missing sentence. So the audit was extended to them on the same day, by Amendment 4 of the registration.

Together the two groups are 44 segments: every source segment on a first run that the merge does not carry word for word and wrote no record for, but for the two kinds named last under the limits below.

| | read | gone | partly gone | present | not content |
|---|---|---|---|---|---|
| first runs, counted as silent loss | 25 | 0 | 3 | 11 | 11 |
| first runs, reworded with no record | 19 | 1 | 2 | 15 | 1 |
| first runs, both groups | 44 | 1 | 5 | 26 | 12 |
| all runs, counted as silent loss | 65 | 2 | 9 | 42 | 12 |
| everything read | 84 | 3 | 11 | 57 | 13 |

**Who read.** An AI model, Claude Opus, in four separate runs: two readings of each group. No person read the cases. For the first group, one reading classed all 65 cases. The other was given the 25 first-run cases and their merged documents and nothing else: not the first reading's classes, not the program's scores, not the benchmark's figures. The two gave the same class to 23 of the 25 cases. For the second group, each reading was given the 19 segments with the source documents and the merged documents of their runs, and neither was given a score or the other's reading. The two gave the same class to 19 of the 19 cases. So each of the 44 first-run cases was read twice, and the two readings come to the same verdict for every row.

**What disqualifies.** A row is disqualified when the first reading classed at least one of its first-run cases, of either group, as gone or partly gone. The program's count does not disqualify. Had the second reading come to the other verdict for a row, the row would be marked "readings disagree" and keep the first reading's verdict; that did not happen.

Of the 44 first-run cases, 6 have lost content, 3 in each group. Three rows are disqualified by them:

- **Haiku 4.5 on the API**, 2 of the 21 segments read. Its merge of the pair `trace_names` lost a link from one sentence and the author's name from the second source's author line.
- **Haiku 4.5 on the subscription**, 3 of the 8 segments read. One merge lost who is responsible for a step, another lost the second half of a sentence, and its merge of `trace_names` lost the second source's author line wholly, the name and the date.
- **GPT-6 Luna**, 1 of the 4 segments read. A source of the pair `library_holds` says: "When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine." The merge has the instruction without its opening condition, under the heading "Placing an item on the shelf". Both readings class it partly gone, and both mark it borderline, with present as the class it could also be, because the heading implies the occasion.

Both author lines and Luna's sentence are in the second group: the program had passed them as reworded.

**The borderline case and the ruling.** The rule does not ask how sure a reading was, and Luna's borderline case is the only loss the audit found for that row. So the benchmark's operator was asked whether a borderline case disqualifies, and ruled: "Disqualify Luna". A reader who takes the heading as enough finds no loss in that sentence, and then GPT-6 Luna has none. The first reading also marks the two author lines borderline, with not content as the class they could also be. Each Haiku 4.5 row has other cases that are not borderline, so its verdict does not rest on that.

Two more rows had first-run cases and are not disqualified: for Sonnet 5 on the subscription all 9 segments read were present, and for Opus 5.5 on the API both segments read were headings. A row with a count above zero and nothing found gone is flagged, not disqualified. Sonnet 5 on the subscription is the one such row.

**The limits of the audit.**

- **Readings by a model, not by people.** A person who reads the cases may class some of them differently. Every case is published with its quotations in [`cases.md`](../arms/2026-09-27/lineup/audit/cases.md), so that it can be checked in a minute.
- **The reader is not independent of what it read.** All four readings were made by a Claude model, and six of the eight rows are Claude models. GPT-6 Luna, the row disqualified on a borderline case, is not one of them.
- **Some cases are borderline.** 19 of the first reading's 84 classifications are marked so, 11 of them on first runs. One row's verdict depends on one: GPT-6 Luna is disqualified by a ruling on a borderline reading, not by a reading that was sure.
- **Repeated runs were read once, and only their counted segments.** The second reading of the first group covers first runs only, and the second group was read on first runs only. On repeated runs 30 segments that only the similarity test finds have no record and were not read: 20 of Haiku 4.5 on the subscription and 10 of GPT-6 Luna.
- **A segment with a record was not read.** The audit reads what a merge was silent about. A record is a declared change, and a declaration can be wrong: it can call a sentence reworded that lost a clause. That is for the tool's own checks to find, not for this audit. It includes a segment that is missing and has a record which the tool itself rejected. Content that is really gone can sit there.
- **A segment whose words stand in the merge as one run was not read, and neither was a title.** On first runs 5 such segments have no record, and the audit takes them as carried word for word. Also on first runs, 2 source titles are missing from merges of Haiku 4.5 on the API and have no record; the registration leaves a title out of silent loss.

[The audit's own page](../arms/2026-09-27/lineup/audit/README.md) has the result for every row, the cases where the two readings differ, and the limits in full.

## Two scorings

The nine merge pairs have been scored twice, and both scorings are published.

**The scoring as registered** is the one fixed before the run. It looked for a segment in the first two ways only, counted every untaken heading as silent loss, and disqualified a row for any silent loss on a first run. By it five of the eight rows were disqualified, and Sonnet 5 on the API did no better than the mechanical union.

**Why it was amended.** The audit showed that most of what this rule counted was still in the merge. It miscounted for three reasons. A sentence that the merge kept and joined to its neighbour has lost its full stop, so the search for the exact text misses it. A sentence that was split in two, or two that were run into one, is compared with one merge segment at a time and cannot reach 0.68. And a heading is looked for only among the merge's headings, so the heading the merge did not take is missing by construction. So the benchmark's headline figure passed every check while much of what it counted was not lost. No check found that. Reading what the figure had counted did.

**The amended scoring** adds the third way of finding a segment, counts untaken headings apart, and disqualifies on what the audit found gone, not on the count. The scorer uses the same rule to decide what a merge kept, so the deviation figures moved as well. By it three of the eight rows are disqualified, and every row is below the mechanical union. Until the audit was extended it was two, both Haiku 4.5.

**It was made after the results.** The amended scoring is Amendment 3 of the registration, dated 2026-10-12. It was written after every call of the benchmark and with the results known, and it says so. Three things were done to limit what hindsight could do. The amended rule was designed by a separate run of an AI model that was given neither the benchmark's outputs nor the audit. It was fixed in writing before it was run on the nine pairs, and it was changed twice after that, both times to make it stricter. And it was then held against the audit separately, not by its designer.

**So was the extension of the audit.** Amendment 4, of the same day, extends the audit to the segments reworded with no record. It was also written after every call and with the results known, and it says so. It changes no count and no figure of either scoring. It changes what was read, and with that the verdict of one row, GPT-6 Luna. Each of the two readings it rests on was given no score and not the other's reading. The ruling on the borderline case names the row it decides.

**And so were two corrected reference merges.** Amendment 5, of 2026-10-15, corrects the reference merge of `bike_docks`. It had kept the support desk's count of 3 beside the field crew's 2 and added a sentence of its own that neither source has. At `high` a merge is told to choose one value where its sources disagree, and the field crew's runbook gives the reason for 2. The corrected reference keeps 2. The amended scoring is counted against it, and six rows that rightly dropped the count have 2 deviations fewer over the nine pairs. The order, who is disqualified and the baselines do not move. The scoring as registered is still counted against the reference it was registered with, which stays in the pair's directory as `ideal-as-registered.md`. Amendment 6, of the same day, corrects `loading_dock` the same way: its reference kept the hours of a phone line that the newer source says is retired, in a sentence of its own. Seven rows have 1 deviation fewer, Haiku 4.5 on the API, which kept the retired instruction, has 1 more, and the mechanical union goes from 7.67 to 7.78 deviations per pair, because it keeps the hours too.

**What the amended rule changes.** It can only clear a segment that the registered rule counted, never add one, and it clears no segment that the audit classed as gone or partly gone. Of the 42 segments the audit found present it finds 8, and the other 34 stay counted, because they are in other words. All 12 headings move to the column of untaken headings. Over all runs the counted silent losses go from 65 to 45, and the runs with a counted silent loss from 18 to 10.

**Which one is shown.** The amended scoring is shown first: in the README's table, in the web interface's model picker and at the top of [`figures.md`](../arms/2026-09-27/lineup/figures.md). The scoring as registered follows it in `figures.md`, unchanged, and its figures stay in `scored.json`. `differences.json` lists every segment whose count differs between the two, with the merge text it was found in. The detection set and the planted-error set are not scored by this rule and did not change.

## How to read a result row

A row is one model on one route: the vendor's API, or a Claude subscription through the `claude` command line. The [README's table](../README.md#results-2026-09-27) shows these figures for each row, and explains them under "How to read the columns":

| column | what it counts | better is |
|---|---|---|
| Flagged as silent loss | source sentences the program could not find in the merge and that no record explains, summed over the nine pairs | lower; a count above zero is a flag and does not disqualify |
| Lost content, by reading | what the audit found in the sentences it read on the row's first runs: *none*, *in part* when a part of at least one was gone, or *gone* when at least one was gone wholly; a dash where it had nothing to read | none; content gone, wholly or in part, disqualifies |
| Deviations per pair | sentences lost, wrongly kept or repeated against the pair's reference merge, averaged over the pairs | lower; the mechanical union, a script with no model, scores 7.78 |
| Planted errors fixed | how many of the 44 errors in `voyager` and the 14 in `bip39` the merge corrected, as the median of three runs | higher |
| $ per merge | the price of one merge with all its checks | lower |

Most pairs ran once. On six of the eight rows, three of the pairs ran three times, and for those the table counts the first run and [`figures.md`](../arms/2026-09-27/lineup/figures.md) shows the spread. A single run can move a model by several sentences, so treat a small difference between two rows as no difference.

## The fairness rules

- **Disqualify, then rank. Never a composite.** A model is disqualified before anything is ranked when the audit found content gone, wholly or in part, among the segments it read of that model's first runs. The program's count of silent loss alone disqualifies nobody. The rest are ranked on quality (deviations per pair), and cost and then speed only break ties. They break a tie only when every row in it has a list price. Otherwise the rows share a rank, as Opus 5.5 and Sonnet 5 on the subscription do in second place. A weighted score would let a cheap model buy back lost facts with its price, and that is the trade this tool exists to refuse.
- **The same work for everybody.** One pinned version of the tool, byte-identical input files whose hashes are recorded beside the registration (`run.json`), the same flags stated explicitly on every call, the same structured-output tier and one scorer for every model. No answer is shared between runs: a retried run may reuse only its own earlier answers, so nothing is paid twice. All rows ran in one session, and the models of a route took turns pair by pair, so a bad hour at a vendor hits its models alike.
- **Common pairs.** Every model is scored on every registered pair. A model that fails a pair keeps that failure as its own result ("exit 2 on 1 of 9") and is listed after the models that completed everything; its failure never removes the pair from anybody else's score.
- **Failures outside a model's control are not charged to it.** A blank answer, a timeout or a platform error is retried. If a run still fails, a cheap reference run is made against a second vendor. If that one works, the failure counts against the row as a failed endpoint. If it fails too, the fault is the infrastructure's: the run is repeated later and the failure is never scored. A refusal to do the task, whether from the prompt or a safety guardrail, is the model's own result and is flagged as one.
- **No model grades itself.** The merge scores are computed by code. Each model does run LLossless's own checks on its merge, but what its checker concludes cannot improve its score: a lost sentence that the tested model's own verifier confirmed as intentional forgives nothing, and is reported beside the score, not subtracted from it. The disqualification is the one verdict that code does not make. It rests on a reading by an AI model, Claude Opus, made twice for each case, in four separate runs after the benchmark. That reading is no part of a tested model's run, and no tested model's own checker has a say in it. It is still a model's reading, by a model of the same family as six of the eight rows, and two of those rows are Opus rows. For the Opus rows it read two segments, both headings. One of the three disqualifications, GPT-6 Luna's, rests on a single borderline case and on a ruling by the benchmark's operator. No person read the cases.
- **Thinking is configuration, not something that is compared.** Every model ran with reasoning on for all three roles. The API rows ran at the vendor's default reasoning effort and the subscription rows at `medium`; Haiku 4.5 has one level. The setting is in the registration, and reasoning is never switched off to make a model cheaper.
- **Baselines with no model in them.** Three texts are scored with the same scorer: the two sources concatenated, a mechanical union (one source, then every paragraph of the other that it does not already contain), and one source alone. A model whose deviations are not below the mechanical union's is flagged "no better than a mechanical union" beside its rank. Under the amended scoring no row is.
- **Registered before it runs.** The lineup, the settings, the rules for failures and the spending caps are written into a registration file whose hash is recorded before the first call. Corrections afterwards are dated amendments below the original text, never edits. Amendments 1 and 2 were written before the calls they govern. Amendments 3, 4, 5 and 6 were not: they were made on 2026-10-12 and 2026-10-15, after every call and with the results known, and each says so. Amendment 3 changes how a finished merge is scored, not what was run, and the scoring as registered stays published beside it. Amendment 4 changes what the audit read, and no count. Amendments 5 and 6 each correct one reference merge, and with it the amended scoring's deviations on that pair.

## Cost as one comparable figure

The headline cost is the vendor's list price per merge, the checks included, read on the day of the run. A subscription route has no per-call price, so its cost is shown as the API-equivalent figure its own CLI reports, labelled as such, and never as a price or as zero.

## What it cannot tell you

This is a small benchmark: nine pairs, thirteen fixtures, two planted-error documents and one control, mostly English, most of them run once. A difference smaller than the spread between runs is reported as no difference. The reference merges and the answer keys were written inside this project, by Claude coding agents under the author's direction, and nobody outside it has reviewed them. Claude models are among the models ranked against those reference merges. Which rows are disqualified rests on readings by an AI model, two of each case, not on a program and not on people. One of the three disqualifications rests on a single borderline case and a ruling. A segment that has a record was not read, and on repeated runs only the counted segments were. The result is a dated snapshot of what each model did on this task, and a model released after the lineup is frozen goes into the next snapshot.

## The earlier specification

[`bench-spec.md`](bench-spec.md) is an older rule set, version 1.0.0, frozen on 2026-08-30. It governed the study of three open-weight models in August and September 2026, whose raw outputs are in `arms/2026-08-30/` and `arms/2026-09-03/`, and `tests/run_bench.py` still reads its property registry. The release benchmark of 2026-09-27 was not scored under it. Its rules are the ones on this page, and its registration is [`arms/2026-09-27/lineup/REGISTRATION.md`](../arms/2026-09-27/lineup/REGISTRATION.md).
