## Verdict

**4 finding(s).** In the claims: 3 partially dropped. In the structure: 1 unresolved replacement.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 17 |
| Claims extracted from `source_a.md` | 11 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **16/19** |
| Forward — carried only in part | 3 |
| Forward — `source_a.md` claims accounted for | **8/11** (3 in part) |
| Forward — `source_b.md` claims accounted for | **8/8** |
| Reverse — merge claims found in a source | **17/17** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **36/36** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **A-006** (`source_a.md:15`) — One customer wanted the stream name left exactly as it stood.
  - evidence: 'A stream name may need to remain unchanged' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference describes a possible need to keep a name unchanged, but does not identify an actual customer who wanted this.
- **A-007** (`source_a.md:15`) — The customer's stream name was the product name in use everywhere in the org.
  - evidence: 'the product name used throughout an organization' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference describes a stream name that is a widely used product name, but does not attribute it to a particular customer.
- **A-008** (`source_a.md:15`) — The customer's reporting keyed of the product name.
  - evidence: 'reporting keys off it' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference says reporting can key off the product name, but does not identify it as a particular customer's reporting.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 11 claim(s): 0 dropped, 0 contradicted, 3 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 6 | One customer wanted the stream name left exactly as it stood. | 15 | carried in part | 'A stream name may need to remain unchanged' in `merged.md` -- The reference describes a possible need to keep a name unchanged, but does not identify an actual customer who wanted this. |
| 7 | The customer's stream name was the product name in use everywhere in the org. | 15 | carried in part | 'the product name used throughout an organization' in `merged.md` -- The reference describes a stream name that is a widely used product name, but does not attribute it to a particular customer. |
| 8 | The customer's reporting keyed of the product name. | 15 | carried in part | 'reporting keys off it' in `merged.md` -- The reference says reporting can key off the product name, but does not identify it as a particular customer's reporting. |
| 1 | Stream name is one of the mandatry field for every Nimbrel Probe agent. | 8 | carried | 'Stream name is a mandatory field for every Nimbrel Probe agent.' in `merged.md` -- The reference states that every agent requires a stream name. |
| 2 | The stream name cant contain arbitrary symbols. | 8 | carried | 'A stream name cannot contain arbitrary symbols' in `merged.md` -- The reference explicitly restricts symbols in stream names. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The reference gives the same validation pattern and timing. |
| 4 | Stream names can contain letters, digits, spaces and hyphens only. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The reference lists exactly those permitted characters. |
| 5 | The agent refuses to start if the stream name contains unsupported symbols. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `merged.md` -- The reference says the agent refuses to start when a name violates the character restriction. |
| 9 | The described environment includes All Nimbrel Probe agents. | 19 | carried | 'All Nimbrel Probe agents' in `merged.md` -- The environment is stated as all Nimbrel Probe agents. |
| 10 | Dropping unsupported symbols from the stream name allows the Nimbrel Probe agent to register. | 25 | carried | 'Rename the stream to remove unsupported symbols so the Nimbrel Probe agent can register.' in `merged.md` -- The stated workaround removes unsupported symbols to permit registration. |
| 11 | Carrying the orignal name as a global tag lets each trace keep a link between the real name and the renamed one. | 26 | carried | 'Carry the original name as a global tag so each trace retains a link between the product name and the renamed stream' in `merged.md` -- The reference says the global tag preserves that link for each trace. |

### `source_b.md` -- 8 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Nimbrel Probe refuses stream names containing a . (dot), such as ` checkout.web`. | 8 | carried | 'Names containing a . (dot), such as ` checkout.web`, or other unsupported symbols are refused.' in `merged.md` -- The reference explicitly says names containing a dot are refused and gives that example. |
| 2 | Nimbrel Probe refuses stream names containing a number of other symbols. | 8 | carried | 'or other unsupported symbols are refused.' in `merged.md` -- The reference says symbols other than the dot can also cause refusal. |
| 3 | The Nimbrel Probe stream name seperates one instrumented process from the next. | 10 | carried | 'It distinguishes one instrumented process from another.' in `merged.md` -- Distinguishing processes is the stated purpose of the stream name. |
| 4 | Only letters, digits, spaces and hyphens are accepted in a Nimbrel Probe stream name. | 10 | carried | 'Only letters, digits, spaces and hyphens are permitted' in `merged.md` -- The reference states exactly which characters are permitted. |
| 5 | A Nimbrel Probe stream name has to match ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- Validation against that pattern entails that a stream name must match it. |
| 6 | Nimbrel Probe refusing these stream names is working as intended for now. | 14 | carried | 'The restriction is intentional for now.' in `merged.md` -- The reference says the refusal-causing restriction is intentional. |
| 7 | No fix is available at present for Nimbrel Probe refusing these stream names. | 18 | carried | 'There is no fix at present.' in `merged.md` -- The reference explicitly says no fix is currently available. |
| 8 | No fix is available at present for Nimbrel Probe refusing these stream names. | 22 | carried | 'There is no fix at present.' in `merged.md` -- The reference explicitly says no fix is currently available. |

### `merged.md` -- 17 claim(s): 0 invented, 0 contradicted, 0 supported in part, 17 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- The source states that every Nimbrel Probe agent requires a stream name. |
| 2 | A stream name distinguishes one instrumented process from another. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Separating instrumented processes is the distinction described in the claim. |
| 3 | A stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols as documented' in `source_a.md` -- The source directly states the restriction. |
| 4 | Only letters, digits, spaces and hyphens are permitted in a stream name. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- The source lists exactly the permitted character types. |
| 5 | Stream names containing a . (dot) are refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- The source explicitly says names containing a dot are refused. |
| 6 | Stream names containing other unsupported symbols are refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- The source says symbols other than the dot are also refused. |
| 7 | The stream name ` checkout.web` contains a . (dot). | supported | `source_b.md` | '` checkout.web`' in `source_b.md` -- The example shown in the source contains a dot. |
| 8 | The restriction on stream-name symbols is intentional for now. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- The source identifies the refusal of unsupported symbols as intended for now. |
| 9 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- The source states the validation pattern and when it is applied. |
| 10 | A stream name can contain letters, digits, spaces and hyphens only. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else' in `source_a.md` -- The source gives the same exclusive list of permitted characters. |
| 11 | The agent refuses to start if a stream name contains anything other than letters, digits, spaces and hyphens. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- The source explicitly ties any other character to the agent refusing to start. |
| 12 | A stream name may need to remain unchanged when it is the product name used throughout an organization. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org' in `source_a.md` -- The claim generalizes the customer's stated reason for wanting the name unchanged. |
| 13 | Reporting may key off a stream name that is the product name used throughout an organization. | supported | `source_a.md` | 'that string was the product name in use everywhere in the org and their reporting keyed of it' in `source_a.md` -- The source says reporting keyed off the string used as the organization-wide product name. |
| 14 | The stream-name restriction applies to all Nimbrel Probe agents. | supported | `source_a.md` | '### Environment\n\nAll Nimbrel Probe agents' in `source_a.md` -- The source gives all Nimbrel Probe agents as the environment for its stream-name restriction. |
| 15 | There is no fix at present for stream names containing unsupported symbols. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- The source states there is currently no fix for the refused symbol. |
| 16 | Removing unsupported symbols from a stream name allows the Nimbrel Probe agent to register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- The source states that removing unsupported symbols permits registration. |
| 17 | Carrying the original name as a global tag lets each trace retain a link between the product name and the renamed stream. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- The source identifies the original name as the product name and says the global tag preserves its link to the renamed stream on each trace. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **17** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **19**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 8 run(s) over 15 attributed segment(s) — sources interleaved. 5 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Unresolved replacement — a record points at text the merge does not contain

- `b6` — segment b6 is declared 'subsumed' with replacement 'Only letters, digits, spaces and hyphens are permitted, as documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).\n\n```\nStream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.\n```', which is not in the merged document

  ```text
  In the merge: Only letters, digits, spaces and hyphens are permitted, as documented [here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name).

```
Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.
```
  ```

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **17** departure(s) from its sources. Checking them confirms 9, rejects 2, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | The topic sentence corrects the spelling and grammar. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a5` | reworded | The topic states the restriction clearly and retains its link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a7` | reworded | The topic makes the product-name and reporting need general. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-006 came back PARTIAL, A-007 came back PARTIAL, A-008 came back PARTIAL (`A-006`, `A-007`, `A-008`) |
| `a11` | reworded | The instructions introduce the available workaround concisely. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a12` | reworded | The first instruction corrects the wording. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`) |
| `a13` | reworded | The second instruction corrects the wording and retains its link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |
| `b1` | superseded | The base title covers the broader restriction. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b3` | superseded | The issue description uses the base topic heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | The topic keeps the example while correcting the prose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b5` | reworded | The topic states the stream name's purpose more clearly. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`) |
| `b6` | subsumed | The topic retains the rule, pattern and browser link without repeating them. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`, `B-005`) |
| `b7` | superseded | The cause is consolidated under the base topic heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | reworded | The topic states the current cause directly. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `b9` | superseded | The workaround uses the base instructions heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | The instructions retain the no-fix status and rename step. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | superseded | The resolution uses the base instructions heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | duplicate | The resolution repeats the workaround and no-fix status. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |


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
| Tokens | 13,628 in, 11,071 out, 7,361 cached, 4,480 reasoning |
| Cost | ~$0.12 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 140.3s |
| Generated | 2026-09-27T16:14:09+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
