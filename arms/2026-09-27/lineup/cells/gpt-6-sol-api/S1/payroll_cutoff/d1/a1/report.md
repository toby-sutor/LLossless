## Verdict

**2 finding(s).** In the claims: 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 17 |
| Claims extracted from `source_a.md` | 17 |
| Claims extracted from `source_b.md` | 11 |
| Forward — source claims accounted for in the merge | **26/28** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **17/17** |
| Forward — `source_b.md` claims accounted for | **9/11** |
| Reverse — merge claims found in a source | **17/17** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **45/45** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:9` says: Timesheet totals must be submitted by 15:00 on the 20th of the month.
  - `merged.md` says: 'Totals must be submitted by 12:00 on the 18th of the month.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated deadline is 12:00 on the 18th, not 15:00 on the 20th.
- **B-003** -- the two documents disagree
  - `source_b.md:12` says: If the 20th falls on a weekend, the cut-off moves to the following Monday.
  - `merged.md` says: 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The weekend rule concerns the 18th and moves the cut-off earlier, not to the following Monday.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 17 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 17 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | This page is for team leads who submit timesheet totals for hourly staff. | 5 | carried | 'Team leads who submit timesheet totals for hourly staff.' in `merged.md` -- The page identifies those team leads as its audience. |
| 2 | Salaried staff are not covered by this page. | 5 | carried | 'Salaried staff are not covered by this page.' in `merged.md` -- The reference states this exclusion directly. |
| 3 | Totals must be submitted by 12:00 on the 18th of the month. | 10 | carried | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The stated submission deadline matches the claim. |
| 4 | The 18th is a hard cut-off, not a target. | 10 | carried | 'The 18th is a hard cut-off, not a target.' in `merged.md` -- The reference states this directly. |
| 5 | Submissions that arrive after the cut-off are held for the following month's run. | 11 | carried | "Submissions that arrive after it are held for the following month's run." in `merged.md` -- Here, “it” refers to the cut-off. |
| 6 | If the 18th falls on a weekend, the cut-off moves to the last working day before the 18th. | 14 | carried | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The stated rule includes weekends and moves the cut-off to the preceding working day. |
| 7 | If the 18th falls on a public holiday, the cut-off moves to the last working day before the 18th. | 14 | carried | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The stated rule includes public holidays and moves the cut-off to the preceding working day. |
| 8 | One file must be submitted per team. | 19 | carried | 'Submit one file per team.' in `merged.md` -- The reference requires one file per team. |
| 9 | The file must list every hourly worker with hours. | 19 | carried | 'The file must list every hourly worker with hours' in `merged.md` -- The reference requires the file to list every hourly worker with hours. |
| 10 | The file must list the cost centre the hours are charged to. | 20 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The required file contents include the cost centre charged for the hours. |
| 11 | Blank rows are rejected by the upload page. | 20 | carried | 'Blank rows are rejected by the upload page.' in `merged.md` -- The reference states this directly. |
| 12 | A correction submitted before the cut-off replaces the earlier file entirely. | 25 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- The reference states this directly. |
| 13 | After the cut-off, corrections go to the payroll inbox as a written request. | 26 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The reference gives the same destination and format for late corrections. |
| 14 | Corrections submitted after the cut-off are applied to the following month. | 27 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.' in `merged.md` -- The reference says corrections after the cut-off are applied to the following month. |
| 15 | If the upload page is unavailable in the hour before the cut-off, email the payroll team. | 31 | carried | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file.' in `merged.md` -- The stated contingency includes emailing the payroll team. |
| 16 | If the upload page is unavailable in the hour before the cut-off, keep the file. | 31 | carried | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file.' in `merged.md` -- The stated contingency includes keeping the file. |
| 17 | Do not send totals in the body of an email. | 32 | carried | 'Do not send totals in the body of an email.' in `merged.md` -- The reference states this prohibition directly. |

### `source_b.md` -- 11 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Timesheet totals must be submitted by 15:00 on the 20th of the month. | 9 | contradicted | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The stated deadline is 12:00 on the 18th, not 15:00 on the 20th. |
| 3 | If the 20th falls on a weekend, the cut-off moves to the following Monday. | 12 | contradicted | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The weekend rule concerns the 18th and moves the cut-off earlier, not to the following Monday. |
| 2 | Submissions that arrive after the cut-off are held for the following month's run. | 9 | carried | "Submissions that arrive after it are held for the following month's run." in `merged.md` -- The reference says submissions arriving after the cut-off are held for the following month's run. |
| 4 | One file must be submitted per team. | 16 | carried | 'Submit one file per team.' in `merged.md` -- The reference requires one file per team. |
| 5 | The file must list every hourly worker. | 16 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The required file contents include every hourly worker. |
| 6 | The file must list hours for every hourly worker. | 16 | carried | 'The file must list every hourly worker with hours' in `merged.md` -- Requiring every hourly worker to be listed with hours supports the claim. |
| 7 | The file must list the cost centre the hours are charged to. | 16 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The required file contents include the cost centre charged for the hours. |
| 8 | A correction submitted before the cut-off replaces the earlier file entirely. | 21 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- The reference states this directly. |
| 9 | After the cut-off, corrections go to the payroll inbox as a written request. | 22 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The reference states exactly where and how corrections are submitted after the cut-off. |
| 10 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | 26 | carried | 'Teams without terminal access may send paper timesheets to the payroll office by internal post' in `merged.md` -- The reference expressly permits this submission method for teams without terminal access. |
| 11 | Paper timesheets sent by teams without terminal access must arrive no later than the cut-off. | 27 | carried | 'Teams without terminal access may send paper timesheets to the payroll office by internal post, to arrive no later than the cut-off.' in `merged.md` -- The reference states the arrival deadline for those paper timesheets. |

### `merged.md` -- 17 claim(s): 0 invented, 0 contradicted, 0 supported in part, 17 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Team leads submit timesheet totals for hourly staff. | supported | `source_a.md` | 'Team leads who submit timesheet totals for hourly staff.' in `source_a.md` -- The source identifies team leads as the people who submit timesheet totals for hourly staff. |
| 2 | Totals must be submitted by 12:00 on the 18th of the month. | supported | `source_a.md` | 'Totals must be submitted by 12:00 on the 18th of the month.' in `source_a.md` -- The source states this deadline. |
| 3 | The 18th is a hard cut-off, not a target. | supported | `source_a.md` | 'The 18th is a hard\ncut-off, not a target.' in `source_a.md` -- The source explicitly describes the 18th as a hard cut-off. |
| 4 | Submissions that arrive after the cut-off are held for the following month's run. | supported | `source_b.md` | "Submissions that\narrive after the cut-off are held for the following month's run." in `source_b.md` -- The source states what happens to submissions arriving after the cut-off. |
| 5 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before the 18th. | supported | `source_a.md` | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the\nlast working day before it.' in `source_a.md` -- In context, “it” refers to the 18th. |
| 6 | One file must be submitted per team. | supported | `source_a.md` | 'Submit one file per team.' in `source_a.md` -- The source requires one file per team. |
| 7 | The file must list every hourly worker with hours. | supported | `source_a.md` | 'The file must list every hourly worker with hours' in `source_a.md` -- The source specifies that each hourly worker and their hours must be listed. |
| 8 | The file must list the cost centre the hours are charged to. | supported | `source_a.md` | 'the cost centre the hours are charged to' in `source_a.md` -- This is part of the source's required file contents. |
| 9 | Blank rows are rejected by the upload page. | supported | `source_a.md` | 'Blank rows are rejected by the upload\npage.' in `source_a.md` -- The source explicitly states that the upload page rejects blank rows. |
| 10 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | supported | `source_b.md` | 'Teams without terminal access may send paper timesheets to the payroll office by\ninternal post' in `source_b.md` -- The source permits this submission method for teams without terminal access. |
| 11 | Paper timesheets sent to the payroll office by internal post must arrive no later than the cut-off. | supported | `source_b.md` | 'Teams without terminal access may send paper timesheets to the payroll office by\ninternal post, to arrive no later than the cut-off.' in `source_b.md` -- The source gives the cut-off as the latest arrival time for those paper timesheets. |
| 12 | A correction submitted before the cut-off replaces the earlier file entirely. | supported | `source_a.md` | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `source_a.md` -- The source states the replacement rule for corrections submitted before the cut-off. |
| 13 | After the cut-off, corrections go to the payroll inbox as a written request. | supported | `source_a.md` | 'After the cut-off, corrections go to the payroll inbox as a written request' in `source_a.md` -- The source specifies where and how to send corrections after the cut-off. |
| 14 | After the cut-off, corrections are applied to the following month. | supported | `source_a.md` | 'After the cut-off, corrections go to the payroll inbox as a written request and\nare applied to the following month.' in `source_a.md` -- The source states that corrections after the cut-off are applied to the following month. |
| 15 | If the upload page is unavailable in the hour before the cut-off, email the payroll team. | supported | `source_a.md` | 'If the upload page is unavailable in the hour before the cut-off, email the\npayroll team and keep the file.' in `source_a.md` -- The source directs team leads to email the payroll team under this condition. |
| 16 | If the upload page is unavailable in the hour before the cut-off, keep the file. | supported | `source_a.md` | 'If the upload page is unavailable in the hour before the cut-off, email the\npayroll team and keep the file.' in `source_a.md` -- The source directs team leads to keep the file under this condition. |
| 17 | Totals must not be sent in the body of an email. | supported | `source_a.md` | 'Do not send totals in the body of an email.' in `source_a.md` -- The source explicitly prohibits sending totals in an email body. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **17** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **28**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 14 attributed segment(s) — sources interleaved. 11 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **22** departure(s) from its sources. Checking them confirms 21, rejects 0, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 33 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | The scope statement is set as one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a7` | reworded | The cut-off statement is set as one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `a8` | reworded | The late-submission statement is set as one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-005`) |
| `a9` | reworded | The non-working-day rule is set as one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`, `A-007`) |
| `a12` | reworded | The file requirements are set as one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`, `A-010`) |
| `a13` | reworded | The upload restriction is set as one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `a16` | reworded | The post-cut-off correction rule is set as one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-013`, `A-014`) |
| `a18` | reworded | The escalation instruction is set as one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-015`, `A-016`) |
| `b1` | superseded | The title uses the base document's schedule. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Payroll Submission Deadlines (2026 Schedule)' and says so (no claim traced to it) |
| `b2` | duplicate | The base already supplies this heading. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b3` | duplicate | The base already states the audience. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b4` | duplicate | The base already supplies this heading. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b5` | superseded | The base supplies the cut-off for the chosen schedule. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b6` | duplicate | The base already states the late-submission rule. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`) |
| `b7` | superseded | The base supplies the non-working-day rule for the chosen schedule. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`) |
| `b8` | duplicate | The base already supplies this heading. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b9` | superseded | The base wording states the same file requirements. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-004`, `B-005`, `B-006`, `B-007`) |
| `b10` | duplicate | The base already supplies this heading. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b11` | duplicate | The base already states the pre-cut-off correction rule. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `b12` | subsumed | The base adds when written corrections are applied. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-009`) |
| `b13` | superseded | Paper timesheets belong under the base submission heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b14` | reworded | The paper-timesheet option is set as one prose line. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-sol |
| Model (decompose) | gpt-6-sol |
| Model (verify) | gpt-6-sol |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 15,277 in, 12,005 out, 0 cached, 4,245 reasoning |
| Cost | ~$0.15 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 127.7s |
| Generated | 2026-09-27T15:39:46+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
