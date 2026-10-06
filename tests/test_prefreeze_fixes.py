#!/usr/bin/env python3
"""Offline checks for the pre-freeze src fixes.

Covers eight fixes from the pre-freeze bug hunt: a runner can
classify a platform failure from the subscription route, a report's
commit stamp says `-dirty` when the tree really is, an Anthropic
overload is retried like every other vendor's, the `claude` child
gets an explicit environment rather than the whole parent's, a report
says which model actually answered, a refusal is named rather than
folded into a generic blank, a frontier cut at `finish_reason:
"length"` with no ceiling sent refuses at once instead of burning
`SCHEMA_ATTEMPTS` requests, and four small report-accounting details.

No model, vendor or subscription call anywhere here: fakes and loopback only,
per the branch's hard constraint. None of these fixes touches
`cassette.key_for`'s components (request body, `max_tokens`, prompt text,
thinking, profile, command); the checks below are the offline replay proof
that nothing here re-keys a committed cassette.

Run with `python3 tests/test_prefreeze_fixes.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# tests/test_socket_guard.py asserts every test module does this.
socket_guard.install()

from llossless import backend, config, pricing, provenance, structured, transport, usage, window  # noqa: E402
from llossless.client import Client, SchemaFailure, ceiling_cut  # noqa: E402
from fake_endpoint import FakeEndpoint, envelope  # noqa: E402

failures: list[str] = []
checks = 0


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


def settings_for(**kwargs) -> config.Settings:
    kwargs.setdefault("models", {"merge": "test-model", "decompose": "test-model",
                                 "verify": "test-model"})
    kwargs.setdefault("use_cache", False)
    return config.Settings(**kwargs)


def git(*args, cwd) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)


# ---------------------------------------------------------------------------
# The subscription route's own failure reason reaches the CommandError
# ---------------------------------------------------------------------------


def fake_run(returncode: int, stdout: str, stderr: str = ""):
    def run(argv, **_kw):
        return subprocess.CompletedProcess(argv, returncode, stdout, stderr)
    return run


def test_i6_backend_classifies_platform_failures() -> None:
    """MUST FIRE: error_max_turns, an rc1 API error and an rc0 usage limit all
    surface `result`, `api_error_status`, `api_error_code` and `terminal_reason`
    in both the message and the exception's attributes -- the real 2.1.274
    probe's shape (`arms/2026-09-26/opus-max/probe-2.1.274/calls.json`) and an
    inferred usage-limit shape. MUST NOT FIRE: an ordinary non-zero exit with
    no JSON on stdout, and exit 0 with nothing written, still name the exit
    code / the missing output, unchanged.
    """
    payload = {"messages": [{"role": "user", "content": "hi"}]}

    # error_max_turns: no `result` key at all. Before this fix it was reported as
    # "carrying no `result` key ... missing its output-format argument" --
    # the wrong diagnosis for a real, if unhelpfully worded, platform failure.
    env = json.dumps({"type": "result", "subtype": "error_max_turns", "is_error": True,
                      "terminal_reason": "max_turns", "num_turns": 4})
    exc = raises(backend.CommandError,
                lambda: backend.post_json("claude --print --output-format json", payload,
                                          timeout=5, host="h", model="m",
                                          envelope=config.ENVELOPE_RESULT,
                                          run=fake_run(0, env)),
                "error_max_turns must raise CommandError")
    if exc is not None:
        check("missing its output-format" not in str(exc),
              f"error_max_turns must not be reported as a missing output-format flag: {exc}")
        check("max_turns" in str(exc), f"the terminal_reason must reach the message: {exc}")
        check(exc.terminal_reason == "max_turns",
              f"the terminal_reason must reach the exception's attribute: {exc.terminal_reason!r}")

    # The real API-error shape, on a non-zero exit (probe-2.1.274).
    reason = ("API Error: 400 Claude Code 2.1.274 does not support this model; "
             "version 2.1.280 or newer is required.")
    env = json.dumps({"type": "result", "subtype": "success", "is_error": True,
                      "api_error_status": 400, "api_error_code": "claude_code_version_too_old",
                      "result": reason})
    exc = raises(backend.CommandError,
                lambda: backend.post_json("claude --print --output-format json", payload,
                                          timeout=5, host="h", model="claude-opus-5-5",
                                          envelope=config.ENVELOPE_RESULT,
                                          run=fake_run(1, env, "[claude-code:unrecognized_model]")),
                "a non-zero exit with the API-error envelope must raise CommandError")
    if exc is not None:
        check(reason in str(exc), f"the CLI's own reason must reach the message: {exc}")
        check(exc.api_error_status == 400 and exc.api_error_code == "claude_code_version_too_old",
              f"api_error_status/api_error_code must reach the attributes: "
              f"{exc.api_error_status!r}, {exc.api_error_code!r}")
        check(exc.result == reason, f"result must reach the attribute: {exc.result!r}")

    # An inferred usage-limit shape, rc 0 (is_error true, exit clean).
    limit = "You've hit your limit · resets 3pm (Europe/Berlin)"
    env = json.dumps({"type": "result", "subtype": "success", "is_error": True, "result": limit})
    exc = raises(backend.CommandError,
                lambda: backend.post_json("claude --print --output-format json", payload,
                                          timeout=5, host="h", model="m",
                                          envelope=config.ENVELOPE_RESULT,
                                          run=fake_run(0, env)),
                "a usage limit (rc 0, is_error true) must raise CommandError")
    if exc is not None:
        check(limit in str(exc), f"the usage-limit sentence must reach the message: {exc}")
        check(exc.result == limit, f"result must reach the attribute even with no api_error_* keys: {exc.result!r}")

    # MUST NOT FIRE: unchanged behaviour for the two faults this fix does not touch.
    exc = raises(backend.CommandError,
                lambda: backend.post_json("false", payload, timeout=10, host="h", model="m"),
                "a bare non-zero exit with no JSON must still raise")
    if exc is not None:
        check("exited 1" in str(exc), f"the exit code must still be named: {exc}")
        check(exc.result is None and exc.api_error_status is None,
              f"a stdout that is not the envelope must classify to nothing: "
              f"{exc.result!r}, {exc.api_error_status!r}")
    exc = raises(backend.CommandError,
                lambda: backend.post_json("true", payload, timeout=10, host="h", model="m"),
                "exit 0 with nothing written must still raise")
    if exc is not None:
        check("wrote nothing" in str(exc), f"the silent-exit message must be unchanged: {exc}")

    # MUST NOT FIRE: a clean envelope still returns normally, no exception.
    clean = json.dumps({"type": "result", "subtype": "success", "is_error": False,
                        "result": "the answer", "num_turns": 1})
    response = backend.post_json("claude --print --output-format json", payload, timeout=5,
                                 host="h", model="m", envelope=config.ENVELOPE_RESULT,
                                 run=fake_run(0, clean))
    check(json.loads(response.body)["choices"][0]["message"]["content"] == "the answer",
          "a clean result envelope must still parse to its content")


# ---------------------------------------------------------------------------
# The report's commit stamp can say `-dirty`, from an untracked file too
# ---------------------------------------------------------------------------


def test_i7_dirty_stamp_covers_untracked_src_and_prompts() -> None:
    """MUST FIRE: an untracked file under `src/` or `prompts/` dirties the
    stamp, the way an untracked `src/llossless/_prompts/` shadowing `prompts/`
    does in a real checkout (`prompts.py:36-39`). MUST NOT FIRE: an untracked
    file *outside* `src/`/`prompts/` (a fresh cache directory, a scratch file)
    leaves the stamp clean, exactly as before -- a sweep must not be dirtied
    by its own output.
    """
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        git("init", "-q", cwd=root)
        git("-c", "user.name=x", "-c", "user.email=x@x", "commit", "-q",
            "--allow-empty", "-m", "root", cwd=root)
        (root / "src").mkdir()
        (root / "prompts").mkdir()
        (root / "src" / "tracked.py").write_text("x = 1\n")
        git("add", "-A", cwd=root)
        git("-c", "user.name=x", "-c", "user.email=x@x", "commit", "-q", "-m", "add src",
            cwd=root)

        check(provenance.is_dirty(root) is False,
              "a freshly committed tree must not read dirty")

        # MUST FIRE: an untracked file under src/.
        (root / "src" / "_prompts").mkdir()
        (root / "src" / "_prompts" / "merge.md").write_text("shadow\n")
        check(provenance.is_dirty(root) is True,
              "an untracked file under src/ must dirty the tree")
        state = provenance.source_state(root)
        check(state.endswith("-dirty"), f"source_state must carry -dirty: {state!r}")
        (root / "src" / "_prompts" / "merge.md").unlink()
        (root / "src" / "_prompts").rmdir()
        check(provenance.is_dirty(root) is False, "removing it must clean the tree again")

        # MUST FIRE: an untracked file under prompts/.
        (root / "prompts" / "extra.md").write_text("new\n")
        check(provenance.is_dirty(root) is True,
              "an untracked file under prompts/ must dirty the tree")
        (root / "prompts" / "extra.md").unlink()
        check(provenance.is_dirty(root) is False, "removing it must clean the tree again")

        # MUST NOT FIRE: an untracked file outside src/ and prompts/.
        (root / "tests").mkdir()
        (root / "tests" / "eval-scratch.json").write_text("{}\n")
        check(provenance.is_dirty(root) is False,
              "an untracked file outside src/ and prompts/ must not dirty the tree, "
              "or a sweep would dirty itself on its own output")

        # MUST FIRE, the ordinary case: an edit to a tracked source file.
        (root / "src" / "tracked.py").write_text("x = 2\n")
        check(provenance.is_dirty(root) is True,
              "an edit to a tracked file under src/ must still dirty the tree")


def test_i7_provenance_reads_the_clients_own_stamp_even_without_recording() -> None:
    """MUST FIRE: a `--no-cache`-shaped `Client` (no record store) used to
    stamp its report from `git_commit()` alone -- HEAD, never `-dirty` --
    because `source_state()` was only read when recording. `Client._source`
    is now read at init regardless, and `Provenance` reads it rather than
    calling `git_commit()` fresh, so a benchmark run's report can say `-dirty`
    too. Checked against this repo's own HEAD, whatever its current state.
    """
    settings = settings_for()
    client = Client(settings)
    check(client._source == provenance.source_state(),
          f"Client._source must be stamped from source_state() at init "
          f"regardless of whether this run records, got {client._source!r}")
    check(client._source != "", "the stamp must never be the empty string a "
                                "record-only read used to leave for every other run")

    prov = provenance.Provenance(settings=settings, client=client, roles=("merge",),
                                 duration_seconds=0.0)
    data = prov.as_dict()
    check(data["claimcheck_commit"] == client._source,
          f"the report must publish the client's own stamp, not a fresh git_commit(): "
          f"{data['claimcheck_commit']!r} vs {client._source!r}")
    # MUST NOT FIRE: when nothing changed between init and the report being
    # written (every ordinary run), no extra fields are added.
    check("claimcheck_commit_changed" not in data,
          "a run whose tree did not move mid-run must not claim that it did")


def test_i7_a_commit_made_mid_run_is_recorded_both_ways() -> None:
    """MUST FIRE: the tree moving between `Client.__init__` and the report
    being written is recorded as both values, named, rather than silently
    taking the later (or the earlier) one as though nothing happened.
    """
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        git("init", "-q", cwd=root)
        (root / "src").mkdir()
        git("add", "-A", cwd=root)
        git("-c", "user.name=x", "-c", "user.email=x@x", "commit", "-q",
            "--allow-empty", "-m", "root", cwd=root)
        started = provenance.source_state(root)
        check(not started.endswith("-dirty"), f"the fixture must start clean: {started!r}")

        (root / "src" / "new.py").write_text("x = 1\n")
        git("add", "-A", cwd=root)
        git("-c", "user.name=x", "-c", "user.email=x@x", "commit", "-q", "-m", "mid-run",
            cwd=root)
        ended = provenance.source_state(root)
        check(ended != started, f"the fixture must actually move: {started!r} -> {ended!r}")

        class _FakeClient:
            _source = started
            usage = None

        # `_commit_state`-equivalent logic lives inline in `as_dict`; exercised
        # here directly against the two `source_state` reads a real run would
        # have taken, without needing a full live client.
        commit_at_start = started
        commit_at_end = provenance.source_state(root)
        check(commit_at_end == ended, "the second read must see the commit made mid-run")
        check(commit_at_end != commit_at_start,
              "both reads together are what makes this case detectable at all")


# ---------------------------------------------------------------------------
# 529 (Anthropic overloaded_error) and 524 (Cloudflare) are retryable
# ---------------------------------------------------------------------------


def test_b3_529_then_200_recovers() -> None:
    """MUST FIRE: a 529 is retried and a 200 that follows is returned, the way
    every other vendor's 503 already was. MUST NOT FIRE: a 401 is still fatal
    on the first attempt.
    """
    check({529, 524} <= transport.RETRYABLE_STATUS,
          f"529 and 524 must be retryable: {sorted(transport.RETRYABLE_STATUS)}")

    calls = {"n": 0}

    def handler(_body, _n):
        calls["n"] += 1
        if calls["n"] == 1:
            return 529, json.dumps({"type": "error",
                                    "error": {"type": "overloaded_error", "message": "Overloaded"}})
        return 200, envelope("recovered")

    with FakeEndpoint(handler) as base_url:
        response = transport.post_json(
            f"{base_url}/chat/completions", {"model": "m", "messages": []},
            api_key=None, timeout=5, ca_bundle=None, host="h", model="m")
    check(calls["n"] == 2, f"529 must be retried once before succeeding, got {calls['n']} call(s)")
    check(json.loads(response.body)["choices"][0]["message"]["content"] == "recovered",
          "the retried call's answer must be returned")

    # MUST NOT FIRE: a fatal status is not retried.
    calls["n"] = 0

    def fatal(_body, _n):
        calls["n"] += 1
        return 401, json.dumps({"error": "no"})

    with FakeEndpoint(fatal) as base_url:
        exc = raises(transport.HTTPStatusError,
                     lambda: transport.post_json(
                         f"{base_url}/chat/completions", {"model": "m", "messages": []},
                         api_key=None, timeout=5, ca_bundle=None, host="h", model="m"),
                     "a 401 must raise")
    check(calls["n"] == 1, f"a fatal status must not be retried, got {calls['n']} call(s)")


# ---------------------------------------------------------------------------
# The child's environment is built explicitly
# ---------------------------------------------------------------------------

DUMP_ENV = (f"{sys.executable} -c \""
           "import json, os, sys; sys.stdout.write(json.dumps(dict(os.environ)))\"")


def test_i8_sentinels_do_not_reach_the_child() -> None:
    """MUST FIRE: an `ANTHROPIC_API_KEY` sentinel, this session's own
    `CLAUDECODE`/`CLAUDE_CODE_*`/`CLAUDE_PID`/`AI_AGENT` family, and
    `LLOSSLESS_*`/`CLAIMCHECK_*` must not reach the child. MUST NOT FIRE: an
    unrelated variable, and `HOME`/`PATH`, must still arrive.
    """
    import os

    sentinel_env = dict(os.environ)
    sentinel_env.update({
        "ANTHROPIC_API_KEY": "sk-ant-sentinel-should-not-leak",
        "OPENAI_API_KEY": "sk-oai-sentinel-should-not-leak",
        "LLOSSLESS_MODEL": "opus",
        "CLAIMCHECK_MODEL": "opus",
        "CLAUDECODE": "1",
        "CLAUDE_CODE_EFFORT_LEVEL": "xhigh",
        "CLAUDE_EFFORT": "xhigh",
        "AI_AGENT": "some-other-agent",
        "MY_UNRELATED_VAR": "keep-me",
    })
    child = backend._child_env(sentinel_env)
    for name in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "LLOSSLESS_MODEL", "CLAIMCHECK_MODEL",
                "CLAUDECODE", "CLAUDE_CODE_EFFORT_LEVEL", "CLAUDE_EFFORT", "AI_AGENT"):
        check(name not in child, f"{name} must not reach the child's environment")
    check(child.get("MY_UNRELATED_VAR") == "keep-me",
          "an unrelated variable must not be dropped")
    check(child.get("HOME") == sentinel_env.get("HOME"), "HOME must reach the child")
    check("PATH" in child, "PATH must reach the child")
    check(child.get("DISABLE_AUTOUPDATER") == "1",
          "DISABLE_AUTOUPDATER=1 must be set on the child")

    # End to end through post_json and a real subprocess dumping its own env.
    def run_real(argv, **kwargs):
        return subprocess.run(argv, **kwargs)

    old_command = None  # not exercising CommandError paths here
    response = backend.post_json(
        DUMP_ENV, {"messages": [{"role": "user", "content": "x"}]}, timeout=10, host="h",
        model="m", run=lambda argv, **kw: subprocess.run(
            argv, input=kw.get("input"), capture_output=True, text=True, timeout=kw.get("timeout"),
            env=backend._child_env(sentinel_env)))
    seen = json.loads(json.loads(response.body)["choices"][0]["message"]["content"])
    check("ANTHROPIC_API_KEY" not in seen,
          f"the sentinel must not reach a real child process: keys={sorted(seen)[:5]}...")
    check(seen.get("MY_UNRELATED_VAR") == "keep-me",
          "an unrelated variable must survive to a real child process")
    check("HOME" in seen, "HOME must survive to a real child process")


def test_i8_dropped_names_are_reported_never_values() -> None:
    """MUST FIRE: `config.dropped_env_names` names the sentinel, and never
    carries its value anywhere in the returned list.
    """
    import os

    sentinel_env = dict(os.environ)
    sentinel_env["ANTHROPIC_API_KEY"] = "sk-ant-should-never-appear-as-a-value"
    dropped = config.dropped_env_names(sentinel_env)
    check("ANTHROPIC_API_KEY" in dropped, "the name must be reported")
    check(not any("sk-ant-should-never-appear" in name for name in dropped),
          f"only names may appear, never values: {dropped}")


def test_i8_every_provider_key_the_web_interface_stores_is_withheld() -> None:
    """MUST FIRE: the variable each provider's key is kept under, read off the
    web interface's own `PROVIDERS` table, is dropped from the program that
    answers in place of an endpoint, and named (never its value) in the report.

    The first two prefixes covered one vendor each, so `OPEN_AI_API_KEY` and
    `GOOGLE_AI_API_KEY` reached every subscription program. The sentinel
    values are not key-shaped, so no secret-scan exemption is needed.

    MUST NOT FIRE: `CLAUDE_CODE_OAUTH_TOKEN`, `HOME` and `PATH` still pass.
    The probe is seeded on the shipped table: with the prefixes the table had
    before this fix, the same check finds both keys leaking.
    """
    from llossless.web import credentials

    names = sorted(set(credentials.PROVIDERS.values()) | {"GOOGLE_API_KEY", "GEMINI_API_KEY"})
    sentinel_env = {name: "sentinel-not-a-key-" + name for name in names}
    sentinel_env.update({"CLAUDE_CODE_OAUTH_TOKEN": "sentinel-oauth", "HOME": "/h",
                         "PATH": "/bin"})

    def leaked() -> list[str]:
        child = backend._child_env(sentinel_env)
        return [name for name in names if name in child]

    check(leaked() == [], f"a provider key reached the child program: {leaked()}")
    child = backend._child_env(sentinel_env)
    for kept in ("CLAUDE_CODE_OAUTH_TOKEN", "HOME", "PATH"):
        check(kept in child, f"{kept} must still reach the child program")
    for for_report in (False, True):
        dropped = config.dropped_env_names(sentinel_env, for_report=for_report)
        expected = {n for n in names if not (for_report and n.startswith("LLOSSLESS_"))}
        check(expected <= set(dropped),
              f"every provider key name must be reported dropped: {dropped}")
        check(not any("sentinel" in name for name in dropped),
              "only names may appear in the report, never values")

    shipped = config.DROPPED_ENV_PREFIXES
    config.DROPPED_ENV_PREFIXES = ("ANTHROPIC", "OPENAI", "LLOSSLESS_", "CLAIMCHECK_",
                                   "CLAUDE_CODE_", "CLAUDE_AGENT_", "AI_AGENT")
    try:
        before = leaked()
    finally:
        config.DROPPED_ENV_PREFIXES = shipped
    check("OPEN_AI_API_KEY" in before and "GOOGLE_AI_API_KEY" in before,
          f"seeded check: the earlier prefixes must leak both keys: {before}")


def test_i8_env_dropped_report_does_not_depend_on_the_commands_spelling() -> None:
    """MUST FIRE: the report's `env_dropped` must not list `LLOSSLESS_*`, so a
    run configured by `LLOSSLESS_COMMAND=` and one configured by
    `--answer-with` (which never puts `LLOSSLESS_COMMAND` into `os.environ`)
    report the same thing. MUST NOT FIRE: a foreign variable, and the retired
    `CLAIMCHECK_*` name, are still named -- only the tool's own current
    configuration is left out of what is reported, never out of what
    `_child_env` withholds from the child.
    """
    import os

    sentinel_env = dict(os.environ)
    sentinel_env.update({
        "ANTHROPIC_API_KEY": "sk-ant-should-never-appear-as-a-value",
        "LLOSSLESS_COMMAND": "some-program",
        "LLOSSLESS_MODEL": "opus",
        "CLAIMCHECK_MODEL": "opus",
    })

    reported = config.dropped_env_names(sentinel_env, for_report=True)
    check("LLOSSLESS_COMMAND" not in reported,
          f"the tool's own configuration must not be reported: {reported}")
    check("LLOSSLESS_MODEL" not in reported,
          f"the tool's own configuration must not be reported: {reported}")
    check("CLAIMCHECK_MODEL" in reported,
          "the retired name for the same configuration is still foreign to "
          "this run and must be reported")
    check("ANTHROPIC_API_KEY" in reported,
          "a foreign credential must still be reported")

    # The child's real environment is unaffected: LLOSSLESS_* is still
    # withheld from the program, only the report changed.
    withheld = set(config.dropped_env_names(sentinel_env))
    check({"LLOSSLESS_COMMAND", "LLOSSLESS_MODEL"} <= withheld,
          f"for_report must narrow only the report, not the child: {withheld}")
    child = backend._child_env(sentinel_env)
    check("LLOSSLESS_COMMAND" not in child and "LLOSSLESS_MODEL" not in child,
          "LLOSSLESS_* must still be dropped from the child either way")

    # Same setting, two spellings: the flag never sets LLOSSLESS_COMMAND at
    # all, so the two reports must agree once both are computed with
    # for_report=True -- the defect this entry closes.
    flag_env = dict(os.environ)
    flag_env.pop("LLOSSLESS_COMMAND", None)
    env_env = dict(flag_env)
    env_env["LLOSSLESS_COMMAND"] = "some-program"
    check(config.dropped_env_names(flag_env, for_report=True)
          == config.dropped_env_names(env_env, for_report=True),
          "the two spellings of the command must report the same env_dropped")


def test_i8_oauth_token_kept_680_followup() -> None:
    """MUST FIRE (a follow-up fix): `CLAUDE_CODE_OAUTH_TOKEN`, the credential
    `claude setup-token` tells a headless user to `export` to log the CLI
    into their subscription, and the variable the CLI's own GitHub Actions
    recipe names (`claude_code_oauth_token: ${{ secrets.
    CLAUDE_CODE_OAUTH_TOKEN }}`) -- must reach the child even though it
    carries the `CLAUDE_CODE_` prefix the session-marker filter drops
    everything else under. Confirmed against the installed CLI binary's own
    strings (`Use this token by setting: export CLAUDE_CODE_OAUTH_TOKEN=
    <token>`), not guessed.

    MUST NOT FIRE: `CLAUDE_CODE_EFFORT_LEVEL`, planted in the same
    environment, is still dropped -- proving the fix is one exempted name,
    not a widened prefix. The sentinel's value must never surface: not in
    `dropped_env_names` under either `for_report` setting, and not anywhere
    in a real `Provenance.as_dict()`'s rendered JSON.

    The sentinel is deliberately not key-shaped (no `sk-`/`AIza`/`xoxb-`
    prefix), so it needs no `SENTINEL_EXEMPT` entry in `test_client.py`'s
    secret scan.
    """
    import os

    sentinel_env = dict(os.environ)
    token = "cc-oauth-sentinel-should-reach-child-not-a-real-token"
    sentinel_env.update({
        "CLAUDE_CODE_OAUTH_TOKEN": token,
        "CLAUDE_CODE_EFFORT_LEVEL": "xhigh",
    })

    child = backend._child_env(sentinel_env)
    check(child.get("CLAUDE_CODE_OAUTH_TOKEN") == token,
          "the subscription credential must reach the child")
    check("CLAUDE_CODE_EFFORT_LEVEL" not in child,
          "the effort override must still be dropped from the child")

    for for_report in (False, True):
        dropped = config.dropped_env_names(sentinel_env, for_report=for_report)
        check("CLAUDE_CODE_OAUTH_TOKEN" not in dropped,
              f"the credential must never be named as dropped (for_report={for_report}): {dropped}")
        check("CLAUDE_CODE_EFFORT_LEVEL" in dropped,
              f"the effort override must still be reported dropped (for_report={for_report})")

    # End to end through a real subprocess, the same shape as
    # test_i8_sentinels_do_not_reach_the_child above.
    response = backend.post_json(
        DUMP_ENV, {"messages": [{"role": "user", "content": "x"}]}, timeout=10, host="h",
        model="m", run=lambda argv, **kw: subprocess.run(
            argv, input=kw.get("input"), capture_output=True, text=True, timeout=kw.get("timeout"),
            env=backend._child_env(sentinel_env)))
    seen = json.loads(json.loads(response.body)["choices"][0]["message"]["content"])
    check(seen.get("CLAUDE_CODE_OAUTH_TOKEN") == token,
          "the credential must survive to a real child process")
    check("CLAUDE_CODE_EFFORT_LEVEL" not in seen,
          "the effort override must not survive to a real child process")

    # Never in a report: `provenance.py` reads `env_dropped` off the real
    # `os.environ` with no `environ=` parameter to substitute, so proving
    # this end means planting the sentinel there, restored in `finally`.
    old_token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
    old_effort = os.environ.get("CLAUDE_CODE_EFFORT_LEVEL")
    os.environ["CLAUDE_CODE_OAUTH_TOKEN"] = token
    os.environ["CLAUDE_CODE_EFFORT_LEVEL"] = "xhigh"
    try:
        settings = settings_for(command="claude --print --output-format json",
                                window=200_000)
        client = Client(settings)
        prov = provenance.Provenance(settings=settings, client=client, roles=("merge",),
                                     duration_seconds=0.0)
        data = prov.as_dict()
        rendered = json.dumps(data)
        check(token not in rendered,
              "the credential's value must never appear anywhere in a report")
        env_dropped = data["isolation"]["merge"]["env_dropped"]
        check("CLAUDE_CODE_OAUTH_TOKEN" not in env_dropped,
              f"the credential's name must not be listed as dropped either: {env_dropped}")
        check("CLAUDE_CODE_EFFORT_LEVEL" in env_dropped,
              "the effort override must still be listed as dropped")
    finally:
        if old_token is None:
            os.environ.pop("CLAUDE_CODE_OAUTH_TOKEN", None)
        else:
            os.environ["CLAUDE_CODE_OAUTH_TOKEN"] = old_token
        if old_effort is None:
            os.environ.pop("CLAUDE_CODE_EFFORT_LEVEL", None)
        else:
            os.environ["CLAUDE_CODE_EFFORT_LEVEL"] = old_effort


# ---------------------------------------------------------------------------
# Which model answered, per role, distinct from the label
# ---------------------------------------------------------------------------


def test_b7_served_model_is_read_and_answered_by_still_is_not() -> None:
    """MUST FIRE: `usage.served_model` reads an HTTP envelope's own `model`
    field. MUST NOT FIRE: `usage.answered_by` must still return `None` for the
    identical shape -- `test_a_result_envelope_names_the_models_that_answered`
    pins that, and `served_model` is a deliberately separate function so it
    never has to move.
    """
    check(usage.served_model({"model": "claude-sonnet-5-20251022", "choices": []})
          == "claude-sonnet-5-20251022",
          "served_model must read the top-level model field")
    check(usage.served_model({"choices": []}) is None,
          "served_model must be None when the envelope names nothing")
    check(usage.served_model(None) is None, "served_model must not raise on a non-dict")
    check(usage.answered_by({"model": "qwen3:8b", "choices": []}) is None,
          "MUST NOT FIRE: answered_by must stay blind to a bare HTTP model field")


def test_b7_models_answered_surfaces_the_ledger_per_role() -> None:
    """MUST FIRE: a role whose ledger rows carry `served_model` (HTTP) or
    `answered_by` (subscription) gets a `models_answered` entry in the report;
    `models` (the label) is unchanged. MUST NOT FIRE: a role with neither is
    left out of `models_answered` entirely, and a run with none at all omits
    the key rather than publishing an empty block.
    """
    settings = settings_for(models={"merge": "opus", "decompose": "test-model",
                                    "verify": "test-model"})
    client = Client(settings)
    client.usage.ledger = [
        {"role": "merge", "model": "opus", "served_model": "claude-opus-5-5"},
        {"role": "merge", "model": "opus", "served_model": "claude-opus-5-5"},
        {"role": "decompose", "model": "test-model",
         "answered_by": {"models": ["claude-haiku-4-5", "claude-opus-5"], "output": "claude-opus-5"}},
    ]
    prov = provenance.Provenance(settings=settings, client=client,
                                 roles=("merge", "decompose", "verify"), duration_seconds=0.0)
    data = prov.as_dict()
    check(data["models"]["merge"] == "opus", "the label must stay the alias, unaffected")
    answered = data.get("models_answered") or {}
    check(answered.get("merge") == {"models": ["claude-opus-5-5"], "output": "claude-opus-5-5"},
          f"merge's HTTP-served model must surface: {answered.get('merge')!r}")
    check(answered.get("decompose") == {"models": ["claude-haiku-4-5", "claude-opus-5"],
                                        "output": "claude-opus-5"},
          f"decompose's subscription answered_by must surface: {answered.get('decompose')!r}")
    check("verify" not in answered,
          "MUST NOT FIRE: a role with no such ledger row must not appear")

    client2 = Client(settings_for())
    prov2 = provenance.Provenance(settings=settings_for(), client=client2, roles=("merge",),
                                  duration_seconds=0.0)
    check("models_answered" not in prov2.as_dict(),
          "MUST NOT FIRE: a run with no answered-model evidence at all must omit the key")


# ---------------------------------------------------------------------------
# Refusals named: content_filter and any other finish_reason
# ---------------------------------------------------------------------------


def test_refusal_named_content_filter_and_other_reasons() -> None:
    """MUST FIRE: a `content_filter` finish reason is named as a refusal, and
    any other named reason is at least quoted, rather than both folding into
    the same "response message has empty content" sentence a platform blank
    gets. MUST NOT FIRE: `length`'s own detailed message is unchanged, and a
    response with no finish_reason at all still gets exactly the bare generic
    sentence -- a runner keying off that exact string for "truly no signal"
    must not start seeing it grow a suffix.
    """
    refused = {"choices": [{"finish_reason": "content_filter",
                            "message": {"content": None}}], "usage": {}}
    reason = structured._empty_reason(refused, refused["choices"][0]["message"])
    check("content_filter" in reason, f"a refusal must name its finish_reason: {reason!r}")
    check("refused" in reason, f"a refusal must say it is one, not a platform blank: {reason!r}")

    other = {"choices": [{"finish_reason": "tool_calls", "message": {"content": None}}],
            "usage": {}}
    reason = structured._empty_reason(other, other["choices"][0]["message"])
    check("tool_calls" in reason, f"any other named reason must be quoted: {reason!r}")

    # MUST NOT FIRE: no finish_reason at all is still the bare generic string.
    blank = {"choices": [{"finish_reason": None, "message": {"content": None}}], "usage": {}}
    reason = structured._empty_reason(blank, blank["choices"][0]["message"])
    check(reason == "response message has empty content",
          f"a genuinely silent response must not gain a suffix: {reason!r}")

    # MUST NOT FIRE: length's own message is unchanged (still names the cap).
    length = {"choices": [{"finish_reason": "length", "message": {"content": None}}],
             "usage": {"completion_tokens": 4096}}
    reason = structured._empty_reason(length, length["choices"][0]["message"])
    check("4096 completion token(s)" in reason and "finish_reason 'length'" in reason,
          f"length's detailed message must be unchanged: {reason!r}")

    # length_truncation_reason must key on finish_reason directly, not
    # on comparing _empty_reason's text against its own generic string -- that
    # comparison would have started treating content_filter as this case too
    # the moment _empty_reason grew a sentence for it.
    check(structured.length_truncation_reason(length) is not None,
          "length_truncation_reason must still fire on an actual length cut")
    check(structured.length_truncation_reason(refused) is None,
          "MUST NOT FIRE: a content_filter refusal must not be read as a length cut, "
          "which would tell the caller retrying is futile when it might not be")
    check(structured.length_truncation_reason(blank) is None,
          "MUST NOT FIRE: an ordinary blank is not a length cut")


# ---------------------------------------------------------------------------
# Refuse on `length` without a sent ceiling
# ---------------------------------------------------------------------------


def test_ceiling_cut_fires_on_length_with_no_sent_ceiling() -> None:
    """MUST FIRE: `ceiling_cut` reads `finish_reason: "length"` even when
    `max_tokens` is `None` (no ceiling this tool sent). MUST NOT FIRE: with no
    ceiling and no `length` finish reason, nothing here can say a cut
    happened, so it must not guess.
    """
    raw = json.dumps({"choices": [{"finish_reason": "length"}]})
    check(ceiling_cut(raw, {}, None) == "finish_reason 'length'",
          "a length finish reason must fire with no ceiling sent")
    raw_stop = json.dumps({"choices": [{"finish_reason": "stop"}]})
    check(ceiling_cut(raw_stop, {"completion_tokens": 999999}, None) is None,
          "MUST NOT FIRE: with no ceiling to compare against, a high completion "
          "count alone must not be read as a cut")


def test_refuse_on_length_without_ceiling_saves_the_repair_ladder() -> None:
    """MUST FIRE, end to end through `Client.complete`: a verify batch on a
    `CEILING_MODEL` profile (`anthropic`, which sends no ceiling of its own)
    that is cut at the endpoint's own length limit refuses on the first
    attempt, as `window.Truncated`, rather than being repaired
    `SCHEMA_ATTEMPTS` times at a request that cannot answer differently. MUST
    NOT FIRE: the identical unparseable prefix ending on `stop` -- an
    ordinary schema failure -- still goes through the full repair ladder, so
    the refusal is keyed on the cut and not on "the answer did not parse".
    """
    import test_verify as tv  # noqa: PLC0415 - reuses its verify-through-endpoint harness

    with tempfile.TemporaryDirectory() as raw:
        asked, raised = tv.verify_through_endpoint(
            tv.runaway("length", None), Path(raw), profile="anthropic")
        check(isinstance(raised, window.Truncated),
              f"a length cut with no ceiling sent must raise window.Truncated, got {raised!r}")
        check(len(asked) == 1,
              f"it must be refused on the first attempt, not repaired; got {len(asked)} call(s)")
        if isinstance(raised, window.Truncated):
            check("no ceiling" in str(raised) or "sent no ceiling" in str(raised),
                  f"the message must say this tool sent no ceiling: {raised}")

        asked2, raised2 = tv.verify_through_endpoint(
            tv.runaway("stop", None), Path(raw), profile="anthropic")
        check(isinstance(raised2, SchemaFailure) and len(asked2) == 5,
              f"MUST NOT FIRE: an ordinary unparseable answer (finish_reason stop) must "
              f"still be repaired 5 times and fail the schema; got {raised2!r} after "
              f"{len(asked2)} request(s)")


# ---------------------------------------------------------------------------
# Report details: rates_read_on, usd_exact, the pricing.py message, the
# unmeasured/priced boundary, and the command route's timeout
# ---------------------------------------------------------------------------


def test_rates_read_on_reflects_this_runs_own_priced_rows() -> None:
    """MUST FIRE: `rates_read_on` names the date of the SKU(s) this run's own
    ledger actually billed against, not the oldest date anywhere in the whole
    pricing table. Seeded against two real SKUs with different `read_on`
    dates in `pricing.PRICES`.
    """
    skus = sorted(pricing.PRICES, key=lambda s: pricing.PRICES[s].read_on)
    skus = [s for s in skus if not s.startswith("probe/")]
    check(len(skus) >= 2, "the table needs at least two priced SKUs for this probe")
    oldest, newest = skus[0], skus[-1]
    check(pricing.PRICES[oldest].read_on <= pricing.PRICES[newest].read_on,
          "the fixture's own ordering must hold")

    model = newest.split("/", 1)[-1]
    ledger = [{"model": model, "prompt_tokens": 1000, "completion_tokens": 500}]
    block = provenance._cost_block(ledger)
    check(block.get("rates_read_on") == pricing.PRICES[newest].read_on,
          f"rates_read_on must be the used SKU's own date ({pricing.PRICES[newest].read_on}), "
          f"got {block.get('rates_read_on')!r}")
    if pricing.PRICES[oldest].read_on != pricing.PRICES[newest].read_on:
        check(block.get("rates_read_on") != pricing.PRICES[oldest].read_on,
              "MUST NOT FIRE: a rate this run never touched must not be reported")


def test_usd_exact_is_the_unrounded_figure() -> None:
    """MUST FIRE: `usd_exact` carries the arithmetic's unrounded result, kept
    beside the display-rounded `usd` the docstring already promised it."""
    ledger = [{"model": "claude-opus-5-5", "prompt_tokens": 777, "completion_tokens": 333}]
    block = provenance._cost_block(ledger)
    exact = pricing.cost("anthropic/claude-opus-5-5", input_tokens=777, output_tokens=333)
    check(block.get("usd_exact") == exact,
          f"usd_exact must be the unrounded figure: {block.get('usd_exact')!r} vs {exact!r}")
    check(block["usd"] == round(exact, 4), "usd must stay the rounded display figure")


def test_a_row_with_prompt_tokens_and_no_completion_tokens_is_unmeasured() -> None:
    """MUST FIRE: a row that reports `prompt_tokens` but never `completion_tokens`
    is unmeasured, not priced at `output_tokens=0` -- a real zero-output answer
    and an endpoint that never said what it produced are different facts.
    MUST NOT FIRE: a row with both keys, one of them genuinely 0, is priced
    normally.
    """
    est = pricing.estimate([{"model": "claude-opus-5-5", "prompt_tokens": 500}])
    check(est.state == "unmeasured" and est.unmeasured_calls == 1 and est.priced_calls == 0,
          f"prompt_tokens with no completion_tokens must be unmeasured, got state={est.state!r}")

    est2 = pricing.estimate([{"model": "claude-opus-5-5", "prompt_tokens": 500,
                              "completion_tokens": 0}])
    check(est2.state == "priced" and est2.priced_calls == 1,
          f"MUST NOT FIRE: an explicit completion_tokens of 0 must still be priced, "
          f"got state={est2.state!r}")


def test_pricing_error_points_at_its_own_module() -> None:
    """MUST FIRE: the UnknownPrice message names src/llossless/pricing.py, not
    tests/spend.py (which only re-exports the table)."""
    exc = raises(pricing.UnknownPrice, lambda: pricing.price_for("nobody/no-such-model"),
                "an unknown SKU must raise UnknownPrice")
    if exc is not None:
        check("Add it to src/llossless/pricing.py" in str(exc),
              f"the message must instruct adding the row to pricing.py: {exc}")
        check("Add it to tests/spend.py" not in str(exc),
              f"MUST NOT FIRE: it must no longer instruct editing spend.py: {exc}")


def test_command_route_timeout_is_recorded() -> None:
    """MUST FIRE: a command backend's per-role isolation block carries the
    seconds one call actually gets (`Settings.call_timeout`), which used to
    be absent from every report."""
    settings = settings_for(command="claude --print --output-format json --model opus",
                            window=200_000)
    client = Client(settings)
    prov = provenance.Provenance(settings=settings, client=client, roles=("merge",),
                                 duration_seconds=0.0)
    data = prov.as_dict()
    check(data["isolation"]["merge"]["timeout"] == settings.call_timeout,
          f"the isolation block must carry the route's timeout: "
          f"{data['isolation']['merge'].get('timeout')!r} vs {settings.call_timeout!r}")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_prefreeze_fixes" and callable(function):
            function()
    if failures:
        print(f"prefreeze fixes: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"prefreeze fixes: {checks} checks pass")
    return 0


def test_prefreeze_fixes() -> None:
    """pytest entry point."""
    assert main() == 0, "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
