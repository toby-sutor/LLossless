## Verdict

**3 finding(s).** In the claims: 1 contradicted. In the structure: 2 verbatim violation.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 21 |
| Claims extracted from `source_a.md` | 14 |
| Claims extracted from `source_b.md` | 10 |
| Forward — source claims accounted for in the merge | **23/24** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **13/14** |
| Forward — `source_b.md` claims accounted for | **10/10** |
| Reverse — merge claims found in a source | **21/21** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **45/45** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-002** -- the two documents disagree
  - `source_a.md:4` says: The document was updated on 2026-01-29.
  - `merged.md` says: 'Updated: 2026-02-03' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text gives a different update date.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 14 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 13 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | The document was updated on 2026-01-29. | 4 | contradicted | 'Updated: 2026-02-03' in `merged.md` -- The reference text gives a different update date. |
| 1 | The document author is Rune Delacroix. | 3 | carried | 'Author: Rune Delacroix, Marlowe Ferrante' in `merged.md` -- Rune Delacroix is listed as an author. |
| 3 | Stream name is a mandatory field for every Nimbrel Probe agent. | 8 | carried | 'The stream name is a mandatory field for every Nimbrel Probe agent' in `merged.md` -- The reference text states this directly. |
| 4 | The Nimbrel Probe stream name cannot contain arbitrary symbols. | 8 | carried | 'It cannot contain arbitrary symbols' in `merged.md` -- The reference text states the stream name cannot contain arbitrary symbols. |
| 5 | Nimbrel Probe stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | 12 | carried | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `merged.md` -- The reference text states this directly. |
| 6 | Nimbrel Probe stream names may contain only letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only' in `merged.md` -- The reference text restricts stream names to these characters. |
| 7 | The Nimbrel Probe agent refuses to start if the stream name contains characters other than letters, digits, spaces and hyphens. | 12 | carried | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start' in `merged.md` -- The reference text states the agent refuses to start otherwise. |
| 8 | One customer wanted the stream name left exactly as it stood. | 15 | carried | 'some organisations need the stream name kept exactly as it stands' in `merged.md` -- The generalised statement about organisations entails the customer's need. |
| 9 | The customer's stream name string was the product name in use everywhere in the customer's org. | 15 | carried | 'because the string is the product name used everywhere in the organisation' in `merged.md` -- The reference text states the string is the product name used throughout the organisation. |
| 10 | The customer's reporting was keyed off the stream name string. | 15 | carried | 'their reporting keys off it' in `merged.md` -- The reference text states reporting keys off the stream name string. |
| 11 | The issue applies to all Nimbrel Probe agents. | 19 | carried | 'All Nimbrel Probe agents' in `merged.md` -- The Environment section lists all Nimbrel Probe agents. |
| 12 | Renaming the stream to drop the unsupported symbols allows the Nimbrel Probe agent to register. | 25 | carried | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register.' in `merged.md` -- The reference text states this directly. |
| 13 | The original stream name can be carried along as a global tag. | 26 | carried | 'Carry the original name along as a global tag' in `merged.md` -- The reference text states this directly. |
| 14 | Carrying the original stream name as a global tag lets each trace keep a link between the real name and the renamed one. | 26 | carried | 'so that each trace keeps a link between the real name and the renamed one' in `merged.md` -- The reference text states this is the purpose of the global tag. |

### `source_b.md` -- 10 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Nimbrel Probe refuses stream names containing a . (dot). | 8 | carried | 'A stream name containing a . (dot), for example `checkout.web`, or any of a number of other symbols is refused by Nimbrel Probe.' in `merged.md` -- The reference text states stream names with a dot are refused. |
| 2 | Nimbrel Probe refuses the stream name checkout.web. | 8 | carried | 'A stream name containing a . (dot), for example `checkout.web`, or any of a number of other symbols is refused by Nimbrel Probe.' in `merged.md` -- The reference text gives checkout.web as an example of a refused name. |
| 3 | Nimbrel Probe refuses stream names containing a number of symbols other than the dot. | 8 | carried | 'A stream name containing a . (dot), for example `checkout.web`, or any of a number of other symbols is refused by Nimbrel Probe.' in `merged.md` -- The reference text states a number of other symbols are also refused. |
| 4 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | 10 | carried | 'it is what separates one instrumented process from the next' in `merged.md` -- The reference text states this directly. |
| 5 | Only letters, digits, spaces and hyphens are accepted in the Nimbrel Probe stream name. | 10 | carried | 'only letters, digits, spaces and hyphens are accepted' in `merged.md` -- The reference text states this directly. |
| 6 | The Nimbrel Probe stream name has to match ^[A-Za-z0-9 -]+$. | 10 | carried | 'the name must match ^[A-Za-z0-9 -]+$' in `merged.md` -- The reference text states this directly. |
| 7 | The Nimbrel Probe stream name restriction is documented at https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name. | 10 | carried | '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' in `merged.md` -- The restriction is documented at this link. |
| 8 | Nimbrel Probe refusing stream names with a dot is working as intended for now. | 14 | carried | 'This behaviour is working as intended for now.' in `merged.md` -- The reference text states the refusal behaviour is working as intended for now. |
| 9 | There is no fix at present for Nimbrel Probe refusing stream names with a dot. | 18 | carried | 'There is no fix at present' in `merged.md` -- The reference text states there is no fix at present. |
| 10 | The workaround is to rename the stream without the refused symbol. | 18 | carried | 'Rename the stream to drop the unsupported symbols' in `merged.md` -- The workaround renames the stream without the refused symbols. |

### `merged.md` -- 21 claim(s): 0 invented, 0 contradicted, 0 supported in part, 21 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | The document authors are Rune Delacroix and Marlowe Ferrante. | supported | `source_a.md` | 'Author: Rune Delacroix' in `source_a.md` -- Source_a names Rune Delacroix and source_b's 'Author: Marlowe Ferrante' supplies the other, so the merged document's joint authorship follows from both. |
| 2 | The document was updated on 2026-02-03. | supported | `source_b.md` | 'Updated: 2026-02-03' in `source_b.md` -- Source_b gives this update date, which is the later of the two source dates. |
| 3 | The stream name is a mandatory field for every Nimbrel Probe agent. | supported | `source_a.md` | 'Stream name is one of the mandatry field for every Nimbrel Probe agent.' in `source_a.md` -- Source_a states the stream name is mandatory for every agent. |
| 4 | The Nimbrel Probe stream name is what separates one instrumented process from the next. | supported | `source_b.md` | 'The Nimbrel Probe stream name is what seperates one instrumented process from the next.' in `source_b.md` -- Source_b states this directly. |
| 5 | The Nimbrel Probe stream name cannot contain arbitrary symbols. | supported | `source_a.md` | 'The stream name cant contain arbitrary symbols' in `source_a.md` -- Source_a states the stream name cannot contain arbitrary symbols. |
| 6 | Only letters, digits, spaces and hyphens are accepted in the Nimbrel Probe stream name. | supported | `source_b.md` | 'Only letters, digits, spaces and hyphens are accepted' in `source_b.md` -- Source_b states the allowed character set. |
| 7 | The Nimbrel Probe stream name must match ^[A-Za-z0-9 -]+$. | supported | `source_b.md` | 'it has to match ^[A-Za-z0-9 -]+$' in `source_b.md` -- Source_b gives this pattern as required. |
| 8 | The stream name character restriction is documented at https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name. | supported | `source_a.md` | '[here](https://docs.nimbrel.example/probe/agent/java/current/config-core.html#config-stream-name)' in `source_a.md` -- Source_a cites this URL as documenting the restriction. |
| 9 | The stream name character restriction is documented at https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name. | supported | `source_b.md` | '[here](https://docs.nimbrel.example/probe/agent/browser/current/configuration.html#stream-name)' in `source_b.md` -- Source_b cites this URL as documenting the restriction. |
| 10 | A stream name containing a . (dot), for example `checkout.web`, is refused by Nimbrel Probe. | supported | `source_b.md` | 'Stream name containing a . (dot) for exampe` checkout.web` along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source_b states dot-containing names like checkout.web are refused. |
| 11 | A stream name containing any of a number of other symbols is refused by Nimbrel Probe. | supported | `source_b.md` | 'along with a number of other symbols are refused by Nimbrel Probe' in `source_b.md` -- Source_b states a number of other symbols are also refused. |
| 12 | Nimbrel Probe stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers. | supported | `source_a.md` | 'Stream names are validated against ^[A-Za-z0-9 -]+$ before the agent registers.' in `source_a.md` -- Source_a states this verbatim. |
| 13 | If a Nimbrel Probe stream name contains anything other than letters, digits, spaces and hyphens, the agent refuses to start. | supported | `source_a.md` | 'letters, digits, spaces and hyphens only, and nothing else, or the agent refuses to start' in `source_a.md` -- Source_a states the agent refuses to start otherwise. |
| 14 | The Nimbrel Probe stream name validation behaviour is working as intended for now. | supported | `source_b.md` | 'Working as intended for now' in `source_b.md` -- Source_b's Cause section states this. |
| 15 | Some organisations need the Nimbrel Probe stream name kept exactly as it stands. | supported | `source_a.md` | 'one customer wanted the stream name left exactly as it stood' in `source_a.md` -- The claim generalises source_a's single customer case, which is permitted at high fidelity. |
| 16 | The stream name validation issue applies to all Nimbrel Probe agents. | supported | `source_a.md` | 'All Nimbrel Probe agents' in `source_a.md` -- Source_a's Environment section lists all Nimbrel Probe agents. |
| 17 | There is no fix at present for the Nimbrel Probe stream name symbol restriction. | supported | `source_b.md` | 'No fix at present , rename the stream without the refused symbol' in `source_b.md` -- Source_b states there is no fix at present. |
| 18 | A workaround exists for the Nimbrel Probe stream name symbol restriction. | supported | `source_a.md` | 'A way round it that works' in `source_a.md` -- Source_a offers a working workaround. |
| 19 | Renaming the stream to drop the unsupported symbols allows the Nimbrel Probe agent to register. | supported | `source_a.md` | 'Rename the stream to drop the unsupported symbols so the Nimbrel Probe agent will register' in `source_a.md` -- Source_a states this step directly. |
| 20 | Carrying the original stream name as a global tag keeps a link in each trace between the real name and the renamed one. | supported | `source_a.md` | 'Then carry the orignal name along as a global tag, so at least each trace keeps a link between the real name and the renamed one' in `source_a.md` -- Source_a states this directly. |
| 21 | Global tags for the Nimbrel Probe Node.js agent are documented at https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags. | supported | `source_a.md` | 'https://docs.nimbrel.example/probe/agent/nodejs/current/configuration.html#global-tags' in `source_a.md` -- Source_a links this Node.js agent global-tags documentation URL. |

## Structure

**9** mechanical check(s) over **27** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **21** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **24**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 8 run(s) over 15 attributed segment(s) — sources interleaved. 4 of 9 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '2026-01-29' does not survive into the merge unchanged
- `b4` (`source_b.md`) — code '` checkout.web`' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **19** departure(s) from its sources. Checking them confirms 10, rejects 2, and leaves 7 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 27 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | superseded | Base title kept. | **confirmed** | no claim is drawn from a title, and the title check passed this one: it is superseded by 'Nimbrel Probe stream name with unsupported symbols' and says so (no claim traced to it) |
| `a2` | reconciled | Author block lists both authors and the later update date. | **rejected** | declared 'reconciled', which predicts SUPPORTED; A-002 came back CONTRADICTED (`A-002`) |
| `b2` | reconciled | Author block lists both authors and the later update date. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reconciled' is what happened to it (no claim traced to it) |
| `b3` | superseded | Base heading used for the problem description. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b7` | superseded | Cause content moved under the base Topic heading. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a4` | reworded | Fixed spelling and grammar; combined with b5. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-003`) |
| `b5` | subsumed | Purpose of stream name joined with mandatory-field statement. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `a5` | reworded | Restriction statement combined with b6; both links kept. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-004`) |
| `b6` | subsumed | Allowed characters, regex and link carried in combined sentence. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`, `B-006`, `B-007`) |
| `b4` | reworded | Fixed spelling and code-span spacing. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`, `B-003`) |
| `a7` | reworded | Generalised the single-customer narrative; fixed truncation and typos. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`, `A-009`, `A-010`) |
| `b8` | reworded | Cause statement placed in Topic as a full sentence. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-008`) |
| `b9` | superseded | Base heading used for the workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b11` | superseded | Base heading used; resolution repeats the workaround. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `a11` | reworded | Intro combined with b10's no-fix statement. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b10` | subsumed | No-fix and rename advice carried by intro and step 1. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b12` | duplicate | Identical to b10. | **rejected** | declared 'duplicate', and its text is not in the merge (no claim traced to it) |
| `a12` | reworded | Added closing punctuation. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-012`) |
| `a13` | reworded | Fixed spelling and phrasing; URL kept. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-013`, `A-014`) |


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
| Tokens | 20,632 in, 14,927 out |
| Cost | ~$0.38 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 117.1s |
| Generated | 2026-09-27T17:03:23+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `af5cd272c023` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
