## Verdict

**34 finding(s).** In the claims: 21 contradicted, 1 partially invented. In the structure: 2 undeclared rewording, 1 false departure, 9 verbatim violation. **3 contradiction(s) below are covering values the merge declared and this tool confirmed.** At fidelity `open` a merge may carry a value spanning two disagreeing figures, and such a value asserts an edge the narrower source denies -- so the contradiction is what the licence produces, not evidence the merge went wrong. It stays a finding because nothing here parses a number: a covering value and a *narrowing* one are the same shape to every check in this tool, and only a reader can tell them apart. 6 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 25 |
| Claims extracted from `source_a.md` | 10 |
| Claims extracted from `source_b.md` | 15 |
| Forward — source claims accounted for in the merge | **12/25** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **3/10** |
| Forward — `source_b.md` claims accounted for | **9/15** |
| Reverse — merge claims found in a source | **16/25** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **47/50** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states mission planners directed Voyager 2 to Uranus, not Voyager 3.
- **A-003** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text attributes this to Voyager 2, not Voyager 3, which contradicts the claim.
- **A-004** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby of Uranus.
  - `merged.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text does not specify that Voyager 1's flyby was of Uranus; it only mentions 6.4 days of close study without identifying the planet.
- **A-005** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2 became the first human-made object to fly past Uranus.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states Voyager 2, not Voyager 1, was the first human-made object to fly past Uranus.
- **A-006** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of the planet began Jan. 31, 1987.
  - `merged.md` says: 'Short-range observations of the planet began on January 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states observations began January 24, 1986, not January 31, 1987, and attributes them to Voyager 2, not Voyager 1.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Signals from Voyager 1 took approximately 2,5 hours to reach Earth.
  - `merged.md` says: 'signals took approximately 2.5 hours to reach Earth' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text attributes this signal delay to Voyager 2, not Voyager 1.
- **A-009** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 EST on January 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states the closest approach occurred on January 24, 1986 at 17:59 EST, not January 24, 1968 at 17:59 ED.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The new moons were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text gives different names: Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca—not Pucka, Portila, Juliette, Kressida, Rosalinde, or Bianca II.
- **B-008** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text names Ariel and Umbriel, not Ariele and Umbrella, and Titania, not Titan.
- **B-009** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons.
  - `merged.md` says: "Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text names these five moons as Ariel and Umbriel, not Ariele and Umbrella, and Titania, not Titan.
- **B-010** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 flew by Miranda at a range of only 17.560 miles.
  - `merged.md` says: 'In flying by Miranda at a range of only 17,560 miles (28,260 kilometers)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states 17,560 miles, not 17.560 miles (which would be 17 miles with decimal notation).
- **B-014** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts during their space shuttle launch.
  - `merged.md` says: 'the tragic Challenger accident that killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states the Challenger accident killed seven astronauts, not six.
- **B-015** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch on January 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states the Challenger accident occurred on January 28, 1986, not February 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with three planetary encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states Voyager 3, not Voyager 2, fulfilled primary mission goals with three planetary encounters.
- **M-006** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 became the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Short-range observations of Uranus began on January 24, 1986.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states observations began Jan. 31, 1987, not January 24, 1986.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 EST on January 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states closest approach was Jan. 24, 1968, not 1986, and uses ED not EST.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: The new moons discovered were named Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source lists different spellings: Pucka not Puck, Portila not Portia, Juliette not Juliet, Kressida not Cressida, Rosalinde not Rosalind, Cordelina not Cordelia, Bianca II not Bianca.
- **M-020** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source lists Ariele and Umbrella, not Ariel and Umbriel, and Titan not Titania.
- **M-024** -- the two documents disagree
  - `merged.md:11` says: The Challenger accident occurred on January 28, 1986.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states the Challenger accident occurred Feb. 28, 1986, not January 28, 1986.
- **M-025** -- the two documents disagree
  - `merged.md:11` says: Seven astronauts were killed during the Challenger space shuttle launch.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states six astronauts were killed, not seven.

### Partly invented — the sources carry some of this claim

- **M-021** (`merged.md:9`) — Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons.
  - evidence: "Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons" in `source_b.md` (transcription_error)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source confirms these are five of Uranus' smaller moons, but the moon names in the claim differ from those in the source.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | votes | 4.5, 6.4, 2.5 | none | English (74 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
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

- `$.dispositions[5].reason` was 90 characters, over the 80-character cap; capped to fit
- `$.dispositions[6].reason` was 91 characters, over the 80-character cap; capped to fit
- `$.dispositions[7].reason` was 85 characters, over the 80-character cap; capped to fit
- `$.additions[0].reason` was 81 characters, over the 80-character cap; capped to fit
- `$.additions[2].reason` was 86 characters, over the 80-character cap; capped to fit
- `$.additions[3].reason` was 86 characters, over the 80-character cap; capped to fit
- `$.additions[5].reason` was 91 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 10 claim(s): 0 dropped, 7 contradicted, 0 carried in part, 3 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- The reference text states mission planners directed Voyager 2 to Uranus, not Voyager 3. |
| 3 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- The reference text attributes this to Voyager 2, not Voyager 3, which contradicts the claim. |
| 4 | Voyager 1 had only 6.4 days of close study during its flyby of Uranus. | 7 | contradicted | 'Voyager 1 had only 6.4 days of close study during its flyby' in `merged.md` -- The reference text does not specify that Voyager 1's flyby was of Uranus; it only mentions 6.4 days of close study without identifying the planet. |
| 5 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2 became the first human-made object to fly past Uranus.' in `merged.md` -- The reference text states Voyager 2, not Voyager 1, was the first human-made object to fly past Uranus. |
| 6 | Voyager 1's short-range observations of the planet began Jan. 31, 1987. | 9 | contradicted | 'Short-range observations of the planet began on January 24, 1986' in `merged.md` -- The reference text states observations began January 24, 1986, not January 31, 1987, and attributes them to Voyager 2, not Voyager 1. |
| 7 | Signals from Voyager 1 took approximately 2,5 hours to reach Earth. | 9 | contradicted | 'signals took approximately 2.5 hours to reach Earth' in `merged.md` -- The reference text attributes this signal delay to Voyager 2, not Voyager 1. |
| 9 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 EST on January 24, 1986' in `merged.md` -- The reference text states the closest approach occurred on January 24, 1986 at 17:59 EST, not January 24, 1968 at 17:59 ED. |
| 2 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4.5 years' in `merged.md` -- The reference text states the journey to Uranus would take about 4.5 years, matching the claim's timeframe. |
| 8 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions.' in `merged.md` -- The reference text directly states that light conditions were five-hundred times less than terrestrial conditions. |
| 10 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | carried | 'at a range of about 50,640 kilometers (81,500 miles)' in `merged.md` -- The reference text states the closest approach was at a range of about 50,640 kilometers (81,500 miles). |

### `source_b.md` -- 15 claim(s): 0 dropped, 6 contradicted, 0 carried in part, 9 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | The new moons were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The reference text gives different names: Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca—not Pucka, Portila, Juliette, Kressida, Rosalinde, or Bianca II. |
| 8 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The reference text names Ariel and Umbriel, not Ariele and Umbrella, and Titania, not Titan. |
| 9 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus' smaller moons. | 7 (unverified) | contradicted | "Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons" in `merged.md` -- The reference text names these five moons as Ariel and Umbriel, not Ariele and Umbrella, and Titania, not Titan. |
| 10 | Voyager 2 flew by Miranda at a range of only 17.560 miles. | 7 | contradicted | 'In flying by Miranda at a range of only 17,560 miles (28,260 kilometers)' in `merged.md` -- The reference text states 17,560 miles, not 17.560 miles (which would be 17 miles with decimal notation). |
| 14 | The Challenger accident killed six astronauts during their space shuttle launch. | 9 | contradicted | 'the tragic Challenger accident that killed seven astronauts' in `merged.md` -- The reference text states the Challenger accident killed seven astronauts, not six. |
| 15 | The Challenger accident occurred on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch on January 28, 1986' in `merged.md` -- The reference text states the Challenger accident occurred on January 28, 1986, not February 28, 1986. |
| 1 | During its flyby, Voyager 2 discovered 11 new moons. | 3 | carried | 'Voyager 2 discovered 11 new moons' in `merged.md` -- The reference text states that during its flyby, Voyager 2 discovered 11 new moons. |
| 3 | Voyager 2 discovered three new rings in addition to eight older rings. | 3 (unverified) | carried | 'three new rings in addition to the eight previously known rings' in `merged.md` -- The reference text states Voyager 2 discovered three new rings in addition to the eight previously known rings. |
| 4 | Uranus has a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | carried | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `merged.md` -- The reference text states that Uranus has a magnetic field tilted at 66 degrees off-axis and off-center. |
| 5 | Wind speeds in Uranus' atmosphere reached as high as 450 km/h. | 5 (unverified) | carried | "wind speeds in Uranus' atmosphere as high as 450 km/h" in `merged.md` -- The reference text states the spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h. |
| 6 | The spacecraft found evidence of a boiling lake of water some 479 miles below the top cloud surface of Uranus. | 5 | carried | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- The reference text states the spacecraft found evidence of a boiling lake of water some 479 miles below the top cloud surface. |
| 7 | The rings of Uranus were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- The reference text states that Uranus' rings were found to be extremely variable in thickness and transparency. |
| 11 | The spacecraft came closest to Miranda during its nearly century-long travels. | 7 | carried | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `merged.md` -- The reference text states the spacecraft came closest to Miranda during its nearly century-long travels. |
| 12 | The surface of Miranda was a mishmash of peculiar features. | 7 | carried | 'whose surface was a mishmash of peculiar features' in `merged.md` -- The reference text states that Miranda's surface was a mishmash of peculiar features. |
| 13 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- The reference text directly states that Uranus itself appeared generally featureless. |

### `merged.md` -- 25 claim(s): 0 invented, 8 contradicted, 1 supported in part, 16 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with three planetary encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source states Voyager 3, not Voyager 2, fulfilled primary mission goals with three planetary encounters. |
| 6 | Voyager 2 became the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations" in `source_a.md` -- Source identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus. |
| 7 | Short-range observations of Uranus began on January 24, 1986. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source states observations began Jan. 31, 1987, not January 24, 1986. |
| 10 | Closest approach to Uranus took place at 17:59 EST on January 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source states closest approach was Jan. 24, 1968, not 1986, and uses ED not EST. |
| 13 | The new moons discovered were named Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- Source lists different spellings: Pucka not Puck, Portila not Portia, Juliette not Juliet, Kressida not Cressida, Rosalinde not Rosalind, Cordelina not Cordelia, Bianca II not Bianca. |
| 20 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Source lists Ariele and Umbrella, not Ariel and Umbriel, and Titan not Titania. |
| 24 | The Challenger accident occurred on January 28, 1986. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source states the Challenger accident occurred Feb. 28, 1986, not January 28, 1986. |
| 25 | Seven astronauts were killed during the Challenger space shuttle launch. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- Source states six astronauts were killed, not seven. |
| 21 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons. | supported in part | `source_b.md` | "Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons" in `source_b.md`, **transcription_error** -- Source confirms these are five of Uranus' smaller moons, but the moon names in the claim differ from those in the source. |
| 2 | Mission planners directed Voyager 2 to Uranus. | supported | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- Source states mission planners directed the spacecraft (Voyager 2 from context) to Uranus. |
| 3 | The journey to Uranus would take about 4.5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Source states the journey to Uranus would take about 4,5 years, which equals 4.5 years. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- Source states Jupiter encounter was optimized to ensure future planetary flybys would be possible. |
| 5 | Voyager 1 had 6.4 days of close study during its flyby of Uranus. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- Source states Voyager 1 had only 6.4 days of close study during its flyby of Uranus. |
| 8 | Signals from Voyager 2 took approximately 2.5 hours to reach Earth. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Source states signals from Voyager took approximately 2,5 hours to reach Earth. |
| 9 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- Source states light conditions were five-hundred times less than terrestrial conditions. |
| 11 | The closest approach to Uranus occurred at a range of about 50,640 kilometers (81,500 miles). | supported | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Source states closest approach occurred at a range of about 50,640 kilometers (81,500 miles). |
| 12 | Voyager 2 discovered 11 new moons during its flyby of Uranus. | supported | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Source states Voyager 2 discovered 11 new moons during its flyby of Uranus. |
| 14 | A naming tradition using Shakespeare allusions began in 1687. | supported | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- Source states a naming tradition was begun in 1687. |
| 15 | Voyager 2 discovered three new rings in addition to the eight previously known rings of Uranus. | supported | `source_b.md` | 'three new rings in addition to the "older" eight rings' in `source_b.md`, **transcription_error** -- Source states Voyager 2 discovered three new rings in addition to the eight previously known rings. |
| 16 | Uranus has a magnetic field tilted at 66 degrees off-axis and off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Source states Uranus has a magnetic field tilted at 66 degrees off-axis and off-center. |
| 17 | Wind speeds in Uranus' atmosphere were as high as 450 km/h. | supported | `source_b.md` | "wind speeds in Uranus' atmosphere as high as 450 km/h" in `source_b.md`, **transcription_error** -- Source states wind speeds in Uranus' atmosphere were found to be as high as 450 km/h. |
| 18 | Evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface was found on Uranus. | supported | `source_b.md` | 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Source states evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface was found. |
| 19 | The rings of Uranus were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- Source states the rings of Uranus were found to be extremely variable in thickness and transparency. |
| 22 | Voyager 2 flew by Miranda at a range of only 17,560 miles (28,260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Source states Voyager 2 flew by Miranda at a range of only 17,560 miles (28,260 kilometers). |
| 23 | Voyager 2 came closest to Miranda at any object during its nearly century-long travels. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Source states the spacecraft came closest to Miranda of any object during its nearly century-long travels. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **25** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **25**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

`[-...-]` is what the source said and `{+...+}` is what the merge says.

### Reworded and undeclared — in the merge in altered wording, and no record explains it. At off this also covers layout: a segment whose source line breaks the merge ran together is altered and undeclared, and 380 reuses this kind rather than moving FINDING_KINDS off 12

- `a4` (`source_a.md`) — 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.' is reworded in the merge and no disposition record explains it (nearest merge segment m4 at 0.99)

  ```text
  In the source: The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.
  In the merge:  The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.
  What changed:  The Ur[- -]anus encounter[-’-]{+'+}s geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby.
  ```
- `b6` (`source_b.md`) — 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.' is reworded in the merge and no disposition record explains it (nearest merge segment m13 at 0.99)

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  What changed:  In flying by Miranda at a range of only 17[-.-]{+,+}560 miles (28[-.-]{+,+}260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  ```

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a6` (`source_a.md`) — 'Light conditions were five-hundred times less than terrestrial conditions.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Light conditions were five-hundred times less than terrestrial conditions.
  In the merge:  Light conditions were five-hundred times less than terrestrial conditions.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a2` (`source_a.md`) — numeric '4,5' (years) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '2,5' (hours) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '17.560' (miles) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '28.260' (kilometers) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **8** departure(s) from its sources. Checking them confirms 3, rejects 5, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Duration corrected from 4,5 to 4.5 years (decimal notation). | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a5` | reconciled | Reconciled spacecraft name correction and date clarification from b9. | **confirmed** | declared 'reconciled' and every claim from it came back SUPPORTED or CONTRADICTED (`A-005`, `A-006`, `A-007`) |
| `a6` | subsumed | Retained within broader observational context. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-008`) |
| `a7` | reworded | Date corrected from 1968 to 1986; ED changed to EST; Jan. expanded to January. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-009 came back CONTRADICTED (`A-009`) |
| `b2` | reworded | Proper names corrected to accurate Shakespearean character spellings. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-002 came back CONTRADICTED (`B-002`) |
| `b3` | reworded | Removed inconsistent unit conversion (72400 meters per hour) as it doesn't match | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-006`) |
| `b5` | reworded | Moon names corrected to accurate spellings (Ariele→Ariel, Umbrella→Umbriel, Tita | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED (`B-008`) |
| `b9` | reworded | Date corrected from Feb. 28, 1986 to January 28, 1986; death toll corrected to s | **rejected** | declared 'reworded', which predicts SUPPORTED; B-014 came back CONTRADICTED, B-015 came back CONTRADICTED (`B-014`, `B-015`) |

## Added from outside the documents

The merge declared 6 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

6 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Voyager 2 became the first human-made object to fly past Uranus. Short-range observations of the planet began on January 24, 1986, when signals took approximately 2.5 hours to reach Earth. | The first human-made object to fly past Uranus, Voyager 1's short-range observations | the model's own knowledge | *no source* | Segment a5 incorrectly names Voyager 1; context and b sections confirm Voyager 2 | *none* |
| Closest approach to Uranus took place at 17:59 EST on January 24, 1986, at a range of about 50,640 kilometers (81,500 miles). | 17:59 ED Jan. 24, 1968 | the model's own knowledge | *no source* | Voyager 2's Uranus encounter was January 1986, not 1968; ED standardized to EST. | *none* |
| During its flyby, Voyager 2 discovered 11 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca—obvious allusions to Shakespeare, continuing a naming tradition begun in 1687) | Pucka, Portila, Juliette, Kressida, Rosalinde, Cordelina, Bianca II – obvious allusions to Goethe | the model's own knowledge | *no source* | Uranus moons follow Shakespeare tradition; spellings correct to official nomencl | *none* |
| The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h | 450 km/h (72400 meters per hour) | the model's own knowledge | *no source* | 450 km/h equals 125 m/s or ~450,000 m/h, not 72,400 m/h; removed erroneous conve | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' smaller moons. | Miranda, Oberon, Ariele, Umbrella, and Titan | the model's own knowledge | *no source* | Correct spellings are Ariel, Umbriel, Titania; Titan orbits Saturn, not Uranus. | *none* |
| The tragic Challenger accident that killed seven astronauts during their space shuttle launch on January 28, 1986. | killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger launched January 28, 1986 with seven crew members; six perished with | *none* |

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
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | 18,587 in, 10,853 out |
| Cost | ~$0.07 estimated (rates read 2026-08-31) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 75.8s |
| Generated | 2026-09-27T19:44:17+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
