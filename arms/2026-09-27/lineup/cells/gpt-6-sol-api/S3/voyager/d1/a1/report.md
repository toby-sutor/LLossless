## Verdict

**66 finding(s).** In the claims: 1 dropped, 1 partially dropped, 46 contradicted, 6 hallucinated, 1 partially invented. In the structure: 11 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 32 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 34 |
| Forward — source claims accounted for in the merge | **12/46** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **2/12** |
| Forward — `source_b.md` claims accounted for | **10/34** (1 in part) |
| Reverse — merge claims found in a source | **11/32** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **71/71** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **B-013** (`source_b.md:3`) — The naming tradition began in 1687.
  - judged against: `merged.md`
  - rationale: The text gives no date for the start of the naming tradition.

### Partly dropped — the merge carries some of this claim

- **B-019** (`source_b.md:5`) — The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  - evidence: 'Its observations also inform models of Uranus’s deep, water-bearing interior.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference connects the observations to water deep inside Uranus, but does not describe a boiling lake or give its depth.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'After completing its primary encounters with Jupiter and Saturn, Voyager 2 continues to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text identifies Voyager 2 and two primary planetary encounters, not Voyager 3 and three.
- **A-002** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'Voyager 2 continues to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The spacecraft continuing to Uranus is Voyager 2, not Voyager 3.
- **A-003** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3's journey to Uranus would take about 4,5 years.
  - `merged.md` says: 'Voyager 2 continues to Uranus, a journey of about 4,5 years' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The journey duration is stated for Voyager 2, not Voyager 3.
- **A-004** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'Voyager 2 continues to Uranus, a journey of about 4,5 years. Its Jupiter encounter is optimized in part to make subsequent planetary flybys possible.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The optimized Jupiter encounter belongs to Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Ur anus encounter’s geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The geometry of its Uranus encounter also preserves the possibility of a later flyby of Neptune.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The later flyby made possible is of Neptune, not Saturn.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2 is the first human-made object to fly past Uranus.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text identifies Voyager 2, not Voyager 1, as the first.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: 'Its short-range observations begin before closest approach, and signals take approximately 2,5 hours to reach Earth. Sunlight at Uranus is approximately 400 times weaker than at Earth. Closest approach occurs at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The observations began before a closest approach in January 1986, not on Jan. 31, 1987.
- **A-010** -- the two documents disagree
  - `source_a.md:9` says: Light conditions were five-hundred times less than terrestrial conditions.
  - `merged.md` says: 'Sunlight at Uranus is approximately 400 times weaker than at Earth.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives approximately 400 times weaker, not 500.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach occurs at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The time standard and year differ from the claim.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim reverses which number is in kilometers and which is in miles.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: Pucka was among the names given to the new moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed name is Puck, not Pucka.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: Portila was among the names given to the new moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed name is Portia, not Portila.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: Juliette was among the names given to the new moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed name is Juliet, not Juliette.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Kressida was among the names given to the new moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed name is Cressida, not Kressida.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Rosalinde was among the names given to the new moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed name is Rosalind, not Rosalinde.
- **B-009** -- the two documents disagree
  - `source_b.md:3` says: Cordelina was among the names given to the new moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed name is Cordelia, not Cordelina.
- **B-011** -- the two documents disagree
  - `source_b.md:3` says: Bianca II was among the names given to the new moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed name is Bianca, not Bianca II.
- **B-012** -- the two documents disagree
  - `source_b.md:3` says: The names given to the new moons allude to Goethe.
  - `merged.md` says: 'whose names draw on characters from Shakespeare and Alexander Pope' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes the names to Shakespeare and Alexander Pope, not Goethe.
- **B-014** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings during its flyby of Uranus.
  - `merged.md` says: 'It also discovers two new rings, bringing the known total to 11' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says Voyager 2 discovered two new rings, not three.
- **B-015** -- the two documents disagree
  - `source_b.md:3` says: Uranus had eight “older” rings in addition to the three new rings.
  - `merged.md` says: 'two new rings, bringing the known total to 11' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Two new rings out of a total of 11 leaves nine previously known rings, not eight.
- **B-016** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis.
  - `merged.md` says: 'a magnetic field tilted at 59 degrees to the rotation axis' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated tilt is 59 degrees, not 66 degrees.
- **B-018** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'The spacecraft measures atmospheric winds as high as 450 km/h.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated 450 km/h equals 450,000 meters per hour, not the claim’s 72,400 meters per hour.
- **B-024** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Ariele.
  - `merged.md` says: 'Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Ariel, not Ariele.
- **B-025** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Umbrella.
  - `merged.md` says: 'Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Umbriel, not Umbrella.
- **B-026** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Titan.
  - `merged.md` says: 'Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Titania, not Titan.
- **B-027** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus’ smaller moons.
  - `merged.md` says: 'Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s moons.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference’s list has Ariel, Umbriel, and Titania rather than Ariele, Umbrella, and Titan.
- **B-028** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers).
  - `merged.md` says: 'At a range of only 17,560 miles (28,260 kilometers), its flyby of Miranda' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 17,560 miles and 28,260 kilometers; the claim’s decimal-point figures have different values.
- **B-029** -- the two documents disagree
  - `source_b.md:7` says: The Miranda flyby brought Voyager 2 closer to an object than it had come so far in its nearly century-long travels.
  - `merged.md` says: 'Voyager 2 continues to Uranus, a journey of about 4,5 years.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference describes a journey of about 4,5 years, incompatible with nearly century-long travels.
- **B-032** -- the two documents disagree
  - `source_b.md:9` says: News of the Uranus encounter was interrupted the same day by the Challenger accident.
  - `merged.md` says: 'News of the Uranus encounter is overshadowed by the Challenger accident on Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference dates the Challenger accident Jan. 28, four days after the stated Jan. 24 Uranus closest approach.
- **B-033** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'which kills seven astronauts during their space shuttle launch.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says seven astronauts were killed, not six.
- **B-034** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during a space shuttle launch Feb. 28, 1986.
  - `merged.md` says: 'the Challenger accident on Jan. 28, 1986, which kills seven astronauts during their space shuttle launch.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference dates the launch accident Jan. 28, 1986, not Feb. 28.
- **M-006** -- the two documents disagree
  - `merged.md:3` says: The geometry of Voyager 2’s Uranus encounter preserves the possibility of a later flyby of Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Saturn, not Neptune, as the possible future encounter.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 is the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies Voyager 1, not Voyager 2, as the first.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Sunlight at Uranus is approximately 400 times weaker than at Earth.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives a factor of five hundred, not four hundred.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Voyager 2’s closest approach to Uranus occurs at 17:59 UT Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The stated time zone and year differ from the claim.
- **M-013** -- the two documents disagree
  - `merged.md:5` says: Voyager 2’s closest approach to Uranus occurs at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The claim reverses the units assigned to the two distances.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: During the Uranus flyby, Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says 11 new moons, not 10, and gives different forms for several names.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The names of Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca draw on characters from Shakespeare and Alexander Pope.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes the naming allusions to Goethe, not Shakespeare and Alexander Pope.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovers two new rings at Uranus.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says three new rings, not two.
- **M-018** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 finds a magnetic field at Uranus tilted at 59 degrees to the rotation axis.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives a tilt of 66 degrees, not 59 degrees.
- **M-024** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives Ariele, Umbrella, and Titan rather than Ariel, Umbriel, and Titania.
- **M-025** -- the two documents disagree
  - `merged.md:9` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus’s moons.
  - `source_b.md` says: 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies a five-moon list with three names different from those in the claim.
- **M-026** -- the two documents disagree
  - `merged.md:9` says: Voyager 2’s flyby of Miranda is at a range of only 17,560 miles (28,260 kilometers).
  - `source_b.md` says: 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the range as 17.560 miles (28.260 kilometers), not the numbers written in the claim.
- **M-031** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident occurs on Jan. 28, 1986.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the accident Feb. 28, 1986, rather than Jan. 28, 1986.
- **M-032** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident kills seven astronauts during their space shuttle launch.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says six astronauts were killed, rather than seven.

### Invented — in the merge, in neither source

- **M-001** (`merged.md:3`) — Voyager 2 completed its primary encounter with Jupiter.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The sources mention a Jupiter encounter for Voyager 3, but do not say Voyager 2 completed a primary encounter there.
- **M-002** (`merged.md:3`) — Voyager 2 completed its primary encounter with Saturn.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Neither source says Voyager 2 completed a primary encounter with Saturn.
- **M-004** (`merged.md:3`) — Voyager 2’s journey to Uranus is about 4,5 years.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The approximately 4,5-year journey is attributed to Voyager 3, not Voyager 2.
- **M-005** (`merged.md:3`) — Voyager 2’s Jupiter encounter is optimized in part to make subsequent planetary flybys possible.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The optimized Jupiter encounter is attributed to Voyager 3; neither source states this about Voyager 2.
- **M-009** (`merged.md:5`) — Voyager 2’s short-range observations begin before closest approach.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Neither source dates the beginning of Voyager 2’s short-range observations relative to its closest approach.
- **M-010** (`merged.md:5`) — Signals from Voyager 2 take approximately 2,5 hours to reach Earth.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The approximately 2,5-hour signal time is given for Voyager 1’s observations, not Voyager 2’s.

### Partly invented — the sources carry some of this claim

- **M-021** (`merged.md:7`) — Voyager 2’s observations inform models of Uranus’s deep, water-bearing interior.
  - evidence: 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source supports observations concerning water below the clouds, but does not say they informed models of Uranus’s interior.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (69 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m7` (`merged.md`) - '2,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **reading resolved by the merge** `m16` (`source_b.md`) - source_b.md writes '17.560' beside 'miles' (line 7), which reads 17.56 in its decimal point convention; the merge writes '17,560' (line 9), which reads 17560 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  At a range of only 17,560 miles (28,260 kilometers), its flyby of Miranda brings the spacecraft closer to an object than any earlier encounter on its journey.
  ```
- **reading resolved by the merge** `m16` (`source_b.md`) - source_b.md writes '28.260' beside 'kilometers' (line 7), which reads 28.26 in its decimal point convention; the merge writes '28,260' (line 9), which reads 28260 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  At a range of only 17,560 miles (28,260 kilometers), its flyby of Miranda brings the spacecraft closer to an object than any earlier encounter on its journey.
  ```

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 10 contradicted, 0 carried in part, 2 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'After completing its primary encounters with Jupiter and Saturn, Voyager 2 continues to Uranus' in `merged.md` -- The text identifies Voyager 2 and two primary planetary encounters, not Voyager 3 and three. |
| 2 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'Voyager 2 continues to Uranus' in `merged.md` -- The spacecraft continuing to Uranus is Voyager 2, not Voyager 3. |
| 3 | Voyager 3's journey to Uranus would take about 4,5 years. | 3 | contradicted | 'Voyager 2 continues to Uranus, a journey of about 4,5 years' in `merged.md` -- The journey duration is stated for Voyager 2, not Voyager 3. |
| 4 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'Voyager 2 continues to Uranus, a journey of about 4,5 years. Its Jupiter encounter is optimized in part to make subsequent planetary flybys possible.' in `merged.md` -- The optimized Jupiter encounter belongs to Voyager 2, not Voyager 3. |
| 5 | The Ur anus encounter’s geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The geometry of its Uranus encounter also preserves the possibility of a later flyby of Neptune.' in `merged.md` -- The later flyby made possible is of Neptune, not Saturn. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2 is the first human-made object to fly past Uranus.' in `merged.md` -- The text identifies Voyager 2, not Voyager 1, as the first. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | 'Its short-range observations begin before closest approach, and signals take approximately 2,5 hours to reach Earth. Sunlight at Uranus is approximately 400 times weaker than at Earth. Closest approach occurs at 17:59 UT Jan. 24, 1986' in `merged.md` -- The observations began before a closest approach in January 1986, not on Jan. 31, 1987. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | contradicted | 'Sunlight at Uranus is approximately 400 times weaker than at Earth.' in `merged.md` -- The text gives approximately 400 times weaker, not 500. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach occurs at 17:59 UT Jan. 24, 1986' in `merged.md` -- The time standard and year differ from the claim. |
| 12 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The claim reverses which number is in kilometers and which is in miles. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `merged.md` -- The text states the claim directly. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals take approximately 2,5 hours to reach Earth' in `merged.md` -- The signal travel time matches the claim. |

### `source_b.md` -- 34 claim(s): 1 dropped, 22 contradicted, 1 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 13 | The naming tradition began in 1687. | 3 | dropped | The text gives no date for the start of the naming tradition. |
| 1 | Voyager 2 discovered 11 new moons during its flyby. | 3 | contradicted | 'Voyager 2 discovers 10 new moons' in `merged.md` -- The text says 10 new moons, not 11. |
| 2 | Pucka was among the names given to the new moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The listed name is Puck, not Pucka. |
| 3 | Portila was among the names given to the new moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The listed name is Portia, not Portila. |
| 4 | Juliette was among the names given to the new moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The listed name is Juliet, not Juliette. |
| 5 | Kressida was among the names given to the new moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The listed name is Cressida, not Kressida. |
| 6 | Rosalinde was among the names given to the new moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The listed name is Rosalind, not Rosalinde. |
| 9 | Cordelina was among the names given to the new moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The listed name is Cordelia, not Cordelina. |
| 11 | Bianca II was among the names given to the new moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The listed name is Bianca, not Bianca II. |
| 12 | The names given to the new moons allude to Goethe. | 3 | contradicted | 'whose names draw on characters from Shakespeare and Alexander Pope' in `merged.md` -- The text attributes the names to Shakespeare and Alexander Pope, not Goethe. |
| 14 | Voyager 2 discovered three new rings during its flyby of Uranus. | 3 | contradicted | 'It also discovers two new rings, bringing the known total to 11' in `merged.md` -- The reference says Voyager 2 discovered two new rings, not three. |
| 15 | Uranus had eight “older” rings in addition to the three new rings. | 3 | contradicted | 'two new rings, bringing the known total to 11' in `merged.md` -- Two new rings out of a total of 11 leaves nine previously known rings, not eight. |
| 16 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis. | 3 | contradicted | 'a magnetic field tilted at 59 degrees to the rotation axis' in `merged.md` -- The stated tilt is 59 degrees, not 66 degrees. |
| 18 | The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'The spacecraft measures atmospheric winds as high as 450 km/h.' in `merged.md` -- The stated 450 km/h equals 450,000 meters per hour, not the claim’s 72,400 meters per hour. |
| 24 | Voyager 2 returned photos of Ariele. | 7 | contradicted | 'Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The reference names Ariel, not Ariele. |
| 25 | Voyager 2 returned photos of Umbrella. | 7 | contradicted | 'Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The reference names Umbriel, not Umbrella. |
| 26 | Voyager 2 returned photos of Titan. | 7 | contradicted | 'Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The reference names Titania, not Titan. |
| 27 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus’ smaller moons. | 7 | contradicted | 'Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s moons.' in `merged.md` -- The reference’s list has Ariel, Umbriel, and Titania rather than Ariele, Umbrella, and Titan. |
| 28 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | contradicted | 'At a range of only 17,560 miles (28,260 kilometers), its flyby of Miranda' in `merged.md` -- The reference gives 17,560 miles and 28,260 kilometers; the claim’s decimal-point figures have different values. |
| 29 | The Miranda flyby brought Voyager 2 closer to an object than it had come so far in its nearly century-long travels. | 7 | contradicted | 'Voyager 2 continues to Uranus, a journey of about 4,5 years.' in `merged.md` -- The reference describes a journey of about 4,5 years, incompatible with nearly century-long travels. |
| 32 | News of the Uranus encounter was interrupted the same day by the Challenger accident. | 9 | contradicted | 'News of the Uranus encounter is overshadowed by the Challenger accident on Jan. 28, 1986' in `merged.md` -- The reference dates the Challenger accident Jan. 28, four days after the stated Jan. 24 Uranus closest approach. |
| 33 | The Challenger accident killed six astronauts. | 9 | contradicted | 'which kills seven astronauts during their space shuttle launch.' in `merged.md` -- The reference says seven astronauts were killed, not six. |
| 34 | The Challenger accident occurred during a space shuttle launch Feb. 28, 1986. | 9 | contradicted | 'the Challenger accident on Jan. 28, 1986, which kills seven astronauts during their space shuttle launch.' in `merged.md` -- The reference dates the launch accident Jan. 28, 1986, not Feb. 28. |
| 19 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | carried in part | 'Its observations also inform models of Uranus’s deep, water-bearing interior.' in `merged.md` -- The reference connects the observations to water deep inside Uranus, but does not describe a boiling lake or give its depth. |
| 7 | Belinda was among the names given to the new moons discovered by Voyager 2. | 3 | carried | 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Belinda appears among the new moons discovered by Voyager 2. |
| 8 | Desdemona was among the names given to the new moons discovered by Voyager 2. | 3 | carried | 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Desdemona appears among the new moons discovered by Voyager 2. |
| 10 | Ophelia was among the names given to the new moons discovered by Voyager 2. | 3 | carried | 'Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Ophelia appears among the new moons discovered by Voyager 2. |
| 17 | The magnetic field discovered by Voyager 2 was off-center. | 3 | carried | 'a magnetic field tilted at 59 degrees to the rotation axis and offset from the planet’s center' in `merged.md` -- The reference describes the magnetic field as offset from the planet’s center. |
| 20 | Uranus’ rings were found to be extremely variable in thickness. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- The reference explicitly states that the rings varied extremely in thickness. |
| 21 | Uranus’ rings were found to be extremely variable in transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- The reference explicitly states that the rings varied extremely in transparency. |
| 22 | Voyager 2 returned photos of Miranda. | 7 | carried | 'Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- Miranda is among the moons Voyager 2 imaged. |
| 23 | Voyager 2 returned photos of Oberon. | 7 | carried | 'Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- Oberon is among the moons Voyager 2 imaged. |
| 30 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Miranda’s images show a striking patchwork of seemingly unrelated surface features' in `merged.md` -- A patchwork of seemingly unrelated features supports the claimed mishmash. |
| 31 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appears generally featureless.' in `merged.md` -- The reference states the claim directly. |

### `merged.md` -- 32 claim(s): 6 invented, 14 contradicted, 1 supported in part, 11 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 completed its primary encounter with Jupiter. | invented | -- | The sources mention a Jupiter encounter for Voyager 3, but do not say Voyager 2 completed a primary encounter there. |
| 2 | Voyager 2 completed its primary encounter with Saturn. | invented | -- | Neither source says Voyager 2 completed a primary encounter with Saturn. |
| 4 | Voyager 2’s journey to Uranus is about 4,5 years. | invented | -- | The approximately 4,5-year journey is attributed to Voyager 3, not Voyager 2. |
| 5 | Voyager 2’s Jupiter encounter is optimized in part to make subsequent planetary flybys possible. | invented | -- | The optimized Jupiter encounter is attributed to Voyager 3; neither source states this about Voyager 2. |
| 9 | Voyager 2’s short-range observations begin before closest approach. | invented | -- | Neither source dates the beginning of Voyager 2’s short-range observations relative to its closest approach. |
| 10 | Signals from Voyager 2 take approximately 2,5 hours to reach Earth. | invented | -- | The approximately 2,5-hour signal time is given for Voyager 1’s observations, not Voyager 2’s. |
| 6 | The geometry of Voyager 2’s Uranus encounter preserves the possibility of a later flyby of Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- The source names Saturn, not Neptune, as the possible future encounter. |
| 8 | Voyager 2 is the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- The source identifies Voyager 1, not Voyager 2, as the first. |
| 11 | Sunlight at Uranus is approximately 400 times weaker than at Earth. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- The source gives a factor of five hundred, not four hundred. |
| 12 | Voyager 2’s closest approach to Uranus occurs at 17:59 UT Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- The stated time zone and year differ from the claim. |
| 13 | Voyager 2’s closest approach to Uranus occurs at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- The claim reverses the units assigned to the two distances. |
| 14 | During the Uranus flyby, Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- The source says 11 new moons, not 10, and gives different forms for several names. |
| 15 | The names of Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca draw on characters from Shakespeare and Alexander Pope. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- The source attributes the naming allusions to Goethe, not Shakespeare and Alexander Pope. |
| 16 | Voyager 2 discovers two new rings at Uranus. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source says three new rings, not two. |
| 18 | Voyager 2 finds a magnetic field at Uranus tilted at 59 degrees to the rotation axis. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source gives a tilt of 66 degrees, not 59 degrees. |
| 24 | Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source gives Ariele, Umbrella, and Titan rather than Ariel, Umbriel, and Titania. |
| 25 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus’s moons. | contradicted | `source_b.md` | 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source identifies a five-moon list with three names different from those in the claim. |
| 26 | Voyager 2’s flyby of Miranda is at a range of only 17,560 miles (28,260 kilometers). | contradicted | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- The source gives the range as 17.560 miles (28.260 kilometers), not the numbers written in the claim. |
| 31 | The Challenger accident occurs on Jan. 28, 1986. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source dates the accident Feb. 28, 1986, rather than Jan. 28, 1986. |
| 32 | The Challenger accident kills seven astronauts during their space shuttle launch. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source says six astronauts were killed, rather than seven. |
| 21 | Voyager 2’s observations inform models of Uranus’s deep, water-bearing interior. | supported in part | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- The source supports observations concerning water below the clouds, but does not say they informed models of Uranus’s interior. |
| 3 | Voyager 2 continues to Uranus. | supported | `source_b.md` | 'During its flyby, Voyager 2 discovered 11 new moons' in `source_b.md` -- Voyager 2’s flyby of Uranus supports the general statement that it continued to the planet. |
| 7 | Voyager 1 had only 6.4 days of close study during its flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- The source states the claim directly. |
| 17 | The known total of Uranus’s rings reaches 11. | supported | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Three new rings added to eight older rings gives a total of 11. |
| 19 | Voyager 2 finds a magnetic field at Uranus offset from the planet’s center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source describes the magnetic field as off-center. |
| 20 | Voyager 2 measures atmospheric winds as high as 450 km/h at Uranus. | supported | `source_b.md` | 'The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h' in `source_b.md` -- The source states the claimed wind speed. |
| 22 | Uranus’s rings were found to be extremely variable in thickness. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source explicitly says the rings varied extremely in thickness. |
| 23 | Uranus’s rings were found to be extremely variable in transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source explicitly says the rings varied extremely in transparency. |
| 27 | Voyager 2’s flyby of Miranda brings the spacecraft closer to an object than any earlier encounter on its journey. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels.' in `source_b.md` -- The source says the Miranda flyby was the spacecraft’s closest approach to any object up to that point. |
| 28 | Miranda’s images show a patchwork of surface features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.' in `source_b.md` -- A mishmash of surface features supports the claim’s description of a patchwork. |
| 29 | Uranus appears generally featureless in Voyager 2’s images. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- The source directly describes Uranus as generally featureless. |
| 30 | News of the Uranus encounter is overshadowed by the Challenger accident. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- The source says news of the encounter was interrupted by the accident, supporting the claim’s general description. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **32** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **46**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 4 attributed segment(s) — not conclusive on this evidence base. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
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

The merge declared **14** departure(s) from its sources. Checking them confirms 3, rejects 11, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | The mission slot corrects the spacecraft and its primary encounters. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back CONTRADICTED, A-003 came back CONTRADICTED (`A-001`, `A-002`, `A-003`) |
| `a3` | reworded | The trajectory slot states the same purpose more directly. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-004 came back CONTRADICTED (`A-004`) |
| `a4` | reworded | The trajectory slot corrects the later destination and retains the study period. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED (`A-005`) |
| `a5` | reworded | The encounter slot corrects the spacecraft and removes the erroneous date. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a6` | reworded | The light-conditions slot uses an approximate solar-distance calculation. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-010 came back CONTRADICTED (`A-010`) |
| `a7` | reworded | The closest-approach slot corrects the year, time standard, and units. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | duplicate | The title slot already carries the identical base heading. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b2` | reworded | The discoveries slot corrects the count, names, rings, and magnetic tilt. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED, B-009 came back CONTRADICTED, B-011 came back CONTRADICTED, B-012 came back CONTRADICTED, B-013 came back MISSING, B-014 came back CONTRADICTED, B-015 came back CONTRADICTED, B-016 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`, `B-005`, `B-006`, `B-009`, `B-011`, `B-012`, `B-013`, `B-014`, `B-015`, `B-016`) |
| `b3` | reworded | The atmosphere slot removes an incorrect conversion and unsupported lake. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-018 came back CONTRADICTED, B-019 came back PARTIAL (`B-018`, `B-019`) |
| `b5` | reworded | The moon-imagery slot corrects three names. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-024 came back CONTRADICTED, B-025 came back CONTRADICTED, B-026 came back CONTRADICTED, B-027 came back CONTRADICTED (`B-024`, `B-025`, `B-026`, `B-027`) |
| `b6` | reworded | The Miranda slot corrects the distance notation and travel duration. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-028 came back CONTRADICTED, B-029 came back CONTRADICTED (`B-028`, `B-029`) |
| `b7` | reworded | The imagery slot describes the same visual contrast more concisely. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-030`) |
| `b8` | subsumed | The imagery slot combines the contrasting appearances. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-031`) |
| `b9` | reworded | The aftermath slot corrects the accident date and death toll. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-032 came back CONTRADICTED, B-033 came back CONTRADICTED, B-034 came back CONTRADICTED (`B-032`, `B-033`, `B-034`) |

## Added from outside the documents

The merge declared 11 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

11 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| After completing its primary encounters with Jupiter and Saturn, Voyager 2 continues to Uranus, a journey of about 4,5 years. | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters | the model's own knowledge | *no source* | Voyager 2, not Voyager 3, flies on from Jupiter and Saturn. | *none* |
| The geometry of its Uranus encounter also preserves the possibility of a later flyby of Neptune. | possibility of a future encounter with Saturn | the model's own knowledge | *no source* | Neptune, not Saturn, is the possible encounter after Uranus. | *none* |
| Voyager 2 is the first human-made object to fly past Uranus. Its short-range observations begin before closest approach, and signals take approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | Voyager 1 never visits Uranus, and the stated date follows the flyby. | *none* |
| Sunlight at Uranus is approximately 400 times weaker than at Earth. | Light conditions were five-hundred times less than terrestrial conditions. | the model's own knowledge | *no source* | Uranus’s solar distance makes sunlight roughly 400 times weaker. | *none* |
| Closest approach occurs at 17:59 UT Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | The flyby is in 1986; the source reverses the distance units. | *none* |
| During the flyby, Voyager 2 discovers 10 new moons—Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca—whose names draw on characters from Shakespeare and Alexander Pope. | 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687) | the model's own knowledge | *no source* | Voyager 2 discovers 10 moons with literary names, not 11. | *none* |
| It also discovers two new rings, bringing the known total to 11, and finds a magnetic field tilted at 59 degrees to the rotation axis and offset from the planet’s center. | three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center | the model's own knowledge | *no source* | The flyby adds two known rings and measures a roughly 59-degree tilt. | *none* |
| Its observations also inform models of Uranus’s deep, water-bearing interior. | found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface | the model's own knowledge | *no source* | The flyby does not establish a boiling lake at a measured depth. | *none* |
| Voyager 2 returns images of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’s moons. | Miranda, Oberon, Ariele, Umbrella, and Titan | the model's own knowledge | *no source* | Ariel, Umbriel, and Titania are Uranian moons; Titan orbits Saturn. | *none* |
| At a range of only 17,560 miles (28,260 kilometers), its flyby of Miranda brings the spacecraft closer to an object than any earlier encounter on its journey. | 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels | the model's own knowledge | *no source* | The distance notation is erroneous, and the spacecraft is not a century old. | *none* |
| News of the Uranus encounter is overshadowed by the Challenger accident on Jan. 28, 1986, which kills seven astronauts during their space shuttle launch. | the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger is lost four days after the flyby, killing seven crew members. | *none* |

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
| Calls | 9 live, 0 cached, 0 replayed |
| Tokens | 24,861 in, 23,070 out, 0 cached, 7,608 reasoning |
| Cost | ~$0.28 estimated (rates read 2026-09-25) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 276.3s |
| Generated | 2026-09-27T17:01:52+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
