## Verdict

**2 finding(s).** In the claims: 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 17 |
| Claims extracted from `source_a.md` | 15 |
| Claims extracted from `source_b.md` | 11 |
| Forward — source claims accounted for in the merge | **24/26** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **15/15** |
| Forward — `source_b.md` claims accounted for | **9/11** |
| Reverse — merge claims found in a source | **17/17** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **43/43** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-002** -- the two documents disagree
  - `source_b.md:9` says: Timesheet totals must be submitted by 15:00 on the 20th of the month.
  - `merged.md` says: 'Totals must be submitted by 12:00 on the 18th of the month.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text gives 12:00 on the 18th, not 15:00 on the 20th.
- **B-004** -- the two documents disagree
  - `source_b.md:12` says: If the 20th falls on a weekend, the cut-off moves to the following Monday.
  - `merged.md` says: 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text moves the cut-off to the last working day before, on the 18th, not the following Monday after the 20th.

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
| 1 | The payroll submission deadlines page is for team leads who submit timesheet totals for hourly staff. | 5 | carried | 'Team leads who submit timesheet totals for hourly staff.' in `merged.md` -- The 'Who this is for' section names team leads submitting timesheet totals for hourly staff as the audience. |
| 2 | Salaried staff are not covered by the payroll submission deadlines page. | 5 | carried | 'Salaried staff are not covered by this page.' in `merged.md` -- The reference text states directly that salaried staff are not covered. |
| 3 | Timesheet totals must be submitted by 12:00 on the 18th of the month. | 10 | carried | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The reference text states the same time and day. |
| 4 | The 18th is a hard cut-off, not a target. | 10 | carried | 'The 18th is a hard cut-off, not a target' in `merged.md` -- The reference text states this verbatim. |
| 5 | Submissions that arrive after the cut-off are held for the following month's run. | 11 | carried | "submissions that arrive after it are held for the following month's run" in `merged.md` -- Late submissions are held for the following month's run. |
| 6 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before the 18th. | 14 | carried | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The reference text states the same rule for weekends and public holidays. |
| 7 | One file per team must be submitted. | 19 | carried | 'Submit one file per team' in `merged.md` -- The reference text instructs submitting one file per team. |
| 8 | The submitted file must list every hourly worker with hours and the cost centre the hours are charged to. | 19 | carried | 'listing every hourly worker with hours and the cost centre the hours are charged to' in `merged.md` -- The file must list every hourly worker with hours and the cost centre. |
| 9 | Blank rows are rejected by the upload page. | 20 | carried | 'The upload page rejects blank rows.' in `merged.md` -- The reference text states the upload page rejects blank rows. |
| 10 | A correction submitted before the cut-off replaces the earlier file entirely. | 25 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- The reference text states this verbatim. |
| 11 | After the cut-off, corrections go to the payroll inbox as a written request. | 26 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The reference text states that post-cut-off corrections go to the payroll inbox as a written request. |
| 12 | Corrections made after the cut-off are applied to the following month. | 26 | carried | 'are applied to the following month' in `merged.md` -- Post-cut-off corrections are applied to the following month. |
| 13 | If the upload page is unavailable in the hour before the cut-off, team leads should email the payroll team. | 31 | carried | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team' in `merged.md` -- The escalation section instructs emailing the payroll team. |
| 14 | If the upload page is unavailable in the hour before the cut-off, team leads should keep the file. | 31 | carried | 'keep the file' in `merged.md` -- The escalation instruction includes keeping the file. |
| 15 | Totals should not be sent in the body of an email. | 32 | carried | 'Do not send totals in the body of an email.' in `merged.md` -- The reference text states this directly. |

### `source_b.md` -- 11 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | Timesheet totals must be submitted by 15:00 on the 20th of the month. | 9 | contradicted | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The reference text gives 12:00 on the 18th, not 15:00 on the 20th. |
| 4 | If the 20th falls on a weekend, the cut-off moves to the following Monday. | 12 | contradicted | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The reference text moves the cut-off to the last working day before, on the 18th, not the following Monday after the 20th. |
| 1 | The payroll submission guidance is for team leads who submit timesheet totals for hourly staff. | 5 | carried | 'Team leads who submit timesheet totals for hourly staff.' in `merged.md` -- The audience section names the same audience. |
| 3 | Submissions that arrive after the cut-off are held for the following month's run. | 9 | carried | "submissions that arrive after it are held for the following month's run" in `merged.md` -- Late submissions are held for the following month's run. |
| 5 | One file per team should be submitted. | 16 | carried | 'Submit one file per team' in `merged.md` -- The reference text instructs one file per team. |
| 6 | The submitted file lists every hourly worker with hours. | 16 | carried | 'listing every hourly worker with hours' in `merged.md` -- The file lists every hourly worker with hours. |
| 7 | The submitted file lists the cost centre the hours are charged to. | 16 | carried | 'the cost centre the hours are charged to' in `merged.md` -- The file lists the cost centre the hours are charged to. |
| 8 | A correction submitted before the cut-off replaces the earlier file entirely. | 21 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- The reference text states this verbatim. |
| 9 | After the cut-off, corrections go to the payroll inbox as a written request. | 22 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The reference text states this directly. |
| 10 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | 26 | carried | 'Teams without terminal access may send paper timesheets to the payroll office by internal post' in `merged.md` -- The paper timesheets section states this directly. |
| 11 | Paper timesheets sent by internal post must arrive no later than the cut-off. | 26 | carried | 'to arrive no later than the cut-off' in `merged.md` -- Paper timesheets must arrive no later than the cut-off. |

### `merged.md` -- 17 claim(s): 0 invented, 0 contradicted, 0 supported in part, 17 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The payroll submission deadlines page is for team leads who submit timesheet totals for hourly staff. | supported | `source_a.md` | 'Team leads who submit timesheet totals for hourly staff.' in `source_a.md` -- Both sources state the page is for team leads submitting timesheet totals for hourly staff. |
| 2 | Salaried staff are not covered by the payroll submission deadlines page. | supported | `source_a.md` | 'Salaried staff are not\ncovered by this page.' in `source_a.md` -- Source_a states salaried staff are not covered by the page. |
| 3 | Timesheet totals must be submitted by 12:00 on the 18th of the month. | supported | `source_a.md` | 'Totals must be submitted by 12:00 on the 18th of the month.' in `source_a.md` -- Source_a (2026 schedule) states this deadline verbatim; source_b's different 2025 deadline does not negate support from source_a. |
| 4 | The 18th is a hard cut-off, not a target. | supported | `source_a.md` | 'The 18th is a hard\ncut-off, not a target.' in `source_a.md` -- Source_a states the 18th is a hard cut-off, not a target. |
| 5 | Submissions that arrive after the 18th cut-off are held for the following month's run. | supported | `source_a.md` | "Submissions that arrive after it are held for the\nfollowing month's run." in `source_a.md` -- Source_a states submissions after the 18th cut-off are held for the following month's run. |
| 6 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before the 18th. | supported | `source_a.md` | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the\nlast working day before it.' in `source_a.md` -- Source_a states this rule in essentially the same words. |
| 7 | One file per team must be submitted. | supported | `source_a.md` | 'Submit one file per team.' in `source_a.md` -- Both sources require one file per team. |
| 8 | The submitted file lists every hourly worker with hours and the cost centre the hours are charged to. | supported | `source_a.md` | 'The file must list every hourly worker with hours and\nthe cost centre the hours are charged to.' in `source_a.md` -- Source_a states the file lists every hourly worker with hours and cost centre. |
| 9 | The upload page rejects blank rows. | supported | `source_a.md` | 'Blank rows are rejected by the upload\npage.' in `source_a.md` -- Source_a states the upload page rejects blank rows. |
| 10 | A correction submitted before the cut-off replaces the earlier file entirely. | supported | `source_a.md` | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `source_a.md` -- Both sources state this verbatim. |
| 11 | After the cut-off, corrections go to the payroll inbox as a written request. | supported | `source_b.md` | 'After the cut-off, corrections go to the payroll inbox as a written request.' in `source_b.md` -- Source_b states this verbatim, and source_a says the same. |
| 12 | Corrections made after the cut-off are applied to the following month. | supported | `source_a.md` | 'are applied to the following month.' in `source_a.md` -- Source_a states post-cut-off corrections are applied to the following month. |
| 13 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | supported | `source_b.md` | 'Teams without terminal access may send paper timesheets to the payroll office by\ninternal post' in `source_b.md` -- Source_b states teams without terminal access may send paper timesheets by internal post. |
| 14 | Paper timesheets sent by internal post must arrive no later than the cut-off. | supported | `source_b.md` | 'to arrive no later than the cut-off.' in `source_b.md` -- Source_b states paper timesheets must arrive no later than the cut-off. |
| 15 | If the upload page is unavailable in the hour before the cut-off, team leads should email the payroll team. | supported | `source_a.md` | 'If the upload page is unavailable in the hour before the cut-off, email the\npayroll team' in `source_a.md` -- Source_a instructs emailing the payroll team if the upload page is unavailable in the hour before cut-off. |
| 16 | If the upload page is unavailable in the hour before the cut-off, team leads should keep the file. | supported | `source_a.md` | 'and keep the file.' in `source_a.md` -- Source_a instructs keeping the file when the upload page is unavailable before cut-off. |
| 17 | Totals should not be sent in the body of an email. | supported | `source_a.md` | 'Do not send totals in the body of an email.' in `source_a.md` -- Source_a states totals must not be sent in the body of an email. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **17** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **26**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 5 run(s) over 12 attributed segment(s) — sources interleaved. 12 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **22** departure(s) from its sources. Checking them confirms 22, rejects 0, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 33 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Audience section; line wrap removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a7` | reworded | Cut-off; joined with late-submission rule, line wrap removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `a8` | reworded | Cut-off; joined with hard cut-off sentence, line wrap removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-005`) |
| `a9` | reworded | Non-working-day rule; line wrap removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`) |
| `a11` | subsumed | What to submit; source_b's single sentence carries it. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-007`) |
| `a12` | subsumed | What to submit; source_b's single sentence carries it. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-008`) |
| `a13` | reworded | What to submit; recast in active voice. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`) |
| `a16` | reworded | Corrections; line wrap removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`, `A-012`) |
| `a18` | reworded | Escalation; line wrap removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-013`, `A-014`) |
| `b1` | superseded | Title; base 2026 title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Payroll Submission Deadlines (2026 Schedule)' and says so (no claim traced to it) |
| `b2` | duplicate | Same heading as base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b3` | duplicate | Audience; identical to a3. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b4` | duplicate | Same heading as base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b5` | superseded | Cut-off; 2026 base value chosen over 2025 value. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`) |
| `b6` | duplicate | Late submissions; same rule as a8. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-003`) |
| `b7` | superseded | Non-working-day rule; 2026 base rule chosen. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-004`) |
| `b8` | duplicate | Same heading as base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b9` | reworded | What to submit; this wording chosen, line wrap removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`, `B-006`, `B-007`) |
| `b10` | duplicate | Same heading as base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b11` | duplicate | Corrections; identical to a15. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-008`) |
| `b12` | duplicate | Corrections; a16 states this plus when it applies. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-009`) |
| `b14` | reworded | Paper timesheets; line wrap removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 31c2462e2828 (command) -- lineup opus-5.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 -> claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=medium, merge=medium, verify=medium |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 127.0s |
| Generated | 2026-09-27T17:10:36+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
