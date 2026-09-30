## Verdict

**4 finding(s).** In the claims: 1 partially dropped. In the structure: 3 false departure.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 17 |
| Claims extracted from `source_a.md` | 13 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **25/26** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **13/13** |
| Forward — `source_b.md` claims accounted for | **12/13** (1 in part) |
| Reverse — merge claims found in a source | **17/17** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **43/43** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-009** (`source_b.md:18`) — The visitor's line on the expected-visitor list is marked with an N.
  - evidence: "Mark the visitor's line on the expected-visitor list with an N." in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference text states this action occurs when a badge is not returned, but the claim omits this condition.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 13 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 13 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | A visitor badge is printed from the front desk terminal. | 6 | carried | 'Print a badge from the front desk terminal.' in `merged.md` -- The reference text directly states that a badge is printed from the front desk terminal during the visitor badge issuing process. |
| 2 | The host's name is written on the badge in the space provided. | 6 | carried | "Write the host's name on the badge in the space provided." in `merged.md` -- The reference text explicitly states that the host's name is written on the badge in the space provided. |
| 3 | The visitor is asked to wear the badge above the waist and in view for the whole visit. | 7 | carried | 'ask the visitor to wear it above the waist and in view for the whole visit.' in `merged.md` -- The reference text states that the visitor is asked to wear the badge above the waist and in view for the whole visit. |
| 4 | Visitors return badges at the front desk on their way out. | 12 | carried | 'Visitors return badges at the front desk on their way out.' in `merged.md` -- The reference text explicitly states that visitors return badges at the front desk on their way out. |
| 5 | The badge is wiped with the cleaning cloth kept in the top drawer. | 12 | carried | 'Wipe the badge with the cleaning cloth kept in the top drawer' in `merged.md` -- The reference text states that the badge is wiped with the cleaning cloth kept in the top drawer. |
| 6 | The badge is put back in the return tray. | 13 | carried | 'put it back in the return tray.' in `merged.md` -- The reference text states that the badge is put back in the return tray after wiping. |
| 7 | Badges in the return tray are re-used the same day. | 14 | carried | 'Badges in the return tray are re-used the same day.' in `merged.md` -- The reference text explicitly states that badges in the return tray are re-used the same day. |
| 8 | The visitor's line on the expected-visitor list is marked with an N if a badge is not returned. | 18 | carried | "Mark the visitor's line on the expected-visitor list with an N." in `merged.md` -- The reference text states that the visitor's line is marked with an N if a badge is not returned. |
| 9 | At the end of the day, the list of unreturned badges is sent to the security office. | 18 | carried | 'At the end of the day, send the list of unreturned badges to the security office.' in `merged.md` -- The reference text explicitly states that the list of unreturned badges is sent to the security office at the end of the day. |
| 10 | Badges that have been missing for 7 days are deactivated. | 19 | carried | 'Badges that have been missing for 7 days are deactivated.' in `merged.md` -- The reference text directly states that badges missing for 7 days are deactivated. |
| 11 | Contractors on a job lasting more than one day are issued a week badge instead of a day badge. | 24 | carried | 'Contractors on a job lasting more than one day are issued a week badge instead of a day badge.' in `merged.md` -- The reference text explicitly states that contractors on jobs lasting more than one day receive a week badge instead of a day badge. |
| 12 | A week badge is valid for 7 days from the date printed on it. | 25 | carried | 'A week badge is valid for 7 days from the date printed on it.' in `merged.md` -- The reference text directly states that a week badge is valid for 7 days from the date printed on it. |
| 13 | Contractors sign the contractor register in addition to the visitor list. | 26 | carried | 'Contractors sign the contractor register in addition to the visitor list.' in `merged.md` -- The reference text explicitly states that contractors sign the contractor register in addition to the visitor list. |

### `source_b.md` -- 13 claim(s): 0 dropped, 0 contradicted, 1 carried in part, 12 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 9 | The visitor's line on the expected-visitor list is marked with an N. | 18 | carried in part | "Mark the visitor's line on the expected-visitor list with an N." in `merged.md` -- The reference text states this action occurs when a badge is not returned, but the claim omits this condition. |
| 1 | The visitor's photo identification is checked against the day's expected-visitor list. | 5 | carried | "Ask the visitor for photo identification and check the name against the day's expected-visitor list." in `merged.md` -- The reference text states that the visitor's photo identification is checked against the day's expected-visitor list. |
| 2 | A badge is printed from the front desk terminal. | 6 | carried | 'Print a badge from the front desk terminal.' in `merged.md` -- The reference text states that a badge is printed from the front desk terminal. |
| 3 | The host's name is written on the badge in the space provided. | 6 | carried | "Write the host's name on the badge in the space provided." in `merged.md` -- The reference text states that the host's name is written on the badge in the space provided. |
| 4 | The visitor is asked to wear the badge above the waist and in view for the whole visit. | 7 | carried | 'ask the visitor to wear it above the waist and in view for the whole visit.' in `merged.md` -- The reference text states that the visitor is asked to wear the badge above the waist and in view for the whole visit. |
| 5 | Visitors return badges at the front desk on their way out. | 12 | carried | 'Visitors return badges at the front desk on their way out.' in `merged.md` -- The reference text states that visitors return badges at the front desk on their way out. |
| 6 | The badge is wiped with the cleaning cloth kept in the top drawer. | 12 | carried | 'Wipe the badge with the cleaning cloth kept in the top drawer' in `merged.md` -- The reference text states that the badge is wiped with the cleaning cloth kept in the top drawer. |
| 7 | The badge is put back in the return tray. | 13 | carried | 'put it back in the return tray.' in `merged.md` -- The reference text states that the badge is put back in the return tray. |
| 8 | Badges in the return tray are re-used the same day. | 14 | carried | 'Badges in the return tray are re-used the same day.' in `merged.md` -- The reference text states that badges in the return tray are re-used the same day. |
| 10 | The list of unreturned badges is sent to the security office at the end of the day. | 18 | carried | 'At the end of the day, send the list of unreturned badges to the security office.' in `merged.md` -- The reference text states that the list of unreturned badges is sent to the security office at the end of the day. |
| 11 | Badges that have been missing for 7 days are deactivated. | 19 | carried | 'Badges that have been missing for 7 days are deactivated.' in `merged.md` -- The reference text states that badges missing for 7 days are deactivated. |
| 12 | A badge handed in after it was reported missing goes to the security office rather than back into the return tray. | 24 | carried | 'A badge handed in after it was reported missing goes to the security office rather than back into the return tray.' in `merged.md` -- The reference text explicitly states that a badge handed in after being reported missing goes to the security office rather than back into the return tray. |
| 13 | The security office decides whether to reactivate a badge. | 25 | carried | 'The security office decides whether to reactivate it.' in `merged.md` -- The reference text explicitly states that the security office decides whether to reactivate a badge that was reported missing and then handed in later. |

### `merged.md` -- 17 claim(s): 0 invented, 0 contradicted, 0 supported in part, 17 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The front desk staff ask the visitor for photo identification. | supported | `source_a.md` | 'Ask the visitor for photo identification' in `source_a.md` -- Both sources state that front desk staff ask visitors for photo identification as the first step in badge issuing. |
| 2 | The front desk staff check the name against the day's expected-visitor list. | supported | `source_a.md` | "check the name against the day's expected-visitor list" in `source_a.md` -- Both sources state that the name is checked against the expected-visitor list during badge issuing. |
| 3 | A badge is printed from the front desk terminal. | supported | `source_a.md` | 'Print a badge from the front desk terminal.' in `source_a.md` -- Both sources state that a badge is printed from the front desk terminal. |
| 4 | The host's name is written on the badge in the space provided. | supported | `source_a.md` | "Write the host's name on the badge in the space provided." in `source_a.md` -- Both sources state that the host's name is written on the badge in the space provided. |
| 5 | The visitor is asked to wear the badge above the waist and in view for the whole visit. | supported | `source_a.md` | 'ask the visitor to wear it above the waist and in view for the whole visit' in `source_a.md` -- Both sources state that visitors are asked to wear the badge above the waist and in view for the whole visit. |
| 6 | Visitors return badges at the front desk on their way out. | supported | `source_a.md` | 'Visitors return badges at the front desk on their way out.' in `source_a.md` -- Both sources state that visitors return badges at the front desk on their way out. |
| 7 | The badge is wiped with the cleaning cloth kept in the top drawer. | supported | `source_a.md` | 'Wipe the badge with the cleaning cloth kept in the top drawer' in `source_a.md` -- Both sources state that the badge is wiped with the cleaning cloth kept in the top drawer. |
| 8 | The badge is put back in the return tray. | supported | `source_a.md` | 'put it back in the return tray' in `source_a.md` -- Both sources state that the badge is put back in the return tray after wiping. |
| 9 | Badges in the return tray are re-used the same day. | supported | `source_a.md` | 'Badges in the return tray are re-used the same day.' in `source_a.md` -- Both sources state that badges in the return tray are re-used the same day. |
| 10 | The visitor's line on the expected-visitor list is marked with an N if a badge is not returned. | supported | `source_a.md` | "Mark the visitor's line on the expected-visitor list with an N." in `source_a.md` -- Both sources state that the visitor's line is marked with an N if a badge is not returned. |
| 11 | At the end of the day, the list of unreturned badges is sent to the security office. | supported | `source_a.md` | 'send the list of unreturned badges to the security office' in `source_a.md` -- Both sources state that at the end of the day, the list of unreturned badges is sent to the security office. |
| 12 | Badges that have been missing for 7 days are deactivated. | supported | `source_a.md` | 'Badges that have been missing for 7 days are deactivated.' in `source_a.md` -- Both sources state that badges missing for 7 days are deactivated. |
| 13 | A badge handed in after it was reported missing goes to the security office rather than back into the return tray. | supported | `source_b.md` | 'A badge handed in after it was reported missing goes to the security office rather than back into the return tray.' in `source_b.md` -- Source B explicitly states this procedure in the 'Lost badges found later' section, which source A does not address. |
| 14 | The security office decides whether to reactivate a badge. | supported | `source_b.md` | 'The security office decides whether to reactivate it.' in `source_b.md` -- Source B states that the security office decides whether to reactivate a badge that was reported missing. |
| 15 | Contractors on a job lasting more than one day are issued a week badge instead of a day badge. | supported | `source_a.md` | 'Contractors on a job lasting more than one day are issued a week badge instead of a day badge.' in `source_a.md` -- Source A states this in the Contractors section; source B does not address contractors. |
| 16 | A week badge is valid for 7 days from the date printed on it. | supported | `source_a.md` | 'A week badge is valid for 7 days from the date printed on it.' in `source_a.md` -- Source A states the validity period of a week badge. |
| 17 | Contractors sign the contractor register in addition to the visitor list. | supported | `source_a.md` | 'Contractors sign the contractor register in addition to the visitor list.' in `source_a.md` -- Source A states that contractors sign the contractor register in addition to the visitor list. |

## Structure

**9** mechanical check(s) over **33** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **17** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **26**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 8 attributed segment(s) — sources interleaved. 9 of 10 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b14` (`source_b.md`) — 'Lost badges found later' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Lost badges found later
  In the merge:  ## Lost badges found later

A badge handed in after it was reported missing goes to the security office rather than back into the return tray. The security office decides whether to reactivate it.
  ```
- `b15` (`source_b.md`) — 'A badge handed in after it was reported missing goes to the security office rather than back into the return tray.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: A badge handed in after it was reported missing goes to the security office rather than back into the return tray.
  In the merge:  A badge handed in after it was reported missing goes to the security office rather than back into the return tray. The security office decides whether to reactivate it.
  What changed:  A badge handed in after it was reported missing goes to the security office rather than back into the return tray. {+The security office decides whether to reactivate it.+}
  ```
- `b16` (`source_b.md`) — 'The security office decides whether to reactivate it.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: The security office decides whether to reactivate it.
  In the merge:  A badge handed in after it was reported missing goes to the security office rather than back into the return tray. The security office decides whether to reactivate it.
  ```

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **4** departure(s) from its sources. Checking them confirms 3, rejects 0, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 33 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base document title chosen over non-base variant. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Badge Access - Front Desk Procedure' and says so (no claim traced to it) |
| `b14` | subsumed | New section added to merge; b14-b16 provide content not in base. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b15` | subsumed | Content survives in new section added to merged document. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-012`) |
| `b16` | subsumed | Content survives in new section added to merged document. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`) |


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
| Tokens | 16,896 in, 7,127 out |
| Cost | ~$0.05 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 45.8s |
| Generated | 2026-09-27T14:44:04+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
