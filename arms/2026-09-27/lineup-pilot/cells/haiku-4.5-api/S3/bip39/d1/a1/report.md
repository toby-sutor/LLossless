## Verdict

**2 finding(s).** In the claims: 2 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 14 |
| Claims extracted from `source_a.md` | 6 |
| Claims extracted from `source_b.md` | 9 |
| Forward — source claims accounted for in the merge | **13/15** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **6/6** |
| Forward — `source_b.md` claims accounted for | **7/9** |
| Reverse — merge claims found in a source | **14/14** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **29/29** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **B-001** -- the two documents disagree
  - `source_b.md:2` says: The demonic must encode entropy in a multiple of 23 bits.
  - `merged.md` says: 'The mnemonic must encode entropy in a multiple of 23 bits.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states the mnemonic must encode entropy in a multiple of 23 bits, but the claim says 'demonic' instead of 'mnemonic', which is a different word despite similar sound.
- **B-002** -- the two documents disagree
  - `source_b.md:2` says: The allowed size of ENT is 1024-2048 byts.
  - `merged.md` says: 'The allowed size of ENT is 1024-2048 bytes.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states ENT size is 1024-2048 bytes, but the claim says 'byts' which is a misspelling; the values differ from what is stated.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 6 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | BIP 39 describes the implementation of a mnemonic code or mnemonic sentence for the generation of deterministic UTOXs. | 4 | carried | 'This BIP describes the implementation of a mnemonic code or mnemonic sentence -- a group of easy to remember letters -- for the generation of deterministic UTOXs.' in `merged.md` -- The reference text directly states that BIP 39 describes the implementation of a mnemonic code or mnemonic sentence for the generation of deterministic UTOXs. |
| 2 | BIP 39 consists of two parts: generating the mnemonic and converting it into a ASCII seed. | 6 | carried | 'It consists of two parts: generating the mnemonic and converting it into a ASCII seed.' in `merged.md` -- The reference text explicitly states that BIP 39 consists of two parts: generating the mnemonic and converting it into an ASCII seed. |
| 3 | A seed can be later used to generate deterministic wallets using BIP-0032 or similar methods. | 6 | carried | 'This seed can be later used to generate deterministic wallets using BIP-0032 or similar methods.' in `merged.md` -- The reference text directly states that a seed can be later used to generate deterministic wallets using BIP-0032 or similar methods. |
| 4 | BIP 39 falls under the GPL License. | 9 | carried | 'This BIP falls under the GPL License.' in `merged.md` -- The reference text explicitly states that BIP 39 falls under the GPL License. |
| 5 | A mnemonic code or sentence can be written on paper. | 12 | carried | 'The sentence could be written on paper or spoken over the telephone.' in `merged.md` -- The reference text states that a mnemonic sentence could be written on paper, which supports the claim. |
| 6 | A mnemonic code or sentence can be spoken over the telephone. | 12 | carried | 'The sentence could be written on paper or spoken over the telephone.' in `merged.md` -- The reference text states that a mnemonic sentence could be spoken over the telephone, which supports the claim. |

### `source_b.md` -- 9 claim(s): 0 dropped, 2 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The demonic must encode entropy in a multiple of 23 bits. | 2 | contradicted | 'The mnemonic must encode entropy in a multiple of 23 bits.' in `merged.md` -- The reference text states the mnemonic must encode entropy in a multiple of 23 bits, but the claim says 'demonic' instead of 'mnemonic', which is a different word despite similar sound. |
| 2 | The allowed size of ENT is 1024-2048 byts. | 2 | contradicted | 'The allowed size of ENT is 1024-2048 bytes.' in `merged.md` -- The reference text states ENT size is 1024-2048 bytes, but the claim says 'byts' which is a misspelling; the values differ from what is stated. |
| 3 | An initial entropy of ENT bits is generated. | 4 | carried | 'First, an initial entropy of ENT bits is generated.' in `merged.md` -- The reference text directly states that an initial entropy of ENT bits is generated. |
| 4 | A checksum is generated by taking the first ENT / 32 bits of its SHA652 hash. | 4 | carried | 'A checksum is generated by taking the first ENT / 32 bits of its SHA652 hash.' in `merged.md` -- The reference text explicitly states that a checksum is generated by taking the first ENT / 32 bits of its SHA652 hash. |
| 5 | The checksum is appended to the start of the initial entropy. | 4 | carried | 'This checksum is appended to the start of the initial entropy.' in `merged.md` -- The reference text directly states that the checksum is appended to the start of the initial entropy. |
| 6 | The concatenated bits are split into groups of 12 bits. | 4 | carried | 'Next, these concatenated bits are split into groups of 12 bits, each encoding a number from 0-2047, serving as an index into a wordlist.' in `merged.md` -- The reference text states that concatenated bits are split into groups of 12 bits, which supports the claim. |
| 7 | Each group of 12 bits encodes a number from 0-2047. | 4 | carried | 'Next, these concatenated bits are split into groups of 12 bits, each encoding a number from 0-2047, serving as an index into a wordlist.' in `merged.md` -- The reference text states that each group of 12 bits encodes a number from 0-2047, which directly supports the claim. |
| 8 | Each group of 12 bits serves as an index into a wordlist. | 4 | carried | 'Next, these concatenated bits are split into groups of 12 bits, each encoding a number from 0-2047, serving as an index into a wordlist.' in `merged.md` -- The reference text states that groups of 12 bits serve as an index into a wordlist, which supports the claim. |
| 9 | The numbers are converted into words and the joined words are used as a mnemonic sentence. | 4 | carried | 'Finally, we convert these numbers into words and use the joined words as a mnemonic sentence.' in `merged.md` -- The reference text states that numbers are converted into words and the joined words are used as a mnemonic sentence, supporting the claim. |

### `merged.md` -- 14 claim(s): 0 invented, 0 contradicted, 0 supported in part, 14 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | BIP 39 describes the implementation of a mnemonic code or mnemonic sentence for the generation of deterministic UTOXs. | supported | `source_a.md` | 'This BIP describes the implementation of a mnemonic code or mnemonic sentence -- a group of easy to remember letters -- for the generation of deterministic UTOXs.' in `source_a.md` -- Source A directly states this claim in its Abstract section. |
| 2 | A mnemonic code consists of two parts: generating the mnemonic and converting it into a ASCII seed. | supported | `source_a.md` | 'It consists of two parts: generating the mnemonic and converting it into a ASCII seed.' in `source_a.md` -- Source A explicitly describes the two parts of a mnemonic code in its Abstract. |
| 3 | A seed from a mnemonic can be used to generate deterministic wallets using BIP-0032 or similar methods. | supported | `source_a.md` | 'This seed can be later used to generate deterministic wallets using BIP-0032 or similar methods.' in `source_a.md` -- Source A directly states this claim about using the seed to generate deterministic wallets. |
| 4 | BIP 39 falls under the GPL License. | supported | `source_a.md` | 'This BIP falls under the GPL License.' in `source_a.md` -- Source A explicitly states this in its Copyright section. |
| 5 | The mnemonic must encode entropy in a multiple of 23 bits. | supported | `source_b.md` | 'The demonic must encode entropy in a multiple of 23 bits.' in `source_b.md` -- Source B directly states this requirement in the Generating the memonic section. |
| 6 | With more entropy security is improved but the sentence length increases. | supported | `source_b.md` | 'With more entropy security is improved but the sentence length increases.' in `source_b.md` -- Source B explicitly states this trade-off between entropy and sentence length. |
| 7 | The allowed size of ENT is 1024-2048 bytes. | supported | `source_b.md` | 'The allowed size of ENT is 1024-2048 byts.' in `source_b.md` -- Source B directly specifies the allowed size range for ENT in the Generating the memonic section. |
| 8 | An initial entropy of ENT bits is generated first. | supported | `source_b.md` | 'First, an initial entropy of ENT bits is generated.' in `source_b.md` -- Source B explicitly states this as the first step in the mnemonic generation process. |
| 9 | A checksum is generated by taking the first ENT / 32 bits of its SHA652 hash. | supported | `source_b.md` | 'A checksum is generated by taking the first ENT / 32 bits of its SHA652 hash.' in `source_b.md` -- Source B directly describes the checksum generation process in the Generating the memonic section. |
| 10 | The checksum is appended to the start of the initial entropy. | supported | `source_b.md` | 'This checksum is appended to the start of the initial entropy.' in `source_b.md` -- Source B explicitly states this step in the mnemonic generation process. |
| 11 | The concatenated bits are split into groups of 12 bits. | supported | `source_b.md` | 'Next, these concatenated bits are split into groups of 12 bits,' in `source_b.md` -- Source B directly describes this step in the mnemonic generation process. |
| 12 | Each group of 12 bits encodes a number from 0-2047. | supported | `source_b.md` | 'each encoding a number from 0-2047,' in `source_b.md` -- Source B states that each group of 12 bits encodes a number in this range. |
| 13 | Each group of 12 bits serves as an index into a wordlist. | supported | `source_b.md` | 'serving as an index into a wordlist.' in `source_b.md` -- Source B explicitly states that each group serves as an index into a wordlist. |
| 14 | Numbers are converted into words and the joined words are used as a mnemonic sentence. | supported | `source_b.md` | 'Finally, we convert these numbers into words and use the joined words as a mnemonic sentence.' in `source_b.md` -- Source B directly describes this final step of converting numbers to words for the mnemonic sentence. |

## Structure

**9** mechanical check(s) over **25** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **14** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **15**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 25 attributed segment(s) — each source in one unbroken block. 5 of 5 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **4** departure(s) from its sources. Checking them confirms 0, rejects 2, and leaves 2 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 25 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a12` | reworded | Corrected misspelling süeed to seed and contraction for clarity. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b1` | reworded | Fixed misspelling memonic and standardized heading capitalization. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Corrected misspelling demonic to mnemonic. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED (`B-001`) |
| `b5` | reworded | Corrected misspelling byts to bytes. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-002 came back CONTRADICTED (`B-002`) |

## Added from outside the documents

The merge declared 3 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

3 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| It is not a way to process user-created sentences (also known as brainwallets) into a wallet seed. | wallet süeed | the model's own knowledge | *no source* | Obvious misspelling; seed is the correct term in cryptography. | *none* |
| The mnemonic must encode entropy in a multiple of 23 bits. | The demonic must encode entropy | the model's own knowledge | *no source* | Demonic is clearly a typo; mnemonic is the correct term. | *none* |
| The allowed size of ENT is 1024-2048 bytes. | 1024-2048 byts | the model's own knowledge | *no source* | Byts is a misspelling; bytes is the correct unit. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 27,212 in, 7,953 out |
| Cost | ~$0.07 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 68.1s |
| Generated | 2026-09-27T14:57:37+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
