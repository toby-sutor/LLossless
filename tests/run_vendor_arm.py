#!/usr/bin/env python3
"""A reasoning arm, on a paid vendor. One variable moves: reasoning.

`tests/run_arm.py` drives the pod and cannot drive this: its `env()` requires
`HOSTED_OLLAMA_URL` and refuses anything else. Everything else about a draw is
copied from its `unit_argv` so the two records stay comparable - same pair, same
base, same fidelity, same title policy, same pinned tier.

The two states, and why neither of them is the default:

    off   LLOSSLESS_THINKING=""                    every call sends
                                                    reasoning_effort: "none"
    on    LLOSSLESS_THINKING="merge,decompose,verify"
                                                    no call sends the field

The bare default is `{"merge"}` (config.DEFAULT_THINKING), which is a third
state: merge reasons, the other two roles do not. An arm that simply omits
`--thinking` is not a thinking-off arm, and this file exists partly so that
mistake cannot be made silently again.

Both shapes are legal on this endpoint and neither is a provider branch: the
2026-08-31 request-shape probe put both on api.anthropic.com/v1 and both came
back 200. `build_body` is not touched.

What is asserted per draw, over the bytes `tests/vendor_arm_tee.py` caught:
temperature 0.0, the pinned json_schema rung with no `tools`, the model, the
endpoint, and the reasoning field present-and-"none" for off / absent for on.
An assertion failure fails the draw. A draw with no captured bodies fails too:
a capture that went empty looks exactly like a run that behaved.

Spend. The Ledger in `tests/spend.py` sits on calls this script makes itself,
and this script makes none - the CLI subprocess does. So the cap here is
enforced *between* draws, from each report's own measured usage, and within a
draw by `--max-calls`. Stated because it is weaker than the Ledger and a reader
should not assume otherwise.

Usage:
    python3 tests/run_vendor_arm.py --self-test
    python3 tests/run_vendor_arm.py --plan
    python3 tests/run_vendor_arm.py --run --out DIR
    python3 tests/run_vendor_arm.py --grade --out DIR
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import source_guard
import spend

ROOT = Path(__file__).resolve().parent.parent
import repo_paths  # noqa: E402
PAIR = ROOT / "tests" / "pairs" / "index_429"
TEE = ROOT / "tests" / "vendor_arm_tee.py"

MODEL = "claude-haiku-4-5-20251001"
SKU = f"anthropic/{MODEL}"
BASE_URL = "https://api.anthropic.com/v1"
ENDPOINT = f"{BASE_URL}/chat/completions"
PS_URL = "https://api.anthropic.com/api/ps"
KEY_ENV = "ANTHROPIC_API_KEY"

# K=3, pinned json_schema, --no-cache, temperature 0.0.
K = 3
FIDELITY = "high"
TIER = "json_schema"
MAX_CALLS = 14

# The reference run over this pair made 10 calls. 14 bounds a draw that goes
# wrong without cutting one that behaves; at haiku's rates a 14-call draw
# cannot reach $0.70 even if every call runs to a full window.
BUDGET = 2.50          # cumulative, checked before each draw is launched
PROJECTED = 1.07       # the projected cost, at a 2x on-arm output multiplier

ARMS = (
    ("H1-haiku-off", ""),
    ("H2-haiku-on", "merge,decompose,verify"),
)


def unit_argv(arm: str, thinking: str, draw: int, dest: Path) -> list[str]:
    """One draw's command line. The document arguments are the public pair."""
    return [sys.executable, str(TEE), str(dest / "bodies.jsonl"),
            "merge", str(PAIR / "source_a.md"), str(PAIR / "source_b.md"),
            "--base", str(PAIR / "source_a.md"),
            "--fidelity", FIDELITY, "--title-policy", "keep-base",
            "--model", MODEL, "--merge-model", MODEL,
            "--structured", TIER, "--no-cache",
            "--max-calls", str(MAX_CALLS), "--sample", str(draw),
            "--json", str(dest / "report.json"), "-o", str(dest / "merged.md")]


def env_for(thinking: str) -> dict:
    """The draw's environment. `thinking` is set explicitly in both states.

    Never left unset: an unset LLOSSLESS_THINKING is the `{"merge"}` default,
    which is neither arm.
    """
    key = os.environ.get(KEY_ENV)
    if not key:
        raise SystemExit(f"{KEY_ENV} is not set; the arm has no credential")
    env = dict(os.environ)
    env.update({
        "LLOSSLESS_THINKING": thinking,
        "LLOSSLESS_BASE_URL": BASE_URL,
        "LLOSSLESS_API_KEY": key,
        "LLOSSLESS_STRUCTURED": TIER,
        "PYTHONPATH": "src",
    })
    return env


# --- what the wire is allowed to have carried -------------------------------

def body_findings(arm: str, bodies: list[dict]) -> list[str]:
    """Every way a draw's captured bodies fail the held-constant conditions.

    Returns reasons, not a bool, so a failing draw says which condition broke.
    """
    out = []
    if not bodies:
        return ["no request bodies were captured, so nothing about this draw "
                "was observed"]
    thinking_on = arm.endswith("-on")
    if not any(rec.get("body") for rec in bodies):
        # The shape this draw actually died in, named rather than left as
        # "no bodies". `merge` asks the endpoint what window it serves before it
        # generates, on `/api/ps`, which exists on ollama and nowhere else. A
        # vendor 404s it and the 404 is fatal, so the run ends before its first
        # paid call. Nothing here can fix that: it is not the body, and it is
        # not `build_body`.
        got = sorted({rec.get("url") for rec in bodies})
        return [f"no request carried a body; the run reached only {got}, which "
                "is the served-window probe, and stopped there"]
    for n, rec in enumerate(bodies, 1):
        url, body = rec.get("url"), rec.get("body")
        if body is None:
            if n == 1 and url == PS_URL:
                # The served-window probe: expected, bodyless, and not a
                # generation. Reported by the no-bodies-at-all branch above
                # when it is all a draw produced; here, with later calls
                # present, it is the correct first step and not a finding.
                continue
            # A bodyless request anywhere else is not a generation and the
            # body clauses do not apply, but it is still a third party being
            # contacted, so it is reported rather than skipped in silence.
            out.append(f"call {n}: bodyless request to {url!r}")
            continue
        where = f"call {n}"
        if url != ENDPOINT:
            out.append(f"{where}: went to {url!r}, not {ENDPOINT!r}")
        # The whole commensurability argument is that the two
        # arms decoded identically, and temperature is the field that carries
        # it. Compared against the float, not against a string.
        if body.get("temperature") != 0.0:
            out.append(f"{where}: temperature is {body.get('temperature')!r}, "
                       "not 0.0")
        if body.get("model") != MODEL:
            out.append(f"{where}: model is {body.get('model')!r}")
        fmt = (body.get("response_format") or {}).get("type")
        if fmt != "json_schema":
            out.append(f"{where}: response_format is {fmt!r}, not the pinned "
                       "json_schema rung")
        if "tools" in body:
            out.append(f"{where}: carries `tools`, so this is the tool_call "
                       "rung wearing a json_schema label")
        effort = body.get("reasoning_effort", "\0absent")
        if thinking_on and effort != "\0absent":
            out.append(f"{where}: thinking-on carries reasoning_effort="
                       f"{effort!r}; the on state is the field's absence")
        if not thinking_on and effort != "none":
            out.append(f"{where}: thinking-off carries reasoning_effort="
                       f"{effort!r}, expected 'none'")
    return out


def read_bodies(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines()
            if ln.strip()]


def leaked_lines(bodies: list[dict], private: list[str]) -> list[str]:
    """Private lines found in what went out. Empty is the only passing value.

    A second gate behind `source_guard`, which checks the documents named on the
    argv. This checks the bytes, so a private document reaching a prompt by any
    other route - a cached fragment, a stray path, an edited fixture - is caught
    at the same place. Short lines are skipped: they are ordinary English and
    would fire on every run.
    """
    blob = json.dumps(bodies)
    return sorted({ln for ln in private if len(ln) >= 40 and ln in blob})


def private_lines() -> list[str]:
    """Every long line under assets/, if it is there. Numbers only ever leave."""
    assets = repo_paths.ASSETS
    if not assets.is_dir():
        return []
    out = set()
    for path in assets.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in (".md", ".txt"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        out.update(ln.strip() for ln in text.splitlines() if len(ln.strip()) >= 40)
    return sorted(out)


# --- spend ------------------------------------------------------------------

def draw_cost(report: dict) -> float:
    tokens = (report.get("provenance") or {}).get("tokens") or {}
    return spend.cost(SKU, input_tokens=tokens.get("input", 0),
                      output_tokens=tokens.get("output", 0))


def render_plan() -> str:
    off = spend.cost(SKU, input_tokens=28000, output_tokens=20000)
    lines = [f"pair            {PAIR.relative_to(ROOT)}",
             f"sku             {SKU}",
             f"endpoint        {ENDPOINT}",
             f"tier            {TIER} (pinned), --no-cache, temperature 0.0",
             f"draws           K={K} per arm, {len(ARMS)} arms, "
             f"--max-calls {MAX_CALLS}",
             ""]
    for arm, thinking in ARMS:
        state = "no reasoning field" if thinking else 'reasoning_effort: "none"'
        lines.append(f"  {arm:<14} LLOSSLESS_THINKING={thinking!r} -> {state}")
    lines += ["", "expected spend, from the 28k in / 20k out reference run:"]
    for mult in (1.0, 1.5, 2.0, 3.0):
        on = spend.cost(SKU, input_tokens=28000,
                        output_tokens=int(20000 * mult))
        lines.append(f"  on-arm output x{mult}   ${(off + on) * K:.2f}")
    lines.append(f"  stop-before-launch budget  ${BUDGET:.2f} cumulative")
    return "\n".join(lines)


# --- the run ----------------------------------------------------------------

def approve_pair() -> list[str]:
    """The pair, cleared by `source_guard`, which takes contents and not paths.

    Passing the paths refuses - an 81-byte path string hashes to nothing tracked
    - which is the module working as written and not a near miss: the question
    it answers is whether these bytes are committed, so it has to be given the
    bytes. Read from disk, deliberately, because disk is what the CLI will read
    a moment later; matching against HEAD is `source_guard`'s half of it.
    """
    return source_guard.approve([(PAIR / name).read_bytes()
                                 for name in ("source_a.md", "source_b.md")])


def run(out: Path) -> int:
    approved = approve_pair()
    private = private_lines()
    out.mkdir(parents=True, exist_ok=True)
    (out / "guard.json").write_text(json.dumps(
        {"approved": approved, "private_lines_scanned": len(private),
         "endpoint": ENDPOINT, "sku": SKU}, indent=1), encoding="utf-8")
    print(f"source_guard approved {approved}")
    print(f"leak scan armed with {len(private)} private lines\n")

    spent, failed = 0.0, 0
    for arm, thinking in ARMS:
        for draw in range(1, K + 1):
            if spent + PROJECTED / (len(ARMS) * K) > BUDGET:
                print(f"STOP: ${spent:.4f} spent, next draw would pass the "
                      f"${BUDGET:.2f} budget")
                return 1
            dest = out / f"{arm}-d{draw}"
            dest.mkdir(parents=True, exist_ok=True)
            argv = unit_argv(arm, thinking, draw, dest)
            (dest / "argv.json").write_text(json.dumps(argv, indent=1),
                                            encoding="utf-8")
            began = time.time()
            proc = subprocess.run(argv, cwd=ROOT, env=env_for(thinking),
                                  capture_output=True, text=True)
            (dest / "stdout.log").write_text(proc.stdout, encoding="utf-8")
            (dest / "stderr.log").write_text(proc.stderr, encoding="utf-8")
            bodies = read_bodies(dest / "bodies.jsonl")
            reasons = body_findings(arm, bodies)
            leaks = leaked_lines(bodies, private)
            if leaks:
                reasons.append(f"{len(leaks)} private line(s) reached the wire")
            cost = 0.0
            if (dest / "report.json").exists():
                cost = draw_cost(json.loads(
                    (dest / "report.json").read_text(encoding="utf-8")))
            spent += cost
            ok = proc.returncode == 0 and not reasons
            failed += not ok
            (dest / "draw.json").write_text(json.dumps(
                {"arm": arm, "draw": draw, "thinking": thinking,
                 "exit_code": proc.returncode, "calls_captured": len(bodies),
                 "body_findings": reasons, "leaked": len(leaks),
                 "cost_usd": round(cost, 6),
                 "seconds": round(time.time() - began, 1)}, indent=1),
                encoding="utf-8")
            mark = "ok " if ok else "BAD"
            print(f"{mark} {arm}-d{draw}  exit {proc.returncode}  "
                  f"{len(bodies)} bodies  ${cost:.4f}  "
                  f"{time.time() - began:.0f}s")
            for reason in reasons:
                print(f"      {reason}")
    print(f"\ntotal ${spent:.4f} over {len(ARMS) * K} draws, {failed} failed")
    return 1 if failed else 0


# --- self-test --------------------------------------------------------------

def self_test() -> int:
    failures = []

    def check(cond, why):
        print(("pass  " if cond else "FAIL  ") + why)
        if not cond:
            failures.append(why)

    check(len({t for _, t in ARMS}) == len(ARMS),
          "the two arms request different thinking sets")
    check("" in {t for _, t in ARMS},
          'the off arm is LLOSSLESS_THINKING="", not an unset variable')

    off, on = ARMS[0][0], ARMS[1][0]
    good = {"url": ENDPOINT, "body": {"temperature": 0.0, "model": MODEL,
            "response_format": {"type": "json_schema"},
            "reasoning_effort": "none"}}
    check(not body_findings(off, [good]), "a well-formed off body passes")
    on_body = {"url": ENDPOINT, "body": dict(good["body"])}
    on_body["body"].pop("reasoning_effort")
    check(not body_findings(on, [on_body]), "a well-formed on body passes")
    # Each must-fire is one mutation of a body that just passed, so a clause
    # that stopped discriminating cannot hide behind another one firing.
    for field, value, why in (
            ("temperature", 1.0, "temperature 1.0 fails"),
            ("temperature", "0.0", "temperature as a string fails"),
            ("model", "claude-sonnet-5", "the wrong model fails"),
            ("reasoning_effort", "low", "off with effort 'low' fails")):
        bad = {"url": ENDPOINT, "body": dict(good["body"]) | {field: value}}
        check(bool(body_findings(off, [bad])), why)
    check(bool(body_findings(off, [{"url": ENDPOINT,
          "body": dict(good["body"]) | {"tools": []}}])),
          "a body carrying `tools` fails the pinned-rung clause")
    check(bool(body_findings(off, [{"url": "https://api.openai.com/v1/chat/completions",
          "body": dict(good["body"])}])), "the wrong endpoint fails")
    check(bool(body_findings(on, [good])),
          "the on arm fails on a body that carries a reasoning field")
    check(bool(body_findings(off, [on_body])),
          "the off arm fails on a body with no reasoning field")
    check(bool(body_findings(off, [])),
          "an empty capture fails rather than passing vacuously")
    ps = [{"url": "https://api.anthropic.com/api/ps", "body": None}]
    check("served-window probe" in " ".join(body_findings(off, ps)),
          "a draw that reached only /api/ps is named as the window probe, not "
          "reported as an empty capture")
    check(not body_findings(off, ps + [good]),
          "the served-window probe ahead of a well-formed body is the "
          "successful shape, not a finding")
    late_ps = [good, {"url": PS_URL, "body": None}]
    check(any("bodyless" in r for r in body_findings(off, late_ps)),
          "a bodyless request that is not the leading probe is still reported")

    # `source_guard` is given contents, not paths, and this is the clause that
    # says so: the path form is a must-fire, the real pair a must-not-fire.
    check(approve_pair() == ["tests/pairs/index_429/source_a.md",
                             "tests/pairs/index_429/source_b.md"],
          "source_guard clears the public pair by content")
    try:
        source_guard.approve([str(PAIR / "source_a.md")])
        check(False, "source_guard refuses a path where a document belongs")
    except source_guard.UnapprovedSource:
        check(True, "source_guard refuses a path where a document belongs")

    # The leak scan gets a seeded positive and a seeded negative, because a
    # scanner that has never fired is indistinguishable from a clean run.
    secret = "a private sentence that is comfortably over forty bytes long"
    check(leaked_lines([{"body": {"messages": [{"content": secret}]}}],
                       [secret]) == [secret], "the leak scan fires when seeded")
    check(leaked_lines([{"body": {"messages": [{"content": "alpha beta"}]}}],
                       [secret]) == [], "the leak scan is quiet on clean bodies")
    check(leaked_lines([{"body": {"messages": [{"content": "the tool"}]}}],
                       ["the tool"]) == [],
          "the leak scan ignores lines under 40 bytes")

    # The pin that matters: this file names a state by an env var and a shape.
    # If either moves in shipped code, the arms stop meaning what they say.
    cfg = (ROOT / "src" / "llossless" / "config.py").read_text(encoding="utf-8")
    # `DEFAULT_THINKING` is now empty, so the bare default is no longer a third
    # state: an unset variable now means what the off arm sets explicitly. What
    # this pin is for survives that -- neither arm may depend on the default --
    # so it points at the value that would break them rather than the old one.
    check("DEFAULT_THINKING: frozenset[str] = frozenset()" in cfg,
          "config.DEFAULT_THINKING is empty; if it gains a role again an "
          "unset variable becomes a third state and these two arms stop meaning "
          "what they say")
    st = (ROOT / "src" / "llossless" / "structured.py").read_text(encoding="utf-8")
    check('body["reasoning_effort"] = "none"' in st,
          "structured.build_body still writes reasoning_effort='none', which is "
          "the shape the off arm is asserted to have sent")
    client = (ROOT / "src" / "llossless" / "client.py").read_text(encoding="utf-8")
    check('f"{self.settings.base_url_for(role)}/chat/completions"' in client,
          "client.py still builds {base_url_for(role)}/chat/completions, so ENDPOINT is "
          "still the URL these draws reach")

    print(f"\n{len(failures)} failing" if failures else "\nall pass")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.plan:
        print(render_plan())
        return 0
    if args.run:
        if args.out is None:
            raise SystemExit("--run needs --out DIR")
        return run(args.out)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
