## Verdict

**45 finding(s).** In the claims: 38 contradicted. In the structure: 7 verbatim violation. 9 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 34 |
| Claims extracted from `source_a.md` | 13 |
| Claims extracted from `source_b.md` | 21 |
| Forward — source claims accounted for in the merge | **16/34** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **6/13** |
| Forward — `source_b.md` claims accounted for | **10/21** |
| Reverse — merge claims found in a source | **14/34** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **68/68** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes this to Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was defined in part by the possibility of a future encounter with Saturn.
  - `merged.md` says: "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text specifies Neptune, not Saturn, as the future encounter possibility.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: "The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes being first to fly past Uranus to Voyager 2, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: "Voyager 2's short-range observations of the planet began Jan. 31, 1986" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes these observations to Voyager 2, beginning in 1986, not Voyager 1 in 1987.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives the year as 1986, not 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus occurred at a range of about 50,640 kilometers.
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,600 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives 81,500 kilometers with 50,600 miles as the mile equivalent, not 50,640 kilometers.
- **A-013** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus occurred at a range of about 81,500 miles.
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,600 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 81,500 kilometers, not 81,500 miles; the mile figure given is 50,600.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its Uranus flyby.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The 11 new moons were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The names in the text differ in spelling and count from those in the claim.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The moon names are allusions to Goethe.
  - `merged.md` says: 'allusions to Shakespeare, continuing a naming tradition begun in 1852' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes the allusions to Shakespeare, not Goethe.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for Uranus' moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1852' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states the tradition began in 1852, not 1687.
- **B-008** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found wind speeds in Uranus' atmosphere as high as 72400 meters per hour.
  - `merged.md` says: '450 km/h (450.000 meters per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 450.000 meters per hour, not 72400.
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'spectacular photos of Miranda, Ariel, Umbriel, Titania, and Oberon' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text lists Ariel, Umbriel, and Titania, not Ariele, Umbrella, and Titan as in the claim.
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons.
  - `merged.md` says: "Miranda, Ariel, Umbriel, Titania, and Oberon, five of Uranus' smaller moons" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text names Titania, not Titan, among the five smaller moons.
- **B-016** -- the two documents disagree
  - `source_b.md:7` says: The Miranda flyby was the closest Voyager 2 had come to any object in its nearly century-long travels.
  - `merged.md` says: 'the spacecraft came closest to any object so far in its nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says nearly decade-long travels, not century-long.
- **B-019** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts during their space shuttle launch.
  - `merged.md` says: 'the tragic Challenger accident that killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states seven astronauts were killed, not six.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: The Challenger space shuttle launch accident occurred on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives the date as Jan. 28, 1986, not Feb. 28, 1986.
- **B-021** -- the two documents disagree
  - `source_b.md:9` says: News of the Uranus encounter was interrupted the same day by the Challenger accident.
  - `merged.md` says: 'was overshadowed four days later by the tragic Challenger accident' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states the news was overshadowed four days later, not interrupted the same day.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with three planetary encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names the spacecraft Voyager 3, not Voyager 2.
- **M-002** -- the two documents disagree
  - `merged.md:3` says: Mission planners directed Voyager 2 to Uranus.
  - `source_a.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The 'veteran spacecraft' referenced is Voyager 3 per the preceding clause, not Voyager 2.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The pronoun 'its' refers to Voyager 3 from the prior sentence, not Voyager 2.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Saturn, not Neptune, as the future encounter possibility.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes this to Voyager 1, not Voyager 2.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's short-range observations of Uranus began Jan. 31, 1986.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives Voyager 1 and year 1987, not Voyager 2 and 1986.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states the year 1968, not 1986.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus occurred at a range of about 81,500 kilometers.
  - `source_a.md` says: 'a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: 81,500 is stated as miles, not kilometers.
- **M-013** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus occurred at a range of about 50,600 miles.
  - `source_a.md` says: 'a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The kilometer figure is 50,640, and 50,600 miles does not match either figure or unit.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered 10 new moons.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 11 new moons, not 10.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The 10 new moons discovered were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source's names differ from the claim's list (e.g. Pucka vs Puck, Kressida vs Cressida).
- **M-016** -- the two documents disagree
  - `merged.md:7` says: The moon names are allusions to Shakespeare.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes the naming allusions to Goethe, not Shakespeare.
- **M-017** -- the two documents disagree
  - `merged.md:7` says: The Shakespeare naming tradition for Uranus' moons was begun in 1852.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states the tradition began in 1687, not 1852.
- **M-021** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450.000 meters per hour.
  - `source_b.md` says: '(72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives 72400 meters per hour, not 450,000.
- **M-025** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 returned photos of Miranda, Ariel, Umbriel, Titania, and Oberon.
  - `source_b.md` says: 'spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source lists Umbrella and Titan, not Umbriel and Titania as in the claim.
- **M-026** -- the two documents disagree
  - `merged.md:11` says: Miranda, Ariel, Umbriel, Titania, and Oberon are five of Uranus' smaller moons.
  - `source_b.md` says: 'five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The five moons named in source differ from those in the claim (Umbrella/Titan vs Umbriel/Titania).
- **M-029** -- the two documents disagree
  - `merged.md:11` says: The Miranda flyby was the closest Voyager 2 came to any object so far in its nearly decade-long travels.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says nearly century-long, not decade-long.
- **M-032** -- the two documents disagree
  - `merged.md:13` says: The news of the Uranus encounter was overshadowed four days later by the Challenger accident.
  - `source_b.md` says: 'was interrupted the same day by the tragic Challenger accident' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says the accident happened the same day, not four days later.
- **M-033** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident killed seven astronauts during their space shuttle launch.
  - `source_b.md` says: 'that killed six astronauts during their space shuttle launch' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states six astronauts were killed, not seven.
- **M-034** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident occurred on Jan. 28, 1986.
  - `source_b.md` says: 'space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source dates the accident to Feb. 28, 1986, not Jan. 28.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (71 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m5` (`merged.md`) - '2,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `m9` (`merged.md`) - '450.000' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 450, a three-place fraction; in the decimal comma convention it is 450000. Which is meant is the author's call
- **readable two ways** `m12` (`merged.md`) - '17.560' (merged.md, line 11) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m12` (`merged.md`) - '28.260' (merged.md, line 11) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

## Length capped

- `$.additions[4].reason` was 82 characters, over the 80-character cap; capped to fit
- `$.additions[8].reason` was 81 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 13 claim(s): 0 dropped, 7 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' in `merged.md` -- The text attributes this to Voyager 2, not Voyager 3. |
| 5 | The Uranus encounter's geometry was defined in part by the possibility of a future encounter with Saturn. | 7 | contradicted | "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune" in `merged.md` -- The text specifies Neptune, not Saturn, as the future encounter possibility. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | "The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986" in `merged.md` -- The text attributes being first to fly past Uranus to Voyager 2, not Voyager 1. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | "Voyager 2's short-range observations of the planet began Jan. 31, 1986" in `merged.md` -- The text attributes these observations to Voyager 2, beginning in 1986, not Voyager 1 in 1987. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' in `merged.md` -- The text gives the year as 1986, not 1968. |
| 12 | Closest approach to Uranus occurred at a range of about 50,640 kilometers. | 9 | contradicted | 'at a range of about 81,500 kilometers (50,600 miles)' in `merged.md` -- The text gives 81,500 kilometers with 50,600 miles as the mile equivalent, not 50,640 kilometers. |
| 13 | Closest approach to Uranus occurred at a range of about 81,500 miles. | 9 | contradicted | 'at a range of about 81,500 kilometers (50,600 miles)' in `merged.md` -- The text states 81,500 kilometers, not 81,500 miles; the mile figure given is 50,600. |
| 2 | Mission planners directed the spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly states mission planners directed the spacecraft to Uranus. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Matches the claim exactly. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Matches the claim exactly. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` -- Matches the claim exactly. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Matches the claim exactly. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions.' in `merged.md` -- Matches the claim exactly. |

### `source_b.md` -- 21 claim(s): 0 dropped, 11 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 2 discovered 11 new moons during its Uranus flyby. | 3 | contradicted | 'Voyager 2 discovered 10 new moons' in `merged.md` -- The text states 10 new moons, not 11. |
| 2 | The 11 new moons were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The names in the text differ in spelling and count from those in the claim. |
| 3 | The moon names are allusions to Goethe. | 3 | contradicted | 'allusions to Shakespeare, continuing a naming tradition begun in 1852' in `merged.md` -- The text attributes the allusions to Shakespeare, not Goethe. |
| 4 | The naming tradition for Uranus' moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1852' in `merged.md` -- The text states the tradition began in 1852, not 1687. |
| 8 | The spacecraft found wind speeds in Uranus' atmosphere as high as 72400 meters per hour. | 5 | contradicted | '450 km/h (450.000 meters per hour)' in `merged.md` -- The text states 450.000 meters per hour, not 72400. |
| 12 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'spectacular photos of Miranda, Ariel, Umbriel, Titania, and Oberon' in `merged.md` -- The text lists Ariel, Umbriel, and Titania, not Ariele, Umbrella, and Titan as in the claim. |
| 13 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 | contradicted | "Miranda, Ariel, Umbriel, Titania, and Oberon, five of Uranus' smaller moons" in `merged.md` -- The text names Titania, not Titan, among the five smaller moons. |
| 16 | The Miranda flyby was the closest Voyager 2 had come to any object in its nearly century-long travels. | 7 | contradicted | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- The text says nearly decade-long travels, not century-long. |
| 19 | The Challenger accident killed six astronauts during their space shuttle launch. | 9 | contradicted | 'the tragic Challenger accident that killed seven astronauts' in `merged.md` -- The text states seven astronauts were killed, not six. |
| 20 | The Challenger space shuttle launch accident occurred on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The text gives the date as Jan. 28, 1986, not Feb. 28, 1986. |
| 21 | News of the Uranus encounter was interrupted the same day by the Challenger accident. | 9 | contradicted | 'was overshadowed four days later by the tragic Challenger accident' in `merged.md` -- The text states the news was overshadowed four days later, not interrupted the same day. |
| 5 | Voyager 2 discovered three new rings at Uranus in addition to the older eight rings. | 3 | carried | 'three new rings in addition to the "older" eight rings' in `merged.md` -- Matches the claim exactly. |
| 6 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center at Uranus. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- Matches the claim exactly. |
| 7 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h. | 5 | carried | "wind speeds in Uranus' atmosphere as high as 450 km/h" in `merged.md` -- Matches the claim exactly. |
| 9 | The spacecraft found evidence of a boiling lake of water some 479 miles below the top cloud surface. | 5 | carried | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- Matches the claim exactly. |
| 10 | The spacecraft found evidence of a boiling lake of water some 900 kilometers below the top cloud surface. | 5 | carried | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- Matches the claim exactly. |
| 11 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- Matches the claim exactly. |
| 14 | Voyager 2 flew by Miranda at a range of only 17.560 miles. | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles' in `merged.md` -- Matches the claim exactly. |
| 15 | Voyager 2 flew by Miranda at a range of only 28.260 kilometers. | 7 | carried | '(28.260 kilometers)' in `merged.md` -- Matches the claim exactly. |
| 17 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- Matches the claim exactly. |
| 18 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- Matches the claim exactly. |

### `merged.md` -- 34 claim(s): 0 invented, 20 contradicted, 0 supported in part, 14 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with three planetary encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source names the spacecraft Voyager 3, not Voyager 2. |
| 2 | Mission planners directed Voyager 2 to Uranus. | contradicted | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The 'veteran spacecraft' referenced is Voyager 3 per the preceding clause, not Voyager 2. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- The pronoun 'its' refers to Voyager 3 from the prior sentence, not Voyager 2. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- Source names Saturn, not Neptune, as the future encounter possibility. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source attributes this to Voyager 1, not Voyager 2. |
| 8 | Voyager 2's short-range observations of Uranus began Jan. 31, 1986. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source gives Voyager 1 and year 1987, not Voyager 2 and 1986. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source states the year 1968, not 1986. |
| 12 | Closest approach to Uranus occurred at a range of about 81,500 kilometers. | contradicted | `source_a.md` | 'a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- 81,500 is stated as miles, not kilometers. |
| 13 | Closest approach to Uranus occurred at a range of about 50,600 miles. | contradicted | `source_a.md` | 'a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- The kilometer figure is 50,640, and 50,600 miles does not match either figure or unit. |
| 14 | During its flyby, Voyager 2 discovered 10 new moons. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Source states 11 new moons, not 10. |
| 15 | The 10 new moons discovered were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- The source's names differ from the claim's list (e.g. Pucka vs Puck, Kressida vs Cressida). |
| 16 | The moon names are allusions to Shakespeare. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- Source attributes the naming allusions to Goethe, not Shakespeare. |
| 17 | The Shakespeare naming tradition for Uranus' moons was begun in 1852. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- Source states the tradition began in 1687, not 1852. |
| 21 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450.000 meters per hour. | contradicted | `source_b.md` | '(72400 meters per hour)' in `source_b.md` -- Source gives 72400 meters per hour, not 450,000. |
| 25 | Voyager 2 returned photos of Miranda, Ariel, Umbriel, Titania, and Oberon. | contradicted | `source_b.md` | 'spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Source lists Umbrella and Titan, not Umbriel and Titania as in the claim. |
| 26 | Miranda, Ariel, Umbriel, Titania, and Oberon are five of Uranus' smaller moons. | contradicted | `source_b.md` | 'five of Uranus’ smaller moons' in `source_b.md` -- The five moons named in source differ from those in the claim (Umbrella/Titan vs Umbriel/Titania). |
| 29 | The Miranda flyby was the closest Voyager 2 came to any object so far in its nearly decade-long travels. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Source says nearly century-long, not decade-long. |
| 32 | The news of the Uranus encounter was overshadowed four days later by the Challenger accident. | contradicted | `source_b.md` | 'was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- Source says the accident happened the same day, not four days later. |
| 33 | The Challenger accident killed seven astronauts during their space shuttle launch. | contradicted | `source_b.md` | 'that killed six astronauts during their space shuttle launch' in `source_b.md` -- Source states six astronauts were killed, not seven. |
| 34 | The Challenger accident occurred on Jan. 28, 1986. | contradicted | `source_b.md` | 'space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source dates the accident to Feb. 28, 1986, not Jan. 28. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Matches the stated travel time exactly. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- Exact match to the source text. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Matches the stated signal travel time. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- Exact match. |
| 18 | During its flyby, Voyager 2 discovered three new rings in addition to the older eight rings. | supported | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Matches the claim exactly. |
| 19 | During its flyby, Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Exact match. |
| 20 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h. | supported | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h' in `source_b.md` -- Matches source directly. |
| 22 | Voyager 2 found evidence of a boiling lake of water some 479 miles below the top cloud surface. | supported | `source_b.md` | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Matches the 479 miles figure. |
| 23 | Voyager 2 found evidence of a boiling lake of water some 900 kilometers below the top cloud surface. | supported | `source_b.md` | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Matches the 900 kilometers figure. |
| 24 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- Exact match. |
| 27 | Voyager 2 flew by Miranda at a range of only 17.560 miles. | supported | `source_b.md` | 'flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Exact match. |
| 28 | Voyager 2 flew by Miranda at a range of only 28.260 kilometers. | supported | `source_b.md` | 'flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Exact match. |
| 30 | Images of Miranda showed a surface that was a mishmash of peculiar features. | supported | `source_b.md` | 'a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason' in `source_b.md` -- Matches the claim. |
| 31 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless' in `source_b.md` -- Exact match. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **34** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **34**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '50,640' (kilometers) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **10** departure(s) from its sources. Checking them confirms 0, rejects 9, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Corrected nonexistent 'Voyager 3' to 'Voyager 2' | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Corrected 'Saturn' to 'Neptune' for chronological sense | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED (`A-005`) |
| `a5` | reworded | Corrected spacecraft name and encounter year | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a7` | reworded | Corrected year and swapped mismatched km/mile figures | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED, A-013 came back CONTRADICTED (`A-011`, `A-012`, `A-013`) |
| `b1` | superseded | Identical title kept once, from the base document | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Corrected moon count, names, allusion, and naming-tradition year | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`) |
| `b3` | reworded | Corrected unit-conversion arithmetic error | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED (`B-008`) |
| `b5` | reworded | Corrected misspelled/misattributed moon names | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back CONTRADICTED, B-013 came back CONTRADICTED (`B-012`, `B-013`) |
| `b6` | reworded | Corrected 'century-long' to match actual mission timespan | **rejected** | declared 'reworded', which predicts SUPPORTED; B-016 came back CONTRADICTED (`B-016`) |
| `b9` | reworded | Corrected Challenger date, death toll, and timing relative to flyby | **rejected** | declared 'reworded', which predicts SUPPORTED; B-019 came back CONTRADICTED, B-020 came back CONTRADICTED, B-021 came back CONTRADICTED (`B-019`, `B-020`, `B-021`) |

## Added from outside the documents

The merge declared 9 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. No call the model made took more turns than a call that retrieves nothing can take, so it retrieved nothing and every source here is recalled rather than looked up.

9 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| mission planners directed the veteran spacecraft to Uranus | Voyager 3 had fulfilled its primary mission goals | the model's own knowledge | *no source* | Only two Voyager probes were ever launched; no Voyager 3 exists | *none* |
| The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune | possibility of a future encounter with Saturn | the model's own knowledge | *no source* | Saturn preceded Uranus in Voyager 2's itinerary; Neptune came next | *none* |
| Voyager 2's short-range observations of the planet began Jan. 31, 1986 | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | Only Voyager 2 visited Uranus, in 1986, not 1987 | *none* |
| Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986, at a range of about 81,500 kilometers (50,600 miles) | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | Voyager 2 launched in 1977, so 1968 is impossible; km/mi figures were swapped | *none* |
| Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – allusions to Shakespeare, continuing a naming tradition begun in 1852) | discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687) | cited | IAU Working Group for Planetary System Nomenclature, Uranian satellite naming convention | Uranus's moons are named for Shakespearean/Popean characters, tradition began 18 | *none* |
| wind speeds in Uranus' atmosphere as high as 450 km/h (450.000 meters per hour) | 450 km/h (72400 meters per hour) | the model's own knowledge | *no source* | 450 kilometers equals 450,000 meters, not 72,400 | *none* |
| photos of Miranda, Ariel, Umbriel, Titania, and Oberon, five of Uranus' smaller moons | photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons | the model's own knowledge | *no source* | Titan is a moon of Saturn; Uranus's major moons are named differently | *none* |
| the spacecraft came closest to any object so far in its nearly decade-long travels | nearly century-long travels | the model's own knowledge | *no source* | Voyager 2 launched in 1977, about nine years before the Uranus flyby | *none* |
| overshadowed four days later by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986 | interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger disaster killed seven crew on Jan. 28, 1986, four days after the flyb | *none* |

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
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 280.3s |
| Generated | 2026-09-27T21:43:51+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
