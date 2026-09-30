## Verdict

**15 finding(s).** In the claims: 1 dropped, 3 contradicted. In the structure: 1 undeclared absence, 3 undeclared rewording, 2 false departure, 4 verbatim violation, 1 declared loss over budget. The merge declared **5** drop(s) of 27 source segment(s), **18.5%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself. The 1 claim(s) they cost are listed in the review queue below.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 9 |
| Claims extracted from `source_a.md` | 8 |
| Claims extracted from `source_b.md` | 7 |
| Forward — source claims accounted for in the merge | **11/15** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **7/8** |
| Forward — `source_b.md` claims accounted for | **4/7** |
| Reverse — merge claims found in a source | **8/9** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **22/22** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-004** (`source_b.md:8`) — A number of other symbols besides dots are refused by Nimbrel Probe.
  - judged against: `merged.md`
  - rationale: The reference text mentions dots but does not state that other symbols are also refused.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:4` says: The document was updated on 2026-01-29.
  - `merged.md` says: 'Updated: 2026-02-03' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document was updated on 2026-02-03, not 2026-01-29.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: The author is Marlowe Ferrante.
  - `merged.md` says: 'Author: Rune Delacroix' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The author is Rune Delacroix, not Marlowe Ferrante.
- **M-002** -- the two documents disagree
  - `merged.md:4` says: The document was updated on 2026-02-03.
  - `source_a.md` says: 'Updated: 2026-01-29' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: source_a.md shows the update date as 2026-01-29, not 2026-02-03 as claimed.

## Length capped

- `$.dispositions[4].reason` was 97 characters, over the 80-character cap; capped to fit
- `$.dispositions[11].reason` was 81 characters, over the 80-character cap; capped to fit
- `$.decisions[0].reason` was 86 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 8 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The document was updated on 2026-01-29. | 4 | contradicted | 'Updated: 2026-02-03' in `merged.md` -- The document was updated on 2026-02-03, not 2026-01-29. |
| 2 | Stream name is one of the mandatory fields for every Nimbrel Probe agent. | 8 | carried | 'Stream name is one of the mandatory field for every Nimbrel Probe agent.' in `merged.md` -- The reference text directly states this claim, with minor grammatical variation (field vs fields). |
| 3 | The stream name cannot contain arbitrary symbols. | 8 | carried | 'The stream name cannot contain arbitrary symbols as documented' in `merged.md` -- The reference text directly states the stream name cannot contain arbitrary symbols. |
| 4 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The reference text states this claim exactly as presented. |
| 5 | Stream names can contain letters, digits, spaces and hyphens only. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The reference text states stream names can contain letters, digits, spaces and hyphens only. |
| 6 | The Nimbrel Probe agent refuses to start if the stream name contains characters other than letters, digits, spaces and hyphens. | 12 | carried | 'or the agent refuses to start' in `merged.md` -- The reference text states the agent refuses to start if invalid characters are used. |
| 7 | A way to work around the restriction is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. | 25 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.' in `merged.md` -- The reference text describes this exact workaround. |
| 8 | The original stream name can be carried along as a global tag so each trace keeps a link between the real name and the renamed one. | 26 | carried | 'Then carry the original name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `merged.md` -- The reference text describes carrying the original name as a global tag to maintain a link. |

### `source_b.md` -- 7 claim(s): 2 dropped, 1 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 4 | A number of other symbols besides dots are refused by Nimbrel Probe. | 8 | dropped | The reference text mentions dots but does not state that other symbols are also refused. |
| 5 | The Nimbrel Probe stream name separates one instrumented process from the next. | 10 | dropped | The reference text does not state anything about stream names separating instrumented processes. |
| 1 | The author is Marlowe Ferrante. | 3 | contradicted | 'Author: Rune Delacroix' in `merged.md` -- The author is Rune Delacroix, not Marlowe Ferrante. |
| 2 | The document was updated on 2026-02-03. | 4 | carried | 'Updated: 2026-02-03' in `merged.md` -- The reference text states the document was updated on 2026-02-03. |
| 3 | Stream names containing a . (dot) are refused by Nimbrel Probe. | 8 | carried | 'Symbols such as dots (for example, checkout.web) are refused by Nimbrel Probe.' in `merged.md` -- The reference text explicitly states that dots are refused by Nimbrel Probe. |
| 6 | Only letters, digits, spaces and hyphens are accepted in Nimbrel Probe stream names. | 10 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The reference text states only letters, digits, spaces and hyphens are accepted. |
| 7 | Nimbrel Probe stream names must match the pattern ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The reference text states stream names must match this pattern. |

### `merged.md` -- 9 claim(s): 0 invented, 1 contradicted, 0 supported in part, 8 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 2 | The document was updated on 2026-02-03. | contradicted | `source_a.md` | 'Updated: 2026-01-29' in `source_a.md` -- source_a.md shows the update date as 2026-01-29, not 2026-02-03 as claimed. |
| 1 | The author is Rune Delacroix. | supported | `source_a.md` | 'Author: Rune Delacroix' in `source_a.md` -- source_a.md explicitly states the author is Rune Delacroix. |
| 3 | Stream name is one of the mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- source_a.md states this claim, using 'mandatry' (spelling preserved from source). |
| 4 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- source_a.md explicitly states stream names are validated against this regex before agent registration. |
| 5 | Stream names can contain letters, digits, spaces and hyphens only. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else' in `source_a.md` -- source_a.md plainly states what characters are allowed in stream names. |
| 6 | The agent refuses to start if the stream name contains symbols other than letters, digits, spaces and hyphens. | supported | `source_a.md` | 'the agent refuses to start' in `source_a.md` -- source_a.md states the agent refuses to start if stream name does not match the regex. |
| 7 | Symbols such as dots (for example, checkout.web) are refused by Nimbrel Probe. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- source_b.md explicitly states that dots and other symbols are refused by Nimbrel Probe. |
| 8 | The workaround is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- source_a.md provides this exact workaround as step 1 of the solution. |
| 9 | The original name can be carried along as a global tag. | supported | `source_a.md` | 'carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- source_a.md describes this as step 2 of the workaround solution. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **9** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **15**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 12 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `b6` (`source_b.md`) — 'Only letters, digits, spaces and hyphens are accepted (it has to match ^[A-Za-z0-9 -]+$) as documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' is not in the merge and no disposition record explains it (nearest merge segment m5 at 0.61)

  ```text
  In the source: Only letters, digits, spaces and hyphens are accepted (it has to match ^[A-Za-z0-9 -]+$) as documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)
  ```

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a14` (`source_a.md`) — '{internal-notes} https://tickets.nimbrel.example/700Bb00000QrmTD {/internal-notes}' is reworded in the merge and no disposition record explains it (nearest merge segment m14 at 0.77)

  ```text
  In the source: {internal-notes} https://tickets.nimbrel.example/700Bb00000QrmTD {/internal-notes}
  In the merge:  {internal-notes} https://tickets.nimbrel.example/700Bb00000QrmTD https://tickets.nimbrel.example/700Bb00000LnqWs {/internal-notes}
  ```
- `b2` (`source_b.md`) — 'Author: Marlowe Ferrante Updated: 2026-02-03' is reworded in the merge and no disposition record explains it (nearest merge segment m2 at 0.77)

  ```text
  In the source: Author: Marlowe Ferrante Updated: 2026-02-03
  In the merge:  Author: Rune Delacroix Updated: 2026-02-03
  ```
- `b13` (`source_b.md`) — '{internal-notes} https://tickets.nimbrel.example/700Bb00000LnqWs {/internal-notes}' is reworded in the merge and no disposition record explains it (nearest merge segment m14 at 0.77)

  ```text
  In the source: {internal-notes} https://tickets.nimbrel.example/700Bb00000LnqWs {/internal-notes}
  In the merge:  {internal-notes} https://tickets.nimbrel.example/700Bb00000QrmTD https://tickets.nimbrel.example/700Bb00000LnqWs {/internal-notes}
  ```

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a12` (`source_a.md`) — 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
  In the merge:  Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. Then carry the original name along as a global tag, so at least each trace keeps a link between the real name and the renamed one: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags
  ```
- `b9` (`source_b.md`) — 'Workaround' is declared 'superseded' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Workaround
  In the merge:  ### Workaround
  What changed:  {+###+} Workaround
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '2026-01-29' does not survive into the merge unchanged
- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged
- `b6` (`source_b.md`) — link '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' does not survive into the merge unchanged
- `b6` (`source_b.md`) — url 'https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 5 of 27 segments are declared dropped (18.5%), over the 3% budget

## Review queue

**1** claim(s) the merge declared dropped and the forward pass confirms are gone. Each is a decision to review — put the fact back, or agree it stays out — and none of them is counted as a finding above.

- **B-005** (`source_b.md:10`) — The Nimbrel Probe stream name separates one instrumented process from the next.
  - left out of: `b5`
  - the merge's reason: Context about stream name separation is not essential to the problem or solution
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not state anything about stream names separating instrumented processes.

> **Over budget.** The merge declared **5** drop(s) of 27 source segment(s), **18.5%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **18** departure(s) from its sources. Checking them confirms 10, rejects 2, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 5 of 27 source segment(s) declared gone, **18.5%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Updated date changed to the later date from source_b.md. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Fixed spelling of "mandatry" to "mandatory". | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a5` | reworded | Fixed contraction "cant" to "cannot". | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a7` | subsumed | Combined with b4 content and completed the incomplete sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a10` | superseded | Heading consolidated under "Workaround" and both sections (a10-a13 and b9-b12) u | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a11` | subsumed | Merged with b10-b12 into single workaround statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a12` | subsumed | Merged with b10-b12 into single workaround statement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-007`) |
| `a13` | subsumed | Merged with b10-b12 into single workaround statement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-008`) |
| `b1` | superseded | Base document title retained as it covers the broader issue. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b3` | dropped | Section heading subsumed into merged structure; content covered by b4. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b4` | subsumed | Combined with a7 to illustrate unsupported symbols with specific example. | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-004 came back MISSING (`B-004`) |
| `b5` | dropped | Context about stream name separation is not essential to the problem or solution | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`B-005`) |
| `b7` | dropped | Section heading removed; content (working as intended) not carried forward. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b8` | dropped | Status that no fix is planned is superseded by workaround provided. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b9` | superseded | Heading consolidated; content merged into unified workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | Merged with a12-a13 into single enhanced workaround statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | dropped | Section heading removed; duplicates content of b9 and b12. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b12` | subsumed | Merged with a12-a13 and enhanced with tag guidance from a13. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |


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
| Tokens | 17,663 in, 7,298 out |
| Cost | ~$0.05 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 51.5s |
| Generated | 2026-09-27T16:47:59+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
