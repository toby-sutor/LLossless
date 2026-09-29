Extract every independently checkable factual assertion from the document below.

The document is shown one line per line, each prefixed with its line number and
a pipe. The prefix is not part of the text.

Rules:
- One assertion per claim. Split compound sentences.
- A single line may contain several sentences, and may therefore yield several
  claims. Do not treat one line as one claim.
- Each claim must stand alone without needing surrounding context.
- Resolve pronouns and references to explicit nouns.
- Copy values, names, numbers, units and time formats exactly as written. Do not
  normalise, round, expand or abbreviate them. "approximately 500" stays
  "approximately 500"; "07:15 till 19:45" stays "07:15 till 19:45".
- Skip headings, formatting, boilerplate and statements of opinion.
- Skip statements about the documents themselves or about how they were
  combined, such as a note that two sources disagree. Attributed content is not
  such a statement: "the guide states that the timeout is 30 seconds" is a
  claim about the timeout, and must be extracted.
- Do not infer, summarise, or combine information.
- line: the number shown against the line the claim comes from. If the claim
  spans several lines, give the first.
- span: the specific sentence the claim comes from, copied exactly, without the
  number prefix. If one line contains several sentences, each claim takes only
  its own sentence as span, never the whole line. The span must appear in the
  document character for character, including any spelling, grammatical or
  formatting errors and any unusual capitalisation. Do not correct anything.

Worked example - one line, two claims.

  12| The kiln fired for eleven hours and the glaze cracked in three places.

This line yields two claims:

  claim: "The kiln fired for eleven hours."
  line: 12
  span: "The kiln fired for eleven hours"

  claim: "The glaze cracked in three places."
  line: 12
  span: "the glaze cracked in three places"

Both claims carry line 12. Neither span is the whole line.

Worked example - fact and opinion in one sentence.

  7| The garden was breathtaking, with eleven rose beds along the south wall.

"The garden was breathtaking" is an evaluation and is skipped. "The garden has
eleven rose beds along the south wall." is checkable and is extracted, with
span "with eleven rose beds along the south wall".

Descriptive prose is not automatically opinion. A stated quantity, position,
duration, time, name, sequence or event is a fact even in a narrative passage,
and must be extracted. Only judgements of quality, beauty, value or feeling are
opinion.

Return JSON matching the provided schema. Nothing else.

DOCUMENT:
{document}
