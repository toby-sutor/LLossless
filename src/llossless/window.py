"""What context window is this endpoint actually serving?

The question has to be asked rather than answered from a constant, because the
answer is model-dependent from a single server setting. ollama serves
`min(the model's native maximum, OLLAMA_CONTEXT_LENGTH)`, so one server
configured at 65,536 serves 40,960 to a model whose native ceiling is 40,960 and
65,536 to one that reaches 262,144. A number written into this file would be
right for whichever model was current the day it was written.

## What can be read, and what has to be measured

`/api/ps` reports `context_length` for each loaded model. It carries `name`,
`model`, `size`, `digest`, `details`, `expires_at`, `size_vram` and
`context_length`, and nothing about how the runner divides that figure — so it
is an **upper bound** on what one request gets, not the per-request window, and
the difference between the two is invisible in the response.

**How the failure looks when the report is wrong.** ollama does not refuse a
prompt that overruns the window. It trims it and answers anyway, and the answer
carries no sign of it — the model speaks confidently about a document whose
beginning it was never shown. Measured on this project's pod on 2026-08-17: a
prompt the server counted at 20,482 `prompt_tokens` and a prompt it counted at
40,016 both came back normally, and a prompt of about 42,000 tokens came back
counted at 20,482 as well. The trim keeps the back half of the window, so the
count does not rise past the ceiling and then stop — it **falls to half** the
moment the prompt overruns, which is a signature a caller can test for.

So this module reports two different things and never conflates them:

  `reported()`  what the endpoint says it allocated. An upper bound on the
                per-request window, and equal to it on this pod.
  `measured()`  a prompt of that size sent, and the endpoint's own
                `prompt_tokens` read back to see whether the whole of it
                arrived. Authoritative, costs one large call per model, and the
                only figure that is safe to pass a run on.

**What `measured()` deliberately does not do is ask the model anything.** An
earlier version buried a code near the front of the prompt and checked whether
it came back. That measures retrieval and truncation together and cannot
separate them: this endpoint's models lose a code at 2% depth in a 20,000-token
log of near-identical records while having been shown every one of them. Worse,
that probe sized its prompts at `CHARS_PER_TOKEN`, which is a prose figure, and
its own structured filler tokenizes at about half that — so every prompt it built
overran the window it was asking about, was trimmed to half, and reported the
half as the window. Both models came back at exactly 0.5 of their report, which
looked like a parallel-slot divisor and was a units error. `prompt_tokens` is a
number the server computes, and reading it costs one token of generation.

`guard()` takes whichever `Window` it is handed and says which kind it was in
the refusal. The asymmetry is the point: refusing on `reported` is sound,
because an upper bound that is already too small is conclusive. **Passing on
`reported` is not**, and `passing_is_sound()` exists so a caller has to make
that distinction deliberately rather than by forgetting to.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit


# Local, not imported from `merge`: `merge` imports this module, and this is only
# the seed for the calibration call below -- the ratio that actually sizes a
# probe is measured against the endpoint, because it depends on the filler.
# Sharing `merge`'s constant would tie the two together for no gain and invert
# the dependency.
CHARS_PER_TOKEN = 3

# The first line of a probe prompt. Named so that a test double can recognise a
# probe without copying the string: a copy that fell out of step would send
# probes somewhere they were never meant to go, and the symptom would point
# nowhere near the cause.
PROBE_PREAMBLE = "Below is a log. Do not read it; this call measures the window."

# How much of the candidate window a probe fills. Under 1.0 because the prompt
# is built from a character count and a measured ratio, and a build that
# overshot by one line would be trimmed and read as a window half the size. The
# slack is the tolerance on that arithmetic, not a claim about the server.
PROBE_FILL = 0.97

# How much of the prompt must come back counted for it to have arrived whole.
# The trim this detects halves the count, so anything near 1.0 separates the two
# cases; the margin is for the chat template and for the ratio's own error.
INTACT = 0.95


class WindowUnknown(RuntimeError):
    """The endpoint would not say what it is serving, or is serving nothing.

    `loadable` separates the one cause a caller can do something about from the
    four it cannot. A model that is simply not resident is fixed by loading it;
    a `/api/ps` that answers with something other than JSON, two models whose
    names differ only in case, and a `context_length` that is not a positive
    integer are all facts about the endpoint that another request will repeat.
    Only the first is worth a second attempt, and a caller that retried on the
    exception class alone would send a load request at an endpoint that had just
    told it something quite different.
    """

    def __init__(self, message: str, *, loadable: bool = False) -> None:
        super().__init__(message)
        self.loadable = loadable


class WindowUnmeasurable(RuntimeError):
    """The endpoint does not expose `/api/ps` at all.

    Kept apart from `WindowUnknown` on purpose. `WindowUnknown` is an endpoint
    that answers `/api/ps` and has nothing useful to say -- wrong JSON, no
    matching model, nothing resident -- and one of those causes is worth a load
    request, because the model might simply not be up yet. A 404 on the route
    itself is a fact about the endpoint's shape, not its inventory: no request
    fixes a route that does not exist, so this is never `loadable` and is never
    handed to `warm()`.

    This was found on a vendor: `merge` cannot reach one at all,
    because `served_window` asked a question only ollama answers and the
    vendor's 404 was fatal. Raising `WindowUnmeasurable` instead of a bare
    `HTTPStatusError` lets `served_window` recognise "this endpoint cannot say"
    as its own outcome -- proceed without the preflight guard, and say so --
    rather than treating every failure to reach `/api/ps` as a run-ending fault.
    """


class BudgetExceedsWindow(RuntimeError):
    """The request cannot fit and has therefore not been sent.

    Raised before the first byte goes out, which is the whole value of it. The
    failure it replaces is silent: ollama truncates a prompt that overruns the
    window rather than refusing it, so the model is shown a document with its
    beginning cut off and answers confidently about the part it can see. The
    output half fails differently and just as quietly -- a merge cut at
    `max_tokens` is an unterminated JSON string, which at least errors, but it
    errors after the generation has been paid for.
    """


# Where a window figure came from, and the three are not interchangeable:
#
#   measured   a prompt of that size was sent and the endpoint's own
#              `prompt_tokens` came back whole. Authoritative.
#   reported   `/api/ps` said so. An upper bound on the per-request window, so
#              a failure against it is conclusive and a pass against it is not.
#   stated     an operator declared it, because the endpoint has no route that
#              can be asked. Nothing confirmed it and nothing sent a probe.
#
# Named as a tuple so a fourth value cannot appear without this list moving,
# and so `passing_is_sound` below is a lookup against the vocabulary rather
# than a string comparison somebody has to remember to update.
SOURCES = ("measured", "reported", "stated")


@dataclass(frozen=True)
class Window:
    """A served window and the provenance of the number."""

    tokens: int
    source: str  # one of SOURCES
    model: str
    detail: str = ""
    # Where the runner put the weights, when it said: "GPU", "CPU", "62% GPU",
    # or "" for an endpoint whose answer did not carry the figures. Empty is
    # not "CPU": a caller that warned on the absence of evidence would warn
    # about every endpoint that is not ollama.
    placement: str = ""
    # `details.quantization_level` as `/api/ps` reports it -- "Q4_K_M",
    # "MXFP4", or "" where the endpoint did not say. Carried here because it
    # arrives in the response this module already parses: the README said
    # reading it "needs `/api/show`, and no such call has been written", and
    # that was wrong in the direction that costs a request.
    # Empty is "not reported", never a guess from the tag -- two models on one
    # tag can be served at different levels, which is the whole reason the
    # registrations say to read it per arm rather than assume it.
    quantization: str = ""

    def __str__(self) -> str:
        return f"{self.tokens} tokens ({self.source}) for {self.model}"


def _root(base_url: str) -> str:
    """The server root, from an OpenAI-compatible base URL.

    `base_url` ends in `/v1` by convention; ollama's own status API sits beside
    it at the root. Rebuilt through `urlsplit` rather than by string surgery so
    that a base URL carrying a path prefix -- which the hosted deployments do --
    keeps the prefix and loses only the `/v1`.
    """
    parts = urlsplit(base_url)
    path = parts.path.rstrip("/")
    if path.endswith("/v1"):
        path = path[: -len("/v1")]
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def placement(entry: dict) -> str:
    """Where the runner loaded this model, from `/api/ps`'s own two figures.

    `size` is the whole resident model and `size_vram` is the part of it in
    video memory, so their ratio is what `ollama ps` prints in its PROCESSOR
    column. It is worth reading because a container that has lost its GPU does
    not fail: it loads on the CPU and answers, twenty to fifty times slower,
    and the symptom reaching the operator is a proxy timeout with no cause in
    it. Measured on this project's pod on 2026-08-28: a 27B model on the CPU
    took the whole 120-second window and returned HTTP 524 from Cloudflare,
    whose body says only that the origin was slow.

    Returns "" when either figure is missing or nonsense. An endpoint that does
    not report the split has not reported a CPU load.
    """
    size, vram = entry.get("size"), entry.get("size_vram")
    if not isinstance(size, int) or not isinstance(vram, int) or size <= 0 or vram < 0:
        return ""
    if vram <= 0:
        return "CPU"
    if vram >= size:
        return "GPU"
    return f"{round(100 * vram / size)}% GPU"


def reported(settings, model: str, *, role: str | None = None) -> Window:
    """What the endpoint says it has allocated for `model`, from `/api/ps`.

    Raises `WindowUnknown` when the model is not loaded. That is deliberate and
    not a fallback to a default: a model that is not resident has no window, and
    guessing one for it is exactly the hard-coding this module exists to avoid.
    The caller's remedy is to send one small request first, which loads it.
    """
    # Imported here rather than at module scope, for the reason `client._live`
    # gives: a replay run must be able to import everything it needs without
    # loading the module that can open a socket. `merge` imports this one
    # unconditionally, so a module-scope import here would put transport back
    # into the replay path through the side door.
    from . import transport

    # `base_url_for`, not `base_url`: a role can be served
    # somewhere else, and probing the wrong host reports the wrong window.
    url = f"{_root(settings.base_url_for(role))}/api/ps"
    try:
        response = transport.get_json(
            url,
            api_key=settings.api_key(role),
            timeout=settings.call_timeout,
            ca_bundle=settings.ca_bundle,
            host=settings.endpoint_name,
        )
    except transport.HTTPStatusError as exc:
        # Tested on the status the endpoint actually answered with, not on
        # what the endpoint is named or configured as. A 404 on this exact
        # route is `/api/ps` itself not existing; every other status -- 401,
        # 500, a proxy's 502 -- is a fact about this attempt and stays fatal,
        # because none of them says "this endpoint has no such route".
        if exc.status == 404:
            raise WindowUnmeasurable(
                f"{settings.endpoint_name} answered /api/ps with HTTP 404: this "
                f"endpoint does not expose it, so the served window cannot be "
                f"measured here."
            ) from exc
        raise
    try:
        loaded = json.loads(response.body).get("models") or []
    except ValueError as exc:
        raise WindowUnknown(
            f"{settings.endpoint_name} answered /api/ps with something that is not JSON"
        ) from exc

    names = [str(entry.get("model") or entry.get("name") or "") for entry in loaded]
    # An exact match first, then a match on case alone. A model tag is
    # case-insensitive to the server -- it resolves `qwen3:8B` and generates
    # from it without comment -- so refusing the window for a spelling the
    # endpoint accepts reports "no such model" about a model that is answering
    # requests, and the guard that depends on this figure then cannot run.
    # Matching on case alone recovers that.
    #
    # Two entries differing only in case would make the case-insensitive answer
    # a guess, so that case refuses rather than picking one.
    matched = [(entry, name) for entry, name in zip(loaded, names) if name == model]
    if not matched:
        folded = model.casefold()
        matched = [(entry, name) for entry, name in zip(loaded, names)
                   if name.casefold() == folded]
        if len(matched) > 1:
            raise WindowUnknown(
                f"{settings.endpoint_name} has {len(matched)} models whose names differ from "
                f"{model} only in case ({', '.join(name for _, name in matched)}); "
                f"name the one you mean exactly"
            )
    for entry, name in matched:
        length = entry.get("context_length")
        if not isinstance(length, int) or length <= 0:
            raise WindowUnknown(
                f"{settings.endpoint_name} has {model} loaded but reported "
                f"context_length={length!r}"
            )
        detail = ("/api/ps context_length, which is the runner's total "
                  "allocation; the per-request window is this divided by "
                  "OLLAMA_NUM_PARALLEL, which no response reports")
        if name != model:
            # Named rather than normalised away: the run asked for one spelling
            # and the endpoint holds another, and a reader comparing this figure
            # against the configured model should be able to see that.
            detail += f"; requested as {model}, the endpoint spells it {name}"
        return Window(tokens=length, source="reported", model=model, detail=detail,
                      placement=placement(entry),
                      quantization=str((entry.get("details") or {}).get(
                          "quantization_level") or ""))

    raise WindowUnknown(
        f"{settings.endpoint_name} has no model named {model} loaded"
        + (f"; loaded: {', '.join(n for n in names if n)}" if any(names) else
           " and nothing else either"),
        loadable=True,
    )


def banner_window(settings, model: str) -> str | None:
    """The served window for a startup banner, or `None` if it cannot be shown.

    Ordinarily a run learns about the window at per-call
    preflight, after documents are read and prompts loaded -- a correct
    refusal, but a late one. This reuses `reported()`, the one call that
    already exists for the purpose, rather than adding a second mechanism.

    Three reasons `None` is returned instead of raised, and none of them is
    treated as an error here -- each is a normal state a banner has to survive:

      not loaded    `WindowUnknown(loadable=True)`. This does *not* trigger a
                    load: warming a large model just to print a banner line
                    would turn a cheap status check into the expensive
                    operation the banner exists to warn about, before the run
                    has asked for one document. The first real call still
                    warms it, exactly as it does today.
      no `/api/ps`  `WindowUnmeasurable`, a vendor endpoint. Not an error --
                    vendor endpoints have no such route, and the run proceeds
                    exactly as it always has.
      offline       `settings.replay_dir` or `settings.dry_run`. Neither sends
                    anything anywhere, and `reported()` opens a socket; this
                    function must not be the one place in an offline run that
                    does.

    A **stated** window short-circuits the request: the operator has already
    said what this endpoint serves, so the banner prints that and asks nothing.
    Not an optimisation -- on the endpoints a stated window exists for,
    `/api/ps` is a 404, and sending one per run to print a line nobody needed
    is the kind of request this project counts. It prints as `stated` because
    this line is the first line of every captured log, and a declared figure
    that reads there as a measured one is the confusion this whole mechanism is
    written to avoid.
    """
    if settings.replay_dir is not None or settings.dry_run:
        # Before the stated window, and deliberately: an offline run is
        # constrained by nothing, and a banner announcing a window over a run
        # that sends no request would describe a guard that did not happen.
        return None
    if settings.window is not None:
        return f"{settings.window:,} (stated)"
    try:
        return f"{reported(settings, model).tokens:,}"
    except (WindowUnknown, WindowUnmeasurable):
        return None


# How long the endpoint is asked to keep a model it was warmed into loading. A
# run's own calls refresh it, so this only has to outlast the gap between the
# warm-up and the first real request; ollama's own default is five minutes and
# there is no reason for this to differ from it.
KEEP_ALIVE = "5m"


def warm(settings, model: str, *, keep_alive: str = KEEP_ALIVE,
         role: str | None = None) -> bool:
    """Load `model` on the endpoint. Returns whether it can be re-probed.

    `reported` above says the caller's remedy is to send one small request
    first. This is that remedy, performed rather than described -- an operator
    whose pod has gone cold got a merge step that errored after 137 seconds and
    a sentence telling them to do by hand what the tool could have done itself.

    An empty prompt with an explicit `keep_alive` is ollama's documented way of
    loading a model without generating from it, so this costs a load and not a
    completion. It is the third method this project sends to the configured
    endpoint and, like `/api/ps`, it goes to that endpoint and nowhere else and
    carries no document.

    **This is not a role call and must never be counted as one.** It is not
    keyed into a cassette, so it cannot be recorded or replayed; it is not a
    `client.complete`, so it is outside `--max-calls`; and the caller counts it
    separately, because a run that had to warm its endpoint and a run that found
    it warm are two different runs and the record should say which.

    Returns False rather than raising on every failure, because every failure
    here has the same meaning to the caller -- the model still cannot be probed
    -- and the message the caller should print is the one `reported` already
    raises. A load slower than `settings.call_timeout` is one of those failures: the
    request gives up, this returns False, and the operator sees the original
    error, which is the right outcome to fix with a larger --timeout rather than
    with a second guess from here.
    """
    from . import transport

    try:
        transport.post_json(
            f"{_root(settings.base_url_for(role))}/api/generate",
            {"model": model, "prompt": "", "keep_alive": keep_alive},
            api_key=settings.api_key(role),
            timeout=settings.call_timeout,
            ca_bundle=settings.ca_bundle,
            host=settings.endpoint_name,
            model=model,
        )
    except transport.TransportError:
        return False
    return True


def stated(tokens: int, model: str, *, declared_by: str) -> Window:
    """The window an operator declared, for an endpoint that cannot be asked.

    **This is not a default and the difference is the whole of why it exists.**
    A default is a number this file chose; nothing here chooses anything. The
    figure comes from a person who knows what their endpoint serves, for the
    case `reported()` structurally cannot reach -- a vendor with no `/api/ps`,
    where the alternatives were to refuse the run (which is what `decompose`
    and `verify` do today) or to proceed unguarded.

    **No probe is sent.** `measured()` confirms a reported figure by spending a
    calibration generation plus a probe at 97% of it, per model per run. On a
    metered vendor with a 200,000-token window that is an expensive preflight
    for a number nobody disputed, and it would be charged before the run's
    first real call. The cost of not confirming is stated rather than hidden:
    the guard is only as true as the declaration, `source` says `stated`, and
    the report says so in its own row.
    """
    return Window(
        tokens=tokens,
        source="stated",
        model=model,
        detail=(f"declared by {declared_by}; no probe was sent, so this figure "
                f"is the operator's statement about the endpoint and not a "
                f"measurement of it"),
    )


PREFLIGHT = "preflight"
STATED = "stated: "


def mechanism(window: Window) -> str:
    """How this window guarded a call, as `Usage.window_mechanism` records it.

    Derived from the window's own `source` and written in one place, because
    the alternative is what it replaced: the caller composing the string it
    believed described the figure it was holding. Those are two facts that can
    disagree, and the way they disagree is the failure this whole mechanism
    exists to prevent -- a declared window recorded as a measured one, after
    which every downstream reader, the Provenance row included, reports a
    guarantee nobody gave.

    `preflight` for a measured window is the string every run in the recorded
    corpus already carries, unchanged and deliberately: those runs measured,
    and this function says so in the words their reports were written with.
    """
    if window.source == "stated":
        return f"{STATED}{window.tokens} tokens, {window.detail}"
    return PREFLIGHT


# Which provenances a run may *pass* on, as opposed to merely be refused by.
# `measured` is in because a probe confirmed it. `stated` is in for a different
# reason and the difference is not cosmetic: nothing confirmed it, and what
# puts it here is that a declaration is the only thing that can be right about
# an endpoint the tool cannot interrogate. What the tool owes in exchange is
# that the declaration is never dressed up as a measurement -- `Window.source`,
# `Usage.window_mechanism` and the Provenance block all say `stated`, and
# `Provenance.notes` says what it therefore does not guarantee.
PASSING_IS_SOUND = frozenset({"measured", "stated"})


def passing_is_sound(window: Window) -> bool:
    """May a run proceed on the strength of this figure?

    Not on a reported one. A reported figure is an upper bound, so `needed <=
    window` establishes nothing when it holds and everything when it fails. The
    question is a function rather than a comparison written out at each call
    site, because there is exactly one right answer and it should not have to be
    remembered twice.
    """
    return window.source in PASSING_IS_SOUND


def _probe_prompt(chars: int) -> str:
    """Filler of about `chars` characters, one unique record per line.

    Unique rather than repeated: repetition can tokenize far shorter than it
    looks, and a probe built from it would pass on a window it never filled.
    Records rather than prose because the ratio only has to be *stable* between
    the calibration call and the probe, and generated lines are the same shape
    at every size while a paragraph of prose is not.

    **At most, not roughly**, and the preamble is charged against the same
    budget. A version that stopped after passing the target overshot by up to a
    line, which is nothing at 40,000 tokens and half the prompt at 60 -- and the
    small end is where the offline tests live. One line is always emitted, so a
    prompt is never empty and `MIN_PROBE_TOKENS` is the size of that case.
    """
    lines: list[str] = []
    used, i = len(PROBE_PREAMBLE) + len("\n\n"), 0
    while True:
        line = (f"Record {i:06d}: node {(i * 7919) % 10**6:06d} reported latency "
                f"{(i * 31) % 1000:03d}ms on link {(i * 104729) % 10**4:04d}.")
        cost = len(line) + (1 if lines else 0)
        if lines and used + cost > chars:
            break
        lines.append(line)
        used += cost
        i += 1
    return PROBE_PREAMBLE + "\n\n" + "\n".join(lines)


# The smallest window this can ask about: the preamble and one record. Derived
# from the strings above rather than written down beside them, because a
# constant here would be a second copy of their lengths and would go quietly
# wrong the first time one was edited.
MIN_PROBE_TOKENS = -(-len(_probe_prompt(1)) // CHARS_PER_TOKEN)


def _counted(settings, model: str, prompt: str, *, role: str | None = None) -> int:
    """How many prompt tokens the endpoint says it received.

    `max_tokens=1` because nothing here reads the answer. The measurement is the
    server's own count of what it was given, which is the one number in the
    exchange that no model judgement enters.
    """
    from . import transport

    response = transport.post_json(
        f"{settings.base_url_for(role).rstrip('/')}/chat/completions",
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "seed": 0,
            "max_tokens": 1,
            # Off: a reasoning trace would put minutes of latency in front of
            # the proxy's time-to-first-byte wall for an answer nobody reads.
            "reasoning_effort": "none",
        },
        api_key=settings.api_key(role),
        timeout=settings.call_timeout,
        ca_bundle=settings.ca_bundle,
        host=settings.endpoint_name,
        model=model,
        stream=settings.stream,
    )
    try:
        usage = json.loads(response.body).get("usage") or {}
        tokens = usage.get("prompt_tokens")
    except ValueError as exc:
        raise WindowUnknown(
            f"{settings.endpoint_name} answered a window probe with something that is "
            f"not JSON"
        ) from exc
    if not isinstance(tokens, int) or tokens <= 0:
        raise WindowUnknown(
            f"{settings.endpoint_name} answered a window probe without a usable "
            f"prompt_tokens (got {tokens!r}), so there is nothing to measure "
            f"against"
        )
    return tokens


def measured(settings, model: str, *, at_most: int, floor: int = 4096,
             role: str | None = None) -> Window:
    """The largest window this endpoint will take a whole prompt at.

    Two calls in the ordinary case. The first is small and establishes how many
    characters of this filler make a token *on this endpoint's tokenizer*, which
    cannot be assumed: the project's prose figure is 3 and the filler measures
    close to 2, and sizing a probe from the wrong one is what made the previous
    version of this function report every window as half of itself. The second
    fills `PROBE_FILL` of `at_most` and reads `prompt_tokens` back. If the count
    agrees with what was sent, nothing was trimmed and `at_most` -- a bound the
    server itself declared -- is what it serves. If it does not, the candidate
    halves and it tries again.

    The returned figure is `at_most` rather than the tokens actually sent,
    because the probe's job is to confirm a declared number rather than to
    discover an undeclared one, and reporting 97% of a window as the window
    would refuse requests that fit. What was proven is in `detail`.

    Costs one large generation per step and is therefore called once per model
    per run, not once per unit of work. It is worth that: the alternative is a
    run whose prompts were silently trimmed, which produces a corpus that looks
    clean and measures the wrong documents.

    `floor` bounds the halving, and it bounds the search rather than the answer:
    an endpoint that reports less than `floor` to begin with gets one probe at
    exactly what it reported, which confirms that figure instead of refusing to
    look at the only candidate there was.

    Raises `WindowUnknown` rather than returning a number when every probe comes
    back trimmed, or when `at_most` is below what a probe prompt can express,
    because at that point the endpoint is not doing what its API says and a
    figure invented here would be the hard-coding this module exists to remove.
    """
    if at_most < MIN_PROBE_TOKENS:
        raise WindowUnknown(
            f"{settings.endpoint_name} offers {model} {at_most} tokens, and the smallest "
            f"prompt that can be sent is {MIN_PROBE_TOKENS}. There is nothing "
            f"here to measure."
        )

    # Calibrated well under `at_most` so that the calibration call cannot itself
    # be the thing that gets trimmed -- a trimmed calibration would inflate the
    # ratio, shrink every probe built from it, and make a truncating endpoint
    # look healthy.
    sample = _probe_prompt(max(len(PROBE_PREAMBLE), at_most * CHARS_PER_TOKEN // 2))
    ratio = len(sample) / _counted(settings, model, sample, role=role)

    size = at_most
    floor = min(floor, at_most)
    sent = counted = 0
    while size >= floor:
        prompt = _probe_prompt(int(size * PROBE_FILL * ratio))
        sent = len(prompt) / ratio
        counted = _counted(settings, model, prompt, role=role)
        if counted >= sent * INTACT:
            return Window(
                tokens=size,
                source="measured",
                model=model,
                detail=(f"a prompt of {counted} tokens was sent and the endpoint "
                        f"counted all of it, so nothing was trimmed at "
                        f"{PROBE_FILL:.0%} of {size}"),
            )
        size //= 2

    raise WindowUnknown(
        f"{settings.endpoint_name} trimmed a probe sent to {model}: {int(sent)} tokens "
        f"went out and it counted {counted}. It is serving less than {floor} "
        f"tokens per request and nothing here will guess how much less."
    )


class Truncated(RuntimeError):
    """A response's own usage counts show it hit its ceiling.

    The post-hoc counterpart to `guard()`, for the one case `guard()` cannot
    cover: an endpoint whose served window cannot be measured (see
    `WindowUnmeasurable`) has nothing for a preflight check to compare against.
    This instead reads what the endpoint already reported about the response
    that came back. `completion_tokens` at or past the `max_tokens` a call
    asked for is the one signature a truncated completion always leaves in the
    numbers a run already carries on its ledger -- the same signature
    `BudgetExceedsWindow`'s docstring describes arriving too late to matter.
    Here it arrives in time to say the answer is not to be trusted, even
    though it could not arrive before the call was paid for.
    """


def assert_untruncated(row: dict, *, what: str) -> None:
    """Raise `Truncated` if `row` shows a completion that hit its ceiling.

    `row` is one line of `Usage.ledger` -- exactly the counts the run already
    reports, rather than a second measurement taken to
    check the first. Silent when either figure is missing: a response the
    vendor reported no usage for, or a call made with no `max_tokens` ceiling,
    has nothing here to check, and manufacturing a verdict from numbers that
    were never sent would be exactly the kind of default this project's window
    handling exists to refuse.
    """
    max_tokens = row.get("max_tokens")
    completion = row.get("completion_tokens")
    if max_tokens is None or completion is None:
        return
    if completion >= max_tokens:
        raise Truncated(
            f"{what}: the response used {completion} completion tokens against "
            f"a {max_tokens}-token ceiling. That is what a truncated completion "
            f"looks like from its own usage counts -- the served window could "
            f"not be measured before this call, so nothing caught it sooner. "
            f"Lower the fidelity level, split the documents, or set "
            f"LLOSSLESS_MAX_TOKENS higher if the ceiling was the tool's own "
            f"budget rather than the endpoint's."
        )


# Below this fraction of the prompt a run believes it sent, the endpoint's own
# count is read as a trim rather than as an estimate that ran long.
#
# Derived twice, from opposite directions, and the value sits near the middle
# of the gap between them:
#
#   the legitimate floor   Over 2,200 recorded calls carrying a prompt count,
#                          `prompt_tokens` against this project's own
#                          `chars // CHARS_PER_TOKEN` estimate runs a minimum
#                          of 0.653 and a median of 0.727 -- the estimate
#                          deliberately over-counts, so every honest call
#                          reports *fewer* tokens than were estimated. The
#                          floor holds per role (0.653 verify, 0.673 decompose,
#                          0.676 merge) and per model (0.653 to 0.828).
#   the trim ceiling       A server that trims keeps the back half of the
#                          window (lines 18-26, measured 2026-08-17), so it
#                          reports about `window / 2`; and a prompt only gets
#                          trimmed if it was longer than the window. Those two
#                          together cap a trimmed call at 0.727 / 2 = 0.364 of
#                          the estimate.
#
# 0.364 and 0.653 with 0.5 between them: 0.136 of margin against a trim being
# missed, 0.153 against an honest call being refused.
TRIM_RATIO = 0.5


def assert_prompt_not_trimmed(row: dict, *, what: str) -> None:
    """Raise `Truncated` if the endpoint counted far fewer prompt tokens than were sent.

    The other half of `assert_untruncated`, and a different failure: that one
    reads a *completion* that hit its ceiling, this reads a *prompt* the server
    silently shortened. `guard()` cannot cover it, because `/api/ps` reports
    the runner's total and the prompt shares that total with the completion --
    so a prompt inside the reported window can still be over the budget the
    generation actually leaves for it, and ollama answers 200 with no error and
    no `finish_reason` saying so.

    **This is not a trimming signature inferred from the answer.** That was
    rejected, and rightly: reading trimming out of the *shape* of the
    output is a guess about content. This compares two numbers the run already
    has -- a count the endpoint states about itself, in a field it already
    sends, against the estimate the preflight already computed -- and asks
    nothing extra of anybody.

    **Silent when either figure is missing, and zero counts as missing.** Every
    one of the 70 vendor bodies in this project's corpus reports
    `prompt_tokens: 0` and carries its billing in `credits_used` instead. Read
    as a count, zero is a total shortfall and would refuse every vendor call;
    it means "this endpoint does not report the figure". Absent and zero take
    the same path, and neither is ever read as agreement -- UNMEASURED is a
    first-class outcome here and this is one.

    **What this will not catch.** A server that trims to *exactly* the window,
    rather than to half of it, returns nearly everything that was sent when the
    overrun is small: the ratio lands just under the legitimate floor, and no
    threshold on this comparison separates that from a tokenizer running
    efficiently. It is a partial guard and `preflight()` stays the primary one.
    What it adds is the case `preflight()` structurally cannot reach -- an
    endpoint with no `/api/ps` to preflight against, and the top of the band
    `measured()` confirms only to `PROBE_FILL` of itself.
    """
    estimated = row.get("estimated_prompt_tokens")
    reported = row.get("prompt_tokens")
    if not estimated or not reported:
        return
    # At or under, not under: the boundary is unreachable by an honest call --
    # the floor is 0.653 -- so refusing it costs nothing, and a threshold that
    # is a knife-edge at its own value is one nobody can reason about.
    if reported <= estimated * TRIM_RATIO:
        raise Truncated(
            f"{what}: {estimated} prompt tokens were sent and the endpoint "
            f"counted {reported} of them, which is at or under "
            f"{TRIM_RATIO:.0%} of "
            f"what went out. That is what a trimmed prompt looks like from the "
            f"endpoint's own numbers: the server took the request, shortened "
            f"it from the front to fit, and answered about a document it was "
            f"not fully shown. The reported context window is the runner's "
            f"total and the completion comes out of it, so a prompt inside "
            f"that window can still be over the budget left for it. Split the "
            f"documents, or raise the served context and restart the server."
        )


def preflight(served, *, needed: int, what: str, role: str) -> None:
    """Guard a call before it is sent, and refuse when the window is unknowable.

    `merge` has preflighted for a while now; `decompose` and `verify` had no guard
    of any kind. That is the shape of the defect rather than an oversight in it:
    ollama does not refuse a prompt that overruns the window, it trims the front
    and answers confidently about a document whose beginning the model was never
    shown. So the claims came from the tail of the source, the verdicts were
    graded against a merge nobody had fully read, and every report said nothing
    was dropped -- because nothing downstream could see that anything had been.

    **An unmeasurable window refuses rather than proceeding.** A guard that
    silently no-ops when it cannot measure is the same defect one level up: the
    run looks guarded and is not. UNMEASURED is a first-class outcome in this
    project and this is one, so it is said and the call is not made.

    Note the asymmetry with `merge`, which proceeds unguarded on an endpoint
    that cannot answer `/api/ps` and says so. `merge` has a
    post-hoc check standing in its place -- `assert_untruncated` over the
    ledger row -- and these two roles have nothing. Refusing is the only
    honest option where there is no second mechanism.

    **A stated window satisfies this.** It arrives here as an ordinary
    `Window`, is compared like any other, and refuses a prompt that does not
    fit it. What it does not do is quietly become a default: `served` is
    `None` unless the operator said otherwise, and this refusal is what they
    meet if they did not.
    """
    if served is None:
        raise WindowUnmeasurable(
            f"UNMEASURED: the served context window for {role} could not be "
            f"established, so {what} cannot be checked against it. Refusing "
            f"rather than sending {needed} estimated tokens unguarded: an "
            f"overrun is trimmed from the front by the server and the answer "
            f"carries no sign of it. Point LLOSSLESS_BASE_URL at an endpoint "
            f"that exposes /api/ps, state the window this one serves with "
            f"--window / LLOSSLESS_WINDOW, or split the documents."
        )
    guard(needed=needed, window=served, what=what)


def guard(
    *,
    needed: int,
    window: Window,
    what: str,
    headroom: int = 0,
) -> None:
    """Refuse before sending when `needed` does not fit `window`.

    `needed` is the whole request: the rendered prompt plus the output ceiling.
    Both halves are charged because both come out of the same window, and a
    guard that checked only the output would pass a request whose prompt alone
    overran the context.
    """
    if needed + headroom <= window.tokens:
        return
    over = needed + headroom - window.tokens
    raise BudgetExceedsWindow(
        f"{what} needs {needed} tokens"
        + (f" plus {headroom} headroom" if headroom else "")
        + f" and {window} leaves room for {window.tokens}. Over by {over}. "
        f"Nothing has been sent. Either lower the fidelity level, split the "
        f"documents, or serve a larger window -- on ollama that is "
        f"OLLAMA_CONTEXT_LENGTH, which is read once when the server starts, so "
        f"raising it means restarting the server; note that {window.source} means "
        f"{window.detail or 'a measured per-request figure'}."
    )
