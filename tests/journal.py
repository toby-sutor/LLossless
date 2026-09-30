"""The exclude-cached rule, in one place instead of three.

A cache hit returns recorded bytes in microseconds and reports zero completion
tokens -- `_fetch`'s cache branch returns at `client.py:386` without touching
`usage.completion_tokens`, the same shape as the replay branch -- so any
per-call metric that counts one is describing disk rather than an endpoint. It
drags a latency mean toward zero and a token-budget ratio toward zero, and in
both directions the wrong answer is the reassuring one.

The rule was written three times before it was written once. `analyse_merges`
holds it as a default on a shared helper; `run_merge.latency_summary` and
`run_merge._slower` open-code it separately. The second of those was written
wrong first, averaging replays on a corpus three-quarters replayed and reporting
2% of ceiling where the live calls said 22%. Once is an oversight, twice is a
missing default, and three times is this module.

So the default lives here rather than in each caller's head. A caller that
genuinely wants them -- `analyse_merges.census`, whose whole job is counting
them -- passes `include_recorded=True` and says so at the call site.

Gathering the rule in one place is also what showed the rule was wrong. All
three copies tested `cached` alone, and the cassette branch does not set it, so
`run_merge.py --offline --journal` called 288 replays live calls. `recorded()`
takes the union of both disk paths.

Nothing here opens a socket, imports a third-party package, or knows what a
merge is. It reads JSONL and filters dictionaries.
"""

from __future__ import annotations

import json
from pathlib import Path


def records(path: Path) -> list[dict]:
    """Every journal record in a JSONL file, or none if it was never written.

    A missing journal is not an error: `--journal` is optional, and a caller
    that summarises one has nothing to say when it is absent. Blank lines are
    skipped because a run killed mid-write can leave one.
    """
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def recorded(record: dict) -> bool:
    """True when the answer came off disk, by either route.

    The cache and the cassette are separate branches of `_fetch` and only the
    cache one sets `cached` -- so `not record["cached"]` reads as "live" on a
    replayed call and is the wrong predicate. Writing the union once is the
    whole point of this module; writing it correctly once is the point of
    writing it once. A journal from before the `replayed` field existed answers
    False here, which is what those runs recorded and not a guess.
    """
    return bool(record.get("cached") or record.get("replayed"))


def steps(
    entries: list[dict],
    step: str | None = None,
    condition: str | None = None,
    *,
    include_recorded: bool = False,
) -> list[dict]:
    """Journal records for one step and condition, **live calls only by default**."""
    chosen = entries if include_recorded else [r for r in entries if not recorded(r)]
    if step is not None:
        chosen = [r for r in chosen if r["step"] == step]
    if condition is not None:
        chosen = [r for r in chosen if r["condition"] == condition]
    return chosen


def measurable(*units) -> bool:
    """True when every unit made a real call and can be compared on timing.

    The in-memory half of the same rule. `steps()` filters journal records;
    this answers the question for `Unit` objects the sweep is still holding,
    where the same two flags have to mean the same thing. A cached or replayed
    merge has no latency of its own, and a zero would read as "fast" rather
    than "not measured" -- so the caller treats a False here as no evidence,
    never as evidence against.
    """
    return not any(
        getattr(unit, "merge_cached", False) or getattr(unit, "merge_replayed", False)
        for unit in units
    )
