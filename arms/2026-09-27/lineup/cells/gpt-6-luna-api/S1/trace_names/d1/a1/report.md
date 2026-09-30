## Verdict

**1 finding(s).** In the claims: 1 partially dropped.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 10 |
| Claims extracted from `source_a.md` | 11 |
| Claims extracted from `source_b.md` | 7 |
| Forward — source claims accounted for in the merge | **17/18** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **10/11** (1 in part) |
| Forward — `source_b.md` claims accounted for | **7/7** |
| Reverse — merge claims found in a source | **10/10** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **28/28** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **A-006** (`source_a.md:15`) — One customer wanted the stream name left exactly as it stood.
  - evidence: 'An organization may need to retain the exact stream name' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text says an organization may need to retain the name, but does not state that a customer wanted it left unchanged.

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
| 6 | One customer wanted the stream name left exactly as it stood. | 15 | carried in part | 'An organization may need to retain the exact stream name' in `merged.md` -- The text says an organization may need to retain the name, but does not state that a customer wanted it left unchanged. |
| 1 | A stream name is one of the mandatory fields for every Nimbrel Probe agent. | 8 | carried | 'The stream name is a mandatory field for every Nimbrel Probe agent' in `merged.md` -- The text explicitly identifies the stream name as mandatory for every agent. |
| 2 | A Nimbrel Probe stream name cannot contain arbitrary symbols. | 8 | carried | 'Only letters, digits, spaces and hyphens are accepted; a dot, as in ` checkout.web`, and other unsupported symbols are refused.' in `merged.md` -- The text limits accepted characters and says unsupported symbols are refused. |
| 3 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The text states the exact validation pattern and when validation occurs. |
| 4 | Stream names may contain letters, digits, spaces and hyphens only. | 12 | carried | 'letters, digits, spaces and hyphens only' in `merged.md` -- The text explicitly lists the only accepted characters. |
| 5 | The agent refuses to start if a stream name contains anything other than letters, digits, spaces and hyphens. | 12 | carried | 'Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `merged.md` -- The text says the agent refuses to start if the name contains anything beyond the listed characters. |
| 7 | The stream name was the product name in use everywhere in the org. | 15 | carried | 'when it is the product name used throughout the organization' in `merged.md` -- The text says the exact stream name may be the product name used throughout the organization. |
| 8 | The customer's reporting keyed off the stream name. | 15 | carried | 'reporting keys off it.' in `merged.md` -- The text explicitly says reporting keys off the stream name. |
| 9 | A workaround exists that works. | 23 | carried | 'A working workaround is:' in `merged.md` -- The text explicitly describes the workaround as working. |
| 10 | Renaming the stream to drop unsupported symbols allows the Nimbrel Probe agent to register. | 25 | carried | 'Rename the stream to remove unsupported symbols so the Nimbrel Probe agent registers.' in `merged.md` -- The first workaround step says removing unsupported symbols allows the agent to register. |
| 11 | Carrying the original name as a global tag keeps a link between the real name and the renamed name on each trace. | 26 | carried | 'Add the original name as a global tag so each trace keeps a link between the real name and the renamed one:' in `merged.md` -- The text states that adding the original name as a global tag links the two names on each trace. |

### `source_b.md` -- 7 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Nimbrel Probe refuses stream names containing a . (dot). | 8 | carried | 'a dot, as in ` checkout.web`, and other unsupported symbols are refused.' in `merged.md` -- The text explicitly identifies a dot as a refused symbol. |
| 2 | Nimbrel Probe refuses stream names containing a number of other symbols. | 8 | carried | 'and other unsupported symbols are refused.' in `merged.md` -- The text says other unsupported symbols are refused as well. |
| 3 | A Nimbrel Probe stream name separates one instrumented process from the next. | 10 | carried | 'separates one instrumented process from the next.' in `merged.md` -- The text states this function of a stream name directly. |
| 4 | Nimbrel Probe stream names accept only letters, digits, spaces and hyphens, matching ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `merged.md` -- The text provides both the matching pattern and the accepted character set. |
| 5 | Nimbrel Probe's refusal of stream names containing unsupported symbols is working as intended for now. | 14 | carried | 'This validation behavior is working as intended for now.' in `merged.md` -- The text explicitly says the validation behavior is working as intended for now. |
| 6 | No fix is available at present for Nimbrel Probe refusing stream names containing unsupported symbols. | 18 | carried | 'There is no fix at present; rename the stream without the refused symbol.' in `merged.md` -- The text says no fix is currently available for the refusal behavior. |
| 7 | No fix is available at present for Nimbrel Probe refusing stream names containing unsupported symbols. | 22 | carried | 'There is no fix at present; rename the stream without the refused symbol.' in `merged.md` -- The text says no fix is currently available for the refusal behavior. |

### `merged.md` -- 10 claim(s): 0 invented, 0 contradicted, 0 supported in part, 10 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source_a.md states that the stream name is a field for every Nimbrel Probe agent. |
| 2 | The stream name separates one instrumented process from the next. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source_b.md directly states that the stream name separates one instrumented process from the next. |
| 3 | Only letters, digits, spaces and hyphens are accepted in a stream name. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Source_b.md lists the accepted characters as letters, digits, spaces and hyphens. |
| 4 | A dot, as in ` checkout.web`, and other unsupported symbols are refused in a stream name. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source_b.md states that a dot, the example string, and other symbols are refused. |
| 5 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source_a.md gives this validation pattern and says validation occurs before registration. |
| 6 | The agent accepts only letters, digits, spaces and hyphens in stream names. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- The stated accepted characters mean the agent accepts only letters, digits, spaces and hyphens. |
| 7 | The agent refuses to start if a stream name contains anything other than letters, digits, spaces and hyphens. | supported | `source_a.md` | 'Put plainly: letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- Source_a.md states that anything beyond those characters causes the agent to refuse to start. |
| 8 | There is no fix at present. | supported | `source_b.md` | 'No fix at present' in `source_b.md` -- Source_b.md explicitly says there is no fix at present. |
| 9 | Removing unsupported symbols from the stream name allows the Nimbrel Probe agent to register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Source_a.md says removing unsupported symbols allows the agent to register. |
| 10 | Adding the original name as a global tag keeps each trace linked between the real name and the renamed one. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Source_a.md recommends carrying the original name as a global tag to link each trace to the renamed stream. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **10** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **18**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 4 run(s) over 12 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **18** departure(s) from its sources. Checking them confirms 10, rejects 1, and leaves 7 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | The base title is chosen for the merged document. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b2` | superseded | The base author and update date are retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a4` | reworded | The Topic paragraph corrects the wording and retains both facts. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `a5` | reworded | The Topic paragraph clarifies the restriction and retains its link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `a7` | reworded | The Topic paragraph states the retention rationale generally. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-006 came back PARTIAL (`A-006`) |
| `b3` | subsumed | The issue-description heading is consolidated under Topic. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b4` | reworded | The Topic paragraph corrects spelling and retains the example and restriction. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b5` | subsumed | The Topic paragraph carries the process-separation fact. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b6` | reworded | The Topic paragraph consolidates the accepted characters and both links. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-004`) |
| `b7` | subsumed | The cause heading is consolidated under Topic. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b8` | reworded | The Topic section states the current intended behavior. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-005`) |
| `b9` | subsumed | The workaround heading is consolidated under the base instructions heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b10` | reworded | The instructions retain the current lack of a fix and rename workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b11` | subsumed | The resolution heading is consolidated under the base instructions heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b12` | duplicate | The repeated resolution is stated once in the instructions. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |
| `a11` | reworded | The instructions introduce the effective workaround. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-009`) |
| `a12` | reworded | The first instruction retains the rename step and its purpose. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`) |
| `a13` | reworded | The second instruction retains the tag purpose and documentation link. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-011`) |


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
| Tokens | 13,468 in, 15,498 out, 0 cached, 10,155 reasoning |
| Cost | ~$0.01 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 133.6s |
| Generated | 2026-09-27T15:56:03+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
