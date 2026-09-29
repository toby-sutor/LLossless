"""Which programs this server may answer a merge with. The operator's list, on disk.

`backend.py` is the second way a request can be answered: a program, the prompt
on its stdin, the answer on its stdout (483). On the command line that is
`--answer-with`, and it is safe there for a reason worth writing down --
whoever types a flag already has a shell, so naming a program is not an
escalation. **A web form is not in that position.** A field that accepts a
command and a server that runs it is remote code execution with a submit
button on it, and no amount of validating the string makes it something else.

So the string never crosses the network. This module is the allowlist that
replaces it: the operator writes the routes into a file that only they can
write, the page is served their *labels*, and a request names one by **id**.
The server looks the id up and supplies the command from its own file. A
submitter chooses among the operator's routes; they never describe one. That is
the same sentence `jobs.endpoint_plan` already makes about addresses, one
mechanism over, and it is not a coincidence: both are the case where the thing
being chosen is dangerous to describe and harmless to name.

**Empty is the default, and it is the default twice.** There is no file until
an operator writes one, and `server.build` is handed no store unless its caller
asks for one -- so a library embedding this, and every server the suite binds,
offers no command backend at all. A capability that runs a program has to be
switched on deliberately, in a place a request cannot reach.

**The browser may switch a route on. It may never describe one.** The first
version of this module wrote that nothing writes the file, and the operator's
answer to it was *"Is this only available in the tool config or can this also
be done in the WebUI (preferably)?"* -- which is a fair complaint about the
experience and not an argument about the security property. The property is
that **no text a browser supplies becomes part of a command**, and hand-editing
a file was never what enforced it.

So there is a second way to populate the same allowlist, and it inverts where
the string comes from. `KNOWN_TOOLS` is a hard-coded table of subscription CLIs
this build recognises; `Commands.discovered` looks each one up on `PATH` and in
`EXTRA_BIN_DIRS` and reports what it found; `Commands.enable` writes a route
whose command is **the path this server resolved** followed by **argv this
table wrote**, under a label **this module** wrote, for an id that has to be
one of the table's. A request carries the id of something the server already
found, which is the same sentence the `get` path makes one mechanism over.
There is no branch anywhere below where a submitted string reaches a command
line.

**One tool becomes several routes, and every one of them names its model.**
The operator's second complaint was that a discovered `claude` ran whatever
the CLI defaults to: *"It is not clear which one would be used. Relying on the
app default is not strategy. I don't wanna use the most expensive model Fable
for such tasks."* So `KnownTool.models` declares the models the tool can be
told to use and the exact argv that tells it, discovery emits one route per
model, and `_row` **refuses a route that states none** -- a hand-written one
as well as a discovered one. That last part reverses half of 517, which let
the model be omitted and recorded the run under the route id. The name was
honest and the run was not: the program still used its own default and nobody
could see which.

**`PATH` is where a server looks, not where a tool is.** The first version of
discovery was `shutil.which` and nothing else, on the argument that a table of
directories would be a guess about somebody's filesystem. That argument is
sound about *which program* may run and wrong about *where to look for it*: a
per-user CLI installs itself into `~/.local/bin`, a daemon's `PATH` is whatever
its unit file says, and the operator's own report was a page saying a tool it
could see was not there. So `EXTRA_BIN_DIRS` is checked after `PATH`, and the
security property is untouched -- the table still decides which *names* are
acceptable, the browser still sends only an id, and no browser-supplied text
reaches argv. Widening where a known name is looked for is not widening what
may be run.

**One unusable row must not take out the usable ones.** `read()` refused the
whole file on any bad row, and `describe()` turned that into an empty list --
so a single stale row emptied the picker, and the operator met a page-level
wall of text about a file they had never written. A row is the unit now:
`load()` returns the rows this build can use beside an `Unusable` for each one
it cannot, `describe()` serves the first, the page shows the second next to
nothing at all, and `_write` copies an unusable row back out verbatim rather
than dropping it. The refusal still binds -- `get` raises that row's own
reason for that row's own id -- it just stops binding rows it was never about.

**A row this page wrote, this page retires.** 526 made an unstated model a
refusal, which turned every route the *pre-526* discovery code had written into
an unusable row: `discovered: true`, the tool's id, no model. Asking the
operator to hand-edit a file they never hand-wrote is not an answer, so
`migrate()` drops exactly that shape at startup and `retired` says so on the
page once. It is narrow on purpose and `Route.discovered` is what makes it
narrow: a row without that flag is the operator's, and this module does not
touch it whatever state it is in. Retired rather than rewritten, because the
old row ran whatever the CLI defaults to and there is no honest mapping from
that to one of four aliases -- choosing one here would be the guess the whole
milestone exists to refuse. What the operator gets back is four available rows
and one tick.

Two stores were the obvious alternative and would have been wrong. There is one
allowlist with two ways to fill it: the operator's own rows and the discovered
ones, told apart by `Route.discovered`, in one file, read by one `get`. A
second store would have meant a second lookup, and a second lookup is a second
chance to answer a request from the wrong list.

**Discovery never edits a row it did not write.** `Route.discovered` is the
whole of that guard: `enable` refuses an id the operator already used for a
route of their own rather than overwriting it, and `disable` refuses to delete
one. The page can turn its own rows on and off and cannot touch the file's.

**And it is never per-account.** `accounts.Directory` gives each account its own
`credentials.json`, which is what makes a key per-user -- and putting commands
in that file would have made "add a command" a thing any account holder could
do through their own settings sheet. This is a separate file, read once per
server, shared by everybody on it. The consequence is the first of the three
things the page has to say out loud: a command runs as the server process with
that machine's credentials, so on a shared instance everybody shares one
subscription and one rate limit.

**The mode check is about writing, not reading.** `credentials.py` refuses a
file wider than `0600` because every account on the box has already had the
chance to *read* a key. Here the exposure runs the other way: a file another
account can write is a file in which they choose what this server executes.
Both are refusals of the same mode for opposite reasons, which is why the
refusal here says so rather than reusing the other's sentence.

**A window is required on every route.** `config.Settings.__post_init__`
already refuses a command backend that has not been told its context window,
for every role, because there is no `/api/ps` to ask and no token count to
check afterwards. Requiring it here turns that refusal from something an
operator meets forty minutes into a run into something they meet when they
write the file.

**A timeout is optional on every route, and this is the only place a web
submitter can be given one.** There is no `--timeout` on a form, so the route
carries it: unstated means the default a command backend resolves for itself
(`config.COMMAND_TIMEOUT`), and a route whose program is slower than that
states its own seconds. Optional where the window is required, because the two
are different kinds of missing -- an unstated window leaves a run with no guard
at all, an unstated timeout leaves it with a measured default (533).

**The command is never served, and the label is never inferred.** A command is
a local path as often as not -- `internal/tests/scan_release.py` scans the
published set for exactly that shape -- so `describe()` answers with the id,
the label and the route's own settings, and there is no route on this server
that returns the string. The label is whatever the operator wrote, rendered
verbatim, because guessing that `claude` means Opus 5 is how a correct-looking
screen produces a wrong bill.

**That rule binds discovery twice over.** What `shutil.which` answers with is
an absolute path under whichever account this server runs as, which is the
exact shape `scan_release.py` refuses and which already cost this feature one
fixture (522). So the resolved path is held in the store and in the file and
goes into **no** payload: `discovered()` answers with an id, a label, whether
it was found and whether it is on, and there is nothing on it a reader could
reconstruct a path from. The label comes from the table rather than from the
program, for the same reason the operator's label does: this module knows that
a binary called `claude` is Anthropic's CLI, and it does not know which model a
subscription behind it answers with.
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import shlex
import shutil
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .. import config as config_web
from ..config import COMMAND_ENVELOPES, COMMAND_TIMEOUT, ENVELOPE_RAW, ENVELOPE_RESULT, ROLES
from ..structured import PROFILES

# The model's own web tools, by the name the CLI's allowlist flag takes, and
# what each costs to permit (537).
#
# **Neither is written into a route, and below `sourced` neither is on.** A
# `claude --print` call with no allowlist says in the text that it needs
# permission and searches nothing, so a route this build writes answers from
# what the model knows. At `sourced` both are granted automatically on the
# argv a run executes (`config.AUTO_GRANT`, 578), and never in the file.
#
# **Two entries rather than one switch, because the risk differs.** This
# tool's entire input is documents somebody supplied, and the prompts already
# tell the model that content inside them is data and not instructions.
# `WebFetch` takes a URL, and a document is a place a URL can come from -- a
# hostile or merely careless source carrying one is a route to both
# exfiltration and to poisoned "evidence" that arrives looking like a citation.
# `WebSearch` sends a query to a search engine and is harder to aim at a chosen
# destination. The automatic grant carries both, on the operator's ruling that
# transparency is the answer; an operator who wants one writes it into the
# route's argv, and a grant already there is never widened.
#
# A closed table for the reason `KNOWN_TOOLS` is one: this is the only source
# a tool name in an argv can come from, so there is no expression anywhere
# that joins a submitted string to an allowlist flag.
#
# **The table moved to `config` and the names did not** (548). `sourced` is a
# fidelity level, so the command line reaches this decision too, and `config`
# is the module both paths already import -- this one imports it and nothing in
# it may import this one. Re-exported under the names this module has always
# used, so every reference below and every comment above stays true, and there
# is still exactly one place a tool name is written down.
WEB_SEARCH = config_web.WEB_SEARCH
WEB_FETCH = config_web.WEB_FETCH
WEB_TOOLS = config_web.WEB_TOOLS

# The flag the allowlist goes in, spelled the way `claude --help` spells it at
# 2.1.274: *"--allowedTools, --allowed-tools <tools...>"*, comma or space
# separated. The long form, for `--print`'s reason one table down -- the argv
# is read back by a check and a reader comparing the two should not have to
# know they are one flag.
#
# `--permission-mode` is deliberately not used. Its choices grant far more
# than retrieval, and an allowlist naming two tools is the narrow instrument.
#
# Re-exported from `config` for the reason the tool names above are.
ALLOW_TOOLS_FLAG = config_web.ALLOW_TOOLS_FLAG

# The flag and the value that make a command answer with a result envelope, and
# the reader that tells whether an argv asks for one. `KNOWN_TOOLS`'s
# `result_args` is built from these rather than repeating them, so the check
# below and the argv it reads cannot drift apart -- which is the failure this
# whole pair exists to stop.
#
# Moved to `config` and re-exported here, exactly as the tool names above were
# and for the same reason: the command line needs this rule too, `config` is
# the module both paths already import, and a second implementation of one
# rule is a second answer to it (555). The names stay as this module has
# always spelled them, so every comment below and every test that reads them
# still means what it says.
RESULT_FORMAT_FLAG = config_web.RESULT_FORMAT_FLAG
RESULT_FORMAT_VALUE = config_web.RESULT_FORMAT_VALUE
RESULT_ARGS = config_web.RESULT_ARGS
_carries_result_args = config_web.carries_result_args

# The profile a route gets when it does not name one. `subscription` is the
# profile that exists for this backend: one rung, no `temperature`, no `seed`,
# because there is no request body to put them in (483). Naming a different one
# is permitted -- an operator's wrapper may genuinely constrain output -- and
# it is their explicit choice rather than this module's guess.
DEFAULT_PROFILE = "subscription"

# The tier every published figure in this project was measured at. A route
# whose profile cannot reach it is a route whose runs are comparable to none of
# them, and `describe()` says so as a boolean rather than leaving a page to
# work it out from a profile name.
PUBLISHED_TIER = "json_schema"

# What an id may be. Lowercase, digits, hyphen and underscore, starting with an
# alphanumeric, and short. An id travels in a JSON body and comes back in a
# refusal message, and it is the one part of a route a submitter may name -- so
# it is held to a shape that cannot be a path, cannot be a URL, and cannot
# carry a line break into a log. Checked on read as well as on lookup, because
# an id that only the file could hold would be an id no request could reach.
ROUTE_ID = re.compile(r"\A[a-z0-9][a-z0-9_-]{0,63}\Z")

# A label is shown to a person and rendered into the run's own banner, so it is
# held to the same two rules a document label is: long enough for a sentence,
# no control characters.
MAX_LABEL = 200

# Above this a command is a paste rather than a command line.
MAX_COMMAND = 4096

# What the file says it is. A version rather than a bare mapping, for the
# reason `credentials.SCHEMA_VERSION` gives: a later shape is then recognised
# and refused with a sentence instead of guessed at and read wrong.
SCHEMA_VERSION = 1
READABLE_SCHEMA_VERSIONS = (1,)

FILE_NAME = "commands.json"

# Owner, and nobody else, on the file and on the directory holding it. A
# directory another account can write is a directory in which the file can be
# replaced.
FILE_MODE = 0o600
DIR_MODE = 0o700

# Where the file lives, and the variable that moves it. Read here rather than
# in `config.py` for `credentials.PATH_ENV`'s reason: `config.from_env` builds
# the settings a *run* resolves against, and nothing a run does should be able
# to name the file its own command came out of.
PATH_ENV = "LLOSSLESS_COMMANDS"

# Where a program `KNOWN_TOOLS` names may be, besides on `PATH`. Checked in
# this order, after `PATH`, and only ever joined to a program name this build
# wrote down -- so what this widens is where a known name is looked for and
# never what may be run.
#
# Every entry is the documented install location of a per-user or per-machine
# CLI: `~/.local/bin` is where a user-scope installer puts one and is what the
# operator's own `claude` is in; `/usr/local/bin` is the machine-wide
# equivalent; `~/.npm-global/bin` is the prefix npm's own documentation gives
# for installing globally without root; `/opt/homebrew/bin` is Homebrew's on
# Apple silicon, which is off the default `PATH` of anything not started from a
# login shell.
#
# **The reason there is a table at all.** `shutil.which` reads the `PATH` of
# *this process*, and a server's is whatever started it -- a unit file, a
# container entrypoint, a desktop sandbox. The operator's report was exactly
# that: `claude` in `~/.local/bin`, on their shell's `PATH`, and not on the
# one the page was asking. A row that says "not found" about a program the
# operator can run is a wrong answer, and it is wrong in the direction that
# loses the feature.
EXTRA_BIN_DIRS: tuple[str, ...] = (
    "~/.local/bin",
    "/usr/local/bin",
    "~/.npm-global/bin",
    "/opt/homebrew/bin",
)

# How much of an unusable route's key a message and a payload may repeat. The
# key comes out of the operator's file rather than out of `ROUTE_ID`, so it is
# exactly the string this module otherwise refuses to trust, and a page that
# rendered a kilobyte of it would be rendering whatever was in the file.
MAX_BAD_ID = 64


@dataclass(frozen=True)
class ToolModel:
    """One model a tool can be told to use, and the argv that tells it. A row.

    **This is the operator's complaint, answered:** *"When using Subscription
    mode in the WebUI, the user should be able to select the model. I have
    Haiku, Sonnet, Opus and Fable available. It is not clear which one would be
    used. Relying on the app default is not strategy. I don't wanna use the
    most expensive model Fable for such tasks."*

    `select` is the exact argv that pins the model, as a tuple, and it is the
    reason this is a table rather than a string the page could build. A model
    reaches a command line only by being a member here; there is no expression
    anywhere that joins a submitted string to an argument list.

    `model` is what the run is recorded under, and it is **the alias that was
    passed**, not a version. That is the only honest string available: the CLI
    resolves an alias to whatever snapshot its plan currently points at, this
    server cannot see which, and writing a dated model id here would be the
    inference `KnownTool.label` already refuses to make. What is recorded is
    what was asked for.

    `rank` orders the models by what they cost to run, cheapest first, and is
    what stops the page preselecting the dearest one. Not a price: a
    subscription has no per-run price, and what a heavier model spends is the
    plan's own quota. It is an ordering, and it is the operator's.

    `evidence` names where this row's facts were checked. It is carried in the
    source rather than in a commit message because a wrong model id here
    produces a wrong bill, and the next person to add a row needs to know what
    standard the existing ones were held to.

    `preselect` marks the row an untouched page is pointed at when the
    operator wrote no route of their own (612): the operator's ruling on 609's
    grid, Opus. At most one per tool, and never the dearest row.
    """

    id: str
    label: str
    model: str
    select: tuple[str, ...]
    rank: int
    evidence: str
    preselect: bool = False


@dataclass(frozen=True)
class KnownTool:
    """One subscription CLI this build recognises by name. A table row.

    `program` is a bare program name and never a path: it is what goes to
    `shutil.which` and what `EXTRA_BIN_DIRS` is joined to, so where it resolves
    is a fact about the machine and this row states none. A path written *here*
    would be a claim that one tool lives in one place; a directory in
    `EXTRA_BIN_DIRS` is a place any of these names may be looked for, which is
    the same widening `PATH` itself already is. The order is what keeps the two
    apart: `PATH` answers first, and the table is only reached when the
    machine's own answer was nothing at all.

    `label` is written here rather than derived from `program`, and it names
    the **tool**, never a model. `claude` is Anthropic's CLI, and which model
    it answers with is `--model`'s business rather than something to guess at
    from a binary name.

    `base_args` is what every route through this tool carries before the model
    is selected: for a CLI, the flag that makes it read stdin and write stdout
    once instead of opening a session.

    `result_args` is what makes the answer readable as an envelope rather than
    as bare text, and `envelope` is the field saying so on the row the argv is
    written into. The two are one decision written twice on purpose: a command
    carrying `--output-format json` whose route says `raw` hands the merge an
    envelope to parse, and `_row` refuses the pair when they disagree -- in
    both directions, and only since 541, which is when the refusal caught up
    with the three comments that already described it.

    Worth the argument because of what the envelope carries. 483 lists three
    things a command backend cannot know, and two of them arrive here: the
    token counts, and -- the reason this was added -- `server_tool_use`, the
    per-call count of whether the model went and looked anything up. A run
    that cannot read that counter cannot honestly say where a citation came
    from, and "the model says it searched" is a claim rather than a
    measurement (537).

    `models` is why one discovered tool becomes **several routes**. 518's rule
    is that the picker is one list and every row in it is a route to a model;
    a dropdown beside a route would be a second piece of state to misread, and
    the whole point of this milestone is that the row a reader highlights is
    what runs. So `claude` found once emits one route per model, each with its
    own id, its own label and its own argv.

    `window` is **declared, not measured**. A command backend cannot be asked
    for its context window and there is no token count to check afterwards
    (483), so some number has to be written down before the first call. This
    one is the conservative figure for the tool's documented default; an
    operator who knows better edits the route in the file, which is the same
    row this writes.
    """

    id: str
    label: str
    program: str
    window: int
    base_args: tuple[str, ...]
    models: tuple[ToolModel, ...]
    result_args: tuple[str, ...] = ()
    envelope: str = ENVELOPE_RAW


# The subscription CLIs this build looks for. A closed table, checked against
# `PATH`, and the only source an enabled route's command can come from.
#
# **`claude` alone, and that is a verification result rather than a shortlist.**
# OpenAI's CLI was to be the second row if its binary name could be confirmed,
# and it could not be: this task permits no network call, the program is on
# neither the host nor this sandbox, and the only spelling of it anywhere in
# this repository is a fixture string in `tests/test_client.py` that an earlier
# session wrote for a cassette-key check. A fixture is not evidence about a
# binary name. Shipping the row anyway would put a line on the operator's
# screen saying a named tool was looked for and not found, which is a claim
# this build cannot make; it is one row here and one row in each catalogue when
# somebody can run `command -v` and see it.
#
# **Every fact in it was read off the installed binary, and the rows say
# which read.** `claude --help` at version 2.1.274 documents `-p/--print` for
# non-interactive output and `--model <model>`, *"Provide an alias for the
# latest model (e.g. 'fable', 'opus', or 'sonnet')"*. That help text names
# three aliases and not the fourth; `haiku` was confirmed separately, out of
# the binary's own string table, where it appears in the same quoted alias
# list as `sonnet`. The two standards of evidence are not the same and the
# rows say which each had, because a wrong model id here produces a wrong
# bill and that is the failure this whole feature exists to prevent.
#
# The aliases are recorded rather than dated model ids: an alias is what was
# *asked for*, a snapshot is what the plan happened to resolve it to, and this
# server can see the first and not the second.
HELP = "claude --help, 2.1.274"
STRINGS = "claude 2.1.274 string table; not in --help"

KNOWN_TOOLS: tuple[KnownTool, ...] = (
    KnownTool(
        id="claude", label="Claude Code", program="claude", window=200000,
        # `--print` and not `-p`: the same flag, spelled the way the help
        # spells it, because the argv is read back by a check and a reader
        # comparing the two should not have to know they are one flag.
        base_args=("--print",),
        # `claude --help` at 2.1.274: *"--output-format <format>  Output
        # format (only works with --print): \"text\" (default), \"json\"
        # (single result), or \"stream-json\"".* The single-result shape is
        # the one `config.ENVELOPE_RESULT` reads, and it was confirmed against
        # installed binary rather than from the help alone: one `--print`
        # call returned `type: "result"`, the text under `result`, and a
        # `usage` block carrying `input_tokens`, `output_tokens`,
        # `cache_read_input_tokens` and `server_tool_use`.
        result_args=RESULT_ARGS,
        envelope=ENVELOPE_RESULT,
        # Cheapest first. `rank` is what the picker orders on and what stops
        # the dearest row being preselected, which the operator asked for in
        # as many words.
        models=(
            ToolModel(id="claude-haiku", label="Claude Code - Haiku",
                      model="haiku", select=("--model", "haiku"), rank=0,
                      evidence=STRINGS),
            ToolModel(id="claude-sonnet", label="Claude Code - Sonnet",
                      model="sonnet", select=("--model", "sonnet"), rank=1,
                      evidence=HELP),
            ToolModel(id="claude-opus", label="Claude Code - Opus",
                      model="opus", select=("--model", "opus"), rank=2,
                      evidence=HELP, preselect=True),
            ToolModel(id="claude-fable", label="Claude Code - Fable",
                      model="fable", select=("--model", "fable"), rank=3,
                      evidence=HELP),
        ),
    ),
)


def expansions() -> tuple[tuple[KnownTool, ToolModel], ...]:
    """Every route the table can produce, in the order the page offers them.

    One tool becomes one route per model, which is 518's rule -- one list,
    every row a route to a model -- applied to the case that produced it. The
    order is `rank` within a tool and table order between tools, so the first
    command route a page meets is the cheapest one to be wrong about.
    """
    out = []
    for tool in KNOWN_TOOLS:
        for model in sorted(tool.models, key=lambda row: row.rank):
            out.append((tool, model))
    return tuple(out)


# Every id a request may name, checked rather than assumed. A row whose id no
# request could name would be a route this server found, offered, and then
# refused on submit; two rows sharing an id would be a route that resolves to
# whichever the loop reached last.
assert all(ROUTE_ID.match(model.id) for _tool, model in expansions())
assert len({model.id for _tool, model in expansions()}) == len(expansions())
assert all(ROUTE_ID.match(tool.id) for tool in KNOWN_TOOLS)
assert len({tool.id for tool in KNOWN_TOOLS}) == len(KNOWN_TOOLS)
# A tool with no models is a tool that can only be run on whatever the CLI
# defaults to, which is the arrangement the operator refused: *"relying on the
# app default is not strategy."* There is no code path that offers one, so
# there is no row that can create one.
assert all(tool.models for tool in KNOWN_TOOLS)
# And every model really does pin one: an empty `select` is a route that
# claims a model in its label and asks the CLI for nothing.
assert all(model.select and model.model for _tool, model in expansions())
# One preselected row per tool at most, and never the dearest: the operator's
# instruction that Fable is not the default still holds under 612.
assert all(sum(model.preselect for model in tool.models) <= 1 for tool in KNOWN_TOOLS)
assert not any(model.preselect and model.rank == max(m.rank for m in tool.models)
               for tool in KNOWN_TOOLS for model in tool.models)

# The merge effort levels a request may choose on a route (613; `max` added
# by 615). The grid in 609 measured the first four, and the page's slider has
# one stop per level. `max` is a fifth stop nobody has measured -- the
# operator's ruling was to offer it anyway, with a warning rather than a
# refusal: the card says the level was never tested and that it may use a
# large share of a subscription's weekly allowance, and the same warning sits
# by the submit button while it is selected. `catalogue.validate_effort_block`
# already treated a level missing from `levels` as unmeasured rather than
# zero, so `max` needed no change there -- it is simply a level the grid never
# ran, like every other level a route's block does not carry a block for it.
# Checked against the binary's own list in `config`.
EFFORT_CHOICES = ("low", "medium", "high", "xhigh", "max")
assert set(EFFORT_CHOICES) <= set(config_web.EFFORT_LEVELS)


# The oldest CLI that can run a model, keyed by the program and the model id a
# route asks for (661). Read off the refusal itself, not a changelog: Claude
# Code 2.1.274, asked for `claude-opus-5-5`, answered `API Error: 400 Claude
# Code 2.1.274 does not support this model; version 2.1.280 or newer is
# required` (`api_error_code: claude_code_version_too_old`; the envelope is
# `arms/2026-09-26/opus-max/probe-2.1.274/calls.json`), and 2.1.281 answered
# as `claude-opus-5-5`. A route whose program is older is still offered and
# still runs: the page says it will be refused rather than this server
# refusing it, because the version is read and not the model's availability.
MIN_CLI_VERSION: dict[tuple[str, str], str] = {("claude", "claude-opus-5-5"): "2.1.280"}

# **Read off the install, never by running the program.** `claude --version`
# would answer in about 10 ms, but this server starts a program only to answer
# a run: discovery lists what it found without starting it, and switching a
# route on writes a file and starts nothing (`tests/test_web_commands.py` pins
# both with a program that leaves a marker when started). The native installer
# already says the version without that: `~/.local/bin/claude` is a symlink to
# `~/.local/share/claude/versions/<version>`, the one layout read off this
# machine (2.1.274, and 2.1.283 after the operator's update of 2026-09-26). A
# program installed any other way is unread, and unread is never "too old".
_VERSION = re.compile(r"\d+\.\d+\.\d+")


def read_cli_version(program: str) -> str:
    """The version the program's install names, or `` when it names none (661).

    `program` is a path this module already holds: a discovered `KNOWN_TOOLS`
    binary, or the first word of a route in the file. The link is resolved
    and the target's own name read; nothing is executed and nothing from a
    request reaches it.
    """
    try:
        name = os.path.basename(os.path.realpath(program))
    except (OSError, ValueError):
        return ""
    return name if _VERSION.fullmatch(name) else ""


def _version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def too_old_for(program: str, version: str) -> list[dict]:
    """`[{model, needs}]` for every model `MIN_CLI_VERSION` says `version` of
    `program` cannot run, or `[]` -- also when the version was not read."""
    if not version:
        return []
    return [{"model": model, "needs": needs}
            for (name, model), needs in sorted(MIN_CLI_VERSION.items())
            if name == program and _version_key(version) < _version_key(needs)]


def preselected(route_id: str) -> bool:
    """Whether a discovered route with this id is the one a page starts on (612)."""
    return any(model.preselect and model.id == route_id
               for _tool, model in expansions())


class CommandsError(Exception):
    """The routes file cannot be used, and the reason is safe to repeat.

    Every message raised as one of these names the file, the mode, the shape or
    a route *id*, and never a command -- `api.ApiError` puts an exception's
    message into a response body, so the discipline holds at the point the
    string is built rather than at the point it is served.
    """


class UnknownRoute(CommandsError):
    """A route id that is not in the file. Refused, never fallen back from.

    A separate class because the answer differs: an unusable file is a 409
    about this server's state, and this is a 400 about the request. A fallback
    is the one thing that must not happen here -- a submitter who names a route
    this server does not have has said something about where their documents
    are going, and running the request some other way answers a question they
    did not ask.
    """


class UnknownTool(UnknownRoute):
    """An id that is not in `KNOWN_TOOLS`. The refusal the enable path rests on.

    A subclass, so every caller that already treats an unknown *route* id as a
    400 about the request treats an unknown *tool* id the same way without
    being edited. The distinction matters in one direction only: this one is
    raised before anything is written, and it is what makes "the browser sends
    only the id of something the server already found" a check rather than a
    sentence.
    """


@dataclass(frozen=True)
class Route:
    """One way to answer a request by running a program. Four fields and a label.

    `command` is the only field that never leaves this process. `__repr__` is
    written rather than generated for exactly that reason: a frozen dataclass's
    default prints every field, a `repr` reaches a log line, a debugger and an
    exception's own rendering, and nobody decides that it should.

    `model` is required and is **not** guessed. It is the string that goes into
    `LLOSSLESS_MODEL`, which the report, the banner and the cassette key all
    read, so an operator who knows their wrapper reaches Opus 5 says so and has
    the run recorded under that name. An operator who does not say has their
    row refused by `_row` rather than filled in here (526): the page shows
    their label either way, and inferring a model from a command is how a
    correct-looking screen produces a wrong bill.

    The field keeps its default so `Route(...)` can be built without it in a
    check that is about some other field; nothing that reads the file can
    produce one, because `_row` refuses the row first.
    """

    id: str
    label: str
    command: str
    window: int
    profile: str = DEFAULT_PROFILE
    model: str = ""
    # Seconds one call through this route gets, or `None` for the default a
    # command backend resolves for itself (`config.COMMAND_TIMEOUT`, 533).
    #
    # Here rather than on the page, and for the reason `window` is here: this
    # is a property of the program the operator put in the file, and the
    # browser sends an id. It is also the only place a web submitter *can* be
    # given the setting -- there is no `--timeout` on a form -- so a route
    # whose program is slower than the default states its own figure and every
    # run through it gets it, with no new field for a browser to fill in.
    #
    # Optional where `window` is required, because the two are not the same
    # kind of missing: an unstated window leaves the run with no guard at all,
    # and an unstated timeout leaves it with a measured default.
    timeout: float | None = None
    # Written by `enable` from `KNOWN_TOOLS`, rather than by the operator. The
    # only thing it is read for is ownership: `enable` will not overwrite a row
    # without it and `disable` will not delete one, so the page can turn its
    # own rows on and off and can do nothing at all to the operator's. Stored
    # in the file rather than recomputed, because the alternative -- "is this
    # row's command still what `shutil.which` answers today" -- makes a tool
    # that moved on `PATH` into a row the page can no longer switch off.
    discovered: bool = False
    # How this route's command answers: `raw` (stdout is the text) or
    # `result` (stdout is a JSON result envelope that also carries the
    # usage block). Declared here because this is where the argv is declared,
    # and the two have to agree -- a command without its output-format
    # argument cannot produce the envelope a route claims for it (537).
    # `_row` refuses the disagreement; `_carries_result_args` is the reader
    # (541).
    #
    # Default `raw`, so a row an operator wrote before this existed means what
    # it meant then.
    envelope: str = ENVELOPE_RAW
    # Which of the model's own web tools this route's argv permits. Empty is
    # the default and is what every route did before this existed.
    #
    # **Here and nowhere else.** A grant to reach the network is a property of
    # the route the operator configured, like the model alias beside it -- not
    # a browser input and not a per-request field. A submitter chooses among
    # the operator's routes; they never describe one, and that rule is what
    # this whole module is (537).
    #
    # Separately selectable rather than one switch, because the two carry
    # different risk. See `WEB_TOOLS`.
    web_tools: tuple[str, ...] = ()

    def __repr__(self) -> str:
        return (f"Route(id={self.id!r}, label={self.label!r}, "
                f"command=<{len(self.command)} chars>, window={self.window}, "
                f"timeout={self.timeout}, "
                f"profile={self.profile!r}, model={self.model!r}, "
                f"envelope={self.envelope!r}, "
                f"web_tools={self.web_tools!r}, "
                f"discovered={self.discovered})")

    @property
    def model_name(self) -> str:
        """What `LLOSSLESS_MODEL` carries. The route's stated model, always.

        There is no fallback any more and that is the point. It used to answer
        with the route id when no model was stated, which was honest about the
        *name* and said nothing about the run: the program still went off and
        used whatever it defaults to, and the operator could not see which.
        `_row` refuses a route with no model now, so this property has one
        thing to return and cannot invent a second.
        """
        return self.model

    @property
    def seconds(self) -> float:
        """The bound one call through this route gets. Stated, or the default.

        `config.COMMAND_TIMEOUT` and never `DEFAULT_TIMEOUT`: every route here
        is a command backend by construction, so the figure that applies is
        the one measured against a subprocess (533).
        """
        return COMMAND_TIMEOUT if self.timeout is None else self.timeout

    @property
    def tier(self) -> str:
        """The single rung this route's profile pins, or `` when it probes.

        `structured.Profile.tiers` is empty for every profile that talks to an
        HTTP endpoint, because what an endpoint refuses is discovered rather
        than declared. A command backend is the case where it cannot be
        discovered, so `subscription` names its one rung -- and that rung is
        what decides whether this route's runs compare to anything published.
        """
        tiers = PROFILES[self.profile].tiers
        return tiers[0] if len(tiers) == 1 else ""

    @property
    def retrieval(self) -> tuple[str, ...]:
        """The web tools a `sourced` run through this route would be permitted (548).

        The operator's own grant where the file carries one, and otherwise the
        automatic grant `config.AUTO_GRANT` makes for a program this build
        recognises. Empty means a `sourced` run naming this route is refused
        rather than quietly answered from recall -- because it cannot retrieve,
        or, since 568, because it answers in plain text and so cannot report
        whether it did. The marker the page draws from this must not promise
        retrieval on a route the level will refuse.

        **Derived, never stored.** `web_tools` is what the operator wrote and
        stays exactly that; this is what a run would get, which is a different
        question and would go stale the day the automatic grant changed. It is
        also why `as_file_row` is untouched: the automatic grant does not write
        itself into the operator's file.
        """
        return config_web.sourced_tools(self.command)

    @property
    def comparable(self) -> bool:
        """Do this route's runs compare with the figures in the catalogue?

        Answered as a boolean and served as one, so the page needs no opinion
        about profile names -- the rule `verify_depths` follows for
        `detects_invention`, and for the same reason: the day a second command
        profile exists the page describes it correctly with no edit.

        False for `subscription`, and the reason is not a reservation about the
        backend. Every measured figure in this project was produced at
        `json_schema`; this route answers at `prompt`, sends no `temperature`
        and no `seed`, and is therefore not reproducible by construction (483).
        A figure measured over an endpoint, rendered beside it, would be a
        number measured under conditions this run does not meet; the figures
        the catalogue does carry for such a route (`command_routes`, 597) were
        measured through the route itself and rank only against each other.
        """
        return self.tier == PUBLISHED_TIER or not self.tier

    def described(self, chosen: dict[str, str] | None = None) -> dict:
        """Everything about this route a browser may be told. Never the command.

        The cost field is a word rather than a number and there is no branch
        here that can make it `0`. `pricing.py` keeps that rule for dollars --
        a run's cost is a figure, *unpriced*, or *unmeasured*, and never
        `$0.00`, because a zero reads as "measured, and free". A subscription
        reports no token counts at all, so `pricing.estimate` answers
        `unmeasured` for every call it makes; what the *operator* pays is their
        plan, which this tool has no way to divide by a merge. Both halves are
        said, and neither is a number.
        """
        return {
            "id": self.id,
            "label": self.label,
            "model": self.model or None,
            "window": self.window,
            # Resolved, not the stored `None`. A page showing what this route
            # will do has to show the number a call actually gets, and "not
            # stated" is not a number.
            "timeout": self.seconds,
            "profile": self.profile,
            "tier": self.tier or None,
            "comparable": self.comparable,
            # One vocabulary, two words, and no third. `plan` is what a
            # subscription costs; `unmeasured` is what this tool can say about
            # the tokens, which is nothing.
            "cost": "plan",
            "tokens": "unmeasured",
            # A command runs as the server process with that machine's
            # credentials, so it is shared by everybody with an account here.
            # Served as a field rather than assumed by the page: the day a
            # per-account route exists, this is what changes.
            "shared": True,
            # Whether the credentials sheet's toggle wrote this row. A boolean
            # about ownership and not about the command: it tells the page
            # which rows its own control may turn off, and carries nothing
            # about what runs.
            "discovered": self.discovered,
            # Which web tools a `sourced` run through this route would be
            # permitted, and whether that permission was the operator's own
            # grant or this build's automatic one (548).
            #
            # **Served rather than derived by the page**, the rule
            # `comparable` and `detects_invention` already follow: a page that
            # worked retrieval out by comparing a command it is never shown
            # against a program name it would have to learn is a page carrying
            # vocabulary it is supposed to be given. It is also the field the
            # transparency rests on -- the operator's condition on the
            # automatic grant was that it be obvious rather than hidden -- so
            # the row can say so without asking a second route.
            "retrieval": list(self.retrieval),
            "retrieval_granted": bool(self.web_tools),
            # The merge effort a request may choose for this route, and what it
            # gets when it chooses none (613), or null for a route that takes
            # none. Served rather than derived by the page, on `retrieval`'s
            # terms: the page is never shown the command it would be read off.
            "effort": self.effort(chosen),
            # The route an untouched page starts on when the operator wrote
            # none of their own (612). Only ever a discovered row.
            "preselect": self.discovered and preselected(self.id),
        }

    @property
    def _effort_capable_program(self) -> bool:
        """Would this route's program take a `--effort` flag at all, from anyone?

        The two refusals `effort_levels` always made, factored out so
        `single_level_model` can ask the same question without repeating them:
        a program this build has not read, or a command that already states
        its own level (562's rule 1), takes no flag from this build either way
        -- whatever the model is.
        """
        argv = config_web._argv(self.command)
        return bool(argv) and os.path.basename(argv[0]) in config_web.AUTO_EFFORT \
            and not config_web.stated_effort(self.command)

    @property
    def single_level_model(self) -> bool:
        """Does this route's stated `--model` take one level, not a scale (688, ruling 11)?

        Read off the argv the way `effort_levels` already is, so the two
        agree: a route this build cannot put a flag on is neither offered a
        level nor told it has one, and a route naming Haiku is told which of
        the two is true of it.
        """
        return self._effort_capable_program and config_web.is_single_level_model(
            config_web.stated_model(self.command))

    @property
    def effort_levels(self) -> tuple[str, ...]:
        """The merge levels a request may choose on this route, or none (613).

        None for a program whose flags this build has not read -- appending
        `--effort` to it breaks a working route -- none for a command that
        already states its own level, which wins over any request (562's rule
        1), so a level the request named would be one the run ignored -- and
        none for a single-level model (688, ruling 11): `effort` names that
        case on its own rather than through an empty list a page cannot tell
        apart from "this route has nothing to say about effort at all".
        """
        if not self._effort_capable_program or self.single_level_model:
            return ()
        return EFFORT_CHOICES

    def effort(self, chosen: dict[str, str] | None = None) -> dict | None:
        """`{levels, default}` for the merge on this route, `{single_level,
        label}` for one whose model takes one level instead of a scale, or
        None for a route that takes neither (613; 688 ruling 11).

        `default` is the level a request naming none gets: `config.effort_of`
        over the command, with `chosen` -- the server's own `LLOSSLESS_EFFORT*`
        -- where the operator set one, and the per-model table (612) where not.
        """
        if self.single_level_model:
            return {"single_level": True, "label": config_web.SINGLE_LEVEL_LABEL}
        levels = self.effort_levels
        if not levels:
            return None
        return {"levels": list(levels),
                "default": config_web.effort_of(self.command, "merge", chosen),
                # The levels 612 keeps out of every default at `sourced`, so
                # the page can say so beside them without a word list of its own.
                "not_at_sourced": [level for level in levels
                                   if level in config_web.MERGE_EFFORT_NOT_AT_SOURCED]}

    def as_file_row(self) -> dict:
        """This route as the `routes` object holds it. The one writer's shape.

        Only `_write` calls it, and `_row` is what reads the result back, so
        the two halves of the file format are a round trip rather than two
        spellings that drift. Optional fields are omitted at their defaults:
        a file an operator opens after using the toggle should look like the
        file the README documents, not like every field this build has.
        """
        row = {"label": self.label, "command": self.command,
               "window": self.window}
        if self.timeout is not None:
            row["timeout"] = self.timeout
        if self.profile != DEFAULT_PROFILE:
            row["profile"] = self.profile
        if self.model:
            row["model"] = self.model
        if self.envelope != ENVELOPE_RAW:
            row["envelope"] = self.envelope
        # Written even though it is always empty on a row this build creates.
        # The field is how an operator grants retrieval, and a route that
        # never shows it is a feature nobody discovers; an empty list in the
        # file beside `command` is the one place the two can be edited
        # together, which `_row` then requires (537).
        row["web_tools"] = list(self.web_tools)
        if self.discovered:
            row["discovered"] = True
        return row

    def environ(self) -> dict[str, str]:
        """The variables a run answering through this route resolves against.

        `LLOSSLESS_WINDOW` rather than a per-role map, because the route is
        one program answering every role and `config` refuses a command backend
        that leaves any role's window unstated -- a map covering two of three
        leaves the third exactly as blind as saying nothing (483).

        Both model variables, because `config.from_env` reads
        `LLOSSLESS_MERGE_MODEL` for the merge and `LLOSSLESS_MODEL` for the
        rest, and a route that set one would put the operator's table selection
        on the other half of their own run.

        **`LLOSSLESS_THINKING` names every role, and that is not a
        preference.** A subprocess is handed the prompt and nothing else --
        `backend.py` writes stdin and reads stdout -- so there is no request
        field any profile could put a thinking-off instruction in. The
        `subscription` profile says so out loud and `build_body` raises
        `ThinkingNotHonoured` rather than sending a request whose answer
        would be filed under a `thinking=False` cassette key (483); any
        other profile would build that field and have `backend.py` drop it
        silently, which is the same lie without the refusal. So the only
        configuration a command route can honestly run under is thinking on
        for every role, and the route states it rather than leaving an
        operator to meet it as a failure on their first call. It is recorded
        that way too: `provenance.decoding.thinking` lists all three.

        This is the one variable here that `jobs.REQUEST_SETTABLE` refuses
        on purpose -- "a quality decision, not a preference" -- and it is
        set here anyway, because it is being set by the operator's own
        route rather than by a submitter, and because the alternative is a
        run that cannot start.
        """
        return {
            "LLOSSLESS_COMMAND": self.command,
            "LLOSSLESS_THINKING": ",".join(ROLES),
            "LLOSSLESS_COMMAND_LABEL": self.label,
            "LLOSSLESS_WINDOW": str(self.window),
            # Written on every route, at the default as much as at a stated
            # figure, for the reason the window above is: the server's own
            # `LLOSSLESS_TIMEOUT` was set for the endpoint this server was
            # started with, and a run that contacts no endpoint must not
            # inherit a bound chosen for one. `:g` because the file may hold
            # either an int or a float and `config` parses both (533).
            "LLOSSLESS_TIMEOUT": f"{self.seconds:g}",
            "LLOSSLESS_PROFILE": self.profile,
            "LLOSSLESS_MODEL": self.model_name,
            "LLOSSLESS_MERGE_MODEL": self.model_name,
            # How the command's stdout is read, from the same row that holds
            # the argv it has to agree with (537). No variable for `web_tools`:
            # the grant is in the argv, the run makes no use of the list, and
            # a second copy in the environment would be a claim about a
            # permission nothing downstream can check. What the run learns
            # about retrieval it learns from the counter the answer carries.
            "LLOSSLESS_COMMAND_ENVELOPE": self.envelope,
        }


@dataclass(frozen=True)
class Unusable:
    """One row of the file this build cannot use, kept beside the ones it can.

    The point of this class is that a bad row stops being a property of the
    *file*. It used to be one: `read()` raised, `describe()` caught that and
    returned nothing, and a single stale route emptied a picker that had four
    good ones in it. Here the failure is the row's, it is reported with that
    row's id next to it, and every other row is loaded.

    `raw` is the row exactly as the file holds it, and it exists for one
    reason: `_write` puts it back. A rewrite that dropped what it could not
    parse would be this server deleting a line out of the operator's own file
    because it did not understand it, which is a larger claim over that file
    than switching a row on.

    `retired` is the one shape this module is allowed to drop -- a route the
    *pre-526* version of this page wrote, recognised by `discovered` plus a
    `KNOWN_TOOLS` id plus no model. See `Commands.migrate`.
    """

    # Exactly as the file holds it. JSON object keys are strings, so this is
    # always one, and it is what a write-back is keyed by.
    key: str
    # The same, clipped, for a message and for a served payload.
    name: str
    reason: str
    raw: object
    discovered: bool
    retired: bool

    def described(self) -> dict:
        """What a page may be told about a row that could not be loaded.

        The id and the sentence, and nothing out of the row itself -- the
        command in an unusable row is still a command, and the rule that
        `describe()` never serves one does not weaken because the row around
        it failed to parse.
        """
        return {"id": self.name, "reason": self.reason,
                "discovered": self.discovered}


@dataclass(frozen=True)
class Catalogue:
    """The file, read: the rows that work and the rows that do not.

    One return value rather than two calls, because two calls are two reads of
    a file that can change between them -- and the second of them would be the
    one deciding whether the first was complete.
    """

    routes: dict[str, Route]
    problems: tuple[Unusable, ...]


def search_dirs(environ=None) -> tuple[Path, ...]:
    """`EXTRA_BIN_DIRS`, expanded against this environment. Never `PATH`.

    Takes its environment as an argument for `default_path`'s reason: a check
    with an opinion about where a tool lives should be able to say so without
    editing the environment of the process running the suite.

    A `~` entry is dropped rather than guessed at when there is no `HOME`,
    because expanding it against whatever `Path.home()` falls back to on a
    daemon account is how a lookup ends up in `/root`.
    """
    source = os.environ if environ is None else environ
    home = (source.get("HOME") or "").strip()
    out = []
    for entry in EXTRA_BIN_DIRS:
        if entry.startswith("~/"):
            if not home:
                continue
            out.append(Path(home) / entry[2:])
        else:
            out.append(Path(entry))
    return tuple(out)


def default_path(environ=None) -> Path:
    """`$XDG_CONFIG_HOME/llossless/commands.json`, or the spec's fallback.

    The same lookup `credentials.default_path` does, through
    `config.config_file`, which takes its environment as an argument so a check
    with an opinion about where this file goes can say so without editing the
    environment of the process running the suite.
    """
    source = os.environ if environ is None else environ
    named = (source.get(PATH_ENV) or "").strip()
    if named:
        return Path(named).expanduser()
    return config_web.config_file(FILE_NAME, source)


def check_route_id(value) -> str:
    """The id, or `UnknownRoute`. The only thing a request may name.

    Returned rather than merely validated, for `credentials.check_provider`'s
    reason: a call site cannot then use the checked value and the raw one in
    the same breath, which is how a check ends up running beside a value
    instead of in front of it.

    The message names the field rather than listing the ids. Which routes exist
    is already on `/api/v1/config`, and a refusal that enumerated them would
    make this the second place that list is maintained.
    """
    if not isinstance(value, str) or not ROUTE_ID.match(value):
        raise UnknownRoute(
            "command_route names one of the routes this server was configured "
            "with, as an id: lowercase letters, digits, hyphen or underscore, "
            "at most 64 characters. It is looked up in a list the operator "
            "wrote and is never used to build a command.")
    return value


def check_tool_id(value) -> tuple[KnownTool, ToolModel]:
    """The table row this id names, or `UnknownTool`. **The whole enable path.**

    Answers with the pair rather than with the id, for `check_route_id`'s
    reason and with more at stake: a caller that got a validated string back
    would still have to look the row up, and a second lookup beside a check is
    how a check ends up running next to the value instead of in front of it.
    Here the only way to reach a `ToolModel` is through this function, so
    neither the command `enable` writes nor the argv that pins its model can
    come from anywhere but the table.

    The message names the ids. They are a constant of this build rather than a
    fact about the operator's file, so saying them is not a second copy of a
    list somebody maintains.
    """
    for tool, model in expansions():
        if isinstance(value, str) and value == model.id:
            return tool, model
    raise UnknownTool(
        f"this server recognises "
        f"{', '.join(model.id for _tool, model in expansions())} as routes it "
        f"can look for, and nothing else. A tool or a model that is not in "
        f"that list is added by writing a route into the commands file, which "
        f"is the way a program this server executes gets named by somebody "
        f"with a shell rather than by a browser.")


class Commands:
    """The routes file: read it, list it, look an id up in it.

    Holds no route in a field. `read()` goes to disk every time, which is what
    lets an operator add a route without restarting the server, and means there
    is nothing on this object for a `repr` or a traceback to find.
    """

    def __init__(self, path=None, *, environ=None, which=None,
                 search=None, version=None) -> None:
        self.path = Path(path) if path is not None else default_path(environ)
        self._environ = environ
        # `shutil.which`, unless a caller supplies one. The seam exists so a
        # check can describe a machine where a tool is present and a machine
        # where none is without installing or deleting a program, which is the
        # only way the "nothing was found" half of this can be driven at all.
        self._which = shutil.which if which is None else which
        # `read_cli_version`, unless a caller supplies one (661): the same
        # seam, for the one other thing this object reads off the machine.
        self._version = read_cli_version if version is None else version
        # **A caller that describes a machine describes all of it.** `search`
        # is the second half of the same seam, and it defaults to *nothing*
        # when `which` was supplied: a check that says "this machine has no
        # `claude` on its `PATH`" would otherwise go on to find the real one in
        # the real `~/.local/bin`, and the machine it was describing would
        # depend on the developer's own laptop. `None` for both is the only
        # combination that reads the machine this process is on.
        if search is not None:
            self._search: tuple[Path, ...] | None = tuple(
                Path(entry) for entry in search)
        elif which is not None:
            self._search = ()
        else:
            self._search = None
        # Which rows `migrate()` retired, for the page to say so once. Empty
        # until it runs, and it runs at `server.build`.
        self.retired: tuple[str, ...] = ()

    def __repr__(self) -> str:
        return f"Commands(path={str(self.path)!r})"

    def read(self) -> dict[str, Route]:
        """Every usable route in the file, or `{}`. Raises on the file itself.

        A row this build cannot use is **not** a reason to answer with nothing:
        that was the defect the operator met, where one stale route emptied a
        picker four good rows would have filled. `load()` is where that is
        decided and this is its first half; `problems()` is the other.

        An absent file is the ordinary state and is not an error: a server that
        has never been given a command route has no file, and `llossless
        serve` starts on such a machine and says nothing about it. That is the
        empty default, and it is the one the whole of this module is arranged
        around.
        """
        return self.load().routes

    def problems(self) -> tuple[Unusable, ...]:
        """Every row this build could not use, each with its own sentence."""
        return self.load().problems

    def load(self) -> Catalogue:
        """The file, split into the rows that work and the rows that do not.

        **The row is the unit and the file is not.** Everything below the
        `routes` object is checked per row and a failure is recorded against
        that row's id; everything at or above it -- the mode, the encoding, the
        JSON, the version, the presence of `routes` -- still raises, because a
        file this cannot parse is a file in which nothing can be said to be a
        row at all. The two are different answers to the operator and they are
        reported as different things: one row is wrong, or the file is.

        A file whose mode is wider than `0600` is refused and not repaired. The
        exposure is the other direction from a credentials file's: what matters
        is not that another account could read the commands, it is that another
        account could *write* them, and this server would then run whatever
        they chose. Repairing the mode would leave the file in service after
        somebody else had had the opportunity to edit it.
        """
        try:
            info = self.path.stat()
        except FileNotFoundError:
            return Catalogue(routes={}, problems=())
        except OSError as exc:
            raise CommandsError(
                f"{self.path} cannot be read: {exc.strerror or exc}") from None

        mode = stat.S_IMODE(info.st_mode)
        if mode & ~FILE_MODE:
            raise CommandsError(
                f"refusing to read {self.path}: it is mode {mode:04o} and a "
                f"file naming programs this server runs must be no wider than "
                f"{FILE_MODE:04o}. Another account on this machine can write "
                f"it, which means another account chooses what this server "
                f"executes; `chmod {FILE_MODE:04o}` is the fix, after checking "
                f"that what is in it is still what you wrote.")

        try:
            raw = self.path.read_text(encoding="utf-8")
        except OSError as exc:
            raise CommandsError(
                f"{self.path} cannot be read: {exc.strerror or exc}") from None
        except UnicodeDecodeError:
            raise CommandsError(
                f"{self.path} is not UTF-8, so it was not written by this "
                f"tool.") from None

        try:
            payload = json.loads(raw)
        except ValueError:
            raise CommandsError(
                f"{self.path} is not readable as JSON. No route in it was "
                f"loaded.") from None
        if not isinstance(payload, dict):
            raise CommandsError(
                f"{self.path} holds a {type(payload).__name__} where this "
                f"expects an object.")
        version = payload.get("version")
        if version not in READABLE_SCHEMA_VERSIONS:
            raise CommandsError(
                f"{self.path} declares schema version {version!r}; this build "
                f"reads {', '.join(str(v) for v in READABLE_SCHEMA_VERSIONS)}.")
        rows = payload.get("routes")
        if not isinstance(rows, dict):
            raise CommandsError(f"{self.path} has no `routes` object in it.")

        out: dict[str, Route] = {}
        bad: list[Unusable] = []
        for name, value in rows.items():
            try:
                out[self._id(name)] = self._row(name, value)
            except CommandsError as refusal:
                # This row and no other. The whole file used to go with it,
                # which is how one stale route emptied a picker.
                bad.append(self._unusable(name, value, str(refusal)))
        return Catalogue(routes=out, problems=tuple(bad))

    def _unusable(self, name, value, reason: str) -> Unusable:
        """One row that did not load, with enough of it to report and rewrite.

        `raw` is the row untouched so `_write` can put it back; everything
        else here is either a boolean or a clipped id, because what did not
        parse is exactly the part of the file this module does not trust.
        """
        key = name if isinstance(name, str) else str(name)
        shown = key[:MAX_BAD_ID]
        flag = isinstance(value, dict) and value.get("discovered") is True
        return Unusable(key=key, name=shown, reason=reason, raw=value,
                        discovered=bool(flag),
                        retired=self._is_retired(key, value))

    @staticmethod
    def _is_retired(key: str, value) -> bool:
        """Is this the row the *pre-526* discovery code wrote? See `migrate`.

        Three things at once, and all three are needed. `discovered` says this
        page wrote it, so retiring it is this page undoing its own work rather
        than editing the operator's. The key being a `KNOWN_TOOLS` **tool** id
        rather than a model id says it predates the split into one route per
        model. And an unstated model is what 526 refused, which is why the row
        is unusable in the first place. A row that a later build writes cannot
        match, because every row `enable` writes states a model.
        """
        if not isinstance(value, dict) or value.get("discovered") is not True:
            return False
        if key not in {tool.id for tool in KNOWN_TOOLS}:
            return False
        model = value.get("model")
        return not (isinstance(model, str) and model.strip())

    def _id(self, name) -> str:
        """One key of the `routes` object, checked as an id.

        Refused rather than skipped, and the refusal is now this row's rather
        than the file's. A route the file holds and no request can name is a
        route the operator wrote and cannot use, and telling them nothing
        about it is how a typo becomes an afternoon.
        """
        if not isinstance(name, str) or not ROUTE_ID.match(name):
            raise CommandsError(
                f"{self.path} has a route whose id is not usable: an id is "
                f"lowercase letters, digits, hyphen or underscore, starting "
                f"with a letter or a digit, at most 64 characters. It is the "
                f"only part of a route a request may name.")
        return name

    def _row(self, name: str, value) -> Route:
        """One entry, checked. Every message names the id and never the command."""
        if not isinstance(value, dict):
            raise CommandsError(
                f"{self.path}'s route {name!r} is a {type(value).__name__} "
                f"where this expects an object with a label, a command and a "
                f"window.")
        unknown = sorted(set(value) - {"label", "command", "window", "timeout",
                                       "profile", "model", "envelope",
                                       "web_tools", "discovered"})
        if unknown:
            raise CommandsError(
                f"{self.path}'s route {name!r} sets {', '.join(unknown)}, "
                f"which this build does not read. A field that is ignored is a "
                f"setting the operator chose and did not get.")

        label = value.get("label")
        if not isinstance(label, str) or not label.strip():
            raise CommandsError(
                f"{self.path}'s route {name!r} has no label. The label is the "
                f"whole of what a submitter is shown about this route, and it "
                f"is not derived from the command -- guessing which model a "
                f"program reaches is how a run goes somewhere it was not meant "
                f"to.")
        label = label.strip()
        if len(label) > MAX_LABEL or any(c in label for c in "\r\n\t"):
            raise CommandsError(
                f"{self.path}'s route {name!r} has a label that is unusable: "
                f"at most {MAX_LABEL} characters and no line breaks. It is "
                f"rendered into the run's own banner event, and a line break "
                f"in it would truncate a frame.")

        command = value.get("command")
        if not isinstance(command, str) or not command.strip():
            raise CommandsError(
                f"{self.path}'s route {name!r} has no command. Remove the "
                f"route rather than leaving it with nothing to run.")
        command = command.strip()
        if len(command) > MAX_COMMAND:
            raise CommandsError(
                f"{self.path}'s route {name!r} has a command of "
                f"{len(command)} characters, which is past the {MAX_COMMAND} "
                f"this accepts. A whole file was probably pasted into it.")
        if any(c in command for c in "\r\n\t") or not command.isprintable():
            raise CommandsError(
                f"{self.path}'s route {name!r} has a command carrying a line "
                f"break or a control character.")
        try:
            argv = shlex.split(command)
        except ValueError:
            # `shlex`'s own message is not repeated: it is about quoting, it
            # would be quoting the command to say so, and the operator is
            # looking at the line already.
            raise CommandsError(
                f"{self.path}'s route {name!r} has a command this cannot "
                f"split into a program and its arguments -- an unbalanced "
                f"quote, almost always. `backend.py` splits it the same way, "
                f"so it would fail on the first call instead.") from None
        if not argv:
            raise CommandsError(
                f"{self.path}'s route {name!r} has a command that splits into "
                f"nothing.")

        window = value.get("window")
        if isinstance(window, bool) or not isinstance(window, int) or window <= 0:
            raise CommandsError(
                f"{self.path}'s route {name!r} has no usable window. A command "
                f"backend cannot be asked for its context window and there is "
                f"no token count to check afterwards, so it has to be told "
                f"one: a positive whole number of tokens. Stating it here is "
                f"what stops the refusal arriving in the middle of a run.")

        # Optional, and refused when it is present and unusable rather than
        # quietly dropped: a route that states a bound and does not get one is
        # the case this whole field exists to answer. `bool` is excluded for
        # the reason it is on the window -- `True` is an `int` in Python, and
        # `"timeout": true` is a mistake rather than one second.
        timeout = value.get("timeout")
        if timeout is not None and (isinstance(timeout, bool)
                                    or not isinstance(timeout, (int, float))
                                    or timeout <= 0):
            raise CommandsError(
                f"{self.path}'s route {name!r} has a `timeout` that is not a "
                f"positive number of seconds. Leave it out to get the default "
                f"for a command backend ({COMMAND_TIMEOUT:g}s), or state the "
                f"seconds one call may take -- a subprocess has no stream to "
                f"renew the clock, so this bounds the whole call.")

        profile = value.get("profile") or DEFAULT_PROFILE
        if profile not in PROFILES:
            raise CommandsError(
                f"{self.path}'s route {name!r} names profile {profile!r}; the "
                f"registered profiles are {', '.join(sorted(PROFILES))} (see "
                f"structured.PROFILES).")

        model = value.get("model")
        if not isinstance(model, str) or not model.strip():
            # **The fix, then the reason, and the fix is one field.** The
            # first version of this said the rule at length and never said
            # what to do, and the operator met it as a wall of text about a
            # file they had not written. The reasoning is in DECISIONS 526;
            # what belongs here is the file, the route, the field and an
            # example of it.
            example = expansions()[0][1].model if expansions() else "haiku"
            raise CommandsError(
                f"{self.path}'s route {name!r} has no `model`. Add the name "
                f"the command's own flag selects, for example "
                f'"model": "{example}". A command backend cannot be asked '
                f"which model answered it, so a route that does not say runs "
                f"on whatever the program defaults to and reports a name "
                f"nobody chose.")

        # How this route's command answers. Refused when named and unknown
        # rather than falling back to `raw`, because a route whose command
        # carries `--output-format json` and whose file says `raw` hands the
        # merge an envelope to parse and reports the confusion as a model
        # fault (537).
        shape = value.get("envelope") or ENVELOPE_RAW
        if shape not in COMMAND_ENVELOPES:
            raise CommandsError(
                f"{self.path}'s route {name!r} names envelope {shape!r}; the "
                f"envelopes are {', '.join(COMMAND_ENVELOPES)}. `raw` means "
                f"the command writes the answer as text; `result` means it "
                f"writes a JSON result envelope, which also carries the token "
                f"counts and the counter saying whether the model searched.")

        # And the envelope has to agree with the argv, which is the half three
        # comments in this module said was here and was not (541). Membership
        # was all that was checked, so `envelope: result` on a command with no
        # `--output-format json` loaded, ran, and failed inside the merge as a
        # model fault. `web_tools` two blocks down has always been checked this
        # way; this is the same rule for the field beside it.
        #
        # Both directions, unlike `web_tools`. A grant the argv does not carry
        # is a permission nobody gave, which is one-sided; an envelope is a
        # parser selection, and picking the wrong one is a defect whichever way
        # the pair disagrees.
        carries = _carries_result_args(argv)
        if shape == ENVELOPE_RESULT and not carries:
            raise CommandsError(
                f"{self.path}'s route {name!r} declares envelope "
                f"{ENVELOPE_RESULT!r} but its command does not carry "
                f"{' '.join(RESULT_ARGS)}. The field records how the command "
                f"answers; it does not change the command. Add "
                f"{' '.join(RESULT_ARGS)} to the command, or set the envelope "
                f"to {ENVELOPE_RAW!r}.")
        if shape == ENVELOPE_RAW and carries:
            raise CommandsError(
                f"{self.path}'s route {name!r} carries "
                f"{' '.join(RESULT_ARGS)} but declares envelope "
                f"{ENVELOPE_RAW!r}. The command answers with a result "
                f"envelope; read as {ENVELOPE_RAW!r} the merge is handed a "
                f"JSON object where the answer should be and reports it as a "
                f"model fault. Set the envelope to {ENVELOPE_RESULT!r}, or "
                f"drop {RESULT_FORMAT_FLAG} from the command.")

        # Which of the model's own web tools this route permits. A list of
        # names from a closed table, and every one of them reaches an argv, so
        # this is checked exactly as strictly as the command itself.
        granted = value.get("web_tools") or []
        if not isinstance(granted, list) or any(
                not isinstance(item, str) for item in granted):
            raise CommandsError(
                f"{self.path}'s route {name!r} has a `web_tools` that is not a "
                f"list of names. Leave it out to grant none, which is what "
                f"every route did before the field existed.")
        unknown = [item for item in granted if item not in WEB_TOOLS]
        if unknown:
            raise CommandsError(
                f"{self.path}'s route {name!r} grants web tool(s) this build "
                f"does not know. The grantable tools are "
                f"{', '.join(WEB_TOOLS)}; nothing else reaches the command "
                f"line. Names are not repeated back here, because they came "
                f"out of the file.")
        # Order is the table's and not the file's, and duplicates collapse: the
        # grant is a set of permissions, and two spellings of one list would
        # otherwise produce two argvs and two of everything downstream.
        granted = tuple(tool for tool in WEB_TOOLS if tool in granted)
        # A grant only means anything if the argv carries it, and the argv is
        # the operator's string. Checked rather than assumed, because a route
        # that says it permits searching and does not pass the flag reports a
        # permission it never gave -- and the counter would then read
        # `not-searched` while the file said otherwise.
        if granted and ALLOW_TOOLS_FLAG not in argv:
            raise CommandsError(
                f"{self.path}'s route {name!r} lists `web_tools` but its "
                f"command does not carry {ALLOW_TOOLS_FLAG}. The field records "
                f"what the argv grants; it does not add the argument. Put "
                f"{ALLOW_TOOLS_FLAG} and the tool name(s) in the command, or "
                f"drop the field.")

        found = value.get("discovered", False)
        if not isinstance(found, bool):
            raise CommandsError(
                f"{self.path}'s route {name!r} has a `discovered` field that "
                f"is not true or false. It marks a row the credentials sheet "
                f"wrote and is the only thing that lets the page switch a row "
                f"off; a row you wrote yourself leaves it out.")

        return Route(id=name, label=label, command=command, window=window,
                     timeout=None if timeout is None else float(timeout),
                     profile=profile, model=(model or "").strip(),
                     envelope=shape, web_tools=granted,
                     discovered=found)

    def describe(self, chosen: dict[str, str] | None = None) -> list[dict]:
        """Every route as the page may see it, by id. **Never the command.**

        **The operator's own rows first, then the discovered ones cheapest
        first.** The order is not decoration: `renderModels` preselects the
        first command route it is given, so this function decides what an
        untouched page is pointed at. A hand-written route is a deliberate act
        by somebody with a shell and outranks anything this server found by
        itself; among the rows this server found, the cheapest to be wrong
        about goes first, which is the operator's instruction in as many
        words -- *"I don't wanna use the most expensive model Fable for such
        tasks."*

        Within each group it is label order, because the label is what a
        reader is choosing between and an id is a handle.

        **A row that did not load takes out itself and nothing else.** It used
        to take out the list: `read()` refused the whole file on one bad row
        and this caught that and answered with nothing, so an operator with
        four good routes and one stale one got an empty picker. The bad row is
        reported by `problems()` beside its own id now, and the rows around it
        are offered.

        An unreadable *file* is still an empty list here and a refusal
        everywhere it matters -- a settings page that could not render is a
        worse answer than a picker with no command rows in it, and `submit`
        still refuses every id over the same file.
        """
        try:
            routes = self.read()
        except CommandsError:
            return []
        out = []
        for route in sorted(routes.values(), key=self._order):
            row = route.described(chosen)
            row.update(self._cli(route))
            out.append(row)
        return out

    def _cli(self, route: Route) -> dict:
        """The version of the CLI a route runs, and the models it is too old for (661).

        Read only when the route's program is named like a `KNOWN_TOOLS`
        program -- the one CLI whose install layout this build has read and
        whose minimums it holds -- and read off that layout, never by running
        it (`read_cli_version`). The version string is served; the path it
        was read from is not, for `locate`'s reason.
        """
        none = {"cli_version": None, "cli_too_old": []}
        argv = config_web._argv(route.command)
        if not argv:
            return none
        name = os.path.basename(argv[0])
        if name not in {tool.program for tool in KNOWN_TOOLS}:
            return none
        try:
            program = argv[0] if os.sep in argv[0] else (self._which(argv[0]) or "")
        except OSError:
            program = ""
        version = self._version(str(program)) if program else ""
        return {"cli_version": version or None, "cli_too_old": too_old_for(name, version)}

    @staticmethod
    def _order(route: Route):
        """Where one route sits in the picker. See `describe`."""
        for position, (_tool, model) in enumerate(expansions()):
            if route.discovered and route.id == model.id:
                return (1, position, route.label)
        return (0, 0, route.label)

    def get(self, route_id) -> Route:
        """The route with this id, or `UnknownRoute`. **Never a fallback.**

        A submitter who names a route this server does not have has said
        something about where their documents are going. Running the request
        some other way answers a question they did not ask, and the money is
        spent before anybody notices -- which is the whole failure this
        milestone exists to prevent.
        """
        route_id = check_route_id(route_id)
        book = self.load()
        if route_id in book.routes:
            return book.routes[route_id]
        for bad in book.problems:
            if bad.key == route_id:
                # The row exists and this build cannot use it, which is a
                # different answer to "there is no such route" and is reported
                # as one: `jobs.command_plan` turns this into a refusal about
                # the server's state and `UnknownRoute` into one about the
                # request. Running it some other way is the thing that must
                # not happen either way.
                raise CommandsError(bad.reason)
        raise UnknownRoute(
            f"command_route {route_id!r} is not a route this server was "
            f"configured with. The routes come from a file only the "
            f"operator writes, and an id that is not in it is refused "
            f"rather than answered some other way.")

    def count(self) -> int:
        """How many usable routes there are. `0` for an absent or bad file."""
        with contextlib.suppress(CommandsError):
            return len(self.read())
        return 0

    # ----------------------------------------------------------------------
    # discovery: the second way the allowlist gets filled
    # ----------------------------------------------------------------------

    @property
    def writable(self) -> bool:
        """Can a route be switched on through this store at all?

        True here and False on `NoCommands`, and the page reads it so that "no
        tool was found" and "this server has no commands file to write" are two
        sentences rather than one empty panel. Losing this feature to an
        unexplained blank is how the operator lost it the first time.
        """
        return True

    def locate(self, tool: KnownTool) -> str:
        """Where this tool is, `PATH` first, or `` -- **server-side only**.

        The one function that produces a filesystem path in this module, and
        the reason every caller of it is inside this file: what it answers with
        is an absolute path under whichever account the server runs as, and
        `internal/tests/scan_release.py` refuses that shape anywhere in the
        published set for a reason that is not about credentials -- it names a
        person and a machine layout. `discovered()` reduces it to a boolean
        before anything can be served.

        **`PATH` answers first and `EXTRA_BIN_DIRS` only when it answered
        nothing.** The order is the whole of what keeps this a widening of
        where a name is looked for rather than a claim about where a tool
        lives: a machine that has an opinion about `claude` keeps it, and the
        table is reached only where the machine had none. What comes out of the
        table is checked to be a file this process can execute, because
        `shutil.which` checks that for its half and a fallback that did not
        would offer a directory or an unreadable name as a program.
        """
        try:
            found = self._which(tool.program)
        except OSError:
            # A `PATH` entry that cannot be stat'd is not this server's
            # problem to report: the tool is not usable, which is the same
            # answer as not being there.
            found = ""
        if found:
            return str(found)
        for directory in self._dirs():
            candidate = directory / tool.program
            try:
                if candidate.is_file() and os.access(candidate, os.X_OK):
                    return os.path.abspath(str(candidate))
            except OSError:
                # An unreadable directory is not this server's problem to
                # report either, for the reason above.
                continue
        return ""

    def _dirs(self) -> tuple[Path, ...]:
        """The directories `locate` falls back to. See `__init__`'s seam."""
        if self._search is not None:
            return self._search
        return search_dirs(self._environ)

    def discovered(self) -> list[dict]:
        """The table, checked against `PATH`. **Never a path, never an argv.**

        One row per *route* rather than per tool: `claude` found once is four
        rows, one per model, because 518's rule is that every row a reader
        chooses between is a route to a model. A tool with a model selector
        beside it would be a second piece of state to misread, which is the
        thing that rule exists to prevent.

        `available` is `locate()` reduced to a boolean, which is the whole of
        the leak discipline here: the resolved path exists in this process and
        in the file and reaches no payload, report or download. The argv that
        selects the model is not served either -- the page has no use for it
        and it is the other half of what gets executed.

        `enabled` is read from the file every call, like everything else here,
        so a route the operator deleted by hand shows as off without a
        restart. An unusable file reads as nothing enabled rather than
        raising, for `describe()`'s reason -- a settings sheet that will not
        render is a worse answer than one whose toggles are all off, and
        `enable` still refuses over the same file.
        """
        enabled: dict[str, Route] = {}
        broken: dict[str, Unusable] = {}
        with contextlib.suppress(CommandsError):
            book = self.load()
            enabled = book.routes
            broken = {bad.key: bad for bad in book.problems}
        rows = []
        for tool, model in expansions():
            row = enabled.get(model.id)
            bad = broken.get(model.id)
            where = self.locate(tool)
            rows.append({
                "id": model.id,
                "label": model.label,
                # Which tool this route runs, so a page can group four rows
                # under one heading without parsing the ids.
                "tool": tool.id,
                "tool_label": tool.label,
                # The model this route pins, stated rather than defaulted.
                # The operator's sentence is the requirement: relying on the
                # app default is not strategy.
                "model": model.model,
                "available": bool(where),
                # The version its install names, or null (661). The string
                # only; `where` stays in this process, and nothing is run.
                "version": (self._version(where) or None) if where else None,
                "enabled": row is not None,
                # An id the operator already used for a route of their own.
                # The page needs it to say why its toggle is inert, rather
                # than offering a control the server refuses. True for an
                # unusable hand-written row as well, because `enable` refuses
                # that one too and a live toggle over it would be a control
                # whose only answer is a 409.
                "owned": ((row is not None and not row.discovered)
                          or (bad is not None and not bad.discovered)),
                # What is wrong with the row that already holds this id, if
                # one does and it did not load. Beside the row it concerns,
                # which is the half of this the page could not say before.
                "problem": bad.reason if bad is not None else "",
                # The declared window this would be switched on with, so the
                # figure is on screen before it is written rather than
                # discovered in a file afterwards.
                "window": tool.window,
            })
        return rows

    def enable(self, route_id) -> ToolModel:
        """Write this route into the allowlist. The id names the table, always.

        **Both halves of the command line come from the table.** The program
        is `shutil.which`'s answer for a `KNOWN_TOOLS` row, and the arguments
        are that row's `base_args` plus the `ToolModel`'s `select`.
        `check_tool_id` is the only way to reach either, so there is no
        argument to this method, and no field of any request, that a command
        line can be built out of. That is the property the whole module exists
        for, stated on the one function that writes.

        Refused rather than merged where the id is already the operator's. A
        row they wrote is a row they can reach with an editor and this cannot:
        overwriting it would be this server editing a file it was given to
        read, and silently keeping theirs would be a toggle that reports on
        and changes nothing.
        """
        tool, model = check_tool_id(route_id)
        where = self.locate(tool)
        if not where:
            raise CommandsError(
                f"{tool.label} is not on this server's PATH, so there is "
                f"nothing to switch on. Install it for the account this "
                f"server runs as, or write a route naming it in the commands "
                f"file. The page offers what was found and never a program to "
                f"name.")
        book = self.load()
        routes = dict(book.routes)
        existing = routes.get(model.id)
        if existing is not None and not existing.discovered:
            raise CommandsError(
                f"the commands file already has a route called {model.id!r} "
                f"that was written by hand. It is left exactly as it is: this "
                f"page switches its own rows on and off and does not edit "
                f"yours. Rename or remove that route if you want this one "
                f"instead.")
        blocked = next((bad for bad in book.problems if bad.key == model.id),
                       None)
        if blocked is not None and not blocked.discovered:
            # The same refusal, for a hand-written row this build could not
            # read. Writing over it would be worse than writing over one that
            # loaded: the operator cannot see from the page what was in it.
            raise CommandsError(
                f"the commands file already has a hand-written route called "
                f"{model.id!r} that this build cannot read: {blocked.reason} "
                f"It is left exactly as it is. Fix or remove that route if "
                f"you want this one instead.")
        routes[model.id] = Route(
            id=model.id, label=model.label,
            command=shlex.join((where, *tool.base_args, *tool.result_args,
                                *model.select)),
            window=tool.window, profile=DEFAULT_PROFILE, model=model.model,
            # The envelope the argv just asked for, written into the same row.
            # A route enabled from the table has its `--output-format` and its
            # `envelope` field set together, which is the agreement `_row`
            # then requires of a hand-written one (541). Both come from
            # `RESULT_ARGS`, so the argv this writes and the check that reads
            # it cannot drift apart.
            envelope=tool.envelope,
            # Empty, always. Retrieval is not something this page grants: the
            # measured default is that no web tool runs, and a control that
            # switched one on from a browser would put the decision in the
            # wrong place. An operator who wants it edits the route.
            web_tools=(),
            discovered=True)
        self._write(routes, book.problems)
        return model

    def disable(self, route_id) -> ToolModel:
        """Take this route back out of the allowlist. Idempotent, and narrow.

        An id that is not in the file is not an error: the state the caller
        asked for is the state that holds, and a 4xx here would make a page
        that had been left open in a second tab report a failure for agreeing
        with it.

        A row the operator wrote is refused, the mirror of `enable`'s refusal
        and for the same reason. A control that can delete a line from a file
        somebody else wrote is a different capability to the one this is.
        """
        _tool, model = check_tool_id(route_id)
        book = self.load()
        routes = dict(book.routes)
        existing = routes.get(model.id)
        blocked = next((bad for bad in book.problems if bad.key == model.id),
                       None)
        if existing is None and blocked is None:
            return model
        if (existing is not None and not existing.discovered) or (
                blocked is not None and not blocked.discovered):
            raise CommandsError(
                f"the commands file's route {model.id!r} was written by hand "
                f"rather than by this page, so this page does not delete it. "
                f"Remove it with an editor if that is what you want.")
        routes.pop(model.id, None)
        # A row this page wrote and this build cannot read comes off with the
        # rest. It is still this page's own row -- `discovered` is what says
        # so -- and leaving it behind would make the toggle report a state
        # the file does not hold.
        keep = tuple(bad for bad in book.problems if bad.key != model.id)
        self._write(routes, keep)
        return model

    def migrate(self) -> tuple[str, ...]:
        """Retire the rows an earlier build of this page wrote. At startup, once.

        **The one case where this module changes a row nobody asked it to.**
        526 made an unstated model a refusal, and every route the version of
        discovery before it had written stated none -- `discovered: true`, the
        tool's own id, one command and no `--model`. The operator's file had
        exactly one row in it and it was that one, so 526 turned a working
        feature into an empty picker and a wall of text about a file they had
        never opened. Telling them to hand-edit it is not an answer; the row
        is this page's, so retiring it is this page's job.

        **Dropped, not rewritten, and that is the honest half.** The old row
        ran whatever the CLI defaults to. There is no mapping from that to one
        of four aliases that is not a guess, and a guess here is the thing 526
        exists to refuse -- writing four routes would switch on the dearest
        model the operator said they did not want, and writing one would pick
        for them. What they get is the four rows discovery already offers,
        none enabled, and one tick. `retired` carries the ids so the page can
        say what happened rather than leaving a route to vanish.

        **It cannot reach a row the operator wrote.** `_is_retired` needs
        `discovered: true`, which only `enable` writes, and a `KNOWN_TOOLS`
        tool id, which no current `enable` produces. A hand-written row with
        no model stays exactly where it is and keeps its own refusal.

        Silent on a file it cannot read or write: the caller is a server
        starting up, and there is a banner and a page for saying so.
        """
        try:
            book = self.load()
        except CommandsError:
            return ()
        retired = tuple(bad for bad in book.problems if bad.retired)
        if not retired:
            return ()
        keep = tuple(bad for bad in book.problems if not bad.retired)
        try:
            self._write(dict(book.routes), keep)
        except CommandsError:
            return ()
        names = tuple(bad.name for bad in retired)
        self.retired = names
        return names

    def _write(self, routes: dict[str, Route],
               problems: tuple[Unusable, ...] = ()) -> None:
        """Replace the file with these routes. Owner-only, and atomically.

        **Whole-file, and that is deliberate.** JSON carries no comments, so a
        rewrite loses formatting and key order and nothing else; the
        alternative is an in-place edit of a document this server did not
        write, which is a larger claim over the operator's file than switching
        one row on. `as_file_row` omits defaults so the result reads like the
        file the README documents.

        The mode is set on the temporary file **before** it holds anything and
        the replace is atomic, so there is no instant at which a wider file
        exists and no instant at which a half-written one is readable. That
        matters more here than it does for a key: `read()` refuses a file
        another account could have written, and a torn write is the one way
        this server could produce such a file itself.
        """
        # **A row this build could not read is copied back out verbatim.**
        # Dropping it would be this server deleting a line from the operator's
        # own file because it did not understand it, which is a larger claim
        # over that file than switching one row on -- and it would happen on a
        # toggle, silently, to a row they may have spent an afternoon on. The
        # usable rows go in second so a row being switched on wins over a
        # broken one with the same id; `enable` has already refused that case
        # unless the broken row is one this page wrote.
        rows: dict[str, object] = {bad.key: bad.raw for bad in problems}
        for route_id in routes:
            rows[route_id] = routes[route_id].as_file_row()
        payload = {"version": SCHEMA_VERSION,
                   "routes": {route_id: rows[route_id]
                              for route_id in sorted(rows)}}
        parent = self.path.parent
        try:
            parent.mkdir(mode=DIR_MODE, parents=True, exist_ok=True)
        except OSError as exc:
            raise CommandsError(
                f"{parent} cannot be created: {exc.strerror or exc}") from None
        body = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        temporary = ""
        try:
            handle, temporary = tempfile.mkstemp(
                dir=str(parent), prefix=".commands-", suffix=".json")
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                os.fchmod(stream.fileno(), FILE_MODE)
                stream.write(body)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
        except OSError as exc:
            # A half-written file in the operator's config directory is
            # litter at best and a second commands file at worst, so it goes
            # whether or not the failure can be reported.
            if temporary:
                with contextlib.suppress(OSError):
                    os.unlink(temporary)
            raise CommandsError(
                f"{self.path} could not be written: "
                f"{exc.strerror or exc}") from None


class NoCommands(Commands):
    """A store with no routes and no file. The default, and it is not a stub.

    `server.build` is handed one of these unless its caller asks for
    something else, so a library embedding this package and every server the
    suite binds offer no command backend at all. Written as a class rather
    than as `None` threaded through five call sites: every caller then asks
    the same object the same questions, and "is there a store" stops being a
    branch that one of them can get wrong.
    """

    def __init__(self) -> None:  # noqa: D107 - see the class docstring
        super().__init__(path=Path(os.devnull))

    def __repr__(self) -> str:
        return "NoCommands()"

    def read(self) -> dict[str, Route]:
        return {}

    def load(self) -> Catalogue:
        return Catalogue(routes={}, problems=())

    def migrate(self) -> tuple[str, ...]:
        """Nothing to retire, because there is no file to have written one."""
        return ()

    @property
    def writable(self) -> bool:
        """Nothing can be switched on here, because there is nowhere to write it."""
        return False

    def discovered(self) -> list[dict]:
        """Nothing, and not "nothing found".

        A server built with no store has no file to write a route into, so
        probing `PATH` and listing what is there would be an offer it cannot
        honour -- a panel of toggles that all refuse. `writable` is what the
        page reads to say which of the two states this is.
        """
        return []

    def enable(self, route_id) -> ToolModel:
        check_tool_id(route_id)
        raise CommandsError(
            "this server was built without a commands file, so there is "
            "nowhere to record a route. `llossless serve` always has one; a "
            "library embedding this package has to ask for it.")

    def disable(self, route_id) -> ToolModel:
        # Nothing is on, so nothing has to come off. Returning the row keeps
        # the idempotent answer `Commands.disable` gives, rather than raising
        # about a file at a caller that asked for a state that already holds.
        return check_tool_id(route_id)[1]
