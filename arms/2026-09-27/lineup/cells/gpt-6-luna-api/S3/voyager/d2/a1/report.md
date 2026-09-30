## Verdict

**64 finding(s).** In the claims: 4 dropped, 1 partially dropped, 43 contradicted, 6 hallucinated, 1 partially invented. In the structure: 9 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 46 |
| Claims extracted from `source_a.md` | 14 |
| Claims extracted from `source_b.md` | 20 |
| Forward — source claims accounted for in the merge | **8/34** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **4/14** |
| Forward — `source_b.md` claims accounted for | **4/20** (1 in part) |
| Reverse — merge claims found in a source | **17/46** |
| Reverse — supported only in part | 1 |
| Evidence grounded | **70/70** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **A-002** (`source_a.md:3`) — Voyager 3 had three planetary encounters.
  - judged against: `merged.md`
  - rationale: The reference does not state that Voyager 3 had three planetary encounters.
- **A-010** (`source_a.md:9`) — Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - judged against: `merged.md`
  - rationale: The reference does not state when Voyager 1's short-range observations of Uranus began.
- **B-003** (`source_b.md:3`) — The listed names are allusions to Goethe.
  - judged against: `merged.md`
  - rationale: The reference does not say the listed names are allusions to Goethe.
- **B-004** (`source_b.md:3`) — The naming tradition began in 1687.
  - judged against: `merged.md`
  - rationale: The reference does not state when a naming tradition began.

### Partly dropped — the merge carries some of this claim

- **B-017** (`source_b.md:9`) — The Challenger accident occurred on the same day as the Uranus encounter news.
  - evidence: 'News coverage of the Uranus encounter was interrupted by the Challenger disaster' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference says the disaster interrupted coverage, but does not establish that it occurred on the same day as the Uranus encounter news.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals.
  - `merged.md` says: 'After Voyager 2 completed its primary mission goals at Jupiter and Saturn, mission planners directed the spacecraft to Uranus—a journey of about 4,5 years.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes completion of the primary mission goals to Voyager 2, not Voyager 3.
- **A-003** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'After Voyager 2 completed its primary mission goals at Jupiter and Saturn, mission planners directed the spacecraft to Uranus—a journey of about 4,5 years.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Voyager 2, rather than Voyager 3, was directed to Uranus.
- **A-005** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part.
  - `merged.md` says: 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text attributes the optimized Jupiter encounter to Voyager 2, not Voyager 3.
- **A-007** -- the two documents disagree
  - `source_a.md:7` says: The Ur anus encounter’s geometry was defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter geometry also allowed a later encounter with Neptune.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text names Neptune, not Saturn, as the later encounter enabled by the geometry.
- **A-009** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2, the first human-made object to fly past Uranus,' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference identifies Voyager 2, not Voyager 1, as the first human-made object to fly past Uranus.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Light conditions were five-hundred times less than terrestrial conditions.
  - `merged.md` says: 'Sunlight at Uranus was about 1/400 as intense as at Earth.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives sunlight intensity as about 1/400 of Earth's, not one five-hundredth.
- **A-013** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'made its closest approach at 17:59 UT on Jan. 24, 1986,' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives the date as Jan. 24, 1986, and the time as 17:59 UT, not 1968 and ED.
- **A-014** -- the two documents disagree
  - `source_a.md:9` says: Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'at a range of about 81,500 kilometers (50,640 miles).' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference assigns 81,500 to kilometers and 50,640 to miles, the reverse of the claim.
- **B-001** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons: Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says Voyager 2 discovered 10 new moons, not 11.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: The 11 new moons discovered by Voyager 2 were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II.
  - `merged.md` says: 'Voyager 2 discovered 10 new moons: Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 10 moons and lists names that differ from those in the claim.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings.
  - `merged.md` says: 'It discovered two new rings, bringing Uranus’ known total to 11,' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says Voyager 2 discovered two new rings, not three.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Uranus had eight “older” rings.
  - `merged.md` says: 'It discovered two new rings, bringing Uranus’ known total to 11,' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: Two new rings bringing the known total to 11 implies nine older rings, not eight.
- **B-007** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center.
  - `merged.md` says: 'found a magnetic field tilted at 59 degrees off-axis and off-center.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives the tilt as 59 degrees, not 66 degrees.
- **B-008** -- the two documents disagree
  - `source_b.md:5` says: Wind speeds in Uranus’ atmosphere reached as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (450000 meters per hour).' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 450000 meters per hour, not 72400 meters per hour.
- **B-009** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.
  - `merged.md` says: 'Voyager 2 did not find a boiling lake of water beneath the cloud tops.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference explicitly says Voyager 2 did not find a boiling lake of water.
- **B-011** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan.
  - `merged.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, and Umbriel, four of Uranus’ smaller moons. Titan is a moon of Saturn, not Uranus.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference lists Ariel and Umbriel rather than Ariele and Umbrella, and identifies Titan as a moon of Saturn.
- **B-012** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus’ smaller moons.
  - `merged.md` says: 'Titan is a moon of Saturn, not Uranus.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim includes Titan among Uranus’ moons, but the reference explicitly identifies Titan as a moon of Saturn, not Uranus.
- **B-014** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 came closer to Miranda than to any other object so far in its nearly century-long travels.
  - `merged.md` says: 'its nearly decade-long travels' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference describes Voyager 2’s travels as nearly a decade long, not nearly a century long.
- **B-018** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'killed seven astronauts during the space shuttle launch.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference states that the Challenger disaster killed seven astronauts, not six.
- **B-019** -- the two documents disagree
  - `source_b.md:9` says: The six astronauts were killed during their space shuttle launch.
  - `merged.md` says: 'killed seven astronauts during the space shuttle launch.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives seven as the number of astronauts killed, not six.
- **B-020** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred Feb. 28, 1986.
  - `merged.md` says: 'which occurred on Jan. 28, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives the Challenger disaster date as Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 was the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987," (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus.
- **M-002** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 made its closest approach to Uranus at 17:59 UT on Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968,' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives Jan. 24, 1968, rather than Jan. 24, 1986.
- **M-003** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 made its closest approach to Uranus at a range of about 81,500 kilometers (50,640 miles).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles).' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source assigns 50,640 to kilometers and 81,500 to miles, the reverse of the claim.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: Sunlight at Uranus was about 1/400 as intense as at Earth.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives light conditions as five-hundred times less than terrestrial conditions, not about 1/400 as intense.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: The Uranus encounter geometry allowed a later encounter with Neptune.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn:' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names a possible future encounter with Saturn, not Neptune.
- **M-012** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered 10 new moons during its flyby.
  - `source_b.md` says: 'During its flyby, Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says Voyager 2 discovered 11 new moons, not 10.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered Puck during its flyby.
  - `source_b.md` says: 'given such names as Pucka,' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the name Pucka, not Puck.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered Portia during its flyby.
  - `source_b.md` says: 'Portila,' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the name Portila, not Portia.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered Juliet during its flyby.
  - `source_b.md` says: 'Juliette,' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the name Juliette, not Juliet.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered Cressida during its flyby.
  - `source_b.md` says: 'Kressida,' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the name Kressida, not Cressida.
- **M-017** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered Rosalind during its flyby.
  - `source_b.md` says: 'Rosalinde,' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the name Rosalinde, not Rosalind.
- **M-020** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered Cordelia during its flyby.
  - `source_b.md` says: 'Cordelina,' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the name Cordelina, not Cordelia.
- **M-022** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered Bianca during its flyby.
  - `source_b.md` says: 'Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the name Bianca II, not Bianca.
- **M-023** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovered two new rings.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings,' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says Voyager 2 discovered three new rings, not two.
- **M-025** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 found a magnetic field tilted at 59 degrees off-axis.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives the tilt as 66 degrees, not 59 degrees.
- **M-027** -- the two documents disagree
  - `merged.md:7` says: Wind speeds in Uranus’ atmosphere reached as high as 450 km/h (450000 meters per hour).
  - `source_b.md` says: 'The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives 72400 meters per hour, not 450000 meters per hour.
- **M-028** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 did not find a boiling lake of water beneath Uranus’ cloud tops.
  - `source_b.md` says: 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says Voyager 2 found evidence of a boiling lake beneath the cloud surface.
- **M-036** -- the two documents disagree
  - `merged.md:9` says: Titan is a moon of Saturn.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies Titan as one of Uranus’ smaller moons, not a moon of Saturn.
- **M-037** -- the two documents disagree
  - `merged.md:9` says: Titan is not a moon of Uranus.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies Titan as one of Uranus’ smaller moons, contradicting the claim that it is not a moon of Uranus.
- **M-038** -- the two documents disagree
  - `merged.md:9` says: The Miranda flyby was Voyager 2’s closest approach to any object in its nearly decade-long travels.
  - `source_b.md` says: 'the spacecraft came closest to any object so far in its nearly century-long travels.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source describes the travels as nearly century-long, not nearly decade-long.
- **M-043** -- the two documents disagree
  - `merged.md:11` says: The Challenger disaster occurred on Jan. 28, 1986.
  - `source_b.md` says: 'Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the Challenger accident Feb. 28, 1986, not Jan. 28, 1986.
- **M-045** -- the two documents disagree
  - `merged.md:11` says: The Challenger disaster killed seven astronauts.
  - `source_b.md` says: 'that killed six astronauts during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the disaster killed six astronauts, not seven.

### Invented — in the merge, in neither source

- **M-006** (`merged.md:5`) — Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source says “its encounter” with Jupiter was optimized but does not identify that spacecraft as Voyager 2.
- **M-007** (`merged.md:5`) — Voyager 2 completed its primary mission goals at Jupiter and Saturn.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source says Voyager 3 fulfilled its primary mission goals with three planetary encounters; it does not state that Voyager 2 completed goals at Jupiter and Saturn.
- **M-008** (`merged.md:5`) — Mission planners directed Voyager 2 to Uranus.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source says mission planners directed the veteran spacecraft to Uranus but does not identify it as Voyager 2.
- **M-033** (`merged.md:9`) — Voyager 2 returned photos of Ariel.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source names “Ariele,” not Ariel, and does not otherwise state that Voyager 2 returned photos of Ariel.
- **M-034** (`merged.md:9`) — Voyager 2 returned photos of Umbriel.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source names “Umbrella,” not Umbriel, and does not otherwise state that Voyager 2 returned photos of Umbriel.
- **M-044** (`merged.md:11`) — The Challenger disaster occurred four days after Voyager 2’s closest approach.
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The sources do not state when Voyager 2’s closest approach occurred in relation to the Challenger disaster.

### Partly invented — the sources carry some of this claim

- **M-035** (`merged.md:9`) — Miranda, Oberon, Ariel, and Umbriel are four of Uranus’ smaller moons.
  - evidence: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source supports Miranda and Oberon as smaller moons, but names the other two as “Ariele” and “Umbrella,” not Ariel and Umbriel.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 6.4 | 2,5, 4,5 | English (65 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m3` (`merged.md`) - '2,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **other convention** `m6` (`merged.md`) - '4,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **readable two ways** `m16` (`merged.md`) - '17.560' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `m16` (`merged.md`) - '28.260' (merged.md, line 9) can be read two ways: this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call

## Length capped

- `$.additions[11].reason` was 82 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 14 claim(s): 2 dropped, 8 contradicted, 0 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | Voyager 3 had three planetary encounters. | 3 | dropped | The reference does not state that Voyager 3 had three planetary encounters. |
| 10 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | dropped | The reference does not state when Voyager 1's short-range observations of Uranus began. |
| 1 | Voyager 3 had fulfilled its primary mission goals. | 3 | contradicted | 'After Voyager 2 completed its primary mission goals at Jupiter and Saturn, mission planners directed the spacecraft to Uranus—a journey of about 4,5 years.' in `merged.md` -- The text attributes completion of the primary mission goals to Voyager 2, not Voyager 3. |
| 3 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'After Voyager 2 completed its primary mission goals at Jupiter and Saturn, mission planners directed the spacecraft to Uranus—a journey of about 4,5 years.' in `merged.md` -- The text says Voyager 2, rather than Voyager 3, was directed to Uranus. |
| 5 | Voyager 3's encounter with Jupiter was optimized in part. | 5 | contradicted | 'In fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `merged.md` -- The text attributes the optimized Jupiter encounter to Voyager 2, not Voyager 3. |
| 7 | The Ur anus encounter’s geometry was defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter geometry also allowed a later encounter with Neptune.' in `merged.md` -- The text names Neptune, not Saturn, as the later encounter enabled by the geometry. |
| 9 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2, the first human-made object to fly past Uranus,' in `merged.md` -- The reference identifies Voyager 2, not Voyager 1, as the first human-made object to fly past Uranus. |
| 12 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | contradicted | 'Sunlight at Uranus was about 1/400 as intense as at Earth.' in `merged.md` -- The reference gives sunlight intensity as about 1/400 of Earth's, not one five-hundredth. |
| 13 | Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'made its closest approach at 17:59 UT on Jan. 24, 1986,' in `merged.md` -- The reference gives the date as Jan. 24, 1986, and the time as 17:59 UT, not 1968 and ED. |
| 14 | Closest approach to Uranus took place at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'at a range of about 81,500 kilometers (50,640 miles).' in `merged.md` -- The reference assigns 81,500 to kilometers and 50,640 to miles, the reverse of the claim. |
| 4 | The journey to Uranus would take about 4,5 years. | 3 | carried | 'a journey of about 4,5 years' in `merged.md` -- The reference gives the journey to Uranus as about 4,5 years. |
| 6 | Future planetary flybys would be possible. | 5 | carried | 'future planetary flybys would be possible' in `merged.md` -- The text explicitly says future planetary flybys would be possible. |
| 8 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | carried | 'Voyager 1 had only 6.4 days of close study during its Saturn flyby.' in `merged.md` -- The reference states Voyager 1 had only 6.4 days of close study during its Saturn flyby. |
| 11 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'Radio signals took approximately 2,5 hours to reach Earth.' in `merged.md` -- The text gives the signal travel time as approximately 2,5 hours. |

### `source_b.md` -- 20 claim(s): 2 dropped, 13 contradicted, 1 carried in part, 4 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 3 | The listed names are allusions to Goethe. | 3 | dropped | The reference does not say the listed names are allusions to Goethe. |
| 4 | The naming tradition began in 1687. | 3 | dropped | The reference does not state when a naming tradition began. |
| 1 | Voyager 2 discovered 11 new moons during its flyby. | 3 | contradicted | 'Voyager 2 discovered 10 new moons: Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.' in `merged.md` -- The reference says Voyager 2 discovered 10 new moons, not 11. |
| 2 | The 11 new moons discovered by Voyager 2 were given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II. | 3 | contradicted | 'Voyager 2 discovered 10 new moons: Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca.' in `merged.md` -- The reference gives 10 moons and lists names that differ from those in the claim. |
| 5 | Voyager 2 discovered three new rings. | 3 | contradicted | 'It discovered two new rings, bringing Uranus’ known total to 11,' in `merged.md` -- The reference says Voyager 2 discovered two new rings, not three. |
| 6 | Uranus had eight “older” rings. | 3 | contradicted | 'It discovered two new rings, bringing Uranus’ known total to 11,' in `merged.md` -- Two new rings bringing the known total to 11 implies nine older rings, not eight. |
| 7 | Voyager 2 discovered a magnetic field tilted at 66 degrees off-axis and off-center. | 3 | contradicted | 'found a magnetic field tilted at 59 degrees off-axis and off-center.' in `merged.md` -- The reference gives the tilt as 59 degrees, not 66 degrees. |
| 8 | Wind speeds in Uranus’ atmosphere reached as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (450000 meters per hour).' in `merged.md` -- The reference gives 450000 meters per hour, not 72400 meters per hour. |
| 9 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface. | 5 | contradicted | 'Voyager 2 did not find a boiling lake of water beneath the cloud tops.' in `merged.md` -- The reference explicitly says Voyager 2 did not find a boiling lake of water. |
| 11 | Voyager 2 returned photos of Miranda, Oberon, Ariele, Umbrella, and Titan. | 7 | contradicted | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, and Umbriel, four of Uranus’ smaller moons. Titan is a moon of Saturn, not Uranus.' in `merged.md` -- The reference lists Ariel and Umbriel rather than Ariele and Umbrella, and identifies Titan as a moon of Saturn. |
| 12 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus’ smaller moons. | 7 | contradicted | 'Titan is a moon of Saturn, not Uranus.' in `merged.md` -- The claim includes Titan among Uranus’ moons, but the reference explicitly identifies Titan as a moon of Saturn, not Uranus. |
| 14 | Voyager 2 came closer to Miranda than to any other object so far in its nearly century-long travels. | 7 | contradicted | 'its nearly decade-long travels' in `merged.md` -- The reference describes Voyager 2’s travels as nearly a decade long, not nearly a century long. |
| 18 | The Challenger accident killed six astronauts. | 9 | contradicted | 'killed seven astronauts during the space shuttle launch.' in `merged.md` -- The reference states that the Challenger disaster killed seven astronauts, not six. |
| 19 | The six astronauts were killed during their space shuttle launch. | 9 | contradicted | 'killed seven astronauts during the space shuttle launch.' in `merged.md` -- The reference gives seven as the number of astronauts killed, not six. |
| 20 | The Challenger accident occurred Feb. 28, 1986. | 9 | contradicted | 'which occurred on Jan. 28, 1986' in `merged.md` -- The reference gives the Challenger disaster date as Jan. 28, 1986, not Feb. 28, 1986. |
| 17 | The Challenger accident occurred on the same day as the Uranus encounter news. | 9 | carried in part | 'News coverage of the Uranus encounter was interrupted by the Challenger disaster' in `merged.md` -- The reference says the disaster interrupted coverage, but does not establish that it occurred on the same day as the Uranus encounter news. |
| 10 | Voyager 2’s rings were extremely variable in thickness and transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency.' in `merged.md` -- The reference states that the rings were extremely variable in thickness and transparency. |
| 13 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | carried | 'The Miranda flyby was Voyager 2’s closest approach to any object in its nearly decade-long travels, at a range of only 17.560 miles (28.260 kilometers).' in `merged.md` -- The reference gives the claimed range for Voyager 2’s Miranda flyby. |
| 15 | Images of Miranda showed features on its surface. | 7 | carried | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.' in `merged.md` -- The reference says Miranda’s images showed peculiar surface features. |
| 16 | Uranus appeared generally featureless. | 7 | carried | 'Uranus itself appeared generally featureless.' in `merged.md` -- The reference directly states that Uranus appeared generally featureless. |

### `merged.md` -- 46 claim(s): 6 invented, 22 contradicted, 1 supported in part, 17 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 6 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | invented | -- | The source says “its encounter” with Jupiter was optimized but does not identify that spacecraft as Voyager 2. |
| 7 | Voyager 2 completed its primary mission goals at Jupiter and Saturn. | invented | -- | The source says Voyager 3 fulfilled its primary mission goals with three planetary encounters; it does not state that Voyager 2 completed goals at Jupiter and Saturn. |
| 8 | Mission planners directed Voyager 2 to Uranus. | invented | -- | The source says mission planners directed the veteran spacecraft to Uranus but does not identify it as Voyager 2. |
| 33 | Voyager 2 returned photos of Ariel. | invented | -- | The source names “Ariele,” not Ariel, and does not otherwise state that Voyager 2 returned photos of Ariel. |
| 34 | Voyager 2 returned photos of Umbriel. | invented | -- | The source names “Umbrella,” not Umbriel, and does not otherwise state that Voyager 2 returned photos of Umbriel. |
| 44 | The Challenger disaster occurred four days after Voyager 2’s closest approach. | invented | -- | The sources do not state when Voyager 2’s closest approach occurred in relation to the Challenger disaster. |
| 1 | Voyager 2 was the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987," in `source_a.md` -- The source identifies Voyager 1, not Voyager 2, as the first human-made object to fly past Uranus. |
| 2 | Voyager 2 made its closest approach to Uranus at 17:59 UT on Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968,' in `source_a.md` -- The source gives Jan. 24, 1968, rather than Jan. 24, 1986. |
| 3 | Voyager 2 made its closest approach to Uranus at a range of about 81,500 kilometers (50,640 miles). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles).' in `source_a.md` -- The source assigns 50,640 to kilometers and 81,500 to miles, the reverse of the claim. |
| 5 | Sunlight at Uranus was about 1/400 as intense as at Earth. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- The source gives light conditions as five-hundred times less than terrestrial conditions, not about 1/400 as intense. |
| 10 | The Uranus encounter geometry allowed a later encounter with Neptune. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn:' in `source_a.md` -- The source names a possible future encounter with Saturn, not Neptune. |
| 12 | Voyager 2 discovered 10 new moons during its flyby. | contradicted | `source_b.md` | 'During its flyby, Voyager 2 discovered 11 new moons' in `source_b.md` -- The source says Voyager 2 discovered 11 new moons, not 10. |
| 13 | Voyager 2 discovered Puck during its flyby. | contradicted | `source_b.md` | 'given such names as Pucka,' in `source_b.md` -- The source gives the name Pucka, not Puck. |
| 14 | Voyager 2 discovered Portia during its flyby. | contradicted | `source_b.md` | 'Portila,' in `source_b.md` -- The source gives the name Portila, not Portia. |
| 15 | Voyager 2 discovered Juliet during its flyby. | contradicted | `source_b.md` | 'Juliette,' in `source_b.md` -- The source gives the name Juliette, not Juliet. |
| 16 | Voyager 2 discovered Cressida during its flyby. | contradicted | `source_b.md` | 'Kressida,' in `source_b.md` -- The source gives the name Kressida, not Cressida. |
| 17 | Voyager 2 discovered Rosalind during its flyby. | contradicted | `source_b.md` | 'Rosalinde,' in `source_b.md` -- The source gives the name Rosalinde, not Rosalind. |
| 20 | Voyager 2 discovered Cordelia during its flyby. | contradicted | `source_b.md` | 'Cordelina,' in `source_b.md` -- The source gives the name Cordelina, not Cordelia. |
| 22 | Voyager 2 discovered Bianca during its flyby. | contradicted | `source_b.md` | 'Bianca II' in `source_b.md` -- The source gives the name Bianca II, not Bianca. |
| 23 | Voyager 2 discovered two new rings. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings,' in `source_b.md` -- The source says Voyager 2 discovered three new rings, not two. |
| 25 | Voyager 2 found a magnetic field tilted at 59 degrees off-axis. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center.' in `source_b.md` -- The source gives the tilt as 66 degrees, not 59 degrees. |
| 27 | Wind speeds in Uranus’ atmosphere reached as high as 450 km/h (450000 meters per hour). | contradicted | `source_b.md` | 'The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source gives 72400 meters per hour, not 450000 meters per hour. |
| 28 | Voyager 2 did not find a boiling lake of water beneath Uranus’ cloud tops. | contradicted | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface.' in `source_b.md` -- The source says Voyager 2 found evidence of a boiling lake beneath the cloud surface. |
| 36 | Titan is a moon of Saturn. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source identifies Titan as one of Uranus’ smaller moons, not a moon of Saturn. |
| 37 | Titan is not a moon of Uranus. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source identifies Titan as one of Uranus’ smaller moons, contradicting the claim that it is not a moon of Uranus. |
| 38 | The Miranda flyby was Voyager 2’s closest approach to any object in its nearly decade-long travels. | contradicted | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels.' in `source_b.md` -- The source describes the travels as nearly century-long, not nearly decade-long. |
| 43 | The Challenger disaster occurred on Jan. 28, 1986. | contradicted | `source_b.md` | 'Feb. 28, 1986.' in `source_b.md` -- The source dates the Challenger accident Feb. 28, 1986, not Jan. 28, 1986. |
| 45 | The Challenger disaster killed seven astronauts. | contradicted | `source_b.md` | 'that killed six astronauts during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source says the disaster killed six astronauts, not seven. |
| 35 | Miranda, Oberon, Ariel, and Umbriel are four of Uranus’ smaller moons. | supported in part | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source supports Miranda and Oberon as smaller moons, but names the other two as “Ariele” and “Umbrella,” not Ariel and Umbriel. |
| 4 | Radio signals took approximately 2,5 hours to reach Earth. | supported | `source_a.md` | 'signals took approximately 2,5 hours to reach Earth.' in `source_a.md` -- The source states that signals took approximately 2,5 hours to reach Earth. |
| 9 | The journey to Uranus took about 4,5 years. | supported | `source_a.md` | 'a journey that would take about 4,5 years.' in `source_a.md` -- The source states that the journey to Uranus would take about 4,5 years. |
| 11 | Voyager 1 had only 6.4 days of close study during its Saturn flyby. | supported | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- In context, the source links Voyager 1's close study to the possible future encounter with Saturn. |
| 18 | Voyager 2 discovered Belinda during its flyby. | supported | `source_b.md` | 'Belinda,' in `source_b.md` -- The source lists Belinda among the new moons discovered during the flyby. |
| 19 | Voyager 2 discovered Desdemona during its flyby. | supported | `source_b.md` | 'Desdemona,' in `source_b.md` -- The source lists Desdemona among the new moons discovered during the flyby. |
| 21 | Voyager 2 discovered Ophelia during its flyby. | supported | `source_b.md` | 'Ophelia,' in `source_b.md` -- The source lists Ophelia among the new moons discovered during the flyby. |
| 24 | Uranus’ known total of rings became 11. | supported | `source_b.md` | 'three new rings in addition to the “older” eight rings,' in `source_b.md` -- The source's three new rings and eight older rings together entail a known total of 11. |
| 26 | Voyager 2 found a magnetic field that was off-center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center.' in `source_b.md` -- The source states that the magnetic field was off-center. |
| 29 | Voyager 2 found that Uranus’ rings were extremely variable in thickness. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states that the rings were extremely variable in thickness. |
| 30 | Voyager 2 found that Uranus’ rings were extremely variable in transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source states that the rings were extremely variable in transparency. |
| 31 | Voyager 2 returned photos of Miranda. | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source explicitly says Voyager 2 returned photos of Miranda. |
| 32 | Voyager 2 returned photos of Oberon. | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source explicitly says Voyager 2 returned photos of Oberon. |
| 39 | The Miranda flyby was at a range of only 17.560 miles (28.260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers),' in `source_b.md` -- The source gives the Miranda flyby range as 17.560 miles (28.260 kilometers). |
| 40 | Images of Miranda showed an object. | supported | `source_b.md` | 'Images of the moon showed a strange object' in `source_b.md` -- The source says images of Miranda showed an object. |
| 41 | Uranus itself appeared generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- The source directly states that Uranus appeared generally featureless. |
| 42 | News coverage of the Uranus encounter was interrupted by the Challenger disaster. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- The source says news of the Uranus encounter was interrupted by the Challenger accident. |
| 46 | The Challenger disaster occurred during the space shuttle launch. | supported | `source_b.md` | 'during their space shuttle launch' in `source_b.md` -- The source says the astronauts were killed during their space shuttle launch. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **46** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **34**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 6 attributed segment(s) — sources in blocks, at least one out of its source order. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

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

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **11** departure(s) from its sources. Checking them confirms 2, rejects 9, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | The mission-history sentence corrects the spacecraft and encounter sequence. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back MISSING, A-003 came back CONTRADICTED (`A-001`, `A-002`, `A-003`) |
| `a4` | reworded | The encounter geometry points to Neptune; Voyager 1's Saturn detail remains. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED (`A-007`) |
| `a5` | reworded | The spacecraft and encounter details are corrected in the opening paragraph. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-009 came back CONTRADICTED, A-010 came back MISSING (`A-009`, `A-010`) |
| `a6` | superseded | The illumination figure is corrected to the supported value. | **confirmed** | declared 'superseded' and every claim from it came back SUPPORTED or CONTRADICTED or PARTIAL (`A-012`) |
| `a7` | reworded | The date, time standard, spacecraft, and unit values are corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-013 came back CONTRADICTED, A-014 came back CONTRADICTED (`A-013`, `A-014`) |
| `b1` | duplicate | The identical title is already carried from the base document. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b2` | reworded | The discoveries, names, ring count, and magnetic tilt are corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-001 came back CONTRADICTED, B-002 came back CONTRADICTED, B-003 came back MISSING, B-004 came back MISSING, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED, B-007 came back CONTRADICTED (`B-001`, `B-002`, `B-003`, `B-004`, `B-005`, `B-006`, `B-007`) |
| `b3` | reworded | The conversion is corrected and the unsupported lake claim is replaced. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-008 came back CONTRADICTED, B-009 came back CONTRADICTED (`B-008`, `B-009`) |
| `b5` | reworded | The moon names and Titan's planetary affiliation are corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-011 came back CONTRADICTED, B-012 came back CONTRADICTED (`B-011`, `B-012`) |
| `b6` | reworded | The travel duration is corrected while retaining the stated range. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-014 came back CONTRADICTED (`B-014`) |
| `b9` | reworded | The disaster date, timing, and number of fatalities are corrected. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-017 came back PARTIAL, B-018 came back CONTRADICTED, B-019 came back CONTRADICTED, B-020 came back CONTRADICTED (`B-017`, `B-018`, `B-019`, `B-020`) |

## Added from outside the documents

The merge declared 12 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

12 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| After Voyager 2 completed its primary mission goals at Jupiter and Saturn, mission planners directed the spacecraft to Uranus—a journey of about 4,5 years. | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters | the model's own knowledge | *no source* | Voyager 2 continued to Uranus after its Jupiter and Saturn encounters. | *none* |
| The Uranus encounter geometry also allowed a later encounter with Neptune. | The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn | the model's own knowledge | *no source* | Voyager 2's Uranus trajectory continued onward to Neptune. | *none* |
| Voyager 2, the first human-made object to fly past Uranus, made its closest approach at 17:59 UT on Jan. 24, 1986, at a range of about 81,500 kilometers (50,640 miles). | Voyager 1's short-range observations of the planet began Jan. 31, 1987; 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | Voyager 2's Uranus closest approach occurred on Jan. 24, 1986. | *none* |
| Sunlight at Uranus was about 1/400 as intense as at Earth. | Light conditions were five-hundred times less than terrestrial conditions. | the model's own knowledge | *no source* | Uranus receives roughly one four-hundredth of Earth's sunlight. | *none* |
| During its flyby, Voyager 2 discovered 10 new moons: Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca. | 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II | the model's own knowledge | *no source* | The Voyager 2 flyby discoveries comprise 10 moons with these names. | *none* |
| It discovered two new rings, bringing Uranus’ known total to 11, and found a magnetic field tilted at 59 degrees off-axis and off-center. | three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center | the model's own knowledge | *no source* | The ring total is 11 and the magnetic-axis tilt is 59 degrees. | *none* |
| The spacecraft found wind speeds in Uranus’ atmosphere as high as 450 km/h (450000 meters per hour). | 72400 meters per hour | the model's own knowledge | *no source* | 450 km/h converts to 450000 meters per hour. | *none* |
| Voyager 2 did not find a boiling lake of water beneath the cloud tops. | found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface | the model's own knowledge | *no source* | The Voyager 2 Uranus encounter did not establish such a lake. | *none* |
| Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariel, and Umbriel, four of Uranus’ smaller moons. | Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons | the model's own knowledge | *no source* | Ariel and Umbriel are Uranian moons; Titan is not. | *none* |
| Titan is a moon of Saturn, not Uranus. | Titan, five of Uranus’ smaller moons | the model's own knowledge | *no source* | Titan is a moon of Saturn. | *none* |
| The Miranda flyby was Voyager 2’s closest approach to any object in its nearly decade-long travels, at a range of only 17.560 miles (28.260 kilometers). | came closest to any object so far in its nearly century-long travels | the model's own knowledge | *no source* | Voyager 2's mission lasted nearly a decade, not a century. | *none* |
| News coverage of the Uranus encounter was interrupted by the Challenger disaster, which occurred on Jan. 28, 1986, four days after Voyager 2’s closest approach, and killed seven astronauts during the space shuttle launch. | same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | The disaster occurred Jan. 28, four days after the Uranus flyby, and killed seve | *none* |

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
| Calls | 10 live, 0 cached, 0 replayed |
| Tokens | 27,590 in, 39,930 out, 0 cached, 25,774 reasoning |
| Cost | ~$0.02 estimated (rates read 2026-09-25) |
| Schema repairs | 2 |
| Errors | 0 |
| Duration | 291.8s |
| Generated | 2026-09-27T17:39:53+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
