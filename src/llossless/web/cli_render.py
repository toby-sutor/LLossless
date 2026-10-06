"""The CLI-equivalent block: how a submitted run reads as an `llossless` command.

The operator's request: when the web UI runs a merge with a browser's worth of
settings, show the exact `llossless merge ...` line that would have done the
same run from a terminal, so the page teaches its own automation path.

**Rendered from `config.Settings`, never from the page's controls.** The
argument for that is the same one `web/jobs.py` makes about `endpoint_plan`:
the object handed to `cli.pipeline` is the one true account of what a run
asked for, and a second computation from the request or from what a form
happened to submit is a second answer that can drift from the first one. So
every function here takes the resolved `Settings` -- and, where the two
disagree, `Run` after it exists, for the one field `Settings` does not carry:
which document a defaulted base turned out to be.

**Never `settings.command`.** `web/commands.py`'s whole architecture is that a
browser may switch a command route on and may never be told what program it
runs -- "the browser may switch a route on. It may never describe one." A
command backend's real argv would leak exactly that, to the one audience the
rule exists to keep it from: whoever is looking at their own run. So a command
route renders `--answer-with` against a placeholder, `PLACEHOLDER_COMMAND`,
and says why in `notes` -- everything else about the route (its label, its
recorded model, its window, its effort levels) is already something
`Route.described` puts in front of a browser before the run starts, and is
rendered here exactly as plainly. Ruling 17 has the `command_route` note carry
`COMMAND_EXAMPLE`, a plain, well known invocation a reader may put in the
placeholder's place -- still never this server's own configured program.

**Never a key value, and never its last four characters.** The address is
real; the variable that holds the key is named for real, because naming a
variable is not naming a secret; the key itself is always `PLACEHOLDER_KEY`.
`tests/test_web_cli_render.py` asserts this by scanning the rendered payload
for every credential this process holds, not by trusting this docstring.
"""

from __future__ import annotations

import re
import shlex
from typing import TYPE_CHECKING

from .. import cli, config, merge as merge_module
from ..structured import DEFAULT_PROFILE as HTTP_DEFAULT_PROFILE
from . import accounts, credentials

if TYPE_CHECKING:  # pragma: no cover - types only; avoids a jobs <-> here cycle
    from ..report import Run
    from .jobs import MergeRequest

# What stands in for a secret the page must never carry. Angle brackets match
# the one other placeholder this project already shows an operator
# (`config.py`'s own `<your key>` convention in credentials error text), so a
# reader meets one visual language for "type your own value here" rather than
# two.
PLACEHOLDER_KEY = "<your key>"
# A command route's argv is never shown (see the module docstring); this
# stands in for it on the one flag that would otherwise carry it.
PLACEHOLDER_COMMAND = "<your subscription command>"
# Ruling 17, 2026-09-28: the operator asked to keep the placeholder and add a
# note showing this plain form as an example of what a reader may put in its
# place -- a well known invocation, never this server's own configured
# program, which the note still says is never shown.
COMMAND_EXAMPLE = "claude -p --output-format json"

_NAME_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")
_NAME_MAX = 100


def _file_safe_name(label: str) -> str:
    """One tab label as a filename: recognisable, unique-able, never a path.

    The same shape `web/api.py`'s `_zip_name` already uses for a zip member --
    dashes for anything not alphanumeric, a fallback name for a label that
    reduces to nothing, and `.md` added only where the label carried no
    extension of its own -- so a name typed into a form and a name read back
    off a filesystem are sanitised by one rule between the two places this
    project turns a label into a filename.
    """
    cleaned = _NAME_UNSAFE.sub("-", str(label)).strip("-.")
    cleaned = cleaned[:_NAME_MAX] or "document"
    return cleaned if "." in cleaned else f"{cleaned}.md"


def _unique_filenames(labels: list[str]) -> list[str]:
    """`_file_safe_name` per label, de-duplicated in order.

    Two tabs can carry the same label -- "Draft", typed twice -- and sanitising
    each alone would then tell the operator to save two different documents
    under one name, silently overwriting the first with the second the moment
    they follow the instruction. A repeat gets `-2`, `-3`, ... before its
    extension instead.
    """
    taken: set[str] = set()
    names: list[str] = []
    for label in labels:
        base = _file_safe_name(label)
        stem, dot, ext = base.rpartition(".")
        if not dot:
            stem, ext = base, ""
        name = base
        counter = 2
        while name in taken:
            name = f"{stem}-{counter}" + (f".{ext}" if ext else "")
            counter += 1
        taken.add(name)
        names.append(name)
    return names


def _num(value) -> str:
    """A float or int as the CLI would be typed it: no trailing junk."""
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value)


def _env_line(name: str, value) -> str:
    """One `export NAME=value` line, shell-quoted.

    Quoted even where the raw value has no metacharacter today, because
    `PLACEHOLDER_KEY` and `PLACEHOLDER_COMMAND` both open with `<` -- a
    redirection operator to a POSIX shell wherever it is unquoted, mid-word or
    not. `export FOO=<your key>` is a shell trying to read a file named
    `your`; `export FOO='<your key>'` is the sentence it looks like.
    """
    return f"export {name}={shlex.quote(str(value))}"


def _endpoint(settings: config.Settings, shown=None
              ) -> tuple[list[str], list[str], list[dict]]:
    """The HTTP transport: address and key, flag where one suffices, env where not.

    A single shared endpoint (the ordinary case) gets `--base-url` -- a real
    flag, and the simpler thing to read -- skipped entirely when it is already
    the CLI's own default. A run split across providers (a frontier merge
    beside a local check) has no flag for that, only `LLOSSLESS_BASE_URL_<ROLE>`,
    so it gets three env lines instead of one.

    The key is never a value. `api_key_env_for` names the *variable* a role's
    key comes from, which is public -- it is served to a browser today, in the
    credentials sheet -- and the indirection (`LLOSSLESS_API_KEY_ENV[_<ROLE>]`)
    is written only where the variable is not this build's own default, so an
    operator who changed nothing sees one `export LLOSSLESS_API_KEY=<your key>`
    rather than a line explaining a default that was never overridden.

    `shown` is the set of addresses the reader stored themselves, or `None`
    for no restriction. A member's run on the operator's endpoint is
    rendered with that endpoint as scheme, host and port
    (`accounts.reduced`), and a note says so: the path of an operator's
    address can carry a token or name a private service, and this block
    reaches the member's page and the report they download.

    A role that sent no key reads `credentials.NO_KEY_ENV`. The variable is
    named, because pointing a role at a variable nothing sets is how the
    command line says "no key here" too, and it is given no value.
    """
    argv: list[str] = []
    env: list[str] = []
    notes: list[dict] = []
    own = None if shown is None else {config.with_api_path(a) for a in shown}

    def address(role: str) -> str:
        full = settings.base_url_for(role)
        if own is None or full in own or full == config.DEFAULT_BASE_URL:
            return full
        if not any(note["key"] == "address_reduced" for note in notes):
            notes.append({"key": "address_reduced"})
        return accounts.reduced(full)

    addr_by_role = {role: address(role) for role in cli.ROLES}
    key_by_role = {role: settings.api_key_env_for(role) for role in cli.ROLES}
    if credentials.NO_KEY_ENV in key_by_role.values():
        notes.append({"key": "key_withheld",
                      "variable": credentials.NO_KEY_ENV})

    if len(set(addr_by_role.values())) == 1:
        addr = next(iter(addr_by_role.values()))
        if addr != config.DEFAULT_BASE_URL:
            argv += ["--base-url", addr]
    else:
        for role in cli.ROLES:
            env.append(_env_line(f"LLOSSLESS_BASE_URL_{role.upper()}", addr_by_role[role]))

    if len(set(key_by_role.values())) == 1:
        name = next(iter(key_by_role.values()))
        if name != config.DEFAULT_KEY_ENV:
            env.append(_env_line("LLOSSLESS_API_KEY_ENV", name))
        if name != credentials.NO_KEY_ENV:
            env.append(_env_line(name, PLACEHOLDER_KEY))
    else:
        for role in cli.ROLES:
            env.append(_env_line(f"LLOSSLESS_API_KEY_ENV_{role.upper()}", key_by_role[role]))
        # One export per distinct variable, not one per role -- two roles
        # sharing a provider share a variable, and a page that exported it
        # twice would not be wrong, only a worse read of a real run.
        for name in dict.fromkeys(key_by_role.values()):
            if name != credentials.NO_KEY_ENV:
                env.append(_env_line(name, PLACEHOLDER_KEY))
    return argv, env, notes


def _window(settings: config.Settings) -> tuple[list[str], list[str]]:
    """`--window`, when every role states the same figure; `LLOSSLESS_WINDOW_<ROLE>`
    when they do not. Applies unchanged to a command route, whose one program
    always states one figure for every role (`config.Settings.__post_init__`
    refuses a command backend that leaves any role's window unstated), so it
    always takes the uniform branch without asking here which backend this is.
    """
    argv: list[str] = []
    env: list[str] = []
    by_role = {role: settings.window_for(role) for role in cli.ROLES}
    if len(set(by_role.values())) == 1:
        value = next(iter(by_role.values()))
        if value is not None:
            argv += ["--window", str(value)]
    else:
        for role in cli.ROLES:
            value = by_role[role]
            if value is not None:
                env.append(_env_line(f"LLOSSLESS_WINDOW_{role.upper()}", str(value)))
    return argv, env


def _base_document(request: "MergeRequest", run: "Run | None",
                   labels: list[str], label_to_filename: dict[str, str]) -> tuple[str | None, list[dict]]:
    """Which filename `--base` names, and a note when this run did not choose one.

    `run.base` -- once there is a `run` -- is the canonical name the merge
    actually followed, `merge.merge_documents`'s own default (`names[0]`, the
    first source) when nobody chose one; `run.paths` maps it back to the
    caller's label. Before a `run` exists (the block shown while a job is
    still going), `request.base` is the best answer available, and an unset
    one falls to the same first-document default `merge.py` would apply --
    correct as often as not, and never wrong about which document is which,
    only about whether the choice was explicit.

    `--base` is required on the command line (`cli.py`'s own reason: "with
    three paths on a command line 'the first one you typed' would be a choice
    you made without knowing you were making it"), so a run that let the merge
    default it still needs an explicit flag here to be a runnable command --
    the note says so rather than leaving a reader to wonder why a setting
    nobody chose is spelled out.
    """
    notes: list[dict] = []
    base_label = None
    defaulted = False
    if run is not None and getattr(run, "base", None):
        paths = getattr(run, "paths", None) or {}
        base_label = paths.get(run.base)
        defaulted = getattr(run, "base_chosen", None) == merge_module.DEFAULTED
    elif request.base is not None:
        base_label = request.base
    else:
        defaulted = True

    filename = label_to_filename.get(base_label) if base_label is not None else None
    if filename is None and labels:
        filename = label_to_filename[labels[0]]
        defaulted = True

    if defaulted and filename is not None:
        notes.append({"key": "base_defaulted"})
    return filename, notes


def render(settings: config.Settings, request: "MergeRequest",
           run: "Run | None" = None, *, shown=None) -> dict:
    """The CLI-equivalent payload: `{command, env, documents, shell, notes}`.

    Called twice over one run's life with the same two rules either time --
    once from `web/jobs.py` right after `web_settings` resolves, while the job
    is still `running` and there is no `run` yet; again from `publish`, with
    the finished `run`, so the base document (and only that field) sharpens
    from "the job's best guess" to "what the merge actually followed".

    `notes` is a list of `{"key": ..., **params}`, not prose: this page is
    shown in English and German, and the things a note can say are a
    closed, known set (`locales/{en,de}.json`'s `cli.note.*` keys), so the
    sentence itself belongs on the page, not baked into a string this module
    would otherwise have to compose twice.

    `shown` is `_endpoint`'s: the addresses the reader may see in full.
    """
    labels = list(request.documents)
    filenames = _unique_filenames(labels)
    documents = [{"label": label, "filename": name}
                 for label, name in zip(labels, filenames)]
    label_to_filename = dict(zip(labels, filenames))

    notes: list[dict] = []
    base_filename, base_notes = _base_document(request, run, labels, label_to_filename)
    notes += base_notes

    argv: list[str] = ["merge", *filenames]
    if base_filename is not None:
        argv += ["--base", base_filename]

    env: list[str] = []

    if settings.command:
        answer_with = PLACEHOLDER_COMMAND
        notes.append({"key": "command_route", "label": settings.command_label or "",
                      "example": COMMAND_EXAMPLE})
        if settings.command_envelope != config.ENVELOPE_RAW:
            # `envelope_refusal` cross-checks the envelope against the argv it
            # describes -- a command that does not carry `--output-format
            # json` may not claim `LLOSSLESS_COMMAND_ENVELOPE=result` -- so the
            # placeholder carries the same flag a real program would need, or
            # the rendered pair would refuse itself on the very first line.
            answer_with = " ".join([answer_with, *config.RESULT_ARGS])
            env.append(_env_line("LLOSSLESS_COMMAND_ENVELOPE", settings.command_envelope))
            notes.append({"key": "command_envelope", "envelope": settings.command_envelope})
        argv += ["--answer-with", answer_with]
    else:
        endpoint_argv, endpoint_env, endpoint_notes = _endpoint(settings, shown)
        argv += endpoint_argv
        env += endpoint_env
        notes += endpoint_notes

    merge_model = settings.model_for("merge")
    check_model = settings.model_for("verify")
    if merge_model == check_model:
        argv += ["--model", check_model]
    else:
        argv += ["--model", check_model, "--merge-model", merge_model]

    window_argv, window_env = _window(settings)
    argv += window_argv
    env += window_env

    # The merge-policy dials, always spelled out: this is the block whose
    # whole point is showing "all their exact settings", and a reader who
    # cannot tell a run that used the default loss budget from one that never
    # said is the ambiguity this exists to remove.
    argv += ["--fidelity", config.fidelity_name(settings.fidelity)]
    argv += ["--verify-depth", settings.verify_depth]
    argv += ["--title-policy", settings.title_policy]
    argv += ["--loss-budget", _num(settings.declared_loss_budget)]

    if settings.field_order != config.DEFAULT_FIELD_ORDER:
        argv += ["--field-order", settings.field_order]
    if settings.pinned:
        argv += ["--structured", settings.structured]
    if settings.profile != HTTP_DEFAULT_PROFILE:
        argv += ["--profile", settings.profile]
    for role in cli.ROLES:
        if settings.thinks(role):
            argv += ["--thinking", role]

    # Effort is the level a role was *asked* for, read off `settings.effort`
    # directly rather than off `effort_for` -- the resolved answer also
    # depends on the hidden command's own program, which this run's renderer
    # cannot see and must not guess at (`config.effort_of`'s rule 1: an
    # operator's own argv is never written over). The flag reproduces the ask;
    # whether a reader's own `--answer-with` program honours it is theirs to
    # know, and the note says so once, rather than promising a level the
    # placeholder plainly cannot deliver.
    #
    # Except a role whose model is single-level: `settings.effort`
    # should never carry one here -- the page hides the control and the API
    # refuses a submitted level (`jobs.route_plan`) -- but this is the one
    # placeholder-building path that has to hold even if it somehow did, since
    # rendering `--effort` for Haiku is exactly what the ruling asks this tool
    # to stop doing everywhere else.
    role_efforts = [(role, settings.effort.get(role)) for role in cli.ROLES]
    role_efforts = [(role, level) for role, level in role_efforts if level
                    and not config.is_single_level_model(settings.model_for(role))]
    for role, level in role_efforts:
        argv += ["--effort", f"{role}={level}"]
    if role_efforts and settings.command:
        notes.append({"key": "effort_limited"})

    if settings.min_interval:
        argv += ["--min-interval", _num(settings.min_interval)]
    if settings.timeout is not None:
        argv += ["--timeout", _num(settings.timeout)]

    if not settings.stream:
        env.append(_env_line("LLOSSLESS_STREAM", "false"))
    if settings.max_tokens is not None:
        env.append(_env_line("LLOSSLESS_MAX_TOKENS", str(settings.max_tokens)))
    if settings.ca_bundle:
        notes.append({"key": "ca_bundle"})

    argv += ["-o", "merged.md"]

    command = "llossless " + " ".join(shlex.quote(part) for part in argv)
    return {
        "command": command,
        "env": env,
        "documents": documents,
        "shell": "posix",
        "notes": notes,
    }
