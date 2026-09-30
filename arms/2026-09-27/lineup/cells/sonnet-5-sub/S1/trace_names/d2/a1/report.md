## Verdict

**5 finding(s).** In the claims: 2 contradicted, 1 hallucinated. In the structure: 1 false departure, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 17 |
| Claims extracted from `source_a.md` | 11 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **22/24** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **11/11** |
| Forward — `source_b.md` claims accounted for | **11/13** |
| Reverse — merge claims found in a source | **16/17** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **40/40** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:3` says: The author of the document is Marlowe Ferrante.
  - `merged.md` says: 'Author: Rune Delacroix' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document names a different author than Marlowe Ferrante.
- **B-002** -- the two documents disagree
  - `source_b.md:4` says: The document was updated on 2026-02-03.
  - `merged.md` says: 'Updated: 2026-01-29' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document states a different update date than 2026-02-03.

### Invented — in the merge, in neither source

- **M-008** (`merged.md:14`) — A stream name such as checkout.web contains a number of other symbols along with the dot.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source lists checkout.web as an example of a dot-containing name and separately mentions other symbols being refused generally, but does not state checkout.web itself contains other symbols besides the dot.

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
| 1 | The document's author is Rune Delacroix. | 3 | carried | 'Author: Rune Delacroix' in `merged.md` -- The document explicitly names the author. |
| 2 | The document was updated on 2026-01-29. | 4 | carried | 'Updated: 2026-01-29' in `merged.md` -- The document explicitly states the update date. |
| 3 | Stream name is one of the mandatory fields for every Nimbrel Probe agent. | 8 | carried | 'The stream name is a mandatory field for every Nimbrel Probe agent' in `merged.md` -- Directly states the stream name is mandatory for every agent. |
| 4 | The stream name can't contain arbitrary symbols as documented. | 8 | carried | 'It cannot contain arbitrary symbols, as documented' in `merged.md` -- Directly matches the claim. |
| 5 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- Directly matches the claim. |
| 6 | Stream names may contain only letters, digits, spaces and hyphens, and nothing else, or the agent refuses to start. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start' in `merged.md` -- Directly matches the claim wording. |
| 7 | One customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org. | 15 | carried | 'one customer wanted the stream name left exactly as it stood, because that string was the product name used everywhere in the organization' in `merged.md` -- Directly matches the claim. |
| 8 | The customer's reporting keyed off the stream name. | 15 | carried | 'their reporting keyed off it' in `merged.md` -- States the customer's reporting keyed off the stream name. |
| 9 | A way to rename the stream to drop the unsupported symbols will allow the Nimbrel Probe agent to register. | 25 | carried | 'The workaround is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `merged.md` -- Directly matches the claim. |
| 10 | The original name can be carried along as a global tag. | 26 | carried | 'carry the original name along as a global tag' in `merged.md` -- Directly matches the claim. |
| 11 | Carrying the original name as a global tag keeps a link between the real name and the renamed one for each trace. | 26 | carried | 'so each trace keeps a link between the real name and the renamed one' in `merged.md` -- Directly matches the claim about keeping a link per trace. |

### `source_b.md` -- 13 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 11 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The author of the document is Marlowe Ferrante. | 3 | contradicted | 'Author: Rune Delacroix' in `merged.md` -- The document names a different author than Marlowe Ferrante. |
| 2 | The document was updated on 2026-02-03. | 4 | contradicted | 'Updated: 2026-01-29' in `merged.md` -- The document states a different update date than 2026-02-03. |
| 3 | Stream names containing a . (dot) are refused by Nimbrel Probe. | 8 | carried | 'a stream name such as `checkout.web`, which contains a dot, along with a number of other symbols, is refused by Nimbrel Probe' in `merged.md` -- Directly matches the claim about dot causing refusal. |
| 4 | A number of other symbols besides the dot are refused by Nimbrel Probe. | 8 | carried | 'along with a number of other symbols, is refused by Nimbrel Probe' in `merged.md` -- Directly matches the claim about other symbols being refused. |
| 5 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | 10 | carried | 'it is what separates one instrumented process from another' in `merged.md` -- Directly matches the claim in different but equivalent wording. |
| 6 | Only letters, digits, spaces and hyphens are accepted in the Nimbrel Probe stream name. | 10 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start' in `merged.md` -- Directly matches the claim. |
| 7 | The Nimbrel Probe stream name has to match the pattern ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- Directly matches the claim. |
| 8 | The stream name requirement is documented at https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name. | 10 | carried | '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' in `merged.md` -- The linked documentation URL matches the claim. |
| 9 | The behavior is working as intended for now. | 14 | carried | 'Working as intended for now.' in `merged.md` -- Directly matches the claim. |
| 10 | There is no fix at present for the dot-in-stream-name issue. | 18 | carried | 'There is no fix planned at present.' in `merged.md` -- States there is no fix planned, consistent with the dot-related issue described earlier. |
| 11 | The workaround is to rename the stream without the refused symbol. | 18 | carried | 'The workaround is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `merged.md` -- Directly matches the claim about renaming without the refused symbol. |
| 12 | There is no fix at present for the resolution of this issue. | 22 | carried | 'There is no fix planned at present.' in `merged.md` -- Directly matches the claim about no fix for the resolution of this issue. |
| 13 | The resolution is to rename the stream without the refused symbol. | 22 | carried | 'The workaround is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `merged.md` -- Directly matches the claim describing the resolution as renaming the stream. |

### `merged.md` -- 17 claim(s): 1 invented, 0 contradicted, 0 supported in part, 16 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 8 | A stream name such as checkout.web contains a number of other symbols along with the dot. | invented | -- | The source lists checkout.web as an example of a dot-containing name and separately mentions other symbols being refused generally, but does not state checkout.web itself contains other symbols besides the dot. |
| 1 | The stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source A states this directly, with a typo preserved in the original. |
| 2 | The stream name is what separates one instrumented process from another. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source B states this in equivalent words, using 'next' instead of 'another'. |
| 3 | The stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols' in `source_a.md` -- Directly stated in source A. |
| 4 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Verbatim match in source A's code block. |
| 5 | Stream names may only contain letters, digits, spaces and hyphens. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Directly stated in source B. |
| 6 | The agent refuses to start if the stream name contains anything other than letters, digits, spaces and hyphens. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start.' in `source_a.md` -- Directly stated in source A. |
| 7 | A stream name such as checkout.web contains a dot. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web`' in `source_b.md` -- Source B gives checkout.web as an example containing a dot. |
| 9 | A stream name such as checkout.web is refused by Nimbrel Probe. | supported | `source_b.md` | 'are refused by Nimbrel Probe' in `source_b.md` -- Source B states such names are refused. |
| 10 | One customer wanted the stream name left exactly as it stood. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood' in `source_a.md` -- Directly stated in source A. |
| 11 | That string was the product name used everywhere in the customer's organization. | supported | `source_a.md` | 'that string was the product name in use everywhere in the org' in `source_a.md` -- Directly stated in source A. |
| 12 | The customer's reporting keyed off that string. | supported | `source_a.md` | 'their reporting keyed of it' in `source_a.md` -- Directly stated in source A, with original typo preserved. |
| 13 | This behavior is working as intended for now. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- Directly stated under Cause in source B. |
| 14 | The affected environment is all Nimbrel Probe agents. | supported | `source_a.md` | 'All Nimbrel Probe agents' in `source_a.md` -- Directly stated under Environment in source A. |
| 15 | There is no fix planned at present for this issue. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- Directly stated under Resolution in source B. |
| 16 | The workaround is to rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Directly stated in source A's Instructions/Answer. |
| 17 | The original name can be carried along as a global tag so each trace keeps a link between the real name and the renamed one. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Directly stated in source A's Instructions/Answer. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **17** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **24**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 5 run(s) over 12 attributed segment(s) — sources interleaved. 5 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a12` (`source_a.md`) — 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
  In the merge:  rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
  What changed:  [-R-]{+r+}ename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **18** departure(s) from its sources. Checking them confirms 10, rejects 2, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title chosen over this one. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b2` | superseded | Base byline chosen over this one. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`, `B-002`) |
| `b3` | superseded | Consolidated under base's Topic heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a4` | reworded | Fixed 'mandatry' typo and combined with b5's fact. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `b5` | subsumed | Process-separation fact folded into combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`) |
| `a5` | reworded | Kept fact and link, added b6's link alongside it. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `b6` | subsumed | Regex restatement duplicates a6's code block; its link preserved here. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-006`, `B-007`, `B-008`) |
| `b4` | reworded | Fixed 'exampe' typo; example placed after the regex rule. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-003`, `B-004`) |
| `a7` | reworded | Fixed 'keyed of it when' grammar; content otherwise unchanged. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-007`, `A-008`) |
| `b9` | superseded | Consolidated under base's Instructions/Answer heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | duplicate | Repeats b9's heading purpose, already superseded once. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a11` | reworded | Introductory phrase merged with b10's no-fix statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a12` | subsumed | Step one folded into combined workaround sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-009`) |
| `a13` | subsumed | Step two folded into combined workaround sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-010`, `A-011`) |
| `b10` | subsumed | No-fix/rename fact merged into combined workaround sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Repeats b10's text verbatim under a different heading. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a14` | reworded | Merged into single internal-notes block alongside b13's ticket link. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b13` | subsumed | Ticket link combined with a14's into one internal-notes block. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | d320da0eb7ed (command) -- lineup sonnet-5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 -> claude-sonnet-5 |
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
| Duration | 595.5s |
| Generated | 2026-09-27T18:59:30+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
