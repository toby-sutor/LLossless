Fidelity level: open. Everything high permits, plus a covering value where
the documents disagree, and a statement of your own where you are certain.

Write the merged document as a professional editor would. Rewrite prose as
freely as clarity requires. Restructure sentences and
paragraphs, combine statements that repeat one another, and fix everything a
careful copy-editor would fix. None of this reaches the verbatim classes: they
are copied character for character here exactly as at every other level.

Write generally rather than narrating one occasion. Do not write "in this
case", "the reported scenario", "the user wanted" or any equivalent framing;
describe the behaviour, the cause and the fix as they apply to anyone who meets
them. Use the present tense throughout, except for something that only makes
sense as a past event.

Where several documents make the same point in different words, make it once
rather than stating each version in turn.

All five dispositions are permitted, and subsumed is expected here: a statement
that survives inside a broader sentence is subsumed, and its replacement is the
sentence that now carries it. reconciled is permitted here and at high, and
nowhere below. Only dropped remains a defect.

Every compression is a disposition you must declare. A passage that quietly
disappears into "and so on" is a dropped segment however well the surrounding
prose reads.

Complementary facts may be combined. Where two documents each state part of
one picture, you may write the statement that carries both, even though
neither document states it on its own: a date in one and a time of day in the
other become one appointment, a general instruction and the specific case that
narrows it become one instruction. This is the freedom this level adds, and it
is bounded at both ends. The combined statement must be supported by the
documents taken together, so that a reader holding both could not accept them
and reject it.

This level, alone, lets you state something the documents do not. Use it where
a document is wrong about a fact you are certain of, or where both are thin on
something a reader needs, and **declare every such statement in `additions`**,
naming what it corrects and why you are confident. A statement you add and do
not declare is an invention by every test this tool has, and is reported as
one.

Be sparing, and be certain. Nothing here is checked against anything: the
documents are the only thing this tool can verify against, so a declared
addition is carried on your word alone and the report says so. Add what a
reader would be worse off not knowing, and nothing else. Where you are not
sure, say nothing -- a merge that omits a fact is a merge somebody can fix,
and one that states a wrong fact confidently is not.

Check the documents against what you know, and correct what is wrong. Two
documents can agree with each other and both be wrong about the world: a
licence named incorrectly, a standard attributed to the wrong body, a figure
that was right once and has since changed. Where you are certain a document is
wrong, write the correct statement into the merged document, quote the words
you are correcting in `corrects`, and give that segment its own disposition
record as well. The two declarations answer different questions: the
disposition says what happened to the source segment, and the addition says
what you are now asserting instead and what you are going on.

Where you are not certain, carry what the documents say. This is a merge, not
a review, and a document that is merely surprising is a document you leave
alone.

An addition record has five fields.

- statement: the sentence you are now asserting, copied from your merged
  document.
- corrects: the words you are correcting, quoted from the document that
  carries them. Empty where you are correcting nothing -- an addition that
  fills a gap the documents leave open corrects no one, and naming a victim
  it does not have would be inventing one.
- basis: what the statement rests on. Exactly one of:
  - citation - you can name something a reader could go and look at.
  - own-knowledge - you are going on what you know, and there is nothing
    to look at.
- source: under citation, the source itself -- a specification and section, a
  title and date, a named licence text. Under own-knowledge, empty. A URL is
  not required and is usually not the best answer: a name a reader can search
  for is a citation, and it cannot be half-remembered into something that
  looks right and resolves nowhere.
- reason: one sentence, maximum 80 characters, saying why you are confident.

**`own-knowledge` is a complete answer and it is the expected one.** Most of
what you know you know without holding a reference for it, and saying so
plainly is what this field is for. Do not reach for `citation` because the
field looks like it wants one. A source you are not certain exists, or a URL
you have assembled from what such a URL usually looks like, is worse than no
source at all: it turns a statement a reader would have weighed into one they
think they can check, and this tool cannot check it for them.

**Name a source only where you can name a real one.** If you looked it up
while merging, cite what you found. If you are recalling it, that is
`own-knowledge`, whatever confidence you have in the recollection.

Nothing in this tool fetches, resolves or verifies anything you write in
`source`. It makes no network request of any kind. A citation here is
recorded and shown to the reader exactly as you wrote it, and it is the
reader who decides whether to go and look.

Every combination is declared, and that is what makes it checkable rather
than merely plausible. Emit one reconciled record for each segment that fed
the combined statement, each naming that statement as its replacement. A
combination you did not declare is indistinguishable from a fact you made up,
and it is read as one.

The freedom you have been given at this level is freedom over content the
documents jointly support, never over content neither supports.

Where the documents disagree, you may choose, and you may instead carry a
value that covers both. Emit a decision record either way, naming the slot,
both candidates with the document each came from, what you carried, and why.
A value carried with no decision record behind it is indistinguishable from a
value the merge lost the other half of.

Covering is the freedom this level adds over high, and it is for the case
where choosing would assert something a document denies. Two documents giving
a range as 30-45% and 35-50% do not disagree about whether the figure is in
that region; they disagree about its edges, and carrying either one alone
tells a reader the other document was wrong. Carrying 30-50% tells them what
both documents support.

A covering value is bounded by what the documents wrote. Every number in it
must be a number one of them states: you may take the lowest floor and the
highest ceiling the documents offer, and you may not round, widen for comfort,
or introduce a figure neither wrote. A covering value with a number no
document states is an invention, and it is read as one.

Cover only what is genuinely one attribute measured two ways. Values that
cannot both be true of the same thing -- a port that is 8443 in one document
and 9443 in the other -- are a disagreement about fact rather than about
edges, and those you choose between as high does.
