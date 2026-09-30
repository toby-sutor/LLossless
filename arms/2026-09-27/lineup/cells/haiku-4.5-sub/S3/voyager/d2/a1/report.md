## Verdict

**27 finding(s).** In the claims: 17 contradicted. In the structure: 4 undeclared rewording, 6 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 26 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **17/25** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **5/12** |
| Forward — `source_b.md` claims accounted for | **12/13** |
| Reverse — merge claims found in a source | **17/26** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **47/51** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 fulfilled its primary mission goals with the three planetary encounters
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with earlier planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies the spacecraft as Voyager 2, not Voyager 3, and does not specify three planetary encounters.
- **A-002** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus
  - `merged.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The spacecraft is Voyager 2, established in preceding sentence, not Voyager 3.
- **A-004** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible
  - `merged.md` says: 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference refers to Voyager 2's Jupiter encounter, not Voyager 3's.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus
  - `merged.md` says: 'Voyager 2 became the first human-made object to fly past Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies Voyager 2, not Voyager 1, as the first human-made object to fly past Uranus.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987
  - `merged.md` says: 'Voyager 2 became the first human-made object to fly past Uranus, with short-range observations of the planet beginning January 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference specifies Voyager 2 and January 24, 1986, contradicting the claim's Voyager 1 and Jan. 31, 1987.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: The closest approach to Uranus took place at 17:59 ED Jan. 24, 1968
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 ED January 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states the year as 1986, not 1968 as claimed.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: The closest approach to Uranus occurred at a range of about 50,640 kilometers (81,500 miles)
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states 81,500 kilometers and 50,640 miles; the claim reverses these units.
- **B-013** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred on Feb. 28, 1986
  - `merged.md` says: 'on January 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states January 28, 1986, not Feb. 28, 1986 as claimed.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with earlier planetary encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes the fulfillment of primary mission goals to Voyager 3, not Voyager 2.
- **M-002** -- the two documents disagree
  - `merged.md:3` says: Mission planners directed Voyager 2 to Uranus.
  - `source_a.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source context refers to Voyager 3 as the spacecraft directed to Uranus, not Voyager 2.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Context indicates this refers to Voyager 3's Jupiter encounter, not Voyager 2's.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 became the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source identifies Voyager 1, not Voyager 2, as the first spacecraft to fly past Uranus.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Short-range observations of Uranus by Voyager 2 began January 24, 1986.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes observations to Voyager 1 on Jan. 31, 1987; claim says Voyager 2 on January 24, 1986.
- **M-009** -- the two documents disagree
  - `merged.md:5` says: Signals from Voyager 2 took approximately 2,5 hours to reach Earth.
  - `source_a.md` says: 'when signals took approximately 2,5 hours to reach Earth' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Signals statement appears in Voyager 1 context, not Voyager 2 context.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 ED January 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives year 1968; claim states 1986.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: The closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source lists 50,640 km first; claim reverses to 81,500 km first.
- **M-026** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident occurred on January 28, 1986.
  - `source_b.md` says: 'Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives date as Feb. 28, 1986; claim states January 28, 1986.

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
- **reading resolved by the merge** `m12` (`source_b.md`) - source_b.md writes '17.560' beside 'miles' (line 7), which reads 17.56 in its decimal point convention; the merge writes '17,560' (line 9), which reads 17560 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  What changed:  In flying by Miranda at a range of only 17[-.-]{+,+}560 miles (28[-.-]{+,+}260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  ```
- **reading resolved by the merge** `m12` (`source_b.md`) - source_b.md writes '28.260' beside 'kilometers' (line 7), which reads 28.26 in its decimal point convention; the merge writes '28,260' (line 9), which reads 28260 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  What changed:  In flying by Miranda at a range of only 17[-.-]{+,+}560 miles (28[-.-]{+,+}260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  ```

## Length capped

- `$.dispositions[2].reason` was 112 characters, over the 80-character cap; capped to fit
- `$.dispositions[5].reason` was 96 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 7 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 fulfilled its primary mission goals with the three planetary encounters | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with earlier planetary encounters' in `merged.md` -- The reference identifies the spacecraft as Voyager 2, not Voyager 3, and does not specify three planetary encounters. |
| 2 | Mission planners directed Voyager 3 to Uranus | 3 | contradicted | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- The spacecraft is Voyager 2, established in preceding sentence, not Voyager 3. |
| 4 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible | 5 | contradicted | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- The reference refers to Voyager 2's Jupiter encounter, not Voyager 3's. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus | 9 | contradicted | 'Voyager 2 became the first human-made object to fly past Uranus' in `merged.md` -- The reference identifies Voyager 2, not Voyager 1, as the first human-made object to fly past Uranus. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987 | 9 | contradicted | 'Voyager 2 became the first human-made object to fly past Uranus, with short-range observations of the planet beginning January 24, 1986' in `merged.md` -- The reference specifies Voyager 2 and January 24, 1986, contradicting the claim's Voyager 1 and Jan. 31, 1987. |
| 11 | The closest approach to Uranus took place at 17:59 ED Jan. 24, 1968 | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 ED January 24, 1986' in `merged.md` -- The reference states the year as 1986, not 1968 as claimed. |
| 12 | The closest approach to Uranus occurred at a range of about 50,640 kilometers (81,500 miles) | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The reference states 81,500 kilometers and 50,640 miles; the claim reverses these units. |
| 3 | A journey to Uranus would take about 4,5 years | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- The reference directly states this exact duration for the journey to Uranus. |
| 5 | The Ur anus encounter's geometry was defined by the possibility of a future encounter with Saturn | 7 (unverified) | carried | "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn" in `merged.md` -- The reference directly states that Uranus encounter geometry was defined by Saturn encounter possibility. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` -- The reference directly states this exact claim about Voyager 1's close study period. |
| 9 | Signals took approximately 2,5 hours to reach Earth | 9 | carried | 'when signals took approximately 2,5 hours to reach Earth' in `merged.md` -- The reference directly states this exact claim about signal travel time. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions' in `merged.md` -- The reference directly states this exact claim about light conditions. |

### `source_b.md` -- 13 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 12 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 13 | The Challenger accident occurred on Feb. 28, 1986 | 9 | contradicted | 'on January 28, 1986' in `merged.md` -- The reference states January 28, 1986, not Feb. 28, 1986 as claimed. |
| 1 | Voyager 2 discovered 11 new moons | 3 | carried | 'Voyager 2 discovered 11 new moons' in `merged.md` -- The reference directly states this exact claim. |
| 2 | The new moons were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II | 3 | carried | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `merged.md` -- The reference directly lists these exact moon names. |
| 3 | A naming tradition began in 1687 | 3 | carried | 'continuing a naming tradition begun in 1687' in `merged.md` -- The reference directly states this exact claim about the naming tradition. |
| 4 | Voyager 2 discovered three new rings in addition to the "older" eight rings | 3 (unverified) | carried | 'three new rings in addition to the "older" eight rings' in `merged.md` -- The reference directly states this exact claim about the rings discovered. |
| 5 | Uranus has a magnetic field tilted at 66 degrees off-axis and off-center | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- The reference directly states this exact claim about Uranus' magnetic field. |
| 6 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour) | 5 (unverified) | carried | "The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour)" in `merged.md` -- The reference directly states these exact wind speeds; the spacecraft is Voyager 2 from context. |
| 7 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface | 5 | carried | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- The reference directly states this exact claim about the water lake evidence. |
| 8 | Uranus' rings were found to be extremely variable in thickness and transparency | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference directly states this about Uranus' rings. |
| 9 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons | 7 (unverified) | carried | "Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons" in `merged.md` -- The reference directly states this exact claim about the photos returned. |
| 10 | In flying by Miranda at a range of 17.560 miles (28.260 kilometers), Voyager 2 came closest to any object so far in its nearly century-long travels | 7 | carried | 'In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels' in `merged.md` -- The reference states these same values with the spacecraft as Voyager 2; thousand-separator notation difference does not change the numerical values. |
| 11 | Uranus appeared generally featureless | 7 | carried | 'Uranus itself appeared generally featureless' in `merged.md` -- The reference directly states this exact claim. |
| 12 | The Challenger accident killed six astronauts during a space shuttle launch | 9 | carried | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch' in `merged.md` -- The reference directly states this exact claim about the Challenger accident. |

### `merged.md` -- 26 claim(s): 0 invented, 9 contradicted, 0 supported in part, 17 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with earlier planetary encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source attributes the fulfillment of primary mission goals to Voyager 3, not Voyager 2. |
| 2 | Mission planners directed Voyager 2 to Uranus. | contradicted | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- Source context refers to Voyager 3 as the spacecraft directed to Uranus, not Voyager 2. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- Context indicates this refers to Voyager 3's Jupiter encounter, not Voyager 2's. |
| 7 | Voyager 2 became the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began" in `source_a.md` -- Source identifies Voyager 1, not Voyager 2, as the first spacecraft to fly past Uranus. |
| 8 | Short-range observations of Uranus by Voyager 2 began January 24, 1986. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source attributes observations to Voyager 1 on Jan. 31, 1987; claim says Voyager 2 on January 24, 1986. |
| 9 | Signals from Voyager 2 took approximately 2,5 hours to reach Earth. | contradicted | `source_a.md` | 'when signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Signals statement appears in Voyager 1 context, not Voyager 2 context. |
| 11 | Closest approach to Uranus took place at 17:59 ED January 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source gives year 1968; claim states 1986. |
| 12 | The closest approach to Uranus was at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Source lists 50,640 km first; claim reverses to 81,500 km first. |
| 26 | The Challenger accident occurred on January 28, 1986. | contradicted | `source_b.md` | 'Feb. 28, 1986' in `source_b.md` -- Source gives date as Feb. 28, 1986; claim states January 28, 1986. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Source directly states the journey duration to Uranus. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | supported | `source_a.md` | "The Ur anus encounter's geometry was also defined by the possibility of a future encounter with Saturn" in `source_a.md`, **transcription_error** -- Source directly states the Uranus encounter geometry was defined by Saturn encounter possibility. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby of Saturn. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- Preceding sentence about Saturn encounter geometry indicates the flyby refers to Saturn. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- Source directly states this light condition measurement. |
| 13 | Voyager 2 discovered 11 new moons. | supported | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Source directly states Voyager 2 discovered 11 new moons. |
| 14 | Voyager 2 discovered three new rings in addition to eight "older" rings. | supported | `source_b.md` | 'three new rings in addition to the "older" eight rings' in `source_b.md`, **transcription_error** -- Source states discovery of three new rings plus eight older rings. |
| 15 | Uranus has a magnetic field tilted at 66 degrees off-axis and off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Source directly describes Uranus' magnetic field characteristics. |
| 16 | Wind speeds in Uranus' atmosphere were as high as 450 km/h (72400 meters per hour). | supported | `source_b.md` | "wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour)" in `source_b.md`, **transcription_error** -- Source directly states the wind speed measurements for Uranus' atmosphere. |
| 17 | There was evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus. | supported | `source_b.md` | 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Source directly reports evidence of subsurface water lake. |
| 18 | The rings of Uranus were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- Source directly describes variability of Uranus' rings. |
| 19 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Source directly states photos of these five moons were returned. |
| 20 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | supported | `source_b.md` | "five of Uranus' smaller moons" in `source_b.md`, **transcription_error** -- Source identifies these five celestial objects as Uranus' smaller moons. |
| 21 | Voyager 2 flew by Miranda at a range of 17,560 miles (28,260 kilometers). | supported | `source_b.md` | 'at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Numerical values match despite formatting difference between periods and commas. |
| 22 | In its nearly century-long travels, Voyager 2's closest approach to any object was during its flyby of Miranda. | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.' in `source_b.md` -- Source explicitly links Miranda flyby to closest approach in spacecraft's history. |
| 23 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- Source directly states Uranus' apparent lack of surface features. |
| 24 | The Challenger accident killed six astronauts. | supported | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- Source directly states the number of astronauts killed in the Challenger accident. |
| 25 | The Challenger accident occurred during a space shuttle launch. | supported | `source_b.md` | 'during their space shuttle launch' in `source_b.md` -- Source confirms Challenger accident occurred during a space shuttle launch. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **26** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **25**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 14 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `b2` (`source_b.md`) — 'During its flyby, Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center.' is reworded in the merge and no disposition record explains it (nearest merge segment m8 at 0.98)

  ```text
  In the source: During its flyby, Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center.
  In the merge:  During its flyby, Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the "older" eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center.
  What changed:  During its flyby, Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the [-“older”-] {+"older"+} eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center.
  ```
- `b3` (`source_b.md`) — 'The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.' is reworded in the merge and no disposition record explains it (nearest merge segment m9 at 1.00)

  ```text
  In the source: The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  In the merge:  The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  What changed:  The spacecraft found wind speeds in Uranus[-’-]{+'+} atmosphere as high as 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  ```
- `b5` (`source_b.md`) — 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' is reworded in the merge and no disposition record explains it (nearest merge segment m11 at 0.99)

  ```text
  In the source: Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.
  In the merge:  Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons.
  What changed:  Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus[-’-]{+'+} smaller moons.
  ```
- `b6` (`source_b.md`) — 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.' is reworded in the merge and no disposition record explains it (nearest merge segment m12 at 0.99)

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  What changed:  In flying by Miranda at a range of only 17[-.-]{+,+}560 miles (28[-.-]{+,+}260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '17.560' (miles) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '28.260' (kilometers) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **6** departure(s) from its sources. Checking them confirms 2, rejects 4, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Corrected spacecraft identifier from Voyager 3 to Voyager 2. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back CONTRADICTED (`A-001`, `A-002`) |
| `a4` | reworded | Corrected typographical error, 'Ur anus' to 'Uranus'. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-006`) |
| `a5` | reworded | Corrected spacecraft identifier and observation date; Voyager 1 to Voyager 2, Ja | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a7` | reworded | Corrected encounter year from 1968 to 1986 and transposed kilometer/mile values. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | duplicate | Identical to base document title a1. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b9` | reworded | Corrected Challenger date from Feb. 28 to January 28, 1986; removed inaccurate ' | **rejected** | declared 'reworded', which predicts SUPPORTED; B-013 came back CONTRADICTED (`B-013`) |

## Added from outside the documents

The merge declared 5 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. No call the model made took more turns than a call that retrieves nothing can take, so it retrieved nothing and every source here is recalled rather than looked up.

5 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with earlier planetary encounters... | Voyager 3 | the model's own knowledge | *no source* | Only Voyager 1 and Voyager 2 were sent to outer planets. | *none* |
| Voyager 2 became the first human-made object to fly past Uranus... | Voyager 1's short-range observations of the planet | the model's own knowledge | *no source* | Voyager 2 was the sole spacecraft to encounter Uranus. | *none* |
| Closest approach to Uranus took place at 17:59 ED January 24, 1986... | Jan. 24, 1968 | the model's own knowledge | *no source* | Voyager 2's Uranus encounter was in 1986, not 1968. | *none* |
| ...at a range of about 81,500 kilometers (50,640 miles). | 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | 81,500 km correctly converts to approximately 50,640 miles. | *none* |
| ...during their space shuttle launch on January 28, 1986. | Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger disaster occurred on January 28, 1986, not February 28. | *none* |

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
| Duration | 684.0s |
| Generated | 2026-09-28T00:06:12+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
