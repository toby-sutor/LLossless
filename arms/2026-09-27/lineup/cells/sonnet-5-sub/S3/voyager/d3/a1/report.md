## Verdict

**49 finding(s).** In the claims: 42 contradicted. In the structure: 7 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 30 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 21 |
| Forward — source claims accounted for in the merge | **13/33** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **6/12** |
| Forward — `source_b.md` claims accounted for | **7/21** |
| Reverse — merge claims found in a source | **8/30** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **63/63** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Voyager 2, the first human-made object to fly past Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The document refers to Voyager 2, not Voyager 3, fulfilling the primary mission goals.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Neptune, not Saturn.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2, the first human-made object to fly past Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes this to Voyager 2, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of the planet began Jan. 31, 1987.
  - `merged.md` says: 'Voyager 2, the first human-made object to fly past Uranus, began short-range observations of the planet on Jan. 31, 1987' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes this to Voyager 2, not Voyager 1.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states the year as 1986, not 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim reverses the units; the text gives 81,500 kilometers (50,640 miles), not the other way around.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby of Uranus.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The new moons discovered by Voyager 2 were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The spellings in the claim differ from those in the text.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for Uranus's moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1787' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 1787, not 1687.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings around Uranus.
  - `merged.md` says: 'two new rings in addition to the nine previously known rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states two new rings, not three.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: There were eight older rings around Uranus in addition to the three new ones discovered by Voyager 2.
  - `merged.md` says: 'two new rings in addition to the nine previously known rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states nine previously known rings and two new ones, contradicting eight older rings and three new ones.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered a magnetic field around Uranus tilted at 66 degrees off-axis and off-center.
  - `merged.md` says: 'a magnetic field tilted at 59 degrees off-axis and off-center' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 59 degrees, not 66 degrees.
- **B-008** -- the two documents disagree
  - `source_b.md:5` says: 450 km/h is equivalent to 72400 meters per hour according to the document.
  - `merged.md` says: '450 km/h (450,000 meters per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 450,000 meters per hour, not 72400.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found evidence of a boiling lake of water some 479 miles below the top cloud surface of Uranus.
  - `merged.md` says: 'a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 559 miles, not 479 miles.
- **B-010** -- the two documents disagree
  - `source_b.md:5` says: 479 miles is equivalent to 900 kilometers according to the document.
  - `merged.md` says: 'a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text pairs 900 kilometers with 559 miles, not 479 miles.
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text names Ariel, Umbriel, and Titania, not Ariele, Umbrella, and Titan.
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are described as five of Uranus' smaller moons.
  - `merged.md` says: "Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text names different moons than those in the claim.
- **B-016** -- the two documents disagree
  - `source_b.md:7` says: The flyby of Miranda was the closest Voyager 2 had come to any object so far in its nearly century-long travels.
  - `merged.md` says: 'the spacecraft came closest to any object so far in its nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states nearly decade-long travels, not century-long.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts during their space shuttle launch.
  - `merged.md` says: 'the tragic Challenger accident that killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states seven astronauts, not six.
- **B-021** -- the two documents disagree
  - `source_b.md:9` says: The space shuttle launch occurred on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states the launch date as Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the three planetary encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states this achievement belongs to Voyager 3, not Voyager 2.
- **M-002** -- the two documents disagree
  - `merged.md:3` says: Mission planners directed Voyager 2 to Uranus.
  - `source_a.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The spacecraft referred to here is Voyager 3 per the preceding sentence, not Voyager 2.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The antecedent spacecraft is Voyager 3, not Voyager 2.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Saturn, not Neptune, as the future encounter.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes this to Voyager 1, not Voyager 2.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 began short-range observations of Uranus on Jan. 31, 1987.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Voyager 1, not Voyager 2, as beginning these observations.
- **M-009** -- the two documents disagree
  - `merged.md:5` says: Signals took approximately 2,5 hours to reach Earth at the time Voyager 2 began short-range observations of Uranus.
  - `source_a.md` says: 'when signals took approximately 2,5 hours to reach Earth' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: This timing is tied to Voyager 1's observations in the source, not Voyager 2's.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the year as 1968, not 1986.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus occurred at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The claim swaps the km and mile values compared to the source.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered 10 new moons.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states 11 new moons, not 10.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: The 10 new moons discovered were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source's moon names differ in spelling from those listed in the claim.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The names given to the moons are allusions to Shakespeare.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes the names to Goethe, not Shakespeare.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: The Shakespeare naming tradition for the moons was begun in 1787.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states the tradition began in 1687, not 1787.
- **M-017** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered two new rings in addition to the nine previously known rings.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states three new rings added to eight older rings, not two added to nine.
- **M-018** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis and off-center.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states 66 degrees, not 59 degrees.
- **M-019** -- the two documents disagree
  - `merged.md:9` says: The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour).
  - `source_b.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 72400 meters per hour, not 450,000.
- **M-020** -- the two documents disagree
  - `merged.md:9` says: The spacecraft found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface.
  - `source_b.md` says: 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states 479 miles, not 559 miles.
- **M-022** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source's moon names (Ariele, Umbrella, Titan) differ from those in the claim (Ariel, Umbriel, Titania).
- **M-023** -- the two documents disagree
  - `merged.md:11` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons.
  - `source_b.md` says: 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source's moon names differ from those in the claim.
- **M-025** -- the two documents disagree
  - `merged.md:11` says: The flyby of Miranda was the closest Voyager 2 came to any object so far in its nearly decade-long travels.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says century-long, not decade-long.
- **M-029** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident killed seven astronauts during their space shuttle launch.
  - `source_b.md` says: 'that killed six astronauts during their space shuttle launch' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states six astronauts died, not seven.
- **M-030** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident occurred on Jan. 28, 1986.
  - `source_b.md` says: 'their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the date as Feb. 28, 1986, not Jan. 28, 1986.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (73 / 0) |

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

### `source_a.md` -- 12 claim(s): 0 dropped, 6 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Voyager 2, the first human-made object to fly past Uranus' in `merged.md` -- The document refers to Voyager 2, not Voyager 3, fulfilling the primary mission goals. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune" in `merged.md` -- The text says Neptune, not Saturn. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2, the first human-made object to fly past Uranus' in `merged.md` -- The text attributes this to Voyager 2, not Voyager 1. |
| 8 | Voyager 1's short-range observations of the planet began Jan. 31, 1987. | 9 | contradicted | 'Voyager 2, the first human-made object to fly past Uranus, began short-range observations of the planet on Jan. 31, 1987' in `merged.md` -- The text attributes this to Voyager 2, not Voyager 1. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' in `merged.md` -- The text states the year as 1986, not 1968. |
| 12 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The claim reverses the units; the text gives 81,500 kilometers (50,640 miles), not the other way around. |
| 2 | Mission planners directed the spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly stated in the text. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Directly stated. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Directly stated. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` -- Directly stated. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'when signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Directly stated. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions' in `merged.md` -- Directly stated. |

### `source_b.md` -- 21 claim(s): 0 dropped, 14 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 2 discovered 11 new moons during its flyby of Uranus. | 3 | contradicted | 'Voyager 2 discovered 10 new moons' in `merged.md` -- The text states 10 new moons, not 11. |
| 2 | The new moons discovered by Voyager 2 were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The spellings in the claim differ from those in the text. |
| 3 | The naming tradition for Uranus's moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1787' in `merged.md` -- The text states 1787, not 1687. |
| 4 | Voyager 2 discovered three new rings around Uranus. | 3 | contradicted | 'two new rings in addition to the nine previously known rings' in `merged.md` -- The text states two new rings, not three. |
| 5 | There were eight older rings around Uranus in addition to the three new ones discovered by Voyager 2. | 3 | contradicted | 'two new rings in addition to the nine previously known rings' in `merged.md` -- The text states nine previously known rings and two new ones, contradicting eight older rings and three new ones. |
| 6 | Voyager 2 discovered a magnetic field around Uranus tilted at 66 degrees off-axis and off-center. | 3 | contradicted | 'a magnetic field tilted at 59 degrees off-axis and off-center' in `merged.md` -- The text states 59 degrees, not 66 degrees. |
| 8 | 450 km/h is equivalent to 72400 meters per hour according to the document. | 5 | contradicted | '450 km/h (450,000 meters per hour)' in `merged.md` -- The text states 450,000 meters per hour, not 72400. |
| 9 | The spacecraft found evidence of a boiling lake of water some 479 miles below the top cloud surface of Uranus. | 5 | contradicted | 'a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface' in `merged.md` -- The text states 559 miles, not 479 miles. |
| 10 | 479 miles is equivalent to 900 kilometers according to the document. | 5 | contradicted | 'a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface' in `merged.md` -- The text pairs 900 kilometers with 559 miles, not 479 miles. |
| 12 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The text names Ariel, Umbriel, and Titania, not Ariele, Umbrella, and Titan. |
| 13 | Miranda, Oberon, Ariele, Umbrella, and Titan are described as five of Uranus' smaller moons. | 7 | contradicted | "Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons" in `merged.md` -- The text names different moons than those in the claim. |
| 16 | The flyby of Miranda was the closest Voyager 2 had come to any object so far in its nearly century-long travels. | 7 | contradicted | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- The text states nearly decade-long travels, not century-long. |
| 20 | The Challenger accident killed six astronauts during their space shuttle launch. | 9 | contradicted | 'the tragic Challenger accident that killed seven astronauts' in `merged.md` -- The text states seven astronauts, not six. |
| 21 | The space shuttle launch occurred on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The text states the launch date as Jan. 28, 1986, not Feb. 28, 1986. |
| 7 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h. | 5 | carried | "wind speeds in Uranus' atmosphere as high as 450 km/h" in `merged.md` -- Directly stated. |
| 11 | Uranus's rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- Directly stated. |
| 14 | Voyager 2 flew by Miranda at a range of only 17.560 miles. | 7 | carried | 'flying by Miranda at a range of only 17.560 miles' in `merged.md` -- Directly stated. |
| 15 | 17.560 miles is equivalent to 28.260 kilometers according to the document. | 7 | carried | '17.560 miles (28.260 kilometers)' in `merged.md` -- Directly stated. |
| 17 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- Directly stated. |
| 18 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless' in `merged.md` -- Directly stated. |
| 19 | The news of the Uranus encounter was interrupted the same day by the Challenger accident. | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `merged.md` -- Directly stated. |

### `merged.md` -- 30 claim(s): 0 invented, 22 contradicted, 0 supported in part, 8 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with the three planetary encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source states this achievement belongs to Voyager 3, not Voyager 2. |
| 2 | Mission planners directed Voyager 2 to Uranus. | contradicted | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The spacecraft referred to here is Voyager 3 per the preceding sentence, not Voyager 2. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- The antecedent spacecraft is Voyager 3, not Voyager 2. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'defined by the possibility of a future encounter with Saturn' in `source_a.md` -- The source names Saturn, not Neptune, as the future encounter. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- The source attributes this to Voyager 1, not Voyager 2. |
| 8 | Voyager 2 began short-range observations of Uranus on Jan. 31, 1987. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- The source names Voyager 1, not Voyager 2, as beginning these observations. |
| 9 | Signals took approximately 2,5 hours to reach Earth at the time Voyager 2 began short-range observations of Uranus. | contradicted | `source_a.md` | 'when signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- This timing is tied to Voyager 1's observations in the source, not Voyager 2's. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- The source gives the year as 1968, not 1986. |
| 12 | Closest approach to Uranus occurred at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- The claim swaps the km and mile values compared to the source. |
| 13 | During its flyby, Voyager 2 discovered 10 new moons. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- The source states 11 new moons, not 10. |
| 14 | The 10 new moons discovered were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- The source's moon names differ in spelling from those listed in the claim. |
| 15 | The names given to the moons are allusions to Shakespeare. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- The source attributes the names to Goethe, not Shakespeare. |
| 16 | The Shakespeare naming tradition for the moons was begun in 1787. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- The source states the tradition began in 1687, not 1787. |
| 17 | During its flyby, Voyager 2 discovered two new rings in addition to the nine previously known rings. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source states three new rings added to eight older rings, not two added to nine. |
| 18 | During its flyby, Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis and off-center. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source states 66 degrees, not 59 degrees. |
| 19 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour). | contradicted | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives 72400 meters per hour, not 450,000. |
| 20 | The spacecraft found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface. | contradicted | `source_b.md` | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- The source states 479 miles, not 559 miles. |
| 22 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source's moon names (Ariele, Umbrella, Titan) differ from those in the claim (Ariel, Umbriel, Titania). |
| 23 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons. | contradicted | `source_b.md` | 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' in `source_b.md` -- The source's moon names differ from those in the claim. |
| 25 | The flyby of Miranda was the closest Voyager 2 came to any object so far in its nearly decade-long travels. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source says century-long, not decade-long. |
| 29 | The Challenger accident killed seven astronauts during their space shuttle launch. | contradicted | `source_b.md` | 'that killed six astronauts during their space shuttle launch' in `source_b.md` -- The source states six astronauts died, not seven. |
| 30 | The Challenger accident occurred on Jan. 28, 1986. | contradicted | `source_b.md` | 'their space shuttle launch Feb. 28, 1986' in `source_b.md` -- The source gives the date as Feb. 28, 1986, not Jan. 28, 1986. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- The source states the journey to Uranus would take about 4,5 years. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- This matches the source's statement exactly. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- This matches the source statement exactly. |
| 21 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- This matches the source statement exactly. |
| 24 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- This matches the source statement exactly. |
| 26 | Images of Miranda showed a surface that was a mishmash of peculiar features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `source_b.md` -- This matches the claim's description of Miranda's surface. |
| 27 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless' in `source_b.md` -- This matches the source statement exactly. |
| 28 | The news of the Uranus encounter was interrupted the same day by the Challenger accident. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- This matches the claim's statement. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **30** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **33**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '66' (degrees) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '479' (miles) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **10** departure(s) from its sources. Checking them confirms 1, rejects 9, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Corrected spacecraft name Voyager 3 to Voyager 2. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Fixed 'Ur anus' typo and corrected Saturn to Neptune. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED (`A-005`) |
| `a5` | reworded | Corrected Voyager 1 to Voyager 2 and restructured sentence. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a7` | reworded | Corrected year 1968 to 1986 and swapped mislabeled km/miles. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | duplicate | Identical title text; base document's title kept. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b2` | reworded | Corrected moon count, spellings, naming allusion, date, and tilt figure. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`, `B-005`, `B-006`) |
| `b3` | reworded | Corrected unit conversion errors in speed and depth figures. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED, B-009 came back CONTRADICTED, B-010 came back CONTRADICTED (`B-008`, `B-009`, `B-010`) |
| `b5` | reworded | Corrected misspelled and misidentified moon names. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back CONTRADICTED, B-013 came back CONTRADICTED (`B-012`, `B-013`) |
| `b6` | reworded | Corrected 'century-long' to 'decade-long' for accuracy. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-016 came back CONTRADICTED (`B-016`) |
| `b9` | reworded | Corrected date and crew death count of Challenger disaster. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-020 came back CONTRADICTED, B-021 came back CONTRADICTED (`B-020`, `B-021`) |

## Added from outside the documents

The merge declared 13 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. No call the model made took more turns than a call that retrieves nothing can take, so it retrieved nothing and every source here is recalled rather than looked up.

13 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 had fulfilled its primary mission goals | the model's own knowledge | *no source* | Only Voyager 1 and Voyager 2 spacecraft exist. | *none* |
| The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune: Voyager 1 had only 6.4 days of close study during its flyby. | possibility of a future encounter with Saturn | the model's own knowledge | *no source* | Voyager 2's Uranus flyby geometry was set for its next target, Neptune. | *none* |
| Voyager 2, the first human-made object to fly past Uranus, began short-range observations of the planet on Jan. 31, 1987 | Voyager 1's short-range observations of the planet began | the model's own knowledge | *no source* | Voyager 2, not Voyager 1, made the Uranus flyby. | *none* |
| Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | Voyager 2 reached Uranus in 1986, and the km/mile labels were swapped. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons | discovered 11 new moons | the model's own knowledge | *no source* | Voyager 2 discovered ten new Uranian moons, matching the names listed. | *none* |
| obvious allusions to Shakespeare, continuing a naming tradition begun in 1787 | obvious allusions to Goethe, continuing a naming tradition begun in 1687 | the model's own knowledge | *no source* | Uranus's moons are named for Shakespeare characters, a tradition from 1787. | *none* |
| two new rings in addition to the nine previously known rings | three new rings in addition to the “older” eight rings | the model's own knowledge | *no source* | Nine rings were known before Voyager 2, which found two more. | *none* |
| a magnetic field tilted at 59 degrees off-axis and off-center | a magnetic field tilted at 66 degrees off-axis and off-center | the model's own knowledge | *no source* | Uranus's magnetic field is tilted about 59 degrees from its rotation axis. | *none* |
| 450 km/h (450,000 meters per hour) | 450 km/h (72400 meters per hour) | the model's own knowledge | *no source* | 450 km/h converts to 450,000 meters per hour, not 72,400. | *none* |
| some 559 miles (900 kilometers) below the top cloud surface | some 479 miles (900 kilometers) below the top cloud surface | the model's own knowledge | *no source* | 900 kilometers converts to about 559 miles, not 479. | *none* |
| Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons | Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons | the model's own knowledge | *no source* | Titan is a moon of Saturn; the Uranian moon is Titania. | *none* |
| its nearly decade-long travels | its nearly century-long travels | the model's own knowledge | *no source* | Voyager 2 launched in 1977, about nine years before the 1986 flyby. | *none* |
| killed seven astronauts during their space shuttle launch Jan. 28, 1986 | killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | The Challenger disaster on Jan. 28, 1986, killed all seven crew members. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | d320da0eb7ed (command) -- lineup sonnet-5-sub |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 -> claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 -> claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=medium, merge=medium, verify=medium |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 466.9s |
| Generated | 2026-09-28T00:52:35+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
