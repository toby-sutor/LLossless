#!/usr/bin/env python3
"""The credentials file and the bind token, driven over a real socket.

`src/llossless/web/credentials.py` covers the settings routes in
`api.py`, the `--host` flag and the token every non-loopback bind now costs.
Everything below that can be asked of a server is asked of a server: bound to
port 0, driven with `urllib.request`, and read back out of a real response
body. That is the rule this project arrived at the expensive way -- four
defects lived only on a command path while the functions underneath them tested
green -- and it applies with more force here than anywhere else in the package,
because the two failures this module is written against are both invisible from
inside the function that causes them. A key served in a response body is a
correct-looking 200. A token compared with `==` is a correct-looking 401.

No model calls and no merges. Nothing here submits a run, so there is no
scripted endpoint: the only sockets this module opens are the servers it binds
itself.

Five of the checks are worth naming, because each guards something that looks
true from the outside while being false:

**a non-loopback bind with no token refuses to start.** The single most
important check in the milestone. `llossless serve` shipped able to bind
loopback and nothing else, on the stated grounds that the server spends the
operator's API credit on every submitted document and nothing authenticated the
submitter; the flag that lifts that arrived in the same commit as the token,
and this is what says the two are actually tied together rather than merely
documented as being. Driven through `cli.main` as well as through
`server.build`, because a refusal that lives in the library and not on the
command is a refusal an operator never meets.

**a near-miss token is refused.** A comparison written with `startswith`, or
one that stops at the shorter of the two strings, passes any test whose wrong
token is a wholly different word. So the wrong tokens here are a prefix of the
right one, an extension of it, and a same-length string differing only in its
last character -- and the right one is required to still work, because a check
that refuses everything is not a check that authenticates anything.

**a seeded key reaches no response body, no log line and no exception text.**
Asserted against the literal, over every route this server answers, including
the refusals -- a path reaches a message by way of an exception, and so does
anything else that was in scope when one was raised. The key is seeded in the
file *and* in the environment, so both of the places it could be read from are
live while the assertion runs.

**a credentials file wider than 0600 is refused.** Must fire on the mode and
must not fire on the same file at 0600, so the refusal is about the mode rather
than about the file being unreadable for some other reason.

**the file this tool writes is 0600 inside a 0700 directory** -- checked on the
file it actually wrote, through the endpoint that writes it, rather than on a
`Credentials` object called directly.

Run with `python3 tests/test_web_credentials.py`, or collect with pytest.
"""

from __future__ import annotations

import contextlib
import http.server
import inspect
import io
import json
import os
import stat
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs. Every request below reaches a real
# loopback socket, so this is the module's claim that the only sockets it opens
# are the ones it bound itself; `tests/test_socket_guard.py` asserts every test
# module states it in exactly this shape.
socket_guard.install()

from llossless import cli, config  # noqa: E402
from llossless.web import api, catalogue, credentials, discover, server  # noqa: E402

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# scaffolding
# --------------------------------------------------------------------------

# Long enough that a loaded machine running the whole suite does not fail a
# check about a request, short enough that a genuine hang is reported as one
# rather than as a suite that never returns.
PATIENCE = 30.0

# The value that must never be served. Not address-shaped, not key-shaped, and
# not a word that occurs in any document under test, so no scanner in this
# repository has a reason to recognise it -- and a tail of its own, so that a
# leak found here cannot be confused with `tests/test_web_server.py`'s probe.
FAKE_KEY = "probe-key-must-never-be-served-7q4z"

# At least `credentials.MIN_TOKEN_LENGTH`, and obviously a probe. The near
# misses are derived from it rather than written out, so that editing it
# cannot leave a "wrong" token that is accidentally right.
TOKEN = "probe-token-0123456789abcdef"

# Which provider the key tests use. `anthropic` because it is a name
# `catalogue.json` also uses, so this module cannot pass on a provider the
# model picker has never heard of.
PROVIDER = "anthropic"
VARIABLE = credentials.PROVIDERS[PROVIDER]

# A name that is not a provider and is shaped like the thing an allowlist is
# for: it would be a path traversal the moment anybody built a filename out of
# it.
NOT_A_PROVIDER = "..%2f..%2fetc"

KEYS = f"{api.API_PREFIX}/settings/keys"

# The most bytes any response here is read for.
READ_CAP = 256 * 1024


@contextlib.contextmanager
def environment():
    """Restore `os.environ` afterwards, whatever the body did to it.

    The settings routes put keys into the process environment on purpose --
    that is how a key configured through the page reaches a run -- so a module
    that exercises them changes the environment of the interpreter running the
    suite. Snapshotted and put back rather than deleted key by key, because the
    thing being guarded is a variable this module never thought about.
    """
    before = dict(os.environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(before)


@contextlib.contextmanager
def live_server(*, host=None, token="", keys=None, work=None, log=None):
    """A serving `Server`. Yields it, and shuts it down whatever happened.

    Port 0, and the bound port is read back off the socket: two runs of the
    suite must not be able to collide on a port, and a developer running their
    own `llossless serve` must not be able to make this fail.

    `environ` carries no endpoint on purpose. Nothing here submits a run, so
    the settings this server would resolve for one are never read, and a
    scripted endpoint standing behind it would be a second thing that can fail
    in a module about credentials.
    """
    raw = tempfile.TemporaryDirectory() if work is None else None
    directory = Path(raw.name) if raw is not None else Path(work)
    built = server.build(host=server.HOST if host is None else host, port=0,
                         token=token, keys=keys,
                         work_dir=directory / "work", environ={},
                         log_stream=log)
    thread = server.background(built)
    try:
        yield built
    finally:
        built.shutdown()
        built.server_close()
        built.store.close()
        thread.join(timeout=5)
        if raw is not None:
            raw.cleanup()


def request(url: str, *, method: str = "GET", payload=None, headers=None,
            timeout: float = PATIENCE):
    """One HTTP call. Returns (status, headers, body-bytes). Never raises on 4xx.

    An `HTTPError` is a response with a body, and every refusal this module
    asserts about arrives as one; letting it propagate would turn every
    negative check into a `try`/`except` at the call site and make the
    interesting assertion the one in the handler.
    """
    body = None
    sent = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        sent.setdefault("Content-Type", "application/json")
    call = urllib.request.Request(url, data=body, method=method, headers=sent)
    try:
        with urllib.request.urlopen(call, timeout=timeout) as answer:
            return answer.status, dict(answer.headers), answer.read(READ_CAP)
    except urllib.error.HTTPError as refusal:
        return refusal.code, dict(refusal.headers), refusal.read(READ_CAP)


def as_json(body: bytes):
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None


def carries_key(text: str) -> str:
    """Whichever suffix of `FAKE_KEY` is present in `text`, or ``.

    Suffixes rather than the whole literal, because the one part of a key this
    server is allowed to serve is its last four characters. Asking only whether
    the whole key is present would pass a response that served all but the
    first character of it. Five is therefore the shortest tail that counts as a
    leak, and the longest present is reported so the failure says how much got
    out.
    """
    for length in range(len(FAKE_KEY), credentials.SUFFIX_LENGTH, -1):
        if FAKE_KEY[-length:] in text:
            return FAKE_KEY[-length:]
    return ""


def written(path: Path, keys: dict) -> Path:
    """A credentials file with `keys` in it, written the way the tool writes one."""
    store = credentials.Credentials(path)
    for name, value in keys.items():
        store.set(name, value)
    return path


# --------------------------------------------------------------------------
# the bind
# --------------------------------------------------------------------------

# The two spellings of "everything". `0.0.0.0` is the one an operator types and
# `""` is the one that matches no address pattern at all, which is why both are
# asked rather than one taken as standing for the other.
WILDCARDS = ("0.0.0.0", "")


def test_a_non_loopback_bind_without_a_token_refuses_to_start() -> None:
    """The check this milestone exists for. Must fire, then must not fire.

    Must fire: every non-loopback spelling, with no token and with a token too
    short to be one, raises before a socket is bound -- asserted by the absence
    of a `Server` rather than by a message, because a server that refused
    loudly and bound anyway would pass a check written against the text.

    Must not fire: the same address with a real token binds, answers, and
    reports the address it was asked for. Without that half this check would
    pass on a `build` that refused every address including the default.
    """
    for host in WILDCARDS:
        for token in ("", "   ", "short"):
            try:
                built = server.build(host=host, port=0, token=token,
                                     work_dir=None, environ={})
            except credentials.BindRefused as refusal:
                check(credentials.TOKEN_ENV in str(refusal),
                      f"the refusal for host={host!r} must name the variable "
                      f"that supplies the token; it says {str(refusal)[:120]!r}")
            except Exception as other:  # noqa: BLE001 - that is the defect
                check(False, f"host={host!r} token={token!r} raised "
                             f"{type(other).__name__} rather than BindRefused: "
                             f"{other}")
            else:
                # `server_close` and the store, and deliberately not
                # `shutdown()`. `BaseServer.shutdown` waits on an event that
                # only `serve_forever` sets, so calling it on a server that was
                # built and never served blocks for good -- which is what the
                # seeded probe for this very check does, turning a failure into
                # a hung suite. A hang is the one failure a test may not have.
                built.server_close()
                built.store.close()
                check(False, f"host={host!r} with token={token!r} bound "
                             f"{built.server_address}; a key-spending endpoint "
                             f"reached the network with nothing in front of it")

    # Must not fire. `0.0.0.0` is bound for as long as one request takes, and
    # it is bound with the token that makes it safe to -- which is the whole
    # proposition being checked.
    with live_server(host="0.0.0.0", token=TOKEN) as built:
        check(built.server_address[0] == "0.0.0.0",
              f"a token was supplied and the server bound "
              f"{built.server_address[0]!r} rather than the address asked for")
        status, _, _ = request(f"http://127.0.0.1:{built.port}{api.API_PREFIX}/health",
                               headers={credentials.TOKEN_HEADER: TOKEN})
        check(status == 200,
              f"a token-protected server must answer a request that carries "
              f"the token; it answered {status}")


def test_the_command_refuses_the_same_bind_and_says_why() -> None:
    """The command, not the function. Must fire on stderr and in the exit code.

    `cli.main(["serve", "--host", ...])` is the path an operator takes, and it
    is the path where a refusal either reaches them or does not. This project
    has four recorded defects that lived only on a command path, so the library
    check above is not taken as covering this one.

    Run on a thread and joined with a deadline, which is not caution: a
    `llossless serve` that stops refusing does not return at all -- it binds
    `0.0.0.0` and calls `serve_forever`. Called in line, the seeded probe for
    this check hangs the suite instead of failing it, and a hang is the one
    failure a test may not have. The thread is a daemon, so a process that
    gives up on it still exits.
    """
    out = io.StringIO()
    result: dict = {}

    def run() -> None:
        with contextlib.redirect_stderr(out):
            result["code"] = cli.main(["serve", "--host", "0.0.0.0", "--port",
                                       "0", "--retention", "0"])

    with tempfile.TemporaryDirectory() as raw, environment():
        os.environ.pop(credentials.TOKEN_ENV, None)
        # Pointed at a file that does not exist. `llossless serve` reads the
        # credentials file the operator's environment names, and this check
        # runs inside the interpreter running the suite -- so without this it
        # would load whatever real keys the developer has configured into the
        # process, for a check that has nothing to do with them.
        os.environ[credentials.PATH_ENV] = str(Path(raw) / "none.json")
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        thread.join(timeout=PATIENCE)
    text = out.getvalue()
    if thread.is_alive():
        check(False, "`llossless serve --host 0.0.0.0` with no token did not "
                     "return; it is serving, which is the thing it refuses")
        return
    check(result.get("code") == 2,
          f"`llossless serve --host 0.0.0.0` with no token must exit 2; it "
          f"exited {result.get('code')}")
    check(credentials.TOKEN_ENV in text,
          f"the refusal must tell the operator which variable to set; it said "
          f"{text[:200]!r}")
    check("serving" not in text,
          f"the command announced a server it was supposed to refuse: "
          f"{text[:200]!r}")


def test_loopback_with_no_token_still_serves() -> None:
    """The default experience, unchanged. Must not fire.

    The companion to the two above: a milestone that adds a refusal has to show
    that it did not also add one nobody asked for. Every route is asked,
    without a token, on the default address.
    """
    with live_server() as built:
        for path in ("/", f"{api.API_PREFIX}/health", f"{api.API_PREFIX}/config",
                     f"{api.API_PREFIX}/runs", KEYS):
            status, _, body = request(f"{built.url}{path}")
            check(status == 200,
                  f"loopback with no token must still serve {path}; it "
                  f"answered {status}: {body[:160]!r}")


def test_the_serve_defaults_and_the_token_variable_match_the_web_package() -> None:
    """The two values `cli.py` restates are required to still be the same two.

    `cli.build_parser` runs on every invocation, so it may not import
    `llossless.web` to read them -- the engine is required to work with the
    web package absent. Restating them is the cost; this is what stops the
    restated copy drifting from the real one, which would show up as a `--help`
    that names a variable the server does not read.
    """
    args = cli.build_parser().parse_args(["serve"])
    check(args.host == cli.SERVE_HOST == server.HOST,
          f"the host default differs: parser {args.host!r}, cli "
          f"{cli.SERVE_HOST!r}, web {server.HOST!r}")
    check(cli.SERVE_TOKEN_ENV == credentials.TOKEN_ENV,
          f"the token variable differs: cli {cli.SERVE_TOKEN_ENV!r}, web "
          f"{credentials.TOKEN_ENV!r}")
    offered = {spelling
               for action in cli.build_parser()._subparsers._group_actions[0]
               .choices["serve"]._actions
               for spelling in action.option_strings}
    check("--host" in offered,
          f"`llossless serve` no longer offers --host: {sorted(offered)}")


# --------------------------------------------------------------------------
# the token on a request
# --------------------------------------------------------------------------


def test_a_near_miss_token_is_refused_and_the_right_one_is_accepted() -> None:
    """Must fire on four wrong tokens, must not fire on the right one.

    Three of the four are near misses, and they are the reason this check is
    not one line. A comparison written with `startswith`, or one that stops at
    the shorter of two strings, refuses a wholly different word and accepts a
    prefix -- so a test whose only wrong token is `"wrong"` would pass over
    exactly the defect worth catching.
    """
    wrong = {
        "a prefix of the real token": TOKEN[:-1],
        "the real token with a character appended": TOKEN + "z",
        "the same length, last character changed": TOKEN[:-1] + "z",
        "a wholly different string": "not-the-token-at-all-0000",
        "no header at all": None,
    }
    with live_server(host="0.0.0.0", token=TOKEN) as built:
        url = f"http://127.0.0.1:{built.port}{api.API_PREFIX}/health"
        for what, value in wrong.items():
            headers = {} if value is None else {credentials.TOKEN_HEADER: value}
            status, _, body = request(url, headers=headers)
            check(status == 401,
                  f"{what} was answered {status}, not 401: {body[:200]!r}")
            check((as_json(body) or {}).get("error", {}).get("code") == "no_token",
                  f"{what} must be refused with the contract's own code; got "
                  f"{body[:200]!r}")
        # Must not fire.
        status, _, body = request(url, headers={credentials.TOKEN_HEADER: TOKEN})
        check(status == 200,
              f"the right token was refused with {status}: {body[:200]!r}. A "
              f"check that refuses everything authenticates nothing")


def test_the_token_header_under_the_old_name_is_ignored() -> None:
    """`X-LLossless-Token` only; the pre-rename header authenticates nothing.

    The code used to accept the old header as a fallback; the operator's fresh-start
    ruling removed it. The right token under the old name is refused as if no
    header were sent, alone and beside a wrong new one. Must fire: the same
    token under the new name is accepted.
    """
    check(credentials.TOKEN_HEADER == "X-LLossless-Token"
          and not hasattr(credentials, "LEGACY_TOKEN_HEADER"),
          f"one token header, {credentials.TOKEN_HEADER!r}, and no old one")
    cases = (
        ("the new header, right token", {"X-LLossless-Token": TOKEN}, 200),
        ("the old header, right token", {"X-Claimcheck-Token": TOKEN}, 401),
        ("a wrong new header beside a right old one",
         {"X-LLossless-Token": TOKEN + "z", "X-Claimcheck-Token": TOKEN}, 401),
        ("a right new header beside a wrong old one",
         {"X-LLossless-Token": TOKEN, "X-Claimcheck-Token": "wrong"}, 200),
    )
    with live_server(host="0.0.0.0", token=TOKEN) as built:
        url = f"http://127.0.0.1:{built.port}{api.API_PREFIX}/health"
        for what, headers, wanted in cases:
            status, _, body = request(url, headers=headers)
            check(status == wanted,
                  f"{what} was answered {status}, not {wanted}: {body[:160]!r}")


def test_the_token_reaches_every_api_route_including_the_stream() -> None:
    """One rule for both ways into the API. Must fire on both.

    `handle` is not the only way in: the event stream is answered by
    `server.py` directly and used to call `api.check_host` on its own. A token
    enforced on the routes and not on it would leave a run's whole progress log
    -- every step, every warning, every quoted fragment -- readable to anybody
    who could reach the port.

    **The page is no longer one of them**, and the exemption is new,
    not an erosion of an earlier one. That earlier ruling demanded the token on the page and
    recorded the cost in the same paragraph: a browser cannot put a custom
    header on a navigation, so a networked deployment needed a reverse proxy
    injecting one. It also named the fix -- a login endpoint setting an
    `HttpOnly` cookie -- and that endpoint now exists. A login form that cannot
    be fetched without being logged in is not a login form.

    So the sentence an auditor checks moved one layer in and got stronger:
    every route under `/api/v1/` but `session` and `setup` needs an identity,
    and `test_web_accounts.py` holds that against the whole routing table
    rather than against a list written here. What the page discloses on its
    own is asserted below, because "it is only a shell" is a claim with a
    truth value.
    """
    with live_server(host="0.0.0.0", token=TOKEN) as built:
        base = f"http://127.0.0.1:{built.port}"
        # A job id of the right shape that does not exist. The stream refuses
        # it either way; what is being asked is *which* refusal comes back.
        stream = f"{api.API_PREFIX}/runs/{'0' * 32}/events"
        for path in (stream, f"{api.API_PREFIX}/runs",
                     f"{api.API_PREFIX}/health", f"{api.API_PREFIX}/config"):
            status, _, body = request(f"{base}{path}")
            check(status == 401,
                  f"{path} answered {status} without a token; every way into "
                  f"this API carries the same rule: {body[:160]!r}")
        # Must not fire: the same two with the token. The stream's 404 is the
        # right answer for an id that does not exist and is the proof that the
        # request got past the token rather than being refused by it.
        header = {credentials.TOKEN_HEADER: TOKEN}
        check(request(f"{base}{stream}", headers=header)[0] == 404,
              "a stream for a job that does not exist must be a 404 once the "
              "token is accepted, not a 401")
        check(request(f"{base}{api.API_PREFIX}/runs", headers=header)[0] == 200,
              "the runs route must answer a request that carries the token")

        # The page is public, and what it is allowed to be is "a shell". Every
        # byte of state on it arrives through a route that is behind the check
        # above, so the served HTML must carry none of it: no key, no run id,
        # no endpoint, and no catalogue. Asserted rather than asserted-in-prose,
        # because "it discloses nothing" is exactly the claim that quietly
        # stops being true when somebody inlines a bootstrap payload.
        for path in ("/", "/index.html"):
            status, _, body = request(f"{base}{path}")
            check(status == 200,
                  f"{path} answered {status}; the login page has to be "
                  f"fetchable or there is no way to log in")
            page = body.decode("utf-8", "replace")
            check(not carries_key(page),
                  f"{path} carries part of a configured key")
            for leaked in (FAKE_KEY, TOKEN, "credentials.json", "accounts.json"):
                check(leaked not in page,
                      f"{path} carries {leaked!r}; the page is public and is "
                      f"allowed to be a shell and nothing else")


def test_the_comparison_is_constant_time_at_the_call_site() -> None:
    """The source, because the property is invisible in the answer.

    A token compared with `==` returns the right answer every time and leaks
    how many leading characters were right in the time it takes to say no.
    Nothing a test can observe over a loopback socket distinguishes the two, so
    this is asserted where the comparison is written -- against the shipped
    function's own source rather than against a copy of the expression, so that
    reverting the fix in `credentials.py` fails here.

    Seeded both ways: the detector is shown to accept the real function and to
    reject a rewritten one, because a source check nobody has watched fail is a
    source check that reads every function as correct.
    """
    def compares_in_constant_time(text: str) -> bool:
        return "hmac.compare_digest(" in text and "== expected" not in text

    real = inspect.getsource(credentials.token_matches)
    check(compares_in_constant_time(real),
          "credentials.token_matches no longer compares with "
          "hmac.compare_digest")
    naive = 'def token_matches(presented, expected):\n    return presented == expected\n'
    check(not compares_in_constant_time(naive),
          "the detector cannot see a token compared with ==, so its silence "
          "over the real function means nothing")
    check("token_matches" in inspect.getsource(api.check_token),
          "api.check_token no longer goes through credentials.token_matches, "
          "so the comparison above is not the one the server runs")


# --------------------------------------------------------------------------
# the file
# --------------------------------------------------------------------------


def test_a_credentials_file_wider_than_0600_is_refused() -> None:
    """Must fire on 0644, must not fire on 0600, and the same file for both.

    The same path, the same bytes, and only the mode changed between the two
    halves, so the refusal cannot be about the file being unreadable for any
    other reason. Asked twice over: of `Credentials` directly, and through the
    endpoint, because a refusal that lives in the library and never reaches a
    response is a refusal the operator never sees.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        path = written(Path(raw) / "credentials.json", {PROVIDER: FAKE_KEY})
        store = credentials.Credentials(path)
        check(store.read()[PROVIDER].key == FAKE_KEY,
              "the file this tool wrote cannot be read back at 0600")

        for mode in (0o644, 0o640, 0o604, 0o700):
            path.chmod(mode)
            try:
                store.read()
            except credentials.CredentialsError as refusal:
                check(f"{mode:04o}" in str(refusal),
                      f"the refusal must name the mode it found; it says "
                      f"{str(refusal)[:160]!r}")
                check(not carries_key(str(refusal)),
                      "the refusal quotes the key it refused to load")
            else:
                check(False, f"a credentials file at {mode:04o} was loaded; "
                             f"every account on the box has had the chance to "
                             f"read it")

        path.chmod(0o644)
        with live_server(keys=credentials.Credentials(path)) as built:
            status, _, body = request(f"{built.url}{KEYS}")
            check(status == 409,
                  f"a server whose credentials file is 0644 must say so when "
                  f"asked about its keys; it answered {status}")
            text = body.decode("utf-8")
            check("0644" in text,
                  f"the refusal served must name the mode: {text[:200]!r}")
            check(not carries_key(text),
                  f"the refusal served carries the key: {text[:200]!r}")
            # Must not fire: the same server, the same file, at 0600.
            path.chmod(0o600)
            check(request(f"{built.url}{KEYS}")[0] == 200,
                  "the same file at 0600 must be read, or the refusal above is "
                  "not about the mode")


def test_the_file_this_tool_writes_is_0600_inside_a_0700_directory() -> None:
    """Must fire on the real write path -- through the endpoint, not the class.

    The directory is created by this write, at a path that did not exist, so
    what is measured is what the tool makes rather than what a temporary
    directory happened to be. And the umask is widened for the duration: a
    check run under `umask 077` passes on a file whose mode nothing in this
    package ever set.
    """
    was = os.umask(0o000)
    try:
        with tempfile.TemporaryDirectory() as raw, environment():
            path = Path(raw) / "fresh" / "deeper" / "credentials.json"
            with live_server(keys=credentials.Credentials(path)) as built:
                status, _, body = request(f"{built.url}{KEYS}/{PROVIDER}",
                                          method="PUT", payload={"key": FAKE_KEY})
                check(status == 204,
                      f"PUT must answer 204 with no body; it answered {status} "
                      f"{body[:160]!r}")
                check(body == b"", f"PUT answered with a body: {body[:160]!r}")
            check(path.is_file(), f"nothing was written to {path}")
            if not path.is_file():
                return
            file_mode = stat.S_IMODE(path.stat().st_mode)
            dir_mode = stat.S_IMODE(path.parent.stat().st_mode)
            check(file_mode == credentials.FILE_MODE,
                  f"the credentials file is {file_mode:04o} under a permissive "
                  f"umask; it must be {credentials.FILE_MODE:04o} whatever the "
                  f"umask says")
            check(dir_mode == credentials.DIR_MODE,
                  f"the directory holding it is {dir_mode:04o}; a directory "
                  f"another account can write is a directory the file can be "
                  f"replaced in")
            check(not list(path.parent.glob(".*tmp*")),
                  f"the atomic write left its temporary behind: "
                  f"{sorted(p.name for p in path.parent.iterdir())}")
    finally:
        os.umask(was)


def test_an_unknown_provider_is_refused_and_never_becomes_a_path() -> None:
    """Must fire on four names, must not fire on the one in the allowlist.

    The names include the shape an allowlist is for -- something that would be
    a traversal the moment anybody built a filename from it -- and the
    assertion that matters as much as the status is that nothing appeared on
    disk next to the real file afterwards.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        path = Path(raw) / "credentials.json"
        with live_server(keys=credentials.Credentials(path)) as built:
            for name in (NOT_A_PROVIDER, "openai/gpt", "Anthropic", "self hosted"):
                # Percent-encoded where the character would not survive a
                # request line, and nowhere else: `%2f` is left as the client
                # wrote it, because a name that is already a traversal on the
                # wire is the one this allowlist exists for.
                wire = urllib.parse.quote(name, safe="%/")
                for method, payload in (("PUT", {"key": FAKE_KEY}),
                                        ("DELETE", None)):
                    status, _, body = request(f"{built.url}{KEYS}/{wire}",
                                              method=method, payload=payload)
                    check(status == 404,
                          f"{method} on provider {name!r} answered {status}; an "
                          f"unknown name is refused, never looked up: "
                          f"{body[:160]!r}")
                    check((as_json(body) or {}).get("error", {}).get("code")
                          in ("unknown_provider", "no_route"),
                          f"{method} on {name!r} must be refused by the "
                          f"contract's own code: {body[:200]!r}")
            # Must not fire: a name that is in the allowlist.
            check(request(f"{built.url}{KEYS}/{PROVIDER}", method="PUT",
                          payload={"key": FAKE_KEY})[0] == 204,
                  f"{PROVIDER} is a provider and must be settable, or the "
                  f"refusals above are refusing everything")
        wrote = sorted(p.name for p in Path(raw).iterdir())
        check(wrote == ["credentials.json"],
              f"a refused provider name reached the filesystem: {wrote}")


def test_a_provider_in_the_catalogue_is_a_provider_the_settings_page_knows() -> None:
    """Must fire. The two lists are required to agree, not merely to exist.

    `catalogue.json` names a provider per model and this module's allowlist
    names a variable per provider. A model whose provider has no row on the
    settings page is a model the operator can pick and cannot configure a key
    for, and nothing else in the suite compares the two files.
    """
    known = set(credentials.PROVIDERS)
    named = {model["provider"] for model in catalogue.models()}
    check(named <= known,
          f"catalogue.json names provider(s) the settings page cannot "
          f"configure a key for: {sorted(named - known)}")
    check(len(set(credentials.PROVIDERS.values())) == len(credentials.PROVIDERS),
          f"two providers share one environment variable, so deleting either "
          f"clears both: {sorted(credentials.PROVIDERS.items())}")


def test_a_stranger_in_the_file_is_counted_and_never_named_back() -> None:
    """Must fire. The one refusal whose message could itself be the key.

    The likeliest way a name this build does not recognise gets into the file
    is an operator editing it by hand and writing the name and the value the
    wrong way round -- in which case the name *is* a key, and `api.ApiError`
    puts an exception's message straight into a response body. So the refusal
    reports how many strangers it found and not what they were called. Seeded
    with the key itself as the provider name, which is exactly the shape of the
    accident.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        path = Path(raw) / "credentials.json"
        path.write_text(json.dumps({"version": credentials.SCHEMA_VERSION,
                                    "endpoints": {FAKE_KEY: {"key": "whatever-1234"}}}),
                        encoding="utf-8")
        path.chmod(credentials.FILE_MODE)
        store = credentials.Credentials(path)
        try:
            store.read()
        except credentials.CredentialsError as refusal:
            check(not carries_key(str(refusal)),
                  f"the refusal names the stranger, and the stranger is a key: "
                  f"{str(refusal)[:200]!r}")
            check("1" in str(refusal),
                  f"the refusal must say how many it found, since it may not "
                  f"say what they were: {str(refusal)[:200]!r}")
        else:
            check(False, "a name this build does not recognise was loaded out "
                         "of the credentials file")
        with live_server(keys=credentials.Credentials(path)) as built:
            status, _, body = request(f"{built.url}{KEYS}")
            check(status == 409,
                  f"a file with an unrecognised name must be refused over the "
                  f"wire too; got {status}")
            check(not carries_key(body.decode("utf-8")),
                  f"the refusal served carries the stranger's name, which is "
                  f"the key: {body[:200]!r}")


def test_a_key_that_is_not_one_is_refused_before_it_reaches_disk() -> None:
    """Must fire on five bodies, must not fire on a real one.

    The empty and the fragment are the two paste failures a length rule can
    actually catch; the line break is the one that would go out in a header.
    Every refusal is asserted not to quote what it refused, because the value
    it refused is a key.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        path = Path(raw) / "credentials.json"
        with live_server(keys=credentials.Credentials(path)) as built:
            url = f"{built.url}{KEYS}/{PROVIDER}"
            for what, payload in (
                    ("an empty key", {"key": ""}),
                    ("a fragment", {"key": "sk-ab"}),
                    ("a key with a line break", {"key": f"{FAKE_KEY}\nHost: x"}),
                    ("a key that is not a string", {"key": 12}),
                    ("no key field at all", {"nope": FAKE_KEY}),
                    ("a field the contract does not define",
                     {"key": FAKE_KEY, "variable": "X"})):
                status, _, body = request(url, method="PUT", payload=payload)
                # 400 exactly, and never the 409 `handle` turns a bad
                # credentials *file* into: the body was wrong, retrying with a
                # different one will work, and a client told 409 has been told
                # the opposite.
                check(status == 400,
                      f"{what} was answered {status}, not 400: {body[:160]!r}")
                check((as_json(body) or {}).get("error", {}).get("code")
                      in ("bad_key", "no_key", "unknown_field", "bad_json"),
                      f"{what} must be refused by one of the contract's own "
                      f"codes: {body[:200]!r}")
                check(not carries_key(body.decode("utf-8")),
                      f"the refusal of {what} quotes the key: {body[:200]!r}")
            check(not path.exists(),
                  f"a refused key reached disk at {path}")
            # Must not fire.
            check(request(url, method="PUT", payload={"key": FAKE_KEY})[0] == 204,
                  "a real key must be accepted, or the refusals above are "
                  "refusing everything")


# --------------------------------------------------------------------------
# what the settings routes say
# --------------------------------------------------------------------------


def test_the_keys_endpoint_reports_a_suffix_and_never_a_key() -> None:
    """The contract, field by field, with the key live in both places it could
    be read from.

    `suffix` is four characters and is absent rather than empty when nothing is
    configured, so a client has nothing to render when there is nothing to say.
    The assertion that it is *only* four characters is `carries_key`, which
    looks for every tail of the key longer than that.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        path = Path(raw) / "credentials.json"
        keys = credentials.Credentials(path)
        with live_server(keys=keys) as built:
            before = as_json(request(f"{built.url}{KEYS}")[2])
            rows = {row["name"]: row for row in before["providers"]}
            check(set(rows) == set(credentials.PROVIDERS),
                  f"the endpoint must answer for every provider; got "
                  f"{sorted(rows)}")
            for name, row in rows.items():
                check(row["variable"] == credentials.PROVIDERS[name],
                      f"{name}: the endpoint must name the variable it looked "
                      f"at; it says {row['variable']!r}")
                check(row["configured"] is False and "suffix" not in row,
                      f"{name}: nothing is configured and the row says "
                      f"{row}; suffix must be absent, never empty")

            status, _, _ = request(f"{built.url}{KEYS}/{PROVIDER}", method="PUT",
                                   payload={"key": FAKE_KEY})
            check(status == 204, f"the key was not accepted: {status}")

            status, _, body = request(f"{built.url}{KEYS}")
            payload = as_json(body)
            row = {r["name"]: r for r in payload["providers"]}[PROVIDER]
            check(row["configured"] is True,
                  f"a key was written and the endpoint reports {row}")
            check(row.get("suffix") == FAKE_KEY[-credentials.SUFFIX_LENGTH:],
                  f"the suffix must be the last "
                  f"{credentials.SUFFIX_LENGTH} characters; got "
                  f"{row.get('suffix')!r}")
            leaked = carries_key(body.decode("utf-8"))
            check(not leaked,
                  f"the keys endpoint served {len(leaked)} characters of the "
                  f"key, and four is the limit")

            # The key really is on disk and really is in the environment, so
            # the assertion above ran with something to find.
            check(keys.read()[PROVIDER].key == FAKE_KEY,
                  "the key was not written, so nothing above was tested")
            check(os.environ.get(VARIABLE) == FAKE_KEY,
                  f"a key set through the page must reach this process's "
                  f"environment under {VARIABLE}, or no run will ever use it")

            status, _, body = request(f"{built.url}{KEYS}/{PROVIDER}",
                                      method="DELETE")
            check(status == 204 and body == b"",
                  f"DELETE must answer 204 with no body; got {status} "
                  f"{body[:160]!r}")
            check(not any(row.key for row in keys.read().values()),
                  f"the key survived its deletion: {sorted(keys.read())}")
            check(VARIABLE not in os.environ,
                  f"{VARIABLE} survived the deletion, so the next run spends a "
                  f"key the operator revoked")
            # Idempotent, like `DELETE /runs/{id}`.
            check(request(f"{built.url}{KEYS}/{PROVIDER}", method="DELETE")[0] == 204,
                  "deleting a key that is already gone must still answer 204")


def test_a_key_the_environment_holds_and_the_file_does_not_reads_configured() -> None:
    """Must fire, and it is the reason this endpoint reads the environment.

    What an operator needs from this page is which credential the next run will
    *spend*, and that is whatever is in `os.environ` under the variable --
    exported by their shell, set by the unit that started the server, or put
    there by this file. An endpoint that answered only out of its own file
    would show `configured: false` beside a key that works, which is the sort
    of answer that gets a working deployment taken apart.

    Must not fire on the other half: the row still carries only four
    characters, whoever set it.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        path = Path(raw) / "credentials.json"
        os.environ[VARIABLE] = FAKE_KEY
        with live_server(keys=credentials.Credentials(path)) as built:
            status, _, body = request(f"{built.url}{KEYS}")
            row = {r["name"]: r for r in (as_json(body) or {})["providers"]}[PROVIDER]
            check(status == 200 and row["configured"] is True,
                  f"a key this server will spend is in the environment and the "
                  f"page reports {row}")
            check(row.get("suffix") == FAKE_KEY[-credentials.SUFFIX_LENGTH:],
                  f"the suffix must describe the value in effect; got "
                  f"{row.get('suffix')!r}")
            check(not carries_key(body.decode("utf-8")),
                  f"the endpoint served the key it found in the environment: "
                  f"{body[:200]!r}")
        check(not path.exists(),
              "reading the keys endpoint wrote a credentials file")


def test_deleting_one_key_leaves_a_variable_this_tool_never_set() -> None:
    """Must not fire. The narrow rule `_applied` exists for.

    A credentials manager that unset every variable it knows the name of would
    disarm a deployment whose key comes from the unit file the first time
    somebody pressed delete on an unrelated row. So a variable this object did
    not put in the environment is not one it takes out.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        ambient = credentials.PROVIDERS["openai"]
        os.environ[ambient] = FAKE_KEY
        path = Path(raw) / "credentials.json"
        with live_server(keys=credentials.Credentials(path)) as built:
            request(f"{built.url}{KEYS}/{PROVIDER}", method="PUT",
                    payload={"key": FAKE_KEY})
            request(f"{built.url}{KEYS}/{PROVIDER}", method="DELETE")
            check(os.environ.get(ambient) == FAKE_KEY,
                  f"deleting {PROVIDER}'s key cleared {ambient}, which this "
                  f"tool never set")
            # Must fire, on the same endpoint: the one it did set is gone.
            check(VARIABLE not in os.environ,
                  f"{VARIABLE} survived, so the check above proves nothing")


def test_the_wrong_method_on_a_settings_route_is_a_405() -> None:
    """A route that exists refuses the wrong verb rather than 404ing.

    404 tells a client the path is wrong and sends it looking for a typo, where
    the path was right and the method was not.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        with live_server(keys=credentials.Credentials(Path(raw) / "c.json")) as built:
            for method, path in (("PUT", KEYS), ("DELETE", KEYS),
                                 ("POST", KEYS), ("GET", f"{KEYS}/{PROVIDER}"),
                                 ("POST", f"{KEYS}/{PROVIDER}")):
                payload = {"key": FAKE_KEY} if method in ("PUT", "POST") else None
                status, _, body = request(f"{built.url}{path}", method=method,
                                          payload=payload)
                check(status == 405,
                      f"{method} {path} answered {status}, not 405: "
                      f"{body[:160]!r}")
            # Must not fire.
            check(request(f"{built.url}{KEYS}")[0] == 200,
                  "GET on the collection must still work")


def test_a_key_written_through_the_page_is_refused_without_json() -> None:
    """The content type is part of the CSRF defence, not a formality.

    A cross-origin form can send three content types and JSON is not one of
    them, so requiring it is the part of the defence that does not depend on a
    header the attacker controls. The same rule that guards a submit has to
    guard the route that writes a credential, which is the one worth stealing.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        path = Path(raw) / "credentials.json"
        with live_server(keys=credentials.Credentials(path)) as built:
            url = f"{built.url}{KEYS}/{PROVIDER}"
            status, _, body = request(
                url, method="PUT", payload={"key": FAKE_KEY},
                headers={"Content-Type": "application/x-www-form-urlencoded"})
            check(status == 415,
                  f"a PUT that is not JSON must be refused with 415; got "
                  f"{status}: {body[:160]!r}")
            status, _, body = request(
                url, method="PUT", payload={"key": FAKE_KEY},
                headers={"Origin": "http://attacker.example"})
            check(status == 403,
                  f"a PUT from another origin must be refused with 403; got "
                  f"{status}: {body[:160]!r}")
            check(not path.exists(),
                  "a refused cross-origin PUT wrote a key to disk")


# --------------------------------------------------------------------------
# the leak check
# --------------------------------------------------------------------------


def test_no_response_body_log_line_or_traceback_carries_the_key() -> None:
    """The must-not-fire that the whole module is arranged around.

    Seeded in the file and in the process environment at once, then looked for
    in the body of every route this server answers -- the refusals included,
    because a value reaches a message by way of an exception and an exception
    is raised with everything that was in scope. The access log and the
    server's own error stream are read too: a key that never reaches a client
    and does reach the operator's log is a key in a file somebody ships to a
    support ticket.

    `carries_key` is the detector and it is shown to work at the end, on a
    string that does carry the key -- a leak check nobody has watched fire is a
    leak check that reads every response as clean.
    """
    log = io.StringIO()
    errors = io.StringIO()
    with tempfile.TemporaryDirectory() as raw, environment():
        path = written(Path(raw) / "credentials.json", {PROVIDER: FAKE_KEY})
        os.environ[VARIABLE] = FAKE_KEY
        keys = credentials.Credentials(path)
        keys.apply()
        with contextlib.redirect_stderr(errors), \
                live_server(keys=keys, log=log) as built:
            asked = [
                ("GET", "/", None),
                ("GET", "/index.html", None),
                ("GET", "/nope.html", None),
                ("GET", f"{api.API_PREFIX}/health", None),
                ("GET", f"{api.API_PREFIX}/config", None),
                ("GET", f"{api.API_PREFIX}/runs", None),
                ("GET", f"{api.API_PREFIX}/runs/{'0' * 32}", None),
                ("GET", f"{api.API_PREFIX}/runs/not-an-id", None),
                ("GET", f"{api.API_PREFIX}/runs/{'0' * 32}/events", None),
                ("GET", f"{api.API_PREFIX}/nope", None),
                ("GET", KEYS, None),
                ("PUT", f"{KEYS}/{PROVIDER}", {"key": FAKE_KEY}),
                ("PUT", f"{KEYS}/{NOT_A_PROVIDER}", {"key": FAKE_KEY}),
                ("PUT", f"{KEYS}/{PROVIDER}", {"key": "x"}),
                ("PUT", f"{KEYS}/{PROVIDER}", {"nope": 1}),
                ("POST", f"{api.API_PREFIX}/runs", {"documents": []}),
                ("DELETE", f"{KEYS}/{PROVIDER}", None),
                ("DELETE", f"{api.API_PREFIX}/runs/{'0' * 32}", None),
            ]
            for method, path_, payload in asked:
                _, headers, body = request(f"{built.url}{path_}", method=method,
                                           payload=payload)
                leaked = carries_key(body.decode("utf-8", "replace"))
                check(not leaked,
                      f"{method} {path_} served {len(leaked)} characters of "
                      f"the key: {body[:200]!r}")
                leaked = carries_key(" ".join(f"{k}: {v}" for k, v in headers.items()))
                check(not leaked,
                      f"{method} {path_} put the key in a response header")

        check(not carries_key(log.getvalue()),
              f"the access log carries the key: {log.getvalue()[:200]!r}")
        check(not carries_key(errors.getvalue()),
              f"the server's error stream carries the key: "
              f"{errors.getvalue()[:400]!r}")
        check(log.getvalue().count("\n") >= len(asked),
              f"the access log holds {log.getvalue().count(chr(10))} lines for "
              f"{len(asked)} requests, so it was not being written and the "
              f"check above read an empty string")

        # The exception path, on the object that holds the key. `repr` reaches
        # a log line and a debugger without anybody deciding that it should.
        check(not carries_key(repr(keys)),
              f"repr(Credentials) carries the key: {repr(keys)}")
        try:
            credentials.Credentials(Path(raw) / "missing" / "x.json").set("nope", FAKE_KEY)
        except Exception as raised:  # noqa: BLE001 - the text is what is checked
            check(not carries_key(f"{raised!r} {raised}"),
                  f"an exception raised while setting a key carries it: "
                  f"{raised!r}")

    # Must fire. Everything above is a silence, and a detector that cannot say
    # yes makes every one of those silences worthless.
    check(carries_key(f"nothing to see: {FAKE_KEY} here") == FAKE_KEY,
          "the leak detector cannot see the key written in front of it")
    check(carries_key(f"tail {FAKE_KEY[-8:]}") == FAKE_KEY[-8:],
          "the leak detector only sees the whole key, so a response serving "
          "all but the first character of one would read as clean")
    check(carries_key(f"suffix {FAKE_KEY[-4:]}") == "",
          "the leak detector fires on the four characters this server is "
          "allowed to serve, which would make every keys response a failure")


def test_the_server_loads_the_file_into_its_own_environment_at_startup() -> None:
    """The command, end to end, with the file where the variable points.

    `Settings.api_key()` reads `os.environ` at send time, so a key that does
    not reach the process environment is a key no run will ever use -- and the
    settings page would be a page that says "saved" and changes nothing. Driven
    through `cli.main` because that is where the file is read from at all:
    `build` deliberately does not go looking for it.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        path = written(Path(raw) / "credentials.json", {PROVIDER: FAKE_KEY})
        os.environ[credentials.PATH_ENV] = str(path)
        os.environ.pop(VARIABLE, None)
        os.environ.pop(credentials.TOKEN_ENV, None)

        out = io.StringIO()
        result: dict = {}
        started = threading.Event()

        class Watch(io.StringIO):
            def write(self, text: str) -> int:
                written_ = out.write(text)
                if "serving http://" in out.getvalue():
                    started.set()
                return written_

        def run() -> None:
            with contextlib.redirect_stderr(Watch()):
                result["code"] = cli.main(["serve", "--port", "0",
                                           "--work-dir", str(Path(raw) / "w"),
                                           "--retention", "0"])

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        check(started.wait(timeout=PATIENCE),
              f"`llossless serve` never announced itself: "
              f"{out.getvalue()[:400]!r}")
        text = out.getvalue()
        check(str(path) in text,
              f"the banner must name the credentials file it read: "
              f"{text[:400]!r}")
        check(not carries_key(text),
              f"the banner carries the key: {text[:400]!r}")
        check(os.environ.get(VARIABLE) == FAKE_KEY,
              f"`llossless serve` did not load the credentials file into its "
              f"own environment; {VARIABLE} is {os.environ.get(VARIABLE)!r}")

        import ctypes  # noqa: PLC0415 - only this check interrupts a thread

        # Stop it the way a terminal does; `serve_forever` is inside `main`.
        deadline = time.monotonic() + PATIENCE
        while thread.is_alive() and time.monotonic() < deadline:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_ulong(thread.ident), ctypes.py_object(KeyboardInterrupt))
            thread.join(timeout=1.0)
        check(not thread.is_alive(), "`llossless serve` did not stop on an "
                                     "interrupt")
        check(result.get("code") == 0,
              f"an interrupted `llossless serve` exits 0; got "
              f"{result.get('code')}")


# --------------------------------------------------------------------------
# entry points
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# the endpoint, and the key it is paired with
# --------------------------------------------------------------------------

ENDPOINTS = f"{api.API_PREFIX}/settings/endpoints"


def test_moving_an_endpoint_clears_the_key_stored_against_it() -> None:
    """The binding, and it is structural rather than remembered. Must fire.

    Changing a provider's address does not carry its key across. Not because
    the next person to type an address is assumed hostile, but because moving
    an endpoint and leaving the previous provider's key attached sends a real
    credential to a host that was typed in thirty seconds ago.

    Asserted three ways, because "the setter remembers to clear it" is exactly
    the kind of rule that survives one refactor and not two: through the
    object, where `moved_to` is the only call that changes an address and
    returns a pair with no key; through the file, where the key is gone after a
    save; and through the route, where the operator does it.

    Must not fire: `with_key` keeps the address, and re-saving the key after
    the move puts it back. A binding that cleared the key on every write would
    pass the first half of this and be useless.
    """
    pair = credentials.Endpoint(base_url="https://one.example/v1", key=FAKE_KEY,
                                models=("m1",))
    moved = pair.moved_to("https://two.example/v1")
    check(moved.key == "" and moved.base_url == "https://two.example/v1",
          f"moving an endpoint kept something it should not: {moved!r}")
    check(moved.models == (),
          "the model listing survived the move; it is a fact about the old host")
    check(pair.with_key("another-key-1234").base_url == pair.base_url,
          "storing a key moved the address, which is the opposite rule")
    check(not any("base_url" in name for name in
                  dir(credentials.Endpoint) if not name.startswith("_")
                  and name not in ("base_url",)),
          "Endpoint grew a second way to change an address; moved_to must be "
          "the only one, or the clearing becomes a step somebody can skip")

    with tempfile.TemporaryDirectory() as raw, environment():
        path = Path(raw) / "credentials.json"
        store = credentials.Credentials(path)
        store.set_endpoint(PROVIDER, "https://one.example/v1")
        store.set(PROVIDER, FAKE_KEY)
        check(store.read()[PROVIDER].key == FAKE_KEY,
              "the key was not stored, so the clearing below tests nothing")
        store.set_endpoint(PROVIDER, "https://two.example/v1")
        check(store.read()[PROVIDER].key == "",
              "the key survived a change of endpoint on disk")
        check(store.read()[PROVIDER].base_url == "https://two.example/v1",
              "the endpoint was not stored")
        check(FAKE_KEY not in path.read_text(encoding="utf-8"),
              "the cleared key is still in the file")

    with tempfile.TemporaryDirectory() as raw, environment():
        path = Path(raw) / "credentials.json"
        keys = credentials.Credentials(path)
        with live_server(keys=keys) as built:
            base = f"{built.url}{ENDPOINTS}/{PROVIDER}"
            status, _, _ = request(base, method="PUT",
                                   payload={"base_url": "https://one.example/v1"})
            check(status == 200, f"saving an endpoint answered {status}")
            status, _, _ = request(f"{built.url}{KEYS}/{PROVIDER}", method="PUT",
                                   payload={"key": FAKE_KEY})
            check(status == 204, f"saving a key answered {status}")
            check(os.environ.get(VARIABLE) == FAKE_KEY,
                  "the key did not reach the environment, so the clearing "
                  "below would pass on a key that was never there")

            status, _, _ = request(base, method="PUT",
                                   payload={"base_url": "https://two.example/v1"})
            check(status == 200, f"moving the endpoint answered {status}")
            check(keys.read()[PROVIDER].key == "",
                  "the key survived a change of endpoint through the route")
            check(VARIABLE not in os.environ,
                  f"{VARIABLE} survived in the environment, so the next run "
                  f"sends the old key to the new address")
            check(os.environ.get(credentials.url_env(PROVIDER))
                  == "https://two.example/v1",
                  "the new address did not reach the environment the jobs "
                  "resolve against")


def test_a_version_one_file_is_read_rather_than_refused() -> None:
    """The shape that predates per-provider endpoints. Must fire, and must not.

    Version 1 held `{"keys": {provider: key}}` and no address anywhere: there
    was one endpoint, the server's own. That is not a broken pair, it is a pair
    whose address has not been set yet, so it is migrated rather than refused
    -- refusing would start a server with no credentials at all over a file
    that is perfectly intelligible, and the operator would find out by watching
    a run fail on a key they can see in the file.

    Must not fire: a version this build has never seen is still refused, so
    the migration is not a licence to read anything.
    """
    with tempfile.TemporaryDirectory() as raw, environment():
        path = Path(raw) / "credentials.json"
        path.write_text(json.dumps({"version": 1, "keys": {PROVIDER: FAKE_KEY}}),
                        encoding="utf-8")
        path.chmod(credentials.FILE_MODE)
        store = credentials.Credentials(path)
        rows = store.read()
        check(rows[PROVIDER].key == FAKE_KEY,
              f"a version 1 file was not migrated: {rows}")
        check(rows[PROVIDER].base_url == "",
              "a version 1 entry came back claiming an address it never had")

        # And writing it puts the file at the current version, with the key
        # intact and no address invented for it.
        store.set(PROVIDER, FAKE_KEY)
        written = json.loads(path.read_text(encoding="utf-8"))
        check(written["version"] == credentials.SCHEMA_VERSION,
              f"the file was not upgraded on write: {written.get('version')}")
        check(written["endpoints"][PROVIDER]["base_url"] == "",
              f"an address was invented for a migrated key: {written}")

        path.write_text(json.dumps({"version": 99, "keys": {}}), encoding="utf-8")
        path.chmod(credentials.FILE_MODE)
        try:
            credentials.Credentials(path).read()
            check(False, "a schema version this build has never seen was read "
                         "anyway; the migration is not a licence to guess")
        except credentials.CredentialsError:
            pass


def test_a_configured_endpoint_is_checked_by_both_of_config_s_guards() -> None:
    """`check_base_url` and `check_cleartext_key`, on a per-provider address.

    Both are `config`'s own and neither is reimplemented here: a second set of
    transport rules maintained on the settings page is a second set to keep in
    step, and the settings page is not where anybody looks when they change one.

    Must fire on each, separately, so a single refusal cannot stand in for
    both. Must not fire on an https address with the same key set, and on the
    loopback http default, which is what local ollama is and must keep working.
    """
    with environment():
        os.environ.pop(VARIABLE, None)
        for bad in ("file:///etc/passwd", "ftp://host/v1", "//host/v1"):
            try:
                credentials.clean_base_url(PROVIDER, bad)
                check(False, f"{bad!r} was accepted as an endpoint; urllib would "
                             f"read it as a local resource")
            except credentials.CredentialsError:
                pass
        check(credentials.clean_base_url(PROVIDER, "http://localhost:11434")
              == "http://localhost:11434",
              "the local ollama default was refused with no key set")

        os.environ[VARIABLE] = FAKE_KEY
        try:
            credentials.clean_base_url(PROVIDER, "http://a-rented-box.example:8000/v1")
            check(False, "a cleartext endpoint off this machine was accepted "
                         "while a key for that provider is set; the token goes "
                         "on the wire once per call")
        except credentials.CredentialsError as refusal:
            check(VARIABLE in str(refusal),
                  f"the refusal does not name the variable: {refusal}")
            check(FAKE_KEY not in str(refusal),
                  "the refusal quotes the key it refused to send")
        check(credentials.clean_base_url(PROVIDER, "https://a-rented-box.example:8000/v1")
              == "https://a-rented-box.example:8000/v1",
              "the https form of the same address was refused, so the check is "
              "refusing the host rather than the scheme")
        check(credentials.clean_base_url(PROVIDER, "http://127.0.0.1:11434/v1")
              == "http://127.0.0.1:11434/v1",
              "a loopback http endpoint was refused with a key set; that is "
              "the local default and takes no key")

        for bad in ("https://user:tok@host/v1", "https://tok@host/v1"):
            try:
                credentials.clean_base_url(PROVIDER, bad)
                check(False, f"{bad!r} was accepted; a credential written into "
                             f"an address travels wherever the address is shown")
            except credentials.CredentialsError:
                pass


def test_the_guards_run_on_every_endpoint_a_run_can_reach() -> None:
    """Not only the run-wide one. Must fire per role.

    `Settings` has carried a role-to-URL map since per-role endpoints landed,
    and both guards read `base_url` alone -- so an address configured for one
    role walked past the check written to stop exactly that. The job layer now
    writes those variables itself, which makes the gap reachable from a web
    request rather than only from a shell.
    """
    with environment():
        os.environ.pop(VARIABLE, None)
        for role in config.ROLES:
            settings = config.from_env({
                "LLOSSLESS_BASE_URL": "http://localhost:11434/v1",
                f"LLOSSLESS_BASE_URL_{role.upper()}": "file:///etc/passwd"})
            try:
                config.check_base_url(settings)
                check(False, f"a file:// endpoint on the {role} role was "
                             f"accepted; its bytes would be parsed as an answer")
            except config.ConfigError as refusal:
                check(role in str(refusal),
                      f"the refusal does not say which role: {refusal}")

            os.environ[VARIABLE] = FAKE_KEY
            settings = config.from_env({
                "LLOSSLESS_BASE_URL": "http://localhost:11434/v1",
                f"LLOSSLESS_BASE_URL_{role.upper()}": "http://a-box.example/v1",
                f"LLOSSLESS_API_KEY_ENV_{role.upper()}": VARIABLE})
            try:
                config.check_cleartext_key(settings)
                check(False, f"a cleartext endpoint on the {role} role was "
                             f"accepted while {VARIABLE} is set")
            except config.ConfigError as refusal:
                check(VARIABLE in str(refusal),
                      f"the refusal does not name the variable: {refusal}")
            os.environ.pop(VARIABLE, None)

        # Must not fire: the ordinary single-endpoint run, and a split across
        # two loopback endpoints, both pass.
        config.check_base_url(config.from_env({}))
        config.check_cleartext_key(config.from_env({}))
        config.check_base_url(config.from_env({
            "LLOSSLESS_BASE_URL": "http://localhost:11434/v1",
            "LLOSSLESS_BASE_URL_MERGE": "http://127.0.0.1:8000/v1"}))


def test_saving_an_endpoint_asks_it_what_it_serves() -> None:
    """The probe, against a real listing server on loopback. Must fire both ways.

    Two shapes are tried, the OpenAI-compatible listing and ollama's, because
    there is no way to tell which an address speaks from the address. What
    comes back is stored against the endpoint and served to the picker as
    `measured: null` rows -- nobody has benchmarked them here, so no figure is
    estimated for them.

    Must not fire: an endpoint that answers neither is stored anyway, with a
    sentence saying it would not list. A probe that could block a configuration
    would turn a convenience into a requirement.
    """
    for shape, payload in (("openai", {"data": [{"id": "qwen3:8b"},
                                                {"id": "gemma3:12b"}]}),
                           ("ollama", {"models": [{"name": "qwen3:8b"}]})):
        with listing_server(shape, payload) as address, \
                tempfile.TemporaryDirectory() as raw, environment():
            keys = credentials.Credentials(Path(raw) / "credentials.json")
            with live_server(keys=keys) as built:
                status, _, body = request(f"{built.url}{ENDPOINTS}/{PROVIDER}",
                                          method="PUT",
                                          payload={"base_url": address + "/v1"})
                answer = as_json(body)
                check(status == 200, f"{shape}: saving answered {status}")
                check(answer.get("listed") is True,
                      f"{shape}: the endpoint was not listed: {answer}")
                check("qwen3:8b" in (answer.get("models") or []),
                      f"{shape}: the listing is missing what the endpoint "
                      f"serves: {answer}")
                check(list(keys.read()[PROVIDER].models)[:1] == ["qwen3:8b"],
                      f"{shape}: the listing was not stored against the "
                      f"endpoint: {keys.read()[PROVIDER]!r}")

                _, _, config_body = request(f"{built.url}{api.API_PREFIX}/config")
                served = as_json(config_body)["endpoints"]["providers"]
                row = next(entry for entry in served if entry["name"] == PROVIDER)
                check("qwen3:8b" in row["models"],
                      f"{shape}: /config does not offer what the endpoint listed")

                # And into the environment a job resolves against, beside the
                # address, because a discovered model has no catalogue row to
                # read a provider off: without this it goes to whichever
                # endpoint the server was started with, which is the defect
                # this whole arrangement exists to remove.
                exported = (os.environ.get(credentials.models_env(PROVIDER)) or "")
                check("qwen3:8b" in exported.split("\n"),
                      f"{shape}: the listing did not reach the environment "
                      f"under {credentials.models_env(PROVIDER)}: {exported!r}")
                check(credentials.provider_serving("qwen3:8b", os.environ) == PROVIDER,
                      f"{shape}: a discovered model does not resolve back to "
                      f"the provider whose endpoint listed it")
                check(credentials.provider_serving("nothing-listed-this", os.environ)
                      is None,
                      f"{shape}: a name nothing listed resolved to a provider "
                      f"anyway, so a typed model id would be routed by guess")

    with listing_server("silent", None) as address, \
            tempfile.TemporaryDirectory() as raw, environment():
        keys = credentials.Credentials(Path(raw) / "credentials.json")
        with live_server(keys=keys) as built:
            status, _, body = request(f"{built.url}{ENDPOINTS}/{PROVIDER}",
                                      method="PUT",
                                      payload={"base_url": address + "/v1"})
            answer = as_json(body)
            check(status == 200,
                  f"an endpoint that would not list was refused with {status}")
            check(answer.get("listed") is False and answer.get("models") == [],
                  f"a silent endpoint reported a listing: {answer}")
            check("could not list" in (answer.get("note") or ""),
                  f"the note does not say the listing failed: {answer}")
            check(keys.read()[PROVIDER].base_url == address + "/v1",
                  "an endpoint that would not list was not stored")


# --------------------------------------------------------------------------
# the well-known addresses
# --------------------------------------------------------------------------

# The addresses this repository's own vendor runs used, written out here as a
# registration, independent of the table they check: a table edited to a new
# address fails this until the edit is deliberate here too.
# (found at these lines in these files):
#   anthropic  arms/2026-09-25/vendor/run_api.py
#   openai     arms/2026-09-25/vendor/run_api.py
#   google     arms/2026-09-25/google/run_api.py
WELL_KNOWN = {
    "anthropic": "https://api.anthropic.com/v1",
    "google": "https://generativelanguage.googleapis.com/v1beta/openai",
    "openai": "https://api.openai.com/v1",
}


@contextlib.contextmanager
def patched(owner, name: str, value):
    """`owner.name` replaced for the body only: one seeded break at a time."""
    before = getattr(owner, name)
    setattr(owner, name, value)
    try:
        yield
    finally:
        setattr(owner, name, before)


@contextlib.contextmanager
def no_probe():
    """Saving an endpoint asks it what it serves; here nothing is asked.

    The addresses below are the vendors' real ones, and a probe would be a
    real request (and a DNS lookup) off this machine. The socket guard would
    refuse the connection, but the lookup would already have left.
    """
    asked: list[str] = []

    def stub(base_url, *, api_key=None, ca_bundle=None):
        asked.append(base_url)
        return [], "not asked: a test"
    with patched(discover, "models", stub):
        yield asked


def served_rows(built) -> dict:
    status, _, body = request(f"{built.url}{KEYS}")
    payload = as_json(body) or {}
    return {row["name"]: row for row in payload.get("providers", [])} if status == 200 else {}


def preset_problems(built) -> list[str]:
    rows = served_rows(built)
    found = []
    for name in credentials.PROVIDERS:
        row = rows.get(name) or {}
        if row.get("preset_url", None) != WELL_KNOWN.get(name, ""):
            found.append(f"{name} offers {row.get('preset_url')!r}")
    if rows.get("self-hosted", {}).get("example_url") != config.DEFAULT_BASE_URL:
        found.append("the self-hosted row has no example address")
    return found


def test_the_well_known_addresses_are_served_and_match_the_table() -> None:
    """Must not fire as shipped; must fire when the table drifts or is not served."""
    check(credentials.PRESET_URLS == WELL_KNOWN,
          f"the preset table is {credentials.PRESET_URLS}, the registered "
          f"addresses are {WELL_KNOWN}")
    for name, url in credentials.PRESET_URLS.items():
        with environment():
            check(credentials.clean_base_url(name, url) == url,
                  f"{name}'s preset would not be stored as written: {url}")
        check(config.with_api_path(url) == url,
              f"{name}'s preset would have a path appended at run time")
    check("self-hosted" not in credentials.PRESET_URLS,
          "self-hosted has a preset; its address is wherever the operator's box is")
    with tempfile.TemporaryDirectory() as raw, environment():
        keys = credentials.Credentials(Path(raw) / "credentials.json")
        with live_server(keys=keys) as built:
            problems = preset_problems(built)
            check(not problems, f"presets as served: {problems}")
            # An offer and nothing else: with no address stored, every row
            # still says it has none.
            for name, row in served_rows(built).items():
                check(row.get("base_url") == "" and row.get("endpoint_configured") is False,
                      f"{name} reports an address nobody stored: {row}")
            with patched(credentials, "PRESET_URLS",
                         {**WELL_KNOWN, "openai": "https://elsewhere.invalid/v1"}):
                check(bool(preset_problems(built)),
                      "must fire: a drifted table passed the registration")
            with patched(credentials, "PRESET_URLS", {}):
                check(bool(preset_problems(built)),
                      "must fire: presets that are not served passed")


def test_a_prefilled_save_stores_the_explicit_address() -> None:
    """The page saves the offered address as a value; nothing resolves it later."""
    with tempfile.TemporaryDirectory() as raw, environment(), no_probe() as asked:
        path = Path(raw) / "credentials.json"
        keys = credentials.Credentials(path)
        with live_server(keys=keys) as built:
            preset = credentials.PRESET_URLS["openai"]
            status, _, body = request(f"{built.url}{ENDPOINTS}/openai", method="PUT",
                                      payload={"base_url": preset})
            check(status == 200, f"saving the offered address answered {status} {body[:160]!r}")
            status, _, _ = request(f"{built.url}{KEYS}/openai", method="PUT",
                                   payload={"key": FAKE_KEY})
            check(status == 204, f"saving the key answered {status}")
            stored = json.loads(path.read_text(encoding="utf-8"))["endpoints"]["openai"]
            check(stored["base_url"] == preset and stored["key"] == FAKE_KEY,
                  f"the file does not hold the explicit address and its key: "
                  f"{ {**stored, 'key': '<set>' if stored.get('key') else ''} }")
            check(asked == [preset], f"the listing probe was asked {asked}")
            # The table moving later moves nothing that is stored.
            with patched(credentials, "PRESET_URLS",
                         {**WELL_KNOWN, "openai": "https://elsewhere.invalid/v1"}):
                row = served_rows(built)["openai"]
                check(row["base_url"] == preset and keys.read()["openai"].base_url == preset,
                      f"a changed table moved a stored address: {row['base_url']}")
                check(os.environ.get(credentials.url_env("openai")) == preset,
                      "a changed table moved the address runs resolve against")
            # A key saved with no address stored is not sent to the preset:
            # the row stays without an address and the provider unconfigured.
            status, _, _ = request(f"{built.url}{KEYS}/google", method="PUT",
                                   payload={"key": FAKE_KEY})
            check(status == 204, f"a key with no address answered {status}")
            check(keys.read()["google"].base_url == ""
                  and not os.environ.get(credentials.url_env("google")),
                  "a key saved with no address was given the preset one")


def test_an_existing_endpoint_is_not_rewritten() -> None:
    """The operator's typed address survives a server with presets, byte for byte."""
    typed = "https://proxy.example/openai/v1"
    with tempfile.TemporaryDirectory() as raw, environment(), no_probe():
        path = Path(raw) / "credentials.json"
        keys = credentials.Credentials(path)
        keys.set_endpoint("openai", typed)
        keys.set("openai", FAKE_KEY)
        before = path.read_bytes()
        env: dict = {}
        keys.apply(env)
        for _ in range(2):  # and again after a restart
            with live_server(keys=keys) as built:
                row = served_rows(built)["openai"]
                check(row["preset_url"] == WELL_KNOWN["openai"],
                      "must not fire: the preset is not offered beside a stored address")
                check(path.read_bytes() == before,
                      "serving the rows rewrote the credentials file")
        check(keys.read()["openai"].base_url == typed and keys.read()["openai"].key == FAKE_KEY,
              "the typed address or its key changed")


def test_a_changed_address_keeps_the_key_binding() -> None:
    """Moving from the offered address clears its key. Must fire; must not fire."""
    def scenario() -> list[str]:
        found = []
        with tempfile.TemporaryDirectory() as raw, environment(), no_probe():
            keys = credentials.Credentials(Path(raw) / "credentials.json")
            with live_server(keys=keys) as built:
                base = f"{built.url}{ENDPOINTS}/anthropic"
                request(base, method="PUT",
                        payload={"base_url": credentials.PRESET_URLS["anthropic"]})
                request(f"{built.url}{KEYS}/anthropic", method="PUT",
                        payload={"key": FAKE_KEY})
                if keys.read()["anthropic"].key != FAKE_KEY:
                    found.append("the key was not bound to the offered address")
                request(base, method="PUT", payload={"base_url": "https://proxy.example/v1"})
                if keys.read()["anthropic"].key:
                    found.append("the key travelled to the new address")
                if os.environ.get(VARIABLE):
                    found.append("the key stayed in the environment runs read")
                # Must not fire: a key saved after the move is bound to it.
                request(f"{built.url}{KEYS}/anthropic", method="PUT",
                        payload={"key": "another-probe-key-5k1"})
                row = keys.read()["anthropic"]
                if row.base_url != "https://proxy.example/v1" or row.key != "another-probe-key-5k1":
                    found.append("a key saved after the move is not bound to the new address")
        return found
    problems = scenario()
    check(not problems, f"the binding: {problems}")
    keeping = lambda self, base_url: credentials.Endpoint(  # noqa: E731
        base_url=base_url, key=self.key, models=())
    with patched(credentials.Endpoint, "moved_to", keeping):
        check(any("travelled" in p for p in scenario()),
              "must fire: a move that keeps the key passed")


def page_save_order_problems(js: str) -> list[str]:
    """The key's Save sends the address on screen first, then the key."""
    start = js.index("  save.addEventListener(\"click\", async () => {")
    body = js[start:js.index("\n  });", start)]
    endpoint = body.find("ROUTES.endpoint")
    key = body.find("ROUTES.key")
    if endpoint < 0 or key < 0:
        return ["the key's Save no longer saves the address it shows"]
    if not endpoint < key:
        return ["the key is sent before the address it belongs to"]
    if "sameAddress(shown" not in body:
        return ["the key's Save does not compare the address shown with the one stored"]
    return []


def test_the_page_saves_the_address_on_screen_before_the_key() -> None:
    app = (ROOT / "src" / "llossless" / "web" / "static" / "app.js").read_text(encoding="utf-8")
    check(not page_save_order_problems(app), f"{page_save_order_problems(app)}")
    seeded = app.replace(
        "      if (shown && !sameAddress(shown, String(provider.base_url || \"\"))) {\n"
        "        await sendJson(\"PUT\", route(ROUTES.endpoint, { name: String(provider.name) }),\n"
        "                       { base_url: shown });\n"
        "      }\n", "", 1)
    check(seeded != app and bool(page_save_order_problems(seeded)),
          "must fire: a Save that sends the key alone passed")
    check("https://" not in app.split("function providerRow", 1)[1].split("\n}\n", 1)[0],
          "the provider row writes an address of its own; the server serves them")


@contextlib.contextmanager
def listing_server(shape: str, payload):
    """A loopback HTTP server that answers one model-listing shape and 404s the rest.

    Bound here rather than scripted through `fake_endpoint`, because what is
    being exercised is a GET of a status route rather than a completion, and
    the point of the `silent` shape is a server that answers *neither* listing.
    """
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802 - the base class names it
            wanted = {"openai": "/v1/models", "ollama": "/api/tags"}.get(shape)
            if wanted is None or self.path != wanted:
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):  # noqa: D102 - silence, this is a fixture
            return

    httpd = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_address[1]}"
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


def test_web_credentials_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    """Every check, and a check that raises is one failure rather than all of them.

    The exception is caught and recorded instead of propagating, which is not
    the usual arrangement in this suite and is earned here by how this module
    is verified. Every detector in it was shown to work by seeding the break it
    is written against into the shipped code, and several of those breaks make
    an *earlier* check raise -- a credentials file that stops being refused
    makes a later `read()` succeed where this module expected it to fail, and
    so on. Propagating would abort the module at the first one, so a single
    seeded defect would report one failure and leave sixteen detectors
    unexercised, which is indistinguishable from sixteen detectors that do not
    work.
    """
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_credentials_offline" \
                and callable(function):
            try:
                function()
            except Exception as raised:  # noqa: BLE001 - see the docstring
                failures.append(f"{name} raised "
                                f"{type(raised).__name__}: {raised}")
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web credentials: {checks} checks pass over "
          f"{len(credentials.PROVIDERS)} providers, the bind token and the "
          f"{KEYS} contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
