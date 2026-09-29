Suppose the documents were:

  <document id="a" filename="marlbrook_handbook.md" base="true">
    a1| Marlbrook Funicular
    a2| The Marlbrook funicular climbs 412 metres.
    a3| The cars run every 20 minutes.
    a4| There is a ticket offise at the lower station.
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

dispositions has four records:
  a4 reworded, replacement "There is a ticket office at the lower station.",
  because offise is a misspelling and nothing else changed.
  b1 superseded, replacement "Marlbrook Funicular", because the base title was
  kept and this one was not.
  b2 duplicate, replacement "The Marlbrook funicular climbs 412 metres.",
  because a2 already states it.
  b4 superseded, replacement "There is a ticket office at the lower station.",
  because a4 states the same fact and one wording is kept.

a4 is the whole of what this level adds to off. One misspelt word is corrected
and the sentence is otherwise the same sentence: the same clause order, the
same number of sentences, the same words. That is a reworded record, and a
mechanical correction is the only kind of reworded this level licenses.

Correcting a4 does not change which wording survives. b4 says what a4 says in
different words, a4 is the one in the merge, so b4 is superseded by it exactly
as it would have been had a4 been spelt correctly to begin with.

a1 and a2 get no record: each appears in the merge character for character.
a3 and b3 get no record either: the two disagree, so both stay
exactly as their documents wrote them and neither is carried over changed.
