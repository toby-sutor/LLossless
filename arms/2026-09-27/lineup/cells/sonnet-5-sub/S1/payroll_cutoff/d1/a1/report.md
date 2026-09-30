## Verdict

**2 finding(s).** In the claims: 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 16 |
| Claims extracted from `source_a.md` | 14 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **20/22** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **14/14** |
| Forward — `source_b.md` claims accounted for | **6/8** |
| Reverse — merge claims found in a source | **16/16** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **38/38** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:9` says: Totals must be submitted by 15:00 on the 20th of the month.
  - `merged.md` says: 'Totals must be submitted by 12:00 on the 18th of the month.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Reference states a different deadline of 12:00 on the 18th, not 15:00 on the 20th.
- **B-003** -- the two documents disagree
  - `source_b.md:12` says: If the 20th falls on a weekend, the cut-off moves to the following Monday.
  - `merged.md` says: 'the cut-off moves to the last working day before it' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Reference states the cut-off moves to the last working day before it, not to the following Monday.

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
| 1 | Team leads submit timesheet totals for hourly staff. | 5 | carried | 'Team leads who submit timesheet totals for hourly staff.' in `merged.md` -- Directly stated in the opening section. |
| 2 | Salaried staff are not covered by this page. | 5 | carried | 'Salaried staff are not covered by this page.' in `merged.md` -- Directly stated. |
| 3 | Totals must be submitted by 12:00 on the 18th of the month. | 10 | carried | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- Directly stated. |
| 4 | The 18th is a hard cut-off, not a target. | 10 | carried | 'The 18th is a hard cut-off, not a target.' in `merged.md` -- Directly stated. |
| 5 | Submissions that arrive after the cut-off are held for the following month's run. | 11 | carried | "Submissions that arrive after it are held for the following month's run." in `merged.md` -- Directly stated. |
| 6 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it. | 14 | carried | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- Directly stated. |
| 7 | One file must be submitted per team. | 19 | carried | 'Submit one file per team, listing every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- Directly stated. |
| 8 | The file must list every hourly worker with hours and the cost centre the hours are charged to. | 19 | carried | 'Submit one file per team, listing every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- Directly stated. |
| 9 | Blank rows are rejected by the upload page. | 20 | carried | 'Blank rows are rejected by the upload page.' in `merged.md` -- Directly stated. |
| 10 | A correction submitted before the cut-off replaces the earlier file entirely. | 25 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- Directly stated. |
| 11 | After the cut-off, corrections go to the payroll inbox as a written request. | 26 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.' in `merged.md` -- Directly stated. |
| 12 | Corrections submitted after the cut-off are applied to the following month. | 27 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.' in `merged.md` -- Directly stated. |
| 13 | If the upload page is unavailable in the hour before the cut-off, one should email the payroll team and keep the file. | 31 | carried | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file.' in `merged.md` -- Directly stated. |
| 14 | One should not send totals in the body of an email. | 32 | carried | 'Do not send totals in the body of an email.' in `merged.md` -- Directly stated. |

### `source_b.md` -- 8 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Totals must be submitted by 15:00 on the 20th of the month. | 9 | contradicted | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- Reference states a different deadline of 12:00 on the 18th, not 15:00 on the 20th. |
| 3 | If the 20th falls on a weekend, the cut-off moves to the following Monday. | 12 | contradicted | 'the cut-off moves to the last working day before it' in `merged.md` -- Reference states the cut-off moves to the last working day before it, not to the following Monday. |
| 2 | Submissions that arrive after the cut-off are held for the following month's run. | 9 | carried | "Submissions that arrive after it are held for the following month's run." in `merged.md` -- This general behavior is stated regardless of the specific cut-off time referenced. |
| 4 | Team leads must submit one file per team listing every hourly worker with hours and the cost centre the hours are charged to. | 16 | carried | 'Submit one file per team, listing every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- This submission requirement matches regardless of the specific date referenced. |
| 5 | A correction submitted before the cut-off replaces the earlier file entirely. | 21 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- Directly stated, independent of specific cut-off date. |
| 6 | After the cut-off, corrections go to the payroll inbox as a written request. | 22 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.' in `merged.md` -- Directly stated, independent of specific cut-off date. |
| 7 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | 26 | carried | 'Teams without terminal access may send paper timesheets to the payroll office by internal post' in `merged.md` -- Directly stated. |
| 8 | Paper timesheets sent by internal post must arrive no later than the cut-off. | 27 | carried | 'to arrive no later than the cut-off' in `merged.md` -- Directly stated. |

### `merged.md` -- 16 claim(s): 0 invented, 0 contradicted, 0 supported in part, 16 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Team leads submit timesheet totals for hourly staff. | supported | `source_a.md` | 'Team leads who submit timesheet totals for hourly staff.' in `source_a.md` -- Both sources state this directly. |
| 2 | Salaried staff are not covered by this page. | supported | `source_a.md` | 'Salaried staff are not covered by this page.' in `source_a.md` -- Stated verbatim in source_a. |
| 3 | Totals must be submitted by 12:00 on the 18th of the month. | supported | `source_a.md` | 'Totals must be submitted by 12:00 on the 18th of the month.' in `source_a.md` -- Matches source_a's stated deadline exactly. |
| 4 | The 18th is a hard cut-off, not a target. | supported | `source_a.md` | 'The 18th is a hard cut-off, not a target.' in `source_a.md` -- Stated verbatim in source_a. |
| 5 | Submissions that arrive after the cut-off are held for the following month's run. | supported | `source_b.md` | "Submissions that arrive after the cut-off are held for the following month's run." in `source_b.md` -- Both sources state this fact in similar wording. |
| 6 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it. | supported | `source_a.md` | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `source_a.md` -- Matches source_a's exact rule. |
| 7 | Team leads submit one file per team. | supported | `source_a.md` | 'Submit one file per team.' in `source_a.md` -- Stated in both sources. |
| 8 | The submitted file lists every hourly worker with hours and the cost centre the hours are charged to. | supported | `source_a.md` | 'The file must list every hourly worker with hours and\nthe cost centre the hours are charged to.' in `source_a.md` -- Stated in source_a and echoed in source_b. |
| 9 | Blank rows are rejected by the upload page. | supported | `source_a.md` | 'Blank rows are rejected by the upload page.' in `source_a.md` -- Stated verbatim in source_a. |
| 10 | A correction submitted before the cut-off replaces the earlier file entirely. | supported | `source_a.md` | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `source_a.md` -- Identical statement in both sources. |
| 11 | After the cut-off, corrections go to the payroll inbox as a written request. | supported | `source_a.md` | 'After the cut-off, corrections go to the payroll inbox as a written request' in `source_a.md` -- Stated in both sources. |
| 12 | Corrections submitted after the cut-off are applied to the following month. | supported | `source_a.md` | 'After the cut-off, corrections go to the payroll inbox as a written request and\nare applied to the following month.' in `source_a.md` -- Source_a states corrections after cutoff are applied to the following month. |
| 13 | If the upload page is unavailable in the hour before the cut-off, team leads should email the payroll team and keep the file. | supported | `source_a.md` | 'If the upload page is unavailable in the hour before the cut-off, email the\npayroll team and keep the file.' in `source_a.md` -- Stated verbatim in source_a. |
| 14 | Team leads should not send totals in the body of an email. | supported | `source_a.md` | 'Do not send totals in the body of an email.' in `source_a.md` -- Stated verbatim in source_a. |
| 15 | Teams without terminal access may send paper timesheets to the payroll office by internal post. | supported | `source_b.md` | 'Teams without terminal access may send paper timesheets to the payroll office by\ninternal post' in `source_b.md` -- Stated verbatim in source_b. |
| 16 | Paper timesheets sent by internal post must arrive no later than the cut-off. | supported | `source_b.md` | 'to arrive no later than the cut-off.' in `source_b.md` -- Stated verbatim in source_b. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **16** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **22**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 4 run(s) over 14 attributed segment(s) — sources interleaved. 12 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **12** departure(s) from its sources. Checking them confirms 12, rejects 0, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 33 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base 2026 title kept over 2025-dated title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Payroll Submission Deadlines (2026 Schedule)' and says so (no claim traced to it) |
| `b3` | duplicate | Same fact as a3; a's wording and extra detail kept. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b5` | superseded | Conflicting cut-off value; a's 2026 value chosen. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b6` | duplicate | Same fact as a8, a's wording kept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-002`) |
| `b7` | superseded | Conflicting adjustment rule; a's fuller rule chosen. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`) |
| `b8` | duplicate | Identical heading to a10, consolidated. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a11` | reworded | Combined with a12 into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`) |
| `a12` | subsumed | Content folded into the combined sentence with a11. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-008`) |
| `b9` | duplicate | Same fact as a11/a12, a's wording basis kept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-004`) |
| `b10` | duplicate | Identical heading to a14, consolidated. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b11` | duplicate | Same fact as a15, wording kept. | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`B-005`) |
| `b12` | superseded | a16's fuller statement already includes this detail. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-006`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | d320da0eb7ed (command) -- lineup sonnet-5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 -> claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=medium, merge=medium, verify=medium |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 114.5s |
| Generated | 2026-09-27T17:12:32+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
