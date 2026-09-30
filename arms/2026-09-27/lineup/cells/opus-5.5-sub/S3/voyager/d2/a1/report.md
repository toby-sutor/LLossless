## Verdict

**59 finding(s).** In the claims: 46 contradicted, 1 hallucinated. In the structure: 12 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 34 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 22 |
| Forward — source claims accounted for in the merge | **10/34** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **1/12** |
| Forward — `source_b.md` claims accounted for | **9/22** |
| Reverse — merge claims found in a source | **11/34** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **67/67** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Voyager 2 and two planetary encounters, not Voyager 3 and three encounters.
- **A-002** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The spacecraft directed to Uranus is Voyager 2, not Voyager 3.
- **A-003** -- the two documents disagree
  - `source_a.md:3` says: The journey of Voyager 3 to Uranus would take about 4,5 years.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The 4,5-year journey matches, but it was made by Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The future encounter was with Neptune, not Saturn.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby.
  - `merged.md` says: 'Voyager 2 had only 5.5 hours of close study during its flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives Voyager 2 with 5.5 hours, not Voyager 1 with 6.4 days.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'The first human-made object to fly past Uranus, Voyager 2' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The first object to fly past Uranus was Voyager 2, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: 'Voyager 2 began its long-range observations of the planet on Nov. 4, 1985' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives Voyager 2's long-range observations beginning Nov. 4, 1985, not Voyager 1's short-range observations on Jan. 31, 1987.
- **A-009** -- the two documents disagree
  - `source_a.md:9` says: When Voyager 1's short-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth.
  - `merged.md` says: 'Voyager 2 began its long-range observations of the planet on Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The 2,5-hour signal time applies to Voyager 2's long-range observations, not Voyager 1's short-range observations.
- **A-010** -- the two documents disagree
  - `source_a.md:9` says: Light conditions at Uranus were five-hundred times less than terrestrial conditions.
  - `merged.md` says: 'Light conditions were 400 times less than terrestrial conditions' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 400 times, not five hundred times.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives UT and 1986, not ED and 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 81,500 kilometers (50,640 miles); the claim swaps the units.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby of Uranus.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The new moons discovered by Voyager 2 at Uranus were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Several names differ, such as Puck vs Pucka, Portia vs Portila and Bianca vs Bianca II.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The names of the new Uranian moons discovered by Voyager 2 are allusions to Goethe.
  - `merged.md` says: 'obvious allusions to Shakespeare' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The names allude to Shakespeare, not Goethe.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for Uranus' moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1852' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The tradition began in 1852, not 1687.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings of Uranus during its flyby.
  - `merged.md` says: 'two new rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives two new rings, not three.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Uranus had eight previously known rings before Voyager 2's flyby.
  - `merged.md` says: 'in addition to the “older” nine rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives nine older rings, not eight.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'wind speeds in Uranus’ atmosphere as high as 724 km/h (450 mph)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 724 km/h (450 mph), not 450 km/h.
- **B-010** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus.
  - `merged.md` says: 'evidence of a boiling ocean of water some 800 kilometers (497 miles) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives an ocean at 800 kilometers (497 miles), not a lake at 479 miles (900 kilometers).
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The moons are named Ariel, Umbriel and Titania, not Ariele, Umbrella and Titan.
- **B-014** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons.
  - `merged.md` says: 'five of Uranus’ larger moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference describes them as larger moons, not smaller, and the names differ.
- **B-017** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2's travels had lasted nearly a century at the time of the Miranda flyby.
  - `merged.md` says: 'its nearly nine-year travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The travels had lasted nearly nine years, not nearly a century.
- **B-021** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says seven astronauts were killed, not six.
- **B-022** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during the space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The launch was Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the two planetary encounters before being directed to Uranus.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the primary mission goals were fulfilled with three planetary encounters, not two.
- **M-002** -- the two documents disagree
  - `merged.md:3` says: Mission planners directed Voyager 2 to Uranus.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names the spacecraft directed to Uranus as Voyager 3, a different name from the claim's Voyager 2.
- **M-005** -- the two documents disagree
  - `merged.md:5` says: The geometry of Voyager 2's Uranus encounter was defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the future encounter was with Saturn, not Neptune.
- **M-006** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 had only 5.5 hours of close study during its Uranus flyby.
  - `source_a.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 6.4 days of close study, not 5.5 hours.
- **M-007** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies the first human-made object to fly past Uranus as Voyager 1, not Voyager 2.
- **M-009** -- the two documents disagree
  - `merged.md:7` says: On Nov. 4, 1985, signals from Voyager 2 took approximately 2,5 hours to reach Earth.
  - `source_a.md` says: 'began Jan. 31, 1987, when signals took approximately 2,5 hours to reach Earth' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source ties the 2,5-hour signal time to Jan. 31, 1987, not Nov. 4, 1985.
- **M-010** -- the two documents disagree
  - `merged.md:7` says: Light conditions at Uranus were 400 times less than terrestrial conditions.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says five-hundred times less, not 400 times.
- **M-011** -- the two documents disagree
  - `merged.md:7` says: Voyager 2's closest approach to Uranus took place at 17:59 UT Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 17:59 ED on Jan. 24, 1968, which differs from the claim's time zone (UT) and year (1986).
- **M-012** -- the two documents disagree
  - `merged.md:7` says: Voyager 2's closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 50,640 kilometers (81,500 miles), with the units reversed relative to the claim.
- **M-013** -- the two documents disagree
  - `merged.md:9` says: During its Uranus flyby, Voyager 2 discovered 10 new moons.
  - `source_b.md` says: 'During its flyby, Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says 11 new moons, not 10.
- **M-014** -- the two documents disagree
  - `merged.md:9` says: The 10 new moons of Uranus discovered by Voyager 2 were given names such as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives different names (e.g. Pucka, Portila, Juliette, Bianca II), and the count differs as well.
- **M-015** -- the two documents disagree
  - `merged.md:9` says: The names of the new Uranian moons discovered by Voyager 2 are allusions to Shakespeare.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the names allude to Goethe, not Shakespeare.
- **M-016** -- the two documents disagree
  - `merged.md:9` says: The Shakespearean naming tradition for Uranus' moons began in 1852.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the naming tradition to 1687, not 1852.
- **M-017** -- the two documents disagree
  - `merged.md:9` says: During its Uranus flyby, Voyager 2 discovered two new rings.
  - `source_b.md` says: 'three new rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says three new rings, not two.
- **M-018** -- the two documents disagree
  - `merged.md:9` says: Before Voyager 2's flyby, nine rings of Uranus were known.
  - `source_b.md` says: 'in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says eight older rings, not nine.
- **M-021** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 724 km/h (450 mph).
  - `source_b.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 450 km/h, not 724 km/h (450 mph).
- **M-022** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 found evidence of a boiling ocean of water some 800 kilometers (497 miles) below Uranus' top cloud surface.
  - `source_b.md` says: 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says a boiling lake at 479 miles (900 kilometers), not an ocean at 800 kilometers (497 miles).
- **M-025** -- the two documents disagree
  - `merged.md:13` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Ariele, Umbrella and Titan rather than Ariel, Umbriel and Titania.
- **M-026** -- the two documents disagree
  - `merged.md:13` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons.
  - `source_b.md` says: 'five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source calls them Uranus' smaller moons, not larger.
- **M-029** -- the two documents disagree
  - `merged.md:13` says: At the time of the Miranda flyby, Voyager 2 had been travelling for nearly nine years.
  - `source_b.md` says: 'its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source describes the travels as nearly century-long, not nearly nine years.
- **M-033** -- the two documents disagree
  - `merged.md:15` says: The Challenger accident killed seven astronauts.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says six astronauts were killed, not seven.
- **M-034** -- the two documents disagree
  - `merged.md:15` says: The Challenger accident occurred during the space shuttle launch on Jan. 28, 1986.
  - `source_b.md` says: 'during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the launch to Feb. 28, 1986, not Jan. 28, 1986.

### Invented — in the merge, in neither source

- **M-008** (`merged.md:7`) — Voyager 2 began its long-range observations of Uranus on Nov. 4, 1985.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: No source mentions long-range observations or the date Nov. 4, 1985; the source gives only a start date for short-range observations.

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

### `source_a.md` -- 12 claim(s): 0 dropped, 11 contradicted, 0 carried in part, 1 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' in `merged.md` -- The reference names Voyager 2 and two planetary encounters, not Voyager 3 and three encounters. |
| 2 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- The spacecraft directed to Uranus is Voyager 2, not Voyager 3. |
| 3 | The journey of Voyager 3 to Uranus would take about 4,5 years. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.' in `merged.md` -- The 4,5-year journey matches, but it was made by Voyager 2, not Voyager 3. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' in `merged.md` -- The future encounter was with Neptune, not Saturn. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | contradicted | 'Voyager 2 had only 5.5 hours of close study during its flyby' in `merged.md` -- The reference gives Voyager 2 with 5.5 hours, not Voyager 1 with 6.4 days. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'The first human-made object to fly past Uranus, Voyager 2' in `merged.md` -- The first object to fly past Uranus was Voyager 2, not Voyager 1. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | 'Voyager 2 began its long-range observations of the planet on Nov. 4, 1985' in `merged.md` -- The reference gives Voyager 2's long-range observations beginning Nov. 4, 1985, not Voyager 1's short-range observations on Jan. 31, 1987. |
| 9 | When Voyager 1's short-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth. | 9 | contradicted | 'Voyager 2 began its long-range observations of the planet on Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth' in `merged.md` -- The 2,5-hour signal time applies to Voyager 2's long-range observations, not Voyager 1's short-range observations. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | contradicted | 'Light conditions were 400 times less than terrestrial conditions' in `merged.md` -- The reference gives 400 times, not five hundred times. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' in `merged.md` -- The reference gives UT and 1986, not ED and 1968. |
| 12 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The reference gives 81,500 kilometers (50,640 miles); the claim swaps the units. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- The reference states this directly. |

### `source_b.md` -- 22 claim(s): 0 dropped, 13 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 2 discovered 11 new moons during its flyby of Uranus. | 3 | contradicted | 'Voyager 2 discovered 10 new moons' in `merged.md` -- The reference gives 10 new moons, not 11. |
| 2 | The new moons discovered by Voyager 2 at Uranus were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Several names differ, such as Puck vs Pucka, Portia vs Portila and Bianca vs Bianca II. |
| 3 | The names of the new Uranian moons discovered by Voyager 2 are allusions to Goethe. | 3 | contradicted | 'obvious allusions to Shakespeare' in `merged.md` -- The names allude to Shakespeare, not Goethe. |
| 4 | The naming tradition for Uranus' moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1852' in `merged.md` -- The tradition began in 1852, not 1687. |
| 5 | Voyager 2 discovered three new rings of Uranus during its flyby. | 3 | contradicted | 'two new rings' in `merged.md` -- The reference gives two new rings, not three. |
| 6 | Uranus had eight previously known rings before Voyager 2's flyby. | 3 | contradicted | 'in addition to the “older” nine rings' in `merged.md` -- The reference gives nine older rings, not eight. |
| 9 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'wind speeds in Uranus’ atmosphere as high as 724 km/h (450 mph)' in `merged.md` -- The reference gives 724 km/h (450 mph), not 450 km/h. |
| 10 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus. | 5 | contradicted | 'evidence of a boiling ocean of water some 800 kilometers (497 miles) below the top cloud surface' in `merged.md` -- The reference gives an ocean at 800 kilometers (497 miles), not a lake at 479 miles (900 kilometers). |
| 13 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The moons are named Ariel, Umbriel and Titania, not Ariele, Umbrella and Titan. |
| 14 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 | contradicted | 'five of Uranus’ larger moons' in `merged.md` -- The reference describes them as larger moons, not smaller, and the names differ. |
| 17 | Voyager 2's travels had lasted nearly a century at the time of the Miranda flyby. | 7 | contradicted | 'its nearly nine-year travels' in `merged.md` -- The travels had lasted nearly nine years, not nearly a century. |
| 21 | The Challenger accident killed six astronauts. | 9 | contradicted | 'killed seven astronauts' in `merged.md` -- The reference says seven astronauts were killed, not six. |
| 22 | The Challenger accident occurred during the space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The launch was Jan. 28, 1986, not Feb. 28, 1986. |
| 7 | Voyager 2 discovered that Uranus has a magnetic field tilted at 66 degrees off-axis. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- The reference lists this among Voyager 2's flyby discoveries. |
| 8 | Voyager 2 discovered that Uranus' magnetic field is off-center. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- The reference states that the discovered magnetic field is off-center. |
| 11 | Uranus' rings were found by Voyager 2 to be extremely variable in thickness. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference states the rings were extremely variable in thickness. |
| 12 | Uranus' rings were found by Voyager 2 to be extremely variable in transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference states the rings were extremely variable in transparency. |
| 15 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- The reference states this range verbatim. |
| 16 | Voyager 2's flyby of Miranda was the closest Voyager 2 had come to any object so far in its travels. | 7 | carried | 'the spacecraft came closest to any object so far' in `merged.md` -- The reference states the Miranda flyby was the closest approach to any object so far. |
| 18 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- The reference states this about images of Miranda. |
| 19 | Uranus appeared generally featureless in Voyager 2's images. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- The reference states this in the context of Voyager 2's returned photos. |
| 20 | The news of Voyager 2's Uranus encounter was interrupted the same day by the Challenger accident. | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `merged.md` -- The reference states this directly. |

### `merged.md` -- 34 claim(s): 1 invented, 22 contradicted, 0 supported in part, 11 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 8 | Voyager 2 began its long-range observations of Uranus on Nov. 4, 1985. | invented | -- | No source mentions long-range observations or the date Nov. 4, 1985; the source gives only a start date for short-range observations. |
| 1 | Voyager 2 had fulfilled its primary mission goals with the two planetary encounters before being directed to Uranus. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source says the primary mission goals were fulfilled with three planetary encounters, not two. |
| 2 | Mission planners directed Voyager 2 to Uranus. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The source names the spacecraft directed to Uranus as Voyager 3, a different name from the claim's Voyager 2. |
| 5 | The geometry of Voyager 2's Uranus encounter was defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- The source says the future encounter was with Saturn, not Neptune. |
| 6 | Voyager 2 had only 5.5 hours of close study during its Uranus flyby. | contradicted | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- The source gives 6.4 days of close study, not 5.5 hours. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations" in `source_a.md` -- The source identifies the first human-made object to fly past Uranus as Voyager 1, not Voyager 2. |
| 9 | On Nov. 4, 1985, signals from Voyager 2 took approximately 2,5 hours to reach Earth. | contradicted | `source_a.md` | 'began Jan. 31, 1987, when signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- The source ties the 2,5-hour signal time to Jan. 31, 1987, not Nov. 4, 1985. |
| 10 | Light conditions at Uranus were 400 times less than terrestrial conditions. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- The source says five-hundred times less, not 400 times. |
| 11 | Voyager 2's closest approach to Uranus took place at 17:59 UT Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- The source gives 17:59 ED on Jan. 24, 1968, which differs from the claim's time zone (UT) and year (1986). |
| 12 | Voyager 2's closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- The source gives 50,640 kilometers (81,500 miles), with the units reversed relative to the claim. |
| 13 | During its Uranus flyby, Voyager 2 discovered 10 new moons. | contradicted | `source_b.md` | 'During its flyby, Voyager 2 discovered 11 new moons' in `source_b.md` -- The source says 11 new moons, not 10. |
| 14 | The 10 new moons of Uranus discovered by Voyager 2 were given names such as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- The source gives different names (e.g. Pucka, Portila, Juliette, Bianca II), and the count differs as well. |
| 15 | The names of the new Uranian moons discovered by Voyager 2 are allusions to Shakespeare. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- The source says the names allude to Goethe, not Shakespeare. |
| 16 | The Shakespearean naming tradition for Uranus' moons began in 1852. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- The source dates the naming tradition to 1687, not 1852. |
| 17 | During its Uranus flyby, Voyager 2 discovered two new rings. | contradicted | `source_b.md` | 'three new rings' in `source_b.md` -- The source says three new rings, not two. |
| 18 | Before Voyager 2's flyby, nine rings of Uranus were known. | contradicted | `source_b.md` | 'in addition to the “older” eight rings' in `source_b.md` -- The source says eight older rings, not nine. |
| 21 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 724 km/h (450 mph). | contradicted | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives 450 km/h, not 724 km/h (450 mph). |
| 22 | Voyager 2 found evidence of a boiling ocean of water some 800 kilometers (497 miles) below Uranus' top cloud surface. | contradicted | `source_b.md` | 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- The source says a boiling lake at 479 miles (900 kilometers), not an ocean at 800 kilometers (497 miles). |
| 25 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source names Ariele, Umbrella and Titan rather than Ariel, Umbriel and Titania. |
| 26 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons. | contradicted | `source_b.md` | 'five of Uranus’ smaller moons' in `source_b.md` -- The source calls them Uranus' smaller moons, not larger. |
| 29 | At the time of the Miranda flyby, Voyager 2 had been travelling for nearly nine years. | contradicted | `source_b.md` | 'its nearly century-long travels' in `source_b.md` -- The source describes the travels as nearly century-long, not nearly nine years. |
| 33 | The Challenger accident killed seven astronauts. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- The source says six astronauts were killed, not seven. |
| 34 | The Challenger accident occurred during the space shuttle launch on Jan. 28, 1986. | contradicted | `source_b.md` | 'during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- The source dates the launch to Feb. 28, 1986, not Jan. 28, 1986. |
| 3 | The journey of Voyager 2 to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- The source states the journey to Uranus would take about 4,5 years. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- The source states this directly. |
| 19 | During its flyby, Voyager 2 discovered that Uranus has a magnetic field tilted at 66 degrees off-axis. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis' in `source_b.md` -- The source states the magnetic field is tilted at 66 degrees off-axis. |
| 20 | Uranus' magnetic field is off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source states the magnetic field is off-center. |
| 23 | Uranus' rings were found to be extremely variable in thickness. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states the rings were extremely variable in thickness. |
| 24 | Uranus' rings were found to be extremely variable in transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states the rings were extremely variable in transparency. |
| 27 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- The source gives the same range for the Miranda flyby. |
| 28 | In flying by Miranda, Voyager 2 came closest to any object so far in its travels. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source states that the Miranda flyby was the closest approach to any object so far. |
| 30 | Images of Miranda showed a surface that was a mishmash of peculiar features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `source_b.md` -- The source states that images showed Miranda's surface as a mishmash of peculiar features. |
| 31 | Uranus appeared generally featureless in Voyager 2 images. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- The source states that Uranus appeared generally featureless. |
| 32 | The news of the Uranus encounter was interrupted the same day by the Challenger accident. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- The source states this directly. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **34** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **34**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

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

The merge declared **11** departure(s) from its sources. Checking them confirms 0, rejects 10, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Corrected spacecraft name and encounter count. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back CONTRADICTED, A-003 came back CONTRADICTED (`A-001`, `A-002`, `A-003`) |
| `a4` | reworded | Fixed 'Ur anus' typo; corrected next target, spacecraft and study time. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED (`A-005`, `A-006`) |
| `a5` | reworded | Corrected spacecraft, observation type and start date. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED, A-009 came back CONTRADICTED (`A-007`, `A-008`, `A-009`) |
| `a6` | reworded | Corrected light-level factor. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-010 came back CONTRADICTED (`A-010`) |
| `a7` | reworded | Corrected time zone, year and swapped distance units. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | superseded | Identical title; the base document's copy is used. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Corrected moon count, names, author, tradition year and ring counts. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`, `B-005`, `B-006`) |
| `b3` | reworded | Corrected wind speed, 'lake' to ocean, and depth figures. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-009 came back CONTRADICTED, B-010 came back CONTRADICTED (`B-009`, `B-010`) |
| `b5` | reworded | Corrected moon names and 'smaller' to larger. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-013 came back CONTRADICTED, B-014 came back CONTRADICTED (`B-013`, `B-014`) |
| `b6` | reworded | Corrected mission duration. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-017 came back CONTRADICTED (`B-017`) |
| `b9` | reworded | Corrected crew count and accident date. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-021 came back CONTRADICTED, B-022 came back CONTRADICTED (`B-021`, `B-022`) |

## Added from outside the documents

The merge declared 12 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. No call the model made took more turns than a call that retrieves nothing can take, so it retrieved nothing and every source here is recalled rather than looked up.

12 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters | the model's own knowledge | *no source* | No Voyager 3 flew; Voyager 2's prior encounters were Jupiter and Saturn | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 5.5 hours of close study during its flyby. | future encounter with Saturn: Voyager 1 had only 6.4 days | the model's own knowledge | *no source* | Saturn preceded Uranus; Neptune followed; close study was about 5.5 hours | *none* |
| The first human-made object to fly past Uranus, Voyager 2 began its long-range observations of the planet on Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | Jan. 31, 1987 postdates the 1986 flyby; observations began Nov. 4, 1985 | *none* |
| Light conditions were 400 times less than terrestrial conditions. | five-hundred times less | the model's own knowledge | *no source* | Uranus at ~19 AU gets roughly 1/370 of Earth's sunlight; NASA cites 400 | *none* |
| Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | Flyby was in 1986 (UT); 81,500 km equals 50,640 miles, not the reverse | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1852), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 66 degrees off-axis and off-center. | 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe | the model's own knowledge | *no source* | Ten moons were found, named for Shakespeare characters; the list names ten | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1852), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 66 degrees off-axis and off-center. | begun in 1687 | the model's own knowledge | *no source* | Uranus was found in 1781; John Herschel named its moons in 1852 | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1852), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 66 degrees off-axis and off-center. | three new rings in addition to the “older” eight rings | the model's own knowledge | *no source* | Nine rings were known from 1977; Voyager 2 added two | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 724 km/h (450 mph) and evidence of a boiling ocean of water some 800 kilometers (497 miles) below the top cloud surface. | 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) | the model's own knowledge | *no source* | Winds reached 450 mph (724 km/h); the ocean lies 800 km (497 mi) down | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ larger moons. | Ariele, Umbrella, and Titan, five of Uranus’ smaller moons | the model's own knowledge | *no source* | Titan orbits Saturn; Ariel, Umbriel, Titania are major Uranian moons | *none* |
| In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly nine-year travels. | nearly century-long travels | the model's own knowledge | *no source* | Launched in 1977, Voyager 2 had flown under nine years by 1986 | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger broke up on Jan. 28, 1986, killing all seven crew | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 31c2462e2828 (command) -- lineup opus-5.5-sub |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (decompose) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 -> claude-opus-5-5 |
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
| Duration | 246.0s |
| Generated | 2026-09-28T00:10:19+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
