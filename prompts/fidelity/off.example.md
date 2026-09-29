Suppose the documents were:

  <document id="a" filename="marlbrook_handbook.md" base="true">
    a1| Marlbrook Funicular
    a2| The Marlbrook funicular climbs 412 metres.
    a3| The cars run every 20 minutes.
    a4| There is a ticket office at the lower station.
  </document>

  <document id="b" filename="marlbrook_field_notes.md">
    b1| The Marlbrook Funicular Railway
    b2| The Marlbrook funicular climbs 412 metres.
    b3| The cars run every 15 minutes.
    b4| The lower station has a ticket office.
  </document>

Then merged_document is:

  Marlbrook Funicular

  The Marlbrook funicular climbs 412 metres.

  The cars run every 20 minutes.
  The cars run every 15 minutes.

  There is a ticket office at the lower station.

decisions has one record: slot "title", candidates "Marlbrook Funicular" from
marlbrook_handbook.md and "The Marlbrook Funicular Railway" from
marlbrook_field_notes.md, chosen "Marlbrook Funicular", because it is the base
document's title.

dispositions has three records:
  b1 superseded, replacement "Marlbrook Funicular", because the base title was
  kept and this one was not.
  b2 duplicate, replacement "The Marlbrook funicular climbs 412 metres.",
  because a2 already states it.
  b4 superseded, replacement "There is a ticket office at the lower station.",
  because a4 states the same fact and one wording is kept.

b2 and b4 are the two cases this level has to tell apart. b2 is word for word
what a2 says, so it is duplicate. b4 and a4 state one fact in different words,
and neither carries a detail the other lacks, so one wording is kept and the
other is superseded naming it. Carrying both would state that fact twice.

a3 and b3 are the boundary beside them, and the one most easily got wrong.
They give different intervals, 20 minutes against 15, and no reader can
believe both at once, so both are stated with the document each came from and
neither is superseded. Had b3 instead read "There is a car every 20 minutes."
- the same interval in different words - a reader could believe both, so that
would be one fact stated twice and it would be superseded exactly as b4 is.
The test is not whether two sentences differ. It is whether they can both be
true. Only the sentences that cannot are attributed; two wordings of one fact
never are.

a1, a2 and a4 get no record: each appears in the merge character for
character. a3 and b3 get no record either: the two disagree, so both stay
exactly as their documents wrote them and neither is carried over changed.
