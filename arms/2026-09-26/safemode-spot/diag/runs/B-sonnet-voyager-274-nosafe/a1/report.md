## Verdict

**50 finding(s).** In the claims: 41 contradicted. In the structure: 9 verbatim violation. **The model retrieved.** This run was made at fidelity sourced, and 5 of the 6 call(s) that reported a turn count took the turns a retrieval costs. Which statement a retrieval backs is not recorded, and each is still the model's. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 29 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 21 |
| Forward — source claims accounted for in the merge | **12/33** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **4/12** |
| Forward — `source_b.md` claims accounted for | **8/21** |
| Reverse — merge claims found in a source | **9/29** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **62/62** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 2's primary mission goals included three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with two planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states two planetary encounters, not three.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was defined in part by the possibility of a future encounter with Saturn.
  - `merged.md` says: "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text names Neptune, not Saturn, as the future encounter.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its Uranus flyby.
  - `merged.md` says: 'Voyager 2 had only 5.5 hours of close study during its flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes 5.5 hours to Voyager 2, not 6.4 days to Voyager 1.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: "The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text identifies Voyager 2, not Voyager 1, as the first object to fly past Uranus.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: "Voyager 2's short-range observations of the planet began Jan. 31, 1986" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Voyager 2 in 1986, not Voyager 1 in 1987.
- **A-010** -- the two documents disagree
  - `source_a.md:9` says: Light conditions at Uranus were five-hundred times less than terrestrial conditions.
  - `merged.md` says: 'Light conditions were about 400 times less than terrestrial conditions' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 400 times less, not five-hundred times less.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives UT (not ED) and the year 1986, not 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'a range of about 81,500 kilometers (50,640 miles)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim reverses the units; the text states 81,500 km (50,640 miles), not 50,640 km (81,500 miles).
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The new moons were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim's moon name spellings differ from those stated in the text.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The moon names are allusions to Goethe.
  - `merged.md` says: 'obvious allusions to Shakespeare and Alexander Pope' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes the names to Shakespeare and Pope, not Goethe.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for Uranus' moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1787' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 1787, not 1687.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings at Uranus in addition to the older eight rings.
  - `merged.md` says: 'two new rings in addition to the “older” nine rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states two new rings and nine older rings, not three new and eight older.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered a magnetic field at Uranus tilted at 66 degrees off-axis and off-center.
  - `merged.md` says: 'a magnetic field tilted at 59 degrees off-axis and off-center' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states 59 degrees, not 66 degrees.
- **B-007** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h.
  - `merged.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: 450 is given in miles per hour, not km/h, per the text.
- **B-008** -- the two documents disagree
  - `source_b.md:5` says: 450 km/h is equivalent to 72400 meters per hour as stated in the document.
  - `merged.md` says: '450 miles per hour (724 kilometers per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text equates 450 mph to 724 kilometers per hour, not 72400 meters per hour.
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text names Ariel, Umbriel, and Titania, not Ariele, Umbrella, and Titan.
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are described as five of Uranus' smaller moons.
  - `merged.md` says: 'five of Uranus’ smaller moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: While the count and description match, the claim pairs this with the incorrect moon names from the text, which is contradicted.
- **B-016** -- the two documents disagree
  - `source_b.md:7` says: The Miranda flyby was the closest Voyager 2 came to any object so far in its nearly century-long travels.
  - `merged.md` says: 'the spacecraft came closest to any object so far in its nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states nearly decade-long travels, not century-long.
- **B-019** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'the tragic Challenger accident that killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states seven astronauts, not six.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states Jan. 28, 1986, not Feb. 28, 1986.
- **B-021** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident interrupted the spectacular news of the Uranus encounter on the same day.
  - `merged.md` says: 'The spectacular news of the Uranus encounter was overshadowed four days later by the tragic Challenger accident' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text states the accident occurred four days later, not on the same day.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with two planetary encounters.
  - `source_a.md` says: 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Voyager 3 with three encounters, not Voyager 2 with two.
- **M-004** -- the two documents disagree
  - `merged.md:5` says: The Uranus encounter's geometry was defined in part by the possibility of a future encounter with Neptune.
  - `source_a.md` says: 'defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states Saturn, not Neptune, as the future encounter possibility.
- **M-005** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 had only 5.5 hours of close study during its Uranus flyby.
  - `source_a.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives 6.4 days for Voyager 1, not 5.5 hours for Voyager 2.
- **M-006** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source explicitly names Voyager 1, not Voyager 2, as first past Uranus.
- **M-007** -- the two documents disagree
  - `merged.md:7` says: Voyager 2's short-range observations of Uranus began Jan. 31, 1986.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Voyager 1 and date 1987, not Voyager 2 and 1986.
- **M-009** -- the two documents disagree
  - `merged.md:7` says: Light conditions at Uranus were about 400 times less than terrestrial conditions.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states five hundred times, not about 400 times.
- **M-010** -- the two documents disagree
  - `merged.md:7` says: Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives 1968 and ED, not 1986 and UT.
- **M-011** -- the two documents disagree
  - `merged.md:7` says: Closest approach to Uranus took place at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Claim swaps the km and miles values relative to the source.
- **M-013** -- the two documents disagree
  - `merged.md:9` says: The 11 new moons were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Several names differ in spelling/form from the claim's list (e.g. Pucka vs Puck, Bianca II vs Bianca).
- **M-014** -- the two documents disagree
  - `merged.md:9` says: The moon names are obvious allusions to Shakespeare and Alexander Pope.
  - `source_b.md` says: 'obvious allusions to Goethe' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes the naming allusion to Goethe, not Shakespeare and Alexander Pope.
- **M-015** -- the two documents disagree
  - `merged.md:9` says: The naming tradition for Uranus's moons was begun in 1787.
  - `source_b.md` says: 'a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 1687, not 1787.
- **M-016** -- the two documents disagree
  - `merged.md:9` says: During its flyby, Voyager 2 discovered two new rings in addition to the older nine rings.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states three new rings and eight older rings, not two and nine.
- **M-017** -- the two documents disagree
  - `merged.md:9` says: During its flyby, Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis and off-center.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 66 degrees, not 59 degrees.
- **M-018** -- the two documents disagree
  - `merged.md:11` says: The spacecraft found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour).
  - `source_b.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives 450 km/h, not 450 mph, and a different secondary unit conversion.
- **M-021** -- the two documents disagree
  - `merged.md:13` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names differ from the claim's Ariel, Umbriel, and Titania.
- **M-022** -- the two documents disagree
  - `merged.md:13` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus's smaller moons.
  - `source_b.md` says: 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source's moon names differ from those in the claim.
- **M-024** -- the two documents disagree
  - `merged.md:13` says: The Miranda flyby was the closest the spacecraft came to any object so far in its nearly decade-long travels.
  - `source_b.md` says: 'in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states nearly century-long, not decade-long.
- **M-027** -- the two documents disagree
  - `merged.md:15` says: The news of the Uranus encounter was overshadowed four days later by the Challenger accident.
  - `source_b.md` says: 'was interrupted the same day by the tragic Challenger accident' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states the news was interrupted the same day, not four days later.
- **M-028** -- the two documents disagree
  - `merged.md:15` says: The Challenger accident killed seven astronauts during their space shuttle launch.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states six astronauts died, not seven.
- **M-029** -- the two documents disagree
  - `merged.md:15` says: The Challenger space shuttle launch took place Jan. 28, 1986.
  - `source_b.md` says: 'during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source gives Feb. 28, 1986, not Jan. 28, 1986.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 5.5 | 4,5, 2,5 | English (71 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m5` (`merged.md`) - '2,5' (merged.md, line 7) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `m12` (`merged.md`) - '17.560' (merged.md, line 13) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m12` (`merged.md`) - '28.260' (merged.md, line 13) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 8 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 2's primary mission goals included three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with two planetary encounters' in `merged.md` -- The text states two planetary encounters, not three. |
| 5 | The Uranus encounter's geometry was defined in part by the possibility of a future encounter with Saturn. | 7 | contradicted | "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune" in `merged.md` -- Text names Neptune, not Saturn, as the future encounter. |
| 6 | Voyager 1 had only 6.4 days of close study during its Uranus flyby. | 7 | contradicted | 'Voyager 2 had only 5.5 hours of close study during its flyby' in `merged.md` -- The text attributes 5.5 hours to Voyager 2, not 6.4 days to Voyager 1. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | "The first human-made object to fly past Uranus, Voyager 2's short-range observations of the planet began Jan. 31, 1986" in `merged.md` -- The text identifies Voyager 2, not Voyager 1, as the first object to fly past Uranus. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | "Voyager 2's short-range observations of the planet began Jan. 31, 1986" in `merged.md` -- The text says Voyager 2 in 1986, not Voyager 1 in 1987. |
| 10 | Light conditions at Uranus were five-hundred times less than terrestrial conditions. | 9 | contradicted | 'Light conditions were about 400 times less than terrestrial conditions' in `merged.md` -- The text states 400 times less, not five-hundred times less. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' in `merged.md` -- The text gives UT (not ED) and the year 1986, not 1968. |
| 12 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'a range of about 81,500 kilometers (50,640 miles)' in `merged.md` -- The claim reverses the units; the text states 81,500 km (50,640 miles), not 50,640 km (81,500 miles). |
| 2 | Mission planners directed the spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly stated. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Matches exactly. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Directly stated. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals took approximately 2,5 hours to reach Earth' in `merged.md` -- Directly stated. |

### `source_b.md` -- 21 claim(s): 0 dropped, 13 contradicted, 0 carried in part, 8 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | The new moons were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The claim's moon name spellings differ from those stated in the text. |
| 3 | The moon names are allusions to Goethe. | 3 | contradicted | 'obvious allusions to Shakespeare and Alexander Pope' in `merged.md` -- The text attributes the names to Shakespeare and Pope, not Goethe. |
| 4 | The naming tradition for Uranus' moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1787' in `merged.md` -- The text states 1787, not 1687. |
| 5 | Voyager 2 discovered three new rings at Uranus in addition to the older eight rings. | 3 | contradicted | 'two new rings in addition to the “older” nine rings' in `merged.md` -- The text states two new rings and nine older rings, not three new and eight older. |
| 6 | Voyager 2 discovered a magnetic field at Uranus tilted at 66 degrees off-axis and off-center. | 3 | contradicted | 'a magnetic field tilted at 59 degrees off-axis and off-center' in `merged.md` -- The text states 59 degrees, not 66 degrees. |
| 7 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h. | 5 | contradicted | 'wind speeds in Uranus’ atmosphere as high as 450 miles per hour (724 kilometers per hour)' in `merged.md` -- 450 is given in miles per hour, not km/h, per the text. |
| 8 | 450 km/h is equivalent to 72400 meters per hour as stated in the document. | 5 | contradicted | '450 miles per hour (724 kilometers per hour)' in `merged.md` -- The text equates 450 mph to 724 kilometers per hour, not 72400 meters per hour. |
| 12 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The text names Ariel, Umbriel, and Titania, not Ariele, Umbrella, and Titan. |
| 13 | Miranda, Oberon, Ariele, Umbrella, and Titan are described as five of Uranus' smaller moons. | 7 | contradicted | 'five of Uranus’ smaller moons' in `merged.md` -- While the count and description match, the claim pairs this with the incorrect moon names from the text, which is contradicted. |
| 16 | The Miranda flyby was the closest Voyager 2 came to any object so far in its nearly century-long travels. | 7 | contradicted | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- The text states nearly decade-long travels, not century-long. |
| 19 | The Challenger accident killed six astronauts. | 9 | contradicted | 'the tragic Challenger accident that killed seven astronauts' in `merged.md` -- The text states seven astronauts, not six. |
| 20 | The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- The text states Jan. 28, 1986, not Feb. 28, 1986. |
| 21 | The Challenger accident interrupted the spectacular news of the Uranus encounter on the same day. | 9 | contradicted | 'The spectacular news of the Uranus encounter was overshadowed four days later by the tragic Challenger accident' in `merged.md` -- The text states the accident occurred four days later, not on the same day. |
| 1 | Voyager 2 discovered 11 new moons during its flyby. | 3 | carried | 'Voyager 2 discovered 11 new moons' in `merged.md` -- Directly stated. |
| 9 | Voyager 2 found evidence of a boiling lake of water some 479 miles below the top cloud surface of Uranus. | 5 | carried | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `merged.md` -- Directly stated. |
| 10 | 479 miles is equivalent to 900 kilometers as stated in the document. | 5 | carried | '479 miles (900 kilometers)' in `merged.md` -- Matches the conversion given in the text. |
| 11 | Uranus' rings were found to be extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- Directly stated. |
| 14 | Voyager 2 flew by Miranda at a range of only 17.560 miles. | 7 | carried | 'flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `merged.md` -- Directly stated. |
| 15 | 17.560 miles is equivalent to 28.260 kilometers as stated in the document. | 7 | carried | '17.560 miles (28.260 kilometers)' in `merged.md` -- Matches the conversion given in the text. |
| 17 | Images of Miranda showed a surface that was a mishmash of peculiar features that seemed to have no rhyme or reason. | 7 | carried | 'a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason' in `merged.md` -- Directly stated. |
| 18 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless' in `merged.md` -- Directly stated. |

### `merged.md` -- 29 claim(s): 0 invented, 20 contradicted, 0 supported in part, 9 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 had fulfilled its primary mission goals with two planetary encounters. | contradicted | `source_a.md` | 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source names Voyager 3 with three encounters, not Voyager 2 with two. |
| 4 | The Uranus encounter's geometry was defined in part by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | 'defined by the possibility of a future encounter with Saturn' in `source_a.md` -- Source states Saturn, not Neptune, as the future encounter possibility. |
| 5 | Voyager 2 had only 5.5 hours of close study during its Uranus flyby. | contradicted | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- Source gives 6.4 days for Voyager 1, not 5.5 hours for Voyager 2. |
| 6 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source explicitly names Voyager 1, not Voyager 2, as first past Uranus. |
| 7 | Voyager 2's short-range observations of Uranus began Jan. 31, 1986. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source names Voyager 1 and date 1987, not Voyager 2 and 1986. |
| 9 | Light conditions at Uranus were about 400 times less than terrestrial conditions. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- Source states five hundred times, not about 400 times. |
| 10 | Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source gives 1968 and ED, not 1986 and UT. |
| 11 | Closest approach to Uranus took place at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Claim swaps the km and miles values relative to the source. |
| 13 | The 11 new moons were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- Several names differ in spelling/form from the claim's list (e.g. Pucka vs Puck, Bianca II vs Bianca). |
| 14 | The moon names are obvious allusions to Shakespeare and Alexander Pope. | contradicted | `source_b.md` | 'obvious allusions to Goethe' in `source_b.md` -- Source attributes the naming allusion to Goethe, not Shakespeare and Alexander Pope. |
| 15 | The naming tradition for Uranus's moons was begun in 1787. | contradicted | `source_b.md` | 'a naming tradition begun in 1687' in `source_b.md` -- Source states 1687, not 1787. |
| 16 | During its flyby, Voyager 2 discovered two new rings in addition to the older nine rings. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Source states three new rings and eight older rings, not two and nine. |
| 17 | During its flyby, Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis and off-center. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Source states 66 degrees, not 59 degrees. |
| 18 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour). | contradicted | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- Source gives 450 km/h, not 450 mph, and a different secondary unit conversion. |
| 21 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- Source names differ from the claim's Ariel, Umbriel, and Titania. |
| 22 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus's smaller moons. | contradicted | `source_b.md` | 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' in `source_b.md` -- Source's moon names differ from those in the claim. |
| 24 | The Miranda flyby was the closest the spacecraft came to any object so far in its nearly decade-long travels. | contradicted | `source_b.md` | 'in its nearly century-long travels' in `source_b.md` -- Source states nearly century-long, not decade-long. |
| 27 | The news of the Uranus encounter was overshadowed four days later by the Challenger accident. | contradicted | `source_b.md` | 'was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- Source states the news was interrupted the same day, not four days later. |
| 28 | The Challenger accident killed seven astronauts during their space shuttle launch. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- Source states six astronauts died, not seven. |
| 29 | The Challenger space shuttle launch took place Jan. 28, 1986. | contradicted | `source_b.md` | 'during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source gives Feb. 28, 1986, not Jan. 28, 1986. |
| 2 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Matches the stated travel time exactly. |
| 3 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | supported | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- The pronoun refers to the spacecraft discussed in the Voyager 2 at Uranus document, matching the claim. |
| 8 | Signals took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Matches exactly. |
| 12 | During its flyby, Voyager 2 discovered 11 new moons. | supported | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Matches exactly. |
| 19 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | supported | `source_b.md` | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Matches exactly. |
| 20 | Uranus's rings were found to be extremely variable in thickness and transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- Matches exactly. |
| 23 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Matches exactly. |
| 25 | Images of Miranda showed a surface that was a mishmash of peculiar features that seemed to have no rhyme or reason. | supported | `source_b.md` | 'a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason' in `source_b.md` -- Matches exactly. |
| 26 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless' in `source_b.md` -- Matches exactly. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **29** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **33**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 13 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '1' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '6.4' (days) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '66' (degrees) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **11** departure(s) from its sources. Checking them confirms 0, rejects 10, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Fixes spacecraft name and prior encounter count. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Fixes planet, spacecraft, and duration errors. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED (`A-005`, `A-006`) |
| `a5` | reworded | Fixes spacecraft name and flyby year. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a6` | reworded | Corrects light-level ratio to about 400 times. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-010 came back CONTRADICTED (`A-010`) |
| `a7` | reworded | Fixes year, time-zone label, and swapped km/mile figures. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | superseded | Base document's title kept; duplicate title superseded. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Fixes moon names, ring/moon counts, allusion, and tilt. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED (`B-002`, `B-003`, `B-004`, `B-005`, `B-006`) |
| `b3` | reworded | Fixes swapped and miscalculated wind-speed units. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-007 came back CONTRADICTED, B-008 came back CONTRADICTED (`B-007`, `B-008`) |
| `b5` | reworded | Fixes misspelled moon names; Titan belongs to Saturn. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back CONTRADICTED, B-013 came back CONTRADICTED (`B-012`, `B-013`) |
| `b6` | reworded | Corrects 'century-long' to 'decade-long' travel time. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-016 came back CONTRADICTED (`B-016`) |
| `b9` | reworded | Fixes timing, crew count, and date of the disaster. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-019 came back CONTRADICTED, B-020 came back CONTRADICTED, B-021 came back CONTRADICTED (`B-019`, `B-020`, `B-021`) |

## Added from outside the documents

The merge declared 22 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. The model took more turns on 5 call(s) than a call that retrieves nothing can take, so it used a tool it was granted at least that often. It is a count of turns rather than of fetches, and which statement a retrieval belongs to is not recorded. The endpoint's own web-request counter reported none, which on this backend means it could not see one rather than that none was made: it counts a vendor's server-side tools and a command-line tool runs in the model's own process.

22 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Voyager 2 | Voyager 3 | cited | science.nasa.gov, Voyager 2 mission overview | No spacecraft named Voyager 3 existed in the program. | *none* |
| two planetary encounters | the three planetary encounters | cited | science.nasa.gov, Planetary Voyage page | Primary mission covered only Jupiter and Saturn before Uranus. | *none* |
| Neptune | Saturn | cited | space.com, '30 Years After Uranus Flyby, Voyager 2 Sails On' | Saturn preceded Uranus; only Neptune was a future encounter. | *none* |
| Voyager 2 | Voyager 1 | the model's own knowledge | *no source* | Voyager 1 never visited Uranus; article concerns Voyager 2. | *none* |
| 5.5 hours | 6.4 days | cited | space.com and earthsky.org coverage of the Uranus flyby | Close-study window at Uranus was 5.5 hours. | *none* |
| Voyager 2's | Voyager 1's | the model's own knowledge | *no source* | Only Voyager 2 ever flew past Uranus. | *none* |
| Jan. 31, 1986 | Jan. 31, 1987 | cited | earthsky.org, 'Voyager 2 met Uranus 40 years ago' | The Uranus flyby occurred in 1986, not 1987. | *none* |
| about 400 times | five-hundred times | cited | solarviews.com, Voyager Uranus Science Summary | Uranus receives about 1/400 of Earth's sunlight. | *none* |
| Jan. 24, 1986 | Jan. 24, 1968 | cited | universetoday.com, NASA/JPL Voyager fact-sheet coverage | Closest approach occurred in 1986, not 1968. | *none* |
| 17:59 UT | 17:59 ED | cited | earthsky.org (9:59 a.m. PST converts to 17:59 UT) | Time is given in Universal Time, not an Eastern zone. | *none* |
| 81,500 kilometers (50,640 miles) | 50,640 kilometers (81,500 miles) | cited | NASA Voyager fact sheet distance figures via universetoday.com | The km and mile figures were swapped. | *none* |
| Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca | Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II | cited | Wikipedia, 'Moons of Uranus' | Corrects garbled spellings of the actual moon names. | *none* |
| Shakespeare and Alexander Pope | Goethe | cited | Folger Shakespeare Library, 'The Shakespearean Moons of Uranus' | Uranus's moons are named for Shakespeare and Pope characters. | *none* |
| 1787 | 1687 | cited | Wikipedia, 'Titania (moon)' | Herschel discovered Titania and Oberon in 1787. | *none* |
| two new rings in addition to the "older" nine rings | three new rings in addition to the "older" eight rings | cited | science.nasa.gov, Voyager 2 mission page | Voyager 2 found two new rings among nine previously known. | *none* |
| 59 degrees | 66 degrees | cited | science.nasa.gov, Voyager 2 mission page | Uranus's magnetic field tilts about 59 degrees from its axis. | *none* |
| 450 miles per hour (724 kilometers per hour) | 450 km/h (72400 meters per hour) | cited | science.nasa.gov, Voyager 2 mission page | Corrects mismatched units; NASA cites 450 mph (724 km/h). | *none* |
| Ariel, Umbriel, and Titania | Ariele, Umbrella, and Titan | the model's own knowledge | *no source* | Titan orbits Saturn; Uranus's large moons include Ariel, Umbriel, Titania. | *none* |
| decade-long | century-long | the model's own knowledge | *no source* | Voyager 2 launched in 1977, about nine years before this flyby. | *none* |
| overshadowed four days later | interrupted the same day | cited | space.com, '30 Years After Uranus Flyby, Voyager 2 Sails On' | The Challenger disaster occurred four days after the flyby. | *none* |
| seven astronauts | six astronauts | the model's own knowledge | *no source* | The Challenger crew numbered seven, not six. | *none* |
| Jan. 28, 1986 | Feb. 28, 1986 | the model's own knowledge | *no source* | The Challenger disaster occurred on January 28, 1986. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 0c160099b569 (command) -- Claude Code - Sonnet |
| Fidelity | sourced |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | sonnet -> claude-sonnet-5 (the answer's output tokens; also named claude-haiku-4-5-20251001) |
| Model (decompose) | sonnet -> claude-sonnet-5 (the answer's output tokens; also named claude-haiku-4-5-20251001) |
| Model (verify) | sonnet -> claude-sonnet-5 (the answer's output tokens; also named claude-haiku-4-5-20251001) |
| Structured output | prompt (probed) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=low, merge=medium, verify=low |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 6cc1b1703658 |
| Calls | 6 live, 0 cached, 0 replayed |
| Tokens | unknown (6 call(s) reported no usage) |
| Cost | unmeasured (6 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Retrieval | WebSearch, WebFetch permitted; 5 of 6 call(s) used a tool (27 turn(s) in total) |
| Isolation | decompose, merge, verify: safe mode, tools WebSearch, WebFetch |
| Errors | 0 |
| Duration | 455.2s |
| Generated | 2026-09-26T16:30:34+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `6d8a835cc983` |
| Prompt | `prompts/verify.md` `55a721b20905` |
| Prompt | `prompts/verify_reverse.md` `2a6d7e955709` |

> **Document content was handed to a program on this machine (`Claude Code - Sonnet`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The model was permitted to reach the network** (WebSearch, WebFetch), so a query or a fetch it made may have carried text from these documents to a third party. 5 of 6 call(s) used a tool (27 turn(s) in total), counted in turns rather than in fetches. LLossless itself made no network request of any kind and resolved none of the sources the merge names.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
