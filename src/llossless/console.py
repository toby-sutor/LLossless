"""Where the command talks to the person running it, and how the report looks.

Three rules hold this module together, and each of them is the answer to a way
a coloured command-line tool usually goes wrong.

**stdout is the artefact; the running commentary goes to stderr.** The README
tells the operator to redirect the report, and a merge takes minutes, so a run
that prints nothing until it finishes looks indistinguishable from one that has
hung. Progress therefore belongs on the other stream: `llossless merge ... >
report.md` shows the steps on the terminal and leaves the file clean. There is
one exception and it predates this module: `cli.run_sweep` prints a line per
fidelity level on stdout, unconditionally. It is left where it is rather than
routed through here, because a sweep's stdout is already a mixed stream -- the
comparison table is printed there too -- and gating those lines behind `-v`
would take away output that runs today print without being asked.

**Colour is decided once, from the stream, and never guessed again.** `auto`
means a terminal that says it can. `NO_COLOR` wins over `TERM`, `--colour
always` wins over both, and a pipe gets nothing. The decision is a function of
the stream and the environment so that it can be tested without a terminal,
which is the only way it gets tested at all.

**Painting the report is cosmetic, and that is a testable claim rather than an
intention.** `paint` adds escape sequences and removes nothing: `strip(paint(t))
== t` for every t, and `tests/test_console.py` asserts it over the report the
CLI actually renders. That invariant is what makes it safe to colour a document
the caller may be about to pipe into something else -- the markdown is still
markdown, and `--colour never` is not a second code path producing a second
report, it is the same string without the escapes.
"""

from __future__ import annotations

import contextlib
import os
import re
import sys
import threading
import time

from .config import DEFAULT_VERIFY_DEPTH, fidelity_name

# The palette the three measurement harnesses already use
# in `tests/run_verify.py`, extended by the two the report needs. Same codes
# and the same `colour()` signature, so a reader who has seen one has seen both;
# `internal/docs/M5-harness.md` documents the harness half and that documentation stays
# true.
GREEN, RED, YELLOW, DIM, BOLD, RESET = (
    "\033[32m",
    "\033[31m",
    "\033[33m",
    "\033[2m",
    "\033[1m",
    "\033[0m",
)
CYAN = "\033[36m"
BLUE = "\033[34m"

ANSI = re.compile(r"\033\[[0-9;]*m")

COLOUR_MODES = ("auto", "always", "never")


def colour(text: str, code: str, enabled: bool) -> str:
    return f"{code}{text}{RESET}" if enabled else text


def strip(text: str) -> str:
    """Every escape this module can add, removed. The inverse of `paint`."""
    return ANSI.sub("", text)


def supports_colour(stream, mode: str = "auto", env: dict | None = None) -> bool:
    """Whether to colour `stream`. A function of the stream and the environment.

    `always` still refuses a stream that cannot be written to as a terminal
    would -- there is no such stream in practice, but the check costs nothing
    and the alternative is an AttributeError inside a report.

    NO_COLOR is honoured for any value including the empty string, which is what
    no-color.org specifies; the common mistake is to test truthiness and so
    ignore `NO_COLOR=`.
    """
    env = os.environ if env is None else env
    if mode not in COLOUR_MODES:
        raise ValueError(f"colour mode must be one of {', '.join(COLOUR_MODES)}, not {mode!r}")
    if mode == "never":
        return False
    if mode == "always":
        return True
    if "NO_COLOR" in env:
        return False
    if env.get("TERM") == "dumb":
        return False
    try:
        return bool(stream.isatty())
    except (AttributeError, ValueError):  # not a stream, or closed
        return False


def _encodable(stream, text: str) -> bool:
    """Can this stream carry these characters at all?

    The glyphs below are nicer than the ASCII, and on a machine whose stderr is
    latin-1 they are a UnicodeEncodeError in the middle of a run -- a decorative
    feature crashing a merge that had otherwise worked. So the fallback is
    chosen up front from the stream's own encoding rather than discovered.
    """
    encoding = getattr(stream, "encoding", None)
    if not encoding:
        return False
    try:
        text.encode(encoding)
    except (UnicodeEncodeError, LookupError):
        return False
    return True


# Two glyph sets, picked by what the stream can encode. Keyed by role rather
# than by shape so the fallback cannot drift into meaning something else.
GLYPHS = {
    "step": ("•", "*"),      # a unit of work starting
    "done": ("✓", "+"),      # it finished
    "fail": ("✗", "x"),      # it did not
    "skip": ("–", "-"),      # it was not attempted
    "wait": ("…", "..."),    # something slow is in progress
}


class Console:
    """The verbose channel. Silent at verbosity 0, which is the default.

    `verbosity` is the count of `-v`: 1 names each step and each model call, 2
    adds the resolved configuration and the per-call timings. Nothing here ever
    writes to stdout, and nothing here is load-bearing -- a run with the console
    switched off produces the same report, the same exit code and the same
    cassettes, which is why it can be this chatty at all.
    """

    def __init__(self, stream=None, *, verbosity: int = 0, enabled: bool = False) -> None:
        self.stream = sys.stderr if stream is None else stream
        self.verbosity = verbosity
        self.enabled = enabled
        self.glyphs = {
            name: rich if _encodable(self.stream, rich) else plain
            for name, (rich, plain) in GLYPHS.items()
        }
        # A moving spinner needs a terminal to move on. Colour is the proxy the
        # rest of this module already resolved, and the isatty is asked again
        # because `--colour always` into a file must not animate.
        self.animate = enabled and verbosity > 0 and is_tty(self.stream)
        self._started: float | None = None

    def _write(self, text: str) -> None:
        print(text, file=self.stream, flush=True)

    def step(self, message: str, *, level: int = 1) -> None:
        """A unit of work is starting."""
        if self.verbosity < level:
            return
        self._write(colour(self.glyphs["step"], BLUE, self.enabled) + " " + message)

    def done(self, message: str, *, seconds: float | None = None, level: int = 1) -> None:
        if self.verbosity < level:
            return
        tail = "" if seconds is None else colour(f"  {seconds:.1f}s", DIM, self.enabled)
        self._write(colour(self.glyphs["done"], GREEN, self.enabled) + " " + message + tail)

    def failed(self, message: str, *, level: int = 1) -> None:
        if self.verbosity < level:
            return
        self._write(colour(self.glyphs["fail"] + " " + message, RED, self.enabled))

    def skipped(self, message: str, *, level: int = 1) -> None:
        if self.verbosity < level:
            return
        self._write(colour(self.glyphs["skip"] + " " + message, DIM, self.enabled))

    def detail(self, message: str, *, level: int = 2) -> None:
        """Something a second -v asked for. Indented under the step it belongs to."""
        if self.verbosity < level:
            return
        self._write(colour(f"    {message}", DIM, self.enabled))

    def warn(self, message: str) -> None:
        """Said whatever the verbosity. This is the channel `client.notify` uses."""
        self._write(colour(f"! {message}", YELLOW, self.enabled))

    def notice(self, message: str) -> None:
        """Something slow starting, said whatever the verbosity.

        Not `step`, which is behind `-v`, and not `warn`, which says something
        went wrong. This is for the one case where the tool is about to be quiet
        for a long time through nobody's fault -- a cold endpoint loading a
        model -- and where an operator who has not asked for verbosity is
        precisely the one who will conclude it has hung.
        """
        self._write(colour(self.glyphs["wait"] + " " + message, CYAN, self.enabled))

    def banner(self, command: str, model: str, endpoint: str, window: str | None = None,
               fidelity: str | None = None, depth: str | None = None,
               retrieval: str | None = None) -> None:
        """What this run is, before it starts doing it.

        The endpoint is printed as the operator typed it, because an operator
        who has three configured is entitled to know which one answered before
        waiting two minutes to find out. The API key is not here and is not
        anywhere: `config` holds the name of the variable, never the value.

        `window` is the served context window, from `window.banner_window()` --
        `/api/ps`'s figure, or the one the operator stated, which arrives here
        marked `(stated)` rather than silently looking like the other --
        printed here for the same reason the endpoint is: a preflight refusal
        during decompose or merge is correct but late, after documents have
        been read and prompts loaded. `None` means the caller could not learn
        it -- no model loaded yet, or an endpoint with no `/api/ps` at all --
        and that is not printed as an error, because a vendor endpoint having
        no such route is not one (Brief DD item 1).

        `fidelity` is gated on `-vv`, same as the full endpoint URL a few lines
        up in `cli.main` -- it is configuration, not progress, and belongs with
        the rest of what `-v` alone does not ask for. The caller passes
        `policy.fidelity` off the same `MergePolicy` the merge and verify calls
        are given, not `config.DEFAULT_FIDELITY` and not the raw `--fidelity`
        string, so what this line prints cannot name a level the run did not
        use -- `DEFAULT_FIDELITY` changed once already (390), and a banner
        reading the default rather than the resolved policy would have been
        wrong about every run that overrode it.

        `depth` is gated differently from `fidelity`, and deliberately. At its
        default it is configuration like the level and waits for `-vv`; at any
        other value it prints at every verbosity, because the only other value
        there is suspends a guarantee. An operator who passed
        `--verify-depth coverage` an hour ago, or who set the environment
        variable last week, is about to read a clean result that means less
        than a clean result usually does, and finding that out afterwards in
        the provenance block is finding it out too late. This is the same rule
        `provenance.rows` applies to `field_order` and `profile` -- say what
        changed, stay quiet about what did not -- with the floor removed for
        the case that matters.

        **"Every verbosity" includes the default one, and did not.** The floor
        below returned before any of that ran unless `-v` had been passed, and
        `--verbose` defaults to 0 -- so the one banner field written to be
        unmissable was missing from every run nobody asked to be verbose,
        which is most of them (505). It was invisible because the test that
        covers the "ordinary verbosity" case passes `-v`: a test that sets the
        thing it is measuring cannot see the default. The floor stays for
        every other reason this line exists, so a run at the default depth
        prints nothing here without `-v`, exactly as before.

        `retrieval` is gated the way a non-default depth is, and for a stronger
        version of the same reason (548). A run whose model was granted a web
        tool may put text from these documents into a query or a fetch, and at
        the level that grants it automatically the operator never typed the
        flag -- so the one thing this line must not do is stay quiet about it.
        `None` is the ordinary case and prints nothing, exactly as before.
        """
        if (self.verbosity < 1 and retrieval is None
                and (depth is None or depth == DEFAULT_VERIFY_DEPTH)):
            return
        line = f"  {model} at {endpoint}"
        if window is not None:
            line += f", window {window}"
        if fidelity is not None and self.verbosity >= 2:
            # Published name: this is a banner, not a record (437).
            line += f", fidelity {fidelity_name(fidelity)}"
        if depth is not None and (self.verbosity >= 2
                                  or depth != DEFAULT_VERIFY_DEPTH):
            line += f", depth {depth}"
        if retrieval:
            line += f", retrieval {retrieval}"
        self._write(
            colour(f"LLossless {command}", BOLD, self.enabled)
            + colour(line, DIM, self.enabled)
        )

    @contextlib.contextmanager
    def waiting(self, message: str):
        """A slow thing, with the elapsed time moving while it is slow.

        The ticker is a daemon thread that only ever writes a carriage-return
        line to a terminal, and only when this console is animating -- so under
        a pipe, under a test harness, and at verbosity 0 no thread starts at
        all. It is cleared on the way out whether the body raised or returned,
        because a half-written progress line left on the terminal in front of a
        traceback is worse than no progress line.
        """
        started = time.monotonic()
        if not self.animate:
            yield lambda: time.monotonic() - started
            return
        stop = threading.Event()

        def tick() -> None:
            while not stop.wait(0.25):
                elapsed = time.monotonic() - started
                line = f"  {self.glyphs['wait']} {message}  {elapsed:.1f}s"
                self.stream.write("\r" + colour(line, DIM, self.enabled) + "\033[K")
                self.stream.flush()

        thread = threading.Thread(target=tick, daemon=True)
        thread.start()
        try:
            yield lambda: time.monotonic() - started
        finally:
            stop.set()
            thread.join(timeout=1.0)
            self.stream.write("\r\033[K")
            self.stream.flush()


def is_tty(stream) -> bool:
    try:
        return bool(stream.isatty())
    except (AttributeError, ValueError):
        return False


# --------------------------------------------------------------------------
# Painting the report
# --------------------------------------------------------------------------

# Markdown, not LLossless vocabulary. `report.py` grows sections and headings
# every milestone, and a painter keyed to its wording would silently stop
# colouring the section that got rewritten. Keyed to the syntax instead, it
# colours whatever the report says next.
HEADING = re.compile(r"^(#{1,6})\s")
SEPARATOR = re.compile(r"^\|[\s|:-]+\|$")
INLINE = re.compile(r"\*\*.+?\*\*|`[^`]+`")

# The three words the report prints as a judgement rather than as prose
# (`verify.CONFIRMED` and its two siblings, rendered in the declarations
# table). Whole words only, so `unchecked` in a sentence is coloured and
# `rechecked` is not.
SEMANTIC = {"confirmed": GREEN, "rejected": RED, "unchecked": YELLOW}
WORD = re.compile(r"\b(" + "|".join(SEMANTIC) + r")\b")

# What the verdict headline means, by exit code. `report.exit_code` owns the
# number; this owns nothing but the colour of it, which is why the code is
# passed in rather than inferred from the sentence.
VERDICT = {0: GREEN, 1: RED, 2: YELLOW}


def paint(text: str, *, enabled: bool, verdict: int | None = None) -> str:
    """The rendered report, with escapes added and nothing else changed.

    The invariant is `strip(paint(t, enabled=True)) == t`. Everything below
    wraps, and nothing rewrites: no markdown marker is consumed, no whitespace
    is normalised, no line is reflowed. A reader piping a coloured report
    through `sed 's/\\x1b\\[[0-9;]*m//g'` gets the file back byte for byte.

    Fenced blocks are left alone entirely. Without `-o` the merged document is
    embedded in the report, and it is the caller's text: colouring inside it
    would be this tool decorating the very document it is supposed to be
    reproducing faithfully.
    """
    if not enabled:
        return text
    out: list[str] = []
    fenced = False
    in_verdict = False
    headline_left = verdict is not None
    for line in text.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
            out.append(colour(line, DIM, True))
            continue
        if fenced:
            out.append(line)
            continue
        heading = HEADING.match(line)
        if heading:
            in_verdict = line.startswith("## Verdict")
            code = BOLD + CYAN if len(heading.group(1)) <= 2 else BOLD
            out.append(colour(line, code, True))
            continue
        if in_verdict and headline_left and line.strip():
            # The one line in the report whose colour is a fact about the run
            # rather than about the syntax. Taken once: the verdict section can
            # run to several sentences and a paragraph of red is unreadable.
            headline_left = False
            out.append(colour(line, VERDICT.get(verdict, ""), True))
            continue
        out.append(_paint_line(line))
    return "\n".join(out)


def _paint_line(line: str) -> str:
    if SEPARATOR.match(line):
        return colour(line, DIM, True)
    if line.startswith("|"):
        # Cell by cell, so the dim pipes and a bold cell cannot fight over who
        # resets whom. Splitting on the pipe and rejoining with a coloured one
        # keeps every character that was there.
        return colour("|", DIM, True).join(_inline(cell) for cell in line.split("|"))
    return _inline(line)


def _inline(text: str) -> str:
    """Bold spans and code spans, in one pass so neither can nest in the other."""
    def wrap(match: re.Match) -> str:
        span = match.group(0)
        return colour(span, BOLD if span.startswith("*") else CYAN, True)

    painted = INLINE.sub(wrap, text)
    return WORD.sub(lambda m: colour(m.group(0), SEMANTIC[m.group(0)], True), painted)
