## Verdict

**6 finding(s).** In the claims: 2 contradicted. In the structure: 2 false departure, 2 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 12 |
| Claims extracted from `source_a.md` | 15 |
| Claims extracted from `source_b.md` | 7 |
| Forward — source claims accounted for in the merge | **20/22** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **15/15** |
| Forward — `source_b.md` claims accounted for | **5/7** |
| Reverse — merge claims found in a source | **12/12** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **34/34** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:9` says: Totals must be submitted by 15:00 on the 20th of the month.
  - `merged.md` says: 'Totals must be submitted by 12:00 on the 18th of the month' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference specifies 12:00 on the 18th, contradicting the claim's 15:00 on the 20th.
- **B-003** -- the two documents disagree
  - `source_b.md:12` says: If the 20th falls on a weekend, the cut-off moves to the following Monday.
  - `merged.md` says: 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference specifies the cut-off moves to the last working day BEFORE the 18th, not the following Monday after the 20th.

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
| 1 | Team leads submit timesheet totals for hourly staff | 5 | carried | 'Team leads who submit timesheet totals for hourly staff' in `merged.md` -- The reference text explicitly states this in the 'Who this is for' section. |
| 2 | Salaried staff are not covered by this page | 5 | carried | 'Salaried staff are not covered by this page' in `merged.md` -- The reference text directly states this restriction in the 'Who this is for' section. |
| 3 | Totals must be submitted by 12:00 on the 18th of the month | 10 | carried | 'Totals must be submitted by 12:00 on the 18th of the month' in `merged.md` -- The reference text explicitly states this deadline in the 'Monthly cut-off' section. |
| 4 | The 18th is a hard cut-off, not a target | 10 | carried | 'The 18th is a hard cut-off, not a target' in `merged.md` -- The reference text directly describes the 18th as a hard cut-off in the 'Monthly cut-off' section. |
| 5 | Submissions that arrive after the cut-off are held for the following month's run | 11 | carried | "submissions that arrive after it are held for the following month's run" in `merged.md` -- This is stated in the 'Monthly cut-off' section regarding what happens to late submissions. |
| 6 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it | 14 | carried | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it' in `merged.md` -- The reference text explicitly states this adjustment rule in the 'Monthly cut-off' section. |
| 7 | One file per team must be submitted | 19 | carried | 'Submit one file per team' in `merged.md` -- The reference text states this requirement in the 'What to submit' section. |
| 8 | The file must list every hourly worker with hours and the cost centre the hours are charged to | 19 | carried | 'listing every hourly worker with hours and the cost centre the hours are charged to' in `merged.md` -- The reference text specifies this content requirement in the 'What to submit' section. |
| 9 | Blank rows are rejected by the upload page | 20 | carried | 'Blank rows are rejected by the upload page' in `merged.md` -- The reference text explicitly states this in the 'What to submit' section. |
| 10 | A correction submitted before the cut-off replaces the earlier file entirely | 25 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely' in `merged.md` -- The reference text directly states this in the 'Corrections' section. |
| 11 | After the cut-off, corrections go to the payroll inbox as a written request | 26 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The reference text states this process in the 'Corrections' section. |
| 12 | After the cut-off, corrections are applied to the following month | 26 | carried | 'are applied to the following month' in `merged.md` -- The reference text states post-cut-off corrections are applied to the following month. |
| 13 | If the upload page is unavailable in the hour before the cut-off, email the payroll team | 31 | carried | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team' in `merged.md` -- The reference text states this action in the 'Escalation' section. |
| 14 | If the upload page is unavailable in the hour before the cut-off, keep the file | 31 | carried | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file' in `merged.md` -- The reference text states both actions in the 'Escalation' section when the upload page is unavailable. |
| 15 | Totals must not be sent in the body of an email | 32 | carried | 'Do not send totals in the body of an email' in `merged.md` -- The reference text states this restriction in the 'Escalation' section with equivalent meaning. |

### `source_b.md` -- 7 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Totals must be submitted by 15:00 on the 20th of the month. | 9 | contradicted | 'Totals must be submitted by 12:00 on the 18th of the month' in `merged.md` -- The reference specifies 12:00 on the 18th, contradicting the claim's 15:00 on the 20th. |
| 3 | If the 20th falls on a weekend, the cut-off moves to the following Monday. | 12 | contradicted | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it' in `merged.md` -- The reference specifies the cut-off moves to the last working day BEFORE the 18th, not the following Monday after the 20th. |
| 2 | Submissions that arrive after the cut-off are held for the following month's run. | 9 | carried | "submissions that arrive after it are held for the following month's run" in `merged.md` -- The reference text states this about late submissions in the 'Monthly cut-off' section. |
| 4 | Submit one file per team listing every hourly worker with hours and the cost centre the hours are charged to. | 16 | carried | 'Submit one file per team listing every hourly worker with hours and the cost centre the hours are charged to' in `merged.md` -- The reference text states this exact requirement in the 'What to submit' section. |
| 5 | A correction submitted before the cut-off replaces the earlier file entirely. | 21 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely' in `merged.md` -- The reference text states this in the 'Corrections' section. |
| 6 | After the cut-off, corrections go to the payroll inbox as a written request. | 22 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request' in `merged.md` -- The reference text states this process in the 'Corrections' section. |
| 7 | Teams without terminal access may send paper timesheets to the payroll office by internal post, to arrive no later than the cut-off. | 26 | carried | 'Teams without terminal access may send paper timesheets to the payroll office by internal post, to arrive no later than the cut-off' in `merged.md` -- The reference text states this provision in the 'Paper timesheets' section. |

### `merged.md` -- 12 claim(s): 0 invented, 0 contradicted, 0 supported in part, 12 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Totals must be submitted by 12:00 on the 18th of the month. | supported | `source_a.md` | 'Totals must be submitted by 12:00 on the 18th of the month.' in `source_a.md` -- Source A states this requirement identically. |
| 2 | The 18th is a hard cut-off, not a target. | supported | `source_a.md` | 'The 18th is a hard cut-off, not a target.' in `source_a.md` -- Source A states this characterization of the deadline identically. |
| 3 | Submissions that arrive after the 18th are held for the following month's run. | supported | `source_a.md` | "Submissions that arrive after it are held for the following month's run." in `source_a.md` -- Source A states this, with 'it' referring to the 18th cut-off mentioned in the preceding sentence. |
| 4 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it. | supported | `source_a.md` | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `source_a.md` -- Source A states this exception to the fixed deadline identically. |
| 5 | One file per team lists every hourly worker with hours and the cost centre the hours are charged to. | supported | `source_a.md` | 'Submit one file per team. The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `source_a.md` -- Source A states these submission requirements in consecutive sentences. |
| 6 | Blank rows are rejected by the upload page. | supported | `source_a.md` | 'Blank rows are rejected by the upload page.' in `source_a.md` -- Source A states this requirement identically. |
| 7 | A correction submitted before the cut-off replaces the earlier file entirely. | supported | `source_a.md` | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `source_a.md` -- Source A states this rule identically. |
| 8 | After the cut-off, corrections go to the payroll inbox as a written request. | supported | `source_a.md` | 'After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.' in `source_a.md` -- Source A contains this statement, with the claim drawn from its first part. |
| 9 | Corrections are applied to the following month. | supported | `source_a.md` | 'After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.' in `source_a.md` -- Source A explicitly states that post-cut-off corrections are applied to the following month. |
| 10 | If the upload page is unavailable in the hour before the cut-off, the payroll team should be emailed and the file should be kept. | supported | `source_a.md` | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file.' in `source_a.md` -- Source A states this guidance; the claim rephrases it using passive voice. |
| 11 | Totals should not be sent in the body of an email. | supported | `source_a.md` | 'Do not send totals in the body of an email.' in `source_a.md` -- Source A states this prohibition; the claim rephrases it with a modal verb. |
| 12 | Teams without terminal access may send paper timesheets to the payroll office by internal post, to arrive no later than the cut-off. | supported | `source_b.md` | 'Teams without terminal access may send paper timesheets to the payroll office by internal post, to arrive no later than the cut-off.' in `source_b.md` -- Source B states this option identically. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **12** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **22**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 4 run(s) over 13 attributed segment(s) — sources interleaved. 12 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a8` (`source_a.md`) — "Submissions that arrive after it are held for the following month's run." is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Submissions that arrive after it are held for the following month's run.
  In the merge:  Totals must be submitted by 12:00 on the 18th of the month. The 18th is a hard cut-off, not a target, and submissions that arrive after it are held for the following month's run.
  ```
- `b9` (`source_b.md`) — 'Submit one file per team listing every hourly worker with hours and the cost centre the hours are charged to.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Submit one file per team listing every hourly worker with hours and the cost centre the hours are charged to.
  In the merge:  Submit one file per team listing every hourly worker with hours and the cost centre the hours are charged to.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b5` (`source_b.md`) — numeric '15:00' (on) does not survive into the merge unchanged
- `b5` (`source_b.md`) — numeric '20th' (of) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **17** departure(s) from its sources. Checking them confirms 16, rejects 0, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 33 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a6` | reworded | Combined a6-a8 for flow and readability. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a7` | subsumed | Content subsumed into combined cut-off statement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-004`) |
| `a8` | subsumed | Content subsumed into combined cut-off statement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-005`) |
| `a11` | reworded | Combined a11-a12 to make concise and clear. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`) |
| `a12` | subsumed | Content subsumed into reworded statement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-008`) |
| `b1` | superseded | Base document's current-year title used instead. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Payroll Submission Deadlines (2026 Schedule)' and says so (no claim traced to it) |
| `b2` | duplicate | Same heading as a2. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b3` | superseded | A's version is more complete with salaried staff exclusion. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | duplicate | Same heading as a5. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b5` | superseded | 2026 schedule uses updated deadline time and date. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b6` | superseded | Same rule expressed with 2026 deadline details. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-002`) |
| `b7` | superseded | A's rule is more comprehensive, covering holidays. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`) |
| `b8` | duplicate | Same heading as a10. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b9` | subsumed | Content included in merged what-to-submit section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b10` | duplicate | Same heading as a14. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b11` | subsumed | Content included in merged corrections section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`) |
| `b12` | superseded | A's version adds when corrections are applied. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-006`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 45fff742d0ed (command) -- lineup haiku-4.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 495.8s |
| Generated | 2026-09-27T17:20:49+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
