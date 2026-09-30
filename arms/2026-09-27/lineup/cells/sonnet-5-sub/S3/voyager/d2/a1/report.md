## Verdict

**32 finding(s).** In the claims: 27 contradicted. In the structure: 5 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 29 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 21 |
| Forward — source claims accounted for in the merge | **20/33** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **8/12** |
| Forward — `source_b.md` claims accounted for | **12/21** |
| Reverse — merge claims found in a source | **15/29** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **62/62** |
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
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: "The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text identifies Voyager 2, not Voyager 1, as the first to fly past Uranus.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of the planet began Jan. 31, 1987.
  - `merged.md` says: "Voyager 2's short-range observations of the planet began Jan. 31, 1986" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes this to Voyager 2 and dates it 1986, not Voyager 1 in 1987.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 1986, not 1968.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The 11 new moons were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The names in the claim differ from the spellings given in the text.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The moon names are allusions to Goethe.
  - `merged.md` says: 'allusions to Shakespeare and Alexander Pope' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes the names to Shakespeare and Pope, not Goethe.
- **B-008** -- the two documents disagree
  - `source_b.md:5` says: The wind speeds as high as 450 km/h equal 72400 meters per hour.
  - `merged.md` says: '450 km/h (450,000 meters per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text equates 450 km/h to 450,000 meters per hour, not 72400.
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'photos of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The names in the claim (Ariele, Umbrella, Titan) do not match the text's Ariel, Umbriel, Titania.
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons.
  - `merged.md` says: "five of Uranus' smaller moons" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The moon names in the claim differ from those the text lists as the five smaller moons.
- **B-016** -- the two documents disagree
  - `source_b.md:7` says: The spacecraft came closest to any object so far in its nearly century-long travels when flying by Miranda.
  - `merged.md` says: 'the spacecraft came closest to any object so far in its nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says nearly decade-long travels, not century-long.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts during their space shuttle launch.
  - `merged.md` says: 'the tragic Challenger accident that killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says seven astronauts, not six.
- **B-021** -- the two documents disagree
  - `source_b.md:9` says: The Challenger space shuttle launch occurred on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text dates the launch Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with three planetary encounters.
  - `source_a.md` says: 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes the three-encounter mission fulfillment to Voyager 3, not Voyager 2.
- **M-002** -- the two documents disagree
  - `merged.md:3` says: Mission planners directed Voyager 2 to Uranus.
  - `source_a.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The 'veteran spacecraft' directed to Uranus is identified in the same sentence as Voyager 3, not Voyager 2.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The Jupiter encounter statement's pronoun 'its' refers to the spacecraft named Voyager 3 in this document, not Voyager 2.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's short-range observations of Uranus began Jan. 31, 1986.
  - `source_a.md` says: 'began Jan. 31, 1987' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 1987 as the start date, while the claim states 1986.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states the year 1968, while the claim states 1986.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered 10 new moons.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states 11 new moons, while the claim states 10.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: The 10 new moons were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Several moon names in the claim differ from the spellings/names given in the source (e.g. Puck vs Pucka, Cressida vs Kressida, Bianca vs Bianca II).
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The moon names are allusions to Shakespeare and Alexander Pope.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes the names to Goethe, not Shakespeare and Alexander Pope.
- **M-019** -- the two documents disagree
  - `merged.md:7` says: The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour).
  - `source_b.md` says: 'as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 72400 meters per hour, while the claim states 450,000 meters per hour.
- **M-022** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source lists Titan (a Saturn moon) rather than Titania, and different spellings for other moons, conflicting with the claim's list.
- **M-023** -- the two documents disagree
  - `merged.md:9` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons.
  - `source_b.md` says: 'five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The five-moon group in the source includes Titan rather than Titania, conflicting with the claim's specific list of moons.
- **M-025** -- the two documents disagree
  - `merged.md:9` says: The Miranda flyby was the closest Voyager 2 had come to any object so far in its nearly decade-long travels.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states 'century-long' travels, while the claim states 'decade-long'.
- **M-029** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident killed seven astronauts during their space shuttle launch Jan. 28, 1986.
  - `source_b.md` says: 'that killed six astronauts during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source states six astronauts died on Feb. 28, 1986, while the claim states seven astronauts and Jan. 28, 1986.

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
- **readable two ways** `m12` (`merged.md`) - '17.560' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m12` (`merged.md`) - '28.260' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 4 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' in `merged.md` -- The text attributes this to Voyager 2, not Voyager 3. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | "The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986" in `merged.md` -- The text identifies Voyager 2, not Voyager 1, as the first to fly past Uranus. |
| 8 | Voyager 1's short-range observations of the planet began Jan. 31, 1987. | 9 | contradicted | "Voyager 2's short-range observations of the planet began Jan. 31, 1986" in `merged.md` -- The text attributes this to Voyager 2 and dates it 1986, not Voyager 1 in 1987. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986' in `merged.md` -- The text states 1986, not 1968. |
| 2 | Mission planners directed the veteran spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly stated. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Directly stated. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Directly stated. |
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | 7 | carried | "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn" in `merged.md` -- Directly stated. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` -- Directly stated. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Directly stated. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions' in `merged.md` -- Directly stated. |
| 12 | Closest approach to Uranus occurred at a range of about 50,640 kilometers (81,500 miles). | 9 | carried | 'at a range of about 50,640 kilometers (81,500 miles)' in `merged.md` -- Directly stated. |

### `source_b.md` -- 21 claim(s): 0 dropped, 9 contradicted, 0 carried in part, 12 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 2 discovered 11 new moons during its flyby. | 3 | contradicted | 'Voyager 2 discovered 10 new moons' in `merged.md` -- The text states 10 new moons, not 11. |
| 2 | The 11 new moons were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The names in the claim differ from the spellings given in the text. |
| 3 | The moon names are allusions to Goethe. | 3 | contradicted | 'allusions to Shakespeare and Alexander Pope' in `merged.md` -- The text attributes the names to Shakespeare and Pope, not Goethe. |
| 8 | The wind speeds as high as 450 km/h equal 72400 meters per hour. | 5 | contradicted | '450 km/h (450,000 meters per hour)' in `merged.md` -- The text equates 450 km/h to 450,000 meters per hour, not 72400. |
| 12 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'photos of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The names in the claim (Ariele, Umbrella, Titan) do not match the text's Ariel, Umbriel, Titania. |
| 13 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 | contradicted | "five of Uranus' smaller moons" in `merged.md` -- The moon names in the claim differ from those the text lists as the five smaller moons. |
| 16 | The spacecraft came closest to any object so far in its nearly century-long travels when flying by Miranda. | 7 | contradicted | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- The text says nearly decade-long travels, not century-long. |
| 20 | The Challenger accident killed six astronauts during their space shuttle launch. | 9 | contradicted | 'the tragic Challenger accident that killed seven astronauts' in `merged.md` -- The text says seven astronauts, not six. |
| 21 | The Challenger space shuttle launch occurred on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The text dates the launch Jan. 28, 1986, not Feb. 28, 1986. |
| 4 | The naming tradition for the moons began in 1687. | 3 | carried | 'continuing a naming tradition begun in 1687' in `merged.md` -- Directly stated. |
| 5 | Voyager 2 discovered three new rings in addition to the older eight rings. | 3 | carried | 'three new rings in addition to the “older” eight rings' in `merged.md` -- Directly stated. |
| 6 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- Directly stated. |
| 7 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h. | 5 | carried | "wind speeds in Uranus' atmosphere as high as 450 km/h" in `merged.md` -- Directly stated. |
| 9 | The spacecraft found evidence of a boiling lake of water some 479 miles below the top cloud surface. | 5 | carried | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- Directly stated. |
| 10 | 479 miles equals 900 kilometers. | 5 | carried | '479 miles (900 kilometers)' in `merged.md` -- Directly stated. |
| 11 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- Directly stated. |
| 14 | Voyager 2 flew by Miranda at a range of only 17.560 miles. | 7 | carried | 'flying by Miranda at a range of only 17.560 miles' in `merged.md` -- Directly stated. |
| 15 | 17.560 miles equals 28.260 kilometers. | 7 | carried | '17.560 miles (28.260 kilometers)' in `merged.md` -- Directly stated. |
| 17 | Images of Miranda showed a strange object whose surface was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- Directly stated. |
| 18 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless' in `merged.md` -- Directly stated. |
| 19 | The news of the Uranus encounter was interrupted the same day by the Challenger accident. | 9 | carried | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `merged.md` -- Directly stated. |

### `merged.md` -- 29 claim(s): 0 invented, 14 contradicted, 0 supported in part, 15 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with three planetary encounters. | contradicted | `source_a.md` | 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source attributes the three-encounter mission fulfillment to Voyager 3, not Voyager 2. |
| 2 | Mission planners directed Voyager 2 to Uranus. | contradicted | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The 'veteran spacecraft' directed to Uranus is identified in the same sentence as Voyager 3, not Voyager 2. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The Jupiter encounter statement's pronoun 'its' refers to the spacecraft named Voyager 3 in this document, not Voyager 2. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- The source identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus. |
| 8 | Voyager 2's short-range observations of Uranus began Jan. 31, 1986. | contradicted | `source_a.md` | 'began Jan. 31, 1987' in `source_a.md` -- The source gives 1987 as the start date, while the claim states 1986. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- The source states the year 1968, while the claim states 1986. |
| 13 | During its flyby, Voyager 2 discovered 10 new moons. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- The source states 11 new moons, while the claim states 10. |
| 14 | The 10 new moons were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- Several moon names in the claim differ from the spellings/names given in the source (e.g. Puck vs Pucka, Cressida vs Kressida, Bianca vs Bianca II). |
| 15 | The moon names are allusions to Shakespeare and Alexander Pope. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- The source attributes the names to Goethe, not Shakespeare and Alexander Pope. |
| 19 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour). | contradicted | `source_b.md` | 'as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives 72400 meters per hour, while the claim states 450,000 meters per hour. |
| 22 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The source lists Titan (a Saturn moon) rather than Titania, and different spellings for other moons, conflicting with the claim's list. |
| 23 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons. | contradicted | `source_b.md` | 'five of Uranus’ smaller moons' in `source_b.md` -- The five-moon group in the source includes Titan rather than Titania, conflicting with the claim's specific list of moons. |
| 25 | The Miranda flyby was the closest Voyager 2 had come to any object so far in its nearly decade-long travels. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source states 'century-long' travels, while the claim states 'decade-long'. |
| 29 | The Challenger accident killed seven astronauts during their space shuttle launch Jan. 28, 1986. | contradicted | `source_b.md` | 'that killed six astronauts during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- The source states six astronauts died on Feb. 28, 1986, while the claim states seven astronauts and Jan. 28, 1986. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Matches the stated travel time exactly. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Saturn. | supported | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- Directly matches the claim about geometry being defined by a future Saturn encounter. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- Directly stated in the source. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Matches the claim exactly. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- Matches the claim exactly. |
| 12 | Closest approach to Uranus occurred at a range of about 50,640 kilometers (81,500 miles). | supported | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Matches the claim exactly. |
| 16 | The moon-naming tradition began in 1687. | supported | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- Matches the claim exactly. |
| 17 | During its flyby, Voyager 2 discovered three new rings in addition to the older eight rings. | supported | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Matches the claim exactly. |
| 18 | During its flyby, Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Matches the claim exactly. |
| 20 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | supported | `source_b.md` | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Matches the claim exactly. |
| 21 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- Matches the claim exactly. |
| 24 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Matches the claim exactly. |
| 26 | Images of Miranda showed a surface that was a mishmash of peculiar features that seemed to have no rhyme or reason. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason' in `source_b.md` -- Matches the claim's description of Miranda's surface. |
| 27 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless' in `source_b.md` -- Matches the claim exactly. |
| 28 | The Challenger accident occurred the same day as the Uranus encounter news. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- Matches the claim exactly. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **29** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **33**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 14 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **10** departure(s) from its sources. Checking them confirms 1, rejects 8, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Corrected nonexistent Voyager 3 to Voyager 2. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Fixed misspelling of Uranus. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-005`, `A-006`) |
| `a5` | reworded | Corrected spacecraft name and flyby year. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a7` | reworded | Corrected flyby year to 1986. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED (`A-011`) |
| `b1` | superseded | Duplicate title; base document's title kept. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Fixed moon-name spellings, attribution, and moon count. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED (`B-001`, `B-002`, `B-003`) |
| `b3` | reworded | Corrected wrong km/h to m/h conversion. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED (`B-008`) |
| `b5` | reworded | Fixed misspelled moon names. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back CONTRADICTED, B-013 came back CONTRADICTED (`B-012`, `B-013`) |
| `b6` | reworded | Corrected century-long to decade-long travel time. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-016 came back CONTRADICTED (`B-016`) |
| `b9` | reworded | Corrected Challenger date and crew count. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-020 came back CONTRADICTED, B-021 came back CONTRADICTED (`B-020`, `B-021`) |

## Added from outside the documents

The merge declared 10 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. No call the model made took more turns than a call that retrieves nothing can take, so it retrieved nothing and every source here is recalled rather than looked up.

10 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 | the model's own knowledge | *no source* | Voyager 3 never existed; only Voyager 1 and 2 were launched. | *none* |
| The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986, when signals took approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations | the model's own knowledge | *no source* | Voyager 1 never visited Uranus; only Voyager 2 did. | *none* |
| The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986, when signals took approximately 2,5 hours to reach Earth. | Jan. 31, 1987 | the model's own knowledge | *no source* | Voyager 2 reached Uranus in January 1986, not 1987. | *none* |
| Closest approach to Uranus took place at 17:59 ED Jan. 24, 1986, at a range of about 50,640 kilometers (81,500 miles). | Jan. 24, 1968 | the model's own knowledge | *no source* | Voyager 2's Uranus flyby occurred in 1986, not 1968. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – allusions to Shakespeare and Alexander Pope, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center. | obvious allusions to Goethe | the model's own knowledge | *no source* | Uranus's moons are named for Shakespeare and Pope characters, not Goethe. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – allusions to Shakespeare and Alexander Pope, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center. | discovered 11 new moons | the model's own knowledge | *no source* | Voyager 2 found ten new Uranian moons, matching the list given. | *none* |
| The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (450,000 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 72400 meters per hour | the model's own knowledge | *no source* | 450 km/h converts to 450,000 meters per hour, not 72,400. | *none* |
| In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels. | nearly century-long travels | the model's own knowledge | *no source* | Voyager 2 launched in 1977, only about nine years before this flyby. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | killed six astronauts | the model's own knowledge | *no source* | The Challenger crew numbered seven, not six. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | Feb. 28, 1986 | the model's own knowledge | *no source* | The Challenger disaster occurred on Jan. 28, 1986. | *none* |

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
| Duration | 268.0s |
| Generated | 2026-09-27T23:54:47+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
