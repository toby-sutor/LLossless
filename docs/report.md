# Reading the report

Every run writes one report. This page says what each section of it means, what to do about it, and whether it can change the exit code. The report is printed as Markdown on stdout. The same report can be written as JSON and as an HTML page, and the web interface shows it as tabs; the section [JSON, HTML and the web interface](#json-html-and-the-web-interface) covers those.

> **In short**
>
> - **Read the Verdict first.** It states the result in one paragraph and always agrees with the [exit code](reference.md#exit-codes).
> - **Then read Coverage.** It says how much was examined. A clean verdict over three claims proves little.
> - **Findings, Attributions and Structure list what is wrong with the merged document.** Every entry names a file and a line or a segment, so you can check it by hand.
> - **Review queue and Declarations list what the merge says it left out or changed on purpose.** Those are decisions for you to accept or undo, not errors.
> - **Inventory lists every claim.** Use it to look up what happened to one particular fact.

Two terms are used throughout. A **claim** is one short factual statement the model extracted from a document, such as "The connect timeout is 30 seconds." Its id names the document it came from: `A-002` is the second claim of the first source, `B-001` the first claim of the second source, and `M-014` a claim of the merged document. A **segment** is one piece of a document as written: a sentence, a heading, a list item, a table row or a code block. `a7` is the seventh segment of the first source and `m6` a segment of the merged document.

## The sections at a glance

Every report has seven sections, and four more on a `merge` run, the last of them only when the merge added something. Attributions and Number format are printed only when they have something to show, and Merged document only when the merge was not written to a file. The table lists all of them in the order they are printed.

| Section | Printed | What it tells you | Can it change the exit code? |
|---|---|---|---|
| **Verdict** | always | The result in one paragraph. | It states the code. |
| **Coverage** | always | How many claims were extracted and checked, and whether part of the check failed to run. | Yes: 2 when part of the check did not run. |
| **Findings** | always | Each claim that was dropped, contradicted, invented, or carried only in part. | Yes: 1. |
| **Attributions** | only when something was found | Sentences that credit a source with a statement that source does not make. | Yes: 1. |
| **Number format** | only when something was flagged | Numbers a reader could misread, such as `17.560`, and numbers whose value the merge changed. | A changed value: 1. A warning: no. |
| **Length capped** | always | Explanations a model wrote that were too long and were shortened. | No. |
| **Not graded** | always | Claims that got no verdict. | Yes: 2. |
| **Inventory** | always | Every claim, and what became of it. | No. It repeats the findings as tables. |
| **Structure** | `merge` | The results of the mechanical checks: missing or reworded segments, changed numbers and links, titles, repeated content. | Yes: 1 or 3. |
| **Review queue** | `merge` | Facts the merge said it left out, confirmed missing. | No, unless too much was left out: then 1. |
| **Declarations** | `merge` | Every change the merge said it made, and whether the checks agree. | No. |
| **Added from outside the documents** | `merge` at `--fidelity open` or `sourced`, only when the merge added something | Statements the merge took from outside your documents. | An addition: no. A correction of a source: 1. |
| **Provenance** | always | Which models and settings produced the run, what it cost, and whether content left the machine. | No. |
| **Merged document** | `merge` without `-o` | The merged text itself. | No. |

A `verify` run checks a merge made elsewhere. That merge declared nothing to the tool, so a `verify` report has no Structure, Review queue or Declarations section. A `--dry-run` report holds only a list of planned calls and the Provenance section.

The exit codes are defined in the [command-line reference](reference.md#exit-codes). In brief: 0 means nothing was found, 1 means the merged document has a fault, 3 means the document passed but the merge described its own work wrongly, and 2 means the check did not finish, so the result is inconclusive. When several apply, 2 wins over 1 and 1 wins over 3.

## Sections in every report

### Verdict

**What it shows.** One paragraph. Its bold opening sentence is the result.

**How to read it.** The opening sentence is one of these:

| The verdict opens with | Meaning | Exit code |
|---|---|---|
| `No extracted claim was dropped, contradicted, invented, or carried only in part.` | Nothing was found. | 0 |
| `No undeclared claim was dropped, contradicted, invented, or carried only in part.` | Nothing was found, but the merge left facts out on purpose. They are in the Review queue. | 0 |
| `N finding(s).` | The merged document has faults. The sentence goes on to count them by kind. | 1 |
| `N finding(s), all in the merge's account of itself.` | The merged document passed. What the merge declared about its own work is wrong. | 3 |
| `Inconclusive.` | Part of the check did not run, or produced nothing usable. Coverage shows which part. | 2 |
| `Inconclusive: not a sourced merge.` | The run was made at `--fidelity sourced` and the model looked nothing up. | 2 |
| `Cancelled.` | The run was stopped before it finished. | 2 |

Later sentences give the counts and point to the sections below. Some of them narrow what the opening sentence means. Look for these:

| A later sentence that starts | Appears | What it means for you |
|---|---|---|
| `N statement(s) in the merge came from outside your documents` | at `--fidelity open` or `sourced` | For those statements a clean verdict does not mean they are true. See [Added from outside the documents](#added-from-outside-the-documents). |
| `The model retrieved.`, `Nothing was retrieved.` or `Whether anything was retrieved is unmeasured.` | at `--fidelity sourced` | Whether the model looked facts up on the web or answered from memory. |
| `This run checked only that your documents' content survived.` | at `--verify-depth coverage` | Nothing checked whether the merge invented anything. |
| `N contradiction(s) below are covering values` | at `--fidelity open` or `sourced` | The merge replaced two disagreeing figures with a range and said so. They still count as findings: check that each range really covers both figures. |
| `The merge flagged these documents as possibly not belonging together` | when the merge model thought the inputs were unrelated | Check that you merged the right files. No effect on the exit code. |
| a file name, then `produced no claims` | when a source yielded no claims | On `verify`, nothing about that source was checked and the run exits 2. On `merge`, only the Structure checks cover it. |

On a `verify` run a clean verdict ends by saying that titles, headings and formatting were not checked. Only `merge` runs the mechanical checks that cover them.

**What to do.** At exit 0, look at Coverage and the Review queue before you use the merged document. At exit 1, go to the sections the verdict names. At exit 3, the document is usable; Structure says which declarations were wrong. At exit 2, run it again and do not rely on this result.

**Exit code.** The verdict and the exit code always agree: a run that exits 1, 2 or 3 never opens with a clean sentence.

### Coverage

**What it shows.** A table of counts: how much was extracted, how much of it was checked, and how much could not be checked.

| Row | What it counts |
|---|---|
| Claims extracted from a file | The claims the model found in each document, the merged document included. |
| Forward: source claims accounted for in the merge | Of the source claims that were checked, how many the merge carries whole. |
| Forward: carried only in part | Source claims the merge carries with a detail missing. They are not in the ratio above. |
| Forward: one file's claims accounted for | The forward ratio again, for each source on its own. |
| Reverse: merge claims found in a source | Of the merged document's claims, how many a source supports. |
| Reverse: supported only in part | Merge claims that add a detail to something a source does state. |
| Evidence grounded | Of the verdicts that quote evidence, how many quotes were found in the file they name. |
| Units of work errored | Steps that failed. Each failure is described under the table. |
| Claims submitted but not graded | Claims that got no verdict. They are listed under [Not graded](#not-graded). |

**How to read it.** A ratio reads `carried/checked`. A ratio that could not be computed is replaced by the reason in words, never printed as `0/0`. The per-source rows show where a loss sits: `3/3` for one source and `0/3` for the other means the merge ignored a whole document, which the pooled `3/6` alone would not show.

**What to do.** If few claims were extracted, a clean verdict covers little: read the merged document yourself. If one source has a low ratio, read its table in the Inventory. If a step errored or claims were not graded, run it again.

**Exit code.** The run exits 2 when a step errored, when a claim was not graded, when a source produced no claims on a `verify` run, or when claims were graded and not one evidence quote was found in the file it names. Nothing else in this section changes the code: the lost claims it counts are the entries under Findings.

### Findings

**What it shows.** One entry for each claim with a problem, under up to five headings:

| Heading | Meaning |
|---|---|
| Dropped | A fact in a source is not in the merged document. |
| Partly dropped | The merged document carries the fact with a detail missing. |
| Contradicted | The merged document and a source state different things. |
| Invented | The merged document states a fact that no source states. |
| Partly invented | The merged document adds a detail to a fact the sources do state. |

**How to read it.** Each entry gives the claim id, the file and line the claim came from, the claim text, the evidence the checking model quoted, the document the claim was checked against, and the model's reason in its own words.

`(grounded)` after a quote means the quote was found in the file named. `(transcription_error)` means it was found in no file, and `(attribution_error)` means it was found in a different file. Check such a verdict yourself before you act on it.

A contradiction prints both statements, each under the name of its file. One disagreement often appears twice: once as a source claim (`A-` or `B-`) that the merge contradicts, and once as a merge claim (`M-`) that a source contradicts.

When no claim has a problem the section says `None.` If the run has findings elsewhere, it says so and names the section they are in.

**What to do.** Open the file at the line given and compare. Then correct the merged document, or run the merge again. For a contradiction, decide which document is right.

**Exit code.** Any entry here makes the run exit 1. Two kinds of claim are deliberately listed elsewhere and do not count: a dropped claim the merge declared and the check confirmed (see [Review queue](#review-queue)), and an invented claim the merge declared as an addition (see [Added from outside the documents](#added-from-outside-the-documents)).

### Attributions

**What it shows.** Sentences in the merged document that credit a named source with a statement that source does not contain, while another source contains it word for word. Example: "According to the Operator Guide, the minimum TLS version is 1.2", where the Operator Guide never mentions TLS and the other document does. The fact is real; the credit is wrong. The section is printed only when such a sentence was found.

**How to read it.** Each entry names the segment of the merged document, says which source was credited and which one really makes the statement, and shows both texts in the comparison block described under [Structure](#structure). No model is involved: the texts are compared as strings, and the source is recognised by its title or its file name. Only an exact case is listed. A misattribution in reworded form, or a name that fits two sources, is not caught here.

**What to do.** Correct the credit in the merged document.

**Exit code.** Any entry makes the run exit 1. This check runs on `merge` and on `verify`, at either verification depth.

### Number format

**What it shows.** Whether each document writes decimals with a point or a comma, and every number that does not fit, or that the merge changed. The same digits can differ by a factor of 1,000: `17.560` is seventeen point five six with a decimal point, and seventeen thousand five hundred and sixty with a decimal comma. The section is printed only when something was flagged.

**How to read it.** A table gives each document's convention and how it was decided: from its own unambiguous numbers, or else from its language (English writes a decimal point, German a decimal comma), or else from the majority of its numbers. Below it, entries are grouped under `Faults` and `Warnings`. A fault, labelled `value changed by the merge`, is a source number that the merged document writes so that it now reads as a different value. A warning is a number a reader could misread, for example one written in the other convention or one that can be read both ways. No model is asked and no number is rewritten.

**What to do.** For a fault, correct the number in the merged document. For a warning, decide which reading is meant and make the number unambiguous in your documents.

**Exit code.** A fault makes the run exit 1. Warnings never change the code.

### Length capped

**What it shows.** Every reason or explanation a model wrote that was longer than its length limit and was shortened: the field, how long it was, and the limit. It says `None.` when nothing was shortened.

**How to read it.** Only explanatory text is affected: the reason beside a declaration, a declared replacement text, or the checking model's reason for a verdict. The verdicts and the merged document are not.

**What to do.** Usually nothing. If you need the full text of one shortened explanation, run it again.

**Exit code.** No effect.

### Not graded

**What it shows.** Claims for which the checking model returned an unusable answer, even after it was asked again. Each entry gives the claim id, the direction of the check, and what was wrong with the answer. When every claim was graded, the section says so.

**How to read it.** The claims listed here have no verdict in either direction. The other claims of the same batch were graded normally and their verdicts stand.

**What to do.** Treat the report as incomplete and run it again. Findings listed elsewhere are real, but they cover only the claims that were graded.

**Exit code.** Any entry makes the run exit 2, whatever the graded claims said.

### Inventory

**What it shows.** Every claim that was extracted, one table per source and then one for the merged document. The sections above list only the problems; this lists everything, so you can look up one fact. The two tables below are what the report prints for a small made-up run in which one claim was carried, one contradicted and one dropped.

### `notes-a.md` -- 3 claim(s): 1 dropped, 1 contradicted, 0 partly kept, 1 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 3 | The archive is signed. | 3 | dropped | The reference text settles it. |
| 2 | The connect timeout is 30 seconds. | 2 | contradicted | 'The connect timeout is 60 seconds.' in `merged.md` -- The reference text settles it. |
| 1 | The relay listens on port 8443. | 1 | carried | 'The relay listens on port 8443.' in `merged.md` -- The reference text settles it. |

The table for the merged document checks the other direction. It is where a merge that kept every source fact and also added one of its own becomes visible:

### `merged.md` -- 3 claim(s): 0 invented, 1 contradicted, 0 supported in part, 2 supported

Each claim below was read against `notes-a.md` and `notes-b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 2 | The connect timeout is 60 seconds. | contradicted | `notes-a.md` | 'The connect timeout is 30 seconds.' in `notes-a.md` -- The reference text settles it. |
| 1 | The relay listens on port 8443. | supported | `notes-a.md` | 'The relay listens on port 8443.' in `notes-a.md` -- The reference text settles it. |
| 3 | The read timeout is 45 seconds. | supported | `notes-b.md` | 'The read timeout is 45 seconds.' in `notes-b.md` -- The reference text settles it. |

**How to read it.** Rows with a problem come first. The status words are:

| In a source's table | In the merged document's table | Meaning |
|---|---|---|
| `carried` | `supported` | The claim is on the other side, whole. |
| `partly kept` | `supported in part` | Only part of the claim is on the other side. |
| `dropped` | `invented` | The other side does not have the claim. |
| `contradicted` | `contradicted` | The other side states something different. |
| `not checked` | `not checked` | No verdict came back for this claim. |

The claim text is always printed whole. The `Note` column holds the quoted evidence, the file it was quoted from and the model's reason, on carried rows too. A quote that was not found where the model said is marked in its row with `transcription_error` or `attribution_error`, which mean the same as under [Findings](#findings). A line number followed by `(unverified)` is the model's estimate: the text it quoted was not found in the document. `Found in` names the source that supports a merge claim, and shows `--` for an invented one.

**What to do.** Search the tables for the fact you care about. If it is in no table, it was never extracted as a claim, so no claim-level check covered it. On a `merge` run the Structure checks still cover its segment.

**Exit code.** No effect of its own. Every problem row here is also an entry under Findings, in the Review queue, or under Added from outside the documents.

## Sections on a `merge` run

When LLossless writes the merge itself, the model returns two things: the merged document, and a **declaration** for every source segment it did not copy word for word. A declaration names the segment, says what happened to it, and gives a reason. There are six kinds:

| Declared as | The merge says |
|---|---|
| `reworded` | The same content, in other words. |
| `superseded` | Another document's version of this content was used instead. |
| `subsumed` | The content survives inside a broader or combined statement. |
| `duplicate` | Another segment already carries this content. |
| `reconciled` | This segment and at least one other were combined into a statement neither makes alone. |
| `dropped` | The content is not in the merged document and nothing replaces it. |

The tool does not take these declarations on trust. The next three sections check them: Structure by comparing text, Review queue and Declarations against the claim-level verdicts.

### Structure

**What it shows.** The results of nine mechanical checks over the source segments, the merged document and the declarations. No model is involved: every check compares strings or counts, so you can verify any entry by hand. These checks cover what claims cannot: titles and headings, tokens that must survive exactly, and segments from which no claim was extracted.

**How to read it.** The section opens with the number of checks and the number of source segments they ran over. A line starting `Ordering:` then describes how the merge arranged the sources. It is a measurement and never a finding, but if it says each source sits in one unbroken block and your documents overlap, the merge may have pasted them one after the other instead of merging them. After that comes either `No structural finding.` or entries under these headings:

| Heading | Meaning | Exit code |
|---|---|---|
| Absent and undeclared | A source segment is missing from the merged document and no declaration explains it. | 1 |
| Reworded and undeclared | A source segment is in the merged document in changed wording and no declaration explains it. At `verbatim`, changed line breaks count too. | 1 |
| Declared gone, still here | A declaration says the segment was replaced or absorbed, and the merged document still carries it unchanged. Nothing was lost. | 3 |
| Invented segment | A declaration names a segment that no source has. | 1 |
| Unresolved replacement | A declaration points at replacement text that is not in the merged document. | 3 |
| Not permitted here | The merge declared a kind of change that the fidelity level forbids. | 3 |
| Verbatim violation | A number, unit, URL, path, version string, piece of inline code or code block did not survive exactly. | 1 |
| Over budget | The merge declared more than 3% of the source segments dropped, or let one replacement stand in for more than 3 missing segments. | 1 |
| Title not from a source | The merged document has no title, or a written one where the title policy requires a source's title. | 1 |
| Title dropped in silence | A source title is gone and no declaration says what replaced it. | 3 |
| Stated twice | The merged document says the same thing more than once. | 1 |
| Prompt example returned | The merged document contains a word from the tool's own prompt example and from no source. | 1 |

In ordinary text, runs of spaces and line breaks are ignored when a token is compared. Inside a fenced code block, spacing is compared exactly, because there indentation is content; only line endings and trailing spaces are ignored.

Where a finding has a source text and a merge text, both are printed one above the other, followed by a word-by-word comparison:

```text
In the source: The audit log is written to /var/log/relay.
In the merge:  The audit log is saved to /var/log/relay.
What changed:  The audit log is [-written-] {+saved+} to /var/log/relay.
```

`[-...-]` marks what the source said and `{+...+}` what the merge says instead. When the two texts are less than 80% alike, a comparison would mark nearly every word, so the `What changed` line is left out and only the two texts are shown.

Two notices can replace or precede the results. `Not checked.` means the mechanical checks did not run, so nothing below the claim level was examined. `Unclosed fence` means a code fence in a source is never closed, so everything after it was compared as code.

**What to do.** For an exit-1 heading, compare the segment with the merged document and correct the document, or run the merge again. For an exit-3 heading the document needs no change: the declaration is wrong, and a new run gives you a clean record if you need one. For an unclosed fence, close it in the source and run again.

**Exit code.** 1 or 3, as the table says. A run with both kinds exits 1.

### Review queue

**What it shows.** Claims from segments the merge declared `dropped`, where the forward check confirms the claim is gone. These are losses the merge owned up to.

**How to read it.** Each entry gives the claim with its file and line, then three lines: `left out of` names the segment, `the merge's reason` quotes the merge's own sentence, which nothing has checked, and `confirmed absent` says the check looked for the claim in the merged document and did not find it. An empty queue says `None.`

**What to do.** For each entry, decide: agree that the fact stays out, or put it back into the merged document.

**Exit code.** No effect, with one rule. A merge may declare at most 3% of the source segments dropped. Above that share the run exits 1, this section prints an `Over budget.` notice, and Structure lists the breach. The share counts declared segments, not claims, so it includes dropped segments from which no claim was extracted. `--loss-budget` changes the ceiling; see [Loss budget](reference.md#loss-budget). A dropped claim the merge did not declare is never queued: it is an entry under Findings.

### Declarations

**What it shows.** Every declaration the merge made, in one table: the segment, what was declared, the merge's reason, whether the checks agree, and on what evidence. Above the table, a line starting `Declared loss:` gives how many source segments were declared gone, as a count and as a percentage, beside the ceiling.

**How to read it.** The `Confirmed?` column holds one of three words:

| Word | Meaning | What to do |
|---|---|---|
| `confirmed` | The verdicts on the claims from that segment match the declaration. A `dropped` segment's claims are really gone; a `reworded` segment's claims are still there. | Read the reason and accept or undo the change. Confirmed drops are in the Review queue. |
| `rejected` | The verdicts contradict the declaration, for example a segment declared `dropped` whose fact is still in the merged document. | The merge described its own work wrongly. If content was really lost, it is listed under Findings or Structure. If it is not, the document is fine for that segment. |
| `unchecked` | Nothing could test the declaration: no claim was extracted from the segment and the position of its text settles nothing. This is not agreement. | Compare the segment with the merged document yourself if it matters. |

`The merge's reason` is what the merge wrote, and nothing checks it. `On what evidence` is the tool's account of how it reached the word beside it. A merge that declared nothing gets a sentence saying so: it thereby asserts that every source segment was carried over unchanged, and Structure checks that.

**Exit code.** No effect. A rejected declaration alone never changes the code. The losses it failed to excuse are findings, and those do.

### Added from outside the documents

**What it shows.** Statements the merge took from outside your documents. Only `--fidelity open` and `sourced` allow that, and only as a declared record, so the section is printed at those two levels when the merge declared at least one. The table has one row per statement: the statement, what it corrects, its basis (`cited` or `the model's own knowledge`), the source it names, the merge's reason, and the claims it covers.

**How to read it.** Nothing in this section has been checked, because your documents are the only reference the tool has. `Source` is plain text: LLossless did not open, fetch or check any source named there. A sentence above the table says whether the model made web requests of its own, as far as that could be measured. There are two cases, and the `Corrects` column tells them apart:

- **An addition.** `Corrects` says *nothing named*. Your documents are silent on the statement, so they cannot contradict it. It is not a finding.
- **A correction.** `Corrects` quotes a statement from one of your documents. The merged document now says something a source denies. The tool cannot tell a correction from an error, so the statement is also reported as a finding.

**What to do.** Read every row and decide whether the statement is true and whether you want it in the document. For a correction, decide which is right: the source or the merge.

**Exit code.** An addition does not change the code. A correction makes the run exit 1. A statement from outside the documents that the merge did not declare is reported as `Invented` under Findings, and also exits 1.

### Merged document

Where the merged text is depends on how you ran the merge:

- **With `-o PATH`:** in that file. The report then has no Merged document section, and the closing lines on stderr name the path.
- **Without `-o`:** in the last section of the report, inside a fenced block.
- **In the web interface:** at the top of the result, with buttons to copy or download it.

## Provenance

**What it shows.** A table of how the run was made, and notes under it. Nothing here changes the exit code.

| If you want to | Look at |
|---|---|
| repeat the run | `Fidelity`, `Verification depth`, `Title policy`, `Base document`, the `Model` rows, `Structured output`, `Decoding` (temperature, seed, thinking, effort), the `Prompt` rows and `LLossless commit` |
| show which model answered | The `Model` rows, one per role (merge, decompose, verify). Where a program answered, the row also gives the model id that program reported. |
| know whether content left the machine | `Endpoint`, which says `local`, `hosted` or `command` after the id, and the notes under the table |
| see what the run cost | `Calls` (live, cached, replayed), `Tokens`, `Cost`, `Duration` |
| see whether anything went wrong | `Schema repairs`, `Errors`, and the notes under the table |

**How to read it.** `Endpoint` shows an id, never an address, so a report can be shared without revealing where it ran. Two reports with the same id used the same endpoint. `Cost` is an estimate from a table of published rates, or says that the model is not priced. `Generated` is the time in UTC.

The notes under the table are the part to read every time:

- `Document content left this machine.` The endpoint is not a local address. Use a local endpoint if that is not acceptable for these documents.
- `Document content was handed to a program on this machine`. A command answered instead of an HTTP endpoint. The tool cannot see what that program did with the text.
- `The model was permitted to reach the network`. The model was given web tools, as `--fidelity sourced` does, so a search or page request it made may have carried text from your documents to a third party. A `Retrieval` row says what was permitted and what was observed.
- `N unit(s) of work errored.` The run is inconclusive and exits 2.
- `Preflight window guard ran for ...` This is the normal case: each prompt was measured against the model's context window before it was sent. If the note says the window was `stated, not measured`, the size came from `--window` and nothing confirmed it.

**What to do.** Keep the report with the merged document. If the content was not supposed to leave the machine and a note says it did, treat the documents as disclosed.

## JSON, HTML and the web interface

All four forms are built from the same run, so the claims, counts and exit code agree.

**JSON (`--json PATH`).** The complete report for a script. `exit_code` holds the code. `findings`, `review_queue`, `declarations`, `additions`, `attributions`, `number_format`, `structural`, `unusable` (not graded) and `truncations` (length capped) correspond to the sections above. `claims` and `verdicts` hold the whole inventory, `coverage` the counts, and `provenance` the provenance. Files appear under the tool's own names, `source_a.md`, `source_b.md` and `merged.md`, with `documents` mapping them to your paths, and an invented claim is called `hallucinated`. The JSON does not contain the merged text.

**HTML (`--html PATH`).** One self-contained file that opens from disk with no network. It has a coloured banner with the result in a word and the exit code (`Clean`, `Findings`, `Record findings` or `Inconclusive`), a table of contents, a filter box, and the same sections in the same order as the Markdown report. On a run that exits 2 because claims were not graded, the banner says so and the Not graded section lists those claims.

**The web interface.** The result page shows the verdict as a banner, the merged document, and the report as tabs:

| Tab | Corresponds to |
|---|---|
| What needs your attention | An index of every item that needs a decision. Shown only when there is one. |
| Conflicts | Findings other than drops, and most Structure findings |
| Omitted content | Dropped and partly dropped claims, missing segments, and every `dropped` declaration, confirmed or not |
| Attributions, Number format, Added from outside your documents | The sections of the same names. Shown only when they have content. |
| Claims | Inventory |
| What was checked | Coverage, the mechanical checks, and Provenance |

The banner words are `Passed every check` (exit 0), `Needs your review` (1), `Document passed, notes are off` (3) and `Not cleared` (2). `View report` opens the HTML report, `Download report` saves it, and `Download everything` saves a zip with the sources, the merged document, the JSON report and the HTML report. When claims were not graded, the What was checked tab lists them under its coverage row, with the direction of each check and what was wrong with the answer. The rest of the page is described in [The web interface](web.md).

## Details for reviewers

- **One source for every figure.** The HTML report takes its numbers, its verdict sentence and its status words from the code that renders the Markdown report. The counts in each Inventory heading are counted from the rows under it, and a report whose Inventory and Coverage counts differ is refused, not printed.
- **Prompt digests.** A `Prompt` row is the SHA-256 of the prompt file plus the fragments that run included, such as the rules for the fidelity level. For the merge and verify prompts it therefore differs from `sha256sum` of the file on disk.
- **Endpoint ids.** The id is a digest of the endpoint's address, or of the name in `LLOSSLESS_ENDPOINT_LABEL` when that variable is set. The address itself is never written to a report.
- **Quantisation is not recorded.** The report names the model id and not its quantisation. For the published figures it is stated under [Reference configuration](results.md#reference-configuration).
