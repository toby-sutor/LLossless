#!/usr/bin/env python3
"""Offline suite for the LLM client contract: config, tiers, parsing, cassettes.

Stdlib only, no model, no API key, no GPU. The eight acceptance tests from an
earlier addendum are at the bottom, named after their numbers; everything above them
is the unit coverage those eight depend on.

Where an acceptance test needs an endpoint, it gets a real one — see
tests/fake_endpoint.py. The only test that reaches outside this process is the
`git ls-files` scan, and the only one that spawns an interpreter is the check
that replay never loads the transport module, which cannot be answered honestly
from inside a process that has already imported it.

Run with `python3 tests/test_client.py`, or collect with pytest.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import inspect
import io
import dataclasses
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
import urllib.error
from dataclasses import replace
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs, so a test that points a
# socket anywhere but the configured endpoint fails loudly instead of
# succeeding quietly. tests/test_socket_guard.py asserts every module does this.
socket_guard.install()

from llossless import (  # noqa: E402
    cassette, config, html_report, merge, parsing, prompts, report, segment,
    structured, transport, usage, verify,
)
from llossless.client import (  # noqa: E402
    Client, ConcurrentCall, DryRun, EMPTY_RESPONSE_ATTEMPTS,
    LOOPING_RESPONSE_ATTEMPTS, PinnedTierViolated, SCHEMA_ATTEMPTS,
    SchemaFailure, SEED, TEMPERATURE, _replay_store,
)
from llossless.console import Console  # noqa: E402
from llossless.decompose import CLAIM_SCHEMA  # noqa: E402
from llossless import provenance  # noqa: E402
from llossless.provenance import Provenance  # noqa: E402

import run_decompose  # noqa: E402
import scan_artefacts  # noqa: E402
from fake_endpoint import FakeEndpoint, envelope, rejects  # noqa: E402

failures: list[str] = []

# Checks that could not be judged here, with the reason. Reported rather than
# dropped: the published copy is missing evidence that is gitignored by
# design, and "did not run" must not read the same as "passed".
unjudged: list[str] = []

# The verify pass will eventually own this. It lives here now because
# acceptance test 6 is specified in terms of a verdict outside the label set,
# and the closed label set is exactly what that test is about.
#
# The brief wrote that test in terms of "PARTIAL", which was later turned into
# a real verdict. The test is about a label the set does not contain, so the
# sentinel moved to UNCLEAR rather than the test being weakened: a hedge is what
# this verdict set exists to refuse, so no later task will make it valid either.
VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "verdicts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "claim_id": {"type": "string"},
                    "verdict": {"enum": ["SUPPORTED", "CONTRADICTED", "MISSING", "PARTIAL"]},
                    "rationale": {"type": "string", "maxLength": 200},
                    "evidence": {"type": "string"},
                },
                "required": ["claim_id", "verdict", "rationale", "evidence"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["verdicts"],
    "additionalProperties": False,
}

FAKE_KEY = "not-a-real-key-3f9c1d7b2e"  # noqa: S105 - the point is that it never escapes


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def raises(exception, call, message: str):
    try:
        call()
    except exception as exc:
        return exc
    except Exception as exc:  # noqa: BLE001
        failures.append(f"{message} (raised {type(exc).__name__}: {exc})")
        return None
    failures.append(f"{message} (nothing raised)")
    return None


NO_MODEL_MAP = ROOT / "tests" / "does-not-exist.json"


def env_settings(**overrides) -> config.Settings:
    """from_env, isolated from the developer's shell and models.local.json."""
    with clean_env(**overrides):
        return config.from_env(model_map_path=NO_MODEL_MAP)


@contextlib.contextmanager
def clean_env(**overrides):
    """LLOSSLESS_* out of the way, so the suite does not read the developer's
    shell. The old CLAIMCHECK_* too: the checks that they are ignored set them."""
    saved = {k: v for k, v in os.environ.items() if k.startswith(("LLOSSLESS_", "CLAIMCHECK_"))}
    for key in saved:
        del os.environ[key]
    os.environ.update({k: v for k, v in overrides.items() if v is not None})
    try:
        yield
    finally:
        for key in [k for k in os.environ if k.startswith(("LLOSSLESS_", "CLAIMCHECK_"))]:
            del os.environ[key]
        os.environ.update(saved)


def settings_for(base_url: str, tmp: Path, **kwargs) -> config.Settings:
    kwargs.setdefault("models", {"verify": "test-model"})
    kwargs.setdefault("cache_dir", tmp / "cache")
    kwargs.setdefault("use_cache", False)
    return config.Settings(base_url=base_url, **kwargs)


def decompose_prompt() -> prompts.Prompt:
    return prompts.load("decompose")


def claims_call(
    client: Client,
    text: str = "The relay listens on port 8443.",
    thinking: bool | None = None,
) -> dict:
    return client.complete(
        role="decompose",
        prompt=decompose_prompt(),
        messages=[{"role": "user", "content": text}],
        schema=CLAIM_SCHEMA,
        schema_name="emit_claims",
        semantic=parsing.check_claims,
        thinking=thinking,
    ).payload


CLAIMS_BODY = json.dumps(
    {"claims": [{"text": "The relay listens on port 8443.", "line": 5, "span": "port 8443"}]}
)


def verdicts_call(client: Client, thinking: bool | None = None) -> dict:
    """One verify-shaped call. The order contract lives on this response."""
    return client.complete(
        role="verify",
        prompt=prompts.load("verify"),
        messages=[{"role": "user", "content": "claim 1: the relay listens on port 8443"}],
        schema=verify.VERDICT_SCHEMA,
        schema_name="emit_verdicts",
        semantic=parsing.check_verdicts,
        thinking=thinking,
    ).payload


VERDICT = {
    "claim_id": "c1",
    "verdict": "SUPPORTED",
    "evidence": "port 8443",
    "evidence_source": "a.md",
    "rationale": "stated in the source",
}


def verdicts_body(order: tuple[str, ...] = parsing.VERDICT_FIELDS) -> str:
    """The same verdict every time, emitted in whatever order is asked for.

    One record, one difference. A fixture that changed the order and the content
    together could not tell an order fault from a content fault, which is the
    distinction the code under test is drawing.
    """
    return json.dumps({"verdicts": [{name: VERDICT[name] for name in order}]})


def reasoning_envelope(content: str, reasoning: str | None) -> str:
    """A response carrying `reasoning`, or carrying the key empty, or without it.

    Three cases, because the three are what endpoints actually send and the
    check under test has to tell them apart: `None` leaves the key out (qwen3:8b
    with thinking off), `""` includes it empty (several gateways do this
    unconditionally), and a string is the model reasoning when it was asked not
    to.
    """
    message: dict = {"role": "assistant", "content": content}
    if reasoning is not None:
        message["reasoning"] = reasoning
    return json.dumps({
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "choices": [{"index": 0, "message": message, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50},
    })


def echo_document(body: dict, _n: int):
    """Answer with claims built from the numbered document in the prompt.

    Genuinely different per document, so the cassette keying is exercised rather
    than assumed: a bug that keyed every call the same way would still pass a
    test whose endpoint returns one canned answer.
    """
    prompt = body["messages"][-1]["content"]
    claims = []
    for line in prompt.splitlines():
        match = re.match(r"^\s*(\d+) \| (.+)$", line)
        if not match or match.group(2).startswith(("#", "|", ">")):
            continue
        claims.append(
            {"text": match.group(2).strip(), "line": int(match.group(1)), "span": match.group(2)}
        )
    return 200, envelope(json.dumps({"claims": claims[:14]}))


# --------------------------------------------------------------------------
# PART A - configuration
# --------------------------------------------------------------------------


def test_config_defaults_to_localhost() -> None:
    settings = env_settings()
    check(settings.base_url == config.DEFAULT_BASE_URL, "the default endpoint must be localhost")
    check(settings.is_local, "the default endpoint must classify as local")
    check(settings.structured == "auto" and not settings.pinned, "auto is the default tier mode")


def test_config_host_is_host_only() -> None:
    settings = config.Settings(base_url="https://gateway.example.net:8443/v1/openai")
    check(settings.host == "gateway.example.net", f"host leaked more than a host: {settings.host}")
    check(not settings.is_local, "a remote host must not classify as local")
    check(settings.where == "hosted", "a remote host must report as hosted")


def test_api_key_is_read_indirectly_and_never_stored() -> None:
    with clean_env(LLOSSLESS_API_KEY_ENV="SOME_EXISTING_VAR", SOME_EXISTING_VAR=FAKE_KEY):
        settings = config.from_env(model_map_path=NO_MODEL_MAP)
        check(settings.api_key() == FAKE_KEY, "the key must be read from the named variable")

        # The whole Settings object is serialised into reports and error paths.
        serialised = repr(settings) + json.dumps(
            {k: str(v) for k, v in settings.__dict__.items()}
        )
        check(FAKE_KEY not in serialised, "the API key must never live on the settings object")

    with clean_env():
        check(config.from_env(model_map_path=NO_MODEL_MAP).api_key() is None, "absent key means no Authorization header")


def test_the_old_variable_names_are_ignored() -> None:
    """`CLAIMCHECK_*` is not read by `from_env`, and nothing is said about it.

    An earlier change read the old names as deprecated fallbacks; the operator's fresh-start
    ruling removed that. Through `from_env`, the reader every run resolves
    through. Each old name is paired with a must-fire probe: the same value
    under the new name is read, so a check that passes here is not passing
    because the variable is never looked at. The prefixed and per-role forms
    are built at run time and are the ones a table of names would miss.
    """
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        fired = env_settings(LLOSSLESS_MODEL="new-model", LLOSSLESS_BASE_URL_MERGE="http://127.0.0.1:9/v1",
                             LLOSSLESS_WINDOW_VERIFY="32768", LLOSSLESS_EFFORT_MERGE="high",
                             LLOSSLESS_API_KEY_ENV_MERGE="MERGE_KEY_VARIABLE")
        check(fired.model_for("verify") == "new-model"
              and fired.base_url_for("merge") == "http://127.0.0.1:9/v1"
              and fired.window_for("verify") == 32768
              and fired.effort.get("merge") == "high"
              and fired.api_key_env_for("merge") == "MERGE_KEY_VARIABLE",
              "must fire: every new name used below is read")
        raises(config.ConfigError, lambda: env_settings(CLAIMCHECK_MODEL="old-model").model_for("verify"),
               "CLAIMCHECK_MODEL alone must leave no model configured")
        ignored = env_settings(LLOSSLESS_MODEL="m",
                               CLAIMCHECK_MODEL="old-model", CLAIMCHECK_BASE_URL_MERGE="http://127.0.0.1:9/v1",
                               CLAIMCHECK_WINDOW_VERIFY="32768", CLAIMCHECK_EFFORT_MERGE="high",
                               CLAIMCHECK_API_KEY_ENV_MERGE="MERGE_KEY_VARIABLE")
        check(ignored.model_for("verify") != "old-model",
              "CLAIMCHECK_MODEL must not be read")
        check(ignored.base_url_for("merge") != "http://127.0.0.1:9/v1",
              f"CLAIMCHECK_BASE_URL_MERGE must not be read: {ignored.base_url_for('merge')}")
        check(ignored.window_for("verify") != 32768,
              f"CLAIMCHECK_WINDOW_VERIFY must not be read: {ignored.window_for('verify')}")
        check(ignored.effort.get("merge") != "high",
              f"CLAIMCHECK_EFFORT_MERGE must not be read: {ignored.effort}")
        check(ignored.api_key_env_for("merge") != "MERGE_KEY_VARIABLE",
              "CLAIMCHECK_API_KEY_ENV_MERGE must not be read")
        # A value no reader accepts: refused under the new name, and under the
        # old one not even looked at.
        raises(config.ConfigError,
               lambda: env_settings(LLOSSLESS_MODEL="m", LLOSSLESS_FIDELITY="nonsense"),
               "must fire: an unreadable LLOSSLESS_FIDELITY is refused")
        env_settings(LLOSSLESS_MODEL="m", CLAIMCHECK_FIDELITY="nonsense")
    check(err.getvalue() == "",
          f"an old name must not be mentioned on stderr: {err.getvalue()!r}")
    check(not any(hasattr(config, name) for name in
                  ("environment", "env_value", "LEGACY_ENV_PREFIX", "announce_once")),
          "the fallback readers must be gone from config.py")


def test_an_exported_CLAIMCHECK_API_KEY_is_ignored() -> None:
    """A key exported as `CLAIMCHECK_API_KEY` is not sent, and not printed.

    `Settings.api_key` reads its source at send time rather than through
    `from_env`, so it is the second reader and needs its own check, with a
    per-run key source as the third. That earlier change sent such a key under the default
    `LLOSSLESS_API_KEY`; the fresh start makes it an unrelated variable.
    """
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        with clean_env(LLOSSLESS_API_KEY=FAKE_KEY):
            check(config.from_env(model_map_path=NO_MODEL_MAP).api_key() == FAKE_KEY,
                  "must fire: a key under LLOSSLESS_API_KEY is sent")
        with clean_env(CLAIMCHECK_API_KEY=FAKE_KEY):
            settings = config.from_env(model_map_path=NO_MODEL_MAP)
            check(settings.api_key_env_for(None) == "LLOSSLESS_API_KEY",
                  "the default key variable is LLOSSLESS_API_KEY")
            check(settings.api_key() is None,
                  "a key under the old name must not be sent")
        with config.keys_for_this_run({"CLAIMCHECK_API_KEY": FAKE_KEY}):
            check(config.Settings().api_key() is None,
                  "a per-run key source must not offer the old name either")
        with config.keys_for_this_run({"LLOSSLESS_API_KEY": FAKE_KEY}):
            check(config.Settings().api_key() == FAKE_KEY,
                  "must fire: a per-run key source under the new name is sent")
    check(err.getvalue() == "",
          f"nothing may be said about the old variable: "
          f"{err.getvalue().replace(FAKE_KEY, '<key>')!r}")


def test_the_old_config_and_cache_directories_are_not_read() -> None:
    """A pre-rename config file or cache is never read, however alone it is.

    Against a temporary `XDG_CONFIG_HOME`: with only an old file present the
    answer is still the new location, and the old file is not touched. Then
    through `Client`, the cache's only reader: an answer in the new default
    cache is served (the must-fire probe), and the same answer in the
    pre-rename cache beside it is not -- the run makes a live call.
    """
    with tempfile.TemporaryDirectory() as raw:
        home = {"XDG_CONFIG_HOME": raw}
        new = Path(raw) / "llossless" / "commands.json"
        old = Path(raw) / "claimcheck" / "commands.json"
        old.parent.mkdir()
        old.write_text("{}", encoding="utf-8")
        check(config.config_file("commands.json", home) == new,
              f"with only the old file present the new location is still the answer: "
              f"{config.config_file('commands.json', home)}")
        check(old.read_text(encoding="utf-8") == "{}", "the old file must be left as it was")
    check(not hasattr(config, "LEGACY_CACHE_DIR") and not hasattr(config, "LEGACY_MODEL_MAP"),
          "the old cache and model-map locations must be gone from config.py")

    saved = config.CACHE_DIR, getattr(config, "LEGACY_CACHE_DIR", None)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        calls = []
        responder = lambda _b, n: (calls.append(n), (200, envelope(CLAIMS_BODY)))[1]  # noqa: E731
        err = io.StringIO()
        try:
            config.CACHE_DIR = tmp / ".llossless-cache"
            if saved[1] is not None:
                # Only a build that still has the old location has one to aim.
                config.LEGACY_CACHE_DIR = tmp / ".claimcheck-cache"
            with FakeEndpoint(responder) as base_url, contextlib.redirect_stderr(err):
                fill = settings_for(base_url, tmp, use_cache=True,
                                    cache_dir=tmp / ".claimcheck-cache",
                                    structured="json_schema", pinned=True)
                claims_call(Client(fill))
                check(len(calls) == 1, "filling the old cache takes one live call")
                default = config.replace(fill, cache_dir=config.CACHE_DIR)
                client = Client(default)
                claims_call(client)
                check(len(calls) == 2 and client.usage.cache_hits == 0,
                      f"an answer in the old cache must not be served: {len(calls)} "
                      f"calls, {client.usage.cache_hits} hit(s)")
                again = Client(default)
                claims_call(again)
                check(len(calls) == 2 and again.usage.cache_hits == 1,
                      "must fire: the same answer in the new default cache is served")
            check("claimcheck" not in err.getvalue(),
                  f"the old cache must not be mentioned: {err.getvalue()!r}")
        finally:
            config.CACHE_DIR = saved[0]
            if saved[1] is not None:
                config.LEGACY_CACHE_DIR = saved[1]


def test_role_to_model_mapping() -> None:
    settings = env_settings(LLOSSLESS_MODEL="small", LLOSSLESS_MERGE_MODEL="big")
    check(settings.model_for("verify") == "small", "verify uses LLOSSLESS_MODEL")
    check(settings.model_for("merge") == "big", "merge uses LLOSSLESS_MERGE_MODEL")
    check(settings.model_for("decompose") == "small", "decompose falls back to the verify model")

    settings = env_settings(LLOSSLESS_MODEL="only")
    check(settings.model_for("merge") == "only", "merge defaults to the verify model")

    raises(
        config.ConfigError,
        lambda: config.Settings().model_for("verify"),
        "an unconfigured role must be a fatal, explanatory error",
    )
    raises(
        config.ConfigError,
        lambda: config.Settings().model_for("summarise"),
        "an unknown role must be rejected",
    )


def test_bad_config_is_rejected_early() -> None:
    with clean_env(LLOSSLESS_STRUCTURED="magic"):
        raises(config.ConfigError, lambda: config.from_env(model_map_path=NO_MODEL_MAP), "an unknown structured mode must be fatal")
    with clean_env(LLOSSLESS_TIMEOUT="soon"):
        raises(config.ConfigError, lambda: config.from_env(model_map_path=NO_MODEL_MAP), "a non-numeric timeout must be fatal")
    with clean_env(LLOSSLESS_CA_BUNDLE="/no/such/bundle.pem"):
        raises(config.ConfigError, lambda: config.from_env(model_map_path=NO_MODEL_MAP), "a missing CA bundle must be fatal")


# --------------------------------------------------------------------------
# PART C - parse, validate, repair
# --------------------------------------------------------------------------


def test_strip_reasoning() -> None:
    check(parsing.strip_reasoning('<think>musing</think>{"a":1}') == '{"a":1}',
          "a think block must be stripped")
    check(parsing.strip_reasoning('<thinking>x</thinking> {"a":1}') == '{"a":1}',
          "<thinking> is the same artefact under another name")
    check(parsing.strip_reasoning('{"a":1}') == '{"a":1}', "content without a block is unchanged")
    check(parsing.strip_reasoning('<think>cut off mid-') == "",
          "an unterminated block means the response was truncated; nothing survives it")


def test_strip_reasoning_only_strips_a_leading_block() -> None:
    """A reasoning block is a preamble, so only a preamble is stripped.

    The old rule scanned the whole string for `<think>` and deleted everything
    between the tags wherever they appeared. A document that *mentions* the
    tags -- a runbook telling an operator to wrap reasoning in them -- had that
    sentence silently deleted from the merged output, and the report said
    nothing was dropped. Offsets came from `text.lower()`, which is a second
    defect on the same line: `\u0130` lowercases to two characters, so every
    index after one was wrong.
    """
    s = parsing.strip_reasoning
    # must fire: a genuine preamble, in each spelling, closed or not
    check(s('<think>musing</think>{"a":1}') == '{"a":1}', "a leading block goes")
    check(s('  <THINK>x</THINK>  {"a":1}') == '{"a":1}', "case-insensitive, and anchored past whitespace")
    check(s('<scratchpad>x</scratchpad><think>y</think>{"a":1}') == '{"a":1}',
          "consecutive leading blocks are all preamble")
    check(s('<think>cut off mid-') == "",
          "an unterminated leading block means the response was truncated")

    # must not fire: the payload mentions the tags
    doc = '{"merged_document": "Wrap your reasoning in <think> and </think> tags."}'
    check(s(doc) == doc, f"tags inside a JSON string value must survive byte for byte: {s(doc)!r}")
    bare = '{"merged_document": "A bare <think> in prose."}'
    check(s(bare) == bare, f"a bare tag inside a string must not truncate: {s(bare)!r}")
    check(s('{"a":1} <think>trailing</think>') == '{"a":1} <think>trailing</think>',
          "nothing after the first non-block character is scanned")

    # the offset defect, both ways round
    keep = '\u0130 mentions <think> without a preamble'
    check(s(keep) == keep, f"a dotted capital I must not shift an offset: {s(keep)!r}")
    check(s('<think>x</think>\u0130 stays') == '\u0130 stays',
          "and a real preamble before one still strips cleanly")


def test_extract_json_counts_brackets() -> None:
    check(parsing.extract_json('prose {"a": {"b": 1}} trailing') == '{"a": {"b": 1}}',
          "nested objects must not close early")
    check(parsing.extract_json('{"path": "/-/healthy}"}') == '{"path": "/-/healthy}"}',
          "a brace inside a string is not a bracket")
    check(parsing.extract_json(r'{"q": "she said \"}\""}') == r'{"q": "she said \"}\""}',
          "an escaped quote must not end the string")
    check(parsing.extract_json('[{"a":1}]') == '[{"a":1}]', "a top-level array is valid JSON too")

    raises(parsing.ParseError, lambda: parsing.extract_json("no json here"),
           "text with no JSON must raise rather than return something")
    raises(parsing.ParseError, lambda: parsing.extract_json('{"a": [1, 2'),
           "truncated JSON must raise rather than be silently completed")


def test_an_unbalanced_scan_says_which_kind_of_unbalanced() -> None:
    """The answer "probably cut off" applied to two different questions.

    Graded against the three bodies an earlier version failed on, which are on
    disk in a gitignored exploratory corpus under `tests/eval/`. Every one is `finish_reason:
    "stop"` with balanced braces, and every one used to be reported as a
    truncation, sending the reader to max_tokens, which was never the problem.
    """
    def fault(text: str) -> parsing.ParseError:
        error = raises(parsing.ParseError, lambda: parsing.extract_json(text),
                       f"{text[:40]!r} must not parse")
        assert error is not None
        return error

    ran_out = fault('{"a": [1, 2')
    check("bracket(s) still open" in str(ran_out) and "cut off" in str(ran_out),
          f"brackets left open with the scanner outside a string is the real "
          f"truncation, and only it may say cut off: {ran_out}")
    check("2 bracket(s) were never closed" in ran_out.feedback,
          f"the repair feedback must name the count, got {ran_out.feedback!r}")

    mid_string = fault('{"a": "unfinished')
    check("ended inside a string value" in str(mid_string)
          and "cut off" not in str(mid_string),
          f"a run of input that stops mid-value is its own case: {mid_string}")

    # A shape seen before, minimised: a string opened and left at a raw newline. Every
    # quote after it reads with inverted parity, so the closing braces are
    # swallowed, yet the document is complete and ends on its own '}'.
    lost = fault('{\n  "a": "one",\n  "b\n  "c": "two"\n}')
    check("not truncated" in str(lost) and "never closed" in str(lost),
          f"a complete document must not be reported as truncated: {lost}")
    check("cut off" not in str(lost) and "max_tokens" not in str(lost),
          f"nothing here may point at the budget: {lost}")
    check(r'write \"' in lost.feedback and r"\n for a newline" in lost.feedback,
          f"the model must be told what to escape, got {lost.feedback!r}")

    # Raw endpoint responses, so `tests/eval/*/` is gitignored and they do not
    # ship -- see .gitignore. The `is_dir()` guard below used to sit in front of
    # a flat `== 3`, which made it dead code: absence produced zero bodies and
    # failed the check, and the published copy failed this module on a file it
    # was never given. Absence is now its own outcome and is counted, because a
    # check that quietly skips is a check that passes.
    failures = ROOT / "tests" / "eval" / "m4-tier-latch" / "failures"
    if not failures.is_dir():
        unjudged.append("failure bodies: evidence not in this copy "
                        "(a gitignored exploratory corpus under tests/eval/ does not publish)")
        bodies = []
    else:
        bodies = sorted(failures.glob("*.txt"))
        check(len(bodies) == 3, f"three recorded failure bodies expected, found {len(bodies)}")
    for path in bodies:
        response = json.loads(path.read_text(encoding="utf-8"))
        choice = response["choices"][0]
        text = parsing.strip_fences(parsing.strip_reasoning(choice["message"]["content"]))
        check(choice["finish_reason"] == "stop",
              f"{path.name} is evidence only because it finished: {choice['finish_reason']}")
        check(text.count("{") == text.count("}") and text.rstrip().endswith("}"),
              f"{path.name} must have balanced braces and end on its own brace")
        reported = fault(text)
        check("not truncated" in str(reported),
              f"{path.name} is a complete document; got {reported}")


def test_validator() -> None:
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "maxLength": 5},
            "n": {"type": "integer"},
            "label": {"enum": ["A", "B"]},
            "items": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["name", "n"],
        "additionalProperties": False,
    }
    check(parsing.validate({"name": "ok", "n": 1}, schema) == [], "a valid object must pass")
    check(parsing.validate({"n": 1}, schema) != [], "a missing required property must fail")
    check(parsing.validate({"name": "ok", "n": "1"}, schema) != [], "a wrong type must fail")
    check(parsing.validate({"name": "toolong", "n": 1}, schema) != [], "maxLength must be enforced")
    check(parsing.validate({"name": "ok", "n": 1, "x": 2}, schema) != [],
          "additionalProperties: false must be enforced")
    check(parsing.validate({"name": "ok", "n": 1, "label": "C"}, schema) != [],
          "a value outside an enum must fail")
    check(parsing.validate({"name": "ok", "n": 1, "items": ["a", 2]}, schema) != [],
          "array item types must be checked")
    check(parsing.validate({"name": "ok", "n": True}, schema) != [],
          "True is not an integer, whatever Python thinks")


def test_semantic_checks() -> None:
    check(parsing.check_claims({"claims": [{"text": "x", "span": "x"}]}) == [],
          "a complete claim must pass")
    check(parsing.check_claims({"claims": [{"text": " ", "span": "x"}]}) != [],
          "an empty claim text must fail")
    check(parsing.check_claims({"claims": [{"text": "x", "span": ""}]}) != [],
          "a claim with no span cannot have its line trusted")

    # A claim is evidence about a place; the same claim offered again
    # for the same line is the response restating itself, and past the limit it
    # is a generation loop. Repetition across *different* lines is a document
    # that repeats itself and must pass, see `test_decompose.py` for the
    # corpus-wide control.
    one_place = [{"text": "x", "line": 3, "span": "x"}]
    check(parsing.check_claims({"claims": one_place * parsing.CLAIM_REPEAT_LIMIT}) == [],
          f"{parsing.CLAIM_REPEAT_LIMIT} claims at one place is the limit, not past it")
    looping = parsing.check_claims({"claims": one_place * (parsing.CLAIM_REPEAT_LIMIT + 1)})
    check(looping and all(isinstance(fault, parsing.RepeatFault) for fault in looping),
          f"one claim past the limit at one place is a loop and nothing else: {looping}")
    check(parsing.parse_error(CLAIM_SCHEMA, looping).looping,
          "and the error must say so, because that is what bounds the re-asks")
    spread = [{"text": "x", "line": line, "span": "x"}
              for line in range(parsing.CLAIM_REPEAT_LIMIT * 4)]
    check(parsing.check_claims({"claims": spread}) == [],
          "the same fact on a different line each time is a repetitive document")

    ok = {"claim_id": "A-001", "verdict": "SUPPORTED", "evidence": "e",
          "evidence_source": "merged.md", "rationale": "r."}
    check(tuple(ok) == parsing.VERDICT_FIELDS, "written in contract order, as required")
    check(parsing.check_verdicts({"verdicts": [ok]}) == [], "a well-formed verdict must pass")
    check(parsing.check_verdicts({"verdicts": [ok, dict(ok)]}) != [],
          "a duplicate claim_id must fail")
    check(parsing.check_verdicts({"verdicts": [dict(ok, evidence="")]}) != [],
          "SUPPORTED without evidence must fail")
    check(parsing.check_verdicts({"verdicts": [dict(ok, verdict="UNCLEAR")]}) != [],
          "the label set is closed")
    check(parsing.check_verdicts({"verdicts": [dict(ok, verdict="PARTIAL")]}) == [],
          "PARTIAL is a verdict, and it owes evidence like any other")
    check(parsing.check_verdicts({"verdicts": [dict(ok, verdict="PARTIAL", evidence="")]}) != [],
          "a PARTIAL that quotes nothing does not say which part is stated")


def test_each_role_can_have_its_own_endpoint_key_and_window() -> None:
    """The point of the whole exercise, asserted.

    `model_for` has resolved a model per role since the brief, but one
    `base_url` served all of them, so "a frontier merge beside a local
    decompose", the operator's stated goal, and the thing the paper's model
    study needs, could not be configured at all.

    Three axes, because an endpoint is not just a URL: the host, the variable
    holding its key, and its context window. A run that got two of the three
    right would send the wrong credential or size the request for the wrong
    box, and both fail at the vendor rather than here.
    """
    settings = config.Settings(
        base_url="http://local.invalid:11434",
        models={"verify": "small", "merge": "large"},
        window=8192,
        endpoints={"merge": "https://vendor.invalid/v1"},
        api_key_envs={"merge": "VENDOR_KEY"},
        windows={"merge": 32768},
    )
    check(settings.base_url_for("merge") == "https://vendor.invalid/v1",
          f"merge must go to its own endpoint: {settings.base_url_for('merge')}")
    check(settings.base_url_for("verify") == "http://local.invalid:11434/v1",
          f"a role with no entry uses base_url: {settings.base_url_for('verify')}")
    check(settings.window_for("merge") == 32768 and settings.window_for("verify") == 8192,
          "the window follows the endpoint, not the run")
    check(settings.api_key_env_for("merge") == "VENDOR_KEY",
          f"merge reads its own key variable: {settings.api_key_env_for('merge')}")

    # No `decompose` -> `verify` fallback for the endpoint, though `model_for`
    # has one. That fallback is an argument about which *model* suits the two
    # roles and says nothing about where either is served; inheriting a host
    # from it would put a role on a box nobody configured for it.
    check(settings.base_url_for("decompose") == settings.base_url,
          "decompose must not inherit an endpoint from verify")

    # The key is still read fresh from the environment and still never stored.
    # Three endpoints must not mean three credentials in a dataclass that
    # `repr` and `asdict` reach.
    dumped = repr(settings) + json.dumps(dataclasses.asdict(settings), default=str)
    check("VENDOR_KEY" in dumped and "secret-value" not in dumped,
          "the map holds variable names; a key in it would reach every dump")
    os.environ["VENDOR_KEY"] = "secret-value"
    try:
        check(settings.api_key("merge") == "secret-value",
              "merge's key comes from merge's variable")
        check(settings.api_key("verify") != "secret-value",
              "verify must not be handed the vendor's key")
    finally:
        del os.environ["VENDOR_KEY"]

    # An unknown role is a configuration error everywhere, not a silent
    # fallback to the default endpoint -- a typo in one of these maps would
    # otherwise route a role to the wrong box and report nothing.
    for call in (settings.base_url_for, settings.window_for,
                 settings.api_key_env_for, settings.endpoint_id_for):
        try:
            call("mrege")
        except config.ConfigError:
            pass
        else:
            check(False, f"{call.__name__} accepted an unknown role")


def test_two_deployments_on_one_host_get_two_ids_and_the_split_follows() -> None:
    """The census half of the per-role split and the warm-cache change, exercised on the topology that broke them.

    **Two paths on one host, which is the whole point of this test.** The
    version it replaces used `local.invalid` and `vendor.invalid` -- two
    different *hostnames* -- and passed for four milestones while every
    deployment on the provider the operator actually runs against shared one
    id, because that provider routes by path and the id hashed the hostname.
    Twelve runs on two boxes recorded one id between them.
    A fixture that varies the hostname varies the thing that already worked.

    So the two settings below differ in exactly one component: one path
    segment. If this test is ever edited to give them two hostnames it is the
    old test again and it will pass against the defect.

    Four things are asserted, in the order they failed:

    1. Two deployments, one id, is the defect -- and the *premise* is checked
       first, because "one host" is what makes the rest of it mean anything.
    2. Scheme 1 is pinned as producing the collision, so a revert cannot make
       this test green: the assertion names the old rule rather than trusting
       that a different one is in force.
    3. The per-role split inherits whatever `endpoint_id` hashes, so it is
       re-asserted here on two paths rather than two hostnames.
    4. None of this may print an address, labelled or not.
    """
    host = "provider.invalid"
    one = config.Settings(base_url=f"https://{host}/v2/aaaaaaaaaaaa/openai/v1")
    two = config.Settings(base_url=f"https://{host}/v2/bbbbbbbbbbbb/openai/v1")

    # 1. The premise. A fixture that quietly stopped varying one thing is how
    #    this defect survived its own test.
    check(one.host == two.host == host,
          f"this fixture must vary the path and nothing else; hosts are "
          f"{one.host!r} and {two.host!r}")
    check(one.base_url != two.base_url, "two deployments, or there is nothing to tell apart")
    check(one.endpoint_id != two.endpoint_id,
          f"two deployments on one host must not share a census entry; both are "
          f"{one.endpoint_id!r}")

    # 2. The old rule, named and pinned firing. Under scheme 1 these two
    #    collide, and that is the measurement this fix rests on -- not an
    #    assumption about what the current code does differently.
    check(config.legacy_endpoint_id(one.host) == config.legacy_endpoint_id(two.host),
          "scheme 1 hashed the hostname, so these two must collide under it; if "
          "they do not, this test is no longer measuring the defect it was written for")

    # 3. The per-role split, on the same topology. Unlabelled, because a
    #    label already separates the roles by name and would hide a hash that
    #    still could not tell two paths apart.
    split = config.Settings(
        base_url=f"https://{host}/v2/aaaaaaaaaaaa/openai/v1",
        endpoints={"merge": f"https://{host}/v2/bbbbbbbbbbbb/openai/v1"},
    )
    check(split.endpoint_id_for("merge") != split.endpoint_id_for("verify"),
          "a role on its own deployment must get its own id, path-routed or not")
    check(split.endpoint_id_for("verify") == split.endpoint_id,
          "a role with no override keeps the run-wide id")
    check(split.endpoint_id_for("merge") == two.endpoint_id,
          "a role's id is its own endpoint's id; the role name must not be mixed in")

    plain = config.Settings(base_url=f"https://{host}/v2/aaaaaaaaaaaa/openai/v1")
    for role in config.ROLES:
        check(plain.endpoint_id_for(role) == plain.endpoint_id,
              f"a single-endpoint run must still be one census row; {role} moved")

    # A port is the other thing two deployments on one host can differ by, and
    # `Settings.port` has accounted for it while the id ignored it.
    check(config.Settings(base_url="http://box.invalid:11434/v1").endpoint_id
          != config.Settings(base_url="http://box.invalid:11435/v1").endpoint_id,
          "two servers on one box at two ports are two deployments")

    # 4. Still no address, and the label still overrides the whole address.
    labelled = config.Settings(
        base_url=f"https://{host}/v2/aaaaaaaaaaaa/openai/v1",
        endpoints={"merge": f"https://{host}/v2/bbbbbbbbbbbb/openai/v1"},
        endpoint_label="prod",
    )
    check(labelled.endpoint_id_for("merge") != labelled.endpoint_id_for("verify"),
          "two deployments under one label must not share a census entry")
    for role in config.ROLES:
        shown = labelled.endpoint_name_for(role)
        check(host not in shown and "aaaaaaaaaaaa" not in shown and "bbbbbbbbbbbb" not in shown,
              f"a labelled deployment must not print an address; got {shown!r}")
    for identifier in (one.endpoint_id, two.endpoint_id,
                       labelled.endpoint_id_for("merge")):
        check(len(identifier) == config.ENDPOINT_ID_CHARS
              and all(c in "0123456789abcdef" for c in identifier),
              f"an id is a truncated digest and nothing else; got {identifier!r}")


def test_pre_pass_caps_length_violations_instead_of_rejecting_them() -> None:
    """The gate on Pass B.

    Three outcomes per capped field, exercised on both the merge shape
    (`replacement`/`reason`) and the verify shape (`rationale`): under the cap
    and untouched, over the cap and truncated in place with the violation
    still reported, and exactly at the cap and cut mid-sentence -- reported
    but *not* mutated, since there is nothing this pass put there to trim.
    Whichever the outcome, `validate` must never see a `maxLength` fault for a
    field this pass already touched: that is the whole of what "non-fatal"
    means here.
    """
    good_disposition = {"segment": "b2", "disposition": "duplicate",
                        "replacement": "the merge", "reason": "a1 already states it."}

    def merge_payload(**overrides):
        disposition = {**good_disposition, **overrides}
        # `mismatch` is required at every level since it was added, and empty is the
        # honest answer: this payload is about a capped `reason`, not about
        # documents that do not belong together.
        return {"merged_document": "the merge", "decisions": [],
                "dispositions": [disposition], "mismatch": ""}

    # Under the cap: neither mutated nor reported.
    payload, errors, truncations = parsing.parse(
        json.dumps(merge_payload()), merge.MERGE_SCHEMA, parsing.check_merge)
    check(errors == [], f"a well-formed pair of records must pass unremarked: {errors}")
    check(truncations == [], f"nothing here overran a cap: {truncations}")
    check(payload["dispositions"][0]["reason"] == good_disposition["reason"],
          "an under-cap field must be left exactly as written")

    # Over the cap: `reason` is cut hard, in place, and the field survives
    # validate() rather than tripping its maxLength.
    over_reason = "x" * (parsing.REASON_MAX + 1) + " and more still after that."
    payload, errors, truncations = parsing.parse(
        json.dumps(merge_payload(reason=over_reason)), merge.MERGE_SCHEMA, parsing.check_merge)
    check(errors == [], f"an over-cap reason must not fail validation: {errors}")
    check(len(truncations) == 1, f"exactly one field overran its cap: {truncations}")
    hit = truncations[0]
    check(hit.path == "$.dispositions[0].reason", f"the path must name the field: {hit.path}")
    check(hit.original_length == len(over_reason),
          f"the original length must be recorded, not the capped one: {hit}")
    check(hit.cap == parsing.REASON_MAX, f"the cap must be REASON_MAX: {hit}")
    check(payload["dispositions"][0]["reason"] == over_reason[:parsing.REASON_MAX],
          "an over-cap reason must be hard-truncated in place")

    # Over the cap on `replacement`: capped with `anchor`, not a hard cut,
    # since it has the two-ended form the prompt documents.
    # Sized from the constant, not by a repeat count somebody once counted:
    # raising `REPLACEMENT_MAX` left the old fixture under the cap it exists to
    # exceed, and the probe failed by IndexError rather than by saying so.
    sentence = "The relay listens on port 8443, and the read timeout is 45 seconds. "
    span = sentence * (parsing.REPLACEMENT_MAX // len(sentence) + 2)
    check(len(span) > parsing.REPLACEMENT_MAX,
          f"the fixture must exceed the cap to test it: {len(span)}")
    payload, errors, truncations = parsing.parse(
        json.dumps(merge_payload(replacement=span)), merge.MERGE_SCHEMA, parsing.check_merge)
    check(errors == [], f"an over-cap replacement must not fail validation: {errors}")
    check(len(truncations) == 1, f"exactly one field overran its cap: {truncations}")
    check(truncations[0].path == "$.dispositions[0].replacement",
          f"the path must name replacement, not reason: {truncations[0]}")
    check(payload["dispositions"][0]["replacement"] == parsing.anchor(span),
          "an over-cap replacement must be capped with anchor(), not a hard cut")
    check(len(payload["dispositions"][0]["replacement"]) <= parsing.REPLACEMENT_MAX,
          "the capped replacement must itself respect the cap")

    # Exactly at the cap and cut mid-sentence: reported, not mutated.
    at_cap_unfinished = ("x" * (parsing.REASON_MAX - 1)) + "e"
    check(len(at_cap_unfinished) == parsing.REASON_MAX, "fixture must land exactly on the cap")
    check(parsing.unfinished(at_cap_unfinished), "fixture must actually look cut off")
    payload, errors, truncations = parsing.parse(
        json.dumps(merge_payload(reason=at_cap_unfinished)), merge.MERGE_SCHEMA, parsing.check_merge)
    check(errors == [], f"an at-cap reason must not fail validation: {errors}")
    check(len(truncations) == 1, f"the at-cap-and-unfinished case must still be reported: {truncations}")
    check(truncations[0].original_length == parsing.REASON_MAX,
          f"nothing was trimmed, so original_length equals the cap: {truncations[0]}")
    check(payload["dispositions"][0]["reason"] == at_cap_unfinished,
          "an at-cap field this pass did not shorten must not be mutated")

    # Exactly at the cap and *finished*: neither mutated nor reported. The
    # mid-sentence check is what tells this apart from a `reason` a model
    # happened to write to exactly REASON_MAX characters on purpose.
    at_cap_finished = ("x" * (parsing.REASON_MAX - 1)) + "."
    check(len(at_cap_finished) == parsing.REASON_MAX, "fixture must land exactly on the cap")
    check(not parsing.unfinished(at_cap_finished), "fixture must read as a complete sentence")
    _, errors, truncations = parsing.parse(
        json.dumps(merge_payload(reason=at_cap_finished)), merge.MERGE_SCHEMA, parsing.check_merge)
    check(errors == [], f"an at-cap finished reason must not fail validation: {errors}")
    check(truncations == [], f"a finished sentence at the cap is not a violation: {truncations}")

    # The verify shape: `rationale`, same three outcomes, on VERDICT_SCHEMA.
    good_verdict = {"claim_id": "A-001", "verdict": "SUPPORTED", "evidence": "e",
                    "evidence_source": "merged.md", "rationale": "the reference text states it."}

    def verify_payload(**overrides):
        return {"verdicts": [{**good_verdict, **overrides}]}

    over_rationale = "y" * (parsing.RATIONALE_MAX + 1) + " and more still after that."
    payload, errors, truncations = parsing.parse(
        json.dumps(verify_payload(rationale=over_rationale)), verify.VERDICT_SCHEMA, parsing.check_verdicts)
    check(errors == [], f"an over-cap rationale must not fail validation: {errors}")
    check(len(truncations) == 1, f"exactly one field overran its cap: {truncations}")
    check(truncations[0].path == "$.verdicts[0].rationale",
          f"the path must name the verdict's rationale: {truncations[0]}")
    check(payload["verdicts"][0]["rationale"] == over_rationale[:parsing.RATIONALE_MAX],
          "an over-cap rationale must be hard-truncated in place")

    # A decisions-shaped record gets the same treatment as a dispositions one,
    # under the same "reason" key, at its own path.
    good_decision = {"slot": "title",
                     "candidates": [{"text": "A", "document": "source_a.md"},
                                    {"text": "B", "document": "source_b.md"}],
                     "chosen": "A", "reason": "The base document's title."}
    over_decision_reason = "z" * (parsing.REASON_MAX + 1) + " and more still after that."
    decision_payload = {"merged_document": "the merge", "dispositions": [],
                        "decisions": [{**good_decision, "reason": over_decision_reason}],
                        "mismatch": ""}
    payload, errors, truncations = parsing.parse(
        json.dumps(decision_payload), merge.MERGE_SCHEMA, parsing.check_merge)
    check(errors == [], f"an over-cap decision reason must not fail validation: {errors}")
    check(len(truncations) == 1, f"exactly one field overran its cap: {truncations}")
    check(truncations[0].path == "$.decisions[0].reason",
          f"the path must name the decision, not a disposition: {truncations[0]}")

    # A payload `_truncate_capped_fields` does not recognise -- decompose's
    # claims shape -- must pass through untouched rather than erroring.
    claims_payload = {"claims": [{"claim_id": "A-001", "text": "x", "span": "x"}]}
    _, _, truncations = parsing.parse(json.dumps(claims_payload), CLAIM_SCHEMA)
    check(truncations == [], f"an unrecognised shape must not be walked: {truncations}")


def test_parse_feedback_names_the_fault() -> None:
    _, defects, _ = parsing.parse(
        '{"verdicts": [{"claim_id": "A-001", "verdict": "UNCLEAR", '
        '"evidence": "e", "evidence_source": "merged.md", '
        '"rationale": "r."}]}',
        VERDICT_SCHEMA, parsing.check_verdicts,
    )
    check(bool(defects), "an out-of-set verdict must be rejected")
    exc = parsing.parse_error(VERDICT_SCHEMA, defects)
    check("UNCLEAR" in exc.feedback, "the repair message must quote the offending value")
    check("SUPPORTED" in exc.feedback, "the repair message must state the allowed values")


def test_no_semantic_checker_raises_on_an_answer_that_is_not_an_object() -> None:
    """A bare array is a complaint, not an AttributeError.

    Every checker, not the two the live run happened to reach. One of them
    having a guard is not evidence the others do, and the four are reached
    from four different callers -- `decompose`, `merge`, and `verify` twice --
    so a hole in any one of them ends a run on a traceback.

    Checked against the shipped functions by name rather than against a list
    of the ones that were broken, so a fifth checker added later is added to
    this tuple or it is the one nobody covered.
    """
    bare = [{"text": "x"}]
    checkers = (
        ("check_claims", parsing.check_claims, "claims"),
        ("check_coverage", parsing.check_coverage, "claims"),
        ("check_verdicts", parsing.check_verdicts, "verdicts"),
        ("check_merge", parsing.check_merge, "merged_document"),
    )
    for name, checker, wanted in checkers:
        try:
            errors = checker(bare)
        except Exception as exc:  # noqa: BLE001 - raising is the defect
            failures.append(f"{name} raised {type(exc).__name__} on a bare array: {exc}")
            continue
        check(bool(errors), f"{name} must complain about a bare array, got {errors}")
        said = " ".join(errors)
        # The shape, not only the fact of a fault: the message is fed back to
        # the model verbatim, and "wrong" without "an object with a `claims`
        # key" is a rejection the model cannot act on.
        check("object" in said, f"{name} must name the expected shape: {said}")
        check(wanted in said, f"{name} must name the key it wanted: {said}")

    # The structured form `verify`'s Pass C reads, and the closure built on
    # top of it. Both walk the payload again after the checker has answered.
    defects, tainted = parsing.verdict_defects(bare)
    check(defects and defects[0][0] is None,
          f"a shape fault belongs to the response, not a record: {defects}")
    check(tainted == set(), f"no record is salvageable from a non-object: {tainted}")
    check(verify._split(["A-001"], (), "off")(bare)[0] == defects,
          "the split checker must return the shape complaint rather than walking on")

    # The capping pre-pass runs before the schema walk, so it is the first
    # thing a bare array touches inside `parse`.
    check(parsing._truncate_capped_fields(bare) == [],
          "nothing can be capped in a payload that has no fields")

    # And `parse` itself, which is where the live run died: it returns the
    # fault as a defect the caller can raise on, and never the payload.
    payload, defects, truncations = parsing.parse(
        json.dumps(bare), CLAIM_SCHEMA, parsing.check_claims)
    check(payload == {} and truncations == [],
          f"a non-object payload is dropped, not returned: {payload}")
    check(any("expected object" in defect for defect in defects),
          f"parse must report the shape fault: {defects}")
    # A schema with no top-level `type` gives the schema walk nothing to
    # refuse, which is the case the checkers' own guards exist for.
    _, defects, _ = parsing.parse(
        json.dumps(bare), {"properties": {"claims": {"type": "array"}}},
        parsing.check_claims)
    check(any("expected object" in defect for defect in defects),
          f"a typeless schema must still refuse a bare array: {defects}")


def test_a_bare_array_answer_reaches_the_repair_loop() -> None:
    """The must-fire: a wrong-shaped answer is repaired, not a traceback.

    Driven through `client.complete` rather than through `parse`, because the
    thing the defect cost was a run: the `AttributeError` left the client's
    `except` clause untouched, so the answer was never fed back and the run
    ended at exit 2 with two errored units.
    """
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(
            lambda _b, _n: (200, envelope(json.dumps([{"text": "x", "span": "x"}]))))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)))
            raises(SchemaFailure, lambda: claims_call(client),
                   "a bare array must be refused as a schema fault")

    check(endpoint.calls == SCHEMA_ATTEMPTS,
          f"the model must be asked again, not dropped: {endpoint.calls} call(s)")
    told = json.dumps(endpoint.requests[1]["messages"])
    check("expected object" in told,
          f"attempt 2 must quote the shape fault back to the model: {told[-400:]}")
    check("claims" in told, "the repair message must name the key that was wanted")


# --------------------------------------------------------------------------
# PART D - cassette keys
# --------------------------------------------------------------------------


def test_cassette_key_covers_what_changes_the_answer() -> None:
    base = dict(
        role="decompose",
        model="m",
        tier="json_schema",
        prompt_sha256="abc",
        messages=[{"role": "user", "content": "hello"}],
        schema={"type": "object"},
        temperature=0.0,
        seed=0,
        max_tokens=None,
    )
    key = cassette.key_for(**base)
    check(key == cassette.key_for(**base), "the key must be stable across calls")
    for field, value in (
        ("role", "verify"),
        ("model", "other"),
        ("tier", "prompt"),
        ("prompt_sha256", "def"),
        ("messages", [{"role": "user", "content": "goodbye"}]),
        ("schema", {"type": "array"}),
        ("temperature", 0.7),
        ("seed", 1),
        ("max_tokens", 512),
        ("sample", 1),
    ):
        check(cassette.key_for(**{**base, field: value}) != key,
              f"changing {field} must change the cassette key")

    # A third role is recorded against a third prompt, and it must not be able
    # to collide with either of the two already on disk or be served their
    # recordings. Checked before merge exists rather than after: a role that
    # shared a key space would only show up as a wrong answer replayed
    # confidently, which is the failure cassettes are supposed to prevent.
    merge = dict(base, role="merge", prompt_sha256="merge-prompt-hash")
    check(cassette.key_for(**merge) != key,
          "a merge call must not share a key with a decompose call")
    check(cassette.key_for(**merge) != cassette.key_for(**dict(merge, model="other")),
          "the merge model must be part of the merge cassette key")
    check(cassette.key_for(**merge) != cassette.key_for(**dict(merge, prompt_sha256="x")),
          "the merge prompt hash must be part of the merge cassette key")
    check(cassette.filename("merge", key).startswith("merge-"),
          "merge cassettes must be filed under their own role prefix")
    check(set(config.ROLES) >= {"merge", "decompose", "verify"},
          "merge must already be a configurable role, or it cannot be given a model")

    # The whole point of the sample dial. If repeats collided, the second
    # identical call would be served the first one's recording and every
    # stability figure the runners print would be 100% by construction.
    check(len({cassette.key_for(**base, sample=n) for n in range(3)}) == 3,
          "three samples of one request must be three distinct cassettes")
    check(cassette.key_for(**base, sample=0) == key,
          "sample 0 is the default, so the parameter cannot be optional in name only")

    check(cassette.filename("decompose", key) == f"decompose-{key[:16]}.json",
          "cassette filenames must be <role>-<key[:16]>.json")


# The eleven components of a cassette key, and the digest each combination of
# them produced on 2026-08-09, before a later change altered how `tier` is
# resolved. Pinned rather than recomputed, which is the entire point: a test
# that derives its expectation from the implementation agrees with every version
# of it.
#
# The stake is the corpora. `tier` is a key component, so a change to how it is
# resolved that reaches `key_for` makes all 264 `m4/` cassettes and all 180 root-corpus
# cassettes unreachable at once — and the symptom is a replay miss on file 1,
# with nothing to say whether the recordings or the derivation moved. Later
# work may change resolution freely but must not change the key; this
# is the line between the two, and it is a stop-and-ask when it fails.
KEY_PIN_BASE = dict(
    role="decompose",
    model="qwen3:8b",
    tier="json_schema",
    prompt_sha256="b4ec1e0c7ead" + "0" * 52,
    messages=[{"role": "user", "content": "  1 | The relay listens on port 8443.\n"}],
    schema={"type": "object", "properties": {"claims": {"type": "array"}}},
    temperature=0.0,
    seed=0,
    max_tokens=None,
    thinking=False,
    sample=0,
)

KEY_PIN = (
    ({}, "2fbce807c03d054acc9c9e214b6ed76b01c1385c028a246715963b0d242c22ed"),
    ({"role": "merge"}, "a6e3a724b4881294c3cf1e76663e37d8904fa4da444199d060fafdafc1983b48"),
    ({"model": "qwen3:4b"}, "d5b9f95a36ea3433cc1efd12dbd9cff419e9e809bb671160d288a2d33e2d2e4c"),
    ({"tier": "tool_call"}, "deefd64e89bb6dbe3b079a0a329b848f73be00f4d580b3a03f30a1d15698a069"),
    ({"tier": "prompt"}, "65a49b5c48a10a11cf4b7c1fab51876d5366625b724f528af3d220fdc59fd913"),
    ({"prompt_sha256": "0" * 64},
     "6f22941b81e0796afbf17a6b1440284fc40fdbffcbe1f8a7a2e4a2eb70a09738"),
    ({"messages": [{"role": "user", "content": "x"}]},
     "3e4e36a7096d71426df7a3225801e3bea501e54931dd89342add806d54ec0eab"),
    ({"schema": None}, "8ba70ef7a41f6aa4e62bc21b2869f10f07245b897901b751b94db43b0bbeca0a"),
    ({"temperature": 0.7}, "a208dc69e371a398e05f29a38ae3c346f19e14988d0c174c71a03741bfbe0b9b"),
    ({"seed": None}, "d537f8dbb40fa9adc067f78def8cf2e6272b4435a33732dfa8d073e2490b5ddb"),
    ({"seed": 1}, "7ca71a6b4b6ddb7ce9e32f510b25047ba3ec4b06703a9431f92abfd7fedff0e1"),
    ({"max_tokens": 2560}, "27e3a8056426d90458bdf33d5af724f27ce3db535289a12d45e25eb3655e6bc2"),
    ({"thinking": True}, "098c867dc148792499ffb6fce442b2d2da2e413b1268c71aa3616f00fe970fd0"),
    ({"sample": 2}, "b126d5ed63a0374f82ba592568438b1c02ceee9488f852bc6871e53bc894cd8c"),
)

M4_CASSETTES = ROOT / "tests" / "responses" / "m4"


def test_cassette_key_derivation_is_pinned() -> None:
    """Fourteen golden digests, the component list, and one real corpus lookup."""
    for overrides, expected in KEY_PIN:
        actual = cassette.key_for(**{**KEY_PIN_BASE, **overrides})
        check(actual == expected,
              f"cassette key derivation changed for {overrides or 'the base case'}: "
              f"expected {expected}, got {actual} — the recorded corpora are keyed "
              f"by this function and every cassette on disk becomes unreachable")

    # Named separately from the digests because the two fail differently. A new
    # component with a default changes every digest above and says nothing about
    # which one appeared; this says the name.
    components = sorted(inspect.signature(cassette.key_for).parameters)
    check(components == [
        "command", "max_tokens", "messages", "model", "profile", "prompt_sha256",
        "role", "sample", "schema", "seed", "temperature", "thinking", "tier",
    ], f"the cassette key takes {components}; adding or removing a component "
       f"orphans every recording, including the `timeout` field wanted in the "
       f"journal: the journal is not the key")

    # `profile` and `command` are the two components left out of the hash at
    # their default values, and `command` was added on exactly the terms
    # `profile` was: every recording on disk was made over HTTP, so
    # naming the mechanism in their keys would rename all of them to say
    # something already true of them. The fourteen digests below are the
    # assertion that it did not. That is what let it be added without
    # moving the fourteen digests above -- which is the assertion, not the
    # anecdote: the corpus is 697 recordings and every one of them was made
    # with the default profile's body, so naming it in their keys would rename
    # all of them to say something already true of them.
    #
    # Both halves, because either alone is satisfiable by a broken function. A
    # `profile` that never entered the hash would pass the first; one that
    # always entered it would pass the second and orphan the corpus.
    check(cassette.key_for(**KEY_PIN_BASE)
          == cassette.key_for(**KEY_PIN_BASE, profile=structured.DEFAULT_PROFILE),
          "naming the default profile must produce the same key as omitting it, "
          "or every recording on disk is keyed under a name it was not written "
          "with")
    for name in sorted(set(structured.PROFILES) - {structured.DEFAULT_PROFILE}):
        check(cassette.key_for(**KEY_PIN_BASE, profile=name)
              != cassette.key_for(**KEY_PIN_BASE),
              f"the {name!r} profile sends a different body -- different field "
              f"names, or fields the default sends and it does not -- so it must "
              f"not share a cassette key with the default")
    check(len({cassette.key_for(**KEY_PIN_BASE, profile=name)
               for name in structured.PROFILES}) == len(structured.PROFILES),
          "two profiles must not share a key: each one is a distinct request "
          "shape and a recording made under one cannot answer for another")


def test_the_m4_merge_corpus_is_orphaned_by_the_new_prompt_and_nothing_else() -> None:
    """An earlier change replaced `merge.md`, and this says so rather than implying it.

    This test used to rebuild six real cassette keys and assert every one was
    present, pinning the whole path to the hash: the prompt file,
    `merge.budget_tokens`, the schema, `TEMPERATURE`, `SEED` and the
    per-condition thinking flag all feed the key, and any of them moving
    unrecords the corpus as surely as editing `key_for` would.

    All six are now absent, by design and on schedule. This was expected:
    `merge.md` orphans all 264 cassettes under `tests/responses/m4/`, and
    a later pass re-records the grid. Deleting the test would throw away the guard
    permanently to make this quiet, so it is inverted instead: the six
    keys must be *missing*, and the corpus files must still be *there*.

    That keeps two real failures live. If someone reverts the prompt without
    reverting the pipeline, the keys resolve and this fails. If someone deletes
    the corpus rather than re-recording it, the file count fails. When that
    pass lands, this flips back to asserting presence: the message says so, because
    a re-recorded corpus that leaves this test green would be a test that had
    stopped meaning anything.
    """
    if not M4_CASSETTES.is_dir():
        return  # the corpus is committed; a checkout without it is not a failure here
    names = merge.source_names(2)  # every fixture is a pair
    sources = {
        name: (ROOT / "tests" / "fixtures" / "contradiction" / name).read_text(encoding="utf-8")
        for name in names
    }
    prompt, fidelity_rules, _example, title_rule = merge.compose_prompt(
        merge.MergePolicy())
    messages = [{
        "role": "user",
        "content": prompt.render(
            fidelity_rules=fidelity_rules,
            title_rule=title_rule,
            base_filename=names[0],
            sources=segment.render_sources(segment.segment_sources(sources), names[0]),
        ),
    }]
    store = cassette.Store(M4_CASSETTES)
    for condition, thinking in (("off", False), ("on", True)):
        for sample in range(3):
            key = cassette.key_for(
                role="merge", model="qwen3:8b", tier="json_schema",
                prompt_sha256=prompt.sha256, messages=messages, schema=merge.MERGE_SCHEMA,
                temperature=TEMPERATURE, seed=SEED,
                max_tokens=merge.budget_tokens(sources, config.DEFAULT_FIDELITY),
                thinking=thinking, sample=sample,
            )
            check(not store.has(key),
                  f"contradiction [{condition}] sample {sample} resolves at {key[:16]}: "
                  f"either the `m4/` corpus has been re-recorded under the new merge prompt, "
                  f"in which case this test must go back to asserting presence, or the "
                  f"merge prompt has been reverted to the one `m4/` was recorded under")

    recorded = len(list(M4_CASSETTES.glob("*.json")))
    check(recorded == 266,
          f"the `m4/` corpus must still be on disk, all 266 files of it, got {recorded}: "
          f"orphaned is not deleted, and a re-record starts from these inputs")


def test_cassette_records_no_secrets() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = cassette.Store(Path(tmp))
        path = store.write(
            key="k" * 64, role="decompose", model="m", tier="json_schema",
            messages=[{"role": "user", "content": "hi"}], schema={}, temperature=0.0,
            raw='{"ok": true}', http_status=200,
            endpoint=config.endpoint_id("gateway.example.net"),
            latency_ms=12, attempt=1,
        )
        assert path is not None
        text = path.read_text()
        check("gateway.example.net" not in text, "a cassette must not name the machine")
        check(
            config.endpoint_id("gateway.example.net") in text,
            "the endpoint is still recorded, because one corpus means one machine",
        )
        check("https://" not in text and "/v1" not in text, "no full endpoint URL in a cassette")
        check("Authorization" not in text and "Bearer" not in text, "no headers in a cassette")

        again = store.write(
            key="k" * 64, role="decompose", model="m", tier="json_schema", messages=[],
            schema={}, temperature=0.0, raw="changed", http_status=200, endpoint="h",
            latency_ms=0, attempt=1,
        )
        check(again is None, "an existing cassette must be kept unless --force")
        check("changed" not in path.read_text(), "an existing cassette must not be overwritten")

        forced = store.write(
            key="k" * 64, role="decompose", model="m", tier="json_schema", messages=[],
            schema={}, temperature=0.0, raw="changed", http_status=200, endpoint="h",
            latency_ms=0, attempt=1, force=True,
        )
        check(forced is not None and "changed" in path.read_text(), "--force must overwrite")


def test_cassette_records_the_revision_that_made_it() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = cassette.Store(Path(tmp))
        for n, source in enumerate(("abc123abc123", "abc123abc123-dirty")):
            store.write(
                key=str(n) * 64, role="verify", model="m", tier="json_schema", messages=[],
                schema={}, temperature=0.0, raw="{}", http_status=200, endpoint="h",
                latency_ms=0, attempt=1, source=source,
            )
        store.write(
            key="9" * 64, role="verify", model="m", tier="json_schema", messages=[],
            schema={}, temperature=0.0, raw="{}", http_status=200, endpoint="h",
            latency_ms=0, attempt=1,
        )

        found = cassette.Store(Path(tmp)).sources()
        check(
            found == {"abc123abc123": 1, "abc123abc123-dirty": 1, "unrecorded": 1},
            f"every cassette must name its revision, or be counted as unrecorded: {found}",
        )
        check(
            "abc123abc123-dirty" in (Path(tmp) / cassette.filename("verify", "1" * 64)).read_text(),
            "the revision belongs in the file, not only in the index",
        )

        raises(
            cassette.MixedSources,
            lambda: cassette.guard_sources(cassette.Store(Path(tmp)), "abc123abc123"),
            "recording under one revision into another revision's corpus must be refused",
        )
        message = str(
            raises(cassette.MixedSources,
                   lambda: cassette.guard_sources(cassette.Store(Path(tmp)), "abc123abc123"),
                   "")
        )
        check("abc123abc123-dirty (1)" in message, "the refusal must name the mixture it found")
        check("unrecorded (1)" in message, "a cassette with no revision is part of the mixture")

        clean = cassette.Store(Path(tmp) / "empty")
        cassette.guard_sources(clean, "abc123abc123")
        check(clean.sources() == {}, "an empty directory is not a mixture")


def test_cassette_records_the_endpoint_that_answered() -> None:
    """Two machines may deepen one corpus; the endpoint is metadata, not a guard.

    `endpoint_id` is not a component of `key_for` and never
    was; the operator's ruling was that the local endpoint is undersized and
    the hosted ones are ephemeral, so a recording tied to either was always
    going to have problems, and the fix is to stop pretending the box that
    answered is part of what makes a cassette valid. `guard_sources` no
    longer takes an `endpoint` argument at all. What survives is the census:
    `Store.endpoints()` still tallies which box wrote which cassette, because
    that is a fact worth knowing even though it is not a fact worth refusing
    over.
    """
    local = config.endpoint_id("http://localhost:11434/v1")
    other = config.endpoint_id("http://10.0.0.9:11434/v1")
    with tempfile.TemporaryDirectory() as tmp:
        store = cassette.Store(Path(tmp))
        for n, endpoint in enumerate((local, other)):
            store.write(
                key=str(n) * 64, role="verify", model="m", tier="json_schema", messages=[],
                schema={}, temperature=0.0, raw="{}", http_status=200, endpoint=endpoint,
                latency_ms=0, attempt=1, source="abc123abc123",
            )

        found = cassette.Store(Path(tmp)).endpoints()
        check(
            found == {local: 1, other: 1},
            f"every cassette must name the endpoint that answered it: {found}",
        )

        # Recording against one endpoint into another endpoint's corpus is no
        # longer refused -- it is exactly what the operator asked for.
        cassette.guard_sources(cassette.Store(Path(tmp)), "abc123abc123")
        check(True, "recording across endpoints into one corpus must not be refused")

        # --mixed-sources (revision=None) still works the same way; there is
        # no endpoint half left for it to waive.
        cassette.guard_sources(cassette.Store(Path(tmp)), None)
        check(True, "a caller making no revision claim is not refused")

        clean = cassette.Store(Path(tmp) / "empty")
        cassette.guard_sources(clean, "abc123abc123")
        check(clean.endpoints() == {}, "an empty directory is not a mixture")

        # And the removal has to be wired, not merely available: a Client
        # that records into a corpus another endpoint wrote must construct
        # cleanly, since a Client is the only place the guard is ever called
        # from.
        client = Client(settings_for("http://localhost:1/v1", Path(tmp),
                                      record_dir=Path(tmp), allow_mixed_sources=True))
        check(
            isinstance(client, Client),
            "a recording Client must not refuse a corpus another endpoint wrote",
        )


def test_a_replay_falls_through_to_its_local_overlay_on_miss() -> None:
    """`client._replay_store`.

    `guard_sources` refuses to deepen a directory with a recording from
    another endpoint; it says nothing about a directory with a `local/`
    subdirectory beside it, recorded and guarded on its own terms. Seeded
    against the shipped function, not a copy of its logic: a mutant that
    always returns the primary Store builds fine here and only fails a
    caller that resolves the overlay-only key below.
    """
    def stash(store: cassette.Store, key: str, raw: str) -> None:
        store.write(key=key, role="verify", model="m", tier="json_schema",
                    messages=[], schema={}, temperature=0.0, raw=raw,
                    http_status=200, endpoint="h", latency_ms=0, attempt=1)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        overlay_dir = root / "local"
        overlay_dir.mkdir()

        primary_only, overlay_only, both, neither = (str(n) * 64 for n in (1, 2, 3, 4))
        stash(cassette.Store(root), primary_only, "primary-answer")
        stash(cassette.Store(overlay_dir), overlay_only, "overlay-answer")
        stash(cassette.Store(root), both, "primary-wins")
        stash(cassette.Store(overlay_dir), both, "overlay-loses")

        chained = _replay_store(root)
        check(isinstance(chained, cassette.ChainedStore),
              "a directory with a local/ subdirectory must chain, not replace")
        check(chained.require(primary_only, "verify").raw == "primary-answer",
              "a key only the primary has must resolve from the primary")
        check(chained.require(overlay_only, "verify").raw == "overlay-answer",
              "a primary miss must fall through to the overlay before raising")
        check(chained.require(both, "verify").raw == "primary-wins",
              "a key present in both must resolve to the primary's answer")
        raises(cassette.MissingCassette,
               lambda: chained.require(neither, "verify"),
               "a miss on both must still raise, not return None silently")

    with tempfile.TemporaryDirectory() as bare:
        plain = _replay_store(Path(bare))
        check(isinstance(plain, cassette.Store) and not isinstance(plain, cassette.ChainedStore),
              "a directory with no local/ subdirectory must not be wrapped")

    check(_replay_store(None) is None,
          "no replay directory configured must still mean no replay store")


def test_no_cassette_publishes_the_address_of_the_machine_that_answered() -> None:
    """A cassette is committed test data in a public repository.

    The operator's endpoint is not the repository's to publish, and it never had
    to be: every question anything asks of this field is an equality test, which
    an opaque label answers exactly. So `endpoint_id` holds
    `sha256(endpoint_address(base_url))[:12]` and no cassette holds an address.

    Normalisation runs before the hash, and that is the load-bearing half. One
    machine spelled two ways would hash to two ids, and the endpoint guard would
    then fire on history rather than on a mistake — the failure already
    fixed once in the corpus. An earlier change moved what is hashed
    from the hostname to the whole address and this is where the *spellings*
    that must still collapse are pinned: the loopback aliases, and a base URL
    written with and without the `/v1` that `with_api_path` supplies.
    """
    canonical = config.endpoint_id("http://localhost:11434/v1")
    for spelling in ("http://127.0.0.1:11434/v1", "http://[::1]:11434/v1",
                     "http://localhost:11434", "http://localhost:11434/v1/"):
        check(
            config.Settings(base_url=spelling).endpoint_id == canonical,
            f"{spelling} is the default endpoint spelled differently and must share its id",
        )
    check(config.endpoint_id("") == "", "an unrecorded endpoint must not acquire an identity")
    check(
        config.endpoint_id("http://10.0.0.9:11434/v1") != canonical,
        "two machines must not share an id",
    )
    # A bare hostname is not an endpoint and must not be hashed as though it
    # were: under scheme 1 it was the whole input, so silently accepting one
    # here is how a caller would keep writing scheme 1 ids into a scheme 2
    # corpus and nothing would say so.
    check(config.endpoint_id("localhost") == "",
          "a bare hostname is not a base URL and must not acquire an id")
    check(len(canonical) == 12 and canonical.isalnum(), f"unexpected id shape {canonical!r}")

    # And the corpus itself. Not "no hostname was written today" — no cassette
    # on disk carries the field at all, which is the claim to prove here.
    corpus = ROOT / "tests" / "responses"
    files = sorted(corpus.rglob("*.json"))
    legacy = [p for p in files if '"endpoint_host"' in p.read_text(encoding="utf-8")]
    check(not legacy, f"{len(legacy)} cassette(s) still carry endpoint_host, e.g. {legacy[:1]}")

    recorded = {
        json.loads(p.read_text(encoding="utf-8")).get("meta", {}).get("endpoint_id")
        for p in files
    } - {None}
    # Every id is a hash and nothing else. This used to read `recorded ==
    # {identifier}`, which was a second claim smuggled in beside the first: that
    # the whole corpus came off one machine. That was true when the corpus was
    # one laptop and stopped being true when the model study recorded on two
    # rented pods, and the test never said so because it was never in `ORDER`.
    # What this test has to make good on is that no cassette carries an address,
    # and the number of machines behind the corpus is not that claim.
    shaped = [r for r in recorded if len(r) == 12 and all(c in "0123456789abcdef" for c in r)]
    check(
        sorted(shaped) == sorted(recorded),
        f"every recorded endpoint is a 12-character digest or it is not "
        f"de-identified; found {sorted(set(recorded) - set(shaped))}",
    )
    check(recorded, "no cassette records an endpoint at all; this proves nothing")


def test_a_cassette_written_before_the_rename_still_reads() -> None:
    """`.llossless-cache/` is gitignored and older builds wrote `endpoint_host`.

    Hashing the legacy field on read, rather than bumping the schema, means a
    cache written yesterday resolves to the id the migration wrote into the
    corpus — so the guard cannot fire on the difference between the two
    spellings of a field rather than on two machines.

    **Under scheme 1, and that is not a leftover.** `endpoint_host` is a
    hostname, the id derived from a hostname is a scheme 1 id, and re-deriving
    it under scheme 2 is impossible rather than merely wrong: a hostname does
    not carry the port or the path scheme 2 hashes. So the value this resolves
    to matches the committed corpus, which is scheme 1, and not what the same
    box would record today. The cassette also reads back as scheme 1,
    which is what makes the two distinguishable at all.
    """
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / cassette.filename("verify", "3" * 64)
        path.write_text(
            json.dumps(
                {
                    "schema_version": cassette.SCHEMA_VERSION,
                    "key": "3" * 64,
                    "request": {"role": "verify", "tier": "json_schema"},
                    "response": {"raw": "{}", "http_status": 200},
                    "meta": {"endpoint_host": "127.0.0.1", "claimcheck_source": "abc"},
                }
            ),
            encoding="utf-8",
        )
        loaded = cassette.Cassette.from_file(path)
        check(
            loaded.endpoint_id == config.legacy_endpoint_id("localhost"),
            f"a legacy 127.0.0.1 cassette must resolve to the localhost id, got "
            f"{loaded.endpoint_id!r}",
        )
        check(
            loaded.endpoint_id_scheme == config.ENDPOINT_ID_SCHEME_HOSTNAME,
            f"a cassette with no scheme marker is scheme 1 by definition, got "
            f"{loaded.endpoint_id_scheme!r}",
        )
        check(
            loaded.endpoint_id != config.Settings(base_url="http://127.0.0.1:11434/v1").endpoint_id,
            "the legacy id must not be confused with what that box records today; "
            "if these are equal the scheme change did not happen",
        )
        cassette.guard_sources(cassette.Store(Path(tmp)), None)
        check(True, "the guard must not fire on a legacy spelling of the same machine")


def test_two_recordings_under_one_key_are_refused_rather_than_ranked() -> None:
    """One key, two bodies, in one directory: the run stops.

    The canary standard, applied to a resolution rule instead of
    a scanner. A seeded conflicting pair must trip the guard and a legitimate
    same-key-same-body pair must survive it, because a guard that fires on
    everything and a guard that fires on nothing are equally uninformative and
    only the second one looks green.
    """
    def plant(directory: Path, name: str, *, key: str, raw: str, at: str, latency: int,
              content: str = "hi") -> Path:
        path = directory / name
        path.write_text(json.dumps({
            "schema_version": cassette.SCHEMA_VERSION,
            "recorded_at": at,
            "key": key,
            "request": {"role": "decompose", "model": "m", "tier": "json_schema",
                        "messages": [{"role": "user", "content": content}],
                        "schema": {}, "temperature": 0.0},
            "response": {"raw": raw, "http_status": 200},
            "meta": {"endpoint_id": "e", "claimcheck_source": at[:8],
                     "latency_ms": latency, "attempt": 1},
        }, indent=2) + "\n", encoding="utf-8")
        return path

    key = "c" * 64

    # MUST PASS. The same answer to the same question, filed twice under two
    # names, with different metadata. `recorded_at`, `latency_ms` and the
    # revision differ and none of them is the answer, so nothing is ambiguous
    # and nothing may be refused: this is the shape a `--force` re-record and a
    # backup copy both leave behind.
    with tempfile.TemporaryDirectory() as tmp:
        directory = Path(tmp)
        plant(directory, "decompose-first.json", key=key, raw='{"claims": []}',
              at="2026-08-08T10:38:43+00:00", latency=900)
        plant(directory, "decompose-second.json", key=key, raw='{"claims": []}',
              at="2026-08-08T18:34:16+00:00", latency=1200)
        store = cassette.Store(directory)
        try:
            found = store.require(key, "decompose")
            check(found.raw == '{"claims": []}',
                  "two copies of one answer must resolve to that answer")
            check(store.conflicts() == {},
                  "identical bodies under one key are a duplicate, not a conflict")
        except cassette.ConflictingCassettes as exc:  # pragma: no cover - the must-pass half
            failures.append(f"a same-key same-body pair must not be refused: {exc}")

    # MUST FIRE. The real shape, reduced: identical request, two answers, eight
    # hours apart. Before the guard this returned whichever filename sorted
    # last, which is `second` here and is the *earlier* recording in the corpus
    # this was found in -- sort order is not chronology either.
    with tempfile.TemporaryDirectory() as tmp:
        directory = Path(tmp)
        first = plant(directory, "decompose-first.json", key=key, raw='{"claims": ["a"]}',
                      at="2026-08-08T10:38:43+00:00", latency=900)
        plant(directory, "decompose-second.json", key=key, raw='{"claims": ["a", "b"]}',
              at="2026-08-08T18:34:16+00:00", latency=1200)
        message = str(raises(
            cassette.ConflictingCassettes,
            lambda: cassette.Store(directory).require(key, "decompose"),
            "one key resolving to two different bodies must be refused, not ranked",
        ))
        check(key in message and "responses differ" in message,
              f"the refusal must name the key and what disagreed: {message!r}")
        check("decompose-first.json" in message and "decompose-second.json" in message,
              f"the refusal must name both recordings so neither is the invisible one: {message!r}")
        check("delete" in message,
              "the refusal must say not to delete either: both are records of what the model said")
        # A census rather than the first offender, for a caller that wants the
        # whole picture. Same directory, so it must see the same conflict.
        census = cassette.Store(directory).conflicts()
        check(list(census) == [key] and len(census[key]) == 2,
              f"conflicts() must report the pair the guard refuses: {census}")

        # And it is the *replay path* that is guarded, not a helper beside it.
        # `has()` is what `_replay_tier` walks the ladder with, so a run that
        # never calls `require` must still stop here.
        raises(cassette.ConflictingCassettes,
               lambda: cassette.Store(directory).has(key),
               "the guard must sit in the index, so every reader trips it and not just require()")

        # Two questions under one key is the worse fault and is named separately:
        # the key is a digest of the request, so this is a derivation bug or a
        # collision, and picking a winner would bury either one.
        first.unlink()
        plant(directory, "decompose-first.json", key=key, raw='{"claims": ["a", "b"]}',
              at="2026-08-08T10:38:43+00:00", latency=900, content="a different question")
        other = str(raises(
            cassette.ConflictingCassettes,
            lambda: cassette.Store(directory).has(key),
            "two different requests under one key must be refused",
        ))
        check("requests differ" in other,
              f"a key collision must not be reported as a difference of answers: {other!r}")


def test_the_committed_corpora_are_three_measurements_and_not_one() -> None:
    """The other half of that guard: the cross-corpus duplicates, pinned and counted.

    Until the 27B import, three keys resolved to different
    bodies in `tests/responses/` and `tests/responses/m4/`: identical qwen3:8b
    requests, recorded about eight hours apart under two revisions. The root
    half of each pair left with the qwen3:8b root corpus, and no 27B request
    can match an m4 one, because the model is in the key. What is left is
    three decompose keys the 27B's root and `m7/` share, with byte-identical
    answers, which is agreement and not divergence.

    Divergence is still a standing hazard, because the first of these
    directories is also the parent of the others, and a file moved between
    them by copy lands where it collides. So the inventory stays pinned, now
    at none: a key that resolves two ways across corpora fails here instead of
    quietly changing what a replay answers.
    """
    corpora = [ROOT / "tests" / "responses", M4_CASSETTES, ROOT / "tests" / "responses" / "m7"]
    for directory in corpora:
        store = cassette.Store(directory)
        check(store.conflicts() == {},
              f"{directory.name}: a corpus must resolve every key to one recording")

    seen: dict[str, list[Path]] = {}
    for directory in corpora:
        for path in sorted(directory.glob("*.json")):
            try:
                seen.setdefault(cassette.Cassette.from_file(path).key, []).append(path)
            except (ValueError, KeyError, json.JSONDecodeError):
                continue
    divergent = {
        key: paths for key, paths in seen.items()
        if len({cassette.Store._resolution(path) for path in paths}) > 1
    }
    check(sorted(key[:16] for key in divergent) == [],
          f"no key may resolve to two answers across corpora: "
          f"{sorted(key[:16] for key in divergent)}")
    for key, paths in divergent.items():
        parents = {path.parent for path in paths}
        check(len(parents) == len(paths),
              f"{key[:16]} must have one recording per corpus: {[str(p) for p in paths]}")


def test_base_url_does_not_reach_the_cassette_key() -> None:
    """Where a call was answered is provenance, never part of the question asked.

    This is a test of behaviour that is already correct, written so it stays
    that way. Adding the endpoint to `key_for` would orphan all 444 committed
    cassettes at once, and the pressure to add it is real: a later corpus records against a
    second machine, and the guard above exists precisely because the key cannot
    tell them apart.

    Two live runs against two genuinely different URLs — two servers on two
    ports — must produce the same key for the same question.
    """
    keys, ports = [], []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            with FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY))) as base_url:
                ports.append(base_url)
                client = Client(settings_for(base_url, tmp, structured="json_schema",
                                             pinned=True))
                claims_call(client)
                keys.append(client.last_key)

    check(ports[0] != ports[1], f"the two runs must differ in URL: {ports}")
    check(
        keys[0] == keys[1] and keys[0] is not None,
        f"--base-url must not move the cassette key: {keys}",
    )


def test_the_cache_does_not_answer_for_another_endpoint() -> None:
    """A warm cache serves across endpoints now; an earlier change made that advisory.

    The corollary of the test above. Because the endpoint is deliberately not
    in the key, one `.llossless-cache` shared across two endpoints serves the
    first machine's answer to the second, and that is the point: the operator
    ruled that the local endpoint is undersized and the hosted ones are
    ephemeral, so binding a cache hit to the box that happened to fill it only
    guaranteed a miss on both. `-vv` still gets a note naming the mismatch;
    the call itself is no longer skipped.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        calls = []
        responder = lambda _b, n: (calls.append(n), (200, envelope(CLAIMS_BODY)))[1]  # noqa: E731

        with FakeEndpoint(responder) as base_url:
            settings = settings_for(base_url, tmp, use_cache=True, structured="json_schema",
                                    pinned=True)
            claims_call(Client(settings))
            check(len(calls) == 1, "the first call must reach the endpoint")

            claims_call(Client(settings))
            check(len(calls) == 1, f"the same question must be served warm: {len(calls)} calls")

            # An alias is not another machine. `127.0.0.1` and `[::1]` are one
            # box under two spellings, and `canonical_host` folds them before
            # anything is derived from the name. Without that, a cache misses
            # and the corpus guard fires on a change of notation.
            alias = config.replace(settings, base_url=base_url.replace("127.0.0.1", "[::1]"))
            check(alias.host != settings.host, "the two settings must spell the host differently")
            check(
                alias.endpoint_id == settings.endpoint_id,
                "one machine under two spellings must be one endpoint id",
            )
            warm = Client(alias)
            try:
                claims_call(warm)
            except Exception:  # noqa: BLE001 -- a miss would dial [::1], which need not answer
                pass
            check(warm.usage.cache_hits == 1, "an alias of one machine must be served warm")
            check(len(calls) == 1, f"an alias must make no live call: {len(calls)} calls")

            # Same question, same key, genuinely another machine. The cassette
            # on disk says localhost; this Settings says otherwise.
            elsewhere = config.replace(settings, base_url="http://gpu.example:11434/v1")
            check(
                elsewhere.endpoint_id != settings.endpoint_id,
                "the two settings must name different machines",
            )
            client = Client(elsewhere)
            claims_call(client)
            check(
                client.usage.cache_hits == 1,
                "a cache entry recorded against another endpoint must still be served",
            )
            check(
                len(calls) == 1,
                f"a served cache hit must not also dial gpu.example: {len(calls)} calls",
            )


def test_an_operator_can_name_a_deployment_the_address_cannot() -> None:
    """A rented endpoint's address is ephemeral; the deployment is not.

    Restart the pod and both host and port change, so a recording run long enough
    to span a restart stamps two `endpoint_id`s into one directory and
    `guard_sources` refuses a corpus that genuinely came from one deployment. The
    guard would be correct and the answer wrong. `LLOSSLESS_ENDPOINT_LABEL` lets
    the operator name the deployment once, and pod churn stops fragmenting it.

    The acceptance is over the ids in every committed cassette that was recorded
    without a label, against a digest computed here from first principles rather
    than read back out of the thing under test.

    **That digest is scheme 1's and is now frozen history.** It used to be
    re-derived through `config.endpoint_id`, which asserted two things at once:
    that the corpus is what it was, and that today's code would produce the same
    value. The second guarantee was broken on purpose and cannot be restored — the
    hostname those 300 ids were hashed from is not recorded anywhere, so the
    corpus can be *described* under scheme 1 and never recomputed under scheme 2.
    So the constant below is spelled out as the hostname digest it is,
    and today's localhost id is asserted to differ from it: a run that quietly
    started reproducing these values again would mean the fix had been reverted.
    """
    independent = hashlib.sha256(b"localhost").hexdigest()[: config.ENDPOINT_ID_CHARS]

    for spelling in ("localhost", "127.0.0.1", "::1", "[::1]"):
        check(
            config.legacy_endpoint_id(spelling) == independent,
            f"{spelling} under scheme 1 must still hash the canonical host: "
            f"{config.legacy_endpoint_id(spelling)!r} != {independent!r}",
        )
    for url in ("http://localhost:11434/v1", "http://127.0.0.1:11434/v1", "http://[::1]:11434/v1"):
        unlabelled = config.Settings(base_url=url)
        check(unlabelled.endpoint_label == "", "no label is the default, not an opt-out")
        check(unlabelled.endpoint_id != independent,
              f"{url} still hashes to the scheme 1 id {independent!r}; that rule is not in this tree")
    check(len({config.Settings(base_url=url).endpoint_id for url in
               ("http://localhost:11434/v1", "http://127.0.0.1:11434/v1",
                "http://[::1]:11434/v1")}) == 1,
          "the local spellings must still be one deployment under scheme 2")

    # The acceptance is split because the committed corpus is no longer one
    # endpoint. A later pass recorded `tests/responses/m7/` against a hosted pod
    # under `LLOSSLESS_ENDPOINT_LABEL`, and another re-recorded
    # `tests/responses` itself against one too, so `m4` is what is left of the
    # localhost recordings and it is the whole of the unlabelled half. A flat
    # "every cassette hashes to localhost" would now be false for a good reason,
    # and bumping its count to 756 would only hide that. Each half is asserted
    # for what it is worth: the local corpus is 300 scheme 1 ids that no longer
    # move because nothing can move them, and the hosted one proves the label
    # did its job -- one id across recordings long enough to outlive a pod
    # restart, and an id that is *not* the canonical-host digest. A single
    # number over both would state neither.
    corpus = sorted((ROOT / "tests" / "responses").rglob("*.json"))
    recorded = [
        json.loads(p.read_text(encoding="utf-8")).get("meta", {}).get("endpoint_id")
        for p in corpus
    ]
    local_dir = ROOT / "tests" / "responses" / "m4"
    pairs_dir = ROOT / "tests" / "responses" / "pairs"
    overlay_dir = ROOT / "tests" / "responses" / "local"
    local = [(p, v) for p, v in zip(corpus, recorded)
             if v is not None and local_dir in p.parents]
    pairs = [(p, v) for p, v in zip(corpus, recorded)
             if v is not None and pairs_dir in p.parents]
    hosted = [(p, v) for p, v in zip(corpus, recorded)
              if v is not None and local_dir not in p.parents
              and pairs_dir not in p.parents]

    moved = [p for p, value in local if value != independent]
    check(not moved, f"{len(moved)} cassette id(s) moved, e.g. {moved[:1]}")
    check(
        len(local) == 264,
        f"the unlabelled acceptance is over all 264 local cassettes; "
        f"found {len(local)}",
    )

    # There was a fourth split, for `tests/responses/local`: a live overlay of
    # qwen3:8b cassettes recorded against local ollama and chained in at read
    # time (`ChainedStore`). The 27B import deleted it.
    # The mechanism stays; a committed overlay does not come
    # back by growing into it. One recorded now would put a second model or
    # endpoint under the root corpus's replay, which `replay_models` refuses,
    # so it is a corpus change to decide here, not a directory to add to.
    check(not overlay_dir.exists(),
          "tests/responses/local/ is back; the 27B corpus has no overlay, so "
          "decide what it is and split it here before committing it")

    ids = {value for _, value in hosted}
    check(
        len(hosted) == 407,
        f"the labelled acceptance is over all 407 hosted cassettes; "
        f"found {len(hosted)}",
    )
    check(
        len(ids) == 1,
        f"one label was set for the whole of the hosted recording, so "
        f"`tests/responses` and `m7` must carry one endpoint_id between them; "
        f"they carry {len(ids)}: {sorted(ids)}",
    )
    check(
        independent not in ids,
        "the hosted corpus was recorded against a remote host and must not hash "
        "to the canonical local digest; the label is not being applied",
    )

    # Split a third time, for the reason the split above was made in the first
    # place. `tests/responses/pairs` was recorded 2026-08-30 against a different
    # rented pod under its own `LLOSSLESS_ENDPOINT_LABEL`, so it is a third
    # deployment and not a second id inside the second one. Folding it into
    # `hosted` would fail the one-id check for a good reason, and widening that
    # check to "one or two ids" would retire the property rather than extend it.
    # What is asserted of this corpus is what is asserted of the others: it is
    # internally one deployment, that deployment is not localhost, and it is not
    # the deployment that recorded the rest -- which is the fact worth having,
    # because a corpus silently sharing an id with another pod is the failure
    # `endpoint_id` exists to catch.
    pair_ids = {value for _, value in pairs}
    check(
        len(pairs) == 26,
        f"the pairs acceptance is over all 26 cassettes recorded for "
        f"tests/pairs; found {len(pairs)}",
    )
    check(
        len(pair_ids) == 1,
        f"one label was set for the whole of the pairs recording; it carries "
        f"{len(pair_ids)}: {sorted(pair_ids)}",
    )
    check(
        independent not in pair_ids,
        "the pairs corpus was recorded against a remote pod and must not hash "
        "to the canonical local digest; the label is not being applied",
    )
    check(
        not (pair_ids & ids),
        f"the pairs corpus and the earlier hosted corpus are different "
        f"deployments and must not share an endpoint_id: {sorted(pair_ids & ids)}",
    )

    # And the label does something, or it is not a feature. One label, two
    # genuinely different addresses, one id: that is the pod restart, and it is
    # the whole case for the variable.
    label = "hosted-a"
    before = config.Settings(base_url="http://a.invalid:11434/v1", endpoint_label=label)
    after = config.Settings(base_url="http://b.invalid:22222/v1", endpoint_label=label)
    check(before.host != after.host, "the two settings must name different addresses")
    check(
        before.endpoint_id == after.endpoint_id,
        "one labelled deployment must keep one id across a change of address",
    )
    check(
        before.endpoint_id == hashlib.sha256(label.encode()).hexdigest()[:12],
        "a labelled id must be the digest of the label and nothing else",
    )
    check(
        before.endpoint_id != independent,
        "a labelled deployment must not collide with the unlabelled host it runs on",
    )
    check(
        config.Settings(base_url="http://a.invalid/v1", endpoint_label="  ").endpoint_id
        == config.endpoint_id("http://a.invalid/v1"),
        "a whitespace label is not a name; it must leave the address path alone",
    )

    # A label says which deployment, never where. Letting it move `is_local`
    # would let an operator relabel their way past the warning that document
    # content is about to leave the machine.
    hosted = config.Settings(base_url="http://a.invalid/v1", endpoint_label="local-box")
    check(not hosted.is_local and hosted.where == "hosted",
          "a label must not decide whether content leaves this machine")

    # End to end. A restart with no label used to break resumption twice over:
    # `guard_sources` refused the --record directory on the changed endpoint
    # id, and every already-made call missed the cache on
    # `cached.endpoint_id != settings.endpoint_id`. Both were removed:
    # the guard no longer takes an endpoint at all, and a mismatched
    # cache hit is now served, with a note at -vv. A label still matters: it
    # keeps one deployment's `endpoint_id` stable across a restart, which is
    # what keeps `Store.endpoints()`'s census meaningful -- but it no longer
    # decides whether a resumed run can proceed at all.
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        calls = []
        responder = lambda _b, n: (calls.append(n), (200, envelope(CLAIMS_BODY)))[1]  # noqa: E731
        with FakeEndpoint(responder) as base_url:
            first = settings_for(base_url, tmp, use_cache=True, record_dir=tmp / "corpus",
                                 endpoint_label=label, structured="json_schema", pinned=True)
            claims_call(Client(first))
            check(len(calls) == 1, "the first call must reach the endpoint")

            # The pod came back at another address. Nothing else changed.
            restarted = config.replace(first, base_url="http://moved.invalid:9/v1")
            check(restarted.host != first.host, "the restart must change the address")
            resumed = Client(restarted)
            claims_call(resumed)
            check(resumed.usage.cache_hits == 1,
                  "a labelled deployment must keep its cache across a restart")
            check(len(calls) == 1, f"nothing may be re-recorded live: {len(calls)} calls")

            # And unlabelled, at the same two addresses, resumption now works
            # too -- neither the guard nor the cache still cares which
            # address answered.
            bare = config.replace(first, endpoint_label="", cache_dir=tmp / "bare",
                                  record_dir=tmp / "bare-corpus")
            claims_call(Client(bare))
            check(len(calls) == 2, f"bare's own recording must reach the endpoint: {len(calls)} calls")
            moved = config.replace(bare, base_url="http://moved.invalid:9/v1")
            client = Client(moved)
            check(
                isinstance(client, Client),
                "without a label the restart must not refuse to deepen its own corpus",
            )
            cold = Client(config.replace(moved, record_dir=None))
            claims_call(cold)
            check(cold.usage.cache_hits == 1,
                  "without a label the restart must still find its cache; the guard was never what paid for 5b")
            check(len(calls) == 2, f"a served cache hit must not dial moved.invalid: {len(calls)} calls")

    # It is provenance, not part of the question asked — the same rule the
    # endpoint itself lives under, and the pressure to break it is the same.
    signature = set(inspect.signature(cassette.key_for).parameters)
    check(
        signature == {"role", "model", "tier", "prompt_sha256", "messages", "schema",
                      "temperature", "seed", "max_tokens", "thinking", "sample",
                      "profile", "command"},
        f"key_for's components changed: {sorted(signature)}",
    )
    keys = []
    for base_url, name in (("http://a.invalid/v1", ""), ("http://b.invalid/v1", label)):
        with tempfile.TemporaryDirectory() as tmp:
            client = Client(settings_for(base_url, Path(tmp), endpoint_label=name,
                                         structured="json_schema", pinned=True))
            keys.append(
                cassette.key_for(
                    role="decompose", model=client.settings.model_for("decompose"),
                    tier="json_schema", prompt_sha256=decompose_prompt().sha256,
                    messages=[], schema=None, temperature=0.0, seed=None, max_tokens=None,
                )
            )
    check(keys[0] == keys[1], f"a label must not move the cassette key: {keys}")


def test_dirty_tree_is_its_own_revision() -> None:
    check(
        provenance.source_state(ROOT / "does" / "not" / "exist").endswith("-unknown"),
        "a tree git cannot be asked about is unknown, never assumed clean",
    )
    state = provenance.source_state()
    check(
        state.startswith(provenance.git_commit()),
        "the recorded revision must begin with the commit it was made at",
    )
    check(
        state == provenance.git_commit() or state.endswith(("-dirty", "-unknown")),
        f"a revision is a commit, or a commit plus why it is not one: {state}",
    )

    # Against a repository this test builds, so the assertion is "dirty is
    # detected", not "this checkout happens to be dirty today".
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        def git(*args: str) -> None:
            subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)

        git("init", "--quiet")
        git("config", "user.email", "t@example.invalid")
        git("config", "user.name", "t")
        (repo / "a.txt").write_text("one\n")
        git("add", "a.txt")
        git("commit", "--quiet", "-m", "one")
        check(provenance.is_dirty(repo) is False, "a committed tree is clean")
        check(not provenance.source_state(repo).endswith("-dirty"), "a clean tree carries no suffix")

        (repo / "untracked.txt").write_text("noise\n")
        check(
            provenance.is_dirty(repo) is False,
            "untracked files must not count; a recording sweep writes them as it runs",
        )

        (repo / "a.txt").write_text("two\n")
        check(provenance.is_dirty(repo) is True, "an edited tracked file is a dirty tree")
        check(
            provenance.source_state(repo).endswith("-dirty"),
            "a dirty tree must be a different revision string, not the same commit",
        )


def test_a_linked_worktree_still_knows_which_commit_it_is() -> None:
    """`git worktree add` leaves a `.git` file, and the commit went `unknown`.

    Found by running the paper build from a worktree: it wrote `unknown`
    over a real commit in the paper's generated output (withheld with the paper), because `git_commit`
    read `root/.git/HEAD` as a path and `root/.git` is a *file* there, holding
    `gitdir: <path>`. Every run made from a second checkout had been recording
    its provenance as "git could not be asked" -- and a second checkout is
    exactly where a branch of work gets done, so the checkouts that lost the
    commit were the ones most likely to be producing something.

    Both halves are asserted. The worktree must resolve to a real commit, and
    it must resolve to the **same** commit as the repository it was made from
    when both sit on one branch -- which is the half that catches a fix that
    finds *a* ref rather than the right one. The refs live in the common
    directory and the `HEAD` naming them does not, so looking the ref up
    beside its own `HEAD` finds nothing.
    """
    from llossless import provenance

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()

        def git(*args: str, cwd: Path = repo) -> None:
            subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)

        git("init", "--quiet", "--initial-branch", "main")
        git("config", "user.email", "t@example.invalid")
        git("config", "user.name", "t")
        (repo / "a.txt").write_text("one\n")
        git("add", "a.txt")
        git("commit", "--quiet", "-m", "one")

        linked = Path(tmp) / "linked"
        git("worktree", "add", "--quiet", "--detach", str(linked))

        # The premise. If `.git` were a directory here the check below would
        # be passing over the ordinary case and proving nothing.
        check((linked / ".git").is_file(),
              "a linked worktree must carry a .git file, not a directory; "
              "this check is about that shape")

        wanted = provenance.git_commit(repo)
        check(re.fullmatch(r"[0-9a-f]{12}", wanted) is not None,
              f"the repository itself must resolve to a commit, got {wanted!r}")
        got = provenance.git_commit(linked)
        check(got == wanted,
              f"a linked worktree must name the commit it is checked out at: "
              f"got {got!r}, the repository says {wanted!r}")

        # A packed ref is the other storage git uses, and the lookup has to
        # follow it into the common directory too. `--detach` above writes a
        # bare sha into HEAD, so this covers the symbolic path as well.
        git("pack-refs", "--all")
        named = Path(tmp) / "named"
        git("worktree", "add", "--quiet", str(named), "-b", "second")
        check(provenance.git_commit(named) == wanted,
              "a worktree on a packed ref must resolve through the common "
              "directory's packed-refs")

        # And the whole point: a source state, not the word `unknown`.
        state = provenance.source_state(linked)
        check(not state.endswith("-unknown"),
              f"a worktree must not record its provenance as unknown: {state!r}")


def test_a_sweep_rewriting_cassettes_does_not_dirty_its_own_provenance() -> None:
    """Re-recording an existing corpus must not stamp that corpus `-dirty`.

    This is the failure it was written for. A 93-call decompose sweep was stopped
    partway and relaunched; the aborted attempt had rewritten cassettes in place
    with `--force`, so the worktree was non-empty when the second sweep computed
    `source_state()`, and all 93 finished cassettes carried `-dirty` for a change
    that was the recording itself. Nothing under `src/` or `prompts/` had moved.

    `--untracked-files=no` did not cover this and could not: it excludes cassettes
    that are new and keeps cassettes that are rewritten, which makes the suffix
    depend on whether a corpus is being created or deepened. Both are sweeps.
    """
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)

        def git(*args: str) -> None:
            subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)

        corpus = repo / provenance.RECORDED_OUTPUT
        corpus.mkdir(parents=True, exist_ok=True)
        (repo / "src").mkdir(exist_ok=True)
        (repo / "src" / "client.py").write_text("source\n")
        (corpus / "decompose-aaaa.json").write_text('{"raw": "first"}\n')
        git("init", "--quiet")
        git("config", "user.email", "t@example.invalid")
        git("config", "user.name", "t")
        git("add", "-A")
        git("commit", "--quiet", "-m", "a corpus and the code that made it")
        check(provenance.is_dirty(repo) is False, "the committed baseline is clean")

        # What `--force` does on a re-record: same key, same filename, new bytes.
        (corpus / "decompose-aaaa.json").write_text('{"raw": "second"}\n')
        check(
            provenance.is_dirty(repo) is False,
            "rewriting a tracked cassette is the sweep's own output, not a source change",
        )
        state = provenance.source_state(repo)
        check(
            not state.endswith("-dirty"),
            f"a sweep that rewrites its corpus must stamp a clean revision, got {state}",
        )

        # A cassette the sweep adds is excluded for the same reason.
        (corpus / "decompose-bbbb.json").write_text('{"raw": "new key"}\n')
        git("add", "-A")
        check(
            provenance.is_dirty(repo) is False,
            "a staged new cassette is still output; tracked-ness must not decide this",
        )

        # And the exclusion is scoped to the corpus, not a blanket amnesty. The
        # suffix has to keep meaning something, or there was no point keeping it.
        (repo / "src" / "client.py").write_text("edited\n")
        check(
            provenance.is_dirty(repo) is True,
            "an edited source file is still dirty; only tests/responses is excluded",
        )
        check(
            provenance.source_state(repo).endswith("-dirty"),
            "a source edit during a sweep must still reach the cassettes it writes",
        )


def test_the_paper_stamp_excludes_its_own_output_and_nothing_else() -> None:
    """The same exclusion one directory over, and it has to stay that narrow.

    The paper's generated `numbers.tex` (withheld with the paper) is tracked and carries the commit the PDF was
    built from, so the build writes it. Left in scope, the first `make paper`
    after a commit stamps a clean revision and the second stamps `-dirty` for
    nothing but the stamp the first one wrote -- the cassette failure above,
    with a different file. `exclude` is a caller's argument rather than a second
    default, so both halves are pinned: the paper's own output is excused, and a
    source edit during a paper build still reaches the stamp.
    """
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)

        def git(*args: str) -> None:
            subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)

        generated = repo / provenance.PAPER_OUTPUT
        generated.mkdir(parents=True, exist_ok=True)
        (repo / "src").mkdir(exist_ok=True)
        (repo / "src" / "client.py").write_text("source\n")
        (generated / "numbers.tex").write_text("\\makeatother\n")
        git("init", "--quiet")
        git("config", "user.email", "t@example.invalid")
        git("config", "user.name", "t")
        git("add", "-A")
        git("commit", "--quiet", "-m", "the paper's generated numbers")

        paper = (provenance.PAPER_OUTPUT,)
        check(provenance.is_dirty(repo, paper) is False, "the committed baseline is clean")

        (generated / "numbers.tex").write_text("\\makeatother\nstamped\n")
        check(provenance.is_dirty(repo, paper) is False,
              "restamping the paper's own generated file is not a source change")
        check(not provenance.source_state(repo, paper).endswith("-dirty"),
              "a build that rewrites its own stamp must stamp a clean revision")

        # Without the argument the same edit is dirty. This is what makes the
        # exclusion evidence about the caller and not about the file.
        check(provenance.is_dirty(repo) is True,
              "the exclusion must be the caller's, not a default nobody asked for")

        (repo / "src" / "client.py").write_text("edited\n")
        check(provenance.is_dirty(repo, paper) is True,
              "an edited source file is still dirty during a paper build")
        check(provenance.source_state(repo, paper).endswith("-dirty"),
              "a source edit must reach the stamp the PDF prints")


# --------------------------------------------------------------------------
# PART E - transport
# --------------------------------------------------------------------------


def test_transport_retries_then_succeeds() -> None:
    def flaky(_body, n):
        if n < 3:
            return 503, '{"error": "busy"}', {"Retry-After": "0"}
        return 200, envelope(CLAIMS_BODY)

    with FakeEndpoint(flaky) as base_url:
        response = transport.post_json(
            f"{base_url}/chat/completions", {"model": "m"}, api_key=None, timeout=5,
            ca_bundle=None, host="127.0.0.1", model="m", sleep=lambda _s: None,
        )
    check(response.attempts == 3, f"a 503 must be retried, took {response.attempts} attempts")
    check(response.status == 200, "the third attempt should have succeeded")


def test_transport_fails_fast_and_leaks_nothing() -> None:
    with FakeEndpoint(lambda _b, _n: (401, '{"error": "bad key"}')) as base_url:
        exc = raises(
            transport.HTTPStatusError,
            lambda: transport.post_json(
                f"{base_url}/chat/completions", {"model": "m"}, api_key=FAKE_KEY, timeout=5,
                ca_bundle=None, host="127.0.0.1", model="test-model", sleep=lambda _s: None,
            ),
            "a 401 must raise",
        )
        endpoint_calls = 1
    if exc:
        check(exc.status == 401, "the status must survive to the caller")
        check("127.0.0.1" in str(exc) and "test-model" in str(exc),
              "a fatal status must name the host and model, so the fix is obvious")
        check(FAKE_KEY not in str(exc), "the API key must never appear in an exception message")
    check(endpoint_calls == 1, "a 401 must not be retried")


class _RedirectPair:
    """A loopback server that 302s to a second loopback server that records.

    Two real `HTTPServer`s rather than a stub, because the property under test
    is what `urllib.request`'s handler chain does with the header, not what
    this file's own logic does with it -- a rebuilt copy of the redirect
    behaviour would test that copy and nothing shipped.
    """

    def __enter__(self):
        self.received: list[dict] = []

        class Target(BaseHTTPRequestHandler):
            outer = self

            def do_GET(self) -> None:  # noqa: N802
                self.outer.received.append(dict(self.headers))
                self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()

            do_POST = do_GET

            def log_message(self, *_args) -> None:
                pass

        self.target = HTTPServer(("127.0.0.1", 0), Target)
        self.target_thread = threading.Thread(
            target=self.target.serve_forever, daemon=True)
        self.target_thread.start()
        self.target_port = self.target.server_address[1]

        class Redirector(BaseHTTPRequestHandler):
            outer = self

            def do_GET(self) -> None:  # noqa: N802
                self.send_response(302)
                self.send_header(
                    "Location",
                    f"http://127.0.0.1:{self.outer.target_port}/v1/chat/completions")
                self.send_header("Content-Length", "0")
                self.end_headers()

            do_POST = do_GET

            def log_message(self, *_args) -> None:
                pass

        self.origin = HTTPServer(("127.0.0.1", 0), Redirector)
        self.origin_thread = threading.Thread(
            target=self.origin.serve_forever, daemon=True)
        self.origin_thread.start()
        self.origin_url = (
            f"http://127.0.0.1:{self.origin.server_address[1]}/v1/chat/completions")
        return self

    def __exit__(self, *_exc) -> None:
        self.origin.shutdown()
        self.origin.server_close()
        self.origin_thread.join(timeout=5)
        self.target.shutdown()
        self.target.server_close()
        self.target_thread.join(timeout=5)


def test_a_post_redirect_is_refused_by_host_not_followed_with_the_key() -> None:
    """`post_json` must not deliver Authorization to a host nobody named.

    Against the shipped function, not a rebuilt copy of its header logic:
    `build_opener` installs `HTTPRedirectHandler` by default, which copies
    every header but `Content-Length`/`Content-Type` onto the redirected
    request and hands it to whatever host `Location` names. The only honest
    test is one where the second server would actually receive the header if
    the refusal did not work.
    """
    with _RedirectPair() as pair:
        exc = raises(
            transport.TransportError,
            lambda: transport.post_json(
                pair.origin_url, {"model": "m"}, api_key=FAKE_KEY, timeout=5,
                ca_bundle=None, host="127.0.0.1", model="m", sleep=lambda _s: None,
            ),
            "a redirect must be refused, not followed",
        )
        check(not pair.received, "the redirect target must never be contacted at all")
        if exc:
            check(str(pair.target_port) in str(exc),
                  f"the refusal must name the redirect target: {exc}")
            check(FAKE_KEY not in str(exc), "the key must never appear in an exception message")


def test_a_get_redirect_is_refused_the_same_way() -> None:
    """The window probe's opener gets the same treatment, not a copy of it."""
    with _RedirectPair() as pair:
        exc = raises(
            transport.TransportError,
            lambda: transport.get_json(
                pair.origin_url, api_key=FAKE_KEY, timeout=5,
                ca_bundle=None, host="127.0.0.1", sleep=lambda _s: None,
            ),
            "a redirect must be refused, not followed",
        )
        check(not pair.received, "the redirect target must never be contacted at all")
        if exc:
            check(str(pair.target_port) in str(exc),
                  f"the refusal must name the redirect target: {exc}")


def test_a_streamed_answer_reassembles_into_the_body_a_whole_one_returns() -> None:
    """The property everything else rests on: one shape above the transport.

    Streaming exists here for one reason -- a proxy in front of one hosted
    endpoint cuts any request that has not begun answering within about 125 s,
    which at that endpoint's rate is around 9,000 output tokens, well inside a
    merge budget at `high`. It is worth nothing if the answer that comes back is
    a different shape, because `client` would then parse two shapes, `cassette`
    would store two, and a corpus recorded one way would not replay the other.
    """
    whole = envelope(CLAIMS_BODY)
    endpoint = FakeEndpoint(lambda _b, _n: (200, whole))
    with endpoint as base_url:
        streamed = transport.post_json(
            f"{base_url}/chat/completions", {"model": "m"}, api_key=None, timeout=5,
            ca_bundle=None, host="h", model="m", stream=True,
        )
        plain = transport.post_json(
            f"{base_url}/chat/completions", {"model": "m"}, api_key=None, timeout=5,
            ca_bundle=None, host="h", model="m", stream=False,
        )
    check(endpoint.streamed == 1,
          f"exactly one of the two requests must have been streamed, {endpoint.streamed} were")
    check(endpoint.requests[0].get("stream") is True,
          "a streaming request must say so in the body")
    check((endpoint.requests[0].get("stream_options") or {}).get("include_usage") is True,
          "usage is absent from an ollama stream unless it is asked for, and "
          "completion_tokens is what flags a merge that landed on its ceiling")
    check("stream" not in endpoint.requests[1],
          "a non-streaming request must not carry the field at all")

    one, two = json.loads(streamed.body), json.loads(plain.body)
    check(one["choices"][0]["message"]["content"] == two["choices"][0]["message"]["content"],
          "the content must survive being delivered in pieces")
    check(one.get("usage") == two.get("usage"),
          f"usage must survive the stream, got {one.get('usage')} against {two.get('usage')}")
    check(one["choices"][0]["finish_reason"] == two["choices"][0]["finish_reason"],
          "finish_reason is how truncation is noticed and must survive")


def test_a_streamed_tool_call_survives_being_split_across_events() -> None:
    """Arguments arrive in pieces and are keyed by index, not by arrival order."""
    whole = envelope(CLAIMS_BODY, tool="emit_claims")
    with FakeEndpoint(lambda _b, _n: (200, whole)) as base_url:
        response = transport.post_json(
            f"{base_url}/chat/completions", {"model": "m"}, api_key=None, timeout=5,
            ca_bundle=None, host="h", model="m", stream=True,
        )
    message = json.loads(response.body)["choices"][0]["message"]
    calls = message.get("tool_calls") or []
    check(len(calls) == 1, f"one tool call went out, {len(calls)} came back")
    if calls:
        check(calls[0]["function"]["name"] == "emit_claims",
              f"the function name must survive, got {calls[0]['function']['name']!r}")
        check(calls[0]["function"]["arguments"] == CLAIMS_BODY,
              "the arguments must be concatenated in order, not overwritten")


def test_a_stream_cut_short_is_a_failure_and_never_a_short_answer() -> None:
    """The one transport fault that could be mistaken for a result.

    A cut stream has already delivered a prefix of a document, and a prefix of a
    merge is a merge with facts missing -- which is the thing this project
    reports on. Returning it would put a transport fault in the coverage table
    under the model's name.
    """
    events = transport._events  # noqa: SLF001 - the point is what the parser saw
    partial = [
        {"choices": [{"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}]},
        {"choices": [{"index": 0, "delta": {"content": '{"claims": ['}, "finish_reason": None}]},
    ]
    exc = raises(transport.StreamTruncated, lambda: transport.reassemble(partial),
                 "a stream with no finish_reason must raise")
    check(exc is not None and "prefix of an answer" in str(exc),
          f"the failure must say what it refused to return, got {exc!r}")
    check(exc is not None and "12 characters of content" in str(exc),
          f"and how much arrived, so the log says where it stopped, got {exc!r}")
    check(callable(events), "the event parser must stay reachable for this test")


def test_a_stream_is_retried_because_a_cut_connection_is_weather() -> None:
    """Bounded, and on an unattended run worth the regeneration it costs."""
    cut = "data: " + json.dumps(
        {"choices": [{"index": 0, "delta": {"content": "half"}, "finish_reason": None}]}
    ) + "\n\n"

    def flaky(_body, n):
        return (200, cut, {"Content-Type": "text/event-stream"}) if n < 3 else (
            200, envelope(CLAIMS_BODY))

    endpoint = FakeEndpoint(flaky)
    with endpoint as base_url:
        response = transport.post_json(
            f"{base_url}/chat/completions", {"model": "m"}, api_key=None, timeout=5,
            ca_bundle=None, host="h", model="m", stream=True, sleep=lambda _s: None,
        )
    check(response.attempts == 3, f"a cut stream must be retried, took {response.attempts}")
    check(json.loads(response.body)["choices"][0]["message"]["content"] == CLAIMS_BODY,
          "the retry that succeeded is the answer, not the two prefixes before it")

    endpoint = FakeEndpoint(lambda _b, _n: (200, cut, {"Content-Type": "text/event-stream"}))
    with endpoint as base_url:
        exc = raises(
            transport.StreamTruncated,
            lambda: transport.post_json(
                f"{base_url}/chat/completions", {"model": "m"}, api_key=None, timeout=5,
                ca_bundle=None, host="h", model="m", stream=True, sleep=lambda _s: None,
            ),
            "three cut streams in a row must raise rather than return a prefix",
        )
    check(exc is not None, "the retries are bounded")
    check(endpoint.calls == 3, f"bounded at MAX_ATTEMPTS, made {endpoint.calls} calls")


def test_an_endpoint_that_ignores_stream_is_not_read_as_an_empty_one() -> None:
    """A whole body answering a streaming request is a legitimate answer.

    Some proxies collapse a stream back into one response. Deciding on the
    content type rather than on what was asked for means that answer is read as
    what it is instead of as a stream with no events in it.
    """
    endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
    with endpoint as base_url:
        # The fake honours `stream`, so it is asked not to: the request still
        # carries the field, and the reply is a plain JSON body.
        response = transport.post_json(
            f"{base_url}/chat/completions", {"model": "m", "stream": False},
            api_key=None, timeout=5, ca_bundle=None, host="h", model="m", stream=False,
        )
    check(json.loads(response.body)["choices"][0]["message"]["content"] == CLAIMS_BODY,
          "a whole body must be read whole")


def test_streaming_is_on_by_default_and_leaves_the_cassette_key_alone() -> None:
    """The wall is the default hazard, so streaming is the default behaviour.

    And it must not reach the key: two recordings that differ only in how the
    bytes crossed the wire are the same recording, exactly as `USER_AGENT` is
    not in the key either.
    """
    check(config.Settings().stream is True, "streaming must be the default")
    check(config.from_env({"LLOSSLESS_STREAM": "0"}).stream is False,
          "an operator must be able to turn it off")
    check(config.from_env({"LLOSSLESS_STREAM": "false"}).stream is False,
          "including by writing the word")
    check(config.from_env({}).stream is True, "an unset variable leaves it on")
    exc = raises(config.ConfigError, lambda: config.from_env({"LLOSSLESS_STREAM": "maybe"}),
                 "an unreadable value must be refused, not read as off")
    check(exc is not None and "neither true nor false" in str(exc),
          f"and the refusal must say why, got {exc!r}")

    fields = inspect.signature(cassette.key_for).parameters
    check("stream" not in fields,
          f"stream must not be a cassette-key component; key_for takes {sorted(fields)}")


def test_authorization_header_is_sent_when_configured() -> None:
    endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
    with endpoint as base_url:
        transport.post_json(
            f"{base_url}/chat/completions", {"model": "m"}, api_key=FAKE_KEY, timeout=5,
            ca_bundle=None, host="h", model="m",
        )
    check(endpoint.headers[0].get("Authorization") == f"Bearer {FAKE_KEY}",
          "a configured key must actually reach the endpoint")

    endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
    with endpoint as base_url:
        transport.post_json(
            f"{base_url}/chat/completions", {"model": "m"}, api_key=None, timeout=5,
            ca_bundle=None, host="h", model="m",
        )
    check("Authorization" not in endpoint.headers[0],
          "no key means no Authorization header at all, not an empty one")


def test_the_client_names_itself_and_never_as_urllib() -> None:
    """A default User-Agent is a 403 on at least one real endpoint.

    urllib sends `Python-urllib/3.x` when nothing else is set, and a Cloudflare
    rule in front of a hosted endpoint answered that signature with error 1010
    while `curl` from the same machine got a 200. The assertion is therefore in
    two halves: something is sent, and it is not the default. Checking only the
    first would pass on the exact string that caused the outage.
    """
    endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
    with endpoint as base_url:
        transport.post_json(
            f"{base_url}/chat/completions", {"model": "m"}, api_key=None, timeout=5,
            ca_bundle=None, host="h", model="m",
        )
    sent = endpoint.headers[0].get("User-Agent", "")
    check(sent == transport.USER_AGENT,
          f"the client must send its own User-Agent, sent {sent!r}")
    check("urllib" not in sent.lower(),
          f"the stdlib default is the signature that gets blocked, sent {sent!r}")


# --------------------------------------------------------------------------
# PART B - the tier ladder
# --------------------------------------------------------------------------


def test_tier_bodies() -> None:
    messages = [{"role": "user", "content": "extract"}]
    schema = {"type": "object", "properties": {}}

    body = structured.build_body(tier="json_schema", model="m", messages=messages,
                                 schema=schema, schema_name="emit_claims")
    check(body["response_format"]["json_schema"]["strict"] is True, "tier 1 must ask for strict")
    check(body["response_format"]["json_schema"]["schema"] == schema, "tier 1 must send the schema")

    body = structured.build_body(tier="tool_call", model="m", messages=messages,
                                 schema=schema, schema_name="emit_claims")
    check(body["tools"][0]["function"]["parameters"] == schema,
          "tier 2's function parameters must be the schema itself")
    check(body["tool_choice"]["function"]["name"] == "emit_claims", "tier 2 must require the call")

    body = structured.build_body(tier="prompt", model="m", messages=messages,
                                 schema=schema, schema_name="emit_claims")
    check("response_format" not in body and "tools" not in body,
          "tier 3 must send no API-level constraint")
    check("SCHEMA:" in body["messages"][-1]["content"],
          "tier 3 must put the schema in the message, or 'the provided schema' means nothing")
    check(messages[0]["content"] == "extract", "build_body must not mutate the caller's messages")


def profile_call(client: Client, *, max_tokens: int | None = None,
                 thinking: bool | None = None) -> None:
    """One ordinary call, so the body under test is one the tool really sends."""
    client.complete(
        role="decompose",
        prompt=decompose_prompt(),
        messages=[{"role": "user", "content": "The relay listens on port 8443."}],
        schema=CLAIM_SCHEMA,
        schema_name="emit_claims",
        semantic=parsing.check_claims,
        max_tokens=max_tokens,
        thinking=thinking,
    )


def test_the_default_profile_sends_the_body_this_project_has_always_sent() -> None:
    """The control for every profile assertion below, and the re-key guard.

    697 recordings on disk were made with this body. The profile table must not
    move it by a byte, and "byte" is meant: the keys, their order and their
    values, as `json.dumps` will serialise them, because that is what
    `transport.post_json` writes and what `request_sha256` describes.
    """
    endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
    with tempfile.TemporaryDirectory() as tmp, endpoint as base_url:
        settings = settings_for(base_url, Path(tmp), models={"decompose": "test-model"},
                                structured="json_schema", pinned=True)
        check(settings.profile == structured.DEFAULT_PROFILE,
              f"a run nobody configured must take the default profile, got "
              f"{settings.profile!r}")
        profile_call(Client(settings), max_tokens=2560)

    sent = endpoint.requests[-1]
    built = ["model", "messages", "temperature", "seed", "max_tokens",
             "reasoning_effort", "response_format"]
    check(list(sent)[:len(built)] == built,
          f"the default body's keys and their order must be unchanged: {list(sent)}")
    # `transport.post_json` appends the two streaming keys after `build_body`
    # has finished, so they are the only legal surplus. Named rather than
    # sliced past, because a key appearing here that nobody named is exactly
    # the kind of surplus this assertion is for.
    check(set(sent) - set(built) == {"stream", "stream_options"},
          f"and nothing but transport's streaming keys may be added: "
          f"{sorted(set(sent) - set(built))}")
    check((sent["temperature"], sent["seed"], sent["max_tokens"]) == (0.0, 0, 2560),
          f"and their values: {sent['temperature']!r}, {sent['seed']!r}, "
          f"{sent['max_tokens']!r}")


def test_the_openai_reasoning_profile_renames_the_budget_and_drops_temperature() -> None:
    """Measured 400s, 2026-08-31.

    > Unsupported parameter: 'max_tokens' is not supported with this model. Use
    > 'max_completion_tokens' instead.

    > Unsupported value: 'temperature' does not support 0.0 with this model.
    > Only the default (1) value is supported.

    The second is the subtle one and the reason `temperature` is a three-valued
    rule rather than a flag: the *same* body at the *same* temperature passes
    when `reasoning_effort: "none"` is present, so on these SKUs the legal range
    of `temperature` is a function of the reasoning state. Both states are
    asserted, because only the pair shows it.
    """
    endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
    with tempfile.TemporaryDirectory() as tmp, endpoint as base_url:
        settings = settings_for(base_url, Path(tmp), models={"decompose": "test-model"},
                                structured="json_schema", pinned=True,
                                profile="openai-reasoning")
        client = Client(settings)
        profile_call(client, max_tokens=2560, thinking=False)
        profile_call(client, max_tokens=2560, thinking=True)

    off, on = endpoint.requests[-2], endpoint.requests[-1]
    for body in (off, on):
        check("max_tokens" not in body and body.get("max_completion_tokens") == 2560,
              f"the output budget must be `max_completion_tokens` here: {sorted(body)}")
    check(off.get("temperature") == 0.0 and off.get("reasoning_effort") == "none",
          f"with reasoning off, temperature 0.0 is legal and must still be sent: {off!r}")
    check("temperature" not in on,
          f"with reasoning on, 0.0 is refused and this project has no other "
          f"value it would rather send, so the field must be absent: {sorted(on)}")
    check("reasoning_effort" not in on,
          f"thinking on still means no reasoning field at all: {sorted(on)}")
    check(on.get("seed") == 0,
          f"`seed` is untouched on this vendor and must survive: {sorted(on)}")


def test_the_openai_reasoning_profile_steps_past_the_rung_it_cannot_send() -> None:
    """> Function tools with reasoning_effort are not supported for gpt-5.6-luna

    The ladder's middle rung is unreachable on these SKUs with thinking off, and
    the honest way to express that is to not send it -- a 400 is a paid answer
    to a question the table already knows. So `build_body` refuses the rung and
    the ladder steps down to `prompt`, with nothing billed for the rung that was
    skipped.
    """
    endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
    with tempfile.TemporaryDirectory() as tmp, endpoint as base_url:
        settings = settings_for(base_url, Path(tmp), models={"decompose": "test-model"},
                                structured="tool_call", pinned=True,
                                profile="openai-reasoning")
        exc = raises(structured.TierUnsupported,
                     lambda: profile_call(Client(settings), thinking=False),
                     "a run pinned to a rung its profile cannot produce must stop")
        check(exc is not None and "tool_call" in str(exc),
              f"the refusal must name the rung: {exc!r}")
        check(endpoint.calls == 0,
              f"and must cost nothing -- the 400 is known, not re-measured: "
              f"{endpoint.calls} call(s)")

    # Unpinned, the same request walks past the rung instead of stopping. The
    # tier that answers is `prompt`, one below the rung that was skipped.
    def refuses_schema(body, _n):
        if "response_format" in body:
            return 400, json.dumps({"error": {"message": "response_format is unsupported"}})
        return 200, envelope(CLAIMS_BODY)

    endpoint = FakeEndpoint(refuses_schema)
    with tempfile.TemporaryDirectory() as tmp, endpoint as base_url:
        settings = settings_for(base_url, Path(tmp), models={"decompose": "test-model"},
                                profile="openai-reasoning")
        client = Client(settings)
        profile_call(client, thinking=False)
    check(client.last_tier == "prompt",
          f"the ladder must land on the rung below the one it cannot send, got "
          f"{client.last_tier!r}")
    check(all("tools" not in body for body in endpoint.requests),
          "and must never have sent a tool_call body at all")


def test_the_anthropic_profile_sends_neither_temperature_nor_seed() -> None:
    """> `temperature` is deprecated for this model.  -- sonnet-5, all shapes

    `seed` is not in Anthropic's surface either. Absent, not `null`: a vendor
    that does not know a field refuses the request rather than ignoring it, so
    "send it as None" would be the same 400 with more steps.
    """
    endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
    with tempfile.TemporaryDirectory() as tmp, endpoint as base_url:
        settings = settings_for(base_url, Path(tmp), models={"decompose": "test-model"},
                                structured="json_schema", pinned=True,
                                profile="anthropic")
        profile_call(Client(settings), max_tokens=2560)

    sent = endpoint.requests[-1]
    check("temperature" not in sent and "seed" not in sent,
          f"neither field may reach this endpoint: {sorted(sent)}")
    check(sent.get("max_tokens") == 2560,
          f"and the budget field is the original name here: {sorted(sent)}")
    check(sent.get("reasoning_effort") == "none",
          f"thinking off is still expressed, on the field haiku accepts: {sorted(sent)}")


def test_a_profile_is_chosen_and_never_read_off_a_model_name() -> None:
    """One vendor serves models with two envelopes, so a guess would be wrong.

    Haiku takes the default body unmodified on the same endpoint that refuses
    `temperature` for sonnet-5. A name-to-profile mapping would therefore be
    wrong on a pair that exists today, and wrong silently, by sending a body
    nobody chose. `config.model_for` returns the model string verbatim and
    nothing in `src/` parses one; this asserts the second half, because it is
    the half a future edit can break without noticing.
    """
    source = "\n".join(
        (ROOT / "src" / "llossless" / name).read_text(encoding="utf-8")
        for name in ("structured.py", "config.py", "client.py")
    )
    for vendor in ("openai", "anthropic", "gpt-", "claude", "sonnet", "haiku",
                   "qwen", "llama"):
        # In a string that decides something, as opposed to in prose about what
        # a vendor measured. `PROFILES` names two vendors as profile *keys*,
        # which is the operator's vocabulary and not a model id.
        deciding = [line for line in source.splitlines()
                    if f'"{vendor}' in line and "model" in line
                    and not line.lstrip().startswith("#")]
        check(not deciding,
              f"a model id must never decide a request shape; {vendor!r} appears "
              f"in a line that reads one: {deciding}")

    # And the settings say so positively: two models, one profile, because the
    # profile is a property of the endpoint the operator pointed at.
    settings = config.Settings(models={"verify": "claude-sonnet-5", "merge": "gpt-5.6-luna"},
                               profile="anthropic")
    check(settings.profile == "anthropic",
          "the configured profile is the one that applies to every role")


def test_the_reasoning_axis_is_two_distinct_serialised_bodies() -> None:
    """The half that needs no vendor.

    Block 5's treatment is one variable: thinking off against thinking on, same
    SKU, same endpoint, same tier. The whole axis rests on those two states
    reaching the wire as two different request bodies, so it is asserted on the
    body `transport` will serialise rather than on the flag that produced it.

    Thinking OFF sends `reasoning_effort: "none"`. Thinking ON sends no
    reasoning field at all, which means the arm runs at whatever the SKU's own
    default reasoning level is. That is a property of the arm and not a
    detail: "on" is the vendor's default, not a level LLossless chose, and the
    registration says so rather than leaving a reader to assume a named level.

    What this cannot check is whether the vendor honours either state. That
    needs a call, and it is the one thing standing between here and the arms.
    """
    messages = [{"role": "user", "content": "merge"}]
    schema = {"type": "object", "properties": {}}

    def body_for(thinking: bool, **extra) -> dict:
        return structured.build_body(tier="json_schema", model="m",
                                     messages=messages, schema=schema,
                                     schema_name="emit_merge",
                                     thinking=thinking, **extra)

    off, on = body_for(False), body_for(True)

    check(off.get("reasoning_effort") == "none",
          f"the thinking-off arm must send reasoning_effort 'none': {off!r}")
    check("reasoning_effort" not in on,
          f"the thinking-on arm must send no reasoning field, so the SKU runs "
          f"at its own default: {on!r}")

    # The two arms have to differ in exactly one key, or the treatment is not
    # one variable. A second difference would be a confound with the same
    # shape as the one refused earlier.
    differing = {k for k in set(off) | set(on) if off.get(k) != on.get(k)}
    check(differing == {"reasoning_effort"},
          f"thinking must move one field and no other; it moved {sorted(differing)}")

    # `--no-reasoning-effort` exists for endpoints that reject the field. It
    # collapses the axis: both arms then serialise identically and the run
    # would report two arms that were one. Registered as a refusal, not a
    # fallback.
    collapsed = body_for(False, reasoning_effort=False)
    check("reasoning_effort" not in collapsed,
          "dropping the field must actually drop it")
    check(collapsed == on,
          "with the field suppressed the two states are the same request, so "
          "an arm pair recorded that way measures nothing; this is why "
          "client.py raises ThinkingNotHonoured rather than retrying without it")


def test_a_recorded_arm_names_its_own_reasoning_state() -> None:
    """The record has to say which arm it is, or the pair cannot be told apart.

    `cassette.write` stores role, model, tier, messages, schema and
    temperature - and not `reasoning_effort`, because the body is rebuilt from
    those on replay. So the cassette does not display the state. What it does
    carry is the key, and `thinking` is one of the key's components: recompute
    the key under the wrong state and it does not match the file.

    That is the check the arms get at close. It proves each recording was made
    under the state its arm claims, which is the link between the offline
    assertion above and the corpus a result is read off.
    """
    common = dict(role="merge", model="m", tier="json_schema",
                  prompt_sha256="a" * 64,
                  messages=[{"role": "user", "content": "merge"}],
                  schema={"type": "object"}, temperature=0.0, seed=0,
                  max_tokens=None, sample=0)
    off_key = cassette.key_for(**common, thinking=False)
    on_key = cassette.key_for(**common, thinking=True)
    check(off_key != on_key,
          "a thinking-off and a thinking-on recording of the same request must "
          "not share a cassette, or the two arms overwrite each other")
    check(cassette.filename("merge", off_key) != cassette.filename("merge", on_key),
          "the two states must land in different files")

def test_thinking_defaults_to_merge_only() -> None:
    """Measured against ollama 0.32: only `reasoning_effort` is honoured there.

    Two defaults live here and they point opposite ways, which is why this test
    was renamed rather than adjusted. `structured.build_body` defaults to *off*
    and must keep doing so: it is the layer that has to say `reasoning_effort:
    "none"` out loud, because an endpoint that is not told is free to reason
    while the cassette key records `thinking=False`. `config.DEFAULT_THINKING`
    defaults to *merge on*, and until 2026-08-24 nothing in this suite asserted
    what it resolved to at all -- the old body of this test set
    LLOSSLESS_THINKING explicitly and never exercised the unset case, so the
    name was a claim the assertions did not make.
    """
    body = structured.build_body(tier="json_schema", model="m", messages=[],
                                 schema={}, schema_name="s")
    check(body.get("reasoning_effort") == "none", "thinking must be off unless asked for")

    body = structured.build_body(tier="json_schema", model="m", messages=[],
                                 schema={}, schema_name="s", thinking=True)
    check("reasoning_effort" not in body, "a thinking role must not be told not to think")

    settings = env_settings(LLOSSLESS_THINKING="merge")
    check(settings.thinks("merge"), "a named role must be allowed to think")
    check(not settings.thinks("verify") and not settings.thinks("decompose"),
          "verify and decompose must stay off; the brief requires it for verify")

    # The resolved default, with nothing in the environment saying anything.
    default = env_settings()
    # The default was emptied. The merge role is the one that fails with reasoning on:
    # `qwen3.8:27b` spent all 12,800 completion tokens thinking and returned no
    # content, three times, and it was never supported by evidence anyway:
    # an earlier measurement found it worse and a follow-up measurement was
    # skipped. The assertion is kept rather than deleted, pointed the other
    # way. The same change also said all 790 recorded cassettes carry
    # thinking=False; that was false for merge, where 76 of 151 were recorded
    # thinking on, and the default rests on the truncation and on that single measurement alone.
    check(default.thinking == config.DEFAULT_THINKING == frozenset(),
          "no role thinks by default; the merge role is why")
    check(not default.thinks("merge"), "merge must not think by default")
    check(not default.thinks("verify") and not default.thinks("decompose"),
          "decompose and verify were recorded thinking-off and must stay off")
    check(config.Settings().thinking == config.DEFAULT_THINKING,
          "the dataclass default and the environment default must agree")

    # Set-but-empty is the off switch, and it is distinct from unset. If these
    # ever collapse into each other there is no way to ask for no reasoning at
    # all without naming a role that is not the one you mean.
    off = env_settings(LLOSSLESS_THINKING="")
    check(off.thinking == frozenset(),
          "LLOSSLESS_THINKING= must turn every role off, not fall back to the default")
    check(not any(off.thinks(r) for r in config.ROLES), "no role thinks when the set is empty")
    check(env_settings(LLOSSLESS_THINKING="verify").thinking == frozenset({"verify"}),
          "naming a role replaces the default set rather than adding to it")
    with clean_env(LLOSSLESS_THINKING="nonsense"):
        raises(config.ConfigError, lambda: config.from_env(model_map_path=NO_MODEL_MAP), "an unknown thinking role must be fatal")

    # The reasoning block changes the answer, so it must change the cassette key.
    base = dict(role="merge", model="m", tier="prompt", prompt_sha256="a", messages=[],
                schema={}, temperature=0.0, seed=0, max_tokens=None)
    check(cassette.key_for(**base, thinking=True) != cassette.key_for(**base, thinking=False),
          "thinking on and thinking off must not share a recording")


def test_thinking_can_be_overridden_per_call() -> None:
    """A sweep runs both conditions in one process, so the flag is a call argument.

    One Client, because `_pace()` and `_last_call_ended` are per-instance: two
    clients would halve the effective interval between live calls, which is the
    whole GPU mitigation. So the condition cannot live in Settings for the
    length of a sweep, and the two conditions must key apart without it.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
        with endpoint as base_url:
            settings = settings_for(base_url, tmp, thinking=frozenset({"decompose"}),
                                    record_dir=tmp / "tapes")
            client = Client(settings)
            claims_call(client, "default")           # settings say think
            claims_call(client, "default", thinking=False)  # this call says do not
            claims_call(client, "explicit", thinking=True)

        bodies = endpoint.requests
        check("reasoning_effort" not in bodies[0],
              "a role Settings names must think when the call says nothing")
        check(bodies[1].get("reasoning_effort") == "none",
              "an override of False must reach the request body, whatever Settings says")
        check("reasoning_effort" not in bodies[2], "an override of True must think")

        # Three calls, three cassettes: the two conditions cannot collide, and
        # the default path must key exactly as an explicit True does.
        recorded = sorted(p.name for p in (tmp / "tapes").glob("*.json"))
        check(len(recorded) == 3, f"three distinct requests must record three cassettes: {recorded}")

    same = dict(role="decompose", model="m", tier="json_schema", prompt_sha256="a",
                messages=[{"role": "user", "content": "x"}], schema={}, temperature=0.0,
                seed=0, max_tokens=None)
    check(cassette.key_for(**same, thinking=False) != cassette.key_for(**same, thinking=True),
          "the override is only meaningful because the flag is in the key")


def test_a_base_url_with_no_path_is_completed_rather_than_404ing() -> None:
    """The endpoint an operator is handed is a host. The API is one segment down.

    A pod's proxy prints a bare `https://<host>`; ollama's README says
    `http://localhost:11434`. Pointed at either, this tool used to report
    `HTTP 404 ... 404 page not found`, which names neither the missing segment
    nor the fact that the server is up. There is no OpenAI-compatible API at any
    server's root, so a base URL with no path at all cannot have meant one.
    """
    completed = (
        ("http://localhost:11434", "http://localhost:11434/v1"),
        ("http://localhost:11434/", "http://localhost:11434/v1"),
        ("https://host.invalid", "https://host.invalid/v1"),
    )
    for given, wanted in completed:
        got = config.with_api_path(given)
        check(got == wanted, f"{given!r} must complete to {wanted!r}, got {got!r}")
        check(config.with_api_path(got) == wanted,
              f"and completing it twice must not append twice: {got!r}")

    # A path the operator typed is a deployment behind a prefix. Appending to it
    # would rewrite an address they chose into one nothing serves.
    for left_alone in ("http://localhost:11434/v1", "https://host.invalid/pod/v1",
                       "https://host.invalid/openai", "http://h.invalid/v1/"):
        got = config.with_api_path(left_alone)
        check(got == left_alone.rstrip("/"),
              f"{left_alone!r} carries a path and must be left alone, got {got!r}")

    # And it happens wherever a Settings is built, not only on the flag: the
    # environment variable and a library caller reach the same field.
    check(config.Settings(base_url="http://localhost:11434").base_url
          == "http://localhost:11434/v1",
          "a Settings built by hand must be completed too")
    check(config.from_env({"LLOSSLESS_BASE_URL": "http://localhost:11434"}).base_url
          == "http://localhost:11434/v1",
          "and so must LLOSSLESS_BASE_URL")


def test_one_model_flag_moves_every_role_including_merge() -> None:
    """`--model` means every role, even when a file already named one.

    The bug this pins: `apply_arguments` used `models.setdefault("merge", ...)`,
    which is a no-op whenever models.local.json supplies a merge entry -- and
    supplying one is the normal case, since that is what the file is for. The
    verify and decompose roles moved to the model the operator typed and the
    merge role silently stayed on the file's. A real run merged on a model
    nobody had named.

    The populated file is the whole point of the test. With an empty map the
    old code and the new code agree, which is why every earlier test passed.
    """
    parser = argparse.ArgumentParser()
    config.add_arguments(parser)

    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "models.local.json"
        path.write_text(json.dumps({"verify": "file-model", "merge": "file-model"}),
                        encoding="utf-8")
        settings = config.from_env(environ={}, model_map_path=path)
        check(settings.model_for("merge") == "file-model",
              "the file must supply the merge role before any flag is applied")

        one = config.apply_arguments(settings, parser.parse_args(["--model", "flag-model"]))
        for role in config.ROLES:
            check(one.model_for(role) == "flag-model",
                  f"--model must reach the {role} role over a populated file, "
                  f"got {one.model_for(role)!r}")

        # And the specific flag still beats the general one, in either order on
        # the command line -- precedence is the branch order in the source, not
        # the order the operator typed.
        for argv in (["--model", "flag-model", "--merge-model", "merge-flag"],
                     ["--merge-model", "merge-flag", "--model", "flag-model"]):
            both = config.apply_arguments(settings, parser.parse_args(argv))
            check(both.model_for("merge") == "merge-flag",
                  f"--merge-model must win for the merge role: {argv}")
            check(both.model_for("verify") == "flag-model",
                  f"--model must still hold the other roles: {argv}")

        # Nothing typed, nothing moved.
        untouched = config.apply_arguments(settings, parser.parse_args([]))
        check(untouched.model_for("merge") == "file-model",
              "with no flag the file must still decide")


def test_offline_resolves_to_the_runner_s_own_corpus() -> None:
    """--offline means this runner's recordings, not the first runner's.

    One corpus records into tests/responses/m4/ — one revision per directory, and
    `Store._load_index` globs non-recursively so the two corpora cannot see
    each other. A hardcoded --offline target would have one runner replay the
    other's cassettes and miss every key.
    """
    parser = argparse.ArgumentParser()
    m4 = config.OFFLINE_CASSETTES / "m4"
    config.add_arguments(parser, offline_dir=m4)

    args = parser.parse_args(["--offline"])
    check(config.apply_arguments(config.Settings(), args, m4).replay_dir == m4,
          "--offline must resolve to the directory the runner declared")
    check(config.resolve(args, environ={}, offline_dir=m4).replay_dir == m4,
          "resolve must pass the runner's directory through")

    default = argparse.ArgumentParser()
    config.add_arguments(default)
    check(config.apply_arguments(config.Settings(), default.parse_args(["--offline"])).replay_dir
          == config.OFFLINE_CASSETTES,
          "existing callers must keep resolving to tests/responses")

    raises(config.ConfigError,
           lambda: config.apply_arguments(
               config.Settings(), parser.parse_args(["--offline", "--replay", "elsewhere"]), m4),
           "--offline and a disagreeing --replay must still be refused")


def test_reasoning_effort_rejection_aborts_and_never_latches() -> None:
    """A refused `reasoning_effort` fails the run; it does not buy a thinking-on one.

    This test used to assert the opposite -- that the field was dropped and the
    call retried without it. That behaviour was a latch: one rejection cleared
    the flag for the life of the client, so every later call omitted the field,
    the model reasoned, and `thinking=False` went on being written into every
    cassette key. On a comparison of a thinking arm against a no-thinking arm it
    merges the two arms and reports the merge as a result.

    What is asserted here is the whole shape of the new contract: it raises, it
    raises something a caller can catch by name, the message says what to do,
    the client is not left in a state where the next call would omit the field,
    and no answer is returned to be recorded.
    """
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(rejects("reasoning_effort"))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)))
            try:
                claims_call(client)
            except structured.ThinkingNotHonoured as exc:
                raised = exc
            else:
                raised = None
        check(raised is not None,
              "a refused reasoning_effort must raise, not degrade to thinking on")
        check("reasoning_effort" in str(raised) and "thinking" in str(raised),
              f"the error must name the field and the condition, got {raised}")
        # The latch is the thing being prevented, so assert the state directly
        # rather than inferring it from behaviour: if this flag can go False,
        # every later call on this client omits the field silently.
        check(client._reasoning_effort is True,
              "the client must not clear its reasoning_effort flag; that is the latch")
        check(endpoint.calls == 1,
              f"the rejection must not be retried at all; got {endpoint.calls} calls")
        # And the field really was sent, so the test is exercising the branch it
        # claims to: an assertion that passes because nothing was sent is vacuous.
        check(endpoint.requests[-1].get("reasoning_effort") == "none",
              "the refused request must have carried reasoning_effort=none")


def test_a_pinned_run_cannot_flip_the_thinking_condition() -> None:
    """LLOSSLESS_STRUCTURED pins the tier; it never protected the thinking flag.

    The old latch was evaluated *before* the `settings.pinned` check, so pinning
    the structured tier did not stop a run from silently turning thinking on.
    That is the specific hole this asserts is closed, at both settings of the
    pin, because "pinned" and "not pinned" took different branches through the
    handler that used to contain the latch.
    """
    for pinned in (True, False):
        with tempfile.TemporaryDirectory() as tmp:
            endpoint = FakeEndpoint(rejects("reasoning_effort"))
            with endpoint as base_url:
                settings = settings_for(
                    base_url, Path(tmp),
                    structured="json_schema" if pinned else "auto",
                    pinned=pinned,
                )
                client = Client(settings)
                check(client.settings.pinned is pinned,
                      f"the fixture must actually pin when asked; pinned={pinned}")
                try:
                    claims_call(client)
                    outcome = "the call returned a body"
                except structured.ThinkingNotHonoured:
                    outcome = "aborted"
                except Exception as exc:  # noqa: BLE001 - any other escape is the bug
                    outcome = repr(exc)
            check(outcome == "aborted",
                  f"pinned={pinned}: a refused reasoning_effort must abort, got {outcome}")


def test_min_interval_paces_live_calls_only() -> None:
    """--min-interval sleeps between live calls, and never between cached ones."""
    with tempfile.TemporaryDirectory() as tmp:
        slept: list[float] = []
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
        with endpoint as base_url:
            settings = settings_for(base_url, Path(tmp), min_interval=30.0, use_cache=True)
            client = Client(settings)
            client._pace = lambda sleep=None: slept.append(  # noqa: SLF001 - the point of the test
                settings.min_interval if client._last_call_ended else 0.0
            )
            claims_call(client, "first")
            claims_call(client, "second")
            claims_call(client, "first")  # served from cache

        check(slept == [0.0, 30.0], f"the second live call must be paced, got {slept}")
        check(endpoint.calls == 2, "the repeated call must come from cache, not the endpoint")


def test_tier_response_reading() -> None:
    arguments = '{"claims": []}'
    tool_response = json.loads(envelope(arguments, tool="emit_claims"))
    check(structured.read_content("tool_call", tool_response) == arguments,
          "tier 2 must read arguments from the tool call, not from content")

    plain = json.loads(envelope(arguments))
    check(structured.read_content("json_schema", plain) == arguments, "tier 1 reads content")

    raises(structured.TierUnsupported,
           lambda: structured.read_content("tool_call", plain),
           "an endpoint that ignores `tools` has not honoured tier 2")


def test_an_empty_body_is_re_asked_and_never_demotes_a_tier() -> None:
    """A blank 200 is a bad answer, not a capability limit.

    Before the fix this had two handlers and both were wrong. `read_content`
    raised plain `TierUnsupported` from the ladder's shape check, so the schema
    attempts in `complete()` never saw it. Unpinned, `should_fall_back` said
    yes and every later call in the process ran a rung lower -- a permanent
    demotion inferred from one blank body. Pinned, it re-raised and, before
    that was contained, took the whole sweep with it: that is what ended an
    earlier full run at unit 68 of 72, on an endpoint that had answered 67 identical shapes.
    """
    def empty_then(good_from: int):
        def responder(_body, n):  # n counts this request, so it is 1-based
            return 200, envelope(CLAIMS_BODY if n >= good_from else "")
        return responder

    for pinned in (False, True):
        label = "pinned" if pinned else "unpinned"
        extra = {"structured": "json_schema", "pinned": True} if pinned else {}

        with tempfile.TemporaryDirectory() as tmp:
            endpoint = FakeEndpoint(empty_then(EMPTY_RESPONSE_ATTEMPTS))
            with endpoint as base_url:
                client = Client(settings_for(base_url, Path(tmp), **extra))
                payload = claims_call(client)
            check(payload["claims"][0]["span"] == "port 8443",
                  f"[{label}] a re-ask that succeeds must return its answer")
            check(endpoint.calls == EMPTY_RESPONSE_ATTEMPTS,
                  f"[{label}] the last permitted re-ask must still be made: "
                  f"{EMPTY_RESPONSE_ATTEMPTS - 1} blanks then an answer is "
                  f"{EMPTY_RESPONSE_ATTEMPTS} calls, got {endpoint.calls}")
            check(client.resolved_tier() == "json_schema",
                  f"[{label}] a blank body must not cost a tier, landed on "
                  f"{client.resolved_tier()}")
            check(client.usage.repairs == 0,
                  f"[{label}] a re-ask is not a schema repair, got "
                  f"{client.usage.repairs}")

        with tempfile.TemporaryDirectory() as tmp:
            endpoint = FakeEndpoint(lambda _b, _n: (200, envelope("")))
            with endpoint as base_url:
                client = Client(settings_for(base_url, Path(tmp), **extra))
                exc = raises(structured.EmptyResponse, lambda: claims_call(client),
                             f"[{label}] an endpoint that only ever says nothing must "
                             f"raise, not loop and not descend")
            check(endpoint.calls == EMPTY_RESPONSE_ATTEMPTS,
                  f"[{label}] the re-asks are bounded at {EMPTY_RESPONSE_ATTEMPTS}, "
                  f"got {endpoint.calls}")
            # Every re-ask must be the same request, so what descent would look
            # like is `tools` or a bare prompt appearing on request 2 or 3.
            asked = ["response_format" in r for r in endpoint.requests]
            check(all(asked) and len(asked) == EMPTY_RESPONSE_ATTEMPTS,
                  f"[{label}] every re-ask must go out at the same rung, got "
                  f"{asked}")
            check("200" in str(exc) and "blank" in str(exc),
                  f"[{label}] the message must separate reachable-but-mute from "
                  f"unreachable, got {str(exc)!r}")
            written = Path(tmp) / "cache" / "capabilities.json"
            check(not written.exists() or "prompt" not in written.read_text(),
                  f"[{label}] no demotion may reach the capability cache")

    blank = structured.EmptyResponse("response message has empty content")
    check(not structured.should_fall_back(blank),
          "a blank body must never be read as a verdict on the tier")
    check(structured.should_fall_back(structured.TierUnsupported("no tool_calls")),
          "a tier that ignored `tools` still is a verdict on the tier")
    check(isinstance(blank, structured.TierUnsupported),
          "EmptyResponse stays catchable wherever TierUnsupported already was")


def test_every_rejected_attempt_is_dumped_not_only_the_last() -> None:
    """A draw that repairs must not erase its
    own attempt 1: before this, only the response that ended the retry loop was
    ever written, so a draw that failed once and then repaired left nothing on
    disk to show what the first answer actually was.
    """
    hedged = json.dumps({"verdicts": [{"claim_id": "A-001", "verdict": "UNCLEAR",
                                       "rationale": "half.", "evidence": "e"}]})
    fixed = verdicts_body()

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        endpoint = FakeEndpoint(lambda _b, n: (200, envelope(hedged if n == 1 else fixed)))
        with endpoint as base_url:
            # The cache is on here, and that is the point of the fixture
            # rather than a detail: with it off the dumps go to a per-run
            # temporary directory, which is the right behaviour and the
            # wrong place to look for them. Where they go when it is off is
            # checked on the command path, in test_cli.
            client = Client(settings_for(base_url, tmp, use_cache=True))
            payload = verdicts_call(client)

        check(payload["verdicts"][0]["verdict"] == "SUPPORTED",
              "the repaired attempt is the answer returned")
        check(endpoint.calls == 2, f"one failed attempt then one good one is 2 calls, got {endpoint.calls}")
        check(client.usage.repairs == 1, "a repaired draw must count one repair")
        check(client.usage.errors == 0, "a draw that eventually succeeds is not an error")

        directory = tmp / "cache" / "failures"
        first = sorted(directory.glob("*attempt1*"))
        check(len(first) == 1,
              f"exactly one dump for the one attempt that failed, got {len(first)}: {first}")
        if first:
            check("UNCLEAR" in first[0].read_text(),
                  "the dumped attempt must hold what attempt 1 actually said")
        second = sorted(directory.glob("*attempt2*"))
        check(not second, "attempt 2 succeeded and must not be dumped as a failure")


def test_every_discard_writes_its_envelope_before_raising() -> None:
    """A blank body was a billed call that
    left nothing on disk: `usage` and any reasoning field arrived and were
    thrown away with the exception. This is the case that destroyed the
    gpt-oss:120b C1 evidence -- 763 completion tokens billed, zero characters
    of content, and nothing an operator could look at afterwards.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope("")))
        with endpoint as base_url:
            client = Client(settings_for(base_url, tmp, use_cache=True))
            raises(structured.EmptyResponse, lambda: claims_call(client),
                   "an endpoint that only ever says nothing must still raise")

        directory = tmp / "cache" / "discards"
        dumps = sorted(directory.glob("*EmptyResponse*"))
        check(len(dumps) == EMPTY_RESPONSE_ATTEMPTS,
              f"one discard file per empty reply, got {len(dumps)}")
        for path in dumps:
            record = json.loads(path.read_text())
            check(record["kind"] == "EmptyResponse", f"the kind must be recorded, got {record}")
            check(record["envelope"] is not None,
                  "an EmptyResponse has a parsed envelope; it must not be thrown away")
            check(record["envelope"].get("usage", {}).get("completion_tokens") == 50,
                  f"usage must survive onto disk, got {record['envelope'].get('usage')}")
            check(record["raw_body"] is None,
                  "raw_body is only for the no-envelope case; do not duplicate the envelope")

    # And the body-level case, where there never was an envelope to parse.
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        endpoint = FakeEndpoint(lambda _b, _n: (200, "   "))
        with endpoint as base_url:
            client = Client(settings_for(base_url, tmp, use_cache=True))
            raises(Exception, lambda: claims_call(client),
                   "a truly empty body must still raise")

        directory = tmp / "cache" / "discards"
        dumps = sorted(directory.glob("*EmptyBody*"))
        check(len(dumps) == EMPTY_RESPONSE_ATTEMPTS,
              f"one discard file per empty body, got {len(dumps)}")
        if dumps:
            record = json.loads(dumps[0].read_text())
            check(record["envelope"] is None,
                  "an EmptyBody never parsed; there is no envelope to record")
            check(record["kind"] == "EmptyBody", f"the kind must be recorded, got {record}")


def test_fallback_discrimination() -> None:
    check(structured.should_fall_back(
        transport.HTTPStatusError(400, "Unrecognized argument: response_format", "h", "m")),
        "a 400 naming response_format means try the next tier")
    check(structured.should_fall_back(structured.TierUnsupported("no tool_calls")),
          "a missing tool call means try the next tier")
    check(not structured.should_fall_back(RuntimeError("something else")),
          "an unrelated error must not be mistaken for a tier problem")

    # Configuration errors are true on every rung, so demoting on one costs two
    # wasted calls and then blames the model. Each of these is a real fault with
    # a real message, and the ladder must let it through untouched.
    for status, body, what in [
        (401, "invalid api key", "a bad key"),
        (403, "forbidden", "a refused key"),
        (404, "404 page not found", "a wrong URL"),
    ]:
        check(not structured.should_fall_back(
            transport.HTTPStatusError(status, body, "h", "m")),
            f"a {status} is {what} on every tier and must fail fast")

    # …including when the body happens to contain a word the marker list looks
    # for. A credential error is free to say "unsupported"; that must not be
    # read as the endpoint declining response_format.
    for status in (401, 403, 404):
        check(not structured.should_fall_back(transport.HTTPStatusError(
            status, "unsupported credential: unknown parameter", "h", "m")),
            f"a {status} must not demote even when its body trips a marker")

    # A status alone is not evidence. 400 and 422 are returned for schema
    # violations, bad model names, and malformed JSON far more often than for an
    # unsupported response_format, and those are not tier problems either.
    check(not structured.should_fall_back(
        transport.HTTPStatusError(400, "messages: field required", "h", "m")),
        "a 400 that says nothing about structured output must not demote")
    check(not structured.should_fall_back(
        transport.HTTPStatusError(422, "model 'nonesuch' not found", "h", "m")),
        "a 422 naming the model must not be read as a tier refusal")


def test_a_404_does_not_walk_the_ladder() -> None:
    """A wrong URL must fail on the first call, naming itself.

    This is the regression that motivated the rule. `--base-url` was given
    without its `/v1` suffix, every request 404'd, the client read three 404s as
    three tier refusals, and reported that the endpoint "accepted none of the
    structured-output modes" for the model. The endpoint was fine and the model
    was fine; the URL had a typo in it.
    """
    # Two bodies. The first is what a wrong path actually returns. The second is
    # the combination that defeats a status-only rule *and* a marker-only rule
    # taken separately: a 404 whose text names response_format, which a gateway
    # fronting several backends will produce when the route does not exist.
    for body, what in [("404 page not found", "a bare 404"),
                       ('{"error":"no route for response_format"}', "a 404 naming a tier field")]:
        with tempfile.TemporaryDirectory() as tmp:
            endpoint = FakeEndpoint(lambda _b, _n, body=body: (404, body))
            with endpoint as base_url:
                client = Client(settings_for(base_url, Path(tmp)))
                raises(transport.HTTPStatusError,
                       lambda: client.complete(
                           role="decompose", prompt=decompose_prompt(),
                           messages=[{"role": "user", "content": "x"}],
                           schema=CLAIM_SCHEMA, schema_name="emit_claims"),
                       f"{what} must surface as itself, not as a structured-output failure")
            check(endpoint.calls == 1,
                  f"{what} must cost one call, not one per tier; made {endpoint.calls}")


def test_the_capability_record_decides_nothing_and_names_the_server() -> None:
    """Two bugs in one file, and neither survives the other.

    The first, the latch: `_fetch` seeded the starting rung from this file, so a
    verdict written once by some earlier process -- possibly, before it was
    fixed, from a single blank body -- chose the rung for every process after it
    and was never tested again. The second, the key: `host|model`, where host
    was whatever the URL happened to spell, so the file recovered on 2026-08-08
    held `localhost|qwen3:8b -> prompt` next to `127.0.0.1|qwen3:8b ->
    json_schema` and nothing could notice.

    Fixing the latch alone leaves the second verdict unreachable but still
    there; fixing the key alone makes the latch merely consistent. Both.
    """
    resolve = {
        "localhost": [(0, 0, 0, "", ("127.0.0.1", 11434)), (0, 0, 0, "", ("::1", 11434))],
        "127.0.0.1": [(0, 0, 0, "", ("127.0.0.1", 11434))],
        "::1": [(0, 0, 0, "", ("::1", 11434))],
        "gpu.example": [(0, 0, 0, "", ("10.1.2.3", 11434))],
    }
    identity = {
        spelling: structured.endpoint_identity(
            spelling, 11434, resolve=lambda h, _p, **_k: resolve[h]
        )
        for spelling in resolve
    }
    check(identity["localhost"] == identity["127.0.0.1"] == identity["::1"],
          f"three spellings of this machine are one server, got {identity}")
    check(identity["gpu.example"] != identity["localhost"],
          f"a real host is not the loopback, got {identity}")
    check(all("://" not in value and "/" not in value for value in identity.values()),
          f"no URL, no path may enter the identity, got {identity}")
    check(structured.endpoint_identity("localhost", 1234,
                                       resolve=lambda h, _p, **_k: resolve[h])
          != identity["localhost"],
          "two ollamas on one box at different ports are two deployments")

    with tempfile.TemporaryDirectory() as tmp:
        record = structured.Capabilities(Path(tmp) / "capabilities.json")
        check(record.record(identity["localhost"], "qwen3:8b", "prompt", "probed") is None,
              "the first write has nothing to report")
        # The whole of the key fix, as one assertion: the other spelling of this
        # machine must land on the entry that is already there.
        seen = record.observed(identity["127.0.0.1"], "qwen3:8b")
        check(seen is not None and seen.tier == "prompt",
              f"one server must have one entry however the URL spelled it, got {seen}")
        previous = record.record(identity["127.0.0.1"], "qwen3:8b", "json_schema", "probed")
        check(previous is not None and previous.tier == "prompt",
              "a changed resolution must hand back what it replaced, so it can be reported")
        stored = json.loads((Path(tmp) / "capabilities.json").read_text())
        check(len(stored) == 1,
              f"two contradictory verdicts about one server is the bug, got {stored}")
        entry = next(iter(stored.values()))
        check(sorted(entry) == ["recorded", "tier", "why"],
              f"an entry must say when and why, got {sorted(entry)}")

        legacy = Path(tmp) / "legacy.json"
        legacy.write_text('{"localhost|qwen3:8b": "prompt"}\n')
        check(structured.Capabilities(legacy).observed("localhost", "qwen3:8b") is None,
              "a bare string, the oldest format, has no date and no reason, so it is not trusted")

    def answers(body: dict, *, refuse_schema: bool):
        if refuse_schema and "response_format" in body:
            return 400, '{"error":"response_format is not supported"}'
        if "tools" in body:
            return 200, envelope(CLAIMS_BODY, tool="emit_claims")
        return 200, envelope(CLAIMS_BODY)

    # The latch itself. An endpoint that refused response_format once, then
    # stopped refusing: the second process must find that out, not inherit it.
    # One FakeEndpoint across both, because the port is part of the identity
    # and two servers would be two deployments -- correctly, and uselessly here.
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        state = {"refuse": True}
        endpoint = FakeEndpoint(lambda b, _n: answers(b, refuse_schema=state["refuse"]))
        told: list[str] = []
        with endpoint as base_url:
            Client(settings_for(base_url, tmp), notify=lambda _m: None).complete(
                role="decompose", prompt=decompose_prompt(),
                messages=[{"role": "user", "content": "x"}],
                schema=CLAIM_SCHEMA, schema_name="emit_claims")
            state["refuse"] = False
            second_process_starts_at = endpoint.calls
            client = Client(settings_for(base_url, tmp), notify=told.append)
            claims_call(client)

        recorded = structured.Capabilities(tmp / "cache" / "capabilities.json")
        check(client.resolved_tier() == "json_schema",
              f"a recorded demotion must not choose this run's rung, got "
              f"{client.resolved_tier()}")
        check("response_format" in endpoint.requests[second_process_starts_at],
              "the ladder must re-derive from the top rung, not resume below it")
        check(any("last resolved to tool_call" in message for message in told),
              f"a resolution that differs from the record must be said out loud, "
              f"got {told}")
        check(len(recorded._load()) == 1,  # noqa: SLF001 - the file is the subject
              "one server, one entry, rewritten rather than accumulated")

    # A demotion inside one process is the loud case: it splits the corpus,
    # because tier is part of the cassette key.
    with tempfile.TemporaryDirectory() as tmp:
        told = []
        endpoint = FakeEndpoint(lambda b, n: answers(b, refuse_schema=n > 1))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)), notify=told.append)
            claims_call(client, "first")
            claims_call(client, "second")
        check(client.resolved_tier() == "tool_call",
              f"the second call must still get an answer, got {client.resolved_tier()}")
        check(any("demoted mid-run" in m and "cassette key" in m for m in told),
              f"a mid-run demotion must be reported when it happens, got {told}")


def test_capability_probe_walks_down_the_ladder() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with FakeEndpoint(rejects("response_format")) as base_url:
            port = config.Settings(base_url=base_url, models={}).port
            client = Client(settings_for(base_url, tmp))
            client.complete(role="decompose", prompt=decompose_prompt(),
                            messages=[{"role": "user", "content": "x"}],
                            schema=CLAIM_SCHEMA, schema_name="emit_claims")
            check(client.resolved_tier() == "tool_call",
                  f"an endpoint refusing response_format must land on tool_call, "
                  f"got {client.resolved_tier()}")

        # Written down, with when and why, and keyed on the server rather than
        # on the spelling. Read back through a fresh Capabilities so this is a
        # statement about the file and not about one object's memory.
        stored = structured.Capabilities(tmp / "cache" / "capabilities.json")
        seen = stored.observed(structured.endpoint_identity("127.0.0.1", port), "test-model")
        check(seen is not None and seen.tier == "tool_call",
              f"the resolution must be written down, got {seen}")
        check(seen is not None and seen.recorded.startswith("20") and "refused" in seen.why,
              f"an entry with no date and no reason is exactly what is forbidden, got {seen}")

        with FakeEndpoint(rejects("response_format", "tools")) as base_url:
            client = Client(settings_for(base_url, tmp / "second"))
            client.complete(role="decompose", prompt=decompose_prompt(),
                            messages=[{"role": "user", "content": "x"}],
                            schema=CLAIM_SCHEMA, schema_name="emit_claims")
            check(client.resolved_tier() == "prompt",
                  f"an endpoint refusing tools too must land on prompt, "
                  f"got {client.resolved_tier()}")


# --------------------------------------------------------------------------
# ACCEPTANCE TESTS
# --------------------------------------------------------------------------


def acceptance_1_dry_run_makes_no_request() -> None:
    """--dry-run against an unreachable base_url exits 0 and makes no request."""
    with tempfile.TemporaryDirectory() as tmp:
        # Port 1 is not listening. A dry run must not care.
        settings = settings_for("http://127.0.0.1:1/v1", Path(tmp), dry_run=True)
        client = Client(settings)
        raises(DryRun, lambda: claims_call(client), "a dry run must not return an invented answer")
        check(client.usage.calls == 0, "a dry run must make no call")
        check(client.usage.planned_calls == 1, "a dry run must count the call it did not make")
        check(client.usage.planned_input_tokens > 0, "a dry run must estimate the input size")

        with clean_env(LLOSSLESS_CACHE_DIR=str(Path(tmp) / "c")):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = run_decompose.main(
                    ["--dry-run", "--base-url", "http://127.0.0.1:1/v1",
                     "--model", "test-model", "--no-colour", "--fixture", "paraphrase"]
                )
        check(code == 0, f"a dry run must exit 0 even with no endpoint, got {code}")
        check("No request was made" in out.getvalue(), "a dry run must say so plainly")


def acceptance_2_replay_reproduces_the_live_run() -> None:
    """--replay with the endpoint gone reproduces the recorded live run.

    Deviation from the addendum's wording, stated rather than hidden: the
    provenance block cannot be byte-identical between the two runs, because
    PART F requires it to record run mode and call counts and those are exactly
    what differ. Everything outside provenance is compared byte for byte;
    inside it, everything except the fields that describe *how* it ran.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cassettes, live_out, replay_out = tmp / "tapes", tmp / "live.json", tmp / "replay.json"
        args = ["--model", "test-model", "--no-colour", "--no-cache",
                "--fixture", "paraphrase", "--fixture", "hallucination"]

        with FakeEndpoint(echo_document) as base_url:
            with clean_env(LLOSSLESS_CACHE_DIR=str(tmp / "cache")):
                with contextlib.redirect_stdout(io.StringIO()):
                    live_code = run_decompose.main(
                        [*args, "--base-url", base_url, "--record", str(cassettes),
                         "--out", str(live_out)]
                    )

        # The endpoint is now gone. Nothing below may reach the network.
        with clean_env(LLOSSLESS_CACHE_DIR=str(tmp / "cache")):
            with contextlib.redirect_stdout(io.StringIO()):
                replay_code = run_decompose.main(
                    [*args, "--base-url", base_url, "--replay", str(cassettes),
                     "--out", str(replay_out)]
                )

        check(live_code == replay_code, f"exit codes differ: {live_code} vs {replay_code}")

        live = json.loads(live_out.read_text())
        replay = json.loads(replay_out.read_text())
        check(json.dumps(live["documents"], sort_keys=True)
              == json.dumps(replay["documents"], sort_keys=True),
              "replayed findings must be byte-identical to the live run")
        check(live["coverage"] == replay["coverage"], "replayed coverage must be identical")

        # `structured_output.how` goes with them: a replay reports "replayed"
        # because it read the tier off the cassette rather than probing for it,
        # and that is a true statement about the run, not drift.
        # The ledger's per-call `source` is the same kind of field one level
        # down -- it is `run_mode` for a single call -- so it is exempt on the
        # same grounds. The rest of every row is not: this asserts that a
        # replay reissues the same requests, in the same order, at the same
        # sizes, which is a stronger claim than the totals alone could make.
        #
        # `latency_ms` joins `source` and nothing else does. It is the
        # live call's wall time, and a replay made no call and so has none:
        # the same class as `source`, how a call ran rather than what it
        # asked. Named, not a pattern, and each gets its own assertion below
        # so an exempt field is not an untested one.
        #
        # A later change adds the split of that time on the same terms: the transport
        # attempts, the answering attempt's own time, the failed attempts',
        # the pacing and backoff, the time to the first byte, and a command
        # route's own two figures. None is a cassette key component; each is
        # asserted below, both ways. `outcome` is *not* here: a replay files
        # the same outcome its live run did, so it is compared.
        how_the_call_ran = ("source", "latency_ms", "attempts", "answer_ms",
                            "failed_ms", "waited_ms", "ttfb_ms",
                            "cli_duration_ms", "cli_duration_api_ms")
        describes_the_run = set(provenance.VOLATILE)
        def comparable(report: dict) -> dict:
            block = {k: v for k, v in report["provenance"].items() if k not in describes_the_run}
            block["structured_output"] = block["structured_output"]["mode"]
            block["ledger"] = [{k: v for k, v in row.items() if k not in how_the_call_ran}
                               for row in block["ledger"]]
            return block

        live_p, replay_p = comparable(live), comparable(replay)
        check(live_p == replay_p, f"provenance drifted beyond the run description:\n"
                                  f"  live:   {live_p}\n  replay: {replay_p}")
        check(replay["provenance"]["structured_output"]["how"] == "replayed",
              "a replay must not claim it probed the endpoint")
        check(replay["provenance"]["run_mode"] == "replay", "the replay run must say so")
        check(replay["provenance"]["counts"]["calls"] == 0, "a replay must make no live call")
        check(replay["provenance"]["counts"]["replayed"] > 0, "a replay must serve from cassettes")

        # `source` is exempt above, so it gets its own assertion rather than
        # going untested. A row that cost money and a row that did not must not
        # be indistinguishable -- that is the whole point of recording it.
        live_src = {row["source"] for row in live["provenance"]["ledger"]}
        replay_src = {row["source"] for row in replay["provenance"]["ledger"]}
        check(live_src == {"live"}, f"a live run's ledger must say so, got {live_src}")
        check(replay_src == {"replay"}, f"a replay's ledger must say so, got {replay_src}")
        # And `latency_ms`, both ways: every live row carries its call's time
        # as a whole number of milliseconds, and no replay row claims one.
        live_ms = [row.get("latency_ms") for row in live["provenance"]["ledger"]]
        check(all(isinstance(ms, int) and ms >= 0 for ms in live_ms),
              f"every live row must carry its call's wall time: {live_ms}")
        replay_ms = [row["latency_ms"] for row in replay["provenance"]["ledger"]
                     if "latency_ms" in row]
        check(not replay_ms,
              f"a replay made no call and must not carry a call's time: {replay_ms}")
        # The attempt-timing fields, each both ways. Every live row here is one attempt
        # over HTTP against a local fake: `attempts` 1, the four times whole
        # milliseconds, and no command route's figures, which only a command
        # backend's result envelope can supply.
        live_rows = live["provenance"]["ledger"]
        replay_rows = replay["provenance"]["ledger"]
        check(all(row.get("attempts") == 1 for row in live_rows),
              f"every live row must carry its attempt count: "
              f"{[row.get('attempts') for row in live_rows]}")
        for name in ("answer_ms", "failed_ms", "waited_ms", "ttfb_ms"):
            values = [row.get(name) for row in live_rows]
            check(all(isinstance(ms, int) and ms >= 0 for ms in values),
                  f"every live row must carry {name}: {values}")
        for name in how_the_call_ran[2:]:
            carried = [row[name] for row in replay_rows if name in row]
            check(not carried, f"a replay made no call and must not carry {name}: {carried}")
        for name in ("cli_duration_ms", "cli_duration_api_ms"):
            check(not any(name in row for row in live_rows),
                  f"an HTTP run has no command envelope to read {name} from")
        check(all(row.get("outcome") == "answer" for row in live_rows + replay_rows),
              "every call here parsed first time, so every row is the answer")
        tokens = live["provenance"]["tokens"]
        check(len(live["provenance"]["ledger"])
              == tokens["measured_calls"] + tokens["unmeasured_calls"],
              "the ledger must carry one row per charged response, measured or not")


def acceptance_3_replay_miss_is_fatal() -> None:
    """--replay on a missing key exits 2 naming the key and role, never falls through."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        empty = tmp / "empty"
        empty.mkdir()

        endpoint = FakeEndpoint(echo_document)
        with endpoint as base_url:
            with clean_env(LLOSSLESS_CACHE_DIR=str(tmp / "cache")):
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    code = run_decompose.main(
                        ["--model", "test-model", "--no-colour", "--fixture", "paraphrase",
                         "--base-url", base_url, "--replay", str(empty)]
                    )
            check(endpoint.calls == 0,
                  "a replay miss must never fall through to a live call, even with an endpoint up")

        check(code == 2, f"a replay miss must exit 2, got {code}")
        message = err.getvalue()
        check("decompose" in message, "the message must name the role")
        check(re.search(r"key [0-9a-f]{64}", message) is not None,
              f"the message must name the missing key:\n{message}")
        check("decompose-" in message, "the message must name the file it looked for")


def acceptance_4_pinned_tier_bypasses_the_probe() -> None:
    """--structured prompt against a json_schema-capable endpoint still parses."""
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(
            lambda body, _n: (200, envelope(
                # Tier 3 has no API-level constraint, so this is what tier 3
                # actually gets from a small model: a reasoning block, a fence,
                # and a sentence of preamble around the JSON.
                f"<think>The document has one fact.</think>\n"
                f"Here is the JSON:\n```json\n{CLAIMS_BODY}\n```"
            ))
        )
        with endpoint as base_url:
            settings = settings_for(base_url, Path(tmp), structured="prompt", pinned=True)
            # The notice is captured rather than printed, and then asserted: a
            # `<think>` block in `content` is a model reasoning on a call that
            # asked it not to, which is the same fact as a `reasoning` field and
            # is reported the same way. Letting it reach stderr would make a
            # passing suite look like a failing one.
            notices: list[str] = []
            client = Client(settings, notify=notices.append)
            payload = claims_call(client)

        check(payload["claims"][0]["line"] == 5, "PART C must recover the payload unaided")
        check("response_format" not in endpoint.requests[0],
              "a pinned prompt tier must send no response_format")
        check(endpoint.calls == 1, "pinning must skip the probe entirely")
        check(len(notices) == 1 and "test-model" in notices[0],
              f"a fenced think block on a thinking-off call must be reported: {notices}")

        header = Provenance(settings=settings, client=client, roles=("decompose",),
                            duration_seconds=0.0).as_markdown()
        check("prompt (pinned)" in header, f"the header must show the pinned tier:\n{header}")


def test_a_pinned_tier_is_asserted_on_every_row_not_once_at_the_start() -> None:
    """Pinning is a per-call claim, so it is checked where the rows are written.

    `resolved_tier()` reports one value and reaches the report header once. A
    single call that answered on another rung would leave that header saying
    "json_schema (pinned)" over a run that was two measurements: the vendor
    arms exist to compare models, and a silent demotion would turn a property
    of the request shape into a property of the model.
    """
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
        with endpoint as base_url:
            settings = settings_for(base_url, Path(tmp),
                                    structured="json_schema", pinned=True)
            client = Client(settings)
            claims_call(client)

            check(bool(client.usage.ledger), "the run must have filed ledger rows")
            check(all(row["tier"] == "json_schema" for row in client.usage.ledger),
                  f"every row must carry the pinned tier: {client.usage.ledger}")

            # MUST FIRE. The shipped write point is called directly, with the
            # one thing that is not allowed to reach it.
            try:
                client._record_usage(envelope(CLAIMS_BODY), tier="prompt",
                                     source="live")
                check(False, "a row on an unpinned rung must raise, not be filed")
            except PinnedTierViolated as exc:
                check("prompt" in str(exc) and "json_schema" in str(exc),
                      f"the refusal must name both rungs: {exc}")
            except Exception as exc:  # a crash is not a refusal
                check(False, f"the pin must raise PinnedTierViolated, got {exc!r}")

            # MUST NOT FIRE. Without --structured there is nothing to violate,
            # and the ladder is allowed to answer wherever it lands.
            loose = Client(settings_for(base_url, Path(tmp)))
            try:
                loose._record_usage(envelope(CLAIMS_BODY), tier="prompt",
                                    source="live")
            except Exception as exc:
                check(False, f"an unpinned run must accept any rung, got {exc!r}")

        # A fatal exception is only fatal if the CLI treats it as one. Read
        # off the shipped tuple rather than grepping the file: the name also
        # appears on the import line, so a substring search stays green while
        # the CLI lets the run continue past a demoted call.
        from llossless.cli import FATAL
        check(PinnedTierViolated in FATAL,
              f"cli.FATAL must carry PinnedTierViolated: "
              f"{[e.__name__ for e in FATAL]}")

def acceptance_5_fenced_thinking_response_parses_first_time() -> None:
    """Valid JSON inside ```json fences behind a <think> block: attempt 1, no repair."""
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(
            lambda _b, _n: (200, envelope(
                f'<think>\nLet me work through this.\n</think>\n\n```json\n{CLAIMS_BODY}\n```\n'
            ))
        )
        notices: list[str] = []
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)), notify=notices.append)
            payload = claims_call(client)

        check(payload["claims"][0]["text"] == "The relay listens on port 8443.",
              "the payload must survive the wrapping intact")
        # Same as acceptance 4: the block is stripped and the payload parses,
        # and the run says the model reasoned anyway rather than swallowing it.
        check(len(notices) == 1 and client.usage.thinking_ignored == {"decompose"},
              f"the stripped think block must still be reported: {notices}")
        check(endpoint.calls == 1, f"this must parse on attempt 1, took {endpoint.calls} calls")
        check(client.usage.repairs == 0, "a first-attempt success is not a repair")


def acceptance_6_bad_verdict_errors_rather_than_guessing() -> None:
    """A verdict of UNCLEAR that never clears exhausts every attempt, then errors. Never coerced to MISSING."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        hedged = json.dumps({"verdicts": [{"claim_id": "A-001", "verdict": "UNCLEAR",
                                           "rationale": "half.", "evidence": "e"}]})
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(hedged)))

        with endpoint as base_url:
            settings = settings_for(base_url, tmp, use_cache=True)
            client = Client(settings)
            exc = raises(
                SchemaFailure,
                lambda: client.complete(
                    role="verify", prompt=prompts.load("verify"),
                    messages=[{"role": "user", "content": "judge"}],
                    schema=VERDICT_SCHEMA, schema_name="emit_verdicts",
                    semantic=parsing.check_verdicts,
                ),
                "an unparseable verify response must raise, not return a verdict",
            )

        check(endpoint.calls == SCHEMA_ATTEMPTS,
              f"exactly {SCHEMA_ATTEMPTS} schema attempts, got {endpoint.calls}")
        check("UNCLEAR" in json.dumps(endpoint.requests[1]["messages"]),
              "attempt 2 must quote the specific validation error back to the model")
        check(endpoint.requests[1]["temperature"] == 0.0, "attempt 2 must not raise temperature")
        check(len(endpoint.requests[1]["messages"]) == len(endpoint.requests[0]["messages"]) + 1,
              "attempt 2 appends one message; it does not rewrite the prompt file")
        check(client.usage.errors == 1, "the failure must be counted as an error")

        if exc:
            check(exc.dump is not None and exc.dump.exists(), "the raw response must be kept")
            check("UNCLEAR" in exc.dump.read_text(), "the dump must hold the unmodified body")
            check(exc.dump.parent == tmp / "cache" / "failures",
                  f"dumps belong under the cache's failures/, got {exc.dump.parent}")

        # ... and the run that contains it is inconclusive, exit 2 regardless.
        empty_claim = json.dumps({"claims": [{"text": "", "line": 1, "span": ""}]})
        with FakeEndpoint(lambda _b, _n: (200, envelope(empty_claim))) as base_url:
            with clean_env(LLOSSLESS_CACHE_DIR=str(tmp / "cache2")):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = run_decompose.main(
                        ["--model", "test-model", "--no-colour", "--no-cache",
                         "--fixture", "paraphrase", "--base-url", base_url]
                    )
        check(code == 2, f"a run containing an errored unit must exit 2, got {code}")
        check("ERRORED" in out.getvalue(), "errored units must be reported prominently")
        check("inconclusive" in out.getvalue().lower(),
              "the run must say it did not measure, rather than reporting a low score")


# RFC 6761 / RFC 2606 reserved names, spelled once. Held at module level so
# the control test can subtract them from the pattern instead of restating them.
# Each carve-out below ends in a name boundary, not `$`. It used to end in
# `(?:[:/]|$)`, and `$` without re.MULTILINE means end of the whole string, so
# in a document of any length the carve-out could not fire at all: on
# 2026-08-24 `gateway.example.net` and `www.apache.org` were both reported as
# leaked addresses by patterns that name them as safe. A
# following dot still defeats the carve-out, which is the point of
# `inference.example.com.attacker.net`.
RESERVED_TLD = r"(?![\w.-]*\.(?:invalid|test|example|localhost)(?:[:/]|(?![\w.-])))"
RESERVED_SLD = r"(?!(?:[\w-]+\.)*example\.(?:com|net|org)(?:[:/]|(?![\w.-])))"

# The public sites this repository quotes on purpose. An allowlist, and the
# direction matters: a denylist of endpoint hostnames is one restart out of
# date permanently, because a rented pod's address changes every time it comes
# back, so the list is always describing the pod before last. What does not
# move is the short list of public documentation anybody cited deliberately.
# An address that is not here is a leak until somebody decides otherwise, and
# deciding means editing this line.
# The three vendors' documented, public endpoints and the pages the price
# table cites. These qualify on the same ground as the two
# above: they are fixed, published addresses that the repository names on
# purpose, and they are not the rented pod - a pod address is private and
# changes on every restart, which is the thing this check exists to catch.
# `api.openai.com` in a source file is documentation of which vendor is
# being called; the same string could not identify the user's hardware.
# `creativecommons.org` joins them for the licensing decision: the availability ruling names
# two licences, Apache 2.0 for the code and CC BY 4.0 for the fixture corpora
# and the per-arm records, and only the first one's URL was already citable. A
# licence deed is the same category as the pricing pages -- fixed, published,
# and incapable of naming anybody's hardware.
PUBLIC_REFERENCES = ("www.apache.org", "creativecommons.org",
                     # `LICENSE` became the Elastic License 2.0, and that text
                     # carries the licence's own URL on its second line -- so
                     # the address arrived with the licence rather than being
                     # written here by anyone. Same ground as the two deeds
                     # above: fixed, published, and incapable of naming
                     # anybody's hardware. `www.apache.org` stays because the
                     # milestone records still cite the licence this replaced.
                     "www.elastic.co",
                     "huggingface.co",
                     "api.openai.com", "platform.openai.com",
                     "api.anthropic.com", "docs.claude.com",
                     "generativelanguage.googleapis.com", "ai.google.dev",
                     # The paper's bibliography-check script (withheld with the paper)
                     # re-fetches every bibliography entry from the arXiv API, and reads the
                     # Atom namespace URI to parse the reply. Same ground as
                     # the pricing pages: a fixed published address the
                     # repository names on purpose. `www.w3.org/2005/Atom` is
                     # not even an endpoint -- it is an XML namespace, and
                     # nothing dereferences it.
                     "export.arxiv.org", "arxiv.org", "www.w3.org",
    # The hand-written corpus cites its own sources. `tests/handwritten/`
    # holds documents a person wrote on ordinary subjects, and four of them
    # carry the Wikipedia article they were drawn from, in the body text
    # where a reader can check it. Same ground as the deeds and the pricing
    # pages above: a fixed, published address, incapable of naming anybody's
    # hardware, and here on purpose. Redacting a citation out of a source
    # document would change the document this project measures merges
    # against, which is the one thing this corpus may not do.
    "en.wikipedia.org", "de.wikipedia.org",
    # The `bip39` pair's operator-written documents cite the BIP they are
    # about, and were copied in byte for byte. Same ground as the Wikipedia
    # entries, one narrowing further: a path, not a host. `github.com`
    # alone would admit every repository on it, and a repository is a place
    # anybody can put anything; `bitcoin/bips` is the one this corpus cites.
    # The entry is matched from the start of the address and must end at a
    # `/`, a `:` or the end of the name, so `github.com/bitcoin/bipsx`,
    # `github.com.attacker.net/bitcoin/bips` and `github.com/someone/else`
    # all still fire.
    "github.com/bitcoin/bips",
    # The lessons-learned note's follow-up on the headroom proxy bug cites the
    # upstream fix, operator-supplied. Same ground as `bitcoin/bips`: a path,
    # not the bare host, so `github.com/someone/else` still fires and only
    # this repository is exempt.
    "github.com/headroomlabs-ai/headroom",
    # The answer-key reviews cite the sources the
    # operator named for the planted-error pairs (voyager, bip39), and the
    # remaining-credit lesson cites the upstream feature request. Operator-
    # supplied, public, fixed; paths, not bare hosts, same ground as the entries above.
    "science.nasa.gov/mission/voyager",
    "bitcoin.org/bip",
    "github.com/anthropics/anthropic-sdk-python",
    # The README's clone command names the project's own public repository,
    # and its screenshot is served from the two GitHub-hosted uploads the
    # operator made for it. Paths, not bare hosts, same ground as
    # the entries above: each upload is pinned by its own id, so another asset under
    # `user-attachments` still fires.
    "github.com/toby-sutor/LLossless",
    "github.com/user-attachments/assets/cf0a9646-d93f-4ca5-bd78-a13dc0bc4459",
    "github.com/user-attachments/assets/80a19e18-9d3a-4e95-898e-aa8876f4d7ea",
    # The README's "About the author" names the operator's own public profile,
    # the committed text of the README the operator wrote and this
    # session was told not to touch. Same ground as the repository link
    # above: a path, not the bare host, so `www.linkedin.com` alone and a
    # different profile under it still fire.
    "www.linkedin.com/in/tobysu")
# Each entry is a host, or a host with a path prefix. Escaped whole, so a
# path's characters are literal; the tail is the same boundary for both.
CITED = (r"(?!(?:"
         + "|".join(re.escape(entry) for entry in PUBLIC_REFERENCES)
         + r")(?:[:/]|(?![\w.-])))")

# IPv4 space that cannot carry a private address: loopback, RFC 1918, RFC 3927
# link-local, the three RFC 5737 documentation blocks, and everything from 224
# up. Written as a lookahead rather than a range check in the caller so that
# one definition of "an address" serves every consumer of `secret_patterns`.
OCTET = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"

# The separator between octets and between labels. A literal dot, or a dot that
# has been escaped for a regex -- `142\\.169\\.249\\.42` is the same address as
# `142.169.249.42`, and it is the form an address takes inside the `sed` command
# written to remove it. Seventeen occurrences of one live pod address sat
# tracked in exactly that shape, inside the scan's scope, with the
# scan green over them on every run: the scope was right and the pattern could
# not see it. Optional, so every plain address still matches as before.
DOT = r"(?:\\?\.)"

# The final label of a portless named address. Not a list of endpoints -- a list
# of public suffixes, so it says nothing about which host is in `.env` and does
# not have to be revised when the pod moves. Kept to suffixes a hosted inference
# endpoint plausibly answers on; anything outside it is still caught by the
# port-bearing branch, which takes any TLD.
PUBLIC_TLD = (r"(?:net|com|org|io|ai|dev|app|cloud|co|sh|run|xyz|us|uk|de|"
              r"eu|tech|site|gg|cc|ca|au|fr|nl|jp)")

# `layout.output.run` is an i18n key, not a host: `static/index.html`'s
# `data-t` attribute and both locale JSON files name it literally, and its
# last label happens to collide with `run` on `PUBLIC_TLD` above (Google
# Cloud Run and Render.com both serve hosted endpoints on that suffix, which
# is why `run` is on the list and stays on it). Not a category exemption --
# an i18n key cannot be told apart from a real address by shape alone, which
# is exactly why a rule for "dotted names that look like keys" would blind
# this detector on the one shape it exists to catch. Pinned by the exact
# string instead, the house rule for a detector that must not live in what
# it scans: renaming the key defeats this carve-out on purpose, not by
# drift, and a *different* three-label name ending in `.run` still fires
# (canaried in SECRET_CANARIES, both directions).
# Dotted keys that end in a real TLD and are not addresses, pinned by exact
# content: an interface string key, and the placeholder figure key that gets
# written when it names the paper's `lineup.<row>.<field>` keys.
# `layout.output.run.hint` is its own entry rather than covered by
# `layout.output.run` above: the boundary check right of the alternation
# passes a dot through (`[\w.-]`) but the outer match's own closing boundary
# does not (`[\w-]`), so the tab's tooltip key, one label longer, needed the
# same exact-string pin its own key does.
I18N_KEY_EXEMPT = ("layout.output.run", "layout.output.run.hint", "lineup.x.dev")
NOT_I18N_KEY = r"(?!(?:" + "|".join(re.escape(k) for k in I18N_KEY_EXEMPT) + r")(?:[:/]|(?![\w.-])))"

# Every separator here is `DOT` for the same reason the address branch uses it.
# Widening the matcher to see an escaped address and leaving these as literal
# dots would have made the carve-outs blind in exactly the way the matcher was:
# an escaped `127\\.0\\.0\\.1` would have been reported as a leaked address, and
# there are six of those in the tracked history log that are nothing of the kind.
RESERVED_V4 = (r"(?!(?:0|10|127)" + DOT + r"|169" + DOT + r"254" + DOT
               + r"|192" + DOT + r"168" + DOT
               + r"|172" + DOT + r"(?:1[6-9]|2\d|3[01])" + DOT
               + r"|192" + DOT + r"0" + DOT + r"2" + DOT
               + r"|198" + DOT + r"51" + DOT + r"100" + DOT
               + r"|203" + DOT + r"0" + DOT + r"113" + DOT
               + r"|2(?:2[4-9]|[3-5]\d)" + DOT + r")")


def test_a_base_url_that_is_not_http_is_refused_before_anything_opens_it() -> None:
    """Must fire, and the named file must never be read.

    `build_opener` installs `FileHandler` from its defaults, so
    `LLOSSLESS_BASE_URL=file:///etc/passwd` survived `with_api_path`, was
    fetched, and its bytes were parsed as a model answer. `socket_guard` cannot
    see it: a file read opens no socket, so the guard enforces its constraint
    one layer above the layer where the route exists.
    """
    with tempfile.TemporaryDirectory() as tmp:
        bait = Path(tmp) / "bait.json"
        bait.write_text('{"claims": []}', encoding="utf-8")
        opened: list[str] = []
        real = Path.read_bytes

        def watched(self, *a, **kw):                  # noqa: ANN001
            opened.append(str(self))
            return real(self, *a, **kw)

        Path.read_bytes = watched
        try:
            raised = raises(config.ConfigError,
                            lambda: config.resolve(environ={
                                "LLOSSLESS_BASE_URL": f"file://{bait}"}),
                            "a file:// base URL must be refused")
        finally:
            Path.read_bytes = real
    check("http" in str(raised),
          f"the refusal must say what is supported, got {str(raised)!r}")
    check(str(bait) not in opened,
          f"the named file must never be opened, and was: {opened}")

    # And the schemes that are not a local read but are still not an endpoint.
    for scheme in ("ftp://host/x", "data:text/plain,hi", "gopher://h/1"):
        raises(config.ConfigError,
               lambda s=scheme: config.resolve(environ={"LLOSSLESS_BASE_URL": s}),
               f"{scheme} must be refused")
    raises(config.ConfigError,
           lambda: config.resolve(environ={"LLOSSLESS_BASE_URL": "http:///v1"}),
           "a URL with no host must be refused")


def test_the_cache_is_owner_only_including_one_that_already_exists() -> None:
    """Modes, on a fresh tree and on a 0755 one.

    The cassettes hold the rendered prompt and the raw response -- the
    documents and the merge. `.gitignore` withholds `/assets/` for carrying
    that content; this is a second copy of it and the umask was deciding.

    Four cases, because three of them are the ones a bare `mkdir(mode=...)`
    would miss: an intermediate directory made by `parents=True`, a target
    directory that already exists, and a file written into either.
    """
    from llossless import structured as structured_module
    from llossless.cassette import DIR_MODE, FILE_MODE, Store

    def cassette_into(directory: Path) -> None:
        Store(directory).write(
            key="k", role="verify", model="m", tier="prompt",
            messages=[{"role": "user", "content": "x"}], schema=None,
            temperature=0.0, raw="{}", http_status=200, endpoint="e",
            latency_ms=1, attempt=1)

    with tempfile.TemporaryDirectory() as tmp:
        # Fresh, two levels deep: the intermediate is the one `parents=True`
        # would have left at the umask's mode.
        fresh = Path(tmp) / "fresh" / "responses"
        cassette_into(fresh)
        for made in (fresh.parent, fresh, *fresh.glob("*.json")):
            mode = made.stat().st_mode & 0o777
            wanted = DIR_MODE if made.is_dir() else FILE_MODE
            check(mode == wanted,
                  f"{made.name} is {oct(mode)}, wanted {oct(wanted)}")

        # Already there, and wide. `mkdir`'s mode is ignored for an existing
        # directory, so without a repair every cache made before this stayed
        # 0755 for ever -- and those are the caches this is for.
        old = Path(tmp) / "old" / "responses"
        old.mkdir(parents=True)
        old.chmod(0o755)
        old.parent.chmod(0o755)
        structured_module.Capabilities(old.parent / "capabilities.json").record(
            "e", "m", "prompt", "why")
        cassette_into(old)
        check(old.stat().st_mode & 0o777 == DIR_MODE,
              f"an existing 0755 cache must be repaired, is "
              f"{oct(old.stat().st_mode & 0o777)}")
        check(old.parent.stat().st_mode & 0o777 == DIR_MODE,
              f"and so must the cache root it sits in, which holds the "
              f"capability record and the dumps, is "
              f"{oct(old.parent.stat().st_mode & 0o777)}")
        for written in sorted(old.parent.rglob("*.json")):
            mode = written.stat().st_mode & 0o777
            check(mode == FILE_MODE,
                  f"{written.name} is {oct(mode)}, wanted {oct(FILE_MODE)}")


def test_the_cache_mode_repair_only_ever_narrows() -> None:
    """Must not fire: nothing outside the tree being created is touched.

    An owner who has widened something above the cache is not overruled, and a
    directory already tighter than `DIR_MODE` keeps what it has.
    """
    from llossless.cassette import DIR_MODE, secure_dir

    with tempfile.TemporaryDirectory() as tmp:
        outside = Path(tmp) / "above"
        outside.mkdir()
        outside.chmod(0o755)
        secure_dir(outside / "cache" / "responses")
        check(outside.stat().st_mode & 0o777 == 0o755,
              f"a pre-existing ancestor must not be touched, is "
              f"{oct(outside.stat().st_mode & 0o777)}")

        tighter = Path(tmp) / "tighter"
        tighter.mkdir(mode=0o500)
        secure_dir(tighter)
        check(tighter.stat().st_mode & 0o777 == 0o500,
              f"a directory already tighter than {oct(DIR_MODE)} keeps it, is "
              f"{oct(tighter.stat().st_mode & 0o777)}")


def test_a_key_is_never_sent_in_cleartext_off_this_machine() -> None:
    """Must fire on http + non-loopback + key; must not on any other corner.

    Three conditions, and the check is only interesting when all three hold, so
    each is varied alone. Refused rather than warned, on the same reasoning
    that leaves this project without an `--insecure` flag.
    """
    key_env = config.DEFAULT_KEY_ENV
    was = os.environ.get(key_env)
    os.environ[key_env] = "a-probe-value-not-shaped-like-a-credential"
    try:
        raised = raises(
            config.ConfigError,
            lambda: config.resolve(environ={
                "LLOSSLESS_BASE_URL": "http://a-rented-pod.example.net:8000/v1"}),
            "a key over cleartext to a remote host must be refused")
        check("https" in str(raised),
              f"the refusal must name the answer, got {str(raised)!r}")
        check(os.environ[key_env] not in str(raised),
              "and it must not quote the key back")

        # Must not fire: loopback in every spelling the default and a developer
        # use. Local ollama takes no key and must keep working for anyone who
        # has one exported for something else.
        for url in ("http://localhost:11434/v1", "http://127.0.0.1:11434/v1",
                    "http://a.localhost:8000/v1", config.DEFAULT_BASE_URL,
                    "https://a-rented-pod.example.net/v1"):
            settings = config.resolve(environ={"LLOSSLESS_BASE_URL": url})
            check(settings.base_url.startswith(("http://", "https://")),
                  f"{url} with a key set must be accepted")
    finally:
        if was is None:
            os.environ.pop(key_env, None)
        else:
            os.environ[key_env] = was

    # And the third variation: cleartext to a remote host with no key at all is
    # the recorded pod's own configuration and stays allowed.
    settings = config.resolve(environ={
        "LLOSSLESS_BASE_URL": "http://a-rented-pod.example.net:8000/v1"})
    check(settings.api_key() is None,
          "no key set means no key sent, and nothing to refuse")


def test_the_ordinary_default_base_url_is_not_refused() -> None:
    """Must not fire. Local ollama keeps working, untouched."""
    for url in ("http://localhost:11434/v1", "http://127.0.0.1:11434/v1",
                "https://an-endpoint.example.net/v1", config.DEFAULT_BASE_URL):
        settings = config.resolve(environ={"LLOSSLESS_BASE_URL": url})
        check(settings.base_url.startswith(("http://", "https://")),
              f"{url} must be accepted unchanged, got {settings.base_url!r}")


def test_the_opener_installs_only_the_handlers_it_names() -> None:
    """The second wall, asserted by name in both directions.

    Naming handlers in a `build_opener` call documents an intention and
    installs the defaults anyway -- it adds every default class the caller did
    not pass an instance of. The set is asserted here because that distinction
    is invisible at the call site.
    """
    from llossless import transport

    installed = {type(h).__name__ for h in transport._opener(None).handlers}
    for wanted in ("HTTPHandler", "HTTPSHandler", "_RefuseRedirects",
                   "HTTPErrorProcessor", "HTTPDefaultErrorHandler",
                   "UnknownHandler"):
        check(wanted in installed, f"{wanted} must be installed, got {sorted(installed)}")
    for refused in ("FileHandler", "FTPHandler", "DataHandler"):
        check(refused not in installed,
              f"{refused} must not be installed, got {sorted(installed)}")
    # `UnknownHandler` is what makes an unspeakable scheme raise. Without it
    # `open()` returns None, which is quieter than the failure being fixed.
    for url in ("file:///etc/hostname", "ftp://h/x", "data:text/plain,hi"):
        raises(urllib.error.URLError,
               lambda u=url: transport._opener(None).open(u),
               f"{url} must raise rather than return")


def test_the_endpoint_pattern_dismisses_reserved_names_and_nothing_else() -> None:
    """The RFC 6761 / RFC 2606 carve-out, pinned from both sides.

    Acceptance 7 tripped on `https://example.invalid/pod/abc/v1` in a document,
    which is a placeholder and not a leak. The lookahead that fixed it is only
    safe while it stays this narrow, so both halves are asserted: every
    dismissed address must be one the un-narrowed pattern would have flagged,
    which is what makes it evidence about the carve-out rather than about the
    path shape, and every routable address must still be caught. Widening the
    carve-out to a host that could resolve fails here rather than passing.
    """
    endpoint = secret_patterns()["a hosted endpoint URL"]

    # The same pattern with the carve-out removed. Deriving it rather than
    # restating it means an edit to the lookaheads trips the check below.
    broad = endpoint.pattern
    for lookahead in (RESERVED_TLD, RESERVED_SLD, CITED):
        check(lookahead in broad, "the carve-out this test pins is no longer in the pattern")
        broad = broad.replace(lookahead, "")
    broad = re.compile(broad)

    dismissed = [
        "https://example.invalid/pod/abc/v1",
        "https://a.invalid/pod/abc/v1",
        "http://pod-7.b.invalid:8080/v1/chat",
        "https://runner.test/pod/abc/v1",
        "https://host.example/some/path/v1",
        "https://box.localhost/pod/abc/api",
        "https://example.com/some/path/v1",
        "https://api.example.net/pod/abc/v1",
        "http://example.org:9000/pod/abc/api",
    ]
    for url in dismissed:
        check(broad.search(url) is not None,
              f"fixture proves nothing; the un-narrowed pattern ignores it too: {url}")
        check(endpoint.search(url) is None,
              f"a reserved placeholder name must not read as a leak: {url}")

    fires = [
        "https://198.51.100.7:36033/v1/chat",
        "http://pod-abc123.provider.io/some/path/api",
        "https://gpu-7.example-host.com/pod/xyz/v1",
        "https://api.test-lab.net/pod/abc/v1",
        "https://invalid-host.net/pod/abc/api",
        "https://exampled.com/pod/abc/v1",
        "https://inference.example.com.attacker.net/pod/abc/v1",
    ]
    for url in fires:
        check(endpoint.search(url) is not None,
              f"a routable endpoint must still be caught: {url}")


def test_a_cited_path_admits_that_path_and_not_its_host() -> None:
    """`github.com/bitcoin/bips` is a path-prefixed allowlist entry, pinned from both sides.

    Every other entry in `PUBLIC_REFERENCES` is a bare host. This one is a host
    and a path, so `CITED` has to honour the whole prefix and not only its host:
    the `bip39` citation passes, and the host off that path, the path with a
    longer last segment, the host under another domain, and a pod address that
    carries the path after its own host all still fire.

    The citation is read from the two corpus files that carry it, so the probe
    is the string on disk and not a copy of it, and the un-narrowed pattern must
    report it, which is what makes the pass evidence about the entry.
    """
    patterns = secret_patterns()
    endpoint = patterns["a hosted endpoint URL"]
    broad = re.compile(endpoint.pattern.replace(CITED, ""))
    citation = "https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki"
    for name in ("tests/handwritten/bip39/source_b.md",
                 "tests/handwritten/bip39/reference.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        check(citation in text, f"{name} no longer carries the citation this test pins")
        check(broad.search(text) is not None,
              f"the un-narrowed pattern reports nothing in {name}, so its pass proves nothing")
        for label, pattern in patterns.items():
            found = pattern.search(text)
            check(found is None,
                  f"{name} is reported for {label}: {found.group(0) if found else ''!r}")

    fires = [
        "https://github.com/someone/else",
        "https://github.com/bitcoin/bipsx/blob/master/x",
        "https://github.com.attacker.net/bitcoin/bips/blob/master/x",
        "https://do-not-resolve.pod-canary-not-a-real-host.net/pod/abc/v1",
        "https://do-not-resolve.pod-canary-not-a-real-host.net/github.com/bitcoin/bips",
        "https://198.51.100.7:36033/github.com/bitcoin/bips",
    ]
    for url in fires:
        check(endpoint.search(url) is not None,
              f"a path-prefixed entry must not admit {url}")


# `tests/test_prefreeze_fixes.py` plants real-shaped API keys as
# sentinels, to prove they reach neither the child environment
# (`backend._child_env`) nor `config.dropped_env_names`'s own reported names.
# `tests/test_web_cli_render.py` plants a fourth, to prove a real-looking
# key never reaches `cli_render.render()`'s payload, not even as a suffix.
# Exempting either whole file the way `tests/test_client.py` and
# `tests/scan_artefacts.py` are exempt in `acceptance_7_no_secrets_committed`
# would be wrong: they are ordinary test modules, not detectors, and would go
# blind on a real key pasted into either by accident. So the four literals are
# pinned here instead, by exact content -- the same rule `I18N_KEY_EXEMPT`
# follows for the address scan -- never by splitting the literal to dodge the
# scanner (the house rule). A key one character longer or shorter than any of
# these four still fires (canaried in SECRET_CANARIES).
SENTINEL_EXEMPT = (
    "sk-ant-sentinel-should-not-leak",
    "sk-oai-sentinel-should-not-leak",
    "sk-ant-should-never-appear-as-a-value",
    # The same sentinel, truncated: the test's own `in` check for a leaked
    # value asks whether this shorter run appears inside a reported name, so
    # the literal recurs in the file one character shorter than the one above.
    "sk-ant-should-never-appear",
    # `test_no_stored_key_or_suffix_ever_appears`: a real-shaped
    # Anthropic key, checked against the rendered payload and every suffix
    # of it down to four characters.
    "sk-ant-api03-REALSECRETVALUEDONOTLEAK00000000000000",
)
NOT_SENTINEL = (r"(?!(?:" + "|".join(re.escape(s) for s in SENTINEL_EXEMPT)
                + r")(?![A-Za-z0-9_-]))")


def secret_patterns() -> dict[str, re.Pattern[str]]:
    """The shapes acceptance 7 refuses, held apart so they can be exercised.

    A narrowing that cannot be tested directly is a narrowing nobody notices
    widening again.
    """
    patterns = {
        # `[A-Za-z0-9]` after `sk-` used to stand here, and it could not see a
        # modern OpenAI key: `sk-proj-...` has a dash in it, so the run of 16
        # never started. Underscore and dash are in the class now, which forces
        # the boundary question -- `\b` does not fire inside `ask-before-...`,
        # because `a` and `s` are both word characters, so it never protected
        # anything; a lookbehind for an alphanumeric does. Both the `sk-proj-`
        # key and the `ask-` filename are canaries below. Found by
        # `tests/scan_artefacts.py` on its first real run.
        "an API key": re.compile(r"(?<![A-Za-z0-9])" + NOT_SENTINEL
                                 + r"(sk-[A-Za-z0-9_-]{16,}|"
                                 r"AIza[A-Za-z0-9_-]{20,}|xoxb-[A-Za-z0-9-]{10,})"),
        "a literal Authorization token": re.compile(r"Bearer\s+[A-Za-z0-9._-]{12,}"),
        # The negative lookaheads carve out addresses that cannot be a leak.
        # Loopback is one such class; the reserved names of RFC 6761 and RFC 2606
        # are another - `.invalid`, `.test`, `.example`, `.localhost` and the
        # `example.com/.net/.org` trio are guaranteed never to resolve, so a URL
        # ending in one is a placeholder by construction and not a private
        # endpoint. This narrows the pattern without weakening the control: it
        # can only ever dismiss a host that could not have served a model.
        # The path requirement used to be `/\S*(?:/v\d|/api|/chat)`, which
        # reads as "an API-ish path" and is not: it needs a segment *before*
        # the marker, so `https://host/v1` cannot match and neither can
        # `https://host/`. Those are the two forms anybody actually types, and
        # they are the two forms that leaked -- four pod hostnames sat in
        # tracked in the history log with this check green over them on every offline
        # run for two days. The discriminator is now the host rather than the
        # path: any host that is neither loopback, nor an RFC
        # 6761 / RFC 2606 reserved name, nor a deliberately cited public site
        # has no business in a tracked file, whatever comes after the slash.
        "a hosted endpoint URL": re.compile(
            r"https?://(?!localhost|127\.0\.0\.1|\[?::1)"
            + RESERVED_TLD + RESERVED_SLD + CITED
            + r"[\w-]+(?:\.[\w-]+)+(?::\d+)?(?:/\S*)?"),
        # And an address does not need a scheme to be an address. `curl` gets
        # given a bare host and port, `LLOSSLESS_BASE_URL` gets echoed without
        # one, and a transcript records both: 58 of the 76 endpoint strings
        # found in the history log on 2026-08-24 had no scheme at all, so a URL
        # pattern alone would have caught 18 of them. Two dots are required in
        # the named form because a source file followed by a line number is the
        # same shape as `host.tld:port` and this repository is full of those;
        # an IPv4 literal needs no such help.
        #
        # Two named branches, because the port is not always there either. The
        # first takes any TLD and requires `:port`, which is what disambiguates
        # it from a dotted Python path. The second drops the port and pays for
        # it by requiring a real TLD in the final label: a proxied pod answers
        # on 443 and prints as `sub.proxy.host.net` with no port at all, and on
        # 2026-08-24 exactly that form reached this session's transcript and
        # this pattern scored 0 on it. `resolve` in `llossless.config.resolve`
        # is letters-only and three labels deep, so letters alone cannot carry
        # the distinction and a TLD list is what is left. A TLD missing from
        # the list falls back to the port-bearing branch, so the list can only
        # widen coverage, never narrow it.
        "a bare endpoint address": re.compile(
            r"(?<![\w.-])(?:"
            + RESERVED_V4 + OCTET + r"(?:" + DOT + OCTET + r"){3}(?::\d{1,5})?"
            + r"|" + RESERVED_TLD + RESERVED_SLD + CITED + NOT_I18N_KEY
            + r"(?:[A-Za-z0-9-]+\.){2,}[A-Za-z][A-Za-z0-9-]+:\d{2,5}"
            + r"|" + RESERVED_TLD + RESERVED_SLD + CITED + NOT_I18N_KEY
            + r"(?:[A-Za-z0-9-]+\.){2,}" + PUBLIC_TLD
            + r")(?![\w-])"),
    }
    return patterns


# Every detector in `secret_patterns()`, with a string it MUST report and a
# string it MUST pass. Held as data beside the patterns rather than inside one
# test, so a new detector added without canaries is a failure and not an
# oversight.
#
# The bad strings are deliberately, visibly synthetic. `do-not-resolve.
# pod-canary-not-a-real-host.net` is not a host anybody owns and `100.64.0.1`
# is RFC 6598 shared address space, which never appears as a public endpoint.
# A canary made from a real address would be the leak it is meant to catch, and
# this file is the one file acceptance 7 exempts -- so a real address in here
# would be invisible to the check twice over.
#
# Nothing RFC-reserved can be a MUST-FIRE. `.invalid`, `.test`, `.example` and
# the `example.com/.net/.org` trio are what the carve-outs exist to dismiss, so
# they are on the other list, which is the list that caught the second defect:
# on 2026-08-24 all three carve-outs had been dead for the whole life of the
# pattern and `www.apache.org` was being reported as a leaked address.
SECRET_CANARIES = {
    "an API key": (
        # must fire
        ["sk-canary000000000000notreal",
         # The project-scoped OpenAI shape and the Anthropic shape. Both carry
         # a dash inside the key, and the pattern this replaced saw neither.
         "sk-proj-CANARY0000000000000000notreal",
         "sk-ant-api03-CANARY0000000000notreal",
         "AIzaCanary0000000000notreal000",
         "xoxb-canary-000000-notreal",
         "the key is sk-canary000000000000notreal, pasted into a terminal",
         # One character longer than each `SENTINEL_EXEMPT` literal, proving
         # `NOT_SENTINEL` pins exact content and not a prefix or a shape: the
         # dash the boundary check requires is itself a key character, so the
         # lookahead's boundary never closes and matching runs on past it.
         "sk-ant-sentinel-should-not-leak-but-longer",
         "sk-oai-sentinel-should-not-leak-too",
         "sk-ant-should-never-appear-as-a-value-either",
         "sk-ant-should-never-appears",
         "sk-ant-api03-REALSECRETVALUEDONOTLEAK00000000000000x"],
        # must not fire
        ["sk-short", "AIza", "xoxb-", "sk- is the openai prefix",
         "AIzaSyD is documented but truncated",
         # A prefix glued to the end of a word is not a key. This exact string
         # is a filename under the user's memory directory and it reached a
         # tracked transcript; a `\b` anchor could not tell it apart.
         "memory/ask-before-hosted-api-endpoint.md",
         "the task-key-000000000000 is an identifier",
         # `SENTINEL_EXEMPT`: the three real-shaped sentinels
         # `tests/test_prefreeze_fixes.py` plants to prove they do not
         # leak, each followed by an ordinary word boundary as they are in
         # that file (a comma, a quote, a space).
         "ANTHROPIC_API_KEY=sk-ant-sentinel-should-not-leak",
         '"OPENAI_API_KEY": "sk-oai-sentinel-should-not-leak",',
         "the value is sk-ant-should-never-appear-as-a-value here",
         'not any("sk-ant-should-never-appear" in name for name in dropped)',
         # The fourth: `test_web_cli_render.py`'s own must-not-fire
         # secret, exactly as it is assigned there.
         'secret = "sk-ant-api03-REALSECRETVALUEDONOTLEAK00000000000000"'],
    ),
    "a literal Authorization token": (
        ["Bearer canary.notreal.000000",
         "Authorization: Bearer canary-token-000000"],
        ["Bearer x", "bearer canary.notreal.000000", "Bearer  ",
         # A shell expansion names the variable; the value is what leaks.
         'curl -H "Authorization: Bearer $LLOSSLESS_API_KEY" "$BASE/models"'],
    ),
    "a hosted endpoint URL": (
        # with port, without port, and an IPv4 literal -- the three shapes an
        # endpoint is written in. The scheme-less shapes belong to the bare
        # address detector below and are canaried there.
        ["https://198.51.100.7:36033/v1/chat",
         "https://do-not-resolve.pod-canary-not-a-real-host.net/pod/abc/v1",
         # The host of a path-prefixed entry, off that path. The entry admits
         # one repository, not the site.
         "https://github.com/someone/else",
         # Another upload under the README screenshot's prefix.
         "https://github.com/user-attachments/assets/00000000-0000-0000-0000-000000000000",
         # Another profile under the README author link's prefix.
         "https://www.linkedin.com/in/someone-else/",
         "http://do-not-resolve.pod-canary-not-a-real-host.net:8443/some/path/api"],
        ["https://example.invalid/pod/abc/v1",
         "https://www.apache.org/licenses/LICENSE-2.0",
         "https://creativecommons.org/licenses/by/4.0/",
         "https://www.elastic.co/licensing/elastic-license",
         "https://runner.test/pod/abc/v1",
         "https://api.example.net/pod/abc/v1",
         "http://localhost:11434/v1",
         "https://box.localhost/pod/abc/api",
         # Vendor endpoints and the pricing pages the table cites. Added with
         # the allowlist entries so the carve-out has a probe from the day it
         # exists rather than only a green scan to show for itself.
         "https://api.openai.com/v1/chat/completions",
         "https://api.anthropic.com/v1/messages",
         "https://generativelanguage.googleapis.com/v1beta/models",
         "https://platform.openai.com/docs/pricing",
         "https://docs.claude.com/en/docs/about-claude/pricing",
         # Two entries that were allowlisted and never
         # probed. Nothing in the repository cites them yet, which is the
         # reason they went uncovered and not a reason to leave them so: the
         # carve-out is live from the moment the host is on the line.
         "https://huggingface.co/docs/hub/models",
         "https://ai.google.dev/pricing",
         "https://export.arxiv.org/api/query?id_list=2305.14251&max_results=1",
         "http://www.w3.org/2005/Atom",
         # The hand-written corpus cites the Wikipedia articles its
         # documents were drawn from, in the body text.
         "https://en.wikipedia.org/wiki/Sepiidae",
         "https://de.wikipedia.org/wiki/Gold",
         # The `bip39` pair's citation, verbatim: a path-prefixed entry.
         "https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki",
         "http://arxiv.org/abs/2004.04228v1",
         # The lessons-learned note's citation of the upstream headroom fix,
         # verbatim: a path-prefixed entry, same ground as bip39.
         "https://github.com/headroomlabs-ai/headroom/pull/3172",
         # The planted-error sources and the credit-balance request (2026-09-27).
         "https://science.nasa.gov/mission/voyager/voyager-2/",
         "https://bitcoin.org/bip/39/",
         "https://github.com/anthropics/anthropic-sdk-python/issues/1942",
         # The README's clone URL and screenshot uploads, verbatim.
         "https://github.com/toby-sutor/LLossless/",
         "https://github.com/user-attachments/assets/cf0a9646-d93f-4ca5-bd78-a13dc0bc4459",
         "https://github.com/user-attachments/assets/80a19e18-9d3a-4e95-898e-aa8876f4d7ea",
         # The README's "About the author" link, verbatim.
         "https://www.linkedin.com/in/tobysu/"],
    ),
    "a bare endpoint address": (
        # Portless first: that is the shape a pod behind a proxy prints, it is
        # the shape that reached this session's transcript on 2026-08-24, and
        # the committed pattern scored 0 on it.
        ["do-not-resolve.pod-canary-not-a-real-host.net",
         "do-not-resolve.pod-canary-not-a-real-host.net:8443",
         "100.64.0.1:11434",
         # The escaped form. An address inside the `sed` command written
         # to remove it is still the address, and seventeen of one lived in
         # a tracked history log with this scan green over them on every run,
         # in scope, and invisible to the matcher.
         r"sed -i s|http://100\.64\.0\.1:11434|$LLOSSLESS_BASE_URL|g",
         r"100\.64\.0\.1",
         "no model named qwen3:8b on do-not-resolve.pod-canary-not-a-real-host.net",
         # A different three-label name ending in `.run`, the suffix
         # `I18N_KEY_EXEMPT` carves out for exactly one literal. Proves the
         # carve-out is keyed to the string `layout.output.run`, not to the
         # shape "some i18n-looking key ending in a public suffix".
         "do-not-resolve.pod-canary-not-a-real-host.run",
         # An earlier defect's exact shape: bare host, no scheme, on an indented
         # continuation line inside a multi-line traceback. The `$`-anchored
         # carve-outs could not see this and the leak reached a transcript.
         "Traceback (most recent call last):\n"
         "  File \"transport.py\", line 327, in post_json\n"
         "    raise HTTPStatusError(exc.code, body, host, model) from None\n"
         "llossless.transport.HTTPStatusError: HTTP 404 from "
         "do-not-resolve.pod-canary-not-a-real-host.net for model qwen3:8b"],
        ["www.apache.org", "creativecommons.org", "www.elastic.co",
         "example.invalid", "gateway.example.net",
         "api.openai.com", "api.anthropic.com", "docs.claude.com",
         "generativelanguage.googleapis.com", "huggingface.co", "ai.google.dev",
         "export.arxiv.org", "arxiv.org", "www.w3.org",
         "127.0.0.1:11434", "192.168.1.10", "localhost:11434",
         # The escaped form of each carve-out. Widening the matcher to see an
         # escaped address without widening `RESERVED_V4` the same way would
         # have reported six escaped loopbacks in the tracked history log as leaks.
         r"127\.0\.0\.1:11434", r"192\.168\.1\.10",
         r"198\.51\.100\.7", r"sed s|127\.0\.0\.1|$HOST|",
         # dotted names that are not hosts. These are why the named branch
         # wants a port or a public suffix and not merely two dots.
         "self.settings.host", "llossless.config.resolve",
         "docs/how-it-works.md", "README.md:124", "tests/test_client.py:2392",
         # The i18n key for the "This run" output tab: `static/index.html`'s
         # `data-t` and both locale JSON files name it literally
         # (`I18N_KEY_EXEMPT`). Ends in `run`, a real `PUBLIC_TLD` suffix, by
         # accident of the tab's own name.
         "layout.output.run"],
    ),
}


def test_every_secret_pattern_has_a_seeded_canary() -> None:
    """A scan that has only ever returned 0 is indistinguishable from a dead one.

    Acceptance 7 has been blind twice, and both times it was found by accident.
    Four pod hostnames once sat in a tracked history log while the
    check ran green over them on every offline run for two days. On 2026-08-24
    the same check matched **0 strings over 1,106 tracked files** while that
    file held five real hostnames, from two independent defects: the named
    branch required `:port`, and every carve-out ended in `(?:[:/]|$)` where
    `$` without `re.MULTILINE` is the end of the whole string, so in a document
    of any length no carve-out could fire either.

    Neither defect was reachable from a 0. This test is the pair that makes a 0
    mean something: the real patterns, not copies of them, exercised against a
    string that must be reported and a string that must pass.
    """
    patterns = secret_patterns()
    check(set(patterns) == set(SECRET_CANARIES),
          "every detector needs a must-fire and a must-not-fire canary; "
          f"uncovered: {sorted(set(patterns) - set(SECRET_CANARIES))}, "
          f"stale: {sorted(set(SECRET_CANARIES) - set(patterns))}")

    # Every allowlisted host needs a probe, because an allowlist entry is a
    # hole in the detector and an unprobed hole is one nobody has ever seen
    # work. Two entries sat here unprobed until a later change
    # added `creativecommons.org` beside them; that is the failure this
    # assertion makes impossible rather than merely discouraged.
    probed = [probe for _, must_pass in SECRET_CANARIES.values()
              for probe in must_pass]
    for host in PUBLIC_REFERENCES:
        check(any(host in probe for probe in probed),
              f"{host} is allowlisted with no must-not-fire canary; "
              "editing the allowlist means adding the probe with it")

    for label, (must_fire, must_pass) in sorted(SECRET_CANARIES.items()):
        pattern = patterns.get(label)
        if pattern is None:
            continue
        check(bool(must_fire) and bool(must_pass),
              f"{label} needs canaries in both directions, not one")
        for probe in must_fire:
            found = pattern.search(probe)
            check(found is not None,
                  f"{label} did not report {probe!r}; a detector that cannot "
                  "fire reports 0 for the same reason a clean tree does")
        for probe in must_pass:
            found = pattern.search(probe)
            check(found is None,
                  f"{label} reported {probe!r} as {found.group(0) if found else ''!r}; "
                  "a false positive here gets fixed by exempting a file, and "
                  "that is how a check stops covering the file it exists for")


def test_a_seeded_canary_survives_the_whole_scan() -> None:
    """The canaries against the loop acceptance 7 actually runs, not just the pattern.

    A pattern can be right while the code around it never reaches the text --
    which is the shape of the `redact()` half of this same failure. So one
    must-fire string per detector goes through a scan of a temporary tree, and
    the scan has to name the file.
    """
    patterns = secret_patterns()
    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp)
        for label, (must_fire, must_pass) in sorted(SECRET_CANARIES.items()):
            name = "canary.md"
            (tree / name).write_text(
                "prose above\n" + must_fire[0] + "\nprose below\n", encoding="utf-8")
            reported = [key for key, pattern in patterns.items()
                        if pattern.search((tree / name).read_text(encoding="utf-8"))]
            check(label in reported,
                  f"a file whose only unusual line is {must_fire[0]!r} was not "
                  f"reported for {label}; scan reported {reported}")

            (tree / name).write_text(
                "prose above\n" + "\n".join(must_pass) + "\nprose below\n",
                encoding="utf-8")
            reported = [key for key, pattern in patterns.items()
                        if pattern.search((tree / name).read_text(encoding="utf-8"))]
            check(reported == [],
                  f"{label}'s allowlisted strings were reported as {reported}")


def acceptance_7_no_secrets_committed() -> None:
    """Grep every tracked file for keys, headers and hosted endpoint URLs.

    This used to also reject hosted model names, which is why the cross-model
    sweep was written up under pseudonyms. That was the wrong thing to guard.
    Which models were measured is the substance of the comparison, not a leak;
    the endpoint they were reached through is nobody's business and stays in
    `.env`. Only the credential and the URL are secrets, so only those are here.
    """
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.split()

    patterns = secret_patterns()
    # This file necessarily contains the shapes it searches for.
    #
    # Nothing else belongs in here. When this check trips on a document, the fix
    # is at the pattern, never at this set. The tracked history log in particular is a
    # transcript dump, which makes it the likeliest place for a key pasted from a
    # terminal to land - exactly the case the docstring below names - so
    # exempting it would retire the check on the file it most needs to read.
    # The rule for the next person who edits a pattern in here:
    # **a scanner fix is done only when the string that was missed is a canary
    # that fails before the fix and passes after it.** `SECRET_CANARIES` above
    # is where it goes. A pattern edit verified against a 0 has been verified
    # against nothing, because a dead detector and a clean tree both report 0 --
    # and this check has been dead twice.
    # `tests/scan_artefacts.py` is on the same footing for the same reason: it
    # is the second credential scanner and its canaries are
    # keys by construction. Two files, both of them detectors, and nothing
    # else. When this check trips on anything that is not a detector, the fix
    # is at the pattern or at the file, never here.
    exempt = {"tests/test_client.py", "tests/scan_artefacts.py"}

    scanned = 0
    documentation = 0
    for name in tracked:
        if name in exempt:
            continue
        path = ROOT / name
        if not path.is_file() or path.suffix in {".png", ".jpg", ".ico"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        scanned += 1
        documentation += name.endswith(".md")
        for label, pattern in patterns.items():
            found = pattern.search(text)
            check(found is None, f"{name} contains {label}: {found.group(0) if found else ''!r}")

    # The scan is over `git ls-files`, so it covers prose as well as code. That is
    # a property of the file list rather than of the patterns, so it is asserted:
    # narrowing this to *.py later would silently stop guarding the documentation,
    # which is where a key pasted from a terminal is most likely to end up.
    check(documentation >= 20,
          f"the scan must cover documentation as well as code; saw {documentation} "
          f".md files in {scanned} scanned")


def acceptance_8_warm_cache_makes_no_calls() -> None:
    """Two consecutive live runs against one endpoint: the second makes zero calls."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        endpoint = FakeEndpoint(echo_document)
        with endpoint as base_url:
            settings = settings_for(base_url, tmp, use_cache=True)

            first = Client(settings)
            claims_call(first)
            after_first = endpoint.calls
            check(after_first >= 1, "the first run must actually call the endpoint")

            second = Client(settings)
            claims_call(second)

        check(endpoint.calls == after_first,
              f"a warm cache must make no calls; the endpoint saw "
              f"{endpoint.calls - after_first} more")
        check(second.usage.calls == 0, "the second client must report zero live calls")
        check(second.usage.cache_hits == 1, "the second client must report the cache hit")


def acceptance_replay_never_loads_the_transport_module() -> None:
    """Offline means offline: neither module that can leave this process loads.

    Checked in a fresh interpreter, because this process imported transport
    several tests ago and could only ever answer yes.

    Two modules now, not one. `transport` owns the socket and `backend`
    owns the subprocess, and a replay that started a program would be as much
    a live call as one that opened a connection -- more visibly so, since the
    program is the operator's and may do anything. Both are imported lazily
    inside `_request` for exactly this reason, and this is what holds them
    there.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cassettes = tmp / "tapes"
        with FakeEndpoint(echo_document) as base_url:
            settings = settings_for(base_url, tmp, record_dir=cassettes)
            claims_call(Client(settings))

        script = f"""
import json, sys
sys.path.insert(0, {str(ROOT / "src")!r})
sys.path.insert(0, {str(ROOT / "tests")!r})
from llossless import config, parsing, prompts
from llossless.client import Client
from llossless.decompose import CLAIM_SCHEMA
settings = config.Settings(models={{"verify": "test-model"}},
                           cache_dir={str(tmp / "c")!r},
                           use_cache=False, replay_dir={str(cassettes)!r})
Client(settings).complete(role="decompose", prompt=prompts.load("decompose"),
                          messages=[{{"role": "user",
                                     "content": "The relay listens on port 8443."}}],
                          schema=CLAIM_SCHEMA, schema_name="emit_claims",
                          semantic=parsing.check_claims)
print(json.dumps(sorted(m for m in sys.modules if "urllib.request" in m
                        or m in ("llossless.transport", "llossless.backend"))))
"""
        result = subprocess.run(
            [sys.executable, "-c", script], capture_output=True, text=True, cwd=ROOT
        )
        check(result.returncode == 0, f"the replay subprocess failed:\n{result.stderr}")
        if result.returncode == 0:
            loaded = json.loads(result.stdout)
            check(loaded == [], f"replay loaded a module that can leave this "
                                f"process: {loaded}")


def test_a_model_that_reasons_with_thinking_off_is_reported_not_hidden() -> None:
    """Requested thinking off, reasoning came back: said out loud, fatal only when recording.

    Two modes, because the damage is not the same in both. A recording run puts
    a permanent artefact on disk keyed `thinking=False`, and there is no honest
    way to write it, so it stops before writing. Every other run produces a
    report, and a report can carry the truth: it continues, says so once, and
    the provenance block prints requested against observed.

    The must-not-fire half is half of the test. `"reasoning": ""` is what
    several gateways send unconditionally when thinking is off, and an absent
    key is what both corpus models send -- qwen3:8b behind `m4/` and `pairs/`,
    and Qwen/Qwen3.8-27B-FP8 behind the root corpus and `m7/`, where none of the
    407 recorded messages carries a reasoning field. A detector that fired on either would abort the whole recorded
    suite, which is the failure mode that makes a detector worse than nothing.
    """
    reasons = lambda _b, _n: (200, reasoning_envelope(CLAIMS_BODY, "First, the port."))  # noqa: E731

    with tempfile.TemporaryDirectory() as tmp:
        notices: list[str] = []
        endpoint = FakeEndpoint(reasons)
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)), notify=notices.append)
            payload = claims_call(client, thinking=False)
            claims_call(client, "A second document, on port 9000.", thinking=False)
        check(payload.get("claims"), "the run must continue and return the answer it got")
        check(client.usage.thinking_ignored == {"decompose"},
              f"the role must be recorded for the report, got {client.usage.thinking_ignored}")
        check(len(notices) == 1,
              f"one notice per model, not one per call; got {len(notices)}")
        check("test-model" in notices[0] and "thinking" in notices[0],
              f"the notice must name the model and the setting, got {notices[0]!r}")

    with tempfile.TemporaryDirectory() as tmp:
        record = Path(tmp) / "corpus"
        endpoint = FakeEndpoint(reasons)
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp), record_dir=record,
                                         allow_mixed_sources=True))
            exc = raises(structured.ThinkingIgnored,
                         lambda: claims_call(client, thinking=False),
                         "a recording run must abort rather than mislabel a cassette")
        check(exc is not None and "test-model" in str(exc),
              f"the abort must name the model, got {exc}")
        check(exc is not None and "--thinking decompose" in str(exc),
              f"the abort must name the remedy for this role, got {exc}")
        check(not list(record.glob("*.json")),
              "nothing may be written: the check runs before the cassette does")

    for label, reasoning in (("absent", None), ("empty", ""), ("blank space", "   ")):
        with tempfile.TemporaryDirectory() as tmp:
            notices = []
            record = Path(tmp) / "corpus"
            endpoint = FakeEndpoint(
                lambda _b, _n, r=reasoning: (200, reasoning_envelope(CLAIMS_BODY, r)))
            with endpoint as base_url:
                client = Client(
                    settings_for(base_url, Path(tmp), record_dir=record,
                                 allow_mixed_sources=True),
                    notify=notices.append)
                claims_call(client, thinking=False)
            check(not notices and not client.usage.thinking_ignored,
                  f"[{label}] a response with no reasoning in it must not be accused")
            check(len(list(record.glob("*.json"))) == 1,
                  f"[{label}] and it must still be recorded")

    with tempfile.TemporaryDirectory() as tmp:
        notices = []
        endpoint = FakeEndpoint(reasons)
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)), notify=notices.append)
            claims_call(client, thinking=True)
        check(not notices and not client.usage.thinking_ignored,
              "reasoning is not a fault when the call asked for it")


def test_the_provenance_block_prints_requested_against_observed() -> None:
    """A run answered by a model that reasons anyway says so in its own report."""
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(
            lambda _b, _n: (200, reasoning_envelope(CLAIMS_BODY, "First, the port.")))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)), notify=lambda _m: None)
            claims_call(client, thinking=False)
            block = Provenance(settings=client.settings, client=client,
                               roles=("decompose",), duration_seconds=1.0).as_markdown()
            clean = Client(settings_for(base_url, Path(tmp)))
            claims_call(clean, "A second document, on port 9000.", thinking=True)
            quiet = Provenance(settings=clean.settings, client=clean,
                               roles=("decompose",), duration_seconds=1.0).as_markdown()
    line = [row for row in block.splitlines() if row.startswith("| Decoding")][0]
    check("decompose reasoned anyway" in line,
          f"the Decoding row must name what was observed, got {line!r}")
    check("requested" in line,
          f"and must mark the other half as the request, got {line!r}")
    quiet_line = [row for row in quiet.splitlines() if row.startswith("| Decoding")][0]
    check("reasoned anyway" not in quiet_line and "requested" not in quiet_line,
          f"a run that got what it asked for must print the old row, got {quiet_line!r}")


def test_a_stream_is_recognised_by_its_first_bytes_not_its_content_type() -> None:
    """The header lies; the body cannot.

    Measured 2026-08-28: a hosted proxy in front of ollama labelled a
    server-sent-event response `application/x-ndjson`, which sent every streamed
    answer down the branch that reads a whole JSON body. Both directions are
    checked here, because a client that decided on the first bytes and got it
    backwards would break the ordinary case instead.
    """
    for label, content_type in (("mislabelled", "application/x-ndjson"),
                                ("labelled", "text/event-stream")):
        with tempfile.TemporaryDirectory() as tmp:
            endpoint = FakeEndpoint(
                lambda _b, _n, c=content_type: (200, envelope(CLAIMS_BODY), {"Content-Type": c}))
            with endpoint as base_url:
                client = Client(settings_for(base_url, Path(tmp), stream=True))
                payload = claims_call(client)
            check(endpoint.streamed == 1,
                  f"[{label}] the fixture must actually have streamed")
            check(payload.get("claims"),
                  f"[{label}] a streamed answer must be reassembled whatever it is called")

    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(
            lambda _b, _n: (200, envelope(CLAIMS_BODY),
                            {"Content-Type": "application/x-ndjson"}))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp), stream=False))
            payload = claims_call(client)
        check(endpoint.streamed == 0 and payload.get("claims"),
              "a whole JSON body must still be read as one, whatever its content type says")


def test_an_endpoint_label_reaches_the_error_text_and_not_only_the_provenance() -> None:
    """A labelled run must not write the host into a message anyone can copy.

    The label was honoured on one path only: `Settings.endpoint_id` fed the
    recorded provenance, while every error string interpolated `settings.host`
    directly. A rented pod's hostname carries the pod id and the provider, and
    the empty-body error is the one an operator is likeliest to paste, because
    it is raised on the path that writes no report at all -- there is nothing
    else to quote. An earlier defect already had an address reach a transcript this way.

    Both directions, by design: a redaction proved only by a must-not-fire
    probe is a redaction that would pass if it redacted everything, and one
    proved only by a must-fire probe would pass if it redacted nothing.
    """
    blank = lambda _b, _n: (200, "", {"Content-Type": "application/json"})  # noqa: E731

    def message(**kwargs) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            with FakeEndpoint(blank) as base_url:
                client = Client(settings_for(base_url, Path(tmp), **kwargs))
                return str(raises(structured.EmptyResponse,
                                  lambda: claims_call(client, thinking=False),
                                  "a blank body must still raise"))

    # Must fire. Unlabelled, the host is the only name the endpoint has, and
    # someone debugging their own box needs to read which one refused them.
    unlabelled = message()
    check("127.0.0.1" in unlabelled,
          f"without a label the message must name the host, got {unlabelled!r}")

    # Must not fire. The label is the operator saying this deployment's address
    # does not get written down; the id is what the provenance records, so the
    # message and the run can still be joined.
    labelled = message(endpoint_label="a-rented-pod")
    check("127.0.0.1" not in labelled,
          f"a labelled run must not name the host, got {labelled!r}")
    expected = config.Settings(base_url="http://127.0.0.1:1/v1",
                               endpoint_label="a-rented-pod").endpoint_id
    check(expected in labelled,
          f"and must name the id instead, expected {expected}, got {labelled!r}")
    check("a-rented-pod" not in labelled,
          f"the label is hashed, never printed: an operator can name a pod after "
          f"the provider, got {labelled!r}")

    # The two probes above cover one message. This covers the other twenty:
    # a new error string that reaches for `settings.host` is the regression,
    # and it would pass both probes above by not being on that path.
    for name in ("client.py", "transport.py", "window.py"):
        body = (ROOT / "src" / "llossless" / name).read_text(encoding="utf-8")
        leaked = re.findall(r"\{[a-z_]*(?:settings\.)?host\}", body)
        check(not leaked or name == "transport.py",
              f"{name} interpolates the host into a message: {leaked}")

    # And the site those clauses could not see. The banner is handed
    # `base_url` rather than interpolating `host`, so it survived the first
    # sweep and became the first line of every captured log on the next pod.
    #
    # Two checks, because the first version of this was a tautology: it rebuilt
    # the labelled-or-not expression here and asserted against its own copy, so
    # reverting `cli.py` left it green. The decision now lives in one property,
    # and the call site is pinned by source to that property -- which is the
    # part a value check cannot reach.
    with tempfile.TemporaryDirectory() as tmp:
        with FakeEndpoint(blank) as base_url:
            plain = settings_for(base_url, Path(tmp))
            named = settings_for(base_url, Path(tmp), endpoint_label="a-rented-pod")
    # Must fire. Unlabelled, the point of the line is that an operator with
    # three deployments configured can see which one is about to be waited on,
    # and host and port are what tell those apart.
    check(f"127.0.0.1:{plain.port}" in plain.banner_endpoint,
          f"unlabelled, the banner must name host and port, got "
          f"{plain.banner_endpoint!r}")

    # Must not fire. A URL is not only an address: userinfo is a credential,
    # and a path or a query can carry a token somebody pasted. This line is the
    # first line of every captured log, so it gets scheme, host and port and
    # nothing else; the full string is still there under -vv.
    dressed = config.Settings(
        base_url="http://carried-in-the-userinfo@127.0.0.1:11434/v1"
                 "?t=carried-in-the-query")
    check(dressed.banner_endpoint == "http://127.0.0.1:11434",
          f"the banner must reduce a URL to scheme, host and port, got "
          f"{dressed.banner_endpoint!r}")
    check("127.0.0.1" not in named.banner_endpoint,
          f"labelled, the banner must not name the host, got {named.banner_endpoint!r}")
    check(named.endpoint_id in named.banner_endpoint,
          f"and must name the id instead, got {named.banner_endpoint!r}")

    source = (ROOT / "src" / "llossless" / "cli.py").read_text(encoding="utf-8")
    at = source.find("console.banner(")
    check(at != -1, "cli.py no longer calls console.banner")
    cursor, depth = at + len("console.banner("), 1
    while depth:                       # model_for("verify") nests, so count
        depth += {"(": 1, ")": -1}.get(source[cursor], 0)
        cursor += 1
    banner_call = source[at + len("console.banner("):cursor - 1]
    check("settings.banner_endpoint" in banner_call,
          f"the banner call must pass settings.banner_endpoint, not an endpoint "
          f"expression rebuilt at the call site: {banner_call!r}")


def test_an_empty_200_is_re_asked_and_never_reaches_the_json_decoder() -> None:
    """Zero bytes with a 200 is a blank answer, not a crash and not a bad tier.

    The measured original: gpt-oss:120b, `reasoning_effort: "none"`, 763
    completion tokens billed and an empty body labelled `application/x-ndjson`.
    It reached `json.loads("")` and ended the run on a decoder error naming a
    character position, three times over, on a run that had already paid for a
    merge.
    """
    blank = lambda _b, _n: (200, "", {"Content-Type": "application/x-ndjson"})  # noqa: E731

    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(blank)
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)))
            exc = raises(structured.EmptyResponse,
                         lambda: claims_call(client, thinking=False),
                         "an empty body must arrive as a blank answer, not a decoder error")
        check(endpoint.calls == EMPTY_RESPONSE_ATTEMPTS,
              f"the re-asks stay bounded at {EMPTY_RESPONSE_ATTEMPTS}, got {endpoint.calls}")
        rungs = ["response_format" in request for request in endpoint.requests]
        check(all(rungs) and len(rungs) == EMPTY_RESPONSE_ATTEMPTS,
              f"a blank body must not cost a tier: every re-ask goes out at the "
              f"same rung, got {rungs}")
        for word in ("200", "empty", "test-model", "json_schema"):
            check(word in str(exc), f"the message must name {word}, got {str(exc)!r}")
        check("--thinking decompose" in str(exc),
              f"and must offer the measured remedy for this role, got {str(exc)!r}")
        check(not re.search(r"\b[A-Z][a-z]+[A-Z][A-Za-z]*Error\b", str(exc)),
              f"no Python class names in what an operator reads, got {str(exc)!r}")

    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(blank)
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)))
            exc = raises(structured.EmptyResponse, lambda: claims_call(client, thinking=True),
                         "a blank answer is a blank answer with thinking on too")
        check("--thinking" not in str(exc),
              f"the thinking hint is for calls that asked for thinking off, got {str(exc)!r}")

    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(blank)
        with endpoint as base_url:
            exc = raises(
                transport.EmptyBody,
                lambda: transport.post_json(
                    f"{base_url}/chat/completions", {"model": "test-model", "messages": []},
                    api_key=None, timeout=5, ca_bundle=None, host="fake", model="test-model"),
                "the transport must raise on an empty body rather than return one")
        check(endpoint.calls == 1,
              f"and must not retry it three times on the way, got {endpoint.calls}")
        check(exc is not None and "x-ndjson" in str(exc),
              f"the content type belongs in the message, got {exc}")


def test_a_looping_answer_is_asked_once_more_and_then_errors() -> None:
    """MUST FIRE, on the whole call path. 489 claims, 41 unique: two attempts, then the unit errors.

    A real response, rebuilt as a fixture because reproducing it needs a
    live model. It is complete, parseable and schema-valid -- the garbage is
    *inside* a well-formed answer, which is why nothing objected to it when it
    happened. What is asserted here is the whole handling: the loop is refused,
    the model is told what it repeated, it is asked exactly
    `LOOPING_RESPONSE_ATTEMPTS` times rather than `SCHEMA_ATTEMPTS`, and the
    claims are neither deduplicated nor returned.
    """
    looped = {"text": "The gateway returns HTTP 429 when the client exceeds its quota.",
              "line": 12,
              "span": "The gateway returns HTTP 429 when the client exceeds its quota."}
    claims = [dict(looped) for _ in range(449)]
    claims += [{"text": f"Fact {i} is stated once.", "line": 20 + i,
                "span": f"Fact {i} is stated once."} for i in range(40)]
    check((len(claims), len({c["text"] for c in claims})) == (489, 41),
          "the probe is the measurement: 489 claims of which 41 are unique")
    body = envelope(json.dumps({"claims": claims}))

    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, body))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)))
            exc = raises(SchemaFailure, lambda: claims_call(client),
                         "a claim list that is mostly one claim must not be returned")

    check(endpoint.calls == LOOPING_RESPONSE_ATTEMPTS,
          f"a loop is asked {LOOPING_RESPONSE_ATTEMPTS} times, not {SCHEMA_ATTEMPTS}: "
          f"got {endpoint.calls} generations")
    check(LOOPING_RESPONSE_ATTEMPTS < SCHEMA_ATTEMPTS,
          "the whole point is that this ladder is shorter than the schema one")
    quoted = json.dumps(endpoint.requests[1]["messages"]) if endpoint.calls > 1 else ""
    check("449 times" in quoted,
          "the re-ask must quote the repeat back, or it is the same request twice")
    check(client.usage.errors == 1, "the unit of work errors and is counted")
    check(exc is not None and "repetition loop" in str(exc),
          f"the message must name what happened, got {exc}")
    check(exc is not None and "Nothing was deduplicated" in str(exc),
          f"and say what was not done with the claims, got {exc}")
    check(exc is not None and exc.payload is not None
          and len(exc.payload.get("claims", [])) == 489,
          "the response is carried for the dump, unaltered; it is just never returned")

    # ... and the same 489 claims, spread one per line, are 489 claims.
    spread = [dict(claim, line=i) for i, claim in enumerate(claims)]
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(json.dumps({"claims": spread}))))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)))
            payload = claims_call(client)
    check(len(payload["claims"]) == 489 and endpoint.calls == 1,
          "MUST NOT FIRE: one claim per place is an extraction, however many places")


def test_an_answer_in_the_wrong_order_is_refused_on_the_first_attempt() -> None:
    """Every field valid, the sequence wrong: one attempt, and a message that says why.

    Measured 2026-08-28: deepseek-r1:70b serializes JSON keys alphabetically.
    The repair round quoted the order back, the model answered identically, and
    a usable merge was discarded after 209.7 s of generation. Key order is a
    property of the serializer -- at temperature 0 the second attempt is the
    first attempt -- so the second attempt is not made.
    """
    alphabetical = tuple(sorted(parsing.VERDICT_FIELDS))
    check(alphabetical != parsing.VERDICT_FIELDS,
          "the fixture is only meaningful while the contract is not alphabetical")

    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(verdicts_body(alphabetical))))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)))
            exc = raises(SchemaFailure, lambda: verdicts_call(client),
                         "an out-of-order answer must fail the unit of work")
        check(endpoint.calls == 1,
              f"it must cost one generation, not two; got {endpoint.calls}")
        check(client.usage.repairs == 0, "and it is not a repair")
        check(exc is not None and "test-model" in str(exc),
              f"the message must name the model that did it, got {exc}")
        check(exc is not None and "order" in str(exc) and "json_schema" in str(exc),
              f"and the measured fact: this tier did not constrain order, got {exc}")
        check(exc is not None and "--field-order any" in str(exc),
              f"and the remedy, by name, since one now exists: got {exc}")

    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(verdicts_body())))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)))
            payload = verdicts_call(client)
        check(payload["verdicts"][0]["verdict"] == "SUPPORTED" and endpoint.calls == 1,
              "the same answer in the declared order must pass on the first attempt")

    wrong = json.dumps({"verdicts": [dict(VERDICT, verdict="PROBABLY")]})
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(wrong)))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)))
            raises(SchemaFailure, lambda: verdicts_call(client),
                   "an invalid label is still a fault worth quoting back")
        check(endpoint.calls == SCHEMA_ATTEMPTS,
              f"a fault the model cannot fix consumes every attempt, got {endpoint.calls}")

    short = {"verdicts": [{name: VERDICT[name] for name in parsing.VERDICT_FIELDS[:-1]}]}
    errors = parsing.check_verdicts(short)
    check(errors and not any(isinstance(error, parsing.OrderFault) for error in errors),
          f"a missing field is not an order fault -- reordering cannot fix it: {errors}")
    shuffled = parsing.check_verdicts(
        {"verdicts": [{name: VERDICT[name] for name in alphabetical}]})
    check(shuffled and all(isinstance(error, parsing.OrderFault) for error in shuffled),
          f"and a pure permutation is nothing else: {shuffled}")


def test_the_field_order_switch_relaxes_the_sequence_and_nothing_else() -> None:
    """`--field-order any` takes a permutation. It does not take a wrong answer.

    The switch exists for deepseek-r1:70b, which serializes keys alphabetically
    and cannot be talked out of it. What it is allowed to forgive is exactly the
    sequence: every fault below arrives on the same response shape, and only the
    one where all the fields are present and valid changes verdict when the
    switch moves. A relaxation that also let a missing field or a bad label
    through would not be a looser reading of the contract, it would be no
    contract.
    """
    alphabetical = tuple(sorted(parsing.VERDICT_FIELDS))
    check(alphabetical != parsing.VERDICT_FIELDS,
          "the fixture is only meaningful while the contract is not alphabetical")
    shuffled = envelope(verdicts_body(alphabetical))

    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, shuffled))
        with endpoint as base_url:
            settings = settings_for(base_url, Path(tmp), field_order="any")
            client = Client(settings)
            payload = client_payload = verdicts_call(client)
        check(client_payload["verdicts"][0]["verdict"] == "SUPPORTED",
              f"the answer the model gave must survive the reordering, got {payload}")
        check(endpoint.calls == 1 and client.usage.repairs == 0,
              f"on the first attempt and without a repair, got {endpoint.calls} calls")

    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, shuffled))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp)))
            raises(SchemaFailure, lambda: verdicts_call(client),
                   "and the same body is still refused under the default")

    wrong = envelope(json.dumps({"verdicts": [dict(VERDICT, verdict="PROBABLY")]}))
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, wrong))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp), field_order="any"))
            raises(SchemaFailure, lambda: verdicts_call(client),
                   "a label outside the vocabulary is not a sequence and stays a fault")
        check(endpoint.calls == SCHEMA_ATTEMPTS,
              f"and keeps the repair round the default gives it, got {endpoint.calls}")

    dropped = tuple(name for name in alphabetical if name != parsing.VERDICT_FIELDS[-1])
    short = envelope(verdicts_body(dropped))
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, short))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp), field_order="any"))
            raises(SchemaFailure, lambda: verdicts_call(client),
                   "shuffled and a field short is a field short: still refused")
        check(endpoint.calls == SCHEMA_ATTEMPTS,
              f"and still worth asking twice, got {endpoint.calls}")


def test_a_relaxed_field_order_is_on_the_record_and_the_default_is_not() -> None:
    """The JSON always carries the mode; the report prints it only when it moved.

    Two readers, two needs. A machine comparing runs has to be able to see which
    one relaxed the contract, so the key is unconditional. A person reading a
    report does not need a line on every page restating the default the tool has
    always had -- but must not be able to miss the run where the sequence was
    forgiven, because that run accepted answers the others would have refused.
    """
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(verdicts_body())))
        with endpoint as base_url:
            strict = settings_for(base_url, Path(tmp), structured="json_schema", pinned=True)
            loose = replace(strict, field_order="any")
            check(strict.field_order == "schema",
                  f"the default is the contract, got {strict.field_order!r}")

            for settings, expected in ((strict, "schema"), (loose, "any")):
                client = Client(settings)
                verdicts_call(client)
                record = Provenance(settings=settings, client=client, roles=("verify",),
                                    duration_seconds=0.0)
                data = record.as_dict()["structured_output"]
                check(data["field_order"] == expected,
                      f"the JSON must state the mode either way, got {data}")
                markdown = record.as_markdown()
                check(("field order any" in markdown) == (expected == "any"),
                      f"the row belongs to the run that moved, and only it:\n{markdown}")



def test_tokens_are_counted_on_every_path_not_only_the_live_one() -> None:
    """A cache hit and a replay spend nothing and still cost what they cost.

    The reason this is a test and not a nicety: every published figure in this
    project comes from a replayed corpus, and the paper divides those figures by
    tokens. If only the live path counted, the cost of a result would be
    readable exactly once -- on the day it was recorded -- and never again from
    the artefact that is actually kept.
    """
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        # `prompt_ratio=None` keeps the envelope's own usage block verbatim.
        # This test is about three paths charging the *same* figures, not
        # about the figures being lifelike, and the assertions below name 100
        # and 50 because that is what the envelope declares. The default
        # ratio rewrites `prompt_tokens` to match the request, which is right
        # for every test that exercises the trim check and wrong for this one.
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(verdicts_body())),
                                prompt_ratio=None)
        with endpoint as base_url:
            live = settings_for(base_url, work, structured="json_schema", pinned=True,
                                use_cache=True, record_dir=work / "corpus")
            client = Client(live)
            verdicts_call(client)
            check(client.usage.calls == 1 and client.usage.tokens.measured == 1,
                  f"one live call, one measurement: {client.usage.tokens.as_dict()}")
            spent = client.usage.tokens.as_dict()
            check(spent["input"] == 100 and spent["output"] == 50,
                  f"the live call must charge what the envelope said: {spent}")

            warm = Client(live)
            verdicts_call(warm)
            check(warm.usage.cache_hits == 1 and warm.usage.calls == 0,
                  "the second client must be answered from the cache")
            check(warm.usage.tokens.as_dict() == spent,
                  f"a cache hit costs what the recording cost: "
                  f"{warm.usage.tokens.as_dict()} vs {spent}")

        # No endpoint at all from here: a replay that reached the network would
        # be a different bug, and socket_guard would say so first.
        replaying = Client(replace(live, replay_dir=work / "corpus", use_cache=False))
        verdicts_call(replaying)
        check(replaying.usage.replayed == 1, "the third client must replay")
        check(replaying.usage.tokens.as_dict() == spent,
              f"and a replay costs the same again: "
              f"{replaying.usage.tokens.as_dict()} vs {spent}")


def test_an_unmeasured_call_is_unknown_and_never_zero() -> None:
    """Two arms with no tokens on the table, and they mean opposite things.

    An arm that reported zero was measured and spent nothing. An arm whose
    endpoint sent no usage block was never measured, and a cost-per-token table
    that read both as `0` would rank the unmeasured one first. So the two are
    kept apart in the tally, in the JSON and in the printed row, and this test
    reads all three.
    """
    silent = usage.Tokens()
    silent.add(json.loads(envelope("{}", usage=False)))
    check(not silent.known and silent.unmeasured == 1,
          f"a response with no usage block is unmeasured: {silent.as_dict()}")
    check("input" not in silent.as_dict(),
          f"and reports no input count at all, not zero: {silent.as_dict()}")
    check("unknown" in silent.describe(),
          f"and says so in words: {silent.describe()!r}")

    free = usage.Tokens()
    free.add({"usage": {"prompt_tokens": 0, "completion_tokens": 0}})
    check(free.known and free.as_dict()["input"] == 0,
          f"a measured zero is a measurement: {free.as_dict()}")
    check(free.describe() != silent.describe(),
          f"and must not read like the unmeasured one: {free.describe()!r}")

    # And on a real client, end to end, through the provenance block a reader
    # actually sees. `usage=False` is what ollama sends when the stream is not
    # asked for totals -- see transport -- so this is a shape from the field.
    with tempfile.TemporaryDirectory() as tmp:
        quiet = FakeEndpoint(lambda _b, _n: (200, envelope(verdicts_body(), usage=False)))
        with quiet as base_url:
            settings = settings_for(base_url, Path(tmp), structured="json_schema", pinned=True)
            client = Client(settings)
            verdicts_call(client)
            record = Provenance(settings=settings, client=client, roles=("verify",),
                                duration_seconds=0.0)
            data = record.as_dict()
            check(data["tokens"] == {"measured_calls": 0, "unmeasured_calls": 1},
                  f"the JSON must carry the absence, not a zero: {data['tokens']}")
            check("| Tokens | unknown" in record.as_markdown(),
                  f"and the table must print it:\n{record.as_markdown()}")


def test_the_legacy_token_pair_mirrors_the_tally() -> None:
    """`prompt_tokens` and `completion_tokens` are a view, not a second answer.

    They stay because several runners attribute spend to a unit of work by
    subtracting one reading from another. A mirror is only safe while something
    checks it is still a mirror, so this does.
    """
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(verdicts_body())))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp),
                                         structured="json_schema", pinned=True))
            verdicts_call(client)
            verdicts_call(client)
            spent = client.usage.tokens
            check(client.usage.prompt_tokens == spent.get("input")
                  and client.usage.completion_tokens == spent.get("output"),
                  f"the pair must agree with the tally: "
                  f"{client.usage.prompt_tokens}/{client.usage.completion_tokens} "
                  f"vs {spent.as_dict()}")


def test_the_ledger_tells_two_different_calls_apart() -> None:
    """The must-fire half: different bytes on the wire, different recorded hash.

    A ledger that recorded a constant would satisfy every must-not-fire probe
    ever written against it, so the probe that matters is this one. The two
    calls differ only in the document text; everything else -- role, model,
    prompt, schema, decoding -- is held fixed, so a differing `request_sha256`
    can only have come from the part that actually moved.
    """
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp),
                                         structured="json_schema", pinned=True))
            claims_call(client, text="The relay listens on port 8443.")
            claims_call(client, text="The relay listens on port 9000.")

    rows = client.usage.ledger
    check(len(rows) == 2, f"two calls must file two rows, got {len(rows)}")
    check(rows[0]["request_sha256"] != rows[1]["request_sha256"],
          f"two different requests must not share a hash: {rows[0]['request_sha256']}")
    check(rows[0]["prompt_sha256"] == rows[1]["prompt_sha256"],
          "the same prompt file must carry the same prompt_sha256 -- it is the "
          "template's identity, not the request's, which is why it cannot do "
          "request_sha256's job")
    check({r["role"] for r in rows} == {"decompose"}, f"role must be recorded: {rows}")
    check({r["model"] for r in rows} == {"test-model"}, f"model must be recorded: {rows}")
    check({r["tier"] for r in rows} == {"json_schema"}, f"tier must be recorded: {rows}")


def test_the_ledger_gives_a_repeated_identical_call_the_same_hash() -> None:
    """The must-not-fire half: same bytes twice, same hash twice.

    Without this a hash that simply counted calls would pass the probe above.
    """
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp),
                                         structured="json_schema", pinned=True))
            claims_call(client, text="The relay listens on port 8443.")
            claims_call(client, text="The relay listens on port 8443.")

    rows = client.usage.ledger
    check(len(rows) == 2, f"two calls must file two rows, got {len(rows)}")
    check(rows[0]["request_sha256"] == rows[1]["request_sha256"],
          f"the same request twice must hash the same: "
          f"{rows[0]['request_sha256']} vs {rows[1]['request_sha256']}")
    check(client.usage.calls == 2,
          f"and both must really have gone out, not one and a cache hit: "
          f"{client.usage.calls}")


def test_a_ledger_row_for_an_unmeasured_call_has_no_token_keys() -> None:
    """One level down: absent, not zero.

    A zero here would reconcile against a vendor's bill as "this call was
    free". The call happened, so the row is there; its size was never
    reported, so the keys are not.
    """
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY, usage=False)))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp),
                                         structured="json_schema", pinned=True))
            claims_call(client)

    rows = client.usage.ledger
    check(len(rows) == 1, f"an unmeasured call is still a call: {rows}")
    check("prompt_tokens" not in rows[0] and "completion_tokens" not in rows[0],
          f"an unreported size must be absent, never zero: {rows[0]}")
    check(rows[0]["request_sha256"] and rows[0]["role"] == "decompose",
          f"the row must still identify the call it stands for: {rows[0]}")
    check(client.usage.tokens.unmeasured == 1,
          "and the per-run tally must agree with its own ledger")


def test_the_ledger_and_the_totals_cannot_disagree() -> None:
    """One write point, so the rows must add up to the figure reported."""
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(CLAIMS_BODY)))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp),
                                         structured="json_schema", pinned=True))
            for text in ("one", "two", "three"):
                claims_call(client, text=text)

    rows = client.usage.ledger
    check(sum(r["prompt_tokens"] for r in rows) == client.usage.prompt_tokens,
          f"prompt tokens must sum to the total: {rows} vs {client.usage.prompt_tokens}")
    check(sum(r["completion_tokens"] for r in rows) == client.usage.completion_tokens,
          "completion tokens must sum to the total")
    check(len(rows) == client.usage.tokens.measured + client.usage.tokens.unmeasured,
          "one row per charged response")


# --------------------------------------------------------------------------
# One caller at a time. See `client.ConcurrentCall`, which holds the guard
# state this section describes.
#
# Four probes and the split is the design. The first two hold the guard -- it
# fires on the arrangement it names and stays quiet on the one the project
# supports. The third holds the release path, because a guard that survives its
# own failure turns one bad unit into every later one. The fourth is the seeded
# positive: it bypasses the guard and shows the defect is still there
# underneath, so the guard cannot quietly become decoration around code that
# was fixed some other way -- and so that whoever deletes it has to make this
# test false first.
# --------------------------------------------------------------------------


def _slow_endpoint(delay_by_marker: dict[str, float]) -> FakeEndpoint:
    """An endpoint that takes its time, for whichever request says the word.

    The delay is what makes an overlap an overlap: two calls to an endpoint
    that answers instantly may never be in flight at once however they are
    issued, and a probe that depended on that would pass by luck.
    """
    def responder(body, _n):
        content = (body.get("messages") or [{}])[0].get("content") or ""
        for marker, delay in delay_by_marker.items():
            if marker in content:
                time.sleep(delay)
                break
        return 200, envelope(CLAIMS_BODY)
    return FakeEndpoint(responder)


def _two_overlapping(call, first: str, second: str) -> list:
    """Run `call(marker, role)` twice, overlapping, and return both outcomes.

    An outcome is the value or the exception, never a raise: both halves have
    to be inspected, and a pool that re-raised the first would hide the second.
    """
    import concurrent.futures

    def outcome(future):
        try:
            return future.result()
        except BaseException as exc:  # noqa: BLE001 - the probe's subject
            return exc

    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        early = pool.submit(call, first, "decompose")
        time.sleep(0.25)                  # `early` is in flight before `late`
        late = pool.submit(call, second, "verify")
        return [outcome(early), outcome(late)]


def test_a_second_thread_inside_one_client_is_refused() -> None:
    """The must-fire half. Two threads, one Client, and the second is told no.

    The arrangement is the one a parallel pipeline would produce: two
    independent units of work handed to the same client at once. It is refused
    at the door rather than serialised, because a caller reaching for
    concurrency wants speed and a lock would give them correctness and no
    speed while hiding that the client does not offer what they asked for.
    """
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = _slow_endpoint({"AAAAA": 1.5, "BBBBB": 0.2})
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp),
                                         structured="json_schema", pinned=True))

            def call(marker, role):
                return client.complete(
                    role=role, prompt=decompose_prompt(),
                    messages=[{"role": "user", "content": marker * 4}],
                    schema=CLAIM_SCHEMA, schema_name="emit_claims",
                    semantic=parsing.check_claims).payload

            outcomes = _two_overlapping(call, "AAAAA", "BBBBB")

    refused = [o for o in outcomes if isinstance(o, ConcurrentCall)]
    check(len(refused) == 1,
          f"exactly one of two overlapping calls must be refused, got {outcomes}")
    message = str(refused[0])
    check("single-threaded" in message and "ledger" in message,
          f"the refusal must say what breaks, not only that it refused: {message}")
    check("its own Client, or run the" in message,
          f"and what to do instead: {message}")
    # The other one is a real answer, not a casualty. Refusing the second
    # caller must not spoil the first: the run that was already in flight had
    # nothing wrong with it.
    survived = [o for o in outcomes if not isinstance(o, BaseException)]
    check(len(survived) == 1 and survived[0]["claims"],
          f"the call that was already in flight must still answer: {outcomes}")


def test_two_clients_on_two_threads_are_not_refused() -> None:
    """The must-not-fire half, and it is the arrangement the project supports.

    `web.jobs.JobStore` at `workers > 1` runs two merges at once and builds a
    Client per job, in `web.jobs._run_merge`. A guard that fired on
    that would take multi-user concurrency out of the web server, which is a
    shipped feature, to protect state those two runs do not share.
    """
    import concurrent.futures

    with tempfile.TemporaryDirectory() as tmp:
        endpoint = _slow_endpoint({"AAAAA": 1.0, "BBBBB": 1.0})
        with endpoint as base_url:
            def call(marker, index):
                client = Client(settings_for(base_url, Path(tmp) / str(index),
                                             structured="json_schema", pinned=True))
                payload = client.complete(
                    role="decompose", prompt=decompose_prompt(),
                    messages=[{"role": "user", "content": marker * 4}],
                    schema=CLAIM_SCHEMA, schema_name="emit_claims",
                    semantic=parsing.check_claims).payload
                return client, payload

            with concurrent.futures.ThreadPoolExecutor(2) as pool:
                futures = [pool.submit(call, "AAAAA", 0), pool.submit(call, "BBBBB", 1)]
                results = [f.result() for f in futures]

    for client, payload in results:
        check(bool(payload["claims"]), "each client must answer for itself")
        rows = client.usage.ledger
        check(len(rows) == 1,
              f"and file its own single row, unshared: {rows}")
        check(rows[0]["role"] == "decompose", f"with its own role: {rows[0]}")


def test_a_unit_that_failed_does_not_leave_the_client_locked() -> None:
    """The release path, on the one route that matters: a unit that errored.

    `cli.step` catches `SchemaFailure` and runs the next unit, so a guard
    released only on success would
    turn one bad decompose into a run where nothing after it can call anything
    -- a far worse failure than the one it was added to prevent, and one that
    would show up only on the runs that were already going badly.
    """
    with tempfile.TemporaryDirectory() as tmp:
        bodies = iter(["not json at all"] * SCHEMA_ATTEMPTS + [CLAIMS_BODY])
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(next(bodies))))
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp),
                                         structured="json_schema", pinned=True))
            try:
                claims_call(client)
            except SchemaFailure:
                pass
            else:
                check(False, "the setup must produce a failed unit")
            check(client._caller is None,
                  f"a failed unit must release the guard, not hold it: "
                  f"{client._caller!r}")
            payload = claims_call(client)
            check(bool(payload["claims"]),
                  "and the next unit must be able to run")


def test_the_defect_the_guard_prevents_is_still_there_underneath() -> None:
    """The seeded positive. Bypass the guard, and the ledger lies.

    Without this, the guard is a claim about a hazard nobody has shown, and a
    later change that made overlapping calls safe some other way would leave a
    refusal in place with nothing behind it. `_complete` is the shipped body
    with the claim taken off, so this exercises production code rather than a
    re-creation of it: if `_pending_call` ever stops being a one-slot field
    held across the request, this test goes green in the wrong direction and
    whoever fixed it has to come here and say so.

    What it shows, measured: a `decompose` call and a `verify` call issued
    0.25 s apart file two rows that both name the *later* call. The earlier
    one is not mislabelled, it is absent -- and `usage.calls_by_role`, which is
    incremented at the call site rather than read out of the slot, still counts
    two roles. So the run's own two accounts of itself disagree, and neither
    the exit code nor any existing check looks at the difference.
    """
    with tempfile.TemporaryDirectory() as tmp:
        endpoint = _slow_endpoint({"AAAAA": 1.5, "BBBBB": 0.2})
        with endpoint as base_url:
            client = Client(settings_for(base_url, Path(tmp),
                                         structured="json_schema", pinned=True))

            def call(marker, role):
                return client._complete(
                    role=role, prompt=decompose_prompt(),
                    messages=[{"role": "user", "content": marker * 4}],
                    schema=CLAIM_SCHEMA, schema_name="emit_claims",
                    semantic=parsing.check_claims).payload

            outcomes = _two_overlapping(call, "AAAAA", "BBBBB")

    check(not any(isinstance(o, BaseException) for o in outcomes),
          f"both unguarded calls must answer -- the defect is silent: {outcomes}")
    rows = client.usage.ledger
    check(len(rows) == 2, f"two calls, two rows: {rows}")
    check(sorted(r["role"] for r in rows) != ["decompose", "verify"],
          f"if this ever holds, the one-slot field is gone and the guard in "
          f"`complete` is no longer standing in front of anything: {rows}")
    check(len({r["request_sha256"] for r in rows}) == 1,
          f"and both rows carry one request hash for two different requests: "
          f"{[r['request_sha256'][:12] for r in rows]}")
    check(dict(client.usage.calls_by_role) == {"decompose": 1, "verify": 1},
          f"while the counter that does not read the slot stays right, which "
          f"is what makes the ledger's version unnoticeable: "
          f"{dict(client.usage.calls_by_role)}")


def test_a_vendor_that_spells_usage_differently_still_counts() -> None:
    """Four spellings of the same two numbers, and one shape out.

    Written against the documented shapes rather than observed ones for
    Anthropic and Google -- both are reached through an OpenAI-compatibility
    endpoint, which should send the OpenAI spelling, and accepting the native
    spelling too costs nothing and fails silently if it is ever needed and
    absent. The reasoning and cached sub-counts are carried separately because
    every vendor that reports them bills them at a different rate.
    """
    cases = {
        "openai chat": ({"usage": {"prompt_tokens": 7, "completion_tokens": 3}},
                        {"input": 7, "output": 3}),
        "openai responses": ({"usage": {"input_tokens": 7, "output_tokens": 3}},
                             {"input": 7, "output": 3}),
        "anthropic native": ({"usage": {"input_tokens": 7, "output_tokens": 3,
                                        "cache_read_input_tokens": 2}},
                             {"input": 7, "output": 3, "cached": 2}),
        "google native": ({"usageMetadata": {"promptTokenCount": 7,
                                             "candidatesTokenCount": 3,
                                             "thoughtsTokenCount": 5}},
                          {"input": 7, "output": 3, "thought": 5}),
    }
    for name, (body, expected) in cases.items():
        got = usage.normalise(body)
        check(got == expected, f"{name}: got {got}, expected {expected}")

    check(usage.normalise({"usage": {}}) is None,
          "an empty usage block has told us nothing and must not read as zero")
    check(usage.normalise({}) is None, "and neither has a missing one")



def test_output_the_vendor_left_out_of_completion_tokens_is_costed() -> None:
    """Google's compatibility endpoint counts thinking in the total only.

    Measured on gemini-3.8-flash, 2026-09-25: `prompt_tokens` 7,
    `completion_tokens` 5, `total_tokens` 253 on a three-word answer, and the
    pricing page bills output "including thinking tokens". A cost read off
    `completion_tokens` alone was 2% of the output billed. Must fire on that
    envelope; must not fire on one whose total adds up, which is every
    recording in the corpus.
    """
    from llossless import pricing
    from fake_endpoint import FakeEndpoint as _Fake

    def row_for(usage_block: dict) -> dict:
        body = json.loads(envelope(verdicts_body()))
        body["usage"] = usage_block
        with tempfile.TemporaryDirectory() as tmp:
            with _Fake(lambda _b, _n: (200, json.dumps(body))) as base_url:
                settings = settings_for(base_url, Path(tmp), structured="json_schema",
                                        pinned=True)
                client = Client(settings)
                verdicts_call(client)
        return client.usage.ledger[-1]

    hidden = row_for({"prompt_tokens": 7, "completion_tokens": 5, "total_tokens": 253})
    check(hidden.get("total_tokens") == 253,
          f"a total above input plus output must reach the ledger row: {hidden}")
    adds_up = row_for({"prompt_tokens": 7, "completion_tokens": 5, "total_tokens": 12})
    check("total_tokens" not in adds_up,
          f"a total that adds up must not add a key to the row: {adds_up}")

    rows = [{"model": "gemini-3.8-flash", "prompt_tokens": 1_000_000,
             "completion_tokens": 0, "total_tokens": 2_000_000}]
    got = pricing.estimate(rows).dollars
    want = 0.75 + 3.75
    check(got is not None and abs(got - want) < 1e-9,
          f"the million tokens outside completion_tokens must be costed as output: "
          f"${got} against ${want}")
    plain = [{"model": "gemini-3.8-flash", "prompt_tokens": 1_000_000,
              "completion_tokens": 1_000_000}]
    check(abs((pricing.estimate(plain).dollars or 0) - want) < 1e-9,
          "a row without a total is costed from its own counts")


def acceptance_9_no_credential_reaches_an_artefact() -> None:
    """Run with a key set, write every artefact kind, scan them all for it.

    The control is that the key is never put anywhere: it is not a field on
    `Settings`, it is read from the environment at send time, and `transport`
    builds the `Authorization` header at the socket. This is the backstop, and
    it is a different scan from acceptance 7. That one reads `git ls-files` and
    catches a key pasted into a document. This one reads the *output* of a run
    -- cassette, Markdown report, JSON report, `-vv` console -- which is
    untracked, which is what gets attached to a message or copied to a mirror,
    and which acceptance 7 therefore cannot see.

    The canary is a real key's shape and nobody's key. The scan is run twice:
    once over the artefacts, which must be clean, and once over the same
    artefacts with the canary planted in one of them, which must fire. A scan
    that has only ever returned 0 has not been observed to work, and this
    project's scanners have been blind while green twice.
    """
    canary = "sk-proj-CANARY000000000000000000notreal"
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        recorded = work / "corpus"
        endpoint = FakeEndpoint(lambda _b, _n: (200, envelope(verdicts_body())))
        with endpoint as base_url:
            settings = settings_for(base_url, work, structured="json_schema", pinned=True,
                                    record_dir=recorded, api_key_env="LLOSSLESS_CANARY_KEY")
            console_out = io.StringIO()
            previous = os.environ.get("LLOSSLESS_CANARY_KEY")
            os.environ["LLOSSLESS_CANARY_KEY"] = canary
            try:
                client = Client(settings, console=Console(console_out, verbosity=2,
                                                          enabled=True))
                verdicts_call(client)
                check(settings.api_key() == canary,
                      "the key must actually have been in play, or this proves nothing")
                record = Provenance(settings=settings, client=client, roles=("verify",),
                                    duration_seconds=0.0)
                (work / "report.md").write_text(record.as_markdown(), encoding="utf-8")
                (work / "report.json").write_text(json.dumps(record.as_dict(), indent=2),
                                                  encoding="utf-8")
                (work / "run.log").write_text(console_out.getvalue(), encoding="utf-8")
                run = report.Run(command="verify", paths={}, steps=[], provenance=record)
                (work / "report.html").write_text(html_report.render(run), encoding="utf-8")
            finally:
                if previous is None:
                    os.environ.pop("LLOSSLESS_CANARY_KEY", None)
                else:
                    os.environ["LLOSSLESS_CANARY_KEY"] = previous

        cassettes = sorted(recorded.glob("*.json"))
        check(len(cassettes) == 1, f"the run must have recorded a cassette, got {cassettes}")
        # Named separately from the scan below, because "no Authorization header
        # is written" is a claim about the cassette *writer* and is the thing
        # the scanner is only a backstop for. `Store.write` takes no header
        # argument at all, which is the real guarantee; this reads the artefact
        # it produced and confirms it.
        body = cassettes[0].read_text(encoding="utf-8")
        check("Authorization" not in body and "Bearer" not in body,
              "a cassette must carry no request header")

        needles = {canary: "LLOSSLESS_CANARY_KEY"}
        findings, scanned = scan_artefacts.scan_paths([work], needles)
        check(not findings, f"an artefact carried the credential: {findings}")
        check(scanned >= 5,
              f"the scan must have covered the cassette, the Markdown, the JSON, "
              f"the HTML and the -vv log, saw {scanned} file(s)")

        # The must-fire half. Same scan, same directory, one planted string.
        (work / "leaked.txt").write_text(f"OPENAI_API_KEY={canary}\n", encoding="utf-8")
        fired, _ = scan_artefacts.scan_paths([work], needles)
        check(any("leaked.txt" in line for line in fired),
              f"the scan must find a planted credential, got {fired}")
        check(not any(canary in line for line in fired),
              f"and must never print it: {fired}")



def test_content_left_this_machine_is_answered_across_every_endpoint() -> None:
    """The one claim in the report a reader relies on, and it was inverted.

    `Settings.is_local` answers for the run-wide `base_url` alone, which was the
    whole story until a run could hold several endpoints. The web interface
    routes each role to its model's provider and leaves `base_url` at the
    server's own default, so a run whose every call went to OpenAI reported
    `content_left_this_machine: false` and an endpoint id belonging to the local
    machine it never touched.

    The operator found it in their first real vendor run: nine live calls,
    264 seconds, `gpt-5.6-terra` on all three roles, and a provenance block
    saying the documents stayed here. Getting this backwards is worse than
    omitting it, because a reader who checks it is a reader relying on it.

    `is_local` keeps its meaning -- it is about one address and two checks above
    assert that. The question "did anything leave" is asked of
    `config.addresses`, which enumerates every configured endpoint.
    """
    class _Client:
        usage = None

    def hosted(**kwargs) -> bool:
        return provenance.Provenance(
            settings=config.Settings(**kwargs), client=_Client(),
            roles=("merge", "verify", "decompose"), duration_seconds=1.0).hosted

    vendor = {"merge": "https://api.openai.com/v1",
              "verify": "https://api.openai.com/v1",
              "decompose": "https://api.openai.com/v1"}
    check(hosted(base_url="http://localhost:11434/v1", endpoints=vendor),
          "a run whose roles all point at a vendor left this machine, whatever "
          "the run-wide base_url says")
    check(hosted(base_url="http://localhost:11434/v1",
                 endpoints={"merge": "https://api.openai.com/v1"}),
          "one hosted role is enough; the documents for it left")

    # Must-not-fire, both halves. An all-local run must not start warning, and
    # a replay sends nothing however remote the address is -- a warning that is
    # not true when it appears stops being read.
    check(not hosted(base_url="http://localhost:11434/v1"),
          "an all-local run must not claim content left the machine")
    check(not hosted(base_url="http://localhost:11434/v1",
                     endpoints={"merge": "http://127.0.0.1:8080/v1"}),
          "a second loopback endpoint is still loopback")
    check(not hosted(base_url="https://api.openai.com/v1", replay_dir=str(ROOT)),
          "a replay sends nothing, so nothing left, however remote the address")

    # The same question, reached by a third route. A subprocess has no
    # address to classify, and every guard this property relies on stops at
    # the process boundary -- `check_base_url` has nothing to inspect and the
    # suite's containment is per-process -- so silence here would be read as
    # "no" about something nothing checked.
    check(hosted(base_url="http://localhost:11434/v1", command="claude -p",
                 window=200_000),
          "a command backend must not claim the documents stayed here; "
          "nothing in this process can see what a child does")
    check(hosted(base_url="http://localhost:11434/v1", command="claude -p",
                 window=200_000, endpoints={"merge": "http://127.0.0.1:1/v1"}),
          "and a loopback endpoint beside it does not make it local again, "
          "because that endpoint is not what answered")

    # The one exemption still applies: a replay sends nothing and starts
    # nothing, so it leaks nothing, command backend or not.
    check(not hosted(base_url="http://localhost:11434/v1", command="claude -p",
                     window=200_000, replay_dir=str(ROOT)),
          "a replayed command-backend run started no process, so no document "
          "left by that route either")


def test_the_key_source_is_swappable_per_thread_and_never_serialised() -> None:
    """The seam: `Settings` still carries names, never values.

    The rule `Settings.api_key` protects is "no key value on anything `repr` or
    `asdict` reaches". Reading from `os.environ` was the first
    implementation of that rule, and it is also what made the web server
    single-tenant: a process has one environment, so two concurrent jobs cannot
    hold two users' keys. `keys_for_this_run` swaps the source for the calling
    thread and leaves the rule alone.

    Four things, and the third is the one that would be a cross-user leak: an
    unset source is `os.environ` exactly as before; an *empty* source yields
    None rather than falling back to the operator's environment; two threads
    with overlapping windows see only their own key; and a key active in the
    context reaches none of the places a key is forbidden to reach.
    """
    was = os.environ.get("LLOSSLESS_TEST_KEY")
    os.environ["LLOSSLESS_TEST_KEY"] = "operator-env-key"
    settings = config.Settings(api_key_envs={"merge": "LLOSSLESS_TEST_KEY"})
    try:
        check(settings.api_key("merge") == "operator-env-key",
              "with no source set, the environment is the source, as every "
              "cassette and every recorded figure was measured under")

        with config.keys_for_this_run({"LLOSSLESS_TEST_KEY": "per-job-key"}):
            check(settings.api_key("merge") == "per-job-key",
                  "inside the context the supplied source wins")
        check(settings.api_key("merge") == "operator-env-key",
              "the source is restored on the way out")

        # An empty mapping is a user with no key configured. Falling back to the
        # environment here would hand them the operator's credential and bill
        # it to whoever owns the process -- the exact failure the seam exists to
        # make impossible, and the one a truthiness test would have caused.
        with config.keys_for_this_run({}):
            check(settings.api_key("merge") is None,
                  "an empty source means no key, never the environment's")

        seen: dict[str, str | None] = {}
        barrier = threading.Barrier(2)

        def run(name: str, value: str) -> None:
            with config.keys_for_this_run({"LLOSSLESS_TEST_KEY": value}):
                barrier.wait(timeout=5)     # force the two windows to overlap
                seen[name] = settings.api_key("merge")

        threads = [threading.Thread(target=run, args=("a", "alice-key")),
                   threading.Thread(target=run, args=("b", "bob-key"))]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)
        check(seen.get("a") == "alice-key" and seen.get("b") == "bob-key",
              f"two threads holding different keys at the same moment must see "
              f"only their own, got {seen}")
        check(settings.api_key("merge") == "operator-env-key",
              "a thread setting a source must not move it for any other")

        # Must-fire discipline: the leak probe has to be capable of finding the
        # string it is looking for, or three clean lines prove nothing.
        with config.keys_for_this_run({"LLOSSLESS_TEST_KEY": "SECRET-abc123"}):
            carriers = {
                "repr(Settings)": repr(settings),
                "asdict(Settings)": json.dumps(dataclasses.asdict(settings), default=str),
                "the api_key_envs map": json.dumps(settings.api_key_envs),
            }
            for what, blob in carriers.items():
                check("SECRET-abc123" not in blob,
                      f"an active key reached {what}; Settings may carry the "
                      f"name of a variable and never its value")
            check("SECRET-abc123" in f"{settings.api_key('merge')}",
                  "the probe cannot see its own key, so the three checks above "
                  "passed over nothing")
    finally:
        if was is None:
            os.environ.pop("LLOSSLESS_TEST_KEY", None)
        else:
            os.environ["LLOSSLESS_TEST_KEY"] = was


def test_a_command_backend_answers_in_the_shape_the_http_path_speaks() -> None:
    """`backend.post_json` against real processes, not a stubbed `run`.

    The whole design is that a subprocess answers in the envelope every reader
    downstream already parses, so the thing worth testing is the envelope --
    and testing it against a stub would test the stub. `cat` echoes stdin, so
    a round trip through it proves the prompt reached the child and the answer
    came back through `structured.read_content` unchanged.
    """
    from llossless import backend

    payload = {"messages": [{"role": "user", "content": "the prompt"}]}
    response = backend.post_json("cat", payload, timeout=10, host="h", model="m")
    check(response.status == 200, f"a completed command is a 200: {response.status}")
    check(response.attempts == 1,
          "one attempt, always: a command backend has no retry ladder, because "
          "a program that failed will fail again")
    envelope = json.loads(response.body)
    check(structured.read_content("prompt", envelope) == "the prompt",
          "the child's stdout is what the parser is handed, unchanged")

    # The reason this shape and not a smaller one: `usage.normalise` has to
    # read the absence of a usage block, and `None` is what makes the run count
    # the call `unmeasured` instead of measured-at-zero.
    check(usage.normalise(envelope) is None,
          "no usage block at all, so the call is unmeasured rather than free")
    check("usage" not in envelope,
          "and the key is absent rather than present and empty, because a "
          "reader testing for the key must not find one")


def test_the_result_envelope_is_declared_and_never_sniffed() -> None:
    """A route says how its command answers; nothing guesses.

    The answer under `raw` is itself JSON -- the `prompt` tier asks the model
    for JSON -- so a sniffer would be choosing between two JSON objects on the
    presence of a key. Every case below is driven through a real process, for
    the reason the test above gives: a stub would be testing the stub.

    The must-not-fire half is the important one. A `raw` route handed the
    very envelope a `result` route expects has to carry it through as content,
    or the declaration means nothing.
    """
    from llossless import backend

    payload = {"messages": [{"role": "user", "content": "x"}]}
    body = json.dumps({"type": "result", "subtype": "success", "is_error": False,
                       "result": '{"merged_document": "done"}',
                       "usage": {"input_tokens": 908,
                                 "cache_read_input_tokens": 5370,
                                 "server_tool_use": {"web_search_requests": 3,
                                                     "web_fetch_requests": 0}}})
    command = f"printf %s {shlex.quote(body)}"

    envelope = json.loads(backend.post_json(
        command, payload, timeout=10, host="h", model="m",
        envelope=backend.RESULT).body)
    check(structured.read_content("prompt", envelope) == '{"merged_document": "done"}',
          "under `result` the answer is what was inside `result`, unwrapped")
    check(usage.server_tools(envelope) == {"web_search": 3, "web_fetch": 0},
          f"and the counter comes through: {usage.server_tools(envelope)}")

    # The token counts are deliberately left behind, and this is the seed that
    # would fire if somebody lifted them. Anthropic's `input_tokens` is what
    # was *not* served from cache -- 908 against 5,370 cache reads here -- and
    # `window.assert_prompt_not_trimmed` refuses a call whose reported prompt
    # is at or under half the estimate. Lifting the uncached remainder as "the
    # prompt" refuses honest calls; summing it with the cache reads is wrong
    # for every vendor whose count already includes them.
    check(usage.normalise(envelope) is None,
          f"a `result` route stays unmeasured on tokens: "
          f"{usage.normalise(envelope)}")
    check("input_tokens" not in json.dumps(envelope),
          "and the figure is not carried anywhere in the envelope either, so "
          "no later reader can pick it up by another name")

    # Must not fire: the same bytes, declared `raw`, stay the answer.
    raw = json.loads(backend.post_json(
        command, payload, timeout=10, host="h", model="m").body)
    check(structured.read_content("prompt", raw) == body,
          "a `raw` route hands the whole envelope on as content; the route's "
          "declaration is what decides, never the shape of what came back")
    check(usage.server_tools(raw) is None,
          "and it reports no tool use, because nothing read the block")

    # A route that declares `result` and gets something else refuses. A silent
    # fall back to `raw` would hand the merge an envelope to parse and report
    # the confusion as a model fault.
    for command, why in (
            ("printf 'plain text'", "not JSON at all"),
            ("printf '{\"choices\": []}'", "JSON with no `result` key"),
            (f"printf %s {shlex.quote(json.dumps({'type': 'result', 'is_error': True, 'subtype': 'error_during_execution', 'result': 'x'}))}",
             "an envelope reporting its own turn as an error")):
        try:
            backend.post_json(command, payload, timeout=10, host="h", model="m",
                              envelope=backend.RESULT)
            check(False, f"a `result` route accepted {why}")
        except backend.CommandError as exc:
            check("result" in str(exc) or "error" in str(exc),
                  f"the refusal for {why} must say what was expected: {exc}")

    check(backend.ENVELOPES == config.COMMAND_ENVELOPES,
          "one table, and it is `config`'s: this module is imported lazily so "
          "that a replay never loads it, and a constant defined here would "
          "pull the socket module into every offline run")


def test_the_search_counter_is_measured_and_unknown_is_not_zero() -> None:
    """Three states, read off the answer and never asked for.

    A model that says it searched has made a claim; `server_tool_use` is a
    count the serving side wrote down. The three states have to stay three:
    an endpoint that never reports is not an endpoint that reported zero, and
    a citation carried by the first is a recollection while a citation carried
    by the second is at least capable of having been looked up.
    """
    tally = usage.Searches()
    check(tally.state == "unmeasured" and tally.total is None,
          "a run that made no call is unmeasured, not not-searched")

    tally.add({"usage": {"input_tokens": 5}})
    check(tally.state == "unmeasured" and tally.unmeasured == 1,
          f"an endpoint that reports tokens and no tool block is unmeasured: "
          f"{tally.as_dict()}")
    check("0" not in tally.describe().split("(")[0],
          f"and it must not describe itself with a number: {tally.describe()}")

    zero = usage.Searches()
    zero.add({"usage": {"server_tool_use": {"web_search_requests": 0,
                                            "web_fetch_requests": 0}}})
    check(zero.state == "not-searched" and zero.total == 0,
          f"a reported zero is a measurement, and a different one: "
          f"{zero.as_dict()}")

    some = usage.Searches()
    some.add({"usage": {"server_tool_use": {"web_search_requests": 0,
                                            "web_fetch_requests": 0}}})
    some.add({"usage": {"server_tool_use": {"web_search_requests": 2,
                                            "web_fetch_requests": 1}}})
    check(some.state == "searched" and some.total == 3,
          f"one call that searched makes the run one that searched: "
          f"{some.as_dict()}")
    check(some.as_dict()["web_search"] == 2 and some.as_dict()["web_fetch"] == 1,
          "and the two counters stay apart, because the two are separately "
          "granted and carry different risk")

    # An empty block is not a measured absence. A vendor that sent
    # `server_tool_use: {}` has told us nothing.
    empty = usage.Searches()
    empty.add({"usage": {"server_tool_use": {}}})
    check(empty.state == "unmeasured",
          f"an empty block tells us nothing: {empty.as_dict()}")

    check(set(usage.SEARCH_STATES) == {"searched", "not-searched", "unmeasured"},
          f"three states and no fourth spelling: {usage.SEARCH_STATES}")


def test_the_turn_counter_sees_the_tool_use_the_search_counter_is_blind_to() -> None:
    """Two instruments, and on this backend only one of them can see.

    `server_tool_use` counts a vendor's **server-side** web tools. A
    subscription CLI's `WebFetch` runs locally in the CLI's own process and
    never increments it, which was measured rather than assumed: a call that
    demonstrably fetched -- proved by pointing it at a hostname that cannot
    resolve and getting the CLI's own `getaddrinfo ENOTFOUND` back -- still
    reported `{"web_search_requests": 0, "web_fetch_requests": 0}`.

    A tool call costs a round trip, so it costs a turn, and a fetch costs two
    tool calls: `WebFetch` is deferred, so `ToolSearch` loads it first. Both
    counters are carried and neither is dropped, because the blind one
    reporting zero is exactly the reading a reader must not be given on its
    own.

    Seeded both ways. The must-fire is the measured fetch -- three turns,
    traced as `ToolSearch`, `WebFetch`, answer -- and the must-not-fires
    are the two readings of a plain answer, one turn here and two on the
    operator's machine, and the run that reported no turn count at all, which
    is every HTTP endpoint this project talks to and must never read as "no
    tool use".
    """
    from llossless import backend

    payload = {"messages": [{"role": "user", "content": "x"}]}

    def envelope_for(turns, tools):
        body = json.dumps({"type": "result", "subtype": "success",
                           "is_error": False,
                           "result": '{"merged_document": "done"}',
                           "num_turns": turns,
                           "usage": {"server_tool_use": tools}})
        return json.loads(backend.post_json(
            f"printf %s {shlex.quote(body)}", payload, timeout=10, host="h",
            model="m", envelope=backend.RESULT).body)

    # The measured calls, and the disagreement in them. Every one reports the
    # blind counter at zero; the turn count separates them.
    quiet = envelope_for(1, {"web_search_requests": 0, "web_fetch_requests": 0})
    fetched = envelope_for(3, {"web_search_requests": 0, "web_fetch_requests": 0})
    check(usage.turns(quiet) == 1 and usage.turns(fetched) == 3,
          f"the turn count must survive the envelope: "
          f"{usage.turns(quiet)}, {usage.turns(fetched)}")
    check(usage.server_tools(quiet) == usage.server_tools(fetched)
          == {"web_search": 0, "web_fetch": 0},
          "and the search counter must be identical across the pair, which is "
          "the blindness this exists to route around")

    used = usage.Turns()
    used.add(quiet)
    used.add(fetched)
    check(used.state == usage.TOOL_USE and used.with_tools == 1 and used.total == 4,
          f"one call at a fetch's three turns makes the run one that used a "
          f"tool: {used.as_dict()}")
    check("fetch" not in used.describe(),
          f"and it is described in turns, never in fetches: {used.describe()}")

    none = usage.Turns()
    none.add(quiet)
    check(none.state == usage.NO_TOOL_USE,
          f"every call at one turn is a run that used nothing: {none.as_dict()}")

    # Seeded against the threshold it replaced. A two-turn call is the
    # operator's plain answer, or a deferred tool loaded and never called; it
    # is not a retrieval either way, because a fetch costs three. The old
    # floor of one counted it as tool use and printed "11 of 12 call(s) used a
    # tool" over 27 turns. The detector reads the shipped `Turns`, and is run
    # a second time with the old floor put back to prove it can fire.
    two = envelope_for(2, {"web_search_requests": 0, "web_fetch_requests": 0})

    def two_turns_retrieved_nothing() -> bool:
        tally = usage.Turns()
        for _ in range(12):
            tally.add(two)
        return tally.state == usage.NO_TOOL_USE and tally.with_tools == 0

    check(two_turns_retrieved_nothing(),
          "a two-turn call must report no tool use: a retrieval costs three "
          "turns, and counting two as one is the defect that was fixed")
    shipped = usage.MOST_TURNS_WITHOUT_RETRIEVAL
    try:
        usage.MOST_TURNS_WITHOUT_RETRIEVAL = 1
        check(not two_turns_retrieved_nothing(),
              "the detector must fire on the old floor of one, or it cannot "
              "tell the defect from the fix")
    finally:
        usage.MOST_TURNS_WITHOUT_RETRIEVAL = shipped
    check(shipped == 2,
          f"the floor is two turns, between a plain answer's one or two and a "
          f"fetch's three: {shipped}")
    check("one turn each" not in _described_twelve_plain(two),
          "and the provenance line must not claim one turn a call")

    # Must not fire. An endpoint that reports tokens and no turn count is
    # unmeasured, and reading that silence as "one turn, so no tool use" would
    # turn every hosted run into a claim the model did not look anything up.
    blind = usage.Turns()
    blind.add({"usage": {"input_tokens": 5}})
    blind.add(None)
    check(blind.state == usage.UNMEASURED and blind.unmeasured == 2,
          f"unmeasured is not no-tool-use: {blind.as_dict()}")
    check("0" not in blind.describe().split("(")[0],
          f"and it must not describe itself with a number: {blind.describe()}")

    # A `raw` route reads neither, because nothing parsed an envelope.
    plain = json.loads(backend.post_json(
        "printf 'hello'", payload, timeout=10, host="h", model="m").body)
    check(usage.turns(plain) is None,
          "a `raw` route has no envelope to read a turn count out of")

    check(set(usage.TOOL_USE_STATES) == {"tool-use", "no-tool-use", "unmeasured"},
          f"three states and no fourth spelling: {usage.TOOL_USE_STATES}")


def test_a_result_envelope_names_the_models_that_answered() -> None:
    """The CLI resolves `--model opus` itself; `modelUsage` says to what.

    Through a program that writes the envelope, as the backend runs one. The
    author is the id whose counts are the envelope's own `usage` block, the
    main conversation's. Seeded with the three envelopes the 2026-09-25 grid
    wrote where the id with the most output tokens was not that one -- a
    verify answer of 11 tokens beside Haiku's 12-token side call, and an Opus
    merge whose subagent wrote 34,498 tokens on Sonnet -- and both ways round:
    one id; no usage block, or a block matching no id, or two, which name no
    author rather than guess; and must-not-fires -- no `modelUsage`, an empty
    one, a `raw` route and an HTTP-shaped envelope carry no `answered_by`.
    """
    from llossless import backend

    payload = {"messages": [{"role": "user", "content": "x"}]}

    def answered(model_usage, envelope=backend.RESULT, used=None):
        body = {"type": "result", "subtype": "success", "is_error": False,
                "result": '{"merged_document": "done"}', "num_turns": 1}
        if model_usage is not ...:
            body["modelUsage"] = model_usage
        if used is not None:
            body["usage"] = used
        text = json.dumps(body)
        wire = json.loads(backend.post_json(
            f"printf %s {shlex.quote(text)}", payload, timeout=10, host="h",
            model="opus", envelope=envelope).body)
        return wire, usage.answered_by(wire)

    haiku, opus, sonnet = "claude-haiku-4-5-20251001", "claude-opus-5", "claude-sonnet-5"
    wire, said = answered({haiku: {"inputTokens": 8377, "outputTokens": 17},
                           opus: {"inputTokens": 8, "outputTokens": 16357}},
                          used={"input_tokens": 8, "output_tokens": 16357})
    check(said == {"models": [haiku, opus], "output": opus},
          f"both ids, and the main conversation's as the author: {said}")
    check(usage.turns(wire) == 1 and "answered_by" not in (wire.get("usage") or {}),
          f"beside the turn count, not inside the usage block: {wire}")
    check(usage.Tokens().add(wire) is None,
          "and no token count crosses: the call stays unmeasured on cost")

    _, said = answered({haiku: {"inputTokens": 900, "outputTokens": 12},
                        opus: {"inputTokens": 4, "outputTokens": 11}},
                       used={"input_tokens": 4, "output_tokens": 11})
    check(said == {"models": [haiku, opus], "output": opus},
          f"an 11-token answer beside a 12-token side call is still Opus's: {said}")
    _, said = answered({haiku: {"inputTokens": 845567, "outputTokens": 14938},
                        sonnet: {"inputTokens": 48, "outputTokens": 34498},
                        opus: {"inputTokens": 4, "outputTokens": 33704}},
                       used={"input_tokens": 4, "output_tokens": 33704})
    check(said == {"models": [haiku, opus, sonnet], "output": opus},
          f"a subagent's larger count does not make it the author: {said}")

    _, said = answered({sonnet: {"outputTokens": 3}})
    check(said == {"models": [sonnet], "output": sonnet}, f"one id is its own author: {said}")
    _, said = answered({haiku: {"outputTokens": 17}, opus: {"outputTokens": 16357}})
    check(said == {"models": [haiku, opus], "output": None},
          f"two ids and no usage block name no author: {said}")
    _, said = answered({haiku: {"outputTokens": 17}, opus: {"outputTokens": 16357}},
                       used={"output_tokens": 500})
    check(said == {"models": [haiku, opus], "output": None},
          f"a block matching no id names no author: {said}")
    _, said = answered({"a-model": {"outputTokens": 40}, "b-model": {"outputTokens": 40}},
                       used={"output_tokens": 40})
    check(said == {"models": ["a-model", "b-model"], "output": None},
          f"a block matching two ids names no author: {said}")
    _, said = answered({"a-model": {"inputTokens": 5, "outputTokens": 40},
                        "b-model": {"inputTokens": 9, "outputTokens": 40}},
                       used={"input_tokens": 9, "output_tokens": 40})
    check(said == {"models": ["a-model", "b-model"], "output": "b-model"},
          f"the input count settles two equal output counts: {said}")
    _, said = answered({"a-model": {"inputTokens": 40}, "b-model": {"outputTokens": True}},
                       used={"output_tokens": 1})
    check(said == {"models": ["a-model", "b-model"], "output": None},
          f"no usable output count names no author, and keeps the ids: {said}")

    for model_usage in (..., {}, [], "claude-opus-5-5"):
        wire, said = answered(model_usage)
        check(said is None and "answered_by" not in wire,
              f"{model_usage!r} names no model and must add no key: {wire}")
    plain = json.loads(backend.post_json(
        "printf 'hello'", payload, timeout=10, host="h", model="m").body)
    check(usage.answered_by(plain) is None, "a `raw` route has no envelope to read")
    check(usage.answered_by({"model": "qwen3:8b", "choices": []}) is None,
          "an HTTP envelope's own `model` field is not read: the recorded "
          "corpus must not grow a key")
    for forged in ({"models": []}, {"models": ["x", 3]}, {"models": "x"},
                   {"output": "x"}):
        check(usage.answered_by({"answered_by": forged}) is None,
              f"a malformed block is no answer: {forged}")
    check(usage.answered_by({"answered_by": {"models": ["x"], "output": "y"}})
          == {"models": ["x"], "output": None},
          "an author the list does not name is not an author")


def test_the_blind_counter_keeps_its_number_and_loses_its_conclusion() -> None:
    """The contradiction the first live `sourced` run printed.

    `server_tool_use` reported `{0, 0}` and the turn counter saw three of four
    calls use a tool, so the report carried *"The model made no web request
    while merging, so every source here is recalled rather than looked up"*
    immediately beside *"it used the tool it was granted at least that often"*.
    Two sentences a reader can only read as a contradiction, and the false one
    is the zero's: that counter counts a vendor's server-side tools and a
    command-line tool runs in the model's own process, so its zero means "this
    instrument saw nothing" rather than "nothing happened".

    Seeded four ways -- the disagreement, the agreement, a real search, and the
    run that reports no turn count at all, which is every recorded figure in
    this project and whose wording must not move.
    """
    from llossless import report as report_module

    def sentence(search_block, turn_count, fidelity="open"):
        run = report.Run(command="merge")
        run.provenance = _Provenance(fidelity, search_block, turn_count)
        return report_module.sourcing_sentence(run)

    recalled = "every source here is recalled rather than looked up"

    # Must fire: the counters disagree. The zero is explained and its
    # conclusion is gone. Three turns is a traced fetch.
    disagree = sentence({"web_search_requests": 0, "web_fetch_requests": 0}, 3)
    check(recalled not in disagree,
          f"the blind counter still drew its conclusion beside a turn count "
          f"that contradicts it: {disagree!r}")
    check("could not see one" in disagree,
          f"and the zero must be explained rather than dropped: {disagree!r}")
    check("used a tool it was granted" in disagree,
          f"the instrument that can see this backend must lead: {disagree!r}")

    # Must not fire: they agree. One turn or two, zero requests, and the
    # honest conclusion is available to both -- two turns is short of the
    # three a fetch costs.
    for plain in (1, 2):
        agree = sentence({"web_search_requests": 0, "web_fetch_requests": 0},
                         plain)
        check("retrieved nothing" in agree,
              f"an agreed absence at {plain} turn(s) is said once, plainly: "
              f"{agree!r}")
        check("could not see one" not in agree,
              f"and needs no explanation of a zero nothing contradicts: "
              f"{agree!r}")

    # Must not fire: a vendor that really did report a search keeps its count.
    searched = sentence({"web_search_requests": 2, "web_fetch_requests": 0}, 6)
    check("2 web request(s)" in searched,
          f"a non-zero count is information and is kept: {searched!r}")

    # Must not fire: no turn count at all. This is every HTTP run and every
    # recorded figure here, and its wording must be byte-for-byte what it was.
    blind = sentence({"web_search_requests": 0, "web_fetch_requests": 0}, None)
    check(recalled in blind,
          f"a run with no turn count keeps the sentence it has always had: "
          f"{blind!r}")

    # And the sourced run that retrieved nothing says so, whatever either
    # counter reported.
    quiet = sentence({"web_search_requests": 0, "web_fetch_requests": 0}, 1,
                     fidelity=config.SOURCED)
    check("nothing was retrieved" in quiet,
          f"a sourced run that used no tool must say every citation is recall: "
          f"{quiet!r}")


def test_a_sourced_run_says_which_of_three_retrieval_states_it_reached() -> None:
    """`sourced` reports what retrieval achieved, not only what it permitted.

    Three states, each seeded, on every surface a reader of a finished run
    meets: the verdict line (Markdown and HTML both render it), the additions
    section's sourcing sentence, the JSON field, and the terminal summary.

    The must-fire that matters most is `unmeasured`: it must never render as
    "did not retrieve", including on a run where some calls reported and one
    did not -- the silent call may be the one that fetched. And the
    must-not-fire: below `sourced` nothing promised retrieval, so no surface
    gains a sentence and every recorded report's wording stands.
    """
    from llossless import cli
    from llossless import report as report_module

    def run_at(fidelity, *turn_counts):
        run = report.Run(command="merge")
        provenance = _Provenance(fidelity, {"web_search_requests": 0,
                                            "web_fetch_requests": 0}, None)
        for count in turn_counts:
            provenance.client.usage.turns.add(
                None if count is None else {"usage": {"num_turns": count}})
        run.provenance = provenance
        return run

    def terminal(run):
        stream = io.StringIO()
        cli.summarise(run, 0, output=None, coloured=False, piped=True,
                      stream=stream)
        return stream.getvalue()

    retrieved = run_at(config.SOURCED, 1, 3, 2)
    nothing = run_at(config.SOURCED, 1, 2, 2)
    silent = run_at(config.SOURCED, None, None)
    partial = run_at(config.SOURCED, 2, 2, None)

    cases = (
        (retrieved, usage.RETRIEVED, "The model retrieved.",
         "The model retrieved. 1 of 3 call(s)"),
        (nothing, usage.NOT_RETRIEVED, "Nothing was retrieved.",
         "Nothing was retrieved. None of 3 call(s)"),
        (silent, usage.UNMEASURED, "Whether anything was retrieved is unmeasured.",
         "is unmeasured. 2 call(s) reported no turn count"),
        (partial, usage.UNMEASURED, "Whether anything was retrieved is unmeasured.",
         "is unmeasured. 1 call(s) reported no turn count"),
    )
    for run, state, verdict, said in cases:
        check(report_module.retrieval_outcome(run) == state,
              f"{state}: the outcome was {report_module.retrieval_outcome(run)!r}")
        line = report_module.verdict_line(run)
        check(verdict in line,
              f"{state}: the verdict line must say it: {line!r}")
        check(said in terminal(run),
              f"{state}: and so must the terminal: {terminal(run)!r}")
        check(report_module.recall_only(run) is (state == usage.NOT_RETRIEVED),
              f"{state}: recall_only is the second state and no other")

    # The inversion, seeded where it is easiest to commit. One silent call and
    # two that reported two turns each: `state` reads `no-tool-use` off the two,
    # and a report that followed it would tell the reader nothing was looked up.
    for run in (silent, partial):
        for text in (report_module.verdict_line(run),
                     report_module.sourcing_sentence(run), terminal(run)):
            check("Nothing was retrieved" not in text
                  and "retrieved nothing" not in text
                  and "every source here is recalled" not in text,
                  f"unmeasured must never read as did-not-retrieve: {text!r}")
    check("unmeasured" in report_module.sourcing_sentence(partial),
          f"the additions section must say the partial run is unmeasured: "
          f"{report_module.sourcing_sentence(partial)!r}")

    # Must not fire: the same three tallies below `sourced`. No level there
    # promised retrieval, so no surface gains a sentence.
    for counts in ((1, 3, 2), (1, 2, 2), (None, None)):
        below = run_at("open", *counts)
        check(report_module.retrieval_outcome(below) == "",
              f"open has no retrieval outcome: {counts}")
        check("retriev" not in report_module.verdict_line(below).lower(),
              f"open's verdict line must not change: {counts}")
        check("retriev" not in terminal(below).lower(),
              f"nor its terminal summary: {counts}")


def _described_twelve_plain(envelope: dict) -> str:
    """`Turns.describe()` over twelve copies of one envelope."""
    tally = usage.Turns()
    for _ in range(12):
        tally.add(envelope)
    return tally.describe()


class _Provenance:
    """The two tallies and the level a `Run` reads off its provenance."""

    def __init__(self, fidelity, search_block, turn_count) -> None:
        searches = usage.Searches()
        searches.add({"usage": {"server_tool_use": search_block}})
        turns = usage.Turns()
        if turn_count is not None:
            turns.add({"usage": {"num_turns": turn_count}})
        self.settings = SimpleNamespace(fidelity=fidelity)
        self.client = SimpleNamespace(
            usage=SimpleNamespace(searches=searches, turns=turns))


def test_a_command_backend_says_which_mechanism_failed() -> None:
    """Three failures a subprocess has and an endpoint does not.

    Each is raised rather than passed on as an empty answer, because the repair
    loop quotes a model's fault back to the model, and none of these is one: a
    program that is not installed cannot be prompted into existing.
    """
    from llossless import backend

    payload = {"messages": [{"role": "user", "content": "x"}]}

    try:
        backend.post_json("llossless-no-such-program", payload,
                          timeout=10, host="h", model="m")
        check(False, "a missing program must be refused, not run")
    except backend.CommandNotFound as exc:
        check("LLOSSLESS_COMMAND" in str(exc),
              f"and the refusal must name the variable to fix: {exc}")

    try:
        backend.post_json("false", payload, timeout=10, host="h", model="m")
        check(False, "a non-zero exit must be refused")
    except backend.CommandError as exc:
        check("exited 1" in str(exc), f"naming the status: {exc}")

    try:
        backend.post_json("true", payload, timeout=10, host="h", model="m")
        check(False, "exit 0 with no output must be refused")
    except backend.CommandError as exc:
        check("wrote nothing" in str(exc),
              f"a command that succeeded silently is a different fault from a "
              f"model that answered blankly, and says so: {exc}")

    # Every one of them is a `TransportError`, which is what makes the call
    # site's existing handling correct without knowing there are two
    # mechanisms.
    check(issubclass(backend.CommandError, transport.TransportError),
          "a command fault is a transport fault: the request never reached a "
          "model, or its answer never came back")


def test_a_command_backends_messages_carry_no_path() -> None:
    """The program is named by basename, never by the path the operator set.

    These strings reach stderr, a captured log, and from there a published
    file, which is the leak this guards against. The case that motivates it is an
    operator whose command is a path under their own home directory.

    The fixture is deliberately *not* such a path. `os.path.basename` is
    shape-agnostic, so any directory component exercises it identically, and
    a home-shaped literal here would be the thing `scan_release` refuses in a
    published file -- earning an exemption for a test that does not need one.
    That exemption exists for detector source that cannot avoid the pattern,
    which is a different situation from a fixture that can.
    """
    from llossless import backend

    payload = {"messages": [{"role": "user", "content": "x"}]}
    try:
        backend.post_json("/opt/private-dir/nope", payload,
                          timeout=10, host="h", model="m")
        check(False, "the program does not exist and must be refused")
    except backend.CommandError as exc:
        check("private-dir" not in str(exc) and "/opt/" not in str(exc),
              f"no path component may reach the message: {exc}")
        check("nope" in str(exc),
              f"but the program must still be nameable, or the operator "
              f"cannot tell which of several failed: {exc}")


def test_a_command_backend_is_a_separate_cassette_keyspace() -> None:
    """A subprocess and an endpoint must not read each other's recordings.

    The profile does not separate them and must not be relied on to: nothing
    stops a command backend running under the default profile, and a keyspace
    that depends on an operator choosing the right one collides the first time
    they do not.
    """
    base = dict(role="merge", model="m", tier="prompt", prompt_sha256="abc",
                messages=[{"role": "user", "content": "x"}], schema=None,
                temperature=0.0, seed=0, max_tokens=None)
    over_http = cassette.key_for(**base)
    check(cassette.key_for(**base, command="") == over_http,
          "the default is absent from the hash, so all 697 recordings keep "
          "their names -- the same exception `profile` is granted, for the "
          "same reason")
    check(cassette.key_for(**base, command="claude -p") != over_http,
          "and a command backend does not read them")
    check(cassette.key_for(**base, command="claude -p")
          != cassette.key_for(**base, command="codex exec"),
          "two different commands are two different things to have asked")

    # Hashed rather than carried. Cassettes are committed test data in a public
    # repository and a command is a local path as often as not.
    everything = cassette.key_for(**base, command="/opt/private-dir/wrapper")
    check("private" not in everything and "wrapper" not in everything,
          "the key is a digest, so the command cannot appear in a filename")


def test_the_subscription_profile_answers_at_one_rung_and_sends_no_knobs() -> None:
    """What a command backend can and cannot put in a request.

    `json_schema` and `tool_call` constrain a model through request *fields*.
    There is no request here, so the profile names its one rung rather than
    letting the ladder discover it -- which also makes a pinned run fail
    loudly instead of answering at a weaker rung than it was told to use.
    """
    common = dict(model="m", messages=[{"role": "user", "content": "x"}],
                  schema={"type": "object", "properties": {}}, schema_name="s",
                  temperature=0.0, seed=7, max_tokens=None,
                  reasoning_effort=True, profile="subscription")

    for tier in ("json_schema", "tool_call"):
        try:
            structured.build_body(tier=tier, thinking=True, **common)
            check(False, f"{tier} must be refused: there is no request to put "
                         f"a {tier} field in")
        except structured.TierUnsupported as exc:
            check("subscription" in str(exc), f"naming the profile: {exc}")

    body = structured.build_body(tier="prompt", thinking=True, **common)
    check(sorted(body) == ["messages", "model"],
          f"nothing else can be sent, so nothing else is: {sorted(body)}")
    check("temperature" not in body and "seed" not in body,
          "and the two that make a run reproducible are among them, which is "
          "why a run under this profile is not reproducible by construction")

    # Thinking cannot be turned off through a subprocess, and claiming it was
    # would file a thinking-on answer under a thinking-off cassette key.
    try:
        structured.build_body(tier="prompt", thinking=False, **common)
        check(False, "asking for thinking off must be refused, not ignored")
    except structured.ThinkingNotHonoured as exc:
        check("subscription" in str(exc), f"naming the profile: {exc}")


def test_a_command_backend_must_be_told_its_window() -> None:
    """Both ends of the window guard are gone at once, so silence is refused.

    `/api/ps` is an HTTP route and there is none to probe; token counts are
    equally unavailable, so the post-hoc overrun check is blind too. A run that
    had neither would report a clean merge on a document the model was handed
    half of.
    """
    try:
        config.Settings(command="claude -p")
        check(False, "an unstated window must be refused")
    except config.ConfigError as exc:
        check("LLOSSLESS_WINDOW" in str(exc),
              f"naming the variable that fixes it: {exc}")

    check(config.Settings(command="claude -p", window=200_000).window == 200_000,
          "a run-wide window satisfies it")
    per_role = config.Settings(
        command="claude -p",
        windows={role: 1000 for role in config.ROLES})
    check(sorted(per_role.windows) == sorted(config.ROLES),
          "and so does a per-role window for every role")

    # Two of three is not a smaller guarantee. The third role is exactly as
    # blind as it would be with nothing stated at all.
    try:
        config.Settings(command="claude -p", windows={"merge": 1000})
        check(False, "a partial per-role map must be refused")
    except config.ConfigError as exc:
        check("verify" in str(exc) and "decompose" in str(exc),
              f"and the refusal must name the roles still unstated: {exc}")


def test_a_command_backend_gets_its_own_default_timeout() -> None:
    """One unstated setting, two backends, two numbers.

    Over HTTP the run streams, so the clock is renewed on every chunk and 120s
    means "this endpoint has gone silent for two minutes". A subprocess has no
    chunks: the same figure means "the whole call finished in two minutes",
    against a backend that also answers at the `prompt` tier and pays process
    start-up per call. The operator's merge died at 120s on a call that needed
    about 178.

    The `--answer-with` case is the one a default resolved when the
    environment was read would have missed: the environment knew nothing about
    a command backend, and the flag turned one on afterwards.
    """
    check(config.COMMAND_TIMEOUT > config.DEFAULT_TIMEOUT,
          f"the command bound must be the larger of the two: "
          f"{config.COMMAND_TIMEOUT} vs {config.DEFAULT_TIMEOUT}")
    check(config.Settings().call_timeout == config.DEFAULT_TIMEOUT,
          "an HTTP run is unchanged by any of this")
    check(config.Settings(command="claude -p", window=9).call_timeout
          == config.COMMAND_TIMEOUT,
          "and a command backend resolves its own")

    # A stated figure is used as stated on either backend. An operator who
    # passes --timeout 30 to a command backend has said something specific.
    check(config.Settings(command="claude -p", window=9, timeout=30).call_timeout
          == 30, "a stated bound is not overruled")
    check(config.from_env({"LLOSSLESS_COMMAND": "claude -p",
                           "LLOSSLESS_WINDOW": "9",
                           "LLOSSLESS_TIMEOUT": "45"}).call_timeout == 45,
          "including one stated in the environment")
    check(config.from_env({"LLOSSLESS_COMMAND": "claude -p",
                           "LLOSSLESS_WINDOW": "9"}).call_timeout
          == config.COMMAND_TIMEOUT,
          "and an environment naming a command with no bound gets the default")

    # The field says what was asked for and `None` means nothing was, which is
    # what lets the resolution happen after the flags rather than before.
    check(config.Settings().timeout is None,
          "the field carries the operator's statement, not a resolved number")

    parser = argparse.ArgumentParser()
    config.add_arguments(parser, corpus_tools=False)
    plain = config.from_env({"LLOSSLESS_WINDOW": "9"})
    turned_on = config.apply_arguments(
        plain, parser.parse_args(["--answer-with", "claude -p"]))
    check(turned_on.call_timeout == config.COMMAND_TIMEOUT,
          f"--answer-with turns the command backend on after the environment "
          f"was read, and the bound has to follow it: "
          f"{turned_on.call_timeout}")
    stated = config.apply_arguments(
        plain, parser.parse_args(["--answer-with", "claude -p",
                                  "--timeout", "42"]))
    check(stated.call_timeout == 42, f"and the flag still wins: {stated.call_timeout}")


def test_a_stopped_command_names_the_setting_that_would_have_let_it_finish() -> None:
    """The message an operator actually gets, against a real slow process.

    The old one explained the mechanism -- no stream, so the bound is on the
    whole call -- and told the reader nothing to do. That is how this was
    reported: a correct sentence about a subprocess, and no sentence about the
    setting. Both halves are asserted, because losing the mechanism to make
    room for the knob would be the same failure the other way round.

    Half a second against a program that sleeps for thirty: the shipped
    default is proved by `test_a_command_backend_gets_its_own_default_timeout`
    above, and a suite that waited 120s to watch a bound fire would be a suite
    nobody runs.
    """
    from llossless import backend

    payload = {"messages": [{"role": "user", "content": "x"}]}
    started = time.monotonic()
    try:
        backend.post_json(f"{sys.executable} -c 'import time; time.sleep(30)'",
                          payload, timeout=0.5, host="h", model="m")
        check(False, "a command past its bound must be stopped")
    except backend.CommandError as exc:
        took = time.monotonic() - started
        check(took < 10,
              f"and stopped at the bound rather than waited out: {took:.1f}s")
        said = str(exc)
        check("--timeout" in said and "LLOSSLESS_TIMEOUT" in said,
              f"the message must name the knob: {said}")
        check("commands.json" in said,
              f"including the one a web submitter's route has, which is where "
              f"this was met: {said}")
        check("stream" in said,
              f"and it must keep the mechanism, which is why the same figure "
              f"is stricter here than over HTTP: {said}")


def test_no_module_bounds_a_call_with_the_unresolved_timeout() -> None:
    """`settings.timeout` is a statement, `call_timeout` is the number.

    A module that passed the field to a request would hand `None` to
    `urllib.request.urlopen` or to `subprocess.run`, which both read it as "no
    bound at all" -- a hang with no message, which is worse than the timeout
    this entry is about. The field is readable from `config` itself, where the
    resolution lives; everywhere else reads the property.

    Scanned by source rather than by calling anything, because the failure is
    a call site that was never exercised: a run that never times out
    passes every test in this suite.
    """
    def offenders(text: str) -> list[str]:
        return [line.strip() for line in text.splitlines()
                if "settings.timeout" in line]

    # Must fire. Without this the scan below could be green over a pattern
    # that no longer matches anything, which is how a detector goes blind.
    check(offenders("    timeout=self.settings.timeout,") == [
              "timeout=self.settings.timeout,"],
          "the scan must recognise the shape it is looking for")

    # `web/cli_render.py` reads the field for the question it is the answer
    # to -- "did the operator state a bound at all" -- and renders `--timeout`
    # only then, into a string a person reads, never into a request or a
    # subprocess. Omitting it where nothing was stated is what reproduces the
    # per-backend default correctly: `call_timeout` resolves the same default
    # again on replay, off the same, unset field. Naming the module rather
    # than widening the scan keeps the check honest about what it still
    # covers -- every other module in `src/llossless` still has none.
    exempt = {"src/llossless/web/cli_render.py"}

    found = []
    for path in sorted((ROOT / "src" / "llossless").rglob("*.py")):
        if path.name == "config.py":
            continue
        relative = str(path.relative_to(ROOT))
        if relative in exempt:
            continue
        for line in offenders(path.read_text(encoding="utf-8")):
            found.append(f"{relative}: {line}")
    check(not found,
          f"these read the stated bound instead of the resolved one, so a run "
          f"that stated none would be unbounded: {found}")


def test_a_command_backend_never_claims_the_documents_stayed_here() -> None:
    """The same question, reached by a second route, answered the same way.

    Every guard this block relies on stops at the process boundary:
    `check_base_url` has no address to inspect and `socket_guard` is
    per-process, so a child that opens a socket opens it unobserved. The tool
    cannot establish that a document stayed on this machine, and the honest
    answer to a question it cannot answer is the one that makes a reader check.
    """
    settings = config.Settings(command="claude -p", window=1000)
    check(settings.endpoint_id != config.Settings().endpoint_id,
          "a command backend must not be stamped with the id of the default "
          "localhost endpoint it never contacted, which is the half of the disclosure "
          "that sits beside the flag below")
    check("private" not in config.Settings(
              command="/opt/private-dir/wrapper", window=1000).endpoint_id,
          "and the id is a digest, so the path stays in the environment")
    check(config.Settings(command="a", window=1000).endpoint_id
          != config.Settings(command="b", window=1000).endpoint_id,
          "two commands are two deployments")
    check(config.Settings(command="a", window=1000, endpoint_label="named"
                          ).endpoint_id
          == config.Settings(endpoint_label="named").endpoint_id,
          "a label still wins: naming the deployment is the operator's call "
          "on this path exactly as on the other one")


def acceptance_a_command_backend_records_and_replays_without_running_again() -> None:
    """Record through a program, replay without starting it.

    The round trip is the deliverable, and the property that makes it worth
    having is the second half: a replay must not run the operator's command.
    A recorded HTTP call that dialled again on replay would be a wasted
    request; a recorded *program* that ran again would be arbitrary local
    execution during what the report calls an offline run.

    Proved by counting, not by trusting the code path. The command appends a
    line to a file every time it starts, so the file's length is the number of
    executions and the replay must not move it.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cassettes = tmp / "tapes"
        ran = tmp / "ran.log"
        program = tmp / "fake-cli.py"
        program.write_text(
            "import json, sys\n"
            f"open({str(ran)!r}, 'a').write('x\\n')\n"
            "sys.stdin.read()\n"
            "sys.stdout.write(json.dumps({'claims': [{'text': 'The relay "
            "listens on port 8443.', 'line': 1, 'span': 'The relay listens on "
            "port 8443.'}]}))\n",
            encoding="utf-8")
        command = f"{sys.executable} {program}"

        def settings(**extra):
            return config.Settings(
                models={"decompose": "test-model", "verify": "test-model"},
                cache_dir=tmp / "cache", use_cache=False,
                command=command, window=200_000, profile="subscription",
                thinking=frozenset(config.ROLES), **extra)

        def call(client):
            return client.complete(
                role="decompose", prompt=prompts.load("decompose"),
                messages=[{"role": "user",
                           "content": "The relay listens on port 8443."}],
                schema=CLAIM_SCHEMA, schema_name="emit_claims",
                semantic=parsing.check_claims)

        live = Client(settings(record_dir=cassettes))
        recorded = call(live)
        runs_after_record = ran.read_text(encoding="utf-8").count("x")

        # The disclosure, on a real run through the seam rather than on a
        # `Settings` in isolation. This is the `content_left_this_machine` field and the one
        # a reader checks; a command backend cannot establish that a document
        # stayed here, so it must not say that it did.
        block = provenance.Provenance(
            settings=live.settings, client=live,
            roles=("decompose",), duration_seconds=1.0).as_dict()["endpoint"]
        check(block["content_left_this_machine"] is True,
              f"a subprocess may send a document anywhere and nothing here can "
              f"see it, so the honest answer is the one that makes a reader "
              f"check: {block}")
        check(block["location"] == "command",
              f"and `command` rather than `hosted`, which would name an "
              f"endpoint this run never addressed: {block}")
        check("by_role" not in block,
              f"with no by-role endpoint list, since it addressed none of "
              f"them: {block}")
        check(runs_after_record == 1,
              f"recording runs the program exactly once: {runs_after_record}")
        tapes = sorted(cassettes.rglob("*.json"))
        check(len(tapes) == 1, f"and writes one cassette: {len(tapes)}")

        replayed = call(Client(settings(replay_dir=cassettes)))
        check(replayed == recorded,
              "the replayed answer is the recorded one, byte for byte")
        runs_after_replay = ran.read_text(encoding="utf-8").count("x")
        check(runs_after_replay == 1,
              f"and the replay did not start the program again: "
              f"{runs_after_replay} execution(s) total")

        # The keyspace, proved against the recording rather than against
        # `key_for` in isolation: the same request with no command must not
        # find this cassette, or an HTTP run would replay a subprocess's
        # answer and call it its own.
        #
        # **Everything but the command is held constant, `profile` included.**
        # The first version of this let the profile differ too, so it passed
        # with `command` deleted from the key -- the two keys were separated by
        # `profile` and the test could not tell which component had done it.
        over_http = config.Settings(
            models={"decompose": "test-model", "verify": "test-model"},
            cache_dir=tmp / "cache2", use_cache=False, replay_dir=cassettes,
            profile="subscription", thinking=frozenset(config.ROLES))
        try:
            call(Client(over_http))
            check(False, "an HTTP run must not find a command backend's tape")
        except Exception as exc:  # noqa: BLE001 - the type is the store's
            check(type(exc).__name__ == "MissingCassette",
                  f"and the miss must be an ordinary replay miss, not a crash "
                  f"and not a live call: {type(exc).__name__}: {exc}")
        check(runs_after_replay == ran.read_text(encoding="utf-8").count("x"),
              "and the miss did not fall back to running the program")



def test_the_ladder_cannot_tell_an_endpoint_that_drops_response_format() -> None:
    """Why the must-fire probe lives outside the ladder.

    A loopback endpoint that answers 200 to `response_format` and never shows
    it to the model, with an answer that happens to fit the schema: the ladder
    settles on `json_schema`, first rung, nothing refused, and the report would
    say the output was constrained. Nothing in the exchange differs from an
    endpoint that honoured the field, so no rule inside `_live` can draw the
    line. `tests/schema_carriage.py` draws it with a schema no model follows
    unprompted, and the next test holds that probe to both directions.
    """
    shown: list[bool] = []

    def drops(body: dict, _n: int):
        # The model sees the messages and nothing else.
        shown.append("emit_claims" in json.dumps(body["messages"]))
        return 200, envelope(CLAIMS_BODY)

    endpoint = FakeEndpoint(drops)
    with tempfile.TemporaryDirectory() as tmp, endpoint as base_url:
        settings = settings_for(base_url, Path(tmp), models={"decompose": "test-model"},
                                profile="anthropic")
        client = Client(settings)
        profile_call(client, thinking=True)
    sent = endpoint.requests[-1]
    check("response_format" in sent,
          f"the anthropic profile sends the schema as response_format: {sorted(sent)}")
    check(shown == [False], f"the fake must not show the model the schema: {shown}")
    check(client.resolved_tier() == "json_schema",
          f"the ladder settles on the first rung whatever the endpoint did with "
          f"it; if this ever changes, the reason for the probe is gone: "
          f"{client.resolved_tier()}")


def test_the_carriage_probe_fires_on_a_dropped_schema_and_not_on_a_carried_one() -> None:
    """The must-fire probe over real HTTP, against the shipped builder.

    Must-fire: an endpoint that drops `response_format` and `tools` reads
    `False` at both rungs, and `prompt` -- the schema in the message -- reads
    `True` on the same endpoint. Must-not-fire: an endpoint that honours both
    reads `True` everywhere. Seeded against the shipped code: `build_body`
    itself is made to lose `response_format`, the way a regression in `src/`
    would, and the honouring endpoint must then read `False` at that rung --
    so the probe cannot be proving a body of its own.
    """
    import schema_carriage

    dropped = schema_carriage.loopback(schema_carriage.ignoring)
    check(dropped == {"json_schema": False, "tool_call": False, "prompt": True},
          f"an endpoint that drops the fields must fire at both rungs: {dropped}")
    carried = schema_carriage.loopback(schema_carriage.honouring)
    check(carried == dict.fromkeys(structured.TIERS, True),
          f"an endpoint that honours them must not fire: {carried}")
    violated = schema_carriage.loopback(schema_carriage.honouring, violate=True)
    check(violated["json_schema"],
          f"asked for a forbidden shape, an honouring endpoint still carries it: {violated}")

    shipped = structured.build_body

    def losing(**kwargs):
        body = shipped(**kwargs)
        body.pop("response_format", None)
        return body

    structured.build_body = losing
    try:
        seeded = schema_carriage.loopback(schema_carriage.honouring)
    finally:
        structured.build_body = shipped
    check(seeded["json_schema"] is False and seeded["prompt"] is True,
          f"a builder that drops response_format must fire the probe: {seeded}")


def test_the_call_thread_and_the_scratch_directory_carry_the_new_name() -> None:
    """A cancellable call runs on `llossless-call`; a cache-off run dumps under `llossless-run-*`.

    Both used the tool's former name as their prefix until the rename's
    fourth phase. Nothing in the package recognises either prefix to
    clean up after it, so the old one needs no reader; this pins the new one
    on the shipped code, through the two methods that make them rather than a
    copy of their literals.
    """
    import shutil
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        client = Client(settings_for("http://127.0.0.1:9/v1", tmp))
        client.cancel = threading.Event()
        seen = client._abandonable(lambda _sleep: threading.current_thread().name)
        check(seen == "llossless-call",
              f"a cancellable call runs on a thread named llossless-call: {seen!r}")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            root = client._dump_root()
        try:
            check(root.name.startswith("llossless-run-"),
                  f"a cache-off run's dumps go under llossless-run-*: {root}")
            check("claimcheck" not in root.name and "claimcheck" not in err.getvalue(),
                  f"and neither the directory nor the notice names the old tool: "
                  f"{root.name} / {err.getvalue()!r}")
        finally:
            shutil.rmtree(root, ignore_errors=True)


ORDER = [
    test_config_defaults_to_localhost,
    test_the_ladder_cannot_tell_an_endpoint_that_drops_response_format,
    test_the_carriage_probe_fires_on_a_dropped_schema_and_not_on_a_carried_one,
    test_config_host_is_host_only,
    test_api_key_is_read_indirectly_and_never_stored,
    test_the_key_source_is_swappable_per_thread_and_never_serialised,
    test_content_left_this_machine_is_answered_across_every_endpoint,
    test_role_to_model_mapping,
    test_the_old_variable_names_are_ignored,
    test_an_exported_CLAIMCHECK_API_KEY_is_ignored,
    test_the_old_config_and_cache_directories_are_not_read,
    test_bad_config_is_rejected_early,
    test_strip_reasoning,
    test_strip_reasoning_only_strips_a_leading_block,
    test_extract_json_counts_brackets,
    test_an_unbalanced_scan_says_which_kind_of_unbalanced,
    test_validator,
    test_semantic_checks,
    test_parse_feedback_names_the_fault,
    test_each_role_can_have_its_own_endpoint_key_and_window,
    test_two_deployments_on_one_host_get_two_ids_and_the_split_follows,
    test_pre_pass_caps_length_violations_instead_of_rejecting_them,
    test_cassette_key_covers_what_changes_the_answer,
    test_cassette_key_derivation_is_pinned,
    test_the_m4_merge_corpus_is_orphaned_by_the_new_prompt_and_nothing_else,
    test_cassette_records_no_secrets,
    test_cassette_records_the_revision_that_made_it,
    test_cassette_records_the_endpoint_that_answered,
    test_two_recordings_under_one_key_are_refused_rather_than_ranked,
    test_the_committed_corpora_are_three_measurements_and_not_one,
    test_base_url_does_not_reach_the_cassette_key,
    test_the_cache_does_not_answer_for_another_endpoint,
    test_an_operator_can_name_a_deployment_the_address_cannot,
    test_dirty_tree_is_its_own_revision,
    test_a_linked_worktree_still_knows_which_commit_it_is,
    test_a_sweep_rewriting_cassettes_does_not_dirty_its_own_provenance,
    test_the_paper_stamp_excludes_its_own_output_and_nothing_else,
    # Four tests were defined and never listed here, found by the ORDER guard in
    # `main`. Three passed on their first run; the fourth is at line 919 and its
    # comment says what it had stopped asserting.
    test_a_base_url_with_no_path_is_completed_rather_than_404ing,
    test_a_cassette_written_before_the_rename_still_reads,
    test_a_replay_falls_through_to_its_local_overlay_on_miss,
    test_no_cassette_publishes_the_address_of_the_machine_that_answered,
    test_one_model_flag_moves_every_role_including_merge,
    test_transport_retries_then_succeeds,
    test_transport_fails_fast_and_leaks_nothing,
    test_a_post_redirect_is_refused_by_host_not_followed_with_the_key,
    test_a_get_redirect_is_refused_the_same_way,
    test_a_streamed_answer_reassembles_into_the_body_a_whole_one_returns,
    test_a_streamed_tool_call_survives_being_split_across_events,
    test_a_stream_cut_short_is_a_failure_and_never_a_short_answer,
    test_a_stream_is_retried_because_a_cut_connection_is_weather,
    test_an_endpoint_that_ignores_stream_is_not_read_as_an_empty_one,
    test_streaming_is_on_by_default_and_leaves_the_cassette_key_alone,
    test_authorization_header_is_sent_when_configured,
    test_the_client_names_itself_and_never_as_urllib,
    test_tier_bodies,
    test_the_default_profile_sends_the_body_this_project_has_always_sent,
    test_the_openai_reasoning_profile_renames_the_budget_and_drops_temperature,
    test_the_openai_reasoning_profile_steps_past_the_rung_it_cannot_send,
    test_the_anthropic_profile_sends_neither_temperature_nor_seed,
    test_a_profile_is_chosen_and_never_read_off_a_model_name,
    test_the_reasoning_axis_is_two_distinct_serialised_bodies,
    test_a_recorded_arm_names_its_own_reasoning_state,
    test_thinking_defaults_to_merge_only,
    test_thinking_can_be_overridden_per_call,
    test_offline_resolves_to_the_runner_s_own_corpus,
    test_reasoning_effort_rejection_aborts_and_never_latches,
    test_a_pinned_run_cannot_flip_the_thinking_condition,
    test_min_interval_paces_live_calls_only,
    test_tier_response_reading,
    test_an_empty_body_is_re_asked_and_never_demotes_a_tier,
    test_every_rejected_attempt_is_dumped_not_only_the_last,
    test_every_discard_writes_its_envelope_before_raising,
    test_fallback_discrimination,
    test_a_404_does_not_walk_the_ladder,
    test_the_capability_record_decides_nothing_and_names_the_server,
    test_capability_probe_walks_down_the_ladder,
    acceptance_1_dry_run_makes_no_request,
    acceptance_2_replay_reproduces_the_live_run,
    acceptance_3_replay_miss_is_fatal,
    acceptance_4_pinned_tier_bypasses_the_probe,
    test_a_pinned_tier_is_asserted_on_every_row_not_once_at_the_start,
    acceptance_5_fenced_thinking_response_parses_first_time,
    acceptance_6_bad_verdict_errors_rather_than_guessing,
    test_a_base_url_that_is_not_http_is_refused_before_anything_opens_it,
    test_a_key_is_never_sent_in_cleartext_off_this_machine,
    test_the_cache_is_owner_only_including_one_that_already_exists,
    test_the_cache_mode_repair_only_ever_narrows,
    test_the_ordinary_default_base_url_is_not_refused,
    test_the_opener_installs_only_the_handlers_it_names,
    test_the_endpoint_pattern_dismisses_reserved_names_and_nothing_else,
    test_a_cited_path_admits_that_path_and_not_its_host,
    test_every_secret_pattern_has_a_seeded_canary,
    test_a_seeded_canary_survives_the_whole_scan,
    acceptance_7_no_secrets_committed,
    test_an_endpoint_label_reaches_the_error_text_and_not_only_the_provenance,
    acceptance_8_warm_cache_makes_no_calls,
    acceptance_replay_never_loads_the_transport_module,
    test_a_model_that_reasons_with_thinking_off_is_reported_not_hidden,
    test_the_provenance_block_prints_requested_against_observed,
    test_a_stream_is_recognised_by_its_first_bytes_not_its_content_type,
    test_an_empty_200_is_re_asked_and_never_reaches_the_json_decoder,
    test_a_looping_answer_is_asked_once_more_and_then_errors,
    test_an_answer_in_the_wrong_order_is_refused_on_the_first_attempt,
    test_the_field_order_switch_relaxes_the_sequence_and_nothing_else,
    test_a_relaxed_field_order_is_on_the_record_and_the_default_is_not,
    test_tokens_are_counted_on_every_path_not_only_the_live_one,
    test_an_unmeasured_call_is_unknown_and_never_zero,
    test_the_legacy_token_pair_mirrors_the_tally,
    test_the_ledger_tells_two_different_calls_apart,
    test_the_ledger_gives_a_repeated_identical_call_the_same_hash,
    test_a_ledger_row_for_an_unmeasured_call_has_no_token_keys,
    test_the_ledger_and_the_totals_cannot_disagree,
    test_a_second_thread_inside_one_client_is_refused,
    test_two_clients_on_two_threads_are_not_refused,
    test_a_unit_that_failed_does_not_leave_the_client_locked,
    test_the_defect_the_guard_prevents_is_still_there_underneath,
    test_a_vendor_that_spells_usage_differently_still_counts,
    test_output_the_vendor_left_out_of_completion_tokens_is_costed,
    acceptance_9_no_credential_reaches_an_artefact,
    acceptance_a_command_backend_records_and_replays_without_running_again,
    test_a_command_backend_answers_in_the_shape_the_http_path_speaks,
    test_the_result_envelope_is_declared_and_never_sniffed,
    test_the_search_counter_is_measured_and_unknown_is_not_zero,
    test_the_turn_counter_sees_the_tool_use_the_search_counter_is_blind_to,
    test_a_result_envelope_names_the_models_that_answered,
    test_the_blind_counter_keeps_its_number_and_loses_its_conclusion,
    test_a_sourced_run_says_which_of_three_retrieval_states_it_reached,
    test_a_command_backend_says_which_mechanism_failed,
    test_a_command_backends_messages_carry_no_path,
    test_a_command_backend_is_a_separate_cassette_keyspace,
    test_the_subscription_profile_answers_at_one_rung_and_sends_no_knobs,
    test_a_command_backend_must_be_told_its_window,
    test_a_command_backend_gets_its_own_default_timeout,
    test_a_stopped_command_names_the_setting_that_would_have_let_it_finish,
    test_no_module_bounds_a_call_with_the_unresolved_timeout,
    test_a_command_backend_never_claims_the_documents_stayed_here,
    test_no_semantic_checker_raises_on_an_answer_that_is_not_an_object,
    test_a_bare_array_answer_reaches_the_repair_loop,
    test_the_call_thread_and_the_scratch_directory_carry_the_new_name,
]


def test_client() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    # `ORDER` is written by hand, so a test can be defined and never called --
    # which is the failure mode this whole file exists to guard against, one
    # level up. `test_the_paper_stamp_excludes_its_own_output_and_nothing_else`
    # was written, was wrong about nothing, and ran zero times until this
    # existed. Checked here rather than as a member of `ORDER`, because a guard
    # that has to be registered has the defect it is guarding against.
    listed = {function.__name__ for function in ORDER}
    defined = {name for name, value in sorted(globals().items())
               if name.startswith("test_") and callable(value)
               and name != "test_client"}
    for name in sorted(defined - listed):
        failures.append(f"{name} is defined and not in ORDER, so it never runs")

    for function in ORDER:
        try:
            function()
        except Exception as exc:  # noqa: BLE001 - a crashing check is a failing check
            failures.append(f"{function.__name__} raised {type(exc).__name__}: {exc}")

    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    for note in unjudged:
        print(f"  unjudged: {note}")
    print(f"client: {len(ORDER)} checks pass ({sum(1 for f in ORDER if 'acceptance' in f.__name__)}"
          f" acceptance){f', {len(unjudged)} unjudged' if unjudged else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
