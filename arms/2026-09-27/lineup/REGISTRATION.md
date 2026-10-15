### Lineup snapshot, registered 2026-09-27

```
Question:        On identical documents and settings, what does each model in
                 the frozen lineup do in a faithful merge, what does it detect,
                 which planted errors does it fix, and what does a merge cost?
Arms:
                 - opus-5.5-api: claude-opus-5-5 via http (anthropic), effort vendor default, thinking ['decompose', 'merge', 'verify'], window 200000, sets ['S1', 'S2', 'S3']
                 - sonnet-5-api: claude-sonnet-5 via http (anthropic), effort vendor default, thinking ['decompose', 'merge', 'verify'], window 200000, sets ['S1', 'S2', 'S3']
                 - haiku-4.5-api: claude-haiku-4-5-20251001 via http (anthropic), effort one level (extended thinking on/off; default kept), thinking ['decompose', 'merge', 'verify'], window 200000, sets ['S1', 'S2', 'S3']
                 - gpt-6-sol-api: gpt-6-sol via http (openai-reasoning), effort vendor default, thinking ['decompose', 'merge', 'verify'], window 200000, sets ['S1', 'S2', 'S3']
                 - gpt-6-luna-api: gpt-6-luna via http (openai-reasoning), effort vendor default, thinking ['decompose', 'merge', 'verify'], window 200000, sets ['S1', 'S2', 'S3']
                 - opus-5.5-sub: claude-opus-5-5 via claude (subscription), effort medium on every role (CLI), thinking ['decompose', 'merge', 'verify'], window 200000, sets ['S1', 'S2', 'S3']
                 - sonnet-5-sub: claude-sonnet-5 via claude (subscription), effort medium on every role (CLI), thinking ['decompose', 'merge', 'verify'], window 200000, sets ['S1', 'S2', 'S3']
                 - haiku-4.5-sub: claude-haiku-4-5-20251001 via claude (subscription), effort one level (extended thinking on/off; default kept), thinking ['decompose', 'merge', 'verify'], window 200000, sets ['S1', 'S2', 'S3']
                 - fable-sub: fable via claude (subscription), effort medium on every role (CLI), thinking ['decompose', 'merge', 'verify'], window 200000, sets ['S1', 'S3'], not in the headline
Control:         none is privileged; every arm runs in this window, pair-major.
Held constant:   tool pin 73b61563c13c789a55b8150a16fee6ceca9e0398; input sha256 list (run.json, written at the
                 first start); --base source_a.md; --title-policy synthesise;
                 --verify-depth full; tier prompt pinned;
                 --timeout 1800; --no-cache; safe mode on every claude call;
                 CLI 2.1.283 sha256 1859583ce32920595c61ef868bee52e1b1594f7486db209935e01f1e5e804ae2
Not held:        1. route; 2. verify batch 25/100; 3. sampling (OpenAI draws share
                 seed 0, best-effort determinism; other vendors sample
                 independently); 4. stated window; 5. field order (27B any);
                 6. effort level per vendor; 7. route overhead in seconds;
                 8. mahjongg is German.
Exclusions:      678: blank, timeout and platform failures excluded and retried
                 in later passes; retries not counted in speed or cost; a retry
                 reuses the cell's own earlier live answers, each counted once at
                 its original time and cost (688). Still failing after every
                 pass: one cheap cell (S1:badge_access) on the row's
                 reference route; it works, so the cell is the row's
                 endpoint_failure; it fails too, so the lane pauses and probes
                 (infrastructure, never scored) and runs the cell again (688).
                 A refusal (flagged "refused (prompt or guardrail)") and an
                 unruled cell (a model failure on a vendor row; limit or config
                 on a self-hosted row) count against the row (688); rules {"refusal_counts": "row"}.
Common pairs:    every registered pair; nothing shrinks it (688). A row missing a
                 pair, for its own reason or not measured, is listed after every
                 complete row with why
Baselines:       byte-concatenation, a mechanical union and base-only, on the
                 common pairs, by the same scorer (plan 4)
Budget:          caps {"anthropic": 36.0, "openai": 10.0, "overall": 46.0}; subscription meter recorded by `note` at the lane's start and end; the meter is
                 shared with the coordinating session, so its delta is an upper bound, never
                 the lane's measure (per-row use is the reports' API-equivalent)
May be used for: plan section 9.2; not for section 9.3
Pilot:           <home>/Documents/Dev/claude-tmp/claimcheck/2026-09-27-release-pilot/PILOT-REPORT.md
                 (25 cells ok, no defect, pin kept). Lanes split by vendor so OpenAI runs
                 first (operator, 2026-09-27). Gemini 3.8 Flash runs in its own best-effort
                 lane (693). Fable (678): the hardest documents, where the frontier rows
                 visibly struggle: S1 rate_limits (the largest pair) and S3 voyager, bip39,
                 mahjongg, one draw each. Anthropic cap provisional pending the operator's
                 answer on the re-scaled estimate (pilot: Sonnet 5 API +29%).
```

Amendments go below the machine block, dated, each before the calls it governs.

```json lineup-registration
{
 "registration": 1,
 "name": "fair lineup snapshot",
 "pin": "73b61563c13c789a55b8150a16fee6ceca9e0398",
 "clone": "tree",
 "settings": {
  "timeout": 1800,
  "structured": "prompt",
  "title_policy": "synthesise",
  "verify_depth": "full",
  "base": "source_a.md",
  "max_calls": 400,
  "cell_wall_seconds": 14400
 },
 "sets": {
  "S1": {
   "kind": "merge",
   "score": "pairs",
   "root": "tests/pairs",
   "fidelity": "high",
   "items": [
    "badge_access",
    "bike_docks",
    "freezer_alarm",
    "index_429",
    "library_holds",
    "loading_dock",
    "payroll_cutoff",
    "rate_limits",
    "trace_names"
   ],
   "draws": {
    "default": 1,
    "badge_access": 3,
    "trace_names": 3,
    "rate_limits": 3
   }
  },
  "S2": {
   "kind": "detect",
   "score": "detect",
   "root": "tests/fixtures",
   "items": [
    "attribution_invented",
    "attribution_swapped",
    "conflict_surfaced",
    "contradiction",
    "dedup",
    "disjoint_domains",
    "disjoint_sources",
    "dropped_claim",
    "hallucination",
    "numeric_drift",
    "ordering_only",
    "paraphrase",
    "structure_added",
    "concatenated",
    "restated",
    "list_structure"
   ],
   "draws": {
    "default": 1
   },
   "headline_items": [
    "attribution_invented",
    "attribution_swapped",
    "conflict_surfaced",
    "contradiction",
    "dedup",
    "disjoint_domains",
    "disjoint_sources",
    "dropped_claim",
    "hallucination",
    "numeric_drift",
    "ordering_only",
    "paraphrase",
    "structure_added"
   ]
  },
  "S3": {
   "kind": "merge",
   "score": "planted",
   "root": "tests/handwritten",
   "fidelity": "open",
   "items": [
    "voyager",
    "bip39",
    "mahjongg"
   ],
   "draws": {
    "default": 1,
    "voyager": 3,
    "bip39": 3
   }
  }
 },
 "caps": {
  "anthropic": 37.0,
  "openai": 10.0,
  "overall": 47.0
 },
 "margin": 1.25,
 "retry": {
  "passes": 2,
  "spacing_seconds": 1800,
  "breaker": 3
 },
 "rules": {
  "refusal_counts": "row"
 },
 "reference_item": "S1:badge_access",
 "references": [
  {
   "id": "luna-ref",
   "model": "gpt-6-luna",
   "vendor": "openai",
   "hosting": "vendor",
   "route": {
    "kind": "http",
    "base_url": "https://api.openai.com/v1",
    "key_env": "OPEN_AI_API_KEY",
    "profile": "openai-reasoning"
   },
   "effort": "vendor_default",
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "cell_estimate_usd": 0.05
  },
  {
   "id": "haiku-ref",
   "model": "claude-haiku-4-5-20251001",
   "vendor": "anthropic",
   "hosting": "vendor",
   "route": {
    "kind": "http",
    "base_url": "https://api.anthropic.com/v1",
    "key_env": "ANTHROPIC_API_KEY",
    "profile": "anthropic"
   },
   "effort": "single_level",
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "cell_estimate_usd": 0.1
  }
 ],
 "infrastructure": {
  "probe_urls": [
   "https://api.anthropic.com/v1/models",
   "https://api.openai.com/v1/models"
  ],
  "probe_intervals_seconds": [
   120,
   120,
   120,
   300
  ],
  "max_pause_seconds": 43200
 },
 "claude": {
  "path": "cli/claude",
  "sha256": "1859583ce32920595c61ef868bee52e1b1594f7486db209935e01f1e5e804ae2",
  "version": "2.1.283"
 },
 "lanes": {
  "openai": {},
  "anthropic": {},
  "subscription": {},
  "fable": {}
 },
 "rows": [
  {
   "id": "opus-5.5-api",
   "model": "claude-opus-5-5",
   "lane": "anthropic",
   "vendor": "anthropic",
   "hosting": "vendor",
   "route": {
    "kind": "http",
    "base_url": "https://api.anthropic.com/v1",
    "key_env": "ANTHROPIC_API_KEY",
    "profile": "anthropic"
   },
   "effort": "vendor_default",
   "effort_documented": "medium (vendor page, read 2026-09-25)",
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "sets": [
    "S1",
    "S2",
    "S3"
   ],
   "cell_estimate_usd": 1.5,
   "reference": "luna-ref"
  },
  {
   "id": "sonnet-5-api",
   "model": "claude-sonnet-5",
   "lane": "anthropic",
   "vendor": "anthropic",
   "hosting": "vendor",
   "route": {
    "kind": "http",
    "base_url": "https://api.anthropic.com/v1",
    "key_env": "ANTHROPIC_API_KEY",
    "profile": "anthropic"
   },
   "effort": "vendor_default",
   "effort_documented": "high (vendor page <redacted> read 2026-09-27)",
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "sets": [
    "S1",
    "S2",
    "S3"
   ],
   "cell_estimate_usd": 1.0,
   "reference": "luna-ref",
   "draws": {
    "S1": {
     "default": 1
    }
   }
  },
  {
   "id": "haiku-4.5-api",
   "model": "claude-haiku-4-5-20251001",
   "lane": "anthropic",
   "vendor": "anthropic",
   "hosting": "vendor",
   "route": {
    "kind": "http",
    "base_url": "https://api.anthropic.com/v1",
    "key_env": "ANTHROPIC_API_KEY",
    "profile": "anthropic"
   },
   "effort": "single_level",
   "effort_documented": "one level (extended thinking on/off; default kept)",
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "sets": [
    "S1",
    "S2",
    "S3"
   ],
   "cell_estimate_usd": 0.3,
   "reference": "luna-ref",
   "draws": {
    "S1": {
     "default": 1
    }
   }
  },
  {
   "id": "gpt-6-sol-api",
   "model": "gpt-6-sol",
   "lane": "openai",
   "vendor": "openai",
   "hosting": "vendor",
   "route": {
    "kind": "http",
    "base_url": "https://api.openai.com/v1",
    "key_env": "OPEN_AI_API_KEY",
    "profile": "openai-reasoning"
   },
   "effort": "vendor_default",
   "effort_documented": "medium (model page, read 2026-09-25)",
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "sets": [
    "S1",
    "S2",
    "S3"
   ],
   "cell_estimate_usd": 0.8,
   "reference": "haiku-ref"
  },
  {
   "id": "gpt-6-luna-api",
   "model": "gpt-6-luna",
   "lane": "openai",
   "vendor": "openai",
   "hosting": "vendor",
   "route": {
    "kind": "http",
    "base_url": "https://api.openai.com/v1",
    "key_env": "OPEN_AI_API_KEY",
    "profile": "openai-reasoning"
   },
   "effort": "vendor_default",
   "effort_documented": "medium (model page, read 2026-09-25)",
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "sets": [
    "S1",
    "S2",
    "S3"
   ],
   "cell_estimate_usd": 0.1,
   "reference": "haiku-ref"
  },
  {
   "id": "opus-5.5-sub",
   "model": "claude-opus-5-5",
   "lane": "subscription",
   "vendor": "subscription",
   "hosting": "vendor",
   "metered": false,
   "route": {
    "kind": "claude",
    "profile": "subscription"
   },
   "effort": {
    "decompose": "medium",
    "merge": "medium",
    "verify": "medium"
   },
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "sets": [
    "S1",
    "S2",
    "S3"
   ],
   "reference": "luna-ref"
  },
  {
   "id": "sonnet-5-sub",
   "model": "claude-sonnet-5",
   "lane": "subscription",
   "vendor": "subscription",
   "hosting": "vendor",
   "metered": false,
   "route": {
    "kind": "claude",
    "profile": "subscription"
   },
   "effort": {
    "decompose": "medium",
    "merge": "medium",
    "verify": "medium"
   },
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "sets": [
    "S1",
    "S2",
    "S3"
   ],
   "reference": "luna-ref"
  },
  {
   "id": "haiku-4.5-sub",
   "model": "claude-haiku-4-5-20251001",
   "lane": "subscription",
   "vendor": "subscription",
   "hosting": "vendor",
   "metered": false,
   "route": {
    "kind": "claude",
    "profile": "subscription"
   },
   "effort": "single_level",
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "sets": [
    "S1",
    "S2",
    "S3"
   ],
   "reference": "luna-ref",
   "effort_note": "one level (extended thinking on/off; default kept): no --effort is passed (688, ruling 11)"
  },
  {
   "id": "fable-sub",
   "model": "fable",
   "lane": "fable",
   "vendor": "subscription",
   "hosting": "vendor",
   "metered": false,
   "route": {
    "kind": "claude",
    "profile": "subscription"
   },
   "effort": {
    "decompose": "medium",
    "merge": "medium",
    "verify": "medium"
   },
   "thinking": [
    "decompose",
    "merge",
    "verify"
   ],
   "window": 200000,
   "field_order": "schema",
   "sets": [
    "S1",
    "S3"
   ],
   "reference": "luna-ref",
   "headline": false,
   "compare_with": "opus-5.5-sub",
   "unpriced": "Fable has no row in pricing.py; subscription only, never metered (678)",
   "items": {
    "S1": [
     "rate_limits",
     "index_429"
    ],
    "S3": [
     "voyager"
    ]
   },
   "served_aliases": [
    "claude-fable-5-1"
   ],
   "draws": {
    "S1": {
     "default": 1
    },
    "S3": {
     "default": 1
    }
   }
  }
 ],
 "env_file": "<home>/Documents/Dev/vibe-coding/claimcheck/.env"
}
```

**Amendment 1, 2026-09-27, before any Anthropic, subscription or Fable call.**
The operator's limits: Anthropic API "$37.01 and not a penny more"; OpenAI
balance $11.19; subscription at 59%; Fable runs last, and if the quota is spent
first, it does not run. The pilot re-scaled the Anthropic estimate to about $36
(Sonnet 5 API +29%). Changes:
- The plan's registered cheaper variant (6.2): no spread draws for
  sonnet-5-api and haiku-4.5-api (S1 one draw per pair). That is 12 fewer
  cells, and the estimate becomes about $32.
- caps: anthropic 37.00, openai 10.00, overall 47.00.
- fable-sub moves to its own lane `fable`, started only after the subscription
  lane ends.

**Amendment 2, 2026-09-27, before any Fable call.** The operator: Fable only on the hardest 2-3 documents, "no need to test anything that Opus already beats"; Fable exists to check what Opus fails. Chosen from opus-5.5-api's counted results, which the lane had already finished:
- S1 `rate_limits`: 10-15 lost, 12-14 bloat, and Opus's only silent loss.
- S1 `index_429`: 10 lost, against Sol's 4.
- S3 `voyager`: 28-32 of 44 fixed.

Dropped:
- S3 `bip39`: Opus fixes 13 of 14.
- S3 `mahjongg`: 0 false corrections.

One draw each. The items were chosen after seeing Opus's results, by design (678). Fable's single draw counts as a gain only where it lies outside Opus's range over its draws.


**Amendment 3, 2026-10-12, after every call of this registration and after its results were published. It governs no call. It changes how a finished merge is scored, and it is made knowing the results.** The registration says an amendment goes "before the calls it governs". This one cannot: the reason for it was found by reading the results. An audit by meaning of the silent losses this lineup counted (2026-10-12) found that most of them are content the merge still has. The scorer's rule calls a source segment "absent" when its text is not in the merge word for word and no single merge segment is at least 0.68 similar to it (`reconcile.NEAR_MATCH`, `rank_matrix.sets`). Three things make that rule call present content gone:
- A sentence kept word for word and joined to its neighbour with a semicolon, a colon or a comma. The search includes the sentence's full stop and misses, and the similarity of a text of length m inside one of length M is at most 2m/(m+M), which cannot reach 0.68 against a long joined sentence.
- A sentence spread over two merge sentences, or two run into one. The similarity is taken against one merge segment at a time.
- A heading the merge did not take because it took the other source's heading for the same section. A heading is looked for only among the merge's headings.

Silent loss is this benchmark's disqualifying figure, so a miscount of it is a miscount of the ranking. The amended rule was designed by a separate run of an AI model (Claude Opus) that was not given the lineup's outputs or the audit. It was fixed in writing before it was run on the nine pairs (2026-10-12 07:32 CEST) and was changed twice after that, both times to make it stricter: step (2) below takes one unbroken run where the first version allowed two, and a heading whose whole section is lost with it stays lost content. It was then evaluated against the audit by the session that coordinates this work and not by its designer.

The rule as amended. Its full definition is the function `reconcile.locate` under the rule `amended`, with `reconcile.is_silent_loss` for headings (`src/llossless/reconcile.py`), and its limits are pinned case by case in `tests/test_amended_rule.py`. This is its substance.
- Whatever the registered rule calls carried or reworded stays that. The amendment looks only at a segment the registered rule calls absent, and can only move it to "reworded". No segment moves the other way, so no cell can gain a silent loss.
- A sentence, list item or table row that the registered rule calls absent is "reworded" if its words still stand in the merge as one unbroken run, in order: (1) every word, punctuation and capitals ignored, for a segment of at least 2 words; or (2) for a segment of at least 4 content words, every content word, inside 2 neighbouring merge segments, together with every number, link, path, version and code value the segment carries. In (2), 21 English connecting words may be missing or added: a, an, the, and, am, is, are, was, were, be, been, being, it, they, them, this, that, these, those, which, who. No other word may be missing and no other word may stand inside the run. The run is looked for in the merge's sentences, list items and table rows only, never across a heading or a code block.
- A source heading that the registered rule calls absent stays absent. With no record it counts as silent loss only if it carries a number, link or code value the merge does not have, or if every segment of its section is itself absent with no record. Otherwise it is counted in a column of its own, "untaken headings", which does not disqualify.
- Titles and fenced code blocks: as registered.
- "Kept" means one thing in the scorer, so the deviation figures (lost, bloat) are formed from the amended verdicts as well, for a model's merge and for the reference merge alike.
- Built after the draft of this amendment was written: the tool applies the same rule in its own check, and an untaken heading is a finding of its own there, "Heading dropped in silence", in the group of findings about the merge's records (exit code 3). The registered rule stays callable, so every figure of the scoring as run can still be re-derived.

The disqualifier, as the operator ruled on 2026-10-12 after the evaluation. A row is disqualified by audited loss on a first run, not by the program's count. The count of silent losses under the amended rule stays a column, as what it is: source segments the program could not find in the merge and that no record explains. A row is disqualified when the audit by reading found content gone, wholly or in part, among the segments counted for it on a first run, which is the lowest counted draw of each pair, the draw the order reads. The verdict is the first reading's; where a second reading of the same cases comes to the other verdict, the row is marked "readings disagree". On this lineup the disqualified rows are `haiku-4.5-api` and `haiku-4.5-sub`. The other rows are ordered by amended deviations per pair, then cost, then speed, a tie decided as registered: shared unless every row in it is list-priced. The amended scoring is the one shown first. The audit is published with this run, in `audit/`, with both readings, their agreement and their limits.

What stays as registered: the rows, sets, draws and pins; the exclusions and the common pairs; the baselines; the definition of silent loss as a source segment that is absent from the merge and has no record; that a title is left out of it; which declarations forgive a lost segment; the count of exact repeats; the order of the rows that are not disqualified (deviations, then cost, then speed); cost and seconds; S2 and S3, which this rule does not score. The registered similarity rule is not replaced: it still decides first.

Both scorings are published. Every figure of the registered scoring stays where it is, under that name: `scored.json`, and `S1_registered` in `figures.json`. The amended figures are published beside them for every row and every baseline (`scored-amended.json`, and `S1` in `figures.json`), with a list, per cell, of every segment whose count differs: the segment's text, the step that decided (1 or 2, or the heading rule), and the merge text it was found in (`differences.json`). Which of the two the README's table and the model picker show first is the operator's decision at adoption and is recorded here: the amended one.

The properties the amended scoring is expected to have, stated before it is run on the lineup's cells. A property that fails is reported with the cells and segments it fails on, and the amendment is not adopted in this form until that is resolved.
1. **No loss is cleared.** No segment that the audit of 2026-10-12 classed as gone, wholly or in part (a clause, a number, a name, a condition, a link, a responsibility no longer named), moves from silent loss to "reworded" or to "untaken heading".
2. **Only clearings.** In every cell the amended silent loss is at most the registered one. No segment is absent under the amended rule that is not absent under the registered rule. The set of carried segments is the same under both.
3. **The reference merges stay clean.** All nine have zero silent loss and zero untaken headings under both scorings (measured: 0 and 0).
4. **Concatenation and the mechanical union stay at zero silent loss** under both scorings (measured: 0 and 0 on all nine pairs).
5. **Base only keeps its losses.** Measured over the nine pairs: 129 silent losses registered, 121 amended. No sentence, list item or table row of source B is cleared against source A alone. The 8 that leave the count are headings of source B with at least one segment of their section in source A: `bike_docks` "Escalating E4"; `loading_dock` "Requesting a slot", "When to request", "On the day", "Late finishes"; `rate_limits` "What the client does", "Other kinds of refusal"; `trace_names` "Resolution". The 23 other source B headings that base only does not have stay silent losses, because their whole section is gone with them.
6. **Every clearing can be read.** Each cleared sentence is in the merge as one run of its own words; the published list shows the run. A reader who disagrees with a clearing can point at it.
7. **The band moves a little and in a known place.** In the reference merges one segment changes side: `bike_docks` b10, "If the field crew have already tried 3 times," whose words the reference keeps with a full stop where the source has a comma. It is "kept by the reference" under the amended rule. Measured consequence for the baselines: concatenation and union go from 65 bloat to 64, base only from 66 lost to 67. For the rows, lost and bloat may each move in either direction by a cell's cleared segments; they are published under both scorings.
8. **The registered rule's own clearings are untouched and are not vouched for.** A sentence that was cut short reads as "reworded" under the registered rule whenever a little more than half of it is left (0.68 = 2m/(m+M) at m/M = 0.515). The amendment neither adds to nor removes from that class. The published list marks every segment that is "reworded" by the similarity rule alone, so that it can be read.

**Outcome of the properties**, from the re-scoring of 2026-10-12. Every figure in this list is re-derived from the stored cells and `audit/audit.json` by `python3 tests/lineup_figures.py --check`, which fails if a line here no longer says what the cells give.
1. Holds. Of the 65 audited segments, the 2 classed gone and the 9 classed partly gone are still counted as silent loss (2 and 9). Of the 42 classed present, 34 are still counted and 8 are found as reworded; of the 12 classed not content, 12 are counted as untaken headings. On first runs: 3 of 3 partly gone still counted; of 11 present, 7 still counted and 4 found; 11 of 11 not content counted as untaken headings. The property names the audit, which is the first reading. Held against the second reading of the 25 first-run cases as well, 5 are gone or partly gone there and 4 of them are still counted; the other: `haiku-4.5-api`, `payroll_cutoff`, segment `b13`, the heading "Paper timesheets", which the second reading classed gone and the first not content, and which the amended scoring counts as an untaken heading, because every segment of its section that is not in the merge has a record.
2. Holds. Over 145 merges (109 cells, the three floors on the nine pairs and the nine reference merges) no segment is absent under the amended rule that is not absent under the registered one, the carried segments are the same, and no cell gains a silent loss. Counted silent losses over the 109 cells: 65 registered, 45 amended, with 12 counted as untaken headings. Runs with a counted silent loss, repeats included: 18 registered, 10 amended.
3. Holds. 9 reference merges: 0 silent loss and 0 untaken headings under both scorings.
4. Holds. Concatenation: 0 registered and 0 amended. Mechanical union: 0 and 0. On all nine pairs.
5. Holds. Base only: 129 silent losses registered, 121 amended. 0 sentences, list items or table rows of source B are cleared against source A alone. The 8 that leave the count are the headings named: `bike_docks` "Escalating E4"; `loading_dock` "Requesting a slot", "When to request", "On the day", "Late finishes"; `rate_limits` "What the client does", "Other kinds of refusal"; `trace_names` "Resolution". 23 other headings stay silent losses.
6. Holds. 96 segments over the 145 merges move from absent to reworded, 87 by step (1) and 9 by step (2). Each was read a second time by a routine of the figure script that is not the scorer's, which found the segment's words as one run in the merge text named for it. `differences.json` shows the run for every segment whose count differs.
7. Holds. The reference merges move 1 segment between the rules: `bike_docks` b10 (step (1)). Concatenation and the union go from 65 bloat to 64, base only from 66 lost to 67. Deviations per pair of the union: 7.78 registered, 7.67 amended.
8. Holds. In every one of the 145 merges the segments the similarity rule calls reworded are the same under both rules. In the 109 cells that is 901 segments, 720 of them by the similarity rule alone (neither step of the amended rule finds their words as a run); `reworded-by-similarity.json` lists and marks them. The audit did not read them.

What this amendment does not claim: that the amended count is the number of real losses. It leaves false alarms it cannot decide without a model (a sentence reworded with other words, with its clauses in another order, split with a word written at the seam, or joined with its subject dropped), and those stay counted as silent loss under both scorings.

A second defect, found while the rule was designed, that this amendment does not address: the registered similarity rule also errs the other way. A sentence that was cut short is called "reworded" whenever a little more than half of it is left. Measured on the sources of the nine pairs: of 181 sentences, list items and table rows of at least six words, each with its last two words cut and nothing put in their place, 173 read as reworded under the registered rule. Such a segment is still a finding in the tool ("Reworded and undeclared", exit code 1, with the difference printed), but it is not a silent loss in either scoring. Closing this means replacing the similarity rule, which would move today's "reworded" to "gone" in an unknown number of cases and needs an audit of its own.

**Amendment 4, 2026-10-12, after every call of this registration and after its results were published. It governs no call and changes no count. It extends the audit by which Amendment 3 disqualifies, and it is made knowing the results.** Amendment 3 disqualifies a row by what an audit by reading found, and that audit read only the segments the registered scoring had counted as silent loss. A sentence that lost a clause and still resembles the original is called "reworded" by the similarity rule, so it was not read, and where the merge wrote no record for it, the loss is as silent as a missing sentence. So the audit now covers every source segment on a first run that the merge does not carry word for word and for which it wrote no record: the 25 segments the registered scoring counted as silent loss there, and the 19 that the similarity rule alone calls reworded and that no record names (`haiku-4.5-api` 8, `haiku-4.5-sub` 5, `sonnet-5-sub` 4, `gpt-6-luna-api` 2, none on the other 4 rows).

What the readings found. Two further separate runs of an AI model (Claude Opus), each given the segments and the documents of their runs and neither given a score or the other's reading, read them and gave every one of the 19 the same class: 15 present, 1 not content, 2 partly gone and 1 gone. The three with loss:
- `haiku-4.5-api`, `trace_names`, segment `b2`, "Author: Marlowe Ferrante Updated: 2026-02-03": partly gone (the first reading names not content as the alternative). The author's name is nowhere in the merge. The date is, beside the other source's author.
- `haiku-4.5-sub`, `trace_names`, segment `b2`, "Author: Marlowe Ferrante Updated: 2026-02-03": gone (the first reading names not content as the alternative). Neither the name nor the date is in the merge.
- `gpt-6-luna-api`, `library_holds`, segment `a3`, "When a requested item arrives, print a hold slip and fold it into the item so the name is visible from the spine.": partly gone (both readings name present as the alternative). The merge has the instruction without its opening condition, under the heading "Placing an item on the shelf", which implies the occasion.

The ruling. The last of these is the only loss the audit found for `gpt-6-luna-api`, and both readings call it borderline. The rule of Amendment 3 does not ask how sure a reading is, so the operator was asked whether a borderline case disqualifies, and ruled on 2026-10-12: "Disqualify Luna". The rule stays as Amendment 3 has it and runs over the cases of both kinds. On this lineup the disqualified rows are now `gpt-6-luna-api`, `haiku-4.5-api` and `haiku-4.5-sub`. The other complete rows in order: 1, `gpt-6-sol-api`; 2, `opus-5.5-sub` and `sonnet-5-sub`, tied and not broken; 4, `opus-5.5-api`; 5, `sonnet-5-api`. The tables say so in words: `gpt-6-luna-api` is disqualified; its one case is borderline.

What stays as it is. The program's counts, the amended rule and both scorings of Amendment 3: over the 109 cells 65 counted silent losses registered and 45 amended, with 12 untaken headings, and every figure of the eight outcomes above. No segment is located or counted differently. The sentence of Amendment 3 that names two disqualified rows stands as written, as the state of the audit before this amendment. Outcome 8 says of the segments that the similarity rule alone calls reworded that the audit did not read them. Of those 720 it has now read the 19 that are on a first run and have no record. The 30 on repeated runs that have no record are still unread, and so is every segment that has a record: a declared change can still be wrongly declared, which the tool's checks on its records and its judge address and this audit does not. `audit/README.md` has every case, both readings and the limits.

**Amendment 5, 2026-10-15, after every call of this registration and after its results were published. It governs no call. It corrects one reference merge, and it was made knowing the results.** The reference merge of `bike_docks` (`tests/pairs/bike_docks/ideal.md`) kept the support desk's count of 3 failed attempts beside the field crew's 2 and added a sentence that is in neither source: "The two documents disagree on the number of attempts; the field crew figure of 2 is the one to work to and the support desk figure of 3 is the one to correct." At the default level `high`, at which this run merged the pairs, a merge is told to choose one value where its sources disagree and to record the choice, and the field crew's runbook gives the reason for 2 (repeated forcing bends the pin). The operator found the sentence on 2026-10-15 and ruled that the reference is wrong. It now reads "Escalate E2 to the workshop after 2 failed attempts. The support desk raises an E2 to the field crew first.", and its records say that the support desk's count was superseded by the field crew's sentence. The reference as registered is kept beside it as `ideal-as-registered.md` and `ideal-as-registered.json`.

What moves. The registered scoring is scored against the reference as registered and does not move: `scored.json` and the registered block of `figures.json` are as they were. The amended scoring's counts are scored against the corrected reference. Under the amended rule the old reference carried the support desk's count (its words stand in the reference as a run), so a merge that rightly dropped it was counted as having lost it; the corrected reference no longer carries it, and its own shorter sentence now carries the support desk's first step. On `bike_docks` six rows have 2 deviations fewer, because they dropped the count and kept the support desk's first step: `gpt-6-sol-api` 38 to 36 over the 9 pairs (4.22 to 4.00 a pair), `opus-5.5-sub` and `sonnet-5-sub` 54 to 52 (6.00 to 5.78), `opus-5.5-api` 55 to 53 (6.11 to 5.89), `sonnet-5-api` 56 to 54 (6.22 to 6.00), `gpt-6-luna-api` 52 to 50 (5.78 to 5.56); `haiku-4.5-sub` is unchanged, because it dropped the first step as well, and `haiku-4.5-api` is unchanged over the pairs it is counted on, because its run of `bike_docks` ended as a model failure and is not counted. The three baselines are unchanged (the mechanical union 69, 7.67 a pair). Who is disqualified, the audit and the order do not move: 1, `gpt-6-sol-api`; 2, `opus-5.5-sub` and `sonnet-5-sub`, tied and not broken; 4, `opus-5.5-api`; 5, `sonnet-5-api`. The differences between the two rules (`differences.json`) and the properties of Amendment 3 are read on the references as registered, because they describe the rule change and nothing else.

**Amendment 6, 2026-10-15, after every call of this registration and after its results were published. It governs no call. It corrects one reference merge, and it was made knowing the results.** A check of the other reference merges for the fault Amendment 5 corrected found the same kind in `loading_dock`. Source A says the dock's phone line was retired; source B still tells its reader to phone it, between 08:00 and 16:00 on working days. The pair's own description says the phone instruction is wrong now and must be removed. The reference merge dropped the number and the instruction but kept the hours, in a sentence that is in neither source: "The line took requests between 08:00 and 16:00 on working days before it was retired." The operator approved the correction on 2026-10-15: the sentence goes, so that section is source A's text word for word, and the record for source B's sentence on the hours stays `superseded`, with source A's sentence "The dock booking phone line was retired and the number no longer connects." as its replacement. The reference as registered is kept as `ideal-as-registered.md` and `ideal-as-registered.json`.

What moves, as with Amendment 5: the registered scoring does not. The amended scoring's counts on `loading_dock` do. Seven rows dropped the hours and have 1 deviation fewer over the 9 pairs: `gpt-6-sol-api` 36 to 35 (4.00 to 3.89 a pair), `opus-5.5-sub` and `sonnet-5-sub` 52 to 51 (5.78 to 5.67), `opus-5.5-api` 53 to 52 (5.89 to 5.78), `sonnet-5-api` 54 to 53 (6.00 to 5.89), `gpt-6-luna-api` 50 to 49 (5.56 to 5.44), `haiku-4.5-sub` 65 to 64 (7.22 to 7.11). `haiku-4.5-api` kept the retired instruction and the hours and has 1 more, 49 to 50 (6.12 to 6.25). The baselines move as well: sources concatenated 8.67 to 8.78 and the mechanical union 7.67 to 7.78 a pair, because both carry the hours, and base only 7.67 to 7.56, because it does not. Who is disqualified and the order do not move. The properties of Amendment 3 describe the rule change alone and are measured with both rules on the references as registered.

