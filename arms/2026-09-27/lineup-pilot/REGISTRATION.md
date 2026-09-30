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
                 - fable-sub: fable via claude (subscription), effort medium on every role (CLI), thinking ['decompose', 'merge', 'verify'], window 200000, sets ['S1'], not in the headline
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
Budget:          caps {"anthropic": 4.0, "openai": 2.0, "overall": 6.0}; subscription meter recorded by `note` before the subscription lane starts
May be used for: plan section 9.2; not for section 9.3
Pilot:           this is the pilot (plan section 7); never counted. Lanes split by vendor so the OpenAI rows run first (operator, 2026-09-27)
```

Amendments go below the machine block, dated, each before the calls it governs.

```json lineup-registration
{
 "registration": 1,
 "name": "fair lineup pilot (never counted)",
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
    "badge_access"
   ],
   "draws": {
    "default": 1
   }
  },
  "S2": {
   "kind": "detect",
   "score": "detect",
   "root": "tests/fixtures",
   "items": [
    "dedup"
   ],
   "draws": {
    "default": 1
   },
   "headline_items": [
    "dedup"
   ]
  },
  "S3": {
   "kind": "merge",
   "score": "planted",
   "root": "tests/handwritten",
   "fidelity": "open",
   "items": [
    "bip39"
   ],
   "draws": {
    "default": 1
   }
  }
 },
 "caps": {
  "anthropic": 4.0,
  "openai": 2.0,
  "overall": 6.0
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
  "subscription": {}
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
   "reference": "luna-ref"
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
   "reference": "luna-ref"
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
    "S1"
   ],
   "reference": "luna-ref",
   "headline": false,
   "compare_with": "opus-5.5-sub",
   "unpriced": "Fable has no row in pricing.py; subscription only, never metered (678)",
   "items": {
    "S1": [
     "badge_access"
    ]
   },
   "served_aliases": [
    "claude-fable-5-1"
   ]
  }
 ],
 "env_file": "<home>/Documents/Dev/vibe-coding/claimcheck/.env"
}
```
