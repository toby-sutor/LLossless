## Verdict

**52 finding(s).** In the claims: 42 contradicted, 1 hallucinated, 1 partially invented. In the structure: 8 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 34 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 22 |
| Forward — source claims accounted for in the merge | **11/34** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **0/12** |
| Forward — `source_b.md` claims accounted for | **11/22** |
| Reverse — merge claims found in a source | **13/34** |
| Reverse — supported only in part | 1 |
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
  - why this was read as a contradiction: The reference names Voyager 2 and two encounters, not Voyager 3 and three.
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
- **A-004** -- the two documents disagree
  - `source_a.md:5` says: The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'its encounter with Saturn was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The optimized encounter was with Saturn, not Jupiter.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The future encounter was with Neptune, not Saturn.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby of Uranus.
  - `merged.md` says: 'Voyager 2 had only 6.4 days of close study during its flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The 6.4 days of close study are attributed to Voyager 2, not Voyager 1.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'The first human-made object to fly past Uranus, Voyager 2' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The first object to fly past Uranus was Voyager 2, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: 'Voyager 2 began its long-range observations of the planet Nov. 4, 1985' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives Voyager 2 long-range observations beginning Nov. 4, 1985, not Voyager 1 short-range observations beginning in 1987.
- **A-009** -- the two documents disagree
  - `source_a.md:9` says: When Voyager 1's short-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth.
  - `merged.md` says: 'Voyager 2 began its long-range observations of the planet Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The 2,5-hour signal time relates to Voyager 2's long-range observations, not Voyager 1's short-range ones.
- **A-010** -- the two documents disagree
  - `source_a.md:9` says: Light conditions at Uranus were five-hundred times less than terrestrial conditions.
  - `merged.md` says: 'Light conditions were roughly 400 times less than terrestrial conditions' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says 400 times, not five hundred.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The year of closest approach is 1986, not 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 81,500 kilometers (50,640 miles), so the claim swaps the units.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The new moons discovered by Voyager 2 were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Several of the claimed names differ from those in the reference, such as Pucka versus Puck and Portila versus Portia.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The names of the new moons are allusions to Goethe.
  - `merged.md` says: 'allusions to Shakespeare and Alexander Pope' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The names allude to Shakespeare and Pope, not Goethe.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The moon naming tradition was begun in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1852' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The naming tradition began in 1852, not 1687.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: During its flyby, Voyager 2 discovered three new rings at Uranus.
  - `merged.md` says: 'two new rings in addition to the “older” nine rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says two new rings, not three.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Uranus had eight previously known rings before Voyager 2's flyby.
  - `merged.md` says: 'two new rings in addition to the “older” nine rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives nine older rings, not eight.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 450 miles per hour (724 km/h), not 450 km/h.
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Ariel, Umbriel and Titania, not Ariele, Umbrella and Titan.
- **B-014** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons.
  - `merged.md` says: 'Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ larger moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Ariel, Umbriel and Titania as larger moons, which is incompatible with the claim's names Ariele, Umbrella and Titan and with calling them smaller moons.
- **B-017** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2's travels had lasted nearly a century at the time of the Miranda flyby.
  - `merged.md` says: 'its nearly nine-year travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives nearly nine years of travel, not nearly a century.
- **B-021** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says seven astronauts were killed, not six.
- **B-022** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during the space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference dates the Challenger launch accident to Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the two planetary encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says three planetary encounters, not two, and it names the spacecraft Voyager 3.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Saturn was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the encounter with Jupiter, not Saturn, was optimized for future flybys.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Saturn, not Neptune, as the future encounter that defined the geometry.
- **M-006** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had only 6.4 days of close study during its Uranus flyby.
  - `source_a.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes the 6.4 days of close study to Voyager 1, not Voyager 2.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: Light conditions at Uranus were roughly 400 times less than terrestrial conditions.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says five-hundred times less, not roughly 400 times less.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach to Uranus took place at 17:59 ED Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the year of closest approach as 1968, not 1986.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 50,640 kilometers (81,500 miles), which reverses the claim's units.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: The new moons discovered by Voyager 2 were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives different moon names, such as Pucka, Portila, Juliette and Kressida, than those in the claim.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The names of the new Uranian moons are allusions to Shakespeare and Alexander Pope.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the names allude to Goethe, not to Shakespeare and Alexander Pope.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: The naming tradition for Uranian moons alluding to Shakespeare and Alexander Pope began in 1852.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the naming tradition to 1687, not 1852.
- **M-017** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered two new rings of Uranus.
  - `source_b.md` says: 'three new rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says three new rings were discovered, not two.
- **M-018** -- the two documents disagree
  - `merged.md:7` says: Uranus had nine previously known rings before Voyager 2's flyby.
  - `source_b.md` says: 'in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says there were eight older rings, not nine.
- **M-021** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour).
  - `source_b.md` says: 'as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 450 km/h, not 450 miles per hour (724 km/h).
- **M-025** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names the moons Ariele, Umbrella and Titan, not Ariel, Umbriel and Titania.
- **M-026** -- the two documents disagree
  - `merged.md:11` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source calls these five of Uranus' smaller moons, not larger, and gives the names as Ariele, Umbrella and Titan rather than Ariel, Umbriel and Titania.
- **M-029** -- the two documents disagree
  - `merged.md:11` says: At the time of the Miranda flyby, Voyager 2 had been traveling for nearly nine years.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source describes the travels as nearly century-long, which is incompatible with nearly nine years.
- **M-033** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident killed seven astronauts.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the accident killed six astronauts, not seven.
- **M-034** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident occurred during a space shuttle launch Jan. 28, 1986.
  - `source_b.md` says: 'during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the launch to Feb. 28, 1986, not Jan. 28, 1986.

### Invented — in the merge, in neither source

- **M-008** (`merged.md:5`) — Voyager 2 began its long-range observations of Uranus Nov. 4, 1985.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: No source mentions long-range observations beginning Nov. 4, 1985; source_a gives only a short-range start date.

### Partly invented — the sources carry some of this claim

- **M-009** (`merged.md:5`) — When Voyager 2 began its long-range observations of Uranus, signals took approximately 2,5 hours to reach Earth.
  - evidence: 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The 2,5-hour signal time is stated, but the source ties it to the start of short-range observations, not long-range ones.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (74 / 0) |

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
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' in `merged.md` -- The reference names Voyager 2 and two encounters, not Voyager 3 and three. |
| 2 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- The spacecraft directed to Uranus is Voyager 2, not Voyager 3. |
| 3 | The journey of Voyager 3 to Uranus would take about 4,5 years. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years' in `merged.md` -- The 4,5-year journey is attributed to Voyager 2, not Voyager 3. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'its encounter with Saturn was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- The optimized encounter was with Saturn, not Jupiter. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' in `merged.md` -- The future encounter was with Neptune, not Saturn. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby of Uranus. | 7 | contradicted | 'Voyager 2 had only 6.4 days of close study during its flyby' in `merged.md` -- The 6.4 days of close study are attributed to Voyager 2, not Voyager 1. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'The first human-made object to fly past Uranus, Voyager 2' in `merged.md` -- The first object to fly past Uranus was Voyager 2, not Voyager 1. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | 'Voyager 2 began its long-range observations of the planet Nov. 4, 1985' in `merged.md` -- The reference gives Voyager 2 long-range observations beginning Nov. 4, 1985, not Voyager 1 short-range observations beginning in 1987. |
| 9 | When Voyager 1's short-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth. | 9 | contradicted | 'Voyager 2 began its long-range observations of the planet Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth' in `merged.md` -- The 2,5-hour signal time relates to Voyager 2's long-range observations, not Voyager 1's short-range ones. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | contradicted | 'Light conditions were roughly 400 times less than terrestrial conditions' in `merged.md` -- The reference says 400 times, not five hundred. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' in `merged.md` -- The year of closest approach is 1986, not 1968. |
| 12 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The reference gives 81,500 kilometers (50,640 miles), so the claim swaps the units. |

### `source_b.md` -- 22 claim(s): 0 dropped, 11 contradicted, 0 carried in part, 11 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | The new moons discovered by Voyager 2 were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Several of the claimed names differ from those in the reference, such as Pucka versus Puck and Portila versus Portia. |
| 3 | The names of the new moons are allusions to Goethe. | 3 | contradicted | 'allusions to Shakespeare and Alexander Pope' in `merged.md` -- The names allude to Shakespeare and Pope, not Goethe. |
| 4 | The moon naming tradition was begun in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1852' in `merged.md` -- The naming tradition began in 1852, not 1687. |
| 5 | During its flyby, Voyager 2 discovered three new rings at Uranus. | 3 | contradicted | 'two new rings in addition to the “older” nine rings' in `merged.md` -- The reference says two new rings, not three. |
| 6 | Uranus had eight previously known rings before Voyager 2's flyby. | 3 | contradicted | 'two new rings in addition to the “older” nine rings' in `merged.md` -- The reference gives nine older rings, not eight. |
| 9 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour)' in `merged.md` -- The reference gives 450 miles per hour (724 km/h), not 450 km/h. |
| 13 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The reference names Ariel, Umbriel and Titania, not Ariele, Umbrella and Titan. |
| 14 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 | contradicted | 'Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ larger moons' in `merged.md` -- The reference names Ariel, Umbriel and Titania as larger moons, which is incompatible with the claim's names Ariele, Umbrella and Titan and with calling them smaller moons. |
| 17 | Voyager 2's travels had lasted nearly a century at the time of the Miranda flyby. | 7 | contradicted | 'its nearly nine-year travels' in `merged.md` -- The reference gives nearly nine years of travel, not nearly a century. |
| 21 | The Challenger accident killed six astronauts. | 9 | contradicted | 'killed seven astronauts' in `merged.md` -- The reference says seven astronauts were killed, not six. |
| 22 | The Challenger accident occurred during the space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The reference dates the Challenger launch accident to Jan. 28, 1986, not Feb. 28, 1986. |
| 1 | During its flyby, Voyager 2 discovered 11 new moons at Uranus. | 3 | carried | 'During its flyby, Voyager 2 discovered 11 new moons' in `merged.md` -- The reference states Voyager 2 discovered 11 new moons during its Uranus flyby. |
| 7 | During its flyby, Voyager 2 discovered a magnetic field at Uranus tilted at 66 degrees off-axis. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis' in `merged.md` -- The reference states the discovered magnetic field was tilted 66 degrees off-axis. |
| 8 | Uranus' magnetic field is off-center. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- The reference states the magnetic field is off-center. |
| 10 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus. | 5 | carried | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- The reference states the boiling lake with the same figures. |
| 11 | Uranus' rings were found to be extremely variable in thickness. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference states the rings were extremely variable in thickness. |
| 12 | Uranus' rings were found to be extremely variable in transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference states the rings were extremely variable in transparency. |
| 15 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- The reference states the same flyby range for Miranda. |
| 16 | In flying by Miranda, Voyager 2 came closest to any object so far in its travels. | 7 | carried | 'the spacecraft came closest to any object so far in its nearly nine-year travels' in `merged.md` -- The reference states that the Miranda flyby was the closest approach to any object so far in the spacecraft's travels. |
| 18 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- The reference describes Miranda's surface in the images as a mishmash of peculiar features. |
| 19 | Uranus appeared generally featureless in Voyager 2 images. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- The reference states that Uranus appeared generally featureless in the context of Voyager 2's returned photos. |
| 20 | The news of the Uranus encounter was interrupted the same day by the Challenger accident. | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `merged.md` -- The reference states that the Uranus encounter news was interrupted the same day by the Challenger accident. |

### `merged.md` -- 34 claim(s): 1 invented, 19 contradicted, 1 supported in part, 13 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 8 | Voyager 2 began its long-range observations of Uranus Nov. 4, 1985. | invented | -- | No source mentions long-range observations beginning Nov. 4, 1985; source_a gives only a short-range start date. |
| 1 | Voyager 2 had fulfilled its primary mission goals with the two planetary encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source says three planetary encounters, not two, and it names the spacecraft Voyager 3. |
| 4 | Voyager 2's encounter with Saturn was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- The source says the encounter with Jupiter, not Saturn, was optimized for future flybys. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- The source names Saturn, not Neptune, as the future encounter that defined the geometry. |
| 6 | Voyager 2 had only 6.4 days of close study during its Uranus flyby. | contradicted | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- The source attributes the 6.4 days of close study to Voyager 1, not Voyager 2. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- The source identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus. |
| 10 | Light conditions at Uranus were roughly 400 times less than terrestrial conditions. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- The source says five-hundred times less, not roughly 400 times less. |
| 11 | Voyager 2's closest approach to Uranus took place at 17:59 ED Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- The source gives the year of closest approach as 1968, not 1986. |
| 12 | Voyager 2's closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- The source gives 50,640 kilometers (81,500 miles), which reverses the claim's units. |
| 14 | The new moons discovered by Voyager 2 were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- The source gives different moon names, such as Pucka, Portila, Juliette and Kressida, than those in the claim. |
| 15 | The names of the new Uranian moons are allusions to Shakespeare and Alexander Pope. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- The source says the names allude to Goethe, not to Shakespeare and Alexander Pope. |
| 16 | The naming tradition for Uranian moons alluding to Shakespeare and Alexander Pope began in 1852. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- The source dates the naming tradition to 1687, not 1852. |
| 17 | During its flyby, Voyager 2 discovered two new rings of Uranus. | contradicted | `source_b.md` | 'three new rings' in `source_b.md` -- The source says three new rings were discovered, not two. |
| 18 | Uranus had nine previously known rings before Voyager 2's flyby. | contradicted | `source_b.md` | 'in addition to the “older” eight rings' in `source_b.md` -- The source says there were eight older rings, not nine. |
| 21 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour). | contradicted | `source_b.md` | 'as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives 450 km/h, not 450 miles per hour (724 km/h). |
| 25 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source names the moons Ariele, Umbrella and Titan, not Ariel, Umbriel and Titania. |
| 26 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source calls these five of Uranus' smaller moons, not larger, and gives the names as Ariele, Umbrella and Titan rather than Ariel, Umbriel and Titania. |
| 29 | At the time of the Miranda flyby, Voyager 2 had been traveling for nearly nine years. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source describes the travels as nearly century-long, which is incompatible with nearly nine years. |
| 33 | The Challenger accident killed seven astronauts. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- The source says the accident killed six astronauts, not seven. |
| 34 | The Challenger accident occurred during a space shuttle launch Jan. 28, 1986. | contradicted | `source_b.md` | 'during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source dates the launch to Feb. 28, 1986, not Jan. 28, 1986. |
| 9 | When Voyager 2 began its long-range observations of Uranus, signals took approximately 2,5 hours to reach Earth. | supported in part | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- The 2,5-hour signal time is stated, but the source ties it to the start of short-range observations, not long-range ones. |
| 2 | Mission planners directed Voyager 2 to Uranus. | supported | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The source states that mission planners directed the spacecraft to Uranus, and the document is headed Voyager 2 at Uranus. |
| 3 | The journey of Voyager 2 to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- The source gives the same journey duration of about 4,5 years. |
| 13 | During its flyby, Voyager 2 discovered 11 new moons of Uranus. | supported | `source_b.md` | 'During its flyby, Voyager 2 discovered 11 new moons' in `source_b.md` -- The source states that Voyager 2 discovered 11 new moons during its flyby. |
| 19 | During its flyby, Voyager 2 discovered that Uranus has a magnetic field tilted at 66 degrees off-axis. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis' in `source_b.md` -- The source states that Voyager 2 discovered a magnetic field tilted 66 degrees off-axis. |
| 20 | Uranus's magnetic field is off-center. | supported | `source_b.md` | 'tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source describes the magnetic field as off-center. |
| 22 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below Uranus' top cloud surface. | supported | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- The source states the same figures and location for the boiling lake. |
| 23 | Uranus' rings were found to be extremely variable in thickness. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states that the rings are extremely variable in thickness. |
| 24 | Uranus' rings were found to be extremely variable in transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states that the rings are extremely variable in transparency. |
| 27 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- The source states the Miranda flyby range exactly as claimed. |
| 28 | In flying by Miranda, Voyager 2 came closest to any object so far in its travels. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source states that the Miranda flyby was the closest approach to any object so far in the spacecraft's travels. |
| 30 | Images of Miranda showed a surface that was a mishmash of peculiar features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `source_b.md` -- The source states that images of Miranda showed a surface that was a mishmash of peculiar features. |
| 31 | Uranus appeared generally featureless in Voyager 2 images. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- The source states that Uranus appeared generally featureless in the returned photos. |
| 32 | The news of the Uranus encounter was interrupted the same day by the Challenger accident. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- The source states that the Uranus news was interrupted the same day by the Challenger accident. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **34** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **34**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '1' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **12** departure(s) from its sources. Checking them confirms 1, rejects 11, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | duplicate | Identical title already carried from the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a2` | reworded | Corrected spacecraft name and number of primary encounters. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back CONTRADICTED, A-003 came back CONTRADICTED (`A-001`, `A-002`, `A-003`) |
| `a3` | reworded | Corrected the optimized encounter from Jupiter to Saturn. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-004 came back CONTRADICTED (`A-004`) |
| `a4` | reworded | Fixed typo; corrected Saturn to Neptune and Voyager 1 to Voyager 2. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED (`A-005`, `A-006`) |
| `a5` | reworded | Corrected spacecraft, observation type and start date. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED, A-009 came back CONTRADICTED (`A-007`, `A-008`, `A-009`) |
| `a6` | reworded | Corrected light ratio to match Uranus's distance from the Sun. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-010 came back CONTRADICTED (`A-010`) |
| `a7` | reworded | Corrected year and swapped units on the range figures. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b2` | reworded | Corrected moon names, literary source, naming year and ring counts. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED (`B-002`, `B-003`, `B-004`, `B-005`, `B-006`) |
| `b3` | reworded | Corrected the wind speed unit and its conversion. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-009 came back CONTRADICTED (`B-009`) |
| `b5` | reworded | Corrected moon names and larger versus smaller. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-013 came back CONTRADICTED, B-014 came back CONTRADICTED (`B-013`, `B-014`) |
| `b6` | reworded | Corrected the length of travel at the time of the flyby. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-017 came back CONTRADICTED (`B-017`) |
| `b9` | reworded | Corrected crew death toll and date of the Challenger accident. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-021 came back CONTRADICTED, B-022 came back CONTRADICTED (`B-021`, `B-022`) |

## Added from outside the documents

The merge declared 11 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

11 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters | the model's own knowledge | *no source* | No Voyager 3 flew; Voyager 2's primary mission was Jupiter and Saturn. | *none* |
| In fact, its encounter with Saturn was optimized in part to ensure that future planetary flybys would be possible. | its encounter with Jupiter was optimized | the model's own knowledge | *no source* | The Saturn flyby trajectory was set to enable Uranus and Neptune. | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 6.4 days of close study during its flyby. | a future encounter with Saturn: Voyager 1 had | the model's own knowledge | *no source* | Saturn preceded Uranus; Neptune followed; only Voyager 2 visited. | *none* |
| The first human-made object to fly past Uranus, Voyager 2 began its long-range observations of the planet Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | A 1987 start postdates the 1986 flyby; observatory phase began Nov 1985. | *none* |
| Light conditions were roughly 400 times less than terrestrial conditions. | five-hundred times less | the model's own knowledge | *no source* | At about 19-20 AU, inverse-square dimming cannot exceed about 404. | *none* |
| Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | Voyager 2 launched 1977; 81,500 km equals about 50,640 miles. | *none* |
| During its flyby, Voyager 2 discovered 11 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – allusions to Shakespeare and Alexander Pope, continuing a naming tradition begun in 1852), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 66 degrees off-axis and off-center. | Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings | the model's own knowledge | *no source* | Uranian moons bear Shakespeare/Pope names; nine rings were known pre-1986. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 450 km/h (72400 meters per hour) | the model's own knowledge | *no source* | 450 mph is 724 km/h; the original pair was internally inconsistent. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ larger moons. | Ariele, Umbrella, and Titan, five of Uranus’ smaller moons | the model's own knowledge | *no source* | Titan orbits Saturn; these five are Uranus's major moons. | *none* |
| In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly nine-year travels. | nearly century-long travels | the model's own knowledge | *no source* | Launched August 1977, it reached Miranda in January 1986. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger broke up on Jan. 28, 1986, killing its crew of seven. | *none* |

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
| Tokens | 32,514 in, 27,251 out |
| Cost | ~$0.68 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 209.6s |
| Generated | 2026-09-27T17:52:37+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
