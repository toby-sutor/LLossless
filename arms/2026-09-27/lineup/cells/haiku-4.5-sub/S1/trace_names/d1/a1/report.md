## Verdict

**9 finding(s).** In the claims: 2 contradicted. In the structure: 1 undeclared rewording, 5 verbatim violation, 1 declared loss over budget. The merge declared **4** drop(s) of 27 source segment(s), **14.8%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself. The 2 claim(s) they cost are listed in the review queue below.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 8 |
| Claims extracted from `source_a.md` | 6 |
| Claims extracted from `source_b.md` | 5 |
| Forward — source claims accounted for in the merge | **7/11** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **4/6** |
| Forward — `source_b.md` claims accounted for | **3/5** |
| Reverse — merge claims found in a source | **8/8** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **17/17** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-004** -- the two documents disagree
  - `source_b.md:18` says: No fix is available at the present time.
  - `merged.md` says: 'A way round it that works:' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text presents a working solution for the problem, contradicting the claim that no fix is available.
- **B-005** -- the two documents disagree
  - `source_b.md:22` says: No fix is available at the present time.
  - `merged.md` says: 'A way round it that works:' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text presents a working solution for the problem, contradicting the claim that no fix is available.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 6 claim(s): 2 dropped, 0 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 5 | One customer wanted the stream name left exactly as it stood. | 15 | dropped | The reference text does not mention any specific customer or their requirements regarding stream names. |
| 6 | The stream name was the product name in use everywhere in the org. | 15 | dropped | The reference text does not describe the stream name as a product name used throughout the organization. |
| 1 | Stream name is one of the mandatory fields for every Nimbrel Probe agent. | 8 | carried | 'Stream name is one of the mandatory fields for every Nimbrel Probe agent' in `merged.md` -- The reference text directly states this claim. |
| 2 | The stream name cannot contain arbitrary symbols. | 8 | carried | 'Stream names containing unsupported symbols—such as dots in `checkout.web` and others—are refused by Nimbrel Probe' in `merged.md` -- The text states stream names containing unsupported symbols are refused, meaning they cannot contain such symbols. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against `^[A-Za-z0-9 -]+$`: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `merged.md` -- The text states validation occurs and the agent refuses to start if invalid, necessarily preceding registration. |
| 4 | The agent refuses to start if stream names contain characters other than letters, digits, spaces and hyphens. | 12 | carried | 'Stream names are validated against `^[A-Za-z0-9 -]+$`: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `merged.md` -- The text directly states the agent refuses to start when stream names contain invalid characters. |

### `source_b.md` -- 5 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 4 | No fix is available at the present time. | 18 | contradicted | 'A way round it that works:' in `merged.md` -- The text presents a working solution for the problem, contradicting the claim that no fix is available. |
| 5 | No fix is available at the present time. | 22 | contradicted | 'A way round it that works:' in `merged.md` -- The text presents a working solution for the problem, contradicting the claim that no fix is available. |
| 1 | Stream names containing dots and other symbols are refused by Nimbrel Probe. | 8 | carried | 'Stream names containing unsupported symbols—such as dots in `checkout.web` and others—are refused by Nimbrel Probe' in `merged.md` -- The text explicitly states stream names containing dots and other symbols are refused by Nimbrel Probe. |
| 2 | Nimbrel Probe stream names are what separate one instrumented process from another. | 10 | carried | 'Stream name is one of the mandatory fields for every Nimbrel Probe agent and separates one instrumented process from another.' in `merged.md` -- The text states that stream names separate one instrumented process from another. |
| 3 | Only letters, digits, spaces, and hyphens are accepted in Nimbrel Probe stream names. | 10 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The text specifies only these characters are accepted in Nimbrel Probe stream names. |

### `merged.md` -- 8 claim(s): 0 invented, 0 contradicted, 0 supported in part, 8 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Stream name is one of the mandatory fields for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source A states this claim with identical meaning, using the same wording including the spelling variant mandatry. |
| 2 | Stream name separates one instrumented process from another. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source B directly states that stream name separates one instrumented process from another. |
| 3 | Stream names containing unsupported symbols are refused by Nimbrel Probe. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source B explicitly states that stream names containing unsupported symbols are refused by Nimbrel Probe. |
| 4 | Stream names are validated against `^[A-Za-z0-9 -]+$`. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source A directly states the validation pattern for stream names. |
| 5 | The stream name pattern allows letters, digits, spaces and hyphens only. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else' in `source_a.md` -- Source A plainly describes that only letters, digits, spaces and hyphens are allowed in stream names. |
| 6 | The Nimbrel Probe agent refuses to start if stream names don't comply with the validation. | supported | `source_a.md` | 'or the agent refuses to start.' in `source_a.md` -- Source A states the agent refuses to start when stream names do not comply with the validation pattern. |
| 7 | The Nimbrel Probe agent will register if the stream is renamed to drop unsupported symbols. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Source A explicitly states that renaming the stream to remove unsupported symbols allows the agent to register. |
| 8 | When the original name is carried along as a global tag, each trace keeps a link between the real name and the renamed stream. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Source A states that carrying the original name as a global tag maintains a link between the real and renamed stream names. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **8** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **11**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 1 run(s) over 11 attributed segment(s) — not conclusive on this evidence base. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `b2` (`source_b.md`) — 'Author: Marlowe Ferrante Updated: 2026-02-03' is reworded in the merge and no disposition record explains it (nearest merge segment m2 at 0.70)

  ```text
  In the source: Author: Marlowe Ferrante Updated: 2026-02-03
  In the merge:  Author: Rune Delacroix Updated: 2026-01-29
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a5` (`source_a.md`) — link '[here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name)' does not survive into the merge unchanged
- `a6` (`source_a.md`) — code_block '```\nStream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.\n```' does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '2026-02-03' does not survive into the merge unchanged
- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged
- `b6` (`source_b.md`) — link '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 4 of 27 segments are declared dropped (14.8%), over the 3% budget

## Review queue

**2** claim(s) the merge declared dropped and the forward pass confirms are gone. Each is a decision to review — put the fact back, or agree it stays out — and none of them is counted as a finding above.

- **A-005** (`source_a.md:15`) — One customer wanted the stream name left exactly as it stood.
  - left out of: `a7`
  - the merge's reason: Incomplete sentence; context not essential.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not mention any specific customer or their requirements regarding stream names.
- **A-006** (`source_a.md:15`) — The stream name was the product name in use everywhere in the org.
  - left out of: `a7`
  - the merge's reason: Incomplete sentence; context not essential.
  - confirmed absent: the forward pass looked for this claim in `merged.md` and did not find it -- The reference text does not describe the stream name as a product name used throughout the organization.

> **Over budget.** The merge declared **4** drop(s) of 27 source segment(s), **14.8%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **19** departure(s) from its sources. Checking them confirms 11, rejects 2, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 4 of 27 source segment(s) declared gone, **14.8%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reconciled | Combined with b5; states purpose and requirement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-001`) |
| `a5` | reworded | Integrated with b4 and b6; both doc links preserved. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a6` | reworded | Converted from code block to inline prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`, `A-004`) |
| `a7` | dropped | Incomplete sentence; context not essential. | **confirmed** | declared 'dropped' and every claim from it came back MISSING (`A-005`, `A-006`) |
| `a12` | reworded | Normalized list formatting from ) to . | **rejected** | declared 'reworded', and its text is in the merge (no claim traced to it) |
| `a13` | reworded | Fixed 'orignal' typo; streamlined text. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a14` | reworded | Merged with b13; both tickets included. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b1` | superseded | Base document's title used. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b3` | superseded | Base section structure used for Issue Description. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | subsumed | Example incorporated into merged topic. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`) |
| `b5` | reconciled | Combined with a4; states purpose and requirement. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-002`) |
| `b6` | superseded | a6's version of validation rules used. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-003`) |
| `b7` | dropped | Cause section not used in base structure. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b8` | dropped | Status doesn't inform workaround decision. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b9` | superseded | Base section structure used for Workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | superseded | a's more complete solution used instead. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | dropped | Resolution section not used in base. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b12` | duplicate | Duplicate of b10; a's solution used. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b13` | reworded | Merged with a14; both tickets included. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |


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
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | unknown (8 call(s) reported no usage) |
| Cost | unmeasured (8 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 2 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 718.3s |
| Generated | 2026-09-27T18:02:28+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
