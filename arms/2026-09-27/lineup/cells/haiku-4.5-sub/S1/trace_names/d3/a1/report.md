## Verdict

**6 finding(s).** In the claims: 1 hallucinated. In the structure: 3 verbatim violation, 2 declared loss over budget. The merge declared **3** drop(s) of 27 source segment(s), **11.1%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 11 |
| Claims extracted from `source_a.md` | 5 |
| Claims extracted from `source_b.md` | 3 |
| Forward — source claims accounted for in the merge | **8/8** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **5/5** |
| Forward — `source_b.md` claims accounted for | **3/3** |
| Reverse — merge claims found in a source | **10/11** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **18/18** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Invented — in the merge, in neither source

- **M-011** (`merged.md:14`) — The validation constraint prevents stream names from matching product names.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: No source explicitly states that the validation constraint prevents stream names from matching product names as a general principle.

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
| 1 | Stream name is one of the mandatry field for every Nimbrel Probe agent | 8 | carried | 'Stream name is a mandatory field for every Nimbrel Probe agent.' in `merged.md` -- The reference text directly states this, supporting the claim despite the typo 'mandatry'. |
| 2 | The stream name cant contain arbitrary symbols as documented | 8 | carried | 'The stream name cannot contain arbitrary symbols as documented for [Java](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [browser](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name) agents.' in `merged.md` -- The reference text states this directly, matching the claim despite using 'cant' vs 'cannot'. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The reference text provides this validation rule explicitly. |
| 4 | Stream names contain letters, digits, spaces and hyphens only, and nothing else | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The reference text plainly enumerates these as the only allowed characters. |
| 5 | The agent refuses to start if the stream name contains unsupported characters | 12 | carried | 'or the agent refuses to start.' in `merged.md` -- The reference text states the agent refuses to start when stream names contain unsupported characters. |

### `source_b.md` -- 3 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Stream names containing a dot, for example checkout.web, along with a number of other symbols are refused by Nimbrel Probe. | 8 | carried | 'Characters such as dots are refused; for example, stream names like checkout.web cannot be used.' in `merged.md` -- The phrase 'Characters such as' indicates multiple character types are refused, supporting the claim. |
| 2 | The Nimbrel Probe stream name is what seperates one instrumented process from the next. | 10 | carried | 'The stream name separates one instrumented process from another.' in `merged.md` -- The reference text states this directly, matching the claim despite the typo 'seperates'. |
| 3 | Only letters, digits, spaces and hyphens are accepted for Nimbrel Probe stream names. | 10 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The reference text plainly states only these characters are accepted for stream names. |

### `merged.md` -- 11 claim(s): 1 invented, 0 contradicted, 0 supported in part, 10 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 11 | The validation constraint prevents stream names from matching product names. | invented | -- | No source explicitly states that the validation constraint prevents stream names from matching product names as a general principle. |
| 1 | Stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- source_a.md directly states this claim with a minor spelling variation. |
| 2 | The stream name cannot contain arbitrary symbols as documented for [Java](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name) and [browser](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name) agents. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols as documented' in `source_a.md` -- source_a.md documents this constraint for Java agents; source_b.md documents it for browser agents. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- source_a.md directly states this claim verbatim. |
| 4 | Stream names contain letters, digits, spaces and hyphens only, and nothing else. | supported | `source_a.md` | 'Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- source_a.md directly states that stream names contain only these character types. |
| 5 | The agent refuses to start if stream names contain unsupported characters. | supported | `source_a.md` | 'or the agent refuses to start.' in `source_a.md` -- source_a.md states the agent refuses to start if unsupported characters are used. |
| 6 | The stream name separates one instrumented process from another. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- source_b.md directly states this claim with a minor spelling variation. |
| 7 | Characters such as dots are refused in stream names. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- source_b.md explicitly states that dots are refused in stream names. |
| 8 | Stream names like checkout.web cannot be used. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- source_b.md explicitly names checkout.web as an example of a refused stream name. |
| 9 | Some customers need the stream name to match their product name. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org and their reporting keyed of it' in `source_a.md` -- source_a.md describes a customer needing the stream name to match their product name for reporting purposes. |
| 10 | Product names are used in reporting throughout customers' organizations. | supported | `source_a.md` | 'because that string was the product name in use everywhere in the org and their reporting keyed of it' in `source_a.md` -- source_a.md indicates that product names are used throughout organizations and reporting depends on them. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **11** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **8**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 10 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a5` (`source_a.md`) — link '[here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name)' does not survive into the merge unchanged
- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged
- `b6` (`source_b.md`) — link '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 4 absent segments are declared replaced by the same replacement (a11, a12, a13, b10), over the ceiling of 3. One replacement standing in for that many segments has not replaced them, it has dropped them: the detail it names is gone from the document
- 3 of 27 segments are declared dropped (11.1%), over the 3% budget

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

> **Over budget.** The merge declared **3** drop(s) of 27 source segment(s), **11.1%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **21** departure(s) from its sources. Checking them confirms 10, rejects 1, and leaves 10 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 3 of 27 source segment(s) declared gone, **11.1%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Reworded for clarity while retaining factual content. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a5` | subsumed | Combined with b6 browser documentation into single statement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-002`) |
| `a6` | reworded | Verbatim block integrated into prose structure. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`, `A-004`, `A-005`) |
| `a7` | reworded | Incomplete sentence completed for clarity. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a11` | subsumed | Phrase subsumed in the complete two-step instruction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a12` | subsumed | First step subsumed in unified instruction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a13` | subsumed | Second step subsumed in unified instruction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a14` | reworded | Ticket link from b13 added to internal notes. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b1` | superseded | Base document title retained as more general. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b2` | superseded | Base document author and date retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | superseded | Base document section structure retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | subsumed | Example integrated into Topic section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`) |
| `b5` | subsumed | Statement integrated into Topic section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`) |
| `b6` | subsumed | Content combined with a5 into single documentation reference. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b7` | dropped | Section heading consolidated under base structure. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b8` | subsumed | Statement integrated into Topic section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b9` | dropped | Section heading consolidated under base structure. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b10` | subsumed | Rename step part of complete two-step solution. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | dropped | Section heading consolidated; content is duplicate. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b12` | duplicate | Identical content to b10. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b13` | subsumed | Ticket link merged into internal notes section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |


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
| Duration | 611.3s |
| Generated | 2026-09-27T20:03:29+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
