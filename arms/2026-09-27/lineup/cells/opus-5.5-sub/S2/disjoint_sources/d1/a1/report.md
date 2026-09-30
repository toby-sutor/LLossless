## Verdict

**1 finding(s).** In the claims: 1 partially dropped.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 47 |
| Claims extracted from `source_a.md` | 18 |
| Claims extracted from `source_b.md` | 35 |
| Forward — source claims accounted for in the merge | **52/53** |
| Forward — carried only in part | 1 |
| Forward — `source_a.md` claims accounted for | **18/18** |
| Forward — `source_b.md` claims accounted for | **34/35** (1 in part) |
| Reverse — merge claims found in a source | **47/47** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **100/100** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Partly dropped — the merge carries some of this claim

- **B-027** (`source_b.md:24`) — The young man recovered at the old lady's house.
  - evidence: 'When the man recovered again' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The text states he recovered but does not explicitly say the recovery happened at her house.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 18 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 18 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | There was a princess in a distant country. | 3 | carried | 'there was a princess in a distant country' in `merged.md` -- The text states a princess lived in a distant country. |
| 2 | The princess loved to spend time in her rosegarden. | 3 | carried | 'loved to spend time in her beautiful rosegarden' in `merged.md` -- The text states she loved spending time in her rosegarden. |
| 3 | The princess visited the rosegarden every morning from 8 am till 9 am. | 7 | carried | 'She visited the rosegarden every morning from 8 am till 9 am' in `merged.md` -- The visiting times match exactly. |
| 4 | The princess visited the rosegarden right after her breakfast. | 7 | carried | 'right after her breakfast' in `merged.md` -- The text states the visit was right after breakfast. |
| 5 | From 02:00 till 15:30 o'clock, the princess worked in the rosegarden to tidy it up. | 8 | carried | "From 02:00 till 15:30 o'clock, she worked in the rosegarden to tidy it up." in `merged.md` -- The working times and purpose match exactly. |
| 6 | The princess's mother did not appreciate that the princess, as a princess, would actually work in the garden. | 8 | carried | 'Her mother did not appreciate that she, as a princess, would actually work in the garden' in `merged.md` -- The text states the mother's disapproval directly. |
| 7 | The princess didn't care that her mother did not appreciate her working in the garden. | 8 | carried | "but the princess didn't care" in `merged.md` -- The text states the princess did not care about the disapproval. |
| 8 | The rosegarden lost all its life in winter. | 12 | carried | 'The rosegarden lost all his life in winter' in `merged.md` -- Same meaning; the text uses 'his' instead of 'its'. |
| 9 | The princess could not enjoy the colors and life of the rosegarden in winter. | 12 | carried | 'so the young lady could not enjoy the beautiful colors and all the life the rosegarden harbored' in `merged.md` -- The young lady refers to the princess, who could not enjoy the colors and life in winter. |
| 10 | Once spring arrived, the rosegarden turned back to life and color. | 13 | carried | 'But once spring arrived, it turned back to life and color.' in `merged.md` -- The text states the garden revived in spring. |
| 11 | The rose garden was the private property of the royal family. | 17 | carried | 'the rose garden was the private property of the royal family' in `merged.md` -- The text states the ownership directly. |
| 12 | The princess insisted on making the rose garden accessible to the public every March 1st to March 31st. | 17 | carried | 'the young princess insisted on making the garden accessible to the public every March 1st to March 31st' in `merged.md` -- The public access dates match. |
| 13 | During the public access period, people from all over the country traveled to the castle to wander through the rosegarden. | 18 | carried | 'During that time, people from all over the country traveled to the castel to enjoy a nice day wandering through the rosegarden' in `merged.md` -- The text states people traveled to the castle to wander the garden during that period. |
| 14 | It became tradition that everyone who visited the rosegarden from the outside picked their favorite scenery and tried to draw what they liked most. | 22 | carried | 'It became tradition that everyone who visited the rosegarden from the outside picked their favorite scenery and tried to draw what they liked most.' in `merged.md` -- The claim matches the text exactly. |
| 15 | Visitors to the rosegarden sent the postcard to their home. | 22 | carried | 'They then sent the postcard to their home.' in `merged.md` -- The visitors sent the postcard home. |
| 16 | People started to make bets on whether the postcard arrived at their home before they arrived home. | 23 | carried | 'People were starting to make bets on whether the postcard arrived at their home before they arrived home.' in `merged.md` -- The betting is stated directly. |
| 17 | In many cases, the bet on whether the postcard arrived home before the visitor was a tie. | 24 | carried | 'In many cases, it was a tie' in `merged.md` -- The text states the result was often a tie. |
| 18 | The people and the postcards were usually transported in the same carriage. | 24 | carried | 'the people and the postcards were usually transported in the same carriage' in `merged.md` -- The shared carriage is stated directly. |

### `source_b.md` -- 35 claim(s): 0 dropped, 0 contradicted, 1 carried in part, 34 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 27 | The young man recovered at the old lady's house. | 24 | carried in part | 'When the man recovered again' in `merged.md` -- The text states he recovered but does not explicitly say the recovery happened at her house. |
| 1 | An old lady lived in a dark, spooky forest. | 3 | carried | 'there was an old lady that lived in a dark, spooky forest' in `merged.md` -- The text states this directly. |
| 2 | The forest was not traversable between October and April. | 7 | carried | 'The forest was not traversable between October and April' in `merged.md` -- The text states this directly. |
| 3 | The forest was too wet and too cold to traverse between October and April. | 7 | carried | 'The forest was not traversable between October and April as it was too wet and too cold.' in `merged.md` -- The text gives wetness and cold as the reason the forest could not be traversed. |
| 4 | The old lady lived the entire year in the forest. | 8 | carried | 'The old lady nevertheless lived the entire year in the forest.' in `merged.md` -- The text states this directly. |
| 5 | Over the years, the old lady acclimated to the weather. | 8 | carried | 'Over the years, she acclimated to the weather' in `merged.md` -- The text states this directly. |
| 6 | Over the years, the old lady built strategies to survive the harsh conditions. | 8 | carried | 'built strategies to survive the harsh conditions' in `merged.md` -- The text states this as part of the same sentence about the years. |
| 7 | Many people suspected the old lady would be a witch that worked on forbidden magic. | 12 | carried | 'many people suspected the old lady would be a witch that worked on forbidden magic' in `merged.md` -- The text states this directly. |
| 8 | The old lady collected wild herbs. | 12 | carried | 'she collected wild herbs' in `merged.md` -- The text states this directly. |
| 9 | The old lady did not harvest skulls and bones. | 12 | carried | 'Instead of harvesting skulls and bones, she collected wild herbs.' in `merged.md` -- 'Instead of' entails she did not harvest skulls and bones. |
| 10 | The wild herbs collected by the old lady were tried. | 13 | carried | 'Those wild herbs were tried' in `merged.md` -- The text uses 'tried', matching the claim. |
| 11 | The wild herbs collected by the old lady were sold to wandering travelers. | 13 | carried | 'sold to wandering travelers' in `merged.md` -- The text states this directly. |
| 12 | The wandering travelers transported the herbs into the cities. | 13 | carried | 'wandering travelers who transported and sold the herbs into the cities' in `merged.md` -- The text states the travelers transported the herbs into the cities. |
| 13 | The wandering travelers sold the herbs into the cities. | 13 | carried | 'wandering travelers who transported and sold the herbs into the cities' in `merged.md` -- The text states the travelers sold the herbs into the cities. |
| 14 | In one harsh winter, many people of the nearby village became very sick. | 17 | carried | 'In one harsh winter, many people of the nearby village became very sick.' in `merged.md` -- The text states this directly. |
| 15 | One young man traveled to the old lady's house to help the villagers. | 17 | carried | "In a desperate attempt to help the villagers, one young man took the courage and traveled to the old lady's house" in `merged.md` -- The text states the young man traveled there to help the villagers. |
| 16 | The old lady's house was deep in the woods. | 17 | carried | "the old lady's house deep in the woods" in `merged.md` -- The text states the house was deep in the woods. |
| 17 | It took the young man days to reach the old lady's house. | 18 | carried | 'It took him days to reach her house' in `merged.md` -- The text states this directly. |
| 18 | The young man struggled with the wet and slippery ground on the way to the old lady's house. | 18 | carried | 'he struggled with the wet and slippery ground' in `merged.md` -- The text states this directly. |
| 19 | The young man lost his orientation several times on the way to the old lady's house. | 18 | carried | 'He also lost his orientation several times.' in `merged.md` -- The text states this directly. |
| 20 | The young man eventually reached the old lady's house. | 19 | carried | 'But eventually, he reached her house.' in `merged.md` -- The text states this directly. |
| 21 | The young man carefully knocked on the old lady's door. | 19 | carried | 'He carefully knocked' in `merged.md` -- The text states he knocked carefully at her house. |
| 22 | The young man hoped that all the rumors about the old lady were untrue. | 19 | carried | 'hoped that all the rumors about the lady were untrue' in `merged.md` -- The text states this directly. |
| 23 | The old lady opened the door and saw the young man. | 20 | carried | 'When she opened the door and saw the young man' in `merged.md` -- The text states this directly. |
| 24 | The old lady asked the young man to come into her house. | 20 | carried | 'she asked him to come into her house' in `merged.md` -- The text states this directly. |
| 25 | The old lady asked the young man to sit at the fire. | 20 | carried | 'sit at the fire' in `merged.md` -- The text states she asked him to sit at the fire. |
| 26 | The old lady asked the young man to drink some hot soup she made for him. | 20 | carried | 'drink some hot soup she made for him' in `merged.md` -- The text states she asked him to drink the soup she made. |
| 28 | The old lady gave the young man enough medicine for the entire village. | 24 | carried | 'she gave him enough medicine made out of the herbs she collected in spring for the entire village' in `merged.md` -- The text states she gave him enough medicine for the entire village. |
| 29 | The medicine was made out of the herbs the old lady collected in spring. | 24 | carried | 'medicine made out of the herbs she collected in spring' in `merged.md` -- The text states this directly. |
| 30 | The young man traveled back to his village. | 25 | carried | 'He traveled back to his village' in `merged.md` -- The text states this directly. |
| 31 | The young man went to the home of every sick person to provide them with the correct amount of medicine. | 25 | carried | 'went to the home of every sick person to provide them with the correct amount of medicine' in `merged.md` -- The text states this directly. |
| 32 | The old lady from the woods told the young man the correct amount of medicine for each sick person. | 25 | carried | 'the correct amount of medicine as told by the old lady from the woods' in `merged.md` -- The text states the amounts were as told by the old lady. |
| 33 | Eventually, everyone in the village got healthy again. | 26 | carried | 'Eventually, everyone got healthy again' in `merged.md` -- The text states everyone recovered. |
| 34 | From then on, the villagers sent a huge basket of cheese and dried meat to the old lady every autumn. | 26 | carried | 'from then on the villagers sent a huge basket of cheese and dried meat to the old lady every autumn' in `merged.md` -- The text states this directly. |
| 35 | The villagers sent the basket so that the old lady could feast in winter. | 26 | carried | 'so that she could feast in winter' in `merged.md` -- The text states the purpose of the basket. |

### `merged.md` -- 47 claim(s): 0 invented, 0 contradicted, 0 supported in part, 47 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | There was a princess in a distant country. | supported | `source_a.md` | 'there was a princess in a distant country' in `source_a.md` -- Source A states this directly. |
| 2 | The princess had a rosegarden. | supported | `source_a.md` | 'loved to spend time in her beautiful rosegarden' in `source_a.md` -- The phrase "her beautiful rosegarden" establishes that the princess had a rosegarden. |
| 3 | The princess visited the rosegarden every morning from 8 am till 9 am. | supported | `source_a.md` | 'She visited the rosegarden every morning from 8 am till 9 am' in `source_a.md` -- Source A states this directly. |
| 4 | The princess visited the rosegarden right after her breakfast. | supported | `source_a.md` | 'right after her breakfast' in `source_a.md` -- Source A says the morning visit was right after her breakfast. |
| 5 | From 02:00 till 15:30 o'clock, the princess worked in the rosegarden to tidy it up. | supported | `source_a.md` | "From 02:00 till 15:30 o'clock, she worked in the rosegarden to tidy it up." in `source_a.md` -- Source A states this verbatim. |
| 6 | The princess's mother did not appreciate that the princess would actually work in the garden. | supported | `source_a.md` | 'Her mother did not appreciate that she, as a princess, would actually work in the garden' in `source_a.md` -- Source A states this directly. |
| 7 | The princess didn't care that her mother did not appreciate her working in the garden. | supported | `source_a.md` | "but the princess didn't care" in `source_a.md` -- Source A says the princess didn't care about her mother's disapproval. |
| 8 | The rosegarden lost all its life in winter. | supported | `source_a.md` | 'The rosegarden lost all his life in winter' in `source_a.md` -- The claim is the same statement with "his" rendered as "its". |
| 9 | Once spring arrived, the rosegarden turned back to life and color. | supported | `source_a.md` | 'But once spring arrived, it turned back to life and color.' in `source_a.md` -- Source A states this directly of the rosegarden. |
| 10 | The rose garden was the private property of the royal family. | supported | `source_a.md` | 'the rose garden was the private property of the royal family' in `source_a.md` -- Source A states this directly. |
| 11 | The young princess insisted on making the rose garden accessible to the public every March 1st to March 31st. | supported | `source_a.md` | 'the young princess insisted on making the garden accessible to the public every March 1st to March 31st' in `source_a.md` -- Source A states this directly. |
| 12 | During the public access period, people from all over the country traveled to the castle to wander through the rosegarden. | supported | `source_a.md` | 'people from all over the country traveled to the castel to enjoy a nice day wandering through the rosegarden' in `source_a.md` -- The claim restates the source, with "castel" corrected to "castle". |
| 13 | It became tradition that everyone who visited the rosegarden from the outside picked their favorite scenery and tried to draw what they liked most. | supported | `source_a.md` | 'It became tradition that everyone who visited the rosegarden from the outside picked their favorite scenery and tried to draw what they liked most.' in `source_a.md` -- Source A states this verbatim. |
| 14 | Visitors to the rosegarden sent the postcard to their home. | supported | `source_a.md` | 'They then sent the postcard to their home.' in `source_a.md` -- Source A says the visitors sent the postcard to their home. |
| 15 | People were starting to make bets on whether the postcard arrived at their home before they arrived home. | supported | `source_a.md` | 'People were starting to make bets on whether the postcard arrived at their home before they arrived home.' in `source_a.md` -- Source A states this verbatim. |
| 16 | In many cases, the bet on whether the postcard or the person arrived home first was a tie. | supported | `source_a.md` | 'In many cases, it was a tie' in `source_a.md` -- Source A says that in many cases the bet was a tie. |
| 17 | The people and the postcards were usually transported in the same carriage. | supported | `source_a.md` | 'the people and the postcards were usually transported in the same carriage' in `source_a.md` -- Source A states this directly. |
| 18 | There was an old lady that lived in a dark forest. | supported | `source_b.md` | 'there was an old lady that lived in a dark, spooky forest' in `source_b.md` -- Source B states this and adds the word "spooky". |
| 19 | The forest was not traversable between October and April. | supported | `source_b.md` | 'The forest was not traversable between October and April' in `source_b.md` -- Source B states this directly. |
| 20 | The forest was too wet and too cold between October and April. | supported | `source_b.md` | 'The forest was not traversable between October and April as it was too wet and too cold.' in `source_b.md` -- Source B says the forest was too wet and too cold in that period. |
| 21 | The old lady lived the entire year in the forest. | supported | `source_b.md` | 'The old lady nevertheless lived the entire year in the forest.' in `source_b.md` -- Source B states this directly. |
| 22 | Over the years, the old lady acclimated to the weather. | supported | `source_b.md` | 'Over the years, she acclimated to the weather' in `source_b.md` -- Source B states this directly. |
| 23 | Over the years, the old lady built strategies to survive the harsh conditions. | supported | `source_b.md` | 'built strategies to survive the harsh conditions' in `source_b.md` -- Source B states this directly. |
| 24 | Many people suspected the old lady was a witch that worked on forbidden magic. | supported | `source_b.md` | 'many people suspected the old lady would be a witch that worked on forbidden magic' in `source_b.md` -- Source B states this directly. |
| 25 | The old lady collected wild herbs. | supported | `source_b.md` | 'she collected wild herbs' in `source_b.md` -- Source B states this directly. |
| 26 | The old lady did not harvest skulls and bones. | supported | `source_b.md` | 'Instead of harvesting skulls and bones, she collected wild herbs.' in `source_b.md` -- "Instead of harvesting skulls and bones" means she did not harvest them. |
| 27 | The wild herbs were dried. | supported | `source_b.md` | 'Those wild herbs were tried and sold to wandering travelers' in `source_b.md` -- The source's "tried" is evidently a typo for "dried" in this context, so it states that the herbs were dried. |
| 28 | The wild herbs were sold to wandering travelers. | supported | `source_b.md` | 'sold to wandering travelers' in `source_b.md` -- Source B states this directly. |
| 29 | The wandering travelers transported and sold the herbs into the cities. | supported | `source_b.md` | 'wandering travelers who transported and sold the herbs into the cities' in `source_b.md` -- Source B states this directly. |
| 30 | In one harsh winter, many people of the village near the forest became very sick. | supported | `source_b.md` | 'In one harsh winter, many people of the nearby village became very sick.' in `source_b.md` -- "Nearby village" refers to the village near the forest. |
| 31 | One young man traveled to the old lady's house deep in the woods to help the villagers. | supported | `source_b.md` | "In a desperate attempt to help the villagers, one young man took the courage and traveled to the old lady's house deep in the woods." in `source_b.md` -- Source B states this directly. |
| 32 | The old lady's house was deep in the woods. | supported | `source_b.md` | "the old lady's house deep in the woods" in `source_b.md` -- Source B states this directly. |
| 33 | It took the young man days to reach the old lady's house. | supported | `source_b.md` | 'It took him days to reach her house' in `source_b.md` -- Source B states this directly. |
| 34 | The young man struggled with the wet and slippery ground. | supported | `source_b.md` | 'he struggled with the wet and slippery ground' in `source_b.md` -- Source B states this directly. |
| 35 | The young man lost his orientation several times. | supported | `source_b.md` | 'He also lost his orientation several times.' in `source_b.md` -- Source B states this directly. |
| 36 | The young man eventually reached the old lady's house. | supported | `source_b.md` | 'But eventually, he reached her house.' in `source_b.md` -- Source B states this directly. |
| 37 | The young man carefully knocked on the old lady's door. | supported | `source_b.md` | 'He carefully knocked' in `source_b.md` -- Source B says he carefully knocked at her house. |
| 38 | The young man hoped that all the rumors about the old lady were untrue. | supported | `source_b.md` | 'hoped that all the rumors about the lady were untrue' in `source_b.md` -- Source B states this directly. |
| 39 | The old lady asked the young man to come into her house. | supported | `source_b.md` | 'she asked him to come into her house' in `source_b.md` -- Source B states this directly. |
| 40 | The old lady asked the young man to sit at the fire. | supported | `source_b.md` | 'sit at the fire' in `source_b.md` -- The same sentence of source B includes asking him to sit at the fire. |
| 41 | The old lady asked the young man to drink some hot soup she made for him. | supported | `source_b.md` | 'drink some hot soup she made for him' in `source_b.md` -- The same sentence of source B includes asking him to drink the soup. |
| 42 | When the young man recovered, the old lady gave him enough medicine for the entire village. | supported | `source_b.md` | 'When the man recovered again, she gave him enough medicine made out of the herbs she collected in spring for the entire village.' in `source_b.md` -- Source B states this directly. |
| 43 | The medicine was made out of the herbs the old lady collected in spring. | supported | `source_b.md` | 'medicine made out of the herbs she collected in spring' in `source_b.md` -- Source B states this directly. |
| 44 | The young man traveled back to his village. | supported | `source_b.md` | 'He traveled back to his village' in `source_b.md` -- Source B states this directly. |
| 45 | The young man went to the home of every sick person to provide them with the correct amount of medicine as told by the old lady. | supported | `source_b.md` | 'went to the home of every sick person to provide them with the correct amount of medicine as told by the old lady from the woods' in `source_b.md` -- Source B states this directly. |
| 46 | Eventually, everyone in the village got healthy again. | supported | `source_b.md` | 'Eventually, everyone got healthy again' in `source_b.md` -- Source B states this, in context of the villagers. |
| 47 | From then on the villagers sent a huge basket of cheese and dried meat to the old lady every autumn. | supported | `source_b.md` | 'from then on the villagers sent a huge basket of cheese and dried meat to the old lady every autumn' in `source_b.md` -- Source B states this directly. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | 31c2462e2828 (command) -- lineup opus-5.5-sub |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | claude-opus-5-5 -> claude-opus-5-5 |
| Model (verify) | claude-opus-5-5 -> claude-opus-5-5 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile subscription, effort decompose=medium, merge=medium, verify=medium |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 5 live, 0 cached, 0 replayed |
| Tokens | unknown (5 call(s) reported no usage) |
| Cost | unmeasured (5 call(s) reported no tokens, so no figure can be derived) |
| Schema repairs | 0 |
| Isolation | decompose, verify: safe mode, no tools |
| Errors | 0 |
| Duration | 120.9s |
| Generated | 2026-09-27T20:33:17+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content was handed to a program on this machine (`lineup opus-5.5-sub`).** What that program did with it is outside anything this tool can see: there is no address to classify, and the network containment this suite runs under is per-process, so a child that opened a socket opened it unobserved. Treat the documents as having left unless you wrote the program.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
