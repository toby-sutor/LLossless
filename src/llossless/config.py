"""Runtime configuration: env vars, flags, and the role -> model mapping.

Everything the client needs to reach an endpoint is resolved here, once, and
passed around as an immutable Settings. Nothing else in the codebase reads
os.environ.

Two rules shape this module and are worth stating out loud:

1. The default base URL is localhost. A hosted endpoint is always something the
   operator opted into, never something a default did to them.
2. The API key is read indirectly, via the *name* of the variable that holds
   it. A corporate setup can point LLOSSLESS_API_KEY_ENV at a variable that
   already exists rather than copying a secret into a second place. The key
   itself never leaves this module except as an Authorization header built at
   send time; it is not stored on any object that gets serialised.

The code refers to logical roles — merge, verify, decompose — and never to a
model id. The mapping lives in models.local.json, which is gitignored because it
is one machine's configuration, not because a model id is a secret. It is not:
the report records the id actually used, because which model produced a number
is the first thing anyone reading that number needs to know.
"""

from __future__ import annotations

import contextlib
import contextvars
import hashlib
import json
import os
import re
import shlex
from dataclasses import dataclass, field, replace
from pathlib import Path
from urllib.parse import urlsplit

# The one import this module makes from its own package, and it is a table of
# constants rather than behaviour: the request-shape profiles are named in a
# flag's `choices` and validated out of the environment here, and a second copy
# of their names in this file would be a list that goes stale the first time
# the table gains a row. `structured` imports nothing from `llossless`, so
# this cannot become a cycle.
from .structured import DEFAULT_PROFILE, PROFILES

ROOT = Path(__file__).resolve().parents[2]

# How a command backend's stdout is read. Named here rather than in
# `backend.py` for one reason and it is not tidiness: `backend` imports
# `transport`, `transport` can open a socket, and both are imported lazily
# inside `Client._request` so that a replay run never loads either. `config`
# is imported by everything, so a constant it reads out of `backend` would
# pull the socket module into every offline run and break the containment
# `acceptance_replay_never_loads_the_transport_module` exists to hold. This
# module already owns the other command-backend setting (`COMMAND_TIMEOUT`),
# so it owns this one.
#
# `raw`    stdout is the answer, byte for byte. What this backend has always
#          done, what an arbitrary wrapper script produces, and the default.
# `result` stdout is a single JSON result envelope whose `result` holds the
#          text and whose `usage` holds the token block and `server_tool_use`.
#          Two of the three things otherwise unknowable on this path.
#
# Declared per route, never detected: the answer under `raw` is itself JSON,
# so a sniffer would be choosing between two JSON objects on the presence of
# a key.
ENVELOPE_RAW = "raw"
ENVELOPE_RESULT = "result"
COMMAND_ENVELOPES = (ENVELOPE_RAW, ENVELOPE_RESULT)

# The flag and the value that make a command answer with a result envelope,
# and the one place either is spelled. Here rather than in `web/commands.py`,
# which is where they were written, for the reason `WEB_TOOLS` below is here:
# two ways in need the same two strings -- a route on the web server and a
# command line -- and `web/commands.py` imports this module while nothing in
# this module may import that one. A second spelling of the rule would be a
# second answer to one question, which is the confusion the pair exists to
# stop.
#
# Long form, like `ALLOW_TOOLS_FLAG`: the argv is read back by a check, and a
# reader comparing the two should not have to know a short form is one flag.
RESULT_FORMAT_FLAG = "--output-format"
RESULT_FORMAT_VALUE = "json"
RESULT_ARGS = (RESULT_FORMAT_FLAG, RESULT_FORMAT_VALUE)

# The model's own web tools, by the name an allowlist flag takes, and the flag
# they go in. Here rather than in `web/commands.py`, which is where they were
# written and is still where the *policy* about them lives: two callers need
# the same three strings now, and `web/commands.py` imports this module while
# nothing in this module may import that one. It is one closed table in a place
# both paths can read, which is the property `WEB_TOOLS` was written for --
# there is no expression anywhere that joins a submitted string to a tool name.
#
# `claude --help` at 2.1.274 spells the flag *"--allowedTools,
# --allowed-tools <tools...>"*, comma or space separated. The long form,
# because the argv is read back by `granted_web_tools` and a reader comparing
# the two should not have to know they are one flag.
WEB_SEARCH = "WebSearch"
WEB_FETCH = "WebFetch"
WEB_TOOLS = (WEB_SEARCH, WEB_FETCH)
ALLOW_TOOLS_FLAG = "--allowed-tools"

# Which program this build knows how to grant retrieval to, and what it grants
# it. Keyed by the program's **basename**, because a route's command
# is an absolute path as often as not and where a binary lives is a fact about
# the machine rather than about the tool.
#
# **Both tools, each observed to fire.** Testing granted `WebFetch` alone at
# first, calling `--allowed-tools WebSearch` a no-op because the CLI listed no
# such tool. That list was read through a local proxy which stripped the tool,
# and every probe ran through it. Without the proxy the tool is there. This
# grant's own argv, `--allowed-tools WebSearch,WebFetch` at 2.1.274, answered a
# question that needs a search with sources, two searches in `modelUsage`, and
# `num_turns` 4, above the no-retrieval floor of 2. `WebFetch` also fired on a
# URL that could not resolve: the CLI's own `getaddrinfo ENOTFOUND` came back.
#
# **The operator decided this, and their reasoning is recorded rather than
# assumed.** *"I think WebSearch should be on"*, and on the grant: *"make it
# automatic and make it obvious in the UI. It is not that big of a change
# anyway as using frontier models capable of websearch already sends the data
# out of the machine anyway, so a search is likely no bigger harm. We just need
# to be transparent."* `WebFetch` is the riskier tool: a URL inside a hostile
# document is a way to aim a fetch. So the grant is automatic and every surface
# says it is in force; what it is not is silent.
AUTO_GRANT: dict[str, tuple[str, ...]] = {"claude": (WEB_SEARCH, WEB_FETCH)}
assert all(set(tools) <= set(WEB_TOOLS) for tools in AUTO_GRANT.values())


# Is this module running out of a checkout, or out of site-packages? None of the
# three paths below is package data -- one is the operator's, one is scratch,
# one is this repository's test corpus -- so none of them may be baked into the
# wheel, and all three answer differently depending on which of the two it is.
# `parents[2]` is right in a checkout and meaningless in a wheel, where it names
# the directory above site-packages.
#
# Asked by looking for the two things a checkout has and an install does not.
IN_CHECKOUT = (ROOT / "pyproject.toml").is_file() and (ROOT / "src" / "llossless").is_dir()

DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_TIMEOUT = 120.0

# The same bound for a command backend, and it is a different quantity rather
# than a larger version of the one above.
#
# Over HTTP the run streams, so every chunk renews the clock and 120 s means
# "this endpoint has gone silent for two minutes", which is a wedged endpoint
# and should be reported quickly. A subprocess has no chunks: `backend.run`
# hands `timeout` to `subprocess.run`, so the same figure means "the whole call
# finished within two minutes" -- a far tighter constraint on a backend that is
# slower for two further reasons. It answers at the `prompt` tier, where the
# model writes the whole merged document out as text instead of being
# constrained by a schema, and it pays process start-up per call.
#
# **The figure is a floor taken from one measurement, not a characterised
# distribution.** One merge of a 2.3 KB pair at `--fidelity open
# --verify-depth coverage` through `claude --print --model haiku` completed in
# 534 s over three calls: 178 s a call on the *fastest* model the command
# catalogue offers, with two small documents. 890 is that mean times five. It
# also clears the only per-call upper bound the measurement actually supports
# -- no single call in that run can have exceeded the 534 s the whole run took
# -- by 1.7x. A larger pair or a slower model will beat it, and the answer then
# is `--timeout`, `LLOSSLESS_TIMEOUT`, or the route's own `timeout`.
COMMAND_TIMEOUT = 890.0

# How many claims go in one verify call, over HTTP and through a command.
#
# Named here rather than in `verify.py` for `COMMAND_TIMEOUT`'s reason one line
# up: this module owns the settings a backend resolves differently, and
# `verify.py` re-exports `DEFAULT_BATCH` under the name it has always had.
#
# **25 over HTTP, and it does not move.** Every one of the 334 recorded verify
# cassettes was made at that figure, batch size reaches `messages`, and
# `messages` is a cassette-key component -- so raising it globally would orphan
# the corpus every published figure in this project comes from.
#
# **100 through a command, and this is now a measurement.** It was set from
# an argument: a six-word prompt reported 16,586 cache-creation
# tokens, therefore the per-call cost is nearly fixed at ~120 s, therefore
# fewer calls must win. The first two steps were wrong. One verify call was
# timed at four batch sizes against test-12's own claims and prompts, through
# `claude --print --model sonnet`:
#
#     claims   forward   s/claim      reverse   s/claim
#         10    31.9 s      3.19       46.9 s      4.69
#         25    68.2 s      2.73       63.5 s      2.54
#         50    86.9 s      1.74      107.5 s      2.15
#         90   141.4 s      1.57      164.6 s      1.83
#
# Least squares: forward 25.7 s fixed + 1.289 s a claim, reverse 29.9 s +
# 1.502 s. So the fixed cost is ~26-30 s and not ~120 s, and the per-claim
# term is real rather than negligible -- but the curve is **sub-linear per
# claim**, so the conclusion reached from the wrong premise still holds: over 90
# claims each way, batch 25 is eight calls and ~474 s and batch 100 is two
# calls and ~307 s. All eight timed answers graded every claim they were
# given, in order, at every size up to 90.
#
# What a bigger batch costs in accuracy is still unmeasured and is still stated
# as unmeasured: more claims in one answer is more for a model to keep
# straight. What bounds the risk is that Pass C salvage is on in
# `cli.pipeline` -- an unusable record is dropped by name and the rest of the
# batch is still graded -- so a larger batch no longer means a larger
# blast radius for one bad record.
#
# **And batch size is not the lever that matters here.** On the same pair one
# merge call took 564 s on its own, 91% of it reasoning tokens, which no batch
# size touches. `AUTO_EFFORT` below is the answer to that, and
# `--verify-depth coverage` is the one a reader chooses: it makes no reverse
# pass at all, which would have made the operator's 13-call run 4 calls.
DEFAULT_VERIFY_BATCH = 25
COMMAND_VERIFY_BATCH = 100

# How hard a subscription CLI is asked to think, for programs whose flags this
# build has read. A sibling of `AUTO_GRANT` above, with the same rule and
# the same reason: a flag is appended only to a named program, never to a
# wrapper script whose arguments nobody here has seen, and never over a choice
# the operator made themselves.
#
# **Reasoning is where the time goes on this backend.** Measured on test-12,
# through `claude --print --model sonnet`, default effort against `low`:
#
#     call                    default    low     output tokens, thinking share
#     merge                    564.2 s   50.9 s  58,219 -> 4,730   (91% -> 22%)
#     decompose one source      95.4 s   17.3 s  12,579 -> ?       (83%)
#     verify, 90 claims (fwd)  141.4 s   60.9 s  20,688 -> 9,363   (63% -> 21%)
#     verify, 90 claims (rev)  164.6 s   84.1 s  22,933 -> 12,254  (66% -> 39%)
#
# End to end on the operator's own three-source pair at `open` and `full`:
# **1,585 s before, 352 s after** over seven calls, on the tree this table
# ships in. A second low-effort run of the same pair took 531 s over eight,
# the extra one a schema repair on a `reason` field two characters over its
# cap. Both beat the baseline; neither repeats the other, because nothing on
# this path does.
#
# **This is a speed setting and it is not free** -- and a later pass measured
# the bill an earlier one could not. `low` against `high` through the pipeline, one variable,
# unproxied: voyager at `sourced`/`full` 245.4 s and 817.4 s, bip39 at
# `sourced`/`coverage` 132.2 s and 408.8 s, for 10 and 17 correction records
# on the first pair and 7 and 11 on the second.
#
# **Those record counts are not a quality measure, and reading them as one is
# the trap this comment exists to mark.** The record count *falls* from 27 to
# 14 as the level rises on the single calls below, because a higher level
# consolidates several corrections into one broader record. The calls were
# then scored against 22 seeded errors typed from reading the voyager pair; a
# diff of the pair finds 47, counting one per changed word (the published key
# counts one per changed unit, 44). Re-scored on the merged text, of the 47:
#     setting                wall     records   fixed of 47   kept
#     medium, thinking off   125 s      13          42           5
#     medium, thinking on    130 s      27          46           1
#     high,   thinking on    165 s      19          39           6
#     xhigh,  thinking on    230 s      14          42           5
#
# One draw per row, on one pair. The whole pipeline at `sourced`/`full`, one or
# two draws a level, fixed 22 and 12 at `low`, 23 and 22 at `medium`, 34 and
# 20 at `high`. **No level is clearly better**, so the merge takes `medium` as
# a default rather than as a finding: ~20% faster than `high` and ~45% faster
# than `xhigh` on the single calls. Thinking stays on; 42 against 46 with it
# off is one draw each and separates nothing. A planted error neither fixed
# nor kept is `other`: reworded, dropped or corrected to a third wrong value,
# so the scorer prints its text and the count alone says little.
#
# The level is **per role**, because the roles do not share the bill. Every
# correction in either measurement was declared by the merge -- `declarations`
# is authored by it, and `decompose` and `verify` cannot add a row to that
# list, only grade one. A single level pays for all six calls of a `full` run
# to improve the one that declares anything. Judging a claim against a
# document is not a reasoning-heavy task and the verify answers held up at
# `low` -- every timed call graded every claim it was given, in order -- so
# `decompose` and `verify` keep the `low` setting and the speed work stands.
#
# An operator who wants something else says so and is obeyed: `--effort`,
# `LLOSSLESS_EFFORT`, `LLOSSLESS_EFFORT_<ROLE>`, or a level written into
# their own command, which this build has never overwritten and still does not.
EFFORT_FLAG = "--effort"
# `claude --help` at 2.1.274: *"--model <model>  Model for the current session.
# Provide an alias for the latest model"*. Read by `stated_model`.
MODEL_FLAG = "--model"
# `claude --help` at 2.1.274: *"--effort <level>  Effort level for the current
# session (low, medium, high, xhigh, max)"*. Named here so the table below is
# checked against the levels the binary documents rather than against a string
# somebody typed, which is the standard `web/commands.HELP` rows are held to.
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
# Program basename -> role -> level. Nested rather than flat because the whole
# finding above is that one number cannot be right for both halves of a run:
# the merge writes the document and the other two read it back.
AUTO_EFFORT: dict[str, dict[str, str]] = {
    "claude": {"merge": "medium", "decompose": "low", "verify": "low"},
}
assert all(level in EFFORT_LEVELS
           for table in AUTO_EFFORT.values() for level in table.values())
# The merge's level per model alias, laid over the program's row above.
# The operator's ruling: a subscription route runs Opus with the
# merge at `high`, Sonnet at `medium`. Read off the argv's own `--model`
# (`stated_model`), so an argv naming no model, or an alias this table does not
# name -- `fable`, never measured, or a dated id -- keeps the program's row and
# no level is claimed for a model nobody ran. Merge only: decompose and verify
# stay at the `low` setting for every model, because they read the merge's work back.
#
# No `haiku` row: see `SINGLE_LEVEL_MODELS` below, which
# refuses this table -- and the program's own row above it -- before either is
# consulted, so a model named here can only ever be one this build measured a
# graded scale on.
AUTO_EFFORT_BY_MODEL: dict[str, dict[str, dict[str, str]]] = {
    "claude": {"opus": {"merge": "high"}, "sonnet": {"merge": "medium"}},
}
assert set(AUTO_EFFORT_BY_MODEL) <= set(AUTO_EFFORT)
assert all(set(row) == {"merge"} and row["merge"] in EFFORT_LEVELS
           for models in AUTO_EFFORT_BY_MODEL.values() for row in models.values())

# Which models take one level of effort -- extended thinking on or off -- and
# never the graded scale `--effort` moves, in the operator's own
# words: *"Haiku does not provide effort levels like sonnet or opus do. It
# only allows 'extended' reasoning on/off. We should keep the default and flag
# it accordingly that it only has one level."*
#
# Matched against `stated_model`'s own reading of the argv's `--model` --
# the alias a route's argv carries (`haiku`, `ToolModel.select` in
# `web/commands.py`) or a full or dated id an operator typed themselves
# (`claude-haiku-4-5`, `claude-haiku-4-5-20251001`) -- the same string
# `AUTO_EFFORT_BY_MODEL` above is keyed by, so a route naming either spelling
# is caught the same way. Only Haiku is named: a model this build has never
# measured keeps its silence rather than being guessed into either bucket,
# the refusal `auto_effort` already makes for a program it does not recognise.
SINGLE_LEVEL_MODELS = re.compile(r"^(haiku|claude-haiku-.*)$")
# The label a report gives such a route in place of a claimed level.
SINGLE_LEVEL_LABEL = "one level (extended thinking on/off; default kept)"


def is_single_level_model(model: str) -> bool:
    """Does `model` (an argv's own `--model`, as `stated_model` reads it) name
    a model this build knows takes one level of effort rather than a scale?

    The one place this is decided, so `auto_effort`, `effort_of` and every web
    surface that has to say the same thing about a Haiku route read it off
    here rather than each holding its own copy of `SINGLE_LEVEL_MODELS`.
    """
    return bool(model) and SINGLE_LEVEL_MODELS.match(model) is not None
# Never `low` for the merge in a row this build picks: testing found it the
# one level that separates, downwards, and at `sourced` it retrieved in 2 of 6
# voyager draws. A person may still ask for it; the table never does, and the
# page's effort card says it is not recommended for looking facts up.
MERGE_EFFORT_NOT_AT_SOURCED = ("low",)
assert all(table["merge"] not in MERGE_EFFORT_NOT_AT_SOURCED
           for table in AUTO_EFFORT.values())
assert all(row["merge"] not in MERGE_EFFORT_NOT_AT_SOURCED
           for models in AUTO_EFFORT_BY_MODEL.values() for row in models.values())

DEFAULT_MAX_CALLS = 200
DEFAULT_KEY_ENV = "LLOSSLESS_API_KEY"

# The tool had a different name earlier. Every variable it reads is
# `LLOSSLESS_*`, and its config and cache directories are `llossless`. The old
# prefix and directories under that former name were read as fallbacks for
# one phase and are no longer read at all: an old variable, file
# or directory is ignored, silently, as any unrelated name would be.
DIR_NAME = "llossless"


def config_file(name: str, environ=None) -> Path:
    """`$XDG_CONFIG_HOME/llossless/<name>`: where the operator's config file `name` lives.

    Takes its environment as an argument, where `_xdg` reads `os.environ`, so a
    check with an opinion about where a file goes can say so without editing
    the environment of the process running the suite.
    """
    source = os.environ if environ is None else environ
    base = (source.get("XDG_CONFIG_HOME") or "").strip()
    root = Path(base) if base else Path.home() / ".config"
    return root / DIR_NAME / name


def _xdg(variable: str, fallback: str) -> Path:
    """An XDG base directory, honouring the variable and falling back per spec."""
    named = os.environ.get(variable, "").strip()
    return Path(named) if named else Path.home() / fallback


MODEL_MAP_NAME = "models.local.json"

# Operator data. In a checkout it is the file beside `pyproject.toml`, exactly
# as before. Installed, there is no repository to put it in, so: the directory
# the operator is standing in first -- one model map per project is how anyone
# with two of them will want it -- then the XDG config location for the machine
# they are on. `LLOSSLESS_MODEL` overrides both and skips the file entirely,
# which is the escape hatch for anyone whose answer is neither.
#
# Every candidate is kept, not just the winner: a run that finds no model has to
# say where it looked, and "models.local.json" on its own is a filename, not an
# instruction.
MODEL_MAP_CANDIDATES = (
    (ROOT / MODEL_MAP_NAME,) if IN_CHECKOUT else
    (Path.cwd() / MODEL_MAP_NAME, _xdg("XDG_CONFIG_HOME", ".config") / DIR_NAME / MODEL_MAP_NAME)
)
MODEL_MAP_FILE = next((p for p in MODEL_MAP_CANDIDATES if p.is_file()),
                      MODEL_MAP_CANDIDATES[-1])

# Runtime scratch. Never inside site-packages: an installed package writing into
# its own installation directory is a package that breaks on a read-only install
# and leaves files behind on an uninstall. The checkout keeps a gitignored
# directory beside the code.
CACHE_DIR = ((ROOT / ".llossless-cache") if IN_CHECKOUT
             else _xdg("XDG_CACHE_HOME", ".cache") / DIR_NAME)

# This repository's recorded corpus, which is a test fixture and is not shipped.
# An installed user has no `tests/`; the path below then names the corpus of a
# checkout they might be standing in, and is refused by name when it is not
# there (`apply_arguments`). `--offline` is not on the installed command at all
# -- `add_arguments(corpus_tools=False)` drops it -- so this is reachable only
# from a harness, which is the only caller that has any business with it.
OFFLINE_CASSETTES = (ROOT if IN_CHECKOUT else Path.cwd()) / "tests" / "responses"

# What an operator may write in a boolean variable. Spelled out rather than
# taken as "anything that is not empty is true", so that LLOSSLESS_STREAM=false
# turns streaming off instead of on, which is the way that mistake goes.
TRUTHY = frozenset({"1", "true", "yes", "on"})
FALSEY = frozenset({"0", "false", "no", "off"})

ROLES = ("merge", "verify", "decompose")

# Here rather than beside `AUTO_EFFORT`, which is defined above this line: a
# table that names two of three roles would leave the third on the program's
# own default without saying so, and "nothing was chosen for verify" is the
# one state this table must not be able to express by accident.
assert all(set(table) == set(ROLES) for table in AUTO_EFFORT.values())

# Which roles emit a reasoning block when nothing says otherwise. None, by
# default -- empty, see below -- though merge is the one role the measurement
# argues for and it is a quality argument rather than a tuning one: over the
# twelve fixtures common to every recording, every merge cell measured is at
# or above 97.5% forward coverage except `thinking off` on today's prompt,
# which recorded 225/243 and then returned 212/243 on a live re-run of the
# identical configuration a day later. Decompose and verify stay off
# regardless of that argument. Their corpora were recorded off, their
# published figures are off, and neither is in question -- flipping them
# would re-key every cassette and buy nothing.
#
# Off is still reachable and still cheap to ask for: `LLOSSLESS_THINKING` is
# authoritative whenever it is set at all, so set-but-empty means no role
# thinks. Unset is the only case that falls back to this.
# The default is empty for two reasons that still hold and a third that turned out
# false. `qwen3.8:27b` spent all 12,800 completion tokens in the reasoning channel
# on a 4,344-token prompt and returned no content, three times,
# deterministically -- the same mechanism as `gpt-oss:120b`'s empty body, on an
# unrelated family. An earlier measurement also found thinking on this role *worse*
# (P1 1/12 to 4/12, s = 0.0) and called for a re-measurement before it was enabled,
# which never happened and is still parked. The claimed third reason, that every
# recorded cassette carries `thinking=False`, was false for merge: 37 of the 115
# recorded merge calls carry reasoning (m4 33, pairs 4, none in m7); every
# decompose and verify cassette is off. The default rests on the first two.
DEFAULT_THINKING: frozenset[str] = frozenset()
STRUCTURED_MODES = ("auto", "json_schema", "tool_call", "prompt")
LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1", "[::1]", ""})

# Every local spelling of one machine is one machine. Normalising before the
# hash is the whole reason this is a function and not an inline digest: a
# corpus half-recorded as `127.0.0.1` and half as `localhost` would produce two
# ids for one box, and the endpoint guard would then fire on history instead of
# on a mistake. That is the failure an earlier version already fixed once in the corpus,
# and doing it in the hash means it cannot come back.
ENDPOINT_ALIASES = frozenset({"127.0.0.1", "::1", "[::1]"})
ENDPOINT_ID_CHARS = 12

# Which rule produced the ids this build writes. Stamped into every cassette's
# `meta` so that a reader can tell which rule an id on disk was made under, and
# an absent marker means scheme 1.
#
#   1  sha256(canonical_host(hostname))[:12], or the label. Everything recorded
#      before 2026-09-17. It cannot be migrated to 2: a cassette records the id
#      and never the URL, so there is nothing left to re-hash.
#   2  sha256(endpoint_address(base_url))[:12], or the label — scheme, host,
#      port and path, because a provider that routes deployments by path
#      collapsed every one of them onto a single id under 1.
#
# A label-derived id is identical under both, since the label replaces the
# address rather than being mixed into it.
ENDPOINT_ID_SCHEME = 2
ENDPOINT_ID_SCHEME_HOSTNAME = 1

# How freely the merge may reword its sources, lowest first. At `off` a
# rewording the caller did not ask for cannot happen: the reverse pass would
# otherwise see generated wording and have to judge whether it is invention,
# and at `off` it does not have to. The levels are ordered, and a reader
# should be able to rely on that — everything permitted at one level is
# permitted at every level above it. `high` is the default; see below.
#
# `open` is the fifth and is a different kind of step. The four
# below it differ in how freely the merge may *reword* its sources, and all four
# share one outer bound: the sources are the only thing the merged document may
# state. `open` moves that bound. It keeps the ladder's promise -- everything
# `high` permits is permitted here -- and adds the one thing no level below it
# has, which is why it is named for what it opens rather than for more of the
# same axis.
#
# `sourced` is the sixth and moves the same bound one step further: at `open`
# the model may assert what it knows, and at `sourced` it is expected to go and
# *retrieve* rather than recall. The schema does not move with it -- an
# undeclared factual change is `hallucinated` here exactly as at `open` -- and
# neither does anything else in the record contract. What changes is what the
# model is asked to do before it declares, and whether the run can say it did.
#
# It is the one level with a *precondition*: a backend that cannot reach the
# network cannot retrieve, and a `sourced` run on one would hand the reader
# recalled assertions wearing citations, which is worse than `open` because
# they believe the claims were checked. `retrieval_refusal` is that
# precondition, and it is the reason this level exists as a level rather than
# as more prose in `open`'s fragment.
FIDELITY_LEVELS = ("off", "low", "mid", "high", "open", "sourced")
# Named rather than spelled at each guard. Three modules ask "is this the level
# that needs retrieval", and a string literal in each is three places a rename
# has to reach -- which is the failure `parsing.DERIVES` and `merge.ADDS`
# already refuse for the tables beside them.
SOURCED = "sourced"
assert SOURCED in FIDELITY_LEVELS
# `high`, based on four operator pairs. `off` is the benchmark's strict mode
# and five registrations hold it constant, so it is not going anywhere -- but a
# flagless run is a person merging two documents, and at `off` the tool is a
# diff with a verifier attached rather than a merge tool: it may not choose
# between two wordings of one fact, so the deliverable carries both. That is
# the right instrument for measuring a model and the wrong default for someone
# who wanted one document. Every block passes --fidelity explicitly
# (`run_arm.py:291`), so no registration reads this.
DEFAULT_FIDELITY = "high"

# How thoroughly a merge is checked, which is a different axis from how freely
# it was allowed to be written. `full` runs four model steps: decompose each
# source, verify forward, decompose the merge, verify backward. `coverage`
# runs one call per source that extracts and judges together, and **no reverse
# pass at all** -- so it asks whether source content survived and never asks
# whether the merge asserts anything its sources do not.
#
# That is a real hole and the name says which one. It is not "fast" and it is
# not "cheap": it is the coverage question on its own. The default stays
# `full` because a tool whose headline promise is that the merge invents
# nothing must not stop checking that unless it is asked to.
#
# The nine mechanical checks in `reconcile` run at both depths. They cost no
# model call.
FULL_DEPTH = "full"
COVERAGE_DEPTH = "coverage"
VERIFY_DEPTHS = (FULL_DEPTH, COVERAGE_DEPTH)
DEFAULT_VERIFY_DEPTH = FULL_DEPTH


@dataclass(frozen=True)
class VerifyDepthShape:
    """What one depth asks, what it refuses to ask, and what it costs.

    Data rather than prose, because three surfaces describe this choice -- the
    `--verify-depth` help below, `/api/v1/config`, and the picker the web page
    renders from it -- and a fourth copy of the sentence is how a page ends up
    explaining a depth that has since changed. It is the arrangement the
    fidelity ladder has kept: `FIDELITY_SHAPES`, one copy that the
    `--fidelity` help renders and the page's locale strings are held to. A
    depth is a shape of the pipeline rather than an instruction to a model,
    so it never had a prompt fragment to confuse with, and this is its copy.

    `detects_invention` is a flag and not a sentence on purpose. It is what a
    reader of a finished report has to branch on -- whether a clean result
    means "nothing was invented" or only "nothing was lost" -- and a page that
    decided that by comparing a depth's name against the string `coverage`
    would be carrying the vocabulary it is supposed to be served, and would go
    quietly wrong the day a third depth arrives.

    The two call counts are counted from the pipeline rather than modelled.
    `cli.pipeline` makes one merge call and one call per source at either
    depth, and at `full` three more: the forward verify, the decompose of the
    merged document and the reverse verify. `tests/test_coverage.py` counts
    what a real pipeline sends at both depths and holds it against this table,
    so a change to the pipeline that does not reach here fails rather than
    publishing a stale price.

    **`exact_calls` corrects an earlier claim.** That claim called
    the figure exact at both depths and it is exact at only one.
    `verify.verify_claims` batches at `Settings.verify_batch`, so each of
    `full`'s two verify steps is one call *per batch*: at the HTTP figure of
    25, 60 source claims
    and 50 merged claims is nine calls, not six. The count is therefore a
    floor at `full` and reached only by a merge small enough to fit one batch
    each way -- which every fixture in this repository is, which is why
    measuring it agreed with publishing it. `coverage` has no batching to do:
    one fused call carries a whole source however many claims come back, so
    there the figure is the number.

    A floor is still worth publishing -- it is the number the saving is
    computed from and it cannot overstate what the cheaper depth costs -- but
    it has to be *said* to be one wherever it renders, or a reader takes a
    minimum for a quote.

    **The call count is most of what a long run costs, and not the whole of
    it.** An operator's three-source merge of 6 KB of
    document took 1,585 s over 13 calls -- one merge, four decompose and eight
    verify -- and that was first read as a nearly fixed cost per call. Measured, the
    fixed part is ~26-30 s and a verify call also pays ~1.3-1.5 s a claim, so
    a call's size matters as well as the count. `coverage` is still the larger
    of the two levers here and still the one a reader chooses: it would have
    made that run four calls. The other is `Settings.verify_batch`, which
    needs no decision from anybody. Neither is the biggest lever the run has
    -- `AUTO_EFFORT` is, and it is a property of the backend rather than of
    this table.
    """

    name: str
    explains: str
    detects_invention: bool
    # Calls a `merge` run makes whatever the source count is.
    fixed_calls: int
    # And one more per source document.
    calls_per_source: int
    # Whether that arithmetic is the whole story, or only its lower bound.
    exact_calls: bool


VERIFY_DEPTH_SHAPES = {
    FULL_DEPTH: VerifyDepthShape(
        name="Full",
        explains=(
            "Checks both ways: that everything in your documents made it into "
            "the merge, and that the merge says nothing your documents do not."
        ),
        detects_invention=True,
        fixed_calls=4,
        calls_per_source=1,
        # A floor. Both verify steps batch at `Settings.verify_batch`,
        # which is 25 over HTTP and 100 through a command.
        exact_calls=False,
    ),
    COVERAGE_DEPTH: VerifyDepthShape(
        name="Coverage",
        explains=(
            "Checks only that everything in your documents made it into the "
            "merge. The merge is never read back, so this depth cannot catch "
            "invention: anything the merge made up goes unnoticed. It needs "
            "fewer model calls."
        ),
        detects_invention=False,
        fixed_calls=1,
        calls_per_source=1,
        # One fused call per source, whatever the claim count. Nothing here
        # batches, so this arithmetic is the number rather than its floor.
        exact_calls=True,
    ),
}
# Asserted, not commented. A depth in one of these and not the other is a
# picker with a missing option or a `KeyError` at render time, and both are
# discovered by the operator rather than by this suite.
assert set(VERIFY_DEPTH_SHAPES) == set(VERIFY_DEPTHS)


def merge_model_calls(depth: str, sources: int) -> int:
    """The model calls a merge of `sources` documents makes at this depth, at least.

    The one figure about this choice that can be stated without measuring
    anything, which is why it is the one the page shows. What the cheaper depth
    costs in *detection* is unmeasured (a benchmark ran, its comparator was
    disqualified), and what it saves in *dollars* is not derivable from
    this either: the calls are not the same size, so halving the count does not
    halve the spend and a figure that implied it would be invented. Naming what
    is exact and declining the rest is `pricing.py`'s own rule for costs.

    **A floor at `full` and the number at `coverage`**; the caller has to say
    which, and `VERIFY_DEPTH_SHAPES[depth].exact_calls` is how it finds out.
    `verify_claims` batches claims, 25 a call over HTTP and 100 through a
    command, so `full` spends a call per batch each way and this counts one. Returning a bare integer
    that means different things at the two depths would be a mistake this
    file's prose once made; the flag beside it is what stops the difference
    living in a docstring only.
    """
    shape = VERIFY_DEPTH_SHAPES[depth]
    return shape.fixed_calls + shape.calls_per_source * max(0, int(sources))

# The strictest level is *called* `verbatim` and *spelled* `off` on the wire.
# The operator's ruling: `--fidelity off` reads as "turn fidelity
# checking off" when it means "rewriting off", and it is the setting that
# permits the least. In a tool being published, a flag whose name suggests the
# opposite of what it does is a defect in its own right.
#
# Why the wire name did not move with it. `off` is in 151 recorded merge
# cassettes, in every graded run record (withheld with the paper), in the fidelity prompt fragments
# whose text is hashed into the cassette key, in five benchmark registrations
# and in the operator's own scripts. Renaming the value would orphan all of it
# for a cosmetic gain. So `FIDELITY_LEVELS` is untouched and the rename lives
# in two mappings: one for what a person may type, one for what a person is
# shown. `verbatim` is an alias that will not be withdrawn -- there is no
# deprecation window here, because the two spellings are the same run.
#
# The invariants below are asserted rather than commented: an alias colliding
# with a level, or a display name with no way back to a level, would make the
# two directions disagree and the disagreement would surface as an unreadable
# report rather than as an error.
FIDELITY_ALIASES = {"verbatim": "off"}
FIDELITY_NAMES = {"off": "verbatim"}
# Every level under the name a person reads, in `FIDELITY_LEVELS` order. This
# is what help text and reports list; `FIDELITY_LEVELS` stays the wire order.
FIDELITY_PUBLISHED = tuple(FIDELITY_NAMES.get(level, level) for level in FIDELITY_LEVELS)
# What `--fidelity` accepts: every published name, then every wire name that
# is no longer one of them. The old spelling is last so `--help` reads as
# "these are the levels, and this also works".
FIDELITY_CHOICES = FIDELITY_PUBLISHED + tuple(
    level for level in FIDELITY_LEVELS if level not in FIDELITY_PUBLISHED
)

assert set(FIDELITY_ALIASES.values()) <= set(FIDELITY_LEVELS)
assert not set(FIDELITY_ALIASES) & set(FIDELITY_LEVELS)
assert set(FIDELITY_NAMES) <= set(FIDELITY_LEVELS)
# Both directions of one relation, so neither can be edited alone.
assert {name: level for level, name in FIDELITY_NAMES.items()} == FIDELITY_ALIASES
assert len(set(FIDELITY_CHOICES)) == len(FIDELITY_CHOICES)
assert FIDELITY_PUBLISHED[0] == "verbatim" and DEFAULT_FIDELITY == "high"


@dataclass(frozen=True)
class FidelityShape:
    """What one level does for a reader, in a reader's words. A row per level.

    **Held apart from the prompt fragment, and that is the whole point.** The
    page used to render `prompts/fidelity/<level>.merge.md`'s opening paragraph
    as the level's description, which put text addressed to the *model* in
    front of a person: *"you are expected to look a fact up"*, *"you have been
    given a web tool for this run"*. The operator's report was exactly that --
    *"those descriptions obviously need to be written for the end-user not the
    model"* -- and it is structural rather than a wording slip. A prompt tells
    a model what it may do; a picker has to tell a person what they are
    choosing and what it costs them. One string cannot be both.

    The fragment keeps its job unchanged. Rewriting prompts into UI copy would
    weaken the instruction the model needs and would re-key every cassette the
    fragment is hashed into; these are new strings beside it, not moved ones.

    Three fields because a person deciding needs three answers, and the third
    is the one the old arrangement lost entirely:

    `summary` -- what the merge may do, in plain terms rather than in the
    prompt's vocabulary. Short enough for a line under a control.

    `buys` -- why anybody would pick this level.

    `costs` -- what the tool can no longer catch, or what becomes the reader's
    own job. Someone choosing `open` or `sourced` is giving up a guarantee and
    has to be told which one.

    Second person about the *reader* is fine and is used. Second person about
    the model is the defect.
    """

    summary: str
    buys: str
    costs: str

    @property
    def explains(self) -> str:
        """The three sentences as one paragraph, for a caller with one slot."""
        return " ".join((self.summary, self.buys, self.costs))


FIDELITY_SHAPES = {
    "off": FidelityShape(
        summary=(
            "Builds the merge only from sentences your documents already "
            "contain, copied exactly. It chooses which ones to keep and in "
            "what order."
        ),
        buys=(
            "Nothing can be reworded into a different meaning: every sentence "
            "is one you already had."
        ),
        costs=(
            "Typos stay, and where two documents disagree, both statements "
            "stay. The result can read like a set of quotes rather than one "
            "text."
        ),
    ),
    "low": FidelityShape(
        summary=(
            "Also fixes spelling, grammar slips and punctuation. Each "
            "sentence stays recognisably the original."
        ),
        buys=(
            "Reads more cleanly, and no statement changes what it says."
        ),
        costs=(
            "A corrected sentence is worth a glance against its original. "
            "Where two documents disagree, both statements still stay."
        ),
    ),
    "mid": FidelityShape(
        summary=(
            "Also rewrites single sentences for clarity, and may fold a short "
            "detail into the sentence it belongs to."
        ),
        buys=(
            "Clearer sentences, with small details placed where they belong "
            "instead of standing alone."
        ),
        costs=(
            "Every folded detail is listed in the report, but the merge now "
            "decides where a detail belongs. Where two documents disagree, "
            "both statements still stay."
        ),
    ),
    "high": FidelityShape(
        summary=(
            "Rewrites freely, like a careful editor: states a repeated point "
            "once, joins facts from both documents into one statement, and "
            "settles a disagreement by choosing one value."
        ),
        buys=(
            "One clear, readable document. The setting most people want."
        ),
        costs=(
            "Where two documents disagree, the merge picks one value and says "
            "which and why, but the choice is its judgement, so check it. "
            "Numbers, links, code and version strings are copied exactly at "
            "every level."
        ),
    ),
    "open": FidelityShape(
        summary=(
            "Everything high does, and the merge may also correct a fact from "
            "what the model knows, or give a range that covers two figures "
            "your documents disagree about."
        ),
        buys=(
            "A document that is wrong about a well-known fact can be fixed "
            "rather than copied, and every correction is listed."
        ),
        costs=(
            "The result can now say things your documents do not. This tool "
            "checks only against your documents, so a correction rests on the "
            "model's word, and reviewing it is your job. A correction the "
            "merge does not list is reported as invented."
        ),
    ),
    "sourced": FidelityShape(
        summary=(
            "Like open, but the model is asked to look facts up on the web "
            "instead of recalling them. The report says whether it did."
        ),
        buys=(
            "A correction backed by a published source rather than memory: "
            "the difference between a confident wrong answer and a right one."
        ),
        costs=(
            "The model may search the web, so text from your documents can "
            "leave this machine in a search or a page request. What it finds "
            "is still the model's claim: LLossless checks no source. Where "
            "the model cannot use the web, this level is refused rather than "
            "answered from memory. Claude Code gets web tools only at this "
            "level, unless your own command grants them, and never loads "
            "your personal CLAUDE.md, skills, plugins or MCP servers."
        ),
    ),
}

# Asserted, not commented, the way `VERIFY_DEPTH_SHAPES` is: a level with no
# description is a picker row with a blank under it or a `KeyError` at render
# time, and both are discovered by the operator rather than by this suite.
assert set(FIDELITY_SHAPES) == set(FIDELITY_LEVELS)


def canonical_fidelity(value: str) -> str:
    """The wire spelling of a level, whichever of its names the caller used.

    Deliberately not a normaliser: it does not strip, lower-case or validate.
    Callers that read a human's input do that themselves and then say what is
    wrong in their own vocabulary, and a function that quietly accepted `OFF `
    here would widen what every one of them takes. An unknown value is returned
    unchanged so the caller's own membership test still refuses it.
    """
    return FIDELITY_ALIASES.get(value, value)


def fidelity_name(value: str) -> str:
    """The published spelling of a level: what a person reads, in help or a report.

    The inverse of `canonical_fidelity` and total on the same inputs, so a
    report can render whatever the run recorded without knowing which spelling
    it was given.
    """
    return FIDELITY_NAMES.get(canonical_fidelity(value), value)


def _argv(command: str) -> list[str]:
    """A command line split the way `backend.post_json` splits it, or nothing.

    Never raises. An unbalanced quote is a command that will fail on its first
    call with `backend`'s own message; a retrieval guard that raised here would
    report a quoting mistake as a retrieval problem, which sends the operator
    to the wrong half of their configuration.
    """
    try:
        return shlex.split(command or "")
    except ValueError:
        return []


def granted_web_tools(command: str, *, raw: bool = False) -> tuple[str, ...]:
    """Which known web tools this command line already permits. Read, not assumed.

    The operator's own grant, read back off the argv they wrote -- the same
    direction `web/commands._row` checks in, and the reason it checks: a field
    that says a tool is permitted and an argv that does not pass it is a
    permission nobody gave.

    Both spellings, `=` or a space, and both separators the CLI documents, comma
    or space; order is the table's and duplicates collapse. A tool the argv's
    own `--tools` leaves out is not granted, whatever the allowlist says;
    `raw` reads the allowlist alone, which is what "already granted" asks.
    """
    argv = _argv(command)
    named: set[str] = set()
    for index, item in enumerate(argv):
        if item == ALLOW_TOOLS_FLAG:
            values = argv[index + 1:]
        elif item.startswith(f"{ALLOW_TOOLS_FLAG}="):
            values = [item.split("=", 1)[1]]
        else:
            continue
        # Up to the next flag: `--allowed-tools <tools...>` takes a list, and a
        # reader that took only the first word would report half a grant.
        for value in values:
            if value.startswith("-"):
                break
            named.update(part.strip() for part in value.split(","))
    found = tuple(tool for tool in WEB_TOOLS if tool in named)
    return found if raw else _available(command, found)


def carries_result_args(argv: list[str]) -> bool:
    """Whether this argv asks its command for a result envelope.

    Both spellings a shell accepts, because an operator who writes
    `--output-format=json` has written the same command and a check that only
    knew the separated form would refuse it -- a refusal on a working command
    is how an operator learns to work around a rule rather than with it.

    `stream-json` is not this envelope and is answered as `raw`: it is a
    sequence of objects, `backend`'s `RESULT` reader takes one, and treating it
    as the same thing is the confusion this check was written to stop. An
    operator who passes it and declares `result` is told the pair disagrees,
    which is true.

    Takes a split argv rather than a command line, because its first caller
    -- `web/commands._row` -- already holds one it built itself, and splitting
    a string it had just joined would be a second chance to disagree.
    """
    for index, item in enumerate(argv):
        if item == RESULT_FORMAT_FLAG:
            if argv[index + 1:index + 2] == [RESULT_FORMAT_VALUE]:
                return True
        elif item == f"{RESULT_FORMAT_FLAG}={RESULT_FORMAT_VALUE}":
            return True
    return False


def auto_granted_tools(command: str) -> tuple[str, ...]:
    """What this build would add to this command line for a `sourced` run.

    Empty for an HTTP endpoint -- there is no command to add a flag to -- and
    empty for a program `AUTO_GRANT` does not name, which is the honest answer
    about a wrapper script this build has never seen: it cannot know which flag
    that script takes, and appending one it does not take would break a working
    route rather than widen it.

    Empty, too, where the operator already granted something, and narrowed to
    what their own `--tools` makes available: their argv is theirs.
    """
    argv = _argv(command)
    if not argv or granted_web_tools(command, raw=True):
        return ()
    return _available(command, AUTO_GRANT.get(os.path.basename(argv[0]), ()))


def retrieval_tools(command: str) -> tuple[str, ...]:
    """Every web tool a `sourced` run through this command would be permitted.

    The operator's own grant where there is one, otherwise the automatic one.
    Empty means this backend cannot retrieve, and that is what `sourced`
    refuses on -- the whole of the level's safety property in one predicate.
    """
    return granted_web_tools(command) or auto_granted_tools(command)


def command_with_retrieval(command: str) -> str:
    """This command line with the automatic grant on it. Idempotent.

    The one writer. Called from `resolve` once the level is known, so both the
    command line and the web server reach it through the same function and a
    run cannot be granted retrieval on one path and not the other.

    Idempotent by construction: `auto_granted_tools` answers nothing once a
    grant is readable off the argv, so applying this twice appends once.
    """
    granted = auto_granted_tools(command)
    if not granted:
        return command
    return shlex.join([*_argv(command), ALLOW_TOOLS_FLAG, ",".join(granted)])


def stated_effort(command: str) -> str:
    """The effort level this command line already names, or "". Read, not assumed.

    `granted_web_tools`' shape one table over, and for its reason: what the
    operator wrote is read back off the argv they wrote, so a choice they made
    is never overwritten by one this build would have made. Both separators a
    shell accepts, because `--effort=low` and `--effort low` are one command.

    The last spelling wins, which is what the program itself does with a
    repeated flag -- a reader of this who found the first would report a level
    the run will not be asked for.
    """
    argv = _argv(command)
    found = ""
    for index, item in enumerate(argv):
        if item == EFFORT_FLAG:
            value = argv[index + 1] if index + 1 < len(argv) else ""
        elif item.startswith(f"{EFFORT_FLAG}="):
            value = item.split("=", 1)[1]
        else:
            continue
        # A value that is itself a flag is the operator having written
        # `--effort` with nothing after it. That is their command's problem to
        # report, not a level to record.
        if value and not value.startswith("-"):
            found = value
    return found


def stated_model(command: str) -> str:
    """The model this command line names on `--model`, or "". Read, not assumed.

    `stated_effort`'s reader for the flag beside it: both spellings, and the
    last one wins, as the program does with a repeated flag. `AUTO_EFFORT_BY_MODEL`
    is keyed by what this returns, so a route that names no model gets the
    program's row rather than a level measured on some other model.
    """
    argv = _argv(command)
    found = ""
    for index, item in enumerate(argv):
        if item == MODEL_FLAG:
            value = argv[index + 1] if index + 1 < len(argv) else ""
        elif item.startswith(f"{MODEL_FLAG}="):
            value = item.split("=", 1)[1]
        else:
            continue
        if value and not value.startswith("-"):
            found = value
    return found


def auto_effort(command: str, role: str) -> str:
    """What this build would ask this role's calls to spend on thinking, or "".

    `auto_granted_tools`' three refusals, unchanged and for the same reasons:
    empty for an HTTP endpoint, because there is no command to put a flag on;
    empty for a program `AUTO_EFFORT` does not name, because appending a flag
    to a wrapper script whose arguments this build has never read breaks a
    working route rather than speeding it up; and empty where the operator
    already stated a level, because their argv is theirs.

    A fourth, added later: empty for a model `is_single_level_model`
    names, on every role -- not only the merge `AUTO_EFFORT_BY_MODEL` used to
    override. Haiku's decompose and verify calls read the program's own row
    exactly as every other model's do, and that row is a level this model
    cannot carry either; the table never measured a per-model exception for
    those two roles because there was never meant to be one to reach.

    Set per role. The table's own comment holds the measurement; what
    this function adds is that the role is asked for rather than assumed, so a
    caller cannot get an answer about "the run" that is true of one call of six.

    Set per model too: the program's row, with `AUTO_EFFORT_BY_MODEL`'s row
    for the argv's own `--model` alias over it.
    """
    if role not in ROLES:
        raise ConfigError(
            f"unknown role {role!r}; expected one of {', '.join(ROLES)}")
    argv = _argv(command)
    if not argv or stated_effort(command):
        return ""
    program = os.path.basename(argv[0])
    if is_single_level_model(stated_model(command)):
        return ""
    by_model = AUTO_EFFORT_BY_MODEL.get(program, {}).get(stated_model(command), {})
    return by_model.get(role) or AUTO_EFFORT.get(program, {}).get(role, "")


def effort_of(command: str, role: str,
              chosen: dict[str, str] | None = None) -> str:
    """The level this role's calls will really be asked for, or "".

    **The whole precedence, in one function**, so that no caller can assemble a
    different one. Highest first:

    1. a level in the operator's own argv, which wins for every role and is
       never written over -- the same rule as `AUTO_GRANT`'s, unchanged;
    2. `chosen`, what they said on `--effort` or in `LLOSSLESS_EFFORT*`;
    3. `AUTO_EFFORT`, what this build would pick for them.

    `chosen` is gated on the program being one this build has read, exactly as
    the automatic level is. An operator who names a level for a wrapper script
    nobody here has seen is asking this build to guess that script's flags,
    and appending one it does not take breaks a working route rather than
    widening it; their own argv is the surface that always works. The drop is
    not silent -- `Settings.effort_ignored` names those roles and the
    provenance block publishes them, in the JSON and in the rendered
    `Decoding` row. The banner does not carry it.

    `chosen` is gated the same way on a single-level model: a
    stray `LLOSSLESS_EFFORT*` or a web request naming one for a Haiku route is
    not honoured either, and is reported through the same `effort_ignored`
    mechanism rather than reaching the argv. Rule 1 above still stands --
    `written` is the operator's own `--effort` on their own command line, and
    this function has never overwritten that for any model.

    Empty means the program's own default applies -- an HTTP endpoint, an
    unknown program, a table with no row for this role, or a single-level
    model -- which is a different statement from any named level and is
    reported as its own.
    """
    if role not in ROLES:
        raise ConfigError(
            f"unknown role {role!r}; expected one of {', '.join(ROLES)}")
    argv = _argv(command)
    if not argv:
        return ""
    written = stated_effort(command)
    if written:
        return written
    if os.path.basename(argv[0]) not in AUTO_EFFORT:
        return ""
    if is_single_level_model(stated_model(command)):
        return ""
    return (chosen or {}).get(role, "") or auto_effort(command, role)


def command_with_effort(command: str, role: str,
                        chosen: dict[str, str] | None = None) -> str:
    """This command line with this role's effort level on it. Idempotent.

    `command_with_retrieval`'s sibling and its one writer rule, moved one layer
    in: the append is per role, so it happens where the role is known -- at the
    call, through `Settings.command_for` -- rather than once in `resolve`.
    Both ways in still reach this one function, so a role cannot be paced on
    the command line and unpaced on the web server.

    Idempotent by construction, and by the same mechanism as the grant: a level
    readable off the argv is the operator's by rule 1 above, so applying this
    twice appends once and the second application is a no-op whatever the role.
    """
    if stated_effort(command):
        return command
    level = effort_of(command, role, chosen)
    if not level:
        return command
    return shlex.join([*_argv(command), EFFORT_FLAG, level])


def retrieval_refusal(fidelity: str, command: str) -> str | None:
    """Why this backend may not answer at `sourced`, or None. The safety property.

    **Selecting `sourced` on a backend that cannot retrieve refuses rather than
    behaving like `open`.** A user who picks the level that says "go and
    check" and receives recalled assertions wearing citations is worse off than
    one who picked `open`, because they believe the claims were verified -- and
    the two runs are not distinguishable from the report. The measurement is
    the same pair, the same model and the same level with one variable: without
    the tool the merge asserted the licence was 2-clause BSD, with it MIT, and
    both runs cited one source whose strings were near-identical.

    Says what is missing and what to do about it, in the shape
    `web/commands._row`'s no-model refusal takes: the thing that is absent, an
    example of the fix, and why the absence is not something this build will
    guess past.
    """
    if canonical_fidelity(fidelity) != SOURCED:
        return None
    if retrieval_tools(command) or tools_withhold_the_grant(command):
        return _grant_refusal(command)  # withheld? can it tell?
    if not (command or "").strip():
        return (
            f"--fidelity {SOURCED} asks the model to look things up before it "
            f"asserts them, and an HTTP endpoint has no way to be granted a "
            f"web tool by this build -- so the run would answer from what the "
            f"model already knows and label it retrieved, which is the one "
            f"outcome this level exists to prevent. Use --fidelity open for a "
            f"recalled answer, or answer through a program that takes "
            f"{ALLOW_TOOLS_FLAG} (--answer-with, or a command route on the "
            f"web server).")
    program = os.path.basename((_argv(command) or [""])[0]) or "that program"
    return (
        f"--fidelity {SOURCED} needs a backend that can retrieve, and this run "
        f"answers through {program!r}, which this build does not know how to "
        f"grant a web tool to. It grants {', '.join(sorted(AUTO_GRANT))} "
        f"automatically and nothing else, because appending a flag to a "
        f"program whose flags it has not read breaks a working command rather "
        f"than widening it. Put `{ALLOW_TOOLS_FLAG} {','.join(WEB_TOOLS)}` in the "
        f"command yourself if {program!r} takes it, or use --fidelity open.")

def envelope_refusal(envelope: str, command: str) -> str | None:
    """Why this command and this envelope cannot both be right, or None.

    The rule `web/commands._row` has held on a route, applied to the
    other way in. A command line reaches a command backend through
    `--answer-with` or `LLOSSLESS_COMMAND` and neither was checked against
    `LLOSSLESS_COMMAND_ENVELOPE`, so a command carrying
    `--output-format json` with the envelope left at its `raw` default handed
    the merge the result envelope to parse *as* the answer: it failed the
    schema, spent every repair attempt on it, and errored -- once, measured,
    against a real subscription.

    Both directions, for `_row`'s reason: a grant the argv does not carry is a
    permission nobody gave, which is one-sided, but an envelope is a parser
    selection and picking the wrong one is a defect whichever way the pair
    disagrees.

    Empty command means an HTTP endpoint, which has no argv to disagree with
    and no envelope to read. The variable is then inert rather than wrong.

    Names the disagreement and the fix, in the shape `retrieval_refusal` above
    takes: the operator has two strings in front of them and needs to be told
    which one to change, not how the reader works.
    """
    if not (command or "").strip():
        return None
    carries = carries_result_args(_argv(command))
    both = " ".join(RESULT_ARGS)
    if envelope == ENVELOPE_RESULT and not carries:
        return (
            f"LLOSSLESS_COMMAND_ENVELOPE={ENVELOPE_RESULT} says this command "
            f"answers with a JSON result envelope, and the command does not "
            f"carry `{both}` -- so its whole standard output is the answer and "
            f"there is no envelope to unwrap. The variable records how the "
            f"command answers; it does not change the command. Add `{both}` to "
            f"the command, or set LLOSSLESS_COMMAND_ENVELOPE={ENVELOPE_RAW}.")
    if envelope == ENVELOPE_RAW and carries:
        return (
            f"this command carries `{both}`, so it answers with a JSON result "
            f"envelope, and LLOSSLESS_COMMAND_ENVELOPE is {ENVELOPE_RAW} -- "
            f"which reads that envelope as the answer. Every call would hand "
            f"the schema an object the model was never asked for and spend the "
            f"repair attempts failing it. Set "
            f"LLOSSLESS_COMMAND_ENVELOPE={ENVELOPE_RESULT}, or drop "
            f"`{RESULT_FORMAT_FLAG}` from the command.")
    return None


# Which title the merged document takes. Unordered, unlike the fidelity levels:
# these are three policies, not three amounts of one thing. `keep-base` takes the
# base document's title; `choose-best` lets the model pick among the titles the
# sources already carry. Neither ever licenses writing a new one — that rule is
# in `merge.md` itself and holds at every level under both policies.
# `synthesise` permits a written title and is the only policy that does.
# A title is a claim, and a claim cannot be graded by the
# words it is made of -- "A motorbike is more stable than a quad" is built
# entirely from source vocabulary and inverts what the sources say. So a
# written title is verified semantically, against the sources, by the same
# machinery that verifies a merged claim. The two existing policies are
# unchanged and need no such call: they permit only a byte-identical copy.
TITLE_POLICIES = ("keep-base", "choose-best", "synthesise")
DEFAULT_TITLE_POLICY = "synthesise"

# One clause per policy, and `--title-policy`'s help is built from this rather
# than written beside it. It read "default synthesise: the base
# document's" -- the default's name interpolated from the constant, the
# description left behind from when `keep-base` was the default, and the one
# policy that may *write* a title not described at all. The flag's own help is
# where an operator learns what they are turning on, and it described the
# opposite of what they were getting.
#
# The shape `--verify-depth` already uses one screen up: a table keyed by the
# value, joined into the help, so a policy cannot be named without its own
# clause being the one that follows it. The prompts under `prompts/title/` are
# the full rule and what `web/api.py`'s `title_policies` serves; these are the
# one-line form a terminal can carry.
TITLE_POLICY_EXPLAINS = {
    "keep-base": "the base document's title, and the first non-empty one in "
                 "document order if the base has none",
    "choose-best": "whichever source title names the subject most clearly, "
                   "never a new one",
    "synthesise": "the merge may write a title, and a written one is verified "
                  "against the sources as a claim",
}
assert set(TITLE_POLICY_EXPLAINS) == set(TITLE_POLICIES)

# How much of the sources a merge may declare it dropped before the declared
# loss is itself a finding. A fraction of the source segments, never a
# percentage: `--loss-budget 5` meaning 500% is a worse failure than a rejected
# input, because it turns the check off while reading like a tightening of it.
# The rule this feeds is written once, in `reconcile.over_budget`, and the
# value travels to it as an argument -- a second copy of the arithmetic, or a
# default baked into that signature, is the same hidden global one layer down.
# Lowered from 0.05 on 2026-09-18. Measured over the
# 36-cell matrix: at 5% only `claude-haiku-4-5` ever fired, and
# `claude-sonnet-5` dropping both `{internal-notes}` markers on
# `index_429` -- 2 of 63 segments, 3.17% -- passed under it. 3% catches
# that and still clears every frontier cell; 1% would flag a single
# legitimate drop by `gpt-5.6-terra` on the same pair, so the margin sits
# between them rather than at either end.
DEFAULT_DECLARED_LOSS_BUDGET = 0.03

# Whether the field order a schema declares is a requirement or a preference.
# `schema` is the contract this project was built on: the model names its
# verdict before it writes the rationale, its disposition before the
# replacement, and a response that argues first has committed to nothing.
# `any` accepts a response that carries every required field, all valid, in
# some other order -- and nothing else; a missing field is still a missing
# field. It exists because a model's key order is a property of its serializer
# rather than of its answer: deepseek-r1:70b emits alphabetically, no tier
# constrains order on the endpoints measured, and refusing it means refusing
# the model. What the relaxation costs is unmeasured, which is why it is a
# switch that has to be asked for rather than a default that quietly moves.
#
# Strictest first, and the order is load-bearing: `replay_field_order` reads
# "more permissive" off a value's position in this tuple.
FIELD_ORDERS = ("schema", "any")
DEFAULT_FIELD_ORDER = "schema"


def replay_field_order(recorded: str, requested: str) -> str:
    """The order a replayed answer is read under: never stricter than its recording.

    `recorded` is what the recording run read the answer under, from the
    cassette (`Cassette.field_order`); `requested` is this run's setting. The
    more permissive of the two wins, and the two halves of that rule have
    different reasons.

    *A replay may not read a recording more strictly than it was read when
    made.* A run recorded under `any` accepted an answer whose keys arrived in
    another order, on the first attempt, and asked for nothing more. Read under
    `schema` the same bytes are an order fault: the client either stops on it
    (`SchemaFailure`) or, where the answer had a second fault, asks for a
    repair the recording never made (a replay miss). Neither outcome says
    anything about the model; both say only that the replay did not reproduce
    the recording's conditions. vLLM's guided decoding emits keys
    alphabetically, so this is every recording made against it.

    *A replay may read a recording more permissively than it was made.* Asking
    `--field-order any` of a `schema` recording is a question the recorded
    bytes can answer, and it is what every replay did before recordings carried
    their order -- including the unstamped `any` recordings of the deepseek-r1
    arms, which replay today only because the flag is passed. A rule where the
    recording always won would read those as `schema` and break them.

    A live call and a cache hit never come through here: they are read under
    `requested`, so a live run's behaviour does not move.
    """
    return max(recorded, requested, key=FIELD_ORDERS.index)

# The served context window, when the operator states it instead of the tool
# measuring it. `None` is the default and is not a number: unset means "ask the
# endpoint", which is what every local run does and what the whole of
# `window.py` exists to do properly.
#
# **This is not a default window and must never become one.** `served_window`
# refuses to invent a figure because the invented figure is the hard-coded
# number an earlier version removed, and that refusal is unchanged. What this
# adds is the one other thing that can be true about an endpoint the tool
# cannot interrogate: a person who knows what it serves, saying so. A stated
# window therefore travels as its own `Window.source` and its own
# `window_mechanism`, all the way to the report's Provenance block, because a
# run guarded against a number an operator typed is a different claim from one
# guarded against a number the server confirmed.
DEFAULT_WINDOW: int | None = None


def canonical_host(host: str) -> str:
    """One spelling per machine, before anything is derived from it."""
    return "localhost" if host in ENDPOINT_ALIASES else host


def endpoint_address(base_url: str) -> str:
    """One spelling for the deployment a URL names: scheme, host, port, path.

    This is the string `endpoint_id` hashes, and it is never written down. It
    exists as its own function because *what* identifies a deployment is a
    judgement, not a formatting detail, and it was wrong: it was the hostname
    alone until this was fixed, and a provider that routes deployments by **path**
    — which is what serverless endpoints do — collapsed every one of them onto
    one id. Eleven runs that wrote a report carry one id between
    them, across two different boxes.

    Four components, and each is here because two endpoints can differ by it
    alone:

    * **host**, canonicalised, so one machine spelled two ways is one id.
    * **port**, defaulted from the scheme rather than left absent, because two
      ollamas on one box are two deployments and `:11434` against nothing is a
      difference in spelling rather than in address.
    * **path**, which is why the deployment id lives here on
      the topology this project actually runs against.
    * **scheme**, because it decides the default port and because plain and TLS
      on one host:port are two ways in, not one.

    No query and no userinfo. A query string can carry a token somebody pasted
    and userinfo is a credential outright; neither identifies a deployment, and
    hashing them would put a secret through a function whose output gets
    committed.

    A string with no hostname in it — empty, or something that never parsed as a
    URL — returns empty, and `endpoint_id` turns that into an unrecorded
    endpoint rather than a hash of nonsense.
    """
    parts = urlsplit(base_url.strip().rstrip("/"))
    host = canonical_host(parts.hostname or "")
    if not host:
        return ""
    try:
        explicit = parts.port
    except ValueError:  # a malformed port; the request itself will say so
        explicit = None
    port = explicit or (443 if parts.scheme == "https" else 80)
    return f"{parts.scheme or 'http'}://{host}:{port}{parts.path}"


def endpoint_id(base_url: str, label: str = "") -> str:
    """A stable, opaque label for the deployment that answered.

    A cassette is committed test data in a public repository, and the operator's
    endpoint is not the repository's to publish. What the corpus needs of the
    endpoint is a census — `Store.endpoints()` tallies
    which boxes answered a directory, and a hash carries that without carrying
    an address.

    **The address is `endpoint_address(base_url)`, not the hostname** (scheme 2).
    The argument is a base URL and this hashes what it resolves to;
    handing this a bare hostname gets an empty id, because a bare hostname is
    not an endpoint. Ids recorded under scheme 1 stay as they are and cannot be
    recomputed — see `ENDPOINT_ID_SCHEME` and `legacy_endpoint_id`.

    Empty stays empty: an unrecorded endpoint is a different thing from a
    recorded one, and hashing the empty string would give it a plausible-looking
    identity it has not earned.

    `label` is the operator naming a *deployment* rather than letting the address
    name it, and when set it replaces the address as the thing hashed — so a
    labelled id is the same under both schemes. It exists because a rented
    endpoint's address is ephemeral: restart the pod and both host and port
    change, so a run long enough to span a restart would stamp two ids into one
    directory, splitting one deployment's tally into two entries that both look
    real. Naming the deployment once keeps the census coherent across a restart
    the address itself cannot survive — it was never load-bearing for what a
    recording proves, only for counting it correctly. Scheme 2 narrows what the
    label is *needed* for rather than replacing it: a serverless deployment's
    path id survives the restart that moves its host.

    The label is opaque and operator-chosen; nothing derives meaning from it and
    only its digest is ever written down.
    """
    if label:
        return hashlib.sha256(label.encode("utf-8")).hexdigest()[:ENDPOINT_ID_CHARS]
    address = endpoint_address(base_url)
    if not address:
        return ""
    return hashlib.sha256(address.encode("utf-8")).hexdigest()[:ENDPOINT_ID_CHARS]


def legacy_endpoint_id(host: str) -> str:
    """Scheme 1: `sha256(canonical_host(host))[:12]`. Read-only history.

    Every id in the committed corpus is one of these, and none of them can be
    turned into a scheme 2 id: a cassette records the id and never the URL, so
    there is nothing left to re-hash. This is kept for the
    two callers that legitimately still speak scheme 1 — `Cassette.from_file`,
    resolving the `endpoint_host` field that older local caches still carry, and
    `tests/migrate_endpoint_id.py`, a one-pass migration already applied, whose
    output is on disk and must keep reproducing.

    Not for new recordings. `endpoint_id` is what a run stamps.
    """
    if not host:
        return ""
    digest = hashlib.sha256(canonical_host(host).encode("utf-8")).hexdigest()
    return digest[:ENDPOINT_ID_CHARS]


class ConfigError(RuntimeError):
    """Configuration is wrong or incomplete. Always fatal, never retried."""


def with_api_path(base_url: str) -> str:
    """An OpenAI-compatible base URL, with the `/v1` supplied when it is absent.

    The endpoint an operator is handed is a host and nothing else: a hosted
    runner's proxy gives out a bare `https://<host>` with no path, and ollama's
    own README says `http://localhost:11434`. The OpenAI-compatible routes live
    one path segment below that, so pointing this tool at what it was given
    produces `HTTP 404 ... 404 page not found` -- an error naming neither the
    missing segment nor the fact that the server is up and answering. Supplying
    it is not a guess: no server serves an OpenAI-compatible API at its root, so
    a base URL with no path at all cannot have been meant as one.

    Only when there is no path. A base URL that already carries one is a
    deployment behind a prefix, and appending to it would rewrite an address the
    operator chose deliberately into one nothing serves.
    """
    url = base_url.strip().rstrip("/")
    return url if urlsplit(url).path else url + "/v1"


# Where `Settings.api_key` reads a key value from, for the calling thread.
#
# `None` means `os.environ`, which is what a CLI run, a test and every recorded
# cassette use, so an unset variable is the behaviour this module has always
# had. A web server handling one user's job sets it to that user's credentials
# for the duration of the job and resets it afterwards.
#
# **A `ContextVar` rather than a field, an argument or a global.** The rule this
# preserves is `Settings.api_key`'s own: no key value on anything `repr` or
# `asdict` reaches. A field would put credentials on a frozen
# dataclass that the provenance block serialises. A plain module global would
# leak one job's key into the job running beside it, because `JobStore` runs
# work on threads. A `ContextVar` is read by the thread that set it and by no
# other, and it is on no object anything dumps.
#
# It holds a mapping rather than a callable so that a plain `dict` is a valid
# source, and so the swap is exactly `os.environ.get` with a different mapping
# behind it -- nothing downstream changes shape.
_KEY_SOURCE: contextvars.ContextVar = contextvars.ContextVar(
    "llossless_key_source", default=None)


@contextlib.contextmanager
def keys_for_this_run(source):
    """Read keys from `source` instead of the environment, on this thread only.

    `source` is anything with `.get(name)` -- a `dict` of variable name to key
    value is the expected case. The names are the ones `api_key_env_for`
    returns, so a caller supplies values for the same variables the operator
    would have exported, and nothing else in the configuration changes.

    Restored on the way out whether the body raised or returned, and restored
    with the token rather than by setting `None`, because a nested call must
    put back what it found rather than what it assumes was there.

    **This is the seam multi-tenancy needs and the reason it is cheap.** The
    single-tenant constraint was never the rule about serialisation; it was
    that `os.environ` is per-process, so two concurrent jobs cannot hold two
    users' keys. Swapping the source per thread removes that without touching
    the rule, so `Settings` still carries only variable *names*.
    """
    token = _KEY_SOURCE.set(source)
    try:
        yield
    finally:
        _KEY_SOURCE.reset(token)


@dataclass(frozen=True)
class Settings:
    """Everything resolved. Safe to log in full — it holds no secret.

    `api_key_env` names the variable the key is read from; the key itself is
    fetched at send time by Settings.api_key() and is deliberately not a field,
    so that no dataclass repr, asdict, or JSON dump can ever carry it.
    """

    base_url: str = DEFAULT_BASE_URL
    endpoint_label: str = ""
    models: dict[str, str] = field(default_factory=dict)
    api_key_env: str = DEFAULT_KEY_ENV
    # Per-role overrides for the two things that make an endpoint an endpoint.
    # Empty is the normal case and means "every role goes to `base_url`".
    #
    # This is what "the best model for the best price" needs that `models`
    # alone could not give: `model_for` has resolved a model per role from the
    # start, but every role shared one host, so a frontier merge beside a local
    # decompose was unreachable however the models were set.
    #
    # Endpoints hold URLs; keys hold *environment variable names*, never keys,
    # for the reason the class docstring gives about `api_key()`.
    endpoints: dict[str, str] = field(default_factory=dict)
    api_key_envs: dict[str, str] = field(default_factory=dict)
    # And the window, because a per-role endpoint implies one. Two endpoints
    # serve two context windows -- a 27B on a rented card and an 8B on the
    # operator's own are not the same number -- and a single figure applied to
    # both is either a refusal on the larger or an overrun on the smaller.
    windows: dict[str, int] = field(default_factory=dict)
    structured: str = "auto"
    pinned: bool = False
    fidelity: str = DEFAULT_FIDELITY
    verify_depth: str = DEFAULT_VERIFY_DEPTH
    title_policy: str = DEFAULT_TITLE_POLICY
    declared_loss_budget: float = DEFAULT_DECLARED_LOSS_BUDGET
    field_order: str = DEFAULT_FIELD_ORDER
    thinking: frozenset[str] = DEFAULT_THINKING
    # How hard the operator asked each role to think, role -> level.
    # `thinking` one line up is the same axis at one bit of resolution, and
    # this is the shape settled on for every other per-role setting: a map
    # the environment and the flag both write into, never a parsed string.
    #
    # Empty is "no opinion", and `AUTO_EFFORT` answers. A level in here is the
    # operator's and beats the table; a level in their own command beats both,
    # which is `effort_of`'s rule and not this field's.
    effort: dict[str, str] = field(default_factory=dict)
    # The part of `effort` a web request chose, role -> level. Set by
    # `web.jobs.web_settings` alone, as `window_declared_by` is, and read by
    # the provenance block so a report says whose choice the level was.
    effort_requested: dict[str, str] = field(default_factory=dict)
    # Which request envelope this endpoint takes. A name from
    # `structured.PROFILES`, chosen by the operator and never derived from the
    # model id: one vendor serves models with different envelopes, so a guess
    # from a name would be wrong on a real pair that exists today.
    profile: str = DEFAULT_PROFILE
    # The served context window, stated rather than measured. See
    # `DEFAULT_WINDOW`: `None` means ask the endpoint, and is the default.
    window: int | None = DEFAULT_WINDOW
    # Who a stated window is attributed to in `window.stated`'s `declared_by`,
    # and so in the Provenance detail (`client.py`, `window.stated`). Not
    # parsed from the environment: the CLI default here names the flag and the
    # variable a shell operator actually set, and the one caller who knows a
    # figure came from somewhere else instead -- `web.jobs.web_settings`, when
    # the request's own `window` field stated it -- replaces this rather than
    # this field guessing its own origin from what else is set.
    window_declared_by: str = "--window / LLOSSLESS_WINDOW"
    # An explicit output ceiling for `merge`, the only role that sets one
    # (`structured.Profile.budget_field`'s docstring). `None` is not "zero
    # ceiling", it is "let the profile decide": `openai-compatible` still
    # computes one from the documents, `anthropic` and `openai-reasoning` send
    # none at all. Set, this overrides that decision on every profile, so an
    # operator can still name a number on an unbounded profile without a code
    # change -- which is the point of the setting existing at all.
    max_tokens: int | None = None
    min_interval: float = 0.0
    # Whether the answer is carried back in pieces. On by default because one
    # hosted endpoint refuses any request that has not begun answering within
    # about 125 seconds -- a proxy in front of it, not the model -- and at that
    # endpoint's rate the wall lands around 9,000 output tokens, which a merge
    # at `high` is routinely budgeted past. The request is identical either way
    # and so is the reassembled body, so this is not part of any cassette key.
    # It does change what `timeout` bounds: a stream renews the clock on every
    # chunk, so the field becomes a limit on silence rather than on the call.
    stream: bool = True
    # What the operator asked for, and `None` for "nothing asked". The number
    # a call is actually made with is `call_timeout`, which is where the two
    # backends' different defaults live: a bound stated by an operator
    # applies as stated, and only an unstated one is resolved per backend.
    # Carried as the unstated value rather than resolved here so that
    # `replace(settings, command=...)` -- which is what `--answer-with` does --
    # still lands on the command default instead of on whatever the HTTP
    # configuration had already been resolved to.
    timeout: float | None = None
    ca_bundle: str | None = None
    cache_dir: Path = CACHE_DIR
    record_dir: Path | None = None
    replay_dir: Path | None = None
    force_record: bool = False
    allow_mixed_sources: bool = False
    max_calls: int = DEFAULT_MAX_CALLS
    dry_run: bool = False
    # On in a checkout, off when installed. See `add_arguments`; the two are
    # the same decision written in the two places it has to be visible.
    #
    # A factory rather than a plain default, so the answer is read when a
    # Settings is made rather than when this module is imported. That is what
    # lets a test stand where an installed user stands without installing
    # anything, and a default nobody can reach from a test is a default nobody
    # has checked.
    use_cache: bool = field(default_factory=lambda: IN_CHECKOUT)
    # The repeat index of an otherwise identical request. It never reaches
    # the request body -- it is in the cassette key so that a runner
    # measuring resample spread does not collide with its own first draw.
    sample: int = 0
    # A subprocess to answer with, instead of an HTTP endpoint. Empty is
    # the ordinary case and means the transport. Non-empty is the whole switch:
    # there is no `backend` field beside it, because a backend named `command`
    # with no command and a command with the backend left at `http` are two
    # invalid states a single field cannot express.
    #
    # Everything this costs is in `backend.py` and stated there. The part that
    # belongs here is that the containment guards stop at the process boundary:
    # `check_base_url` has no URL to inspect, and the suite's network
    # containment is per-process, so a child that opens a socket opens it
    # unobserved. That is why `provenance.hosted` is true for any command
    # backend rather than silent.
    command: str = ""
    # What a person may call that command. Empty is the ordinary case and means
    # nothing has a name for this backend but the hash of its command.
    #
    # It exists because the hash is unreadable and the address is a lie. Before
    # this, a command run's banner and the web page's endpoint row both printed
    # `banner_endpoint`, which is derived from `base_url` -- so a run that
    # contacted no endpoint at all announced the local ollama it never touched.
    # That was a defect on the one line an operator reads *while the run is
    # going*, and it is the line the money is committed on.
    #
    # **Display only.** It is not a cassette key component, for the reason
    # `endpoint_label` is not: naming a deployment is a thing the operator does
    # to their own records, and nothing about the bytes sent changes with it.
    # `command` is already in the key and is what separates one program's
    # recordings from another's.
    command_label: str = ""
    # How this command's stdout is read: `backend.RAW` (the answer is the
    # text) or `backend.RESULT` (the answer is inside a JSON result envelope
    # that also carries the usage block). Declared by whoever configured the
    # command, never detected from what comes back -- the answer under `raw`
    # is itself JSON, so a sniffer would be choosing between two JSON objects
    # on the presence of a key.
    #
    # Default `raw`, which is what this backend did before the option existed,
    # so no configured command changes behaviour by being upgraded past it.
    #
    # Not a cassette key component, for `command_label`'s reason: it changes
    # how a reply is unwrapped and not what was sent.
    command_envelope: str = ENVELOPE_RAW

    def __post_init__(self) -> None:
        # Every directory here can arrive as a string: from an env var, from a
        # caller building Settings by hand, from JSON. Coercing once at the
        # boundary beats a TypeError three modules away from the mistake.
        for name in ("cache_dir", "record_dir", "replay_dir"):
            value = getattr(self, name)
            if isinstance(value, str):
                object.__setattr__(self, name, Path(value))
        # Same argument for the label, and it is load-bearing rather than tidy:
        # a whitespace-only label is an operator who did not name a deployment,
        # and if it survived here it would hash to an id and silently detach the
        # corpus from the host it actually came from.
        object.__setattr__(self, "endpoint_label", self.endpoint_label.strip())
        object.__setattr__(self, "base_url", with_api_path(self.base_url))
        # The same normalisation for every per-role endpoint, and the same
        # reason: `with_api_path` is what lets an operator paste the URL the
        # vendor's console shows them. A map entry that skipped it would work
        # for one vendor and 404 for the next, and the difference would look
        # like the role rather than like the URL.
        if self.endpoints:
            object.__setattr__(self, "endpoints", {
                role: with_api_path(url) for role, url in self.endpoints.items()})
        # Checked on the object rather than only in `from_env`, because a
        # stated window is the one setting here that a guard is computed
        # against: `window.guard` refuses a request that does not fit it, so a
        # zero or a negative would refuse every call in the run and a string
        # would raise a TypeError inside the comparison, three modules from the
        # mistake. A Settings built by hand in a test reaches the same check.
        if self.window is not None:
            try:
                tokens = int(self.window)
            except (TypeError, ValueError):
                raise ConfigError(
                    f"the stated context window {self.window!r} is not a whole "
                    f"number of tokens"
                ) from None
            if tokens <= 0:
                raise ConfigError(
                    f"the stated context window must be a positive number of "
                    f"tokens; got {self.window!r}. Unset it to have the tool "
                    f"ask the endpoint instead -- there is no such thing as a "
                    f"default window here."
                )
            object.__setattr__(self, "window", tokens)
        if self.profile not in PROFILES:
            raise ConfigError(
                f"unknown request profile {self.profile!r}; the profiles are "
                f"{', '.join(sorted(PROFILES))}"
            )
        # Refused here rather than at the first call, for the reason every
        # other setting in this block is: a typo in a route's envelope is a
        # sentence before anything is spent, not a `CommandError` after a
        # model has answered.
        if self.command_envelope not in COMMAND_ENVELOPES:
            raise ConfigError(
                f"unknown command envelope {self.command_envelope!r}; the "
                f"envelopes are {', '.join(COMMAND_ENVELOPES)}"
            )
        # A command backend has to be told its window, because it cannot be
        # asked for one. `DEFAULT_WINDOW is None` means "probe the
        # endpoint", and the probe is `/api/ps` over HTTP: there is no endpoint
        # here to probe. Token counts are equally unavailable, so the post-hoc
        # overrun check is blind too, and *both* ends of the window guard are
        # gone at once. A run that silently had neither would report a clean
        # merge that the model had in fact been handed half of.
        #
        # Every role, not one. A run states a window per role or states one for
        # all of them, and a per-role map covering two of three leaves the
        # third exactly as blind as stating nothing.
        if self.command and self.window is None:
            missing = sorted(set(ROLES) - set(self.windows))
            if missing:
                raise ConfigError(
                    f"a command backend cannot be asked for its context "
                    f"window, so it has to be told: pass --window, or set "
                    f"LLOSSLESS_WINDOW, or set LLOSSLESS_WINDOW_<ROLE> for "
                    f"every role ({', '.join(missing)} still unstated). "
                    f"Unlike an HTTP "
                    f"endpoint there is nothing here to probe and no token "
                    f"count to check against afterwards, so an unstated window "
                    f"is not a smaller guarantee -- it is none."
                )

    # -- endpoint ---------------------------------------------------------

    @property
    def host(self) -> str:
        """Host only. No scheme, no port, no path, no credentials.

        This is the one form of the endpoint that is allowed into a report or a
        cassette. A full URL can carry a path that identifies a deployment, and
        in some setups a token in the query string.
        """
        return urlsplit(self.base_url).hostname or ""

    @property
    def endpoint_id(self) -> str:
        """This deployment, de-identified — or the one the operator named instead.

        Scheme, host, port and path, hashed. Not `host`: the deployment
        this project's own runs are recorded against is one path on a shared
        provider hostname, and hashing the hostname gave every deployment there
        the same id.

        `is_local` and `where` deliberately stay on `host`. A label says which
        deployment this is, not where it is, and letting it move the local/hosted
        judgement would let an operator relabel their way past the warning that
        document content is leaving the machine.
        """
        # A command backend has no address to hash. Falling through would
        # stamp every such run with the id of the default localhost endpoint it
        # never contacted, which is the second half of the same fault
        # -- the first half being the `content_left_this_machine: false` beside
        # it. The command is what distinguishes one of these deployments from
        # another, so the command is what gets hashed. Only the digest is ever
        # written, so an absolute path inside it stays in the environment, on
        # the same terms as the address it stands in for. A label still wins,
        # because naming the deployment is the operator's call either way.
        if self.command and not self.endpoint_label:
            return hashlib.sha256(
                self.command.encode("utf-8")).hexdigest()[:ENDPOINT_ID_CHARS]
        return endpoint_id(self.base_url, self.endpoint_label)

    @property
    def endpoint_name(self) -> str:
        """What an error message is allowed to call this endpoint.

        `cli.py` documents the label as recorded *in place of* the host, and an
        error message is a record: it reaches stderr, a captured log, and from
        there a decision entry or a paper. A rented pod's hostname carries the
        pod id and the provider, and one already reached a transcript
        through a 404 body. So every message that names the endpoint names this
        instead of `host`.

        Unlabelled, it *is* the host, because someone debugging their own
        endpoint needs to read which machine refused them and has no label to
        look the hash back up in. The label is the operator saying this
        deployment is one whose address does not get written down.

        **A command backend never gives the host**, labelled or not. There is
        no host: `base_url` still holds whatever the environment configured and
        the run contacted none of it, so returning it here would put an address
        this run never used into every message about a program that failed.
        The id is the hashed command, which is the one identifier this
        backend actually has.
        """
        if self.command:
            return f"endpoint {self.endpoint_id}"
        return f"endpoint {self.endpoint_id}" if self.endpoint_label else self.host

    @property
    def banner_endpoint(self) -> str:
        """What the opening line may call the endpoint.

        Separate from `endpoint_name` because the unlabelled answer differs: the
        banner names the endpoint so that someone with three configured can see
        which one is about to be waited on. `endpoint_name` answers a narrower
        question inside an error. Labelled, both give the id and neither gives
        the address.

        **Scheme, host and port only.** It used to print the whole URL the
        operator typed, path and all, which is the first line of every captured
        log -- and a URL carries more than an address: userinfo is a credential,
        and a path or query can carry a token somebody pasted. Those are dropped
        here rather than trusted not to be there. The full string is still
        available at `-vv`, where the operator has asked for it.

        **A command backend answers with its own name and never an address.**
        This line is read while the run is going, before anything is spent, and
        for a command run every URL in the environment is configuration the run
        is about to ignore -- so printing one announced a destination that was
        not the destination. `command_label` is what the operator called this
        route; with none, the word `command`, which says which mechanism is
        answering and claims nothing about where it went.
        """
        return self.banner_endpoint_for(None)

    def banner_endpoint_for(self, role: str | None) -> str:
        """`banner_endpoint`, read off one role's own endpoint.

        The same three answers in the same order, so a run header that names
        each role cannot word an address differently from the one that names
        the run. `None` is the run-wide endpoint, `base_url_for`'s convention.
        """
        if self.command:
            return self.command_label or "command"
        if self.endpoint_label:
            return self.endpoint_name if role is None else self.endpoint_name_for(role)
        url = self.base_url_for(role)
        parsed = urlsplit(url)
        if not parsed.scheme or not parsed.hostname:
            return url
        port = f":{parsed.port}" if parsed.port else ""
        return f"{parsed.scheme}://{parsed.hostname}{port}"

    @property
    def port(self) -> int:
        """Port only, defaulted from the scheme. Part of which server this is.

        Two ollamas on one box at different ports are two deployments, and the
        capability record has to be able to tell them apart. Like `host`, this
        carries no path and no query, so nothing that identifies a deployment
        or hides a token comes with it.
        """
        parts = urlsplit(self.base_url)
        try:
            explicit = parts.port
        except ValueError:  # a malformed port; the request will fail on its own
            explicit = None
        return explicit or (443 if parts.scheme == "https" else 80)

    @property
    def is_local(self) -> bool:
        return self.host in LOCAL_HOSTS

    @property
    def where(self) -> str:
        return "local" if self.is_local else "hosted"

    def api_key(self, role: str | None = None) -> str | None:
        """The key for this role, read fresh at send time from the active source.

        None means send no header. `role=None` asks for the default key, which
        is what a caller outside a unit of work -- the window probe's own
        fallback, a smoke test -- has to ask for.

        Read fresh every call rather than captured at construction, and that is
        load-bearing now there can be several: a run holding three keys in
        fields would put three credentials in one object that `repr` and
        `asdict` reach. This kept the existing rule rather than making an
        exception for the map.

        **The rule is "no key value on anything serialisation reaches", not
        "keys come from `os.environ`"**. The environment was the first
        implementation of that rule and it is the reason this is single-tenant:
        a process has exactly one environment, so two jobs cannot hold two
        users' keys at once. `keys_for_this_run` swaps the *source* for the
        calling thread and leaves the rule untouched -- the source is a
        `ContextVar`, so it is on no dataclass, `asdict` cannot see it, and a
        thread that did not set one is unaffected.

        Unset, this is `os.environ.get` exactly as before, which is what every
        CLI run, every cassette and every recorded figure was measured under.
        """
        source = _KEY_SOURCE.get()
        if source is None:
            source = os.environ
        return source.get(self.api_key_env_for(role)) or None

    def api_key_env_for(self, role: str | None) -> str:
        """Which environment variable holds this role's key."""
        if role is not None and role not in ROLES:
            raise ConfigError(
                f"unknown role {role!r}; expected one of {', '.join(ROLES)}")
        return self.api_key_envs.get(role or "", self.api_key_env)

    def base_url_for(self, role: str | None = None) -> str:
        """Which endpoint serves this role.

        No `decompose` -> `verify` fallback here, deliberately, though
        `model_for` has one. That fallback exists because the two roles were
        argued to want the same *model*; it says nothing about where either is
        served, and inheriting a host from it would put a role on an endpoint
        nobody configured for it. A role with no entry uses `base_url`, which is
        the setting the operator did configure.
        """
        if role is not None and role not in ROLES:
            raise ConfigError(
                f"unknown role {role!r}; expected one of {', '.join(ROLES)}")
        return self.endpoints.get(role or "", self.base_url)

    def endpoint_id_for(self, role: str | None = None) -> str:
        """`endpoint_id`, per role, and identical to it unless a role is split.

        A label names a *deployment* so that a pod restart does not split one
        census entry in two. That guarantee broke in the other
        direction: with two endpoints under one label, two deployments shared
        one id and the census merged them. So a role with an endpoint of its
        own is hashed with its role name appended to the label -- still no
        address, still stable across a restart, and now one entry per box.

        A role with no override returns `endpoint_id`, so a single-endpoint run
        still stamps one id across all three roles.

        **Unlabelled, this hashes the role's whole address.** It hashed the
        role's hostname, which made that split a no-op on the one topology it
        was written for: two serverless deployments of one provider differ only
        in their path, so both roles got one id and the census merged the two
        boxes it exists to tell apart.
        """
        if role is not None and role not in ROLES:
            raise ConfigError(
                f"unknown role {role!r}; expected one of {', '.join(ROLES)}")
        # A command backend answers every role through the one program, so
        # per-role endpoints are dead configuration rather than routing.
        # Falling through would stamp this role's cassettes and its provenance
        # with the id of an HTTP endpoint the run never addressed, which is
        # the same fault at cassette scale -- and the combination is ordinary, not
        # exotic: an operator with vendor endpoints already in their
        # environment who tries a command run has it. Refusing that would make
        # the backend unusable without first clearing the environment, so it
        # is answered rather than refused, and `provenance` drops the by-role
        # block for the same reason.
        if self.command:
            return self.endpoint_id
        if role is None or role not in self.endpoints:
            return self.endpoint_id
        if self.endpoint_label:
            return endpoint_id("", f"{self.endpoint_label}/{role}")
        return endpoint_id(self.base_url_for(role))

    def endpoint_name_for(self, role: str | None = None) -> str:
        """What a message may call this role's endpoint.

        `endpoint_name`'s rule, applied per role: labelled, the id and never the
        address; unlabelled, the host, because an operator debugging their own
        box needs to read which machine refused them. One label covers the run,
        so a labelled deployment stays labelled for every role -- what differs
        is the host underneath, and that is exactly what must not be printed.
        """
        if self.endpoint_label:
            return f"endpoint {self.endpoint_id_for(role)}"
        return urlsplit(self.base_url_for(role)).hostname or self.base_url_for(role)

    def effort_for(self, role: str) -> str:
        """The level this role's calls will really be asked for, or "".

        One line, because the precedence is `effort_of`'s and lives there. What
        this adds is the operator's own map, which only a `Settings` holds.
        """
        return effort_of(self.command, role, self.effort)

    def command_for(self, role: str) -> str:
        """The argv this role's calls will really execute.

        **Read this, never `command`**, wherever a call is about to be made.
        `command` is the route -- the operator's program, plus the retrieval
        grant, which is a property of the run and not of the role. The effort
        level is not: the merge is asked for more than the two roles that read
        its work back, so the flag goes on here, where the role is known.

        So is the isolation, `--safe-mode` and `--tools`: here, per call,
        so `command` stays what a sweep re-levels. Both are read back off this,
        so a provenance block cannot describe a level the run was not asked for.
        """
        return command_with_effort(command_with_isolation(self.command), role, self.effort)

    @property
    def effort_ignored(self) -> tuple[str, ...]:
        """Roles the operator named a level for that this build cannot deliver.

        Not a refusal, deliberately. `LLOSSLESS_EFFORT` exported in a shell
        would otherwise break every HTTP run in it, and an HTTP endpoint has
        no level to be asked for -- `reasoning_effort` on that path is a
        thinking-off switch and not a rung (`structured.build_body`). The same
        goes for a program whose flags this build has never read: appending one
        it does not take breaks a working route rather than widening it.

        So the request is dropped and **said out loud** instead, on
        `usage.thinking_ignored`'s terms -- what was asked, and what was really
        done, kept apart and both published.
        """
        return tuple(role for role in ROLES
                     if self.effort.get(role) and not self.effort_for(role))

    def window_for(self, role: str | None = None) -> int | None:
        """The stated window for this role's endpoint, or the run-wide one.

        None still means "ask the endpoint", which only Ollama answers. A role
        whose endpoint cannot be asked and has no stated figure is refused by
        `window.preflight`, unchanged since the per-role map was added -- the point of the map is
        that the figure can now differ per role, not that it can be skipped.
        """
        if role is not None and role not in ROLES:
            raise ConfigError(
                f"unknown role {role!r}; expected one of {', '.join(ROLES)}")
        return self.windows.get(role or "", self.window)

    @property
    def call_timeout(self) -> float:
        """The seconds one call gets. **Read this, never `timeout`**.

        `timeout` is what the operator stated and is `None` when they stated
        nothing; this is the number a request is made with, and it is the one
        place the two backends' defaults differ. See `COMMAND_TIMEOUT` for the
        measurement the command figure comes from and for why it is not simply
        a larger `DEFAULT_TIMEOUT`: over HTTP the field bounds *silence*,
        because a stream renews the clock on every chunk, and against a
        subprocess it bounds the whole call.

        A stated figure is used exactly as stated on either backend. An
        operator who passes `--timeout 30` to a command backend has said
        something specific, and quietly serving them 890 would be this
        function overruling them.
        """
        if self.timeout is not None:
            return self.timeout
        return COMMAND_TIMEOUT if self.command else DEFAULT_TIMEOUT

    @property
    def verify_batch(self) -> int:
        """How many claims one verify call carries on this backend.

        `call_timeout`'s sibling, and the same shape for the same reason: it is
        one setting whose right answer depends on which backend answers, and
        resolving it here means no call site has to know that. See
        `COMMAND_VERIFY_BATCH` for the measurement the command figure comes
        from -- a command backend's cost is ~26-30 s a call plus ~1.3-1.5 s a
        claim, so time per claim falls as the batch grows and 25 there pays
        the fixed part four times where 100 pays it once.

        The HTTP figure is untouched and must stay untouched: batch size
        reaches `messages`, `messages` is a cassette-key component, and every
        recorded verify cassette in this repository was made at 25.
        """
        return COMMAND_VERIFY_BATCH if self.command else DEFAULT_VERIFY_BATCH

    @property
    def split_endpoints(self) -> bool:
        """Is more than one endpoint in play? `-vv` and the banner ask this."""
        return bool(self.endpoints) and {
            self.base_url_for(role) for role in ROLES} != {self.base_url}

    # -- models -----------------------------------------------------------

    def model_for(self, role: str) -> str:
        """The vendor model id for a logical role.

        decompose falls back to verify: they are both the small structured-output
        model and the original design never gives them separate budgets. If that stops
        being true, add a decompose entry to models.local.json — no code change.
        """
        if role not in ROLES:
            raise ConfigError(f"unknown role {role!r}; expected one of {', '.join(ROLES)}")
        for candidate in (role, "verify") if role == "decompose" else (role,):
            if self.models.get(candidate):
                return self.models[candidate]
        # Names every path, not just the filename. Installed, `models.local.json`
        # is not beside anything the operator can see, and a refusal that says
        # only the name leaves them to guess which directory it meant.
        raise ConfigError(
            f"no model configured for role {role!r}. Set LLOSSLESS_MODEL, or add "
            f'{{"{role}": "..."}} to ' + " or ".join(str(p) for p in MODEL_MAP_CANDIDATES)
            + "."
        )

    def thinks(self, role: str) -> bool:
        """Should this role be allowed to emit a reasoning block?

        Off for every role by default -- `DEFAULT_THINKING` is empty. Verify
        and decompose are the same small model doing the same kind of
        mechanical extraction, where a reasoning block costs several seconds a
        call and changes nothing, and their published figures were recorded
        off.

        Merge is the interesting case. See DEFAULT_THINKING for the evidence
        that argues for turning it on there and for what it does not claim --
        the A/B that would have attributed the difference to the prompt
        returned no clear signal -- and for why it ships off anyway.
        """
        return role in self.thinking

    # -- run mode ---------------------------------------------------------

    @property
    def mode(self) -> str:
        # Dry run first, and above replay: it is the only mode in which nothing
        # was asked of anything, and a provenance header reading "live" over a
        # run that made no request is the report telling its first lie.
        if self.dry_run:
            return "dry-run"
        if self.replay_dir is not None:
            return "replay"
        if self.record_dir is not None:
            return "record"
        return "live"


def load_model_map(path: Path = MODEL_MAP_FILE) -> dict[str, str]:
    """Read the untracked role -> model id map. Absent is normal, not an error."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"{path.name} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"{path.name} must be an object of role -> model id")

    unknown = sorted(set(data) - set(ROLES))
    if unknown:
        raise ConfigError(
            f"{path.name} names roles that do not exist: {', '.join(unknown)}. "
            f"Valid roles: {', '.join(ROLES)}."
        )
    return {role: str(model) for role, model in data.items() if model}


def from_env(
    environ: dict[str, str] | None = None,
    model_map_path: Path = MODEL_MAP_FILE,
    *,
    window: int | None = None,
) -> Settings:
    """Resolve settings from the environment and models.local.json.

    Precedence is env > file. The file supplies the mapping for a normal run;
    an env var is the explicit one-off override, so it wins.

    `window` is `--window`, when `resolve` has one, and it beats
    `LLOSSLESS_WINDOW` as every flag beats its variable. It is taken here and
    not only in `apply_arguments` because `Settings.__post_init__` refuses a
    command with no window, and this function builds a `Settings`: with
    `LLOSSLESS_COMMAND` set and the window given as a flag, the object built
    from the environment alone was refused before the flag was read.

    `model_map_path` is a parameter so the test suite can point it somewhere
    empty. Reading the developer's own models.local.json would make the suite
    pass or fail depending on a file that is deliberately untracked.
    """
    env = os.environ if environ is None else environ

    models = load_model_map(model_map_path)
    if env.get("LLOSSLESS_MODEL"):
        models["verify"] = env["LLOSSLESS_MODEL"]
    if env.get("LLOSSLESS_MERGE_MODEL"):
        models["merge"] = env["LLOSSLESS_MERGE_MODEL"]
    models.setdefault("merge", models.get("verify", ""))
    models = {role: model for role, model in models.items() if model}

    # Per-role endpoint, key and window. One variable per role per
    # axis rather than one parsed string, because the parsed form would need a
    # separator that cannot appear in a URL, an env var name or an integer, and
    # every candidate appears in at least one of them.
    #
    # `LLOSSLESS_API_KEY_ENV_<ROLE>` names a *variable*, matching
    # `LLOSSLESS_API_KEY_ENV`. A run with a frontier merge and a local
    # decompose then holds two variable names and no keys, which is the same
    # property already true of the single-endpoint case.
    endpoints, api_key_envs, windows = {}, {}, {}
    # The run-wide effort level, laid down first so that a per-role variable
    # below overwrites it. `LLOSSLESS_WINDOW`'s relationship to
    # `LLOSSLESS_WINDOW_<ROLE>`, on the same axis: the general
    # statement is the floor and the specific one is the exception to it.
    effort = effort_from_env(env)
    for role in ROLES:
        suffix = role.upper()
        if env.get(f"LLOSSLESS_BASE_URL_{suffix}", "").strip():
            endpoints[role] = env[f"LLOSSLESS_BASE_URL_{suffix}"].strip().rstrip("/")
        if env.get(f"LLOSSLESS_API_KEY_ENV_{suffix}", "").strip():
            api_key_envs[role] = env[f"LLOSSLESS_API_KEY_ENV_{suffix}"].strip()
        raw = env.get(f"LLOSSLESS_WINDOW_{suffix}", "").strip()
        if raw:
            try:
                windows[role] = int(raw)
            except ValueError:
                raise ConfigError(
                    f"LLOSSLESS_WINDOW_{suffix} must be a whole number of "
                    f"tokens; got {raw!r}") from None
            if windows[role] <= 0:
                raise ConfigError(
                    f"LLOSSLESS_WINDOW_{suffix} must be positive; got {raw!r}")

    structured = env.get("LLOSSLESS_STRUCTURED", "auto").strip().lower() or "auto"
    if structured not in STRUCTURED_MODES:
        raise ConfigError(
            f"LLOSSLESS_STRUCTURED={structured!r} is not one of "
            f"{', '.join(STRUCTURED_MODES)}"
        )

    # Validated here rather than left to argparse, because nothing validates an
    # environment variable for you and an unknown level would otherwise travel
    # as far as the fragment loader, where it becomes a filename.
    depth = (env.get("LLOSSLESS_VERIFY_DEPTH", DEFAULT_VERIFY_DEPTH)
             .strip().lower() or DEFAULT_VERIFY_DEPTH)
    if depth not in VERIFY_DEPTHS:
        raise ConfigError(
            f"LLOSSLESS_VERIFY_DEPTH={depth!r} is not one of "
            f"{', '.join(VERIFY_DEPTHS)}")
    verify_depth = depth

    given = env.get("LLOSSLESS_FIDELITY", DEFAULT_FIDELITY).strip().lower() or DEFAULT_FIDELITY
    # Resolved to the wire spelling before the membership test, so `verbatim`
    # and `off` are the same run and everything downstream sees one value.
    fidelity = canonical_fidelity(given)
    if fidelity not in FIDELITY_LEVELS:
        raise ConfigError(
            f"LLOSSLESS_FIDELITY={given!r} is not one of {', '.join(FIDELITY_CHOICES)}"
        )

    field_order = (env.get("LLOSSLESS_FIELD_ORDER", DEFAULT_FIELD_ORDER)
                   .strip().lower() or DEFAULT_FIELD_ORDER)
    if field_order not in FIELD_ORDERS:
        raise ConfigError(
            f"LLOSSLESS_FIELD_ORDER={field_order!r} is not one of {', '.join(FIELD_ORDERS)}"
        )

    title_policy = (
        env.get("LLOSSLESS_TITLE_POLICY", DEFAULT_TITLE_POLICY).strip().lower()
        or DEFAULT_TITLE_POLICY
    )
    if title_policy not in TITLE_POLICIES:
        raise ConfigError(
            f"LLOSSLESS_TITLE_POLICY={title_policy!r} is not one of {', '.join(TITLE_POLICIES)}"
        )

    # `.get` with no default, deliberately: unset and set-but-empty are two
    # different instructions here. Unset means "no opinion", and takes
    # DEFAULT_THINKING. Empty means "no role thinks", and is the off switch.
    raw_thinking = env.get("LLOSSLESS_THINKING")
    thinking = (
        DEFAULT_THINKING
        if raw_thinking is None
        else frozenset(
            role.strip().lower()
            for role in raw_thinking.split(",")
            if role.strip()
        )
    )
    unknown_roles = sorted(thinking - set(ROLES))
    if unknown_roles:
        raise ConfigError(
            f"LLOSSLESS_THINKING names roles that do not exist: {', '.join(unknown_roles)}"
        )

    profile = (env.get("LLOSSLESS_PROFILE", DEFAULT_PROFILE).strip().lower()
               or DEFAULT_PROFILE)
    if profile not in PROFILES:
        raise ConfigError(
            f"LLOSSLESS_PROFILE={profile!r} is not one of "
            f"{', '.join(sorted(PROFILES))}"
        )

    # Unset is not zero and is not a default -- it is "ask the endpoint", which
    # is what `window.reported` and `window.measured` are for. Only an operator
    # who has stated a figure gets one, and they get exactly the figure they
    # stated. `int(raw, 10)` rather than `float`: a window is a token count, and
    # `LLOSSLESS_WINDOW=1e5` is a typo worth refusing rather than rounding.
    raw_window = env.get("LLOSSLESS_WINDOW", "").strip()
    try:
        stated_window = int(raw_window, 10) if raw_window else DEFAULT_WINDOW
    except ValueError as exc:
        raise ConfigError(
            f"LLOSSLESS_WINDOW={raw_window!r} is not a whole number of tokens"
        ) from exc
    if stated_window is not None and stated_window <= 0:
        raise ConfigError(
            f"LLOSSLESS_WINDOW={raw_window!r} must be a positive number of "
            f"tokens; unset it to have the tool ask the endpoint instead"
        )

    # Same shape as `LLOSSLESS_WINDOW` just above: unset is not zero, it is
    # "let the profile decide" (`Settings.max_tokens`'s docstring), and only an
    # operator who names a figure gets one.
    raw_max_tokens = env.get("LLOSSLESS_MAX_TOKENS", "").strip()
    try:
        max_tokens = int(raw_max_tokens, 10) if raw_max_tokens else None
    except ValueError as exc:
        raise ConfigError(
            f"LLOSSLESS_MAX_TOKENS={raw_max_tokens!r} is not a whole number of tokens"
        ) from exc
    if max_tokens is not None and max_tokens <= 0:
        raise ConfigError(
            f"LLOSSLESS_MAX_TOKENS={raw_max_tokens!r} must be a positive number "
            f"of tokens; unset it to have the profile decide instead"
        )

    raw_interval = env.get("LLOSSLESS_MIN_INTERVAL", "").strip()
    try:
        min_interval = float(raw_interval) if raw_interval else 0.0
    except ValueError as exc:
        raise ConfigError(f"LLOSSLESS_MIN_INTERVAL={raw_interval!r} is not a number") from exc

    # Off by an explicit falsehood only. A variable set to something unreadable
    # is a mistake, and defaulting it to "no streaming" would answer that mistake
    # by walking into the 125-second wall three hours into a run.
    raw_stream = env.get("LLOSSLESS_STREAM", "").strip().lower()
    if raw_stream and raw_stream not in TRUTHY | FALSEY:
        raise ConfigError(
            f"LLOSSLESS_STREAM={raw_stream!r} is neither true nor false; use one of "
            f"{', '.join(sorted(TRUTHY | FALSEY))}"
        )
    stream = raw_stream not in FALSEY

    # Bounds checked here, both ends, because argparse validates neither and a
    # budget is the threshold an exit code is read against. 0.0 is a coherent
    # strict mode under the strictly-greater rule -- no drop at all is
    # permitted, one drop fails -- so it is accepted rather than treated as
    # unset. 1.0 is accepted too, and is the reason `Run.budget_disables_check`
    # exists: at 1.0 the check cannot fire, and a disabled check that reads as
    # a passed check is this project's most-repeated failure class.
    raw_budget = env.get("LLOSSLESS_LOSS_BUDGET", "").strip()
    try:
        loss_budget = (float(raw_budget) if raw_budget
                       else DEFAULT_DECLARED_LOSS_BUDGET)
    except ValueError as exc:
        raise ConfigError(
            f"LLOSSLESS_LOSS_BUDGET={raw_budget!r} is not a number"
        ) from exc
    if not 0.0 <= loss_budget <= 1.0:
        # `not (0 <= x <= 1)` rather than two comparisons: NaN fails every
        # comparison it is asked, so this is the form that rejects it.
        raise ConfigError(
            f"LLOSSLESS_LOSS_BUDGET={raw_budget!r} is not a fraction between "
            f"0.0 and 1.0 inclusive; it is a share of the source segments, not "
            f"a percentage"
        )

    # Unset is `None` -- "nothing was stated" -- and not a number, because the
    # number depends on which backend answers and that is not settled here:
    # `--answer-with` can turn a command backend on after this function has
    # run. `Settings.call_timeout` resolves it.
    raw_timeout = env.get("LLOSSLESS_TIMEOUT", "").strip()
    try:
        timeout = float(raw_timeout) if raw_timeout else None
    except ValueError as exc:
        raise ConfigError(f"LLOSSLESS_TIMEOUT={raw_timeout!r} is not a number") from exc
    if timeout is not None and timeout <= 0:
        raise ConfigError("LLOSSLESS_TIMEOUT must be greater than zero")

    ca_bundle = env.get("LLOSSLESS_CA_BUNDLE", "").strip() or None
    if ca_bundle and not Path(ca_bundle).exists():
        raise ConfigError(f"LLOSSLESS_CA_BUNDLE points at a file that does not exist: {ca_bundle}")

    # Not in the original variable list, but an earlier deployment's container ran on a
    # read-only filesystem and the cache has to go somewhere writable.
    cache_dir = Path(env.get("LLOSSLESS_CACHE_DIR", "").strip() or CACHE_DIR)

    return Settings(
        base_url=(env.get("LLOSSLESS_BASE_URL") or DEFAULT_BASE_URL).rstrip("/"),
        # Stripped, and empty means unset: a variable exported as "" is an
        # operator who did not name a deployment, not one who named it "".
        endpoint_label=env.get("LLOSSLESS_ENDPOINT_LABEL", "").strip(),
        models=models,
        endpoints=endpoints,
        api_key_envs=api_key_envs,
        windows=windows,
        # Stripped, and empty means unset for the same reason the label above
        # is: `LLOSSLESS_COMMAND=""` is an operator who did not choose a
        # command backend, not one who chose the empty command.
        command=env.get("LLOSSLESS_COMMAND", "").strip(),
        # Display only, and stripped for the same reason: a variable exported
        # as "" is a backend nobody named. It is what the banner and the
        # provenance block call this route instead of naming an address the
        # run never contacted.
        command_label=env.get("LLOSSLESS_COMMAND_LABEL", "").strip(),
        # Set by the route that owns the command, so the operator who wrote
        # the argv is the one who says what that argv answers with. Empty
        # falls back to `raw`, which is what an existing configuration means.
        command_envelope=(env.get("LLOSSLESS_COMMAND_ENVELOPE", "").strip().lower()
                          or ENVELOPE_RAW),
        api_key_env=env.get("LLOSSLESS_API_KEY_ENV", DEFAULT_KEY_ENV).strip() or DEFAULT_KEY_ENV,
        structured=structured,
        pinned=structured != "auto",
        fidelity=fidelity,
        verify_depth=verify_depth,
        declared_loss_budget=loss_budget,
        field_order=field_order,
        title_policy=title_policy,
        thinking=thinking,
        effort=effort,
        profile=profile,
        window=stated_window if window is None else window,
        max_tokens=max_tokens,
        min_interval=min_interval,
        stream=stream,
        timeout=timeout,
        ca_bundle=ca_bundle,
        cache_dir=cache_dir,
    )


def add_arguments(
    parser,
    offline_dir: Path = OFFLINE_CASSETTES,
    *,
    corpus_tools: bool = True,
) -> None:
    """The flags every entry point shares. Kept here so they cannot drift apart.

    `offline_dir` is what `--offline` resolves to. It is a parameter because a
    milestone's corpus is its own directory: for example, the `m4/` corpus records into
    `tests/responses/m4/`, one revision per directory — and `--offline` has to
    mean "this runner's recordings" rather than "the recordings of whichever
    runner was written first". Pass the same value to `apply_arguments`.

    `corpus_tools=False` drops `--record`, `--replay`, `--offline`, `--force`
    and `--mixed-sources`. They exist to build and replay the measurement
    corpus under `tests/responses/`, which is a thing this repository does to
    itself; on the installed command they would be five flags whose failure
    modes — a half-recorded corpus, a mixed-revision one — a user has no way to
    diagnose. `apply_arguments` reads every flag through `getattr` with a
    default, so their absence needs no second code path.
    """
    group = parser.add_argument_group("endpoint")
    group.add_argument("--base-url", help="override LLOSSLESS_BASE_URL")
    # `--answer-with`, not `--command`: the subparser in `cli.py` already owns
    # `dest="command"` for the subcommand name, so a flag of that name
    # overwrites it -- with `None` when unpassed, which loses the subcommand
    # and prints the top-level usage, and with the subcommand name when
    # `apply_arguments` reads it back, which would have turned the command
    # backend on for every run. The explicit `dest` keeps the two apart even
    # if a future flag name drifts back towards the collision.
    group.add_argument(
        "--answer-with",
        dest="answer_with",
        metavar="COMMAND",
        help="answer through this program instead of an HTTP endpoint: the "
             "prompt on its stdin, the answer on its stdout (overrides "
             "LLOSSLESS_COMMAND). Needs --window, because there is nothing "
             "to probe for one and no token count to check against after",
    )
    group.add_argument("--model", help="model id for the verify/decompose role")
    group.add_argument("--merge-model", help="model id for the merge role")
    group.add_argument(
        "--structured",
        choices=STRUCTURED_MODES[1:],
        help="pin a structured-output tier and skip the capability probe",
    )
    group.add_argument(
        "--field-order",
        choices=FIELD_ORDERS,
        default=None,
        help=f"whether a response must emit fields in the order the schema "
             f"declares (default {DEFAULT_FIELD_ORDER}); `any` accepts a "
             f"complete, valid answer whose keys arrived in another order",
    )
    group.add_argument(
        "--profile",
        choices=sorted(PROFILES),
        default=None,
        help=f"the request envelope this endpoint accepts (default "
             f"{DEFAULT_PROFILE}): which field carries the output budget, and "
             f"whether temperature and seed are sent at all. Chosen, never "
             f"guessed from the model id",
    )
    group.add_argument(
        "--window",
        type=int,
        default=None,
        metavar="TOKENS",
        help="the context window this endpoint serves, stated because it "
             "cannot be measured -- a vendor has no /api/ps. Reported as "
             "stated rather than measured, and no probe is sent to confirm it",
    )
    group.add_argument(
        "--timeout",
        type=float,
        metavar="SECONDS",
        help=f"seconds per request (default {DEFAULT_TIMEOUT:g} over HTTP, "
             f"where a stream renews the clock and this bounds silence; "
             f"{COMMAND_TIMEOUT:g} for a command backend, which has no stream, "
             f"so it bounds the whole call)",
    )
    group.add_argument(
        "--thinking",
        action="append",
        choices=ROLES,
        metavar="ROLE",
        help=f"let this role emit a reasoning block; repeatable. The default "
             f"set is {', '.join(sorted(DEFAULT_THINKING)) or 'empty'}, and the "
             f"flag replaces that set rather than adding to it",
    )
    group.add_argument(
        "--effort",
        action="append",
        metavar="LEVEL|ROLE=LEVEL",
        help=f"how hard a command backend is asked to think: one of "
             f"{', '.join(EFFORT_LEVELS)}. Repeatable, and the two spellings "
             f"compose -- a bare level covers every role, ROLE=LEVEL names "
             f"one, later wins. A role nobody names keeps this build's own "
             f"level for it. Command backends only: an HTTP endpoint has no "
             f"flag to carry it",
    )
    group.add_argument(
        "--min-interval",
        type=float,
        metavar="SECONDS",
        help="wait at least this long between live calls; lets a local GPU cool down",
    )

    # Its own group, not "endpoint": this says what the merge is *allowed to
    # do*, which is a property of the work rather than of where the work runs.
    # The same level against the same documents means the same thing on a
    # laptop and behind an API, and a report has to print it for either.
    group = parser.add_argument_group("merge policy")
    group.add_argument(
        "--fidelity",
        choices=FIDELITY_CHOICES,
        default=None,
        # Rendered from `FIDELITY_SHAPES`, the way `--verify-depth` below is
        # rendered from `VERIFY_DEPTH_SHAPES` and for the same reason: the
        # help text and the sentence the web picker shows were two copies of
        # one description, and the copy nobody edits goes on describing the
        # old behaviour while reading exactly like the new one.
        help="how freely the merge may reword and combine the sources (default "
             + DEFAULT_FIDELITY + ". "
             + " ".join(f"{fidelity_name(level)}: {shape.summary} {shape.costs}"
                        for level, shape in FIDELITY_SHAPES.items())
             + f" {FIDELITY_PUBLISHED[0]} is the strictest setting, not the "
               f"absence of one; `off` is its older name and still works)",
    )
    group.add_argument(
        "--verify-depth",
        choices=VERIFY_DEPTHS,
        default=None,
        # Rendered from `VERIFY_DEPTH_SHAPES` rather than restated. The help
        # text and the sentence the web picker shows were two copies of one
        # description, which is the shape of drift this project has paid for
        # before: the copy nobody edits goes on describing the old behaviour
        # and reads exactly like the new one.
        help="how thoroughly the merge is checked (default "
             + DEFAULT_VERIFY_DEPTH + ". "
             + " ".join(f"{value}: {shape.explains}"
                        for value, shape in VERIFY_DEPTH_SHAPES.items())
             + " The mechanical structural checks run at either depth and cost "
               "no model call)",
    )
    group.add_argument(
        "--title-policy",
        choices=TITLE_POLICIES,
        default=None,
        # Built from the table, never retyped: the default's clause first and
        # the others after it, so naming a policy and describing another is not
        # a thing this string can do.
        help="which title the merged document takes (default "
             + DEFAULT_TITLE_POLICY + ": "
             + TITLE_POLICY_EXPLAINS[DEFAULT_TITLE_POLICY] + "; "
             + "; ".join(f"{value}: {TITLE_POLICY_EXPLAINS[value]}"
                         for value in TITLE_POLICIES
                         if value != DEFAULT_TITLE_POLICY)
             + ")",
    )
    group.add_argument(
        "--loss-budget",
        type=float,
        default=None,
        metavar="FRACTION",
        help=f"share of the source segments the merge may declare it dropped "
             f"before that is itself a finding (default "
             f"{DEFAULT_DECLARED_LOSS_BUDGET}); a fraction, not a percentage, "
             f"and 1.0 disables the check",
    )

    group = parser.add_argument_group("run mode")
    if corpus_tools:
        group.add_argument("--record", metavar="DIR", type=Path, help="write each call to DIR")
        group.add_argument("--replay", metavar="DIR", type=Path,
                           help="serve every call from DIR")
        group.add_argument(
            "--offline",
            action="store_true",
            help=f"alias for --replay {offline_dir.relative_to(ROOT)}",
        )
        group.add_argument(
            "--force",
            action="store_true",
            help="with --record, overwrite cassettes that already exist",
        )
        group.add_argument(
            "--mixed-sources",
            action="store_true",
            help="with --record, deepen a corpus recorded by a different revision",
        )
    # Two flags rather than one, because the default is not the same in both
    # places it runs. In a checkout the cache is on: the people it helps are
    # working on this repository, replaying the same corpus all day. Installed
    # it is off, because an installed user pointing this at a confidential
    # document should opt into keeping a copy of it, not opt out.
    group.add_argument("--no-cache", action="store_true",
                       help="ignore cached responses and persist nothing")
    group.add_argument("--cache", action="store_true",
                       help="use the response cache (the default in a checkout)")
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="render prompts and count calls, make no requests",
    )
    group.add_argument(
        "--max-calls",
        type=int,
        default=DEFAULT_MAX_CALLS,
        help=f"abort before exceeding N live calls (default {DEFAULT_MAX_CALLS})",
    )
    group.add_argument(
        "--sample",
        type=int,
        default=0,
        metavar="N",
        help="repeat index; part of the cassette key, never of the request",
    )


def cache_choice(args, settings: Settings) -> bool:
    """`--no-cache` off, `--cache` on, neither leaves the default alone.

    Written out rather than `not args.no_cache`, which is what stood here and
    is the reason the default could not move: it read as "the flag decides"
    and meant "the flag decides, and its absence decides too". A default that
    every invocation silently overrides is not a default.

    `--no-cache` wins over `--cache`. Somebody who has passed both is asking
    for two things and the safe one is the one that keeps nothing.
    """
    if getattr(args, "no_cache", False):
        return False
    if getattr(args, "cache", False):
        return True
    return settings.use_cache


def parse_effort(stated: list[str] | None) -> dict[str, str]:
    """`--effort`'s values as a role -> level map, in the order they were given.

    Two spellings on one flag: a bare level covers every role, `ROLE=LEVEL`
    names one, and later wins -- which is what a repeated flag means elsewhere
    on this command line and what the program itself does with a repeated
    `--effort`. So `--effort low --effort merge=high` reads as one sentence.

    Validated here rather than by argparse's `choices`, because `choices` on a
    flag with two spellings would have to hold every role crossed with every
    level, and what it prints on a typo would be that product instead of a
    sentence naming which half was wrong.
    """
    chosen: dict[str, str] = {}
    for item in stated or ():
        if "=" in item:
            named, _, level = item.partition("=")
            named, level = named.strip().lower(), level.strip().lower()
            if named not in ROLES:
                raise ConfigError(
                    f"--effort {item}: {named!r} is not a role; expected one "
                    f"of {', '.join(ROLES)}")
            roles: tuple[str, ...] = (named,)
        else:
            level, roles = item.strip().lower(), ROLES
        if level not in EFFORT_LEVELS:
            raise ConfigError(
                f"--effort {item}: {level!r} is not a level; expected one of "
                f"{', '.join(EFFORT_LEVELS)}")
        chosen.update(dict.fromkeys(roles, level))
    return chosen


def apply_arguments(settings: Settings, args, offline_dir: Path = OFFLINE_CASSETTES) -> Settings:
    """Layer parsed flags over env-derived settings. Flags always win."""
    models = dict(settings.models)
    if getattr(args, "model", None):
        # Assigned, not `setdefault`. `setdefault` looked equivalent and was
        # not: `models` starts as whatever models.local.json and the environment
        # produced, so a file naming a merge model made `--model` silently
        # partial -- the verify and decompose roles moved to the model the
        # operator named and the merge role stayed on the file's. That is not a
        # default being respected, it is a flag being half applied, and it
        # disagreed with this function's own first line, with README:172, and
        # with what an operator who types one model id means by it. It cost a
        # real run: a merge went out on a model nobody had named.
        #
        # Before the `--merge-model` branch, so the specific flag still beats
        # the general one. That ordering is the whole of the precedence rule.
        #
        # `decompose` too, for the same reason: `model_for` reads a file's
        # `decompose` entry before falling back to `verify`, so a flag that set
        # only `verify` left decompose on the file's model.
        models["verify"] = models["decompose"] = args.model
        models["merge"] = args.model
    if getattr(args, "merge_model", None):
        models["merge"] = args.merge_model

    replay = getattr(args, "replay", None)
    if getattr(args, "offline", False):
        if replay is not None and replay != offline_dir:
            raise ConfigError("--offline and --replay disagree; pass only one")
        # Named here rather than discovered later. `--offline` means "the
        # corpus in this repository", and outside a checkout of this repository
        # there is no such thing; without this the run gets as far as looking
        # for a cassette and reports a missing recording, which is a true
        # sentence about the wrong problem.
        if not Path(offline_dir).is_dir():
            raise ConfigError(
                f"--offline replays this repository's recorded corpus and there "
                f"is none at {offline_dir}. Use --replay DIR to name a corpus, "
                f"or run from a checkout that has one."
            )
        replay = offline_dir

    record = getattr(args, "record", None)
    if record is not None and replay is not None:
        raise ConfigError("--record and --replay are mutually exclusive")

    structured = getattr(args, "structured", None) or settings.structured
    base_url = getattr(args, "base_url", None) or settings.base_url

    return replace(
        settings,
        base_url=base_url.rstrip("/"),
        # Symmetry with every other endpoint flag: what an operator can set in
        # the environment they can override for one run, because switching
        # model and endpoint per run is what the CLI is for. The window
        # refusal lives in `__post_init__`, so it fires on the flag exactly as
        # it fires on the variable.
        command=getattr(args, "answer_with", None) or settings.command,
        models=models,
        structured=structured,
        pinned=structured != "auto",
        # The flag defaults to None rather than to the level, so an unpassed
        # flag leaves whatever the environment said instead of overwriting it.
        # `canonical_fidelity` is where `--fidelity verbatim` becomes `off`:
        # one resolution, at the boundary, so no consumer below has to know
        # the level has two names.
        fidelity=canonical_fidelity(getattr(args, "fidelity", None) or settings.fidelity),
        verify_depth=getattr(args, "verify_depth", None) or settings.verify_depth,
        title_policy=getattr(args, "title_policy", None) or settings.title_policy,
        declared_loss_budget=(
            settings.declared_loss_budget
            if getattr(args, "loss_budget", None) is None
            else args.loss_budget
        ),
        field_order=getattr(args, "field_order", None) or settings.field_order,
        thinking=frozenset(getattr(args, "thinking", None) or ()) or settings.thinking,
        # Overlaid on the environment's map rather than replacing it, which is
        # where this parts company with `--thinking` one line up: that flag
        # replaces a *set*, and there is exactly one way to spell "no role
        # thinks". Here every role always has a level, so replacing the map
        # would mean `--effort merge=high` silently handing `decompose` and
        # `verify` back to the program's own default -- the 3.3x this work
        # exists to stop paying.
        effort={**settings.effort, **parse_effort(getattr(args, "effort", None))},
        profile=getattr(args, "profile", None) or settings.profile,
        # `is None`, not `or`: every other numeric flag here is falsy at a
        # legal value or has none, and a window of 0 is refused rather than
        # read as unset -- so the only question this asks is whether the flag
        # was passed.
        window=(settings.window if getattr(args, "window", None) is None
                else args.window),
        min_interval=(
            settings.min_interval
            if getattr(args, "min_interval", None) is None
            else args.min_interval
        ),
        timeout=getattr(args, "timeout", None) or settings.timeout,
        record_dir=record,
        replay_dir=replay,
        force_record=getattr(args, "force", False),
        allow_mixed_sources=getattr(args, "mixed_sources", False),
        max_calls=getattr(args, "max_calls", None) or settings.max_calls,
        dry_run=getattr(args, "dry_run", False),
        use_cache=cache_choice(args, settings),
        sample=getattr(args, "sample", None) or settings.sample,
    )


ALLOWED_SCHEMES = ("http", "https")


def check_base_url(settings: Settings) -> None:
    """Refuse a base URL that is not an http(s) endpoint. Before any client.

    `urllib.request.build_opener` installs `FileHandler`, `FTPHandler` and
    `DataHandler` from its defaults, and this project only ever passed it an
    `HTTPSHandler` -- so `LLOSSLESS_BASE_URL=file:///etc/passwd` survived
    `with_api_path` (it has a path), `FileHandler` returned the file's bytes as
    the response body, and the parser read a local file as a model answer.

    **The suite's network guard cannot see this**, and that is the interesting
    half. It refuses a socket to anywhere but the configured endpoint; a
    `file://` read opens no socket at all. The constraint was enforced one layer
    above the layer where the route exists, which is why a check that has been
    green for the life of the project was green over this too.

    A hostname is required as well. `file:///etc/passwd` has none, and neither
    does anything else worth refusing here.

    **Every configured endpoint, not only the run-wide one.** `Settings` has
    held a role-to-URL map since per-role endpoints landed, and this function
    read `base_url` alone -- so `LLOSSLESS_BASE_URL_MERGE=file:///etc/passwd`
    walked straight past the check written to stop exactly that, because the
    role map was added after the guard and nothing tied the two together. A
    guard that inspects one field of an object that can carry three addresses
    is a guard over one third of its own subject. `addresses()` is the list,
    and it is derived from the settings rather than restated, so a fourth place
    an address can come from is covered by construction.
    """
    for role, url in addresses(settings):
        where = "base URL" if role is None else f"base URL for {role}"
        variable = ("LLOSSLESS_BASE_URL" if role is None
                    else f"LLOSSLESS_BASE_URL_{role.upper()}")
        parsed = urlsplit(url)
        if parsed.scheme not in ALLOWED_SCHEMES:
            raise ConfigError(
                f"{where} scheme {parsed.scheme or '(none)'!r} is not supported. "
                f"LLossless talks to an HTTP endpoint: use http:// or https://. "
                f"A {parsed.scheme or 'schemeless'} URL would be read by urllib as "
                f"a local resource and its bytes parsed as a model answer.")
        if not parsed.hostname:
            raise ConfigError(
                f"{where} {url!r} names no host. "
                f"Set {variable} to the endpoint's address.")


def addresses(settings: Settings) -> list[tuple[str | None, str]]:
    """Every endpoint this run can talk to, as (role, URL). The run-wide one first.

    `None` is the run-wide `base_url`, matching `base_url_for`'s own argument,
    and every role that has an endpoint of its own follows it in name order. A
    role with no override is not repeated: it resolves to `base_url`, which is
    already the first entry, and listing it again would make a single-endpoint
    run report the same refusal three times.

    Exists so that the two guards below cannot disagree about what "every
    configured endpoint" means, and so that neither of them has to know how the
    map is spelled.
    """
    seen = [(None, settings.base_url)]
    for role in sorted(settings.endpoints):
        url = settings.endpoints[role]
        if url != settings.base_url:
            seen.append((role, url))
    return seen


def is_loopback(hostname: str) -> bool:
    """Loopback by name or by address, including the `.localhost` suffix.

    RFC 6761 reserves `localhost` *and* everything under it, and a developer
    running two endpoints as `a.localhost` and `b.localhost` is doing an
    ordinary thing. `LOCAL_HOSTS` covers the exact spellings; this adds the
    suffix, and nothing else.
    """
    host = (hostname or "").lower()
    return host in LOCAL_HOSTS or host.endswith(".localhost")


def check_cleartext_key(settings: Settings) -> None:
    """Refuse to send a bearer token over cleartext to a host off this machine.

    `transport.py` set `Authorization` whenever a key was present, with no
    reference to the scheme, so `LLOSSLESS_BASE_URL=http://a-rented-pod:8000/v1`
    plus a key in the environment put the token on the wire in the clear, once
    per call, for anyone on the path.

    **Refused, not warned**, on the same reasoning that leaves this project
    without an `--insecure` flag (`transport._tls_context`): an escape used more
    often than the situation that justifies it is not a safety valve. It is also
    what `_RefuseRedirects` already does for the other half of this threat --
    that class was written because a redirect is how a token reaches a host
    nobody configured, and it would be odd to refuse the redirect and permit the
    first hop.

    Loopback is carved out and has to be: `DEFAULT_BASE_URL` is
    `http://localhost:11434/v1`, local ollama takes no key, and a developer who
    exports one for something else must not find the local default broken.

    Nothing in the current or planned configuration trips this. The recorded pod
    was cleartext `http` on a public address and ollama takes no key, so the two
    halves have never been true at once. It goes live the first time a hosted
    endpoint wants a token, and the answer then is the provider's `https` proxy
    URL, never a bypass.

    **Per role, over every configured endpoint**, for the reason `check_base_url`
    now does: the key a role sends is `api_key_env_for(role)` and the host it
    sends it to is `base_url_for(role)`, and a check that paired the run-wide
    key with the run-wide host answered a question about a configuration that
    may not be the one any call is made under. A frontier merge beside a local
    decompose is exactly the split this project ships for, and it is the split
    where the two halves first differ.
    """
    for role, url in addresses(settings):
        parsed = urlsplit(url)
        if parsed.scheme != "http" or is_loopback(parsed.hostname or ""):
            continue
        if not settings.api_key(role):
            continue
        variable = settings.api_key_env_for(role)
        where = "the base URL" if role is None else f"the base URL for {role}"
        raise ConfigError(
            f"refusing to send an API key in cleartext to {parsed.hostname}. "
            f"{variable} is set and {where} is http://, so the "
            f"token would go on the wire unencrypted on every call. Use the "
            f"endpoint's https:// address -- a hosted provider has one, and it is "
            f"the answer rather than a way round this. If the key is not meant for "
            f"this endpoint, unset {variable}.")


def resolve(
    args=None,
    environ: dict[str, str] | None = None,
    offline_dir: Path = OFFLINE_CASSETTES,
) -> Settings:
    # The flag's window goes in with the environment, not after it: the pair
    # the window refusal checks can arrive split across the two, and the
    # refusal runs on every `Settings` built, including the first.
    settings = from_env(environ, window=getattr(args, "window", None))
    if args is not None:
        settings = apply_arguments(settings, args, offline_dir)
    # After argument handling, because both halves of this decision can move
    # there: `--fidelity sourced` and `--answer-with` are flags, and a guard
    # that read the environment's answer would be guarding a run that is not
    # the one about to happen.
    #
    # The grant and then the refusal, in `at_fidelity`, which is also what
    # `sweep.settings_for` calls for every row of `--sweep-fidelity`: one
    # owner, so a sweep row cannot be granted or refused differently from a
    # run at its level. The function is at the foot of this module.
    settings = at_fidelity(settings, settings.fidelity)
    # **The effort level is not appended here.** It used to sit beside the
    # grant, which was right while one level covered the run; it is per role
    # now, and a role is not known until a call is about to be made. So
    # `Settings.command_for` appends it and `settings.command` stays the route
    # -- the operator's program plus the grant, which really is one per run.
    # The two are still one writer each and both are still idempotent.
    # Here for the same reason the refusal above is, and one step further: the
    # command can arrive from the environment or from `--answer-with`, and the
    # envelope only from the environment, so the pair is only whole once both
    # have been read. `web/commands._row` refuses this on a route before a job
    # is ever built; this is the same rule on the command line, which had none
    # at all.
    refusal = envelope_refusal(settings.command_envelope, settings.command)
    if refusal is not None:
        raise ConfigError(refusal)
    # After argument handling, because `--base-url` can replace what the
    # environment gave, and validating the one that loses is validating nothing.
    check_base_url(settings)
    # After `check_base_url`, so a `file://` URL is refused for being a local
    # read rather than for the key it does not carry.
    check_cleartext_key(settings)
    return settings


# `sourced`'s second refusal and the two predicates it rests on. At the
# foot of the module rather than beside `retrieval_refusal`, which reaches
# them by name at call time: other files cite line numbers in this one, and
# three functions added above those lines would have moved every citation.
def reports_retrieval(command: str) -> bool:
    """Whether a run through this command can say afterwards if it retrieved.

    The only answer this build has to "did the model retrieve" is `num_turns`,
    and the only envelope that carries it is `claude --print`'s result
    envelope. A command answering in plain text returns the model's words and
    nothing about how many turns they took, so every call through it is
    `unmeasured` on retrieval -- and the report cannot tell a reader whether
    the citations it prints were looked up. Read off the argv, as the grant
    is, because the argv is what the program will be asked; `envelope_refusal`
    already holds the declared envelope to it.
    """
    return carries_result_args(_argv(command))


def sourced_tools(command: str) -> tuple[str, ...]:
    """The web tools a `sourced` run through this command would get, or ().

    `retrieval_tools`, narrowed to a command that can also report whether they
    were used. Empty means `sourced` refuses this command, for either
    reason; what a route row serves as its retrieval marker, so the picker
    does not advertise retrieval on a route the level will refuse.
    """
    return retrieval_tools(command) if reports_retrieval(command) else ()


def _measurement_refusal(command: str) -> str | None:
    """Why this command could retrieve and could not say whether it did.

    The second half of `retrieval_refusal`, and the half an operator met
    without being told: their routes predated the result envelope, every call
    through them was `unmeasured`, and the report looked normal for hours.
    `sourced` promises the reader an answer to "was this looked up", and a
    command that cannot carry the answer turns that promise into recall
    wearing citations -- which is the outcome the first half refuses.
    """
    if reports_retrieval(command):
        return None
    program = os.path.basename((_argv(command) or [""])[0]) or "that program"
    both = " ".join(RESULT_ARGS)
    return (
        f"--fidelity {SOURCED} has to report whether the model retrieved "
        f"anything, and {program!r} is asked to answer in plain text, which "
        f"carries no turn count -- so every run through it would report "
        f"retrieval as unmeasured and print its citations as though they might "
        f"have been checked. Add `{both}` to the command and set "
        f"LLOSSLESS_COMMAND_ENVELOPE={ENVELOPE_RESULT} (on the web server, "
        f"the route's `envelope` is `{ENVELOPE_RESULT}`), or use "
        f"--fidelity open.")


def at_fidelity(settings: "Settings", level: str) -> "Settings":
    """These settings at one fidelity level, granted and refused as a run there is.

    **The one owner of `sourced`'s grant-then-refuse step.** `resolve`
    reaches a run's level through here, and `sweep.settings_for` reaches every
    row of `--sweep-fidelity` through here. The sweep used to swap the level in
    with a plain `replace`, so its `sourced` row met neither half: over an
    HTTP endpoint it ran unrefused and answered from recall under the
    `sourced` label, and through `claude` it was granted no tool.

    The grant is applied first and the refusal is read off the *result*, so
    what is checked is what the run will really be permitted rather than what
    it was configured with. `command_with_retrieval` is idempotent, so the
    web path -- which reaches `resolve` with a route's own command already in
    the environment -- appends once however often it is resolved.

    Raises `ConfigError` carrying `retrieval_refusal`'s reason. At the foot of
    the module for `reports_retrieval`'s reason: other files cite lines above.
    """
    moved = replace(settings, fidelity=level)
    if canonical_fidelity(level) == SOURCED:
        moved = replace(moved, command=command_with_retrieval(moved.command))
    refusal = retrieval_refusal(moved.fidelity, moved.command)
    if refusal is not None:
        raise ConfigError(refusal)
    return moved


# The subscription CLI's isolation, at the foot for `reports_retrieval`'s
# reason: other files cite lines above.
#
# **A document-merging tool must not inherit its operator's agent setup, and
# must not use tools it was not granted.** `claude --print` loads the user's
# own `~/.claude/CLAUDE.md`, their auto-memory, skills, plugins, hooks and MCP
# servers, and offers the model its whole built-in tool set whatever
# `--allowed-tools` says: the allowlist decides what runs without a prompt, not
# what exists. Measured on 2026-09-25 through CLI 2.1.274, `--model haiku`, from
# this repository's directory: asked whether it had user- or project-level
# instructions, the model answered yes and named two files; its `system/init`
# event listed 30 built-in tools, `Task` and `Bash` among them, and 8 MCP
# tools. Testing had seen one Opus merge spawn two subagents through that `Task`.
#
# With `--safe-mode` it answered no and named nothing, and with `--tools`
# naming the grant the tool list was exactly the grant: `WebFetch` and
# `WebSearch` at `sourced`, and empty under `--tools ""`, with no MCP tool
# either way. `--bare` is not used: it never reads the subscription's OAuth.
#
# Keyed by the program's basename, like `AUTO_GRANT` and `AUTO_EFFORT`, and
# for their reason: a wrapper script's flags are not read here, and appending
# one it does not take breaks a working route rather than narrowing it. That
# is also the one way out of safe mode, which has no negating flag.
SAFE_MODE_FLAG = "--safe-mode"
TOOLS_FLAG = "--tools"
# `claude --help` at 2.1.274: *"Use "" to disable all tools, "default" to use
# all tools, or specify tool names"*. A route that says `default` has asked for
# every tool, and is read as no restriction at all.
TOOLS_DEFAULT = "default"
ISOLATED: frozenset[str] = frozenset({"claude"})


def stated_tools(command: str) -> tuple[str, ...] | None:
    """The tools this command line's own `--tools` names, or None where it has none.

    `granted_web_tools`' reader for the neighbouring flag: both spellings, both
    separators, up to the next flag, every occurrence. An empty tuple is a
    statement -- `--tools ""`, no tool at all -- and None is its absence, and
    the two are never folded together, because only the second leaves the
    choice to this build.
    """
    argv = _argv(command)
    named: list[str] | None = None
    for index, item in enumerate(argv):
        if item == TOOLS_FLAG:
            values = argv[index + 1:]
        elif item.startswith(f"{TOOLS_FLAG}="):
            values = [item.split("=", 1)[1]]
        else:
            continue
        named = [] if named is None else named
        for value in values:
            if value.startswith("-"):
                break
            named.extend(part.strip() for part in value.split(",") if part.strip())
    return None if named is None else tuple(dict.fromkeys(named))


def _available(command: str, tools: tuple[str, ...]) -> tuple[str, ...]:
    """`tools`, less any the command's own `--tools` leaves out.

    No `--tools`, or `--tools default`, restricts nothing. Otherwise a tool is
    available only when it is named there, and a permission for one that is not
    is a permission for nothing -- which `granted_web_tools` must not report.
    """
    named = stated_tools(command)
    if named is None or TOOLS_DEFAULT in named:
        return tools
    return tuple(tool for tool in tools if tool in named)


def command_with_isolation(command: str) -> str:
    """This command line with the CLI's isolation on it. Idempotent.

    The one writer, reached through `Settings.command_for` for every call, on
    `command_with_retrieval`'s rules: only for a program in `ISOLATED`, and
    never beside or over a flag the operator wrote.

    - `--safe-mode`, unless the argv already carries it.
    - `--tools`, naming exactly the web tools this argv grants, unless the argv
      already carries a `--tools`. At `sourced` that is the automatic grant,
      `WebSearch,WebFetch`; at every other level it is `""` -- no tool --
      unless the operator's own route grants one, which stays in force at
      every level, as the route caveat on the page says it does.

    An operator's own `--tools` is theirs: it is never widened, never narrowed
    and never appended beside. What it leaves out is not granted
    (`granted_web_tools`), so `sourced` refuses a route whose `--tools` makes no
    web tool available rather than labelling recall as retrieval.

    Idempotent by construction: once both flags are readable off the argv
    there is nothing to append, and the string comes back unchanged.
    """
    argv = _argv(command)
    if not argv or os.path.basename(argv[0]) not in ISOLATED:
        return command
    extra: list[str] = []
    if SAFE_MODE_FLAG not in argv:
        extra.append(SAFE_MODE_FLAG)
    if stated_tools(command) is None:
        extra += [TOOLS_FLAG, ",".join(granted_web_tools(command))]
    return shlex.join([*argv, *extra]) if extra else command


# Environment variable names, and prefixes, `backend._child_env` drops from
# a command backend's child process, and what `Provenance` reports
# was dropped (`isolation.<role>.env_dropped`). Defined here, not in
# `backend.py`: this module is imported at module scope by every run
# including a pure replay, and `backend.py` imports `transport`, which a
# replay must never load (`acceptance_replay_never_loads_the_transport_module`).
# A `Provenance` that imported `backend` merely because a command *was
# configured*, regardless of whether this run made a live call, would break
# that guarantee for a replay of a command-backend corpus; reading these two
# names from here instead means neither module has to.
#
# `ANTHROPIC` and `OPENAI`: no trailing underscore, on purpose -- an API key
# present as either bare name or with a suffix (`ANTHROPIC_API_KEY`) would
# make the CLI bill the metered API instead of the subscription this backend
# exists to reach, and it would leak that key to a program this project does
# not control.
#
# `OPEN_AI`, `GOOGLE_AI`, `GOOGLE_API_KEY` and `GEMINI`: another vendor's
# API key. The web interface stores provider keys under `OPEN_AI_API_KEY` and
# `GOOGLE_AI_API_KEY`, which the two prefixes above do not match, and a
# subscription program for one vendor has no use for another vendor's key.
#
# `LLOSSLESS_` and the retired prefix it replaced: this tool's own
# configuration, meaningless to the program being run.
#
# `CLAUDECODE`, `CLAUDE_CODE_` and `CLAUDE_AGENT_`: the Claude Code session
# this process may itself be running inside of -- confirmed against this very
# process's own environment, which carries `CLAUDECODE`, nine `CLAUDE_CODE_*`
# names, `CLAUDE_AGENT_SDK_VERSION` and the bare `CLAUDE_PID`.
# `CLAUDE_CODE_EFFORT_LEVEL` is one of this family and the 2.1.283 binary
# reads it to override `--effort`, which would make the argv's own flag a lie
# the report could not see. `CLAUDE_EFFORT`, `CLAUDE_PID` and `AI_AGENT`
# (bare, not only a suffixed form) are the same class of fact by other names.
DROPPED_ENV_PREFIXES = ("ANTHROPIC", "OPENAI", "OPEN_AI", "GOOGLE_AI",
                        "GOOGLE_API_KEY", "GEMINI", "LLOSSLESS_", "CLAIMCHECK_",
                        "CLAUDE_CODE_", "CLAUDE_AGENT_", "AI_AGENT")
DROPPED_ENV_NAMES = frozenset({"CLAUDECODE", "CLAUDE_EFFORT", "CLAUDE_PID"})

# A later fix: the
# `CLAUDE_CODE_` prefix above was written to catch session and effort
# markers, but it also caught `CLAUDE_CODE_OAUTH_TOKEN` -- the credential a
# headless user sets (`export CLAUDE_CODE_OAUTH_TOKEN=<token>`, the exact
# line `claude setup-token` prints, also the variable the CLI's own GitHub
# Actions example names: `claude_code_oauth_token: ${{ secrets.
# CLAUDE_CODE_OAUTH_TOKEN }}`) to log the CLI into their subscription without
# an interactive login. Dropping it made the subscription route unusable for
# exactly the users it exists for. Confirmed against the installed 2.1.283
# binary's own strings, not guessed: the login flow prints that export line
# verbatim, and the auth-state debug dump lists `CLAUDE_CODE_OAUTH_TOKEN=`
# beside `ANTHROPIC_API_KEY=` and `ANTHROPIC_AUTH_TOKEN=` as the credential
# slots it checks. A sibling refresh-token flow exists too
# (`CLAUDE_CODE_OAUTH_REFRESH_TOKEN` with `CLAUDE_CODE_OAUTH_CLIENT_ID` and
# `CLAUDE_CODE_OAUTH_SCOPES`), but it is not what `claude setup-token` or the
# documented CI recipe use, and this fix stays scoped to the credential the
# bug named. Kept, not merely un-dropped: it must never appear in
# `for_report=True`'s names either, the same as any other name this function
# never puts in `DROPPED_ENV_NAMES` or the prefixes -- a name in this set
# skips both regardless of `for_report`, so the credential is invisible to
# `env_dropped` rather than merely present with `for_report` narrowing it.
KEPT_CREDENTIAL_NAMES = frozenset({"CLAUDE_CODE_OAUTH_TOKEN"})

# `env_dropped` follow-up, found comparing the two spellings of the
# command setting: `LLOSSLESS_*` is dropped from the child either way, but it
# is this tool's own configuration, consumed on purpose, not a foreign
# credential or session variable withheld from a program that never asked for
# it. Reporting it made two runs that differ only in how the command was
# spelled -- `--answer-with PROGRAM` against `LLOSSLESS_COMMAND=PROGRAM` --
# produce two different `env_dropped` lists for what is otherwise one
# setting, because only the env spelling puts `LLOSSLESS_COMMAND` itself into
# `os.environ` for the filter to see. The old prefix stays reported: it is the
# retired name for the same configuration, so a value found under it is a
# leftover from before the rename, not this run's own configuration, and is
# exactly the kind of thing the report exists to name.
REPORT_EXEMPT_PREFIXES = ("LLOSSLESS_",)


def dropped_env_names(environ: dict | None = None, *, for_report: bool = False) -> list[str]:
    """Which names in `environ` (default `os.environ`) a command backend withholds.

    A pure function of the environment and never of one call: the filter
    never varies by role or by command, so both `backend._child_env` (which
    builds the child's real environment, `for_report=False`, the default) and
    `Provenance` (which only ever reports the names, `for_report=True`) call
    this one function rather than keeping two lists in step by hand. Sorted,
    and names only -- never a value, which is the whole point for the ones
    this exists to keep out of a report.

    `for_report` narrows the prefixes, never the names dropped from the
    child: `LLOSSLESS_*` is left out of what is reported, not out of what
    `_child_env` withholds.

    `KEPT_CREDENTIAL_NAMES` narrows the other way and unconditionally: a name
    in that set is never returned, `for_report` or not, because it is not
    withheld from the child at all (see that set's own comment).
    """
    source = os.environ if environ is None else environ
    prefixes = DROPPED_ENV_PREFIXES
    if for_report:
        prefixes = tuple(prefix for prefix in DROPPED_ENV_PREFIXES
                         if prefix not in REPORT_EXEMPT_PREFIXES)
    return sorted(
        name for name in source
        if (name in DROPPED_ENV_NAMES or name.startswith(prefixes))
        and name not in KEPT_CREDENTIAL_NAMES
    )


def command_safe_mode(command: str) -> bool:
    """Whether `--safe-mode` is on this argv, read the way `stated_tools` reads `--tools`.

    Off the string directly rather than off membership in `ISOLATED`: an
    argv this build isolated carries the flag because `command_with_isolation`
    wrote it, and an operator's own wrapper can carry it too (the "one way
    out of safe mode" is starting a differently-named program with the flag
    already on its own argv) -- both are `True` here, on the same evidence
    `Provenance` reports the rest of a run from.
    """
    return SAFE_MODE_FLAG in _argv(command)


def only_web_tools(command: str) -> bool:
    """Whether this argv leaves the model no tool but the web tools.

    What decides how many turns a call can take without retrieving. Under the
    shipped argv `WebFetch` and `WebSearch` are deferred and loaded through
    `ToolSearch`, so one retrieval is three turns and a plain answer may be two.
    Under `--safe-mode` and a `--tools` naming web tools alone there is
    no `ToolSearch`, no hook and no other tool, so any turn past the first is a
    web tool call: measured, one fetch and one search are two turns each.

    True only for a program in `ISOLATED` that carries `--safe-mode` and a
    `--tools` naming nothing else. An operator's own `--tools default`, or one
    naming another tool, keeps the older floor, which errs low.
    """
    argv = _argv(command)
    if not argv or os.path.basename(argv[0]) not in ISOLATED:
        return False
    named = stated_tools(command)
    return (SAFE_MODE_FLAG in argv and named is not None
            and set(named) <= set(WEB_TOOLS))


def tools_withhold_the_grant(command: str) -> bool:
    """Whether a grant exists here but the argv's own `--tools` makes it void.

    The operator's allowlist, or failing that the automatic grant, names a web
    tool, and a `--tools` of their own leaves every one of them out. `sourced`
    refuses that command, and says why in these terms rather than in the terms
    of a program this build does not know.
    """
    argv = _argv(command)
    if not argv or stated_tools(command) is None:
        return False
    wanted = (granted_web_tools(command, raw=True)
              or AUTO_GRANT.get(os.path.basename(argv[0]), ()))
    return bool(wanted) and not _available(command, wanted)


def _grant_refusal(command: str) -> str | None:
    """`retrieval_refusal`'s answer for a program this build can grant.

    Two ways it still cannot answer at `sourced`: the command's own `--tools`
    makes no web tool available, or it cannot say afterwards whether it
    retrieved (`_measurement_refusal`).
    """
    if retrieval_tools(command):
        return _measurement_refusal(command)
    program = os.path.basename((_argv(command) or [""])[0]) or "that program"
    return (
        f"--fidelity {SOURCED} needs a web tool the model can use, and this "
        f"command's own {TOOLS_FLAG} makes none available to {program!r}: a "
        f"tool granted by {ALLOW_TOOLS_FLAG} but left out of {TOOLS_FLAG} does "
        f"not exist for the model. Add {','.join(WEB_TOOLS)} to its "
        f"{TOOLS_FLAG}, or drop {TOOLS_FLAG} and let this build name the web "
        f"tools itself, or use --fidelity open.")


def effort_from_env(env) -> dict[str, str]:
    """`LLOSSLESS_EFFORT` then `LLOSSLESS_EFFORT_<ROLE>`, as role -> level.

    `from_env`'s reading, moved out so the web server can say what a request
    that names no level would get without resolving a whole `Settings`
    for it. The run-wide variable is laid down first and a per-role one
    overwrites it: `LLOSSLESS_WINDOW`'s relationship to its per-role form.
    """
    env = os.environ if env is None else env
    effort: dict[str, str] = {}
    run_wide = env.get("LLOSSLESS_EFFORT", "").strip().lower()
    if run_wide:
        if run_wide not in EFFORT_LEVELS:
            raise ConfigError(
                f"LLOSSLESS_EFFORT={run_wide!r} is not one of "
                f"{', '.join(EFFORT_LEVELS)}")
        effort = dict.fromkeys(ROLES, run_wide)
    for role in ROLES:
        suffix = role.upper()
        level = env.get(f"LLOSSLESS_EFFORT_{suffix}", "").strip().lower()
        if level:
            if level not in EFFORT_LEVELS:
                raise ConfigError(
                    f"LLOSSLESS_EFFORT_{suffix}={level!r} is not one of "
                    f"{', '.join(EFFORT_LEVELS)}")
            effort[role] = level
    return effort
