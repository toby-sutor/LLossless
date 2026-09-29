Suppose the documents were:

  <document id="a" filename="marlbrook_handbook.md" base="true">
    a1| Marlbrook Funicular
    a2| The Marlbrook funicular climbs 412 metres.
    a3| The cars run every 20 minutes.
    a4| There is a ticket office at the lower station.
    a5| Open daily.
  </document>

  <document id="b" filename="marlbrook_field_notes.md">
    b1| The Marlbrook Funicular Railway
    b2| The Marlbrook funicular climbs 412 metres.
    b3| The cars run every 15 minutes.
    b4| The lower station has a ticket office, staffed all day.
  </document>

Then merged_document is:

  Marlbrook Funicular

  The Marlbrook funicular climbs 412 metres.

  The cars run every 20 minutes.
  The cars run every 15 minutes.

  The lower station has a ticket office, staffed all day. It is open daily.

decisions has one record: slot "title", candidates "Marlbrook Funicular" from
marlbrook_handbook.md and "The Marlbrook Funicular Railway" from
marlbrook_field_notes.md, chosen "Marlbrook Funicular", because it is the base
document's title.

dispositions has four records:
  a4 superseded, replacement "The lower station has a ticket office, staffed
  all day.", because b4 states the same fact and adds the staffing.
  a5 reworded, replacement "It is open daily.", because a fragment was
  completed into the sentence it was already trying to be.
  b1 superseded, replacement "Marlbrook Funicular", because the base title was
  kept and this one was not.
  b2 duplicate, replacement "The Marlbrook funicular climbs 412 metres.",
  because a2 already states it.

a5 is what this level adds to low. "Open daily." is a bare fragment, and it
becomes a natural sentence rather than being carried over as it stands. Low
could complete a fragment too; what low could not do is rewrite a sentence
that already stands up, and this level can.

a4 is superseded rather than duplicate: b4 states everything a4 states and
adds the staffing, so the wording that says more is the one kept. The
verbatim classes are untouched by any of this: 412 metres, 20 minutes and 15
minutes are copied character for character at every level.

Had a5 instead read "The ticket office is staffed all day." it would be
subsumed rather than reworded, since b4's sentence already carries that
detail and the record would name b4's sentence as its replacement. subsumed
is how a detail merge is declared, and it is the other thing this level adds.

a1, a2 and b4 get no record: each appears in the merge character for
character. a3 and b3 get no record either: the two disagree, so both stay
exactly as their documents wrote them and neither is carried over changed.
