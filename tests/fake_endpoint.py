"""A real OpenAI-compatible endpoint on localhost, for testing the client.

Monkeypatching transport.post_json would have been quicker and would have
tested nothing: the retry loop, the TLS context, the proxy handling and the
Authorization header all live inside the function that got replaced. This
serves actual HTTP on a loopback port instead, so the whole transport path runs
in the suite.

It is also the only way to test the capability probe honestly, because "does
this endpoint support response_format" is a question about a server, and a stub
can only be asked what it was told to say.
"""

from __future__ import annotations

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def envelope(content: str, *, tool: str | None = None, usage: bool = True) -> str:
    """A chat-completions response body carrying `content`."""
    message: dict = {"role": "assistant"}
    if tool:
        message["tool_calls"] = [
            {
                "id": "call_1",
                "type": "function",
                "function": {"name": tool, "arguments": content},
            }
        ]
        message["content"] = None
    else:
        message["content"] = content

    body: dict = {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "choices": [{"index": 0, "message": message, "finish_reason": "stop"}],
    }
    if usage:
        body["usage"] = {"prompt_tokens": 100, "completion_tokens": 50}
    return json.dumps(body)


def sse(body: str, request: dict) -> str | None:
    """One chat-completion body, taken apart into the events a stream sends.

    Returns None when `body` is not a chat completion -- a malformed body, an
    error envelope, a truncated string a test is using to provoke a parse
    failure. Those are answered whole, so that a test about bad JSON stays a test
    about bad JSON instead of becoming a test about a stream carrying it.

    The splitting is deliberately awkward where the reassembler could cheat.
    Content goes out in three pieces so concatenation is exercised rather than
    "the last chunk wins"; `tool_calls` arrive with the name in one event and the
    arguments split across two more, which is the shape that broke every naive
    accumulator; `finish_reason` arrives alone in an event with an empty delta,
    which is what a real stream does and what `reassemble` must not mistake for
    the end of the content.
    """
    try:
        payload = json.loads(body)
        choice = payload["choices"][0]
        message = choice["message"]
    except (ValueError, KeyError, IndexError, TypeError):
        return None

    identity = {"id": payload.get("id", ""), "object": "chat.completion.chunk",
                "created": payload.get("created", 0), "model": payload.get("model", "")}

    def event(delta: dict, finish=None) -> str:
        chunk = dict(identity)
        chunk["choices"] = [{"index": 0, "delta": delta, "finish_reason": finish}]
        return f"data: {json.dumps(chunk)}\n\n"

    out = [event({"role": "assistant"})]

    for field in ("reasoning", "reasoning_content"):
        text = message.get(field)
        if text:
            out.append(event({field: text[: len(text) // 2]}))
            out.append(event({field: text[len(text) // 2:]}))

    content = message.get("content")
    if content:
        third = max(1, len(content) // 3)
        for start in range(0, len(content), third):
            out.append(event({"content": content[start:start + third]}))

    for index, call in enumerate(message.get("tool_calls") or []):
        function = call.get("function") or {}
        arguments = function.get("arguments") or ""
        out.append(event({"tool_calls": [
            {"index": index, "id": call.get("id", ""), "type": "function",
             "function": {"name": function.get("name", ""), "arguments": ""}},
        ]}))
        half = len(arguments) // 2
        for piece in (arguments[:half], arguments[half:]):
            out.append(event({"tool_calls": [
                {"index": index, "function": {"arguments": piece}},
            ]}))

    out.append(event({}, finish=choice.get("finish_reason") or "stop"))

    if (request.get("stream_options") or {}).get("include_usage") and payload.get("usage"):
        final = dict(identity)
        final["choices"] = []
        final["usage"] = payload["usage"]
        out.append(f"data: {json.dumps(final)}\n\n")

    out.append("data: [DONE]\n\n")
    return "".join(out)


class FakeEndpoint:
    """Context manager yielding a base_url. `responder` decides every reply.

    responder(request_body, call_number) -> (status, body_text)
    or (status, body_text, extra_headers)

    It also answers `GET /api/ps`, because a merge asks the server
    what window it is serving before it sends anything, and an endpoint that
    could not answer would make every offline merge test exercise the branch
    where the guard is skipped. `served` is that answer in tokens, and `loaded`
    the model names it is given for; a test that wants the refusal to fire sets
    `served` low rather than reaching into `merge` to move a constant.
    """

    def __init__(self, responder, *, served: int = 131072,
                 loaded: tuple[str, ...] = ("test-model", "stub"),
                 loads_on_warm: bool = False,
                 vram_fraction: float | None = None,
                 ps_status: int | None = None,
                 prompt_budget: int | None = None,
                 prompt_ratio: float | None = 0.727) -> None:
        self.responder = responder
        # See `_counted_prompt`. The default is the median ratio measured over
        # the 2,200 recorded calls that carry a prompt count; `None` leaves
        # whatever the responder wrote, for the few tests that pin a usage
        # block byte for byte.
        self.prompt_ratio = prompt_ratio
        # What `/api/ps` reports is the runner's *total* allocation, and the
        # prompt shares it with the completion -- so the largest prompt a
        # server will take without trimming can be well below the figure it
        # reports. Measured on this project's own card: a
        # 4096-token total answered a ~13,000-token prompt with
        # `prompt_eval_count` 2050. `served` stays what `/api/ps` says;
        # `prompt_budget` is what the generation actually accepts, and
        # defaults to `served` so every existing test keeps the behaviour it
        # was written against.
        self.prompt_budget = served if prompt_budget is None else prompt_budget
        # `None` answers `/api/ps` normally; a status forces
        # that answer instead, for the one case a vendor's own endpoint sends
        # unprompted: a 404 because the route does not exist there at all.
        self.ps_status = ps_status
        # How much of the model the runner put in video memory, as `/api/ps`
        # reports it: `size` and `size_vram`. None leaves both out, which is
        # what every test that predates the check wants and what a server that
        # is not ollama does -- and "not reported" must not read as "on the CPU".
        self.vram_fraction = vram_fraction
        self.requests: list[dict] = []
        self.headers: list[dict] = []
        self.gets: list[str] = []
        self.probes: list[dict] = []
        # Warm-up requests to `/api/generate`, kept apart from `requests` for
        # the reason the probes are: a load is the server being asked to make a
        # model resident, not a unit of work, and counting it in `calls` would
        # make every existing test's call accounting off by one on any run that
        # found the endpoint cold.
        self.loads: list[dict] = []
        # Whether a load actually loads. False models a server that will accept
        # the request and still not have the model afterwards -- which is the
        # branch where `client._reported` has to give up rather than loop. True
        # models the ordinary cold pod: `/api/ps` is empty, then it is not.
        self.loads_on_warm = loads_on_warm
        self.streamed = 0
        self.served = served
        self.loaded = loaded
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def calls(self) -> int:
        return len(self.requests)

    def probe_answer(self, body: dict) -> str | None:
        """Answer a window probe the way a real server would, or `None`.

        `None` means this was not a probe and belongs to the responder.

        The behaviour being modelled is the one that makes the probe necessary:
        a prompt longer than the window is **trimmed and answered anyway**, and
        nothing in the response says so except the token count. So the count is
        what this gets right -- `prompt_tokens` is what the server would have
        after trimming, never more than `served` -- and the content is a
        formality, because `window.measured` does not read it. That makes
        `served` the one place a test states a window, rather than reaching into
        `window` to move a constant.

        The marker is imported rather than copied. A prompt that changed shape
        while a duplicate here did not would leave probes falling through to the
        responder, and the symptom -- one extra scripted reply consumed per
        model -- points nowhere near the cause.
        """
        from llossless import window as window_module

        messages = body.get("messages") or []
        if len(messages) != 1:
            return None
        content = messages[0].get("content") or ""
        if not content.startswith(window_module.PROBE_PREAMBLE):
            return None
        return json.dumps({
            "choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": min(len(content) // window_module.CHARS_PER_TOKEN,
                                           self.prompt_budget),
                      "completion_tokens": 1},
        })

    def _counted_prompt(self, body: str, request: dict) -> str:
        """Report a prompt count proportional to what was actually sent.

        `envelope()` writes a fixed `prompt_tokens: 100` because it is handed
        no request and cannot know better. A real server counts what it
        received, and `window.assert_prompt_not_trimmed` compares that count
        against the size the run believed it sent -- so a fixture reporting
        100 against a 3,000-token prompt is a fixture claiming a 97% trim on
        every call.

        `prompt_ratio` is what the endpoint reports as a fraction of this
        project's own `chars // CHARS_PER_TOKEN` estimate. It defaults to the
        median measured over 2,200 recorded calls, so an ordinary test call
        looks ordinary to the check. A test that wants a trim sets it low; a
        test that wants a vendor reporting nothing sets it to 0, which is what
        all 70 vendor bodies in the corpus do.

        Only ever rewrites a `usage.prompt_tokens` that is already there: a
        response deliberately built without usage keeps none, because "the
        vendor reported no usage" is its own case and the check treats it as
        UNMEASURED rather than as agreement.
        """
        from llossless import window as window_module

        if self.prompt_ratio is None:
            return body
        try:
            parsed = json.loads(body)
        except (ValueError, TypeError):
            return body
        usage = parsed.get("usage") if isinstance(parsed, dict) else None
        if not isinstance(usage, dict) or "prompt_tokens" not in usage:
            return body
        chars = sum(len(m.get("content") or "")
                    for m in (request.get("messages") or []))
        usage["prompt_tokens"] = int(
            (chars // window_module.CHARS_PER_TOKEN) * self.prompt_ratio)
        return json.dumps(parsed)

    def __enter__(self) -> str:
        endpoint = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's naming
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                body_in = json.loads(raw)

                # A window probe is the server being interrogated, not a unit
                # of work, so it is answered here and kept out of `requests`. If
                # it went to the responder it would consume a scripted reply and
                # every test's call accounting would be off by one per model.
                # `/api/generate` is ollama's load route and a different route
                # from `/v1/chat/completions`. Answered here so that `calls`
                # keeps meaning "completions asked for", which is what every
                # test that reads it is asserting about.
                if self.path.endswith("/api/generate"):
                    endpoint.loads.append(body_in)
                    name = str(body_in.get("model") or "")
                    if endpoint.loads_on_warm and name and name not in endpoint.loaded:
                        endpoint.loaded = endpoint.loaded + (name,)
                    payload = json.dumps({
                        "model": name, "done": True, "response": "",
                        "done_reason": "load",
                    }).encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(payload)))
                    self.end_headers()
                    self.wfile.write(payload)
                    return

                probe = endpoint.probe_answer(body_in)
                if probe is not None:
                    endpoint.probes.append(body_in)
                    payload = probe.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(payload)))
                    self.end_headers()
                    self.wfile.write(payload)
                    return

                endpoint.requests.append(body_in)
                endpoint.headers.append(dict(self.headers))

                result = endpoint.responder(endpoint.requests[-1], endpoint.calls)
                status, body = result[0], result[1]
                extra = result[2] if len(result) > 2 else {}
                body = endpoint._counted_prompt(body, endpoint.requests[-1])

                events = (sse(body, endpoint.requests[-1])
                          if status == 200 and endpoint.requests[-1].get("stream")
                          else None)
                if events is not None:
                    endpoint.streamed += 1
                    payload = events.encode("utf-8")
                    self.send_response(status)
                    # A responder that names its own content type gets it here
                    # too, and for a reason measured rather than imagined: a
                    # hosted proxy in front of ollama labelled a real event
                    # stream `application/x-ndjson` on 2026-08-28. A test that
                    # could not reproduce a mislabelled stream could not check
                    # that the client stopped believing the label.
                    if not any(name.lower() == "content-type" for name in extra):
                        self.send_header("Content-Type", "text/event-stream")
                    self.send_header("Content-Length", str(len(payload)))
                    for name, value in extra.items():
                        self.send_header(name, value)
                    self.end_headers()
                    self.wfile.write(payload)
                    return

                payload = body.encode("utf-8")
                self.send_response(status)
                # A responder that names its own content type gets it, and gets
                # it once: sending both leaves the client to pick, and a client
                # picking between `application/json` and `text/event-stream`
                # decides how it reads the body.
                if not any(name.lower() == "content-type" for name in extra):
                    self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                for name, value in extra.items():
                    self.send_header(name, value)
                self.end_headers()
                self.wfile.write(payload)

            def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler's naming
                endpoint.gets.append(self.path)
                if not self.path.endswith("/api/ps"):
                    self.send_error(404)
                    return
                if endpoint.ps_status is not None:
                    self.send_error(endpoint.ps_status)
                    return
                size = 1_000_000
                extra = ({} if endpoint.vram_fraction is None else
                         {"size": size,
                          "size_vram": int(size * endpoint.vram_fraction)})
                payload = json.dumps({
                    "models": [
                        {"model": name, "context_length": endpoint.served, **extra}
                        for name in endpoint.loaded
                    ]
                }).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *_args) -> None:
                pass  # the suite's output is the report, not an access log

        class Server(ThreadingHTTPServer):
            def handle_error(self, request, client_address) -> None:
                """A client that hangs up is a test, not a fault.

                The timeout tests make the client give up mid-response on
                purpose, and the write that follows raises BrokenPipeError on
                this side. Printing its traceback puts a stack trace in the
                middle of a passing suite. Anything else still prints.
                """
                if not isinstance(sys.exc_info()[1], ConnectionError):
                    super().handle_error(request, client_address)

        self._server = Server(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return f"http://127.0.0.1:{self._server.server_address[1]}/v1"

    def __exit__(self, *_exc) -> None:
        assert self._server is not None
        self._server.shutdown()
        self._server.server_close()
        assert self._thread is not None
        self._thread.join(timeout=5)


def rejects(*fields: str, status: int = 400):
    """A responder refusing the named request fields, the way an older gateway does.

    Anything it does not refuse, it honours properly — a request carrying
    `tools` gets a real tool_call back. That matters: an endpoint that accepts
    `tools` and then answers in plain content has not honoured tier 2, and the
    client is supposed to notice. Faking that as success would have hidden the
    difference between "the ladder works" and "the ladder always falls to the
    bottom rung".
    """

    def responder(body: dict, _n: int):
        for field in fields:
            if field in body:
                return status, json.dumps(
                    {"error": {"message": f"Unrecognized request argument supplied: {field}"}}
                )
        claims = json.dumps({"claims": []})
        if "tools" in body:
            return 200, envelope(claims, tool=body["tools"][0]["function"]["name"])
        return 200, envelope(claims)

    return responder
