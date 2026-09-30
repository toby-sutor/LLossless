## Verdict

**61 finding(s).** In the claims: 47 contradicted, 1 partially invented. In the structure: 13 verbatim violation. **The model retrieved.** This run was made at fidelity sourced, and 1 of the 6 call(s) that reported a turn count took the turns a retrieval costs. Which statement a retrieval backs is not recorded, and each is still the model's. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 29 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 22 |
| Forward — source claims accounted for in the merge | **8/34** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **1/12** |
| Forward — `source_b.md` claims accounted for | **7/22** |
| Reverse — merge claims found in a source | **7/29** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **63/63** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge names Voyager 2 and two encounters, not Voyager 3 and three.
- **A-002** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The spacecraft sent to Uranus is Voyager 2, not Voyager 3.
- **A-003** -- the two documents disagree
  - `source_a.md:3` says: The journey of Voyager 3 to Uranus would take about 4,5 years.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The 4,5-year duration matches, but the spacecraft is Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge says Neptune, not Saturn.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby.
  - `merged.md` says: 'Voyager 2 had only 5.5 hours of close study during its flyby.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge gives Voyager 2 and 5.5 hours, not Voyager 1 and 6.4 days.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2 was the first human-made object to fly past Uranus.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge names Voyager 2, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: 'Its long-range observations of the planet began Nov. 4, 1985' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge describes long-range observations by Voyager 2 beginning Nov. 4, 1985, not short-range observations by Voyager 1 beginning Jan. 31, 1987.
- **A-009** -- the two documents disagree
  - `source_a.md:9` says: When Voyager 1's short-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth.
  - `merged.md` says: 'Its long-range observations of the planet began Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The 2,5-hour signal time matches, but it belongs to Voyager 2's long-range observations, not Voyager 1's short-range ones.
- **A-010** -- the two documents disagree
  - `source_a.md:9` says: Light conditions at Uranus were five-hundred times less than terrestrial conditions.
  - `merged.md` says: 'Light conditions were 400 times less than terrestrial conditions.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge says 400 times, not 500.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge gives UT and 1986, not ED and 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 50,640 miles (81,500 kilometers)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim swaps the units: the merge gives 50,640 miles, not 50,640 kilometers.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: During its flyby of Uranus, Voyager 2 discovered 11 new moons.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge says 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The new moons discovered by Voyager 2 were given names such as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Several of the claim's names differ from the names listed in the merge.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The names of the new Uranian moons are allusions to Goethe.
  - `merged.md` says: 'obvious allusions to Shakespeare' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge says the names allude to Shakespeare, not Goethe.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for Uranian moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1787' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge gives 1787, not 1687.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: During its flyby, Voyager 2 discovered three new rings of Uranus.
  - `merged.md` says: 'two new rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge says two new rings, not three.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Uranus had eight previously known rings before Voyager 2's flyby.
  - `merged.md` says: 'in addition to the “older” nine rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge says nine previously known rings, not eight.
- **B-007** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered that Uranus has a magnetic field tilted at 66 degrees off-axis.
  - `merged.md` says: 'a magnetic field tilted at 55 degrees off-axis' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge gives 55 degrees, not 66.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'as high as 450 miles per hour (724 kilometers per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge gives 450 miles per hour, not 450 km/h.
- **B-010** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus.
  - `merged.md` says: 'evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge says an ocean at 497 miles (800 km), not a lake at 479 miles (900 km).
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge names Ariel, Umbriel and Titania, not Ariele, Umbrella and Titan.
- **B-014** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus’ smaller moons.
  - `merged.md` says: 'five of Uranus’ larger moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge calls them larger moons, not smaller ones, and gives different names.
- **B-017** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2's travels at the time of the Miranda flyby had lasted nearly a century.
  - `merged.md` says: 'nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge says nearly a decade, not nearly a century.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: News of Voyager 2's Uranus encounter was interrupted the same day by the Challenger accident.
  - `merged.md` says: 'was interrupted the same week by the tragic Challenger accident' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge says the same week, not the same day.
- **B-021** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge says seven astronauts, not six.
- **B-022** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during the space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The merge gives Jan. 28, not Feb. 28.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the two planetary encounters before being directed to Uranus.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says three planetary encounters (and names Voyager 3), not two.
- **M-004** -- the two documents disagree
  - `merged.md:5` says: The geometry of Voyager 2's Uranus encounter was defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Saturn, not Neptune.
- **M-005** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 had only 5.5 hours of close study during its Uranus flyby.
  - `source_a.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 6.4 days, not 5.5 hours.
- **M-007** -- the two documents disagree
  - `merged.md:7` says: Voyager 2's long-range observations of Uranus began Nov. 4, 1985.
  - `source_a.md` says: 'short-range observations of the planet began Jan. 31, 1987' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives short-range observations beginning Jan. 31, 1987, which conflicts with Nov. 4, 1985.
- **M-009** -- the two documents disagree
  - `merged.md:7` says: Light conditions at Uranus were 400 times less than terrestrial conditions.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says 500 times, not 400.
- **M-010** -- the two documents disagree
  - `merged.md:7` says: Voyager 2's closest approach to Uranus took place at 17:59 UT Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives ED and 1968, not UT and 1986.
- **M-011** -- the two documents disagree
  - `merged.md:7` says: Voyager 2's closest approach to Uranus was at a range of about 50,640 miles (81,500 kilometers).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source has the units reversed: 50,640 kilometers and 81,500 miles.
- **M-012** -- the two documents disagree
  - `merged.md:9` says: During its Uranus flyby, Voyager 2 discovered 10 new moons.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says 11 new moons, not 10.
- **M-013** -- the two documents disagree
  - `merged.md:9` says: The new Uranian moons discovered by Voyager 2 were given names such as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Several of the source's names differ from the claimed ones (Pucka, Portila, Juliette, and others).
- **M-014** -- the two documents disagree
  - `merged.md:9` says: The names of the new Uranian moons are allusions to Shakespeare.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the names allude to Goethe, not Shakespeare.
- **M-015** -- the two documents disagree
  - `merged.md:9` says: The Shakespearean naming tradition for Uranian moons began in 1787.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 1687, not 1787.
- **M-016** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 discovered two new rings of Uranus in addition to the older nine rings.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says three new rings and eight older ones, not two and nine.
- **M-017** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 discovered that Uranus has a magnetic field tilted at 55 degrees off-axis and off-center.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says 66 degrees, not 55.
- **M-018** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour).
  - `source_b.md` says: 'as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 450 km/h, not 450 mph or 724 km/h.
- **M-019** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 found evidence of a boiling ocean of water some 497 miles (800 kilometers) below Uranus' top cloud surface.
  - `source_b.md` says: 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says a lake at 479 miles (900 km), not an ocean at 497 miles (800 km).
- **M-021** -- the two documents disagree
  - `merged.md:13` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Ariele, Umbrella and Titan, not Ariel, Umbriel and Titania.
- **M-022** -- the two documents disagree
  - `merged.md:13` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons.
  - `source_b.md` says: 'five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source calls them the smaller moons, not the larger ones.
- **M-024** -- the two documents disagree
  - `merged.md:13` says: Miranda was the closest Voyager 2 came to any object so far in its nearly decade-long travels.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says century-long, not decade-long.
- **M-027** -- the two documents disagree
  - `merged.md:15` says: News of the Uranus encounter was interrupted the same week by the Challenger accident.
  - `source_b.md` says: 'The spectacular news of the Uranus encounter was interrupted the same day' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the same day, not the same week.
- **M-028** -- the two documents disagree
  - `merged.md:15` says: The Challenger accident killed seven astronauts.
  - `source_b.md` says: 'killed six astronauts' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says six astronauts, not seven.
- **M-029** -- the two documents disagree
  - `merged.md:15` says: The Challenger accident occurred during the space shuttle launch on Jan. 28, 1986.
  - `source_b.md` says: 'during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives Feb. 28, not Jan. 28.

### Partly invented — the sources carry some of this claim

- **M-008** (`merged.md:7`) — On Nov. 4, 1985, signals from Voyager 2 took approximately 2,5 hours to reach Earth.
  - evidence: 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The 2,5-hour signal time is supported, but the source ties it to Jan. 31, 1987, not Nov. 4, 1985.

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
- **other convention** `m6` (`merged.md`) - '2,5' (merged.md, line 7) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `m13` (`merged.md`) - '17.560' (merged.md, line 13) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m13` (`merged.md`) - '28.260' (merged.md, line 13) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

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
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' in `merged.md` -- The merge names Voyager 2 and two encounters, not Voyager 3 and three. |
| 2 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- The spacecraft sent to Uranus is Voyager 2, not Voyager 3. |
| 3 | The journey of Voyager 3 to Uranus would take about 4,5 years. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.' in `merged.md` -- The 4,5-year duration matches, but the spacecraft is Voyager 2, not Voyager 3. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' in `merged.md` -- The merge says Neptune, not Saturn. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | contradicted | 'Voyager 2 had only 5.5 hours of close study during its flyby.' in `merged.md` -- The merge gives Voyager 2 and 5.5 hours, not Voyager 1 and 6.4 days. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2 was the first human-made object to fly past Uranus.' in `merged.md` -- The merge names Voyager 2, not Voyager 1. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | 'Its long-range observations of the planet began Nov. 4, 1985' in `merged.md` -- The merge describes long-range observations by Voyager 2 beginning Nov. 4, 1985, not short-range observations by Voyager 1 beginning Jan. 31, 1987. |
| 9 | When Voyager 1's short-range observations of Uranus began, signals took approximately 2,5 hours to reach Earth. | 9 | contradicted | 'Its long-range observations of the planet began Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth.' in `merged.md` -- The 2,5-hour signal time matches, but it belongs to Voyager 2's long-range observations, not Voyager 1's short-range ones. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | contradicted | 'Light conditions were 400 times less than terrestrial conditions.' in `merged.md` -- The merge says 400 times, not 500. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' in `merged.md` -- The merge gives UT and 1986, not ED and 1968. |
| 12 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 50,640 miles (81,500 kilometers)' in `merged.md` -- The claim swaps the units: the merge gives 50,640 miles, not 50,640 kilometers. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `merged.md` -- The merge states this directly. |

### `source_b.md` -- 22 claim(s): 0 dropped, 15 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | During its flyby of Uranus, Voyager 2 discovered 11 new moons. | 3 | contradicted | 'Voyager 2 discovered 10 new moons' in `merged.md` -- The merge says 10 new moons, not 11. |
| 2 | The new moons discovered by Voyager 2 were given names such as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Several of the claim's names differ from the names listed in the merge. |
| 3 | The names of the new Uranian moons are allusions to Goethe. | 3 | contradicted | 'obvious allusions to Shakespeare' in `merged.md` -- The merge says the names allude to Shakespeare, not Goethe. |
| 4 | The naming tradition for Uranian moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1787' in `merged.md` -- The merge gives 1787, not 1687. |
| 5 | During its flyby, Voyager 2 discovered three new rings of Uranus. | 3 | contradicted | 'two new rings' in `merged.md` -- The merge says two new rings, not three. |
| 6 | Uranus had eight previously known rings before Voyager 2's flyby. | 3 | contradicted | 'in addition to the “older” nine rings' in `merged.md` -- The merge says nine previously known rings, not eight. |
| 7 | Voyager 2 discovered that Uranus has a magnetic field tilted at 66 degrees off-axis. | 3 | contradicted | 'a magnetic field tilted at 55 degrees off-axis' in `merged.md` -- The merge gives 55 degrees, not 66. |
| 9 | Voyager 2 found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'as high as 450 miles per hour (724 kilometers per hour)' in `merged.md` -- The merge gives 450 miles per hour, not 450 km/h. |
| 10 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus. | 5 | contradicted | 'evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface' in `merged.md` -- The merge says an ocean at 497 miles (800 km), not a lake at 479 miles (900 km). |
| 13 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The merge names Ariel, Umbriel and Titania, not Ariele, Umbrella and Titan. |
| 14 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus’ smaller moons. | 7 | contradicted | 'five of Uranus’ larger moons' in `merged.md` -- The merge calls them larger moons, not smaller ones, and gives different names. |
| 17 | Voyager 2's travels at the time of the Miranda flyby had lasted nearly a century. | 7 | contradicted | 'nearly decade-long travels' in `merged.md` -- The merge says nearly a decade, not nearly a century. |
| 20 | News of Voyager 2's Uranus encounter was interrupted the same day by the Challenger accident. | 9 | contradicted | 'was interrupted the same week by the tragic Challenger accident' in `merged.md` -- The merge says the same week, not the same day. |
| 21 | The Challenger accident killed six astronauts. | 9 | contradicted | 'killed seven astronauts' in `merged.md` -- The merge says seven astronauts, not six. |
| 22 | The Challenger accident occurred during the space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The merge gives Jan. 28, not Feb. 28. |
| 8 | Voyager 2 discovered that Uranus' magnetic field is off-center. | 3 | carried | 'a magnetic field tilted at 55 degrees off-axis and off-center' in `merged.md` -- The merge states that the magnetic field is off-center. |
| 11 | Uranus' rings were found to be extremely variable in thickness. | 5 | carried | 'Uranus’ rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- The merge states that the rings are variable in thickness. |
| 12 | Uranus' rings were found to be extremely variable in transparency. | 5 | carried | 'Uranus’ rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- The merge states that the rings are variable in transparency. |
| 15 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- The range matches exactly. |
| 16 | Voyager 2's flyby of Miranda was the closest it had come to any object so far in its travels. | 7 | carried | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- The merge states this directly. |
| 18 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- The merge states this directly. |
| 19 | Uranus appeared generally featureless in Voyager 2 images. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- The merge states this in context of the images. |

### `merged.md` -- 29 claim(s): 0 invented, 21 contradicted, 1 supported in part, 7 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with the two planetary encounters before being directed to Uranus. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source says three planetary encounters (and names Voyager 3), not two. |
| 4 | The geometry of Voyager 2's Uranus encounter was defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- The source names Saturn, not Neptune. |
| 5 | Voyager 2 had only 5.5 hours of close study during its Uranus flyby. | contradicted | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- The source gives 6.4 days, not 5.5 hours. |
| 7 | Voyager 2's long-range observations of Uranus began Nov. 4, 1985. | contradicted | `source_a.md` | 'short-range observations of the planet began Jan. 31, 1987' in `source_a.md` -- The source gives short-range observations beginning Jan. 31, 1987, which conflicts with Nov. 4, 1985. |
| 9 | Light conditions at Uranus were 400 times less than terrestrial conditions. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- The source says 500 times, not 400. |
| 10 | Voyager 2's closest approach to Uranus took place at 17:59 UT Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- The source gives ED and 1968, not UT and 1986. |
| 11 | Voyager 2's closest approach to Uranus was at a range of about 50,640 miles (81,500 kilometers). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- The source has the units reversed: 50,640 kilometers and 81,500 miles. |
| 12 | During its Uranus flyby, Voyager 2 discovered 10 new moons. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- The source says 11 new moons, not 10. |
| 13 | The new Uranian moons discovered by Voyager 2 were given names such as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- Several of the source's names differ from the claimed ones (Pucka, Portila, Juliette, and others). |
| 14 | The names of the new Uranian moons are allusions to Shakespeare. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- The source says the names allude to Goethe, not Shakespeare. |
| 15 | The Shakespearean naming tradition for Uranian moons began in 1787. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- The source gives 1687, not 1787. |
| 16 | Voyager 2 discovered two new rings of Uranus in addition to the older nine rings. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source says three new rings and eight older ones, not two and nine. |
| 17 | Voyager 2 discovered that Uranus has a magnetic field tilted at 55 degrees off-axis and off-center. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source says 66 degrees, not 55. |
| 18 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour). | contradicted | `source_b.md` | 'as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives 450 km/h, not 450 mph or 724 km/h. |
| 19 | Voyager 2 found evidence of a boiling ocean of water some 497 miles (800 kilometers) below Uranus' top cloud surface. | contradicted | `source_b.md` | 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- The source says a lake at 479 miles (900 km), not an ocean at 497 miles (800 km). |
| 21 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source names Ariele, Umbrella and Titan, not Ariel, Umbriel and Titania. |
| 22 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons. | contradicted | `source_b.md` | 'five of Uranus’ smaller moons' in `source_b.md` -- The source calls them the smaller moons, not the larger ones. |
| 24 | Miranda was the closest Voyager 2 came to any object so far in its nearly decade-long travels. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source says century-long, not decade-long. |
| 27 | News of the Uranus encounter was interrupted the same week by the Challenger accident. | contradicted | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day' in `source_b.md` -- The source says the same day, not the same week. |
| 28 | The Challenger accident killed seven astronauts. | contradicted | `source_b.md` | 'killed six astronauts' in `source_b.md` -- The source says six astronauts, not seven. |
| 29 | The Challenger accident occurred during the space shuttle launch on Jan. 28, 1986. | contradicted | `source_b.md` | 'during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- The source gives Feb. 28, not Jan. 28. |
| 8 | On Nov. 4, 1985, signals from Voyager 2 took approximately 2,5 hours to reach Earth. | supported in part | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- The 2,5-hour signal time is supported, but the source ties it to Jan. 31, 1987, not Nov. 4, 1985. |
| 2 | Mission planners directed Voyager 2 to Uranus, a journey that would take about 4,5 years. | supported | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years' in `source_a.md` -- The source states the Uranus direction and the 4,5-year journey; the document heading identifies the spacecraft as Voyager 2. |
| 3 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- The source states this in the same words. |
| 6 | Voyager 2 was the first human-made object to fly past Uranus. | supported | `source_a.md` | 'The first human-made object to fly past Uranus' in `source_a.md` -- The source states this; it names Voyager 1 in the sentence, but the document is about Voyager 2, so the claim is taken as supported. |
| 20 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states this. |
| 23 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- The source gives the same figures. |
| 25 | Images of Miranda showed a surface that was a mishmash of peculiar features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `source_b.md` -- The source states this. |
| 26 | Uranus appeared generally featureless in Voyager 2 images. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- The source states this. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **29** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **34**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

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

The merge declared **12** departure(s) from its sources. Checking them confirms 1, rejects 10, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Spacecraft name and encounter count corrected; see additions. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back CONTRADICTED, A-003 came back CONTRADICTED (`A-001`, `A-002`, `A-003`) |
| `a4` | reworded | Typo fixed; target planet, spacecraft and duration corrected per NASA. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED (`A-005`, `A-006`) |
| `a5` | reworded | Dangling modifier fixed; spacecraft, range and start date corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED, A-009 came back CONTRADICTED (`A-007`, `A-008`, `A-009`) |
| `a6` | reworded | Light-condition factor corrected to the NASA figure. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-010 came back CONTRADICTED (`A-010`) |
| `a7` | reworded | Time zone, year and swapped distance units corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | superseded | Identical title; the base document's heading is kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Moon count, names, namesake, year, ring counts and tilt corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED, B-007 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`, `B-005`, `B-006`, `B-007`) |
| `b3` | reworded | Wind units, ocean wording and depth figures corrected per NASA. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-009 came back CONTRADICTED, B-010 came back CONTRADICTED (`B-009`, `B-010`) |
| `b4` | reworded | Ambiguous 'Its' replaced with the planet's name. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-011`, `B-012`) |
| `b5` | reworded | Moon names and 'smaller' corrected per NASA. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-013 came back CONTRADICTED, B-014 came back CONTRADICTED (`B-013`, `B-014`) |
| `b6` | reworded | 'century-long' corrected to 'decade-long'; distances kept verbatim. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-017 came back CONTRADICTED (`B-017`) |
| `b9` | reworded | Interval, death toll and launch date corrected per NASA. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-020 came back CONTRADICTED, B-021 came back CONTRADICTED, B-022 came back CONTRADICTED (`B-020`, `B-021`, `B-022`) |

## Added from outside the documents

The merge declared 28 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. The model took more turns on 1 call(s) than a call that retrieves nothing can take, so it used a tool it was granted at least that often. It is a count of turns rather than of fetches, and which statement a retrieval belongs to is not recorded. The endpoint's own web-request counter reported none, which on this backend means it could not see one rather than that none was made: it counts a vendor's server-side tools and a command-line tool runs in the model's own process.

28 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page and both titles name Voyager 2 as the spacecraft. | *none* |
| Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | the three planetary encounters | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: primary goals met with the two planetary encounters. | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 5.5 hours of close study during its flyby. | a future encounter with Saturn | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: geometry set by a possible future Neptune encounter. | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 5.5 hours of close study during its flyby. | Voyager 1 had only | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: Voyager 2, not Voyager 1, made the Uranus flyby. | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 5.5 hours of close study during its flyby. | 6.4 days | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: only 5.5 hours of close study during the flyby. | *none* |
| Voyager 2 was the first human-made object to fly past Uranus. | Voyager 1's | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: Voyager 2 was the first to fly past Uranus. | *none* |
| Its long-range observations of the planet began Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth. | short-range | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page describes long-range observations beginning pre-flyby. | *none* |
| Its long-range observations of the planet began Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth. | Jan. 31, 1987 | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: long-range observations began Nov. 4, 1985. | *none* |
| Light conditions were 400 times less than terrestrial conditions. | five-hundred times less | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: light conditions were 400 times less. | *none* |
| Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers). | 17:59 ED | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page gives closest approach at 17:59 UT. | *none* |
| Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers). | Jan. 24, 1968 | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page gives Jan. 24, 1986 for closest approach. | *none* |
| Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers). | 50,640 kilometers (81,500 miles) | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: 50,640 miles (81,500 km); units were swapped. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 55 degrees off-axis and off-center. | 11 new moons | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: Voyager 2 discovered 10 new moons. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 55 degrees off-axis and off-center. | Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page lists Puck, Portia, Juliet, Cressida, Rosalind ... Bianca. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 55 degrees off-axis and off-center. | obvious allusions to Goethe | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: the names are allusions to Shakespeare. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 55 degrees off-axis and off-center. | a naming tradition begun in 1687 | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page dates the naming tradition to 1787. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 55 degrees off-axis and off-center. | three new rings | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: two new rings were discovered. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 55 degrees off-axis and off-center. | the “older” eight rings | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: the new rings add to the older nine rings. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 55 degrees off-axis and off-center. | 66 degrees | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: magnetic field tilted at 55 degrees. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour) and found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface. | 450 km/h (72400 meters per hour) | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: 450 miles per hour (724 kilometers per hour). | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour) and found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface. | a boiling lake of water | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page describes a boiling ocean, not a lake. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour) and found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface. | 479 miles (900 kilometers) | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: 497 miles (800 kilometers); 800 km is about 497 mi. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ larger moons. | Ariele, Umbrella, and Titan | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page lists Ariel, Umbriel and Titania. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ larger moons. | five of Uranus’ smaller moons | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: five of Uranus' larger moons. | *none* |
| In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels. | nearly century-long travels | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: nearly decade-long travels. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | interrupted the same day | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: same week; Jan. 24 and Jan. 28, 1986 are 4 days apart. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | killed six astronauts | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page: the Challenger accident killed seven astronauts. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | Feb. 28, 1986 | cited | NASA Science, Voyager 2 mission page, <redacted> read during this merge | NASA page gives the launch date as Jan. 28, 1986. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 80665793f0d7 (command) -- Claude Code - Opus |
| Fidelity | sourced |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-opus-5-5 -> claude-opus-5-5 (the answer's output tokens; also named claude-haiku-4-5-20251001) |
| Model (decompose) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 -> claude-opus-5-5 |
| Structured output | prompt (probed) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=low, merge=xhigh, verify=low |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | a13818a072bf |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Retrieval | WebSearch, WebFetch permitted; 1 of 6 call(s) used a tool (8 turn(s) in total) |
| Isolation | decompose, merge, verify: safe mode, tools WebSearch, WebFetch |
| Errors | 0 |
| Duration | 301.0s |
| Generated | 2026-09-26T13:50:07+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `6d8a835cc983` |
| Prompt | `prompts/verify.md` `55a721b20905` |
| Prompt | `prompts/verify_reverse.md` `2a6d7e955709` |

> **Document content was handed to a program on this machine (`Claude Code - Opus`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The model was permitted to reach the network** (WebSearch, WebFetch), so a query or a fetch it made may have carried text from these documents to a third party. 1 of 6 call(s) used a tool (8 turn(s) in total), counted in turns rather than in fetches. LLossless itself made no network request of any kind and resolved none of the sources the merge names.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
