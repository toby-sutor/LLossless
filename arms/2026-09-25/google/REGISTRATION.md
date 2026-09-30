# Block: Gemini 3.8 Flash and Gemini 3.5 Flash-Lite on Google's free tier

Registered 2026-09-25, before the first measured call. Not edited afterwards;
corrections are dated amendments at the bottom. Its sha256 is recorded in
`REGISTRATION.sha256` at the moment it was written.

## The question

The operator will not top up Google (a $30 minimum) and approved a **free-tier
test**: prove the tool works with the Google API and see how Gemini compares
with the GPT-6 Sol, GPT-6 Luna and Claude Opus 5.5 rows of
`arms/2026-09-25/vendor/`. **Zero dollars is a hard rule.**

## What is fixed

The design of `arms/2026-09-25/vendor/REGISTRATION.md` (its Arm A), with
Google's differences named here.

- **Tool commit `0771aa6`** (master with the `google` profile, the Google price
  rows and the thinking-token costing, DECISIONS 624), from a clone pinned at
  it, `PYTHONPATH` on the clone's `src/`, `claimcheck.__file__` asserted inside
  the clone. Every report's `provenance.claimcheck_commit` must be the pin with
  no `-dirty`.
- **Corpus:** the nine pairs in `tests/pairs/`, `source_a.md` + `source_b.md`,
  `--base source_a.md`, `--fidelity high`, `--verify-depth full`, `--no-cache`,
  K = 1, scored against each pair's `ideal.md` by `tests/rank_matrix.py`'s
  `cell_figures` at the pin. The same scoring as the vendor rows.
- **The real CLI path**, `claimcheck.cli.main`, one process per cell, through
  `ledger_cli.py`. Asserted per cell: `counts.cache_hits == 0`,
  `counts.replayed == 0`, `run_mode == "live"`, all three roles in
  `calls_by_role`, `counts.calls` equal to the calls the ledger saw answered,
  the tier `prompt`/`pinned`, the model the one named, and **$0.00 charged**.
- **Endpoint** `https://generativelanguage.googleapis.com/v1beta/openai`,
  **profile `google`**, **tier `prompt` pinned**: the rung the vendor rows ran
  at, so the rows compare at one rung (the pilot found all three rungs carry
  the schema on Flash-Lite, 624). Thinking on for every role
  (`CLAIMCHECK_THINKING=decompose,merge,verify`); Gemini 3 cannot turn it off.
  No `reasoning_effort` is sent, so each model's default thinking level
  applies. No `temperature`, no `seed`. `--window 200000`, `--timeout 600`,
  as the vendor rows.
- **Models**, both listed by this key's `GET /v1beta/models` and both "Free of
  charge" in the pricing page's Free Tier column (read 2026-09-25):
  `gemini-3.8-flash`, then `gemini-3.5-flash-lite`. Not 3.1 Pro (no free
  tier). `gemini-2.5-flash`, the named fallback, answers 404 to this key.

## Money: zero

- Every chat request goes through `tests/spend.py`'s `Ledger` with Google's cap
  at **$0.00**, never raised. The ledger SKU is `google-free/<model>`, priced
  at zero in the harness's own process from the Free Tier column; the shipped
  `google/<model>` rows are the paid tier's rates, and the cap refuses them.
- **A billing signal stops the block.** Any error body speaking of billing,
  prepayment, credit or payment, other than the standard text of a quota 429
  whose every named quota is a free-tier one, writes `STOP-BILLING` and exits.
  The key has no credit loaded, so no call can be billed; the guard is there in
  case that is wrong.
- **Free-tier inputs may be used by Google** to improve its products (pricing
  page, "Used to improve our products: Yes" on the free tier). Every document
  sent is a `tests/pairs/` or `tests/fixtures/` file, public and CC BY 4.0,
  approved by `source_guard` against the clone's HEAD.

## Rate limits and quota

- **20 requests per day per model**, read off a 429 during the pilot
  (`GenerateRequestsPerDayPerProjectPerModel-FreeTier`, `quotaValue: "20"`);
  the rate-limit page states no free-tier figures. It resets at midnight
  Pacific (07:00 UTC). **A 503 counts against it.** One merge at `high`/`full`
  makes 6 to 14 calls on the vendor rows, so the nine pairs are about 70
  requests per model: **several days of quota**, and more if 503s continue.
- The pilot spent 3.8 Flash's quota for 2026-09-25. **So 3.5 Flash-Lite runs
  first today, and 3.8 Flash starts when its quota resets.** Each model's
  quota is its own, so the order does not change what either measures.
- **Pacing**: the ledger's interval is 15 s between calls (4 per minute), under
  any per-minute free limit this key has shown; none was observed.
- **Retries are the harness's**, one ledger row each at $0.00: a 429 on a
  per-minute quota waits the `retryDelay` Google names plus 5 s; a 503, 5xx or
  timeout waits 60, 120, 240 s; at most 4 attempts per request. **A 429 on the
  per-day quota stops the model's block** for the day, and the cell it cut is
  recorded and excluded. Every attempt is recorded with its status and body.
- A cell that exits 2 or leaves no report because of an infrastructure fault
  (429, 5xx, timeout) is re-run once, if quota remains.

## Order within a model

1. **Probe:** one merge of `tests/fixtures/dedup` through the harness. It is
   the pilot's end-to-end check: all three roles live through the real CLI.
2. The nine pairs, cheapest first by the 2026-09-18 Terra cost (the vendor
   run's order): `badge_access`, `payroll_cutoff`, `loading_dock`,
   `freezer_alarm`, `bike_docks`, `trace_names`, `library_holds`, `index_429`,
   `rate_limits`. A later session resumes where the quota stopped; recorded
   cells are skipped.

## Figures

Per cell: silent loss, deviations (`lost + bloat + dup` against `ideal.md`),
wall seconds, the seconds the harness spent pacing and backing off, tokens
(input, output, `total_tokens`, cached), and the ledger's dollars (0.00).

- **A catalogue model row per model**, by `tests/rank_matrix.py`'s arithmetic
  over the counted cells: silent loss and deviations with their per-pair rates.
- **Seconds per merge** are the wall seconds **less the harness's pacing and
  backoff waits**, whole seconds per cell. The free tier's waits are a property
  of the quota, not of the model, and the vendor rows had none; the raw wall is
  stated beside it.
- **`usd_per_merge` is null**: nothing was billed, and `pricing.py`'s rule is
  that an unbilled or unmeasured cost is never shown as $0.00. What a paid run
  would cost is **computed, not billed**, from each answered call's tokens at
  the paid tier's Standard rates in `pricing.py` (read 2026-09-25), with output
  taken as `total_tokens - prompt_tokens` where that is larger (624), and is
  stated in the row's notes as that.
- A row forms only from the pairs completed. If a model has fewer than nine,
  the row says so and its per-pair rates are over its own pairs.

## What this may be used for

The web UI's catalogue: a Gemini 3.8 Flash row and a Gemini 3.5 Flash-Lite
row, each with its date, commit, pair count and the words "free tier". Not the
paper, not the frozen benchmark (403).

## What is not controlled

Sampling: no `temperature`, no `seed` (Google refuses `seed`), so no cell
repeats and K = 1. The free tier's capacity: 503s under "high demand" add
waits and may cost whole cells. The days: a model measured across two days
may meet a changed endpoint; each cell's date is recorded.

## Amendments

**2026-09-25, 18:40 UTC, after the Flash-Lite probe and before any pair.**
The harness's zero row was named `google-free/<model>`, and `pricing.sku_for`
matches on the part after the prefix, so it found two rows for the model and
the probe's report read its cost as `unpriced`. The row is renamed
`probe/google-free/<model>`: the `probe/` prefix is the table's own marker for
a row that is not a vendor price, and `sku_for` skips it, so each report now
states what its calls would cost at the paid rate. Nothing measured changes;
the probe is not a figure.

**2026-09-25, 18:56 UTC, after Flash-Lite's `freezer_alarm` cell.** That cell
exited 2: the merge answered five times with a schema violation
(`decisions[4].candidates has 1`) and `verify` never ran. The runner read "a
role never called" as a failed assertion and stopped the block. By the
Exclusions rule it is an exit 2, excluded and named, and not re-run (no
infrastructure fault). The runner now skips the roles assertion on an exit 2
and the block resumes at `bike_docks`. Nothing counted changes.

**2026-09-25, 19:16 UTC, the block stops for the day.** 3.5 Flash-Lite ran its
probe and all nine pairs: eight counted, `freezer_alarm` excluded (exit 2). It
never met a 429, so its free-tier daily quota is above the 75 requests it made;
no 503 either after 18:30. A fresh call to 3.8 Flash at 19:15 still answered
429 on `GenerateRequestsPerDayPerProjectPerModel-FreeTier`. **3.8 Flash has no
measured cell**: its first day's quota went on the pilot. At 20 requests a day
and 6 to 14 per merge, its probe and nine pairs need about five days of quota,
from the next reset (07:00 UTC). It resumes at the same pin, probe first, as
this registration says; no Gemini 3.8 Flash row is formed until it has.

**2026-09-25, 20:40 UTC, after the day's block, before any further call.**
The operator reported many 429 and 503 answers from Google. Counted per model
(`error_counts.json`): 3.8 Flash 37 requests, 3 answered, 13 x 429, 18 x 503;
3.5 Flash-Lite 77 requests, 69 answered, 0 x 429, 5 x 503; every one in the
pilot, none in the 66 measured calls. Twelve of the 429s were the pilot's own
retry script retrying a **per-day** 429 at 30 s spacing, which it should have
stopped at. For every later call, ledger_cli.py's policy is now:
- **Pacing 20 s** between calls (3 a minute): the free tier's per-minute
  limit is not published and no 429 has named one, so 20 s is 1.5x the minimum
  interval of a 5-a-minute limit, the strictest this key could plausibly have.
- **At most 5 retries per request**, then the request fails and the tool's own
  handling takes over. Exponential backoff with jitter (x1.0-1.25), capped at
  600 s: a 429 waits what Google names (`Retry-After`, `retryDelay`) and at
  least 30 s, doubling from 30 s when it names nothing; a 503 is Google
  overloaded and waits from 60 s.
- **A 429 on the per-day quota stops the arm** at once, with no retry and no
  waiting for the reset; the pairs done are recorded.
`selftest_retry.py` drives the real wrapper offline through five cases. The
measured Flash-Lite cells ran under the earlier policy (15 s, retries on 5xx
from 60 s, at most 3); they met no 429 and no 503, so no figure depends on it.
