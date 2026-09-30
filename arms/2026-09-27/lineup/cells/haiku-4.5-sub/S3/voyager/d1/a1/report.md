## Verdict

**35 finding(s).** In the claims: 1 partially dropped, 21 contradicted, 1 partially invented. In the structure: 1 undeclared rewording, 3 false departure, 8 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 23 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 16 |
| Forward — source claims accounted for in the merge | **14/28** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **5/12** (1 in part) |
| Forward — `source_b.md` claims accounted for | **9/16** |
| Reverse — merge claims found in a source | **14/23** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **48/51** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **A-006** (`source_a.md:7`) — Voyager 1 had 6.4 days of close study during its Saturn flyby.
  - evidence: 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference states the 6.4 days observation period but does not explicitly name Saturn in the same clause; Saturn appears in the preceding clause connected by a colon.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Voyager 2 fulfilled its primary mission goals with three planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states Voyager 2, not Voyager 3, fulfilled its primary mission goals with three planetary encounters.
- **A-002** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies the spacecraft as Voyager 2, not Voyager 3.
- **A-004** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies the spacecraft as Voyager 2, not Voyager 3.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2 became the first human-made object to fly past Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states Voyager 2, not Voyager 1, was the first human-made object to fly past Uranus.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of the planet began Jan. 31, 1987.
  - `merged.md` says: 'Its short-range observations of the planet began on January 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies the spacecraft as Voyager 2 and the date as January 24, 1986, contradicting Voyager 1 and Jan. 31, 1987.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 UT on January 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states 17:59 UT on January 24, 1986, contradicting the claim's 17:59 ED in 1968.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The moons were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II
  - `merged.md` says: 'Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference lists different moon names; the claim uses incorrect variants like Pucka, Portila, Juliette, Kressida, Rosalinde, Cordelina, and Bianca II.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: A naming tradition was begun in 1687
  - `merged.md` says: 'continuing a naming tradition begun in 1787' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states 1787, not 1687.
- **B-009** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan
  - `merged.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, and Umbriel' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference lists Ariel and Umbriel, not Ariele and Umbrella; Titan is not mentioned.
- **B-010** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons
  - `merged.md` says: 'Miranda, Oberon, Ariel, and Umbriel, among other smaller moons of Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference lists Ariel and Umbriel with different spellings than claimed; Titan is not mentioned as a moon of Uranus.
- **B-011** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers)
  - `merged.md` says: 'at a range of only 17,560 miles (28,260 kilometers)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference uses comma notation (17,560) for thousands separator; the claim uses period notation (17.560), representing different numerical values.
- **B-014** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts
  - `merged.md` says: 'the tragic Challenger accident that killed seven crew members' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states seven crew members, not six astronauts.
- **B-015** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986
  - `merged.md` says: 'during their space shuttle launch on January 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states January 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 fulfilled its primary mission goals with three planetary encounters.
  - `source_a.md` says: 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source explicitly states Voyager 3, not Voyager 2, fulfilled these mission goals.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 became the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source explicitly identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's short-range observations of Uranus began on January 24, 1986.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes observations to Voyager 1 on Jan. 31, 1987, not Voyager 2 on January 24, 1986.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach to Uranus took place at 17:59 UT on January 24, 1986, at a range of about 50,640 kilometers (81,500 miles).
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source specifies the date as Jan. 24, 1968, not 1986 as claimed.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: The new moons discovered by Voyager 2 were given names such as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source lists different moon name spellings: Pucka, Portila, Juliette, Kressida, Rosalinde, Cordelina, Bianca II.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: A naming tradition for the moons was begun in 1787.
  - `source_b.md` says: 'a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states naming tradition was begun in 1687, not 1787 as claimed.
- **M-020** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, and Umbriel, among other smaller moons of Uranus.
  - `source_b.md` says: 'returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source lists moons as Ariele and Umbrella, contradicting claim's spellings of Ariel and Umbriel.
- **M-023** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident killed seven crew members during their space shuttle launch on January 28, 1986.
  - `source_b.md` says: 'killed six astronauts during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states Challenger killed six astronauts on Feb. 28, 1986, not seven on January 28, 1986.

### Partly invented — the sources carry some of this claim

- **M-006** (`merged.md:3`) — Voyager 1 had only 6.4 days of close study during its Saturn flyby.
  - evidence: 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source confirms Voyager 1 had 6.4 days of close study, but does not explicitly state this refers to Saturn.

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
- **other convention** `m6` (`merged.md`) - '2,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **reading resolved by the merge** `m13` (`source_b.md`) - source_b.md writes '17.560' beside 'miles' (line 7), which reads 17.56 in its decimal point convention; the merge writes '17,560' (line 9), which reads 17560 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  What changed:  In flying by Miranda at a range of only 17[-.-]{+,+}560 miles (28[-.-]{+,+}260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  ```
- **reading resolved by the merge** `m13` (`source_b.md`) - source_b.md writes '28.260' beside 'kilometers' (line 7), which reads 28.26 in its decimal point convention; the merge writes '28,260' (line 9), which reads 28260 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  What changed:  In flying by Miranda at a range of only 17[-.-]{+,+}560 miles (28[-.-]{+,+}260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  ```

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 6 contradicted, 1 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Voyager 2 fulfilled its primary mission goals with three planetary encounters' in `merged.md` -- The reference text states Voyager 2, not Voyager 3, fulfilled its primary mission goals with three planetary encounters. |
| 2 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- The reference identifies the spacecraft as Voyager 2, not Voyager 3. |
| 4 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- The reference identifies the spacecraft as Voyager 2, not Voyager 3. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2 became the first human-made object to fly past Uranus' in `merged.md` -- The reference states Voyager 2, not Voyager 1, was the first human-made object to fly past Uranus. |
| 8 | Voyager 1's short-range observations of the planet began Jan. 31, 1987. | 9 | contradicted | 'Its short-range observations of the planet began on January 24, 1986' in `merged.md` -- The reference identifies the spacecraft as Voyager 2 and the date as January 24, 1986, contradicting Voyager 1 and Jan. 31, 1987. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 UT on January 24, 1986' in `merged.md` -- The reference states 17:59 UT on January 24, 1986, contradicting the claim's 17:59 ED in 1968. |
| 6 | Voyager 1 had 6.4 days of close study during its Saturn flyby. | 7 | carried in part | 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` -- The reference states the 6.4 days observation period but does not explicitly name Saturn in the same clause; Saturn appears in the preceding clause connected by a colon. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- The reference directly states the journey to Uranus would take about 4,5 years. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | 7 (unverified) | carried | "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn" in `merged.md` -- The reference directly states this claim. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals took approximately 2,5 hours to reach Earth' in `merged.md` -- The reference directly states this claim. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five hundred times less than terrestrial conditions' in `merged.md` -- The reference states the same fact with identical meaning despite different hyphenation. |
| 12 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | carried | 'at a range of about 50,640 kilometers (81,500 miles)' in `merged.md` -- The reference directly states this claim. |

### `source_b.md` -- 16 claim(s): 0 dropped, 7 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | The moons were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II | 3 | contradicted | 'Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The reference lists different moon names; the claim uses incorrect variants like Pucka, Portila, Juliette, Kressida, Rosalinde, Cordelina, and Bianca II. |
| 3 | A naming tradition was begun in 1687 | 3 | contradicted | 'continuing a naming tradition begun in 1787' in `merged.md` -- The reference states 1787, not 1687. |
| 9 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan | 7 | contradicted | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, and Umbriel' in `merged.md` -- The reference lists Ariel and Umbriel, not Ariele and Umbrella; Titan is not mentioned. |
| 10 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons | 7 (unverified) | contradicted | 'Miranda, Oberon, Ariel, and Umbriel, among other smaller moons of Uranus' in `merged.md` -- The reference lists Ariel and Umbriel with different spellings than claimed; Titan is not mentioned as a moon of Uranus. |
| 11 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers) | 7 | contradicted | 'at a range of only 17,560 miles (28,260 kilometers)' in `merged.md` -- The reference uses comma notation (17,560) for thousands separator; the claim uses period notation (17.560), representing different numerical values. |
| 14 | The Challenger accident killed six astronauts | 9 | contradicted | 'the tragic Challenger accident that killed seven crew members' in `merged.md` -- The reference states seven crew members, not six astronauts. |
| 15 | The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986 | 9 | contradicted | 'during their space shuttle launch on January 28, 1986' in `merged.md` -- The reference states January 28, 1986, not Feb. 28, 1986. |
| 1 | Voyager 2 discovered 11 new moons | 3 | carried | 'Voyager 2 discovered 11 new moons' in `merged.md` -- The reference directly states this claim. |
| 4 | Voyager 2 discovered three new rings in addition to eight older rings | 3 (unverified) | carried | 'three new rings in addition to the eight older rings' in `merged.md` -- The reference directly states this claim. |
| 5 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- The reference directly states this claim. |
| 6 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour) | 5 (unverified) | carried | "wind speeds in Uranus' atmosphere as high as 450 km/h (72,400 meters per hour)" in `merged.md` -- The reference states the same values with identical meaning despite comma formatting differences. |
| 7 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface | 5 | carried | 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- The reference directly states this claim. |
| 8 | Uranus' rings were found to be extremely variable in thickness and transparency | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference directly states this claim with identical meaning. |
| 12 | The spacecraft came closest to any object so far in its nearly century-long travels | 7 | carried | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `merged.md` -- The reference directly states this claim. |
| 13 | Uranus appeared generally featureless | 7 | carried | 'Uranus itself appeared generally featureless' in `merged.md` -- The reference directly states this claim. |
| 16 | The news of the Uranus encounter was interrupted the same day by the Challenger accident | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `merged.md` -- The reference directly states this claim. |

### `merged.md` -- 23 claim(s): 0 invented, 8 contradicted, 1 supported in part, 14 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 fulfilled its primary mission goals with three planetary encounters. | contradicted | `source_a.md` | 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source explicitly states Voyager 3, not Voyager 2, fulfilled these mission goals. |
| 7 | Voyager 2 became the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations" in `source_a.md` -- Source explicitly identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus. |
| 8 | Voyager 2's short-range observations of Uranus began on January 24, 1986. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source attributes observations to Voyager 1 on Jan. 31, 1987, not Voyager 2 on January 24, 1986. |
| 11 | Voyager 2's closest approach to Uranus took place at 17:59 UT on January 24, 1986, at a range of about 50,640 kilometers (81,500 miles). | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Source specifies the date as Jan. 24, 1968, not 1986 as claimed. |
| 13 | The new moons discovered by Voyager 2 were given names such as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- Source lists different moon name spellings: Pucka, Portila, Juliette, Kressida, Rosalinde, Cordelina, Bianca II. |
| 14 | A naming tradition for the moons was begun in 1787. | contradicted | `source_b.md` | 'a naming tradition begun in 1687' in `source_b.md` -- Source states naming tradition was begun in 1687, not 1787 as claimed. |
| 20 | Voyager 2 returned photos of Miranda, Oberon, Ariel, and Umbriel, among other smaller moons of Uranus. | contradicted | `source_b.md` | 'returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Source lists moons as Ariele and Umbrella, contradicting claim's spellings of Ariel and Umbriel. |
| 23 | The Challenger accident killed seven crew members during their space shuttle launch on January 28, 1986. | contradicted | `source_b.md` | 'killed six astronauts during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source states Challenger killed six astronauts on Feb. 28, 1986, not seven on January 28, 1986. |
| 6 | Voyager 1 had only 6.4 days of close study during its Saturn flyby. | supported in part | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- Source confirms Voyager 1 had 6.4 days of close study, but does not explicitly state this refers to Saturn. |
| 2 | Mission planners directed Voyager 2 to Uranus. | supported | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The document is titled 'Voyager 2 at Uranus' and the text states mission planners directed the spacecraft to Uranus. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Source directly states the journey to Uranus would take about 4,5 years. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- Source states that the Jupiter encounter was optimized to ensure future planetary flybys would be possible. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | supported | `source_a.md` | "The Ur anus encounter's geometry was also defined by the possibility of a future encounter with Saturn" in `source_a.md`, **transcription_error** -- Source states the Uranus encounter's geometry was defined by possibility of future Saturn encounter. |
| 9 | Signals from Voyager 2 took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Source directly states signals took approximately 2,5 hours to reach Earth. |
| 10 | Light conditions on Uranus were five hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- Source directly states light conditions were five-hundred times less than terrestrial conditions. |
| 12 | Voyager 2 discovered 11 new moons. | supported | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Source directly states that Voyager 2 discovered 11 new moons. |
| 15 | Voyager 2 discovered three new rings in addition to the eight older rings of Uranus. | supported | `source_b.md` | 'three new rings in addition to the "older" eight rings' in `source_b.md`, **transcription_error** -- Source directly states Voyager 2 discovered three new rings in addition to eight older rings. |
| 16 | Uranus has a magnetic field tilted at 66 degrees off-axis and off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Source directly states Uranus has a magnetic field tilted at 66 degrees off-axis and off-center. |
| 17 | Wind speeds in Uranus' atmosphere are as high as 450 km/h (72,400 meters per hour). | supported | `source_b.md` | "wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour)" in `source_b.md`, **transcription_error** -- Source directly states wind speeds in Uranus' atmosphere are as high as 450 km/h (72400 meters per hour). |
| 18 | There is evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus. | supported | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Source directly states evidence of boiling lake 479 miles (900 kilometers) below top cloud surface. |
| 19 | Uranus' rings are extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- Source states rings were found to be extremely variable in thickness and transparency. |
| 21 | Voyager 2 flew by Miranda at a range of 17,560 miles (28,260 kilometers) and this was its closest approach to any object in its travels so far. | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Source confirms Voyager 2 flew by Miranda at that range as its closest approach to any object. |
| 22 | Uranus appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless' in `source_b.md` -- Source directly states Uranus itself appeared generally featureless. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **23** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **28**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a4` (`source_a.md`) — 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.' is reworded in the merge and no disposition record explains it (nearest merge segment m4 at 0.99)

  ```text
  In the source: The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.
  In the merge:  The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.
  What changed:  The Ur[- -]anus encounter[-’-]{+'+}s geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.
  ```

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `b4` (`source_b.md`) — 'Its rings were found to be extremely variable in thickness and transparency.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Its rings were found to be extremely variable in thickness and transparency.
  In the merge:  Its rings were found to be extremely variable in thickness and transparency.
  ```
- `b7` (`source_b.md`) — 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.
  In the merge:  Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.
  ```
- `b8` (`source_b.md`) — 'Uranus itself appeared generally featureless.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Uranus itself appeared generally featureless.
  In the merge:  Uranus itself appeared generally featureless.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '17.560' (miles) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '28.260' (kilometers) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **13** departure(s) from its sources. Checking them confirms 4, rejects 7, and leaves 2 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Corrected Voyager 3 to Voyager 2 | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back CONTRADICTED (`A-001`, `A-002`) |
| `a5` | reworded | Corrected spacecraft to Voyager 2 and date to January 24, 1986 | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a6` | reworded | Converted five-hundred to prose format | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`) |
| `a7` | reworded | Corrected year from 1968 to 1986 and standardized time notation | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED (`A-011`) |
| `b1` | superseded | Base document title is identical | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Corrected moon name spellings and naming tradition date | **rejected** | declared 'reworded', which predicts SUPPORTED; B-002 came back CONTRADICTED, B-003 came back CONTRADICTED (`B-002`, `B-003`) |
| `b3` | subsumed | Scientific findings incorporated into narrative structure | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-007`) |
| `b4` | subsumed | Ring observations merged into findings section | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-008`) |
| `b5` | reworded | Corrected moon names and removed non-Uranian moon Titan | **rejected** | declared 'reworded', which predicts SUPPORTED; B-009 came back CONTRADICTED (`B-009`) |
| `b6` | subsumed | Flyby details incorporated into main narrative | **rejected** | declared 'subsumed', which predicts SUPPORTED; B-011 came back CONTRADICTED (`B-011`) |
| `b7` | subsumed | Miranda description integrated into observations | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b8` | subsumed | Planet appearance integrated into findings | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`) |
| `b9` | reworded | Corrected casualty count and accident date | **rejected** | declared 'reworded', which predicts SUPPORTED; B-014 came back CONTRADICTED, B-015 came back CONTRADICTED (`B-014`, `B-015`) |

## Added from outside the documents

The merge declared 7 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. No call the model made took more turns than a call that retrieves nothing can take, so it retrieved nothing and every source here is recalled rather than looked up.

7 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Voyager 2 became the first human-made object to fly past Uranus. | The first human-made object to fly past Uranus, Voyager 1's short-range observations | the model's own knowledge | *no source* | Voyager 2, not Voyager 1, conducted the Uranus flyby | *none* |
| Its short-range observations of the planet began on January 24, 1986, when signals took approximately 2,5 hours to reach Earth. | began Jan. 31, 1987 | the model's own knowledge | *no source* | Voyager 2 Uranus encounter occurred January 24, 1986 | *none* |
| Closest approach to Uranus took place at 17:59 UT on January 24, 1986, at a range of about 50,640 kilometers (81,500 miles). | Jan. 24, 1968 | the model's own knowledge | *no source* | Encounter occurred in 1986, not 1968 | *none* |
| given names such as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca | Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II | the model's own knowledge | *no source* | Standard astronomical names for Uranus's moons | *none* |
| continuing a naming tradition begun in 1787 | begun in 1687 | the model's own knowledge | *no source* | Uranus discovered 1781; moon discoveries began 1787 | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, and Umbriel, among other smaller moons of Uranus. | Miranda, Oberon, Ariele, Umbrella, and Titan | the model's own knowledge | *no source* | Ariel and Umbriel are Uranus moons; Titan is Saturn's moon | *none* |
| killed seven crew members during their space shuttle launch on January 28, 1986 | killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger disaster occurred January 28, 1986 with 7 fatalities | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 45fff742d0ed (command) -- lineup haiku-4.5-sub |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 -> claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 666.2s |
| Generated | 2026-09-27T21:54:58+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
