## Verdict

**1 finding(s).** In the structure: 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 19 |
| Claims extracted from `source_a.md` | 14 |
| Claims extracted from `source_b.md` | 8 |
| Forward — source claims accounted for in the merge | **22/22** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **14/14** |
| Forward — `source_b.md` claims accounted for | **8/8** |
| Reverse — merge claims found in a source | **19/19** |
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
| 1 | The author of the article on Nimbrel Probe stream names with unsupported symbols is Rune Delacroix. | 3 | carried | 'Author: Rune Delacroix' in `merged.md` -- The header names Rune Delacroix as the author. |
| 2 | The article on Nimbrel Probe stream names with unsupported symbols was updated on 2026-01-29. | 4 | carried | 'Updated: 2026-01-29' in `merged.md` -- The header gives the update date as 2026-01-29. |
| 3 | Stream name is a mandatory field for every Nimbrel Probe agent. | 8 | carried | 'The stream name is a mandatory field for every Nimbrel Probe agent' in `merged.md` -- The text states this directly. |
| 4 | The Nimbrel Probe stream name cannot contain arbitrary symbols. | 8 | carried | 'It cannot contain arbitrary symbols' in `merged.md` -- The text states the stream name cannot contain arbitrary symbols. |
| 5 | Nimbrel Probe stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The code block states this validation verbatim. |
| 6 | Nimbrel Probe stream names may contain only letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- The text restricts stream names to letters, digits, spaces and hyphens. |
| 7 | The Nimbrel Probe agent refuses to start if the stream name contains characters other than letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start' in `merged.md` -- The text says the agent refuses to start if the name contains other characters. |
| 8 | One customer wanted the Nimbrel Probe stream name left exactly as it stood. | 15 | carried | 'some organisations need the stream name kept exactly as it stands' in `merged.md` -- The merged text generalises the single customer's need to organisations, which carries the claim. |
| 9 | The customer's stream name string was the product name in use everywhere in the customer's org. | 15 | carried | 'that string is the product name used everywhere in the organisation' in `merged.md` -- The generalised statement carries the claim that the string is the product name used org-wide. |
| 10 | The customer's reporting keyed off the stream name string. | 15 | carried | 'their reporting keys off it' in `merged.md` -- The text states that reporting keys off the stream name string. |
| 11 | The issue with stream names containing unsupported symbols applies to all Nimbrel Probe agents. | 19 | carried | 'All Nimbrel Probe agents' in `merged.md` -- The Environment section lists all Nimbrel Probe agents. |
| 12 | Renaming the stream to drop the unsupported symbols allows the Nimbrel Probe agent to register. | 25 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `merged.md` -- The first workaround step states this. |
| 13 | The original stream name can be carried along as a global tag. | 26 | carried | 'Then carry the original name along as a global tag' in `merged.md` -- The second workaround step states this. |
| 14 | Carrying the original stream name as a global tag lets each trace keep a link between the real name and the renamed one. | 26 | carried | 'so that each trace at least keeps a link between the real name and the renamed one' in `merged.md` -- The text states the global tag keeps this link on each trace. |

### `source_b.md` -- 8 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Nimbrel Probe refuses stream names containing a . (dot), such as checkout.web. | 8 | carried | 'A stream name containing a . (dot), for example `checkout.web`, or any of a number of other symbols is refused by Nimbrel Probe.' in `merged.md` -- The text states that dotted names such as checkout.web are refused. |
| 2 | Nimbrel Probe refuses stream names containing a number of other symbols besides the dot. | 8 | carried | 'A stream name containing a . (dot), for example `checkout.web`, or any of a number of other symbols is refused by Nimbrel Probe.' in `merged.md` -- The same sentence says a number of other symbols are also refused. |
| 3 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | 10 | carried | 'is what separates one instrumented process from the next' in `merged.md` -- The text states this directly. |
| 4 | Only letters, digits, spaces and hyphens are accepted in the Nimbrel Probe stream name. | 10 | carried | 'only letters, digits, spaces and hyphens are accepted' in `merged.md` -- The text states this directly. |
| 5 | The Nimbrel Probe stream name has to match ^[A-Za-z0-9 -]+$. | 10 | carried | 'the name has to match ^[A-Za-z0-9 -]+$' in `merged.md` -- The text states the pattern the name must match. |
| 6 | The rejection of dots in Nimbrel Probe stream names is working as intended for now. | 14 | carried | 'This is working as intended for now.' in `merged.md` -- This sentence follows the statement that dotted names are refused and says the behaviour is intended for now. |
| 7 | There is no fix at present for Nimbrel Probe refusing stream names with a dot. | 18 | carried | 'There is no fix at present' in `merged.md` -- The text states there is no fix at present. |
| 8 | The workaround is to rename the stream without the refused symbol. | 18 | carried | 'Rename the stream to drop the unsupported symbols' in `merged.md` -- The workaround is to rename the stream without the unsupported symbols. |

### `merged.md` -- 19 claim(s): 0 invented, 0 contradicted, 0 supported in part, 19 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The author of the Nimbrel Probe stream name article is Rune Delacroix. | supported | `source_a.md` | 'Author: Rune Delacroix' in `source_a.md` -- Source A lists Rune Delacroix as the author of the stream name article. |
| 2 | The Nimbrel Probe stream name article was updated 2026-01-29. | supported | `source_a.md` | 'Updated: 2026-01-29' in `source_a.md` -- Source A gives the updated date as 2026-01-29. |
| 3 | The stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source A states the stream name is mandatory for every agent. |
| 4 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source B states this directly. |
| 5 | The Nimbrel Probe stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols' in `source_a.md` -- Source A states the stream name cannot contain arbitrary symbols. |
| 6 | Only letters, digits, spaces and hyphens are accepted in the Nimbrel Probe stream name. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Source B states only these characters are accepted. |
| 7 | The Nimbrel Probe stream name has to match ^[A-Za-z0-9 -]+$. | supported | `source_b.md` | 'it has to match ^[A-Za-z0-9 -]+$' in `source_b.md` -- Source B gives this exact pattern requirement. |
| 8 | Nimbrel Probe stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source A states this verbatim. |
| 9 | If a Nimbrel Probe stream name contains characters other than letters, digits, spaces and hyphens, the agent refuses to start. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- Source A states that any other characters cause the agent to refuse to start. |
| 10 | A stream name containing a . (dot), such as `checkout.web`, is refused by Nimbrel Probe. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source B gives the dot example checkout.web as refused. |
| 11 | Nimbrel Probe refuses stream names containing any of a number of other symbols besides the dot. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source B says a number of other symbols besides the dot are also refused. |
| 12 | Nimbrel Probe refusing stream names with unsupported symbols is working as intended for now. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- Source B gives the cause of the refusal as working as intended for now. |
| 13 | Some organisations need the stream name kept exactly as it stands because that string is the product name used everywhere in the organisation. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org' in `source_a.md` -- The claim is a permitted generalisation of Source A's single-customer case. |
| 14 | Some organisations' reporting keys off the stream name. | supported | `source_a.md` | 'their reporting keyed of it' in `source_a.md` -- The claim generalises the customer's reporting keying off the stream name. |
| 15 | The stream name symbol restriction applies to all Nimbrel Probe agents. | supported | `source_a.md` | 'All Nimbrel Probe agents' in `source_a.md` -- Source A's environment for the restriction article is all Nimbrel Probe agents. |
| 16 | There is no fix at present for Nimbrel Probe stream names with unsupported symbols. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- Source B states there is no fix at present. |
| 17 | A workaround exists for Nimbrel Probe stream names with unsupported symbols. | supported | `source_a.md` | 'A way round it that works' in `source_a.md` -- Source A presents a working workaround. |
| 18 | The workaround's first step is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Source A gives this as step 1 of the workaround. |
| 19 | The workaround's second step is to carry the original stream name along as a global tag so that each trace keeps a link between the real name and the renamed one. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Source A gives this as step 2 of the workaround. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **19** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **22**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 6 run(s) over 15 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **17** departure(s) from its sources. Checking them confirms 9, rejects 1, and leaves 7 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b2` | superseded | Base metadata block kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b3` | superseded | Issue Description consolidated under the base Topic heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a4` | reconciled | Mandatory-field fact combined with b5's purpose; typo fixed. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-003`) |
| `b5` | reconciled | Purpose of stream name combined with a4. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-003`) |
| `a5` | reconciled | Restriction combined with b6's allowed characters; both links kept. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`A-004`) |
| `b6` | reconciled | Allowed characters and regex combined with a5; both links kept. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED (`B-004`, `B-005`) |
| `b4` | reworded | Topic: example of refused symbols, typos and backtick spacing fixed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b7` | superseded | Cause heading has no base slot; its content moved into Topic. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | reworded | Cause statement moved into Topic as a full sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `a7` | reworded | Generalised from one customer; trailing fragment 'when' removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`, `A-009`, `A-010`) |
| `b9` | superseded | Workaround consolidated under base Instructions/Answer heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Resolution consolidated under base Instructions/Answer heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a11` | reconciled | Workaround intro combined with b10's no-fix statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b10` | reconciled | No-fix statement joined to a11; rename step carried by a12. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Identical to b10. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a13` | reworded | Step 2: typo fixed, link kept. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-013`, `A-014`) |


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
| Tokens | 20,492 in, 12,874 out |
| Cost | ~$0.34 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 104.2s |
| Generated | 2026-09-27T17:13:44+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
