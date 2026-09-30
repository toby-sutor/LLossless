## Verdict

**7 finding(s).** In the claims: 2 dropped. In the structure: 1 false departure, 3 verbatim violation, 1 declared loss over budget. The merge declared **3** drop(s) of 27 source segment(s), **11.1%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 13 |
| Claims extracted from `source_a.md` | 5 |
| Claims extracted from `source_b.md` | 5 |
| Forward — source claims accounted for in the merge | **8/10** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **5/5** |
| Forward — `source_b.md` claims accounted for | **3/5** |
| Reverse — merge claims found in a source | **13/13** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **21/21** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-004** (`source_b.md:18`) — There is no fix at present.
  - judged against: `merged.md`
  - rationale: The reference text provides a solution but does not state that there is no fix at present.
- **B-005** (`source_b.md:22`) — There is no fix at present.
  - judged against: `merged.md`
  - rationale: The reference text provides a solution but does not state that there is no fix at present.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 5 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Stream name is one of the mandatry field for every Nimbrel Probe agent. | 8 | carried | 'Stream name is a mandatory field for every Nimbrel Probe agent' in `merged.md` -- The reference text directly states that stream name is a mandatory field for every Nimbrel Probe agent, supporting the claim despite the typo 'mandatry'. |
| 2 | The stream name cant contain arbitrary symbols as documented. | 8 | carried | 'The stream name cannot contain arbitrary symbols.' in `merged.md` -- The reference text states this exactly, with 'cannot' matching the informal 'cant' in the claim. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- This exact sentence appears in the reference text. |
| 4 | Stream names can only contain letters, digits, spaces and hyphens, and nothing else, or the agent refuses to start. | 12 | carried | 'Only letters, digits, spaces and hyphens are accepted; anything else causes the agent to refuse to start.' in `merged.md` -- The reference text states this constraint and the consequence for non-compliant names. |
| 5 | One customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org and their reporting keyed of it. | 15 | carried | 'One customer wanted to keep a stream name exactly as it stood because that string was their product name in use throughout their organization and their reporting depended on it.' in `merged.md` -- The reference text conveys the same meaning despite different wording ('keyed of' vs 'depended on', 'everywhere' vs 'throughout'). |

### `source_b.md` -- 5 claim(s): 2 dropped, 0 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 4 | There is no fix at present. | 18 | dropped | The reference text provides a solution but does not state that there is no fix at present. |
| 5 | There is no fix at present. | 22 | dropped | The reference text provides a solution but does not state that there is no fix at present. |
| 1 | Stream names containing dots and other symbols are refused by Nimbrel Probe. | 8 | carried | 'Stream names containing a dot (for example, `checkout.web`) and other characters are refused by Nimbrel Probe.' in `merged.md` -- The reference text states that dots and other characters are refused, supporting the claim's reference to 'dots and other symbols'. |
| 2 | The Nimbrel Probe stream name separates one instrumented process from the next. | 10 | carried | 'it separates one instrumented process from another' in `merged.md` -- The reference text states this role of stream names in the opening paragraph. |
| 3 | Only letters, digits, spaces and hyphens are accepted in stream names. | 10 | carried | 'Only letters, digits, spaces and hyphens are accepted' in `merged.md` -- The reference text directly states what characters are accepted in stream names. |

### `merged.md` -- 13 claim(s): 0 invented, 0 contradicted, 0 supported in part, 13 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source A directly states that stream name is a mandatory field for every Nimbrel Probe agent, using identical meaning despite spelling variation. |
| 2 | The stream name separates one instrumented process from another. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source B explicitly states that the stream name separates one instrumented process from another, matching the claim exactly. |
| 3 | The stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols as documented' in `source_a.md` -- Source A directly states that the stream name cannot contain arbitrary symbols, matching the claim with identical meaning. |
| 4 | Stream names containing a dot (for example, `checkout.web`) and other characters are refused by Nimbrel Probe. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source B explicitly states that stream names containing a dot (such as checkout.web) and other symbols are refused by Nimbrel Probe. |
| 5 | Stream names are validated against the pattern below before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source A states that stream names are validated against a pattern before the agent registers, directly supporting the claim. |
| 6 | Only letters, digits, spaces and hyphens are accepted. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Source B explicitly lists the exact characters accepted for stream names, directly matching the claim. |
| 7 | Anything else causes the agent to refuse to start. | supported | `source_a.md` | 'or the agent refuses to start.' in `source_a.md` -- Source A states that invalid stream names cause the agent to refuse to start, directly supporting the claim. |
| 8 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source A provides the exact regex pattern and timing of validation that the claim states. |
| 9 | One customer wanted to keep a stream name exactly as it stood. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood' in `source_a.md` -- Source A directly states that one customer wanted to keep the stream name exactly as it stood. |
| 10 | That stream name string was the customer's product name in use throughout the customer's organization. | supported | `source_a.md` | 'that string was the product name in use everywhere in the org' in `source_a.md` -- Source A states the stream name string was the product name in use throughout the organization, matching the claim. |
| 11 | The customer's reporting depended on that stream name. | supported | `source_a.md` | 'and their reporting keyed of it when' in `source_a.md` -- Source A indicates that customer reporting depended on the stream name, using the phrase 'reporting keyed of it'. |
| 12 | If the stream is renamed to contain only supported symbols, the Nimbrel Probe agent will register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Source A provides this as a solution, stating that renaming the stream enables the agent to register. |
| 13 | A global tag allows each trace to maintain a link between the original name and the renamed name. | supported | `source_a.md` | 'carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Source A describes using a global tag to maintain a link between original and renamed stream names in traces. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **13** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **10**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 5 run(s) over 10 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a10` (`source_a.md`) — 'Instructions/Answer' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Instructions/Answer
  In the merge:  Rename the stream to contain only supported symbols so the Nimbrel Probe agent will register.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a5` (`source_a.md`) — link '[here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name)' does not survive into the merge unchanged
- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged
- `b6` (`source_b.md`) — link '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 3 of 27 segments are declared dropped (11.1%), over the 3% budget

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

> **Over budget.** The merge declared **3** drop(s) of 27 source segment(s), **11.1%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **21** departure(s) from its sources. Checking them confirms 10, rejects 1, and leaves 10 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 3 of 27 source segment(s) declared gone, **11.1%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | superseded | More recent metadata from b2 selected. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a4` | subsumed | Combined with b5 in opening paragraph. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-001`) |
| `a5` | subsumed | Merged into Topic validation description. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-002`) |
| `a7` | reworded | Completed incomplete source sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-005`) |
| `a10` | subsumed | Heading and intro merged into instructions prose. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a11` | subsumed | Preamble merged into flowing instructions. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a12` | subsumed | Bullet point converted to prose. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a13` | subsumed | Solution step and documentation integrated. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a14` | subsumed | Combined with b13 ticket reference. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b1` | superseded | Base document title selected. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b3` | subsumed | Consolidated under base section heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b4` | subsumed | Merged into opening paragraph. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`) |
| `b5` | subsumed | Combined with a4 about stream name role. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`) |
| `b6` | subsumed | Merged into unified validation explanation. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b7` | dropped | Base structure does not include Cause section. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b8` | subsumed | Integrated into validation paragraph. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b9` | dropped | Base structure does not include Workaround heading. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b10` | subsumed | Merged with a12 into unified instructions. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | dropped | Base structure does not include Resolution heading. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b12` | duplicate | Duplicate of b10; single version retained. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b13` | subsumed | Combined with a14 preserving both ticket references. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |


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
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 605.6s |
| Generated | 2026-09-27T19:09:37+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
