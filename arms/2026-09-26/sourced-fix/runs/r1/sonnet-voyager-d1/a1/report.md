## Verdict

**33 finding(s).** In the claims: 1 partially dropped, 22 contradicted, 3 partially invented. In the structure: 7 verbatim violation. **The model retrieved.** This run was made at fidelity sourced, and 1 of the 1 merge call(s) that reported a turn count took the turns a retrieval costs. Which statement a retrieval backs is not recorded, and each is still the model's. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 24 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 15 |
| Forward — source claims accounted for in the merge | **13/27** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **5/12** |
| Forward — `source_b.md` claims accounted for | **8/15** (1 in part) |
| Reverse — merge claims found in a source | **12/24** |
| Reverse — supported only in part | 3 |
| Evidence grounded | **51/51** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-013** (`source_b.md:9`) — The Challenger accident interrupted the news of the Uranus encounter on the same day.
  - evidence: 'The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: Text says the same week, not the same day.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says Neptune, not Saturn.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby.
  - `merged.md` says: 'Voyager 2 had only 5.5 hours of close study during its flyby.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says Voyager 2 and 5.5 hours, not Voyager 1 and 6.4 days.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: "The first human-made object to fly past Uranus, Voyager 2's short-range observations" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Voyager 2, not Voyager 1, was first.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: "Voyager 2's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text attributes the observations to Voyager 2, not Voyager 1.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text gives year 1986, not 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 50,640 miles (81,500 kilometers)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Units are swapped.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: During its flyby, Voyager 2 discovered 11 new moons.
  - `merged.md` says: 'discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says 10, not 11.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings in addition to the "older" eight rings.
  - `merged.md` says: 'two new rings in addition to the “older” nine rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says two new and nine older rings.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center.
  - `merged.md` says: 'a magnetic field tilted at 55 degrees off-axis and off-center' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says 55 degrees, not 66.
- **B-008** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons.
  - `merged.md` says: 'Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Names differ: Ariel, Umbriel, Titania, not Ariele, Umbrella, Titan.
- **B-014** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says seven, not six.
- **B-015** -- the two documents disagree
  - `source_b.md:9` says: The Challenger space shuttle launch was on Feb. 28, 1986.
  - `merged.md` says: 'space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Launch was Jan. 28, not Feb. 28.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with the three planetary encounters before being directed to Uranus.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says Voyager 3, not Voyager 2, though the title says Voyager 2; the source names a different spacecraft.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says Saturn, not Neptune.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had only 5.5 hours of close study during its Uranus flyby.
  - `source_a.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives 6.4 days, not 5.5 hours.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says 1968, not 1986.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus was at a range of about 50,640 miles (81,500 kilometers).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Units are swapped relative to the source.
- **M-012** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered 10 new moons during its Uranus flyby.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says 11, not 10.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered two new rings in addition to the "older" nine rings.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says three new and eight older rings.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered a magnetic field tilted at 55 degrees off-axis and off-center.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says 66 degrees, not 55.
- **M-023** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident killed seven astronauts during their space shuttle launch Jan. 28, 1986.
  - `source_b.md` says: 'killed six astronauts during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source says six astronauts and Feb. 28, not seven and Jan. 28.

### Partly invented — the sources carry some of this claim

- **M-013** (`merged.md:7`) — The naming tradition of Shakespeare allusions for Uranus moons was begun in 1687.
  - evidence: 'continuing a naming tradition begun in 1687' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The 1687 date is supported, but the source alludes to Goethe, not Shakespeare.
- **M-019** (`merged.md:11`) — Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons, and Voyager 2 returned photos of them.
  - evidence: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source names Ariele, Umbrella and Titan, not Ariel, Umbriel and Titania.
- **M-024** (`merged.md:13`) — The Challenger accident interrupted the news of the Uranus encounter the same week.
  - evidence: 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Source says the same day, not the same week.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 5.5 | 4,5, 2,5 | English (72 / 0) |

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
| 5 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune' in `merged.md` -- Text says Neptune, not Saturn. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | contradicted | 'Voyager 2 had only 5.5 hours of close study during its flyby.' in `merged.md` -- Text says Voyager 2 and 5.5 hours, not Voyager 1 and 6.4 days. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | "The first human-made object to fly past Uranus, Voyager 2's short-range observations" in `merged.md` -- Voyager 2, not Voyager 1, was first. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | "Voyager 2's short-range observations of the planet began Jan. 31, 1987" in `merged.md` -- Text attributes the observations to Voyager 2, not Voyager 1. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' in `merged.md` -- Text gives year 1986, not 1968. |
| 12 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 50,640 miles (81,500 kilometers)' in `merged.md` -- Units are swapped. |
| 2 | Mission planners directed the spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Stated directly. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Stated directly. |
| 4 | Voyager's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Stated directly. |
| 9 | Signals took approximately 2,5 hours to reach Earth when the short-range observations began. | 9 | carried | 'when signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Stated directly. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions.' in `merged.md` -- Stated directly. |

### `source_b.md` -- 15 claim(s): 0 dropped, 6 contradicted, 1 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | During its flyby, Voyager 2 discovered 11 new moons. | 3 | contradicted | 'discovered 10 new moons' in `merged.md` -- Text says 10, not 11. |
| 3 | Voyager 2 discovered three new rings in addition to the "older" eight rings. | 3 | contradicted | 'two new rings in addition to the “older” nine rings' in `merged.md` -- Text says two new and nine older rings. |
| 4 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | contradicted | 'a magnetic field tilted at 55 degrees off-axis and off-center' in `merged.md` -- Text says 55 degrees, not 66. |
| 8 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus' smaller moons. | 7 | contradicted | 'Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- Names differ: Ariel, Umbriel, Titania, not Ariele, Umbrella, Titan. |
| 14 | The Challenger accident killed six astronauts. | 9 | contradicted | 'killed seven astronauts' in `merged.md` -- Text says seven, not six. |
| 15 | The Challenger space shuttle launch was on Feb. 28, 1986. | 9 | contradicted | 'space shuttle launch Jan. 28, 1986' in `merged.md` -- Launch was Jan. 28, not Feb. 28. |
| 13 | The Challenger accident interrupted the news of the Uranus encounter on the same day. | 9 | carried in part | 'The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident' in `merged.md` -- Text says the same week, not the same day. |
| 2 | The naming tradition for Uranus's moons was begun in 1687. | 3 | carried | 'continuing a naming tradition begun in 1687' in `merged.md` -- Stated directly. |
| 5 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | 5 | carried | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `merged.md` -- Stated directly. |
| 6 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | carried | 'evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- Stated directly. |
| 7 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- Stated directly. |
| 9 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- Stated directly. |
| 10 | Miranda was the closest object the spacecraft had come to so far in its travels. | 7 | carried | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `merged.md` -- Closest approach to any object was at Miranda. |
| 11 | Voyager 2's travels were nearly century-long. | 7 | carried | 'its nearly century-long travels' in `merged.md` -- Stated directly. |
| 12 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- Stated directly. |

### `merged.md` -- 24 claim(s): 0 invented, 9 contradicted, 3 supported in part, 12 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with the three planetary encounters before being directed to Uranus. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source says Voyager 3, not Voyager 2, though the title says Voyager 2; the source names a different spacecraft. |
| 4 | The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- Source says Saturn, not Neptune. |
| 5 | Voyager 2 had only 5.5 hours of close study during its Uranus flyby. | contradicted | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- Source gives 6.4 days, not 5.5 hours. |
| 10 | Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source says 1968, not 1986. |
| 11 | Closest approach to Uranus was at a range of about 50,640 miles (81,500 kilometers). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Units are swapped relative to the source. |
| 12 | Voyager 2 discovered 10 new moons during its Uranus flyby. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Source says 11, not 10. |
| 14 | Voyager 2 discovered two new rings in addition to the "older" nine rings. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Source says three new and eight older rings. |
| 15 | Voyager 2 discovered a magnetic field tilted at 55 degrees off-axis and off-center. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Source says 66 degrees, not 55. |
| 23 | The Challenger accident killed seven astronauts during their space shuttle launch Jan. 28, 1986. | contradicted | `source_b.md` | 'killed six astronauts during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source says six astronauts and Feb. 28, not seven and Jan. 28. |
| 13 | The naming tradition of Shakespeare allusions for Uranus moons was begun in 1687. | supported in part | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- The 1687 date is supported, but the source alludes to Goethe, not Shakespeare. |
| 19 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' smaller moons, and Voyager 2 returned photos of them. | supported in part | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- Source names Ariele, Umbrella and Titan, not Ariel, Umbriel and Titania. |
| 24 | The Challenger accident interrupted the news of the Uranus encounter the same week. | supported in part | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- Source says the same day, not the same week. |
| 2 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Source states the same duration. |
| 3 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- Stated directly, with the spacecraft being the subject of the document. |
| 6 | Voyager 2 was the first human-made object to fly past Uranus. | supported | `source_a.md` | 'The first human-made object to fly past Uranus' in `source_a.md` -- Source states this, attributing it to Voyager 1 in text but the document is about Voyager 2. |
| 7 | Voyager 2's short-range observations of Uranus began Jan. 31, 1987. | supported | `source_a.md` | 'short-range observations of the planet began Jan. 31, 1987' in `source_a.md` -- Date matches the source. |
| 8 | Signals took approximately 2,5 hours to reach Earth when the observations began. | supported | `source_a.md` | 'when signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Matches the source. |
| 9 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- Matches the source. |
| 16 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 km/h (72400 meters per hour). | supported | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- Matches the source. |
| 17 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | supported | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Matches the source. |
| 18 | Uranus' rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- Matches the source. |
| 20 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Matches the source. |
| 21 | The Miranda flyby was the closest Voyager 2 had come to any object so far in its travels. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Same meaning. |
| 22 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- Matches the source. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **24** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **27**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '1' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '6.4' (days) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1' does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '66' (degrees) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **8** departure(s) from its sources. Checking them confirms 1, rejects 7, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | duplicate | Identical to the base title. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a2` | reworded | Spacecraft name corrected to Voyager 2. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Typo fixed; planet, spacecraft and duration corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED (`A-005`, `A-006`) |
| `a5` | reworded | Spacecraft name corrected to Voyager 2. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a7` | reworded | Time zone, year and swapped distance units corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b2` | reworded | Moon count, names, rings and tilt corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED (`B-001`, `B-003`, `B-004`) |
| `b5` | reworded | Moon names corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED (`B-008`) |
| `b9` | reworded | Timing, crew count and date corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-013 came back PARTIAL, B-014 came back CONTRADICTED, B-015 came back CONTRADICTED (`B-013`, `B-014`, `B-015`) |

## Added from outside the documents

The merge declared 7 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. The model took more turns on 1 call(s) than a call that retrieves nothing can take, so it used a tool it was granted at least that often. It is a count of turns rather than of fetches, and which statement a retrieval belongs to is not recorded. The endpoint's own web-request counter reported none, which on this backend means it could not see one rather than that none was made: it counts a vendor's server-side tools and a command-line tool runs in the model's own process.

7 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the three planetary encounters | Although Voyager 3 had fulfilled its primary mission goals | cited | NASA Science, Voyager 2 mission page (science.nasa.gov/mission/voyager/voyager-2/) | Page and title identify the Uranus flyby craft as Voyager 2. | *none* |
| The Uranus encounter’s geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 5.5 hours of close study during its flyby. | possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study | cited | NASA Science, Voyager 2 mission page (science.nasa.gov/mission/voyager/voyager-2/) | Page states Neptune and 5.5 hours for Voyager 2. | *none* |
| The first human-made object to fly past Uranus, Voyager 2's short-range observations | Voyager 1's short-range observations | cited | NASA Science, Voyager 2 mission page (science.nasa.gov/mission/voyager/voyager-2/) | Voyager 2 alone flew past Uranus. | *none* |
| Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers). | 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | cited | NASA Science, Voyager 2 mission page (science.nasa.gov/mission/voyager/voyager-2/) | Page gives 17:59 UT, 1986, 50,640 miles (81,500 km). | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1687), two new rings in addition to the “older” nine rings, and a magnetic field tilted at 55 degrees off-axis and off-center. | 11 new moons; Pucka, Portila, Juliette, Kressida, Rosalinde, Cordelina, Bianca II; Goethe; three new rings; eight rings; 66 degrees | cited | NASA Science, Voyager 2 mission page (science.nasa.gov/mission/voyager/voyager-2/) | Page gives 10 moons, names, two new and nine older rings, 55 degrees. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons. | Miranda, Oberon, Ariele, Umbrella, and Titan | cited | Search results on Voyager 2 imaging of Miranda, Ariel, Umbriel, Titania and Oberon (JPL/NASA summaries) | Search results name these five moons. | *none* |
| The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986 | cited | Web search results: NASA Challenger STS-51-L page, Britannica (28 Jan 1986, seven crew) | Sources give Jan. 28, 1986, seven crew, four days after encounter. | *none* |

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
| Calls | 7 live, 0 cached, 0 replayed |
| Tokens | unknown (7 call(s) reported no usage) |
| Cost | unmeasured (7 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 1 |
| Retrieval | WebSearch, WebFetch permitted; 1 of 7 call(s) used a tool (13 turn(s) in total) |
| Isolation | decompose, merge, verify: safe mode, tools WebSearch, WebFetch |
| Errors | 0 |
| Duration | 165.9s |
| Generated | 2026-09-26T17:55:10+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `831fa897e6f5` |
| Prompt | `prompts/verify.md` `55a721b20905` |
| Prompt | `prompts/verify_reverse.md` `2a6d7e955709` |

> **Document content was handed to a program on this machine (`Claude Code - Sonnet`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The model was permitted to reach the network** (WebSearch, WebFetch), so a query or a fetch it made may have carried text from these documents to a third party. 1 of 7 call(s) used a tool (13 turn(s) in total), counted in turns rather than in fetches. LLossless itself made no network request of any kind and resolved none of the sources the merge names.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
