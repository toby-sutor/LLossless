## Verdict

**54 finding(s).** In the claims: 1 partially dropped, 37 contradicted, 2 hallucinated, 3 partially invented. In the structure: 11 verbatim violation. 6 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 33 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 19 |
| Forward — source claims accounted for in the merge | **8/31** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **4/12** |
| Forward — `source_b.md` claims accounted for | **4/19** (1 in part) |
| Reverse — merge claims found in a source | **13/33** |
| Reverse — supported only in part | 3 |
| Evidence grounded | **61/62** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-004** (`source_b.md:3`) — The names continued a naming tradition begun in 1687.
  - evidence: 'The moons’ names follow the established literary naming tradition for Uranian moons' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference says the names follow an established tradition but does not state that it began in 1687.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'After completing its primary mission goals with the Jupiter and Saturn encounters, Voyager 2 continued to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference attributes the completed goals to Voyager 2 and names Jupiter and Saturn, not Voyager 3 and three encounters.
- **A-002** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'Voyager 2 continued to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies Voyager 2, not Voyager 3, as the spacecraft that continued to Uranus.
- **A-004** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference attributes the Jupiter encounter and its optimization to Voyager 2, not Voyager 3.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Ur anus encounter’s geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter’s geometry also allowed for a possible onward encounter with Neptune.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says the possible onward encounter was with Neptune, not Saturn.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2, the first human-made object to fly past Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies Voyager 2, not Voyager 1, as the first human-made object to fly past Uranus.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: 'Voyager 2, the first human-made object to fly past Uranus, began close-range observations on Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives Voyager 2 and Jan. 24, 1986, rather than Voyager 1 and Jan. 31, 1987.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach took place at 17:59 UTC on Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives UTC and Jan. 24, 1986, not ED and Jan. 24, 1968.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles).' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference assigns 81,500 to kilometers and 50,640 to miles, the reverse of the claim.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby.
  - `merged.md` says: 'discovered 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states that Voyager 2 discovered 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: Some names given to the 11 new moons were Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'During its flyby, Voyager 2 discovered 10 new moons and two new rings, bringing the known ring total to 11, and measured a magnetic field tilted at 59 degrees off-axis and off-center. The moons’ names follow the established literary naming tradition for Uranian moons, drawing on Shakespeare and Alexander Pope; the names include Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 10 new moons and names including Puck, Portia, Juliet, and Bianca, rather than the claimed count and names.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: The names were allusions to Goethe.
  - `merged.md` says: 'The moons’ names follow the established literary naming tradition for Uranian moons, drawing on Shakespeare and Alexander Pope' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference attributes the literary tradition to Shakespeare and Alexander Pope, not Goethe.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings.
  - `merged.md` says: 'two new rings' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says Voyager 2 discovered two new rings, not three.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Uranus had eight older rings.
  - `merged.md` says: 'two new rings, bringing the known ring total to 11' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Two new rings bringing the known total to 11 means nine rings were previously known, not eight.
- **B-007** -- the two documents disagree
  - `source_b.md:3` says: Uranus’ magnetic field was tilted at 66 degrees off-axis.
  - `merged.md` says: 'measured a magnetic field tilted at 59 degrees off-axis' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives the tilt as 59 degrees, not 66 degrees.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: Wind speeds in Uranus’ atmosphere reached as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: '450 km/h (450,000 meters per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 450,000 meters per hour, not 72400 meters per hour.
- **B-010** -- the two documents disagree
  - `source_b.md:5` says: The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  - `merged.md` says: 'It found no boiling lake of water beneath the cloud tops.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference explicitly says no boiling lake of water was found.
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Ariel, Umbriel, and Titania, not Ariele, Umbrella, and Titan.
- **B-013** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan were five of Uranus’ smaller moons.
  - `merged.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies five smaller moons, but three of the names in the claim differ from those it gives.
- **B-014** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 flew by Miranda at a range of 17.560 miles (28.260 kilometers).
  - `merged.md` says: 'It passed within about 18,000 miles (29,000 kilometers) of Miranda' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives a different range for Voyager 2’s pass by Miranda.
- **B-015** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 came closest to any object so far in its nearly century-long travels during its flyby of Miranda.
  - `merged.md` says: 'its closest approach to any object during its nearly nine-year journey' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference describes the journey as nearly nine years, not nearly a century.
- **B-018** -- the two documents disagree
  - `source_b.md:9` says: News of Voyager 2’s Uranus encounter was interrupted on the same day by the Challenger accident.
  - `merged.md` says: 'Closest approach took place at 17:59 UTC on Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles).\nThe Uranus encounter’s news was soon overshadowed by the Challenger disaster, which killed seven astronauts when the space shuttle broke apart during launch on Jan. 28, 1986.' (transcription_error)
  - judged against: `merged.md`
  - why this was read as a contradiction: The encounter’s closest approach was Jan. 24, while the Challenger disaster occurred Jan. 28, so they were not on the same day.
- **B-019** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts during their space shuttle launch on Feb. 28, 1986.
  - `merged.md` says: 'The Uranus encounter’s news was soon overshadowed by the Challenger disaster, which killed seven astronauts when the space shuttle broke apart during launch on Jan. 28, 1986.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says seven astronauts were killed on Jan. 28, not six on Feb. 28.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 completed its primary mission goals with the Jupiter and Saturn encounters.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes completion of the primary mission goals to Voyager 3, not Voyager 2, and specifies three encounters.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes the optimized Jupiter encounter to the spacecraft identified immediately before as Voyager 3, not Voyager 2.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: The geometry of the Uranus encounter allowed for a possible onward encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn:' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Saturn, not Neptune, as the possible future encounter.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987," (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies Voyager 1, rather than Voyager 2, as the first human-made object to fly past Uranus.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 began close-range observations on Jan. 24, 1986.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987," (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives Voyager 1 and Jan. 31, 1987, rather than Voyager 2 and Jan. 24, 1986.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach took place at 17:59 UTC on Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968,' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the year as 1968, not 1986, and does not identify this as Voyager 2's approach.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach was at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles).' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source assigns 50,640 to kilometers and 81,500 to miles, the reverse of the claim.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered 10 new moons during its flyby.
  - `source_b.md` says: 'During its flyby, Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source reports 11 new moons, not 10.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered two new rings during its flyby.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source reports three new rings, not two.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 measured a magnetic field tilted at 59 degrees off-axis.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives a tilt of 66 degrees, not 59 degrees.
- **M-022** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 measured wind speeds in Uranus’ atmosphere as high as 450 km/h (450,000 meters per hour).
  - `source_b.md` says: '450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 72400 meters per hour, not 450,000 meters per hour.
- **M-023** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 found no boiling lake of water beneath the cloud tops.
  - `source_b.md` says: 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source reports evidence of a boiling lake beneath the cloud surface, contrary to the claim.
- **M-029** -- the two documents disagree
  - `merged.md:9` says: Miranda was the object Voyager 2 approached most closely during its nearly nine-year journey.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The claim says the journey was nearly nine years, whereas the source says the travels were nearly a century long.
- **M-032** -- the two documents disagree
  - `merged.md:11` says: The Challenger disaster killed seven astronauts.
  - `source_b.md` says: 'that killed six astronauts' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the Challenger accident killed six astronauts, not seven.
- **M-033** -- the two documents disagree
  - `merged.md:11` says: The space shuttle broke apart during launch on Jan. 28, 1986.
  - `source_b.md` says: 'during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source places the accident during the launch on Feb. 28, 1986, not Jan. 28, 1986.

### Invented — in the merge, in neither source

- **M-019** (`merged.md:7`) — The naming tradition for Uranian moons draws on Shakespeare.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Neither source states that the Uranian moon naming tradition draws on Shakespeare.
- **M-020** (`merged.md:7`) — The naming tradition for Uranian moons draws on Alexander Pope.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: Neither source states that the Uranian moon naming tradition draws on Alexander Pope.

### Partly invented — the sources carry some of this claim

- **M-021** (`merged.md:7`) — The names include Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.
  - evidence: 'Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source gives Belinda, Desdemona, and Ophelia exactly, but gives different forms for the other claimed names.
- **M-026** (`merged.md:9`) — Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania.
  - evidence: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source supports photos of Miranda and Oberon, but names Ariele, Umbrella, and Titan rather than Ariel, Umbriel, and Titania.
- **M-027** (`merged.md:9`) — Miranda, Oberon, Ariel, Umbriel, and Titania were five of Uranus’ smaller moons.
  - evidence: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source identifies Miranda and Oberon as two of the five smaller moons, but gives different names for the other three.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (70 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m6` (`merged.md`) - '2,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25

## Length capped

- `$.additions[10].reason` was 81 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 8 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'After completing its primary mission goals with the Jupiter and Saturn encounters, Voyager 2 continued to Uranus' in `merged.md` -- The reference attributes the completed goals to Voyager 2 and names Jupiter and Saturn, not Voyager 3 and three encounters. |
| 2 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'Voyager 2 continued to Uranus' in `merged.md` -- The reference identifies Voyager 2, not Voyager 3, as the spacecraft that continued to Uranus. |
| 4 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- The reference attributes the Jupiter encounter and its optimization to Voyager 2, not Voyager 3. |
| 5 | The Ur anus encounter’s geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter’s geometry also allowed for a possible onward encounter with Neptune.' in `merged.md` -- The reference says the possible onward encounter was with Neptune, not Saturn. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2, the first human-made object to fly past Uranus' in `merged.md` -- The reference identifies Voyager 2, not Voyager 1, as the first human-made object to fly past Uranus. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | 'Voyager 2, the first human-made object to fly past Uranus, began close-range observations on Jan. 24, 1986' in `merged.md` -- The reference gives Voyager 2 and Jan. 24, 1986, rather than Voyager 1 and Jan. 31, 1987. |
| 11 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach took place at 17:59 UTC on Jan. 24, 1986' in `merged.md` -- The reference gives UTC and Jan. 24, 1986, not ED and Jan. 24, 1968. |
| 12 | Closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles).' in `merged.md` -- The reference assigns 81,500 to kilometers and 50,640 to miles, the reverse of the claim. |
| 3 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey that took about 4,5 years' in `merged.md` -- The reference gives the journey to Uranus as taking about 4,5 years. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `merged.md` -- The reference states this directly. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals took approximately 2,5 hours to reach Earth' in `merged.md` -- The reference states that signals took approximately 2,5 hours to reach Earth. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | carried | 'Light conditions were five-hundred times less than terrestrial conditions.' in `merged.md` -- The reference states this directly. |

### `source_b.md` -- 19 claim(s): 0 dropped, 14 contradicted, 1 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 2 discovered 11 new moons during its flyby. | 3 | contradicted | 'discovered 10 new moons' in `merged.md` -- The reference states that Voyager 2 discovered 10 new moons, not 11. |
| 2 | Some names given to the 11 new moons were Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'During its flyby, Voyager 2 discovered 10 new moons and two new rings, bringing the known ring total to 11, and measured a magnetic field tilted at 59 degrees off-axis and off-center. The moons’ names follow the established literary naming tradition for Uranian moons, drawing on Shakespeare and Alexander Pope; the names include Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.' in `merged.md` -- The reference gives 10 new moons and names including Puck, Portia, Juliet, and Bianca, rather than the claimed count and names. |
| 3 | The names were allusions to Goethe. | 3 | contradicted | 'The moons’ names follow the established literary naming tradition for Uranian moons, drawing on Shakespeare and Alexander Pope' in `merged.md` -- The reference attributes the literary tradition to Shakespeare and Alexander Pope, not Goethe. |
| 5 | Voyager 2 discovered three new rings. | 3 | contradicted | 'two new rings' in `merged.md` -- The reference says Voyager 2 discovered two new rings, not three. |
| 6 | Uranus had eight older rings. | 3 | contradicted | 'two new rings, bringing the known ring total to 11' in `merged.md` -- Two new rings bringing the known total to 11 means nine rings were previously known, not eight. |
| 7 | Uranus’ magnetic field was tilted at 66 degrees off-axis. | 3 | contradicted | 'measured a magnetic field tilted at 59 degrees off-axis' in `merged.md` -- The reference gives the tilt as 59 degrees, not 66 degrees. |
| 9 | Wind speeds in Uranus’ atmosphere reached as high as 450 km/h (72400 meters per hour). | 5 | contradicted | '450 km/h (450,000 meters per hour)' in `merged.md` -- The reference gives 450,000 meters per hour, not 72400 meters per hour. |
| 10 | The spacecraft found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | contradicted | 'It found no boiling lake of water beneath the cloud tops.' in `merged.md` -- The reference explicitly says no boiling lake of water was found. |
| 12 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons.' in `merged.md` -- The reference names Ariel, Umbriel, and Titania, not Ariele, Umbrella, and Titan. |
| 13 | Miranda, Oberon, Ariele, Umbrella, and Titan were five of Uranus’ smaller moons. | 7 | contradicted | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons.' in `merged.md` -- The reference identifies five smaller moons, but three of the names in the claim differ from those it gives. |
| 14 | Voyager 2 flew by Miranda at a range of 17.560 miles (28.260 kilometers). | 7 | contradicted | 'It passed within about 18,000 miles (29,000 kilometers) of Miranda' in `merged.md` -- The reference gives a different range for Voyager 2’s pass by Miranda. |
| 15 | Voyager 2 came closest to any object so far in its nearly century-long travels during its flyby of Miranda. | 7 | contradicted | 'its closest approach to any object during its nearly nine-year journey' in `merged.md` -- The reference describes the journey as nearly nine years, not nearly a century. |
| 18 | News of Voyager 2’s Uranus encounter was interrupted on the same day by the Challenger accident. | 9 | contradicted | 'Closest approach took place at 17:59 UTC on Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles).\nThe Uranus encounter’s news was soon overshadowed by the Challenger disaster, which killed seven astronauts when the space shuttle broke apart during launch on Jan. 28, 1986.' in `merged.md`, **transcription_error** -- The encounter’s closest approach was Jan. 24, while the Challenger disaster occurred Jan. 28, so they were not on the same day. |
| 19 | The Challenger accident killed six astronauts during their space shuttle launch on Feb. 28, 1986. | 9 | contradicted | 'The Uranus encounter’s news was soon overshadowed by the Challenger disaster, which killed seven astronauts when the space shuttle broke apart during launch on Jan. 28, 1986.' in `merged.md` -- The reference says seven astronauts were killed on Jan. 28, not six on Feb. 28. |
| 4 | The names continued a naming tradition begun in 1687. | 3 | carried in part | 'The moons’ names follow the established literary naming tradition for Uranian moons' in `merged.md` -- The reference says the names follow an established tradition but does not state that it began in 1687. |
| 8 | Uranus’ magnetic field was off-center. | 3 | carried | 'measured a magnetic field tilted at 59 degrees off-axis and off-center' in `merged.md` -- The reference states that the magnetic field was off-center. |
| 11 | Uranus’ rings were variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- The reference describes the rings as extremely variable in thickness and transparency. |
| 16 | Images of Miranda showed features on its surface. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.' in `merged.md` -- The reference says images showed peculiar features on Miranda’s surface. |
| 17 | Uranus appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- The reference states that Uranus appeared generally featureless. |

### `merged.md` -- 33 claim(s): 2 invented, 15 contradicted, 3 supported in part, 13 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 19 | The naming tradition for Uranian moons draws on Shakespeare. | invented | -- | Neither source states that the Uranian moon naming tradition draws on Shakespeare. |
| 20 | The naming tradition for Uranian moons draws on Alexander Pope. | invented | -- | Neither source states that the Uranian moon naming tradition draws on Alexander Pope. |
| 1 | Voyager 2 completed its primary mission goals with the Jupiter and Saturn encounters. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source attributes completion of the primary mission goals to Voyager 3, not Voyager 2, and specifies three encounters. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- The source attributes the optimized Jupiter encounter to the spacecraft identified immediately before as Voyager 3, not Voyager 2. |
| 5 | The geometry of the Uranus encounter allowed for a possible onward encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn:' in `source_a.md` -- The source names Saturn, not Neptune, as the possible future encounter. |
| 7 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987," in `source_a.md` -- The source identifies Voyager 1, rather than Voyager 2, as the first human-made object to fly past Uranus. |
| 8 | Voyager 2 began close-range observations on Jan. 24, 1986. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987," in `source_a.md` -- The source gives Voyager 1 and Jan. 31, 1987, rather than Voyager 2 and Jan. 24, 1986. |
| 11 | Voyager 2's closest approach took place at 17:59 UTC on Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968,' in `source_a.md` -- The source gives the year as 1968, not 1986, and does not identify this as Voyager 2's approach. |
| 12 | Voyager 2's closest approach was at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles).' in `source_a.md` -- The source assigns 50,640 to kilometers and 81,500 to miles, the reverse of the claim. |
| 13 | Voyager 2 discovered 10 new moons during its flyby. | contradicted | `source_b.md` | 'During its flyby, Voyager 2 discovered 11 new moons' in `source_b.md` -- The source reports 11 new moons, not 10. |
| 14 | Voyager 2 discovered two new rings during its flyby. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source reports three new rings, not two. |
| 16 | Voyager 2 measured a magnetic field tilted at 59 degrees off-axis. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center.' in `source_b.md` -- The source gives a tilt of 66 degrees, not 59 degrees. |
| 22 | Voyager 2 measured wind speeds in Uranus’ atmosphere as high as 450 km/h (450,000 meters per hour). | contradicted | `source_b.md` | '450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives 72400 meters per hour, not 450,000 meters per hour. |
| 23 | Voyager 2 found no boiling lake of water beneath the cloud tops. | contradicted | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.' in `source_b.md` -- The source reports evidence of a boiling lake beneath the cloud surface, contrary to the claim. |
| 29 | Miranda was the object Voyager 2 approached most closely during its nearly nine-year journey. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels.' in `source_b.md` -- The claim says the journey was nearly nine years, whereas the source says the travels were nearly a century long. |
| 32 | The Challenger disaster killed seven astronauts. | contradicted | `source_b.md` | 'that killed six astronauts' in `source_b.md` -- The source says the Challenger accident killed six astronauts, not seven. |
| 33 | The space shuttle broke apart during launch on Jan. 28, 1986. | contradicted | `source_b.md` | 'during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source places the accident during the launch on Feb. 28, 1986, not Jan. 28, 1986. |
| 21 | The names include Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | supported in part | `source_b.md` | 'Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II' in `source_b.md` -- The source gives Belinda, Desdemona, and Ophelia exactly, but gives different forms for the other claimed names. |
| 26 | Voyager 2 returned photos of Miranda, Oberon, Ariel, Umbriel, and Titania. | supported in part | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source supports photos of Miranda and Oberon, but names Ariele, Umbrella, and Titan rather than Ariel, Umbriel, and Titania. |
| 27 | Miranda, Oberon, Ariel, Umbriel, and Titania were five of Uranus’ smaller moons. | supported in part | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source identifies Miranda and Oberon as two of the five smaller moons, but gives different names for the other three. |
| 2 | Voyager 2 continued to Uranus. | supported | `source_b.md` | '# Voyager 2 at Uranus' in `source_b.md` -- The source identifies Voyager 2 as being at Uranus. |
| 3 | The journey to Uranus took about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years.' in `source_a.md` -- The source states that the journey to Uranus would take about 4,5 years. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- The source states this directly. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth.' in `source_a.md` -- The source states that signals took approximately 2,5 hours to reach Earth. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | supported | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- The source states this directly. |
| 15 | The known ring total was 11. | supported | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source reports three new rings and eight older rings, which together make a total of 11. |
| 17 | Voyager 2 measured a magnetic field that was off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center.' in `source_b.md` -- The source states that the magnetic field was off-center. |
| 18 | The names of Uranian moons follow the established literary naming tradition. | supported | `source_b.md` | 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' in `source_b.md` -- The source describes literary allusions and a continuing naming tradition. |
| 24 | Voyager 2's rings were extremely variable in thickness. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states that the rings were extremely variable in thickness. |
| 25 | Voyager 2's rings were extremely variable in transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states that the rings were extremely variable in transparency. |
| 28 | Voyager 2 passed within about 18,000 miles (29,000 kilometers) of Miranda. | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers),' in `source_b.md` -- The stated distances are approximately 18,000 miles and 29,000 kilometers. |
| 30 | Images of Miranda showed an object. | supported | `source_b.md` | 'Images of the moon showed a strange object' in `source_b.md` -- The source directly states that images of Miranda showed an object. |
| 31 | Uranus appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- The source states this directly. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **33** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **31**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 8 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
- `a7` (`source_a.md`) — numeric '1968' (at) does not survive into the merge unchanged
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

The merge declared **12** departure(s) from its sources. Checking them confirms 2, rejects 10, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `b1` | duplicate | The base title is retained; this identical title is a duplicate. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `a2` | reworded | The mission slot corrects the spacecraft and encounter history. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back CONTRADICTED (`A-001`, `A-002`) |
| `a3` | reworded | The Jupiter-planning statement is retained with its wording unchanged. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-004 came back CONTRADICTED (`A-004`) |
| `a4` | reworded | The trajectory slot corrects Saturn to Neptune and retains the study duration. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED (`A-005`) |
| `a5` | reworded | The observation slot corrects the spacecraft and date. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a6` | reworded | The light-conditions statement is retained with its wording unchanged. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-010`) |
| `a7` | reworded | The encounter slot corrects the date, time zone, and unit pairing. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b2` | reworded | The discoveries slot corrects counts, names, field details, and naming history. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back PARTIAL, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED, B-007 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`, `B-005`, `B-006`, `B-007`) |
| `b3` | reworded | The atmosphere slot corrects the conversion and the lake claim. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-009 came back CONTRADICTED, B-010 came back CONTRADICTED (`B-009`, `B-010`) |
| `b5` | reworded | The moon-photography slot corrects the moon names. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-012 came back CONTRADICTED, B-013 came back CONTRADICTED (`B-012`, `B-013`) |
| `b6` | reworded | The Miranda slot corrects the distance and travel duration. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-014 came back CONTRADICTED, B-015 came back CONTRADICTED (`B-014`, `B-015`) |
| `b9` | reworded | The Challenger slot corrects the date, crew count, and timing. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-018 came back CONTRADICTED, B-019 came back CONTRADICTED (`B-018`, `B-019`) |

## Added from outside the documents

The merge declared 11 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

11 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| After completing its primary mission goals with the Jupiter and Saturn encounters, Voyager 2 continued to Uranus, a journey that took about 4,5 years. | Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years. | the model's own knowledge | *no source* | Voyager 2 made the Jupiter, Saturn, and Uranus encounters. | *none* |
| The Uranus encounter’s geometry also allowed for a possible onward encounter with Neptune. | The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn: | the model's own knowledge | *no source* | Voyager 2’s Uranus trajectory enabled its later Neptune encounter. | *none* |
| Voyager 2, the first human-made object to fly past Uranus, began close-range observations on Jan. 24, 1986; signals took approximately 2,5 hours to reach Earth. | The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987, | the model's own knowledge | *no source* | Voyager 2’s Uranus flyby occurred on Jan. 24, 1986. | *none* |
| Closest approach took place at 17:59 UTC on Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles). | the model's own knowledge | *no source* | The date and distance-unit pairing are known for the Uranus encounter. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons and two new rings, bringing the known ring total to 11, and measured a magnetic field tilted at 59 degrees off-axis and off-center. | During its flyby, Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center. | the model's own knowledge | *no source* | Voyager 2 found 10 new moons and two rings; the field tilt is 59 degrees. | *none* |
| The moons’ names follow the established literary naming tradition for Uranian moons, drawing on Shakespeare and Alexander Pope; the names include Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | obvious allusions to Goethe, continuing a naming tradition begun in 1687 | the model's own knowledge | *no source* | The Uranian moon names draw on Shakespeare and Alexander Pope. | *none* |
| The spacecraft measured wind speeds in Uranus’ atmosphere as high as 450 km/h (450,000 meters per hour). | The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour) | the model's own knowledge | *no source* | 450 km/h equals 450,000 meters per hour. | *none* |
| It found no boiling lake of water beneath the cloud tops. | and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | the model's own knowledge | *no source* | Voyager 2 did not find a subsurface boiling lake on Uranus. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ smaller moons. | Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons. | the model's own knowledge | *no source* | The moon names are Ariel, Umbriel, and Titania. | *none* |
| It passed within about 18,000 miles (29,000 kilometers) of Miranda, its closest approach to any object during its nearly nine-year journey. | In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels. | the model's own knowledge | *no source* | The Miranda encounter was about 29,000 kilometers into the mission. | *none* |
| The Uranus encounter’s news was soon overshadowed by the Challenger disaster, which killed seven astronauts when the space shuttle broke apart during launch on Jan. 28, 1986. | The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986. | the model's own knowledge | *no source* | The Challenger disaster occurred on Jan. 28, 1986, and killed seven crew members | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-luna |
| Model (decompose) | gpt-6-luna |
| Model (verify) | gpt-6-luna |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | 21,628 in, 28,152 out, 0 cached, 17,889 reasoning |
| Cost | ~$0.02 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 210.4s |
| Generated | 2026-09-27T17:05:23+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
