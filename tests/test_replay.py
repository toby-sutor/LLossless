#!/usr/bin/env python3
"""A replay reads each answer the way its recording run read it.

The defect this exists for: vLLM's guided decoding emits JSON keys
alphabetically, so a corpus recorded against it has to be recorded under
`--field-order any`. Replayed under the default `schema`, the same bytes are an
order fault. An answer with no other fault stops the call on the first attempt
(`SchemaFailure`: the merge shape). An answer with a second fault was repaired
when it was recorded, and a strict replay quotes the order fault in its repair
message too, so it asks for a repair nobody recorded (a replay miss: the verify
shape). Measured on the Qwen3.8-27B sizing corpus, 2026-09-24: both happened.

So a cassette carries the order it was read under (`meta.field_order`), and a
replay reads it no more strictly than that (`config.replay_field_order`). A
live run's default does not move.

Every recording here is made by the shipped client, against a local endpoint
that answers the way vLLM does, and every replay reads it back through the
shipped client. Nothing in this file writes a `field_order` stamp itself: the
must-fire controls only take one away.

One neighbour: `--model`, which every offline consumer uses to
pin the corpus's model, must name the decompose role over a model map too.

Run with `python3 tests/test_replay.py`, or collect with pytest.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs, so a test that points a
# socket anywhere but the configured endpoint fails loudly instead of
# succeeding quietly. tests/test_socket_guard.py asserts every module does this.
socket_guard.install()

from llossless import config, parsing, prompts, verify  # noqa: E402
from llossless.cassette import (  # noqa: E402
    UNSTAMPED_FIELD_ORDER, Cassette, MissingCassette, Store, canonical,
)
from llossless.client import Client, SchemaFailure  # noqa: E402
from fake_endpoint import FakeEndpoint, envelope  # noqa: E402
import replay_models  # noqa: E402
import run_verify  # noqa: E402
import stale_corpus  # noqa: E402

failures: list[str] = []

# A replay sends nothing; this address is never connected to.
NOWHERE = "http://127.0.0.1:1/v1"

RESPONSES = ROOT / "tests" / "responses"

VERDICT = {
    "claim_id": "c1",
    "verdict": "SUPPORTED",
    "evidence": "port 8443",
    "evidence_source": "a.md",
    "rationale": "stated in the source",
}
ALPHABETICAL = tuple(sorted(parsing.VERDICT_FIELDS))


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def verdicts_body(order: tuple[str, ...], **changes) -> str:
    """One verdict record, its keys in `order`, with any field replaced."""
    record = dict(VERDICT, **changes)
    return json.dumps({"verdicts": [{name: record[name] for name in order}]})


def verdicts_call(client: Client) -> dict:
    """One verify-shaped call, the response the order contract lives on."""
    return client.complete(
        role="verify",
        prompt=prompts.load("verify"),
        messages=[{"role": "user", "content": "claim c1: the relay listens on port 8443"}],
        schema=verify.VERDICT_SCHEMA,
        schema_name="emit_verdicts",
        semantic=parsing.check_verdicts,
    ).payload


def settings_for(base_url: str, tmp: Path, **kwargs) -> config.Settings:
    kwargs.setdefault("models", {"verify": "test-model"})
    kwargs.setdefault("cache_dir", tmp / "cache")
    kwargs.setdefault("use_cache", False)
    return config.Settings(base_url=base_url, **kwargs)


def attempt(call):
    """`(result, None)`, or `(None, the replay's failure)` -- so a red is a line, not a crash."""
    try:
        return call(), None
    except (SchemaFailure, MissingCassette) as exc:
        return None, f"{type(exc).__name__}: {str(exc).splitlines()[0][:160]}"


def unstamped_copy(source: Path, target: Path) -> Path:
    """`source` with every `meta.field_order` removed: what a build from before that field existed wrote."""
    target.mkdir(parents=True)
    for path in sorted(source.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["meta"].pop("field_order", None)
        (target / path.name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                                        encoding="utf-8")
    return target


def stamps(directory: Path) -> list:
    return [json.loads(p.read_text(encoding="utf-8"))["meta"].get("field_order")
            for p in sorted(directory.glob("*.json"))]


def test_the_reading_rule() -> None:
    """Never stricter than the recording; never stricter than the run asked."""
    for recorded, requested, want in (("schema", "schema", "schema"),
                                      ("schema", "any", "any"),
                                      ("any", "schema", "any"),
                                      ("any", "any", "any")):
        got = config.replay_field_order(recorded, requested)
        check(got == want, f"recorded {recorded}, requested {requested}: read under "
                           f"{got!r}, expected {want!r}")
    check(UNSTAMPED_FIELD_ORDER == config.FIELD_ORDERS[0] == "schema",
          "an unstamped cassette must read as the strictest order, so the run's "
          f"own setting decides; got {UNSTAMPED_FIELD_ORDER!r}")
    check(config.DEFAULT_FIELD_ORDER == "schema",
          "a live run's default must not move with this change, "
          f"got {config.DEFAULT_FIELD_ORDER!r}")


def test_a_recording_carries_the_order_it_was_read_under() -> None:
    """The write half, through the shipped client, both ways, and the reader's limits."""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        with FakeEndpoint(lambda _b, _n: (200, envelope(verdicts_body(ALPHABETICAL)))) as url:
            verdicts_call(Client(settings_for(url, tmp, field_order="any",
                                              record_dir=tmp / "any")))
        with FakeEndpoint(lambda _b, _n: (200, envelope(verdicts_body(parsing.VERDICT_FIELDS)))) as url:
            verdicts_call(Client(settings_for(url, tmp, record_dir=tmp / "schema")))
        check(stamps(tmp / "any") == ["any"],
              f"a run under --field-order any must stamp its recording, got {stamps(tmp / 'any')}")
        check(stamps(tmp / "schema") == ["schema"],
              f"a default run must stamp `schema`, not leave it implied, got {stamps(tmp / 'schema')}")

        # A caller that does not say writes no field, which reads as unstamped.
        store = Store(tmp / "silent")
        path = store.write(key="k" * 64, role="verify", model="m", tier="json_schema",
                           messages=[], schema=None, temperature=0.0, raw="{}",
                           http_status=200, endpoint="e", latency_ms=0, attempt=1)
        meta = json.loads(path.read_text(encoding="utf-8"))["meta"]
        check("field_order" not in meta, f"no order given must write none, got {meta}")
        check(Cassette.from_file(path).field_order == UNSTAMPED_FIELD_ORDER,
              "a cassette without the field must read as unstamped")

        # A value this build does not know is refused, not defaulted.
        data = json.loads(path.read_text(encoding="utf-8"))
        data["meta"]["field_order"] = "sideways"
        path.write_text(json.dumps(data), encoding="utf-8")
        try:
            Cassette.from_file(path)
            check(False, "an unknown meta.field_order must be refused")
        except ValueError as exc:
            check("sideways" in str(exc), f"the refusal must name the value, got {exc}")


def test_an_order_only_answer_replays_under_the_default() -> None:
    """The merge shape: nothing wrong but the order, accepted on attempt 1 when recorded."""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        with FakeEndpoint(lambda _b, _n: (200, envelope(verdicts_body(ALPHABETICAL)))) as url:
            verdicts_call(Client(settings_for(url, tmp, field_order="any",
                                              record_dir=tmp / "rec")))

        client = Client(settings_for(NOWHERE, tmp, replay_dir=tmp / "rec"))
        payload, error = attempt(lambda: verdicts_call(client))
        check(error is None and payload["verdicts"][0]["verdict"] == "SUPPORTED",
              f"the recorded answer must replay with no flag, got {error or payload}")
        check(client.usage.replayed == 1 and client.usage.repairs == 0,
              f"one replayed call and no repair, got {client.usage.replayed} and "
              f"{client.usage.repairs}")
        check(client.resolved_field_order() == "any",
              "the report must say the answer was read under `any`, got "
              f"{client.resolved_field_order()!r}")

        # MUST FIRE: the same bytes without the stamp are what every replay
        # got before that field existed, and the default refuses them.
        bare = unstamped_copy(tmp / "rec", tmp / "bare")
        try:
            verdicts_call(Client(settings_for(NOWHERE, tmp, replay_dir=bare)))
            check(False, "an unstamped alphabetical answer must still fail under the default")
        except SchemaFailure:
            pass
        # And the route that replayed it before still does.
        again = Client(settings_for(NOWHERE, tmp, replay_dir=bare, field_order="any"))
        check(verdicts_call(again)["verdicts"][0]["verdict"] == "SUPPORTED",
              "an unstamped cassette must still replay under an explicit --field-order any")


def test_a_repaired_answer_replays_under_the_default() -> None:
    """The verify shape: a second fault, a repair, and a repair message that must match.

    The second fault is a semantic one, as the order fault is: both come out of
    `verdict_defects`, so a strict reading quotes both and a relaxed one quotes
    only the evidence. A schema-walk fault would stop before the order check
    and give the same message both ways, which is not the shape that missed.
    """
    def responder(_body, number):
        if number == 1:
            return 200, envelope(verdicts_body(ALPHABETICAL, evidence=""))
        return 200, envelope(verdicts_body(ALPHABETICAL))

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        with FakeEndpoint(responder) as url:
            recording = Client(settings_for(url, tmp, field_order="any", record_dir=tmp / "rec"))
            verdicts_call(recording)
        check(recording.usage.repairs == 1 and len(stamps(tmp / "rec")) == 2,
              f"the fixture must record a repair: {recording.usage.repairs} repairs, "
              f"{len(stamps(tmp / 'rec'))} cassettes")

        client = Client(settings_for(NOWHERE, tmp, replay_dir=tmp / "rec"))
        payload, error = attempt(lambda: verdicts_call(client))
        check(error is None and client.usage.replayed == 2
              and payload["verdicts"][0]["verdict"] == "SUPPORTED",
              f"both attempts must replay with no flag, got {client.usage.replayed} "
              f"replayed; {error or payload}")

        # MUST FIRE: read strictly, attempt 1's repair message also quotes the
        # order, so attempt 2 is a request nobody recorded.
        bare = unstamped_copy(tmp / "rec", tmp / "bare")
        try:
            verdicts_call(Client(settings_for(NOWHERE, tmp, replay_dir=bare)))
            check(False, "an unstamped repaired recording must miss under the default")
        except MissingCassette:
            pass


def committed_verify_answers() -> dict[bytes, str]:
    """Every committed root verify answer, by the messages that asked for it."""
    return {canonical(data["request"]["messages"]): data["response"]["raw"]
            for data in (json.loads(p.read_text(encoding="utf-8"))
                         for p in sorted(replay_models.RESPONSES.glob("verify-*.json")))}


def as_vllm_answers(raw: str) -> str:
    """The same answer, serialized the way vLLM's guided decoding emits it: keys sorted."""
    body = json.loads(raw)
    message = body["choices"][0]["message"]
    message["content"] = json.dumps(json.loads(message["content"]), sort_keys=True)
    return json.dumps(body)


@contextlib.contextmanager
def cache_in(directory: Path):
    """`LLOSSLESS_CACHE_DIR` pointed at `directory` for an in-process run, then restored.

    A runner resolves its cache from the environment, and in a checkout the
    default is the repository's own `.llossless-cache/`. A recording run writes
    its capability record there, which the publication rehearsal refuses to
    find in the copy it builds.
    """
    saved = os.environ.get("LLOSSLESS_CACHE_DIR")
    os.environ["LLOSSLESS_CACHE_DIR"] = str(directory)
    try:
        yield
    finally:
        if saved is None:
            os.environ.pop("LLOSSLESS_CACHE_DIR", None)
        else:
            os.environ["LLOSSLESS_CACHE_DIR"] = saved


def replay_command(corpus: Path, model_argv: list[str], cache: Path) -> subprocess.CompletedProcess:
    """`run_verify.py --replay`, as a command, with no field order anywhere in its environment."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("LLOSSLESS_")}
    env["LLOSSLESS_CACHE_DIR"] = str(cache)
    return subprocess.run(
        [sys.executable, "tests/run_verify.py", "--replay", str(corpus),
         "--fixture", "dropped_claim", "--samples", "1", "--no-cache", "--no-colour",
         *model_argv],
        cwd=ROOT, env=env, capture_output=True, text=True, timeout=300)


def test_a_relaxed_corpus_replays_through_the_command_with_no_flag() -> None:
    """End to end: the runner records under `any`, the command replays with nothing set.

    The endpoint answers each request with the committed corpus's own answer
    to it, keys sorted, which is what the 27B on vLLM sends. The recording is
    the runner's own `--record`; the replay is `tests/run_verify.py` as a
    command, the way `audit_docs` and the publication rehearsal run it.
    """
    answers = committed_verify_answers()
    model_argv = replay_models.replay_argv(roles=("verify",))
    unknown: list[int] = []

    def as_recorded(messages):
        # The committed answers were asked before the held-back prompt
        # changes, so the question is looked up as it was worded then. What is
        # recorded here is recorded under HEAD's prompt, and replays under it.
        return [dict(m, content=undo_held_back_everywhere(m.get("content") or ""))
                for m in messages or []]

    def responder(body, number):
        raw = answers.get(canonical(as_recorded(body.get("messages"))))
        if raw is None:
            unknown.append(number)
            return 500, "{}"
        return 200, as_vllm_answers(raw)

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        printed = io.StringIO()
        with FakeEndpoint(responder) as url, contextlib.redirect_stdout(printed), \
                contextlib.redirect_stderr(printed), cache_in(tmp / "cache"):
            code = run_verify.main([
                "--record", str(tmp / "rec"), "--base-url", url, "--field-order", "any",
                "--fixture", "dropped_claim", "--samples", "1", "--structured", "json_schema",
                "--window", "32768", "--no-cache", "--no-colour", *model_argv])
        recorded = stamps(tmp / "rec")
        check(code in (0, 1) and not unknown and recorded and set(recorded) == {"any"},
              f"the recording run must finish and stamp every cassette `any`: exit {code}, "
              f"{len(unknown)} unanswerable request(s), stamps {recorded}")

        out = replay_command(tmp / "rec", model_argv, tmp / "cache")
        text = out.stdout + out.stderr
        check(out.returncode in (0, 1) and "replay miss" not in text
              and f"0 live, 0 cached, {len(recorded)} replayed" in text
              and "| Errors | 0 |" in text,
              f"the command must replay the relaxed corpus with no flag: exit "
              f"{out.returncode}; {next((l.strip() for l in text.splitlines() if 'live,' in l or 'miss' in l), text[-300:])}")
        check("field order any" in text,
              "the replay's report must say how its answers were read")

        # MUST FIRE: the same corpus unstamped does not reproduce under the default.
        bare = unstamped_copy(tmp / "rec", tmp / "bare")
        out = replay_command(bare, model_argv, tmp / "cache")
        text = out.stdout + out.stderr
        check(out.returncode == 2 or "replay miss" in text,
              f"an unstamped alphabetical corpus must fail under the default, exit {out.returncode}")


def test_the_committed_corpus_replays_with_no_flag() -> None:
    """The offline corpus, at the default field order: 0 live, nothing missed, nothing errored.

    Today that corpus is qwen3:8b and unstamped, so this is the "replays exactly
    as it does now" half. After the 27B import it is stamped `any`, and this is
    the half that says no consumer needs a flag.
    """
    printed = io.StringIO()
    with tempfile.TemporaryDirectory() as raw, contextlib.redirect_stdout(printed), \
            contextlib.redirect_stderr(printed), cache_in(Path(raw)):
        code = run_verify.main(["--offline", "--no-cache", "--no-colour",
                                *replay_models.replay_argv(roles=("verify",))])
    text = printed.getvalue()
    # Exit 3 is `run_verify`'s "everything measured passed, and something was
    # not measured": `attribution_invented`'s reverse call has no cassette on
    # the 27B, and its two probes must say so by name.
    check(code in (0, 1, 3) and "replay miss" not in text and "| Errors | 0 |" in text
          and " 0 live, 0 cached, " in text,
          f"the committed verify corpus must replay with no flag, exit {code}; "
          f"{next((l.strip() for l in text.splitlines() if 'live,' in l or 'miss' in l), text[-300:])}")
    held = stale_corpus.deferred_reason(RESPONSES, "verify")
    if held is not None:
        # The whole corpus predates a held-back prompt change, so every
        # probe is UNMEASURED for that reason, the runaway's two included.
        check(code == run_verify.UNMEASURED_EXIT and f"-- {held}" in text,
              f"a corpus stale by ruling must read UNMEASURED with its reason, exit {code}")
        return
    check("UNMEASURED: attribution_invented/m-tls-attributed, "
          "attribution_invented/m-read-timeout -- " + run_verify.RUNAWAY_27B in text,
          "the unrecordable reverse call must be reported UNMEASURED by name and reason")


def test_the_model_flag_names_every_role() -> None:
    """`--model` beats a model map's `decompose` entry, as it beats `verify` and `merge`.

    `model_for("decompose")` reads a `decompose` entry before it falls
    back to `verify`, and `--model` used to set only `verify` and
    `merge`. So a model map naming decompose kept decompose on the
    file's model under `--model`, and every replay that passes the
    corpus's model, which is how the offline consumers pin theirs
    (`replay_models`), missed on that role.
    """
    import argparse

    parser = argparse.ArgumentParser()
    config.add_arguments(parser)
    mapped = config.Settings(models={"verify": "file-model", "merge": "file-model",
                                     "decompose": "file-model"})
    flagged = config.apply_arguments(mapped, parser.parse_args(["--model", "flag-model"]))
    got = {role: flagged.model_for(role) for role in config.ROLES}
    check(set(got.values()) == {"flag-model"},
          f"--model must name every role over the model map, got {got}")
    split = config.apply_arguments(mapped, parser.parse_args(
        ["--model", "flag-model", "--merge-model", "merge-model"]))
    check(split.model_for("merge") == "merge-model"
          and split.model_for("decompose") == "flag-model",
          "--merge-model must still beat --model for merge, and only for merge")


# -- a corpus stale by ruling reads UNMEASURED -----------------


def prompts_with(tmp: Path, edit=None) -> Path:
    """A copy of HEAD's `prompts/`, with `edit(name, text) -> text` applied to each template."""
    copy = tmp / "prompts"
    shutil.copytree(ROOT / "prompts", copy)
    for path in copy.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        path.write_text(edit(path.stem, text) if edit else text, encoding="utf-8")
    return copy


def undo_held_back_everywhere(text: str) -> str:
    """A rendered message as it read before every held-back change."""
    for change in stale_corpus.HELD_BACK:
        text = text.replace(change.now, change.was)
    return text


def undo_held_back(name: str, text: str) -> str:
    """The template as it was before every held-back change: what the corpus was recorded under."""
    for change in stale_corpus.HELD_BACK:
        if change.template == name:
            text = text.replace(change.now, change.was)
    return text


def test_a_corpus_stale_by_ruling_is_detected_and_reads_unmeasured() -> None:
    """MUST FIRE: the verify corpora predate a held-back change, and a replay says so.

    On the real corpora and the real prompts: both verify corpora are stale by
    ruling alone, and the reason names the decision and the ruling. Then end
    to end through the shipped harness: `run_verify.py --offline` on one
    fixture reports every probe UNMEASURED with that reason, in the marker
    form `run_all` reads, makes no live call, and exits 3, not 1 or 2.
    """
    for corpus in (RESPONSES, RESPONSES / "m7"):
        found = stale_corpus.survey(corpus, "verify")
        check(found is not None and found.deferred and not found.faults,
              f"MUST FIRE: {corpus.name}'s verify cassettes predate a held-back change "
              f"and must read stale by ruling alone; got {found}")
        reason = stale_corpus.deferred_reason(corpus, "verify") or ""
        check(reason.startswith("prompt changed after recording; re-record deferred "
                                "by operator ruling of 2026-09-26"),
              f"the reason must name the change and the dated ruling: {reason[:120]!r}")

    printed = io.StringIO()
    scratch = tempfile.TemporaryDirectory(prefix="llossless-stale-")
    was = os.environ.get("LLOSSLESS_CACHE_DIR")
    os.environ["LLOSSLESS_CACHE_DIR"] = scratch.name
    try:
        with contextlib.redirect_stdout(printed):
            code = run_verify.main(["--offline", "--no-colour", "--samples", "1",
                                    "--fixture", "attribution_swapped"]
                                   + replay_models.replay_argv(roles=("verify",)))
    finally:
        if was is None:
            del os.environ["LLOSSLESS_CACHE_DIR"]
        else:
            os.environ["LLOSSLESS_CACHE_DIR"] = was
        scratch.cleanup()
    text = printed.getvalue()
    marked = [line.strip() for line in text.splitlines()
              if line.strip().startswith("UNMEASURED:")]
    check(code == run_verify.UNMEASURED_EXIT,
          f"a replay of a corpus stale by ruling exits {run_verify.UNMEASURED_EXIT}, got {code}")
    check(len(marked) == 1 and "operator ruling of 2026-09-26" in marked[0],
          f"the summary must carry one UNMEASURED marker naming the ruling: {marked}")
    check("0 live, 0 cached" in text, "a replay must make no live call")
    check("FAIL" not in text and "ERROR" not in text,
          "a probe stale by ruling is neither failed nor errored")


def test_a_fresh_corpus_is_not_stale_and_still_replays() -> None:
    """MUST NOT FIRE: a corpus recorded under HEAD's prompt is fresh, and replays.

    Three ways. Decompose and merge, whose prompts are unchanged, are fresh in
    both corpora. The verify corpora are fresh against HEAD's prompts with
    the held-back changes undone, which is what they were recorded under --
    so the detector fires on the change and on nothing else. And a replay
    through `run_merge.py` still serves every merge and decompose call from
    the corpus and prints the figures they make, with 0 misses.
    """
    import run_merge

    for corpus in (RESPONSES, RESPONSES / "m7"):
        for role in ("decompose", "merge"):
            check(stale_corpus.survey(corpus, role) is None,
                  f"MUST NOT FIRE: {corpus.name}'s {role} cassettes match HEAD's prompt")
    with tempfile.TemporaryDirectory() as raw:
        before = prompts_with(Path(raw), undo_held_back)
        for corpus in (RESPONSES, RESPONSES / "m7"):
            check(stale_corpus.survey(corpus, "verify", prompts=before) is None,
                  f"MUST NOT FIRE: {corpus.name}'s verify cassettes are fresh against "
                  f"the prompt they were recorded under")

    printed = io.StringIO()
    scratch = tempfile.TemporaryDirectory(prefix="llossless-stale-")
    was = os.environ.get("LLOSSLESS_CACHE_DIR")
    os.environ["LLOSSLESS_CACHE_DIR"] = scratch.name
    try:
        with contextlib.redirect_stdout(printed):
            code = run_merge.main(["--offline", "--no-colour", "--samples", "1",
                                   "--condition", "off", "--fixture", "attribution_swapped"]
                                  + replay_models.replay_argv(
                                      RESPONSES / "m7", ("decompose", "verify", "merge")))
    finally:
        if was is None:
            del os.environ["LLOSSLESS_CACHE_DIR"]
        else:
            os.environ["LLOSSLESS_CACHE_DIR"] = was
        scratch.cleanup()
    text = printed.getvalue()
    check("0 live, 0 cached, 2 replayed" in text,
          f"the merge and the decompose of the merged document must both replay: "
          f"{next((l for l in text.splitlines() if 'live,' in l), 'no census')}")
    check("must_not_extract ...... 0 unit(s)" in text and "Prompt-example leaks .. 0" in text,
          "the figures merge and decompose make must still be printed and asserted")
    check(code == run_merge.UNMEASURED_EXIT and "UNMEASURED:" in text,
          f"with the verify half stale by ruling the run exits "
          f"{run_merge.UNMEASURED_EXIT} and says so; got {code}")


def test_a_stale_corpus_no_ruling_covers_is_a_fault() -> None:
    """MUST FIRE the other way: staleness the ruling does not cover is not excused.

    A verify template edited somewhere the held-back list does not name makes
    every verify cassette a fault, and `deferred_reason` refuses it. So does a
    listed change HEAD no longer carries: a stale list excuses nothing.
    """
    with tempfile.TemporaryDirectory() as raw:
        other = prompts_with(Path(raw) / "a", lambda name, text: text.replace(
            "Judge only against the reference text.", "Judge against the reference text."))
        found = stale_corpus.survey(RESPONSES, "verify", prompts=other)
        check(found is not None and not found.deferred and found.faults,
              f"MUST FIRE: an unlisted edit must make the corpus a fault: {found}")
        before = prompts_with(Path(raw) / "b", undo_held_back)
        (before / "verify.md").write_text(
            (before / "verify.md").read_text(encoding="utf-8").replace(
                "Judge only against", "Judge solely against"), encoding="utf-8")
        found = stale_corpus.survey(RESPONSES, "verify", prompts=before)
        check(found is not None and not found.deferred,
              f"MUST FIRE: a held-back change HEAD does not carry must excuse nothing: {found}")


def test_replay() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_replay" and callable(function):
            function()

    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("replay: all checks pass; recorded field order and corpus model both honoured")
    return 0


if __name__ == "__main__":
    sys.exit(main())
