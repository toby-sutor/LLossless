## Verdict

**5 finding(s).** In the claims: 1 dropped, 4 partially dropped.

## Coverage

| | |
|---|---|
| Claims extracted from `merged.md` | 31 |
| Claims extracted from `source_a.md` | 23 |
| Claims extracted from `source_b.md` | 23 |
| Forward — source claims accounted for in the merge | **41/46** |
| Forward — carried only in part | 4 |
| Forward — `source_a.md` claims accounted for | **18/23** (4 in part) |
| Forward — `source_b.md` claims accounted for | **23/23** |
| Reverse — merge claims found in a source | **31/31** |
| Reverse — supported only in part | 0 |
| Evidence grounded | **74/76** |
| Units of work errored | 0 |
| Claims submitted but not graded | 0 |

## Findings

Each finding below names the document it was judged against. The model is told to use that document alone and to ignore anything it knows from elsewhere, and nothing here can prove it did -- so a rationale that reads like general knowledge is one to check against the span it quoted.

### Dropped — in a source, not in the merge

- **A-021** (`source_a.md:7`) — Protestantism itself split into hundres or thousands different sects.
  - judged against: `merged.md`
  - rationale: The reference text mentions Protestantism splitting into 'hundreds or thousands different sects' but the claim misspells 'hundres' which does not appear in the reference text.

### Partly dropped — the merge carries some of this claim

- **A-004** (`source_a.md:3`) — Jesus of Nazareth was a Jewish preacher.
  - evidence: 'Jesus of Nazareth, a Jewish preacher' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The reference text calls Jesus a Jewish preacher in one version but a Jewish rabbi in another version, presenting conflicting descriptions.
- **A-008** (`source_a.md:5`) — Christianity's central beliefs include the Trinity (God as Father, Son (Jesus), and the Holy Spirit).
  - evidence: 'the Trinity (God as Father, Son (Jesus), and the Holy Spirit)' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: One version specifies Son as Jesus in parentheses; another version lists Father, Son, and Holy Spirit without the clarification, so the full claim details are partially stated.
- **A-012** (`source_a.md:7`) — The Bible is made up of the Old (Hebrew) and New (Greek) Testaments.
  - evidence: 'made up of the Old (Hebrew) and New (Greek) Testaments' in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: One version includes the language specifications (Hebrew and Greek) in parentheses; another omits them, so the claim's detailed specifications are only partially stated.
- **A-015** (`source_a.md:7`) — Core Christian practices include the Eucharist (communion) commemorating Jesus' last supper.
  - evidence: "the Eucharist (communion) commemorating Jesus' last supper" in `merged.md` (grounded)
  - judged against: `merged.md`
  - rationale: The claim specifies Jesus' last supper; one version adds 'with his disciples' but the basic claim is supported by the shorter version.

## Length capped

None.

## Not graded

None. Every claim submitted came back with a usable verdict.

## Inventory

Every claim that was extracted, and what became of it. The sections above list only the exceptions; this lists all of them, so a claim that is not here was never checked.

### `source_a.md` -- 23 claim(s): 1 dropped, 0 contradicted, 4 carried in part, 18 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 21 | Protestantism itself split into hundres or thousands different sects. | 7 | dropped | The reference text mentions Protestantism splitting into 'hundreds or thousands different sects' but the claim misspells 'hundres' which does not appear in the reference text. |
| 4 | Jesus of Nazareth was a Jewish preacher. | 3 | carried in part | 'Jesus of Nazareth, a Jewish preacher' in `merged.md` -- The reference text calls Jesus a Jewish preacher in one version but a Jewish rabbi in another version, presenting conflicting descriptions. |
| 8 | Christianity's central beliefs include the Trinity (God as Father, Son (Jesus), and the Holy Spirit). | 5 | carried in part | 'the Trinity (God as Father, Son (Jesus), and the Holy Spirit)' in `merged.md` -- One version specifies Son as Jesus in parentheses; another version lists Father, Son, and Holy Spirit without the clarification, so the full claim details are partially stated. |
| 12 | The Bible is made up of the Old (Hebrew) and New (Greek) Testaments. | 7 | carried in part | 'made up of the Old (Hebrew) and New (Greek) Testaments' in `merged.md` -- One version includes the language specifications (Hebrew and Greek) in parentheses; another omits them, so the claim's detailed specifications are only partially stated. |
| 15 | Core Christian practices include the Eucharist (communion) commemorating Jesus' last supper. | 7 | carried in part | "the Eucharist (communion) commemorating Jesus' last supper" in `merged.md` -- The claim specifies Jesus' last supper; one version adds 'with his disciples' but the basic claim is supported by the shorter version. |
| 1 | Christianity is the world's largest religion. | 3 | carried | "Christianity is the world's largest religion" in `merged.md` -- The reference text explicitly states this claim in its opening sentence. |
| 2 | Christianity has over two billion adherents. | 3 | carried | 'with over two billion adherents' in `merged.md` -- The reference text states Christianity has over two billion adherents in the first sentence. |
| 3 | Christianity began in the first century. | 3 | carried | 'it began in the first century with Jesus of Nazareth' in `merged.md` -- The reference text explicitly states Christianity began in the first century. |
| 5 | Jesus of Nazareth was crucified in Jerusalem around AD 30-33. | 3 | carried | 'crucified in Jerusalem around AD 30-33' in `merged.md` -- The reference text states Jesus was crucified in Jerusalem around AD 30-33. |
| 6 | The followers of Jesus proclaimed that he rose from the dead. | 3 | carried | 'whose followers proclaimed that he rose from the dead' in `merged.md` -- The reference text explicitly states that followers proclaimed Jesus rose from the dead. |
| 7 | Christianity's central beliefs include monotheism. | 5 | carried | 'Its central beliefs are monotheism' in `merged.md` -- The reference text explicitly lists monotheism as one of Christianity's central beliefs. |
| 9 | Christianity's central beliefs include the incarnation and divinity of Jesus. | 5 | carried | 'the incarnation and divinity of Jesus' in `merged.md` -- The reference text explicitly lists incarnation and divinity of Jesus as central beliefs. |
| 10 | Christianity's central beliefs include salvation by God's grace through faith in Christ's death and resurrection. | 5 | carried | "salvation by God's grace through faith in Christ's death and resurrection" in `merged.md` -- The reference text explicitly states this as a central belief of Christianity. |
| 11 | The sacred text of Christianity is the Bible. | 7 | carried | 'Its sacred text is the Bible' in `merged.md` -- The reference text explicitly identifies the Bible as Christianity's sacred text. |
| 13 | Christians regard the Bible as the inspired and authoritative Word of God. | 7 | carried | 'which Christians regard as the inspired and authoritative Word of God' in `merged.md` -- The reference text explicitly states Christians regard the Bible as the inspired and authoritative Word of God. |
| 14 | Core Christian practices include baptism as a rite of initiation. | 7 | carried | 'baptism as a rite of initiation' in `merged.md` -- The reference text explicitly lists baptism as a rite of initiation among core Christian practices. |
| 16 | Core Christian practices include prayer. | 7 | carried | 'prayer' in `merged.md` -- The reference text explicitly lists prayer as a core Christian practice. |
| 17 | Core Christian practices include communal worship in a church. | 7 | carried | 'communal worship in a church' in `merged.md` -- The reference text explicitly lists communal worship in a church as a core Christian practice. |
| 18 | Over the centuries Christianity divided into three main branches - Catholicism, Eastern Orthodoxy, and Protestantism. | 7 | carried | 'the faith divided into three main branches - Catholicism, Eastern Orthodoxy, and Protestantism' in `merged.md`, **transcription_error** -- The reference text explicitly states Christianity divided into these three main branches. |
| 19 | Eastern Orthodoxy split in the East-West Schism of 1054. | 7 | carried | 'Eastern Orthodoxy (split in the East-West Schism of 1054)' in `merged.md` -- The reference text explicitly states Eastern Orthodoxy split in the East-West Schism of 1054. |
| 20 | Protestantism emerged from the 16th-century Reformation. | 7 | carried | 'Protestantism (emerging from the 16th-century Reformation' in `merged.md` -- The reference text explicitly states Protestantism emerged from the 16th-century Reformation. |
| 22 | Christianity is growing fastest in Africa and Asia. | 7 | carried | 'today it is growing fastest in Africa and Asia' in `merged.md` -- The reference text explicitly states Christianity is growing fastest in Africa and Asia. |
| 23 | Christianity is declining in much of the Western world. | 7 | carried | 'while declining in much of the Western world' in `merged.md` -- The reference text explicitly states Christianity is declining in much of the Western world. |

### `source_b.md` -- 23 claim(s): 0 dropped, 0 contradicted, 0 carried in part, 23 carried

Each claim below was read against `merged.md`.

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| 1 | Christianity is the world's largest religion. | 3 | carried | "Christianity is the world's largest religion" in `merged.md` -- The reference text explicitly states this claim in its opening sentence. |
| 2 | Christianity has over 2,000,000,000 followers. | 3 | carried | 'with over 2,000,000,000 followers' in `merged.md` -- The reference text states Christianity has over 2,000,000,000 followers in one of its opening sentences. |
| 3 | Christianity began in the first century. | 3 | carried | 'it began in the first century with Jesus of Nazareth' in `merged.md` -- The reference text explicitly states that Christianity began in the first century. |
| 4 | Jesus of Nazareth was a Jewish rabbi. | 3 | carried | 'Jesus of Nazareth, a Jewish rabbi who was crucified in Jerusalem' in `merged.md` -- The reference text identifies Jesus of Nazareth as a Jewish rabbi. |
| 5 | Jesus of Nazareth was crucified in Jerusalem around AD 30–33. | 3 | carried | 'crucified in Jerusalem around AD 30–33' in `merged.md` -- The reference text states Jesus was crucified in Jerusalem around AD 30–33. |
| 6 | Followers of Jesus proclaimed that he arose from the dead. | 3 | carried | 'whose followers proclaimed that he arose from the dead' in `merged.md` -- The reference text states followers proclaimed that Jesus arose from the dead. |
| 7 | Central beliefs of Christianity include monotheism. | 5 | carried | 'Its central beliefs are monotheism, the Trinity' in `merged.md` -- The reference text lists monotheism as one of the central beliefs of Christianity. |
| 8 | Central beliefs of Christianity include the Trinity (God as Father, Son, and Holy Spirit). | 5 | carried | 'the Trinity (God as Father, Son, and Holy Spirit)' in `merged.md` -- The reference text identifies the Trinity as a central belief with the exact composition claimed. |
| 9 | Central beliefs of Christianity include the incarnation and divinity of Jesus. | 5 | carried | 'the incarnation and divinity of Jesus' in `merged.md` -- The reference text lists the incarnation and divinity of Jesus as central beliefs. |
| 10 | Central beliefs of Christianity include salvation by God's grace through faith in Christ's death and resurrection. | 5 | carried | "salvation by God's grace through faith in Christ's death and resurrection" in `merged.md` -- The reference text states this as a central belief of Christianity. |
| 11 | The sacred text of Christianity is the Bible. | 7 | carried | 'Its sacred text is the Bible' in `merged.md` -- The reference text directly states the Bible is the sacred text of Christianity. |
| 12 | The Bible is made up of the Old and New Testaments. | 7 | carried | 'made up of the Old and New Testaments' in `merged.md` -- The reference text states the Bible is made up of the Old and New Testaments. |
| 13 | Christians regard the Bible as the inspired and authoritative Word of God. | 7 | carried | 'which Christians regard as the inspired and authoritative Word of God' in `merged.md` -- The reference text states Christians regard the Bible as the inspired and authoritative Word of God. |
| 14 | Baptism is a core practice of Christianity as a rite of initiation. | 7 | carried | 'baptism as a rite of initiation' in `merged.md` -- The reference text identifies baptism as a core practice and rite of initiation. |
| 15 | The Eucharist (communion) is a core practice of Christianity commemorating Jesus' last supper with his diciples. | 7 | carried | "the Eucharist (communion) commemorating Jesus' last supper with his disciples" in `merged.md` -- The reference text states the Eucharist commemorates Jesus' last supper with his disciples. |
| 16 | Prayer is a core practice of Christianity. | 7 | carried | 'prayer, and communal worship' in `merged.md` -- The reference text lists prayer as a core practice of Christianity. |
| 17 | Communal worship in a church is a core practice of Christianity. | 7 | carried | 'communal worship in a church' in `merged.md` -- The reference text identifies communal worship in a church as a core practice. |
| 18 | Christianity divided over the centuries into three main branches. | 7 | carried | 'the faith divided into three main branches' in `merged.md` -- The reference text states Christianity divided into three main branches over the centuries. |
| 19 | The three main branches of Christianity are Catholicism, Eastern Orthodoxy, and Protestantism. | 7 | carried | 'Catholicism, Eastern Orthodoxy, and Protestantism' in `merged.md`, **transcription_error** -- The reference text identifies these as the three main branches of Christianity. |
| 20 | Eastern Orthodoxy split from Christianity in the East–West Schism of 1054. | 7 | carried | 'Eastern Orthodoxy (split in the East–West Schism of 1054)' in `merged.md` -- The reference text states Eastern Orthodoxy split in the East–West Schism of 1054. |
| 21 | Protestantism emerged from the 16th-century Reformation. | 7 | carried | 'Protestantism (emerging from the 16th-century Reformation)' in `merged.md` -- The reference text states Protestantism emerged from the 16th-century Reformation. |
| 22 | Christianity is growing fastest in Africa and Asia. | 7 | carried | 'today it is growing fastest in Africa and Asia' in `merged.md` -- The reference text states Christianity is growing fastest in Africa and Asia. |
| 23 | Christianity is declining in much of the West. | 7 | carried | 'while declining in much of the West' in `merged.md` -- The reference text states Christianity is declining in much of the West. |

### `merged.md` -- 31 claim(s): 0 invented, 0 contradicted, 0 supported in part, 31 supported

Each claim below was read against `source_a.md` and `source_b.md`.

| # | Claim | Status | Found in | Note |
|---|---|---|---|---|
| 1 | Christianity is the world's largest religion, with over two billion adherents. | supported | `source_a.md` | "Christianity is the world's largest religion, with over two billion adherents" in `source_a.md` -- Source A states this claim directly using identical phrasing and numbers. |
| 2 | Christianity began in the first century with Jesus of Nazareth, a Jewish preacher crucified in Jerusalem around AD 30-33. | supported | `source_a.md` | 'it began in the first century with Jesus of Nazareth, a Jewish preacher crucified in Jerusalem around AD 30-33, whose followers proclaimed that he rose from the dead' in `source_a.md` -- Source A states this claim directly with the same wording and date format. |
| 3 | Followers of Jesus proclaimed that he rose from the dead. | supported | `source_a.md` | 'whose followers proclaimed that he rose from the dead' in `source_a.md` -- Source A states this claim directly in identical words. |
| 4 | Christianity is the world's largest religion, with over 2,000,000,000 followers. | supported | `source_b.md` | "Christianity is the world's largest religion, with over 2,000,000,000 followers" in `source_b.md` -- Source B states this claim directly using the same meaning and numerical format. |
| 5 | Christianity began in the first century with Jesus of Nazareth, a Jewish rabbi who was crucified in Jerusalem around AD 30–33. | supported | `source_b.md` | 'it began in the first century with Jesus of Nazareth, a Jewish rabbi who was crucified in Jerusalem around AD 30–33, whose followers proclaimed that he arose from the dead' in `source_b.md` -- Source B states this claim directly with identical phrasing and date format. |
| 6 | Followers of Jesus proclaimed that he arose from the dead. | supported | `source_b.md` | 'whose followers proclaimed that he arose from the dead' in `source_b.md` -- Source B states this claim directly in identical words. |
| 7 | Central Christian beliefs include monotheism, the Trinity (God as Father, Son (Jesus), and the Holy Spirit), the incarnation and divinity of Jesus, and salvation by God's grace through faith in Christ's death and resurrection. | supported | `source_a.md` | "Its central beliefs are monotheism, the Trinity (God as Father, Son (Jesus), and the Holy Spirit), the incarnation and divinity of Jesus, and salvation by God's grace through faith in Christ's death and resurrection" in `source_a.md` -- Source A states this claim directly using identical phrasing and notation. |
| 8 | Central Christian beliefs include monotheism, the Trinity (God as Father, Son, and Holy Spirit), the incarnation and divinity of Jesus, and salvation by God's grace through faith in Christ's death and resurrection. | supported | `source_b.md` | "Its central beliefs are monotheism, the Trinity (God as Father, Son, and Holy Spirit), the incarnation and divinity of Jesus, and salvation by God's grace through faith in Christ's death and resurrection" in `source_b.md` -- Source B states this claim directly using identical phrasing and notation. |
| 9 | The sacred text of Christianity is the Bible, made up of the Old (Hebrew) and New (Greek) Testaments. | supported | `source_a.md` | 'Its sacred text is the Bible, made up of the Old (Hebrew) and New (Greek) Testaments' in `source_a.md` -- Source A states this claim directly with identical phrasing and language notations. |
| 10 | Christians regard the Bible as the inspired and authoritative Word of God. | supported | `source_a.md` | 'which Christians regard as the inspired and authoritative Word of God' in `source_a.md` -- Source A states this claim directly in identical words. |
| 11 | The sacred text of Christianity is the Bible, made up of the Old and New Testaments. | supported | `source_b.md` | 'Its sacred text is the Bible, made up of the Old and New Testaments' in `source_b.md` -- Source B states this claim directly with identical phrasing. |
| 12 | Christians regard the Bible as the inspired and authoritative Word of God. | supported | `source_b.md` | 'which Christians regard as the inspired and authoritative Word of God' in `source_b.md` -- Source B states this claim directly in identical words. |
| 13 | Core Christian practices include baptism as a rite of initiation. | supported | `source_a.md` | 'Core practices include baptism as a rite of initiation' in `source_a.md` -- Source A states this claim directly in identical words. |
| 14 | Core Christian practices include the Eucharist (communion) commemorating Jesus' last supper. | supported | `source_a.md` | "the Eucharist (communion) commemorating Jesus' last supper" in `source_a.md` -- Source A states this claim directly in identical words. |
| 15 | Core Christian practices include prayer. | supported | `source_a.md` | 'prayer' in `source_a.md` -- Source A lists prayer as a core practice in identical words. |
| 16 | Core Christian practices include communal worship in a church. | supported | `source_a.md` | 'communal worship in a church' in `source_a.md` -- Source A states this claim directly in identical words. |
| 17 | Core Christian practices include baptism as a rite of initiation. | supported | `source_b.md` | 'Core practices include baptism as a rite of initiation' in `source_b.md` -- Source B states this claim directly in identical words. |
| 18 | Core Christian practices include the Eucharist (communion) commemorating Jesus' last supper with his disciples. | supported | `source_b.md` | "the Eucharist (communion) commemorating Jesus' last supper with his diciples" in `source_b.md` -- Source B states this claim directly with identical phrasing (preserving the spelling error 'diciples'). |
| 19 | Core Christian practices include prayer. | supported | `source_b.md` | 'prayer' in `source_b.md` -- Source B lists prayer as a core practice in identical words. |
| 20 | Core Christian practices include communal worship in a church. | supported | `source_b.md` | 'communal worship in a church' in `source_b.md` -- Source B states this claim directly in identical words. |
| 21 | Over the centuries Christianity divided into three main branches: Catholicism, Eastern Orthodoxy, and Protestantism. | supported | `source_a.md` | 'the faith divided into three main branches - Catholicism, Eastern Orthodoxy (split in the East-West Schism of 1054), and Protestantism' in `source_a.md` -- Source A states this claim directly, listing the three branches in identical form. |
| 22 | Eastern Orthodoxy split in the East-West Schism of 1054. | supported | `source_a.md` | 'Eastern Orthodoxy (split in the East-West Schism of 1054)' in `source_a.md` -- Source A states this claim directly in identical words. |
| 23 | Protestantism emerged from the 16th-century Reformation. | supported | `source_a.md` | 'Protestantism (emerging from the 16th-century Reformation' in `source_a.md` -- Source A states this claim directly in identical words. |
| 24 | Protestantism itself split into hundreds or thousands different sects. | supported | `source_a.md` | 'and itself split into hundres or thousands different sects' in `source_a.md` -- Source A states this claim directly in identical words (preserving the spelling error 'hundres'). |
| 25 | Christianity is growing fastest in Africa and Asia. | supported | `source_a.md` | 'today it is growing fastest in Africa and Asia' in `source_a.md` -- Source A states this claim directly in identical words. |
| 26 | Christianity is declining in much of the Western world. | supported | `source_a.md` | 'declining in much of the Western world' in `source_a.md` -- Source A states this claim directly in its final sentence about Christianity's current growth and decline patterns. |
| 27 | Over the centuries Christianity divided into three main branches: Catholicism, Eastern Orthodoxy, and Protestantism. | supported | `source_a.md` | 'the faith divided into three main branches - Catholicism, Eastern Orthodoxy (split in the East-West Schism of 1054), and Protestantism' in `source_a.md` -- Source A explicitly states that Christianity divided into these three main branches over the centuries. |
| 28 | Eastern Orthodoxy split in the East–West Schism of 1054. | supported | `source_a.md` | 'Eastern Orthodoxy (split in the East-West Schism of 1054)' in `source_a.md` -- Source A directly states that Eastern Orthodoxy split in the East-West Schism of 1054. |
| 29 | Protestantism emerged from the 16th-century Reformation. | supported | `source_a.md` | 'Protestantism (emerging from the 16th-century Reformation' in `source_a.md` -- Source A explicitly states that Protestantism emerged from the 16th-century Reformation. |
| 30 | Christianity is growing fastest in Africa and Asia. | supported | `source_a.md` | 'today it is growing fastest in Africa and Asia' in `source_a.md` -- Source A directly states that Christianity is growing fastest in Africa and Asia today. |
| 31 | Christianity is declining in much of the West. | supported | `source_b.md` | 'declining in much of the West' in `source_b.md` -- Source B states this claim in its final sentence, using 'the West' as a synonym for 'the Western world'. |

## Provenance

| | |
|---|---|
| Run mode | live |
| Endpoint | ec0c9ecb43e3 (hosted) |
| Fidelity | high |
| Verification depth | full |
| Title policy | synthesise |
| Base document | none — this run made no merge |
| Model (decompose) | claude-haiku-4-5-20251001 |
| Model (verify) | claude-haiku-4-5-20251001 |
| Structured output | prompt (pinned) |
| Decoding | temperature not sent, seed not sent, thinking decompose, merge, verify, profile anthropic, effort decompose one level (extended thinking on/off; default kept), verify one level (extended thinking on/off; default kept) |
| Context window | 200000 tokens, declared by --window / LLOSSLESS_WINDOW; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it (decompose, verify) |
| LLossless commit | 73b61563c13c |
| Calls | 8 live, 0 cached, 0 replayed |
| Tokens | 18,016 in, 12,889 out |
| Cost | ~$0.08 estimated (rates read 2026-08-31) |
| Schema repairs | 1 |
| Errors | 0 |
| Duration | 89.4s |
| Generated | 2026-09-27T17:43:39+00:00 |
| Prompt | `prompts/decompose.md` `b4ec1e0c7ead` |
| Prompt | `prompts/verify.md` `af6354d0b620` |
| Prompt | `prompts/verify_reverse.md` `c24eb04c5375` |

> **Document content left this machine.** It was sent to the endpoint in `LLOSSLESS_BASE_URL` (id `ec0c9ecb43e3`), which is not a local address. Run against a local endpoint if that is not acceptable for the documents involved.

> **The context window was stated, not measured, for decompose, verify.** 200000 tokens, declared by --window / llossless_window; no probe was sent, so this figure is the operator's statement about the endpoint and not a measurement of it. The rendered prompt was checked against that figure before each call, so a prompt too large for it was refused rather than sent -- but nothing here confirmed the figure itself, and if the endpoint serves less than was declared, an overrun is trimmed from the front and answered exactly as it would be with no guard at all. This is what a vendor endpoint with no /api/ps route can be given; it is weaker than what a local endpoint is measured against.
