# Block: verification depth, re-run after 569

Registered 2026-09-24, before any call. Not edited afterwards; corrections are
dated amendments at the bottom.

## Why a re-run

The 2026-09-22 run (`../2026-09-22-depth-benchmark/`, tool `9f1d5d4`) was
disqualified on its own pre-registered rule: `full`, the comparator, exited
clean on `attribution_invented` in all three draws. DECISIONS 569 then added a
mechanical attributions check (`reconcile.attribution_findings`, no model
call) that runs at both depths. This re-run measures the depth comparison at a
tool commit that carries 569, so the web UI's "unmeasured" can be replaced by a
figure or kept for a stated reason.

## Arms

Unchanged from the 2026-09-22 registration: `full` (comparator, first) and
`coverage`, same session, same endpoint, same model, one tool commit, tier
pinned `json_schema`, `--field-order any`, thinking at the model's default,
`--window 32768`, `--no-cache`, `--timeout 900`. Driven by
`tests/run_detect.py` over `tests/fixtures/`, each fixture's hand-written
`merged.md`, so no merge call is made.

Run from a clone of the working repo pinned at one commit (recorded in
`COMMIT`), so commits made to the working repo during the run cannot move the
tool under it.

## Draws: K = 1, and why

The registered 2026-09-22 minimum was K = 3 because of decomposer spread
(entry 485). On this model that spread measured zero: every figure in the
2026-09-22 table was identical in all three draws (`depth-benchmark.md`).
K = 1 is chosen on that measurement. If this draw's figures on fixtures 569
cannot touch differ from 2026-09-22's, that is reported as a cross-day
difference and **not** attributed to 569 or to the tool commit (a figure from
another day is a confound, not a control). Within-session, `full` against
`coverage` is the only comparison this run makes.

## Predicted (properties, registered before the call)

1. `full` detects every plant it is registered to detect. In particular
   `attribution_invented` exits 1. If `full` exits clean on any plant, the
   comparator is disqualified again, on the same rule, and nothing reaches the
   catalogue or the page.
2. `coverage` detects zero plants whose detection requires a model pass over
   the merged document (`hallucination`). Its `attribution_*` detections, if
   any, come from the mechanical check and are reported as such, separated
   from model-pass detections.
3. `wrong findings on guards` stays 0 in both arms. 569 is new and mechanical;
   a firing on any `kind: guard` fixture or guard probe is a false positive of
   569 and is reported as that, named by fixture.
4. `coverage` is faster and makes fewer calls.

## Falsified by

Any reverse-probe model-pass detection by `coverage`; a clean exit by `full`
on any plant; any guard firing attributable to 569.

## What this may be used for

If prediction 1 holds and prediction 3 holds: a `verify_depth` figure for
`catalogue.json` and the page, as rates split by direction, with the
structural miss (invention: `hallucination`) named rather than blended. If
either fails: the page keeps "unmeasured" and the reason is written down.
