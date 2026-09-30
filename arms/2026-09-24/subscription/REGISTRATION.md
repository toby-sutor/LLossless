# Block: the subscription routes over the nine pairs

Registered 2026-09-24, before any call. Not edited afterwards; corrections are
dated amendments at the bottom.

## What is measured

Three command routes, one draw each, over the nine pairs in `tests/pairs/`
(`source_a.md` + `source_b.md`, base `source_a.md`), at `--fidelity high`
and the default verification depth, `--no-cache`:

    claude-haiku    claude --print --output-format json --model haiku
    claude-sonnet   claude --print --output-format json --model sonnet
    claude-opus     claude --print --output-format json --model opus

`claude-fable` is not run: the operator does not want the most expensive model
used. It stays unmeasured and the page says so.

Each route runs under the environment the web UI gives it, taken from
`commands.Route.environ()` for the discovered route: `subscription` profile,
`prompt` tier, thinking on for every role, `--window 200000`, the route's
call timeout, and the per-role effort `config.AUTO_EFFORT` applies (merge
`medium`, decompose and verify `low`). Nothing is pinned beyond what the route
pins. No `temperature`, no `seed`: not reproducible by construction (483).

Run serially, one cell at a time, cheapest route first, from a clone of the
working repo pinned at one commit (recorded in `COMMIT`), with the parent
session's `CLAUDE*` variables removed from the child environment.

## Figures

Per route, the catalogue's model-row figures, formed the way
`tests/rank_matrix.py` forms the hosted rows of 2026-09-18 over the same nine
pairs and the same `ideal.md` references:

- `seconds_per_merge`: wall time of the whole `claimcheck merge` process,
  per completed pair, summed as whole seconds and divided by the pairs.
- `silent_loss`, `silent_loss_per_pair`: segments absent from the merge with
  no declaration.
- `deviations`, `deviations_per_pair`: lost + bloat + duplicates against
  `ideal.md`.
- `usd_per_merge`: null. The calls are included in the subscription and not
  priced per call.

## Exclusions

A cell that exits 2 (inconclusive) is excluded and named, as the qwen rows
excluded `toby-test-5`; `pairs` is then the completed count. Each cell is
attempted once. The one exception is a cell stopped by a subscription usage
limit, which is infrastructure rather than the model: the run stops at the
first such cell and that cell is re-run after the limit resets, at the same
pin. A route with fewer than 9 completed pairs is published with its own
`pairs` count and says so in `notes`.

## What this may be used for

A rough estimate on the web UI, beside each subscription route, in the same
columns as the other rows. Not for the paper and not for the frozen benchmark
(403). Not a ranking against the hosted rows: a different backend (the CLI,
`prompt` tier, no temperature or seed), a newer tool commit than 2026-09-18,
one draw. The subscription routes compare with each other within this run.
