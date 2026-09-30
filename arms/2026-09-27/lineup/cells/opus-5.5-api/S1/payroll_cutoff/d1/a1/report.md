## Verdict

**2 finding(s).** In the claims: 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 18 |
| Claims extracted from `source_a.md` | 14 |
| Claims extracted from `source_b.md` | 10 |
| Forward — source claims accounted for in the merge | **22/24** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **14/14** |
| Forward — `source_b.md` claims accounted for | **8/10** |
| Reverse — merge claims found in a source | **18/18** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **42/42** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-002** -- the two documents disagree
  - `source_b.md:9` says: Timesheet totals must be submitted by 15:00 on the 20th of the month.
  - `merged.md` says: 'Totals must be submitted by 12:00 on the 18th of the month.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 12:00 on the 18th, not 15:00 on the 20th.
- **B-004** -- the two documents disagree
  - `source_b.md:12` says: If the 20th falls on a weekend, the payroll cut-off moves to the following Monday.
  - `merged.md` says: 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference moves a weekend cut-off to the prior working day, not to the following Monday, and uses the 18th.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 14 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 14 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The payroll submission deadlines page is for team leads who submit timesheet totals for hourly staff. | 5 | carried | 'Team leads who submit timesheet totals for hourly staff.' in `merged.md` -- The 'Who this is for' section states the page's audience as team leads submitting hourly timesheet totals. |
| 2 | Salaried staff are not covered by the payroll submission deadlines page. | 5 | carried | 'Salaried staff are not covered by this page.' in `merged.md` -- The text explicitly excludes salaried staff from the page. |
| 3 | Timesheet totals must be submitted by 12:00 on the 18th of the month. | 10 | carried | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The reference text gives the same time and day for the deadline. |
| 4 | The 18th is a hard cut-off, not a target. | 10 | carried | 'The 18th is a hard cut-off, not a target.' in `merged.md` -- The text states this verbatim. |
| 5 | Submissions that arrive after the cut-off are held for the following month's run. | 11 | carried | "Submissions that arrive after it are held for the following month's run." in `merged.md` -- Here 'it' refers to the cut-off, so the meaning matches the claim. |
| 6 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before the 18th. | 14 | carried | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The text gives the same weekend and holiday rule. |
| 7 | Team leads must submit one file per team. | 19 | carried | 'Submit one file per team.' in `merged.md` -- This instruction, addressed to team leads, requires one file per team. |
| 8 | The submission file must list every hourly worker with hours and the cost centre the hours are charged to. | 19 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The text states the file contents exactly as claimed. |
| 9 | Blank rows are rejected by the upload page. | 20 | carried | 'Blank rows are rejected by the upload page.' in `merged.md` -- The text states this verbatim. |
| 10 | A correction submitted before the cut-off replaces the earlier file entirely. | 25 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- The text states this verbatim. |
| 11 | After the cut-off, corrections go to the payroll inbox as a written request. | 26 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The text states that post-cut-off corrections go to the payroll inbox as written requests. |
| 12 | Corrections made after the cut-off are applied to the following month. | 26 | carried | 'are applied to the following month' in `merged.md` -- Post-cut-off corrections are stated to be applied to the following month. |
| 13 | If the upload page is unavailable in the hour before the cut-off, team leads should email the payroll team and keep the file. | 31 | carried | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file.' in `merged.md` -- The escalation section states this instruction. |
| 14 | Totals must not be sent in the body of an email. | 32 | carried | 'Do not send totals in the body of an email.' in `merged.md` -- The text prohibits sending totals in the email body. |

### `source_b.md` -- 10 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | Timesheet totals must be submitted by 15:00 on the 20th of the month. | 9 | contradicted | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The reference gives 12:00 on the 18th, not 15:00 on the 20th. |
| 4 | If the 20th falls on a weekend, the payroll cut-off moves to the following Monday. | 12 | contradicted | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The reference moves a weekend cut-off to the prior working day, not to the following Monday, and uses the 18th. |
| 1 | The payroll submission deadlines document is intended for team leads who submit timesheet totals for hourly staff. | 5 | carried | 'Team leads who submit timesheet totals for hourly staff.' in `merged.md` -- The 'Who this is for' section states the same intended audience. |
| 3 | Submissions that arrive after the cut-off are held for the following month's run. | 9 | carried | "Submissions that arrive after it are held for the following month's run." in `merged.md` -- Late submissions are held for the following month's run, as the claim says. |
| 5 | Team leads should submit one file per team. | 16 | carried | 'Submit one file per team.' in `merged.md` -- The reference instructs one file per team. |
| 6 | The submitted file lists every hourly worker with hours and the cost centre the hours are charged to. | 16 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The file contents stated match the claim. |
| 7 | A correction submitted before the cut-off replaces the earlier file entirely. | 21 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- The text states this verbatim. |
| 8 | After the cut-off, corrections go to the payroll inbox as a written request. | 22 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The text states this verbatim. |
| 9 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | 26 | carried | 'Teams without terminal access may send paper timesheets to the payroll office by internal post' in `merged.md` -- The paper timesheets section states this. |
| 10 | Paper timesheets must arrive at the payroll office no later than the cut-off. | 26 | carried | 'to arrive no later than the cut-off' in `merged.md` -- Paper timesheets sent to the payroll office must arrive no later than the cut-off. |

### `merged.md` -- 18 claim(s): 0 invented, 0 contradicted, 0 supported in part, 18 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The payroll submission deadlines page is for team leads who submit timesheet totals for hourly staff. | supported | `source_a.md` | 'Team leads who submit timesheet totals for hourly staff.' in `source_a.md` -- Source A's 'Who this is for' section states the page is for these team leads. |
| 2 | Salaried staff are not covered by the payroll submission deadlines page. | supported | `source_a.md` | 'Salaried staff are not\ncovered by this page.' in `source_a.md` -- Source A explicitly excludes salaried staff from the page. |
| 3 | Timesheet totals must be submitted by 12:00 on the 18th of the month. | supported | `source_a.md` | 'Totals must be submitted by 12:00 on the 18th of the month.' in `source_a.md` -- Source A's 2026 schedule states this deadline; source B's 15:00 on the 20th belongs to the separate 2025 schedule. |
| 4 | The 18th is a hard cut-off, not a target. | supported | `source_a.md` | 'The 18th is a hard\ncut-off, not a target.' in `source_a.md` -- Source A states this verbatim. |
| 5 | Submissions that arrive after the 18th cut-off are held for the following month's run. | supported | `source_a.md` | "Submissions that arrive after it are held for the\nfollowing month's run." in `source_a.md` -- Source A states that late submissions are held for the following month's run. |
| 6 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before the 18th. | supported | `source_a.md` | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the\nlast working day before it.' in `source_a.md` -- Source A states this rule directly. |
| 7 | One timesheet file is submitted per team. | supported | `source_a.md` | 'Submit one file per team.' in `source_a.md` -- Source A requires one file per team. |
| 8 | The timesheet file must list every hourly worker with hours. | supported | `source_a.md` | 'The file must list every hourly worker with hours' in `source_a.md` -- Source A requires the file to list every hourly worker with hours. |
| 9 | The timesheet file must list the cost centre the hours are charged to. | supported | `source_a.md` | 'the cost centre the hours are charged to' in `source_a.md` -- Source A requires the file to list the cost centre the hours are charged to. |
| 10 | Blank rows are rejected by the upload page. | supported | `source_a.md` | 'Blank rows are rejected by the upload\npage.' in `source_a.md` -- Source A states this verbatim. |
| 11 | A correction submitted before the cut-off replaces the earlier file entirely. | supported | `source_a.md` | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `source_a.md` -- Both sources state this; source A is quoted. |
| 12 | After the cut-off, corrections go to the payroll inbox as a written request. | supported | `source_b.md` | 'After the cut-off, corrections go to the payroll inbox as a written request.' in `source_b.md` -- Source B states this verbatim, and source A says the same. |
| 13 | Corrections made after the cut-off are applied to the following month. | supported | `source_a.md` | 'are applied to the following month.' in `source_a.md` -- Source A says corrections made after the cut-off are applied to the following month. |
| 14 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | supported | `source_b.md` | 'Teams without terminal access may send paper timesheets to the payroll office by\ninternal post' in `source_b.md` -- Source B states this in its 'Paper timesheets' section. |
| 15 | Paper timesheets must arrive at the payroll office no later than the cut-off. | supported | `source_b.md` | 'to arrive no later than the cut-off.' in `source_b.md` -- Source B requires paper timesheets to arrive no later than the cut-off. |
| 16 | If the upload page is unavailable in the hour before the cut-off, team leads should email the payroll team. | supported | `source_a.md` | 'If the upload page is unavailable in the hour before the cut-off, email the\npayroll team' in `source_a.md` -- Source A's escalation section states this. |
| 17 | If the upload page is unavailable in the hour before the cut-off, team leads should keep the file. | supported | `source_a.md` | 'payroll team and keep the file.' in `source_a.md` -- Source A instructs team leads to keep the file when the upload page is unavailable. |
| 18 | Timesheet totals should not be sent in the body of an email. | supported | `source_a.md` | 'Do not send totals in the body of an email.' in `source_a.md` -- Source A states this directly. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **18** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **24**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 15 attributed segment(s) — sources interleaved. 12 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **21** departure(s) from its sources. Checking them confirms 21, rejects 0, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 33 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Audience slot: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a7` | reworded | Cut-off slot: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `a8` | reworded | Late submissions slot: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-005`) |
| `a9` | reworded | Weekend rule slot: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`) |
| `a12` | reworded | File contents slot: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`) |
| `a13` | reworded | File rules slot: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`) |
| `a16` | reworded | Corrections slot: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`, `A-012`) |
| `a18` | reworded | Escalation slot: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-013`) |
| `b1` | superseded | Title slot: base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Payroll Submission Deadlines (2026 Schedule)' and says so (no claim traced to it) |
| `b2` | duplicate | Heading already carried from base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b3` | duplicate | Audience slot: identical to a3. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-001`) |
| `b4` | duplicate | Heading already carried from base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b5` | superseded | Cut-off slot: 2026 value chosen over 2025 value. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`) |
| `b6` | duplicate | Late submissions slot: same fact as a8. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-003`) |
| `b7` | superseded | Weekend rule slot: 2026 rule chosen over 2025 rule. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-004`) |
| `b8` | duplicate | Heading already carried from base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b9` | superseded | File contents slot: base wording kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-005`, `B-006`) |
| `b10` | duplicate | Heading already carried from base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b11` | duplicate | Corrections slot: identical to a15. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-007`) |
| `b12` | superseded | Corrections slot: base's fuller statement kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-008`) |
| `b14` | reworded | Paper timesheets slot: line break joined into prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-009`, `B-010`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 27,264 in, 14,263 out |
| Cost | ~$0.39 estimated (rates read 2026-09-25) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 113.4s |
| Generated | 2026-09-27T16:23:16+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
