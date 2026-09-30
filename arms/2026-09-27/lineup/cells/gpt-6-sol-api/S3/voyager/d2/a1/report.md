## Verdict

**82 finding(s).** In the claims: 2 partially dropped, 63 contradicted, 2 partially invented. In the structure: 15 verbatim violation. 8 number-format warning(s), on numerals that could be misread, are listed under Number format below and do not move the exit code.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 47 |
| Claims extracted from `source_a.md` | 12 |
| Claims extracted from `source_b.md` | 36 |
| Forward — source claims accounted for in the merge | **13/48** |
| Forward — carried only in part | 2 |
| Forward — `source_a.md` claims accounted for | **1/12** |
| Forward — `source_b.md` claims accounted for | **12/36** (2 in part) |
| Reverse — merge claims found in a source | **15/47** |
| Reverse — supported only in part | 2 |
| Evidence grounded | **95/95** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-031** (`source_b.md:7`) — Voyager 2 had been traveling for nearly a century at the time of the Miranda flyby.
  - evidence: 'its closest approach to any object during its journey to that point' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference establishes a journey up to the Miranda flyby but does not give a nearly century-long duration.
- **B-034** (`source_b.md:9`) — News of the Uranus encounter was interrupted by the Challenger accident.
  - evidence: 'The Challenger disaster on Jan. 28, 1986, overshadows news of the Uranus encounter' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The disaster overshadowed the news, but the reference does not say the news was interrupted.

### Contradicted — the merge states something different

- **A-001** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3 had fulfilled its primary mission goals with the three planetary encounters.
  - `merged.md` says: 'Voyager 2 completes its primary mission at Jupiter and Saturn' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text identifies Voyager 2, not Voyager 3, and names two planetary encounters.
- **A-002** -- the two documents disagree
  - `source_a.md:3` says: Mission planners directed Voyager 3 to Uranus.
  - `merged.md` says: 'Voyager 2 completes its primary mission at Jupiter and Saturn, then continues to Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The spacecraft continuing to Uranus is Voyager 2, not Voyager 3.
- **A-003** -- the two documents disagree
  - `source_a.md:3` says: Voyager 3's journey to Uranus would take about 4,5 years.
  - `merged.md` says: 'Voyager 2 completes its primary mission at Jupiter and Saturn, then continues to Uranus on a journey of about 4,5 years from Saturn.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated journey belongs to Voyager 2, not Voyager 3.
- **A-004** -- the two documents disagree
  - `source_a.md:5` says: Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `merged.md` says: 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: In context, this describes Voyager 2’s Jupiter encounter, not Voyager 3’s.
- **A-005** -- the two documents disagree
  - `source_a.md:7` says: The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn.
  - `merged.md` says: 'The Uranus encounter’s geometry is also shaped by the possibility of a later Neptune encounter' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The later encounter considered was with Neptune, not Saturn.
- **A-006** -- the two documents disagree
  - `source_a.md:7` says: Voyager 1 had only 6.4 days of close study during its flyby.
  - `merged.md` says: 'leaving Voyager 2 only 5.5 hours of close study during the flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives Voyager 2 a 5.5-hour study period, not Voyager 1 a 6.4-day period.
- **A-007** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1 was the first human-made object to fly past Uranus.
  - `merged.md` says: 'Voyager 2 is the first human-made object to fly past Uranus' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The first human-made object to fly past Uranus is identified as Voyager 2.
- **A-008** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's short-range observations of Uranus began Jan. 31, 1987.
  - `merged.md` says: 'Voyager 2 is the first human-made object to fly past Uranus; its close-range observations begin before the Jan. 24, 1986 flyby' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The observations are attributed to Voyager 2 and began before a January 1986 flyby.
- **A-010** -- the two documents disagree
  - `source_a.md:9` says: Light conditions were five-hundred times less than terrestrial conditions.
  - `merged.md` says: 'Sunlight at Uranus is roughly 400 times fainter than at Earth.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text gives roughly 400 times fainter, rather than five-hundred times.
- **A-011** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's closest approach to Uranus took place at 17:59 ED Jan. 24, 1968.
  - `merged.md` says: 'Closest approach occurs at 17:59 UT Jan. 24, 1986' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated time designation and year differ from the claim, and the context identifies Voyager 2.
- **A-012** -- the two documents disagree
  - `source_a.md:9` says: Voyager 1's closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles).
  - `merged.md` says: 'Closest approach occurs at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers).' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim reverses the distance units and attributes the approach to Voyager 1 rather than Voyager 2.
- **B-002** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered 11 new moons during its flyby of Uranus.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The text says Voyager 2 discovered 10 new moons, not 11.
- **B-003** -- the two documents disagree
  - `source_b.md:3` says: Pucka was among the moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons, including Puck' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed moon is Puck, not Pucka.
- **B-004** -- the two documents disagree
  - `source_b.md:3` says: Portila was among the moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons, including Puck, Portia' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed moon is Portia, not Portila.
- **B-005** -- the two documents disagree
  - `source_b.md:3` says: Juliette was among the moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed moon is Juliet, not Juliette.
- **B-006** -- the two documents disagree
  - `source_b.md:3` says: Kressida was among the moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed moon is Cressida, not Kressida.
- **B-007** -- the two documents disagree
  - `source_b.md:3` says: Rosalinde was among the moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed moon is Rosalind, not Rosalinde.
- **B-010** -- the two documents disagree
  - `source_b.md:3` says: Cordelina was among the moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed moon is Cordelia, not Cordelina.
- **B-012** -- the two documents disagree
  - `source_b.md:3` says: Bianca II was among the moons discovered by Voyager 2.
  - `merged.md` says: 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The listed moon is Bianca, not Bianca II.
- **B-013** -- the two documents disagree
  - `source_b.md:3` says: The listed moon names allude to Goethe.
  - `merged.md` says: 'whose names follow a tradition drawing on Shakespeare and Alexander Pope that begins in 1852' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The naming tradition draws on Shakespeare and Alexander Pope, not Goethe.
- **B-014** -- the two documents disagree
  - `source_b.md:3` says: The moon-naming tradition began in 1687.
  - `merged.md` says: 'whose names follow a tradition drawing on Shakespeare and Alexander Pope that begins in 1852' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference dates the naming tradition to 1852, not 1687.
- **B-015** -- the two documents disagree
  - `source_b.md:3` says: Voyager 2 discovered three new rings at Uranus.
  - `merged.md` says: 'It also discovers two new rings beyond the nine already known' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says Voyager 2 discovered two new rings, not three.
- **B-016** -- the two documents disagree
  - `source_b.md:3` says: Uranus had eight previously known rings.
  - `merged.md` says: 'the nine already known' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says nine rings were previously known, not eight.
- **B-017** -- the two documents disagree
  - `source_b.md:3` says: Uranus has a magnetic field tilted at 66 degrees off-axis.
  - `merged.md` says: 'a magnetic field tilted about 60 degrees from the rotation axis' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The stated tilt is about 60 degrees, rather than 66 degrees.
- **B-019** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour).
  - `merged.md` says: 'The spacecraft measures atmospheric winds as high as 450 miles per hour (724 kilometers per hour)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The claim gives different units and values for the wind speed.
- **B-020** -- the two documents disagree
  - `source_b.md:5` says: Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus.
  - `merged.md` says: 'it does not find evidence of a boiling lake of water beneath the cloud tops' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference explicitly says Voyager 2 did not find that evidence.
- **B-025** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Ariele.
  - `merged.md` says: 'Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The photographed moon is named Ariel, not Ariele.
- **B-026** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Umbrella.
  - `merged.md` says: 'Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The photographed moon is named Umbriel, not Umbrella.
- **B-027** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 returned photos of Titan.
  - `merged.md` says: 'Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The photographed moon is named Titania, not Titan.
- **B-028** -- the two documents disagree
  - `source_b.md:7` says: Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus’ smaller moons.
  - `merged.md` says: 'Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ moons' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference names Ariel, Umbriel, and Titania rather than Ariele, Umbrella, and Titan.
- **B-029** -- the two documents disagree
  - `source_b.md:7` says: Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers).
  - `merged.md` says: 'Voyager 2 passes Miranda at a range of 17,560 miles (28,260 kilometers)' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference gives 17,560 miles and 28,260 kilometers, not the claimed figures with decimal points.
- **B-035** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident killed six astronauts.
  - `merged.md` says: 'kills seven astronauts during launch' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference says seven astronauts died, not six.
- **B-036** -- the two documents disagree
  - `source_b.md:9` says: The Challenger accident occurred during a space shuttle launch Feb. 28, 1986.
  - `merged.md` says: 'The Challenger disaster on Jan. 28, 1986, overshadows news of the Uranus encounter and kills seven astronauts during launch' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference dates the disaster to Jan. 28, 1986, not Feb. 28, 1986.
- **M-001** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 completes its primary mission at Jupiter and Saturn.
  - `source_a.md` says: 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes completion of the primary mission goals to Voyager 3, not Voyager 2.
- **M-004** -- the two documents disagree
  - `merged.md:3` says: Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.
  - `source_a.md` says: 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.\n\nIn fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The Jupiter optimization is attributed to Voyager 3, not Voyager 2.
- **M-005** -- the two documents disagree
  - `merged.md:3` says: The geometry of Voyager 2's Uranus encounter is shaped by the possibility of a later Neptune encounter.
  - `source_a.md` says: 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Saturn, not Neptune, as the possible future encounter shaping the geometry.
- **M-006** -- the two documents disagree
  - `merged.md:3` says: Voyager 2 has only 5.5 hours of close study during the Uranus flyby.
  - `source_a.md` says: 'Voyager 1 had only 6.4 days of close study during its flyby.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives a different spacecraft and a different duration.
- **M-007** -- the two documents disagree
  - `merged.md:5` says: Voyager 2 is the first human-made object to fly past Uranus.
  - `source_a.md` says: "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source identifies Voyager 1 as the first human-made object to fly past Uranus.
- **M-008** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's close-range observations of Uranus begin before the Jan. 24, 1986 flyby.
  - `source_a.md` says: "Voyager 1's short-range observations of the planet began Jan. 31, 1987" (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives a different spacecraft and places the start of short-range observations after Jan. 24, 1986.
- **M-010** -- the two documents disagree
  - `merged.md:5` says: Sunlight at Uranus is roughly 400 times fainter than at Earth.
  - `source_a.md` says: 'Light conditions were five-hundred times less than terrestrial conditions.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives five-hundred times, not roughly 400 times.
- **M-011** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach to Uranus occurs at 17:59 UT Jan. 24, 1986.
  - `source_a.md` says: 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives a different time designation and year.
- **M-012** -- the two documents disagree
  - `merged.md:5` says: Voyager 2's closest approach to Uranus is at a range of about 50,640 miles (81,500 kilometers).
  - `source_a.md` says: 'at a range of about 50,640 kilometers (81,500 miles)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The claim reverses the units attached to the source's two numbers.
- **M-013** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovers 10 new moons.
  - `source_b.md` says: 'Voyager 2 discovered 11 new moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says 11 new moons, not 10.
- **M-014** -- the two documents disagree
  - `merged.md:7` says: Puck is among the new moons Voyager 2 discovers.
  - `source_b.md` says: 'Pucka' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The named moon is Pucka, not Puck.
- **M-015** -- the two documents disagree
  - `merged.md:7` says: Portia is among the new moons Voyager 2 discovers.
  - `source_b.md` says: 'Portila' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The named moon is Portila, not Portia.
- **M-016** -- the two documents disagree
  - `merged.md:7` says: Juliet is among the new moons Voyager 2 discovers.
  - `source_b.md` says: 'Juliette' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The named moon is Juliette, not Juliet.
- **M-017** -- the two documents disagree
  - `merged.md:7` says: Cressida is among the new moons Voyager 2 discovers.
  - `source_b.md` says: 'Kressida' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The named moon is Kressida, not Cressida.
- **M-018** -- the two documents disagree
  - `merged.md:7` says: Rosalind is among the new moons Voyager 2 discovers.
  - `source_b.md` says: 'Rosalinde' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The named moon is Rosalinde, not Rosalind.
- **M-021** -- the two documents disagree
  - `merged.md:7` says: Cordelia is among the new moons Voyager 2 discovers.
  - `source_b.md` says: 'Cordelina' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The named moon is Cordelina, not Cordelia.
- **M-023** -- the two documents disagree
  - `merged.md:7` says: Bianca is among the new moons Voyager 2 discovers.
  - `source_b.md` says: 'Bianca II' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Bianca II, not Bianca.
- **M-024** -- the two documents disagree
  - `merged.md:7` says: The names of the new moons Voyager 2 discovers follow a tradition drawing on Shakespeare and Alexander Pope.
  - `source_b.md` says: 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source attributes the names to Goethe rather than Shakespeare and Alexander Pope.
- **M-025** -- the two documents disagree
  - `merged.md:7` says: The tradition of naming the moons after figures drawn from Shakespeare and Alexander Pope begins in 1852.
  - `source_b.md` says: 'continuing a naming tradition begun in 1687' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the naming tradition to 1687, not 1852.
- **M-026** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 discovers two new rings at Uranus.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says Voyager 2 discovered three new rings, not two.
- **M-027** -- the two documents disagree
  - `merged.md:7` says: Nine rings at Uranus were already known before Voyager 2 discovered two new rings.
  - `source_b.md` says: 'three new rings in addition to the “older” eight rings' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source gives eight previously known rings and three new ones, rather than nine and two.
- **M-029** -- the two documents disagree
  - `merged.md:7` says: Uranus' magnetic field is tilted about 60 degrees from the rotation axis.
  - `source_b.md` says: 'a magnetic field tilted at 66 degrees off-axis and off-center' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source specifies 66 degrees, not about 60 degrees.
- **M-031** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 measures atmospheric winds at Uranus as high as 450 miles per hour (724 kilometers per hour).
  - `source_b.md` says: 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source assigns kilometers per hour, not miles per hour, to 450 and does not give 724 kilometers per hour.
- **M-032** -- the two documents disagree
  - `merged.md:7` says: Voyager 2 does not find evidence of a boiling lake of water beneath Uranus' cloud tops.
  - `source_b.md` says: 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says the spacecraft did find such evidence.
- **M-037** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returns photographs of Ariel.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Ariele, not Ariel, among the photographed moons.
- **M-038** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returns photographs of Umbriel.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Umbrella, not Umbriel, among the photographed moons.
- **M-039** -- the two documents disagree
  - `merged.md:9` says: Voyager 2 returns photographs of Titania.
  - `source_b.md` says: 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source names Titan, not Titania, among the photographed moons.
- **M-040** -- the two documents disagree
  - `merged.md:9` says: Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' moons.
  - `source_b.md` says: 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: Although Miranda and Oberon match, the source gives Ariele, Umbrella, and Titan instead of Ariel, Umbriel, and Titania.
- **M-045** -- the two documents disagree
  - `merged.md:11` says: The Challenger disaster occurs on Jan. 28, 1986.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source dates the accident Feb. 28, 1986, rather than Jan. 28, 1986.
- **M-047** -- the two documents disagree
  - `merged.md:11` says: The Challenger disaster kills seven astronauts during launch.
  - `source_b.md` says: 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - why this was read as a contradiction: The source says six astronauts were killed, not seven.

### Partly invented — the sources carry some of this claim

- **M-003** (`merged.md:3`) — Voyager 2's journey from Saturn to Uranus takes about 4,5 years.
  - evidence: 'mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.' in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The source gives the duration of a journey to Uranus but attributes it to Voyager 3 and does not specify Saturn as its starting point.
- **M-009** (`merged.md:5`) — Signals from Voyager 2 at Uranus take approximately 2,5 hours to reach Earth.
  - evidence: "Voyager 1's short-range observations of the planet began Jan. 31, 1987, when signals took approximately 2,5 hours to reach Earth." in `source_a.md` (grounded)
  - judged against: `source_a.md` and `source_b.md`
  - rationale: The signal travel time is supported, but the passage attributes it to Voyager 1 rather than Voyager 2.

## Number format

Each document's decimal convention is decided from its own numerals that can only be read one way, when they all agree; otherwise from its language (English writes a decimal point, German a decimal comma); otherwise from the majority of its numerals; and on a tie with no language, not at all. A numeral written in the other convention is listed, as is a separator before exactly three digits that the document's own convention reads as a fraction (17.560 under a decimal point), because the other convention reads it as thousands. A document whose numerals all use the convention its language does not write is listed once, naming them. Only a merged numeral that states a settled source value differently is a fault; every other row is a warning, and none of them moves the exit code. No number was rewritten and no model was asked.

| document | convention | decided by | votes, decimal point | votes, decimal comma | language (stop words en / de) |
|---|---|---|---|---|---|
| `source_a.md` | decimal point | language | 6.4 | 4,5, 2,5 | English (29 / 0) |
| `source_b.md` | decimal point | language | none | none | English (43 / 0) |
| `merged.md` | decimal point | language | 5.5 | 4,5, 2,5 | English (70 / 0) |

### Warnings

- **other convention** `a2` (`source_a.md`) - '4,5' (source_a.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `a5` (`source_a.md`) - '2,5' (source_a.md, line 9) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **readable two ways** `b6` (`source_b.md`) - '17.560' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 17.56, a three-place fraction; in the decimal comma convention it is 17560. Which is meant is the author's call
- **readable two ways** `b6` (`source_b.md`) - '28.260' (source_b.md, line 7) can be read two ways: this document uses the decimal point, decided by its language, English (0 numeral(s) voting decimal point, 0 decimal comma), and reads it 28.26, a three-place fraction; in the decimal comma convention it is 28260. Which is meant is the author's call
- **other convention** `m2` (`merged.md`) - '4,5' (merged.md, line 3) is written in the decimal comma convention, where it reads 4.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 45
- **other convention** `m5` (`merged.md`) - '2,5' (merged.md, line 5) is written in the decimal comma convention, where it reads 2.5; this document uses the decimal point, decided by its language, English (1 numeral(s) voting decimal point, 2 decimal comma), and a reader of that convention takes it for 25
- **reading resolved by the merge** `m13` (`source_b.md`) - source_b.md writes '17.560' beside 'miles' (line 7), which reads 17.56 in its decimal point convention; the merge writes '17,560' (line 9), which reads 17560 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  Voyager 2 passes Miranda at a range of 17,560 miles (28,260 kilometers), its closest approach to any object during its journey to that point.
  ```
- **reading resolved by the merge** `m13` (`source_b.md`) - source_b.md writes '28.260' beside 'kilometers' (line 7), which reads 28.26 in its decimal point convention; the merge writes '28,260' (line 9), which reads 28260 in its own decimal point convention, 1,000 times larger: a value that document itself left open, so the merge took its other reading

  ```text
  In the source: In flying by Miranda at a range of only 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels.
  In the merge:  Voyager 2 passes Miranda at a range of 17,560 miles (28,260 kilometers), its closest approach to any object during its journey to that point.
  ```

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 12 claim(s): 0 dropped, 11 contradicted, 0 carried in part, 1 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters. | 3 | contradicted | 'Voyager 2 completes its primary mission at Jupiter and Saturn' in `merged.md` -- The text identifies Voyager 2, not Voyager 3, and names two planetary encounters. |
| 2 | Mission planners directed Voyager 3 to Uranus. | 3 | contradicted | 'Voyager 2 completes its primary mission at Jupiter and Saturn, then continues to Uranus' in `merged.md` -- The spacecraft continuing to Uranus is Voyager 2, not Voyager 3. |
| 3 | Voyager 3's journey to Uranus would take about 4,5 years. | 3 | contradicted | 'Voyager 2 completes its primary mission at Jupiter and Saturn, then continues to Uranus on a journey of about 4,5 years from Saturn.' in `merged.md` -- The stated journey belongs to Voyager 2, not Voyager 3. |
| 4 | Voyager 3's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | 5 | contradicted | 'its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible' in `merged.md` -- In context, this describes Voyager 2’s Jupiter encounter, not Voyager 3’s. |
| 5 | The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn. | 7 | contradicted | 'The Uranus encounter’s geometry is also shaped by the possibility of a later Neptune encounter' in `merged.md` -- The later encounter considered was with Neptune, not Saturn. |
| 6 | Voyager 1 had only 6.4 days of close study during its flyby. | 7 | contradicted | 'leaving Voyager 2 only 5.5 hours of close study during the flyby' in `merged.md` -- The text gives Voyager 2 a 5.5-hour study period, not Voyager 1 a 6.4-day period. |
| 7 | Voyager 1 was the first human-made object to fly past Uranus. | 9 | contradicted | 'Voyager 2 is the first human-made object to fly past Uranus' in `merged.md` -- The first human-made object to fly past Uranus is identified as Voyager 2. |
| 8 | Voyager 1's short-range observations of Uranus began Jan. 31, 1987. | 9 | contradicted | 'Voyager 2 is the first human-made object to fly past Uranus; its close-range observations begin before the Jan. 24, 1986 flyby' in `merged.md` -- The observations are attributed to Voyager 2 and began before a January 1986 flyby. |
| 10 | Light conditions were five-hundred times less than terrestrial conditions. | 9 | contradicted | 'Sunlight at Uranus is roughly 400 times fainter than at Earth.' in `merged.md` -- The text gives roughly 400 times fainter, rather than five-hundred times. |
| 11 | Voyager 1's closest approach to Uranus took place at 17:59 ED Jan. 24, 1968. | 9 | contradicted | 'Closest approach occurs at 17:59 UT Jan. 24, 1986' in `merged.md` -- The stated time designation and year differ from the claim, and the context identifies Voyager 2. |
| 12 | Voyager 1's closest approach to Uranus was at a range of about 50,640 kilometers (81,500 miles). | 9 | contradicted | 'Closest approach occurs at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers).' in `merged.md` -- The claim reverses the distance units and attributes the approach to Voyager 1 rather than Voyager 2. |
| 9 | Signals took approximately 2,5 hours to reach Earth. | 9 | carried | 'signals taking approximately 2,5 hours to reach Earth' in `merged.md` -- The text states the claimed signal travel time. |

### `source_b.md` -- 36 claim(s): 0 dropped, 22 contradicted, 2 carried in part, 12 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 2 | Voyager 2 discovered 11 new moons during its flyby of Uranus. | 3 | contradicted | 'Voyager 2 discovers 10 new moons' in `merged.md` -- The text says Voyager 2 discovered 10 new moons, not 11. |
| 3 | Pucka was among the moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons, including Puck' in `merged.md` -- The listed moon is Puck, not Pucka. |
| 4 | Portila was among the moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons, including Puck, Portia' in `merged.md` -- The listed moon is Portia, not Portila. |
| 5 | Juliette was among the moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet' in `merged.md` -- The listed moon is Juliet, not Juliette. |
| 6 | Kressida was among the moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida' in `merged.md` -- The listed moon is Cressida, not Kressida. |
| 7 | Rosalinde was among the moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind' in `merged.md` -- The listed moon is Rosalind, not Rosalinde. |
| 10 | Cordelina was among the moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia' in `merged.md` -- The listed moon is Cordelia, not Cordelina. |
| 12 | Bianca II was among the moons discovered by Voyager 2. | 3 | contradicted | 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca' in `merged.md` -- The listed moon is Bianca, not Bianca II. |
| 13 | The listed moon names allude to Goethe. | 3 | contradicted | 'whose names follow a tradition drawing on Shakespeare and Alexander Pope that begins in 1852' in `merged.md` -- The naming tradition draws on Shakespeare and Alexander Pope, not Goethe. |
| 14 | The moon-naming tradition began in 1687. | 3 | contradicted | 'whose names follow a tradition drawing on Shakespeare and Alexander Pope that begins in 1852' in `merged.md` -- The reference dates the naming tradition to 1852, not 1687. |
| 15 | Voyager 2 discovered three new rings at Uranus. | 3 | contradicted | 'It also discovers two new rings beyond the nine already known' in `merged.md` -- The reference says Voyager 2 discovered two new rings, not three. |
| 16 | Uranus had eight previously known rings. | 3 | contradicted | 'the nine already known' in `merged.md` -- The reference says nine rings were previously known, not eight. |
| 17 | Uranus has a magnetic field tilted at 66 degrees off-axis. | 3 | contradicted | 'a magnetic field tilted about 60 degrees from the rotation axis' in `merged.md` -- The stated tilt is about 60 degrees, rather than 66 degrees. |
| 19 | Voyager 2 found wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour). | 5 | contradicted | 'The spacecraft measures atmospheric winds as high as 450 miles per hour (724 kilometers per hour)' in `merged.md` -- The claim gives different units and values for the wind speed. |
| 20 | Voyager 2 found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface of Uranus. | 5 | contradicted | 'it does not find evidence of a boiling lake of water beneath the cloud tops' in `merged.md` -- The reference explicitly says Voyager 2 did not find that evidence. |
| 25 | Voyager 2 returned photos of Ariele. | 7 | contradicted | 'Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The photographed moon is named Ariel, not Ariele. |
| 26 | Voyager 2 returned photos of Umbrella. | 7 | contradicted | 'Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The photographed moon is named Umbriel, not Umbrella. |
| 27 | Voyager 2 returned photos of Titan. | 7 | contradicted | 'Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- The photographed moon is named Titania, not Titan. |
| 28 | Miranda, Oberon, Ariele, Umbrella, and Titan are five of Uranus’ smaller moons. | 7 | contradicted | 'Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ moons' in `merged.md` -- The reference names Ariel, Umbriel, and Titania rather than Ariele, Umbrella, and Titan. |
| 29 | Voyager 2 flew by Miranda at a range of only 17.560 miles (28.260 kilometers). | 7 | contradicted | 'Voyager 2 passes Miranda at a range of 17,560 miles (28,260 kilometers)' in `merged.md` -- The reference gives 17,560 miles and 28,260 kilometers, not the claimed figures with decimal points. |
| 35 | The Challenger accident killed six astronauts. | 9 | contradicted | 'kills seven astronauts during launch' in `merged.md` -- The reference says seven astronauts died, not six. |
| 36 | The Challenger accident occurred during a space shuttle launch Feb. 28, 1986. | 9 | contradicted | 'The Challenger disaster on Jan. 28, 1986, overshadows news of the Uranus encounter and kills seven astronauts during launch' in `merged.md` -- The reference dates the disaster to Jan. 28, 1986, not Feb. 28, 1986. |
| 31 | Voyager 2 had been traveling for nearly a century at the time of the Miranda flyby. | 7 | carried in part | 'its closest approach to any object during its journey to that point' in `merged.md` -- The reference establishes a journey up to the Miranda flyby but does not give a nearly century-long duration. |
| 34 | News of the Uranus encounter was interrupted by the Challenger accident. | 9 | carried in part | 'The Challenger disaster on Jan. 28, 1986, overshadows news of the Uranus encounter' in `merged.md` -- The disaster overshadowed the news, but the reference does not say the news was interrupted. |
| 1 | Voyager 2 flew by Uranus. | 3 | carried | 'Voyager 2 is the first human-made object to fly past Uranus' in `merged.md` -- Flying past Uranus supports the flyby claim. |
| 8 | Belinda was among the moons discovered by Voyager 2. | 3 | carried | 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind, Belinda' in `merged.md` -- Belinda is listed among the moons Voyager 2 discovered. |
| 9 | Desdemona was among the moons discovered by Voyager 2. | 3 | carried | 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona' in `merged.md` -- Desdemona is listed among the moons Voyager 2 discovered. |
| 11 | Ophelia was among the moons discovered by Voyager 2. | 3 | carried | 'Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia' in `merged.md` -- Ophelia is listed among the moons Voyager 2 discovered. |
| 18 | Uranus’ magnetic field is off-center. | 3 | carried | 'offset from the planet’s center' in `merged.md` -- The magnetic field is described as off-center. |
| 21 | Uranus’ rings are extremely variable in thickness. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference states that the rings vary extremely in thickness. |
| 22 | Uranus’ rings are extremely variable in transparency. | 5 | carried | 'Its rings were found to be extremely variable in thickness and transparency' in `merged.md` -- The reference states that the rings vary extremely in transparency. |
| 23 | Voyager 2 returned photos of Miranda. | 7 | carried | 'Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- Miranda is among the moons photographed. |
| 24 | Voyager 2 returned photos of Oberon. | 7 | carried | 'Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania' in `merged.md` -- Oberon is among the moons photographed. |
| 30 | During the Miranda flyby, Voyager 2 came closer to Miranda than it had to any other object so far. | 7 | carried | 'its closest approach to any object during its journey to that point' in `merged.md` -- The Miranda pass was Voyager 2’s closest approach to any object up to then. |
| 32 | Images of Miranda showed peculiar features on its surface. | 7 | carried | 'Images show Miranda’s surface as a puzzling mishmash of unusual features' in `merged.md` -- The images show unusual features on Miranda’s surface. |
| 33 | Uranus appeared generally featureless. | 7 | carried | 'Uranus itself appears generally featureless' in `merged.md` -- The reference states this directly. |

### `merged.md` -- 47 claim(s): 0 invented, 30 contradicted, 2 supported in part, 15 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Voyager 2 completes its primary mission at Jupiter and Saturn. | contradicted | `source_a.md` | 'Voyager 3 had fulfilled its primary mission goals with the three planetary encounters' in `source_a.md` -- The source attributes completion of the primary mission goals to Voyager 3, not Voyager 2. |
| 4 | Voyager 2's encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible. | contradicted | `source_a.md` | 'Although Voyager 3 had fulfilled its primary mission goals with the three planetary encounters, mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.\n\nIn fact, its encounter with Jupiter was optimized in part to ensure that future planetary flybys would be possible.' in `source_a.md` -- The Jupiter optimization is attributed to Voyager 3, not Voyager 2. |
| 5 | The geometry of Voyager 2's Uranus encounter is shaped by the possibility of a later Neptune encounter. | contradicted | `source_a.md` | 'The Ur anus encounter’s geometry was also defined by the possibility of a future encounter with Saturn' in `source_a.md` -- The source names Saturn, not Neptune, as the possible future encounter shaping the geometry. |
| 6 | Voyager 2 has only 5.5 hours of close study during the Uranus flyby. | contradicted | `source_a.md` | 'Voyager 1 had only 6.4 days of close study during its flyby.' in `source_a.md` -- The source gives a different spacecraft and a different duration. |
| 7 | Voyager 2 is the first human-made object to fly past Uranus. | contradicted | `source_a.md` | "The first human-made object to fly past Uranus, Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- The source identifies Voyager 1 as the first human-made object to fly past Uranus. |
| 8 | Voyager 2's close-range observations of Uranus begin before the Jan. 24, 1986 flyby. | contradicted | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987" in `source_a.md` -- The source gives a different spacecraft and places the start of short-range observations after Jan. 24, 1986. |
| 10 | Sunlight at Uranus is roughly 400 times fainter than at Earth. | contradicted | `source_a.md` | 'Light conditions were five-hundred times less than terrestrial conditions.' in `source_a.md` -- The source gives five-hundred times, not roughly 400 times. |
| 11 | Voyager 2's closest approach to Uranus occurs at 17:59 UT Jan. 24, 1986. | contradicted | `source_a.md` | 'Closest approach to Uranus took place at 17:59 ED Jan. 24, 1968' in `source_a.md` -- The source gives a different time designation and year. |
| 12 | Voyager 2's closest approach to Uranus is at a range of about 50,640 miles (81,500 kilometers). | contradicted | `source_a.md` | 'at a range of about 50,640 kilometers (81,500 miles)' in `source_a.md` -- The claim reverses the units attached to the source's two numbers. |
| 13 | Voyager 2 discovers 10 new moons. | contradicted | `source_b.md` | 'Voyager 2 discovered 11 new moons' in `source_b.md` -- The source says 11 new moons, not 10. |
| 14 | Puck is among the new moons Voyager 2 discovers. | contradicted | `source_b.md` | 'Pucka' in `source_b.md` -- The named moon is Pucka, not Puck. |
| 15 | Portia is among the new moons Voyager 2 discovers. | contradicted | `source_b.md` | 'Portila' in `source_b.md` -- The named moon is Portila, not Portia. |
| 16 | Juliet is among the new moons Voyager 2 discovers. | contradicted | `source_b.md` | 'Juliette' in `source_b.md` -- The named moon is Juliette, not Juliet. |
| 17 | Cressida is among the new moons Voyager 2 discovers. | contradicted | `source_b.md` | 'Kressida' in `source_b.md` -- The named moon is Kressida, not Cressida. |
| 18 | Rosalind is among the new moons Voyager 2 discovers. | contradicted | `source_b.md` | 'Rosalinde' in `source_b.md` -- The named moon is Rosalinde, not Rosalind. |
| 21 | Cordelia is among the new moons Voyager 2 discovers. | contradicted | `source_b.md` | 'Cordelina' in `source_b.md` -- The named moon is Cordelina, not Cordelia. |
| 23 | Bianca is among the new moons Voyager 2 discovers. | contradicted | `source_b.md` | 'Bianca II' in `source_b.md` -- The source names Bianca II, not Bianca. |
| 24 | The names of the new moons Voyager 2 discovers follow a tradition drawing on Shakespeare and Alexander Pope. | contradicted | `source_b.md` | 'obvious allusions to Goethe, continuing a naming tradition begun in 1687' in `source_b.md` -- The source attributes the names to Goethe rather than Shakespeare and Alexander Pope. |
| 25 | The tradition of naming the moons after figures drawn from Shakespeare and Alexander Pope begins in 1852. | contradicted | `source_b.md` | 'continuing a naming tradition begun in 1687' in `source_b.md` -- The source dates the naming tradition to 1687, not 1852. |
| 26 | Voyager 2 discovers two new rings at Uranus. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source says Voyager 2 discovered three new rings, not two. |
| 27 | Nine rings at Uranus were already known before Voyager 2 discovered two new rings. | contradicted | `source_b.md` | 'three new rings in addition to the “older” eight rings' in `source_b.md` -- The source gives eight previously known rings and three new ones, rather than nine and two. |
| 29 | Uranus' magnetic field is tilted about 60 degrees from the rotation axis. | contradicted | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source specifies 66 degrees, not about 60 degrees. |
| 31 | Voyager 2 measures atmospheric winds at Uranus as high as 450 miles per hour (724 kilometers per hour). | contradicted | `source_b.md` | 'wind speeds in Uranus’ atmosphere as high as 450 km/h (72400 meters per hour)' in `source_b.md` -- The source assigns kilometers per hour, not miles per hour, to 450 and does not give 724 kilometers per hour. |
| 32 | Voyager 2 does not find evidence of a boiling lake of water beneath Uranus' cloud tops. | contradicted | `source_b.md` | 'found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface' in `source_b.md` -- The source says the spacecraft did find such evidence. |
| 37 | Voyager 2 returns photographs of Ariel. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source names Ariele, not Ariel, among the photographed moons. |
| 38 | Voyager 2 returns photographs of Umbriel. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source names Umbrella, not Umbriel, among the photographed moons. |
| 39 | Voyager 2 returns photographs of Titania. | contradicted | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source names Titan, not Titania, among the photographed moons. |
| 40 | Miranda, Oberon, Ariel, Umbriel, and Titania are five of Uranus' moons. | contradicted | `source_b.md` | 'Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons' in `source_b.md` -- Although Miranda and Oberon match, the source gives Ariele, Umbrella, and Titan instead of Ariel, Umbriel, and Titania. |
| 45 | The Challenger disaster occurs on Jan. 28, 1986. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source dates the accident Feb. 28, 1986, rather than Jan. 28, 1986. |
| 47 | The Challenger disaster kills seven astronauts during launch. | contradicted | `source_b.md` | 'the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986.' in `source_b.md` -- The source says six astronauts were killed, not seven. |
| 3 | Voyager 2's journey from Saturn to Uranus takes about 4,5 years. | supported in part | `source_a.md` | 'mission planners directed the veteran spacecraft to Uranus—a journey that would take about 4,5 years.' in `source_a.md` -- The source gives the duration of a journey to Uranus but attributes it to Voyager 3 and does not specify Saturn as its starting point. |
| 9 | Signals from Voyager 2 at Uranus take approximately 2,5 hours to reach Earth. | supported in part | `source_a.md` | "Voyager 1's short-range observations of the planet began Jan. 31, 1987, when signals took approximately 2,5 hours to reach Earth." in `source_a.md` -- The signal travel time is supported, but the passage attributes it to Voyager 1 rather than Voyager 2. |
| 2 | Voyager 2 continues to Uranus. | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- Voyager 2's observations of Uranus’ moons establish that it continued to Uranus. |
| 19 | Belinda is among the new moons Voyager 2 discovers. | supported | `source_b.md` | 'Belinda' in `source_b.md` -- Belinda appears among the new moons Voyager 2 discovered. |
| 20 | Desdemona is among the new moons Voyager 2 discovers. | supported | `source_b.md` | 'Desdemona' in `source_b.md` -- Desdemona appears among the new moons Voyager 2 discovered. |
| 22 | Ophelia is among the new moons Voyager 2 discovers. | supported | `source_b.md` | 'Ophelia' in `source_b.md` -- Ophelia appears among the new moons Voyager 2 discovered. |
| 28 | Voyager 2 discovers a magnetic field at Uranus. | supported | `source_b.md` | 'Voyager 2 discovered 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687), three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center.' in `source_b.md` -- The source says Voyager 2 discovered a magnetic field. |
| 30 | Uranus' magnetic field is offset from the planet’s center. | supported | `source_b.md` | 'a magnetic field tilted at 66 degrees off-axis and off-center' in `source_b.md` -- The source describes the magnetic field as off-center. |
| 33 | Uranus' rings were found to be extremely variable in thickness. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source explicitly describes the rings as extremely variable in thickness. |
| 34 | Uranus' rings were found to be extremely variable in transparency. | supported | `source_b.md` | 'Its rings were found to be extremely variable in thickness and transparency.' in `source_b.md` -- The source explicitly describes the rings as extremely variable in transparency. |
| 35 | Voyager 2 returns photographs of Miranda. | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source says Voyager 2 returned photos of Miranda. |
| 36 | Voyager 2 returns photographs of Oberon. | supported | `source_b.md` | 'Voyager 2 also returned spectacular photos of Miranda, Oberon, Ariele, Umbrella, and Titan, five of Uranus’ smaller moons.' in `source_b.md` -- The source says Voyager 2 returned photos of Oberon. |
| 41 | Voyager 2 passes Miranda at a range of 17,560 miles (28,260 kilometers). | supported | `source_b.md` | 'In flying by Miranda at a range of only 17.560 miles (28.260 kilometers)' in `source_b.md` -- The source gives the same distances with periods rather than commas as separators. |
| 42 | Voyager 2's pass of Miranda is its closest approach to any object during its journey to that point. | supported | `source_b.md` | 'the spacecraft came closest to any object so far in its nearly century-long travels' in `source_b.md` -- The source identifies the Miranda flyby as the spacecraft’s closest approach to any object up to that point. |
| 43 | Images show Miranda's surface as a mishmash of unusual features. | supported | `source_b.md` | 'Images of the moon showed a strange object whose surface was a mishmash of peculiar features that seemed to have no rhyme or reason.' in `source_b.md` -- The passage describes images of Miranda showing a mishmash of peculiar surface features. |
| 44 | Uranus appears generally featureless. | supported | `source_b.md` | 'Uranus itself appeared generally featureless.' in `source_b.md` -- The source states the claim directly. |
| 46 | The Challenger disaster overshadows news of the Uranus encounter. | supported | `source_b.md` | 'The spectacular news of the Uranus encounter was interrupted the same day by the tragic Challenger accident' in `source_b.md` -- The claim generalizes the source’s statement that news of the encounter was interrupted by the accident. |

## Structure

**9** mechanical check(s) over **16** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **47** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **48**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 2 run(s) over 7 attributed segment(s) — each source in one unbroken block. 2 of 2 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Verbatim violation — an invariant-core token did not survive unchanged

- `a2` (`source_a.md`) — numeric '3' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '1' (had) does not survive into the merge unchanged
- `a4` (`source_a.md`) — numeric '6.4' (days) does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '31' does not survive into the merge unchanged
- `a5` (`source_a.md`) — numeric '1987' (when) does not survive into the merge unchanged
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

The merge declared **13** departure(s) from its sources. Checking them confirms 3, rejects 10, and leaves 0 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 16 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a2` | reworded | Mission sequence: Voyager 2, not Voyager 3, makes the journey. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-001 came back CONTRADICTED, A-002 came back CONTRADICTED, A-003 came back CONTRADICTED (`A-001`, `A-002`, `A-003`) |
| `a4` | reworded | Flyby geometry: Neptune and Voyager 2 replace Saturn and Voyager 1. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-005 came back CONTRADICTED, A-006 came back CONTRADICTED (`A-005`, `A-006`) |
| `a5` | reworded | Observations: corrects the spacecraft and the date. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-007 came back CONTRADICTED, A-008 came back CONTRADICTED (`A-007`, `A-008`) |
| `a6` | reworded | Light conditions: corrects the comparison with Earth. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-010 came back CONTRADICTED (`A-010`) |
| `a7` | reworded | Closest approach: corrects the time zone, year, and distance units. | **rejected** | declared 'reworded', which predicts SUPPORTED; A-011 came back CONTRADICTED, A-012 came back CONTRADICTED (`A-011`, `A-012`) |
| `b1` | duplicate | Title: the identical base title already appears. | **confirmed** | no claim was drawn from this segment, and its text is in the merge, which is what 'duplicate' says happened to it (no claim traced to it) |
| `b2` | reworded | Discoveries: corrects names, counts, naming tradition, and tilt. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-002 came back CONTRADICTED, B-003 came back CONTRADICTED, B-004 came back CONTRADICTED, B-005 came back CONTRADICTED, B-006 came back CONTRADICTED, B-007 came back CONTRADICTED, B-010 came back CONTRADICTED, B-012 came back CONTRADICTED, B-013 came back CONTRADICTED, B-014 came back CONTRADICTED, B-015 came back CONTRADICTED, B-016 came back CONTRADICTED, B-017 came back CONTRADICTED (`B-002`, `B-003`, `B-004`, `B-005`, `B-006`, `B-007`, `B-010`, `B-012`, `B-013`, `B-014`, `B-015`, `B-016`, `B-017`) |
| `b3` | reworded | Atmosphere: corrects wind units and the unsupported lake claim. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-019 came back CONTRADICTED, B-020 came back CONTRADICTED (`B-019`, `B-020`) |
| `b5` | reworded | Moon photographs: corrects the names of the photographed moons. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-025 came back CONTRADICTED, B-026 came back CONTRADICTED, B-027 came back CONTRADICTED, B-028 came back CONTRADICTED (`B-025`, `B-026`, `B-027`, `B-028`) |
| `b6` | reworded | Miranda flyby: corrects the distances and journey duration. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-029 came back CONTRADICTED, B-031 came back PARTIAL (`B-029`, `B-031`) |
| `b7` | reworded | Miranda images: expresses the same observation more clearly. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-032`) |
| `b8` | reworded | Uranus’s appearance: uses the requested present tense. | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`B-033`) |
| `b9` | reworded | Challenger: corrects the date, timing, and death toll. | **rejected** | declared 'reworded', which predicts SUPPORTED; B-034 came back PARTIAL, B-035 came back CONTRADICTED, B-036 came back CONTRADICTED (`B-034`, `B-035`, `B-036`) |

## Added from outside the documents

The merge declared 11 statement(s) that your documents do not contain. **Nothing here has been verified against them**, because they are the only thing this tool checks against. Each is the model's own claim, and reviewing them is the reader's job rather than the tool's.

LLossless did not fetch, resolve or check any source listed here. LLossless itself opens no socket to do it. Whether the model made any web request is unmeasured -- this endpoint does not report it -- which is not the same as none.

11 of them correct(s) something a document states. A correction is a departure from your documents, so it is also reported as a finding and it moves the exit code: nothing here can tell a correction from a corruption, and the declaration buys you this row rather than a clean run.

| Statement | Corrects | Basis | Source | The merge's reason | Claims it covers |
|---|---|---|---|---|---|
| Voyager 2 completes its primary mission at Jupiter and Saturn, then continues to Uranus on a journey of about 4,5 years from Saturn. | Voyager 3 had fulfilled its primary mission goals with the three planetary encounters | the model's own knowledge | *no source* | Voyager 2 reaches Uranus after its Jupiter and Saturn encounters. | *none* |
| The Uranus encounter’s geometry is also shaped by the possibility of a later Neptune encounter, leaving Voyager 2 only 5.5 hours of close study during the flyby. | a future encounter with Saturn: Voyager 1 had only 6.4 days of close study during its flyby | the model's own knowledge | *no source* | Voyager 2 proceeds from Uranus to Neptune. | *none* |
| Voyager 2 is the first human-made object to fly past Uranus; its close-range observations begin before the Jan. 24, 1986 flyby, with signals taking approximately 2,5 hours to reach Earth. | Voyager 1's short-range observations of the planet began Jan. 31, 1987 | the model's own knowledge | *no source* | Voyager 2 flies past Uranus in 1986, before the stated date. | *none* |
| Sunlight at Uranus is roughly 400 times fainter than at Earth. | Light conditions were five-hundred times less than terrestrial conditions. | the model's own knowledge | *no source* | Sunlight weakens with the square of the distance from the Sun. | *none* |
| Closest approach occurs at 17:59 UT Jan. 24, 1986, at a range of about 50,640 miles (81,500 kilometers). | 17:59 ED Jan. 24, 1968, at a range of about 50,640 kilometers (81,500 miles) | the model's own knowledge | *no source* | The flyby occurs in 1986; the source reverses the distance units. | *none* |
| Voyager 2 discovers 10 new moons, including Puck, Portia, Juliet, Cressida, Rosalind, Belinda, Desdemona, Cordelia, Ophelia, and Bianca, whose names follow a tradition drawing on Shakespeare and Alexander Pope that begins in 1852. | 11 new moons (given such names as Pucka, Portila, Juliette, Kressida, Rosalinde, Belinda, Desdemona, Cordelina, Ophelia, and Bianca II – obvious allusions to Goethe, continuing a naming tradition begun in 1687) | the model's own knowledge | *no source* | The listed moon names derive from Shakespeare and Pope, not Goethe. | *none* |
| It also discovers two new rings beyond the nine already known and a magnetic field tilted about 60 degrees from the rotation axis and offset from the planet’s center. | three new rings in addition to the “older” eight rings, and a magnetic field tilted at 66 degrees off-axis and off-center | the model's own knowledge | *no source* | Voyager finds two further rings and a magnetic tilt near 60 degrees. | *none* |
| The spacecraft measures atmospheric winds as high as 450 miles per hour (724 kilometers per hour); it does not find evidence of a boiling lake of water beneath the cloud tops. | 450 km/h (72400 meters per hour) and found evidence of a boiling lake of water some 479 miles (900 kilometers) below the top cloud surface | the model's own knowledge | *no source* | The wind units are wrong, and the lake claim is unsupported. | *none* |
| Voyager 2 also returns photographs of Miranda, Oberon, Ariel, Umbriel, and Titania, five of Uranus’ moons. | Miranda, Oberon, Ariele, Umbrella, and Titan | the model's own knowledge | *no source* | Ariel, Umbriel, and Titania are the Uranian moons named here. | *none* |
| Voyager 2 passes Miranda at a range of 17,560 miles (28,260 kilometers), its closest approach to any object during its journey to that point. | 17.560 miles (28.260 kilometers), the spacecraft came closest to any object so far in its nearly century-long travels | the model's own knowledge | *no source* | Voyager 2 had traveled for years, not nearly a century. | *none* |
| The Challenger disaster on Jan. 28, 1986, overshadows news of the Uranus encounter and kills seven astronauts during launch. | the same day by the tragic Challenger accident that killed six astronauts during their space shuttle launch Feb. 28, 1986 | the model's own knowledge | *no source* | Challenger breaks apart on Jan. 28, killing all seven crew members. | *none* |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | bf7d5842201d (hosted) |
| Fidelity | open |
| Verification depth | full |
| Title policy | synthesise |
| Base document | `source_a.md` (explicit) |
| Model (merge) | gpt-6-sol |
| Model (decompose) | gpt-6-sol |
| Model (verify) | gpt-6-sol |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed 0, thinking decompose, merge, verify, profile openai-reasoning |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, merge, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | 22,041 in, 23,502 out, 0 cached, 8,358 reasoning |
| Cost | ~$0.28 estimated (rates read 2026-09-25) |
| Schema repairs | 0 |
| Errors | 0 |
| Duration | 221.1s |
| Generated | 2026-09-27T17:43:35+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `bf7d5842201d`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
