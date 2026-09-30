#!/usr/bin/env python3
"""`web/cli_render.py`: the round trip, and the two things that must never appear.

The whole of what this block is for is stated in `cli_render.py`'s own
module docstring: showing the equivalent CLI command for a run. So what
this file asserts is not "does it look plausible" but "does the CLI, fed
exactly this rendered text through its own argument parser and its own
environment resolution, arrive at the same settings the job ran with". A
command that reads correctly and parses to something else is the
harder-to-notice version of the defect this test exists to catch.

**The round trip is real, not simulated.** `cli.build_parser()` is the actual
parser `llossless` builds from `sys.argv`; `config.resolve` is the actual
resolution `cli.main` calls. Nothing here stubs either half.

**What "equal" means is stated once, in `_comparable`, and it is not "every
field of `Settings` byte for byte".** A command route's own program is never
rendered -- `cli_render`'s docstring gives the reason, `web/commands.py`'s
gives the one underneath it -- so a rendered `--answer-with` carries a
placeholder, and `effort_of`'s resolution of an effort level is gated on the
program's own basename being one this build has read (`config.py`'s
`AUTO_EFFORT` table). Comparing the *resolved* effort level across that
substitution would fail for a reason that has nothing to do with whether the
render is correct, so `_comparable` compares the *stated* level (`settings.effort`,
the dict a role was asked for) instead -- exactly reproduced regardless of which
program answers, which is the property rendering an explicit `--effort` flag
is for. Every other field compares the resolved, per-role answer
(`model_for`, `window_for`, and -- HTTP only, since a command backend's
per-role endpoints are dead configuration by the same docstring's own words --
`base_url_for`, `api_key_env_for`).

Offline throughout: `config.resolve` makes no request, and neither does
anything below it on this path (`Settings.__post_init__`'s checks are all
local). No cassette, no socket.

Run with `python3 tests/test_web_cli_render.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import shlex
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless import cli, config, merge  # noqa: E402
from llossless.web import cli_render  # noqa: E402
from llossless.web.jobs import MergeRequest  # noqa: E402

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


SOURCE_A = "# Draft A\n\nFirst paragraph.\n"
SOURCE_B = "# Draft B\n\nSecond paragraph.\n"


# --------------------------------------------------------------------------
# the round trip
# --------------------------------------------------------------------------


def _comparable(settings: config.Settings) -> dict:
    """The projection two `Settings` are compared on. See the module docstring
    for why this is not every field.

    `effort` drops a role whose model is single-level (the ruling that keeps Haiku's default effort) for
    the same reason the module docstring already gives for comparing the
    *stated* level rather than the resolved one: `cli_render.render` will not
    put `--effort` on the placeholder for such a role even where
    `settings.effort` names one (it must not -- rendering it is exactly the
    behaviour the ruling stops), so the round trip loses that entry by
    design and the comparison has to drop it on both sides to mean anything.
    """
    per_role = {
        role: {
            "model": settings.model_for(role),
            "window": settings.window_for(role),
        }
        for role in cli.ROLES
    }
    if not settings.command:
        for role in cli.ROLES:
            per_role[role]["base_url"] = settings.base_url_for(role)
            per_role[role]["api_key_env"] = settings.api_key_env_for(role)
    effort = {role: level for role, level in settings.effort.items()
             if not config.is_single_level_model(settings.model_for(role))}
    return {
        "roles": per_role,
        "fidelity": settings.fidelity,
        "verify_depth": settings.verify_depth,
        "title_policy": settings.title_policy,
        "declared_loss_budget": settings.declared_loss_budget,
        "field_order": settings.field_order,
        "pinned": settings.pinned,
        "structured": settings.structured if settings.pinned else None,
        "profile": settings.profile,
        "min_interval": settings.min_interval,
        "timeout": settings.timeout,
        "stream": settings.stream,
        "max_tokens": settings.max_tokens,
        "thinking": sorted(settings.thinking),
        "effort": effort,
        "is_command": bool(settings.command),
        "command_envelope": settings.command_envelope if settings.command else None,
    }


def _parse_env(lines: list[str]) -> dict[str, str]:
    env: dict[str, str] = {}
    for line in lines:
        check(line.startswith("export "), f"an env line is not an export: {line!r}")
        body = line[len("export "):]
        tokens = shlex.split(body)
        check(len(tokens) == 1, f"an env line is not one shell word: {line!r}")
        name, sep, value = tokens[0].partition("=")
        check(sep == "=", f"an env line does not assign: {line!r}")
        env[name] = value
    return env


def _round_trip(settings: config.Settings, request: MergeRequest, run=None):
    """`render()`'s output, parsed back through the CLI's own parser and resolver.

    Returns `(rendered, settings_b)`. Raises exactly as a real invocation
    would if the rendered command line does not parse -- the caller decides
    whether that is expected.
    """
    rendered = cli_render.render(settings, request, run)
    argv = shlex.split(rendered["command"])
    check(argv[0] == "llossless", f"the command does not start with llossless: {argv}")
    args = cli.build_parser().parse_args(argv[1:])
    env = _parse_env(rendered["env"])
    settings_b = config.resolve(args, environ=env)
    return rendered, settings_b


def _assert_round_trips(settings: config.Settings, request: MergeRequest, run=None,
                        label: str = "") -> dict:
    rendered, settings_b = _round_trip(settings, request, run)
    mine, theirs = _comparable(settings), _comparable(settings_b)
    check(mine == theirs,
          f"{label}: rendered command does not round-trip to the same settings\n"
          f"  command: {rendered['command']}\n"
          f"  env: {rendered['env']}\n"
          f"  original:   {mine}\n"
          f"  round-trip: {theirs}")
    return rendered


def _request(labels=("Draft A", "Draft B"), base=None) -> MergeRequest:
    sources = (SOURCE_A, SOURCE_B)
    documents = {label: sources[i % len(sources)] for i, label in enumerate(labels)}
    return MergeRequest(documents=documents, base=base)


# --------------------------------------------------------------------------
# HTTP endpoint, one address
# --------------------------------------------------------------------------


def test_http_default_policy_round_trips() -> None:
    settings = config.Settings(
        base_url="https://api.example.test/v1",
        models={"merge": "gpt-5.6-terra", "verify": "gpt-5.6-terra"},
    )
    request = _request(base="Draft A")
    rendered = _assert_round_trips(settings, request, label="http default policy")
    check("--base-url" in rendered["command"], "a non-default address needs --base-url")
    check(any("LLOSSLESS_API_KEY" in line for line in rendered["env"]),
          "the default key variable should still be exported")
    check(all(config.DEFAULT_KEY_ENV not in line or "<your key>" in line
              for line in rendered["env"] if "=" in line),
          "the key line must carry the placeholder, never a value")


def test_http_non_default_policy_round_trips() -> None:
    settings = config.Settings(
        base_url="http://localhost:11434/v1",
        models={"merge": "qwen3:8b", "verify": "qwen3:8b"},
        fidelity="mid",
        verify_depth=config.COVERAGE_DEPTH,
        title_policy="keep-base",
        declared_loss_budget=0.1,
        field_order="any",
        structured="json_schema",
        pinned=True,
        profile="anthropic",
        thinking=frozenset({"merge"}),
        min_interval=5.0,
        timeout=300.0,
        stream=False,
        max_tokens=4096,
    )
    request = _request(base="Draft B")
    rendered = _assert_round_trips(settings, request, label="http non-default policy")
    for flag in ("--fidelity", "--verify-depth", "--title-policy", "--loss-budget",
                 "--field-order", "--structured", "--profile", "--thinking",
                 "--min-interval", "--timeout"):
        check(flag in rendered["command"], f"{flag} missing from {rendered['command']!r}")
    check(any("LLOSSLESS_STREAM" in line for line in rendered["env"]),
          "stream=False must be recorded, and there is no flag for it")
    check(any("LLOSSLESS_MAX_TOKENS" in line for line in rendered["env"]),
          "an explicit max_tokens must be recorded, and there is no flag for it")


def test_http_split_endpoints_round_trip() -> None:
    settings = config.Settings(
        base_url="http://localhost:11434/v1",
        models={"merge": "gpt-5.6-terra", "verify": "qwen3:8b", "decompose": "qwen3:8b"},
        endpoints={"merge": "https://api.example.test/v1"},
        api_key_envs={"merge": "EXAMPLE_API_KEY"},
        windows={"merge": 200000, "verify": 32768, "decompose": 32768},
    )
    request = _request(base="Draft A")
    rendered = _assert_round_trips(settings, request, label="http split endpoints")
    check(any("LLOSSLESS_BASE_URL_MERGE" in line for line in rendered["env"]),
          "a split endpoint needs the per-role address variable")
    check(any("LLOSSLESS_API_KEY_ENV_MERGE" in line for line in rendered["env"]),
          "a split endpoint needs the per-role key-variable indirection")
    check(any("LLOSSLESS_WINDOW_MERGE" in line for line in rendered["env"]),
          "a split window needs the per-role window variable")
    check("--window" not in rendered["command"],
          "a non-uniform window must not also render the run-wide flag")


# --------------------------------------------------------------------------
# a command (subscription) route
# --------------------------------------------------------------------------


SECRET_COMMAND = "/srv/operator-private/claude-wrapper.sh --account totally-secret-42"


def _command_route_settings() -> config.Settings:
    return config.Settings(
        command=SECRET_COMMAND,
        command_label="Opus 5 - Subscription",
        command_envelope=config.ENVELOPE_RESULT,
        models={"merge": "claude-opus-5", "verify": "claude-opus-5"},
        window=200000,
        profile="subscription",
        thinking=frozenset(cli.ROLES),
        effort={"merge": "high"},
        fidelity="open",
    )


def test_command_route_round_trips_and_never_names_its_program() -> None:
    settings = _command_route_settings()
    request = _request(base="Draft A")
    rendered = _assert_round_trips(settings, request, label="command route")
    check("--answer-with" in rendered["command"], "a command route needs --answer-with")
    check(cli_render.PLACEHOLDER_COMMAND in rendered["command"],
          "a command route's program must be the placeholder")
    check("--effort merge=high" in rendered["command"] or "merge=high" in rendered["command"],
          "the requested effort level must still be rendered")
    check(any("LLOSSLESS_COMMAND_ENVELOPE" in line for line in rendered["env"]),
          "a non-raw envelope must be recorded so the user's own program can match it")
    blob = json.dumps(rendered)
    check(SECRET_COMMAND not in blob, "the real command leaked into the payload")
    check("totally-secret-42" not in blob, "a fragment of the real command leaked")
    check(any(note.get("key") == "command_route"
              and note.get("label") == "Opus 5 - Subscription"
              for note in rendered["notes"]),
          f"the route's own label should be named, since it is already "
          f"public: {rendered['notes']}")


def _haiku_command_route_settings() -> config.Settings:
    return config.Settings(
        command=SECRET_COMMAND,
        command_label="Haiku - Subscription",
        command_envelope=config.ENVELOPE_RESULT,
        models={"merge": "haiku", "verify": "haiku"},
        window=200000,
        profile="subscription",
        thinking=frozenset(cli.ROLES),
        # A stray choice this model cannot carry -- unreachable through the
        # page, which hides the effort control for a single-level route, or
        # through the API, which refuses a submitted level
        # (`jobs.route_plan`) -- held here so the renderer is proven never to
        # let it reach the placeholder even if something upstream slipped.
        effort={"merge": "medium"},
        fidelity="open",
    )


def test_haiku_command_route_renders_no_effort_and_still_round_trips() -> None:
    """Haiku has one level (extended thinking on or off), not
    a graded scale, so the "run this from the command line" block must never
    show `--effort` for it -- not even where `settings.effort` names one.
    """
    settings = _haiku_command_route_settings()
    request = _request(base="Draft A")
    rendered = _assert_round_trips(settings, request, label="haiku command route")
    check("--effort" not in rendered["command"],
          f"a single-level model must render no --effort at all: "
          f"{rendered['command']}")


def test_the_command_route_note_carries_a_plain_example() -> None:
    """The operator's ruling on 2026-09-28: keep the placeholder, and have the command-route
    note offer the plain form `claude -p --output-format json` as an example
    of what a reader may put in its place.

    Must-fire: a command route's own note carries that example.
    Must-not-fire: an HTTP route renders no such note at all, and the real
    configured program never appears anywhere in the payload, example
    included.
    """
    settings = _command_route_settings()
    request = _request(base="Draft A")
    rendered = cli_render.render(settings, request)
    command_notes = [note for note in rendered["notes"] if note.get("key") == "command_route"]
    check(len(command_notes) == 1, f"expected one command_route note: {rendered['notes']}")
    check(command_notes and command_notes[0].get("example") == cli_render.COMMAND_EXAMPLE,
          f"the command_route note does not carry the example: {command_notes}")
    check(cli_render.COMMAND_EXAMPLE == "claude -p --output-format json",
          "the example drifted from the ruling's exact plain form")

    blob = json.dumps(rendered)
    check(SECRET_COMMAND not in blob, "the real configured command leaked into the payload")
    check("totally-secret-42" not in blob, "a fragment of the real command leaked")

    # Must-not-fire: an HTTP route has no command_route note and no example.
    http_settings = config.Settings(
        base_url="http://localhost:11434/v1",
        models={"merge": "qwen3:8b", "verify": "qwen3:8b"},
    )
    http_rendered = cli_render.render(http_settings, request)
    check(not any(note.get("key") == "command_route" for note in http_rendered["notes"]),
          f"an HTTP route must carry no command_route note: {http_rendered['notes']}")
    check(not any("example" in note for note in http_rendered["notes"]),
          f"an HTTP route must carry no example note either: {http_rendered['notes']}")
    check(cli_render.COMMAND_EXAMPLE not in json.dumps(http_rendered),
          "the command example must not appear on an HTTP route's payload")


def test_no_stored_key_or_suffix_ever_appears() -> None:
    """The must-not-fire case the brief names: a key-shaped credential, absent.

    A real-looking key is put where the resolved settings would have to reach
    it from -- an environment the request's key came from -- and the rendered
    payload is scanned for it and for every suffix down to four characters,
    which is the shape a "last four characters" leak would take.
    """
    secret = "sk-ant-api03-REALSECRETVALUEDONOTLEAK00000000000000"
    settings = config.Settings(
        base_url="https://api.anthropic.com/v1",
        models={"merge": "claude-opus-5", "verify": "claude-opus-5"},
        api_key_env="ANTHROPIC_API_KEY",
    )
    request = _request(base="Draft A")
    rendered = cli_render.render(settings, request)
    blob = json.dumps(rendered)
    check(secret not in blob, "the literal key appeared in the rendered payload")
    for length in (4, 6, 8, 12, len(secret)):
        suffix = secret[-length:]
        check(suffix not in blob,
              f"a {length}-character suffix of the key appeared: {suffix!r}")
    check("<your key>" in blob, "the placeholder must still be present")


# --------------------------------------------------------------------------
# every fidelity level and every verify depth
# --------------------------------------------------------------------------


def test_every_fidelity_level_and_depth_round_trips() -> None:
    """Every level but `sourced`, which an HTTP endpoint refuses outright
    (`config.retrieval_refusal`) and which `resolved_environ` already turns
    into a `JobRefused` before a web job ever reaches `web_settings` -- so a
    plain HTTP `Settings` at `sourced` is not a run this renderer is ever
    handed. `sourced` over a command route has its own test below, and its
    own, different, limit.
    """
    for level in config.FIDELITY_LEVELS:
        if config.canonical_fidelity(level) == config.SOURCED:
            continue
        for depth in config.VERIFY_DEPTHS:
            try:
                settings = config.Settings(
                    base_url="http://localhost:11434/v1",
                    models={"merge": "qwen3:8b", "verify": "qwen3:8b"},
                    fidelity=level, verify_depth=depth,
                )
            except config.ConfigError as exc:
                check(False, f"could not build Settings for {level}/{depth}: {exc}")
                continue
            request = _request(base="Draft A")
            rendered = _assert_round_trips(settings, request,
                                           label=f"fidelity={level} depth={depth}")
            command = rendered["command"]
            check(f"--fidelity {config.fidelity_name(level)}" in command,
                  f"{level} did not render its published name in {command!r}")
            check(f"--verify-depth {depth}" in command,
                  f"{depth} missing from {command!r}")


def test_sourced_fidelity_via_command_route_notes_its_own_limit() -> None:
    """`sourced` over a command route is real and does not round-trip.

    A `sourced` run needs a backend that can retrieve, granted automatically
    for a program this build recognises by basename (`config.AUTO_GRANT`,
    keyed on `claude`). The rendered command cannot name that program (the
    module docstring's whole rule), so the placeholder it names instead is,
    correctly, not one -- `config.resolve` refuses `--fidelity sourced`
    against it. That is not a bug in the render: it is the true fact that
    nobody but the operator's own machine can reproduce this particular run,
    and the note says so instead of a command that looks runnable and is not.
    """
    settings = config.Settings(
        command="claude --model opus", command_label="Opus 5 - Subscription",
        window=200000, profile="subscription", thinking=frozenset(cli.ROLES),
        models={"merge": "claude-opus-5", "verify": "claude-opus-5"},
        fidelity="sourced",
    )
    request = _request(base="Draft A")
    rendered = cli_render.render(settings, request)
    check("--fidelity sourced" in rendered["command"], "the level itself must still be named")
    argv = shlex.split(rendered["command"])
    args = cli.build_parser().parse_args(argv[1:])
    env = _parse_env(rendered["env"])
    raised = False
    try:
        config.resolve(args, environ=env)
    except config.ConfigError:
        raised = True
    check(raised,
          "a placeholder --answer-with cannot retrieve, so --fidelity sourced "
          "must still refuse against it -- if this stops raising, the "
          "placeholder is leaking real retrieval capability from somewhere")


# --------------------------------------------------------------------------
# documents and the base
# --------------------------------------------------------------------------


def test_documents_get_unique_file_safe_names() -> None:
    # Two different labels -- dict keys, so they cannot literally collide --
    # that sanitise to the same stem, "Draft-A.md", the way "Draft/A" and
    # "Draft:A" both would: a path separator and a colon are equally not
    # `[A-Za-z0-9._-]`, and both become one dash.
    request = _request(labels=("Draft/A", "Draft:A"))
    settings = config.Settings(models={"merge": "qwen3:8b", "verify": "qwen3:8b"})
    rendered = cli_render.render(settings, request)
    names = [doc["filename"] for doc in rendered["documents"]]
    check(len(names) == 2 and len(names) == len(set(names)), f"filenames collided: {names}")
    check(names[0] == "Draft-A.md" and names[1] == "Draft-A-2.md",
          f"a repeated sanitised stem should be suffixed -2, not renamed: {names}")


def test_defaulted_base_is_named_explicitly_and_noted() -> None:
    settings = config.Settings(models={"merge": "qwen3:8b", "verify": "qwen3:8b"})
    request = _request(base=None)
    rendered = cli_render.render(settings, request)
    check("--base" in rendered["command"], "the CLI requires --base even when none was chosen")
    check(any(note.get("key") == "base_defaulted" for note in rendered["notes"]),
          f"an implicit base must be noted, not silently assumed: {rendered['notes']}")
    # And once the run exists, the note follows what the merge really used --
    # here, the second document, so the render must track it rather than
    # keep guessing "the first one".
    run = types.SimpleNamespace(
        base="source_b.md",
        paths={"source_a.md": "Draft A", "source_b.md": "Draft B"},
        base_chosen=merge.DEFAULTED,
    )
    rendered_final = cli_render.render(settings, request, run)
    base_index = rendered_final["command"].split().index("--base") + 1
    base_file = rendered_final["command"].split()[base_index]
    expected = next(doc["filename"] for doc in rendered_final["documents"]
                    if doc["label"] == "Draft B")
    check(base_file == expected,
          f"the finished run's base ({expected}) was not what got rendered ({base_file})")


# --------------------------------------------------------------------------
# the seed: drop one flag, and the round trip must catch it
# --------------------------------------------------------------------------


def test_a_dropped_flag_is_caught_by_the_comparison() -> None:
    settings = config.Settings(
        base_url="http://localhost:11434/v1",
        models={"merge": "qwen3:8b", "verify": "qwen3:8b"},
        fidelity="mid", declared_loss_budget=0.2,
    )
    request = _request(base="Draft A")
    rendered = cli_render.render(settings, request)
    argv = shlex.split(rendered["command"])
    # Remove "--loss-budget" and its value -- a real regression this test
    # exists to catch (a flag quietly dropped from the renderer).
    index = argv.index("--loss-budget")
    del argv[index:index + 2]
    args = cli.build_parser().parse_args(argv[1:])
    env = _parse_env(rendered["env"])
    settings_b = config.resolve(args, environ=env)
    mine, theirs = _comparable(settings), _comparable(settings_b)
    check(mine != theirs,
          "dropping --loss-budget from the rendered command must change the "
          "round-tripped settings, or this comparison cannot catch a real "
          "regression")
    check(mine["declared_loss_budget"] == 0.2 and theirs["declared_loss_budget"] != 0.2,
          f"the dropped field specifically must differ: {mine} vs {theirs}")


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_cli_render" and callable(function):
            function()
    if failures:
        print(f"web cli_render: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web cli_render: {checks} checks pass")
    return 0


def test_web_cli_render() -> None:
    """pytest entry point."""
    assert main() == 0, "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
