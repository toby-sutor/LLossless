## Verdict

**61 finding(s).** In the claims: 44 contradicted, 1 hallucinated. In the structure: 16 verbatim violation. **The model retrieved.** This run was made at fidelity sourced, and 7 of the 8 call(s) that reported a turn count took the turns a retrieval costs. Which statement a retrieval backs is not recorded, and each is still the model's. 7 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 29 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 22 |
| Forward — source claims accounted for in the merge | **12/34** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **5/12** |
| Forward — `source_b.md` claims accounted for | **7/22** |
| Reverse — merge claims found in a source | **6/29** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **61/62** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with three planetary encounters.
  - `merged.md` says: 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text names Voyager 2 with two encounters, not Voyager 3 with three.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Uranus encounter's geometry was defined in part by the possibility of a future encounter with Saturn.
  - `merged.md` says: "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says Neptune, not Saturn.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby.
  - `merged.md` says: 'Voyager 2 had only 5.5 hours of close study during its flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text refers to Voyager 2 with 5.5 hours, not Voyager 1 with 6.4 days.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: "The first human-made object to fly past Uranus, Voyager 2's long-range observations of the planet began Nov. 4, 1985" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states Voyager 2, not Voyager 1, was first.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: "Voyager 2's long-range observations of the planet began Nov. 4, 1985" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states long-range observations began Nov. 4, 1985 by Voyager 2, not short-range by Voyager 1 on Jan. 31, 1987.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says UT and year 1986, not ED and 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 50,640 miles (81,500 kilometers)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text has miles and kilometers reversed from the claim's units.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby of Uranus.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The new moons discovered were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Names differ from the claim's altered spellings.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The names of the new moons are allusions to Goethe.
  - `merged.md` says: 'obvious allusions to Shakespeare' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says Shakespeare, not Goethe.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: The naming tradition for Uranus' moons began in 1687.
  - `merged.md` says: 'continuing a naming tradition begun in 1787' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says 1787, not 1687.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings at Uranus in addition to the older eight rings.
  - `merged.md` says: 'two new rings in addition to the "older" nine rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says two new rings and nine older rings, not three new and eight older.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 found Uranus' magnetic field tilted at 66 degrees off-axis and off-center.
  - `merged.md` says: 'a magnetic field tilted at 59 degrees off-axis and off-center' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says 59 degrees, not 66 degrees.
- **B-008** -- the two documents disagree
  - `source_b.md:5` says: 450 km/h is equivalent to 72400 meters per hour as stated in the document.
  - `merged.md` says: '724 kilometers per hour' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states 724 km/h, not 72400 meters per hour equivalent claim of 450 km/h converted differently.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found evidence of a boiling lake of water some 479 miles below the top cloud surface of Uranus.
  - `merged.md` says: 'found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says ocean not lake, and 497 miles not 479 miles.
- **B-010** -- the two documents disagree
  - `source_b.md:5` says: The document states the boiling lake of water was some 900 kilometers below the top cloud surface.
  - `merged.md` says: 'some 497 miles (800 kilometers) below the top cloud surface' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states 800 kilometers, not 900 kilometers.
- **B-012** -- the two documents disagree
  - `source_b.md:5` says: Uranus' rings were found to be extremely variable in transparency.
  - `merged.md` says: 'Its rings were found to be extremely variable in thickness and opacity' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says opacity, not transparency, which is the inverse property.
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text lists Ariel, Umbriel, and Titania, not the altered names in the claim.
- **B-014** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are described as five of Uranus' smaller moons.
  - `merged.md` says: "five of Uranus' larger moons" (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says larger moons, not smaller.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: News of the Uranus encounter was interrupted the same day by the Challenger accident.
  - `merged.md` says: 'was interrupted the same week by the tragic Challenger accident' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says same week, not same day.
- **B-021** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'the tragic Challenger accident that killed seven astronauts' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text says seven astronauts, not six.
- **B-022** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'during their space shuttle launch Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Text states Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had fulfilled its primary mission goals with two planetary encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source names Voyager 3 with three encounters, not Voyager 2 with two.
- **M-002** -- the two documents disagree
  - `merged.md:3` says: Mission planners directed Voyager 2 to Uranus.
  - `source_a.md` says: 'mission planners directed the veteran spacecraft to Uranus' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The veteran spacecraft referenced is Voyager 3, not Voyager 2.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: This refers to Voyager 3's Jupiter encounter, not Voyager 2's.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune.
  - `source_a.md` says: "The Ur anus encounter's geometry was also defined by the possibility of a future encounter with Saturn" (transcription_error)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states Saturn, not Neptune.
- **M-006** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 had only 5.5 hours of close study during its Uranus flyby.
  - `source_a.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source attributes 6.4 days to Voyager 1, not 5.5 hours to Voyager 2.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source credits Voyager 1 as first, not Voyager 2.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: Light conditions at Uranus were 400 times less than terrestrial conditions.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 500 times, not 400 times.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states year 1968, not 1986.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Closest approach to Uranus occurred at a range of about 50,640 miles (81,500 kilometers).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Units are swapped in the claim compared to the source.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered 10 new moons.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 11 new moons, not 10.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: The 10 new moons discovered were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - `source_b.md` says: 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The claim's spellings of the moon names differ from those given in the source.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: The naming tradition of Uranus's moons using Shakespeare allusions began in 1787.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states the tradition began in 1687, not 1787.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered two new rings in addition to the older nine rings.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states three new rings and eight older rings, not two and nine.
- **M-017** -- the two documents disagree
  - `merged.md:7` says: During its flyby, Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis and off-center.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 66 degrees, not 59.
- **M-018** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour).
  - `source_b.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states km/h units and a different conversion than the claim's mph/km-h figures.
- **M-019** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface.
  - `source_b.md` says: 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states 479 miles (900 km) and a lake, not 497 miles (800 km) and an ocean.
- **M-021** -- the two documents disagree
  - `merged.md:11` says: Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - `source_b.md` says: 'spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The claim's moon names (Ariel, Umbriel, Titania) differ from those stated in the source.
- **M-022** -- the two documents disagree
  - `merged.md:11` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons.
  - `source_b.md` says: 'five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source describes them as smaller moons, not larger.
- **M-024** -- the two documents disagree
  - `merged.md:11` says: The Miranda flyby was Voyager 2's closest approach to any object so far in its nearly decade-long travels.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states nearly century-long, not decade-long.
- **M-027** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident killed seven astronauts during their space shuttle launch.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states six astronauts, not seven.
- **M-028** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident occurred Jan. 28, 1986.
  - `source_b.md` says: 'during their space shuttle launch Feb. 28, 1986' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states February 28, not January 28.
- **M-029** -- the two documents disagree
  - `merged.md:13` says: The Challenger accident occurred the same week as the news of the Uranus encounter.
  - `source_b.md` says: 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Source states the same day, not the same week.

### Invented — in the merge, in neither source

- **M-008** (`merged.md:5`) — Voyager 2's long-range observations of Uranus began Nov. 4, 1985.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: No source states long-range observations beginning Nov. 4, 1985.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 5.5, 2.5 | 4,5 | English (72 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (2 numeral(s) voting decimal point, 1 decimal comma), and a reader of that convention takes it for 45
- **reading resolved by the merge** `m12` (`source_b.md`) - source_b.md writes '17.560' beside 'miles' (line 7), which reads 17.56 in its decimal point convention; the merge writes '17,560' (line 11), which reads 17560 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels.
  What changed:  In flying by Miranda at a range of only 17[-.-]{+,+}560 miles (28[-.-]{+,+}260 kilometers), the spacecraft came closest to any object so far in its nearly [-century-long-] {+decade-long+} travels.
  ```
- **reading resolved by the merge** `m12` (`source_b.md`) - source_b.md writes '28.260' beside 'kilometers' (line 7), which reads 28.26 in its decimal point convention; the merge writes '28,260' (line 11), which reads 28260 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels.
  What changed:  In flying by Miranda at a range of only 17[-.-]{+,+}560 miles (28[-.-]{+,+}260 kilometers), the spacecraft came closest to any object so far in its nearly [-century-long-] {+decade-long+} travels.
  ```

## Length capped

- `$.additions[5].source` was 212 characters, over the 200-character cap; capped to fit
- `$.additions[5].reason` was 97 characters, over the 80-character cap; capped to fit
- `$.additions[8].reason` was 81 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 7 contradicted, 0 carried in part, 5 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with three planetary encounters. | 3 | contradicted | 'Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters' in `merged.md` -- The text names Voyager 2 with two encounters, not Voyager 3 with three. |
| 5 | The Uranus encounter's geometry was defined in part by the possibility of a future encounter with Saturn. | 7 | contradicted | "The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune" in `merged.md` -- Text says Neptune, not Saturn. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | contradicted | 'Voyager 2 had only 5.5 hours of close study during its flyby' in `merged.md` -- Text refers to Voyager 2 with 5.5 hours, not Voyager 1 with 6.4 days. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | "The first human-made object to fly past Uranus, Voyager 2's long-range observations of the planet began Nov. 4, 1985" in `merged.md` -- Text states Voyager 2, not Voyager 1, was first. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | "Voyager 2's long-range observations of the planet began Nov. 4, 1985" in `merged.md` -- Text states long-range observations began Nov. 4, 1985 by Voyager 2, not short-range by Voyager 1 on Jan. 31, 1987. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986' in `merged.md` -- Text says UT and year 1986, not ED and 1968. |
| 12 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 50,640 miles (81,500 kilometers)' in `merged.md` -- Text has miles and kilometers reversed from the claim's units. |
| 2 | Mission planners directed the spacecraft to Uranus. | 3 | carried | 'mission planners directed the veteran spacecraft to Uranus' in `merged.md` -- Directly stated. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that would take about 4,5 years' in `merged.md` -- Directly stated. |
| 4 | The spacecraft's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | carried | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- Directly stated. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals took approximately 2.5 hours to reach Earth' in `merged.md` -- Matches value (comma vs period is formatting variance from original spelled differently but numeric value same). |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were 400 times less than terrestrial conditions' in `merged.md` -- 400 times equals five-hundred... wait check. |

### `source_b.md` -- 22 claim(s): 0 dropped, 15 contradicted, 0 carried in part, 7 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 2 discovered 11 new moons during its flyby of Uranus. | 3 | contradicted | 'Voyager 2 discovered 10 new moons' in `merged.md` -- Text states 10 new moons, not 11. |
| 2 | The new moons discovered were given names including Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- Names differ from the claim's altered spellings. |
| 3 | The names of the new moons are allusions to Goethe. | 3 | contradicted | 'obvious allusions to Shakespeare' in `merged.md` -- Text says Shakespeare, not Goethe. |
| 4 | The naming tradition for Uranus' moons began in 1687. | 3 | contradicted | 'continuing a naming tradition begun in 1787' in `merged.md` -- Text says 1787, not 1687. |
| 5 | Voyager 2 discovered three new rings at Uranus in addition to the older eight rings. | 3 | contradicted | 'two new rings in addition to the "older" nine rings' in `merged.md` -- Text says two new rings and nine older rings, not three new and eight older. |
| 6 | Voyager 2 found Uranus' magnetic field tilted at 66 degrees off-axis and off-center. | 3 | contradicted | 'a magnetic field tilted at 59 degrees off-axis and off-center' in `merged.md` -- Text says 59 degrees, not 66 degrees. |
| 8 | 450 km/h is equivalent to 72400 meters per hour as stated in the document. | 5 | contradicted | '724 kilometers per hour' in `merged.md` -- Text states 724 km/h, not 72400 meters per hour equivalent claim of 450 km/h converted differently. |
| 9 | The spacecraft found evidence of a boiling lake of water some 479 miles below the top cloud surface of Uranus. | 5 | contradicted | 'found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface' in `merged.md` -- Text says ocean not lake, and 497 miles not 479 miles. |
| 10 | The document states the boiling lake of water was some 900 kilometers below the top cloud surface. | 5 | contradicted | 'some 497 miles (800 kilometers) below the top cloud surface' in `merged.md` -- Text states 800 kilometers, not 900 kilometers. |
| 12 | Uranus' rings were found to be extremely variable in transparency. | 5 | contradicted | 'Its rings were found to be extremely variable in thickness and opacity' in `merged.md` -- Text says opacity, not transparency, which is the inverse property. |
| 13 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- Text lists Ariel, Umbriel, and Titania, not the altered names in the claim. |
| 14 | Miranda, Oberon, Ariele, Umbrella, and Titan are described as five of Uranus' smaller moons. | 7 | contradicted | "five of Uranus' larger moons" in `merged.md` -- Text says larger moons, not smaller. |
| 20 | News of the Uranus encounter was interrupted the same day by the Challenger accident. | 9 | contradicted | 'was interrupted the same week by the tragic Challenger accident' in `merged.md` -- Text says same week, not same day. |
| 21 | The Challenger accident killed six astronauts. | 9 | contradicted | 'the tragic Challenger accident that killed seven astronauts' in `merged.md` -- Text says seven astronauts, not six. |
| 22 | The Challenger accident occurred during a space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'during their space shuttle launch Jan. 28, 1986' in `merged.md` -- Text states Jan. 28, 1986, not Feb. 28, 1986. |
| 7 | The spacecraft found wind speeds in Uranus' atmosphere as high as 450 km/h. | 5 | carried | "wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour)" in `merged.md` -- 450 mph converts to 724 km/h, but claim states 450 km/h which is a different unit conversion; checking further. |
| 11 | Uranus' rings were found to be extremely variable in thickness. | 5 | carried | 'Its rings were found to be extremely variable in thickness and opacity' in `merged.md` -- Directly states variable thickness. |
| 15 | Voyager 2 flew by Miranda at a range of only 17.560 miles. | 7 | carried | 'In flying by Miranda at a range of only 17,560 miles (28,260 kilometers)' in `merged.md` -- Matches the mile figure exactly. |
| 16 | The document states the flyby range of Miranda was 28.260 kilometers. | 7 | carried | '17,560 miles (28,260 kilometers)' in `merged.md` -- Matches the kilometer figure exactly. |
| 17 | The Miranda flyby was the closest Voyager 2 had come to any object during its travels up to that point. | 7 | carried | 'the spacecraft came closest to any object so far in its nearly decade-long travels' in `merged.md` -- Directly states closest approach so far. |
| 18 | Images of Miranda showed a surface that was a mishmash of peculiar features. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features' in `merged.md` -- Directly stated. |
| 19 | Uranus itself appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless' in `merged.md` -- Directly stated verbatim. |

### `merged.md` -- 29 claim(s): 1 invented, 22 contradicted, 0 supported in part, 6 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 8 | Voyager 2's long-range observations of Uranus began Nov. 4, 1985. | invented | -- | No source states long-range observations beginning Nov. 4, 1985. |
| 1 | Voyager 2 had fulfilled its primary mission goals with two planetary encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- Source names Voyager 3 with three encounters, not Voyager 2 with two. |
| 2 | Mission planners directed Voyager 2 to Uranus. | contradicted | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus' in `source_a.md` -- The veteran spacecraft referenced is Voyager 3, not Voyager 2. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `source_a.md` -- This refers to Voyager 3's Jupiter encounter, not Voyager 2's. |
| 5 | The Uranus encounter's geometry was defined by the possibility of a future encounter with Neptune. | contradicted | `source_a.md` | "The Ur anus encounter's geometry was also defined by the possibility of a future encounter with Saturn" in `source_a.md`, **transcription_error** -- Source states Saturn, not Neptune. |
| 6 | Voyager 2 had only 5.5 hours of close study during its Uranus flyby. | contradicted | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby' in `source_a.md` -- Source attributes 6.4 days to Voyager 1, not 5.5 hours to Voyager 2. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- Source credits Voyager 1 as first, not Voyager 2. |
| 10 | Light conditions at Uranus were 400 times less than terrestrial conditions. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions' in `source_a.md` -- Source states 500 times, not 400 times. |
| 11 | Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- Source states year 1968, not 1986. |
| 12 | Closest approach to Uranus occurred at a range of about 50,640 miles (81,500 kilometers). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- Units are swapped in the claim compared to the source. |
| 13 | During its flyby, Voyager 2 discovered 10 new moons. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- Source states 11 new moons, not 10. |
| 14 | The 10 new moons discovered were given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | contradicted | `source_b.md` | 'given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- The claim's spellings of the moon names differ from those given in the source. |
| 15 | The naming tradition of Uranus's moons using Shakespeare allusions began in 1787. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- Source states the tradition began in 1687, not 1787. |
| 16 | During its flyby, Voyager 2 discovered two new rings in addition to the older nine rings. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- Source states three new rings and eight older rings, not two and nine. |
| 17 | During its flyby, Voyager 2 discovered a magnetic field tilted at 59 degrees off-axis and off-center. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- Source states 66 degrees, not 59. |
| 18 | Voyager 2 found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour). | contradicted | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- Source states km/h units and a different conversion than the claim's mph/km-h figures. |
| 19 | Voyager 2 found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface. | contradicted | `source_b.md` | 'a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- Source states 479 miles (900 km) and a lake, not 497 miles (800 km) and an ocean. |
| 21 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | contradicted | `source_b.md` | 'spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan' in `source_b.md` -- The claim's moon names (Ariel, Umbriel, Titania) differ from those stated in the source. |
| 22 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' larger moons. | contradicted | `source_b.md` | 'five of Uranus’ smaller moons' in `source_b.md` -- Source describes them as smaller moons, not larger. |
| 24 | The Miranda flyby was Voyager 2's closest approach to any object so far in its nearly decade-long travels. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- Source states nearly century-long, not decade-long. |
| 27 | The Challenger accident killed seven astronauts during their space shuttle launch. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts' in `source_b.md` -- Source states six astronauts, not seven. |
| 28 | The Challenger accident occurred Jan. 28, 1986. | contradicted | `source_b.md` | 'during their space shuttle launch Feb. 28, 1986' in `source_b.md` -- Source states February 28, not January 28. |
| 29 | The Challenger accident occurred the same week as the news of the Uranus encounter. | contradicted | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- Source states the same day, not the same week. |
| 3 | The journey to Uranus would take about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years' in `source_a.md` -- Matches the stated duration. |
| 9 | Signals from Voyager 2 took approximately 2.5 hours to reach Earth. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth' in `source_a.md` -- Matches the stated signal travel time. |
| 20 | Uranus's rings were found to be extremely variable in thickness and opacity. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency' in `source_b.md` -- Opacity is the inverse property of transparency, describing the same variability. |
| 23 | Voyager 2 flew by Miranda at a range of only 17,560 miles (28,260 kilometers). | supported | `source_b.md` | 'at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- Numbers match despite different punctuation formatting. |
| 25 | Images of Miranda showed a surface that was a mishmash of peculiar features. | supported | `source_b.md` | 'a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason' in `source_b.md` -- Matches the claim's description of Miranda's surface. |
| 26 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless' in `source_b.md` -- Exact match to source statement. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **29** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **34**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 12 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '1' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '6.4' (days) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '2,5' (hours) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '11' (new) does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '1687' does not survive into the merge unchanged
- `b2` (`source_b.md`) — numeric '66' (degrees) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '72400' (meters) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '479' (miles) does not survive into the merge unchanged
- `b3` (`source_b.md`) — numeric '900' (kilometers) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '17.560' (miles) does not survive into the merge unchanged
- `b6` (`source_b.md`) — numeric '28.260' (kilometers) does not survive into the merge unchanged

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **12** departure(s) from its sources. Checking them confirms 2, rejects 9, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Fixed spacecraft name and encounter count per NASA source | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED (`A-001`) |
| `a4` | reworded | Fixed planet, spacecraft, and duration per NASA source | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED (`A-005`, `A-006`) |
| `a5` | reworded | Fixed spacecraft, observation phase, and date per NASA source | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a6` | reworded | NASA source states 400 times, not 500 | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`) |
| `a7` | reworded | Fixed year, timezone label, and swapped km/miles | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | superseded | Base title kept; both titles were identical | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'superseded' is what happened to it (no claim traced to it) |
| `b2` | reworded | Fixed moon count, spellings, allusion, ring count, and tilt | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`, `B-005`, `B-006`) |
| `b3` | reworded | Fixed unit conversion and ocean depth figure per NASA source | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED, B-009 came back CONTRADICTED, B-010 came back CONTRADICTED (`B-008`, `B-009`, `B-010`) |
| `b4` | reworded | NASA source says opacity, not transparency | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back CONTRADICTED (`B-012`) |
| `b5` | reworded | Fixed moon names (Titan is Saturn's) and larger/smaller | **rejected** | declared 'reworded', which predicts SUPPORTED; B-013 came back CONTRADICTED, B-014 came back CONTRADICTED (`B-013`, `B-014`) |
| `b6` | reworded | Fixed century-long to decade-long per NASA source | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-015`, `B-016`, `B-017`) |
| `b9` | reworded | Fixed casualty count, date, and timing per NASA source | **rejected** | declared 'reworded', which predicts SUPPORTED; B-020 came back CONTRADICTED, B-021 came back CONTRADICTED, B-022 came back CONTRADICTED (`B-020`, `B-021`, `B-022`) |

## Added from outside the documents

The merge declared 11 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. The model took more turns on 7 call(s) than a call that retrieves nothing can take, so it used a tool it was granted at least that often. It is a count of turns rather than of fetches, and which statement a retrieval belongs to is not recorded. The endpoint's own web-request counter reported none, which on this backend means it could not see one rather than that none was made: it counts a vendor's server-side tools and a command-line tool runs in the model's own process.

11 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Although Voyager 2 had fulfilled its primary mission goals with the two planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants' (science.nasa.gov/mission/voyager/voyager-2/) | Only Voyager 1 and 2 exist; NASA text names two prior encounters | *none* |
| The Uranus encounter's geometry was also defined by the possibility of a future encounter with Neptune: Voyager 2 had only 5.5 hours of close study during its flyby. | The Ur anus encounter's geometry was also defined by the possibility of a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby. | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants' (science.nasa.gov/mission/voyager/voyager-2/) | NASA's text names Neptune, Voyager 2, and 5.5 hours | *none* |
| The first human-made object to fly past Uranus, Voyager 2's long-range observations of the planet began Nov. 4, 1985, when signals took approximately 2.5 hours to reach Earth. | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants' (science.nasa.gov/mission/voyager/voyager-2/) | NASA names Voyager 2, long-range phase, starting Nov. 4, 1985 | *none* |
| Light conditions were 400 times less than terrestrial conditions. | five-hundred times less than terrestrial conditions | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants' (science.nasa.gov/mission/voyager/voyager-2/) | NASA's figure is 400 times, not 500 | *none* |
| Closest approach to Uranus took place at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers). | 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants' (science.nasa.gov/mission/voyager/voyager-2/) | Encounter was 1986 UT; the km/miles labels were swapped | *none* |
| During its flyby, Voyager 2 discovered 10 new moons (given such names as Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca – obvious allusions to Shakespeare, continuing a naming tradition begun in 1787), two new rings in addition to the "older" nine rings, and a magnetic field tilted at 59 degrees off-axis and off-center. | 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the "older" eight rings, and a magnetic field tilted at 66 degrees | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants'; corroborated by Wikipedia 'Cressida (moon)' and 'Rings of Uranus' for names/ring count, and multiple sources (EBSCO, Planetary Society) for t | Ten named moons, Shakespeare, 1787, nine prior rings, and ~59° tilt are consiste | *none* |
| The spacecraft found wind speeds in Uranus' atmosphere as high as 450 miles per hour (724 kilometers per hour) and found evidence of a boiling ocean of water some 497 miles (800 kilometers) below the top cloud surface. | 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants' (science.nasa.gov/mission/voyager/voyager-2/) | NASA gives 450 mph (724 km/h) winds and a 497-mile (800 km) ocean depth | *none* |
| Its rings were found to be extremely variable in thickness and opacity. | thickness and transparency | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants' (science.nasa.gov/mission/voyager/voyager-2/) | NASA's wording says opacity, not transparency | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus' larger moons. | Ariele, Umbrella, and Titan, five of Uranus' smaller moons | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants' (science.nasa.gov/mission/voyager/voyager-2/) | Titan is a moon of Saturn; NASA names Ariel, Umbriel, Titania as the larger moon | *none* |
| In flying by Miranda at a range of only 17,560 miles (28,260 kilometers), the spacecraft came closest to any object so far in its nearly decade-long travels. | nearly century-long travels | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants' (science.nasa.gov/mission/voyager/voyager-2/) | Voyager 2 had flown under 9 years by 1986, not a century | *none* |
| The spectacular news of the Uranus encounter was interrupted the same week by the tragic Challenger accident that killed seven astronauts during their space shuttle launch Jan. 28, 1986. | the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986 | cited | NASA Science, 'Voyager 2: First To Visit All Four Giants'; Wikipedia 'Space Shuttle Challenger disaster'; History.com | Challenger launched Jan. 28, 1986, killing seven, the same week as the flyby | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 2d9e6f013ad9 (command) -- Claude Code - Sonnet |
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
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | unknown (8 call(s) reported no usage) |
| Cost | unmeasured (8 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 2 |
| Retrieval | WebSearch, WebFetch permitted; 7 of 8 call(s) used a tool (82 turn(s) in total) |
| Isolation | decompose, merge, verify: safe mode, tools WebSearch, WebFetch |
| Errors | 0 |
| Duration | 1052.7s |
| Generated | 2026-09-26T16:48:07+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `6d8a835cc983` |
| Prompt | `prompts/verify.md` `55a721b20905` |
| Prompt | `prompts/verify_reverse.md` `2a6d7e955709` |

> **Document content was handed to a program on this machine (`Claude Code - Sonnet`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The model was permitted to reach the network** (WebSearch, WebFetch), so a query or a fetch it made may have carried text from these documents to a third party. 7 of 8 call(s) used a tool (82 turn(s) in total), counted in turns rather than in fetches. LLossless itself made no network request of any kind and resolved none of the sources the merge names.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
