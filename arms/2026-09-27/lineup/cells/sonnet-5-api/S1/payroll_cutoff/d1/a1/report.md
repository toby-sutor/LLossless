## Verdict

**2 finding(s).** In the claims: 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 15 |
| Claims extracted from `source_a.md` | 15 |
| Claims extracted from `source_b.md` | 9 |
| Forward — source claims accounted for in the merge | **22/24** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **15/15** |
| Forward — `source_b.md` claims accounted for | **7/9** |
| Reverse — merge claims found in a source | **15/15** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **38/39** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-002** -- the two documents disagree
  - `source_b.md:9` says: Totals must be submitted by 15:00 on the 20th of the month.
  - `merged.md` says: 'Totals must be submitted by 12:00 on the 18th of the month.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states a different time (12:00) and date (18th) than the claim's 15:00 on the 20th.
- **B-004** -- the two documents disagree
  - `source_b.md:12` says: If the 20th falls on a weekend, the cut-off moves to the following Monday.
  - `merged.md` says: 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text ties the rule to the 18th and moves the cut-off to the prior working day, not to the following Monday after the 20th.

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
| 1 | Team leads submit timesheet totals for hourly staff. | 5 | carried | 'Team leads who submit timesheet totals for hourly staff.' in `merged.md` -- Directly stated in the 'Who this is for' section. |
| 2 | Totals must be submitted by 12:00 on the 18th of the month. | 10 | carried | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- Exact match to the monthly cut-off statement. |
| 3 | The 18th is a hard cut-off, not a target. | 10 | carried | 'The 18th is a hard cut-off, not a target' in `merged.md` -- Directly stated. |
| 4 | Submissions that arrive after the cut-off are held for the following month's run. | 11 | carried | "submissions that arrive after it are held for the following month's run" in `merged.md` -- Directly stated. |
| 5 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it. | 14 | carried | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- Directly stated. |
| 6 | One file must be submitted per team. | 19 | carried | 'Submit one file per team' in `merged.md` -- Directly stated in the What to submit section. |
| 7 | The file must list every hourly worker with hours. | 19 | carried | 'listing every hourly worker with hours and the cost centre the hours are charged to' in `merged.md` -- Directly stated. |
| 8 | The file must list the cost centre the hours are charged to. | 20 | carried | 'listing every hourly worker with hours and the cost centre the hours are charged to' in `merged.md` -- Directly stated including cost centre requirement. |
| 9 | Blank rows are rejected by the upload page. | 20 | carried | 'Blank rows are rejected by the upload page.' in `merged.md` -- Directly stated. |
| 10 | A correction submitted before the cut-off replaces the earlier file entirely. | 25 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- Directly stated. |
| 11 | After the cut-off, corrections go to the payroll inbox as a written request. | 26 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- Directly stated. |
| 12 | Corrections submitted after the cut-off are applied to the following month. | 27 | carried | 'and are applied to the following month' in `merged.md` -- Directly stated in the Corrections section. |
| 13 | If the upload page is unavailable in the hour before the cut-off, email the payroll team. | 31 | carried | 'email the payroll team and keep the file' in `merged.md` -- Directly stated in Escalation section. |
| 14 | If the upload page is unavailable in the hour before the cut-off, keep the file. | 32 | carried | 'email the payroll team and keep the file' in `merged.md` -- Directly stated in Escalation section. |
| 15 | Do not send totals in the body of an email. | 32 | carried | 'Do not send totals in the body of an email.' in `merged.md` -- Directly stated. |

### `source_b.md` -- 9 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | Totals must be submitted by 15:00 on the 20th of the month. | 9 | contradicted | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The reference text states a different time (12:00) and date (18th) than the claim's 15:00 on the 20th. |
| 4 | If the 20th falls on a weekend, the cut-off moves to the following Monday. | 12 | contradicted | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The reference text ties the rule to the 18th and moves the cut-off to the prior working day, not to the following Monday after the 20th. |
| 1 | Team leads submit timesheet totals for hourly staff. | 5 | carried | 'Team leads who submit timesheet totals for hourly staff.' in `merged.md` -- Same fact as stated in the reference text. |
| 3 | Submissions that arrive after the cut-off are held for the following month's run. | 9 | carried | "submissions that arrive after it are held for the following month's run" in `merged.md` -- Directly stated. |
| 5 | Teams must submit one file per team listing every hourly worker with hours and the cost centre the hours are charged to. | 16 | carried | 'Submit one file per team, listing every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- Directly stated in full. |
| 6 | A correction submitted before the cut-off replaces the earlier file entirely. | 21 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- Directly stated. |
| 7 | After the cut-off, corrections go to the payroll inbox as a written request. | 22 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- Directly stated. |
| 8 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | 26 | carried | 'Teams without terminal access may send paper timesheets to the payroll office by internal post' in `merged.md` -- Directly stated. |
| 9 | Paper timesheets sent by internal post must arrive no later than the cut-off. | 27 | carried | 'to arrive no later than the cut-off' in `merged.md` -- Directly stated as part of the Paper timesheets section. |

### `merged.md` -- 15 claim(s): 0 invented, 0 contradicted, 0 supported in part, 15 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Team leads submit timesheet totals for hourly staff. | supported | `source_a.md` | 'Team leads who submit timesheet totals for hourly staff.' in `source_a.md` -- Both sources describe the audience as team leads submitting timesheet totals for hourly staff. |
| 2 | Totals must be submitted by 12:00 on the 18th of the month. | supported | `source_a.md` | 'Totals must be submitted by 12:00 on the 18th of the month.' in `source_a.md` -- Source_a states this exact deadline. |
| 3 | The 18th is a hard cut-off, not a target. | supported | `source_a.md` | 'The 18th is a hard cut-off, not a target.' in `source_a.md` -- Directly stated in source_a. |
| 4 | Submissions that arrive after the 18th cut-off are held for the following month's run. | supported | `source_a.md` | "Submissions that arrive after it are held for the following month's run." in `source_a.md` -- Matches source_a's statement about late submissions. |
| 5 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it. | supported | `source_a.md` | 'If the 18th falls on a weekend or a public holiday, the cutoff moves to the last working day before it.' in `source_a.md`, **transcription_error** -- Directly stated in source_a (quoted with original wording). |
| 6 | Team leads submit one file per team, listing every hourly worker with hours and the cost centre the hours are charged to. | supported | `source_a.md` | 'Submit one file per team. The file must list every hourly worker with hours and\nthe cost centre the hours are charged to.' in `source_a.md` -- Matches source_a's submission instructions. |
| 7 | Blank rows are rejected by the upload page. | supported | `source_a.md` | 'Blank rows are rejected by the upload page.' in `source_a.md` -- Directly stated in source_a. |
| 8 | A correction submitted before the cut-off replaces the earlier file entirely. | supported | `source_a.md` | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `source_a.md` -- Directly stated in source_a. |
| 9 | After the cut-off, corrections go to the payroll inbox as a written request. | supported | `source_a.md` | 'After the cut-off, corrections go to the payroll inbox as a written request and\nare applied to the following month.' in `source_a.md` -- Matches source_a's statement about post-cutoff correction handling. |
| 10 | Corrections submitted after the cut-off are applied to the following month. | supported | `source_a.md` | 'After the cut-off, corrections go to the payroll inbox as a written request and\nare applied to the following month.' in `source_a.md` -- Source_a explicitly states corrections after cutoff are applied to the following month. |
| 11 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | supported | `source_b.md` | 'Teams without terminal access may send paper timesheets to the payroll office by\ninternal post, to arrive no later than the cut-off.' in `source_b.md` -- Directly stated in source_b. |
| 12 | Paper timesheets must arrive no later than the cut-off. | supported | `source_b.md` | 'to arrive no later than the cut-off.' in `source_b.md` -- Directly stated in source_b as part of the paper timesheet instructions. |
| 13 | If the upload page is unavailable in the hour before the cut-off, team leads should email the payroll team. | supported | `source_a.md` | 'If the upload page is unavailable in the hour before the cut-off, email the\npayroll team and keep the file.' in `source_a.md` -- Directly stated in source_a's escalation section. |
| 14 | If the upload page is unavailable in the hour before the cut-off, team leads should keep the file. | supported | `source_a.md` | 'If the upload page is unavailable in the hour before the cut-off, email the\npayroll team and keep the file.' in `source_a.md` -- Directly stated in source_a's escalation section. |
| 15 | Totals should not be sent in the body of an email. | supported | `source_a.md` | 'Do not send totals in the body of an email.' in `source_a.md` -- Directly stated in source_a. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **15** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **24**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 5 run(s) over 13 attributed segment(s) — sources interleaved. 12 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **16** departure(s) from its sources. Checking them confirms 16, rejects 0, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 33 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept; 2025 title not used. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Payroll Submission Deadlines (2026 Schedule)' and says so (no claim traced to it) |
| `b2` | duplicate | Same heading consolidated under base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b3` | duplicate | Same audience statement as a3. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `a7` | reworded | Joined with adjacent cut-off sentences into one paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a8` | reworded | Joined with adjacent cut-off sentences into one paragraph. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `b4` | duplicate | Same heading consolidated under base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b5` | superseded | Chose 2026 cut-off value over 2025's. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`) |
| `b6` | duplicate | Same hold-over rule as a8. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-003`) |
| `b7` | superseded | Chose 2026 weekend/holiday rule over 2025's. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-004`) |
| `a11` | reworded | Merged with a12 into a single sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`) |
| `a12` | subsumed | Content merged into the combined submission sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-007`, `A-008`) |
| `b8` | duplicate | Same heading consolidated under base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b9` | duplicate | Same submission instruction as a11+a12. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`) |
| `b10` | duplicate | Same heading consolidated under base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b11` | duplicate | Same correction rule as a15. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-006`) |
| `b12` | duplicate | Narrower version of a16's fuller instruction. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 19,167 in, 19,716 out |
| Cost | ~$0.24 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 161.2s |
| Generated | 2026-09-27T16:25:57+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
