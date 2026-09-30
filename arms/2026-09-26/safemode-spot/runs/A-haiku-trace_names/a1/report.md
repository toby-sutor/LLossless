## Verdict

**4 finding(s).** In the claims: 1 dropped. In the structure: 1 undeclared absence, 1 verbatim violation, 1 declared loss over budget. The merge declared **3** drop(s) of 27 source segment(s), **11.1%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 9 |
| Claims extracted from `source_a.md` | 7 |
| Claims extracted from `source_b.md` | 5 |
| Forward — source claims accounted for in the merge | **11/12** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **7/7** |
| Forward — `source_b.md` claims accounted for | **4/5** |
| Reverse — merge claims found in a source | **9/9** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **19/20** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-004** (`source_b.md:18`) — There is no fix at present
  - judged against: `merged.md`
  - rationale: The reference provides a workaround but does not state whether a permanent fix exists or not.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 7 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Stream name is one of the mandatry field for every Nimbrel Probe agent. | 8 | carried | 'Stream name is one of the mandatory fields for every Nimbrel Probe agent' in `merged.md` -- The claim and reference state the same fact despite the claim's spelling variation in 'mandatry'; the meaning is identical. |
| 2 | The stream name cant contain arbitrary symbols as documented | 8 | carried | 'Stream names cannot contain arbitrary symbols' in `merged.md` -- The reference directly states that stream names cannot contain arbitrary symbols, matching the claim's assertion. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- Direct textual match between claim and reference text. |
| 4 | Stream names can contain letters, digits, spaces and hyphens only, and nothing else. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The reference explicitly states these are the only characters allowed in stream names. |
| 5 | If a stream name contains anything other than letters, digits, spaces and hyphens, the agent refuses to start. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start' in `merged.md` -- The reference establishes the conditional: if stream name contains only permitted characters, otherwise agent refuses to start. |
| 6 | If the stream is renamed to drop unsupported symbols, the Nimbrel Probe agent will register. | 25 | carried | 'Rename the stream to use only supported characters so the Nimbrel Probe agent will register.' in `merged.md` -- The reference identifies this as the solution to enable agent registration with unsupported stream names. |
| 7 | The original name can be carried along as a global tag so that each trace keeps a link between the real name and the renamed stream name. | 26 | carried | 'carry the original name as a global tag, preserving the link between the renamed stream and its actual name' in `merged.md` -- The reference states that carrying the original name as a tag preserves the connection between renamed stream and actual name. |

### `source_b.md` -- 5 claim(s): 1 dropped, 0 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 4 | There is no fix at present | 18 | dropped | The reference provides a workaround but does not state whether a permanent fix exists or not. |
| 1 | Stream names containing a dot and other symbols are refused by Nimbrel Probe | 8 | carried | 'Stream names cannot contain arbitrary symbols—dots, for example' in `merged.md` -- Cannot contain dots and other symbols is equivalent to saying they are refused by the system. |
| 2 | Nimbrel Probe stream names separate one instrumented process from the next | 10 | carried | 'is what separates one instrumented process from the next' in `merged.md` -- The reference directly states that stream names separate instrumented processes. |
| 3 | Only letters, digits, spaces and hyphens are accepted in Nimbrel Probe stream names | 10 | carried | 'can only use letters, digits, spaces and hyphens' in `merged.md` -- Only these characters can be used means only these are accepted. |
| 5 | The workaround is to rename the stream without the refused symbol | 18 | carried | 'Rename the stream to use only supported characters' in `merged.md` -- The reference identifies renaming the stream without unsupported symbols as the workaround. |

### `merged.md` -- 9 claim(s): 0 invented, 0 contradicted, 0 supported in part, 9 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Stream name is one of the mandatory fields for every Nimbrel Probe agent | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source A directly states that stream name is one of the mandatory fields for every Nimbrel Probe agent. |
| 2 | Stream name is what separates one instrumented process from the next | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source B explicitly states the role of stream names in separating instrumented processes. |
| 3 | Stream names cannot contain arbitrary symbols (dots are an example) | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols' in `source_a.md` -- Source A states stream names cannot contain arbitrary symbols; source B provides dots as a specific example of refused symbols. |
| 4 | Stream names can only use letters, digits, spaces and hyphens | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else' in `source_a.md` -- Source A explicitly specifies the only allowed characters in stream names. |
| 5 | Stream names are validated against ^[A-Za-z0-9 -]+$ | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$' in `source_a.md` -- Source A specifies the exact regex pattern used for stream name validation. |
| 6 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source A states both the regex pattern and that validation occurs before agent registration. |
| 7 | Only letters, digits, spaces and hyphens are allowed in stream names | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Source B directly specifies the only permitted characters for stream names. |
| 8 | The stream name constraint is by design | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- Source B indicates the constraint is working as intended, confirming intentional implementation by design. |
| 9 | A workaround is available for product names in use across an organization that do not conform to stream name restrictions | supported | `source_a.md` | 'However , one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org and their reporting keyed of it when\n\nA way round it that works\n\n1) Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register\n2) Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md`, **transcription_error** -- Source A describes a scenario where a product name used across the organization does not conform, and provides a workaround using renaming and global tags. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **9** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **12**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 9 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Absent and undeclared — in a source, not in the merge, and no record explains it

- `a13` (`source_a.md`) — 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags' is not in the merge and no disposition record explains it (nearest merge segment m13 at 0.43)

  ```text
  In the source: Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 3 of 27 segments are declared dropped (11.1%), over the 3% budget

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

> **Over budget.** The merge declared **3** drop(s) of 27 source segment(s), **11.1%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **19** departure(s) from its sources. Checking them confirms 10, rejects 1, and leaves 8 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 3 of 27 source segment(s) declared gone, **11.1%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Fixed spelling and grammar errors. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a5` | subsumed | Combined with b4 example and b6 validation details. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-002`) |
| `a7` | subsumed | Incorporated as context for why workaround is needed. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a11` | subsumed | Merged into solution description. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a12` | reworded | Converted from numbered list to prose format. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`) |
| `a14` | reworded | Added second ticket reference from b13. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b1` | superseded | Base document's more general title preferred. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b2` | superseded | Base document's metadata retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | subsumed | Content consolidated into base document structure. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b4` | subsumed | Dot example merged into problem description. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`) |
| `b5` | subsumed | Role definition integrated into topic section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-002`) |
| `b6` | subsumed | Validation merged with a5; second documentation link preserved. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b7` | dropped | Heading consolidated; structure follows base document. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b8` | subsumed | Design intent integrated into topic section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b9` | dropped | Heading consolidated into instructions/answer section. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b10` | subsumed | Workaround merged into more complete solution. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | dropped | Duplicate heading removed per base structure. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b12` | duplicate | Duplicate of b10; workaround integrated into solution. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `b13` | subsumed | Merged with a14; second ticket reference added. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bbb0be176544 (command) -- Claude Code - Haiku |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | haiku -> claude-haiku-4-5-20251001 |
| Model (decompose) | haiku -> claude-haiku-4-5-20251001 |
| Model (verify) | haiku -> claude-haiku-4-5-20251001 |
| Structured output | prompt (probed) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=low, merge=medium, verify=low |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 6cc1b1703658 |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 609.9s |
| Generated | 2026-09-26T16:04:33+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `5afca8163bfa` |
| Prompt | `prompts/verify_reverse.md` `cb2face6b7f4` |

> **Document content was handed to a program on this machine (`Claude Code - Haiku`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
