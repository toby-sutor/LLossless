#!/usr/bin/env python3
"""The fair-lineup benchmark runner: one registration, a pinned clone, one cell at a time.

A benchmark is registered before it runs, and this program runs one
registration: it
reads the machine block of one `REGISTRATION.md`, refuses to start unless the
clone it runs from is the registered pin and clean, and then runs every cell
(model x set item x draw) of one lane as `python -m llossless` from that
clone, serially, recording each attempt in an append-only `cells.jsonl` that
it resumes from.

What it enforces:

- **The pin**. This file must be the clone's own
  `tests/run_lineup.py`; the clone's HEAD is the registered pin and
  `git status --porcelain --ignored` is empty, before and after every cell;
  every report's `claimcheck_commit` is the pin with no `-dirty` and no
  `claimcheck_commit_changed`; every prompt a report names is under the
  clone's `prompts/` at the digest recorded when the run first started; the
  input files copied into each cell hash to the sha256 list recorded then.
- **Every row priced or said unpriced** (`sku_for`): a row's model
  has a SKU in the clone's `pricing.py`, or the row carries an `unpriced`
  reason. A metered row must be priced and have a cap.
- **The flags**: `--effort` per role on every command route,
  `--thinking` per the registration, `--structured prompt` pinned, `--timeout`,
  `--window`, `--field-order`, `--profile`, `--no-cache`, `--title-policy`,
  `--base`, stated on every call; the report is then asserted to say the same
  (`decoding.thinking`, `decoding.profile`, `decoding.effort`,
  `structured_output`, `merge_policy`, `window`, safe mode and tools per role).
- **The environment**: the child starts from this process's environment
  less every `CLAUDE*`, `AI_AGENT*`, `LLOSSLESS_*`, `CLAIMCHECK_*`,
  `ANTHROPIC*`, `OPENAI*` and `PYTHON*` name, plus only what the runner sets.
  The `claude` wrapper logs the names (never values) it was started with on
  every call, and a forbidden name that reached it stops the lane.
  `DISABLE_AUTOUPDATER=1` is set.
- **The `claude` binary**: the registered copy's sha256 before and after
  every cell, its `--version` once per start, and the realpath, size, inode and
  mtime the wrapper saw on every call, all constant.
- **The model that answered**: the row's model is the label
  (`provenance.models`), the argv's `--model`, and every ledger row's
  `answered_by.output` (command route) or `served_model` (HTTP), give or take
  a date suffix or a registered `served_aliases` entry.
- **Failures that are not the model's**. Each attempt is
  classified `ok` (the run completed; unruled calls inside it are counted
  beside it, never discard it), `model_failure` (a result, and only on
  positive evidence that the model's own output failed after the tool's
  repairs: no usable response, a complete answer in the wrong order, a
  repetition loop, corroborated by a ledger row whose `outcome` is `failed`),
  `refused` (a refusal on either route: a `content_filter` blank, the CLI's
  refusal; final, never retried), `unruled` (the open cases that ended the
  run: a ceiling cut, a blank on length; read off the report's structured
  fields), `window` (the stated window cannot hold the task: the tool said so
  before sending, or the endpoint's 400 named the context
  length), `platform` (a 408/409/425/429/5xx, a blank, a timeout, a cut
  stream, the CLI's blank result; excluded, re-queued), `unclassified` (anything
  not recognised: excluded and re-queued like `platform`, never a model
  failure), `usage_limit` (the subscription's limit, or a vendor's spend,
  credit or quota message: the lane stops, or sleeps to the parsed reset on
  the subscription), `halted` (a runner assertion, a configuration or account
  fault: the lane stops, loudly). A breaker stops a lane after N non-model
  failures in a row.
- **Money**. A cell is charged what its report says was
  billed: `answering_cost` plus `excluded.cost` plus `unruled.cost`, exact,
  with each call that may have been billed and reported no usage charged one
  conservative call estimate (a 5xx or a transport retry is charged nothing).
  Without a report: nothing when the merge died on an HTTP status, the whole
  projection when the process was killed or crashed, one call estimate
  otherwise. Never an estimate for an attempt that was not made. Before each cell the
  projection (the most this item has cost this row so far, or a size-scaled
  figure, or the registered estimate) times the margin must fit under the
  vendor cap and the overall cap, or the lane stops. A self-hosted lane may
  register `gpu_seconds`, a cap on its cells' wall seconds and its pre-warms,
  gated the same way.
- **The pod's address**: every evidence file the runner writes, and
  every journal line, has the value of each `base_url_env` and
  `health_url_env` replaced (the whole URL by `$NAME`, its host forms by
  `<redacted>`), as `scripts/stream_redact.py` does for a runner's streams.
- **A torn journal**: a last line a crash cut short is moved to a side
  file with a loud warning, and the run continues; any other line that is not
  JSON still refuses.
- **Pre-warm**: a lane with a `prewarm` block waits for health and
  sends one untimed warm-up request before its first cell, before each retry
  pass and after an idle gap; it is an event in `cells.jsonl`, never a cell.
- **Order**: pair-major with the rows rotated per item, draw-major
  across draws, sets in registration order.

Modes:

    run_lineup.py template [--pilot] --pin HASH --out REGISTRATION.md
    run_lineup.py check    --registration R [--lane L]   preflight only, no call
    run_lineup.py plan     --registration R [--lane L]   the ordered cells, states
    run_lineup.py run      --registration R --lane L     run and resume
    run_lineup.py status   --registration R              states and spend
    run_lineup.py note     --registration R --lane L TEXT   an operator note
    run_lineup.py amend    --registration R --reason TEXT   accept a changed block
    run_lineup.py fit      --registration R --row ROW    each merge item's window need
    run_lineup.py thinking-pilot --registration R --row ROW --items S1:rate_limits,...

- **Reference checks and outages**. A cell still failing on the platform
  after every retry pass sends one cheap cell (`reference_item`) to the row's
  registered reference route on another vendor. It works: the cell is the
  row's `endpoint_failure`, counted against it. It fails too: `infrastructure`,
  never scored; the lane writes `OPERATOR-ATTENTION.txt`, pauses and probes
  (`infrastructure`), and resumes on its own. The breaker asks the same
  question. A retry of a cell reuses that cell's own earlier live answers
  (its per-attempt `cache/`, `reuse.json`), each counted once at its
  original time and cost. Nothing finished is ever re-run.

Exit codes of `run`: 0 lane complete; 3 gated by a cap; 4 usage limit; 5
halted (assertion, configuration or account); 6 the breaker on an endpoint
whose reference works, or a pre-warm that never came up; 7 complete with
excluded cells left after every retry pass; 8 paused_infrastructure (the
registered maximum pause passed; `run` again continues); 2 a refusal before
the first cell.
"""
from __future__ import annotations

import sys

# Nothing this process imports from the clone may leave a `.pyc` in it: the
# clone's `git status --porcelain --ignored` must stay empty (see `git_state`).
sys.dont_write_bytecode = True

import argparse  # noqa: E402
import contextlib  # noqa: E402
import fcntl  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import shlex  # noqa: E402
import shutil  # noqa: E402
import signal  # noqa: E402
import statistics  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import urllib.error  # noqa: E402
import urllib.request  # noqa: E402
from dataclasses import dataclass, field  # noqa: E402
from datetime import datetime, timedelta, timezone  # noqa: E402
from pathlib import Path  # noqa: E402
from urllib.parse import urlsplit  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from llossless import config, pricing  # noqa: E402

ROLES = tuple(sorted(config.ROLES))
REGISTRATION_FENCE = "```json lineup-registration"

EXIT_DONE = 0
EXIT_PREFLIGHT = 2
EXIT_GATED = 3
EXIT_USAGE_LIMIT = 4
EXIT_REFUSED = 5
EXIT_BREAKER = 6
EXIT_EXCLUDED_LEFT = 7
EXIT_PAUSED = 8  # paused_infrastructure: the registered maximum pause passed

# Final: never re-run. Retryable: re-queued for a later pass, bounded. Stop: the
# lane stops and the cell is re-run on the next start. `refused` is a refusal by
# the model or its vendor; the runner's own stop is `halted` (an earlier
# version called it `refused`). `endpoint_failure` is a verdict,
# not a run: the cell failed on the platform after every retry pass while the
# registered reference route answered, so the endpoint's failure is the row's.
# `infrastructure` is the other verdict: the reference failed too, the
# network or the machine is at fault, the lane pauses and probes, and the cell
# is run again when it comes back. Never a model failure, never scored.
# `harness_timeout` (found in the 27B's live test): on a self-hosted row, a call the
# tool's own `--timeout` cut after the endpoint took it, or a cell the runner's
# wall limit stopped. The harness's setting was too short for the card: a
# `config` failure of the registration, documented, never the model's and
# never a runaway. Final: a slow card is slow again on a retry.
FINAL_STATES = ("ok", "model_failure", "unruled", "window", "refused", "endpoint_failure",
                "harness_timeout")
RETRYABLE_STATES = ("platform", "unclassified", "interrupted")
STOP_STATES = ("usage_limit", "halted", "infrastructure")
STATES = FINAL_STATES + RETRYABLE_STATES + STOP_STATES
# The headline rules, ruled by the operator on 2026-09-28. A refusal
# counts against the row ("a model failure and needs to be flagged"), fixed: no
# longer a switch. `unruled_counts` and `platform_lost` are gone: an unruled
# cell always counts against its row, and nothing shrinks the common
# pairs any more (the operator: "if a model fails repeatedly let the model fail. Do
# not remove the pass for everyone"). A registration naming either is refused.
RULES = {"refusal_counts": ("row",)}
RULE_DEFAULTS = {name: allowed[0] for name, allowed in RULES.items()}
REMOVED_RULES = {
    "unruled_counts": "an unruled cell always counts against its row (operator ruling, 2026-09-28)",
    "platform_lost": "nothing shrinks the common pairs; a pair the platform kept from a row "
                     "is that row's alone, and after the retry passes the reference check "
                     "decides (operator ruling, 2026-09-28)",
}
# The flags a row carries beside its own failures, in the cell record and
# in figures.md.
REFUSED_FLAG = "refused (prompt or guardrail)"
ENDPOINT_FLAG = "endpoint failed while reference worked"
HARNESS_FLAG = ("CONFIG: cut by the harness's own timeout, not the model; the registration's "
                "timeout is too short for this card (documented in the run report)")
# By ruling: Haiku has one effort level (extended thinking on or off). Its rows
# register `single_level`, the runner passes no `--effort`, and the model's
# default is kept. Only a model this pattern names may register it.
SINGLE_LEVEL = "single_level"
SINGLE_LEVEL_MODELS = re.compile(r"^claude-haiku-")
SINGLE_LEVEL_LABEL = "one level (extended thinking on/off; default kept)"
HOSTINGS = ("vendor", "self")
# By the outage ruling: the states whose attempt's successful live calls a
# later attempt of the same cell may reuse. A `halted` attempt only when no
# runner assertion failed on it (a wrong model, a moved tree), which the end
# record says as `assertions_failed`.
REUSE_FROM_STATES = ("platform", "unclassified", "interrupted", "usage_limit", "halted")

# Never handed to the child, whatever the lane. `PYTHON*` too:
# the runner sets the child's own `PYTHONPATH`, and a stray `PYTHONHOME` or
# `PYTHONSTARTUP` would change what runs.
FORBIDDEN_ENV = re.compile(r"^(CLAUDE|AI_AGENT|LLOSSLESS_|CLAIMCHECK_|ANTHROPIC|OPENAI)")
# The same prefixes, as the detector reads them: a second object on purpose, so
# the check that a name reached the child does not share its regex with the
# scrub it checks (a narrowed scrub must not narrow its own alarm).
FORBIDDEN_AT_CHILD = re.compile(r"^(?:CLAUDE|AI_AGENT|LLOSSLESS_|CLAIMCHECK_|ANTHROPIC|OPENAI)")
DROPPED_ALSO = re.compile(r"^PYTHON")
# The only `LLOSSLESS_*` names the runner itself hands the child. Everything
# else the run needs is a flag on the argv, where `argv.json` shows it.
RUNNER_SET = frozenset({"LLOSSLESS_API_KEY_ENV", "LLOSSLESS_CACHE_DIR",
                        "LLOSSLESS_COMMAND", "LLOSSLESS_COMMAND_ENVELOPE",
                        "LLOSSLESS_COMMAND_LABEL"})
KEY_VAR = "LINEUP_API_KEY"
CALLS_VAR = "LINEUP_CALLS"

# Classification patterns. Read off the tool's own messages (backend.py,
# transport.py, client.py, cli.step) and the envelopes the wrapper keeps.
#
# A failure nothing below recognises is `unclassified` (re-queued,
# the breaker is the net), never the model's. `model_failure` needs the tool's
# own sentence that the model's output failed after its repairs, at the start
# of the step's detail as `cli.step` writes a `SchemaFailure` (no class name in
# front), and a ledger row whose `outcome` is `failed` beside it.
MODEL_OUTPUT = re.compile(
    r"^[a-z_]+: (?:model did not return a usable response after \d+ attempts"
    r"|\S+ gave every field this response needs, valid, and in the wrong order"
    r"|\S+ answered in a repetition loop)")
# The subscription's own limit, in a CLI envelope or its stderr.
USAGE_LIMIT = re.compile(r"usage limit|limit reached|hit your limit|limit will reset|"
                         r"resets at|resets \d|out of extra usage", re.I)
# A vendor's spend, credit or quota limit on a metered key: the lane
# stops, and resuming after a top-up re-runs the cell. The Anthropic 400 of
# 2026-09-18 (`arms/2026-09-18/matrix/results_anthropic.json`), Anthropic's
# credit message, OpenAI's `insufficient_quota` 429. Not applied to Google's
# free tier, whose per-minute quota says "exceeded your current quota" too.
SPEND_LIMIT = re.compile(
    r"specified API usage limits|will regain access on|credit balance is too low|"
    r"insufficient_quota|exceeded your current quota|billing_hard_limit_reached|"
    r"spend(?:ing)? limit|out of credits|purchase (?:more )?credits|"
    r"insufficient (?:credits|balance|funds)", re.I)
PER_DAY_QUOTA = re.compile(r"PerDay|per[ -]day", re.I)
FREE_QUOTA = re.compile(r"exceeded your current quota", re.I)
BILLING = re.compile(r"billing|prepa(?:y|id)|credit balance|payment", re.I)
# A fault in the configuration, the account or the run's own contract: the
# lane stops, loudly, and the cell is re-run after the fix. A lost or expired
# subscription login is one: never a model failure, never retried in a loop.
HALT_DETAIL = re.compile(
    r"HTTP 40[134]\b|api_error_status=40[13]\b|API Error: 40[13]\b|no such program|"
    r"CommandNotFound|version \S+ or newer is required|claude_code_version_too_old|"
    r"PinnedTierViolated|ConfigError|UnknownPrice|CallBudgetExceeded|ThinkingIgnored|"
    r"ThinkingNotHonoured|TierUnsupported|run /login|Invalid API key|OAuth|"
    r"authentication_error|not logged in", re.I)
# A refusal, on either route: the vendor's filter or the model's own.
REFUSAL_TEXT = re.compile(
    r"violat\w* (?:our|the|its) usage polic|unable to respond to this request|"
    r"\bcontent_filter\b|\binvalid_prompt\b", re.I)
# The tool refused before sending because the stated window cannot hold the
# task, or the endpoint's 400 named the context length.
WINDOW_DETAIL = re.compile(r"BudgetExceedsWindow|WindowUnknown|WindowUnmeasurable")
STATUS_4XX = re.compile(r"HTTP 4(?:00|13|22)\b|api_error_status=4(?:00|13)\b|"
                        r"API Error: 4(?:00|13)\b")
CONTEXT_TEXT = re.compile(r"maximum context length|context[_ ]length|prompt is too long|"
                          r"too many (?:input )?tokens|max_model_len|context window", re.I)
# A blank on either route (the path's, not the model's), unless the
# report's structured fields say it was a refusal or a runaway (below).
BLANK_DETAIL = re.compile(r"EmptyResponse|EmptyBody|empty body|exited 0 and wrote nothing|"
                          r"result envelope whose `result` is empty")
# Excluded and re-queued. No bare `HTTPStatusError`: a 400 that is not a
# context length, a spend limit or a refusal is not known to be the platform's.
PLATFORM_DETAIL = re.compile(
    r"HTTP (?:408|409|425|429|5\d\d)\b|StreamTruncated|TransportError|timed out|Timeout|"
    r"produced nothing for|ConnectionError|Connection refused|Connection reset|URLError|"
    r"RemoteDisconnected|Remote end closed|overloaded|\b52[49]\b|Cancelled|"
    r"api_error_status=(?:429|5\d\d)", re.I)
# The network itself: the machine could not reach anything. Read before a
# halt, because the CLI can name its login while the real fault is that it could
# not reach the server to refresh it. Never the model's, and never a halt.
NETWORK_DETAIL = re.compile(
    r"ENOTFOUND|EAI_AGAIN|ECONNREFUSED|ECONNRESET|ETIMEDOUT|ENETUNREACH|EHOSTUNREACH|"
    r"Connection error|fetch failed|socket hang up|Name or service not known|"
    r"Temporary failure in name resolution|Network is unreachable|No route to host|"
    r"getaddrinfo", re.I)
# The tool's own per-call timeout, after the endpoint took the request
# (`transport.timed_out(sent=True)`): the endpoint was up and generating, and the
# budget was what was wrong. On a self-hosted row that is `harness_timeout`.
HARNESS_TIMEOUT = re.compile(r"did not finish answering within \d")
# When one report holds several errored steps: the run's own contract first,
# then the row's own results, then what is not the model's.
PRECEDENCE = ("halted", "model_failure", "refused", "unruled", "window", "harness_timeout",
              "unclassified", "platform")
USAGE_LIMIT_MARGIN = 120  # seconds past a parsed reset before the subscription lane resumes
USAGE_LIMIT_SLEEPS = 3    # consecutive sleeps before a limit that will not lift stops the lane
DATE_SUFFIX = r"(?:-\d{4}-?\d{2}-?\d{2})?"
WARM_UP_PROMPT = "LINEUP WARM-UP: reply with the single word OK."
THINKING_PILOT_FLAG = 0.60  # a ceiling more than 60% used is flagged


class Refusal(SystemExit):
    """The runner will not start or continue. Raised with the reason, never swallowed."""

    def __init__(self, message: str, code: int = EXIT_PREFLIGHT) -> None:
        super().__init__(code)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return self.message


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


# --- the registration ---------------------------------------------------------------

def parse_registration(path: Path) -> tuple[dict, str]:
    """The machine block of a REGISTRATION.md, and the sha256 of that block's text."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == REGISTRATION_FENCE]
    if len(starts) != 1:
        raise Refusal(f"{path}: expected exactly one {REGISTRATION_FENCE!r} block, "
                      f"found {len(starts)}")
    end = next((i for i in range(starts[0] + 1, len(lines)) if lines[i].strip() == "```"),
               None)
    if end is None:
        raise Refusal(f"{path}: the registration block is not closed")
    block = "\n".join(lines[starts[0] + 1:end])
    try:
        data = json.loads(block)
    except ValueError as exc:
        raise Refusal(f"{path}: the registration block is not JSON: {exc}") from None
    return data, hashlib.sha256(block.encode("utf-8")).hexdigest()


def _fills(value, where: str = "") -> list[str]:
    if isinstance(value, str):
        return [where] if "<FILL" in value else []
    if isinstance(value, dict):
        return [hit for key, item in value.items() for hit in _fills(item, f"{where}.{key}")]
    if isinstance(value, list):
        return [hit for i, item in enumerate(value) for hit in _fills(item, f"{where}[{i}]")]
    return []


def route_kind(row: dict) -> str:
    return row["route"]["kind"]


def metered(row: dict) -> bool:
    """Billed in dollars against a cap. HTTP rows are, unless they say not."""
    return bool(row.get("metered", route_kind(row) == "http"))


def items_of(reg: dict, row: dict, set_id: str) -> list[str]:
    allowed = reg["sets"][set_id]["items"]
    chosen = (row.get("items") or {}).get(set_id)
    return list(allowed if chosen is None else chosen)


def draws_of(reg: dict, row: dict, set_id: str, item: str) -> int:
    table = (row.get("draws") or {}).get(set_id) or reg["sets"][set_id].get("draws") or {}
    return int(table.get(item, table.get("default", 1)))


def validate(reg: dict) -> list[str]:
    """Every reason the registration cannot run. Empty means it can."""
    out = [f"unfilled placeholder at {hit}" for hit in _fills(reg, "registration")]
    if out:
        return out
    if reg.get("registration") != 1:
        out.append("registration: expected 1 (the block's format version)")
    if not re.fullmatch(r"[0-9a-f]{40}", str(reg.get("pin", ""))):
        out.append(f"pin: a full 40-character commit hash, got {reg.get('pin')!r}")
    settings = reg.get("settings") or {}
    for key in ("timeout", "structured", "title_policy", "verify_depth", "base"):
        if key not in settings:
            out.append(f"settings.{key}: missing")
    if settings.get("structured") not in (None, "prompt", "json_schema", "tool_call"):
        out.append(f"settings.structured: {settings.get('structured')!r} is not a pinned tier")
    if settings.get("title_policy") not in (None, *config.TITLE_POLICIES):
        out.append(f"settings.title_policy: {settings.get('title_policy')!r}")
    if settings.get("verify_depth") not in (None, *config.VERIFY_DEPTHS):
        out.append(f"settings.verify_depth: {settings.get('verify_depth')!r}")
    sets = reg.get("sets") or {}
    if not sets:
        out.append("sets: none registered")
    for set_id, spec in sets.items():
        if spec.get("kind") not in ("merge", "detect"):
            out.append(f"sets.{set_id}.kind: merge or detect, got {spec.get('kind')!r}")
        if spec.get("kind") == "merge" and spec.get("fidelity") not in config.FIDELITY_LEVELS:
            out.append(f"sets.{set_id}.fidelity: {spec.get('fidelity')!r}")
        if spec.get("score") not in ("pairs", "detect", "planted"):
            out.append(f"sets.{set_id}.score: pairs, detect or planted")
        if not spec.get("items"):
            out.append(f"sets.{set_id}.items: none")
    lanes = reg.get("lanes") or {}
    caps = reg.get("caps") or {}
    for name, value in caps.items():
        if not isinstance(value, (int, float)) or value < 0:
            out.append(f"caps.{name}: a number of dollars, got {value!r}")
    for name, spec in lanes.items():
        cap = (spec or {}).get("gpu_seconds")
        if cap is not None and (not isinstance(cap, (int, float)) or cap <= 0):
            out.append(f"lanes.{name}.gpu_seconds: a positive number of seconds, got {cap!r}")
    for name, value in (reg.get("rules") or {}).items():
        if name in REMOVED_RULES:
            out.append(f"rules.{name}: removed, {REMOVED_RULES[name]}")
        elif name not in RULES:
            out.append(f"rules.{name}: not a rule; the rules are {sorted(RULES)}")
        elif value not in RULES[name]:
            out.append(f"rules.{name}: fixed at {RULES[name][0]!r} by operator ruling of 2026-09-28, "
                       f"got {value!r}")
    ids = [row.get("id") for row in reg.get("rows") or []]
    references = {ref.get("id"): ref for ref in reg.get("references") or []}
    if len(ids) != len(set(ids)):
        out.append(f"rows: duplicate ids {sorted(i for i in ids if ids.count(i) > 1)}")
    if not ids:
        out.append("rows: none registered")
    if set(ids) & set(references):
        out.append(f"references: an id shared with a row: {sorted(set(ids) & set(references))}")
    out += _validate_reference_item(reg, sets)
    named = {row.get("reference") for row in reg.get("rows") or []}
    for ref in reg.get("references") or []:
        # Only a reference some row names is ever run, so only it must be capped.
        if ref.get("id") in named:
            out += _validate_route(ref, f"references.{ref.get('id')}", caps, lanes,
                                   is_reference=True)
    infra = reg.get("infrastructure") or {}
    urls = infra.get("probe_urls")
    if not isinstance(urls, list) or not urls or not all(isinstance(u, str) and (
            u.startswith(("http://", "https://")) or re.fullmatch(r"\$[A-Z_][A-Z0-9_]*", u))
            for u in urls):
        out.append("infrastructure.probe_urls: a list of http(s) URLs (or $NAME for an "
                   f"address held in the environment), got {urls!r}")
    intervals = infra.get("probe_intervals_seconds")
    if not isinstance(intervals, list) or not intervals or not all(
            isinstance(v, (int, float)) and v > 0 for v in intervals):
        out.append(f"infrastructure.probe_intervals_seconds: a non-empty list of positive "
                   f"seconds, got {intervals!r}")
    if not isinstance(infra.get("max_pause_seconds"), (int, float)) or \
            infra.get("max_pause_seconds") < 0:
        out.append(f"infrastructure.max_pause_seconds: the most a lane may pause for an "
                   f"outage in one start, in seconds, got {infra.get('max_pause_seconds')!r}")
    has_claude = False
    for row in reg.get("rows") or []:
        rid = row.get("id")
        where = f"rows.{rid}"
        for key in ("model", "lane", "vendor", "route", "thinking", "window", "sets",
                    "reference"):
            if key not in row:
                out.append(f"{where}.{key}: missing")
        if any(key not in row for key in ("model", "lane", "vendor", "route")):
            continue
        if row["lane"] not in lanes:
            out.append(f"{where}.lane: {row['lane']!r} is not a registered lane")
        ref = references.get(row.get("reference"))
        if "reference" in row and ref is None:
            out.append(f"{where}.reference: {row.get('reference')!r} is not a registered "
                       f"reference route")
        elif ref is not None and (ref.get("vendor") == row["vendor"]
                                  or ref.get("route") == row["route"]):
            out.append(f"{where}.reference: {ref.get('id')!r} is on the row's own vendor or "
                       f"route; a reference must be a different endpoint")
        out += _validate_route(row, where, caps, lanes)
        kind = row["route"].get("kind")
        if kind == "claude":
            has_claude = True
        for set_id in row.get("sets") or []:
            if set_id not in sets:
                out.append(f"{where}.sets: {set_id!r} is not a registered set")
                continue
            if sets[set_id].get("fidelity") == config.SOURCED and kind != "claude":
                out.append(f"{where}.sets: {set_id} is at sourced, which an HTTP route "
                           f"refuses by design; command routes only")
            chosen = (row.get("items") or {}).get(set_id)
            if chosen is not None and not set(chosen) <= set(sets[set_id]["items"]):
                out.append(f"{where}.items.{set_id}: not a subset of the set's items")
        if row.get("items") and row.get("headline", True):
            out.append(f"{where}: a row on a subset of the items cannot be in the headline "
                       f"(it would shrink every row's common pairs); set headline: false")
        if row.get("compare_with") and row["compare_with"] not in ids:
            out.append(f"{where}.compare_with: no row {row['compare_with']!r}")
    if has_claude:
        claude = reg.get("claude") or {}
        for key in ("path", "sha256", "version"):
            if not claude.get(key):
                out.append(f"claude.{key}: required when a row answers through `claude`")
    retry = reg.get("retry") or {}
    if not isinstance(retry.get("passes", 0), int) or retry.get("passes", 0) < 0:
        out.append("retry.passes: a whole number")
    return out


def _validate_reference_item(reg: dict, sets: dict) -> list[str]:
    """The one cheap cell a reference route runs, `SET:item` of a merge set."""
    spec = str(reg.get("reference_item") or "")
    set_id, _, item = spec.partition(":")
    if set_id not in sets or item not in (sets[set_id].get("items") or []) or \
            sets[set_id].get("kind") != "merge":
        return [f"reference_item: SET:item of a registered merge set (the smallest, "
                f"S1:badge_access), got {spec!r}"]
    return []


def _validate_route(row: dict, where: str, caps: dict, lanes: dict, *,
                    is_reference: bool = False) -> list[str]:
    """Every rule a row's route, effort, window, hosting and price must meet.

    Shared by the counted rows and the reference routes, which run one
    asserted cell each and are charged like any metered row.
    """
    out = []
    if is_reference:
        for key in ("id", "model", "vendor", "route", "thinking", "window"):
            if key not in row:
                out.append(f"{where}.{key}: missing")
        if any(key not in row for key in ("model", "vendor", "route")):
            return out
    route = row["route"]
    kind = route.get("kind")
    if kind not in ("http", "claude"):
        return out + [f"{where}.route.kind: http or claude, got {kind!r}"]
    if is_reference and kind != "http":
        out.append(f"{where}.route.kind: a reference route is an HTTP API route")
    profile = route.get("profile", "subscription" if kind == "claude" else None)
    from llossless import structured  # noqa: PLC0415
    if profile not in structured.PROFILES:
        out.append(f"{where}.route.profile: {profile!r} is not one of "
                   f"{sorted(structured.PROFILES)}")
    hosting = row.get("hosting")
    if hosting not in HOSTINGS:
        out.append(f"{where}.hosting: one of {list(HOSTINGS)} (who owns a "
                   f"ceiling or a window), got {hosting!r}")
    for key in ("timeout", "cell_wall_seconds"):
        if key in row and (not isinstance(row[key], (int, float)) or row[key] <= 0):
            out.append(f"{where}.{key}: a positive number of seconds, got {row[key]!r}")
    if hosting == "self":
        if not isinstance(row.get("timeout"), (int, float)):
            out.append(f"{where}.timeout: a self-hosted row registers its own per-call "
                       f"timeout for its card (at least 2400 s for the 27B), got "
                       f"{row.get('timeout')!r}")
        limits = row.get("model_limits") or {}
        if not all(isinstance(limits.get(k), int) and limits[k] > 0
                   for k in ("context_tokens", "output_tokens")) or not str(
                       limits.get("source") or "").strip():
            out.append(f"{where}.model_limits: a self-hosted row states the model's own "
                       f"context_tokens and output_tokens, with their source (to tell "
                       f"`limit` from `config`), got {limits!r}")
    thinking = row.get("thinking")
    if not isinstance(thinking, list) or not set(thinking) <= set(ROLES):
        out.append(f"{where}.thinking: a list of roles, got {thinking!r}")
    effort = row.get("effort")
    single = SINGLE_LEVEL_MODELS.match(str(row.get("model"))) is not None
    if effort == SINGLE_LEVEL and not single:
        out.append(f"{where}.effort: {SINGLE_LEVEL!r} is for a model with one effort level "
                   f"(Haiku), not {row.get('model')!r}")
    if kind == "claude":
        if sorted(thinking or []) != list(ROLES):
            out.append(f"{where}.thinking: a command route thinks on every role "
                       f"(commands.environ); got {thinking!r}")
        if single and effort != SINGLE_LEVEL:
            out.append(f"{where}.effort: Haiku has one level (extended thinking on or "
                       f"off); register {SINGLE_LEVEL!r} and no --effort is passed "
                       f"got {effort!r}")
        elif not single and (not isinstance(effort, dict) or sorted(effort) != list(ROLES)
                             or any(level not in config.EFFORT_LEVELS
                                    for level in effort.values())):
            out.append(f"{where}.effort: a level for each of {', '.join(ROLES)} "
                       f"(never the build's default), got {effort!r}")
    else:
        if not (route.get("base_url") or route.get("base_url_env")):
            out.append(f"{where}.route: base_url or base_url_env")
        if effort not in ("vendor_default",) + ((SINGLE_LEVEL,) if single else ()):
            out.append(f"{where}.effort: an HTTP route cannot carry a level "
                       f"(it runs at the vendor's default); say \"vendor_default\"")
    if row.get("field_order", "schema") not in config.FIELD_ORDERS:
        out.append(f"{where}.field_order: {row.get('field_order')!r}")
    if not isinstance(row.get("window"), int) or row["window"] <= 0:
        out.append(f"{where}.window: a positive number of tokens")
    sku = pricing.sku_for(row["model"])
    if sku is None and not str(row.get("unpriced") or "").strip():
        out.append(f"{where}: {row['model']!r} has no SKU in pricing.py; add one or "
                   f"state the reason as `unpriced`")
    if metered(row):
        if sku is None:
            out.append(f"{where}: a metered row must be priced, or no cap can hold it")
        if row["vendor"] not in caps:
            out.append(f"{where}: metered on {row['vendor']!r} and caps names no "
                       f"such vendor (set metered: false only for a route nobody bills)")
        if "overall" not in caps:
            out.append("caps.overall: required when any row is metered")
        if not isinstance(row.get("cell_estimate_usd"), (int, float)):
            out.append(f"{where}.cell_estimate_usd: a conservative per-cell figure "
                       f"for the first cell, before anything is measured")
    if not is_reference and (lanes.get(row.get("lane")) or {}).get(
            "gpu_seconds") is not None and not isinstance(
            row.get("cell_estimate_seconds"), (int, float)):
        out.append(f"{where}.cell_estimate_seconds: its lane caps GPU seconds, so the "
                   f"first cell needs a conservative wall-seconds figure")
    return out


@dataclass
class Cell:
    row: str
    set: str
    item: str
    draw: int

    @property
    def id(self) -> str:
        return f"{self.row}|{self.set}|{self.item}|d{self.draw}"

    def dir(self, run_dir: Path, attempt: int) -> Path:
        return (run_dir / "cells" / self.row / self.set / self.item.replace("/", "_")
                / f"d{self.draw}" / f"a{attempt}")


def plan(reg: dict, lane: str | None = None) -> list[Cell]:
    """Every cell of the lane, in run order.

    Sets in registration order; within a set draw-major (every draw 1 before any
    draw 2), and pair-major within a draw: for each item, every row that runs
    it, the rows rotated by the item's position and the draw so that a bad
    afternoon or a cut does not always land on the same row.
    """
    rows = [r for r in reg["rows"] if lane is None or r["lane"] == lane]
    out: list[Cell] = []
    for set_id, spec in reg["sets"].items():
        members = [r for r in rows if set_id in r["sets"]]
        if not members:
            continue
        top = max(draws_of(reg, r, set_id, item) for r in members for item in spec["items"])
        for draw in range(1, top + 1):
            for index, item in enumerate(spec["items"]):
                shift = (index + draw - 1) % len(members)
                for row in members[shift:] + members[:shift]:
                    if item in items_of(reg, row, set_id) and \
                            draw <= draws_of(reg, row, set_id, item):
                        out.append(Cell(row["id"], set_id, item, draw))
    return out


# --- the clone ----------------------------------------------------------------------

def git(clone: Path, *args: str) -> str:
    done = subprocess.run(["git", "-C", str(clone), *args], capture_output=True, text=True,
                          timeout=60)
    if done.returncode != 0:
        raise Refusal(f"git {' '.join(args)} failed in {clone}: {done.stderr.strip()}")
    return done.stdout


def git_state(clone: Path) -> tuple[str, list[str]]:
    """(HEAD, every porcelain line): untracked and ignored files included.

    Ignored files count too: an untracked `src/llossless/_prompts/` shadows
    `prompts/`, a `models.local.json` at the clone's root changes the
    models, and a `.llossless-cache/` would be a cache. None may exist.
    """
    head = git(clone, "rev-parse", "HEAD").strip()
    lines = [line for line in git(clone, "status", "--porcelain", "--ignored",
                                  "--untracked-files=all").splitlines() if line.strip()]
    return head, lines


def check_clone(clone: Path, pin: str) -> list[str]:
    problems = []
    try:
        head, dirty = git_state(clone)
    except Refusal as exc:
        return [str(exc)]
    if head != pin:
        problems.append(f"the clone's HEAD is {head}, not the pin {pin}")
    if dirty:
        problems.append(f"the clone is not clean ({len(dirty)} line(s) of "
                        f"`git status --porcelain --ignored`): {dirty[:5]}")
    if (clone / "internal" / "assets").exists():
        problems.append("internal/assets reached the clone")
    return problems


def prompt_digests(clone: Path) -> dict[str, str]:
    return {str(p.resolve()): sha256_file(p)
            for p in sorted((clone / "prompts").rglob("*")) if p.is_file()}


def item_dir(clone: Path, reg: dict, set_id: str, item: str) -> Path:
    return clone / reg["sets"][set_id]["root"] / item


def input_files(clone: Path, reg: dict, set_id: str, item: str) -> list[Path]:
    """The files one item's cell reads: its sources, and for a fixture its merged.md."""
    where = item_dir(clone, reg, set_id, item)
    names = sorted(p.name for p in where.glob("source_*.md"))
    if reg["sets"][set_id]["kind"] == "detect":
        names.append("merged.md")
    return [where / name for name in names]


def scored_files(clone: Path, reg: dict, set_id: str, item: str) -> list[Path]:
    """Every input a cell's figure depends on (the registered sha256 list)."""
    where = item_dir(clone, reg, set_id, item)
    extra = [where / n for n in ("ideal.md", "ideal.json", "expected.json", "reference.md",
                                 "meta.json") if (where / n).is_file()]
    return input_files(clone, reg, set_id, item) + extra


def inputs_sha256(clone: Path, reg: dict) -> dict[str, str]:
    out = {}
    for set_id in reg["sets"]:
        for item in reg["sets"][set_id]["items"]:
            where = item_dir(clone, reg, set_id, item)
            if not where.is_dir():
                raise Refusal(f"sets.{set_id}: {item} is not in the clone at {where}")
            for path in scored_files(clone, reg, set_id, item):
                out[str(path.relative_to(clone))] = sha256_file(path)
    return out


# --- the `claude` wrapper ---------------------------------------------------------------

WRAPPER = r'''#!{python} -I
"""The lineup runner's `claude`: logs each call, then runs the registered copy.

Named `claude` so the build's isolation and effort tables apply as they do to
the real CLI. Per call it writes, into $LINEUP_CALLS: the argv, the names (never
the values) of the environment it was started with, the realpath, size, inode
and mtime of the program it runs, the exit code, and the program's stdout (the
result envelope) and stderr, then passes both on unchanged. The program is
started in its own process group and is sent SIGTERM if this wrapper dies, so a
call the tool timed out does not keep running.
"""
import ctypes, json, os, signal, subprocess, sys, time
REAL = {real!r}
where = os.environ.get("LINEUP_CALLS")
if not where:
    sys.stderr.write("lineup wrapper: LINEUP_CALLS is not set; refusing to run\n")
    sys.exit(97)
os.makedirs(where, exist_ok=True)
stamp = "%d-%d" % (time.time_ns(), os.getpid())
info = os.stat(REAL)
record = {{"argv": sys.argv[1:], "env_names": sorted(os.environ),
          "real": REAL, "realpath": os.path.realpath(REAL), "size": info.st_size,
          "inode": info.st_ino, "mtime_ns": info.st_mtime_ns, "started": time.time()}}

def die_with_parent():
    try:
        ctypes.CDLL("libc.so.6", use_errno=True).prctl(1, signal.SIGTERM)
    except OSError:
        pass

done = subprocess.run([REAL, *sys.argv[1:]], stdin=sys.stdin, capture_output=True,
                      preexec_fn=die_with_parent)
record.update(rc=done.returncode, ended=time.time())
with open(os.path.join(where, stamp + ".out"), "wb") as out:
    out.write(done.stdout)
with open(os.path.join(where, stamp + ".err"), "wb") as err:
    err.write(done.stderr)
with open(os.path.join(where, stamp + ".json"), "w") as log:
    json.dump(record, log)
sys.stdout.buffer.write(done.stdout)
sys.stderr.buffer.write(done.stderr)
sys.exit(done.returncode)
'''


def write_wrapper(run_dir: Path, real: Path) -> Path:
    directory = run_dir / "bin"
    directory.mkdir(parents=True, exist_ok=True)
    wrapper = directory / "claude"
    text = WRAPPER.format(python=sys.executable, real=str(real))
    if not wrapper.exists() or wrapper.read_text(encoding="utf-8") != text:
        wrapper.write_text(text, encoding="utf-8")
        wrapper.chmod(0o755)
    return wrapper


def read_calls(calls_dir: Path) -> list[dict]:
    """Every call the wrapper logged in one cell, in order, with its envelope parsed."""
    out = []
    if not calls_dir.is_dir():
        return out
    for record_path in sorted(calls_dir.glob("*.json"),
                              key=lambda p: tuple(int(x) for x in p.stem.split("-"))):
        record = json.loads(record_path.read_text(encoding="utf-8"))
        raw = (record_path.with_suffix(".out")).read_bytes().decode("utf-8", "replace")
        try:
            envelope = json.loads(raw)
        except ValueError:
            envelope = None
        record["envelope"] = envelope if isinstance(envelope, dict) else None
        record["stderr"] = (record_path.with_suffix(".err")).read_bytes().decode(
            "utf-8", "replace")[-600:]
        out.append(record)
    return out


def envelope_answered(record: dict) -> bool:
    """A call whose envelope is an answer: exit 0, not `is_error`, a non-empty result."""
    env = record.get("envelope") or {}
    return record.get("rc") == 0 and not env.get("is_error") and bool(
        str(env.get("result") or "").strip())


def api_equivalent(calls: list[dict]) -> dict:
    """The CLI's own `total_cost_usd`, over every call and over the answering calls."""
    every = sum(float((c.get("envelope") or {}).get("total_cost_usd") or 0) for c in calls)
    answering = sum(float((c.get("envelope") or {}).get("total_cost_usd") or 0)
                    for c in calls if envelope_answered(c))
    per_model: dict[str, dict] = {}
    for c in calls:
        if not envelope_answered(c):
            continue
        for model, usage in ((c.get("envelope") or {}).get("modelUsage") or {}).items():
            slot = per_model.setdefault(model, {})
            for key, value in (usage or {}).items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    slot[key] = slot.get(key, 0) + value
    return {"all_usd": every, "answering_usd": answering, "per_model": per_model,
            "calls": len(calls), "answered": sum(1 for c in calls if envelope_answered(c))}


# --- the run directory -----------------------------------------------------------------

@contextlib.contextmanager
def locked(path: Path, mode: int = fcntl.LOCK_EX):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+", encoding="utf-8") as handle:
        fcntl.flock(handle, mode)
        try:
            yield handle
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


class Journal:
    """`cells.jsonl`: append-only, one JSON object per line, shared by every lane.

    A crash, a full disk or a `kill -9` during an append can leave the last line
    cut short. That line, and only that line, is moved to a side file
    (`cells.jsonl.torn-N`), a `torn_tail_quarantined` event is appended, and a
    loud warning goes to stderr; the attempt it belonged to then has a begin
    and no end, and is closed `interrupted` and re-run like any other. Checked
    before every append too, so a record is never glued onto a torn one. A line
    that is not JSON anywhere else was edited, and is refused.
    """

    def __init__(self, path: Path, redact=None) -> None:
        self.path = path
        # Every record passes through this before it is written.
        self.redact = redact or (lambda record: record)

    @contextlib.contextmanager
    def _exclusive(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a+b") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                yield handle
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    def _heal(self, handle) -> None:
        """Under the exclusive lock: quarantine a torn last line, or end a whole one."""
        handle.seek(0)
        data = handle.read()
        if not data or data.endswith(b"\n") and self._parses(data[:-1].rsplit(b"\n", 1)[-1]):
            return
        terminated = data.endswith(b"\n")
        body = data[:-1] if terminated else data
        start = body.rfind(b"\n") + 1
        last = body[start:]
        if not terminated and self._parses(last):
            # The record is whole and only its newline was lost.
            handle.write(b"\n")
            handle.flush()
            os.fsync(handle.fileno())
            return
        number = 1
        while self.path.with_name(f"{self.path.name}.torn-{number}").exists():
            number += 1
        side = self.path.with_name(f"{self.path.name}.torn-{number}")
        side.write_bytes(data[start:])
        handle.truncate(start)
        event = {"type": "event", "event": "torn_tail_quarantined", "at": now(),
                 "bytes": len(data) - start, "side_file": side.name}
        handle.write((json.dumps(event, sort_keys=True) + "\n").encode("utf-8"))
        handle.flush()
        os.fsync(handle.fileno())
        print(f"WARNING: {self.path} ended in a torn line ({len(data) - start} bytes, a write "
              f"cut short); it was moved to {side.name} and the run continues. The attempt "
              f"it belonged to is closed `interrupted` and re-run.", file=sys.stderr)

    @staticmethod
    def _parses(line: bytes) -> bool:
        if not line.strip():
            return True
        try:
            json.loads(line)
        except ValueError:
            return False
        return True

    def append(self, record: dict) -> None:
        line = json.dumps(self.redact(record), sort_keys=True) + "\n"
        with self._exclusive() as handle:
            self._heal(handle)
            handle.write(line.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        with locked(self.path, fcntl.LOCK_SH) as handle:
            handle.seek(0)
            text = handle.read()
        lines = text.splitlines()
        if lines and not self._parses(lines[-1].encode("utf-8")) or \
                text and not text.endswith("\n"):
            with self._exclusive() as handle:
                self._heal(handle)
            with locked(self.path, fcntl.LOCK_SH) as handle:
                handle.seek(0)
                text = handle.read()
        out = []
        for number, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except ValueError:
                raise Refusal(f"{self.path}:{number} is not JSON and is not the last line; "
                              f"the journal is append-only and was edited") from None
        return out


def ends(records: list[dict]) -> dict[str, list[dict]]:
    """cell id -> its attempts' end records, in order."""
    out: dict[str, list[dict]] = {}
    for record in records:
        if record.get("type") == "end":
            out.setdefault(record["cell"], []).append(record)
    return out


def dangling(records: list[dict], lane: str) -> list[dict]:
    """Begin records of this lane with no end: attempts a dead process left."""
    closed = {(r["cell"], r["attempt"]) for r in records if r.get("type") == "end"}
    return [r for r in records if r.get("type") == "begin" and r.get("lane") == lane
            and (r["cell"], r["attempt"]) not in closed]


def latest_state(attempts: list[dict]) -> str | None:
    return attempts[-1]["state"] if attempts else None


def spent(records: list[dict]) -> dict[str, float]:
    """Dollars charged per vendor, and `overall` over the metered vendors."""
    out: dict[str, float] = {}
    for record in records:
        if record.get("type") != "end":
            continue
        vendor = record.get("vendor")
        out[vendor] = out.get(vendor, 0.0) + float(record.get("charged_usd") or 0.0)
        if record.get("metered"):
            out["overall"] = out.get("overall", 0.0) + float(record.get("charged_usd") or 0.0)
    return out


def gpu_used(records: list[dict], lane: str) -> float:
    """Wall seconds a lane has held its GPU: every attempt's cell, and every pre-warm."""
    total = 0.0
    for record in records:
        if record.get("lane") != lane:
            continue
        if record.get("type") == "end" and record.get("kind") != "reference":
            # A reference check runs on another vendor's route, not this GPU.
            total += float(record.get("wall_seconds") or 0.0)
        elif record.get("type") == "event" and record.get("event") == "prewarm":
            total += float(record.get("total_seconds") or record.get("gpu_seconds") or 0.0)
    return total


# --- the pod's address ---------------------------------------------------------------

REDACT_MARK = "<redacted>"


@dataclass
class Redactor:
    """Every form of a secret address, and what replaces it, longest first.

    `scripts/stream_redact.literal_forms`' rule: the real values are read out of
    the environment (or the env file) and replaced literally, so no pattern has
    to anticipate a host. The whole URL becomes `$NAME`, which tells a reader
    where it came from; its scheme-less form, `scheme://netloc`, the netloc,
    the host, and any path segment of eight characters or more (a serverless
    endpoint's id lives in the path) become `<redacted>`. Anything shorter than
    four characters is left alone, so a short value cannot turn prose to marks.
    """

    forms: list[tuple[str, str]] = field(default_factory=list)

    @classmethod
    def of(cls, named: dict[str, str]) -> "Redactor":
        pairs: dict[str, str] = {}
        for name, value in named.items():
            value = (value or "").strip()
            if not value:
                continue
            whole = value.rstrip("/")
            pairs.setdefault(value, f"${name}")
            pairs.setdefault(whole, f"${name}")
            parts = urlsplit(whole) if "://" in whole else None
            if parts is None:
                continue
            forms = [whole.split("://", 1)[1], f"{parts.scheme}://{parts.netloc}",
                     parts.netloc, parts.hostname or ""]
            forms += [piece for piece in parts.path.split("/") if len(piece) >= 8]
            for form in forms:
                if len(form) > 3:
                    pairs.setdefault(form, REDACT_MARK)
        return cls(sorted(pairs.items(), key=lambda item: len(item[0]), reverse=True))

    def text(self, value: str) -> str:
        for form, mark in self.forms:
            value = value.replace(form, mark)
        return value

    def obj(self, value):
        if isinstance(value, str):
            return self.text(value)
        if isinstance(value, list):
            return [self.obj(item) for item in value]
        if isinstance(value, dict):
            return {key: self.obj(item) for key, item in value.items()}
        return value

    def tree(self, where: Path, keep: set[str]) -> None:
        """Every text file under `where` rewritten, except the names in `keep`."""
        if not self.forms:
            return
        for path in sorted(where.rglob("*")):
            if not path.is_file() or path.name in keep:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            redacted = self.text(text)
            if redacted != text:
                path.write_text(redacted, encoding="utf-8")


# --- the context ---------------------------------------------------------------------------

@dataclass
class Context:
    """One registration, resolved: where things are and what was recorded at the first start."""

    registration: Path
    reg: dict
    block_sha256: str
    run_dir: Path
    clone: Path
    journal: Journal
    rows: dict[str, dict]
    run_info: dict = field(default_factory=dict)
    sleep: callable = time.sleep
    out: callable = print
    clock: callable = lambda: datetime.now(timezone.utc)  # noqa: E731
    redactor: Redactor = field(default_factory=Redactor)
    # The registered reference routes, and how the lane asks whether the
    # network is back (`probe(ctx, urls) -> bool`; tests stub it).
    references: dict[str, dict] = field(default_factory=dict)
    probe: callable = None

    def row(self, rid: str) -> dict:
        return self.rows[rid]

    def say(self, text: str) -> None:
        """A line to the lane's log, which is evidence too: the address comes out first."""
        self.out(self.redactor.text(text))

    @property
    def settings(self) -> dict:
        return self.reg["settings"]

    @property
    def rules(self) -> dict:
        return {**RULE_DEFAULTS, **(self.reg.get("rules") or {})}


def load_context(registration: Path, *, require_self: bool = True) -> Context:
    """Parse and validate the registration and resolve its paths. Makes no call."""
    registration = registration.resolve()
    reg, block_sha = parse_registration(registration)
    problems = validate(reg)
    if problems:
        raise Refusal("the registration cannot run:\n  - " + "\n  - ".join(problems))
    run_dir = (registration.parent / reg.get("run_dir", ".")).resolve()
    clone = (run_dir / reg.get("clone", "tree")).resolve()
    if require_self and ROOT.resolve() != clone:
        raise Refusal(f"this runner is {Path(__file__).resolve()}; it must be the pinned "
                      f"clone's own copy, {clone / 'tests' / 'run_lineup.py'} (never "
                      f"the working repository)")
    ctx = Context(registration=registration, reg=reg, block_sha256=block_sha,
                  run_dir=run_dir, clone=clone, journal=Journal(run_dir / "cells.jsonl"),
                  rows={row["id"]: row for row in reg["rows"]},
                  references={ref["id"]: ref for ref in reg.get("references") or []},
                  probe=default_probe)
    ctx.redactor = Redactor.of({name: secret(ctx, name) or "" for name in secret_names(reg)})
    ctx.journal.redact = ctx.redactor.obj
    return ctx


def secret_names(reg: dict) -> list[str]:
    """The variables whose values are addresses never written down (the pod's)."""
    names = {row["route"]["base_url_env"]
             for row in list(reg.get("rows") or []) + list(reg.get("references") or [])
             if row.get("route", {}).get("base_url_env")}
    names |= {url[1:] for url in (reg.get("infrastructure") or {}).get("probe_urls") or []
              if isinstance(url, str) and url.startswith("$")}
    names |= {(spec.get("prewarm") or {}).get("health_url_env")
              for spec in (reg.get("lanes") or {}).values() if isinstance(spec, dict)}
    return sorted(name for name in names if name)


def read_env_file(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.strip().partition("=")
        if sep and not key.startswith("#"):
            out[key.strip().removeprefix("export ").strip()] = value.strip().strip("'\"")
    return out


def secret(ctx: Context, name: str) -> str | None:
    """A variable's value from this process's environment, else the registered env file."""
    if os.environ.get(name):
        return os.environ[name]
    env_file = ctx.reg.get("env_file")
    if env_file and Path(env_file).is_file():
        return read_env_file(Path(env_file)).get(name) or None
    return None


def base_url(ctx: Context, row: dict) -> str:
    route = row["route"]
    if route.get("base_url"):
        return route["base_url"].rstrip("/")
    value = secret(ctx, route["base_url_env"])
    if not value:
        raise Refusal(f"rows.{row['id']}: {route['base_url_env']} is not set (the hosted "
                      f"endpoint's address changes on restart and is never in a file)")
    return value.rstrip("/")


def preflight(ctx: Context, lane: str | None) -> list[str]:
    """Every refusal before the first cell. Makes no model call."""
    problems = check_clone(ctx.clone, ctx.reg["pin"])
    # The code the child will import is the clone's: asked of a child with the
    # same PYTHONPATH the cells get, not assumed from this process.
    probe = subprocess.run(
        [sys.executable, "-c", "import llossless; print(llossless.__file__)"],
        capture_output=True, text=True, env=base_env(ctx), timeout=60, cwd=str(ctx.run_dir))
    where = probe.stdout.strip()
    if not where.startswith(str(ctx.clone / "src") + os.sep):
        problems.append(f"llossless resolves to {where or probe.stderr.strip()[-200:]}, not "
                        f"the clone's src/")
    rows = [r for r in ctx.reg["rows"] if lane is None or r["lane"] == lane]
    if lane is not None and not rows:
        problems.append(f"no row runs on lane {lane!r}")
    # A lane's reference routes are asked the moment a cell fails every pass,
    # so their key and address are checked before the first cell, like the rows'.
    used = sorted({r["reference"] for r in rows if r.get("reference") in ctx.references})
    for row in rows + [ctx.references[name] for name in used]:
        route = row["route"]
        if route["kind"] == "http":
            if route.get("key_env") and not secret(ctx, route["key_env"]):
                problems.append(f"rows.{row['id']}: {route['key_env']} is not set, in the "
                                f"environment or the env file")
            try:
                base_url(ctx, row)
            except Refusal as exc:
                problems.append(str(exc))
    if any(r["route"]["kind"] == "claude" for r in rows):
        problems += check_claude(ctx)
    return problems


def check_claude(ctx: Context) -> list[str]:
    """The registered copy of `claude` is there, hashes as registered, and says its version."""
    claude = ctx.reg["claude"]
    real = Path(claude["path"])
    if not real.is_absolute():
        real = (ctx.run_dir / real).resolve()
    if not real.is_file():
        return [f"claude.path: {real} is not a file"]
    problems = []
    digest = sha256_file(real)
    if digest != claude["sha256"]:
        problems.append(f"claude.sha256: {real} hashes to {digest}, not the registered "
                        f"{claude['sha256']}")
    env = scrubbed_env(os.environ)
    env["DISABLE_AUTOUPDATER"] = "1"
    try:
        said = subprocess.run([str(real), "--version"], capture_output=True, text=True,
                              env=env, timeout=60).stdout.strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        said = f"(could not run: {exc})"
    if claude["version"] not in said:
        problems.append(f"claude.version: {real} --version says {said!r}, not "
                        f"{claude['version']!r}")
    ctx.run_info["claude_version_output"] = said
    return problems


def claude_binary(ctx: Context) -> Path:
    real = Path(ctx.reg["claude"]["path"])
    return real if real.is_absolute() else (ctx.run_dir / real).resolve()


def first_start(ctx: Context) -> dict:
    """run.json: what the first start recorded, checked on every later start."""
    path = ctx.run_dir / "run.json"
    now_info = {"pin": ctx.reg["pin"], "block_sha256": ctx.block_sha256,
                "inputs_sha256": inputs_sha256(ctx.clone, ctx.reg),
                "prompts_sha256": prompt_digests(ctx.clone)}
    with locked(ctx.run_dir / ".run.json.lock"):
        if not path.exists():
            info = {**now_info, "created": now(), "amendments": []}
            path.write_text(json.dumps(info, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            return info
        info = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    if info["pin"] != now_info["pin"]:
        problems.append(f"run.json was started at pin {info['pin']}, the registration now "
                        f"says {now_info['pin']}")
    accepted = [info["block_sha256"]] + [a["new"] for a in info.get("amendments", [])]
    if now_info["block_sha256"] not in accepted:
        problems.append(f"the registration block changed since the run started "
                        f"({info['block_sha256'][:12]} -> {now_info['block_sha256'][:12]}); "
                        f"restore it, or record a dated amendment with `amend`")
    if info["inputs_sha256"] != now_info["inputs_sha256"]:
        problems.append("an input file's sha256 differs from the first start's")
    if info["prompts_sha256"] != now_info["prompts_sha256"]:
        problems.append("a prompt file's sha256 differs from the first start's")
    if problems:
        raise Refusal("resume refused:\n  - " + "\n  - ".join(problems))
    return info


# --- one cell --------------------------------------------------------------------------------

def scrubbed_env(source) -> dict[str, str]:
    return {k: v for k, v in source.items()
            if not FORBIDDEN_ENV.match(k) and not DROPPED_ALSO.match(k)}


def base_env(ctx: Context) -> dict[str, str]:
    env = scrubbed_env(os.environ)
    env.update({"PYTHONPATH": str(ctx.clone / "src"), "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONIOENCODING": "utf-8"})
    return env


def cell_env(ctx: Context, row: dict, cell_dir: Path) -> dict[str, str]:
    """The child's whole environment. Checked here, before it is used."""
    env = base_env(ctx)
    (cell_dir / "tmp").mkdir(parents=True, exist_ok=True)
    env["TMPDIR"] = str(cell_dir / "tmp")
    env["LLOSSLESS_CACHE_DIR"] = str(cell_dir / "cache")
    route = row["route"]
    if route["kind"] == "http":
        if route.get("key_env"):
            env[KEY_VAR] = secret(ctx, route["key_env"]) or ""
            env["LLOSSLESS_API_KEY_ENV"] = KEY_VAR
    else:
        env[CALLS_VAR] = str(cell_dir / "calls")
        env["DISABLE_AUTOUPDATER"] = "1"
        env["LLOSSLESS_COMMAND_ENVELOPE"] = "result"
        env["LLOSSLESS_COMMAND_LABEL"] = f"lineup {row['id']}"
    stray = sorted(k for k in env if FORBIDDEN_AT_CHILD.match(k) and k not in RUNNER_SET)
    if stray:
        raise Refusal(f"the child environment would carry {stray}", EXIT_REFUSED)
    return env


def command_line(ctx: Context, row: dict) -> str:
    """The `claude` route's command: the wrapper, the result envelope, the full model id."""
    wrapper = ctx.run_dir / "bin" / "claude"
    return shlex.join([str(wrapper), "--print", *config.RESULT_ARGS, "--model", row["model"]])


def row_timeout(ctx: Context, row: dict) -> float:
    """The per-call `--timeout` for this row: its own when registered, else the run's.

    A timeout bounds a call and changes no answer, so a slower route
    (the self-hosted 27B decodes at about 6 tokens a second on its 48 GB card)
    registers a longer one rather than losing merges to the harness.
    """
    return float(row.get("timeout", ctx.settings["timeout"]))


def cell_wall(ctx: Context, row: dict) -> float:
    """The runner's own kill for a whole cell: the row's, else the run's."""
    return float(row.get("cell_wall_seconds", ctx.settings.get("cell_wall_seconds", 14400)))


def cell_argv(ctx: Context, row: dict, cell: Cell, names: list[str],
              thinking: list[str] | None = None) -> list[str]:
    """`python -m llossless ...` with every setting the registration holds stated as a flag."""
    s = ctx.settings
    spec = ctx.reg["sets"][cell.set]
    route = row["route"]
    thinking = row["thinking"] if thinking is None else thinking
    argv = [sys.executable, "-m", "llossless"]
    if spec["kind"] == "merge":
        argv += ["merge", *names, "--base", s["base"], "--fidelity", spec["fidelity"],
                 "--title-policy", s["title_policy"], "-o", "merged.md"]
    else:
        argv += ["verify", *names]
    argv += ["--verify-depth", s["verify_depth"], "--structured", s["structured"],
             "--field-order", row.get("field_order", "schema"),
             "--timeout", f"{row_timeout(ctx, row):g}", "--window", str(row["window"]),
             "--model", row["model"], "--merge-model", row["model"],
             "--max-calls", str(s.get("max_calls", 400)),
             # The tool's own response cache, in this attempt's directory
             # (`LLOSSLESS_CACHE_DIR`, `cell_env`). It starts empty, so every
             # call goes live and its answer is kept; a retry of the same cell
             # and draw starts with the earlier attempts' answers copied in
             # (`seed_reuse`), and only the missing calls go live.
             "--cache", "--json", "report.json", "-v"]
    for role in sorted(thinking):
        argv += ["--thinking", role]
    if route["kind"] == "http":
        argv += ["--base-url", base_url(ctx, row), "--profile", route["profile"]]
    else:
        argv += ["--answer-with", command_line(ctx, row),
                 "--profile", route.get("profile", "subscription")]
        # By ruling, a one-level model (Haiku) is passed no --effort.
        if row.get("effort") != SINGLE_LEVEL:
            for role in ROLES:
                argv += ["--effort", f"{role}={row['effort'][role]}"]
    if row.get("min_interval"):
        argv += ["--min-interval", f"{row['min_interval']:g}"]
    return argv


def charge(ctx: Context, row: dict, report: dict | None, calls: list[dict],
           projection: float, *, stderr: str = "", killed: bool = False,
           reused_usd: float = 0.0) -> dict:
    """What this attempt is charged against the caps, and on what basis.

    Exact where the report says: `answering_cost` plus `excluded.cost` plus
    `unruled.cost`, all billed. One conservative call estimate for each call
    that may have been billed and reported no usage: a ledger row without
    tokens, or a discarded call lost to anything but an HTTP status (a timeout
    or a cut stream can be billed; a 429 or a 5xx is not). Nothing for a
    transport retry, which files no row and is not billed. Without a report:
    nothing when the one call that ran (the merge is the first) died on an
    HTTP status; the whole projection when the process was killed or crashed
    (calls unknown); one call estimate otherwise.

    A call this attempt took from the same cell's earlier attempt
    (`reused_usd`, a cache row the report prices by its tokens) was charged
    when it was made, and is not charged again. A `claude` route's reused call
    never reaches the wrapper, so its envelope is not in `calls` at all.
    """
    if route_kind(row) == "claude":
        equiv = api_equivalent(calls)
        return {"charged_usd": equiv["all_usd"], "charge_basis": "cli_envelopes",
                "api_equivalent_usd": equiv["all_usd"],
                "api_equivalent_answering_usd": equiv["answering_usd"]}
    if not metered(row):
        return {"charged_usd": 0.0, "charge_basis": "not_metered"}
    sku = pricing.sku_for(row["model"])
    per_call = float(row.get("call_estimate_usd") or pricing.cost(
        sku, input_tokens=20_000, output_tokens=40_000))
    if report is None:
        if killed or "Traceback" in stderr:
            return {"charged_usd": projection, "charge_basis": "estimate_no_report"}
        if re.search(r"HTTP \d{3}\b", stderr):
            return {"charged_usd": 0.0, "charge_basis": "status_not_billed"}
        return {"charged_usd": per_call, "charge_basis": "estimate_one_call"}
    prov = report.get("provenance") or {}
    total, unpriced = 0.0, 0
    for block in (prov.get("answering_cost"), (prov.get("excluded") or {}).get("cost"),
                  (prov.get("unruled") or {}).get("cost")):
        if block:
            total += float(block.get("usd_exact") or 0.0)
            unpriced += int(block.get("unpriced_calls") or 0)

    def unreported(r: dict) -> bool:
        return r.get("prompt_tokens") is None or r.get("completion_tokens") is None

    unmeasured = sum(1 for r in prov.get("ledger") or [] if unreported(r))
    unmeasured += sum(1 for r in prov.get("discarded_calls") or []
                      if unreported(r) and r.get("error") != "HTTPStatusError")
    return {"charged_usd": max(0.0, total - reused_usd) + unmeasured * per_call,
            "charge_basis": "report" if not unmeasured else "report+estimate",
            "report_usd": total, "unmeasured_calls": unmeasured,
            "unpriced_calls": unpriced,
            **({"reused_usd_not_charged": reused_usd} if reused_usd else {})}


def projection(ctx: Context, row: dict, cell: Cell, records: list[dict]) -> float:
    """The most this cell could plausibly cost, before the margin.

    The most this row's attempts on the same item have been charged; else the
    row's highest charge per input byte in the same set times this item's
    bytes; else the registered estimate. Never below the registered estimate.
    """
    estimate = row.get("cell_estimate_usd")
    if isinstance(estimate, dict):
        estimate = estimate.get(cell.set, max(estimate.values()))
    floor = float(estimate or 0.0)
    mine = [r for r in records if r.get("type") == "end" and r.get("row") == row["id"]
            and r.get("set") == cell.set and r.get("charge_basis") in (
                "report", "report+estimate", "cli_envelopes")]
    same = [float(r["charged_usd"]) for r in mine if r.get("item") == cell.item]
    if same:
        return max(max(same), floor)
    size = sum(p.stat().st_size for p in input_files(ctx.clone, ctx.reg, cell.set, cell.item))
    rates = [float(r["charged_usd"]) / r["input_bytes"] for r in mine if r.get("input_bytes")]
    return max(max(rates) * size if rates else 0.0, floor)


def projected_seconds(ctx: Context, row: dict, cell: Cell, records: list[dict]) -> float:
    """The most wall seconds this cell could plausibly hold its GPU, before the margin.

    `projection`'s rule in seconds: the longest attempt of this row on the same
    item; else the row's highest seconds per input byte in the same set times
    this item's bytes; never below the registered `cell_estimate_seconds`.
    """
    floor = float(row.get("cell_estimate_seconds") or 0.0)
    mine = [r for r in records if r.get("type") == "end" and r.get("row") == row["id"]
            and r.get("set") == cell.set and isinstance(r.get("wall_seconds"), (int, float))]
    same = [float(r["wall_seconds"]) for r in mine if r.get("item") == cell.item]
    if same:
        return max(max(same), floor)
    size = sum(p.stat().st_size for p in input_files(ctx.clone, ctx.reg, cell.set, cell.item))
    rates = [float(r["wall_seconds"]) / r["input_bytes"] for r in mine if r.get("input_bytes")]
    return max(max(rates) * size if rates else 0.0, floor)


def gpu_gate(ctx: Context, row: dict, cell: Cell, records: list[dict]) -> dict | None:
    """A self-hosted lane's GPU seconds, capped and gated like its dollars."""
    # A reference route has no lane of its own and holds no GPU.
    cap = (ctx.reg["lanes"].get(row.get("lane")) or {}).get("gpu_seconds")
    if cap is None:
        return None
    margin = float(ctx.reg.get("margin", 1.25))
    need = projected_seconds(ctx, row, cell, records) * margin
    used = gpu_used(records, row["lane"])
    if need > cap - used:
        return {"pot": f"{row['lane']} GPU seconds", "unit": "s", "cap": cap,
                "spent": round(used, 1), "need": round(need, 1), "left": round(cap - used, 1)}
    return None


def gate(ctx: Context, row: dict, cell: Cell, records: list[dict]) -> dict | None:
    """None if the cell may start; else why not (the lane stops)."""
    gpu = gpu_gate(ctx, row, cell, records)
    if gpu:
        return gpu
    if not metered(row) and not (route_kind(row) == "claude"
                                 and row["vendor"] in (ctx.reg.get("caps") or {})):
        return None
    caps = ctx.reg.get("caps") or {}
    margin = float(ctx.reg.get("margin", 1.25))
    need = projection(ctx, row, cell, records) * margin
    so_far = spent(records)
    for pot in ([row["vendor"], "overall"] if metered(row) else [row["vendor"]]):
        if pot not in caps:
            continue
        left = caps[pot] - so_far.get(pot, 0.0)
        if need > left:
            return {"pot": pot, "unit": "$", "cap": caps[pot],
                    "spent": round(so_far.get(pot, 0.0), 6), "need": round(need, 6),
                    "left": round(left, 6)}
    return None


def copy_inputs(ctx: Context, cell: Cell, cell_dir: Path) -> tuple[list[str], int]:
    """The item's input files into the cell, each checked against run.json's sha256."""
    recorded = ctx.run_info["inputs_sha256"]
    names, size = [], 0
    for source in input_files(ctx.clone, ctx.reg, cell.set, cell.item):
        target = cell_dir / source.name
        shutil.copyfile(source, target)
        key = str(source.relative_to(ctx.clone))
        if sha256_file(target) != recorded.get(key):
            raise Refusal(f"{key}: the copy in {cell_dir} does not hash as recorded",
                          EXIT_REFUSED)
        names.append(source.name)
        size += target.stat().st_size
    return names, size


def served_ok(row: dict, name: str | None) -> bool:
    if name is None:
        return False
    allowed = [row["model"], *(row.get("served_aliases") or [])]
    return any(re.fullmatch(re.escape(a) + DATE_SUFFIX, name) for a in allowed)


def check_report(ctx: Context, row: dict, cell: Cell, report: dict,
                 thinking: list[str] | None = None) -> list[str]:
    """Every way this report says it did not run what the registration registered."""
    p = []
    prov = report.get("provenance") or {}
    s = ctx.settings
    spec = ctx.reg["sets"][cell.set]
    pin = ctx.reg["pin"]
    stamp = str(prov.get("claimcheck_commit") or "")
    if "-" in stamp or not stamp or not pin.startswith(stamp):
        p.append(f"commit stamp {stamp!r} is not the pin {pin[:12]}")
    for key in ("claimcheck_commit_changed", "claimcheck_commit_end"):
        if prov.get(key):
            p.append(f"the tree moved during the run: {key}={prov.get(key)!r}")
    counts = prov.get("counts") or {}
    # A cache hit is checked by `account_reuse`: only this cell's own
    # earlier live answers may serve one. A replay never may.
    if prov.get("run_mode") != "live" or counts.get("replayed"):
        p.append(f"not a live run: run_mode {prov.get('run_mode')!r}, {counts}")
    so = prov.get("structured_output") or {}
    if (so.get("mode"), so.get("how")) != (s["structured"], "pinned"):
        p.append(f"tier {so}, registered {s['structured']} pinned")
    if so.get("field_order", "schema") != row.get("field_order", "schema"):
        p.append(f"field order {so.get('field_order')!r}")
    decoding = prov.get("decoding") or {}
    want_thinking = sorted(row["thinking"] if thinking is None else thinking)
    if sorted(decoding.get("thinking") or []) != want_thinking:
        p.append(f"decoding.thinking {decoding.get('thinking')!r}, registered {want_thinking}")
    profile = row["route"].get("profile", "subscription")
    # The report names a profile only when it is not the default one
    # (`provenance`, "only when it was not the default").
    said = decoding.get("profile", config.DEFAULT_PROFILE)
    if said != profile:
        p.append(f"decoding.profile {said!r}, registered {profile!r}")
    effort = decoding.get("effort")
    if route_kind(row) == "claude":
        if row["effort"] == SINGLE_LEVEL:
            # By ruling, the runner set none. The report then carries what
            # the tool's own table picks for this command with nothing set
            # (`config.effort_of`, `AUTO_EFFORT`), or nothing; anything else was
            # set by someone.
            command = command_line(ctx, row)
            auto = {role: level for role in ROLES
                    if (level := config.effort_of(command, role))}
            if effort not in (None, {}, auto):
                p.append(f"decoding.effort {effort!r}: a one-level row passes no --effort "
                         f"and records the tool's own {auto!r} or nothing")
        elif effort != row["effort"]:
            p.append(f"decoding.effort {effort!r}, registered {row['effort']!r} (effort mismatch)")
    elif effort or decoding.get("effort_ignored"):
        p.append(f"an HTTP row recorded an effort {effort!r} / "
                 f"{decoding.get('effort_ignored')!r}; none was registered")
    models = prov.get("models") or {}
    if set(models.values()) != {row["model"]}:
        p.append(f"provenance.models {models}, registered {row['model']!r} (model mismatch)")
    ledger = prov.get("ledger") or []
    live = [r for r in ledger if r.get("source") in ("live", "cache")]
    if len(live) != len(ledger):
        p.append(f"{len(ledger) - len(live)} ledger row(s) neither live nor this cell's "
                 f"own reused answer")
    for r in ledger + list(prov.get("discarded_calls") or []):
        if r.get("model") != row["model"]:
            p.append(f"a {r.get('role')} call asked for {r.get('model')!r}, not "
                     f"{row['model']!r} (model mismatch)")
        said = ((r.get("answered_by") or {}).get("output") if route_kind(row) == "claude"
                else r.get("served_model"))
        if said is not None and not served_ok(row, said):
            p.append(f"a {r.get('role')} call answered as {said!r}, not {row['model']!r} (model mismatch)")
    answered = [r for r in ledger if (r.get("answered_by") or {}).get("output")
                or r.get("served_model")]
    if ledger and not answered and not row.get("served_model_absent_ok"):
        p.append("no ledger row names the model that answered (model mismatch)")
    wanted = {"decompose", "verify"} | ({"merge"} if spec["kind"] == "merge" else set())
    # A role whose calls were all reused made no live call in this attempt.
    called = set(prov.get("calls_by_role") or {}) | {
        r.get("role") for r in ledger if r.get("source") == "cache"}
    if report.get("exit_code") in (0, 1, 3) and not wanted <= called:
        p.append(f"a role never called: {prov.get('calls_by_role')}")
    if spec["kind"] == "merge":
        policy = prov.get("merge_policy") or {}
        expect = {"fidelity": spec["fidelity"], "verify_depth": s["verify_depth"],
                  "title_policy": s["title_policy"]}
        if report.get("exit_code") in (0, 1, 3) or policy.get("base") is not None:
            expect["base"] = s["base"]
        for key, value in expect.items():
            if policy.get(key) != value:
                p.append(f"merge_policy.{key} {policy.get(key)!r}, registered {value!r}")
    for role, said in (prov.get("window") or {}).items():
        if not str(said).startswith(f"stated: {row['window']} tokens"):
            p.append(f"window.{role} {str(said)[:60]!r}, registered {row['window']}")
    p += check_prompts(ctx, spec, prov.get("prompts") or {})
    if route_kind(row) == "claude":
        granted = sorted(config.AUTO_GRANT["claude"]) \
            if spec.get("fidelity") == config.SOURCED else []
        for role, block in (prov.get("isolation") or {}).items():
            tools = sorted(block.get("tools") or []) if isinstance(
                block.get("tools"), list) else block.get("tools")
            want = granted if role == "merge" else []
            if block.get("safe_mode") is not True or tools not in (want, granted):
                p.append(f"isolation.{role} {block} (expected safe mode, tools {want})")
            if block.get("timeout") != row_timeout(ctx, row):
                p.append(f"isolation.{role}.timeout {block.get('timeout')!r}")
        missing = set(prov.get("calls_by_role") or {}) - set(prov.get("isolation") or {})
        if missing:
            p.append(f"no isolation block for {sorted(missing)}")
    return p


def check_prompts(ctx: Context, spec: dict, reported: dict[str, str]) -> list[str]:
    """Every prompt a report names is the clone's, as it was at the first start.

    A report's digest is the file's own sha256, or, for a prompt a fidelity
    fragment is substituted into, the digest of the file with its fragments
    (`prompts.compose`). The files are held by run.json's `prompts_sha256`;
    a composed digest is held by the first cell of the same set kind and
    fidelity that reported it (`prompts-observed.json`), and every later cell
    must report the same.
    """
    out = []
    files = ctx.run_info["prompts_sha256"]
    ledger_path = ctx.run_dir / "prompts-observed.json"
    group = f"{spec['kind']}:{spec.get('fidelity', '-')}"
    with locked(ctx.run_dir / ".prompts-observed.lock"):
        seen = json.loads(ledger_path.read_text(encoding="utf-8")) \
            if ledger_path.is_file() else {}
        changed = False
        for path, digest in sorted(reported.items()):
            if not path.startswith(str(ctx.clone / "prompts") + os.sep):
                out.append(f"a prompt came from outside the clone: {path}")
                continue
            if path not in files:
                out.append(f"{path} was not in the clone's prompts at the first start")
                continue
            if digest == files[path]:
                continue
            first = seen.setdefault(group, {}).setdefault(path, digest)
            changed = changed or first == digest
            if first != digest:
                out.append(f"{path} composed to {digest[:12]}, and to {first[:12]} in the "
                           f"first {group} cell")
        if changed:
            ledger_path.write_text(json.dumps(seen, indent=1, sort_keys=True) + "\n",
                                   encoding="utf-8")
    return out


def check_calls(ctx: Context, row: dict, calls: list[dict]) -> list[str]:
    """The wrapper's per-call log: environment names, the binary, the argv."""
    p = []
    real = claude_binary(ctx)
    info = real.stat()
    for c in calls:
        leaked = [n for n in c.get("env_names") or [] if FORBIDDEN_AT_CHILD.match(n)]
        if leaked:
            p.append(f"forbidden environment reached `claude`: {leaked}")
        if "DISABLE_AUTOUPDATER" not in (c.get("env_names") or []):
            p.append("DISABLE_AUTOUPDATER did not reach `claude`")
        if (c.get("realpath"), c.get("size"), c.get("inode"), c.get("mtime_ns")) != (
                os.path.realpath(real), info.st_size, info.st_ino, info.st_mtime_ns):
            p.append(f"the `claude` binary changed between calls: {c.get('realpath')}")
        argv = c.get("argv") or []
        model = argv[argv.index("--model") + 1] if "--model" in argv else None
        if model != row["model"]:
            p.append(f"argv --model {model!r}, registered {row['model']!r} (model mismatch)")
        env = c.get("envelope") or {}
        for used in (env.get("modelUsage") or {}):
            if not served_ok(row, used) and "haiku" not in used:
                p.append(f"the envelope names {used!r} (model mismatch)")
    return p


def discard_kinds(report: dict | None, cell_dir: Path | None = None) -> dict[str, int]:
    """How many calls the tool discarded, by kind (`blank_refusal`, `blank_length`, ...).

    The report's `provenance.discarded_calls` when there is a report. Without one
    (a fault on the run's first call writes none), the discard dumps the tool
    keeps under the cell's own `tmp/` (`client._dump_discard`, cache off), each
    of which names its kind.
    """
    kinds: dict[str, int] = {}
    if report is not None:
        rows = ((report.get("provenance") or {}).get("discarded_calls") or [])
        for row in rows:
            kinds[str(row.get("kind"))] = kinds.get(str(row.get("kind")), 0) + 1
        return kinds
    if cell_dir is None:
        return kinds
    # With the cache on the tool keeps its dumps in the attempt's own cache
    # directory; with it off, under the attempt's TMPDIR. Either is this attempt's.
    for dump in sorted(cell_dir.glob("**/discards/*.json")):
        try:
            kind = _dump_kind(json.loads(dump.read_text(encoding="utf-8")))
        except (ValueError, OSError, AttributeError):
            continue
        kinds[kind] = kinds.get(kind, 0) + 1
    return kinds


_FINISH = re.compile(r"finish_reason\W{1,4}(content_filter|length)")


def _dump_kind(dump: dict) -> str:
    """A discard dump's kind. The dump names the exception class (`EmptyResponse`),
    and keeps the envelope and the reason, where `finish_reason` says which blank it was
    (`client.blank_kind`'s reading)."""
    kind = str(dump.get("kind"))
    if kind in ("blank", "platform", "cancelled", "blank_length", "blank_refusal"):
        return kind
    found = _FINISH.search(f"{dump.get('detail') or ''} {dump.get('envelope') or ''}")
    if found:
        return "blank_refusal" if found.group(1) == "content_filter" else "blank_length"
    return "blank" if kind in ("EmptyResponse", "EmptyBody") else "platform"


def cli_refusal(envelope: dict | None) -> bool:
    """A `claude` envelope that is a refusal: `stop_reason: refusal`, or refusal prose
    where an answer (a JSON object) belongs."""
    envelope = envelope or {}
    if envelope.get("stop_reason") == "refusal":
        return True
    text = str(envelope.get("result") or "").strip()
    return bool(text) and not re.match(r"(?:```(?:json)?\s*)?\{", text) and \
        REFUSAL_TEXT.search(text) is not None


def _cli_error_texts(calls: list[dict]) -> list[str]:
    """What each failed `claude` call said: its envelope's result, status and stderr."""
    out = []
    for c in calls:
        env = c.get("envelope") or {}
        if env.get("is_error") or c.get("rc"):
            status = env.get("api_error_status")
            out.append(f"{env.get('result') or ''} "
                       + (f"(api_error_status={status}) " if status is not None else "")
                       + (c.get("stderr") or ""))
    return out


def step_class(detail: str, evidence: dict) -> str:
    """One errored step's detail (or a run's stderr), to a state. See `classify`."""
    if MODEL_OUTPUT.search(detail) and evidence["failed_rows"]:
        return "refused" if evidence["cli_refusals"] else "model_failure"
    if NETWORK_DETAIL.search(detail):
        return "platform"
    if evidence.get("self_hosted") and HARNESS_TIMEOUT.search(detail):
        return "harness_timeout"
    if HALT_DETAIL.search(detail):
        return "halted"
    if WINDOW_DETAIL.search(detail) or (STATUS_4XX.search(detail)
                                        and CONTEXT_TEXT.search(detail)):
        return "window"
    if REFUSAL_TEXT.search(detail):
        return "refused"
    if BLANK_DETAIL.search(detail):
        if evidence["kinds"].get("blank_refusal") or evidence["cli_refusals"]:
            return "refused"
        if evidence["kinds"].get("blank_length"):
            return "unruled"
        return "platform"
    if re.search(r"\bTruncated\b", detail):
        return "unruled" if evidence["ceiling"] else "unclassified"
    if PLATFORM_DETAIL.search(detail):
        return "platform"
    return "unclassified"


def classify(row: dict, exit_code, report: dict | None, stderr: str,
             calls: list[dict], killed: bool, dumps: dict[str, int] | None = None
             ) -> tuple[str, list[str]]:
    """678/681/684: whose failure this attempt is. (state, reasons).

    Limits first, because they stop the lane whatever else went wrong. Then a
    run that completed (exit 0, 1 or 3) is `ok`, whatever unruled calls it
    carried (they are counted beside it). Then each errored step (or,
    with no report, the stderr) is read on its own and the cell takes the first
    of `PRECEDENCE` among them. `model_failure` needs positive evidence (the
    tool's sentence and a `failed` ledger row), `refused` and `unruled` read the
    structured discard kinds, the ledger's `ceiling` outcome and the CLI's
    envelopes, and anything else is `unclassified`, never the model's.
    """
    google = row["route"].get("profile") == "google"
    prov = (report or {}).get("provenance") or {}
    details = [str(step.get("detail") or "") for step in (report or {}).get("steps") or []
               if step.get("state") == "errored"]
    texts = details if report is not None else [stderr]
    cli_errors = _cli_error_texts(calls)
    if route_kind(row) == "claude":
        for c, text in zip([c for c in calls if (c.get("envelope") or {}).get("is_error")
                            or c.get("rc")], cli_errors, strict=True):
            env = c.get("envelope") or {}
            if USAGE_LIMIT.search(text) or SPEND_LIMIT.search(text):
                return "usage_limit", [str(env.get("result") or c.get("stderr"))[:300]]
            if env.get("api_error_code") == "claude_code_version_too_old":
                return "halted", [str(env.get("result"))[:200]]
    readable = [t for t in texts + cli_errors if not MODEL_OUTPUT.search(t)]
    joined = "\n".join(readable)
    if google and PER_DAY_QUOTA.search(joined) and FREE_QUOTA.search(joined):
        return "usage_limit", ["the free tier's daily quota"]
    if google and BILLING.search(joined) and not FREE_QUOTA.search(joined):
        return "halted", ["a billing signal from Google (the free tier only; 624)"]
    if not google and SPEND_LIMIT.search(joined):
        hit = next(t for t in readable if SPEND_LIMIT.search(t))
        return "usage_limit", [hit.strip()[-300:]]
    if killed:
        if row.get("hosting") == "self":
            return "harness_timeout", ["the runner's cell wall limit stopped the cell ("
                                       "the registration's limit, not the model)"]
        return "platform", ["the runner's wall limit stopped the cell"]
    if report is not None and exit_code in (0, 1, 3):
        return "ok", []
    ledger = prov.get("ledger") or []
    evidence = {
        "kinds": discard_kinds(report) if report is not None else dict(dumps or {}),
        "ceiling": any(r.get("outcome") == "ceiling" for r in ledger)
        or "ceiling" in ((prov.get("unruled") or {}).get("calls") or {})
        or any(isinstance(r.get("completion_tokens"), int) and isinstance(
            r.get("max_tokens"), int) and r["completion_tokens"] >= r["max_tokens"]
            for r in ledger),
        # The tool writes `outcome` on every ledger row; a report without the field
        # is from before that, where the sentence alone is the evidence.
        "failed_rows": any(r.get("outcome") == "failed" for r in ledger)
        or (bool(ledger) and not any("outcome" in r for r in ledger)),
        "cli_refusals": sum(1 for c in calls if cli_refusal(c.get("envelope"))),
        "self_hosted": row.get("hosting") == "self",
    }
    found = [(step_class(t, evidence), t) for t in texts + ([] if report is not None
                                                            else cli_errors) if t.strip()]
    if not found:
        return "unclassified", [f"exit {exit_code} with a report and no errored step: "
                                f"{stderr.strip()[-200:]}" if report is not None else
                                f"exit {exit_code}, no report: {stderr.strip()[-200:]}"]
    state = min((s for s, _ in found), key=PRECEDENCE.index)
    return state, [t.strip()[-300:] if report is None else t[:300]
                   for s, t in found if s == state]


# --- the subscription's reset time ------------------------------------------------------

_MONTHS = {m: i for i, m in enumerate(("jan", "feb", "mar", "apr", "may", "jun", "jul",
                                       "aug", "sep", "oct", "nov", "dec"), 1)}
_EPOCH = re.compile(r"limit reached\|(\d{10})\b")
_RESET = re.compile(
    r"resets?(?:\s+at)?\s+(?:(?P<mon>[A-Za-z]{3,9})\.?\s+(?P<day>\d{1,2})(?:st|nd|rd|th)?,?"
    r"\s+(?:at\s+)?)?(?P<hour>\d{1,2})(?::(?P<min>\d{2}))?\s*(?P<ampm>[ap]\.?m\.?)?"
    r"(?:\s*\((?P<tz>[A-Za-z_]+(?:/[A-Za-z_+\-]+)*)\))?", re.I)


def parse_reset(text: str, now: datetime) -> datetime | None:
    """When a subscription limit lifts, from the CLI's message; None if it does not say.

    The CLI names the time on the operator's own clock ("resets 3pm
    (Europe/Berlin)", "resets Oct 1, 3pm"), or, in older builds, the epoch after
    a bar ("limit reached|1759327200"). A time with no zone is read in this
    machine's zone; a time with no date is the next such time after `now`.
    """
    epoch = _EPOCH.search(text)
    if epoch:
        return datetime.fromtimestamp(int(epoch.group(1)), timezone.utc)
    found = _RESET.search(text)
    if not found:
        return None
    hour, minute = int(found["hour"]), int(found["min"] or 0)
    ampm = (found["ampm"] or "").lower().replace(".", "")
    if ampm:
        if not 1 <= hour <= 12:
            return None
        hour = hour % 12 + (12 if ampm == "pm" else 0)
    if hour > 23 or minute > 59:
        return None
    if found["tz"]:
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # noqa: PLC0415
        try:
            zone = ZoneInfo(found["tz"])
        except (ZoneInfoNotFoundError, ValueError):
            return None
    else:
        zone = datetime.now().astimezone().tzinfo
    local = now.astimezone(zone)
    if found["mon"]:
        month = _MONTHS.get(found["mon"][:3].lower())
        if month is None:
            return None
        try:
            when = local.replace(month=month, day=int(found["day"]), hour=hour, minute=minute,
                                 second=0, microsecond=0)
        except ValueError:
            return None
        if when < local - timedelta(days=1):
            when = when.replace(year=when.year + 1)
        return when.astimezone(timezone.utc)
    when = local.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if when <= local:
        when += timedelta(days=1)
    return when.astimezone(timezone.utc)


def run_process(argv: list[str], env: dict, cwd: Path, limit: float) -> tuple:
    """(exit code, stdout, stderr, seconds, killed). The whole process group on a kill."""
    started = time.monotonic()
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            env=env, cwd=str(cwd), start_new_session=True)
    killed = False
    try:
        out, err = proc.communicate(timeout=limit)
    except subprocess.TimeoutExpired:
        killed = True
        with contextlib.suppress(ProcessLookupError):
            os.killpg(proc.pid, signal.SIGTERM)
        try:
            out, err = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(proc.pid, signal.SIGKILL)
            out, err = proc.communicate()
    return proc.returncode, out or "", err or "", time.monotonic() - started, killed


# --- reusing a cell's own earlier answers (the outage ruling) -----------------------------

def _reuse_sources(journal: Journal, records: list[dict], cell: Cell) -> list[dict]:
    """The end records of this cell's earlier attempts whose live answers may be reused.

    Only the same cell id (row, set, item, draw) in the same run directory, only
    real attempts (never a verdict record), and only an attempt that stopped for
    a reason outside the model: never one that finished (`ok` and every final
    state are never re-run), and never one a runner assertion failed on.
    """
    return [end for end in ends(records).get(cell.id, [])
            if end.get("kind", "cell") == "cell" and not end.get("verdict")
            and end.get("state") in REUSE_FROM_STATES and not end.get("assertions_failed")
            and end.get("dir")]


def seed_reuse(journal: Journal, records: list[dict], cell: Cell,
               cell_dir: Path) -> dict[str, dict]:
    """Copy the earlier attempts' kept answers into this attempt's cache. {file: origin}.

    Each earlier attempt's `cache/responses/` holds every answer the tool got
    live in it (and the ones it was itself given), keyed by the whole request.
    The earliest attempt that holds a file is its origin. Nothing is shared
    across cells, draws or runs: the files come from this cell's own directories.
    """
    target = cell_dir / "cache" / "responses"
    seeded: dict[str, dict] = {}
    for end in _reuse_sources(journal, records, cell):
        source = journal.path.parent / end["dir"] / "cache" / "responses"
        if not source.is_dir():
            continue
        for path in sorted(source.glob("*.json")):
            if path.name in seeded:
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                continue
            target.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target / path.name)
            seeded[path.name] = {"attempt": end["attempt"], "dir": end["dir"],
                                 "role": (data.get("request") or {}).get("role"),
                                 "latency_ms": (data.get("meta") or {}).get("latency_ms"),
                                 "content": _cassette_content(data)}
    return seeded


def _cassette_content(data: dict) -> str | None:
    """The answer text a kept response carries (a `claude` route's is its `result`)."""
    try:
        body = json.loads((data.get("response") or {}).get("raw") or "")
        return body["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        return None


def account_reuse(ctx: Context, journal: Journal, row: dict, cell: Cell,
                  report: dict | None, seeded: dict[str, dict],
                  records: list[dict]) -> tuple[dict | None, list[str]]:
    """What this attempt reused, with each call's original time and cost; and what is wrong.

    Every reused answer is counted once: its original measured `answer_ms`
    (read off the earlier attempt's own report, matched by `request_sha256`; an
    attempt a crash left with no report gives its kept `latency_ms` instead,
    said so), and its original cost (an HTTP row's report already prices the
    reused row by its tokens, the same tokens; a `claude` route's is the
    earlier envelope's `total_cost_usd`, matched by its answer text). Refused
    as an assertion: a cache hit with nothing seeded (a request repeated inside
    one run and answered from the cache, not live), a reused answer no earlier
    live call of this cell accounts for, or a count per role that does not line
    up with what was seeded.
    """
    prov = (report or {}).get("provenance") or {}
    hits = [r for r in prov.get("ledger") or [] if r.get("source") == "cache"]
    counted = int((prov.get("counts") or {}).get("cache_hits") or 0)
    problems: list[str] = []
    if not seeded:
        if hits or counted:
            problems.append(f"{counted or len(hits)} cache hit(s) with no earlier live answer "
                            f"of this cell: a request repeated inside one run was answered "
                            f"from the cache, not live")
        return None, problems
    if report is None:
        return {"seeded": len(seeded), "served": None,
                "note": "no report: what was served is unknown"}, problems
    seeded_roles: dict[str, int] = {}
    for info in seeded.values():
        seeded_roles[str(info["role"])] = seeded_roles.get(str(info["role"]), 0) + 1
    served_roles: dict[str, int] = {}
    for r in hits:
        served_roles[str(r.get("role"))] = served_roles.get(str(r.get("role")), 0) + 1
    if served_roles != seeded_roles:
        problems.append(f"reuse did not line up: seeded {seeded_roles}, served "
                        f"{served_roles}")
    base_dir = journal.path.parent
    earlier: dict[str, list[tuple[int, dict]]] = {}
    reported = set()
    for end in _reuse_sources(journal, records, cell):
        path = base_dir / end["dir"] / "report.json"
        if not path.is_file():
            continue
        reported.add(end["attempt"])
        try:
            rows = ((json.loads(path.read_text(encoding="utf-8")).get("provenance") or {})
                    .get("ledger") or [])
        except ValueError:
            continue
        for r in rows:
            if r.get("source") == "live" and r.get("request_sha256"):
                earlier.setdefault(r["request_sha256"], []).append((end["attempt"], r))
    calls, answer_ms, unmatched = [], 0, 0
    for r in hits:
        found = earlier.get(str(r.get("request_sha256"))) or []
        if found:
            attempt, orig = found.pop(0)
            ms = orig.get("answer_ms")
            calls.append({"role": r.get("role"), "request_sha256": r.get("request_sha256"),
                          "from_attempt": attempt, "answer_ms": ms,
                          "prompt_tokens": orig.get("prompt_tokens"),
                          "completion_tokens": orig.get("completion_tokens")})
            answer_ms += int(ms or 0)
        else:
            unmatched += 1
    # A hit no earlier report accounts for must come from an attempt that left no
    # report (a crash): its kept latency stands in, retries included, said so.
    from_crash = [info for info in seeded.values() if info["attempt"] not in reported]
    if unmatched > len(from_crash):
        problems.append(f"{unmatched - len(from_crash)} reused answer(s) no earlier live call "
                        f"of this cell accounts for")
    latency_ms = sum(int(info.get("latency_ms") or 0) for info in from_crash[:unmatched])
    out = {"seeded": len(seeded), "served": len(hits), "by_role": served_roles,
           "from_attempts": sorted({info["attempt"] for info in seeded.values()}),
           "answer_ms": answer_ms + latency_ms,
           "time_basis": "answer_ms" if not latency_ms else
           "answer_ms, and latency_ms (retries included) for an attempt that left no report",
           "calls": calls}
    if route_kind(row) == "claude":
        envelopes: list[dict] = []
        for end in _reuse_sources(journal, records, cell):
            envelopes += [c["envelope"] for c in read_calls(base_dir / end["dir"] / "calls")
                          if envelope_answered(c)]
        usd, per_model, missing = 0.0, {}, 0
        for info in seeded.values():
            match = next((e for e in envelopes if str(e.get("result") or "") == info["content"]),
                         None)
            if match is None:
                missing += 1
                continue
            envelopes.remove(match)
            usd += float(match.get("total_cost_usd") or 0)
            for model, usage in (match.get("modelUsage") or {}).items():
                slot = per_model.setdefault(model, {})
                for key, value in (usage or {}).items():
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        slot[key] = slot.get(key, 0) + value
        if missing:
            problems.append(f"{missing} reused CLI answer(s) with no earlier envelope to price "
                            f"them")
        out["cli"] = {"usd": usd, "per_model": per_model}
    else:
        out["usd"] = pricing.estimate(hits).dollars or 0.0
    return out, problems


# --- by ruling: an unruled cell counts against its row, with its cause ------------------

def unruled_calls(report: dict | None) -> list[dict]:
    """The calls that ended the run unruled: a ceiling cut, a blank on length."""
    prov = (report or {}).get("provenance") or {}
    out = []
    for r in prov.get("ledger") or []:
        if r.get("outcome") == "ceiling" or (
                isinstance(r.get("completion_tokens"), int) and isinstance(r.get("max_tokens"), int)
                and r["completion_tokens"] >= r["max_tokens"]):
            out.append(dict(r, cause="ceiling cut"))
    for r in prov.get("discarded_calls") or []:
        if r.get("kind") == "blank_length":
            out.append(dict(r, cause="blank after thinking (length)"))
    return out


def limit_flag(row: dict, call: dict) -> str:
    """A self-hosted unruled call: the model's own `limit`, or our `config`.

    `limit`: the cut came at a limit of the model itself, its maximum output or
    its maximum context (`model_limits`), or at a served window that already
    equals the model's context. `config`: at a ceiling or a window we set below
    the model's own limits, so the registration is wrong; and where the numbers
    do not say, `config` too, until the run report documents it.
    """
    limits = row["model_limits"]
    context, output = limits["context_tokens"], limits["output_tokens"]
    prompt, done, ceiling = (call.get("prompt_tokens"), call.get("completion_tokens"),
                             call.get("max_tokens"))
    if isinstance(ceiling, int) and isinstance(done, int) and done >= ceiling:
        return "limit" if ceiling >= output else "config"
    if isinstance(prompt, int) and isinstance(done, int):
        if done >= output or prompt + done >= context:
            return "limit"
        if prompt + done >= row["window"]:
            return "limit" if row["window"] >= context else "config"
    return "config"


def unruled_ruling(row: dict, report: dict | None, dumps: dict[str, int] | None) -> dict:
    """How an unruled cell counts against its row, with the numbers."""
    calls = unruled_calls(report)
    causes = sorted({c["cause"] for c in calls}) or (
        ["blank after thinking (length)"] if (dumps or {}).get("blank_length")
        else ["ceiling cut"])
    numbers = [{k: c.get(k) for k in ("role", "cause", "prompt_tokens", "completion_tokens",
                                      "max_tokens")} for c in calls]
    if row.get("hosting") != "self":
        return {"unruled_as": "model_failure", "unruled_cause": causes,
                "flag": f"model failure (unruled: {', '.join(causes)})",
                "unruled_numbers": numbers}
    flags = [limit_flag(row, c) for c in calls] or ["config"]
    flag = "config" if "config" in flags else "limit"
    for entry, one in zip(numbers, flags):
        entry["flag"] = one
    return {"unruled_as": flag, "unruled_cause": causes,
            "flag": ("CONFIG: the registration set a ceiling or window below the model's own "
                     "limits, or the numbers do not say; document it in the run report"
                     if flag == "config" else "limit: the model's own limit"),
            "unruled_numbers": numbers, "window": row["window"],
            "model_limits": {k: row["model_limits"][k]
                             for k in ("context_tokens", "output_tokens")}}


def write_limits_stub(ctx: Context) -> Path | None:
    """SELF-HOSTED-LIMITS.md: every self-hosted unruled cell, with its numbers."""
    cells = [r for r in ctx.journal.read() if r.get("type") == "end"
             and r.get("kind", "cell") == "cell"
             and (r.get("state") == "unruled" and r.get("unruled_as") in ("limit", "config")
                  or r.get("state") == "harness_timeout")]
    if not cells:
        return None
    lines = ["# Self-hosted limits (a stub the runner writes; document every cell in the run "
             "report)", "",
             "By operator ruling of 2026-09-28, a self-hosted row fails only when it is misconfigured "
             "or hits the model's own limits, and either is documented. `limit` is the "
             "model's own (its maximum context or output); `config` means the registration "
             "set a ceiling or window below the model's limits (or the numbers do not say), "
             "so the registration is wrong: every CONFIG cell must be explained in the run "
             "report, with the fix.", "",
             "| cell | attempt | flag | cause | role | prompt tokens | completion tokens | "
             "ceiling sent | stated window | model context | model output |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for end in cells:
        # A cell id carries `|`, which a Markdown table reads as a column break.
        end = dict(end, cell=end["cell"].replace("|", "\\|"))
        if end["state"] == "harness_timeout":
            lines.append(f"| {end['cell']} | a{end['attempt']} | CONFIG | harness timeout "
                         f"(--timeout {end.get('timeout_seconds')}s, cell wall "
                         f"{end.get('cell_wall_seconds')}s) | - | - | - | - | - | - | - |")
            continue
        numbers = end.get("unruled_numbers") or [{}]
        limits = end.get("model_limits") or {}
        for n in numbers:
            lines.append(
                f"| {end['cell']} | a{end['attempt']} | "
                f"{str(n.get('flag') or end['unruled_as']).upper()} | "
                f"{n.get('cause') or ', '.join(end.get('unruled_cause') or [])} | "
                f"{n.get('role') or '-'} | {n.get('prompt_tokens', '-')} | "
                f"{n.get('completion_tokens', '-')} | {n.get('max_tokens', '-')} | "
                f"{end.get('window', '-')} | {limits.get('context_tokens', '-')} | "
                f"{limits.get('output_tokens', '-')} |")
    lines += ["", "## To document", ""]
    lines += [f"- `{end['cell']}` a{end['attempt']} "
              f"({'CONFIG, harness timeout' if end['state'] == 'harness_timeout' else end['unruled_as'].upper()}): "
              f"<FILL: why, and what the registration should say>" for end in cells]
    path = ctx.run_dir / "SELF-HOSTED-LIMITS.md"
    path.write_text(ctx.redactor.text("\n".join(lines) + "\n"), encoding="utf-8")
    return path


def run_cell(ctx: Context, cell: Cell, attempt: int, lane: str, *,
             journal: Journal | None = None, thinking: list[str] | None = None,
             kind: str = "cell") -> dict:
    """One attempt at one cell: begin record, the run, the checks, the end record.

    A counted cell's retry reuses the answers its earlier attempts got live
    `seed_reuse` before the run, `account_reuse` after it. A reference
    check and a pilot cell never do: each must reach its endpoint afresh.
    """
    journal = journal or ctx.journal
    row = ctx.row(cell.row)
    records = journal.read()
    proj = projection(ctx, row, cell, records)
    base = {"cell": cell.id, "row": cell.row, "set": cell.set, "item": cell.item,
            "draw": cell.draw, "attempt": attempt, "lane": lane, "kind": kind,
            "vendor": row["vendor"], "metered": metered(row), "model": row["model"]}
    before = check_clone(ctx.clone, ctx.reg["pin"])
    if before:
        raise Refusal("before " + cell.id + ": " + "; ".join(before), EXIT_REFUSED)
    if route_kind(row) == "claude" and sha256_file(claude_binary(ctx)) != \
            ctx.reg["claude"]["sha256"]:
        raise Refusal(f"before {cell.id}: the `claude` binary no longer hashes as "
                      f"registered", EXIT_REFUSED)
    cell_dir = cell.dir(journal.path.parent, attempt)
    if cell_dir.exists():
        shutil.rmtree(cell_dir)
    cell_dir.mkdir(parents=True)
    names, size = copy_inputs(ctx, cell, cell_dir)
    seeded = seed_reuse(journal, records, cell, cell_dir) if kind == "cell" else {}
    env = cell_env(ctx, row, cell_dir)
    argv = cell_argv(ctx, row, cell, names, thinking)
    # The argv as it ran, less the pod's address: `$NAME` in its place.
    (cell_dir / "argv.json").write_text(json.dumps(ctx.redactor.obj(argv[1:]), indent=1),
                                        encoding="utf-8")
    (cell_dir / "env_names.json").write_text(json.dumps(sorted(env), indent=1),
                                             encoding="utf-8")
    started = now()
    journal.append({**base, "type": "begin", "at": started, "dir": str(
        cell_dir.relative_to(journal.path.parent)), "projection_usd": round(proj, 6),
        "projection_seconds": round(projected_seconds(ctx, row, cell, records), 1)})
    code, out, err, seconds, killed = run_process(argv, env, cell_dir, cell_wall(ctx, row))
    (cell_dir / "report.md").write_text(ctx.redactor.text(out), encoding="utf-8")
    (cell_dir / "stderr.log").write_text(ctx.redactor.text(err), encoding="utf-8")
    report = None
    if (cell_dir / "report.json").is_file():
        try:
            report = json.loads((cell_dir / "report.json").read_text(encoding="utf-8"))
        except ValueError:
            report = None
    calls = read_calls(cell_dir / "calls")
    dumps = discard_kinds(None, cell_dir) if report is None else None
    state, reasons = classify(row, code, report, err, calls, killed, dumps=dumps)
    problems = check_report(ctx, row, cell, report, thinking) if report is not None else []
    reuse, reuse_problems = account_reuse(ctx, journal, row, cell, report, seeded, records)
    problems += reuse_problems
    if reuse is not None:
        (cell_dir / "reuse.json").write_text(json.dumps(reuse, indent=1) + "\n",
                                             encoding="utf-8")
    if route_kind(row) == "claude":
        problems += check_calls(ctx, row, calls)
        if sha256_file(claude_binary(ctx)) != ctx.reg["claude"]["sha256"]:
            problems.append("the `claude` binary no longer hashes as registered")
    after = check_clone(ctx.clone, ctx.reg["pin"])
    problems += [f"after the cell: {line}" for line in after]
    money = charge(ctx, row, report, calls, proj, stderr=err, killed=killed,
                   reused_usd=float((reuse or {}).get("usd") or 0.0))
    if money.get("unpriced_calls"):
        problems.append(f"{money['unpriced_calls']} call(s) of a metered row were unpriced; "
                        f"the cap cannot hold them")
    if problems:
        state, reasons = "halted", problems
    prov = (report or {}).get("provenance") or {}
    ruled: dict = {}
    if state == "refused":
        ruled["flag"] = REFUSED_FLAG
    elif state == "unruled":
        ruled = unruled_ruling(row, report, dumps)
    elif state == "harness_timeout":
        ruled = {"flag": HARNESS_FLAG, "timeout_seconds": row_timeout(ctx, row),
                 "cell_wall_seconds": cell_wall(ctx, row), "killed": killed}
    end = {**base, "type": "end", "state": state, "reasons": reasons, "started_at": started,
           "ended_at": now(), "exit_code": code, "killed": killed,
           "wall_seconds": round(seconds, 1), "report": report is not None,
           "dir": str(cell_dir.relative_to(journal.path.parent)), "input_bytes": size,
           "claimcheck_commit": prov.get("claimcheck_commit"),
           "calls": (prov.get("counts") or {}).get("calls"),
           "cli_calls": len(calls), "projection_usd": round(proj, 6),
           "answering_seconds": (prov.get("answering_seconds") or {}).get("total"),
           "answering_usd": (prov.get("answering_cost") or {}).get("usd_exact"),
           "excluded_usd": ((prov.get("excluded") or {}).get("cost") or {}).get("usd_exact"),
           "unruled_usd": ((prov.get("unruled") or {}).get("cost") or {}).get("usd_exact"),
           **money, **ruled}
    if problems:
        # A runner assertion failed: nothing this attempt got is ever reused.
        end["assertions_failed"] = True
    if reuse is not None:
        end["reused_calls"] = reuse.get("served")
        end["reused_answer_ms"] = reuse.get("answer_ms")
    if state == "ok" and (prov.get("unruled") or {}).get("calls"):
        # A run that completed is scored; the calls the tool left unruled
        # inside it are counted beside it, and are already out of its answering
        # cost and seconds.
        end["unruled_calls"] = dict(prov["unruled"]["calls"])
    if state == "usage_limit" and route_kind(row) == "claude":
        reset = parse_reset(" ".join(reasons), ctx.clock())
        end["reset_at"] = reset.isoformat(timespec="seconds") if reset else None
    if route_kind(row) == "claude":
        end["claude_sha256"] = sha256_file(claude_binary(ctx))
        end["claude_realpaths"] = sorted({str(c.get("realpath")) for c in calls})
    if thinking is not None:
        end["thinking"] = sorted(thinking)
    # Everything the cell wrote, the tool's report and dumps included, less the
    # pod's address. The inputs and the merge are the documents'
    # own text and are never rewritten. The tool's capability record keys the
    # endpoint by its resolved address (`structured.endpoint_key`), which no
    # literal form of the URL matches; for a secret address it goes. A
    # `--no-cache` cell's cache holds nothing else, and its report carries
    # the pinned tier.
    if row["route"].get("base_url_env") and ctx.redactor.forms:
        with contextlib.suppress(FileNotFoundError):
            (cell_dir / "cache" / "capabilities.json").unlink()
    ctx.redactor.tree(cell_dir, keep=set(names) | {"merged.md"})
    journal.append(end)
    ctx.say(f"  [{cell.id} a{attempt}] {state} exit={code} {seconds:.1f}s "
            f"charged ${money['charged_usd']:.4f}"
            + (f" reused {end['reused_calls']} call(s)" if end.get("reused_calls") else "")
            + (f" [{ruled['flag']}]" if ruled.get("flag") else "")
            + (f" -- {'; '.join(reasons)[:300]}" if reasons else ""))
    if (ruled.get("unruled_as") in ("limit", "config") or state == "harness_timeout") \
            and journal is ctx.journal:
        stub = write_limits_stub(ctx)
        if state == "harness_timeout":
            ctx.say(f"CONFIG: {cell.id} was cut by the harness's own timeout (--timeout "
                    f"{row_timeout(ctx, row):g}s, cell wall {cell_wall(ctx, row):g}s), not by "
                    f"the model: the registration's timeout is too short for this card; "
                    f"document it in the run report ({stub})")
        elif ruled["unruled_as"] == "config":
            ctx.say(f"CONFIG: {cell.id} was cut by a ceiling or window the registration set "
                    f"below the model's own limits (or the numbers do not say): the "
                    f"registration is wrong; document it in the run report ({stub})")
    return journal.redact(end)


# --- pre-warm --------------------------------------------------------------------------------

def _http(url: str, *, data: dict | None = None, key: str | None = None,
          timeout: float = 120) -> tuple[int, str]:
    body = None if data is None else json.dumps(data).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST" if body else "GET")
    request.add_header("Content-Type", "application/json")
    if key:
        request.add_header("Authorization", f"Bearer {key}")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")[:300]
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        return 0, f"{type(exc).__name__}: {exc}"


def default_probe(ctx: Context, urls: list[str]) -> bool:
    """The network is back when every probe URL answers with any HTTP status.

    A 401 or a 404 is an answer: the address was reached. No key is sent and no
    token is spent. Status 0 is `_http`'s word for nothing came back.
    """
    return all(_http(url, timeout=30)[0] != 0 for url in urls)


def prewarm(ctx: Context, row: dict, lane: str, why: str) -> bool:
    """Wait for health, then one untimed warm-up request. Recorded, never a cell."""
    spec = ctx.reg["lanes"][lane].get("prewarm") or {}
    limit = float(spec.get("timeout_seconds", 900))
    key = secret(ctx, row["route"]["key_env"]) if row["route"].get("key_env") else None
    started = time.monotonic()
    event = {"type": "event", "event": "prewarm", "lane": lane, "row": row["id"],
             "why": why, "at": now()}
    health = spec.get("health_url") or (secret(ctx, spec["health_url_env"])
                                        if spec.get("health_url_env") else None)
    if health:
        tries = 0
        while True:
            tries += 1
            status, text = _http(health, key=key if spec.get("health_auth", True) else None,
                                 timeout=30)
            if status == 200:
                break
            if time.monotonic() - started > limit:
                event.update(ok=False, health_status=status, health_tries=tries,
                             detail=text[:200],
                             total_seconds=round(time.monotonic() - started, 1))
                ctx.journal.append(event)
                return False
            ctx.sleep(float(spec.get("poll_seconds", 10)))
        event.update(health_status=status, health_tries=tries,
                     health_seconds=round(time.monotonic() - started, 1))
    warm_started = time.monotonic()
    tries = 0
    body = {"model": row["model"], "messages": [{"role": "user", "content": WARM_UP_PROMPT}],
            "max_tokens": 16, "stream": False}
    while True:
        tries += 1
        status, text = _http(base_url(ctx, row) + "/chat/completions", data=body, key=key,
                             timeout=float(spec.get("request_timeout_seconds", 600)))
        if status == 200:
            break
        if time.monotonic() - started > limit:
            event.update(ok=False, warm_status=status, warm_tries=tries, detail=text[:200],
                         total_seconds=round(time.monotonic() - started, 1))
            ctx.journal.append(event)
            return False
        ctx.sleep(float(spec.get("poll_seconds", 10)))
    event.update(ok=True, warm_status=status, warm_tries=tries,
                 warm_seconds=round(time.monotonic() - warm_started, 1),
                 total_seconds=round(time.monotonic() - started, 1))
    ctx.journal.append(event)
    ctx.say(f"  [prewarm {row['id']}] ready after {event['total_seconds']}s ({why})")
    return True


# --- a lane ----------------------------------------------------------------------------------

@dataclass
class LaneRun:
    ctx: Context
    lane: str
    max_cells: int | None = None
    ran: int = 0
    streak: int = 0
    limit_sleeps: int = 0
    warmed: dict = field(default_factory=dict)
    paused: float = 0.0  # seconds this start has paused for outages

    def pending_main(self, records: list[dict]) -> list[Cell]:
        """Cells never run, or stopped for a reason outside the model. Never a finished one.

        A cell whose latest attempt is final (`ok`, or the row's own result) is
        never run again, whatever happened after it (an outage throws
        nothing away).
        """
        done = ends(records)
        out = []
        for cell in plan(self.ctx.reg, self.lane):
            state = latest_state(done.get(cell.id, []))
            if state is None or state in ("usage_limit", "interrupted", "halted",
                                          "infrastructure"):
                out.append(cell)
        return out

    def pending_retry(self, records: list[dict]) -> list[Cell]:
        passes = int((self.ctx.reg.get("retry") or {}).get("passes", 2))
        done = ends(records)
        out = []
        for cell in plan(self.ctx.reg, self.lane):
            attempts = done.get(cell.id, [])
            if latest_state(attempts) in ("platform", "unclassified") and \
                    sum(1 for a in attempts if a["state"] in RETRYABLE_STATES) <= passes:
                out.append(cell)
        return out

    def needs_warm(self, row: dict) -> str | None:
        spec = self.ctx.reg["lanes"][self.lane].get("prewarm")
        if not spec:
            return None
        last = self.warmed.get(row["id"])
        if last is None:
            return "first cell"
        idle = time.monotonic() - last
        if idle > float(spec.get("rewarm_after_idle_seconds", 240)):
            return f"idle {idle:.0f}s"
        return None

    def one(self, cell: Cell) -> int | None:
        """Run one cell; an exit code if the lane must stop, else None."""
        ctx = self.ctx
        row = ctx.row(cell.row)
        records = ctx.journal.read()
        stopped = gate(ctx, row, cell, records)
        if stopped:
            ctx.journal.append({"type": "event", "event": "gated", "lane": self.lane,
                                "cell": cell.id, "at": now(), **stopped})
            if stopped["unit"] == "s":
                ctx.say(f"GATED: {cell.id} needs {stopped['need']:.0f} GPU seconds and "
                        f"{stopped['pot']} has {stopped['left']:.0f} left of "
                        f"{stopped['cap']:.0f}; the lane stops")
            else:
                ctx.say(f"GATED: {cell.id} needs ${stopped['need']:.4f} and {stopped['pot']} "
                        f"has ${stopped['left']:.4f} left of ${stopped['cap']:.2f}; the lane "
                        f"stops")
            return EXIT_GATED
        why = self.needs_warm(row)
        if why:
            if not prewarm(ctx, row, self.lane, why):
                ctx.say(f"STOP: pre-warm of {row['id']} never came up")
                return EXIT_BREAKER
        attempt = len(ends(records).get(cell.id, [])) + 1
        end = run_cell(ctx, cell, attempt, self.lane)
        if ctx.reg["lanes"][self.lane].get("prewarm"):
            self.warmed[row["id"]] = time.monotonic()
        self.ran += 1
        if end["state"] == "halted":
            ctx.say(f"STOP: {cell.id} halted: {'; '.join(end['reasons'])[:600]}")
            return EXIT_REFUSED
        if end["state"] == "usage_limit":
            wait = self.usage_limit_wait(row, end)
            if wait is None:
                ctx.say(f"STOP: usage limit at {cell.id}; resume this lane later"
                        + (f" (resets {end['reset_at']})" if end.get("reset_at") else ""))
                return EXIT_USAGE_LIMIT
            # The subscription names its reset; sleep to it and go on.
            self.limit_sleeps += 1
            ctx.journal.append({"type": "event", "event": "usage_limit_sleep",
                                "lane": self.lane, "cell": cell.id, "at": now(),
                                "reset_at": end["reset_at"], "seconds": round(wait, 1)})
            ctx.say(f"usage limit at {cell.id}: sleeping {wait:.0f}s to its reset "
                    f"{end['reset_at']} (plus {USAGE_LIMIT_MARGIN}s), then this cell again")
            ctx.sleep(wait)
            self.warmed.clear()
            return self.one(cell)
        self.limit_sleeps = 0
        if end["state"] in RETRYABLE_STATES:
            self.streak += 1
            breaker = int((ctx.reg.get("retry") or {}).get("breaker", 3))
            if self.streak >= breaker:
                # Is it this endpoint, or everything? The reference decides.
                # Everything (the network): pause and probe, then go on. The
                # endpoint alone: stop as before; its cells keep their passes.
                ctx.say(f"BREAKER: {self.streak} failures in a row outside the model's "
                        f"control at {cell.id}; asking the reference route")
                verdict = self.reference_check(row)
                if isinstance(verdict, int):
                    return verdict
                if verdict == "down":
                    code = self.pause(row, [cell], "the breaker tripped and the reference "
                                                   "failed too")
                    if code is not None:
                        return code
                    self.streak = 0
                else:
                    ctx.say(f"STOP: {self.streak} failures in a row on {row['id']}'s "
                            f"endpoint while the reference answered; resume this lane when "
                            f"the endpoint is back (its cells keep their retry passes)")
                    return EXIT_BREAKER
        else:
            self.streak = 0
        if self.max_cells is not None and self.ran >= self.max_cells:
            return -1
        return None

    # --- the reference check, the verdicts, and the outage pause -----------------------

    def reference_check(self, row: dict) -> str | int:
        """One cheap cell on the row's registered reference route: "ok", "down", or an exit.

        `reference_item` (S1:badge_access, the smallest) on a different vendor's
        route, asserted like any cell, recorded in `cells.jsonl` as kind
        `reference` (charged against its vendor's cap, never scored, never
        reusing an earlier answer). Only a clean `ok` means the reference
        worked; anything outside the model means it did not. A halt, a limit or
        a cap on the reference stops the lane as it would for any cell.
        """
        ctx = self.ctx
        ref = ctx.references[row["reference"]]
        set_id, _, item = ctx.reg["reference_item"].partition(":")
        cell = Cell(f"{ref['id']}~reference", set_id, item, 1)
        ctx.rows[cell.row] = ref
        records = ctx.journal.read()
        stopped = gate(ctx, ref, cell, records)
        if stopped:
            ctx.journal.append({"type": "event", "event": "gated", "lane": self.lane,
                                "cell": cell.id, "at": now(), **stopped})
            ctx.say(f"GATED: the reference check {cell.id} needs ${stopped['need']:.4f} and "
                    f"{stopped['pot']} has ${stopped['left']:.4f} left; the lane stops")
            return EXIT_GATED
        attempt = len(ends(records).get(cell.id, [])) + 1
        end = run_cell(ctx, cell, attempt, self.lane, kind="reference")
        verdict = "ok" if end["state"] == "ok" else "down"
        ctx.journal.append({"type": "event", "event": "reference_check", "lane": self.lane,
                            "row": row["id"], "reference": ref["id"], "cell": cell.id,
                            "attempt": attempt, "state": end["state"], "verdict": verdict,
                            "at": now()})
        ctx.say(f"reference check for {row['id']} on {ref['id']}: {end['state']} -> "
                f"{'the reference works' if verdict == 'ok' else 'the reference failed too'}")
        if end["state"] == "halted":
            ctx.say(f"STOP: the reference {cell.id} halted: {'; '.join(end['reasons'])[:600]}")
            return EXIT_REFUSED
        if end["state"] == "usage_limit":
            ctx.say(f"STOP: usage limit on the reference {cell.id}; resume this lane later")
            return EXIT_USAGE_LIMIT
        return verdict

    def verdict(self, cell: Cell, state: str, reasons: list[str], **extra) -> dict:
        """A verdict record: the cell's final word, from the reference check, not from a run."""
        ctx = self.ctx
        row = ctx.row(cell.row)
        attempts = ends(ctx.journal.read()).get(cell.id, [])
        last = attempts[-1] if attempts else {}
        end = {"type": "end", "cell": cell.id, "row": cell.row, "set": cell.set,
               "item": cell.item, "draw": cell.draw, "attempt": len(attempts) + 1,
               "lane": self.lane, "kind": "cell", "vendor": row["vendor"],
               "metered": metered(row), "model": row["model"], "state": state,
               "reasons": reasons, "verdict": True, "at": now(), "ended_at": now(),
               "started_at": last.get("started_at"), "dir": last.get("dir"),
               "exit_code": last.get("exit_code"), "charged_usd": 0.0,
               "charge_basis": "verdict", "wall_seconds": 0.0, **extra}
        ctx.journal.append(end)
        ctx.say(f"  [{cell.id} a{end['attempt']}] {state} -- {'; '.join(reasons)[:300]}")
        return end

    def attention(self, text: str) -> None:
        """A loud line for the operator: the lane log and OPERATOR-ATTENTION.txt."""
        ctx = self.ctx
        line = f"{now()} lane {self.lane}: {text}"
        ctx.say(f"OPERATOR ATTENTION: {text}")
        with open(ctx.run_dir / "OPERATOR-ATTENTION.txt", "a", encoding="utf-8") as handle:
            handle.write(ctx.redactor.text(line) + "\n")

    def probe_urls(self, row: dict) -> list[str]:
        """What the pause asks: the registered probe URLs, the row's and its reference's."""
        ctx = self.ctx
        urls = []
        for url in (ctx.reg.get("infrastructure") or {}).get("probe_urls") or []:
            urls.append(secret(ctx, url[1:]) if url.startswith("$") else url)
        for route_row in (row, ctx.references.get(row.get("reference")) or {}):
            if (route_row.get("route") or {}).get("kind") == "http":
                with contextlib.suppress(Refusal):
                    urls.append(base_url(ctx, route_row) + "/models")
        return [u for u in dict.fromkeys(urls) if u]

    def pause(self, row: dict, cells: list[Cell], why: str) -> int | None:
        """An outage pauses the lane; nothing is thrown away. None to go on, or an exit.

        Writes OPERATOR-ATTENTION.txt and a lane-log line, then waits and probes
        (`infrastructure.probe_intervals_seconds`, the last one repeated): every
        probe URL must answer with any HTTP status. Resumes on its own when they
        do. After `infrastructure.max_pause_seconds` in this start, the lane
        stops as `paused_infrastructure` (exit 8); `run` again continues from
        there. The sleep, not the wall clock, is what is counted.
        """
        ctx = self.ctx
        infra = ctx.reg.get("infrastructure") or {}
        intervals = [float(v) for v in infra.get("probe_intervals_seconds") or [120]]
        limit = float(infra.get("max_pause_seconds", 43200))
        urls = self.probe_urls(row)
        self.attention(f"infrastructure: {why} ({row['id']}; cells "
                       f"{', '.join(c.id for c in cells)}). Pausing: probing "
                       f"{len(urls)} address(es) every {intervals[0]:g}s and later every "
                       f"{intervals[-1]:g}s, for at most {limit:g}s in all "
                       f"({self.paused:g}s used). The lane resumes on its own; nothing "
                       f"recorded is discarded.")
        event = {"type": "event", "event": "infrastructure_pause", "lane": self.lane,
                 "row": row["id"], "cells": [c.id for c in cells], "why": why, "at": now()}
        probes = 0
        while True:
            wait = intervals[min(probes, len(intervals) - 1)]
            if self.paused + wait > limit:
                event.update(resumed=False, probes=probes, paused_seconds=self.paused,
                             ended_at=now())
                ctx.journal.append(event)
                ctx.journal.append({"type": "event", "event": "paused_infrastructure",
                                    "lane": self.lane, "at": now(),
                                    "paused_seconds": self.paused})
                self.attention(f"paused_infrastructure: {self.paused:g}s of pause used, the "
                               f"registered maximum is {limit:g}s; the lane stops (exit "
                               f"{EXIT_PAUSED}). `run` again continues from here.")
                return EXIT_PAUSED
            ctx.sleep(wait)
            self.paused += wait
            probes += 1
            if ctx.probe(ctx, urls):
                event.update(resumed=True, probes=probes, paused_seconds=self.paused,
                             ended_at=now())
                ctx.journal.append(event)
                self.warmed.clear()
                self.attention(f"infrastructure back after {probes} probe(s); the lane "
                               f"resumes ({self.paused:g}s of pause used in this start)")
                return None

    def settle(self) -> int | None:
        """A cell still failing after every retry pass.

        Per row, one reference check. The reference works: each such cell is the
        row's own `endpoint_failure` ("endpoint failed while reference worked"),
        counted against the row, never shrinking another row's pairs. The
        reference fails too: `infrastructure`, never scored; the lane pauses and
        probes, and when the network is back runs each such cell again (reusing
        what it already got), and settles what is still failing the same way.
        """
        ctx = self.ctx
        while True:
            done = ends(ctx.journal.read())
            left = [c for c in plan(ctx.reg, self.lane)
                    if latest_state(done.get(c.id, [])) in ("platform", "unclassified")]
            if not left:
                return None
            by_row: dict[str, list[Cell]] = {}
            for cell in left:
                by_row.setdefault(cell.row, []).append(cell)
            rerun: list[Cell] = []
            for rid, cells in by_row.items():
                row = ctx.row(rid)
                verdict = self.reference_check(row)
                if isinstance(verdict, int):
                    return verdict
                ref = row["reference"]
                if verdict == "ok":
                    for cell in cells:
                        self.verdict(cell, "endpoint_failure",
                                     [f"{ENDPOINT_FLAG}: failed on the platform after every "
                                      f"retry pass; the reference {ref} answered"],
                                     flag=ENDPOINT_FLAG, reference=ref)
                    continue
                for cell in cells:
                    self.verdict(cell, "infrastructure",
                                 [f"infrastructure: failed after every retry pass and the "
                                  f"reference {ref} failed too; not scored, run again when "
                                  f"the network is back"], reference=ref)
                code = self.pause(row, cells, "a cell failed every retry pass and the "
                                              "reference failed too")
                if code is not None:
                    return code
                rerun += cells
            for cell in rerun:
                code = self.one(cell)
                if code == -1:
                    return EXIT_DONE
                if code is not None:
                    return code

    def usage_limit_wait(self, row: dict, end: dict) -> float | None:
        """Seconds to sleep before the subscription's limit lifts; None to stop the lane.

        Only a command route (the subscription) sleeps: a vendor's spend or credit
        limit needs a top-up, not a wait. None when the message names no reset,
        when the reset is further off than `retry.usage_limit_max_sleep_seconds`
        (default three days, the registered window), or after `USAGE_LIMIT_SLEEPS`
        sleeps in a row that did not lift it.
        """
        if route_kind(row) != "claude" or not end.get("reset_at"):
            return None
        if self.limit_sleeps >= USAGE_LIMIT_SLEEPS:
            return None
        retry = self.ctx.reg.get("retry") or {}
        cap = float(retry.get("usage_limit_max_sleep_seconds", 3 * 86400))
        reset = datetime.fromisoformat(end["reset_at"])
        wait = (reset - self.ctx.clock()).total_seconds() + USAGE_LIMIT_MARGIN
        return max(wait, 0.0) if wait <= cap else None

    def run(self) -> int:
        ctx = self.ctx
        lock = ctx.run_dir / "locks" / f"{self.lane}.lock"
        lock.parent.mkdir(parents=True, exist_ok=True)
        with open(lock, "a+", encoding="utf-8") as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                raise Refusal(f"lane {self.lane} is already running", EXIT_REFUSED) from None
            records = ctx.journal.read()
            for begin in dangling(records, self.lane):
                ctx.journal.append({**{k: begin[k] for k in (
                    "cell", "row", "set", "item", "draw", "attempt", "lane", "kind", "vendor",
                    "metered", "model", "dir")}, "type": "end", "state": "interrupted",
                    "reasons": ["the runner stopped during this attempt"],
                    "ended_at": now(), "charged_usd": begin.get("projection_usd", 0.0)
                    if begin.get("metered") else 0.0, "charge_basis": "estimate_interrupted",
                    # Its GPU time is unknown: charged at its projection, like its dollars.
                    "wall_seconds": begin.get("projection_seconds", 0.0)})
            ctx.journal.append({"type": "event", "event": "start", "lane": self.lane,
                                "at": now(), "pid": os.getpid(),
                                "block_sha256": ctx.block_sha256,
                                "claude_version": ctx.run_info.get("claude_version_output")})
            code = EXIT_REFUSED
            try:
                code = self._run()
            except Refusal as exc:
                code = exc.code
                raise
            finally:
                ctx.journal.append({"type": "event", "event": "stop", "lane": self.lane,
                                    "at": now(), "exit": code})
            return code

    def _run(self) -> int:
        ctx = self.ctx
        for cell in self.pending_main(ctx.journal.read()):
            code = self.one(cell)
            if code == -1:
                return EXIT_DONE
            if code is not None:
                return code
        retry = ctx.reg.get("retry") or {}
        for number in range(1, int(retry.get("passes", 2)) + 1):
            queue = self.pending_retry(ctx.journal.read())
            if not queue:
                break
            spacing = float(retry.get("spacing_seconds", 1800))
            ctx.journal.append({"type": "event", "event": "retry_pass", "lane": self.lane,
                                "pass": number, "cells": [c.id for c in queue], "at": now(),
                                "spacing_seconds": spacing})
            ctx.say(f"retry pass {number}: {len(queue)} cell(s), after {spacing:g}s")
            ctx.sleep(spacing)
            self.warmed.clear()
            self.streak = 0
            for cell in queue:
                code = self.one(cell)
                if code == -1:
                    return EXIT_DONE
                if code is not None:
                    return code
        code = self.settle()
        if code is not None:
            return code
        done = ends(ctx.journal.read())
        cells = plan(ctx.reg, self.lane)
        excluded = [c.id for c in cells
                    if latest_state(done.get(c.id, [])) in RETRYABLE_STATES]
        # What the lane finished with, said as it is. A completed run
        # carrying unruled calls is scored, and counted here so nobody reads
        # "complete" as "nothing held apart".
        finals = {}
        for c in cells:
            state = latest_state(done.get(c.id, []))
            finals[state] = finals.get(state, 0) + 1
        held = sum(1 for c in cells if (done.get(c.id) or [{}])[-1].get("unruled_calls"))
        summary = ", ".join(f"{k} {v}" for k, v in sorted(finals.items(), key=str)) + (
            f"; {held} ok cell(s) carry unruled calls, counted beside their figures"
            if held else "")
        if excluded:
            ctx.say(f"DONE with {len(excluded)} cell(s) still excluded after every retry "
                    f"pass: {excluded[:8]} ({summary})")
            return EXIT_EXCLUDED_LEFT
        ctx.say(f"DONE: lane {self.lane} complete ({summary})")
        return EXIT_DONE


# --- the 27B thinking pilot ------------------------------------------------------------------

def utilisation(report: dict, roles=("verify", "decompose")) -> list[dict]:
    """Per call: completion_tokens / max_tokens where a ceiling was sent; a cut is 1.0+."""
    prov = report.get("provenance") or {}
    out = []
    for r in list(prov.get("ledger") or []) + list(prov.get("discarded_calls") or []):
        if r.get("role") not in roles:
            continue
        ceiling = r.get("max_tokens")
        used = r.get("completion_tokens")
        cut = r.get("outcome") == "ceiling" or r.get("kind") == "blank_length"
        share = (used / ceiling if isinstance(used, int) and isinstance(ceiling, int)
                 and ceiling > 0 else None)
        out.append({"role": r.get("role"), "max_tokens": ceiling, "completion_tokens": used,
                    "share": None if share is None else round(share, 4), "cut": cut,
                    "flag": cut or (share is not None and share > THINKING_PILOT_FLAG)})
    return out


def merge_need(ctx: Context, row: dict, set_id: str, item: str) -> int | None:
    """The tokens the tool's own preflight will ask the stated window to hold for this merge.

    `merge.merge_documents`' own arithmetic, from the clone's code, with no call:
    the rendered prompt plus the output ceiling this row's profile sends
    (`merge.request_tokens`), which `window.guard` compares with `--window`
    before anything is sent. None for a set that is not a merge. It reproduces
    the measured figures: `index_429` 38,687 and `rate_limits` 55,667 at `high`,
    `mahjongg` 139,173 at `open`.
    """
    spec = ctx.reg["sets"][set_id]
    if spec["kind"] != "merge":
        return None
    from llossless import merge as merging, segment, structured  # noqa: PLC0415
    documents = {p.name: p.read_text(encoding="utf-8")
                 for p in input_files(ctx.clone, ctx.reg, set_id, item)}
    policy = merging.MergePolicy(fidelity=spec["fidelity"],
                                 title_policy=ctx.settings["title_policy"])
    prompt, rules, example, title = merging.compose_prompt(policy)
    base = ctx.settings["base"]
    rendered = prompt.render(fidelity_rules=rules, fidelity_example=example, title_rule=title,
                             base_filename=base, sources=segment.render_sources(
                                 segment.segment_sources(documents), base))
    profile = row["route"].get("profile", "subscription")
    frontier = structured.profile_for(profile).output_ceiling == structured.CEILING_MODEL
    budget = None if frontier else merging.budget_tokens(documents, policy.fidelity)
    return merging.request_tokens(rendered, budget or 0)


def fit(ctx: Context, row_id: str) -> int:
    """Each merge item of a row against its stated window, by the tool's own preflight."""
    row = ctx.row(row_id)
    ctx.say(f"{row_id}: stated window {row['window']} tokens")
    for set_id in row["sets"]:
        for item in items_of(ctx.reg, row, set_id):
            need = merge_need(ctx, row, set_id, item)
            if need is None:
                continue
            ctx.say(f"  {set_id}:{item:<18}{need:>8} {'fits' if need <= row['window'] else 'DOES NOT FIT'}")
    return EXIT_DONE


def thinking_pilot(ctx: Context, row_id: str, items: list[str]) -> int:
    """2-3 small cells, thinking on and off, for the self-hosted route. Never counted.

    Every item must fit the row's registered window by the tool's own
    preflight (`merge_need`), or the pilot is refused before any call: an item
    the tool refuses before sending measures nothing about thinking.
    """
    row = ctx.row(row_id)
    if route_kind(row) != "http":
        raise Refusal("the thinking pilot is for an HTTP route whose thinking is a "
                      "deployment choice (the self-hosted 27B)")
    journal = Journal(ctx.run_dir / "thinking-pilot" / "cells.jsonl", redact=ctx.redactor.obj)
    table = []
    lane = row["lane"]
    too_big = []
    for spec in items:
        set_id, _, item = spec.partition(":")
        if set_id not in ctx.reg["sets"] or item not in ctx.reg["sets"][set_id]["items"]:
            raise Refusal(f"--items: {spec!r} is not SET:item of a registered set")
        need = merge_need(ctx, row, set_id, item)
        if need is not None and need > row["window"]:
            too_big.append(f"{spec} needs {need} tokens")
    if too_big:
        raise Refusal(f"--items: over {row_id}'s stated window of {row['window']} tokens by "
                      f"the tool's own preflight: {'; '.join(too_big)}. Choose items that fit "
                      f"(`fit --row {row_id}`)")
    if ctx.reg["lanes"][lane].get("prewarm") and not prewarm(ctx, row, lane, "thinking pilot"):
        ctx.say("STOP: pre-warm never came up")
        return EXIT_BREAKER
    for spec in items:
        set_id, _, item = spec.partition(":")
        for mode, thinking in (("on", list(ROLES)), ("off", [])):
            cell = Cell(f"{row_id}~thinking-{mode}", set_id, item, 1)
            ctx.rows[cell.row] = row
            attempt = len(ends(journal.read()).get(cell.id, [])) + 1
            end = run_cell(ctx, cell, attempt, lane, journal=journal, thinking=thinking,
                           kind="thinking-pilot")
            report_path = journal.path.parent / end["dir"] / "report.json"
            calls = utilisation(json.loads(report_path.read_text(encoding="utf-8"))) \
                if report_path.is_file() else []
            shares = [c["share"] for c in calls if c["share"] is not None]
            table.append({"item": spec, "thinking": mode, "state": end["state"],
                          "exit_code": end["exit_code"],
                          "answering_seconds": end.get("answering_seconds"),
                          "calls": len(calls), "cut": sum(1 for c in calls if c["cut"]),
                          "max_share": max(shares) if shares else None,
                          "median_share": statistics.median(shares) if shares else None,
                          "flagged": [c for c in calls if c["flag"]]})
            if end["state"] == "halted":
                ctx.say(f"STOP: {cell.id} halted: {'; '.join(end['reasons'])[:600]}")
                return EXIT_REFUSED
    out = journal.path.parent / "utilisation.json"
    out.write_text(json.dumps(table, indent=1) + "\n", encoding="utf-8")
    ctx.out(f"\n{'item':<22}{'thinking':>9}{'state':>15}{'calls':>7}{'cut':>5}"
            f"{'max used':>10}{'median':>9}  flag (>{THINKING_PILOT_FLAG:.0%} of a ceiling)")
    for line in table:
        top = "-" if line["max_share"] is None else f"{line['max_share']:.2f}"
        mid = "-" if line["median_share"] is None else f"{line['median_share']:.2f}"
        ctx.out(f"{line['item']:<22}{line['thinking']:>9}{line['state']:>15}"
                f"{line['calls']:>7}{line['cut']:>5}{top:>10}{mid:>9}  "
                f"{'FLAG ' + str(len(line['flagged'])) if line['flagged'] else '-'}")
    ctx.out(f"-> {out}")
    return EXIT_DONE


# --- the registration template ---------------------------------------------------------------

PAIRS = ("badge_access", "bike_docks", "freezer_alarm", "index_429", "library_holds",
         "loading_dock", "payroll_cutoff", "rate_limits", "trace_names")
SPREAD = ("badge_access", "trace_names", "rate_limits")
DETECT_BLOCK = ("attribution_invented", "attribution_swapped", "conflict_surfaced",
                "contradiction", "dedup", "disjoint_domains", "disjoint_sources",
                "dropped_claim", "hallucination", "numeric_drift", "ordering_only",
                "paraphrase", "structure_added")
DETECT_GUARDS = ("concatenated", "restated", "list_structure")


def template(pin: str = "<FILL: the 40-character pin>", clone: str = "tree", *,
             pilot: bool = False) -> dict:
    """The registered lineup as a registration block, placeholders marked `<FILL: ...>`.

    `pilot` is the pilot set: per row, `badge_access` at high, the
    `dedup` fixture, and one draw of `bip39` at open. Its cells are never
    counted: it is its own run directory with its own registration.
    """
    every = list(ROLES)
    medium = {role: "medium" for role in ROLES}

    # Each row names a reference route on another vendor,
    # asked once when a cell still fails after every retry pass. Anthropic's rows
    # (API and subscription alike: the CLI reaches Anthropic's API) and every
    # other row name OpenAI's cheapest priced model; OpenAI's rows name
    # Anthropic's.
    def api(rid, model, vendor, base, key, profile, estimate, documented, **extra):
        return {"id": rid, "model": model, "lane": "api", "vendor": vendor,
                "hosting": "vendor",
                "route": {"kind": "http", "base_url": base, "key_env": key,
                          "profile": profile},
                "effort": "vendor_default", "effort_documented": documented,
                "thinking": every, "window": 200000, "field_order": "schema",
                "sets": ["S1", "S2", "S3"], "cell_estimate_usd": estimate,
                "reference": "haiku-ref" if vendor == "openai" else "luna-ref", **extra}

    def sub(rid, model, **extra):
        return {"id": rid, "model": model, "lane": "subscription", "vendor": "subscription",
                "hosting": "vendor", "metered": False,
                "route": {"kind": "claude", "profile": "subscription"},
                "effort": dict(medium), "thinking": every, "window": 200000,
                "field_order": "schema", "sets": ["S1", "S2", "S3"],
                "reference": "luna-ref", **extra}

    anthropic = "https://api.anthropic.com/v1"
    openai = "https://api.openai.com/v1"
    google = "https://generativelanguage.googleapis.com/v1beta/openai"
    rows = [
        api("opus-5.5-api", "claude-opus-5-5", "anthropic", anthropic, "ANTHROPIC_API_KEY",
            "anthropic", 1.5, "medium (vendor page, read 2026-09-25)"),
        api("sonnet-5-api", "claude-sonnet-5", "anthropic", anthropic, "ANTHROPIC_API_KEY",
            "anthropic", 1.0, "<FILL: Sonnet 5's documented default, URL and date>"),
        # By ruling, Haiku has one effort level (extended thinking on or
        # off); the default is kept and the row says so, on both routes.
        api("haiku-4.5-api", "claude-haiku-4-5-20251001", "anthropic", anthropic,
            "ANTHROPIC_API_KEY", "anthropic", 0.3, SINGLE_LEVEL_LABEL,
            effort=SINGLE_LEVEL),
        api("gpt-6-sol-api", "gpt-6-sol", "openai", openai, "OPEN_AI_API_KEY",
            "openai-reasoning", 0.8, "medium (model page, read 2026-09-25)"),
        api("gpt-6-luna-api", "gpt-6-luna", "openai", openai, "OPEN_AI_API_KEY",
            "openai-reasoning", 0.1, "medium (model page, read 2026-09-25)"),
        sub("opus-5.5-sub", "claude-opus-5-5"),
        sub("sonnet-5-sub", "claude-sonnet-5"),
        sub("haiku-4.5-sub", "claude-haiku-4-5-20251001", effort=SINGLE_LEVEL,
            effort_note=f"{SINGLE_LEVEL_LABEL}: no --effort is passed"),
        sub("fable-sub", "fable", headline=False, compare_with="opus-5.5-sub",
            unpriced="Fable has no row in pricing.py; subscription only, never metered",
            items={"S1": ["<FILL: the 3-4 hardest documents>"]},
            served_aliases=["<FILL: the id Fable answers as, from its probe>"],
            sets=["S1"]),
        {"id": "gemini-3.5-flash-lite", "model": "gemini-3.5-flash-lite", "lane": "google",
         "vendor": "google", "metered": False, "headline": False, "hosting": "vendor",
         "reference": "luna-ref",
         "route": {"kind": "http", "base_url": google, "key_env": "GOOGLE_AI_API_KEY",
                   "profile": "google"},
         "effort": "vendor_default", "thinking": every, "window": 200000,
         "field_order": "schema", "min_interval": 20, "sets": ["S1", "S2", "S3"],
         "note": "free tier, best effort; paid-tier equivalent priced, never billed"},
        {"id": "gemini-3.8-flash", "model": "gemini-3.8-flash", "lane": "google",
         "vendor": "google", "metered": False, "headline": False, "hosting": "vendor",
         "reference": "luna-ref",
         "route": {"kind": "http", "base_url": google, "key_env": "GOOGLE_AI_API_KEY",
                   "profile": "google"},
         "effort": "vendor_default", "thinking": every, "window": 200000,
         "field_order": "schema", "min_interval": 20, "sets": ["S1", "S2", "S3"],
         "note": "free tier, best effort; 20 requests a day, expected not to complete"},
    ]
    return {
        "registration": 1,
        "name": "fair lineup snapshot",
        "pin": pin,
        "clone": clone,
        "settings": {"timeout": 1800, "structured": "prompt", "title_policy": "synthesise",
                     "verify_depth": "full", "base": "source_a.md", "max_calls": 400,
                     "cell_wall_seconds": 14400},
        "sets": {
            "S1": {"kind": "merge", "score": "pairs", "root": "tests/pairs", "fidelity": "high",
                   "items": list(PAIRS),
                   "draws": {"default": 1, **{p: 3 for p in SPREAD}}},
            "S2": {"kind": "detect", "score": "detect", "root": "tests/fixtures",
                   "items": list(DETECT_BLOCK + DETECT_GUARDS), "draws": {"default": 1},
                   "headline_items": list(DETECT_BLOCK)},
            "S3": {"kind": "merge", "score": "planted", "root": "tests/handwritten",
                   "fidelity": "open", "items": ["voyager", "bip39", "mahjongg"],
                   "draws": {"default": 1, "voyager": 3, "bip39": 3}},
        },
        "caps": {"anthropic": "<FILL: dollars>", "openai": "<FILL: dollars>",
                 "overall": "<FILL: dollars>"},
        "margin": 1.25,
        "retry": {"passes": 2, "spacing_seconds": 1800, "breaker": 3},
        # The headline rule the operator fixed, written out so the block
        # states what it ran under.
        "rules": dict(RULE_DEFAULTS),
        # The reference routes and the one cheap cell each
        # runs. Metered, capped and asserted like any row; never scored.
        "reference_item": "S1:badge_access",
        "references": [
            {"id": "luna-ref", "model": "gpt-6-luna", "vendor": "openai", "hosting": "vendor",
             "route": {"kind": "http", "base_url": openai, "key_env": "OPEN_AI_API_KEY",
                       "profile": "openai-reasoning"},
             "effort": "vendor_default", "thinking": every, "window": 200000,
             "field_order": "schema", "cell_estimate_usd": 0.05},
            {"id": "haiku-ref", "model": "claude-haiku-4-5-20251001", "vendor": "anthropic",
             "hosting": "vendor",
             "route": {"kind": "http", "base_url": anthropic, "key_env": "ANTHROPIC_API_KEY",
                       "profile": "anthropic"},
             "effort": SINGLE_LEVEL, "thinking": every, "window": 200000,
             "field_order": "schema", "cell_estimate_usd": 0.1},
        ],
        # By the outage ruling, an outage pauses the lane; nothing is thrown
        # away. Probed with no token spent (any HTTP status means reachable),
        # every 2 minutes and later every 5, for at most 12 hours per start.
        "infrastructure": {"probe_urls": [anthropic + "/models", openai + "/models"],
                           "probe_intervals_seconds": [120, 120, 120, 300],
                           "max_pause_seconds": 43200},
        "claude": {"path": "<FILL: the pinned copy of the CLI>",
                   "sha256": "<FILL: its sha256>", "version": "<FILL: >= 2.1.280>"},
        "lanes": {"api": {}, "subscription": {}, "google": {}},
        "rows": rows,
        **({"env_file": "<FILL: the .env holding the API keys, or delete this line>"}),
    } if not pilot else _pilot(pin, clone, rows)


def _pilot(pin: str, clone: str, rows: list[dict]) -> dict:
    reg = template(pin, clone)
    reg["name"] = "fair lineup pilot (never counted)"
    reg["sets"]["S1"].update(items=["badge_access"], draws={"default": 1})
    reg["sets"]["S2"].update(items=["dedup"], draws={"default": 1},
                             headline_items=["dedup"])
    reg["sets"]["S3"].update(items=["bip39"], draws={"default": 1})
    for row in reg["rows"]:
        row.pop("draws", None)
        if row["id"] == "fable-sub":
            row["items"] = {"S1": ["badge_access"]}
    return reg


def effort_label(row: dict) -> str:
    """How a row's effort reads in the registration, the figures and the report."""
    effort = row.get("effort")
    if effort == SINGLE_LEVEL:
        return SINGLE_LEVEL_LABEL
    if effort == "vendor_default":
        return "vendor default"
    if isinstance(effort, dict):
        levels = sorted(set(effort.values()))
        return (f"{levels[0]} on every role (CLI)" if len(levels) == 1
                else ", ".join(f"{role} {effort[role]}" for role in sorted(effort)) + " (CLI)")
    return str(effort)


def render_registration(reg: dict) -> str:
    """REGISTRATION.md: the registration skeleton, with the machine block the runner reads."""
    arms = "\n".join(
        f"                 - {r['id']}: {r['model']} via {r['route']['kind']}"
        f" ({r['route'].get('profile', 'subscription')}), effort "
        f"{effort_label(r)}, "
        f"thinking {r['thinking']}, window {r['window']}, sets {r['sets']}"
        f"{'' if r.get('headline', True) else ', not in the headline'}"
        for r in reg["rows"])
    s = reg["settings"]
    return f"""### Lineup snapshot, registered <FILL: date>

```
Question:        On identical documents and settings, what does each model in
                 the frozen lineup do in a faithful merge, what does it detect,
                 which planted errors does it fix, and what does a merge cost?
Arms:
{arms}
Control:         none is privileged; every arm runs in this window, pair-major.
Held constant:   tool pin {reg['pin']}; input sha256 list (run.json, written at the
                 first start); --base {s['base']}; --title-policy {s['title_policy']};
                 --verify-depth {s['verify_depth']}; tier {s['structured']} pinned;
                 --timeout {s['timeout']}; --no-cache; safe mode on every claude call;
                 CLI {reg.get('claude', {}).get('version')} sha256 {reg.get('claude', {}).get('sha256')}
Not held:        1. route; 2. verify batch 25/100; 3. sampling (OpenAI draws share
                 seed 0, best-effort determinism; other vendors sample
                 independently); 4. stated window; 5. field order (27B any);
                 6. effort level per vendor; 7. route overhead in seconds;
                 8. mahjongg is German.
Exclusions:      blank, timeout and platform failures excluded and retried
                 in later passes; retries not counted in speed or cost; a retry
                 reuses the cell's own earlier live answers, each counted once at
                 its original time and cost. Still failing after every
                 pass: one cheap cell ({reg.get('reference_item')}) on the row's
                 reference route; it works, so the cell is the row's
                 endpoint_failure; it fails too, so the lane pauses and probes
                 (infrastructure, never scored) and runs the cell again.
                 A refusal (flagged "refused (prompt or guardrail)") and an
                 unruled cell (a model failure on a vendor row; limit or config
                 on a self-hosted row) count against the row; rules {json.dumps({**RULE_DEFAULTS, **(reg.get('rules') or {})})}.
Common pairs:    every registered pair; nothing shrinks it. A row missing a
                 pair, for its own reason or not measured, is listed after every
                 complete row with why
Baselines:       byte-concatenation, a mechanical union and base-only, on the
                 common pairs, by the same scorer
Budget:          caps {json.dumps(reg.get('caps'))}; subscription meter at start <FILL>
May be used for: dated statements about these pairs at list price; not for a ranking where ranges overlap, other documents or a composite score
Pilot:           <FILL: path to the pilot report>
```

Amendments go below the machine block, dated, each before the calls it governs.

{REGISTRATION_FENCE}
{json.dumps(reg, indent=1)}
```
"""


# --- commands ---------------------------------------------------------------------------------

def status(ctx: Context) -> int:
    records = ctx.journal.read()
    done = ends(records)
    counts: dict[str, dict[str, int]] = {}
    for cell in plan(ctx.reg):
        lane = ctx.row(cell.row)["lane"]
        state = latest_state(done.get(cell.id, [])) or "pending"
        counts.setdefault(lane, {}).setdefault(state, 0)
        counts[lane][state] += 1
    for lane, by in sorted(counts.items()):
        ctx.say(f"{lane:<14}" + "  ".join(f"{k} {v}" for k, v in sorted(by.items())))
    money = spent(records)
    caps = ctx.reg.get("caps") or {}
    for pot, value in sorted(money.items()):
        cap = caps.get(pot)
        ctx.say(f"spent {pot:<14}${value:.4f}" + (f" of ${cap:.2f}" if cap is not None else ""))
    for lane, spec in sorted((ctx.reg.get("lanes") or {}).items()):
        if (spec or {}).get("gpu_seconds") is not None:
            ctx.say(f"GPU   {lane:<14}{gpu_used(records, lane):.0f}s of "
                    f"{spec['gpu_seconds']:.0f}s")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    tpl = sub.add_parser("template", help="write a REGISTRATION.md skeleton")
    tpl.add_argument("--pin", default="<FILL: the 40-character pin>")
    tpl.add_argument("--out", type=Path, required=True)
    tpl.add_argument("--pilot", action="store_true",
                     help="the pilot sets instead of the core test set")
    for name in ("check", "plan", "run", "status", "note", "thinking-pilot", "amend", "fit"):
        p = sub.add_parser(name)
        p.add_argument("--registration", type=Path, required=True)
        if name in ("check", "plan", "run", "note"):
            p.add_argument("--lane", required=name in ("run", "note"))
        if name == "run":
            p.add_argument("--max-cells", type=int)
        if name == "note":
            p.add_argument("text")
        if name in ("thinking-pilot", "fit"):
            p.add_argument("--row", required=True)
        if name == "thinking-pilot":
            p.add_argument("--items", required=True,
                           help="comma-separated SET:item, e.g. S1:rate_limits,S3:bip39; each must fit")
        if name == "amend":
            p.add_argument("--reason", required=True)
    args = parser.parse_args(argv)
    if args.command == "template":
        args.out.write_text(render_registration(template(pin=args.pin, pilot=args.pilot)),
                            encoding="utf-8")
        print(f"wrote {args.out}; fill every <FILL: ...> before `check`")
        return 0
    try:
        ctx = load_context(args.registration)
        if args.command == "plan":
            done = ends(ctx.journal.read())
            for cell in plan(ctx.reg, args.lane):
                attempts = done.get(cell.id, [])
                print(f"{cell.id:<60}{latest_state(attempts) or 'pending':>14}"
                      f"{len(attempts):>4}")
            return 0
        if args.command == "status":
            return status(ctx)
        if args.command == "fit":
            return fit(ctx, args.row)
        if args.command == "note":
            ctx.journal.append({"type": "event", "event": "note", "lane": args.lane,
                                "at": now(), "text": args.text})
            return 0
        if args.command == "amend":
            path = ctx.run_dir / "run.json"
            info = json.loads(path.read_text(encoding="utf-8"))
            info.setdefault("amendments", []).append(
                {"at": now(), "new": ctx.block_sha256, "reason": args.reason})
            path.write_text(json.dumps(info, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            ctx.journal.append({"type": "event", "event": "amendment", "at": now(),
                                "block_sha256": ctx.block_sha256, "reason": args.reason})
            print(f"recorded amendment {ctx.block_sha256[:12]}")
            return 0
        lane = getattr(args, "lane", None)
        if args.command == "thinking-pilot":
            lane = ctx.row(args.row)["lane"]
        problems = preflight(ctx, lane)
        if problems:
            raise Refusal("preflight refused:\n  - " + "\n  - ".join(problems))
        ctx.run_info = {**first_start(ctx), **ctx.run_info}
        if any(r["route"]["kind"] == "claude" for r in ctx.reg["rows"]
               if lane is None or r["lane"] == lane):
            write_wrapper(ctx.run_dir, claude_binary(ctx))
        if args.command == "check":
            cells = plan(ctx.reg, lane)
            print(f"preflight clean: pin {ctx.reg['pin'][:12]}, {len(cells)} cell(s)"
                  + (f" on lane {lane}" if lane else ""))
            return 0
        if args.command == "thinking-pilot":
            return thinking_pilot(ctx, args.row, args.items.split(","))
        return LaneRun(ctx, args.lane, max_cells=args.max_cells).run()
    except Refusal as exc:
        print(f"REFUSED: {exc.message}", file=sys.stderr)
        return exc.code


if __name__ == "__main__":
    sys.exit(main())
