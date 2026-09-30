## Verdict

**3 finding(s).** In the claims: 2 contradicted. In the structure: 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 18 |
| Claims extracted from `source_a.md` | 9 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **20/22** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **9/9** |
| Forward — `source_b.md` claims accounted for | **11/13** |
| Reverse — merge claims found in a source | **18/18** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **40/40** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:3` says: The document's author is Marlowe Ferrante.
  - `merged.md` says: 'Author: Rune Delacroix' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document names a different author than claimed.
- **B-002** -- the two documents disagree
  - `source_b.md:4` says: The document was updated 2026-02-03.
  - `merged.md` says: 'Updated: 2026-01-29' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document states a different update date than claimed.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 9 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Stream name is one of the mandatory fields for every Nimbrel Probe agent. | 8 | carried | 'Stream name is one of the mandatory fields for every Nimbrel Probe agent, and it is what separates one instrumented process from the next.' in `merged.md` -- Directly stated. |
| 2 | The stream name cannot contain arbitrary symbols as documented at https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name. | 8 | carried | 'The stream name cannot contain arbitrary symbols, as documented [here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name)' in `merged.md` -- Directly stated with matching URL. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- Directly stated verbatim. |
| 4 | Stream names may only contain letters, digits, spaces and hyphens. | 12 | carried | 'Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `merged.md` -- Directly stated. |
| 5 | The agent refuses to start if the stream name contains anything other than letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start' in `merged.md` -- Directly states the refusal condition matches the claim. |
| 6 | One customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org. | 15 | carried | 'One customer wanted the stream name left exactly as it stood, because that string was the product name in use everywhere in the org and their reporting keyed off it.' in `merged.md` -- Directly stated. |
| 7 | The customer's reporting keyed off the stream name string. | 15 | carried | 'their reporting keyed off it' in `merged.md` -- Directly stated. |
| 8 | A workaround involves renaming the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. | 25 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.' in `merged.md` -- Directly stated as workaround step. |
| 9 | A workaround involves carrying the original name along as a global tag, so each trace keeps a link between the real name and the renamed one. | 26 | carried | 'Then carry the original name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `merged.md` -- Directly stated as workaround step. |

### `source_b.md` -- 13 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 11 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The document's author is Marlowe Ferrante. | 3 | contradicted | 'Author: Rune Delacroix' in `merged.md` -- The document names a different author than claimed. |
| 2 | The document was updated 2026-02-03. | 4 | contradicted | 'Updated: 2026-01-29' in `merged.md` -- The document states a different update date than claimed. |
| 3 | Stream names containing a . (dot), for example `checkout.web`, are refused by Nimbrel Probe. | 8 | carried | 'A stream name containing a dot (for example `checkout.web`), along with a number of other symbols, is refused for this reason.' in `merged.md` -- Directly stated. |
| 4 | A number of other symbols besides the dot are also refused by Nimbrel Probe. | 8 | carried | 'along with a number of other symbols, is refused for this reason' in `merged.md` -- Directly stated. |
| 5 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | 10 | carried | 'it is what separates one instrumented process from the next' in `merged.md` -- Directly stated. |
| 6 | Only letters, digits, spaces and hyphens are accepted in the Nimbrel Probe stream name. | 10 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- Directly stated. |
| 7 | The Nimbrel Probe stream name has to match the pattern ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- Directly stated. |
| 8 | This stream name requirement is documented at https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name. | 10 | carried | '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' in `merged.md` -- Directly cited as documentation source for the requirement. |
| 9 | The behavior is working as intended for now. | 14 | carried | 'Working as intended for now.' in `merged.md` -- Directly stated under Cause. |
| 10 | There is no fix at present for the dot-in-stream-name issue. | 18 | carried | 'There is no fix at present.' in `merged.md` -- Directly stated, applying to the described dot-in-stream-name issue. |
| 11 | The workaround is to rename the stream without the refused symbol. | 18 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.' in `merged.md` -- Directly stated as the workaround. |
| 12 | There is no fix at present for the resolution. | 22 | carried | 'There is no fix at present.' in `merged.md` -- Directly stated regarding the resolution. |
| 13 | The resolution is to rename the stream without the refused symbol. | 22 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.' in `merged.md` -- Directly stated as the resolution/workaround. |

### `merged.md` -- 18 claim(s): 0 invented, 0 contradicted, 0 supported in part, 18 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Stream name is one of the mandatory fields for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Directly stated in source_a. |
| 2 | The stream name is what separates one instrumented process from the next. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Directly stated in source_b, with minor spelling variant. |
| 3 | The stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols' in `source_a.md` -- Directly stated in source_a. |
| 4 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Directly stated in source_a. |
| 5 | Stream names may only contain letters, digits, spaces and hyphens. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Both sources state the same restriction. |
| 6 | The agent refuses to start if the stream name contains anything other than letters, digits, spaces and hyphens. | supported | `source_a.md` | 'or the agent refuses to start' in `source_a.md` -- Directly stated in source_a's quoted config text. |
| 7 | A stream name containing a dot is refused for this reason. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source_b states dots are refused due to the same regex restriction explained immediately after. |
| 8 | checkout.web is an example of a stream name containing a dot. | supported | `source_b.md` | 'checkout.web' in `source_b.md` -- Directly given as the example in source_b. |
| 9 | A stream name containing a number of other symbols besides a dot is refused for this reason. | supported | `source_b.md` | 'along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source_b states other symbols besides the dot are also refused for the same regex reason. |
| 10 | One customer wanted the stream name left exactly as it stood. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood' in `source_a.md` -- Directly stated in source_a. |
| 11 | That customer's string was the product name in use everywhere in their organization. | supported | `source_a.md` | 'because that string was the product name in use everywhere in the org' in `source_a.md` -- Directly stated in source_a. |
| 12 | That customer's reporting keyed off the stream name string. | supported | `source_a.md` | 'their reporting keyed of it when' in `source_a.md` -- Directly stated in source_a. |
| 13 | This issue applies to all Nimbrel Probe agents. | supported | `source_a.md` | 'All Nimbrel Probe agents' in `source_a.md` -- Source_a's Environment section states the issue applies to all Nimbrel Probe agents. |
| 14 | The stream name symbol restriction is working as intended for now. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- Directly stated in source_b's Cause section. |
| 15 | A way to work around the issue is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Directly stated as step 1 in source_a's instructions. |
| 16 | The workaround involves carrying the original name along as a global tag. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag' in `source_a.md` -- Directly stated as step 2 in source_a's instructions. |
| 17 | Carrying the original name as a global tag keeps a link between the real name and the renamed one for each trace. | supported | `source_a.md` | 'so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Directly stated in source_a. |
| 18 | There is no fix at present for this issue. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- Directly stated in source_b's Resolution section. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **18** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **22**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 7 run(s) over 16 attributed segment(s) — sources interleaved. 5 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **17** departure(s) from its sources. Checking them confirms 11, rejects 2, and leaves 4 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reconciled | Combined with b5 into one sentence about stream name's role. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-001`) |
| `b5` | reconciled | Combined with a4 into one sentence about stream name's role. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-005`) |
| `a5` | reconciled | Merged with b6's link into one sentence with both references. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-002`) |
| `b6` | reconciled | Link kept alongside a5; regex restated in a6's verbatim block. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-006`, `B-007`, `B-008`) |
| `b4` | reworded | Typo 'exampe' fixed and rephrased as a specific instance. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `a7` | reworded | Grammar and dangling clause fixed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`, `A-007`) |
| `b7` | duplicate | Heading text identical to merged heading. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b8` | reworded | Period added; content unchanged. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-009`) |
| `a11` | reworded | Colon added for readability. | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a13` | reworded | Link joined onto same line with a colon. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`) |
| `b9` | superseded | Consolidated into base's heading for the fix. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Consolidated into base's heading for the fix. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | Same rename instruction as a12. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Repeats b10, which duplicates a12's instruction. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b1` | superseded | Base title chosen instead. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b2` | superseded | Base document's authorship and date kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`, `B-002`) |
| `b3` | superseded | Consolidated into base's heading for this section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |


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
| Duration | 130.0s |
| Generated | 2026-09-27T18:06:50+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
