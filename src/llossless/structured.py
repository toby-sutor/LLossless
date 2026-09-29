"""Three ways to ask an OpenAI-compatible endpoint for JSON, tried in order.

Schema-constrained decoding is the best of the three and is not available
everywhere. Ollama has it, most hosted providers have it, some corporate
gateways strip it, and older or self-hosted stacks return a 400 for the field
they do not know. The tool has to work on all of them, so it implements all
three and finds out at runtime which one the endpoint honours:

  json_schema  response_format with a strict schema. The endpoint constrains
               decoding, so the output is valid by construction.
  tool_call    one function whose parameters *are* the schema, made mandatory
               with tool_choice. Same constraint through an older door.
  prompt       no API-level constraint at all. The schema goes into the message
               and PART C does the rest.

Falling back is never silent. The resolved tier is recorded in the report
header, because "how strongly was the output constrained" is part of what a
quality number means, and a number produced on tier 3 is not the same
measurement as one produced on tier 1.
"""

from __future__ import annotations

import ipaddress
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

TIERS = ("json_schema", "tool_call", "prompt")

# Statuses that can never mean "this tier is unavailable". A 401 or 403 is a
# credential problem and a 404 is a wrong URL or a wrong route; all three are
# equally true on every rung of the ladder, so treating them as a tier refusal
# walks the whole ladder and then reports a configuration error as a model
# capability. A base URL missing its `/v1` suffix once surfaced as "accepted
# none of the structured-output modes" for exactly this reason — three 404s,
# one misleading message, and nothing naming the actual fault.
NEVER_FALLBACK_STATUS = frozenset({401, 403, 404})
FALLBACK_MARKERS = (
    "response_format",
    "json_schema",
    "json schema",
    "tool_choice",
    "tools",
    "unsupported",
    "not supported",
    "unrecognized",
    "unknown field",
    "unknown parameter",
)


# --------------------------------------------------------------------------
# Request-shape profiles
# --------------------------------------------------------------------------
#
# "OpenAI-compatible" is a name for a wire *format*, and the four hosted SKUs
# this project has paid to talk to all speak it. What differs between them is
# the request envelope, and the envelope is where a run keeps its held-constant
# conditions. Every row below is a measured 400 from a real call on
# 2026-08-31, recorded in `internal/docs/vendor-endpoint-support.md`, not a
# reading of anybody's documentation:
#
#   `max_tokens`              > Unsupported parameter: 'max_tokens' is not
#                               supported with this model. Use
#                               'max_completion_tokens' instead.
#                             — both OpenAI 5.6 SKUs. Anthropic's compat
#                               endpoint takes `max_tokens` on the same body,
#                               so the field name is per-vendor and a fix
#                               cannot be unconditional.
#   `temperature: 0.0`        > Unsupported value: 'temperature' does not
#                               support 0.0 with this model. Only the default
#                               (1) value is supported.
#                             — OpenAI 5.6, and *only* in the thinking-on
#                               shape: the identical body passes when
#                               `reasoning_effort: "none"` is present. And
#                             > `temperature` is deprecated for this model.
#                             — Anthropic sonnet-5, all three shapes.
#   `seed`                    not in Anthropic's surface at all.
#   `tools` + `reasoning_effort`
#                             > Function tools with reasoning_effort are not
#                               supported for gpt-5.6-luna in
#                               /v1/chat/completions.
#                             — both OpenAI 5.6 SKUs, so the ladder's middle
#                               rung cannot be reached there with thinking off.
#
# **A profile is chosen, never inferred.** `config.model_for` returns the model
# string verbatim and nothing in `src/` parses a model name; this table does not
# start. One vendor serves models with different envelopes — haiku takes the
# default body unmodified on the same endpoint that refuses it for sonnet-5 —
# so a name-to-profile guess would be wrong on a real pair that exists today,
# and it would be wrong silently, by sending a body nobody chose.

# When `temperature` may be sent. Three values and not a boolean, because the
# measured constraint is not a boolean: on the OpenAI 5.6 SKUs the legal range
# of `temperature` is a function of the reasoning state, which is a coupling
# no single flag can express.
TEMPERATURE_ALWAYS = "always"
TEMPERATURE_NEVER = "never"
TEMPERATURE_THINKING_OFF = "thinking-off"
TEMPERATURE_RULES = (TEMPERATURE_ALWAYS, TEMPERATURE_NEVER, TEMPERATURE_THINKING_OFF)

# How a profile expresses "do not reason". `REASONING_EFFORT` is the only field
# this project has ever found honoured on the OpenAI-compatible path;
# `THINKING_OFF_UNAVAILABLE` is the honest other answer, and it refuses rather
# than sending a thinking-on body under a `thinking=False` label.
REASONING_EFFORT = "reasoning_effort"
THINKING_OFF_UNAVAILABLE = "unavailable"
THINKING_OFF_RULES = (REASONING_EFFORT, THINKING_OFF_UNAVAILABLE)

# Where the merge and decompose ceilings come from. `CEILING_DOCUMENT` is the historical
# behaviour: `merge.budget_tokens` sizes it from the sources and adds a flat
# `REASONING_ALLOWANCE`. `CEILING_MODEL` sends no ceiling at all and lets the
# endpoint apply its own, which is DECISIONS 443 - a fixed allowance cannot
# hold for a model that scales reasoning with perceived difficulty, and
# `claude-sonnet-5` proved it by spending 13,824 tokens on reasoning and being
# truncated with `content: null` before writing a character.
#
# `openai-compatible` deliberately keeps `CEILING_DOCUMENT`, and NOT because of
# cassettes: local ollama allocates the `num_ctx` KV cache up front
# (see `merge.py`, the KV-cache note beside `CHARS_PER_TOKEN`), so an unbounded ceiling there makes the operator's own
# card reserve memory the run cannot use.
CEILING_DOCUMENT = "document"
CEILING_MODEL = "model"
CEILING_RULES = (CEILING_DOCUMENT, CEILING_MODEL)


@dataclass(frozen=True)
class Profile:
    """One endpoint family's request envelope. Four fields and one coupling.

    Deliberately small and deliberately flat: it is a table of what a named
    family accepts, not a strategy object. Anything that reads the *content* of
    a request belongs elsewhere — this decides field names and presence only,
    and every row of it can be checked against a quoted vendor refusal.
    """

    # Where the output ceiling goes. `merge` is the only role that sets one.
    budget_field: str
    # One of `TEMPERATURE_RULES`.
    temperature: str
    # Whether `seed` may be sent at all. False is not "send seed=None": the key
    # is absent from the body, because a vendor that does not know the field
    # refuses the request rather than ignoring it.
    seed: bool
    # One of `THINKING_OFF_RULES`.
    thinking_off: str
    # Whether the thinking-off field may ride with `tools`. False makes the
    # `tool_call` rung unavailable on a thinking-off call, which is what the
    # measured 400 means; `build_body` raises `TierUnsupported` for it so the
    # ladder steps past the rung instead of paying for the refusal.
    thinking_off_with_tools: bool = True
    # One of `CEILING_RULES`. `CEILING_MODEL` means this project imposes no
    # output ceiling and the endpoint's own default applies.
    output_ceiling: str = CEILING_DOCUMENT
    # Which rungs this profile can produce a body for. Empty means all of
    # them, which is every profile that talks to an HTTP endpoint: the ladder
    # probes, and what an endpoint refuses is discovered rather than declared.
    # A command backend is the case where it cannot be discovered -- there is
    # no `response_format` to be refused and no `tools` to be ignored, only a
    # prompt and whatever comes back -- so its profile names its one rung and
    # `build_body` raises `TierUnsupported` for the others (483).
    tiers: tuple[str, ...] = ()

    def sends_temperature(self, *, thinking: bool) -> bool:
        if self.temperature == TEMPERATURE_ALWAYS:
            return True
        if self.temperature == TEMPERATURE_NEVER:
            return False
        return not thinking


PROFILES: dict[str, Profile] = {
    # The default, and it is the body this project has sent since it was
    # written: `max_tokens`, `temperature` always, `seed` always,
    # `reasoning_effort: "none"` for thinking off on every rung. ollama, the
    # recorded corpus, and Anthropic's compat endpoint on haiku all take it.
    "openai-compatible": Profile(
        budget_field="max_tokens",
        temperature=TEMPERATURE_ALWAYS,
        seed=True,
        thinking_off=REASONING_EFFORT,
    ),
    # The OpenAI 5.6 reasoning SKUs (`gpt-5.6-luna`, `gpt-5.6-terra` as
    # measured). `temperature` is sent only with reasoning off, which is the
    # only state in which 0.0 is legal; with reasoning on the field is omitted
    # and the endpoint's own default (1) applies, because there is no value
    # this project would rather send than the one it is allowed.
    "openai-reasoning": Profile(
        budget_field="max_completion_tokens",
        temperature=TEMPERATURE_THINKING_OFF,
        seed=True,
        thinking_off=REASONING_EFFORT,
        thinking_off_with_tools=False,
        output_ceiling=CEILING_MODEL,
    ),
    # Anthropic's OpenAI-compatible endpoint, at the shape sonnet-5 requires:
    # no `temperature`, no `seed`. Haiku accepts the default profile on the
    # same endpoint, so this is the conservative shape for the vendor rather
    # than the necessary one for every model on it — and what it costs is
    # worth saying out loud: without `seed` the endpoint is free to sample
    # differently on identical bytes, so a run under this profile is not
    # reproducible by construction and its cassettes record one draw.
    #
    # No `tiers`, so the ladder probes from `json_schema`. The vendor documents
    # `response_format` as ignored on this endpoint; a must-fire schema showed
    # it carried on four Anthropic models on 2026-09-25 (621). The ladder
    # cannot tell the two apart, so `tests/schema_carriage.py` is the check.
    "anthropic": Profile(
        budget_field="max_tokens",
        temperature=TEMPERATURE_NEVER,
        seed=False,
        thinking_off=REASONING_EFFORT,
        output_ceiling=CEILING_MODEL,
    ),
    # Google's OpenAI-compatible endpoint
    # (`generativelanguage.googleapis.com/v1beta/openai/`), as measured on
    # `gemini-3.8-flash` and `gemini-3.5-flash-lite` on 2026-09-25 (624):
    #
    #   `seed`                    > Invalid JSON payload received. Unknown name
    #                               "seed": Cannot find field.
    #                             -- HTTP 400 on both models, so the default
    #                               profile is refused outright here.
    #   `max_completion_tokens`   accepted (200).
    #   `temperature: 0.0`        accepted (200), and not sent: Google's
    #                               Gemini 3 guidance is to leave it at its
    #                               default, and with thinking on no other
    #                               vendor profile here sends one either.
    #   `reasoning_effort`        "minimal" refused on 3.8 Flash ("Thinking
    #                               level MINIMAL is not supported for this
    #                               model"); the compatibility page says
    #                               "Reasoning cannot be turned off for Gemini
    #                               2.5 Pro or 3 models", so a thinking-off call
    #                               is refused here rather than sent.
    #
    # No `tiers`, so the ladder probes; the free-tier run pinned `prompt`, as
    # the other vendor rows of 2026-09-25 did.
    "google": Profile(
        budget_field="max_completion_tokens",
        temperature=TEMPERATURE_NEVER,
        seed=False,
        thinking_off=THINKING_OFF_UNAVAILABLE,
        output_ceiling=CEILING_MODEL,
    ),
    # A subprocess answering instead of an endpoint (483). Everything here is
    # a consequence of there being no HTTP request to put a field in.
    #
    # `prompt` and nothing else: the other two rungs constrain a model through
    # request fields -- `response_format`, `tools` -- and a command backend
    # has no request to put them in. Naming the rung rather than letting the
    # ladder probe for it also keeps the failure honest: a run pinned to
    # `json_schema` here raises instead of silently answering at a weaker rung
    # than it was told to use.
    #
    # No `temperature` and no `seed`, because there is nowhere to send them.
    # The cost is the same one the `anthropic` profile states and it is worth
    # repeating: a run under this profile is **not reproducible by
    # construction**, so its cassettes record one draw. It is worth saying
    # twice as loudly here, because every published figure in this project was
    # measured at `json_schema` and these runs are comparable to none of them.
    "subscription": Profile(
        budget_field="max_tokens",
        temperature=TEMPERATURE_NEVER,
        seed=False,
        thinking_off=THINKING_OFF_UNAVAILABLE,
        output_ceiling=CEILING_MODEL,
        tiers=("prompt",),
    ),
}

# The profile whose body is byte-identical to what this project sent before
# profiles existed. It is the default everywhere — `build_body`, `Settings`,
# `cassette.key_for` — and `key_for` leaves it out of the hash entirely, so no
# recording made before this table existed is re-keyed by it.
DEFAULT_PROFILE = "openai-compatible"


def profile_for(name: str) -> Profile:
    """The named profile, or a refusal naming the ones that exist."""
    try:
        return PROFILES[name]
    except KeyError:
        raise ValueError(
            f"unknown request profile {name!r}; the profiles are "
            f"{', '.join(sorted(PROFILES))}"
        ) from None


class TierUnsupported(RuntimeError):
    """This tier does not work against this endpoint. Try the next one down."""


class EmptyResponse(TierUnsupported):
    """The endpoint answered 200 and said nothing. Ask it again, same tier.

    This is deliberately not the same event as the rung above it, even though
    both arrive from `read_content`. "No tool_call in a response to a request
    carrying `tools`" is a statement about what the endpoint can do. An empty
    `content` is a statement about one request: the same endpoint had answered
    the same shape of request 67 times in the process that hit this on
    2026-08-08 (`tests/responses/m4/sweep.log`, the first attempt-4 marker),
    and the 68th came back blank.

    It subclasses `TierUnsupported` so that every existing handler still
    catches it rather than letting a blank body escape somewhere new; the two
    places where the difference decides anything -- `should_fall_back` below
    and the ladder in `client._live` -- name it explicitly.
    """


class ThinkingIgnored(RuntimeError):
    """The endpoint took the field that turns thinking off, and reasoned anyway.

    `ThinkingNotHonoured`'s sibling, and the quieter half of the same problem.
    There the endpoint says no and the run knows immediately; here it says 200,
    sends the reasoning it was asked not to, and nothing about the exchange
    looks wrong. Measured 2026-08-28 against deepseek-r1:70b on a hosted
    endpoint: `reasoning_effort: "none"` accepted, and the reasoning block came
    back *longer* than the same request without the field, 2555 characters to
    3026.

    The damage is the same damage: a cassette key that says `thinking=False`
    over an answer the model reasoned its way to, and a two-arm comparison of
    thinking against no-thinking that has quietly merged its arms.

    So the severity is not the same everywhere, and this is the one place in
    this module that draws a distinction on what the run is for rather than on
    what the endpoint did. A recording run writes a permanent artefact whose
    label would be false, and it aborts. Every other run produces a report, and
    a report can say what happened: it carries on, tells the operator once, and
    the provenance block prints requested and observed side by side. Refusing
    to run a model because it thinks would make thinking models unusable, and
    thinking models are the ones this tool most needs to work with.

    Fires only on reasoning that is actually there -- `client.reasoned` strips
    before it decides, so an endpoint that includes `"reasoning": ""` when
    thinking is off is not accused of anything.
    """


class ThinkingNotHonoured(RuntimeError):
    """The endpoint refused the only field that turns thinking off.

    Not a tier problem and not recoverable by retrying, which is why it is a
    plain `RuntimeError` and not a `TierUnsupported`: every tier would send the
    same field and every tier would be refused the same way.

    This used to be a latch. The client cleared a flag, retried without the
    field, and every later call on that client omitted it -- so the model
    reasoned while `thinking=False` went on being written into the cassette key.
    The corpus recorded one condition under the other condition's name, and on a
    two-arm comparison of thinking against no-thinking that silently merges the
    arms. It also costs about 7x wall clock, which is the only symptom anyone
    would have noticed, and it would have been read as a slow endpoint.

    `reasoning_effort` is only ever sent when a caller asked for thinking off
    (see `build_body`), so this exception cannot fire on a run that wanted
    thinking on. Every time it fires, continuing would mean lying.
    """


def build_body(
    *,
    tier: str,
    model: str,
    messages: list[dict],
    schema: dict,
    schema_name: str,
    temperature: float = 0.0,
    seed: int | None = 0,
    max_tokens: int | None = None,
    thinking: bool = False,
    reasoning_effort: bool = True,
    profile: str = DEFAULT_PROFILE,
) -> dict:
    """The request body for one tier, in one named profile's envelope.

    Still one request path. `profile` selects field *names and presence* from
    the table above and nothing else: there is no branch here on a vendor, a
    host or a model id, and the default profile emits the body this function
    emitted before the parameter existed, key for key and in the same order.

    Raises `TierUnsupported` when the profile says this rung cannot carry the
    thinking-off field — the ladder steps down instead of paying for a 400 —
    and `ThinkingNotHonoured` when the profile has no way to ask for thinking
    off at all, which is a refusal rather than a silent thinking-on call.
    """
    if tier not in TIERS:
        raise ValueError(f"unknown structured mode {tier!r}")
    shape = profile_for(profile)
    # Before anything is assembled, and outside every `thinking` branch: which
    # rungs a profile can answer at is a property of the profile alone. The
    # first version of this sat inside `if not thinking and reasoning_effort`
    # and never fired on a call that asked for neither.
    if shape.tiers and tier not in shape.tiers:
        raise TierUnsupported(
            f"the {profile!r} request profile answers only at "
            f"{', '.join(shape.tiers)}; {tier!r} constrains a model through "
            f"request fields, and there is no request here to put them in"
        )

    body: dict = {"model": model, "messages": messages}
    if shape.sends_temperature(thinking=thinking):
        body["temperature"] = temperature
    if seed is not None and shape.seed:
        body["seed"] = seed
    if max_tokens is not None:
        body[shape.budget_field] = max_tokens
    if not thinking and reasoning_effort:
        # Measured against ollama 0.32: of `think: false`,
        # `chat_template_kwargs.enable_thinking` and this, only this one is
        # honoured on the OpenAI-compatible path — and it takes a qwen3:8b
        # decompose call from 13.5s to 2.0s. `reasoning_effort` is a field some
        # endpoints will not recognise, so the client drops it and retries
        # rather than mistaking the rejection for an unsupported tier.
        if shape.thinking_off == THINKING_OFF_UNAVAILABLE:
            raise ThinkingNotHonoured(
                f"the {profile!r} request profile has no field that turns "
                f"thinking off, and this call asked for thinking off. Sending "
                f"the request anyway would record a thinking-on answer under a "
                f"`thinking=False` cassette key. Run the role with thinking on "
                f"and say so, or use a profile whose endpoint accepts "
                f"`reasoning_effort`."
            )
        if tier == "tool_call" and not shape.thinking_off_with_tools:
            raise TierUnsupported(
                f"the {profile!r} request profile refuses `tools` and "
                f"`reasoning_effort` in one request, so the tool_call rung "
                f"cannot carry a thinking-off call. Measured as HTTP 400 on "
                f"both OpenAI 5.6 SKUs, 2026-08-31."
            )
        body["reasoning_effort"] = "none"

    if tier == "json_schema":
        body["response_format"] = {
            "type": "json_schema",
            "json_schema": {"name": schema_name, "strict": True, "schema": schema},
        }
    elif tier == "tool_call":
        function = {
            "name": schema_name,
            "description": "Return the result. Call this exactly once.",
            "parameters": schema,
        }
        body["tools"] = [{"type": "function", "function": function}]
        body["tool_choice"] = {"type": "function", "function": {"name": schema_name}}
    else:
        # Tier 3 puts the schema where the only thing reading it is the model.
        # The prompt file already ends with "Return JSON matching the provided
        # schema"; without this, "the provided schema" refers to nothing.
        messages = list(messages)
        messages[-1] = dict(messages[-1])
        messages[-1]["content"] = (
            messages[-1]["content"]
            + "\n\nSCHEMA:\n"
            + json.dumps(schema, indent=2)
            + "\n\nReturn one JSON object matching this schema. No prose, no markdown."
        )
        body["messages"] = messages

    return body


def read_content(tier: str, response: dict) -> str:
    """Pull the text PART C should parse out of a chat-completions response."""
    try:
        message = response["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise TierUnsupported(f"response has no choices[0].message: {exc}") from exc

    if tier == "tool_call":
        calls = message.get("tool_calls") or []
        if not calls:
            # The endpoint accepted `tools` and then ignored them. Constraining
            # by tool call is not actually available here.
            raise TierUnsupported("endpoint accepted tools but returned no tool_call")
        arguments = calls[0].get("function", {}).get("arguments")
        if not isinstance(arguments, str):
            # A few gateways hand back an already-decoded object.
            return json.dumps(arguments)
        return arguments

    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise EmptyResponse(_empty_reason(response, message))
    return content


def _empty_reason(response: dict, message: dict) -> str:
    """Why the content was empty, when the response says so itself.

    An ordinary empty body and a completion budget spent entirely in the
    reasoning channel are the same string to a reader and different problems
    to fix. The second says so in fields this function already holds:
    `finish_reason: "length"` with a reasoning block and no content means the
    model was still thinking when it hit the cap (385). Naming the cap and the
    size of the reasoning is what turns "the generation is blank" into an
    instruction -- the operator met the first while the response carried both.

    Message only. `EmptyResponse` is a `TierUnsupported` and stays on the
    exit-2 operational path, so `FINDING_KINDS` stays 12 and `CHECKS` stays 9.
    """
    generic = "response message has empty content"
    try:
        choice = (response.get("choices") or [{}])[0]
        usage = response.get("usage") or {}
        finish = choice.get("finish_reason")
        completion = usage.get("completion_tokens")
    except (AttributeError, IndexError, TypeError):  # pragma: no cover
        return generic
    reasoning = message.get("reasoning") or message.get("reasoning_content") or ""
    # The reasoning text is NOT required, and requiring it made this blind on
    # the one envelope it was written for: Anthropic's compat endpoint returns
    # `{"content": null, "finish_reason": "length"}` with no reasoning block at
    # all, so a predicate that insisted on one fell through to the generic
    # message and sent the investigation at the endpoint instead of the
    # ceiling. `finish_reason: "length"` with empty content and tokens on the
    # clock is already sufficient: the budget was spent and no answer came out,
    # whether or not the vendor chose to show its working.
    if finish == "length":
        cap = f"{completion} completion token(s)" if completion else "its completion budget"
        shown = (f" ({len(reasoning)} characters of reasoning returned)"
                 if reasoning else " (the endpoint returned no reasoning text)")
        return (
            f"the model spent {cap} and emitted no content "
            f"(finish_reason 'length'){shown}. Thinking on this role is the likely "
            f"cause, and raising the ceiling is the fix rather than a retry: "
            f"reasoning is charged against the same budget as the answer, so the "
            f"same prompt at the same ceiling reasons into the same wall again"
        )
    # A refusal, named rather than folded into the generic blank (680): a
    # safety layer that declines is a different fault from a platform that
    # answered nothing, and a runner classifying failures for 678 has to be
    # able to tell them apart. Distinct from `length` above because retrying
    # is not obviously futile here the way it is there -- a rephrased prompt
    # can clear a content filter a resend of the identical one will not.
    if finish == "content_filter":
        return (
            "the endpoint refused to answer (finish_reason 'content_filter'): "
            "this is a safety layer declining, not a platform fault, and "
            "asking the identical prompt again asks the same question again"
        )
    # Any other named `finish_reason` still says more than the generic
    # sentence alone -- a runner reading only this string, not the response
    # object, can at least see which reason arrived even when this function
    # has no specific handling for it yet.
    if finish:
        return f"{generic} (finish_reason {finish!r})"
    return generic


def rejected_field(exc: Exception, field: str) -> bool:
    """Did the endpoint refuse specifically because of this one request field?

    Distinguishing this from an unsupported tier matters: dropping to a weaker
    tier because the endpoint disliked `reasoning_effort` would degrade output
    quality to fix a problem that had nothing to do with the schema.
    """
    status, body = getattr(exc, "status", None), getattr(exc, "body", None)
    return isinstance(status, int) and isinstance(body, str) and field in body.lower()


def should_fall_back(exc: Exception) -> bool:
    """Did this failure mean "wrong tier" rather than "wrong configuration"?

    Only a response that actually says something about structured output may
    demote a tier. A status code alone is not enough: endpoints return 400 and
    404 for a great many reasons, almost none of them "I do not support
    response_format", and every one of the others is just as true one rung down.
    So the body must name a structured-output field or say the request was not
    understood, and 401/403/404 never demote whatever the body says — a
    credential error is free to contain the word "unsupported".

    The cost of being wrong is asymmetric, which is why the rule is this strict.
    A false negative raises the endpoint's own error, naming the real fault. A
    false positive spends two more calls, discards them, and reports "accepted
    none of the structured-output modes" — an answer about the model, for a
    question that was never about the model.

    The HTTP error is matched structurally rather than by class, so that this
    module never imports transport. That keeps the socket-owning module out of
    a replay run's import graph, which is how "runs fully offline" is checked
    instead of asserted.
    """
    if isinstance(exc, EmptyResponse):
        # A blank body is not evidence about this tier, so it may never demote
        # one. The ladder retries it in place instead. Checked before the line
        # below because EmptyResponse is a TierUnsupported.
        return False
    if isinstance(exc, TierUnsupported):
        # Not a status at all: the endpoint answered 200 and the reply had no
        # tool call. That is this tier failing, first-hand.
        return True
    status, body = getattr(exc, "status", None), getattr(exc, "body", None)
    if not isinstance(status, int) or not isinstance(body, str):
        return False
    if status in NEVER_FALLBACK_STATUS:
        return False
    return any(marker in body.lower() for marker in FALLBACK_MARKERS)


def tiers_from(start: str) -> tuple[str, ...]:
    """The ladder below and including `start`."""
    return TIERS[TIERS.index(start) :]


def endpoint_identity(host: str, port: int, *, resolve=None) -> str:
    """Which server this is, rather than how the URL happened to spell it.

    The file recovered on 2026-08-08 held `localhost|qwen3:8b -> prompt` beside
    `127.0.0.1|qwen3:8b -> json_schema`: two contradictory verdicts about one
    ollama on one machine, and no code path that could ever notice, because the
    key was the hostname string. Both spellings resolve here, but not to the
    same set -- `localhost` gives `['127.0.0.1', '::1']` and the literal gives
    `['127.0.0.1']` -- so comparing resolved addresses is not enough on its own.
    Every loopback address is the same server, so they collapse to one token.

    Port is part of the identity: two ollamas on one box are two deployments.
    Scheme, path, query and credentials are not, and never enter the string --
    a path can name a deployment and a query can carry a token.

    Resolution is a local NSS lookup for the endpoint the tool is already
    configured to call, and it happens only on a live path, so a replay run
    never reaches it. If it fails, the spelling is used with a marker saying so
    rather than raising: this is a label on a record, not a routing decision.
    """
    import socket  # function-local, so importing this module pulls in no name resolver

    resolve = socket.getaddrinfo if resolve is None else resolve
    try:
        addresses = sorted({info[4][0] for info in resolve(host, port, proto=socket.IPPROTO_TCP)})
    except (OSError, ValueError, UnicodeError):
        return f"unresolved:{host.lower()}:{port}"

    def loopback(address: str) -> bool:
        try:
            return ipaddress.ip_address(address.partition("%")[0]).is_loopback
        except ValueError:  # a scoped or otherwise unparseable literal
            return False

    if addresses and all(loopback(address) for address in addresses):
        return f"loopback:{port}"
    return f"{','.join(addresses)}:{port}"


@dataclass(frozen=True)
class Observation:
    """What one endpoint did once, when, and why it came out that way."""

    tier: str
    recorded: str  # ISO-8601 UTC, when this tier was first seen for this key
    why: str

    def describe(self) -> str:
        return f"{self.tier} on {self.recorded} ({self.why})"


class Capabilities:
    """A record of what each endpoint did. It decides nothing.

    It used to. `Client` seeded its starting rung from this file, so one
    refusal -- or, before M5 entry 8, one blank body -- wrote a demotion that
    every later process inherited without ever testing it again. A tier
    resolution is an observation about one request, not a fact about a server,
    and a file that turns the first into the second is a latch.

    So the ladder now re-derives the answer every process, from the top rung,
    and this file is written for the operator rather than read by the client.
    The revalidation is the descent itself; the cost is the one or two refused
    calls the cache used to save, on the first request of a process against an
    endpoint that genuinely cannot do `response_format`. That is the correct
    price for not carrying a silent, untested verdict between runs.

    What it is still good for is noticing change: `record` hands back what was
    there before, so a resolution that differs from last time gets said out
    loud at the moment it happens.

    Entries written before M5 are bare strings with no timestamp and no reason.
    They are dropped on load rather than migrated -- their whole problem is
    that nothing is known about when or why they were written.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self._data: dict[str, Observation] | None = None

    def _load(self) -> dict[str, Observation]:
        if self._data is None:
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                loaded = {}
            self._data = {}
            for key, value in (loaded if isinstance(loaded, dict) else {}).items():
                if not isinstance(value, dict) or value.get("tier") not in TIERS:
                    continue  # legacy bare string, or something hand-edited
                self._data[key] = Observation(
                    tier=value["tier"],
                    recorded=str(value.get("recorded", "")),
                    why=str(value.get("why", "")),
                )
        return self._data

    @staticmethod
    def _key(endpoint: str, model: str) -> str:
        return f"{endpoint}|{model}"

    def observed(self, endpoint: str, model: str) -> Observation | None:
        return self._load().get(self._key(endpoint, model))

    def record(self, endpoint: str, model: str, tier: str, why: str) -> Observation | None:
        """Write what happened. Returns what was there before, or None.

        A repeat of the same tier is not rewritten, so `recorded` keeps meaning
        "when this endpoint was first seen doing this" rather than "the last
        time anything was asked", and a 291-call sweep does not write the file
        291 times.
        """
        data = self._load()
        previous = data.get(self._key(endpoint, model))
        if previous is not None and previous.tier == tier:
            return previous
        data[self._key(endpoint, model)] = Observation(
            tier=tier,
            recorded=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            # One line, bounded: the reason usually quotes an endpoint's own
            # error body, which arrives with newlines in it and is not
            # length-limited by anything on this side.
            why=" ".join(why.split())[:200],
        )
        # The cache root, and the capability record in it. Not documents,
        # but it lives in the same tree and a mode that is right for one file
        # and wrong for its directory is not a mode anybody can reason about
        # (325).
        # Imported here, not at module scope: `cassette` imports `config` and
        # this module is imported by `client` before either, so a top-level
        # import would be a cycle for the sake of two helpers.
        from .cassette import secure_dir, secure_write
        secure_dir(self.path.parent)
        secure_write(
            self.path,
            json.dumps(
                {key: asdict(value) for key, value in sorted(data.items())}, indent=2
            )
            + "\n")
        return previous

def length_truncation_reason(response: dict) -> str | None:
    """`_empty_reason`'s `finish_reason == "length"` case, or `None` otherwise.

    For a caller that already gave up on this response -- `client._live`'s
    empty-body retry, once it has exhausted `EMPTY_RESPONSE_ATTEMPTS` -- and
    needs to know whether retrying again would help before saying so. It would
    not, for this case: the model spent the whole ceiling reasoning and never
    reached the answer, and the same ceiling on the same prompt produces the
    same outcome. `None` covers an ordinary empty body, a refusal
    (`content_filter`), any other named reason, and a response this function
    cannot parse -- every one of those either has a retry that could help or
    is not this specific, provably-futile case; either way the caller's
    existing generic message still applies.

    Checked on `finish_reason` directly, and not (as before 680) by comparing
    `_empty_reason`'s text against its own generic string: that comparison
    silently started treating a `content_filter` refusal as this case too,
    the moment `_empty_reason` grew a specific sentence for one, because both
    sentences are equally "not the generic one". Asking the field the caller
    actually cares about is what keeps the two from being able to drift apart
    like that again.
    """
    try:
        choice = response["choices"][0]
        message = choice["message"]
    except (KeyError, IndexError, TypeError):
        return None
    if choice.get("finish_reason") != "length":
        return None
    return _empty_reason(response, message)
