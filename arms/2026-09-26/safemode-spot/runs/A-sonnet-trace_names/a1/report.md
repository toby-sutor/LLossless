## Verdict

**3 finding(s).** In the claims: 1 partially invented. In the structure: 2 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 12 |
| Claims extracted from `source_a.md` | 10 |
| Claims extracted from `source_b.md` | 11 |
| Forward — source claims accounted for in the merge | **21/21** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **10/10** |
| Forward — `source_b.md` claims accounted for | **11/11** |
| Reverse — merge claims found in a source | **11/12** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **33/33** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly invented — the sources carry some of this claim

- **M-010** (`merged.md:20`) — The issue applies to all Nimbrel Probe agents.
  - evidence: 'All Nimbrel Probe agents' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source A's Environment lists all agents, but Source B does not limit it that way, and calling it the 'issue' applying to all is loosely supported.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 10 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Stream name is one of the mandatry field for every Nimbrel Probe agent. | 8 | carried | 'The stream name is a mandatory field for every Nimbrel Probe agent' in `merged.md` -- The text states the stream name is a mandatory field for every agent. |
| 2 | The stream name of a Nimbrel Probe agent cannot contain arbitrary symbols. | 8 | carried | 'It cannot contain arbitrary symbols' in `merged.md` -- Directly stated. |
| 3 | Nimbrel Probe stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- Directly stated in the code block. |
| 4 | Nimbrel Probe stream names may contain only letters, digits, spaces and hyphens. | 12 | carried | 'Only letters, digits, spaces and hyphens are accepted' in `merged.md` -- Directly stated. |
| 5 | The Nimbrel Probe agent refuses to start if the stream name contains characters other than letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `merged.md` -- The text says the agent refuses to start otherwise. |
| 6 | One customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org. | 15 | carried | 'a customer may want the stream name left exactly as it stands because that string is the product name in use everywhere in the organisation' in `merged.md` -- The text states this customer motivation, in the general rather than past tense. |
| 7 | The customer's reporting keyed off the stream name. | 15 | carried | 'their reporting is keyed off it' in `merged.md` -- The text says the customer's reporting is keyed off the name. |
| 8 | The environment affected is all Nimbrel Probe agents. | 19 | carried | 'All Nimbrel Probe agents' in `merged.md` -- The Environment section states this. |
| 9 | Renaming the stream to drop the unsupported symbols lets the Nimbrel Probe agent register. | 25 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `merged.md` -- Directly stated. |
| 10 | Carrying the original name along as a global tag keeps a link between the real name and the renamed one on each trace. | 26 | carried | 'Then carry the original name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `merged.md` -- Directly stated. |

### `source_b.md` -- 11 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 11 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Nimbrel Probe refuses a stream name containing a . (dot), for example `checkout.web`. | 8 | carried | 'A stream name containing a . (dot), for example `checkout.web`, along with a number of other symbols, is refused.' in `merged.md` -- Directly stated. |
| 2 | Nimbrel Probe refuses a number of other symbols in stream names besides the dot. | 8 | carried | 'along with a number of other symbols, is refused' in `merged.md` -- Other symbols are refused too. |
| 3 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | 10 | carried | 'it is what separates one instrumented process from the next' in `merged.md` -- Directly stated. |
| 4 | Nimbrel Probe accepts only letters, digits, spaces and hyphens in stream names. | 10 | carried | 'Only letters, digits, spaces and hyphens are accepted' in `merged.md` -- Directly stated. |
| 5 | A Nimbrel Probe stream name has to match the regular expression ^[A-Za-z0-9 -]+$. | 10 | carried | 'the name has to match ^[A-Za-z0-9 -]+$' in `merged.md` -- Directly stated. |
| 6 | The accepted stream name characters are documented at https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name. | 10 | carried | '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' in `merged.md` -- The browser docs link is cited for the symbol restriction. |
| 7 | The refusal of dots in stream names is working as intended for now. | 14 | carried | 'This is working as intended for now.' in `merged.md` -- Directly stated. |
| 8 | There is no fix at present for the refusal of symbols in stream names. | 18 | carried | 'There is no fix at present.' in `merged.md` -- Directly stated. |
| 9 | The workaround is to rename the stream without the refused symbol. | 18 | carried | 'Rename the stream without the refused symbol' in `merged.md` -- Directly stated as the way round. |
| 10 | There is no fix at present for the refusal of symbols in stream names. | 22 | carried | 'There is no fix at present.' in `merged.md` -- Directly stated. |
| 11 | The resolution is to rename the stream without the refused symbol. | 22 | carried | 'Rename the stream without the refused symbol' in `merged.md` -- Stated as the answer given. |

### `merged.md` -- 12 claim(s): 0 invented, 0 contradicted, 1 supported in part, 11 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 10 | The issue applies to all Nimbrel Probe agents. | supported in part | `source_a.md` | 'All Nimbrel Probe agents' in `source_a.md` -- Source A's Environment lists all agents, but Source B does not limit it that way, and calling it the 'issue' applying to all is loosely supported. |
| 1 | The stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source A states the stream name is a mandatory field for every agent. |
| 2 | The stream name separates one instrumented process from the next in Nimbrel Probe. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source B states this directly. |
| 3 | The Nimbrel Probe stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols as documented' in `source_a.md` -- Source A states the stream name cannot contain arbitrary symbols. |
| 4 | Only letters, digits, spaces and hyphens are accepted in a Nimbrel Probe stream name. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Source B states the accepted character set. |
| 5 | A Nimbrel Probe stream name has to match the pattern ^[A-Za-z0-9 -]+$. | supported | `source_b.md` | 'it has to match ^[A-Za-z0-9 -]+$' in `source_b.md` -- Source B gives the exact pattern requirement. |
| 6 | A stream name containing a . (dot), for example `checkout.web`, is refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source B states dotted names such as checkout.web are refused. |
| 7 | Rejection of stream names with unsupported symbols is working as intended for now. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- Source B's Cause section says the behaviour is working as intended for now. |
| 8 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source A states this verbatim. |
| 9 | The agent refuses to start if the stream name contains anything other than letters, digits, spaces and hyphens. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- Source A states the agent refuses to start otherwise. |
| 11 | There is no fix at present for the stream name symbol restriction. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- Source B states no fix at present. |
| 12 | Carrying the original name as a global tag keeps a link between the real name and the renamed one on each trace. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Source A states this directly. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **12** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **21**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 8 run(s) over 17 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '2026-01-29' does not survive into the merge unchanged
- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **17** departure(s) from its sources. Checking them confirms 9, rejects 0, and leaves 8 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Author line combines both authors; later update date chosen. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b2` | subsumed | Author kept in combined line; date chosen over the earlier one. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b1` | superseded | Base title kept; this title not taken. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `a4` | reworded | Typo fixed and merged with b5 into one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-001`) |
| `b5` | reconciled | Combined with a4 into one sentence. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-003`) |
| `a5` | reworded | Typo fixed; both documentation links kept in one sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-002`) |
| `b6` | reworded | Rule stated once; browser link moved into preceding sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-004`, `B-005`, `B-006`) |
| `b4` | reworded | Typos fixed and grammar smoothed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b8` | reworded | Cause folded into Topic; base has no Cause section. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-007`) |
| `b7` | superseded | Cause heading dropped; its content sits in Topic. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | superseded | Base heading for the issue description. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a7` | reworded | Typos fixed; truncated trailing 'when' removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`, `A-007`) |
| `a13` | reworded | Typo 'orignal' fixed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`) |
| `b9` | superseded | Base heading for workaround content. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Base heading; same content as workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | reworded | Reworded as intro to the steps. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Identical to b10; stated once. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'duplicate' is what happened to it (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | e52670eb755f (command) -- Claude Code - Sonnet |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | sonnet -> claude-sonnet-5 |
| Model (decompose) | sonnet -> claude-sonnet-5 |
| Model (verify) | sonnet -> claude-sonnet-5 |
| Structured output | prompt (probed) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=low, merge=medium, verify=low |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 6cc1b1703658 |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 77.3s |
| Generated | 2026-09-26T15:33:20+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `5afca8163bfa` |
| Prompt | `prompts/verify_reverse.md` `cb2face6b7f4` |

> **Document content was handed to a program on this machine (`Claude Code - Sonnet`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
