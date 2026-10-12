# The audit of the silent losses

Made on 2026-10-12, after the benchmark of 2026-09-27 was finished and its results were known, and extended on the same day. This page says what was read, who read it, what came out and how far it can be trusted. [`cases.md`](cases.md) has every case with its quotations, and [`audit.json`](audit.json) has the same in a form a program can read.

## Why there is an audit

The benchmark disqualified a model configuration for "silent loss". By its registered rule a segment of a source document (a sentence, a list item, a table row or a heading) is a silent loss when three things hold: its text is not in the merged document word for word, no record of the merge names it, and no single segment of the merge is at least 0.68 similar to it. That is a rule a program can apply. It does not read.

So the audit asked the question the rule cannot answer: is the content of such a segment really gone from the merged document? It asks that of two groups of segments. The second group was added when it became clear that the first left a gap.

## What was read

- **The segments counted as silent loss.** Every segment the registered scoring counted, in every run that had one, repeats included.
- **The segments reworded with no record.** The third condition of the rule lets a segment through as "reworded" when some segment of the merge is at least 0.68 similar to it. A sentence that lost a clause still resembles the original, so it is called reworded, it is not counted, and the audit of the first group did not read it. Where the merge wrote no record for such a segment, a loss in it is as silent as a missing sentence. So every segment on a first run that the similarity rule alone calls reworded, and that no record of the merge names, was read too. "Alone" means that its words do not also stand in the merge as one unbroken run. [`reworded-by-similarity.json`](../reworded-by-similarity.json) lists what that rule calls reworded in every run and marks these segments `similarity_alone`. Whether a record names a segment is in the `report.json` of its run.

Together the two groups are every source segment on a first run that the merge does not carry word for word and for which it wrote no record. A first run is the first counted draw of a pair, which is the draw the benchmark's order reads. On repeated runs only the first group was read. The result section ends with a count of what has no record and was not read.

Every segment was read together with the whole merged document of its run.

## Who read

Four separate runs of an AI model, Claude Opus. No person read the cases.

- **The segments counted as silent loss** were read by reading 1 and reading 2. Reading 1 was given every counted segment and the merged document of its run, and classed all of them. Every quotation it gives was checked by a program against the file it is quoted from. Reading 2 was given the cases on first runs and their merged documents, and nothing else. It was not shown reading 1's classes, the program's scores or the benchmark's figures.
- **The segments reworded with no record** were read by reading A and reading B. Each was given the segments with the source documents and the merged documents of their runs, and nothing else. Each was told that a program had called the segments reworded and that the merge had written no record for them. Neither was given the program's scores, the benchmark's figures or the other's reading. The passages they quote from the merged documents, and the words they report as absent from them, were checked by a program against those documents when this page was extended.

In the tables, in `audit.json` and in the rule below, "the first reading" is reading 1 for the first group and reading A for the second, and "the second reading" is reading 2 and reading B.

## The classes

Each segment was put in one of four classes, by meaning and against the whole merged document, not against the sentence nearest to it.

- **gone**: the fact or instruction is nowhere in the merged document.
- **partly gone**: part of it is in the merged document and part is gone. A clause, a number, a name, a condition, a link, or who is responsible for something.
- **present**: the merged document states it, in other words, split in two, or joined onto another sentence.
- **not content**: a heading whose section is in the merged document under another heading, or the like.

Where a second class could also be defended, the case is marked borderline, with that class and the reason.

## The result

Every figure in this section is derived from `audit.json` and the stored runs by `python3 tests/lineup_figures.py --check`, which fails if a line here no longer says what they give.

### Result on first runs

The runs the order counts: the first counted draw of each pair. Every case on them was read twice, and the classes in these tables are the first reading's. `read` is how many segments of a configuration the audit read there: those the registered scoring counted as silent loss (`counted`), and those the similarity rule alone called reworded and no record of the merge names (`reworded, no record`). `audited loss` is the verdict.

| configuration | read | counted | reworded, no record | gone | partly gone | present | not content | audited loss |
|---|---|---|---|---|---|---|---|---|
| opus-5.5-api | 2 | 2 | 0 | 0 | 0 | 0 | 2 | no |
| gpt-6-luna-api | 4 | 2 | 2 | 0 | 1 | 3 | 0 | yes: disqualified; its one case is borderline |
| haiku-4.5-sub | 8 | 3 | 5 | 1 | 2 | 5 | 0 | yes |
| sonnet-5-sub | 9 | 5 | 4 | 0 | 0 | 9 | 0 | no |
| haiku-4.5-api | 21 | 13 | 8 | 0 | 2 | 9 | 10 | yes |
| all | 44 | 25 | 19 | 1 | 5 | 26 | 12 | |

The segments counted as silent loss, on first runs:

| configuration | counted | gone | partly gone | present | not content |
|---|---|---|---|---|---|
| gpt-6-luna-api | 2 | 0 | 0 | 2 | 0 |
| opus-5.5-api | 2 | 0 | 0 | 0 | 2 |
| haiku-4.5-sub | 3 | 0 | 2 | 1 | 0 |
| sonnet-5-sub | 5 | 0 | 0 | 5 | 0 |
| haiku-4.5-api | 13 | 0 | 1 | 3 | 9 |
| all | 25 | 0 | 3 | 11 | 11 |

The segments reworded with no record, on first runs:

| configuration | reworded, no record | gone | partly gone | present | not content |
|---|---|---|---|---|---|
| gpt-6-luna-api | 2 | 0 | 1 | 1 | 0 |
| sonnet-5-sub | 4 | 0 | 0 | 4 | 0 |
| haiku-4.5-sub | 5 | 1 | 0 | 4 | 0 |
| haiku-4.5-api | 8 | 0 | 1 | 6 | 1 |
| all | 19 | 1 | 2 | 15 | 1 |

The 6 first-run cases the first reading classed gone or partly gone:

- Counted as silent loss: `haiku-4.5-api`, `trace_names`, segment `b6`, "Only letters, digits, spaces and hyphens are accepted (it has to match ^[A-Za-z0-9 -]+$) as documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)": partly gone.
- Counted as silent loss: `haiku-4.5-sub`, `bike_docks`, segment `b18`, "The support desk takes a station out of service in the app when more than half its docks are faulted.": partly gone.
- Counted as silent loss: `haiku-4.5-sub`, `rate_limits`, segment `a6`, "A client spread across eight worker processes is throttled at exactly the point one process would have been — and pays for the extra file descriptors as well.": partly gone.
- Reworded with no record: `gpt-6-luna-api`, `library_holds`, segment `a3`, "When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine.": partly gone (both readings name present as the alternative).
- Reworded with no record: `haiku-4.5-api`, `trace_names`, segment `b2`, "Author: Marlowe Ferrante Updated: 2026-02-03": partly gone (the first reading names not content as the alternative).
- Reworded with no record: `haiku-4.5-sub`, `trace_names`, segment `b2`, "Author: Marlowe Ferrante Updated: 2026-02-03": gone (the first reading names not content as the alternative).

### Result over all runs, repeats included

The segments counted as silent loss, in every run that had one. The segments reworded with no record were read on first runs only and are not in this table.

| configuration | runs | counted | gone | partly gone | present | not content |
|---|---|---|---|---|---|---|
| gpt-6-sol-api | 1 | 1 | 0 | 0 | 1 | 0 |
| opus-5.5-api | 1 | 2 | 0 | 0 | 0 | 2 |
| gpt-6-luna-api | 3 | 5 | 0 | 0 | 5 | 0 |
| sonnet-5-sub | 2 | 5 | 0 | 0 | 5 | 0 |
| haiku-4.5-api | 7 | 13 | 0 | 1 | 3 | 9 |
| haiku-4.5-sub | 4 | 39 | 2 | 8 | 28 | 1 |
| all | 18 | 65 | 2 | 9 | 42 | 12 |

### The two readings

Every first-run case was read twice: 44 cases. Of the 25 segments counted as silent loss, both readings give the same class to 23. Of the 19 segments reworded with no record, both readings give the same class to 19.

| configuration | cases | gone or partly gone, first reading | gone or partly gone, second reading | same verdict |
|---|---|---|---|---|
| opus-5.5-api | 2 | 0 | 0 | yes |
| gpt-6-luna-api | 4 | 1 | 1 | yes |
| haiku-4.5-sub | 8 | 3 | 4 | yes |
| sonnet-5-sub | 9 | 0 | 0 | yes |
| haiku-4.5-api | 21 | 2 | 3 | yes |

- Differs: `haiku-4.5-api`, `payroll_cutoff`, draw 1, segment `b13`. First reading: not content, with gone as the alternative. Second reading: gone, with not content as the alternative.
- Differs: `haiku-4.5-sub`, `rate_limits`, draw 1, segment `a8`. First reading: present, with partly gone as the alternative. Second reading: partly gone, with present as the alternative.

The two readings come to the same verdict for every configuration.

19 of the 84 classifications of the first reading are marked borderline, 11 of them on first runs. With every borderline case read the other way, gone plus partly gone is 3 to 11 on first runs, and 7 to 18 over all runs of the segments counted as silent loss. The verdict depends on a borderline case for: gpt-6-luna-api.

`gpt-6-luna-api` is disqualified; its one case is borderline: `library_holds`, segment `a3`, "When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine.": partly gone (both readings name present as the alternative).

### What the amended scoring makes of the segments counted as silent loss

| first reading | cases | still counted as silent loss | found, reworded | counted as an untaken heading |
|---|---|---|---|---|
| gone | 2 | 2 | 0 | 0 |
| partly gone | 9 | 9 | 0 | 0 |
| present | 42 | 34 | 8 | 0 |
| not content | 12 | 0 | 0 | 12 |

The 19 segments reworded with no record are not in this table: both scorings call them reworded, and neither counts them.

### What has no record and was not read

- On repeated runs: 30 segments that the similarity rule alone calls reworded and that no record names (`haiku-4.5-sub` 20, `gpt-6-luna-api` 10).
- On first runs: 5 segments that the similarity rule calls reworded and that no record names, whose words also stand in the merge as one unbroken run, in order: 3 with every word, punctuation and capitals aside, and 2 with every word but small connecting words. The audit takes these as carried word for word.
- On first runs: 2 source titles that are not in the merge and that no record names (`haiku-4.5-api` 2). The registration leaves a title out of silent loss.

## Why the program counted the first group, and let the second through

Most of the counted segments are still in the merged document. The registered rule misses them for three reasons.

- **A sentence joined to its neighbour.** The search is for the exact text, final punctuation included. A sentence that the merge joined onto another with a comma, a colon or a semicolon has lost its full stop and is not found.
- **A sentence split, or two run into one.** The similarity score compares the segment with one segment of the merge at a time. A sentence kept whole inside a merge sentence about twice its length cannot reach 0.68, by arithmetic.
- **A heading not taken.** A heading is looked for only among the merge's headings. Where the two sources head one section differently, the heading the merge did not take is missing by construction, and is counted unless the merge wrote a record for it.

The amended scoring (`REGISTRATION.md`, Amendment 3) finds the first kind and the cleanly split ones of the second, and counts the third in a column of its own. The table above shows what it makes of every class. The sentences it still counts although a reading found them present are sentences in other words, which no program here can recognise.

The same similarity score errs the other way too, and that is what the second group is for. A sentence that was cut short still resembles the original and passes as "reworded" whenever a little more than half of it is left. Most segments the rule calls reworded are exactly that, and a reading found the ones that are not. Neither scoring counts them, before or after the audit read them (`REGISTRATION.md`, Amendment 4).

## How the result is used

The rule that turns the readings into a verdict is this, and nothing else:

- A configuration has **audited loss on a first run** if the first reading classed at least one of its first-run cases as gone or partly gone. A first run is the first counted draw of a pair, which is the draw the benchmark's order reads. The cases are those of both groups.
- Where the second reading, by the same rule, comes to the other verdict for a configuration, that configuration is marked **"readings disagree"** in the tables. Its verdict stays the first reading's.

Under the amended scoring a configuration with audited loss on a first run is disqualified. The program's count of silent losses stays a column in the benchmark's table, as what it is: source segments the program could not find and that no record explains. It does not disqualify. The rule is the function `verdict_of` in `tests/lineup_figures.py`.

A borderline case counts like any other: the rule does not ask how sure a reading was. Whether it should was put to the benchmark's operator when the only case of loss of one configuration turned out to be borderline, and the ruling was "Disqualify Luna" (`REGISTRATION.md`, Amendment 4). So that a reader sees the ruling and not only its effect, the tables say of a configuration whose verdict rests on borderline cases and on nothing else: "disqualified; its one case is borderline". A case of loss is borderline in this sense when its first reading names present or not content as the class it could also be.

## The limits

- **Readings by a model, not by people.** A person who reads the cases may class some of them differently. The quotations are there so that a reader can check a case in a minute.
- **The reader is not independent of what it read.** All four readings were made by a Claude model, and most of the configurations it read are Claude models too.
- **Some cases are borderline.** The result section says how many, and how far the totals move if every one of them is read the other way.
- **One disqualification rests on a single borderline case.** `gpt-6-luna-api` has one case of loss, and both readings of it name present as the class it could also be. The source says "When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine." The merge has the instruction without its opening condition, under the heading "Placing an item on the shelf", which implies the occasion. A reader who takes the heading as enough finds no loss there, and then that configuration has none. It is disqualified by a ruling on a borderline reading, not by a reading that was sure.
- **Repeated runs were read once, and only their counted segments.** The second reading of the first group covers first runs only. The segments reworded with no record were read on first runs only; the result section counts those on repeated runs.
- **A segment with a record was not read.** The audit reads what a merge was silent about. A record is a declared change, and a declaration can be wrong: it can call a sentence reworded that lost a clause, or give a reason that does not hold. That is for the tool's own checks on the records and for its judge to find, not for this audit. It includes a segment that is missing and has a record which the tool itself rejected: that is not a silent loss by the benchmark's definition, and content that is really gone can sit there. `figures.json` gives the count per row as `absent_behind_rejected_declarations`.
- **A segment whose words stand in the merge as one run was not read, and neither was a title.** The audit takes the first as carried word for word, and the registration leaves a source title out of silent loss. The result section counts those on first runs that have no record.
- **What reading 2 noticed outside its cases was not followed up.** All of it is in merges of `haiku-4.5-api`. In `freezer_alarm` the first sentence of the section "Reading the alarm" is not in the merged document; only the heading was among the cases. In `loading_dock` the merged document contradicts itself about the phone line. In `index_429` the conclusion of the item "Resource accounting" is not in the merged document.

## The files

| File | What it is |
|---|---|
| `README.md` | This page. |
| `cases.md` | Every case with its quotations, run by run. For a segment counted as silent loss: what the first reading found, what each scoring makes of it, and the second reading's line. For a segment reworded with no record: both readings in full. The second reading's table of the first-run cases of the first group closes the page. Generated from `audit.json` and the stored runs. |
| `audit.json` | One entry per case: the configuration, the pair, the draw, the segment and its text, the group it belongs to (`counted_missing` or `reworded_no_record`), the first reading (class, alternative, and its evidence: quotations, what is gone, why) and the second reading where there is one (class, alternative, evidence). An input of `tests/lineup_figures.py`, which refuses it unless its cases are exactly the segments the registered scoring counted and the segments on first runs that the similarity rule alone calls reworded and no record names. |
