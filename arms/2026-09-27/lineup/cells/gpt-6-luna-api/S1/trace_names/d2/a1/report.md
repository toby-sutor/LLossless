## Verdict

**1 finding(s).** In the claims: 1 partially dropped.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 13 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **19/20** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **11/12** (1 in part) |
| Forward — `source_b.md` claims accounted for | **8/8** |
| Reverse — merge claims found in a source | **13/13** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **33/33** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **A-011** (`source_a.md:25`) — The Nimbrel Probe agent will register after the stream is renamed to drop the unsupported symbols.
  - evidence: 'Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text says renaming lets the agent register, but does not guarantee that it will register.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 0 contradicted, 1 carried in part, 11 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 11 | The Nimbrel Probe agent will register after the stream is renamed to drop the unsupported symbols. | 25 | carried in part | 'Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register.' in `merged.md` -- The text says renaming lets the agent register, but does not guarantee that it will register. |
| 1 | Rune Delacroix is the author. | 3 | carried | 'Author: Rune Delacroix' in `merged.md` -- The document names Rune Delacroix as an author. |
| 2 | The document was updated on 2026-01-29. | 4 | carried | 'Updated: 2026-01-29' in `merged.md` -- The document gives 2026-01-29 as an update date. |
| 3 | A stream name is one of the mandatry field for every Nimbrel Probe agent. | 8 | carried | 'The stream name is a mandatory field for every Nimbrel Probe agent.' in `merged.md` -- The text states that the stream name is mandatory for every agent. |
| 4 | The stream name cant contain arbitrary symbols. | 8 | carried | 'A stream name cannot contain unsupported symbols' in `merged.md` -- The text expressly disallows unsupported symbols in a stream name. |
| 5 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The text gives the exact validation pattern and says when it is applied. |
| 6 | Stream names may contain letters, digits, spaces and hyphens only, and nothing else. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The text specifies exactly these allowed characters. |
| 7 | The agent refuses to start if the stream name contains anything else. | 12 | carried | 'or the agent refuses to start.' in `merged.md` -- The text says the agent refuses to start when the name contains anything outside the allowed set. |
| 8 | One customer wanted the stream name left exactly as it stood. | 15 | carried | 'A customer may need to preserve a stream name exactly' in `merged.md` -- The text says a customer may need the name preserved exactly. |
| 9 | The string was the product name in use everywhere in the org. | 15 | carried | 'when it is the product name used throughout the organization' in `merged.md` -- The text identifies it as the product name used throughout the organization. |
| 10 | The customer's reporting keyed of the string. | 15 | carried | 'and reporting keys off it.' in `merged.md` -- The text says reporting keys off the name. |
| 12 | Each trace keeps a link between the real name and the renamed one when the original name is carried along as a global tag. | 26 | carried | 'Carry the original name as a global tag so each trace retains a link between the real name and the renamed one.' in `merged.md` -- The workaround carries the original name as a global tag to preserve that link in each trace. |

### `source_b.md` -- 8 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Nimbrel Probe refuses stream names containing a . (dot). | 8 | carried | 'A dot, as in ` checkout.web`, and other unsupported symbols are refused.' in `merged.md` -- The text expressly says a dot in the stream name is refused. |
| 2 | Nimbrel Probe refuses stream names containing a number of other symbols. | 8 | carried | 'and other unsupported symbols are refused.' in `merged.md` -- The text says other unsupported symbols are refused as well. |
| 3 | The Nimbrel Probe stream name separates one instrumented process from the next. | 10 | carried | 'It distinguishes one instrumented process from another.' in `merged.md` -- The text states that the stream name distinguishes instrumented processes. |
| 4 | Only letters, digits, spaces and hyphens are accepted in a Nimbrel Probe stream name. | 10 | carried | 'only letters, digits, spaces, and hyphens are accepted.' in `merged.md` -- The text lists the only accepted characters. |
| 5 | A Nimbrel Probe stream name has to match ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The text states that names are validated against the specified pattern. |
| 6 | The refusal of stream names containing a dot and other symbols by Nimbrel Probe is working as intended for now. | 14 | carried | 'The validation is working as intended for now.' in `merged.md` -- The validation described for dot and other unsupported symbols is said to be working as intended. |
| 7 | There is no fix at present. | 18 | carried | 'There is no fix at present.' in `merged.md` -- The text explicitly says there is no fix at present. |
| 8 | There is no fix at present. | 22 | carried | 'There is no fix at present.' in `merged.md` -- The text explicitly says there is no fix at present. |

### `merged.md` -- 13 claim(s): 0 invented, 0 contradicted, 0 supported in part, 13 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source_a.md states that the stream name is a field for every Nimbrel Probe agent. |
| 2 | A stream name distinguishes one instrumented process from another. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source_b.md directly states that the stream name distinguishes one instrumented process from the next. |
| 3 | Only letters, digits, spaces, and hyphens are accepted in a stream name. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Source_b.md explicitly lists the accepted characters. |
| 4 | A dot, as in ` checkout.web`, and other unsupported symbols are refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source_b.md says a stream name containing the dot in the example and other symbols is refused. |
| 5 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source_a.md states the exact validation pattern and that validation occurs before registration. |
| 6 | Only letters, digits, spaces and hyphens are accepted in stream names. | supported | `source_a.md` | 'Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- Source_a.md explicitly states that only those characters are accepted in stream names. |
| 7 | The agent refuses to start if a stream name contains unsupported symbols. | supported | `source_a.md` | 'Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- Source_a.md says the agent refuses to start when the name contains anything beyond the listed allowed characters. |
| 8 | A customer may need to preserve a stream name exactly when the stream name is the product name used throughout the organization. | supported | `source_a.md` | 'However , one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org' in `source_a.md` -- Source_a.md describes a customer wanting to keep the exact name because it was the organization-wide product name. |
| 9 | Reporting keys off the product name. | supported | `source_a.md` | 'their reporting keyed of it' in `source_a.md` -- Source_a.md states that the reporting keyed off the product name. |
| 10 | The guidance applies to all Nimbrel Probe agents. | supported | `source_a.md` | 'All Nimbrel Probe agents' in `source_a.md` -- Source_a.md identifies all Nimbrel Probe agents as the scope of the guidance. |
| 11 | There is no fix at present. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- Source_b.md explicitly says there is no fix at present. |
| 12 | Renaming a stream to remove unsupported symbols enables the Nimbrel Probe agent to register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Source_a.md directly says that renaming the stream to remove unsupported symbols lets the agent register. |
| 13 | Carrying the original name as a global tag enables each trace to retain a link between the real name and the renamed one. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Source_a.md says to carry the original name as a global tag so each trace retains that link. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **13** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **20**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 6 run(s) over 13 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **17** departure(s) from its sources. Checking them confirms 9, rejects 2, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Topic: corrected the wording and spelling. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a5` | reworded | Topic: clarified the restriction and retained the documentation link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `a7` | reworded | Topic: generalized the stated reason for retaining the exact name. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`, `A-009`, `A-010`) |
| `a11` | reworded | Instructions: introduces the stated workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a12` | reworded | Instructions: clarified the rename step. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back PARTIAL (`A-011`) |
| `a13` | reworded | Instructions: corrected wording and retained the link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `b1` | superseded | Title: the base document's title is retained. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b3` | superseded | Topic heading: consolidated under the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | Topic: corrected spelling and incorporated the dot example. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b5` | reworded | Topic: corrected spelling and clarified the distinction. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`) |
| `b6` | reworded | Topic: combined the accepted characters and retained both links. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-004`, `B-005`) |
| `b7` | superseded | Cause heading: consolidated under the base Topic heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | reworded | Topic: expressed the cause in a complete sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `b9` | superseded | Instructions heading: consolidated under the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | reworded | Instructions: clarified the no-fix statement and workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Resolution heading: consolidated under the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Instructions: the repeated no-fix workaround statement appears once. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-luna |
| Model (decompose) | gpt-6-luna |
| Model (verify) | gpt-6-luna |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 13,570 in, 15,997 out, 7,361 cached, 10,709 reasoning |
| Cost | ~$0.01 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 134.5s |
| Generated | 2026-09-27T16:11:48+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
