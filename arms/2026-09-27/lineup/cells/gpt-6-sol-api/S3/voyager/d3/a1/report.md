## Verdict

**66 finding(s).** In the claims: 2 dropped, 1 partially dropped, 48 contradicted, 2 hallucinated, 1 partially invented. In the structure: 12 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 46 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 22 |
| Forward — source claims accounted for in the merge | **11/34** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **3/12** |
| Forward — `source_b.md` claims accounted for | **8/22** (1 in part) |
| Reverse — merge claims found in a source | **15/46** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **76/76** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **A-001** (`source_a.md:3`) — Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - judged against: `merged.md`
  - rationale: The text does not discuss Voyager 3 or the fulfillment of primary mission goals.
- **B-016** (`source_b.md:7`) — Voyager 2 had been traveling for nearly a century when it flew by Miranda.
  - judged against: `merged.md`
  - rationale: The reference does not state how long Voyager 2 had been traveling when it flew by Miranda.

### Partly dropped — the merge carries some of this claim

- **B-003** (`source_b.md:3`) — The naming tradition for the moons began in 1687.
  - evidence: 'their names continue the tradition of drawing on Shakespeare' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text mentions a naming tradition but does not say when it began.

### Contradicted — the merge states something different

- **A-002** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'After encounters with Jupiter and Saturn, Voyager 2 continues to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The spacecraft continuing to Uranus is Voyager 2, not Voyager 3.
- **A-003** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3's journey to Uranus would take about 4,5 years.
  - `merged.md` says: 'Voyager 2 continues to Uranus, a journey of about 4,5 years from Saturn' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated journey belongs to Voyager 2, not Voyager 3.
- **A-004** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'Its encounter with Jupiter is optimized in part to keep future planetary flybys possible.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The preceding sentence identifies the spacecraft as Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Ur anus encounter’s geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The geometry of the Uranus encounter preserves the possibility of a future encounter with Neptune.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The possible future encounter is with Neptune, not Saturn.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2 is the first human-made object to fly past Uranus.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text names Voyager 2, not Voyager 1, as the first.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: 'Its short-range observations take place during the Jan. 24, 1986 flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text identifies Voyager 2 and gives a different date for its short-range observations.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach occurs at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated time designation and year differ from the claim.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim reverses the units assigned to the two figures.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby.
  - `merged.md` says: 'During its flyby, Voyager 2 discovers 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The new moons discovered by Voyager 2 were given names such as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Several names in the claim differ from the names listed in the text.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings during its flyby.
  - `merged.md` says: 'It also discovers two new rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says two new rings, not three.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Uranus had eight “older” rings.
  - `merged.md` says: 'the nine previously known rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives nine previously known rings, not eight.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis.
  - `merged.md` says: 'a magnetic field tilted at 59 degrees to the planet’s rotation axis' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated tilt is 59 degrees, not 66 degrees.
- **B-008** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'The spacecraft finds atmospheric winds reaching 450 mph (724 km/h)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim assigns different units and values to the wind speed.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  - `merged.md` says: 'no evidence of a boiling lake of water beneath the cloud tops' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text explicitly says no evidence of the claimed lake was found.
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Voyager 2 returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The photographed moons’ names differ from several names in the claim.
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus’ smaller moons.
  - `merged.md` says: 'Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s major moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text calls the moons major rather than smaller and gives different names for three of them.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred the same day as the Uranus encounter.
  - `merged.md` says: 'News of the Uranus encounter is interrupted by the Challenger accident, which kills seven astronauts during the space shuttle launch Jan. 28, 1986.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference dates the accident Jan. 28, while it dates the Uranus flyby Jan. 24, 1986.
- **B-021** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts during their space shuttle launch.
  - `merged.md` says: 'the Challenger accident, which kills seven astronauts during the space shuttle launch' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says seven astronauts were killed, not six.
- **B-022** -- the two documents disagree
  - `source_b.md:9` says: The space shuttle launch occurred Feb. 28, 1986.
  - `merged.md` says: 'the space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference dates the launch Jan. 28, 1986, not Feb. 28.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter is optimized in part to keep future planetary flybys possible.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.\n\nIn fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The optimized Jupiter encounter is attributed to Voyager 3, not Voyager 2.
- **M-006** -- the two documents disagree
  - `merged.md:3` says: The geometry of Voyager 2's Uranus encounter preserves the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The stated possible future encounter is with Saturn, not Neptune.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 is the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source A identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus.
- **M-009** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's short-range observations take place during the Jan. 24, 1986 flyby.
  - `source_b.md` says: 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source B places the Uranus encounter on Feb. 28, 1986, rather than Jan. 24, 1986.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: During Voyager 2's Jan. 24, 1986 flyby, signals take approximately 2,5 hours to reach Earth.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987, when signals took approximately 2,5 hours to reach Earth." (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The signal time is stated for Voyager 1's observations beginning Jan. 31, 1987, not for the claimed Voyager 2 flyby.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach to Uranus occurs at 17:59 UT Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives ED and 1968, rather than UT and 1986, for the closest approach.
- **M-013** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach to Uranus is at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles).' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The claim reverses the source's numbers and units for the range.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: During its flyby of Uranus, Voyager 2 discovers 10 new moons.
  - `source_b.md` says: 'During its flyby, Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says 11 new moons, not 10.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: Puck is one of the new moons discovered by Voyager 2 during its Uranus flyby.
  - `source_b.md` says: 'given such names as Pucka' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The listed name is Pucka, not Puck.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: Portia is one of the new moons discovered by Voyager 2 during its Uranus flyby.
  - `source_b.md` says: 'given such names as Pucka, Portila' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The listed name is Portila, not Portia.
- **M-017** -- the two documents disagree
  - `merged.md:7` says: Juliet is one of the new moons discovered by Voyager 2 during its Uranus flyby.
  - `source_b.md` says: 'Juliette' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The listed name is Juliette, not Juliet.
- **M-018** -- the two documents disagree
  - `merged.md:7` says: Cressida is one of the new moons discovered by Voyager 2 during its Uranus flyby.
  - `source_b.md` says: 'Kressida' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The listed name is Kressida, not Cressida.
- **M-019** -- the two documents disagree
  - `merged.md:7` says: Rosalind is one of the new moons discovered by Voyager 2 during its Uranus flyby.
  - `source_b.md` says: 'Rosalinde' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The listed name is Rosalinde, not Rosalind.
- **M-022** -- the two documents disagree
  - `merged.md:7` says: Cordelia is one of the new moons discovered by Voyager 2 during its Uranus flyby.
  - `source_b.md` says: 'Cordelina' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The listed name is Cordelina, not Cordelia.
- **M-024** -- the two documents disagree
  - `merged.md:7` says: Bianca is one of the new moons discovered by Voyager 2 during its Uranus flyby.
  - `source_b.md` says: 'Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The listed name is Bianca II, not Bianca.
- **M-025** -- the two documents disagree
  - `merged.md:7` says: The names of the moons discovered by Voyager 2 during its Uranus flyby continue the tradition of drawing on Shakespeare.
  - `source_b.md` says: 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes the naming tradition to Goethe, not Shakespeare.
- **M-026** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovers two new rings at Uranus.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says Voyager 2 discovered three new rings, not two.
- **M-027** -- the two documents disagree
  - `merged.md:7` says: Nine rings at Uranus were previously known.
  - `source_b.md` says: 'the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives eight previously known rings, not nine.
- **M-028** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 finds a magnetic field at Uranus tilted at 59 degrees to the planet’s rotation axis.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives a tilt of 66 degrees, not 59 degrees.
- **M-030** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 finds atmospheric winds at Uranus reaching 450 mph (724 km/h).
  - `source_b.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source assigns 450 to km/h, not mph, and does not give 724 km/h.
- **M-031** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 finds no evidence of a boiling lake of water beneath the cloud tops of Uranus.
  - `source_b.md` says: 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says Voyager 2 found evidence of the lake.
- **M-034** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returns photographs of five of Uranus’s major moons.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source calls the five photographed moons smaller moons, not major moons.
- **M-037** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returns photographs of Ariel.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Ariele, not Ariel.
- **M-038** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returns photographs of Umbriel.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Umbrella, not Umbriel.
- **M-039** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returns photographs of Titania.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Titan, not Titania.
- **M-040** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 flies past Miranda at a range of 17,560 miles (28,260 kilometers).
  - `source_b.md` says: 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 17.560 miles and 28.260 kilometers, rather than the claimed numbers.
- **M-045** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident kills seven astronauts.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says six astronauts were killed, not seven.
- **M-046** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident occurs during the space shuttle launch Jan. 28, 1986.
  - `source_b.md` says: 'during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the launch Feb. 28, 1986, not Jan. 28, 1986.

### Invented — in the merge, in neither source

- **M-001** (`merged.md:3`) — Voyager 2 encountered Jupiter.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source A mentions Voyager 3's Jupiter encounter, but neither source says whether Voyager 2 encountered Jupiter.
- **M-002** (`merged.md:3`) — Voyager 2 encountered Saturn.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source A mentions Voyager 1's Saturn flyby, but neither source says whether Voyager 2 encountered Saturn.

### Partly invented — the sources carry some of this claim

- **M-004** (`merged.md:3`) — Voyager 2's journey from Saturn to Uranus takes about 4,5 years.
  - evidence: 'mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The duration of a journey to Uranus is stated, but the journey is attributed to Voyager 3, and no departure from Saturn is stated.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (70 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m7` (`merged.md`) - '2,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **reading resolved by the merge** `m15` (`source_b.md`) - source_b.md writes '17.560' beside 'miles' (line 7), which reads 17.56 in its decimal point convention; the merge writes '17,560' (line 9), which reads 17560 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  At a range of 17,560 miles (28,260 kilometers), its flyby of Miranda brings it closer to that moon than to any other object during its travels.
  ```
- **reading resolved by the merge** `m15` (`source_b.md`) - source_b.md writes '28.260' beside 'kilometers' (line 7), which reads 28.26 in its decimal point convention; the merge writes '28,260' (line 9), which reads 28260 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  At a range of 17,560 miles (28,260 kilometers), its flyby of Miranda brings it closer to that moon than to any other object during its travels.
  ```

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 1 dropped, 8 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | dropped | The text does not discuss Voyager 3 or the fulfillment of primary mission goals. |
| 2 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'After encounters with Jupiter and Saturn, Voyager 2 continues to Uranus' in `merged.md` -- The spacecraft continuing to Uranus is Voyager 2, not Voyager 3. |
| 3 | Voyager 3's journey to Uranus would take about 4,5 years. | 3 | contradicted | 'Voyager 2 continues to Uranus, a journey of about 4,5 years from Saturn' in `merged.md` -- The stated journey belongs to Voyager 2, not Voyager 3. |
| 4 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'Its encounter with Jupiter is optimized in part to keep future planetary flybys possible.' in `merged.md` -- The preceding sentence identifies the spacecraft as Voyager 2, not Voyager 3. |
| 5 | The Ur anus encounter’s geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The geometry of the Uranus encounter preserves the possibility of a future encounter with Neptune.' in `merged.md` -- The possible future encounter is with Neptune, not Saturn. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2 is the first human-made object to fly past Uranus.' in `merged.md` -- The text names Voyager 2, not Voyager 1, as the first. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | 'Its short-range observations take place during the Jan. 24, 1986 flyby' in `merged.md` -- The text identifies Voyager 2 and gives a different date for its short-range observations. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach occurs at 17:59 UT Jan. 24, 1986' in `merged.md` -- The stated time designation and year differ from the claim. |
| 12 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The claim reverses the units assigned to the two figures. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 has only 6.4 days of close study during its flyby of Saturn.' in `merged.md` -- The text states the duration of Voyager 1’s close study during its flyby. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals take approximately 2,5 hours to reach Earth' in `merged.md` -- The stated signal travel time matches the claim. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Sunlight at Uranus is five-hundred times weaker than at Earth.' in `merged.md` -- The text states the claimed comparison of sunlight conditions. |

### `source_b.md` -- 22 claim(s): 1 dropped, 12 contradicted, 1 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 16 | Voyager 2 had been traveling for nearly a century when it flew by Miranda. | 7 | dropped | The reference does not state how long Voyager 2 had been traveling when it flew by Miranda. |
| 1 | Voyager 2 discovered 11 new moons during its flyby. | 3 | contradicted | 'During its flyby, Voyager 2 discovers 10 new moons' in `merged.md` -- The text says 10 new moons, not 11. |
| 2 | The new moons discovered by Voyager 2 were given names such as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Several names in the claim differ from the names listed in the text. |
| 4 | Voyager 2 discovered three new rings during its flyby. | 3 | contradicted | 'It also discovers two new rings' in `merged.md` -- The text says two new rings, not three. |
| 5 | Uranus had eight “older” rings. | 3 | contradicted | 'the nine previously known rings' in `merged.md` -- The text gives nine previously known rings, not eight. |
| 6 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis. | 3 | contradicted | 'a magnetic field tilted at 59 degrees to the planet’s rotation axis' in `merged.md` -- The stated tilt is 59 degrees, not 66 degrees. |
| 8 | Voyager 2 found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'The spacecraft finds atmospheric winds reaching 450 mph (724 km/h)' in `merged.md` -- The claim assigns different units and values to the wind speed. |
| 9 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | contradicted | 'no evidence of a boiling lake of water beneath the cloud tops' in `merged.md` -- The text explicitly says no evidence of the claimed lake was found. |
| 12 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Voyager 2 returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The photographed moons’ names differ from several names in the claim. |
| 13 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus’ smaller moons. | 7 | contradicted | 'Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s major moons' in `merged.md` -- The text calls the moons major rather than smaller and gives different names for three of them. |
| 20 | The Challenger accident occurred the same day as the Uranus encounter. | 9 | contradicted | 'News of the Uranus encounter is interrupted by the Challenger accident, which kills seven astronauts during the space shuttle launch Jan. 28, 1986.' in `merged.md` -- The reference dates the accident Jan. 28, while it dates the Uranus flyby Jan. 24, 1986. |
| 21 | The Challenger accident killed six astronauts during their space shuttle launch. | 9 | contradicted | 'the Challenger accident, which kills seven astronauts during the space shuttle launch' in `merged.md` -- The reference says seven astronauts were killed, not six. |
| 22 | The space shuttle launch occurred Feb. 28, 1986. | 9 | contradicted | 'the space shuttle launch Jan. 28, 1986' in `merged.md` -- The reference dates the launch Jan. 28, 1986, not Feb. 28. |
| 3 | The naming tradition for the moons began in 1687. | 3 | carried in part | 'their names continue the tradition of drawing on Shakespeare' in `merged.md` -- The text mentions a naming tradition but does not say when it began. |
| 7 | The magnetic field discovered by Voyager 2 was off-center. | 3 | carried | 'displaced from its center' in `merged.md` -- The text describes the magnetic field as off-center. |
| 10 | Uranus’ rings were found to be extremely variable in thickness. | 5 | carried | 'Uranus’s rings vary greatly in thickness and transparency.' in `merged.md` -- Great variation in thickness supports the claim. |
| 11 | Uranus’ rings were found to be extremely variable in transparency. | 5 | carried | 'Uranus’s rings vary greatly in thickness and transparency.' in `merged.md` -- Great variation in transparency supports the claim. |
| 14 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'At a range of 17,560 miles (28,260 kilometers), its flyby of Miranda brings it closer to that moon than to any other object during its travels.' in `merged.md` -- The reference gives the same distance, using commas rather than periods as thousands separators. |
| 15 | Voyager 2 came closest to any object so far when it flew by Miranda. | 7 | carried | 'its flyby of Miranda brings it closer to that moon than to any other object during its travels' in `merged.md` -- The Miranda flyby brought Voyager 2 closer to Miranda than it had come to any other object. |
| 17 | Images of Miranda showed an object whose surface was a mishmash of features. | 7 | carried | 'Images show a surface with a striking mixture of seemingly unrelated features.' in `merged.md` -- A striking mixture of unrelated surface features conveys the claimed mishmash. |
| 18 | Uranus appeared generally featureless. | 7 | carried | 'Uranus itself appears generally featureless.' in `merged.md` -- The reference states the claim directly. |
| 19 | News of the Uranus encounter was interrupted by the Challenger accident. | 9 | carried | 'News of the Uranus encounter is interrupted by the Challenger accident' in `merged.md` -- The reference states the claim directly. |

### `merged.md` -- 46 claim(s): 2 invented, 28 contradicted, 1 supported in part, 15 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 encountered Jupiter. | invented | -- | Source A mentions Voyager 3's Jupiter encounter, but neither source says whether Voyager 2 encountered Jupiter. |
| 2 | Voyager 2 encountered Saturn. | invented | -- | Source A mentions Voyager 1's Saturn flyby, but neither source says whether Voyager 2 encountered Saturn. |
| 5 | Voyager 2's encounter with Jupiter is optimized in part to keep future planetary flybys possible. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.\n\nIn fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- The optimized Jupiter encounter is attributed to Voyager 3, not Voyager 2. |
| 6 | The geometry of Voyager 2's Uranus encounter preserves the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- The stated possible future encounter is with Saturn, not Neptune. |
| 8 | Voyager 2 is the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source A identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus. |
| 9 | Voyager 2's short-range observations take place during the Jan. 24, 1986 flyby. | contradicted | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- Source B places the Uranus encounter on Feb. 28, 1986, rather than Jan. 24, 1986. |
| 10 | During Voyager 2's Jan. 24, 1986 flyby, signals take approximately 2,5 hours to reach Earth. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987, when signals took approximately 2,5 hours to reach Earth." in `source_a.md` -- The signal time is stated for Voyager 1's observations beginning Jan. 31, 1987, not for the claimed Voyager 2 flyby. |
| 12 | Voyager 2's closest approach to Uranus occurs at 17:59 UT Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- The source gives ED and 1968, rather than UT and 1986, for the closest approach. |
| 13 | Voyager 2's closest approach to Uranus is at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles).' in `source_a.md` -- The claim reverses the source's numbers and units for the range. |
| 14 | During its flyby of Uranus, Voyager 2 discovers 10 new moons. | contradicted | `source_b.md` | 'During its flyby, Voyager 2 discovered 11 new moons' in `source_b.md` -- The source says 11 new moons, not 10. |
| 15 | Puck is one of the new moons discovered by Voyager 2 during its Uranus flyby. | contradicted | `source_b.md` | 'given such names as Pucka' in `source_b.md` -- The listed name is Pucka, not Puck. |
| 16 | Portia is one of the new moons discovered by Voyager 2 during its Uranus flyby. | contradicted | `source_b.md` | 'given such names as Pucka, Portila' in `source_b.md` -- The listed name is Portila, not Portia. |
| 17 | Juliet is one of the new moons discovered by Voyager 2 during its Uranus flyby. | contradicted | `source_b.md` | 'Juliette' in `source_b.md` -- The listed name is Juliette, not Juliet. |
| 18 | Cressida is one of the new moons discovered by Voyager 2 during its Uranus flyby. | contradicted | `source_b.md` | 'Kressida' in `source_b.md` -- The listed name is Kressida, not Cressida. |
| 19 | Rosalind is one of the new moons discovered by Voyager 2 during its Uranus flyby. | contradicted | `source_b.md` | 'Rosalinde' in `source_b.md` -- The listed name is Rosalinde, not Rosalind. |
| 22 | Cordelia is one of the new moons discovered by Voyager 2 during its Uranus flyby. | contradicted | `source_b.md` | 'Cordelina' in `source_b.md` -- The listed name is Cordelina, not Cordelia. |
| 24 | Bianca is one of the new moons discovered by Voyager 2 during its Uranus flyby. | contradicted | `source_b.md` | 'Ophelia, and Bianca II' in `source_b.md` -- The listed name is Bianca II, not Bianca. |
| 25 | The names of the moons discovered by Voyager 2 during its Uranus flyby continue the tradition of drawing on Shakespeare. | contradicted | `source_b.md` | 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' in `source_b.md` -- The source attributes the naming tradition to Goethe, not Shakespeare. |
| 26 | Voyager 2 discovers two new rings at Uranus. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source says Voyager 2 discovered three new rings, not two. |
| 27 | Nine rings at Uranus were previously known. | contradicted | `source_b.md` | 'the “older” eight rings' in `source_b.md` -- The source gives eight previously known rings, not nine. |
| 28 | Voyager 2 finds a magnetic field at Uranus tilted at 59 degrees to the planet’s rotation axis. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source gives a tilt of 66 degrees, not 59 degrees. |
| 30 | Voyager 2 finds atmospheric winds at Uranus reaching 450 mph (724 km/h). | contradicted | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source assigns 450 to km/h, not mph, and does not give 724 km/h. |
| 31 | Voyager 2 finds no evidence of a boiling lake of water beneath the cloud tops of Uranus. | contradicted | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- The source says Voyager 2 found evidence of the lake. |
| 34 | Voyager 2 returns photographs of five of Uranus’s major moons. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source calls the five photographed moons smaller moons, not major moons. |
| 37 | Voyager 2 returns photographs of Ariel. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source names Ariele, not Ariel. |
| 38 | Voyager 2 returns photographs of Umbriel. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source names Umbrella, not Umbriel. |
| 39 | Voyager 2 returns photographs of Titania. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source names Titan, not Titania. |
| 40 | Voyager 2 flies past Miranda at a range of 17,560 miles (28,260 kilometers). | contradicted | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- The source gives 17.560 miles and 28.260 kilometers, rather than the claimed numbers. |
| 45 | The Challenger accident kills seven astronauts. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- The source says six astronauts were killed, not seven. |
| 46 | The Challenger accident occurs during the space shuttle launch Jan. 28, 1986. | contradicted | `source_b.md` | 'during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source dates the launch Feb. 28, 1986, not Jan. 28, 1986. |
| 4 | Voyager 2's journey from Saturn to Uranus takes about 4,5 years. | supported in part | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.' in `source_a.md` -- The duration of a journey to Uranus is stated, but the journey is attributed to Voyager 3, and no departure from Saturn is stated. |
| 3 | Voyager 2 continues to Uranus. | supported | `source_b.md` | 'During its flyby, Voyager 2 discovered 11 new moons' in `source_b.md` -- Voyager 2's flyby in this document is its Uranus flyby. |
| 7 | Voyager 1 has only 6.4 days of close study during its flyby of Saturn. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- The preceding clause identifies Saturn as the possible encounter discussed in this sentence. |
| 11 | Sunlight at Uranus is five-hundred times weaker than at Earth. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- The source describes light at Uranus as five-hundred times less than on Earth. |
| 20 | Belinda is one of the new moons discovered by Voyager 2 during its Uranus flyby. | supported | `source_b.md` | 'Rosalinde, Belinda, Desdemona' in `source_b.md` -- Belinda appears among the names given for Voyager 2's newly discovered moons. |
| 21 | Desdemona is one of the new moons discovered by Voyager 2 during its Uranus flyby. | supported | `source_b.md` | 'Belinda, Desdemona, Cordelina' in `source_b.md` -- Desdemona appears among the names given for Voyager 2's newly discovered moons. |
| 23 | Ophelia is one of the new moons discovered by Voyager 2 during its Uranus flyby. | supported | `source_b.md` | 'Cordelina, Ophelia, and Bianca II' in `source_b.md` -- Ophelia appears among the names given for Voyager 2's newly discovered moons. |
| 29 | Voyager 2 finds that the magnetic field at Uranus is displaced from the planet's center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Off-center states that the magnetic field is displaced from the planet’s center. |
| 32 | Uranus’s rings vary greatly in thickness. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- Extremely variable thickness supports the claim. |
| 33 | Uranus’s rings vary greatly in transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- Extremely variable transparency supports the claim. |
| 35 | Voyager 2 returns photographs of Miranda. | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Miranda is among the moons photographed. |
| 36 | Voyager 2 returns photographs of Oberon. | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Oberon is among the moons photographed. |
| 41 | Voyager 2's flyby of Miranda brings it closer to Miranda than to any other object during its travels. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source says the Miranda flyby was the spacecraft’s closest approach to any object so far. |
| 42 | Images of Miranda show a surface with a mixture of seemingly unrelated features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.' in `source_b.md` -- The source describes Miranda’s surface as a mixture of seemingly unrelated features. |
| 43 | Uranus appears generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- The source states the claim directly. |
| 44 | News of the Uranus encounter is interrupted by the Challenger accident. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- The source says the accident interrupted news of the encounter. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **46** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **34**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 5 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '66' (degrees) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '479' (miles) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '900' (kilometers) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '17.560' (miles) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '28.260' (kilometers) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **15** departure(s) from its sources. Checking them confirms 5, rejects 10, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | duplicate | The title is already carried by a1. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a2` | reworded | The mission history corrects the spacecraft and earlier encounters. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back MISSING, A-002 came back CONTRADICTED, A-003 came back CONTRADICTED (`A-001`, `A-002`, `A-003`) |
| `a3` | reworded | The Jupiter flyby purpose is retained in present tense. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-004 came back CONTRADICTED (`A-004`) |
| `a4` | reworded | The trajectory points toward Neptune, while the study detail is retained. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED (`A-005`) |
| `a5` | reworded | The flyby account corrects the spacecraft and observation date. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a6` | reworded | The light comparison is expressed clearly in present tense. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`) |
| `a7` | reworded | The approach date, time designation, and distance units are corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b2` | reworded | The discoveries, names, literary source, and magnetic tilt are corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back PARTIAL, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`, `B-005`, `B-006`) |
| `b3` | reworded | The wind units are corrected and the unsupported lake finding is removed. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED, B-009 came back CONTRADICTED (`B-008`, `B-009`) |
| `b4` | reworded | The ring observation is retained in present tense. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |
| `b5` | reworded | The moon names and their description are corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back CONTRADICTED, B-013 came back CONTRADICTED (`B-012`, `B-013`) |
| `b6` | reworded | The distance notation and implausible travel duration are corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-016 came back MISSING (`B-016`) |
| `b7` | reworded | Miranda’s unusual appearance is expressed more concisely. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-017`) |
| `b8` | reworded | The observation is retained in present tense. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-018`) |
| `b9` | reworded | The accident date, crew count, and timing relative to the flyby are corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-020 came back CONTRADICTED, B-021 came back CONTRADICTED, B-022 came back CONTRADICTED (`B-020`, `B-021`, `B-022`) |

## Added from outside the documents

The merge declared 11 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

11 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| After encounters with Jupiter and Saturn, Voyager 2 continues to Uranus, a journey of about 4,5 years from Saturn. | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters | the model's own knowledge | *no source* | Voyager 2 encounters Jupiter and Saturn before Uranus. | *none* |
| The geometry of the Uranus encounter preserves the possibility of a future encounter with Neptune. | possibility of a future encounter with Saturn | the model's own knowledge | *no source* | Neptune, not Saturn, is the next planetary encounter. | *none* |
| Voyager 2 is the first human-made object to fly past Uranus. | The first human-made object to fly past Uranus, Voyager 1's | the model's own knowledge | *no source* | Voyager 2 makes the Uranus flyby. | *none* |
| Its short-range observations take place during the Jan. 24, 1986 flyby, when signals take approximately 2,5 hours to reach Earth. | short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | The Uranus flyby takes place on Jan. 24, 1986. | *none* |
| Closest approach occurs at 17:59 UT Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | The year and time designation are wrong, and the distance units are reversed. | *none* |
| During its flyby, Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca; their names continue the tradition of drawing on Shakespeare. | 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687) | the model's own knowledge | *no source* | The flyby discovers 10 moons whose listed names draw on Shakespeare. | *none* |
| It also discovers two new rings in addition to the nine previously known rings and finds a magnetic field tilted at 59 degrees to the planet’s rotation axis and displaced from its center. | three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center | the model's own knowledge | *no source* | The ring counts and magnetic tilt in the source are inaccurate. | *none* |
| The spacecraft finds atmospheric winds reaching 450 mph (724 km/h), but no evidence of a boiling lake of water beneath the cloud tops. | 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface | the model's own knowledge | *no source* | The wind units are wrong, and Voyager 2 does not observe such a lake. | *none* |
| Voyager 2 returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s major moons. | Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons | the model's own knowledge | *no source* | Ariel, Umbriel, and Titania are the intended moon names. | *none* |
| At a range of 17,560 miles (28,260 kilometers), its flyby of Miranda brings it closer to that moon than to any other object during its travels. | 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels | the model's own knowledge | *no source* | The notation implies tiny distances, and the mission is not a century old. | *none* |
| News of the Uranus encounter is interrupted by the Challenger accident, which kills seven astronauts during the space shuttle launch Jan. 28, 1986. | the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger is lost four days after the flyby, killing seven astronauts. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-sol |
| Model (decompose) | gpt-6-sol |
| Model (verify) | gpt-6-sol |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 10 live, 0 cached, 0 replayed |
| Tokens | 27,609 in, 22,054 out, 8,640 cached, 6,187 reasoning |
| Cost | ~$0.26 estimated (rates read 2026-09-25) |
| Schema repairs | 2 |
| Errors | 0 |
| Duration | 214.5s |
| Generated | 2026-09-27T17:53:13+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
