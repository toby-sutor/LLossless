"""The only module in this project that opens a socket.

Keeping it alone in a file is the point: "no network calls other than the
configured LLM endpoint" is checkable by reading one short file, and replay mode
proves itself by never importing this module at all.

Everything here is stdlib. urllib.request already does the three things an HTTP
client is usually added for — TLS verification against the system trust store,
HTTPS_PROXY/HTTP_PROXY/NO_PROXY, and per-request timeouts — so a dependency
would buy only the retry loop below, which is about forty lines.
"""

from __future__ import annotations

import json
from itertools import chain
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

from . import __version__

# urllib sends `Python-urllib/3.x` when nothing else is set, and a Cloudflare
# rule in front of one hosted endpoint answers that signature with a 403 and
# error 1010 — before the request reaches the model, on a host `curl` reaches
# from the same machine a second earlier. The name matters less than sending
# one; any explicit value passed. It is a constant rather than a setting
# because it identifies the client, not the run, and it stays out of the
# cassette key for the same reason: two recordings that differ only in who
# said hello are the same recording.
USER_AGENT = f"llossless/{__version__}"

# 529 (Anthropic's `overloaded_error`) and 524 (Cloudflare origin timeout)
# joined the OpenAI/Google-shaped codes later: both were fatal on the
# first attempt, so an Anthropic overload ended the call where an identical
# OpenAI or Google 503 got two more tries, and only the runner's own re-run
# stood between that and an exclusion the common-pairs rule then spread to
# every model.
RETRYABLE_STATUS = frozenset({408, 429, 500, 502, 503, 504, 524, 529})
FATAL_STATUS = frozenset({400, 401, 403, 404, 422})

MAX_ATTEMPTS = 3
BACKOFF_SECONDS = (1.0, 2.0, 4.0)
MAX_RETRY_AFTER = 60.0
BODY_EXCERPT = 600


# What stands where a credential was taken out of a relayed body.
REDACTED = "<redacted>"

# The fewest trailing characters of a key that count as part of it. Four is
# what a vendor's "ending in ..." names, and what the settings page shows the
# key's owner and nobody else.
MIN_KEY_TAIL = 4

# And the fewest leading characters. More than a tail needs, because the
# start of a key is the part that is not secret: `sk-`, `AIza` and their like
# are a vendor's prefix and stand in ordinary sentences about keys. Six is
# past every prefix that is a word of its own, and short enough that an echo
# of "the first eight characters" does not get through.
MIN_KEY_HEAD = 6

# Stands for the key this process holds while the shapes below are applied,
# so that no shape can match half of a mark already made. A private-use
# character: no key, no mask and no error message is written with one.
_HELD = "\ue000"

# What a key looks like in somebody else's text. An endpoint's error body is
# written by the endpoint, and it reaches whoever ran the job: the terminal on
# the command line, and on a shared server a member whose run spent the
# operator's key. A 401 that says which key it refused is ordinary.
#
# The first two shapes are the repository's own definition of a secret, the
# one its release scan uses (`secret_patterns` in `tests/test_client.py`),
# restated because nothing under `src/` may import the test tree. The other
# three are a key that was masked before it was echoed: a run of asterisks or
# bullets with whatever is left of the key on either side, an ellipsis
# between two pieces of one, and a sentence about a key that names the
# characters it ends in. Each is paired with what replaces a match, and the
# last keeps the sentence and takes only the characters.
_KEY = r"-A-Za-z0-9_"
_KEY_SHAPES = tuple((re.compile(shape), put) for shape, put in (
    (rf"(?<![A-Za-z0-9])(?:sk-[{_KEY}]{{16,}}|AIza[{_KEY}]{{20,}}"
     rf"|xoxb-[A-Za-z0-9-]{{10,}})", REDACTED),
    (r"Bearer\s+[A-Za-z0-9._-]{12,}", REDACTED),
    (rf"(?<![{_KEY}])[{_KEY}]+[*\u2022]{{3,}}[{_KEY}*\u2022{_HELD}]*"
     rf"|(?<![*\u2022])[*\u2022]{{3,}}[{_KEY}{_HELD}][{_KEY}*\u2022{_HELD}]*",
     REDACTED),
    (rf"(?<![{_KEY}])[{_KEY}]+(?:\.{{3,}}|\u2026)[{_KEY}{_HELD}]+", REDACTED),
    (rf"(?i)(\b(?:key|token)\b[^.\n]{{0,60}}?\b(?:ending|ends)\s+(?:in|with)"
     rf"[\s:'\"`]{{0,3}})[{_KEY}]{{2,}}", r"\1" + REDACTED),
))
_MARKS = re.compile(f"(?:{_HELD}|{re.escape(REDACTED)})+")


def scrub(text: str, secret: str | None = None) -> str:
    """`text` with every credential, and every piece of one, taken out.

    `secret` is the key this process sent with the request the text answers.
    It goes first and it is exact: the key itself, any tail of it of
    `MIN_KEY_TAIL` characters or more, and any head of it of `MIN_KEY_HEAD`
    or more, wherever one occurs. That is the part that is certain. A masked
    echo keeps an end of a key, and both ends of this key are known here, so
    they are removed whatever is written around them. An echo of the start
    alone, "the key beginning sk-proj-Ab12Cd34", used to pass: no shape
    below matches a piece of a key with no mask beside it.

    Then the shapes, which are a guess and are still worth making: an
    endpoint can echo a key this process never held, such as the upstream
    key of a proxy.

    The rest of the text is left as it was. The status and the reason an
    endpoint gave are what an operator reads a failed call for.
    """
    if secret and len(secret) >= MIN_KEY_TAIL:
        text = text.replace(secret, _HELD)
        tail = secret[-MIN_KEY_TAIL:]
        kept, done = [], 0
        at = text.find(tail)
        while at != -1:
            # As much of the key's end as stands in front of these four.
            start, back = at, len(secret) - MIN_KEY_TAIL
            while start > done and back > 0 and text[start - 1] == secret[back - 1]:
                start, back = start - 1, back - 1
            kept += (text[done:start], _HELD)
            done = at + MIN_KEY_TAIL
            at = text.find(tail, done)
        text = "".join(kept) + text[done:]
    if secret and len(secret) >= MIN_KEY_HEAD:
        head = secret[:MIN_KEY_HEAD]
        kept, done = [], 0
        at = text.find(head)
        while at != -1:
            # As much of the key's start as follows these six.
            end = at + MIN_KEY_HEAD
            while (end < len(text) and end - at < len(secret)
                   and text[end] == secret[end - at]):
                end += 1
            kept += (text[done:at], _HELD)
            done = end
            at = text.find(head, done)
        text = "".join(kept) + text[done:]
    for shape, put in _KEY_SHAPES:
        text = shape.sub(put, text)
    return _MARKS.sub(REDACTED, text)


class TransportError(RuntimeError):
    """A request could not be completed. Always fatal at the call site."""


class Cancelled(RuntimeError):
    """The run was cancelled: no further call is made.

    Raised by `Client` before a call it will not make and in place of one it
    abandoned in flight, and by `backend.post_json` for a program it stopped.
    Not a `TransportError`: nothing failed, somebody asked for the run to stop.
    Here, the lowest layer both backends import, so the command backend and
    the HTTP path raise one class and `cli.FATAL` names it once.
    """


class HTTPStatusError(TransportError):
    """The endpoint answered with an error status.

    `status` and `body` are exposed because the capability probe reads them to
    decide whether an endpoint rejected `response_format` specifically or is
    simply misconfigured.

    The body is the endpoint's own text and the message carries an excerpt of
    it to whoever ran the call, so it is passed through `scrub` first.
    `secret` is the key that was sent with the request. It is used for that
    and is not kept: no key is stored on an exception from this module.
    """

    def __init__(self, status: int, body: str, host: str, model: str,
                 *, secret: str | None = None) -> None:
        body = scrub(body, secret)
        excerpt = body.strip()[:BODY_EXCERPT]
        super().__init__(
            f"HTTP {status} from {host} for model {model}"
            + (f"\n{excerpt}" if excerpt else "")
        )
        self.status = status
        self.body = body
        self.host = host
        self.model = model


@dataclass(frozen=True)
class Response:
    """One answered request, and how its time was spent.

    `latency_ms` has kept the same meaning throughout: the wall time from
    the first attempt going out to the answer arriving, so it spans every
    transport attempt *and* the backoff sleeps between them. It is not the
    answering attempt's time, and it never includes `Client._pace`.

    The four fields after `attempts` split that span, so a report can charge a
    benchmark cell with the attempt that produced its answer alone and
    show everything else apart:

      `answer_ms`  the attempt that returned this body, alone
      `failed_ms`  the attempts before it that failed (429/5xx, a timeout, a
                   cut stream), each one's own time, sleeps excluded
      `waited_ms`  the backoff sleeps between attempts (the client adds its
                   own pacing to this figure on the ledger row)
      `ttfb_ms`    from the answering attempt going out to the first line of
                   its body arriving; `None` where nothing measured it

    so `latency_ms` is `failed_ms + waited_ms + answer_ms` to within a few
    milliseconds: each is truncated to a whole millisecond, and building each
    request object is in none of them. Defaults keep a `Response(status, body,
    latency, attempts)` built by hand -- a fake transport -- valid; `Client`
    reads a missing `answer_ms` on a one-attempt response as the whole
    latency, which is what one attempt with no sleep is, and leaves the split
    unrecorded on a response of several attempts that did not carry one.

    `cli_timing` is a command route's own figures, off its result envelope:
    `duration_ms` and `duration_api_ms`, each present only when it said.
    """

    status: int
    body: str
    latency_ms: int
    attempts: int
    answer_ms: int | None = None
    failed_ms: int = 0
    waited_ms: int = 0
    ttfb_ms: int | None = None
    cli_timing: dict | None = None


def _ms(seconds: float) -> int:
    return int(seconds * 1000)


def _stamp(exc: Exception, *, attempts: int, failed: float, waited: float,
           answered: float | None = None) -> Exception:
    """`exc`, carrying the attempts it took and how their time was spent.

    Attributes rather than a new exception class, so every handler that
    catches these by class today still does. `Client` reads them off a failed
    call to file it under `provenance.discarded_calls` with its time split the
    way a ledger row's is. Here `failed_ms` includes the attempt that raised,
    except for `EmptyBody`, whose attempt did answer (blank) and is
    `answer_ms`. An exception without them (a command backend's, or a fake's)
    is timed by the client's own stopwatch instead.
    """
    exc.attempts = attempts
    exc.failed_ms = _ms(failed)
    exc.waited_ms = _ms(waited)
    exc.answer_ms = None if answered is None else _ms(answered)
    return exc


def _tls_context(ca_bundle: str | None) -> ssl.SSLContext:
    """Verification is always on. There is deliberately no --insecure flag.

    A corporate TLS-interception proxy is a real situation and LLOSSLESS_CA_BUNDLE
    is the answer to it: point at the bundle and verification still happens. A
    flag that turns verification off would be used far more often than the
    situation that justifies it.
    """
    return ssl.create_default_context(cafile=ca_bundle)


def _opener(ca_bundle: str | None) -> urllib.request.OpenerDirector:
    """Every handler named, none inherited.

    This passed `build_opener` an `HTTPSHandler` and a redirect refuser and took
    the rest of its defaults, with a comment naming `ProxyHandler` and stopping
    there. The defaults it did not name are `FileHandler`, `FTPHandler` and
    `DataHandler`, and the first of those turned `LLOSSLESS_BASE_URL=file://...`
    into a local file read whose bytes were parsed as a model answer.

    `config.check_base_url` refuses that URL before a client is built, which is
    where the refusal belongs and where the error message can be useful. This is
    the second wall: the scheme cannot be spoken here even if something one day
    reaches this function without going through `resolve`.

    What is installed, and why each:

      `HTTPHandler`            plain HTTP. The default endpoint is
                               `http://localhost:11434/v1`.
      `HTTPSHandler`           with this project's TLS context, so
                               `LLOSSLESS_CA_BUNDLE` is honoured.
      `_RefuseRedirects`       the threat: a redirect is how a
                               bearer token reaches a host nobody configured.
      `HTTPErrorProcessor`     turns non-2xx into `HTTPError`, which the
                               callers here are written against.
      `HTTPDefaultErrorHandler` the fallback that raises rather than returning
                               a half-open response.
      `ProxyHandler`           honours `*_PROXY`, and only registers itself
                               when one is set, which is why it was easy to
                               name and easy to believe was the whole list.

      `UnknownHandler`         raises on a scheme nothing above handles.
                               Dropping it was tried and is wrong: without it
                               `open()` returns `None` for a `file://` URL
                               rather than raising, which is a quieter failure
                               than the one being fixed.

    Not installed, deliberately: `FileHandler`, `FTPHandler`, `DataHandler`. A
    URL this opener cannot speak raises rather than being fetched by some other
    means.
    """
    # `OpenerDirector` and not `build_opener`. `build_opener` adds every
    # default class the caller did not pass an instance of, so naming the
    # handlers there documents an intention and installs `FileHandler` anyway.
    # Checked rather than assumed: `tests/test_client.py` asserts the installed
    # set by name, both directions.
    opener = urllib.request.OpenerDirector()
    for handler in (urllib.request.ProxyHandler(),
                    urllib.request.HTTPHandler(),
                    urllib.request.HTTPSHandler(context=_tls_context(ca_bundle)),
                    _RefuseRedirects(),
                    urllib.request.HTTPErrorProcessor(),
                    urllib.request.HTTPDefaultErrorHandler(),
                    urllib.request.UnknownHandler()):
        opener.add_handler(handler)
    return opener


class _RefuseRedirects(urllib.request.HTTPRedirectHandler):
    """No redirect is ever followed. `build_opener` installs one that would be.

    `urllib.request.HTTPRedirectHandler` copies every header but
    `Content-Length` and `Content-Type` onto the redirected request -- which
    means `Authorization` -- and hands it to whatever host the `Location`
    header names, no matter who configured the original one. A POST becomes a
    GET on the way, so a merge would silently stop being sent at all while the
    key kept travelling.

    A redirect from an inference endpoint is not a normal event: refusing
    matches `_tls_context`'s posture, which declines an `--insecure` escape
    hatch on the same reasoning that it would be reached for more often than
    the situation justifies. This class replaces `build_opener`'s default --
    `build_opener` skips installing its own `HTTPRedirectHandler` when the
    caller passes a subclass of it -- so nothing here is bypassed by the
    default the caller did not ask for.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urllib.parse.urlparse(newurl)
        raise TransportError(
            f"{req.host} answered with a redirect to "
            f"{target.netloc or newurl}, which this client does not follow: "
            f"the request carries a bearer token and a redirect handler "
            f"forwards it to any host named in Location. If the endpoint "
            f"legitimately moved, repoint LLOSSLESS_BASE_URL at "
            f"{target.scheme}://{target.netloc} directly."
        )


def timed_out(host: str, timeout: float, *, sent: bool) -> TransportError:
    """The message for a timeout, which of the two it was, and where to look.

    One clock covers two events that have nothing in common except a stopwatch.
    Nothing was sent -- no route, no listener, a firewall holding the SYN -- and
    the endpoint answered nothing. Or the request was accepted and the answer
    did not arrive in time, which means the endpoint is up and generating, and
    the budget is the thing that was wrong.

    Both printed as a timeout until this was fixed, and an operator reading "localhost did
    not respond within 300s" cannot tell which happened. That line is in
    `tests/responses/m4/sweep-attempt3-aborted.log`; the endpoint was in fact
    alive and thermally throttled to a fifth of its rate, so the answer was
    `--timeout`, and the message pointed at the server.

    A separate function so the pair can be tested without provoking a real
    connect timeout, which would mean opening a socket to something that is not
    the configured endpoint.
    """
    if sent:
        return TransportError(
            f"{host} took the request and did not finish answering within "
            f"{timeout:g}s: the endpoint is up and was too slow. Raise --timeout, "
            f"or lower max_tokens."
        )
    return TransportError(
        f"{host} accepted no connection within {timeout:g}s: the request was never "
        f"sent, so the endpoint answered nothing. Check it is listening and reachable."
    )


def _retry_after(headers) -> float | None:
    """Seconds to wait, if the endpoint said. Only the numeric form is honoured."""
    raw = headers.get("Retry-After") if headers else None
    if not raw:
        return None
    try:
        return min(max(float(raw), 0.0), MAX_RETRY_AFTER)
    except ValueError:
        return None  # HTTP-date form; fall back to the backoff schedule


class StreamTruncated(TransportError):
    """The connection closed part-way through a streamed answer.

    Its own class because it is the one transport failure that could be mistaken
    for a result. A stream that stops early has already delivered a prefix of a
    document, and a prefix of a merge is a merge with facts missing -- which is
    precisely what this project reports on. Returning it would put a transport
    fault into the coverage table under the model's name.
    """


class EmptyBody(TransportError):
    """A 200 whose body has nothing in it at all.

    Its own class for the same reason `StreamTruncated` is: it arrives after a
    success and has to be told apart from one. It is not retried here. A blank
    generation is not weather -- the request crossed the wire, the endpoint
    answered, and the model wrote nothing -- so the decision about asking again
    belongs to the client, which knows the tier, the role and how many times it
    has already asked. Measured on 2026-08-28: gpt-oss:120b behind a hosted
    proxy, sent `reasoning_effort: "none"`, billed 763 completion tokens and
    returned zero bytes with a 200. Before this class existed those zero bytes
    reached `json.loads` and the run ended on a Python decoder error that named
    nothing an operator could act on.
    """

    def __init__(self, host: str, model: str, content_type: str) -> None:
        super().__init__(
            f"{host} answered 200 with an empty body for model {model} "
            f"(content type {content_type or 'unset'})"
        )
        self.host = host
        self.model = model
        self.content_type = content_type


def _events(response, secret: str | None = None) -> "list[dict]":
    """The parsed `data:` events of a server-sent-event response, in order.

    Blank lines and comment lines are skipped, `[DONE]` ends the stream, and an
    unparseable event raises rather than being dropped: a stream is a document
    delivered in pieces, and a piece silently discarded is a hole in the middle
    of the answer that nothing downstream could see.

    `secret` is the key the request carried, for `scrub`: the event that does
    not parse is quoted in the error, and an endpoint can put anything in it.
    """
    events: list[dict] = []
    for line in response:
        text = line.decode("utf-8", errors="replace").strip()
        if not text or text.startswith(":"):
            continue
        if not text.startswith("data:"):
            continue
        chunk = text[5:].strip()
        if chunk == "[DONE]":
            break
        try:
            events.append(json.loads(chunk))
        except ValueError as exc:
            raise StreamTruncated(
                f"a streamed event was not JSON after {len(events)} good ones: "
                f"{scrub(chunk[:4 * BODY_EXCERPT], secret)[:BODY_EXCERPT]}"
            ) from exc
    return events


def reassemble(events: "list[dict]") -> str:
    """Streamed deltas, folded back into the body a non-streamed call returns.

    The point is that nothing above this line has to know which way the answer
    arrived. `client` parses one shape, `cassette` stores one shape, and a
    corpus recorded over a streaming transport replays against one recorded
    without it. Measured equal before it was written: the same request answered
    both ways gave byte-identical `content` (316 chars), byte-identical
    `reasoning`, and the same `usage` (50 and 168 completion tokens),
    which is the evidence that this is a transport detail and not a second kind
    of request.

    `usage` needs `stream_options.include_usage`, which `post_json` sets. Without
    it ollama sends no usage at all, and `completion_tokens` is what flags a
    merge that landed on its ceiling -- so its absence is treated as truncation
    rather than as a response with a field missing.

    Raises `StreamTruncated` when no `finish_reason` arrived. That is the whole
    safety property here: the failure this transport exists to survive is a proxy
    cutting a long answer, and a cut stream and a complete one differ only in
    that field.
    """
    content: list[str] = []
    reasoning: list[str] = []
    calls: dict[int, dict] = {}
    finish: str | None = None
    usage: dict | None = None
    identity = {"id": "", "model": "", "created": 0}

    for event in events:
        usage = event.get("usage") or usage
        for name in identity:
            if event.get(name):
                identity[name] = event[name]
        for choice in event.get("choices") or []:
            finish = choice.get("finish_reason") or finish
            delta = choice.get("delta") or {}
            if delta.get("content"):
                content.append(str(delta["content"]))
            for field in ("reasoning", "reasoning_content"):
                if delta.get(field):
                    reasoning.append(str(delta[field]))
            for call in delta.get("tool_calls") or []:
                # Arguments arrive split across events, so the accumulator is
                # keyed by the index the endpoint assigns rather than by
                # position in this chunk.
                slot = calls.setdefault(
                    int(call.get("index", 0)),
                    {"id": "", "type": "function",
                     "function": {"name": "", "arguments": ""}},
                )
                if call.get("id"):
                    slot["id"] = call["id"]
                function = call.get("function") or {}
                if function.get("name"):
                    slot["function"]["name"] = function["name"]
                if function.get("arguments"):
                    slot["function"]["arguments"] += function["arguments"]

    if finish is None:
        raise StreamTruncated(
            f"the stream ended after {len(events)} events without a finish_reason, "
            f"so what arrived is a prefix of an answer and not an answer: "
            f"{len(''.join(content))} characters of content, "
            f"{len(''.join(reasoning))} of reasoning"
        )

    message: dict = {"role": "assistant", "content": "".join(content) or None}
    if reasoning:
        message["reasoning"] = "".join(reasoning)
    if calls:
        message["tool_calls"] = [calls[index] for index in sorted(calls)]

    body: dict = {
        "id": identity["id"],
        "object": "chat.completion",
        "created": identity["created"],
        "model": identity["model"],
        "choices": [{"index": 0, "message": message, "finish_reason": finish}],
    }
    if usage:
        body["usage"] = usage
    return json.dumps(body)


def post_json(
    url: str,
    payload: dict,
    *,
    api_key: str | None,
    timeout: float,
    ca_bundle: str | None,
    host: str,
    model: str,
    stream: bool = False,
    sleep=time.sleep,
) -> Response:
    """POST `payload` and return the raw body. Retries transport faults only.

    The Authorization header is built here and nowhere else. It is not stored,
    not logged, and not included in any exception raised from this module —
    which is why the error messages name `host` and `model` and are given those
    values as arguments rather than digging them out of the request.

    `stream` changes how the answer is carried and nothing about what was asked.
    It exists because one hosted endpoint sits behind a proxy that gives up on a
    request that has not started answering within about 125 seconds and returns
    a 524 with no body at all: measured, twice, at 125.1 s and 125.3 s, against
    the same request streamed running 326.4 s and delivering all 24,000 tokens.
    At the ~75 tokens/s that endpoint sustains, the wall lands at roughly 9,000
    output tokens — well below the budget a merge at `high` is given — so on that
    endpoint the choice is streaming or a corpus of timeouts.

    The reassembled body is the same shape a non-streamed call returns, so
    `stream` is not part of the cassette key and must not become part of it: two
    recordings that differ only in how the bytes crossed the wire are the same
    recording, in exactly the way `USER_AGENT` is not part of it either.
    """
    if stream:
        payload = {**payload, "stream": True,
                   "stream_options": {"include_usage": True}}
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    opener = _opener(ca_bundle)
    started = time.monotonic()
    last: Exception | None = None
    # How the span `latency_ms` covers was spent: the failed attempts'
    # own time and the sleeps between them, so the answering attempt can be
    # told apart from both. See `Response`.
    failed = waited = 0.0

    for attempt in range(1, MAX_ATTEMPTS + 1):
        request = urllib.request.Request(url, data=data, headers=headers, method="POST")
        attempt_started = time.monotonic()
        first_byte: float | None = None
        try:
            with opener.open(request, timeout=timeout) as response:
                # An endpoint is allowed to ignore `stream` and answer with
                # the whole body, and some proxies collapse one into the other,
                # so what arrived has to be established rather than assumed --
                # assuming would turn a perfectly good complete answer into a
                # stream with no events in it.
                #
                # This used to read the content type. It no longer does: the
                # header lies. A hosted proxy in front of ollama labelled a
                # server-sent-event response `application/x-ndjson` (measured
                # 2026-08-28, gpt-oss:120b), which sent every streamed answer
                # down the non-streamed branch. The first bytes cannot lie the
                # same way. An SSE body opens with a `data:` or a `:` comment
                # line and a JSON envelope opens with `{`, so one line of the
                # body decides it, whatever any header claims. The line is put
                # back in front of the rest, so nothing is consumed to find out.
                head = response.readline()
                # The first line of the body, streamed or not: the one timing
                # figure a stream makes cheap, and on a non-streamed answer
                # the moment the whole generation was done.
                first_byte = time.monotonic()
                streamed = head.lstrip().startswith((b"data:", b":"))
                body = (reassemble(_events(chain([head], response), api_key)) if streamed
                        else (head + response.read()).decode("utf-8", errors="replace"))
                content_type = response.headers.get_content_type()
            if not body.strip():
                # A 200 with nothing in it, which is neither a fault in the
                # stream nor a statement about the tier. Raised rather than
                # returned so that it cannot be mistaken for an answer, and
                # raised from here rather than retried in the loop below
                # because the client is the one that knows what to ask again.
                raise _stamp(EmptyBody(host, model, content_type), attempts=attempt,
                             failed=failed, waited=waited,
                             answered=time.monotonic() - attempt_started)
            ended = time.monotonic()
            return Response(
                status=200,
                body=body,
                latency_ms=_ms(ended - started),
                attempts=attempt,
                answer_ms=_ms(ended - attempt_started),
                failed_ms=_ms(failed),
                waited_ms=_ms(waited),
                ttfb_ms=None if first_byte is None else _ms(first_byte - attempt_started),
            )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            failed += time.monotonic() - attempt_started
            if exc.code in FATAL_STATUS:
                # Configuration, not weather. Retrying a 401 three times just
                # makes the operator wait longer for the same wrong answer.
                raise _stamp(HTTPStatusError(exc.code, body, host, model,
                                             secret=api_key),
                             attempts=attempt, failed=failed, waited=waited) from None
            if exc.code not in RETRYABLE_STATUS:
                raise _stamp(HTTPStatusError(exc.code, body, host, model,
                                             secret=api_key),
                             attempts=attempt, failed=failed, waited=waited) from None
            last = HTTPStatusError(exc.code, body, host, model, secret=api_key)
            wait = _retry_after(exc.headers)
        except urllib.error.URLError as exc:
            # urllib wraps the connect and send phases in URLError and lets the
            # wait-for-response phase raise TimeoutError bare, so which
            # exception arrives says which half of the exchange failed.
            failed += time.monotonic() - attempt_started
            last = (
                timed_out(host, timeout, sent=False)
                if isinstance(exc.reason, TimeoutError)
                else TransportError(f"cannot reach {host}: {exc.reason}")
            )
            wait = None
        except TimeoutError:
            failed += time.monotonic() - attempt_started
            last = timed_out(host, timeout, sent=True)
            wait = None
        except StreamTruncated as exc:
            # Retried, unlike every other failure that arrives after a 200. A
            # cut stream is weather -- a proxy, a dropped connection, a pod
            # restart -- and the request is idempotent, so the only cost of
            # trying again is the generation. On an unattended run that is the
            # right trade: a single hiccup at hour three should not end the arm.
            # It is bounded by MAX_ATTEMPTS like everything else, and if all
            # three are cut the exception says so rather than returning a prefix.
            failed += time.monotonic() - attempt_started
            last = exc
            wait = None

        if attempt == MAX_ATTEMPTS:
            break
        slept = time.monotonic()
        sleep(BACKOFF_SECONDS[attempt - 1] if wait is None else wait)
        waited += time.monotonic() - slept

    assert last is not None
    raise _stamp(last, attempts=MAX_ATTEMPTS, failed=failed, waited=waited)


def get_json(
    url: str,
    *,
    api_key: str | None,
    timeout: float,
    ca_bundle: str | None,
    host: str,
    sleep=time.sleep,
) -> Response:
    """GET `url` and return the raw body. Same retry discipline as `post_json`.

    Added because a caller has to know the context window the endpoint is
    actually serving before it sends a request sized against a guess. Until
    then this module made exactly one kind of request, to
    `/v1/chat/completions`, and that narrowness was a feature worth naming:
    "no network calls other than the configured LLM endpoint" was checkable by
    reading one file.

    It still is. This adds a second *method* to the same endpoint, not a second
    endpoint — callers pass a URL built from `settings.base_url` — and it sends
    no body, so there is nothing here that could carry a document off the box.
    The alternative was to hard-code the window, which is the failure this
    exists to prevent: the served window is model-dependent, and a number
    written into the source is a number that is wrong for the next model.

    `model` is absent from the signature and from the errors because a GET of a
    server-status path is not about a model. `HTTPStatusError` wants one, so
    it is given the empty string rather than a guess.
    """
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    opener = _opener(ca_bundle)
    started = time.monotonic()
    last: Exception | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with opener.open(request, timeout=timeout) as response:
                body = response.read().decode("utf-8", errors="replace")
            return Response(
                status=200,
                body=body,
                latency_ms=int((time.monotonic() - started) * 1000),
                attempts=attempt,
            )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            if exc.code in FATAL_STATUS or exc.code not in RETRYABLE_STATUS:
                raise HTTPStatusError(exc.code, body, host, "",
                                      secret=api_key) from None
            last = HTTPStatusError(exc.code, body, host, "", secret=api_key)
            wait = _retry_after(exc.headers)
        except urllib.error.URLError as exc:
            last = (
                timed_out(host, timeout, sent=False)
                if isinstance(exc.reason, TimeoutError)
                else TransportError(f"cannot reach {host}: {exc.reason}")
            )
            wait = None
        except TimeoutError:
            last = timed_out(host, timeout, sent=True)
            wait = None

        if attempt == MAX_ATTEMPTS:
            break
        sleep(BACKOFF_SECONDS[attempt - 1] if wait is None else wait)

    assert last is not None
    raise last
