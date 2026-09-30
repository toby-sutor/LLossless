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

