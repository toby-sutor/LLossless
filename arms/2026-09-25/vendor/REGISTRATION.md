# Block: GPT-6 Sol and Luna, and API Opus against subscription Opus

Registered 2026-09-25, before the first paid call. Not edited afterwards;
corrections are dated amendments at the bottom. Its sha256 is recorded in
`REGISTRATION.sha256` at the moment it was written.

## The questions

1. The operator: *"Can we pull some model data for GPT-6 Sol with the
   remaining $4.16 balance? ... It would be good to have a second model for
   reference."* And later: *"Seems like Luna is pretty cheap. If you can
   squeeze it in too, that would be cool."*
2. The operator: *"Try to retest the Opus models again. They are important."*
   Read as: a controlled comparison of `claude-opus-5` through the API against
   the same model through the subscription `opus` route, plus a first look at
   `claude-opus-5-5`. The two existing Opus rows (API, 2026-09-18, `cf30209`;
   subscription, 2026-09-24, `3480292`) differ in tool commit, effort, tier,
   the operator's `CLAUDE.md` being loaded, and K = 1, so they do not compare.

## What is fixed for every arm

- **Tool commit `ff8ff77`** (master: 5ab0115 plus the three price rows the
  arms need), from a clone pinned at it, with `PYTHONPATH` on the clone's
  `src/` and `claimcheck.__file__` asserted inside the clone. Every report's
  `provenance.claimcheck_commit` must be the pin with no `-dirty`.
- **Corpus:** the nine pairs in `tests/pairs/`, `source_a.md` + `source_b.md`,
  `--base source_a.md`, `--fidelity high`, `--verify-depth full`,
  `--no-cache`, scored against each pair's `ideal.md` by
  `tests/rank_matrix.py`'s `cell_figures` at the pin: the scoring the
  2026-09-18 hosted rows and the 2026-09-24 subscription rows used.
- **The real CLI path:** `claimcheck merge`'s own `cli.main`, one process per
  cell. Live calls asserted per cell: `counts.cache_hits == 0`,
  `counts.replayed == 0`, `run_mode == "live"`, all three roles in
  `calls_by_role`, and for the API arms `counts.calls` equal to the calls the
  ledger charged in that cell.
- **Tier `prompt`, pinned, on every arm.** Three reasons. The subscription
  route has no other rung. GPT-6's Chat Completions refuses function calling
  unless `reasoning_effort` is `none` (model pages), so `tool_call` is not
  available with reasoning on, which is why the Terra row pinned `prompt`.
  And Anthropic's OpenAI-compatible endpoint documents `response_format` as
  "Ignored", so at `json_schema` the model is shown no schema at all; `prompt`
  is the one rung at which both Opus routes are shown the same schema.
  The 2026-09-18 Anthropic rows ran `json_schema/probed`; this is a
  difference from them and it is deliberate.
- **Thinking on for every role** (`CLAIMCHECK_THINKING=decompose,merge,verify`),
  as on 2026-09-18. `--window 200000` and `--timeout 600` on the API arms, as
  then. No `temperature` on any arm (the profiles do not send it with
  reasoning on); `seed` is sent to OpenAI only.

## Effort

The `anthropic` profile sends no effort field and, with thinking on, no
`reasoning_effort` either (which the compatibility endpoint documents as
"Ignored" anyway). So the API default applies: **`high` on Claude Opus 5**
("The API default is `high`") and **`medium` on Claude Opus 5.5** (effort
page, read 2026-09-25). Thinking is on by default on Claude 5 models through
that endpoint.

**B2 runs the CLI at `--effort high` for all three roles**
(`CLAIMCHECK_EFFORT=high`), matching B1 role by role. That is not the route's
default (merge `high`, decompose and verify `low`, entry 612); the brief asks
for the effort matched, and the route's default is measured elsewhere.

OpenAI: no `reasoning_effort` is sent with thinking on, so each GPT-6 model's
default applies, `medium` for both (model pages).

## Money: the ledger

`tests/spend.py`'s `Ledger`, with run-specific `Caps`: **openai $3.90,
anthropic $8.60**, google $0.00, 400 calls and 4,000,000 tokens per vendor.
The shipped `FIRST_PASS` ($7.50/$7.50, 357) is not used and not edited. The
balances are $4.16 and $9.12.

- Enforced per call: `claimcheck.transport.post_json` is wrapped in
  `Ledger.call`, the one seam every chat request goes through. Pre-call
  estimate: the body's characters / 3 as input, plus an output allowance of
  24,000 tokens (OpenAI) or 40,000 (Anthropic) at the SKU's output rate; the
  largest single call on 2026-09-18 was 26,972 output tokens (Opus, merge,
  `rate_limits`). Charged after the call from the envelope's own `usage`. A
  call that fails is charged the estimate; each retried attempt beyond the
  first is charged the estimate again. `documents` is the pair's two files,
  approved by `source_guard` against the clone's HEAD.
- The ledger state persists to disk after every call and is shared by every
  cell and every probe of that vendor, so the caps count all of it.
- `interval` is 0 for this run. Pacing would add a fixed wait to every call,
  inside the seconds this run reports; calls are serial and sized far below
  either account's per-minute token limits.
- **Per-cell gate:** a cell starts only if the vendor's remaining cap covers
  its projected cost x 1.25 plus one call's estimate. The projection is the
  largest cost already measured on that pair in that arm; before that, the
  arm's sizing cell scaled by that pair's cost ratio in the 2026-09-18 run of
  the same vendor (Terra for OpenAI, Opus 5 for Anthropic).
- No two metered API calls are ever in flight together: the API arms run one
  after another. B2 is not metered per call and may run beside Arm A.

## Arm A: GPT-6 Sol, then GPT-6 Luna (OpenAI, $3.90 together)

`gpt-6-sol` and `gpt-6-luna`, both listed by this account's `GET /v1/models`
and named on their model pages, profile `openai-reasoning`, K = 1.

1. **Probe:** one `claimcheck merge` of `tests/fixtures/dedup` per model,
   through the same harness and ledger. Confirms the profile and the pinned
   tier answer, all three roles called live. Probes count against the cap.
2. **Sizing:** Sol's first cell, `badge_access`, the cheapest pair on
   2026-09-18. It counts as a cell.
3. **Luna's reserve**, held back before Sol's remaining cells: Luna's nine
   pairs projected from Sol's projection x the ratio of Luna's probe cost to
   Sol's, x 1.5, and never under $0.30.
4. **Sol** on as many of the nine pairs as the cap less that reserve allows,
   cheapest first by the 2026-09-18 Terra cost, which is also the order when
   nothing is cut. **Luna** then runs exactly the pairs Sol completed, so the
   two rows cover the same pairs.

## Arm B: API Opus against subscription Opus (Anthropic, $8.60 in total)

Three pairs: `trace_names` (all four of the subscription row's silent losses),
`rate_limits` (the largest pair, 104 segments), and `badge_access` as the
clean pair: 0 silent loss and 0 deviations in both earlier Opus rows, and the
cheapest pair in the 2026-09-18 Opus run. Draw-major: draw 1 of all three
pairs, then draw 2, then draw 3, so a cut lowers K evenly.

- **B1, `claude-opus-5` through the API**, profile `anthropic`, K = 3. Its
  first cell (`badge_access`, draw 1) is the sizing probe and counts as a
  draw.
- **B2, the subscription `opus` route**, the same three pairs, K = 3:
  exactly nine runs. The route's own environment
  (`commands.Route.environ()` at the pin) with `CLAIMCHECK_EFFORT=high`,
  run under entry 610's isolation: every report's `provenance.isolation` must
  show `safe_mode: true` and `tools: []` for every role, and
  `decoding.effort` must be `high` for every role. The parent session's
  `CLAUDE*`, `AI_AGENT`, `CLAIMCHECK_*`, `ANTHROPIC*` and `OPENAI*` variables
  are removed from the child environment. Every CLI call's JSON envelope is
  kept by a transparent wrapper named `claude`, and the usage B2 reports is
  summed from those envelopes. Runs after B1.
- **B3, `claude-opus-5-5` through the API**, listed by `GET /v1/models`,
  profile `anthropic`, the same three pairs, draw-major, after B1. Draw 1 runs
  if the remaining cap covers it at B1's largest per-pair cost x 0.8 (the
  price ratio, $4/$20 against $5/$25) x 1.25. Draws 2 and 3 each run only if
  the remaining cap covers another whole draw at B3's own largest measured
  per-pair cost x 1.25. K is therefore 0 to 3, decided by the ledger, and
  stated. It runs at its API default effort, `medium`, one level below B1,
  and is not matched to anything.

## Figures

Per cell: `silent` (segments absent with no declaration), deviations
(`lost + bloat + dup` against `ideal.md`), wall seconds of the merge process,
and for the API arms the dollars the ledger charged in that cell (the billed
upper bound, failed attempts included).

- **Arm A rows**, as catalogue model rows, by `tests/rank_matrix.py`'s
  arithmetic: silent loss and deviations summed with their per-pair rates,
  seconds per merge from whole seconds per cell, usd per merge from whole
  cents per cell.
- **Arm B, per arm:** per pair, median with min-max over the draws, for
  silent loss, deviations, seconds and (B1, B3) dollars; and per draw the
  arm's mean over the three pairs, reported as median with min-max over the
  draws. B2 has no dollar figure.

## The rule: do B1 and B2 differ beyond their own draw spread?

For each pair and each of the two quality figures (silent loss, deviations),
the routes **differ on that pair** when their min-max ranges over the draws
do not overlap. A pair counts only when both routes have at least two draws
on it. Then:

- **API Opus is better** if at least one (pair, figure) differs and every one
  that differs favours the API; **subscription Opus is better** the other way
  round;
- **they differ, with no winner** if differing (pair, figure)s point both
  ways;
- **no difference beyond the draw spread** if none differs.

Seconds are reported under the same rule, separately; speed is not quality.

## Exclusions

A cell that exits 2 is excluded and named, as `rank_matrix.py` excludes one.
It is re-run once, at the same pin, only if its stderr names an
infrastructure fault (HTTP 429 or 5xx, a timeout, a usage limit) and the
ledger allows it. A cell the gate refuses is not run and is named. B2 stops
at a subscription usage limit.

## What this may be used for

The web UI's catalogue: a GPT-6 Sol row and a GPT-6 Luna row, an Opus 5.5
row if measured, and a new measured block for API Opus and for the
subscription `opus` route at `ff8ff77`, beside the earlier figures, each
with its date and commit. Not the paper, not the frozen benchmark (403).

## What is not controlled

The route itself, which is the variable: an HTTP compatibility endpoint
against the `claude` CLI with its own harness and system prompt, whose
seconds include the CLI's start-up on every call. Sampling: neither Anthropic
route sends a temperature or a seed, OpenAI's seed is best-effort, so no cell
repeats and K is the only defence. B2 may run beside Arm A. Opus 5.5 runs at
a different effort from B1.

## Amendments

**2026-09-25, 13:35 UTC, before any B2 or B3 call.** B1 cannot run: API
`claude-opus-5` refuses every merge at `ff8ff77` (`reasoning_extraction`),
bisected to one paragraph of `prompts/merge.md` (DECISIONS 617). B2 and B3
held for the operator. Arm A proceeds as registered.

**2026-09-25, 14:12 UTC, before any Opus 5.5 call.** The operator's ruling
(DECISIONS 618): Opus 5 is retired in favour of Opus 5.5. B1 and B2 are
dropped. **Arm B is now `claude-opus-5-5` through the API**, as the other
hosted rows and Arm A are run: the nine pairs, K = 1, profile `anthropic`,
tier `prompt` pinned, effort the API default (`medium`). First a probe of
`tests/fixtures/dedup`; then `badge_access` as the sizing cell; then the other
eight pairs cheapest first by the 2026-09-18 Opus 5 cost, each through the
per-cell gate, under what remains of the $8.60 Anthropic cap. Figures as for
Arm A: a catalogue model row by `rank_matrix.py`'s arithmetic. It starts after
Arm A ends, so no two metered calls overlap.

**2026-09-25, 13:58 UTC.** A machine crash interrupted Arm A's
`trace_names` cell after four charged calls ($0.0930) with a fifth in flight
(boot 13:47:57, last ledger write 13:47:11). The four stay charged; the fifth
is charged its estimate ($0.2503), as a call that never reported is. The
attempt counts against the cap, never the figures, and the cell was re-run
once.
