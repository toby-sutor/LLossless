## Verdict

**2 finding(s).** In the structure: 1 verbatim violation, 1 declared loss over budget. The merge declared **1** drop(s) of 27 source segment(s), **3.7%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 25 |
| Claims extracted from `source_a.md` | 11 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **24/24** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **11/11** |
| Forward — `source_b.md` claims accounted for | **13/13** |
| Reverse — merge claims found in a source | **25/25** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **49/49** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None in the claims. The 2 finding(s) this run reports are structural and are listed under `## Structure` below.

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
| 1 | The document was authored by Rune Delacroix. | 3 | carried | 'Author: Rune Delacroix' in `merged.md` -- Document lists Rune Delacroix as author. |
| 2 | The document was updated on 2026-01-29. | 4 | carried | 'Updated: 2026-01-29' in `merged.md` -- Document states the update date directly. |
| 3 | Stream name is one of the mandatry field for every Nimbrel Probe agent. | 8 | carried | 'Stream name is one of the mandatory fields for every Nimbrel Probe agent' in `merged.md` -- Matches claim despite minor typo in claim text. |
| 4 | The stream name cant contain arbitrary symbols as documented in the linked page. | 8 | carried | "The stream name can't contain arbitrary symbols, as documented [here]" in `merged.md` -- States the restriction is documented via the linked page. |
| 5 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- Exact statement present in code block. |
| 6 | Stream names may only contain letters, digits, spaces and hyphens, and nothing else, or the agent refuses to start. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start' in `merged.md` -- Directly states the restriction and consequence. |
| 7 | One customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org. | 15 | carried | 'one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org' in `merged.md` -- Direct match to claim. |
| 8 | The customer's reporting keyed off the stream name string. | 15 | carried | 'their reporting keyed of it when' in `merged.md` -- States reporting keyed off the stream name string, despite sentence being truncated. |
| 9 | The workaround applies to all Nimbrel Probe agents. | 19 | carried | 'All Nimbrel Probe agents' in `merged.md` -- Environment section states workaround applies to all agents. |
| 10 | The first step of the workaround is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. | 25 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `merged.md` -- Matches first workaround step exactly. |
| 11 | The second step of the workaround is to carry the original name along as a global tag, so each trace keeps a link between the real name and the renamed one. | 26 | carried | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `merged.md` -- Matches second workaround step. |

### `source_b.md` -- 13 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 13 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The document was authored by Marlowe Ferrante. | 3 | carried | 'Author: Marlowe Ferrante' in `merged.md` -- Document lists Marlowe Ferrante as author. |
| 2 | The document was updated on 2026-02-03. | 4 | carried | 'Updated: 2026-02-03' in `merged.md` -- Document states this update date directly. |
| 3 | A stream name containing a . (dot), for example `checkout.web`, is refused by Nimbrel Probe. | 8 | carried | 'a stream name containing a . (dot), such as `checkout.web`, along with a number of other symbols, is refused' in `merged.md` -- Directly matches example given. |
| 4 | A number of other symbols are refused by Nimbrel Probe. | 8 | carried | 'along with a number of other symbols, is refused' in `merged.md` -- States other symbols are also refused. |
| 5 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | 10 | carried | 'is what separates one instrumented process from the next' in `merged.md` -- Directly matches claim. |
| 6 | Only letters, digits, spaces and hyphens are accepted in the Nimbrel Probe stream name. | 10 | carried | 'only letters, digits, spaces and hyphens are accepted' in `merged.md` -- Directly matches claim. |
| 7 | The Nimbrel Probe stream name has to match ^[A-Za-z0-9 -]+$. | 10 | carried | 'it has to match ^[A-Za-z0-9 -]+$' in `merged.md` -- Directly matches claim. |
| 8 | The stream name restriction is documented at https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name. | 10 | carried | 'https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name' in `merged.md` -- This URL is one of the linked documentation sources cited. |
| 9 | The issue is working as intended for now. | 14 | carried | 'This is working as intended for now' in `merged.md` -- Directly matches claim. |
| 10 | There is no fix at present for the issue. | 18 | carried | 'there is no fix planned' in `merged.md` -- States no fix is planned, matching claim of no fix at present. |
| 11 | The workaround is to rename the stream without the refused symbol. | 18 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `merged.md` -- Matches the workaround of renaming to remove refused symbols. |
| 12 | There is no fix at present for the issue. | 22 | carried | 'there is no fix planned' in `merged.md` -- Duplicate claim also supported by same statement of no planned fix. |
| 13 | The resolution is to rename the stream without the refused symbol. | 22 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `merged.md` -- Duplicate claim also supported by the same renaming step described as the resolution. |

### `merged.md` -- 25 claim(s): 0 invented, 0 contradicted, 0 supported in part, 25 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The author Rune Delacroix authored the document. | supported | `source_a.md` | 'Author: Rune Delacroix' in `source_a.md` -- Source a lists Rune Delacroix as author. |
| 2 | The document was updated 2026-01-29. | supported | `source_a.md` | 'Updated: 2026-01-29' in `source_a.md` -- Source a states this update date. |
| 3 | The author Marlowe Ferrante authored the document. | supported | `source_b.md` | 'Author: Marlowe Ferrante' in `source_b.md` -- Source b lists Marlowe Ferrante as author. |
| 4 | The document was updated 2026-02-03. | supported | `source_b.md` | 'Updated: 2026-02-03' in `source_b.md` -- Source b states this update date. |
| 5 | Stream name is one of the mandatory fields for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Directly states stream name is mandatory for every agent. |
| 6 | The stream name is what separates one instrumented process from the next. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Matches claim wording nearly verbatim. |
| 7 | The stream name can't contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols' in `source_a.md` -- Directly states this restriction. |
| 8 | This is documented at https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name. | supported | `source_a.md` | 'https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name' in `source_a.md` -- URL matches exactly as given in source a. |
| 9 | This is documented at https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name. | supported | `source_b.md` | 'https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name' in `source_b.md` -- URL matches exactly as given in source b. |
| 10 | Only letters, digits, spaces and hyphens are accepted in a stream name. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Directly states this restriction. |
| 11 | A stream name has to match ^[A-Za-z0-9 -]+$. | supported | `source_b.md` | 'it has to match ^[A-Za-z0-9 -]+$' in `source_b.md` -- Directly states the regex requirement. |
| 12 | A stream name containing a . (dot), such as checkout.web, is refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Directly states the dot example being refused. |
| 13 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Exact statement present in source a. |
| 14 | Only letters, digits, spaces and hyphens are allowed in stream names, and nothing else, or the agent refuses to start. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- Matches claim wording closely. |
| 15 | There is no fix planned for the stream name validation behavior. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- Cause and Resolution sections indicate no fix is planned currently. |
| 16 | One customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org' in `source_a.md` -- Matches claim almost verbatim. |
| 17 | The customer's reporting keyed off that string. | supported | `source_a.md` | 'their reporting keyed of it when' in `source_a.md` -- States the customer's reporting keyed off the string, matching the claim. |
| 18 | The issue applies to all Nimbrel Probe agents. | supported | `source_a.md` | 'All Nimbrel Probe agents' in `source_a.md` -- Environment section in source a states the issue applies to all agents. |
| 19 | The workaround is the only option since no fix is planned. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- Source b's Workaround/Resolution states no fix exists and renaming is the workaround, implying it is the only option. |
| 20 | The first step of the workaround is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Matches first workaround step exactly. |
| 21 | The second step of the workaround is to carry the original name along as a global tag. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag' in `source_a.md` -- Matches second workaround step. |
| 22 | Carrying the original name as a global tag means each trace keeps a link between the real name and the renamed one. | supported | `source_a.md` | 'so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Matches claim about global tag purpose. |
| 23 | Global tags are documented at https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags. | supported | `source_a.md` | 'https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags' in `source_a.md` -- URL matches exactly as given in source a. |
| 24 | There is an internal ticket at https://tickets.nimbrel.example/700Bb00000QrmTD. | supported | `source_a.md` | 'https://tickets.nimbrel.example/700Bb00000QrmTD' in `source_a.md` -- Internal ticket URL matches source a. |
| 25 | There is an internal ticket at https://tickets.nimbrel.example/700Bb00000LnqWs. | supported | `source_b.md` | 'https://tickets.nimbrel.example/700Bb00000LnqWs' in `source_b.md` -- Internal ticket URL matches source b. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **25** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **24**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 3 run(s) over 11 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 1 of 27 segments are declared dropped (3.7%), over the 3% budget

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

> **Over budget.** The merge declared **1** drop(s) of 27 source segment(s), **3.7%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **15** departure(s) from its sources. Checking them confirms 9, rejects 2, and leaves 4 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 1 of 27 source segment(s) declared gone, **3.7%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title chosen over this specific-case title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `a4` | reconciled | Combined with b5's process-separation fact into one sentence. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-003`) |
| `b5` | reconciled | Combined with a4's mandatory-field fact into one sentence. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-005`) |
| `a5` | reconciled | Combined with b6's regex/link statement into one sentence. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-004`) |
| `b6` | reconciled | Combined with a5's symbol-restriction statement into one sentence. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-006`, `B-007`, `B-008`) |
| `b4` | subsumed | Dot example folded into the Topic section as an illustration. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `b3` | superseded | Base heading used for the shared introductory section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b7` | dropped | No separate Cause heading kept; underlying fact moved via b8. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b8` | reworded | Cause statement folded into the Topic section. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-009`) |
| `a7` | reworded | Minor punctuation fix (stray comma spacing removed). | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`, `A-008`) |
| `b9` | superseded | Base heading used for the shared fix section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | duplicate | Resolution heading duplicates the Workaround heading's purpose. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a11` | reconciled | Combined with b10's no-fix statement into one lead sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b10` | reconciled | No-fix fact combined with a11's lead sentence; rename step matches a12. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Repeats b10's identical text under a different heading. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |


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
| Duration | 164.3s |
| Generated | 2026-09-27T19:53:17+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
