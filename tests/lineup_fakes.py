#!/usr/bin/env python3
"""A fake model for the lineup runner, behind a loopback endpoint and a fake `claude`. No model call.

`tests/run_lineup.py` drives `python -m llossless` from a pinned clone, cell by
cell, and everything it asserts is read off what the tool wrote: the report,
the stderr, the `claude` envelopes its wrapper kept. So the runner is tested
against the real tool, and only the model is fake. Two doors to one fake
model:

- `responder(...)`, for `tests/fake_endpoint.FakeEndpoint`: an
  OpenAI-compatible chat endpoint on 127.0.0.1, which the real transport
  reaches over a real socket (streaming, retries and all);
- `write_fake_claude(...)`, an executable that answers `claude --print
  --output-format json` on stdin and stdout with the CLI's result envelope,
  for the runner's own `claude` wrapper to start.

The fake reads the prompt the tool actually sent, as a model would: a merge
prompt's `<document>` blocks, a decompose prompt's numbered lines, a verify
prompt's claim list and reference text. Its answers are valid against the
schema the prompt carries, so a clean run of the whole pipeline exits 0 or 1
on its own merits, and a behaviour below changes exactly one thing:

    merge            good | lossy (drops one segment, silently) |
                     declares (drops it and declares it) | concat
    fail_merge_on    [text]: a merge whose prompt holds the text answers
                     unusable JSON every time (a model failure, exit 2)
    platform_on      {text: n}: the first n calls whose prompt holds the
                     text fail on the platform (HTTP 503, or the CLI's 529)
    blank_length_on  [text]: a verify call whose prompt holds the text answers
                     empty with finish_reason "length" (an `unruled` call)
    usage_limit_at   n: (claude) the n-th call answers a usage-limit envelope,
                     once
    limit_text       the usage-limit envelope's text (default `LIMIT_TEXT`)
    utilisation      f: where a ceiling was sent, completion_tokens is f of it
    serve_as         id: the answer names this model instead of the one asked
    refuse_merge_on  [text]: a merge whose prompt holds the text is refused,
                     every time: over HTTP a refusal's shape (200, content null,
                     finish_reason content_filter), through `claude` the CLI's
                     refusal sentence as the result
    refusal_blank_once_on  [text]: (HTTP) the first verify call whose prompt
                     holds the text is a content_filter blank; the re-ask answers
    empty_result_once_on   [text]: (claude) the first call whose prompt holds the
                     text answers an envelope with an empty `result`
    oauth_expired_at n: (claude) from the n-th call on, the login has expired
                     (the CLI's 401 envelope), until `relogin` is called

An outage is the fake's, not one model's: `schedule_outage(state, n)` takes
the network down after n more answered calls, for every model on both doors
(HTTP answers 503 "network down", the CLI its "Connection error" envelope),
and `restore(state)` brings it back. `outage(state)` says whether it is down.

State (the counters `platform_on` and `usage_limit_at` need) lives in a JSON
file beside the fake, locked, so a fake `claude` started once per call still
counts across calls.

    python3 tests/lineup_fakes.py dry-run --out DIR     the whole registered
                                                        lineup against fakes
"""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"

# The first sentence of each prompt the pipeline sends, as `test_cli.Script`
# keys them. `check_markers` (run by the tests) fails if a prompt is reworded.
MARKERS = (
    ("merge", "Combine the source documents below"),
    # Before decompose: the coverage prompt opens with decompose's own sentence.
    ("coverage", "then decide whether the merged document carries each one"),
    ("decompose", "Extract every independently checkable factual assertion"),
    ("forward", "supported by the reference text below"),
    ("reverse", "supported by the source documents below"),
)
WARM_UP = "LINEUP WARM-UP"
LIMIT_TEXT = "You've hit your limit · resets 3pm (Europe/Berlin)"
VERSION = "2.1.283 (Claude Code)"
# The Claude Code refusal sentence (the CLI's own wording for a refused turn; the
# policy link it carries is left out, a tracked file holds no address).
CLI_REFUSAL = ("Claude Code is unable to respond to this request, which appears to violate "
               "our Usage Policy. Please double press esc to edit your last message or start "
               "a new session for Claude Code to assist with a different task.")
OAUTH_EXPIRED = ("OAuth token has expired. Please obtain a new token or refresh your existing "
                 "token.")


def check_markers() -> list[str]:
    """Every marker is still in the prompt it names. Returns the misses."""
    texts = {"merge": "merge.md", "decompose": "decompose.md", "forward": "verify.md",
             "reverse": "verify_reverse.md", "coverage": "verify_coverage.md"}
    out = []
    for kind, marker in MARKERS:
        body = (ROOT / "prompts" / texts[kind]).read_text(encoding="utf-8")
        if marker not in " ".join(body.split()):
            out.append(f"{kind}: {marker!r} is not in prompts/{texts[kind]}")
    return out


def kind_of(content: str) -> str:
    flat = " ".join(content[:4000].split())
    if flat.startswith(WARM_UP):
        return "warm"
    for kind, marker in MARKERS:
        if marker in flat:
            return kind
    raise ValueError(f"unrecognised prompt: {content[:80]!r}")


# --- the fake model's answers ------------------------------------------------

_DOC = re.compile(r'<document id="(?P<id>[^"]+)" filename="(?P<name>[^"]+)"'
                  r'(?P<base> base="true")?>\n(?P<body>.*?)\n</document>', re.S)
_SEG = re.compile(r"^(?P<sid>[a-z]+\d+)\| ?(?P<text>.*)$")
_CONT = re.compile(r"^\s+\| ?(?P<text>.*)$")
_NUMBERED = re.compile(r"^\s*(\d+) ?\| ?(.*)$")
_CLAIM = re.compile(r"^([A-Z]+-\d+): (.*)$")


def _segments(body: str) -> list:
    """[[segment id, text], ...] with None for a paragraph break."""
    out: list = []
    for line in body.split("\n"):
        seg = _SEG.match(line)
        if seg:
            out.append([seg["sid"], seg["text"]])
            continue
        cont = _CONT.match(line)
        if cont and out and out[-1] is not None:
            out[-1][1] += "\n" + cont["text"]
            continue
        if not line.strip() and out and out[-1] is not None:
            out.append(None)
    return out


def merge_answer(content: str, behaviour: str = "good") -> dict:
    """The base document, then every segment of the others it does not already carry."""
    docs = [(m["id"], bool(m["base"]), _segments(m["body"])) for m in _DOC.finditer(content)]
    if not docs:
        raise ValueError("a merge prompt with no <document> blocks")
    base = next((d for d in docs if d[1]), docs[0])
    seen: set[str] = set()
    lines: list[str] = []
    base_title = ""
    for seg in base[2]:
        if seg is None:
            lines.append("")
            continue
        if not base_title and seg[1].startswith("# "):
            base_title = seg[1]
        lines.append(seg[1])
        seen.add(" ".join(seg[1].split()))
    dispositions, extra = [], []
    for doc in docs:
        if doc is base:
            continue
        for seg in doc[2]:
            if seg is None or " ".join(seg[1].split()) in seen:
                continue
            if seg[1].startswith("# "):
                # Another document's title: superseded by the base's, and said so.
                dispositions.append({"segment": seg[0], "disposition": "superseded",
                                     "replacement": base_title or seg[1],
                                     "reason": "one title for the merged document"})
                continue
            extra.append(seg)
    if behaviour in ("lossy", "declares") and extra:
        dropped = extra.pop()
        if behaviour == "declares":
            dispositions.append({"segment": dropped[0], "disposition": "dropped",
                                 "replacement": "", "reason": "left out"})
    for seg in extra:
        lines += ["", seg[1]]
        seen.add(" ".join(seg[1].split()))
    text = "\n".join(lines)
    if behaviour == "concat":
        text = "\n\n".join("\n".join(s[1] for s in d[2] if s) for d in docs)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    answer = {"merged_document": text, "decisions": [], "dispositions": dispositions,
              "mismatch": ""}
    if '"additions"' in content:
        answer["additions"] = []
    return answer


def decompose_answer(content: str, limit: int = 14) -> dict:
    """One claim per numbered line that reads as a sentence; headings skipped."""
    body = content.rsplit("DOCUMENT:\n", 1)[-1].split("\n\nSCHEMA:")[0]
    claims = []
    for line in body.split("\n"):
        numbered = _NUMBERED.match(line)
        if not numbered:
            continue
        text = numbered[2].strip()
        if len(text) < 12 or text.startswith(("#", "|", "```", "<!--")):
            continue
        claims.append({"text": text, "line": int(numbered[1]), "span": text})
    return {"claims": claims[:limit]}


def verify_answer(content: str) -> dict:
    """SUPPORTED where the claim's text is in a reference verbatim, MISSING where not."""
    head, _, tail = content.rpartition("\n\nCLAIMS:\n")
    block = tail.split("\n\nSCHEMA:")[0]
    references: dict[str, str] = {}
    if "SOURCE DOCUMENTS:\n" in head:
        body = head.split("SOURCE DOCUMENTS:\n", 1)[1]
        for found in re.finditer(r"^--- (\S+) ---\n(.*?)(?=^--- \S+ ---\n|\Z)", body,
                                 re.S | re.M):
            references[found.group(1)] = " ".join(found.group(2).split())
    elif "REFERENCE TEXT" in head:
        ref = head.split("REFERENCE TEXT", 1)[1]
        named = re.match(r" \(([^)]+)\):\n", ref)
        references[named.group(1) if named else "merged.md"] = " ".join(
            ref[named.end() if named else 0:].split())
    verdicts = []
    for line in block.split("\n"):
        claim = _CLAIM.match(line)
        if not claim:
            continue
        text = " ".join(claim[2].split())
        where = next((name for name, flat in references.items() if text in flat), "")
        verdicts.append({"claim_id": claim[1], "verdict": "SUPPORTED" if where else "MISSING",
                         "evidence": text if where else "", "evidence_source": where,
                         "rationale": ("Stated in the reference." if where
                                       else "Not in the reference.")})
    return {"verdicts": verdicts}


# --- shared state across processes --------------------------------------------

@contextlib.contextmanager
def _state(path: Path):
    """The fake's counters, read and written under an exclusive lock."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.seek(0)
        raw = handle.read()
        data = json.loads(raw) if raw.strip() else {}
        yield data
        handle.seek(0)
        handle.truncate()
        handle.write(json.dumps(data))
        handle.flush()
        fcntl.flock(handle, fcntl.LOCK_UN)


class Model:
    """One fake model: its behaviour, and the decision each call gets."""

    def __init__(self, name: str, spec: dict | None, state: Path) -> None:
        self.name = name
        self.spec = dict(spec or {})
        self.state = state

    def decide(self, content: str, door: str = "http") -> tuple[str, str]:
        """(outcome, kind): outcome is answer, garbage, platform, blank_length or usage_limit.

        `door` is `http` or `claude`: a usage limit is the subscription's, so
        only the fake `claude` counts toward it and meets it.
        """
        kind = kind_of(content)
        if kind == "warm":
            return "warm", kind
        spec = self.spec
        with _state(self.state) as data:
            after = data.get("outage_after")
            if after is not None and data.get("answered", 0) >= after:
                data["down"], data["outage_after"] = True, None
            if data.get("down"):
                data["refused_while_down"] = data.get("refused_while_down", 0) + 1
                return "network", kind
            calls = data.setdefault("calls", {})
            key = f"{door}|{self.name}"
            calls[key] = calls.get(key, 0) + 1
            n = calls[key]
            limit_at = spec.get("usage_limit_at") if door == "claude" else None
            used = data.setdefault("usage_limit_used", {})
            if limit_at and n >= limit_at and not used.get(self.name):
                used[self.name] = True
                return "usage_limit", kind
            expired_at = spec.get("oauth_expired_at") if door == "claude" else None
            if expired_at and n >= expired_at and not (data.get("relogged") or {}).get(
                    self.name):
                return "oauth_expired", kind
            once = data.setdefault("once_fired", {})
            for field, doors, kinds in (
                    ("refusal_blank_once_on", ("http",), ("forward", "reverse")),
                    ("empty_result_once_on", ("claude",), None)):
                for text in spec.get(field) or []:
                    key = f"{field}|{self.name}|{text}"
                    if door in doors and (kinds is None or kind in kinds) and \
                            text in content and not once.get(key):
                        once[key] = True
                        return field.split("_once_on")[0], kind
            fired = data.setdefault("platform_fired", {})
            for text, times in (spec.get("platform_on") or {}).items():
                key = f"{self.name}|{text}"
                if text in content and fired.get(key, 0) < times:
                    fired[key] = fired.get(key, 0) + 1
                    return "platform", kind
        if kind == "merge" and any(t in content for t in spec.get("fail_merge_on") or []):
            return "garbage", kind
        if kind == "merge" and any(t in content for t in spec.get("refuse_merge_on") or []):
            return "refusal", kind
        if kind in ("forward", "reverse") and any(
                t in content for t in spec.get("blank_length_on") or []):
            return "blank_length", kind
        with _state(self.state) as data:
            data["answered"] = data.get("answered", 0) + 1
        return "answer", kind

    def answer(self, content: str, kind: str) -> str:
        if kind == "merge":
            return json.dumps(merge_answer(content, self.spec.get("merge", "good")))
        if kind == "decompose":
            return json.dumps(decompose_answer(content))
        if kind in ("forward", "reverse", "coverage"):
            return json.dumps(verify_answer(content))
        return "OK"

    @property
    def served(self) -> str:
        return self.spec.get("serve_as") or self.name


def schedule_outage(state: Path, after_calls: int = 0) -> None:
    """The network goes down after `after_calls` more answered calls (the outage tests)."""
    with _state(state) as data:
        data["outage_after"] = data.get("answered", 0) + after_calls
        data["down"] = after_calls == 0


def restore(state: Path) -> None:
    """The network is back."""
    with _state(state) as data:
        data["down"], data["outage_after"] = False, None


def outage(state: Path) -> bool:
    with _state(state) as data:
        return bool(data.get("down"))


def answered(state: Path) -> int:
    with _state(state) as data:
        return int(data.get("answered", 0))


def relogin(state: Path, name: str) -> None:
    """The operator logs the fake `claude` in again after `oauth_expired_at`."""
    with _state(state) as data:
        data.setdefault("relogged", {})[name] = True


def _completion_tokens(model: Model, text: str, ceiling) -> int:
    share = model.spec.get("utilisation")
    if share is not None and isinstance(ceiling, int) and ceiling > 0:
        return max(1, int(ceiling * float(share)))
    return max(8, len(text) // 4)


def responder(models: dict[str, dict], state: Path):
    """A `FakeEndpoint` responder answering as each named model would."""

    def respond(body: dict, _n: int):
        name = str(body.get("model") or "")
        model = Model(name, models.get(name), state)
        content = (body.get("messages") or [{}])[0].get("content") or ""
        outcome, kind = model.decide(content)
        if outcome == "platform":
            return 503, json.dumps({"error": {"message": "fake: overloaded"}}), \
                {"Retry-After": "0.01"}
        if outcome == "network":
            return 503, json.dumps({"error": {"message": "fake: network down"}}), \
                {"Retry-After": "0.01"}
        ceiling = body.get("max_tokens") or body.get("max_completion_tokens")
        if outcome in ("refusal", "refusal_blank"):
            # The refusal shape: how Anthropic's compatibility endpoint reports a refusal.
            return 200, json.dumps({
                "id": "chatcmpl-fake", "object": "chat.completion", "model": model.served,
                "choices": [{"index": 0, "message": {"role": "assistant", "content": None},
                             "finish_reason": "content_filter"}],
                "usage": {"prompt_tokens": max(1, len(content) // 4), "completion_tokens": 0}})
        if outcome == "blank_length":
            text, finish = "", "length"
        elif outcome == "garbage":
            text, finish = "this is not json, and the fake says so", "stop"
        else:
            text, finish = model.answer(content, kind), "stop"
        envelope = {
            "id": "chatcmpl-fake", "object": "chat.completion", "model": model.served,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": text},
                         "finish_reason": finish}],
            "usage": {"prompt_tokens": max(1, len(content) // 4),
                      "completion_tokens": _completion_tokens(model, text, ceiling)},
        }
        return 200, json.dumps(envelope)

    return respond


# --- the fake `claude` ---------------------------------------------------------

_CLAUDE = '''#!{python} -I
"""A fake `claude --print --output-format json`. Written by tests/lineup_fakes.py."""
import json, sys, time
sys.path.insert(0, {tests!r})
import lineup_fakes
sys.exit(lineup_fakes.fake_claude_main(sys.argv[1:], {spec!r}, {state!r}))
'''


def write_fake_claude(directory: Path, models: dict[str, dict], state: Path,
                      name: str = "claude-2.1.283-fake") -> Path:
    """An executable fake `claude`, its behaviour in a JSON file beside it."""
    directory.mkdir(parents=True, exist_ok=True)
    spec = directory / f"{name}.json"
    spec.write_text(json.dumps(models, indent=1), encoding="utf-8")
    program = directory / name
    program.write_text(_CLAUDE.format(python=sys.executable, tests=str(TESTS),
                                      spec=str(spec), state=str(state)), encoding="utf-8")
    program.chmod(0o755)
    return program


def fake_claude_main(argv: list[str], spec_path: str, state_path: str) -> int:
    if "--version" in argv:
        print(VERSION)
        return 0
    content = sys.stdin.read()
    name = argv[argv.index("--model") + 1] if "--model" in argv else "unknown"
    models = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    model = Model(name, models.get(name), Path(state_path))
    outcome, kind = model.decide(content, door="claude")
    tokens_in = max(1, len(content) // 4)
    base = {"type": "result", "num_turns": 1, "duration_ms": 900, "duration_api_ms": 850,
            "session_id": "fake"}
    if outcome == "usage_limit":
        print(json.dumps({**base, "subtype": "success", "is_error": True,
                          "result": model.spec.get("limit_text") or LIMIT_TEXT,
                          "total_cost_usd": 0, "usage": {"input_tokens": 0, "output_tokens": 0},
                          "modelUsage": {}}))
        return 1
    if outcome == "oauth_expired":
        print(json.dumps({**base, "subtype": "success", "is_error": True,
                          "result": OAUTH_EXPIRED, "api_error_status": 401,
                          "terminal_reason": "api_error", "total_cost_usd": 0,
                          "usage": {"input_tokens": 0, "output_tokens": 0}, "modelUsage": {}}))
        return 1
    if outcome == "empty_result":
        print(json.dumps({**base, "subtype": "success", "is_error": False, "result": "",
                          "total_cost_usd": 0.0001,
                          "usage": {"input_tokens": tokens_in, "output_tokens": 0},
                          "modelUsage": {model.served: {"inputTokens": tokens_in,
                                                        "outputTokens": 0, "costUSD": 0.0001}}}))
        return 0
    if outcome == "network":
        print(json.dumps({**base, "subtype": "success", "is_error": True,
                          "terminal_reason": "api_error",
                          "result": "API Error: Connection error.",
                          "total_cost_usd": 0, "usage": {"input_tokens": 0, "output_tokens": 0},
                          "modelUsage": {}}))
        return 1
    if outcome == "platform":
        print(json.dumps({**base, "subtype": "success", "is_error": True,
                          "api_error_status": 529, "terminal_reason": "api_error",
                          "result": 'API Error: 529 {"type":"error","error":{"type":'
                                    '"overloaded_error","message":"Overloaded"}}',
                          "total_cost_usd": 0, "usage": {"input_tokens": 0, "output_tokens": 0},
                          "modelUsage": {}}))
        return 1
    text = ("this is not json, and the fake says so" if outcome == "garbage"
            else CLI_REFUSAL if outcome == "refusal" else model.answer(content, kind))
    tokens_out = max(8, len(text) // 4)
    cost = round((tokens_in * 3.0 + tokens_out * 15.0) / 1_000_000, 6)
    usage = {"input_tokens": tokens_in, "output_tokens": tokens_out,
             "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    print(json.dumps({**base, "subtype": "success", "is_error": False, "result": text,
                      "total_cost_usd": cost, "usage": usage,
                      "modelUsage": {model.served: {
                          "inputTokens": tokens_in, "outputTokens": tokens_out,
                          "cacheReadInputTokens": 0, "cacheCreationInputTokens": 0,
                          "costUSD": cost}}}))
    return 0


# --- the dry run -------------------------------------------------------------------

# What the dry run's fake models do, so its figures table shows each rule at
# work: a lossy model (disqualified on silent loss) whose endpoint also keeps
# failing one pair while its reference answers (an `endpoint_failure`), one
# that fails the largest pair (its own exit 2, which shrinks nobody's
# pairs), a platform failure in the middle of a cell whose retry reuses the
# merge and decompose calls it already got, a usage limit on the
# subscription lane that stops it and resumes, a merge refused on both routes
# (`refused`, and flagged), a refusal blank a re-ask recovers (a
# completed cell with an unruled call), and the subscription's blank result
# retried as the platform's. The self-hosted 27B row has left the release
# lineup, so no fake models it in this dry run any more.
DRY_RUN_BEHAVIOUR = {
    "gpt-6-luna": {"merge": "lossy", "platform_on": {"Nimbrel Probe stream name": 99}},
    "claude-haiku-4-5-20251001": {"fail_merge_on": ["Rate limiting and the 429 contract"],
                                  "empty_result_once_on": ["Badge Access"]},
    "gpt-6-sol": {"platform_on": {"supported by the reference text below": 3}},
    "claude-sonnet-5": {"merge": "declares", "usage_limit_at": 40,
                        "refusal_blank_once_on": ["Nimbrel Probe"]},
    "claude-opus-5-5": {"refuse_merge_on": ["Payroll Submission Deadlines"]},
}


def dry_run(out: Path, *, sets: str | None = None) -> int:
    """The full registered lineup against fakes, end to end, from a clone of HEAD."""
    sys.path.insert(0, str(TESTS))
    sys.path.insert(0, str(ROOT / "src"))
    import run_lineup  # noqa: PLC0415
    from fake_endpoint import FakeEndpoint  # noqa: PLC0415

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    tree = out / "tree"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(ROOT), str(tree)], check=True)
    pin = subprocess.run(["git", "-C", str(tree), "rev-parse", "HEAD"], check=True,
                         capture_output=True, text=True).stdout.strip()
    state = out / "fakes" / "state.json"
    claude = write_fake_claude(out / "fakes", DRY_RUN_BEHAVIOUR, state)
    registration = run_lineup.template(pin=pin, clone="tree")
    registration["claude"] = {"path": str(claude), "version": VERSION.split()[0],
                              "sha256": run_lineup.sha256_file(claude)}
    # A parsed reset is never slept to here: the lane stops and is resumed.
    registration["retry"] = {"passes": 2, "spacing_seconds": 0, "breaker": 4,
                             "usage_limit_max_sleep_seconds": 0}
    registration["caps"] = {"anthropic": 200.0, "openai": 200.0, "overall": 400.0}
    registration.pop("env_file", None)
    for row in registration["rows"]:
        for key, value in list(row.items()):
            if isinstance(value, str) and "<FILL" in value:
                row.pop(key)
        # What the operator fills from the pilots: Fable's hardest documents.
        # The fake Fable answers as `fable`.
        row.setdefault("thinking", list(run_lineup.ROLES))
        # The fakes have no rate limit to respect: the pacing is kept, and short.
        if row.get("min_interval"):
            row["min_interval"] = 0.2
        if row["id"] == "fable-sub":
            row["items"] = {"S1": ["rate_limits", "index_429", "trace_names"]}
            row.pop("served_aliases", None)
    if sets:
        keep = sets.split(",")
        registration["sets"] = {k: v for k, v in registration["sets"].items() if k in keep}
        for row in registration["rows"]:
            row["sets"] = [s for s in row["sets"] if s in keep]
            if "items" in row:
                row["items"] = {k: v for k, v in row["items"].items() if k in keep}
    with contextlib.ExitStack() as stack:
        urls = {}
        for vendor in ("anthropic", "openai", "google"):
            endpoint = FakeEndpoint(responder(DRY_RUN_BEHAVIOUR, state), prompt_ratio=None)
            urls[vendor] = stack.enter_context(endpoint)
        for row in registration["rows"] + registration["references"]:
            route = row["route"]
            if route["kind"] == "http":
                route["key_env"] = "LINEUP_FAKE_KEY"
                if route.get("base_url_env"):
                    continue  # a self-hosted address comes from the environment, as live
                route["base_url"] = urls[row["vendor"]]
        registration["infrastructure"]["probe_urls"] = [
            urls["anthropic"] + "/models", urls["openai"] + "/models"]
        path = out / "REGISTRATION.md"
        path.write_text(run_lineup.render_registration(registration), encoding="utf-8")
        env = {**os.environ, "LINEUP_FAKE_KEY": "fake-key-not-a-secret"}
        runner = [sys.executable, str(tree / "tests" / "run_lineup.py")]
        started = time.monotonic()
        codes = {}
        lanes = sorted({row["lane"] for row in registration["rows"]})
        procs = {lane: subprocess.Popen(runner + ["run", "--registration", str(path),
                                                  "--lane", lane],
                                        env=env, stdout=open(out / f"lane-{lane}.log", "w"),
                                        stderr=subprocess.STDOUT)
                 for lane in lanes}
        for lane, proc in procs.items():
            codes[lane] = proc.wait()
        # A lane stopped by its usage limit is resumed, as the operator would.
        for lane, code in list(codes.items()):
            if code == run_lineup.EXIT_USAGE_LIMIT:
                with open(out / f"lane-{lane}.log", "a") as log:
                    codes[lane] = subprocess.run(
                        runner + ["run", "--registration", str(path), "--lane", lane],
                        env=env, stdout=log, stderr=subprocess.STDOUT).returncode
                codes[f"{lane} (resumed)"] = codes[lane]
        print(f"lanes finished in {time.monotonic() - started:.0f}s: {codes}")
        # A self-hosted address never reaching the run's own files is
        # covered directly in test_run_lineup.py with its own fake row (no
        # self-hosted row is registered in this dry run any more).
    figures = subprocess.run([sys.executable, str(tree / "tests" / "lineup_figures.py"),
                              "--run-dir", str(out), "--write"], capture_output=True, text=True)
    print(figures.stdout[-400:], figures.stderr[-2000:])
    check = subprocess.run([sys.executable, str(tree / "tests" / "lineup_figures.py"),
                            "--run-dir", str(out), "--check"], capture_output=True, text=True)
    print(check.stdout[-600:], check.stderr[-1000:])
    table = out / "figures.md"
    if table.exists():
        print(table.read_text(encoding="utf-8"))
    return 0 if check.returncode == 0 and all(c == 0 for c in codes.values()) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    dry = sub.add_parser("dry-run", help="the whole registered lineup against fakes")
    dry.add_argument("--out", type=Path, required=True)
    dry.add_argument("--sets", help="comma-separated set ids, default all")
    args = parser.parse_args(argv)
    if args.command == "dry-run":
        return dry_run(args.out.resolve(), sets=args.sets)
    return 2


if __name__ == "__main__":
    sys.exit(main())
