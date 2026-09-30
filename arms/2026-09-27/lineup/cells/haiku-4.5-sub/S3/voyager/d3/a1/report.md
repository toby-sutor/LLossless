## Verdict

**19 finding(s).** In the claims: 12 contradicted. In the structure: 3 undeclared rewording, 4 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 29 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 14 |
| Forward — source claims accounted for in the merge | **20/26** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **7/12** |
| Forward — `source_b.md` claims accounted for | **13/14** |
| Reverse — merge claims found in a source | **23/29** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **50/55** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Voyager 2 was directed to Uranus after fulfilling its primary mission goals with three planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states Voyager 2 fulfilled its primary mission with three planetary encounters, not Voyager 3 as claimed.
- **A-004** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'Its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference describes Voyager 2's Jupiter encounter, not Voyager 3's, contradicting the spacecraft identification in the claim.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2 became the first human-made object to fly past Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies Voyager 2, not Voyager 1, as the first to fly past Uranus.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of the planet began Jan. 31, 1987.
  - `merged.md` says: 'Its observations began on January 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives January 24, 1986 as the observation date, contradicting the claim's Jan. 31, 1987; also refers to Voyager 2, not 1.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 on January 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 1986 as the year, contradicting the claim's 1968; time is correct but year is wrong.
- **B-014** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts during their space shuttle launch Feb. 28, 1986.
  - `merged.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch on January 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives January 28, 1986 as the Challenger accident date, contradicting the claim's Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 fulfilled its primary mission goals through three planetary encounters
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Voyager 3 as the spacecraft that fulfilled the mission goals, not Voyager 2.
- **M-003** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.\n\nIn fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source associates the Jupiter optimization with Voyager 3, not Voyager 2.
- **M-006** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 became the first human-made object to fly past Uranus
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source identifies Voyager 1 as the first object to fly past Uranus, not Voyager 2.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's observations began on January 24, 1986
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes observations to Voyager 1 on Jan. 31, 1987, not January 24, 1986.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 on January 24, 1986
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source indicates closest approach on January 24, 1968, not January 24, 1986.
- **M-029** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident occurred on January 28, 1986
  - `source_b.md` says: 'Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source indicates Challenger accident on Feb. 28, 1986, not January 28, 1986.

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
- **other convention** `m6` (`merged.md`) - '2,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `m13` (`merged.md`) - '17.560' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m13` (`merged.md`) - '28.260' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

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
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Voyager 2 was directed to Uranus after fulfilling its primary mission goals with three planetary encounters' in `merged.md` -- The reference text states Voyager 2 fulfilled its primary mission with three planetary encounters, not Voyager 3 as claimed. |
| 4 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'Its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `merged.md` -- The reference describes Voyager 2's Jupiter encounter, not Voyager 3's, contradicting the spacecraft identification in the claim. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2 became the first human-made object to fly past Uranus' in `merged.md` -- The reference identifies Voyager 2, not Voyager 1, as the first to fly past Uranus. |
| 8 | Voyager 1's short-range observations of the planet began Jan. 31, 1987. | 9 | contradicted | 'Its observations began on January 24, 1986' in `merged.md` -- The reference gives January 24, 1986 as the observation date, contradicting the claim's Jan. 31, 1987; also refers to Voyager 2, not 1. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 on January 24, 1986' in `merged.md` -- The reference gives 1986 as the year, contradicting the claim's 1968; time is correct but year is wrong. |
| 2 | Mission planners directed the veteran spacecraft to Uranus. | 3 | carried | 'Voyager 2 was directed to Uranus' in `merged.md` -- The reference text directly states that the spacecraft was directed to Uranus, supporting the claim. |
| 3 | A journey would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- The reference text states exactly this duration for the journey to Uranus. |
| 5 | The Ur anus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | 7 (unverified) | carried | "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn" in `merged.md` -- The reference text states this claim about Uranus encounter geometry and future Saturn encounter possibility. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` -- The reference text contains this exact statement about Voyager 1's observation duration. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals took approximately 2,5 hours to reach Earth' in `merged.md` -- The reference text states this exact signal transmission time. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions' in `merged.md` -- The reference text contains this exact statement about light conditions. |
| 12 | The closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | carried | 'at a range of about 50,640 kilometers (81,500 miles)' in `merged.md` -- The reference text provides this exact range for the closest approach to Uranus. |

### `source_b.md` -- 14 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 13 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 14 | The Challenger accident killed six astronauts during their space shuttle launch Feb. 28, 1986. | 9 | contradicted | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch on January 28, 1986' in `merged.md` -- The reference gives January 28, 1986 as the Challenger accident date, contradicting the claim's Feb. 28, 1986. |
| 1 | Voyager 2 discovered 11 new moons. | 3 | carried | 'Voyager 2 discovered 11 new moons' in `merged.md` -- The reference text states this discovery directly. |
| 2 | The moons were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | carried | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `merged.md` -- The reference text lists these exact moon names. |
| 3 | A naming tradition was begun in 1687. | 3 | carried | 'a naming tradition begun in 1687' in `merged.md` -- The reference text confirms a naming tradition was begun in 1687. |
| 4 | Voyager 2 discovered three new rings in addition to eight older rings. | 3 (unverified) | carried | 'three new rings in addition to the "older" eight rings' in `merged.md` -- The reference states three new rings were discovered in addition to eight older rings. |
| 5 | Uranus has a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- The reference text describes Uranus' magnetic field with these exact specifications. |
| 6 | Wind speeds in Uranus' atmosphere were as high as 450 km/h (72400 meters per hour). | 5 (unverified) | carried | "wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour)" in `merged.md` -- The reference text provides these exact wind speed measurements. |
| 7 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | carried | 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- The reference text describes this finding about a subsurface water body. |
| 8 | Uranus' rings are extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference describes Uranus' rings as extremely variable in these properties. |
| 9 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 (unverified) | carried | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `merged.md` -- The reference text confirms these photos were returned for these five moons. |
| 10 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 (unverified) | carried | "five of Uranus' smaller moons" in `merged.md` -- The reference identifies these five objects as Uranus' smaller moons. |
| 11 | The spacecraft flew by Miranda at a range of 17.560 miles (28.260 kilometers). | 7 | carried | 'at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- The reference provides this exact range for the Miranda flyby. |
| 12 | The spacecraft came closest to any object so far in its nearly century-long travels. | 7 | carried | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `merged.md` -- The reference text states this about the spacecraft's closest approach in its long journey. |
| 13 | Uranus appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless' in `merged.md` -- The reference text characterizes Uranus' appearance as generally featureless. |

### `merged.md` -- 29 claim(s): 0 invented, 6 contradicted, 0 supported in part, 23 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 fulfilled its primary mission goals through three planetary encounters | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source names Voyager 3 as the spacecraft that fulfilled the mission goals, not Voyager 2. |
| 3 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.\n\nIn fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- Source associates the Jupiter optimization with Voyager 3, not Voyager 2. |
| 6 | Voyager 2 became the first human-made object to fly past Uranus | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations" in `source_a.md` -- Source identifies Voyager 1 as the first object to fly past Uranus, not Voyager 2. |
| 7 | Voyager 2's observations began on January 24, 1986 | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source attributes observations to Voyager 1 on Jan. 31, 1987, not January 24, 1986. |
| 10 | Closest approach to Uranus took place at 17:59 on January 24, 1986 | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source indicates closest approach on January 24, 1968, not January 24, 1986. |
| 29 | The Challenger accident occurred on January 28, 1986 | contradicted | `source_b.md` | 'Feb. 28, 1986' in `source_b.md` -- Source indicates Challenger accident on Feb. 28, 1986, not January 28, 1986. |
| 2 | The journey to Uranus would take about 4,5 years | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Source states the journey to Uranus would take about 4,5 years. |
| 4 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn | supported | `source_a.md` | "The Ur anus encounter's geometry was also defined by the possibility of a future encounter with Saturn" in `source_a.md`, **transcription_error** -- Source states the Uranus encounter's geometry was defined by possibility of future Saturn encounter. |
| 5 | Voyager 1 had only 6.4 days of close study during its flyby | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- Source provides exact statement about Voyager 1's close study duration. |
| 8 | Signals took approximately 2,5 hours to reach Earth | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Source provides exact matching statement about signal travel time. |
| 9 | Light conditions were five-hundred times less than terrestrial conditions | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- Source provides exact matching statement about light conditions. |
| 11 | Closest approach was at a range of about 50,640 kilometers (81,500 miles) | supported | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Source provides exact matching statement about closest approach distance. |
| 12 | Voyager 2 discovered 11 new moons | supported | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Source states Voyager 2 discovered 11 new moons during its flyby. |
| 13 | The moons were given names Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II | supported | `source_b.md` | 'Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- Source lists these exact names as given to the moons discovered by Voyager 2. |
| 14 | A naming tradition was begun in 1687 | supported | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- Source states a naming tradition was begun in 1687. |
| 15 | Voyager 2 discovered three new rings | supported | `source_b.md` | 'three new rings in addition to the "older" eight rings' in `source_b.md`, **transcription_error** -- Source states three new rings were discovered by Voyager 2. |
| 16 | There were eight "older" rings | supported | `source_b.md` | 'the "older" eight rings' in `source_b.md`, **transcription_error** -- Source mentions eight older rings of Uranus. |
| 17 | A magnetic field was tilted at 66 degrees off-axis and off-center | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Source provides exact matching statement about magnetic field tilt. |
| 18 | Wind speeds in Uranus' atmosphere reached as high as 450 km/h (72400 meters per hour) | supported | `source_b.md` | "wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour)" in `source_b.md`, **transcription_error** -- Source states wind speeds reached 450 km/h with equivalent measurement in m/h. |
| 19 | Evidence was found of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface | supported | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Source describes boiling lake discovery at specified depth and distance. |
| 20 | Uranus's rings are extremely variable in thickness and transparency | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- Source states Uranus's rings are extremely variable in thickness and transparency. |
| 21 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Source identifies Voyager 2 as returning photos of these specific moons. |
| 22 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons | supported | `source_b.md` | "Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons" in `source_b.md`, **transcription_error** -- Source identifies these five objects as smaller moons of Uranus. |
| 23 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers) | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Source confirms Voyager 2 flew past Miranda at the specified distance. |
| 24 | The spacecraft came closest to any object so far in its nearly century-long travels during the flyby of Miranda | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Source states the spacecraft achieved closest approach during Miranda flyby. |
| 25 | Uranus itself appeared generally featureless | supported | `source_b.md` | 'Uranus itself appeared generally featureless' in `source_b.md` -- Source provides exact matching statement about Uranus appearance. |
| 26 | The news of the Uranus encounter was interrupted the same day by the Challenger accident | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- Source confirms Uranus news was interrupted by Challenger accident that same day. |
| 27 | The Challenger accident killed six astronauts | supported | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- Source states the Challenger accident killed six astronauts. |
| 28 | The Challenger accident occurred during a space shuttle launch | supported | `source_b.md` | 'killed six astronauts during their space shuttle launch' in `source_b.md` -- Source confirms Challenger accident occurred during a space shuttle launch. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **29** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **26**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `b2` (`source_b.md`) — 'During its flyby, Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center.' is reworded in the merge and no disposition record explains it (nearest merge segment m9 at 0.98)

  ```text
  In the source: During its flyby, Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center.
  In the merge:  During its flyby, Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the "older" eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center.
  What changed:  During its flyby, Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the [-“older”-] {+"older"+} eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center.
  ```
- `b3` (`source_b.md`) — 'The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.' is reworded in the merge and no disposition record explains it (nearest merge segment m10 at 1.00)

  ```text
  In the source: The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  In the merge:  The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  What changed:  The spacecraft found wind speeds in Uranus[-’-]{+'+} atmosphere as high as 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  ```
- `b5` (`source_b.md`) — 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' is reworded in the merge and no disposition record explains it (nearest merge segment m12 at 0.99)

  ```text
  In the source: Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.
  In the merge:  Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons.
  What changed:  Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus[-’-]{+'+} smaller moons.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **7** departure(s) from its sources. Checking them confirms 2, rejects 5, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Corrected spacecraft name and restructured phrasing for clarity. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a3` | subsumed | Content integrated into opening paragraph with a2 and a4. | **rejected** | declared 'subsumed', which predicts SUPPORTED; A-004 came back CONTRADICTED (`A-004`) |
| `a4` | subsumed | Content combined with a2 and a3 in opening section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-006`) |
| `a5` | reworded | Corrected spacecraft and encounter date; rephrased for clarity. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a7` | reworded | Corrected year from 1968 to 1986; improved date and time formatting. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED (`A-011`) |
| `b1` | duplicate | Same title as a1; base document version retained. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b9` | reworded | Corrected accident date from Feb. 28 to January 28, 1986. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-014 came back CONTRADICTED (`B-014`) |

## Added from outside the documents

The merge declared 4 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. No call the model made took more turns than a call that retrieves nothing can take, so it retrieved nothing and every source here is recalled rather than looked up.

4 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Voyager 2 was directed to Uranus after fulfilling its primary mission goals with three planetary encounters, a journey that would take about 4,5 years. | Voyager 3 | the model's own knowledge | *no source* | No Voyager 3 spacecraft existed; program consisted of Voyager 1 and 2. | *none* |
| Voyager 2 became the first human-made object to fly past Uranus. Its observations began on January 24, 1986, when signals took approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | Voyager 2 (not 1) encountered Uranus on January 24, 1986. | *none* |
| Closest approach to Uranus took place at 17:59 on January 24, 1986, at a range of about 50,640 kilometers (81,500 miles). | Jan. 24, 1968 | the model's own knowledge | *no source* | Voyager 2 encountered Uranus in January 1986, not 1968. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch on January 28, 1986. | Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger accident occurred on January 28, 1986, not February 28. | *none* |

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
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 775.2s |
| Generated | 2026-09-28T00:40:51+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content was handed to a program on this machine (`lineup haiku-4.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
