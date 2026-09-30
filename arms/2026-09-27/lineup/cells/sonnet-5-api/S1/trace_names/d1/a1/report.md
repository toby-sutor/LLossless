## Verdict

**7 finding(s).** In the claims: 2 partially dropped, 2 contradicted, 1 hallucinated. In the structure: 1 false departure, 1 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 18 |
| Claims extracted from `source_a.md` | 13 |
| Claims extracted from `source_b.md` | 12 |
| Forward — source claims accounted for in the merge | **21/25** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **13/13** |
| Forward — `source_b.md` claims accounted for | **8/12** (2 in part) |
| Reverse — merge claims found in a source | **17/18** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **42/42** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-009** (`source_b.md:18`) — There is no fix at present for this issue, as stated under Workaround.
  - evidence: 'There is no fix at present.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The 'no fix at present' fact is stated, but the text uses an 'Instructions/Answer' section, not one labeled 'Workaround'.
- **B-011** (`source_b.md:22`) — There is no fix at present for this issue, as stated under Resolution.
  - evidence: 'There is no fix at present.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The 'no fix at present' fact is stated, but the text uses an 'Instructions/Answer' section, not one labeled 'Resolution'.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:3` says: The author is Marlowe Ferrante.
  - `merged.md` says: 'Author: Rune Delacroix' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document names a different author than claimed.
- **B-002** -- the two documents disagree
  - `source_b.md:4` says: The document was updated on 2026-02-03.
  - `merged.md` says: 'Updated: 2026-01-29' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document states a different update date than claimed.

### Invented — in the merge, in neither source

- **M-012** (`merged.md:14`) — There is no fix planned for the stream name symbol restriction.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source_b.md only says no fix exists at present; it never states whether a fix is or isn't planned for the future.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 13 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 13 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The author of the document is Rune Delacroix. | 3 | carried | 'Author: Rune Delacroix' in `merged.md` -- The document explicitly states the author's name. |
| 2 | The document was updated on 2026-01-29. | 4 | carried | 'Updated: 2026-01-29' in `merged.md` -- The document explicitly states the update date. |
| 3 | Stream name is one of the mandatory fields for every Nimbrel Probe agent. | 8 | carried | 'Stream name is one of the mandatory fields for every Nimbrel Probe agent' in `merged.md` -- This is directly stated in the topic section. |
| 4 | The stream name cannot contain arbitrary symbols. | 8 | carried | 'The stream name cannot contain arbitrary symbols' in `merged.md` -- Directly stated in the topic section. |
| 5 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- This is a verbatim statement of the validation regex. |
| 6 | Stream names may only contain letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- Directly states the allowed character set. |
| 7 | The agent refuses to start if the stream name contains characters other than letters, digits, spaces and hyphens. | 12 | carried | 'or the agent refuses to start' in `merged.md` -- Directly states the consequence of invalid characters. |
| 8 | One customer wanted the stream name left exactly as it stood. | 15 | carried | 'Where the original name matters — for instance when it is a product name already in use throughout the organization and referenced by existing reporting — carry it forward as a global tag' in `merged.md` -- The general scenario describes wanting to preserve the original stream name. |
| 9 | That string was the product name in use everywhere in the customer's org. | 15 | carried | 'Where the original name matters — for instance when it is a product name already in use throughout the organization and referenced by existing reporting — carry it forward as a global tag' in `merged.md` -- The scenario states the name is a product name already in use throughout the organization. |
| 10 | The customer's reporting keyed off that string. | 15 | carried | 'Where the original name matters — for instance when it is a product name already in use throughout the organization and referenced by existing reporting — carry it forward as a global tag' in `merged.md` -- The scenario states the name is referenced by existing reporting. |
| 11 | The workaround applies to all Nimbrel Probe agents. | 19 | carried | 'All Nimbrel Probe agents' in `merged.md` -- The Environment section states the issue and workaround apply to all Nimbrel Probe agents. |
| 12 | Renaming the stream to drop the unsupported symbols allows the Nimbrel Probe agent to register. | 25 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.' in `merged.md` -- This directly states the renaming action allows registration. |
| 13 | Carrying the original name along as a global tag keeps a link between the real name and the renamed one for each trace. | 26 | carried | 'carry it forward as a global tag, so each trace still keeps a link between the real name and the renamed one' in `merged.md` -- Directly states the global tag preserves a link between the real and renamed names. |

### `source_b.md` -- 12 claim(s): 0 dropped, 2 contradicted, 2 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The author is Marlowe Ferrante. | 3 | contradicted | 'Author: Rune Delacroix' in `merged.md` -- The document names a different author than claimed. |
| 2 | The document was updated on 2026-02-03. | 4 | contradicted | 'Updated: 2026-01-29' in `merged.md` -- The document states a different update date than claimed. |
| 9 | There is no fix at present for this issue, as stated under Workaround. | 18 | carried in part | 'There is no fix at present.' in `merged.md` -- The 'no fix at present' fact is stated, but the text uses an 'Instructions/Answer' section, not one labeled 'Workaround'. |
| 11 | There is no fix at present for this issue, as stated under Resolution. | 22 | carried in part | 'There is no fix at present.' in `merged.md` -- The 'no fix at present' fact is stated, but the text uses an 'Instructions/Answer' section, not one labeled 'Resolution'. |
| 3 | Stream names containing a . (dot), for example `checkout.web`, along with a number of other symbols, are refused by Nimbrel Probe. | 8 | carried | 'A stream name containing a . (dot) — for example `checkout.web` — along with a number of other symbols, is refused for this reason.' in `merged.md` -- This matches the claim verbatim in meaning. |
| 4 | The Nimbrel Probe stream name is what seperates one instrumented process from the next. | 10 | carried | 'it is what separates one instrumented process from the next' in `merged.md` -- This matches the claim's meaning despite the claim's alternate spelling of 'separates'. |
| 5 | Only letters, digits, spaces and hyphens are accepted for Nimbrel Probe stream names. | 10 | carried | 'letters, digits, spaces and hyphens only, and nothing else' in `merged.md` -- Directly states the allowed character set. |
| 6 | The accepted Nimbrel Probe stream name pattern must match ^[A-Za-z0-9 -]+$. | 10 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- States the exact regex pattern for stream names. |
| 7 | The stream name character restriction is documented at https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name. | 10 | carried | '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' in `merged.md` -- This link is cited as documentation for the stream name restriction. |
| 8 | The cause of the issue is described as working as intended for now. | 14 | carried | 'This is expected behaviour rather than a bug, and there is no fix planned.' in `merged.md` -- This paraphrases the cause as working as intended with no planned fix. |
| 10 | The workaround is to rename the stream without the refused symbol. | 18 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.' in `merged.md` -- This describes the recommended action of renaming the stream to avoid the refused symbol. |
| 12 | The resolution is to rename the stream without the refused symbol. | 22 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.' in `merged.md` -- This describes the recommended resolution of renaming the stream to avoid the refused symbol. |

### `merged.md` -- 18 claim(s): 1 invented, 0 contradicted, 0 supported in part, 17 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 12 | There is no fix planned for the stream name symbol restriction. | invented | -- | Source_b.md only says no fix exists at present; it never states whether a fix is or isn't planned for the future. |
| 1 | Rune Delacroix is the author of the document. | supported | `source_a.md` | 'Author: Rune Delacroix' in `source_a.md` -- Source_a.md explicitly lists Rune Delacroix as the author. |
| 2 | The document was updated on 2026-01-29. | supported | `source_a.md` | 'Updated: 2026-01-29' in `source_a.md` -- Source_a.md explicitly states the update date as 2026-01-29. |
| 3 | Stream name is one of the mandatory fields for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source_a.md states this fact, with the typo 'mandatry' generalized to 'mandatory'. |
| 4 | Stream name is what separates one instrumented process from the next. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source_b.md states this directly, with the typo 'seperates'. |
| 5 | The stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols as documented' in `source_a.md` -- Source_a.md states this directly. |
| 6 | Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Exact match found in source_a.md's quoted config block. |
| 7 | Stream names may contain only letters, digits, spaces and hyphens, and nothing else. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else' in `source_a.md` -- Source_a.md states this restriction verbatim. |
| 8 | If the stream name contains characters other than letters, digits, spaces and hyphens, the agent refuses to start. | supported | `source_a.md` | 'or the agent refuses to start.' in `source_a.md` -- Source_a.md states that violating the symbol rule causes the agent to refuse to start. |
| 9 | A stream name containing a . (dot), for example `checkout.web`, is refused. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source_b.md gives this exact example and states it is refused. |
| 10 | Stream names containing a number of other symbols besides a dot are also refused. | supported | `source_b.md` | 'along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source_b.md states other symbols besides the dot are also refused. |
| 11 | This behaviour is expected rather than a bug. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- Source_b.md's Cause section states this is expected behaviour, not a bug. |
| 13 | There is no fix at present for the stream name symbol restriction. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- Source_b.md's Workaround/Resolution sections state exactly that there is no fix at present. |
| 14 | Renaming the stream to drop the unsupported symbols allows the Nimbrel Probe agent to register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Source_a.md's instructions state this exact workaround step. |
| 15 | The original name may matter when it is a product name already in use throughout the organization. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood because that string was the product name in use everywhere in the org' in `source_a.md` -- Source_a.md describes this exact customer scenario about the product name. |
| 16 | The original name may matter when it is referenced by existing reporting. | supported | `source_a.md` | 'and their reporting keyed of it when' in `source_a.md` -- Source_a.md mentions the customer's reporting being keyed off the original name. |
| 17 | The original name can be carried forward as a global tag. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag' in `source_a.md` -- Source_a.md's instructions state this exact step. |
| 18 | Each trace keeps a link between the real name and the renamed one when the original name is carried forward as a global tag. | supported | `source_a.md` | 'so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Source_a.md states this outcome of carrying the original name as a global tag. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **18** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **25**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 5 run(s) over 11 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a12` (`source_a.md`) — 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register
  In the merge:  Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.
  What changed:  Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register{+.+}
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **18** departure(s) from its sources. Checking them confirms 11, rejects 1, and leaves 6 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a4` | subsumed | Combined with b5's fact into one descriptive sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-003`) |
| `a5` | subsumed | Combined with b6's link into one sentence with both links. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-004`) |
| `a7` | reworded | Generalised from a single customer's case to the general rule. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`, `A-009`, `A-010`) |
| `a11` | subsumed | Intro folded into the workaround sentence. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a12` | subsumed | Step 1 restated as the workaround sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-012`) |
| `a13` | subsumed | Step 2 restated with its link kept. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-013`) |
| `b1` | superseded | Base title chosen over this one. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `b2` | superseded | Base byline chosen; bylines cannot both stand. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-001`, `B-002`) |
| `b3` | superseded | Base heading used for the consolidated section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b4` | subsumed | Dot example kept, folded into topic paragraph. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b5` | subsumed | Combined with a4's fact. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b6` | subsumed | Browser link kept; regex restatement duplicates the code block. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`, `B-006`, `B-007`) |
| `b7` | subsumed | Cause heading dropped; content folded into topic paragraph. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b8` | subsumed | Cause statement reworded into the topic paragraph. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`) |
| `b9` | superseded | Workaround heading merged into base's Instructions/Answer heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | Workaround text folded into the combined instructions. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b11` | superseded | Resolution heading merged into base's Instructions/Answer heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Identical wording to the workaround already stated. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |


## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 20,132 in, 31,017 out |
| Cost | ~$0.35 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 265.7s |
| Generated | 2026-09-27T16:54:16+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
