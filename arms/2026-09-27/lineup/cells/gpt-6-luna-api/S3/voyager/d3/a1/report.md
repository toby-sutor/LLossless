## Verdict

**57 finding(s).** In the claims: 6 dropped, 1 partially dropped, 34 contradicted, 1 hallucinated, 3 partially invented. In the structure: 12 verbatim violation. 6 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 28 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 20 |
| Forward — source claims accounted for in the merge | **7/32** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **3/12** |
| Forward — `source_b.md` claims accounted for | **4/20** (1 in part) |
| Reverse — merge claims found in a source | **8/28** |
| Reverse — supported only in part | 3 |
| Evidence grounded | **53/53** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **A-001** (`source_a.md:3`) — Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - judged against: `merged.md`
  - rationale: The reference text does not mention Voyager 3 or state that it fulfilled mission goals across three encounters.
- **A-002** (`source_a.md:3`) — Mission planners directed Voyager 3 to Uranus.
  - judged against: `merged.md`
  - rationale: The reference text does not say mission planners directed Voyager 3 to Uranus.
- **A-004** (`source_a.md:5`) — Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - judged against: `merged.md`
  - rationale: The reference attributes the Jupiter encounter optimization to Voyager 2, not Voyager 3, and does not discuss Voyager 3.
- **A-008** (`source_a.md:9`) — Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - judged against: `merged.md`
  - rationale: The reference does not give this date or state that Voyager 1 began short-range observations of Uranus then.
- **B-004** (`source_b.md:3`) — The naming tradition began in 1687.
  - judged against: `merged.md`
  - rationale: The reference does not state when the naming tradition began.
- **B-006** (`source_b.md:3`) — Uranus had eight “older” rings.
  - judged against: `merged.md`
  - rationale: The reference does not state that Uranus had eight older rings.

### Partly dropped — the merge carries some of this claim

- **B-015** (`source_b.md:7`) — Voyager 2 came closest to any object so far in its nearly century-long travels when it flew by Miranda.
  - evidence: 'It passed Miranda at about 29,000 kilometers (18,000 miles), its closest approach to any object in its travels to that point.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The closest-approach claim is stated, but the reference does not say Voyager 2’s travels were nearly a century long.

### Contradicted — the merge states something different

- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter’s geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'Voyager 2’s Uranus trajectory also enabled its later encounter with Neptune.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies Neptune, not Saturn, as the later encounter enabled by the Uranus trajectory.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2 was the first human-made object to fly past Uranus.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies Voyager 2, not Voyager 1, as the first human-made object to fly past Uranus.
- **A-010** -- the two documents disagree
  - `source_a.md:9` says: Light conditions were five-hundred times less than terrestrial conditions.
  - `merged.md` says: 'Sunlight at Uranus is about 1/400 as intense as on Earth.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives about one four-hundredth the intensity, not one five-hundredth.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach took place at 17:59 UT on Jan. 24, 1986,' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives UT and 1986, not ED and 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles).' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim reverses the kilometer and mile values stated in the reference.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby.
  - `merged.md` says: 'During its flyby, Voyager 2 discovered 10 new moons—Cordelia, Ophelia, Bianca, Cressida, Desdemona, Juliet, Portia, Rosalind, Belinda, and Puck—and two new rings.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says Voyager 2 discovered 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The 11 new moons were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'During its flyby, Voyager 2 discovered 10 new moons—Cordelia, Ophelia, Bianca, Cressida, Desdemona, Juliet, Portia, Rosalind, Belinda, and Puck—and two new rings.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed names differ from the names asserted in the claim.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The names listed for the new moons were allusions to Goethe.
  - `merged.md` says: 'The moon names follow a literary naming tradition drawn from Shakespeare and Alexander Pope.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference attributes the naming tradition to Shakespeare and Alexander Pope, not Goethe.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings.
  - `merged.md` says: 'During its flyby, Voyager 2 discovered 10 new moons—Cordelia, Ophelia, Bianca, Cressida, Desdemona, Juliet, Portia, Rosalind, Belinda, and Puck—and two new rings.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says Voyager 2 discovered two new rings, not three.
- **B-007** -- the two documents disagree
  - `source_b.md:3` says: Uranus had a magnetic field tilted at 66 degrees off-axis and off-center.
  - `merged.md` says: 'Uranus’s magnetic field is tilted about 59 degrees from its rotational axis and is offset from the planet’s center.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives a tilt of about 59 degrees, not 66 degrees.
- **B-008** -- the two documents disagree
  - `source_b.md:5` says: Wind speeds in Uranus’ atmosphere reached as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'Wind speeds in Uranus’s atmosphere reach about 900 km/h;' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives about 900 km/h, not 450 km/h.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  - `merged.md` says: 'Voyager 2 found no evidence of a boiling lake of water beneath the clouds.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference explicitly says Voyager 2 found no evidence of a boiling lake.
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Voyager 2 returned images of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s smaller moons.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference lists Ariel, Umbriel, and Titania, not Ariele, Umbrella, and Titan.
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan were five of Uranus’ smaller moons.
  - `merged.md` says: 'Voyager 2 returned images of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s smaller moons.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies five smaller moons but gives different names for three of those claimed.
- **B-014** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers).
  - `merged.md` says: 'It passed Miranda at about 29,000 kilometers (18,000 miles), its closest approach to any object in its travels to that point.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives a different range for the Miranda flyby.
- **B-018** -- the two documents disagree
  - `source_b.md:9` says: News of the Uranus encounter was interrupted the same day by the Challenger accident.
  - `merged.md` says: 'Four days after the Uranus encounter, the Challenger disaster killed seven astronauts during the space shuttle launch on Jan. 28, 1986.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference places the disaster four days after the Uranus encounter, not on the same day.
- **B-019** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'Four days after the Uranus encounter, the Challenger disaster killed seven astronauts during the space shuttle launch on Jan. 28, 1986.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says the disaster killed seven astronauts, not six.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'Four days after the Uranus encounter, the Challenger disaster killed seven astronauts during the space shuttle launch on Jan. 28, 1986.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference dates the disaster to Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 completed its primary mission goals at Jupiter and Saturn.
  - `source_a.md` says: 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes fulfillment of the primary mission goals to Voyager 3, not Voyager 2.
- **M-003** -- the two documents disagree
  - `merged.md:3` says: Voyager 2’s encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The sentence refers back to Voyager 3, whereas the claim attributes the Jupiter encounter to Voyager 2.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: Voyager 1 did not fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987," (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies Voyager 1 as the first human-made object to fly past Uranus.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987," (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2’s signals took approximately 2,5 hours to reach Earth.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987, when signals took approximately 2,5 hours to reach Earth." (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source assigns the signals taking approximately 2,5 hours to Voyager 1, not Voyager 2.
- **M-009** -- the two documents disagree
  - `merged.md:5` says: Voyager 2’s closest approach took place at 17:59 UT on Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles).' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives Jan. 24, 1968, rather than Jan. 24, 1986, and does not attribute the approach to Voyager 2.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: Voyager 2’s closest approach was at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles).' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The claim reverses the source's units and values: it gives 81,500 kilometers instead of 50,640 kilometers.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Sunlight at Uranus is about 1/400 as intense as on Earth.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives light conditions as five-hundred times less than terrestrial conditions, not about 1/400 as intense.
- **M-012** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered 10 new moons—Cordelia, Ophelia, Bianca, Cressida, Desdemona, Juliet, Portia, Rosalind, Belinda, and Puck.
  - `source_b.md` says: 'During its flyby, Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says Voyager 2 discovered 11 new moons, not 10.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered two new rings.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says three new rings were discovered, not two.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: Uranus’s magnetic field is tilted about 59 degrees from its rotational axis.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the tilt as 66 degrees, not about 59 degrees.
- **M-017** -- the two documents disagree
  - `merged.md:7` says: Wind speeds in Uranus’s atmosphere reach about 900 km/h.
  - `source_b.md` says: 'The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives wind speeds as high as 450 km/h, not about 900 km/h.
- **M-018** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 found no evidence of a boiling lake of water beneath the clouds.
  - `source_b.md` says: 'and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says Voyager 2 found evidence of a boiling lake beneath the cloud surface.
- **M-026** -- the two documents disagree
  - `merged.md:11` says: The Challenger disaster occurred four days after the Uranus encounter.
  - `source_b.md` says: 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the accident occurred the same day as the Uranus encounter, not four days later.
- **M-027** -- the two documents disagree
  - `merged.md:11` says: The Challenger disaster killed seven astronauts during the space shuttle launch.
  - `source_b.md` says: 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the accident killed six astronauts, not seven.
- **M-028** -- the two documents disagree
  - `merged.md:11` says: The space shuttle launch during which the Challenger disaster killed seven astronauts took place on Jan. 28, 1986.
  - `source_b.md` says: 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the launch date as Feb. 28, 1986, not Jan. 28, 1986, and says six astronauts were killed.

### Invented — in the merge, in neither source

- **M-004** (`merged.md:3`) — Voyager 2’s Uranus trajectory enabled its later encounter with Neptune.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Neither source states that the Uranus trajectory enabled a later encounter with Neptune.

### Partly invented — the sources carry some of this claim

- **M-002** (`merged.md:3`) — The flight from Saturn to Uranus took about 4,5 years.
  - evidence: 'a journey that would take about 4,5 years.' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source gives the journey to Uranus as about 4,5 years, but does not say it was a flight from Saturn.
- **M-014** (`merged.md:7`) — The moon names follow a literary naming tradition drawn from Shakespeare and Alexander Pope.
  - evidence: 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source supports literary allusions and a naming tradition, but identifies Goethe and does not mention Shakespeare or Alexander Pope.
- **M-021** (`merged.md:9`) — Voyager 2 returned images of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s smaller moons.
  - evidence: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source supports photos of Miranda and Oberon, but lists different names for the other three moons.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (60 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m7` (`merged.md`) - '2,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 4 dropped, 5 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | dropped | The reference text does not mention Voyager 3 or state that it fulfilled mission goals across three encounters. |
| 2 | Mission planners directed Voyager 3 to Uranus. | 3 | dropped | The reference text does not say mission planners directed Voyager 3 to Uranus. |
| 4 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | dropped | The reference attributes the Jupiter encounter optimization to Voyager 2, not Voyager 3, and does not discuss Voyager 3. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | dropped | The reference does not give this date or state that Voyager 1 began short-range observations of Uranus then. |
| 5 | The Uranus encounter’s geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'Voyager 2’s Uranus trajectory also enabled its later encounter with Neptune.' in `merged.md` -- The reference identifies Neptune, not Saturn, as the later encounter enabled by the Uranus trajectory. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2 was the first human-made object to fly past Uranus.' in `merged.md` -- The reference identifies Voyager 2, not Voyager 1, as the first human-made object to fly past Uranus. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | contradicted | 'Sunlight at Uranus is about 1/400 as intense as on Earth.' in `merged.md` -- The reference gives about one four-hundredth the intensity, not one five-hundredth. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach took place at 17:59 UT on Jan. 24, 1986,' in `merged.md` -- The reference gives UT and 1986, not ED and 1968. |
| 12 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles).' in `merged.md` -- The claim reverses the kilometer and mile values stated in the reference. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'the flight from Saturn to Uranus took about 4,5 years' in `merged.md` -- This directly states the approximate duration of the journey to Uranus. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 did not fly past Uranus; it had only 6.4 days of close study during its Saturn flyby.' in `merged.md` -- The reference states Voyager 1 had only 6.4 days of close study during its flyby of Saturn. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'Its signals took approximately 2,5 hours to reach Earth.' in `merged.md` -- The reference gives the same approximate signal travel time. |

### `source_b.md` -- 20 claim(s): 2 dropped, 13 contradicted, 1 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 4 | The naming tradition began in 1687. | 3 | dropped | The reference does not state when the naming tradition began. |
| 6 | Uranus had eight “older” rings. | 3 | dropped | The reference does not state that Uranus had eight older rings. |
| 1 | Voyager 2 discovered 11 new moons during its flyby. | 3 | contradicted | 'During its flyby, Voyager 2 discovered 10 new moons—Cordelia, Ophelia, Bianca, Cressida, Desdemona, Juliet, Portia, Rosalind, Belinda, and Puck—and two new rings.' in `merged.md` -- The reference says Voyager 2 discovered 10 new moons, not 11. |
| 2 | The 11 new moons were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'During its flyby, Voyager 2 discovered 10 new moons—Cordelia, Ophelia, Bianca, Cressida, Desdemona, Juliet, Portia, Rosalind, Belinda, and Puck—and two new rings.' in `merged.md` -- The listed names differ from the names asserted in the claim. |
| 3 | The names listed for the new moons were allusions to Goethe. | 3 | contradicted | 'The moon names follow a literary naming tradition drawn from Shakespeare and Alexander Pope.' in `merged.md` -- The reference attributes the naming tradition to Shakespeare and Alexander Pope, not Goethe. |
| 5 | Voyager 2 discovered three new rings. | 3 | contradicted | 'During its flyby, Voyager 2 discovered 10 new moons—Cordelia, Ophelia, Bianca, Cressida, Desdemona, Juliet, Portia, Rosalind, Belinda, and Puck—and two new rings.' in `merged.md` -- The reference says Voyager 2 discovered two new rings, not three. |
| 7 | Uranus had a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | contradicted | 'Uranus’s magnetic field is tilted about 59 degrees from its rotational axis and is offset from the planet’s center.' in `merged.md` -- The reference gives a tilt of about 59 degrees, not 66 degrees. |
| 8 | Wind speeds in Uranus’ atmosphere reached as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'Wind speeds in Uranus’s atmosphere reach about 900 km/h;' in `merged.md` -- The reference gives about 900 km/h, not 450 km/h. |
| 9 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | contradicted | 'Voyager 2 found no evidence of a boiling lake of water beneath the clouds.' in `merged.md` -- The reference explicitly says Voyager 2 found no evidence of a boiling lake. |
| 12 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Voyager 2 returned images of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s smaller moons.' in `merged.md` -- The reference lists Ariel, Umbriel, and Titania, not Ariele, Umbrella, and Titan. |
| 13 | Miranda, Oberon, Ariele, Umbrella, and Titan were five of Uranus’ smaller moons. | 7 | contradicted | 'Voyager 2 returned images of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s smaller moons.' in `merged.md` -- The reference identifies five smaller moons but gives different names for three of those claimed. |
| 14 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | contradicted | 'It passed Miranda at about 29,000 kilometers (18,000 miles), its closest approach to any object in its travels to that point.' in `merged.md` -- The reference gives a different range for the Miranda flyby. |
| 18 | News of the Uranus encounter was interrupted the same day by the Challenger accident. | 9 | contradicted | 'Four days after the Uranus encounter, the Challenger disaster killed seven astronauts during the space shuttle launch on Jan. 28, 1986.' in `merged.md` -- The reference places the disaster four days after the Uranus encounter, not on the same day. |
| 19 | The Challenger accident killed six astronauts. | 9 | contradicted | 'Four days after the Uranus encounter, the Challenger disaster killed seven astronauts during the space shuttle launch on Jan. 28, 1986.' in `merged.md` -- The reference says the disaster killed seven astronauts, not six. |
| 20 | The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'Four days after the Uranus encounter, the Challenger disaster killed seven astronauts during the space shuttle launch on Jan. 28, 1986.' in `merged.md` -- The reference dates the disaster to Jan. 28, 1986, not Feb. 28, 1986. |
| 15 | Voyager 2 came closest to any object so far in its nearly century-long travels when it flew by Miranda. | 7 | carried in part | 'It passed Miranda at about 29,000 kilometers (18,000 miles), its closest approach to any object in its travels to that point.' in `merged.md` -- The closest-approach claim is stated, but the reference does not say Voyager 2’s travels were nearly a century long. |
| 10 | Uranus’ rings were extremely variable in thickness. | 5 | carried | 'The rings vary greatly in thickness and transparency.' in `merged.md` -- The reference states that the rings vary greatly in thickness. |
| 11 | Uranus’ rings were extremely variable in transparency. | 5 | carried | 'The rings vary greatly in thickness and transparency.' in `merged.md` -- The reference states that the rings vary greatly in transparency. |
| 16 | Images of Miranda showed features on its surface. | 7 | carried | 'Images showed a surface marked by a seemingly irregular mix of unusual features.' in `merged.md` -- The reference explicitly says Miranda’s images showed surface features. |
| 17 | Uranus appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- The reference states that Uranus appeared generally featureless. |

### `merged.md` -- 28 claim(s): 1 invented, 16 contradicted, 3 supported in part, 8 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 4 | Voyager 2’s Uranus trajectory enabled its later encounter with Neptune. | invented | -- | Neither source states that the Uranus trajectory enabled a later encounter with Neptune. |
| 1 | Voyager 2 completed its primary mission goals at Jupiter and Saturn. | contradicted | `source_a.md` | 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source attributes fulfillment of the primary mission goals to Voyager 3, not Voyager 2. |
| 3 | Voyager 2’s encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- The sentence refers back to Voyager 3, whereas the claim attributes the Jupiter encounter to Voyager 2. |
| 5 | Voyager 1 did not fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987," in `source_a.md` -- The source identifies Voyager 1 as the first human-made object to fly past Uranus. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987," in `source_a.md` -- The source names Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus. |
| 8 | Voyager 2’s signals took approximately 2,5 hours to reach Earth. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987, when signals took approximately 2,5 hours to reach Earth." in `source_a.md` -- The source assigns the signals taking approximately 2,5 hours to Voyager 1, not Voyager 2. |
| 9 | Voyager 2’s closest approach took place at 17:59 UT on Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles).' in `source_a.md` -- The source gives Jan. 24, 1968, rather than Jan. 24, 1986, and does not attribute the approach to Voyager 2. |
| 10 | Voyager 2’s closest approach was at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles).' in `source_a.md` -- The claim reverses the source's units and values: it gives 81,500 kilometers instead of 50,640 kilometers. |
| 11 | Sunlight at Uranus is about 1/400 as intense as on Earth. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- The source gives light conditions as five-hundred times less than terrestrial conditions, not about 1/400 as intense. |
| 12 | During its flyby, Voyager 2 discovered 10 new moons—Cordelia, Ophelia, Bianca, Cressida, Desdemona, Juliet, Portia, Rosalind, Belinda, and Puck. | contradicted | `source_b.md` | 'During its flyby, Voyager 2 discovered 11 new moons' in `source_b.md` -- The source says Voyager 2 discovered 11 new moons, not 10. |
| 13 | During its flyby, Voyager 2 discovered two new rings. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source says three new rings were discovered, not two. |
| 15 | Uranus’s magnetic field is tilted about 59 degrees from its rotational axis. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center.' in `source_b.md` -- The source gives the tilt as 66 degrees, not about 59 degrees. |
| 17 | Wind speeds in Uranus’s atmosphere reach about 900 km/h. | contradicted | `source_b.md` | 'The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives wind speeds as high as 450 km/h, not about 900 km/h. |
| 18 | Voyager 2 found no evidence of a boiling lake of water beneath the clouds. | contradicted | `source_b.md` | 'and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.' in `source_b.md` -- The source says Voyager 2 found evidence of a boiling lake beneath the cloud surface. |
| 26 | The Challenger disaster occurred four days after the Uranus encounter. | contradicted | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source says the accident occurred the same day as the Uranus encounter, not four days later. |
| 27 | The Challenger disaster killed seven astronauts during the space shuttle launch. | contradicted | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source says the accident killed six astronauts, not seven. |
| 28 | The space shuttle launch during which the Challenger disaster killed seven astronauts took place on Jan. 28, 1986. | contradicted | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source gives the launch date as Feb. 28, 1986, not Jan. 28, 1986, and says six astronauts were killed. |
| 2 | The flight from Saturn to Uranus took about 4,5 years. | supported in part | `source_a.md` | 'a journey that would take about 4,5 years.' in `source_a.md` -- The source gives the journey to Uranus as about 4,5 years, but does not say it was a flight from Saturn. |
| 14 | The moon names follow a literary naming tradition drawn from Shakespeare and Alexander Pope. | supported in part | `source_b.md` | 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' in `source_b.md` -- The source supports literary allusions and a naming tradition, but identifies Goethe and does not mention Shakespeare or Alexander Pope. |
| 21 | Voyager 2 returned images of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s smaller moons. | supported in part | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source supports photos of Miranda and Oberon, but lists different names for the other three moons. |
| 6 | Voyager 1 had only 6.4 days of close study during its Saturn flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- The source states Voyager 1 had only 6.4 days of close study in the flyby context of its possible Saturn encounter. |
| 16 | Uranus’s magnetic field is offset from the planet’s center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center.' in `source_b.md` -- The source states that the magnetic field was off-center. |
| 19 | The rings vary greatly in thickness. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states that the rings varied extremely in thickness. |
| 20 | The rings vary greatly in transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states that the rings varied extremely in transparency. |
| 22 | Voyager 2 passed Miranda at about 29,000 kilometers (18,000 miles). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers),' in `source_b.md` -- The source's 17.560 miles and 28.260 kilometers support the claim's rounded approximate distances. |
| 23 | Voyager 2’s pass by Miranda was its closest approach to any object in its travels to that point. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels.' in `source_b.md` -- The source says the Miranda flyby was the closest approach to any object in the spacecraft's travels up to then. |
| 24 | Images showed Miranda’s surface marked by a seemingly irregular mix of unusual features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.' in `source_b.md` -- The source describes Miranda's surface as a seemingly irregular mix of peculiar features. |
| 25 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- The source directly states that Uranus appeared generally featureless. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **28** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **32**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 6 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '66' (degrees) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '450' (km/h) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '479' (miles) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '17.560' (miles) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '28.260' (kilometers) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **14** departure(s) from its sources. Checking them confirms 10, rejects 4, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | The opening paragraph corrects the craft and clarifies the journey. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back MISSING, A-002 came back MISSING (`A-001`, `A-002`) |
| `a3` | reworded | The Jupiter-planning fact is retained in the opening paragraph. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-004 came back MISSING (`A-004`) |
| `a4` | superseded | The Uranus trajectory is corrected; the study duration is placed at Saturn. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-005`, `A-006`) |
| `a5` | superseded | The spacecraft and encounter timing are corrected. | **rejected** | declared 'superseded', which predicts SUPPORTED or CONTRADICTED or PARTIAL; A-008 came back MISSING (`A-008`) |
| `a6` | superseded | The light-level statement is corrected. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-010`) |
| `a7` | superseded | The date, time standard, and distance units are corrected. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-011`, `A-012`) |
| `b2` | superseded | The discoveries, names, literary tradition, and field description are corrected. | **rejected** | declared 'superseded', which predicts SUPPORTED or CONTRADICTED or PARTIAL; B-004 came back MISSING, B-006 came back MISSING (`B-004`, `B-006`) |
| `b3` | superseded | The wind-speed and boiling-lake claims are corrected. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-008`, `B-009`) |
| `b4` | reworded | The ring-variation fact is restated clearly. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |
| `b5` | superseded | The five moon names are corrected and retained. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-012`, `B-013`) |
| `b6` | superseded | The range and travel-duration claim are corrected. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-014`, `B-015`) |
| `b7` | reworded | The description of Miranda’s unusual surface is retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-016`) |
| `b8` | reworded | The description of Uranus is retained. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-017`) |
| `b9` | superseded | The timing, date, and death toll are corrected. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`B-018`, `B-019`, `B-020`) |

## Added from outside the documents

The merge declared 13 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

13 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| After Voyager 2 completed its primary mission goals at Jupiter and Saturn, the flight from Saturn to Uranus took about 4,5 years. | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters | the model's own knowledge | *no source* | Voyager 2 continued from Saturn to Uranus after its primary mission. | *none* |
| Voyager 2’s Uranus trajectory also enabled its later encounter with Neptune. | The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn | the model's own knowledge | *no source* | Voyager 2 continued from Uranus to Neptune, not back to Saturn. | *none* |
| Voyager 1 did not fly past Uranus; it had only 6.4 days of close study during its Saturn flyby. | Voyager 1's short-range observations of the planet | the model's own knowledge | *no source* | Voyager 1 flew past Saturn, while Voyager 2 visited Uranus. | *none* |
| Voyager 2 was the first human-made object to fly past Uranus. | Voyager 1's short-range observations of the planet | the model's own knowledge | *no source* | Voyager 2 made the Uranus flyby. | *none* |
| Closest approach took place at 17:59 UT on Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | The Uranus encounter occurred in 1986 at the stated corrected range. | *none* |
| Sunlight at Uranus is about 1/400 as intense as on Earth. | Light conditions were five-hundred times less than terrestrial conditions. | the model's own knowledge | *no source* | Uranus receives roughly one four-hundredth of Earth's sunlight. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons—Cordelia, Ophelia, Bianca, Cressida, Desdemona, Juliet, Portia, Rosalind, Belinda, and Puck—and two new rings. | 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings | the model's own knowledge | *no source* | Voyager 2's discoveries and the moon names differ from the source claim. | *none* |
| The moon names follow a literary naming tradition drawn from Shakespeare and Alexander Pope. | obvious allusions to Goethe, continuing a naming tradition begun in 1687 | the model's own knowledge | *no source* | Uranian moon names draw on Shakespeare and Pope. | *none* |
| Uranus’s magnetic field is tilted about 59 degrees from its rotational axis and is offset from the planet’s center. | a magnetic field tilted at 66 degrees off-axis and off-center | the model's own knowledge | *no source* | Voyager 2 measured a field tilt of about 59 degrees. | *none* |
| Wind speeds in Uranus’s atmosphere reach about 900 km/h; Voyager 2 found no evidence of a boiling lake of water beneath the clouds. | wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface | the model's own knowledge | *no source* | The wind figure is incorrect, and Voyager did not find a boiling lake. | *none* |
| Voyager 2 returned images of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s smaller moons. | Miranda, Oberon, Ariele, Umbrella, and Titan | the model's own knowledge | *no source* | The listed moon names are Ariel, Umbriel, and Titania. | *none* |
| It passed Miranda at about 29,000 kilometers (18,000 miles), its closest approach to any object in its travels to that point. | a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels | the model's own knowledge | *no source* | The reported range and century-long duration are inaccurate. | *none* |
| Four days after the Uranus encounter, the Challenger disaster killed seven astronauts during the space shuttle launch on Jan. 28, 1986. | the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | The launch occurred on Jan. 28 and killed seven crew members. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-luna |
| Model (decompose) | gpt-6-luna |
| Model (verify) | gpt-6-luna |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 9 live, 0 cached, 0 replayed |
| Tokens | 24,509 in, 28,015 out, 8,640 cached, 16,397 reasoning |
| Cost | ~$0.02 estimated (rates read 2026-09-25) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 203.7s |
| Generated | 2026-09-27T17:56:37+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
