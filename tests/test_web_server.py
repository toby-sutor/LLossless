#!/usr/bin/env python3
"""The HTTP server and the versioned JSON contract, driven over a real socket.

`src/llossless/web/api.py`, `server.py` and `redact.py` are tested here. Everything here
runs against a server bound to port 0 on loopback and driven with
`urllib.request` -- not against the handler functions, and not against `Api`
alone. That is a rule this project arrived at the expensive way: four defects
lived only on the command path while the functions underneath them tested green,
and a contract exercised by calling its own implementation is a contract whose
routing, header handling and status codes have never been checked at all.

No live model calls, ever. Every merge below goes to `tests/fake_endpoint.py`,
the same scripted loopback double `tests/test_cli.py` and
`tests/test_web_jobs.py` use, with the replies imported from that module rather
than copied -- two fixtures for one endpoint is how the second one stops
matching the prompts.

Four of the checks here are the ones worth naming, because each guards a
property that looks true from the outside while being false:

**the web path and the command path produce the same report.** If they diverge
the web interface is not the same tool, and the divergence would be invisible to
everybody: both runs succeed, both produce a plausible report, and only a
comparison says they disagree. One merge through `POST /api/v1/runs` and one
through `cli.main`, same endpoint, same documents, reports required to match.

**a served report carries no absolute host path.** `Usage.prompts` is keyed by
the full prompt path (`client.py:458`), so `report.as_dict` genuinely contains
one -- which means the must-fire probe is not a seeded string but the real
thing, asserted present in the job's own report and absent from the one the
server hands out.

**no response carries a key.** Seeded both into the process environment and into
the server's own copy of it, then looked for in the body of every endpoint.

**the stream replays exactly the tail.** An off-by-one in either direction is
invisible on a run that never dropped its connection, which is every run nobody
is debugging.

Run with `python3 tests/test_web_server.py`, or collect with pytest.
"""

from __future__ import annotations

import base64
import contextlib
import inspect
import io
import json
import os
import re
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs. Every request below reaches a real
# loopback socket -- two of them, this server and the scripted endpoint behind
# it -- so this is the module's claim that the only sockets it opens are the
# ones it bound itself; `tests/test_socket_guard.py` asserts every test module
# states it in exactly this shape.
socket_guard.install()

from llossless import cli, config, merge, prompts  # noqa: E402
from llossless.web import api, catalogue, jobs, redact, server  # noqa: E402

from fake_endpoint import FakeEndpoint  # noqa: E402
from test_cli import CLEAN, SOURCE_A, SOURCE_B, Script  # noqa: E402

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# scaffolding
# --------------------------------------------------------------------------

# Long enough that a loaded machine running the whole suite does not fail a
# check about a state transition, short enough that a genuine hang is reported
# as one rather than as a suite that never returns. Same number as
# `tests/test_web_jobs.py` uses, for the same reason.
PATIENCE = 60.0

# A value that could not be anything but a probe, and that no scanner in this
# repository has a reason to recognise: not address-shaped, not key-shaped, and
# not a word that occurs in any document under test. It is seeded as an API key
# and then looked for in every response body.
FAKE_KEY = "probe-value-must-never-be-served-9f2c"

LABELS = ("notes-a.md", "notes-b.md")


def a_submission(**overrides) -> dict:
    """The POST body for a two-document merge. Both models named explicitly.

    `config.from_env` merges `models.local.json` under the environment and a
    developer's own file is untracked, so without both model fields a run here
    would carry whatever model that machine happens to prefer into the
    provenance block of a test that never called one.
    """
    body = {
        "documents": [{"name": LABELS[0], "text": SOURCE_A},
                      {"name": LABELS[1], "text": SOURCE_B}],
        "base": LABELS[0],
        "model": "test-model",
        "merge_model": "test-model",
    }
    body.update(overrides)
    return body


@contextlib.contextmanager
def live_server(**kwargs):
    """A serving `Server` wired to a scripted endpoint. Yields (server, base_url).

    Port 0, and the bound port is read back off the socket: two runs of the
    suite must not be able to collide on a port, and a developer running their
    own `llossless serve` must not be able to make this fail.

    `--structured prompt` for the reason `tests/test_cli.py` pins it: the
    capability probe is the client's business and is tested there, and leaving
    it on would put a negotiation this module does not own inside every
    assertion it makes.
    """
    with FakeEndpoint(Script(**CLEAN)) as endpoint_url, \
            tempfile.TemporaryDirectory() as raw:
        environ = {"LLOSSLESS_BASE_URL": endpoint_url,
                   "LLOSSLESS_STRUCTURED": "prompt",
                   "LLOSSLESS_API_KEY": FAKE_KEY}
        built = server.build(port=0, work_dir=Path(raw) / "work",
                             environ=environ, **kwargs)
        thread = server.background(built)
        try:
            yield built, endpoint_url
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


# The most bytes any response here is read for. A stream has no length and is
# ended by the server closing the connection, so a stream that never ends is
# read forever -- and a socket timeout never fires, because data keeps
# arriving. That is not hypothetical: a seeded off-by-one in `EventLog.since`
# makes the SSE loop re-send its own last frame, and without this cap the check
# that was built to catch it hangs the suite instead of failing it. A hang is
# the one failure a test may not have.
READ_CAP = 256 * 1024


def request(url: str, *, method: str = "GET", payload=None, headers=None,
            raw: bytes | None = None, timeout: float = PATIENCE,
            limit: int = READ_CAP):
    """One HTTP call. Returns (status, headers, body-bytes). Never raises on 4xx.

    An `HTTPError` is a response with a body, and every refusal this module
    asserts about arrives as one; letting it propagate would turn every
    negative check into a `try`/`except` at the call site and make the
    interesting assertion the one in the handler.
    """
    body = raw
    sent = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        sent.setdefault("Content-Type", "application/json")
    call = urllib.request.Request(url, data=body, method=method, headers=sent)
    try:
        with urllib.request.urlopen(call, timeout=timeout) as answer:
            return answer.status, dict(answer.headers), answer.read(limit)
    except urllib.error.HTTPError as refusal:
        return refusal.code, dict(refusal.headers), refusal.read(limit)


def as_json(body: bytes):
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None


def wait_for(predicate, *, timeout: float = PATIENCE) -> bool:
    """Poll until `predicate` holds. False on timeout, never an exception."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return predicate()


def a_finished_run(built, **overrides) -> tuple[str, dict]:
    """Submit, wait, and return (id, the run payload). Fails loudly if it hangs."""
    status, _, body = request(f"{built.url}{api.API_PREFIX}/runs", method="POST",
                              payload=a_submission(**overrides))
    if status != 202:
        check(False, f"the submit was refused with {status}: {body[:300]!r}")
        return "", {}
    job_id = as_json(body)["id"]
    url = f"{built.url}{api.API_PREFIX}/runs/{job_id}"

    def done() -> bool:
        # `or {}` because a body that is not JSON is a *failure to report*,
        # and an `AttributeError` raised here would abort the test module with
        # a traceback instead of letting the check below name what went wrong.
        return (as_json(request(url)[2]) or {}).get("state") in ("done", "failed")

    if not wait_for(done):
        check(False, f"run {job_id} never reached a terminal state")
        return job_id, {}
    return job_id, as_json(request(url)[2])


def sse_events(built, job_id: str, last_event_id=None) -> list[dict]:
    """The stream, read to its end, as the decoded `data:` payloads.

    Read whole rather than incrementally: every job in this module is finished
    before the stream is opened, so `EventLog` is closed, the generator yields
    the tail and returns, and the connection closes on its own. What is being
    asserted is which events came back and in what order, and that is the same
    question either way.
    """
    headers = {} if last_event_id is None else {"Last-Event-ID": str(last_event_id)}
    _, _, body = request(f"{built.url}{api.API_PREFIX}/runs/{job_id}/events",
                         headers=headers, limit=READ_CAP)
    out = []
    for block in body.decode("utf-8").split("\n\n"):
        for line in block.splitlines():
            if line.startswith("data: "):
                out.append(json.loads(line[len("data: "):]))
    return out


# --------------------------------------------------------------------------
# health and config
# --------------------------------------------------------------------------


def test_health_reports_the_version_and_a_credential_by_presence_only() -> None:
    """Must fire and must not fire, on one endpoint.

    The must-not-fire half is the whole point of the endpoint: a provider with
    no variable set must read `configured: false` rather than being absent, so
    an operator whose key is missing is told which variable was looked at. The
    must-fire half is that a key which *is* set reads `true` -- without it the
    endpoint could be hard-coded to `false` and pass every leak check in this
    file.
    """
    with live_server() as (built, _):
        status, _, body = request(f"{built.url}{api.API_PREFIX}/health")
        payload = as_json(body)
        check(status == 200, f"/health answered {status}")
        check(payload.get("api") == api.API_VERSION,
              f"/health must name the API version; got {payload.get('api')!r}")
        check(payload.get("version") == cli.__version__,
              "/health must report the tool's version")
        rows = {row["role"]: row for row in payload.get("providers", [])}
        check(set(rows) == {"default", *config.ROLES},
              f"/health must answer for every role; got {sorted(rows)}")
        configured = rows["default"]
        check(configured["configured"] is True,
              "the default provider's key is set in this server's environment "
              "and /health reports it unconfigured, so the presence check is "
              "not reading anything")
        check(configured["variable"] == config.DEFAULT_KEY_ENV,
              f"/health must name the variable it looked at; got "
              f"{configured['variable']!r}")
        check(FAKE_KEY not in body.decode("utf-8"),
              "/health served the value of the key, not its presence")

    # The other direction, on a server whose environment holds no key at all.
    with FakeEndpoint(Script(**CLEAN)) as endpoint_url, \
            tempfile.TemporaryDirectory() as raw:
        bare = server.build(port=0, work_dir=Path(raw) / "work",
                            environ={"LLOSSLESS_BASE_URL": endpoint_url})
        thread = server.background(bare)
        try:
            payload = as_json(request(f"{bare.url}{api.API_PREFIX}/health")[2])
            rows = {row["role"]: row for row in payload["providers"]}
            check(rows["default"]["configured"] is False,
                  "a server with no key configured must say so; this one "
                  "reported a credential it does not have")
        finally:
            bare.shutdown()
            bare.server_close()
            bare.store.close()
            thread.join(timeout=5)


def test_config_reads_the_enumerations_from_config_and_the_text_from_the_prompts() -> None:
    """The levels are `config`'s, and the copy comes from one table per family.

    A hardcoded list of levels would go stale the day one is added, and a
    hardcoded *description* would go stale the day a level's rules change --
    which is worse, because the list would still be right and the operator
    would be reading a sentence about a level that no longer behaves that way.

    **The fidelity descriptions used to be compared against the prompt
    fragments, and that was the defect.** It answered drift and got
    audience wrong: a prompt is written to the model in the second person, so
    the picker rendered *"you are expected to look a fact up"* and *"you have
    been given a web tool for this run"* at somebody choosing a setting. They
    now come from `config.FIDELITY_SHAPES`, which is written for a reader and
    is the same table `--fidelity`'s help renders from -- one source for the
    two surfaces that face a person, which is the drift answer without the
    audience mistake. The title policies still read from their prompt, because
    that fragment is a rule about the merged document rather than an
    instruction in the second person.
    """
    with live_server() as (built, _):
        status, _, body = request(f"{built.url}{api.API_PREFIX}/config")
        payload = as_json(body)
    check(status == 200, f"/config answered {status}")

    levels = payload["fidelity"]["levels"]
    check([entry["value"] for entry in levels] == list(config.FIDELITY_LEVELS),
          f"/config must list config.FIDELITY_LEVELS in order; got "
          f"{[entry['value'] for entry in levels]}")
    check(payload["fidelity"]["default"] == config.DEFAULT_FIDELITY,
          "/config must name the default fidelity level")
    for entry in levels:
        check(entry["name"] == config.fidelity_name(entry["value"]),
              f"{entry['value']}: /config must carry the published name beside "
              f"the wire value, or a picker shows a word the API refuses")
        # **The copy is not in this payload and must not be**, which is the
        # one place the fidelity picker differs from the depth picker below. A
        # description is prose shown to a person, the page is translated, and
        # an English paragraph arriving from an API into a German page is the
        # same defect in a second language.
        # `retrieves` is a flag, not copy: the effort card warns at the
        # level that looks facts up without the page learning its name.
        # `adds` is the same kind of flag: whether this level ever
        # hands the merge the `additions` field at all, the same test
        # `merge.merge_schema` itself reads.
        check(set(entry) == {"value", "name", "default", "retrieves", "adds"},
              f"{entry['value']}: /config serves the enumeration and not the "
              f"copy; got {sorted(entry)}")
        check(entry["retrieves"] is (entry["value"] == config.SOURCED),
              f"{entry['value']}: only {config.SOURCED} retrieves; got "
              f"{entry['retrieves']!r}")
        check(entry["adds"] is bool(merge.ADDS[entry["value"]]),
              f"{entry['value']}: adds must mirror merge.ADDS; got "
              f"{entry['adds']!r}")

    policies = payload["title_policy"]["policies"]
    check([entry["value"] for entry in policies] == list(config.TITLE_POLICIES),
          "/config must list config.TITLE_POLICIES")
    for entry in policies:
        wanted = api.first_paragraph(prompts.load(f"title/{entry['value']}").text)
        check(entry["explains"] == wanted,
              f"{entry['value']}: the policy explanation served is not the "
              f"opening of prompts/title/{entry['value']}.md")

    depths = payload["verify_depth"]["depths"]
    check([entry["value"] for entry in depths] == list(config.VERIFY_DEPTHS),
          f"/config must list config.VERIFY_DEPTHS in order; got "
          f"{[entry['value'] for entry in depths]}")
    check(payload["verify_depth"]["default"] == config.DEFAULT_VERIFY_DEPTH,
          "/config must name the default verification depth")
    for entry in depths:
        shape = config.VERIFY_DEPTH_SHAPES[entry["value"]]
        check(entry["explains"] == shape.explains,
              f"{entry['value']}: the explanation served is not the one "
              f"`--verify-depth`'s help renders, so the picker and the command "
              f"line can describe the same depth differently")
        check(entry["detects_invention"] is shape.detects_invention,
              f"{entry['value']}: the page decides whether a clean result means "
              f"'nothing was invented' from this flag, and it is wrong")
        # The call counts, so the page can price the depth for the documents
        # actually loaded rather than for an assumed two -- and the flag that
        # says whether their sum is the price or its floor. `full` batches
        # both verify passes at 25 claims, so a page that rendered its figure
        # as a quote would understate a long merge. Asserted as a whole
        # dict so a fourth key cannot arrive unnoticed.
        check(entry["calls"] == {"fixed": shape.fixed_calls,
                                 "per_source": shape.calls_per_source,
                                 "exact": shape.exact_calls},
              f"{entry['value']}: the call counts served are not the table's: "
              f"{entry['calls']}")

    # **The measured figure is the catalogue's `verify_depth` block**,
    # served whole as `quality_delta` beside the rows, as `catalogue.load`
    # validated it with its run, artefacts and derived_by. The rows themselves
    # still carry no detection figure: what a depth does comes from `config`,
    # and a measurement of one model on one test set stays in the one block
    # that carries its provenance. With no block the field says "unmeasured"
    # -- `test_the_depth_delta_falls_back_to_unmeasured_without_a_block`.
    block = catalogue.load().get("verify_depth")
    check(isinstance(block, dict)
          and payload["verify_depth"]["quality_delta"] == block,
          f"/config must serve the catalogue's verify_depth block as "
          f"quality_delta; got {str(payload['verify_depth'].get('quality_delta'))[:200]}")
    numeric = sorted(
        f"{entry['value']}.{key}"
        for entry in depths for key, value in entry.items()
        if key != "calls" and isinstance(value, (int, float))
        and not isinstance(value, bool))
    check(not numeric,
          f"a depth row carries the number(s) {numeric} beside the call counts; "
          f"the only quantity measured about this choice is what it costs in "
          f"calls, and anything else here is a figure standing in for a "
          f"benchmark that has not been run")

    check(payload["catalogue"] == catalogue.load(),
          "/config must serve the model catalogue the loader validates, whole")
    check(payload["limits"]["min_documents"] == merge.MIN_SOURCES
          and payload["limits"]["max_documents"] == merge.MAX_SOURCES,
          "/config must state the arity the engine enforces, not a copy of it")
    check(payload["limits"]["max_body_bytes"] == api.MAX_BODY_BYTES,
          "/config must state the body cap a client will be refused at")



def test_the_depth_delta_falls_back_to_unmeasured_without_a_block() -> None:
    """No `verify_depth` block, no figure: the field says "unmeasured".

    A fork's own catalogue, or one written before the benchmark, has nothing
    to serve here, and the failure to avoid is not a wrong number but a zero
    or a blank that a reader completes as "no difference". Built from
    the shipped catalogue with the block taken out and nothing else changed,
    so the only thing that can move the field is the block's absence.
    """
    data = json.loads(catalogue.DEFAULT_PATH.read_text(encoding="utf-8"))
    check("verify_depth" in data, "the shipped catalogue has no verify_depth "
                                  "block, so removing it below proves nothing")
    del data["verify_depth"]
    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "catalogue.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        with live_server(catalogue_path=path) as (built, _):
            status, _, body = request(f"{built.url}{api.API_PREFIX}/config")
    payload = as_json(body)
    check(status == 200, f"/config answered {status} over a catalogue with no "
                         f"verify_depth block")
    check(payload["verify_depth"]["quality_delta"] == "unmeasured",
          f"with no verify_depth block the quality difference is unmeasured "
          f"and must say so; got {payload['verify_depth'].get('quality_delta')!r}")

# --------------------------------------------------------------------------
# the run lifecycle
# --------------------------------------------------------------------------


def test_a_submitted_run_is_accepted_with_202_a_location_and_an_id() -> None:
    """202 rather than 201, and the id is the contract's whole surface.

    201 would tell a client the result exists at `Location`, and it does not --
    a merge takes between 23 and 4,559 seconds, measured over the graded run records (withheld with the paper), and
    the only thing that exists at submit time is a record that the work was
    accepted.
    """
    with live_server() as (built, _):
        status, headers, body = request(f"{built.url}{api.API_PREFIX}/runs",
                                        method="POST", payload=a_submission())
        payload = as_json(body)
        check(status == 202, f"a submit must answer 202; got {status}: {body[:300]!r}")
        check(api.JOB_ID.match(payload.get("id") or ""),
              f"the id must be uuid4 hex; got {payload.get('id')!r}")
        check(headers.get("Location") == f"{api.API_PREFIX}/runs/{payload['id']}",
              f"a submit must point at the run it created; got "
              f"{headers.get('Location')!r}")
        check(payload["state"] in (jobs.QUEUED, jobs.RUNNING),
              f"a fresh run is queued or running; got {payload['state']!r}")
        check(payload["documents"] == len(LABELS),
              "the accepted run must count the documents it took")

        listed = as_json(request(f"{built.url}{api.API_PREFIX}/runs")[2])
        check([entry["id"] for entry in listed["runs"]] == [payload["id"]],
              "the run list must contain the run that was just accepted")
        check(all("report" not in entry for entry in listed["runs"]),
              "the run list must not carry a report in every row; it is what a "
              "page refreshes, and the report is its own route")


def test_a_finished_run_reports_its_outcome_and_serves_its_three_artefacts() -> None:
    """The documented shape of every endpoint that exists only once a run ends."""
    with live_server() as (built, _):
        job_id, payload = a_finished_run(built)
        if not payload:
            return
        check(payload["state"] == jobs.DONE,
              f"the scripted merge must finish clean; it is {payload['state']!r} "
              f"({payload.get('error')!r})")
        check(payload["exit_code"] == 0,
              f"the scripted merge exits 0; got {payload['exit_code']!r}")
        for field in ("created_at", "started_at", "finished_at"):
            check(isinstance(payload.get(field), float),
                  f"a finished run must carry {field} as a timestamp")
        check(payload["report"]["command"] == "merge",
              "a finished run must carry its report")

        base = f"{built.url}{api.API_PREFIX}/runs/{job_id}"
        status, headers, body = request(f"{base}/merged")
        check(status == 200 and headers["Content-Type"].startswith("text/markdown"),
              f"the merged document is served as markdown; got {status} "
              f"{headers.get('Content-Type')!r}")
        check(payload["report"]["merged_written_to"] == jobs.MERGED_MD,
              f"the report must name the merged file as a bare name, not a "
              f"path; got {payload['report']['merged_written_to']!r}")
        check(body.strip() and b"relay" in body,
              f"the merged document served is not the scripted merge: "
              f"{body[:120]!r}")

        status, headers, body = request(f"{base}/report.html")
        check(status == 200 and headers["Content-Type"].startswith("text/html"),
              f"the HTML report is served as HTML; got {status}")
        check(b"<html" in body.lower() and b"<title>LLossless " in body,
              "the HTML report must be a page, not a stub")


def test_an_artefact_asked_for_too_early_says_so_rather_than_404ing() -> None:
    """Must fire. "not yet", "never will be" and "not any more" are three answers.

    A single 404 for all three is the failure: an operator polling a running job
    would be told their run does not exist, which is the same thing they would
    be told for a typo in the id.
    """
    with live_server() as (built, _):
        status, _, body = request(f"{built.url}{api.API_PREFIX}/runs",
                                  method="POST", payload=a_submission())
        job_id = as_json(body)["id"]
        base = f"{built.url}{api.API_PREFIX}/runs/{job_id}"
        # Racy by nature -- the merge may already have finished -- so both the
        # early answer and the finished one are accepted, and what is asserted
        # is that the early answer is never a 404.
        status, _, body = request(f"{base}/merged")
        check(status in (200, 409),
              f"an artefact on a run in flight must answer 409 (or 200 if it "
              f"finished first), never {status}: {body[:200]!r}")
        if status == 409:
            check(as_json(body)["error"]["code"] == "not_finished",
                  "a 409 here must say the run is not finished")

        if not wait_for(lambda: (as_json(request(base)[2]) or {}).get("state")
                        == jobs.DONE):
            check(False, "the run never finished")
            return
        check(request(f"{base}/merged")[0] == 200,
              "and the same URL must serve once the run is done")


def test_a_deleted_run_is_gone_and_deleting_it_again_still_answers() -> None:
    """DELETE is idempotent, and the second call is not an error.

    The operator asked for the run to be gone and it is gone. A 404 on the
    retry would tell a client whose connection dropped that its first attempt
    failed, which is the one thing that is certainly untrue.
    """
    with live_server() as (built, _):
        job_id, payload = a_finished_run(built)
        if not payload:
            return
        base = f"{built.url}{api.API_PREFIX}/runs/{job_id}"
        status, _, body = request(base, method="DELETE")
        check(status == 204 and body == b"",
              f"DELETE must answer 204 with no body; got {status} {body[:200]!r}")
        check(request(base)[0] == 404,
              "a deleted run must not be looked up again")
        check(request(base, method="DELETE")[0] == 204,
              "deleting a run twice must answer the same way twice")
        listed = as_json(request(f"{built.url}{api.API_PREFIX}/runs")[2])
        check(listed["runs"] == [],
              f"a deleted run must leave the list; it holds {listed['runs']}")


# --------------------------------------------------------------------------
# the equivalence check -- the most important one here
# --------------------------------------------------------------------------


def test_the_web_path_and_the_command_path_produce_the_same_report() -> None:
    """Same documents, same endpoint, one merge through each. Reports must agree.

    If these two diverge the web interface is not the same tool, and nothing
    else in this suite would say so: both runs succeed, both produce a report
    that looks right, and the divergence is only visible in a comparison.
    `tests/test_web_jobs.py` makes the same assertion one layer down, between
    `jobs.run_merge` and `cli.one_merge`; this one is over HTTP against
    `cli.main`, because the defects this project has actually shipped lived on
    the command path and not in the function underneath it.

    Four keys are set aside, each for a stated reason rather than for
    convenience:

      generated_at       a wall clock
      duration_seconds   a stopwatch
      merged_written_to  deliberately different -- the CLI writes where `-o`
                         pointed and the web path writes a bare name into a
                         directory it owns
      documents          also deliberately different, and asserted separately
                         below: the CLI's values are the paths it was given and
                         the web path's are the labels the submitter chose
      latency_ms         on each ledger row, a stopwatch per call; taken
                         off both sides after asserting every row carries it,
                         with the rest of its time split beside it
      answering_seconds, excluded, discarded_calls, unruled
                         the run's own time accounting: stopwatches

    Both sides are passed through `redact.report` before comparing. The served
    copy has already been through it, so comparing a raw report against a
    redacted one would fail on the prompt paths and say nothing about whether
    the two runs agreed.
    """
    volatile = ("generated_at", "duration_seconds", "answering_seconds",
                "excluded", "discarded_calls", "unruled")
    stopwatches = ("latency_ms", "attempts", "answer_ms", "failed_ms",
                   "waited_ms", "ttfb_ms")
    with live_server() as (built, endpoint_url):
        job_id, served = a_finished_run(built)
        if not served or "report" not in served:
            check(False, f"the web run produced no report: {served}")
            return

        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw)
            for label, text in zip(LABELS, (SOURCE_A, SOURCE_B)):
                (home / label).write_text(text, encoding="utf-8")
            report_path = home / "report.json"
            was = os.environ.get("LLOSSLESS_CACHE_DIR")
            os.environ["LLOSSLESS_CACHE_DIR"] = str(home / "cache")
            out, err = io.StringIO(), io.StringIO()
            try:
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    code = cli.main([
                        "merge", str(home / LABELS[0]), str(home / LABELS[1]),
                        "--base", str(home / LABELS[0]),
                        "--json", str(report_path),
                        "--base-url", endpoint_url,
                        "--model", "test-model", "--merge-model", "test-model",
                        "--structured", "prompt", "--no-cache",
                    ])
            finally:
                if was is None:
                    os.environ.pop("LLOSSLESS_CACHE_DIR", None)
                else:
                    os.environ["LLOSSLESS_CACHE_DIR"] = was
            check(code == 0,
                  f"the command-line merge must succeed or the comparison is "
                  f"against nothing; exit {code}, stderr {err.getvalue()[-300:]!r}")
            if code != 0:
                return
            theirs = redact.report(json.loads(report_path.read_text(encoding="utf-8")))

    mine = dict(served["report"])
    theirs = dict(theirs)
    # Another field only the web side ever carries, popped the same way and
    # for the same reason: `cli_equivalent` is `web/cli_render.render`'s
    # block, and a plain `llossless merge` has no request behind it to render
    # one from. Asserted present and shaped, not merely absent from the diff.
    mine_cli_equivalent = mine.pop("cli_equivalent", None)
    check(isinstance(mine_cli_equivalent, dict)
          and isinstance(mine_cli_equivalent.get("command"), str)
          and mine_cli_equivalent["command"].startswith("llossless merge "),
          f"a finished web run must carry a rendered CLI-equivalent command; "
          f"got {mine_cli_equivalent!r}")
    check("cli_equivalent" not in theirs,
          "a plain `llossless merge` has no request to render a CLI equivalent from")
    # The one field the paths differ on by design, taken off the web
    # side only after asserting it is there: the server chose each role's
    # route from a row somebody picked and records how each was billed, and
    # the command line was handed an address and chose nothing.
    endpoint = dict(mine["provenance"].get("endpoint") or {})
    check(set(endpoint.pop("billed", {}) or {}) == {"merge", "decompose", "verify"},
          f"the web run does not record how each role was billed: "
          f"{mine['provenance'].get('endpoint')}")
    check("billed" not in (theirs["provenance"].get("endpoint") or {}),
          "the command line recorded a route it never chose")
    mine["provenance"] = dict(mine["provenance"], endpoint=endpoint)
    check(sorted(Path(path).name for path in theirs["documents"].values())
          == sorted(mine["documents"].values()),
          f"the two runs must name the same documents; the command line has "
          f"{theirs['documents']} and the web path has {mine['documents']}")
    for payload in (mine, theirs):
        payload.pop("documents", None)
        payload.pop("merged_written_to", None)
        payload["provenance"] = {key: value
                                 for key, value in payload["provenance"].items()
                                 if key not in volatile}
        rows = payload["provenance"].get("ledger") or []
        check(rows and all(isinstance(row.get("latency_ms"), int) for row in rows),
              f"both runs are live, so every ledger row carries its call's time: "
              f"{[row.get('latency_ms') for row in rows]}")
        payload["provenance"]["ledger"] = [
            {k: v for k, v in row.items() if k not in stopwatches} for row in rows]
    differing = sorted(key for key in set(mine) | set(theirs)
                       if mine.get(key) != theirs.get(key))
    check(not differing,
          f"the web path and `llossless merge` disagree on "
          f"{', '.join(differing)}; the web interface is not running the same "
          f"tool")


# --------------------------------------------------------------------------
# redaction
# --------------------------------------------------------------------------


def test_a_served_report_carries_no_absolute_host_path() -> None:
    """Must fire on the real positive, and must not fire on the cleaned copy.

    The probe is not seeded. `Usage.prompts` is keyed by the full prompt path
    (`client.py:458`), so the job's own report genuinely contains one, and that
    is asserted first -- without it this check would pass on a report that never
    had a path in it and would prove nothing about the redaction. The served
    copy is then required not to contain it, and to name the prompt by a
    relative name instead, because four provenance rows reading `<redacted>`
    would have protected the same thing and told the reader nothing.
    """
    wanted = str(prompts.load("merge").path)
    with live_server() as (built, _):
        job_id, served = a_finished_run(built)
        if not served:
            return
        job = built.store.get(job_id)
        held = json.dumps(job.report)
        check(wanted in held,
              f"the job's own report must contain the absolute prompt path, or "
              f"there is nothing here to redact and this check is blind; "
              f"looked for {wanted!r}")

        body = request(f"{built.url}{api.API_PREFIX}/runs/{job_id}")[2].decode("utf-8")
        check(wanted not in body,
              "the served run carries the absolute prompt path; redaction did "
              "not reach the report on the way out")
        check("prompts/merge.md" in body,
              "the served report must still name which prompt ran; a row that "
              "is only a mark cannot be checked against its own digest")

        page = request(f"{built.url}{api.API_PREFIX}/runs/{job_id}/report.html")[2]
        check(wanted not in page.decode("utf-8"),
              "the HTML report carries the absolute prompt path")

        home = str(Path.home())
        if len(home) > redact.MIN_ROOT:
            for what, text in (("run", body), ("html", page.decode("utf-8"))):
                check(home not in text,
                      f"the served {what} names this host's home directory")


def test_the_published_redactor_clears_the_key_under_both_names() -> None:
    """`LLOSSLESS_API_KEY`'s value is scrubbed, and so is the old name's.

    The rename made `LLOSSLESS_API_KEY` the variable a key is
    read from and left `scripts/stream_redact.py` listing only
    `CLAIMCHECK_API_KEY`, so a key set under the new name passed through the
    redactor unchanged. The old name is no longer read, but a shell can
    still export it and its value is still a key, so the redactor keeps it.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    import stream_redact  # noqa: E402
    for name in ("LLOSSLESS_API_KEY", "CLAIMCHECK_API_KEY"):
        value = "probe-" + name.lower() + "-" + "q" * 20
        check(value in stream_redact.literal_forms({name: value}),
              f"scripts/stream_redact.py does not treat {name}'s value as a secret")


def test_the_redaction_clears_a_path_the_published_redactor_also_clears() -> None:
    """One rule, two implementations, and the agreement is checked not assumed.

    `scripts/stream_redact.py` cannot be imported by the shipped server --
    `scripts/` is not in the wheel and that module reaches into
    `tests/test_client.py` for its patterns at call time -- so
    `llossless.web.redact` states the rule a second time, in a form that needs
    no home-directory literal, which the release scanner would
    flag in a published source file anyway, and which is why neither this file
    nor `redact.py` contains one. Two statements of one rule is the cost, and
    this is what stops them being two rules: a real path that the published
    redactor cleans must come back cleaned here too.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    import stream_redact  # noqa: E402

    # Built from this process's own home directory rather than written out: a
    # home-directory literal in a published file is what
    # the release scanner scans for, and the operator ruled out
    # disguising one to get past a scanner. This is the real directory, so the
    # probe is the shape the published redactor actually recognises whenever
    # this host has a home of that shape -- and the assertion below refuses to
    # pass if it does not.
    under_home = str(Path.home() / "a-checkout" / "prompts" / "merge.md")
    check(stream_redact.scrub(under_home) != under_home,
          f"scripts/stream_redact.py does not clean {under_home!r}, so the "
          f"comparison below is between two silences and proves nothing about "
          f"either rule")
    check(redact.text(under_home) != under_home
          and str(Path.home()) not in redact.text(under_home),
          f"the published redactor cleans {under_home!r} and this one leaves "
          f"it; the two rules have come apart, and the server is the one "
          f"serving reports")

    # And the direction that is deliberately *not* symmetric. The prompt path
    # on this machine may be anywhere -- under `/tmp` when the suite runs from
    # a copied tree, under `/srv` or `/opt` on a deployed server -- and
    # `stream_redact`'s home-only rule reaches none of those. Covering them is
    # the whole reason `llossless.web.redact` states the rule again instead of
    # importing it, so it is asserted rather than described.
    real = str(prompts.load("merge").path)
    check(redact.text(real) != real and real not in redact.text(real),
          f"llossless.web.redact left the real prompt path in place: {real!r}")
    # And the must-not-fire half: ordinary prose, and a path inside a document
    # that belongs to nobody on this host, must come back untouched.
    for innocent in ("The audit log is written to /var/log/relay.",
                     "prompts/merge.md", "a sentence with no path in it"):
        check(redact.text(innocent) == innocent,
              f"redaction ate ordinary text: {innocent!r} -> "
              f"{redact.text(innocent)!r}")


def test_the_merged_document_is_served_exactly_as_written() -> None:
    """Must not fire. The product is not redacted, and that is on purpose.

    A merged document that happened to contain one of this host's directories
    would come back with a hole in it, and a merge tool that silently edits its
    own output has done something worse than disclose a directory name. This is
    the assertion that keeps that decision from being quietly reversed by
    somebody extending redaction to "every response".
    """
    with live_server() as (built, _):
        job_id, served = a_finished_run(built)
        if not served:
            return
        job = built.store.get(job_id)
        body = request(f"{built.url}{api.API_PREFIX}/runs/{job_id}/merged")[2]
        check(body.decode("utf-8") == job.run.merged,
              "the merged document served differs from the one the run "
              "produced; the product must leave byte for byte")


# --------------------------------------------------------------------------
# keys
# --------------------------------------------------------------------------


def test_no_response_body_carries_a_key() -> None:
    """Seeded in the real environment, looked for in every endpoint's body.

    The must-fire half is at the bottom and is about the *search*, not about
    the server: a check that looks for a string nothing could ever contain
    passes whatever the code does, and this one has to be shown capable of
    saying yes.
    """
    was = os.environ.get(config.DEFAULT_KEY_ENV)
    os.environ[config.DEFAULT_KEY_ENV] = FAKE_KEY
    try:
        with live_server() as (built, _):
            job_id, served = a_finished_run(built)
            if not served:
                return
            root = f"{built.url}{api.API_PREFIX}"
            seen = []
            for url in (f"{root}/health", f"{root}/config", f"{root}/runs",
                        f"{root}/runs/{job_id}", f"{root}/runs/{job_id}/merged",
                        f"{root}/runs/{job_id}/report.html",
                        f"{root}/runs/{job_id}/events",
                        f"{root}/runs/not-an-id", f"{root}/nothing-here",
                        f"{built.url}/"):
                body = request(url)[2]
                seen.append((url, body))
                check(FAKE_KEY.encode("utf-8") not in body,
                      f"{url} served the API key out of the environment")
    finally:
        if was is None:
            os.environ.pop(config.DEFAULT_KEY_ENV, None)
        else:
            os.environ[config.DEFAULT_KEY_ENV] = was

    check(len(seen) == 10, f"only {len(seen)} endpoints were searched")
    # Must fire. The same search, over a body that does carry the value.
    planted = json.dumps({"env": {config.DEFAULT_KEY_ENV: FAKE_KEY}}).encode("utf-8")
    check(FAKE_KEY.encode("utf-8") in planted,
          "the key search cannot find a key that is right in front of it, so "
          "every negative above is a negative about the search")


# --------------------------------------------------------------------------
# refusals
# --------------------------------------------------------------------------


def test_a_traversal_shaped_id_is_refused_by_shape() -> None:
    """Must fire, with a real id beside it as the must-not-fire case.

    By shape and not by `os.path`. A check that asked "does this resolve inside
    the work directory" would depend on symlinks, on the separator and on
    whether the directory existed; `api.JOB_ID` depends on none of those.
    """
    with live_server() as (built, _):
        job_id, served = a_finished_run(built)
        if not served:
            return
        root = f"{built.url}{api.API_PREFIX}"
        # One path segment each, so the route the request lands on is the same
        # one a real id lands on and the answer is about the *id*. A refusal
        # here has to be `bad_id`, not `no_run`: an id check that accepted
        # anything would still 404 on every one of these, because none of them
        # is in the index -- and a test that took 404 for an answer would pass
        # against no id validation at all. That is not hypothetical; it is what
        # this check did before a seeded `JOB_ID = ".*"` went uncaught.
        for shape in ("..", "....", "%2e%2e", "%2e%2e%2f%2e%2e", "~",
                      job_id.upper(), job_id[:-1], job_id + "0", "0" * 32 + "x"):
            for suffix in ("", "/merged", "/report.html", "/events"):
                status, _, body = request(f"{root}/runs/{shape}{suffix}")
                payload = as_json(body) or {}
                check(status == 400,
                      f"/runs/{shape}{suffix} answered {status}; an id that is "
                      f"not 32 hex characters must be refused by shape")
                check((payload.get('error') or {}).get("code") == "bad_id",
                      f"/runs/{shape}{suffix} was refused as "
                      f"{(payload.get('error') or {}).get('code')!r}, not by shape; "
                      f"a 404 here would mean nothing looked at the id at all")
        # A well-formed id that is simply not here is the other answer, and it
        # has to be a different one.
        absent = "0" * 32
        status, _, body = request(f"{root}/runs/{absent}")
        check(status == 404 and ((as_json(body) or {}).get("error") or {}).get("code")
              == "no_run",
              f"a well-formed id that is not in the index must be `no_run`; got "
              f"{status} {body[:150]!r}")
        # And a traversal that changes the *shape of the path* is not a route.
        for escape in ("../../etc/passwd/merged", f"{job_id}/../{job_id}/merged"):
            status, _, body = request(f"{root}/runs/{escape}")
            check(status == 404,
                  f"/runs/{escape} answered {status}; nothing outside the "
                  f"contract's routes is served")
        # Must not fire: the real id, same routes, all served.
        for suffix in ("", "/merged", "/report.html", "/events"):
            check(request(f"{root}/runs/{job_id}{suffix}")[0] == 200,
                  f"the real id was refused at {suffix or '/'}, so the shape "
                  f"check above is refusing everything")


def test_an_oversized_body_is_refused_with_413() -> None:
    """Refused on the declared length, and an ordinary body still accepted.

    The must-not-fire half is not decoration: a cap implemented as "refuse
    every POST" would pass the first assertion and fail the tool.
    """
    with live_server() as (built, _):
        url = f"{built.url}{api.API_PREFIX}/runs"
        payload = a_submission()
        payload["documents"][0]["text"] = "x" * (api.MAX_BODY_BYTES + 1024)
        status, _, body = request(url, method="POST", payload=payload)
        check(status == 413,
              f"an oversized body must be refused with 413; got {status}")
        error = as_json(body)
        check(error and error["error"]["code"] == "body_too_large",
              f"a 413 must say why; got {body[:200]!r}")
        check(request(url, method="POST", payload=a_submission())[0] == 202,
              "an ordinary body must still be accepted, or the cap is a ban")
        check(len(as_json(request(url)[2])["runs"]) == 1,
              "the refused submit must not have created a run")


def test_a_cross_origin_or_non_json_submit_is_refused() -> None:
    """Origin against Host on the mutating verbs, and JSON or nothing.

    Both halves of the CSRF defence, and the second is the one that does the
    work: a cross-origin form can send three content types and JSON is not one
    of them, so requiring JSON means a page that wants to post here has to make
    a preflighted request -- which arrives with an `Origin` the first half then
    refuses.
    """
    with live_server() as (built, _):
        url = f"{built.url}{api.API_PREFIX}/runs"
        status, _, body = request(url, method="POST", payload=a_submission(),
                                  headers={"Origin": "http://evil.example"})
        check(status == 403 and as_json(body)["error"]["code"] == "cross_origin",
              f"a POST from another origin must be refused; got {status}")

        status, _, body = request(
            url, method="POST", raw=json.dumps(a_submission()).encode("utf-8"),
            headers={"Content-Type": "text/plain"})
        check(status == 415 and as_json(body)["error"]["code"] == "not_json",
              f"a submit that is not declared JSON must be refused; got {status}")

        # Must not fire: the server's own origin, and a DELETE from it.
        status, _, body = request(url, method="POST", payload=a_submission(),
                                  headers={"Origin": built.url})
        check(status == 202,
              f"a same-origin POST must be accepted; got {status} {body[:200]!r}")
        job_id = as_json(body)["id"]
        check(request(f"{url}/{job_id}", method="DELETE",
                      headers={"Origin": built.url})[0] == 204,
              "a same-origin DELETE must be accepted")


def test_a_host_header_that_is_not_loopback_is_refused() -> None:
    """The DNS-rebinding guard, on a read as well as on a write.

    Binding `127.0.0.1` stops a packet from another machine. It does nothing
    about a page in the operator's own browser whose hostname resolves here
    after the first response -- that request is same-origin, carries no
    `Origin`, and is distinguished only by the `Host` it names.
    """
    with live_server() as (built, _):
        url = f"{built.url}{api.API_PREFIX}/health"
        status, _, body = request(url, headers={"Host": "attacker.example"})
        check(status == 403 and as_json(body)["error"]["code"] == "host_not_loopback",
              f"a request naming another host must be refused; got {status}")
        for allowed in ("127.0.0.1", f"localhost:{built.port}", "[::1]"):
            check(request(url, headers={"Host": allowed})[0] == 200,
                  f"Host: {allowed} is a loopback name and must be served")


def test_a_malformed_or_unknown_submit_field_is_refused_with_a_reason() -> None:
    """An unknown field is refused, not ignored. Must fire and must not fire.

    Ignored, a `titlepolicy` typo runs at the default, succeeds, and the
    operator is never told the setting they chose was not the setting that ran.
    """
    with live_server() as (built, _):
        url = f"{built.url}{api.API_PREFIX}/runs"
        cases = [
            ({"documents": [], "base": None}, "bad_arity"),
            ({"titlepolicy": "keep-base"}, "unknown_field"),
            ({"fidelity": "extremely"}, "bad_fidelity"),
            # Refused at submit rather than at resolve. `config.from_env` would
            # refuse it too, one call later and after a job id exists -- and a
            # depth is the setting where "it ran at the default instead" is
            # the expensive direction to be wrong in.
            ({"verify_depth": "shallow"}, "bad_verify_depth"),
            ({"title_policy": "invent-one"}, "bad_title_policy"),
            ({"base": "not-a-document.md"}, "refused"),
            ({"documents": [{"name": "a.md", "text": " "},
                            {"name": "b.md", "text": "x"}]}, "refused"),
            ({"documents": [{"name": "a.md", "text": "x"},
                            {"name": "a.md", "text": "y"}]}, "duplicate_document"),
            ({"documents": [{"name": "a\nb.md", "text": "x"},
                            {"name": "b.md", "text": "y"}]}, "bad_documents"),
            # The one that must never be accepted at any spelling: a request
            # aiming this server, and the operator's key, at a host of the
            # submitter's choosing.
            ({"LLOSSLESS_BASE_URL": "http://elsewhere.example"}, "unknown_field"),
        ]
        for overrides, wanted in cases:
            payload = a_submission()
            payload.update(overrides)
            if "base" in overrides and overrides["base"] is None:
                payload.pop("base")
            status, _, body = request(url, method="POST", payload=payload)
            error = as_json(body) or {}
            check(status == 400,
                  f"{overrides} must be refused with 400; got {status}")
            check((error.get('error') or {}).get("code") == wanted,
                  f"{overrides} must be refused as {wanted}; got "
                  f"{(error.get('error') or {}).get('code')!r} -- {body[:200]!r}")

        status, _, body = request(url, method="POST", raw=b"{not json",
                                  headers={"Content-Type": "application/json"})
        check(status == 400 and as_json(body)["error"]["code"] == "bad_json",
              f"a body that is not JSON must be refused as such; got {status}")
        # Must not fire.
        check(request(url, method="POST", payload=a_submission())[0] == 202,
              "a well-formed submit must still be accepted")


@contextlib.contextmanager
def vendor_server(typed: str):
    """A server whose OpenAI provider is a loopback fake with no `/api/ps`.

    The fake answers `/api/ps` with 404, which is what every vendor answers, so
    a model the catalogue does not know has no window unless one is stated.
    The server's own endpoint is a second fake that reports one, loaded with
    the typed id, for the case where the field is optional. Yields
    (server, vendor fake, own fake).
    """
    vendor = FakeEndpoint(Script(**CLEAN), ps_status=404)
    own = FakeEndpoint(Script(**CLEAN), loaded=(typed,))
    with vendor as vendor_url, own as own_url, \
            tempfile.TemporaryDirectory() as raw:
        environ = {"LLOSSLESS_BASE_URL": own_url,
                   "LLOSSLESS_PROVIDER_URL_OPENAI": vendor_url,
                   "OPEN_AI_API_KEY": FAKE_KEY,
                   "LLOSSLESS_STRUCTURED": "prompt"}
        built = server.build(port=0, work_dir=Path(raw) / "work",
                             environ=environ)
        thread = server.background(built)
        try:
            yield built, vendor, own
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


def finished(built, job_id: str) -> dict:
    """The run payload once it is terminal, or {} with a failure recorded."""
    url = f"{built.url}{api.API_PREFIX}/runs/{job_id}"
    if not wait_for(lambda: (as_json(request(url)[2]) or {}).get("state")
                    in (jobs.DONE, jobs.FAILED)):
        check(False, f"run {job_id} never reached a terminal state")
        return {}
    return as_json(request(url)[2]) or {}


def test_a_typed_vendor_id_runs_on_a_stated_window_and_is_refused_without_one() -> None:
    """A typed id sent to a vendor states its window, or is refused before any call.

    A vendor exposes no `/api/ps` and a model the catalogue does not know
    carries no window, so the merge ran and every decompose step refused with
    `WindowUnmeasurable`, unless the server set `LLOSSLESS_WINDOW`. The
    request now carries `window`, the way `--window` states it on the command
    line, and the server refuses at submit where nothing supplies one.

    Driven over HTTP against a loopback OpenAI-shaped fake: without a window,
    a 400 naming the field and no request at the fake; with one, every step
    completes and the run records the window as stated.
    """
    typed = "gpt-typed-not-in-the-catalogue"
    with vendor_server(typed) as (built, vendor, own):
        runs = f"{built.url}{api.API_PREFIX}/runs"
        config_payload = as_json(request(f"{built.url}{api.API_PREFIX}/config")[2]) or {}
        rows = {row["name"]: row for row in
                (config_payload.get("endpoints") or {}).get("providers") or []}
        check(rows.get("openai", {}).get("window_required") is True,
              f"the page must be told the OpenAI endpoint needs a stated "
              f"window: {rows.get('openai')}")
        check(rows.get("self-hosted", {}).get("window_required") is False,
              f"and that a self-hosted one does not: {rows.get('self-hosted')}")
        limits = config_payload.get("limits") or {}
        check((limits.get("min_window"), limits.get("max_window"))
              == (jobs.STATED_WINDOW_MIN, jobs.STATED_WINDOW_MAX),
              f"the page must be served the bounds the server checks: {limits}")

        # Must fire: no window, refused at submit, nothing sent.
        typed_body = a_submission(model=typed, merge_model=typed, endpoint="openai")
        status, _, body = request(runs, method="POST", payload=typed_body)
        error = (as_json(body) or {}).get("error") or {}
        check(status == 400 and error.get("code") == "refused",
              f"a typed vendor id with no window must be refused at submit; "
              f"got {status} {body[:300]!r}")
        check("window field" in str(error.get("message")),
              f"the refusal must name the field: {error.get('message')!r}")
        check(vendor.requests == [] and vendor.gets == [],
              f"nothing may reach the endpoint before the refusal: "
              f"{len(vendor.requests)} call(s), gets {vendor.gets}")

        # A figure outside the bounds, and one that is not a number.
        for bad in (100, "200000", 4096.5, True):
            status, _, body = request(runs, method="POST",
                                      payload=dict(typed_body, window=bad))
            code = ((as_json(body) or {}).get("error") or {}).get("code")
            check(status == 400 and code == "bad_window",
                  f"window={bad!r} must be refused as bad_window; got {status} "
                  f"{code!r}")
        # Beside a command route the route's own file states the window, so
        # a request stating one too is refused rather than silently overruled.
        routed = a_submission(command_route="some-route", window=200000)
        routed.pop("model"), routed.pop("merge_model")
        status, _, body = request(runs, method="POST", payload=routed)
        error = (as_json(body) or {}).get("error") or {}
        check(status == 400 and error.get("code") == "refused"
              and "LLOSSLESS_WINDOW" in str(error.get("message")),
              f"a window beside a command route must be refused for that "
              f"reason; got {status} {body[:300]!r}")
        check(vendor.requests == [], "no refused submit may reach the endpoint")

        # Must not fire: the same id with a stated window completes every step.
        status, _, body = request(runs, method="POST",
                                  payload=dict(typed_body, window=200000))
        check(status == 202, f"a typed vendor id with a window must be accepted; "
                             f"got {status} {body[:300]!r}")
        payload = finished(built, (as_json(body) or {}).get("id", "")) if status == 202 else {}
        report = payload.get("report") or {}
        check(payload.get("state") == jobs.DONE and payload.get("exit_code") == 0,
              f"the run must finish clean; {payload.get('state')!r} "
              f"exit {payload.get('exit_code')!r} {payload.get('error')!r}")
        steps = report.get("steps") or []
        check(steps and all(step["state"] == "ok" for step in steps)
              and sum(step["name"].startswith("decompose") for step in steps) >= 3,
              f"every step must complete, the decomposes included: "
              f"{[(s['name'], s['state']) for s in steps]}")
        windows = (report.get("provenance") or {}).get("window") or {}
        check(windows and all(str(v).startswith("stated: 200000")
                              for v in windows.values()),
              f"the run must record the window as stated: {windows}")
        check(len(vendor.requests) >= 6 and all(
                  body.get("model") == typed for body in vendor.requests),
              f"every call must go to the vendor, as the typed id: "
              f"{len(vendor.requests)} call(s)")
        check(not any("/api/ps" in path for path in vendor.gets),
              f"a stated window sends no probe: {vendor.gets}")
        check(own.requests == [], "and nothing to the server's own endpoint")

        # Must not fire either: the server's own endpoint can report its
        # window, so the field is optional there and the run measures it.
        status, _, body = request(runs, method="POST", payload=a_submission(
            model=typed, merge_model=typed))
        check(status == 202, f"a typed id for this server's own endpoint needs "
                             f"no window; got {status} {body[:300]!r}")
        payload = finished(built, (as_json(body) or {}).get("id", "")) if status == 202 else {}
        check(payload.get("state") == jobs.DONE and payload.get("exit_code") == 0,
              f"and the run must measure it and finish: {payload.get('state')!r} "
              f"{payload.get('error')!r}")

        # Seeded on the shipped predicate: with `endpoint_plan`'s refusal
        # switched off, the same windowless submit is accepted, the merge
        # runs, and the checks refuse after it -- the defect this replaces.
        vendor.requests.clear()
        real = jobs.window_unreportable
        jobs.window_unreportable = lambda *_a, **_k: False
        try:
            status, _, body = request(runs, method="POST", payload=typed_body)
            payload = (finished(built, (as_json(body) or {}).get("id", ""))
                       if status == 202 else {})
        finally:
            jobs.window_unreportable = real
        steps = (payload.get("report") or {}).get("steps") or []
        check(status == 202 and payload.get("exit_code") == 2
              and any(step["name"] == "merge" and step["state"] == "ok"
                      for step in steps)
              and any(step["name"].startswith("decompose")
                      and "WindowUnmeasurable" in str(step["detail"])
                      for step in steps),
              f"with the refusal seeded out, the merge must run and the checks "
              f"refuse on the window, or the refusal guards nothing: {status} "
              f"{[(s['name'], s['state']) for s in steps]}")


def test_a_request_stated_window_names_the_page_s_field_in_provenance() -> None:
    """The phrase "declared by --window / LLOSSLESS_WINDOW" is a shell operator's

    own words for a figure only they could have stated. A run whose window
    reached the server through the *request* -- typed beside a vendor id
    or picked from a table row the catalogue does not know -- was not one, and
    naming the flag in its Provenance block would send a reader hunting a
    command line nobody typed. `web_settings` swaps the attribution
    (`Settings.window_declared_by`) for the one call site, exactly where
    `LLOSSLESS_WINDOW` arrived as a request override rather than the server's
    own environment; both reach `endpoint_plan` as the same variable, so this
    is the one place that can still tell them apart.
    """
    typed = "gpt-typed-not-in-the-catalogue"
    page_field = 'the page\'s "Context window (tokens)" field'
    with vendor_server(typed) as (built, vendor, own):
        runs = f"{built.url}{api.API_PREFIX}/runs"
        body = a_submission(model=typed, merge_model=typed, endpoint="openai",
                            window=200000)
        status, _, raw = request(runs, method="POST", payload=body)
        check(status == 202, f"a request-stated window must still be accepted; "
                             f"got {status} {raw[:200]!r}")
        payload = (finished(built, (as_json(raw) or {}).get("id", ""))
                  if status == 202 else {})
        report = payload.get("report") or {}
        windows = (report.get("provenance") or {}).get("window") or {}
        check(windows and all(page_field in str(v) for v in windows.values()),
              f"a request-stated window must name the page's field: {windows}")
        check(all("--window / LLOSSLESS_WINDOW" not in str(v)
                  for v in windows.values()),
              f"and must not also carry the CLI's own words: {windows}")

    # Must not fire: the server's own LLOSSLESS_WINDOW, set by whoever runs
    # it rather than by a request, still names the flag and the variable --
    # the ordinary case, unchanged.
    vendor = FakeEndpoint(Script(**CLEAN), ps_status=404)
    own = FakeEndpoint(Script(**CLEAN), loaded=(typed,))
    with vendor as vendor_url, own as own_url, \
            tempfile.TemporaryDirectory() as raw_dir:
        environ = {"LLOSSLESS_BASE_URL": own_url,
                  "LLOSSLESS_PROVIDER_URL_OPENAI": vendor_url,
                  "OPEN_AI_API_KEY": FAKE_KEY,
                  "LLOSSLESS_STRUCTURED": "prompt",
                  "LLOSSLESS_WINDOW": "200000"}
        built = server.build(port=0, work_dir=Path(raw_dir) / "work",
                             environ=environ)
        thread = server.background(built)
        try:
            runs = f"{built.url}{api.API_PREFIX}/runs"
            body = a_submission(model=typed, merge_model=typed, endpoint="openai")
            status, _, raw = request(runs, method="POST", payload=body)
            check(status == 202, f"the server's own stated window must still "
                                 f"be accepted with no request field; got "
                                 f"{status} {raw[:200]!r}")
            payload = (finished(built, (as_json(raw) or {}).get("id", ""))
                      if status == 202 else {})
            report = payload.get("report") or {}
            windows = (report.get("provenance") or {}).get("window") or {}
            check(windows and all("--window / LLOSSLESS_WINDOW" in str(v)
                                  for v in windows.values()),
                  f"a server-stated window must keep naming the CLI's own "
                  f"flag and variable: {windows}")
            check(all(page_field not in str(v) for v in windows.values()),
                  f"and must not name the page for a figure the page never "
                  f"stated: {windows}")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


def test_a_wrong_method_is_a_405_and_an_unknown_route_a_404() -> None:
    """Two refusals a client branches on differently, kept apart."""
    with live_server() as (built, _):
        root = f"{built.url}{api.API_PREFIX}"
        job_id, served = a_finished_run(built)
        if not served:
            return
        for url, method, wanted in (
                (f"{root}/health", "DELETE", 405),
                (f"{root}/runs/{job_id}", "POST", 405),
                (f"{root}/runs/{job_id}/merged", "DELETE", 405),
                (f"{root}/runs/{job_id}/events", "DELETE", 405),
                (f"{root}/runs/{job_id}/nothing", "GET", 404),
                (f"{root}/nothing", "GET", 404),
                (f"{built.url}/api/v2/health", "GET", 404)):
            status, _, body = request(url, method=method,
                                      raw=b"{}" if method == "POST" else None,
                                      headers={"Content-Type": "application/json"}
                                      if method == "POST" else None)
            check(status == wanted,
                  f"{method} {url} answered {status}, expected {wanted}: "
                  f"{body[:200]!r}")


# --------------------------------------------------------------------------
# the stream
# --------------------------------------------------------------------------


def test_the_stream_replays_exactly_the_tail_after_last_event_id() -> None:
    """Must fire and must not fire on one property: the tail, and only the tail.

    An off-by-one in either direction is invisible on a run that never dropped
    its connection, which is every run nobody is debugging. Asserted by
    comparing two responses from the same finished job rather than against the
    store's own `since()`, so a `since` that is wrong in both places cannot
    make this pass.
    """
    with live_server() as (built, _):
        job_id, served = a_finished_run(built)
        if not served:
            return
        whole = sse_events(built, job_id)
        check(len(whole) >= 4,
              f"a complete merge must produce several events; got {len(whole)}")
        check([event["id"] for event in whole] == list(range(1, len(whole) + 1)),
              f"event ids must be a dense run from 1; got "
              f"{[event['id'] for event in whole]}")
        check(whole[0]["kind"] == "state" and whole[-1]["kind"] == "state",
              "a stream must open with the queued state and close with the "
              "terminal one")
        check(whole[-1]["fields"]["terminal"] is True,
              "the last event must tell a page to stop listening")

        for cut in (0, 1, len(whole) // 2, len(whole) - 1, len(whole)):
            tail = sse_events(built, job_id, last_event_id=cut)
            check(tail == whole[cut:],
                  f"Last-Event-ID: {cut} must return exactly the {len(whole) - cut} "
                  f"event(s) after it; got {len(tail)}")
        # An unreadable header is "send everything", never a refusal: a page
        # that never loads is a worse answer than a few hundred events it
        # already had.
        check(sse_events(built, job_id, last_event_id="banana") == whole,
              "an unreadable Last-Event-ID must replay the whole log")
        check(sse_events(built, job_id, last_event_id=len(whole) + 500) == [],
              "an id past the end must return nothing, not the whole log")


def test_the_stream_frames_are_well_formed_sse() -> None:
    """`id:`, `event:`, `data:`, blank line -- and `data:` on exactly one line.

    The single-line rule is the one that breaks silently: SSE delimits fields by
    newline, so a message carrying one would end the frame early and the rest
    would arrive as a field the browser does not recognise.
    """
    with live_server() as (built, _):
        job_id, served = a_finished_run(built)
        if not served:
            return
        _, headers, body = request(
            f"{built.url}{api.API_PREFIX}/runs/{job_id}/events")
        check(headers["Content-Type"].startswith("text/event-stream"),
              f"the stream must be text/event-stream; got "
              f"{headers.get('Content-Type')!r}")
        text = body.decode("utf-8")
        check(text.endswith("\n\n"), "every frame ends with the blank line that "
                                     "dispatches it")
        blocks = [block for block in text.split("\n\n") if block.strip()]
        for block in blocks:
            lines = block.splitlines()
            if lines[0].startswith(":"):  # a keep-alive comment
                continue
            check(lines[0].startswith("id: "),
                  f"a frame must lead with its id, so a truncated frame has not "
                  f"advanced the browser's Last-Event-ID: {block[:80]!r}")
            check(lines[1].startswith("event: "), f"no event kind: {block[:80]!r}")
            data = [line for line in lines if line.startswith("data: ")]
            check(len(data) == 1,
                  f"a frame's data must be one line; {block[:80]!r} has "
                  f"{len(data)}")


# --------------------------------------------------------------------------
# the bind
# --------------------------------------------------------------------------

# Two detectors, because a wildcard bind has two spellings and only one of them
# is address-shaped. `ADDRESS_LITERAL` finds `"0.0.0.0"` and `"::"`;
# `BIND_CALL` finds whatever expression is actually passed as the host half of
# a server address, which is the only way to see `("", port)` -- an empty
# string is a wildcard bind and matches no address pattern at all. Both are
# functions so the code that judges `server.py` can be pointed at a snippet
# known to be wrong; a detector with no evidence it can say yes is not one.
ADDRESS_LITERAL = re.compile(r"""["'](\d{1,3}(?:\.\d{1,3}){3}|::1?)["']""")
BIND_CALL = re.compile(r"""(?:__init__|bind)\(\s*\(\s*([^,()]+?)\s*,""")


def bind_addresses(text: str) -> set[str]:
    """Every address-shaped literal in `text`."""
    return set(ADDRESS_LITERAL.findall(text))


def bind_hosts(text: str) -> set[str]:
    """Whatever `text` passes as the host half of a `(host, port)` server address."""
    return {found.strip() for found in BIND_CALL.findall(text)}


def test_the_server_binds_loopback_by_default_and_every_address_is_one_expression() -> None:
    """Three ways, because the constant alone is not the guarantee.

    The bound socket is asked what it bound; the source is scanned for any
    other address literal it could have bound instead; and the constructors are
    asked what a caller can pass. The third changed once `--host` existed,
    and what stands in for its absence is that every entry point which
    can be told an address can also be told a token. A `--host` shipped
    *before* the token would have left a commit in which a key-spending
    endpoint is reachable from the network with nothing in front of it, and
    intermediate commits get deployed; the refusal that makes the pair
    inseparable is `credentials.require_token`, and
    `tests/test_web_credentials.py` drives it against a real bind.
    """
    with live_server() as (built, _):
        check(built.server_address[0] == "127.0.0.1",
              f"the server bound {built.server_address[0]!r}")
        check(server.HOST == "127.0.0.1",
              f"server.HOST is {server.HOST!r}")

    text = (ROOT / "src" / "llossless" / "web" / "server.py").read_text(encoding="utf-8")
    found = bind_addresses(text)
    check(found <= {"127.0.0.1"},
          f"server.py carries address literals other than loopback: "
          f"{sorted(found - {'127.0.0.1'})}. A wildcard bind may not exist in "
          f"this file before the authentication token does")
    bound = bind_hosts(text)
    check(bound == {"self.host"},
          f"server.py passes {sorted(bound)} as a bind address; there is one "
          f"permitted expression and it is the attribute `build` set after "
          f"`require_token` ruled on it, because an empty string is a wildcard "
          f"bind and is not address-shaped")

    # Every way in that can be told where to listen can be told what to demand
    # from a request. This is what replaced "no entry point takes a host":
    # a function that could be given an address and not a token would be a
    # function through which the pair comes apart.
    for name, function in (("build", server.build), ("serve", server.serve),
                           ("Server.__init__", server.Server.__init__)):
        parameters = set(inspect.signature(function).parameters)
        addressable = parameters & {"host", "address", "bind", "interface"}
        check(not addressable or "token" in parameters,
              f"{name} takes a bind address ({sorted(addressable)}) and no "
              f"token, so an address can be chosen without one being demanded")

    offered = {spelling
               for action in cli.build_parser()._subparsers._group_actions[0]
               .choices["serve"]._actions
               for spelling in action.option_strings}
    check("--host" in offered and "--bind" not in offered,
          f"`llossless serve` must offer --host and only that spelling of it: "
          f"{sorted(offered)}")

    # Must fire, both detectors, on the two spellings of the same mistake.
    dotted = 'super().__init__(("0.0.0.0", port), Handler)\n'
    check(bind_addresses(dotted) == {"0.0.0.0"},
          f"the address scan cannot see a wildcard bind written in front of it "
          f"({bind_addresses(dotted)}), so its silence over server.py means "
          f"nothing")
    empty = 'sock.bind(("", port))\n'
    check(bind_addresses(empty) == set() and bind_hosts(empty) == {'""'},
          f"the bind scan cannot see an empty-string wildcard "
          f"({bind_hosts(empty)}) -- which is the spelling no address pattern "
          f"catches and the reason the second detector exists")


def test_a_fault_in_a_handler_is_a_500_that_says_nothing_about_the_host() -> None:
    """Must fire. A traceback may reach the operator's stream and never a client.

    Without this, a bug anywhere below the router reaches
    `BaseHTTPRequestHandler.handle_error`, which writes a traceback to stderr
    and closes the connection **with no response at all** -- a client sees a
    reset and cannot tell a broken server from a network fault. And a traceback
    names modules, line numbers and frequently a path on this host, which is
    the disclosure the whole of `redact` exists to prevent.

    Seeded on a store whose `jobs()` raises, because that is a real call the
    router makes and not a copy of the error path.
    """
    class Exploding:
        """A store that raises where the router will call it."""

        work_dir = cache_dir = None
        environ: dict = {}

        def jobs(self):
            raise RuntimeError("a path on this host: " + str(Path.home()))

        def get(self, job_id):
            return None

    failed = io.StringIO()
    try:
        with contextlib.redirect_stderr(failed):
            answer = api.Api(Exploding()).handle(
                "GET", f"{api.API_PREFIX}/runs", headers={"Host": "127.0.0.1"})
    except Exception as escaped:  # noqa: BLE001 - that is the defect
        check(False, f"a handler fault escaped `handle` instead of becoming a "
                     f"response: {type(escaped).__name__}: {escaped}")
        return
    payload = as_json(answer.body) or {}
    check(answer.status == 500 and (payload.get('error') or {}).get("code") == "internal",
          f"a handler fault must become a 500 the contract defines; got "
          f"{answer.status} {answer.body[:200]!r}")
    check(str(Path.home()) not in answer.body.decode("utf-8")
          and b"RuntimeError" not in answer.body,
          f"the 500 body carries the exception: {answer.body[:200]!r}")
    check("RuntimeError" in failed.getvalue(),
          "the traceback must reach the operator's own stream; it went nowhere")
    # Must not fire: an ordinary request through the same entry point.
    with live_server() as (built, _):
        check(request(f"{built.url}{api.API_PREFIX}/runs")[0] == 200,
              "a working store must still answer 200 through the same path")


def test_the_report_page_carries_the_file_it_offers_to_save() -> None:
    """Two routes, and the control asks this server for nothing.

    It cannot ask. The report is served sandboxed into an opaque origin, so a
    request it starts is cross-site, and the session cookie is
    `SameSite=Strict` -- a link to the file route was measured answering 401
    in a browser tab that had just loaded the page it was on. So the control
    carries the report in its own `data:` URL, and what it hands over has to
    be the file this server would have sent: decoded here and compared byte
    for byte, because "the page contains the file" is the whole property and
    a page that carried a near-copy would look identical in a screenshot.
    """
    with live_server() as (built, _):
        job_id, served = a_finished_run(built)
        if not served:
            return
        root = f"{built.url}{api.API_PREFIX}/runs/{job_id}"
        _, file_headers, file_body = request(f"{root}/report.html")
        _, _, page_body = request(f"{root}/report")
        page = page_body.decode("utf-8")
        check("Content-Disposition" not in file_headers,
              "the file route answers the panel's link, the API and `curl` "
              "alike; it does not decide for them what a reader is doing")
        mark = 'href="data:text/html;charset=utf-8;base64,'
        check(mark in page, "the page carries no control that holds the report")
        if mark not in page:
            return
        start = page.index(mark) + len(mark)
        carried = base64.b64decode(page[start:page.index('"', start)])
        check(carried == file_body,
              f"what the control hands over is not the file this server "
              f"serves: {len(carried)} bytes against {len(file_body)}")
        check(b'class="save"' not in carried,
              "the saved copy carries a control of its own")
        # And the page is the file with one slot filled, so a reader who saves
        # from either place gets the same report.
        rebuilt = re.sub(r'<p class="toolbar">.*?</p>', "<!--controls-->",
                         page, count=1, flags=re.S)
        check(rebuilt.encode("utf-8") == file_body,
              "the page and the file are not one report with one slot filled; "
              "a second renderer has appeared between them")


def test_the_html_report_is_served_in_a_sandbox_of_its_own() -> None:
    """One policy header, and it is the report's rather than the API's.

    `html_report.render` puts an inline `<script>` in the page -- the filter box
    -- so the server's own policy, which forbids inline script, would serve a
    report whose search field silently does nothing. Two policy headers would
    do the same thing, because a browser enforces the intersection of them.
    That is the failure being checked: not that a header is present, but that
    exactly one is and it is the right one.
    """
    with live_server() as (built, _):
        job_id, served = a_finished_run(built)
        if not served:
            return
        raw = urllib.request.urlopen(
            f"{built.url}{api.API_PREFIX}/runs/{job_id}/report.html",
            timeout=PATIENCE)
        with raw as answer:
            policies = answer.headers.get_all("Content-Security-Policy") or []
            body = answer.read(READ_CAP)
        check(len(policies) == 1,
              f"the report must carry exactly one policy; it carries "
              f"{len(policies)}: {policies}")
        check(policies and policies[0] == api.REPORT_CSP,
              f"the report must be served under its own policy, not the API's; "
              f"got {policies[0] if policies else None!r}")
        check("sandbox allow-scripts" in policies[0]
              and "allow-same-origin" not in policies[0],
              "the report must run in an opaque origin: its script is there to "
              "filter its own rows, not to read anything of this server's")
        check(b"<script>" in body,
              "the report really does carry an inline script, or the policy "
              "above is solving a problem this page does not have")
        # The page that shows the same report is the same policy plus one
        # token. A sandboxed document may not start a download unless the
        # policy says so, and the control on that page is a download; without
        # the token Chromium blocks it with no dialogue and no page error, so
        # the failure is a button that does nothing.
        raw = urllib.request.urlopen(
            f"{built.url}{api.API_PREFIX}/runs/{job_id}/report", timeout=PATIENCE)
        with raw as answer:
            page_policies = answer.headers.get_all("Content-Security-Policy") or []
            page_body = answer.read(READ_CAP)
        check(len(page_policies) == 1 and page_policies[0] == api.REPORT_PAGE_CSP,
              f"the report page must carry exactly its own policy; got "
              f"{page_policies}")
        check("allow-downloads" in page_policies[0],
              "the page carries a control that saves the report, and a "
              "sandbox without allow-downloads blocks it silently")
        check("allow-same-origin" not in page_policies[0],
              "nothing but the download was relaxed: the page still runs in "
              "an opaque origin")
        check(b'class="save"' in page_body,
              "the page is served under a policy that permits a download and "
              "carries no control that starts one")
        # And the file itself is the strict policy and no such control, which
        # is the pair: the policy is relaxed exactly where the control is.
        check("allow-downloads" not in api.REPORT_CSP,
              "the file's own policy must stay the strict one")
        check(b'class="save"' not in body,
              "the file a reader keeps carries a control pointing at this "
              "server, which is a dead link on their disk")
        # Must not fire: every other response keeps the server's own policy.
        for url in (f"{built.url}/", f"{built.url}{api.API_PREFIX}/health"):
            _, headers, _ = request(url)
            check("sandbox" not in headers.get("Content-Security-Policy", ""),
                  f"{url} was served under the report's sandbox policy")


def test_the_static_directory_serves_a_page_and_nothing_above_itself() -> None:
    """The placeholder is served, and no request reaches out of the directory."""
    with live_server() as (built, _):
        status, headers, body = request(f"{built.url}/")
        check(status == 200 and headers["Content-Type"].startswith("text/html"),
              f"/ must serve the page in static/; got {status}")
        check(b"<title>LLossless</title>" in body
              and b'<span class="wordmark">LLossless</span>' in body,
              "the placeholder page must name the tool, as LLossless, in its "
              "title and its wordmark")
        check(headers.get("X-Content-Type-Options") == "nosniff"
              and headers.get("X-Frame-Options") == "DENY"
              and "frame-ancestors 'none'" in headers.get("Content-Security-Policy", ""),
              f"every response carries the security headers; got "
              f"{sorted(headers)}")
        # `catalogue.json` is the probe that matters: it is one directory above
        # `static/`, it really exists, and its extension is one this server
        # does hand out -- so it is the only one of these that the extension
        # allowlist does not refuse on its own, and therefore the only one that
        # tests the path rules rather than the type rules.
        for escape in ("/../catalogue.json", "/../../web/catalogue.json",
                       "/index.html/../../catalogue.json",
                       "/../pyproject.toml", "/../../pyproject.toml",
                       "/..%2fpyproject.toml", "/static/../server.py",
                       "/server.py", "/.env", "/index.html/../../cli.py"):
            status, _, body = request(f"{built.url}{escape}")
            check(status == 404,
                  f"{escape} answered {status}; nothing above static/ is served")
            check(b"hatchling" not in body and b"def main" not in body
                  and b"schema_version" not in body,
                  f"{escape} served content from outside static/")
        check(request(f"{built.url}/", headers={"Host": "attacker.example"})[0] == 403,
              "the page is behind the same Host check as every API route")
        # Must not fire: the file that is there, by name.
        check(request(f"{built.url}/index.html")[0] == 200,
              "static/index.html must be servable by name")


# --------------------------------------------------------------------------
# the command line
# --------------------------------------------------------------------------


def test_serve_is_a_subcommand_and_its_defaults_match_the_web_package() -> None:
    """The three numbers `cli.py` restates are required to still be the same three.

    `cli.build_parser` runs on every invocation, so it may not import
    `llossless.web` to read them -- the engine is required to work with the web
    package absent. Restating them is the cost; this is what stops the restated
    copy drifting from the real one, which would show up as a `--help` that
    names a default the server does not use.
    """
    args = cli.build_parser().parse_args(["serve"])
    check(args.command == "serve", "there must be a `serve` subcommand")
    check(args.port == cli.SERVE_PORT == server.DEFAULT_PORT,
          f"the port default differs: cli {cli.SERVE_PORT}, web "
          f"{server.DEFAULT_PORT}")
    check(args.workers == cli.SERVE_WORKERS == jobs.DEFAULT_WORKERS,
          f"the worker default differs: cli {cli.SERVE_WORKERS}, web "
          f"{jobs.DEFAULT_WORKERS}")
    check(cli.SERVE_RETENTION == jobs.DEFAULT_RETENTION_SECONDS,
          f"the retention default differs: cli {cli.SERVE_RETENTION}, web "
          f"{jobs.DEFAULT_RETENTION_SECONDS}")
    check(cli.SERVE_RETENTION_ENV == jobs.RETENTION_ENV,
          f"the retention variable differs: cli {cli.SERVE_RETENTION_ENV}, web "
          f"{jobs.RETENTION_ENV}")
    # Not the default value: `--retention` defaults to "the operator did not
    # say", so that a flag can beat `LLOSSLESS_RETENTION` and the variable can
    # beat the default. The restated number above is what `--help` prints and
    # what the absent flag resolves to, which is asserted through `serve` in
    # `test_the_retention_window_is_the_flag_then_the_variable_then_the_default`.
    check(args.retention is None,
          f"`--retention` must default to None so that 'not given' and 'keep "
          f"forever' are different answers; got {args.retention!r}")
    check(args.work_dir is None,
          "the work directory defaults to None so the web package chooses it")


def test_serve_starts_a_real_server_through_cli_main() -> None:
    """The command, not the function. Port 0, then asked what it bound.

    `cli.main(["serve", ...])` is the path an operator takes, and it is the path
    where the lazy import of `llossless.web` either happens or raises. Driven
    on a thread and stopped by interrupting `serve_forever` the way a terminal
    would, so what is exercised is the whole of the branch rather than the part
    of it up to the import.

    **The command always has an account store, so a first boot is in setup.**
    That is what it now announces and what it now refuses: `/health` answers
    401, the banner carries a one-time address, and the account that address
    creates is the one the existing credentials file belongs to. Both the
    refusal and the address are asserted here, because a setup mode that
    printed its URL and let everybody in anyway would look identical from the
    banner.

    `LLOSSLESS_ACCOUNTS` points the store at the temporary directory. Without
    it this test would read -- and, if it created anything, write -- the
    accounts file of whoever is running the suite.
    """
    out = io.StringIO()
    banner = threading.Event()
    result: dict = {}

    class Watch(io.StringIO):
        """Stands in for stderr, and releases the test once the banner lands."""

        def write(self, text: str) -> int:
            written = out.write(text)
            if "serving http://127.0.0.1:" in out.getvalue():
                banner.set()
            return written

    with tempfile.TemporaryDirectory() as raw:
        # `serve` blocks, so the exit code comes back through the thread. The
        # port is read out of the banner because that is the only thing the
        # command tells an operator who asked for port 0, and a test that
        # reached into the server object instead would not be checking what the
        # operator is told.
        def run() -> None:
            with contextlib.redirect_stderr(Watch()):
                result["code"] = cli.main(
                    ["serve", "--port", "0", "--work-dir", str(Path(raw) / "w"),
                     "--retention", "0"])

        before = os.environ.get("LLOSSLESS_ACCOUNTS")
        os.environ["LLOSSLESS_ACCOUNTS"] = str(Path(raw) / "accounts.json")
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        check(banner.wait(timeout=PATIENCE), f"`llossless serve` never announced "
                                             f"itself: {out.getvalue()[:400]!r}")
        text = out.getvalue()
        port = re.search(r"serving http://127\.0\.0\.1:(\d+)", text)
        if port is None:
            check(False, f"no address in the banner: {text[:400]!r}")
            return
        url = f"http://127.0.0.1:{port.group(1)}"
        status, _, body = request(f"{url}{api.API_PREFIX}/health")
        check(status == 401 and as_json(body)["error"]["code"] == "setup_required",
              f"a server with no accounts must answer nothing but setup; "
              f"/health said {status} {body[:160]!r}")
        check("kept until deleted, across restarts" in text,
              f"`--retention 0` must be announced as keeping documents; the "
              f"banner says {text[:400]!r}")
        check(f"this machine only (127.0.0.1:{port.group(1)}); the first account "
              f"is not made yet" in text,
              f"the banner must say who can reach this server and whether "
              f"anything stands in front of it: {text[:400]!r}")
        setup_url = re.search(r"http://127\.0\.0\.1:\d+/#setup=(\S+)", text)
        check(setup_url is not None,
              f"the banner must carry the one-time setup address, or a first "
              f"boot is a server nobody can start using: {text[:600]!r}")
        # And the page itself is still served, because the form that uses that
        # address is on it. A setup mode that refused the page too would be a
        # setup mode with no way in.
        check(request(f"{url}/")[0] == 200,
              "the page must be fetchable in setup mode")
        if setup_url is not None:
            created = request(
                f"{url}{api.API_PREFIX}/setup", method="POST",
                payload={"token": setup_url.group(1), "username": "probe",
                         "password": "probe-password-01"})
            check(created[0] == 200,
                  f"the printed setup address must create the first account; "
                  f"got {created[0]} {created[2][:200]!r}")
            # Must not fire twice. A one-time address that works a second time
            # is a standing account-creation endpoint on a public port.
            again = request(
                f"{url}{api.API_PREFIX}/setup", method="POST",
                payload={"token": setup_url.group(1), "username": "probe2",
                         "password": "probe-password-02"})
            check(again[0] == 409,
                  f"the setup address must stop working once an account "
                  f"exists; got {again[0]}")

        # Stop it the way a terminal does. `serve_forever` is inside `main`, so
        # the interrupt has to reach the thread that is in it; raising in this
        # one would prove nothing about the command.
        request(f"{url}{api.API_PREFIX}/health")
        import ctypes

        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_ulong(thread.ident), ctypes.py_object(KeyboardInterrupt))
        thread.join(timeout=PATIENCE)
        check(not thread.is_alive(),
              "`llossless serve` did not stop on an interrupt")
        check(result.get("code") == 0,
              f"an interrupted `llossless serve` exits 0; got {result.get('code')}")
        if before is None:
            os.environ.pop("LLOSSLESS_ACCOUNTS", None)
        else:
            os.environ["LLOSSLESS_ACCOUNTS"] = before


def serve_banner(argv, environ=None) -> str:
    """Start `llossless serve` the way an operator does and return its banner.

    The command and not the function: the retention window it ends up on is
    decided across three places -- argparse's default, `cli.main`'s
    translation of it, and `server.serve`'s read of the environment -- and a
    check that called any one of them would be checking a link rather than the
    chain. The banner is what the operator is told, so it is what is read.

    `LLOSSLESS_ACCOUNTS` is pointed at a temporary file, or this would read --
    and could write -- the accounts of whoever is running the suite.
    """
    out = io.StringIO()
    banner = threading.Event()

    class Watch(io.StringIO):
        def write(self, text: str) -> int:
            written = out.write(text)
            if "serving http://127.0.0.1:" in out.getvalue() or "serve: " in text:
                banner.set()
            return written

    with tempfile.TemporaryDirectory() as raw:
        def run() -> None:
            with contextlib.redirect_stderr(Watch()):
                cli.main(["serve", "--port", "0",
                          "--work-dir", str(Path(raw) / "w")] + list(argv))

        before = {name: os.environ.get(name)
                  for name in ("LLOSSLESS_ACCOUNTS", jobs.RETENTION_ENV)}
        os.environ["LLOSSLESS_ACCOUNTS"] = str(Path(raw) / "accounts.json")
        if environ is None:
            os.environ.pop(jobs.RETENTION_ENV, None)
        else:
            os.environ[jobs.RETENTION_ENV] = environ
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        try:
            banner.wait(timeout=PATIENCE)
            return out.getvalue()
        finally:
            # The same interrupt a terminal sends. Raised on the serving
            # thread, so the command returns through its own shutdown rather
            # than being left with live worker threads behind a dead test.
            #
            # One request first, where there is a server to make it to. An
            # asynchronous exception is delivered when the target thread next
            # runs bytecode, and a thread parked in `serve_forever`'s select
            # does not -- so without this the interrupt lands whenever
            # something else happens to wake it, which is to say never.
            where = re.search(r"serving (http://127\.0\.0\.1:\d+)",
                              out.getvalue())
            if where:
                with contextlib.suppress(Exception):
                    request(f"{where.group(1)}{api.API_PREFIX}/health")
            _interrupt(thread)
            thread.join(timeout=PATIENCE)
            check(not thread.is_alive(),
                  f"a `llossless serve` started for a retention check is "
                  f"still running: {out.getvalue()[:200]!r}")
            for name, value in before.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value


def _interrupt(thread: threading.Thread) -> None:
    """Ask a serving thread to stop, the way Ctrl-C does."""
    import ctypes
    if thread.ident is None:  # pragma: no cover - never started
        return
    ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_ulong(thread.ident),
        ctypes.py_object(KeyboardInterrupt))


def test_the_retention_window_is_the_flag_then_the_variable_then_the_default() -> None:
    """Three sources, ranked, asserted through the command an operator runs.

    Read off the banner rather than out of a store, because the banner is the
    promise: an operator handed a confidential document is told how long this
    server keeps it, and a banner that said one number while the reaper used
    another would be the worst available failure of this setting.

    The `--retention 0` case is here rather than in a test of its own because
    it is the one that must survive the new precedence: `0` and "the flag was
    not given" are two different things, and a version of this that spelled
    both `None` would turn an operator's opt-out into whatever the environment
    happened to hold.
    """
    default = int(jobs.DEFAULT_RETENTION_SECONDS)
    plain = serve_banner([])
    check(f"deleted {default}s after a run finishes" in plain,
          f"a server with no flag and no variable must announce the default "
          f"{default}s: {plain[:400]!r}")

    from_env = serve_banner([], environ="900")
    check("deleted 900s after a run finishes" in from_env,
          f"{jobs.RETENTION_ENV} must set the window when no flag does: "
          f"{from_env[:400]!r}")

    both = serve_banner(["--retention", "60"], environ="900")
    check("deleted 60s after a run finishes" in both,
          f"the flag must beat the variable: {both[:400]!r}")

    opted_out = serve_banner(["--retention", "0"], environ="900")
    check("kept until deleted, across restarts" in opted_out,
          f"`--retention 0` must still mean keep forever, whatever the "
          f"variable says: {opted_out[:400]!r}")

    refused = serve_banner([], environ="48h")
    check(jobs.RETENTION_ENV in refused and "must be a number" in refused,
          f"an unreadable window must be refused by name rather than quietly "
          f"replaced with the default: {refused[:400]!r}")
    check("serving http://" not in refused,
          f"a server must not start on a window nobody chose: {refused[:400]!r}")


def test_a_server_with_no_flag_and_no_variable_runs_the_default_window() -> None:
    """The default, read back out of the thing that enforces it.

    Off `built.store` rather than off `jobs.DEFAULT_RETENTION_SECONDS`: the
    store's own field is what `sweep` reads, and a constant that had drifted
    from the signature default would leave this passing while every deployment
    ran on something else.
    """
    with live_server() as (built, _endpoint):
        check(built.store.retention_seconds == jobs.DEFAULT_RETENTION_SECONDS,
              f"a server built with no retention argument runs on "
              f"{built.store.retention_seconds}s, not the "
              f"{jobs.DEFAULT_RETENTION_SECONDS}s default")
        _status, _headers, body = request(f"{built.url}{api.API_PREFIX}/config")
        block = (as_json(body) or {}).get("retention") or {}
        check(block.get("seconds") == built.store.retention_seconds,
              f"/config must serve the window this server is actually on; it "
              f"says {block.get('seconds')!r}")
        check(block.get("warn_seconds") == 4 * 3600.0,
              f"/config must serve the threshold the page warns at; it says "
              f"{block.get('warn_seconds')!r}")


def test_a_server_that_keeps_everything_says_so_rather_than_naming_a_number() -> None:
    """The opt-out, end to end. `null` is a sentence, not a very large window."""
    with live_server(retention_seconds=None) as (built, _endpoint):
        _status, _headers, body = request(f"{built.url}{api.API_PREFIX}/config")
        block = (as_json(body) or {}).get("retention") or {}
        check("seconds" in block and block["seconds"] is None,
              f"retention off must be served as null, so the page can say "
              f"'kept until you delete them'; got {block!r}")
        check(block.get("warn_seconds") is None,
              "there is nothing to warn about when nothing is deleted")
        job_id, payload = a_finished_run(built)
        check(payload.get("expires_in") is None,
              f"a run on a server that deletes nothing has no countdown; got "
              f"{payload.get('expires_in')!r}")


def test_a_finished_run_reports_how_long_it_has_left() -> None:
    """The countdown the page renders, and that it is an interval, not a time."""
    with live_server(retention_seconds=600.0) as (built, _endpoint):
        job_id, payload = a_finished_run(built)
        left = payload.get("expires_in")
        check(isinstance(left, (int, float)) and 0 < left <= 600.0,
              f"a run on a ten-minute window must report what is left of it; "
              f"got {left!r}")
        # Twice, a moment apart, and the second is smaller. A field that was
        # really a timestamp, or a constant, would not move.
        time.sleep(1.1)
        _status, _headers, body = request(
            f"{built.url}{api.API_PREFIX}/runs/{job_id}")
        again = (as_json(body) or {}).get("expires_in")
        check(isinstance(again, (int, float)) and again < left,
              f"the countdown must fall between two requests; {left!r} then "
              f"{again!r}")
        # And it is in the list too, so a run opened from the history panel
        # knows where it stands without a second request.
        _status, _headers, body = request(f"{built.url}{api.API_PREFIX}/runs")
        rows = (as_json(body) or {}).get("runs") or []
        mine = [row for row in rows if row.get("id") == job_id]
        check(len(mine) == 1 and isinstance(mine[0].get("expires_in"), (int, float)),
              f"the run list must carry the countdown too; got {mine!r}")


def test_a_forgotten_run_refuses_every_download_and_names_the_knob() -> None:
    """The reaper, driven, and then all four download routes asked.

    The operator opened a finished run's report and was told only what had
    happened. What a person needs at that moment is whether it can be stopped
    from happening again, which on a self-hosted tool is a question they can
    usually answer themselves -- so the refusal names the flag and the
    variable, and does it on every route rather than on the one link they were
    least likely to click.
    """
    with live_server(retention_seconds=600.0) as (built, _endpoint):
        job_id, _payload = a_finished_run(built)
        job = built.store.get(job_id)
        check(job is not None and job.terminal, "the run did not finish")
        # Past the window, then the real sweep. Not `_forget` directly: what
        # is being checked is the path a server takes on its own.
        forgotten = built.store.sweep(now=time.time() + 10_000)
        check([one.id for one in forgotten] == [job_id],
              f"the sweep did not forget the run; got {forgotten!r}")
        for name, suffix in (("merged", "/merged"),
                             ("report file", "/report.html"),
                             ("report page", "/report"),
                             ("bundle", f"/{api.BUNDLE_ZIP}")):
            status, _headers, body = request(
                f"{built.url}{api.API_PREFIX}/runs/{job_id}{suffix}")
            payload = as_json(body) or {}
            message = str((payload.get("error") or {}).get("message", ""))
            check(status == 410 and (payload.get("error") or {}).get("code")
                  == "forgotten",
                  f"the {name} route answered {status} for a forgotten run: "
                  f"{body[:200]!r}")
            check("--retention" in message and jobs.RETENTION_ENV in message,
                  f"the {name} refusal does not say how to stop this happening "
                  f"again: {message!r}")
            check("0 keeps runs" in message or "keeps runs" in message,
                  f"the {name} refusal does not name the opt-out: {message!r}")
        # And the run is still findable, so a bookmark is answered rather than
        # looking like a typo. That is the property the message rides on.
        status, _headers, body = request(
            f"{built.url}{api.API_PREFIX}/runs/{job_id}")
        check(status == 200 and (as_json(body) or {}).get("forgotten_at"),
              f"a forgotten run must still answer its own route: {status}")
        check((as_json(body) or {}).get("expires_in") is None,
              "a forgotten run has nothing left to count down to")


def test_the_forgotten_message_check_fires_when_the_remedy_is_taken_out() -> None:
    """Seeded on the shipped string rather than on a copy of the comparison.

    The message is built inside `Api._artefact`, so the seed is that function
    with its remedy removed -- the state the code was in before the fix -- and the
    assertion the real check makes is run against it.
    """
    source = inspect.getsource(api.Api._artefact)
    start = source.index('raise ApiError(410, "forgotten"')
    end = source.index("if not job.terminal", start)
    shipped = source[start:end]
    check("--retention" in shipped and "RETENTION_ENV" in shipped,
          f"the forgotten refusal must name the flag and the variable in the "
          f"source the server runs: {shipped!r}")
    seeded = shipped.split("passes.")[0] + 'passes.")\n        '
    check("--retention" not in seeded and "RETENTION_ENV" not in seeded,
          "the seeded message still carries the remedy, so this probe would "
          "not fail on a regression")


def test_the_bundle_carries_the_sources_the_merge_and_both_reports() -> None:
    """One archive an auditor can check this run from, with no server left.

    The members are what decides whether this is an audit record: the sources
    it was made from, the document it produced, and both reports -- the HTML
    for a person and `report.json` for a tool, carrying the provenance block
    that names the models and the settings. A bundle of the product alone
    would be a download, not an audit.
    """
    with live_server() as (built, _endpoint):
        job_id, _payload = a_finished_run(built)
        status, headers, body = request(
            f"{built.url}{api.API_PREFIX}/runs/{job_id}/{api.BUNDLE_ZIP}")
        check(status == 200, f"the bundle answered {status}: {body[:200]!r}")
        check(headers.get("Content-Type") == "application/zip",
              f"the bundle must be served as a zip; got "
              f"{headers.get('Content-Type')!r}")
        check(job_id in str(headers.get("Content-Disposition", "")),
              f"the saved name must identify the run: "
              f"{headers.get('Content-Disposition')!r}")
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            names = sorted(archive.namelist())
            broken = archive.testzip()
            check(broken is None, f"the archive is damaged at {broken!r}")
            for wanted in (jobs.MERGED_MD, jobs.REPORT_JSON, jobs.REPORT_HTML):
                check(wanted in names,
                      f"the bundle has no {wanted}; it holds {names}")
            sources = [name for name in names if name.startswith("sources/")]
            check(len(sources) == 2,
                  f"the bundle must carry both submitted documents; it holds "
                  f"{sources}")
            # The sources are the operator's own text, byte for byte, which is
            # the whole reason an auditor can check anything against them.
            joined = "\n".join(
                archive.read(name).decode("utf-8") for name in sources)
            check(SOURCE_A in joined and SOURCE_B in joined,
                  "the bundled sources are not the documents that were sent")
            merged = archive.read(jobs.MERGED_MD).decode("utf-8")
            _status, _headers, served = request(
                f"{built.url}{api.API_PREFIX}/runs/{job_id}/merged")
            check(merged == served.decode("utf-8"),
                  "the bundled merge is not the one this server serves")
            record = json.loads(archive.read(jobs.REPORT_JSON).decode("utf-8"))
            check(isinstance(record, dict) and record.get("provenance"),
                  f"the bundled record carries no provenance, which is what an "
                  f"auditor reads it for: {sorted(record)[:12]}")
            page = archive.read(jobs.REPORT_HTML).decode("utf-8")
            check("<style" in page and "<html" in page.lower(),
                  "the bundled report is not the self-contained page")


def test_the_bundle_is_refused_to_a_stranger_and_on_the_wrong_method() -> None:
    """Same authorisation as the downloads beside it, not a weaker second path.

    A run nobody else may read answers the same 404 here as it does on every
    other route -- `Api.job` is the one lookup, and a bundle route that did its
    own would be the place that rule stopped being true.
    """
    with live_server() as (built, _endpoint):
        job_id, _payload = a_finished_run(built)
        invented = "f" * 32
        status, _headers, body = request(
            f"{built.url}{api.API_PREFIX}/runs/{invented}/{api.BUNDLE_ZIP}")
        check(status == 404 and (as_json(body) or {}).get("error", {}).get("code")
              == "no_run",
              f"a bundle for a run that does not exist answered {status}: "
              f"{body[:200]!r}")
        status, _headers, _body = request(
            f"{built.url}{api.API_PREFIX}/runs/{job_id}/{api.BUNDLE_ZIP}",
            method="DELETE")
        check(status == 405, f"a bundle is a GET; DELETE answered {status}")
        status, _headers, body = request(
            f"{built.url}{api.API_PREFIX}/runs/not-an-id/{api.BUNDLE_ZIP}")
        check(status == 400 and (as_json(body) or {}).get("error", {}).get("code")
              == "bad_id",
              f"an id that is not an id answered {status}: {body[:200]!r}")


def test_a_bundle_member_name_is_built_and_never_a_path() -> None:
    """A document label is free text, and a zip member name is not.

    `../../.ssh/authorized_keys` is a legal label -- it comes from a form
    field -- and an archive carrying it as a member name is an archive that
    writes outside whatever directory it is extracted into. The name is
    therefore built from the characters that are allowed rather than cleaned
    of the ones that are not, which is the same answer `check_job_id` gives.
    """
    for label, expected in (
            ("notes-a.md", "notes-a.md"),
            ("../../.ssh/authorized_keys", "ssh-authorized_keys.md"),
            ("/etc/passwd", "etc-passwd.md"),
            ("..", "document.md"),
            ("", "document.md"),
            # The ordinary case, and the reason the extension is added at all:
            # a label typed into a form has none, and a member with no
            # extension extracts to a file nothing opens.
            ("Document 1", "Document-1.md"),
            ("C:\\Windows\\win.ini", "C-Windows-win.ini")):
        built = api._zip_name(label)
        check(built == expected,
              f"{label!r} became {built!r}, expected {expected!r}")
        check("/" not in built and "\\" not in built and ".." not in built,
              f"{label!r} became a member name with a path in it: {built!r}")


def test_the_web_package_is_not_imported_by_building_the_parser() -> None:
    """Must fire. The companion to `tests/test_cli.py`'s import-boundary probe.

    That test runs a complete merge in a subprocess and requires
    `llossless.web` absent afterwards. This one is the cheap, specific half:
    the parser is what a `serve` subcommand is most likely to be wired into at
    module scope, and this is where that would show up first. It runs in a
    subprocess for the same reason -- by the time this module has imported, the
    web package is in `sys.modules` and nothing in-process could tell.
    """
    import subprocess

    probe = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, %r);"
         "from llossless import cli; cli.build_parser().parse_args(['serve']);"
         "print(any(m.startswith('llossless.web') for m in sys.modules))"
         % str(ROOT / "src")],
        capture_output=True, text=True, timeout=PATIENCE)
    check(probe.returncode == 0,
          f"the probe must run to completion; {probe.stderr[-300:]!r}")
    check(probe.stdout.strip() == "False",
          f"building the parser loaded llossless.web: {probe.stdout!r}. The "
          f"serve import belongs inside main's serve branch and nowhere else")


# --------------------------------------------------------------------------
# the merge effort a request chooses on a command route
# --------------------------------------------------------------------------


@contextlib.contextmanager
def claude_routes(environ_extra: dict | None = None):
    """A server with four command routes through a fake program named `claude`.

    Named `claude` because `AUTO_EFFORT` and `AUTO_EFFORT_BY_MODEL` are keyed by
    the program's basename. It logs its argv and the prompt's kind to a file,
    then answers as `tests/test_web_commands.py`'s fake does, so "the level
    reached the argv" is read off what the program was really started with.
    Yields `(built, calls)`, `calls()` reading the log back.

    The four `claude-<alias>` rows are the discovered ones; `wrapper` is the
    same program under a name this build has not read; `pinned` is `claude`
    with a level already in its own command, which wins over any request.
    `tests/test_web_static.py` drives the page's effort card over the same
    `/config`.
    """
    from test_web_commands import FAKE_COMMAND, resolved_replies
    import shlex
    with tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        replies = home / "replies.json"
        replies.write_text(json.dumps(resolved_replies()), encoding="utf-8")
        log, marker = home / "calls.jsonl", home / "started.log"
        preamble = (
            f"#!{sys.executable}\n"
            "import io, json, sys\n"
            "argv = sys.argv[1:]\n"
            "prompt = sys.stdin.read()\n"
            "sys.stdin = io.StringIO(prompt)\n"
            f"markers = json.loads(open({str(replies)!r}, encoding='utf-8').read())['markers']\n"
            "kind = next((n for n, needle in markers.items() if needle in prompt), '')\n"
            f"with open({str(log)!r}, 'a', encoding='utf-8') as handle:\n"
            "    handle.write(json.dumps({'kind': kind, 'argv': argv}) + '\\n')\n"
            f"sys.argv = [sys.argv[0], {str(marker)!r}, {str(replies)!r}, *argv]\n")
        (home / "bin").mkdir()
        for name in ("claude", "claude-wrapper"):
            program = home / "bin" / name
            program.write_text(preamble + FAKE_COMMAND, encoding="utf-8")
            program.chmod(0o755)

        def row(program: str, alias: str, *extra: str, discovered: bool = False) -> dict:
            command = shlex.join([str(home / "bin" / program), "--print",
                                  *config.RESULT_ARGS, "--model", alias, *extra])
            out = {"label": f"{program} {alias}", "command": command,
                   "window": 200000, "model": alias, "envelope": config.ENVELOPE_RESULT,
                   "web_tools": []}
            if discovered:
                out["discovered"] = True
            return out

        rows = {f"claude-{alias}": row("claude", alias, discovered=True)
                for alias in ("haiku", "sonnet", "opus", "fable")}
        rows.update({"wrapper": row("claude-wrapper", "opus"),
                     "pinned": row("claude", "opus", config.EFFORT_FLAG, "xhigh")})
        path = home / "commands.json"
        path.write_text(json.dumps({"version": 1, "routes": rows}), encoding="utf-8")
        os.chmod(path, 0o600)
        from llossless.web import commands
        store = commands.Commands(path)
        with FakeEndpoint(Script(**CLEAN)) as endpoint_url:
            environ = {"LLOSSLESS_BASE_URL": endpoint_url,
                       "LLOSSLESS_STRUCTURED": "prompt", **(environ_extra or {})}
            built = server.build(port=0, work_dir=home / "work", environ=environ,
                                 commands=store)
            thread = server.background(built)

            def calls() -> list[dict]:
                if not log.exists():
                    return []
                return [json.loads(line) for line in
                        log.read_text(encoding="utf-8").splitlines()]
            try:
                yield built, calls
            finally:
                built.shutdown()
                built.server_close()
                built.store.close()
                thread.join(timeout=5)


def route_submission(route: str, **fields) -> dict:
    """A two-document merge through `route`, naming no model: the route decides it."""
    body = {"documents": [{"name": LABELS[0], "text": SOURCE_A},
                          {"name": LABELS[1], "text": SOURCE_B}],
            "base": LABELS[0], "command_route": route}
    body.update(fields)
    return body


def _flag(argv: list[str], flag: str) -> str | None:
    return argv[argv.index(flag) + 1] if flag in argv else None


def test_config_serves_each_route_s_effort_levels_and_default() -> None:
    """`/config` says, per route, which merge levels a request may
    choose and what it gets choosing none.

    Opus defaults to `high` and Sonnet to `medium`; a program
    this build has not read takes none, and so does a route whose own command
    names a level. The server's own `LLOSSLESS_EFFORT_MERGE` moves the default,
    because it is what a request naming none would get. Only the discovered
    Opus row is marked `preselect`. `max` is the fifth stop, on every
    route that takes a level at all -- nobody measured it, which is a fact the
    page's card states, not a reason to leave it off the levels a route serves.

    Haiku serves neither shape: no `levels` list, because it
    has none to choose among, and no `default` naming a level it cannot carry
    either. `single_level` and the operator's own label instead.
    """
    levels = ["low", "medium", "high", "xhigh", "max"]
    shape = {"levels": levels, "not_at_sourced": ["low"]}
    with claude_routes() as (built, _calls):
        payload = as_json(request(f"{built.url}{api.API_PREFIX}/config")[2]) or {}
        routes = {row["id"]: row for row in payload.get("commands", {}).get("routes", [])}
    check(set(routes) == {"claude-haiku", "claude-sonnet", "claude-opus", "claude-fable",
                          "wrapper", "pinned"},
          f"all six routes must be served: {sorted(routes)}")
    check(routes.get("claude-opus", {}).get("effort") == {**shape, "default": "high"},
          f"the Opus route takes the five levels and defaults to high: "
          f"{routes.get('claude-opus', {}).get('effort')}")
    for alias in ("sonnet", "fable"):
        check(routes.get(f"claude-{alias}", {}).get("effort") == {**shape, "default": "medium"},
              f"the {alias} route defaults to medium: "
              f"{routes.get(f'claude-{alias}', {}).get('effort')}")
    check(routes.get("claude-haiku", {}).get("effort") ==
          {"single_level": True, "label": config.SINGLE_LEVEL_LABEL},
          f"the Haiku route names its one level, not a scale: "
          f"{routes.get('claude-haiku', {}).get('effort')}")
    for name in ("wrapper", "pinned"):
        check(name in routes and routes[name].get("effort") is None,
              f"{name} takes no level from a request, so it serves none: "
              f"{routes.get(name, {}).get('effort', 'absent')}")
    check([name for name, row in routes.items() if row.get("preselect")] == ["claude-opus"],
          f"only the discovered Opus row is preselected: "
          f"{[(name, row.get('preselect')) for name, row in routes.items()]}")
    with claude_routes({"LLOSSLESS_EFFORT_MERGE": "xhigh"}) as (built, _calls):
        payload = as_json(request(f"{built.url}{api.API_PREFIX}/config")[2]) or {}
        routes = {row["id"]: row for row in payload.get("commands", {}).get("routes", [])}
    check((routes.get("claude-opus", {}).get("effort") or {}).get("default") == "xhigh",
          f"the server's own LLOSSLESS_EFFORT_MERGE is the default a request "
          f"without a level gets: {routes.get('claude-opus', {}).get('effort')}")
    check(routes.get("claude-haiku", {}).get("effort") ==
          {"single_level": True, "label": config.SINGLE_LEVEL_LABEL},
          f"LLOSSLESS_EFFORT_MERGE must not move Haiku, which has no default "
          f"to move: {routes.get('claude-haiku', {}).get('effort')}")


def test_a_request_s_effort_is_refused_where_no_route_can_carry_it() -> None:
    """`400 bad_effort`, naming the field, nothing started.

    Must fire: no route at all (including `max` with no route), a level
    outside the five, a number, an empty string, a route through a program
    this build has not read, a route whose own command names a level, and
    the Haiku route -- it has one level and no scale a
    request could name.
    Must not fire: `high` and `max` are both accepted on the Opus
    route -- nobody having measured `max` is a fact the card states, not a
    reason for the server to refuse it.
    """
    with claude_routes() as (built, calls):
        url = f"{built.url}{api.API_PREFIX}/runs"
        cases = [
            ("no route", {**a_submission(), "effort": "high"}),
            ("max with no route", {**a_submission(), "effort": "max"}),
            ("the Haiku route", route_submission("claude-haiku", effort="medium")),
            ("an unknown level", route_submission("claude-opus", effort="extreme")),
            ("a number", route_submission("claude-opus", effort=3)),
            ("an empty string", route_submission("claude-opus", effort="")),
            ("a program this build has not read", route_submission("wrapper", effort="high")),
            ("a route whose command names a level", route_submission("pinned", effort="high")),
        ]
        for what, body in cases:
            status, _, answer = request(url, method="POST", payload=body)
            code = (as_json(answer) or {}).get("error", {})
            code = code.get("code") if isinstance(code, dict) else (as_json(answer) or {}).get("code")
            check(status == 400 and code == "bad_effort",
                  f"{what}: effort must be refused as bad_effort; got {status} "
                  f"{answer[:200]!r}")
            check("effort" in answer.decode("utf-8", "replace"),
                  f"{what}: the refusal must name the field: {answer[:200]!r}")
        started = len(calls())
        status, _, answer = request(url, method="POST",
                                    payload=route_submission("claude-opus", effort="high"))
        status_max, _, answer_max = request(url, method="POST",
                                            payload=route_submission("claude-opus", effort="max"))
    check(started == 0, f"a refused request must start nothing; {started} calls ran")
    check(status == 202, f"the same level on the Opus route is accepted: {status} "
                         f"{answer[:200]!r}")
    check(status_max == 202, f"max on the Opus route must be accepted as a valid effort level: "
                             f"{status_max} {answer_max[:200]!r}")


def test_a_request_s_effort_reaches_the_merge_argv_and_is_recorded_as_its_choice() -> None:
    """Through the server and a fake `claude`: the level the page sent is
    the level the merge was started with, and the report says whose it was.

    `effort: "xhigh"` on the Opus route: every merge call's argv carries
    `--effort xhigh`, every decompose and verify call keeps `low`, the report's
    `decoding.effort_requested` is `{"merge": "xhigh"}`, its Decoding row says
    the requester chose it, and the banner event names `xhigh`. The control,
    which is the must-fire half: the same route with no `effort` starts the
    merge at its own default `high` and records no requested level. A third run,
    `effort: "max"`, proves the fifth stop reaches the argv the same way
    and only for the merge -- decompose and verify keep `low` beside it too.
    """
    with claude_routes() as (built, calls):
        job_id, chosen = a_finished_run_body(built, route_submission("claude-opus", effort="xhigh"))
        chosen_calls = calls()
        banner = [event for event in sse_events(built, job_id) if event.get("kind") == "banner"]
        page = request(f"{built.url}{api.API_PREFIX}/runs/{job_id}/report.html")[2].decode(
            "utf-8", "replace")
        _job, plain = a_finished_run_body(built, route_submission("claude-opus"))
        plain_calls = calls()[len(chosen_calls):]
        _job, maxed = a_finished_run_body(built, route_submission("claude-opus", effort="max"))
        max_calls = calls()[len(chosen_calls) + len(plain_calls):]
    for what, payload, runs, level in (("chosen", chosen, chosen_calls, "xhigh"),
                                       ("default", plain, plain_calls, "high"),
                                       ("max", maxed, max_calls, "max")):
        check(payload.get("state") == jobs.DONE,
              f"the {what} run must finish: {payload.get('state')!r} {payload.get('error')!r}")
        merges = [c["argv"] for c in runs if c["kind"] == "merge"]
        others = [c["argv"] for c in runs if c["kind"] not in ("merge", "")]
        check(merges and all(_flag(argv, config.EFFORT_FLAG) == level for argv in merges),
              f"{what}: every merge call must be started at --effort {level}: {merges}")
        check(others and all(_flag(argv, config.EFFORT_FLAG) == "low" for argv in others),
              f"{what}: decompose and verify keep low: {[_flag(a, config.EFFORT_FLAG) for a in others]}")
    decoding = ((chosen.get("report") or {}).get("provenance") or {}).get("decoding") or {}
    check(decoding.get("effort", {}).get("merge") == "xhigh"
          and decoding.get("effort_requested") == {"merge": "xhigh"},
          f"the report must record xhigh, and record it as the requester's: {decoding}")
    plain_decoding = ((plain.get("report") or {}).get("provenance") or {}).get("decoding") or {}
    check(plain_decoding.get("effort", {}).get("merge") == "high"
          and "effort_requested" not in plain_decoding,
          f"a run that chose nothing records the default and no choice: {plain_decoding}")
    max_decoding = ((maxed.get("report") or {}).get("provenance") or {}).get("decoding") or {}
    check(max_decoding.get("effort", {}).get("merge") == "max"
          and max_decoding.get("effort_requested") == {"merge": "max"},
          f"the report must record max, and record it as the requester's: {max_decoding}")
    check(banner and (banner[0].get("fields") or {}).get("effort") == "xhigh",
          f"the banner event must name the merge's level: {banner[:1]}")
    check("merge=xhigh chosen by the requester" in page,
          "the report's rendered Decoding row must say whose choice the level was")


def a_finished_run_body(built, body: dict) -> tuple[str, dict]:
    """`a_finished_run` for a body built here rather than by `a_submission`."""
    status, _, answer = request(f"{built.url}{api.API_PREFIX}/runs", method="POST",
                                payload=body)
    if status != 202:
        check(False, f"the submit was refused with {status}: {answer[:300]!r}")
        return "", {}
    job_id = as_json(answer)["id"]
    url = f"{built.url}{api.API_PREFIX}/runs/{job_id}"
    if not wait_for(lambda: (as_json(request(url)[2]) or {}).get("state")
                    in ("done", "failed")):
        check(False, f"run {job_id} never reached a terminal state")
        return job_id, {}
    return job_id, as_json(request(url)[2])


# --------------------------------------------------------------------------
# entry points
# --------------------------------------------------------------------------


def test_web_server_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


# --------------------------------------------------------------------------
# the persisted queue, through a real server process that is killed
# --------------------------------------------------------------------------

# A seed for the shipped code inside the server process: the one defect the
# kill test exists for, a restart that puts a running job back on the queue.
# Applied by the launcher below before `cli.main` runs, so what is patched is
# the module the real command imports.
REQUEUE_SEED = """
import llossless.web.jobs as _jobs
_shipped = _jobs.JobStore._restore
def _requeue(self, record, now):
    if record["state"] == _jobs.RUNNING:
        record = dict(record, state=_jobs.QUEUED)
    return _shipped(self, record, now)
_jobs.JobStore._restore = _requeue
"""


def a_loopback_port() -> int:
    """A free port, bound here first so the socket guard lets this process dial it.

    `socket_guard` permits a connect only to the configured endpoint or to a
    loopback port this process bound. The server is another process, so the
    port is bound and released here and handed to it with `--port`.
    """
    import socket
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.bind(("127.0.0.1", 0))
    port = probe.getsockname()[1]
    probe.close()
    return port


class ServerProcess:
    """`llossless serve` in a subprocess, on a work directory that outlives it."""

    def __init__(self, home: Path, work: Path, endpoint_url: str, *,
                 seed: str = "") -> None:
        import subprocess
        self.port = a_loopback_port()
        self.base = f"http://127.0.0.1:{self.port}"
        environ = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / "config"),
            "XDG_CACHE_HOME": str(home / "cache"),
            "PYTHONPATH": str(ROOT / "src"),
            "LLOSSLESS_BASE_URL": endpoint_url,
            "LLOSSLESS_STRUCTURED": "prompt",
        }
        launcher = (seed + "\nimport sys\nfrom llossless.cli import main\n"
                    "sys.exit(main(sys.argv[1:]))\n")
        self.process = subprocess.Popen(
            [sys.executable, "-c", launcher, "serve", "--port", str(self.port),
             "--work-dir", str(work), "--retention", "3600"],
            cwd=ROOT, env=environ, stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE, text=True)
        self.lines: list[str] = []
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()
        if not wait_for(lambda: any("serving http://" in line for line in self.lines)
                        or self.process.poll() is not None):
            raise AssertionError("the server never said it was serving")

    def _read(self) -> None:
        for line in self.process.stderr:
            self.lines.append(line.rstrip("\n"))

    @property
    def banner(self) -> str:
        return "\n".join(self.lines)

    def setup_token(self) -> str:
        found = re.search(r"#setup=([A-Za-z0-9_-]+)", self.banner)
        return found.group(1) if found else ""

    def kill(self) -> None:
        import signal
        self.process.send_signal(signal.SIGKILL)
        self.process.wait(timeout=PATIENCE)

    def stop(self) -> None:
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except Exception:  # noqa: BLE001 - a stuck server is killed
                self.process.kill()
                self.process.wait(timeout=10)

    def call(self, path: str, who=None, **kwargs):
        return request(f"{self.base}{api.API_PREFIX}{path}", headers=who, **kwargs)

    def sign_in(self, username: str, password: str) -> dict:
        from llossless.web import accounts
        status, _, body = self.call("/session", method="POST", payload={
            "username": username, "password": password, "token": True})
        payload = as_json(body) or {}
        if status != 200 or "token" not in payload:
            raise AssertionError(f"could not sign in as {username}: {status} {body[:200]!r}")
        return {accounts.SESSION_HEADER: payload["token"]}


ALICE = ("alice", "probe-password-alice-660")
BOB = ("bob", "probe-password-bob-660")


def killed_server_verdict(seed: str = "", *, full: bool = True) -> list[str]:
    """Three queued runs, SIGKILL while the second runs, restart. What is wrong?"""
    problems: list[str] = []
    script = Script(**CLEAN)

    def slow(body: dict, n: int):
        time.sleep(0.4)
        return script(body, n)

    with FakeEndpoint(slow) as endpoint_url, tempfile.TemporaryDirectory() as raw:
        home, work = Path(raw) / "home", Path(raw) / "work"
        home.mkdir()
        first = ServerProcess(home, work, endpoint_url)
        try:
            status, _, body = first.call("/setup", method="POST", payload={
                "token": first.setup_token(), "username": ALICE[0],
                "password": ALICE[1]})
            if status not in (200, 201):
                return [f"setup answered {status}: {body[:200]!r}"]
            alice = first.sign_in(*ALICE)
            first.call("/accounts", who=alice, method="POST",
                       payload={"username": BOB[0], "password": BOB[1]})
            ids = []
            for _ in range(3):
                status, _, body = first.call("/runs", who=alice, method="POST",
                                             payload=a_submission())
                ids.append((as_json(body) or {}).get("id", ""))
                if status != 202:
                    return [f"a submit answered {status}: {body[:200]!r}"]

            def state(job_id):
                return (as_json(first.call(f"/runs/{job_id}", who=alice)[2]) or {}).get("state")

            log = work / ids[1] / jobs.EVENTS_JSONL
            if not wait_for(lambda: state(ids[0]) == "done" and state(ids[1]) == "running"
                            and log.is_file() and '"kind": "done"' in log.read_text()):
                return ["the first run never finished, or the second never got a step done"]
            queued = as_json(first.call(f"/runs/{ids[2]}", who=alice)[2]) or {}
            if (queued.get("queue_position"), queued.get("queue_length")) != (1, 1):
                problems.append(f"before the kill the third run is not position 1 "
                                f"of 1: {queued.get('queue_position')}, "
                                f"{queued.get('queue_length')}")
            first.kill()
        finally:
            first.stop()

        second = ServerProcess(home, work, endpoint_url, seed=seed)
        try:
            alice = second.sign_in(*ALICE)
            bob = second.sign_in(*BOB)
            runs = (as_json(second.call("/runs", who=alice)[2]) or {}).get("runs", [])
            if [run.get("id") for run in runs] != ids:
                problems.append(f"the run list after the restart is not the three "
                                f"runs in order: {[r.get('id') for r in runs]}")
            states = {run.get("id"): run for run in runs}
            one, two = states.get(ids[0], {}), states.get(ids[1], {})
            if one.get("state") != "done":
                problems.append(f"the finished run is {one.get('state')}")
            if two.get("state") != "interrupted":
                problems.append(f"the killed run is {two.get('state')}, not interrupted")
            elif not ("not complete" in (two.get("error") or "")
                      and two.get("retryable") is True):
                problems.append(f"the interrupted run does not say it is incomplete "
                                f"or cannot be retried: {two}")
            if "1 interrupted" not in second.banner or "1 queued and resumed" not in second.banner:
                problems.append("the banner does not say what the reload found")
            index = work / jobs.INDEX_JSON
            import stat as stat_module
            if stat_module.S_IMODE(index.stat().st_mode) != jobs.FILE_MODE:
                problems.append("the index is not owner-only")
            if (as_json(second.call("/runs", who=bob)[2]) or {}).get("runs") != []:
                problems.append("bob sees runs that are alice's after the restart")
            if second.call(f"/runs/{ids[0]}", who=bob)[0] != 404:
                problems.append("bob can read alice's reloaded run")
            if second.call(f"/runs/{ids[1]}/retry", who=bob, method="POST")[0] != 404:
                problems.append("bob can retry alice's run")
            if not full:
                return problems

            def state(job_id):
                return (as_json(second.call(f"/runs/{job_id}", who=alice)[2]) or {}).get("state")

            if not wait_for(lambda: state(ids[2]) == "done"):
                problems.append(f"the queued run never ran after the restart: {state(ids[2])}")
            if state(ids[1]) != "interrupted":
                problems.append("the interrupted run changed state on its own")
            if second.call(f"/runs/{ids[0]}/report.html", who=alice)[0] != 200:
                problems.append("the finished run's report is not served after the restart")
            status, headers, body = second.call(f"/runs/{ids[1]}/retry", who=alice,
                                                method="POST")
            retried = as_json(body) or {}
            if status != 202 or retried.get("retry_of") != ids[1] \
                    or retried.get("id") in ids:
                problems.append(f"Retry answered {status}: {body[:200]!r}")
            elif not wait_for(lambda: state(retried["id"]) == "done"):
                problems.append("the retried run never finished")
            if second.call(f"/runs/{ids[0]}/retry", who=alice, method="POST")[0] != 409:
                problems.append("a finished run was offered a retry")
        finally:
            second.stop()
    return problems


def test_a_killed_server_restarts_with_its_queue() -> None:
    """SIGKILL mid-run, restart: done listed, running interrupted, queued runs.

    The real command in a real process, killed the way a crash kills it, and
    restarted on the same work directory. Must fire on the shipped code seeded
    in the server process with the defect this exists for: a restart that
    re-queues the running job, billing its calls twice.
    """
    problems = killed_server_verdict()
    check(not problems, "after a SIGKILL: " + "; ".join(problems))
    seeded = killed_server_verdict(REQUEUE_SEED, full=False)
    check(any("not interrupted" in problem for problem in seeded),
          f"must fire: a server that re-queues a killed run passed: {seeded}")


def test_serve_refuses_a_corrupt_index_and_names_the_way_out() -> None:
    """`llossless serve` exits 2 on an unreadable index and deletes nothing."""
    with tempfile.TemporaryDirectory() as raw:
        work = Path(raw) / "work"
        work.mkdir()
        keep = work / ("d" * 32)
        keep.mkdir()
        (keep / jobs.SOURCES_JSON).write_text("{}", encoding="utf-8")
        (work / jobs.INDEX_JSON).write_text('{"version": 1, "jobs": [', encoding="utf-8")
        out = io.StringIO()
        code = server.serve(port=0, work_dir=work, retention_seconds=3600,
                            environ={}, token="",
                            credentials_path=Path(raw) / "credentials.json",
                            accounts_path=Path(raw) / "accounts.json",
                            commands_path=Path(raw) / "commands.json", stream=out)
        said = out.getvalue()
        check(code == 2, f"serve must exit 2 on a corrupt index; got {code}")
        check(str(work / jobs.INDEX_JSON) in said and "move that file aside" in said,
              f"the refusal must name the file and the way out: {said!r}")
        check((keep / jobs.SOURCES_JSON).is_file(),
              "a refused start deleted a job directory")


class Seeded:
    """Patch one attribute of the shipped code for a `with`, and put it back."""

    def __init__(self, owner, name: str, value) -> None:
        self.owner, self.name, self.value = owner, name, value

    def __enter__(self):
        self.before = getattr(self.owner, self.name)
        setattr(self.owner, self.name, self.value)
        return self

    def __exit__(self, *exc_info) -> None:
        setattr(self.owner, self.name, self.before)


def failed_bind_verdict() -> list[str]:
    """A restart whose port is taken must not run the queue it reloaded."""
    import socket
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as raw:
        work = Path(raw) / "work"
        held = threading.Event()

        def hold(job, workspace):
            held.wait(timeout=PATIENCE)

        store = jobs.JobStore(work, environ={}, runner=hold).start()
        try:
            store.submit(jobs.MergeRequest(
                documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                overrides={"LLOSSLESS_MODEL": "test-model",
                           "LLOSSLESS_MERGE_MODEL": "test-model"}))
            queued = store.submit(jobs.MergeRequest(
                documents={"a.md": SOURCE_A, "b.md": SOURCE_B},
                overrides={"LLOSSLESS_MODEL": "test-model",
                           "LLOSSLESS_MERGE_MODEL": "test-model"}))
            import shutil
            copy = Path(raw) / "copy"
            shutil.copytree(work, copy)
        finally:
            held.set()
            store.close()
        taken = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        taken.bind(("127.0.0.1", 0))
        taken.listen(1)
        try:
            server.build(port=taken.getsockname()[1], work_dir=copy, environ={})
            problems.append("a build on a taken port succeeded")
        except OSError:
            pass
        finally:
            taken.close()
        index = json.loads((copy / jobs.INDEX_JSON).read_text(encoding="utf-8"))
        state = {r["id"]: r["state"] for r in index["jobs"]}.get(queued.id)
        if state != jobs.QUEUED:
            problems.append(f"the queued run is {state} after a failed bind; the "
                            f"store ran the queue before it could serve it")
    return problems


def test_a_restart_that_cannot_bind_runs_nothing() -> None:
    """Found by killing a real server and restarting it on its own port.

    The port sits in TIME_WAIT after a crash, the bind fails, and the store
    that was started before the bind ran the reloaded queue and died under it.
    Must fire on the shipped `build` with the store started before the bind.
    """
    problems = failed_bind_verdict()
    check(not problems, "failed bind: " + "; ".join(problems))
    shipped = jobs.JobStore.__init__

    def eager(self, *args, **kwargs):
        shipped(self, *args, **kwargs)
        self.start()

    with Seeded(jobs.JobStore, "__init__", eager):
        seeded = failed_bind_verdict()
    check(any("ran the queue" in problem for problem in seeded),
          f"must fire: a store started before the bind passed: {seeded}")


def test_serve_refuses_a_work_directory_another_server_owns() -> None:
    """Two servers on one index is refused before anything in it is read."""
    with tempfile.TemporaryDirectory() as raw:
        work = Path(raw) / "work"
        owner = jobs.JobStore(work, environ={})
        try:
            out = io.StringIO()
            code = server.serve(port=0, work_dir=work, retention_seconds=3600,
                                environ={}, token="",
                                credentials_path=Path(raw) / "credentials.json",
                                accounts_path=Path(raw) / "accounts.json",
                                commands_path=Path(raw) / "commands.json", stream=out)
            check(code == 2 and "already using the work directory" in out.getvalue(),
                  f"a second server on an owned work directory must exit 2 and "
                  f"say why; got {code}: {out.getvalue()!r}")
        finally:
            owner.close()


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_server_offline" \
                and callable(function):
            function()
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web server: {checks} checks pass over {len(api.SUBMIT_FIELDS)} submit "
          f"fields and the {api.API_PREFIX} contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
