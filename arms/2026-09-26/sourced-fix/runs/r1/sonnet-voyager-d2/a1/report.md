## Verdict

**45 finding(s).** In the claims: 30 contradicted, 2 partially invented. In the structure: 13 verbatim violation. **The model retrieved.** This run was made at fidelity sourced, and 2 of the 2 merge call(s) that reported a turn count took the turns a retrieval costs. Which statement a retrieval backs is not recorded, and each is still the model's. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 24 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 15 |
| Forward — source claims accounted for in the merge | **10/27** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **5/12** |
| Forward — `source_b.md` claims accounted for | **5/15** |
| Reverse — merge claims found in a source | **9/24** |
| Reverse — supported only in part | 2 |
| Evidence grounded | **51/51** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says Voyager 2, not Voyager 3.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby.
  - `merged.md` says: 'Voyager 2 had only 6.4 days of close study during its flyby.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text attributes this to Voyager 2, not Voyager 1.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: "The first human-made object to fly past Uranus, Voyager 2's" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: It was Voyager 2.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: "Voyager 2's long-range observations of the planet began Nov. 4, 1985" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Different spacecraft, range and date.
- **A-010** -- the two documents disagree
  - `source_a.md:9` says: Light conditions at Uranus were five-hundred times less than terrestrial conditions.
  - `merged.md` says: 'Light conditions were 400 times less than terrestrial conditions.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: 400 versus 500.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Year is 1986, not 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 50,640 miles (81,500 kilometers)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Units are swapped.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: During its flyby, Voyager 2 discovered 11 new moons.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: 10, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings in addition to the "older" eight rings.
  - `merged.md` says: 'two new rings in addition to the nine known rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Two new and nine known, not three and eight.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center.
  - `merged.md` says: 'a magnetic field tilted at 55 degrees off-axis and off-center' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: 55, not 66.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The moon names given include Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Several names differ.
- **B-006** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'as high as 450 miles per hour (about 724 kilometers per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: 450 mph, not km/h; 724 km/h not 72400 m/h.
- **B-007** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  - `merged.md` says: 'a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Ocean, 497 miles/800 km differ.
- **B-009** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons.
  - `merged.md` says: 'Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Names differ.
- **B-011** -- the two documents disagree
  - `source_b.md:7` says: The Miranda flyby was the closest the spacecraft came to any object so far in its nearly century-long travels.
  - `merged.md` says: 'in its decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Decade-long, not century-long.
- **B-013** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident interrupted the news of the Uranus encounter the same day.
  - `merged.md` says: 'interrupted the same week by the tragic Challenger accident' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Same week, not same day.
- **B-015** -- the two documents disagree
  - `source_b.md:9` says: The Challenger space shuttle launch took place Feb. 28, 1986.
  - `merged.md` says: 'space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: January, not February.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's long-range observations of Uranus began Nov. 4, 1985.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says short-range observations began Jan. 31, 1987, not long-range on Nov. 4, 1985.
- **M-009** -- the two documents disagree
  - `merged.md:5` says: Light conditions at Uranus were 400 times less than terrestrial conditions.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says 500 times, not 400.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives the year 1968, not 1986.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus was at a range of about 50,640 miles (81,500 kilometers).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives 50,640 kilometers and 81,500 miles, so the units are swapped in the claim.
- **M-012** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered 10 new moons at Uranus during its flyby.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says 11, not 10.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered two new rings in addition to the nine known rings.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says three new rings and eight older, not two and nine.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 found a magnetic field tilted at 55 degrees off-axis and off-center.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says 66 degrees, not 55.
- **M-016** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (about 724 kilometers per hour).
  - `source_b.md` says: 'as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says 450 km/h, not miles per hour.
- **M-017** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface.
  - `source_b.md` says: 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives 479 miles and 900 km, a lake not an ocean, differing from 497 and 800.
- **M-019** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons.
  - `source_b.md` says: 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Ariele, Umbrella and Titan, differing from the claim's Ariel, Umbriel and Titania.
- **M-021** -- the two documents disagree
  - `merged.md:11` says: The Miranda flyby was the closest the spacecraft came to any object so far in its decade-long travels.
  - `source_b.md` says: 'in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says nearly century-long, not decade-long.
- **M-023** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident killed six astronauts during their space shuttle launch Jan. 28, 1986.
  - `source_b.md` says: 'during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says Feb. 28, not Jan. 28.
- **M-024** -- the two documents disagree
  - `merged.md:13` says: The Uranus encounter news was interrupted the same week by the Challenger accident.
  - `source_b.md` says: 'was interrupted the same day by the tragic Challenger accident' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says the same day, not the same week.

### Partly invented — the sources carry some of this claim

- **M-001** (`merged.md:3`) — Voyager 2 had fulfilled its primary mission goals with the three planetary encounters before being directed to Uranus.
  - evidence: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source says Voyager 3 (not 2) fulfilled goals; the title says Voyager 2, so the spacecraft is inconsistent in the source.
- **M-013** (`merged.md:7`) — The naming tradition of Shakespearean allusions for Uranus moons began in 1687.
  - evidence: 'continuing a naming tradition begun in 1687' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Tradition began 1687 is stated, but the source says allusions to Goethe, not Shakespeare.

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
- **reading resolved by the merge** `m12` (`source_b.md`) - source_b.md writes '17.560' beside 'miles' (line 7), which reads 17.56 in its decimal point convention; the merge writes '17,560' (line 11), which reads 17560 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its decade-long travels.
  What changed:  In flying by Miranda at a range of only 17[-.-]{+,+}560 miles (28[-.-]{+,+}260 kilometers), the spacecraft came closest to any object so far in its [-nearly century-long-] {+decade-long+} travels.
  ```
- **reading resolved by the merge** `m12` (`source_b.md`) - source_b.md writes '28.260' beside 'kilometers' (line 7), which reads 28.26 in its decimal point convention; the merge writes '28,260' (line 11), which reads 28260 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its decade-long travels.
  What changed:  In flying by Miranda at a range of only 17[-.-]{+,+}560 miles (28[-.-]{+,+}260 kilometers), the spacecraft came closest to any object so far in its [-nearly century-long-] {+decade-long+} travels.
  ```

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
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' in `merged.md` -- Text says Voyager 2, not Voyager 3. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | contradicted | 'Voyager 2 had only 6.4 days of close study during its flyby.' in `merged.md` -- Text attributes this to Voyager 2, not Voyager 1. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | "The first human-made object to fly past Uranus, Voyager 2's" in `merged.md` -- It was Voyager 2. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | "Voyager 2's long-range observations of the planet began Nov. 4, 1985" in `merged.md` -- Different spacecraft, range and date. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | contradicted | 'Light conditions were 400 times less than terrestrial conditions.' in `merged.md` -- 400 versus 500. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' in `merged.md` -- Year is 1986, not 1968. |
| 12 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 50,640 miles (81,500 kilometers)' in `merged.md` -- Units are swapped. |
| 2 | Mission planners directed the spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly stated. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Directly stated. |
| 4 | Voyager's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Directly stated. |
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | 7 | carried | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `merged.md` -- Directly stated. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Directly stated. |

### `source_b.md` -- 15 claim(s): 0 dropped, 10 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | During its flyby, Voyager 2 discovered 11 new moons. | 3 | contradicted | 'Voyager 2 discovered 10 new moons' in `merged.md` -- 10, not 11. |
| 2 | Voyager 2 discovered three new rings in addition to the "older" eight rings. | 3 | contradicted | 'two new rings in addition to the nine known rings' in `merged.md` -- Two new and nine known, not three and eight. |
| 3 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | contradicted | 'a magnetic field tilted at 55 degrees off-axis and off-center' in `merged.md` -- 55, not 66. |
| 4 | The moon names given include Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Several names differ. |
| 6 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'as high as 450 miles per hour (about 724 kilometers per hour)' in `merged.md` -- 450 mph, not km/h; 724 km/h not 72400 m/h. |
| 7 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | contradicted | 'a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface' in `merged.md` -- Ocean, 497 miles/800 km differ. |
| 9 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons. | 7 | contradicted | 'Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- Names differ. |
| 11 | The Miranda flyby was the closest the spacecraft came to any object so far in its nearly century-long travels. | 7 | contradicted | 'in its decade-long travels' in `merged.md` -- Decade-long, not century-long. |
| 13 | The Challenger accident interrupted the news of the Uranus encounter the same day. | 9 | contradicted | 'interrupted the same week by the tragic Challenger accident' in `merged.md` -- Same week, not same day. |
| 15 | The Challenger space shuttle launch took place Feb. 28, 1986. | 9 | contradicted | 'space shuttle launch Jan. 28, 1986' in `merged.md` -- January, not February. |
| 5 | The naming tradition for Uranus' moons was begun in 1687. | 3 | carried | 'continuing a naming tradition begun in 1687' in `merged.md` -- Directly stated. |
| 8 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- Directly stated. |
| 10 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'at a range of only 17,560 miles (28,260 kilometers)' in `merged.md` -- Same values; separator formatting differs. |
| 12 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- Directly stated. |
| 14 | The Challenger accident killed six astronauts. | 9 | carried | 'the tragic Challenger accident that killed six astronauts' in `merged.md` -- Directly stated. |

### `merged.md` -- 24 claim(s): 0 invented, 13 contradicted, 2 supported in part, 9 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 7 | Voyager 2's long-range observations of Uranus began Nov. 4, 1985. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source says short-range observations began Jan. 31, 1987, not long-range on Nov. 4, 1985. |
| 9 | Light conditions at Uranus were 400 times less than terrestrial conditions. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- Source says 500 times, not 400. |
| 10 | Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source gives the year 1968, not 1986. |
| 11 | Closest approach to Uranus was at a range of about 50,640 miles (81,500 kilometers). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Source gives 50,640 kilometers and 81,500 miles, so the units are swapped in the claim. |
| 12 | Voyager 2 discovered 10 new moons at Uranus during its flyby. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Source says 11, not 10. |
| 14 | Voyager 2 discovered two new rings in addition to the nine known rings. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Source says three new rings and eight older, not two and nine. |
| 15 | Voyager 2 found a magnetic field tilted at 55 degrees off-axis and off-center. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Source says 66 degrees, not 55. |
| 16 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (about 724 kilometers per hour). | contradicted | `source_b.md` | 'as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- Source says 450 km/h, not miles per hour. |
| 17 | Voyager 2 found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface. | contradicted | `source_b.md` | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Source gives 479 miles and 900 km, a lake not an ocean, differing from 497 and 800. |
| 19 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons. | contradicted | `source_b.md` | 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' in `source_b.md` -- Source names Ariele, Umbrella and Titan, differing from the claim's Ariel, Umbriel and Titania. |
| 21 | The Miranda flyby was the closest the spacecraft came to any object so far in its decade-long travels. | contradicted | `source_b.md` | 'in its nearly century-long travels' in `source_b.md` -- Source says nearly century-long, not decade-long. |
| 23 | The Challenger accident killed six astronauts during their space shuttle launch Jan. 28, 1986. | contradicted | `source_b.md` | 'during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source says Feb. 28, not Jan. 28. |
| 24 | The Uranus encounter news was interrupted the same week by the Challenger accident. | contradicted | `source_b.md` | 'was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- Source says the same day, not the same week. |
| 1 | Voyager 2 had fulfilled its primary mission goals with the three planetary encounters before being directed to Uranus. | supported in part | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source says Voyager 3 (not 2) fulfilled goals; the title says Voyager 2, so the spacecraft is inconsistent in the source. |
| 13 | The naming tradition of Shakespearean allusions for Uranus moons began in 1687. | supported in part | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- Tradition began 1687 is stated, but the source says allusions to Goethe, not Shakespeare. |
| 2 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Stated directly. |
| 3 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- Stated directly. |
| 4 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | supported | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- Stated directly. |
| 5 | Voyager 2 had only 6.4 days of close study during its flyby of Uranus. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- Source names Voyager 1 but context is the Voyager 2 Uranus flyby; same fact. |
| 6 | Voyager 2 was the first human-made object to fly past Uranus. | supported | `source_a.md` | 'The first human-made object to fly past Uranus' in `source_a.md` -- Stated, with the spacecraft name garbled in the source. |
| 8 | When observations began, signals took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'when signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Stated directly. |
| 18 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- Stated directly. |
| 20 | Voyager 2 flew by Miranda at a range of only 17,560 miles (28,260 kilometers). | supported | `source_b.md` | 'at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Same figures, differing only in the separator. |
| 22 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- Stated directly. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **24** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **27**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 12 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '1' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '66' (degrees) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '479' (miles) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '900' (kilometers) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '17.560' (miles) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '28.260' (kilometers) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **11** departure(s) from its sources. Checking them confirms 1, rejects 10, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | duplicate | Same title as the base. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a2` | reworded | Spacecraft name corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Typo and spacecraft name corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-006 came back CONTRADICTED (`A-006`) |
| `a5` | reworded | Observation type, date and name corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a6` | reworded | Figure corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-010 came back CONTRADICTED (`A-010`) |
| `a7` | reworded | Time zone, year and units corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b2` | reworded | Moon, ring, tilt and name facts corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`) |
| `b3` | reworded | Wind and ocean figures corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-006 came back CONTRADICTED, B-007 came back CONTRADICTED (`B-006`, `B-007`) |
| `b5` | reworded | Moon names corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-009 came back CONTRADICTED (`B-009`) |
| `b6` | reworded | Number format and duration corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-011 came back CONTRADICTED (`B-011`) |
| `b9` | reworded | Timing and date corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-013 came back CONTRADICTED, B-015 came back CONTRADICTED (`B-013`, `B-015`) |

## Added from outside the documents

The merge declared 8 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. The model took more turns on 2 call(s) than a call that retrieves nothing can take, so it used a tool it was granted at least that often. It is a count of turns rather than of fetches, and which statement a retrieval belongs to is not recorded. The endpoint's own web-request counter reported none, which on this backend means it could not see one rather than that none was made: it counts a vendor's server-side tools and a command-line tool runs in the model's own process.

8 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers). | 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | cited | NASA Voyager 2 page, science.nasa.gov/mission/voyager/voyager-2/, read | NASA page gives 1986, UT and 50,640 miles. | *none* |
| Voyager 2's long-range observations of the planet began Nov. 4, 1985, when signals took approximately 2,5 hours to reach Earth. Light conditions were 400 times less than terrestrial conditions. | short-range observations of the planet began Jan. 31, 1987; five-hundred times less | cited | NASA Voyager 2 page, science.nasa.gov/mission/voyager/voyager-2/, read | NASA page gives long-range, Nov. 4 1985, 400 times. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1687), two new rings in addition to the nine known rings, and a magnetic field tilted at 55 degrees off-axis and off-center. | 11 new moons ... Goethe ... three new rings in addition to the “older” eight rings ... 66 degrees | cited | NASA Voyager 2 page, science.nasa.gov/mission/voyager/voyager-2/, read | NASA page lists 10 Shakespearean moons, 2+9 rings, 55 degrees. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 miles per hour (about 724 kilometers per hour) and found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface. | 450 km/h (72400 meters per hour) ... boiling lake ... 479 miles (900 kilometers) | cited | NASA Voyager 2 page, science.nasa.gov/mission/voyager/voyager-2/, read | NASA page gives 450 mph, ocean, 497 miles (800 km). | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons. | Miranda, Oberon, Ariele, Umbrella, and Titan | the model's own knowledge | *no source* | Uranian moons are Ariel, Umbriel, Titania. | *none* |
| In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its decade-long travels. | 17.560 miles (28.260 kilometers) ... nearly century-long travels | cited | NASA Voyager 2 page, science.nasa.gov/mission/voyager/voyager-2/, read | NASA page says 17,560 miles and decade-long. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident that killed six astronauts during their space shuttle launch Jan. 28, 1986. | the same day ... Feb. 28, 1986 | cited | NASA Voyager 2 page, science.nasa.gov/mission/voyager/voyager-2/, read | NASA page gives Jan. 28, 1986, same week. | *none* |
| Although Voyager 2 had fulfilled its primary mission goals ... Voyager 2 had only 6.4 days of close study during its flyby. | Voyager 3 ... Voyager 1 | the model's own knowledge | *no source* | Uranus was visited only by Voyager 2; title says so. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | e609144cb465 (command) -- Claude Code - Sonnet |
| Fidelity | sourced |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | sonnet -> claude-sonnet-5 (the answer's output tokens; also named claude-haiku-4-5-20251001) |
| Model (decompose) | sonnet -> claude-sonnet-5 |
| Model (verify) | sonnet -> claude-sonnet-5 |
| Structured output | prompt (probed) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=low, merge=medium, verify=low |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | b86a50510992 |
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | unknown (8 call(s) reported no usage) |
| Cost | unmeasured (8 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 2 |
| Retrieval | WebSearch, WebFetch permitted; 2 of 8 call(s) used a tool (10 turn(s) in total) |
| Isolation | decompose, merge, verify: safe mode, tools WebSearch, WebFetch |
| Errors | 0 |
| Duration | 157.4s |
| Generated | 2026-09-26T17:57:58+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `831fa897e6f5` |
| Prompt | `prompts/verify.md` `55a721b20905` |
| Prompt | `prompts/verify_reverse.md` `2a6d7e955709` |

> **Document content was handed to a program on this machine (`Claude Code - Sonnet`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The model was permitted to reach the network** (WebSearch, WebFetch), so a query or a fetch it made may have carried text from these documents to a third party. 2 of 8 call(s) used a tool (10 turn(s) in total), counted in turns rather than in fetches. LLossless itself made no network request of any kind and resolved none of the sources the merge names.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
