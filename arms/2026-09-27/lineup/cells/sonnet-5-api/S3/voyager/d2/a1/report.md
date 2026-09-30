## Verdict

**40 finding(s).** In the claims: 33 contradicted. In the structure: 7 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 27 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 16 |
| Forward — source claims accounted for in the merge | **13/28** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **6/12** |
| Forward — `source_b.md` claims accounted for | **7/16** |
| Reverse — merge claims found in a source | **9/27** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **55/55** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes this to Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text names Neptune, not Saturn, as the future encounter.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2, the first human-made object to fly past Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text attributes this milestone to Voyager 2, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of the planet began Jan. 31, 1987.
  - `merged.md` says: 'began its short-range observations of the planet on Jan. 31, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text attributes this to Voyager 2 in 1986, not Voyager 1 in 1987.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 ED on Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states the year as 1986, not 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text has the units reversed compared to the claim.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The 11 new moons were given names such as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The moon names differ from those listed in the claim.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for Uranus' moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1787' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states 1787, not 1687.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center.
  - `merged.md` says: 'a magnetic field tilted at 59 degrees off-axis and off-center' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states 59 degrees, not 66 degrees.
- **B-006** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'as high as 450 km/h (450,000 meters per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states 450,000 meters per hour, not 72400.
- **B-007** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  - `merged.md` says: 'a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states 559 miles, not 479 miles.
- **B-009** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons.
  - `merged.md` says: 'spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The moon names in the text differ from the misspelled names in the claim.
- **B-011** -- the two documents disagree
  - `source_b.md:7` says: The spacecraft came closest to any object so far in its nearly century-long travels when flying by Miranda.
  - `merged.md` says: 'the spacecraft came closest to any object so far in its nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states decade-long, not century-long.
- **B-015** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'the tragic Challenger accident that killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states seven astronauts were killed, not six.
- **B-016** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch on Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text gives the date as Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the three planetary encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names the spacecraft as Voyager 3, not Voyager 2, a different name for the same attribute.
- **M-002** -- the two documents disagree
  - `merged.md:3` says: Mission planners directed Voyager 2 to Uranus.
  - `source_a.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The 'veteran spacecraft' refers back to Voyager 3 named in the same sentence, not Voyager 2.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The pronoun 'its' refers to the previously named Voyager 3, not Voyager 2 as claimed.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Saturn, not Neptune, as the future encounter.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Voyager 1, not Voyager 2, as the first object to fly past Uranus.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 began its short-range observations of Uranus on Jan. 31, 1986.
  - `source_a.md` says: 'began Jan. 31, 1987' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives 1987, not 1986, as the year observations began.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 ED on Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states the year 1968, not 1986 as claimed.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Claim reverses the units, stating 81,500 kilometers (50,640 miles) instead of the source's 50,640 kilometers (81,500 miles).
- **M-014** -- the two documents disagree
  - `merged.md:7` says: The new moons discovered were given names including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source's list of moon names differs substantially from the names given in the claim.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The moon names are allusions to characters from Shakespeare and Alexander Pope.
  - `source_b.md` says: 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes the allusions to Goethe, not Shakespeare and Alexander Pope.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: The moon naming tradition began in 1787.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states the tradition began in 1687, not 1787.
- **M-018** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis and off-center.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 66 degrees, not 59 degrees as claimed.
- **M-019** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour).
  - `source_b.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives 72400 meters per hour, not 450,000 as claimed.
- **M-020** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface.
  - `source_b.md` says: 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 479 miles, not 559 miles as claimed.
- **M-022** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source's moon names (Ariele, Umbrella, Titan) differ from the claim's Ariel, Umbriel, and Titania.
- **M-023** -- the two documents disagree
  - `merged.md:11` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons.
  - `source_b.md` says: 'five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The specific moon names in the source differ from those in the claim, as noted for M-022.
- **M-025** -- the two documents disagree
  - `merged.md:11` says: The flyby of Miranda was the closest Voyager 2 had come to any object so far in its nearly decade-long travels.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 'century-long', not 'decade-long' as claimed.
- **M-027** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident killed seven astronauts during their space shuttle launch on Jan. 28, 1986.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states six astronauts died on Feb. 28, 1986, not seven on Jan. 28, 1986.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (78 / 0) |

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
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' in `merged.md` -- The text attributes this to Voyager 2, not Voyager 3. |
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' in `merged.md` -- Text names Neptune, not Saturn, as the future encounter. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2, the first human-made object to fly past Uranus' in `merged.md` -- Text attributes this milestone to Voyager 2, not Voyager 1. |
| 8 | Voyager 1's short-range observations of the planet began Jan. 31, 1987. | 9 | contradicted | 'began its short-range observations of the planet on Jan. 31, 1986' in `merged.md` -- Text attributes this to Voyager 2 in 1986, not Voyager 1 in 1987. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 ED on Jan. 24, 1986' in `merged.md` -- Text states the year as 1986, not 1968. |
| 12 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- Text has the units reversed compared to the claim. |
| 2 | Mission planners directed the veteran spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly stated in the text. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Directly stated in the text. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Directly stated in the text. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` -- Directly stated in the text. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'when signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Directly stated in the text. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions' in `merged.md` -- Directly stated in the text. |

### `source_b.md` -- 16 claim(s): 0 dropped, 9 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | The 11 new moons were given names such as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The moon names differ from those listed in the claim. |
| 3 | The naming tradition for Uranus' moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1787' in `merged.md` -- Text states 1787, not 1687. |
| 5 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | contradicted | 'a magnetic field tilted at 59 degrees off-axis and off-center' in `merged.md` -- Text states 59 degrees, not 66 degrees. |
| 6 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'as high as 450 km/h (450,000 meters per hour)' in `merged.md` -- Text states 450,000 meters per hour, not 72400. |
| 7 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | contradicted | 'a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface' in `merged.md` -- Text states 559 miles, not 479 miles. |
| 9 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons. | 7 | contradicted | 'spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons' in `merged.md` -- The moon names in the text differ from the misspelled names in the claim. |
| 11 | The spacecraft came closest to any object so far in its nearly century-long travels when flying by Miranda. | 7 | contradicted | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- Text states decade-long, not century-long. |
| 15 | The Challenger accident killed six astronauts. | 9 | contradicted | 'the tragic Challenger accident that killed seven astronauts' in `merged.md` -- The reference text states seven astronauts were killed, not six. |
| 16 | The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch on Jan. 28, 1986' in `merged.md` -- The reference text gives the date as Jan. 28, 1986, not Feb. 28, 1986. |
| 1 | Voyager 2 discovered 11 new moons during its flyby. | 3 | carried | 'Voyager 2 discovered 11 new moons' in `merged.md` -- Directly stated in the text. |
| 4 | Voyager 2 discovered three new rings in addition to the "older" eight rings. | 3 | carried | 'three new rings in addition to the “older” eight rings' in `merged.md` -- Directly stated in the text. |
| 8 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- Directly stated in the text. |
| 10 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- Directly stated in the text. |
| 12 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason' in `merged.md` -- Directly stated in the text. |
| 13 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless' in `merged.md` -- Directly stated in the text. |
| 14 | The news of the Uranus encounter was interrupted the same day by the Challenger accident. | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch on Jan. 28, 1986.' in `merged.md` -- The text states the Uranus encounter news was interrupted the same day by the Challenger accident. |

### `merged.md` -- 27 claim(s): 0 invented, 18 contradicted, 0 supported in part, 9 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with the three planetary encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source names the spacecraft as Voyager 3, not Voyager 2, a different name for the same attribute. |
| 2 | Mission planners directed Voyager 2 to Uranus. | contradicted | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The 'veteran spacecraft' refers back to Voyager 3 named in the same sentence, not Voyager 2. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- The pronoun 'its' refers to the previously named Voyager 3, not Voyager 2 as claimed. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- Source names Saturn, not Neptune, as the future encounter. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source names Voyager 1, not Voyager 2, as the first object to fly past Uranus. |
| 8 | Voyager 2 began its short-range observations of Uranus on Jan. 31, 1986. | contradicted | `source_a.md` | 'began Jan. 31, 1987' in `source_a.md` -- Source gives 1987, not 1986, as the year observations began. |
| 11 | Closest approach to Uranus took place at 17:59 ED on Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source states the year 1968, not 1986 as claimed. |
| 12 | Closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Claim reverses the units, stating 81,500 kilometers (50,640 miles) instead of the source's 50,640 kilometers (81,500 miles). |
| 14 | The new moons discovered were given names including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- The source's list of moon names differs substantially from the names given in the claim. |
| 15 | The moon names are allusions to characters from Shakespeare and Alexander Pope. | contradicted | `source_b.md` | 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' in `source_b.md` -- Source attributes the allusions to Goethe, not Shakespeare and Alexander Pope. |
| 16 | The moon naming tradition began in 1787. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- Source states the tradition began in 1687, not 1787. |
| 18 | Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis and off-center. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Source states 66 degrees, not 59 degrees as claimed. |
| 19 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour). | contradicted | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- Source gives 72400 meters per hour, not 450,000 as claimed. |
| 20 | Voyager 2 found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface. | contradicted | `source_b.md` | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Source states 479 miles, not 559 miles as claimed. |
| 22 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Source's moon names (Ariele, Umbrella, Titan) differ from the claim's Ariel, Umbriel, and Titania. |
| 23 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons. | contradicted | `source_b.md` | 'five of Uranus’ smaller moons' in `source_b.md` -- The specific moon names in the source differ from those in the claim, as noted for M-022. |
| 25 | The flyby of Miranda was the closest Voyager 2 had come to any object so far in its nearly decade-long travels. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Source states 'century-long', not 'decade-long' as claimed. |
| 27 | The Challenger accident killed seven astronauts during their space shuttle launch on Jan. 28, 1986. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source states six astronauts died on Feb. 28, 1986, not seven on Jan. 28, 1986. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Source states the same duration exactly. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- Exact match to source statement. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Matches source's statement exactly. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- Matches source's statement exactly. |
| 13 | Voyager 2 discovered 11 new moons during its flyby of Uranus. | supported | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Matches source's statement exactly. |
| 17 | Voyager 2 discovered three new rings at Uranus in addition to the older eight rings. | supported | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Matches source's statement exactly. |
| 21 | Uranus's rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- Matches source's statement about Uranus's rings. |
| 24 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Matches source's statement exactly. |
| 26 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- This is a verbatim statement from source_b.md. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **27** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **28**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '66' (degrees) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '479' (miles) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **10** departure(s) from its sources. Checking them confirms 0, rejects 9, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Corrected spacecraft name from nonexistent Voyager 3 to Voyager 2. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Fixed 'Ur anus' typo and corrected future target from Saturn to Neptune. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED (`A-005`) |
| `a5` | reworded | Corrected spacecraft name and year to match Voyager 2's 1986 flyby. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a7` | reworded | Corrected year (1968→1986) and swapped mismatched km/mi figures. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | superseded | Duplicate of base title; base's title retained. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Fixed moon-name spellings, naming tradition, start year, and tilt angle. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-005 came back CONTRADICTED (`B-002`, `B-003`, `B-005`) |
| `b3` | reworded | Corrected unit conversions for wind speed and lake depth. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-006 came back CONTRADICTED, B-007 came back CONTRADICTED (`B-006`, `B-007`) |
| `b5` | reworded | Corrected moon names; Titan belongs to Saturn, not Uranus. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-009 came back CONTRADICTED (`B-009`) |
| `b6` | reworded | Corrected 'century-long' to 'decade-long' travel duration. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-011 came back CONTRADICTED (`B-011`) |
| `b9` | reworded | Corrected Challenger date and crew death toll. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-015 came back CONTRADICTED, B-016 came back CONTRADICTED (`B-015`, `B-016`) |

## Added from outside the documents

The merge declared 13 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

13 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 | the model's own knowledge | *no source* | No Voyager 3 spacecraft exists; the document concerns Voyager 2. | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 1 had only 6.4 days of close study during its flyby. | a future encounter with Saturn | the model's own knowledge | *no source* | Voyager 2 visited Saturn before Uranus; Neptune was the next target. | *none* |
| Voyager 2, the first human-made object to fly past Uranus, began its short-range observations of the planet on Jan. 31, 1986, when signals took approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | Voyager 2, not Voyager 1, flew past Uranus, and did so in 1986. | *none* |
| Closest approach to Uranus took place at 17:59 ED on Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles). | the model's own knowledge | *no source* | The flyby occurred in 1986, and 81,500 km equals about 50,640 miles. | *none* |
| During its flyby, Voyager 2 discovered 11 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca — allusions to characters from Shakespeare and Alexander Pope, continuing a naming tradition begun in 1787), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | obvious allusions to Goethe, continuing a naming tradition begun in 1687 | the model's own knowledge | *no source* | Uranus's moons are named after Shakespeare/Pope characters, begun 1787. | *none* |
| During its flyby, Voyager 2 discovered 11 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca — allusions to characters from Shakespeare and Alexander Pope, continuing a naming tradition begun in 1787), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | a magnetic field tilted at 66 degrees off-axis and off-center | the model's own knowledge | *no source* | Uranus's magnetic dipole is tilted about 59° from its rotation axis. | *none* |
| During its flyby, Voyager 2 discovered 11 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca — allusions to characters from Shakespeare and Alexander Pope, continuing a naming tradition begun in 1787), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II | the model's own knowledge | *no source* | These are misspellings of the real Uranian moon names. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (450,000 meters per hour) and found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface. | 72400 meters per hour | the model's own knowledge | *no source* | 450 km/h equals 450,000 meters per hour, not 72,400. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (450,000 meters per hour) and found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface. | 479 miles | the model's own knowledge | *no source* | 900 kilometers equals about 559 miles, not 479. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons. | Ariele, Umbrella, and Titan | the model's own knowledge | *no source* | Titan is Saturn's moon; the Uranian moons are Ariel, Umbriel, Titania. | *none* |
| In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels. | nearly century-long travels | the model's own knowledge | *no source* | Voyager 2 had been traveling only about nine years by 1986. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch on Jan. 28, 1986. | Feb. 28, 1986 | the model's own knowledge | *no source* | The Challenger disaster occurred on Jan. 28, 1986. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch on Jan. 28, 1986. | killed six astronauts | the model's own knowledge | *no source* | All seven Challenger crew members died in the accident. | *none* |

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
| Tokens | 32,019 in, 51,430 out |
| Cost | ~$0.58 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 430.8s |
| Generated | 2026-09-27T19:28:50+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
