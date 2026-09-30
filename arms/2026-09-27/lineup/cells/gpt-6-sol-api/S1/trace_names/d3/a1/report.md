## Verdict

**No extracted claim was dropped, contradicted, invented, or carried only in part.** 19 source claim(s) checked against the merge, 16 merge claim(s) checked against the sources. The 9 mechanical checks under Structure below cover what the claims do not: titles, invariant-core tokens, and all 27 source segment(s) — including the ones no claim was drawn from.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 16 |
| Claims extracted from `source_a.md` | 11 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **19/19** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **11/11** |
| Forward — `source_b.md` claims accounted for | **8/8** |
| Reverse — merge claims found in a source | **16/16** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **35/35** |
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
| 1 | Stream name is a mandatory field for every Nimbrel Probe agent. | 8 | carried | 'The stream name is a mandatory field for every Nimbrel Probe agent' in `merged.md` -- The reference states that every agent requires a stream name. |
| 2 | A Nimbrel Probe agent's stream name cannot contain arbitrary symbols. | 8 | carried | 'Stream names cannot contain arbitrary symbols' in `merged.md` -- The reference explicitly restricts symbols in stream names. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The reference gives the same validation pattern and timing. |
| 4 | Stream names can contain letters, digits, spaces and hyphens only. | 12 | carried | 'letters, digits, spaces and hyphens only' in `merged.md` -- The reference lists exactly those permitted character types. |
| 5 | An agent refuses to start if its stream name contains characters other than letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `merged.md` -- The reference says an agent refuses to start when the name contains other characters. |
| 6 | One customer wanted the stream name left exactly as it stood. | 15 | carried | 'A customer may need the stream name to remain unchanged' in `merged.md` -- The reference describes the customer's need to retain the name. |
| 7 | The customer's stream name was the product name in use everywhere in the org. | 15 | carried | 'it is the product name used throughout the organization' in `merged.md` -- The reference identifies the stream name as the product name used throughout the organization. |
| 8 | The customer's reporting keyed of the stream name. | 15 | carried | 'reporting keys off it' in `merged.md` -- The reference states that reporting depends on the stream name. |
| 9 | The stated environment is All Nimbrel Probe agents. | 19 | carried | 'All Nimbrel Probe agents' in `merged.md` -- This is the stated environment. |
| 10 | A Nimbrel Probe agent will register if the stream is renamed to drop unsupported symbols. | 25 | carried | 'Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register.' in `merged.md` -- The workaround says renaming the stream permits registration. |
| 11 | Carrying the orignal name as a global tag keeps a link between the real name and the renamed one in each trace. | 26 | carried | 'Carry the original name as a global tag so each trace retains a link between the original and renamed names.' in `merged.md` -- The reference states the tag's purpose for each trace. |

### `source_b.md` -- 8 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Nimbrel Probe refuses stream names containing a . (dot), for exampe` checkout.web`. | 8 | carried | 'A stream name containing a . (dot), such as ` checkout.web`, is refused' in `merged.md` -- The reference gives the same prohibited symbol and example. |
| 2 | Nimbrel Probe refuses a number of other symbols in stream names. | 8 | carried | 'as are names containing other unsupported symbols.' in `merged.md` -- The reference says other unsupported symbols also cause refusal. |
| 3 | The Nimbrel Probe stream name seperates one instrumented process from the next. | 10 | carried | 'separates one instrumented process from another' in `merged.md` -- The reference gives this function for the stream name. |
| 4 | Only letters, digits, spaces and hyphens are accepted in Nimbrel Probe stream names. | 10 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The reference limits accepted characters to those four types. |
| 5 | The Nimbrel Probe stream name has to match ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The validation pattern is stated explicitly. |
| 6 | Nimbrel Probe's refusal of those stream names is working as intended for now. | 14 | carried | 'This refusal is working as intended for now.' in `merged.md` -- The reference describes the refusal as intended behavior for now. |
| 7 | There is no fix at present for Nimbrel Probe refusing those stream names. | 18 | carried | 'No fix is available at present.' in `merged.md` -- The reference states that no fix is currently available. |
| 8 | There is no fix at present for Nimbrel Probe refusing those stream names. | 22 | carried | 'No fix is available at present.' in `merged.md` -- The reference states that no fix is currently available. |

### `merged.md` -- 16 claim(s): 0 invented, 0 contradicted, 0 supported in part, 16 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- The source says every agent requires a stream name. |
| 2 | The stream name separates one instrumented process from another. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- The source gives the stream name this separating role. |
| 3 | Stream names cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols as documented' in `source_a.md` -- The source explicitly disallows arbitrary symbols. |
| 4 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- The source states both the pattern and when validation occurs. |
| 5 | Stream names can contain letters, digits, spaces and hyphens only. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else' in `source_a.md` -- The source lists exactly the permitted character types. |
| 6 | A Nimbrel Probe agent refuses to start if its stream name contains other symbols. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- The source says other characters cause the agent to refuse to start. |
| 7 | The ^[A-Za-z0-9 -]+$ restriction is documented in the browser agent configuration. | supported | `source_b.md` | 'it has to match ^[A-Za-z0-9 -]+$) as documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' in `source_b.md` -- The cited documentation link is for browser agent configuration. |
| 8 | A stream name containing a . (dot), such as ` checkout.web`, is refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- The source identifies a dot as refused and gives the same example. |
| 9 | Stream names containing other unsupported symbols are refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- The source says symbols besides the dot are also refused. |
| 10 | The refusal of stream names containing unsupported symbols is working as intended for now. | supported | `source_b.md` | '### Cause\n\nWorking as intended for now' in `source_b.md` -- The source characterizes the described refusal as intended for now. |
| 11 | A customer's stream name can be the product name used throughout the organization. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org' in `source_a.md` -- The customer's stream-name string was the product name used throughout the organization. |
| 12 | A customer's reporting can key off the product name used as the stream name. | supported | `source_a.md` | 'that string was the product name in use everywhere in the org and their reporting keyed of it' in `source_a.md` -- The source connects the product-name string to the customer's reporting. |
| 13 | The stream name restriction applies to all Nimbrel Probe agents. | supported | `source_a.md` | '### Environment\n\nAll Nimbrel Probe agents' in `source_a.md` -- The restriction is the topic of this source, whose environment is all Nimbrel Probe agents. |
| 14 | No fix is available at present for stream names containing unsupported symbols. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- The source explicitly says no fix is available at present. |
| 15 | Removing unsupported symbols from the stream name allows the Nimbrel Probe agent to register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- The source states that dropping unsupported symbols allows registration. |
| 16 | Carrying the original name as a global tag lets each trace retain a link between the original and renamed names. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- The source describes using a global tag to preserve that link on each trace. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **16** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **19**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 8 run(s) over 15 attributed segment(s) — sources interleaved. 5 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **17** departure(s) from its sources. Checking them confirms 10, rejects 1, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Topic: correct the spelling and combine the stream-name definitions. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a5` | reworded | Topic: correct the spelling while retaining the documentation link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a7` | reworded | Topic: express the customer’s reason without the unfinished clause. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`, `A-007`, `A-008`) |
| `a11` | reworded | Instructions/Answer: introduce the steps concisely. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a12` | reworded | Instructions/Answer: state the first step clearly. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`) |
| `a13` | reworded | Instructions/Answer: correct the spelling and clarify the second step. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `b1` | superseded | Title: use the broader base title. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b3` | superseded | Issue heading: use the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | Topic: correct the prose while retaining the example. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b5` | subsumed | Topic: combine the stream-name definitions. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b6` | subsumed | Topic: retain the second link without repeating the allowed characters. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`, `B-005`) |
| `b7` | superseded | Cause heading: place the cause within the base Topic section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | reworded | Topic: make the cause a complete sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `b9` | superseded | Workaround heading: use the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | Instructions/Answer: retain the lack of a fix and the rename step. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | superseded | Resolution heading: consolidate the repeated advice under the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Instructions/Answer: this repeats the workaround. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-sol |
| Model (decompose) | gpt-6-sol |
| Model (verify) | gpt-6-sol |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 13,648 in, 9,500 out, 7,361 cached, 3,091 reasoning |
| Cost | ~$0.11 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 119.5s |
| Generated | 2026-09-27T16:29:09+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
