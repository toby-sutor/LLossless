## Verdict

**163 finding(s).** In the claims: 1 partially dropped, 2 contradicted, 1 hallucinated. In the structure: 156 false departure, 2 verbatim violation, 1 declared loss over budget. The merge declared **43** drop(s) of 216 source segment(s), **19.9%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 234 |
| Claims extracted from `source_a.md` | 42 |
| Claims extracted from `source_b.md` | 26 |
| Claims extracted from `source_c.md` | 112 |
| Forward — source claims accounted for in the merge | **177/180** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **40/42** (1 in part) |
| Forward — `source_b.md` claims accounted for | **26/26** |
| Forward — `source_c.md` claims accounted for | **111/112** |
| Reverse — merge claims found in a source | **233/234** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **406/413** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **A-001** (`source_a.md:1`) — Der Mah-Jongg-Rufer erhält eine zusätzliche Prämie von 10 Punkten gutgeschrieben.
  - evidence: 'Der Mah-Jongg-Rufer erhält eine zusätzliche Prämie von 10 (häufig 20) Punkten gutgeschrieben.' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference text states the Mah-Jongg caller receives a bonus of 10 points, but also notes it is often 20 points, making the claim incomplete.

### Contradicted — the merge states something different

- **A-031** -- the two documents disagree
  - `source_a.md:55` says: Das moderne Mah-Jongg wurde 1998 von der staatlichen Sportkommission Chinas offiziell als 255. Sportart anerkannt.
  - `merged.md` says: 'Das moderne Mah-Jongg, so wie es 1998 von der staatlichen Sportkommission Chinas offiziell als Sportart anerkannt wurde' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states it was recognized as a 'Sportart' (sport), not as the '255. Sportart' (255th sport) as claimed.
- **C-050** -- the two documents disagree
  - `source_c.md:44` says: East Wind counts from his own position against the clock.
  - `merged.md` says: 'Nun wirft Ostwind die zwei Würfel und zählt wie vorhin, bei sich selbst beginnend, die Augensumme gegen den Uhrzeigersinn an den Spielern ab.' (grounded)
  - judged against: `merged.md`
  - why this was read as a contradiction: The reference text states East Wind counts counter-clockwise (gegen den Uhrzeigersinn), not clockwise as the claim implies by 'with the clock'.

### Invented — in the merge, in neither source

- **M-142** (`merged.md:85`) — The game continues in this way until the game is scored.
  - judged against: `source_a.md`, `source_b.md` and `source_c.md`
  - rationale: The source text indicates the game continues until it is either won by a Mah-Jongg call or ends in a draw, but does not explicitly state it continues until the game is scored.

## Length capped

- `$.dispositions[8].reason` was 87 characters, over the 80-character cap; capped to fit
- `$.decisions[0].reason` was 106 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 42 claim(s): 0 dropped, 1 contradicted, 1 carried in part, 40 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 31 | Das moderne Mah-Jongg wurde 1998 von der staatlichen Sportkommission Chinas offiziell als 255. Sportart anerkannt. | 55 | contradicted | 'Das moderne Mah-Jongg, so wie es 1998 von der staatlichen Sportkommission Chinas offiziell als Sportart anerkannt wurde' in `merged.md` -- The reference text states it was recognized as a 'Sportart' (sport), not as the '255. Sportart' (255th sport) as claimed. |
| 1 | Der Mah-Jongg-Rufer erhält eine zusätzliche Prämie von 10 Punkten gutgeschrieben. | 1 | carried in part | 'Der Mah-Jongg-Rufer erhält eine zusätzliche Prämie von 10 (häufig 20) Punkten gutgeschrieben.' in `merged.md` -- The reference text states the Mah-Jongg caller receives a bonus of 10 points, but also notes it is often 20 points, making the claim incomplete. |
| 2 | Für Beraubung des Kong erhält der Spieler einen zusätzlichen Bonus von 10 Punkten. | 5 | carried | 'Für diese Beraubung des Kong erhält er einen zusätzlichen Bonus von 10 Punkten.' in `merged.md` -- The reference text directly states that for kong robbery, the player receives an additional bonus of 10 points. |
| 3 | Zweimaliges Verdoppeln vervierfacht den ursprünglichen Wert des Spielbildes. | 9 | carried | 'zweimaliges Verdoppeln vervierfacht beispielsweise den ursprünglichen Wert des Spielbildes' in `merged.md` -- The reference text explicitly states that doubling twice quadruples the original value of the game picture. |
| 4 | Das Limit beträgt meist 300 oder 500 Punkte. | 17 | carried | 'Dieses beträgt meist 300 oder 500 Punkte.' in `merged.md` -- The reference text states that the limit is usually 300 or 500 points. |
| 5 | Wenn der errechnete Punktewert das vereinbarte Limit übersteigt, wird das Spielbild nur mit diesem Höchstwert gezählt. | 17 | carried | 'Übersteigt der errechnete Punktewert das vereinbarte Limit, so wird das Spielbild nur mit diesem Höchstwert gezählt.' in `merged.md` -- The reference text directly states that if the calculated point value exceeds the agreed limit, the game picture is counted only with this maximum value. |
| 6 | Wenn das Spielbild des Mah-Jongg-Rufers ausschließlich aus Ziegeln der Trumpffarbe besteht, wird diese Hand mit dem Punktemaximum bewertet. | 19 | carried | 'Besteht das Spielbild des Mah-Jongg-Rufers ausschließlich aus Ziegeln der Trumpffarbe, also nur aus Wind- und Drachenziegeln, so wird diese Hand mit dem Punktemaximum bewertet.' in `merged.md` -- The reference text states that if the Mah-Jongg caller's game picture consists exclusively of trump suit tiles, it is valued at the maximum points. |
| 7 | Wenn Ostwind sofort nach Aufnehmen seiner Ziegel Mah-Jongg rufen kann, besitzt er den Segen des Himmels und erhält das Punktemaximum gutgeschrieben. | 21 | carried | 'Kann Ostwind sofort nach Aufnehmen seiner Ziegel Mah-Jongg rufen, so besitzt er den Segen des Himmels und erhält das Punktemaximum gutgeschrieben.' in `merged.md` -- The reference text directly states that if East Wind can call Mah-Jongg immediately after taking his tiles, he has the blessing of heaven and receives the maximum points. |
| 8 | Wenn ein anderer Spieler den ersten von Ostwind abgelegten Stein aufrufen und damit Mah-Jongg erklären kann, ist dies der Segen der Erde und der Spieler erhält die Hälfte des Limits gutgeschrieben. | 21 | carried | 'Kann ein anderer Spieler den ersten von Ostwind abgelegten Stein aufrufen und damit Mah-Jongg erklären, so ist dies der Segen der Erde und der Spieler erhält die Hälfte des Limits gutgeschrieben.' in `merged.md` -- The reference text directly states that if another player can call the first stone discarded by East Wind and declare Mah-Jongg, it is the blessing of earth and the player receives half the limit. |
| 9 | Wird Mah-Jongg mit 144 Steinen gespielt, besteht jede Seite der Mauer aus 18 Ziegelstapeln. | 33 | carried | 'so besteht jede Seite der Mauer aus 18 Ziegelstapeln' in `merged.md` -- The reference text states that when playing Mah-Jongg with 144 stones, each side of the wall consists of 18 tile stacks. |
| 10 | Wenn ein Spieler zu Beginn eines Spieles seine Steine aufnimmt, legt er seine Blumen- und Jahreszeitenziegel offen vor sich und zieht dafür einen Ersatzziegel vom toten Ende der Mauer. | 33 | carried | 'Sobald ein Spieler zu Beginn eines Spieles seine Steine aufnimmt, legt er seine Blumen- und Jahreszeitenziegel offen vor sich und zieht dafür einen Ersatzziegel vom toten Ende der Mauer' in `merged.md` -- The reference text directly states that when a player takes his stones at the beginning of a game, he places his flower and season tiles openly and draws a replacement tile from the dead end of the wall. |
| 11 | Wenn ein Spieler einen Blumen- oder Jahreszeitziegel von der Mauer kauft, wird genauso verfahren wie wenn er ihn zu Beginn aufnimmt. | 33 | carried | 'ebenso wird verfahren, wenn ein Spieler einen solchen Stein von der Mauer kauft' in `merged.md` -- The reference text explicitly states that the same procedure is followed when a player draws such a stone from the wall. |
| 12 | Nr. 1 der Ziegel der Hauptfarbe gilt für den Ostwind. | 35 | carried | 'Nr. 1 gilt für den Ostwind' in `merged.md` -- The reference text states that number 1 of the main suit tiles applies to East Wind. |
| 13 | Nr. 2 der Ziegel der Hauptfarbe gilt für den Südwind. | 35 | carried | 'Nr. 2 für den Südwind' in `merged.md` -- The reference text states that number 2 of the main suit tiles applies to South Wind. |
| 14 | Nr. 3 der Ziegel der Hauptfarbe gilt für den Westwind. | 35 | carried | 'Nr. 3 für den Westwind' in `merged.md` -- The reference text states that number 3 of the main suit tiles applies to West Wind. |
| 15 | Nr. 4 der Ziegel der Hauptfarbe gilt für den Nordwind. | 35 | carried | 'Nr. 4. für den Nordwind' in `merged.md` -- The reference text states that number 4 of the main suit tiles applies to North Wind. |
| 16 | Wenn Ostwind Mah-Jongg rufen kann, bleibt er im nächsten Spiel weiter Ostwind und die übrigen Positionen bleiben unverändert. | 39 | carried | 'Wenn Ostwind Mah-Jongg rufen kann, so bleibt er im nächsten Spiel weiter Ostwind und auch die übrigen Positionen bleiben unverändert.' in `merged.md` -- The reference text directly states that if East Wind can call Mah-Jongg, he remains East Wind in the next game and the other positions remain unchanged. |
| 17 | Wenn ein anderer Spieler Mah-Jongg ruft, übernimmt der bisherige Südwind die Rolle von Ostwind und die Positionen wechseln um einen Platz gegen den Uhrzeigersinn. | 39 | carried | 'Wenn ein anderer Spieler Mah-Jongg ruft, so übernimmt der bisherige Südwind die Rolle von Ostwind, und die Positionen wechseln um einen Platz gegen den Uhrzeigersinn.' in `merged.md` -- The reference text directly states that if another player calls Mah-Jongg, the previous South Wind takes the role of East Wind and positions shift one place counterclockwise. |
| 18 | Eine Runde ist beendet, sobald der Spieler, der im ersten Spiel die Position des Nordwindes innehatte, ein Spiel als Ostwind verliert. | 41 | carried | 'Eine Runde ist beendet, sobald der Spieler, der im ersten Spiel die Position des Nordwindes innehatte, ein Spiel als Ostwind verliert' in `merged.md` -- The reference text directly states that a round ends when the player who held North Wind position in the first game loses a game as East Wind. |
| 19 | Eine Runde besteht aus mindestens vier Spielen. | 41 | carried | 'Eine Runde besteht aus mindestens vier Spielen.' in `merged.md` -- The reference text directly states that a round consists of at least four games. |
| 20 | Eine Partie besteht aus vier Runden. | 43 | carried | 'so besteht diese aus vier Runden' in `merged.md` -- The reference text states that when a match is agreed upon rather than just one round, it consists of four rounds. |
| 21 | In der ersten Runde ist Ost der vorherrschende Wind. | 43 | carried | 'In der ersten Runde, der Ostwindrunde, ist Ost der vorherrschende Wind' in `merged.md` -- The reference text directly states that in the first round, East Wind is the prevailing wind. |
| 22 | In der zweiten Runde herrscht Südwind vor. | 43 | carried | 'in der zweiten Runde (Südwindrunde) herrscht Südwind vor' in `merged.md` -- The reference text directly states that in the second round South Wind prevails. |
| 23 | Die dritte Runde ist die Westwindrunde. | 43 | carried | 'die dritte Runde ist die Westwindrunde' in `merged.md` -- The reference text directly states that the third round is the West Wind round. |
| 24 | Die vierte Runde ist die Nordwindrunde. | 43 | carried | 'die vierte die Nordwindrunde' in `merged.md` -- The reference text directly states that the fourth round is the North Wind round. |
| 25 | Eine kleine Dose namens Mingg wird verwendet, um die einzelnen Spiele und Runden mitzuzählen. | 47 | carried | 'Um die einzelnen Spiele und Runden mitzuzählen, wird eine kleine Dose (Mingg) verwendet.' in `merged.md` -- The reference text directly states that a small box called Mingg is used to count the individual games and rounds. |
| 26 | Die Mingg stellt der jeweilige Spieler des Ostwindes vor sich auf den Tisch. | 47 | carried | 'Diese stellt der jeweilige Spieler des Ostwindes vor sich auf den Tisch' in `merged.md` -- The reference text directly states that the Mingg is placed on the table by the player who is East Wind. |
| 27 | Der Platzstein des vorherrschenden Windes wird oben auf die Mingg gelegt. | 47 | carried | 'der Platzstein des vorherrschenden Windes wird oben auf die Mingg gelegt' in `merged.md` -- The reference text explicitly states that the position stone of the prevailing wind is placed on top of the Mingg. |
| 28 | Vor einer weiteren Partie werden die Sitzplätze neu gelost. | 49 | carried | 'Vor einer weiteren Partie werden die Sitzplätze neu gelost' in `merged.md` -- The reference text directly states that seating positions are redrawn before another game/match. |
| 29 | Meist werden nicht mehr als zwei Partien gespielt. | 49 | carried | 'meist werden nicht mehr als zwei Partien gespielt' in `merged.md` -- The reference text states that usually no more than two matches are played. |
| 30 | Babcock führte in seinem Red Book von 1920 bestimmte Spielbilder an. | 53 | carried | 'Babcock in seinem Red Book von 1920 angeführt hat' in `merged.md` -- The reference text states that Babcock mentioned certain game patterns in his Red Book from 1920. |
| 32 | Das moderne Mah-Jongg ist eine Weiterentwicklung der klassischen Spielweise. | 55 | carried | 'Das moderne Mah-Jongg, so wie es 1998 von der staatlichen Sportkommission Chinas offiziell als Sportart anerkannt wurde, ist eine Weiterentwicklung der klassischen Spielweise' in `merged.md` -- The reference text directly states that modern Mah-Jongg is a further development of the classical gameplay. |
| 33 | Die offiziellen Regeln der modernen Spielweise finden bei internationalen Turnieren wie Welt- und Europameisterschaften Anwendung. | 57 | carried | 'Die offiziellen Regeln dieser modernen Spielweise finden bei internationalen Turnieren wie Welt- und Europameisterschaften Anwendung' in `merged.md` -- The reference text explicitly states that the official rules of modern gameplay are applied at international tournaments such as world and European championships. |
| 34 | In der Rangliste der European Mahjong Association werden nur Ergebnisse berücksichtigt, die aufgrund dieser Spielregeln erzielt wurden. | 57 | carried | 'In der Rangliste der European Mahjong Association werden nur Ergebnisse berücksichtigt, die aufgrund dieser Spielregeln erzielt wurden' in `merged.md` -- The reference text directly states that the European Mahjong Association rankings only consider results achieved according to these game rules. |
| 35 | Der finnische Hersteller Lagarto bietet eine kostenpflichtige Windows-Version des traditionellen Mah-Jongg namens Four Winds an. | 61 | carried | 'Der finnische Hersteller Lagarto bietet eine kostenpflichtige Windows-Version des traditionellen Mah-Jongg namens Four Winds an' in `merged.md` -- The reference text directly states that Finnish manufacturer Lagarto offers a paid Windows version of traditional Mah-Jongg called Four Winds. |
| 36 | Ein Spieler kann gegen drei durch die Software nachgebildete Spieler antreten. | 61 | carried | 'Ein Spieler kann gegen drei durch die Software nachgebildete Spieler antreten' in `merged.md` -- The reference text explicitly states that a player can play against three computer-simulated players. |
| 37 | Über ein Netzwerk können mehrere reale Spieler gegeneinander oder gegen die Software antreten. | 61 | carried | 'Ebenso können über ein Netzwerk mehrere reale Spieler gegeneinander oder gegen die Software antreten' in `merged.md` -- The reference text directly states that multiple real players can play against each other or against the software over a network. |
| 38 | Es kann nach verschiedenen Regeln gespielt werden. | 61 | carried | 'Es kann nach verschiedenen Regeln gespielt werden' in `merged.md` -- The reference text explicitly states that the game can be played according to different rules. |
| 39 | Das KDE-Projekt enthält eine kostenfreie Version von Mah-Jongg, die Kajongg genannt wird. | 61 | carried | 'Das KDE-Projekt enthält eine kostenfreie Version von Mah-Jongg, die Kajongg genannt wird' in `merged.md` -- The reference text directly states that the KDE Project contains a free version of Mah-Jongg called Kajongg. |
| 40 | In Yakuza 0 ist die japanische Variante von Mah-Jongg namens Riichi Mahjong als Minispiel vorhanden. | 63 | carried | 'In verschiedenen Teilen der Yakuza-Spieleserie, wie zum Beispiel Yakuza 0, ist die japanische Variante von Mah-Jongg (Riichi Mahjong) als Minispiel vorhanden' in `merged.md` -- The reference text directly states that Yakuza 0 contains the Japanese variant of Mah-Jongg (Riichi Mahjong) as a mini-game. |
| 41 | Für iPhone und iPad gibt es im Apple App Store unter dem Namen Mahjong! von POK-Software eine traditionelle Version. | 65 | carried | 'Für iPhone und iPad gibt es im Apple App Store unter dem Namen Mahjong! von POK-Software eine traditionelle Version' in `merged.md` -- The reference text directly states that there is a traditional version called Mahjong! by POK-Software available in the Apple App Store for iPhone and iPad. |
| 42 | Die Mahjong!-App von POK-Software simuliert bis zu 3 Mitspieler. | 65 | carried | 'eine traditionelle Version, die bis zu 3 Mitspieler simuliert' in `merged.md` -- The reference text explicitly states that the traditional version simulates up to 3 co-players. |

### `source_b.md` -- 26 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 26 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Ab Mitte der 1980er Jahre wurde Mah-Jongg Solitaire zunächst unter dem Namen Shanghai als Computerspiel populär. | 4 | carried | 'Ab Mitte der 1980er Jahre wurde Mah-Jongg Solitaire zunächst unter dem Namen Shanghai als Computerspiel populär' in `merged.md` -- The reference text directly states that from the mid-1980s, Mah-Jongg Solitaire became popular as a computer game first under the name Shanghai. |
| 2 | Die verbesserten grafischen Möglichkeiten des neuen Amiga-Computers ermöglichten erstmals eine ansprechende Darstellung dieses Spiels. | 4 | carried | 'nachdem die verbesserten grafischen Möglichkeiten des neuen Amiga-Computers erstmals eine ansprechende Darstellung dieses Spiels erlaubten' in `merged.md` -- The reference text directly states that improved graphical capabilities of the new Amiga computer first allowed an appealing representation of this game. |
| 3 | Bei der beliebtesten Computerspiel-Variante liegen zu Spielbeginn alle 144 Steine auf dem Tisch, teils in mehreren Lagen übereinander. | 6 | carried | 'Bei der beliebtesten Computerspiel-Variante liegen zu Spielbeginn alle 144 Steine auf dem Tisch, teils in mehreren Lagen übereinander' in `merged.md` -- The reference text directly states that in the most popular computer game variant, all 144 tiles lie on the table at the start of play, partially in multiple layers on top of each other. |
| 4 | Traditionell werden die Spielsteine in der Figur eines Drachen oder einer Schildkröte aufgebaut. | 6 | carried | 'Traditionell werden die Spielsteine in der Figur eines Drachen oder einer Schildkröte aufgebaut' in `merged.md` -- The reference text directly states that traditionally the game pieces are arranged in the shape of a dragon or a turtle. |
| 5 | Ein einzelner Spieler muss paarweise alle 144 Steine vom Tisch nehmen. | 6 | carried | 'Ein einzelner Spieler muss paarweise alle 144 Steine vom Tisch nehmen' in `merged.md` -- The reference text directly states that a single player must remove all 144 stones from the table in pairs. |
| 6 | Ein Paar darf nur abgetragen werden, wenn beide Steine von keinem anderen Stein teilweise oder vollständig überdeckt sind und an zumindest einer Längsseite freiliegen. | 6 | carried | 'Ein Paar darf nur abgetragen werden, wenn beide Steine von keinem anderen Stein teilweise oder vollständig überdeckt sind und an zumindest einer Längsseite freiliegen' in `merged.md` -- The reference text directly states the rule for when a pair may be removed from the board. |
| 7 | Die Steine der Hauptfarben kommen jeweils nur einmal vor und können keine Paare bilden. | 6 | carried | 'Während die Steine der Hauptfarben jeweils nur einmal vorkommen und keine Paare bilden können' in `merged.md` -- The reference text directly states that stones of the main colors each occur only once and cannot form pairs. |
| 8 | Die Blumenziegel und die Jahreszeitenziegel dürfen jeweils untereinander beliebig kombiniert werden. | 6 | carried | 'dürfen die Blumenziegel und die Jahreszeitenziegel jeweils untereinander beliebig kombiniert werden' in `merged.md` -- The reference text directly states that flower tiles and season tiles may be combined arbitrarily with each other. |
| 9 | In einigen Varianten sind die Blumen- und Jahreszeitenziegel verdoppelt und dafür zum Ausgleich die Windziegel nur zweimal enthalten. | 6 | carried | 'In einigen Varianten sind die Blumen- und Jahreszeitenziegel verdoppelt und dafür zum Ausgleich beispielsweise die Windziegel nur zweimal enthalten.' in `merged.md` -- The reference text states exactly this claim about certain variants doubling flower and season tiles while reducing wind tiles to two copies. |
| 10 | Mitunter kommen die Jahreszeitenziegel doppelt vor und dafür keine Blumenziegel. | 6 | carried | 'Mitunter kommen die Jahreszeitenziegel doppelt vor und dafür keine Blumenziegel.' in `merged.md` -- The reference text states verbatim that in some variants season tiles appear doubled and flower tiles are omitted. |
| 11 | Es gibt heute Angebote auf dem Netz, auf denen Mahjong Solitaire online gespielt werden kann. | 8 | carried | 'Als Weiterentwicklung der Computerspiele gibt es heute Angebote auf dem Netz, auf denen Mahjong Solitaire online gespielt werden kann.' in `merged.md` -- The reference text directly states that today there are online offerings where Mahjong Solitaire can be played. |
| 12 | Bei Mahjong Connect können die identischen Spielsteine nur ausgewählt werden, wenn zwischen ihnen eine Linie gezogen werden kann. | 10 | carried | 'Zum Beispiel können beim Mahjong Connect die identischen Spielsteine nur ausgewählt werden, wenn zwischen ihnen eine Linie gezogen werden kann.' in `merged.md` -- The reference text states that in Mahjong Connect, identical tiles can only be selected if a line can be drawn between them. |
| 13 | Bei Mahjong Dimensions gibt es kein zweidimensionales Spielfeld, sondern die Spielsteine sind zu einem dreidimensionalen Objekt gefügt. | 10 | carried | 'Beim Mahjong Dimensions gibt es kein zweidimensionales Spielfeld, sondern die Spielsteine sind zu einem dreidimensionalen Objekt gefügt.' in `merged.md` -- The reference text states that Mahjong Dimensions has no two-dimensional playing field but rather three-dimensional tile arrangement. |
| 14 | In Japan entwickelte sich auf Grundlage des Spiels das Genre Mah-Jongg in Anime und Manga. | 16 | carried | 'In Japan entwickelte sich auf Grundlage des Spiels das Genre Mah-Jongg in Anime und Manga' in `merged.md` -- The reference text directly states that a Mah-Jongg genre in anime and manga developed in Japan based on the game. |
| 15 | Saki ist ein Werk im Genre Mah-Jongg in Anime und Manga. | 16 | carried | 'siehe auch: Saki, Tobaku Mokushiroku Kaiji, Akagi, The Legend of Koizumi' in `merged.md` -- The reference text lists Saki as an example work in the Mah-Jongg anime and manga genre. |
| 16 | Tobaku Mokushiroku Kaiji ist ein Werk im Genre Mah-Jongg in Anime und Manga. | 16 | carried | 'siehe auch: Saki, Tobaku Mokushiroku Kaiji, Akagi, The Legend of Koizumi' in `merged.md` -- The reference text lists Tobaku Mokushiroku Kaiji as an example work in the Mah-Jongg anime and manga genre. |
| 17 | Akagi ist ein Werk im Genre Mah-Jongg in Anime und Manga. | 16 | carried | 'siehe auch: Saki, Tobaku Mokushiroku Kaiji, Akagi, The Legend of Koizumi' in `merged.md` -- The reference text lists Akagi as an example work in the Mah-Jongg anime and manga genre. |
| 18 | The Legend of Koizumi ist ein Werk im Genre Mah-Jongg in Anime und Manga. | 16 | carried | 'siehe auch: Saki, Tobaku Mokushiroku Kaiji, Akagi, The Legend of Koizumi' in `merged.md` -- The reference text lists The Legend of Koizumi as an example work in the Mah-Jongg anime and manga genre. |
| 19 | In der romantischen Filmkomödie Crazy Rich Asians (2018) bildet eine Mah-Jongg-Partie den dramaturgischen Höhepunkt einer zentralen Konfrontation. | 20 | carried | 'In der romantischen Filmkomödie Crazy Rich Asians (2018) bildet eine Mah-Jongg-Partie den dramaturgischen Höhepunkt einer zentralen Konfrontation.' in `merged.md` -- The reference text states exactly that a Mah-Jongg game forms the dramaturgical climax of a central confrontation in Crazy Rich Asians. |
| 20 | Der Film Gefahr und Begierde basiert auf der gleichnamigen Kurzgeschichte von Eileen Chang. | 22 | carried | 'In dem Film Gefahr und Begierde, nach der gleichnamigen Kurzgeschichte von Eileen Chang' in `merged.md` -- The reference text states that the film Gefahr und Begierde is based on the same-named short story by Eileen Chang. |
| 21 | Ang Lee erzählt in Gefahr und Begierde die Geschichte einer tragischen Liebesbeziehung zwischen einer Widerstandskämpferin und dem Geheimdienstchef der Kollaborationsregierung von Wang Jingwei. | 22 | carried | 'erzählt Ang Lee die Geschichte einer tragischen Liebesbeziehung zwischen einer Widerstandskämpferin und dem Geheimdienstchef der Kollaborationsregierung von Wang Jingwei.' in `merged.md` -- The reference text states that Ang Lee tells the story of a tragic love relationship between a resistance fighter and the secret service chief of Wang Jingwei's collaborationist government. |
| 22 | Tang Wei spielte die Widerstandskämpferin in Gefahr und Begierde. | 22 | carried | 'die Widerstandskämpferin, gespielt von Tang Wei' in `merged.md` -- The reference text explicitly states that Tang Wei played the resistance fighter in Gefahr und Begierde. |
| 23 | Im Kriminalroman Sous les vents de Neptun von Fred Vargas (Frédérique Audoin-Rouzeau) nimmt das Spiel Mah-Jongg eine zentrale Rolle ein. | 24 (unverified) | carried | 'Im Kriminalroman Sous les vents de Neptun (dt. "Der vierzehnte Stein") von Fred Vargas (Frédérique Audoin-Rouzeau) nimmt das Spiel Mah-Jongg eine zentrale Rolle ein.' in `merged.md` -- The reference text states that Mah-Jongg plays a central role in the crime novel Sous les vents de Neptun by Fred Vargas. |
| 24 | Das Buch Sous les vents de Neptun wurde 2008 verfilmt. | 24 | carried | 'Das Buch wurde 2008 verfilmt.' in `merged.md` -- The reference text states that the book Sous les vents de Neptun was made into a film in 2008. |
| 25 | Im französisch-Schweizer Spielfilm Die Gleichung ihres Lebens (2023) lernt die Hauptperson Marguerite Mah-Jongg nach dem Abbruch ihrer Mathematik-Promotion. | 26 | carried | 'Im französisch-Schweizer Spielfilm Die Gleichung ihres Lebens (2023) lernt die Hauptperson Marguerite nach dem Abbruch ihrer Mathematik-Promotion Mah-Jongg' in `merged.md` -- The reference text states that Marguerite learns Mah-Jongg after abandoning her mathematics doctoral studies in the film. |
| 26 | Marguerite erzielt in Die Gleichung ihres Lebens erhebliche Einnahmen mit Mah-Jongg. | 26 | carried | 'und erzielt erhebliche Einnahmen damit.' in `merged.md` -- The reference text states that Marguerite achieves considerable income from Mah-Jongg in the film. |

### `source_c.md` -- 112 claim(s): 0 dropped, 1 contradicted, 0 carried in part, 111 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 50 | East Wind counts from his own position against the clock. | 44 | contradicted | 'Nun wirft Ostwind die zwei Würfel und zählt wie vorhin, bei sich selbst beginnend, die Augensumme gegen den Uhrzeigersinn an den Spielern ab.' in `merged.md` -- The reference text states East Wind counts counter-clockwise (gegen den Uhrzeigersinn), not clockwise as the claim implies by 'with the clock'. |
| 1 | Mah-Jongg is a Chinese game for four persons. | 2 | carried | 'ist ein chinesisches Spiel für vier Personen.' in `merged.md` -- The reference text states in German that Mah-Jongg is a Chinese game for four persons, supporting the English translation of this claim. |
| 2 | Joseph Park Babcock lived from 1893–1949. | 6 | carried | 'Joseph Park Babcock (1893–1949)' in `merged.md` -- The reference text directly states Babcock's birth and death years as 1893–1949. |
| 3 | Joseph Park Babcock was an American traveller in the Republic of China. | 6 | carried | 'ein amerikanischer Reisender in der Republik China' in `merged.md` -- The reference text describes Babcock as an American traveller in the Republic of China. |
| 4 | Joseph Park Babcock drafted a rulebook in the 1920er Jahren. | 6 | carried | 'verfasste in den 1920er Jahren ein Regelwerk' in `merged.md` -- The reference text states that Babcock drafted a rulebook in the 1920s. |
| 5 | Joseph Park Babcock brought the game to the USA. | 6 | carried | 'und brachte das Spiel in die USA.' in `merged.md` -- The reference text states that Babcock brought the game to the USA. |
| 6 | Babcock gave the game the name MAH-JONGG. | 6 | carried | 'Babcock gab ihm den Namen MAH-JONGG' in `merged.md` -- The reference text states that Babcock gave the game the name MAH-JONGG. |
| 7 | Babcock registered MAH-JONGG as a trademark. | 6 | carried | 'den er als Marke eintragen ließ.' in `merged.md` -- The reference text states that Babcock registered MAH-JONGG as a trademark. |
| 8 | Babcock simplified the game for the American market. | 6 | carried | 'Babcock vereinfachte das Spiel für den amerikanischen Markt' in `merged.md` -- The reference text directly states that Babcock simplified the game for the American market. |
| 9 | Babcock equipped the stones with Roman numerals. | 6 | carried | 'versah die Steine unter anderem mit römischen Ziffern' in `merged.md` -- The reference text explicitly states that Babcock equipped the stones with Roman numerals among other things. |
| 10 | Babcock designated Mah-Jongg as his own development in the foreword to his Red Book. | 8 | carried | 'Babcock bezeichnet Mah-Jongg im Vorwort zu seinem Red Book als eine eigene Entwicklung, basierend auf dem alten chinesischen Spiel' in `merged.md` -- The reference text states that Babcock designated Mah-Jongg in the foreword to his Red Book as his own development based on the old Chinese game. |
| 11 | Babcock named Ningpo (today Ningbo) or the province Fukien (today Fujian) as the place of origin. | 8 | carried | 'Als Entstehungsort nennt er an anderer Stelle die Stadt Ningpo (heute Ningbo) oder die Provinz Fukien (heute Fujian).' in `merged.md` -- The reference text states that Babcock named Ningpo or the province Fukien as the place of origin. |
| 12 | Mah-Jongg originated in the second half of the 19th century. | 10 | carried | 'Tatsächlich entstand Mah-Jongg erst in der zweiten Hälfte des 19. Jahrhunderts.' in `merged.md` -- The reference text directly states that Mah-Jongg originated in the second half of the 19th century. |
| 13 | The oldest preserved games date to around 1870. | 10 | carried | 'Die ältesten erhaltenen Spiele datieren um 1870' in `merged.md` -- The reference text explicitly states that the oldest preserved games date to around 1870. |
| 14 | The oldest written references are from 1890. | 10 | carried | 'die ältesten schriftlichen Hinweise aus dem Jahr 1890' in `merged.md` -- The reference text states that the oldest written references are from 1890. |
| 15 | Originally, Mah-Jongg was a gambling game connected with tea houses and brothels. | 10 | carried | 'Ursprünglich war Mah-Jongg ein Glücksspiel, das mit Teehäusern und Bordellen in Verbindung stand' in `merged.md` -- The reference text directly states that originally Mah-Jongg was a gambling game connected with tea houses and brothels. |
| 16 | By the end of the 19th century, Mah-Jongg had established itself in bourgeois households. | 10 | carried | 'gegen Ende des 19. Jahrhunderts hatte es sich jedoch auch in bürgerlichen Haushalten etabliert' in `merged.md` -- The reference text states that by the end of the 19th century, Mah-Jongg had established itself in bourgeois households. |
| 17 | Mah-Jongg spread from Shanghai to other parts of China. | 10 | carried | 'sich von Shanghai aus in andere Teile Chinas verbreitet' in `merged.md` -- The reference text explicitly states that Mah-Jongg spread from Shanghai to other parts of China. |
| 18 | The Mah-Jongg game spread rapidly in China and Japan. | 10 | carried | 'Das Mah-Jongg-Spiel verbreitete sich rasch in China und Japan.' in `merged.md` -- The reference text directly states that the Mah-Jongg game spread rapidly in China and Japan. |
| 19 | After Babcock made the game known in the USA, Mah-Jongg attained worldwide popularity. | 10 | carried | 'Nachdem Babcock das Spiel in den USA bekanntgemacht hatte, erlangte Mah-Jongg weltweite Popularität' in `merged.md` -- The reference text states that after Babcock made the game known in the USA, Mah-Jongg attained worldwide popularity. |
| 20 | Factories were founded specifically to meet the demand for Mah-Jongg games. | 12 | carried | 'Es wurden eigens Fabriken gegründet, um die Nachfrage nach Mah-Jongg-Spielen zu befriedigen' in `merged.md` -- The reference text explicitly states that factories were founded specifically to meet the demand for Mah-Jongg games. |
| 21 | In Germany, the game was introduced by F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt. | 12 | carried | 'In Deutschland wurde das Spiel eingeführt durch F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt' in `merged.md` -- The reference text states that in Germany the game was introduced by F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt. |
| 22 | F. Ad. Richter & Cie held Gebrauchsmusterschutz Nr. 722354 v. 6. November 1919. | 12 | carried | 'Gebrauchsmusterschutz Nr. 722354 v. 6. November 1919' in `merged.md` -- The reference text provides the exact protection number and date for F. Ad. Richter & Cie. |
| 23 | The Hamburger Nordicus-Golconda Werke was another Mah-Jongg manufacturer in Germany. | 12 | carried | 'Ein weiterer Mah-Jongg-Hersteller in Deutschland war die Hamburger Nordicus-Golconda Werke.' in `merged.md` -- The reference text explicitly states that Hamburger Nordicus-Golconda Werke was another Mah-Jongg manufacturer in Germany. |
| 24 | There were Mah-Jongg magazines. | 12 | carried | 'Es gab Mah-Jongg-Zeitschriften' in `merged.md` -- The reference text directly states that there were Mah-Jongg magazines. |
| 25 | Mah-Jongg tournaments were held in many American cities. | 12 | carried | 'in vielen amerikanischen Städten wurden Mah-Jongg-Turniere veranstaltet' in `merged.md` -- The reference text explicitly states that Mah-Jongg tournaments were held in many American cities. |
| 26 | Fred Astaire was among the prominent promoters of the American Mah-Jongg boom of the 1920er-Jahre. | 12 | carried | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire' in `merged.md` -- The reference text states that Fred Astaire was among the prominent promoters of the American Mah-Jongg boom of the 1920er-Jahre. |
| 27 | President Warren G. Harding was among the prominent promoters of the American Mah-Jongg boom of the 1920er-Jahre. | 12 (unverified) | carried | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding' in `merged.md` -- The reference text states that President Warren G. Harding was among the prominent promoters of the Mah-Jongg boom of the 1920er-Jahre. |
| 28 | First Lady Florence Harding was among the prominent promoters of the American Mah-Jongg boom of the 1920er-Jahre. | 12 (unverified) | carried | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.' in `merged.md` -- The reference text states that First Lady Florence Harding was among the prominent promoters of the Mah-Jongg boom. |
| 29 | The National Mah Jongg League was founded in New York in 1937. | 12 | carried | 'In New York wurde 1937 die National Mah Jongg League gegründet' in `merged.md` -- The reference text explicitly states that the National Mah Jongg League was founded in New York in 1937. |
| 30 | The National Mah Jongg League further standardized the rules. | 12 | carried | 'die die Regeln weiter vereinheitlichte' in `merged.md` -- The reference text states that the National Mah Jongg League further standardized the rules. |
| 31 | The game is extremely popular in China and Japan. | 14 | carried | 'Das Spiel ist in China und Japan überaus populär' in `merged.md` -- The reference text states that the game is extremely popular in China and Japan. |
| 32 | Since the 2020er Jahren, a clear upturn can be observed particularly in western major cities. | 14 | carried | 'seit den 2020er Jahren lässt sich jedoch besonders in westlichen Großstädten wieder ein deutlicher Aufschwung beobachten' in `merged.md` -- The reference text states that since the 2020er Jahren a clear upturn can be observed particularly in western major cities. |
| 33 | Global participation in Mah-Jongg events has more than tripled within a year. | 14 | carried | 'Die weltweite Teilnahme an Mah-Jongg-Veranstaltungen hat sich innerhalb eines Jahres mehr als verdreifacht' in `merged.md` -- The reference text directly states that global participation in Mah-Jongg events has more than tripled within a year. |
| 34 | Regular events take place in Berlin, Helsinki, London, Los Angeles, New York, Paris and Sydney. | 14 | carried | 'regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt' in `merged.md` -- The reference text explicitly lists all seven cities where regular Mah-Jongg events take place. |
| 35 | On YouTube there are numerous introduction and learning videos. | 14 | carried | 'Auf YouTube existieren zahlreiche Einführungs- und Lernvideos' in `merged.md` -- The reference text states that numerous introduction and learning videos exist on YouTube. |
| 36 | On TikTok, the amount of Mah-Jongg-related content increased by around 70 Prozent within a year. | 14 | carried | 'auf TikTok nahm die Menge der Mah-Jongg-bezogenen Inhalte innerhalb eines Jahres um rund 70 Prozent zu' in `merged.md` -- The reference text directly states that Mah-Jongg-related content on TikTok increased by around 70 percent within a year. |
| 37 | A Mah-Jongg game consists of 136 or 144 playing stones. | 22 | carried | 'Ein Mah-Jongg-Spiel besteht aus 136 oder 144 Spielsteinen, die Ziegel genannt werden.' in `merged.md` -- The reference text explicitly states that a Mah-Jongg game consists of 136 or 144 playing stones called tiles. |
| 38 | In the standard variant, 136 stones are used. | 30 | carried | 'In der Standard-Variante wird mit 136 Steinen gespielt' in `merged.md` -- The reference text directly states that 136 stones are used in the standard variant. |
| 39 | The eight tiles of the main color are not used in the standard variant. | 30 | carried | 'die acht Ziegel der Hauptfarbe werden nicht verwendet' in `merged.md` -- The reference text states that the eight tiles of the main color are not used in the standard variant. |
| 40 | Before the start of a game, the four players stand at the four sides of a square table. | 36 | carried | 'Vor Beginn einer Partie stehen die vier Spieler an den vier Seiten eines quadratischen Tisches.' in `merged.md` -- The reference text directly states that before a game begins, the four players stand at the four sides of a square table. |
| 41 | The oldest player shuffles the four position tiles face down. | 36 | carried | 'Der älteste Spieler mischt verdeckt die vier Platzsteine' in `merged.md` -- The reference text explicitly states that the oldest player shuffles the four position tiles face down. |
| 42 | The player who receives the East Wind position tile becomes the dealer in the first game. | 38 | carried | 'Der Spieler, der den Platzstein Ostwind erhält, wird Spielleiter im ersten Spiel' in `merged.md` -- The reference text states that the player who receives the East Wind position tile becomes the dealer (Spielleiter) in the first game. |
| 43 | West Wind sits opposite East Wind. | 38 | carried | 'Westwind setzt sich gegenüber' in `merged.md` -- The reference text states that West Wind sits opposite (gegenüber) East Wind. |
| 44 | South Wind sits to the right of East Wind. | 38 | carried | 'Südwind zur Rechten (!) von Ostwind' in `merged.md` -- The reference text explicitly states that South Wind sits to the right of East Wind. |
| 45 | North Wind sits to the left of East Wind. | 38 | carried | 'Nordwind zur Linken' in `merged.md` -- The reference text states that North Wind sits to the left of East Wind. |
| 46 | Each of the four players builds one side of the wall by taking 34 tiles and arranging them in a wall 17 tiles long and two tiles high. | 42 | carried | 'baut jeder der vier Spieler eine Seite der Mauer, indem er 34 der Ziegel verdeckt nimmt und zu einer 17 Ziegel langen und zwei Ziegel hohen Mauer anordnet' in `merged.md` -- The reference text states that each of the four players builds one side of the wall by taking 34 tiles and arranging them in a wall 17 tiles long and two tiles high. |
| 47 | If flower and season tiles are used, each player takes 36 tiles and the width of the wall is 18 stacks. | 42 | carried | 'Wird mit Blumen- und Jahreszeitenziegeln gespielt, so nimmt jeder Spieler 36 Ziegel und die Breite der Mauer beträgt 18 Stapel' in `merged.md` -- The reference text directly states that if flower and season tiles are used, each player takes 36 tiles and the wall width is 18 stacks. |
| 48 | The four wall sections are pushed together so they touch at the corners and form a square. | 42 | carried | 'Die vier Mauerstücke werden zusammengeschoben, so dass sie sich an den Ecken berühren und ein Quadrat bilden.' in `merged.md` -- The reference text explicitly states that the four wall sections are pushed together so they touch at the corners and form a square. |
| 49 | Outside Asian countries, this is sometimes called the Chinese Wall. | 42 | carried | 'Außerhalb der asiatischen Länder wird dies manchmal Chinesische Mauer genannt.' in `merged.md` -- The reference text states that outside Asian countries, this is sometimes called Chinese Wall. |
| 51 | The determined player throws both dice again. | 44 | carried | 'Der so bestimmte Spieler wirft ebenfalls beide Würfel' in `merged.md` -- The reference text states that the determined player throws both dice again. |
| 52 | East Wind counts from the right end of the wall in front of him clockwise according to the total sum of tiles. | 44 | carried | 'Ostwind zählt am rechten Ende der vor ihm befindlichen Mauer beginnend im Uhrzeigersinn der Gesamtsumme entsprechend Ziegelstapel ab.' in `merged.md` -- The reference text states that East Wind counts from the right end of the wall in front of him clockwise according to the total sum of tiles. |
| 53 | The removed tiles are called loose tiles. | 46 | carried | 'Die herausgenommenen Steine heißen lose Ziegel' in `merged.md` -- The reference text states that the removed tiles are called loose tiles (lose Ziegel). |
| 54 | Loose tiles mark the dead end of the wall. | 46 | carried | 'markieren das tote Ende der Mauer' in `merged.md` -- The reference text states that loose tiles mark the dead end of the wall. |
| 55 | The end to the left of the gap is the living end of the wall. | 46 | carried | 'das Ende links der Lücke ist das lebende Ende der Mauer' in `merged.md` -- The reference text states that the end to the left of the gap is the living end of the wall. |
| 56 | Tiles are regularly drawn from the living end of the wall. | 46 | carried | 'Gezogen werden die Steine regulär vom lebenden Ende der Mauer.' in `merged.md` -- The reference text states that tiles are regularly drawn from the living end of the wall. |
| 57 | Only replacement tiles are taken from the dead end. | 46 | carried | 'Vom toten Ende werden dagegen nur Ersatzziegel (siehe unten) genommen' in `merged.md` -- The reference text states that only replacement tiles are taken from the dead end of the wall. |
| 58 | Replacement tiles are taken beginning with the two loose tiles. | 46 | carried | 'Vom toten Ende werden dagegen nur Ersatzziegel (siehe unten) genommen, beginnend mit den beiden losen Ziegeln.' in `merged.md` -- The reference text explicitly states that replacement tiles are taken from the dead end beginning with the two loose tiles. |
| 59 | The players take three times in turn counterclockwise each two stacks of two tiles from the living end of the wall. | 46 | carried | 'Die Spieler nehmen dreimal reihum gegen den Uhrzeigersinn jeder zwei Stapel zu zwei Ziegel vom lebenden Ende der Mauer' in `merged.md` -- The reference text states players take three times in turn counterclockwise each two stacks of two tiles from the living end of the wall. |
| 60 | East Wind serves himself first. | 46 | carried | 'wobei sich Ostwind als erster bedient' in `merged.md` -- The reference text states that East Wind serves himself first in the tile-taking process. |
| 61 | Finally, each player takes one more thirteenth tile. | 46 | carried | 'Zuletzt nimmt jeder Spieler noch einen weiteren, dreizehnten' in `merged.md` -- The reference text states that finally each player takes one more thirteenth tile. |
| 62 | East Wind additionally takes a fourteenth tile. | 46 | carried | 'und Ostwind außerdem einen vierzehnten Ziegel' in `merged.md` -- The reference text explicitly states that East Wind additionally takes a fourteenth tile. |
| 63 | Each of the four players tries to form a complete game image from the most valuable figures by drawing and discarding tiles. | 50 | carried | 'Jeder der vier Spieler versucht, durch Ziehen und Abwerfen von Steinen seine ursprüngliche Hand zu verbessern und ein vollständiges Spielbild aus möglichst wertvollen Figuren zu formen.' in `merged.md` -- The reference text states that each of the four players tries to form a complete game image from most valuable figures by drawing and discarding tiles. |
| 64 | A complete game image consists of four figures and finally a pair. | 50 | carried | 'Hat ein Spieler ein vollständiges Spielbild bestehend aus vier Figuren und schließlich einem Paar gebildet' in `merged.md` -- The reference text explicitly states that a complete game image consists of four figures and finally a pair. |
| 65 | The four figures can optionally be triplets, quadruplets or sequences. | 50 | carried | 'Die vier Figuren können wahlweise Drillinge, Vierlinge oder Folgen sein.' in `merged.md` -- The reference text states the four figures can optionally be triplets, quadruplets or sequences. |
| 66 | A pair consists of two identical tiles. | 56 | carried | 'Ein Paar besteht aus zwei gleichen Steinen' in `merged.md` -- The reference text explicitly states that a pair consists of two identical tiles. |
| 67 | To call Mah-Jongg, a complete game image is necessary. | 58 | carried | 'Um Mah-Jongg rufen zu können, ist ein vollständiges Spielbild nötig' in `merged.md` -- The reference text states that to call Mah-Jongg, a complete game image is necessary. |
| 68 | The game image must contain exactly one pair, the closing pair. | 58 | carried | 'in diesem muss genau ein Paar, das Schlusspaar (將, jiàng, manchmal 眼, yǎn), enthalten sein' in `merged.md` -- The reference text states the game image must contain exactly one pair, the closing pair. |
| 69 | A discarded tile can only be called to complete a pair if Mah-Jongg is called at the same time. | 58 | carried | 'Zur Vervollständigung eines Paares darf ein abgelegter Stein nur aufgerufen werden, wenn gleichzeitig Mah-Jongg gerufen wird.' in `merged.md` -- The reference text states a discarded tile can only be called to complete a pair if Mah-Jongg is called at the same time. |
| 70 | A Pong consists of three identical tiles. | 62 | carried | 'Ein Pong (碰, pèng) besteht aus drei gleichen Steinen.' in `merged.md` -- The reference text explicitly states that a Pong consists of three identical tiles. |
| 71 | If a Pong is formed exclusively from tiles of the original hand or drawn tiles, it is a concealed Pong. | 62 | carried | 'Wird ein Pong ausschließlich aus Ziegeln der ursprünglichen Hand oder von der Mauer gezogenen Ziegeln gebildet, so handelt es sich um einen verdeckten Pong' in `merged.md` -- The reference text states if a Pong is formed exclusively from tiles of the original hand or drawn tiles, it is a concealed Pong. |
| 72 | A concealed Pong does not need to be reported. | 62 | carried | 'der nicht gemeldet werden muss' in `merged.md` -- The reference text states a concealed Pong does not need to be reported. |
| 73 | If a player has a pair and the third tile is discarded by any other player, the player may call the tile with the call "Pong". | 64 (unverified) | carried | 'Besitzt ein Spieler ein Paar und wird der dritte Stein von einem beliebigen anderen Spieler abgelegt, so darf der Spieler diesen Stein mit dem Ruf "Pong" aufrufen.' in `merged.md` -- The reference text states if a player has a pair and the third tile is discarded by any other player, the player may call the tile with 'Pong'. |
| 74 | In the 1970s and 1980s, the term Pon was often used instead of Pong in the German-speaking area. | 66 | carried | 'In den 1970er und 1980er Jahren wurde im deutschsprachigen Raum statt Pong oftmals der Begriff Pon verwendet.' in `merged.md` -- The reference text states that in the 1970s and 1980s, the term Pon was often used instead of Pong in the German-speaking area. |
| 75 | In the 1982 instruction book by Ursula Eschenbach, the terms Pon, Kan and Chii are used throughout. | 66 | carried | 'Auch in dem 1982 erschienenen Anleitungsbuch von Ursula Eschenbach ist durchgehend von Pon, Kan und Chii die Rede.' in `merged.md` -- The reference text states that in the 1982 instruction book by Ursula Eschenbach, the terms Pon, Kan and Chii are used throughout. |
| 76 | The terms Pon, Kan and Chii come from the Japanese variant of Riichi Mahjong. | 66 | carried | 'Die Begriffe Pon (jap. ポン, 碰 pon), Kan (カン, 槓, 杠 kan) oder Chii (チー, 吃 chī) stammen aus der japanischen Spielart des Riichi Mahjong' in `merged.md` -- The reference text states the terms Pon, Kan and Chii come from the Japanese variant of Riichi Mahjong. |
| 77 | A Kong consists of four identical tiles. | 70 | carried | 'Ein Kong (槓 / 杠, gàng) besteht aus vier gleichen Steinen.' in `merged.md` -- The reference text explicitly states that a Kong consists of four identical tiles. |
| 78 | If a Kong is formed exclusively from tiles of the original hand and drawn tiles, the player should announce a concealed Kong. | 72 | carried | 'Wird ein Kong ausschließlich aus Steinen der ursprünglichen Hand und von der Mauer gezogenen Ziegeln gebildet, so sollte der Spieler einen verdeckten Kong melden.' in `merged.md` -- The reference text states if a Kong is formed exclusively from tiles of the original hand and drawn tiles, the player should announce a concealed Kong. |
| 79 | If a player does not announce a concealed Kong, he cannot draw a replacement tile from the wall. | 72 | carried | 'Tut er dies nicht, so kann er keinen Ersatzziegel aus der Mauer ziehen' in `merged.md` -- The reference text states if a player does not announce a concealed Kong, he cannot draw a replacement tile from the wall. |
| 80 | A replacement tile is necessary for Kongs to achieve a complete game image. | 72 | carried | 'der bei Kongs notwendig ist, um ein komplettes Spielbild zu erreichen' in `merged.md` -- The reference text states a replacement tile is necessary for Kongs to achieve a complete game image. |
| 81 | If the game ends before the player announces the quadruplet, the concealed Kong is counted as a concealed Pong. | 72 | carried | 'Wird das Spiel beendet, bevor der Spieler den Vierling meldet, so wird der verdeckte Kong als verdeckter Pong gewertet.' in `merged.md` -- The reference text states if the game ends before the player announces the quadruplet, the concealed Kong is counted as a concealed Pong. |
| 82 | A concealed Kong does not have to be announced immediately. | 74 | carried | 'Ein verdeckter Kong muss nicht sofort gemeldet werden, sondern kann auch später herausgelegt werden' in `merged.md` -- The reference text states a concealed Kong does not have to be announced immediately, but can be laid out later. |
| 83 | A concealed Kong can also be laid out later when the player is on turn again. | 74 | carried | 'Ein verdeckter Kong muss nicht sofort gemeldet werden, sondern kann auch später herausgelegt werden, wenn der Spieler erneut am Zug ist.' in `merged.md` -- The reference text directly states that a concealed Kong does not have to be announced immediately but can be laid out later when the player is on turn again. |
| 84 | When a concealed Kong is announced, the four tiles are laid out openly. | 76 | carried | 'Bei der Meldung werden die vier Steine offen ausgelegt' in `merged.md` -- The text states that when a concealed Kong is announced, the four tiles are laid out openly. |
| 85 | To indicate that it is a concealed Kong, the two outer tiles are placed face down. | 76 (unverified) | carried | 'werden die beiden äußeren Steine mit der Rückseite nach oben gelegt' in `merged.md` -- The reference text specifies that the two outer tiles are placed with their reverse side facing up to indicate a concealed Kong. |
| 86 | If a player holds three identical tiles in hand, he may claim the fourth tile with the call "Kong" if a player discards it. | 78 (unverified) | carried | 'Hält ein Spieler drei gleiche Steine in der Hand – also einen verdeckten Pong – so darf er, wenn ein Spieler den vierten Stein ablegt, diesen Ziegel mit dem Ruf "Kong" für sich beanspruchen' in `merged.md` -- The text directly supports the claim that a player holding three identical tiles may claim the fourth tile with the call 'Kong' if discarded. |
| 87 | If a player has already announced an open Pong and the missing fourth tile is discarded by another player, this tile cannot be called to complete the Kong. | 80 | carried | 'Hat ein Spieler bereits einen offenen Pong gemeldet und wird der fehlende vierte Stein von einem anderen Spieler abgelegt, so kann dieser Ziegel nicht zur Komplettierung des Kongs aufgerufen werden.' in `merged.md` -- The reference text explicitly states that if a player has announced an open Pong and the fourth tile is discarded, it cannot be called to complete the Kong. |
| 88 | If a player has announced a Pong and draws the missing fourth tile from the wall, he may attach it to the Pong to create an open Kong. | 82 | carried | 'Hat ein Spieler bereits einen Pong gemeldet und zieht er den fehlenden vierten Stein von der Mauer, so darf er ihn an den Pong anlegen und besitzt damit einen offenen Kong.' in `merged.md` -- The text states that if a player has announced a Pong and draws the missing fourth tile from the wall, he may attach it to the Pong to create an open Kong. |
| 89 | In this situation, a robbery of the Kong can occur. | 82 | carried | 'In dieser Situation kann es zu einer Beraubung des Kong kommen.' in `merged.md` -- The reference text confirms that in this situation, a robbery of the Kong can occur. |
| 90 | The tile drawn from the wall can be demanded by another player if he can call "Mah-Jongg" with it. | 82 (unverified) | carried | 'Der von der Mauer gezogene Stein kann von einem anderen Spieler für sich gefordert werden, wenn er damit "Mah-Jongg" rufen kann.' in `merged.md` -- The text states that the tile drawn from the wall can be demanded by another player if he can call 'Mah-Jongg' with it. |
| 91 | As soon as a player announces an open or concealed Kong, he must draw a replacement tile from the dead end of the wall. | 84 | carried | 'Sobald ein Spieler einen offenen oder verdeckten Kong meldet, muss er einen Ersatzziegel vom toten Ende der Mauer ziehen.' in `merged.md` -- The reference text directly states that as soon as a player announces an open or concealed Kong, he must draw a replacement tile from the dead end of the wall. |
| 92 | A Chow is a sequence of exactly three consecutive tiles of a basic color. | 88 | carried | 'Ein Chow (吃, chī, manchmal 上, shàng) ist eine Sequenz aus genau drei aufeinanderfolgenden Steinen einer Grundfarbe' in `merged.md` -- The text defines a Chow as a sequence of exactly three consecutive tiles of a basic color. |
| 93 | Sequences of more than three tiles are not allowed. | 88 | carried | 'Sequenzen aus mehr als drei Steinen sind nicht gestattet.' in `merged.md` -- The reference text explicitly states that sequences of more than three tiles are not allowed. |
| 94 | A Chow from tiles of the trump color is not possible. | 90 | carried | 'Ein Chow aus Steinen der Trumpffarbe ist nicht möglich.' in `merged.md` -- The text states that a Chow from tiles of the trump color is not possible. |
| 95 | A discarded tile can be called with "Chow" by a player if the player sits immediately to the right of the player who discarded the tile. | 92 (unverified) | carried | 'Ein abgelegter Stein kann von einem Spieler mit "Chow" aufgerufen werden, wenn der Spieler unmittelbar zur Rechten desjenigen Spielers sitzt, der den betreffenden Stein abgelegt hat.' in `merged.md` -- The reference text states that a discarded tile can be called with 'Chow' if the player sits immediately to the right of the player who discarded it. |
| 96 | Another player can only call a discarded tile for a sequence if he calls Mah-Jongg at the same time. | 94 | carried | 'Ein anderer Spieler kann nur dann einen abgelegten Stein für eine Folge aufrufen, wenn er gleichzeitig Mah-Jongg ruft.' in `merged.md` -- The text states that another player can only call a discarded tile for a sequence if he calls Mah-Jongg at the same time. |
| 97 | Sequences formed from tiles of the original hand or drawn tiles can remain concealed until the end of the game. | 96 | carried | 'Folgen, die aus Steinen der ursprünglichen Hand bzw. aus gezogenen Steinen gebildet werden, können bis zum Spielende verdeckt bleiben.' in `merged.md` -- The reference text states that sequences formed from tiles of the original hand or drawn tiles can remain concealed until the end of the game. |
| 98 | Mah-Jongg is played counterclockwise. | 100 | carried | 'Mah-Jongg wird gegen den Uhrzeigersinn gespielt.' in `merged.md` -- The text directly states that Mah-Jongg is played counterclockwise. |
| 99 | After East Wind has taken his 14 tiles, he begins the game by discarding one tile openly in the middle of the table. | 100 | carried | 'Nachdem sich Ostwind seine 14 Ziegel genommen hat, beginnt er das Spiel, indem er nach einer eventuellen Meldung einen Stein offen in der Mitte des Tisches ablegt' in `merged.md` -- The text states that after East Wind has taken his 14 tiles, he begins by discarding one tile openly in the middle of the table. |
| 100 | If no player calls the discarded tile, the right neighbor draws a tile from the living end of the wall. | 102 | carried | 'Wenn kein Spieler den abgelegten Stein aufruft, so zieht der rechte Nachbar einen Stein vom lebenden Ende der Mauer' in `merged.md` -- The reference text states that if no player calls the discarded tile, the right neighbor draws a tile from the living end of the wall. |
| 101 | If a tile is discarded, it is dead. | 104 | carried | 'Wird ein Stein abgelegt, so ist er tot' in `merged.md` -- The text states that if a tile is discarded, it is dead. |
| 102 | A dead tile remains openly in the middle of the table. | 104 | carried | 'er bleibt offen in der Mitte des Tisches liegen' in `merged.md` -- The reference text states that a dead tile remains openly in the middle of the table. |
| 103 | The next player can play a Chow with a discarded tile. | 104 | carried | 'der nächste Spieler kann einen Chow spielen' in `merged.md` -- The text states that the next player can play a Chow with a discarded tile. |
| 104 | Any player can play a Pong or Kong with a discarded tile. | 104 | carried | 'sowie jener und alle weiteren Spieler einen Pong oder einen Kong' in `merged.md` -- The reference text indicates that any player (that player and all further players) can play a Pong or Kong with a discarded tile. |
| 105 | After that, a tile is no longer available for play or can be taken. | 104 | carried | 'Danach ist der Stein nicht mehr für das Spiel verfügbar beziehungsweise aufnehmbar.' in `merged.md` -- The text states that after that, a tile is no longer available for play or can be taken. |
| 106 | If a tile is called by a player, the player takes the discarded tile and must lay down the corresponding figure openly. | 106 | carried | 'Wird ein Stein von einem Spieler aufgerufen, so nimmt der Spieler den abgelegten Stein und muss die betreffende Figur offen auflegen.' in `merged.md` -- The reference text states that if a tile is called, the player takes the discarded tile and must lay down the corresponding figure openly. |
| 107 | After that, the player discards a tile and the game continues with that player. | 106 | carried | 'Danach wirft er einen Stein ab, und das Spiel wird mit diesem Spieler fortgesetzt.' in `merged.md` -- The text states that after that, the player discards a tile and the game continues with that player. |
| 108 | In this way, other players can also be skipped. | 106 | carried | 'Auf diese Weise können auch Spieler übergangen werden: Legt beispielsweise Südwind einen Stein ab, der von Nordwind gerufen wird, so wird Westwind übersprungen.' in `merged.md` -- The reference text explicitly states that players can be skipped in this way, with an example of Westwind being skipped when Südwind discards a tile called by Nordwind. |
| 109 | If a tile is called by multiple players, the following ranking applies: If a player needs the tile for a Mah-Jongg call, he has priority over a Kong or Pong call. | 108 | carried | 'Wird ein Ziegel von mehreren Spielern gerufen, so gilt folgende Rangordnung: Benötigt ein Spieler den Stein für einen Mah-Jongg-Ruf, so hat er Vorrang gegenüber einem Kong- oder Pong-Ruf' in `merged.md` -- The text directly states the ranking when multiple players call a tile, specifying that a Mah-Jongg call has priority over Kong or Pong calls. |
| 110 | Kong and Pong calls have priority over a Chow. | 108 | carried | 'und diese wiederum haben Vorrang vor einem Chow' in `merged.md` -- The reference text explicitly states that Kong and Pong calls have priority over a Chow, completing the ranking hierarchy. |
| 111 | Concealed combinations count double. | 124 | carried | 'Verdeckte Kombinationen zählen das Doppelte.' in `merged.md` -- The reference text directly states that concealed combinations count double, which is the exact meaning of the claim. |
| 112 | A Kong counts four times as much as the corresponding Pong. | 128 | carried | 'Ein Kong zählt viermal so viel wie der entsprechende Pong.' in `merged.md` -- The reference text explicitly states that a Kong counts four times as much as the corresponding Pong, matching the claim exactly. |

### `merged.md` -- 234 claim(s): 1 invented, 0 contradicted, 0 supported in part, 233 supported

Each claim below was read against `source_a.md`, `source_b.md` and `source_c.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 142 | The game continues in this way until the game is scored. | invented | -- | The source text indicates the game continues until it is either won by a Mah-Jongg call or ends in a draw, but does not explicitly state it continues until the game is scored. |
| 1 | Mah-Jongg is a Chinese game for four people. | supported | `source_c.md` | 'ist ein chinesisches Spiel für vier Personen' in `source_c.md` -- Source_c.md explicitly states Mah-Jongg is a Chinese game for four people. |
| 2 | Joseph Park Babcock lived from 1893 to 1949. | supported | `source_c.md` | 'Joseph Park Babcock (1893–1949)' in `source_c.md` -- Source_c.md directly provides Babcock's birth and death years. |
| 3 | Joseph Park Babcock was an American traveler in the Republic of China. | supported | `source_c.md` | 'ein amerikanischer Reisender in der Republik China' in `source_c.md` -- Source_c.md describes Babcock as an American traveler in the Republic of China. |
| 4 | Joseph Park Babcock drafted a ruleset in the 1920s. | supported | `source_c.md` | 'verfasste in den 1920er Jahren ein Regelwerk' in `source_c.md` -- Source_c.md states Babcock drafted a ruleset in the 1920s. |
| 5 | Joseph Park Babcock brought the game to the USA. | supported | `source_c.md` | 'brachte das Spiel in die USA' in `source_c.md` -- Source_c.md confirms Babcock brought the game to the USA. |
| 6 | Babcock gave the game the name MAH-JONGG in this spelling. | supported | `source_c.md` | 'Babcock gab ihm den Namen MAH-JONGG (in dieser Schreibweise)' in `source_c.md` -- Source_c.md explicitly states Babcock gave the game the name MAH-JONGG in this spelling. |
| 7 | Babcock registered the name as a trademark. | supported | `source_c.md` | 'den er als Marke eintragen ließ' in `source_c.md` -- Source_c.md states Babcock registered the name as a trademark. |
| 8 | Babcock simplified the game for the American market. | supported | `source_c.md` | 'Babcock vereinfachte das Spiel für den amerikanischen Markt' in `source_c.md` -- Source_c.md confirms Babcock simplified the game for the American market. |
| 9 | Babcock equipped the stones with Roman numerals among other things. | supported | `source_c.md` | 'versah die Steine unter anderem mit römischen Ziffern' in `source_c.md` -- Source_c.md states Babcock equipped the stones with Roman numerals among other things. |
| 10 | Babcock describes Mah-Jongg in the preface to his Red Book as its own development based on the old Chinese game. | supported | `source_c.md` | 'Babcock bezeichnet Mah-Jongg im Vorwort zu seinem Red Book als eine eigene Entwicklung, basierend auf dem alten chinesischen Spiel' in `source_c.md` -- Source_c.md directly quotes Babcock describing Mah-Jongg in his Red Book preface as his own development based on the old Chinese game. |
| 11 | Babcock names the city of Ningpo (today Ningbo) as the place of origin. | supported | `source_c.md` | 'Als Entstehungsort nennt er an anderer Stelle die Stadt Ningpo (heute Ningbo)' in `source_c.md` -- Source_c.md states Babcock names the city of Ningpo (today Ningbo) as a place of origin. |
| 12 | Babcock names the province of Fukien (today Fujian) as the place of origin. | supported | `source_c.md` | 'oder die Provinz Fukien (heute Fujian)' in `source_c.md` -- Source_c.md states Babcock names the province of Fukien (today Fujian) as a place of origin. |
| 13 | Mah-Jongg actually originated in the second half of the 19th century. | supported | `source_c.md` | 'Tatsächlich entstand Mah-Jongg erst in der zweiten Hälfte des 19. Jahrhunderts' in `source_c.md` -- Source_c.md explicitly states Mah-Jongg actually originated in the second half of the 19th century. |
| 14 | The oldest preserved games date to around 1870. | supported | `source_c.md` | 'Die ältesten erhaltenen Spiele datieren um 1870' in `source_c.md` -- Source_c.md confirms the oldest preserved games date to around 1870. |
| 15 | The oldest written references date from 1890. | supported | `source_c.md` | 'die ältesten schriftlichen Hinweise aus dem Jahr 1890' in `source_c.md` -- Source_c.md states the oldest written references date from 1890. |
| 16 | Originally Mah-Jongg was a gambling game associated with teahouses and brothels. | supported | `source_c.md` | 'Ursprünglich war Mah-Jongg ein Glücksspiel, das mit Teehäusern und Bordellen in Verbindung stand' in `source_c.md` -- Source_c.md confirms Mah-Jongg was originally a gambling game associated with teahouses and brothels. |
| 17 | By the end of the 19th century Mah-Jongg had established itself in bourgeois households. | supported | `source_c.md` | 'gegen Ende des 19. Jahrhunderts hatte es sich jedoch auch in bürgerlichen Haushalten etabliert' in `source_c.md` -- Source_c.md states that by the end of the 19th century Mah-Jongg had established itself in bourgeois households. |
| 18 | Mah-Jongg spread from Shanghai to other parts of China. | supported | `source_c.md` | 'sich von Shanghai aus in andere Teile Chinas verbreitet' in `source_c.md` -- Source_c.md confirms Mah-Jongg spread from Shanghai to other parts of China. |
| 19 | Mah-Jongg spread rapidly in China and Japan. | supported | `source_c.md` | 'Das Mah-Jongg-Spiel verbreitete sich rasch in China und Japan' in `source_c.md` -- Source_c.md states Mah-Jongg spread rapidly in China and Japan. |
| 20 | After Babcock made the game known in the USA, Mah-Jongg achieved worldwide popularity. | supported | `source_c.md` | 'Nachdem Babcock das Spiel in den USA bekanntgemacht hatte, erlangte Mah-Jongg weltweite Popularität' in `source_c.md` -- Source_c.md confirms that after Babcock made the game known in the USA, Mah-Jongg achieved worldwide popularity. |
| 21 | This worldwide popularity was comparable to Canasta in the 1950s. | supported | `source_c.md` | 'vergleichbar dem Canasta in den 1950er Jahren' in `source_c.md` -- Source_c.md states this worldwide popularity was comparable to Canasta in the 1950s. |
| 22 | Factories were established specifically to meet the demand for Mah-Jongg games. | supported | `source_c.md` | 'Es wurden eigens Fabriken gegründet, um die Nachfrage nach Mah-Jongg-Spielen zu befriedigen' in `source_c.md` -- Source_c.md confirms factories were established specifically to meet the demand for Mah-Jongg games. |
| 23 | There was a rumor that imported games were contaminated with viruses. | supported | `source_c.md` | 'zumal das Gerücht umging, importierte Spiele wären mit Viren verseucht' in `source_c.md` -- Source_c.md states there was a rumor that imported games were contaminated with viruses. |
| 24 | In Germany, the game was introduced by F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt. | supported | `source_c.md` | 'In Deutschland wurde das Spiel eingeführt durch F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt' in `source_c.md` -- Source_c.md confirms in Germany the game was introduced by F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt. |
| 25 | F. Ad. Richter & Cie held Gebrauchsmusterschutz Nr. 722354 from 6. November 1919. | supported | `source_c.md` | '(Gebrauchsmusterschutz Nr. 722354 v. 6. November 1919)' in `source_c.md` -- Source_c.md states F. Ad. Richter & Cie held Gebrauchsmusterschutz Nr. 722354 from 6. November 1919. |
| 26 | Nordicus-Golconda Werke in Hamburg was another Mah-Jongg manufacturer in Germany. | supported | `source_c.md` | 'Ein weiterer Mah-Jongg-Hersteller in Deutschland war die Hamburger Nordicus-Golconda Werke.' in `source_c.md` -- Source_c.md explicitly states that Nordicus-Golconda Werke in Hamburg was another Mah-Jongg manufacturer in Germany. |
| 27 | There were Mah-Jongg journals. | supported | `source_c.md` | 'Es gab Mah-Jongg-Zeitschriften' in `source_c.md` -- Source_c.md directly states that there were Mah-Jongg journals (Zeitschriften). |
| 28 | Mah-Jongg tournaments were held in many American cities. | supported | `source_c.md` | 'in vielen amerikanischen Städten wurden Mah-Jongg-Turniere veranstaltet' in `source_c.md` -- Source_c.md explicitly states that Mah-Jongg tournaments were held in many American cities. |
| 29 | Fred Astaire was among the prominent supporters of the American Mah-Jongg boom of the 1920s. | supported | `source_c.md` | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire' in `source_c.md` -- Source_c.md names Fred Astaire as one of the prominent supporters of the American Mah-Jongg boom of the 1920s. |
| 30 | President Warren G. Harding was among the prominent supporters of the American Mah-Jongg boom of the 1920s. | supported | `source_c.md` | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding' in `source_c.md` -- Source_c.md explicitly names President Warren G. Harding as one of the prominent supporters of the American Mah-Jongg boom of the 1920s. |
| 31 | First Lady Florence Harding was among the prominent supporters of the American Mah-Jongg boom of the 1920s. | supported | `source_c.md` | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.' in `source_c.md` -- Source_c.md explicitly names First Lady Florence Harding as one of the prominent supporters of the American Mah-Jongg boom of the 1920s. |
| 32 | The National Mah Jongg League was founded in New York in 1937. | supported | `source_c.md` | 'In New York wurde 1937 die National Mah Jongg League gegründet' in `source_c.md` -- Source_c.md directly states that the National Mah Jongg League was founded in New York in 1937. |
| 33 | The National Mah Jongg League further standardized the rules. | supported | `source_c.md` | 'die National Mah Jongg League gegründet, die die Regeln weiter vereinheitlichte' in `source_c.md` -- Source_c.md states that the National Mah Jongg League further standardized the rules. |
| 34 | The National Mah Jongg League significantly shaped the game style now known as American Mahjong. | supported | `source_c.md` | 'die National Mah Jongg League gegründet, die die Regeln weiter vereinheitlichte und damit die heute als American Mahjong bekannte Spielart maßgeblich prägte' in `source_c.md` -- Source_c.md states that the National Mah Jongg League significantly shaped the game style now known as American Mahjong. |
| 35 | Mah-Jongg disappeared like a fashion within a few years. | supported | `source_c.md` | 'Doch bereits wenige Jahre später verschwand Mah-Jongg wie eine Mode und ebenso schnell, wie sie gekommen war.' in `source_c.md` -- Source_c.md states that Mah-Jongg disappeared like a fashion within a few years, and as quickly as it came. |
| 36 | The game is extremely popular in China and Japan. | supported | `source_c.md` | 'Das Spiel ist in China und Japan überaus populär' in `source_c.md` -- Source_c.md directly states that the game is extremely popular in China and Japan. |
| 37 | Outside East Asia, the number of interested people was long lower. | supported | `source_c.md` | 'außerhalb Ostasiens war die Zahl der Interessenten lange geringer' in `source_c.md` -- Source_c.md states that outside East Asia the number of interested people was long lower. |
| 38 | Since the 2020s, a clear upturn can be observed particularly in Western major cities. | supported | `source_c.md` | 'seit den 2020er Jahren lässt sich jedoch besonders in westlichen Großstädten wieder ein deutlicher Aufschwung beobachten' in `source_c.md` -- Source_c.md states that since the 2020s a clear upturn can be observed particularly in Western major cities. |
| 39 | Global participation in Mah-Jongg events more than tripled within one year. | supported | `source_c.md` | 'Die weltweite Teilnahme an Mah-Jongg-Veranstaltungen hat sich innerhalb eines Jahres mehr als verdreifacht' in `source_c.md` -- Source_c.md states that global participation in Mah-Jongg events more than tripled within one year. |
| 40 | Regular events take place in Berlin, Helsinki, London, Los Angeles, New York, Paris and Sydney. | supported | `source_c.md` | 'regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt' in `source_c.md` -- Source_c.md lists the cities where regular Mah-Jongg events take place, matching the claim exactly. |
| 41 | Social media contributes to this development. | supported | `source_c.md` | 'Auch soziale Medien tragen zu dieser Entwicklung bei' in `source_c.md` -- Source_c.md explicitly states that social media contributes to this development. |
| 42 | Numerous introduction and learning videos exist on YouTube. | supported | `source_c.md` | 'Auf YouTube existieren zahlreiche Einführungs- und Lernvideos' in `source_c.md` -- Source_c.md states that numerous introduction and learning videos exist on YouTube. |
| 43 | The amount of Mah-Jongg-related content on TikTok increased by approximately 70 percent within one year. | supported | `source_c.md` | 'auf TikTok nahm die Menge der Mah-Jongg-bezogenen Inhalte innerhalb eines Jahres um rund 70 Prozent zu' in `source_c.md` -- Source_c.md states that the amount of Mah-Jongg-related content on TikTok increased by approximately 70 percent within one year. |
| 44 | Mah-Jongg can be understood as a variant of the card game Rummy. | supported | `source_c.md` | 'Von den Regeln her kann Mah-Jongg als eine Variante des Kartenspiels Rummy verstanden werden' in `source_c.md` -- Source_c.md directly states that Mah-Jongg can be understood as a variant of the card game Rummy. |
| 45 | Rummy also has a variant with game stones. | supported | `source_c.md` | 'von dem es ebenfalls eine Variante mit Spielsteinen gibt' in `source_c.md` -- Source_c.md states that Rummy also has a variant with game stones. |
| 46 | There is no evidence that the Rummy game developed from Mah-Jongg or vice versa. | supported | `source_c.md` | 'Es gibt jedoch keine Hinweise, dass sich das Rummy-Spiel aus dem Mah-Jongg entwickelt hätte oder umgekehrt.' in `source_c.md` -- Source_c.md explicitly states there is no evidence that Rummy developed from Mah-Jongg or vice versa. |
| 47 | Descent from a hypothetical common ancestor is not proven. | supported | `source_c.md` | 'Die Abstammung von einem (hypothetischen) gemeinsamen Vorfahren ist nicht erwiesen.' in `source_c.md` -- Source_c.md states that descent from a hypothetical common ancestor is not proven. |
| 48 | In better quality games, the game stones are made from two parts. | supported | `source_c.md` | 'Die Spielsteine sind bei den besseren Spielen aus zwei Teilen gearbeitet' in `source_c.md` -- Source_c.md states that in better quality games, the game stones are made from two parts. |
| 49 | The images on the front sides are engraved with chisels into a small block of bone – formerly ivory. | supported | `source_c.md` | 'die Bilder auf den Vorderseiten sind mit Sticheln in einen kleinen Block aus Bein – früher Elfenbein – eingraviert' in `source_c.md` -- Source_c.md states that the images on the front are engraved with chisels into a small block of bone – formerly ivory. |
| 50 | The images are colored. | supported | `source_c.md` | 'die Bilder auf den Vorderseiten sind mit Sticheln in einen kleinen Block aus Bein – früher Elfenbein – eingraviert und koloriert' in `source_c.md` -- Source_c.md states that the images are engraved and colored. |
| 51 | The back sides are made from bamboo. | supported | `source_c.md` | 'die Rückseiten sind aus Bambus' in `source_c.md` -- Source_c.md directly states that the back sides are made from bamboo in the description of Mah-Jongg game stones. |
| 52 | These two parts are usually not simply glued but riveted. | supported | `source_c.md` | 'diese beiden Teile sind üblicherweise nicht einfach verklebt, sondern verzinkt' in `source_c.md` -- Source_c.md explicitly states these two parts are usually not simply glued but riveted (verzinkt). |
| 53 | Cheaper game stones are made from printed wood or plastic. | supported | `source_c.md` | 'Die Steine preisgünstigerer Spiele sind aus bedrucktem Holz oder aus Kunststoff gefertigt.' in `source_c.md` -- Source_c.md directly states that cheaper game stones are made from printed wood or plastic. |
| 54 | Mah-Jongg card games exist. | supported | `source_c.md` | 'Es gibt auch Mah-Jongg-Kartenspiele.' in `source_c.md` -- Source_c.md explicitly confirms that Mah-Jongg card games exist. |
| 55 | In the 21st century, Mah-Jongg sets are increasingly marketed as design objects. | supported | `source_c.md` | 'Im 21. Jahrhundert werden Mah-Jongg-Sets zudem zunehmend als Designobjekte vermarktet' in `source_c.md` -- Source_c.md directly states that in the 21st century, Mah-Jongg sets are increasingly marketed as design objects. |
| 56 | Luxury brands like Hermès, Prada and Louis Vuitton offer their own versions. | supported | `source_c.md` | 'neben modern gestalteten thematischen Steinsätzen bieten auch Luxusmarken wie Hermès, Prada und Louis Vuitton eigene Ausführungen an' in `source_c.md` -- Source_c.md explicitly names Hermès, Prada and Louis Vuitton as luxury brands offering their own Mah-Jongg versions. |
| 57 | A Mah-Jongg game consists of 136 or 144 game stones, called tiles. | supported | `source_c.md` | 'Ein Mah-Jongg-Spiel besteht aus 136 oder 144 Spielsteinen, die Ziegel genannt werden' in `source_c.md` -- Source_c.md directly states that a Mah-Jongg game consists of 136 or 144 game stones called tiles. |
| 58 | Mah-Jongg is played in countless rule variants from Chinese Traditional to Jewish American. | supported | `source_c.md` | 'Mah-Jongg wird in unzähligen Regelvarianten von Chinese Traditional bis Jewish American gespielt.' in `source_c.md` -- Source_c.md explicitly confirms Mah-Jongg is played in countless rule variants from Chinese Traditional to Jewish American. |
| 59 | The Hua Bao Rules correspond to Joseph P. Babcock's rules except for a few differences. | supported | `source_c.md` | 'welche bis auf wenige Unterschiede den Regeln von Joseph P. Babcock entsprechen' in `source_c.md` -- Source_c.md states the Hua Bao Rules correspond to Joseph P. Babcock's rules except for a few differences. |
| 60 | The Hua Bao Rules represent the common core of the diverse variants. | supported | `source_c.md` | 'und den gemeinsamen Kern der mannigfaltigen Varianten darstellen' in `source_c.md` -- Source_c.md explicitly states the Hua Bao Rules represent the common core of the diverse variants. |
| 61 | The Hua Bao Rules are the common playing style in Europe. | supported | `source_c.md` | 'Diese ist die in Europa gängige Spielweise.' in `source_c.md` -- Source_c.md directly confirms the Hua Bao Rules are the common playing style in Europe. |
| 62 | In the standard variant, the game is played with 136 stones. | supported | `source_c.md` | 'In der Standard-Variante wird mit 136 Steinen gespielt' in `source_c.md` -- Source_c.md explicitly states that in the standard variant, the game is played with 136 stones. |
| 63 | In the standard variant, the eight tiles of the main suit are not used. | supported | `source_c.md` | 'die acht Ziegel der Hauptfarbe werden nicht verwendet' in `source_c.md` -- Source_c.md states that in the standard variant, the eight tiles of the main suit are not used. |
| 64 | Before the start of a game, the four players stand at the four sides of a square table. | supported | `source_c.md` | 'Vor Beginn einer Partie stehen die vier Spieler an den vier Seiten eines quadratischen Tisches.' in `source_c.md` -- Source_c.md directly confirms that before the start of a game, the four players stand at the four sides of a square table. |
| 65 | The oldest player mixes the four place stones face down and stacks them on top of each other. | supported | `source_c.md` | 'Der älteste Spieler mischt verdeckt die vier Platzsteine und stapelt sie aufeinander.' in `source_c.md` -- Source_c.md explicitly states the oldest player mixes the four place stones face down and stacks them on top of each other. |
| 66 | He then rolls two dice and counts the sum of the pips counterclockwise, starting with himself. | supported | `source_c.md` | 'Sodann wirft er zwei Würfel und zählt die Augensumme gegen den Uhrzeigersinn ab, wobei er bei sich selbst zu zählen beginnt.' in `source_c.md` -- Source_c.md directly states he rolls two dice and counts the sum counterclockwise, starting with himself. |
| 67 | The player thus determined takes the top place stone, the next one takes the second, etc. | supported | `source_c.md` | 'Der solcherart bestimmte Spieler nimmt den obersten Platzstein, der nächste den zweiten usw.' in `source_c.md` -- Source_c.md confirms the player thus determined takes the top place stone, the next one takes the second, etc. |
| 68 | The playing surface of the table is interpreted as a sky map. | supported | `source_c.md` | 'Die Spielfläche des Tisches wird als Himmelskarte interpretiert.' in `source_c.md` -- Source_c.md explicitly states the playing surface of the table is interpreted as a sky map. |
| 69 | The player who receives the East Wind place stone becomes the dealer in the first game and stays in place. | supported | `source_c.md` | 'Der Spieler, der den Platzstein Ostwind erhält, wird Spielleiter im ersten Spiel und bleibt an seinem Platz' in `source_c.md` -- Source_c.md directly states the player receiving East Wind becomes the dealer in the first game and stays in place. |
| 70 | West Wind sits opposite East Wind. | supported | `source_c.md` | 'Westwind setzt sich gegenüber' in `source_c.md` -- Source_c.md explicitly confirms West Wind sits opposite East Wind. |
| 71 | South Wind sits to the right of East Wind. | supported | `source_c.md` | 'Südwind zur Rechten (!) von Ostwind' in `source_c.md` -- Source_c.md directly states South Wind sits to the right of East Wind. |
| 72 | North Wind sits to the left of East Wind. | supported | `source_c.md` | 'Nordwind zur Linken' in `source_c.md` -- Source_c.md explicitly states North Wind sits to the left of East Wind. |
| 73 | The tiles are mixed face down on the table. | supported | `source_c.md` | 'Die Ziegel werden verdeckt auf dem Tisch gemischt.' in `source_c.md` -- Source_c.md directly confirms the tiles are mixed face down on the table. |
| 74 | Each of the four players builds one side of the wall by taking 34 of the tiles face down. | supported | `source_c.md` | 'Anschließend baut jeder der vier Spieler eine Seite der Mauer, indem er 34 der Ziegel verdeckt nimmt' in `source_c.md` -- Source_c.md explicitly states each of the four players builds one side of the wall by taking 34 of the tiles face down. |
| 75 | Each player arranges their tiles into a wall 17 tiles long and two tiles high. | supported | `source_c.md` | 'zu einer 17 Ziegel langen und zwei Ziegel hohen Mauer anordnet' in `source_c.md` -- Source_c.md directly states each player arranges their tiles into a wall 17 tiles long and two tiles high. |
| 76 | When playing with flower and season tiles, each player takes 36 tiles. | supported | `source_c.md` | 'Wird mit Blumen- und Jahreszeitenziegeln gespielt, so nimmt jeder Spieler 36 Ziegel' in `source_c.md` -- Source_c.md directly states that when playing with flower and season tiles, each player takes 36 tiles. |
| 77 | When playing with flower and season tiles, the wall width is 18 stacks. | supported | `source_c.md` | 'die Breite der Mauer beträgt 18 Stapel' in `source_c.md` -- Source_c.md explicitly states that when playing with flower and season tiles, the wall width is 18 stacks. |
| 78 | The four wall sections are pushed together so they touch at the corners and form a square. | supported | `source_c.md` | 'Die vier Mauerstücke werden zusammengeschoben, so dass sie sich an den Ecken berühren und ein Quadrat bilden.' in `source_c.md` -- Source_c.md directly states that the four wall sections are pushed together so they touch at the corners and form a square. |
| 79 | Outside of Asian countries, this is sometimes called the Chinese Wall. | supported | `source_c.md` | 'Außerhalb der asiatischen Länder wird dies manchmal Chinesische Mauer genannt.' in `source_c.md` -- Source_c.md directly states that outside of Asian countries, this is sometimes called the Chinese Wall (Chinesische Mauer). |
| 80 | East Wind now rolls the two dice and counts the sum of the pips counterclockwise at the players, starting with himself. | supported | `source_c.md` | 'Nun wirft Ostwind die zwei Würfel und zählt wie vorhin, bei sich selbst beginnend, die Augensumme gegen den Uhrzeigersinn an den Spielern ab.' in `source_c.md` -- Source_c.md states that East Wind rolls the two dice and counts the sum counterclockwise at the players, starting with himself. |
| 81 | The player thus determined also rolls both dice and counts the sum of the pips of both rolls together. | supported | `source_c.md` | 'Der so bestimmte Spieler wirft ebenfalls beide Würfel und zählt die Augensumme beider Würfe zusammen.' in `source_c.md` -- Source_c.md states that the determined player also rolls both dice and counts the sum of the pips of both rolls together. |
| 82 | East Wind counts off tile stacks at the right end of the wall in front of him, clockwise, according to the total sum. | supported | `source_c.md` | 'Ostwind zählt am rechten Ende der vor ihm befindlichen Mauer beginnend im Uhrzeigersinn der Gesamtsumme entsprechend Ziegelstapel ab.' in `source_c.md` -- Source_c.md states that East Wind counts off tile stacks at the right end of the wall in front of him, clockwise, according to the total sum. |
| 83 | If necessary, East Wind continues the count with tiles from the wall of his left neighbor. | supported | `source_c.md` | 'Eventuell setzt er die Zählung mit Ziegeln aus der Mauer seines linken Nachbarn fort.' in `source_c.md` -- Source_c.md states that if necessary, East Wind continues the count with tiles from the wall of his left neighbor. |
| 84 | East Wind takes out the determined stack (wall break) and places it on the stack to the right of the resulting gap. | supported | `source_c.md` | 'Den so bestimmten Stapel nimmt er heraus (Mauerdurchbruch) und stellt ihn auf den Stapel rechts neben der entstandenen Lücke.' in `source_c.md` -- Source_c.md states that East Wind takes out the determined stack (wall break) and places it on the stack to the right of the resulting gap. |
| 85 | The removed stones are called loose tiles and mark the dead end of the wall. | supported | `source_c.md` | 'Die herausgenommenen Steine heißen lose Ziegel und markieren das tote Ende der Mauer' in `source_c.md` -- Source_c.md directly states that the removed stones are called loose tiles and mark the dead end of the wall. |
| 86 | The end to the left of the gap is the living end of the wall. | supported | `source_c.md` | 'das Ende links der Lücke ist das lebende Ende der Mauer' in `source_c.md` -- Source_c.md directly states that the end to the left of the gap is the living end of the wall. |
| 87 | Tiles are drawn regularly from the living end of the wall. | supported | `source_c.md` | 'Gezogen werden die Steine regulär vom lebenden Ende der Mauer.' in `source_c.md` -- Source_c.md states that tiles are drawn regularly from the living end of the wall. |
| 88 | Replacement tiles are taken from the dead end, starting with the two loose tiles. | supported | `source_c.md` | 'Vom toten Ende werden dagegen nur Ersatzziegel (siehe unten) genommen, beginnend mit den beiden losen Ziegeln.' in `source_c.md` -- Source_c.md states that replacement tiles are taken from the dead end, starting with the two loose tiles. |
| 89 | The players take each two stacks of two tiles from the living end of the wall three times in turn counterclockwise, with East Wind serving first. | supported | `source_c.md` | 'Die Spieler nehmen dreimal reihum gegen den Uhrzeigersinn jeder zwei Stapel zu zwei Ziegel vom lebenden Ende der Mauer, wobei sich Ostwind als erster bedient.' in `source_c.md` -- Source_c.md states that the players take each two stacks of two tiles from the living end of the wall three times in turn counterclockwise, with East Wind serving first. |
| 90 | Finally, each player takes one additional, thirteenth tile. | supported | `source_c.md` | 'Zuletzt nimmt jeder Spieler noch einen weiteren, dreizehnten' in `source_c.md` -- Source_c.md states that finally, each player takes one additional, thirteenth tile. |
| 91 | East Wind takes an additional fourteenth tile. | supported | `source_c.md` | 'und Ostwind außerdem einen vierzehnten Ziegel' in `source_c.md` -- Source_c.md states that East Wind takes an additional fourteenth tile. |
| 92 | Each of the four players tries to improve his original hand by drawing and discarding stones. | supported | `source_c.md` | 'Jeder der vier Spieler versucht, durch Ziehen und Abwerfen von Steinen seine ursprüngliche Hand zu verbessern' in `source_c.md` -- Source_c.md states that each of the four players tries to improve his original hand by drawing and discarding stones. |
| 93 | Each player tries to form a complete game picture of the most valuable figures possible. | supported | `source_c.md` | 'und ein vollständiges Spielbild aus möglichst wertvollen Figuren zu formen' in `source_c.md` -- Source_c.md states that each player tries to form a complete game picture of the most valuable figures possible. |
| 94 | Stones are drawn from the wall or taken after another player's discard. | supported | `source_c.md` | 'Steine werden von der Mauer gezogen oder nach Abwurf eines anderen Spielers aufgenommen.' in `source_c.md` -- Source_c.md states that stones are drawn from the wall or taken after another player's discard. |
| 95 | When a player has formed a complete game picture consisting of four figures and finally a pair, he may call "Mah-Jongg" and end the game. | supported | `source_c.md` | 'Hat ein Spieler ein vollständiges Spielbild bestehend aus vier Figuren und schließlich einem Paar gebildet, so darf er "Mah-Jongg" rufen und das Spiel beenden.' in `source_c.md`, **transcription_error** -- Source_c.md states that when a player has formed a complete game picture consisting of four figures and finally a pair, he may call Mah-Jongg and end the game. |
| 96 | The four figures can be either triplets, quadruplets or sequences. | supported | `source_c.md` | 'Die vier Figuren können wahlweise Drillinge, Vierlinge oder Folgen sein.' in `source_c.md` -- Source_c.md states that the four figures can be either triplets, quadruplets or sequences. |
| 97 | A pair consists of two identical stones, for example twice Bamboo-Five or two green dragons etc. | supported | `source_c.md` | 'Ein Paar besteht aus zwei gleichen Steinen, z. B. zweimal Bambus-Fünf oder zwei grüne Drachen etc.' in `source_c.md` -- Source_c.md directly states that a pair consists of two identical stones, for example twice Bamboo-Five or two green dragons etc. |
| 98 | To call Mah-Jongg, a complete game picture is necessary. | supported | `source_c.md` | 'Um Mah-Jongg rufen zu können, ist ein vollständiges Spielbild nötig' in `source_c.md` -- Source_c.md states that to call Mah-Jongg, a complete game picture is necessary. |
| 99 | A complete game picture must contain exactly one pair, the final pair (將, jiàng, sometimes 眼, yǎn). | supported | `source_c.md` | 'in diesem muss genau ein Paar, das Schlusspaar (將, jiàng, manchmal 眼, yǎn), enthalten sein.' in `source_c.md` -- Source_c.md states that a complete game picture must contain exactly one pair, the final pair (將, jiàng, sometimes 眼, yǎn). |
| 100 | To complete a pair, a discarded stone may only be called if Mah-Jongg is called at the same time. | supported | `source_c.md` | 'Zur Vervollständigung eines Paares darf ein abgelegter Stein nur aufgerufen werden, wenn gleichzeitig Mah-Jongg gerufen wird.' in `source_c.md` -- Source_c.md states that to complete a pair, a discarded stone may only be called if Mah-Jongg is called at the same time. |
| 101 | A Pong (碰, pèng) consists of three identical stones. | supported | `source_c.md` | 'Ein Pong (碰, pèng) besteht aus drei gleichen Steinen.' in `source_c.md` -- Source_c.md directly states that a Pong consists of three identical stones, matching the claim exactly. |
| 102 | If a Pong is formed exclusively from tiles from the original hand or tiles drawn from the wall, it is a concealed Pong that does not need to be announced. | supported | `source_c.md` | 'Wird ein Pong ausschließlich aus Ziegeln der ursprünglichen Hand oder von der Mauer gezogenen Ziegeln gebildet, so handelt es sich um einen verdeckten Pong, der nicht gemeldet werden muss.' in `source_c.md` -- Source_c.md states that if a Pong is formed exclusively from tiles of the original hand or tiles drawn from the wall, it is a concealed Pong that does not need to be announced. |
| 103 | If a concealed Pong is revealed, one of the stones should be turned over to mark it as actually concealed. | supported | `source_c.md` | 'Wird er dennoch aufgedeckt, so sollte er durch ein Umdrehen eines der Steine als eigentlich verdeckt markiert werden.' in `source_c.md` -- Source_c.md states that if a concealed Pong is revealed, one of the stones should be turned over to mark it as actually concealed. |
| 104 | If a player has a pair and the third stone is discarded by any other player, the player may call this stone with the call "Pong". | supported | `source_c.md` | 'Besitzt ein Spieler ein Paar und wird der dritte Stein von einem beliebigen anderen Spieler abgelegt, so darf der Spieler diesen Stein mit dem Ruf "Pong" aufrufen.' in `source_c.md`, **transcription_error** -- Source_c.md directly states that if a player has a pair and the third stone is discarded by any other player, the player may call this stone with the call "Pong". |
| 105 | The player lays his pair and the called tile openly on the table and possesses an open Pong. | supported | `source_c.md` | 'Er legt sein Paar und den aufgerufenen Ziegel offen vor sich auf den Tisch und besitzt einen offenen Pong.' in `source_c.md` -- Source_c.md states that the player lays his pair and the called tile openly on the table and possesses an open Pong. |
| 106 | In the 1970s and 1980s, the term Pon was often used instead of Pong in German-speaking countries. | supported | `source_c.md` | 'In den 1970er und 1980er Jahren wurde im deutschsprachigen Raum statt Pong oftmals der Begriff Pon verwendet.' in `source_c.md` -- Source_c.md directly states that in the 1970s and 1980s, the term Pon was often used instead of Pong in German-speaking countries. |
| 107 | The 1982 instruction book by Ursula Eschenbach uses the terms Pon, Kan and Chii throughout. | supported | `source_c.md` | 'Auch in dem 1982 erschienenen Anleitungsbuch von Ursula Eschenbach ist durchgehend von Pon, Kan und Chii die Rede.' in `source_c.md` -- Source_c.md states that the 1982 instruction book by Ursula Eschenbach uses the terms Pon, Kan and Chii throughout. |
| 108 | The terms Pon (jap. ポン, 碰 pon), Kan (カン, 槓, 杠 kan) or Chii (チー, 吃 chī) come from the Japanese variant of Riichi Mahjong. | supported | `source_c.md` | 'Die Begriffe Pon (jap. ポン, 碰 pon), Kan (カン, 槓, 杠 kan) oder Chii (チー, 吃 chī) stammen aus der japanischen Spielart des Riichi Mahjong (リーチ麻雀, 立直マージャン rīchi mājan).' in `source_c.md` -- Source_c.md directly states that the terms Pon, Kan and Chii come from the Japanese variant of Riichi Mahjong. |
| 109 | A Kong (槓 / 杠, gàng) consists of four identical stones. | supported | `source_c.md` | 'Ein Kong (槓 / 杠, gàng) besteht aus vier gleichen Steinen.' in `source_c.md` -- Source_c.md directly states that a Kong consists of four identical stones. |
| 110 | If a Kong is formed exclusively from stones from the original hand and tiles drawn from the wall, the player should announce a concealed Kong. | supported | `source_c.md` | 'Wird ein Kong ausschließlich aus Steinen der ursprünglichen Hand und von der Mauer gezogenen Ziegeln gebildet, so sollte der Spieler einen verdeckten Kong melden.' in `source_c.md` -- Source_c.md states that if a Kong is formed exclusively from stones from the original hand and tiles drawn from the wall, the player should announce a concealed Kong. |
| 111 | If a concealed Kong is not announced, the player cannot draw a replacement tile from the wall, which is necessary for Kongs to achieve a complete game picture. | supported | `source_c.md` | 'Tut er dies nicht, so kann er keinen Ersatzziegel aus der Mauer ziehen, der bei Kongs notwendig ist, um ein komplettes Spielbild zu erreichen.' in `source_c.md` -- Source_c.md states that if a concealed Kong is not announced, the player cannot draw a replacement tile from the wall, which is necessary for Kongs to achieve a complete game picture. |
| 112 | If the game ends before the player announces the quad, the concealed Kong is valued as a concealed Pong. | supported | `source_c.md` | 'Wird das Spiel beendet, bevor der Spieler den Vierling meldet, so wird der verdeckte Kong als verdeckter Pong gewertet.' in `source_c.md` -- Source_c.md states that if the game ends before the player announces the quad, the concealed Kong is valued as a concealed Pong. |
| 113 | A concealed Kong does not have to be announced immediately but can also be laid out later when the player's turn comes again. | supported | `source_c.md` | 'Ein verdeckter Kong muss nicht sofort gemeldet werden, sondern kann auch später herausgelegt werden, wenn der Spieler erneut am Zug ist.' in `source_c.md` -- Source_c.md states that a concealed Kong does not have to be announced immediately but can also be laid out later when the player's turn comes again. |
| 114 | When announcing, the four stones are laid out openly and the two outer stones are placed face down to indicate that it is a concealed (also: "half-concealed", or "announced from hand") Kong. | supported | `source_c.md` | 'Bei der Meldung werden die vier Steine offen ausgelegt und zum Zeichen, dass es sich um einen verdeckten (auch: "halbverdeckten", oder "aus der Hand gemeldeten") Kong handelt, werden die beiden äußeren Steine mit der Rückseite nach oben gelegt.' in `source_c.md`, **transcription_error** -- Source_c.md states that when announcing, the four stones are laid out openly and the two outer stones are placed face down to indicate a concealed Kong. |
| 115 | If a player holds three identical stones in hand – that is, a concealed Pong – he may claim the fourth stone with the call "Kong" when another player discards it. | supported | `source_c.md` | 'Hält ein Spieler drei gleiche Steine in der Hand – also einen verdeckten Pong – so darf er, wenn ein Spieler den vierten Stein ablegt, diesen Ziegel mit dem Ruf "Kong" für sich beanspruchen' in `source_c.md`, **transcription_error** -- Source_c.md states that if a player holds three identical stones in hand (a concealed Pong) he may claim the fourth stone with the call "Kong" when another player discards it. |
| 116 | When claiming the fourth stone this way, a player obtains an open Kong. | supported | `source_c.md` | 'und erhält so einen offenen Kong.' in `source_c.md` -- Source_c.md states that when claiming the fourth stone this way, a player obtains an open Kong. |
| 117 | If a player has already announced an open Pong and the missing fourth stone is discarded by another player, this tile cannot be called to complete the Kong. | supported | `source_c.md` | 'Hat ein Spieler bereits einen offenen Pong gemeldet und wird der fehlende vierte Stein von einem anderen Spieler abgelegt, so kann dieser Ziegel nicht zur Komplettierung des Kongs aufgerufen werden.' in `source_c.md` -- Source_c.md states that if a player has already announced an open Pong and the missing fourth stone is discarded by another player, this tile cannot be called to complete the Kong. |
| 118 | If a player has already announced a Pong and draws the missing fourth stone from the wall, he may attach it to the Pong and thus has an open Kong. | supported | `source_c.md` | 'Hat ein Spieler bereits einen Pong gemeldet und zieht er den fehlenden vierten Stein von der Mauer, so darf er ihn an den Pong anlegen und besitzt damit einen offenen Kong.' in `source_c.md` -- Source_c.md states that if a player has already announced a Pong and draws the missing fourth stone from the wall, he may attach it to the Pong and thus has an open Kong. |
| 119 | In this situation, a robbing of the Kong can occur. | supported | `source_c.md` | 'In dieser Situation kann es zu einer Beraubung des Kong kommen.' in `source_c.md` -- Source_c.md states that in this situation, a robbing of the Kong can occur. |
| 120 | The stone drawn from the wall can be demanded by another player if he can call "Mah-Jongg" with it. | supported | `source_c.md` | 'Der von der Mauer gezogene Stein kann von einem anderen Spieler für sich gefordert werden, wenn er damit "Mah-Jongg" rufen kann.' in `source_c.md`, **transcription_error** -- Source_c.md states that the stone drawn from the wall can be demanded by another player if he can call "Mah-Jongg" with it. |
| 121 | For this robbing of the Kong, the player receives an additional bonus of 10 points. | supported | `source_a.md` | 'Für diese Beraubung des Kong erhält er einen zusätzlichen Bonus von 10 Punkten.' in `source_a.md` -- Source_a.md states that for this robbing of the Kong, the player receives an additional bonus of 10 points. |
| 122 | As soon as a player announces an open or concealed Kong, he must draw a replacement tile from the dead end of the wall. | supported | `source_c.md` | 'Sobald ein Spieler einen offenen oder verdeckten Kong meldet, muss er einen Ersatzziegel vom toten Ende der Mauer ziehen.' in `source_c.md` -- Source_c.md states that as soon as a player announces an open or concealed Kong, he must draw a replacement tile from the dead end of the wall. |
| 123 | A Chow (吃, chī, sometimes 上, shàng) is a sequence of exactly three consecutive stones of a base suit. | supported | `source_c.md` | 'Ein Chow (吃, chī, manchmal 上, shàng) ist eine Sequenz aus genau drei aufeinanderfolgenden Steinen einer Grundfarbe' in `source_c.md` -- Source_c.md states that a Chow is a sequence of exactly three consecutive stones of a base suit. |
| 124 | Sequences of more than three stones are not permitted. | supported | `source_c.md` | 'Sequenzen aus mehr als drei Steinen sind nicht gestattet.' in `source_c.md` -- Source_c.md states that sequences of more than three stones are not permitted. |
| 125 | A Chow from stones of the trump suit is not possible. | supported | `source_c.md` | 'Ein Chow aus Steinen der Trumpffarbe ist nicht möglich.' in `source_c.md` -- Source_c.md states that a Chow from stones of the trump suit is not possible. |
| 126 | A discarded stone can be called by a player with "Chow" if the player sits immediately to the right of the player who discarded the stone. | supported | `source_c.md` | 'Ein abgelegter Stein kann von einem Spieler mit "Chow" aufgerufen werden, wenn der Spieler unmittelbar zur Rechten desjenigen Spielers sitzt, der den betreffenden Stein abgelegt hat.' in `source_c.md`, **transcription_error** -- The claim directly matches the source text about calling a Chow when sitting immediately to the right of the player who discarded the stone. |
| 127 | The calling player then lays out the sequence formed with it openly. | supported | `source_c.md` | 'Der aufrufende Spieler legt dann die damit gebildete Folge offen.' in `source_c.md` -- The source states the calling player lays out the sequence formed with it openly, matching the claim exactly. |
| 128 | Another player can only call a discarded stone for a sequence if he calls Mah-Jongg at the same time. | supported | `source_c.md` | 'Ein anderer Spieler kann nur dann einen abgelegten Stein für eine Folge aufrufen, wenn er gleichzeitig Mah-Jongg ruft.' in `source_c.md` -- The source directly states another player can only call a discarded stone for a sequence if calling Mah-Jongg simultaneously. |
| 129 | Sequences formed from stones from the original hand or drawn stones can remain concealed until the end of the game. | supported | `source_c.md` | 'Folgen, die aus Steinen der ursprünglichen Hand bzw. aus gezogenen Steinen gebildet werden, können bis zum Spielende verdeckt bleiben.' in `source_c.md` -- The source directly states sequences formed from original hand or drawn stones can remain concealed until the end of the game. |
| 130 | Mah-Jongg is played counterclockwise. | supported | `source_c.md` | 'Mah-Jongg wird gegen den Uhrzeigersinn gespielt.' in `source_c.md` -- The source directly states Mah-Jongg is played counterclockwise. |
| 131 | After East Wind has taken his 14 tiles, he begins the game by discarding a stone openly in the middle of the table after any announcements, naming its name. | supported | `source_c.md` | 'Nachdem sich Ostwind seine 14 Ziegel genommen hat, beginnt er das Spiel, indem er nach einer eventuellen Meldung einen Stein offen in der Mitte des Tisches ablegt, dabei nennt er dessen Namen.' in `source_c.md` -- The source states East Wind begins the game by discarding a stone openly in the middle of the table after any announcements, naming its name. |
| 132 | If no player calls the discarded stone, the right neighbor draws a stone from the living end of the wall. | supported | `source_c.md` | 'Wenn kein Spieler den abgelegten Stein aufruft, so zieht der rechte Nachbar einen Stein vom lebenden Ende der Mauer' in `source_c.md` -- The source directly states if no player calls the discarded stone, the right neighbor draws a stone from the living end of the wall. |
| 133 | The right neighbor announces figures if he wishes and finally discards a stone. | supported | `source_c.md` | 'meldet, wenn er möchte, eine oder mehrere Figuren und legt zuletzt einen Stein ab.' in `source_c.md` -- The source states the right neighbor announces figures if desired and finally discards a stone. |
| 134 | When a stone is discarded, it is dead and remains openly in the middle of the table. | supported | `source_c.md` | 'Wird ein Stein abgelegt, so ist er tot, er bleibt offen in der Mitte des Tisches liegen' in `source_c.md` -- The source directly states when a stone is discarded it is dead and remains openly in the middle of the table. |
| 135 | The next player can play a Chow, and that player and all further players can play a Pong or Kong. | supported | `source_c.md` | 'der nächste Spieler kann einen Chow spielen, sowie jener und alle weiteren Spieler einen Pong oder einen Kong.' in `source_c.md` -- The source states the next player can play a Chow and that player and all further players can play a Pong or Kong. |
| 136 | After that, the stone is no longer available for play or can be taken. | supported | `source_c.md` | 'Danach ist der Stein nicht mehr für das Spiel verfügbar beziehungsweise aufnehmbar.' in `source_c.md` -- The source directly states after that the stone is no longer available for play or can be taken. |
| 137 | If a stone is called by a player, the player takes the discarded stone and must lay out the relevant figure openly. | supported | `source_c.md` | 'Wird ein Stein von einem Spieler aufgerufen, so nimmt der Spieler den abgelegten Stein und muss die betreffende Figur offen auflegen.' in `source_c.md` -- The source directly states if a stone is called by a player, the player takes the stone and must lay out the figure openly. |
| 138 | Then he discards a stone and the game continues with this player. | supported | `source_c.md` | 'Danach wirft er einen Stein ab, und das Spiel wird mit diesem Spieler fortgesetzt.' in `source_c.md` -- The source states then he discards a stone and the game continues with this player. |
| 139 | In this way, players can also be skipped. | supported | `source_c.md` | 'Auf diese Weise können auch Spieler übergangen werden' in `source_c.md` -- The source directly states in this way players can also be skipped. |
| 140 | If a tile is called by multiple players, the following ranking applies: If a player needs the stone for a Mah-Jongg call, he has priority over a Kong or Pong call. | supported | `source_c.md` | 'Benötigt ein Spieler den Stein für einen Mah-Jongg-Ruf, so hat er Vorrang gegenüber einem Kong- oder Pong-Ruf' in `source_c.md` -- The source states if a player needs the stone for a Mah-Jongg call, he has priority over Kong or Pong calls. |
| 141 | Kong and Pong calls have priority over a Chow. | supported | `source_c.md` | 'diese wiederum haben Vorrang vor einem Chow.' in `source_c.md` -- The source directly states Kong and Pong calls have priority over a Chow. |
| 143 | The stones are mixed again and the game is repeated with unchanged roles. | supported | `source_c.md` | 'die Steine werden erneut gemischt und das Spiel mit unveränderten Rollen wiederholt.' in `source_c.md` -- The source directly states the stones are mixed again and the game is repeated with unchanged roles. |
| 144 | Hidden combinations count double. | supported | `source_c.md` | 'Verdeckte Kombinationen zählen das Doppelte.' in `source_c.md` -- The source states hidden combinations count double. |
| 145 | A Kong counts four times as much as the corresponding Pong. | supported | `source_c.md` | 'Ein Kong zählt viermal so viel wie der entsprechende Pong.' in `source_c.md` -- The source directly states a Kong counts four times as much as the corresponding Pong. |
| 146 | The Mah-Jongg caller receives an additional premium of 10 (often 20) points. | supported | `source_a.md` | 'Der Mah-Jongg-Rufer erhält eine zusätzliche Prämie von 10 (häufig 20) Punkten gutgeschrieben.' in `source_a.md` -- The source states the Mah-Jongg caller receives an additional premium of 10 (often 20) points. |
| 147 | After evaluating the individual figures, a player may double the point value one or more times. | supported | `source_a.md` | 'Nach der Bewertung der einzelnen Figuren darf ein Spieler den Punktewert eventuell noch ein oder mehrere Male verdoppeln.' in `source_a.md` -- The source states after evaluating individual figures, a player may double the point value one or more times. |
| 148 | Doublings are calculated in succession. | supported | `source_a.md` | 'Die Verdopplungen werden nacheinander gerechnet' in `source_a.md` -- The source directly states doublings are calculated in succession. |
| 149 | Doubling twice, for example, quadruples the original value of the game picture. | supported | `source_a.md` | 'zweimaliges Verdoppeln vervierfacht beispielsweise den ursprünglichen Wert des Spielbildes.' in `source_a.md` -- The source states doubling twice, for example, quadruples the original value of the game picture. |
| 150 | Due to the many doublings, the point values of the game pictures can reach very large values. | supported | `source_a.md` | 'Infolge der mannigfachen Verdopplungen können die Punktezahlen der Spielbilder sehr große Werte erreichen' in `source_a.md` -- The source states due to the many doublings, the point values of the game pictures can reach very large values. |
| 151 | Usually a limit is agreed upon. | supported | `source_a.md` | 'üblicherweise ein Limit vereinbart wird' in `source_a.md` -- Source A states that a limit is usually agreed upon, which matches the claim's assertion. |
| 152 | This limit is usually 300 or 500 points. | supported | `source_a.md` | 'Dieses beträgt meist 300 oder 500 Punkte.' in `source_a.md` -- Source A explicitly states the limit is usually 300 or 500 points, matching the claim exactly. |
| 153 | If the calculated point value exceeds the agreed limit, the game picture is only counted at this maximum value. | supported | `source_a.md` | 'Übersteigt der errechnete Punktewert das vereinbarte Limit, so wird das Spielbild nur mit diesem Höchstwert gezählt.' in `source_a.md` -- Source A states that if the calculated point value exceeds the agreed limit, the game picture is only counted at this maximum value. |
| 154 | If the game picture of the Mah-Jongg caller consists exclusively of tiles of the trump suit, consisting only of wind and dragon tiles, this hand is valued at the maximum point value. | supported | `source_a.md` | 'Besteht das Spielbild des Mah-Jongg-Rufers ausschließlich aus Ziegeln der Trumpffarbe, also nur aus Wind- und Drachenziegeln, so wird diese Hand mit dem Punktemaximum bewertet.' in `source_a.md` -- Source A directly states this claim about hands consisting exclusively of wind and dragon tiles being valued at maximum points. |
| 155 | If East Wind can call Mah-Jongg immediately after taking his tiles, he has the blessing of heaven and receives the maximum point value. | supported | `source_a.md` | 'Kann Ostwind sofort nach Aufnehmen seiner Ziegel Mah-Jongg rufen, so besitzt er den Segen des Himmels und erhält das Punktemaximum gutgeschrieben.' in `source_a.md` -- Source A explicitly describes the blessing of heaven scenario and its consequence of receiving maximum points. |
| 156 | If another player can call the first stone discarded by East Wind and declare Mah-Jongg, this is the blessing of the earth. | supported | `source_a.md` | 'Kann ein anderer Spieler den ersten von Ostwind abgelegten Stein aufrufen und damit Mah-Jongg erklären, so ist dies der Segen der Erde' in `source_a.md` -- Source A defines the blessing of the earth as when another player calls the first stone discarded by East Wind and declares Mah-Jongg. |
| 157 | The player with the blessing of the earth receives half of the limit. | supported | `source_a.md` | 'und der Spieler erhält die Hälfte des Limits gutgeschrieben.' in `source_a.md` -- Source A states that the player with the blessing of the earth receives half the limit, matching the claim. |
| 158 | Many rule books contain further point bonuses or doublings for special features of the Mah-Jongg caller's game picture. | supported | `source_a.md` | 'In vielen Regelbüchern finden sich weitere Punkteprämien oder Verdopplungen für Besonderheiten des Spielbildes des Mah-Jongg-Rufers.' in `source_a.md` -- Source A states that many rule books contain further point bonuses or doublings for special features of the Mah-Jongg caller's game picture. |
| 159 | Such variations should definitely be clarified before the start of the game. | supported | `source_a.md` | 'Solche Variationen sollten unbedingt vor Beginn des Spiels geklärt werden.' in `source_a.md` -- Source A directly states that such variations should definitely be clarified before the start of the game. |
| 160 | If Mah-Jongg is played with 144 stones, including the stones of the main suit (flower and season tiles), each side of the wall consists of 18 tile stacks. | supported | `source_a.md` | 'Wird Mah-Jongg mit 144 Steinen, also einschließlich der Steine der Hauptfarbe (der Blumen- und Jahreszeitenziegel), gespielt, so besteht jede Seite der Mauer aus 18 Ziegelstapeln.' in `source_a.md` -- Source A explicitly states that when played with 144 stones including flower and season tiles, each side has 18 tile stacks. |
| 161 | When a player picks up his stones at the beginning of a game, he lays his flower and season tiles openly in front of him and draws a replacement tile from the dead end of the wall. | supported | `source_a.md` | 'Sobald ein Spieler zu Beginn eines Spieles seine Steine aufnimmt, legt er seine Blumen- und Jahreszeitenziegel offen vor sich und zieht dafür einen Ersatzziegel vom toten Ende der Mauer' in `source_a.md` -- Source A describes the procedure of laying flower and season tiles openly and drawing a replacement tile from the dead end. |
| 162 | The same procedure is followed if a player draws such a stone from the wall. | supported | `source_a.md` | 'ebenso wird verfahren, wenn ein Spieler einen solchen Stein von der Mauer kauft.' in `source_a.md` -- Source A states the same procedure is followed if a player draws such a stone from the wall. |
| 163 | The stones of the main suit are assigned to the four winds: Nr. 1 applies to East Wind, Nr. 2 to South Wind, Nr. 3 to West Wind and Nr. 4. to North Wind. | supported | `source_a.md` | 'Die Ziegel der Hauptfarbe sind den vier Winden zugeordnet: Nr. 1 gilt für den Ostwind, Nr. 2 für den Südwind, Nr. 3 für den Westwind und Nr. 4. für den Nordwind.' in `source_a.md` -- Source A assigns the main suit stones to the four winds exactly as the claim states. |
| 164 | If East Wind can call Mah-Jongg, he remains East Wind in the next game and the other positions remain unchanged. | supported | `source_a.md` | 'Wenn Ostwind Mah-Jongg rufen kann, so bleibt er im nächsten Spiel weiter Ostwind und auch die übrigen Positionen bleiben unverändert.' in `source_a.md` -- Source A states that if East Wind calls Mah-Jongg, he remains East Wind and other positions stay unchanged. |
| 165 | If another player calls Mah-Jongg, the previous South Wind takes on the role of East Wind. | supported | `source_a.md` | 'Wenn ein anderer Spieler Mah-Jongg ruft, so übernimmt der bisherige Südwind die Rolle von Ostwind' in `source_a.md` -- Source A states that if another player calls Mah-Jongg, the previous South Wind takes on the role of East Wind. |
| 166 | The positions change one place counterclockwise. | supported | `source_a.md` | 'und die Positionen wechseln um einen Platz gegen den Uhrzeigersinn.' in `source_a.md` -- Source A directly states that positions change one place counterclockwise. |
| 167 | A round is completed as soon as the player who held the North Wind position in the first game loses a game as East Wind. | supported | `source_a.md` | 'Eine Runde ist beendet, sobald der Spieler, der im ersten Spiel die Position des Nordwindes innehatte, ein Spiel als Ostwind verliert' in `source_a.md` -- Source A describes when a round ends: when the player who held North Wind in the first game loses as East Wind. |
| 168 | At this point, East Wind from the first game would again become East Wind. | supported | `source_a.md` | '– es würde Ostwind des ersten Spieles wiederum zu Ostwind.' in `source_a.md` -- Source A clarifies that East Wind from the first game would again become East Wind at this point. |
| 169 | A round consists of at least four games. | supported | `source_a.md` | 'Eine Runde besteht aus mindestens vier Spielen.' in `source_a.md` -- Source A explicitly states that a round consists of at least four games. |
| 170 | If not just a single round is played, but a match is agreed upon, it consists of four rounds. | supported | `source_a.md` | 'Wird nicht nur eine einzelne Runde gespielt, sondern eine Partie vereinbart, so besteht diese aus vier Runden.' in `source_a.md` -- Source A states that if a match is agreed upon instead of a single round, it consists of four rounds. |
| 171 | In the first round, the East Wind round, East is the prevailing wind (round wind). | supported | `source_a.md` | 'In der ersten Runde, der Ostwindrunde, ist Ost der vorherrschende Wind (Rundenwind)' in `source_a.md` -- Source A describes the first round as the East Wind round with East as the prevailing wind. |
| 172 | In the second round (South Wind round), South Wind prevails. | supported | `source_a.md` | 'in der zweiten Runde (Südwindrunde) herrscht Südwind vor' in `source_a.md` -- Source A explicitly states that in the second round (South Wind round), South Wind prevails. |
| 173 | The third round is the West Wind round. | supported | `source_a.md` | 'die dritte Runde ist die Westwindrunde' in `source_a.md` -- Source A directly states that the third round is the West Wind round. |
| 174 | The fourth round is the North Wind round. | supported | `source_a.md` | 'und die vierte die Nordwindrunde.' in `source_a.md` -- Source A explicitly states that the fourth round is the North Wind round. |
| 175 | The prevailing wind is significant when settling the game picture. | supported | `source_a.md` | 'Der vorherrschende Wind ist bei der Abrechnung des Spielbildes von Bedeutung:' in `source_a.md` -- Source A states that the prevailing wind is significant when settling the game picture. |
| 176 | To count individual games and rounds, a small box (Mingg) is used. | supported | `source_a.md` | 'Um die einzelnen Spiele und Runden mitzuzählen, wird eine kleine Dose (Mingg)verwendet.' in `source_a.md` -- Source_a.md directly states that a small box (Mingg) is used to count individual games and rounds. |
| 177 | The player who is East Wind places this box in front of him on the table. | supported | `source_a.md` | 'Diese stellt der jeweilige Spieler des Ostwindes vor sich auf den Tisch' in `source_a.md` -- Source_a.md states that the player of East Wind places this box in front of him on the table. |
| 178 | The place stone of the prevailing wind is placed on top of the Mingg. | supported | `source_a.md` | 'der Platzstein des vorherrschenden Windes wird oben auf die Mingg gelegt.' in `source_a.md` -- Source_a.md directly states that the place stone of the prevailing wind is placed on top of the Mingg. |
| 179 | Before another match, the seats are drawn anew. | supported | `source_a.md` | 'Vor einer weiteren Partie werden die Sitzplätze neu gelost' in `source_a.md` -- Source_a.md states that before another match, the seats are drawn anew. |
| 180 | Usually, no more than two matches are played. | supported | `source_a.md` | 'meist werden nicht mehr als zwei Partien gespielt.' in `source_a.md` -- Source_a.md states that usually no more than two matches are played. |
| 181 | In the traditional Chinese game, certain game pictures are valued at the maximum point value (limit). | supported | `source_a.md` | 'Im traditionellen chinesischen Spiel werden bestimmte Spielbilder mit dem Punktemaximum (Limit) bewertet.' in `source_a.md` -- Source_a.md directly states that in the traditional Chinese game, certain game pictures are valued at the maximum point value (limit). |
| 182 | Some of the game pictures that Babcock already mentioned in his Red Book of 1920 are classical Chinese. | supported | `source_a.md` | 'die teilweise bereits Babcock in seinem Red Book von 1920 angeführt hat und die als klassisch chinesisch anzusehen sind.' in `source_a.md` -- Source_a.md states that some of the game pictures Babcock already mentioned in his Red Book of 1920 are considered classical Chinese. |
| 183 | The poetic names of these game pictures certainly contributed significantly to the popularity of the game in the 1920s. | supported | `source_a.md` | 'Die poetischen Namen dieser Spielbilder trugen sicher zur Popularität des Spiels in den 1920er Jahren wesentlich bei' in `source_a.md` -- Source_a.md states that the poetic names of these game pictures certainly contributed significantly to the popularity of the game in the 1920s. |
| 184 | However, countless new special hands were invented especially in the USA and the ruleset became increasingly complicated. | supported | `source_a.md` | 'unzählige neue special hands erfunden wurden und das Regelwerk immer komplizierter wurde' in `source_a.md` -- Source_a.md states that countless new special hands were invented especially in the USA and the ruleset became increasingly complicated. |
| 185 | This multitude of special rules may have led to the sudden disappearance of Mah-Jongg. | supported | `source_a.md` | 'mag diese Vielzahl von Sonderregeln zum plötzlichen Verschwinden des Mah-Jongg-Spieles geführt haben.' in `source_a.md` -- Source_a.md states that this multitude of special rules may have led to the sudden disappearance of Mah-Jongg. |
| 186 | Modern Mah-Jongg was officially recognized as a sport by China's state sports commission in 1998. | supported | `source_a.md` | 'Das moderne Mah-Jongg, so wie es 1998 von der staatlichen Sportkommission Chinas offiziell als 255. Sportart anerkannt wurde' in `source_a.md` -- Source_a.md states that modern Mah-Jongg was officially recognized as the 255th sport by China's state sports commission in 1998. |
| 187 | Modern Mah-Jongg is a further development of the classical playing style. | supported | `source_a.md` | 'ist eine Weiterentwicklung der klassischen Spielweise' in `source_a.md` -- Source_a.md states that modern Mah-Jongg is a further development of the classical playing style. |
| 188 | This is similar to how the Bridge game evolved from the older Whist. | supported | `source_a.md` | 'ähnlich wie das Bridge-Spiel aus dem älteren Whist hervorgegangen ist.' in `source_a.md` -- Source_a.md makes the comparison that this is similar to how Bridge evolved from Whist. |
| 189 | The official rules of this modern playing style are used in international tournaments such as World and European Championships. | supported | `source_a.md` | 'Die offiziellen Regeln dieser modernen Spielweise finden bei internationalen Turnieren wie Welt- und Europameisterschaften Anwendung.' in `source_a.md` -- Source_a.md states that the official rules of this modern playing style are used in international tournaments such as World and European Championships. |
| 190 | In the ranking of the European Mahjong Association, only results achieved according to these playing rules are considered. | supported | `source_a.md` | 'In der Rangliste der European Mahjong Association werden nur Ergebnisse berücksichtigt, die aufgrund dieser Spielregeln erzielt wurden.' in `source_a.md` -- Source_a.md states that in the ranking of the European Mahjong Association, only results achieved according to these playing rules are considered. |
| 191 | Finnish manufacturer Lagarto offers a paid Windows version of traditional Mah-Jongg called Four Winds. | supported | `source_a.md` | 'Der finnische Hersteller Lagarto bietet eine kostenpflichtige Windows-Version des traditionellen Mah-Jongg namens Four Winds an.' in `source_a.md` -- Source_a.md states that Finnish manufacturer Lagarto offers a paid Windows version of traditional Mah-Jongg called Four Winds. |
| 192 | A player can compete against three players simulated by the software. | supported | `source_a.md` | 'Ein Spieler kann gegen drei durch die Software nachgebildete Spieler antreten.' in `source_a.md` -- Source_a.md states that a player can compete against three players simulated by the software. |
| 193 | Multiple real players can also compete against each other or against the software via a network. | supported | `source_a.md` | 'Ebenso können über ein Netzwerk mehrere reale Spieler gegeneinander oder gegen die Software antreten.' in `source_a.md` -- Source_a.md states that multiple real players can also compete against each other or against the software via a network. |
| 194 | Different rules can be played. | supported | `source_a.md` | 'Es kann nach verschiedenen Regeln gespielt werden.' in `source_a.md` -- Source_a.md states that different rules can be played. |
| 195 | The KDE project includes a free version of Mah-Jongg called Kajongg. | supported | `source_a.md` | 'Das KDE-Projekt enthält eine kostenfreie Version von Mah-Jongg, die Kajongg genannt wird.' in `source_a.md` -- Source_a.md states that the KDE project includes a free version of Mah-Jongg called Kajongg. |
| 196 | In various parts of the Yakuza game series, such as Yakuza 0, the Japanese variant of Mah-Jongg (Riichi Mahjong) is present as a minigame. | supported | `source_a.md` | 'In verschiedenen Teilen der Yakuza-Spieleserie, wie zum Beispiel Yakuza 0 ist die japanische Variante von Mah-Jongg (Riichi Mahjong) als Minispiel vorhanden.' in `source_a.md` -- Source_a.md states that in various parts of the Yakuza game series, such as Yakuza 0, the Japanese variant of Mah-Jongg (Riichi Mahjong) is present as a minigame. |
| 197 | For iPhone and iPad, there is a traditional version in the Apple App Store under the name Mahjong! by POK-Software that simulates up to 3 co-players. | supported | `source_a.md` | 'Für iPhone und iPad gibt es im Apple App Store unter dem Namen Mahjong! von POK-Software eine traditionelle Version, die bis zu 3 Mitspieler simuliert.' in `source_a.md` -- Source_a.md states that for iPhone and iPad there is a traditional version in the Apple App Store under the name Mahjong! by POK-Software that simulates up to 3 co-players. |
| 198 | Many other computer games referred to as Mah-Jongg use digitized forms of game stones but are usually games for only one person. | supported | `source_b.md` | 'Viele andere als Mah-Jongg bezeichnete Computerspiele verwenden zwar digitalisierte Formen der Spielsteine, sind jedoch meistens Spiele für nur eine Person' in `source_b.md` -- Source_b.md states that many other computer games referred to as Mah-Jongg use digitized forms of game stones but are usually games for only one person. |
| 199 | These games resemble a solitaire game in their rules (Mah-Jongg Solitaire). | supported | `source_b.md` | 'ähneln von den Regeln einer Patience (Mah-Jongg Solitaire).' in `source_b.md` -- Source_b.md states that these games resemble a solitaire game in their rules (Mah-Jongg Solitaire). |
| 200 | Starting in the mid-1980s, Mah-Jongg Solitaire became popular as a computer game under the name Shanghai. | supported | `source_b.md` | 'Ab Mitte der 1980er Jahre wurde Mah-Jongg Solitaire zunächst unter dem Namen Shanghai als Computerspiel populär' in `source_b.md` -- Source_b.md states that starting in the mid-1980s, Mah-Jongg Solitaire became popular as a computer game under the name Shanghai. |
| 201 | The improved graphics capabilities of the new Amiga computer allowed an appealing presentation of this game for the first time. | supported | `source_b.md` | 'Ab Mitte der 1980er Jahre wurde Mah-Jongg Solitaire zunächst unter dem Namen Shanghai als Computerspiel populär, nachdem die verbesserten grafischen Möglichkeiten des neuen Amiga-Computers erstmals eine ansprechende Darstellung dieses Spiels erlaubten.' in `source_b.md` -- Source B directly states that improved graphics of the new Amiga computer allowed an appealing presentation of the game for the first time. |
| 202 | In the most popular computer game variant, all 144 stones are on the table at the start of the game. | supported | `source_b.md` | 'Bei der beliebtesten Computerspiel-Variante liegen zu Spielbeginn alle 144 Steine auf dem Tisch, teils in mehreren Lagen übereinander.' in `source_b.md` -- Source B states that in the most popular computer game variant, all 144 stones are on the table at the start of the game. |
| 203 | Some of the stones are stacked in multiple layers on top of each other. | supported | `source_b.md` | 'Bei der beliebtesten Computerspiel-Variante liegen zu Spielbeginn alle 144 Steine auf dem Tisch, teils in mehreren Lagen übereinander.' in `source_b.md` -- Source B states that some stones are stacked in multiple layers on top of each other. |
| 204 | Traditionally, the game stones are arranged in the figure of a dragon or a turtle. | supported | `source_b.md` | 'Traditionell werden die Spielsteine in der Figur eines Drachen oder einer Schildkröte aufgebaut, die Computerspielvarianten bieten oft viele verschiedene Startfiguren an.' in `source_b.md` -- Source B states that traditionally the game stones are arranged in the figure of a dragon or a turtle. |
| 205 | Computer game variants often offer many different starting figures. | supported | `source_b.md` | 'Traditionell werden die Spielsteine in der Figur eines Drachen oder einer Schildkröte aufgebaut, die Computerspielvarianten bieten oft viele verschiedene Startfiguren an.' in `source_b.md` -- Source B states that computer game variants often offer many different starting figures. |
| 206 | A single player must remove all 144 stones from the table in pairs. | supported | `source_b.md` | 'Ein einzelner Spieler muss paarweise alle 144 Steine vom Tisch nehmen.' in `source_b.md` -- Source B states that a single player must remove all 144 stones from the table in pairs. |
| 207 | A pair may only be removed if both stones are not partially or completely covered by another stone and are exposed on at least one long side. | supported | `source_b.md` | 'Ein Paar darf nur abgetragen werden, wenn beide Steine von keinem anderen Stein teilweise oder vollständig überdeckt sind und an zumindest einer Längsseite freiliegen.' in `source_b.md` -- Source B states the exact condition for removing pairs regarding covering and exposure on long sides. |
| 208 | While the stones of the main suits each occur only once and cannot form pairs, the flower tiles and season tiles can be arbitrarily combined with each other. | supported | `source_b.md` | 'Während die Steine der Hauptfarben jeweils nur einmal vorkommen und keine Paare bilden können, dürfen die Blumenziegel und die Jahreszeitenziegel jeweils untereinander beliebig kombiniert werden, beispielsweise Pflaume mit Orchidee oder Winter mit Frühling.' in `source_b.md` -- Source B states that main suit stones occur only once and cannot form pairs, while flower and season tiles can be arbitrarily combined. |
| 209 | For example, plum can be combined with orchid or winter with spring. | supported | `source_b.md` | 'Während die Steine der Hauptfarben jeweils nur einmal vorkommen und keine Paare bilden können, dürfen die Blumenziegel und die Jahreszeitenziegel jeweils untereinander beliebig kombiniert werden, beispielsweise Pflaume mit Orchidee oder Winter mit Frühling.' in `source_b.md` -- Source B provides the specific examples of plum with orchid and winter with spring as valid combinations. |
| 210 | In some variants, the flower and season tiles are doubled and, for balance, the wind tiles are only included twice. | supported | `source_b.md` | 'In einigen Varianten sind die Blumen- und Jahreszeitenziegel verdoppelt und dafür zum Ausgleich beispielsweise die Windziegel nur zweimal enthalten.' in `source_b.md` -- Source B states that in some variants, flower and season tiles are doubled and wind tiles are only included twice for balance. |
| 211 | Sometimes the season tiles appear twice and there are no flower tiles. | supported | `source_b.md` | 'Mitunter kommen die Jahreszeitenziegel doppelt vor und dafür keine Blumenziegel.' in `source_b.md` -- Source B states that sometimes season tiles appear twice and there are no flower tiles. |
| 212 | As a further development of computer games, there are now online offerings where Mahjong Solitaire can be played. | supported | `source_b.md` | 'Als Weiterentwicklung der Computerspiele gibt es heute Angebote auf dem Netz, auf denen Mahjong Solitaire online gespielt werden kann.' in `source_b.md` -- Source B states that as a further development of computer games, there are now online offerings where Mahjong Solitaire can be played. |
| 213 | These are usually single-player game variants. | supported | `source_b.md` | 'Dabei handelt es sich in der Regel meist um die Spielvariante für Einzelspieler, aber durch Bestenlisten oder Wettkämpfe spielt man quasi gegen andere Mahjong-Spieler.' in `source_b.md` -- Source B states these are usually single-player game variants. |
| 214 | Through leaderboards or competitions, players essentially compete against other Mahjong players. | supported | `source_b.md` | 'Dabei handelt es sich in der Regel meist um die Spielvariante für Einzelspieler, aber durch Bestenlisten oder Wettkämpfe spielt man quasi gegen andere Mahjong-Spieler.' in `source_b.md` -- Source B states that through leaderboards or competitions, players essentially compete against other Mahjong players. |
| 215 | Often there are additional features, such as displaying the available pairs or the ability to undo moves. | supported | `source_b.md` | 'Oft gibt es zusätzliche Funktionen, wie die Anzeige der noch verfügbaren Paare oder die Möglichkeit Spielzüge rückgängig zu machen.' in `source_b.md` -- Source B states there are often additional features such as displaying available pairs or the ability to undo moves. |
| 216 | Many game types beyond the traditional rules have established themselves in the online variants. | supported | `source_b.md` | 'Bei den Online-Varianten haben sich viele Spielarten jenseits der traditionellen Regeln etabliert.' in `source_b.md` -- Source B states that many game types beyond traditional rules have established themselves in online variants. |
| 217 | For example, in Mahjong Connect, identical game stones can only be selected if a line can be drawn between them. | supported | `source_b.md` | 'Zum Beispiel können beim Mahjong Connect die identischen Spielsteine nur ausgewählt werden, wenn zwischen ihnen eine Linie gezogen werden kann.' in `source_b.md` -- Source B provides the example of Mahjong Connect where identical stones can only be selected if a line can be drawn between them. |
| 218 | In Mahjong Dimensions, there is no two-dimensional playing field. | supported | `source_b.md` | 'Beim Mahjong Dimensions gibt es kein zweidimensionales Spielfeld, sondern die Spielsteine sind zu einem dreidimensionalen Objekt gefügt.' in `source_b.md` -- Source B states that in Mahjong Dimensions, there is no two-dimensional playing field. |
| 219 | In Mahjong Dimensions, the game stones are arranged in a three-dimensional object. | supported | `source_b.md` | 'Beim Mahjong Dimensions gibt es kein zweidimensionales Spielfeld, sondern die Spielsteine sind zu einem dreidimensionalen Objekt gefügt.' in `source_b.md` -- Source B states that in Mahjong Dimensions, the game stones are arranged in a three-dimensional object. |
| 220 | There are numerous platforms where players can compete against each other. | supported | `source_a.md` | 'Es gibt zahlreiche Plattformen, auf denen man gegen andere Spieler antreten kann.' in `source_a.md` -- Source A states there are numerous platforms where one can compete against other players. |
| 221 | The following lists are limited to English-language products that can also be played for free. | supported | `source_a.md` | 'Die folgenden Listen beschränken sich auf englischsprachige Produkte, die auch gratis gespielt werden können.' in `source_a.md` -- Source A states that the following lists are limited to English-language products that can also be played for free. |
| 222 | Various rule sets and Riichi-Mahjong (Japanese variant) are offered. | supported | `source_a.md` | '#### Verschiedene Regelsätze\n\n#### Riichi-Mahjong (japanische Variante)' in `source_a.md` -- Source A shows section headings indicating various rule sets and Riichi-Mahjong (Japanese variant) are offered. |
| 223 | In Japan, the genre Mah-Jongg developed in anime and manga based on the game. | supported | `source_b.md` | 'In Japan entwickelte sich auf Grundlage des Spiels das Genre Mah-Jongg in Anime und Manga (siehe auch: Saki, Tobaku Mokushiroku Kaiji, Akagi, The Legend of Koizumi).' in `source_b.md` -- Source B states that in Japan, the genre Mah-Jongg developed in anime and manga based on the game. |
| 224 | The game often serves there as a narrative means to intensify strategic and dramatic conflicts. | supported | `source_b.md` | 'Dabei dient das Spiel dort häufig als erzählerisches Mittel zur Zuspitzung strategischer und dramatischer Konflikte.' in `source_b.md` -- Source B states that the game often serves there as a narrative means to intensify strategic and dramatic conflicts. |
| 225 | In the romantic film comedy Crazy Rich Asians (2018), a Mah-Jongg game forms the dramaturgical climax of a central confrontation. | supported | `source_b.md` | 'In der romantischen Filmkomödie Crazy Rich Asians (2018) bildet eine Mah-Jongg-Partie den dramaturgischen Höhepunkt einer zentralen Konfrontation.' in `source_b.md` -- Source B states that in Crazy Rich Asians (2018), a Mah-Jongg game forms the dramaturgical climax of a central confrontation. |
| 226 | The film Gefahr und Begierde is based on the short story of the same name by Eileen Chang. | supported | `source_b.md` | 'In dem Film Gefahr und Begierde, nach der gleichnamigen Kurzgeschichte von Eileen Chang' in `source_b.md` -- Source B states the film is based on the short story of the same name by Eileen Chang. |
| 227 | Ang Lee directs the story of a tragic love affair between a resistance fighter and the intelligence chief of the Wang Jingwei collaborative government. | supported | `source_b.md` | 'erzählt Ang Lee die Geschichte einer tragischen Liebesbeziehung zwischen einer Widerstandskämpferin und dem Geheimdienstchef der Kollaborationsregierung von Wang Jingwei' in `source_b.md` -- Source B directly states that Ang Lee tells the story of a tragic love affair between a resistance fighter and the intelligence chief of the Wang Jingwei collaborative government. |
| 228 | The film features numerous artistically staged Mah-Jongg scenes. | supported | `source_b.md` | 'Bemerkenswert sind hier die zahlreichen kunstvoll inszenierten Mah-Jongg-Szenen' in `source_b.md` -- Source B states the film features numerous artistically staged Mah-Jongg scenes. |
| 229 | In these scenes, the resistance fighter, played by Tang Wei, meets the wives of government officials. | supported | `source_b.md` | 'in denen die Widerstandskämpferin, gespielt von Tang Wei, auf die Ehefrauen der Regierungsmitglieder trifft' in `source_b.md` -- Source B states the resistance fighter, played by Tang Wei, meets the wives of government officials in these scenes. |
| 230 | In the crime novel Sous les vents de Neptun (German: "Der vierzehnte Stein") by Fred Vargas (Frédérique Audoin-Rouzeau), the game Mah-Jongg plays a central role. | supported | `source_b.md` | 'Im Kriminalroman Sous les vents de Neptun (dt. "Der vierzehnte Stein") von Fred Vargas (Frédérique Audoin-Rouzeau) nimmt das Spiel Mah-Jongg eine zentrale Rolle ein' in `source_b.md`, **transcription_error** -- Source B states that in the crime novel Sous les vents de Neptun (German: Der vierzehnte Stein) by Fred Vargas (Frédérique Audoin-Rouzeau), Mah-Jongg plays a central role. |
| 231 | The book was filmed in 2008. | supported | `source_b.md` | 'Das Buch wurde 2008 verfilmt' in `source_b.md` -- Source B states the book was filmed in 2008. |
| 232 | In the French-Swiss film Die Gleichung ihres Lebens (2023), the main character Marguerite learns Mah-Jongg after abandoning her mathematics doctorate. | supported | `source_b.md` | 'Im französisch-Schweizer Spielfilm Die Gleichung ihres Lebens (2023) lernt die Hauptperson Marguerite nach dem Abbruch ihrer Mathematik-Promotion Mah-Jongg' in `source_b.md` -- Source B states the main character Marguerite learns Mah-Jongg after abandoning her mathematics doctorate in the French-Swiss film Die Gleichung ihres Lebens (2023). |
| 233 | Marguerite achieves significant income from Mah-Jongg. | supported | `source_b.md` | 'erzielt erhebliche Einnahmen damit' in `source_b.md` -- Source B states that Marguerite achieves significant income (erhebliche Einnahmen) from Mah-Jongg. |
| 234 | The structure of the game provides her with inspiration for a return to mathematics. | supported | `source_b.md` | 'Die Struktur des Spiels liefert ihr wiederum Inspirationen für einen Wiedereinstieg in die Mathematik' in `source_b.md` -- Source B states that the structure of the game provides her with inspiration for a return to mathematics. |

## Structure

**9** mechanical check(s) over **216** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **234** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **180**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 7 run(s) over 209 attributed segment(s) — sources interleaved. 34 of 37 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

### Declared gone, still here — a record says the content departed and the merge carries the segment unchanged

- `a1` (`source_a.md`) — 'Der Mah-Jongg-Rufer erhält eine zusätzliche Prämie von 10 (häufig 20) Punkten gutgeschrieben.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Der Mah-Jongg-Rufer erhält eine zusätzliche Prämie von 10 (häufig 20) Punkten gutgeschrieben.
  In the merge:  Der Mah-Jongg-Rufer erhält eine zusätzliche Prämie von 10 (häufig 20) Punkten gutgeschrieben.
  ```
- `a4` (`source_a.md`) — 'Für diese Beraubung des Kong erhält er einen zusätzlichen Bonus von 10 Punkten.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Für diese Beraubung des Kong erhält er einen zusätzlichen Bonus von 10 Punkten.
  In the merge:  Für diese Beraubung des Kong erhält er einen zusätzlichen Bonus von 10 Punkten.
  ```
- `a6` (`source_a.md`) — 'Nach der Bewertung der einzelnen Figuren darf ein Spieler den Punktewert eventuell noch ein oder mehrere Male verdoppeln.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Nach der Bewertung der einzelnen Figuren darf ein Spieler den Punktewert eventuell noch ein oder mehrere Male verdoppeln.
  In the merge:  Nach der Bewertung der einzelnen Figuren darf ein Spieler den Punktewert eventuell noch ein oder mehrere Male verdoppeln.
  ```
- `a7` (`source_a.md`) — 'Die Verdopplungen werden nacheinander gerechnet, zweimaliges Verdoppeln vervierfacht beispielsweise den ursprünglichen Wert des Spielbildes.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Verdopplungen werden nacheinander gerechnet, zweimaliges Verdoppeln vervierfacht beispielsweise den ursprünglichen Wert des Spielbildes.
  In the merge:  Die Verdopplungen werden nacheinander gerechnet, zweimaliges Verdoppeln vervierfacht beispielsweise den ursprünglichen Wert des Spielbildes.
  ```
- `a11` (`source_a.md`) — 'Infolge der mannigfachen Verdopplungen können die Punktezahlen der Spielbilder sehr große Werte erreichen, sodass üblicherweise ein Limit vereinbart wird.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Infolge der mannigfachen Verdopplungen können die Punktezahlen der Spielbilder sehr große Werte erreichen, sodass üblicherweise ein Limit vereinbart wird.
  In the merge:  Infolge der mannigfachen Verdopplungen können die Punktezahlen der Spielbilder sehr große Werte erreichen, sodass üblicherweise ein Limit vereinbart wird.
  ```
- `a12` (`source_a.md`) — 'Dieses beträgt meist 300 oder 500 Punkte.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Dieses beträgt meist 300 oder 500 Punkte.
  In the merge:  Dieses beträgt meist 300 oder 500 Punkte.
  ```
- `a13` (`source_a.md`) — 'Übersteigt der errechnete Punktewert das vereinbarte Limit, so wird das Spielbild nur mit diesem Höchstwert gezählt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Übersteigt der errechnete Punktewert das vereinbarte Limit, so wird das Spielbild nur mit diesem Höchstwert gezählt.
  In the merge:  Übersteigt der errechnete Punktewert das vereinbarte Limit, so wird das Spielbild nur mit diesem Höchstwert gezählt.
  ```
- `a14` (`source_a.md`) — 'Besteht das Spielbild des Mah-Jongg-Rufers ausschließlich aus Ziegeln der Trumpffarbe, also nur aus Wind- und Drachenziegeln, so wird diese Hand mit dem Punktemaximum bewertet.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Besteht das Spielbild des Mah-Jongg-Rufers ausschließlich aus Ziegeln der Trumpffarbe, also nur aus Wind- und Drachenziegeln, so wird diese Hand mit dem Punktemaximum bewertet.
  In the merge:  Besteht das Spielbild des Mah-Jongg-Rufers ausschließlich aus Ziegeln der Trumpffarbe, also nur aus Wind- und Drachenziegeln, so wird diese Hand mit dem Punktemaximum bewertet.
  ```
- `a15` (`source_a.md`) — 'Kann Ostwind sofort nach Aufnehmen seiner Ziegel Mah-Jongg rufen, so besitzt er den Segen des Himmels und erhält das Punktemaximum gutgeschrieben.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Kann Ostwind sofort nach Aufnehmen seiner Ziegel Mah-Jongg rufen, so besitzt er den Segen des Himmels und erhält das Punktemaximum gutgeschrieben.
  In the merge:  Kann Ostwind sofort nach Aufnehmen seiner Ziegel Mah-Jongg rufen, so besitzt er den Segen des Himmels und erhält das Punktemaximum gutgeschrieben.
  ```
- `a16` (`source_a.md`) — 'Kann ein anderer Spieler den ersten von Ostwind abgelegten Stein aufrufen und damit Mah-Jongg erklären, so ist dies der Segen der Erde und der Spieler erhält die Hälfte des Limits gutgeschrieben.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Kann ein anderer Spieler den ersten von Ostwind abgelegten Stein aufrufen und damit Mah-Jongg erklären, so ist dies der Segen der Erde und der Spieler erhält die Hälfte des Limits gutgeschrieben.
  In the merge:  Kann ein anderer Spieler den ersten von Ostwind abgelegten Stein aufrufen und damit Mah-Jongg erklären, so ist dies der Segen der Erde und der Spieler erhält die Hälfte des Limits gutgeschrieben.
  ```
- `a18` (`source_a.md`) — 'In vielen Regelbüchern finden sich weitere Punkteprämien oder Verdopplungen für Besonderheiten des Spielbildes des Mah-Jongg-Rufers.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In vielen Regelbüchern finden sich weitere Punkteprämien oder Verdopplungen für Besonderheiten des Spielbildes des Mah-Jongg-Rufers.
  In the merge:  In vielen Regelbüchern finden sich weitere Punkteprämien oder Verdopplungen für Besonderheiten des Spielbildes des Mah-Jongg-Rufers.
  ```
- `a19` (`source_a.md`) — 'Solche Variationen sollten unbedingt vor Beginn des Spiels geklärt werden.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Solche Variationen sollten unbedingt vor Beginn des Spiels geklärt werden.
  In the merge:  Solche Variationen sollten unbedingt vor Beginn des Spiels geklärt werden.
  ```
- `a21` (`source_a.md`) — 'Haben alle Spieler den Wert ihrer Spielbilder ermittelt, so erfolgt die Abrechnung.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Haben alle Spieler den Wert ihrer Spielbilder ermittelt, so erfolgt die Abrechnung.
  In the merge:  Haben alle Spieler den Wert ihrer Spielbilder ermittelt, so erfolgt die Abrechnung.
  ```
- `a23` (`source_a.md`) — 'Wird Mah-Jongg mit 144 Steinen, also einschließlich der Steine der Hauptfarbe (der Blumen- und Jahreszeitenziegel), gespielt, so besteht jede Seite der Mauer aus 18 Ziegelstapeln.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wird Mah-Jongg mit 144 Steinen, also einschließlich der Steine der Hauptfarbe (der Blumen- und Jahreszeitenziegel), gespielt, so besteht jede Seite der Mauer aus 18 Ziegelstapeln.
  In the merge:  Wird Mah-Jongg mit 144 Steinen, also einschließlich der Steine der Hauptfarbe (der Blumen- und Jahreszeitenziegel), gespielt, so besteht jede Seite der Mauer aus 18 Ziegelstapeln.
  ```
- `a24` (`source_a.md`) — 'Sobald ein Spieler zu Beginn eines Spieles seine Steine aufnimmt, legt er seine Blumen- und Jahreszeitenziegel offen vor sich und zieht dafür einen Ersatzziegel vom toten Ende der Mauer; ebenso wird verfahren, wenn ein Spieler einen solchen Stein von der Mauer kauft.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Sobald ein Spieler zu Beginn eines Spieles seine Steine aufnimmt, legt er seine Blumen- und Jahreszeitenziegel offen vor sich und zieht dafür einen Ersatzziegel vom toten Ende der Mauer; ebenso wird verfahren, wenn ein Spieler einen solchen Stein von der Mauer kauft.
  In the merge:  Sobald ein Spieler zu Beginn eines Spieles seine Steine aufnimmt, legt er seine Blumen- und Jahreszeitenziegel offen vor sich und zieht dafür einen Ersatzziegel vom toten Ende der Mauer; ebenso wird verfahren, wenn ein Spieler einen solchen Stein von der Mauer kauft.
  ```
- `a25` (`source_a.md`) — 'Die Ziegel der Hauptfarbe sind den vier Winden zugeordnet: Nr. 1 gilt für den Ostwind, Nr. 2 für den Südwind, Nr. 3 für den Westwind und Nr. 4. für den Nordwind.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Ziegel der Hauptfarbe sind den vier Winden zugeordnet: Nr. 1 gilt für den Ostwind, Nr. 2 für den Südwind, Nr. 3 für den Westwind und Nr. 4. für den Nordwind.
  In the merge:  Die Ziegel der Hauptfarbe sind den vier Winden zugeordnet: Nr. 1 gilt für den Ostwind, Nr. 2 für den Südwind, Nr. 3 für den Westwind und Nr. 4. für den Nordwind.
  ```
- `a28` (`source_a.md`) — 'Wenn Ostwind Mah-Jongg rufen kann, so bleibt er im nächsten Spiel weiter Ostwind und auch die übrigen Positionen bleiben unverändert.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wenn Ostwind Mah-Jongg rufen kann, so bleibt er im nächsten Spiel weiter Ostwind und auch die übrigen Positionen bleiben unverändert.
  In the merge:  Wenn Ostwind Mah-Jongg rufen kann, so bleibt er im nächsten Spiel weiter Ostwind und auch die übrigen Positionen bleiben unverändert.
  ```
- `a29` (`source_a.md`) — 'Wenn ein anderer Spieler Mah-Jongg ruft, so übernimmt der bisherige Südwind die Rolle von Ostwind, und die Positionen wechseln um einen Platz gegen den Uhrzeigersinn.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wenn ein anderer Spieler Mah-Jongg ruft, so übernimmt der bisherige Südwind die Rolle von Ostwind, und die Positionen wechseln um einen Platz gegen den Uhrzeigersinn.
  In the merge:  Wenn ein anderer Spieler Mah-Jongg ruft, so übernimmt der bisherige Südwind die Rolle von Ostwind, und die Positionen wechseln um einen Platz gegen den Uhrzeigersinn.
  ```
- `a30` (`source_a.md`) — 'Eine Runde ist beendet, sobald der Spieler, der im ersten Spiel die Position des Nordwindes innehatte, ein Spiel als Ostwind verliert – es würde Ostwind des ersten Spieles wiederum zu Ostwind.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Eine Runde ist beendet, sobald der Spieler, der im ersten Spiel die Position des Nordwindes innehatte, ein Spiel als Ostwind verliert – es würde Ostwind des ersten Spieles wiederum zu Ostwind.
  In the merge:  Eine Runde ist beendet, sobald der Spieler, der im ersten Spiel die Position des Nordwindes innehatte, ein Spiel als Ostwind verliert – es würde Ostwind des ersten Spieles wiederum zu Ostwind.
  ```
- `a31` (`source_a.md`) — 'Eine Runde besteht aus mindestens vier Spielen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Eine Runde besteht aus mindestens vier Spielen.
  In the merge:  Eine Runde besteht aus mindestens vier Spielen.
  ```
- `a32` (`source_a.md`) — 'Wird nicht nur eine einzelne Runde gespielt, sondern eine Partie vereinbart, so besteht diese aus vier Runden.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wird nicht nur eine einzelne Runde gespielt, sondern eine Partie vereinbart, so besteht diese aus vier Runden.
  In the merge:  Wird nicht nur eine einzelne Runde gespielt, sondern eine Partie vereinbart, so besteht diese aus vier Runden.
  ```
- `a33` (`source_a.md`) — 'In der ersten Runde, der Ostwindrunde, ist Ost der vorherrschende Wind (Rundenwind); in der zweiten Runde (Südwindrunde) herrscht Südwind vor, die dritte Runde ist die Westwindrunde und die vierte die Nordwindrunde.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In der ersten Runde, der Ostwindrunde, ist Ost der vorherrschende Wind (Rundenwind); in der zweiten Runde (Südwindrunde) herrscht Südwind vor, die dritte Runde ist die Westwindrunde und die vierte die Nordwindrunde.
  In the merge:  In der ersten Runde, der Ostwindrunde, ist Ost der vorherrschende Wind (Rundenwind); in der zweiten Runde (Südwindrunde) herrscht Südwind vor, die dritte Runde ist die Westwindrunde und die vierte die Nordwindrunde.
  ```
- `a36` (`source_a.md`) — 'Diese stellt der jeweilige Spieler des Ostwindes vor sich auf den Tisch, der Platzstein des vorherrschenden Windes wird oben auf die Mingg gelegt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Diese stellt der jeweilige Spieler des Ostwindes vor sich auf den Tisch, der Platzstein des vorherrschenden Windes wird oben auf die Mingg gelegt.
  In the merge:  Diese stellt der jeweilige Spieler des Ostwindes vor sich auf den Tisch, der Platzstein des vorherrschenden Windes wird oben auf die Mingg gelegt.
  ```
- `a37` (`source_a.md`) — 'Vor einer weiteren Partie werden die Sitzplätze neu gelost, meist werden nicht mehr als zwei Partien gespielt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Vor einer weiteren Partie werden die Sitzplätze neu gelost, meist werden nicht mehr als zwei Partien gespielt.
  In the merge:  Vor einer weiteren Partie werden die Sitzplätze neu gelost, meist werden nicht mehr als zwei Partien gespielt.
  ```
- `a39` (`source_a.md`) — 'Im traditionellen chinesischen Spiel werden bestimmte Spielbilder mit dem Punktemaximum (Limit) bewertet.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Im traditionellen chinesischen Spiel werden bestimmte Spielbilder mit dem Punktemaximum (Limit) bewertet.
  In the merge:  Im traditionellen chinesischen Spiel werden bestimmte Spielbilder mit dem Punktemaximum (Limit) bewertet.
  ```
- `a40` (`source_a.md`) — 'Im Folgenden seien einige der gebräuchlichsten Bilder namentlich angeführt, die teilweise bereits Babcock in seinem Red Book von 1920 angeführt hat und die als klassisch chinesisch anzusehen sind.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Im Folgenden seien einige der gebräuchlichsten Bilder namentlich angeführt, die teilweise bereits Babcock in seinem Red Book von 1920 angeführt hat und die als klassisch chinesisch anzusehen sind.
  In the merge:  Im Folgenden seien einige der gebräuchlichsten Bilder namentlich angeführt, die teilweise bereits Babcock in seinem Red Book von 1920 angeführt hat und die als klassisch chinesisch anzusehen sind.
  ```
- `a41` (`source_a.md`) — 'Die poetischen Namen dieser Spielbilder trugen sicher zur Popularität des Spiels in den 1920er Jahren wesentlich bei, als jedoch vor allem in den USA unzählige neue special hands erfunden wurden und das Regelwerk immer komplizierter wurde, mag diese Vielzahl von Sonderregeln zum plötzlichen Verschwinden des Mah-Jongg-Spieles geführt haben.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die poetischen Namen dieser Spielbilder trugen sicher zur Popularität des Spiels in den 1920er Jahren wesentlich bei, als jedoch vor allem in den USA unzählige neue special hands erfunden wurden und das Regelwerk immer komplizierter wurde, mag diese Vielzahl von Sonderregeln zum plötzlichen Verschwinden des Mah-Jongg-Spieles geführt haben.
  In the merge:  Die poetischen Namen dieser Spielbilder trugen sicher zur Popularität des Spiels in den 1920er Jahren wesentlich bei, als jedoch vor allem in den USA unzählige neue special hands erfunden wurden und das Regelwerk immer komplizierter wurde, mag diese Vielzahl von Sonderregeln zum plötzlichen Verschwinden des Mah-Jongg-Spieles geführt haben.
  ```
- `a43` (`source_a.md`) — 'Sportart anerkannt wurde, ist eine Weiterentwicklung der klassischen Spielweise, ähnlich wie das Bridge-Spiel aus dem älteren Whist hervorgegangen ist.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Sportart anerkannt wurde, ist eine Weiterentwicklung der klassischen Spielweise, ähnlich wie das Bridge-Spiel aus dem älteren Whist hervorgegangen ist.
  In the merge:  Die offiziellen Regeln dieser modernen Spielweise finden bei internationalen Turnieren wie Welt- und Europameisterschaften Anwendung.
  ```
- `a44` (`source_a.md`) — 'Die offiziellen Regeln dieser modernen Spielweise finden bei internationalen Turnieren wie Welt- und Europameisterschaften Anwendung.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die offiziellen Regeln dieser modernen Spielweise finden bei internationalen Turnieren wie Welt- und Europameisterschaften Anwendung.
  In the merge:  In der Rangliste der European Mahjong Association werden nur Ergebnisse berücksichtigt, die aufgrund dieser Spielregeln erzielt wurden.
  ```
- `a46` (`source_a.md`) — 'Mah-Jongg als Computerspiel' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Mah-Jongg als Computerspiel
  In the merge:  Der finnische Hersteller Lagarto bietet eine kostenpflichtige Windows-Version des traditionellen Mah-Jongg namens Four Winds an.
  ```
- `a47` (`source_a.md`) — 'Der finnische Hersteller Lagarto bietet eine kostenpflichtige Windows-Version des traditionellen Mah-Jongg namens Four Winds an.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Der finnische Hersteller Lagarto bietet eine kostenpflichtige Windows-Version des traditionellen Mah-Jongg namens Four Winds an.
  In the merge:  Ein Spieler kann gegen drei durch die Software nachgebildete Spieler antreten.
  ```
- `a48` (`source_a.md`) — 'Ein Spieler kann gegen drei durch die Software nachgebildete Spieler antreten.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein Spieler kann gegen drei durch die Software nachgebildete Spieler antreten.
  In the merge:  Ebenso können über ein Netzwerk mehrere reale Spieler gegeneinander oder gegen die Software antreten.
  ```
- `a49` (`source_a.md`) — 'Ebenso können über ein Netzwerk mehrere reale Spieler gegeneinander oder gegen die Software antreten.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ebenso können über ein Netzwerk mehrere reale Spieler gegeneinander oder gegen die Software antreten.
  In the merge:  Es kann nach verschiedenen Regeln gespielt werden.
  ```
- `a50` (`source_a.md`) — 'Es kann nach verschiedenen Regeln gespielt werden.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Es kann nach verschiedenen Regeln gespielt werden.
  In the merge:  Das KDE-Projekt enthält eine kostenfreie Version von Mah-Jongg, die Kajongg genannt wird.
  ```
- `a51` (`source_a.md`) — 'Das KDE-Projekt enthält eine kostenfreie Version von Mah-Jongg, die Kajongg genannt wird.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Das KDE-Projekt enthält eine kostenfreie Version von Mah-Jongg, die Kajongg genannt wird.
  In the merge:  In verschiedenen Teilen der Yakuza-Spieleserie, wie zum Beispiel Yakuza 0, ist die japanische Variante von Mah-Jongg (Riichi Mahjong) als Minispiel vorhanden.
  ```
- `a54` (`source_a.md`) — 'Online-Plattformen' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Online-Plattformen
  In the merge:  Es gibt zahlreiche Plattformen, auf denen man gegen andere Spieler antreten kann. Die folgenden Listen beschränken sich auf englischsprachige Produkte, die auch gratis gespielt werden können. Dabei werden verschiedene Regelsätze und Riichi-Mahjong (japanische Variante) angeboten.
  ```
- `a55` (`source_a.md`) — 'Es gibt zahlreiche Plattformen, auf denen man gegen andere Spieler antreten kann.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Es gibt zahlreiche Plattformen, auf denen man gegen andere Spieler antreten kann.
  In the merge:  Es gibt zahlreiche Plattformen, auf denen man gegen andere Spieler antreten kann.
  ```
- `a56` (`source_a.md`) — 'Die folgenden Listen beschränken sich auf englischsprachige Produkte, die auch gratis gespielt werden können.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die folgenden Listen beschränken sich auf englischsprachige Produkte, die auch gratis gespielt werden können.
  In the merge:  Die folgenden Listen beschränken sich auf englischsprachige Produkte, die auch gratis gespielt werden können.
  ```
- `b2` (`source_b.md`) — 'Viele andere als Mah-Jongg bezeichnete Computerspiele verwenden zwar digitalisierte Formen der Spielsteine, sind jedoch meistens Spiele für nur eine Person und ähneln von den Regeln einer Patience (Mah-Jongg Solitaire).' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Viele andere als Mah-Jongg bezeichnete Computerspiele verwenden zwar digitalisierte Formen der Spielsteine, sind jedoch meistens Spiele für nur eine Person und ähneln von den Regeln einer Patience (Mah-Jongg Solitaire).
  In the merge:  Viele andere als Mah-Jongg bezeichnete Computerspiele verwenden zwar digitalisierte Formen der Spielsteine, sind jedoch meistens Spiele für nur eine Person und ähneln von den Regeln einer Patience (Mah-Jongg Solitaire).
  ```
- `b3` (`source_b.md`) — 'Ab Mitte der 1980er Jahre wurde Mah-Jongg Solitaire zunächst unter dem Namen Shanghai als Computerspiel populär, nachdem die verbesserten grafischen Möglichkeiten des neuen Amiga-Computers erstmals eine ansprechende Darstellung dieses Spiels erlaubten.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ab Mitte der 1980er Jahre wurde Mah-Jongg Solitaire zunächst unter dem Namen Shanghai als Computerspiel populär, nachdem die verbesserten grafischen Möglichkeiten des neuen Amiga-Computers erstmals eine ansprechende Darstellung dieses Spiels erlaubten.
  In the merge:  Ab Mitte der 1980er Jahre wurde Mah-Jongg Solitaire zunächst unter dem Namen Shanghai als Computerspiel populär, nachdem die verbesserten grafischen Möglichkeiten des neuen Amiga-Computers erstmals eine ansprechende Darstellung dieses Spiels erlaubten.
  ```
- `b4` (`source_b.md`) — 'Bei der beliebtesten Computerspiel-Variante liegen zu Spielbeginn alle 144 Steine auf dem Tisch, teils in mehreren Lagen übereinander.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Bei der beliebtesten Computerspiel-Variante liegen zu Spielbeginn alle 144 Steine auf dem Tisch, teils in mehreren Lagen übereinander.
  In the merge:  Bei der beliebtesten Computerspiel-Variante liegen zu Spielbeginn alle 144 Steine auf dem Tisch, teils in mehreren Lagen übereinander.
  ```
- `b5` (`source_b.md`) — 'Traditionell werden die Spielsteine in der Figur eines Drachen oder einer Schildkröte aufgebaut, die Computerspielvarianten bieten oft viele verschiedene Startfiguren an.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Traditionell werden die Spielsteine in der Figur eines Drachen oder einer Schildkröte aufgebaut, die Computerspielvarianten bieten oft viele verschiedene Startfiguren an.
  In the merge:  Traditionell werden die Spielsteine in der Figur eines Drachen oder einer Schildkröte aufgebaut, die Computerspielvarianten bieten oft viele verschiedene Startfiguren an.
  ```
- `b6` (`source_b.md`) — 'Ein einzelner Spieler muss paarweise alle 144 Steine vom Tisch nehmen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein einzelner Spieler muss paarweise alle 144 Steine vom Tisch nehmen.
  In the merge:  Ein einzelner Spieler muss paarweise alle 144 Steine vom Tisch nehmen.
  ```
- `b7` (`source_b.md`) — 'Ein Paar darf nur abgetragen werden, wenn beide Steine von keinem anderen Stein teilweise oder vollständig überdeckt sind und an zumindest einer Längsseite freiliegen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein Paar darf nur abgetragen werden, wenn beide Steine von keinem anderen Stein teilweise oder vollständig überdeckt sind und an zumindest einer Längsseite freiliegen.
  In the merge:  Ein Paar darf nur abgetragen werden, wenn beide Steine von keinem anderen Stein teilweise oder vollständig überdeckt sind und an zumindest einer Längsseite freiliegen.
  ```
- `b8` (`source_b.md`) — 'Während die Steine der Hauptfarben jeweils nur einmal vorkommen und keine Paare bilden können, dürfen die Blumenziegel und die Jahreszeitenziegel jeweils untereinander beliebig kombiniert werden, beispielsweise Pflaume mit Orchidee oder Winter mit Frühling.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Während die Steine der Hauptfarben jeweils nur einmal vorkommen und keine Paare bilden können, dürfen die Blumenziegel und die Jahreszeitenziegel jeweils untereinander beliebig kombiniert werden, beispielsweise Pflaume mit Orchidee oder Winter mit Frühling.
  In the merge:  Während die Steine der Hauptfarben jeweils nur einmal vorkommen und keine Paare bilden können, dürfen die Blumenziegel und die Jahreszeitenziegel jeweils untereinander beliebig kombiniert werden, beispielsweise Pflaume mit Orchidee oder Winter mit Frühling.
  ```
- `b9` (`source_b.md`) — 'In einigen Varianten sind die Blumen- und Jahreszeitenziegel verdoppelt und dafür zum Ausgleich beispielsweise die Windziegel nur zweimal enthalten.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In einigen Varianten sind die Blumen- und Jahreszeitenziegel verdoppelt und dafür zum Ausgleich beispielsweise die Windziegel nur zweimal enthalten.
  In the merge:  In einigen Varianten sind die Blumen- und Jahreszeitenziegel verdoppelt und dafür zum Ausgleich beispielsweise die Windziegel nur zweimal enthalten.
  ```
- `b10` (`source_b.md`) — 'Mitunter kommen die Jahreszeitenziegel doppelt vor und dafür keine Blumenziegel.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Mitunter kommen die Jahreszeitenziegel doppelt vor und dafür keine Blumenziegel.
  In the merge:  Mitunter kommen die Jahreszeitenziegel doppelt vor und dafür keine Blumenziegel.
  ```
- `b11` (`source_b.md`) — 'Als Weiterentwicklung der Computerspiele gibt es heute Angebote auf dem Netz, auf denen Mahjong Solitaire online gespielt werden kann.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Als Weiterentwicklung der Computerspiele gibt es heute Angebote auf dem Netz, auf denen Mahjong Solitaire online gespielt werden kann.
  In the merge:  Als Weiterentwicklung der Computerspiele gibt es heute Angebote auf dem Netz, auf denen Mahjong Solitaire online gespielt werden kann.
  ```
- `b12` (`source_b.md`) — 'Dabei handelt es sich in der Regel meist um die Spielvariante für Einzelspieler, aber durch Bestenlisten oder Wettkämpfe spielt man quasi gegen andere Mahjong-Spieler.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Dabei handelt es sich in der Regel meist um die Spielvariante für Einzelspieler, aber durch Bestenlisten oder Wettkämpfe spielt man quasi gegen andere Mahjong-Spieler.
  In the merge:  Dabei handelt es sich in der Regel meist um die Spielvariante für Einzelspieler, aber durch Bestenlisten oder Wettkämpfe spielt man quasi gegen andere Mahjong-Spieler.
  ```
- `b13` (`source_b.md`) — 'Oft gibt es zusätzliche Funktionen, wie die Anzeige der noch verfügbaren Paare oder die Möglichkeit Spielzüge rückgängig zu machen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Oft gibt es zusätzliche Funktionen, wie die Anzeige der noch verfügbaren Paare oder die Möglichkeit Spielzüge rückgängig zu machen.
  In the merge:  Oft gibt es zusätzliche Funktionen, wie die Anzeige der noch verfügbaren Paare oder die Möglichkeit Spielzüge rückgängig zu machen.
  ```
- `b14` (`source_b.md`) — 'Bei den Online-Varianten haben sich viele Spielarten jenseits der traditionellen Regeln etabliert.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Bei den Online-Varianten haben sich viele Spielarten jenseits der traditionellen Regeln etabliert.
  In the merge:  Bei den Online-Varianten haben sich viele Spielarten jenseits der traditionellen Regeln etabliert.
  ```
- `b15` (`source_b.md`) — 'Zum Beispiel können beim Mahjong Connect die identischen Spielsteine nur ausgewählt werden, wenn zwischen ihnen eine Linie gezogen werden kann.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Zum Beispiel können beim Mahjong Connect die identischen Spielsteine nur ausgewählt werden, wenn zwischen ihnen eine Linie gezogen werden kann.
  In the merge:  Zum Beispiel können beim Mahjong Connect die identischen Spielsteine nur ausgewählt werden, wenn zwischen ihnen eine Linie gezogen werden kann.
  ```
- `b16` (`source_b.md`) — 'Beim Mahjong Dimensions gibt es kein zweidimensionales Spielfeld, sondern die Spielsteine sind zu einem dreidimensionalen Objekt gefügt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Beim Mahjong Dimensions gibt es kein zweidimensionales Spielfeld, sondern die Spielsteine sind zu einem dreidimensionalen Objekt gefügt.
  In the merge:  Beim Mahjong Dimensions gibt es kein zweidimensionales Spielfeld, sondern die Spielsteine sind zu einem dreidimensionalen Objekt gefügt.
  ```
- `b19` (`source_b.md`) — 'In Japan entwickelte sich auf Grundlage des Spiels das Genre Mah-Jongg in Anime und Manga (siehe auch: Saki, Tobaku Mokushiroku Kaiji, Akagi, The Legend of Koizumi).' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In Japan entwickelte sich auf Grundlage des Spiels das Genre Mah-Jongg in Anime und Manga (siehe auch: Saki, Tobaku Mokushiroku Kaiji, Akagi, The Legend of Koizumi).
  In the merge:  In Japan entwickelte sich auf Grundlage des Spiels das Genre Mah-Jongg in Anime und Manga (siehe auch: Saki, Tobaku Mokushiroku Kaiji, Akagi, The Legend of Koizumi).
  ```
- `b20` (`source_b.md`) — 'Dabei dient das Spiel dort häufig als erzählerisches Mittel zur Zuspitzung strategischer und dramatischer Konflikte.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Dabei dient das Spiel dort häufig als erzählerisches Mittel zur Zuspitzung strategischer und dramatischer Konflikte.
  In the merge:  Dabei dient das Spiel dort häufig als erzählerisches Mittel zur Zuspitzung strategischer und dramatischer Konflikte.
  ```
- `b22` (`source_b.md`) — 'In der romantischen Filmkomödie Crazy Rich Asians (2018) bildet eine Mah-Jongg-Partie den dramaturgischen Höhepunkt einer zentralen Konfrontation.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In der romantischen Filmkomödie Crazy Rich Asians (2018) bildet eine Mah-Jongg-Partie den dramaturgischen Höhepunkt einer zentralen Konfrontation.
  In the merge:  In der romantischen Filmkomödie Crazy Rich Asians (2018) bildet eine Mah-Jongg-Partie den dramaturgischen Höhepunkt einer zentralen Konfrontation.
  ```
- `b23` (`source_b.md`) — 'In dem Film Gefahr und Begierde, nach der gleichnamigen Kurzgeschichte von Eileen Chang, erzählt Ang Lee die Geschichte einer tragischen Liebesbeziehung zwischen einer Widerstandskämpferin und dem Geheimdienstchef der Kollaborationsregierung von Wang Jingwei.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In dem Film Gefahr und Begierde, nach der gleichnamigen Kurzgeschichte von Eileen Chang, erzählt Ang Lee die Geschichte einer tragischen Liebesbeziehung zwischen einer Widerstandskämpferin und dem Geheimdienstchef der Kollaborationsregierung von Wang Jingwei.
  In the merge:  In dem Film Gefahr und Begierde, nach der gleichnamigen Kurzgeschichte von Eileen Chang, erzählt Ang Lee die Geschichte einer tragischen Liebesbeziehung zwischen einer Widerstandskämpferin und dem Geheimdienstchef der Kollaborationsregierung von Wang Jingwei.
  ```
- `b24` (`source_b.md`) — 'Bemerkenswert sind hier die zahlreichen kunstvoll inszenierten Mah-Jongg-Szenen, in denen die Widerstandskämpferin, gespielt von Tang Wei, auf die Ehefrauen der Regierungsmitglieder trifft.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Bemerkenswert sind hier die zahlreichen kunstvoll inszenierten Mah-Jongg-Szenen, in denen die Widerstandskämpferin, gespielt von Tang Wei, auf die Ehefrauen der Regierungsmitglieder trifft.
  In the merge:  Bemerkenswert sind hier die zahlreichen kunstvoll inszenierten Mah-Jongg-Szenen, in denen die Widerstandskämpferin, gespielt von Tang Wei, auf die Ehefrauen der Regierungsmitglieder trifft.
  ```
- `b26` (`source_b.md`) — 'Das Buch wurde 2008 verfilmt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Das Buch wurde 2008 verfilmt.
  In the merge:  Das Buch wurde 2008 verfilmt.
  ```
- `b27` (`source_b.md`) — 'Im französisch-Schweizer Spielfilm Die Gleichung ihres Lebens (2023) lernt die Hauptperson Marguerite nach dem Abbruch ihrer Mathematik-Promotion Mah-Jongg und erzielt erhebliche Einnahmen damit.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Im französisch-Schweizer Spielfilm Die Gleichung ihres Lebens (2023) lernt die Hauptperson Marguerite nach dem Abbruch ihrer Mathematik-Promotion Mah-Jongg und erzielt erhebliche Einnahmen damit.
  In the merge:  Im französisch-Schweizer Spielfilm Die Gleichung ihres Lebens (2023) lernt die Hauptperson Marguerite nach dem Abbruch ihrer Mathematik-Promotion Mah-Jongg und erzielt erhebliche Einnahmen damit.
  ```
- `b28` (`source_b.md`) — 'Die Struktur des Spiels liefert ihr wiederum Inspirationen für einen Wiedereinstieg in die Mathematik.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Struktur des Spiels liefert ihr wiederum Inspirationen für einen Wiedereinstieg in die Mathematik.
  In the merge:  Die Struktur des Spiels liefert ihr wiederum Inspirationen für einen Wiedereinstieg in die Mathematik.
  ```
- `c3` (`source_c.md`) — 'Joseph Park Babcock (1893–1949), ein amerikanischer Reisender in der Republik China, verfasste in den 1920er Jahren ein Regelwerk basierend auf unterschiedlichen Varianten, die er kennengelernt hatte, und brachte das Spiel in die USA.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Joseph Park Babcock (1893–1949), ein amerikanischer Reisender in der Republik China, verfasste in den 1920er Jahren ein Regelwerk basierend auf unterschiedlichen Varianten, die er kennengelernt hatte, und brachte das Spiel in die USA.
  In the merge:  Joseph Park Babcock (1893–1949), ein amerikanischer Reisender in der Republik China, verfasste in den 1920er Jahren ein Regelwerk basierend auf unterschiedlichen Varianten, die er kennengelernt hatte, und brachte das Spiel in die USA.
  ```
- `c4` (`source_c.md`) — 'Babcock gab ihm den Namen MAH-JONGG (in dieser Schreibweise) – den er als Marke eintragen ließ.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Babcock gab ihm den Namen MAH-JONGG (in dieser Schreibweise) – den er als Marke eintragen ließ.
  In the merge:  Babcock gab ihm den Namen MAH-JONGG (in dieser Schreibweise) – den er als Marke eintragen ließ.
  ```
- `c5` (`source_c.md`) — 'Um den Markenschutz nicht zu verletzen, wurde diese Schreibung vielfältig variiert.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Um den Markenschutz nicht zu verletzen, wurde diese Schreibung vielfältig variiert.
  In the merge:  Um den Markenschutz nicht zu verletzen, wurde diese Schreibung vielfältig variiert.
  ```
- `c6` (`source_c.md`) — 'Dieser im Westen gebräuchliche Name bezeichnet einen Sperling, der auf dem Spielstein Bambus-Eins abgebildet ist.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Dieser im Westen gebräuchliche Name bezeichnet einen Sperling, der auf dem Spielstein Bambus-Eins abgebildet ist.
  In the merge:  Dieser im Westen gebräuchliche Name bezeichnet einen Sperling, der auf dem Spielstein Bambus-Eins abgebildet ist.
  ```
- `c7` (`source_c.md`) — 'Babcock vereinfachte das Spiel für den amerikanischen Markt und versah die Steine unter anderem mit römischen Ziffern, was die Verbreitung des Spiels in den Vereinigten Staaten zusätzlich begünstigte.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Babcock vereinfachte das Spiel für den amerikanischen Markt und versah die Steine unter anderem mit römischen Ziffern, was die Verbreitung des Spiels in den Vereinigten Staaten zusätzlich begünstigte.
  In the merge:  Babcock vereinfachte das Spiel für den amerikanischen Markt und versah die Steine unter anderem mit römischen Ziffern, was die Verbreitung des Spiels in den Vereinigten Staaten zusätzlich begünstigte.
  ```
- `c9` (`source_c.md`) — 'Als Entstehungsort nennt er an anderer Stelle die Stadt Ningpo (heute Ningbo) oder die Provinz Fukien (heute Fujian).' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Als Entstehungsort nennt er an anderer Stelle die Stadt Ningpo (heute Ningbo) oder die Provinz Fukien (heute Fujian).
  In the merge:  Als Entstehungsort nennt er an anderer Stelle die Stadt Ningpo (heute Ningbo) oder die Provinz Fukien (heute Fujian).
  ```
- `c10` (`source_c.md`) — 'Möglicherweise irrte sich Babcock bezüglich des tatsächlichen Alters; der Vermarktung war es sicher zuträglich, Mah-Jongg als sehr altes Spiel auszugeben (dazu H. F. Müllers Spiel Glocke und Hammer).' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Möglicherweise irrte sich Babcock bezüglich des tatsächlichen Alters; der Vermarktung war es sicher zuträglich, Mah-Jongg als sehr altes Spiel auszugeben (dazu H. F. Müllers Spiel Glocke und Hammer).
  In the merge:  Möglicherweise irrte sich Babcock bezüglich des tatsächlichen Alters; der Vermarktung war es sicher zuträglich, Mah-Jongg als sehr altes Spiel auszugeben (dazu H. F. Müllers Spiel Glocke und Hammer).
  ```
- `c11` (`source_c.md`) — 'Es wurde behauptet, es habe das Spiel schon vor 4.000 Jahren zur Zeit der Shang-Dynastie gegeben oder Mah-Jongg sei lange Zeit dem einfachen Volk verboten und nur der Oberschicht vorbehalten gewesen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Es wurde behauptet, es habe das Spiel schon vor 4.000 Jahren zur Zeit der Shang-Dynastie gegeben oder Mah-Jongg sei lange Zeit dem einfachen Volk verboten und nur der Oberschicht vorbehalten gewesen.
  In the merge:  Es wurde behauptet, es habe das Spiel schon vor 4.000 Jahren zur Zeit der Shang-Dynastie gegeben oder Mah-Jongg sei lange Zeit dem einfachen Volk verboten und nur der Oberschicht vorbehalten gewesen.
  ```
- `c12` (`source_c.md`) — 'Tatsächlich entstand Mah-Jongg erst in der zweiten Hälfte des 19. Jahrhunderts.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Tatsächlich entstand Mah-Jongg erst in der zweiten Hälfte des 19. Jahrhunderts.
  In the merge:  Tatsächlich entstand Mah-Jongg erst in der zweiten Hälfte des 19. Jahrhunderts.
  ```
- `c13` (`source_c.md`) — 'Die ältesten erhaltenen Spiele datieren um 1870, die ältesten schriftlichen Hinweise aus dem Jahr 1890.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die ältesten erhaltenen Spiele datieren um 1870, die ältesten schriftlichen Hinweise aus dem Jahr 1890.
  In the merge:  Die ältesten erhaltenen Spiele datieren um 1870, die ältesten schriftlichen Hinweise aus dem Jahr 1890.
  ```
- `c14` (`source_c.md`) — 'Ursprünglich war Mah-Jongg ein Glücksspiel, das mit Teehäusern und Bordellen in Verbindung stand; gegen Ende des 19. Jahrhunderts hatte es sich jedoch auch in bürgerlichen Haushalten etabliert und sich von Shanghai aus in andere Teile Chinas verbreitet.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ursprünglich war Mah-Jongg ein Glücksspiel, das mit Teehäusern und Bordellen in Verbindung stand; gegen Ende des 19. Jahrhunderts hatte es sich jedoch auch in bürgerlichen Haushalten etabliert und sich von Shanghai aus in andere Teile Chinas verbreitet.
  In the merge:  Ursprünglich war Mah-Jongg ein Glücksspiel, das mit Teehäusern und Bordellen in Verbindung stand; gegen Ende des 19. Jahrhunderts hatte es sich jedoch auch in bürgerlichen Haushalten etabliert und sich von Shanghai aus in andere Teile Chinas verbreitet.
  ```
- `c15` (`source_c.md`) — 'Das Mah-Jongg-Spiel verbreitete sich rasch in China und Japan.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Das Mah-Jongg-Spiel verbreitete sich rasch in China und Japan.
  In the merge:  Das Mah-Jongg-Spiel verbreitete sich rasch in China und Japan.
  ```
- `c16` (`source_c.md`) — 'Nachdem Babcock das Spiel in den USA bekanntgemacht hatte, erlangte Mah-Jongg weltweite Popularität – vergleichbar dem Canasta in den 1950er Jahren.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Nachdem Babcock das Spiel in den USA bekanntgemacht hatte, erlangte Mah-Jongg weltweite Popularität – vergleichbar dem Canasta in den 1950er Jahren.
  In the merge:  Nachdem Babcock das Spiel in den USA bekanntgemacht hatte, erlangte Mah-Jongg weltweite Popularität – vergleichbar dem Canasta in den 1950er Jahren.
  ```
- `c17` (`source_c.md`) — 'Es wurden eigens Fabriken gegründet, um die Nachfrage nach Mah-Jongg-Spielen zu befriedigen, zumal das Gerücht umging, importierte Spiele wären mit Viren verseucht.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Es wurden eigens Fabriken gegründet, um die Nachfrage nach Mah-Jongg-Spielen zu befriedigen, zumal das Gerücht umging, importierte Spiele wären mit Viren verseucht.
  In the merge:  Es wurden eigens Fabriken gegründet, um die Nachfrage nach Mah-Jongg-Spielen zu befriedigen, zumal das Gerücht umging, importierte Spiele wären mit Viren verseucht.
  ```
- `c18` (`source_c.md`) — 'In Deutschland wurde das Spiel eingeführt durch F. Ad.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In Deutschland wurde das Spiel eingeführt durch F. Ad.
  In the merge:  In Deutschland wurde das Spiel eingeführt durch F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt (Gebrauchsmusterschutz Nr. 722354 v. 6. November 1919).
  ```
- `c19` (`source_c.md`) — 'Richter & Cie, Baukastenfabrik, Rudolstadt (Gebrauchsmusterschutz Nr. 722354 v. 6. November 1919).' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Richter & Cie, Baukastenfabrik, Rudolstadt (Gebrauchsmusterschutz Nr. 722354 v. 6. November 1919).
  In the merge:  Ein weiterer Mah-Jongg-Hersteller in Deutschland war die Hamburger Nordicus-Golconda Werke.
  ```
- `c20` (`source_c.md`) — 'Ein weiterer Mah-Jongg-Hersteller in Deutschland war die Hamburger Nordicus-Golconda Werke.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein weiterer Mah-Jongg-Hersteller in Deutschland war die Hamburger Nordicus-Golconda Werke.
  In the merge:  Es gab Mah-Jongg-Zeitschriften, in vielen amerikanischen Städten wurden Mah-Jongg-Turniere veranstaltet.
  ```
- `c21` (`source_c.md`) — 'Es gab Mah-Jongg-Zeitschriften, in vielen amerikanischen Städten wurden Mah-Jongg-Turniere veranstaltet.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Es gab Mah-Jongg-Zeitschriften, in vielen amerikanischen Städten wurden Mah-Jongg-Turniere veranstaltet.
  In the merge:  Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.
  ```
- `c22` (`source_c.md`) — 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.
  In the merge:  In New York wurde 1937 die National Mah Jongg League gegründet, die die Regeln weiter vereinheitlichte und damit die heute als American Mahjong bekannte Spielart maßgeblich prägte.
  ```
- `c23` (`source_c.md`) — 'In New York wurde 1937 die National Mah Jongg League gegründet, die die Regeln weiter vereinheitlichte und damit die heute als American Mahjong bekannte Spielart maßgeblich prägte.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In New York wurde 1937 die National Mah Jongg League gegründet, die die Regeln weiter vereinheitlichte und damit die heute als American Mahjong bekannte Spielart maßgeblich prägte.
  In the merge:  Doch bereits wenige Jahre später verschwand Mah-Jongg wie eine Mode und ebenso schnell, wie sie gekommen war.
  ```
- `c24` (`source_c.md`) — 'Doch bereits wenige Jahre später verschwand Mah-Jongg wie eine Mode und ebenso schnell, wie sie gekommen war.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Doch bereits wenige Jahre später verschwand Mah-Jongg wie eine Mode und ebenso schnell, wie sie gekommen war.
  In the merge:  Das Spiel ist in China und Japan überaus populär; außerhalb Ostasiens war die Zahl der Interessenten lange geringer, seit den 2020er Jahren lässt sich jedoch besonders in westlichen Großstädten wieder ein deutlicher Aufschwung beobachten.
  ```
- `c25` (`source_c.md`) — 'Das Spiel ist in China und Japan überaus populär; außerhalb Ostasiens war die Zahl der Interessenten lange geringer, seit den 2020er Jahren lässt sich jedoch besonders in westlichen Großstädten wieder ein deutlicher Aufschwung beobachten.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Das Spiel ist in China und Japan überaus populär; außerhalb Ostasiens war die Zahl der Interessenten lange geringer, seit den 2020er Jahren lässt sich jedoch besonders in westlichen Großstädten wieder ein deutlicher Aufschwung beobachten.
  In the merge:  Die weltweite Teilnahme an Mah-Jongg-Veranstaltungen hat sich innerhalb eines Jahres mehr als verdreifacht; regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt.
  ```
- `c26` (`source_c.md`) — 'Die weltweite Teilnahme an Mah-Jongg-Veranstaltungen hat sich innerhalb eines Jahres mehr als verdreifacht; regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die weltweite Teilnahme an Mah-Jongg-Veranstaltungen hat sich innerhalb eines Jahres mehr als verdreifacht; regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt.
  In the merge:  Auch soziale Medien tragen zu dieser Entwicklung bei: Auf YouTube existieren zahlreiche Einführungs- und Lernvideos, und auf TikTok nahm die Menge der Mah-Jongg-bezogenen Inhalte innerhalb eines Jahres um rund 70 Prozent zu.
  ```
- `c27` (`source_c.md`) — 'Auch soziale Medien tragen zu dieser Entwicklung bei: Auf YouTube existieren zahlreiche Einführungs- und Lernvideos, und auf TikTok nahm die Menge der Mah-Jongg-bezogenen Inhalte innerhalb eines Jahres um rund 70 Prozent zu.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Auch soziale Medien tragen zu dieser Entwicklung bei: Auf YouTube existieren zahlreiche Einführungs- und Lernvideos, und auf TikTok nahm die Menge der Mah-Jongg-bezogenen Inhalte innerhalb eines Jahres um rund 70 Prozent zu.
  In the merge:  Von den Regeln her kann Mah-Jongg als eine Variante des Kartenspiels Rummy verstanden werden, von dem es ebenfalls eine Variante mit Spielsteinen gibt.
  ```
- `c28` (`source_c.md`) — 'Von den Regeln her kann Mah-Jongg als eine Variante des Kartenspiels Rummy verstanden werden, von dem es ebenfalls eine Variante mit Spielsteinen gibt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Von den Regeln her kann Mah-Jongg als eine Variante des Kartenspiels Rummy verstanden werden, von dem es ebenfalls eine Variante mit Spielsteinen gibt.
  In the merge:  Dann wird Mah-Jongg mit "chinesischen" Spielkarten statt mit französischem Blatt gespielt.
  ```
- `c30` (`source_c.md`) — 'Es gibt jedoch keine Hinweise, dass sich das Rummy-Spiel aus dem Mah-Jongg entwickelt hätte oder umgekehrt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Es gibt jedoch keine Hinweise, dass sich das Rummy-Spiel aus dem Mah-Jongg entwickelt hätte oder umgekehrt.
  In the merge:  Die Abstammung von einem (hypothetischen) gemeinsamen Vorfahren ist nicht erwiesen.
  ```
- `c32` (`source_c.md`) — 'Die Spielsteine' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Spielsteine
  In the merge:  Mah-Jongg-Spiele sind in den verschiedenen Ausführungen erhältlich.
  ```
- `c33` (`source_c.md`) — 'Mah-Jongg-Spiele sind in den verschiedenen Ausführungen erhältlich.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Mah-Jongg-Spiele sind in den verschiedenen Ausführungen erhältlich.
  In the merge:  Die Spielsteine sind bei den besseren Spielen aus zwei Teilen gearbeitet, die Bilder auf den Vorderseiten sind mit Sticheln in einen kleinen Block aus Bein – früher Elfenbein – eingraviert und koloriert, die Rückseiten sind aus Bambus und diese beiden Teile sind üblicherweise nicht einfach verklebt, sondern verzinkt.
  ```
- `c34` (`source_c.md`) — 'Die Spielsteine sind bei den besseren Spielen aus zwei Teilen gearbeitet, die Bilder auf den Vorderseiten sind mit Sticheln in einen kleinen Block aus Bein – früher Elfenbein – eingraviert und koloriert, die Rückseiten sind aus Bambus und diese beiden Teile sind üblicherweise nicht einfach verklebt, sondern verzinkt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Spielsteine sind bei den besseren Spielen aus zwei Teilen gearbeitet, die Bilder auf den Vorderseiten sind mit Sticheln in einen kleinen Block aus Bein – früher Elfenbein – eingraviert und koloriert, die Rückseiten sind aus Bambus und diese beiden Teile sind üblicherweise nicht einfach verklebt, sondern verzinkt.
  In the merge:  Die Steine preisgünstigerer Spiele sind aus bedrucktem Holz oder aus Kunststoff gefertigt.
  ```
- `c35` (`source_c.md`) — 'Die Steine preisgünstigerer Spiele sind aus bedrucktem Holz oder aus Kunststoff gefertigt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Steine preisgünstigerer Spiele sind aus bedrucktem Holz oder aus Kunststoff gefertigt.
  In the merge:  Es gibt auch Mah-Jongg-Kartenspiele.
  ```
- `c36` (`source_c.md`) — 'Es gibt auch Mah-Jongg-Kartenspiele.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Es gibt auch Mah-Jongg-Kartenspiele.
  In the merge:  Im 21. Jahrhundert werden Mah-Jongg-Sets zudem zunehmend als Designobjekte vermarktet; neben modern gestalteten thematischen Steinsätzen bieten auch Luxusmarken wie Hermès, Prada und Louis Vuitton eigene Ausführungen an.
  ```
- `c41` (`source_c.md`) — 'Mah-Jongg wird in unzähligen Regelvarianten von Chinese Traditional bis Jewish American gespielt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Mah-Jongg wird in unzähligen Regelvarianten von Chinese Traditional bis Jewish American gespielt.
  In the merge:  Mah-Jongg wird in unzähligen Regelvarianten von Chinese Traditional bis Jewish American gespielt.
  ```
- `c42` (`source_c.md`) — 'Die folgende Anleitung beschreibt die Hua Bao Rules, welche bis auf wenige Unterschiede den Regeln von Joseph P. Babcock entsprechen und den gemeinsamen Kern der mannigfaltigen Varianten darstellen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die folgende Anleitung beschreibt die Hua Bao Rules, welche bis auf wenige Unterschiede den Regeln von Joseph P. Babcock entsprechen und den gemeinsamen Kern der mannigfaltigen Varianten darstellen.
  In the merge:  Die folgende Anleitung beschreibt die Hua Bao Rules, welche bis auf wenige Unterschiede den Regeln von Joseph P. Babcock entsprechen und den gemeinsamen Kern der mannigfaltigen Varianten darstellen.
  ```
- `c43` (`source_c.md`) — 'Diese ist die in Europa gängige Spielweise.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Diese ist die in Europa gängige Spielweise.
  In the merge:  Diese ist die in Europa gängige Spielweise.
  ```
- `c44` (`source_c.md`) — 'In der Standard-Variante wird mit 136 Steinen gespielt, die acht Ziegel der Hauptfarbe werden nicht verwendet.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In der Standard-Variante wird mit 136 Steinen gespielt, die acht Ziegel der Hauptfarbe werden nicht verwendet.
  In the merge:  In der Standard-Variante wird mit 136 Steinen gespielt, die acht Ziegel der Hauptfarbe werden nicht verwendet.
  ```
- `c47` (`source_c.md`) — 'Vor Beginn einer Partie stehen die vier Spieler an den vier Seiten eines quadratischen Tisches.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Vor Beginn einer Partie stehen die vier Spieler an den vier Seiten eines quadratischen Tisches.
  In the merge:  Vor Beginn einer Partie stehen die vier Spieler an den vier Seiten eines quadratischen Tisches.
  ```
- `c48` (`source_c.md`) — 'Der älteste Spieler mischt verdeckt die vier Platzsteine und stapelt sie aufeinander.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Der älteste Spieler mischt verdeckt die vier Platzsteine und stapelt sie aufeinander.
  In the merge:  Der älteste Spieler mischt verdeckt die vier Platzsteine und stapelt sie aufeinander.
  ```
- `c49` (`source_c.md`) — 'Sodann wirft er zwei Würfel und zählt die Augensumme gegen den Uhrzeigersinn ab, wobei er bei sich selbst zu zählen beginnt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Sodann wirft er zwei Würfel und zählt die Augensumme gegen den Uhrzeigersinn ab, wobei er bei sich selbst zu zählen beginnt.
  In the merge:  Sodann wirft er zwei Würfel und zählt die Augensumme gegen den Uhrzeigersinn ab, wobei er bei sich selbst zu zählen beginnt.
  ```
- `c50` (`source_c.md`) — 'Der solcherart bestimmte Spieler nimmt den obersten Platzstein, der nächste den zweiten usw.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Der solcherart bestimmte Spieler nimmt den obersten Platzstein, der nächste den zweiten usw.
  In the merge:  Der solcherart bestimmte Spieler nimmt den obersten Platzstein, der nächste den zweiten usw.
  ```
- `c51` (`source_c.md`) — 'Die Spielfläche des Tisches wird als Himmelskarte interpretiert.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Spielfläche des Tisches wird als Himmelskarte interpretiert.
  In the merge:  Die Spielfläche des Tisches wird als Himmelskarte interpretiert.
  ```
- `c52` (`source_c.md`) — 'Der Spieler, der den Platzstein Ostwind erhält, wird Spielleiter im ersten Spiel und bleibt an seinem Platz, Westwind setzt sich gegenüber, Südwind zur Rechten (!) von Ostwind und Nordwind zur Linken.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Der Spieler, der den Platzstein Ostwind erhält, wird Spielleiter im ersten Spiel und bleibt an seinem Platz, Westwind setzt sich gegenüber, Südwind zur Rechten (!) von Ostwind und Nordwind zur Linken.
  In the merge:  Der Spieler, der den Platzstein Ostwind erhält, wird Spielleiter im ersten Spiel und bleibt an seinem Platz, Westwind setzt sich gegenüber, Südwind zur Rechten (!) von Ostwind und Nordwind zur Linken.
  ```
- `c54` (`source_c.md`) — 'Die Ziegel werden verdeckt auf dem Tisch gemischt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Ziegel werden verdeckt auf dem Tisch gemischt.
  In the merge:  Die Ziegel werden verdeckt auf dem Tisch gemischt.
  ```
- `c55` (`source_c.md`) — 'Anschließend baut jeder der vier Spieler eine Seite der Mauer, indem er 34 der Ziegel verdeckt nimmt und zu einer 17 Ziegel langen und zwei Ziegel hohen Mauer anordnet.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Anschließend baut jeder der vier Spieler eine Seite der Mauer, indem er 34 der Ziegel verdeckt nimmt und zu einer 17 Ziegel langen und zwei Ziegel hohen Mauer anordnet.
  In the merge:  Anschließend baut jeder der vier Spieler eine Seite der Mauer, indem er 34 der Ziegel verdeckt nimmt und zu einer 17 Ziegel langen und zwei Ziegel hohen Mauer anordnet.
  ```
- `c56` (`source_c.md`) — 'Wird mit Blumen- und Jahreszeitenziegeln gespielt, so nimmt jeder Spieler 36 Ziegel und die Breite der Mauer beträgt 18 Stapel (siehe Blumen- und Jahreszeitenziegel).' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wird mit Blumen- und Jahreszeitenziegeln gespielt, so nimmt jeder Spieler 36 Ziegel und die Breite der Mauer beträgt 18 Stapel (siehe Blumen- und Jahreszeitenziegel).
  In the merge:  Wird mit Blumen- und Jahreszeitenziegeln gespielt, so nimmt jeder Spieler 36 Ziegel und die Breite der Mauer beträgt 18 Stapel (siehe Blumen- und Jahreszeitenziegel).
  ```
- `c57` (`source_c.md`) — 'Die vier Mauerstücke werden zusammengeschoben, so dass sie sich an den Ecken berühren und ein Quadrat bilden.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die vier Mauerstücke werden zusammengeschoben, so dass sie sich an den Ecken berühren und ein Quadrat bilden.
  In the merge:  Die vier Mauerstücke werden zusammengeschoben, so dass sie sich an den Ecken berühren und ein Quadrat bilden.
  ```
- `c58` (`source_c.md`) — 'Außerhalb der asiatischen Länder wird dies manchmal Chinesische Mauer genannt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Außerhalb der asiatischen Länder wird dies manchmal Chinesische Mauer genannt.
  In the merge:  Außerhalb der asiatischen Länder wird dies manchmal Chinesische Mauer genannt.
  ```
- `c59` (`source_c.md`) — 'Nun wirft Ostwind die zwei Würfel und zählt wie vorhin, bei sich selbst beginnend, die Augensumme gegen den Uhrzeigersinn an den Spielern ab.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Nun wirft Ostwind die zwei Würfel und zählt wie vorhin, bei sich selbst beginnend, die Augensumme gegen den Uhrzeigersinn an den Spielern ab.
  In the merge:  Nun wirft Ostwind die zwei Würfel und zählt wie vorhin, bei sich selbst beginnend, die Augensumme gegen den Uhrzeigersinn an den Spielern ab.
  ```
- `c60` (`source_c.md`) — 'Der so bestimmte Spieler wirft ebenfalls beide Würfel und zählt die Augensumme beider Würfe zusammen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Der so bestimmte Spieler wirft ebenfalls beide Würfel und zählt die Augensumme beider Würfe zusammen.
  In the merge:  Der so bestimmte Spieler wirft ebenfalls beide Würfel und zählt die Augensumme beider Würfe zusammen.
  ```
- `c61` (`source_c.md`) — 'Ostwind zählt am rechten Ende der vor ihm befindlichen Mauer beginnend im Uhrzeigersinn der Gesamtsumme entsprechend Ziegelstapel ab.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ostwind zählt am rechten Ende der vor ihm befindlichen Mauer beginnend im Uhrzeigersinn der Gesamtsumme entsprechend Ziegelstapel ab.
  In the merge:  Ostwind zählt am rechten Ende der vor ihm befindlichen Mauer beginnend im Uhrzeigersinn der Gesamtsumme entsprechend Ziegelstapel ab.
  ```
- `c62` (`source_c.md`) — 'Eventuell setzt er die Zählung mit Ziegeln aus der Mauer seines linken Nachbarn fort.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Eventuell setzt er die Zählung mit Ziegeln aus der Mauer seines linken Nachbarn fort.
  In the merge:  Eventuell setzt er die Zählung mit Ziegeln aus der Mauer seines linken Nachbarn fort.
  ```
- `c63` (`source_c.md`) — 'Den so bestimmten Stapel nimmt er heraus (Mauerdurchbruch) und stellt ihn auf den Stapel rechts neben der entstandenen Lücke.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Den so bestimmten Stapel nimmt er heraus (Mauerdurchbruch) und stellt ihn auf den Stapel rechts neben der entstandenen Lücke.
  In the merge:  Den so bestimmten Stapel nimmt er heraus (Mauerdurchbruch) und stellt ihn auf den Stapel rechts neben der entstandenen Lücke.
  ```
- `c64` (`source_c.md`) — 'Die herausgenommenen Steine heißen lose Ziegel und markieren das tote Ende der Mauer, das Ende links der Lücke ist das lebende Ende der Mauer.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die herausgenommenen Steine heißen lose Ziegel und markieren das tote Ende der Mauer, das Ende links der Lücke ist das lebende Ende der Mauer.
  In the merge:  Die herausgenommenen Steine heißen lose Ziegel und markieren das tote Ende der Mauer, das Ende links der Lücke ist das lebende Ende der Mauer.
  ```
- `c65` (`source_c.md`) — 'Gezogen werden die Steine regulär vom lebenden Ende der Mauer.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Gezogen werden die Steine regulär vom lebenden Ende der Mauer.
  In the merge:  Gezogen werden die Steine regulär vom lebenden Ende der Mauer.
  ```
- `c66` (`source_c.md`) — 'Vom toten Ende werden dagegen nur Ersatzziegel (siehe unten) genommen, beginnend mit den beiden losen Ziegeln.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Vom toten Ende werden dagegen nur Ersatzziegel (siehe unten) genommen, beginnend mit den beiden losen Ziegeln.
  In the merge:  Vom toten Ende werden dagegen nur Ersatzziegel (siehe unten) genommen, beginnend mit den beiden losen Ziegeln.
  ```
- `c67` (`source_c.md`) — 'Die Spieler nehmen dreimal reihum gegen den Uhrzeigersinn jeder zwei Stapel zu zwei Ziegel vom lebenden Ende der Mauer, wobei sich Ostwind als erster bedient.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Spieler nehmen dreimal reihum gegen den Uhrzeigersinn jeder zwei Stapel zu zwei Ziegel vom lebenden Ende der Mauer, wobei sich Ostwind als erster bedient.
  In the merge:  Die Spieler nehmen dreimal reihum gegen den Uhrzeigersinn jeder zwei Stapel zu zwei Ziegel vom lebenden Ende der Mauer, wobei sich Ostwind als erster bedient.
  ```
- `c68` (`source_c.md`) — 'Zuletzt nimmt jeder Spieler noch einen weiteren, dreizehnten, und Ostwind außerdem einen vierzehnten Ziegel.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Zuletzt nimmt jeder Spieler noch einen weiteren, dreizehnten, und Ostwind außerdem einen vierzehnten Ziegel.
  In the merge:  Zuletzt nimmt jeder Spieler noch einen weiteren, dreizehnten, und Ostwind außerdem einen vierzehnten Ziegel.
  ```
- `c70` (`source_c.md`) — 'Jeder der vier Spieler versucht, durch Ziehen und Abwerfen von Steinen seine ursprüngliche Hand zu verbessern und ein vollständiges Spielbild aus möglichst wertvollen Figuren zu formen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Jeder der vier Spieler versucht, durch Ziehen und Abwerfen von Steinen seine ursprüngliche Hand zu verbessern und ein vollständiges Spielbild aus möglichst wertvollen Figuren zu formen.
  In the merge:  Jeder der vier Spieler versucht, durch Ziehen und Abwerfen von Steinen seine ursprüngliche Hand zu verbessern und ein vollständiges Spielbild aus möglichst wertvollen Figuren zu formen.
  ```
- `c71` (`source_c.md`) — 'Steine werden von der Mauer gezogen oder nach Abwurf eines anderen Spielers aufgenommen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Steine werden von der Mauer gezogen oder nach Abwurf eines anderen Spielers aufgenommen.
  In the merge:  Steine werden von der Mauer gezogen oder nach Abwurf eines anderen Spielers aufgenommen.
  ```
- `c73` (`source_c.md`) — 'Die vier Figuren können wahlweise Drillinge, Vierlinge oder Folgen sein.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die vier Figuren können wahlweise Drillinge, Vierlinge oder Folgen sein.
  In the merge:  Die vier Figuren können wahlweise Drillinge, Vierlinge oder Folgen sein.
  ```
- `c76` (`source_c.md`) — 'Ein Paar besteht aus zwei gleichen Steinen, z. B. zweimal Bambus-Fünf oder zwei grüne Drachen etc.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein Paar besteht aus zwei gleichen Steinen, z. B. zweimal Bambus-Fünf oder zwei grüne Drachen etc.
  In the merge:  Ein Paar besteht aus zwei gleichen Steinen, z. B. zweimal Bambus-Fünf oder zwei grüne Drachen etc.
  ```
- `c77` (`source_c.md`) — 'Um Mah-Jongg rufen zu können, ist ein vollständiges Spielbild nötig, in diesem muss genau ein Paar, das Schlusspaar (將, jiàng, manchmal 眼, yǎn), enthalten sein.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Um Mah-Jongg rufen zu können, ist ein vollständiges Spielbild nötig, in diesem muss genau ein Paar, das Schlusspaar (將, jiàng, manchmal 眼, yǎn), enthalten sein.
  In the merge:  Um Mah-Jongg rufen zu können, ist ein vollständiges Spielbild nötig, in diesem muss genau ein Paar, das Schlusspaar (將, jiàng, manchmal 眼, yǎn), enthalten sein.
  ```
- `c78` (`source_c.md`) — 'Zur Vervollständigung eines Paares darf ein abgelegter Stein nur aufgerufen werden, wenn gleichzeitig Mah-Jongg gerufen wird.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Zur Vervollständigung eines Paares darf ein abgelegter Stein nur aufgerufen werden, wenn gleichzeitig Mah-Jongg gerufen wird.
  In the merge:  Zur Vervollständigung eines Paares darf ein abgelegter Stein nur aufgerufen werden, wenn gleichzeitig Mah-Jongg gerufen wird.
  ```
- `c80` (`source_c.md`) — 'Ein Pong (碰, pèng) besteht aus drei gleichen Steinen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein Pong (碰, pèng) besteht aus drei gleichen Steinen.
  In the merge:  Ein Pong (碰, pèng) besteht aus drei gleichen Steinen.
  ```
- `c81` (`source_c.md`) — 'Wird ein Pong ausschließlich aus Ziegeln der ursprünglichen Hand oder von der Mauer gezogenen Ziegeln gebildet, so handelt es sich um einen verdeckten Pong, der nicht gemeldet werden muss.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wird ein Pong ausschließlich aus Ziegeln der ursprünglichen Hand oder von der Mauer gezogenen Ziegeln gebildet, so handelt es sich um einen verdeckten Pong, der nicht gemeldet werden muss.
  In the merge:  Wird ein Pong ausschließlich aus Ziegeln der ursprünglichen Hand oder von der Mauer gezogenen Ziegeln gebildet, so handelt es sich um einen verdeckten Pong, der nicht gemeldet werden muss.
  ```
- `c82` (`source_c.md`) — 'Wird er dennoch aufgedeckt, so sollte er durch ein Umdrehen eines der Steine als eigentlich verdeckt markiert werden.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wird er dennoch aufgedeckt, so sollte er durch ein Umdrehen eines der Steine als eigentlich verdeckt markiert werden.
  In the merge:  Wird er dennoch aufgedeckt, so sollte er durch ein Umdrehen eines der Steine als eigentlich verdeckt markiert werden.
  ```
- `c84` (`source_c.md`) — 'Er legt sein Paar und den aufgerufenen Ziegel offen vor sich auf den Tisch und besitzt einen offenen Pong.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Er legt sein Paar und den aufgerufenen Ziegel offen vor sich auf den Tisch und besitzt einen offenen Pong.
  In the merge:  Er legt sein Paar und den aufgerufenen Ziegel offen vor sich auf den Tisch und besitzt einen offenen Pong.
  ```
- `c85` (`source_c.md`) — 'In den 1970er und 1980er Jahren wurde im deutschsprachigen Raum statt Pong oftmals der Begriff Pon verwendet.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In den 1970er und 1980er Jahren wurde im deutschsprachigen Raum statt Pong oftmals der Begriff Pon verwendet.
  In the merge:  In den 1970er und 1980er Jahren wurde im deutschsprachigen Raum statt Pong oftmals der Begriff Pon verwendet.
  ```
- `c86` (`source_c.md`) — 'Auch in dem 1982 erschienenen Anleitungsbuch von Ursula Eschenbach ist durchgehend von Pon, Kan und Chii die Rede.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Auch in dem 1982 erschienenen Anleitungsbuch von Ursula Eschenbach ist durchgehend von Pon, Kan und Chii die Rede.
  In the merge:  Auch in dem 1982 erschienenen Anleitungsbuch von Ursula Eschenbach ist durchgehend von Pon, Kan und Chii die Rede.
  ```
- `c87` (`source_c.md`) — 'Die Begriffe Pon (jap. ポン, 碰 pon), Kan (カン, 槓, 杠 kan) oder Chii (チー, 吃 chī) stammen aus der japanischen Spielart des Riichi Mahjong (リーチ麻雀, 立直マージャン rīchi mājan).' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Begriffe Pon (jap. ポン, 碰 pon), Kan (カン, 槓, 杠 kan) oder Chii (チー, 吃 chī) stammen aus der japanischen Spielart des Riichi Mahjong (リーチ麻雀, 立直マージャン rīchi mājan).
  In the merge:  Die Begriffe Pon (jap. ポン, 碰 pon), Kan (カン, 槓, 杠 kan) oder Chii (チー, 吃 chī) stammen aus der japanischen Spielart des Riichi Mahjong (リーチ麻雀, 立直マージャン rīchi mājan).
  ```
- `c89` (`source_c.md`) — 'Ein Kong (槓 / 杠, gàng) besteht aus vier gleichen Steinen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein Kong (槓 / 杠, gàng) besteht aus vier gleichen Steinen.
  In the merge:  Ein Kong (槓 / 杠, gàng) besteht aus vier gleichen Steinen.
  ```
- `c90` (`source_c.md`) — 'Wird ein Kong ausschließlich aus Steinen der ursprünglichen Hand und von der Mauer gezogenen Ziegeln gebildet, so sollte der Spieler einen verdeckten Kong melden.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wird ein Kong ausschließlich aus Steinen der ursprünglichen Hand und von der Mauer gezogenen Ziegeln gebildet, so sollte der Spieler einen verdeckten Kong melden.
  In the merge:  Wird ein Kong ausschließlich aus Steinen der ursprünglichen Hand und von der Mauer gezogenen Ziegeln gebildet, so sollte der Spieler einen verdeckten Kong melden.
  ```
- `c91` (`source_c.md`) — 'Tut er dies nicht, so kann er keinen Ersatzziegel aus der Mauer ziehen, der bei Kongs notwendig ist, um ein komplettes Spielbild zu erreichen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Tut er dies nicht, so kann er keinen Ersatzziegel aus der Mauer ziehen, der bei Kongs notwendig ist, um ein komplettes Spielbild zu erreichen.
  In the merge:  Tut er dies nicht, so kann er keinen Ersatzziegel aus der Mauer ziehen, der bei Kongs notwendig ist, um ein komplettes Spielbild zu erreichen.
  ```
- `c92` (`source_c.md`) — 'Wird das Spiel beendet, bevor der Spieler den Vierling meldet, so wird der verdeckte Kong als verdeckter Pong gewertet.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wird das Spiel beendet, bevor der Spieler den Vierling meldet, so wird der verdeckte Kong als verdeckter Pong gewertet.
  In the merge:  Wird das Spiel beendet, bevor der Spieler den Vierling meldet, so wird der verdeckte Kong als verdeckter Pong gewertet.
  ```
- `c93` (`source_c.md`) — 'Ein verdeckter Kong muss nicht sofort gemeldet werden, sondern kann auch später herausgelegt werden, wenn der Spieler erneut am Zug ist.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein verdeckter Kong muss nicht sofort gemeldet werden, sondern kann auch später herausgelegt werden, wenn der Spieler erneut am Zug ist.
  In the merge:  Ein verdeckter Kong muss nicht sofort gemeldet werden, sondern kann auch später herausgelegt werden, wenn der Spieler erneut am Zug ist.
  ```
- `c96` (`source_c.md`) — 'Hat ein Spieler bereits einen offenen Pong gemeldet und wird der fehlende vierte Stein von einem anderen Spieler abgelegt, so kann dieser Ziegel nicht zur Komplettierung des Kongs aufgerufen werden.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Hat ein Spieler bereits einen offenen Pong gemeldet und wird der fehlende vierte Stein von einem anderen Spieler abgelegt, so kann dieser Ziegel nicht zur Komplettierung des Kongs aufgerufen werden.
  In the merge:  Hat ein Spieler bereits einen offenen Pong gemeldet und wird der fehlende vierte Stein von einem anderen Spieler abgelegt, so kann dieser Ziegel nicht zur Komplettierung des Kongs aufgerufen werden.
  ```
- `c97` (`source_c.md`) — 'Hat ein Spieler bereits einen Pong gemeldet und zieht er den fehlenden vierten Stein von der Mauer, so darf er ihn an den Pong anlegen und besitzt damit einen offenen Kong.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Hat ein Spieler bereits einen Pong gemeldet und zieht er den fehlenden vierten Stein von der Mauer, so darf er ihn an den Pong anlegen und besitzt damit einen offenen Kong.
  In the merge:  Hat ein Spieler bereits einen Pong gemeldet und zieht er den fehlenden vierten Stein von der Mauer, so darf er ihn an den Pong anlegen und besitzt damit einen offenen Kong.
  ```
- `c98` (`source_c.md`) — 'In dieser Situation kann es zu einer Beraubung des Kong kommen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: In dieser Situation kann es zu einer Beraubung des Kong kommen.
  In the merge:  In dieser Situation kann es zu einer Beraubung des Kong kommen.
  ```
- `c100` (`source_c.md`) — 'Sobald ein Spieler einen offenen oder verdeckten Kong meldet, muss er einen Ersatzziegel vom toten Ende der Mauer ziehen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Sobald ein Spieler einen offenen oder verdeckten Kong meldet, muss er einen Ersatzziegel vom toten Ende der Mauer ziehen.
  In the merge:  Sobald ein Spieler einen offenen oder verdeckten Kong meldet, muss er einen Ersatzziegel vom toten Ende der Mauer ziehen.
  ```
- `c102` (`source_c.md`) — 'Ein Chow (吃, chī, manchmal 上, shàng) ist eine Sequenz aus genau drei aufeinanderfolgenden Steinen einer Grundfarbe; Sequenzen aus mehr als drei Steinen sind nicht gestattet.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein Chow (吃, chī, manchmal 上, shàng) ist eine Sequenz aus genau drei aufeinanderfolgenden Steinen einer Grundfarbe; Sequenzen aus mehr als drei Steinen sind nicht gestattet.
  In the merge:  Ein Chow (吃, chī, manchmal 上, shàng) ist eine Sequenz aus genau drei aufeinanderfolgenden Steinen einer Grundfarbe; Sequenzen aus mehr als drei Steinen sind nicht gestattet.
  ```
- `c103` (`source_c.md`) — 'Ein Chow aus Steinen der Trumpffarbe ist nicht möglich.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein Chow aus Steinen der Trumpffarbe ist nicht möglich.
  In the merge:  Ein Chow aus Steinen der Trumpffarbe ist nicht möglich.
  ```
- `c105` (`source_c.md`) — 'Der aufrufende Spieler legt dann die damit gebildete Folge offen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Der aufrufende Spieler legt dann die damit gebildete Folge offen.
  In the merge:  Der aufrufende Spieler legt dann die damit gebildete Folge offen.
  ```
- `c106` (`source_c.md`) — 'Ein anderer Spieler kann nur dann einen abgelegten Stein für eine Folge aufrufen, wenn er gleichzeitig Mah-Jongg ruft.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein anderer Spieler kann nur dann einen abgelegten Stein für eine Folge aufrufen, wenn er gleichzeitig Mah-Jongg ruft.
  In the merge:  Ein anderer Spieler kann nur dann einen abgelegten Stein für eine Folge aufrufen, wenn er gleichzeitig Mah-Jongg ruft.
  ```
- `c107` (`source_c.md`) — 'Folgen, die aus Steinen der ursprünglichen Hand bzw. aus gezogenen Steinen gebildet werden, können bis zum Spielende verdeckt bleiben.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Folgen, die aus Steinen der ursprünglichen Hand bzw. aus gezogenen Steinen gebildet werden, können bis zum Spielende verdeckt bleiben.
  In the merge:  Folgen, die aus Steinen der ursprünglichen Hand bzw. aus gezogenen Steinen gebildet werden, können bis zum Spielende verdeckt bleiben.
  ```
- `c109` (`source_c.md`) — 'Mah-Jongg wird gegen den Uhrzeigersinn gespielt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Mah-Jongg wird gegen den Uhrzeigersinn gespielt.
  In the merge:  Mah-Jongg wird gegen den Uhrzeigersinn gespielt.
  ```
- `c110` (`source_c.md`) — 'Nachdem sich Ostwind seine 14 Ziegel genommen hat, beginnt er das Spiel, indem er nach einer eventuellen Meldung einen Stein offen in der Mitte des Tisches ablegt, dabei nennt er dessen Namen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Nachdem sich Ostwind seine 14 Ziegel genommen hat, beginnt er das Spiel, indem er nach einer eventuellen Meldung einen Stein offen in der Mitte des Tisches ablegt, dabei nennt er dessen Namen.
  In the merge:  Nachdem sich Ostwind seine 14 Ziegel genommen hat, beginnt er das Spiel, indem er nach einer eventuellen Meldung einen Stein offen in der Mitte des Tisches ablegt, dabei nennt er dessen Namen.
  ```
- `c111` (`source_c.md`) — 'Wenn kein Spieler den abgelegten Stein aufruft, so zieht der rechte Nachbar einen Stein vom lebenden Ende der Mauer, meldet, wenn er möchte, eine oder mehrere Figuren und legt zuletzt einen Stein ab.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wenn kein Spieler den abgelegten Stein aufruft, so zieht der rechte Nachbar einen Stein vom lebenden Ende der Mauer, meldet, wenn er möchte, eine oder mehrere Figuren und legt zuletzt einen Stein ab.
  In the merge:  Wenn kein Spieler den abgelegten Stein aufruft, so zieht der rechte Nachbar einen Stein vom lebenden Ende der Mauer, meldet, wenn er möchte, eine oder mehrere Figuren und legt zuletzt einen Stein ab.
  ```
- `c112` (`source_c.md`) — 'Wird ein Stein abgelegt, so ist er tot, er bleibt offen in der Mitte des Tisches liegen und der nächste Spieler kann einen Chow spielen, sowie jener und alle weiteren Spieler einen Pong oder einen Kong.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wird ein Stein abgelegt, so ist er tot, er bleibt offen in der Mitte des Tisches liegen und der nächste Spieler kann einen Chow spielen, sowie jener und alle weiteren Spieler einen Pong oder einen Kong.
  In the merge:  Wird ein Stein abgelegt, so ist er tot, er bleibt offen in der Mitte des Tisches liegen und der nächste Spieler kann einen Chow spielen, sowie jener und alle weiteren Spieler einen Pong oder einen Kong.
  ```
- `c113` (`source_c.md`) — 'Danach ist der Stein nicht mehr für das Spiel verfügbar beziehungsweise aufnehmbar.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Danach ist der Stein nicht mehr für das Spiel verfügbar beziehungsweise aufnehmbar.
  In the merge:  Danach ist der Stein nicht mehr für das Spiel verfügbar beziehungsweise aufnehmbar.
  ```
- `c114` (`source_c.md`) — 'Wird ein Stein von einem Spieler aufgerufen, so nimmt der Spieler den abgelegten Stein und muss die betreffende Figur offen auflegen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wird ein Stein von einem Spieler aufgerufen, so nimmt der Spieler den abgelegten Stein und muss die betreffende Figur offen auflegen.
  In the merge:  Wird ein Stein von einem Spieler aufgerufen, so nimmt der Spieler den abgelegten Stein und muss die betreffende Figur offen auflegen.
  ```
- `c115` (`source_c.md`) — 'Danach wirft er einen Stein ab, und das Spiel wird mit diesem Spieler fortgesetzt.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Danach wirft er einen Stein ab, und das Spiel wird mit diesem Spieler fortgesetzt.
  In the merge:  Danach wirft er einen Stein ab, und das Spiel wird mit diesem Spieler fortgesetzt.
  ```
- `c116` (`source_c.md`) — 'Auf diese Weise können auch Spieler übergangen werden: Legt beispielsweise Südwind einen Stein ab, der von Nordwind gerufen wird, so wird Westwind übersprungen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Auf diese Weise können auch Spieler übergangen werden: Legt beispielsweise Südwind einen Stein ab, der von Nordwind gerufen wird, so wird Westwind übersprungen.
  In the merge:  Auf diese Weise können auch Spieler übergangen werden: Legt beispielsweise Südwind einen Stein ab, der von Nordwind gerufen wird, so wird Westwind übersprungen.
  ```
- `c117` (`source_c.md`) — 'Wird ein Ziegel von mehreren Spielern gerufen, so gilt folgende Rangordnung: Benötigt ein Spieler den Stein für einen Mah-Jongg-Ruf, so hat er Vorrang gegenüber einem Kong- oder Pong-Ruf und diese wiederum haben Vorrang vor einem Chow.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Wird ein Ziegel von mehreren Spielern gerufen, so gilt folgende Rangordnung: Benötigt ein Spieler den Stein für einen Mah-Jongg-Ruf, so hat er Vorrang gegenüber einem Kong- oder Pong-Ruf und diese wiederum haben Vorrang vor einem Chow.
  In the merge:  Wird ein Ziegel von mehreren Spielern gerufen, so gilt folgende Rangordnung: Benötigt ein Spieler den Stein für einen Mah-Jongg-Ruf, so hat er Vorrang gegenüber einem Kong- oder Pong-Ruf und diese wiederum haben Vorrang vor einem Chow.
  ```
- `c121` (`source_c.md`) — 'Die Bewertung der Spielbilder setzt sich aus folgenden Teilen zusammen.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Die Bewertung der Spielbilder setzt sich aus folgenden Teilen zusammen.
  In the merge:  Die Bewertung der Spielbilder setzt sich aus folgenden Teilen zusammen.
  ```
- `c125` (`source_c.md`) — 'Verdeckte Kombinationen zählen das Doppelte.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Verdeckte Kombinationen zählen das Doppelte.
  In the merge:  Verdeckte Kombinationen zählen das Doppelte.
  ```
- `c127` (`source_c.md`) — 'Ein Kong zählt viermal so viel wie der entsprechende Pong.' is declared 'subsumed' but the merge carries it unchanged, and no other source has it to have superseded it; the record describes a departure that did not happen

  ```text
  In the source: Ein Kong zählt viermal so viel wie der entsprechende Pong.
  In the merge:  Ein Kong zählt viermal so viel wie der entsprechende Pong.
  ```

### Verbatim violation — an invariant-core token did not survive unchanged

- `a3` (`source_a.md`) — numeric '5' does not survive into the merge unchanged
- `a42` (`source_a.md`) — numeric '255' does not survive into the merge unchanged

### Over budget — declared loss past the ceiling

- 43 of 216 segments are declared dropped (19.9%), over the 3% budget

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

> **Over budget.** The merge declared **43** drop(s) of 216 source segment(s), **19.9%**, over the 3% budget: past that share the omissions are the finding, whatever each one says about itself.

## Declarations

The merge declared **216** departure(s) from its sources. Checking them confirms 120, rejects 41, and leaves 55 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 43 of 216 source segment(s) declared gone, **19.9%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `a1` | subsumed | Moved to Prämienpunkte section; content preserved in proper section. | **rejected** | declared 'subsumed', which predicts SUPPORTED; A-001 came back PARTIAL (`A-001`) |
| `a2` | dropped | Section heading replaced by reconciled full content from both documents. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `a3` | subsumed | Merged with c98-c99 in Kong section; full logic preserved. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a4` | subsumed | Integrated into Kong section after c99. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-002`) |
| `a5` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `a6` | subsumed | Opening sentence of Verdopplungen section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a7` | subsumed | Integrated into Verdopplungen section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-003`) |
| `a8` | subsumed | Integrated into Verdopplungen section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a9` | dropped | Introductory line subsumed into structure; specific conditions not detailed in s | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `a10` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `a11` | subsumed | First sentence of Limit section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a12` | subsumed | Second sentence of Limit section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-004`) |
| `a13` | subsumed | Third sentence of Limit section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-005`) |
| `a14` | subsumed | Integrated into Limit section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-006`) |
| `a15` | subsumed | Integrated into Limit section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-007`) |
| `a16` | subsumed | Integrated into Limit section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-008`) |
| `a17` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `a18` | subsumed | First sentence of Anmerkungen section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a19` | subsumed | Second sentence of Anmerkungen section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a20` | dropped | Section heading; content (a21) follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `a21` | subsumed | Integrated as standalone section Die Abrechnung. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a22` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `a23` | subsumed | First sentence of Blumen- und Jahreszeitenziegel section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-009`) |
| `a24` | subsumed | Integrated into Blumen- und Jahreszeitenziegel section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-010`, `A-011`) |
| `a25` | subsumed | Integrated into Blumen- und Jahreszeitenziegel section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-012`, `A-013`, `A-014`, `A-015`) |
| `a26` | dropped | Introductory clause; no detailed scoring table provided in sources. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `a27` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `a28` | subsumed | First sentence of Runden und Partien section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-016`) |
| `a29` | subsumed | Second sentence of Runden und Partien section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-017`) |
| `a30` | subsumed | Integrated into Runden und Partien section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-018`) |
| `a31` | subsumed | Integrated into Runden und Partien section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-019`) |
| `a32` | subsumed | Integrated into Runden und Partien section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-020`) |
| `a33` | subsumed | Integrated into Runden und Partien section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-021`, `A-022`, `A-023`, `A-024`) |
| `a34` | subsumed | Integrated into Runden und Partien section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a35` | subsumed | Integrated into Runden und Partien section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-025`) |
| `a36` | subsumed | Integrated into Runden und Partien section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-026`, `A-027`) |
| `a37` | subsumed | Integrated into Runden und Partien section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-028`, `A-029`) |
| `a38` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `a39` | subsumed | First sentence of Varianten section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a40` | subsumed | Integrated into Varianten section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-030`) |
| `a41` | subsumed | Integrated into Varianten section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a42` | reworded | Fixed incomplete segment by adding 'Sportart anerkannt wurde' from context. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `a43` | subsumed | Integrated into Varianten section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-032`) |
| `a44` | subsumed | Integrated into Varianten section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-033`) |
| `a45` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', which predicts MISSING; A-034 came back SUPPORTED (`A-034`) |
| `a46` | subsumed | First sentence of Mah-Jongg als Computerspiel section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a47` | subsumed | Integrated into Computerspiel section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-035`) |
| `a48` | subsumed | Integrated into Computerspiel section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-036`) |
| `a49` | subsumed | Integrated into Computerspiel section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-037`) |
| `a50` | subsumed | Integrated into Computerspiel section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-038`) |
| `a51` | subsumed | Integrated into Computerspiel section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-039`) |
| `a52` | subsumed | Integrated into Computerspiel section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`A-040`) |
| `a53` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', which predicts MISSING; A-041 came back SUPPORTED, A-042 came back SUPPORTED (`A-041`, `A-042`) |
| `a54` | subsumed | Consolidated with b55-b58 into Online-Plattformen section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a55` | subsumed | Part of Online-Plattformen section consolidation. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a56` | subsumed | Part of Online-Plattformen section consolidation. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `a57` | dropped | Subsection heading; content merged into parent section. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `a58` | dropped | Subsection heading; content merged into parent section. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `b1` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `b2` | subsumed | First sentence of Mah-Jongg Solitaire section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b3` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-001`, `B-002`) |
| `b4` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-003`) |
| `b5` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-004`) |
| `b6` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-005`) |
| `b7` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-006`) |
| `b8` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-007`, `B-008`) |
| `b9` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-009`) |
| `b10` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-010`) |
| `b11` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-011`) |
| `b12` | subsumed | Integrated into Mah-Jongg Solitaire section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b13` | subsumed | Integrated into Mah-Jongg Solitaire section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b14` | subsumed | Integrated into Mah-Jongg Solitaire section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b15` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-012`) |
| `b16` | subsumed | Integrated into Mah-Jongg Solitaire section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-013`) |
| `b17` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `b18` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `b19` | subsumed | First sentence of Mah-Jongg in Manga und Anime section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-014`, `B-015`, `B-016`, `B-017`, `B-018`) |
| `b20` | subsumed | Second sentence of Mah-Jongg in Manga und Anime section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b21` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `b22` | subsumed | Integrated into Mah-Jongg in Film und Literatur section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-019`) |
| `b23` | subsumed | Integrated into Mah-Jongg in Film und Literatur section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-020`, `B-021`) |
| `b24` | subsumed | Integrated into Mah-Jongg in Film und Literatur section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-022`) |
| `b25` | subsumed | Integrated into Mah-Jongg in Film und Literatur section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b26` | subsumed | Integrated into Mah-Jongg in Film und Literatur section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-024`) |
| `b27` | subsumed | Integrated into Mah-Jongg in Film und Literatur section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`B-025`, `B-026`) |
| `b28` | subsumed | Integrated into Mah-Jongg in Film und Literatur section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `b29` | dropped | Source citation; not part of article content. | **confirmed** | no claim was drawn from this segment, and its text is not in the merge, which is what 'dropped' says happened to it (no claim traced to it) |
| `c1` | subsumed | Used as opening paragraph. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-001`) |
| `c2` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c3` | subsumed | First sentence of Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-002`, `C-003`, `C-004`, `C-005`) |
| `c4` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-006`, `C-007`) |
| `c5` | subsumed | Integrated into Geschichte section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c6` | subsumed | Integrated into Geschichte section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c7` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-008`, `C-009`) |
| `c8` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-010`) |
| `c9` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-011`) |
| `c10` | subsumed | Integrated into Geschichte section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c11` | subsumed | Integrated into Geschichte section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c12` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-012`) |
| `c13` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-013`, `C-014`) |
| `c14` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-015`, `C-016`, `C-017`) |
| `c15` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-018`) |
| `c16` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-019`) |
| `c17` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-020`) |
| `c18` | subsumed | Integrated into Geschichte section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c19` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-022`) |
| `c20` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-023`) |
| `c21` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-024`, `C-025`) |
| `c22` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-026`) |
| `c23` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-029`, `C-030`) |
| `c24` | subsumed | Integrated into Geschichte section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c25` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-031`, `C-032`) |
| `c26` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-033`, `C-034`) |
| `c27` | subsumed | Integrated into Geschichte section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-035`, `C-036`) |
| `c28` | subsumed | Integrated into Geschichte section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c29` | subsumed | Integrated into Geschichte section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c30` | subsumed | Integrated into Geschichte section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c31` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c32` | subsumed | First sentence of Die Spielsteine section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c33` | subsumed | Integrated into Die Spielsteine section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c34` | subsumed | Integrated into Die Spielsteine section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c35` | subsumed | Integrated into Die Spielsteine section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c36` | subsumed | Integrated into Die Spielsteine section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c37` | dropped | Introductory clause to list; list itself not provided in sources. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c38` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', which predicts MISSING; C-037 came back SUPPORTED (`C-037`) |
| `c39` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c40` | dropped | Subsection heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c41` | subsumed | First sentence of Allgemeines section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c42` | subsumed | Integrated into Allgemeines section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c43` | subsumed | Integrated into Allgemeines section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c44` | subsumed | Integrated into Allgemeines section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-038`, `C-039`) |
| `c45` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c46` | dropped | Subsection heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c47` | subsumed | First sentence of Die Sitzordnung section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-040`) |
| `c48` | subsumed | Integrated into Die Sitzordnung section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-041`) |
| `c49` | subsumed | Integrated into Die Sitzordnung section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c50` | subsumed | Integrated into Die Sitzordnung section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c51` | subsumed | Integrated into Die Sitzordnung section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c52` | subsumed | Integrated into Die Sitzordnung section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-042`, `C-043`, `C-044`, `C-045`) |
| `c53` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c54` | subsumed | First sentence of Die Mauer section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c55` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-046`) |
| `c56` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-047`) |
| `c57` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-048`) |
| `c58` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-049`) |
| `c59` | subsumed | Integrated into Die Mauer section. | **rejected** | declared 'subsumed', which predicts SUPPORTED; C-050 came back CONTRADICTED (`C-050`) |
| `c60` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-051`) |
| `c61` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-052`) |
| `c62` | subsumed | Integrated into Die Mauer section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c63` | subsumed | Integrated into Die Mauer section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c64` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-053`, `C-054`, `C-055`) |
| `c65` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-056`) |
| `c66` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-057`, `C-058`) |
| `c67` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-059`, `C-060`) |
| `c68` | subsumed | Integrated into Die Mauer section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-061`, `C-062`) |
| `c69` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c70` | subsumed | First sentence of Das Ziel des Spiels section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-063`) |
| `c71` | subsumed | Integrated into Das Ziel des Spiels section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c72` | subsumed | Integrated into Das Ziel des Spiels section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-064`) |
| `c73` | subsumed | Integrated into Das Ziel des Spiels section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-065`) |
| `c74` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c75` | dropped | Subsection heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c76` | subsumed | Integrated into Paare section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-066`) |
| `c77` | subsumed | Integrated into Paare section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-067`, `C-068`) |
| `c78` | subsumed | Integrated into Paare section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-069`) |
| `c79` | dropped | Subsection heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c80` | subsumed | First sentence of Drillinge (Pong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-070`) |
| `c81` | subsumed | Integrated into Drillinge (Pong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-071`, `C-072`) |
| `c82` | subsumed | Integrated into Drillinge (Pong) section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c83` | subsumed | Integrated into Drillinge (Pong) section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c84` | subsumed | Integrated into Drillinge (Pong) section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c85` | subsumed | Integrated into Drillinge (Pong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-074`) |
| `c86` | subsumed | Integrated into Drillinge (Pong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-075`) |
| `c87` | subsumed | Integrated into Drillinge (Pong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-076`) |
| `c88` | dropped | Subsection heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c89` | subsumed | First sentence of Vierlinge (Kong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-077`) |
| `c90` | subsumed | Integrated into Vierlinge (Kong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-078`) |
| `c91` | subsumed | Integrated into Vierlinge (Kong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-079`, `C-080`) |
| `c92` | subsumed | Integrated into Vierlinge (Kong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-081`) |
| `c93` | subsumed | Integrated into Vierlinge (Kong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-082`, `C-083`) |
| `c94` | subsumed | Integrated into Vierlinge (Kong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-084`) |
| `c95` | subsumed | Integrated into Vierlinge (Kong) section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c96` | subsumed | Integrated into Vierlinge (Kong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-087`) |
| `c97` | subsumed | Integrated into Vierlinge (Kong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-088`) |
| `c98` | subsumed | Integrated into Vierlinge (Kong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-089`) |
| `c99` | subsumed | Integrated into Vierlinge (Kong) section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c100` | subsumed | Integrated into Vierlinge (Kong) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-091`) |
| `c101` | dropped | Subsection heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c102` | subsumed | First sentence of Folgen (Chow) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-092`, `C-093`) |
| `c103` | subsumed | Integrated into Folgen (Chow) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-094`) |
| `c104` | subsumed | Integrated into Folgen (Chow) section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c105` | subsumed | Integrated into Folgen (Chow) section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c106` | subsumed | Integrated into Folgen (Chow) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-096`) |
| `c107` | subsumed | Integrated into Folgen (Chow) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-097`) |
| `c108` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c109` | subsumed | First sentence of Spielablauf section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-098`) |
| `c110` | subsumed | Integrated into Spielablauf section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-099`) |
| `c111` | subsumed | Integrated into Spielablauf section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-100`) |
| `c112` | subsumed | Integrated into Spielablauf section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-101`, `C-102`, `C-103`, `C-104`) |
| `c113` | subsumed | Integrated into Spielablauf section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-105`) |
| `c114` | subsumed | Integrated into Spielablauf section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-106`) |
| `c115` | subsumed | Integrated into Spielablauf section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-107`) |
| `c116` | subsumed | Integrated into Spielablauf section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-108`) |
| `c117` | subsumed | Integrated into Spielablauf section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-109`, `C-110`) |
| `c118` | dropped | Incomplete sentence; continuation not provided in sources. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c119` | subsumed | Integrated into Spielablauf section with assumed completion. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c120` | dropped | Section heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c121` | subsumed | First sentence of Bewertung section. | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'subsumed' is what happened to it (no claim traced to it) |
| `c122` | dropped | Subsection heading; content follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c123` | dropped | Subsubsection heading; detailed values not provided. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c124` | dropped | Subsubsection heading; detailed values not provided. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c125` | subsumed | Integrated into Drillinge (Pongs) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-111`) |
| `c126` | dropped | Subsubsection heading; detailed explanation follows. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c127` | subsumed | Integrated into Vierlinge (Kongs) section. | **confirmed** | declared 'subsumed' and every claim from it came back SUPPORTED (`C-112`) |
| `c128` | dropped | Subsubsection heading; no detailed content provided. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |
| `c129` | dropped | Section heading; no detailed content provided. | **rejected** | declared 'dropped', and its text is in the merge (no claim traced to it) |


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
| Calls | 29 live, 0 cached, 0 replayed |
| Tokens | 284,035 in, 123,793 out |
| Cost | ~$0.90 estimated (rates read 2026-08-31) |
| Schema repairs | 5 |
| Errors | 0 |
| Duration | 1024.6s |
| Generated | 2026-09-27T18:26:18+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
