Suppose the documents were:

  <document id="a" filename="marlbrook_handbook.md" base="true">
    a1| Marlbrook Funicular
    a2| The Marlbrook funicular climbs 412 metres.
    a3| The funicular opens on 7 April.
    a4| There is a ticket offise at the lower station.
    a5| Best wishes, the Marlbrook staff
  </document>

  <document id="b" filename="marlbrook_field_notes.md">
    b1| The Marlbrook Funicular Railway
    b2| The Marlbrook funicular climbs 412 metres.
    b3| The first cars run at 09:00.
    b4| The lower station has a ticket office.
    b5| With best regards, the Marlbrook staff
  </document>

Then merged_document is:

  Marlbrook Funicular

  The Marlbrook funicular climbs 412 metres and opens on 7 April, with the
  first cars running at 09:00.

  There is a ticket office at the lower station.

  Best wishes, the Marlbrook staff

decisions has one record: slot "title", candidates "Marlbrook Funicular" from
marlbrook_handbook.md and "The Marlbrook Funicular Railway" from
marlbrook_field_notes.md, chosen "Marlbrook Funicular", because it is the base
document's title.

dispositions has six records:
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
  b5 superseded, replacement "Best wishes, the Marlbrook staff", because the
  two closings are one closing and this one was not kept.

a3 and b3 are what this level adds and nothing below it may do. A date in one
document and a time of day in the other are one opening, and the sentence that
carries both is a sentence neither document makes on its own. It is permitted
here since a reader holding both documents could not accept them and reject
it. Every segment that fed the combined statement gets its own reconciled
record naming that statement, which is what makes the combination checkable
rather than merely plausible. a2 is not reconciled: its own sentence survives
inside the combined one unchanged, so it is carried and needs no record.

b5 shows the other thing this level is for. Two closings are one closing said
twice, so the merge states it once. Lower levels reach the same answer through
superseded; what differs here is that the surrounding prose may be rewritten
freely around it.

The verbatim classes do not move for any of this: 412 metres, 7 April and
09:00 are copied character for character here exactly as at off. A date
combined with a time is a sentence this level wrote; the date and the time
themselves are not rewritten, rounded or reformatted.

a1 and a5 get no record: each appears in the merge character for character.
