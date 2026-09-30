## Verdict

**1 finding(s).** In the structure: 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 17 |
| Claims extracted from `source_a.md` | 14 |
| Claims extracted from `source_b.md` | 10 |
| Forward — source claims accounted for in the merge | **24/24** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **14/14** |
| Forward — `source_b.md` claims accounted for | **10/10** |
| Reverse — merge claims found in a source | **17/17** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **41/41** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None in the claims. The 1 finding(s) this run reports are structural and are listed under `## Structure` below.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 14 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 14 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The document author is Rune Delacroix. | 3 | carried | 'Author: Rune Delacroix' in `merged.md` -- The header names Rune Delacroix as author. |
| 2 | The document was updated on 2026-01-29. | 4 | carried | 'Updated: 2026-01-29' in `merged.md` -- The header gives the update date as 2026-01-29. |
| 3 | Stream name is a mandatory field for every Nimbrel Probe agent. | 8 | carried | 'The stream name is a mandatory field for every Nimbrel Probe agent' in `merged.md` -- The text states the stream name is mandatory for every agent. |
| 4 | The Nimbrel Probe stream name cannot contain arbitrary symbols. | 8 | carried | 'It cannot contain arbitrary symbols' in `merged.md` -- The text states the stream name cannot contain arbitrary symbols. |
| 5 | Nimbrel Probe stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The code block states this validation directly. |
| 6 | Nimbrel Probe stream names may contain only letters, digits, spaces and hyphens. | 12 | carried | 'only letters, digits, spaces and hyphens are accepted' in `merged.md` -- The text limits stream names to letters, digits, spaces and hyphens. |
| 7 | The Nimbrel Probe agent refuses to start if the stream name contains characters other than letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start' in `merged.md` -- The code block says the agent refuses to start otherwise. |
| 8 | One customer wanted the stream name left exactly as it stood. | 15 | carried | 'Renaming the stream is not always acceptable' in `merged.md` -- The merge generalises the customer's wish to keep the name unchanged into a statement that renaming is not always acceptable. |
| 9 | The customer's stream name string was the product name in use everywhere in the customer's org. | 15 | carried | 'when the existing string is the product name used everywhere in the organisation' in `merged.md` -- The generalised example carries the product-name-used-everywhere situation. |
| 10 | The customer's reporting keyed off the stream name string. | 15 | carried | 'reporting is keyed off it' in `merged.md` -- The generalised example states reporting is keyed off the string. |
| 11 | The issue applies to all Nimbrel Probe agents. | 19 | carried | 'All Nimbrel Probe agents' in `merged.md` -- The Environment section lists all Nimbrel Probe agents. |
| 12 | Renaming the stream to drop the unsupported symbols allows the Nimbrel Probe agent to register. | 25 | carried | 'Rename the stream to drop the unsupported symbols so that the Nimbrel Probe agent registers.' in `merged.md` -- Workaround step 1 states this. |
| 13 | The original stream name can be carried along as a global tag. | 26 | carried | 'Carry the original name along as a global tag' in `merged.md` -- Workaround step 2 states this. |
| 14 | Carrying the original stream name as a global tag lets each trace keep a link between the real name and the renamed one. | 26 | carried | 'so that each trace keeps a link between the real name and the renamed one' in `merged.md` -- Workaround step 2 gives this purpose. |

### `source_b.md` -- 10 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Nimbrel Probe refuses stream names containing a . (dot). | 8 | carried | 'A stream name containing a . (dot), for example `checkout.web`, is refused by Nimbrel Probe' in `merged.md` -- The text states dotted stream names are refused. |
| 2 | Nimbrel Probe refuses the stream name checkout.web. | 8 | carried | 'A stream name containing a . (dot), for example `checkout.web`, is refused by Nimbrel Probe' in `merged.md` -- checkout.web is given as a refused example. |
| 3 | Nimbrel Probe refuses stream names containing a number of other symbols besides the dot. | 8 | carried | 'as are a number of other symbols' in `merged.md` -- The text says other symbols are also refused. |
| 4 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | 10 | carried | 'is what separates one instrumented process from the next' in `merged.md` -- The text states this about the stream name. |
| 5 | Only letters, digits, spaces and hyphens are accepted in the Nimbrel Probe stream name. | 10 | carried | 'only letters, digits, spaces and hyphens are accepted' in `merged.md` -- The text states exactly this. |
| 6 | The Nimbrel Probe stream name has to match ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- Validation against the regex entails that names must match it. |
| 7 | The Nimbrel Probe stream name restriction is documented at https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name. | 10 | carried | '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' in `merged.md` -- The restriction is documented at this linked URL. |
| 8 | The refusal of dots in Nimbrel Probe stream names is working as intended for now. | 14 | carried | 'This is working as intended for now.' in `merged.md` -- The text states the refusal is working as intended for now. |
| 9 | There is no fix at present for the refusal of dots in Nimbrel Probe stream names. | 18 | carried | 'There is no fix at present.' in `merged.md` -- The text states there is no fix at present. |
| 10 | The workaround is to rename the stream without the refused symbol. | 18 | carried | 'Rename the stream to drop the unsupported symbols so that the Nimbrel Probe agent registers.' in `merged.md` -- Workaround step 1 is renaming without the unsupported symbols. |

### `merged.md` -- 17 claim(s): 0 invented, 0 contradicted, 0 supported in part, 17 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The author of the Nimbrel Probe stream name article is Rune Delacroix. | supported | `source_a.md` | 'Author: Rune Delacroix' in `source_a.md` -- Source A lists Rune Delacroix as the author of the stream name article. |
| 2 | The Nimbrel Probe stream name article was updated on 2026-01-29. | supported | `source_a.md` | 'Updated: 2026-01-29' in `source_a.md` -- Source A gives the update date as 2026-01-29. |
| 3 | The stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source A states the stream name is a mandatory field for every agent. |
| 4 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source B states this directly. |
| 5 | The Nimbrel Probe stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols' in `source_a.md` -- Source A states the stream name cannot contain arbitrary symbols. |
| 6 | Only letters, digits, spaces and hyphens are accepted in a Nimbrel Probe stream name. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Source B states only these characters are accepted. |
| 7 | Nimbrel Probe stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source A states this validation verbatim. |
| 8 | The Nimbrel Probe agent refuses to start if the stream name contains anything other than letters, digits, spaces and hyphens. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- Source A says the agent refuses to start if other characters are present. |
| 9 | A stream name containing a . (dot), such as `checkout.web`, is refused by Nimbrel Probe. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source B states dot-containing names like checkout.web are refused. |
| 10 | A number of symbols other than the dot are refused in Nimbrel Probe stream names. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source B says a number of other symbols besides the dot are also refused. |
| 11 | The refusal of dots in Nimbrel Probe stream names is working as intended for now. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- Source B's Cause section says the behaviour is working as intended for now. |
| 12 | The stream name restriction applies to all Nimbrel Probe agents. | supported | `source_a.md` | 'All Nimbrel Probe agents' in `source_a.md` -- Source A's Environment section says the restriction applies to all Nimbrel Probe agents. |
| 13 | There is at present no fix for unsupported symbols in Nimbrel Probe stream names. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- Source B states there is no fix at present. |
| 14 | A workaround exists for unsupported symbols in Nimbrel Probe stream names. | supported | `source_a.md` | 'A way round it that works' in `source_a.md` -- Source A describes a working workaround. |
| 15 | Renaming the stream to drop the unsupported symbols allows the Nimbrel Probe agent to register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Source A states renaming lets the agent register. |
| 16 | Carrying the original stream name as a global tag keeps a link between the real name and the renamed one in each trace. | supported | `source_a.md` | 'so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Source A says carrying the original name as a global tag keeps this link in each trace. |
| 17 | Global tags for the Nimbrel Probe Node.js agent are documented at https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags. | supported | `source_a.md` | 'https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags' in `source_a.md` -- Source A cites this Node.js agent configuration URL as the global tags documentation. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **17** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **24**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 4 run(s) over 13 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **18** departure(s) from its sources. Checking them confirms 10, rejects 1, and leaves 7 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b2` | superseded | Base author block kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | superseded | Base heading used for the problem section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a4` | reworded | Typo fixed and merged with b5's purpose statement. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `b5` | subsumed | Purpose of the stream name joined to the mandatory-field sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `a5` | reworded | Allowed-characters rule stated once with both doc links. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `b6` | subsumed | Rule and link kept here; the regex is carried in the code block. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`, `B-006`, `B-007`) |
| `b4` | reworded | Typos and inline-code spacing fixed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`, `B-003`) |
| `b7` | superseded | Cause content moved into the base Topic section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | reworded | Cause stated in the Topic section as a full sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-008`) |
| `a7` | reworded | Generalised from one customer and truncated ending completed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`, `A-009`, `A-010`) |
| `b9` | superseded | Base heading used for the solution section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Base heading used for the solution section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a11` | reworded | Introduction to the steps made a full sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | No-fix statement kept; rename step carried by step 1. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Identical to b10. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a12` | reworded | List formatting and phrasing tidied. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `a13` | reworded | Typo fixed and list formatting tidied; URL unchanged. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-013`, `A-014`) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 20,392 in, 13,414 out |
| Cost | ~$0.35 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 110.0s |
| Generated | 2026-09-27T16:49:50+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
