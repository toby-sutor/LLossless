## Verdict

**2 finding(s).** In the claims: 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 19 |
| Claims extracted from `source_a.md` | 14 |
| Claims extracted from `source_b.md` | 11 |
| Forward — source claims accounted for in the merge | **23/25** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **14/14** |
| Forward — `source_b.md` claims accounted for | **9/11** |
| Reverse — merge claims found in a source | **19/19** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **44/44** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:3` says: The author of the Nimbrel Probe document is Marlowe Ferrante.
  - `merged.md` says: 'Author: Rune Delacroix' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Rune Delacroix as author, not Marlowe Ferrante.
- **B-002** -- the two documents disagree
  - `source_b.md:4` says: The Nimbrel Probe document was updated 2026-02-03.
  - `merged.md` says: 'Updated: 2026-01-29' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives the update date as 2026-01-29, not 2026-02-03.

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
| 5 | Nimbrel Probe stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The quoted documentation states this validation pattern and timing. |
| 6 | Nimbrel Probe stream names may contain only letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only' in `merged.md` -- The text restricts stream names to letters, digits, spaces and hyphens. |
| 7 | The Nimbrel Probe agent refuses to start if the stream name contains characters other than letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start' in `merged.md` -- The text states the agent refuses to start if other characters are present. |
| 8 | One customer wanted the stream name left exactly as it stood. | 15 | carried | 'a stream name sometimes has to stay exactly as it stands' in `merged.md` -- The merged text generalises the single customer case into a broader statement that entails it. |
| 9 | The customer's stream name string was the product name in use everywhere in the customer's org. | 15 | carried | 'that string is the product name in use everywhere in the organisation' in `merged.md` -- The text states the string is the product name used throughout the organisation. |
| 10 | The customer's reporting was keyed off the stream name string. | 15 | carried | 'reporting keys off it' in `merged.md` -- The text states reporting is keyed off the stream name string. |
| 11 | The issue applies to all Nimbrel Probe agents. | 19 | carried | 'All Nimbrel Probe agents' in `merged.md` -- The Environment section lists all Nimbrel Probe agents. |
| 12 | Renaming the stream to drop the unsupported symbols allows the Nimbrel Probe agent to register. | 25 | carried | 'Rename the stream to drop the unsupported symbols so that the Nimbrel Probe agent registers.' in `merged.md` -- The workaround step states renaming lets the agent register. |
| 13 | The original stream name can be carried along as a global tag. | 26 | carried | 'Carry the original name along as a global tag' in `merged.md` -- The workaround says to carry the original name as a global tag. |
| 14 | Carrying the original stream name as a global tag lets each trace keep a link between the real name and the renamed one. | 26 | carried | 'Carry the original name along as a global tag, so that each trace keeps a link between the real name and the renamed one' in `merged.md` -- The text states the global tag keeps a per-trace link between the real and renamed names. |

### `source_b.md` -- 11 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The author of the Nimbrel Probe document is Marlowe Ferrante. | 3 | contradicted | 'Author: Rune Delacroix' in `merged.md` -- The reference names Rune Delacroix as author, not Marlowe Ferrante. |
| 2 | The Nimbrel Probe document was updated 2026-02-03. | 4 | contradicted | 'Updated: 2026-01-29' in `merged.md` -- The reference gives the update date as 2026-01-29, not 2026-02-03. |
| 3 | Nimbrel Probe refuses stream names containing a . (dot), for example checkout.web. | 8 | carried | 'A stream name containing a . (dot), for example ` checkout.web`, is refused' in `merged.md` -- The text states a name containing a dot, such as checkout.web, is refused. |
| 4 | Nimbrel Probe refuses stream names containing a number of other symbols besides the dot. | 8 | carried | 'as are names containing a number of other symbols' in `merged.md` -- The text states names with a number of other symbols are also refused. |
| 5 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | 10 | carried | 'is what separates one instrumented process from the next' in `merged.md` -- The text states the stream name separates one instrumented process from the next. |
| 6 | Only letters, digits, spaces and hyphens are accepted in the Nimbrel Probe stream name. | 10 | carried | 'letters, digits, spaces and hyphens only' in `merged.md` -- The text restricts accepted characters to letters, digits, spaces and hyphens. |
| 7 | The Nimbrel Probe stream name has to match ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- Validation against this pattern means the name must match it. |
| 8 | The stream name restriction is documented at https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name. | 10 | carried | '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' in `merged.md` -- This URL is cited as documenting the stream name restriction. |
| 9 | The refusal of stream names containing a dot in Nimbrel Probe is working as intended for now. | 14 | carried | 'This is working as intended for now.' in `merged.md` -- The text states the refusal is working as intended for now. |
| 10 | There is no fix at present for Nimbrel Probe refusing stream names containing a dot. | 18 | carried | 'There is no fix at present.' in `merged.md` -- The text states there is no fix at present. |
| 11 | The workaround is to rename the stream without the refused symbol. | 18 | carried | 'Rename the stream to drop the unsupported symbols' in `merged.md` -- The workaround is to rename the stream dropping the unsupported symbols. |

### `merged.md` -- 19 claim(s): 0 invented, 0 contradicted, 0 supported in part, 19 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The document author is Rune Delacroix. | supported | `source_a.md` | 'Author: Rune Delacroix' in `source_a.md` -- Source A names Rune Delacroix as its author. |
| 2 | The document was updated on 2026-01-29. | supported | `source_a.md` | 'Updated: 2026-01-29' in `source_a.md` -- Source A gives 2026-01-29 as its update date. |
| 3 | The stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source A states that the stream name is a mandatory field for every agent. |
| 4 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source B states this directly. |
| 5 | The Nimbrel Probe stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols' in `source_a.md` -- Source A states that the stream name cannot contain arbitrary symbols. |
| 6 | Nimbrel Probe stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source A states this validation verbatim. |
| 7 | Nimbrel Probe stream names may contain letters, digits, spaces and hyphens only. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Source B states that only these characters are accepted, and source A agrees. |
| 8 | The Nimbrel Probe agent refuses to start if the stream name contains characters other than letters, digits, spaces and hyphens. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- Source A states that the agent refuses to start if the name contains other characters. |
| 9 | A Nimbrel Probe stream name containing a . (dot), for example ` checkout.web`, is refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source B states that dotted names such as checkout.web are refused. |
| 10 | Nimbrel Probe stream names containing a number of other symbols besides the dot are refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source B states that a number of other symbols are refused too. |
| 11 | The refusal of Nimbrel Probe stream names containing unsupported symbols is working as intended for now. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- Source B gives the cause as working as intended for now. |
| 12 | A Nimbrel Probe stream name sometimes has to stay exactly as it stands because that string is the product name in use everywhere in the organisation. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org' in `source_a.md` -- The claim generalises source A's single customer case, which is permitted at high fidelity. |
| 13 | Reporting sometimes keys off the Nimbrel Probe stream name. | supported | `source_a.md` | 'their reporting keyed of it' in `source_a.md` -- The claim generalises source A's statement that the customer's reporting keyed off the name. |
| 14 | The stream name symbol restriction applies to all Nimbrel Probe agents. | supported | `source_a.md` | 'All Nimbrel Probe agents' in `source_a.md` -- Source A gives the environment as all Nimbrel Probe agents. |
| 15 | There is no fix at present for Nimbrel Probe stream names with unsupported symbols. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- Source B states that there is no fix at present. |
| 16 | A workaround exists for Nimbrel Probe stream names with unsupported symbols. | supported | `source_a.md` | 'A way round it that works' in `source_a.md` -- Source A presents a working workaround, and source B has a Workaround section. |
| 17 | Renaming the stream to drop the unsupported symbols allows the Nimbrel Probe agent to register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Source A states this directly. |
| 18 | Carrying the original stream name along as a global tag lets each trace keep a link between the real name and the renamed one. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Source A states this directly. |
| 19 | Global tags configuration for the Nimbrel Probe Node.js agent is documented at https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags. | supported | `source_a.md` | 'https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags' in `source_a.md` -- Source A links this nodejs configuration URL with a global-tags anchor for the global tag step. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **19** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **25**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 4 run(s) over 15 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **18** departure(s) from its sources. Checking them confirms 11, rejects 1, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | reworded | Topic: spelling fixed and joined with b5's purpose statement. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `a5` | reworded | Topic: rewritten and both documentation links carried together. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `a7` | reworded | Topic: generalised; truncated trailing 'when' fragment removed. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`, `A-009`, `A-010`) |
| `a11` | reworded | Answer: intro line rewritten as a sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a12` | reworded | Answer: step 1 copy-edited. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `a13` | reworded | Answer: step 2 spelling fixed; URL kept verbatim. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-013`, `A-014`) |
| `b1` | superseded | Title: base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b2` | superseded | Metadata: base author and date block kept. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`, `B-002`) |
| `b3` | superseded | Heading: consolidated into base Topic heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | reworded | Topic: copy-edited; example code span kept as written. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `b5` | subsumed | Topic: purpose statement joined to a4's sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`) |
| `b6` | subsumed | Topic: rule and regex carried by a6's block; link kept here. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-006`, `B-007`, `B-008`) |
| `b7` | superseded | Heading: cause folded into base Topic section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b8` | reworded | Topic: cause statement placed after the refused-symbol description. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-009`) |
| `b9` | superseded | Heading: consolidated into base answer heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | Answer: no-fix statement and rename step carried in answer section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | superseded | Heading: consolidated into base answer heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Answer: identical to b10. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 31c2462e2828 (command) -- lineup opus-5.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 -> claude-opus-5-5 |
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
| Duration | 124.2s |
| Generated | 2026-09-27T20:05:34+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
