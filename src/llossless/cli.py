"""The `llossless` command. Two subcommands over one pipeline.

`merge` writes the merged document and then verifies it. `verify` skips the
merge call and checks a document you already have. They differ by one step, so
they are one pipeline with that step made conditional rather than two functions
that will drift.

Three decisions here are worth the paragraph each.

**The caller's filenames are mapped onto canonical ones.** `merge.py` names the
sources `source_a.md`, `source_b.md`, `source_c.md` — one per path given, in the
order given — and `verify.py` targets `merged.md`; the prompts are rendered with
those names and the model attributes its evidence to them. That is not an
accident to be papered over — every figure this project publishes was measured
with those names in the prompt, and rendering the caller's `notes-a.md` instead
would make each run a configuration nothing was measured under. So the mapping
is explicit, one-way, and printed in the report. `--base` is how the operator
points at one of those documents, and it is matched against the paths they
typed rather than against the names this module gave them.

**Some faults end the run and some end a unit of work.** A schema failure is
one model call the model could not be made to answer usably: the unit errors,
the run continues, and the exit code is 2. An unreachable endpoint or an
exhausted structured-output ladder is not going to be different on the next
call, so it ends the run rather than producing five identical timeouts.

**There is no `--offline`, `--record` or `--replay`.** They build the corpus
under `tests/responses/`, which is something this repository does to itself.
`config.add_arguments(corpus_tools=False)` is where that is decided.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import replace
from pathlib import Path

from . import (__version__, config, merge, numerals, prompts, reconcile,
               segment, structured, sweep, usage)
from .console import (
    COLOUR_MODES, GREEN, RED, YELLOW, Console, colour, is_tty, paint,
    supports_colour,
)
from .cassette import (
    ConflictingCassettes, MissingCassette, MixedSources,
)
from .client import (CallBudgetExceeded, Client, DryRun,
                     PinnedTierViolated, SchemaFailure)
from .config import ConfigError
from .decompose import decompose_text
from .html_report import render as render_html
from .provenance import Provenance
from .report import (
    ERRORED, EXIT_CODES, OK, PLANNED, RECORD_ONLY, SKIPPED, InventoryDisagrees, Run, Step,
    as_dict, exit_code, inconclusive_for_retrieval_alone, render, retrieval_calls_word,
    retrieval_lead, retrieval_outcome, retrieval_turns, what_was_found,
)
from .structured import ThinkingIgnored, ThinkingNotHonoured, TierUnsupported
from .transport import Cancelled, TransportError
from .verify import (
    verify_coverage,
    MERGED_TO_SOURCES,
    SOURCE_TO_MERGED,
    Unusable,
    grade_declarations,
    verify_claims,
)

# What the caller's source paths become, and the name their merge takes. Read
# from the modules that own them rather than spelled again here: the names are
# load-bearing in the prompt, and a second copy is a second thing to keep in
# step. The count is the caller's now, so what used to be a constant here is
# `merge.source_names(len(args.sources))` at the one place that knows it.
MERGED = segment.MERGED_NAME

# Faults that will be the same fault on the next call. A unit of work erroring
# is a measurement outcome and the run goes on; these are not, and retrying
# them five times only makes the operator wait longer for the same message.
FATAL = (
    ConfigError,
    ConflictingCassettes,
    MissingCassette,
    MixedSources,
    CallBudgetExceeded,
    PinnedTierViolated,
    TierUnsupported,
    # Both halves of the thinking contract, and both fatal. The endpoint
    # refusing to turn thinking off and the endpoint accepting the field and
    # reasoning anyway leave the run in the same position: it cannot be what it
    # says it is. Erroring one unit of work and calling the next one would ask
    # the same model the same impossible question for the rest of the run.
    ThinkingIgnored,
    ThinkingNotHonoured,
    TransportError,
    merge.MergeError, Cancelled,  # Cancelled: the web server's cancel
)

ROLES = ("merge", "decompose", "verify")


# --------------------------------------------------------------------------
# Help text
# --------------------------------------------------------------------------
#
# Long, and deliberately. `llossless --help` used to print a usage line, one
# sentence and two subcommand names, which told a reader who had not found the
# README that there were two commands and nothing about how to run either. The
# facts a first run needs -- that there must be two sources, that `--base` picks
# the document whose structure survives, that the report is stdout and the merge
# is `-o`, that exit 1 and exit 2 mean different things -- are all in the README
# and were nowhere on the terminal.
#
# Every default and every choice list below is read from `config` rather than
# spelled again, so a value that moves moves here too.

DESCRIPTION = """\
LLossless: merge documents with a language model, then check the merge
against its sources both ways round: every claim in a source must survive
into the merge, and every claim in the merge must come from a source.
"""

EPILOG = f"""\
getting started

  1. Tell it which model to use. The default endpoint is a local Ollama at
     {config.DEFAULT_BASE_URL}, and the model is read from
     models.local.json (copy models.local.example.json), or from
     LLOSSLESS_MODEL, or from --model:

         llossless merge a.md b.md --base a.md --model qwen3:8b

  2. Merge two documents and keep both halves of the result:

         llossless merge notes-a.md notes-b.md --base notes-a.md \\
             -o merged.md > report.md

  3. Check a merge that already exists, however it was made:

         llossless verify notes-a.md notes-b.md merged.md

  4. Count the calls before spending them, and watch it work:

         llossless merge a.md b.md --base a.md --dry-run
         llossless merge a.md b.md --base a.md -v

what the arguments are

  SOURCE     A document to merge, or to check the merge against. Two or more,
             never one; UTF-8 text, markdown or plain.
  MERGED     On `verify`, the merged document. It goes last, after the sources.
  --base     On `merge`, which SOURCE the result follows: its structure, and
             its title under --title-policy keep-base. Required, because with
             three paths on one command line "the first one you typed" would
             be a choice you made without knowing you were making it.
  -o PATH    Where the merged document is written. Without it the merge is
             embedded in the report under `## Merged document` instead.

where the output goes

  The report is markdown on stdout, so it can be redirected. Progress and
  warnings go to stderr, so `> report.md` still leaves you something to watch.
  `-v` names each step, `-vv` adds each model call and each cache hit.

  exit 0   nothing was dropped or contradicted and, at `--verify-depth full`,
           nothing was invented. At `coverage` nothing reads the merged
           document back, so 0 says nothing about invention; reports say so
  exit 1   at least one finding, or more of the source segments declared
           dropped than --loss-budget allows ({config.DEFAULT_DECLARED_LOSS_BUDGET:.0%} by default)
  exit 2   inconclusive: bad configuration, an unreachable endpoint, a unit
           the model could not answer, a source with no claims on verify,
           no evidence quote found, a sourced merge that looked nothing up,
           an unwritable -o, disagreeing counts. 2 supersedes 1.
  exit 3   the merged document is sound as far as this tool looked and the
           merge's account of itself is not. 1 and 2 both supersede it.

environment

  LLOSSLESS_BASE_URL         endpoint, default {config.DEFAULT_BASE_URL}. A URL
                             with no path gets /v1 appended, so the bare host a
                             hosted runner gives you works as typed
  LLOSSLESS_MODEL            model for the verify and decompose roles
  LLOSSLESS_MERGE_MODEL      model for the merge role; defaults to the above
  LLOSSLESS_COMMAND          a program to answer through instead of HTTP, as
                             --answer-with: the prompt on its stdin, the answer
                             on its stdout
  LLOSSLESS_COMMAND_ENVELOPE  one of {", ".join(config.COMMAND_ENVELOPES)} (default {config.ENVELOPE_RAW}):
                             whether that program's stdout is the answer or
                             a JSON result envelope carrying it
  LLOSSLESS_COMMAND_LABEL    what the report calls that program
  LLOSSLESS_EFFORT           how hard a command backend is asked to think, one
                             of {", ".join(config.EFFORT_LEVELS)};
                             LLOSSLESS_EFFORT_<ROLE> sets it for one role
  LLOSSLESS_STRUCTURED       one of {", ".join(config.STRUCTURED_MODES)}
  LLOSSLESS_PROFILE          request envelope, one of
                             {", ".join(sorted(structured.PROFILES))}; default
                             {structured.DEFAULT_PROFILE}. Chosen, never guessed from a model id
  LLOSSLESS_WINDOW           the context window this endpoint serves, in tokens.
                             Unset means ask the endpoint; state a figure for one
                             that has no /api/ps. Reported as stated, not measured
  LLOSSLESS_THINKING         roles that may emit reasoning, comma-separated;
                             default {",".join(sorted(config.DEFAULT_THINKING)) or "none"}. Set
                             but empty always means none, whatever the default
                             is; unset is the only case that falls back to it
  LLOSSLESS_TIMEOUT          seconds per request, default {config.DEFAULT_TIMEOUT:g} over HTTP,
                             where a stream renews the clock and this bounds
                             silence; {config.COMMAND_TIMEOUT:g} for a command backend, which
                             has no stream, so it bounds the whole call
  LLOSSLESS_MIN_INTERVAL     seconds between live calls; lets a GPU cool down
  LLOSSLESS_FIDELITY         one of {", ".join(config.FIDELITY_CHOICES)}
                             (`off` is the older name for `verbatim`)
  LLOSSLESS_TITLE_POLICY     one of {", ".join(config.TITLE_POLICIES)}; default
                             {config.DEFAULT_TITLE_POLICY}
  LLOSSLESS_VERIFY_DEPTH     one of {", ".join(config.VERIFY_DEPTHS)}; default {config.DEFAULT_VERIFY_DEPTH}
  LLOSSLESS_LOSS_BUDGET      share of the source segments a merge may declare
                             dropped, default {config.DEFAULT_DECLARED_LOSS_BUDGET}
  LLOSSLESS_FIELD_ORDER      one of {", ".join(config.FIELD_ORDERS)}; default {config.DEFAULT_FIELD_ORDER}
  LLOSSLESS_MAX_TOKENS       an output ceiling for the merge; unset lets the
                             request profile decide
  LLOSSLESS_STREAM           false turns off streamed answers over HTTP
  LLOSSLESS_API_KEY_ENV      the NAME of the variable holding the API key,
                             default {config.DEFAULT_KEY_ENV}. The key itself is
                             never logged, cached or reported.
  LLOSSLESS_CA_BUNDLE        CA bundle, for a TLS-intercepting proxy
  LLOSSLESS_CACHE_DIR        response cache, default {config.CACHE_DIR}
  LLOSSLESS_ENDPOINT_LABEL   a name for the deployment, recorded in place of
                             its address
  LLOSSLESS_BASE_URL_<ROLE>, LLOSSLESS_API_KEY_ENV_<ROLE>,
  LLOSSLESS_WINDOW_<ROLE>    the same three for one role, where <ROLE> is
                             one of {", ".join(r.upper() for r in ROLES)}
  NO_COLOR                   set to anything to turn colour off

  A flag beats an environment variable, which beats models.local.json.

  `llossless merge --help` and `llossless verify --help` list every flag.
"""

MERGE_EPILOG = """\
examples

  llossless merge a.md b.md --base a.md
  llossless merge a.md b.md c.md --base b.md -o merged.md > report.md
  llossless merge a.md b.md --base a.md --fidelity mid -v
  llossless merge a.md b.md --base a.md --json report.json --dry-run

Fidelity is how freely the merge may reword the sources. At `verbatim`, every
sentence in the merged document is a sentence copied out of a source character
for character. No level licenses rewriting a number, a unit, a URL, a file
path, a version string, a command, or anything inside a fenced block.

`verbatim` is the strictest level, not the absence of one: it turns rewriting
off, not checking. It used to be called `off`, and `--fidelity off` still
names it, indefinitely: recorded runs and older scripts are written in that
spelling and keep working.

The level is printed on every report, because the same coverage figure means
different things at different levels.
"""

VERIFY_EPILOG = f"""\
examples

  llossless verify a.md b.md merged.md
  llossless verify a.md b.md c.md merged.md --json report.json

`verify` makes no merge call, so it is the cheaper and the more reproducible of
the two commands. It checks a document you already have, whoever wrote it.

Without --fidelity it assumes the merge was made at the default level
({config.DEFAULT_FIDELITY}). If it was actually made at a stricter level, say
so with --fidelity: a checker that believes it is looking at a licensed
rewrite or combination will excuse one that never happened.
"""

# The four defaults `serve` starts from, restated here rather than read from
# the web package. Reading them would mean importing `llossless.web` at module
# scope -- `build_parser` runs on every invocation, including `--help` -- and
# the engine is required to work with the web package absent, which
# `test_a_complete_merge_never_loads_the_web_package`
# (`tests/test_cli.py:4718`) asserts. A restated value is a value that can drift, so
# it is not left to a comment: `tests/test_web_server.py` asserts all four
# still equal `web.server.HOST`, `web.server.DEFAULT_PORT`,
# `web.jobs.DEFAULT_WORKERS` and `web.jobs.DEFAULT_RETENTION_SECONDS`.
SERVE_HOST = "127.0.0.1"
SERVE_PORT = 8765
SERVE_WORKERS = 1
SERVE_RETENTION = 172800.0

# The variable that carries the token, restated for the same reason and
# checked against `web.credentials.TOKEN_ENV` by the same test. It is named in
# `--help` because the one thing an operator reaching for `--host` needs to
# know is what the refusal is going to ask them for.
SERVE_TOKEN_ENV = "LLOSSLESS_WEB_TOKEN"

# And the variable that carries the retention window, restated and checked the
# same way against `web.jobs.RETENTION_ENV`. Named in `--help` because the
# deployment this setting is for -- a unit file, a container -- is the one with
# no command line anybody edits.
SERVE_RETENTION_ENV = "LLOSSLESS_RETENTION"

SERVE_EPILOG = f"""\
examples

  llossless serve
  llossless serve --port 0
  llossless serve --workers 2 --retention 0
  {SERVE_TOKEN_ENV}=$(head -c 24 /dev/urandom | base64) llossless serve --host 0.0.0.0

The interface listens on {SERVE_HOST} unless --host says otherwise, and any
address that is not loopback needs an account, or, while the server has none, a
token in {SERVE_TOKEN_ENV}. With neither the command refuses to start rather
than binding: this server spends whatever credential its own environment holds
on every document submitted to it, so reaching it from another machine and
authenticating the submitter are one decision and not two. With no accounts,
every API request must carry the token in an X-LLossless-Token header; the
page asks for it, then offers the first-account form. Once an account exists,
logging in is the authentication and the token is not consulted. The page
itself is public: it is a shell, and everything on it arrives through the API.

Documents, the merged document, the report and the progress log are deleted
{int(SERVE_RETENTION // 3600)} hours ({int(SERVE_RETENTION)}s) after a run
finishes, so a run made at the end of one working day is still there the next
morning. --retention or {SERVE_RETENTION_ENV} sets that, in seconds, and
`--retention 0` keeps them until they are deleted; that is the opt-out and has
to be asked for, because these are confidential files on somebody else's
machine.

A submitted form may choose the models, the fidelity level, the verification
depth, the title policy and the loss budget, and which of this server's own
endpoints or command routes answers, by name. It may not supply an address, a
command, the variable an API key is read from, or any path this server reads or
writes: those belong to whoever runs it.

API keys set through the settings page are kept in a file of their own, owner-
readable and nothing else, at $XDG_CONFIG_HOME/llossless/credentials.json
unless LLOSSLESS_CREDENTIALS names another. They are loaded into this server's
own environment; no key is ever sent back to a browser.
"""



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llossless",
        description=DESCRIPTION,
        epilog=EPILOG,
        # Raw, because the text above is a laid-out document and argparse's
        # default formatter would reflow the examples into one paragraph.
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-V", "--version", action="version",
        version=f"LLossless {__version__} (python {sys.version.split()[0]})",
        help="print the version and exit",
    )
    # Not `required=True`. A bare `llossless` is somebody finding out what the
    # thing is, and argparse's answer to a missing required subcommand is a
    # usage line, `error: the following arguments are required: COMMAND`, and
    # exit 2 -- which tells them a word they have not heard of is missing and
    # nothing about what to type instead. `main` prints the full help for it
    # and exits 0, which is what `-h` does and what they meant.
    commands = parser.add_subparsers(
        dest="command", required=False, metavar="COMMAND", title="commands",
    )

    merge_parser = commands.add_parser(
        "merge",
        help="merge two or more sources and verify the result",
        description="Merge two or more documents into one, then check the "
                    "result against every source in both directions.",
        epilog=MERGE_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    merge_parser.add_argument(
        "sources", type=Path, nargs="+", metavar="SOURCE",
        help="the source documents to merge, two or more",
    )
    # Required, and not defaulted to the first path. `MergePolicy` keeps the
    # base's title under `keep-base` and the merge follows the base's structure,
    # so which document it is changes the answer — and with three paths on a
    # command line "the first one you typed" is a choice the operator made
    # without knowing they were making it. `merge_documents` still defaults, for
    # a library caller who has already decided; the command line refuses.
    merge_parser.add_argument(
        "--base", type=Path, required=True, metavar="PATH",
        help="which SOURCE the merge follows the structure of, and the title "
             "of under --title-policy keep-base",
    )

    # On `merge` alone: `verify` composes nothing, so there is no
    # policy for a sweep to vary. The deliverable needs live inference and
    # `sweep.refuse_before_running` says so before a call is made.
    merge_parser.add_argument(
        "--sweep-fidelity", action="store_true",
        help=f"merge once at each of the {len(sweep.LEVELS)} levels, "
             f"{', '.join(config.FIDELITY_PUBLISHED)}, and report them side "
             f"by side. A level this backend refuses ({config.SOURCED} "
             f"without retrieval) is left out, and the sweep says so and why. "
             f"Requires live inference.",
    )
    merge_parser.add_argument(
        "--sweep-dir", type=Path, metavar="DIR",
        help="with --sweep-fidelity, write merged.LEVEL.md and report.LEVEL.json "
             "for every level here",
    )

    verify_parser = commands.add_parser(
        "verify",
        help="verify a merge you already have",
        description="Check an existing merged document against the sources it "
                    "was made from. Makes no merge call.",
        epilog=VERIFY_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # `SOURCE... MERGED` parses because argparse leaves the last positional a
    # value before it feeds the greedy one. `verify` takes no --base: nothing
    # here composes a document, so there is no structure to follow.
    verify_parser.add_argument(
        "sources", type=Path, nargs="+", metavar="SOURCE",
        help="the source documents the merge was made from, two or more",
    )
    verify_parser.add_argument(
        "merged", type=Path, metavar="MERGED",
        help="the merged document to check, last on the line, after the sources")
    # Declared here only so that `main` can refuse it with a reason, and for a
    # sharper motive than `-o` below has. On this subparser `--base` is not an
    # unknown option at all: argparse accepts unambiguous prefixes and
    # `--base-url` is right there, so without this line
    # `verify a.md b.md m.md --base a.md` quietly points the client at a
    # filename and reports nothing wrong. `merge` is unaffected, because an
    # exact match beats a prefix — which is what makes the trap belong to the
    # one command that has no base.
    verify_parser.add_argument(
        "--base", type=Path, metavar="PATH",
        help="which SOURCE the merge follows (merge only)",
    )

    for subparser in (merge_parser, verify_parser):
        # `-o` is on both so that passing it to `verify` is an error with a
        # reason rather than argparse's "unrecognized arguments". The caller who
        # typed it expected a merged document, and the failure this project is
        # about is a step not happening quietly.
        subparser.add_argument(
            "-o", "--output", type=Path, metavar="PATH",
            help="write the merged document here (merge only)",
        )
        subparser.add_argument(
            "--json", type=Path, metavar="PATH", dest="json_path",
            help="also write the machine-readable report here",
        )
        # Beside `--json` because it is the same offer: the report you just
        # read, written somewhere you can keep it. The page is self-contained
        # and makes no request to anything, so a reader can open it from a
        # share or an attachment without a network.
        subparser.add_argument(
            "--html", type=Path, metavar="PATH", dest="html_path",
            help="also write a self-contained HTML report here",
        )
        # On the subparsers rather than on the top-level parser, where
        # `llossless -v merge ...` would be the only accepted spelling.
        # Everything else a caller passes goes after the subcommand, so putting
        # these anywhere else would make them the two flags that are typed in a
        # different position from the rest and rejected when they are not.
        group = subparser.add_argument_group("output")
        group.add_argument(
            "-v", "--verbose", action="count", default=0,
            help="say what is happening, on stderr. Repeat for more: -v names "
                 "each step, -vv adds every model call, cache hit and retry",
        )
        group.add_argument(
            "--colour", "--color", choices=COLOUR_MODES, default="auto",
            dest="colour", metavar="WHEN",
            help=f"colour the report and the progress lines: "
                 f"{', '.join(COLOUR_MODES)} (default auto, which means a "
                 f"terminal that is not NO_COLOR and not TERM=dumb)",
        )
        config.add_arguments(subparser, corpus_tools=False)

    # The web interface, and the third command. Declared here, imported
    # nowhere: `build_parser` runs on every invocation including `--help`, and
    # `tests/test_cli.py::test_a_complete_merge_never_loads_the_web_package`
    # requires a complete `merge` run to leave `llossless.web` absent from
    # `sys.modules`. The import is inside `main`'s `serve` branch and must stay
    # there; `merge.verify_title` (`merge.py:746`) defers an import the same
    # way and for a related reason.
    serve_parser = commands.add_parser(
        "serve",
        help="run the local web interface",
        description="Serve the web interface and its JSON API on this machine. "
                    "Merges submitted through it run the same pipeline "
                    "`llossless merge` runs, against the endpoint this "
                    "server's own environment configures.",
        epilog=SERVE_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    serve_parser.add_argument(
        "--port", type=int, default=SERVE_PORT, metavar="PORT",
        help=f"listen on this port (default {SERVE_PORT}). 0 asks the "
             f"operating system for a free one and prints what it gave",
    )
    # `--host`, and it arrived in the same commit as the token rather than
    # before it. The server spends the operator's API credit on every document
    # submitted to it, so a flag that accepted 0.0.0.0 while nothing
    # authenticated the submitter would make a key-spending endpoint reachable
    # from the network -- and a commit in which that is true is a commit
    # somebody deploys. `web.server.build` refuses any non-loopback address
    # with no account and no token before it binds, which is what makes this
    # flag safe to offer rather than merely documented as dangerous.
    serve_parser.add_argument(
        "--host", default=SERVE_HOST, metavar="HOST",
        help=f"listen on this address (default {SERVE_HOST}). Anything that is "
             f"not loopback needs an account, or, while the server has none, a "
             f"token of at least 16 characters in {SERVE_TOKEN_ENV}, presented "
             f"by every API request in an X-LLossless-Token header (the page "
             f"asks for it); with neither the command refuses to start",
    )
    serve_parser.add_argument(
        "--work-dir", type=Path, metavar="DIR",
        help="where submitted documents and their reports are kept until the "
             "retention window passes (default: a `web` directory under the "
             "cache directory). Created owner-only",
    )
    serve_parser.add_argument(
        "--workers", type=int, default=SERVE_WORKERS, metavar="N",
        help=f"how many merges may run at once (default {SERVE_WORKERS}). "
             f"The engine is synchronous and --min-interval paces one client, "
             f"not a pool, so raising this is a statement about your endpoint",
    )
    serve_parser.add_argument(
        # `None` is the default rather than `SERVE_RETENTION`, and it means
        # "not given" rather than "keep forever" -- the two are told apart one
        # layer down, by `web.jobs.FROM_ENVIRONMENT`. It has to be a sentinel:
        # this flag has to beat the environment variable, and a flag whose
        # default is the real number arrives at `serve` indistinguishable from
        # one the operator typed.
        "--retention", type=float, default=None, metavar="SECONDS",
        help=f"delete a finished run's documents, merge and report this long "
             f"after it finishes (default {int(SERVE_RETENTION)}, which is "
             f"{int(SERVE_RETENTION // 3600)} hours; {SERVE_RETENTION_ENV} "
             f"sets the same thing for a deployment with no command line). 0 "
             f"keeps them until they are deleted, which has to be asked for",
    )

    return parser


def read_document(path: Path, what: str) -> str:
    """One document off disk, with the three ways it can be useless named."""
    try:
        # `utf-8-sig` strips a leading byte-order mark and does nothing else --
        # it is not `errors="replace"`, which was refused because it
        # turns a mis-encoded document into a silently mangled one. A BOM read
        # as content left U+FEFF glued to the first heading, the ATX pattern
        # stopped matching it, and a byte-faithful merge reported four findings
        # about a character nobody can see. A BOM that is not leading is
        # content and survives.
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise ConfigError(f"cannot read {what} {path}: {exc.strerror or exc}") from exc
    except UnicodeDecodeError as exc:
        raise ConfigError(
            f"{what} {path} is not UTF-8 (byte {exc.start}: {exc.reason}); "
            "this tool reads text, not the file's original encoding"
        ) from exc
    if not text.strip():
        raise ConfigError(f"{what} {path} is empty; there is nothing to check")
    return text


def planned_writes(args) -> list[tuple[str, Path]]:
    """Every file this run will write, as (what named it, where), before any call.

    Derived from the arguments rather than listed at each write site, because
    listing them at the write sites is what produced the defect this exists to
    stop: `-o` was guarded and `--json`, `--html` and `--sweep-dir` were not.
    """
    writes: list[tuple[str, Path]] = []
    for flag, value in (("-o", getattr(args, "output", None)),
                        ("--json", getattr(args, "json_path", None)),
                        ("--html", getattr(args, "html_path", None))):
        if value is not None:
            writes.append((flag, value))
    sweep_dir = getattr(args, "sweep_dir", None)
    if sweep_dir is not None and getattr(args, "sweep_fidelity", False):
        for level in config.FIDELITY_LEVELS:
            writes.append((f"--sweep-dir ({level})", sweep_dir / f"merged.{level}.md"))
            writes.append((f"--sweep-dir ({level})", sweep_dir / f"report.{level}.json"))
    return writes


def output_collision(args, paths: dict[str, Path]) -> str | None:
    """The refusal message, or None. Checked before the client is built.

    `-o` had this check and its siblings did not, so `merge a.md b.md --json
    a.md` exited 0 having replaced the source with a JSON report. The sources
    are read into memory before any output is written, so by the time
    `write_text` runs there is nothing left to un-truncate -- which is why this
    refuses ahead of the first model call rather than repairing afterwards.

    Resolved paths, the same way `canonical_base` matches `--base`, so `./a.md`
    and `a.md` collide. Two outputs naming one path are refused too: the second
    write silently replaces the first, and a report that was produced and then
    overwritten is indistinguishable from one that was never produced.
    """
    seen: dict[Path, str] = {}
    for flag, path in planned_writes(args):
        target = path.expanduser().resolve()
        clobbered = [name for name, source in paths.items()
                     if source.expanduser().resolve() == target]
        if clobbered:
            return (f"{flag} {path} is also {', '.join(clobbered)} -- refusing "
                    f"to overwrite an input with output made from it. Write it "
                    f"somewhere else, or run again without {flag.split()[0]} "
                    f"and redirect stdout.")
        if target in seen and seen[target] != flag:
            return (f"{seen[target]} and {flag} both name {path} -- refusing to "
                    f"write two outputs over one path, because the second "
                    f"replaces the first and the loss is silent.")
        seen[target] = flag
    return None


def canonical_base(base: Path, paths: dict[str, Path]) -> str:
    """Which canonical name `--base` picked out. Exactly one, or a ConfigError.

    Matched on the resolved path rather than on the string, so `./a.md` and
    `a.md` are one document and an operator is not asked to retype what they
    typed. Two matches is not a tie to break: the same file was passed twice, so
    the merge would be told to fold a document into itself, and the two counts
    get different messages because they are different mistakes.
    """
    wanted = base.expanduser().resolve()
    matches = [name for name, path in paths.items() if path.expanduser().resolve() == wanted]
    if not matches:
        raise ConfigError(
            f"--base {base} is not one of the sources: "
            f"{', '.join(str(path) for path in paths.values())}"
        )
    if len(matches) > 1:
        raise ConfigError(
            f"--base {base} matches {len(matches)} of the sources, so the same "
            "document was given more than once; each source must be a different file"
        )
    return matches[0]


def step(run: Run, name: str, call, console: Console):
    """Run one unit of work and record what became of it.

    Returns None on anything but success, and every caller checks. A step that
    failed has no value to hand back, and a placeholder would be this function
    inventing the answer the model did not give.

    The console is told the same four outcomes the report is told, from the same
    branches, so a `-v` transcript and the step list in the report cannot
    disagree about what happened. It is passed rather than reached for: this is
    the one place every unit of work goes through, and a module-level console
    would be a second piece of global state for a run to write to.
    """
    console.step(name)
    started = time.monotonic()
    try:
        value = call()
    except DryRun:
        run.steps.append(Step(name, PLANNED))
        console.skipped(f"{name}: planned, not called (--dry-run)")
        return None
    except FATAL as exc:
        # Recorded before the re-raise: a fault that will recur
        # identically on retry still aborts the run, but whatever `main` has
        # already measured -- a finished merge, prior decomposes, an earlier
        # verify pass -- is not the report's to discard. `Run.errored` is what
        # `exit_code` and `verdict_line` already read, so a FATAL fault here
        # renders exactly as an ordinary errored unit does, not as a special
        # case bolted on beside it.
        run.steps.append(Step(name, ERRORED, f"{type(exc).__name__}: {exc}"))
        console.failed(f"{name}: {type(exc).__name__}: {exc}")
        raise
    except SchemaFailure as exc:
        run.steps.append(Step(name, ERRORED, str(exc)))
        console.failed(f"{name}: {exc}")
        return None
    except Exception as exc:  # noqa: BLE001 - one bad unit errors one unit
        run.steps.append(Step(name, ERRORED, f"{type(exc).__name__}: {exc}"))
        console.failed(f"{name}: {type(exc).__name__}: {exc}")
        return None
    run.steps.append(Step(name, OK))
    console.done(name, seconds=time.monotonic() - started)
    return value


def skip(run: Run, name: str, why: str, console: Console) -> None:
    run.steps.append(Step(name, SKIPPED, why))
    console.skipped(f"{name}: {why}")


def pipeline(
    client: Client,
    run: Run,
    documents: dict[str, str],
    loaded: dict,
    base: str | None = None,
    policy: merge.MergePolicy | None = None,
    depth: str = config.DEFAULT_VERIFY_DEPTH,
) -> Run:
    """Merge if asked, then both verification directions. One order, one place.

    `policy` reaches all three model passes or none of them. The merge is told
    what it may rewrite; both verify passes are told the same thing, because a
    grader that does not know the level reads a licensed rewrite as invention.
    Defaulted here rather than required so that a `verify` run, which had no
    merge to set a policy for, still has one to grade against.

    The step order is not arbitrary: the source decomposes come before anything
    that needs the merge, so `--dry-run` can still count them when the merge
    itself was only planned.
    """
    # Written from the argument that decides the run's shape, in the one
    # function every caller goes through, so a `Run` can never carry a depth
    # other than the one it ran at. The report reads it to decide whether a
    # clean verdict may say "nothing was invented"; `Provenance` records
    # it separately from `settings`, which is the same fact taken from the
    # configuration rather than from the run.
    run.verify_depth = depth
    # Read before the merge runs, because the merge adds itself to `documents`.
    # Taken from the mapping rather than passed in: `main` built it under
    # canonical names and `merge.check_sources` has already agreed with it, so a
    # second list here would be a third opinion about what the sources are.
    sources = tuple(name for name in documents if name != MERGED)
    policy = policy or merge.MergePolicy()
    # What the merge declared it did, kept from the merge step so the forward
    # verdicts can be held against it further down. `()` covers both the
    # `verify` command and a merge that errored: in neither case did anything
    # declare anything to this run.
    dispositions: tuple[dict, ...] = ()
    decisions: tuple[dict, ...] = ()
    # The reconciler's measurement of the two texts, kept for the declaration
    # grader below. Bound here rather than in the `merge` branch so the name
    # exists on every path through this function.
    measured: reconcile.Reconciliation | None = None
    # Pass C's accumulator, and its switch. Handing this to `verify_claims` is
    # what turns salvage on at all -- see that function's docstring for why the
    # two are the same object. `run.unusable` itself rather than a local that
    # gets copied over later: a forward-pass drop has to be reported even when
    # the reverse pass never runs, and every path out of this function then
    # carries the record without having to remember to.
    ungraded: list[Unusable] = run.unusable

    if run.command == "merge":
        # The declared-loss denominator, computed here because it is a
        # fact about the sources and the report holds no document to derive it
        # from. Same call the merge prompt's rendering makes and the same call
        # `reconcile` counts, so the budget the report prints and the budget the
        # reconciler enforces cannot be fractions of different wholes. Only on
        # `merge`: on `verify` nothing declared anything and a denominator with
        # no numerator invites a ratio nobody measured.
        run.segments = sum(
            len(document.segments)
            for document in segment.segment_sources(
                {name: documents[name] for name in sources}
            )
        )
        # Set beside the denominator, from the same policy object the
        # reconciler is about to be handed, so the record cannot name one
        # ceiling while another decided the finding.
        run.declared_loss_budget = policy.declared_loss_budget
        merged = step(
            run,
            "merge",
            lambda: merge.merge_documents(
                client, documents, loaded["merge"], base=base, policy=policy,
                max_tokens=client.settings.max_tokens,
            ),
            client.console,
        )
        # The declared decisions and dispositions ride on the result and are the
        # reconciler's input; what every other pass needs is the document. The
        # base comes off it too, and off the result rather than off the argument
        # to this function: `base=None` here means the merge chose, and the
        # report has to say which document it chose and that nobody told it.
        if merged is not None:
            run.base, run.base_chosen = merged.base, merged.base_chosen
            dispositions = merged.dispositions
            decisions = merged.decisions
            run.decisions = decisions
            # Carried whatever the level, because the schema only offers the
            # key at `open` and a merge that emitted none leaves this empty.
            # Reading it unconditionally means a level that gains the licence
            # later needs no change here, and a payload that carries one where
            # it should not is visible in the report rather than discarded.
            run.additions = merged.additions
            # The merge's own warning about its inputs. Carried at every
            # level: this is about the documents rather than the licence.
            run.mismatch = merged.mismatch
            run.title_policy = policy.title_policy
            run.sources_with_a_title = sum(
                1 for document in segment.segment_sources(
                    {name: documents[name] for name in sources})
                if any(item.kind == segment.TITLE for item in document.segments)
            )
            run.truncations = merged.truncations
        merged = None if merged is None else merged.document
        if merged is not None:
            documents[MERGED] = merged
            run.merged = merged
            # `merge.example_content_leaks` before anything else looks at this text.
            # An earlier run recorded it on 73 units and `src/` called it on none, so the
            # detector that caught qwen3:4b returning `merge.md`'s illustration
            # instead of the documents has never run on a document a user
            # merged. This was found and fixed here.
            #
            # Here rather than inside `merge_documents` so that it reads the
            # text the rest of the pipeline reads, and before the reconciler so
            # that a merge which returned the prompt is a finding even if
            # reconciliation then fails on it. One finding per marker, and the
            # detail names the marker rather than quoting the merge: the whole
            # document is the evidence and it is on disk beside the report.
            #
            # Two halves, one kind. The first reads the merged document for
            # the example's content words; the second reads what the records
            # say about themselves, because a model can merge the real
            # documents faithfully -- no marker anywhere in the text -- and
            # still write the illustration's argument into its own `reason`.
            # That happened, and the first half was green over it, which is
            # not a failure of its claim but the edge of it.
            run.leaks = tuple(
                reconcile.Finding(
                    reconcile.PROMPT_EXAMPLE_LEAK,
                    f"the merged document contains {marker!r}, which is in "
                    f"`merge.md`'s worked example and in neither source; the "
                    f"model returned the illustration rather than the documents",
                )
                for marker in merge.example_content_leaks(merged)
            ) + tuple(
                reconcile.Finding(
                    reconcile.PROMPT_EXAMPLE_LEAK,
                    f"the reason given for {where} is {clause!r}, which is "
                    f"`merge.md`'s worked example word for word; the record "
                    f"argues the illustration's case rather than this merge's",
                    segment=where,
                )
                for where, clause in merge.example_reason_leaks(
                    tuple(dispositions) + tuple(decisions))
            )

        # The reconciler, held against the two texts and what the merge said it
        # did. Until this line existed,
        # `reconcile.findings` was called from no module in the shipped package,
        # so eight checks were written, tested against 72 recorded merges, and
        # reached no report and no exit code.
        #
        # A step rather than a bare call, unlike `grade_declarations` below,
        # even though it asks nothing of a model. Two reasons, and both are
        # about being seen: the step list is this report's own denominator, so
        # a reader can tell a merge the reconciler passed from one it never
        # looked at; and if it raises, the run has to come back inconclusive
        # rather than clean. Swallowing the exception would restore exactly the
        # behaviour this task removed — a clean report from a check that was
        # never made.
        #
        # It runs whether or not anything was declared. Under the disposition model silence is
        # the claim: an empty `dispositions` asserts that every source segment
        # survives character for character, and check 2 is the string comparison
        # that tests that assertion.
        #
        # Before the four decompose and verify calls, so a merge that is
        # mechanically wrong is known before the run spends a model on it.
        # Held rather than discarded: `grade_declarations` below asks it about
        # the declarations no claim reaches, and asking it a second time would
        # be a second measurement of the same two texts that could disagree
        # with the one the findings were drawn from. Assigned inside the step
        # so a reconciler that raises still comes back as a failed step rather
        # than an exception nobody catches.
        def reconciled() -> reconcile.Reconciled:
            nonlocal measured
            measured = reconcile.reconcile({n: documents[n] for n in sources}, merged)
            return reconcile.findings(
                measured,
                dispositions,
                fidelity=policy.fidelity,
                title_policy=policy.title_policy,
                # `run.base`, not the `base` argument: `base=None` means the
                # merge applied the default, and the title policy's `keep-base` check has to
                # be made against the document that actually governed the
                # structure rather than against the absence of a flag.
                base=run.base or "",
                budget=policy.declared_loss_budget,
            )

        if merged is not None:
            run.reconciled = step(run, "reconcile", reconciled, client.console)
            # Only `synthesise` permits a written title, and
            # `reconcile` cannot grade one: it grades no claims by design. So a
            # title this project did not copy goes to the pass that reads both
            # texts. Costs one short call, and only when the model chose to
            # write rather than copy -- the other two policies never reach it.
            if (policy.title_policy == "synthesise"
                    and run.reconciled is not None and measured is not None):
                def title_checked() -> reconcile.Reconciled:
                    titles = tuple(
                        item.text
                        for coverage in measured.coverages
                        for item in reconcile.titles_of(coverage.document.segments)
                    )
                    written = reconcile.titles_of(measured.merged)
                    if not written:
                        return run.reconciled
                    finding = merge.verify_title(
                        client, written[0].text,
                        {n: documents[n] for n in sources}, titles)
                    if finding is None:
                        return run.reconciled
                    return replace(run.reconciled,
                                   findings=run.reconciled.findings + (finding,))
                # Assigned only on success. `step` returns None on
                # anything else, and this field already holds the
                # reconciliation line 825 produced -- so writing the result
                # straight back discarded nine mechanical checks that had
                # already run, on the failure of one short call that can only
                # ever *add* a finding. The report then said "Structure: not
                # checked", which was false: it had been checked, and the
                # result was thrown away.
                #
                # The uncertainty the failure creates is real and is already
                # recorded: `run.errored` carries the step and drives exit 2,
                # so a reader is told the title was not graded without also
                # being told nothing else was.
                graded = step(run, "title", title_checked, client.console)
                if graded is not None:
                    run.reconciled = graded
            # The other half of `measured`, and the reason this line exists at
            # all: `Reconciliation.order` was computed on every run and never
            # read by any module in `src/`. Same shape as the eight
            # checks the comment above describes, one tier milder -- it is not
            # a check that never ran, it is a correct measurement nobody was
            # shown. Assigned outside the step because a
            # reconciler that raised leaves `measured` as None and there is
            # nothing to report.
            if measured is not None:
                run.order = measured.order
                # Same shape and the same reason: a correct measurement
                # that nothing was showing. Taken from `measured` rather than
                # from `run.reconciled` so it still arrives when the findings
                # step failed, since it is a fact about the two texts and not
                # about the reconciliation.
                run.added_breaks = measured.added_breaks
    else:
        merged = documents.get(MERGED)

    # A statement credited to a source that does not carry it. Here, on
    # both commands and before the depth branches, because it reads the texts
    # and asks no model: `coverage` never reads the merged document back and
    # the decomposer rightly files "the guide states X" as a claim about X, so
    # this is the only place an invented attribution can be seen at all.
    if merged is not None:
        run.attributions = reconcile.attribution_findings(
            {name: documents[name] for name in sources}, merged,
            shown={name: run.display(name) for name in sources})
        run.attributions_checked = True

    # How each document writes its decimals, and the numerals that break it.
    # Beside the attributions for their reasons: it reads the texts
    # alone, so it runs on both commands, at both depths and every level, and
    # a model reads "4,5" as the same quantity as "4.5" and would never say.
    # The sources are read even where no merge exists, since a source's own
    # "17.560" is worth a warning before anything is merged from it.
    checked = numerals.check(
        {name: documents[name] for name in sources}, merged, MERGED,
        shown={name: run.display(name) for name in [*sources, MERGED]})
    run.number_format = checked.findings
    run.conventions = checked.conventions
    run.number_format_checked = True

    # The forward half, at whichever depth was asked for. `coverage` fuses the
    # two calls per source into one and is the only difference the sources see;
    # everything downstream reads `run.claims` and `run.forward` and cannot
    # tell which produced them, which is the point -- the depth must change
    # what is *checked*, never how a result is reported.
    #
    # The depth alone, with no second condition. This read `and merged is not
    # None`, which made `--dry-run` fall into the `full` branch every time:
    # the merge is only *planned* under a dry run, so `merged` is None, and
    # the plan then named a `decompose source_a.md` call this depth never
    # makes and neither skip below appeared. A plan that describes a different
    # pipeline from the one the same flags would run is worse than no plan.
    # The real "there is no merged document" case is handled inside,
    # where it can say so.
    covering = depth == config.COVERAGE_DEPTH
    # A fused call carries the merged document, so it has nothing to ask
    # without one -- and a merge that errored must not be followed by one call
    # per source comparing it against an empty string, which would spend real
    # money to report every claim MISSING. `--dry-run` is the exception and is
    # the whole point of the flag: nothing is asked of anybody, and what is
    # being printed is the set of calls this configuration would make.
    if covering and merged is None and not client.settings.dry_run:
        for name in sources:
            skip(run, f"cover {run.display(name)}",
                 "there is no merged document to cover against", client.console)
        skip(run, "verify (forward)", "there is no merged document to check against",
             client.console)
    elif covering:
        covered: list = []
        for name in sources:
            outcome = step(
                run,
                f"cover {run.display(name)}",
                lambda name=name: verify_coverage(
                    client, documents[name], name, documents,
                    loaded.get("verify_coverage"), policy=policy),
                client.console,
            )
            if outcome is None:
                continue
            claims, verdicts = outcome
            run.claims[name] = claims
            covered.extend(verdicts)
        run.forward = covered
        if len(run.claims) < len(sources):
            # Said once, here, rather than left to be inferred from a short
            # claim list. One fused call carries a whole source, so losing it
            # loses that source's coverage entirely.
            skip(run, "verify (forward)", "a source could not be covered",
                 client.console)
    else:
        for name in sources:
            claims = step(
                run,
                f"decompose {run.display(name)}",
                lambda name=name: decompose_text(client, documents[name], name, loaded["decompose"]),
                client.console,
            )
            if claims is not None:
                run.claims[name] = claims

    source_claims = [claim for name in sources for claim in run.claims.get(name, [])]
    if covering:
        pass
    elif merged is None:
        skip(run, "verify (forward)", "there is no merged document to check against",
             client.console)
    elif len(run.claims) < len(sources):
        skip(run, "verify (forward)", "a source could not be decomposed", client.console)
    else:
        verdicts = step(
            run,
            "verify (forward)",
            lambda: verify_claims(
                client, source_claims, documents, SOURCE_TO_MERGED,
                loaded[SOURCE_TO_MERGED], policy=policy, unusable=ungraded,
            ),
            client.console,
        )
        run.forward = verdicts or []

    # Grading the declarations makes no call, so it is not a step and cannot
    # error a run: it reads the forward verdicts and the sources and returns.
    # It runs even when the forward pass was skipped or errored, because a merge
    # that declared six departures and had none of them checked has to say so —
    # `unchecked` is a result, and suppressing the section would report the
    # merge's own account of itself as though nobody had questioned it.
    if dispositions:
        run.declarations = grade_declarations(
            dispositions, run.forward, source_claims, documents,
            located=measured,
            findings=None if run.reconciled is None else run.reconciled.findings,
            # Threaded so a covering reconciliation predicts the CONTRADICTED
            # its own construction guarantees. Every level below `open`
            # answers exactly as it did before, because `reconcile.COVERS` is
            # false for all of them.
            fidelity=policy.fidelity,
        )

    # `coverage` has no reverse pass. That is the depth's defining property and
    # the reason it is cheaper, so it is recorded as a skip with its reason
    # rather than left as two steps that quietly never appear: a reader
    # comparing two reports has to be able to see that this run never asked
    # whether the merge invented anything.
    #
    # Before the missing-document case rather than after it, because at this
    # depth the depth is always the reason: a coverage run skips both steps
    # whether or not a merge came back, and a `--dry-run` plan -- where
    # `merged` is None by construction -- has to name the two calls it is not
    # going to make for the reason it is not going to make them.
    if covering:
        skip(run, f"decompose {run.display(MERGED)}",
             "--verify-depth coverage does not read the merged document back",
             client.console)
        skip(run, "verify (reverse)",
             "--verify-depth coverage does not check for invention",
             client.console)
        return run

    if merged is None:
        skip(run, f"decompose {run.display(MERGED)}", "there is no merged document",
             client.console)
        skip(run, "verify (reverse)", "there is no merged document", client.console)
        return run

    merged_claims = step(
        run,
        f"decompose {run.display(MERGED)}",
        lambda: decompose_text(client, documents[MERGED], MERGED, loaded["decompose"]),
        client.console,
    )
    if merged_claims is None:
        skip(run, "verify (reverse)", "the merged document could not be decomposed",
             client.console)
        return run
    run.claims[MERGED] = merged_claims

    # Check 9's claim-level half, and the only place in the pipeline it can
    # stand: it reads the merged document's claims, which do not exist until
    # the line above. The reconciler ran two hundred lines earlier, before the
    # four model passes, so that a mechanically wrong merge costs nothing --
    # moving it down here to collect this would pay for every merge with four
    # calls to find a fault the sources alone already prove. `run.leaks` sets
    # the precedent for a finding the reconciler does not produce and the
    # report carries anyway.
    #
    # `merge` only, like the reconciler itself. `verify` has a merged document
    # and its claims too, and the check would work there -- but every
    # `tests/fixtures/*/expected.json` declares an `expected_exit_code` for a
    # `verify` run derived from its probes alone, and a document-level finding
    # is not derivable from probes. Firing here on `verify` would
    # make the new fixture's own answer key false rather than catch anything
    # the corpus contains: measured over 14 fixtures x 3 samples, no merged.md
    # in the corpus restates a claim. Widening it needs a declarable field in
    # the fixture schema, and that is a change to the answer keys, not to the
    # tool.
    if run.command == "merge":
        run.restated = reconcile.restated_findings(merged_claims)

    run.reverse = step(
        run,
        "verify (reverse)",
        lambda: verify_claims(
            client, merged_claims, documents, MERGED_TO_SOURCES,
            loaded[MERGED_TO_SOURCES], policy=policy, unusable=ungraded,
        ),
        client.console,
    ) or []
    return run


def prepare_merge(
    documents: dict[str, str],
    depth: str = config.DEFAULT_VERIFY_DEPTH,
) -> tuple[dict[str, str], dict[str, prompts.Prompt], tuple[tuple[str, int, str], ...]]:
    """Turn documents already in memory into what `pipeline` needs. Nothing here opens a file.

    `main` used to have these five lines inline, between the point the command
    line was parsed and the point `pipeline` was called, and that was fine as
    long as `main` was the only caller. It stopped being fine the day a web
    server needed to run a merge starting from two strings already in memory
    rather than from two paths on disk: reimplementing this block beside
    `main`'s copy is exactly how the two would drift, silently, while
    `tests/test_cli.py` kept passing the whole time, because that suite only
    ever exercises `main`'s copy. So this is the one copy, and `main` below
    calls it rather than inlining it a second time.

    `documents` is keyed however the caller likes -- an uploaded filename, a
    label typed into a form, a path string turned to text -- and the *order*
    the keys were inserted in is the order the sources are treated as given,
    because a `dict` keeps that order and this function trusts it exactly the
    way `main` trusts `argv`. The first thing done here is throwing that key
    away and replacing it with the canonical one `merge.source_names` assigns
    to that position: `source_a.md`, `source_b.md`, and so on. See the module
    docstring, `cli.py:10-19` -- every figure this project has published was
    measured with the model shown those names in the prompt, and a caller's
    own filename reaching the prompt instead would make the run a
    configuration nothing was measured under. There is deliberately no
    argument here to opt out of the rename.

    That same call is also the arity guard. `merge.source_names` raises
    `MergeError` itself, below `merge.MIN_SOURCES` or above `merge.MAX_SOURCES`
    (`merge.py:257-266`), so a caller with zero, one or fifty documents is refused
    here without a second copy of either number. `main` still checks the arity
    before this function is ever reached, but through `parser.error` -- an
    argparse call that prints the usage line and exits the process, which has
    no meaning for a caller that is not a command line reading `argv`. That
    half stays in `main`, entangled with argparse as it always was; the check
    itself does not need to stay there, because `source_names` already makes
    it, and a web server that skips the friendlier message still gets refused
    rather than crashing three calls later on a document that was never there.

    The internal order still matters even though nothing here writes to a
    console. The fence scan runs and is fully computed before
    `check_sources` (`merge.py:874`) gets the chance to raise, the same order
    `main` ran both of these lines in before this function existed. It buys
    nothing observable when `check_sources` accepts -- the caller gets the
    same tuple back regardless of which of the two ran first -- but it means
    that a document which is both fence-broken and empty is refused with the
    same message either way. `check_sources` itself can only actually refuse a
    blank source here: every entry in `mapped` already carries an exactly
    canonical name by construction, so the name-shape half of what it checks
    can never fire through this call path. One real behaviour did move: `main`
    used to print each fence warning to the console the instant it was found,
    while `check_sources` had not run yet and could still fail a moment later;
    now the printing happens after this function returns, so on that one
    coincidence -- an unclosed fence and an empty source in the same run --
    the warning that used to land on stderr just ahead of the fatal error no
    longer does. No test depends on it, and the run still ends the same way:
    refused, with the same message.

    The prompts are loaded unconditionally, on `verify` as much as on `merge`
    -- `loaded["merge"]` goes unread on a `verify` run, but a run that decides
    its own shape from which prompt files happen to exist on disk is one more
    way for two invocations of the same command to differ. Which prompts those
    are follows from `depth`, and that is the one thing about the set that is
    allowed to vary, because the depth is an argument rather than a fact about
    the filesystem.

    **Loading here is what makes a malformed prompt cheap.** The point of the
    preload is that a run dies before the merge is paid for rather than three
    calls in. `verify_coverage` was loading its own prompt inside the
    per-source loop, so at `coverage` the one prompt the depth actually needs
    was the one prompt nothing checked until the merge had already been bought.
    It joins the set; the two verify prompts a coverage run can never
    reach leave it, because a preload of a file nothing will open is not an
    early failure, it is an unrelated one.

    No `settings` parameter, unlike the shape this was sketched from: none of
    the five things this function does reads it, and `depth` arrives as a
    value rather than as the object it was read from for that reason. `main`
    still resolves `settings` for the client, the banner and the merge policy,
    all of it downstream of this call.
    """
    canonical = merge.source_names(len(documents))
    mapped = dict(zip(canonical, documents.values()))
    # An unclosed fence swallows the rest of the document into one code
    # block. Harvested before anything is scored, so the reader is told what
    # the segmenter saw rather than left to infer it from a block that runs to
    # the end of the file.
    unclosed_fences = tuple(
        (name, line, reason)
        for name, text in mapped.items()
        for line, reason in segment.segment_document(text, "a").skipped
        if reason.startswith("fence opened")
    )
    merge.check_sources(mapped)
    loaded = {"merge": prompts.load("merge")}
    if depth == config.COVERAGE_DEPTH:
        loaded["verify_coverage"] = prompts.load("verify_coverage")
    else:
        loaded["decompose"] = prompts.load("decompose")
        loaded[SOURCE_TO_MERGED] = prompts.load("verify")
        loaded[MERGED_TO_SOURCES] = prompts.load("verify_reverse")
    return mapped, loaded, unclosed_fences


def one_merge(settings, paths: dict, documents: dict, loaded: dict,
              base: str | None, console: Console) -> tuple[Run, dict]:
    """One complete merge-and-verify at whatever fidelity `settings` carries.

    `documents` is copied because `pipeline` adds the merged document to the
    mapping it is given. Four levels sharing one mapping would have the second
    level verifying the first level's merge, which is the kind of failure that
    produces a plausible table.
    """
    run = Run(command="merge")
    run.paths = {name: str(path) for name, path in paths.items()}
    client = Client(settings, console=console)
    started = time.monotonic()
    pipeline(client, run, dict(documents), loaded, base,
             merge.MergePolicy.from_settings(settings),
             depth=settings.verify_depth)
    run.provenance = Provenance(
        settings=settings, client=client, roles=ROLES,
        duration_seconds=time.monotonic() - started,
        base=run.base, base_chosen=run.base_chosen,
    )
    return run, as_dict(run)


def run_sweep(args, settings, paths: dict, documents: dict, loaded: dict,
              base: str | None, console: Console) -> int:
    """Every level, one report, and nothing written unless all land.

    "Every level" is every level `sweep.plan` kept for this backend, decided
    before the first call; a level it left out is said on stderr here, before
    anything runs, and again under the table.

    A level that raises does not stop the sweep: the remaining levels still run,
    so the refusal at the end can name every level that failed instead of the
    first one. Nothing reaches disk until `refuse_after_running` has passed,
    because a partial sweep on disk reads exactly like a complete one.
    """
    runs, left_out = sweep.plan(settings)
    for level, reason in left_out.items():
        console.warn(f"--sweep-fidelity leaves out {config.fidelity_name(level)}"
                     f", which this backend refuses: {reason}")
    for level, at in runs.items():
        # The banner above was printed for the resolved level, which grants
        # nothing, so a grant a row carries is said here or not at all -- and
        # an automatic grant is never silent.
        tools = config.granted_web_tools(at.command)
        if tools and not config.granted_web_tools(settings.command):
            console.warn(f"fidelity {config.fidelity_name(level)}: the model is "
                         f"granted {', '.join(tools)}, and a query or a fetch "
                         f"may carry text from these documents")
    rows: list[dict] = []
    reports: dict[str, dict] = {}
    merged: dict[str, str] = {}
    # `--max-calls` is a ceiling on an invocation, and a sweep is one
    # invocation. Each level gets its own Client, so the counter would reset
    # once per level and the flag would quietly mean that many times what it
    # says.
    spent = 0
    for level, at in runs.items():
        # Through the console, which writes to stderr. This was a bare `print`
        # to stdout, and the README's "stdout is the report and nothing else"
        # was false for exactly one line in exactly one mode -- so `--sweep-
        # fidelity > report.md` put a progress line per level inside the
        # artefact.
        console.done(f"fidelity {config.fidelity_name(level)}: merging")
        at_level = replace(at, max_calls=settings.max_calls - spent)
        try:
            run, reported = one_merge(at_level, paths, documents, loaded, base, console)
        except FATAL as exc:
            # A fatal fault is one that will be identical on the next call --
            # that is what puts it in FATAL rather than erroring a single unit.
            # So the sweep stops here rather than spending the levels that are
            # left proving it three more times. The levels never reached are
            # missing from `rows`, which `incomplete` reports as such.
            print(f"  {level}: {type(exc).__name__}: {exc}", file=sys.stderr)
            rows.append({"fidelity": level, "settled": False,
                         "errored_steps": [f"{type(exc).__name__}: {exc}"]})
            break
        reports[level] = reported
        rows.append(sweep.row(level, reported))
        spent += ((reported.get("provenance") or {}).get("counts") or {}).get("calls", 0)
        if run.merged is not None:
            merged[level] = run.merged

    refusal = sweep.refuse_after_running(rows, list(runs))
    if refusal:
        return fail(refusal, coloured=console.enabled)

    print(sweep.render(rows, left_out), end="")

    payload = sweep.as_dict(rows, reports,
                            {name: str(path) for name, path in paths.items()},
                            left_out)
    try:
        if args.sweep_dir is not None:
            args.sweep_dir.mkdir(parents=True, exist_ok=True)
            for level, text in sorted(merged.items()):
                (args.sweep_dir / f"merged.{level}.md").write_text(text, encoding="utf-8")
                (args.sweep_dir / f"report.{level}.json").write_text(
                    json.dumps(reports[level], indent=2) + "\n", encoding="utf-8")
        if args.json_path is not None:
            args.json_path.write_text(json.dumps(payload, indent=2) + "\n",
                                      encoding="utf-8")
    except OSError as exc:
        return fail(f"cannot write the sweep: {exc.strerror or exc}",
                    coloured=console.enabled)

    # The worst level, not an average. A sweep is one measurement per level
    # and the caller wants to know whether any of them found something.
    return max(r["exit_code"] for r in rows)


# A CamelCase class name and its colon, at the front of a step's recorded
# detail. `step` writes `f"{type(exc).__name__}: {exc}"` so the report can name
# the class; the summary below has to say what went wrong to somebody who does
# not write Python, and `WindowUnknown` is not that. Two capitals are required
# so an ordinary sentence opening `Note: ` or `Error: ` is left alone.
CLASS_PREFIX = re.compile(r"^[A-Z][a-z0-9_]*(?:[A-Z][A-Za-z0-9_]*)+:\s*")

# What the run amounted to, by exit code, in the words a person would use.
# `report.exit_code` decides the number; this decides nothing and only says it.
#
# 3 is the page's `advice.record` word for word, and `test_contract_parity`
# holds the two equal. It had no row here, and the lookup below fell back to
# 2's, so a finished run whose merged document the tool had found sound ended
# "Could not complete. Part of this run did not finish".
OUTCOME = {
    0: ("Done.", "Nothing was dropped, contradicted or invented."),
    1: ("Finished, with problems.", "The report lists what was found."),
    2: ("Could not complete.", "Part of this run did not finish, so the report "
        "does not establish that the claims it did check are all there were."),
    RECORD_ONLY: ("Finished, with record findings.",
                  "The document is sound as far as this tool looked; the "
                  "merge's account of itself is not."),
}

# The headline's colour. 3 is yellow, the HTML banner's amber, because the
# document is sound as far as the tool looked and red would say it is not.
TINT = {0: GREEN, 1: RED, 2: YELLOW, RECORD_ONLY: YELLOW}

# Both tables are read with a bare subscript, so a code without a row is a
# failure at import and never a borrowed sentence at the end of a run.
# `html_report.BANNER` is held to the same tuple for the same reason.
assert set(OUTCOME) == set(TINT) == set(EXIT_CODES), (
    f"every exit code needs an outcome and a colour: OUTCOME has "
    f"{sorted(OUTCOME)}, TINT has {sorted(TINT)}, the tool returns "
    f"{sorted(EXIT_CODES)}")


def plain(detail: str) -> str:
    """One step's failure, without the exception class in front of it."""
    return CLASS_PREFIX.sub("", detail).strip()


def summarise(run: Run, code: int, *, output: Path | None, coloured: bool,
              piped: bool, stream=None) -> None:
    """The last thing a run says, on stderr, in plain words. Never on stdout.

    This exists because of a real run that was correct in every respect and
    still failed its operator. The merge step errored against a cold endpoint,
    nothing was written to the `-o` path they had named, the process exited 2 as
    it should, and stdout was redirected to a file -- so the terminal showed
    nothing for 137 seconds and nothing at the end. The exit code was the only
    channel left, and an exit code is not a channel a person reads.

    So the exit code becomes an echo of this block rather than the primary
    account of the run. The documented codes do not change; what changes
    is that they are now also said out loud. And it is stderr for the reason the
    whole of this module is careful about: stdout carries the report, is piped
    and diffed, and every published figure was measured against it.
    """
    # Resolved here rather than in the signature: a default argument is bound
    # once, at import, and would hold the original stderr for the life of the
    # process. Anything that redirects the stream -- a test, a caller embedding
    # this -- would then be talked past rather than to.
    stream = sys.stderr if stream is None else stream

    def line(text: str, code_: str = "") -> None:
        print(colour(text, code_, coloured and bool(code_)), file=stream)

    headline, gloss = OUTCOME[code]
    # The failure classes this run actually looked for. A `coverage` run read
    # nothing back out of the merged document, so naming invention here would
    # be the terminal making the claim `report.lost_classes` refuses to make
    # two lines earlier in the same output. The fourth surface of the
    # same sentence, and the one `verdict_line` does not reach.
    #
    # `checked_for_invention`, not `detects_invention`: the question is whether
    # this run asked, and a `full` run whose merged document yielded no claims
    # did not ask it either. Same predicate as `report.lost_classes`, so
    # the sentence here and the headline in the report cannot disagree about
    # which failure classes were examined.
    #
    # The wide form is `OUTCOME[0]`'s own gloss rather than a second copy of
    # it. Two copies is what this whole block is about: the one that was here
    # was identical to the table's and would have been the only one a reader
    # ever saw, so the table's could have drifted for good without a single
    # surface changing.
    if run.planned:
        # A dry run made no call, so it has nothing to report a verdict about.
        # `code` is 0 only because a plan takes no verdict colour (see the call
        # site, a few lines above where `summarise` is called); reusing
        # OUTCOME[0]'s clean headline here would claim a check that never ran.
        # The count is the same one the report's own plan prints, so the
        # terminal and `## Planned calls` cannot disagree about it.
        headline = "Dry run:"
        gloss = (f"{len(run.planned)} call(s) planned, none made. "
                 "Nothing was checked.")
    else:
        clean = (OUTCOME[0][1].rstrip(".")
                 if run.checked_for_invention
                 else "Nothing your documents state was dropped or contradicted")
        if code == 0:
            gloss = f"{clean}."
            if not run.detects_invention:
                gloss += (" Nothing read the merged document back, so invention "
                          "was not checked.")
        # A clean run over a source that produced no claims is not the clean run
        # this sentence describes. `verify` exits 2 for it and never reaches here;
        # `merge` still exits 0, because the reconciler did check the source
        # structurally -- but "nothing was dropped" would be claiming more than
        # was looked at, so the gloss says what the check rested on.
        if code == 0 and run.unexamined_sources():
            named = ", ".join(run.unexamined_sources())
            gloss = (f"{clean} among the claims extracted -- but {named} produced "
                     f"no claims, so coverage for it rests on the structural "
                     f"check alone.")
        if code == 2 and inconclusive_for_retrieval_alone(run):
            gloss = ("The merge was asked to look its facts up and retrieved "
                     "nothing, so this is not a sourced merge; read it as a merge "
                     "at open, or re-run it.")
        elif code == 2:
            headline, gloss = finished_inconclusive(run) or (headline, gloss)
    tint = TINT[code]
    line("")
    line(f"{headline} {gloss}", tint)

    # The two suspended guarantees, on every exit code, because a caveat that
    # appears only on a clean run is a caveat missing from the report anyone
    # reads carefully -- `report.invention_sentence` and `app.js`'s
    # `suspendedGuarantee` both say so in those words and both already do it.
    # This surface said the first one on exit 0 alone and the second one never,
    # so the reader most likely to act on a report -- the one whose run just
    # failed -- was the one not told which guarantee was suspended.
    #
    # Indented lines rather than more of the headline: the headline is the
    # verdict and these are conditions on it, which is the shape the queued
    # claims and the written-document notice below already use. Uncoloured, for
    # the reason the queue line gives: nothing failed here.
    #
    # Said once, not twice. At exit 0 it continues the gloss above, because
    # that sentence is the one a reader takes away and "Nothing your documents
    # state was dropped or contradicted." alone reads as a full clean result.
    # At every other code the gloss is about the failure and the caveat needs a
    # line of its own -- which is the case that was missing, not the clean one.
    if not run.detects_invention and code != 0:
        line("  nothing read the merged document back, so invention was not "
             "checked; a clean result would mean your content was carried "
             "across, not that nothing was invented")
    if run.declared_additions:
        line(f"  {len(run.declared_additions)} statement(s) in the merge came "
             f"from the model's own knowledge and could not be checked against "
             f"your documents; see `## Added from outside the documents`")
    # What `sourced` achieved, not only what it permitted. The banner
    # at the top of the run said which tool was granted; this is the other
    # half, and the terminal is where an operator who never opens the report
    # learns it. Yellow for the two states that leave a citation unchecked,
    # because neither is a failure of the documents and both change what the
    # reader may believe about the sources.
    #
    # Opens on the report's own words, `retrieval_lead`, so the terminal and
    # the verdict cannot name one state two ways.
    achieved = retrieval_outcome(run)
    # The merge's calls on a merge, and the words say which.
    turns = retrieval_turns(run)
    calls = retrieval_calls_word(run)
    if achieved == usage.RETRIEVED:
        line(f"  {retrieval_lead(achieved)} {turns.with_tools} of {turns.calls} "
             f"{calls} took the turns a retrieval costs; which citation each "
             f"retrieval backs is not recorded")
    elif achieved == usage.NOT_RETRIEVED:
        line(f"  {retrieval_lead(achieved)} None of {turns.calls} {calls} took "
             f"the turns a retrieval costs, so every source the merge names is "
             f"a recollection", YELLOW)
    elif achieved == usage.UNMEASURED:
        silent = turns.unmeasured if turns is not None else 0
        said = (f"{silent} {calls} reported no turn count" if silent
                else "No call reported a turn count")
        line(f"  {retrieval_lead(achieved)} {said}, which is not the same as "
             f"nothing retrieved", YELLOW)

    for errored in run.errored:
        line(f"  {errored.name} did not finish: "
             f"{plain(errored.detail or 'no reason was recorded')}")

    # What was found, and not only that something was. `Finished, with problems.
    # The report lists what was found.` is true and useless: it sends a reader
    # to a document to learn whether one link lost a character or forty claims
    # went missing, and those are not the same news. The counts come from
    # `report.what_was_found`, which is what the verdict line is counted from,
    # so the terminal and the document cannot disagree about how many there were.
    found = what_was_found(run)
    for entry in found:
        line(f"  {entry}", tint)
    if code == 1 and not found and run.over_budget:
        # The one exit 1 with nothing to enumerate: the merge declared more loss
        # than the budget allows, which is a fact about the volume rather than
        # about any one claim.
        line("  the merge declared more loss than this fidelity level allows; "
             "`## Verdict` has the figures", tint)
    if run.queued:
        # Not a finding and not coloured. These are claims the merge said it was
        # dropping, so nothing failed -- but a run that reports "Done." over
        # thirty declared drops has told its operator less than it knows.
        line(f"  {len(run.queued)} claim(s) the merge declared dropped are "
             f"listed under `## Review queue`")
    if run.number_warnings:
        # Not a finding and not coloured, for the queue's reason.
        line(f"  {len(run.number_warnings)} number-format warning(s), on numerals "
             f"that could be misread, are listed under `## Number format`")

    # The single worst moment in the run this block was written for: a `-o` path
    # was named, no file appeared, and nothing said so. `verify` composes
    # nothing and is left out, because "no merged document was written" is not
    # news about a command that never writes one.
    if run.command == "merge":
        if run.merged_written_to:
            line(f"  merged document written to {run.merged_written_to}")
        elif output is not None:
            line(f"  nothing was written to {output}: the merge step did not "
                 f"produce a document", tint)
        elif run.merged is not None:
            line("  the merged document is in the report, under "
                 "`## Merged document`")
        else:
            line("  no merged document was produced", tint)

    # Only when they cannot see it. If stdout is the same terminal, the report
    # is already on the screen above this block and saying where it is would be
    # noise.
    if piped:
        line(f"  the full report went to stdout; exit code {code}")
    else:
        line(f"  exit code {code}")


def fail(message: str, *, coloured: bool) -> int:
    """One refusal, on stderr, and the exit code that goes with it.

    Every `print(..., file=sys.stderr); return 2` in this module came through
    here once colour arrived, because ten copies of the same two lines is ten
    places for the word `error:` to end up a different colour or a different
    word. The text is unchanged -- `error: ` and then the message -- so anything
    that was grepping this stream still matches.

    **All of it is red, not the prefix.** The messages that matter here are the
    long ones: an HTTP status, the endpoint, and for a 5xx the origin's own JSON
    body underneath it. One red word in front of ten grey lines does not read as
    an error. `coloured` is the decision taken for stderr -- see `main`, where
    taking it from stdout was the reason no error this tool printed under
    `> report.md` was ever red.
    """
    print(colour(f"error: {message}", RED, coloured), file=sys.stderr)
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Before anything reads `args.colour`, which only the subparsers define.
    # stdout, at exit 0: this is `-h` reached by a different route, and a reader
    # who pipes it into a pager should get the same bytes either way.
    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "serve":
        # **The import is here and may never move.** `llossless.web` must not
        # be in `sys.modules` after a complete `llossless merge` run, which is
        # the operator's stated requirement that the command line works
        # standalone with no web interface installed, and which
        # `test_a_complete_merge_never_loads_the_web_package`
        # (`tests/test_cli.py:4718`) asserts against a real merge with a
        # paired must-fire probe beside it. A module-scope `from . import web` added
        # "just to register the route" would break it silently -- the merge
        # would still work, and nothing but that test would notice.
        # `merge.verify_title` (`merge.py:746`) defers an import for a
        # different reason in the same shape; this is the pattern.
        #
        # Returned before `args.colour` is read, because `serve` is not one of
        # the subparsers that defines it. That ordering is the reason this
        # branch is here rather than beside the other command branches below.
        from .web.jobs import FROM_ENVIRONMENT
        from .web.server import serve as serve_http

        return serve_http(
            host=args.host,
            port=args.port,
            work_dir=args.work_dir,
            workers=args.workers,
            # Three values and two translations. `args.retention is None` is
            # argparse saying the flag was absent, which is not an answer about
            # documents at all -- it is handed on as `FROM_ENVIRONMENT` so that
            # `serve` reads `LLOSSLESS_RETENTION`, and falls back to the
            # default only when that says nothing too. A flag that *was* typed
            # wins outright, and 0 means keep: `None` is the job layer's
            # spelling of "keep forever" and a float is what the flag takes, so
            # the translation happens here rather than by `--retention`
            # accepting a word -- a flag that took either a number or the
            # string `never` would be a flag whose type argparse cannot check.
            retention_seconds=(
                FROM_ENVIRONMENT if args.retention is None
                else None if args.retention <= 0
                else args.retention),
        )

    # Two decisions, not one, because they are two streams: the common case is
    # a report redirected into a file while the terminal still shows progress,
    # and one answer for both would either strip the colour off the terminal or
    # write escape sequences into the file.
    report_colour = supports_colour(sys.stdout, args.colour)
    console = Console(sys.stderr, verbosity=args.verbose,
                      enabled=supports_colour(sys.stderr, args.colour))
    # Everything else in this function that colours anything is writing to
    # stderr, so it takes stderr's answer. It used to take stdout's, which is
    # False on the invocation the README documents -- `... > report.md` -- and
    # that is why an operator watching a pod fail four different ways saw four
    # grey `error:` lines in a stream that was already grey.
    coloured = console.enabled

    if args.command == "verify" and args.output is not None:
        return fail(
            "verify does not produce a merged document, so -o would name "
            "a file nothing writes to. Use `llossless merge` if you wanted one.",
            coloured=coloured,
        )

    if args.command == "verify" and args.base is not None:
        return fail(
            "verify takes no --base: it composes nothing, so there is no "
            "document whose structure a result would follow. If you meant the "
            "endpoint, that is --base-url.",
            coloured=coloured,
        )

    if len(args.sources) < merge.MIN_SOURCES:
        # Refused by the parser rather than by `check_sources`, so the arity is
        # wrong before a file is opened and the message carries the usage line.
        parser.error(
            f"a merge needs at least {merge.MIN_SOURCES} sources; "
            f"{len(args.sources)} was given"
        )

    if len(args.sources) > merge.MAX_SOURCES:
        # Here for the same reason as the floor above, and refused for the
        # reason `merge.MAX_SOURCES` states: past it the source letters reach
        # the merge's own and a segment id stops naming one document. `verify`
        # is capped too -- it takes the same sources, and `MERGED` is added to
        # `paths` beside them under a name of its own.
        parser.error(
            f"a merge takes at most {merge.MAX_SOURCES} sources; "
            f"{len(args.sources)} was given. Past {merge.MAX_SOURCES} the "
            f"source letters reach the merged document's own and a segment id "
            f"in the report stops naming which document it came from"
        )

    canonical = merge.source_names(len(args.sources))
    run = Run(command=args.command)
    paths = dict(zip(canonical, args.sources))
    if args.command == "verify":
        paths[MERGED] = args.merged
    run.paths = {name: str(path) for name, path in paths.items()}

    collision = output_collision(args, paths)
    if collision is not None:
        return fail(collision, coloured=coloured)

    try:
        base = None if args.command == "verify" else canonical_base(args.base, paths)
        settings = config.resolve(args)
        # Built once, here, and threaded to both the banner below and the
        # pipeline call further down rather than reconstructed at each site.
        # `MergePolicy.from_settings` is pure -- same `settings` in, same
        # policy out -- but a second call is still a second place for the two
        # to drift if one of them is ever edited to read `args.fidelity` or
        # `config.DEFAULT_FIDELITY` directly, and the printed level would then
        # disagree with the level the run actually used.
        policy = merge.MergePolicy.from_settings(settings)
        # The sweep that found the twenty error strings
        # searched for `settings.host` and this passes `base_url`, so it was the
        # one message left naming the pod -- and it is the first line of every
        # captured log. Unlabelled it stays the full URL: the operator typed it
        # and is entitled to know which of three configured endpoints answered.
        # Scheme, host and port; the full URL only at -vv, where the operator
        # asked for it. A URL carries more than an address -- userinfo is a
        # credential and a path or query can carry a pasted token -- and this
        # line is the first line of every captured log.
        # Lazy, matching client.py and decompose.py: a replay run must be able
        # to import everything it needs without loading the module that can
        # open a socket, and window.reported() is the one function in this
        # module that does.
        from . import window

        console.banner(args.command, settings.model_for("verify"),
                       settings.base_url if args.verbose >= 2
                       else settings.banner_endpoint,
                       window=window.banner_window(settings, settings.model_for("verify")),
                       fidelity=policy.fidelity,
                       # From the same object `pipeline` is about to be handed
                       # its `depth=` from, for the reason the fidelity is
                       # taken off the resolved policy rather than off the
                       # default: a banner that reads a default cannot be
                       # wrong about a run that overrode it, and a banner that
                       # reads the wrong field can.
                       depth=settings.verify_depth,
                       # What the model was granted, read off the command this
                       # run will really execute rather than off the level that
                       # asked for it. `None` on every run with no grant,
                       # which is every HTTP run and every command run below
                       # `sourced`, so this line is unchanged for all of them.
                       retrieval=", ".join(
                           config.granted_web_tools(settings.command)) or None)
        # The banner names one endpoint, because for almost every run there is
        # one. That is not always true, and a banner naming the
        # default host over a run whose merge goes to a vendor is a line that
        # reads as a complete account and is not one. So when the roles differ,
        # each role's model and endpoint is listed under the banner at `-vv`.
        # `console.detail` is silent below that: a quieter run sees the banner.
        if settings.split_endpoints:
            for role in sorted(config.ROLES):
                console.detail(
                    f"{role}: {settings.model_for(role)} on "
                    f"{settings.base_url_for(role) if args.verbose >= 2 else settings.endpoint_name_for(role)}")
        console.step(f"reading {len(paths)} document(s)")
        documents = {
            name: read_document(path, "source" if name in canonical else "merged document")
            for name, path in paths.items()
        }
        for name, path in paths.items():
            console.detail(f"{path} -> {name}, {len(documents[name])} characters")
        # `prepare_merge` only knows about sources -- `verify`'s merged document
        # is not one, and its own name is already canonical, so it is set aside
        # here and put back once the sources have been through the shared
        # preparation rather than run through a rename that has nothing to do
        # for it.
        merged_text = documents.pop(MERGED, None)
        documents, loaded, run.unclosed_fences = prepare_merge(
            documents, settings.verify_depth)
        if merged_text is not None:
            documents[MERGED] = merged_text
            # The one thing `prepare_merge` does not do for a document that
            # is not a source: scan it for the same fault, in the same shape,
            # so a `verify` run is told about an unclosed fence in `merged.md`
            # exactly as it always was, appended after the sources' own.
            run.unclosed_fences += tuple(
                (MERGED, line, reason)
                for line, reason in segment.segment_document(merged_text, "a").skipped
                if reason.startswith("fence opened")
            )
        for name, line, reason in run.unclosed_fences:
            console.warn(f"{name}: {reason}")
        console.step("loading prompts")
        for role, prompt in sorted(loaded.items()):
            console.detail(f"{role}: {prompt.path.name} {prompt.sha256[:12]}")
    except (ConfigError, FileNotFoundError, merge.MergeError) as exc:
        return fail(str(exc), coloured=coloured)

    if getattr(args, "sweep_fidelity", False):
        # A sweep is a run and a report per level. `--json` has a sweep-shaped
        # payload to write; the HTML report is one page about one run and has
        # no honest answer here. Refused rather than silently skipped, which is
        # what it did before: a caller who asked for a file and got none would
        # read the empty path as a clean run.
        if args.html_path is not None:
            return fail("--html writes one page about one run, and a fidelity "
                        "sweep is one run per level. Use --sweep-dir for the "
                        "per-level reports, or drop --sweep-fidelity.",
                        coloured=coloured)
        refusal = sweep.refuse_before_running(
            settings, getattr(args, "fidelity", None) is not None, args.output)
        if refusal:
            return fail(refusal, coloured=coloured)
        return run_sweep(args, settings, paths, documents, loaded, base, console)

    if getattr(args, "sweep_dir", None) is not None:
        return fail("--sweep-dir names where a sweep's levels go, and no "
                    "sweep was asked for. Add --sweep-fidelity.", coloured=coloured)

    client = Client(settings, console=console)
    started = time.monotonic()
    try:
        pipeline(client, run, documents, loaded, base, policy,
                 depth=settings.verify_depth)
    except FATAL as exc:
        # `step` already recorded this as an errored unit before re-raising
        # it, so `run.errored` carries it and `exit_code` below already
        # reads 2 from that -- the same path an ordinary errored unit takes.
        # This used to `return fail(...)` unconditionally here: one red line
        # to stderr, and nothing past this point ever ran. A fault on the
        # pipeline's last call -- a final verify, say -- discarded the report
        # of everything that had already finished along with it: a completed
        # merge, three decomposes, an earlier verify pass.
        #
        # But a fault on the *first* call has nothing completed to discard,
        # and a full report scaffold around one failed step is worse than the
        # single plain line the operator used to get -- so that shape is kept
        # for exactly that case. `any(... OK)` is the test: if some unit of
        # work already finished, the rest of this function renders what was
        # measured, attempts the outputs the caller asked for, and lets
        # `summarise` report the fault on top of that report rather than
        # instead of it. A run that could not finish is still inconclusive,
        # and the exit code says so unchanged either way.
        if not any(step.state == OK for step in run.steps):
            return fail(plain(f"{type(exc).__name__}: {exc}"), coloured=coloured)

    run.provenance = Provenance(
        settings=settings,
        client=client,
        roles=ROLES if run.command == "merge" else ROLES[1:],
        duration_seconds=time.monotonic() - started,
        base=run.base,
        base_chosen=run.base_chosen,
    )

    # `--dry-run` graded nothing, so its headline is a plan rather than a
    # verdict and takes no verdict colour. Same reasoning as the exit code four
    # lines further down, which is 0 for the same reason.
    code = 0 if run.planned else exit_code(run)

    # `-o` is attempted, and the report is printed, before either can fail the
    # other's way out of existing. It used to be `-o` first, `return fail(...)`
    # on an OSError, report never printed: a full merge that ran to completion
    # and then hit a permission error or a full disk lost the merged document
    # entirely, because the report -- which carries it too, in the `## Merged
    # document` section -- was the next line down and never ran. The model call
    # already happened; nothing here should be able to make that call cost the
    # operator the text it produced.
    write_error = None
    if run.merged is not None and args.output is not None:
        try:
            args.output.write_text(run.merged, encoding="utf-8")
        except OSError as exc:
            write_error = f"cannot write {args.output}: {exc.strerror or exc}"
        else:
            run.merged_written_to = str(args.output)
            console.done(f"merged document written to {args.output}")

    # `render` holds the Inventory against the Coverage table and raises
    # sooner than print two counts for one quantity. Nothing caught that, so
    # the one time it fired the operator would have been shown a traceback.
    # It is a run with no verdict to act on, which is what 2 means, and it is
    # said in a sentence: `report_refused`, at the foot of this module.
    try:
        rendered = render(run)
    except InventoryDisagrees as exc:
        return report_refused(exc, run, coloured=coloured)
    print(paint(rendered, enabled=report_colour,
                verdict=None if run.planned else code), end="")

    if write_error is not None:
        # 2 supersedes 1 for the same reason it does everywhere else in this
        # function: a report that ran to a verdict but could not deliver the
        # thing it verified is not a clean run, whatever the verdict says.
        return fail(write_error, coloured=coloured)

    if args.json_path is not None:
        try:
            args.json_path.write_text(
                json.dumps(as_dict(run), indent=2) + "\n", encoding="utf-8"
            )
        except OSError as exc:
            return fail(f"cannot write {args.json_path}: {exc.strerror or exc}",
                        coloured=coloured)

    if args.html_path is not None:
        try:
            args.html_path.write_text(render_html(run), encoding="utf-8")
        except InventoryDisagrees as exc:
            return report_refused(exc, run, coloured=coloured, html=args.html_path)
        except OSError as exc:
            return fail(f"cannot write {args.html_path}: {exc.strerror or exc}",
                        coloured=coloured)

    # A dry run made no call, so it graded nothing and has nothing to report a
    # verdict about. Exiting 0 says the plan was printed, not that the documents
    # are clean -- the report says which, and says it before any number.
    summarise(run, code, output=args.output, coloured=console.enabled,
              piped=not is_tty(sys.stdout))
    return code


def finished_inconclusive(run: Run) -> tuple[str, str] | None:
    """The closing sentence for a 2 on a run that finished, or None.

    A source that produced no claims on `verify`, and claims graded with no
    quote found in the file it names, exit 2 with every call answered, so
    "part of this run did not finish" is false for them. The reason is the
    report verdict's own (`report.unanswered_by_no_fault`), said once more on
    the terminal in its plain voice. None for a run with an errored or
    unusable unit, which really did not finish, and for the other 2s, which
    have their own sentence above this call.
    """
    from .report import GROUNDED, NOT_GRADED, unanswered_by_no_fault
    graded = [v for v in run.verdicts if v.grounding != NOT_GRADED]
    named = run.unexamined_sources() if run.command == "verify" else []
    nothing_grounded = bool(graded) and not any(v.grounding == GROUNDED for v in graded)
    if run.unusable or run.errored or not (named or nothing_grounded):
        return None
    said = unanswered_by_no_fault(run).replace("**", "", 2)
    gloss = said.split(" ", 1)[1]
    if named:
        gloss += f" No claims came from: {', '.join(named)}."
    return said.split(" ", 1)[0], gloss


def report_refused(exc: InventoryDisagrees, run: Run, *, coloured: bool,
                   html: Path | None = None) -> int:
    """The report counted one quantity two ways and refused to print both.

    `report.InventoryDisagrees` is the report holding the rows of its
    Inventory against its Coverage table. Both are read off the same verdicts,
    so no path through `pipeline` raises it, and when it fires the fault is in
    this tool and never in the documents. The run still has no verdict a
    reader can act on, so it is inconclusive, 2, and the last line says what
    happened and whose defect it is.

    **The merged document is not lost with the report.** When no `-o` wrote
    it, the report was going to carry it, under `## Merged document`. The
    merge call is paid for by the time anything here runs, so the text goes to
    stdout where the report would have put it, and the line says so. Where
    `-o` did write it, the line names the file: nothing else says so at the
    default verbosity. `html` is the page that was refused when the Markdown
    report had already been printed, with the merged document in it or
    beside it.

    At the foot of the module so that no line another file cites in this one
    moves.
    """
    if html is not None:
        what = f"the HTML report was not written to {html}"
    elif run.merged is not None and run.merged_written_to is None:
        print(run.merged, end="" if run.merged.endswith("\n") else "\n")
        what = ("the report was not printed, and the merged document was "
                "printed in its place")
    elif run.merged_written_to is not None:
        what = (f"the report was not printed; the merged document is in "
                f"{run.merged_written_to}")
    else:
        what = "the report was not printed"
    return fail(
        f"{what}. Its Inventory and its Coverage table counted the same "
        f"claims differently, and LLossless refuses to print two different "
        f"counts for one quantity, so this run is inconclusive. That is a "
        f"defect in LLossless and not in your documents: please report it, "
        f"with this detail. {exc}", coloured=coloured)


if __name__ == "__main__":
    sys.exit(main())
