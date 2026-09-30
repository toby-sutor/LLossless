"""The HTTP plumbing. Loopback by default; anything wider costs an account or a token.

`api.py` decides what a request means; this reads bytes off a socket, hands them
over, and writes the answer back. Nothing in here knows what a fidelity level is
and nothing in `api.py` knows what a socket is, which is what lets the contract
be tested as function calls and the transport be tested by driving a real
server -- both of which `tests/test_web_server.py` does, because this project
has four recorded defects that lived only on a command path while the functions
underneath them tested green.

**The bind address is settable, and every address but loopback needs an account
or a token** -- the token only while the server has no account, which
`credentials.require_token` decides. `HOST` below is still `127.0.0.1` and the
default. The flag arrived in the same commit as the token rather than before
it: the server spends the operator's API
credit on every submitted document, and a version of this file where one flag
makes a key-spending endpoint reachable from the network with nothing in front
of it would be a version somebody deploys. `credentials.require_token` is
therefore called by `build` *before* the socket exists, and it raises rather
than warning -- a server that binds first and checks its configuration second
was, for however long that took, the thing this refuses to be.

**The body is refused by its declared length, before it is read.** A `POST` with
no `Content-Length` is refused outright: this server does not accept chunked
uploads, which removes both the "declare a small length and send a large body"
case and the need to count bytes while reading. The limit itself belongs to the
contract (`api.MAX_BODY_BYTES`) rather than here, because a second
implementation has to refuse at the same size to be the same API.

**Every response says `nosniff`, `deny` and a content type.** The static
directory is where the frontend will land, and a page served from the same
origin as this API can read every one of its responses; the headers are the part
of that arrangement that does not depend on what the frontend writes. `Content-Security-
Policy` is set to allow only what a self-contained page needs, because the one
artefact this server hands out that is already a whole HTML document -- the
report -- is built from a model's output, and `html_report` escaping it
correctly and a policy refusing to execute it are two independent defences
rather than one restated.

**A streamed response is written by hand rather than through `send_response`.**
SSE has no content length, so the connection is closed at the end of the stream
and the browser reconnects with `Last-Event-ID`; `close_connection` is set
explicitly for that. The alternative -- chunked transfer encoding -- would keep
the connection alive and add a framing layer between the frames this project
already tests, for no gain on a link that is always loopback.
"""

from __future__ import annotations

import re
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .. import __version__, config
from . import api
from .commands import Commands, CommandsError, NoCommands
from .accounts import Accounts, AccountError, Directory, Sessions, Setup
from .credentials import (TOKEN_ENV, TOKEN_HEADER, BindRefused, Credentials,
                          CredentialsError, is_loopback, require_token,
                          token_from)
from .jobs import (DEFAULT_RETENTION_SECONDS, DEFAULT_WORKERS,
                   FROM_ENVIRONMENT, IndexUnreadable, JobStore, WorkDirBusy,
                   retention_from)

# The default, and the only address that can be bound without a token. See the
# docstring, and `credentials.require_token` for what the other ones cost.
HOST = "127.0.0.1"

# Chosen high, unprivileged and unremarkable. 0 is honoured and is what the
# suite binds, so that two runs of the tests cannot collide on a port and a
# developer's own server cannot make the suite fail.
DEFAULT_PORT = 8765

# Where the operator's uploads live until retention deletes them. Under the
# cache directory because that is already the one place this tool is entitled
# to write on both an installed system and a checkout (`config.py:154`), and
# because everything in here genuinely is scratch: `JobStore` chmods it 0700
# and deletes each job's directory once the retention window passes.
DEFAULT_WORK_DIR = config.CACHE_DIR / "web"

# The frontend lands here. Served rather than proxied because the whole point
# of a self-hosted UI is that it is one process with no build step in front of
# it, and because a page served from a different origin than the API would need
# CORS -- which is a permission this server has no reason to grant to anybody.
STATIC_DIR = Path(__file__).resolve().parent / "static"
INDEX = "index.html"

# What a static path segment may contain. An allowlist rather than a check for
# `..`, because the list of things that mean "go up" is longer than it looks
# once percent-encoding, backslashes and unicode separators are counted, and a
# denylist has to be right about all of them. This has to be right about one.
STATIC_SEGMENT = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._-]*\Z")

# Only what a page is made of. An extension this map does not carry is not
# served at all -- a directory that will be edited by hand should not be able
# to start serving `.py` or `.pem` because somebody dropped one in it.
STATIC_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/vnd.microsoft.icon",
    ".woff2": "font/woff2",
}

# On every response. `nosniff` because a document this server did not write --
# a merged document served as markdown -- must not be re-typed as HTML by a
# browser guessing. `DENY` because nothing here is meant to be framed, and a
# framed local UI is the click-jacking case. `no-referrer` because a report
# page's URL contains a job id and a link out of it would hand that id to a
# third party. The CSP allows a page to style and script itself from this
# origin and to talk to this origin, and forbids every remote fetch -- the
# report is a self-contained page by design and has never needed one.
SECURITY_HEADERS = (
    ("X-Content-Type-Options", "nosniff"),
    ("X-Frame-Options", "DENY"),
    ("Referrer-Policy", "no-referrer"),
    ("Content-Security-Policy",
     "default-src 'none'; base-uri 'none'; form-action 'none'; "
     "frame-ancestors 'none'; img-src 'self' data:; style-src 'self' "
     "'unsafe-inline'; script-src 'self'; connect-src 'self'; font-src 'self'"),
)

# How an oversized body is got rid of. `DRAIN_CHUNK` is what is held in memory
# at once while discarding it -- the number that makes refusing cheap -- and
# `DRAIN_LIMIT` is the point past which even reading and throwing away is more
# work than hanging up. See `Handler._oversize`.
DRAIN_CHUNK = 64 * 1024
DRAIN_LIMIT = 64 * 1024 * 1024

# How long a quiet stream waits before sending a comment frame. Short enough
# that an intermediary with a thirty-second idle timeout never fires, long
# enough that a run producing nothing costs four wakeups a minute.
KEEPALIVE_SECONDS = 15.0


class Handler(BaseHTTPRequestHandler):
    """One request. Reads, delegates, writes. Decides nothing about the contract."""

    # HTTP/1.1 so that a browser keeps one connection for the page and its API
    # calls. Every response therefore carries a `Content-Length` or closes the
    # connection itself; `_stream` does the second.
    protocol_version = "HTTP/1.1"
    server_version = f"LLossless/{__version__}"
    # The Python version, withheld. It is the one part of the default
    # `Server:` header that tells a reader something about the host rather than
    # about the tool, and a version number is the first thing anybody matches
    # an advisory against.
    sys_version = ""

    # -- methods ---------------------------------------------------------

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's naming
        path = urlsplit(self.path).path
        if self._is_event_stream(path):
            self._stream(path)
            return
        if path.startswith(api.API_PREFIX):
            self._respond(self.server.api.handle("GET", path, headers=self.headers))
            return
        self._static(path)

    def do_POST(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        body = self._body()
        if body is None:
            return
        self._respond(self.server.api.handle("POST", path, body=body,
                                             headers=self.headers))

    def do_PUT(self) -> None:  # noqa: N802
        """A body-carrying replacement. The settings routes, and nothing else.

        Written out beside `do_POST` rather than aliased to it, because the two
        are not the same request even where the plumbing is: `handle` routes on
        the method, and a `PUT` that arrived here labelled `POST` would answer
        405 on a route that takes it and 202 on one that does not.
        """
        path = urlsplit(self.path).path
        body = self._body()
        if body is None:
            return
        self._respond(self.server.api.handle("PUT", path, body=body,
                                             headers=self.headers))

    def do_DELETE(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        self._respond(self.server.api.handle("DELETE", path, headers=self.headers))

    def do_HEAD(self) -> None:  # noqa: N802
        """The same answer with no body. Answered rather than 501.

        A supervisor checking whether the port is alive uses HEAD, and a 501
        from a health check reads as a server that is down.
        """
        path = urlsplit(self.path).path
        if self._is_event_stream(path):
            self.send_error(405, "a stream is not fetchable with HEAD")
            return
        response = (self.server.api.handle("GET", path, headers=self.headers)
                    if path.startswith(api.API_PREFIX) else self._static_response(path))
        self._respond(response, body=False)

    # -- reading ---------------------------------------------------------

    def _body(self) -> bytes | None:
        """The request body, or None once a refusal has already been written.

        Refused by the declared length before a byte is read, which is the only
        point at which refusing is cheaper than accepting. A request with no
        declared length is refused too: this server takes no chunked uploads,
        so there is no shape in which a body arrives whose size was not stated
        up front, and nothing here ever finds out mid-read that it is holding
        more than it agreed to.
        """
        raw = self.headers.get("Content-Length")
        if raw is None:
            self._refuse(411, "length_required",
                         "a submitted body must declare its Content-Length; "
                         "this server does not accept chunked uploads.")
            return None
        try:
            length = int(raw)
        except (TypeError, ValueError):
            self._refuse(400, "bad_length", f"Content-Length {raw!r} is not a number.")
            return None
        if length < 0:
            self._refuse(400, "bad_length", "Content-Length may not be negative.")
            return None
        try:
            api.check_body_size(length)
        except api.ApiError as refusal:
            self._oversize(length, refusal)
            return None
        return self.rfile.read(length)

    def _oversize(self, length: int, refusal: api.ApiError) -> None:
        """Answer 413 without ever holding the body, and without a reset.

        The refusal happens on the declared length, so nothing oversized is
        read into memory -- that is the whole point of checking `Content-Length`
        first. But a server that answers and then hangs up while the client is
        still writing gives that client a connection reset, and a reset is
        indistinguishable from a crash: the operator sees "the server died on
        my upload" rather than "the server told you it was too big". So the
        body is *drained* in fixed-size chunks and discarded -- bounded memory,
        which is what was being protected, rather than bounded bytes, which was
        never the risk on a loopback socket.

        Past `DRAIN_LIMIT` even draining is refused, and the client does get a
        reset. Reading a gigabyte in order to be polite about refusing it is
        the denial of service arriving by a different door.
        """
        if length <= DRAIN_LIMIT:
            remaining = length
            while remaining > 0:
                chunk = self.rfile.read(min(DRAIN_CHUNK, remaining))
                if not chunk:
                    break
                remaining -= len(chunk)
        self.close_connection = True
        self._respond(refusal.response(extra=self.server.api.extra_roots))

    # -- writing ---------------------------------------------------------

    def _respond(self, response: api.Response, *, body: bool = True) -> None:
        self.send_response(response.status)
        self.send_header("Content-Type", response.content_type)
        self.send_header("Content-Length", str(len(response.body)))
        for name, value in self._headers(response.headers):
            self.send_header(name, value)
        self.end_headers()
        if body and response.body:
            self.wfile.write(response.body)

    @staticmethod
    def _headers(own) -> list[tuple[str, str]]:
        """The default security headers, with a response's own **replacing** them.

        Replacing and not joining, and the distinction is the whole reason this
        is a function. A browser given two `Content-Security-Policy` headers
        enforces the intersection, so a route that needs a *different* policy --
        the HTML report, which carries an inline script and is served in a
        sandbox of its own (`api.REPORT_CSP`) -- would have the server's own
        policy applied on top and its script blocked anyway. The failure is
        silent: the page renders, and only its filter box stops working.
        """
        merged = {name.lower(): (name, value) for name, value in SECURITY_HEADERS}
        for name, value in own:
            merged[name.lower()] = (name, value)
        return list(merged.values())

    def _refuse(self, status: int, code: str, message: str) -> None:
        self._respond(api.ApiError(status, code, message).response(
            extra=self.server.api.extra_roots))

    # -- the stream ------------------------------------------------------

    @staticmethod
    def _is_event_stream(path: str) -> bool:
        parts = path.split("/")
        return (path.startswith(api.API_PREFIX) and len(parts) == 6
                and parts[-1] == "events" and parts[-3] == "runs")

    def _stream(self, path: str) -> None:
        """Server-Sent Events, written frame by frame until the log closes.

        The refusals still go through the contract: an id that is not an id and
        a job that does not exist are a 400 and a 404 here exactly as they are
        on every other route, and a stream endpoint that answered those by
        opening a stream and immediately closing it would make a typo
        indistinguishable from a finished run.

        `ConnectionError` is swallowed. A browser navigating away closes the
        connection mid-frame, which is the ordinary end of every stream this
        server will ever write, and a traceback per page-close is noise that
        trains an operator to ignore the log.
        """
        job_id = path.split("/")[-2]
        try:
            # The identity, and then the job behind it. Both, on this path,
            # because `handle` is not in front of it: a stream authenticated
            # but not owner-checked would hand a run's whole progress log --
            # every step, every warning, every quoted fragment -- to anybody
            # with the id, which is the one place a job id most easily leaks.
            who = self.server.api.check_access(
                self.headers, ("runs", job_id, "events"))
            stream = self.server.api.stream(
                job_id, who=who,
                last_event_id=self.headers.get("Last-Event-ID"),
                keepalive=self.server.keepalive)
        except api.ApiError as refusal:
            self._respond(refusal.response(extra=self.server.api.extra_roots))
            return

        # No `Content-Length`, so the connection has to close at the end of the
        # stream for the client to know it ended.
        self.close_connection = True
        self.send_response(200)
        for name, value in (*SECURITY_HEADERS, *stream.headers):
            self.send_header(name, value)
        self.send_header("Connection", "close")
        self.end_headers()
        try:
            for chunk in stream.chunks:
                self.wfile.write(chunk.encode("utf-8"))
                self.wfile.flush()
        except (ConnectionError, BrokenPipeError):
            return

    # -- static ----------------------------------------------------------

    def _static(self, path: str) -> None:
        """The page, behind the transport guard and nothing else. It is public.

        **This is the one exemption in the package, and it is the answer to an
        open question an earlier decision left.** It demanded the token on the page
        itself, and said why: "every request carries the token" is a sentence
        an auditor can check and "every request except the ones that do not" is
        not. It also recorded the cost -- a browser cannot put a custom header
        on a navigation, so an operator who bound a network address and typed
        the URL got a 401 for the page -- and named the fix: "a login endpoint
        setting an `HttpOnly` cookie would make a bare `--host` deployment
        usable without a proxy."

        That endpoint now exists, and a login form that cannot be fetched
        without being logged in is not a login form. So the auditable sentence
        moves one layer in and gets stronger rather than weaker: **no route
        under `/api/v1/` but `session` and `setup` answers without an
        identity**, and those two are an allowlist of tuples in `api.py` rather
        than a prefix anything can be added under.

        What is served here is a shell. Every byte of state on the page --
        the catalogue, the limits, the endpoints, the runs, the reports --
        arrives through a route that is behind `check_access`, so a stranger
        who fetches this gets the same HTML the project publishes.

        `check_transport` still runs, so a loopback-bound server still refuses
        a `Host` that is not loopback. The rebinding case is answered twice
        over here: a rebound page carries no session cookie, because a cookie
        is scoped to the host it was set for and the attacker's name is not
        that host.
        """
        try:
            self.server.api.check_transport(self.headers)
        except api.ApiError as refusal:
            self._respond(refusal.response(extra=self.server.api.extra_roots))
            return
        self._respond(self._static_response(path))

    def _static_response(self, path: str) -> api.Response:
        """A file from `static/`, by an allowlisted name, or a 404.

        Two independent checks, and the second is not redundant with the first.
        The segment allowlist means no request can *name* a path that leaves
        the directory; resolving and re-checking containment means no
        **symlink** inside the directory can take a request out of it either,
        which is a property of the filesystem rather than of the request and is
        therefore invisible to any amount of string validation.
        """
        wanted = path[1:] or INDEX
        if wanted.endswith("/"):
            wanted += INDEX
        segments = wanted.split("/")
        if not all(STATIC_SEGMENT.match(segment) for segment in segments):
            return api.ApiError(404, "not_found", f"{path} is not served.").response()
        target = STATIC_DIR / Path(*segments)
        content_type = STATIC_TYPES.get(target.suffix.lower())
        if content_type is None:
            return api.ApiError(404, "not_found",
                                f"{path} is not a kind of file this server "
                                f"hands out.").response()
        try:
            resolved = target.resolve(strict=True)
            resolved.relative_to(STATIC_DIR.resolve())
            payload = resolved.read_bytes()
        except (OSError, ValueError):
            return api.ApiError(404, "not_found", f"{path} is not served.").response()
        return api.Response(200, payload, content_type=content_type)

    # -- noise -----------------------------------------------------------

    def log_message(self, fmt: str, *args) -> None:
        """One line per request on the server's own stream, or none.

        Routed through the server rather than to `sys.stderr` directly so that
        a caller which wants silence gets it without reassigning a global. The
        line carries the path, which carries a job id -- that is the operator's
        own log on the operator's own machine, and an access log that hid which
        run a request was for would be unusable for the one thing it is for.
        """
        stream = getattr(self.server, "log_stream", None)
        if stream is None:
            return
        print(f"{self.address_string()} {fmt % args}", file=stream, flush=True)


class Server(ThreadingHTTPServer):
    """A threading server that owns the API, the job store and the log stream.

    `daemon_threads` so a `Ctrl-C` does not wait for an open SSE connection: a
    stream is held for as long as the browser is on the page, and a shutdown
    that joined those would hang until the operator closed a tab. The merge
    itself is not on one of these threads -- it is on a `JobStore` worker -- so
    nothing that is mid-model-call is killed by this.

    `allow_reuse_address` is **off**, which is the opposite of the usual
    default and is deliberate. Reuse exists so a restart does not fail on a
    socket in `TIME_WAIT`; the cost is that a second instance started by
    mistake binds silently beside the first on some platforms and the operator
    ends up with two servers, one of which holds the jobs and neither of which
    says so. A restart that has to wait a moment is the better failure.
    """

    daemon_threads = True
    allow_reuse_address = False

    def __init__(self, port: int, job_store, *, host: str = HOST, token: str = "",
                 keys=None, accounts=None, directory=None, sessions=None,
                 setup=None, log_stream=None,
                 keepalive: float = KEEPALIVE_SECONDS, catalogue_path=None) -> None:
        self.store = job_store
        self.host = host
        self.api = api.Api(job_store, catalogue_path=catalogue_path,
                           token=token, keys=keys, accounts=accounts,
                           directory=directory, sessions=sessions, setup=setup,
                           # The bind, handed over rather than guessed at. It
                           # is what decides whether the `Host` header is
                           # checked -- see `Api.check_transport` -- and this
                           # is the only object that knows it.
                           bind=host)
        self.log_stream = log_stream
        self.keepalive = keepalive
        # The only bind in this package, and there is exactly one expression
        # that can be its host. `tests/test_web_server.py` greps this file for
        # any other, because a constant is only a guarantee for as long as it
        # is the thing that is used -- and `build` is the only caller that
        # supplies `host`, having put it past `require_token` first.
        super().__init__((self.host, port), Handler)

    @property
    def port(self) -> int:
        """The port actually bound, which is the only useful answer when 0 was asked for."""
        return self.server_address[1]

    @property
    def url(self) -> str:
        """A URL a client can paste. Bracketed when the address is IPv6.

        `http://::1:8765` is not a URL -- the colons in the address run into
        the one before the port -- so an operator copying the banner of an
        IPv6 deployment would get a string nothing can dial, and would
        reasonably read that as the server having bound the wrong thing.
        """
        shown = f"[{self.host}]" if ":" in self.host else self.host
        return f"http://{shown}:{self.port}"


def build(*, host: str = HOST, port: int = DEFAULT_PORT, token: str = "",
          keys=None, accounts=None, sessions=None, setup=None, commands=None,
          work_dir=None,
          workers: int = DEFAULT_WORKERS,
          retention_seconds: float | None = DEFAULT_RETENTION_SECONDS,
          environ=None, log_stream=None, catalogue_path=None) -> Server:
    """A started job store behind a bound, not-yet-serving server.

    Split from `serve` so that a caller which needs the port before anything is
    served -- the suite, binding 0 -- can have it. The store is started here
    because a server that accepted a submit before its workers existed would
    queue work nothing was going to take.

    **The token is checked before anything else happens here.** Not after the
    store is up and not after the socket is bound: `require_token` raises
    `BindRefused` on the first line, so a non-loopback address with no token
    never reaches a `bind` call at all. The ordering is the check -- a server
    that binds and then validates has already been the thing it was refusing
    to be, for as long as the validation took.

    `token` and `keys` are arguments rather than read from the environment
    here, and `serve` supplies both from it. That keeps this function
    answerable for exactly what it was passed: a suite that binds a hundred
    servers on loopback must not start demanding a header because the
    developer happens to have exported `LLOSSLESS_WEB_TOKEN`, and it must not
    read, let alone load, the operator's real credentials file.

    `keys` is handed on and not read. Loading it into the environment is
    `serve`'s, because a credentials file that cannot be read is a thing the
    operator has to be *told* about rather than a reason for there to be no
    server, and deciding that is a decision about the command.

    **`accounts=None` means this server has no accounts**, which is a
    configuration and not a missing value: it is the single-tenant server,
    everybody who gets past the token is the same person, and every job belongs
    to everybody. It is what a library caller embedding this gets unless it
    asks for more, and it is what the suite binds a hundred of. `serve` -- the
    command an operator actually runs -- always supplies a store, so the mode
    with no identity in it is not reachable from the command line;
    `tests/test_web_accounts.py` asserts that rather than leaving it to
    whoever edits `serve` next.

    The bind rule follows from it. With no accounts, it stands in full: an
    address that is not loopback costs a token. With at least one, logging in
    *is* that authentication and no token is wanted -- see
    `credentials.require_token`, which is where the count is read.
    """
    keys = Credentials() if keys is None else keys
    # **`commands=None` means this server has no command routes**, and unlike
    # `keys` above it does not fall back to the operator's file. The asymmetry
    # is the point: a credentials file holds keys for endpoints this server
    # talks to, and a commands file names *programs this server executes*. A
    # capability that runs a program is switched on deliberately by the command
    # an operator types, never inherited by a library caller that did not ask
    # and never by the hundred servers the suite binds. `serve` supplies the
    # real store; everything else gets an empty one.
    commands = NoCommands() if commands is None else commands
    # **Here rather than in `serve`, so the path an operator runs and the path
    # a check binds are the same path.** `Commands.migrate` retires the routes
    # the earlier version of the credentials sheet wrote: `discovered`, a
    # tool id, no model. That change turned working rows into rows that
    # refuse. It touches nothing else and it is silent on a file it cannot
    # read; `serve` reads `commands.retired` afterwards and says what went.
    commands.migrate()
    directory = Directory(keys, accounts=accounts)
    token = require_token(host, token,
                          accounts=0 if accounts is None else accounts.count())
    store = JobStore(DEFAULT_WORK_DIR if work_dir is None else work_dir,
                     workers=workers, retention_seconds=retention_seconds,
                     environ=environ, directory=directory, routes=commands)
    try:
        server = Server(port, store, host=host, token=token, keys=keys,
                        accounts=accounts, directory=directory,
                        sessions=sessions, setup=setup,
                        log_stream=log_stream, catalogue_path=catalogue_path)
    except BaseException:
        # A port already in use is the ordinary case here -- after a crash it
        # is in TIME_WAIT for up to a minute -- and the store is given up
        # without its workers ever having started. Started first, as it used to be
        # ordered, a restart that then failed to bind ran the queue it had
        # just reloaded and died under it, which the next start reported as
        # interrupted: a run billed and lost by a bind error. Found by
        # killing a real server and restarting it on the same port.
        store.close()
        raise
    # After the bind, so the only process that runs this queue is one that is
    # serving it.
    store.start()
    return server


def serve(*, host: str = HOST, port: int = DEFAULT_PORT, work_dir=None,
          workers: int = DEFAULT_WORKERS,
          retention_seconds=FROM_ENVIRONMENT,
          environ=None, token=None, credentials_path=None, accounts_path=None,
          commands_path=None, stream=None) -> int:
    """Run until interrupted. The whole of what `llossless serve` does.

    Returns an exit code rather than raising or calling `sys.exit`, matching
    `cli.main`, so that the command line has one place where a process's exit
    status is decided.

    This is where the environment is read, and `build` is where it is not.
    `LLOSSLESS_WEB_TOKEN`, `LLOSSLESS_RETENTION` and the credentials file are
    the operator's configuration of *this command*, and a `build` that went
    looking for them
    itself would be a `build` that behaves differently in a suite than in a
    deployment.

    A refused bind exits 2, the same as a port already in use, and for the
    same reason: in both cases there is no server, the operator asked for
    something this machine will not give them, and the line above the exit
    code says which.

    The banner names the address, says what the retention window is, and says
    whether anything authenticates a request. All three are promises the
    operator is making to whoever hands them a document, and none is visible
    from the page.

    **This command always has an account store, and that is the difference
    between it and `build`.** A server nobody has an account on answers one
    route -- the one that creates the first account -- and prints a one-time
    address carrying a `secrets` token to reach it with. A default password was
    the alternative and is not one: the password that has not been changed yet
    is the one a scanner finds, and it would have to be documented, which means
    published.

    The token rides in the URL's **fragment**, which is not sent to any server.
    So it does not reach this server's own access log, an intermediary's, or a
    `Referer` on the way out, and the page can still read it and post it.

    **The retention window has three sources and they are ranked: the flag,
    then `LLOSSLESS_RETENTION`, then the default.** `FROM_ENVIRONMENT` is what
    a caller that did not choose passes, and it is a sentinel rather than
    `None` because `None` is already the opt-out -- see `jobs.retention_from`.
    A caller that did choose is obeyed and the environment is not consulted,
    which is what makes a flag on the command line beat a variable inherited
    from whatever started this process.
    """
    out = sys.stderr if stream is None else stream
    if retention_seconds is FROM_ENVIRONMENT:
        try:
            retention_seconds = retention_from()
        except ValueError as bad:
            # Before anything is built or bound. An unreadable window is not a
            # server that starts with the default: the default is longer than
            # almost anything an operator types, so guessing would keep their
            # documents beyond the life they asked for and the banner would
            # report a number nobody chose.
            print(f"llossless serve: {bad}", file=out)
            return 2
    keys = Credentials(credentials_path)
    accounts = Accounts(accounts_path)
    # The command routes, read from the operator's own file. This is the only
    # place in the package that constructs a store over a real path: `build`
    # defaults to an empty one, because running a program is a capability that
    # belongs to the command an operator types rather than to a library import.
    command_routes = Commands(commands_path)
    setup = Setup()
    try:
        registered = accounts.count()
    except AccountError as refusal:
        # Unusable, so there are no accounts as far as this server is
        # concerned -- which puts it in setup, refusing everything, rather
        # than open. Not fatal for the same reason the credentials file is
        # not: the operator is the only person who can act on it and a server
        # that would not start is a server they cannot read the message from.
        print(f"llossless serve: {refusal}", file=out)
        registered = 0
    try:
        # At start, and again after every change (`Api._reload_keys`). Before
        # `build`, because `JobStore` copies the environment once at
        # construction and a copy taken first would be a copy with no keys in
        # it -- `/health` would then report a credential this server does hold
        # as missing.
        keys.apply()
    except CredentialsError as refusal:
        # Not fatal, and not silent. The file is unusable, so the keys in it
        # are not loaded and the run will fail on a missing credential rather
        # than on a mystery; but a server that refused to start would take out
        # a deployment whose keys are in the environment already and whose
        # file is merely a leftover.
        print(f"llossless serve: {refusal}", file=out)
        print("llossless serve: no key from that file is loaded.", file=out)
    # Before the count, because it changes it. `build` runs the same call and
    # finds nothing left to do; this one is here so the banner below reports
    # the file as it will be served rather than as it was found.
    for gone in command_routes.migrate():
        print(f"llossless serve: the route {gone!r} was written by an "
              f"earlier version of this tool and did not state a model, so "
              f"it has been retired.", file=out)
        print("llossless serve: switch the model you want on in the "
              "credentials sheet; nothing you wrote by hand was touched.",
              file=out)
    try:
        routes_configured = len(command_routes.read())
        # One line per row the file holds and this build cannot use. Not fatal
        # and not a reason to drop the rest: the rows beside it are offered,
        # which is the whole of what changed here.
        for bad in command_routes.problems():
            print(f"llossless serve: {bad.reason}", file=out)
            print(f"llossless serve: the route {bad.name!r} is not offered; "
                  f"every other route in that file is.", file=out)
    except CommandsError as refusal:
        # Not fatal, and not silent, for the reason the credentials file is
        # not: the operator is the only person who can act on it, and a server
        # that refused to start is a server they cannot read the message from.
        # This is the *file* now rather than a row in it -- a mode, a parse, a
        # version -- so every route really is refused and the failure is a
        # picker with no command rows rather than a command chosen wrong.
        print(f"llossless serve: {refusal}", file=out)
        print("llossless serve: no command route from that file is offered.",
              file=out)
        routes_configured = 0
    configured_token = token_from() if token is None else token
    try:
        server = build(host=host, port=port,
                       token=configured_token,
                       keys=keys, accounts=accounts, setup=setup,
                       commands=command_routes,
                       work_dir=work_dir, workers=workers,
                       retention_seconds=retention_seconds, environ=environ,
                       log_stream=out)
    except BindRefused as refusal:
        print(f"llossless serve: {refusal}", file=out)
        return 2
    except (IndexUnreadable, WorkDirBusy) as refusal:
        # Refused rather than started empty: see `IndexUnreadable`. The
        # message says what moving the file aside would delete, because that
        # is the operator's decision to make and not this command's. A second
        # server on a work directory another one owns is refused the same way
        # and before anything in it is read.
        print(f"llossless serve: {refusal}", file=out)
        return 2
    except OSError as exc:
        print(f"llossless serve: cannot listen on {host}:{port}: {exc}", file=out)
        return 2
    window = ("kept until deleted, across restarts" if retention_seconds is None
              else f"deleted {int(retention_seconds)}s after a run finishes")
    # The port actually bound, not the one asked for (0 asks for any), and an
    # IPv6 address bracketed as in `server.url`.
    where = f"[{host}]:{server.port}" if ":" in host else f"{host}:{server.port}"
    if registered:
        reach = (f"anything that can reach {where}; every request must be "
                 f"signed in")
    elif server.api.token:
        reach = (f"anything that can reach {where}; every request must carry "
                 f"{TOKEN_HEADER} until the first account exists")
    elif is_loopback(host):
        reach = f"this machine only ({where}); the first account is not made yet"
    else:  # pragma: no cover - `require_token` has already refused this
        reach = where
    print(f"LLossless {__version__} serving {server.url}", file=out)
    print(f"  work directory  {server.store.work_dir}", file=out)
    # What the reload found, so an operator restarting after a crash is
    # told before anybody asks. Counts only: nothing about whose runs.
    found = server.store.restored
    print(f"  job index       {server.store.index_path} ({found['restored']} "
          f"run(s) reloaded: {found['resumed']} queued and resumed, "
          f"{found['interrupted']} interrupted, {found['reaped']} past their "
          f"window and deleted, {found['orphans_deleted']} unindexed "
          f"director(ies) deleted)", file=out)
    print(f"  uploads         {window}", file=out)
    print(f"  workers         {workers}", file=out)
    print(f"  credentials     {keys.path}", file=out)
    print(f"  accounts        {accounts.path} ({registered})", file=out)
    # Said on the banner because it is a promise the operator is making to
    # whoever hands them a document, and it is not visible from the page: a
    # command route runs a program as this process, with this machine's
    # credentials, shared by every account here. `0` is the ordinary answer
    # and the one a server that has never been given a routes file gives.
    print(f"  command routes  {command_routes.path} ({routes_configured})",
          file=out)
    print(f"  reachable from  {reach}", file=out)
    if registered:
        if configured_token:
            # Said out loud rather than left to be discovered. The token is
            # not merely unnecessary now, it is *not consulted* -- a script
            # still presenting it gets a 401 -- and an operator who thinks it
            # is what protects this server is an operator with the wrong
            # picture of their own deployment.
            print(f"", file=out)
            print(f"  {TOKEN_ENV} is set and is no longer used. Signing in is "
                  f"what", file=out)
            print(f"  authenticates a request now, per person rather than per "
                  f"server.", file=out)
            print(f"  Scripts present a session id in {TOKEN_HEADER} instead.",
                  file=out)
    else:
        print(f"", file=out)
        print(f"  No account exists yet, so nothing on this server answers.",
              file=out)
        print(f"  Open this once to make the first one:", file=out)
        print(f"", file=out)
        print(f"    {setup.url(server.url)}", file=out)
        print(f"", file=out)
        print(f"  The address is new on every start and stops working the "
              f"moment", file=out)
        print(f"  an account exists. Whatever is in {keys.path}", file=out)
        print(f"  becomes that account's, and is what every later account "
              f"shares.", file=out)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("", file=out)
    finally:
        server.shutdown()
        server.server_close()
        server.store.close()
    return 0


def background(server: Server) -> threading.Thread:
    """Serve on a daemon thread. For a caller that has something else to do.

    Used by the suite, and by nothing shipped. Here rather than in the test
    because `serve_forever` on a thread has one correct shutdown sequence --
    `shutdown()`, then `server_close()`, then the store -- and a test that
    writes its own copy of it is a test that can leave a worker pool alive
    after it passes.
    """
    thread = threading.Thread(target=server.serve_forever, name="llossless-http",
                              daemon=True)
    thread.start()
    return thread
