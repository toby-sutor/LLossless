## Verdict

**1 finding(s).** In the claims: 1 contradicted.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 142 |
| Claims extracted from `source_a.md` | 45 |
| Claims extracted from `source_b.md` | 44 |
| Claims extracted from `source_c.md` | 129 |
| Forward — source claims accounted for in the merge | **218/218** |
| Forward — carried only in part | 0 |
| Forward — `source_a.md` claims accounted for | **45/45** |
| Forward — `source_b.md` claims accounted for | **44/44** |
| Forward — `source_c.md` claims accounted for | **129/129** |
| Reverse — merge claims found in a source | **141/142** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **360/360** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Contradicted — the merge states something different

- **M-029** -- the two documents disagree
  - `merged.md:11` says: A rumor circulated that imported games were infested with vermin.
  - `source_c.md` says: 'zumal das Gerücht umging, importierte Spiele wären mit Viren verseucht' (grounded)
  - judged against: `source_a.md`, `source_b.md` and `source_c.md`
  - why this was read as a contradiction: Source says the rumor was about games infested with viruses (Viren), not vermin.

## Length capped

- `$.decisions[0].reason` was 83 characters, over the 80-character cap; capped to fit

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 45 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 45 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | The Mah-Jongg caller receives an additional bonus of 10 (often 20) points credited. | 1 | carried | 'Der Mah-Jongg-Rufer erhält eine zusätzliche Prämie von 10 (häufig 20) Punkten gutgeschrieben.' in `merged.md` -- Directly stated. |
| 2 | For robbing the kong, the player receives an additional bonus of 10 points. | 5 | carried | 'Für diese Beraubung des Kong erhält er einen zusätzlichen Bonus von 10 Punkten.' in `merged.md` -- Directly stated. |
| 3 | Doubling twice quadruples the original value of the hand. | 9 | carried | 'zweimaliges Verdoppeln vervierfacht beispielsweise den ursprünglichen Wert des Spielbildes' in `merged.md` -- Directly stated. |
| 4 | The limit is usually 300 or 500 points. | 17 | carried | 'Dieses beträgt meist 300 oder 500 Punkte.' in `merged.md` -- Directly stated. |
| 5 | If the calculated point value exceeds the agreed limit, the hand is counted only with this maximum value. | 17 | carried | 'Übersteigt der errechnete Punktewert das vereinbarte Limit, so wird das Spielbild nur mit diesem Höchstwert gezählt.' in `merged.md` -- Directly stated. |
| 6 | If the Mah-Jongg caller's hand consists exclusively of tiles of the trump suit, that is only wind and dragon tiles, this hand is scored with the maximum points. | 19 | carried | 'Besteht das Spielbild des Mah-Jongg-Rufers ausschließlich aus Ziegeln der Trumpffarbe, also nur aus Wind- und Drachenziegeln, so wird diese Hand mit dem Punktemaximum bewertet.' in `merged.md` -- Directly stated. |
| 7 | If East Wind can call Mah-Jongg immediately after picking up his tiles, he possesses the Blessing of Heaven and receives the maximum points credited. | 21 | carried | 'Kann Ostwind sofort nach Aufnehmen seiner Ziegel Mah-Jongg rufen, so besitzt er den Segen des Himmels und erhält das Punktemaximum gutgeschrieben.' in `merged.md` -- Directly stated. |
| 8 | If another player can claim the first tile discarded by East Wind and thereby declare Mah-Jongg, this is the Blessing of the Earth and the player receives half of the limit credited. | 21 | carried | 'Kann ein anderer Spieler den ersten von Ostwind abgelegten Stein aufrufen und damit Mah-Jongg erklären, so ist dies der Segen der Erde und der Spieler erhält die Hälfte des Limits gutgeschrieben.' in `merged.md` -- Directly stated. |
| 9 | When Mah-Jongg is played with 144 tiles, including the tiles of the main suit (the flower and season tiles), each side of the wall consists of 18 tile stacks. | 33 | carried | 'Wird Mah-Jongg mit 144 Steinen, also einschließlich der Steine der Hauptfarbe (der Blumen- und Jahreszeitenziegel), gespielt, so besteht jede Seite der Mauer aus 18 Ziegelstapeln.' in `merged.md` -- Directly stated. |
| 10 | As soon as a player picks up his tiles at the start of a game, he lays his flower and season tiles openly in front of him. | 33 | carried | 'Sobald ein Spieler zu Beginn eines Spieles seine Steine aufnimmt, legt er seine Blumen- und Jahreszeitenziegel offen vor sich' in `merged.md` -- Directly stated. |
| 11 | The player draws a replacement tile from the dead end of the wall for a flower or season tile. | 33 | carried | 'und zieht dafür einen Ersatzziegel vom toten Ende der Mauer' in `merged.md` -- Directly stated. |
| 12 | The same procedure is followed when a player buys such a tile from the wall. | 33 | carried | 'ebenso wird verfahren, wenn ein Spieler einen solchen Stein von der Mauer kauft.' in `merged.md` -- Directly stated. |
| 13 | The tiles of the main suit are assigned to the four winds. | 35 | carried | 'Die Ziegel der Hauptfarbe sind den vier Winden zugeordnet' in `merged.md` -- Directly stated. |
| 14 | Tile No. 1 applies to East Wind. | 35 | carried | 'Nr. 1 gilt für den Ostwind' in `merged.md` -- Directly stated. |
| 15 | Tile No. 2 applies to South Wind. | 35 | carried | 'Nr. 2 für den Südwind' in `merged.md` -- Directly stated. |
| 16 | Tile No. 3 applies to West Wind. | 35 | carried | 'Nr. 3 für den Westwind' in `merged.md` -- Directly stated. |
| 17 | Tile No. 4 applies to North Wind. | 35 | carried | 'Nr. 4. für den Nordwind' in `merged.md` -- Directly stated. |
| 18 | If East Wind can call Mah-Jongg, he remains East Wind in the next game. | 39 | carried | 'Wenn Ostwind Mah-Jongg rufen kann, so bleibt er im nächsten Spiel weiter Ostwind' in `merged.md` -- Directly stated. |
| 19 | If East Wind can call Mah-Jongg, the other positions also remain unchanged. | 39 | carried | 'und auch die übrigen Positionen bleiben unverändert.' in `merged.md` -- Directly stated. |
| 20 | If another player calls Mah-Jongg, the previous South Wind takes over the role of East Wind. | 39 | carried | 'Wenn ein anderer Spieler Mah-Jongg ruft, so übernimmt der bisherige Südwind die Rolle von Ostwind' in `merged.md` -- Directly stated. |
| 21 | If another player calls Mah-Jongg, the positions shift by one place counterclockwise. | 39 | carried | 'und die Positionen wechseln um einen Platz gegen den Uhrzeigersinn.' in `merged.md` -- Directly stated. |
| 22 | A round ends as soon as the player who held the position of North Wind in the first game loses a game as East Wind. | 41 | carried | 'Eine Runde ist beendet, sobald der Spieler, der im ersten Spiel die Position des Nordwindes innehatte, ein Spiel als Ostwind verliert' in `merged.md` -- Directly stated. |
| 23 | A round consists of at least four games. | 41 | carried | 'Eine Runde besteht aus mindestens vier Spielen.' in `merged.md` -- Directly stated. |
| 24 | If not just a single round is played but a match is agreed upon, the match consists of four rounds. | 43 | carried | 'Wird nicht nur eine einzelne Runde gespielt, sondern eine Partie vereinbart, so besteht diese aus vier Runden.' in `merged.md` -- Directly stated. |
| 25 | In the first round, the East Wind round, East is the prevailing wind. | 43 | carried | 'In der ersten Runde, der Ostwindrunde, ist Ost der vorherrschende Wind (Rundenwind)' in `merged.md` -- Directly stated. |
| 26 | In the second round, the South Wind round, South Wind prevails. | 43 | carried | 'in der zweiten Runde (Südwindrunde) herrscht Südwind vor' in `merged.md` -- Directly stated. |
| 27 | The third round is the West Wind round. | 43 | carried | 'die dritte Runde ist die Westwindrunde' in `merged.md` -- Directly stated. |
| 28 | The fourth round is the North Wind round. | 43 | carried | 'und die vierte die Nordwindrunde.' in `merged.md` -- Directly stated. |
| 29 | A small box (Mingg) is used to count the individual games and rounds. | 47 | carried | 'Um die einzelnen Spiele und Runden mitzuzählen, wird eine kleine Dose (Mingg) verwendet.' in `merged.md` -- Directly stated. |
| 30 | This box is placed on the table by the respective player of East Wind. | 47 | carried | 'Diese stellt der jeweilige Spieler des Ostwindes vor sich auf den Tisch' in `merged.md` -- Directly stated. |
| 31 | The place tile of the prevailing wind is placed on top of the Mingg. | 47 | carried | 'der Platzstein des vorherrschenden Windes wird oben auf die Mingg gelegt.' in `merged.md` -- Directly stated. |
| 32 | Before a further match, the seating positions are drawn anew. | 49 | carried | 'Vor einer weiteren Partie werden die Sitzplätze neu gelost' in `merged.md` -- Directly stated. |
| 33 | Usually no more than two matches are played. | 49 | carried | 'meist werden nicht mehr als zwei Partien gespielt.' in `merged.md` -- Directly stated. |
| 34 | In traditional Chinese play, certain hands are scored with the maximum points (limit). | 53 | carried | 'Im traditionellen chinesischen Spiel werden bestimmte Spielbilder mit dem Punktemaximum (Limit) bewertet.' in `merged.md` -- Directly stated. |
| 35 | Some of these hands were already named by Babcock in his Red Book of 1920. | 53 | carried | 'die teilweise bereits Babcock in seinem Red Book von 1920 angeführt hat' in `merged.md` -- Directly stated. |
| 36 | Modern Mah-Jongg was officially recognized in 1998 by China's state sports commission as the 255th sport. | 55 | carried | 'so wie es 1998 von der staatlichen Sportkommission Chinas offiziell als 255. Sportart anerkannt wurde' in `merged.md` -- Directly stated. |
| 37 | The official rules of this modern style of play are applied at international tournaments such as world and European championships. | 57 | carried | 'Die offiziellen Regeln dieser modernen Spielweise finden bei internationalen Turnieren wie Welt- und Europameisterschaften Anwendung.' in `merged.md` -- Directly stated. |
| 38 | In the ranking of the European Mahjong Association, only results achieved under these game rules are considered. | 57 | carried | 'In der Rangliste der European Mahjong Association werden nur Ergebnisse berücksichtigt, die aufgrund dieser Spielregeln erzielt wurden.' in `merged.md` -- Directly stated. |
| 39 | The Finnish manufacturer Lagarto offers a paid Windows version of traditional Mah-Jongg called Four Winds. | 61 | carried | 'Der finnische Hersteller Lagarto bietet eine kostenpflichtige Windows-Version des traditionellen Mah-Jongg namens Four Winds an.' in `merged.md` -- Directly stated. |
| 40 | A player can compete against three players simulated by the software. | 61 | carried | 'Ein Spieler kann gegen drei durch die Software nachgebildete Spieler antreten.' in `merged.md` -- Directly stated. |
| 41 | Several real players can compete against each other or against the software over a network. | 61 | carried | 'Ebenso können über ein Netzwerk mehrere reale Spieler gegeneinander oder gegen die Software antreten.' in `merged.md` -- Directly stated. |
| 42 | The KDE project contains a free version of Mah-Jongg called Kajongg. | 61 | carried | 'Das KDE-Projekt enthält eine kostenfreie Version von Mah-Jongg, die Kajongg genannt wird.' in `merged.md` -- Directly stated. |
| 43 | In various parts of the Yakuza game series, such as Yakuza 0, the Japanese variant of Mah-Jongg (Riichi Mahjong) is available as a minigame. | 63 | carried | 'In verschiedenen Teilen der Yakuza-Spieleserie, wie zum Beispiel Yakuza 0 ist die japanische Variante von Mah-Jongg (Riichi Mahjong) als Minispiel vorhanden.' in `merged.md` -- Directly stated. |
| 44 | For iPhone and iPad there is a traditional version in the Apple App Store called Mahjong! by POK-Software. | 65 | carried | 'Für iPhone und iPad gibt es im Apple App Store unter dem Namen Mahjong! von POK-Software eine traditionelle Version' in `merged.md` -- Directly stated. |
| 45 | The Mahjong! app by POK-Software simulates up to 3 co-players. | 65 | carried | 'die bis zu 3 Mitspieler simuliert.' in `merged.md` -- Directly stated. |

### `source_b.md` -- 44 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 44 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Many computer games described as Mah-Jongg use digitized forms of the game tiles. | 4 | carried | 'Viele andere als Mah-Jongg bezeichnete Computerspiele verwenden zwar digitalisierte Formen der Spielsteine' in `merged.md` -- Directly stated. |
| 2 | Many computer games described as Mah-Jongg are mostly games for only one person. | 4 | carried | 'sind jedoch meistens Spiele für nur eine Person' in `merged.md` -- Directly stated. |
| 3 | Many computer games described as Mah-Jongg resemble a solitaire game in their rules (Mah-Jongg Solitaire). | 4 | carried | 'und ähneln von den Regeln einer Patience (Mah-Jongg Solitaire).' in `merged.md` -- Directly stated. |
| 4 | From the mid-1980s, Mah-Jongg Solitaire first became popular as a computer game under the name Shanghai. | 4 | carried | 'Ab Mitte der 1980er Jahre wurde Mah-Jongg Solitaire zunächst unter dem Namen Shanghai als Computerspiel populär' in `merged.md` -- Directly stated. |
| 5 | The improved graphical capabilities of the new Amiga computer first allowed an appealing depiction of the Mah-Jongg Solitaire game. | 4 | carried | 'nachdem die verbesserten grafischen Möglichkeiten des neuen Amiga-Computers erstmals eine ansprechende Darstellung dieses Spiels erlaubten.' in `merged.md` -- Directly stated. |
| 6 | In the most popular computer game variant, all 144 tiles lie on the table at the start of the game. | 6 | carried | 'Bei der beliebtesten Computerspiel-Variante liegen zu Spielbeginn alle 144 Steine auf dem Tisch' in `merged.md` -- Directly stated. |
| 7 | In the most popular computer game variant, the tiles lie partly in several layers on top of each other. | 6 | carried | 'teils in mehreren Lagen übereinander.' in `merged.md` -- Directly stated. |
| 8 | Traditionally, the game tiles are arranged in the figure of a dragon or a turtle. | 6 | carried | 'Traditionell werden die Spielsteine in der Figur eines Drachen oder einer Schildkröte aufgebaut' in `merged.md` -- Directly stated. |
| 9 | The computer game variants often offer many different starting figures. | 6 | carried | 'die Computerspielvarianten bieten oft viele verschiedene Startfiguren an.' in `merged.md` -- Directly stated. |
| 10 | A single player must remove all 144 tiles from the table in pairs. | 6 | carried | 'Ein einzelner Spieler muss paarweise alle 144 Steine vom Tisch nehmen.' in `merged.md` -- Directly stated. |
| 11 | A pair may only be removed if both tiles are not partially or fully covered by any other tile and are exposed on at least one long side. | 6 | carried | 'Ein Paar darf nur abgetragen werden, wenn beide Steine von keinem anderen Stein teilweise oder vollständig überdeckt sind und an zumindest einer Längsseite freiliegen.' in `merged.md` -- Directly stated. |
| 12 | The tiles of the main suits each occur only once and cannot form pairs. | 6 | carried | 'Während die Steine der Hauptfarben jeweils nur einmal vorkommen und keine Paare bilden können' in `merged.md` -- Directly stated. |
| 13 | The flower tiles may be combined arbitrarily among each other. | 6 | carried | 'dürfen die Blumenziegel und die Jahreszeitenziegel jeweils untereinander beliebig kombiniert werden' in `merged.md` -- States flower tiles can be combined among themselves. |
| 14 | The season tiles may be combined arbitrarily among each other. | 6 | carried | 'dürfen die Blumenziegel und die Jahreszeitenziegel jeweils untereinander beliebig kombiniert werden' in `merged.md` -- States season tiles can be combined among themselves. |
| 15 | An example combination is the plum tile with the orchid tile. | 6 | carried | 'beispielsweise Pflaume mit Orchidee' in `merged.md` -- Directly stated. |
| 16 | An example combination is the winter tile with the spring tile. | 6 | carried | 'oder Winter mit Frühling' in `merged.md` -- Directly stated. |
| 17 | In some variants, the flower and season tiles are doubled. | 6 | carried | 'In einigen Varianten sind die Blumen- und Jahreszeitenziegel verdoppelt' in `merged.md` -- Directly stated. |
| 18 | In some variants, the wind tiles are correspondingly reduced to only two. | 6 | carried | 'und dafür zum Ausgleich beispielsweise die Windziegel nur zweimal enthalten.' in `merged.md` -- Directly stated. |
| 19 | In some variants, the season tiles occur twice and there are no flower tiles. | 6 | carried | 'Mitunter kommen die Jahreszeitenziegel doppelt vor und dafür keine Blumenziegel.' in `merged.md` -- Directly stated. |
| 20 | As a further development of computer games, there are now offerings on the internet where Mahjong Solitaire can be played online. | 8 | carried | 'Als Weiterentwicklung der Computerspiele gibt es heute Angebote auf dem Netz, auf denen Mahjong Solitaire online gespielt werden kann.' in `merged.md` -- Directly stated. |
| 21 | The online offerings are usually the single-player variant of the game. | 8 | carried | 'Dabei handelt es sich in der Regel meist um die Spielvariante für Einzelspieler' in `merged.md` -- Directly stated. |
| 22 | Through leaderboards or competitions, players effectively play against other Mahjong players. | 8 | carried | 'aber durch Bestenlisten oder Wettkämpfe spielt man quasi gegen andere Mahjong-Spieler.' in `merged.md` -- Directly stated. |
| 23 | The online offerings often include additional functions such as the display of still available pairs. | 8 | carried | 'Oft gibt es zusätzliche Funktionen, wie die Anzeige der noch verfügbaren Paare' in `merged.md` -- Directly stated. |
| 24 | The online offerings often include the possibility of undoing moves. | 8 | carried | 'oder die Möglichkeit Spielzüge rückgängig zu machen.' in `merged.md` -- Directly stated. |
| 25 | In the online variants, many game types beyond the traditional rules have become established. | 10 | carried | 'Bei den Online-Varianten haben sich viele Spielarten jenseits der traditionellen Regeln etabliert.' in `merged.md` -- Directly stated. |
| 26 | In Mahjong Connect, the identical game tiles can only be selected if a line can be drawn between them. | 10 | carried | 'Zum Beispiel können beim Mahjong Connect die identischen Spielsteine nur ausgewählt werden, wenn zwischen ihnen eine Linie gezogen werden kann.' in `merged.md` -- Directly stated. |
| 27 | In Mahjong Dimensions, there is no two-dimensional playing field. | 10 | carried | 'Beim Mahjong Dimensions gibt es kein zweidimensionales Spielfeld' in `merged.md` -- Directly stated. |
| 28 | In Mahjong Dimensions, the game tiles are joined into a three-dimensional object. | 10 | carried | 'sondern die Spielsteine sind zu einem dreidimensionalen Objekt gefügt.' in `merged.md` -- Directly stated. |
| 29 | In Japan, the genre of Mah-Jongg in anime and manga developed based on the game. | 16 | carried | 'In Japan entwickelte sich auf Grundlage des Spiels das Genre Mah-Jongg in Anime und Manga' in `merged.md` -- Directly stated. |
| 30 | Examples of Mah-Jongg in anime and manga include Saki, Tobaku Mokushiroku Kaiji, Akagi, and The Legend of Koizumi. | 16 | carried | '(siehe auch: Saki, Tobaku Mokushiroku Kaiji, Akagi, The Legend of Koizumi)' in `merged.md` -- Directly stated. |
| 31 | In these works, the game often serves as a narrative device to heighten strategic and dramatic conflicts. | 16 | carried | 'Dabei dient das Spiel dort häufig als erzählerisches Mittel zur Zuspitzung strategischer und dramatischer Konflikte.' in `merged.md` -- Directly stated. |
| 32 | The romantic film comedy Crazy Rich Asians was released in 2018. | 20 | carried | 'In der romantischen Filmkomödie Crazy Rich Asians (2018)' in `merged.md` -- Directly stated. |
| 33 | In Crazy Rich Asians, a Mah-Jongg game forms the dramaturgical climax of a central confrontation. | 20 | carried | 'bildet eine Mah-Jongg-Partie den dramaturgischen Höhepunkt einer zentralen Konfrontation.' in `merged.md` -- Directly stated. |
| 34 | The film Gefahr und Begierde is based on the short story of the same name by Eileen Chang. | 22 | carried | 'In dem Film Gefahr und Begierde, nach der gleichnamigen Kurzgeschichte von Eileen Chang' in `merged.md` -- Directly stated. |
| 35 | Ang Lee tells the story of a tragic love relationship between a resistance fighter and the intelligence chief of the collaborationist government of Wang Jingwei in the film Gefahr und Begierde. | 22 | carried | 'erzählt Ang Lee die Geschichte einer tragischen Liebesbeziehung zwischen einer Widerstandskämpferin und dem Geheimdienstchef der Kollaborationsregierung von Wang Jingwei.' in `merged.md` -- Directly stated. |
| 36 | The resistance fighter in Gefahr und Begierde is played by Tang Wei. | 22 | carried | 'die Widerstandskämpferin, gespielt von Tang Wei' in `merged.md` -- Directly stated. |
| 37 | In Gefahr und Begierde, the resistance fighter meets the wives of the government members. | 22 | carried | 'in denen die Widerstandskämpferin, gespielt von Tang Wei, auf die Ehefrauen der Regierungsmitglieder trifft.' in `merged.md` -- Directly stated. |
| 38 | In the crime novel Sous les vents de Neptun (German: "Der vierzehnte Stein") by Fred Vargas, the game Mah-Jongg plays a central role. | 24 | carried | 'Im Kriminalroman Sous les vents de Neptun (dt. „Der vierzehnte Stein“) von Fred Vargas (Frédérique Audoin-Rouzeau) nimmt das Spiel Mah-Jongg eine zentrale Rolle ein.' in `merged.md` -- Directly stated. |
| 39 | Fred Vargas is the pen name of Frédérique Audoin-Rouzeau. | 24 | carried | 'von Fred Vargas (Frédérique Audoin-Rouzeau)' in `merged.md` -- The parenthetical naming convention identifies Frédérique Audoin-Rouzeau as the real name behind the pen name Fred Vargas. |
| 40 | The book Sous les vents de Neptun was filmed in 2008. | 24 | carried | 'Das Buch wurde 2008 verfilmt.' in `merged.md` -- Directly stated. |
| 41 | The French-Swiss feature film Die Gleichung ihres Lebens was released in 2023. | 26 | carried | 'Im französisch-Schweizer Spielfilm Die Gleichung ihres Lebens (2023)' in `merged.md` -- Directly stated. |
| 42 | In Die Gleichung ihres Lebens, the main character Marguerite learns Mah-Jongg after abandoning her mathematics doctorate. | 26 | carried | 'lernt die Hauptperson Marguerite nach dem Abbruch ihrer Mathematik-Promotion Mah-Jongg' in `merged.md` -- Directly stated. |
| 43 | In Die Gleichung ihres Lebens, Marguerite earns considerable income with Mah-Jongg. | 26 | carried | 'und erzielt erhebliche Einnahmen damit.' in `merged.md` -- Directly stated. |
| 44 | The structure of the game gives Marguerite inspiration for a return to mathematics. | 26 | carried | 'Die Struktur des Spiels liefert ihr wiederum Inspirationen für einen Wiedereinstieg in die Mathematik.' in `merged.md` -- Directly stated. |

### `source_c.md` -- 129 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 129 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Mah-Jongg is a Chinese game for four people. | 2 | carried | 'ist ein chinesisches Spiel für vier Personen.' in `merged.md` -- Directly stated. |
| 2 | Joseph Park Babcock was born in 1893. | 6 | carried | 'Joseph Park Babcock (1893–1949)' in `merged.md` -- Birth year given. |
| 3 | Joseph Park Babcock died in 1949. | 6 | carried | 'Joseph Park Babcock (1893–1949)' in `merged.md` -- Death year given. |
| 4 | Joseph Park Babcock was an American traveler in the Republic of China. | 6 | carried | 'ein amerikanischer Reisender in der Republik China' in `merged.md` -- Directly stated. |
| 5 | Joseph Park Babcock wrote a rulebook in the 1920s based on different variants he had learned. | 6 | carried | 'verfasste in den 1920er Jahren ein Regelwerk basierend auf unterschiedlichen Varianten, die er kennengelernt hatte' in `merged.md` -- Directly stated. |
| 6 | Joseph Park Babcock brought the game to the USA. | 6 | carried | 'und brachte das Spiel in die USA.' in `merged.md` -- Directly stated. |
| 7 | Babcock gave the game the name MAH-JONGG in that spelling. | 6 (unverified) | carried | 'Babcock gab ihm den Namen MAH-JONGG (in dieser Schreibweise)' in `merged.md` -- Directly stated. |
| 8 | Babcock had the name MAH-JONGG registered as a trademark. | 6 | carried | 'den er als Marke eintragen ließ.' in `merged.md` -- Directly stated. |
| 9 | This Western name refers to a sparrow depicted on the Bamboo-One playing tile. | 6 | carried | 'Dieser im Westen gebräuchliche Name bezeichnet einen Sperling, der auf dem Spielstein Bambus-Eins abgebildet ist.' in `merged.md` -- Directly stated. |
| 10 | Babcock simplified the game for the American market. | 6 | carried | 'Babcock vereinfachte das Spiel für den amerikanischen Markt' in `merged.md` -- Directly stated. |
| 11 | Babcock provided the tiles with, among other things, Roman numerals. | 6 | carried | 'und versah die Steine unter anderem mit römischen Ziffern' in `merged.md` -- Directly stated. |
| 12 | Babcock describes Mah-Jongg in the foreword to his Red Book as his own development based on the old Chinese game. | 8 | carried | 'Babcock bezeichnet Mah-Jongg im Vorwort zu seinem Red Book als eine eigene Entwicklung, basierend auf dem alten chinesischen Spiel' in `merged.md` -- Directly stated. |
| 13 | Babcock names the city Ningpo (today Ningbo) as the place of origin in one place. | 8 | carried | 'Als Entstehungsort nennt er an anderer Stelle die Stadt Ningpo (heute Ningbo)' in `merged.md` -- Directly stated. |
| 14 | Babcock names the province Fukien (today Fujian) as the place of origin in another place. | 8 | carried | 'oder die Provinz Fukien (heute Fujian)' in `merged.md` -- Directly stated. |
| 15 | It was claimed that the game already existed 4,000 years ago at the time of the Shang dynasty. | 10 | carried | 'Es wurde behauptet, es habe das Spiel schon vor 4.000 Jahren zur Zeit der Shang-Dynastie gegeben' in `merged.md` -- Directly stated. |
| 16 | It was claimed that Mah-Jongg was forbidden to common people for a long time and reserved only for the upper class. | 10 | carried | 'oder Mah-Jongg sei lange Zeit dem einfachen Volk verboten und nur der Oberschicht vorbehalten gewesen' in `merged.md` -- Directly stated. |
| 17 | Mah-Jongg actually originated in the second half of the 19th century. | 10 | carried | 'Tatsächlich entstand Mah-Jongg erst in der zweiten Hälfte des 19. Jahrhunderts.' in `merged.md` -- Directly stated. |
| 18 | The oldest surviving games date to around 1870. | 10 | carried | 'Die ältesten erhaltenen Spiele datieren um 1870' in `merged.md` -- Directly stated. |
| 19 | The oldest written references date from the year 1890. | 10 | carried | 'die ältesten schriftlichen Hinweise aus dem Jahr 1890' in `merged.md` -- Directly stated. |
| 20 | Mah-Jongg was originally a gambling game associated with tea houses and brothels. | 10 | carried | 'Ursprünglich war Mah-Jongg ein Glücksspiel, das mit Teehäusern und Bordellen in Verbindung stand' in `merged.md` -- Directly stated. |
| 21 | By the end of the 19th century Mah-Jongg had also become established in bourgeois households. | 10 | carried | 'gegen Ende des 19. Jahrhunderts hatte es sich jedoch auch in bürgerlichen Haushalten etabliert' in `merged.md` -- Directly stated. |
| 22 | Mah-Jongg spread from Shanghai to other parts of China. | 10 | carried | 'und sich von Shanghai aus in andere Teile Chinas verbreitet' in `merged.md` -- Directly stated. |
| 23 | The Mah-Jongg game spread quickly in China and Japan. | 10 | carried | 'Das Mah-Jongg-Spiel verbreitete sich rasch in China und Japan.' in `merged.md` -- Directly stated. |
| 24 | After Babcock made the game known in the USA, Mah-Jongg achieved worldwide popularity. | 10 | carried | 'Nachdem Babcock das Spiel in den USA bekanntgemacht hatte, erlangte Mah-Jongg weltweite Popularität' in `merged.md` -- Directly stated. |
| 25 | Factories were specifically founded to meet the demand for Mah-Jongg games. | 12 | carried | 'Es wurden eigens Fabriken gegründet, um die Nachfrage nach Mah-Jongg-Spielen zu befriedigen' in `merged.md` -- Directly stated. |
| 26 | There was a rumor circulating that imported games were infected with viruses. | 12 | carried | 'zumal das Gerücht umging, importierte Spiele wären mit Viren verseucht' in `merged.md` -- Directly stated. |
| 27 | The game was introduced in Germany by F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt. | 12 | carried | 'In Deutschland wurde das Spiel eingeführt durch F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt' in `merged.md` -- Directly stated. |
| 28 | The utility model protection number was 722354, dated 6 November 1919. | 12 | carried | '(Gebrauchsmusterschutz Nr. 722354 v. 6. November 1919)' in `merged.md` -- Directly stated. |
| 29 | Another Mah-Jongg manufacturer in Germany was the Hamburg Nordicus-Golconda Werke. | 12 | carried | 'Ein weiterer Mah-Jongg-Hersteller in Deutschland war die Hamburger Nordicus-Golconda Werke.' in `merged.md` -- Directly stated. |
| 30 | There were Mah-Jongg magazines. | 12 | carried | 'Es gab Mah-Jongg-Zeitschriften' in `merged.md` -- Directly stated. |
| 31 | Mah-Jongg tournaments were held in many American cities. | 12 | carried | 'in vielen amerikanischen Städten wurden Mah-Jongg-Turniere veranstaltet' in `merged.md` -- Directly stated. |
| 32 | Fred Astaire was among the prominent promoters of the American Mah-Jongg boom of the 1920s. | 12 | carried | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.' in `merged.md` -- Directly stated. |
| 33 | President Warren G. Harding was among the prominent promoters of the American Mah-Jongg boom of the 1920s. | 12 | carried | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.' in `merged.md` -- Directly stated. |
| 34 | First Lady Florence Harding was among the prominent promoters of the American Mah-Jongg boom of the 1920s. | 12 | carried | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.' in `merged.md` -- Directly stated. |
| 35 | The National Mah Jongg League was founded in New York in 1937. | 12 | carried | 'In New York wurde 1937 die National Mah Jongg League gegründet' in `merged.md` -- Directly stated. |
| 36 | The National Mah Jongg League further standardized the rules. | 12 | carried | 'die die Regeln weiter vereinheitlichte und damit die heute als American Mahjong bekannte Spielart maßgeblich prägte' in `merged.md` -- Directly stated. |
| 37 | The National Mah Jongg League significantly shaped the game style known today as American Mahjong. | 12 | carried | 'und damit die heute als American Mahjong bekannte Spielart maßgeblich prägte' in `merged.md` -- Directly stated. |
| 38 | Mah-Jongg disappeared a few years later as quickly as it had come, like a fashion. | 14 | carried | 'Doch bereits wenige Jahre später verschwand Mah-Jongg wie eine Mode und ebenso schnell, wie sie gekommen war.' in `merged.md` -- Directly stated. |
| 39 | The game is extremely popular in China and Japan. | 14 | carried | 'Das Spiel ist in China und Japan überaus populär' in `merged.md` -- Directly stated. |
| 40 | Worldwide participation in Mah-Jongg events has more than tripled within one year. | 14 | carried | 'Die weltweite Teilnahme an Mah-Jongg-Veranstaltungen hat sich innerhalb eines Jahres mehr als verdreifacht' in `merged.md` -- Directly stated. |
| 41 | Regular events take place in Berlin, Helsinki, London, Los Angeles, New York, Paris and Sydney. | 14 | carried | 'regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt' in `merged.md` -- Directly stated. |
| 42 | There are numerous introductory and learning videos about Mah-Jongg on YouTube. | 14 | carried | 'Auf YouTube existieren zahlreiche Einführungs- und Lernvideos' in `merged.md` -- Directly stated. |
| 43 | The amount of Mah-Jongg-related content on TikTok increased by around 70 percent within one year. | 14 | carried | 'auf TikTok nahm die Menge der Mah-Jongg-bezogenen Inhalte innerhalb eines Jahres um rund 70 Prozent zu' in `merged.md` -- Directly stated. |
| 44 | There is no evidence that the Rummy game developed from Mah-Jongg or vice versa. | 16 | carried | 'Es gibt jedoch keine Hinweise, dass sich das Rummy-Spiel aus dem Mah-Jongg entwickelt hätte oder umgekehrt.' in `merged.md` -- Directly stated. |
| 45 | In better games, the playing tiles are made from two parts. | 20 | carried | 'Die Spielsteine sind bei den besseren Spielen aus zwei Teilen gearbeitet' in `merged.md` -- Directly stated. |
| 46 | The images on the front sides are engraved and colored with chisels into a small block of bone, formerly ivory. | 20 | carried | 'die Bilder auf den Vorderseiten sind mit Sticheln in einen kleinen Block aus Bein – früher Elfenbein – eingraviert und koloriert' in `merged.md` -- Directly stated. |
| 47 | The backs of the tiles are made of bamboo. | 20 | carried | 'die Rückseiten sind aus Bambus' in `merged.md` -- Directly stated. |
| 48 | The two parts of the tiles are usually not simply glued but dovetailed. | 20 | carried | 'diese beiden Teile sind üblicherweise nicht einfach verklebt, sondern verzinkt' in `merged.md` -- Directly stated. |
| 49 | The tiles of cheaper games are made of printed wood or plastic. | 20 | carried | 'Die Steine preisgünstigerer Spiele sind aus bedrucktem Holz oder aus Kunststoff gefertigt.' in `merged.md` -- Directly stated. |
| 50 | There are also Mah-Jongg card games. | 20 | carried | 'Es gibt auch Mah-Jongg-Kartenspiele.' in `merged.md` -- Directly stated. |
| 51 | Luxury brands such as Hermès, Prada and Louis Vuitton offer their own versions of Mah-Jongg sets. | 20 | carried | 'bieten auch Luxusmarken wie Hermès, Prada und Louis Vuitton eigene Ausführungen an' in `merged.md` -- Directly stated. |
| 52 | A Mah-Jongg game consists of 136 or 144 playing tiles, which are called bricks. | 22 | carried | 'Ein Mah-Jongg-Spiel besteht aus 136 oder 144 Spielsteinen, die Ziegel genannt werden' in `merged.md` -- Directly stated. |
| 53 | Mah-Jongg is played in countless rule variants from Chinese Traditional to Jewish American. | 28 | carried | 'Mah-Jongg wird in unzähligen Regelvarianten von Chinese Traditional bis Jewish American gespielt.' in `merged.md` -- Directly stated. |
| 54 | The Hua Bao Rules correspond, apart from a few differences, to the rules of Joseph P. Babcock. | 28 | carried | 'welche bis auf wenige Unterschiede den Regeln von Joseph P. Babcock entsprechen' in `merged.md` -- Directly stated. |
| 55 | The Hua Bao Rules are the common style of play in Europe. | 28 | carried | 'Diese ist die in Europa gängige Spielweise.' in `merged.md` -- Directly stated. |
| 56 | In the standard variant, the game is played with 136 tiles. | 30 | carried | 'In der Standard-Variante wird mit 136 Steinen gespielt' in `merged.md` -- Directly stated. |
| 57 | In the standard variant, the eight bricks of the main suit are not used. | 30 | carried | 'die acht Ziegel der Hauptfarbe werden nicht verwendet' in `merged.md` -- Directly stated. |
| 58 | Before the start of a game, the four players stand at the four sides of a square table. | 36 | carried | 'stehen die vier Spieler an den vier Seiten eines quadratischen Tisches' in `merged.md` -- Directly stated. |
| 59 | The oldest player shuffles the four seat tiles face down and stacks them on top of each other. | 36 | carried | 'Der älteste Spieler mischt verdeckt die vier Platzsteine und stapelt sie aufeinander.' in `merged.md` -- Directly stated. |
| 60 | The oldest player then throws two dice and counts the sum of the pips counterclockwise, starting with himself. | 36 | carried | 'Sodann wirft er zwei Würfel und zählt die Augensumme gegen den Uhrzeigersinn ab, wobei er bei sich selbst zu zählen beginnt.' in `merged.md` -- Directly stated. |
| 61 | The player determined in this way takes the top seat tile, the next player the second, and so on. | 36 | carried | 'Der solcherart bestimmte Spieler nimmt den obersten Platzstein, der nächste den zweiten usw.' in `merged.md` -- Directly stated. |
| 62 | The playing surface of the table is interpreted as a map of the sky. | 38 | carried | 'Die Spielfläche des Tisches wird als Himmelskarte interpretiert.' in `merged.md` -- Directly stated. |
| 63 | The player who receives the East Wind seat tile becomes the game leader in the first game and remains in his seat. | 38 | carried | 'Der Spieler, der den Platzstein Ostwind erhält, wird Spielleiter im ersten Spiel und bleibt an seinem Platz' in `merged.md` -- Directly stated. |
| 64 | West Wind sits opposite East Wind. | 38 | carried | 'Westwind setzt sich gegenüber' in `merged.md` -- Directly stated. |
| 65 | South Wind sits to the right of East Wind. | 38 | carried | 'Südwind zur Rechten (!) von Ostwind' in `merged.md` -- Directly stated. |
| 66 | North Wind sits to the left of East Wind. | 38 | carried | 'und Nordwind zur Linken' in `merged.md` -- Directly stated. |
| 67 | The tiles are shuffled face down on the table. | 42 | carried | 'Die Ziegel werden verdeckt auf dem Tisch gemischt.' in `merged.md` -- Directly stated. |
| 68 | Each of the four players builds one side of the wall by taking 34 of the tiles face down and arranging them into a wall 17 tiles long and two tiles high. | 42 | carried | 'indem er 34 der Ziegel verdeckt nimmt und zu einer 17 Ziegel langen und zwei Ziegel hohen Mauer anordnet' in `merged.md` -- Directly stated. |
| 69 | If played with flower and season tiles, each player takes 36 tiles and the width of the wall is 18 stacks. | 42 | carried | 'so nimmt jeder Spieler 36 Ziegel und die Breite der Mauer beträgt 18 Stapel' in `merged.md` -- Directly stated. |
| 70 | The four wall pieces are pushed together so that they touch at the corners and form a square. | 42 | carried | 'Die vier Mauerstücke werden zusammengeschoben, so dass sie sich an den Ecken berühren und ein Quadrat bilden.' in `merged.md` -- Directly stated. |
| 71 | Outside Asian countries this is sometimes called the Chinese Wall. | 42 | carried | 'Außerhalb der asiatischen Länder wird dies manchmal Chinesische Mauer genannt.' in `merged.md` -- Directly stated. |
| 72 | East Wind then throws the two dice and counts the sum of the pips counterclockwise among the players, starting with himself. | 44 | carried | 'Nun wirft Ostwind die zwei Würfel und zählt wie vorhin, bei sich selbst beginnend, die Augensumme gegen den Uhrzeigersinn an den Spielern ab.' in `merged.md` -- Directly stated. |
| 73 | The player determined in this way also throws both dice and adds together the sums of both throws. | 44 | carried | 'Der so bestimmte Spieler wirft ebenfalls beide Würfel und zählt die Augensumme beider Würfe zusammen.' in `merged.md` -- Directly stated. |
| 74 | East Wind counts, starting at the right end of the wall in front of him and going clockwise, a number of tile stacks corresponding to the total sum. | 44 | carried | 'Ostwind zählt am rechten Ende der vor ihm befindlichen Mauer beginnend im Uhrzeigersinn der Gesamtsumme entsprechend Ziegelstapel ab.' in `merged.md` -- Directly stated. |
| 75 | He may continue the count with tiles from his left neighbor's wall if necessary. | 44 | carried | 'Eventuell setzt er die Zählung mit Ziegeln aus der Mauer seines linken Nachbarn fort.' in `merged.md` -- Directly stated. |
| 76 | He removes the stack determined in this way, which is called breaking the wall, and places it on the stack to the right of the resulting gap. | 44 | carried | 'Den so bestimmten Stapel nimmt er heraus (Mauerdurchbruch) und stellt ihn auf den Stapel rechts neben der entstandenen Lücke.' in `merged.md` -- Directly stated. |
| 77 | The removed tiles are called loose tiles and mark the dead end of the wall. | 46 | carried | 'Die herausgenommenen Steine heißen lose Ziegel und markieren das tote Ende der Mauer' in `merged.md` -- Directly stated. |
| 78 | The end to the left of the gap is the living end of the wall. | 46 | carried | 'das Ende links der Lücke ist das lebende Ende der Mauer' in `merged.md` -- Directly stated. |
| 79 | Tiles are regularly drawn from the living end of the wall. | 46 | carried | 'Gezogen werden die Steine regulär vom lebenden Ende der Mauer.' in `merged.md` -- Directly stated. |
| 80 | From the dead end, only replacement tiles are taken, starting with the two loose tiles. | 46 | carried | 'Vom toten Ende werden dagegen nur Ersatzziegel (siehe unten) genommen, beginnend mit den beiden losen Ziegeln.' in `merged.md` -- Directly stated. |
| 81 | The players take, three times in a row counterclockwise, two stacks of two tiles each from the living end of the wall, with East Wind serving himself first. | 46 | carried | 'Die Spieler nehmen dreimal reihum gegen den Uhrzeigersinn jeder zwei Stapel zu zwei Ziegel vom lebenden Ende der Mauer, wobei sich Ostwind als erster bedient.' in `merged.md` -- Directly stated. |
| 82 | Finally each player takes one more, a thirteenth tile, and East Wind additionally takes a fourteenth tile. | 46 | carried | 'Zuletzt nimmt jeder Spieler noch einen weiteren, dreizehnten, und Ostwind außerdem einen vierzehnten Ziegel.' in `merged.md` -- Directly stated. |
| 83 | Tiles are drawn from the wall or taken after another player's discard. | 50 | carried | 'Steine werden von der Mauer gezogen oder nach Abwurf eines anderen Spielers aufgenommen.' in `merged.md` -- Directly stated. |
| 84 | If a player has formed a complete hand consisting of four sets and finally one pair, he may call "Mah-Jongg" and end the game. | 50 | carried | 'Hat ein Spieler ein vollständiges Spielbild bestehend aus vier Figuren und schließlich einem Paar gebildet, so darf er „Mah-Jongg“ rufen und das Spiel beenden.' in `merged.md` -- Directly stated. |
| 85 | The four sets can optionally be triplets, quadruplets, or sequences. | 50 | carried | 'Die vier Figuren können wahlweise Drillinge, Vierlinge oder Folgen sein.' in `merged.md` -- Directly stated. |
| 86 | A pair consists of two identical tiles, for example two Bamboo-Five tiles or two green dragons. | 56 | carried | 'Ein Paar besteht aus zwei gleichen Steinen, z. B. zweimal Bambus-Fünf oder zwei grüne Drachen etc.' in `merged.md` -- Directly stated. |
| 87 | To call Mah-Jongg, a complete hand is required which must contain exactly one pair, the final pair. | 58 | carried | 'Um Mah-Jongg rufen zu können, ist ein vollständiges Spielbild nötig, in diesem muss genau ein Paar, das Schlusspaar (將, jiàng, manchmal 眼, yǎn), enthalten sein.' in `merged.md` -- Directly stated. |
| 88 | A discarded tile may only be claimed to complete a pair if Mah-Jongg is called at the same time. | 58 | carried | 'Zur Vervollständigung eines Paares darf ein abgelegter Stein nur aufgerufen werden, wenn gleichzeitig Mah-Jongg gerufen wird.' in `merged.md` -- Directly stated. |
| 89 | A Pong consists of three identical tiles. | 62 | carried | 'Ein Pong (碰, pèng) besteht aus drei gleichen Steinen.' in `merged.md` -- Directly stated. |
| 90 | If a Pong is formed exclusively from tiles of the original hand or tiles drawn from the wall, it is a concealed Pong that does not need to be declared. | 62 | carried | 'Wird ein Pong ausschließlich aus Ziegeln der ursprünglichen Hand oder von der Mauer gezogenen Ziegeln gebildet, so handelt es sich um einen verdeckten Pong, der nicht gemeldet werden muss.' in `merged.md` -- Directly stated. |
| 91 | If a concealed Pong is nevertheless revealed, it should be marked as actually concealed by turning one of the tiles over. | 62 | carried | 'Wird er dennoch aufgedeckt, so sollte er durch ein Umdrehen eines der Steine als eigentlich verdeckt markiert werden.' in `merged.md` -- Directly stated. |
| 92 | If a player has a pair and the third tile is discarded by any other player, the player may claim that tile with the call "Pong." | 64 | carried | 'Besitzt ein Spieler ein Paar und wird der dritte Stein von einem beliebigen anderen Spieler abgelegt, so darf der Spieler diesen Stein mit dem Ruf „Pong“ aufrufen.' in `merged.md` -- Directly stated. |
| 93 | He places his pair and the claimed tile openly on the table and has an open Pong. | 64 | carried | 'Er legt sein Paar und den aufgerufenen Ziegel offen vor sich auf den Tisch und besitzt einen offenen Pong.' in `merged.md` -- Directly stated. |
| 94 | In the 1970s and 1980s the term Pon was often used in German-speaking regions instead of Pong. | 66 | carried | 'In den 1970er und 1980er Jahren wurde im deutschsprachigen Raum statt Pong oftmals der Begriff Pon verwendet.' in `merged.md` -- Directly stated. |
| 95 | In Ursula Eschenbach's instructional book published in 1982, the terms Pon, Kan and Chii are used throughout. | 66 | carried | 'Auch in dem 1982 erschienenen Anleitungsbuch von Ursula Eschenbach ist durchgehend von Pon, Kan und Chii die Rede.' in `merged.md` -- Directly stated. |
| 96 | The terms Pon, Kan or Chii come from the Japanese game variant Riichi Mahjong. | 66 | carried | 'Die Begriffe Pon (jap. ポン, 碰 pon), Kan (カン, 槓, 杠 kan) oder Chii (チー, 吃 chī) stammen aus der japanischen Spielart des Riichi Mahjong' in `merged.md` -- Directly stated. |
| 97 | A Kong consists of four identical tiles. | 70 | carried | 'Ein Kong (槓 / 杠, gàng) besteht aus vier gleichen Steinen.' in `merged.md` -- Directly stated. |
| 98 | If a Kong is formed exclusively from tiles of the original hand and tiles drawn from the wall, the player should declare a concealed Kong. | 72 | carried | 'Wird ein Kong ausschließlich aus Steinen der ursprünglichen Hand und von der Mauer gezogenen Ziegeln gebildet, so sollte der Spieler einen verdeckten Kong melden.' in `merged.md` -- Directly stated. |
| 99 | If the player does not declare the concealed Kong, he cannot draw a replacement tile from the wall, which is necessary for a Kong to achieve a complete hand. | 72 | carried | 'Tut er dies nicht, so kann er keinen Ersatzziegel aus der Mauer ziehen, der bei Kongs notwendig ist, um ein komplettes Spielbild zu erreichen.' in `merged.md` -- Directly stated. |
| 100 | If the game ends before the player declares the quadruplet, the concealed Kong is scored as a concealed Pong. | 72 | carried | 'Wird das Spiel beendet, bevor der Spieler den Vierling meldet, so wird der verdeckte Kong als verdeckter Pong gewertet.' in `merged.md` -- Directly stated. |
| 101 | A concealed Kong does not need to be declared immediately, but can be laid out later when the player is again at his turn. | 74 | carried | 'Ein verdeckter Kong muss nicht sofort gemeldet werden, sondern kann auch später herausgelegt werden, wenn der Spieler erneut am Zug ist.' in `merged.md` -- Directly stated. |
| 102 | When declaring a concealed Kong, the four tiles are laid out face up and the two outer tiles are placed face down to indicate it is a concealed Kong. | 76 | carried | 'Bei der Meldung werden die vier Steine offen ausgelegt und zum Zeichen, dass es sich um einen verdeckten (auch: „halbverdeckten“, oder „aus der Hand gemeldeten“) Kong handelt, werden die beiden äußeren Steine mit der Rückseite nach oben gelegt.' in `merged.md` -- Text states tiles laid open (face up) and the two outer tiles placed back side up (face down), matching the claim. |
| 103 | If a player holds three identical tiles in hand, that is a concealed Pong, and if another player discards the fourth tile, he may claim it with the call "Kong" and obtain an open Kong. | 78 | carried | 'Hält ein Spieler drei gleiche Steine in der Hand – also einen verdeckten Pong – so darf er, wenn ein Spieler den vierten Stein ablegt, diesen Ziegel mit dem Ruf „Kong“ für sich beanspruchen und erhält so einen offenen Kong.' in `merged.md` -- Directly stated. |
| 104 | If a player has already declared an open Pong and the missing fourth tile is discarded by another player, that tile cannot be claimed to complete the Kong. | 80 | carried | 'Hat ein Spieler bereits einen offenen Pong gemeldet und wird der fehlende vierte Stein von einem anderen Spieler abgelegt, so kann dieser Ziegel nicht zur Komplettierung des Kongs aufgerufen werden.' in `merged.md` -- Directly stated. |
| 105 | If a player has already declared a Pong and draws the missing fourth tile from the wall, he may add it to the Pong and thereby has an open Kong. | 82 (unverified) | carried | 'Hat ein Spieler bereits einen Pong gemeldet und zieht er den fehlenden vierten Stein von der Mauer, so darf er ihn an den Pong anlegen und besitzt damit einen offenen Kong.' in `merged.md` -- Directly stated. |
| 106 | The tile drawn from the wall can be claimed by another player if he can call "Mah-Jongg" with it. | 82 | carried | 'kann ein anderer Spieler diesen vierten Stein für sich fordern, wenn er damit „Mah-Jongg“ rufen kann' in `merged.md` -- Directly stated. |
| 107 | As soon as a player declares an open or concealed Kong, he must draw a replacement tile from the dead end of the wall. | 84 | carried | 'Sobald ein Spieler einen offenen oder verdeckten Kong meldet, muss er einen Ersatzziegel vom toten Ende der Mauer ziehen.' in `merged.md` -- Directly stated. |
| 108 | A Chow is a sequence of exactly three consecutive tiles of a basic suit. | 88 | carried | 'Ein Chow (吃, chī, manchmal 上, shàng) ist eine Sequenz aus genau drei aufeinanderfolgenden Steinen einer Grundfarbe' in `merged.md` -- Directly stated. |
| 109 | Sequences of more than three tiles are not allowed. | 88 | carried | 'Sequenzen aus mehr als drei Steinen sind nicht gestattet.' in `merged.md` -- Directly stated. |
| 110 | A Chow made of trump-suit tiles is not possible. | 90 | carried | 'Ein Chow aus Steinen der Trumpffarbe ist nicht möglich.' in `merged.md` -- Directly stated. |
| 111 | A discarded tile can be claimed by a player with "Chow" if the player sits immediately to the right of the player who discarded the tile. | 92 | carried | 'Ein abgelegter Stein kann von einem Spieler mit „Chow“ aufgerufen werden, wenn der Spieler unmittelbar zur Rechten desjenigen Spielers sitzt, der den betreffenden Stein abgelegt hat.' in `merged.md` -- Directly stated. |
| 112 | The claiming player then lays the resulting sequence face up. | 92 | carried | 'Der aufrufende Spieler legt dann die damit gebildete Folge offen.' in `merged.md` -- Directly states the calling player lays the formed sequence face up. |
| 113 | Another player can only claim a discarded tile for a sequence if he calls Mah-Jongg at the same time. | 94 | carried | 'Ein anderer Spieler kann nur dann einen abgelegten Stein für eine Folge aufrufen, wenn er gleichzeitig Mah-Jongg ruft.' in `merged.md` -- Matches the claim exactly. |
| 114 | Sequences formed from tiles of the original hand or from drawn tiles can remain concealed until the end of the game. | 96 | carried | 'Folgen, die aus Steinen der ursprünglichen Hand bzw. aus gezogenen Steinen gebildet werden, können bis zum Spielende verdeckt bleiben.' in `merged.md` -- Directly states this rule for sequences. |
| 115 | Mah-Jongg is played counterclockwise. | 100 | carried | 'Mah-Jongg wird gegen den Uhrzeigersinn gespielt.' in `merged.md` -- States the game is played counterclockwise. |
| 116 | After East Wind has taken his 14 tiles, he begins the game by discarding a tile face up in the middle of the table. | 100 | carried | 'Nachdem sich Ostwind seine 14 Ziegel genommen hat, beginnt er das Spiel, indem er nach einer eventuellen Meldung einen Stein offen in der Mitte des Tisches ablegt' in `merged.md` -- States East Wind takes 14 tiles and begins by discarding a tile face up in the middle. |
| 117 | East Wind states the name of the discarded tile. | 100 | carried | 'dabei nennt er dessen Namen' in `merged.md` -- States he names the discarded tile. |
| 118 | If no player claims the discarded tile, the right neighbor draws a tile from the living end of the wall. | 102 | carried | 'Wenn kein Spieler den abgelegten Stein aufruft, so zieht der rechte Nachbar einen Stein vom lebenden Ende der Mauer' in `merged.md` -- Matches the claim exactly. |
| 119 | Once a tile is discarded, it is dead and remains face up in the middle of the table. | 104 | carried | 'Wird ein Stein abgelegt, so ist er tot, er bleibt offen in der Mitte des Tisches liegen' in `merged.md` -- States discarded tiles are dead and remain face up in the middle of the table. |
| 120 | The next player can play a Chow with the discarded tile, and that player and all other players can claim a Pong or a Kong. | 104 | carried | 'und der nächste Spieler kann einen Chow spielen, sowie jener und alle weiteren Spieler einen Pong oder einen Kong.' in `merged.md` -- States the next player can play a Chow and others can claim Pong or Kong. |
| 121 | After that, the tile is no longer available or claimable for the game. | 104 | carried | 'Danach ist der Stein nicht mehr für das Spiel verfügbar beziehungsweise aufnehmbar.' in `merged.md` -- Directly matches the claim. |
| 122 | If a tile is claimed by a player, that player takes the discarded tile and must lay out the relevant set face up. | 106 | carried | 'Wird ein Stein von einem Spieler aufgerufen, so nimmt der Spieler den abgelegten Stein und muss die betreffende Figur offen auflegen.' in `merged.md` -- Matches the claim closely. |
| 123 | After claiming, the player discards a tile, and the game continues with that player. | 106 | carried | 'Danach wirft er einen Stein ab, und das Spiel wird mit diesem Spieler fortgesetzt.' in `merged.md` -- Matches the claim exactly. |
| 124 | If South Wind discards a tile that is claimed by North Wind, West Wind is skipped. | 106 | carried | 'Legt beispielsweise Südwind einen Stein ab, der von Nordwind gerufen wird, so wird Westwind übersprungen.' in `merged.md` -- Matches the specific example given in the claim. |
| 125 | If a tile is called by several players, a player who needs the tile for a Mah-Jongg call has priority over a Kong or Pong call. | 108 | carried | 'Benötigt ein Spieler den Stein für einen Mah-Jongg-Ruf, so hat er Vorrang gegenüber einem Kong- oder Pong-Ruf' in `merged.md` -- Directly states Mah-Jongg call priority over Kong or Pong. |
| 126 | A Kong or Pong call has priority over a Chow call. | 108 | carried | 'und diese wiederum haben Vorrang vor einem Chow' in `merged.md` -- States Kong/Pong calls have priority over Chow. |
| 127 | If the game is not scored, the tiles are shuffled again and the game is repeated with unchanged roles. | 112 | carried | 'Im letzteren Fall wird das Spiel nicht gewertet, die Steine werden erneut gemischt und das Spiel mit unveränderten Rollen wiederholt.' in `merged.md` -- Matches the claim exactly. |
| 128 | Concealed combinations count double. | 124 | carried | 'Verdeckte Kombinationen zählen das Doppelte.' in `merged.md` -- States concealed combinations count double. |
| 129 | A Kong counts four times as much as the corresponding Pong. | 128 | carried | 'Ein Kong zählt viermal so viel wie der entsprechende Pong.' in `merged.md` -- Matches the claim exactly. |

### `merged.md` -- 142 claim(s): 0 invented, 1 contradicted, 0 supported in part, 141 supported

Each claim below was read against `source_a.md`, `source_b.md` and `source_c.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 29 | A rumor circulated that imported games were infested with vermin. | contradicted | `source_c.md` | 'zumal das Gerücht umging, importierte Spiele wären mit Viren verseucht' in `source_c.md` -- Source says the rumor was about games infested with viruses (Viren), not vermin. |
| 1 | Mah-Jongg is a Chinese game for four people. | supported | `source_c.md` | 'ist ein chinesisches Spiel für vier Personen' in `source_c.md` -- Directly states the game is Chinese and for four people. |
| 2 | Joseph Park Babcock lived from 1893 to 1949. | supported | `source_c.md` | 'Joseph Park Babcock (1893–1949)' in `source_c.md` -- Dates match exactly. |
| 3 | Joseph Park Babcock was an American traveler in the Republic of China. | supported | `source_c.md` | 'ein amerikanischer Reisender in der Republik China' in `source_c.md` -- Matches claim directly. |
| 4 | Joseph Park Babcock wrote a rulebook in the 1920s based on different variants he had encountered. | supported | `source_c.md` | 'verfasste in den 1920er Jahren ein Regelwerk basierend auf unterschiedlichen Varianten, die er kennengelernt hatte' in `source_c.md` -- Matches claim directly. |
| 5 | Joseph Park Babcock brought the game to the USA. | supported | `source_c.md` | 'brachte das Spiel in die USA' in `source_c.md` -- Direct statement. |
| 6 | Babcock gave the game the name MAH-JONGG in that spelling. | supported | `source_c.md` | 'Babcock gab ihm den Namen MAH-JONGG (in dieser Schreibweise)' in `source_c.md` -- Direct statement. |
| 7 | Babcock had the name MAH-JONGG registered as a trademark. | supported | `source_c.md` | 'den er als Marke eintragen ließ' in `source_c.md` -- Direct statement. |
| 8 | This spelling was varied in many ways in order not to violate the trademark protection. | supported | `source_c.md` | 'Um den Markenschutz nicht zu verletzen, wurde diese Schreibung vielfältig variiert.' in `source_c.md` -- Direct statement. |
| 9 | The name used in the West refers to a sparrow depicted on the Bamboo-One playing tile. | supported | `source_c.md` | 'Dieser im Westen gebräuchliche Name bezeichnet einen Sperling, der auf dem Spielstein Bambus-Eins abgebildet ist.' in `source_c.md` -- Direct statement. |
| 10 | Babcock simplified the game for the American market. | supported | `source_c.md` | 'Babcock vereinfachte das Spiel für den amerikanischen Markt' in `source_c.md` -- Direct statement. |
| 11 | Babcock provided the tiles with, among other things, Roman numerals. | supported | `source_c.md` | 'versah die Steine unter anderem mit römischen Ziffern' in `source_c.md` -- Direct statement. |
| 12 | This additionally favored the spread of the game in the United States. | supported | `source_c.md` | 'was die Verbreitung des Spiels in den Vereinigten Staaten zusätzlich begünstigte' in `source_c.md` -- Direct statement. |
| 13 | Babcock describes Mah-Jongg in the foreword to his Red Book as his own development based on the old Chinese game. | supported | `source_c.md` | 'Babcock bezeichnet Mah-Jongg im Vorwort zu seinem Red Book als eine eigene Entwicklung, basierend auf dem alten chinesischen Spiel' in `source_c.md` -- Direct statement. |
| 14 | The old Chinese game's origin was said by Babcock to be centuries old. | supported | `source_c.md` | 'das seinerseits – zumindest sein Ursprung – Jahrhunderte alt sei' in `source_c.md` -- Direct statement about centuries-old origin. |
| 15 | Babcock wrote "The Chinese game itself was a gradual development of centuries of play in China". | supported | `source_c.md` | 'The Chinese game itself was a gradual development of centuries of play in China' in `source_c.md` -- Exact quoted phrase matches claim. |
| 16 | Babcock names the city of Ningpo (today Ningbo) as a possible place of origin elsewhere. | supported | `source_c.md` | 'Als Entstehungsort nennt er an anderer Stelle die Stadt Ningpo (heute Ningbo) oder die Provinz Fukien (heute Fujian).' in `source_c.md` -- Direct statement. |
| 17 | Babcock names the province of Fukien (today Fujian) as a possible place of origin elsewhere. | supported | `source_c.md` | 'Als Entstehungsort nennt er an anderer Stelle die Stadt Ningpo (heute Ningbo) oder die Provinz Fukien (heute Fujian).' in `source_c.md` -- Direct statement. |
| 18 | It has been claimed that the game already existed 4,000 years ago at the time of the Shang dynasty. | supported | `source_c.md` | 'Es wurde behauptet, es habe das Spiel schon vor 4.000 Jahren zur Zeit der Shang-Dynastie gegeben' in `source_c.md` -- Direct statement. |
| 19 | It has been claimed that Mah-Jongg was forbidden to common people for a long time and reserved only for the upper class. | supported | `source_c.md` | 'oder Mah-Jongg sei lange Zeit dem einfachen Volk verboten und nur der Oberschicht vorbehalten gewesen' in `source_c.md` -- Direct statement. |
| 20 | Mah-Jongg actually originated in the second half of the 19th century. | supported | `source_c.md` | 'Tatsächlich entstand Mah-Jongg erst in der zweiten Hälfte des 19. Jahrhunderts.' in `source_c.md` -- Direct statement. |
| 21 | The oldest surviving sets date from around 1870. | supported | `source_c.md` | 'Die ältesten erhaltenen Spiele datieren um 1870' in `source_c.md` -- Direct statement. |
| 22 | The oldest written references date from the year 1890. | supported | `source_c.md` | 'die ältesten schriftlichen Hinweise aus dem Jahr 1890' in `source_c.md` -- Direct statement. |
| 23 | Mah-Jongg was originally a gambling game associated with teahouses and brothels. | supported | `source_c.md` | 'Ursprünglich war Mah-Jongg ein Glücksspiel, das mit Teehäusern und Bordellen in Verbindung stand' in `source_c.md` -- Direct statement. |
| 24 | By the end of the 19th century Mah-Jongg had also established itself in bourgeois households. | supported | `source_c.md` | 'gegen Ende des 19. Jahrhunderts hatte es sich jedoch auch in bürgerlichen Haushalten etabliert' in `source_c.md` -- Direct statement. |
| 25 | Mah-Jongg had spread from Shanghai to other parts of China. | supported | `source_c.md` | 'und sich von Shanghai aus in andere Teile Chinas verbreitet' in `source_c.md` -- Direct statement. |
| 26 | The Mah-Jongg game spread rapidly in China and Japan. | supported | `source_c.md` | 'Das Mah-Jongg-Spiel verbreitete sich rasch in China und Japan.' in `source_c.md` -- Direct statement. |
| 27 | After Babcock made the game known in the USA, Mah-Jongg gained worldwide popularity. | supported | `source_c.md` | 'Nachdem Babcock das Spiel in den USA bekanntgemacht hatte, erlangte Mah-Jongg weltweite Popularität' in `source_c.md` -- Direct statement. |
| 28 | Factories were specifically founded to meet demand for Mah-Jongg games. | supported | `source_c.md` | 'Es wurden eigens Fabriken gegründet, um die Nachfrage nach Mah-Jongg-Spielen zu befriedigen' in `source_c.md` -- Direct statement. |
| 30 | The game was introduced in Germany by F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt. | supported | `source_c.md` | 'In Deutschland wurde das Spiel eingeführt durch F. Ad. Richter & Cie, Baukastenfabrik, Rudolstadt' in `source_c.md` -- Direct statement. |
| 31 | The utility model protection was Nr. 722354 dated 6 November 1919. | supported | `source_c.md` | '(Gebrauchsmusterschutz Nr. 722354 v. 6. November 1919)' in `source_c.md` -- Direct statement. |
| 32 | Another Mah-Jongg manufacturer in Germany was the Hamburg Nordicus-Golconda Werke. | supported | `source_c.md` | 'Ein weiterer Mah-Jongg-Hersteller in Deutschland war die Hamburger Nordicus-Golconda Werke.' in `source_c.md` -- Direct statement. |
| 33 | There were Mah-Jongg magazines. | supported | `source_c.md` | 'Es gab Mah-Jongg-Zeitschriften' in `source_c.md` -- Direct statement. |
| 34 | Mah-Jongg tournaments were held in many American cities. | supported | `source_c.md` | 'in vielen amerikanischen Städten wurden Mah-Jongg-Turniere veranstaltet' in `source_c.md` -- Direct statement. |
| 35 | Fred Astaire was among the prominent promoters of the American Mah-Jongg boom of the 1920s. | supported | `source_c.md` | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.' in `source_c.md` -- Fred Astaire named among promoters. |
| 36 | President Warren G. Harding was among the prominent promoters of the American Mah-Jongg boom of the 1920s. | supported | `source_c.md` | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.' in `source_c.md` -- Warren G. Harding named among promoters. |
| 37 | First Lady Florence Harding was among the prominent promoters of the American Mah-Jongg boom of the 1920s. | supported | `source_c.md` | 'Zu den prominenten Förderern des amerikanischen Mah-Jongg-Booms der 1920er-Jahre zählten Fred Astaire sowie Präsident Warren G. Harding und First Lady Florence Harding.' in `source_c.md` -- Florence Harding named among promoters. |
| 38 | The National Mah Jongg League was founded in New York in 1937. | supported | `source_c.md` | 'In New York wurde 1937 die National Mah Jongg League gegründet' in `source_c.md` -- Direct statement. |
| 39 | The National Mah Jongg League further standardized the rules. | supported | `source_c.md` | 'die die Regeln weiter vereinheitlichte' in `source_c.md` -- Direct statement. |
| 40 | This standardization significantly shaped what is known today as American Mahjong. | supported | `source_c.md` | 'und damit die heute als American Mahjong bekannte Spielart maßgeblich prägte' in `source_c.md` -- Direct statement. |
| 41 | The worldwide participation in Mah-Jongg events has more than tripled within one year. | supported | `source_c.md` | 'Die weltweite Teilnahme an Mah-Jongg-Veranstaltungen hat sich innerhalb eines Jahres mehr als verdreifacht' in `source_c.md` -- Direct statement. |
| 42 | Regular Mah-Jongg events take place in Berlin. | supported | `source_c.md` | 'regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt' in `source_c.md` -- Berlin listed among cities. |
| 43 | Regular Mah-Jongg events take place in Helsinki. | supported | `source_c.md` | 'regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt' in `source_c.md` -- Helsinki listed among cities. |
| 44 | Regular Mah-Jongg events take place in London. | supported | `source_c.md` | 'regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt' in `source_c.md` -- London listed among cities. |
| 45 | Regular Mah-Jongg events take place in Los Angeles. | supported | `source_c.md` | 'regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt' in `source_c.md` -- Los Angeles listed among cities. |
| 46 | Regular Mah-Jongg events take place in New York. | supported | `source_c.md` | 'regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt' in `source_c.md` -- New York listed among cities. |
| 47 | Regular Mah-Jongg events take place in Paris. | supported | `source_c.md` | 'regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt' in `source_c.md` -- Paris listed among cities. |
| 48 | Regular Mah-Jongg events take place in Sydney. | supported | `source_c.md` | 'regelmäßige Veranstaltungen finden unter anderem in Berlin, Helsinki, London, Los Angeles, New York, Paris und Sydney statt' in `source_c.md` -- Sydney listed among cities. |
| 49 | Numerous introductory and tutorial videos exist on YouTube. | supported | `source_c.md` | 'Auf YouTube existieren zahlreiche Einführungs- und Lernvideos' in `source_c.md` -- Direct statement. |
| 50 | On TikTok, the amount of Mah-Jongg-related content increased by around 70 percent within one year. | supported | `source_c.md` | 'auf TikTok nahm die Menge der Mah-Jongg-bezogenen Inhalte innerhalb eines Jahres um rund 70 Prozent zu' in `source_c.md` -- Direct statement. |
| 51 | Mah-Jongg can be understood as a variant of the card game Rummy in terms of rules. | supported | `source_c.md` | 'Von den Regeln her kann Mah-Jongg als eine Variante des Kartenspiels Rummy verstanden werden' in `source_c.md` -- Direct statement. |
| 52 | There is also a variant of Rummy played with playing stones. | supported | `source_c.md` | 'von dem es ebenfalls eine Variante mit Spielsteinen gibt' in `source_c.md` -- Direct statement. |
| 53 | Mah-Jongg is then played with "Chinese" playing cards instead of a French deck. | supported | `source_c.md` | 'Dann wird Mah-Jongg mit „chinesischen“ Spielkarten statt mit französischem Blatt gespielt.' in `source_c.md` -- Direct statement. |
| 54 | There are no indications that the Rummy game developed from Mah-Jongg or vice versa. | supported | `source_c.md` | 'Es gibt jedoch keine Hinweise, dass sich das Rummy-Spiel aus dem Mah-Jongg entwickelt hätte oder umgekehrt.' in `source_c.md` -- Direct statement. |
| 55 | The stones of better games have their front faces engraved and colored with burins into a small block of bone, formerly ivory. | supported | `source_c.md` | 'die Bilder auf den Vorderseiten sind mit Sticheln in einen kleinen Block aus Bein – früher Elfenbein – eingraviert und koloriert' in `source_c.md` -- Direct statement. |
| 56 | The backs of the tiles are made of bamboo. | supported | `source_c.md` | 'die Rückseiten sind aus Bambus' in `source_c.md` -- Direct statement. |
| 57 | These two parts are usually not simply glued but dovetailed. | supported | `source_c.md` | 'diese beiden Teile sind üblicherweise nicht einfach verklebt, sondern verzinkt' in `source_c.md` -- Direct statement. |
| 58 | The stones of cheaper games are made from printed wood or plastic. | supported | `source_c.md` | 'Die Steine preisgünstigerer Spiele sind aus bedrucktem Holz oder aus Kunststoff gefertigt.' in `source_c.md` -- Direct statement. |
| 59 | There are also Mah-Jongg card games. | supported | `source_c.md` | 'Es gibt auch Mah-Jongg-Kartenspiele.' in `source_c.md` -- Direct statement. |
| 60 | Luxury brands including Hermès offer their own versions of Mah-Jongg sets. | supported | `source_c.md` | 'bieten auch Luxusmarken wie Hermès, Prada und Louis Vuitton eigene Ausführungen an' in `source_c.md` -- Hermès named among luxury brands. |
| 61 | Luxury brands including Prada offer their own versions of Mah-Jongg sets. | supported | `source_c.md` | 'bieten auch Luxusmarken wie Hermès, Prada und Louis Vuitton eigene Ausführungen an' in `source_c.md` -- Prada named among luxury brands. |
| 62 | Luxury brands including Louis Vuitton offer their own versions of Mah-Jongg sets. | supported | `source_c.md` | 'bieten auch Luxusmarken wie Hermès, Prada und Louis Vuitton eigene Ausführungen an' in `source_c.md` -- Louis Vuitton named among luxury brands. |
| 63 | A Mah-Jongg game consists of 136 or 144 playing stones, which are called tiles (Ziegel). | supported | `source_c.md` | 'Ein Mah-Jongg-Spiel besteht aus 136 oder 144 Spielsteinen, die Ziegel genannt werden' in `source_c.md` -- Direct statement. |
| 64 | Mah-Jongg is played in countless rule variants from Chinese Traditional to Jewish American. | supported | `source_c.md` | 'Mah-Jongg wird in unzähligen Regelvarianten von Chinese Traditional bis Jewish American gespielt.' in `source_c.md` -- Direct statement. |
| 65 | The described Hua Bao Rules correspond, apart from a few differences, to the rules of Joseph P. Babcock. | supported | `source_c.md` | 'Die folgende Anleitung beschreibt die Hua Bao Rules, welche bis auf wenige Unterschiede den Regeln von Joseph P. Babcock entsprechen' in `source_c.md` -- Direct statement. |
| 66 | In the standard variant, the game is played with 136 tiles. | supported | `source_c.md` | 'In der Standard-Variante wird mit 136 Steinen gespielt' in `source_c.md` -- Direct statement. |
| 67 | The eight tiles of the main suit are not used in the standard variant. | supported | `source_c.md` | 'die acht Ziegel der Hauptfarbe werden nicht verwendet' in `source_c.md` -- Direct statement. |
| 68 | Before a game begins, the four players stand at the four sides of a square table. | supported | `source_c.md` | 'stehen die vier Spieler an den vier Seiten eines quadratischen Tisches' in `source_c.md` -- Direct statement. |
| 69 | The oldest player shuffles the four seat tiles face down and stacks them on top of each other. | supported | `source_c.md` | 'Der älteste Spieler mischt verdeckt die vier Platzsteine und stapelt sie aufeinander.' in `source_c.md` -- Direct statement. |
| 70 | He then throws two dice and counts the pip total counterclockwise, starting with himself. | supported | `source_c.md` | 'Sodann wirft er zwei Würfel und zählt die Augensumme gegen den Uhrzeigersinn ab, wobei er bei sich selbst zu zählen beginnt.' in `source_c.md` -- Direct statement. |
| 71 | The player determined in this way takes the top seat tile, the next one takes the second, and so on. | supported | `source_c.md` | 'Der solcherart bestimmte Spieler nimmt den obersten Platzstein, der nächste den zweiten usw.' in `source_c.md` -- Direct statement. |
| 72 | The playing surface of the table is interpreted as a sky map. | supported | `source_c.md` | 'Die Spielfläche des Tisches wird als Himmelskarte interpretiert.' in `source_c.md` -- Direct statement. |
| 73 | The player who receives the seat tile East Wind becomes the game leader in the first game and stays in his place. | supported | `source_c.md` | 'Der Spieler, der den Platzstein Ostwind erhält, wird Spielleiter im ersten Spiel und bleibt an seinem Platz' in `source_c.md` -- Direct statement. |
| 74 | West Wind sits opposite East Wind. | supported | `source_c.md` | 'Westwind setzt sich gegenüber' in `source_c.md` -- Direct statement. |
| 75 | South Wind sits to the right of East Wind. | supported | `source_c.md` | 'Südwind zur Rechten (!) von Ostwind' in `source_c.md` -- Direct statement. |
| 76 | North Wind sits to the left of East Wind. | supported | `source_c.md` | 'und Nordwind zur Linken' in `source_c.md` -- Direct statement. |
| 77 | The tiles are shuffled face down on the table. | supported | `source_c.md` | 'Die Ziegel werden verdeckt auf dem Tisch gemischt.' in `source_c.md` -- Direct statement. |
| 78 | Each of the four players builds one side of the wall by taking 34 of the tiles face down. | supported | `source_c.md` | 'indem er 34 der Ziegel verdeckt nimmt' in `source_c.md` -- Direct statement. |
| 79 | The wall is arranged 17 tiles long and two tiles high. | supported | `source_c.md` | 'und zu einer 17 Ziegel langen und zwei Ziegel hohen Mauer anordnet' in `source_c.md` -- Direct statement. |
| 80 | When playing with flower and season tiles, each player takes 36 tiles. | supported | `source_c.md` | 'Wird mit Blumen- und Jahreszeitenziegeln gespielt, so nimmt jeder Spieler 36 Ziegel' in `source_c.md` -- Direct statement. |
| 81 | When playing with flower and season tiles, the width of the wall is 18 stacks. | supported | `source_c.md` | 'und die Breite der Mauer beträgt 18 Stapel' in `source_c.md` -- Direct statement. |
| 82 | The four wall pieces are pushed together so that they touch at the corners and form a square. | supported | `source_c.md` | 'Die vier Mauerstücke werden zusammengeschoben, so dass sie sich an den Ecken berühren und ein Quadrat bilden.' in `source_c.md` -- Direct statement. |
| 83 | Outside Asian countries this is sometimes called the Chinese Wall. | supported | `source_c.md` | 'Außerhalb der asiatischen Länder wird dies manchmal Chinesische Mauer genannt.' in `source_c.md` -- Direct statement. |
| 84 | Each player takes two stacks of two tiles three times in a row counterclockwise from the living end of the wall, with East Wind serving first. | supported | `source_c.md` | 'Die Spieler nehmen dreimal reihum gegen den Uhrzeigersinn jeder zwei Stapel zu zwei Ziegel vom lebenden Ende der Mauer, wobei sich Ostwind als erster bedient.' in `source_c.md` -- Direct statement. |
| 85 | Each player finally takes one more, a thirteenth, tile. | supported | `source_c.md` | 'Zuletzt nimmt jeder Spieler noch einen weiteren, dreizehnten, und Ostwind außerdem einen vierzehnten Ziegel.' in `source_c.md` -- Direct statement. |
| 86 | East Wind additionally takes a fourteenth tile. | supported | `source_c.md` | 'und Ostwind außerdem einen vierzehnten Ziegel' in `source_c.md` -- Direct statement. |
| 87 | A pair consists of two identical tiles, for example two Bamboo-Five tiles or two green dragons. | supported | `source_c.md` | 'Ein Paar besteht aus zwei gleichen Steinen, z. B. zweimal Bambus-Fünf oder zwei grüne Drachen etc.' in `source_c.md` -- Direct statement. |
| 88 | A complete hand must contain exactly one pair, the final pair. | supported | `source_c.md` | 'Um Mah-Jongg rufen zu können, ist ein vollständiges Spielbild nötig, in diesem muss genau ein Paar, das Schlusspaar (將,  jiàng, manchmal 眼,  yǎn), enthalten sein.' in `source_c.md` -- Direct statement. |
| 89 | A discarded tile may only be called to complete a pair if Mah-Jongg is called at the same time. | supported | `source_c.md` | 'Zur Vervollständigung eines Paares darf ein abgelegter Stein nur aufgerufen werden, wenn gleichzeitig Mah-Jongg gerufen wird.' in `source_c.md` -- Direct statement. |
| 90 | A Pong consists of three identical tiles. | supported | `source_c.md` | 'Ein Pong (碰,  pèng) besteht aus drei gleichen Steinen.' in `source_c.md` -- Direct statement. |
| 91 | A Pong formed exclusively from tiles of the original hand or tiles drawn from the wall is a concealed Pong that does not need to be declared. | supported | `source_c.md` | 'Wird ein Pong ausschließlich aus Ziegeln der ursprünglichen Hand oder von der Mauer gezogenen Ziegeln gebildet, so handelt es sich um einen verdeckten Pong, der nicht gemeldet werden muss.' in `source_c.md` -- Direct statement. |
| 92 | In the 1970s and 1980s, the term Pon was often used in German-speaking regions instead of Pong. | supported | `source_c.md` | 'In den 1970er und 1980er Jahren wurde im deutschsprachigen Raum statt Pong oftmals der Begriff Pon verwendet.' in `source_c.md` -- Direct statement. |
| 93 | In the instruction book published in 1982 by Ursula Eschenbach, the terms Pon, Kan, and Chii are used throughout. | supported | `source_c.md` | 'Auch in dem 1982 erschienenen Anleitungsbuch von Ursula Eschenbach ist durchgehend von Pon, Kan und Chii die Rede.' in `source_c.md` -- Direct statement. |
| 94 | The terms Pon, Kan, and Chii originate from the Japanese variant of Riichi Mahjong. | supported | `source_c.md` | 'Die Begriffe Pon (jap. ポン, 碰 pon), Kan (カン, 槓, 杠 kan) oder Chii (チー, 吃 chī) stammen aus der japanischen Spielart des Riichi Mahjong (リーチ麻雀, 立直マージャン rīchi mājan).' in `source_c.md` -- Direct statement. |
| 95 | A Kong consists of four identical tiles. | supported | `source_c.md` | 'Ein Kong (槓 / 杠,  gàng) besteht aus vier gleichen Steinen.' in `source_c.md` -- Direct statement. |
| 96 | A Chow is a sequence of exactly three consecutive tiles of a basic suit. | supported | `source_c.md` | 'Ein Chow (吃,  chī, manchmal 上,  shàng) ist eine Sequenz aus genau drei aufeinanderfolgenden Steinen einer Grundfarbe' in `source_c.md` -- Direct statement. |
| 97 | Sequences of more than three tiles are not permitted. | supported | `source_c.md` | 'Sequenzen aus mehr als drei Steinen sind nicht gestattet.' in `source_c.md` -- Direct statement. |
| 98 | A Chow made from tiles of the trump suit is not possible. | supported | `source_c.md` | 'Ein Chow aus Steinen der Trumpffarbe ist nicht möglich.' in `source_c.md` -- Direct statement. |
| 99 | A discarded tile can be called with "Chow" by a player only if that player sits immediately to the right of the player who discarded the tile. | supported | `source_c.md` | 'Ein abgelegter Stein kann von einem Spieler mit „Chow“ aufgerufen werden, wenn der Spieler unmittelbar zur Rechten desjenigen Spielers sitzt, der den betreffenden Stein abgelegt hat.' in `source_c.md` -- Direct statement. |
| 100 | Mah-Jongg is played counterclockwise. | supported | `source_c.md` | 'Mah-Jongg wird gegen den Uhrzeigersinn gespielt.' in `source_c.md` -- Direct statement. |
| 101 | The Mah-Jongg caller receives an additional bonus of 10 points credited, often 20 points. | supported | `source_a.md` | 'Der Mah-Jongg-Rufer erhält eine zusätzliche Prämie von 10 (häufig 20) Punkten gutgeschrieben.' in `source_a.md` -- Directly stated in source_a. |
| 102 | Concealed combinations count double. | supported | `source_c.md` | 'Verdeckte Kombinationen zählen das Doppelte.' in `source_c.md` -- Directly stated in source_c under Drillinge (Pongs). |
| 103 | A Kong counts four times as much as the corresponding Pong. | supported | `source_c.md` | 'Ein Kong zählt viermal so viel wie der entsprechende Pong.' in `source_c.md` -- Directly stated in source_c. |
| 104 | A player who robs the Kong receives an additional bonus of 10 points. | supported | `source_a.md` | 'Für diese Beraubung des Kong erhält er einen zusätzlichen Bonus von 10 Punkten.' in `source_a.md` -- Directly stated in source_a. |
| 105 | Doubling twice quadruples the original value of the hand. | supported | `source_a.md` | 'zweimaliges Verdoppeln vervierfacht beispielsweise den ursprünglichen Wert des Spielbildes.' in `source_a.md` -- Directly stated in source_a. |
| 106 | The limit is usually agreed at 300 or 500 points. | supported | `source_a.md` | 'Dieses beträgt meist 300 oder 500 Punkte.' in `source_a.md` -- Directly stated in source_a. |
| 107 | If a hand consists exclusively of trump-suit tiles, i.e. only wind and dragon tiles, this hand is scored with the maximum point value. | supported | `source_a.md` | 'Besteht das Spielbild des Mah-Jongg-Rufers ausschließlich aus Ziegeln der Trumpffarbe, also nur aus Wind- und Drachenziegeln, so wird diese Hand mit dem Punktemaximum bewertet.' in `source_a.md` -- Directly stated in source_a. |
| 108 | If East Wind can call Mah-Jongg immediately after picking up his tiles, he possesses the Blessing of Heaven and receives the maximum score credited. | supported | `source_a.md` | 'Kann Ostwind sofort nach Aufnehmen seiner Ziegel Mah-Jongg rufen, so besitzt er den Segen des Himmels und erhält das Punktemaximum gutgeschrieben.' in `source_a.md` -- Directly stated in source_a. |
| 109 | If another player can call the first tile discarded by East Wind and thereby declare Mah-Jongg, this is called the Blessing of Earth and the player receives half the limit credited. | supported | `source_a.md` | 'Kann ein anderer Spieler den ersten von Ostwind abgelegten Stein aufrufen und damit Mah-Jongg erklären, so ist dies der Segen der Erde und der Spieler erhält die Hälfte des Limits gutgeschrieben.' in `source_a.md` -- Directly stated in source_a. |
| 110 | When playing with 144 tiles, including the main-suit tiles (flower and season tiles), each side of the wall consists of 18 stacks of tiles. | supported | `source_a.md` | 'Wird Mah-Jongg mit 144 Steinen, also einschließlich der Steine der Hauptfarbe (der Blumen- und Jahreszeitenziegel), gespielt, so besteht jede Seite der Mauer aus 18 Ziegelstapeln.' in `source_a.md` -- Directly stated in source_a. |
| 111 | Main-suit tile No. 1 is assigned to East Wind. | supported | `source_a.md` | 'Nr. 1 gilt für den Ostwind, Nr. 2 für den Südwind, Nr. 3 für den Westwind und Nr. 4. für den Nordwind.' in `source_a.md` -- Directly stated in source_a. |
| 112 | Main-suit tile No. 2 is assigned to South Wind. | supported | `source_a.md` | 'Nr. 1 gilt für den Ostwind, Nr. 2 für den Südwind, Nr. 3 für den Westwind und Nr. 4. für den Nordwind.' in `source_a.md` -- Directly stated in source_a. |
| 113 | Main-suit tile No. 3 is assigned to West Wind. | supported | `source_a.md` | 'Nr. 1 gilt für den Ostwind, Nr. 2 für den Südwind, Nr. 3 für den Westwind und Nr. 4. für den Nordwind.' in `source_a.md` -- Directly stated in source_a. |
| 114 | Main-suit tile No. 4 is assigned to North Wind. | supported | `source_a.md` | 'Nr. 1 gilt für den Ostwind, Nr. 2 für den Südwind, Nr. 3 für den Westwind und Nr. 4. für den Nordwind.' in `source_a.md` -- Directly stated in source_a. |
| 115 | A round ends as soon as the player who held the position of North Wind in the first game loses a game as East Wind. | supported | `source_a.md` | 'Eine Runde ist beendet, sobald der Spieler, der im ersten Spiel die Position des Nordwindes innehatte, ein Spiel als Ostwind verliert' in `source_a.md` -- Directly stated in source_a. |
| 116 | A round consists of at least four games. | supported | `source_a.md` | 'Eine Runde besteht aus mindestens vier Spielen.' in `source_a.md` -- Directly stated in source_a. |
| 117 | A full match, if agreed, consists of four rounds. | supported | `source_a.md` | 'Wird nicht nur eine einzelne Runde gespielt, sondern eine Partie vereinbart, so besteht diese aus vier Runden.' in `source_a.md` -- Directly stated in source_a. |
| 118 | In the first round, the East Wind round, East is the prevailing wind. | supported | `source_a.md` | 'In der ersten Runde, der Ostwindrunde, ist Ost der vorherrschende Wind (Rundenwind);' in `source_a.md` -- Directly stated in source_a. |
| 119 | In the second round, the South Wind round, South Wind prevails. | supported | `source_a.md` | 'in der zweiten Runde (Südwindrunde) herrscht Südwind vor,' in `source_a.md` -- Directly stated in source_a. |
| 120 | The third round is the West Wind round. | supported | `source_a.md` | 'die dritte Runde ist die Westwindrunde' in `source_a.md` -- Directly stated in source_a. |
| 121 | The fourth round is the North Wind round. | supported | `source_a.md` | 'und die vierte die Nordwindrunde.' in `source_a.md` -- Directly stated in source_a. |
| 122 | Usually no more than two matches are played. | supported | `source_a.md` | 'meist werden nicht mehr als zwei Partien gespielt.' in `source_a.md` -- Directly stated in source_a. |
| 123 | The modern Mah-Jongg was officially recognized in 1998 by the state sports commission of China as the 255th sport. | supported | `source_a.md` | 'Das moderne Mah-Jongg, so wie es 1998 von der staatlichen Sportkommission Chinas offiziell als 255. Sportart anerkannt wurde' in `source_a.md` -- Directly stated in source_a. |
| 124 | Babcock listed some of these classic hands in his Red Book of 1920. | supported | `source_a.md` | 'die teilweise bereits Babcock in seinem Red Book von 1920 angeführt hat und die als klassisch chinesisch anzusehen sind.' in `source_a.md` -- Directly stated in source_a. |
| 125 | The Finnish manufacturer Lagarto offers a paid Windows version of traditional Mah-Jongg called Four Winds. | supported | `source_a.md` | 'Der finnische Hersteller Lagarto bietet eine kostenpflichtige Windows-Version des traditionellen Mah-Jongg namens Four Winds an.' in `source_a.md` -- Directly stated in source_a. |
| 126 | A player can compete against three players simulated by the software. | supported | `source_a.md` | 'Ein Spieler kann gegen drei durch die Software nachgebildete Spieler antreten.' in `source_a.md` -- Directly stated in source_a. |
| 127 | The KDE project includes a free version of Mah-Jongg called Kajongg. | supported | `source_a.md` | 'Das KDE-Projekt enthält eine kostenfreie Version von Mah-Jongg, die Kajongg genannt wird.' in `source_a.md` -- Directly stated in source_a. |
| 128 | In various parts of the Yakuza game series, such as Yakuza 0, the Japanese variant of Mah-Jongg (Riichi Mahjong) is present as a minigame. | supported | `source_a.md` | 'In verschiedenen Teilen der Yakuza-Spieleserie, wie zum Beispiel Yakuza 0 ist die japanische Variante von Mah-Jongg (Riichi Mahjong) als Minispiel vorhanden.' in `source_a.md` -- Directly stated in source_a. |
| 129 | For iPhone and iPad there is an app in the Apple App Store called Mahjong! by POK-Software, a traditional version simulating up to 3 co-players. | supported | `source_a.md` | 'Für iPhone und iPad gibt es im Apple App Store unter dem Namen Mahjong! von POK-Software eine traditionelle Version, die bis zu 3 Mitspieler simuliert.' in `source_a.md` -- Directly stated in source_a. |
| 130 | From the mid-1980s, Mah-Jongg Solitaire became popular as a computer game initially under the name Shanghai. | supported | `source_b.md` | 'Ab Mitte der 1980er Jahre wurde Mah-Jongg Solitaire zunächst unter dem Namen Shanghai als Computerspiel populär' in `source_b.md` -- Directly stated in source_b. |
| 131 | The improved graphical capabilities of the new Amiga computer first allowed an appealing display of this game. | supported | `source_b.md` | 'nachdem die verbesserten grafischen Möglichkeiten des neuen Amiga-Computers erstmals eine ansprechende Darstellung dieses Spiels erlaubten.' in `source_b.md` -- Directly stated in source_b. |
| 132 | In the most popular computer game variant, all 144 tiles lie on the table at the start of the game, sometimes in several layers on top of each other. | supported | `source_b.md` | 'Bei der beliebtesten Computerspiel-Variante liegen zu Spielbeginn alle 144 Steine auf dem Tisch, teils in mehreren Lagen übereinander.' in `source_b.md` -- Directly stated in source_b. |
| 133 | Traditionally the playing tiles are arranged in the figure of a dragon or a turtle. | supported | `source_b.md` | 'Traditionell werden die Spielsteine in der Figur eines Drachen oder einer Schildkröte aufgebaut,' in `source_b.md` -- Directly stated in source_b. |
| 134 | A single player must remove all 144 tiles from the table in pairs. | supported | `source_b.md` | 'Ein einzelner Spieler muss paarweise alle 144 Steine vom Tisch nehmen.' in `source_b.md` -- Directly stated in source_b. |
| 135 | In the romantic film comedy Crazy Rich Asians (2018), a Mah-Jongg game forms the dramaturgical climax of a central confrontation. | supported | `source_b.md` | 'In der romantischen Filmkomödie Crazy Rich Asians (2018) bildet eine Mah-Jongg-Partie den dramaturgischen Höhepunkt einer zentralen Konfrontation.' in `source_b.md` -- Directly stated in source_b. |
| 136 | The film Gefahr und Begierde is based on the short story of the same name by Eileen Chang. | supported | `source_b.md` | 'In dem Film Gefahr und Begierde, nach der gleichnamigen Kurzgeschichte von Eileen Chang, erzählt Ang Lee die Geschichte einer tragischen Liebesbeziehung' in `source_b.md` -- Directly stated in source_b. |
| 137 | Ang Lee tells the story of a tragic romantic relationship between a resistance fighter and the intelligence chief of the collaborationist government of Wang Jingwei. | supported | `source_b.md` | 'erzählt Ang Lee die Geschichte einer tragischen Liebesbeziehung zwischen einer Widerstandskämpferin und dem Geheimdienstchef der Kollaborationsregierung von Wang Jingwei.' in `source_b.md` -- Directly stated in source_b. |
| 138 | The resistance fighter in the film is played by Tang Wei. | supported | `source_b.md` | 'in denen die Widerstandskämpferin, gespielt von Tang Wei, auf die Ehefrauen der Regierungsmitglieder trifft.' in `source_b.md` -- Directly stated in source_b. |
| 139 | In the crime novel Sous les vents de Neptun (German title "Der vierzehnte Stein") by Fred Vargas (Frédérique Audoin-Rouzeau), the game Mah-Jongg plays a central role. | supported | `source_b.md` | 'Im Kriminalroman Sous les vents de Neptun (dt. „Der vierzehnte Stein“) von Fred Vargas (Frédérique Audoin-Rouzeau) nimmt das Spiel Mah-Jongg eine zentrale Rolle ein.' in `source_b.md` -- Directly stated in source_b. |
| 140 | The book was made into a film in 2008. | supported | `source_b.md` | 'Das Buch wurde 2008 verfilmt.' in `source_b.md` -- Directly stated in source_b. |
| 141 | In the French-Swiss feature film Die Gleichung ihres Lebens (2023), the main character Marguerite learns Mah-Jongg after abandoning her mathematics doctorate. | supported | `source_b.md` | 'Im französisch-Schweizer Spielfilm Die Gleichung ihres Lebens (2023) lernt die Hauptperson Marguerite nach dem Abbruch ihrer Mathematik-Promotion Mah-Jongg und erzielt erhebliche Einnahmen damit.' in `source_b.md` -- Directly stated in source_b. |
| 142 | Marguerite earns considerable income with Mah-Jongg. | supported | `source_b.md` | 'und erzielt erhebliche Einnahmen damit.' in `source_b.md` -- Directly stated in source_b. |

## Structure

**9** mechanical check(s) over **216** source segment(s) and what the merge declared about them. No model was asked anything: every check here is a set difference, a string containment or a division.
Separately, and not one of those 9: the merged text was searched for `merge.md`'s worked-example words (`marlbrook`, `funicular`), which belong to no source document.
Separately again: the **142** claim(s) extracted from the merged document were checked for one claim appearing on two different lines, which is a merge that kept both sources' wordings of one fact. The sources yielded **218**. The two counts are reported, not compared: claim extraction is a sample, so a merge count above a source count is evidence and never the finding.

Ordering: 5 run(s) over 215 attributed segment(s) — sources interleaved. 37 of 37 source heading(s) survive. This is a measurement, not a finding: whether this shape is right depends on whether the sources had anything to interleave, which this tool does not measure.

No structural finding.

## Review queue

None. Every claim the forward pass found missing is a finding above, and no declared drop accounts for one.

## Declarations

The merge declared **3** departure(s) from its sources. Checking them confirms 2, rejects 0, and leaves 1 unchecked — a declaration is unchecked when no claim was drawn from the segment it names *and* the reconciler's location of that text settles nothing about what was declared, and that is not agreement.

Declared loss: 0 of 216 source segment(s) declared gone, **0.0%** against a 3% ceiling.

| Segment | Declared | The merge's reason | Confirmed? | On what evidence |
|---|---|---|---|---|
| `c98` | reworded | added forward reference to the dedicated Beraubung des Kong section | **unchecked** | no claim was drawn from this segment, so the forward pass says nothing about whether 'reworded' is what happened to it (no claim traced to it) |
| `c99` | duplicate | same fact restated more fully by a3 under its own heading | **confirmed** | declared 'duplicate' and every claim from it came back SUPPORTED (`C-106`) |
| `a35` | reworded | fixed missing space typo before "verwendet" | **confirmed** | declared 'reworded' and every claim from it came back SUPPORTED (`A-029`) |


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
| Calls | 10 live, 0 cached, 0 replayed |
| Tokens | unknown (10 call(s) reported no usage) |
| Cost | unmeasured (10 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, merge, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 1956.4s |
| Generated | 2026-09-27T23:50:18+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/merge.md` `5f7133b7091c` |
| Prompt | `prompts/verify.md` `8c9ca12b724f` |
| Prompt | `prompts/verify_reverse.md` `ffb9672d7d6b` |

> **Document content was handed to a program on this machine (`lineup sonnet-5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, merge, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
