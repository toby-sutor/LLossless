## Verdict

**11 finding(s).** In the claims: 1 partially dropped, 3 contradicted, 2 partially invented. In the structure: 1 undeclared absence, 2 undeclared rewording, 1 verbatim violation, 1 declared loss over budget. The merge declared **1** drop(s) of 33 source segment(s), **3.0%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself. The 1 claim(s) they cost are listed in the review queue below.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 13 |
| Claims extracted from `source_a.md` | 11 |
| Claims extracted from `source_b.md` | 7 |
| Forward — source claims accounted for in the merge | **14/18** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **11/11** |
| Forward — `source_b.md` claims accounted for | **3/7** (1 in part) |
| Reverse — merge claims found in a source | **10/13** |
| Reverse — supported only in part | 2 |
| Evidence grounded | **29/30** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-006** (`source_b.md:22`) — After the cut-off, corrections go to the payroll inbox as a written request.
  - evidence: 'After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference text states that corrections go to payroll inbox as a written request, but also specifies they are applied to the following month, not stated in the claim.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:9` says: Totals must be submitted by 15:00 on the 20th of the month.
  - `merged.md` says: 'Totals must be submitted by 12:00 on the 18th of the month.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text specifies 12:00 on the 18th, contradicting the claim's 15:00 on the 20th.
- **B-003** -- the two documents disagree
  - `source_b.md:12` says: If the 20th falls on a weekend, the cut-off moves to the following Monday.
  - `merged.md` says: 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text specifies the last working day before the 18th, not the following Monday as claimed.
- **M-003** -- the two documents disagree
  - `merged.md:9` says: Totals must be submitted by 12:00 on the 18th of the month.
  - `source_b.md` says: 'Totals must be submitted by 15:00 on the 20th of the month.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_a.md specifies 12:00 on the 18th, while source_b.md specifies 15:00 on the 20th. The claim states the former, contradicting source_b.md.

### Partly invented — the sources carry some of this claim

- **M-005** (`merged.md:9`) — Submissions that arrive after the 18th are held for the following month's run.
  - evidence: "Submissions that arrive after the cut-off are held for the following month's run." in `source_a.md` (attribution_error)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source_a.md states submissions after the cut-off go to the following month, but the claim specifies 'after the 18th' when source_a.md only says 'after the cut-off'.
- **M-011** (`merged.md:19`) — After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.
  - evidence: 'After the cut-off, corrections go to the payroll inbox as a written request' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source_a.md supports the first part, but only source_a.md adds 'and are applied to the following month'; source_b.md omits this detail.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 11 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 11 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Totals must be submitted by 12:00 on the 18th of the month. | 10 | carried | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The reference text states this claim exactly. |
| 2 | The 18th is a hard cut-off, not a target. | 10 | carried | 'The 18th is a hard cut-off, not a target.' in `merged.md` -- The reference text states this claim exactly. |
| 3 | Submissions that arrive after the 18th are held for the following month's run. | 11 | carried | "Submissions that arrive after it are held for the following month's run." in `merged.md` -- The reference text states this claim with 'it' referring to the 18th cut-off. |
| 4 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it. | 14 | carried | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The reference text states this claim exactly. |
| 5 | Submit one file per team. | 19 | carried | 'Submit one file per team.' in `merged.md` -- The reference text states this claim exactly. |
| 6 | The file must list every hourly worker with hours and the cost centre the hours are charged to. | 19 | carried | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The reference text states this claim exactly. |
| 7 | Blank rows are rejected by the upload page. | 20 | carried | 'Blank rows are rejected by the upload page.' in `merged.md` -- The reference text states this claim exactly. |
| 8 | A correction submitted before the cut-off replaces the earlier file entirely. | 25 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- The reference text states this claim exactly. |
| 9 | After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month. | 26 | carried | 'After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.' in `merged.md` -- The reference text states this claim exactly. |
| 10 | If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file. | 31 | carried | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file.' in `merged.md` -- The reference text states this claim exactly. |
| 11 | Do not send totals in the body of an email. | 32 | carried | 'Do not send totals in the body of an email.' in `merged.md` -- The reference text states this claim exactly. |

### `source_b.md` -- 7 claim(s): 1 dropped, 2 contradicted, 1 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 7 | Teams without terminal access may send paper timesheets to the payroll office by internal post, to arrive no later than the cut-off. | 26 | dropped | The reference text contains no information about paper timesheets or teams without terminal access. |
| 1 | Totals must be submitted by 15:00 on the 20th of the month. | 9 | contradicted | 'Totals must be submitted by 12:00 on the 18th of the month.' in `merged.md` -- The reference text specifies 12:00 on the 18th, contradicting the claim's 15:00 on the 20th. |
| 3 | If the 20th falls on a weekend, the cut-off moves to the following Monday. | 12 | contradicted | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `merged.md` -- The reference text specifies the last working day before the 18th, not the following Monday as claimed. |
| 6 | After the cut-off, corrections go to the payroll inbox as a written request. | 22 | carried in part | 'After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month.' in `merged.md` -- The reference text states that corrections go to payroll inbox as a written request, but also specifies they are applied to the following month, not stated in the claim. |
| 2 | Submissions that arrive after the cut-off are held for the following month's run. | 9 | carried | "Submissions that arrive after it are held for the following month's run." in `merged.md` -- The reference text states that submissions after the cut-off are held for the following month, matching this claim. |
| 4 | Submit one file per team listing every hourly worker with hours and the cost centre the hours are charged to. | 16 | carried | 'Submit one file per team. The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `merged.md` -- The reference text states both elements of this claim. |
| 5 | A correction submitted before the cut-off replaces the earlier file entirely. | 21 | carried | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `merged.md` -- The reference text states this claim exactly. |

### `merged.md` -- 13 claim(s): 0 invented, 1 contradicted, 2 supported in part, 10 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 3 | Totals must be submitted by 12:00 on the 18th of the month. | contradicted | `source_b.md` | 'Totals must be submitted by 15:00 on the 20th of the month.' in `source_b.md` -- Source_a.md specifies 12:00 on the 18th, while source_b.md specifies 15:00 on the 20th. The claim states the former, contradicting source_b.md. |
| 5 | Submissions that arrive after the 18th are held for the following month's run. | supported in part | `source_a.md` | "Submissions that arrive after the cut-off are held for the following month's run." in `source_a.md`, **attribution_error** -- Source_a.md states submissions after the cut-off go to the following month, but the claim specifies 'after the 18th' when source_a.md only says 'after the cut-off'. |
| 11 | After the cut-off, corrections go to the payroll inbox as a written request and are applied to the following month. | supported in part | `source_a.md` | 'After the cut-off, corrections go to the payroll inbox as a written request' in `source_a.md` -- Source_a.md supports the first part, but only source_a.md adds 'and are applied to the following month'; source_b.md omits this detail. |
| 1 | This page covers team leads who submit timesheet totals for hourly staff. | supported | `source_a.md` | 'Team leads who submit timesheet totals for hourly staff.' in `source_a.md` -- Both sources state this in their 'Who this is for' sections. Source_a.md uses identical wording. |
| 2 | Salaried staff are not covered by this page. | supported | `source_a.md` | 'Salaried staff are not covered by this page.' in `source_a.md` -- Source_a.md explicitly states this in the 'Who this is for' section. |
| 4 | The 18th is a hard cut-off, not a target. | supported | `source_a.md` | 'The 18th is a hard cut-off, not a target.' in `source_a.md` -- Source_a.md explicitly states this phrase in the 'Monthly cut-off' section. |
| 6 | If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it. | supported | `source_a.md` | 'If the 18th falls on a weekend or a public holiday, the cut-off moves to the last working day before it.' in `source_a.md` -- Source_a.md states this exact rule in the 'Monthly cut-off' section. |
| 7 | One file per team must be submitted. | supported | `source_a.md` | 'Submit one file per team.' in `source_a.md` -- Source_a.md states this in the 'What to submit' section; source_b.md also covers this. |
| 8 | The file must list every hourly worker with hours and the cost centre the hours are charged to. | supported | `source_a.md` | 'The file must list every hourly worker with hours and the cost centre the hours are charged to.' in `source_a.md` -- Source_a.md states this requirement in the 'What to submit' section. |
| 9 | Blank rows are rejected by the upload page. | supported | `source_a.md` | 'Blank rows are rejected by the upload page.' in `source_a.md` -- Source_a.md explicitly states this in the 'What to submit' section. |
| 10 | A correction submitted before the cut-off replaces the earlier file entirely. | supported | `source_a.md` | 'A correction submitted before the cut-off replaces the earlier file entirely.' in `source_a.md` -- Both sources state this identically in their 'Corrections' sections. |
| 12 | If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file. | supported | `source_a.md` | 'If the upload page is unavailable in the hour before the cut-off, email the payroll team and keep the file.' in `source_a.md` -- Source_a.md states this exactly in the 'Escalation' section. |
| 13 | Do not send totals in the body of an email. | supported | `source_a.md` | 'Do not send totals in the body of an email.' in `source_a.md` -- Source_a.md explicitly states this instruction in the 'Escalation' section. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **13** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **18**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 1 run(s) over 13 attributed segment(s) — not conclusive on this evidence base. 11 of 12 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `b13` (`source_b.md`) — 'Paper timesheets' is not in the merge and no disposition record explains it (nearest merge segment m3 at 0.36)

  ```text
  In the source: Paper timesheets
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `b6` (`source_b.md`) — "Submissions that arrive after the cut-off are held for the following month's run." is reworded in the merge and no disposition record explains it (nearest merge segment m8 at 0.93)

  ```text
  In the source: Submissions that arrive after the cut-off are held for the following month's run.
  In the merge:  Submissions that arrive after it are held for the following month's run.
  What changed:  Submissions that arrive after [-the cut-off-] {+it+} are held for the following month's run.
  ```
- `b9` (`source_b.md`) — 'Submit one file per team listing every hourly worker with hours and the cost centre the hours are charged to.' is reworded in the merge and no disposition record explains it (nearest merge segment m12 at 0.89)

  ```text
  In the source: Submit one file per team listing every hourly worker with hours and the cost centre the hours are charged to.
  In the merge:  The file must list every hourly worker with hours and the cost centre the hours are charged to.
  What changed:  [-Submit one-] {+The+} file [-per team listing-] {+must list+} every hourly worker with hours and the cost centre the hours are charged to.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b7` (`source_b.md`) — numeric '20th' (falls) does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 1 of 33 segments are declared dropped (3.0%), over the 3% budget

## Review queue

**1** claim(s) the merge declared dropped and the forward pass confirms are gone. Each is a decision to review — put the fact back, or agree it stays out — and none of them is counted as a finding above.

- **B-007** (`source_b.md:26`) — Teams without terminal access may send paper timesheets to the payroll office by internal post, to arrive no later than the cut-off.
  - left out of: `b14`
  - the merge's reason: Paper timesheet option not mentioned in 2026 schedule; dropped as obsolete.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text contains no information about paper timesheets or teams without terminal access.

> **Over budget.** The merge declared **1** drop(s) of 33 source segment(s), **3.0%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **5** departure(s) from its sources. Checking them confirms 3, rejects 2, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 1 of 33 source segment(s) declared gone, **3.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base document title kept; reflects current year schedule. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Payroll Submission Deadlines (2026 Schedule)' and says so (no claim traced to it) |
| `b5` | superseded | Cut-off time and date from base document used; 2026 schedule applies. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`) |
| `b7` | subsumed | Base document's more comprehensive rule covers both weekends and holidays. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-003 came back CONTRADICTED (`B-003`) |
| `b12` | subsumed | Base document adds detail that corrections are applied to following month. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-006 came back PARTIAL (`B-006`) |
| `b14` | dropped | Paper timesheet option not mentioned in 2026 schedule; dropped as obsolete. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-007`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 17,300 in, 7,504 out |
| Cost | ~$0.05 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 49.4s |
| Generated | 2026-09-27T16:26:47+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
