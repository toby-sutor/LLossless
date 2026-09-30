## Verdict

**25 finding(s).** In the claims: 14 contradicted, 2 partially invented. In the structure: 2 undeclared rewording, 7 verbatim violation. 6 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 21 |
| Claims extracted from `source_a.md` | 9 |
| Claims extracted from `source_b.md` | 13 |
| Forward — source claims accounted for in the merge | **12/22** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **2/9** |
| Forward — `source_b.md` claims accounted for | **10/13** |
| Reverse — merge claims found in a source | **15/21** |
| Reverse — supported only in part | 2 |
| Evidence grounded | **40/43** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states Voyager 2 was directed to Uranus, not Voyager 3.
- **A-003** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states Voyager 2's encounter with Jupiter was optimized, not Voyager 3's.
- **A-004** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby of Uranus.
  - `merged.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text attributes the 6.4 days of close study to Voyager 1's flyby of Saturn, not Uranus.
- **A-005** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2 was the first human-made object to fly past Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states Voyager 2, not Voyager 1, was the first human-made object to fly past Uranus.
- **A-006** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: 'Its short-range observations of the planet began on 24 January 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text gives the date as 24 January 1986, not Jan. 31, 1987, and refers to Voyager 2, not Voyager 1.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Signals from Voyager 1 took approximately 2,5 hours to reach Earth.
  - `merged.md` says: 'when signals took approximately 2.5 hours to reach Earth' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text attributes the 2.5-hour signal delay to Voyager 2, not Voyager 1.
- **A-009** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 EST on 24 January 1986, at a range of about 50,640 kilometres (81,500 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text gives the date as 24 January 1986, not 24 January 1968, and the time zone as EST, not ED.
- **B-008** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titan' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text spells the moon names as Ariel and Umbriel, not Ariele and Umbrella.
- **B-009** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons.
  - `merged.md` says: "Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titan, five of Uranus' smaller moons" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text correctly spells these as Ariel and Umbriel, not Ariele and Umbrella.
- **B-013** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts during their space shuttle launch Feb. 28, 1986.
  - `merged.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch on 28 January 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text gives the Challenger accident date as 28 January 1986, not Feb. 28, 1986.
- **M-004** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states Voyager 1 was the first human-made object to fly past Uranus, not Voyager 2.
- **M-005** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's short-range observations of Uranus began on 24 January 1986.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states observations began Jan. 31, 1987, not Jan. 24, 1986. Also, source attributes this to Voyager 1, not Voyager 2.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 EST on 24 January 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states date was Jan. 24, 1968, not Jan. 24, 1986. Also states ED not EST.
- **M-020** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident occurred on 28 January 1986.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states Challenger accident occurred on Feb. 28, 1986, not Jan. 28, 1986.

### Partly invented — the sources carry some of this claim

- **M-016** (`merged.md:9`) — Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titan.
  - evidence: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source lists Miranda, Oberon, Ariele, Umbrella, and Titan. Claim names Ariel and Umbriel, which differ from source's Ariele and Umbrella.
- **M-017** (`merged.md:9`) — Miranda, Oberon, Ariel, Umbriel, and Titan are five of Uranus' smaller moons.
  - evidence: "five of Uranus' smaller moons" in `source_b.md` (transcription_error)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source describes them as five of Uranus' smaller moons, but the specific names in claim differ from source spelling.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | votes | 4.5, 6.4, 2.5 | none | English (75 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **readable two ways** `m14` (`merged.md`) - '17.560' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its numerals (3 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m14` (`merged.md`) - '28.260' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its numerals (3 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

## Length capped

- `$.dispositions[1].reason` was 103 characters, over the 80-character cap; capped to fit
- `$.dispositions[3].reason` was 93 characters, over the 80-character cap; capped to fit
- `$.dispositions[4].reason` was 92 characters, over the 80-character cap; capped to fit
- `$.decisions[1].reason` was 97 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 9 claim(s): 0 dropped, 7 contradicted, 0 carried in part, 2 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- The reference text states Voyager 2 was directed to Uranus, not Voyager 3. |
| 3 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- The reference text states Voyager 2's encounter with Jupiter was optimized, not Voyager 3's. |
| 4 | Voyager 1 had only 6.4 days of close study during its flyby of Uranus. | 7 | contradicted | 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` -- The reference text attributes the 6.4 days of close study to Voyager 1's flyby of Saturn, not Uranus. |
| 5 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2 was the first human-made object to fly past Uranus' in `merged.md` -- The reference text states Voyager 2, not Voyager 1, was the first human-made object to fly past Uranus. |
| 6 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | 'Its short-range observations of the planet began on 24 January 1986' in `merged.md` -- The reference text gives the date as 24 January 1986, not Jan. 31, 1987, and refers to Voyager 2, not Voyager 1. |
| 7 | Signals from Voyager 1 took approximately 2,5 hours to reach Earth. | 9 | contradicted | 'when signals took approximately 2.5 hours to reach Earth' in `merged.md` -- The reference text attributes the 2.5-hour signal delay to Voyager 2, not Voyager 1. |
| 9 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 EST on 24 January 1986, at a range of about 50,640 kilometres (81,500 miles)' in `merged.md` -- The reference text gives the date as 24 January 1986, not 24 January 1968, and the time zone as EST, not ED. |
| 2 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4.5 years' in `merged.md` -- The reference text states the journey to Uranus would take about 4.5 years. |
| 8 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five hundred times less than terrestrial conditions' in `merged.md` -- The reference text states light conditions at Uranus were five hundred times less than terrestrial conditions. |

### `source_b.md` -- 13 claim(s): 0 dropped, 3 contradicted, 0 carried in part, 10 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 8 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titan' in `merged.md` -- The reference text spells the moon names as Ariel and Umbriel, not Ariele and Umbrella. |
| 9 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 (unverified) | contradicted | "Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titan, five of Uranus' smaller moons" in `merged.md` -- The reference text correctly spells these as Ariel and Umbriel, not Ariele and Umbrella. |
| 13 | The Challenger accident killed six astronauts during their space shuttle launch Feb. 28, 1986. | 9 | contradicted | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch on 28 January 1986' in `merged.md` -- The reference text gives the Challenger accident date as 28 January 1986, not Feb. 28, 1986. |
| 1 | During its flyby, Voyager 2 discovered 11 new moons. | 3 | carried | 'During its flyby, Voyager 2 discovered 11 new moons' in `merged.md` -- The reference text directly states Voyager 2 discovered 11 new moons during its flyby. |
| 2 | The 11 new moons discovered by Voyager 2 were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | carried | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `merged.md` -- The reference text lists these exact moon names among those discovered by Voyager 2. |
| 3 | Voyager 2 discovered three new rings in addition to the older eight rings of Uranus. | 3 (unverified) | carried | 'three new rings in addition to the eight known rings' in `merged.md` -- The reference text states Voyager 2 discovered three new rings in addition to the eight known rings of Uranus. |
| 4 | Uranus has a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-centre' in `merged.md` -- The reference text states Uranus has a magnetic field tilted at 66 degrees off-axis and off-centre. |
| 5 | Wind speeds in Uranus' atmosphere are as high as 450 km/h (72400 meters per hour). | 5 (unverified) | carried | "wind speeds in Uranus' atmosphere as high as 450 km/h (72,400 metres per hour)" in `merged.md` -- The reference text states wind speeds in Uranus' atmosphere reach 450 km/h as specified. |
| 6 | There is evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus. | 5 | carried | 'evidence of a boiling lake of water some 479 miles (900 kilometres) below the top cloud surface' in `merged.md` -- The reference text states Voyager 2 found evidence of a boiling lake of water at the specified depth. |
| 7 | Uranus' rings are extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference text states Uranus' rings were found to be extremely variable in thickness and transparency. |
| 10 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometres)' in `merged.md` -- The reference text states Voyager 2 flew by Miranda at a range of 17.560 miles (28.260 kilometres). |
| 11 | Voyager 2 came closest to Miranda than to any other object in its nearly century-long travels. | 7 | carried | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `merged.md` -- The reference text states Voyager 2 came closest to Miranda than to any other object in its nearly century-long travels. |
| 12 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- The reference text states images of Miranda showed a surface that was a mishmash of peculiar features. |

### `merged.md` -- 21 claim(s): 0 invented, 4 contradicted, 2 supported in part, 15 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 4 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations" in `source_a.md` -- Source states Voyager 1 was the first human-made object to fly past Uranus, not Voyager 2. |
| 5 | Voyager 2's short-range observations of Uranus began on 24 January 1986. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source states observations began Jan. 31, 1987, not Jan. 24, 1986. Also, source attributes this to Voyager 1, not Voyager 2. |
| 8 | Closest approach to Uranus took place at 17:59 EST on 24 January 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source states date was Jan. 24, 1968, not Jan. 24, 1986. Also states ED not EST. |
| 20 | The Challenger accident occurred on 28 January 1986. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source states Challenger accident occurred on Feb. 28, 1986, not Jan. 28, 1986. |
| 16 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titan. | supported in part | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Source lists Miranda, Oberon, Ariele, Umbrella, and Titan. Claim names Ariel and Umbriel, which differ from source's Ariele and Umbrella. |
| 17 | Miranda, Oberon, Ariel, Umbriel, and Titan are five of Uranus' smaller moons. | supported in part | `source_b.md` | "five of Uranus' smaller moons" in `source_b.md`, **transcription_error** -- Source describes them as five of Uranus' smaller moons, but the specific names in claim differ from source spelling. |
| 1 | Voyager 2 had fulfilled its primary mission goals with three planetary encounters. | supported | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source states Voyager 3 fulfilled primary mission with three planetary encounters. The claim attributes this to Voyager 2, which appears to be a naming error in the sources themselves. |
| 2 | The journey from Voyager 2's primary mission to Uranus would take about 4.5 years. | supported | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years' in `source_a.md` -- Source states the journey would take about 4.5 years (shown as 4,5 in original). The claim restates this with standard decimal notation. |
| 3 | Voyager 1 had 6.4 days of close study during its flyby of Uranus. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- Source explicitly states Voyager 1 had only 6.4 days of close study during its Uranus flyby. |
| 6 | Signals from Voyager 2 took approximately 2.5 hours to reach Earth. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Source states signals took approximately 2.5 hours to reach Earth. |
| 7 | Light conditions at Uranus were five hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- Source explicitly states light conditions were five-hundred times less than terrestrial conditions. |
| 9 | Closest approach to Uranus was at a range of about 50,640 kilometres (81,500 miles). | supported | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Source states closest approach was at a range of about 50,640 kilometers (81,500 miles). |
| 10 | Voyager 2 discovered 11 new moons during its Uranus flyby. | supported | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Source explicitly states Voyager 2 discovered 11 new moons during its flyby. |
| 11 | Voyager 2 discovered three new rings at Uranus in addition to the eight known rings. | supported | `source_b.md` | 'three new rings in addition to the "older" eight rings' in `source_b.md`, **transcription_error** -- Source states three new rings were discovered in addition to eight older rings. |
| 12 | Uranus has a magnetic field tilted at 66 degrees off-axis and off-centre. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Source states magnetic field was tilted at 66 degrees off-axis and off-center. |
| 13 | Wind speeds in Uranus' atmosphere are as high as 450 km/h (72,400 metres per hour). | supported | `source_b.md` | "wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour)" in `source_b.md`, **transcription_error** -- Source states wind speeds were as high as 450 km/h. |
| 14 | There is evidence of a boiling lake of water some 479 miles (900 kilometres) below the top cloud surface of Uranus. | supported | `source_b.md` | 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Source explicitly states evidence of a boiling lake of water some 479 miles below the top cloud surface. |
| 15 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- Source states Uranus' rings were found to be extremely variable in thickness and transparency. |
| 18 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometres). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Source states Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). |
| 19 | Voyager 2 came closest to any object in its nearly century-long travels when passing Miranda. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Source explicitly states Voyager 2 came closest to any object during its nearly century-long travels at Miranda. |
| 21 | The Challenger accident killed six astronauts. | supported | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- Source explicitly states the Challenger accident killed six astronauts. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **21** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **22**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 14 attributed segment(s) — sources in blocks, at least one out of its source order. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a4` (`source_a.md`) — 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.' is reworded in the merge and no disposition record explains it (nearest merge segment m4 at 0.99)

  ```text
  In the source: The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.
  In the merge:  The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.
  What changed:  The Ur[- -]anus encounter[-’-]{+'+}s geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.
  ```
- `b9` (`source_b.md`) — 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' is reworded in the merge and no disposition record explains it (nearest merge segment m16 at 0.96)

  ```text
  In the source: The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.
  In the merge:  The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch on 28 January 1986.
  What changed:  The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch [-Feb. 28,-] {+on 28 January+} 1986.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a2` (`source_a.md`) — numeric '4,5' (years) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '2,5' (hours) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **8** departure(s) from its sources. Checking them confirms 4, rejects 4, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Standardized spacing in decimal number from 4,5 to 4.5. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a5` | reworded | Corrected spacecraft name from Voyager 1 to Voyager 2 and standardized date form | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED, A-007 came back CONTRADICTED (`A-005`, `A-006`, `A-007`) |
| `a6` | reworded | Changed five-hundred to five hundred for consistency. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-008`) |
| `a7` | reworded | Corrected year from 1968 to 1986, timezone notation, date format, and spelled ou | **rejected** | declared 'reworded', which predicts SUPPORTED; A-009 came back CONTRADICTED (`A-009`) |
| `b2` | reworded | Changed em-dash style, capitalized 'off-centre', and changed 'older' eight to 'k | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-001`, `B-002`, `B-004`) |
| `b3` | reworded | Changed metres per hour from singular to metric style with comma separator. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `b5` | reworded | Corrected moon names: Ariele to Ariel and Umbrella to Umbriel. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED (`B-008`) |
| `b6` | reworded | Standardized spacing in decimal numbers and changed kilometres spelling. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-010`, `B-011`) |

## Added from outside the documents

The merge declared 2 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

2 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Voyager 2 was the first human-made object to fly past Uranus. | The first human-made object to fly past Uranus, Voyager 1's short-range observations | the model's own knowledge | *no source* | Source a incorrectly names Voyager 1; the encounter was Voyager 2's mission. | *none* |
| Closest approach to Uranus took place at 17:59 EST on 24 January 1986, at a range of about 50,640 kilometres (81,500 miles). | 17:59 ED Jan. 24, 1968 | the model's own knowledge | *no source* | Source a date 1968 is impossible; Voyager 2 reached Uranus in January 1986. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | claude-haiku-4-5-20251001 |
| Model (decompose) | claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic, effort decompose one level (extended thinking on/off; default kept), merge one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | 27,545 in, 11,671 out |
| Cost | ~$0.09 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 85.8s |
| Generated | 2026-09-27T18:00:55+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
