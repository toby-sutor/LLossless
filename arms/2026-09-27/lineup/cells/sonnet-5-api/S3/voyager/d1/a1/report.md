## Verdict

**44 finding(s).** In the claims: 37 contradicted. In the structure: 7 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 28 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 19 |
| Forward — source claims accounted for in the merge | **13/31** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **5/12** |
| Forward — `source_b.md` claims accounted for | **8/19** |
| Reverse — merge claims found in a source | **9/28** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **59/59** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters at Jupiter and Saturn' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text names Voyager 2 with two encounters, not Voyager 3 with three.
- **A-004** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The 'its' refers to Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text specifies Neptune, not Saturn.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: "The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes this to Voyager 2, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of the planet began Jan. 31, 1987.
  - `merged.md` says: "Voyager 2's short-range observations of the planet began Jan. 31, 1986" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text names Voyager 2 and year 1986, not Voyager 1 and 1987.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives the year 1986, not 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The units are swapped: the text gives 81,500 km and 50,640 miles, not the reverse.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The 11 new moons were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The names differ in spelling from the claim's list.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The moon names are allusions to Goethe.
  - `merged.md` says: 'named after characters from the works of Shakespeare and Alexander Pope' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes the names to Shakespeare and Pope, not Goethe.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for the moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1787' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states the tradition began in 1787, not 1687.
- **B-008** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: "wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour)" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives 450,000 meters per hour, not 72400.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  - `merged.md` says: 'a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives 559 miles, not 479 miles.
- **B-011** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The names differ from the claim's list (Ariele, Umbrella, Titan).
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons.
  - `merged.md` says: "Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The moon names differ from the claim's list.
- **B-014** -- the two documents disagree
  - `source_b.md:7` says: The flyby of Miranda was the closest approach to any object so far in Voyager 2's nearly century-long travels.
  - `merged.md` says: 'the spacecraft came closest to any object so far in its nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text says 'nearly decade-long travels', not 'century-long', which contradicts the claim.
- **B-018** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states seven astronauts died, not six.
- **B-019** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during their space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text gives the date as Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the two planetary encounters at Jupiter and Saturn.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names the craft Voyager 3 and states three planetary encounters, not Voyager 2 with two encounters.
- **M-002** -- the two documents disagree
  - `merged.md:3` says: Mission planners directed Voyager 2 to Uranus.
  - `source_a.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The 'veteran spacecraft' referred to is the one just named Voyager 3 in the same sentence, not Voyager 2.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The pronoun 'its' refers back to the craft named Voyager 3 in the prior sentence, not Voyager 2.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states the future encounter possibility was with Saturn, not Neptune.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes being the first human-made object to fly past Uranus to Voyager 1, not Voyager 2.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's short-range observations of Uranus began Jan. 31, 1986.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Voyager 1 and gives the year 1987, not Voyager 2 and 1986.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives the year 1968 for closest approach, not 1986 as the claim states.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source pairs 50,640 kilometers with 81,500 miles, the reverse of the units given in the claim.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered 10 new moons during its flyby of Uranus.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 11 new moons were discovered, not 10.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: The 10 new moons discovered were named Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Several of the moon names in the claim differ from the names given in the source list.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The moons were named after characters from the works of Shakespeare and Alexander Pope.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes the naming to allusions to Goethe, not Shakespeare and Alexander Pope.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: The naming tradition began in 1787.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states the tradition began in 1687, not 1787.
- **M-019** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour).
  - `source_b.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source pairs 450 km/h with 72400 meters per hour, not 450,000 meters per hour as claimed.
- **M-020** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface.
  - `source_b.md` says: 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 479 miles, not 559 miles, paired with 900 kilometers.
- **M-022** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names the moons Ariele, Umbrella, and Titan, not Ariel, Umbriel, and Titania.
- **M-023** -- the two documents disagree
  - `merged.md:9` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons.
  - `source_b.md` says: 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source lists different moon names (Ariele, Umbrella, Titan) than those given in the claim.
- **M-025** -- the two documents disagree
  - `merged.md:9` says: Voyager 2's flyby of Miranda was its closest approach to any object so far in its nearly decade-long travels.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source describes the travels as nearly century-long, not nearly decade-long.
- **M-027** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident occurred during a space shuttle launch on Jan. 28, 1986.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b states the launch occurred Feb. 28, 1986, not Jan. 28, 1986 as the claim asserts.
- **M-028** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident killed seven astronauts.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b states six astronauts died, not seven as the claim asserts.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (75 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m5` (`merged.md`) - '2,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `m12` (`merged.md`) - '17.560' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m12` (`merged.md`) - '28.260' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

## Length capped

- `$.additions[4].reason` was 81 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 7 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters at Jupiter and Saturn' in `merged.md` -- The text names Voyager 2 with two encounters, not Voyager 3 with three. |
| 4 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `merged.md` -- The 'its' refers to Voyager 2, not Voyager 3. |
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | 7 | contradicted | "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune" in `merged.md` -- The text specifies Neptune, not Saturn. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | "The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986" in `merged.md` -- The text attributes this to Voyager 2, not Voyager 1. |
| 8 | Voyager 1's short-range observations of the planet began Jan. 31, 1987. | 9 | contradicted | "Voyager 2's short-range observations of the planet began Jan. 31, 1986" in `merged.md` -- The text names Voyager 2 and year 1986, not Voyager 1 and 1987. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' in `merged.md` -- The text gives the year 1986, not 1968. |
| 12 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The units are swapped: the text gives 81,500 km and 50,640 miles, not the reverse. |
| 2 | Mission planners directed the veteran spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly stated. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Directly stated. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `merged.md` -- Directly stated. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Directly stated. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions.' in `merged.md` -- Directly stated. |

### `source_b.md` -- 19 claim(s): 0 dropped, 11 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 2 discovered 11 new moons during its flyby. | 3 | contradicted | 'Voyager 2 discovered 10 new moons' in `merged.md` -- The text states 10 new moons, not 11. |
| 2 | The 11 new moons were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The names differ in spelling from the claim's list. |
| 3 | The moon names are allusions to Goethe. | 3 | contradicted | 'named after characters from the works of Shakespeare and Alexander Pope' in `merged.md` -- The text attributes the names to Shakespeare and Pope, not Goethe. |
| 4 | The naming tradition for the moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1787' in `merged.md` -- The text states the tradition began in 1787, not 1687. |
| 8 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | "wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour)" in `merged.md` -- The text gives 450,000 meters per hour, not 72400. |
| 9 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | contradicted | 'a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface' in `merged.md` -- The text gives 559 miles, not 479 miles. |
| 11 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The names differ from the claim's list (Ariele, Umbrella, Titan). |
| 12 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 | contradicted | "Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons" in `merged.md` -- The moon names differ from the claim's list. |
| 14 | The flyby of Miranda was the closest approach to any object so far in Voyager 2's nearly century-long travels. | 7 | contradicted | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- The reference text says 'nearly decade-long travels', not 'century-long', which contradicts the claim. |
| 18 | The Challenger accident killed six astronauts. | 9 | contradicted | 'the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The reference text states seven astronauts died, not six. |
| 19 | The Challenger accident occurred during their space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The reference text gives the date as Jan. 28, 1986, not Feb. 28, 1986. |
| 5 | Voyager 2 discovered three new rings. | 3 | carried | 'three new rings in addition to the "older" eight rings' in `merged.md` -- Directly stated. |
| 6 | There were eight "older" rings in addition to the three new rings. | 3 | carried | 'three new rings in addition to the "older" eight rings' in `merged.md` -- Directly stated. |
| 7 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- Directly stated. |
| 10 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- Directly stated. |
| 13 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- Directly stated. |
| 15 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.' in `merged.md` -- The text directly states Miranda's surface was a mishmash of peculiar features. |
| 16 | Uranus appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- This is stated verbatim in the reference text. |
| 17 | News of the Uranus encounter was interrupted the same day by the Challenger accident. | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986.' in `merged.md` -- The text states the news was interrupted the same day by the Challenger accident. |

### `merged.md` -- 28 claim(s): 0 invented, 19 contradicted, 0 supported in part, 9 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with the two planetary encounters at Jupiter and Saturn. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source names the craft Voyager 3 and states three planetary encounters, not Voyager 2 with two encounters. |
| 2 | Mission planners directed Voyager 2 to Uranus. | contradicted | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The 'veteran spacecraft' referred to is the one just named Voyager 3 in the same sentence, not Voyager 2. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- The pronoun 'its' refers back to the craft named Voyager 3 in the prior sentence, not Voyager 2. |
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- Source states the future encounter possibility was with Saturn, not Neptune. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source attributes being the first human-made object to fly past Uranus to Voyager 1, not Voyager 2. |
| 8 | Voyager 2's short-range observations of Uranus began Jan. 31, 1986. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source names Voyager 1 and gives the year 1987, not Voyager 2 and 1986. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source gives the year 1968 for closest approach, not 1986 as the claim states. |
| 12 | Closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Source pairs 50,640 kilometers with 81,500 miles, the reverse of the units given in the claim. |
| 13 | Voyager 2 discovered 10 new moons during its flyby of Uranus. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Source states 11 new moons were discovered, not 10. |
| 14 | The 10 new moons discovered were named Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- Several of the moon names in the claim differ from the names given in the source list. |
| 15 | The moons were named after characters from the works of Shakespeare and Alexander Pope. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- Source attributes the naming to allusions to Goethe, not Shakespeare and Alexander Pope. |
| 16 | The naming tradition began in 1787. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- Source states the tradition began in 1687, not 1787. |
| 19 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour). | contradicted | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- Source pairs 450 km/h with 72400 meters per hour, not 450,000 meters per hour as claimed. |
| 20 | Voyager 2 found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface. | contradicted | `source_b.md` | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Source states 479 miles, not 559 miles, paired with 900 kilometers. |
| 22 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' in `source_b.md` -- Source names the moons Ariele, Umbrella, and Titan, not Ariel, Umbriel, and Titania. |
| 23 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons. | contradicted | `source_b.md` | 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' in `source_b.md` -- Source lists different moon names (Ariele, Umbrella, Titan) than those given in the claim. |
| 25 | Voyager 2's flyby of Miranda was its closest approach to any object so far in its nearly decade-long travels. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Source describes the travels as nearly century-long, not nearly decade-long. |
| 27 | The Challenger accident occurred during a space shuttle launch on Jan. 28, 1986. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source_b states the launch occurred Feb. 28, 1986, not Jan. 28, 1986 as the claim asserts. |
| 28 | The Challenger accident killed seven astronauts. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source_b states six astronauts died, not seven as the claim asserts. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Matches the source's stated travel time exactly. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- This is an exact match to the source text. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'when signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Matches the source's stated signal travel time exactly. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- Matches the source text exactly. |
| 17 | Voyager 2 discovered three new rings in addition to the "older" eight rings. | supported | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Matches the source text exactly. |
| 18 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Matches the source text exactly. |
| 21 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- Matches the source text exactly. |
| 24 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Matches the source text exactly. |
| 26 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- This exact statement appears verbatim in source_b.md. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **28** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **31**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '479' (miles) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **10** departure(s) from its sources. Checking them confirms 0, rejects 9, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Corrected nonexistent Voyager 3 and encounter count to Jupiter/Saturn. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Fixed 'Ur anus' typo and wrong 'Saturn' to Neptune. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED (`A-005`) |
| `a5` | reworded | Fixed craft name and encounter year. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a7` | reworded | Fixed encounter year and swapped km/mile figures. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | superseded | Base document's identical title was kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Fixed moon count, spellings, naming allusion and tradition date. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`) |
| `b3` | reworded | Fixed unit-conversion errors for speed and depth. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED, B-009 came back CONTRADICTED (`B-008`, `B-009`) |
| `b5` | reworded | Fixed misspelled names and wrong moon (Titan to Titania). | **rejected** | declared 'reworded', which predicts SUPPORTED; B-011 came back CONTRADICTED, B-012 came back CONTRADICTED (`B-011`, `B-012`) |
| `b6` | reworded | Fixed 'century-long' to 'decade-long'. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-014 came back CONTRADICTED (`B-014`) |
| `b9` | reworded | Fixed Challenger date and crew death toll. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-018 came back CONTRADICTED, B-019 came back CONTRADICTED (`B-018`, `B-019`) |

## Added from outside the documents

The merge declared 9 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

9 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters at Jupiter and Saturn, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters | the model's own knowledge | *no source* | No Voyager 3 exists; the primary mission covered only Jupiter and Saturn. | *none* |
| The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune: Voyager 1 had only 6.4 days of close study during its flyby. | a future encounter with Saturn | the model's own knowledge | *no source* | Voyager 2 had already passed Saturn before Uranus; Neptune was next. | *none* |
| The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986, when signals took approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | Voyager 1 never visited Uranus, and the flyby occurred in 1986. | *none* |
| Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | Voyager 2 flew by Uranus in 1986, at about 81,500 km altitude. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – named after characters from the works of Shakespeare and Alexander Pope, continuing a naming tradition begun in 1787), three new rings in addition to the "older" eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center. | discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687) | the model's own knowledge | *no source* | Voyager 2 found 10 moons named for Shakespeare/Pope characters, first found 1787 | *none* |
| The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour) and found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface. | as high as 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) | the model's own knowledge | *no source* | 450 km/h equals 450,000 m/h, and 900 km equals about 559 miles. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons. | Miranda, Oberon, Ariele, Umbrella, and Titan | the model's own knowledge | *no source* | Titan orbits Saturn; the Uranian moon is Titania, with spellings fixed. | *none* |
| In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels. | nearly century-long travels | the model's own knowledge | *no source* | Voyager 2 had traveled about nine years by the Uranus flyby, not a century. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | The Challenger disaster killed all seven crew on Jan. 28, 1986. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-sonnet-5 |
| Model (decompose) | claude-sonnet-5 |
| Model (verify) | claude-sonnet-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | 32,087 in, 50,045 out |
| Cost | ~$0.56 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 411.4s |
| Generated | 2026-09-27T17:59:29+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
