## Verdict

**2 finding(s).** In the claims: 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 15 |
| Claims extracted from `source_a.md` | 15 |
| Claims extracted from `source_b.md` | 12 |
| Forward — source claims accounted for in the merge | **25/27** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **15/15** |
| Forward — `source_b.md` claims accounted for | **10/12** |
| Reverse — merge claims found in a source | **15/15** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **42/42** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:9` says: Timesheet totals must be submitted by 15:00 on the 20th of the month.
  - `merged.md` says: 'Totals must be submitted by 12:00 on the 18th of the month.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives a different submission deadline from 15:00 on the 20th.
- **B-003** -- the two documents disagree
  - `source_b.md:12` says: If the 20th falls on a weekend, the cut-off moves to the following Monday.
  - `merged.md` says: 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference specifies a different weekend adjustment for the monthly cut-off.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 15 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 15 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Payroll totals must be submitted by 12:00 on the 18th of the month. | 10 | carried | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The reference gives the same submission deadline. |
| 2 | The 18th is a hard cut-off, not a target. | 10 | carried | 'The 18th is a hard cut-off, not a target.' in `merged.md` -- The reference states this explicitly. |
| 3 | Submissions that arrive after the 18th are held for the following month's run. | 11 | carried | "Submissions that arrive after it are held for the following month's run." in `merged.md` -- “It” refers to the 18th, and the reference states the stated consequence. |
| 4 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before the 18th. | 14 | carried | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The reference states the same condition and adjustment. |
| 5 | One file must be submitted per team. | 19 | carried | 'Submit one file per team.' in `merged.md` -- The reference requires one file per team. |
| 6 | The file must list every hourly worker. | 19 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The reference explicitly requires every hourly worker to be listed. |
| 7 | The file must list the hours for every hourly worker. | 19 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The reference requires the file to list each hourly worker with their hours. |
| 8 | The file must list the cost centre that the hours are charged to for every hourly worker. | 19 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The reference requires listing the cost centre to which the hours are charged. |
| 9 | Blank rows are rejected by the upload page. | 20 | carried | 'Blank rows are rejected by the upload page.' in `merged.md` -- The reference states this explicitly. |
| 10 | A correction submitted before the cut-off replaces the earlier file entirely. | 25 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- The reference states the same correction rule. |
| 11 | After the cut-off, corrections go to the payroll inbox as a written request. | 26 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The reference specifies both the destination and written-request format. |
| 12 | Corrections submitted after the cut-off are applied to the following month. | 26 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.' in `merged.md` -- The reference states that post-cut-off corrections are applied to the following month. |
| 13 | If the upload page is unavailable in the hour before the cut-off, the payroll team must be emailed. | 31 | carried | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team' in `merged.md` -- The reference instructs users to email the payroll team under that condition. |
| 14 | If the upload page is unavailable in the hour before the cut-off, the file must be kept. | 31 | carried | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file.' in `merged.md` -- The reference instructs users to keep the file under that condition. |
| 15 | Totals must not be sent in the body of an email. | 32 | carried | 'Do not send totals in the body of an email.' in `merged.md` -- The reference explicitly prohibits sending totals in an email body. |

### `source_b.md` -- 12 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Timesheet totals must be submitted by 15:00 on the 20th of the month. | 9 | contradicted | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The reference gives a different submission deadline from 15:00 on the 20th. |
| 3 | If the 20th falls on a weekend, the cut-off moves to the following Monday. | 12 | contradicted | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The reference specifies a different weekend adjustment for the monthly cut-off. |
| 2 | Submissions that arrive after the cut-off are held for the following month's run. | 9 | carried | "Submissions that arrive after it are held for the following month's run." in `merged.md` -- The reference states that submissions arriving after the cut-off are held for the following month's run. |
| 4 | Each team must submit one file. | 16 | carried | 'Submit one file per team.' in `merged.md` -- The reference requires one file per team. |
| 5 | Each team file must list every hourly worker and their hours. | 16 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The reference requires every hourly worker and their hours to be listed. |
| 6 | Each team file must list the cost centre the hours are charged to. | 16 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The reference requires the file to list the cost centre to which the hours are charged. |
| 7 | A correction submitted before the cut-off replaces the earlier file entirely. | 21 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- The reference states the same correction rule. |
| 8 | Corrections submitted after the cut-off go to the payroll inbox. | 22 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The reference states that post-cut-off corrections go to the payroll inbox. |
| 9 | Corrections submitted after the cut-off are written requests. | 22 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The reference specifies that post-cut-off corrections are written requests. |
| 10 | Teams without terminal access may send paper timesheets. | 26 | carried | 'Teams without terminal access may send paper timesheets to the payroll office by internal post, to arrive no later than the cut-off.' in `merged.md` -- The reference says teams without terminal access may send paper timesheets. |
| 11 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | 26 | carried | 'Teams without terminal access may send paper timesheets to the payroll office by internal post' in `merged.md` -- The text explicitly permits teams without terminal access to send paper timesheets to the payroll office by internal post. |
| 12 | Paper timesheets must arrive no later than the cut-off. | 27 | carried | 'to arrive no later than the cut-off' in `merged.md` -- The text says the paper timesheets must arrive no later than the cut-off. |

### `merged.md` -- 15 claim(s): 0 invented, 0 contradicted, 0 supported in part, 15 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Totals must be submitted by 12:00 on the 18th of the month. | supported | `source_a.md` | 'Totals must be submitted by 12:00 on the 18th of the month.' in `source_a.md` -- Source A states this deadline directly. |
| 2 | The 18th is a hard cut-off, not a target. | supported | `source_a.md` | 'The 18th is a hard\ncut-off, not a target.' in `source_a.md` -- Source A describes the 18th as a hard cut-off, not a target. |
| 3 | Submissions that arrive after the cut-off are held for the following month's run. | supported | `source_b.md` | "Submissions that\narrive after the cut-off are held for the following month's run." in `source_b.md` -- Source B states that submissions after the cut-off are held for the following month's run. |
| 4 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before the 18th. | supported | `source_a.md` | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the\nlast working day before it.' in `source_a.md` -- Source A states this weekend and public-holiday adjustment. |
| 5 | One file must be submitted per team. | supported | `source_a.md` | 'Submit one file per team.' in `source_a.md` -- Source A directly requires one file per team. |
| 6 | The file must list every hourly worker with hours and the cost centre the hours are charged to. | supported | `source_a.md` | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `source_a.md` -- Source A specifies all the listed file contents. |
| 7 | The upload page rejects blank rows. | supported | `source_a.md` | 'Blank rows are rejected by the upload page.' in `source_a.md` -- Source A directly states that the upload page rejects blank rows. |
| 8 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | supported | `source_b.md` | 'Teams without terminal access may send paper timesheets to the payroll office by\ninternal post,' in `source_b.md` -- Source B permits teams without terminal access to send paper timesheets by internal post. |
| 9 | Paper timesheets sent by teams without terminal access must arrive no later than the cut-off. | supported | `source_b.md` | 'Teams without terminal access may send paper timesheets to the payroll office by\ninternal post, to arrive no later than the cut-off.' in `source_b.md` -- Source B says these paper timesheets must arrive no later than the cut-off. |
| 10 | A correction submitted before the cut-off replaces the earlier file entirely. | supported | `source_a.md` | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `source_a.md` -- Source A directly states this correction rule. |
| 11 | After the cut-off, corrections go to the payroll inbox as a written request. | supported | `source_b.md` | 'After the cut-off, corrections go to the payroll inbox as a written request.' in `source_b.md` -- Source B directly states where and how after-cut-off corrections are sent. |
| 12 | Corrections submitted after the cut-off are applied to the following month. | supported | `source_a.md` | 'After the cut-off, corrections go to the payroll inbox as a written request and\nare applied to the following month.' in `source_a.md` -- Source A states that after-cut-off corrections are applied to the following month. |
| 13 | If the upload page is unavailable in the hour before the cut-off, the payroll team must be emailed. | supported | `source_a.md` | 'If the upload page is unavailable in the hour before the cut-off, email the\npayroll team' in `source_a.md` -- Source A instructs staff to email the payroll team in this situation. |
| 14 | If the upload page is unavailable in the hour before the cut-off, the file must be kept. | supported | `source_a.md` | 'keep the file.' in `source_a.md` -- Source A instructs staff to keep the file if the upload page is unavailable in that hour. |
| 15 | Totals must not be sent in the body of an email. | supported | `source_a.md` | 'Do not send totals in the body of an email.' in `source_a.md` -- Source A directly prohibits sending totals in an email body. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **15** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **27**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 14 attributed segment(s) — sources interleaved. 11 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **23** departure(s) from its sources. Checking them confirms 21, rejects 1, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 33 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Audience: flattened the source line break. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a6` | reworded | Monthly cut-off: flattened the source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a7` | reworded | Monthly cut-off: flattened the source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a8` | reworded | Monthly cut-off: flattened the source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a9` | reworded | Monthly cut-off: flattened the source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `a12` | reworded | What to submit: flattened the source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`, `A-007`, `A-008`) |
| `a13` | reworded | What to submit: flattened the source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`) |
| `a16` | reworded | Corrections: flattened the source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`, `A-012`) |
| `a18` | reworded | Escalation: flattened the source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-013`, `A-014`) |
| `b1` | superseded | Title: the base document's 2026 title is chosen. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Payroll Submission Deadlines (2026 Schedule)' and says so (no claim traced to it) |
| `b2` | duplicate | Audience heading: the same heading appears in the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b3` | duplicate | Audience: the same fact appears in the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b4` | duplicate | Cut-off heading: the same heading appears in the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b5` | superseded | Monthly cut-off: the base document's deadline is chosen. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b6` | duplicate | Monthly cut-off: the same late-submission rule appears in the base. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`) |
| `b7` | superseded | Monthly cut-off: the base document's weekend rule is chosen. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`) |
| `b8` | duplicate | Submission heading: the same heading appears in the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b9` | duplicate | What to submit: the base already states these requirements. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `b10` | duplicate | Corrections heading: the same heading appears in the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b11` | duplicate | Corrections: the same rule appears in the base. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `b12` | duplicate | Corrections: the base states this rule and its timing. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`, `B-009`) |
| `b13` | subsumed | Submission heading: its content is placed under What to submit. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b14` | reworded | What to submit: flattened the source line break. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`, `B-011`, `B-012`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-luna |
| Model (decompose) | gpt-6-luna |
| Model (verify) | gpt-6-luna |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 15,232 in, 15,221 out, 0 cached, 9,018 reasoning |
| Cost | ~$0.01 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 113.4s |
| Generated | 2026-09-27T15:41:40+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
