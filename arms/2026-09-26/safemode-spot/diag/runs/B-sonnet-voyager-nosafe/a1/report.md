## Verdict

**24 finding(s).** In the claims: 19 contradicted. In the structure: 5 verbatim violation. **Nothing was retrieved.** This run was made at fidelity sourced, which asks the model to retrieve rather than recall, and none of its 6 call(s) took the turns a retrieval costs, so every source it names is a recollection, exactly as it would be at open. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 30 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 19 |
| Forward — source claims accounted for in the merge | **21/31** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **5/12** |
| Forward — `source_b.md` claims accounted for | **16/19** |
| Reverse — merge claims found in a source | **21/30** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **61/61** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Ur anus encounter's geometry was also defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Neptune, not Saturn.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby.
  - `merged.md` says: 'Voyager 2 had only 6.4 days of close study during its flyby.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Voyager 2, not Voyager 1.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: "The first human-made object to fly past Uranus, Voyager 2's short-range observations" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes this to Voyager 2, not Voyager 1.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: "Voyager 2's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text names Voyager 2, not Voyager 1, though the date matches.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives 1986, not 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The units are swapped: the text gives 81,500 km.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The moon names are allusions to Goethe.
  - `merged.md` says: 'obvious allusions to Shakespeare' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Shakespeare, not Goethe.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for Uranus' moons was begun in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1787' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says 1787, not 1687.
- **B-019** -- the two documents disagree
  - `source_b.md:9` says: The Challenger space shuttle launch took place on Feb. 28, 1986.
  - `merged.md` says: 'space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives Jan. 28, not Feb. 28.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the three planetary encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Voyager 3, not Voyager 2, as having fulfilled its goals.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says Saturn, not Neptune.
- **M-006** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had only 6.4 days of close study during its flyby.
  - `source_a.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes this to Voyager 1, not Voyager 2.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Voyager 1, not Voyager 2.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's short-range observations of Uranus began Jan. 31, 1987.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes the observations to Voyager 1 rather than Voyager 2.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives the year 1968, not 1986.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives 50,640 km and 81,500 miles, the reverse of the claim.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The moon names are allusions to Shakespeare, continuing a naming tradition begun in 1787.
  - `source_b.md` says: 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says Goethe and 1687, not Shakespeare and 1787.
- **M-030** -- the two documents disagree
  - `merged.md:13` says: The Challenger space shuttle launch was on Jan. 28, 1986.
  - `source_b.md` says: 'space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives Feb. 28, not Jan. 28.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (72 / 0) |

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

### `source_a.md` -- 12 claim(s): 0 dropped, 7 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' in `merged.md` -- The text says Voyager 2, not Voyager 3. |
| 5 | The Ur anus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' in `merged.md` -- The text says Neptune, not Saturn. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | contradicted | 'Voyager 2 had only 6.4 days of close study during its flyby.' in `merged.md` -- The text says Voyager 2, not Voyager 1. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | "The first human-made object to fly past Uranus, Voyager 2's short-range observations" in `merged.md` -- The text attributes this to Voyager 2, not Voyager 1. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | "Voyager 2's short-range observations of the planet began Jan. 31, 1987" in `merged.md` -- The text names Voyager 2, not Voyager 1, though the date matches. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' in `merged.md` -- The text gives 1986, not 1968. |
| 12 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The units are swapped: the text gives 81,500 km. |
| 2 | Mission planners directed the spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly stated. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Directly stated. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Directly stated. |
| 9 | Signals took approximately 2,5 hours to reach Earth when the short-range observations began. | 9 | carried | 'when signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Directly stated. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions.' in `merged.md` -- Directly stated. |

### `source_b.md` -- 19 claim(s): 0 dropped, 3 contradicted, 0 carried in part, 16 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 3 | The moon names are allusions to Goethe. | 3 | contradicted | 'obvious allusions to Shakespeare' in `merged.md` -- The text says Shakespeare, not Goethe. |
| 4 | The naming tradition for Uranus' moons was begun in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1787' in `merged.md` -- The text says 1787, not 1687. |
| 19 | The Challenger space shuttle launch took place on Feb. 28, 1986. | 9 | contradicted | 'space shuttle launch Jan. 28, 1986' in `merged.md` -- The text gives Jan. 28, not Feb. 28. |
| 1 | During its flyby, Voyager 2 discovered 11 new moons. | 3 | carried | 'Voyager 2 discovered 11 new moons' in `merged.md` -- Directly stated. |
| 2 | The new moons discovered by Voyager 2 were given names such as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | carried | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `merged.md` -- Names match. |
| 5 | Voyager 2 discovered three new rings in addition to the "older" eight rings. | 3 | carried | 'three new rings in addition to the “older” eight rings' in `merged.md` -- Directly stated. |
| 6 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- Directly stated. |
| 7 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h. | 5 | carried | 'wind speeds in Uranus’ atmosphere as high as 450 km/h' in `merged.md` -- Directly stated. |
| 8 | 450 km/h equals 72400 meters per hour. | 5 | carried | '450 km/h (72400 meters per hour)' in `merged.md` -- The text gives this equivalence. |
| 9 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | carried | 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- Directly stated. |
| 10 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- Directly stated. |
| 11 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons. | 7 | carried | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `merged.md` -- Directly stated. |
| 12 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- Directly stated. |
| 13 | Voyager 2 came closest to any object so far in its travels during the Miranda flyby. | 7 | carried | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `merged.md` -- Directly stated. |
| 14 | Voyager 2's travels have lasted nearly a century. | 7 | carried | 'nearly century-long travels' in `merged.md` -- The text states the travels were nearly century-long. |
| 15 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- Directly stated. |
| 16 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- Directly stated. |
| 17 | The Uranus encounter news was interrupted the same day by the Challenger accident. | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `merged.md` -- Directly stated. |
| 18 | The Challenger accident killed six astronauts. | 9 | carried | 'the tragic Challenger accident that killed six astronauts' in `merged.md` -- Directly stated. |

### `merged.md` -- 30 claim(s): 0 invented, 9 contradicted, 0 supported in part, 21 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with the three planetary encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source names Voyager 3, not Voyager 2, as having fulfilled its goals. |
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- Source says Saturn, not Neptune. |
| 6 | Voyager 2 had only 6.4 days of close study during its flyby. | contradicted | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- Source attributes this to Voyager 1, not Voyager 2. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations" in `source_a.md` -- Source names Voyager 1, not Voyager 2. |
| 8 | Voyager 2's short-range observations of Uranus began Jan. 31, 1987. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source attributes the observations to Voyager 1 rather than Voyager 2. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source gives the year 1968, not 1986. |
| 12 | Closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Source gives 50,640 km and 81,500 miles, the reverse of the claim. |
| 15 | The moon names are allusions to Shakespeare, continuing a naming tradition begun in 1787. | contradicted | `source_b.md` | 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' in `source_b.md` -- Source says Goethe and 1687, not Shakespeare and 1787. |
| 30 | The Challenger space shuttle launch was on Jan. 28, 1986. | contradicted | `source_b.md` | 'space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source gives Feb. 28, not Jan. 28. |
| 2 | Mission planners directed Voyager 2 to Uranus. | supported | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- Source states planners directed the spacecraft to Uranus, and the title identifies it as Voyager 2. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Directly stated. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- Directly stated for the spacecraft, which the title identifies as Voyager 2. |
| 9 | When short-range observations began, signals took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'when signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Directly stated. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- Directly stated. |
| 13 | Voyager 2 discovered 11 new moons during its flyby. | supported | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Directly stated. |
| 14 | The new moons discovered included Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | supported | `source_b.md` | 'Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- Names listed identically. |
| 16 | Voyager 2 discovered three new rings in addition to the "older" eight rings. | supported | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Directly stated. |
| 17 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Directly stated. |
| 18 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h. | supported | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h' in `source_b.md` -- Directly stated. |
| 19 | 450 km/h equals 72400 meters per hour. | supported | `source_b.md` | '450 km/h (72400 meters per hour)' in `source_b.md` -- Source equates the two figures, though the conversion is arithmetically wrong. |
| 20 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | supported | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Directly stated. |
| 21 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- Directly stated. |
| 22 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Directly stated. |
| 23 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | supported | `source_b.md` | 'five of Uranus’ smaller moons' in `source_b.md` -- Directly stated. |
| 24 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Directly stated. |
| 25 | The Miranda flyby was the closest the spacecraft came to any object so far in its nearly century-long travels. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Directly stated. |
| 26 | Images of Miranda showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.' in `source_b.md` -- Directly stated. |
| 27 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- Directly stated. |
| 28 | The news of the Uranus encounter was interrupted the same day by the Challenger accident. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- Directly stated. |
| 29 | The Challenger accident killed six astronauts during their space shuttle launch. | supported | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch' in `source_b.md` -- Directly stated. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **30** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **31**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 14 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '1' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1' does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **7** departure(s) from its sources. Checking them confirms 1, rejects 6, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | duplicate | Identical title to the base title. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a2` | reworded | Corrected spacecraft name from Voyager 3. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Fixed typo, planet and spacecraft name. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED (`A-005`, `A-006`) |
| `a5` | reworded | Corrected spacecraft name from Voyager 1. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a7` | reworded | Corrected year and swapped km/miles units. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b2` | reworded | Corrected author and year. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-003 came back CONTRADICTED, B-004 came back CONTRADICTED (`B-003`, `B-004`) |
| `b9` | reworded | Corrected Challenger launch date. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-019 came back CONTRADICTED (`B-019`) |

## Added from outside the documents

The merge declared 6 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. No call the model made took more turns than a call that retrieves nothing can take, so it retrieved nothing and every source here is recalled rather than looked up. **This run was made at fidelity sourced, which asks the model to retrieve rather than recall, and nothing was retrieved.** Every source listed here is therefore a recollection, exactly as it would be at open.

6 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals | Although Voyager 3 had fulfilled | the model's own knowledge | *no source* | Only Voyagers 1 and 2 exist; the title says Voyager 2. | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 6.4 days of close study during its flyby. | The Ur anus encounter’s ... encounter with Saturn: Voyager 1 had only 6.4 days | the model's own knowledge | *no source* | Voyager 2 flew on to Neptune; Voyager 1 never visited Uranus. | *none* |
| The first human-made object to fly past Uranus, Voyager 2's short-range observations | Voyager 1's short-range observations | the model's own knowledge | *no source* | Voyager 2 alone flew past Uranus. | *none* |
| Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | Voyagers launched 1977; a kilometre is shorter than a mile. | *none* |
| obvious allusions to Shakespeare, continuing a naming tradition begun in 1787 | obvious allusions to Goethe, continuing a naming tradition begun in 1687 | the model's own knowledge | *no source* | Uranian moons carry Shakespeare and Pope names; tradition began 1787. | *none* |
| during their space shuttle launch Jan. 28, 1986. | space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger launched and was lost on Jan. 28, 1986. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 7517fd0c82b1 (command) -- Claude Code - Sonnet |
| Fidelity | sourced |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | sonnet -> claude-sonnet-5 |
| Model (decompose) | sonnet -> claude-sonnet-5 |
| Model (verify) | sonnet -> claude-sonnet-5 |
| Structured output | prompt (probed) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=low, merge=medium, verify=low |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 6cc1b1703658 |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Retrieval | WebSearch, WebFetch permitted; no tool use (6 call(s), 6 turn(s) in total) |
| Isolation | decompose, merge, verify: safe mode, tools WebSearch, WebFetch |
| Errors | 0 |
| Duration | 125.9s |
| Generated | 2026-09-26T16:22:22+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `6d8a835cc983` |
| Prompt | `prompts/verify.md` `55a721b20905` |
| Prompt | `prompts/verify_reverse.md` `2a6d7e955709` |

> **Document content was handed to a program on this machine (`Claude Code - Sonnet`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The model was permitted to reach the network** (WebSearch, WebFetch), so a query or a fetch it made may have carried text from these documents to a third party. No tool use (6 call(s), 6 turn(s) in total), counted in turns rather than in fetches. LLossless itself made no network request of any kind and resolved none of the sources the merge names.

> **This run was made at fidelity sourced, which asks the model to retrieve rather than recall, and it retrieved nothing.** Every source the merge names is therefore a recollection, exactly as it would be one level down.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
