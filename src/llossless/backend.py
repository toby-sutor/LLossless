"""The only module in this project that starts a subprocess to answer a prompt.

The second of two ways a request can be answered. `transport.py` opens a
socket; this one runs a command, writes the prompt to its stdin and reads the
answer from its stdout. It exists because both vendor APIs are metered per
token while most people hold a flat-rate subscription, and a subscription is
usually reachable only through that vendor's own CLI.

Vendor-independent on purpose. Nothing here knows what it is running: the
operator names a command, and any program that reads a prompt and writes an
answer will do. That is also the limit of what can be promised about it --
see `Settings.command` and `provenance.hosted` for what the tool stops being
able to tell you once a child process is in the loop.

**Three things are unavailable here, and none of them is a smaller version of
what the HTTP path gives.**

- *Token counts.* There is no usage block to read, so `usage.normalise` is
  handed an envelope without one and answers `None`. That is `unmeasured`,
  never zero (480), and it takes out the post-hoc overrun check with it.
- *A context window to probe.* `/api/ps` is an HTTP endpoint. `config`
  refuses a command backend that has not been told its window, because with
  the token counts gone as well there is nothing left to notice an overrun.
- *Containment.* `config.check_base_url` has no URL to inspect, and the
  suite's network containment is per-process, so a child that opens a socket
  opens it unobserved. `provenance.hosted` answers true for any command
  backend rather than letting silence imply a document stayed here.

**The envelope is synthesised, and that is the whole design.** Everything
downstream -- `structured.read_content`, `reasoned()`, `usage.normalise` --
reads an OpenAI chat-completions shape, and the cheapest correct way to add a
second backend is to answer in the shape the first one already speaks rather
than to teach four readers a second dialect.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import time

from .config import COMMAND_ENVELOPES as ENVELOPES
from .config import ENVELOPE_RAW as RAW
from .config import ENVELOPE_RESULT as RESULT
from .config import dropped_env_names
from .transport import Cancelled, Response, TransportError

# How a command's stdout is read, declared per route and never sniffed (537).
#
# RAW is what this backend has always done and stays the default: stdout is
# the answer, byte for byte. It is the only shape that works for an arbitrary
# wrapper script, which is what this backend promises to run.
#
# RESULT is the single-object envelope `claude --print --output-format json`
# writes, confirmed at 2.1.274: a `type: "result"` object whose `result` holds
# the text and whose `usage` holds the Anthropic-native token block *and*
# `server_tool_use`. A route that asks for it gets back token counts this
# backend otherwise cannot have -- two of the three things the header above
# lists as unavailable -- and the one measurement that says whether the model
# went and looked anything up.
#
# **Declared and not detected.** The answer under RAW is itself JSON -- the
# `prompt` tier asks the model for JSON -- so an envelope sniffer would be
# choosing between two JSON objects on the presence of a key, which is the
# guess this project refuses to make about record shapes anywhere else. A
# route that declares RESULT and gets something else is an error rather than a
# quiet fall back to RAW: the fall back would hand the merge an envelope to
# parse and report the confusion as a model fault.
#
# The names themselves are `config`'s, imported rather than restated. `config`
# is loaded by every offline run and this module deliberately is not, so a
# constant defined here would pull the socket module into replay and break the
# containment `acceptance_replay_never_loads_the_transport_module` holds.

# What a command is handed and what it must answer with, in one place because
# an operator writing a wrapper script needs both.
#
# stdin  the composed prompt, exactly as the HTTP path would have put in
#        `messages[0].content`, and nothing else -- no JSON envelope, no
#        arguments, no schema flag. A wrapper that needs more builds it.
# stdout the model's answer as text. This is the `prompt` tier, so the answer
#        is expected to be the JSON the prompt asked for, and it is parsed by
#        the same code that parses a hosted model's reply.
PROMPT_ON = "stdin"
ANSWER_ON = "stdout"

# How much of a failing command's stderr is quoted back. The same figure
# `transport.BODY_EXCERPT` uses for an error body, and for the same reason: a
# wrapper script's traceback is what an operator needs to see, and all of one
# is more than an error message should carry.
#
# `Settings.call_timeout` bounds the call rather than the silence within it
# here. A stream renews that clock on every chunk; a subprocess has no chunks,
# so the same figure means something stricter on this path than on the HTTP
# one -- which is why the two backends resolve different defaults out of one
# unstated setting (`config.COMMAND_TIMEOUT`, 533).
STDERR_EXCERPT = 600

# The filter itself, and why each prefix is on it, lives in `config.py` (I8,
# 680) and not here: `Provenance` has to report the same names a live call
# withheld without importing this module to ask, because this module imports
# `transport` and a replay must never load that
# (`acceptance_replay_never_loads_the_transport_module`). See
# `config.DROPPED_ENV_PREFIXES` for the reasoning behind each one, and
# `config.KEPT_CREDENTIAL_NAMES` for the one `CLAUDE_CODE_` name (680
# follow-up) the filter deliberately still hands the child: the subscription
# login token, which a `CLAUDE_CODE_` prefix drop would otherwise withhold
# along with the session markers it exists to catch.
# (`dropped_env_names` itself is imported above, beside the module's other
# `config` names.)

# Set on the child unconditionally: the auto-updater is a network call and a
# version change neither asked for nor visible to this backend, and every
# call already declares its own isolation from everything else the CLI might
# reach for (`config.command_safe_mode`, `config.stated_tools`). This is the
# same posture applied to the binary itself.
CHILD_ENV_ADDITIONS = {"DISABLE_AUTOUPDATER": "1"}


def _child_env(environ: dict | None = None) -> dict:
    """The environment `post_json` hands the child: `environ`, filtered, plus the additions.

    Never inherited whole -- `post_json` used to pass no `env=` at all, which
    handed the child every credential and every piece of session state this
    process itself was given. Kept, deliberately, by the filter this drops
    from: `HOME`, `PATH`, `USER`, `LANG`/`LC_*`, `TERM`, `XDG_*`, `TMPDIR` and
    the proxy variables -- what the CLI needs to run at all and to find its
    own subscription login, which on every platform this project targets is
    read off `HOME` (or an `XDG_CONFIG_HOME` override), never off a variable
    this backend would otherwise have dropped.
    """
    source = os.environ if environ is None else environ
    dropped = set(dropped_env_names(source))
    env = {name: value for name, value in source.items() if name not in dropped}
    env.update(CHILD_ENV_ADDITIONS)
    return env


class CommandError(TransportError):
    """The command could not be run, or answered in a way nothing can use.

    A `TransportError` because every call site already treats one as fatal,
    and because it is the same *kind* of event: the request never reached a
    model, or its answer never came back. What differs is only which of the
    two mechanisms failed.

    `result`, `api_error_status`, `api_error_code` and `terminal_reason` are
    the envelope's own classifying fields (I6), carried as attributes and not
    only folded into the message: a runner telling a usage limit or a vendor
    API error apart from an ordinary model fault reads these rather than
    re-parsing a sentence. `None` when the envelope did not parse or did not
    name one -- which is every failure this class described before 680, and
    every plain subprocess fault (a missing program, a timeout) still.
    """

    def __init__(self, message: str, *, result: str | None = None,
                api_error_status: object = None, api_error_code: object = None,
                terminal_reason: object = None) -> None:
        super().__init__(message)
        self.result = result
        self.api_error_status = api_error_status
        self.api_error_code = api_error_code
        self.terminal_reason = terminal_reason


class CommandNotFound(CommandError):
    """The named program does not exist. Almost always a typo or a PATH."""


def _classify_envelope(stdout: str) -> dict:
    """Best-effort read of a failing call's stdout as the JSON result envelope.

    For a call that has already failed by another signal -- a non-zero exit,
    or `is_error` -- and never raises on its own account: a stdout that is not
    that shape just has nothing more to classify, and the caller's own message
    about the exit or the error stands unchanged.

    Returns `result` (truncated to `STDERR_EXCERPT`, the same figure a failing
    stderr is quoted at, and for the same reason), `api_error_status`,
    `api_error_code`, `terminal_reason` and `subtype`, each present only when
    the envelope named it. This is what turns "'claude' exited 1" into
    something a runner can tell a usage limit or a vendor API error apart from
    (I6): the real 2.1.274 probe carried `terminal_reason: "api_error"` in
    stdout on a non-zero exit, and this backend used to quote stderr alone and
    drop it.
    """
    try:
        envelope = json.loads(stdout)
    except ValueError:
        return {}
    if not isinstance(envelope, dict):
        return {}
    found: dict = {}
    result = envelope.get("result")
    if isinstance(result, str) and result:
        found["result"] = result[:STDERR_EXCERPT]
    for key in ("api_error_status", "api_error_code", "terminal_reason", "subtype"):
        value = envelope.get(key)
        if value is not None:
            found[key] = value
    return found


def _classified_message(prefix: str, classified: dict) -> str:
    """`prefix`, plus whatever `_classify_envelope` found, as one message."""
    message = prefix
    if classified.get("result"):
        message += f"\n{classified['result']}"
    tags = ", ".join(f"{key}={classified[key]}" for key in
                     ("terminal_reason", "api_error_status", "api_error_code")
                     if classified.get(key) is not None)
    if tags:
        message += f" ({tags})"
    return message


def _classified_error(prefix: str, stdout: str) -> CommandError:
    """`CommandError(prefix)`, enriched with `stdout`'s envelope where there is one."""
    classified = _classify_envelope(stdout)
    return CommandError(
        _classified_message(prefix, classified),
        result=classified.get("result"),
        api_error_status=classified.get("api_error_status"),
        api_error_code=classified.get("api_error_code"),
        terminal_reason=classified.get("terminal_reason"),
    )


def messages_to_prompt(messages: list[dict]) -> str:
    """Flatten a chat-completions message list into one prompt.

    A command backend has no roles to give a CLI: there is one stdin. Every
    request this tool makes is a single user message -- `structured.build_body`
    composes the system instructions into it -- so this is a join over a list
    of one in every case the tool itself produces, written as a join because a
    silent `messages[0]` would turn a future second message into a dropped
    instruction rather than an error.
    """
    parts = [str(message.get("content", "")) for message in messages
             if str(message.get("content", "")).strip()]
    if not parts:
        raise CommandError("nothing to send: the request carried no content")
    return "\n\n".join(parts)


def envelope_for(content: str, server_tool_use: dict | None = None,
                 num_turns: int | None = None,
                 answered_by: dict | None = None) -> dict:
    """The chat-completions shape, carrying `content` and admitting no tokens.

    No token counts, ever, on this path. A `RESULT` envelope has them --
    `input_tokens`, `output_tokens`, `cache_read_input_tokens` -- and they are
    deliberately left where they were found (537). Under Anthropic's spelling
    `input_tokens` is what was *not* served from cache, and a measured call in
    this project routinely reads 908 uncached against 5,370 cache reads; the
    post-hoc trim guard compares the reported prompt count against the
    estimate and refuses at half, so lifting the uncached remainder as "the
    prompt" would refuse an honest call almost every time. Summing the two
    instead is wrong the other way for every vendor whose `prompt_tokens`
    already includes its cache reads, which is most of them, and would make
    the guard lenient on the path it was measured for. Getting that right is a
    convention question per vendor and is not this feature's job; leaving the
    counts unmeasured keeps the header's third bullet true.

    So the block carries two things that are not token counts, and only when
    the command reported them.

    `server_tool_use` is the first, and it has one convention. **It is also
    blind to this backend**, which was measured after it was added (548): it
    counts Anthropic's *server-side* web tools, the CLI's own `WebFetch` runs
    locally in the CLI process, and a call that demonstrably fetched still
    reported `{"web_search_requests": 0, "web_fetch_requests": 0}`. It is
    carried anyway, because an endpoint reached through a compatibility
    surface may genuinely fill it in, and a reader of a report has to be able
    to see a zero that came from a vendor rather than from a gap.

    `num_turns` is the second and is the one that works here. A tool call costs
    a round trip, so it costs a turn, and a fetch costs two tool calls because
    `WebFetch` is deferred: `ToolSearch` loads it, then it runs, then the model
    answers -- three turns, against one or two for a call that retrieved
    nothing (564, correcting 548's two). Under the isolated argv nothing is
    deferred and a fetch is two turns; the floor follows the argv (610). It is
    a count of *turns* and not of fetches, which is what every reader of it says.

    `usage.normalise` finds no token field in either and answers None, so the
    call stays `unmeasured` on cost -- which is what it is.

    `answered_by` is not usage and sits beside `choices`, not inside `usage`:
    which model ids the command's own envelope named, and which of them wrote
    the answer (`models_named`). No HTTP endpoint writes a key of that name,
    so `usage.answered_by` reading it back is scoped to this backend by
    construction, and a recorded corpus without it reads as it always did.
    """
    envelope = {
        "choices": [{"message": {"role": "assistant", "content": content},
                     "finish_reason": "stop"}],
    }
    used: dict = {}
    if server_tool_use:
        used["server_tool_use"] = server_tool_use
    # `is not None` rather than truthiness: `num_turns: 0` is not a command
    # that failed to report, and folding the two together is the confusion
    # `usage.py`'s whole unknown-is-not-zero rule exists to prevent.
    if num_turns is not None:
        used["num_turns"] = num_turns
    if used:
        envelope["usage"] = used
    if answered_by:
        envelope["answered_by"] = answered_by
    return envelope


def models_named(model_usage, usage=None) -> dict | None:
    """Which model ids a result envelope's `modelUsage` names, and which answered.

    The route names an alias -- `--model opus` -- and the CLI resolves it to
    whatever it maps that alias to on the day, so a report that records only
    the alias cannot say which model a figure came from once a new version
    ships under it. `modelUsage` is keyed by the ids that really ran.

    **More than one id is normal**, so every id is kept. The CLI runs
    `claude-haiku-4-5-20251001` for its own steps and for summarising what
    `WebFetch` and `WebSearch` bring back, and a merge may hand work to a
    subagent on another model: a measured Opus merge at `xhigh` named Haiku at
    14,938 output tokens and `claude-sonnet-5` at 34,498 beside Opus's 33,704.

    **`output` is the id whose counts are the envelope's own `usage` block**,
    which is the main conversation's, the one that wrote the answer: its
    `output_tokens` and, when both say, its `input_tokens`. Not the id with the
    most output tokens -- that named a subagent's Sonnet above, and Haiku on a
    verify call whose whole answer was 11 tokens beside a 12-token side call.
    One id named is its own author. Otherwise, when no id's counts are the
    block's, or two are, `output` is None: the envelope cannot settle it, and
    naming one would be a guess.

    Names only, never the counts. `envelope_for` says why no token count
    crosses this backend, and a per-model count would be one.
    """
    if not isinstance(model_usage, dict):
        return None
    models = sorted(str(name) for name in model_usage if str(name).strip())
    if not models:
        return None
    if len(models) == 1:
        return {"models": models, "output": models[0]}

    def count(block, name):
        value = block.get(name) if isinstance(block, dict) else None
        return value if isinstance(value, int) and not isinstance(value, bool) else None

    said_out = count(usage, "output_tokens")
    said_in = count(usage, "input_tokens")
    authors = [] if said_out is None else [
        name for name in models
        if count(model_usage.get(name), "outputTokens") == said_out
        and (said_in is None or count(model_usage.get(name), "inputTokens") in (None, said_in))]
    return {"models": models, "output": authors[0] if len(authors) == 1 else None}


def read_result(stdout: str, named: str
                ) -> tuple[str, dict | None, int | None, dict | None]:
    """The text, the tool-use block, the turn count and the models in a `RESULT` envelope.

    `named` is the program's basename, for the message only. Every refusal
    here says what was configured and what arrived, because the operator who
    meets one has a route declaring an envelope its command does not produce,
    and the repair is on the route rather than in the prompt.
    """
    try:
        envelope = json.loads(stdout)
    except ValueError as exc:
        raise CommandError(
            f"{named!r} is configured to answer with a JSON result envelope "
            f"and wrote something that is not JSON: {exc}. Either the command "
            f"is missing its output-format argument, or the route should "
            f"declare the {RAW!r} envelope."
        ) from exc
    if not isinstance(envelope, dict):
        raise CommandError(
            f"{named!r} answered with JSON carrying no `result` key, so this "
            f"is not the result envelope the route declared. Either the "
            f"command is missing its output-format argument, or the route "
            f"should declare the {RAW!r} envelope."
        )
    # `is_error` is the envelope's own verdict on the turn and it is honoured
    # rather than second-guessed: a CLI that says the turn failed has said
    # something this backend cannot learn any other way, and passing the text
    # on would file a refusal as a model answer.
    #
    # Checked before the `result` key's presence below, and not after (I6): a
    # turn that ends `error_max_turns` carries no `result` at all, and asking
    # the presence question first reported that real failure as a
    # misconfigured route -- the same sentence a genuinely wrong
    # `--output-format` gets, which sent the operator looking at the wrong
    # thing.
    if envelope.get("is_error"):
        raise _classified_error(
            f"{named!r} reported the turn as an error "
            f"({envelope.get('subtype') or 'no subtype given'})",
            stdout,
        )
    if "result" not in envelope:
        raise CommandError(
            f"{named!r} answered with JSON carrying no `result` key, so this "
            f"is not the result envelope the route declared. Either the "
            f"command is missing its output-format argument, or the route "
            f"should declare the {RAW!r} envelope."
        )
    # One sub-block, not the whole `usage`. See `envelope_for` for why the
    # token counts stay where they are.
    used = envelope.get("usage")
    tools = used.get("server_tool_use") if isinstance(used, dict) else None
    # Top level, beside `result` and not inside `usage`: that is where the CLI
    # writes it. A `bool` is excluded for the reason it is excluded everywhere
    # a count is read here -- `True` is an `int` in Python and `num_turns: true`
    # is a broken envelope rather than one turn.
    turns = envelope.get("num_turns")
    return (str(envelope.get("result") or ""),
            tools if isinstance(tools, dict) else None,
            int(turns) if isinstance(turns, int) and not isinstance(turns, bool)
            else None,
            # Top level too, beside `num_turns`: where the CLI writes it.
            models_named(envelope.get("modelUsage"), used))


# How long a cancelled program is given to exit on SIGTERM before SIGKILL
# (639). Long enough for a CLI to write its own state and exit cleanly, short
# enough that "cancel" still means stopped before anybody wonders.
TERMINATE_GRACE_SECONDS = 5.0

# How often a cancellable run looks at its cancel flag while the program works.
CANCEL_POLL_SECONDS = 0.2


def _stop(process: subprocess.Popen, grace: float) -> None:
    """SIGTERM the program's whole process group, then SIGKILL after `grace`.

    The group, not the pid: a CLI such as `claude` starts children of its own,
    and a SIGTERM to the parent alone can leave one of them running and
    talking to its vendor. `start_new_session=True` at spawn is what makes the
    program the leader of a group of its own, so this reaches nothing else.
    """
    import signal
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return
    try:
        process.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            return
        process.wait()


def run_cancellable(argv: list[str], *, input: str, timeout: float, cancel,
                    grace: float = TERMINATE_GRACE_SECONDS,
                    on_start=None, env: dict | None = None) -> subprocess.CompletedProcess:
    """`subprocess.run(..., capture_output=True, text=True)` that `cancel` can stop.

    `cancel` is a `threading.Event`. While the program runs it is looked at
    every `CANCEL_POLL_SECONDS`; once it is set the program's group is
    stopped (`_stop`) and `Cancelled` is raised. The whole-call `timeout`
    keeps `subprocess.run`'s contract: the program is stopped the same way and
    `TimeoutExpired` is raised, which `post_json` words exactly as before.
    `on_start(pid)` is for the suite, which asserts the process is gone.

    `env`, like `subprocess.run`'s own keyword, replaces the child's whole
    environment rather than adding to the parent's (I8) -- `None` is the one
    value that still means "inherit everything", and `post_json` never passes
    that value here.
    """
    process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True,
                               start_new_session=True, env=env)
    if on_start is not None:
        on_start(process.pid)
    deadline = time.monotonic() + timeout
    # The prompt goes in on the first `communicate` only: a retry after its
    # timeout keeps writing what is left and refuses to be handed it again.
    pending: str | None = input
    while True:
        if cancel.is_set():
            _stop(process, grace)
            process.communicate()
            raise Cancelled(f"the program was stopped (pid {process.pid}, exit "
                            f"{process.returncode}) before it answered")
        left = deadline - time.monotonic()
        if left <= 0:
            _stop(process, grace)
            process.communicate()
            raise subprocess.TimeoutExpired(argv, timeout)
        try:
            stdout, stderr = process.communicate(
                input=pending, timeout=min(CANCEL_POLL_SECONDS, left))
        except subprocess.TimeoutExpired:
            pending = None
            continue
        return subprocess.CompletedProcess(argv, process.returncode, stdout, stderr)


def post_json(
    command: str,
    payload: dict,
    *,
    timeout: float,
    host: str,
    model: str,
    envelope: str = RAW,
    run=subprocess.run,
    cancel=None,
) -> Response:
    """Answer `payload` by running `command`, in `transport.post_json`'s shape.

    Same return type and same failure contract as the HTTP path, so the call
    site in `client.py` differs by which function it names and nothing else.

    `run` is injected for the tests, which is not a seam for production use:
    every call here goes through it, so a test that replaces it proves the
    argument assembly and the envelope, and a test that does not replace it
    really does start a process.

    `cancel`, a `threading.Event`, is the web server's (639): with one, the
    program runs under `run_cancellable`, and setting it stops the program's
    process group, SIGTERM then SIGKILL, and raises `Cancelled`. Without one
    nothing here changes, which is every command-line run.
    """
    argv = shlex.split(command)
    if not argv:
        raise CommandError("LLOSSLESS_COMMAND is empty after parsing")
    # The basename in every message below, never `argv[0]`. An operator who
    # names an absolute path has put their home directory in the command, and
    # these strings reach stderr, a captured log, and from there a decision
    # entry -- which is the route 297 exists about. The full path stays in the
    # environment where it was set.
    named = os.path.basename(argv[0]) or argv[0]
    prompt = messages_to_prompt(payload.get("messages") or [])
    # Built explicitly rather than inherited (I8): see `_child_env` for what
    # is dropped and kept, and why.
    child_env = _child_env()

    started = time.monotonic()
    try:
        done = (run(argv, input=prompt, capture_output=True, text=True,
                    timeout=timeout, env=child_env) if cancel is None else
                run_cancellable(argv, input=prompt, timeout=timeout, cancel=cancel,
                                env=child_env))
    except FileNotFoundError as exc:
        raise CommandNotFound(
            f"no such program: {named!r}. LLOSSLESS_COMMAND names the "
            f"program to run, and it has to be on PATH or an absolute path."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        # The mechanism, then the knob. The first version of this message
        # explained why the bound is strict here and left the reader with
        # nothing to do about it -- which is how the operator met it: a
        # correct sentence about a subprocess, and no sentence about the
        # setting that would have let the call finish (533).
        raise CommandError(
            f"{named!r} produced nothing for {timeout:.0f}s and was stopped. "
            f"A subprocess has no stream to renew the clock, so this bounds "
            f"the whole call rather than the silence within it, and a command "
            f"backend is slower by nature: it answers at the `prompt` tier, "
            f"where the model writes the whole document out as text. A "
            f"measured merge took about 180s a call. Raise it with --timeout "
            f"or LLOSSLESS_TIMEOUT; on the web server it is the route's own "
            f"`timeout` in commands.json."
        ) from exc
    except OSError as exc:
        raise CommandError(f"could not run {named!r}: {exc}") from exc
    latency_ms = int((time.monotonic() - started) * 1000)

    if done.returncode != 0:
        excerpt = (done.stderr or "").strip()[:STDERR_EXCERPT]
        # stdout is parsed too, not only stderr (I6): a CLI that exits
        # non-zero can still have written the result envelope, and that is
        # where a usage limit or a vendor API error names itself
        # (`api_error_status`, `api_error_code`, `terminal_reason`) --
        # `arms/2026-09-26/opus-max/probe-2.1.274/calls.json` is the real
        # shape this backend used to discard by quoting stderr alone.
        raise _classified_error(
            f"{named!r} exited {done.returncode} for model {model} at {host}"
            + (f"\n{excerpt}" if excerpt else ""),
            done.stdout or "",
        )

    content = done.stdout or ""
    # An empty answer is raised here rather than passed on as an envelope with
    # an empty content field. Both end at the same retry, but only this one can
    # say which mechanism was silent -- and a command that exits 0 saying
    # nothing is a different fault from a model that answered blankly.
    if not content.strip():
        excerpt = (done.stderr or "").strip()[:STDERR_EXCERPT]
        raise CommandError(
            f"{named!r} exited 0 and wrote nothing to {ANSWER_ON}. The "
            f"prompt was written to its {PROMPT_ON}; a wrapper that does not "
            f"read it exits 0 with nothing to say, which is this exactly"
            + (f". It did write to stderr:\n{excerpt}" if excerpt else "")
        )

    tool_use = None
    turns = None
    answered = None
    reported = None
    if envelope == RESULT:
        content, tool_use, turns, answered = read_result(content, named)
        reported = cli_timing(done.stdout)
        # A result envelope whose `result` is empty is the same fault as an
        # empty stdout, one layer in, and it is raised here rather than passed
        # on for the same reason: the caller can then say which mechanism was
        # silent instead of reporting a model that answered blankly.
        if not content.strip():
            raise CommandError(
                f"{named!r} answered with a result envelope whose `result` is "
                f"empty"
            )
    elif envelope != RAW:
        raise CommandError(
            f"unknown command envelope {envelope!r}; the envelopes are "
            f"{', '.join(ENVELOPES)}"
        )

    # One attempt, so the answering attempt is the whole call (681). What the
    # program did inside that call -- the CLI's own retries and backoff among
    # them -- is invisible from here and is in this figure; `cli_timing` is
    # the program's own account, where its envelope gave one.
    return Response(
        status=200,
        body=json.dumps(envelope_for(content, tool_use, turns, answered)),
        latency_ms=latency_ms,
        attempts=1,
        answer_ms=latency_ms,
        cli_timing=reported,
    )


def cli_timing(stdout: str) -> dict | None:
    """`duration_ms` and `duration_api_ms` off a `RESULT` envelope, or `None` (681).

    Kept off the synthesised envelope, and so out of any cassette body: a
    call's time is how it ran, not what it answered, and a recording that
    carried it would make a replay claim a time it never took. It reaches the
    live ledger row only, beside `latency_ms`, through `Response.cli_timing`.

    **Neither figure excludes retries.** Read off the 2.1.283 binary: each
    request is timed twice, `durationMsIncludingRetries` and `durationMs`, and
    `recordApiDuration` keeps both totals, but the result envelope's
    `duration_api_ms` is `totalAPIDuration()` -- the *including-retries* sum,
    over every model request of the turn, side calls included, which is why
    it can exceed `duration_ms` (a committed Opus envelope: 108,175 against
    107,888). `duration_ms` is the turn's wall time. The without-retries total
    is written to the CLI's own cost state and never to this envelope.
    Recorded as the CLI says them, never corrected: absent when a field is
    missing or not an integer, never zero.
    """
    try:
        envelope = json.loads(stdout)
    except ValueError:
        return None
    if not isinstance(envelope, dict):
        return None
    found = {key: envelope[key] for key in ("duration_ms", "duration_api_ms")
             if isinstance(envelope.get(key), int)
             and not isinstance(envelope.get(key), bool)}
    return found or None
