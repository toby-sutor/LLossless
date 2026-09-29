Suppose the documents were:

  <document id="a" filename="marlbrook_handbook.md" base="true">
    a1| Marlbrook Funicular
    a2| The Marlbrook funicular climbs 412 metres.
    a3| The funicular opens on 7 April.
    a4| There is a ticket offise at the lower station.
    a5| The climb takes 8–11 minutes.
    a6| The climb of 412 metres is a little over 1,800 feet.
    a7| Best wishes, the Marlbrook staff
  </document>

  <document id="b" filename="marlbrook_field_notes.md">
    b1| The Marlbrook Funicular Railway
    b2| The Marlbrook funicular climbs 412 metres.
    b3| The first cars run at 09:00.
    b4| The lower station has a ticket office.
    b5| The climb takes 9–13 minutes.
    b6| The timetable data is released under the MIT licence, which forbids
        commercial reuse.
    b7| With best regards, the Marlbrook staff
  </document>

Then merged_document is:

  Marlbrook Funicular

  The Marlbrook funicular climbs 412 metres and opens on 7 April, with the
  first cars running at 09:00. The climb of 412 metres is a little over 1,350
  feet.

  There is a ticket office at the lower station. The climb takes 8–13
  minutes.

  The timetable data is released under the MIT licence, which permits
  commercial reuse.

  Best wishes, the Marlbrook staff

decisions has two records. The first: slot "title", candidates "Marlbrook
Funicular" from marlbrook_handbook.md and "The Marlbrook Funicular Railway"
from marlbrook_field_notes.md, chosen "Marlbrook Funicular", because it is the
base document's title.

The second: slot "climb duration", candidates "8–11 minutes" from
marlbrook_handbook.md and "9–13 minutes" from marlbrook_field_notes.md,
chosen "8–13 minutes", because carrying either range alone would tell a
reader the other document was wrong.

dispositions has ten records:
  a3 reconciled, replacement "The Marlbrook funicular climbs 412 metres and
  opens on 7 April, with the first cars running at 09:00.", because the date
  and the time are one opening.
  b3 reconciled, replacement "The Marlbrook funicular climbs 412 metres and
  opens on 7 April, with the first cars running at 09:00.", because the date
  and the time are one opening.
  a4 reworded, replacement "There is a ticket office at the lower station.",
  because offise is a misspelling.
  b1 superseded, replacement "Marlbrook Funicular", because the base title was
  kept and this one was not.
  b4 superseded, replacement "There is a ticket office at the lower station.",
  because a4 states the same fact and one wording is kept.
  a5 reconciled, replacement "The climb takes 8–13 minutes.", because the
  two ranges give different edges for one figure.
  b5 reconciled, replacement "The climb takes 8–13 minutes.", because the
  two ranges give different edges for one figure.
  a6 reworded, replacement "The climb of 412 metres is a little over 1,350
  feet.", because 412 metres is 1,352 feet and not 1,800.
  b6 reworded, replacement "The timetable data is released under the MIT
  licence, which permits commercial reuse.", because the licence text was read
  and places no such restriction.
  b7 superseded, replacement "Best wishes, the Marlbrook staff", because the
  two closings are one closing and this one was not kept.

additions has two records, one for each correction above.

  statement "The climb of 412 metres is a little over 1,350 feet.", corrects
  "a little over 1,800 feet", basis own-knowledge, source empty, reason
  "412 metres is 1,352 feet".

  statement "The timetable data is released under the MIT licence, which
  permits commercial reuse.", corrects "which forbids commercial reuse",
  basis citation, source "the OSI-approved MIT licence text, read during this
  merge", reason "the retrieved licence text restricts commercial use nowhere".

a6 and b6 are the pair this level is for, and the difference between them is
the whole point. Both are corrections and both are declared, exactly as at
open. What separates them is what was done before the correction was written.

b6 is what `sourced` asks for. The documents disagree with nothing here -- they
agree with each other -- and one of them is wrong about the world. The licence
is named, a named licence has a canonical published text, so that text was
fetched and read before b6 was rewritten, and `source` says what was read. Had
it not been reachable, the honest record would have been own-knowledge with an
empty source: a level that expects retrieval does not turn a failure to
retrieve into a citation.

a6 is what retrieval cannot help with. 1,352 feet is arithmetic; there is no
page to fetch and nothing a fetch would settle, so the basis is own-knowledge
and source is empty. That is a complete answer here as it is at open, and
reaching for a citation because this level's name suggests one would be worse
than the honest record.

Note what a6 is allowed to do that a5 is not. 1,350 is a figure no document
states, and it reaches the merged document only because it is declared as an
addition. A covering value is not declared that way and may not introduce a
figure: that bound is on covering, not on the level, and the two licences are
separate. A figure you retrieve is an addition too, never a covering value.

a3 and b3 are joint support, which this level keeps from open. A date in one
document and a time of day in the other are one opening, and the sentence that
carries both is a sentence neither document makes on its own. It is permitted
since a reader holding both documents could not accept them and reject it.
Every segment that fed the combined statement gets its own reconciled record
naming that statement, which is what makes the combination checkable rather
than merely plausible. a2 is not reconciled: its own sentence survives inside
the combined one unchanged, so it is carried and needs no record.

a5 and b5 are the covering value. The two ranges are not a disagreement about
where the figure lies -- they overlap -- but about its edges, and choosing
either alone tells a reader the other document was wrong. 8–13 carries what
both documents support. Every number in it is a number a document wrote: 8 from
the handbook and 13 from the field notes. Do not round to 10–15, do not split
the difference at 9–12, and do not widen to 5–15 for comfort. Do not look up
the real timetable and put its figure here either: a retrieved figure is an
addition with a declaration behind it, and a covering value has no room for
one.

Both segments get a reconciled record, as with a3 and b3, and the decision
record names the slot as well. The two declarations answer different
questions: the dispositions say what happened to each source segment, and the
decision says what was carried and why.

b7 shows the other thing this level is for. Two closings are one closing said
twice, so the merge states it once. Lower levels reach the same answer through
superseded; what differs here is that the surrounding prose may be rewritten
freely around it.

A correction is still reported, and declaring it does not make it clean, and
neither does having checked it. The merged document now says something a source
denies, and nothing in this tool can tell a correction from a corruption -- so
1,800 not surviving into the merge is reported, and so is the corrected
sentence when it is checked back against the sources. LLossless did not fetch
anything, cannot see that you did, and will not verify what you write in
`source`. What the declaration buys is that a reader sees the statement, what
it replaced, and what you are going on, instead of meeting an unexplained
change.

The verbatim classes do not move for anything else: 412 metres, 7 April and
09:00 are copied character for character here exactly as at off. 8 and 13 are
copied too -- a covering value is assembled from the documents' own figures,
never computed from them and never looked up. A date
combined with a time is a sentence this level wrote; the date and the time
themselves are not rewritten, rounded or reformatted. The one case where a
document's own figure does not survive is a6: a declared correction of a
figure that is wrong, which is a departure you own rather than one the
verbatim rule permits.

a1 and a7 get no record: each appears in the merge character for character.

Before you write your own answer: use WebSearch or WebFetch to check each
fact you are about to correct or add, then write the JSON. Answering without
looking anything up is not what this level asks for.
