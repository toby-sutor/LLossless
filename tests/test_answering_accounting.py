#!/usr/bin/env python3
"""Offline checks for the answering-attempt accounting.

The rules have to be measurable from a report: a blank, a timeout or a
platform failure is excluded from quality, cost and speed; retries are not
counted in speed or cost; a cell's cost and time are those of the attempt that
produced its answer. A schema repair is the model failing the format, so it
stays in the answering cost. Each check here has a must-fire seed and a
must-not-fire case:

- 429, 429, 200: three attempts, the waits in `waited_ms`, and `answer_ms`
  covering the last attempt alone;
- a blank then an answer: one ledger row, one discarded row, and
  `answering_cost` without the blank;
- a schema repair stays in the answering cost;
- `--min-interval` pacing lands in `waited_ms`;
- a command route's own `duration_ms`/`duration_api_ms` are recorded;
- a call the platform lost, a refusal blank and a ceiling cut each land in
  the right bucket, and a replay files the same outcomes its live run did.

Real transport against a loopback `FakeEndpoint`, and a fake program for the
command route: no model, vendor, subscription or serverless call.

Run with `python3 tests/test_answering_accounting.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import stat
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# tests/test_socket_guard.py asserts every test module does this.
socket_guard.install()

from llossless import backend, config, parsing, pricing, prompts, provenance, transport, window  # noqa: E402
from llossless.client import Client, SchemaFailure  # noqa: E402
from llossless.decompose import CLAIM_SCHEMA  # noqa: E402
from fake_endpoint import FakeEndpoint  # noqa: E402

failures: list[str] = []
checks = 0

# Priced in `pricing.py`, so a cost figure is a number and not `unpriced`.
MODEL = "claude-opus-5-5"
DOCUMENT = "The relay listens on port 8443."
GOOD = json.dumps({"claims": [{"text": DOCUMENT, "line": 1, "span": "port 8443"}]})


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def raises(exception, call, message: str):
    global checks
    checks += 1
    try:
        call()
    except exception as exc:
        return exc
    except Exception as exc:  # noqa: BLE001 - the wrong exception is still a failure to report
        failures.append(f"{message}: raised {type(exc).__name__} not {exception.__name__}: {exc}")
        return None
    failures.append(f"{message}: nothing raised")
    return None


def body(content, *, finish: str = "stop", prompt: int = 1000, completion: int = 100) -> str:
    return json.dumps({
        "id": "chatcmpl-test", "object": "chat.completion", "model": MODEL,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content},
                     "finish_reason": finish}],
        "usage": {"prompt_tokens": prompt, "completion_tokens": completion},
    })


def price(prompt: int, completion: int) -> float:
    return pricing.cost(pricing.sku_for(MODEL), input_tokens=prompt, output_tokens=completion)


def settings(base_url: str, tmp: str, **kwargs) -> config.Settings:
    kwargs.setdefault("models", {"decompose": MODEL, "verify": MODEL})
    return config.Settings(base_url=base_url, cache_dir=Path(tmp) / "c", use_cache=False,
                           structured="prompt", pinned=True, **kwargs)


def ask(client: Client, **kwargs):
    return client.complete(role="decompose", prompt=prompts.load("decompose"),
                           messages=[{"role": "user", "content": DOCUMENT}],
                           schema=CLAIM_SCHEMA, schema_name="emit_claims",
                           semantic=parsing.check_claims, **kwargs)


def report(client: Client) -> dict:
    return provenance.Provenance(settings=client.settings, client=client,
                                 roles=("decompose",), duration_seconds=0.0).as_dict()


def close(a, b, tolerance: float = 1e-12) -> bool:
    return a is not None and b is not None and abs(a - b) <= tolerance


# ---------------------------------------------------------------------------
# 1. Retries: 429, 429, 200.
# ---------------------------------------------------------------------------

def test_429_429_200_is_three_attempts_and_times_the_last_alone() -> None:
    """MUST FIRE: the two 429s' waits land in `waited_ms`, and `answer_ms` is the
    last attempt's own time, which `latency_ms`, the older figure, is not.
    MUST NOT FIRE: one clean 200 is one attempt, nothing waited, nothing failed,
    and its answering time is its whole latency."""
    def responder(_body, n):
        if n <= 2:
            return 429, '{"error": "rate limited"}', {"Retry-After": "0.2"}
        time.sleep(0.15)
        return 200, body(GOOD)

    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(responder, prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        ask(client)
        row = client.usage.ledger[-1]
        data = report(client)
    check(row.get("attempts") == 3, f"429, 429, 200 is three attempts: {row.get('attempts')}")
    check(row.get("waited_ms", 0) >= 380,
          f"two Retry-After waits of 0.2 s must be in waited_ms: {row.get('waited_ms')}")
    check(150 <= row.get("answer_ms", 0) < 350,
          f"answer_ms is the last attempt alone (~150 ms), not the waits: {row.get('answer_ms')}")
    check(row.get("latency_ms", 0) >= 530,
          f"the seed: latency_ms still spans every attempt and wait: {row.get('latency_ms')}")
    split = row.get("failed_ms", 0) + row.get("waited_ms", 0) + row.get("answer_ms", 0)
    check(abs(row.get("latency_ms", 0) - split) <= 15,
          f"latency_ms must be failed + waited + answer: {row.get('latency_ms')} vs {split}")
    check(isinstance(row.get("ttfb_ms"), int) and row["ttfb_ms"] <= row.get("answer_ms", 0),
          f"ttfb_ms is inside the answering attempt: {row.get('ttfb_ms')}")
    check(data["excluded"]["calls"].get("retries") == 2,
          f"two transport retries are excluded: {data['excluded']['calls']}")
    check(data["excluded"]["seconds"]["waited"] >= 0.38,
          f"the waits are excluded seconds: {data['excluded']['seconds']}")
    check(data["answering_seconds"]["total"] == round(row["answer_ms"] / 1000, 3),
          f"answering seconds are answer_ms alone: {data['answering_seconds']}")
    check(data["answering_seconds"]["by_role"] == {"decompose": round(row["answer_ms"] / 1000, 3)},
          f"per role too: {data['answering_seconds']}")

    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(lambda _b, _n: (200, body(GOOD)), prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        ask(client)
        row = client.usage.ledger[-1]
        data = report(client)
    check(row.get("attempts") == 1 and row.get("waited_ms") == 0 and row.get("failed_ms") == 0,
          f"MUST NOT FIRE: a clean 200 is one attempt with nothing waited or failed: {row}")
    check(abs(row.get("answer_ms", -99) - row.get("latency_ms", 0)) <= 2,
          f"MUST NOT FIRE: one attempt's answering time is its latency: {row}")
    check(data["excluded"]["calls"] == {"retries": 0}
          and data["excluded"]["seconds"]["total"] == 0.0,
          f"MUST NOT FIRE: nothing excluded on a clean call: {data['excluded']}")


def test_a_call_the_platform_lost_is_a_discarded_excluded_row() -> None:
    """MUST FIRE: 503 on all three attempts raises, and the call is filed under
    `discarded_calls` as `platform`, with its attempts and waits, excluded and
    unmeasured (a 5xx reports no tokens). MUST NOT FIRE: a fatal 401 is one
    attempt with no retries counted."""
    responder = lambda _b, _n: (503, '{"error": "overloaded"}', {"Retry-After": "0.05"})  # noqa: E731
    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(responder, prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        raises(transport.HTTPStatusError, lambda: ask(client), "three 503s must raise")
        data = report(client)
    rows = data["discarded_calls"]
    check(len(rows) == 1 and rows[0].get("kind") == "platform"
          and rows[0].get("counted_as") == "excluded",
          f"the lost call is one excluded platform row: {rows}")
    if rows:
        check(rows[0].get("attempts") == 3 and rows[0].get("waited_ms", 0) >= 90
              and "answer_ms" not in rows[0] and "prompt_tokens" not in rows[0],
              f"three attempts, two waits, no answer, no tokens: {rows[0]}")
        check(isinstance(rows[0].get("latency_ms"), int)
              and rows[0]["latency_ms"] >= rows[0].get("waited_ms", 0),
              f"a discarded row carries latency_ms, the waits inside it: {rows[0]}")
    check(data["ledger"] == [], f"nothing answered, so nothing in the ledger: {data['ledger']}")
    check(data["excluded"]["calls"] == {"retries": 2, "platform": 1},
          f"two retries and one lost call: {data['excluded']['calls']}")
    check(data["excluded"]["cost"]["state"] == "unmeasured",
          f"a call nothing reported tokens for is unmeasured, never $0.00: {data['excluded']['cost']}")
    check(data["counts"]["calls"] == len(data["ledger"]) + len(rows),
          f"every counted call is a ledger row or a discarded one: {data['counts']['calls']}")

    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(lambda _b, _n: (401, '{"error": "no"}'), prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        raises(transport.HTTPStatusError, lambda: ask(client), "a 401 must raise")
        data = report(client)
    rows = data["discarded_calls"]
    check(len(rows) == 1 and rows[0].get("attempts") == 1
          and data["excluded"]["calls"].get("retries") == 0,
          f"MUST NOT FIRE: a fatal status is one attempt and no retry: {rows}")


# ---------------------------------------------------------------------------
# 2. A blank, then an answer.
# ---------------------------------------------------------------------------

def test_a_blank_then_an_answer_is_one_ledger_row_and_one_discard() -> None:
    """MUST FIRE: the blank is re-asked; it is a discarded row with the tokens
    its vendor reported and its own price, and `answering_cost` is the answer's
    price alone. `cost`, the ledger's, keeps its meaning. MUST NOT FIRE: a
    clean call discards nothing and excludes no cost."""
    def responder(_body, n):
        if n == 1:
            return 200, body("", prompt=5000, completion=900)
        return 200, body(GOOD, prompt=1000, completion=100)

    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(responder, prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        ask(client)
        data = report(client)
    answer, blank = price(1000, 100), price(5000, 900)
    check(len(data["ledger"]) == 1 and data["ledger"][0].get("outcome") == "answer",
          f"one ledger row, the answer: {data['ledger']}")
    rows = data["discarded_calls"]
    check(len(rows) == 1, f"one discarded row, the blank: {rows}")
    if rows:
        row = rows[0]
        check(row.get("kind") == "blank" and row.get("counted_as") == "excluded"
              and row.get("finish_reason") == "stop",
              f"a blank with no named reason is excluded: {row}")
        check(row.get("prompt_tokens") == 5000 and row.get("completion_tokens") == 900,
              f"the blank carries the tokens its vendor reported: {row}")
        check(close(row.get("usd_exact"), blank), f"and its own price: {row.get('usd_exact')} vs {blank}")
        check(row.get("attempts") == 1 and isinstance(row.get("answer_ms"), int),
              f"and its time: {row}")
    check(close(data["answering_cost"]["usd_exact"], answer)
          and data["answering_cost"]["state"] == "priced",
          f"answering_cost is the answer alone: {data['answering_cost']} vs {answer}")
    check(close(data["excluded"]["cost"]["usd_exact"], blank),
          f"excluded cost is the blank: {data['excluded']['cost']} vs {blank}")
    check(close(data["cost"]["usd_exact"], answer),
          f"`cost` is still the ledger's, which never held the blank: {data['cost']}")
    check(data["excluded"]["calls"].get("blank") == 1, f"one blank excluded: {data['excluded']}")
    check("unruled" not in data, "a plain blank is ruled on: no unruled block")
    check(data["counts"]["calls"] == 2 == len(data["ledger"]) + len(rows),
          f"two calls: one row each side: {data['counts']['calls']}")
    check(data["tokens"].get("input") == 1000,
          f"the run's token totals keep their meaning, the blank's are not in them: {data['tokens']}")

    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(lambda _b, _n: (200, body(GOOD)), prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        ask(client)
        data = report(client)
    check(data["discarded_calls"] == [] and data["excluded"]["cost"]["state"] == "none"
          and "blank" not in data["excluded"]["calls"],
          f"MUST NOT FIRE: a clean call discards and excludes nothing: {data['excluded']}")


def test_an_empty_body_is_a_blank_with_no_tokens() -> None:
    """MUST FIRE: a 200 with zero bytes is `EmptyBody`: discarded as a blank,
    unmeasured, timed from the transport's own stamp."""
    def responder(_body, n):
        return (200, "") if n == 1 else (200, body(GOOD))

    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(responder, prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        ask(client)
        data = report(client)
    rows = data["discarded_calls"]
    check(len(rows) == 1 and rows[0].get("error") == "EmptyBody"
          and rows[0].get("kind") == "blank" and "prompt_tokens" not in rows[0]
          and rows[0].get("attempts") == 1 and isinstance(rows[0].get("latency_ms"), int),
          f"an empty body is a blank with no tokens, one attempt, timed: {rows}")
    check(data["excluded"]["cost"]["state"] == "unmeasured",
          f"and its cost is unmeasured, never $0.00: {data['excluded']['cost']}")


def test_a_refusal_blank_waits_for_a_ruling() -> None:
    """MUST FIRE: a blank that says `content_filter` is neither excluded nor
    charged: `unruled`, out of both totals. MUST NOT FIRE is the plain blank
    in the test above, which has no `unruled` block."""
    def responder(_body, n):
        if n == 1:
            return 200, body(None, finish="content_filter", prompt=2000, completion=0)
        return 200, body(GOOD, prompt=1000, completion=100)

    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(responder, prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        ask(client)
        data = report(client)
    rows = data["discarded_calls"]
    check(len(rows) == 1 and rows[0].get("kind") == "blank_refusal"
          and rows[0].get("counted_as") == "unruled",
          f"a content_filter blank waits for a ruling: {rows}")
    check(data.get("unruled", {}).get("calls") == {"blank_refusal": 1},
          f"and says so: {data.get('unruled')}")
    check(close(data["answering_cost"]["usd_exact"], price(1000, 100)),
          f"it is not in the answering cost: {data['answering_cost']}")
    check(data["excluded"]["cost"]["state"] == "none",
          f"nor in the excluded cost: {data['excluded']['cost']}")
    held = data.get("unruled", {}).get("cost", {})
    check(close(held.get("usd_exact"), price(2000, 0)),
          f"it is priced where it is held: {held}")


# ---------------------------------------------------------------------------
# 3. A schema repair stays in the answering cost.
# ---------------------------------------------------------------------------

def test_a_schema_repair_is_charged_to_the_model() -> None:
    """MUST FIRE: an answer that fails the format and is repaired is two ledger
    rows, `repair` then `answer`, and both are in `answering_cost` and
    `answering_seconds`. MUST NOT FIRE: nothing is discarded or excluded -- the
    same tokens as a blank would have been, and a repair is not a blank."""
    def responder(_body, n):
        if n == 1:
            return 200, body("this is not json", prompt=1000, completion=300)
        return 200, body(GOOD, prompt=1000, completion=100)

    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(responder, prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        ask(client)
        data = report(client)
    outcomes = [row.get("outcome") for row in data["ledger"]]
    check(outcomes == ["repair", "answer"], f"a repaired attempt, then the answer: {outcomes}")
    both = price(1000, 300) + price(1000, 100)
    check(close(data["answering_cost"]["usd_exact"], both)
          and data["answering_cost"]["priced_calls"] == 2,
          f"the repair stays in the answering cost: {data['answering_cost']} vs {both}")
    timed = sum(row["answer_ms"] for row in data["ledger"]) / 1000
    check(abs(data["answering_seconds"]["total"] - timed) <= 0.002,
          f"and in the answering seconds: {data['answering_seconds']} vs {timed}")
    check(data["discarded_calls"] == [] and data["excluded"]["cost"]["state"] == "none",
          f"MUST NOT FIRE: a repair is not discarded or excluded: {data['excluded']}")


def test_a_unit_that_never_parses_is_charged_as_failed() -> None:
    """MUST FIRE: every attempt at a unit that gives up is the model's, four
    `repair`s and a `failed`. MUST NOT FIRE: none of them is unruled."""
    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(lambda _b, _n: (200, body("still not json")), prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        raises(SchemaFailure, lambda: ask(client), "a unit that never parses fails")
        data = report(client)
    outcomes = [row.get("outcome") for row in data["ledger"]]
    check(outcomes == ["repair"] * 4 + ["failed"], f"four repairs then the failure: {outcomes}")
    check(data["answering_cost"]["priced_calls"] == 5 and "unruled" not in data,
          f"MUST NOT FIRE: all five are the model's: {data['answering_cost']}")


def test_a_ceiling_cut_waits_for_a_ruling() -> None:
    """MUST FIRE: a response cut at its ceiling and refused is a
    ledger row with outcome `ceiling`, held in `unruled` and out of the
    answering cost. MUST NOT FIRE: the same cut without `refuse_at_ceiling`
    goes through the repair ladder and is charged to the model."""
    cut = body('{"claims": [{"text": "The relay', finish="length", completion=64)
    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(lambda _b, _n: (200, cut), prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        raises(window.Truncated, lambda: ask(client, max_tokens=64, refuse_at_ceiling=True),
               "a cut at the ceiling is refused")
        data = report(client)
    check([row.get("outcome") for row in data["ledger"]] == ["ceiling"],
          f"one row, a ceiling cut: {data['ledger']}")
    check(data.get("unruled", {}).get("calls") == {"ceiling": 1},
          f"held for a ruling: {data.get('unruled')}")
    check(data["answering_cost"]["state"] == "none",
          f"and nothing is charged to the model: {data['answering_cost']}")

    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(lambda _b, _n: (200, cut), prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp))
        raises(SchemaFailure, lambda: ask(client, max_tokens=64), "without refusal it repairs")
        data = report(client)
    check("unruled" not in data and data["answering_cost"]["priced_calls"] == 5,
          f"MUST NOT FIRE: the repair path is the model's: {data['answering_cost']}")


# ---------------------------------------------------------------------------
# 4. Pacing goes to `waited_ms`.
# ---------------------------------------------------------------------------

def test_pacing_is_waited_not_answering() -> None:
    """MUST FIRE: the second call waits out `--min-interval`, and that pause is
    its `waited_ms`, never its `answer_ms`. MUST NOT FIRE: the first call has
    nothing to pace against and waited nothing."""
    with tempfile.TemporaryDirectory() as tmp, \
            FakeEndpoint(lambda _b, _n: (200, body(GOOD)), prompt_ratio=None) as base_url:
        client = Client(settings(base_url, tmp, min_interval=0.3))
        ask(client)
        ask(client)
        first, second = client.usage.ledger
        data = report(client)
    check(first.get("waited_ms") == 0, f"MUST NOT FIRE: the first call is not paced: {first}")
    check(second.get("waited_ms", 0) >= 250 and second.get("attempts") == 1
          and second.get("failed_ms") == 0,
          f"the pause is the second call's wait: {second}")
    check(second.get("answer_ms", 999) < 200,
          f"and not its answering time: {second.get('answer_ms')}")
    check(data["excluded"]["seconds"]["waited"] >= 0.25,
          f"pacing is excluded time: {data['excluded']['seconds']}")
    check(data["answering_seconds"]["total"] < 0.25,
          f"answering seconds never carry the pause: {data['answering_seconds']}")


# ---------------------------------------------------------------------------
# 5. The subscription envelope's own durations.
# ---------------------------------------------------------------------------

PROGRAM = """import sys
sys.stdin.read()
sys.stdout.write({DATA})
"""


def program(directory: Path, name: str, printed: str) -> str:
    """A command that reads its prompt and writes `printed`, verbatim."""
    path = directory / name
    path.write_text(PROGRAM.replace("{DATA}", repr(printed)), encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return f"{sys.executable} {path}"


def test_the_command_envelope_durations_are_recorded() -> None:
    """MUST FIRE: a result envelope's `duration_ms` and `duration_api_ms` reach
    the ledger row as `cli_duration_ms`/`cli_duration_api_ms` and the answering
    total as `answering_seconds.cli`. MUST NOT FIRE: a raw route, a missing or
    boolean figure, and stdout that is not JSON record nothing."""
    check(backend.cli_timing(json.dumps({"duration_ms": 1234, "duration_api_ms": 1500}))
          == {"duration_ms": 1234, "duration_api_ms": 1500}, "both figures are read")
    check(backend.cli_timing(json.dumps({"duration_ms": True, "result": "x"})) is None,
          "MUST NOT FIRE: a boolean is not a duration")
    check(backend.cli_timing("not json") is None, "MUST NOT FIRE: not an envelope")

    envelope = {"type": "result", "subtype": "success", "is_error": False,
                "result": GOOD, "num_turns": 1, "duration_ms": 1234,
                "duration_api_ms": 1500}
    with tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        command = program(home, "answer.py", json.dumps(envelope)) + " --output-format json"
        client = Client(config.Settings(command=command, command_envelope="result",
                                        window=200_000, models={"decompose": "opus"},
                                        cache_dir=home / "c", use_cache=False))
        ask(client)
        row = client.usage.ledger[-1]
        data = report(client)

        plain = program(home, "plain.py", GOOD)
        client = Client(config.Settings(command=plain, window=200_000,
                                        models={"decompose": "opus"},
                                        cache_dir=home / "c2", use_cache=False))
        ask(client)
        quiet = client.usage.ledger[-1]
        quiet_data = report(client)
    check(row.get("cli_duration_ms") == 1234 and row.get("cli_duration_api_ms") == 1500,
          f"the envelope's durations are on the row: {row}")
    check(row.get("attempts") == 1 and row.get("answer_ms") == row.get("latency_ms"),
          f"a command is one attempt, answered in its whole latency: {row}")
    cli = data["answering_seconds"].get("cli") or {}
    check(cli.get("duration", {}).get("total") == 1.234
          and cli.get("duration_api", {}).get("total") == 1.5
          and cli.get("duration", {}).get("by_role") == {"decompose": 1.234},
          f"and in the answering total: {data['answering_seconds']}")
    check(not any(name.startswith("cli_") for name in quiet)
          and "cli" not in quiet_data["answering_seconds"],
          f"MUST NOT FIRE: a raw route reports no envelope durations: {quiet}")


# ---------------------------------------------------------------------------
# 6. A replay files the same outcomes, so `answering_cost` replays.
# ---------------------------------------------------------------------------

def test_a_replay_files_the_outcomes_its_live_run_did() -> None:
    """MUST FIRE: a repair recorded live and then replayed carries the same
    `outcome`s and the same `answering_cost`, and no timing field. MUST NOT
    FIRE: the replay's `answering_seconds` is unmeasured, never zero."""
    def responder(_body, n):
        if n == 1:
            return 200, body("this is not json", prompt=1000, completion=300)
        return 200, body(GOOD, prompt=1000, completion=100)

    with tempfile.TemporaryDirectory() as tmp:
        tapes = Path(tmp) / "tapes"
        with FakeEndpoint(responder, prompt_ratio=None) as base_url:
            live = Client(settings(base_url, tmp, record_dir=tapes))
            ask(live)
            live_data = report(live)
        replay = Client(settings("http://127.0.0.1:1/v1", tmp, replay_dir=tapes))
        ask(replay)
        replay_data = report(replay)
    check([row.get("outcome") for row in replay_data["ledger"]]
          == [row.get("outcome") for row in live_data["ledger"]] == ["repair", "answer"],
          f"the replay files the live run's outcomes: {replay_data['ledger']}")
    check(replay_data["answering_cost"] == live_data["answering_cost"],
          f"so the answering cost replays: {replay_data['answering_cost']} "
          f"vs {live_data['answering_cost']}")
    timing = ("attempts", "answer_ms", "failed_ms", "waited_ms", "ttfb_ms")
    check(not any(name in row for row in replay_data["ledger"] for name in timing),
          f"a replay made no call and carries no call's time: {replay_data['ledger']}")
    check(replay_data["answering_seconds"]["total"] is None
          and replay_data["answering_seconds"].get("untimed_calls") == 2,
          f"MUST NOT FIRE: a replay's seconds are unmeasured, not 0: "
          f"{replay_data['answering_seconds']}")
    check(set(provenance.VOLATILE) >= {"answering_seconds", "excluded", "unruled",
                                       "discarded_calls"}
          and "answering_cost" not in provenance.VOLATILE,
          "the stopwatch blocks are volatile; the answering cost is compared")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_answering_accounting" and callable(function):
            function()
    if failures:
        print(f"answering accounting: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"answering accounting: {checks} checks pass")
    return 0


def test_answering_accounting() -> None:
    """pytest entry point."""
    assert main() == 0, "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
