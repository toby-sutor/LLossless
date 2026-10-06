#!/usr/bin/env python3
"""The command-route allowlist: the file, the refusals, and two seeded attacks.

`src/llossless/web/commands.py` is the answer to one question -- how does a
browser get to use a flat-rate subscription CLI without a form that accepts a
command and a server that runs it. The answer is that it does not get to name a
command at all: the operator writes the routes into a file on the server, the
page is served their labels, and a request names one by **id**.

Everything here exists because that arrangement is only worth as much as its
weakest refusal, and a refusal that has never been driven is a refusal nobody
has checked. Four of these checks are the ones worth naming.

**Two seeded attacks, and the command that must not run.** One posts a command
string straight at the API in five shapes, bypassing the page entirely; the
other posts an id this server does not have. Both must be refused, and -- the
half that is easy to forget -- neither may execute anything. The fake command
writes a line to a marker file every time it starts, so "nothing ran" is a
measurement rather than an assumption.

**And a control that must fire.** A run that names the real id has to create
that marker, or the two assertions above are assertions about a program that
could never have started, and would stay green with the whole backend deleted.

**The command never reaches a browser.** Asserted against `/config`, against
the served report, and against the HTML download, with the string present in
the store the whole time so the search has something to find.

**The route reaches the record.** A run that went out over a command backend
says so in its banner event, in `provenance.endpoint.location`, and by the
operator's own label in `provenance.endpoint.route` -- which is what a reader
comes back to a week later to find out whether the merge spent a subscription
or a metered API.

**And the same three properties again for discovery.** The page can now
switch a route on, so there is a second write path and it gets the same
treatment: an id that is not in `KNOWN_TOOLS` is refused in five shapes -- a
real program on this `PATH` that is not in the table, two spellings of a path,
a command line, and an id that belongs to the operator's own file -- none of
them writes a route and none of them starts a program. The must-fire half is
`HoledCommands`, which removes exactly one call, `check_tool_id`, and is the
obvious wrong implementation of this feature rather than a contrived one: the
same `PUT` then writes a route, the same submit runs it, and the marker file
appears.

The resolved path `shutil.which` answers with is searched for in every served
body while the store holds it, which is the same shape one mechanism over: an
absolute path under whichever account the server runs as is what
the release scanner refuses, and `discovered()` reduces it to a
boolean before anything is served.

**And who may switch one on.** A command route runs as the server process with
that machine's credentials and is shared by every account here, so it is the
operator's to configure. Driven with two real accounts and two real sessions
rather than by calling `_operator`: a member is refused `not_operator`, nothing
is written, and the operator's request over the same store is accepted -- or
the refusal is a refusal of a route nobody could have used.

No live model calls, ever, and no real vendor CLI. The fake command is a
generated Python script that reads the prompt on stdin and prints a canned
answer, chosen by the same prompt markers `tests/test_cli.py`'s scripted
endpoint uses -- imported from there rather than copied, because two tables of
prompt markers is how the second one stops matching the prompts. The discovery
probes run the same body with the marker baked in, because a discovered route's
command is the resolved path and nothing else -- there is nowhere for an
argument to come from, which is the point.

Run with `python3 tests/test_web_commands.py`, or collect with pytest.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shlex
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs. This module binds two loopback sockets
# of its own -- the server under test and nothing else -- and starts a
# subprocess that opens none; `tests/test_socket_guard.py` asserts every test
# module states it in exactly this shape.
socket_guard.install()

from llossless import config, provenance  # noqa: E402
from llossless.web import accounts as user_accounts  # noqa: E402
from llossless.web import api, commands, credentials, jobs, redact, server  # noqa: E402

from test_cli import CLEAN, SOURCE_A, SOURCE_B, Script  # noqa: E402

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# scaffolding
# --------------------------------------------------------------------------

# Same figure as `tests/test_web_server.py` and for the same reason: long
# enough that a loaded machine running the whole suite does not fail a check
# about a state transition, short enough that a genuine hang is reported as one.
PATIENCE = 60.0
READ_CAP = 256 * 1024

LABELS = ("notes-a.md", "notes-b.md")

# The label the operator wrote, and the one the whole presentation half of this
# milestone rests on. It names a route to a model rather than a model, which is
# the distinction that stops somebody firing at a metered API believing they
# were on a plan.
SUBSCRIPTION_LABEL = "Opus 5 - Subscription"

# The model the fake route pins. A route must state one -- a command backend
# cannot be asked which model answered it -- and the recorded model is
# compared against this rather than against a copy.
FAKE_MODEL = "opus-under-a-plan"

# An address no run here may contact and no message may name. Used as the
# server's `LLOSSLESS_BASE_URL` so that a command run which fell back to the
# HTTP path -- or merely *reported* the HTTP path -- is visible as this string
# turning up somewhere it has no business being.
#
# A reserved *name* rather than a reserved address. TEST-NET-3 stood here
# first, and it is reserved for documentation by RFC 5737 -- but the leak scan
# this repository runs over its own tracked files carves out reserved names and
# not reserved literals, so `tests/test_client.py` and the manifest
# auditor both reported this file as carrying a hosted endpoint URL. The
# carve-out is deliberately narrow (see `secret_patterns`) and widening a
# security detector to admit a fixture is the wrong way round, so the fixture
# moved instead: `.invalid` is guaranteed never to resolve by RFC 6761, which
# is the same promise TEST-NET-3 makes and one the scan already recognises.
#
# The host is a constant because the assertions below test for its *absence*,
# and an absence asserted against a copied literal is an absence that stops
# being checked the moment the address it was copied from changes.
UNUSED_HOST = "never-contacted.invalid"

# The shape a command usually has: an absolute path to a program, which is the
# whole reason `describe()` must never serve one.
#
# A path under a user's home directory stood here first, and was the more
# realistic fixture -- which is exactly why it had to go.
# The release scanner refuses that shape anywhere in the published
# set, and this file publishes. Its only exemption is
# `scripts/stream_redact.py`, which defines the rule and so contains the shape
# by construction, pinned there by count and digest; widening the exemption so
# a fixture could pass would blind the scan to the class it exists for. That
# class is not a credential -- it names a person and a machine layout, and 124
# files under `arms/` once carried one.
#
# The comment above is written not to contain the shape either. That is not
# dodging the scanner: there is nothing here the rule needs to quote, and a
# file that has to be exempted to describe its own fixture is the second file
# the detector cannot read. `/opt` keeps every property the checks need --
# absolute, local, a program, a distinctive stem to search a served body for --
# and carries none of what the scan refuses.
#
# A constant because three checks assert this string's *absence* from a served
# body, and an absence asserted against a copied literal stops being checked
# the moment one copy changes.
PRIVATE_COMMAND = "/opt/llossless/bin/claude-wrapper.sh --print"
PRIVATE_STEM = "claude-wrapper"
UNUSED_ENDPOINT = f"http://{UNUSED_HOST}:1234/v1"

# The fake command. It appends one line to a marker file every time it starts,
# which is what makes "nothing was executed" a measurement: the two attack
# probes below assert the file is still absent, and the control probe asserts
# it is not.
#
# Written out here rather than imported, because it has to run in a subprocess
# that shares nothing with this interpreter. What it must not do is hold a
# second copy of the prompt markers: those are written into its replies file
# from `Script.MARKERS`, so a reworded prompt breaks this the same way it
# breaks the scripted endpoint.
FAKE_COMMAND = '''\
import json, sys

marker, replies_path = sys.argv[1], sys.argv[2]
with open(marker, "a", encoding="utf-8") as handle:
    handle.write("started\\n")

replies = json.loads(open(replies_path, encoding="utf-8").read())
prompt = sys.stdin.read()
kind = ""
for name, needle in replies["markers"].items():
    if needle in prompt:
        kind = name
        break
if not kind:
    sys.stderr.write("unrecognised prompt\\n")
    raise SystemExit(3)

answer = replies["replies"][kind]
# The same rule the scripted endpoint follows: supply the empty answer for a
# required merge key the fixture omitted, and only where the request asked for
# it. A real compliant model answers the schema it was given.
if kind == "merge":
    payload = json.loads(answer)
    for key, empty in (("additions", []), ("mismatch", "")):
        if '"' + key + '"' in prompt and key not in payload:
            payload[key] = empty
    answer = json.dumps(payload)
# The one flag this fake honours, because production now depends on it. The
# discovered routes carry `--output-format json`, and `claude` answers that
# with a single result envelope: the text under `result`, the token block and
# `server_tool_use` under `usage`. A stub that wrote bare text while being
# passed the flag would be testing a CLI nobody ships.
# Written with `dict(...)` and not a literal, because `PROBE_TOOL` runs this
# source through `str.format` and a brace in it would be read as a field.
if "--output-format" in sys.argv and "json" in sys.argv:
    tools = dict(web_search_requests=0, web_fetch_requests=0)
    used = dict(input_tokens=11, output_tokens=7, server_tool_use=tools)
    # `num_turns` beside `result`, and the pair reproduces the measured
    # disagreement: `server_tool_use` stays at zero whatever happened, because
    # it counts a vendor's server-side tools and a CLI's own `WebFetch` runs
    # locally, and the turn count is the one that moves. Two turns with
    # no tool use and three with one fetch: two is the operator's plain
    # answer and the harder of its two measured readings, because a fake at
    # one would pass under the old floor as well as the new.
    #
    # Keyed on its own flag rather than on the allowlist, so the grant and the
    # tool use are two variables. They are two in production as well -- a model
    # that was permitted a tool may still not reach for it, which is the case
    # the level has to report loudest -- and a fake that tied them together
    # could not produce it.
    turns = 3 if "--simulate-tool-use" in sys.argv else 2
    envelope = dict(type="result", subtype="success", is_error=False,
                    result=answer, num_turns=turns, usage=used)
    # A result envelope that carries no turn count. `sourced` refuses a
    # command that cannot ask for the envelope at all; this is the case the
    # refusal cannot see coming -- the envelope arrives and the field is not
    # in it -- and the run has to say so rather than look normal.
    if "--omit-turns" in sys.argv:
        envelope.pop("num_turns")
    answer = json.dumps(envelope)
sys.stdout.write(answer)
'''


def resolved_replies() -> dict:
    """`CLEAN`, with its one callable resolved, plus the prompt markers.

    `CLEAN["decompose"]` is a function of the call index and answers the same
    thing on every branch, so resolving it once here is not a simplification of
    the fixture -- it is the fixture, evaluated.
    """
    replies = {}
    for kind, reply in CLEAN.items():
        replies[kind] = reply(1) if callable(reply) else reply
    return {"markers": dict(Script.MARKERS), "replies": replies}


@contextlib.contextmanager
def routes_file(rows: dict, *, mode: int = 0o600):
    """A `commands.json` holding `rows`, and a `Commands` over it."""
    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "commands.json"
        path.write_text(json.dumps({"version": 1, "routes": rows}),
                        encoding="utf-8")
        os.chmod(path, mode)
        yield commands.Commands(path), path


@contextlib.contextmanager
def fake_route(*, command_suffix: str = "", **overrides):
    """A store holding one route that runs the fake command. Yields the parts.

    Yields `(store, marker_path, command)`. `marker_path` does not exist until
    the command has been started at least once, which is the whole mechanism
    behind the two attack probes.

    `command_suffix` is appended to the argv rather than being a row field:
    `_row` refuses a field this build does not read, and a grant has to be in
    the *command* for the route's own `web_tools` check to accept it.
    """
    with tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        script = home / "fake_cli.py"
        script.write_text(FAKE_COMMAND, encoding="utf-8")
        replies = home / "replies.json"
        replies.write_text(json.dumps(resolved_replies()), encoding="utf-8")
        marker = home / "started.log"
        command = " ".join(shlex.quote(part) for part in
                           (sys.executable, str(script), str(marker),
                            str(replies))) + command_suffix
        row = {"label": SUBSCRIPTION_LABEL, "command": command,
               "window": 200000, "model": FAKE_MODEL}
        row.update(overrides)
        path = home / "commands.json"
        path.write_text(json.dumps({"version": 1, "routes": {"opus-sub": row}}),
                        encoding="utf-8")
        os.chmod(path, 0o600)
        yield commands.Commands(path), marker, command


@contextlib.contextmanager
def live_server(store, **kwargs):
    """A serving server wired to `store` and to an endpoint that does not exist.

    `LLOSSLESS_BASE_URL` is `UNUSED_ENDPOINT` on purpose. Every run in this
    module goes through a command, so nothing should ever dial it -- and the
    address being unroutable rather than absent is what makes a fallback to the
    HTTP path fail loudly instead of quietly finding something to talk to.
    """
    with tempfile.TemporaryDirectory() as raw:
        environ = {"LLOSSLESS_BASE_URL": UNUSED_ENDPOINT,
                   "LLOSSLESS_MODEL": "test-model",
                   "LLOSSLESS_MERGE_MODEL": "test-model",
                   # A run-wide stated window, which is an ordinary thing for
                   # an operator to configure -- and it is here to take an
                   # accidental defence *out* of the picture. Without it,
                   # `Settings.__post_init__` refuses any command backend that
                   # has not been told a window, so an injected command would
                   # never reach `backend.py` even through a hole in the
                   # allowlist, and the probe below would be measuring the
                   # window guard rather than the allowlist. Seeded both ways:
                   # with the allowlist opened and this set, the injected
                   # command really does run and the evidence file appears.
                   "LLOSSLESS_WINDOW": "200000"}
        built = server.build(port=0, work_dir=Path(raw) / "work",
                             environ=environ, commands=store, **kwargs)
        thread = server.background(built)
        try:
            yield built
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


def request(url: str, *, method: str = "GET", payload=None, headers=None,
            timeout: float = PATIENCE):
    """One HTTP call. Returns (status, body-bytes). Never raises on 4xx."""
    body = None
    sent = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        sent.setdefault("Content-Type", "application/json")
    if body is None and method in ("POST", "PUT", "DELETE"):
        # A request that changes something declares the JSON type with or
        # without a body, which is what the page sends and what the server
        # asks for. A caller that means otherwise passes the header itself.
        sent.setdefault("Content-Type", "application/json")
    call = urllib.request.Request(url, data=body, method=method, headers=sent)
    try:
        with urllib.request.urlopen(call, timeout=timeout) as answer:
            return answer.status, answer.read(READ_CAP)
    except urllib.error.HTTPError as refusal:
        return refusal.code, refusal.read(READ_CAP)


def as_json(body: bytes):
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None


def a_submission(**overrides) -> dict:
    body = {"documents": [{"name": LABELS[0], "text": SOURCE_A},
                          {"name": LABELS[1], "text": SOURCE_B}],
            "base": LABELS[0]}
    body.update(overrides)
    return body


def wait_for(predicate, *, timeout: float = PATIENCE) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.02)
    return False


def finished(base: str, job_id: str):
    """Poll one job to a terminal state and hand back its status payload."""
    holder: dict = {}

    def done() -> bool:
        status, body = request(f"{base}/api/v1/runs/{job_id}")
        payload = as_json(body) or {}
        holder.update(payload)
        return status == 200 and payload.get("state") in ("done", "failed")

    wait_for(done)
    return holder


# --------------------------------------------------------------------------
# the file
# --------------------------------------------------------------------------


def test_a_server_with_no_routes_file_offers_no_command_backend() -> None:
    """The empty default, which is the whole posture of this feature.

    A capability that runs a program is switched on deliberately. There is no
    file until an operator writes one, `server.build` is handed no store unless
    its caller asks, and both halves answer the same way: nothing.
    """
    with tempfile.TemporaryDirectory() as raw:
        store = commands.Commands(Path(raw) / "nothing.json")
        check(store.read() == {}, "an absent routes file is not an error")
        check(store.describe() == [], "and it offers nothing to a page")
        check(store.count() == 0, "and counts zero")
    empty = commands.NoCommands()
    check(empty.read() == {} and empty.describe() == [],
          "NoCommands holds nothing")
    try:
        empty.get("anything")
    except commands.UnknownRoute:
        pass
    else:
        failures.append("NoCommands.get must refuse every id, including a "
                        "well-formed one")


def test_a_world_writable_routes_file_is_refused_not_repaired() -> None:
    """Another account writing this file is another account choosing the command.

    The mirror of `credentials.py`'s mode check and the opposite reason. There
    the exposure is that a key has already been *read*; here it is that the
    program this server executes can be *written*, and chmodding it back would
    leave it in service after somebody else had had the opportunity to edit it.
    """
    rows = {"x": {"label": "X", "command": "/bin/true", "window": 1000,
                  "model": "m"}}
    with routes_file(rows, mode=0o644) as (store, path):
        try:
            store.read()
        except commands.CommandsError as refusal:
            check(str(path) in str(refusal), "the refusal must name the file")
            check("write" in str(refusal),
                  f"and must say what the exposure is, got {str(refusal)[:90]!r}")
        else:
            failures.append("a 0644 routes file was read")
        # Must-fire's other half: the same rows at 0600 are read.
        os.chmod(path, 0o600)
        check(set(store.read()) == {"x"}, "and 0600 is readable")


def test_every_shape_the_file_can_be_wrong_is_refused_by_id() -> None:
    """One refusal per way a route can be unusable, each naming the id.

    The list is the check. A route with no window would otherwise be refused by
    `config` forty minutes into a run; a route with no label would leave the
    page with nothing true to render and an invitation to infer one from the
    command.

    **Quarantined rather than raised, and the refusal is the same refusal.**
    The row is not in `read()`, it is not in `describe()`, and `get()` answers
    with its own sentence -- which is every place a refusal has to hold. What
    changed is that it no longer takes the file with it, and the
    companion check below is the one that measures that.
    """
    cases = {
        "no label": {"command": "/bin/true", "window": 10, "model": "m"},
        "blank label": {"label": "  ", "command": "/bin/true", "window": 10,
                        "model": "m"},
        "no command": {"label": "L", "window": 10, "model": "m"},
        "blank command": {"label": "L", "command": " ", "window": 10,
                          "model": "m"},
        "no window": {"label": "L", "command": "/bin/true", "model": "m"},
        "zero window": {"label": "L", "command": "/bin/true", "window": 0,
                        "model": "m"},
        "boolean window": {"label": "L", "command": "/bin/true", "window": True,
                           "model": "m"},
        # The operator's rule, as a shape the file can be wrong in: a command
        # backend cannot be asked which model answered it, so a route that
        # does not say runs on whatever the program defaults to and reports a
        # name nobody chose. Refused on read, where the operator meets it
        # while writing the file rather than forty minutes into a run.
        "no model": {"label": "L", "command": "/bin/true", "window": 10},
        "blank model": {"label": "L", "command": "/bin/true", "window": 10,
                        "model": "   "},
        "unknown profile": {"label": "L", "command": "/bin/true", "window": 10,
                            "model": "m",
                            "profile": "not-a-profile"},
        "unknown field": {"label": "L", "command": "/bin/true", "window": 10,
                          "model": "m",
                          "base_url": "http://elsewhere"},
        "unbalanced quote": {"label": "L", "command": 'sh -c "oops', "window": 10,
                             "model": "m"},
        "not an object": "just a string",
        # The envelope, in every shape it can be wrong. Membership was
        # the only thing checked until then, so the two agreement cases below
        # loaded, ran, and failed inside the merge as a model fault.
        "unknown envelope": {"label": "L", "command": "/bin/true", "window": 10,
                             "model": "m", "envelope": "stream-json"},
        "envelope that is not a string": {
            "label": "L", "command": "/bin/true", "window": 10, "model": "m",
            "envelope": ["result"]},
        "result envelope the command cannot produce": {
            "label": "L", "command": "/bin/true", "window": 10, "model": "m",
            "envelope": "result"},
        "result command read as raw": {
            "label": "L", "command": "/bin/true --output-format json",
            "window": 10, "model": "m", "envelope": "raw"},
    }
    for name, row in cases.items():
        with routes_file({"probe-id": row}) as (store, _path):
            if "probe-id" in store.read():
                failures.append(f"a route with {name} was accepted")
                continue
            reasons = [bad.reason for bad in store.problems()
                       if bad.key == "probe-id"]
            if not reasons:
                failures.append(f"a route with {name} vanished without a word")
                continue
            check("probe-id" in reasons[0],
                  f"the {name} refusal must name the route id")
            check(not store.describe(),
                  f"a route with {name} must not be offered to a page")
            try:
                store.get("probe-id")
            except commands.CommandsError as refusal:
                check("probe-id" in str(refusal),
                      f"the {name} refusal at get() must name the route id")
            else:
                failures.append(f"a route with {name} was resolved by get()")

    # An id that is not an id is refused too, because a route the file holds
    # and no request can name is a route the operator cannot use.
    with routes_file({"../etc/passwd": {"label": "L", "command": "/bin/true",
                                        "window": 10, "model": "m"}}) as (store, _path):
        check(store.read() == {}, "a route id shaped like a path was accepted")
        check([bad.key for bad in store.problems()] == ["../etc/passwd"],
              "and the operator has to be told which key it was")


def test_the_envelope_is_read_off_the_file_and_agrees_with_the_argv() -> None:
    """`Route.envelope`, accepted and refused, which nothing asserted before.

    The field decides which reader `backend` hands the command's stdout to, and
    it had no parsing test at all -- not for its default, not for its accepted
    values, and not for the agreement with the argv that three comments in
    `web/commands.py` said `_row` enforced and `_row` did not.

    The refusals are in the table above, beside every other shape a row can be
    wrong in. This is the other half: the shapes that have to *load*, including
    both spellings of the flag, because an operator who writes
    `--output-format=json` has written a working command and a check that
    refused it would teach them to work around this module.
    """
    accepted = {
        "absent, which is raw": ({"command": "/bin/true"},
                                 commands.ENVELOPE_RAW),
        "raw, said out loud": ({"command": "/bin/true", "envelope": "raw"},
                               commands.ENVELOPE_RAW),
        "result, flag and value": (
            {"command": "/bin/true --output-format json",
             "envelope": "result"}, commands.ENVELOPE_RESULT),
        "result, one token": (
            {"command": "/bin/true --output-format=json",
             "envelope": "result"}, commands.ENVELOPE_RESULT),
        # `stream-json` is a different envelope and is not this one. Declared
        # `raw` it loads, because `raw` is what this build can do with it.
        "a streaming format declared raw": (
            {"command": "/bin/true --output-format stream-json",
             "envelope": "raw"}, commands.ENVELOPE_RAW),
    }
    for name, (overrides, wanted) in accepted.items():
        row = {"label": "L", "window": 10, "model": "m"}
        row.update(overrides)
        with routes_file({"probe-id": row}) as (store, _path):
            loaded = store.read().get("probe-id")
            if loaded is None:
                reasons = [bad.reason for bad in store.problems()]
                failures.append(f"a route with {name} was refused: {reasons}")
                continue
            check(loaded.envelope == wanted,
                  f"a route with {name} loaded with envelope "
                  f"{loaded.envelope!r}, expected {wanted!r}")

    # And the refusal says what to do, in both directions. The operator meets
    # this while writing the file, so the sentence has to carry the flag.
    for row, expected in (
            ({"label": "L", "command": "/bin/true", "window": 10, "model": "m",
              "envelope": "result"}, commands.RESULT_FORMAT_FLAG),
            ({"label": "L", "command": "/bin/true --output-format json",
              "window": 10, "model": "m", "envelope": "raw"},
             commands.RESULT_FORMAT_FLAG)):
        with routes_file({"probe-id": row}) as (store, _path):
            reasons = [bad.reason for bad in store.problems()
                       if bad.key == "probe-id"]
            check(bool(reasons) and expected in reasons[0],
                  f"the envelope disagreement refusal must name {expected!r}; "
                  f"got {reasons}")


def test_the_envelope_agreement_check_fires_on_a_route_that_disagrees() -> None:
    """Seeded: the shipped predicate, given each half of a disagreeing pair.

    Against `commands._carries_result_args` itself rather than a copy of it, so
    a rewrite that stopped seeing the flag is caught here rather than passing a
    re-implementation of what it used to do.
    """
    check(commands._carries_result_args(
              ["claude", "--print", "--output-format", "json"]),
          "the separated spelling of the result flag is not recognised")
    check(commands._carries_result_args(
              ["claude", "--print", "--output-format=json"]),
          "the joined spelling of the result flag is not recognised")
    check(not commands._carries_result_args(["claude", "--print"]),
          "a command with no output format is read as asking for one")
    check(not commands._carries_result_args(
              ["claude", "--print", "--output-format", "stream-json"]),
          "`stream-json` is a different envelope and must not read as this one")
    # The flag last, with nothing after it. An index error here would be a
    # crash on a hand-written file rather than a refusal.
    check(not commands._carries_result_args(["claude", "--output-format"]),
          "a dangling result flag must be read as absent, not crash")


def test_one_unusable_row_does_not_take_the_usable_ones_with_it() -> None:
    """**The operator's symptom, as an assertion.**

    Their file held one route: `discovered: true`, the id `claude`, and no
    model, written by an earlier version of discovery, now refused.
    `read()` raised on it, `describe()` caught that and answered `[]`, and the
    picker lost every command row on the server. There was one row in their
    file so nothing else was there to lose; the failure is the same either way
    and this measures it on a file with good rows in it.

    Seeded: with the quarantine removed -- one bad row raising for the whole
    file, which is what this did before -- `usable` is empty and four checks
    go red at once.
    """
    rows = {
        "good-one": {"label": "First", "command": "/bin/true", "window": 10,
                     "model": "haiku"},
        "stale": {"label": "Stale", "command": "/bin/true", "window": 10,
                  "discovered": True},
        "good-two": {"label": "Second", "command": "/bin/true", "window": 10,
                     "model": "sonnet"},
    }
    with routes_file(rows) as (store, _path):
        usable = store.read()
        check(set(usable) == {"good-one", "good-two"},
              f"the rows that load must load: {sorted(usable)}")
        check([row["id"] for row in store.describe()]
              == ["good-one", "good-two"],
              "and both must reach the picker, with the bad row dropped")
        check(store.count() == 2, f"and be counted: {store.count()}")
        check([bad.key for bad in store.problems()] == ["stale"],
              "and the bad row must be reported, once, by its own id")
        check(store.get("good-two").label == "Second",
              "and a good row must still resolve while a bad one is there")
        try:
            store.get("stale")
        except commands.CommandsError as refusal:
            check("stale" in str(refusal),
                  f"the bad row's own refusal must name it: {refusal}")
        else:
            failures.append("an unusable route was resolved and would have run")


def test_a_rewrite_copies_back_a_row_it_could_not_read() -> None:
    """A toggle must not delete a line out of the operator's own file.

    `_write` replaces the whole file, which is fine for rows it can round trip
    and would be silent data loss for a row it cannot parse. The operator's
    hand-written route with one field missing is exactly that row, and the
    remedy for it is an editor -- which needs the row to still be there.
    """
    rows = {
        "mine": {"label": "Mine", "command": "/bin/true", "window": 10,
                 "profile": "not-a-profile", "model": "m"},
    }
    with discovered_tools(present=("claude",)) as (store, _marker, _paths):
        store._write({}, ())            # make the file exist
        raw = json.loads(store.path.read_text(encoding="utf-8"))
        raw["routes"].update(rows)
        store.path.write_text(json.dumps(raw), encoding="utf-8")
        os.chmod(store.path, 0o600)
        check([bad.key for bad in store.problems()] == ["mine"],
              "the fixture must actually be an unusable row")
        store.enable("claude-haiku")
        after = json.loads(store.path.read_text(encoding="utf-8"))["routes"]
        check("mine" in after, "a row that did not parse was deleted by a toggle")
        check(after["mine"] == rows["mine"],
              f"and it must come back verbatim: {after.get('mine')}")
        check("claude-haiku" in after, "and the toggle must still have worked")


def test_describe_carries_the_label_and_never_the_command() -> None:
    """A command is a local path as often as not, and the page never sees one.

    The probe is not vacuous: the command is in the store for the whole check
    and `read()` returns it, so the search below has something to find and is
    looking in the right place.
    """
    secret = PRIVATE_COMMAND
    rows = {"opus-sub": {"label": SUBSCRIPTION_LABEL, "command": secret,
                         "window": 200000, "model": "opus"}}
    with routes_file(rows) as (store, _path):
        check(store.read()["opus-sub"].command == secret,
              "the store must actually hold the command, or this proves nothing")
        described = json.dumps(store.describe())
        check(secret not in described,
              "describe() served the command string")
        check(PRIVATE_STEM not in described,
              "describe() served part of the command string")
        check(SUBSCRIPTION_LABEL in described, "and it must serve the label")
        check('"opus-sub"' in described, "and the id")
        row = store.describe()[0]
        check(row["comparable"] is False,
              "a subscription route answers at `prompt` and every published "
              "figure here was measured at `json_schema`; the row has to say so")
        check(row["cost"] == "plan" and row["tokens"] == "unmeasured",
              f"cost and tokens must be words and never zero, got {row}")
        check(row["shared"] is True,
              "a command runs as the server process, shared by every account")
        check(row["model"] == "opus",
              "the row must serve the model the route states")
        check(repr(store.read()["opus-sub"]).find(secret) == -1,
              "Route.__repr__ must not print the command")


def test_a_route_that_states_no_model_is_refused_rather_than_run() -> None:
    """The operator's rule: *"relying on the app default is not strategy."*

    A command backend cannot be asked which model answered it. A route that
    does not say runs on whatever the program defaults to -- which may be the
    dearest model on the plan -- and then reports a name nobody chose. This
    reverses an old rule, which allowed the omission and recorded the run under
    the route id: the *name* was honest and the run was not.

    Refused on read rather than at submit, so the operator meets it while
    writing the file instead of forty minutes into a merge. Seeded both ways:
    the stated case is accepted over the same call.
    """
    with routes_file({"a": {"label": "A", "command": "/bin/true", "window": 9,
                            "model": "claude-opus-5"}}) as (store, _p):
        route = store.read()["a"]
        check(route.model_name == "claude-opus-5", "a stated model is used")
        check(store.describe()[0]["model"] == "claude-opus-5",
              "and is served so the row can show it")
        check(route.environ()["LLOSSLESS_MODEL"] == "claude-opus-5",
              "and is what the run resolves against")
    with routes_file({"claude-sub": {"label": "A", "command": "/bin/true",
                                     "window": 9}}) as (store, _p):
        check("claude-sub" not in store.read(),
              "a route that states no model was accepted; it would run on "
              "whatever the program defaults to")
        reasons = [bad.reason for bad in store.problems()]
        check(len(reasons) == 1, f"one row, one refusal: {reasons}")
        refusal = reasons[0] if reasons else ""
        check("claude-sub" in refusal,
              f"the refusal must name the route: {refusal}")
        check("default" in refusal,
              f"and must say why a default is not an answer: {refusal}")
        # **The remedy, not the reasoning.** The first version of this message
        # explained the rule for five sentences and never said what to type,
        # and the operator met it as a wall of text about a file they had not
        # written. The reasoning lives elsewhere; what has to be here is
        # the field and an example of it.
        check("`model`" in refusal,
              f"the refusal must name the field to add: {refusal}")
        check('"model": "' in refusal,
              f"and show it written out: {refusal}")
        check(str(store.path) in refusal,
              f"and name the file it is in: {refusal}")
        check(len(refusal) <= 360,
              f"and stay short enough to read: {len(refusal)} characters")


# --------------------------------------------------------------------------
# the job layer
# --------------------------------------------------------------------------


def test_the_request_allowlist_does_not_carry_the_command_variable() -> None:
    """`LLOSSLESS_COMMAND` on `REQUEST_SETTABLE` would be arbitrary execution.

    Seeded both ways. The must-not-fire half is the real allowlist; the
    must-fire half is the same test against an allowlist that does carry it, so
    a check that could never fail is not standing here reading green.
    """
    check("LLOSSLESS_COMMAND" not in jobs.REQUEST_SETTABLE,
          "a submitted request must never be able to set LLOSSLESS_COMMAND")
    check("LLOSSLESS_COMMAND_LABEL" not in jobs.REQUEST_SETTABLE,
          "nor the label, which would let a request rename somebody else's run")
    seeded = frozenset(jobs.REQUEST_SETTABLE | {"LLOSSLESS_COMMAND"})
    check("LLOSSLESS_COMMAND" in seeded,
          "the probe cannot see the variable it is looking for")
    check(set(api.SETTINGS_FIELDS.values()) <= jobs.REQUEST_SETTABLE,
          "every field the API maps must be on the allowlist")
    check("command" not in api.SUBMIT_FIELDS,
          "the contract must define no field called `command`")
    check("command_route" in api.SUBMIT_FIELDS,
          "and must define the id that replaces it")


def test_a_route_supplies_the_backend_and_skips_the_endpoint_plan() -> None:
    """The id resolves server-side, after the overrides, and instead of an address.

    A command backend addresses nothing, so planning an endpoint for it would
    write per-role addresses into the environment of a run that contacts none
    of them -- and would refuse the request outright when the route's model
    shares a name with a catalogue row whose provider has no endpoint. `Opus 5
    - Subscription` on a server with no Anthropic key is exactly that case.
    """
    rows = {"opus-sub": {"label": SUBSCRIPTION_LABEL,
                         "command": "/usr/bin/claude-wrap -p",
                         "window": 200000, "model": "claude-opus-5"}}
    with routes_file(rows) as (store, _path):
        request_ = jobs.MergeRequest(documents={"a": "x", "b": "y"},
                                     route="opus-sub")
        environ = jobs.resolved_environ(
            request_, {"LLOSSLESS_BASE_URL": UNUSED_ENDPOINT}, routes=store)
        check(environ["LLOSSLESS_COMMAND"] == "/usr/bin/claude-wrap -p",
              "the server supplies the command from its own file")
        check(environ["LLOSSLESS_COMMAND_LABEL"] == SUBSCRIPTION_LABEL,
              "and the label, which is what the banner and the report name")
        check(environ["LLOSSLESS_WINDOW"] == "200000",
              "and the window, which a command backend cannot be asked for")
        check(environ["LLOSSLESS_PROFILE"] == "subscription",
              "and the profile, which pins the one rung it can answer at")
        check(environ["LLOSSLESS_MODEL"] == "claude-opus-5"
              and environ["LLOSSLESS_MERGE_MODEL"] == "claude-opus-5",
              "and both model variables, or half the run runs on the other one")
        planned = [key for key in environ if key.startswith("LLOSSLESS_BASE_URL_")
                   or key.startswith("LLOSSLESS_API_KEY_ENV_")]
        check(not planned,
              f"a command run must not have an endpoint planned for it; got "
              f"{planned}")
        # And the settings that come out of it resolve rather than refusing,
        # which is the regression the skip exists to prevent.
        settings = config.resolve(None, environ=environ)
        check(settings.command == "/usr/bin/claude-wrap -p",
              "the resolved settings must carry the command")
        check(settings.window == 200000, "and the stated window")


def test_an_unknown_route_is_refused_and_never_fallen_back_from() -> None:
    """A submitter who names a route this server lacks has said where it goes."""
    with routes_file({"real": {"label": "R", "command": "/bin/true",
                               "window": 9, "model": "m"}}) as (store, _path):
        request_ = jobs.MergeRequest(documents={"a": "x", "b": "y"},
                                     route="not-here")
        try:
            jobs.resolved_environ(request_, {}, routes=store)
        except commands.UnknownRoute as refusal:
            # `UnknownRoute` and not `JobRefused`, deliberately: `api.submit`
            # gives it its own error code so a page can say "this server has no
            # such route" rather than repeating a generic refusal, and wrapping
            # it in the job layer is what made the two indistinguishable.
            check("not-here" in str(refusal), "the refusal must name the id")
        else:
            failures.append("an unknown route id resolved to something")
    # And a server with no routes at all refuses a well-formed id.
    request_ = jobs.MergeRequest(documents={"a": "x", "b": "y"}, route="real")
    try:
        jobs.resolved_environ(request_, {}, routes=None)
    except commands.UnknownRoute:
        pass
    else:
        failures.append("a server with no routes accepted a route id")


def test_a_request_naming_a_route_and_a_model_is_refused() -> None:
    """The guard that fires when a page and a request disagree.

    A route is one whole row in the picker -- it decides which program answers
    and which model the run is recorded under -- so a request carrying both has
    two answers to "where are these documents going" and the one thing that
    must not happen is picking one of them silently.
    """
    with routes_file({"r": {"label": "R", "command": "/bin/true",
                            "window": 9, "model": "m"}}) as (store, _path):
        for overrides in ({"LLOSSLESS_MODEL": "gpt-5.6-terra"},
                          {"LLOSSLESS_MERGE_MODEL": "claude-opus-5"}):
            request_ = jobs.MergeRequest(documents={"a": "x", "b": "y"},
                                         route="r", overrides=overrides)
            try:
                jobs.resolved_environ(request_, {}, routes=store)
            except jobs.JobRefused as refusal:
                check("command_route" in str(refusal),
                      "the refusal must name the field that collided")
            else:
                failures.append(f"a route beside {sorted(overrides)} was accepted")
        # The same for an endpoint, which a command route contacts none of.
        request_ = jobs.MergeRequest(documents={"a": "x", "b": "y"},
                                     route="r", endpoint="openai")
        try:
            jobs.resolved_environ(request_, {}, routes=store)
        except jobs.JobRefused:
            pass
        else:
            failures.append("a route beside an endpoint was accepted")
        # Must-fire's other half: the route alone resolves.
        alone = jobs.MergeRequest(documents={"a": "x", "b": "y"}, route="r")
        check(jobs.resolved_environ(alone, {}, routes=store)["LLOSSLESS_COMMAND"]
              == "/bin/true",
              "a route on its own must still resolve, or the guard above is "
              "refusing everything")


def test_a_route_carries_the_timeout_a_web_submitter_cannot_pass() -> None:
    """The one run setting a form has no field for.

    The operator met a merge that died at 120s through the page, with no way
    to raise it from there: `--timeout` is a flag and a browser has none. So
    the bound is derived per route from the allowlist entry, the way `window`
    already is -- server-side, one figure per row, no new browser input.

    Optional where `window` is required. An unstated window leaves a run with
    no guard at all; an unstated timeout leaves it with the measured default
    for a command backend.
    """
    with routes_file({"plain": {"label": "P", "command": "/bin/true",
                                "window": 9, "model": "m"},
                      "slow": {"label": "S", "command": "/bin/true",
                               "window": 9, "model": "m", "timeout": 1800}}
                     ) as (store, _path):
        plain = store.get("plain")
        slow = store.get("slow")
        check(plain.timeout is None and plain.seconds == config.COMMAND_TIMEOUT,
              f"an unstated timeout is the command backend's own default, not "
              f"the HTTP one: {plain.timeout} -> {plain.seconds}")
        check(plain.seconds > config.DEFAULT_TIMEOUT,
              "and that default is the larger of the two, or this feature is "
              "the operator's failure again")
        check(slow.timeout == 1800 and slow.seconds == 1800,
              f"a stated figure is used as stated: {slow.seconds}")
        check(plain.environ()["LLOSSLESS_TIMEOUT"] == f"{config.COMMAND_TIMEOUT:g}",
              "every route writes the variable, at the default as much as at "
              "a stated figure")
        check(slow.environ()["LLOSSLESS_TIMEOUT"] == "1800",
              f"{slow.environ()['LLOSSLESS_TIMEOUT']!r}")
        # Served to the page as the resolved number: "not stated" is not
        # something a screen can render beside a route.
        check(plain.described()["timeout"] == config.COMMAND_TIMEOUT,
              f"the page is told the number a call gets: {plain.described()}")
        # Never the file's `None`: a row an operator opens after using the
        # toggle should look like the file the README documents.
        check("timeout" not in plain.as_file_row(),
              f"an unstated timeout is written back as absent: "
              f"{plain.as_file_row()}")
        check(slow.as_file_row()["timeout"] == 1800,
              "and a stated one survives the round trip")

    # Refused rather than dropped, in the four shapes a hand-written row takes.
    # `True` is in the list because `bool` is an `int` in Python and
    # `"timeout": true` is a mistake rather than one second.
    for bad in (0, -1, True, "1800"):
        try:
            with routes_file({"r": {"label": "R", "command": "/bin/true",
                                    "window": 9, "model": "m",
                                    "timeout": bad}}) as (store, _path):
                store.get("r")
        except commands.CommandsError as refusal:
            check("timeout" in str(refusal),
                  f"the refusal must name the field: {refusal}")
        else:
            failures.append(f"a route with timeout={bad!r} was accepted")


def test_a_routes_timeout_beats_the_servers_own_and_reaches_the_client() -> None:
    """The property, measured where a run reads it: `Settings.call_timeout`.

    A server started with `LLOSSLESS_TIMEOUT` set has been configured for the
    endpoint it was started with. A command route contacts no endpoint, so
    inheriting that figure would put an HTTP bound on a subprocess, the same
    shape one setting over, and it is what the operator hit: the page could
    not have raised it either way.

    Driven through `jobs.resolved_environ` and `config.resolve` rather than by
    reading `environ()`, because the question is what the *run* is bounded by
    and there are two layers between the row and the call.
    """
    with routes_file({"plain": {"label": "P", "command": "/bin/true",
                                "window": 9, "model": "m"},
                      "slow": {"label": "S", "command": "/bin/true",
                               "window": 9, "model": "m", "timeout": 1800}}
                     ) as (store, _path):
        server_environ = {"LLOSSLESS_TIMEOUT": "120"}
        for route_id, wanted in (("plain", config.COMMAND_TIMEOUT), ("slow", 1800.0)):
            request_ = jobs.MergeRequest(documents={"a": "x", "b": "y"},
                                         route=route_id)
            environ = jobs.resolved_environ(request_, server_environ, routes=store)
            settings = config.resolve(None, environ=environ)
            check(settings.call_timeout == wanted,
                  f"route {route_id!r} bounds its calls at {wanted}s, not "
                  f"{settings.call_timeout}s")
        # Must-not-fire: with no route, the server's own figure is untouched.
        # Without this the check above would pass with the route ignored and
        # the number coming from somewhere else entirely.
        untouched = config.resolve(None, environ=server_environ)
        check(untouched.call_timeout == 120.0,
              f"a run that names no route keeps the server's setting: "
              f"{untouched.call_timeout}")


def test_the_web_path_cannot_reach_the_thinking_refusal() -> None:
    """A refusal the page offers no way to act on must not be reachable.

    `subscription` has no field that turns thinking off, so `build_body`
    refuses a thinking-off call rather than filing a thinking-on answer under
    a `thinking=False` cassette key. On the command line the answer is
    `--thinking merge --thinking verify --thinking decompose`; the page has no
    such control, so the route states it and `resolved_environ` applies the
    route **after** the request's own overrides -- and `LLOSSLESS_THINKING`
    is not on `REQUEST_SETTABLE` in the first place.

    Both halves are checked here: the roles that come out on, and that a
    server-wide setting turning them off does not survive a route.
    """
    with routes_file({"r": {"label": "R", "command": "/bin/true",
                            "window": 9, "model": "m"}}) as (store, _path):
        request_ = jobs.MergeRequest(documents={"a": "x", "b": "y"}, route="r")
        # The operator's own environment, with thinking explicitly off: the
        # shape that would otherwise refuse every call this route makes.
        environ = jobs.resolved_environ(request_, {"LLOSSLESS_THINKING": ""},
                                        routes=store)
        settings = config.resolve(None, environ=environ)
        missing = [role for role in config.ROLES if not settings.thinks(role)]
        check(not missing,
              f"a subscription route must run with thinking on for every role "
              f"or its first call is a refusal the page cannot act on; off "
              f"for {missing}")
        check("LLOSSLESS_THINKING" not in jobs.REQUEST_SETTABLE,
              "and a submitter still may not set it: it is the operator's "
              "route that turns it on, not a form")
    # Must-not-fire: nothing here turned thinking on for the HTTP path, where
    # the profile can carry the field and the published figures are off.
    plain = config.resolve(None, environ={"LLOSSLESS_THINKING": ""})
    check(not any(plain.thinks(role) for role in config.ROLES),
          "an HTTP run's thinking setting is untouched by any of this")


# --------------------------------------------------------------------------
# what a command run records about itself
# --------------------------------------------------------------------------


def command_settings(**overrides):
    environ = {"LLOSSLESS_BASE_URL": UNUSED_ENDPOINT,
               "LLOSSLESS_COMMAND": PRIVATE_COMMAND,
               "LLOSSLESS_COMMAND_LABEL": SUBSCRIPTION_LABEL,
               "LLOSSLESS_WINDOW": "200000",
               "LLOSSLESS_PROFILE": "subscription",
               "LLOSSLESS_MODEL": "opus-sub",
               "LLOSSLESS_MERGE_MODEL": "opus-sub",
               "LLOSSLESS_STRUCTURED": "prompt"}
    environ.update(overrides)
    return config.resolve(None, environ=environ)


def test_the_banner_names_the_route_and_never_an_address_it_did_not_use() -> None:
    """The line an operator reads while the money is being committed.

    `banner_endpoint` is derived from `base_url`, so before this a run that
    contacted nothing announced whatever address the server happened to be
    started with. That is the same fault moved to the one line that is in front of
    the reader *during* the run rather than after it.
    """
    settings = command_settings()
    check(settings.banner_endpoint == SUBSCRIPTION_LABEL,
          f"the banner must name the route, got {settings.banner_endpoint!r}")
    check(UNUSED_HOST not in settings.banner_endpoint,
          "and must not name an address the run never contacted")
    check(UNUSED_HOST not in settings.endpoint_name,
          "nor may an error message about the program name one")
    check(PRIVATE_STEM not in settings.banner_endpoint,
          "and the label is the operator's words, never the command")
    unlabelled = command_settings(LLOSSLESS_COMMAND_LABEL="")
    check(unlabelled.banner_endpoint == "command",
          f"with no label it says which mechanism answered, got "
          f"{unlabelled.banner_endpoint!r}")
    # Must-fire's other half: an HTTP run still names its address.
    http_only = config.resolve(None, environ={
        "LLOSSLESS_BASE_URL": UNUSED_ENDPOINT, "LLOSSLESS_MODEL": "m"})
    check(UNUSED_HOST in http_only.banner_endpoint,
          "an HTTP run must still name its endpoint, or this check is asserting "
          "that the banner says nothing")


def test_provenance_names_the_route_and_says_what_it_cannot_know() -> None:
    """`content_left_this_machine` is true, and the note says why it is true.

    The flag is already true for any command backend: the tool cannot
    establish that a document stayed here, and the honest answer to a question
    it cannot answer is the one that makes a reader check. What was still wrong
    is the sentence beside it: it named `LLOSSLESS_BASE_URL` as the
    destination, which for a command run is an address nothing contacted.
    """
    import dataclasses

    from llossless.client import Client

    with tempfile.TemporaryDirectory() as raw:
        settings = dataclasses.replace(command_settings(),
                                       cache_dir=Path(raw), use_cache=False)
        block = provenance.Provenance(
            settings=settings, client=Client(settings),
            roles=("merge", "verify", "decompose"), duration_seconds=1.0)
        data = block.as_dict()
        endpoint = data["endpoint"]
        check(endpoint["location"] == "command",
              f"a command run's location is `command`, got {endpoint}")
        check(endpoint["content_left_this_machine"] is True,
              "and content_left_this_machine is true, because nothing here can "
              "establish that it did not")
        check(endpoint.get("route") == SUBSCRIPTION_LABEL,
              f"and the route is named, got {endpoint.get('route')!r}")
        check("by_role" not in endpoint,
              "a command run addresses no endpoints, so it lists none")
        check(PRIVATE_STEM not in json.dumps(data),
              "and the command never reaches the block")

        notes = " ".join(block.notes())
        check("handed to a program" in notes,
              f"the note must say what actually happened, got {notes[:160]!r}")
        check("LLOSSLESS_BASE_URL" not in notes,
              "and must not send a reader to look at an address this run never "
              "contacted")
        check(SUBSCRIPTION_LABEL in notes, "and must name the route")

        rows = dict(block.rows())
        check(SUBSCRIPTION_LABEL in rows["Endpoint"],
              f"the report's own endpoint row must name the route, got "
              f"{rows['Endpoint']!r}")


# --------------------------------------------------------------------------
# over HTTP: the two seeded attacks, and the control that must fire
# --------------------------------------------------------------------------

# Every shape a client might try to hand this server a command with, posted
# straight at the API with no page involved. Each must be refused, and none may
# start anything.
#
# The list is deliberately wider than what the contract defines: `command` and
# `answer_with` are the two flag names, `LLOSSLESS_COMMAND` is the variable,
# and `overrides` is the shape somebody would reach for after reading
# `jobs.py`. An unknown field is refused rather than ignored, which is what
# makes all four one refusal.
def injections(evidence: Path) -> tuple[dict, ...]:
    """The bodies, each carrying a command that would leave `evidence` behind.

    The command is `touch` rather than something inert, deliberately. "Nothing
    was executed" has to be a *measurement of the injected command*, not of the
    allowlisted one: an earlier draft of this checked only the route's own
    marker, which would have stayed absent while `/bin/sh` ran perfectly well
    under a seeded hole. Seeded with the door opened -- the field added to the
    contract, the variable added to the allowlist and both shipped assertions
    removed -- this file appears.
    """
    touch = f"/bin/sh -c 'touch {evidence}'"
    return (
        {"command": touch},
        {"answer_with": touch},
        {"LLOSSLESS_COMMAND": touch},
        {"overrides": {"LLOSSLESS_COMMAND": touch}},
        {"command_route": {"command": touch}},
    )


def test_posting_a_command_straight_at_the_api_is_refused_and_runs_nothing() -> None:
    """Seeded attack one: bypass the page and hand the server a command.

    This is the failure the whole allowlist exists to prevent, so it is driven
    over a real socket rather than asserted about `parse_submit`: a contract
    exercised by calling its own implementation is a contract whose routing and
    status codes have never been checked.
    """
    with fake_route() as (store, marker, command):
        evidence = marker.parent / "injected-command-ran"
        with live_server(store) as built:
            base = built.url
            for body in injections(evidence):
                status, raw = request(f"{base}/api/v1/runs", method="POST",
                                      payload=a_submission(**body))
                payload = as_json(raw) or {}
                check(status == 400,
                      f"{sorted(body)} was answered {status}, not refused")
                code = (payload.get("error") or {}).get("code", "")
                check(code in ("unknown_field", "bad_command_route"),
                      f"{sorted(body)} was refused as {code!r}, which is not a "
                      f"refusal about the field it named")
                check("id" not in payload,
                      f"{sorted(body)} was accepted as a job")
                # A job that was accepted would run on a worker thread, so the
                # evidence file appears after the response rather than with it.
                wait_for(evidence.exists, timeout=2.0)
        check(not evidence.exists(),
              f"an injected command was executed; {evidence} exists")
        check(not marker.exists(),
              f"the allowlisted command was started by an injection probe; "
              f"{marker} exists")


def test_posting_an_unknown_route_id_is_refused_and_runs_nothing() -> None:
    """Seeded attack two: a well-formed id this server does not have.

    Refused naming the field, never answered some other way. A fallback here
    would spend money on a route the submitter did not ask for and nobody would
    find out until the bill.
    """
    with fake_route() as (store, marker, _command):
        with live_server(store) as built:
            status, raw = request(f"{built.url}/api/v1/runs", method="POST",
                                  payload=a_submission(command_route="no-such-route"))
            payload = as_json(raw) or {}
            check(status == 400, f"an unknown id was answered {status}")
            check((payload.get("error") or {}).get("code") == "bad_command_route",
                  f"refused as {payload.get('error')}, which does not name the "
                  f"field")
            message = (payload.get("error") or {}).get("message", "")
            check("no-such-route" in message,
                  f"the refusal must name the id, got {message[:120]!r}")
            check("id" not in payload, "an unknown id was accepted as a job")
            # An id that is not even an id, on the same route.
            status, raw = request(f"{built.url}/api/v1/runs", method="POST",
                                  payload=a_submission(command_route="../../etc/passwd"))
            check(status == 400, "a path-shaped id was accepted")
        check(not marker.exists(),
              "the fake command was started by an unknown-id probe")


def test_the_control_run_does_start_the_command() -> None:
    """The must-fire half of both probes above, and the feature working.

    Without this, "the marker file does not exist" is a statement about a
    program that could never have started, and would stay green with the whole
    backend deleted.
    """
    with fake_route() as (store, marker, command):
        with live_server(store) as built:
            base = built.url
            status, raw = request(f"{base}/api/v1/runs", method="POST",
                                  payload=a_submission(command_route="opus-sub"))
            accepted = as_json(raw) or {}
            check(status == 202, f"a valid route was answered {status}: {raw[:200]!r}")
            job_id = accepted.get("id", "")
            check(bool(job_id), "a valid route must produce a job")
            if not job_id:
                return
            status_payload = finished(base, job_id)
            check(status_payload.get("state") == "done",
                  f"the run did not finish: {status_payload.get('state')!r} "
                  f"{str(status_payload.get('error'))[:200]!r}")
            check(marker.exists(),
                  "the command was never started, so the two probes above prove "
                  "nothing")
            starts = marker.read_text(encoding="utf-8").count("started")
            check(starts >= 3,
                  f"a merge is at least three model calls and the command ran "
                  f"{starts} time(s)")

            report = (status_payload.get("report") or {})
            endpoint = (report.get("provenance") or {}).get("endpoint") or {}
            check(endpoint.get("location") == "command",
                  f"the served report must say a command answered, got {endpoint}")
            check(endpoint.get("route") == SUBSCRIPTION_LABEL,
                  f"and must name the route, got {endpoint.get('route')!r}")
            check(endpoint.get("content_left_this_machine") is True,
                  "and must not claim the content stayed here")

            # The command string reaches no served body. The store holds it
            # throughout, so the search has something to find.
            check(command in store.read()["opus-sub"].command,
                  "the store must hold the command, or the searches below are "
                  "looking for a string nothing has")
            program = shlex.split(command)[1]
            # Both report spellings, and the status is asserted before the
            # search. `report` used to 404, and a "the command is not in this
            # body" check against a 404 body is a check that passes over
            # nothing -- which is what it was doing until the browser harness
            # surfaced the wrong path. It is now the page that shows the
            # report, which is a second body a reader sees and a second body
            # the command must not reach.
            for name, url in (("config", f"{base}/api/v1/config"),
                              ("run", f"{base}/api/v1/runs/{job_id}"),
                              ("report", f"{base}/api/v1/runs/{job_id}/report.html"),
                              ("report page", f"{base}/api/v1/runs/{job_id}/report"),
                              ("merged", f"{base}/api/v1/runs/{job_id}/merged")):
                status, body = request(url)
                check(status == 200,
                      f"the {name} route answered {status}, so the search below "
                      f"is looking at an error body")
                text = body.decode("utf-8", "replace")
                check(command not in text,
                      f"the {name} response carries the whole command string")
                check(program not in text,
                      f"the {name} response carries the command's script path")
            # And the downloaded report names the route, which is where a
            # reader goes a week later.
            _status, page = request(f"{base}/api/v1/runs/{job_id}/report.html")
            check(SUBSCRIPTION_LABEL in page.decode("utf-8", "replace"),
                  "the downloadable report does not name the route that ran")

            # And the banner the operator watched named the route.
            _status, body = request(f"{base}/api/v1/runs/{job_id}/events")
            banner = [line for line in body.decode("utf-8", "replace").splitlines()
                      if '"kind": "banner"' in line or '"banner"' in line]
            check(any(SUBSCRIPTION_LABEL in line for line in banner),
                  "the banner event must name the route the run took")
            check(not any(UNUSED_HOST in line for line in banner),
                  "and must not name an address the run never contacted")


def test_config_serves_labels_and_ids_and_never_a_command() -> None:
    """What a browser is told about the operator's routes.

    And the default beside it: a server built without a store serves an empty
    list, so the page offers no command backend at all.
    """
    with fake_route() as (store, _marker, command):
        with live_server(store) as built:
            _status, body = request(f"{built.url}/api/v1/config")
            payload = as_json(body) or {}
            block = payload.get("commands") or {}
            rows = block.get("routes") or []
            check(len(rows) == 1, f"one route was configured, served {len(rows)}")
            if rows:
                check(rows[0]["id"] == "opus-sub" and rows[0]["label"] == SUBSCRIPTION_LABEL,
                      f"the row must carry the id and the label, got {rows[0]}")
                check("command" not in rows[0],
                      "the row must not carry a command field at all")
            check(block.get("per_user") is False,
                  "a command runs as the server process, and the page has to be "
                  "told that rather than assume it")
            check(command not in body.decode("utf-8", "replace"),
                  "/config carries the command string")
    # The default: no store asked for, no routes offered.
    with tempfile.TemporaryDirectory() as raw:
        built = server.build(port=0, work_dir=Path(raw) / "work",
                             environ={"LLOSSLESS_BASE_URL": UNUSED_ENDPOINT})
        try:
            rows = (built.api.config().get("commands") or {}).get("routes")
            check(rows == [],
                  f"a server built with no command store must offer none, got "
                  f"{rows}")
        finally:
            built.server_close()
            built.store.close()


# --------------------------------------------------------------------------
# discovery: the second way the allowlist gets filled
# --------------------------------------------------------------------------

# The program the discovery probes run. Same body as `FAKE_COMMAND`, with the
# marker and the replies baked in rather than taken as arguments, and **with
# its own argv written to the marker**.
#
# That last part is the point of this fixture and not a convenience. A route
# that declares Haiku in its label and runs the CLI's default is exactly the
# defect this milestone exists to remove, and it is invisible from the outside:
# the run finishes, the report names the model the route declared, and nothing
# anywhere compared that name with what the program was actually told. So the
# fake echoes the arguments it was handed and the checks read them back, which
# makes "this route really did select that model" a measurement.
PROBE_TOOL = ('#!{python}\n'
              'import json, sys\n'
              '\n'
              'marker, replies_path = {marker!r}, {replies!r}\n'
              'with open(marker, "a", encoding="utf-8") as handle:\n'
              '    handle.write("argv " + " ".join(sys.argv[1:]) + "\\n")\n'
              # Everything from the first `open(marker...)` onward, unchanged.
              # Taking the body rather than copying it is what keeps this and
              # the argument-taking fake in step when the prompts move.
              + "\n".join(FAKE_COMMAND.split("\n")[3:]))


def argv_lines(marker: Path) -> list[str]:
    """Every argv the fake tool was started with, in order."""
    if not marker.exists():
        return []
    return [line[len("argv "):]
            for line in marker.read_text(encoding="utf-8").splitlines()
            if line.startswith("argv ")]

# A program name that is **not** in `commands.KNOWN_TOOLS`. Every probe below
# that must be refused names this, and it is a real program on the stubbed
# `PATH` -- so a refusal here is the table refusing an id, not `shutil.which`
# failing to find anything. A guard that only ever sees a name nothing resolves
# is a guard nobody has driven.
OUTSIDE_TABLE = "cc-not-in-the-table"


def probe_program(directory: Path, name: str, marker: Path,
                  replies: Path) -> Path:
    """An executable that appends to `marker` and then answers like the fake CLI."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(PROBE_TOOL.format(python=sys.executable, marker=str(marker),
                                      replies=str(replies)), encoding="utf-8")
    os.chmod(path, 0o700)
    return path


def expected_command(paths: dict, tool, model) -> str:
    """The command `enable` must write for this route, built here independently.

    Not read back off the store: a check that asks the store what it wrote and
    then asserts it wrote that passes over any command at all. This composes
    the same three parts from the table and the stubbed `PATH` and compares.
    """
    return shlex.join((paths[tool.program], *tool.base_args, *tool.result_args,
                       *model.select))


@contextlib.contextmanager
def discovered_tools(*, present=(), holed=False):
    """A store whose `PATH` holds exactly `present`. Yields the parts.

    Yields `(store, marker, paths)`. `paths` maps a program name to the
    absolute path `shutil.which` would answer with, which is what the leak
    assertions search served bodies for.

    `which` is injected rather than `PATH` edited, because the alternative is a
    check that installs and deletes programs -- and because the "nothing was
    found" machine has to be describable without unsetting the `PATH` of the
    interpreter running the suite.
    """
    with tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        replies = home / "replies.json"
        replies.write_text(json.dumps(resolved_replies()), encoding="utf-8")
        marker = home / "started.log"
        paths = {name: str(probe_program(home / "bin", name, marker, replies))
                 for name in present}
        maker = HoledCommands if holed else commands.Commands
        store = maker(home / "config" / "commands.json",
                      which=lambda name: paths.get(name))
        yield store, marker, paths


class HoledCommands(commands.Commands):
    """The hole, opened on purpose, and the only thing it removes is one call.

    `enable` here resolves the caller's id on `PATH` instead of looking it up
    in `KNOWN_TOOLS` -- which is the obvious wrong implementation of this
    feature, not a contrived one. Every other guard stays: the id still has to
    resolve to a real program, the route still goes through the allowlist, the
    submit path still refuses anything it has no row for.

    It exists so the probes below are a **measurement**. "Nothing ran" is a
    statement about a backend that could never have started until the same
    probe, run against a server with this in it, does start one.
    """

    def enable(self, route_id):
        invented = commands.KnownTool(
            id=str(route_id), label=str(route_id), program=str(route_id),
            window=200000, base_args=(), models=())
        where = self.locate(invented)
        if not where:
            raise commands.CommandsError("nothing by that name on PATH")
        routes = self.read()
        routes[str(route_id)] = commands.Route(
            id=str(route_id), label=str(route_id), command=where, window=200000,
            model=str(route_id), discovered=True)
        self._write(routes)
        return commands.ToolModel(id=str(route_id), label=str(route_id),
                                  model=str(route_id), select=(), rank=0,
                                  evidence="seeded")


def test_the_table_is_closed_and_every_row_is_reachable() -> None:
    """What `KNOWN_TOOLS` may hold, checked rather than described.

    A row whose id no request could name would be a route this server found,
    offered on the page, and refused on submit. A row with no model would be
    a route that runs on whatever the program defaults to, which is the
    arrangement the operator refused in as many words.
    """
    check(bool(commands.KNOWN_TOOLS), "the table must not be empty")
    for tool in commands.KNOWN_TOOLS:
        check("/" not in tool.program and "\\" not in tool.program,
              f"{tool.program!r} is a path; the table names programs and lets "
              f"PATH decide where they are")
        check(tool.window > 0, f"{tool.id!r} has no stated window")
        check(bool(tool.models), f"{tool.id!r} offers no model to select")
        check(bool(tool.base_args),
              f"{tool.id!r} passes no arguments, so it would open a session "
              f"rather than answer a prompt on stdin")

    seen = set()
    for tool, model in commands.expansions():
        check(bool(commands.ROUTE_ID.match(model.id)),
              f"{model.id!r} is not an id a request could name")
        check(model.id not in seen, f"{model.id!r} is in the table twice")
        seen.add(model.id)
        check(bool(model.model), f"{model.id!r} pins no model")
        check(bool(model.select),
              f"{model.id!r} names a model and asks the program for nothing, "
              f"so it would run on the program's default")
        check(bool(model.evidence),
              f"{model.id!r} does not say where its facts were checked; a "
              f"wrong model id here produces a wrong bill")
        check(model.label and model.label != model.model,
              f"{model.id!r} has no label of its own")
    # Cheapest first, which is what stops the page preselecting the dearest.
    ranks = [model.rank for _tool, model in commands.expansions()]
    check(ranks == sorted(ranks),
          f"the expansions are not in cheapest-first order: {ranks}")


def test_discovery_reports_availability_and_never_the_resolved_path() -> None:
    """Four facts per row, and the path is not one of them.

    The resolved path is an absolute path under whichever account the server
    runs as. The release scanner refuses that shape anywhere in
    the published set and it already caught this feature once, so the
    reduction to a boolean happens here rather than at whichever caller
    remembers.
    """
    tool, model = commands.expansions()[0]
    with discovered_tools(present=[tool.program]) as (store, _marker, paths):
        rows = store.discovered()
        check(len(rows) == len(commands.expansions()),
              f"every route the table can produce must be reported, got "
              f"{len(rows)}")
        row = next(entry for entry in rows if entry["id"] == model.id)
        check(row["available"] is True, "the program is on PATH and was not found")
        check(row["enabled"] is False, "nothing is enabled until it is switched on")
        check(row["model"] == model.model,
              f"the row must say which model it pins, got {row}")
        served = json.dumps(rows)
        check(paths[tool.program] not in served,
              "the resolved path reached the payload")
        check("/bin" not in served,
              f"a filesystem path reached the payload: {served}")
        # And the store does hold it, or the search above is looking for a
        # string nothing has.
        store.enable(model.id)
        written = store.read()[model.id]
        check(written.command.startswith(paths[tool.program]),
              "the store must hold the resolved path")
        check(paths[tool.program] not in json.dumps(store.discovered()),
              "an enabled row leaks the path the disabled row did not")
        check(paths[tool.program] not in json.dumps(store.describe()),
              "`describe` leaks the path")
        check(paths[tool.program] not in repr(written),
              "the route's own `repr` carries the path into every log line")
        # The argv that pins the model is the other half of what gets
        # executed, and the page has no use for it. The *model* is served and
        # must be -- that is the operator's whole complaint -- so what is
        # searched for is the flag and the joined argument list, not the
        # model string the flag carries.
        payload = json.dumps(store.discovered())
        flags = [part for part in model.select if part.startswith("-")]
        check(bool(flags), "the probe has no flag to look for")
        for flag in flags:
            check(flag not in payload,
                  f"the discovered payload carries the argv flag {flag!r}")
        check(" ".join(model.select) not in payload,
              "the discovered payload carries the whole argument list")


def test_nothing_found_is_a_state_and_not_an_empty_panel() -> None:
    """The machine where no tool is installed. Rows, and every one says so."""
    with discovered_tools(present=[]) as (store, _marker, _paths):
        rows = store.discovered()
        check(len(rows) == len(commands.expansions()),
              "a machine with nothing installed still reports the table")
        check(all(row["available"] is False for row in rows),
              f"nothing is installed and something was found: {rows}")
        check(store.describe() == [], "and nothing is offered in the picker")
        try:
            store.enable(rows[0]["id"])
        except commands.CommandsError as refusal:
            check("PATH" in str(refusal),
                  f"the refusal must say why: {refusal}")
        else:
            failures.append("a tool that is not installed was switched on")


def test_a_tool_off_the_path_is_found_where_a_per_user_install_puts_it() -> None:
    """**The half of the operator's report the page got wrong on its own.**

    `shutil.which` reads the `PATH` of *this process*. A server started from a
    unit file, a container or a desktop sandbox has whatever `PATH` that gave
    it, and a per-user CLI installs itself into `~/.local/bin` -- so the page
    said "not found" about a program the operator runs every day. The remedy
    is `EXTRA_BIN_DIRS`, checked after `PATH` and never instead of it.

    Seeded: `search=()` is the lookup as it was, PATH and nothing else, and it
    is asserted here rather than described -- the same fixture, the same
    program, the same call, and the row goes unavailable.
    """
    tool, model = commands.expansions()[0]
    with tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        replies = home / "replies.json"
        replies.write_text(json.dumps(resolved_replies()), encoding="utf-8")
        marker = home / "started.log"
        elsewhere = home / "not-on-path"
        program = probe_program(elsewhere, tool.program, marker, replies)

        # `which` answers nothing, which is the operator's server exactly:
        # the program is real, it is executable, and it is not on the `PATH`
        # this process was started with.
        widened = commands.Commands(home / "config" / "commands.json",
                                    which=lambda name: None,
                                    search=(elsewhere,))
        rows = {row["id"]: row for row in widened.discovered()}
        check(rows[model.id]["available"] is True,
              "a tool in a per-user install directory must be found")
        check(widened.locate(tool) == str(program),
              f"and resolved to the program itself: {widened.locate(tool)!r}")
        check(str(program) not in json.dumps(widened.discovered()),
              "and the resolved path must still reach no payload")

        # The seed: the lookup as it was. Nothing else about the fixture moves.
        narrow = commands.Commands(home / "config" / "commands.json",
                                   which=lambda name: None, search=())
        check(narrow.discovered()[0]["available"] is False,
              "PATH alone must not find it, or this check proves nothing")

        # And `PATH` still wins where it answers, so the table is a fallback
        # rather than an override: a machine with an opinion keeps it.
        other = probe_program(home / "on-path", tool.program, marker, replies)
        both = commands.Commands(home / "config" / "commands.json",
                                 which=lambda name: str(other),
                                 search=(elsewhere,))
        check(both.locate(tool) == str(other),
              f"PATH must answer first: {both.locate(tool)!r}")

        # A directory in the table that holds a *directory* by that name, or
        # a file nothing may execute, is not a tool.
        (home / "traps" / tool.program).mkdir(parents=True)
        unreadable = home / "plain"
        unreadable.mkdir()
        (unreadable / tool.program).write_text("#!/bin/sh\n", encoding="utf-8")
        os.chmod(unreadable / tool.program, 0o600)
        for directory, why in ((home / "traps", "a directory"),
                               (unreadable, "a file with no execute bit")):
            store = commands.Commands(home / "config" / "commands.json",
                                      which=lambda name: None,
                                      search=(directory,))
            check(store.locate(tool) == "",
                  f"{why} named {tool.program!r} was offered as a program")


def test_the_search_table_names_directories_and_never_a_program() -> None:
    """What `EXTRA_BIN_DIRS` may hold, checked rather than described.

    The security property is that the table decides which *names* may run and
    the browser only ever sends an id. Widening where a known name is looked
    for keeps that property exactly as long as the entries are directories: an
    entry naming a program would be this file asserting what runs, which is
    the one thing `KNOWN_TOOLS.program` exists to refuse.
    """
    check(bool(commands.EXTRA_BIN_DIRS), "the table must not be empty")
    for entry in commands.EXTRA_BIN_DIRS:
        check(entry.startswith("/") or entry.startswith("~/"),
              f"{entry!r} is relative; a relative directory is resolved "
              f"against whatever this process's cwd happens to be")
        check(not entry.endswith("/"), f"{entry!r} has a trailing separator")
        names = {tool.program for tool in commands.KNOWN_TOOLS}
        check(Path(entry).name not in names,
              f"{entry!r} names a program; the table names directories")
    # `~` is dropped rather than guessed at where there is no home, because
    # expanding it against a daemon account's fallback is how a lookup ends
    # up somewhere nobody installed anything.
    check(all("~" not in str(path)
              for path in commands.search_dirs({"HOME": "/home/probe"})),
          "every `~` entry must be expanded")
    check(all(not str(path).startswith("~")
              for path in commands.search_dirs({})),
          "and a missing HOME must drop them rather than leave them literal")


def test_the_row_the_old_page_wrote_is_retired_and_not_left_to_scold() -> None:
    """**The operator's file, migrated.** An update turned their row into a refusal.

    The row is `discovered: true`, the id `claude`, a command and no model,
    the shape older discovery code wrote, and the shape current code refuses.
    It is this page's own row, so this page retires it; asking them to
    hand-edit a file they never hand-wrote is not an answer.

    Dropped rather than rewritten into four. The old row ran whatever the CLI
    defaults to and there is no honest mapping from that to one of four
    aliases: picking one is the guess this code exists to refuse.

    Seeded: with `migrate()` not called the orphan is still there, still
    unusable, and still the only row in the file.
    """
    stale = {"label": "Claude Code (subscription)",
             "command": "/usr/bin/claude", "window": 200000,
             "discovered": True}
    with routes_file({"claude": dict(stale)}) as (store, path):
        # The seed: this is the state before the call, and it is the state the
        # operator reported.
        check(store.read() == {}, "the fixture must reproduce the empty list")
        check([bad.key for bad in store.problems()] == ["claude"],
              "and the orphan must be the reason")
        check(store.retired == (), "nothing is retired until migrate() runs")

        check(store.migrate() == ("claude",),
              "the row the old page wrote must be retired by name")
        check(store.retired == ("claude",),
              "and said once, so the page can explain where a route went")
        after = json.loads(path.read_text(encoding="utf-8"))
        check(after["routes"] == {}, f"and be gone from the file: {after}")
        check(store.problems() == (),
              "and stop being a complaint the operator cannot act on")
        check(store.migrate() == (),
              "and a second call must find nothing to do")

    # A hand-written row of the same shape is **not** touched. `discovered` is
    # the whole of the guard and this is the case it guards.
    hand = {"label": "Mine", "command": "/usr/bin/claude", "window": 200000}
    with routes_file({"claude": dict(hand)}) as (store, path):
        check(store.migrate() == (),
              "a row the operator wrote must not be retired")
        after = json.loads(path.read_text(encoding="utf-8"))
        check(after["routes"] == {"claude": hand},
              f"and must be left exactly as it is: {after}")
        check(len(store.problems()) == 1,
              "and keep its own refusal, which is the operator's to act on")

    # Nor is a discovered row that states a model, whatever else is wrong with
    # it: that is a row a later build wrote, and this migration is about one
    # shape only.
    later = {"label": "L", "command": "/usr/bin/claude", "window": 200000,
             "model": "haiku", "discovered": True, "base_url": "nope"}
    with routes_file({"claude": dict(later)}) as (store, path):
        check(store.migrate() == (),
              "a discovered row that states a model is not this shape")
        after = json.loads(path.read_text(encoding="utf-8"))
        check(after["routes"] == {"claude": later},
              f"and must be left alone: {after}")


def test_retiring_the_orphan_puts_the_feature_back_within_one_click() -> None:
    """The whole chain, from the operator's file to a route in the picker.

    Each link was broken on its own and the report was one complaint: the
    picker had no command rows, the toggle answered with a wall of text, and
    the row said the tool was not there. This walks it once.
    """
    stale = {"label": "Claude Code (subscription)",
             "command": "/usr/bin/claude", "window": 200000,
             "discovered": True}
    tool, model = commands.expansions()[0]
    with discovered_tools(present=[tool.program]) as (store, _marker, paths):
        store.path.parent.mkdir(parents=True, exist_ok=True)
        store.path.write_text(
            json.dumps({"version": 1, "routes": {"claude": stale}}),
            encoding="utf-8")
        os.chmod(store.path, 0o600)

        check(store.describe() == [],
              "the fixture must start in the state that was reported")
        rows = {row["id"]: row for row in store.discovered()}
        check(rows[model.id]["available"] is True,
              "the tool is installed on this machine, or nothing below holds")

        store.migrate()
        rows = {row["id"]: row for row in store.discovered()}
        check(all(not row["owned"] for row in rows.values()),
              f"no row may be owned once the orphan is gone: {rows}")
        check(all(not row["problem"] for row in rows.values()),
              "and none may carry a problem")
        store.enable(model.id)
        offered = store.describe()
        check([row["id"] for row in offered] == [model.id],
              f"one click must put one route in the picker: {offered}")
        check(offered[0]["model"] == model.model,
              "and it must name the model it selects")
        check(store.get(model.id).command == expected_command(paths, tool, model),
              "and run the program this server found, with the argv the "
              "table wrote")


def test_a_broken_hand_written_row_is_said_on_its_row_and_never_replaced() -> None:
    """A row with a discovered id that the operator wrote, and cannot be read.

    Two things have to hold at once. The toggle must be inert, because the
    server would refuse it -- a control whose only answer is a 409 explains a
    refusal after the fact. And the reason has to be on that row, because the
    message names one route and the page used to render it across the panel.
    """
    tool, model = commands.expansions()[0]
    broken = {"label": "Mine", "command": PRIVATE_COMMAND, "window": 200000}
    with discovered_tools(present=[tool.program]) as (store, _marker, _paths):
        store.path.parent.mkdir(parents=True, exist_ok=True)
        store.path.write_text(
            json.dumps({"version": 1, "routes": {model.id: broken}}),
            encoding="utf-8")
        os.chmod(store.path, 0o600)
        rows = {row["id"]: row for row in store.discovered()}
        row = rows[model.id]
        check(row["owned"] is True,
              f"a broken hand-written row must own its id: {row}")
        check(model.id in row["problem"],
              f"and the row must say what is wrong with it: {row['problem']}")
        check(PRIVATE_COMMAND not in json.dumps(store.discovered()),
              "and the command in it must not reach the payload")
        try:
            store.enable(model.id)
        except commands.CommandsError as refusal:
            check("hand-written" in str(refusal),
                  f"the refusal must say whose row it is: {refusal}")
        else:
            failures.append("a hand-written row was overwritten by the toggle")
        after = json.loads(store.path.read_text(encoding="utf-8"))["routes"]
        check(after == {model.id: broken},
              f"and the file must be untouched: {after}")


def test_discovery_writes_the_one_allowlist_and_never_touches_a_hand_row() -> None:
    """One store, two ways to fill it, and the page owns only its own rows."""
    tool, model = commands.expansions()[0]
    with discovered_tools(present=[tool.program]) as (store, _marker, paths):
        store.path.parent.mkdir(parents=True, exist_ok=True)
        store.path.write_text(json.dumps({"version": 1, "routes": {
            "mine": {"label": "Mine", "command": PRIVATE_COMMAND,
                     "window": 1000, "model": "mine"}}}), encoding="utf-8")
        os.chmod(store.path, 0o600)
        store.enable(model.id)
        routes = store.read()
        check(set(routes) == {"mine", model.id},
              f"the operator's row must survive, got {sorted(routes)}")
        check(routes["mine"].command == PRIVATE_COMMAND,
              "the operator's command was rewritten")
        check(routes["mine"].discovered is False and routes[model.id].discovered,
              "the two kinds of row must be told apart in the file")
        check(routes[model.id].command == expected_command(paths, tool, model),
              f"the discovered row's command is not the resolved path plus the "
              f"table's argv: {routes[model.id].command!r}")
        # And `get` is still the one lookup, over both kinds.
        check(store.get(model.id).command == expected_command(paths, tool, model),
              "a discovered row must resolve through the same `get`")
        store.disable(model.id)
        check(set(store.read()) == {"mine"}, "switching off left the row behind")
        check(store.read()["mine"].command == PRIVATE_COMMAND,
              "switching off rewrote the operator's row")

    with discovered_tools(present=[tool.program]) as (store, _marker, paths):
        # The operator's own row, under the id discovery would use. Refused in
        # both directions rather than overwritten or silently kept.
        store.path.parent.mkdir(parents=True, exist_ok=True)
        store.path.write_text(json.dumps({"version": 1, "routes": {
            model.id: {"label": "Mine", "command": PRIVATE_COMMAND,
                       "window": 1000, "model": "mine"}}}), encoding="utf-8")
        os.chmod(store.path, 0o600)
        for verb, call in (("enable", store.enable), ("disable", store.disable)):
            try:
                call(model.id)
            except commands.CommandsError:
                pass
            else:
                failures.append(f"{verb} edited a route the operator wrote")
        check(store.read()[model.id].command == PRIVATE_COMMAND,
              "the operator's row did not survive")
        check(store.discovered()[0]["owned"] is True,
              "the page is not told why its toggle would be refused")


def test_the_enable_route_takes_an_id_and_the_table_is_the_only_source() -> None:
    """Over a real socket: what the browser may say, and what it may not.

    Every probe here is a string a browser could put in the path segment, and
    every one of them is refused by `check_tool_id` before anything is
    resolved, written or run. The marker file is the measurement: none of them
    may start a program.
    """
    tool, model = commands.expansions()[0]
    with discovered_tools(present=[tool.program, OUTSIDE_TABLE]) as (
            store, marker, paths):
        with live_server(store) as built:
            base = built.url
            refused = (
                # A program that really is on this PATH, and really is not in
                # the table. The refusal is the table's, not `which`'s.
                OUTSIDE_TABLE,
                # A path, in the two spellings that reach a path segment.
                "%2Fbin%2Fsh",
                "..%2F..%2Fbin%2Fsh",
                # A command line.
                "sh%20-c%20touch",
                # An id shaped like one of the operator's routes but not in
                # the table: discovery's list is not the allowlist's.
                "opus-sub",
            )
            for name in refused:
                status, raw = request(f"{base}/api/v1/settings/commands/{name}",
                                      method="PUT")
                payload = as_json(raw) or {}
                code = (payload.get("error") or {}).get("code", "")
                check(status == 400,
                      f"PUT .../{name} was answered {status}, not refused")
                check(code == "bad_command_tool",
                      f"PUT .../{name} was refused as {code!r}, which does not "
                      f"name the field")
            check(store.read() == {},
                  f"a refused enable wrote a route: {sorted(store.read())}")

            # And the id that is in the table is accepted, or every refusal
            # above is a refusal of a route that could never have been made.
            status, raw = request(f"{base}/api/v1/settings/commands/{model.id}",
                                  method="PUT")
            payload = as_json(raw) or {}
            check(status == 200, f"the table's own id was answered {status}")
            check(payload.get("enabled") is True and payload.get("id") == model.id,
                  f"the answer must state the new state, got {payload}")
            check(store.read()[model.id].command == expected_command(paths, tool, model),
                  "the command written is not the resolved path plus the "
                  "table's argv")
        check(not marker.exists(),
              f"switching a route on must not run it; {marker} exists")


def test_the_seeded_hole_runs_the_program_the_probe_names() -> None:
    """**The must-fire half**, and the whole reason the probe above is evidence.

    One call removed -- `check_tool_id` -- and the same `PUT` that was refused
    five times writes a route, the same submit runs it, and the marker file
    appears. Without this, "no program was started" is a sentence about a
    backend that could never have started one, and would read green with the
    feature deleted.
    """
    with discovered_tools(present=[OUTSIDE_TABLE], holed=True) as (
            store, marker, _paths):
        with live_server(store) as built:
            base = built.url
            status, _raw = request(
                f"{base}/api/v1/settings/commands/{OUTSIDE_TABLE}", method="PUT")
            check(status == 200,
                  f"the seeded hole did not open: PUT answered {status}")
            check(OUTSIDE_TABLE in store.read(),
                  "the seeded hole wrote no route, so the probe below proves "
                  "nothing")
            status, raw = request(f"{base}/api/v1/runs", method="POST",
                                  payload=a_submission(command_route=OUTSIDE_TABLE))
            accepted = as_json(raw) or {}
            check(status == 202, f"the holed route was answered {status}")
            job_id = accepted.get("id", "")
            if job_id:
                finished(base, job_id)
        check(marker.exists(),
              "the seeded hole did not execute the named program, so the "
              "refusals asserted above are not measurements")


def model_ran(marker: Path) -> set[str]:
    """Which model the program was actually told to use, off its own argv.

    Read back rather than assumed. A route that declares Haiku in its label
    and runs the CLI's default is precisely the defect the model rows exist to
    remove, and it is invisible from the outside: the run finishes, the report
    carries the route's declared name, and nothing compared the two. The fake
    tool echoes its argv, and this is what reads it.
    """
    found = set()
    for line in argv_lines(marker):
        parts = line.split()
        for index, part in enumerate(parts):
            if part == "--model" and index + 1 < len(parts):
                found.add(parts[index + 1])
    return found


def test_a_discovered_route_runs_the_model_it_declares() -> None:
    """**The route's word against the program's argv**, for two models.

    Two routes, two models, one tool, driven end to end over a socket. Three
    things have to agree for each: the row the page would show, the model in
    the run's own provenance, and the `--model` the program was actually
    handed. The third is the one no other check here looks at, and it is the
    one that catches a route whose label says Haiku and whose command says
    nothing.

    Seeded: the mismatch check below runs the same comparison against a route
    whose argv was rewritten to the other model, and fires.
    """
    pairs = commands.expansions()
    check(len(pairs) >= 2,
          "this check needs two models on one tool to be worth running")
    if len(pairs) < 2:
        return
    (tool, first), (_same, second) = pairs[0], pairs[1]
    check(first.model != second.model, "the two probes pin the same model")

    for model in (first, second):
        with discovered_tools(present=[tool.program]) as (store, marker, _paths):
            with live_server(store) as built:
                base = built.url
                status, _raw = request(
                    f"{base}/api/v1/settings/commands/{model.id}", method="PUT")
                check(status == 200,
                      f"enabling {model.id} answered {status}")
                check(store.read()[model.id].model == model.model,
                      f"the written route does not declare {model.model!r}")
                status, raw = request(f"{base}/api/v1/runs", method="POST",
                                      payload=a_submission(command_route=model.id))
                job_id = (as_json(raw) or {}).get("id", "")
                check(status == 202 and bool(job_id),
                      f"{model.id} was answered {status}: {raw[:200]!r}")
                if not job_id:
                    continue
                payload = finished(base, job_id)
                check(payload.get("state") == "done",
                      f"{model.id} did not finish: {payload.get('state')!r} "
                      f"{str(payload.get('error'))[:200]!r}")

                # 1. what the program was told, read off its own argv.
                asked = model_ran(marker)
                check(asked == {model.model},
                      f"{model.id} declares {model.model!r} and the program "
                      f"was told {sorted(asked)}")
                # 2. what the run recorded, read off provenance rather than
                #    off the route this test already has in hand.
                recorded = (((payload.get("report") or {}).get("provenance")
                             or {}).get("models") or {})
                names = {str(value) for value in recorded.values()} if isinstance(
                    recorded, dict) else set()
                if not names:
                    names = {str((payload.get("report") or {}).get("model", ""))}
                check(names == {model.model},
                      f"{model.id} ran as {sorted(names)} and declares "
                      f"{model.model!r}")
                # 3. and the banner the operator watched named it too.
                _status, body = request(f"{base}/api/v1/runs/{job_id}/events")
                banner = [line for line in body.decode("utf-8", "replace").splitlines()
                          if '"banner"' in line]
                check(any(model.model in line for line in banner),
                      f"the banner does not name {model.model!r}")


def test_the_declared_model_check_fires_on_an_argv_that_selects_another() -> None:
    """Seeded: a route that declares one model and asks the program for another.

    This is the defect, built on purpose. The route's `model` field says
    Haiku, its command says Sonnet, and every other signal in the system --
    the picker row, the banner, the provenance block -- reports Haiku, because
    every one of them reads the field. Only the argv says otherwise, which is
    why the argv is what the check above reads.
    """
    pairs = commands.expansions()
    if len(pairs) < 2:
        return
    (tool, declared), (_same, actually) = pairs[0], pairs[1]
    with discovered_tools(present=[tool.program]) as (store, marker, paths):
        store.enable(declared.id)
        # One field rewritten: the argv, and nothing else. The route still
        # declares the first model everywhere a reader can see.
        routes = store.read()
        routes[declared.id] = commands.Route(
            id=declared.id, label=declared.label,
            command=shlex.join((paths[tool.program], *tool.base_args,
                                *actually.select)),
            window=tool.window, model=declared.model, discovered=True)
        store._write(routes)
        with live_server(store) as built:
            base = built.url
            status, raw = request(f"{base}/api/v1/runs", method="POST",
                                  payload=a_submission(command_route=declared.id))
            job_id = (as_json(raw) or {}).get("id", "")
            check(status == 202, f"the seeded route was answered {status}")
            if job_id:
                finished(base, job_id)
        asked = model_ran(marker)
        check(asked == {actually.model},
              f"the seeded route did not reach the program: {sorted(asked)}")
        check(asked != {declared.model},
              "the seeded mismatch does not differ from the declaration, so "
              "the check above is comparing a value with itself")
        check(store.read()[declared.id].model == declared.model,
              "the seeded route stopped declaring the model it declares, so "
              "the mismatch is not the one being probed")


def test_a_discovered_route_runs_and_its_path_reaches_no_served_body() -> None:
    """The control run for discovery, and the leak search with a live target.

    The path `shutil.which` resolved is in the store and in the file for the
    whole of this check, so every `not in` below is looking for a string that
    exists rather than passing over an absence.
    """
    tool, model = commands.expansions()[0]
    with discovered_tools(present=[tool.program]) as (store, marker, paths):
        resolved = expected_command(paths, tool, model)
        program = paths[tool.program]
        with live_server(store) as built:
            base = built.url
            status, _raw = request(f"{base}/api/v1/settings/commands/{model.id}",
                                   method="PUT")
            check(status == 200, f"enabling answered {status}")
            status, raw = request(f"{base}/api/v1/runs", method="POST",
                                  payload=a_submission(command_route=model.id))
            accepted = as_json(raw) or {}
            check(status == 202,
                  f"a discovered route was answered {status}: {raw[:200]!r}")
            job_id = accepted.get("id", "")
            check(bool(job_id), "a discovered route must produce a job")
            if not job_id:
                return
            payload = finished(base, job_id)
            check(payload.get("state") == "done",
                  f"the discovered run did not finish: "
                  f"{payload.get('state')!r} {str(payload.get('error'))[:200]!r}")
            check(marker.exists(),
                  "the discovered command was never started, so the searches "
                  "below prove nothing about a live route")
            check(store.read()[model.id].command == resolved,
                  f"the store must hold the resolved command throughout, got "
                  f"{store.read()[model.id].command!r}")

            for name, url in (("config", f"{base}/api/v1/config"),
                              ("run", f"{base}/api/v1/runs/{job_id}"),
                              ("report", f"{base}/api/v1/runs/{job_id}/report.html"),
                              ("report page", f"{base}/api/v1/runs/{job_id}/report"),
                              ("merged", f"{base}/api/v1/runs/{job_id}/merged"),
                              ("events", f"{base}/api/v1/runs/{job_id}/events")):
                status, body = request(url)
                check(status == 200,
                      f"the {name} route answered {status}, so the search below "
                      f"is looking at an error body")
                text = body.decode("utf-8", "replace")
                check(program not in text,
                      f"the {name} response carries the resolved path")
                check(resolved not in text,
                      f"the {name} response carries the whole command line")
                check(str(Path(program).parent) not in text,
                      f"the {name} response carries the directory it is in")
            # The audit bundle, member by member. Deflated bytes hide a
            # string from a `not in` over the archive, so the search is over
            # what a reader extracts rather than over what came down the wire
            # -- which is the whole reason this is a block of its own and not
            # one more row in the loop above.
            status, raw = request(f"{base}/api/v1/runs/{job_id}/{api.BUNDLE_ZIP}")
            check(status == 200,
                  f"the bundle answered {status}, so the search below is "
                  f"looking at an error body")
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                names = archive.namelist()
                check(len(names) >= 4,
                      f"the bundle holds {names}; a search over an almost "
                      f"empty archive proves nothing")
                for name in names:
                    text = archive.read(name).decode("utf-8", "replace")
                    check(program not in text,
                          f"the bundle member {name} carries the resolved path")
                    check(resolved not in text,
                          f"the bundle member {name} carries the whole "
                          f"command line")
                    check(str(Path(program).parent) not in text,
                          f"the bundle member {name} carries the directory it "
                          f"is in")
                # And the label is in it, so the bundle names the route that
                # ran -- the same substitution the report makes.
                report = archive.read("report.html").decode("utf-8", "replace")
                check(model.label in report,
                      "the bundled report does not name the route that ran")

            # The label the table wrote is what a reader gets instead.
            _status, page = request(f"{base}/api/v1/runs/{job_id}/report.html")
            check(model.label in page.decode("utf-8", "replace"),
                  "the report does not name the route that ran")


def test_a_discovered_id_is_refused_until_it_is_switched_on() -> None:
    """Found is not enabled, and the submit path knows only the allowlist.

    The id is in the discovered set the page renders the whole time. What
    decides whether a run may use it is the file, which is the same lookup a
    hand-written route goes through -- there is no second list a submit can be
    answered from.
    """
    tool, model = commands.expansions()[0]
    with discovered_tools(present=[tool.program]) as (store, marker, _paths):
        with live_server(store) as built:
            base = built.url
            _status, body = request(f"{base}/api/v1/config")
            block = (as_json(body) or {}).get("commands") or {}
            found = [row for row in block.get("discovered") or []
                     if row["id"] == model.id]
            check(bool(found) and found[0]["available"] is True,
                  "the tool must be reported as found before it is enabled")
            check(block.get("routes") == [],
                  "a found tool must not be offered in the picker until it is on")
            status, raw = request(f"{base}/api/v1/runs", method="POST",
                                  payload=a_submission(command_route=model.id))
            payload = as_json(raw) or {}
            check(status == 400,
                  f"a discovered but unenabled id was answered {status}")
            check((payload.get("error") or {}).get("code") == "bad_command_route",
                  f"refused as {payload.get('error')}, which does not name the "
                  f"field")
        check(not marker.exists(),
              "a discovered but unenabled id started the program")


def test_only_the_operator_may_switch_a_tool_on() -> None:
    """A command route is shared by everybody here, so it is not everybody's.

    Driven over the socket with two real accounts and two real sessions, not
    by calling `_operator` directly. A member's `PUT` is refused and
    nothing is written, and the operator's over the same store is accepted, or
    the refusal is a refusal of a route nobody could use.
    """
    tool, model = commands.expansions()[0]
    with discovered_tools(present=[tool.program]) as (store, marker, _paths):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            people = user_accounts.Accounts(root / "accounts.json")
            setup = user_accounts.Setup()
            built = server.build(
                port=0, accounts=people, setup=setup, commands=store,
                keys=credentials.Credentials(root / "credentials.json"),
                work_dir=root / "work",
                environ={"LLOSSLESS_BASE_URL": UNUSED_ENDPOINT,
                         "LLOSSLESS_WINDOW": "200000"})
            thread = server.background(built)
            base = built.url
            try:
                request(f"{base}/api/v1/setup", method="POST",
                        payload={"token": setup.token, "username": "alice",
                                 "password": "a-long-enough-password"})

                def session(name, password):
                    _status, raw_body = request(
                        f"{base}/api/v1/session", method="POST",
                        payload={"username": name, "password": password,
                                 "token": True})
                    token = (as_json(raw_body) or {}).get("token", "")
                    return {user_accounts.SESSION_HEADER: token}

                alice = session("alice", "a-long-enough-password")
                request(f"{base}/api/v1/accounts", method="POST", headers=alice,
                        payload={"username": "bob",
                                 "password": "another-long-password"})
                bob = session("bob", "another-long-password")

                url = f"{base}/api/v1/settings/commands/{model.id}"
                status, raw_body = request(url, method="PUT", headers=bob)
                code = ((as_json(raw_body) or {}).get("error") or {}).get("code", "")
                check(status == 403,
                      f"a member's enable was answered {status}, not refused")
                check(code == "not_operator",
                      f"refused as {code!r}, which is not about who they are")
                check(store.read() == {},
                      "a member's refused enable wrote a route")
                # A member still sees the panel, or the page has a blank box
                # for everybody who is not the operator.
                _status, body = request(f"{base}/api/v1/config", headers=bob)
                block = (as_json(body) or {}).get("commands") or {}
                check(len(block.get("discovered") or []) == len(commands.expansions()),
                      "a member is not told what this server found")
                check(block.get("editable") is False,
                      "a member is not told that the toggle is not theirs")

                status, _raw = request(url, method="PUT", headers=alice)
                check(status == 200,
                      f"the operator's enable was answered {status}, so the "
                      f"refusal above is a refusal of nothing")
                check(model.id in store.read(), "the operator's enable wrote nothing")
                _status, body = request(f"{base}/api/v1/config", headers=alice)
                block = (as_json(body) or {}).get("commands") or {}
                check(block.get("editable") is True,
                      "the operator is told the toggle is not theirs")
            finally:
                built.shutdown()
                built.server_close()
                built.store.close()
                thread.join(timeout=5)
        check(not marker.exists(),
              "switching a route on over two accounts ran the program")


def test_config_reports_the_discovered_set_and_who_may_change_it() -> None:
    """What the credentials sheet reads, including its two empty states."""
    tool, model = commands.expansions()[0]
    with discovered_tools(present=[]) as (store, _marker, _paths):
        with live_server(store) as built:
            _status, body = request(f"{built.url}/api/v1/config")
            block = (as_json(body) or {}).get("commands") or {}
            check(block.get("configurable") is True,
                  "a server with a commands file can record a route")
            check(len(block.get("discovered") or []) == len(commands.expansions()),
                  "a machine with nothing installed still reports the table, "
                  "or the panel is blank with no explanation")
            check(all(row["available"] is False
                      for row in block.get("discovered") or []),
                  "nothing is installed and something was reported as found")
            check(block.get("editable") is True,
                  "a single-tenant server has nobody who is not the operator")
    # And the other empty state: a server with no store at all.
    with tempfile.TemporaryDirectory() as raw:
        built = server.build(port=0, work_dir=Path(raw) / "work",
                             environ={"LLOSSLESS_BASE_URL": UNUSED_ENDPOINT})
        try:
            block = built.api.config().get("commands") or {}
            check(block.get("configurable") is False,
                  "a server built with no store has nowhere to write a route")
            check(block.get("discovered") == [],
                  f"and offers nothing to switch on, got {block.get('discovered')}")
        finally:
            built.server_close()
            built.store.close()
    check(commands.NoCommands().writable is False,
          "NoCommands must say it cannot be written")


def test_the_pre_rename_config_files_are_not_read() -> None:
    """The pre-rename `commands.json` and its two neighbours are never read.

    Against a temporary `XDG_CONFIG_HOME` holding only the old files. Each of
    the three resolves to the new directory, the page's config block carries
    no `legacy_file` flag, nothing is said on stderr, and the old files are
    left where they were. `CLAIMCHECK_COMMANDS` names nothing. Must fire:
    `LLOSSLESS_COMMANDS` names the file it points at.
    """
    with tempfile.TemporaryDirectory() as raw:
        home = {"XDG_CONFIG_HOME": raw}
        old_dir, new_dir = Path(raw) / "claimcheck", Path(raw) / "llossless"
        old_dir.mkdir()
        for name in ("commands.json", "credentials.json", "accounts.json"):
            (old_dir / name).write_text("{}", encoding="utf-8")
        (old_dir / "commands.json").write_text(
            json.dumps({"version": 1, "routes": {}}), encoding="utf-8")
        os.chmod(old_dir / "commands.json", 0o600)
        with contextlib.redirect_stderr(io.StringIO()) as err:
            check(commands.default_path(home) == new_dir / "commands.json",
                  f"the old commands file must not be read: {commands.default_path(home)}")
            check(credentials.default_path(home) == new_dir / "credentials.json",
                  "the old credentials file must not be read")
            check(user_accounts.default_path(home) == new_dir / "accounts.json",
                  "the old accounts file must not be read")
            routes = commands.Commands(environ=home, which=lambda _name: None)
            built = server.build(port=0, work_dir=Path(raw) / "work", commands=routes,
                                 environ={"LLOSSLESS_BASE_URL": UNUSED_ENDPOINT})
            try:
                block = built.api.config().get("commands") or {}
            finally:
                built.server_close()
                built.store.close()
        check(routes.path == new_dir / "commands.json"
              and not hasattr(routes, "legacy_location") and "legacy_file" not in block,
              f"the page must hear nothing about an old file: {sorted(block)}")
        check("claimcheck" not in err.getvalue() and "old location" not in err.getvalue(),
              f"nothing may be said about the old files: {err.getvalue()!r}")

        named = str(Path(raw) / "elsewhere.json")
        with contextlib.redirect_stderr(io.StringIO()):
            fired = commands.Commands(environ=dict(home, LLOSSLESS_COMMANDS=named))
            ignored = commands.Commands(environ=dict(home, CLAIMCHECK_COMMANDS=named))
        check(fired.path == Path(named),
              "must fire: LLOSSLESS_COMMANDS names the file")
        check(ignored.path == new_dir / "commands.json",
              f"CLAIMCHECK_COMMANDS must name nothing: {ignored.path}")
        check(sorted(p.name for p in old_dir.iterdir())
              == ["accounts.json", "commands.json", "credentials.json"],
              "the old files must stay where they were")


def test_config_says_which_row_is_wrong_and_which_route_was_retired() -> None:
    """The two things the page could not say, over HTTP, where it reads them.

    The operator met one message and it was page-level: the picker was empty
    and the panel was a paragraph about a file they had never written. Both
    halves are served per route now -- the reason beside the row it names, and
    the retired id so a route that was there yesterday does not just go.

    **And the leak rule still binds.** Every one of these strings is built
    around `self.path`, which is an absolute path under the account the server
    runs as, exactly the shape this feature was once caught producing.
    It goes through `redact.text`, the same scrub `ApiError` uses.
    """
    tool, model = commands.expansions()[0]
    broken = {"label": "Mine", "command": PRIVATE_COMMAND, "window": 200000}
    stale = {"label": "Old", "command": PRIVATE_COMMAND, "window": 200000,
             "discovered": True}
    with discovered_tools(present=[tool.program]) as (store, _marker, _paths):
        store.path.parent.mkdir(parents=True, exist_ok=True)
        store.path.write_text(json.dumps({"version": 1, "routes": {
            "hand-broken": dict(broken), "claude": dict(stale)}}),
            encoding="utf-8")
        os.chmod(store.path, 0o600)
        with live_server(store) as built:
            _status, body = request(f"{built.url}/api/v1/config")
            block = (as_json(body) or {}).get("commands") or {}
            problems = block.get("problems") or []
            check([bad["id"] for bad in problems] == ["hand-broken"],
                  f"the row that did not load must be reported: {problems}")
            check("hand-broken" in (problems[0]["reason"] if problems else ""),
                  "and the reason must name the route it is about")
            check(block.get("retired") == ["claude"],
                  f"and the retired route must be named: {block.get('retired')}")
            # `live_server` goes through `server.build`, which is where
            # `migrate()` runs -- so this is the command's own path and not a
            # call this check made.
            after = json.loads(store.path.read_text(encoding="utf-8"))["routes"]
            check(set(after) == {"hand-broken"},
                  f"the orphan must be gone and the hand row kept: {after}")
            whole = body.decode("utf-8")
            check(PRIVATE_COMMAND not in whole,
                  "a command out of an unusable row reached /config")
            check(PRIVATE_STEM not in whole,
                  "part of a command out of an unusable row reached /config")
            # Pinned against the shipped call rather than re-derived: what is
            # served has to be what `redact.text` makes of the store's own
            # sentence, under the roots this server was built with.
            raw = [bad.reason for bad in store.problems()]
            check(len(raw) == 1, f"one unusable row is the fixture: {raw}")
            check(problems and raw and problems[0]["reason"]
                  == redact.text(raw[0], extra=built.api.extra_roots),
                  "the served reason is not the scrubbed form of the store's")
            # And the scrub is not a no-op on this shape. The fixture's file
            # is under a temporary directory, which is nobody's root; on a
            # deployment it is under the operator's home, which is one -- and
            # their own report came back reading `<redacted>/.config/...`,
            # which is this working.
            here = redact.text(raw[0], extra=(str(store.path.parent),))
            check(str(store.path) not in here and redact.MARK in here,
                  f"redact.text must clear the commands file's path when its "
                  f"directory is a root: {here}")


def test_sourced_refuses_a_route_that_cannot_retrieve_and_grants_one_that_can() -> None:
    """The level's safety property, at the layer a browser reaches it through.

    `config` owns the rule and `tests/test_cli.py` seeds it there; what is
    seeded here is that the *web* path enforces it, that it does so **before a
    job id exists**, and that the refusal names the route the submitter chose
    rather than only the mechanism. A refusal an operator meets after the work
    was accepted is a refusal they meet in a log.

    The automatic grant is the other half and is the operator's decision:
    *"make it automatic and make it obvious in the UI"*. So a recognised
    program gets `WebSearch` and `WebFetch` without the file being
    edited, and the page is told about it in a field of its own.
    """
    documents = {"a.md": SOURCE_A, "b.md": SOURCE_B}
    sourced = {"LLOSSLESS_FIDELITY": config.SOURCED}

    # Must fire: a hand-written route to a program this build has never read
    # the flags of. Nothing is appended to it, so it cannot retrieve.
    with routes_file({"wrapper": {"label": "A wrapper", "window": 4096,
                                  "command": "/usr/local/bin/my-wrapper.sh",
                                  "model": "whatever"}}) as (store, _path):
        request = jobs.MergeRequest(documents=documents, route="wrapper",
                                    overrides=dict(sourced))
        try:
            jobs.resolved_environ(request, {}, routes=store)
            check(False, "a sourced run through a route that cannot retrieve "
                         "was accepted; it would have answered from recall and "
                         "labelled the answer retrieved")
        except jobs.JobRefused as refusal:
            check("wrapper" in str(refusal),
                  f"the refusal must name the route that was chosen: {refusal}")
            check("my-wrapper.sh" in str(refusal),
                  f"and what is missing from it: {refusal}")

        # Must not fire: the same route at every other level runs.
        for level in config.FIDELITY_LEVELS:
            if level == config.SOURCED:
                continue
            environ = jobs.resolved_environ(
                jobs.MergeRequest(documents=documents, route="wrapper",
                                  overrides={"LLOSSLESS_FIDELITY": level}),
                {}, routes=store)
            check(environ["LLOSSLESS_COMMAND"] == "/usr/local/bin/my-wrapper.sh",
                  f"{level} must run the operator's own argv untouched: "
                  f"{environ['LLOSSLESS_COMMAND']!r}")

    # Must fire: no route at all. An HTTP endpoint has nothing to grant.
    try:
        jobs.resolved_environ(
            jobs.MergeRequest(documents=documents, overrides=dict(sourced)),
            {"LLOSSLESS_BASE_URL": UNUSED_ENDPOINT})
        check(False, "sourced over an HTTP endpoint was accepted")
    except jobs.JobRefused as refusal:
        check("open" in str(refusal),
              f"the refusal must name the level to use instead: {refusal}")

    # Must fire: a recognised program the build can grant a tool to, on
    # a route answering in plain text. It could retrieve and could never say
    # whether it had, which is the state an operator ran in for hours with a
    # report that looked normal. Refused before a job id, naming the route,
    # and the picker's retrieval marker is gone from its row.
    silent = {"claude-plain": {
        "label": "Claude Code - Sonnet", "window": 200000, "model": "sonnet",
        "command": "/opt/claude-cli/bin/claude --print --model sonnet"}}
    with routes_file(silent) as (store, _path):
        try:
            jobs.resolved_environ(
                jobs.MergeRequest(documents=documents, route="claude-plain",
                                  overrides=dict(sourced)),
                {}, routes=store)
            check(False, "a sourced run through a route that reports no turn "
                         "count was accepted")
        except jobs.JobRefused as refusal:
            check("claude-plain" in str(refusal) and "turn count" in str(refusal),
                  f"the refusal must name the route and what it cannot "
                  f"report: {refusal}")
        row = next(entry for entry in store.describe()
                   if entry["id"] == "claude-plain")
        check(row["retrieval"] == [],
              f"a route sourced refuses must not be marked as retrieving: {row}")

    # Must not fire, and this is the automatic grant: a route whose program
    # this build recognises runs, and the argv it runs carries the flag.
    recognised = {"claude-sonnet": {
        "label": "Claude Code - Sonnet", "window": 200000, "model": "sonnet",
        "command": "/opt/claude-cli/bin/claude --print --model sonnet "
                   + " ".join(config.RESULT_ARGS),
        "envelope": config.ENVELOPE_RESULT}}
    with routes_file(recognised) as (store, path):
        environ = jobs.resolved_environ(
            jobs.MergeRequest(documents=documents, route="claude-sonnet",
                              overrides=dict(sourced)),
            {}, routes=store)
        # The grant is applied by `config.resolve`, which is the single writer
        # and the function the worker thread reaches. What the job layer has to
        # get right is that it does not refuse a route this build can grant.
        settings = config.resolve(None, environ=dict(
            environ, LLOSSLESS_WINDOW="200000"))
        check(environ.get("LLOSSLESS_COMMAND_ENVELOPE") == config.ENVELOPE_RESULT,
              f"the route's envelope must reach the run: {environ}")
        check(config.granted_web_tools(settings.command) == ("WebSearch", "WebFetch"),
              f"a recognised program must be granted both web tools "
              f"automatically: {settings.command!r}")

        # **And the operator's file is not edited by any of it.** The grant is
        # a property of the run, not a line written into a file the server was
        # given to read.
        on_disk = json.loads(path.read_text(encoding="utf-8"))
        check(on_disk["routes"]["claude-sonnet"] == recognised["claude-sonnet"],
              f"the automatic grant rewrote the operator's file: {on_disk}")

        # The page is told, in a field of its own, rather than left to work it
        # out from a command it is never shown.
        row = next(entry for entry in store.describe()
                   if entry["id"] == "claude-sonnet")
        check(row["retrieval"] == ["WebSearch", "WebFetch"]
              and row["retrieval_granted"] is False,
              f"the served row must say what a sourced run would be permitted "
              f"and that the operator did not grant it: {row}")
        check("command" not in row and "my-wrapper" not in json.dumps(row),
              f"and it must still never carry the command: {row}")


def test_a_sourced_run_says_whether_anything_was_retrieved_and_opens_no_socket() -> None:
    """End to end over a socket: the run the whole level exists to report on.

    The measured fact this rests on is that the two counters disagree here.
    `server_tool_use` counts a vendor's server-side web tools and reports zero
    for a subscription CLI that demonstrably fetched, because that fetch
    happened locally in the CLI's own process; `num_turns` counts the round
    trip the tool call cost and does move. The fake reproduces exactly that
    pair, so a report that read the blind counter would be green here and
    would be wrong in production.

    Three things have to come back: that retrieval was permitted, that the
    turn counter saw tool use, and that **LLossless itself still opened no
    socket** -- which is not the same sentence and never changes. The last is
    the socket guard this module installs, asserted over the whole run rather
    than assumed.
    """
    with fake_route(web_tools=["WebFetch"], envelope="result",
                    command_suffix=" --output-format json "
                                   f"{commands.ALLOW_TOOLS_FLAG} WebFetch"
                                   " --simulate-tool-use"
                    ) as (store, _marker, command):
        check(commands.ALLOW_TOOLS_FLAG in command,
              f"the fixture route must carry the grant it declares: {command!r}")
        route = store.read()["opus-sub"]
        check(route.retrieval == ("WebFetch",) and route.described()["retrieval_granted"],
              f"the route must report the operator's own grant: {route.retrieval}")

        with live_server(store) as built:
            base = built.url
            before = list(socket_guard.blocked())
            status, raw = request(
                f"{base}/api/v1/runs", method="POST",
                payload=a_submission(command_route="opus-sub",
                                     fidelity=config.SOURCED))
            job_id = (as_json(raw) or {}).get("id", "")
            check(status == 202 and bool(job_id),
                  f"a sourced run through a route that can retrieve was "
                  f"answered {status}: {raw[:200]!r}")
            if not job_id:
                return
            payload = finished(base, job_id)
            check(payload.get("state") == "done",
                  f"the sourced run did not finish: {payload.get('state')!r} "
                  f"{str(payload.get('error'))[:300]!r}")

            report = payload.get("report") or {}
            sourcing = report.get("sourcing") or {}
            check(sourcing.get("state") == "not-searched",
                  f"the blind counter must still report its zero rather than "
                  f"being dropped: {sourcing.get('state')!r}")
            check((sourcing.get("tool_use") or {}).get("state") == "tool-use",
                  f"and the turn counter must report the tool use it can see: "
                  f"{sourcing.get('tool_use')!r}")
            check(sourcing.get("recall_only") is False,
                  f"a run that used a tool is not recall-only: {sourcing!r}")
            check(sourcing.get("retrieval") == "retrieved",
                  f"and the level's outcome is served in one word: "
                  f"{sourcing!r}")
            check(sourcing.get("retrieval_permitted") == ["WebFetch"],
                  f"and the report must say what was permitted: "
                  f"{sourcing.get('retrieval_permitted')!r}")

            retrieval = ((report.get("provenance") or {}).get("retrieval") or {})
            check(retrieval.get("permitted") == ["WebFetch"],
                  f"provenance must carry the grant: {retrieval!r}")
            check("fetch" not in str(retrieval.get("described", "")),
                  f"and describe it in turns rather than in fetches: "
                  f"{retrieval.get('described')!r}")

            _status, body = request(f"{base}/api/v1/runs/{job_id}/events")
            banner = [line for line in body.decode("utf-8", "replace").splitlines()
                      if '"banner"' in line]
            check(any("WebFetch" in line for line in banner),
                  "the banner the submitter watched must name the grant")

            # The sentence that never changes, in the artefact a reader keeps.
            _status, page = request(f"{base}/api/v1/runs/{job_id}/report.html")
            text = page.decode("utf-8", "replace")
            check("no network request of any kind" in text,
                  "the report must go on saying what this tool did, which is "
                  "nothing, whatever the model was permitted")
            check("permitted to reach the network" in text,
                  "and it must disclose, unprompted, that the model was not "
                  "under the same constraint")
            check("turns rather than in fetches" in text,
                  "and say what the number it printed is a count of")
            check("The model retrieved." in text,
                  "and the verdict must say what the level achieved, not only "
                  "what it permitted")

            # The guard refuses any destination but the configured endpoint
            # and the loopback ports this process bound, and it reports what
            # it did rather than staying silent. Nothing may be added to that
            # list by a run whose model was granted a web tool: the tool runs
            # in the model's process, and this one still opens no socket.
            after = list(socket_guard.blocked())
            check(after == before,
                  f"a sourced run was refused a socket from this process, so "
                  f"something here tried to open one: "
                  f"{[row for row in after if row not in before]}")
            endpoint = ((report.get("provenance") or {}).get("endpoint") or {})
            check(endpoint.get("location") == "command",
                  f"and the whole run must have gone through the program: "
                  f"{endpoint!r}")


def test_a_sourced_run_that_retrieved_nothing_says_so_rather_than_averaging_it_away() -> None:
    """The interesting case, and the one a report must not smooth over.

    The level asked the model to go and look. It was granted a tool, it did not
    use it, and every citation under the additions heading is therefore a
    recollection -- which is the state a reader would otherwise mistake for a
    checked one, because the citation itself reads identically either way. That
    was measured: two runs of the same pair at the same level, one with the
    tool and one without, cited the same authority in near-identical words, and
    one of them named the wrong licence.

    The pair with the test above varies exactly one thing: the fake's
    `--simulate-tool-use` flag. The grant, the route, the documents, the level
    and the envelope are held constant, so a difference in what the report says
    is a difference the turn counter produced.
    """
    with fake_route(web_tools=["WebFetch"], envelope="result",
                    command_suffix=" --output-format json "
                                   f"{commands.ALLOW_TOOLS_FLAG} WebFetch"
                    ) as (store, _marker, _command):
        with live_server(store) as built:
            base = built.url
            status, raw = request(
                f"{base}/api/v1/runs", method="POST",
                payload=a_submission(command_route="opus-sub",
                                     fidelity=config.SOURCED))
            job_id = (as_json(raw) or {}).get("id", "")
            check(status == 202 and bool(job_id),
                  f"the control run was answered {status}: {raw[:200]!r}")
            if not job_id:
                return
            payload = finished(base, job_id)
            check(payload.get("state") == "done",
                  f"the control run did not finish: {payload.get('state')!r}")

            sourcing = (payload.get("report") or {}).get("sourcing") or {}
            check((sourcing.get("tool_use") or {}).get("state") == "no-tool-use",
                  f"the turn counter must report the absence it measured: "
                  f"{sourcing.get('tool_use')!r}")
            check(sourcing.get("recall_only") is True,
                  f"a sourced run that used no tool is recall-only, and the "
                  f"report has to say so in a field rather than leave a page "
                  f"to derive it from a level name: {sourcing!r}")
            check(sourcing.get("retrieval_permitted") == ["WebFetch"],
                  f"and it must still say the tool was there to be used, or "
                  f"'did not look' reads as 'could not': {sourcing!r}")
            check(sourcing.get("retrieval") == "not-retrieved",
                  f"the level's outcome, in one word: {sourcing!r}")

            _status, page = request(f"{base}/api/v1/runs/{job_id}/report.html")
            text = page.decode("utf-8", "replace")
            check("retrieved nothing" in text,
                  "the artefact a reader keeps must say it in words")
            check("Nothing was retrieved." in text,
                  "and the verdict must say it, not only the provenance notes")


def test_a_sourced_run_whose_backend_reported_no_turn_count_says_unmeasured() -> None:
    """The third state, and the one an operator ran in for hours unwarned.

    The pair above varies whether the model used the tool. This varies whether
    the answer said: the envelope arrives, carries the text, and carries no
    `num_turns`. Nothing else changes -- grant, route, documents, level. The
    run must finish, and every surface must say **unmeasured** and none may
    say "did not retrieve": a reader told nothing was looked up trusts the
    citations less than they deserve only if that is true, and here nobody
    knows.
    """
    with fake_route(web_tools=["WebFetch"], envelope="result",
                    command_suffix=" --output-format json "
                                   f"{commands.ALLOW_TOOLS_FLAG} WebFetch"
                                   " --omit-turns"
                    ) as (store, _marker, _command):
        with live_server(store) as built:
            base = built.url
            status, raw = request(
                f"{base}/api/v1/runs", method="POST",
                payload=a_submission(command_route="opus-sub",
                                     fidelity=config.SOURCED))
            job_id = (as_json(raw) or {}).get("id", "")
            check(status == 202 and bool(job_id),
                  f"the unmeasured run was answered {status}: {raw[:200]!r}")
            if not job_id:
                return
            payload = finished(base, job_id)
            check(payload.get("state") == "done",
                  f"the unmeasured run did not finish: {payload.get('state')!r}")

            sourcing = (payload.get("report") or {}).get("sourcing") or {}
            check(sourcing.get("retrieval") == "unmeasured",
                  f"no turn count is unmeasured: {sourcing!r}")
            check(sourcing.get("recall_only") is False,
                  f"and unmeasured is not recall-only: {sourcing!r}")
            check((sourcing.get("tool_use") or {}).get("state") == "unmeasured",
                  f"the turn counter must say it saw nothing: {sourcing!r}")

            _status, page = request(f"{base}/api/v1/runs/{job_id}/report.html")
            text = page.decode("utf-8", "replace")
            check("Whether anything was retrieved is unmeasured." in text,
                  "the verdict must say unmeasured in words")
            check("whether the model retrieved anything is unmeasured" in text,
                  "and so must the provenance notes, which travel with every "
                  "artefact")
            check("Nothing was retrieved" not in text
                  and "retrieved nothing" not in text,
                  "and nothing may say it did not retrieve")


def test_the_cli_version_is_read_off_the_install_and_nothing_runs() -> None:
    """The version a `claude` route runs is read off the native installer's
    layout -- `bin/claude` a symlink to `versions/<version>` -- and served with
    the models it is too old for; nothing is started to find it out.

    Every fake `claude` here is a program that appends to a marker when run
    and prints its version, so a build that read the version by running
    `--version` would pass the figures and fail the marker. Must-fire: a store
    whose reader does run it leaves the marker, so the marker can see a start.
    """
    import subprocess
    with tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        marker = home / "started.log"

        def install(version: str) -> Path:
            target = home / "share" / "claude" / "versions" / version
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"#!/bin/sh\necho started >> {shlex.quote(str(marker))}\n"
                              f"echo '{version} (Claude Code)'\n", encoding="utf-8")
            os.chmod(target, 0o700)
            link = home / f"bin-{version}" / "claude"
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(target)
            return link

        old, new = install("2.1.274"), install("2.1.283")
        plain = home / "plain" / "claude"
        plain.parent.mkdir()
        plain.write_text(f"#!/bin/sh\necho started >> {shlex.quote(str(marker))}\n"
                         f"echo '2.1.274 (Claude Code)'\n", encoding="utf-8")
        os.chmod(plain, 0o700)

        def row(program: Path | str, model: str) -> dict:
            return {"label": f"{model} via {Path(str(program)).parent.name}",
                    "command": f"{shlex.quote(str(program))} --print --model {model}",
                    "window": 200000, "model": model, "web_tools": []}

        rows = {"old55": row(old, "claude-opus-5-5"), "new55": row(new, "claude-opus-5-5"),
                "oldalias": row(old, "opus"), "plain55": row(plain, "claude-opus-5-5"),
                "onpath": row("claude", "claude-opus-5-5")}
        path = home / "config" / "commands.json"
        path.parent.mkdir()
        path.write_text(json.dumps({"version": 1, "routes": rows}), encoding="utf-8")
        os.chmod(path, 0o600)
        store = commands.Commands(path, which=lambda name: str(old) if name == "claude" else None)
        served = {entry["id"]: entry for entry in store.describe()}
        too_old = [{"model": "claude-opus-5-5", "needs": "2.1.280"}]
        for rid, version, listed in (("old55", "2.1.274", too_old),
                                     ("new55", "2.1.283", []),
                                     ("oldalias", "2.1.274", too_old),
                                     ("plain55", None, []),
                                     ("onpath", "2.1.274", too_old)):
            got = served.get(rid, {})
            check(got.get("cli_version") == version,
                  f"{rid}: cli_version is {got.get('cli_version')!r}, want {version!r}")
            check(got.get("cli_too_old") == listed,
                  f"{rid}: cli_too_old is {got.get('cli_too_old')!r}, want {listed!r}")
        check(not any(str(home) in json.dumps(entry) for entry in served.values()),
              "a served route carries the path its version was read from")
        found = store.discovered()
        check(bool(found) and all(entry["version"] == "2.1.274" for entry in found
                                  if entry["tool"] == "claude"),
              f"discovery does not serve the found CLI's version: "
              f"{[entry.get('version') for entry in found]}")
        check(commands.MIN_CLI_VERSION == {("claude", "claude-opus-5-5"): "2.1.280"},
              "the minimum is the one the 2.1.274 refusal named")
        check(not marker.exists(), "reading a CLI's version started it")

        # Must-fire: the same store, reading by running it.
        def run_it(program: str) -> str:
            done = subprocess.run([program, "--version"], capture_output=True, text=True,
                                  check=False)
            return done.stdout.split()[0] if done.stdout.split() else ""

        running = commands.Commands(path, which=lambda name: str(old) if name == "claude"
                                    else None, version=run_it)
        check(any(entry.get("cli_too_old") for entry in running.describe()),
              "the seeded reader must still read a version")
        check(marker.exists(), "a reader that runs the program left no marker, so the "
              "check above could not have seen one")


def main() -> int:
    tests = [value for name, value in sorted(globals().items())
             if name.startswith("test_") and callable(value)]
    for test in tests:
        try:
            test()
        except Exception as exc:  # noqa: BLE001 - reported, not raised
            failures.append(f"{test.__name__} raised {type(exc).__name__}: {exc}")
    if failures:
        print(f"web commands: {len(failures)} of {len(tests)} test(s) failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web commands: {len(tests)} checks pass over the route allowlist, "
          f"PATH discovery, three seeded injection probes, an authorisation "
          f"refusal and three control runs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
