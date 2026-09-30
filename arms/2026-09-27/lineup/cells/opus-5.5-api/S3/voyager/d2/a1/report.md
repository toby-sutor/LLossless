## Verdict

**58 finding(s).** In the claims: 1 partially dropped, 45 contradicted. In the structure: 12 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 34 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 20 |
| Forward — source claims accounted for in the merge | **8/32** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **2/12** |
| Forward — `source_b.md` claims accounted for | **6/20** (1 in part) |
| Reverse — merge claims found in a source | **12/34** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **66/66** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-017** (`source_b.md:7`) — Uranus appeared generally featureless in Voyager 2 images.
  - evidence: 'Uranus itself appeared generally featureless.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: Uranus is said to appear generally featureless, but the text does not explicitly say this was in Voyager 2 images, though the context implies it.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Voyager 2 and two planetary encounters, not Voyager 3 and three.
- **A-002** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The spacecraft directed to Uranus is Voyager 2, not Voyager 3.
- **A-003** -- the two documents disagree
  - `source_a.md:3` says: The journey of Voyager 3 to Uranus would take about 4,5 years.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The 4,5-year journey is attributed to Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The future encounter was with Neptune, not Saturn.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby of Uranus.
  - `merged.md` says: 'Voyager 2 had only 5.5 hours of close study during its flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says Voyager 2 had 5.5 hours, not Voyager 1 with 6.4 days.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'The first human-made object to fly past Uranus, Voyager 2' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The first object to fly past Uranus was Voyager 2, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: 'Voyager 2 began its long-range observations of the planet on Nov. 4, 1985' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives Voyager 2's long-range observations beginning Nov. 4, 1985, not Voyager 1's short-range observations in 1987.
- **A-009** -- the two documents disagree
  - `source_a.md:9` says: When Voyager 1's short-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth.
  - `merged.md` says: 'Voyager 2 began its long-range observations of the planet on Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The 2,5-hour signal time applies to Voyager 2's long-range observations, not Voyager 1's short-range ones.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The year given is 1986, not 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 81,500 kilometers and 50,640 miles, the reverse of the claim's units.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: During its flyby, Voyager 2 discovered 11 new moons at Uranus.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The new moons discovered by Voyager 2 were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Several of the names differ from those in the reference.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The names of the new Uranian moons are allusions to Goethe.
  - `merged.md` says: 'obvious allusions to Shakespeare' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The names allude to Shakespeare, not Goethe.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for Uranian moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1852' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The tradition began in 1852, not 1687.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings at Uranus.
  - `merged.md` says: 'two new rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says two new rings, not three.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Uranus had eight previously known rings before Voyager 2's flyby.
  - `merged.md` says: 'the “older” nine rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says nine older rings, not eight.
- **B-008** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'as high as 450 miles per hour (724 kilometers per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 450 mph (724 km/h), not 450 km/h.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below Uranus' top cloud surface.
  - `merged.md` says: 'found evidence of a boiling ocean of water some 500 miles (800 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says an ocean at 500 miles (800 km), not a lake at 479 miles (900 km).
- **B-011** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The moon names Ariel, Umbriel and Titania differ from those in the claim.
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons.
  - `merged.md` says: 'five of Uranus’ larger moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference calls them larger moons, not smaller, and the names differ.
- **B-015** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2's travels were nearly century-long at the time of the Miranda flyby.
  - `merged.md` says: 'its nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text describes the travels as nearly decade-long, not nearly century-long.
- **B-019** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says seven astronauts were killed, not six.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during the space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text dates the launch to Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the two planetary encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says three planetary encounters, not two, and it names Voyager 3.
- **M-002** -- the two documents disagree
  - `merged.md:3` says: Mission planners directed Voyager 2 to Uranus.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names the spacecraft directed to Uranus as Voyager 3, not Voyager 2.
- **M-005** -- the two documents disagree
  - `merged.md:5` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Saturn, not Neptune.
- **M-006** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 had only 5.5 hours of close study during its Uranus flyby.
  - `source_a.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 6.4 days of close study, not 5.5 hours.
- **M-007** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Voyager 1 as the first human-made object to fly past Uranus.
- **M-008** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 began its long-range observations of Uranus on Nov. 4, 1985.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives short-range observations beginning Jan. 31, 1987, not long-range observations beginning Nov. 4, 1985.
- **M-009** -- the two documents disagree
  - `merged.md:7` says: On Nov. 4, 1985, signals from Voyager 2 took approximately 2,5 hours to reach Earth.
  - `source_a.md` says: 'began Jan. 31, 1987, when signals took approximately 2,5 hours to reach Earth' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source ties the 2,5-hour signal time to Jan. 31, 1987, not Nov. 4, 1985.
- **M-011** -- the two documents disagree
  - `merged.md:7` says: Voyager 2's closest approach to Uranus took place at 17:59 ED Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the year as 1968, not 1986.
- **M-012** -- the two documents disagree
  - `merged.md:7` says: Voyager 2's closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 50,640 kilometers (81,500 miles), which reverses the claim's units.
- **M-013** -- the two documents disagree
  - `merged.md:9` says: During its Uranus flyby, Voyager 2 discovered 10 new moons.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says 11 new moons, not 10.
- **M-014** -- the two documents disagree
  - `merged.md:9` says: The 10 new moons of Uranus discovered by Voyager 2 were given names such as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives different names for the moons.
- **M-015** -- the two documents disagree
  - `merged.md:9` says: The names of the new Uranian moons are allusions to Shakespeare.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the names allude to Goethe, not Shakespeare.
- **M-016** -- the two documents disagree
  - `merged.md:9` says: The Shakespearean naming tradition for Uranian moons began in 1852.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the naming tradition began in 1687, not 1852.
- **M-017** -- the two documents disagree
  - `merged.md:9` says: During its Uranus flyby, Voyager 2 discovered two new rings.
  - `source_b.md` says: 'three new rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says three new rings, not two.
- **M-018** -- the two documents disagree
  - `merged.md:9` says: Uranus had nine previously known rings before Voyager 2's flyby.
  - `source_b.md` says: 'in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says eight previously known rings, not nine.
- **M-021** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour).
  - `source_b.md` says: 'as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 450 km/h, not 450 miles per hour (724 km/h).
- **M-022** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 found evidence of a boiling ocean of water some 500 miles (800 kilometers) below Uranus' top cloud surface.
  - `source_b.md` says: 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says a lake at 479 miles (900 km), not an ocean at 500 miles (800 km).
- **M-025** -- the two documents disagree
  - `merged.md:13` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Ariele, Umbrella and Titan rather than Ariel, Umbriel and Titania.
- **M-026** -- the two documents disagree
  - `merged.md:13` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons.
  - `source_b.md` says: 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Ariele, Umbrella and Titan rather than Ariel, Umbriel and Titania, and calls them smaller moons, not larger ones.
- **M-029** -- the two documents disagree
  - `merged.md:13` says: Voyager 2's travels up to the Miranda flyby were nearly decade-long.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source describes the travels as nearly century-long, not nearly decade-long.
- **M-033** -- the two documents disagree
  - `merged.md:15` says: The Challenger accident killed seven astronauts.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the accident killed six astronauts, not seven.
- **M-034** -- the two documents disagree
  - `merged.md:15` says: The Challenger accident occurred during the space shuttle launch on Jan. 28, 1986.
  - `source_b.md` says: 'during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the launch Feb. 28, 1986, not Jan. 28, 1986.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 5.5 | 4,5, 2,5 | English (74 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m5` (`merged.md`) - '2,5' (merged.md, line 7) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `m12` (`merged.md`) - '17.560' (merged.md, line 13) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m12` (`merged.md`) - '28.260' (merged.md, line 13) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

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
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' in `merged.md` -- The reference names Voyager 2 and two planetary encounters, not Voyager 3 and three. |
| 2 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- The spacecraft directed to Uranus is Voyager 2, not Voyager 3. |
| 3 | The journey of Voyager 3 to Uranus would take about 4,5 years. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years' in `merged.md` -- The 4,5-year journey is attributed to Voyager 2, not Voyager 3. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' in `merged.md` -- The future encounter was with Neptune, not Saturn. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby of Uranus. | 7 | contradicted | 'Voyager 2 had only 5.5 hours of close study during its flyby' in `merged.md` -- The reference says Voyager 2 had 5.5 hours, not Voyager 1 with 6.4 days. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'The first human-made object to fly past Uranus, Voyager 2' in `merged.md` -- The first object to fly past Uranus was Voyager 2, not Voyager 1. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | 'Voyager 2 began its long-range observations of the planet on Nov. 4, 1985' in `merged.md` -- The reference gives Voyager 2's long-range observations beginning Nov. 4, 1985, not Voyager 1's short-range observations in 1987. |
| 9 | When Voyager 1's short-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth. | 9 | contradicted | 'Voyager 2 began its long-range observations of the planet on Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth' in `merged.md` -- The 2,5-hour signal time applies to Voyager 2's long-range observations, not Voyager 1's short-range ones. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' in `merged.md` -- The year given is 1986, not 1968. |
| 12 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The reference gives 81,500 kilometers and 50,640 miles, the reverse of the claim's units. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- The reference states this directly. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions' in `merged.md` -- The reference states this directly. |

### `source_b.md` -- 20 claim(s): 0 dropped, 13 contradicted, 1 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | During its flyby, Voyager 2 discovered 11 new moons at Uranus. | 3 | contradicted | 'Voyager 2 discovered 10 new moons' in `merged.md` -- The reference says 10 new moons, not 11. |
| 2 | The new moons discovered by Voyager 2 were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Several of the names differ from those in the reference. |
| 3 | The names of the new Uranian moons are allusions to Goethe. | 3 | contradicted | 'obvious allusions to Shakespeare' in `merged.md` -- The names allude to Shakespeare, not Goethe. |
| 4 | The naming tradition for Uranian moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1852' in `merged.md` -- The tradition began in 1852, not 1687. |
| 5 | Voyager 2 discovered three new rings at Uranus. | 3 | contradicted | 'two new rings' in `merged.md` -- The reference says two new rings, not three. |
| 6 | Uranus had eight previously known rings before Voyager 2's flyby. | 3 | contradicted | 'the “older” nine rings' in `merged.md` -- The reference says nine older rings, not eight. |
| 8 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'as high as 450 miles per hour (724 kilometers per hour)' in `merged.md` -- The reference gives 450 mph (724 km/h), not 450 km/h. |
| 9 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below Uranus' top cloud surface. | 5 | contradicted | 'found evidence of a boiling ocean of water some 500 miles (800 kilometers) below the top cloud surface' in `merged.md` -- The reference says an ocean at 500 miles (800 km), not a lake at 479 miles (900 km). |
| 11 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The moon names Ariel, Umbriel and Titania differ from those in the claim. |
| 12 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 | contradicted | 'five of Uranus’ larger moons' in `merged.md` -- The reference calls them larger moons, not smaller, and the names differ. |
| 15 | Voyager 2's travels were nearly century-long at the time of the Miranda flyby. | 7 | contradicted | 'its nearly decade-long travels' in `merged.md` -- The text describes the travels as nearly decade-long, not nearly century-long. |
| 19 | The Challenger accident killed six astronauts. | 9 | contradicted | 'killed seven astronauts' in `merged.md` -- The text says seven astronauts were killed, not six. |
| 20 | The Challenger accident occurred during the space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The text dates the launch to Jan. 28, 1986, not Feb. 28, 1986. |
| 17 | Uranus appeared generally featureless in Voyager 2 images. | 7 | carried in part | 'Uranus itself appeared generally featureless.' in `merged.md` -- Uranus is said to appear generally featureless, but the text does not explicitly say this was in Voyager 2 images, though the context implies it. |
| 7 | Voyager 2 discovered that Uranus has a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- The reference states this as a Voyager 2 discovery. |
| 10 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference states this directly. |
| 13 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- The reference states this directly. |
| 14 | Voyager 2's flyby of Miranda was the closest it came to any object so far in its travels. | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- The text states that the Miranda flyby was the closest the spacecraft came to any object so far in its travels. |
| 16 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- The text states that images of Miranda showed a surface that was a mishmash of peculiar features. |
| 18 | The news of Voyager 2's Uranus encounter was interrupted the same day by the Challenger accident. | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `merged.md` -- The text states that the news of the Uranus encounter was interrupted the same day by the Challenger accident. |

### `merged.md` -- 34 claim(s): 0 invented, 22 contradicted, 0 supported in part, 12 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with the two planetary encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source says three planetary encounters, not two, and it names Voyager 3. |
| 2 | Mission planners directed Voyager 2 to Uranus. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The source names the spacecraft directed to Uranus as Voyager 3, not Voyager 2. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- The source names Saturn, not Neptune. |
| 6 | Voyager 2 had only 5.5 hours of close study during its Uranus flyby. | contradicted | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- The source gives 6.4 days of close study, not 5.5 hours. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's" in `source_a.md` -- The source names Voyager 1 as the first human-made object to fly past Uranus. |
| 8 | Voyager 2 began its long-range observations of Uranus on Nov. 4, 1985. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- The source gives short-range observations beginning Jan. 31, 1987, not long-range observations beginning Nov. 4, 1985. |
| 9 | On Nov. 4, 1985, signals from Voyager 2 took approximately 2,5 hours to reach Earth. | contradicted | `source_a.md` | 'began Jan. 31, 1987, when signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- The source ties the 2,5-hour signal time to Jan. 31, 1987, not Nov. 4, 1985. |
| 11 | Voyager 2's closest approach to Uranus took place at 17:59 ED Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- The source gives the year as 1968, not 1986. |
| 12 | Voyager 2's closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- The source gives 50,640 kilometers (81,500 miles), which reverses the claim's units. |
| 13 | During its Uranus flyby, Voyager 2 discovered 10 new moons. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- The source says 11 new moons, not 10. |
| 14 | The 10 new moons of Uranus discovered by Voyager 2 were given names such as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- The source gives different names for the moons. |
| 15 | The names of the new Uranian moons are allusions to Shakespeare. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- The source says the names allude to Goethe, not Shakespeare. |
| 16 | The Shakespearean naming tradition for Uranian moons began in 1852. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- The source says the naming tradition began in 1687, not 1852. |
| 17 | During its Uranus flyby, Voyager 2 discovered two new rings. | contradicted | `source_b.md` | 'three new rings' in `source_b.md` -- The source says three new rings, not two. |
| 18 | Uranus had nine previously known rings before Voyager 2's flyby. | contradicted | `source_b.md` | 'in addition to the “older” eight rings' in `source_b.md` -- The source says eight previously known rings, not nine. |
| 21 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour). | contradicted | `source_b.md` | 'as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives 450 km/h, not 450 miles per hour (724 km/h). |
| 22 | Voyager 2 found evidence of a boiling ocean of water some 500 miles (800 kilometers) below Uranus' top cloud surface. | contradicted | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- The source says a lake at 479 miles (900 km), not an ocean at 500 miles (800 km). |
| 25 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source names Ariele, Umbrella and Titan rather than Ariel, Umbriel and Titania. |
| 26 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons. | contradicted | `source_b.md` | 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' in `source_b.md` -- The source names Ariele, Umbrella and Titan rather than Ariel, Umbriel and Titania, and calls them smaller moons, not larger ones. |
| 29 | Voyager 2's travels up to the Miranda flyby were nearly decade-long. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source describes the travels as nearly century-long, not nearly decade-long. |
| 33 | The Challenger accident killed seven astronauts. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- The source says the accident killed six astronauts, not seven. |
| 34 | The Challenger accident occurred during the space shuttle launch on Jan. 28, 1986. | contradicted | `source_b.md` | 'during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- The source dates the launch Feb. 28, 1986, not Jan. 28, 1986. |
| 3 | The journey of Voyager 2 to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- The source states that the journey to Uranus would take about 4,5 years. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- The source states this directly for the spacecraft. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- The source states this verbatim. |
| 19 | Voyager 2 discovered that Uranus has a magnetic field tilted at 66 degrees off-axis. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source states that the magnetic field is tilted at 66 degrees off-axis. |
| 20 | Voyager 2 discovered that Uranus' magnetic field is off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source states that the magnetic field is off-center. |
| 23 | Uranus' rings were found to be extremely variable in thickness. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states that the rings are extremely variable in thickness. |
| 24 | Uranus' rings were found to be extremely variable in transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states that the rings are extremely variable in transparency. |
| 27 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- The source states the Miranda flyby range exactly as the claim gives it. |
| 28 | Voyager 2's Miranda flyby was the closest it had come to any object so far in its travels. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source states that the Miranda flyby was the closest approach to any object so far in its travels. |
| 30 | Images of Miranda showed a surface that was a mishmash of peculiar features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `source_b.md` -- The source states that images of Miranda showed a surface that was a mishmash of peculiar features. |
| 31 | Uranus appeared generally featureless in Voyager 2 images. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- The source states that Uranus appeared generally featureless in the returned photos. |
| 32 | The news of the Uranus encounter was interrupted the same day by the Challenger accident. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- The source states that the news was interrupted the same day by the Challenger accident. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **34** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **32**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 14 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

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
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '479' (miles) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '900' (kilometers) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **10** departure(s) from its sources. Checking them confirms 1, rejects 9, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | duplicate | Identical title already carried from the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a2` | reworded | Corrected spacecraft name and number of prior encounters. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back CONTRADICTED, A-003 came back CONTRADICTED (`A-001`, `A-002`, `A-003`) |
| `a4` | reworded | Fixed typo; corrected next planet, spacecraft and close-study time. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED (`A-005`, `A-006`) |
| `a5` | reworded | Corrected spacecraft, observation type and start date. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED, A-009 came back CONTRADICTED (`A-007`, `A-008`, `A-009`) |
| `a7` | reworded | Corrected year and swapped distance units. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b2` | reworded | Corrected moon count, names, author, tradition year and ring counts. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`, `B-005`, `B-006`) |
| `b3` | reworded | Corrected inconsistent wind and depth figures; lake to ocean. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED, B-009 came back CONTRADICTED (`B-008`, `B-009`) |
| `b5` | reworded | Corrected moon names and smaller to larger. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-011 came back CONTRADICTED, B-012 came back CONTRADICTED (`B-011`, `B-012`) |
| `b6` | reworded | Corrected century-long to decade-long. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-015 came back CONTRADICTED (`B-015`) |
| `b9` | reworded | Corrected Challenger death toll and date. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-019 came back CONTRADICTED, B-020 came back CONTRADICTED (`B-019`, `B-020`) |

## Added from outside the documents

The merge declared 9 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

9 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters | the model's own knowledge | *no source* | No Voyager 3 exists; primary mission was Jupiter and Saturn only. | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 5.5 hours of close study during its flyby. | a future encounter with Saturn: Voyager 1 had only 6.4 days of close study | the model's own knowledge | *no source* | Saturn preceded Uranus; Neptune followed; Voyager 1 never visited Uranus. | *none* |
| The first human-made object to fly past Uranus, Voyager 2 began its long-range observations of the planet on Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | 1987 is after the Jan. 1986 flyby; observations began Nov. 1985. | *none* |
| Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | Voyager launched 1977; flyby was 1986 at 81,500 km, units were swapped. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1852), two new rings in addition to the “older” nine rings | 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings | the model's own knowledge | *no source* | Standard Voyager 2 Uranus results; names are Shakespearean, Uranus found 1781. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour) and found evidence of a boiling ocean of water some 500 miles (800 kilometers) below the top cloud surface. | 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) | the model's own knowledge | *no source* | Source unit pairs are internally inconsistent; NASA figures are these. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ larger moons. | Ariele, Umbrella, and Titan, five of Uranus’ smaller moons | the model's own knowledge | *no source* | These are the five major Uranian moons; Titan orbits Saturn. | *none* |
| In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels. | nearly century-long travels | the model's own knowledge | *no source* | Launched 1977, flyby 1986: under ten years. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger broke up Jan. 28, 1986 with a crew of seven. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | 32,473 in, 25,787 out |
| Cost | ~$0.65 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 202.0s |
| Generated | 2026-09-27T19:33:33+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
