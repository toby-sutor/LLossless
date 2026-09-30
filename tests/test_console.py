#!/usr/bin/env python3
"""Offline checks for the terminal layer. No network, no model, no terminal.

Two properties carry this module, and both exist because a decorative feature
is exactly the kind that gets shipped untested and then breaks something real.

**Colour must be a function of the stream and the environment**, so that it can
be decided without a terminal and therefore checked without one. Every case
below hands `supports_colour` an object with an `isatty` and a dict, which is
the whole input.

**Painting must be reversible.** `strip(paint(t)) == t` for the report the CLI
actually renders, not for a sample written here -- a painter that swallowed a
markdown marker would produce a report that is no longer the report, and the
published figures were measured against the report. The same invariant is what
makes `--colour never` and a redirected stdout the same bytes as before any of
this existed, which is the regression bar the whole change was held to.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless import config, console, reconcile, report  # noqa: E402
from llossless.verify import MERGED_TO_SOURCES, SOURCE_TO_MERGED, Verdict  # noqa: E402

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


class Stream(io.StringIO):
    """A stream that can lie about being a terminal, and about its encoding.

    `encoding` is a property because `io.StringIO` refuses the attribute: a
    StringIO holds text and has no encoding to report, which is itself worth
    knowing -- it is why `_encodable` treats a missing encoding as "cannot" and
    falls back rather than assuming UTF-8.
    """

    def __init__(self, tty: bool = False, encoding: str = "utf-8") -> None:
        super().__init__()
        self._tty = tty
        self._encoding = encoding

    @property
    def encoding(self) -> str:
        return self._encoding

    def isatty(self) -> bool:
        return self._tty


# --------------------------------------------------------------------------
# Deciding whether to colour
# --------------------------------------------------------------------------


def test_colour_is_off_unless_a_terminal_asks_for_it() -> None:
    """The default has to be off, because the default destination is a pipe."""
    check(console.supports_colour(Stream(tty=True), "auto", {}),
          "a terminal on auto must be coloured")
    check(not console.supports_colour(Stream(tty=False), "auto", {}),
          "a pipe on auto must not be coloured")
    check(not console.supports_colour(None, "auto", {}),
          "something that is not a stream at all must not be coloured")


def test_no_color_wins_over_the_terminal_and_the_empty_value_counts() -> None:
    """no-color.org says any value, including none. Truthiness is the usual bug."""
    for value in ("1", "", "0", "false"):
        check(not console.supports_colour(Stream(tty=True), "auto", {"NO_COLOR": value}),
              f"NO_COLOR={value!r} must turn colour off")
    check(not console.supports_colour(Stream(tty=True), "auto", {"TERM": "dumb"}),
          "TERM=dumb must turn colour off")


def test_the_flag_beats_the_environment_in_both_directions() -> None:
    """`always` is for a pager; `never` is the escape hatch and must be absolute."""
    check(console.supports_colour(Stream(tty=False), "always", {"NO_COLOR": "1"}),
          "--colour always must colour a pipe even under NO_COLOR")
    check(not console.supports_colour(Stream(tty=True), "never", {}),
          "--colour never must not colour a terminal")
    try:
        console.supports_colour(Stream(tty=True), "sometimes", {})
    except ValueError:
        pass
    else:
        check(False, "an unknown colour mode must be refused, not guessed")


# --------------------------------------------------------------------------
# Painting the report
# --------------------------------------------------------------------------


def a_real_report() -> str:
    """A rendered report with every section the painter can meet in one string."""
    run = report.Run(command="merge")
    run.paths = {"source_a.md": "a.md", "source_b.md": "b.md", "merged.md": "m.md"}
    run.merged = "# Title\n\nThe relay listens on port 8443.\n\n```\ncode ** and ` here\n```\n"
    run.segments = 12
    run.steps.append(report.Step("merge", report.OK))
    run.steps.append(report.Step("verify (reverse)", report.ERRORED, "SchemaFailure: nope"))
    run.forward = [
        Verdict("A-001", "MISSING", "", "", "the merge does not state it",
                SOURCE_TO_MERGED, "not_graded"),
        Verdict("A-002", "CONTRADICTED", "60 seconds", "merged.md",
                "source_a.md says 30", SOURCE_TO_MERGED, "grounded"),
    ]
    run.reverse = [
        Verdict("M-001", "SUPPORTED", "port 8443", "source_a.md", "present",
                MERGED_TO_SOURCES, "grounded"),
    ]
    return report.render(run)


def test_no_rendered_report_contains_a_mask_byte() -> None:
    """`\x00` is `segment._mask`'s internal marker and must never be printed.

    Blanket, over a report carrying every section plus a real reconciler
    finding on a document shaped like the one that leaked: a link with a code
    span inside it, dropped by the merge. The leak was fixed at the source:
    `find_spans` reads its tokens back out of the unmasked text, and this is
    the assertion that would have caught it in the report, which is where
    a reader would have met it.
    """
    link = "[the `relay` guide](https://example.test/docs/relay.md)"
    sources = {
        "source_a.md": f"# Relay Notes\n\nSee {link} for detail.\n",
        "source_b.md": "# Relay Notes\n\nThe relay listens on port 8443.\n",
    }
    merged = "# Relay Notes\n\nThe relay listens on port 8443.\n"
    result = reconcile.reconcile(sources, merged)
    run = report.Run(command="merge")
    run.paths = {"source_a.md": "a.md", "source_b.md": "b.md", "merged.md": "m.md"}
    run.merged = merged
    run.segments = sum(len(coverage.document.segments) for coverage in result.coverages)
    run.steps.append(report.Step("merge", report.OK))
    run.reconciled = reconcile.findings(
        result, (), fidelity="off", title_policy="keep-base", base="source_a.md",
        budget=config.DEFAULT_DECLARED_LOSS_BUDGET,
    )
    run.order = result.order
    text = report.render(run)
    check(link in text, f"the sample report must actually name the link: {text[:0]!r}")
    check("\x00" not in text, "a rendered report printed a mask byte")
    check("\x00" not in a_real_report(), "the sample report printed a mask byte")


def test_painting_adds_escapes_and_changes_nothing_else() -> None:
    """The invariant the whole feature rests on, over the real renderer."""
    text = a_real_report()
    for wanted in ("## Verdict", "|---|---|", "### ", "```", "**", "`"):
        check(wanted in text,
              f"the sample report must exercise {wanted!r} for this to mean anything")
    for verdict in (0, 1, 2, None):
        painted = console.paint(text, enabled=True, verdict=verdict)
        check(painted != text, f"verdict {verdict} must actually colour something")
        check(console.strip(painted) == text,
              f"painting at verdict {verdict} must be reversible, and was not")


def test_colour_off_returns_the_same_bytes() -> None:
    """`--colour never`, a pipe and a redirect are the same string as before."""
    text = a_real_report()
    check(console.paint(text, enabled=False, verdict=1) == text,
          "an unpainted report must be byte-identical to the rendered one")
    check(console.strip(text) == text, "the rendered report must carry no escapes of its own")


def test_a_fenced_block_is_left_alone() -> None:
    """Without -o the caller's own merged document is in the report."""
    body = "## Merged document\n\n```\nkeep ** this ` exactly\n```\n"
    painted = console.paint(body, enabled=True)
    check("keep ** this ` exactly" in painted.split("\n")[3],
          "the inside of a fenced block must carry no escapes")


def test_the_verdict_headline_takes_the_colour_of_the_exit_code() -> None:
    """Green, red and yellow are the three outcomes, and only the headline gets one."""
    text = "## Verdict\n\n**Something.** And a second sentence.\n\nAnd a later paragraph.\n"
    for code, want in ((0, console.GREEN), (1, console.RED), (2, console.YELLOW)):
        painted = console.paint(text, enabled=True, verdict=code)
        headline = painted.split("\n")[2]
        check(headline.startswith(want),
              f"exit {code} must colour the verdict headline {want!r}")
    later = console.paint(text, enabled=True, verdict=1).split("\n")[4]
    check(console.RED not in later, "only the headline takes the verdict colour")


# --------------------------------------------------------------------------
# The console itself
# --------------------------------------------------------------------------


def test_the_console_is_silent_until_asked() -> None:
    """Verbosity 0 is the default and prints nothing but the two unconditional kinds."""
    stream = Stream()
    quiet = console.Console(stream, verbosity=0, enabled=False)
    quiet.step("reading")
    quiet.done("reading")
    quiet.detail("a detail")
    quiet.skipped("skipped")
    quiet.failed("failed")
    quiet.banner("merge", "m", "http://e/v1")
    check(stream.getvalue() == "", f"a quiet console must print nothing, got {stream.getvalue()!r}")

    quiet.warn("something moved")
    quiet.notice("loading a model")
    value = stream.getvalue()
    check("something moved" in value and "loading a model" in value,
          "a warning and a load notice must print whatever the verbosity")


def test_the_levels_are_a_ladder() -> None:
    """-v is steps, -vv adds the detail. Neither is the other."""
    one, two = Stream(), Stream()
    console.Console(one, verbosity=1, enabled=False).step("merge")
    console.Console(one, verbosity=1, enabled=False).detail("cache hit")
    console.Console(two, verbosity=2, enabled=False).detail("cache hit")
    check("merge" in one.getvalue(), "-v must name each step")
    check("cache hit" not in one.getvalue(), "-v must not print the -vv detail")
    check("cache hit" in two.getvalue(), "-vv must print the detail")


def test_glyphs_fall_back_to_ascii_a_stream_can_encode() -> None:
    """A decorative character must not raise inside somebody's merge."""
    rich = console.Console(Stream(encoding="utf-8"), verbosity=1, enabled=False)
    plain = console.Console(Stream(encoding="ascii"), verbosity=1, enabled=False)
    check(rich.glyphs["done"] == "✓", "a UTF-8 stream should get the nicer glyph")
    for name, (fancy, ascii_) in console.GLYPHS.items():
        check(plain.glyphs[name] == ascii_,
              f"an ASCII stream must fall back for {name}")
        ascii_.encode("ascii")  # raises here rather than in a report if it ever changes


def test_nothing_animates_without_a_terminal() -> None:
    """The ticker is the one thread this project starts. It must not start under a pipe."""
    import threading

    quiet = console.Console(Stream(tty=False), verbosity=2, enabled=True)
    check(not quiet.animate, "a pipe must not animate even with colour forced on")
    before = threading.active_count()
    with quiet.waiting("waiting") as elapsed:
        check(elapsed() >= 0, "the elapsed clock must run whether or not it is shown")
    check(threading.active_count() == before,
          "a non-animating console must start no thread")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
    if failures:
        print(f"{len(failures)} failing, of {checks}:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"console: all {checks} checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
