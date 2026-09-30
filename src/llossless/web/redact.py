"""Nothing this host knows about its own filesystem reaches whoever submitted a job.

One thing was left open for the HTTP layer. `Usage.prompts` is keyed
by the full prompt path (`client.py:604`), so `report.as_dict` carries an
absolute filesystem path for every prompt a run loaded. That is harmless in the
artefacts this repository publishes, because `scripts/stream_redact.py` rewrites
them on the way out -- but a server hands the report straight to whoever posted
the documents, and an absolute path discloses the host's directory layout and,
on the ordinary self-hosted install, the operator's username. So every payload
that carries a report goes through this module first: the JSON, the HTML, and
the body of any error raised on the way to producing either.

**Why this is not an import of `scripts/stream_redact.py`.** That was the first
thing tried and it does not work, for two reasons that are both structural
rather than stylistic. `scripts/` is not inside the wheel -- `pyproject.toml`
packages `src/llossless` and force-includes `prompts`, nothing else -- so an
installed server would import a module that is not there. And
`stream_redact.patterns()` reaches into `tests/test_client.py` at call time for
its detectors, which is right for a runner standing in a checkout and wrong for
a server that has no test tree beside it. A module the shipped tool depends on
cannot be one that lives outside what ships.

**Why the rule here is not the same rule either, and why that is the point.**
`stream_redact.HOME_PATH` matches one shape -- a named directory under the
conventional Linux home mount -- and nothing else. That covers
the machine this project is developed on and misses every other shape a server
actually runs under -- a systemd unit under `/srv`, a container under `/opt`, a
`root` install, a mac. Worse, the literal cannot be written here at all:
the release scan checks the published set for exactly that shape
and exempts one file by name and digest, so a second copy of the pattern in
`src/` is itself a scan failure, and disguising a literal to get past a
scanner has already been ruled out.

So the rule is the *other* half of `stream_redact`, the half that generalises:
`literal_forms()` there collects real values out of the environment and replaces
them literally, longest first, with a minimum length so a short string cannot
turn prose into marks. `roots()` below collects real directories out of this
process and replaces them the same way. It needs no literal, it covers every
prefix a deployment can have rather than one, and it is checked against the
other implementation rather than assumed to agree with it --
`tests/test_web_server.py` asserts that a path this module clears is a path
`stream_redact.scrub` also clears, which is the only form of "one rule" two
files on opposite sides of a packaging boundary can actually have.

**What is deliberately not scrubbed.** The merged document. It is the
operator's own text and the product of the run, and a substring of it that
happened to collide with a root would come back corrupted -- a merge tool that
silently edits its own output is a worse failure than a disclosed directory
name. `merged.md` is served as written; the report that quotes it is not,
because the report is where the paths actually are.
"""

from __future__ import annotations

import copy
from pathlib import Path

from .. import prompts

# What replaces a root. One mark for every root rather than a mark per root
# (`<home>`, `<prompts>`, `<work>`): a per-root mark is a second, smaller
# disclosure -- it tells a reader which of the server's directories the path
# was under, which is most of what knowing the path would have told them.
# `stream_redact.MARK` is the same string for the same reason.
MARK = "<redacted>"

# Below this length a "root" is not a root, it is a fragment that would turn
# ordinary text into marks. `/` and `/tmp` are the two that matter: the first
# would replace every separator in the document, and the second is short enough
# to appear inside words. `stream_redact.literal_forms` draws the line at the
# same place and for the same reason.
MIN_ROOT = 4

# The prompt paths, rewritten to the name the report's own markdown renderer
# already prints. `provenance._relative` (`provenance.py:1509`) shows
# `prompts/merge.md` when the run stood in a checkout and the absolute path
# otherwise; this gives the readable form in both cases, because what a reader
# needs from that row is which prompt file, not where this server keeps it.
PROMPTS_LABEL = "prompts"


def roots(extra=()) -> list[str]:
    """Every directory prefix this process knows the absolute location of.

    Four come from the installation and are the same for every request: where
    the prompts are, where the package is, the checkout above it when there is
    one, and the home directory. `extra` is what the *server* knows and this
    module cannot -- its work directory and its cache directory, which are
    chosen at startup and are exactly the paths a failed job's exception
    message is most likely to quote.

    Longest first, so that a nested root wins over the one that contains it. It
    is not a detail: the prompts directory is normally under the home
    directory, and replacing the home directory first would leave
    `<redacted>/Documents/Dev/.../prompts/merge.md` -- a string that has been
    through a redactor and still describes the operator's filesystem in full.

    Anything shorter than `MIN_ROOT`, anything relative, and anything that is
    not a directory this process can name is dropped rather than raising.
    `Path.home()` raises `RuntimeError` on a process with no home at all, which
    is an ordinary state for a container and not a reason to refuse to serve a
    report.
    """
    found: set[str] = set()
    candidates: list[Path | str] = [prompts.PROMPTS_DIR,
                                    Path(__file__).resolve().parents[1]]
    # The checkout root, when this is a checkout. `parents[3]` of this file is
    # the directory above `src/`, which is the repository root in a clone and
    # is site-packages' parent in a wheel -- so it is taken only when it looks
    # like the former. In a wheel the package root above already covers
    # everything the report can name.
    checkout = Path(__file__).resolve().parents[3]
    if (checkout / "pyproject.toml").is_file():
        candidates.append(checkout)
    try:
        candidates.append(Path.home())
    except RuntimeError:  # pragma: no cover - a process with no home
        pass
    candidates.extend(extra)
    for candidate in candidates:
        if candidate is None:
            continue
        text = str(candidate)
        if len(text) < MIN_ROOT or not Path(text).is_absolute():
            continue
        found.add(text.rstrip("/") or text)
    return sorted(found, key=len, reverse=True)


def scrub(text: str, known: list[str] | None = None) -> str:
    """Replace every known root in `text` with `MARK`. Idempotent.

    Literal replacement, not a regex over path-shaped substrings. A pattern
    that matched "anything that looks like an absolute path" would also match
    the operator's own content -- `tests/test_cli.py`'s fixture documents say
    "The audit log is written to /var/log/relay", and a report that quoted that
    back as `<redacted>` would have destroyed a claim in order to protect a
    directory nobody owns. Only the directories this process actually stands in
    are secret, and only those are replaced.
    """
    for root in (roots() if known is None else known):
        text = text.replace(root, MARK)
    return text


def prompt_label(raw: str) -> str | None:
    """`prompts/merge.md` for a path under the prompt directory, else None.

    None rather than a best effort, so the caller can tell "this is a prompt
    and here is its name" from "this is some other string" and fall back to
    `scrub` for the second. A fragment keeps its subdirectory --
    `prompts/fidelity/high.merge.md` -- because which level was rendered is
    part of what the provenance row is for.
    """
    try:
        relative = Path(raw).relative_to(prompts.PROMPTS_DIR)
    except (ValueError, TypeError, OSError):
        return None
    return (Path(PROMPTS_LABEL) / relative).as_posix()


def walk(value, known: list[str]):
    """`scrub` every string in a nested structure, keys included.

    Keys as well as values, and that is the whole reason this recurses rather
    than scrubbing `json.dumps` output: `provenance.prompts` is a mapping whose
    *keys* are the paths (`provenance.py:726`), so a pass that only touched
    values would leave every one of them in place.
    """
    if isinstance(value, dict):
        return {scrub(key, known) if isinstance(key, str) else key: walk(item, known)
                for key, item in value.items()}
    if isinstance(value, list):
        return [walk(item, known) for item in value]
    if isinstance(value, tuple):
        return tuple(walk(item, known) for item in value)
    if isinstance(value, str):
        return scrub(value, known)
    return value


def report(payload: dict, *, extra=()) -> dict:
    """A report safe to hand to whoever submitted the job. Never mutates `payload`.

    Two passes, and the order matters. The prompt paths are rewritten first, by
    name, so the served report carries `prompts/merge.md` rather than a mark --
    a provenance table whose four prompt rows all read `<redacted>` has
    protected the same thing and told the reader nothing, and the prompt digest
    beside it is only checkable against a file somebody can name. Everything
    that survives that is then swept literally, which is the backstop for the
    carriers nobody enumerated: a failed step's `detail` is
    `f"{type(exc).__name__}: {exc}"` (`cli.py:679`) and an exception raised
    anywhere in the engine can quote a path this module never thought about.

    Copied rather than edited in place because `Job.report` is the same dict on
    every poll, held for the life of the job and compared against the CLI's own
    report by `tests/test_web_server.py`. Redacting it in place would make the
    first request permanently change what every later one, and that comparison,
    sees.
    """
    known = roots(extra)
    served = copy.deepcopy(payload)
    provenance = served.get("provenance")
    if isinstance(provenance, dict) and isinstance(provenance.get("prompts"), dict):
        provenance["prompts"] = {
            (prompt_label(path) or scrub(path, known)): digest
            for path, digest in provenance["prompts"].items()
        }
    return walk(served, known)


def text(body: str, *, extra=()) -> str:
    """The same treatment for a rendered artefact: the HTML report, an error body.

    `html_report.render` writes the provenance table out of the same data
    `report()` above cleans, so the page carries the same paths -- in a
    checkout `provenance._relative` has already shortened them, and on an
    installed server it has not, which is precisely the deployment a
    checkout-only defence would miss.
    """
    return scrub(body, roots(extra))
