#!/usr/bin/env python3
"""The lineup runner and its figures, each rule with a must-fire and a must-not-fire case. Fakes only.

`tests/run_lineup.py` runs the fair-lineup benchmark from a
pinned clone, and `tests/lineup_figures.py` forms its figures. Every check here
runs the real `python -m llossless` from a throwaway git clone of this tree's
code against `tests/lineup_fakes.py`: a fake model behind a loopback
`FakeEndpoint`, and a fake `claude` behind the runner's own wrapper. No model,
vendor, subscription or serverless call.

- the pin and the clean tree: a clone off the pin, or with an untracked or an
  ignored file, is refused; the runner refuses to run from anywhere but the
  clone; a report stamped with another commit is refused;
- the registration: an unpriced model with no reason, a metered row with no
  cap, a subset row in the headline, and a placeholder are refused;
- the environment: a `CLAUDE*` name that reaches `claude` stops the lane, and
  with the scrub in place none does;
- the label: a model that answers as another model (HTTP `served_model`, the
  CLI's `answered_by`) is refused; a dated id is not;
- classification: a platform failure is excluded and re-queued, then counted
  when the retry answers; a model's own exit 2 is a final result and is not
  retried; a blank on `length` is `unruled`; the classifier on each message
  shape;
- resume: a stopped lane skips its finished cells and re-runs an attempt a dead
  process left;
- the spend cap: a lane whose next cell could exceed a cap stops before it; a
  5xx discard is charged nothing and an unreported answer one estimate;
- pre-warm: one untimed request and an event, never a cell or a ledger row;
- the thinking pilot flags a call over 60% of its ceiling;
- `lineup_figures`: `--check` against a real run, clean and then tampered;
- the second bug hunt: `model_failure` only on positive evidence (a lost
  login halts, the CLI's blank and a 400 are not the model's); a refusal on
  either route is `refused`, final and charged once, and `rules.refusal_counts`
  decides where the row goes; a row's own exit 2 or window never shrinks
  another row's pairs (the committed 2026-09-25 cells: Luna does not go from
  disqualified to first), for S2's fixtures too; the platform rule; the lowest
  counted draw; shared ranks across price units; the floors; spend limits and
  the subscription's reset; the GPU-seconds cap; a torn journal; a completed
  run with an unruled call; a row that completed nothing; the pod's address
  in no evidence file.

Run with `python3 tests/test_run_lineup.py`, or collect with pytest.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import contextlib  # noqa: E402
import copy  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

import figure_rules  # noqa: E402
import lineup_fakes  # noqa: E402
import lineup_figures  # noqa: E402
import run_detect  # noqa: E402
import run_lineup  # noqa: E402
from fake_endpoint import FakeEndpoint  # noqa: E402

failures: list[str] = []
KEY = "LINEUP_TEST_KEY"
os.environ[KEY] = "fake-key-not-a-secret"


def check(ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


# --- a throwaway clone, a registration, a context ------------------------------------

_CLONE: dict = {}


def make_clone(where: Path) -> tuple[Path, str]:
    """This tree's code and test data, committed in a git repository of its own."""
    where.mkdir(parents=True)
    for name in ("src", "prompts"):
        shutil.copytree(ROOT / name, where / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy(ROOT / "pyproject.toml", where / "pyproject.toml")
    (where / "tests").mkdir()
    for path in (ROOT / "tests").glob("*.py"):
        shutil.copy(path, where / "tests" / path.name)
    for name in ("pairs", "fixtures", "handwritten"):
        shutil.copytree(ROOT / "tests" / name, where / "tests" / name)
    (where / ".gitignore").write_text("__pycache__/\n*.pyc\nmodels.local.json\n")

    def git(*args):
        return subprocess.run(["git", "-C", str(where), *args], check=True,
                              capture_output=True, text=True).stdout
    git("init", "-q")
    # No background gc or maintenance: it would write into .git while a test's
    # temporary directory is being removed.
    git("config", "gc.auto", "0")
    git("config", "maintenance.auto", "false")
    git("add", "-A")
    git("-c", "user.name=lineup", "-c", "user.email=lineup@example.invalid", "commit",
        "-qm", "pin")
    return where, git("rev-parse", "HEAD").strip()


def shared_clone() -> tuple[Path, str]:
    """One clone for the checks that leave it clean. Made once per process."""
    if "path" not in _CLONE:
        base = Path(tempfile.mkdtemp(prefix="lineup-clone-"))
        _CLONE["base"] = base
        _CLONE["path"], _CLONE["pin"] = make_clone(base / "tree")
    return _CLONE["path"], _CLONE["pin"]


def small_registration(pin: str, clone: Path, *, rows: list[dict], items=("badge_access",),
                       draws=None, caps=None, lanes=None, claude=None, retry=None,
                       reference_url: str = "http://reference.invalid/v1",
                       infrastructure=None) -> dict:
    reg = run_lineup.template(pin=pin, clone=str(clone))
    # Two reference routes on the fake (never asked unless a cell fails
    # every retry pass), and probes the tests stub (`ctx.probe`).
    reg["references"] = [
        {"id": "ref-openai", "model": "gpt-6-luna", "vendor": "openai", "hosting": "vendor",
         "route": {"kind": "http", "base_url": reference_url, "key_env": KEY,
                   "profile": "openai-reasoning"},
         "effort": "vendor_default", "thinking": list(run_lineup.ROLES), "window": 200000,
         "field_order": "schema", "cell_estimate_usd": 0.05},
        {"id": "ref-anthropic", "model": "claude-haiku-4-5-20251001", "vendor": "anthropic",
         "hosting": "vendor",
         "route": {"kind": "http", "base_url": reference_url, "key_env": KEY,
                   "profile": "anthropic"},
         "effort": "vendor_default", "thinking": list(run_lineup.ROLES), "window": 200000,
         "field_order": "schema", "cell_estimate_usd": 0.05}]
    reg["infrastructure"] = infrastructure or {"probe_urls": [reference_url + "/models"],
                                               "probe_intervals_seconds": [120, 300],
                                               "max_pause_seconds": 3600}
    reg["sets"] = {"S1": {"kind": "merge", "score": "pairs", "root": "tests/pairs",
                          "fidelity": "high", "items": list(items),
                          "draws": draws or {"default": 1}}}
    reg["rows"] = rows
    reg["caps"] = caps if caps is not None else {"anthropic": 50.0, "openai": 50.0,
                                                  "overall": 100.0}
    reg["lanes"] = lanes or {"api": {}, "subscription": {}, "serverless": {}}
    reg["retry"] = retry or {"passes": 1, "spacing_seconds": 0, "breaker": 5}
    reg.pop("claude", None)
    reg.pop("env_file", None)
    if claude:
        reg["claude"] = claude
    return reg


def http_row(rid: str, model: str, url: str, vendor: str = "anthropic", **extra) -> dict:
    profile = {"anthropic": "anthropic", "openai": "openai-reasoning"}.get(
        vendor, "openai-compatible")
    row = {"id": rid, "model": model, "lane": "api", "vendor": vendor, "hosting": "vendor",
           "route": {"kind": "http", "base_url": url, "key_env": KEY, "profile": profile},
           "effort": "vendor_default", "thinking": list(run_lineup.ROLES), "window": 200000,
           "field_order": "schema", "sets": ["S1"], "cell_estimate_usd": 0.5,
           "reference": "ref-anthropic" if vendor == "openai" else "ref-openai"}
    row.update(extra)
    return row


def claude_row(rid: str, model: str, **extra) -> dict:
    one_level = run_lineup.SINGLE_LEVEL_MODELS.match(model) is not None
    row = {"id": rid, "model": model, "lane": "subscription", "vendor": "subscription",
           "hosting": "vendor", "metered": False,
           "route": {"kind": "claude", "profile": "subscription"},
           # By ruling, Haiku registers its one level and gets no --effort.
           "effort": run_lineup.SINGLE_LEVEL if one_level
           else {role: "medium" for role in run_lineup.ROLES},
           "thinking": list(run_lineup.ROLES), "window": 200000, "field_order": "schema",
           "sets": ["S1"], "reference": "ref-openai"}
    row.update(extra)
    return row


def write_run(reg: dict, run_dir: Path) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "REGISTRATION.md"
    path.write_text(run_lineup.render_registration(reg), encoding="utf-8")
    return path


def context(path: Path) -> run_lineup.Context:
    ctx = run_lineup.load_context(path, require_self=False)
    ctx.out = lambda *_a, **_k: None
    ctx.sleep = lambda _s: None
    problems = run_lineup.preflight(ctx, None)
    if problems:
        raise AssertionError(f"preflight: {problems}")
    ctx.run_info = {**run_lineup.first_start(ctx), **ctx.run_info}
    if "claude" in ctx.reg:
        run_lineup.write_wrapper(ctx.run_dir, run_lineup.claude_binary(ctx))
    return ctx


def fake_claude(run_dir: Path, behaviour: dict) -> dict:
    program = lineup_fakes.write_fake_claude(run_dir / "fakes", behaviour,
                                             run_dir / "fakes" / "state.json")
    return {"path": str(program), "sha256": run_lineup.sha256_file(program),
            "version": "2.1.283"}


@contextlib.contextmanager
def endpoint(behaviour: dict, state: Path):
    fake = FakeEndpoint(lineup_fakes.responder(behaviour, state), prompt_ratio=None)
    with fake as url:
        yield fake, url


def states(ctx: run_lineup.Context) -> dict[str, list[str]]:
    """Each counted cell's attempts' states. A reference check is not a cell."""
    return {cell: [a["state"] for a in attempts]
            for cell, attempts in run_lineup.ends(ctx.journal.read()).items()
            if "~reference|" not in cell}


# --- the markers the fake reads prompts by ---------------------------------------------

def test_the_fake_still_recognises_every_prompt() -> None:
    """The fake model keys on each prompt's first sentence; a reworded prompt must fail here."""
    check(lineup_fakes.check_markers() == [],
          f"a prompt no longer carries its marker: {lineup_fakes.check_markers()}")


# --- 1. the pin and the clean tree ------------------------------------------------------

def test_the_pin_and_a_clean_tree_are_required() -> None:
    """MUST FIRE: HEAD off the pin; an untracked file; an ignored file (a stray
    models.local.json); internal/assets. MUST NOT FIRE: the clone as committed."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        clone, pin = make_clone(Path(tmp) / "tree")
        check(run_lineup.check_clone(clone, pin) == [],
              f"MUST NOT FIRE: a fresh clone at its pin: {run_lineup.check_clone(clone, pin)}")
        other = "0" * 40
        check(any("not the pin" in p for p in run_lineup.check_clone(clone, other)),
              "a clone whose HEAD is not the pin must be refused")
        (clone / "notes.txt").write_text("x")
        check(any("not clean" in p for p in run_lineup.check_clone(clone, pin)),
              "an untracked file must be refused")
        (clone / "notes.txt").unlink()
        (clone / "models.local.json").write_text("{}")
        check(any("not clean" in p for p in run_lineup.check_clone(clone, pin)),
              "an ignored file (models.local.json) must be refused: it changes the models")
        (clone / "models.local.json").unlink()
        (clone / "internal" / "assets").mkdir(parents=True)
        check(any("internal/assets" in p for p in run_lineup.check_clone(clone, pin)),
              "internal/assets in the clone must be refused")


def test_the_runner_runs_only_from_the_clone_and_refuses_a_dirty_start() -> None:
    """MUST FIRE: this tree's runner pointed at another clone; `check` on a dirty
    clone exits 2. MUST NOT FIRE: the clone's own runner, clean, passes `check`."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        clone, pin = make_clone(Path(tmp) / "tree")
        reg = small_registration(pin, clone, rows=[http_row("a", "claude-opus-5-5",
                                                            "http://127.0.0.1:9/v1")])
        path = write_run(reg, Path(tmp))
        try:
            run_lineup.load_context(path)
            failures.append("this tree's runner must refuse a registration whose clone "
                            "is elsewhere")
        except run_lineup.Refusal as exc:
            check("pinned clone's own copy" in exc.message, f"wrong refusal: {exc.message}")
        runner = [sys.executable, str(clone / "tests" / "run_lineup.py"), "check",
                  "--registration", str(path)]
        done = subprocess.run(runner, capture_output=True, text=True)
        check(done.returncode == 0, f"MUST NOT FIRE: `check` from the clone's own runner: "
                                    f"{done.returncode} {done.stderr[-400:]}")
        (clone / "src" / "llossless" / "stray.py").write_text("x = 1\n")
        done = subprocess.run(runner, capture_output=True, text=True)
        check(done.returncode == run_lineup.EXIT_PREFLIGHT and "not clean" in done.stderr,
              f"a dirty clone must be refused before any cell: {done.returncode} "
              f"{done.stderr[-400:]}")


def test_a_report_stamped_with_another_commit_is_refused() -> None:
    """MUST FIRE: a `-dirty` stamp, another commit, a moved tree. MUST NOT FIRE: the pin."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        reg = small_registration(pin, clone, rows=[http_row("a", "claude-opus-5-5",
                                                            "http://127.0.0.1:9/v1")])
        ctx = context(write_run(reg, Path(tmp)))
        cell = run_lineup.Cell("a", "S1", "badge_access", 1)
        row = ctx.row("a")
        good = {"exit_code": 0, "provenance": {"claimcheck_commit": pin[:12]}}
        hits = lambda rep: [p for p in run_lineup.check_report(ctx, row, cell, rep)  # noqa: E731
                            if "commit" in p or "moved" in p]
        check(hits(good) == [], f"MUST NOT FIRE: the pin's own stamp: {hits(good)}")
        for stamp in (pin[:12] + "-dirty", "0123456789ab"):
            bad = copy.deepcopy(good)
            bad["provenance"]["claimcheck_commit"] = stamp
            check(hits(bad), f"a report stamped {stamp!r} must be refused")
        moved = copy.deepcopy(good)
        moved["provenance"]["claimcheck_commit_changed"] = True
        check(hits(moved), "a report whose tree moved mid-run must be refused")


# --- 2. the registration ----------------------------------------------------------------

def test_the_registration_is_refused_unless_every_row_is_priced_or_says_why() -> None:
    """MUST FIRE: an unpriced model with no reason; a metered row with no cap; a
    subset row in the headline; a placeholder; HTTP effort. MUST NOT FIRE: each
    fixed."""
    clone, pin = shared_clone()
    ok = small_registration(pin, clone, rows=[http_row("a", "claude-opus-5-5", "http://x/v1")])
    check(run_lineup.validate(ok) == [], f"MUST NOT FIRE: {run_lineup.validate(ok)}")
    bad = copy.deepcopy(ok)
    bad["rows"].append(http_row("b", "no-such-model", "http://x/v1", metered=False))
    check(any("no SKU" in p for p in run_lineup.validate(bad)),
          "an unpriced model with no `unpriced` reason must be refused")
    bad["rows"][-1]["unpriced"] = "self-hosted"
    check(not any("no SKU" in p for p in run_lineup.validate(bad)),
          "MUST NOT FIRE: an unpriced model with its reason")
    capless = copy.deepcopy(ok)
    capless["caps"].pop("anthropic")
    check(any("caps names no such vendor" in p for p in run_lineup.validate(capless)),
          "a metered row whose vendor has no cap must be refused")
    subset = copy.deepcopy(ok)
    subset["rows"][0]["items"] = {"S1": ["badge_access"]}
    check(any("headline" in p for p in run_lineup.validate(subset)),
          "a row on a subset of the items must not be in the headline")
    filled = copy.deepcopy(ok)
    filled["pin"] = "<FILL: the pin>"
    check(any("placeholder" in p for p in run_lineup.validate(filled)),
          "an unfilled placeholder must be refused")
    effort = copy.deepcopy(ok)
    effort["rows"][0]["effort"] = {r: "high" for r in run_lineup.ROLES}
    check(any("cannot carry a level" in p for p in run_lineup.validate(effort)),
          "an HTTP row naming an effort level must be refused")
    sub = copy.deepcopy(ok)
    sub["rows"].append(claude_row("s", "claude-opus-5-5"))
    sub["rows"][-1]["effort"] = {"merge": "medium"}
    sub["claude"] = {"path": "x", "sha256": "y", "version": "z"}
    check(any("never the build's default" in p for p in run_lineup.validate(sub)),
          "a command route must state an effort for every role")


# --- 3. the environment --------------------------------------------------------------

def test_a_forbidden_name_that_reaches_claude_stops_the_lane() -> None:
    """MUST FIRE: with the runner's scrub narrowed to drop nothing, a `CLAUDE_*`
    name the tool's own filter keeps (`CLAUDE_CONFIG_DIR`) reaches the fake CLI
    and the cell is refused. MUST NOT FIRE: with the scrub in place, the same
    parent environment reaches `claude` with none of the forbidden names."""
    clone, pin = shared_clone()
    seeded = {"CLAUDE_CONFIG_DIR": "/nowhere", "ANTHROPIC_API_KEY": "sk-sentinel",
              "CLAUDE_CODE_EFFORT_LEVEL": "max", "LLOSSLESS_EFFORT": "low"}
    saved = {k: os.environ.get(k) for k in seeded}
    os.environ.update(seeded)
    try:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            run_dir = Path(tmp)
            reg = small_registration(pin, clone, rows=[claude_row("s", "claude-opus-5-5")],
                                     claude=fake_claude(run_dir, {}))
            ctx = context(write_run(reg, run_dir))
            cell = run_lineup.Cell("s", "S1", "badge_access", 1)
            end = run_lineup.run_cell(ctx, cell, 1, "subscription")
            check(end["state"] == "ok", f"MUST NOT FIRE: the scrubbed cell: {end['state']} "
                                        f"{end['reasons']}")
            calls = run_lineup.read_calls(run_dir / end["dir"] / "calls")
            seen = {n for c in calls for n in c["env_names"]}
            check(calls and not {n for n in seen if run_lineup.FORBIDDEN_AT_CHILD.match(n)},
                  f"MUST NOT FIRE: forbidden names reached claude: "
                  f"{sorted(n for n in seen if run_lineup.FORBIDDEN_AT_CHILD.match(n))}")
            check("DISABLE_AUTOUPDATER" in seen, "DISABLE_AUTOUPDATER must reach claude")
            # Seed 1: the scrub keeps everything. The runner's own check on the
            # child's environment refuses before anything starts.
            narrow = run_lineup.FORBIDDEN_ENV
            run_lineup.FORBIDDEN_ENV = __import__("re").compile(r"^(?!)")
            try:
                run_lineup.run_cell(ctx, cell, 2, "subscription")
                failures.append("a forbidden name in the child's environment must stop the "
                                "cell before it starts")
            except run_lineup.Refusal as exc:
                check("CLAUDE_CONFIG_DIR" in exc.message and "ANTHROPIC_API_KEY" in exc.message,
                      f"the pre-launch refusal must name what it found: {exc.message}")
            # Seed 2: the scrub keeps it and the runner also believes it set it.
            # The tool's own filter keeps CLAUDE_CONFIG_DIR, so it reaches the CLI,
            # and the wrapper's log is the last line of defence.
            real_set = run_lineup.RUNNER_SET
            run_lineup.RUNNER_SET = real_set | {"CLAUDE_CONFIG_DIR"}
            run_lineup.FORBIDDEN_ENV = __import__("re").compile(
                r"^(AI_AGENT|LLOSSLESS_|CLAIMCHECK_|ANTHROPIC|OPENAI|CLAUDE(?!_CONFIG_DIR))")
            try:
                end = run_lineup.run_cell(ctx, cell, 3, "subscription")
            finally:
                run_lineup.FORBIDDEN_ENV = narrow
                run_lineup.RUNNER_SET = real_set
            leaked = [r for r in end["reasons"] if "forbidden environment" in r]
            check(end["state"] == "halted" and leaked and "CLAUDE_CONFIG_DIR" in leaked[0],
                  f"a CLAUDE_* name reaching claude must refuse the cell: {end['state']} "
                  f"{end['reasons'][:3]}")
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def test_the_child_environment_carries_no_stray_tool_setting() -> None:
    """MUST FIRE: `cell_env` refuses when a forbidden name survives into the child
    (seeded by widening what the runner says it sets). MUST NOT FIRE: an operator's
    `LLOSSLESS_EFFORT` and API keys never reach the llossless process."""
    clone, pin = shared_clone()
    os.environ["LLOSSLESS_THINKING"] = "merge"
    os.environ["OPENAI_API_KEY"] = "sk-sentinel"
    try:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            reg = small_registration(pin, clone, rows=[http_row("a", "claude-opus-5-5",
                                                                "http://127.0.0.1:9/v1")])
            ctx = context(write_run(reg, Path(tmp)))
            env = run_lineup.cell_env(ctx, ctx.row("a"), Path(tmp) / "cell")
            check("LLOSSLESS_THINKING" not in env and "OPENAI_API_KEY" not in env,
                  f"MUST NOT FIRE: the operator's own variables reached the child: "
                  f"{sorted(k for k in env if k.startswith(('LLOSSLESS', 'OPENAI')))}")
            check(env.get("LLOSSLESS_API_KEY_ENV") == run_lineup.KEY_VAR
                  and env.get(run_lineup.KEY_VAR) == os.environ[KEY],
                  "the key must reach the child under the runner's own name only")
            real = run_lineup.scrubbed_env
            run_lineup.scrubbed_env = lambda source: dict(source)
            try:
                run_lineup.cell_env(ctx, ctx.row("a"), Path(tmp) / "cell")
                failures.append("a forbidden name in the child environment must be refused")
            except run_lineup.Refusal as exc:
                check("LLOSSLESS_THINKING" in exc.message, f"wrong refusal: {exc.message}")
            finally:
                run_lineup.scrubbed_env = real
    finally:
        os.environ.pop("LLOSSLESS_THINKING", None)
        os.environ.pop("OPENAI_API_KEY", None)


# --- 4. the label ----------------------------------------------------------------------

def test_a_model_that_answers_as_another_is_refused() -> None:
    """MUST FIRE: the HTTP endpoint serves another model; the CLI answers as another.
    MUST NOT FIRE: a dated id of the registered model."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        behaviour = {"gpt-6-luna": {"serve_as": "gpt-6-luna-2026-09-01"},
                     "gpt-6-sol": {"serve_as": "gpt-5.6-terra"},
                     "claude-sonnet-5": {"serve_as": "claude-haiku-4-5-20251001"}}
        with endpoint(behaviour, run_dir / "fakes" / "http.json") as (_fake, url):
            reg = small_registration(pin, clone, claude=fake_claude(run_dir, behaviour), rows=[
                http_row("luna", "gpt-6-luna", url, vendor="openai"),
                http_row("sol", "gpt-6-sol", url, vendor="openai"),
                claude_row("sonnet", "claude-sonnet-5")])
            ctx = context(write_run(reg, run_dir))
            luna = run_lineup.run_cell(ctx, run_lineup.Cell("luna", "S1", "badge_access", 1),
                                       1, "api")
            sol = run_lineup.run_cell(ctx, run_lineup.Cell("sol", "S1", "badge_access", 1),
                                      1, "api")
            sonnet = run_lineup.run_cell(
                ctx, run_lineup.Cell("sonnet", "S1", "badge_access", 1), 1, "subscription")
    check(luna["state"] == "ok", f"MUST NOT FIRE: a dated id is the model: {luna['reasons']}")
    check(sol["state"] == "halted" and any("model mismatch" in r for r in sol["reasons"]),
          f"an HTTP answer served as another model must halt the lane: {sol['reasons'][:2]}")
    check(sonnet["state"] == "halted" and any("model mismatch" in r for r in sonnet["reasons"]),
          f"a CLI answer from another model must halt the lane: {sonnet['reasons'][:2]}")


# --- 5. classification and the retry pass -----------------------------------------------

def test_platform_is_retried_model_failure_is_final_and_length_is_unruled() -> None:
    """MUST FIRE: three 503s on a merge -> `platform`, excluded, re-queued, and `ok`
    on the retry pass; a merge the model never answers usably -> `model_failure`,
    never retried; a verify blank on `length` -> `unruled`. MUST NOT FIRE: a clean
    cell is `ok` on its first attempt."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        behaviour = {"claude-opus-5-5": {"platform_on": {"Badge Access": 3}},
                     "claude-sonnet-5": {"fail_merge_on": ["Badge Access"]},
                     "claude-haiku-4-5-20251001": {"blank_length_on": ["Badge Access"]},
                     "gpt-6-luna": {}}
        with endpoint(behaviour, run_dir / "fakes" / "http.json") as (_fake, url):
            reg = small_registration(pin, clone, rows=[
                http_row("opus", "claude-opus-5-5", url),
                http_row("sonnet", "claude-sonnet-5", url),
                http_row("haiku", "claude-haiku-4-5-20251001", url),
                http_row("luna", "gpt-6-luna", url, vendor="openai")])
            ctx = context(write_run(reg, run_dir))
            code = run_lineup.LaneRun(ctx, "api").run()
            got = states(ctx)
            haiku = [r for r in ctx.journal.read() if r.get("type") == "end"
                     and r["row"] == "haiku"][-1]
            checks = [r for r in ctx.journal.read() if r.get("event") == "reference_check"]
    check(haiku.get("unruled_as") == "model_failure"
          and haiku.get("flag") == "model failure (unruled: blank after thinking (length))",
          f"a vendor row's unruled cell is a model failure, flagged: "
          f"{haiku.get('unruled_as')} {haiku.get('flag')}")
    check(not checks, f"MUST NOT FIRE: a cell that recovered on a retry pass asks no "
                      f"reference: {checks}")
    check(got.get("opus|S1|badge_access|d1") == ["platform", "ok"],
          f"a platform failure must be excluded, re-queued and then counted: "
          f"{got.get('opus|S1|badge_access|d1')}")
    check(got.get("sonnet|S1|badge_access|d1") == ["model_failure"],
          f"a model's own exit 2 is a final result, never retried: "
          f"{got.get('sonnet|S1|badge_access|d1')}")
    check(got.get("haiku|S1|badge_access|d1") == ["unruled"],
          f"a blank on length is the unruled case: {got.get('haiku|S1|badge_access|d1')}")
    check(got.get("luna|S1|badge_access|d1") == ["ok"],
          f"MUST NOT FIRE: a clean cell: {got.get('luna|S1|badge_access|d1')}")
    check(code == run_lineup.EXIT_DONE, f"the lane completes: exit {code}")


def test_a_usage_limit_stops_the_lane_and_the_resume_reruns_the_cell() -> None:
    """MUST FIRE: the CLI's usage-limit envelope, naming no reset time, stops the
    lane at exit 4 with the cell `usage_limit`, and the next start re-runs it.
    MUST NOT FIRE: the resumed cell is `ok`, and no other cell ran while the lane
    was stopped."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        reg = small_registration(pin, clone, items=("badge_access", "library_holds"),
                                 claude=fake_claude(run_dir, {"claude-sonnet-5": {
                                     "usage_limit_at": 1,
                                     "limit_text": "Claude usage limit reached."}}),
                                 rows=[claude_row("s", "claude-sonnet-5")])
        ctx = context(write_run(reg, run_dir))
        first = run_lineup.LaneRun(ctx, "subscription").run()
        after_first = states(ctx)
        second = run_lineup.LaneRun(ctx, "subscription").run()
        got = states(ctx)
    check(first == run_lineup.EXIT_USAGE_LIMIT
          and after_first == {"s|S1|badge_access|d1": ["usage_limit"]},
          f"the usage limit stops the lane on its first cell: {first} {after_first}")
    check(second == run_lineup.EXIT_DONE
          and got == {"s|S1|badge_access|d1": ["usage_limit", "ok"],
                      "s|S1|library_holds|d1": ["ok"]},
          f"MUST NOT FIRE: the resume re-runs the stopped cell and finishes: {second} {got}")


# --- 6. resume ---------------------------------------------------------------------------------

def test_a_stopped_lane_resumes_without_rerunning_finished_cells() -> None:
    """MUST FIRE: an attempt a dead process began and never ended is closed as
    `interrupted` and re-run. MUST NOT FIRE: a finished cell is not run again."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        with endpoint({}, run_dir / "fakes" / "http.json") as (fake, url):
            reg = small_registration(pin, clone, items=("badge_access", "library_holds"),
                                     rows=[http_row("a", "claude-opus-5-5", url)])
            ctx = context(write_run(reg, run_dir))
            first = run_lineup.LaneRun(ctx, "api", max_cells=1).run()
            calls_after_one = fake.calls
            ctx.journal.append({"type": "begin", "cell": "a|S1|library_holds|d1", "row": "a",
                                "set": "S1", "item": "library_holds", "draw": 1, "attempt": 1,
                                "lane": "api", "kind": "cell", "vendor": "anthropic",
                                "metered": True, "model": "claude-opus-5-5",
                                "dir": "cells/a/S1/library_holds/d1/a1",
                                "projection_usd": 0.5})
            second = run_lineup.LaneRun(ctx, "api").run()
            got = states(ctx)
    check(first == run_lineup.EXIT_DONE and calls_after_one > 0, f"the first run: {first}")
    check(got.get("a|S1|badge_access|d1") == ["ok"],
          f"MUST NOT FIRE: a finished cell is not re-run: {got.get('a|S1|badge_access|d1')}")
    check(got.get("a|S1|library_holds|d1") == ["interrupted", "ok"],
          f"a dangling attempt is closed as interrupted and re-run: "
          f"{got.get('a|S1|library_holds|d1')}")
    check(second == run_lineup.EXIT_DONE, f"the resumed lane completes: {second}")


# --- 7. the spend cap (I2) ------------------------------------------------------------------------

def test_the_cap_stops_a_lane_before_a_cell_that_could_exceed_it() -> None:
    """MUST FIRE: a cap below the first cell's projection stops the lane before any
    call, and a cap that one measured cell nearly exhausts stops the second.
    MUST NOT FIRE: a cap with room runs every cell."""
    clone, pin = shared_clone()
    for cap, want_code, want_cells in ((0.10, run_lineup.EXIT_GATED, 0),
                                       (0.35, run_lineup.EXIT_GATED, 1),
                                       (50.0, run_lineup.EXIT_DONE, 2)):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            run_dir = Path(tmp)
            with endpoint({}, run_dir / "fakes" / "http.json") as (fake, url):
                reg = small_registration(pin, clone, items=("badge_access", "library_holds"),
                                         caps={"anthropic": cap, "openai": 50.0,
                                               "overall": 100.0},
                                         rows=[http_row("a", "claude-opus-5-5", url,
                                                        cell_estimate_usd=0.2)])
                ctx = context(write_run(reg, run_dir))
                code = run_lineup.LaneRun(ctx, "api").run()
                ran = sum(len(v) for v in states(ctx).values())
                gated = [r for r in ctx.journal.read() if r.get("event") == "gated"]
            check(code == want_code and ran == want_cells,
                  f"cap ${cap}: exit {code} after {ran} cell(s), expected {want_code} after "
                  f"{want_cells}")
            if want_code == run_lineup.EXIT_GATED:
                check(gated and gated[-1]["need"] > gated[-1]["left"],
                      f"cap ${cap}: the gate must record what it refused: {gated}")


def test_a_cell_is_charged_what_was_billed_and_no_phantom() -> None:
    """MUST FIRE: a call with no reported usage (a timeout) is charged one estimate.
    MUST NOT FIRE: a 5xx discard is charged nothing; a clean report is charged its
    exact cost; a merge that died on an HTTP status with no report is charged
    nothing."""
    clone, pin = shared_clone()
    reg = small_registration(pin, clone, rows=[http_row("a", "claude-opus-5-5", "http://x/v1",
                                                        call_estimate_usd=0.25)])
    ctx = run_lineup.Context(registration=Path("x"), reg=reg, block_sha256="", run_dir=Path("."),
                             clone=clone, journal=run_lineup.Journal(Path("/nonexistent")),
                             rows={"a": reg["rows"][0]})
    row = reg["rows"][0]
    priced = {"state": "priced", "usd_exact": 0.1, "unpriced_calls": 0}
    clean = {"provenance": {"answering_cost": priced, "excluded": {"cost": {"usd_exact": None}},
                            "ledger": [{"prompt_tokens": 1, "completion_tokens": 1}],
                            "discarded_calls": []}}
    got = run_lineup.charge(ctx, row, clean, [], 9.0)
    check(abs(got["charged_usd"] - 0.1) < 1e-12 and got["charge_basis"] == "report",
          f"MUST NOT FIRE: a clean report is charged its exact cost: {got}")
    fivexx = copy.deepcopy(clean)
    fivexx["provenance"]["discarded_calls"] = [{"kind": "platform", "error": "HTTPStatusError"}]
    got = run_lineup.charge(ctx, row, fivexx, [], 9.0)
    check(abs(got["charged_usd"] - 0.1) < 1e-12,
          f"MUST NOT FIRE: a 5xx discard is not billed and not charged: {got}")
    timeout = copy.deepcopy(clean)
    timeout["provenance"]["discarded_calls"] = [{"kind": "platform", "error": "TimeoutError"}]
    got = run_lineup.charge(ctx, row, timeout, [], 9.0)
    check(abs(got["charged_usd"] - 0.35) < 1e-12 and got["charge_basis"] == "report+estimate",
          f"a timed-out call may be billed and is charged one estimate: {got}")
    got = run_lineup.charge(ctx, row, None, [], 9.0, stderr="error: HTTP 503 from x")
    check(got["charged_usd"] == 0.0, f"MUST NOT FIRE: a merge lost to a 503 bills nothing: {got}")
    got = run_lineup.charge(ctx, row, None, [], 9.0, killed=True)
    check(got["charged_usd"] == 9.0, f"a killed cell is charged its whole projection: {got}")


# --- 8. pre-warm ------------------------------------------------------------------------------

def test_prewarm_is_one_untimed_request_and_never_a_cell() -> None:
    """MUST FIRE: a lane with a prewarm block waits for health, sends one warm-up
    request, records an event, and the cell's report has no warm-up call in it.
    MUST NOT FIRE: a lane without one sends no warm-up."""
    clone, pin = shared_clone()
    for warm in (True, False):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            run_dir = Path(tmp)
            with endpoint({}, run_dir / "fakes" / "http.json") as (fake, url):
                row = http_row("q", "Qwen/Qwen3.8-27B-FP8", url, vendor="serverless",
                               metered=False, unpriced="self-hosted", lane="serverless",
                               window=32768, field_order="any")
                lanes = {"serverless": {"prewarm": {
                    "health_url": url.rsplit("/v1", 1)[0] + "/api/ps",
                    "timeout_seconds": 20}}} if warm else {"serverless": {}}
                reg = small_registration(pin, clone, rows=[row], lanes=lanes)
                ctx = context(write_run(reg, run_dir))
                code = run_lineup.LaneRun(ctx, "serverless").run()
                warmups = [b for b in fake.requests
                           if lineup_fakes.WARM_UP in str(b.get("messages"))]
                events = [r for r in ctx.journal.read() if r.get("event") == "prewarm"]
                ends_ = [r for r in ctx.journal.read() if r.get("type") == "end"]
                report = json.loads((run_dir / ends_[0]["dir"] / "report.json").read_text())
            in_report = [r for r in report["provenance"]["ledger"]
                         if r.get("estimated_prompt_tokens", 99) < 30]
            if warm:
                check(code == 0 and len(warmups) == 1 and len(events) == 1
                      and events[0]["ok"] and fake.gets,
                      f"one health check, one warm-up, one event: code {code}, "
                      f"{len(warmups)} warm-up(s), events {events}, gets {fake.gets}")
                check(len(ends_) == 1 and report["provenance"]["counts"]["calls"]
                      == len(fake.requests) - 1 and not in_report,
                      "the warm-up must not be a cell nor a call in the cell's report")
            else:
                check(not warmups and not events,
                      f"MUST NOT FIRE: no prewarm block, no warm-up: {len(warmups)} {events}")


# --- 9. the thinking pilot --------------------------------------------------------------

def test_the_pilot_flags_a_call_over_sixty_percent_of_its_ceiling() -> None:
    """MUST FIRE: 70% of a verify ceiling, and a ceiling cut. MUST NOT FIRE: 50%, a
    merge call, and a call with no ceiling sent."""
    report = {"provenance": {"ledger": [
        {"role": "verify", "max_tokens": 1000, "completion_tokens": 700, "outcome": "answer"},
        {"role": "decompose", "max_tokens": 1000, "completion_tokens": 500, "outcome": "answer"},
        {"role": "merge", "max_tokens": 1000, "completion_tokens": 990, "outcome": "answer"},
        {"role": "verify", "max_tokens": None, "completion_tokens": 50000, "outcome": "answer"},
        {"role": "verify", "max_tokens": 1000, "completion_tokens": 1000, "outcome": "ceiling"},
    ], "discarded_calls": [{"role": "decompose", "kind": "blank_length", "max_tokens": 800}]}}
    rows = run_lineup.utilisation(report)
    flags = [(r["role"], r["share"], r["cut"]) for r in rows if r["flag"]]
    check(len(rows) == 5, f"merge calls are out of the pilot's table: {len(rows)}")
    check(("verify", 0.7, False) in flags and ("verify", 1.0, True) in flags
          and ("decompose", None, True) in flags,
          f"70% and the two cuts must be flagged: {flags}")
    check(("decompose", 0.5, False) not in flags and len(flags) == 3,
          f"MUST NOT FIRE: 50% and a call with no ceiling: {flags}")


def test_the_pilot_runs_on_and_off_and_writes_its_table() -> None:
    """End to end on the fake 27B: two cells per item, thinking on and off, each
    asserted as it ran, and the utilisation table flags the fake's 70%."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        with endpoint({"Qwen/Qwen3.8-27B-FP8": {"utilisation": 0.7}},
                      run_dir / "fakes" / "http.json") as (_fake, url):
            row = http_row("q", "Qwen/Qwen3.8-27B-FP8", url, vendor="serverless",
                           metered=False, unpriced="self-hosted", lane="serverless",
                           window=32768, field_order="any")
            reg = small_registration(pin, clone, rows=[row], lanes={"serverless": {}})
            ctx = context(write_run(reg, run_dir))
            code = run_lineup.thinking_pilot(ctx, "q", ["S1:badge_access"])
            table = json.loads((run_dir / "thinking-pilot" / "utilisation.json").read_text())
            counted = run_lineup.ends(ctx.journal.read())
    check(code == 0 and [t["thinking"] for t in table] == ["on", "off"]
          and all(t["state"] == "ok" for t in table),
          f"the pilot runs one cell per mode: {code} {table}")
    check(all(t["flagged"] and abs(t["max_share"] - 0.7) < 0.01 for t in table),
          f"the fake's 70% must be flagged: {[t['max_share'] for t in table]}")
    check(not counted, f"MUST NOT FIRE: the pilot's cells are never counted: {list(counted)}")


# --- 10. the figures -----------------------------------------------------------------------------

def _scored(row: str, pair: str, draw: int = 1, *, state: str = "ok", silent: int = 0,
            dev: int = 2, usd: float = 0.1, seconds: float = 10.0) -> dict:
    record = {"cell": f"{row}|S1|{pair}|d{draw}", "row": row, "model": row, "set": "S1",
              "pair": pair, "draw": draw, "state": state,
              "excluded": "" if state == "ok" else state, "attempts": 1, "exit_code": 0,
              "started_at": "2026-09-28T10:00:00+00:00", "claimcheck_commit": "a" * 12}
    if state == "ok":
        record.update(silent=silent, decl=0, lost=dev, bloat=0, dup=0, near_dup=0,
                      model_confirmed=0, absent_rejected=0, usd=usd, billed=usd * 1.1,
                      seconds=seconds, duration_seconds=seconds)
    return record


def _figures_reg(rows: list[str], pairs: list[str] | None = None) -> dict:
    reg = run_lineup.template(pin="a" * 40)
    reg["sets"] = {"S1": {"kind": "merge", "score": "pairs", "root": "tests/pairs",
                          "fidelity": "high", "items": pairs or ["badge_access",
                                                                 "library_holds",
                                                                 "rate_limits"],
                          "draws": {"default": 1}}}
    reg["rows"] = [{"id": r, "model": "claude-opus-5-5", "lane": "api", "vendor": "anthropic",
                    "route": {"kind": "http", "base_url": "http://x/v1", "profile": "anthropic"},
                    "sets": ["S1"]} for r in rows]
    return reg


def test_figures_check_reproduces_a_real_run_and_catches_a_tamper() -> None:
    """MUST NOT FIRE: `--check` on the run it just wrote. MUST FIRE: a merged.md
    edited after scoring; a figure edited in figures.json."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        behaviour = {"gpt-6-luna": {"merge": "lossy"}}
        with endpoint(behaviour, run_dir / "fakes" / "http.json") as (_fake, url):
            reg = small_registration(pin, clone, items=("badge_access", "library_holds"),
                                     rows=[http_row("opus", "claude-opus-5-5", url),
                                           http_row("luna", "gpt-6-luna", url,
                                                    vendor="openai")])
            ctx = context(write_run(reg, run_dir))
            code = run_lineup.LaneRun(ctx, "api").run()
        check(code == 0, f"the run completes: {code}")
        check(lineup_figures.main(["--run-dir", str(run_dir), "--write"]) == 0, "--write")
        formed = json.loads((run_dir / "figures.json").read_text())
        check([d["row"] for d in formed["S1"]["order"]["disqualified"]] == ["luna"],
              f"the lossy fake is disqualified on silent loss: {formed['S1']['order']}")
        check(lineup_figures.check(run_dir) == [],
              f"MUST NOT FIRE: --check on the run it wrote: {lineup_figures.check(run_dir)}")
        end = [r for r in ctx.journal.read() if r.get("type") == "end"
               and r["row"] == "opus"][0]
        merged = run_dir / end["dir"] / "merged.md"
        original = merged.read_text()
        kept = [line for line in original.splitlines() if "security office" not in line]
        merged.write_text("\n".join(kept) + "\n")
        check(any("no longer give scored.json" in p for p in lineup_figures.check(run_dir)),
              "a merged.md edited after scoring must be caught")
        merged.write_text(original)
        tampered = copy.deepcopy(formed)
        tampered["S1"]["rows"]["opus"]["deviations"] += 1
        (run_dir / "figures.json").write_text(json.dumps(tampered))
        check(any("figures.json" in p for p in lineup_figures.check(run_dir)),
              "an edited figure in figures.json must be caught")


# --- 11. the second bug hunt's fixes, each seeded both ways ---------------

def test_684_n1_the_classifier_needs_positive_evidence_for_a_model_failure() -> None:
    """N1, N4, N8, N10. Each shape the report confirmed, built with the tool's own
    exception classes and messages. MUST FIRE: `model_failure` for the tool's three
    sentences with a `failed` ledger row. MUST NOT FIRE: `model_failure` for a lost
    login, the CLI's blank, a 400, `error_during_execution`, a crash, a Python
    exception in a step, or a schema sentence with no `failed` row; and `unruled`
    for a schema failure whose text says "not truncated"."""
    from llossless import backend, parsing, transport, window  # noqa: PLC0415
    from llossless.client import SchemaFailure  # noqa: PLC0415

    def detail(exc) -> str:  # as `cli.step` writes it
        return str(exc) if isinstance(exc, SchemaFailure) else f"{type(exc).__name__}: {exc}"

    http = {"route": {"kind": "http", "profile": "openai-compatible"}}
    google = {"route": {"kind": "http", "profile": "google"}}
    cli = {"route": {"kind": "claude", "profile": "subscription"}}
    failed = [{"role": "merge", "outcome": "repair"}, {"role": "merge", "outcome": "failed"}]
    answered = [{"role": "merge", "outcome": "answer"}]

    def report(exc_or_text, *, ledger=None, discards=(), unruled=None, code=2):
        text = exc_or_text if isinstance(exc_or_text, str) else detail(exc_or_text)
        return {"exit_code": code, "provenance": {
            "ledger": answered if ledger is None else ledger, "unruled": unruled,
            "discarded_calls": [{"kind": k} for k in discards]},
            "steps": [{"name": "merge", "state": "errored", "detail": text}]}

    def env(result, **extra):
        return json.dumps({"type": "result", "subtype": "success", "is_error": True,
                           "result": result, **extra})

    not_truncated = parsing.ParseError(
        "JSON is unterminated: a string value was opened and never closed. The response is "
        "not truncated -- it ends on its own '}' and its '{'/'}' counts balance at 1 -- so a "
        "quote or newline inside a string value is unescaped.")
    oauth = backend._classified_error(
        "'claude' exited 1 for model claude-opus-5-5 at claude",
        env("OAuth token has expired. Please obtain a new token or refresh your existing "
            "token.", api_error_status=401, terminal_reason="api_error"))
    login = backend._classified_error("'claude' reported the turn as an error (success)",
                                      env("Invalid API key · Please run /login"))
    cli_400 = backend._classified_error(
        "'claude' reported the turn as an error (success)",
        env('API Error: 400 {"type":"error","error":{"type":"invalid_request_error",'
            '"message":"prompt is too long"}}', api_error_status=400, terminal_reason="api_error"))
    cli_400_other = backend._classified_error(
        "'claude' reported the turn as an error (success)",
        env('API Error: 400 {"type":"error","error":{"type":"invalid_request_error",'
            '"message":"messages: unexpected field"}}', api_error_status=400))
    during = backend._classified_error(
        "'claude' reported the turn as an error (error_during_execution)",
        json.dumps({"type": "result", "subtype": "error_during_execution", "is_error": True}))
    crash = backend.CommandError("'claude' exited 1 for model claude-opus-5-5 at claude\n"
                                 "Error: ENOSPC: no space left on device, write")
    blank_cli = backend.CommandError(
        "'claude' answered with a result envelope whose `result` is empty")
    overloaded = backend._classified_error(
        "'claude' reported the turn as an error (success)",
        env("API Error: 529 overloaded", api_error_status=529))
    context_400 = transport.HTTPStatusError(
        400, '{"object":"error","message":"This model\'s maximum context length is 32768 '
        'tokens. However, you requested 33012 tokens.","code":400}', "pod", "Qwen/Qwen3.8-27B")
    plain_400 = transport.HTTPStatusError(400, '{"error":"bad field"}', "pod", "m")
    limits = json.loads((ROOT / "arms" / "2026-09-18" / "matrix" /
                         "results_anthropic.json").read_text(encoding="utf-8"))
    anthropic_limit = next(r["stderr_tail"] for r in limits
                           if "usage limits" in str(r.get("stderr_tail")))
    cases = [
        # must fire: the model's own output failed after the tool's repairs
        (http, report(SchemaFailure("merge", str(not_truncated), None), ledger=failed),
         "", "model_failure"),
        (http, report(SchemaFailure("merge", "invalid JSON: Expecting value", None),
                      ledger=failed), "", "model_failure"),
        (http, report(SchemaFailure("merge", "x", None, why="merge: m gave every field this "
                                    "response needs, valid, and in the wrong order -- x"),
                      ledger=failed), "", "model_failure"),
        (http, report(SchemaFailure("verify", "x", None, why="verify: m answered in a "
                                    "repetition loop and did it again"),
                      ledger=failed), "", "model_failure"),
        # must not fire: the sentence with no `failed` row behind it
        (http, report(SchemaFailure("merge", "invalid JSON", None), ledger=answered), "",
         "unclassified"),
        # must not fire: none of these is the model's
        (cli, report(oauth), "", "halted"),
        (cli, report(login), "", "halted"),
        (cli, report(cli_400), "", "window"),
        (cli, report(cli_400_other), "", "unclassified"),
        (cli, report(during), "", "unclassified"),
        (cli, report(crash), "", "unclassified"),
        (cli, report(blank_cli), "", "platform"),
        (cli, report(overloaded), "", "platform"),
        (http, report(KeyError("dispositions")), "", "unclassified"),
        (http, report(context_400), "", "window"),
        (http, report(plain_400), "", "unclassified"),
        (http, report(transport.HTTPStatusError(503, "busy", "h", "m")), "", "platform"),
        (http, report(transport.HTTPStatusError(401, "bad key", "h", "m")), "", "halted"),
        (http, report("PinnedTierViolated: x"), "", "halted"),
        (http, report(window.BudgetExceedsWindow("merge needs 55667 tokens")), "", "window"),
        # blanks, refusals and runaways, read off the structured fields (N4, N6)
        (http, report("EmptyResponse: h answered 3 times with an empty body at tier prompt"),
         "", "platform"),
        (http, report("EmptyResponse: h answered 3 times with an empty body at tier prompt",
                      discards=("blank_refusal",) * 3), "", "refused"),
        (http, report("EmptyResponse: h exhausted its output ceiling on m",
                      discards=("blank_length",)), "", "unruled"),
        (http, report("Truncated: verify: m stopped on its 900-token output ceiling",
                      ledger=[{"role": "verify", "outcome": "ceiling"}]), "", "unruled"),
        (http, report("Truncated: merge: 9000 prompt tokens were sent and the endpoint "
                      "counted 3000"), "", "unclassified"),
        (http, report("x", code=0, unruled={"calls": {"blank_refusal": 1}}), "", "ok"),
        ({"route": {"kind": "http", "profile": "openai-reasoning"}},
         report(transport.HTTPStatusError(400, '{"error":{"message":"Invalid prompt: your '
                'prompt was flagged as potentially violating our usage policy.","code":'
                '"invalid_prompt"}}', "api.openai.com", "gpt-6-sol")), "", "refused"),
        # no report: the stderr, and the discard dumps as `dumps`
        (http, None, "error: HTTP 503 from 127.0.0.1 for model m", "platform"),
        (http, None, "error: HTTP 401 from api for model m", "halted"),
        (http, None, "Traceback (most recent call last):\n  KeyError: 'x'", "unclassified"),
        (google, None, "HTTP 429: You exceeded your current quota ... "
         "GenerateRequestsPerDayPerProjectPerModel-FreeTier", "usage_limit"),
        (google, None, "HTTP 400: this API requires a billing account with prepayment",
         "halted"),
        # N10: a vendor's spend limit stops the lane; an ordinary rate limit does not
        ({"route": {"kind": "http", "profile": "anthropic"}}, None, anthropic_limit,
         "usage_limit"),
        ({"route": {"kind": "http", "profile": "anthropic"}},
         report("HTTPStatusError: " + anthropic_limit.removeprefix("error: ")), "",
         "usage_limit"),
        ({"route": {"kind": "http", "profile": "openai-reasoning"}},
         report(transport.HTTPStatusError(429, '{"error":{"message":"You exceeded your '
                'current quota, please check your plan and billing details.","type":'
                '"insufficient_quota"}}', "api.openai.com", "gpt-6-sol")), "", "usage_limit"),
        ({"route": {"kind": "http", "profile": "openai-reasoning"}},
         report(transport.HTTPStatusError(429, '{"error":{"message":"Rate limit reached for '
                'gpt-6-sol on tokens per min"}}', "api.openai.com", "gpt-6-sol")), "",
         "platform"),
    ]
    for row, rep, stderr, want in cases:
        got, why = run_lineup.classify(row, (rep or {}).get("exit_code", 2), rep, stderr, [],
                                       False)
        check(got == want, f"classify {str(rep and rep['steps'][0]['detail'])[:90]!r} "
                           f"{stderr[:50]!r}: {got} ({why[:1]}), expected {want}")
    # No report: the discard dumps name the refusal, and a CLI refusal envelope.
    got, _ = run_lineup.classify(http, 2, None, "error: h answered 3 times with an empty body",
                                 [], False, dumps={"blank_refusal": 3})
    check(got == "refused", f"a refusal read off the discard dumps: {got}")
    refusal_call = {"rc": 0, "stderr": "", "envelope": {"is_error": False,
                                                       "result": lineup_fakes.CLI_REFUSAL}}
    got, _ = run_lineup.classify(cli, 2, report(SchemaFailure("merge", "invalid JSON", None),
                                                ledger=failed), "", [refusal_call] * 5, False)
    check(got == "refused", f"the CLI's refusal, answered five times as prose: {got}")
    stopped = {"rc": 0, "stderr": "", "envelope": {"is_error": False, "result": "",
                                                  "stop_reason": "refusal"}}
    got, _ = run_lineup.classify(cli, 2, report(blank_cli), "", [stopped], False)
    check(got == "refused", f"a CLI envelope with stop_reason refusal: {got}")
    answer_call = {"rc": 0, "stderr": "", "envelope": {"is_error": False,
                                                      "result": '{"merged_document": "violates '
                                                                'our usage policy"}'}}
    got, _ = run_lineup.classify(cli, 2, report(SchemaFailure("merge", "invalid JSON", None),
                                                ledger=failed), "", [answer_call], False)
    check(got == "model_failure", f"MUST NOT FIRE: a JSON answer quoting a usage policy is "
                                  f"not a refusal: {got}")


def test_684_n1_a_lost_login_halts_the_lane_and_the_resume_reruns_the_cell() -> None:
    """N1 end to end. MUST FIRE: the fake CLI's login expires on the cell's third
    call; the cell is `halted`, never `model_failure`, and the lane stops (exit 5)
    before the next cell. MUST NOT FIRE: after a new login the resume re-runs that
    cell and finishes the lane, every cell `ok`."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        reg = small_registration(pin, clone, items=("badge_access", "library_holds"),
                                 claude=fake_claude(run_dir, {"claude-opus-5-5": {
                                     "oauth_expired_at": 3}}),
                                 rows=[claude_row("o", "claude-opus-5-5")])
        ctx = context(write_run(reg, run_dir))
        first = run_lineup.LaneRun(ctx, "subscription").run()
        after_first = states(ctx)
        lineup_fakes.relogin(run_dir / "fakes" / "state.json", "claude-opus-5-5")
        second = run_lineup.LaneRun(ctx, "subscription").run()
        got = states(ctx)
    check(first == run_lineup.EXIT_REFUSED
          and after_first == {"o|S1|badge_access|d1": ["halted"]},
          f"a lost login halts the lane at its cell: {first} {after_first}")
    check(second == run_lineup.EXIT_DONE
          and got == {"o|S1|badge_access|d1": ["halted", "ok"],
                      "o|S1|library_holds|d1": ["ok"]},
          f"MUST NOT FIRE: after a new login the cell is re-run and counted: {second} {got}")


def _vendor_0925(*, luna_fails: bool = False, window_row: bool = False) -> tuple[dict, list]:
    """The committed 2026-09-25 vendor cells (draw 1, `high`) as lineup scored cells."""
    data = json.loads((ROOT / "arms" / "2026-09-25" / "vendor" / "scored.json").read_text(
        encoding="utf-8"))
    arms = ("claude-opus-5-5", "gpt-6-sol", "gpt-6-luna")
    cells = []
    for c in data:
        if c["arm"] not in arms or c["draw"] != 1 or c["fidelity"] != "high":
            continue
        state = "ok" if not c["excluded"] else "platform"
        cells.append({"cell": f"{c['arm']}|S1|{c['pair']}|d1", "row": c["arm"],
                      "model": c["arm"], "set": "S1", "pair": c["pair"], "draw": 1,
                      "state": state, "excluded": "" if state == "ok" else state,
                      "started_at": c["started_at"], "claimcheck_commit": c["claimcheck_commit"],
                      **{k: c.get(k, 0) for k in ("silent", "lost", "bloat", "dup",
                                                   "model_confirmed", "absent_rejected")},
                      "usd": c.get("usd"), "billed": c.get("ledger_usd"),
                      "seconds": c.get("seconds")})
    ids = list(arms)
    if luna_fails:
        cells = [dict(c, state="model_failure", excluded="model_failure")
                 if (c["row"], c["pair"]) == ("gpt-6-luna", "rate_limits") else c
                 for c in cells]
    if window_row:
        ids.append("qwen-like")
        for c in [c for c in cells if c["row"] == "claude-opus-5-5"]:
            twin = dict(c, row="qwen-like", model="qwen-like",
                        cell=c["cell"].replace("claude-opus-5-5", "qwen-like"))
            if c["pair"] in ("index_429", "rate_limits"):
                twin.update(state="window", excluded="window")
            cells.append(twin)
    reg = _figures_reg(ids, pairs=list(run_lineup.PAIRS))
    return reg, cells


def test_684_n2_n3_a_rows_own_failure_never_shrinks_the_others_pairs() -> None:
    """N2 and N3 on the committed 2026-09-25 cells. MUST NOT FIRE: as recorded, Sol
    first, Opus 5.5 second, Luna disqualified (2 silent-loss segments, both on
    rate_limits). MUST FIRE: Luna's own exit 2 on rate_limits keeps all nine pairs
    in the common set, and Luna is listed after every complete row, not first (the old
    rule put it first); a headline row whose index_429 and rate_limits are `window`
    shrinks nobody, and Luna stays disqualified."""
    reg, cells = _vendor_0925()
    formed = lineup_figures.rows(reg, cells)["S1"]
    check(len(formed["common_pairs"]) == 9
          and formed["order"]["survivors"] == ["gpt-6-sol", "claude-opus-5-5"]
          and [d["row"] for d in formed["order"]["disqualified"]] == ["gpt-6-luna"],
          f"MUST NOT FIRE: the recorded order: {formed['order']}")
    reg, cells = _vendor_0925(luna_fails=True)
    formed = lineup_figures.rows(reg, cells)["S1"]
    luna = formed["rows"]["gpt-6-luna"]
    check(len(formed["common_pairs"]) == 9,
          f"Luna's own exit 2 must not shrink the common pairs: {formed['common_pairs']}")
    check(formed["order"]["survivors"] == ["gpt-6-sol", "claude-opus-5-5"]
          and [d["row"] for d in formed["order"]["incomplete"]] == ["gpt-6-luna"]
          and formed["order"]["ranks"]["gpt-6-luna"] == 3,
          f"Luna must be listed after every complete row, never first: {formed['order']}")
    check(luna["incomplete_text"] == "exit 2 on 1 of 9" and luna["pairs"] == 8,
          f"Luna's row says what it did not complete: {luna['incomplete_text']} "
          f"{luna['pairs']}")
    reg, cells = _vendor_0925(window_row=True)
    formed = lineup_figures.rows(reg, cells)["S1"]
    check(len(formed["common_pairs"]) == 9
          and [d["row"] for d in formed["order"]["disqualified"]] == ["gpt-6-luna"]
          and formed["order"]["survivors"][0] == "gpt-6-sol"
          and [d["row"] for d in formed["order"]["incomplete"]] == ["qwen-like"]
          and formed["rows"]["qwen-like"]["incomplete_text"] == "window on 2 of 9",
          f"a window row decides nobody's disqualification: {formed['common_pairs']} "
          f"{formed['order']}")


def test_688_nothing_shrinks_the_common_pairs() -> None:
    """The old shrink rule was superseded. MUST FIRE: a pair B lost to the
    platform stays in every row's common set, and only B is incomplete, "not measured
    (platform) on 1 of 3"; the rule's old switch is refused. MUST NOT FIRE: A, which
    completed everything, ranks first on all three pairs; C, which counted nothing,
    shrinks nothing and is listed."""
    reg = _figures_reg(["A", "B", "C"])
    pairs = ["badge_access", "library_holds", "rate_limits"]
    cells = [_scored("A", p) for p in pairs]
    cells += [_scored("B", "badge_access"), _scored("B", "library_holds"),
              _scored("B", "rate_limits", state="platform")]
    cells += [_scored("C", p, state="platform") for p in pairs]
    formed = lineup_figures.rows(reg, cells)["S1"]
    check(formed["common_pairs"] == pairs and "left_out" not in formed,
          f"a pair lost to the platform never leaves the common set: {formed['common_pairs']}")
    check(formed["order"]["survivors"] == ["A"]
          and formed["rows"]["B"]["incomplete_text"] == "not measured (platform) on 1 of 3"
          and [d["row"] for d in formed["order"]["incomplete"]] == ["B", "C"]
          and formed["rows"]["A"]["pairs"] == 3,
          f"only B misses rate_limits; C is listed: {formed['order']}")
    clone, pin = shared_clone()
    for name, value in (("platform_lost", "shrink"), ("platform_lost", "not_measured"),
                        ("unruled_counts", "excluded"), ("refusal_counts", "excluded")):
        bad = small_registration(pin, clone, rows=[http_row("a", "claude-opus-5-5",
                                                            "http://x/v1")])
        bad["rules"] = {name: value}
        check(any(f"rules.{name}" in problem for problem in run_lineup.validate(bad)),
              f"rules.{name}: {value} must be refused")
    try:
        figure_rules.lineup_groups([], ("A",), "row", pairs, treat=lambda c: "done",
                                   platform_lost="shrink")
        failures.append("lineup_groups must no longer take platform_lost")
    except TypeError:
        pass


def test_684_n2_a_fixture_failure_never_shrinks_the_others_fixtures() -> None:
    """S2 by the same rule. MUST FIRE: B's exit 2 on one fixture keeps all three in the
    common set, and B follows A with "exit 2 on 1 of 3"; B's fixture lost to the
    platform keeps them too, B "not measured"."""
    names = ["dedup", "paraphrase", "hallucination"]
    reg = _figures_reg(["A", "B"])
    reg["sets"] = {"S2": {"kind": "detect", "score": "detect", "root": "tests/fixtures",
                          "items": names, "headline_items": names, "draws": {"default": 1}}}
    for row in reg["rows"]:
        row["sets"] = ["S2"]

    def fixture(row, name, state="ok"):
        expected = run_detect.load_expected(name)
        graded = run_detect.grade(expected, {}, 0 if state == "ok" else 2)
        return {"cell": f"{row}|S2|{name}|d1", "row": row, "model": row, "set": "S2",
                "pair": name, "draw": 1, "state": state, "detect": graded,
                "excluded": "" if state == "ok" else state, "usd": 0.1, "seconds": 1.0,
                "started_at": "2026-09-28T10:00:00+00:00", "claimcheck_commit": "a" * 12}
    cells = [fixture("A", n) for n in names] + [fixture("B", "dedup"),
                                                fixture("B", "paraphrase"),
                                                fixture("B", "hallucination", "model_failure")]
    formed = lineup_figures.rows(reg, cells)["S2"]
    check(formed["common_fixtures"] == names and formed["order"] == ["A", "B"]
          and formed["rows"]["B"]["incomplete_text"] == "exit 2 on 1 of 3"
          and formed["rows"]["A"]["fixtures_measured"] == 3,
          f"B's own exit 2 must not shrink A's fixtures: {formed['common_fixtures']} "
          f"{formed['order']} {formed['rows']['B']['incomplete_text']}")
    cells[-1] = fixture("B", "hallucination", "platform")
    formed = lineup_figures.rows(reg, cells)["S2"]
    check(formed["common_fixtures"] == names
          and formed["rows"]["B"]["incomplete_text"] == "not measured (platform) on 1 of 3",
          f"a fixture lost to the platform stays in the set, B's alone: "
          f"{formed['common_fixtures']} {formed['rows']['B']['incomplete_text']}")


def test_684_n3_the_window_is_a_registration_edit_and_the_pilot_fits_it() -> None:
    """N3 and N15. A self-hosted row's own fake registers a window (the 27B
    itself is dropped from the release lineup; this is generic self-hosted coverage).
    `merge_need` reproduces the tool's own figures from its own arithmetic. MUST FIRE:
    the thinking pilot refuses an item over the stated window before any call.
    MUST NOT FIRE: at 65,536 the shipped pilot items fit."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        with endpoint({}, run_dir / "fakes" / "http.json") as (fake, url):
            q = http_row("q", "Qwen/Qwen3.8-27B-FP8", url, vendor="serverless", metered=False,
                         unpriced="self-hosted", lane="serverless", window=32768,
                         field_order="any", route={"kind": "http", "base_url": url,
                                                   "key_env": KEY,
                                                   "profile": "openai-compatible"})
            reg = small_registration(pin, clone, rows=[q], lanes={"serverless": {}},
                                     items=list(run_lineup.PAIRS))
            reg["sets"]["S3"] = {"kind": "merge", "score": "planted",
                                 "root": "tests/handwritten", "fidelity": "open",
                                 "items": ["voyager", "bip39", "mahjongg"],
                                 "draws": {"default": 1}}
            q["sets"] = ["S1", "S3"]
            ctx = context(write_run(reg, run_dir))
            need = {item: run_lineup.merge_need(ctx, q, set_id, item) for set_id, item in (
                ("S1", "index_429"), ("S1", "rate_limits"), ("S3", "mahjongg"),
                ("S3", "bip39"))}
            try:
                run_lineup.thinking_pilot(ctx, "q", ["S1:rate_limits", "S3:bip39"])
                failures.append("the pilot must refuse an item over the stated window")
            except run_lineup.Refusal as exc:
                check("S1:rate_limits needs 55667" in exc.message and "bip39" not in
                      exc.message, f"the refusal names what does not fit: {exc.message}")
            check(fake.calls == 0, f"the refused pilot made {fake.calls} call(s)")
    check(need == {"index_429": 38687, "rate_limits": 55667, "mahjongg": 139173,
                   "bip39": 25422}, f"the tool's own window needs: {need}")
    check(need["rate_limits"] <= 65536 and need["index_429"] <= 65536
          and need["bip39"] <= 65536,
          f"MUST NOT FIRE: the pilot items fit 65,536: {need}")


def test_684_n4_a_refusal_is_refused_on_either_route_final_and_charged_once() -> None:
    """N4 end to end. MUST FIRE: the refusal shape over HTTP (200, content null,
    content_filter) and the CLI's refusal sentence are both `refused`: final, one
    attempt, never re-queued as the platform's, charged once. MUST NOT FIRE: a clean
    row beside them is `ok`, and the lane completes."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        behaviour = {"claude-opus-5-5": {"refuse_merge_on": ["Badge Access"]}}
        with endpoint(behaviour, run_dir / "fakes" / "http.json") as (_fake, url):
            reg = small_registration(pin, clone, claude=fake_claude(run_dir, behaviour),
                                     retry={"passes": 2, "spacing_seconds": 0, "breaker": 5},
                                     rows=[http_row("opus", "claude-opus-5-5", url),
                                           claude_row("opus-sub", "claude-opus-5-5"),
                                           http_row("luna", "gpt-6-luna", url,
                                                    vendor="openai")])
            ctx = context(write_run(reg, run_dir))
            api = run_lineup.LaneRun(ctx, "api").run()
            sub = run_lineup.LaneRun(ctx, "subscription").run()
            got = states(ctx)
            charged = [r["charged_usd"] for r in ctx.journal.read()
                       if r.get("type") == "end" and r["row"] == "opus"]
            flags = {r["row"]: r.get("flag") for r in ctx.journal.read()
                     if r.get("type") == "end"}
    check(flags.get("opus") == run_lineup.REFUSED_FLAG
          and flags.get("opus-sub") == run_lineup.REFUSED_FLAG and flags.get("luna") is None,
          f"a refusal's cell record carries the flag, a clean one none: {flags}")
    check(got.get("opus|S1|badge_access|d1") == ["refused"],
          f"a content_filter merge is refused, once: {got.get('opus|S1|badge_access|d1')}")
    check(got.get("opus-sub|S1|badge_access|d1") == ["refused"],
          f"the CLI's refusal is refused too: {got.get('opus-sub|S1|badge_access|d1')}")
    check(len(charged) == 1, f"a refusal is charged once, never per retry pass: {charged}")
    check(got.get("luna|S1|badge_access|d1") == ["ok"] and api == 0 and sub == 0,
          f"MUST NOT FIRE: the clean row, and both lanes complete: {got} {api} {sub}")


def test_688_a_refusal_counts_against_the_row_flagged_and_never_shrinks() -> None:
    """MUST FIRE: B's refusal lists B after every complete row, "refused
    (prompt or guardrail) on 1 of 3", in figures.json and figures.md. MUST NOT FIRE: the
    common set keeps the refused pair, A is ranked on all three, and `excluded` is no
    longer a value the registration may hold."""
    reg = _figures_reg(["A", "B"])
    pairs = ["badge_access", "library_holds", "rate_limits"]
    cells = [_scored("A", p, dev=3) for p in pairs]
    cells += [_scored("B", "badge_access", dev=1), _scored("B", "library_holds", dev=1),
              _scored("B", "rate_limits", state="refused")]
    formed = lineup_figures.rows(reg, cells)
    block = formed["S1"]
    check(block["common_pairs"] == pairs and block["order"]["survivors"] == ["A"]
          and [d["row"] for d in block["order"]["incomplete"]] == ["B"]
          and block["rows"]["B"]["incomplete_text"]
          == "refused (prompt or guardrail) on 1 of 3" and block["rows"]["A"]["pairs"] == 3,
          f"B's refusal counts against it, flagged: {block['order']}")
    text = lineup_figures.render(reg, json.loads(json.dumps(formed)))
    check("refused (prompt or guardrail) on 1 of 3" in text,
          "figures.md names the refusal with its flag")
    clone, pin = shared_clone()
    reg = small_registration(pin, clone, rows=[http_row("a", "claude-opus-5-5", "http://x/v1")])
    reg["rules"] = {"refusal_counts": "excluded"}
    check(any("rules.refusal_counts" in p for p in run_lineup.validate(reg)),
          "refusal_counts is fixed at row")


def test_684_n5_the_floors_are_scored_and_a_row_no_better_than_the_union_is_flagged() -> None:
    """N5. The floors from the sources, no model call: concatenation 79, the union 70,
    base-only 129 silent over the nine pairs. MUST FIRE: a row with the union's own
    deviations is flagged. MUST NOT FIRE: a row below it is not."""
    floors = lineup_figures.baselines(list(run_lineup.PAIRS), "source_a.md")
    over = {name: lineup_figures._floor(per, list(run_lineup.PAIRS))
            for name, per in floors.items()}
    check((over["concatenation"]["silent_loss"], over["concatenation"]["deviations"]) == (0, 79)
          and (over["union"]["silent_loss"], over["union"]["deviations"]) == (0, 70)
          and over["base_only"]["silent_loss"] == 129,
          f"the floors: {over}")
    reg = _figures_reg(["copycat", "good"], pairs=list(run_lineup.PAIRS))
    cells = []
    for pair in run_lineup.PAIRS:
        cells.append(_scored("copycat", pair, dev=floors["union"][pair]["deviations"]))
        cells.append(_scored("good", pair, dev=max(0, floors["union"][pair]["deviations"] - 1)))
    formed = lineup_figures.rows(reg, cells)["S1"]
    check(formed["rows"]["copycat"]["no_better_than_union"],
          "a row with the union's deviations must be flagged")
    check(not formed["rows"]["good"]["no_better_than_union"],
          "MUST NOT FIRE: a row below the union")
    text = lineup_figures.render(reg, json.loads(json.dumps(lineup_figures.rows(reg, cells))))
    check("| base | union | 9 of 9 | 0 | 0.00 | 70 | 7.78 |" in text
          and "no better than a mechanical union: copycat." in text,
          "figures.md prints the floors and names the flagged row")


def test_684_n7_the_headline_reads_the_lowest_counted_draw() -> None:
    """N7. MUST FIRE: A's draw 1 of rate_limits lost to the platform, draws 2 and 3
    counted: the pair stays in the headline on A's draw 2, and B's silent loss there
    still disqualifies B. MUST NOT FIRE: with draw 1 counted the headline is draw 1,
    never a better later draw."""
    reg = _figures_reg(["A", "B"])
    pairs = ["badge_access", "library_holds", "rate_limits"]
    cells = []
    for row in ("A", "B"):
        for pair in pairs:
            for draw in (1, 2, 3):
                lost = (row, pair, draw) == ("A", "rate_limits", 1)
                cells.append(_scored(row, pair, draw, state="platform" if lost else "ok",
                                     silent=3 if (row, pair) == ("B", "rate_limits") else 0,
                                     dev=draw))
    formed = lineup_figures.rows(reg, cells)["S1"]
    check(formed["common_pairs"] == pairs
          and formed["rows"]["A"]["headline_draws"]["rate_limits"] == 2
          and [d["row"] for d in formed["order"]["disqualified"]] == ["B"],
          f"a lost draw 1 falls through to draw 2: {formed['common_pairs']} "
          f"{formed['rows']['A']['headline_draws']} {formed['order']}")
    check(formed["rows"]["A"]["headline_draws"]["badge_access"] == 1
          and formed["rows"]["A"]["deviations"] == 1 + 1 + 2,
          f"MUST NOT FIRE: a counted draw 1 is the headline: "
          f"{formed['rows']['A']['headline_draws']} {formed['rows']['A']['deviations']}")


def test_684_n8_equal_deviations_share_a_rank_unless_both_are_list_priced() -> None:
    """N8. MUST FIRE: two list-priced rows tied on deviations are ordered by dollars;
    a subscription row tied with list rows shares their rank, whatever either costs.
    MUST NOT FIRE: a row with fewer deviations ranks above whatever it costs."""
    pairs = ["badge_access", "library_holds", "rate_limits"]
    reg = _figures_reg(["cheap", "dear"])
    cells = [_scored("cheap", p, usd=0.01) for p in pairs]
    cells += [_scored("dear", p, usd=0.5) for p in pairs]
    order = lineup_figures.rows(reg, cells)["S1"]["order"]
    check(order["survivors"] == ["cheap", "dear"] and order["ranks"] == {"cheap": 1, "dear": 2}
          and not order["shared_ranks"], f"list against list breaks on dollars: {order}")
    reg = _figures_reg(["cheap", "dear", "sub"])
    reg["rows"][2]["route"] = {"kind": "claude", "profile": "subscription"}
    cells += [_scored("sub", p, usd=0.001) for p in pairs]
    order = lineup_figures.rows(reg, cells)["S1"]["order"]
    check(order["ranks"] == {"cheap": 1, "dear": 1, "sub": 1} and order["shared_ranks"] == [1],
          f"a tie holding an API-equivalent is shared: {order}")
    cells = [c for c in cells if c["row"] != "sub"] + [_scored("sub", p, usd=0.001, dev=1)
                                                      for p in pairs]
    order = lineup_figures.rows(reg, cells)["S1"]["order"]
    check(order["survivors"][0] == "sub" and order["ranks"]["sub"] == 1
          and order["ranks"]["cheap"] == 2 and order["ranks"]["dear"] == 3,
          f"MUST NOT FIRE: fewer deviations rank first: {order}")


def test_684_n8_the_subscriptions_blank_is_the_platforms() -> None:
    """Fix 8. MUST FIRE: the CLI's blank `result` on a merge is `platform`, excluded
    and retried, and counted when the retry answers. MUST NOT FIRE: never a
    `model_failure`."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        reg = small_registration(pin, clone, claude=fake_claude(run_dir, {
            "claude-haiku-4-5-20251001": {"empty_result_once_on": ["Badge Access"]}}),
            rows=[claude_row("h", "claude-haiku-4-5-20251001")])
        ctx = context(write_run(reg, run_dir))
        code = run_lineup.LaneRun(ctx, "subscription").run()
        got = states(ctx)
    check(got == {"h|S1|badge_access|d1": ["platform", "ok"]} and code == 0,
          f"the CLI's blank is retried as the platform's, then counted: {code} {got}")


def test_684_n9_the_subscription_sleeps_to_a_parsed_reset() -> None:
    """N25. `parse_reset` reads the CLI's forms. MUST FIRE: a limit that names its
    reset sleeps the lane until it (plus the margin) and re-runs the cell. MUST NOT
    FIRE: a reset further off than the registered cap stops the lane (exit 4)."""
    now = run_lineup.datetime(2026, 9, 28, 10, 0, tzinfo=run_lineup.timezone.utc)
    for text, want in (
            ("You've hit your limit · resets 3pm (Europe/Berlin)", "2026-09-28T13:00:00+00:00"),
            ("5-hour limit reached ∙ resets 11am (UTC)", "2026-09-28T11:00:00+00:00"),
            ("Weekly limit reached ∙ resets Oct 1, 9am (UTC)", "2026-10-01T09:00:00+00:00"),
            ("resets 9am (UTC)", "2026-09-29T09:00:00+00:00"),
            ("Claude AI usage limit reached|1759327200", "2025-10-01T14:00:00+00:00"),
            ("Claude usage limit reached.", None)):
        got = run_lineup.parse_reset(text, now)
        check((got.isoformat() if got else None) == want,
              f"parse_reset({text!r}): {got}, expected {want}")
    clone, pin = shared_clone()
    for cap, want_code, want_states in ((86400.0, 0, ["usage_limit", "ok"]),
                                        (60.0, run_lineup.EXIT_USAGE_LIMIT, ["usage_limit"])):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            run_dir = Path(tmp)
            reg = small_registration(pin, clone, claude=fake_claude(run_dir, {
                "claude-sonnet-5": {"usage_limit_at": 1,
                                    "limit_text": "You've hit your limit · resets 3pm (UTC)"}}),
                rows=[claude_row("s", "claude-sonnet-5")],
                retry={"passes": 1, "spacing_seconds": 0, "breaker": 5,
                       "usage_limit_max_sleep_seconds": cap})
            ctx = context(write_run(reg, run_dir))
            slept = []
            ctx.sleep = slept.append
            ctx.clock = lambda: run_lineup.datetime(2026, 9, 28, 14, 0,
                                                    tzinfo=run_lineup.timezone.utc)
            code = run_lineup.LaneRun(ctx, "subscription").run()
            got = states(ctx)["s|S1|badge_access|d1"]
            events = [r for r in ctx.journal.read() if r.get("event") == "usage_limit_sleep"]
        if want_code == 0:
            check(code == 0 and got == want_states
                  and slept[:1] == [3600.0 + run_lineup.USAGE_LIMIT_MARGIN] and events,
                  f"the lane sleeps to the reset and goes on: {code} {got} {slept} {events}")
        else:
            check(code == want_code and got == want_states and not events,
                  f"MUST NOT FIRE: a reset past the cap stops the lane: {code} {got} {slept}")


def test_684_n10_a_self_hosted_lane_is_capped_in_gpu_seconds() -> None:
    """N24. MUST FIRE: a GPU-seconds cap below the first cell's estimate times the
    margin stops the lane before any call; a cap one measured cell nearly exhausts
    stops the second. MUST NOT FIRE: a cap with room runs every cell; the
    registration refuses a capped lane whose row has no seconds estimate."""
    clone, pin = shared_clone()
    for cap, want_code, want_cells in ((5.0, run_lineup.EXIT_GATED, 0),
                                       (12.55, run_lineup.EXIT_GATED, 1),
                                       (10000.0, run_lineup.EXIT_DONE, 2)):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            run_dir = Path(tmp)
            with endpoint({}, run_dir / "fakes" / "http.json") as (fake, url):
                row = http_row("q", "Qwen/Qwen3.8-27B-FP8", url, vendor="serverless",
                               metered=False, unpriced="self-hosted", lane="serverless",
                               field_order="any", cell_estimate_seconds=10)
                reg = small_registration(pin, clone, rows=[row],
                                         items=("badge_access", "library_holds"),
                                         lanes={"serverless": {"gpu_seconds": cap}})
                ctx = context(write_run(reg, run_dir))
                code = run_lineup.LaneRun(ctx, "serverless").run()
                ran = sum(len(v) for v in states(ctx).values())
                gated = [r for r in ctx.journal.read() if r.get("event") == "gated"]
            check(code == want_code and ran == want_cells,
                  f"GPU cap {cap}s: exit {code} after {ran} cell(s), expected {want_code} "
                  f"after {want_cells}")
            if want_code == run_lineup.EXIT_GATED:
                check(gated and gated[-1]["unit"] == "s" and gated[-1]["need"] > gated[-1]["left"],
                      f"GPU cap {cap}s: the gate records seconds: {gated}")
    bad = small_registration(pin, clone, rows=[http_row("q", "Qwen/Qwen3.8-27B-FP8", "http://x/v1",
                                                        vendor="serverless", metered=False,
                                                        unpriced="self-hosted",
                                                        lane="serverless")],
                             lanes={"serverless": {"gpu_seconds": 100}})
    check(any("cell_estimate_seconds" in p for p in run_lineup.validate(bad)),
          "a capped lane's row needs a seconds estimate")


def test_684_n11_a_torn_journal_tail_is_quarantined_and_the_run_goes_on() -> None:
    """N22. MUST FIRE: a last line cut short moves to a side file with an event and a
    warning; the lane then resumes, closing the dangling attempt as `interrupted`.
    MUST NOT FIRE: a clean journal is untouched; a bad line that is not the last is
    still refused as an edit."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        with endpoint({}, run_dir / "fakes" / "http.json") as (_fake, url):
            reg = small_registration(pin, clone, items=("badge_access", "library_holds"),
                                     rows=[http_row("a", "claude-opus-5-5", url)])
            ctx = context(write_run(reg, run_dir))
            run_lineup.LaneRun(ctx, "api", max_cells=1).run()
            path = ctx.journal.path
            clean = path.read_bytes()
            ctx.journal.read()
            check(path.read_bytes() == clean, "MUST NOT FIRE: a clean journal is untouched")
            begin = {"type": "begin", "cell": "a|S1|library_holds|d1", "row": "a", "set": "S1",
                     "item": "library_holds", "draw": 1, "attempt": 1, "lane": "api",
                     "kind": "cell", "vendor": "anthropic", "metered": True,
                     "model": "claude-opus-5-5", "dir": "cells/a/S1/library_holds/d1/a1",
                     "projection_usd": 0.5}
            end = json.dumps({"type": "end", "cell": "a|S1|library_holds|d1", "state": "ok"})
            path.write_bytes(clean + (json.dumps(begin) + "\n").encode() + end[:40].encode())
            records = ctx.journal.read()
            side = list(run_dir.glob("cells.jsonl.torn-*"))
            check(side and side[0].read_bytes() == end[:40].encode()
                  and records[-1].get("event") == "torn_tail_quarantined",
                  f"the torn tail is moved aside with an event: {side} {records[-1]}")
            code = run_lineup.LaneRun(ctx, "api").run()
            got = states(ctx)
            check(code == 0 and got.get("a|S1|library_holds|d1") == ["interrupted", "ok"],
                  f"the run goes on and re-runs the torn attempt: {code} {got}")
            # An append meets a torn tail too, and never glues its record onto it.
            before = path.read_bytes()
            path.write_bytes(before + b'{"type": "end", "ce')
            ctx.journal.append({"type": "event", "event": "note", "text": "after a tear"})
            tail = ctx.journal.read()[-2:]
            check([r.get("event") for r in tail] == ["torn_tail_quarantined", "note"]
                  and len(list(run_dir.glob("cells.jsonl.torn-*"))) == 2,
                  f"an append quarantines the tail before writing: {tail}")
            lines = path.read_bytes().split(b"\n")
            lines[1] = lines[1][:30]
            path.write_bytes(b"\n".join(lines))
            try:
                ctx.journal.read()
                failures.append("a bad line that is not the last must still be refused")
            except run_lineup.Refusal as exc:
                check(":2 is not JSON" in exc.message, f"wrong refusal: {exc.message}")


def test_684_n11_a_completed_run_with_an_unruled_call_is_counted() -> None:
    """N6. MUST FIRE: a verify call blanked by the vendor's filter and answered on the
    re-ask leaves a completed merge `ok`, its unruled call counted beside it (end
    record, scored cell, figures). MUST NOT FIRE: the same row without the blank
    carries no unruled call."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        behaviour = {"gpt-6-sol": {"refusal_blank_once_on": ["Front Desk Procedure"]}}
        with endpoint(behaviour, run_dir / "fakes" / "http.json") as (_fake, url):
            reg = small_registration(pin, clone, rows=[
                http_row("sol", "gpt-6-sol", url, vendor="openai"),
                http_row("luna", "gpt-6-luna", url, vendor="openai")])
            ctx = context(write_run(reg, run_dir))
            code = run_lineup.LaneRun(ctx, "api").run()
            ends_ = {r["row"]: r for r in ctx.journal.read() if r.get("type") == "end"}
        check(code == 0 and ends_["sol"]["state"] == "ok"
              and ends_["sol"].get("unruled_calls") == {"blank_refusal": 1},
              f"a completed run is ok, its unruled call counted: {code} {ends_['sol']}")
        check(ends_["luna"]["state"] == "ok" and "unruled_calls" not in ends_["luna"],
              f"MUST NOT FIRE: a clean run carries none: {ends_['luna']}")
        formed = lineup_figures.rows(reg, lineup_figures.score(run_dir))["S1"]
        check(formed["rows"]["sol"]["unruled_calls"] == 1 and formed["rows"]["sol"]["pairs"] == 1,
              f"the figures count it and score the cell: {formed['rows']['sol']}")


def test_684_n11_a_headline_row_that_completed_nothing_is_still_listed() -> None:
    """N9. MUST FIRE: a row whose every pair is its own exit 2 is in figures.md, with
    why. MUST NOT FIRE: it shrinks nobody's pairs."""
    reg = _figures_reg(["good", "refuser"])
    pairs = ["badge_access", "library_holds", "rate_limits"]
    cells = [_scored("good", p) for p in pairs] + [
        _scored("refuser", p, state="model_failure") for p in pairs]
    formed = lineup_figures.rows(reg, cells)
    text = lineup_figures.render(reg, json.loads(json.dumps(formed)))
    check("| refuser | 0 of 3 |" in text and "exit 2 on 3 of 3" in text,
          "a row that completed nothing must be listed, with why")
    check(formed["S1"]["common_pairs"] == pairs and formed["S1"]["order"]["survivors"] == ["good"],
          f"MUST NOT FIRE: it shrinks nothing: {formed['S1']['common_pairs']}")


def test_684_n12_the_pods_address_never_reaches_an_evidence_file() -> None:
    """N27. A serverless row whose address comes from its `base_url_env`, with a
    platform failure so the address reaches the tool's own error texts. MUST NOT
    FIRE: after the lane, no file under the run directory (cells, journal, run.json)
    and no line the lane printed holds the endpoint's host. MUST FIRE: with the
    redaction switched off, the same scan finds it."""
    clone, pin = shared_clone()
    for redact in (True, False):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            run_dir = Path(tmp)
            # The source decomposes fail on the platform after the merge answered,
            # so the tool writes a report whose errored step names the host.
            behaviour = {"Qwen/Qwen3.8-27B-FP8": {"platform_on": {
                "Extract every independently checkable": 3}}}
            with endpoint(behaviour, run_dir / "fakes" / "http.json") as (_fake, url):
                os.environ["LINEUP_TEST_POD_URL"] = url
                try:
                    row = http_row("q", "Qwen/Qwen3.8-27B-FP8", "unused", vendor="serverless",
                                   metered=False, unpriced="self-hosted", lane="serverless",
                                   field_order="any")
                    row["route"] = {"kind": "http", "base_url_env": "LINEUP_TEST_POD_URL",
                                    "key_env": KEY, "profile": "openai-compatible"}
                    reg = small_registration(pin, clone, rows=[row],
                                             lanes={"serverless": {}})
                    ctx = context(write_run(reg, run_dir))
                    if not redact:
                        ctx.redactor = run_lineup.Redactor()
                        ctx.journal.redact = ctx.redactor.obj
                    printed = []
                    ctx.out = printed.append
                    code = run_lineup.LaneRun(ctx, "serverless").run()
                finally:
                    os.environ.pop("LINEUP_TEST_POD_URL", None)
                host = url.split("://", 1)[1].split("/", 1)[0]
                # The host, and the tool's own key for a loopback endpoint (its
                # capability record keys an endpoint by its resolved address).
                needles = (host.split(":")[0], f"loopback:{host.split(':')[1]}")
                leaked = sorted(str(f.relative_to(run_dir)) for f in run_dir.rglob("*")
                                if f.is_file() and f.relative_to(run_dir).parts[0] != "fakes"
                                and any(n.encode() in f.read_bytes() for n in needles))
                said = [line for line in printed if any(n in line for n in needles)]
                got = states(ctx)
        if redact:
            check(code == 0 and got == {"q|S1|badge_access|d1": ["platform", "ok"]},
                  f"the lane ran, the address in its errors: {code} {got}")
            check(not leaked and not said,
                  f"MUST NOT FIRE: the pod's host reached {leaked[:6]} {said[:2]}")
        else:
            check(any(name.endswith(("argv.json", "stderr.log")) for name in leaked)
                  and any(name.endswith("report.json") for name in leaked)
                  and "cells.jsonl" in leaked
                  and any(name.endswith("capabilities.json") for name in leaked),
                  f"with no redaction the scan must find the host: {leaked[:6]}")


def test_684_the_registration_refuses_an_unknown_rule() -> None:
    """MUST FIRE: a rule value other than the fixed one. MUST NOT FIRE: the
    template's own rules block, which states it."""
    clone, pin = shared_clone()
    ok = small_registration(pin, clone, rows=[http_row("a", "claude-opus-5-5", "http://x/v1")])
    check(ok["rules"] == run_lineup.RULE_DEFAULTS and run_lineup.validate(ok) == [],
          f"MUST NOT FIRE: {ok.get('rules')} {run_lineup.validate(ok)}")
    bad = copy.deepcopy(ok)
    bad["rules"]["refusal_counts"] = "platform"
    check(any("rules.refusal_counts" in p for p in run_lineup.validate(bad)),
          "an unknown rule value must be refused")


# --- 12. the operator's rulings of 2026-09-28, each seeded both ways --------

def _journal_ends(ctx, cell_id: str) -> list[dict]:
    return run_lineup.ends(ctx.journal.read()).get(cell_id, [])


def test_688_a_failing_endpoint_with_a_working_reference_is_the_rows_own() -> None:
    """The reference-endpoint check. MUST FIRE: opus's library_holds fails on the platform on every
    pass; one reference cell on another vendor answers; the cell becomes opus's own
    `endpoint_failure`, flagged, counted against opus and shrinking nobody. MUST NOT
    FIRE: luna, clean, gets no reference check and ranks first on both pairs; the lane
    completes."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        behaviour = {"claude-opus-5-5": {"platform_on": {"Hold Shelf Management": 99}}}
        with endpoint(behaviour, run_dir / "fakes" / "http.json") as (_fake, url):
            reg = small_registration(pin, clone, items=("badge_access", "library_holds"),
                                     reference_url=url,
                                     rows=[http_row("opus", "claude-opus-5-5", url),
                                           http_row("luna", "gpt-6-luna", url,
                                                    vendor="openai")])
            ctx = context(write_run(reg, run_dir))
            code = run_lineup.LaneRun(ctx, "api").run()
            got = states(ctx)
            checks = [r for r in ctx.journal.read() if r.get("event") == "reference_check"]
            last = _journal_ends(ctx, "opus|S1|library_holds|d1")[-1]
        formed = lineup_figures.rows(reg, lineup_figures.score(run_dir))["S1"]
    check(got.get("opus|S1|library_holds|d1") == ["platform", "platform", "endpoint_failure"]
          and last.get("flag") == run_lineup.ENDPOINT_FLAG and last.get("verdict"),
          f"the endpoint's failure is the row's, flagged: {got} {last}")
    check(len(checks) == 1 and checks[0]["row"] == "opus" and checks[0]["verdict"] == "ok"
          and checks[0]["reference"] == "ref-openai",
          f"one reference check, on the other vendor: {checks}")
    check(formed["common_pairs"] == ["badge_access", "library_holds"]
          and formed["rows"]["opus"]["incomplete_text"]
          == "endpoint failed while reference worked on 1 of 2"
          and formed["order"]["survivors"] == ["luna"],
          f"counted against opus, shrinking nobody: {formed['order']} "
          f"{formed['rows']['opus']['incomplete_text']}")
    check(code == 0 and got.get("luna|S1|library_holds|d1") == ["ok"],
          f"MUST NOT FIRE: the clean row, and the lane completes: {code} {got}")


def _clean_cost(clone, pin, row_args, item="badge_access"):
    """The same cell run once with nothing going wrong: (charged, figures usd, seconds)."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        with endpoint({}, run_dir / "fakes" / "http.json") as (_fake, url):
            reg = small_registration(pin, clone, items=(item,), reference_url=url,
                                     rows=[http_row(*row_args[:2], url, **row_args[2])])
            ctx = context(write_run(reg, run_dir))
            run_lineup.LaneRun(ctx, "api").run()
            charged = sum(r["charged_usd"] for r in ctx.journal.read()
                          if r.get("type") == "end" and r.get("kind") == "cell")
        scored = lineup_figures.score(run_dir)[0]
    return charged, scored["usd"], scored


def test_688_the_network_dies_mid_cell_and_comes_back() -> None:
    """Outage handling: pause-and-resume, plus reusing what already ran. The network goes down after the merge and one
    decompose answered. MUST FIRE: the cell fails, its retry pass reuses the two answers
    it already has, the reference fails too (`infrastructure`, never scored), the lane
    writes OPERATOR-ATTENTION.txt, pauses and probes, resumes on its own when the probe
    answers, and completes the cell reusing the two calls: charged in all exactly what one
    clean run is charged, its figure the clean run's dollars. MUST NOT FIRE: nothing is
    scored as the model's, and the reference cell is never counted."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        state = run_dir / "fakes" / "http.json"
        with endpoint({}, state) as (_fake, url):
            reg = small_registration(pin, clone, reference_url=url,
                                     retry={"passes": 1, "spacing_seconds": 0, "breaker": 5},
                                     rows=[http_row("opus", "claude-opus-5-5", url)])
            ctx = context(write_run(reg, run_dir))
            probes = []

            def probe(_ctx, urls):
                probes.append(list(urls))
                if len(probes) >= 2:
                    lineup_fakes.restore(state)
                    return True
                return False
            ctx.probe = probe
            printed = []
            ctx.out = printed.append
            lineup_fakes.schedule_outage(state, after_calls=2)
            code = run_lineup.LaneRun(ctx, "api").run()
            attempts = _journal_ends(ctx, "opus|S1|badge_access|d1")
            events = [r for r in ctx.journal.read() if r.get("event") == "infrastructure_pause"]
            charged = sum(r["charged_usd"] for r in ctx.journal.read()
                          if r.get("type") == "end" and r.get("kind") == "cell")
            reference_charged = [r for r in ctx.journal.read() if r.get("type") == "end"
                                 and r.get("kind") == "reference"]
            attention = (run_dir / "OPERATOR-ATTENTION.txt").read_text() \
                if (run_dir / "OPERATOR-ATTENTION.txt").is_file() else ""
            final_dir = run_dir / attempts[-1]["dir"]
            reuse = json.loads((final_dir / "reuse.json").read_text())
        scored = lineup_figures.score(run_dir)
    clean_charged, clean_usd, clean = _clean_cost(clone, pin, ("opus", "claude-opus-5-5", {}))
    check([a["state"] for a in attempts] == ["platform", "platform", "infrastructure", "ok"],
          f"platform, a pass, infrastructure, then ok after the pause: "
          f"{[a['state'] for a in attempts]}")
    check(attempts[1].get("reused_calls") == 2 and attempts[-1].get("reused_calls") == 2
          and reuse["served"] == 2 and reuse["from_attempts"] == [1],
          f"both retries reuse the two answers the first attempt got: "
          f"{[a.get('reused_calls') for a in attempts]} {reuse}")
    check(code == 0 and len(probes) == 2 and events and events[-1]["resumed"] is True
          and "infrastructure" in attention and "resumes" in attention
          and any("OPERATOR ATTENTION" in line for line in printed),
          f"the lane paused, probed twice and resumed on its own: {code} {probes} {events}")
    check(abs(charged - clean_charged) < 1e-9,
          f"the cost is counted once: charged {charged} in all, a clean run {clean_charged}")
    check(abs(scored[0]["usd"] - clean_usd) < 1e-9 and scored[0]["reused_calls"] == 2
          and scored[0]["seconds"] >= clean["seconds"] * 0 and scored[0]["state"] == "ok",
          f"the figure is the clean run's dollars, the reuse counted: {scored[0]} {clean_usd}")
    check(len(reference_charged) == 1 and reference_charged[0]["state"] != "ok"
          and all(c["cell"] != reference_charged[0]["cell"] for c in scored),
          f"MUST NOT FIRE: the reference cell is recorded and never scored: {reference_charged}")


def test_688_an_outage_between_cells_leaves_finished_cells_untouched() -> None:
    """Outage handling: a finished cell stays untouched. MUST NOT FIRE: a cell finished before the outage is never
    re-run and its record never changes; the journal before the outage is a prefix of the
    journal after. MUST FIRE: the breaker asks the reference, which fails too, so the lane
    pauses instead of stopping, and every cell the outage hit is run again and counted."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        state = run_dir / "fakes" / "http.json"
        items = ("badge_access", "library_holds", "loading_dock", "freezer_alarm")
        with endpoint({}, state) as (_fake, url):
            reg = small_registration(pin, clone, items=items, reference_url=url,
                                     retry={"passes": 1, "spacing_seconds": 0, "breaker": 2},
                                     rows=[http_row("opus", "claude-opus-5-5", url)])
            ctx = context(write_run(reg, run_dir))
            first = run_lineup.LaneRun(ctx, "api", max_cells=1).run()
            before = ctx.journal.path.read_bytes()
            finished = _journal_ends(ctx, "opus|S1|badge_access|d1")

            def probe(_ctx, _urls):
                lineup_fakes.restore(state)
                return True
            ctx.probe = probe
            lineup_fakes.schedule_outage(state, after_calls=0)
            code = run_lineup.LaneRun(ctx, "api").run()
            after = ctx.journal.path.read_bytes()
            got = states(ctx)
            pauses = [r for r in ctx.journal.read() if r.get("event") == "infrastructure_pause"]
            still = _journal_ends(ctx, "opus|S1|badge_access|d1")
    check(first == 0 and [a["state"] for a in finished] == ["ok"], f"the first cell: {first}")
    check(after.startswith(before) and got["opus|S1|badge_access|d1"] == ["ok"]
          and still == finished,
          f"MUST NOT FIRE: the finished cell is untouched: {got['opus|S1|badge_access|d1']}")
    check(code == 0 and len(pauses) == 1 and pauses[0]["resumed"]
          and all(v[-1] == "ok" for v in got.values())
          and got["opus|S1|library_holds|d1"][0] == "platform",
          f"the breaker paused the lane, and every cell is counted in the end: {code} {got}")


def test_688_the_maximum_pause_stops_the_lane_and_run_continues() -> None:
    """Outage handling: the maximum pause stops the lane. MUST FIRE: with the network still down after the
    registered maximum pause, the lane stops as paused_infrastructure (exit 8), the cell
    `infrastructure`, never a model failure, and the operator is told. MUST NOT FIRE: a
    second `run` after the network is back continues from there and counts the cell."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        state = run_dir / "fakes" / "http.json"
        with endpoint({}, state) as (_fake, url):
            reg = small_registration(pin, clone, reference_url=url,
                                     retry={"passes": 0, "spacing_seconds": 0, "breaker": 5},
                                     infrastructure={"probe_urls": [url + "/models"],
                                                     "probe_intervals_seconds": [120],
                                                     "max_pause_seconds": 300},
                                     rows=[http_row("opus", "claude-opus-5-5", url)])
            ctx = context(write_run(reg, run_dir))
            slept = []
            ctx.sleep = slept.append
            ctx.probe = lambda _ctx, _urls: False
            lineup_fakes.schedule_outage(state, after_calls=0)
            first = run_lineup.LaneRun(ctx, "api").run()
            after_first = states(ctx)
            stopped = [r for r in ctx.journal.read() if r.get("event") == "paused_infrastructure"]
            attention = (run_dir / "OPERATOR-ATTENTION.txt").read_text()
            lineup_fakes.restore(state)
            ctx.probe = lambda _ctx, _urls: True
            second = run_lineup.LaneRun(ctx, "api").run()
            got = states(ctx)
    check(first == run_lineup.EXIT_PAUSED and slept == [120.0, 120.0] and stopped
          and after_first == {"opus|S1|badge_access|d1": ["platform", "infrastructure"]}
          and "paused_infrastructure" in attention,
          f"the maximum pause stops the lane as paused_infrastructure: {first} {slept} "
          f"{after_first}")
    check(second == 0 and got == {"opus|S1|badge_access|d1": ["platform", "infrastructure",
                                                               "ok"]},
          f"MUST NOT FIRE: the next run continues and counts the cell: {second} {got}")


def test_688_reuse_is_this_cells_own_and_a_stray_cache_hit_halts() -> None:
    """Outage handling: the never-pay-twice guard. MUST FIRE: a cache hit with nothing seeded (a
    request repeated inside one run) and a reused answer no earlier live call accounts
    for are runner assertions. MUST NOT FIRE: an earlier attempt of another draw, or one
    a runner assertion failed on, is never a source."""
    row = {"route": {"kind": "http"}, "model": "m"}
    hit = {"role": "merge", "source": "cache", "request_sha256": "x", "prompt_tokens": 10,
           "completion_tokens": 5, "model": "m"}
    report = {"provenance": {"ledger": [hit], "counts": {"cache_hits": 1}}}
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        journal = run_lineup.Journal(Path(tmp) / "cells.jsonl")
        cell = run_lineup.Cell("r", "S1", "badge_access", 1)
        _, problems = run_lineup.account_reuse(None, journal, row, cell, report, {}, [])
        check(any("repeated inside one run" in p for p in problems),
              f"a cache hit with nothing seeded is refused: {problems}")
        seeded = {"merge-x.json": {"attempt": 1, "role": "merge", "latency_ms": 5,
                                   "content": "{}"}}
        records = [{"type": "end", "cell": cell.id, "attempt": 1, "state": "platform",
                    "kind": "cell", "dir": "cells/r/a1"}]
        _, problems = run_lineup.account_reuse(None, journal, row, cell, report, seeded,
                                               records)
        check(not problems, f"a hit from an attempt a crash left without a report is "
                            f"counted at its kept latency: {problems}")
        other = [{"type": "end", "cell": "r|S1|badge_access|d2", "attempt": 1,
                  "state": "platform", "kind": "cell", "dir": "d2"},
                 {"type": "end", "cell": cell.id, "attempt": 1, "state": "halted",
                  "assertions_failed": True, "kind": "cell", "dir": "d1"},
                 {"type": "end", "cell": cell.id, "attempt": 2, "state": "infrastructure",
                  "verdict": True, "kind": "cell", "dir": "d1"}]
        check(run_lineup._reuse_sources(journal, other, cell) == [],
              "MUST NOT FIRE: another draw, an assertion halt and a verdict are no source")


def test_688_unruled_counts_against_the_row_with_its_cause() -> None:
    """MUST FIRE: a vendor row's ceiling cut is a model failure; a self-hosted
    row's cut at a ceiling below the model's output limit is `config`, at the model's own
    limit `limit`, at a served window below the model's context `config`, at the model's
    context `limit`, and with no numbers `config`. The figures list the row after every
    complete row with the flag, and figures.md shouts CONFIG."""
    vendor = {"hosting": "vendor", "window": 200000}
    self_row = {"hosting": "self", "window": 65536,
                "model_limits": {"context_tokens": 131072, "output_tokens": 32768,
                                 "source": "test"}}

    def rep(ledger=(), discards=()):
        return {"provenance": {"ledger": list(ledger), "discarded_calls": list(discards)}}
    cut = {"role": "verify", "outcome": "ceiling", "prompt_tokens": 9000,
           "completion_tokens": 900, "max_tokens": 900}
    ruled = run_lineup.unruled_ruling(vendor, rep([cut]), None)
    check(ruled["unruled_as"] == "model_failure"
          and ruled["flag"] == "model failure (unruled: ceiling cut)",
          f"a vendor row's cut is a model failure: {ruled}")
    for call, want in (
            (dict(cut), "config"),
            (dict(cut, completion_tokens=32768, max_tokens=32768), "limit"),
            ({"role": "verify", "kind": "blank_length", "prompt_tokens": 60000,
              "completion_tokens": 5536, "max_tokens": None}, "config"),
            ({"role": "verify", "kind": "blank_length", "prompt_tokens": 100000,
              "completion_tokens": 31072, "max_tokens": None}, "limit"),
            ({"role": "verify", "kind": "blank_length"}, "config")):
        report = rep([call]) if call.get("outcome") else rep(discards=[call])
        got = run_lineup.unruled_ruling(self_row, report, None)
        check(got["unruled_as"] == want, f"self-hosted {call}: {got['unruled_as']}, "
                                         f"expected {want}")
    reg = _figures_reg(["A", "Q"])
    pairs = ["badge_access", "library_holds", "rate_limits"]
    cells = [_scored("A", p) for p in pairs] + [_scored("Q", "badge_access"),
                                                _scored("Q", "library_holds")]
    q = _scored("Q", "rate_limits", state="unruled")
    q["excluded"] = "unruled_config"
    formed = lineup_figures.rows(reg, cells + [q])
    text = lineup_figures.render(reg, json.loads(json.dumps(formed)))
    check(formed["S1"]["rows"]["Q"]["incomplete_text"]
          == "CONFIG (self-hosted, the registration is wrong) on 1 of 3"
          and formed["S1"]["order"]["survivors"] == ["A"] and "\nCONFIG (688" in text,
          f"a config cell counts against the row, loudly: "
          f"{formed['S1']['rows']['Q']['incomplete_text']}")


def test_688_a_self_hosted_blank_on_length_writes_the_limits_stub() -> None:
    """End to end. MUST FIRE: the 27B's verify blank on length (no ceiling sent,
    far below its window) is `config`: the cell record says so, SELF-HOSTED-LIMITS.md lists
    it with its numbers, and the lane log says CONFIG. MUST NOT FIRE: the clean vendor row
    beside it carries no such flag and no stub line."""
    clone, pin = shared_clone()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        behaviour = {"Qwen/Qwen3.8-27B-FP8": {"blank_length_on": ["Badge Access"]}}
        with endpoint(behaviour, run_dir / "fakes" / "http.json") as (_fake, url):
            q = http_row("q", "Qwen/Qwen3.8-27B-FP8", url, vendor="serverless", metered=False,
                         unpriced="self-hosted", lane="api", field_order="any",
                         hosting="self", window=65536, timeout=2400,
                         model_limits={"context_tokens": 131072, "output_tokens": 32768,
                                       "source": "test"},
                         route={"kind": "http", "base_url": url, "key_env": KEY,
                                "profile": "openai-compatible"})
            reg = small_registration(pin, clone, reference_url=url,
                                     rows=[q, http_row("luna", "gpt-6-luna", url,
                                                       vendor="openai")])
            ctx = context(write_run(reg, run_dir))
            printed = []
            ctx.out = printed.append
            run_lineup.LaneRun(ctx, "api").run()
            ends_ = {r["row"]: r for r in ctx.journal.read() if r.get("type") == "end"}
            stub = (run_dir / "SELF-HOSTED-LIMITS.md").read_text() \
                if (run_dir / "SELF-HOSTED-LIMITS.md").is_file() else ""
    check(ends_["q"]["state"] == "unruled" and ends_["q"].get("unruled_as") == "config"
          and "q|S1|badge_access|d1" in stub and "CONFIG" in stub
          and any(line.startswith("CONFIG:") for line in printed),
          f"a self-hosted config cut is recorded, stubbed and shouted: {ends_['q']} "
          f"{stub[:200]}")
    check(ends_["luna"]["state"] == "ok" and "unruled_as" not in ends_["luna"]
          and "luna" not in stub, f"MUST NOT FIRE: the clean row: {ends_['luna']}")


def test_688_a_self_hosted_harness_timeout_is_config_never_the_model() -> None:
    """The 27B's live test (the row itself is dropped from the release lineup;
    this covers the generic self-hosted capability). MUST FIRE: on a self-hosted
    row, the tool's own timeout after the endpoint took the request, and the runner's
    cell wall limit, are `harness_timeout`: final, the row's CONFIG failure, counted
    against it and listed loudly, never `model_failure`, `unruled` or retried. MUST NOT
    FIRE: the same timeout on a vendor row is the platform's (retried); a connect
    timeout, where nothing was sent, is the platform's on either; a self-hosted row
    must register its own timeout."""
    from llossless import transport  # noqa: PLC0415
    self_row = {"route": {"kind": "http", "profile": "openai-compatible"}, "hosting": "self"}
    vendor_row = {"route": {"kind": "http", "profile": "anthropic"}, "hosting": "vendor"}
    sent = transport.timed_out("pod", 900, sent=True)
    unsent = transport.timed_out("pod", 900, sent=False)

    def report(exc):
        return {"exit_code": 2, "provenance": {"ledger": [{"role": "merge",
                                                           "outcome": "answer"}]},
                "steps": [{"name": "merge", "state": "errored",
                           "detail": f"{type(exc).__name__}: {exc}"}]}
    for row, exc, killed, want in ((self_row, sent, False, "harness_timeout"),
                                   (vendor_row, sent, False, "platform"),
                                   (self_row, unsent, False, "platform"),
                                   (self_row, None, True, "harness_timeout"),
                                   (vendor_row, None, True, "platform")):
        got, _ = run_lineup.classify(row, 2, report(exc) if exc else None, "", [], killed)
        check(got == want, f"{row['hosting']} {exc} killed={killed}: {got}, expected {want}")
    check("harness_timeout" in run_lineup.FINAL_STATES, "a harness timeout is final")
    clone, pin = shared_clone()
    bare = http_row("q", "Qwen/Qwen3.8-27B-FP8", "http://x/v1", vendor="serverless",
                    metered=False, unpriced="self-hosted", hosting="self",
                    model_limits={"context_tokens": 1, "output_tokens": 1, "source": "t"})
    check(any("q.timeout" in p for p in run_lineup.validate(
        small_registration(pin, clone, rows=[bare]))),
          "a self-hosted row without its own timeout is refused")
    reg = _figures_reg(["A", "Q"])
    pairs = ["badge_access", "library_holds", "rate_limits"]
    cells = [_scored("A", p) for p in pairs] + [_scored("Q", "badge_access"),
                                                _scored("Q", "library_holds"),
                                                _scored("Q", "rate_limits",
                                                        state="harness_timeout")]
    formed = lineup_figures.rows(reg, cells)
    text = lineup_figures.render(reg, json.loads(json.dumps(formed)))
    check(formed["S1"]["rows"]["Q"]["incomplete_text"]
          == "CONFIG (harness timeout, not the model) on 1 of 3"
          and formed["S1"]["common_pairs"] == pairs
          and "rate_limits d1 (harness timeout)" in text,
          f"counted against the row as CONFIG, loudly: "
          f"{formed['S1']['rows']['Q']['incomplete_text']}")


def test_688_haiku_gets_no_effort_and_keeps_its_default() -> None:
    """MUST FIRE: the registration refuses a Haiku command row with per-role
    levels and a non-Haiku row claiming one level. MUST NOT FIRE: a Haiku command row at
    `single_level` runs with no --effort on the tool's argv, its report records the tool's
    single-level label (not a level) and it is ok; an Opus row beside it still gets
    its three levels. The tool itself sends the CLI no --effort for Haiku
    either, recorded here so a regression is seen (what the CLI receives for Haiku)."""
    clone, pin = shared_clone()
    bad = small_registration(pin, clone, rows=[
        claude_row("h", "claude-haiku-4-5-20251001",
                   effort={role: "medium" for role in run_lineup.ROLES})])
    check(any("Haiku has one level" in p for p in run_lineup.validate(bad)),
          "a Haiku command row with levels is refused")
    bad = small_registration(pin, clone, rows=[claude_row("o", "claude-opus-5-5",
                                                          effort=run_lineup.SINGLE_LEVEL)])
    check(any("single_level" in p for p in run_lineup.validate(bad)),
          "a non-Haiku row may not claim one level")
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        run_dir = Path(tmp)
        reg = small_registration(pin, clone, claude=fake_claude(run_dir, {}), rows=[
            claude_row("h", "claude-haiku-4-5-20251001"), claude_row("o", "claude-opus-5-5")])
        ctx = context(write_run(reg, run_dir))
        code = run_lineup.LaneRun(ctx, "subscription").run()
        ends_ = {r["row"]: r for r in ctx.journal.read() if r.get("type") == "end"}
        argv = {rid: json.loads((run_dir / ends_[rid]["dir"] / "argv.json").read_text())
                for rid in ("h", "o")}
        report = json.loads((run_dir / ends_["h"]["dir"] / "report.json").read_text())
        sent = [c["argv"] for c in run_lineup.read_calls(run_dir / ends_["h"]["dir"] / "calls")]
    check(code == 0 and ends_["h"]["state"] == "ok" and "--effort" not in argv["h"]
          and argv["o"].count("--effort") == 3,
          f"Haiku runs with no --effort, Opus with three: {code} {ends_['h']['state']} "
          f"{argv['h'].count('--effort')} {argv['o'].count('--effort')}")
    decoding = report["provenance"]["decoding"]
    effort, single = decoding.get("effort"), decoding.get("effort_single_level")
    check(not effort and single and all(
              v == "one level (extended thinking on/off; default kept)"
              for v in single.values()),
          f"the report records one level, never a claimed level: {effort} {single}")
    levels = sorted({c[c.index("--effort") + 1] for c in sent if "--effort" in c})
    check(levels == [],
          f"what the CLI receives for Haiku: no --effort at all: {levels}")
    check(run_lineup.effort_label(reg["rows"][0])
          == "one level (extended thinking on/off; default kept)",
          "the label the registration and the figures print")


def test_run_lineup_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    checks = 0
    try:
        for name, function in sorted(globals().items()):
            if name.startswith("test_") and name != "test_run_lineup_offline" \
                    and callable(function):
                try:
                    function()
                except BaseException as exc:  # noqa: BLE001 - a crash (or a Refusal, a SystemExit) fails the check
                    import traceback
                    failures.append(f"{name} raised {type(exc).__name__}: {exc}\n"
                                    f"{traceback.format_exc()[-1500:]}")
                checks += 1
    finally:
        if "base" in _CLONE:
            shutil.rmtree(_CLONE["base"], ignore_errors=True)
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"run_lineup: {checks} checks pass -- the pin, the registration, the environment, "
          f"the label, classification and retry, resume, the caps, pre-warm, the pilot, "
          f"limits, the journal, redaction and the figures, each seeded both ways against "
          f"fakes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
