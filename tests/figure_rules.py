"""How a pairs headline is formed from scored cells: one home for the rules.

Every figure script that forms a lineup, vendor or matrix headline from the
nine pairs (`vendor_figures.py`, `matrix_figures.py`, `subscription_figures.py`,
`google_figures.py`, `rank_matrix.py`'s ranking, and the lineup's own figures
script when it is written) forms it here, so the rules cannot drift apart
between them. Nothing here scores a merge -- `rank_matrix.cell_figures` does
that -- and nothing here calls a model.

The rules, each with where it comes from:

- **One figure per (model, pair).** The headline reads draw 1 of every pair.
  A draw is never counted as a pair: the three spread pairs at K = 3 would
  otherwise weigh three times. Their further draws are
  reported beside the headline as min, median and max, never folded into it.
- **(model, pair, draw) is unique among counted cells**, asserted. A second
  counted cell for one key is a runner that did not mark its superseded or
  interrupted row, and taking either would make the figure depend on order.
- **The common-pairs rule.** Headline rates are over the pairs
  **every counted model completed**. A model that completed fewer keeps its
  full-row figure beside the headline (`*_all_completed`), and the pairs it
  did not complete are their own column (`pairs_not_completed`, with the
  reason: `exit_2`, `gated`, `interrupted`, ...). A counted model is one with
  at least one counted cell in the run.
- **Failures outside the model's control are not scored.** An excluded
  cell adds nothing to quality, cost or speed.
- **Cost from exact values, rounded once.** A cell's cost is
  `provenance.answering_cost.usd_exact` when the report carries that
  block (the answering attempt's own cost, apart from retries and
  discards), else `provenance.cost.usd_exact` when the report carries
  that one instead, else `pricing.estimate` over the report's own
  ledger (the arithmetic the report's `usd` was rounded from). The
  row's figure is the mean of the exact values, rounded once, to the
  page's three decimals. The runner's billed ledger is a separate
  column, the billed upper bound, never the headline.
- **One seconds source per row.** A cell's seconds are
  `provenance.answering_seconds.total` when the report carries that block and
  it is not `None` (`answer_ms` over the rows charged to the model,
  already apart from waits, retries and discards), less a harness's own
  pacing and backoff where the harness booked them (outside the report
  entirely, e.g. a vendor rate limit the runner itself slept through).
  Otherwise -- an older report, or one where nothing was timed -- the report's
  own `provenance.duration_seconds` (the whole merge run, all three
  roles), less the waits the run recorded as not the model's: retry and
  pacing waits on the ledger rows (`waited_ms`) and discarded blank attempts
  (`provenance.discarded_calls[].latency_ms`), when the report carries them,
  and the same harness waits. The mean is rounded once, to a tenth of a
  second.

**The lineup's own rule** (`lineup_groups`), for the
fair-lineup figures only; the published P rows keep `groups` above until they
are rescored. A row's own result on a pair -- its exit 2, a window its
registration cannot hold, a refusal, an unruled cell, an endpoint that failed
while the reference worked -- never shrinks another row's common pairs: the
row is incomplete, and is listed after every complete row. The headline cell of
(row, pair) is its lowest-numbered draw that counts, not draw 1 alone. Nothing
shrinks the common pairs: a pair a row could not be measured on
is that row's alone, "not measured".
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from llossless import pricing  # noqa: E402

# The three pairs every model runs at K = 3.
SPREAD_PAIRS = ("badge_access", "trace_names", "rate_limits")
# The draw the nine-pair headline reads.
HEADLINE_DRAW = 1
# Display precision, the page's own (`app.js` renders usd_per_merge to three
# places and seconds to one): the one rounding a figure gets.
USD_PLACES = 3
SECONDS_PLACES = 1
RATE_PLACES = 2


class RuleBroken(SystemExit):
    """A figure the rules refuse to form. Raised, never printed and passed over."""

    def __init__(self, message: str) -> None:
        super().__init__(f"figure_rules: {message}")


def deviations(cell: dict) -> int:
    """The band deviation of one scored cell: lost + bloat + exact repeats."""
    return cell["lost"] + cell["bloat"] + cell["dup"]


def draw_of(cell: dict, *, registered_k1: bool) -> int:
    """The cell's draw. A run registered at K = 1 whose records carry no draw
    field is draw 1 by its registration; any other record must say."""
    if "draw" in cell:
        return int(cell["draw"])
    if registered_k1:
        return HEADLINE_DRAW
    raise RuleBroken(f"a cell of {cell.get('pair')} carries no draw and the run is "
                     f"not registered at K = 1")


def check_unique(cells: list[dict], model_key: str, *, registered_k1: bool) -> None:
    """(model, pair, draw) is unique among the counted cells."""
    seen: set[tuple] = set()
    for cell in cells:
        if cell["excluded"]:
            continue
        key = (cell[model_key], cell["pair"], draw_of(cell, registered_k1=registered_k1))
        if key in seen:
            raise RuleBroken(f"two counted cells for {key}; a superseded or interrupted "
                             f"row was not marked as such")
        seen.add(key)


def mean_rounded(values: list[float], places: int) -> float:
    """The exact mean, rounded once."""
    return round(sum(values) / len(values), places)


def spread(values: list) -> dict:
    """min, median and max of a draw set."""
    med = statistics.median(values)
    med = int(med) if float(med).is_integer() else med
    return {"min": min(values), "median": med, "max": max(values)}


def groups(cells: list[dict], models: tuple[str, ...], model_key: str, pairs_run: list[str],
           *, registered_k1: bool) -> dict[str, dict]:
    """Per counted model: its draw-1 cells, the common pairs, and what it did not complete.

    `models` are the rows the script forms, in order; a model with no counted
    cell is not a counted model and forms no row. `pairs_run` are the pairs the
    run registered.
    """
    check_unique(cells, model_key, registered_k1=registered_k1)
    first: dict[str, dict[str, dict]] = {}
    for model in models:
        mine = [c for c in cells if c[model_key] == model and not c["excluded"]
                and draw_of(c, registered_k1=registered_k1) == HEADLINE_DRAW]
        if mine:
            first[model] = {c["pair"]: c for c in mine}
    if not first:
        return {}
    common = sorted(set.intersection(*(set(done) for done in first.values())))
    if not common:
        raise RuleBroken(f"no pair was completed by every counted model "
                         f"({', '.join(first)}); there is no common headline")
    out = {}
    for model, done in first.items():
        missing = {}
        for pair in pairs_run:
            if pair in done:
                continue
            reasons = [c["excluded"] for c in cells
                       if c[model_key] == model and c["pair"] == pair and c["excluded"]]
            missing[pair] = reasons[-1] if reasons else "not_run"
        draws = {}
        for pair in SPREAD_PAIRS:
            more = sorted((c for c in cells if c[model_key] == model and c["pair"] == pair
                           and not c["excluded"]),
                          key=lambda c: draw_of(c, registered_k1=registered_k1))
            if len(more) > 1:
                draws[pair] = {"draws": len(more),
                               "silent_loss": spread([c["silent"] for c in more]),
                               "deviations": spread([deviations(c) for c in more])}
        out[model] = {
            "common": common,
            "cells": [done[p] for p in common],
            "completed": sorted(done),
            "all_cells": [done[p] for p in sorted(done)],
            "not_completed": missing,
            "spread_draws": draws,
        }
    return out


# What became of one (row, pair), decided by the lineup's registered rules.
DONE = "done"      # a counted cell: scored
OWN = "own"        # the row's own result (exit 2, window, a refusal, unruled, endpoint_failure)
APART = "apart"    # held apart for this row only (no lineup rule produces it)
LOST = "lost"      # not measured: lost outside the model (never run, an outage); the row's alone


def lineup_groups(cells: list[dict], models: tuple[str, ...], model_key: str,
                  pairs_run: list[str], *, treat) -> dict:
    """The lineup's headline groups: the common pairs, and per model its figures' cells.

    `treat(cell)` says what a cell is: `DONE`, `OWN`, `APART` or `LOST`. For
    each (model, pair) the draws are read in order and the first that is
    `DONE` or `OWN` decides it; `APART` and `LOST` draws are passed over, so a
    lost draw 1 does not hide a counted draw 2. A pair with nothing decided is
    `LOST` if any draw was lost or none ran, else `APART`.

    The common pairs are every pair in `pairs_run`: nothing shrinks them
    (superseding the common-pairs rule and `platform_lost: shrink`).
    A pair a model lost, for its own reason or to anything else, is that
    model's alone.

    Per model: `cells` (its `DONE` headline cells on the common pairs),
    `all_cells`, `completed`, `not_completed` ({pair: reason}, every pair run),
    `incomplete` ({pair: reason}: `OWN` and `LOST`), `apart` ({pair: reason}),
    and `spread_draws` over its `DONE` draws.
    """
    check_unique(cells, model_key, registered_k1=False)
    status: dict[tuple, tuple] = {}
    for model in models:
        for pair in pairs_run:
            mine = sorted((c for c in cells if c[model_key] == model and c["pair"] == pair),
                          key=lambda c: draw_of(c, registered_k1=False))
            decided = None
            for cell in mine:
                kind = treat(cell)
                if kind in (DONE, OWN):
                    decided = (kind, cell, cell["excluded"] or "ok")
                    break
            if decided is None:
                lost = [c["excluded"] for c in mine if treat(c) == LOST]
                decided = ((LOST, None, lost[0]) if lost else (LOST, None, "not_run")
                           if not mine else (APART, None, mine[0]["excluded"]))
            status[(model, pair)] = decided
    common = list(pairs_run)
    out = {}
    for model in models:
        done = {p: status[(model, p)][1] for p in pairs_run if status[(model, p)][0] == DONE}
        incomplete, apart = {}, {}
        for pair in common:
            kind, _, reason = status[(model, pair)]
            if kind == OWN or kind == LOST:
                incomplete[pair] = reason
            elif kind == APART:
                apart[pair] = reason
        draws = {}
        for pair in SPREAD_PAIRS:
            more = sorted((c for c in cells if c[model_key] == model and c["pair"] == pair
                           and treat(c) == DONE),
                          key=lambda c: draw_of(c, registered_k1=False))
            if len(more) > 1:
                draws[pair] = {"draws": len(more),
                               "silent_loss": spread([c["silent"] for c in more]),
                               "deviations": spread([deviations(c) for c in more])}
        out[model] = {
            "common": common,
            "cells": [done[p] for p in common if p in done],
            "completed": sorted(done),
            "all_cells": [done[p] for p in sorted(done)],
            "not_completed": {p: status[(model, p)][2] for p in pairs_run if p not in done},
            "incomplete": incomplete,
            "apart": apart,
            "spread_draws": draws,
        }
    return {"common": common, "rows": out}


def quality(group: dict) -> dict:
    """The headline quality figures over the common pairs, and the full row beside them."""
    cells, every = group["cells"], group["all_cells"]
    n = len(cells)
    silent = sum(c["silent"] for c in cells)
    dev = sum(deviations(c) for c in cells)
    return {
        "silent_loss": silent,
        "silent_loss_per_pair": round(silent / n, RATE_PLACES),
        "deviations": dev,
        "deviations_per_pair": round(dev / n, RATE_PLACES),
        "pairs": n,
        "pairs_completed": len(every),
        "silent_loss_all_completed": sum(c["silent"] for c in every),
        "deviations_all_completed": sum(deviations(c) for c in every),
        "pairs_not_completed": [f"{pair} ({why})"
                                for pair, why in group["not_completed"].items()],
        # What the tested model's own verifier would forgive on top of the
        # mechanical grades. Never subtracted from the headline.
        "model_confirmed_declarations": sum(c["model_confirmed"] for c in cells),
        # Design gap 1: absent segments behind a declaration the tool rejected.
        # Silent loss keeps its definition; this is a column of its own.
        "absent_behind_rejected_declarations": sum(c["absent_rejected"] for c in cells),
    }


def per_merge(values: list[float | None], places: int) -> float | None:
    """The mean of a per-cell figure over the common pairs, or None if any is missing."""
    if not values or any(v is None for v in values):
        return None
    return mean_rounded(values, places)


# --- per cell: cost and seconds out of a report --------------------------------

def exact_usd(report: dict, recorded: float | None = None) -> float | None:
    """The priced cost of a report's answering calls, unrounded; None if not all priced.

    `provenance.answering_cost.usd_exact` when the report carries that block
    (the answering attempt's own cost, already apart from retries and
    discards). Otherwise `provenance.cost.usd_exact` when the report carries
    it. Otherwise `pricing.estimate` over the report's own ledger, which is
    the arithmetic the report's rounded `usd` came from; it must round back
    to that `usd` (or to `recorded`, a runner's own figure at four places), or
    the rates on record have moved since the run and the figure is refused
    rather than re-priced silently.
    """
    provenance = report.get("provenance") or {}
    answering_cost = provenance.get("answering_cost")
    if answering_cost is not None and "usd_exact" in answering_cost:
        return answering_cost["usd_exact"] if answering_cost.get("state") == "priced" else None
    block = provenance.get("cost") or {}
    if "usd_exact" in block:
        return block["usd_exact"] if block.get("state") == "priced" else None
    found = pricing.estimate(provenance.get("ledger") or [])
    if found.state != "priced":
        return None
    for said in (block.get("usd"), recorded):
        if said is not None and abs(round(found.dollars, 4) - round(said, 4)) > 0.00011:
            raise RuleBroken(f"the ledger prices at ${found.dollars:.6f} today and the run "
                             f"recorded ${said}; the rates moved, so this cell cannot be "
                             f"re-priced from the table")
    return found.dollars


def answer_seconds(report: dict, harness_waits: float = 0.0) -> float:
    """A cell's seconds: the answering attempt's own time, less a harness's own waits.

    `provenance.answering_seconds.total` when the report carries that block
    and it is not `None` (`answer_ms` over the rows charged to the
    model, already apart from retries, pacing and discards). Otherwise -- an
    older report, or one where nothing was timed (a replay, a cache hit) --
    the run's own duration less the waits recorded on it.
    """
    provenance = report.get("provenance") or {}
    answering_seconds = provenance.get("answering_seconds")
    if answering_seconds is not None and answering_seconds.get("total") is not None:
        return answering_seconds["total"] - harness_waits
    if provenance.get("duration_seconds") is None:
        raise RuleBroken("a counted report carries no provenance.duration_seconds")
    waited = sum(row.get("waited_ms") or 0 for row in provenance.get("ledger") or []) / 1000
    discarded = sum(row.get("latency_ms") or 0
                    for row in provenance.get("discarded_calls") or []) / 1000
    return provenance["duration_seconds"] - waited - discarded - harness_waits


def uncached_list_usd(per_model: dict[str, dict]) -> float | None:
    """The same tokens at the API's uncached list price.

    `per_model` is a `claude` envelope's `modelUsage` shape, summed over a run:
    every input token -- uncached, cache read and cache write -- at the input
    rate, every output token at the output rate. The CLI's own `costUSD`
    prices its prompt cache: reads below the input rate, writes at 1.25x (5
    minutes) or 2x (one hour) it. So its API-equivalent carries a cache
    premium and a cache discount that are properties of the CLI, and this
    figure carries neither. Web-search fees are left out: they are not
    tokens. None when any model in it is unpriced.
    """
    total = 0.0
    for model, usage in per_model.items():
        sku = pricing.sku_for(model)
        if sku is None:
            return None
        price = pricing.PRICES[sku]
        tokens_in = sum(int(usage.get(k) or 0) for k in (
            "inputTokens", "cacheReadInputTokens", "cacheCreationInputTokens"))
        total += (tokens_in * price.input + int(usage.get("outputTokens") or 0)
                  * price.output) / 1_000_000
    return total


def stated(notes: str, pattern, values: tuple) -> tuple[list[str], str]:
    """A figure a row's notes state in prose, checked and rewritten like a field.

    `pattern` is the sentence with each figure a group; it must occur in
    `notes` exactly once, or the claim moved and a check would be blind to it.
    Returns the differences, and the notes with every group set to `values`.
    """
    found = list(pattern.finditer(notes))
    if len(found) != 1:
        return [f"notes state {pattern.pattern!r} {len(found)} times, not once"], notes
    match, want = found[0], tuple(str(v) for v in values)
    problems = [] if match.groups() == want else [
        f"notes say {match.group(0)!r}; the cells give {want}"]
    out = notes
    for index in reversed(range(len(want))):
        start, end = match.span(index + 1)
        out = out[:start] + want[index] + out[end:]
    return problems, out


# --- writing formed figures back into catalogue.json ---------------------------
#
# `catalogue.json` is laid out by hand: arrays on one line, nested blocks
# expanded. A figure script's `--write` changes the value of a derived field
# in place, in the layout it already has, and adds a new field on its own
# line before `run`; nothing else in the file moves. What it wrote is then
# parsed back and compared with what was meant.

_DECODER = json.JSONDecoder()


def _ws(text: str, pos: int) -> int:
    while pos < len(text) and text[pos] in " \t\r\n":
        pos += 1
    return pos


def _value_end(text: str, pos: int) -> int:
    return _DECODER.raw_decode(text, pos)[1]


def _entries(text: str, start: int):
    """(key, key offset, value start, value end) of each member of the object at `start`."""
    if text[start] != "{":
        raise RuleBroken(f"catalogue.json: expected an object at offset {start}")
    pos = _ws(text, start + 1)
    while text[pos] != "}":
        key, after = _DECODER.raw_decode(text, pos)
        colon = _ws(text, after)
        value = _ws(text, colon + 1)
        end = _value_end(text, value)
        yield key, pos, value, end
        pos = _ws(text, end)
        if text[pos] == ",":
            pos = _ws(text, pos + 1)


def _locate(text: str, path: list) -> tuple[int, int]:
    """(start, end) offsets of the JSON value at `path` (keys and list indices)."""
    start = _ws(text, 0)
    for step in path:
        if isinstance(step, int):
            if text[start] != "[":
                raise RuleBroken(f"catalogue.json: {path}: {step} indexes a non-list")
            pos = _ws(text, start + 1)
            for _ in range(step):
                pos = _ws(text, _value_end(text, pos))
                pos = _ws(text, pos + 1)  # the comma
            start = pos
        else:
            found = next((value for key, _, value, _ in _entries(text, start) if key == step),
                         None)
            if found is None:
                raise RuleBroken(f"catalogue.json: {path}: no key {step!r}")
            start = found
    return start, _value_end(text, start)


def _render(value, old: str, indent: str) -> str:
    """`value` in the layout `old` had: one line, or expanded under a key line at `indent`."""
    if "\n" not in old:
        return json.dumps(value, ensure_ascii=False)
    return json.dumps(value, indent=2, ensure_ascii=False).replace("\n", "\n" + indent)


def set_field(text: str, container: list, key: str, value, before: str = "run") -> str:
    """`text` with `container[key] = value`, in place; a new key goes on its own line before `before`."""
    start, _ = _locate(text, container)
    members = {k: (at, v, e) for k, at, v, e in _entries(text, start)}
    if key in members:
        _, v, e = members[key]
        if json.loads(text[v:e]) == value:
            return text
        line = text[text.rfind("\n", 0, v) + 1:v]
        indent = line[:len(line) - len(line.lstrip())]
        return text[:v] + _render(value, text[v:e], indent) + text[e:]
    if before not in members:
        raise RuleBroken(f"catalogue.json: {container} has no {before!r} to insert {key!r} before")
    at = members[before][0]
    line_start = text.rfind("\n", 0, at) + 1
    indent = text[line_start:at]
    return (text[:line_start] + f"{indent}{json.dumps(key)}: "
            f"{json.dumps(value, ensure_ascii=False)},\n" + text[line_start:])


def write_catalogue(path: Path, edits: list[tuple[list, str, object]]) -> bool:
    """Apply (container path, key, value) edits to catalogue.json; True if it changed.

    The result must parse, and every edited field must read back as the value
    it was given, or nothing is written.
    """
    old = path.read_text(encoding="utf-8")
    text = old
    for container, key, value in edits:
        text = set_field(text, container, key, value)
    data = json.loads(text)
    for container, key, value in edits:
        node = data
        for step in container:
            node = node[step]
        if node.get(key) != value:
            raise RuleBroken(f"catalogue.json: {container}.{key} did not read back as written")
    if text != old:
        path.write_text(text, encoding="utf-8")
    return text != old


def raw_catalogue() -> dict:
    """catalogue.json as it is on disk, parsed and not validated: a write may be
    the one that makes it valid again."""
    from llossless.web import catalogue
    return json.loads(catalogue.DEFAULT_PATH.read_text(encoding="utf-8"))


def entry_index(data: dict, block: str, field: str, ident: str) -> int:
    """Where the entry whose `field` is `ident` sits in `data[block]`."""
    hits = [i for i, entry in enumerate(data[block]) if entry.get(field) == ident]
    if len(hits) != 1:
        raise RuleBroken(f"catalogue.json: {len(hits)} {block} entries with {field} {ident!r}")
    return hits[0]


def commit_of(cells: list[dict], what: str) -> str:
    """The one tool commit a row's cells ran at, twelve characters. A `-dirty`
    or `-unknown` stamp is refused before it is cut to the pin's length."""
    stamps = {str(c["claimcheck_commit"]) for c in cells}
    if len(stamps) != 1:
        raise RuleBroken(f"expected one tool commit for {what}, found {sorted(stamps)}")
    stamp = stamps.pop()
    if "-" in stamp:
        raise RuleBroken(f"{what} ran at {stamp!r}, not a clean commit")
    return stamp[:12]
