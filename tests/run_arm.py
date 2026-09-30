#!/usr/bin/env python3
"""One arm of the model-size trendline sweep, with the three guards that arm X needed.

This driver ran arms A, B, C and T from the scratchpad. It is in the repository
now for one reason: on 2026-08-23 a driver invocation carrying a plausible arm
label, `X`, passed every assertion the scratchpad copy had and started live GPU
work against a sweep that was already complete. Every assertion it passed was a
check on *shape* -- a seven-pair arm at 8b/40960 is well-formed -- and shape was
never the thing in question.

Three guards, cheapest first. Each is a pure function returning a refusal string
or `None`, so `tests/test_run_arm.py` can prove it refuses without a GPU. That
matters more than it looks: this sweep is finished, so nothing here will run
again in anger, and a guard whose only witness is a run that never happens is a
guard that passes by not being called.

  1. `live_calls_permitted`  Invert the default. No live call leaves this
     file unless `--record` is on the command line. A bare invocation renders
     prompts and counts calls with the CLI's `--dry-run`. An accident then has
     to include the word `--record` to reach the network, and `--record` is not
     a word anybody types by accident.

  2. `guard_known_arm`  Close the label. `ARMS` pins the model, the served
     window and the plan for each of A, B, C and T, so `X` is rejected by name
     rather than by coincidence, and an arm cannot silently change model or
     window between two invocations of itself.

  3. `guard_settled_arm`  Refuse to overwrite a settled arm. The predicate is
     the terminal sentinel or **any unit artifact on disk** -- deliberately not
     `arms/<label>/journal.jsonl`. Arm A's journal carries 26 rows
     over 28 unit artifacts, because a restart skips a finished unit and a
     skipped unit appends nothing. The journal is a log, not a census, and a
     guard keyed to it would have waved through the one case it exists for.

`--mirror` is a fourth thing and not a guard: it verifies, on exit, that the
arm's record survived the run. "The run completed" and "the run was preserved"
are two assertions and neither is inferred from the other -- `mirror.sh` died
when arm T exited, and that was harmless only because the arm had already
finished. The path is verified, never chosen: no default can be right, because
the destination is a property of the machine and this file is published.

The terminal sentinel is the other half of (3). On exit -- including a crash --
`arms/<label>/sentinel.json` records the arm, the model, the window, how many
units were planned and how many settled, the exit status and a UTC timestamp.
A later session then reads arm state in one read instead of inferring it from
file mtimes, which is what this one had to do.

Usage:

    tests/run_arm.py C qwen3.8:27b --num-ctx 65536 --out DIR             dry run
    tests/run_arm.py C qwen3.8:27b --num-ctx 65536 --out DIR --record    live
    tests/run_arm.py T qwen3:8b    --num-ctx 40960 --out DIR --record    thinking
    tests/run_arm.py C qwen3.8:27b --num-ctx 65536 --out DIR --record \
        --mirror /elsewhere/claude-tmp/2026-08-23                with a mirror check

`--out` is required and is never inside this repository: the arm record corpus
lives outside the repository, and a default that wrote into
`tests/` would put 2.4 MB of model output one `git add -A` away from the
standing prohibition on `tests/responses/`.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# The sweep's corpus, written down rather than read off the disk. `tests/pairs/` used
# to be exactly these seven and this line used to be a directory listing; two
# more were added later, and a directory listing would have re-based the denominator
# every recorded arm was measured against -- the retroactive change that was
# refused when the attribution pairs were kept out of this directory. So the arms
# name their corpus, and a later pair joins it only by being added here.
M9_PAIRS = (
    "badge_access",
    "bike_docks",
    "freezer_alarm",
    "library_holds",
    "loading_dock",
    "payroll_cutoff",
    "rate_limits",
)
PAIRS = list(M9_PAIRS)
LEVELS = ("off", "high")

# A registration that names a fixture is only as good as the fixture. A pair
# renamed or removed would otherwise make every arm fail one unit at a time,
# deep inside a pod window, rather than here.
_missing = [p for p in M9_PAIRS if not (ROOT / "tests" / "pairs" / p).is_dir()]
assert not _missing, f"M9_PAIRS names {_missing}, which are not in tests/pairs/"

# Layer 2. Model and window are pinned per arm because they are two axes, not
# one: an arm that reloads at a different window is measuring size and context
# at the same time. `draws` is 3 for a size arm (the scored draw plus the two
# variance draws at `off`) and 1 for the thinking arm, which was registered as
# a single draw over the six common pairs.
ARMS: dict[str, dict] = {
    "A": {"model": "qwen3:4b", "num_ctx": 65536, "pairs": "all", "draws": 3, "thinking": ()},
    "B": {"model": "qwen3:8b", "num_ctx": 40960, "pairs": "all", "draws": 3, "thinking": ()},
    "C": {"model": "qwen3.8:27b", "num_ctx": 65536, "pairs": "all", "draws": 3, "thinking": ()},
    # `rate_limits` is out of capability at 40960 and thinking does not
    # change a window, so the pair is excluded rather than allowed to fail.
    "T": {"model": "qwen3:8b", "num_ctx": 40960, "pairs": "common6", "draws": 1,
          "thinking": ("merge",)},
}


# -- the three guards -------------------------------------------------------

def live_calls_permitted(argv: list[str]) -> bool:
    """Layer 1, as a predicate over the command that is actually about to run.

    Not a refusal: a bare invocation is not an error, it is a dry run. The
    guard is that this predicate and the `--record` flag must agree, checked in
    `run_unit` against the argv `subprocess.run` receives -- not against the
    intent that built it. `--dry-run` outranks every other mode in
    `Settings.mode` (config.py:287-296), so there is no flag ordering that
    reaches the network past it.
    """
    return "--dry-run" not in argv


def guard_known_arm(label: str, model: str, num_ctx: int) -> str | None:
    """Layer 2. The label is closed, and it carries its model and window with it."""
    if label not in ARMS:
        return (f"unknown arm {label!r}: this sweep has arms "
                f"{', '.join(sorted(ARMS))} and no others. An arm label is not a "
                f"free-form name; add it to ARMS with its model and window, "
                f"deliberately, or use one that exists.")
    want = ARMS[label]
    if model != want["model"]:
        return (f"arm {label} is {want['model']}, not {model!r}. Re-pointing a "
                f"settled label at another model re-keys every cassette it owns.")
    if num_ctx != want["num_ctx"]:
        return (f"arm {label} is served at {want['num_ctx']}, not {num_ctx}. Size "
                f"and window are two axes; an arm that moves both measures neither.")
    return None


def unit_artifacts(arm_dir: Path) -> list[Path]:
    """Every settled unit record under an arm directory, in a stable order.

    Deliberately not `journal.jsonl`. A restart skips a finished unit without
    appending a row, so the journal undercounts by exactly the units a resumed
    arm already holds -- the population layer 3 exists to protect.
    """
    return sorted(p for sub in ("off", "high", "var")
                  for p in (arm_dir / sub).glob("*.json"))


def guard_settled_arm(arm_dir: Path, record: bool, append: bool) -> str | None:
    """Layer 3. Recording over an arm that already has records needs `--append`."""
    if not record or append:
        return None
    sentinel = arm_dir / "sentinel.json"
    if sentinel.exists():
        try:
            state = json.loads(sentinel.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            state = {}
        return (f"arm {arm_dir.name} is already settled: {sentinel} reports "
                f"{state.get('units_settled', '?')} of {state.get('units_planned', '?')} "
                f"units at {state.get('finished_at', 'an unrecorded time')}. "
                f"Pass --append to add to it deliberately.")
    found = unit_artifacts(arm_dir)
    if found:
        return (f"arm {arm_dir.name} holds {len(found)} unit artifact(s) already, "
                f"first {found[0].relative_to(arm_dir)}, and no sentinel says how "
                f"that run ended. Pass --append to add to it deliberately.")
    return None


# -- the terminal sentinel --------------------------------------------------

def verify_mirror(arm_dir: Path, dest: Path) -> dict:
    """Compare an arm directory against its mirror, byte for byte.

    "The run completed" and "the run was preserved" are two assertions and
    neither may be inferred from the other. `mirror.sh` died when arm T exited
    and that was harmless only because the arm had already finished; had it died
    mid-arm the loss would have been silent, because a copy process that stops
    early stops printing too.

    This proves the mirror was complete **at the moment the arm ended**. It does
    not prove the mirror was live throughout, and a mirror that died and was
    re-run by hand passes here - correctly, because end-state completeness is
    the property that matters for a record corpus.
    """
    src = sorted(q.relative_to(arm_dir) for q in arm_dir.rglob("*") if q.is_file())
    got = sorted(q.relative_to(dest) for q in dest.rglob("*") if q.is_file()) \
        if dest.is_dir() else []
    missing = sorted(set(src) - set(got))
    differing = sorted(r for r in set(src) & set(got)
                       if (arm_dir / r).read_bytes() != (dest / r).read_bytes())
    extra = sorted(set(got) - set(src))
    return {
        "dest": str(dest),
        "source_files": len(src),
        "dest_files": len(got),
        "missing_total": len(missing),
        "missing": [str(r) for r in missing[:20]],
        "differing_total": len(differing),
        "differing": [str(r) for r in differing[:20]],
        "extra_total": len(extra),
        "verified": not missing and not differing,
    }



def write_sentinel(arm_dir: Path, label: str, spec: dict, planned: int,
                   status: str, exit_code: int, started_at: str,
                   observed: bool = True, note: str = "",
                   mirror: dict | None = None) -> Path:
    """Arm state in one file, so no later session has to read mtimes for it."""
    arm_dir.mkdir(parents=True, exist_ok=True)
    path = arm_dir / "sentinel.json"
    settled = unit_artifacts(arm_dir)
    payload = {
        "arm": label,
        "model": spec["model"],
        "num_ctx": spec["num_ctx"],
        "thinking": list(spec["thinking"]),
        "units_planned": planned,
        "units_settled": len(settled),
        "status": status,
        "exit_code": exit_code,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "observed": observed,
        # Separate from `status` on purpose. `status` says how the run ended;
        # this says whether the record survived it. Null means no mirror was
        # named, which is a third state and not a pass.
        "mirror": mirror,
    }
    if note:
        payload["note"] = note
    path.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    return path


# -- the plan ---------------------------------------------------------------

def plan_for(label: str) -> list[tuple[str, str, int]]:
    """(pair, fidelity, sample) for every unit the arm owes, asserted by count.

    The counts are the pre-registered denominators: 14 scored units plus 14
    variance draws for a size arm (as amended, and the 21-unit variance
    corpus), 12 for the thinking arm. Asserted here so a fixture
    appearing or vanishing stops the arm instead of quietly moving every
    denominator it feeds.
    """
    spec = ARMS[label]
    pairs = PAIRS if spec["pairs"] == "all" else [p for p in PAIRS if p != "rate_limits"]
    if spec["pairs"] == "all":
        assert len(pairs) == 7, pairs
        units = [(p, lv, 0) for p in pairs for lv in LEVELS]
        assert len(units) == 14, len(units)
        units += [(p, "off", s) for p in pairs for s in (1, 2)]
        assert len(units) == 28, len(units)
    else:
        assert len(pairs) == 6, pairs
        units = [(p, lv, 0) for p in pairs for lv in LEVELS]
        assert len(units) == 12, len(units)
    return units


def unit_argv(label: str, pair: str, level: str, sample: int, out: Path,
              record: bool) -> list[str]:
    """The CLI command for one unit. Pure, so layer 1 is testable offline.

    Layer 1 lives here rather than in a refusal: a bare invocation is not an
    error, it is a dry run. `--dry-run` outranks every other mode in
    `Settings.mode` (config.py:287-296), so appending it is sufficient -- there
    is no flag ordering that reaches the network past it.
    """
    spec = ARMS[label]
    sub = level if sample == 0 else "var"
    stem = pair if sample == 0 else f"{pair}.s{sample}"
    dest = out / "arms" / label / sub
    d = ROOT / "tests" / "pairs" / pair
    argv = [sys.executable, "-m", "llossless.cli", "merge",
            str(d / "source_a.md"), str(d / "source_b.md"),
            "--base", str(d / "source_a.md"),
            "--fidelity", level, "--title-policy", "keep-base",
            "--merge-model", spec["model"], "--model", spec["model"],
            "--sample", str(sample)]
    for role in spec["thinking"]:
        argv += ["--thinking", role]
    argv += ["--json", str(dest / f"{stem}.json"), "-o", str(dest / f"{stem}.md")]
    if not record:
        argv.append("--dry-run")
    return argv


# -- the endpoint -----------------------------------------------------------

def env(require_endpoint: bool = True) -> dict[str, str]:
    """Process environment for a unit, with the local endpoint refused.

    The address itself is read from an untracked `.env`; only the variable's
    name appears here. The local endpoint has a thermal limit that has shut the
    machine down, so an arm that quietly retargets it is worse than an arm that
    does not run.
    """
    e = dict(os.environ)
    dotenv = ROOT / ".env"
    if dotenv.exists():
        for line in dotenv.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                e[k.strip()] = v.strip().strip('"').strip("'")
    e["LLOSSLESS_STRUCTURED"] = "json_schema"
    e["PYTHONPATH"] = "src"
    if "HOSTED_OLLAMA_URL" not in e:
        if not require_endpoint:
            return e
        sys.exit("HOSTED_OLLAMA_URL is unset: the endpoint is an ephemeral pod and "
                 "its address moves on every restart, so it lives in the "
                 "environment and never in a tracked file.")
    e["LLOSSLESS_BASE_URL"] = e["HOSTED_OLLAMA_URL"].rstrip("/") + "/v1"
    if any(h in e["LLOSSLESS_BASE_URL"] for h in ("127.0.0.1", "localhost", "::1")):
        sys.exit(f"refusing the local endpoint: {e['LLOSSLESS_BASE_URL']}")
    return e


def ollama(path: str, payload: dict | None, e: dict[str, str]) -> dict:
    root = e["HOSTED_OLLAMA_URL"].rstrip("/")
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(f"{root}/{path}", data=data,
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "curl/8.0"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read() or b"{}")


def resident(model: str, e: dict[str, str]) -> dict | None:
    for m in ollama("api/ps", None, e).get("models", []):
        if m["name"] == model:
            return {"context_length": m.get("context_length"),
                    "size_vram_gb": round(m.get("size_vram", 0) / 2 ** 30, 2)}
    return None


def check_window(model: str, want: int, e: dict[str, str], where: str) -> None:
    """Refuse rather than report. A window that drifts mid-arm invalidates the arm."""
    res = resident(model, e)
    got = None if res is None else res.get("context_length")
    if got != want:
        sys.exit(f"context drift at {where}: /api/ps reports {got}, pinned {want}")


def clear_card(model: str, e: dict[str, str]) -> None:
    """Unload every other model, then prove it. 27B and 8B do not both fit."""
    for other in [m["name"] for m in ollama("api/ps", None, e).get("models", [])]:
        if other != model:
            print(f"unloading {other}", flush=True)
            ollama("api/generate", {"model": other, "keep_alive": 0}, e)
    for _ in range(30):
        still = [m["name"] for m in ollama("api/ps", None, e).get("models", [])
                 if m["name"] != model]
        if not still:
            return
        time.sleep(2)
    sys.exit(f"still resident after unload, refusing to co-load {model}: {still}")


# -- one unit ---------------------------------------------------------------

def run_unit(label: str, pair: str, level: str, sample: int, out: Path,
             record: bool, e: dict[str, str], journal: Path) -> dict | None:
    dest = out / "arms" / label / (level if sample == 0 else "var")
    dest.mkdir(parents=True, exist_ok=True)
    stem = pair if sample == 0 else f"{pair}.s{sample}"
    jpath = dest / f"{stem}.json"
    if jpath.exists():
        try:
            if "exit_code" in json.loads(jpath.read_text(encoding="utf-8")):
                print(f"  skip {label} {pair} {level} s{sample} (done)", flush=True)
                return None
        except json.JSONDecodeError:
            pass
    argv = unit_argv(label, pair, level, sample, out, record)
    # Layer 1, checked against the command rather than the intention behind it.
    assert live_calls_permitted(argv) == record, argv
    t0 = time.time()
    proc = subprocess.run(argv, cwd=ROOT, env=e, capture_output=True, text=True)
    rec = {"arm": label, "model": ARMS[label]["model"], "pair": pair,
           "fidelity": level, "sample": sample, "wall_s": round(time.time() - t0, 1),
           "returncode": proc.returncode, "live": record}
    if jpath.exists():
        r = json.loads(jpath.read_text(encoding="utf-8"))
        rec["exit_code"] = r["exit_code"]
        rec["counts"] = r["provenance"]["counts"]
        rec["duration_s"] = r["provenance"]["duration_seconds"]
        rec["steps"] = {s["name"].split(" tests/")[0].split(" /")[0]: s["state"]
                        for s in r["steps"]}
        rec["errored_steps"] = [s["name"] + ": " + s["detail"][:120]
                                for s in r["steps"] if s["state"] == "errored"]
        rec["findings"] = sorted(f["kind"] for f in r["structural"]["findings"])
    else:
        rec["exit_code"] = None
        rec["stderr"] = proc.stderr[-800:]
    with journal.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(f"  {label} {pair:15s} {level:4s} s{sample} {rec['wall_s']:7.1f}s "
          f"exit={rec['exit_code']} findings={rec.get('findings')}", flush=True)
    return rec


# -- entry point ------------------------------------------------------------

def parse(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("arm", help=f"one of {', '.join(sorted(ARMS))}")
    p.add_argument("model")
    p.add_argument("--num-ctx", type=int, required=True,
                   help="the served window, pinned at load and re-checked per unit")
    p.add_argument("--out", type=Path, required=True,
                   help="record root; never inside this repository")
    p.add_argument("--record", action="store_true",
                   help="permit live calls. Without it every unit is a --dry-run")
    p.add_argument("--append", action="store_true",
                   help="with --record, add to an arm that already holds records")
    p.add_argument("--mirror", type=Path, default=None,
                   help="mirror root to verify this arm against on exit. Laid out "
                        "like --out, so the arm is compared with "
                        "<mirror>/arms/<label>. Verified, never created and never "
                        "chosen: the destination is a property of the machine, not "
                        "of this repository, so no default can be correct here.")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse(argv)
    refusal = guard_known_arm(args.arm, args.model, args.num_ctx)
    if refusal:
        sys.exit(refusal)
    spec = ARMS[args.arm]
    out = args.out.resolve()
    if ROOT == out or ROOT in out.parents:
        sys.exit(f"--out {out} is inside the repository. Arm records live in "
                 f"claimcheck-run-artifacts/, not in tests/.")
    mirror_dir = None
    if args.mirror is not None:
        mirror_root = args.mirror.resolve()
        if ROOT == mirror_root or ROOT in mirror_root.parents:
            sys.exit(f"--mirror {mirror_root} is inside the repository. A mirror "
                     f"of the record corpus is not a tracked artefact.")
        mirror_dir = mirror_root / "arms" / args.arm

    arm_dir = out / "arms" / args.arm
    refusal = guard_settled_arm(arm_dir, args.record, args.append)
    if refusal:
        sys.exit(refusal)

    units = plan_for(args.arm)
    arm_dir.mkdir(parents=True, exist_ok=True)
    journal = arm_dir / "journal.jsonl"
    started_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    status, code = "crashed", 1
    try:
        e = env(require_endpoint=args.record)
        if args.record:
            clear_card(spec["model"], e)
            print(f"card clear, warming {spec['model']} at num_ctx {spec['num_ctx']}",
                  flush=True)
            ollama("api/generate", {"model": spec["model"], "prompt": "hi",
                                    "stream": False, "keep_alive": "6h",
                                    "options": {"num_predict": 1,
                                                "num_ctx": spec["num_ctx"]}}, e)
            check_window(spec["model"], spec["num_ctx"], e, "warm")
            (arm_dir / "resident.json").write_text(
                json.dumps(resident(spec["model"], e), indent=1) + "\n", encoding="utf-8")
        else:
            print(f"DRY RUN: arm {args.arm} plans {len(units)} units and will make "
                  f"no request. Pass --record to run it live.", flush=True)
        t0 = time.time()
        for pair, level, sample in units:
            run_unit(args.arm, pair, level, sample, out, args.record, e, journal)
            if args.record:
                check_window(spec["model"], spec["num_ctx"], e,
                             f"after {pair}/{level}/s{sample}")
        print(f"arm {args.arm} wall clock {round(time.time() - t0, 1)}s", flush=True)
        status, code = "complete", 0
    except SystemExit as exc:
        status = "refused"
        code = exc.code if isinstance(exc.code, int) else 1
        raise
    except KeyboardInterrupt:
        status, code = "interrupted", 130
        raise
    finally:
        # Only a recording run leaves a sentinel. A dry run that left one would
        # make layer 3 refuse the live run it was rehearsing, which is the one
        # workflow this driver is supposed to encourage.
        mirror = verify_mirror(arm_dir, mirror_dir) if mirror_dir else None
        if mirror is not None:
            print(f"mirror: {mirror['dest']} "
                  f"{mirror['dest_files']}/{mirror['source_files']} files, "
                  f"{mirror['missing_total']} missing, "
                  f"{mirror['differing_total']} differing -> "
                  f"{'VERIFIED' if mirror['verified'] else 'NOT PRESERVED'}",
                  flush=True)
        if args.record:
            path = write_sentinel(arm_dir, args.arm, spec, len(units),
                                  status, code, started_at, mirror=mirror)
            print(f"sentinel: {path} ({status}, "
                  f"{len(unit_artifacts(arm_dir))}/{len(units)} units)", flush=True)
        else:
            print(f"dry run: no sentinel written. Arm {args.arm} holds "
                  f"{len(unit_artifacts(arm_dir))} unit artifact(s) on disk.", flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
