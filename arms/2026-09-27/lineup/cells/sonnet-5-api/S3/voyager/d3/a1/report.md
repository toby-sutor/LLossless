## Verdict

**39 finding(s).** In the claims: 29 contradicted, 2 partially invented. In the structure: 8 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 28 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 17 |
| Forward — source claims accounted for in the merge | **13/29** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **7/12** |
| Forward — `source_b.md` claims accounted for | **6/17** |
| Reverse — merge claims found in a source | **13/28** |
| Reverse — supported only in part | 2 |
| Evidence grounded | **57/57** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states Voyager 2, not Voyager 3, fulfilled its primary mission goals.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'The first human-made object to fly past Uranus, Voyager 2’s short-range observations of the planet began Jan. 31, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes this to Voyager 2, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of the planet began Jan. 31, 1987.
  - `merged.md` says: 'Voyager 2’s short-range observations of the planet began Jan. 31, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Voyager 2, and the year is 1986, not 1987 as claimed for Voyager 1.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives the year as 1986, not 1968 as claimed.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: The closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim swaps the units, stating 50,640 kilometers (81,500 miles), which contradicts the text's figures.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The 11 new moons were given names such as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim's names differ in spelling from those given in the text (e.g. Pucka vs Puck, Bianca II vs Bianca).
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for the moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1787' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states the tradition began in 1787, not 1687.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center.
  - `merged.md` says: 'a magnetic field tilted at 59 degrees off-axis and off-center' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 59 degrees, not 66 degrees.
- **B-006** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 km/h (450,000 meters per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 450,000 meters per hour, not 72400.
- **B-007** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  - `merged.md` says: 'a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 559 miles, not 479 miles.
- **B-009** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The moon names in the text differ from those in the claim (Ariel vs Ariele, Umbriel vs Umbrella, Titania vs Titan).
- **B-010** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons.
  - `merged.md` says: 'five of Uranus’ smaller moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The moons named in the text (Ariel, Umbriel, Titania) differ from those in the claim (Ariele, Umbrella, Titan).
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: The spacecraft came closest to any object so far in its nearly century-long travels when flying by Miranda.
  - `merged.md` says: 'the spacecraft came closest to any object so far in its nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says nearly decade-long, not century-long.
- **B-016** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'the tragic Challenger accident that killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states seven astronauts died, not six as claimed.
- **B-017** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states the launch occurred on Jan. 28, 1986, not Feb. 28, 1986 as claimed.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the three planetary encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes fulfilling the primary mission goals to Voyager 3, not Voyager 2.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The pronoun 'its' refers back to Voyager 3, the antecedent established in the prior sentence, not Voyager 2.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source credits Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's short-range observations of the planet began Jan. 31, 1986.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Voyager 1 and gives the year 1987, not Voyager 2 and 1986.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles).' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the year 1968, not 1986.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states 50,640 kilometers (81,500 miles), the claim reverses the km and mile figures.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered 10 new moons.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states 11 new moons, not 10.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The naming tradition for Uranus' moons was begun in 1787.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states the tradition began in 1687, not 1787.
- **M-017** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis and off-center.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states 66 degrees, not 59 degrees.
- **M-018** -- the two documents disagree
  - `merged.md:9` says: The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour).
  - `source_b.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 72400 meters per hour, not 450,000 meters per hour.
- **M-019** -- the two documents disagree
  - `merged.md:9` says: The spacecraft found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface.
  - `source_b.md` says: 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states 479 miles, not 559 miles.
- **M-024** -- the two documents disagree
  - `merged.md:11` says: The spacecraft came closest to any object so far in its nearly decade-long travels.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says 'century-long', not 'decade-long'.
- **M-028** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident killed seven astronauts during their space shuttle launch Jan. 28, 1986.
  - `source_b.md` says: 'that killed six astronauts during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source_b.md states six astronauts died on Feb. 28, 1986, not seven on Jan. 28, 1986 as the claim asserts.

### Partly invented — the sources carry some of this claim

- **M-021** (`merged.md:11`) — Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - evidence: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Miranda, Oberon and Ariel(e) are supported, but the source names 'Umbrella' and 'Titan' rather than Umbriel and Titania, a more substantial naming difference than simple typos.
- **M-022** (`merged.md:11`) — Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons.
  - evidence: 'five of Uranus’ smaller moons' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The 'five smaller moons' framing is supported, but the source's names for two of them (Umbrella, Titan) differ substantially from Umbriel and Titania.

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

### `source_a.md` -- 12 claim(s): 0 dropped, 5 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' in `merged.md` -- The text states Voyager 2, not Voyager 3, fulfilled its primary mission goals. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'The first human-made object to fly past Uranus, Voyager 2’s short-range observations of the planet began Jan. 31, 1986' in `merged.md` -- The text attributes this to Voyager 2, not Voyager 1. |
| 8 | Voyager 1's short-range observations of the planet began Jan. 31, 1987. | 9 | contradicted | 'Voyager 2’s short-range observations of the planet began Jan. 31, 1986' in `merged.md` -- The text says Voyager 2, and the year is 1986, not 1987 as claimed for Voyager 1. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' in `merged.md` -- The text gives the year as 1986, not 1968 as claimed. |
| 12 | The closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The claim swaps the units, stating 50,640 kilometers (81,500 miles), which contradicts the text's figures. |
| 2 | Mission planners directed the veteran spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly stated in the text. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Directly stated in the text. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Directly stated in the text. |
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | 7 | carried | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `merged.md` -- Directly stated in the text. |
| 6 | Voyager 1 had only 6.4 days of close study during Voyager 1's flyby. | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` -- Directly stated in the text. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'when signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Directly stated in the text. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions.' in `merged.md` -- Directly stated in the text. |

### `source_b.md` -- 17 claim(s): 0 dropped, 11 contradicted, 0 carried in part, 6 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 2 discovered 11 new moons during its flyby. | 3 | contradicted | 'Voyager 2 discovered 10 new moons' in `merged.md` -- The text states 10 new moons, not 11. |
| 2 | The 11 new moons were given names such as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The claim's names differ in spelling from those given in the text (e.g. Pucka vs Puck, Bianca II vs Bianca). |
| 3 | The naming tradition for the moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1787' in `merged.md` -- The text states the tradition began in 1787, not 1687. |
| 5 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | contradicted | 'a magnetic field tilted at 59 degrees off-axis and off-center' in `merged.md` -- The text states 59 degrees, not 66 degrees. |
| 6 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (450,000 meters per hour)' in `merged.md` -- The text states 450,000 meters per hour, not 72400. |
| 7 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | contradicted | 'a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface' in `merged.md` -- The text states 559 miles, not 479 miles. |
| 9 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The moon names in the text differ from those in the claim (Ariel vs Ariele, Umbriel vs Umbrella, Titania vs Titan). |
| 10 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 | contradicted | 'five of Uranus’ smaller moons' in `merged.md` -- The moons named in the text (Ariel, Umbriel, Titania) differ from those in the claim (Ariele, Umbrella, Titan). |
| 12 | The spacecraft came closest to any object so far in its nearly century-long travels when flying by Miranda. | 7 | contradicted | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- The text says nearly decade-long, not century-long. |
| 16 | The Challenger accident killed six astronauts. | 9 | contradicted | 'the tragic Challenger accident that killed seven astronauts' in `merged.md` -- The reference text states seven astronauts died, not six as claimed. |
| 17 | The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The reference text states the launch occurred on Jan. 28, 1986, not Feb. 28, 1986 as claimed. |
| 4 | Voyager 2 discovered three new rings in addition to the older eight rings. | 3 | carried | 'three new rings in addition to the “older” eight rings' in `merged.md` -- Directly stated in the text. |
| 8 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- Directly stated in the text. |
| 11 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- Directly stated in the text, matching exactly. |
| 13 | Images of Miranda showed a strange object whose surface was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.' in `merged.md` -- Directly stated in the text. |
| 14 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- The reference text states this exact claim verbatim. |
| 15 | The news of the Uranus encounter was interrupted the same day by the Challenger accident. | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986.' in `merged.md` -- The text confirms the news was interrupted the same day by the Challenger accident. |

### `merged.md` -- 28 claim(s): 0 invented, 13 contradicted, 2 supported in part, 13 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with the three planetary encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The source attributes fulfilling the primary mission goals to Voyager 3, not Voyager 2. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- The pronoun 'its' refers back to Voyager 3, the antecedent established in the prior sentence, not Voyager 2. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- The source credits Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus. |
| 8 | Voyager 2's short-range observations of the planet began Jan. 31, 1986. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- The source names Voyager 1 and gives the year 1987, not Voyager 2 and 1986. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles).' in `source_a.md` -- The source gives the year 1968, not 1986. |
| 12 | Closest approach to Uranus took place at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- The source states 50,640 kilometers (81,500 miles), the claim reverses the km and mile figures. |
| 13 | During its flyby, Voyager 2 discovered 10 new moons. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- The source states 11 new moons, not 10. |
| 15 | The naming tradition for Uranus' moons was begun in 1787. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- The source states the tradition began in 1687, not 1787. |
| 17 | Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis and off-center. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source states 66 degrees, not 59 degrees. |
| 18 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour). | contradicted | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives 72400 meters per hour, not 450,000 meters per hour. |
| 19 | The spacecraft found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface. | contradicted | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- The source states 479 miles, not 559 miles. |
| 24 | The spacecraft came closest to any object so far in its nearly decade-long travels. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source says 'century-long', not 'decade-long'. |
| 28 | The Challenger accident killed seven astronauts during their space shuttle launch Jan. 28, 1986. | contradicted | `source_b.md` | 'that killed six astronauts during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source_b.md states six astronauts died on Feb. 28, 1986, not seven on Jan. 28, 1986 as the claim asserts. |
| 21 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | supported in part | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- Miranda, Oberon and Ariel(e) are supported, but the source names 'Umbrella' and 'Titan' rather than Umbriel and Titania, a more substantial naming difference than simple typos. |
| 22 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons. | supported in part | `source_b.md` | 'five of Uranus’ smaller moons' in `source_b.md` -- The 'five smaller moons' framing is supported, but the source's names for two of them (Umbrella, Titan) differ substantially from Umbriel and Titania. |
| 2 | Mission planners directed the veteran spacecraft to Uranus. | supported | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The source states this directly. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Matches the source's stated travel time. |
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | supported | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- Matches the source statement, with the source's own spacing typo preserved. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- Directly matches the source. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'when signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Matches the source's stated signal travel time. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- Matches the source directly. |
| 14 | The new moons were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | supported | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- These are minor spelling variants of the same ten moon names listed in the claim, consistent with the document's typo pattern. |
| 16 | Voyager 2 discovered three new rings in addition to the older eight rings. | supported | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Matches the source directly. |
| 20 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- Matches the source directly, referring to Uranus's rings. |
| 23 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Matches the source's stated flyby range. |
| 25 | Images of the moon showed a strange object whose surface was a mishmash of peculiar features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `source_b.md` -- Matches the source's description directly. |
| 26 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- This exact statement appears in source_b.md. |
| 27 | The Uranus encounter news was interrupted the same day by the Challenger accident. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- Source_b.md states the encounter news was interrupted the same day by the Challenger accident. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **28** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **29**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '66' (degrees) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '479' (miles) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **10** departure(s) from its sources. Checking them confirms 1, rejects 8, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Corrected nonexistent Voyager 3 to Voyager 2. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Fixed 'Ur anus' typo to 'Uranus'. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-005`, `A-006`) |
| `a5` | reworded | Corrected spacecraft and year of Uranus encounter. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a7` | reworded | Fixed year and swapped mismatched km/mile labels. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | superseded | Duplicate title; base document's title kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Fixed moon count, names, naming allusion, year, and tilt figure. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-005 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-005`) |
| `b3` | reworded | Corrected two unit-conversion errors. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-006 came back CONTRADICTED, B-007 came back CONTRADICTED (`B-006`, `B-007`) |
| `b5` | reworded | Fixed spelling and replaced Saturn's moon Titan with Titania. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-009 came back CONTRADICTED, B-010 came back CONTRADICTED (`B-009`, `B-010`) |
| `b6` | reworded | Corrected travel duration from century- to decade-long. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back CONTRADICTED (`B-012`) |
| `b9` | reworded | Corrected Challenger date and crew count. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-016 came back CONTRADICTED, B-017 came back CONTRADICTED (`B-016`, `B-017`) |

## Added from outside the documents

The merge declared 15 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

15 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 had fulfilled its primary mission goals | the model's own knowledge | *no source* | There is no Voyager 3; only Voyager 1 and 2 exist. | *none* |
| The first human-made object to fly past Uranus, Voyager 2’s short-range observations of the planet began Jan. 31, 1986, when signals took approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations | the model's own knowledge | *no source* | Only Voyager 2, not Voyager 1, flew past Uranus. | *none* |
| The first human-made object to fly past Uranus, Voyager 2’s short-range observations of the planet began Jan. 31, 1986, when signals took approximately 2,5 hours to reach Earth. | began Jan. 31, 1987 | the model's own knowledge | *no source* | The Uranus encounter occurred in 1986, not 1987. | *none* |
| Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | Jan. 24, 1968 | the model's own knowledge | *no source* | Voyager 2's Uranus flyby occurred in 1986; it launched in 1977. | *none* |
| Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | Closest approach was 81,500 km (about 50,600 mi), not the reverse. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare and Alexander Pope, continuing a naming tradition begun in 1787), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | 11 new moons | the model's own knowledge | *no source* | Voyager 2 discovered 10 new Uranian moons, matching the list given. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare and Alexander Pope, continuing a naming tradition begun in 1787), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | obvious allusions to Goethe | the model's own knowledge | *no source* | Uranus's moons are named for Shakespeare and Pope characters, not Goethe. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare and Alexander Pope, continuing a naming tradition begun in 1787), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | naming tradition begun in 1687 | the model's own knowledge | *no source* | Herschel discovered the first two Uranian moons in 1787, not 1687. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare and Alexander Pope, continuing a naming tradition begun in 1787), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | magnetic field tilted at 66 degrees | the model's own knowledge | *no source* | Uranus's magnetic field is tilted about 59 degrees from its rotation axis. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (450,000 meters per hour) and found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface. | 72400 meters per hour | the model's own knowledge | *no source* | 450 km/h converts to 450,000 meters per hour, not 72,400. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (450,000 meters per hour) and found evidence of a boiling lake of water some 559 miles (900 kilometers) below the top cloud surface. | 479 miles (900 kilometers) | the model's own knowledge | *no source* | 900 kilometers converts to about 559 miles, not 479. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons. | Titan | the model's own knowledge | *no source* | Titan is a moon of Saturn; Uranus's fifth major moon is Titania. | *none* |
| In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels. | nearly century-long travels | the model's own knowledge | *no source* | Voyager 2 had been travelling under a decade by the 1986 encounter. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | Feb. 28, 1986 | the model's own knowledge | *no source* | The Challenger disaster occurred on Jan. 28, 1986, not February. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | killed six astronauts | the model's own knowledge | *no source* | The Challenger crew numbered seven, not six. | *none* |

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
| Tokens | 32,053 in, 60,209 out |
| Cost | ~$0.67 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 519.2s |
| Generated | 2026-09-27T19:56:08+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
