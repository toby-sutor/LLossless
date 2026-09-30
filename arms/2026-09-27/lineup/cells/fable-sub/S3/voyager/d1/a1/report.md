## Verdict

**64 finding(s).** In the claims: 50 contradicted, 1 partially invented. In the structure: 13 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 33 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 21 |
| Forward — source claims accounted for in the merge | **6/33** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **0/12** |
| Forward — `source_b.md` claims accounted for | **6/21** |
| Reverse — merge claims found in a source | **9/33** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **66/66** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Voyager 2 and two planetary encounters, not Voyager 3 and three.
- **A-002** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed the Voyager 3 spacecraft to Uranus.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The spacecraft directed to Uranus is Voyager 2, not Voyager 3.
- **A-003** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3's journey to Uranus would take about 4,5 years.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The journey duration matches but the spacecraft is Voyager 2, not Voyager 3.
- **A-004** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The Jupiter encounter optimization is stated for Voyager 2, so the name Voyager 3 is incompatible.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says the future encounter was with Neptune, not Saturn.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its Uranus flyby.
  - `merged.md` says: 'Voyager 2 had only 5.5 hours of close study during its flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives Voyager 2 and 5.5 hours, not Voyager 1 and 6.4 days.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: "The first human-made object to fly past Uranus, Voyager 2's long-range observations" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies Voyager 2, not Voyager 1, as the first human-made object to fly past Uranus.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: "Voyager 2's long-range observations of the planet began Nov. 4, 1985" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states Voyager 2's long-range observations began Nov. 4, 1985, which differs in spacecraft, range type and date.
- **A-009** -- the two documents disagree
  - `source_a.md:9` says: When Voyager 1's short-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth.
  - `merged.md` says: "Voyager 2's long-range observations of the planet began Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The signal time matches but the reference attributes it to Voyager 2's long-range observations, not Voyager 1's short-range ones.
- **A-010** -- the two documents disagree
  - `source_a.md:9` says: Light conditions at Uranus were five-hundred times less than terrestrial conditions.
  - `merged.md` says: 'Light conditions were 400 times less than terrestrial conditions' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 400 times, not five hundred times.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives UT and the year 1986, not ED and 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 50,640 miles (81,500 kilometers)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 50,640 miles and 81,500 kilometers, so the claim swaps the units.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: During its flyby of Uranus, Voyager 2 discovered 11 new moons.
  - `merged.md` says: 'During its flyby, Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The new moons discovered by Voyager 2 at Uranus were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Several of the names in the claim differ from those given in the reference, such as Puck, Portia, Juliet and Cordelia.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The names of the new moons discovered by Voyager 2 at Uranus are allusions to Goethe.
  - `merged.md` says: 'obvious allusions to Shakespeare' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says the names allude to Shakespeare, not Goethe.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for Uranus' moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1787' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference dates the naming tradition to 1787, not 1687.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: During its flyby of Uranus, Voyager 2 discovered three new rings.
  - `merged.md` says: 'two new rings in addition to the “older” nine rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states two new rings, not three.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Uranus had eight rings known before the Voyager 2 flyby.
  - `merged.md` says: 'two new rings in addition to the “older” nine rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states nine previously known rings, not eight.
- **B-007** -- the two documents disagree
  - `source_b.md:3` says: During its flyby of Uranus, Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis.
  - `merged.md` says: 'a magnetic field tilted at 59 degrees off-axis and off-center' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives a tilt of 59 degrees, not 66 degrees.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 450 miles per hour (724 km/h), not 450 km/h or 72400 meters per hour.
- **B-010** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus.
  - `merged.md` says: 'found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states a boiling ocean at 497 miles (800 kilometers), not a lake at 479 miles (900 kilometers).
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Ariel, Umbriel and Titania, not Ariele, Umbrella and Titan.
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons.
  - `merged.md` says: 'Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ larger moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference calls them larger moons and gives different names for three of them.
- **B-016** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2's travels had been nearly century-long at the time of the Miranda flyby.
  - `merged.md` says: 'the spacecraft came closest to any object so far in its nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference describes the travels as nearly decade-long, not nearly century-long.
- **B-019** -- the two documents disagree
  - `source_b.md:9` says: The news of the Voyager 2 Uranus encounter was interrupted the same day by the Challenger accident.
  - `merged.md` says: 'The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says the interruption came the same week, not the same day, with the accident four days after closest approach.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'the tragic Challenger accident that killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states seven astronauts were killed, not six.
- **B-021** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during the space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference dates the launch accident to Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the two planetary encounters.
  - `source_a.md` says: 'had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives three planetary encounters, not two.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: The geometry of Voyager 2's Uranus encounter was defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Saturn as the future encounter, not Neptune.
- **M-006** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had only 5.5 hours of close study during its Uranus flyby.
  - `source_a.md` says: 'had only 6.4 days of close study during its flyby' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 6.4 days of close study, not 5.5 hours.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source text names Voyager 1 as the first human-made object to fly past Uranus, a different name from the claim's Voyager 2.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's long-range observations of Uranus began Nov. 4, 1985.
  - `source_a.md` says: 'short-range observations of the planet began Jan. 31, 1987' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives short-range observations beginning Jan. 31, 1987, not long-range observations beginning Nov. 4, 1985.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: Light conditions at Uranus during Voyager 2's observations were 400 times less than terrestrial conditions.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives five-hundred times less, not 400 times.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach to Uranus took place at 17:59 UT Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the year 1968 and the time zone ED, not 1986 and UT.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach to Uranus was at a range of about 50,640 miles (81,500 kilometers).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attaches the units the other way round, giving 50,640 kilometers and 81,500 miles.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: During its Uranus flyby, Voyager 2 discovered 10 new moons.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 11 new moons, not 10.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: The moons of Uranus discovered by Voyager 2 were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives different names for most of the moons, such as Pucka, Portila and Bianca II.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The names of the moons of Uranus discovered by Voyager 2 are allusions to Shakespeare.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the names allude to Goethe, not Shakespeare.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: The tradition of naming Uranus' moons with allusions to Shakespeare began in 1787.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the tradition to 1687, not 1787, and ties it to Goethe.
- **M-017** -- the two documents disagree
  - `merged.md:7` says: During its Uranus flyby, Voyager 2 discovered two new rings.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives three new rings, not two.
- **M-018** -- the two documents disagree
  - `merged.md:7` says: Nine rings of Uranus were known before Voyager 2's flyby.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives eight previously known rings, not nine.
- **M-019** -- the two documents disagree
  - `merged.md:7` says: During its Uranus flyby, Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives a tilt of 66 degrees, not 59.
- **M-021** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour).
  - `source_b.md` says: 'as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 450 km/h and 72400 meters per hour, not 450 miles per hour and 724 kilometers per hour.
- **M-022** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface of Uranus.
  - `source_b.md` says: 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives a lake at 479 miles (900 kilometers), not an ocean at 497 miles (800 kilometers).
- **M-025** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Ariele, Umbrella and Titan, not Ariel, Umbriel and Titania.
- **M-026** -- the two documents disagree
  - `merged.md:11` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons.
  - `source_b.md` says: 'smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source describes the five as smaller moons, not larger, and gives different names for three of them.
- **M-028** -- the two documents disagree
  - `merged.md:11` says: In flying by Miranda, Voyager 2 came closest to any object so far in its nearly decade-long travels.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says nearly century-long travels, not decade-long.
- **M-031** -- the two documents disagree
  - `merged.md:13` says: The news of Voyager 2's Uranus encounter was interrupted the same week by the Challenger accident.
  - `source_b.md` says: 'was interrupted the same day by the tragic Challenger accident' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the news was interrupted the same day, not the same week.
- **M-032** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident killed seven astronauts.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives six astronauts killed, not seven.
- **M-033** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident occurred during the space shuttle launch on Jan. 28, 1986.
  - `source_b.md` says: 'during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the launch Feb. 28, 1986, not Jan. 28, 1986.

### Partly invented — the sources carry some of this claim

- **M-009** (`merged.md:5`) — When Voyager 2's long-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth.
  - evidence: 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The signal time at the start of observations is stated, but the source calls those observations short-range, not long-range.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 5.5 | 4,5, 2,5 | English (72 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m5` (`merged.md`) - '2,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `m12` (`merged.md`) - '17.560' (merged.md, line 11) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m12` (`merged.md`) - '28.260' (merged.md, line 11) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 12 contradicted, 0 carried in part, 0 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' in `merged.md` -- The reference names Voyager 2 and two planetary encounters, not Voyager 3 and three. |
| 2 | Mission planners directed the Voyager 3 spacecraft to Uranus. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- The spacecraft directed to Uranus is Voyager 2, not Voyager 3. |
| 3 | Voyager 3's journey to Uranus would take about 4,5 years. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years' in `merged.md` -- The journey duration matches but the spacecraft is Voyager 2, not Voyager 3. |
| 4 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' in `merged.md` -- The Jupiter encounter optimization is stated for Voyager 2, so the name Voyager 3 is incompatible. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' in `merged.md` -- The reference says the future encounter was with Neptune, not Saturn. |
| 6 | Voyager 1 had only 6.4 days of close study during its Uranus flyby. | 7 | contradicted | 'Voyager 2 had only 5.5 hours of close study during its flyby' in `merged.md` -- The reference gives Voyager 2 and 5.5 hours, not Voyager 1 and 6.4 days. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | "The first human-made object to fly past Uranus, Voyager 2's long-range observations" in `merged.md` -- The reference identifies Voyager 2, not Voyager 1, as the first human-made object to fly past Uranus. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | "Voyager 2's long-range observations of the planet began Nov. 4, 1985" in `merged.md` -- The reference states Voyager 2's long-range observations began Nov. 4, 1985, which differs in spacecraft, range type and date. |
| 9 | When Voyager 1's short-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth. | 9 | contradicted | "Voyager 2's long-range observations of the planet began Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth" in `merged.md` -- The signal time matches but the reference attributes it to Voyager 2's long-range observations, not Voyager 1's short-range ones. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | contradicted | 'Light conditions were 400 times less than terrestrial conditions' in `merged.md` -- The reference gives 400 times, not five hundred times. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' in `merged.md` -- The reference gives UT and the year 1986, not ED and 1968. |
| 12 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 50,640 miles (81,500 kilometers)' in `merged.md` -- The reference gives 50,640 miles and 81,500 kilometers, so the claim swaps the units. |

### `source_b.md` -- 21 claim(s): 0 dropped, 15 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | During its flyby of Uranus, Voyager 2 discovered 11 new moons. | 3 | contradicted | 'During its flyby, Voyager 2 discovered 10 new moons' in `merged.md` -- The reference states 10 new moons, not 11. |
| 2 | The new moons discovered by Voyager 2 at Uranus were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Several of the names in the claim differ from those given in the reference, such as Puck, Portia, Juliet and Cordelia. |
| 3 | The names of the new moons discovered by Voyager 2 at Uranus are allusions to Goethe. | 3 | contradicted | 'obvious allusions to Shakespeare' in `merged.md` -- The reference says the names allude to Shakespeare, not Goethe. |
| 4 | The naming tradition for Uranus' moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1787' in `merged.md` -- The reference dates the naming tradition to 1787, not 1687. |
| 5 | During its flyby of Uranus, Voyager 2 discovered three new rings. | 3 | contradicted | 'two new rings in addition to the “older” nine rings' in `merged.md` -- The reference states two new rings, not three. |
| 6 | Uranus had eight rings known before the Voyager 2 flyby. | 3 | contradicted | 'two new rings in addition to the “older” nine rings' in `merged.md` -- The reference states nine previously known rings, not eight. |
| 7 | During its flyby of Uranus, Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis. | 3 | contradicted | 'a magnetic field tilted at 59 degrees off-axis and off-center' in `merged.md` -- The reference gives a tilt of 59 degrees, not 66 degrees. |
| 9 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour)' in `merged.md` -- The reference gives 450 miles per hour (724 km/h), not 450 km/h or 72400 meters per hour. |
| 10 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus. | 5 | contradicted | 'found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface' in `merged.md` -- The reference states a boiling ocean at 497 miles (800 kilometers), not a lake at 479 miles (900 kilometers). |
| 12 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The reference names Ariel, Umbriel and Titania, not Ariele, Umbrella and Titan. |
| 13 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 | contradicted | 'Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ larger moons' in `merged.md` -- The reference calls them larger moons and gives different names for three of them. |
| 16 | Voyager 2's travels had been nearly century-long at the time of the Miranda flyby. | 7 | contradicted | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- The reference describes the travels as nearly decade-long, not nearly century-long. |
| 19 | The news of the Voyager 2 Uranus encounter was interrupted the same day by the Challenger accident. | 9 | contradicted | 'The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident' in `merged.md` -- The reference says the interruption came the same week, not the same day, with the accident four days after closest approach. |
| 20 | The Challenger accident killed six astronauts. | 9 | contradicted | 'the tragic Challenger accident that killed seven astronauts' in `merged.md` -- The reference states seven astronauts were killed, not six. |
| 21 | The Challenger accident occurred during the space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The reference dates the launch accident to Jan. 28, 1986, not Feb. 28, 1986. |
| 8 | The magnetic field of Uranus discovered by Voyager 2 is off-center. | 3 | carried | 'a magnetic field tilted at 59 degrees off-axis and off-center' in `merged.md` -- The reference states the magnetic field discovered by Voyager 2 is off-center. |
| 11 | The rings of Uranus were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference states this directly about the rings of Uranus. |
| 14 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- The reference gives the same Miranda flyby range in the same figures. |
| 15 | In flying by Miranda, Voyager 2 came closest to any object so far in its travels. | 7 | carried | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- The reference states that the Miranda flyby was the spacecraft's closest approach to any object so far. |
| 17 | Images of Miranda showed an object whose surface was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- The reference states this about Miranda, referred to as the moon in the sentence following its flyby. |
| 18 | Uranus itself appeared generally featureless to Voyager 2. | 7 | carried | 'Uranus itself appeared generally featureless' in `merged.md` -- The reference states Uranus appeared generally featureless in the context of Voyager 2's observations. |

### `merged.md` -- 33 claim(s): 0 invented, 23 contradicted, 1 supported in part, 9 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with the two planetary encounters. | contradicted | `source_a.md` | 'had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source gives three planetary encounters, not two. |
| 5 | The geometry of Voyager 2's Uranus encounter was defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'defined by the possibility of a future encounter with Saturn' in `source_a.md` -- The source names Saturn as the future encounter, not Neptune. |
| 6 | Voyager 2 had only 5.5 hours of close study during its Uranus flyby. | contradicted | `source_a.md` | 'had only 6.4 days of close study during its flyby' in `source_a.md` -- The source gives 6.4 days of close study, not 5.5 hours. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's" in `source_a.md` -- The source text names Voyager 1 as the first human-made object to fly past Uranus, a different name from the claim's Voyager 2. |
| 8 | Voyager 2's long-range observations of Uranus began Nov. 4, 1985. | contradicted | `source_a.md` | 'short-range observations of the planet began Jan. 31, 1987' in `source_a.md` -- The source gives short-range observations beginning Jan. 31, 1987, not long-range observations beginning Nov. 4, 1985. |
| 10 | Light conditions at Uranus during Voyager 2's observations were 400 times less than terrestrial conditions. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- The source gives five-hundred times less, not 400 times. |
| 11 | Voyager 2's closest approach to Uranus took place at 17:59 UT Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- The source gives the year 1968 and the time zone ED, not 1986 and UT. |
| 12 | Voyager 2's closest approach to Uranus was at a range of about 50,640 miles (81,500 kilometers). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- The source attaches the units the other way round, giving 50,640 kilometers and 81,500 miles. |
| 13 | During its Uranus flyby, Voyager 2 discovered 10 new moons. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- The source gives 11 new moons, not 10. |
| 14 | The moons of Uranus discovered by Voyager 2 were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- The source gives different names for most of the moons, such as Pucka, Portila and Bianca II. |
| 15 | The names of the moons of Uranus discovered by Voyager 2 are allusions to Shakespeare. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- The source says the names allude to Goethe, not Shakespeare. |
| 16 | The tradition of naming Uranus' moons with allusions to Shakespeare began in 1787. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- The source dates the tradition to 1687, not 1787, and ties it to Goethe. |
| 17 | During its Uranus flyby, Voyager 2 discovered two new rings. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source gives three new rings, not two. |
| 18 | Nine rings of Uranus were known before Voyager 2's flyby. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source gives eight previously known rings, not nine. |
| 19 | During its Uranus flyby, Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source gives a tilt of 66 degrees, not 59. |
| 21 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour). | contradicted | `source_b.md` | 'as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives 450 km/h and 72400 meters per hour, not 450 miles per hour and 724 kilometers per hour. |
| 22 | Voyager 2 found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface of Uranus. | contradicted | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- The source gives a lake at 479 miles (900 kilometers), not an ocean at 497 miles (800 kilometers). |
| 25 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source names Ariele, Umbrella and Titan, not Ariel, Umbriel and Titania. |
| 26 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons. | contradicted | `source_b.md` | 'smaller moons' in `source_b.md` -- The source describes the five as smaller moons, not larger, and gives different names for three of them. |
| 28 | In flying by Miranda, Voyager 2 came closest to any object so far in its nearly decade-long travels. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source says nearly century-long travels, not decade-long. |
| 31 | The news of Voyager 2's Uranus encounter was interrupted the same week by the Challenger accident. | contradicted | `source_b.md` | 'was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- The source says the news was interrupted the same day, not the same week. |
| 32 | The Challenger accident killed seven astronauts. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- The source gives six astronauts killed, not seven. |
| 33 | The Challenger accident occurred during the space shuttle launch on Jan. 28, 1986. | contradicted | `source_b.md` | 'during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- The source dates the launch Feb. 28, 1986, not Jan. 28, 1986. |
| 9 | When Voyager 2's long-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth. | supported in part | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- The signal time at the start of observations is stated, but the source calls those observations short-range, not long-range. |
| 2 | Mission planners directed Voyager 2 to Uranus. | supported | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The source states planners directed the spacecraft, the subject of the Voyager 2 document, to Uranus. |
| 3 | Voyager 2's journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- The source gives the same journey duration in the same format. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- The source states this directly. |
| 20 | The magnetic field of Uranus discovered by Voyager 2 is off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source states the magnetic field is off-center. |
| 23 | The rings of Uranus were found to be extremely variable in thickness. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- The source states the rings were extremely variable in thickness. |
| 24 | The rings of Uranus were found to be extremely variable in transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- The source states the rings were extremely variable in transparency. |
| 27 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- The source gives the same range in the same format. |
| 29 | Voyager 2's images of Miranda showed an object whose surface was a mishmash of peculiar features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `source_b.md` -- The source states this about the images of Miranda. |
| 30 | Uranus itself appeared generally featureless to Voyager 2. | supported | `source_b.md` | 'Uranus itself appeared generally featureless' in `source_b.md` -- The source states this directly. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **33** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **33**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 12 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '1' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '6.4' (days) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '66' (degrees) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '479' (miles) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '900' (kilometers) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **11** departure(s) from its sources. Checking them confirms 1, rejects 10, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | duplicate | Title: identical to the base title, stated once. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a2` | reworded | Spacecraft name and encounter count corrected; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back CONTRADICTED, A-003 came back CONTRADICTED (`A-001`, `A-002`, `A-003`) |
| `a4` | reworded | Typo fixed; next planet, spacecraft and duration corrected; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED (`A-005`, `A-006`) |
| `a5` | reworded | Spacecraft, observation type and start date corrected; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED, A-009 came back CONTRADICTED (`A-007`, `A-008`, `A-009`) |
| `a6` | reworded | Light level factor corrected; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-010 came back CONTRADICTED (`A-010`) |
| `a7` | reworded | Time standard, year and swapped distance units corrected; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b2` | reworded | Moon count, names, author, year, ring counts and tilt corrected; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED, B-007 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`, `B-005`, `B-006`, `B-007`) |
| `b3` | reworded | Wind speed units, ocean and depth figures corrected; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-009 came back CONTRADICTED, B-010 came back CONTRADICTED (`B-009`, `B-010`) |
| `b5` | reworded | Moon names and size description corrected; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back CONTRADICTED, B-013 came back CONTRADICTED (`B-012`, `B-013`) |
| `b6` | reworded | Travel duration corrected from century to decade; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-016 came back CONTRADICTED (`B-016`) |
| `b9` | reworded | Challenger date, crew count and timing corrected; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-019 came back CONTRADICTED, B-020 came back CONTRADICTED, B-021 came back CONTRADICTED (`B-019`, `B-020`, `B-021`) |

## Added from outside the documents

The merge declared 17 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. No call the model made took more turns than a call that retrieves nothing can take, so it retrieved nothing and every source here is recalled rather than looked up.

17 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 | the model's own knowledge | *no source* | No Voyager 3 flew; Voyager 2 is the spacecraft that visited Uranus. | *none* |
| Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | the three planetary encounters | the model's own knowledge | *no source* | Before Uranus, Voyager 2 had flown past only Jupiter and Saturn. | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 5.5 hours of close study during its flyby. | a future encounter with Saturn | the model's own knowledge | *no source* | Saturn was already passed in 1981; Neptune followed Uranus in 1989. | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 5.5 hours of close study during its flyby. | Voyager 1 had only 6.4 days of close study | the model's own knowledge | *no source* | Voyager 1 never visited Uranus; NASA's account gives 5.5 hours of close study. | *none* |
| The first human-made object to fly past Uranus, Voyager 2's long-range observations of the planet began Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | Voyager 2 began long-range observation in Nov. 1985, before the 1986 flyby. | *none* |
| Light conditions were 400 times less than terrestrial conditions. | five-hundred times less | the model's own knowledge | *no source* | At about 19 AU sunlight is roughly 1/370 of Earth's; NASA states 400 times. | *none* |
| Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers). | 17:59 ED Jan. 24, 1968 | the model's own knowledge | *no source* | The flyby was on Jan. 24, 1986, timed in UT; Voyager 2 launched in 1977. | *none* |
| Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers). | 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | The units were swapped: 50,640 miles equals about 81,500 kilometers. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II | the model's own knowledge | *no source* | Voyager 2 found 10 moons during the flyby; these are their official names. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | obvious allusions to Goethe, continuing a naming tradition begun in 1687 | the model's own knowledge | *no source* | The names are Shakespearean; the first Uranian moons were found in 1787. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | three new rings in addition to the “older” eight rings | the model's own knowledge | *no source* | Nine rings were known from 1977 occultations; Voyager 2 added two. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | tilted at 66 degrees | the model's own knowledge | *no source* | Uranus' magnetic dipole is tilted about 59 degrees from its rotation axis. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour) and found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface. | 450 km/h (72400 meters per hour) | the model's own knowledge | *no source* | The figure is 450 mph, which converts to 724 km/h; source units are garbled. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour) and found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface. | a boiling lake of water some 479 miles (900 kilometers) | the model's own knowledge | *no source* | NASA describes an ocean 800 km down; 800 km is 497 miles, not 479. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ larger moons. | Ariele, Umbrella, and Titan, five of Uranus’ smaller moons | the model's own knowledge | *no source* | Ariel, Umbriel and Titania are Uranus' moons; these five are its largest. | *none* |
| In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels. | nearly century-long travels | the model's own knowledge | *no source* | Voyager 2 launched in 1977, under nine years before the 1986 flyby. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger was lost Jan. 28, 1986 with seven crew, four days after the flyby. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 640c0f94c750 (command) -- lineup fable-sub |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | fable -> claude-fable-5-1 |
| Model (decompose) | fable -> claude-fable-5-1 |
| Model (verify) | fable -> claude-fable-5-1 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=medium, merge=medium, verify=medium |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 262.4s |
| Generated | 2026-09-28T01:25:32+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content was handed to a program on this machine (`lineup fable-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
