## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 18 source claim(s) checked against the merge, 16 merge claim(s) checked against the sources. The 9 mechanical checks under Structure below cover what the claims do not: titles, invariant-core tokens, and all 27 source segment(s) — including the ones no claim was drawn from.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 16 |
| Claims extracted from `source_a.md` | 11 |
| Claims extracted from `source_b.md` | 7 |
| Forward — source claims accounted for in the merge | **18/18** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **11/11** |
| Forward — `source_b.md` claims accounted for | **7/7** |
| Reverse — merge claims found in a source | **16/16** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **34/34** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

None.

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
| 1 | A stream name is one of the mandatory fields for every Nimbrel Probe agent. | 8 | carried | 'A stream name is a required field for every Nimbrel Probe agent.' in `merged.md` -- The text explicitly describes a stream name as required for every agent. |
| 2 | A stream name cannot contain arbitrary symbols. | 8 | carried | 'A name containing a dot—for example ` checkout.web`—or other unsupported symbols is refused.' in `merged.md` -- The text says names with unsupported symbols are refused. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The text states this validation rule and timing verbatim. |
| 4 | Stream names can contain only letters, digits, spaces and hyphens. | 12 | carried | 'Stream names accept only letters, digits, spaces and hyphens and must match ^[A-Za-z0-9 -]+$.' in `merged.md` -- The permitted characters are stated directly. |
| 5 | The agent refuses to start if a stream name contains characters other than letters, digits, spaces and hyphens. | 12 | carried | 'Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `merged.md` -- The text says the agent refuses to start if the name contains anything beyond the listed characters. |
| 6 | One customer wanted the stream name left exactly as it stood. | 15 | carried | 'A customer may need to retain the exact stream name when it is the product name used throughout the organization and reporting keys off it.' in `merged.md` -- Retaining the exact name means leaving it as it stood. |
| 7 | The stream name was the product name in use everywhere in the org. | 15 | carried | 'A customer may need to retain the exact stream name when it is the product name used throughout the organization and reporting keys off it.' in `merged.md` -- The text says the name is the product name used throughout the organization. |
| 8 | The customer's reporting keyed of the product name. | 15 | carried | 'A customer may need to retain the exact stream name when it is the product name used throughout the organization and reporting keys off it.' in `merged.md` -- The text explicitly says reporting keys off the name. |
| 9 | The instructions apply to all Nimbrel Probe agents. | 19 | carried | 'All Nimbrel Probe agents' in `merged.md` -- The Environment section identifies all Nimbrel Probe agents as in scope. |
| 10 | The Nimbrel Probe agent will register after the stream is renamed to drop the unsupported symbols. | 25 | carried | 'Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register.' in `merged.md` -- The workaround says removing unsupported symbols allows the agent to register. |
| 11 | Each trace keeps a link between the real name and the renamed one. | 26 | carried | 'Carry the original name as a global tag so each trace retains a link between the original and renamed names: https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags' in `merged.md` -- The workaround explicitly says each trace retains that link. |

### `source_b.md` -- 7 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | A stream name containing a . (dot), such as checkout.web, is refused by Nimbrel Probe. | 8 | carried | 'A name containing a dot—for example ` checkout.web`—or other unsupported symbols is refused.' in `merged.md` -- The text says a name containing a dot, with checkout.web as its example, is refused. |
| 2 | A number of other symbols are refused by Nimbrel Probe. | 8 | carried | 'A name containing a dot—for example ` checkout.web`—or other unsupported symbols is refused.' in `merged.md` -- The text also says other unsupported symbols are refused. |
| 3 | The Nimbrel Probe stream name separates one instrumented process from the next. | 10 | carried | 'It identifies what separates one instrumented process from the next.' in `merged.md` -- This states the stream name's function directly. |
| 4 | Only letters, digits, spaces and hyphens are accepted for a Nimbrel Probe stream name, and it has to match ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names accept only letters, digits, spaces and hyphens and must match ^[A-Za-z0-9 -]+$.' in `merged.md` -- The text gives both the allowed characters and the required pattern. |
| 5 | The refusal of stream names containing a dot is working as intended for now. | 14 | carried | 'This is working as intended for now.' in `merged.md` -- In context, “This” refers to refusing names with unsupported symbols, including a dot. |
| 6 | There is no fix at present. | 18 | carried | 'There is no fix at present; renaming the stream without the refused symbol is the available workaround.' in `merged.md` -- The resolution explicitly says there is no fix at present. |
| 7 | There is no fix at present. | 22 | carried | 'There is no fix at present; renaming the stream without the refused symbol is the available workaround.' in `merged.md` -- The resolution explicitly says there is no fix at present. |

### `merged.md` -- 16 claim(s): 0 invented, 0 contradicted, 0 supported in part, 16 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | A stream name is a required field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- The source states that a stream name is a field required for every Nimbrel Probe agent. |
| 2 | A stream name identifies what separates one instrumented process from the next. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- The source directly describes the stream name as separating one instrumented process from the next. |
| 3 | A name containing a dot—for example ` checkout.web`—or other unsupported symbols is refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- The source says names containing a dot, including the example, and other symbols are refused. |
| 4 | Stream names accept only letters, digits, spaces and hyphens. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- The source explicitly lists the accepted characters. |
| 5 | Stream names must match ^[A-Za-z0-9 -]+$. | supported | `source_b.md` | 'it has to match ^[A-Za-z0-9 -]+$' in `source_b.md` -- The source gives this exact required pattern. |
| 6 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- The source directly states that validation occurs before registration. |
| 7 | Stream names accept only letters, digits, spaces and hyphens, and nothing else. | supported | `source_a.md` | 'Put plainly: letters, digits, spaces and hyphens only, and nothing else' in `source_a.md` -- The source explicitly limits names to these characters and excludes anything else. |
| 8 | The agent refuses to start if the stream name contains anything other than letters, digits, spaces and hyphens. | supported | `source_a.md` | 'or the agent refuses to start.' in `source_a.md` -- The source states the agent refuses to start when the name contains anything beyond the allowed characters. |
| 9 | A customer may need to retain the exact stream name when the stream name is the product name used throughout the organization. | supported | `source_a.md` | 'However , one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org' in `source_a.md` -- The source describes a customer wanting the exact name retained because it was the product name used throughout the organization. |
| 10 | Reporting keys off the stream name when the stream name is the product name used throughout the organization. | supported | `source_a.md` | 'and their reporting keyed of it when' in `source_a.md` -- In context, the source says the customer's reporting keyed off the stream name when it was the product name used throughout the organization. |
| 11 | The refusal of stream names containing unsupported symbols is working as intended for now. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- The source labels the cause as working as intended for now. |
| 12 | The issue applies to all Nimbrel Probe agents. | supported | `source_a.md` | 'All Nimbrel Probe agents' in `source_a.md` -- The source identifies all Nimbrel Probe agents as the environment for the issue. |
| 13 | Renaming the stream to remove unsupported symbols allows the Nimbrel Probe agent to register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- The source says removing unsupported symbols by renaming lets the agent register. |
| 14 | Carrying the original name as a global tag allows each trace to retain a link between the original and renamed names. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- The source states that a global tag carrying the original name keeps each trace linked to the renamed name. |
| 15 | There is no fix at present. | supported | `source_b.md` | 'No fix at present' in `source_b.md` -- The source states there is no fix at present. |
| 16 | Renaming the stream without the refused symbol is the available workaround. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- The source identifies renaming the stream without the refused symbol as the workaround. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **16** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **18**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 12 run(s) over 19 attributed segment(s) — sources interleaved. 8 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **14** departure(s) from its sources. Checking them confirms 10, rejects 0, and leaves 4 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | The base title is retained for the shared subject. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b2` | superseded | The base author and update values are retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a4` | reworded | The Topic slot corrects the spelling and wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a5` | reworded | The Topic slot retains the restriction and its documentation link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a7` | reworded | The Topic slot preserves the customer need and its stated reason. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`, `A-007`, `A-008`) |
| `b4` | reworded | The Topic slot preserves the refused-symbol example. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b5` | reworded | The Topic slot states what the stream name distinguishes. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`) |
| `b6` | reworded | The Topic slot retains the accepted characters, pattern and link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-004`) |
| `b8` | reworded | The Cause slot states the current intended behavior. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`) |
| `a11` | reworded | The Instructions/Answer slot introduces the available workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a12` | reworded | The Workaround slot preserves the renaming step. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`) |
| `a13` | reworded | The Workaround slot preserves the tag, trace link and documentation URL. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `b10` | subsumed | The Resolution slot carries the no-fix status and rename workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b12` | duplicate | The Resolution slot states this repeated status once. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |


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
| Tokens | 13,672 in, 15,005 out, 7,361 cached, 9,910 reasoning |
| Cost | ~$0.01 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 122.5s |
| Generated | 2026-09-27T16:31:12+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
