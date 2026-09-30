## Verdict

**1 finding(s).** In the claims: 1 partially dropped.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 16 |
| Claims extracted from `source_a.md` | 11 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **18/19** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **10/11** (1 in part) |
| Forward — `source_b.md` claims accounted for | **8/8** |
| Reverse — merge claims found in a source | **16/16** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **35/35** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **A-006** (`source_a.md:15`) — One customer wanted the stream name left exactly as it stood.
  - evidence: 'An organization may need to retain the original stream name' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text describes a possible need to retain the original name, but does not identify a particular customer wanting it left exactly as it stood.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 11 claim(s): 0 dropped, 0 contradicted, 1 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 6 | One customer wanted the stream name left exactly as it stood. | 15 | carried in part | 'An organization may need to retain the original stream name' in `merged.md` -- The text describes a possible need to retain the original name, but does not identify a particular customer wanting it left exactly as it stood. |
| 1 | Stream name is one of the mandatry field for every Nimbrel Probe agent. | 8 | carried | 'A stream name is a mandatory field for every Nimbrel Probe agent.' in `merged.md` -- The text says every Nimbrel Probe agent requires a stream name. |
| 2 | The stream name cant contain arbitrary symbols. | 8 | carried | 'The stream name cannot contain arbitrary symbols' in `merged.md` -- The text explicitly disallows arbitrary symbols. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The validation pattern and timing match the claim. |
| 4 | Stream names can contain letters, digits, spaces and hyphens only. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The text gives exactly these permitted characters. |
| 5 | The agent refuses to start if a stream name contains other symbols. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `merged.md` -- The text says other characters cause the agent to refuse to start. |
| 7 | The stream name was the product name in use everywhere in the org. | 15 | carried | 'it is the product name used throughout the organization' in `merged.md` -- The text says the original stream name is the product name used throughout the organization. |
| 8 | The customer's reporting keyed of the stream name. | 15 | carried | 'its reporting keys off that name' in `merged.md` -- The text says the organization's reporting keys off the name. |
| 9 | The Nimbrel Probe agent will register if the stream is renamed to drop the unsupported symbols. | 25 | carried | 'Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register.' in `merged.md` -- The stated workaround enables registration by removing unsupported symbols. |
| 10 | The orignal name can be carried along as a global tag. | 26 | carried | 'Carry the original name as a global tag' in `merged.md` -- The text explicitly proposes carrying the original name as a global tag. |
| 11 | Carrying the orignal name along as a global tag lets each trace keep a link between the real name and the renamed one. | 26 | carried | 'Carry the original name as a global tag so each trace retains a link between it and the renamed stream' in `merged.md` -- The text states that the tag preserves the link on each trace. |

### `source_b.md` -- 8 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Nimbrel Probe refuses stream names containing a . (dot), such as ` checkout.web`. | 8 | carried | 'Names containing a . (dot), such as ` checkout.web`, or other unsupported symbols are refused.' in `merged.md` -- The text explicitly identifies dot-containing names and the example as refused. |
| 2 | Nimbrel Probe refuses stream names containing a number of other symbols. | 8 | carried | 'Names containing a . (dot), such as ` checkout.web`, or other unsupported symbols are refused.' in `merged.md` -- The text says names with other unsupported symbols are also refused. |
| 3 | The Nimbrel Probe stream name seperates one instrumented process from the next. | 10 | carried | 'It distinguishes one instrumented process from another.' in `merged.md` -- Distinguishing processes is the same as separating one from the next. |
| 4 | Only letters, digits, spaces and hyphens are accepted in a Nimbrel Probe stream name. | 10 | carried | 'Only letters, digits, spaces and hyphens are accepted' in `merged.md` -- The text lists exactly those accepted character types. |
| 5 | A Nimbrel Probe stream name has to match ^[A-Za-z0-9 -]+$. | 10 | carried | 'it has to match ^[A-Za-z0-9 -]+$' in `merged.md` -- The required pattern matches the claim. |
| 6 | Nimbrel Probe's refusal of these stream names is working as intended for now. | 14 | carried | 'This restriction is working as intended for now.' in `merged.md` -- The text describes the refusal-causing restriction as intended. |
| 7 | There is no fix at present for Nimbrel Probe's refusal of stream names containing the refused symbol. | 18 | carried | 'No fix is available at present.' in `merged.md` -- The text states that no fix is currently available for the described restriction. |
| 8 | There is no fix at present for Nimbrel Probe's refusal of stream names containing the refused symbol. | 22 | carried | 'No fix is available at present.' in `merged.md` -- The text states that no fix is currently available for the described restriction. |

### `merged.md` -- 16 claim(s): 0 invented, 0 contradicted, 0 supported in part, 16 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | A stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- The source says every agent requires a stream name. |
| 2 | A stream name distinguishes one instrumented process from another. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- The source describes the stream name as distinguishing instrumented processes. |
| 3 | The stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols as documented' in `source_a.md` -- The source explicitly rules out arbitrary symbols. |
| 4 | Only letters, digits, spaces and hyphens are accepted in stream names. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- The source lists exactly those accepted characters. |
| 5 | A stream name has to match ^[A-Za-z0-9 -]+$. | supported | `source_b.md` | 'it has to match ^[A-Za-z0-9 -]+$' in `source_b.md` -- The source gives the same required pattern. |
| 6 | Stream names containing a . (dot), such as ` checkout.web`, are refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- The source says dot-containing names are refused and gives that example. |
| 7 | Stream names containing other unsupported symbols are refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- The source says symbols other than the dot are also refused. |
| 8 | The stream name restriction is working as intended for now. | supported | `source_b.md` | '### Cause\n\nWorking as intended for now' in `source_b.md` -- The source identifies the restriction as working as intended for now. |
| 9 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- The source states the claim verbatim. |
| 10 | An agent refuses to start if its stream name contains characters other than letters, digits, spaces and hyphens. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- The source links any other characters to the agent refusing to start. |
| 11 | An organization's original stream name is the product name used throughout the organization. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org' in `source_a.md` -- The claim generalizes the source's account of one customer's product name. |
| 12 | An organization's reporting keys off the original stream name. | supported | `source_a.md` | 'that string was the product name in use everywhere in the org and their reporting keyed of it' in `source_a.md` -- The source says the customer's reporting keyed off the original string. |
| 13 | The stream name restriction applies to All Nimbrel Probe agents. | supported | `source_a.md` | '### Environment\n\nAll Nimbrel Probe agents' in `source_a.md` -- The source lists all Nimbrel Probe agents as the environment for this restriction. |
| 14 | No fix is available at present for stream names containing unsupported symbols. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- The source says there is no fix at present for a refused symbol. |
| 15 | Renaming a stream to remove unsupported symbols allows the Nimbrel Probe agent to register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- The source gives renaming as the way to let the agent register. |
| 16 | Carrying the original stream name as a global tag lets each trace retain a link between the original name and the renamed stream. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- The source says the global tag preserves that link on each trace. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **16** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **19**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 8 run(s) over 17 attributed segment(s) — sources interleaved. 5 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **17** departure(s) from its sources. Checking them confirms 9, rejects 2, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Corrected the wording in Topic. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a5` | reworded | Corrected the wording in Topic and retained its link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a7` | reworded | Completed the truncated sentence in Topic without adding a fact. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-006 came back PARTIAL (`A-006`) |
| `a11` | subsumed | The informal introduction becomes the workaround introduction. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a12` | reworded | Corrected and clarified the first workaround step. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`) |
| `a13` | reworded | Corrected the second workaround step and retained its link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`, `A-011`) |
| `b1` | superseded | The base title covers the broader symbol restriction. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b3` | superseded | The issue description belongs under the base Topic heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | Corrected the dot example in Topic. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b5` | reworded | Clarified the stream name's role in Topic. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`) |
| `b6` | reworded | Corrected the wording in Topic and retained its link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-004`, `B-005`) |
| `b7` | superseded | The cause statement belongs under the base Topic heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | reworded | Identified what is working as intended in Topic. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `b9` | superseded | The workaround belongs under the base instructions heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | The no-fix status and rename step are retained in the instructions. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | superseded | The resolution repeats the workaround under the base heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | duplicate | The resolution repeats the no-fix status and rename step. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |


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
| Tokens | 13,668 in, 9,254 out, 0 cached, 2,907 reasoning |
| Cost | ~$0.12 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 117.0s |
| Generated | 2026-09-27T15:53:49+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
