"""One shape for the token counts every vendor reports differently.

Why this is its own module rather than three lines where the response is
parsed: the counts are about to become the denominator of a published metric.
The paper compares arms on defects found per dollar and per million tokens, and
that comparison spans local open-weights models and three paid APIs. A number
that means `prompt_tokens` on one arm and `promptTokenCount` on another, and
silently zero on a third because the field was spelled a fourth way, would not
be a metric -- it would be a table of spelling accidents.

Three rules, and each is here because getting it wrong is invisible:

*Unknown is not zero.* A call whose response carried no usage block at all is
unmeasured. A call that genuinely consumed nothing is measured, and its answer
is zero. They render differently everywhere, because a token-free arm and an
unmeasured arm support opposite conclusions about cost.

*The raw block is never discarded.* Normalising is lossy by construction -- it
keeps the fields the metric needs and drops whatever a vendor invents next
week. The provider's own block is already stored verbatim in every cassette's
`response.raw`, so nothing here has to preserve it; this module is the reader,
not the archive.

*No prices live in this codebase.* Tokens are a measurement and a price is a
dated fact about a vendor's website. Cost is computed offline, in the paper
pipeline, against a price table that carries the date it was read.

Field names, and where each was seen:

  input   prompt_tokens (OpenAI chat completions, and every OpenAI-compatible
          endpoint this project has talked to, including ollama, which is the
          shape all 756 recorded cassettes carry), input_tokens (the OpenAI
          responses API and Anthropic's native API), promptTokenCount (Google
          native).
  output  completion_tokens, output_tokens, candidatesTokenCount.
  cached  prompt_tokens_details.cached_tokens, cache_read_input_tokens,
          cachedContentTokenCount. Billed at a different rate by every vendor
          that reports it, which is the whole reason it is carried separately.
  thought completion_tokens_details.reasoning_tokens, thoughtsTokenCount. A
          reasoning model's output count may or may not already include these;
          the raw block is what settles that per vendor, and the paper says
          which convention it read.

The Anthropic and Google spellings are written from their documented native
APIs and have NOT been observed by this code. Both are reached here through an
OpenAI-compatibility endpoint, which is expected to send the OpenAI spelling.
They are accepted anyway, because the cost of a wrong guess is silence.
"""

from __future__ import annotations

# Each entry: the normalised name, then the paths tried in order. A path is a
# tuple so a nested details block is expressed without a parser.
FIELDS: dict[str, tuple[tuple[str, ...], ...]] = {
    "input": (("prompt_tokens",), ("input_tokens",), ("promptTokenCount",)),
    "output": (("completion_tokens",), ("output_tokens",), ("candidatesTokenCount",)),
    "cached": (("prompt_tokens_details", "cached_tokens"),
               ("cache_read_input_tokens",),
               ("cachedContentTokenCount",)),
    "thought": (("completion_tokens_details", "reasoning_tokens"),
                ("thoughtsTokenCount",)),
    "total": (("total_tokens",), ("totalTokenCount",)),
}

NAMES = tuple(FIELDS)

# Whether the model reached the network on its own account, and how often.
# Read, never asked for.
#
# The distinction this exists to keep is the one the whole module is about. A
# model that says it searched has made a claim; `server_tool_use` is a count
# the serving side wrote down, and it is the only honest way to know. It is
# the same line this project already draws between the evidence a verifier
# says it used and `reconcile.grounding_of` going and locating that span.
#
# Observed on `claude --print --output-format json` at 2.1.274, where
# `usage.server_tool_use` reads `{"web_search_requests": 0,
# "web_fetch_requests": 0}` on a call made with no web tools allowed. The same
# block is documented on Anthropic's native messages API, so an endpoint
# reached through a compatibility surface may carry it too; a vendor that
# sends nothing leaves this unmeasured, which is a third state and not zero.
#
# The two are separate counters rather than one "did it use a tool" flag,
# because they are separately grantable and carry different risk: a search is
# a query this tool aimed at nothing in particular, and a fetch is a
# retrieval something *in the documents* may have aimed. See `web.commands`.
SERVER_TOOL_FIELDS: dict[str, tuple[tuple[str, ...], ...]] = {
    "web_search": (("server_tool_use", "web_search_requests"),),
    "web_fetch": (("server_tool_use", "web_fetch_requests"),),
}

SERVER_TOOL_NAMES = tuple(SERVER_TOOL_FIELDS)

# How many turns one call took, which is the one instrument that answers "did
# the model use a tool" on a command backend.
#
# **`SERVER_TOOL_FIELDS` above is structurally blind to it and this is not.**
# That block counts Anthropic's server-side web tools; the subscription CLI's
# `WebFetch` runs locally in the CLI's own process and never increments it.
# Measured: a call that demonstrably fetched -- proved by handing it a hostname
# that cannot resolve and getting the CLI's own `getaddrinfo ENOTFOUND` back --
# still reported `{"web_search_requests": 0, "web_fetch_requests": 0}`. A
# design that read that counter to answer the question would report `0` for a
# run that fetched a hundred pages.
#
# A tool call costs a round trip, so it costs a turn -- and a retrieval costs
# two tool calls, not one. `WebFetch` is a *deferred* tool in this CLI:
# traced through `--output-format stream-json`, one fetch is `ToolSearch`
# loading its schema, then `WebFetch`, then the answer, and `num_turns` reads
# 3, not the 2 an earlier reading assumed. A plain
# answer measured 1 turn on every configuration tried here and 2 on the
# operator's; a web search 4 to 6. `MOST_TURNS_WITHOUT_RETRIEVAL` below
# sits between the two readings of a plain answer and the lowest reading of a
# retrieval, so it is right on both.
#
# **That was the shipped argv, and the isolation changed it.** Under
# `--safe-mode` with a `--tools` naming the web tools alone there is no
# `ToolSearch` to load them through, so one fetch is 2 turns and one search is
# 2 -- three draws each, the same session's shipped argv reading 3 and 3 --
# and a plain answer 1. The floor of 2 would have read every single retrieval
# as none. So the floor follows the argv: `config.only_web_tools` says which
# regime a call ran under and `Turns.add` takes it.
#
# `modelUsage.<model>.webSearchRequests` was read beside it and is not wired:
# it counted each search (1, 1, 1) and is blind to a fetch (0, 0, 0), so it
# cannot replace the turn count, and under either argv a search already
# crosses the floor that argv gets.
#
# **It counts turns and not fetches**, and every reader of it says so. With
# the web tools as the only grant a call past the floor is a retrieval, but that
# is an inference from the grant rather than something this number carries,
# and a report that implied otherwise would be claiming precision the
# instrument does not have.
TURN_FIELDS: tuple[tuple[str, ...], ...] = (("num_turns",),)


def _dig(block: dict, path: tuple[str, ...]):
    for step in path:
        if not isinstance(block, dict):
            return None
        block = block.get(step)
    return block


def usage_block(envelope: dict | None) -> dict | None:
    """The provider's own usage block, or None when the response carried none.

    `usageMetadata` is Google's name for it. An empty dict counts as absent:
    a vendor that sends `"usage": {}` has told us nothing, and treating that
    as a measured zero is the exact confusion this module exists to prevent.
    """
    if not isinstance(envelope, dict):
        return None
    for name in ("usage", "usageMetadata"):
        block = envelope.get(name)
        if isinstance(block, dict) and block:
            return block
    return None


def normalise(envelope: dict | None) -> dict[str, int] | None:
    """Normalised counts for one response, or None if it reported no usage.

    A field the vendor did not send is absent from the result rather than
    zero -- same rule one level down. `cached` and `thought` are absent from
    every cassette in the corpus, and reporting them as zero would claim the
    endpoint measured something it never mentioned.
    """
    block = usage_block(envelope)
    if block is None:
        return None
    counts: dict[str, int] = {}
    for name, paths in FIELDS.items():
        for path in paths:
            value = _dig(block, path)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            counts[name] = int(value)
            break
    # A usage block carrying no *token* field is unmeasured, not measured-at-
    # nothing. This became reachable when `backend.envelope_for` started
    # sending a block holding `server_tool_use` and nothing else: an
    # empty dict here counts the call as measured, `Tokens.describe` then
    # prints "0 in, 0 out", and a run that reported no tokens reads as a run
    # that consumed none. That is the same inversion arriving through a new door,
    # and the rule that closes it is the module's own.
    return counts or None


def server_tools(envelope: dict | None) -> dict[str, int] | None:
    """Per-call counts of the model's own network use, or None if unreported.

    None is `unmeasured` and is never zero, for `normalise`'s reason one field
    over: "this endpoint does not report tool use" and "this call used no
    tools" support opposite conclusions about where a citation came from, and
    an int cannot hold the difference.

    A block that is present but names neither counter also answers None. A
    vendor that sent `server_tool_use: {}` has told us nothing, and the empty
    dict would otherwise read as a measured absence.
    """
    block = usage_block(envelope)
    if block is None:
        return None
    counts: dict[str, int] = {}
    for name, paths in SERVER_TOOL_FIELDS.items():
        for path in paths:
            value = _dig(block, path)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            counts[name] = int(value)
            break
    return counts or None


def turns(envelope: dict | None) -> int | None:
    """How many turns this call took, or None when the backend did not say.

    None is `unmeasured` and is never zero or one, for `server_tools`' reason
    one field over: every HTTP endpoint this project talks to reports nothing
    here, and reading that silence as "a plain answer, so no tool use" would turn
    every hosted run into a claim that the model did not look anything up.
    """
    block = usage_block(envelope)
    if block is None:
        return None
    for path in TURN_FIELDS:
        value = _dig(block, path)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        return int(value)
    return None


def answered_by(envelope: dict | None) -> dict | None:
    """Which model ids answered this call, or None when the backend did not say.

    Only a command backend's synthesised envelope carries it
    (`backend.models_named`): the ids its CLI named under `modelUsage`, and
    `output`, the one that wrote the answer. An alias on the route is the
    CLI's to resolve and moves when a new version ships under it, so this is
    the only record of which model a figure came from. None for every HTTP
    envelope and every cassette recorded before it existed -- not "no model",
    for `turns`' reason.
    """
    if not isinstance(envelope, dict):
        return None
    block = envelope.get("answered_by")
    if not isinstance(block, dict):
        return None
    models = block.get("models")
    if not isinstance(models, list) or not models or not all(
            isinstance(name, str) and name for name in models):
        return None
    output = block.get("output")
    return {"models": list(models),
            "output": output if isinstance(output, str) and output in models else None}


def served_model(envelope: dict | None) -> str | None:
    """The HTTP response's own top-level `model` field, when it named one.

    Kept apart from `answered_by` on purpose, and reading a different key
    than that function does -- not folded into it, and not read by it: a
    hosted vendor endpoint's `model` can genuinely be more specific than the
    alias a route asked for (a pinned alias resolving to a dated id the
    operator did not type), but most of this project's own traffic is a
    local endpoint that only ever echoes back the string it was asked for.
    `answered_by`'s whole contract is "the backend said who really answered,
    on evidence the alias itself cannot fake"; a bare echo does not clear
    that bar, which is why `test_a_result_envelope_names_the_models_that_answered`
    pins `answered_by({"model": ...})` at `None` and must go on doing so. This
    function names the same field under its own name instead: a self-reported
    label, recorded as one, for a caller that already knows which kind of
    endpoint answered and can judge it accordingly.
    """
    if not isinstance(envelope, dict):
        return None
    served = envelope.get("model")
    return served if isinstance(served, str) and served.strip() else None


# The three states, written once. Every reader spells them the same way, and a
# fourth spelling somewhere would be a fourth state nothing renders.
SEARCHED = "searched"
NOT_SEARCHED = "not-searched"
UNMEASURED = "unmeasured"
SEARCH_STATES = (SEARCHED, NOT_SEARCHED, UNMEASURED)


class Searches:
    """A run's account of whether the model went and looked anything up.

    Three states, and the third is why this is a class rather than an int,
    not just a bool:

      searched     some call reported a non-zero count. The model reached the
                   network in its own process, which is where a real citation
                   can come from.
      not searched every call that reported reported zero. The model answered
                   from what it knows, and any citation in the output is a
                   recollection.
      unmeasured   no call reported at all -- an endpoint that does not send
                   the block, or a command backend not configured to hand its
                   envelope back. Not zero, for `Tokens`'s reason.

    **This is a measurement about the model's process, not about this one.**
    LLossless opens no socket for any purpose, and the acceptance test for that
    is what proves it. A model that searched did so on the serving side; the
    two facts are independent and the reports state both, because stating
    either alone is misleading in one direction or the other.
    """

    def __init__(self) -> None:
        self.totals: dict[str, int] = {}
        self.measured = 0
        self.unmeasured = 0

    def add(self, envelope: dict | None) -> dict[str, int] | None:
        counts = server_tools(envelope)
        if counts is None:
            self.unmeasured += 1
            return None
        self.measured += 1
        for name, value in counts.items():
            self.totals[name] = self.totals.get(name, 0) + value
        return counts

    @property
    def known(self) -> bool:
        """Did anything report? False means unmeasured, never "no searches"."""
        return self.measured > 0

    @property
    def total(self) -> int | None:
        """Every reported request, or None when nothing reported."""
        if not self.known:
            return None
        return sum(self.totals.values())

    @property
    def state(self) -> str:
        """`searched`, `not-searched` or `unmeasured`. One word for a reader."""
        if not self.known:
            return UNMEASURED
        return SEARCHED if (self.total or 0) > 0 else NOT_SEARCHED

    def as_dict(self) -> dict:
        """What reaches the JSON report. Absent counters stay absent."""
        return {
            **{name: self.totals[name] for name in SERVER_TOOL_NAMES
               if name in self.totals},
            "state": self.state,
            "measured_calls": self.measured,
            "unmeasured_calls": self.unmeasured,
        }

    def describe(self) -> str:
        """One line for the provenance table, in the reader's terms.

        Never the bare word `0`. A run where nothing reported and a run where
        every call reported zero read identically as a number and mean
        different things, so each says which it is in words.
        """
        if not self.known:
            if not self.unmeasured:
                return "no calls"
            return (f"unmeasured ({self.unmeasured} call(s) reported no "
                    f"tool use)")
        parts = [f"{self.totals.get(name, 0):,} {name.replace('_', ' ')}"
                 for name in SERVER_TOOL_NAMES if name in self.totals]
        if (self.total or 0) == 0:
            line = "no web tool use reported (" + ", ".join(parts) + ")"
        else:
            line = ", ".join(parts)
        if self.unmeasured:
            line += f" ({self.unmeasured} call(s) unmeasured)"
        return line



# The three states of the turn counter, written once, and deliberately not the
# three above. `searched` is a count of web requests; this is a count of turns,
# and giving the two one vocabulary is how a report ends up saying "searched"
# about a number that cannot see a search.
TOOL_USE = "tool-use"
NO_TOOL_USE = "no-tool-use"
TOOL_USE_STATES = (TOOL_USE, NO_TOOL_USE, UNMEASURED)

# What a `sourced` run owes its reader about retrieval, in three words.
# Not `TOOL_USE_STATES` renamed: the two disagree on a run where some calls
# reported and some did not. `state` calls that run `no-tool-use` off the
# calls that reported; this calls it `unmeasured`, because a call that did not
# report may be the one that retrieved, and "did not retrieve" said over an
# absent measurement is the inversion this module refuses everywhere.
RETRIEVED = "retrieved"
NOT_RETRIEVED = "not-retrieved"
RETRIEVAL_STATES = (RETRIEVED, NOT_RETRIEVED, UNMEASURED)

# The most turns a call can take without having retrieved anything.
#
# Was `TURNS_WITHOUT_TOOLS = 1`, from an earlier measurement of one fetch as two
# turns, and that threshold overstated on every command-backend run: a call
# that spent a turn and retrieved nothing -- a deferred tool loaded and never
# called, or the second turn the operator's plain answers report -- counted as
# tool use. The operator's run printed "11 of 12 call(s) used a tool (27
# turn(s) in total)", which is 2.25 turns a call and cannot be eleven fetches
# at three turns each. A retrieval costs three turns at the least, so two is
# the floor and anything above it retrieved.
#
# **Erring low here is the safe direction and erring high is not.** A fetch
# missed by this floor reads as recall, which makes a reader trust a citation
# less than it deserves; a plain answer counted as a fetch reads as verified,
# which is the inversion the `sourced` level exists to prevent.
MOST_TURNS_WITHOUT_RETRIEVAL = 2

# The same floor for a call whose argv left the model no tool but the web tools
# (`config.only_web_tools`). Nothing else can spend a turn there: no
# `ToolSearch`, no hook, no other tool -- so the first turn past the answer is
# a web tool call. Measured: a plain answer 1 turn, one fetch 2, one search 2.
MOST_TURNS_WITHOUT_RETRIEVAL_WEB_ONLY = 1


class Turns:
    """A run's account of whether the model used a tool, read off `num_turns`.

    `Searches`' sibling, and the two are kept apart on purpose. They answer the
    same question through different instruments and they disagree on this
    backend: `server_tool_use` is blind to a local `WebFetch` and reports zero
    for a run that fetched, and this counter sees the round trip the fetch
    cost. Folding them into one state would publish whichever happened to be
    written last.

      tool use     some call took more turns than a retrieval-free call can
                   (`MOST_TURNS_WITHOUT_RETRIEVAL`, or `..._WEB_ONLY` under
                   the isolated argv). The model called a tool and, with
                   retrieval as the only grant, retrieved.
      no tool use  no call that reported went past that floor. The model may
                   have spent a turn loading a tool, and fetched nothing, so
                   every citation is recall.
      unmeasured   no call reported at all -- an HTTP endpoint, or a command
                   backend whose route does not ask for the result envelope.
                   Not "no tool use", for `Tokens`' reason.

    **This says nothing about what LLossless did.** It opens no socket for any
    purpose; a turn spent on a tool was spent in the model's own process. The
    reports state both facts and keep them apart.
    """

    def __init__(self) -> None:
        self.total = 0
        self.calls = 0
        self.with_tools = 0
        self.unmeasured = 0
        # The same tally per role, beside the run-wide one. At `sourced`
        # the grant is run-wide, so decompose and verify calls may retrieve
        # too -- measured on CLI 2.1.274, five of seven low-effort verify and
        # decompose calls of one voyager run took 2-5 turns -- and a run-wide
        # "retrieved" can then stand over a merge that recalled every source
        # it names. `report.retrieval_turns` judges the level on the merge's.
        # Empty for a tally fed without roles, which reads as it always did.
        self.roles: dict[str, Turns] = {}

    def add(self, envelope: dict | None, *, web_only: bool = False,
            role: str | None = None) -> int | None:
        """Tally one call. `web_only` is `config.only_web_tools` of its argv.

        Per call rather than per run, because the floor is a property of the
        argv a call executed; the floors are read here, at call time, so both
        stay one name each. `role`, where the caller knows it, also files the
        call under `roles[role]`.
        """
        if role is not None:
            self.roles.setdefault(role, Turns()).add(envelope, web_only=web_only)
        count = turns(envelope)
        if count is None:
            self.unmeasured += 1
            return None
        self.calls += 1
        self.total += count
        floor = (MOST_TURNS_WITHOUT_RETRIEVAL_WEB_ONLY if web_only
                 else MOST_TURNS_WITHOUT_RETRIEVAL)
        if count > floor:
            self.with_tools += 1
        return count

    @property
    def known(self) -> bool:
        """Did anything report? False means unmeasured, never "no tool use"."""
        return self.calls > 0

    @property
    def state(self) -> str:
        """`tool-use`, `no-tool-use` or `unmeasured`. One word for a reader."""
        if not self.known:
            return UNMEASURED
        return TOOL_USE if self.with_tools else NO_TOOL_USE

    @property
    def retrieval(self) -> str:
        """`retrieved`, `not-retrieved` or `unmeasured`.

        Retrieved as soon as one call crossed the floor, whatever the others
        reported. Not retrieved only when **every** call reported and none
        crossed it: one silent call is enough to make the absence unproven.
        """
        if self.with_tools:
            return RETRIEVED
        if not self.known or self.unmeasured:
            return UNMEASURED
        return NOT_RETRIEVED

    def as_dict(self) -> dict:
        """What reaches the JSON report."""
        return {
            "state": self.state,
            "retrieval": self.retrieval,
            "turns": self.total,
            "calls_with_tool_use": self.with_tools,
            "measured_calls": self.calls,
            "unmeasured_calls": self.unmeasured,
        }

    def describe(self) -> str:
        """One line for the provenance table, in turns rather than in fetches.

        Never the word "fetch" and never a fetch count. The number is turns;
        what a turn past the floor was spent on is not in it, and a sentence
        that said otherwise would be inventing the precision.
        """
        if not self.known:
            if not self.unmeasured:
                return "no calls"
            return (f"unmeasured ({self.unmeasured} call(s) reported no turn "
                    f"count)")
        if not self.with_tools:
            # The total rather than "one turn each", which stopped being true
            # when the floor moved to two.
            line = (f"no tool use ({self.calls} call(s), {self.total} turn(s) "
                    f"in total)")
        else:
            line = (f"{self.with_tools} of {self.calls} call(s) used a tool "
                    f"({self.total} turn(s) in total)")
        if self.unmeasured:
            line += f" ({self.unmeasured} call(s) unmeasured)"
        return line


class Tokens:
    """A run's token totals, with unmeasured calls counted rather than dropped.

    Deliberately not a dataclass of five ints: the point of this type is that
    "nothing was measured" and "zero was measured" are different states, and an
    int cannot hold that difference. `measured` and `unmeasured` do.
    """

    def __init__(self) -> None:
        self.totals: dict[str, int] = {}
        self.measured = 0
        self.unmeasured = 0

    def add(self, envelope: dict | None) -> dict[str, int] | None:
        counts = normalise(envelope)
        if counts is None:
            self.unmeasured += 1
            return None
        self.measured += 1
        for name, value in counts.items():
            self.totals[name] = self.totals.get(name, 0) + value
        return counts

    def get(self, name: str) -> int | None:
        """A total, or None when no call reported that field. Never a false zero."""
        return self.totals.get(name)

    @property
    def known(self) -> bool:
        return self.measured > 0

    def as_dict(self) -> dict:
        """What reaches the JSON report. Absent fields stay absent."""
        return {
            **{name: self.totals[name] for name in NAMES if name in self.totals},
            "measured_calls": self.measured,
            "unmeasured_calls": self.unmeasured,
        }

    def describe(self) -> str:
        """One line for the provenance table.

        `unknown` when nothing was measured, and it says how many calls it is
        unknown for -- a reader who sees `0 in, 0 out` should be able to trust
        that a model really was asked for nothing.
        """
        if not self.known:
            if not self.unmeasured:
                return "no calls"
            return f"unknown ({self.unmeasured} call(s) reported no usage)"
        parts = [f"{self.totals.get('input', 0):,} in",
                 f"{self.totals.get('output', 0):,} out"]
        if "cached" in self.totals:
            parts.append(f"{self.totals['cached']:,} cached")
        if "thought" in self.totals:
            parts.append(f"{self.totals['thought']:,} reasoning")
        line = ", ".join(parts)
        if self.unmeasured:
            line += f" ({self.unmeasured} call(s) unmeasured)"
        return line
