"""The versioned JSON contract. Request in, response out, no sockets anywhere.

Everything this package serves lives under `/api/v1/`, versioned from the first
commit rather than from the first breaking change. The reason is not politeness
to a future client: this project expects a second implementation of the same
contract -- a hosted service on somebody else's framework -- and a contract that
was unversioned for its first six months is a contract whose first version
cannot be named. `v1` in the path from the start means the day a field has to
change, `v2` is a directory and not an argument.

**Nothing here touches a socket, and that is the split that earns this file.**
`server.py` reads bytes off a connection and writes bytes back; this module
turns a method, a path, a header mapping and a body into a `Response`. The
motive is the one this repository has recorded twice: "four defects lived only
on the CLI path while the underlying functions tested green" -- a handler class
with the contract inlined into it can only be tested by standing a server up,
and a contract that can only be tested that way is one where the awkward cases
(a body that is not JSON, a header that is missing, an id shaped like a path)
get tested once and never again. Here they are ordinary function calls. The
server is still driven end to end by `tests/test_web_server.py`, because the
split is about making both possible, not about replacing one with the other.

**The enumerations are read, never written.** `config.FIDELITY_LEVELS` and
`config.TITLE_POLICIES` are the source of truth and `/config` reports what they
say; a second list here would be the same defect `catalogue.py` avoided by
importing `structured.PROFILES` instead of restating it. The *explanations* are
read the same way, out of the prompt fragments themselves
(`prompts/fidelity/<level>.merge.md`, `prompts/title/<policy>.md`), because the
sentence that tells the operator what a level permits and the sentence that
tells the model what it permits must not be two sentences. A picker describing
`mid` as something the prompt no longer says is worse than a picker with no
description at all.

**What a submitted request may not do** is settled one layer down and left
there. `jobs.REQUEST_SETTABLE` is the allowlist, `MergeRequest.__post_init__`
enforces it, and this module's job is to translate a form's vocabulary
(`fidelity`, `title_policy`, `model`) into the five variable names on that list
and hand the result over. It deliberately does not accept a free-form
environment mapping, even filtered: that would put a second gate in front of the
same allowlist, and two gates are how one of them ends up not being the one that
runs.

Four security rules are enforced here rather than in the handler, because each
is a property of the request and not of the transport:

  a body cap        refused at 413 by size, before the JSON parser sees it. A
                    submit with no limit is a denial of service against a box
                    whose default worker count is one.
  an id by shape    `JOB_ID` matches uuid4 hex and nothing else, checked before
                    any path is built from an id. `/runs/../../etc/passwd` is
                    refused for its shape, not by whatever `os.path` would have
                    made of it.
  a JSON body only  a cross-origin HTML form can send three content types and
                    `application/json` is not one of them, so requiring it is
                    the part of the CSRF defence that does not depend on a
                    header the attacker controls.
  origin and host   checked to agree on POST, PUT and DELETE, and the `Host`
                    itself checked to be loopback on every request that carries
                    no token. The second is the DNS-rebinding case: binding
                    `127.0.0.1` stops a packet from another machine and does
                    nothing about a page in the operator's own browser
                    resolving an attacker's name to `127.0.0.1` and posting to
                    it.

  a token           on every request, once one is configured, and then the
                    `Host` check is not also applied. `Api.check_access` has
                    the argument: the loopback rule is what a server with no
                    way to tell one requester from another does *instead of*
                    authenticating, and a deployment reached by any name at all
                    would fail it.

  an identity       once this server has accounts, every route but `session`
                    and `setup` needs one, and it is a *person* rather than a
                    shared secret. `Api.check_access` returns the account the
                    request belongs to and hands it to the route; a route that
                    looks something up takes it as an argument rather than
                    reaching for it, so a route added later cannot inherit
                    access to everybody's work by forgetting to ask.

**A job belongs to whoever submitted it, and a uuid4 is not an access
control.** `Api.job` takes the principal and answers 404 for a run belonging to
somebody else -- the same answer as a run that does not exist, because "that id
is real but not yours" is an oracle for what other people are doing on this
server. Every route that reaches a job goes through that one function: the
status, the report, the merged document, the deletion and the event stream.

And one that is not optional anywhere: **every response carrying a report goes
through `redact`**. See that module; a gap in what it redacts was left open, and
this call site closes it.

**No route returns a key, including the ones that set them.** `/settings/keys`
answers with a variable name, a boolean and four characters; `PUT` and `DELETE`
answer 204 with no body at all. The file itself is `credentials.py`'s, and the
reason this module does no more than call it is that a key which never becomes
a value here is a key no refactor of this file can serve by accident.
"""

from __future__ import annotations

import contextlib
import io
import json
import math
import os
import re
import sys
import traceback
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from .. import __version__, config, html_report, merge, prompts
from . import accounts as user_accounts
from . import catalogue, commands, credentials, defaults, discover, i18n, redact
from .events import Event, frames, parse_last_event_id
from .jobs import (MERGED_MD, REPORT_HTML, REPORT_JSON, REQUEST_SETTABLE,
                   STATED_WINDOW_MAX, STATED_WINDOW_MIN, stated_window_refusal,
                   window_unreportable,
                   RETENTION_ENV, RETRYABLE, EffortRefused, JobRefused,
                   MergeRequest, retention_warning_seconds)

# The audit bundle's route suffix and the name it downloads as. One string,
# because the route and the file are one thing: a reader who saved it and a
# reader reading a log of this server should see the same word.
BUNDLE_ZIP = "bundle.zip"

# The one prefix. Written once here and derived everywhere else, so that a
# second version can be mounted beside this one rather than instead of it.
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# uuid4 hex, as `Job.__init__` produces it, anchored at both ends. `\A`/`\Z`
# rather than `^`/`$`: `$` also matches before a trailing newline, so an id of
# `<32 hex>\n/../../etc/passwd` -- which is a thing a URL can carry once
# percent-decoding has run -- would pass a `$`-anchored check. That is not a
# hypothetical class; it is the standard way this exact validation is defeated.
JOB_ID = re.compile(r"\A[0-9a-f]{32}\Z")

# 4 MiB. Well above any realistic merge -- `MAX_SOURCES` documents that each
# fit a model's context window come to a fraction of it -- and far below what
# it costs to hold several of them in memory on a small box. A number rather
# than "unlimited, the OS will cope": the OS coping means swapping, and the
# worker that is mid-merge is the process that gets slow.
MAX_BODY_BYTES = 4 * 1024 * 1024

# The most a body may hold on a route that answers before anybody has signed
# in. A sign-in and the first account are a name, a password and a code; four
# megabytes of either is nobody's password, and those two routes are the ones
# anybody who can reach the port can post to.
MAX_OPEN_BODY_BYTES = 64 * 1024

# What a document label may be. Long enough for a real filename, short enough
# that a megabyte of text submitted as a *name* is refused as one, and no
# control characters: the label is rendered into the report's markdown tables
# and into an SSE `data:` field, and a newline in it would end a frame early.
LABEL_MAX = 200

# Hosts a `Host:` header may name. The server binds loopback and only loopback
# (see `server.HOST`), so any other value is either a proxy this milestone does
# not support or a name that resolved here without meaning to.
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})

# The body a submit may carry, and the only keys it may carry. An unknown key
# is refused rather than ignored, because the failure being guarded is a
# `title_policy` typed `titlepolicy`: silently ignored, the run happens at the
# default, succeeds, and the operator is never told the setting they chose was
# not the setting that ran.
#
# Each maps to the environment variable `config.from_env` reads it from, which
# is why the values are the names on `jobs.REQUEST_SETTABLE` rather than a
# second vocabulary. `documents` and `base` are not settings and are handled
# separately.
SETTINGS_FIELDS = {
    "model": "LLOSSLESS_MODEL",
    "merge_model": "LLOSSLESS_MERGE_MODEL",
    "fidelity": "LLOSSLESS_FIDELITY",
    "verify_depth": "LLOSSLESS_VERIFY_DEPTH",
    "title_policy": "LLOSSLESS_TITLE_POLICY",
    "loss_budget": "LLOSSLESS_LOSS_BUDGET",
    # The context window the submitter states for a typed model id, in tokens.
    # A number, bounded by `jobs.stated_window_refusal`.
    "window": "LLOSSLESS_WINDOW",
}
# `endpoint` is not a setting and is not on `REQUEST_SETTABLE`: it names one of
# the operator's own configured endpoints by provider name, and `jobs`
# translates that into an address server-side. A request never carries an
# address. See `jobs.endpoint_plan`.
# `command_route` is not a setting either, and it is the field this contract
# most needs to be read carefully. It names one of the operator's own command
# routes **by id**, and `jobs.route_plan` supplies the command from a file on
# the server. A request never carries a command: that is the whole of
# `web/commands.py`, and `jobs.REQUEST_SETTABLE` states the same rule from the
# other side by not holding `LLOSSLESS_COMMAND`.
# `effort` is the merge's effort level on a command route, and it is not
# a setting for `command_route`'s reason: it is valid only beside a route that
# can carry it, which `jobs.route_plan` checks against the operator's file.
SUBMIT_FIELDS = frozenset({"documents", "base", "endpoint", "command_route",
                           "effort", *SETTINGS_FIELDS})

# Asserted rather than commented: this module translates a form's vocabulary
# into the job layer's allowlist, and a field here that the allowlist does not
# carry would be a setting accepted by the API and refused by `MergeRequest`
# one call later -- a 500 where the contract promised a 400.
assert set(SETTINGS_FIELDS.values()) <= REQUEST_SETTABLE

JSON_TYPE = "application/json; charset=utf-8"
SSE_TYPE = "text/event-stream; charset=utf-8"

# The routes that answer before anybody has logged in, and the whole of that
# list. `session` is where a password is exchanged for one and where a page
# asks whether it needs to; `setup` is where the first account comes from; and
# `locales` is the sentences the other two are written in.
#
# **`locales` is here because a login page in no language is not a login
# page.** It was not, and the consequence was found by driving the page in a
# browser and not by any file-level check: every string on the gate rendered as
# its own key -- `auth.setup.heading` where a heading belongs -- because the
# script fetches the catalogue before it knows whether it is signed in, got a
# 401, and fell back to an empty table. The page after login was no better,
# since nothing re-fetches a catalogue that failed. What this discloses is a
# file this project publishes, naming no credential, no run and no account.
#
# An allowlist of tuples rather than a prefix test, because the failure being
# guarded is a route added under `/session/` next year that inherits an
# exemption nobody chose -- the same reasoning `jobs.REQUEST_SETTABLE` is an
# allowlist for. `/locales/<tag>` is the one shape that cannot be an exact
# tuple, and `Api._is_open` writes it out as the same two-segment rule the
# router itself uses rather than as a prefix anything can be added under.
OPEN_ROUTES = frozenset({("session",), ("setup",), ("locales",)})

# Which header a proxy uses to say the request reached it over TLS, and the
# only thing about a request this server takes a proxy's word for. It can make
# the session cookie stricter and can never make it laxer, so a hostile value
# costs a browser that refuses to send the cookie back over plain HTTP -- a
# login that does not work, rather than a credential that travels further than
# it should.
FORWARDED_PROTO = "X-Forwarded-Proto"

# The policy the HTML report is served under, which is not the server's own.
# `html_report.render` puts a `<style>` (`html_report.py:1060`) and a
# `<script>` (`html_report.py:1068`) inline in the page -- the filter box is
# that script
# -- so the API's policy, which forbids inline script, would serve a report
# whose search field silently does nothing.
#
# `sandbox allow-scripts` without `allow-same-origin` is the answer rather than
# `'unsafe-inline'` on the API's own policy: the page is put in an opaque
# origin, so its script runs and can rewrite its own DOM and cannot read
# anything belonging to this server. That is the right shape for this
# artefact on its own terms -- the report is assembled from a model's output,
# and `html_report`'s escaping and this are two independent defences rather
# than one restated.
_REPORT_POLICY = ("default-src 'none'; img-src data:; "
                  "style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
                  "base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
REPORT_CSP = f"sandbox allow-scripts; {_REPORT_POLICY}"

# The same policy for the page a reader is *shown*, plus the one capability
# that page has and the file does not: it carries a control that saves the
# report, and a sandboxed document may not start a download unless the policy
# says so. Chromium refuses it with `Download is disallowed. The frame
# initiating or instantiating the download is sandboxed, but the flag
# 'allow-downloads' is not set` -- a console warning, no dialogue, and a
# button that does nothing.
#
# Written out as the sandbox token it is rather than as a second header,
# because a browser enforces the intersection of two policies and the
# intersection of these two is the stricter one. Nothing else is relaxed: no
# `allow-same-origin`, so the page still runs in an opaque origin and its
# script still cannot read anything belonging to this server. That is also
# why the control carries the report in a `data:` URL instead of linking to
# it: an opaque origin makes every request it starts cross-site, and a
# `SameSite=Strict` session cookie does not travel with one.
REPORT_PAGE_CSP = f"sandbox allow-scripts allow-downloads; {_REPORT_POLICY}"


@dataclass(frozen=True)
class Response:
    """What the contract decided. `server.py` writes it and adds nothing.

    `body` is bytes rather than a string because the handler writes bytes and a
    `Content-Length` is a byte count; encoding here rather than there means the
    length and the payload are computed in one place from one value, which is
    the pair that goes wrong when a non-ASCII character reaches a length
    computed off a `str`.
    """

    status: int
    body: bytes = b""
    content_type: str = JSON_TYPE
    headers: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Stream:
    """An SSE response: the headers, then frames until the caller stops reading.

    Separate from `Response` rather than a `Response` whose body is a generator,
    so that a handler cannot accidentally treat one as the other -- the two are
    written to the socket in completely different ways, and the failure of
    getting it wrong is a stream that buffers until the job finishes, which is
    exactly the behaviour the stream exists to avoid and is invisible in a test
    that only checks the final bytes.
    """

    chunks: object  # an iterator of str, each one or more whole SSE frames
    headers: tuple[tuple[str, str], ...] = ()


class ApiError(Exception):
    """A refusal with a status, a stable code, and a message written for a person.

    The `code` is the part a second implementation has to keep: a client
    branching on an HTTP status alone cannot tell "that id does not exist" from
    "that id is not an id", and a client branching on the message is a client
    that breaks when the message is improved.
    """

    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message

    def response(self, *, extra=()) -> Response:
        """The error as a body. Redacted, because an exception can carry a path.

        The obvious reading is that an error body is too small to leak
        anything. It is the opposite: the bodies that carry a path are almost
        all error bodies, because a path reaches a message by way of an
        exception -- `FileNotFoundError` names the file, and the file is on
        this host.
        """
        payload = {"error": {"code": self.code,
                             "message": redact.text(self.message, extra=extra)}}
        return Response(self.status, dump(payload))


def dump(payload) -> bytes:
    """JSON as bytes, sorted, with a trailing newline. One spelling, everywhere.

    `sort_keys` so two servers serialising the same state produce the same
    bytes -- which is what lets a test compare a response against a locally
    computed payload without either side caring about dict ordering. The
    newline is for the operator with `curl` and no pretty-printer.
    """
    return (json.dumps(payload, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


# --------------------------------------------------------------------------
# what the request said
# --------------------------------------------------------------------------


def header(headers, name: str) -> str:
    """One header, case-insensitively, as a stripped string. Missing is ``.

    Takes a plain mapping rather than an `email.message.Message`, so that this
    module can be called with a dict from a test and with the handler's own
    header object from the server, and neither has to know which the other
    used.
    """
    if headers is None:
        return ""
    getter = getattr(headers, "get", None)
    if getter is None:  # pragma: no cover - defensive
        return ""
    value = getter(name)
    if value is None:
        for key in headers:
            if isinstance(key, str) and key.lower() == name.lower():
                value = headers[key]
                break
    return str(value).strip() if value is not None else ""


def hostname(authority: str) -> str:
    """The host out of a `Host:` or an origin's authority, port and brackets gone.

    Written out rather than handed to `urlsplit`, because `urlsplit` on a bare
    authority with no scheme parses the whole thing as a path and returns an
    empty hostname -- which would make every `Host:` header look like a host
    this server does not recognise, or, with the test inverted, make every one
    of them pass.
    """
    value = authority.strip().lower()
    if value.startswith("["):  # [::1]:8765
        return value[1:].split("]", 1)[0]
    if value.count(":") == 1:
        host, _, port = value.partition(":")
        return host if port.isdigit() else value
    return value


def check_host(headers) -> None:
    """The `Host` header must name a loopback address. Raises `ApiError` if not.

    This is the DNS-rebinding guard and it is the reason it runs on reads as
    well as on writes. Binding `127.0.0.1` means no packet from another machine
    reaches this socket; it means nothing at all about a page the operator's own
    browser loaded from an attacker, whose hostname resolves -- after the first
    response, deliberately -- to `127.0.0.1`. The browser then makes a
    *same-origin* request to this server, sends every cookie and no `Origin`,
    and reads the reply. The only thing that distinguishes it is the `Host`
    header, which still names the attacker.

    A missing `Host` is refused rather than allowed. HTTP/1.1 requires one, and
    the only clients that omit it are hand-written.
    """
    host = header(headers, "Host")
    if not host:
        raise ApiError(400, "no_host",
                       "the request carried no Host header, which HTTP/1.1 requires.")
    if hostname(host) not in LOOPBACK_HOSTS:
        raise ApiError(
            403, "host_not_loopback",
            f"this server answers only for a loopback Host; the request named "
            f"{host!r}. It is bound to a loopback address, so a request under "
            f"another name reached it through something in front of it. To be "
            f"reached under another name it has to be started with --host.")


def presented_token(headers) -> str:
    """The `X-LLossless-Token` header's value, or ``.

    The pre-rename header name was read too until the rename completed and is ignored
    now, as any other unknown header is.
    """
    return header(headers, credentials.TOKEN_HEADER)


def check_token(headers, expected: str) -> None:
    """Every request carries the bind token. Raises `ApiError` if it does not.

    One refusal for a missing token and a wrong one, with one message. The
    distinction is worth nothing to the operator, who knows perfectly well
    whether they set the header, and worth something to a caller probing for
    the header's name -- so it is not made.

    401 rather than 403, because the request was not authenticated rather than
    not permitted, and a client that can supply a credential should be told
    which of those happened. No `WWW-Authenticate` is sent with it: the header
    is what makes a browser open its own password dialog, and the dialog
    cannot supply a token that goes in `X-LLossless-Token`.
    """
    if not credentials.token_matches(presented_token(headers), expected):
        raise ApiError(
            401, "no_token",
            f"this server is bound where anything can reach it, so every "
            f"request must carry the operator's token in "
            f"{credentials.TOKEN_HEADER}. The token is whatever "
            f"{credentials.TOKEN_ENV} was set to when the server started.")


DEFAULT_PORTS = {"http": 80, "https": 443}


def forwarded_https(headers) -> bool:
    """Did this request reach the front of the deployment over TLS?

    The one thing this server takes a proxy's word for: see `FORWARDED_PROTO`.
    The first value, because a chain of proxies appends and the first is the
    one the browser spoke to.
    """
    return header(headers, FORWARDED_PROTO).lower().split(",")[0].strip() == "https"


def _origin(scheme: str, authority: str):
    """(scheme, host, port) of an origin, the port defaulted from the scheme.

    `None` for anything that is not one: no host, a port that is not a
    number, a scheme this server is never reached by.
    """
    scheme = scheme.lower()
    if scheme not in DEFAULT_PORTS:
        return None
    try:
        parts = urlsplit(f"//{authority}")
        port = parts.port
    except ValueError:
        return None
    if not parts.hostname or parts.username is not None:
        return None
    return scheme, parts.hostname.lower(), port or DEFAULT_PORTS[scheme]


def check_origin(headers) -> None:
    """On a mutating request, `Origin` must be this server's own. Raises if not.

    **Scheme, host and port, all three.** This compared the host alone, so a
    page served from another port of the same machine passed, and so did one
    from the same name over the other scheme. Those are other origins: a
    second service on the machine, or anything a member can start on it. And
    `SameSite=Strict` does not stand in for the comparison there, because a
    site is a name without its port, so the session cookie travels with a
    form posted from one port to another.

    This server's own origin is the `Host` the request named, under the
    scheme it arrived by. That scheme is `http` unless a proxy in front says
    it terminated TLS (`X-Forwarded-Proto: https`), which is the same word
    the `Secure` flag on the session cookie is decided by. A proxy that
    terminates TLS and does not say so is refused here on every request
    that changes something; the message says what to send.

    `Origin: null` is refused. A browser sends it for a sandboxed frame, a
    `data:` page and a redirect across origins, none of which is this
    server's page.

    A missing `Origin` is allowed, and that is a considered position rather than
    an oversight. Browsers send it on every cross-origin request and on every
    POST regardless of origin; `curl` sends none. Refusing the absent case would
    refuse the command line and buy nothing, because the requests it would
    refuse are the ones that cannot be made from a page in the first place.

    What carries the rest of this defence is the content type: see
    `check_content_type`. A cross-origin form post can only be one of three
    content types and JSON is not among them, so a page that wants to submit
    here has to make a request that is preflighted -- and the preflight arrives
    here with an `Origin` that this check then refuses.
    """
    origin = header(headers, "Origin")
    if not origin:
        return
    host = header(headers, "Host")
    scheme = "https" if forwarded_https(headers) else "http"
    wanted = _origin(scheme, host)
    parts = urlsplit(origin)
    got = _origin(parts.scheme, parts.netloc)
    if got is None or wanted is None or got != wanted:
        raise ApiError(
            403, "cross_origin",
            f"a request that changes something must come from this server's own "
            f"origin, which is {scheme}://{host}; it named {origin!r}. The "
            f"scheme, the host and the port all have to agree. Behind a proxy "
            f"that terminates TLS, the proxy has to pass the Host header "
            f"through and send {FORWARDED_PROTO}: https.")


def check_content_type(headers) -> None:
    """A submit must be JSON, by its own declaration. Raises `ApiError` if not.

    The type is checked before the body is parsed, and the refusal is 415 rather
    than 400, because "I could not read what you sent" and "I do not accept that
    kind of thing" are different answers and a client retrying on the first
    would loop forever on the second.
    """
    declared = header(headers, "Content-Type").split(";")[0].strip().lower()
    if declared != "application/json":
        raise ApiError(
            415, "not_json",
            f"a request that changes something declares Content-Type: "
            f"application/json, with or without a body; this request declared "
            f"{declared or 'nothing'}. The type is part of the defence rather "
            f"than a formality: a cross-origin form cannot send JSON without a "
            f"preflight, and the preflight is refused.")


def check_body_size(length: int, limit: int = MAX_BODY_BYTES) -> None:
    """Refuse an oversized body by its declared length, before it is read.

    Called by the server with `Content-Length` in hand, which is the only point
    at which refusing is cheaper than accepting. Checked again after the read
    in `parse_submit`, because a chunked request carries no length to check and
    a client is free to send fewer bytes than it declared or more.
    """
    if length > limit:
        raise ApiError(
            413, "body_too_large",
            f"the request body is {length} bytes and the limit is "
            f"{limit}." + (" A merge holds its documents in memory on a "
                           "server whose default worker count is one."
                           if limit == MAX_BODY_BYTES else ""))


def check_job_id(job_id: str) -> str:
    """The id, or a refusal by shape. Nothing builds a path from an unchecked id.

    By shape and not by lookup, and not by `os.path` either. A check that asked
    "does this resolve inside the work directory" would be a check whose
    correctness depended on symlinks, on the platform's separator and on
    whether the directory existed yet; a regex over 32 hex characters depends on
    none of those and refuses `../../etc/passwd` for what it is rather than for
    where it points.
    """
    if not JOB_ID.match(job_id or ""):
        raise ApiError(
            400, "bad_id",
            "a run id is 32 hexadecimal characters. Nothing else is looked up, "
            "and nothing is built from an id that is not one.")
    return job_id


# What a bundle member's name may be made of, and how long it may be. An
# operator's document label is free text up to `LABEL_MAX`: it arrives from a
# form field, and `../../.ssh/authorized_keys` is a legal one. So a member name
# is not a label with the dangerous parts taken out -- it is **built** from the
# characters of the label that are on this list, which is the same shape of
# answer `check_job_id` gives one function up. A name that survives is a name
# no separator, no drive letter and no traversal could ever have got into.
ZIP_NAME_SAFE = re.compile(r"[^A-Za-z0-9._-]+")
ZIP_NAME_MAX = 100


def _zip_name(label: str) -> str:
    """One document label as a member name: recognisable, and never a path.

    Leading and trailing dots and dashes come off after the substitution
    rather than before, so `..` is not a name that reappears once the slashes
    around it are gone. Anything that reduces to nothing becomes `document`,
    because a zip member has to be called something and an empty name is the
    one input `zipfile` will happily write.

    A name with no extension gets `.md`, and only then. These are markdown
    documents -- the engine's own names for them are `source_a.md` and so on
    -- and a label typed into a form frequently has no extension at all, which
    extracts to a file nothing will open. A label that already carries one is
    left as the operator wrote it.
    """
    cleaned = ZIP_NAME_SAFE.sub("-", str(label)).strip("-.")
    cleaned = cleaned[:ZIP_NAME_MAX] or "document"
    return cleaned if "." in cleaned else f"{cleaned}.md"


def _redacted_report_json(raw: str, *, extra=()) -> str:
    """`report.json` as the run route serves it: parsed, redacted, written back.

    As a structure and not as text, because `redact.report` walks the payload
    and `Api.run` already hands a client the result of exactly this call. A
    bundle carrying the file off disk unchanged would be a copy of the one
    artefact on this server that has never been through a scrub.

    A file this server cannot parse is scrubbed as text instead of refused.
    It should not be possible -- this process wrote it -- and if it ever is,
    the reader gets a damaged report rather than no bundle, with the redaction
    still applied.
    """
    try:
        payload = json.loads(raw)
    except ValueError:
        return redact.text(raw, extra=extra)
    if not isinstance(payload, dict):
        return redact.text(raw, extra=extra)
    return json.dumps(redact.report(payload, extra=extra), indent=2) + "\n"


def _not_a_number(name: str):
    """`NaN`, `Infinity` and `-Infinity` are not JSON, and are refused as not JSON.

    Python's parser reads all three unless told otherwise. A `loss_budget` of
    `NaN` was accepted and queued: every comparison against it is false, so it
    is a budget nothing is ever over.
    """
    raise ValueError(f"{name} is not a JSON number")


def _json_object(raw: bytes) -> dict:
    """A request body as a JSON object, or a 400 a person can act on.

    Shared by the submit path and the settings path rather than written twice.
    The size check comes first here as it does there: a body is refused by its
    declared length in `server.py` before it is read, and again by its actual
    length here, because a client is free to send fewer bytes than it declared
    or more.

    The parser's own message is quoted, as it is for a submit -- it names a
    position in a document the client itself sent. The value inside that
    document is never quoted, which is what keeps this usable on a body whose
    one field is a key.
    """
    if len(raw) > MAX_BODY_BYTES:
        check_body_size(len(raw))
    try:
        payload = json.loads(raw.decode("utf-8"), parse_constant=_not_a_number)
    except (UnicodeDecodeError, ValueError) as exc:
        raise ApiError(400, "bad_json", f"the request body is not JSON: {exc}") from None
    if not isinstance(payload, dict):
        raise ApiError(400, "bad_json",
                       f"this route takes a JSON object; got a "
                       f"{type(payload).__name__}.")
    return payload


def parse_submit(raw: bytes) -> MergeRequest:
    """A POST body as a `MergeRequest`. Every refusal is a 400 a person can act on.

    **`documents` is a list of objects, not an object keyed by name.** The order
    is load-bearing all the way down -- `cli.prepare_merge` renames the nth
    document to the nth canonical name, and every figure this project has
    published was measured with those names -- and while Python's `json`
    preserves object order, JSON itself does not promise it and neither does
    every client library that will ever post here. A list says the order is
    meant. It also makes a duplicate label visible: as an object the second
    would silently replace the first and the merge would run with one fewer
    document than the operator sent.
    """
    payload = _json_object(raw)

    unknown = sorted(set(payload) - SUBMIT_FIELDS)
    if unknown:
        raise ApiError(
            400, "unknown_field",
            f"this request sets {', '.join(unknown)}, which the contract does "
            f"not define. The fields are {', '.join(sorted(SUBMIT_FIELDS))}. An "
            f"unknown field is refused rather than ignored, because a "
            f"mistyped setting that is ignored runs at the default and says "
            f"nothing about it.")

    documents = _documents(payload.get("documents"))
    base = payload.get("base")
    if base is not None and not isinstance(base, str):
        raise ApiError(400, "bad_base",
                       f"base names one of the submitted documents and is "
                       f"therefore a string; got a {type(base).__name__}.")

    endpoint = payload.get("endpoint")
    if endpoint is not None and not isinstance(endpoint, str):
        raise ApiError(400, "bad_endpoint",
                       f"endpoint names one of this server's configured "
                       f"providers and is therefore a string; got a "
                       f"{type(endpoint).__name__}.")

    route = payload.get("command_route")
    if route is not None and not isinstance(route, str):
        raise ApiError(400, "bad_command_route",
                       f"command_route names one of this server's configured "
                       f"command routes by id and is therefore a string; got a "
                       f"{type(route).__name__}.")

    effort = payload.get("effort")
    if effort is not None and not isinstance(effort, str):
        raise ApiError(400, "bad_effort",
                       f"effort is the merge's effort level, one of "
                       f"{', '.join(commands.EFFORT_CHOICES)}, and therefore a "
                       f"string; got a {type(effort).__name__}.")

    try:
        return MergeRequest(documents=documents, base=base,
                            endpoint=endpoint or None,
                            route=route or None,
                            overrides=_overrides(payload),
                            effort=None if effort is None else effort.strip())
    except EffortRefused as exc:
        raise ApiError(400, "bad_effort", str(exc)) from None
    except credentials.UnknownProvider as exc:
        raise ApiError(400, "bad_endpoint", str(exc)) from None
    except commands.UnknownRoute as exc:
        # Named as its own code rather than folded into `refused`, because a
        # client branching on the status alone cannot tell "that is not an id"
        # from "these documents cannot be merged", and this is the refusal a
        # page has to be able to explain in its own words.
        raise ApiError(400, "bad_command_route", str(exc)) from None
    except JobRefused as exc:
        raise ApiError(400, "refused", str(exc)) from None


def _documents(value) -> dict[str, str]:
    """The documents, checked for arity, shape, labels and duplicates."""
    if not isinstance(value, list):
        raise ApiError(
            400, "bad_documents",
            f"documents is a list of "
            f'{{"name": ..., "text": ...}} objects, in the order the sources '
            f"are given; got a {type(value).__name__}.")
    if not merge.MIN_SOURCES <= len(value) <= merge.MAX_SOURCES:
        raise ApiError(
            400, "bad_arity",
            f"a merge takes between {merge.MIN_SOURCES} and "
            f"{merge.MAX_SOURCES} documents; this request carried "
            f"{len(value)}.")
    documents: dict[str, str] = {}
    for index, entry in enumerate(value):
        if not isinstance(entry, dict):
            raise ApiError(400, "bad_documents",
                           f"document {index} is a {type(entry).__name__}, not "
                           f"an object with a name and a text.")
        name, text = entry.get("name"), entry.get("text")
        if not isinstance(name, str) or not name.strip():
            raise ApiError(400, "bad_documents",
                           f"document {index} has no name. The name is what the "
                           f"report calls this document back to you.")
        if len(name) > LABEL_MAX or any(character in name for character in "\r\n\t"):
            raise ApiError(
                400, "bad_documents",
                f"document {index}'s name is unusable: at most {LABEL_MAX} "
                f"characters and no line breaks. It is rendered into the "
                f"report's tables and into the progress stream, and a line "
                f"break in it would truncate an event.")
        if not isinstance(text, str):
            raise ApiError(400, "bad_documents",
                           f"document {name!r} has no text, or its text is a "
                           f"{type(text).__name__} rather than a string.")
        if name in documents:
            raise ApiError(
                400, "duplicate_document",
                f"{name!r} was submitted twice. Names are how base picks a "
                f"document and how the report names them back to you, so two "
                f"documents cannot share one.")
        documents[name] = text
    return documents


def _overrides(payload: dict) -> dict[str, str]:
    """The settings a request may choose, as the environment `config` reads.

    Validated here against `config`'s own tuples rather than passed through for
    `config.from_env` to refuse later. Both would refuse; only one of them
    refuses before a job id exists, and an operator who is told their fidelity
    level is wrong after the job was accepted has to go and look at a run that
    failed for a reason they could have been told at submit time.
    """
    overrides: dict[str, str] = {}
    for name, variable in SETTINGS_FIELDS.items():
        value = payload.get(name)
        if value is None:
            continue
        if name == "loss_budget":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ApiError(400, "bad_loss_budget",
                               f"loss_budget is a fraction of the source "
                               f"segments; got a {type(value).__name__}.")
            # A number too large for a float parses as infinity, and an
            # integer too large for one does not convert at all.
            try:
                finite = math.isfinite(float(value))
            except OverflowError:
                finite = False
            if not finite:
                raise ApiError(400, "bad_loss_budget",
                               "loss_budget is a fraction of the source "
                               "segments, so a finite number.")
            overrides[variable] = repr(float(value))
            continue
        if name == "window":
            # A JSON integer, and nothing that merely converts to one: `true`
            # is an int in Python and "200k" is a string a person meant as a
            # number. The bounds are the job layer's, in one function.
            if isinstance(value, bool) or not isinstance(value, int):
                raise ApiError(400, "bad_window",
                               f"window is a whole number of tokens; got a "
                               f"{type(value).__name__}.")
            refusal = stated_window_refusal(value)
            if refusal:
                raise ApiError(400, "bad_window", refusal)
            overrides[variable] = str(value)
            continue
        if not isinstance(value, str) or not value.strip():
            raise ApiError(400, f"bad_{name}",
                           f"{name} is a non-empty string; got "
                           f"{type(value).__name__}.")
        value = value.strip()
        if name == "fidelity":
            if value not in config.FIDELITY_CHOICES:
                raise ApiError(400, "bad_fidelity",
                               f"{value!r} is not a fidelity level. The levels "
                               f"are {', '.join(config.FIDELITY_CHOICES)}.")
            # Canonicalised here so the job layer, the cassette key and the
            # report all see one spelling. `verbatim` and `off` are the same
            # run (`config.py:707`), and two spellings reaching disk would make
            # them look like two.
            value = config.canonical_fidelity(value)
        if name == "verify_depth" and value not in config.VERIFY_DEPTHS:
            raise ApiError(400, "bad_verify_depth",
                           f"{value!r} is not a verification depth. The depths "
                           f"are {', '.join(config.VERIFY_DEPTHS)}.")
        if name == "title_policy" and value not in config.TITLE_POLICIES:
            raise ApiError(400, "bad_title_policy",
                           f"{value!r} is not a title policy. The policies are "
                           f"{', '.join(config.TITLE_POLICIES)}.")
        overrides[variable] = value
    return overrides


# --------------------------------------------------------------------------
# what the answer says
# --------------------------------------------------------------------------


def first_paragraph(text: str) -> str:
    """The opening paragraph of a prompt fragment, on one line.

    Lines joined rather than kept, because a prompt is wrapped for a model and a
    picker renders into whatever width the page has; a hard wrap copied into
    JSON is a hard wrap in somebody's tooltip.
    """
    return " ".join(text.split("\n\n")[0].split())


def fidelity_levels() -> list[dict]:
    """Every level, in `config.FIDELITY_LEVELS` order, described for a person.

    **This used to serve the prompt fragment's opening paragraph, and that was
    the defect.** The argument for it was that the sentence shown to the
    operator and the sentence shown to the model should be one sentence, so a
    level whose rules changed could not go on being described by a summary
    somebody wrote once. The argument is sound about drift and wrong about
    audience: a prompt is written to a model in the second person, so the
    picker rendered *"you are expected to look a fact up"* and *"you have been
    given a web tool for this run"* at somebody choosing a setting. Every level
    had it; the newest fragment only made it obvious.

    So the copy is `config.FIDELITY_SHAPES`, which is written for a reader and
    is the same table `--fidelity`'s help renders from -- the drift this
    function's old docstring worried about is answered by having *one* source
    for the two surfaces that face a person, rather than by pointing one of
    them at the model's instructions.

    **The copy itself is not in this payload, and that is the one place this
    differs from `verify_depths` below.** A description is prose shown to a
    person, the page is translated, and an English paragraph arriving from an
    API into a German page is the same defect in a second language. So this
    serves the enumeration -- the values, in order, with the published name and
    the default -- and the page renders `fidelity.<value>.summary`, `.buys` and
    `.costs` out of the locale catalogue it already loaded, exactly as it
    renders `basis.<value>` and `kind.<value>`. It holds no level vocabulary
    either way: the key is built from a value this function gave it.

    `config.FIDELITY_SHAPES` stays the English source and is what `--fidelity`'s
    help renders from; `tests/test_contract_parity.py` pins `en.json` to it
    field by field, so the command line and the page cannot describe one level
    two ways.

    `name` is what a person reads and `value` is what goes on the wire; they
    differ for exactly one level (`config.FIDELITY_NAMES`), and a picker that
    showed only one of them would either display a word the API refuses or
    submit a word the operator never saw.
    """
    return [{
        "value": level,
        "name": config.fidelity_name(level),
        "default": level == config.DEFAULT_FIDELITY,
        # The level that asks the model to look facts up, flagged so the
        # page's effort card can say what it says about it without
        # learning the level's name.
        "retrieves": level == config.SOURCED,
        # Whether this level lets the merge declare an addition at all:
        # `merge.ADDS`, the same flag `merge_schema` reads to decide whether a
        # model at this level is even handed the field. The page's checks
        # tile reads this to tell "this level does not ask for that" apart
        # from "it should have run and did not", without learning which
        # levels those are by name.
        "adds": bool(merge.ADDS[level]),
    } for level in config.FIDELITY_LEVELS]


def verify_depths() -> list[dict]:
    """Every depth, in `config.VERIFY_DEPTHS` order, with what it does and does not do.

    The fidelity ladder's counterpart, and it follows the same rule for the
    same reason: the page renders a picker out of what it was served and holds
    no vocabulary of its own. There the explanation comes from the prompt
    fragment the model is given; a depth has no fragment, so it comes from
    `config.VERIFY_DEPTH_SHAPES`, which is also what `--verify-depth`'s help
    renders from. One sentence, three surfaces.

    Three fields here are not prose, and each exists because a page that had to
    derive it would derive it from the depth's *name*:

    `detects_invention` is what the verdict is read against. A clean `coverage`
    run means the sources' content survived and means nothing at all about
    invention, and the page says so on the verdict rather than only in the
    provenance block. Served as a boolean so that the day a third depth exists
    the page needs no edit to describe it correctly.

    `fixed_calls` and `calls_per_source` are what makes the cost fall visibly
    when the cheaper depth is picked, for the source count actually loaded
    rather than for an assumed two. `exact` says whether their sum is the
    run's cost or its lower bound -- `full` batches its two verify steps, 25
    claims a call over HTTP and 100 through a command, so there it is a floor,
    and the page renders the two cases in different words. See
    `config.merge_model_calls` for why no dollar figure is offered beside it.

    What is deliberately *not* on these rows is any detection figure. One is
    published now: the 2026-09-24 re-run measured what the cheap depth
    costs in detection, and it is served beside the rows as
    `verify_depth.quality_delta`, the catalogue's `verify_depth` block as
    `catalogue.load` validated it -- split by probe direction, with the class
    a depth cannot reach named rather than folded into a lower rate, and with
    its run, artefacts and derived_by. A row here describes what a depth
    *does*, from `config`; a measured figure is a fact about one model on one
    test set, and it stays in the one block that carries its provenance. When
    the catalogue has no block the page says "unmeasured" rather than showing
    a zero, a blank or an estimate -- the rule `pricing.py` already keeps for
    costs.
    """
    return [{
        "value": value,
        "name": shape.name,
        "explains": shape.explains,
        "detects_invention": shape.detects_invention,
        "calls": {
            "fixed": shape.fixed_calls,
            "per_source": shape.calls_per_source,
            # Whether the two above add up to the run's cost or to its floor.
            # Served rather than derived for `detects_invention`'s reason: a
            # page that knew which depth batches would know it by name.
            "exact": shape.exact_calls,
        },
        "default": value == config.DEFAULT_VERIFY_DEPTH,
    } for value, shape in config.VERIFY_DEPTH_SHAPES.items()]


def title_policies() -> list[dict]:
    """Every policy, with the rule the merge prompt is actually given for it."""
    return [{
        "value": policy,
        "explains": first_paragraph(prompts.load(f"title/{policy}").text),
        "default": policy == config.DEFAULT_TITLE_POLICY,
    } for policy in config.TITLE_POLICIES]


def providers(environ, keys=None) -> list[dict]:
    """Which roles have a credential configured. Presence, and never a value.

    `keys` is where presence is read from when the caller has one -- an
    account's own credentials, which never reach `os.environ` and so cannot be
    found by looking there. Without it the environment answers, which is the
    single-tenant server and every CLI run.

    `Settings.api_key()` (`config.py:1924`) stores the *name* of an environment
    variable and reads the value at send time, deliberately, so that no `repr`,
    `asdict` or JSON dump can carry a key. This endpoint is the one place a
    browser asks about that arrangement, and it answers with a boolean.

    The variable *name* is reported, and that is not an oversight: `config.py`'s
    own docstring says a name is not a secret, and without it an operator whose
    server reports `configured: false` has no way to find out which variable it
    looked at. What is never reported is the value, and there is no endpoint
    that takes a variable name and returns anything about it.
    """
    settings = config.from_env(environ)
    seen: list[dict] = []
    for role in (None, *sorted(config.ROLES)):
        variable = settings.api_key_env_for(role)
        source = environ if keys is None else keys
        seen.append({
            "role": role or "default",
            "variable": variable,
            "configured": bool((source.get(variable) or "").strip()),
        })
    return seen


# --------------------------------------------------------------------------
# the routes
# --------------------------------------------------------------------------


@dataclass
class Api:
    """The contract, bound to one job store. Call `handle`; get a `Response`.

    A class rather than module functions because every route needs the same two
    things -- the store to look a job up in, and the environment the server was
    started with -- and threading both through nine functions is how one call
    site ends up reading `os.environ` directly and reporting a provider the jobs
    do not actually resolve.

    `environ` defaults to the store's own copy rather than to `os.environ`, so
    that `/health` answers for what a submitted job would see. The store copies
    the environment once at construction (`web/jobs.py:1876`) precisely so an
    unrelated part of the process cannot change what a queued job resolves to;
    a health endpoint reading the live environment would report a configuration
    no run on this server will ever use.
    """

    store: object
    environ: dict = None  # type: ignore[assignment]
    catalogue_path: object = None
    # What a request has to present. Empty means nothing does, which is the
    # loopback default and is the only configuration in which this server can
    # be started without one -- `server.build` refuses any other address with
    # an empty token, so an `Api` with no token is an `Api` nothing but this
    # machine can reach.
    token: str = ""
    # The credentials file the settings routes manage. Defaulted here rather
    # than required, so that every existing construction of `Api` keeps
    # working; nothing reads the file until a settings route is called.
    keys: object = None
    # The account store, and `None` is a configuration rather than a missing
    # value: it means *this server has no accounts at all*, which is the
    # single-tenant arrangement, and is what a library caller
    # embedding `build` gets unless it asks for more. `server.serve` -- the
    # command an operator actually runs -- always supplies one, so the mode
    # below with no identity in it is not reachable from the command line.
    accounts: object = None
    # Live sessions and the one-time setup token. Both are per-server and both
    # die with the process; see `accounts.Sessions` and `accounts.Setup`.
    sessions: object = None
    setup: object = None
    # How many wrong passwords one submitted name may collect. See
    # `accounts.Throttle` for why a locked name answers exactly as a wrong
    # password does rather than with a status of its own.
    throttle: object = None
    # Which credentials file belongs to whom. `accounts.Directory`, built from
    # `keys` so that the operator's shared file and the per-account ones are
    # the same object's two answers rather than two objects that can disagree.
    directory: object = None
    # The address this server was bound to. Not cosmetic: it is what decides
    # whether the `Host` header is checked, and the honest discriminator for
    # that is the bind rather than whether a secret happens to be configured.
    bind: str = "127.0.0.1"
    # The directories this server writes to, handed to `redact` so that a path
    # quoted by a failing job is cleaned along with the rest. Not derivable
    # inside `redact`: it knows where the *tool* is installed, not where this
    # operator told this server to keep its work.
    extra_roots: tuple = field(default_factory=tuple)
    # The operator's command routes, read from the store rather than passed in
    # beside it. Two fields naming one list is two things that can disagree,
    # and the one that mattered would be the store's, because that is the one a
    # submitted job resolves against -- the same argument `environ` above makes
    # for reading the store's copy.
    routes: object = None

    def __post_init__(self) -> None:
        if self.environ is None:
            self.environ = getattr(self.store, "environ", {})
        if self.routes is None:
            self.routes = getattr(self.store, "routes", None) or commands.NoCommands()
        if self.keys is None:
            self.keys = credentials.Credentials()
        if self.sessions is None:
            self.sessions = user_accounts.Sessions()
        if self.setup is None:
            self.setup = user_accounts.Setup()
        if self.throttle is None:
            self.throttle = user_accounts.Throttle()
        if self.directory is None:
            self.directory = user_accounts.Directory(self.keys)
        if not self.extra_roots:
            self.extra_roots = tuple(
                str(path) for path in (getattr(self.store, "work_dir", None),
                                       getattr(self.store, "cache_dir", None))
                if path is not None)

    # -- entry point -----------------------------------------------------

    def handle(self, method: str, path: str, *, body: bytes = b"",
               headers=None) -> Response:
        """One request, one response. Never raises; a refusal is a status.

        A handler that raised would put the decision about what a client sees
        in an `except` clause in `server.py`, which is the one place a traceback
        can reach a socket. Everything that can go wrong here is an `ApiError`
        with a status already chosen, and anything that is not is caught and
        turned into a 500 with no detail -- the detail goes to the operator's
        stderr, where the operator is, and not to whoever posted the request.
        """
        who = None
        try:
            who = self.check_access(headers, self._segments(path))
            if method in ("POST", "DELETE", "PUT", "PATCH"):
                check_origin(headers)
                # On every one of them, not only the ones that read a body.
                # Retry and cancel take none, so they asked for no type, and
                # a form on another page can post without one: a form sent
                # with the session cookie started a new run. The page sends
                # the type on everything it sends (`sendJson` in `app.js`).
                check_content_type(headers)
            return self._route(method, path, body=body, headers=headers, who=who)
        except user_accounts.AccountError as refusal:
            # The same shape as the credentials case below and for the same
            # reason: the message names a rule, a file or a shape and never a
            # password, and the person who can act on it is the one asking.
            return ApiError(400, "bad_account",
                            str(refusal)).response(extra=self.roots_for(who))
        except credentials.CredentialsError as refusal:
            # The credentials file is unusable and the operator is the only
            # person who can act on it, so the reason travels -- these messages
            # are built under the rule that they name a path, a mode or a shape
            # and never a value. 409 rather than 500: nothing here is broken,
            # the state on disk is wrong, and a client retrying would loop.
            #
            # To the operator. A member cannot act on a file's mode and is
            # not shown where this server keeps its files, so a member gets
            # the fact and the operator's stream gets the reason.
            if self._member(who):
                print(f"llossless serve: {refusal}", file=sys.stderr, flush=True)
                return ApiError(
                    409, "bad_credentials",
                    "the endpoints and keys stored on this server could not "
                    "be read, so this was not done. The reason is on the "
                    "server's own error stream; ask whoever runs it.").response()
            return ApiError(409, "bad_credentials",
                            str(refusal)).response(extra=self.extra_roots)
        except ApiError as refusal:
            return refusal.response(extra=self.roots_for(who))
        except Exception:  # noqa: BLE001 - see the docstring
            # The traceback goes to the operator's stream, where the operator
            # is. It does not go into the response: a traceback names modules,
            # line numbers and frequently a path, and the person who posted the
            # documents is not the person who can act on any of it.
            traceback.print_exc(file=sys.stderr)
            return ApiError(
                500, "internal",
                "the server failed while answering this request. What went "
                "wrong is on the server's own error stream; nothing about it "
                "is reported here on purpose.").response()

    def admit(self, path: str, headers, length: int) -> None:
        """May this request's body be read at all? Raises `ApiError` if not.

        Asked by the server with the declared length in hand and before it
        reads a byte. A body was read in full, up to the four megabytes a
        submit may carry, and only then was its sender asked who they were:
        anybody who could reach the port could have the server hold that
        much per connection. So the identity comes first, and the routes
        that answer without one take a body no larger than a sign-in is.

        `handle` asks who is there again when it is handed the request. That
        is one more lookup, and it keeps this from being the only gate.
        """
        parts = self._segments(path)
        self.check_access(headers, parts)
        check_body_size(length, MAX_OPEN_BODY_BYTES
                        if self.tenanted and self._is_open(parts)
                        else MAX_BODY_BYTES)

    def knows(self, headers) -> bool:
        """Is this request from somebody this server would answer? Never raises.

        A signed-in account, or anybody at all on a server that has no
        accounts and asks for no token. For the server's decision about how
        much of a refused body it will read out of politeness.
        """
        try:
            return self.check_access(headers, None) is not None or not self.tenanted
        except ApiError:
            return False

    @staticmethod
    def _member(who) -> bool:
        """Is this an account that is not an operator's?"""
        return who is not None and not getattr(who, "operator", False)

    def roots_for(self, who) -> tuple:
        """The directories to take out of what this caller is sent.

        `extra_roots` for the operator and for a server with no accounts:
        where the work is kept. A member is also not told where this server
        keeps its configuration: the directories of the credentials file,
        the accounts file and the commands file. Those messages are written
        for the operator and name the file by its path, and `redact` on its
        own knows the home directory and not what is below it.

        For what this server says in its own words: a refusal, a run's
        `error`, the progress stream, a route's reason. A report is served
        under `extra_roots` to everybody, as it always was: it quotes the
        documents, and its bytes do not depend on who reads it.
        """
        if not self._member(who):
            return self.extra_roots
        # Not the null device, which is the path of a store with no file
        # (`commands.NoCommands`): its directory is no secret, and taking it
        # out would take four characters out of ordinary text.
        places = [getattr(self.keys, "path", None),
                  getattr(self.accounts, "path", None),
                  getattr(self.routes, "path", None)]
        folders = [str(Path(place).parent) for place in places
                   if place and str(place) != os.devnull]
        root = getattr(self.directory, "root", None)
        return (*self.extra_roots, *folders, *([str(root)] if root else []))

    # -- who is asking ---------------------------------------------------

    @property
    def tenanted(self) -> bool:
        """Does this server have an account store at all? See the `accounts` field."""
        return self.accounts is not None

    def account_count(self) -> int:
        """How many accounts exist, or 0 when there is no store.

        Read on every request rather than cached, and that is deliberate: the
        first account is created *by a request*, and a cached zero would leave
        the server in setup mode until it was restarted -- the operator would
        create their account, be told it worked, and then be refused by the
        next page load.
        """
        if self.accounts is None:
            return 0
        try:
            return self.accounts.count()
        except user_accounts.AccountError:
            # An unusable accounts file is not a reason to let everybody in.
            # Zero means setup mode, which answers one route and refuses the
            # rest, and the operator meets the file's own message there.
            return 0

    def check_transport(self, headers) -> None:
        """The `Host` check, when and only when this server bound loopback.

        The discriminator changed with this milestone and the change is the
        honest one. An earlier change switched the check off whenever a *token* was
        configured, because a deployment reached over a network is reached by
        some name and every such name fails the loopback test -- true, but it
        tied a transport question to whether a secret happened to be set, so a
        loopback server with a token stopped being defended against rebinding
        for no reason connected to rebinding.

        The question the check answers is "could this request have come from
        another machine at all", and the thing that decides it is the address
        this server bound. So: bound to loopback, the `Host` must name
        loopback; bound to anything else, it is not checked, because there is
        no name that would pass and the operator asked for exactly that.

        On a loopback bind the two defences now stack rather than alternate. A
        rebound page carries no session cookie -- cookies are scoped to the
        host they were set for, and the attacker's name is not that host -- and
        it fails this as well.
        """
        if credentials.is_loopback(self.bind):
            check_host(headers)

    def check_access(self, headers, parts=None):
        """Who is allowed to ask, and who they are. Returns the account or None.

        Four arrangements, in the order they are decided, and each is a
        configuration rather than a fallback:

          no account store      the base server. The token if one is configured,
                                the `Host` check as the transport guard, and
                                no identity -- everybody who gets in is the
                                same person. `server.build` gives this to a
                                library caller that asks for nothing else;
                                `server.serve` never does.

          a store, no accounts  setup. One route answers -- `POST /setup`, and
                                only with the one-time token -- and everything
                                else is 401 `setup_required`. A server nobody
                                has an account on is not a server anybody may
                                use, which is what makes "no default password"
                                affordable.

          an account, open      `session` and `setup` answer with no identity.
          route                 A login page that needed to be logged in to
                                reach would be a login page nobody can use.

          an account, anything  a live session, presented as the cookie a
          else                  browser sends by itself or as the header a
                                script sets. The account it belongs to is
                                returned and handed to the route.

        **The bind token is not consulted once an account exists.** It has been
        superseded, and `credentials.require_token` says why at the other end:
        two parallel secrets where one is redundant is an arrangement in which
        the wrong one stays configured for years. `serve` prints a line saying
        so when it finds one set.

        Called from `handle` and, separately, from the event stream in
        `server.py`, which does not go through it. One expression of the rule
        for both, because the version of this that goes wrong is the one where
        a path added later inherits a gap nobody chose.
        """
        self.check_transport(headers)
        if not self.tenanted:
            if self.token:
                check_token(headers, self.token)
            return None
        if self.account_count() == 0:
            if self.token:
                check_token(headers, self.token)
            if self._is_open(parts):
                return None
            raise ApiError(
                401, "setup_required",
                "this server has no accounts yet, so nothing on it is "
                "reachable. The line it printed when it started carries a "
                "one-time address that creates the first one.")
        if self._is_open(parts):
            return None
        who = self.principal(headers)
        if who is None:
            raise ApiError(
                401, "no_session",
                f"this server needs you to be logged in. Post a username and a "
                f"password to {API_PREFIX}/session; a browser is then carried "
                f"by the cookie that answer sets, and a script presents the "
                f"same value in {user_accounts.SESSION_HEADER}.")
        return who

    @staticmethod
    def _is_open(parts) -> bool:
        """Does this route answer with no identity? The whole of that question.

        Exact tuples, plus the one route that has two spellings: `GET /locales`
        and `GET /locales/<tag>` are one thing asked two ways, and the second
        cannot be an exact tuple because the tag is the argument. It is written
        out as the same two-segment rule `_route` uses rather than as a prefix,
        so a route added at `/locales/<tag>/something` does not inherit the
        exemption.
        """
        if parts is None:
            return False
        parts = tuple(parts)
        if parts in OPEN_ROUTES:
            return True
        return parts[:1] == ("locales",) and len(parts) <= 2

    def principal(self, headers):
        """The account behind this request's session, or None. Never raises.

        The header is preferred over the cookie where both are present: a
        script that set one asked for that identity explicitly, and a cookie is
        ambient -- attached by the browser to a request the page may not have
        meant to make. Where the two disagree, the explicit one is the one
        somebody chose.

        An id that names a live session belonging to an account that has since
        been deleted answers None, so a deletion takes effect on the next
        request even if `revoke_account` was not reached.
        """
        session_id = self.session_id(headers)
        if not session_id:
            return None
        session = self.sessions.lookup(session_id)
        if session is None:
            return None
        try:
            return self.accounts.by_id(session.account)
        except user_accounts.AccountError:
            return None

    @staticmethod
    def session_id(headers) -> str:
        """The presented session id, from the header first and the cookie second."""
        presented = presented_token(headers)
        if presented:
            return presented
        return user_accounts.session_from_cookie(header(headers, "Cookie"))

    @staticmethod
    def session_ids(headers) -> tuple[str, ...]:
        """Every session id the request presents: the header, then the cookie.

        What a logout revokes.
        """
        ids = (presented_token(headers),
               *user_accounts.sessions_from_cookie(header(headers, "Cookie")))
        return tuple(dict.fromkeys(i for i in ids if i))

    @staticmethod
    def over_tls(headers) -> bool:
        """Did this request reach the front of the deployment over TLS?

        The only thing here that takes a proxy header's word for anything, and
        it is safe in exactly one direction: see `FORWARDED_PROTO`.
        """
        return forwarded_https(headers)

    def _operator(self, who):
        """`who`, if they may change what everybody shares. 403 if not.

        403 and not 404: the route exists, the caller is authenticated, and
        they are not permitted -- which is a different thing to tell a client
        than "there is no such thing", and the one they can act on by asking
        the operator.
        """
        if who is None or getattr(who, "operator", False):
            return who
        raise ApiError(
            403, "not_operator",
            "that belongs to whoever set this server up. The endpoints the "
            "operator configures are shared with everybody; the ones you "
            "configure are yours, and you can set your own for any provider.")

    def _route(self, method: str, path: str, *, body: bytes, headers,
               who=None) -> Response:
        parts = self._under_prefix(path)
        if parts[:1] == ("session",) and len(parts) == 1:
            if method == "GET":
                return Response(200, dump(self.session_state(headers)))
            if method == "POST":
                return self.log_in(body, headers)
            if method == "DELETE":
                return self.log_out(headers)
            raise self._wrong_method(method, "GET, POST, DELETE")
        if parts == ("setup",):
            if method != "POST":
                raise self._wrong_method(method, "POST")
            return self.first_account(body, headers)
        if parts[:1] == ("accounts",):
            return self._account_route(method, parts, body, headers, who)
        # A route that exists refuses the wrong verb with a 405 rather than
        # falling through to the 404 below. The two are different answers: 404
        # tells a client the path is wrong and sends it looking for a typo,
        # where the path was right and the method was not.
        if parts in (("health",), ("config",)):
            if method != "GET":
                raise self._wrong_method(method, "GET")
            return Response(200, dump(self.health(who) if parts[0] == "health"
                                      else self.config(who)))
        if parts == ("defaults",):
            # The caller's saved run settings. Their own and nobody
            # else's: the file is named by `who`, never by the request.
            if method == "GET":
                return Response(200, dump(self.get_defaults(who)))
            if method == "PUT":
                return self.put_defaults(body, headers, who)
            if method == "DELETE":
                return self.delete_defaults(who)
            raise self._wrong_method(method, "GET, PUT, DELETE")
        if parts[:1] == ("locales",) and len(parts) <= 2:
            # `GET /locales` is "the right one for this browser, plus what else
            # there is"; `GET /locales/<tag>` is "that one". Two spellings of
            # one route rather than a query parameter, because the second is
            # the one a persisted choice asks for and a path is what a cache,
            # a proxy log and an operator with `curl` can all read as an
            # identity.
            if method != "GET":
                raise self._wrong_method(method, "GET")
            return Response(200, dump(self.locale(parts[1] if len(parts) == 2
                                                  else "", headers)))
        if parts[:2] == ("settings", "keys"):
            if len(parts) == 2:
                if method != "GET":
                    raise self._wrong_method(method, "GET")
                return Response(200, dump(self.list_keys(who)))
            if len(parts) == 3:
                if method == "PUT":
                    return self.set_key(parts[2], body, headers, who)
                if method == "DELETE":
                    return self.delete_key(parts[2], who)
                raise self._wrong_method(method, "PUT, DELETE")
        if parts[:2] == ("settings", "endpoints") and len(parts) == 3:
            if method == "PUT":
                return self.set_endpoint(parts[2], body, headers, who)
            if method == "DELETE":
                return self.delete_endpoint(parts[2], who)
            raise self._wrong_method(method, "PUT, DELETE")
        if parts[:2] == ("settings", "commands") and len(parts) == 3:
            # No body is read on either verb. The path segment is the whole of
            # the request and it is looked up in a table, which is what makes
            # "the browser never supplies text that reaches a shell" a property
            # of the routing rather than of a validator.
            if method == "PUT":
                return self.enable_command(parts[2], who)
            if method == "DELETE":
                return self.disable_command(parts[2], who)
            raise self._wrong_method(method, "PUT, DELETE")
        if parts == ("runs",):
            if method == "GET":
                return Response(200, dump(self.runs(who)))
            if method == "POST":
                return self.submit(body, headers, who)
            raise self._wrong_method(method, "GET, POST")
        if len(parts) == 2 and parts[0] == "runs":
            if method == "GET":
                return Response(200, dump(self.run(parts[1], who)))
            if method == "DELETE":
                return self.delete(parts[1], who)
            raise self._wrong_method(method, "GET, DELETE")
        if len(parts) == 3 and parts[0] == "runs" and parts[2] == "cancel":
            # A POST under a run: cancel it.
            if method != "POST":
                raise self._wrong_method(method, "POST")
            return self.cancel(parts[1], who)
        if len(parts) == 3 and parts[0] == "runs" and parts[2] == "retry":
            # The other: start a new run from this one's documents.
            if method != "POST":
                raise self._wrong_method(method, "POST")
            return self.retry(parts[1], who)
        if len(parts) == 3 and parts[0] == "runs":
            # `events` never reaches here on a GET: `server.py` recognises the
            # suffix and calls `stream()`, because a stream is written to the
            # socket frame by frame and a `Response` is written once. Any other
            # method on it is an ordinary method error, which is why the suffix
            # is named here at all rather than left to fall through to a 404
            # that would tell the caller the route does not exist.
            # `report.html` is the file and `report` is the page that shows it
            # -- two routes because they are two things, not one thing served
            # twice: the file must be safe to keep and mail on, so it carries
            # no link to this server, and the page carries exactly one.
            served = {"merged": self.merged, REPORT_HTML: self.report_html,
                      "report": self.report_page, BUNDLE_ZIP: self.bundle,
                      "events": None}
            if parts[2] in served:
                if method != "GET" or served[parts[2]] is None:
                    raise self._wrong_method(method, "GET")
                return served[parts[2]](parts[1], who)
        raise ApiError(404, "no_route",
                       f"{method} {path} is not a route this API defines.")

    def _under_prefix(self, path: str) -> tuple[str, ...]:
        """The path segments below `/api/v1/`, or a 404 for anything else."""
        parts = self._segments(path)
        if parts is None:
            raise ApiError(404, "no_route", f"{path} is not under {API_PREFIX}/.")
        return parts

    @staticmethod
    def _segments(path: str):
        """The same split, answering `None` instead of raising. For `check_access`.

        The access check has to run **before** the 404, or an unauthenticated
        caller learns which paths exist by reading which ones answer `no_route`
        -- and it has to know which route was asked for, because two of them
        answer without an identity. A raising split would force the order the
        other way round, so this is the non-raising one and `_under_prefix` is
        the raising one built on it.
        """
        if path != API_PREFIX and not path.startswith(API_PREFIX + "/"):
            return None
        return tuple(part for part in path[len(API_PREFIX):].split("/") if part)

    @staticmethod
    def _wrong_method(method: str, allowed: str) -> ApiError:
        return ApiError(405, "wrong_method",
                        f"{method} is not allowed here; this route takes {allowed}.")

    # -- logging in ------------------------------------------------------

    def session_state(self, headers) -> dict:
        """Am I logged in, and does this server need setting up. No credential.

        Open on purpose and the only route that says anything before a
        password: a page cannot know whether to draw a login form, a setup
        form or the tool itself without being told, and every other way of
        telling it -- a 401 it has to provoke, a flag baked into the HTML --
        is either a guess or a second place the answer is written.

        What it discloses is whether this server has accounts, which is the
        same thing the login form itself discloses by existing. It does not
        disclose who they are: `accounts` is a boolean and not a list, and the
        list is behind the operator's own route.
        """
        who = self.principal(headers) if self.tenanted else None
        return {
            "api": API_VERSION,
            "version": __version__,
            "tenanted": self.tenanted,
            "setup_required": self.tenanted and self.account_count() == 0,
            "authenticated": who is not None,
            "user": who.describe() if who is not None else None,
        }

    def log_in(self, body: bytes, headers) -> Response:
        """A username and a password for a session. 200, a cookie, and a user.

        **One refusal for an unknown name, a wrong password and a throttled
        name**, with one status and one sentence. `Accounts.verify` makes the
        first two take the same time; this makes them say the same thing; and
        `accounts.Throttle` is folded in here rather than answering 429,
        because a distinct answer for "too many attempts" is a distinct answer
        about a name, which is the enumeration this is all written to prevent.

        The session id is set as an `HttpOnly` cookie and is **not** in the
        body unless the caller asked for it. A browser never needs to see it
        -- that is what `HttpOnly` is -- and a page that could read it is a
        page an injected script could read it from. A script has no cookie jar
        it did not build itself, so it asks with `"token": true` and presents
        what it gets in a header; that is one field with one reason, rather
        than a second credential type with a second lifetime.
        """
        check_content_type(headers)
        payload = _json_object(body)
        unknown = sorted(set(payload) - {"username", "password", "token"})
        if unknown:
            raise ApiError(400, "unknown_field",
                           f"this request sets {', '.join(unknown)}; a login "
                           f"is an object with a username and a password.")
        if not self.tenanted or self.account_count() == 0:
            raise ApiError(
                409, "no_accounts",
                "this server has no accounts, so there is nothing to log in "
                "to. The line it printed when it started carries a one-time "
                "address that creates the first one.")
        name = payload.get("username")
        name = name.strip().lower() if isinstance(name, str) else ""
        if len(name) > user_accounts.USERNAME_MAX:
            # No account's name, so it is not kept: the throttle is keyed on
            # the submitted name and would hold a megabyte of one for five
            # minutes for anybody who posted it. Counted and answered as the
            # one name that is nobody's, the empty one, which takes the same
            # time and gets the same refusal as any wrong sign-in.
            name = ""
        record = None
        if not self.throttle.locked(name):
            record = self.accounts.verify(name, payload.get("password"))
        if record is None:
            self.throttle.failed(name)
            # The message names nothing that was submitted. A refusal that
            # quoted the username back would put it in a proxy log beside the
            # request that carried the password.
            raise ApiError(401, "bad_login",
                           "that username and password do not match an account "
                           "on this server.")
        self.throttle.succeeded(name)
        session_id = self.sessions.new(record.id)
        wants_token = payload.get("token") is True
        answer = {"user": record.describe(),
                  "expires_in": self.sessions.idle_seconds}
        if wants_token:
            answer["token"] = session_id
        return Response(200, dump(answer), headers=(
            ("Set-Cookie", user_accounts.cookie(
                session_id, secure=self.over_tls(headers),
                max_age=self.sessions.idle_seconds)),
        ))

    def log_out(self, headers) -> Response:
        """End this session. 204, and 204 again if there was none.

        Idempotent for the reason `delete` is, and the cookie is cleared
        either way: a client that got a dropped connection on its first
        attempt must not be told the second failed, and a browser holding a
        cookie for a session this server has already forgotten should stop
        sending it.
        """
        for session_id in self.session_ids(headers):
            self.sessions.revoke(session_id)
        return Response(204, b"", content_type=JSON_TYPE, headers=(
            ("Set-Cookie",
             user_accounts.expired_cookie(secure=self.over_tls(headers))),
        ))

    def first_account(self, body: bytes, headers) -> Response:
        """The one-time setup route. Creates the operator, then logs them in.

        **Only while there are no accounts, and only with the token this
        server printed.** Both halves are checked here and not by
        `check_access`, because the route is open by design -- it is how a
        server that refuses everything else stops doing so -- and a route that
        is open has to carry its own gate.

        The account it creates is the operator's, which is a statement about
        the *shared* credentials file rather than a permission level: whoever
        set this server up owns the endpoints everybody can reach, and
        everyone else owns their own. See `accounts.Directory`.

        **The migration is a sentence, not a copy.** An upgrade from a
        single-tenant server already has a `credentials.json` full of keys, and
        it does not move: it becomes the operator's, which is exactly what it
        already was, and from here it is the set of endpoints shared with every
        later account. The answer says so, because a tool that silently
        re-owned an operator's credentials would be a tool whose upgrade notes
        were the only place that happened.
        """
        check_content_type(headers)
        payload = _json_object(body)
        unknown = sorted(set(payload) - {"token", "username", "password"})
        if unknown:
            raise ApiError(400, "unknown_field",
                           f"this request sets {', '.join(unknown)}; setup is "
                           f"an object with a token, a username and a password.")
        if not self.tenanted:
            raise ApiError(409, "no_account_store",
                           "this server was started without an account store, "
                           "so it has nothing to set up.")
        if self.account_count() > 0:
            # 409 and not 403: the state on disk is what refuses this, the
            # request is well formed, and retrying will not help.
            raise ApiError(409, "already_set_up",
                           "this server already has an account on it. The "
                           "setup address works once, and once only.")
        if not self.setup.matches(payload.get("token")):
            raise ApiError(403, "bad_setup_token",
                           "that is not the setup address this server printed "
                           "when it started. It is a new one on every start.")
        try:
            # `first`: only into an empty store, decided under the store's
            # own lock. The count above is the quick refusal; two requests
            # that both passed it used to make two operators.
            record = self.accounts.create(
                payload.get("username"), payload.get("password"),
                operator=True, first=True)
        except user_accounts.AlreadySetUp as refusal:
            raise ApiError(409, "already_set_up", str(refusal)) from None
        session_id = self.sessions.new(record.id)
        shared = getattr(self.keys, "path", None)
        return Response(200, dump({
            "user": record.describe(),
            # What happened to whatever was already configured. Named, because
            # the alternative is an operator wondering whether their keys
            # survived the upgrade and finding out by running a merge.
            "migrated": {
                "credentials": str(shared) if shared is not None else "",
                "note": "The keys and endpoints already on this server are "
                        "yours, and are the ones every other account shares. "
                        "Anyone else who signs in configures their own.",
            },
        }), headers=(
            ("Set-Cookie", user_accounts.cookie(
                session_id, secure=self.over_tls(headers),
                max_age=self.sessions.idle_seconds)),
        ))

    # -- the accounts ----------------------------------------------------

    def _account_route(self, method: str, parts, body: bytes, headers,
                       who) -> Response:
        """`/accounts`, `/accounts/{name}` and `/accounts/{name}/password`.

        Split out of `_route` because the permission rule here is not the one
        the rest of the API has: three of the four are the operator's alone,
        and the fourth is "the operator, or you about yourself". Inlining that
        would put a second access decision in the middle of a dispatch table,
        which is the shape where one branch ends up not having it.
        """
        if not self.tenanted:
            # 404 with a code of its own rather than `no_route`. The route is
            # one this API defines and this server does not mount, which is a
            # different answer to a client than "no such path" -- and a page
            # that enumerates the contract has to be able to tell the two
            # apart in order to render the second as a state.
            raise ApiError(404, "no_account_store",
                           "this server has no account store, so it has no "
                           "accounts to manage.")
        if parts == ("accounts",):
            if method == "GET":
                self._operator(who)
                return Response(200, dump(
                    {"accounts": [record.describe() for record in
                                  sorted(self.accounts.read().values(),
                                         key=lambda row: row.username)]}))
            if method == "POST":
                return self.add_account(body, headers, who)
            raise self._wrong_method(method, "GET, POST")
        if len(parts) == 2:
            if method == "DELETE":
                return self.remove_account(parts[1], who)
            raise self._wrong_method(method, "DELETE")
        if len(parts) == 3 and parts[2] == "password":
            if method == "PUT":
                return self.change_password(parts[1], body, headers, who)
            raise self._wrong_method(method, "PUT")
        raise ApiError(404, "no_route",
                       f"{'/'.join(parts)} is not a route this API defines.")

    def add_account(self, body: bytes, headers, who) -> Response:
        """The operator adds somebody. 201, and never a password back.

        The new account starts with no credentials of its own at all, which is
        the point of the arrangement rather than an omission: they can use
        whatever endpoints the operator put up, and anything they add is
        theirs. Nobody is issued somebody else's key by being issued an
        account.
        """
        self._operator(who)
        check_content_type(headers)
        payload = _json_object(body)
        unknown = sorted(set(payload) - {"username", "password", "operator"})
        if unknown:
            raise ApiError(400, "unknown_field",
                           f"this request sets {', '.join(unknown)}; an "
                           f"account is a username and a password.")
        record = self.accounts.create(payload.get("username"),
                                      payload.get("password"),
                                      operator=payload.get("operator") is True)
        return Response(201, dump({"user": record.describe()}))

    def remove_account(self, name: str, who) -> Response:
        """The operator removes somebody, and their credentials go with them.

        204 whether or not there was one, for the reason `delete` is
        idempotent. The private credentials file is deleted as part of it, not
        left behind: a vendor key belonging to an account that no longer
        exists is a key nobody can reach and nobody can rotate, and the person
        whose key it is asked for it to be gone.

        Their sessions are revoked in the same breath. An account deleted
        while its owner has a browser open would otherwise go on working until
        the cookie expired -- `principal` would answer None, so nothing would
        actually be *served*, but the revocation is the statement rather than
        the side effect.
        """
        self._operator(who)
        record = self.accounts.remove(name)
        if record is not None:
            self.sessions.revoke_account(record.id)
            # And their runs, queued and running. Left alone they all ran
            # to the end after the removal, as a member with nothing of
            # their own, which is on the operator's key, where the operator
            # could neither see nor cancel them. After the sessions, so no
            # new run arrives behind this; one that does is refused when it
            # starts (`accounts.Directory.for_run`).
            self.store.cancel_owned(record.id)
            self.directory.forget(record)
        return Response(204, b"", content_type=JSON_TYPE)

    def change_password(self, name: str, body: bytes, headers, who) -> Response:
        """A new password: the operator for anybody, or you for yourself.

        **Your own change needs the current one**, and the operator's reset
        does not. The two are different acts: a reset is for the person who
        cannot log in, and demanding the password they have lost would make
        the feature useless; a self-service change is for a browser somebody
        may have walked away from, and the current password is what says the
        person at the keyboard is the owner.

        Every session belonging to the account is revoked, including the one
        making the request. A password changed because it may have leaked has
        bought nothing while the session opened with the old one is still
        live, and that is the whole reason this is not just a file write.
        """
        check_content_type(headers)
        payload = _json_object(body)
        unknown = sorted(set(payload) - {"password", "current"})
        if unknown:
            raise ApiError(400, "unknown_field",
                           f"this request sets {', '.join(unknown)}; a "
                           f"password change carries a password, and your own "
                           f"also carries the current one.")
        wanted = user_accounts.check_username(name)
        mine = who is not None and who.username == wanted
        if not mine:
            self._operator(who)
        else:
            # Under the sign-in throttle, by the same name. A session is not
            # the password: somebody at an unattended browser could otherwise
            # try the current one as fast as the hash allows. A throttled
            # name is refused in the words a wrong password is.
            known = (None if self.throttle.locked(wanted)
                     else self.accounts.verify(wanted, payload.get("current")))
            if known is None:
                self.throttle.failed(wanted)
                raise ApiError(403, "bad_current_password",
                               "the current password does not match. A password "
                               "is changed by somebody who can already give it.")
            self.throttle.succeeded(wanted)
        if self.accounts.get(wanted) is None:
            raise ApiError(404, "no_account",
                           f"there is no account called {wanted}.")
        record = self.accounts.set_password(wanted, payload.get("password"))
        self.sessions.revoke_account(record.id)
        return Response(204, b"", content_type=JSON_TYPE, headers=(
            ("Set-Cookie",
             user_accounts.expired_cookie(secure=self.over_tls(headers))),
        ) if mine else ())

    # -- whose settings --------------------------------------------------

    def environ_for(self, who) -> dict:
        """The server's environment with this account's own addresses over it.

        Addresses and model listings only. A key never goes in here -- this
        mapping is copied into a job, merged with a request's overrides and
        read by anything that resolves settings, and a key in a dict that
        travels that far is a key in the next thing that dumps one. Keys go
        through `keys_for` and `config.keys_for_this_run`.
        """
        if who is None or self.directory is None:
            return self.environ
        return {**self.environ, **self.directory.environ_for(who.id)}

    def keys_for(self, who):
        """What this account's runs read credentials from, or `None` for nobody.

        `None` means "do not swap the source", which is `os.environ` and is
        the single-tenant server. See `accounts.Directory.keys_for`: `None`
        and `{}` are different statements, and the difference is a user being
        handed the operator's credential.
        """
        if who is None or self.directory is None:
            return None
        return self.directory.keys_for(who.id, os.environ)

    # -- the routes themselves -------------------------------------------

    def health(self, who=None) -> dict:
        """Is this thing running, what is it, and what credentials does it hold.

        Deliberately answerable without touching the job store's lock or the
        filesystem: this is the endpoint a supervisor polls, and a health check
        that blocks behind whatever a worker thread is holding reports the
        server as down at exactly the moment it is busy.
        """
        return {
            "api": API_VERSION,
            "version": __version__,
            "status": "ok",
            "providers": providers(self.environ_for(who),
                                   keys=self.keys_for(who)),
            # Who this server thinks is asking, so a page that has one request
            # in flight does not need a second to find out. `None` on a server
            # with no account store, which is the single-tenant arrangement.
            "user": who.describe() if who is not None else None,
        }

    def _effort_chosen(self) -> dict[str, str]:
        """This server's own `LLOSSLESS_EFFORT*`, role -> level, or nothing.

        An unreadable value is nothing here rather than a 500: every run on
        this server refuses on it with `config`'s own message, and the picker
        is where an operator goes to find that out.
        """
        environ = getattr(self.store, "environ", None) or {}
        try:
            return config.effort_from_env(environ)
        except config.ConfigError:
            return {}

    def config(self, who=None) -> dict:
        """Everything a picker needs before the operator commits a document.

        The catalogue is served whole rather than filtered down to the fields a
        picker is expected to render. `catalogue.load` already validated it, the
        file is small, and a server that decided which of the measured figures
        were interesting would be the place a future field went missing without
        anybody editing a renderer.
        """
        try:
            models = catalogue.load(self.catalogue_path)
        except (OSError, ValueError) as exc:
            raise ApiError(500, "bad_catalogue",
                           f"the model catalogue could not be read: {exc}") from None
        return {
            "api": API_VERSION,
            "version": __version__,
            "fidelity": {
                "default": config.DEFAULT_FIDELITY,
                "levels": fidelity_levels(),
            },
            "verify_depth": {
                "default": config.DEFAULT_VERIFY_DEPTH,
                "depths": verify_depths(),
                # Stated as a field rather than left for the page to know, and
                # read by `renderDepthDelta` rather than mirrored in a static
                # sentence: a served field no surface reads is one that can go
                # out of step with the page in silence.
                #
                # The catalogue's `verify_depth` block, which `catalogue.load`
                # has already validated with its run, artefacts and derived_by:
                # the 2026-09-24 re-run, K = 1, one model, 13 fixtures,
                # with the comparator's registered conditions met. Served
                # whole, like the catalogue itself, so the page renders the
                # figures the loader checked rather than a copy of them.
                #
                # "unmeasured" when the catalogue carries no block -- a fork's
                # own catalogue, or one written before the benchmark -- and
                # never a zero or a blank in its place: a page that filled the
                # gap would be answering "how much worse is the cheap one"
                # with nothing measured behind the answer.
                "quality_delta": models.get("verify_depth") or "unmeasured",
            },
            "title_policy": {
                "default": config.DEFAULT_TITLE_POLICY,
                "policies": title_policies(),
            },
            "loss_budget": {"default": config.DEFAULT_DECLARED_LOSS_BUDGET},
            "catalogue": models,
            # Which languages exist and which one an unknown browser gets.
            # The strings themselves are not here: a page reads `/config`
            # before it knows which language it wants, and carrying every
            # catalogue in it would make one page load fetch every
            # translation this server has in order to render one of them.
            "locales": {
                "default": i18n.DEFAULT_TAG,
                "available": i18n.describe(),
            },
            "limits": {
                "min_documents": merge.MIN_SOURCES,
                "max_documents": merge.MAX_SOURCES,
                "max_body_bytes": MAX_BODY_BYTES,
                "max_label": LABEL_MAX,
                # The bounds on a stated window, so the page refuses
                # the figure the server would refuse, in the same terms.
                "min_window": STATED_WINDOW_MIN,
                "max_window": STATED_WINDOW_MAX,
            },
            # How long this server keeps a finished run, and how long before
            # that a reader should be told. Served rather than written into the
            # page, because it is this server's setting and not this tool's: a
            # page carrying "deleted after an hour" would be wrong on every
            # deployment that passed `--retention`, and wrong silently.
            #
            # `null` seconds is `--retention 0`, which is not a large number --
            # "kept until you delete them" is a different sentence, and the
            # page renders it as one rather than as an enormous countdown.
            "retention": {
                "seconds": self.store.retention_seconds,
                "warn_seconds": retention_warning_seconds(
                    self.store.retention_seconds),
            },
            # Which settings a `POST /runs` body may carry, for a client
            # that is not this page. Deliberately unread by `app.js`:
            # this page knows its own form and would learn nothing from being
            # told, and a control built from this list would be a control with
            # no label and no explanation. It is here because `/api/v1/` is
            # versioned as a contract a second implementation can satisfy, and
            # "which keys are accepted" is the one thing a client cannot
            # discover by trying -- an unknown key is refused rather than
            # ignored, on purpose, so guessing costs a 400 per guess.
            "settable": sorted(SETTINGS_FIELDS),
            # The command routes this operator configured, **by id and label
            # and never by command**. A command is a local path as often as
            # not, and the release scan checks the published set
            # for exactly that shape; there is no route on this server that
            # returns the string, and `tests/test_web_commands.py` asserts it
            # is absent from this payload, from a report and from the HTML
            # download rather than leaving that to this comment.
            #
            # An empty list is the default and is what a server without a
            # commands file serves. The page then offers no command backend at
            # all, which is the right thing for a capability that runs a
            # program.
            "commands": {
                # Each route's merge effort levels and default come with it;
                # the default reads this server's own
                # `LLOSSLESS_EFFORT*`, so it is what a request naming no level
                # gets.
                "routes": self.routes.describe(self._effort_chosen()),
                # What every route on this server is, said once rather than per
                # row because it is a property of the mechanism. A command runs
                # as the server process with that machine's credentials, so on
                # a shared instance everybody shares one subscription and one
                # rate limit -- unlike an API key, which `keys_for_this_run`
                # keeps per account.
                "per_user": False,
                # What this server found on its own `PATH`, from the closed
                # table in `commands.KNOWN_TOOLS`. Four facts per row and
                # **never the resolved path**: that is an absolute path under
                # whichever account the server runs as, which is the shape
                # the release scan refuses and the one that
                # already caught this feature once.
                #
                # Served to every reader rather than to the operator alone.
                # Which CLIs exist on a machine everybody here already sends
                # documents to is not a secret worth a second contract, and a
                # panel that renders for one account and is blank for the rest
                # is how a feature gets lost again. What is gated is the
                # *change*: `editable` says whether this caller may make one,
                # the same field `endpoints` already carries per row.
                "discovered": self.routes.discovered(),
                # The rows in that file this build could not use, each with
                # the sentence that says why and the id it concerns. Served so
                # a page can put the problem next to the row instead of
                # rendering a wall of text where the picker should be, which
                # is the failure this answers.
                #
                # Through `redact.text` for the reason `ApiError` goes through
                # it: the message names the commands file, which is an
                # absolute path under the account this server runs as. It is
                # the same scrub, so the two cannot drift.
                "problems": [
                    {**bad.described(),
                     "reason": redact.text(bad.reason,
                                           extra=self.roots_for(who))}
                    for bad in self._route_problems()],
                # Which rows `Commands.migrate` retired at startup. A route the
                # operator had switched on is gone from the picker, and a
                # feature that vanishes without a sentence is how this one was
                # lost the first time. Ids only: the page owns the wording.
                "retired": list(getattr(self.routes, "retired", ()) or ()),
                "editable": who is None or bool(getattr(who, "operator", False)),
                # Can anything be switched on here at all? False for a server
                # built with no store, where there is nowhere to write a route
                # -- which is a different sentence to "nothing was found", and
                # a page that ran the two together would show an empty panel
                # with no explanation. That is exactly how the operator lost
                # this feature the first time.
                "configurable": bool(getattr(self.routes, "writable", False)),
            },
            # Which endpoints exist, so the picker can say what is reachable
            # before a document is committed to it rather than after. A model
            # whose provider has no endpoint here cannot be run on this server
            # at all, and a picker that offered it anyway would be offering a
            # failure two steps into a forty-minute wait.
            "endpoints": self.endpoints(who),
        }

    def _route_problems(self) -> tuple:
        """The rows of the commands file this build could not use, or nothing.

        An unreadable *file* answers with nothing here rather than raising,
        which is `Commands.describe`'s rule one call over: a settings sheet
        that will not render is a worse answer than one with an empty panel,
        and `serve`'s banner and every write path still report it.
        """
        try:
            return tuple(self.routes.problems())
        except commands.CommandsError:
            return ()
        except AttributeError:  # pragma: no cover - a store from before this
            return ()

    def endpoints(self, who=None) -> dict:
        """Where this server can send a model, and what each address serves.

        The address and never the key, the same rule `list_keys` follows. What
        is added here beyond that route is the *default* endpoint -- the one a
        model this catalogue has never heard of goes to -- because the page has
        a free-text model field and "which endpoint will this be sent to" is
        the question an operator typing into it is entitled to have answered
        before they press the button.

        `banner_endpoint` rather than `base_url`: scheme, host and port, with
        no userinfo and no path. It is the same string a run's own opening
        event carries, chosen there because a URL holds more than an address --
        userinfo is a credential and a path or a query can carry a pasted
        token.

        The endpoints are editable on every deployment, so there is no flag
        here saying whether they are. That was built and removed: it gated the
        capability on whether a bind token was set, which answered a threat
        this tool does not model -- everyone who can reach this server shares
        one set of credentials by design -- at the cost of the freedom the
        page exists to offer.
        """
        environ = self.environ_for(who)
        settings = config.from_env(environ)
        rows = []
        for row in self.directory.rows_for(who, environ=environ):
            rows.append({
                "name": row["name"],
                "base_url": row["base_url"],
                "configured": row["endpoint_configured"],
                "key_configured": row["configured"],
                "url_variable": row["url_variable"],
                "models": row["models"],
                # Whose row this is, and whether this account may change it.
                # A page that offered an edit the server answers 403 to would
                # be a page that has to explain a refusal after the fact.
                "owner": row["owner"],
                "editable": row["editable"],
                # Local, metered, or not classifiable. The submit button names
                # the route the click takes, and a typed model goes to one of
                # these rows -- so the row has to carry which kind of
                # destination it is. Answered here rather than on the page for
                # `verify_depths`' reason and one more: whether an address is
                # on this network is a question about the address, and the
                # page has no vocabulary for it.
                "kind": discover.kind_of(row["base_url"]),
                # Whether a model the catalogue does not know needs its window
                # stated to run here: true for a vendor, which cannot
                # report one, unless this server states one for every role.
                # The page makes its "Context window" field required on it,
                # and `endpoint_plan` refuses on the same predicate.
                "window_required": window_unreportable(row["name"], environ),
            })
        return {
            "providers": rows,
            "default": settings.banner_endpoint,
            # The same question about the endpoint a request that names none
            # falls to. This was the hole the label had: a typed model with no
            # endpoint chosen read as `metered API` whatever the server's own
            # default was, so an operator pointed at a local ollama was told
            # their run would bill per token.
            "default_kind": discover.kind_of(settings.base_url),
        }

    # -- saved defaults ----------------------------------------------------

    def offer(self, who=None) -> defaults.Offer:
        """What this server offers this caller now, for checking saved defaults.

        Built from the same sources `/config` serves the picker from -- the
        catalogue, the command routes, this caller's endpoints and `config`'s
        enumerations -- so a value the page could pick is a value this
        accepts, and one the picker no longer offers is one this refuses.
        """
        try:
            models = catalogue.load(self.catalogue_path)
        except (OSError, ValueError) as exc:
            raise ApiError(500, "bad_catalogue",
                           f"the model catalogue could not be read: {exc}") from None
        rows = self.endpoints(who)["providers"]
        configured = {row["name"] for row in rows if row["configured"]}
        routes = {}
        single_level_routes = set()
        for route in self.routes.describe(self._effort_chosen()):
            effort = route.get("effort") or {}
            routes[str(route["id"])] = tuple(effort.get("levels") or ())
            if effort.get("single_level"):
                single_level_routes.add(str(route["id"]))
        return defaults.Offer(
            routes=routes,
            single_level_routes=frozenset(single_level_routes),
            catalogue=frozenset(
                str(model["id"]) for model in models.get("models") or ()
                if not (model.get("retired") or {}).get("on")
                and (not model.get("provider") or model["provider"] in configured)),
            listed={row["name"]: frozenset(row["models"] or ())
                    for row in rows if row["configured"]},
            providers=frozenset(configured),
            fidelity=tuple(level["value"] for level in fidelity_levels()),
            depths=tuple(config.VERIFY_DEPTHS),
            titles=tuple(config.TITLE_POLICIES),
            window_min=STATED_WINDOW_MIN, window_max=STATED_WINDOW_MAX)

    def defaults_store(self, who=None) -> defaults.Store:
        """This caller's defaults file, named by who they are and nothing else."""
        return defaults.Store(self.directory.defaults_path(who, defaults.FILE_NAME))

    def get_defaults(self, who=None) -> dict:
        """The caller's saved settings that this server still offers, and the rest.

        `dropped` names each saved value that is no longer offered -- a model
        gone from an endpoint, a level removed -- so the page can say so in one
        line instead of quietly starting from something else. The file is not
        rewritten: a model that is back tomorrow is used again tomorrow.
        """
        try:
            stored = self.defaults_store(who).read()
        except defaults.DefaultsError as refusal:
            raise ApiError(409, "bad_defaults", str(refusal)) from None
        if stored is None:
            return {"saved": False, "defaults": {}, "dropped": []}
        kept, dropped = defaults.sift(stored, self.offer(who))
        return {"saved": True, "defaults": kept, "dropped": dropped}

    def put_defaults(self, body: bytes, headers, who=None) -> Response:
        """Save the caller's settings, every field checked against this server.

        JSON only, for `check_content_type`'s reason, and `handle` has already
        held the `Origin` to the `Host`: a cross-site page cannot make this
        request without a preflight, and the session cookie is `SameSite=Strict`.
        Answers with what was stored, which is the request in its clean form.
        """
        check_content_type(headers)
        if len(body) > defaults.MAX_BYTES:
            raise ApiError(413, "body_too_large",
                           f"saved defaults are at most {defaults.MAX_BYTES} "
                           f"bytes; this request carried {len(body)}.")
        payload = _json_object(body)
        try:
            clean = defaults.check(payload, self.offer(who))
            self.defaults_store(who).write(clean)
        except defaults.Refused as refusal:
            raise ApiError(400, "bad_defaults", str(refusal)) from None
        return Response(200, dump({"saved": True, "defaults": clean, "dropped": []}))

    def delete_defaults(self, who=None) -> Response:
        """Forget the caller's saved settings. 204 whether or not there were any."""
        self.defaults_store(who).remove()
        return Response(204, b"", content_type=JSON_TYPE)

    # -- the strings -----------------------------------------------------

    def locale(self, tag: str, headers) -> dict:
        """One language's whole catalogue, plus the list the picker renders.

        `tag` empty means "you decide", and the decision is `Accept-Language`
        falling back to English. An explicit tag is honoured whatever the
        header says -- the operator choosing German on an English-configured
        browser is the case that has to work, and it is the only one where the
        two disagree on purpose.

        **An unknown tag is a 404 and never a quiet English answer.** A page
        that asked for `de` and was handed `en` under a `"tag": "de"` it
        believed would render English text under a German picker and leave the
        operator hunting for a translation that was never installed. The
        refusal is what makes the page's own fallback -- ask again with no tag
        -- a decision it took rather than one taken for it.

        The `available` list rides along with the catalogue rather than being
        a second request, because a picker with no options is not a picker,
        and the page has to have both before it renders anything at all.
        """
        try:
            data = i18n.load(tag) if tag else i18n.load(
                i18n.negotiate(header(headers, "Accept-Language")))
        except i18n.InvalidLocale as refusal:
            # 404 rather than 400: a tag this server does not have is a
            # resource that is not here, and a client that sent a perfectly
            # well-formed request for a language nobody installed has not made
            # a mistake it can fix by rewriting the request.
            raise ApiError(404, "no_locale", str(refusal)) from None
        return {
            "api": API_VERSION,
            "tag": data["tag"],
            "label": data["label"],
            "default": i18n.DEFAULT_TAG,
            "available": i18n.describe(),
            "strings": data["strings"],
        }

    # -- the credentials -------------------------------------------------

    def list_keys(self, who=None) -> dict:
        """Which providers have a key in effect, and four characters of each.

        No endpoint on this server returns a key, and this is the one an
        auditor will check first, so it is worth saying what it does return
        instead. `configured` is a boolean. `suffix` is the last four
        characters and is absent entirely when nothing is configured, so a
        client has nothing to render when there is nothing to say. It is
        also absent from a shared row when a member asks: the four characters
        go to the account that owns the key (`accounts.Directory.rows_for`).

        The *variable* is reported, and that is not an oversight for the same
        reason it is not one on `/health`: `config.py`'s own docstring says a
        name is not a secret, and without it an operator whose page reads
        `configured: false` has no way to find out which variable was looked
        at. What is never reported is a value, and there is no route here that
        takes a variable name and answers anything about it.
        """
        # Each row with the address the page may offer for it: the
        # provider's well-known one, or an example for the field's
        # placeholder. An offer, not a setting -- `base_url` and
        # `endpoint_configured` still say only what is stored.
        return {"providers": [
            dict(row, preset_url=credentials.PRESET_URLS.get(row["name"], ""),
                 example_url=credentials.EXAMPLE_URLS.get(row["name"], ""))
            for row in self.directory.rows_for(who, environ=os.environ)]}

    def set_key(self, name: str, body: bytes, headers, who=None) -> Response:
        """Write one provider's key and load it. 204, because there is nothing to say.

        204 and not the row that `list_keys` would return: the only thing this
        could add to the answer is four characters of the key that was just
        submitted, told back to the client that submitted it, and a response
        body that carries part of a credential is a response body in somebody's
        proxy log.
        """
        check_content_type(headers)
        payload = _json_object(body)
        unknown = sorted(set(payload) - {"key"})
        if unknown:
            raise ApiError(400, "unknown_field",
                           f"this request sets {', '.join(unknown)}; the body "
                           f"of a key is an object with one field, `key`.")
        if "key" not in payload:
            raise ApiError(400, "no_key",
                           "the body of a key must carry a `key` field.")
        provider = self._provider(name)
        # Validated here rather than left to `Credentials.set`, so that a key
        # which is not one is a 400 about this request and not the 409 that
        # `handle` turns every other `CredentialsError` into. The two are
        # different answers: 409 says the state on disk is wrong and retrying
        # will not help, and this says the body was.
        try:
            key = credentials.clean_key(payload["key"])
        except credentials.CredentialsError as refusal:
            raise ApiError(400, "bad_key", str(refusal)) from None
        self._key_store_for(who, provider).set(provider, key)
        self._reload_keys(who)
        return Response(204, b"", content_type=JSON_TYPE)

    def set_endpoint(self, name: str, body: bytes, headers, who=None) -> Response:
        """Point one provider at an address, then ask that address what it serves.

        **The key stored against this provider does not survive, by
        construction.** `Credentials.set_endpoint` goes through
        `Endpoint.moved_to`, which is the only way an address changes and
        returns a pair with no key in it. The rule it enforces is that no key
        is ever sent to an endpoint it was not stored against: whoever moves an
        endpoint brings their own credential, so moving one cannot be a way to
        spend somebody else's.

        **Available on every deployment**, and deliberately not gated on how
        the server was bound. `llossless merge --base-url X --model Y`
        switches both with two flags, and a page that made the same change a
        configuration exercise would be friction against the thing it exists
        for: trying models out. A gate on the bind address was written here
        and removed for that reason.

        The answer carries the listing, because the operator asked for an
        endpoint and what they want to know is which models they can now pick.
        A failed listing is a 200 with an empty list and a sentence: an
        endpoint that will not enumerate is still an endpoint, and refusing the
        configuration over it would make a discovery convenience into a
        requirement.
        """
        check_content_type(headers)
        payload = _json_object(body)
        unknown = sorted(set(payload) - {"base_url"})
        if unknown:
            raise ApiError(400, "unknown_field",
                           f"this request sets {', '.join(unknown)}; the body "
                           f"of an endpoint is an object with one field, "
                           f"`base_url`.")
        if "base_url" not in payload:
            raise ApiError(400, "no_base_url",
                           "the body of an endpoint must carry a `base_url` "
                           "field.")
        provider = self._provider(name)
        store = self._store_for(who)
        try:
            # Under the keys that could be sent to this address, not the
            # process's. `clean_base_url` runs `config.check_cleartext_key`,
            # whose whole question is whether *the key that would actually be
            # sent* goes on the wire unencrypted. For a member that is a key
            # of their own and never the operator's: the operator's key is
            # not sent to an address a member stored, so it must not decide
            # whether the member may store one.
            with self._as_owner(who):
                stored = store.set_endpoint(provider, payload["base_url"])
        except credentials.CleartextKey as refusal:
            raise ApiError(400, "bad_endpoint",
                           self._cleartext_refusal(who, provider, refusal)
                           ) from None
        except credentials.CredentialsError as refusal:
            raise ApiError(400, "bad_endpoint", str(refusal)) from None
        found, note = discover.models(
            stored.base_url, api_key=None,
            ca_bundle=config.from_env(self.environ_for(who)).ca_bundle)
        store.set_models(provider, found)
        self._reload_keys(who)
        return Response(200, dump({"name": provider,
                                   "base_url": stored.base_url,
                                   "models": found,
                                   "listed": bool(found),
                                   "note": note}))

    def delete_endpoint(self, name: str, who=None) -> Response:
        """Forget one provider's endpoint, its key and its listing. 204, always.

        The whole row, not the address alone. A key kept behind an address that
        has been deleted is a credential with no recorded destination, which is
        the state the pairing exists to make unreachable -- and
        `Credentials._row` refuses to read one back, so keeping it would write
        a file this build cannot load.
        """
        provider = self._provider(name)
        self._store_for(who).remove_endpoint(provider)
        self._reload_keys(who)
        return Response(204, b"", content_type=JSON_TYPE)

    def delete_key(self, name: str, who=None) -> Response:
        """Forget one provider's key. 204, and 204 again if there was none.

        Idempotent for the reason `delete` is: the operator asked for the key
        to be gone and it is gone, and a client retrying after a dropped
        connection should not be told its first attempt failed.
        """
        provider = self._provider(name)
        self._store_for(who).remove(provider)
        self._reload_keys(who)
        return Response(204, b"", content_type=JSON_TYPE)

    def enable_command(self, name: str, who=None) -> Response:
        """Switch one discovered tool on. **The id is all the caller supplies.**

        This is the route the operator asked for -- *"can this also be done in
        the WebUI (preferably)?"* -- and it is also the route that must not
        become a way to name a program. It takes a path segment, hands it
        straight to `commands.check_tool_id`, and what comes back is a
        `(KnownTool, ToolModel)` pair out of `commands.KNOWN_TOOLS`. The
        command written into the allowlist is whatever `shutil.which`
        resolved for that tool's program name followed by the argv the
        table wrote to pin the model, on the server, in `commands.py`. There is no body, which is not an oversight:
        a body is a place a field could be added, and every field this route
        could accept would be a string reaching a command line.

        Operator-only, because a command route is shared by everybody with an
        account here -- it runs as the server process with that machine's
        credentials, which is the first of the three sentences the page says
        out loud. `_operator` is the same gate `accounts` uses.

        The answer says the state rather than echoing the request, so a second
        tab that toggled the other way is corrected by the reply it gets.
        """
        self._operator(who)
        try:
            model = self.routes.enable(name)
        except commands.UnknownRoute as refusal:
            # Includes `UnknownTool`, which is a subclass. A 400 about the
            # request, not a 404 about the path: the route exists and the id in
            # it is not one this build recognises.
            raise ApiError(400, "bad_command_tool", str(refusal)) from None
        except commands.CommandsError as refusal:
            # The tool is not there, or the file cannot be written, or the id
            # is the operator's own. All three are facts about this server's
            # state rather than about the request, which is the 409 `submit`
            # already gives an unusable commands file.
            raise ApiError(409, "commands_unusable", str(refusal)) from None
        return Response(200, dump({"id": model.id, "label": model.label,
                                   "model": model.model, "enabled": True}))

    def disable_command(self, name: str, who=None) -> Response:
        """Switch one discovered tool off. Idempotent, and never a deletion.

        `Commands.disable` refuses a row the operator wrote by hand, so this
        route cannot remove a line from a file it did not write. An id that is
        already off answers 200 with `enabled: false`, for `delete_key`'s
        reason: the caller asked for a state and that state holds.
        """
        self._operator(who)
        try:
            model = self.routes.disable(name)
        except commands.UnknownRoute as refusal:
            raise ApiError(400, "bad_command_tool", str(refusal)) from None
        except commands.CommandsError as refusal:
            raise ApiError(409, "commands_unusable", str(refusal)) from None
        return Response(200, dump({"id": model.id, "label": model.label,
                                   "model": model.model, "enabled": False}))

    @staticmethod
    def _provider(name: str) -> str:
        """The provider name, or a 404. Nothing is built from an unchecked one.

        404 rather than 400: a name that is not a provider names a resource
        that does not exist, and a client that gets a 400 goes looking for a
        malformed body it does not have.
        """
        try:
            return credentials.check_provider(name)
        except credentials.UnknownProvider as refusal:
            raise ApiError(404, "unknown_provider", str(refusal)) from None

    def _store_for(self, who):
        """Which credentials file this account's write lands in.

        The operator's land in the shared file and everyone else's in their
        own. That is the whole ownership rule and it is one expression rather
        than a flag on every route: a non-operator has no way to *name* the
        shared file, so there is no request shape in which one of them edits
        an endpoint everybody uses.
        """
        if self.directory is None:
            return self.keys
        return self.directory.store_for(who)

    def _key_store_for(self, who, provider: str):
        """The same, and a refusal for a key with no address of its own.

        **A member must configure their own endpoint before they may store a
        key against it**, and the refusal is a routing rule rather than a
        permission. A key with no recorded address is a key that goes to
        whichever address is in effect -- the operator's shared one, or the
        server's own default -- and that is exactly the pairing
        `Endpoint.moved_to` exists to make unrepresentable: a credential must
        never reach a host it was not stored against. For the operator the
        question does not arise, because the address in effect *is* theirs.

        The message says what to do rather than only what was refused: set
        your own endpoint for this provider, and your runs go there with your
        key while everybody else's go on using the shared one.
        """
        store = self._store_for(who)
        if who is None or who.operator:
            return store
        if store.read().get(provider, credentials.Endpoint()).base_url:
            return store
        raise ApiError(
            403, "no_endpoint_of_your_own",
            f"you have no {provider} endpoint of your own, so there is nowhere "
            f"to store a key against. A key is only ever sent to the address "
            f"it was stored with, and one saved here would travel to whichever "
            f"address is in effect -- which on this server is the one whoever "
            f"set it up configured. Set your own {provider} endpoint first; "
            f"your runs will go there with your key, and everybody else's will "
            f"go on using theirs.")

    def _as(self, who):
        """Run a block with this account's keys as the key source, if it has one.

        `contextlib.nullcontext` for the operator and for a server with no
        accounts, because their credentials *are* the process environment and
        swapping in a copy of it would make the two able to disagree.
        """
        source = self.keys_for(who)
        if source is None:
            return contextlib.nullcontext()
        return config.keys_for_this_run(source)

    def _as_owner(self, who):
        """Run a block with only the keys this account stored itself.

        The key source for a question about an address the account is
        storing. For the operator and for a server with no accounts that is
        the process environment, as in `_as`. For a member it is the member's
        own keys and nothing of the operator's, which is where it differs
        from `_as`: a run on a shared endpoint spends the operator's key, and
        an address a member typed never receives it.
        """
        if who is None or who.operator or self.directory is None:
            return contextlib.nullcontext()
        return config.keys_for_this_run(self.directory.own_keys(who.id))

    @staticmethod
    def _cleartext_refusal(who, provider: str, refusal) -> str:
        """The cleartext refusal, in words its reader can act on.

        `config` words it for an operator: it names the variable and says to
        unset it. A member has no variable to unset. Theirs is the key they
        saved on the credentials sheet, so that is what the message names.
        """
        if who is None or who.operator:
            return str(refusal)
        return (f"refusing to store that address: it is http:// to a machine "
                f"other than this one, and you have a {provider} key saved, "
                f"which would be sent in cleartext on every call. Use the "
                f"endpoint's https:// address, or delete your {provider} key "
                f"on the credentials sheet and save the address again.")

    def _reload_keys(self, who=None) -> None:
        """Put the file back into the environment, both copies of it.

        `os.environ` is the one that matters, because `Settings.api_key()`
        reads it at send time and it is therefore what a model call will
        actually spend.

        The store's own copy is updated too, and it is the exception to a rule
        rather than an oversight. `JobStore` copies the environment once at
        construction precisely so that an unrelated part of the process cannot
        change what a queued job resolves to -- but that rule is about a
        *submitted request* reaching a setting, and a request cannot reach this
        route's effect: `jobs.REQUEST_SETTABLE` does not carry a key variable
        and this is the operator changing their own credential. Leaving the
        copy stale would make `/health` report `configured: false` over a key
        the very next run is going to use, which is the sort of answer that
        gets a working deployment taken apart.
        """
        if who is not None and not who.operator:
            # A user's keys do not go into any environment, which is the whole
            # of what makes this multi-tenant: `os.environ` is per process and
            # a second user's key in it is exactly the arrangement this rules out. They
            # are read out of their file at the moment a job runs and handed to
            # `config.keys_for_this_run`, which is per thread.
            return
        self.keys.apply(os.environ, self.environ)

    def runs(self, who=None) -> dict:
        """Every job, oldest first, as tombstones -- no report, no document text.

        The list is what a page renders as a table, and a report in every row
        would put the whole of every merge into a response the operator refreshes.
        `Job.status()` is the payload for the same reason it is the payload of a
        status poll: it carries a state, three timestamps, an integer and a
        count, and nothing quoted out of anybody's document.
        """
        return {"runs": [self._with_expiry(job, who) for job in self.store.jobs()
                         if self._owns(job, who)]}

    @staticmethod
    def _owns(job, who) -> bool:
        """Is this job this account's? One expression, and every route uses it.

        On a server with no account store both sides are ``, so everything
        belongs to everybody: the single-tenant server stated rather than
        implied.
        """
        return getattr(job, "owner", "") == (who.id if who is not None else "")

    def job(self, job_id: str, who=None):
        """The job, by a validated id and its owner, or a 404. The only lookup here.

        **Somebody else's run answers exactly as a run that does not exist**,
        and the sameness is the point rather than a convenience. A 403 on a
        real id and a 404 on an invented one is an oracle: it turns a uuid4
        into a thing worth guessing, and tells whoever guesses right that
        somebody on this server has a job by that name -- which, on a server
        where a run is a confidential document, is already more than they
        should have.

        A uuid4 is not an access control. It is unguessable, which makes it a
        fine *name*; it is also printed in a URL bar, copied into a chat window
        and kept in a browser history, and every one of those is a way it stops
        being secret without anybody's account being compromised.
        """
        job = self.store.get(check_job_id(job_id))
        if job is None or not self._owns(job, who):
            raise ApiError(404, "no_run", f"there is no run with id {job_id}.")
        return job

    def run(self, job_id: str, who=None) -> dict:
        """One job's state, and its report once there is one. Redacted.

        The report rides in this payload rather than in a route of its own
        because the question a client asks is "is it done, and if so what
        happened" -- two requests to answer one question is a race, and the
        client that loses it renders a finished job with no report.

        `cli_equivalent` rides beside it and not only inside it: `web/jobs.py`
        sets `job.cli_equivalent` as soon as the run's settings resolve --
        while the job is still `running`, well before there is a report to
        carry it -- so the page can show "run this from the command line"
        from the moment a run starts, not only once it finishes. Once
        `job.report` exists it holds the same block, sharpened (the base
        document reads off what the merge actually followed) and redacted
        along with the rest of the report; that copy wins once it exists,
        for the one field that can change between the two.
        """
        job = self.job(job_id, who)
        payload = self._with_expiry(job, who)
        cli_equivalent = job.cli_equivalent
        if job.report is not None:
            redacted = redact.report(job.report, extra=self.extra_roots)
            payload["report"] = redacted
            if isinstance(redacted, dict) and redacted.get("cli_equivalent") is not None:
                cli_equivalent = redacted["cli_equivalent"]
        if cli_equivalent is not None:
            payload["cli_equivalent"] = cli_equivalent
        return payload

    def _with_expiry(self, job, who=None) -> dict:
        """`job.status()`, plus how many seconds are left before it is forgotten.

        **Seconds remaining and not an expiry timestamp**, and the difference
        is the whole reason this is computed here. The page uses it to stop
        offering downloads for a run this server has already forgotten, and a
        page that worked that out by subtracting `finished_at` from
        `Date.now()` would be subtracting one machine's clock from another's.
        A laptop half an hour fast would black out a live run; half an hour
        slow, it would keep offering a dead one. `JobStore.forgets_in` reads
        the same clock the reaper does, so what the page counts down is an
        interval and never a time of day.

        `None` means there is nothing to count: retention is off, the run has
        not finished, or it is already a tombstone. `forgotten_at` says which
        of the last two.
        """
        payload = job.status()
        if payload.get("error"):
            # A failed write names the file it could not write, and that is
            # a path in this server's work directory. Taken out as it is
            # taken out of a report, for whoever is asking.
            payload["error"] = redact.text(payload["error"],
                                           extra=self.roots_for(who))
        payload["expires_in"] = self.store.forgets_in(job)
        # Where a queued run stands: "position 2 of 3". The queue is
        # every account's, since the workers are, so this is a count of other
        # people's runs and nothing else about them. None when not queued.
        place = self.store.queue_position(job)
        payload["queue_position"] = place[0] if place else None
        payload["queue_length"] = place[1] if place else None
        return payload

    def submit(self, body: bytes, headers, who=None) -> Response:
        """202, an id, and a `Location`. The work has not started.

        202 and not 201: nothing exists yet at the URL in `Location` except a
        record that the work was accepted, and 201 would tell a client the
        result is there. The distinction is the whole reason this layer exists
        -- a merge takes between 23 and 4,559 seconds.
        """
        check_content_type(headers)
        try:
            # Under this account's own key source and its own addresses. The
            # refusals `submit` makes -- "this server cannot reach that model"
            # -- are answers about *this* submitter's endpoints, and a version
            # of this that resolved against the server's own would tell a user
            # their own endpoint does not exist.
            with self._as(who):
                job = self.store.submit(
                    parse_submit(body),
                    owner=who.id if who is not None else "")
        except commands.UnknownRoute as exc:
            # Its own code, and ahead of `JobRefused` because it is the more
            # specific answer. A client branching on the status alone cannot
            # tell "that is not a route this server has" from "these documents
            # cannot be merged", and the first is the one a page has to explain
            # in its own words. It reaches here rather than `parse_submit`
            # because resolving an id needs the operator's file, which a
            # `MergeRequest` deliberately has no access to.
            raise ApiError(400, "bad_command_route", str(exc)) from None
        except EffortRefused as exc:
            # The route exists and cannot carry the level, found only
            # once the operator's file is read. The field's own code, for the
            # reason `bad_command_route` has one.
            raise ApiError(400, "bad_effort", str(exc)) from None
        except JobRefused as exc:
            raise ApiError(400, "refused", str(exc)) from None
        return Response(
            202, dump(job.status()),
            headers=(("Location", f"{API_PREFIX}/runs/{job.id}"),),
        )

    def delete(self, job_id: str, who=None) -> Response:
        """Forget the job entirely. 204, and 204 again if it was already gone.

        Idempotent rather than 404 on the second call: the operator asked for
        the run to be gone and it is gone, and a client that retries a deletion
        after a dropped connection should not be told its first attempt
        failed.
        """
        check_job_id(job_id)
        job = self.store.get(job_id)
        # Somebody else's run is left alone and answered 204, which is the
        # same answer an id that was never here gets. Anything else -- a 403,
        # or a 404 where a stranger's id gets 204 -- would make this route an
        # oracle for whose runs exist, which is what `job` refuses to be.
        if job is not None and self._owns(job, who):
            self.store.delete(job_id)
        return Response(204, b"", content_type=JSON_TYPE)

    def cancel(self, job_id: str, who=None) -> Response:
        """Cancel a run: 202 and its status, for its submitter or the operator.

        **Who.** The submitter, by `_owns`, or an operator (`who.operator`),
        who is the person paying for the endpoints everybody shares and so the
        one who may stop a run that is spending on them. Anybody else gets the
        404 `job` gives a stranger's id: a 403 here would be the oracle for
        whose runs exist that `job` refuses to be. On a server with no account
        store every run is everybody's, as it is on every other route.

        **What.** A queued run never starts and is `cancelled` in this answer.
        A running one answers `running` with `cancel_requested: true`: its
        client makes no further call, a call in flight is abandoned and may
        still be billed, a command backend's program is stopped, and the run
        lands in `cancelled` once the worker is back, with the report of what
        ran. 409 for a run that has already finished, because there is nothing
        left to stop and a 202 would say there was.
        """
        job = self.store.get(check_job_id(job_id))
        allowed = job is not None and (
            self._owns(job, who) or bool(getattr(who, "operator", False)))
        if not allowed:
            raise ApiError(404, "no_run", f"there is no run with id {job_id}.")
        if job.terminal:
            raise ApiError(409, "not_running",
                           f"run {job_id} has already finished ({job.state}), "
                           f"so there is nothing to cancel.")
        self.store.cancel(job.id)
        return Response(202, dump(self._with_expiry(job, who)))

    def retry(self, job_id: str, who=None) -> Response:
        """Start a new run from a failed or interrupted one's documents.

        202, the new run's status and its `Location`, exactly as `submit`
        answers -- it is a submit, of the documents and settings the old run
        was given, with `retry_of` naming it. **Its submitter only**: `job`
        answers a stranger's id with the 404 an unknown one gets, and an
        operator may cancel anybody's run but not re-send somebody else's
        documents. 409 for a run that is not retryable, 410 for one whose
        documents retention has deleted.

        The page asks first, and says why: the new run makes every call again
        and every one of them may be billed again. Nothing here re-uses the
        old run's answers.
        """
        job = self.job(job_id, who)
        if job.state not in RETRYABLE:
            raise ApiError(409, "not_retryable",
                           f"run {job.id} is {job.state}; only a failed or "
                           f"interrupted run can be retried.")
        if not job.retryable:
            raise ApiError(410, "forgotten",
                           f"run {job.id}'s documents have been deleted, so "
                           f"there is nothing to retry it from. Documents are "
                           f"removed when the retention window passes.")
        try:
            with self._as(who):
                new = self.store.retry(job.id)
        except commands.UnknownRoute as exc:
            raise ApiError(400, "bad_command_route", str(exc)) from None
        except EffortRefused as exc:
            raise ApiError(400, "bad_effort", str(exc)) from None
        except JobRefused as exc:
            raise ApiError(400, "refused", str(exc)) from None
        return Response(
            202, dump(self._with_expiry(new, who)),
            headers=(("Location", f"{API_PREFIX}/runs/{new.id}"),),
        )

    def merged(self, job_id: str, who=None) -> Response:
        """The merged document, as markdown. The product, byte for byte.

        **Not redacted, and that is deliberate.** It is the operator's own text.
        A root that happened to occur inside it would come back replaced, and a
        merge tool that silently edits its own output has done something worse
        than disclose a directory name. See `redact`'s module docstring.
        """
        job = self.job(job_id, who)
        text = self._artefact(job, MERGED_MD, "merged")
        return Response(200, text.encode("utf-8"),
                        content_type="text/markdown; charset=utf-8")

    def report_html(self, job_id: str, who=None) -> Response:
        """The self-contained HTML report as a file to keep, redacted on the way out.

        Read back from the file the job wrote rather than re-rendered from
        `job.run`. Two reasons, and the second is the one that decided it: the
        `Run` is dropped when retention forgets a job while the tombstone
        survives, so a re-render would have to handle a job whose report exists
        and whose run does not; and a page re-rendered per request is a second
        artefact, which could differ from the one on disk and would do so
        silently.

        **This route is the artefact; `report_page` is the page.** What comes
        back here is what the command line writes with `--html` and what a
        reader can mail to somebody: one file, nothing fetched, no link to this
        server in it. It is what the results panel's "Download report" saves,
        and it is what the control on the report page carries.
        """
        job = self.job(job_id, who)
        page = self._artefact(job, REPORT_HTML, "report")
        return Response(200,
                        redact.text(page, extra=self.extra_roots).encode("utf-8"),
                        content_type="text/html; charset=utf-8",
                        headers=(("Content-Security-Policy", REPORT_CSP),))

    def report_page(self, job_id: str, who=None) -> Response:
        """The same report as a page to read, with a control that saves it.

        The one copy of this report that knows a reader is at a browser. It is
        the artefact above with `html_report.SLOT` filled in, and what the
        control hands over is those same bytes -- carried in the control's own
        `data:` URL, not fetched back from here.

        **It cannot be fetched back from here, and that is what decided the
        design.** A report is served sandboxed into an opaque origin, so every
        request it starts is cross-site, and the session cookie is
        `SameSite=Strict` because that is this server's CSRF defence
        (`accounts.cookie`). A control linking to the route above was measured
        answering **401** in a tab that had just loaded this page. Nothing on
        a sandboxed report page can ask this server for anything; a control
        there either carries what it offers or does not work.

        The redaction runs before the fill, so the copy a reader saves is the
        copy this server would have sent -- roots and all, redacted once.
        """
        job = self.job(job_id, who)
        page = self._artefact(job, REPORT_HTML, "report")
        served = html_report.with_download(
            redact.text(page, extra=self.extra_roots), filename=REPORT_HTML)
        return Response(200, served.encode("utf-8"),
                        content_type="text/html; charset=utf-8",
                        headers=(("Content-Security-Policy", REPORT_PAGE_CSP),))

    def bundle(self, job_id: str, who=None) -> Response:
        """Everything this run left, in one zip, for an audit done later.

        The operator asked for one control that yields *"sources, merge and
        full report ... for auditing purposes"*, and what auditing needs is
        what decides the contents: enough to answer "was this merge faithful
        to those documents" months later, on a machine with no access to this
        server. So the sources go in beside the product, `report.json` goes in
        beside `report.html` -- the machine-readable record is the one an
        auditor reads with a tool, and it carries the provenance block naming
        the models, the prompts and the settings that produced the rest.

        **Every member is the same bytes the route that already serves it
        would send, redacted by the same call.** This is one route and four
        artefacts, not a fifth renderer: `report.json` goes through
        `redact.report` because `run` does, `report.html` through
        `redact.text` because `report_html` does, and the sources and the
        merged document go through neither because `merged` deliberately does
        not -- they are the operator's own text, and a merge tool that edits
        its own output on the way out has done something worse than name a
        directory. That symmetry is the guard: a member cannot leak what its
        own route refuses to leak, because it *is* its own route's answer.

        **A forgotten run refuses here exactly as it refuses everywhere
        else.** `_artefact` is asked for the report first and before anything
        is assembled, so the 410 arrives instead of a zip rather than inside
        one -- an empty or half-filled archive is the failure shape that makes
        somebody believe they have an audit record.

        `merged.md` is the one optional member: the merge step itself can
        fail, and then there is no merged document to put in. The report is
        still the account of how it failed, and a bundle refused because one
        of four artefacts does not exist would be a bundle you cannot get for
        exactly the runs worth auditing.
        """
        job = self.job(job_id, who)
        # First, and before the archive exists. Every refusal this route can
        # make is this call's.
        report = self._artefact(job, REPORT_JSON, "report")
        page = self._artefact(job, REPORT_HTML, "report")
        members: list[tuple[str, str]] = []
        # The sources as submitted, under the labels the operator gave them --
        # the same labels the report's own tables name, so a reader can line
        # the two up. Read from the job's request, which after a restart is
        # itself read back from the job's `sources.json`.
        taken: set[str] = set()
        for label, text in (job.request.documents or {}).items():
            name = _zip_name(label)
            # Two labels can reduce to one name -- `a/b.md` and `a-b.md` do --
            # and `zipfile` writes both, leaving an archive with two members of
            # the same name that extracts to one file. Numbered rather than
            # dropped: an audit bundle silently missing a source is the worst
            # outcome available here.
            if name in taken:
                stem, dot, extension = name.rpartition(".")
                base = stem if dot else name
                suffix = f".{extension}" if dot else ""
                index = 2
                while f"{base}-{index}{suffix}" in taken:
                    index += 1
                name = f"{base}-{index}{suffix}"
            taken.add(name)
            members.append((f"sources/{name}", text))
        if job.directory is not None and (job.directory / MERGED_MD).is_file():
            members.append((MERGED_MD,
                            (job.directory / MERGED_MD).read_text(encoding="utf-8")))
        members.append((REPORT_JSON, _redacted_report_json(
            report, extra=self.extra_roots)))
        members.append((REPORT_HTML, redact.text(page, extra=self.extra_roots)))
        buffer = io.BytesIO()
        # Deflate rather than stored: a report quotes its sources, so a bundle
        # is three overlapping copies of the same prose and compresses hard.
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, text in members:
                archive.writestr(name, text)
        return Response(
            200, buffer.getvalue(), content_type="application/zip",
            # The id and nothing else. It is 32 hex characters by the time it
            # reaches here (`check_job_id`, through `job` above), so there is
            # nothing in this header a submitter chose -- a filename built from
            # an operator's document label would be a header value a form could
            # write.
            headers=(("Content-Disposition",
                      f'attachment; filename="llossless-{job.id}.zip"'),))

    def _artefact(self, job, name: str, what: str) -> str:
        """One of the three files a finished job leaves, or a reason there is none.

        The three states a client can be in are answered apart, because "not
        yet", "never will be" and "not any more" are three different things to
        show a person and a single 404 would make them one.

        **The `forgotten` message names the knob.** It used to say only what
        had happened, which is the one thing the reader has already worked out
        by the time they read it: they clicked a link and their report was
        gone. What they need next is whether it can be stopped from happening
        again, and on a self-hosted tool the person reading this is frequently
        the person who could have set the window. It is not a disclosure: the
        flag is in `--help` and in the README, and the page states the window
        under a finished run's download buttons.
        """
        if job.forgotten:
            raise ApiError(410, "forgotten",
                           f"this run's {what} has been deleted. Documents and "
                           f"everything derived from them are removed when the "
                           f"retention window passes. That window is "
                           f"configurable: start this server with "
                           f"`--retention SECONDS`, or set "
                           f"{RETENTION_ENV}; `--retention 0` keeps runs "
                           f"until they are deleted.")
        if not job.terminal:
            raise ApiError(409, "not_finished",
                           f"this run is {job.state}; there is no {what} yet.")
        if job.directory is None or not (job.directory / name).is_file():
            raise ApiError(404, "no_artefact",
                           f"this run produced no {what}. See the run's error "
                           f"and its event log for what happened.")
        return (job.directory / name).read_text(encoding="utf-8")

    # -- the stream ------------------------------------------------------

    def stream(self, job_id: str, *, who=None, last_event_id=None,
               keepalive: float = 15.0, retry_ms: int | None = None) -> Stream:
        """The SSE endpoint. Frames from `Last-Event-ID` onward, then live ones.

        The replay is `EventLog.since`'s job and the waiting is `EventLog.wait`'s,
        so neither is re-implemented here; what this adds is the loop that
        alternates between them and the comment frame that keeps an idle
        connection open. A merge can go minutes between events -- one model call
        at `high` on a long pair is exactly that -- and an intermediary with an
        idle timeout will close a connection that has said nothing, which the
        browser sees as a dropped stream and reconnects, replaying from the last
        id. It works, and it costs a round trip every timeout for a run that was
        never in trouble.

        The generator ends when the log is closed and there is nothing after the
        last id delivered. Ending is what closes the connection, and the browser
        reads that as a drop and reconnects -- which is correct and is why the
        final `state` event carries `terminal: true`: a page that has seen it
        stops listening rather than reconnecting to a job that has finished.
        """
        job = self.job(job_id, who)
        after = (parse_last_event_id(last_event_id)
                 if not isinstance(last_event_id, int) else max(0, last_event_id))
        # What a step said when it failed can quote a path under this
        # server's directories, as a report can. The log keeps what was said;
        # what is sent has the directories taken out, event by event, before
        # it is serialised.
        known = redact.roots(self.roots_for(who))

        def sent(event):
            return Event(event.id, event.kind, redact.scrub(event.message, known),
                         at=event.at, seconds=event.seconds, level=event.level,
                         fields=redact.walk(event.fields, known))

        def produce():
            cursor = after
            first = True
            while True:
                events = job.events.since(cursor)
                if events:
                    yield frames([sent(event) for event in events],
                                 retry_ms=retry_ms if first else None)
                    cursor = events[-1].id
                    first = False
                    continue
                if job.events.closed:
                    if first and retry_ms is not None:
                        yield f"retry: {int(retry_ms)}\n\n"
                    return
                # A comment frame. The browser ignores it and every proxy
                # between here and it sees traffic, which is the whole job.
                if not job.events.wait(cursor, timeout=keepalive):
                    yield ": keep-alive\n\n"
                    first = False

        return Stream(produce(), headers=(
            ("Content-Type", SSE_TYPE),
            # Nothing between this server and a browser on the same machine
            # should be buffering, and `X-Accel-Buffering` is the one header
            # that tells the proxy people do put there anyway.
            ("Cache-Control", "no-store"),
            ("X-Accel-Buffering", "no"),
        ))
