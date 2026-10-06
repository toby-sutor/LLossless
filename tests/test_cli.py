#!/usr/bin/env python3
"""Offline checks for the `llossless` command. No network, no model.

Every test here runs `cli.main` end to end against a real loopback endpoint
(tests/fake_endpoint.py), because the things worth checking about a CLI are
properties of the whole path: that the exit code agrees with the report, that a
step which errored is visible in both, that `--dry-run` sends nothing, and that
the model was shown the canonical filenames whatever the caller typed.

The structured-output tier is pinned to `prompt` throughout. The capability
probe is `client.py`'s job and is tested there; leaving it on here would put a
negotiation the CLI does not own inside every assertion about the CLI.

Run with `python3 tests/test_cli.py`, or collect with pytest.
"""

from __future__ import annotations

import contextlib
import dataclasses
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs, so a test that points a
# socket anywhere but the configured endpoint fails loudly instead of
# succeeding quietly. tests/test_socket_guard.py asserts every module does this.
socket_guard.install()

from llossless import (  # noqa: E402
    __version__, cli, config, html_report, merge, prompts, reconcile, report,
    structured, sweep, verify,
)
from llossless.client import Client, SCHEMA_ATTEMPTS  # noqa: E402
from llossless.console import RED, RESET, strip  # noqa: E402
from llossless.decompose import Claim  # noqa: E402
from llossless.provenance import Provenance  # noqa: E402
from llossless.verify import (  # noqa: E402
    MERGED_TO_SOURCES, SOURCE_TO_MERGED, Graded, Verdict,
)

from fake_endpoint import FakeEndpoint, envelope  # noqa: E402

failures: list[str] = []

SOURCE_A = "The relay listens on port 8443.\nThe connect timeout is 30 seconds.\n"
SOURCE_B = "The relay listens on port 8443.\nThe read timeout is 45 seconds.\n"
SOURCE_C = "The relay listens on port 8443.\nThe idle timeout is 90 seconds.\n"
MERGED = (
    "The relay listens on port 8443.\n"
    "The connect timeout is 30 seconds.\n"
    "The read timeout is 45 seconds.\n"
)
# The same merge over three sources. `MERGED` leaves `C`'s idle timeout out of
# it, which the reconciler now reads as an undeclared absence and a lost `90
# seconds`, so a test about the third document reaching the pipeline would fail
# on the merged text being wrong rather than on the count.
MERGED_ABC = MERGED + "The idle timeout is 90 seconds.\n"

# Twelve segments each, and the count is the point rather than the content.
# The declared-loss budget makes a declared drop a finding above 5% of the source segments, so on the
# two-line sources above *any* declared drop is 25% and over budget — which would
# make "a declared drop does not move the exit code" untestable, because the
# budget would move it for an unrelated reason. At 24 segments one drop is 4.2%
# and passes, two are 8.3% and fail, so both sides of the declared-loss budget are reachable from the
# same pair. `a3` carries two facts in one line on purpose: it is the only way to
# get one segment with two claims, which is what a rejected declaration needs to
# be more than a tautology.
LONG_A = (
    "The relay listens on port 8443.\n"
    "The connect timeout is 30 seconds.\n"
    "The archive rotates every 7 days and every archive is signed.\n"
    "The queue drains at 200 messages per second.\n"
    "The cache holds 4096 entries.\n"
    "The retry limit is 5 attempts.\n"
    "The audit log is written to /var/log/relay.\n"
    "The health probe runs every 15 seconds.\n"
    "The certificate is renewed every 90 days.\n"
    "The metrics port is 9100.\n"
    "The worker pool starts with 8 threads.\n"
    "The shutdown delay is 20 seconds.\n"
)
LONG_B = (
    "The relay listens on port 8443.\n"
    "The read timeout is 45 seconds.\n"
    "The backup window opens at 02:00 UTC.\n"
    "The replica count is 3.\n"
    "The index is rebuilt every 6 hours.\n"
    "The upload limit is 25 megabytes.\n"
    "The session cookie expires after 12 hours.\n"
    "The admin console is served on port 8080.\n"
    "The rate limiter allows 60 requests per minute.\n"
    "The changelog is published every Friday.\n"
    "The staging cluster runs 2 nodes.\n"
    "The support address is relay@example.invalid.\n"
)
LONG_SEGMENTS = 24


def faithful_merge(*declared: dict) -> str:
    """Both sources in full, the shared line once, minus what was declared dropped.

    Built rather than written out, because an earlier version wired the reconciler
    into the pipeline. The three-line document this replaced lost 21 of 24 segments
    with nothing said about them, which is now nineteen `undeclared_absence`
    findings and eighteen `verbatim_violation`s — and every test below would
    have failed on a defect in the fixture rather than on the thing it asserts.
    A merge that carries everything it did not declare away is the only fixture
    that leaves the exit code free to be about a test's own subject.
    """
    gone = {
        record["segment"] for record in declared
        if record.get("disposition") == "dropped"
    }
    lines: list[str] = []
    for letter, text in (("a", LONG_A), ("b", LONG_B)):
        for index, line in enumerate(text.splitlines(), start=1):
            if f"{letter}{index}" in gone or line in lines:
                continue
            lines.append(line)
    return "".join(line + "\n" for line in lines)


LONG_MERGED = faithful_merge()
# The merge `LONG_MERGED` used to be: three lines, 21 segments gone, nothing
# declared about any of them. Kept as a fixture rather than deleted, because it
# is the exact shape this check exists to catch: every claim it was asked about
# comes back SUPPORTED, so no verify pass objects and the run exited 0.
LONG_MERGED_SHORT = (
    "The relay listens on port 8443.\n"
    "The connect timeout is 30 seconds.\n"
    "The read timeout is 45 seconds.\n"
)


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# a scripted endpoint
# --------------------------------------------------------------------------


def claims(*rows: tuple[str, int]) -> str:
    return json.dumps(
        {"claims": [{"text": text, "line": line, "span": text} for text, line in rows]}
    )


def verdicts(*rows: tuple[str, str, str, str]) -> str:
    return json.dumps(
        {
            "verdicts": [
                {
                    "claim_id": claim_id,
                    "verdict": verdict,
                    "evidence": evidence,
                    "evidence_source": source,
                    "rationale": "The reference text settles it.",
                }
                for claim_id, verdict, evidence, source in rows
            ]
        }
    )


class Script:
    """Replies chosen by which prompt arrived, not by call order.

    Order would make every test depend on the pipeline's step sequence, so a
    reordering would break twenty assertions that are not about ordering. The
    first line of each prompt file is the discriminator; `test_the_script_still
    _recognises_every_prompt` fails if one of them is reworded.
    """

    # The empty answer for each merge key a fixture may not carry. Empty is
    # the *honest* answer in both cases: no addition was declared, and no
    # mismatch was noticed.
    _MERGE_EMPTIES = {"additions": list, "mismatch": ""}

    MARKERS = {
        "merge": "Combine the source documents below",
        # First, and deliberately so. The coverage prompt opens with
        # decompose's own sentence -- it is assembled from that prompt and the
        # forward one -- so the more specific rule has to be asked first or
        # every coverage call is answered with a decompose payload.
        "coverage": "then decide whether the merged document carries each one",
        "decompose": "Extract every independently checkable factual assertion",
        "forward": "supported by the reference text below",
        "reverse": "supported by the source documents below",
    }

    def __init__(self, **replies: object) -> None:
        self.replies = replies
        self.seen: list[str] = []
        self.bodies: list[dict] = []

    def kind(self, content: str) -> str:
        for name, marker in self.MARKERS.items():
            if marker in content:
                return name
        raise AssertionError(f"unrecognised prompt: {content[:80]!r}")

    def __call__(self, body: dict, _n: int):
        self.bodies.append(body)
        content = body["messages"][0]["content"]
        kind = self.kind(content)
        self.seen.append(kind)
        reply = self.replies[kind]
        if callable(reply):
            reply = reply(self.seen.count(kind))
        if reply is None:  # the model answering unusably, twice
            return 200, envelope("not json at all")
        return 200, envelope(self.answering_the_schema(kind, content, reply))

    @staticmethod
    def answering_the_schema(kind: str, content: str, reply: object) -> object:
        """Supply the empty answer for a required key the fixture omitted.

        The merge schema is level-shaped: `additions` exists at `open` and
        nowhere else, and `required` lists it there, so one canned reply cannot
        satisfy every level. `mismatch` is required at every level, which
        no fixture written before it existed supplies. A real compliant model answers the schema it was
        given, and this is the smallest way for the fake to do the same --
        without it, every fixture would need a fifth variant and every
        level-parametrised test would assert against a fake that no model
        resembles.

        Only an absent key is filled, and only with the empty list, which is
        the honest answer for a merge that added nothing. A fixture that
        declares additions of its own passes through untouched, so nothing here
        can manufacture the thing under test.
        """
        if kind != "merge":
            return reply
        try:
            payload = json.loads(reply)
        except (TypeError, ValueError):
            return reply  # a deliberately unusable reply stays unusable
        if not isinstance(payload, dict):
            return reply
        filled = False
        for key, empty in Script._MERGE_EMPTIES.items():
            # Only where the request asked for the key, and only where the
            # fixture did not answer it. A fixture that supplies its own value
            # passes through untouched, so the fake cannot manufacture the
            # thing under test.
            if f'"{key}"' in content and key not in payload:
                payload[key] = empty() if callable(empty) else empty
                filled = True
        return json.dumps(payload) if filled else reply


@contextlib.contextmanager
def workspace(script, *, merged_on_disk: bool = False, **endpoint_kwargs):
    """A temp dir with the sources in it, and a base_url wired to `script`.

    LLOSSLESS_CACHE_DIR is redirected into the temp dir for the duration. A
    test suite that leaves files in the working tree is a test suite that will
    one day leave a wrong one. `--no-cache` used to stop responses being cached
    and not the raw dump a schema failure writes; it stops both now.
    """
    with tempfile.TemporaryDirectory() as raw, \
            FakeEndpoint(script, **endpoint_kwargs) as base_url:
        home = Path(raw)
        (home / "notes-a.md").write_text(SOURCE_A, encoding="utf-8")
        (home / "notes-b.md").write_text(SOURCE_B, encoding="utf-8")
        (home / "notes-c.md").write_text(SOURCE_C, encoding="utf-8")
        (home / "long-a.md").write_text(LONG_A, encoding="utf-8")
        (home / "long-b.md").write_text(LONG_B, encoding="utf-8")
        if merged_on_disk:
            (home / "draft.md").write_text(MERGED, encoding="utf-8")
        was = os.environ.get("LLOSSLESS_CACHE_DIR")
        os.environ["LLOSSLESS_CACHE_DIR"] = str(home / "cache")
        try:
            yield home, base_url
        finally:
            if was is None:
                del os.environ["LLOSSLESS_CACHE_DIR"]
            else:
                os.environ["LLOSSLESS_CACHE_DIR"] = was


def invoke(home: Path, base_url: str, *argv: str,
           cache: str | None = "--no-cache") -> tuple[int, str, str]:
    """Run the command, capturing both streams. Returns (code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    # Both model flags: --model leaves an already-configured merge model alone,
    # so a machine with models.local.json would otherwise put its own model id
    # in the provenance block of a test that never called it.
    argv = list(argv)
    # `--base` is required on the command line and every caller below is merging
    # its first path into its second, so the helper supplies it rather than
    # twenty call sites repeating it. The refusals it exists for are asserted
    # directly in `test_the_base_document_must_be_named_and_must_be_a_source`.
    if argv and argv[0] == "merge" and "--base" not in argv:
        argv += ["--base", argv[1]]
    argv += [
        "--base-url", base_url,
        "--model", "test-model",
        "--merge-model", "test-model",
        "--structured", "prompt",
    ]
    # `--no-cache` by default, because a test suite that fills a cache is a
    # test suite whose second run measures the first. `cache=None` leaves the
    # flags alone entirely, which is the only way to see what the *default*
    # does, and it is what three checks written for the cache-default rule needed and did not
    # have: every invocation arrived with the flag already appended, so they
    # passed against the unfixed code and measured this helper.
    if cache is not None:
        argv.append(cache)
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


CLEAN = {
    # All three fields, because an earlier milestone made all three required. An empty list is the
    # honest answer for these two sources: nothing was chosen between, and every
    # segment came over unchanged.
    "merge": json.dumps({"merged_document": MERGED, "decisions": [], "dispositions": []}),
    "decompose": lambda n: claims(("The relay listens on port 8443.", 1))
    if n < 3
    else claims(("The relay listens on port 8443.", 1)),
    "forward": verdicts(
        ("A-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
        ("B-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
    ),
    "reverse": verdicts(
        ("M-001", "SUPPORTED", "The relay listens on port 8443.", "source_a.md")
    ),
}


# --------------------------------------------------------------------------
# the parser
# --------------------------------------------------------------------------


def parse_fails(argv: list[str], message: str) -> None:
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            cli.build_parser().parse_args(argv)
        except SystemExit as exit_code:
            check(exit_code.code == 2, f"{message} (exited {exit_code.code}, expected 2)")
            return
    failures.append(f"{message} (nothing was rejected)")


def test_both_subcommands_exist_and_take_the_arity_the_readme_states() -> None:
    """Two commands, two or more sources each, and the merge only on `verify`."""
    parser = cli.build_parser()
    merge_args = parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md"])
    check(merge_args.command == "merge", "the merge subcommand must be named merge")
    check([str(path) for path in merge_args.sources] == ["a.md", "b.md"],
          "merge must bind its positionals in order")

    three = parser.parse_args(["merge", "a.md", "b.md", "c.md", "--base", "b.md"])
    check([str(path) for path in three.sources] == ["a.md", "b.md", "c.md"],
          "merge must take a third source")

    verify_args = parser.parse_args(["verify", "a.md", "b.md", "m.md"])
    check(verify_args.command == "verify", "the verify subcommand must be named verify")
    check(str(verify_args.merged) == "m.md", "verify must take the merged document last")
    check([str(path) for path in verify_args.sources] == ["a.md", "b.md"],
          "verify must leave the last path to `merged` and not swallow it")
    four = parser.parse_args(["verify", "a.md", "b.md", "c.md", "m.md"])
    check(str(four.merged) == "m.md" and len(four.sources) == 3,
          "verify's greedy source list must still leave the merge its own slot")

    parse_fails(["merge", "a.md", "b.md"], "merge must require --base")
    parse_fails(["verify", "a.md"], "verify must require the merged document")
    parse_fails(["check", "a.md", "b.md", "m.md"], "there is no `check` subcommand")

    # One source is refused by the parser rather than by `check_sources`, so the
    # message carries the usage line and no file is opened first.
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            cli.main(["merge", "a.md", "--base", "a.md"])
        except SystemExit as exit_code:
            check(exit_code.code == 2, f"one source must exit 2, got {exit_code.code}")
        else:
            check(False, "one source must be refused")
    check("at least 2" in err.getvalue(),
          f"the refusal must say what the floor is, got {err.getvalue()!r}")


def cli_error(argv: list[str]) -> str:
    """Run `main` for its refusal. Returns stderr; fails the check if it succeeded."""
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        code = cli.main(argv)
    check(code == 2, f"{argv} must exit 2, got {code}")
    return err.getvalue()


def test_three_sources_run_the_whole_pipeline() -> None:
    """End to end: the count reaches decompose, verify and the report.

    The forward pass is the one that would notice a third document being
    dropped somewhere in the middle -- it sends every source's claims in one
    batch, so `C-001` arriving is the evidence that `notes-c.md` was decomposed
    at all, and the coverage table is where a reader would see it missing.
    """
    script = Script(
        merge=json.dumps(
            {"merged_document": MERGED_ABC, "decisions": [], "dispositions": []}
        ),
        decompose=lambda n: claims(("The relay listens on port 8443.", 1)),
        forward=verdicts(
            ("A-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
            ("B-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
            ("C-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
        ),
        reverse=verdicts(
            ("M-001", "SUPPORTED", "The relay listens on port 8443.", "source_c.md")
        ),
    )
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"), str(home / "notes-c.md"),
            "--base", str(home / "notes-b.md"),
        )

    check(code == 0, f"a clean three-source run must exit 0, got {code}: {err[:300]}")
    check(script.seen.count("decompose") == 4,
          f"three sources and the merge is four decomposes, got {script.seen}")
    for name in ("notes-a.md", "notes-b.md", "notes-c.md"):
        check(name in out, f"the coverage table must name {name}, got {out[:800]!r}")

    # The base reached the prompt as the document the operator pointed at, not
    # as the first one they typed.
    merged_prompt = next(
        body["messages"][0]["content"] for body in script.bodies
        if "Combine the source documents below" in body["messages"][0]["content"]
    )
    check('filename="source_b.md" base="true"' in merged_prompt,
          "--base notes-b.md must mark source_b.md, not source_a.md")
    # Counted per document rather than over the whole prompt: `merge.md` states
    # the base rule and shows a worked example, so the string occurs twice in
    # the prompt text before any source is rendered into it.
    for name in ("source_a.md", "source_c.md"):
        check(f'filename="{name}" base="true"' not in merged_prompt,
              f"{name} must not also be marked as the base")
    check('filename="source_c.md"' in merged_prompt,
          "the third source must reach the merge prompt")


def test_the_base_document_must_be_named_and_must_be_a_source() -> None:
    """Exactly one document carries base="true", and the CLI will not pick.

    `merge_documents` still defaults to the first source for a library caller who
    has already decided. A command line has not: `--base` changes which title is
    kept and which structure is followed, and with three paths typed in some
    order "the first one" is a decision made on the operator's behalf without
    telling them. So zero matches is an error and so is two, and neither is
    resolved by choosing.

    Refused before any file is opened, which is why this needs no workspace: the
    message names the paths the operator typed, not the canonical names this
    module would have given them.
    """
    missing = cli_error(["merge", "a.md", "b.md", "--base", "c.md"])
    check("--base c.md is not one of the sources" in missing,
          f"a base naming no source must say so, got {missing!r}")
    check("a.md, b.md" in missing,
          f"the refusal must list what the sources were, got {missing!r}")

    twice = cli_error(["merge", "a.md", "./a.md", "--base", "a.md"])
    check("more than once" in twice,
          f"the same file twice must be refused rather than resolved, got {twice!r}")

    # And the match is on the resolved path, so an operator is not asked to
    # retype the spelling they used.
    parsed = cli.build_parser().parse_args(["merge", "a.md", "b.md", "--base", "./b.md"])
    check(cli.canonical_base(parsed.base, dict(zip(("source_a.md", "source_b.md"),
                                                   parsed.sources))) == "source_b.md",
          "./b.md and b.md must be one document")


def test_verify_refuses_base_rather_than_reading_it_as_base_url() -> None:
    """`verify` composes nothing, so there is no base, and no prefix.

    The refusal is worth a test of its own because the flag is not unknown on
    this subparser: argparse accepts unambiguous abbreviations, and `--base` is
    one of `--base-url`. Deleted, this test would go on passing while
    `--base notes-a.md` silently set the endpoint to a filename and the run
    failed somewhere else entirely.
    """
    refused = cli_error(["verify", "a.md", "b.md", "m.md", "--base", "a.md"])
    check("verify takes no --base" in refused,
          f"verify must refuse --base by name, got {refused!r}")
    check("--base-url" in refused,
          f"the refusal must point at the flag that was probably meant, got {refused!r}")

    # And the flag it is a prefix of still works, on both commands.
    for argv in (["verify", "a.md", "b.md", "m.md"], ["merge", "a.md", "b.md", "--base", "a.md"]):
        parsed = cli.build_parser().parse_args(argv + ["--base-url", "http://x/v1"])
        check(parsed.base_url == "http://x/v1",
              f"--base-url must survive on {argv[0]}, got {parsed.base_url!r}")


def merge_with_no_base(home: Path, base_url: str) -> tuple[str, dict]:
    """A merge run with nobody naming a base. Returns (markdown, dict).

    Not reachable from the command line, which is the point: `--base` is
    required there and `merge_documents` keeps its default for library callers,
    so this is the only path on which `defaulted` can be produced -- and the one
    the record exists for. It goes through `cli.pipeline` rather than around it,
    because the pipeline is what carries the base off the merge result, and a
    test that assembled the `Run` by hand would assert my arithmetic instead of
    the code's.
    """
    argv = [
        "merge", str(home / "notes-a.md"), str(home / "notes-b.md"),
        # Parsed and then not passed on: `main` requires it, `pipeline` does not.
        "--base", str(home / "notes-a.md"),
        "--base-url", base_url, "--model", "test-model",
        "--merge-model", "test-model", "--structured", "prompt", "--no-cache",
    ]
    args = cli.build_parser().parse_args(argv)
    settings = config.resolve(args)
    names = merge.source_names(len(args.sources))
    documents = {
        name: path.read_text(encoding="utf-8") for name, path in zip(names, args.sources)
    }
    loaded = {
        "merge": prompts.load("merge"),
        "decompose": prompts.load("decompose"),
        SOURCE_TO_MERGED: prompts.load("verify"),
        MERGED_TO_SOURCES: prompts.load("verify_reverse"),
    }
    client = Client(settings)
    run = report.Run(command="merge")
    run.paths = {name: str(path) for name, path in zip(names, args.sources)}
    cli.pipeline(client, run, documents, loaded)
    run.provenance = Provenance(
        settings=settings,
        client=client,
        roles=cli.ROLES,
        duration_seconds=0.0,
        base=run.base,
        base_chosen=run.base_chosen,
    )
    return report.render(run), report.as_dict(run)


def test_the_level_the_report_names_is_the_level_all_three_passes_ran_at() -> None:
    """`--fidelity high` has to reach the merger and both graders, not just the header.

    It did not. `Settings.fidelity` was resolved, stamped into `merge_policy`
    and rendered, and `cli.pipeline` then called `merge_documents` with no
    policy at all — so a run reported at `high` was performed at `off`, which is
    the same defect as a title policy printed without its base and worse,
    because the number underneath it changes meaning with the level.
    An earlier fix is what made it visible: once both verify prompts take the level,
    three passes had to agree about it and one call site supplying it was the
    only way they could.

    Asserted over the wire. `MergePolicy` being constructed correctly is not the
    property in question; the property is that the fragment for the level named
    in the header is in all three requests.
    """
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"), "--fidelity", "high",
        )
    check(code == 0, f"the run must succeed, got {code}")
    check("| Fidelity | high |" in out,
          "the report must name the level the run was asked for")

    high = merge.MergePolicy(fidelity="high")
    # The contrast level, literal. It was written as `DEFAULT_FIDELITY` back
    # when that was `off`, which read as "not the level we fell back to" -- and
    # a later change made the default `high`, turning the negative assertion below into
    # "a run asked for high was not given the high fragment". Pinned to `off`,
    # and the `mid` run at the end of this test is what now carries the
    # property the default used to carry here: that the flag is read at all.
    off = merge.MergePolicy(fidelity="off")
    roles = {"merge": "merge", "forward": "verify", "reverse": "verify_reverse"}
    sent: dict[str, list[str]] = {}
    for body in script.bodies:
        content = body["messages"][0]["content"]
        sent.setdefault(script.kind(content), []).append(content)

    for kind, role in roles.items():
        requests = sent.get(kind, [])
        check(len(requests) > 0, f"no {kind} request was made, so nothing was asserted")
        for content in requests:
            check(high.fragment(role).text.strip() in content,
                  f"the {kind} pass was not given the high fragment; the header "
                  f"says high and the request says otherwise")
            check(off.fragment(role).text.strip() not in content,
                  f"the {kind} pass was given the off fragment on a run asked "
                  f"for high")

    # And on `verify`, which made no merge and is the run where the level is
    # most easily forgotten: the README tells the operator to pass the level the
    # merge was written at, so a `verify` run that ignored --fidelity would make
    # that instruction useless. Only the two graders run here; there is no merge
    # request to check.
    script = Script(**CLEAN)
    with workspace(script, merged_on_disk=True) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "verify",
            str(home / "notes-a.md"), str(home / "notes-b.md"), str(home / "draft.md"),
            "--fidelity", "high",
        )
    check(code == 0, f"the verify run must succeed, got {code}")
    check("| Fidelity | high |" in out, "a verify run reports the level it graded at")
    graded = [body["messages"][0]["content"] for body in script.bodies]
    check("merge" not in {script.kind(content) for content in graded},
          "a verify run must make no merge call; the rest of this check assumes it")
    for kind, role in (("forward", "verify"), ("reverse", "verify_reverse")):
        requests = [c for c in graded if script.kind(c) == kind]
        check(len(requests) > 0, f"no {kind} request was made on the verify run")
        for content in requests:
            check(high.fragment(role).text.strip() in content,
                  f"the {kind} pass of a verify run ignored --fidelity, so the "
                  f"README's instruction to pass the merge's level does nothing")

    # Once more at a level that is not the default. Everything above asks
    # for `high`, which is now also what a run with no flag would take, so a
    # pipeline that dropped the policy on the floor a second time would pass
    # every assertion above by falling back to the same fragment it was meant
    # to be handed. That is precisely the defect this test was written for, so
    # the level has to differ from the default for the assertion to see it.
    check("mid" != config.DEFAULT_FIDELITY,
          "this block only discriminates while mid is not the default level")
    mid = merge.MergePolicy(fidelity="mid")
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"), "--fidelity", "mid",
        )
    check(code == 0, f"the mid run must succeed, got {code}")
    check("| Fidelity | mid |" in out, "the report must name mid")
    sent = {}
    for body in script.bodies:
        content = body["messages"][0]["content"]
        sent.setdefault(script.kind(content), []).append(content)
    for kind, role in roles.items():
        requests = sent.get(kind, [])
        check(len(requests) > 0, f"no {kind} request was made at mid")
        for content in requests:
            check(mid.fragment(role).text.strip() in content,
                  f"the {kind} pass was not given the mid fragment")
            check(high.fragment(role).text.strip() not in content,
                  f"the {kind} pass fell back to the default fragment on a run "
                  f"asked for mid")


def test_the_vv_banner_names_the_fidelity_the_wire_requests_actually_carry() -> None:
    """`-vv` prints a fidelity level; it has to be the one the run used.

    Same shape of defect as the report-level check above, one layer up: the
    banner is written from whatever the call site in `cli.main` hands
    `console.banner`, before any model call is made. A call site that read
    `config.DEFAULT_FIDELITY`, or the raw `--fidelity` string off `args` rather
    than the resolved `MergePolicy`, would print the same thing as a correct
    call on a run that happened to ask for the default -- and print something
    else on every run that did not. `mid` is not the default, so a
    defaulted or unresolved read is visibly wrong here, and the check is made
    twice: once against the printed line, once against what the wire actually
    carries, so the two cannot silently agree with each other while both being
    wrong the same way.
    """
    check("mid" != config.DEFAULT_FIDELITY,
          "this test only discriminates while mid is not the default level")
    mid = merge.MergePolicy(fidelity="mid")
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--fidelity", "mid", "-vv",
        )
    check(code == 0, f"the run must succeed, got {code}")
    check("fidelity mid" in err,
          f"-vv must print the configured fidelity level, got {err!r}")
    check("fidelity high" not in err,
          f"the banner named a level other than the one asked for: {err!r}")

    roles = {"merge": "merge", "forward": "verify", "reverse": "verify_reverse"}
    sent: dict[str, list[str]] = {}
    for body in script.bodies:
        content = body["messages"][0]["content"]
        sent.setdefault(script.kind(content), []).append(content)
    for kind, role in roles.items():
        requests = sent.get(kind, [])
        check(len(requests) > 0, f"no {kind} request was made, so nothing was asserted")
        for content in requests:
            check(mid.fragment(role).text.strip() in content,
                  f"the {kind} pass ran at a level other than the one the "
                  f"-vv banner named as mid")


def test_the_banner_names_a_depth_that_stops_checking_at_any_verbosity() -> None:
    """The one banner field that is not gated behind `-vv`, and why.

    `fidelity` waits for `-vv` because it is configuration and a terminal line
    has to stay short. `coverage` is not configuration in that sense: it
    suspends the guarantee this tool exists to make. An operator who set the
    environment variable last week and runs an ordinary `-v` merge today is
    about to read a clean result that means less than a clean result usually
    does, and learning that afterwards from the provenance block is learning it
    too late.

    Four cases, because the rule has four parts and any one of them alone
    would look like it worked: the cheap depth prints with no `-v` at all and
    again at the ordinary verbosity, the default stays quiet there, and the
    default does print under `-vv` beside the fidelity it belongs with.

    **The first case is the one that was missing.** `--verbose` defaults to 0
    and `Console.banner` returned before printing anything below 1, so "prints
    at every verbosity" was true of every verbosity except the one almost
    every run uses. It was invisible because this test passed `-v` to
    exercise what it called the ordinary case -- a test that sets the thing it
    is measuring cannot see the default.

    Asserted against **the banner line alone** and not against stderr. A
    coverage run also writes two skipped steps whose reasons quote the flag --
    *"--verify-depth coverage does not check for invention"* -- and those print
    at `-v` too, so a search of the whole stream finds the words `depth
    coverage` whatever the banner did. The first cut of this test did exactly
    that and stayed green under a seeded break that removed the banner field.
    """
    def banner_of(stderr: str) -> str:
        lines = [line for line in stderr.splitlines()
                 if line.startswith("LLossless ")]
        check(len(lines) == 1,
              f"expected exactly one banner line, found {len(lines)} in "
              f"{stderr!r}")
        return lines[0] if lines else ""

    replies = dict(CLEAN)
    replies["coverage"] = lambda n: _coverage(
        ("The relay listens on port 8443.", 1,
         "The relay listens on port 8443", "SUPPORTED",
         "The relay listens on port 8443"))

    with workspace(Script(**replies)) as (home, base_url):
        code, _, bare = invoke(home, base_url, *sweep_argv(
            home, "--verify-depth", "coverage"))
    check(code == 0, f"the coverage run must succeed with no -v, got {code}")
    check("depth coverage" in banner_of(bare),
          f"the banner must carry the depth at the default verbosity, which is "
          f"the verbosity nearly every run has, got {banner_of(bare)!r}")

    with workspace(Script(**CLEAN)) as (home, base_url):
        code, _, silent = invoke(home, base_url, *sweep_argv(home))
    check(code == 0, f"the default run must succeed with no -v, got {code}")
    check(not [line for line in silent.splitlines()
               if line.startswith("LLossless ")],
          f"and a run at the default depth must still print no banner without "
          f"-v: the floor moved for one case, not for all of them, got "
          f"{silent!r}")

    with workspace(Script(**replies)) as (home, base_url):
        code, _, cheap = invoke(home, base_url, *sweep_argv(
            home, "--verify-depth", "coverage", "-v"))
    check(code == 0, f"the coverage run must succeed, got {code}")
    check("depth coverage" in banner_of(cheap),
          f"a depth that stops checking for invention must be on the banner at "
          f"the ordinary verbosity, got {banner_of(cheap)!r}")

    with workspace(Script(**CLEAN)) as (home, base_url):
        code, _, quiet = invoke(home, base_url, *sweep_argv(home, "-v"))
    check(code == 0, f"the default run must succeed, got {code}")
    check("depth" not in banner_of(quiet),
          f"the default depth must not add a word to every banner ever "
          f"printed; it says nothing changed, got {banner_of(quiet)!r}")

    with workspace(Script(**CLEAN)) as (home, base_url):
        code, _, loud = invoke(home, base_url, *sweep_argv(home, "-vv"))
    check(code == 0, f"the -vv run must succeed, got {code}")
    check(f"depth {config.DEFAULT_VERIFY_DEPTH}" in banner_of(loud),
          f"under -vv the depth is configuration like the level and belongs "
          f"beside it, got {banner_of(loud)!r}")


def test_a_declared_drop_the_merge_kept_is_rejected_without_becoming_a_finding() -> None:
    """End to end, on the case only this check can catch.

    The merge declares it dropped `a1` and then ships the fact anyway. Nothing
    else in the tool notices: the forward pass says SUPPORTED and is right, so
    there is no finding; `reconcile`'s replacement check passes because a drop
    names no replacement; and the declared-loss budget counts the record without
    ever asking whether it was true. The declaration is false and the merged
    document is fine, which is exactly the split between findings and the review queue, so it is reported
    and it produces no finding, and both halves of that are asserted here.

    The exit code is 1 and that is not this test's subject. These sources are
    two lines each, so one declared drop is 25% of four segments and the declared-loss budget fails
    the run on volume alone, which an earlier fix wired to the exit code and which
    says nothing about whether the declaration was true. So the assertion is on
    `findings`, which stays empty, and on the budget being the named cause;
    `test_a_declared_drop_the_forward_pass_confirms_is_not_charged` is where a
    declaration meets an exit code with no budget breach underneath it.
    """
    kept = json.dumps({
        "merged_document": MERGED,
        "decisions": [],
        "dispositions": [{
            "segment": "a1",
            "disposition": "dropped",
            "replacement": "",
            "reason": "the other document states the same thing.",
        }],
    })
    with workspace(Script(**{**CLEAN, "merge": kept})) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    check(code == 1, f"1 of 4 segments declared dropped is over budget; got {code}")
    check("## Declarations" in out, "a merge run reports what it declared")
    check("| `a1` | dropped | the other document states the same thing. | "
          "**rejected** |" in out,
          f"the false declaration must be rejected in the report, beside the "
          f"reason it gave; got "
          f"{[line for line in out.splitlines() if 'a1' in line]}")
    check("A-001" in out,
          "a rejected declaration must name the claim that rejected it")
    check("**1** departure(s)" in out and "rejects 1" in out,
          f"the counts above the table must agree with it; got "
          f"{[line for line in out.splitlines() if 'departure' in line]}")
    check(data["findings"] == [],
          f"a rejected declaration is not a finding and must not become one; "
          f"got {data['findings']}")
    check(data["declared_loss"] == {"drops": 1, "segments": 4, "budget": 0.03,
                                    "check_disabled": False, "over_budget": True,
                                    "ratio": 1 / 4},
          f"the exit code must be attributable to the budget and to nothing "
          f"else; got {data['declared_loss']}")
    check([(d["segment"], d["grade"]) for d in data["declarations"]] == [("a1", "rejected")],
          f"the JSON must carry the same grade as the markdown, got {data['declarations']}")

    # And the silent case, which is a claim too: CLEAN declares nothing, and
    # under the disposition model, that asserts every source segment survived character for
    # character. A section that vanished when there was nothing to list would
    # leave the strongest statement in the report unprinted.
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
        )
    check(code == 0, f"the clean run must exit 0, got {code}")
    check("declared no departures" in out,
          "a merge that declared nothing must say so, not omit the section")

    # `verify` merged nothing and was told nothing, so it has no declarations to
    # report and must not print an empty verdict about someone else's merge.
    with workspace(Script(**CLEAN), merged_on_disk=True) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "verify",
            str(home / "notes-a.md"), str(home / "notes-b.md"), str(home / "draft.md"),
        )
    check(code == 0, f"the verify run must exit 0, got {code}")
    check("## Declarations" not in out,
          "a verify run has no declarations of its own and must not claim otherwise")


# The claims the long sources hand back, and which segment each lands in. `a3`
# holds two of them because that is what makes a rejected declaration testable:
# one claim falsifies it and the other stays MISSING, so "rejected" and "the
# MISSING claim is still a finding" are two facts about the same segment rather
# than one restated.
LONG_A_CLAIMS = (
    ("The connect timeout is 30 seconds.", 2),   # A-001, segment a2
    ("The archive rotates every 7 days", 3),     # A-002, segment a3
    ("every archive is signed", 3),              # A-003, segment a3
)
LONG_B_CLAIMS = (("The read timeout is 45 seconds.", 2),)  # B-001, segment b2
LONG_M_CLAIMS = (("The relay listens on port 8443.", 1),)  # M-001


def dropped(*segments: str) -> list[dict]:
    return [
        {
            "segment": name,
            "disposition": "dropped",
            "replacement": "",
            "reason": "the fact is stale and belongs in neither document.",
        }
        for name in segments
    ]


def long_script(
    dispositions: list[dict],
    forward: tuple,
    *,
    a_claims=LONG_A_CLAIMS,
    merged: str | None = None,
):
    """A scripted run over the 24-segment sources. Decompose order is the pipeline's.

    The merged text defaults to one that agrees with `dispositions`: everything
    carried, except the segments this run says it dropped. Anything else is a
    reconciler finding, and a caller that wants one passes `merged`.
    """
    replies = (claims(*a_claims), claims(*LONG_B_CLAIMS), claims(*LONG_M_CLAIMS))
    return Script(
        merge=json.dumps({
            "merged_document": faithful_merge(*dispositions) if merged is None else merged,
            "decisions": [],
            "dispositions": dispositions,
        }),
        decompose=lambda n: replies[min(n, len(replies)) - 1],
        forward=verdicts(*forward),
        reverse=verdicts(
            ("M-001", "SUPPORTED", "The relay listens on port 8443.", "source_a.md")
        ),
    )


def long_merge(home: Path, base_url: str, *extra: str) -> tuple[int, str, dict]:
    code, out, _ = invoke(
        home, base_url, "merge",
        str(home / "long-a.md"), str(home / "long-b.md"),
        "--json", str(home / "report.json"), *extra,
    )
    return code, out, json.loads((home / "report.json").read_text(encoding="utf-8"))


def test_a_declared_drop_the_forward_pass_confirms_is_not_charged() -> None:
    """The review queue does not reach the exit code.

    The merge declares `a3` dropped, the forward pass finds both of that
    segment's claims missing, and the declaration is confirmed. Two claims are
    genuinely gone — the previous behaviour was two findings and exit 1, and the
    reason that was wrong is that nothing was lost by accident. The omission is
    on the page with a reason beside it, and a reader can put the fact back or
    agree it stays out. That is work, not a fault.

    One drop of 24 segments is 4.2%, inside the declared-loss budget, so nothing else here can move
    the exit code and a 0 means what it says.
    """
    with workspace(long_script(dropped("a3"), (
        ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
        ("A-002", "MISSING", "", ""),
        ("A-003", "MISSING", "", ""),
        ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
    ))) as (home, base_url):
        code, out, data = long_merge(home, base_url, "--loss-budget", "0.05")

    check(code == 0, f"a declared and confirmed drop must not fail the run; got {code}")
    check(data["findings"] == [],
          f"a queued drop must not also be a finding; got {data['findings']}")
    check([v["claim_id"] for v in data["review_queue"]] == ["A-002", "A-003"],
          f"both claims of the declared segment belong in the queue; got "
          f"{[v['claim_id'] for v in data['review_queue']]}")
    check(data["declared_loss"] == {"drops": 1, "segments": LONG_SEGMENTS, "budget": 0.05,
                                    "check_disabled": False, "over_budget": False,
                                    "ratio": 1 / LONG_SEGMENTS},
          f"one drop of {LONG_SEGMENTS} segments is inside the pinned 5% ceiling; got "
          f"{data['declared_loss']}")

    # The headline is the assertion that used to be false. "No extracted claim
    # was dropped" over a run holding two dropped claims would be the report
    # contradicting its own queue two sections down.
    check("No undeclared claim was dropped" in out,
          f"the verdict must not claim nothing was dropped when something was; "
          f"got {[line for line in out.splitlines() if line.startswith('**')]}")
    check("No extracted claim was dropped" not in out,
          "the clean sentence is false on a run with a non-empty queue")
    check("**2** dropped claim(s) are in the review queue below" in out,
          f"a verdict that passes over two dropped claims must say so and say "
          f"where; got {[line for line in out.splitlines() if line.startswith('**')]}")
    queue = out.split("## Review queue")[1].split("## Declarations")[0]
    for claim_id in ("A-002", "A-003"):
        check(claim_id in queue, f"{claim_id} must be listed in the review queue")
    check("### Dropped" not in out.split("## Review queue")[0],
          "a queued claim must not also appear under Findings")
    # A KB editor reading this decides whether to put the fact back,
    # and cannot decide it from the claim alone: the queue has to say where the
    # fact was, what the merge said about leaving it out, and that the absence
    # was checked rather than taken on the merge's word. The reason is quoted
    # and not graded -- it is the merge's sentence, in the merge's voice.
    check("the fact is stale and belongs in neither document." in queue,
          f"the queue must carry the merge's own reason; got {queue!r}")
    check("left out of: `a3`" in queue,
          f"the queue must name the segment the claim was left out of; got {queue!r}")
    check("confirmed absent" in queue,
          f"the queue must say the absence was confirmed, not assumed; got {queue!r}")


def test_an_undeclared_drop_is_still_a_finding_beside_a_declared_one() -> None:
    """The second half of the findings-versus-queue split: do not hide findings inside the queue.

    Same run, one more loss the merge said nothing about. The two are told apart
    by whose claim id a confirmed declaration covers, not by whether the run
    contains a declaration at all — which is the failure this test exists to
    catch, because filtering on "did anything get declared" would let one honest
    disclosure carry an arbitrary number of silent drops out of the exit code.
    """
    with workspace(long_script(dropped("a3"), (
        ("A-001", "MISSING", "", ""),
        ("A-002", "MISSING", "", ""),
        ("A-003", "MISSING", "", ""),
        ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
    ))) as (home, base_url):
        code, out, data = long_merge(home, base_url, "--loss-budget", "0.05")

    check(code == 1, f"an undeclared drop must fail the run; got {code}")
    check([v["claim_id"] for v in data["findings"]] == ["A-001"],
          f"only the undeclared loss is a finding; got "
          f"{[v['claim_id'] for v in data['findings']]}")
    check([v["claim_id"] for v in data["review_queue"]] == ["A-002", "A-003"],
          f"the declared losses stay queued; got "
          f"{[v['claim_id'] for v in data['review_queue']]}")
    check(not (set(v["claim_id"] for v in data["findings"])
               & set(v["claim_id"] for v in data["review_queue"])),
          "findings and the review queue must be disjoint")
    check("**1 finding(s).**" in out,
          f"the verdict counts findings and not queued claims; got "
          f"{[line for line in out.splitlines() if 'finding(s)' in line]}")

    findings = out.split("## Findings")[1].split("## Review queue")[0]
    check("A-001" in findings, "the undeclared loss must be under Findings")
    for claim_id in ("A-002", "A-003"):
        check(claim_id not in findings,
              f"{claim_id} was declared and must not be charged under Findings")


def test_a_rejected_declaration_accounts_for_nothing() -> None:
    """A declaration the forward pass disagrees with covers none of its claims.

    `a3` is declared dropped and one of its two claims comes back SUPPORTED, so
    the declaration is rejected. The other claim is still MISSING, and the
    question is what a rejected account of a segment does with it. Nothing: a
    merge that described this segment wrongly has not earned a queue entry for
    the part it happened to get right, so the loss is charged. `grade_declarations`
    lists only the falsifying claims on a rejected record, which is what makes
    the conservative reading fall out of the data rather than out of a special
    case here.
    """
    with workspace(long_script(dropped("a3"), (
        ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
        ("A-002", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
        ("A-003", "MISSING", "", ""),
        ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
    ))) as (home, base_url):
        code, out, data = long_merge(home, base_url)

    check(code == 1, f"the loss under a rejected declaration is charged; got {code}")
    check([(d["segment"], d["grade"]) for d in data["declarations"]]
          == [("a3", "rejected")],
          f"the declaration must be rejected; got {data['declarations']}")
    check([v["claim_id"] for v in data["findings"]] == ["A-003"],
          f"the MISSING claim of a rejected declaration stays a finding; got "
          f"{[v['claim_id'] for v in data['findings']]}")
    check(data["review_queue"] == [],
          f"a rejected declaration queues nothing; got {data['review_queue']}")
    check("None. Every claim the forward pass found missing is a finding" in out,
          "an empty queue says so rather than being omitted")


def test_the_reconciler_runs_and_its_findings_reach_the_exit_code() -> None:
    """Eight checks that never ran now do.

    Nine, after an earlier fix closed the same class of hole for duplication.

    The merge here keeps three of the 24 source segments and declares nothing,
    which is the case the whole disposition model is built around: under it
    silence asserts that every segment survived character for character, and
    this is the merge that makes that assertion falsely. Every claim the forward
    pass was given comes back SUPPORTED, so nothing in the verify layer objects
    and the run exited 0 before this test existed.

    The three assertions that matter are the finding, the denominator, and the
    step. The step is the one a reader needs most: `## Structure` printing "No
    structural finding" and `## Structure` never having been reached look the
    same to anyone who is not counting, and the whole point of the section is
    that the difference is visible.
    """
    with workspace(long_script([], (
        ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
        ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
    ), a_claims=(("The connect timeout is 30 seconds.", 2),),
        merged=LONG_MERGED_SHORT,
    )) as (home, base_url):
        code, out, data = long_merge(home, base_url)

    check(code == 1,
          f"a merge that silently lost 21 of 24 segments must not exit 0; got {code}")
    check(data["findings"] == [],
          f"no claim was lost, so the verify layer must still find nothing — the "
          f"exit code has to come from the reconciler; got {data['findings']}")
    kinds = {f["kind"] for f in data["structural"]["findings"]}
    check(kinds == {"undeclared_absence", "verbatim_violation"},
          f"an undeclared absence and its lost tokens are the finding; got {kinds}")
    check(data["structural"]["ran"] is True and data["structural"]["checks"] == 9
          and data["structural"]["segments"] == LONG_SEGMENTS,
          f"the section carries its denominator, not just its result; got "
          f"{ {k: v for k, v in data['structural'].items() if k != 'findings'} }")
    check([s["name"] for s in data["steps"]].count("reconcile") == 1,
          f"the reconciler must appear in the step list exactly once, so a report "
          f"that skipped it is distinguishable from one it passed; got "
          f"{[s['name'] for s in data['steps']]}")
    check("## Structure" in out and "Not checked" not in out,
          f"the report must carry the section and must not call a run it made "
          f"'not checked'; got {[l for l in out.splitlines() if l.startswith('##')]}")

    # And the clean side of the same wiring: a faithful merge declaring nothing
    # passes all eight, and says over how many segments it did so. Without this
    # the test above is satisfied by a reconciler that fails everything.
    with workspace(long_script([], (
        ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
        ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
    ), a_claims=(("The connect timeout is 30 seconds.", 2),))) as (home, base_url):
        code, out, data = long_merge(home, base_url)

    check(code == 0, f"a faithful merge must still exit 0; got {code}")
    check(data["structural"] == {"ran": True, "checks": 9,
                                 "segments": LONG_SEGMENTS, "findings": []},
          f"nine checks over 24 segments, nothing found; got {data['structural']}")
    check("No structural finding." in out,
          "a clean reconciliation says so under its own heading")

    # `verify` merged nothing and was told nothing, so there is no declaration
    # to hold anything against and no section. The reconciler is not run over
    # someone else's merge: checks 1, 3 and 4 would be vacuous and check 2 would
    # fail every reworded sentence, which is a different tool's answer.
    with workspace(Script(**CLEAN), merged_on_disk=True) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "verify",
            str(home / "notes-a.md"), str(home / "notes-b.md"), str(home / "draft.md"),
        )
    check(code == 0, f"the verify run must exit 0, got {code}")
    check("## Structure" not in out,
          "a verify run declared nothing, so there is nothing to reconcile it against")


def test_the_budget_stops_a_merge_declaring_its_way_to_a_clean_exit() -> None:
    """The declared-loss budget as the ceiling on the findings-versus-queue split, which is the only thing holding the queue up.

    Every drop here is declared, confirmed and individually reasonable, and
    without the budget that is exit 0 for any number of them — the queue would
    be a way of moving losses out of the exit code by describing them. Two of 24
    segments is 8.3%, over the 5% ceiling, so the volume is the finding.

    The verdict line is asserted because this is the one exit 1 with an empty
    *claim* findings list, and "0 finding(s)" over a failing run would be the
    report disagreeing with the command that printed it. The breach is also
    the reconciler's check 6, so the headline counts one
    structural finding and names it; the two are the same breach, computed once
    by `reconcile.over_budget` and reported by whichever section a reader
    reaches first.
    """
    with workspace(long_script(dropped("a3", "a4"), (
        ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
        ("A-002", "MISSING", "", ""),
        ("A-003", "MISSING", "", ""),
        ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
    ), a_claims=(
        ("The connect timeout is 30 seconds.", 2),
        ("The archive rotates every 7 days", 3),
        ("The queue drains at 200 messages per second.", 4),
    ))) as (home, base_url):
        code, out, data = long_merge(home, base_url)

    check(code == 1, f"declared loss over budget must fail the run; got {code}")
    check(data["findings"] == [],
          f"the budget is not a per-claim finding; got {data['findings']}")
    check([v["claim_id"] for v in data["review_queue"]] == ["A-002", "A-003"],
          f"the claims are still queued and still reported; got "
          f"{[v['claim_id'] for v in data['review_queue']]}")
    check(data["declared_loss"] == {"drops": 2, "segments": LONG_SEGMENTS, "budget": 0.03,
                                    "check_disabled": False, "over_budget": True,
                                    "ratio": 2 / LONG_SEGMENTS},
          f"two drops of {LONG_SEGMENTS} is over the budget; got "
          f"{data['declared_loss']}")
    check("**1 finding(s).** In the structure: 1 declared loss over budget." in out,
          f"the verdict must name the breach rather than count zero findings; "
          f"got {[line for line in out.splitlines() if line.startswith('**')]}")
    check("0 finding(s)" not in out,
          "a failing run must not headline a finding count of zero")
    check("In the claims:" not in out,
          "no claim was lost to a finding here, so the verdict must not open a "
          "claims breakdown with nothing in it")
    check([f["kind"] for f in data["structural"]["findings"]] == ["declared_loss_over_budget"],
          f"the breach is the reconciler's check 6 and the only one that fired; "
          f"got {data['structural']['findings']}")
    check("**2** drop(s) of 24 source segment(s)" in out,
          f"the breach must print both halves of its ratio; got "
          f"{[line for line in out.splitlines() if 'drop(s)' in line]}")
    check("not charged" not in out.split("## Coverage")[0],
          "the verdict must not say the losses are not charged in the paragraph "
          "explaining why the run failed on them")


def test_a_confirmed_supersede_is_a_finding_and_not_queued() -> None:
    """The queue takes omissions and never assertions. That was the actual decision.

    `superseded` is the other disposition that can produce a finding, and it is
    the one a wider rule would have swept into the queue: the merge declared the
    swap, the forward pass confirmed the declaration, and by the reasoning that
    queues a declared drop this claim is "accounted for" too. It is not. A drop
    leaves the merge silent about a fact and a reader can put it back; a
    supersede leaves the merge *asserting* something a source denies, and a
    reader who trusts the merged document is misinformed no matter how well the
    swap was announced. Announcing a contradiction does not make it safe to act
    on, so CONTRADICTED stays a finding and stays in the exit code.
    """
    replacement = "The archive rotates every 14 days.\n"
    with workspace(long_script(
        [{
            "segment": "a3",
            "disposition": "superseded",
            "replacement": replacement.strip(),
            "reason": "the newer rotation period replaces the older one.",
        }],
        (
            ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
            ("A-002", "CONTRADICTED", replacement.strip(), "merged.md"),
            ("A-003", "SUPPORTED", replacement.strip(), "merged.md"),
            ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
        ),
        merged=LONG_MERGED + replacement,
    )) as (home, base_url):
        code, out, data = long_merge(home, base_url)

    check([(d["segment"], d["grade"]) for d in data["declarations"]]
          == [("a3", "confirmed")],
          f"the supersede must be confirmed, or this test proves nothing about "
          f"confirmed supersedes; got {data['declarations']}")
    check(code == 1, f"a confirmed supersede that contradicts a source is a "
                     f"finding; got {code}")
    check([v["claim_id"] for v in data["findings"]] == ["A-002"],
          f"the contradicted claim stays a finding; got "
          f"{[v['claim_id'] for v in data['findings']]}")
    check(data["review_queue"] == [],
          f"only drops are queued; got {data['review_queue']}")
    check(data["declared_loss"]["drops"] == 0,
          f"a supersede is not a declared drop and must not be budgeted as one; "
          f"got {data['declared_loss']}")
    check("### Contradicted" in out,
          "the contradiction must be reported under Findings")


def test_a_drop_declared_as_something_else_is_not_laundered_into_the_queue() -> None:
    """The route out of both the exit code and the budget, closed.

    `subsumed` is permitted at `high` and is not counted by the declared-loss budget: the scope
    note in the brief excludes it on purpose, because compression is what high
    fidelity is for. So a merger that wants a loss to cost nothing has an
    obvious move: drop the segment and call it `subsumed`. The forward pass
    catches it — MISSING is not what `subsumed` predicts, so the declaration is
    rejected — and the claim has to stay a finding, or declaring the wrong
    disposition would be strictly better than declaring the right one.

    This is the case that makes both filters in `accounted_for` load-bearing at
    once. Neither is sufficient alone here and neither is testable alone: the
    disposition filter is what stops a rejected `subsumed` and the grade filter
    is what stops it under any other name.
    """
    with workspace(long_script(
        [{
            "segment": "a3",
            "disposition": "subsumed",
            "replacement": "The relay listens on port 8443.",
            "reason": "the rotation detail is covered by the summary line.",
        }],
        (
            ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
            ("A-002", "MISSING", "", ""),
            ("A-003", "MISSING", "", ""),
            ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
        ),
    )) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge",
            str(home / "long-a.md"), str(home / "long-b.md"),
            "--fidelity", "high",
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    check([(d["segment"], d["grade"]) for d in data["declarations"]]
          == [("a3", "rejected")],
          f"a subsumed segment whose claims are missing must be rejected; got "
          f"{data['declarations']}")
    check(code == 1, f"a drop declared as a subsume is still a drop; got {code}")
    check([v["claim_id"] for v in data["findings"]] == ["A-002", "A-003"],
          f"both losses stay findings; got "
          f"{[v['claim_id'] for v in data['findings']]}")
    check(data["review_queue"] == [],
          f"only a confirmed drop earns a queue entry; got {data['review_queue']}")
    check(data["declared_loss"]["drops"] == 0,
          f"the declared-loss budget counts `dropped` and this record did not say dropped; got "
          f"{data['declared_loss']}")
    check("### Dropped" in out, "the losses must be reported as dropped claims")


def test_a_verify_run_has_no_review_queue() -> None:
    """Nothing declared anything to a `verify` run, so it owns no queue.

    The same reason `declarations_section` is gated on the command: an empty
    queue printed here would read as this tool having examined someone else's
    merge for declared drops and found none, when it was never told what that
    merge intended. The declared-loss budget's denominator is 0 for the same reason, and a budget
    with no numerator must not print as a ratio anybody measured.
    """
    with workspace(Script(**CLEAN), merged_on_disk=True) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "verify",
            str(home / "notes-a.md"), str(home / "notes-b.md"), str(home / "draft.md"),
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    check(code == 0, f"the verify run must exit 0, got {code}")
    check("## Review queue" not in out,
          "a verify run has no declarations and therefore no queue to print")
    check(data["review_queue"] == [] and data["declared_loss"]["segments"] == 0,
          f"a verify run declares nothing and segments nothing; got "
          f"{data['review_queue']} and {data['declared_loss']}")
    check(data["declared_loss"]["over_budget"] is False,
          "a zero denominator is not a breach")


def test_the_report_names_the_base_and_says_whether_anyone_chose_it() -> None:
    """The header prints two rules whose operand is the base, so it prints that too.

    `Title policy: keep-base` names which title survives without naming the
    document it survives from, and under every policy the base decides the
    merged structure. `base_chosen` rides with it because the default is
    `names[0]`, which is *alphabetically* first: with nothing said, the document
    governing the merge is decided by what the files happened to be called. That
    is defensible recorded and indefensible unrecorded.

    Asserted on the rendered markdown and on the dict, not on `MergeResult`. A
    dataclass carrying a field that nothing prints is the failure this is about.
    """
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--base", str(home / "notes-b.md"),
            "--json", str(home / "report.json"),
        )
        check(code == 0, f"the clean merge must exit 0, got {code}")
        check("| Base document | `source_b.md` (explicit) |" in out,
              "a merge report must name the base and say it was chosen")
        policy = json.loads((home / "report.json").read_text())["provenance"]["merge_policy"]
        check(policy == {"fidelity": config.DEFAULT_FIDELITY,
                         "verify_depth": config.DEFAULT_VERIFY_DEPTH,
                         "title_policy": config.DEFAULT_TITLE_POLICY,
                         "base": "source_b.md", "base_chosen": "explicit"},
              f"the base belongs in merge_policy beside its three rules, got {policy}")

    # The case the command line cannot reach and the record exists for.
    with workspace(Script(**CLEAN)) as (home, base_url):
        markdown, data = merge_with_no_base(home, base_url)
    check("| Base document | `source_a.md` (defaulted) |" in markdown,
          f"an unnamed base must be named and marked defaulted, got:\n{markdown}")
    policy = data["provenance"]["merge_policy"]
    check(policy["base"] == "source_a.md" and policy["base_chosen"] == "defaulted",
          f"the dict must say the same as the markdown, got {policy}")

    # And a verify run, which made no merge and so has no base to name. The row
    # stays and says so: dropping it would read as an omission rather than a fact.
    with workspace(Script(**CLEAN), merged_on_disk=True) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "verify", str(home / "notes-a.md"),
            str(home / "notes-b.md"), str(home / "draft.md"),
        )
        check("| Base document | none — this run made no merge |" in out,
              f"a verify report must say it has no base, got:\n{out}")


def test_the_corpus_flags_are_not_on_the_installed_command() -> None:
    """--record, --replay and --offline build this repository's own corpus.

    They are not conveniences a user of the tool is missing; they are the
    machinery for recording `tests/responses/`, and their failure modes -- a
    half-recorded corpus, a mixed-revision one -- are diagnosable only from
    inside the repository.
    """
    for flag in ("--record", "--replay", "--offline", "--force", "--mixed-sources"):
        parse_fails(["merge", "a.md", "b.md", "--base", "a.md", flag, "x"],
                    f"{flag} must not be on the installed command")
    for flag in ("--dry-run", "--no-cache"):
        cli.build_parser().parse_args(["merge", "a.md", "b.md", "--base", "a.md", flag])


def test_output_on_verify_is_an_error_with_a_reason() -> None:
    """Silently not producing a document is the failure this project is about."""
    script = Script(**CLEAN)
    with workspace(script, merged_on_disk=True) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "verify",
            str(home / "notes-a.md"), str(home / "notes-b.md"), str(home / "draft.md"),
            "-o", str(home / "never.md"),
        )
    check(code == 2, f"verify -o must exit 2, got {code}")
    check("does not produce a merged document" in err,
          f"verify -o must say why, got {err!r}")
    check(not (home / "never.md").exists(), "verify -o must not create the file")
    check(script.bodies == [], "verify -o must be refused before any call is made")


# --------------------------------------------------------------------------
# the clean run
# --------------------------------------------------------------------------


def test_a_clean_merge_exits_zero_and_reports_its_denominator_first() -> None:
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )

    check(code == 0, f"a clean merge must exit 0, got {code} (stderr: {err!r})")
    for heading in ("## Verdict", "## Coverage", "## Findings", "## Provenance"):
        check(heading in out, f"the report must have a {heading} section")
    check(out.index("## Coverage") < out.index("## Findings"),
          "coverage must be printed before the findings, not after")
    check(out.index("## Verdict") < out.index("## Coverage"),
          "the verdict line must come first")
    check("No extracted claim was dropped, contradicted, invented, or carried "
          "only in part." in out,
          f"a clean run must say so in words, got {out[:200]!r}")
    # The unscoped sentence was printed over a concatenation that had dropped
    # both titles, so the scope travels with the claim or the headline goes
    # back to being broader than the measurement behind it. On a `merge` run
    # the reconciler now covers what the claims do not, and the sentence says
    # which checks did it and over how many segments, the same rule pointing
    # the other way, since a caveat about titles over a run that did check
    # the titles understates it by exactly as much.
    check("mechanical checks under Structure below cover what the claims do not" in out,
          "the clean verdict must say which question it answered")
    check("4 source segment(s) — including the ones no claim was drawn from" in out,
          "the clean verdict must carry the reconciler's denominator, not just its result")
    check("titles, headings and formatting are not claims and were not checked" not in out,
          "the pre-task-36 caveat is false on a run the reconciler examined")
    check("2 source claim(s) checked against the merge" in out,
          "the clean verdict must state how much was checked")
    check(script.seen == ["merge", "decompose", "decompose", "forward", "decompose", "reverse"],
          f"the pipeline order changed: {script.seen}")


def test_the_fidelity_level_is_off_by_default_and_on_every_report() -> None:
    """A coverage number is not interpretable without the level.

    At `off` a rewording is a defect; at `high` it is the requested behaviour.
    The same figure therefore means different things at different levels, which
    puts the level in the provenance block for the same reason the model id is
    there — including on `verify` runs, which make no merge call but whose
    reverse pass will read the level too.
    """
    parser = cli.build_parser()
    flags = {action.dest: action for action in parser._subparsers._group_actions[0]
             .choices["merge"]._actions}
    check("fidelity" in flags, "--fidelity must be on the installed command")
    # One spelling per level plus one alias: the published names in wire
    # order, then `off`, which is `verbatim`'s older name and keeps working.
    check(tuple(flags["fidelity"].choices)
          == ("verbatim", "low", "mid", "high", "open", "sourced", "off"),
          f"the level names are fixed and `off` still names the first: "
          f"{flags['fidelity'].choices}")
    check(flags["fidelity"].default is None,
          "the flag must default to None so the env var can still be seen")
    parse_fails(["merge", "a.md", "b.md", "--base", "a.md", "--fidelity", "medium"],
                "an invented level must be rejected by the parser")

    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )
    check(code == 0, f"the default run must still be clean, got {code}")
    check(f"| Fidelity | {config.DEFAULT_FIDELITY} |" in out,
          f"an unflagged run must report the default level, got {out[:600]!r}")

    for level in ("low", "mid", "high"):
        script = Script(**CLEAN)
        with workspace(script) as (home, base_url):
            _, out, _ = invoke(
                home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md"),
                "--fidelity", level,
            )
        check(f"| Fidelity | {level} |" in out, f"--fidelity {level} must reach the report")

    # And on verify, which never calls merge. The level is a verification
    # parameter too, so a report that omitted it there would be the one place
    # a reader could not tell which question was answered.
    script = Script(**CLEAN)
    with workspace(script, merged_on_disk=True) as (home, base_url):
        _, out, _ = invoke(
            home, base_url, "verify", str(home / "notes-a.md"), str(home / "notes-b.md"),
            str(home / "draft.md"), "--fidelity", "high",
        )
    check("| Fidelity | high |" in out, "a verify run must report the level as well")


def test_the_title_policy_defaults_from_the_constant_and_is_on_every_report() -> None:
    """The second half of the merge policy, printed beside the first.

    A report that named the fidelity level and not the title policy would be the
    more dangerous of the two omissions, because `choose-best` produces a heading
    neither source states verbatim — the one line of a `high` merge that can look
    like invention while being exactly what was asked for.
    """
    parser = cli.build_parser()
    flags = {action.dest: action for action in parser._subparsers._group_actions[0]
             .choices["merge"]._actions}
    check("title_policy" in flags, "--title-policy must be on the installed command")
    check(tuple(flags["title_policy"].choices) == config.TITLE_POLICIES,
          f"the two policies are fixed: {flags['title_policy'].choices}")
    check(flags["title_policy"].default is None,
          "the flag must default to None so the env var can still be seen")
    parse_fails(["merge", "a.md", "b.md", "--base", "a.md", "--title-policy", "keep-longest"],
                "an invented policy must be rejected by the parser")

    # **The help describes the default it names**. It read "default
    # synthesise: the base document's" -- the name interpolated from the
    # constant, the description left behind from when `keep-base` was the
    # default -- and the one policy that may write a title was not described at
    # all. Every clause is read out of `TITLE_POLICY_EXPLAINS` rather than
    # written here, so this fails when the help stops being built from it and
    # not when somebody rewords a clause.
    said = " ".join(flags["title_policy"].help.split())
    check(f"default {config.DEFAULT_TITLE_POLICY}: "
          f"{config.TITLE_POLICY_EXPLAINS[config.DEFAULT_TITLE_POLICY]}" in said,
          f"--title-policy's help must describe the default it names; "
          f"got {said!r}")
    for value in config.TITLE_POLICIES:
        check(config.TITLE_POLICY_EXPLAINS[value] in said,
              f"--title-policy's help does not describe {value!r}; a policy an "
              f"operator can pass is one the flag has to explain")

    # Seeded with the shape that shipped: the default's name, another policy's
    # description. The wrong policy is picked off the tuple rather than written
    # here, so the probe survives the default moving again.
    other = next(value for value in config.TITLE_POLICIES
                 if value != config.DEFAULT_TITLE_POLICY)
    stale = (f"which title the merged document takes (default "
             f"{config.DEFAULT_TITLE_POLICY}: "
             f"{config.TITLE_POLICY_EXPLAINS[other]})")
    check(f"default {config.DEFAULT_TITLE_POLICY}: "
          f"{config.TITLE_POLICY_EXPLAINS[config.DEFAULT_TITLE_POLICY]}"
          not in stale,
          "seeded check: a help naming the default and describing another "
          "policy was accepted; this assertion no longer reads the clause")

    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )
    check(code == 0, f"the default run must still be clean, got {code}")
    # Read from the constant rather than written as a literal: the default moved
    # once (an earlier title-policy decision and the untitled-sources fix behind it) and every literal
    # copy of it was a second edit. `test_merge.py` pins the value in one place.
    check(f"| Title policy | {config.DEFAULT_TITLE_POLICY} |" in out,
          f"an unflagged run must report {config.DEFAULT_TITLE_POLICY}, "
          f"got {out[:600]!r}")

    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        _, out, _ = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--title-policy", "choose-best",
        )
    check("| Title policy | choose-best |" in out,
          "--title-policy choose-best must reach the report")

    # Both flags at once, because the failure worth catching is one field of the
    # policy travelling and the other silently defaulting.
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        _, out, _ = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--fidelity", "high", "--title-policy", "choose-best",
        )
    check("| Fidelity | high |" in out and "| Title policy | choose-best |" in out,
          f"both halves of the policy must reach one report, got {out[:800]!r}")


def test_the_model_is_shown_the_canonical_filenames() -> None:
    """Every published figure was measured with source_a.md in the prompt.

    Rendering the caller's filename instead would make each run a configuration
    nothing was measured under, so the mapping is one-way: the prompt keeps the
    canonical name, and the report shows a short name scanned from the caller's
    own path, not the canonical name and not the full path.
    """
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )

    sent = "\n".join(body["messages"][0]["content"] for body in script.bodies)
    check("source_a.md" in sent and "source_b.md" in sent,
          "the prompts must name source_a.md and source_b.md")
    check("notes-a.md" not in sent,
          "the caller's filename must not reach the prompt; the figures were not measured with it")
    check("notes-a.md" in out and "notes-b.md" in out,
          f"the report must show the caller's filenames, got {out[:400]!r}")
    check(str(home / "notes-a.md") not in out,
          f"the report must not print the caller's full path, got {out[:400]!r}")


def test_a_shared_basename_is_still_told_apart() -> None:
    """`run.display` shortens to a basename, and two sources can share one.

    `a/notes.md` and `b/notes.md` would both print as `notes.md`, a collision
    that would make two coverage rows read the same, so a name that collides
    with another document in the run keeps one directory of disambiguation
    instead.
    """
    run = report.Run(
        command="merge",
        paths={"source_a.md": "a/notes.md", "source_b.md": "b/notes.md"},
    )
    check(run.display("source_a.md") == "a/notes.md",
          f"a colliding basename must be disambiguated, got {run.display('source_a.md')!r}")
    check(run.display("source_b.md") == "b/notes.md",
          f"a colliding basename must be disambiguated, got {run.display('source_b.md')!r}")

    run = report.Run(
        command="merge",
        paths={"source_a.md": "a/notes-a.md", "source_b.md": "b/notes-b.md"},
    )
    check(run.display("source_a.md") == "notes-a.md",
          f"a basename with no collision must not carry a directory, got "
          f"{run.display('source_a.md')!r}")
    check(run.display("source_b.md") == "notes-b.md",
          f"a basename with no collision must not carry a directory, got "
          f"{run.display('source_b.md')!r}")


def test_the_merged_document_goes_where_the_caller_said() -> None:
    """-o writes it; without -o it is embedded. Never both, never neither."""
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"), "-o", str(home / "out.md"),
        )
        written = (home / "out.md").read_text(encoding="utf-8")
    check(written == MERGED, "-o must write the merged document byte for byte")
    check("## Merged document" not in out,
          "with -o the report must not also embed the document")

    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        _, out, _ = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )
    check("## Merged document" in out and MERGED.strip() in out,
          "without -o the merged document must be embedded, so nothing is lost")


def test_verify_makes_no_merge_call() -> None:
    """The cheaper command, and the claim the README makes about it."""
    script = Script(**CLEAN)
    with workspace(script, merged_on_disk=True) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "verify",
            str(home / "notes-a.md"), str(home / "notes-b.md"), str(home / "draft.md"),
        )
    check(code == 0, f"a clean verify must exit 0, got {code} (stderr: {err!r})")
    check("merge" not in script.seen, f"verify must make no merge call, made {script.seen}")
    check("## Merged document" not in out,
          "verify produced no document, so it must not print one")
    check("draft.md" in out and str(home / "draft.md") not in out,
          f"verify must show a short name for the merged document, not the "
          f"full path, got {out[:400]!r}")


# --------------------------------------------------------------------------
# findings and exit codes
# --------------------------------------------------------------------------


def test_a_dropped_claim_exits_one_and_is_named() -> None:
    script = Script(
        **{
            **CLEAN,
            "forward": verdicts(
                ("A-001", "MISSING", "", ""),
                ("B-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
            ),
        }
    )
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )
    check(code == 1, f"a dropped claim must exit 1, got {code} (stderr: {err!r})")
    check("1 finding(s)" in out and "1 dropped" in out, f"the verdict must count it: {out[:300]!r}")
    check("Dropped — in a source, not in the merge" in out,
          "the finding must be filed under the right heading")
    check("**A-001**" in out and "notes-a.md:1" in out,
          f"the finding must name the claim and the caller's file: {out!r}")


def test_an_invented_claim_is_reported_as_invented_not_missing() -> None:
    """Same label, opposite direction, different failure. FINDINGS decides."""
    script = Script(
        **{**CLEAN, "reverse": verdicts(("M-001", "MISSING", "", ""))}
    )
    with workspace(script) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )
    check(code == 1, f"an invented claim must exit 1, got {code}")
    check("Invented — in the merge, in neither source" in out,
          f"a reverse MISSING is invention, not a drop: {out!r}")
    check("Dropped —" not in out, "nothing was dropped; the report must not say so")


def test_a_partial_is_neither_a_drop_nor_a_pass() -> None:
    """The verdict that had nowhere to go before it existed.

    Both places it could have been folded into are wrong, and this asserts it
    landed in neither. Folded into MISSING it would print under "Dropped" and
    count a fact carried with one detail missing as a fact that did not survive.
    Folded into SUPPORTED it would print nothing at all, exit 0, and the run
    would say every claim was accounted for — which is how a merge that adds one
    detail to a real fact gets past a tool built to catch exactly that.

    The coverage row is the third thing: the forward ratio counts fully
    accounted-for claims, so a partial is missing from its numerator, and
    without a row of its own the table would read as a whole claim lost.
    """
    script = Script(
        **{
            **CLEAN,
            "forward": verdicts(
                ("A-001", "PARTIAL", "The relay listens on port 8443.", "merged.md"),
                ("B-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
            ),
        }
    )
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    check(code == 1, f"a partial claim must exit 1, got {code} (stderr: {err!r})")
    check("1 finding(s)" in out and "1 partially dropped" in out,
          f"the verdict must count it under its own name: {out[:400]!r}")
    check("Partly dropped — the merge carries some of this claim" in out,
          f"a partial needs its own heading: {out!r}")
    check("Dropped — in a source, not in the merge" not in out,
          "a partial is not a drop and must not be filed as one")
    check("| Forward — carried only in part | 1 |" in out,
          f"the coverage table must show the partial on its own row: {out!r}")
    check("| Forward — source claims accounted for in the merge | **1/2** |" in out,
          f"a partial is not accounted for either, so it leaves the numerator: {out!r}")
    check("| Reverse — supported only in part | 0 |" in out,
          f"the other direction's row is printed at zero rather than omitted: {out!r}")
    check(data["coverage"]["forward_partial"] == 1
          and data["coverage"]["reverse_partial"] == 0,
          f"the machine-readable coverage must carry it too, got {data['coverage']}")
    check([f["finding"] for f in data["findings"]] == ["partially_dropped"],
          f"the JSON finding keeps the direction in its name, got {data['findings']}")


def test_a_partial_on_the_reverse_pass_is_partly_invented() -> None:
    """Same label, opposite direction, and the quieter of the two.

    A merge claim the sources support in part is a detail the merge added to a
    real fact, which reads far more plausibly than a wholly invented sentence
    and is the case `prompts/verify_reverse.md` warns about in those words.
    """
    script = Script(
        **{
            **CLEAN,
            "reverse": verdicts(
                ("M-001", "PARTIAL", "The relay listens on port 8443.", "source_a.md")
            ),
        }
    )
    with workspace(script) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )
    check(code == 1, f"a partly invented claim must exit 1, got {code}")
    check("Partly invented — the sources carry some of this claim" in out,
          f"a reverse PARTIAL is an addition, not a loss: {out!r}")
    check("Partly dropped" not in out,
          "nothing was partly dropped; the report must not say so")
    check("| Reverse — supported only in part | 1 |" in out,
          f"the reverse coverage row must carry it: {out!r}")


def test_a_source_dropped_whole_is_visible_beside_the_pooled_ratio() -> None:
    """The pooled forward ratio cannot tell two failures apart.

    Two sources of two claims each. One is carried whole, the other is dropped
    whole, and the pooled row reads `2/4` — the identical figure a merge that
    lost one claim from each source would print. The first is a document the
    merge ignored and the second is ordinary attrition, and they want different
    responses from whoever reads the report.

    The per-source rows are what separate them, and each is counted against its
    own claims rather than against the run's. Nothing here changes the exit
    code: every dropped claim is already a finding, and a source at 0/2 is those
    findings arranged so the shape is visible, not a second charge for them.
    """
    script = Script(
        **{
            **CLEAN,
            "decompose": lambda n: claims(
                ("The relay listens on port 8443.", 1),
                ("The connect timeout is 30 seconds.", 2),
            )
            if n < 3
            else claims(("The relay listens on port 8443.", 1)),
            "forward": verdicts(
                ("A-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
                ("A-002", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
                ("B-001", "MISSING", "", ""),
                ("B-002", "MISSING", "", ""),
            ),
        }
    )
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    check(code == 1, f"two dropped claims must exit 1, got {code} (stderr: {err!r})")
    check("| Forward — source claims accounted for in the merge | **2/4** |" in out,
          f"the pooled row must still be printed, and first: {out!r}")
    check("| Forward — `notes-a.md` claims accounted for | **2/2** |" in out,
          f"the carried source must show its own denominator: {out!r}")
    check("| Forward — `notes-b.md` claims accounted for | **0/2** |" in out,
          f"the dropped source must show 0 against its own claims, not vanish "
          f"into the pooled average: {out!r}")
    check(out.index("accounted for in the merge")
          < out.index("`notes-a.md` claims accounted for"),
          "the pooled row comes before the per-source rows it is the sum of")

    by_source = data["coverage"]["forward_by_source"]
    check(sorted(by_source) == ["source_a.md", "source_b.md"],
          f"the JSON must key per-source coverage by canonical name, got {by_source}")
    check(by_source["source_a.md"] == {"extracted": 2, "checked": 2,
                                       "accounted": 2, "partial": 0},
          f"source_a: {by_source.get('source_a.md')}")
    check(by_source["source_b.md"] == {"extracted": 2, "checked": 2,
                                       "accounted": 0, "partial": 0},
          f"source_b: {by_source.get('source_b.md')}")
    check(sum(row["checked"] for row in by_source.values())
          == data["coverage"]["forward_verdicts"],
          "the per-source denominators must sum to the pooled one, or one of the "
          "two tables is counting something the other is not")


def test_per_source_coverage_names_the_cases_a_ratio_cannot() -> None:
    """The two rows that are not ratios, asserted where they can be constructed.

    A source decompose found nothing in has no denominator, and `0/0` is the one
    thing it must not print. A forward verdict belonging to no source cannot
    happen through the pipeline — claim ids carry their document's letter — but
    if it ever did, the per-source rows would sum to less than the pooled row
    with nothing in the report saying so, so it is printed instead of dropped.
    """
    run = report.Run(command="merge",
                     paths={"source_a.md": "notes-a.md", "source_b.md": "notes-b.md"})
    run.claims = {
        "source_a.md": [Claim("A-001", "source_a.md", "x", 1, "x", True)],
        "source_b.md": [],
    }
    run.forward = [
        Verdict("A-001", "SUPPORTED", "x", "merged.md", "r", "source_to_merged", "grounded"),
        Verdict("Z-009", "SUPPORTED", "x", "merged.md", "r", "source_to_merged", "grounded"),
    ]
    rendered = report.coverage_section(run)
    check("0/0" not in rendered, f"a source with no claims printed a ratio: {rendered!r}")
    check("| Forward — `notes-b.md` claims accounted for | no claims extracted — "
          "nothing to check |" in rendered,
          f"a source nothing was extracted from must say so: {rendered!r}")
    check("| Forward — claims matching no source | 1 |" in rendered,
          f"a verdict belonging to no source must be printed: {rendered!r}")

    del run.forward[1]
    rendered = report.coverage_section(run)
    check("matching no source" not in rendered,
          f"the row must not be printed at zero; it is an invariant, not a "
          f"measurement: {rendered!r}")


def test_an_errored_unit_exits_two_whatever_the_rest_said() -> None:
    """2 supersedes 1, and a check that examined nothing does not pass.

    The forward pass here is unanswerable, so the run has one clean reverse
    direction and no forward coverage at all. Exiting 1 would report the
    findings it happened to find; exiting 0 would be worse. It exits 2 and the
    coverage row says the pass was not checked rather than printing 0/0.
    """
    script = Script(**{**CLEAN, "forward": None})
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )
    check(code == 2, f"an errored unit must exit 2, got {code} (stderr: {err!r})")
    check("Inconclusive." in out, f"the verdict must say so: {out[:300]!r}")
    check("verify (forward)" in out, "the verdict must name the unit that errored")
    check("0/0" not in out, f"a zero denominator must not be printed as a ratio: {out!r}")
    check("not checked (2 claim(s) extracted)" in out,
          f"coverage must say what went unexamined: {out!r}")
    check("unit(s) of work errored" in out,
          "the provenance block must carry the inconclusive warning")


def test_a_fatal_fault_on_the_last_call_still_reports_what_finished() -> None:
    """A FATAL fault must not throw away a finished report.

    `verify (reverse)` is the pipeline's last unit of work on a merge run --
    merge, reconcile, decompose x2, verify forward, decompose merged, verify
    reverse -- and everything before it succeeds here. Every attempt at the
    reverse call gets a 503, so `transport.py` retries to `MAX_ATTEMPTS` and
    raises `TransportError`, which is FATAL: the run aborts rather than
    erroring one unit. The six units of real work already on `run` -- a
    finished merge among them -- must still reach the report, not be
    discarded for one red line.
    """
    inner = Script(**CLEAN)

    def flaky(body: dict, n: int):
        kind = inner.kind(body["messages"][0]["content"])
        if kind == "reverse":
            return 503, json.dumps({"error": "unavailable"}), {"Retry-After": "0"}
        return inner(body, n)

    with workspace(flaky) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )
    check(code == 2, f"a run that could not finish must exit 2, got {code} (stderr: {err!r})")
    check("Inconclusive." in out, f"the verdict must say so: {out[:300]!r}")
    check("verify (reverse)" in out, "the report must name the unit that errored")
    check("## Merged document" in out and MERGED.strip() in out,
          f"the merge that did complete must still reach the report, not be "
          f"discarded for the later fault: {out[:400]!r}")
    check("Claims extracted from" in out,
          f"the decomposes that did complete must still reach the report: {out[:400]!r}")
    check("error:" not in out,
          f"the fault belongs to the report and the summary, not to stdout as "
          f"a bare refusal: {out[:200]!r}")
    check("did not finish" in err,
          f"the fault must still reach the summary on stderr: {err!r}")


def test_two_supersedes_one_when_both_are_true() -> None:
    script = Script(
        **{
            **CLEAN,
            "forward": verdicts(
                ("A-001", "MISSING", "", ""),
                ("B-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
            ),
            "reverse": None,
        }
    )
    with workspace(script) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md")
        )
    check(code == 2, f"a finding plus an errored unit must exit 2, got {code}")
    check("Inconclusive." in out,
          "the verdict line must match the exit code, not the findings it did make")


def test_the_exit_code_and_the_report_are_computed_from_one_object() -> None:
    """The third principle, applied to the number the shell sees.

    An exit code derived in `main` and a verdict line derived in `report` are
    two implementations of one rule, and the failure mode is a report that says
    clean over a code of 1. Both come from `report.exit_code`.

    The pin used to be the literal return statement. It is the call now, because
    the number has three readers rather than one -- the shell, the verdict
    colour, and the end-of-run summary on stderr -- and pinning the return line
    would have said nothing about the other two. Counting the call covers all of
    them: one derivation, however many things read it.
    """
    source = (ROOT / "src" / "llossless" / "cli.py").read_text(encoding="utf-8")
    check(source.count("exit_code(run)") == 1,
          "cli.py must derive the exit code from report.exit_code exactly once")
    check("code = 0 if run.planned else exit_code(run)" in source,
          "the one derivation must be the one main returns")
    check("if run.errored" not in source,
          "cli.py must not decide inconclusiveness a second time; report.exit_code owns it")

    run = report.Run(command="merge")
    check(report.exit_code(run) == 0, "an empty run is clean")
    run.steps.append(report.Step("verify (forward)", report.ERRORED, "boom"))
    check(report.exit_code(run) == 2, "an errored step is inconclusive")


def test_a_record_fault_and_a_document_fault_get_different_exit_codes() -> None:
    """The A2 inversion: 1 is the document, 3 is only the record.

    The pair that forced this: on `universe`, `off` declared 23 dispositions,
    got every one right, and exited 0 with a document matching 6 of 23
    sentences of the operator's key, while the three levels that matched 23 of
    23 exited 1 on `false_departure` findings. The exit code ranked the 26%
    document above the 100% ones because a finding was a finding.

    Built from `Finding` objects directly rather than from a merge, because
    what is under test is the mapping from kind to code, and a merge that
    produced one of each kind would be a fixture with two variables in it.
    """
    def coded(*kinds: str) -> int:
        run = report.Run(command="merge")
        run.reconciled = reconcile.Reconciled(
            findings=tuple(reconcile.Finding(kind, "detail") for kind in kinds),
            declared_drops=(),
            segments=10,
        )
        return report.exit_code(run)

    check(coded() == 0, "no findings is still clean")
    check(coded(reconcile.FALSE_DEPARTURE) == report.RECORD_ONLY,
          "a merge that mis-declared work it did correctly is a record fault")
    check(coded(reconcile.UNDECLARED_ABSENCE) == 1,
          "content missing with no record is a document fault")
    check(coded(reconcile.DUPLICATED_CONTENT) == 1,
          "the check 9 defect the operator reported is a document fault")
    # Both at once is the document's code. A reader who has to pick one thing
    # to fix picks the one in the document they are about to ship.
    check(coded(reconcile.FALSE_DEPARTURE, reconcile.UNDECLARED_ABSENCE) == 1,
          "a document fault outranks a record fault in the same run")
    # And 3 is a failure, not a pass. This is the whole guard: a
    # merge cannot declare its way to 0, it can only declare its way to 3.
    check(report.RECORD_ONLY != 0,
          "the record-only code must be non-zero or declaring becomes free")

    # Every kind is reachable from one of the two, asserted over the vocabulary
    # rather than over the three examples above -- a kind added to
    # `FINDING_KINDS` and to neither family is the one silent failure here.
    for kind in reconcile.FINDING_KINDS:
        check(coded(kind) in (1, report.RECORD_ONLY),
              f"{kind} reaches neither exit code; it is filed in no family")


# --------------------------------------------------------------------------
# dry run, JSON, and the ways a run does not start
# --------------------------------------------------------------------------


def test_dry_run_sends_nothing_and_counts_what_it_can() -> None:
    """It must not invent the calls it cannot count.

    The verify calls depend on how many claims come back, which is what the
    decompose calls it did not make were going to establish. So the plan states
    three and names the rest as uncountable rather than estimating.
    """
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"), "--dry-run",
        )
    check(code == 0, f"--dry-run must exit 0, got {code} (stderr: {err!r})")
    check(script.bodies == [], f"--dry-run must make no request, made {len(script.bodies)}")
    check("3 call(s) planned, none made." in out, f"the plan must be counted: {out!r}")
    check("## Verdict" not in out,
          "a dry run graded nothing and must not print a verdict over it")
    check("| Run mode | dry-run |" in out,
          f"the provenance block must not call a dry run live: {out!r}")


def test_a_dry_run_says_it_is_a_dry_run_not_a_clean_verdict() -> None:
    """A dry run makes no call, so its terminal summary must not read as
    a verdict on the documents.

    It used to end "Done. Nothing your documents state was dropped or
    contradicted." -- the same words a real clean merge ends with -- even
    though nothing was checked, on both `merge --dry-run` and `verify
    --dry-run`. The new wording states the plan's own count instead, the one
    `## Planned calls` already prints, so the terminal and the report cannot
    disagree about it.
    """
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"), "--dry-run",
        )
    check(code == 0, f"merge --dry-run must exit 0, got {code}")
    check("3 call(s) planned, none made." in out,
          f"the report's own plan count must still be printed: {out!r}")
    check("Dry run: 3 call(s) planned, none made. Nothing was checked." in err,
          f"the terminal summary must state the plan, not a verdict: {err!r}")
    check("dropped or contradicted" not in err,
          f"a dry run checked nothing, so its summary must not read like a "
          f"clean merge's: {err!r}")

    script = Script(**CLEAN)
    with workspace(script, merged_on_disk=True) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "verify",
            str(home / "notes-a.md"), str(home / "notes-b.md"), str(home / "draft.md"),
            "--dry-run",
        )
    check(code == 0, f"verify --dry-run must exit 0, got {code}")
    check("Dry run: 3 call(s) planned, none made. Nothing was checked." in err,
          f"verify --dry-run's terminal summary must also state the plan: {err!r}")
    check("dropped or contradicted" not in err,
          f"verify --dry-run checked nothing, so its summary must not read "
          f"like a clean verify's: {err!r}")

    # Seeded: the wording the summary used to end with, the same one a real
    # clean merge ends with. If the check above still passed against it, it
    # would not be testing anything.
    stale = ("Done. Nothing your documents state was dropped or contradicted.\n"
             "  the full report went to stdout; exit code 0\n")
    check("Dry run: 3 call(s) planned, none made. Nothing was checked." not in stale,
          "seeded check: the old dry-run wording was accepted as the new one")
    check("dropped or contradicted" in stale,
          "seeded check: the old wording's own tell is not in the seed")


def test_pass_c_drops_the_one_bad_record_on_the_cli_and_grades_the_rest() -> None:
    """The whole command, not `verify_claims`. Pass C.

    `B-001` comes back MISSING and names an `evidence_source` anyway, which is
    the ruling this pass was written around: that record is individually
    unusable, and the document is not. It is the same answer on both attempts,
    so the repair loop is exhausted and the batch used to be discarded whole.
    `A-001` beside it is a valid verdict about a real claim and is graded.
    """
    bad = verdicts(
        ("A-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
        ("B-001", "MISSING", "", "merged.md"),
    )
    script = Script(**{**CLEAN, "forward": bad})
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    check(code == 2, f"an ungraded claim must exit 2, got {code} (stderr: {err!r})")
    check("Inconclusive." in out, f"the verdict line must match the code: {out[:300]!r}")
    section = out.split("## Not graded", 1)[-1].split("\n## ", 1)[0]
    check("B-001" in section, f"the section must name the claim it refused: {section!r}")
    check("A-001" not in section,
          f"a graded claim must not appear among the ungraded: {section!r}")
    check("evidence_source" in section,
          f"the section must carry the defect, not just a count: {section!r}")
    # The point of the pass: the rest of the batch survived. Without salvage the
    # forward direction errors whole, `A-001` is graded nowhere, and both source
    # rows read "not checked". An ungraded claim leaves the denominator the same
    # way an errored unit does, so the pooled row is 1/1 and not 1/2 -- the
    # claim that was dropped is accounted for in `Not graded`, not scored as a
    # loss the merge caused.
    check("| 1 | The relay listens on port 8443. | 1 | carried |" in out,
          f"the claim beside the dropped one must still be graded: {out!r}")
    check("Forward \u2014 source claims accounted for in the merge | **1/1**" in out,
          f"the graded half must have a denominator of its own: {out!r}")
    check("not checked (1 claim(s) extracted)" in out,
          f"the source whose claim went ungraded must say so: {out!r}")
    check("1 call(s) came back unusable and were graded in part" in out,
          "provenance must say the call errored and was salvaged, not that a "
          f"unit produced nothing: {out!r}")
    check("unit(s) of work errored" not in out,
          f"nothing errored whole here; the note must not say so: {out!r}")
    check(data["coverage"]["ungraded"] == 1,
          f"the json must carry the count too: {data['coverage']}")
    check([u["claim_id"] for u in data["unusable"]] == ["B-001"],
          f"and the record itself: {data['unusable']}")
    check(data["exit_code"] == code, "the json and the process must agree")


def test_a_whole_bad_answer_is_still_refused_whole_on_the_cli() -> None:
    """The must-not-fire beside the test above, over the same command.

    Only one verdict comes back for two claims. Nothing about the missing one
    is a property of a record -- there is no record -- so there is nothing to
    drop and the unit errors exactly as it did before Pass C. Both runs exit 2;
    what separates them is whether `Not graded` names a claim or says `None.`,
    which is the difference between a report that answers part of the question
    and one that answers none of it.
    """
    short = verdicts(("A-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"))
    script = Script(**{**CLEAN, "forward": short})
    with workspace(script) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    check(code == 2, f"a short answer must still exit 2, got {code} (stderr: {err!r})")
    check("verify (forward)" in out, "the verdict must name the unit that errored")
    section = out.split("## Not graded", 1)[-1].split("\n## ", 1)[0]
    check("None." in section,
          f"nothing may be salvaged out of a response-level fault: {section!r}")
    check(data["unusable"] == [], f"and nothing in the json either: {data['unusable']}")
    check("not checked (2 claim(s) extracted)" in out,
          f"the forward pass examined nothing and must say so: {out!r}")


def test_json_report_agrees_with_the_exit_code() -> None:
    script = Script(
        **{
            **CLEAN,
            "forward": verdicts(
                ("A-001", "MISSING", "", ""),
                ("B-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
            ),
        }
    )
    with workspace(script) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    check(data["exit_code"] == code,
          f"the JSON report says {data['exit_code']}, the process exited {code}")
    check(data["command"] == "merge", "the JSON report must name the command")
    check(len(data["findings"]) == 1, f"one finding expected, got {len(data['findings'])}")
    check(data["findings"][0]["finding"] == "dropped", "the finding must carry its label")
    check(data["documents"]["source_a.md"].endswith("notes-a.md"),
          "the JSON report must carry the mapping the Markdown one discloses")
    check(data["coverage"]["forward_submitted"] == 2,
          f"coverage must record what was submitted: {data['coverage']}")


def test_a_document_that_cannot_be_read_stops_the_run_before_any_call() -> None:
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, _, err = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "absent.md")
        )
        check(code == 2, f"a missing source must exit 2, got {code}")
        check("cannot read source" in err, f"the error must say what it could not read: {err!r}")

        (home / "blank.md").write_text("   \n\n", encoding="utf-8")
        code, _, err = invoke(
            home, base_url, "merge", str(home / "notes-a.md"), str(home / "blank.md")
        )
        check(code == 2, f"an empty source must exit 2, got {code}")
        check("is empty" in err, f"the error must say the document is empty: {err!r}")
        check(script.bodies == [], "neither failure may reach the endpoint")


def test_an_unreachable_endpoint_fails_once_not_five_times() -> None:
    """A transport fault will be the same fault on the next call.

    A schema failure errors one unit and the run goes on; this does not, and
    five identical timeouts only make the operator wait longer for the same
    message.
    """
    def refuse(_body, _n):
        return 500, "upstream is down"

    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        pass  # the endpoint is closed on exit; base_url now refuses connections

    with FakeEndpoint(refuse) as dead_url, tempfile.TemporaryDirectory() as raw:
        home = Path(raw)
        (home / "notes-a.md").write_text(SOURCE_A, encoding="utf-8")
        (home / "notes-b.md").write_text(SOURCE_B, encoding="utf-8")
        code, out, err = invoke(
            home, dead_url, "merge", str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--timeout", "2",
        )
    check(code == 2, f"an unreachable endpoint must exit 2, got {code}")
    check(out == "", f"a run that never started must not print a report: {out[:200]!r}")
    check("error:" in err, f"the failure must go to stderr: {err!r}")


# --------------------------------------------------------------------------
# the renderer, without a subprocess
# --------------------------------------------------------------------------


def test_the_script_still_recognises_every_prompt() -> None:
    """The scripted endpoint dispatches on prompt text. Prompt text moves."""
    for name, marker in Script.MARKERS.items():
        path = {"forward": "verify", "reverse": "verify_reverse",
                "coverage": "verify_coverage"}.get(name, name)
        text = (ROOT / "prompts" / f"{path}.md").read_text(encoding="utf-8")
        check(marker in text,
              f"tests/test_cli.py dispatches on {marker!r}; prompts/{path}.md no longer says it")


def test_a_ratio_is_never_printed_over_a_zero_denominator() -> None:
    """0/0 reads as a perfect score to anyone skimming for numbers."""
    check(report.ratio(0, 0, "not checked") == "not checked",
          "a zero denominator must render as words")
    check(report.ratio(3, 4, "not checked") == "**3/4**", "a real ratio renders as one")

    run = report.Run(command="verify", paths={"source_a.md": "a.md"})
    run.claims = {"source_a.md": [Claim("A-001", "source_a.md", "x", 1, "x", True)]}
    rendered = report.coverage_section(run)
    check("0/0" not in rendered, f"the empty coverage table printed a ratio: {rendered!r}")
    check("1 claim(s) extracted" in rendered,
          f"coverage must still report what it extracted: {rendered!r}")


def test_the_findings_list_carries_the_evidence_not_a_summary() -> None:
    claim = Claim("A-001", "source_a.md", "The connect timeout is 30 seconds.", 2, "30", True)
    run = report.Run(command="merge", paths={"source_a.md": "notes-a.md"})
    run.claims = {"source_a.md": [claim]}
    run.forward = [
        Verdict("A-001", "CONTRADICTED", "60 seconds", "merged.md", "b says 60",
                "source_to_merged", "grounded")
    ]
    rendered = report.findings_section(run)
    for fragment in ("**A-001**", "notes-a.md:2", "The connect timeout is 30 seconds.",
                     "'60 seconds'", "grounded", "b says 60"):
        check(fragment in rendered, f"the findings entry must carry {fragment!r}: {rendered!r}")


# --------------------------------------------------------------------------
# the inventory
# --------------------------------------------------------------------------


def inventoried(*, forward=(), reverse=(), claims=None, merged=()):
    """A `Run` carrying whole claims and their verdicts, ready to render.

    Built by hand rather than driven through the pipeline because the
    properties below are the renderer's, and a scripted endpoint would put a
    second thing between the assertion and the code it is about.
    """
    run = report.Run(command="merge",
                     paths={"source_a.md": "notes-a.md", "merged.md": "merged.md"})
    run.claims = {"source_a.md": list(claims or []), "merged.md": list(merged)}
    run.forward = list(forward)
    run.reverse = list(reverse)
    return run


def test_the_inventory_lists_every_claim_not_only_the_exceptions() -> None:
    """A carried claim has a row of its own, not only an exception.

    An exception-only report answers "was this fact carried over" with
    silence, and silence is also what a report prints when nothing was
    checked. The two must not look the same to a reader deciding whether to
    put a fact back.
    """
    kept = Claim("A-001", "source_a.md", "The relay listens on port 8443.", 1,
                 "port 8443", True)
    lost = Claim("A-002", "source_a.md", "The connect timeout is 30 seconds.", 2,
                 "30 seconds", True)
    run = inventoried(
        claims=[kept, lost],
        forward=[
            Verdict("A-001", "SUPPORTED", "The relay listens on port 8443.",
                    "merged.md", "carried whole", SOURCE_TO_MERGED, "grounded"),
            Verdict("A-002", "MISSING", "", "", "no timeout is stated",
                    SOURCE_TO_MERGED, "not_graded"),
        ],
    )
    rendered = report.inventory_section(run)

    check("2 claim(s): 1 dropped, 0 contradicted, 0 partly kept, 1 carried"
          in rendered,
          f"the heading counts every status; got {rendered!r}")
    for claim, status in ((kept, "carried"), (lost, "dropped")):
        row = [line for line in rendered.splitlines() if claim.text in line]
        check(len(row) == 1, f"{claim.id} needs exactly one row; got {row!r}")
        check(f"| {status} |" in row[0],
              f"{claim.id} must be marked {status!r}; got {row[0]!r}")
    # The carried row is not blank. A blank note beside "carried" is
    # indistinguishable from a claim nobody looked at.
    carried = [line for line in rendered.splitlines() if kept.text in line][0]
    check("carried whole" in carried,
          f"a carried claim must show what was found for it; got {carried!r}")


def test_a_claim_is_never_shortened_to_fit_a_cell() -> None:
    """The defect this project documents, applied to its own output.

    A claim bundling three facts can be scored covered by a merge that
    dropped one of them. A report that abbreviated the claim would hide the
    half that went missing, so `cell` escapes and never elides.
    """
    text = ("The archive rotates every 7 days | every archive is signed\n"
            "and the signature covers the manifest as well as the payload, "
            "which is the part a summary would drop.")
    rendered = report.cell(text)
    check("..." not in rendered and "\u2026" not in rendered,
          f"the cell elided: {rendered!r}")
    check(len(rendered) >= len(text.strip()),
          f"the cell lost characters: {len(rendered)} < {len(text.strip())}")
    check("\\|" in rendered and "<br>" in rendered,
          f"a pipe and a newline must be escaped, not dropped: {rendered!r}")
    # And through the table, where a raw pipe would end the cell early.
    claim = Claim("A-001", "source_a.md", text, 1, "x", True)
    row = [line for line in report.inventory_section(
        inventoried(claims=[claim])).splitlines() if "archive rotates" in line]
    delimiters = row[0].replace("\\|", "").count("|") if row else 0
    check(len(row) == 1 and delimiters == 6,
          f"the escaped pipe must not add a column; got {row!r}")


def test_an_unverified_line_number_says_so() -> None:
    """`anchored=False` means the model estimated the line. Not the same fact."""
    guessed = Claim("A-001", "source_a.md", "The relay listens.", 4, "listens", False)
    found = Claim("A-002", "source_a.md", "The timeout is 30s.", 2, "30s", True)
    rendered = report.inventory_section(inventoried(claims=[guessed, found]))
    check("| 4 (unverified) |" in rendered,
          f"an unanchored line must be marked; got {rendered!r}")
    check("| 2 |" in rendered,
          f"an anchored line prints the number alone; got {rendered!r}")


def test_an_ungrounded_quote_never_looks_like_a_verified_one() -> None:
    """Grounding is what separates a quote from a claim about a quote.

    `verify` grades the evidence span against the files themselves, and a
    span that is in no file, or in a file the model did not name, is not
    evidence. The row it sits in has to say which.
    """
    for grounding in ("transcription_error", "attribution_error"):
        claim = Claim("A-001", "source_a.md", "The relay listens.", 1, "listens", True)
        run = inventoried(
            claims=[claim],
            forward=[Verdict("A-001", "SUPPORTED", "the relay listens", "merged.md",
                             "found it", SOURCE_TO_MERGED, grounding)],
        )
        rendered = report.inventory_section(run)
        check(f"**{grounding}**" in rendered,
              f"{grounding} must be marked in the row; got {rendered!r}")


def test_an_invented_claim_is_not_given_a_source() -> None:
    """`Found in` answers "where does this come from". For an invention: nowhere.

    The model names a file even when it found nothing there. Printing it
    would have the report invent a provenance for the invention.
    """
    claim = Claim("M-001", "merged.md", "The idle timeout is 90 seconds.", 3, "90", True)
    run = inventoried(
        merged=[claim],
        reverse=[Verdict("M-001", "MISSING", "", "source_a.md", "no source says this",
                         MERGED_TO_SOURCES, "not_graded")],
    )
    rendered = report.inventory_section(run)
    row = [line for line in rendered.splitlines() if "idle timeout" in line]
    check(len(row) == 1 and "| invented | -- |" in row[0],
          f"an invented claim is sourced to nothing; got {row!r}")


def test_the_inventory_and_the_coverage_table_cannot_disagree() -> None:
    """Two figures for one quantity is the defect this report refuses.

    Both are read off `run.forward`, so this cannot fire through the
    pipeline. It fires for the next caller who assembles a `Run` by hand,
    which is what the pipeline is one refactor away from being.
    """
    claim = Claim("A-001", "source_a.md", "The relay listens.", 1, "listens", True)
    graded = Verdict("A-001", "SUPPORTED", "The relay listens.", "merged.md", "found",
                     SOURCE_TO_MERGED, "grounded")
    run = inventoried(claims=[claim], forward=[graded])
    report.inventory_section(run)  # one claim, one verdict, one row: consistent

    # The same claim graded twice, which is a model returning a duplicate. The
    # coverage table counts verdicts and sees two; the rows are keyed on the
    # claim and see one. Neither is wrong on its own terms, and that is the
    # problem: the report would print both figures for one quantity.
    run.forward = [graded, graded]
    try:
        report.inventory_section(run)
    except report.InventoryDisagrees as disagreement:
        check("One report, two answers" in str(disagreement),
              f"the refusal must say why; got {disagreement}")
    else:
        failures.append("an inventory that disagreed with coverage was printed anyway")


def test_a_clean_merge_still_reports_what_it_carried() -> None:
    """End to end, through the real CLI. The clean run is the point.

    Nothing went wrong, so the findings list is empty and the old report said
    almost nothing. The reader still has to be able to see that each claim was
    looked for and found.
    """
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, _ = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    check(code == 0, f"the clean run exits 0; got {code}")
    check("## Inventory" in out, "a clean run must still print the inventory")
    inventory = out.split("## Inventory")[1]
    # Headed by the name the caller typed, which `Run.display` resolves to the
    # path as given -- an absolute one under the temp workspace here.
    headings = [line for line in inventory.splitlines() if line.startswith("### ")]
    for name in ("notes-a.md", "notes-b.md", "merged.md"):
        check(any(f"{name}` --" in heading for heading in headings),
              f"{name} needs a table of its own; got {headings}")
    # Every claim the JSON carries has a row, and the rows carry no claim the
    # JSON does not: the two exports are of one run.
    listed = {claim["text"] for claim in data["claims"]}
    check(listed and all(report.cell(text) in inventory for text in listed),
          f"every extracted claim needs a row; got {sorted(listed)}")
    check("1 dropped" not in inventory and "1 contradicted" not in inventory,
          f"a clean run must count no exceptions; got {inventory!r}")


def test_a_contradiction_prints_both_halves_and_no_verdict_on_them() -> None:
    """The conflict case: what each document says, and why that is a clash.

    Which side is right is not printed, because the merge never said. The
    dispositions schema has no field for it, so a line here would be this
    tool's own guess wearing the merge's voice.
    """
    claim = Claim("A-002", "source_a.md", "The connect timeout is 30 seconds.", 2,
                  "30 seconds", True)
    run = inventoried(
        claims=[claim],
        forward=[Verdict("A-002", "CONTRADICTED", "The connect timeout is 60 seconds.",
                         "merged.md", "30 against 60", SOURCE_TO_MERGED, "grounded")],
    )
    rendered = report.findings_section(run)
    for fragment in ("notes-a.md:2", "The connect timeout is 30 seconds.",
                     "The connect timeout is 60 seconds.", "merged.md", "30 against 60"):
        check(fragment in rendered,
              f"a contradiction must carry {fragment!r}; got {rendered!r}")
    for invented in ("chose", "correct", "wins", "preferred"):
        check(invented not in rendered.lower(),
              f"the report must not adjudicate the conflict ({invented!r}): {rendered!r}")



def test_every_column_the_inventory_prints_is_in_the_json() -> None:
    """`--json` is the machine-readable half and has to stay the same report.

    A column readable only in the Markdown makes the JSON a summary of the
    report rather than the same run, and the next tool built on it would have
    to scrape the tables to get back what was already computed.
    """
    with workspace(Script(**CLEAN)) as (home, base_url):
        invoke(home, base_url, "merge",
               str(home / "notes-a.md"), str(home / "notes-b.md"),
               "--json", str(home / "report.json"))
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    # Claim column -> JSON field, verdict column -> JSON field, for every
    # column the two inventory tables print.
    for field in ("text", "line", "anchored"):
        check(field in data["claims"][0],
              f"the Claim/Line columns need {field!r} in the JSON; "
              f"got {sorted(data['claims'][0])}")
    for field in ("finding", "evidence", "evidence_source", "grounding", "rationale"):
        check(field in data["verdicts"][0],
              f"the Status/Found in/Note columns need {field!r} in the JSON; "
              f"got {sorted(data['verdicts'][0])}")
    # And the declarations table's new column, which is the merge's own words.
    check("reason" in Graded("a1", "dropped", "confirmed", "detail").as_dict(),
          "the declarations table prints a reason the JSON must carry too")


# --------------------------------------------------------------------------
# --html
# --------------------------------------------------------------------------
# The renderer itself is `tests/test_html_report.py`, which holds it against
# the Markdown and the JSON claim by claim. What is left for this file is the
# wiring: that the flag reaches the writer, that the page on disk is about the
# run that just happened, and that the two failure modes -- an unwritable path
# and a sweep -- are refusals rather than silence.


def test_the_html_report_is_written_and_is_about_this_run() -> None:
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, _ = invoke(home, base_url, "merge",
                              str(home / "notes-a.md"), str(home / "notes-b.md"),
                              "--json", str(home / "report.json"),
                              "--html", str(home / "report.html"))
        page = (home / "report.html").read_text(encoding="utf-8")
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))

    check(page.startswith("<!doctype html>"), "the file must be a whole document")
    check(page.rstrip().endswith("</html>"), "the file must be a whole document")
    check(f'data-exit-code="{code}"' in page,
          f"the page must carry the exit code the process returned ({code})")
    check(data["exit_code"] == code, "the JSON must agree, as it already did")
    # The caller's filenames, not the canonical ones the prompts saw.
    check("notes-a.md" in page and "notes-b.md" in page,
          "the page must name the documents the caller passed")
    check("\x00" not in page, "a NUL byte reached the page")
    # And it carries no control that points at a server. This file is written
    # to a path the caller chose, is opened from `file://` and is mailed on;
    # a "download this report" button in it would resolve against whatever
    # directory it ended up in, which is a broken link in the one copy nobody
    # can fix. The slot `html_report.render` leaves is empty here and only a
    # served page fills it (`api.report_page`).
    #
    # Matched on the markup rather than on the word: a *document* may well say
    # "download", and `esc` turns every quote a document carries into
    # `&quot;`, so an attribute spelling can only have come from this codebase.
    check(html_report.SLOT in page,
          "the slot has to be in the file, or a served page has nothing to "
          "fill and this check is asserting over its own absence")
    for marker in ('class="toolbar"', 'class="save"', 'download="'):
        check(marker not in page,
              f"the file written by --html carries {marker}, a control that "
              f"only means anything while a server is up")


def test_the_html_report_is_offered_by_both_commands() -> None:
    """`verify` too. The flag is on the shared parser and both paths write it."""
    with workspace(Script(**CLEAN), merged_on_disk=True) as (home, base_url):
        code, _, err = invoke(home, base_url, "verify",
                              str(home / "notes-a.md"), str(home / "notes-b.md"),
                              str(home / "draft.md"),
                              "--html", str(home / "verify.html"))
        check((home / "verify.html").exists(),
              f"verify --html wrote nothing (exit {code}): {strip(err)[:200]}")
        page = (home / "verify.html").read_text(encoding="utf-8")
    check("<title>LLossless verify " in page, "the page must name the command that ran")


def test_a_dry_run_writes_a_page_that_grades_nothing() -> None:
    """No call was made, so the page is a plan and carries no verdict banner."""
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, _, _ = invoke(home, base_url, "merge",
                            str(home / "notes-a.md"), str(home / "notes-b.md"),
                            "--dry-run", "--html", str(home / "plan.html"))
        page = (home / "plan.html").read_text(encoding="utf-8")

    check(code == 0, f"a dry run exits 0, got {code}")
    check("data-exit-code" not in page,
          "a dry run graded nothing and must show no verdict banner")
    check("none made" in page, "the page must say the calls were counted, not made")


def test_an_unwritable_html_path_is_a_refusal_and_not_a_silence() -> None:
    """Same bar as `--json`: a file the caller asked for and did not get is said."""
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, _, err = invoke(home, base_url, "merge",
                              str(home / "notes-a.md"), str(home / "notes-b.md"),
                              "--html", str(home / "nowhere" / "report.html"))

    check(code == 2, f"an unwritable report is a refusal, got exit {code}")
    check("report.html" in strip(err),
          f"the refusal must name the path it could not write: {strip(err)[:200]}")


def test_a_source_that_yields_no_claims_is_not_a_clean_verify() -> None:
    """Verify exited 0 and said nothing was dropped over an unexamined source.

    A source whose decomposition returns no claims was not examined at the
    claim level, and on `verify` the claim level is the whole examination.
    Reporting a clean verdict over it is the pattern this project exists to
    catch, so it is an error rather than a finding: findings are things the
    tool saw.
    """
    # Only source_a yields a claim; source_b decomposes to nothing. The
    # verdicts reference only the claim that exists, so the run is otherwise
    # entirely clean -- which is the shape that used to exit 0.
    empty = {**CLEAN,
             "decompose": lambda n: claims() if n == 2
             else claims(("The relay listens on port 8443.", 1)),
             "forward": verdicts(
                 ("A-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md")),
             "reverse": verdicts(
                 ("M-001", "SUPPORTED", "The relay listens on port 8443.", "source_a.md"))}
    script = Script(**empty)
    with workspace(script, merged_on_disk=True) as (home, base_url):
        code, out, err = invoke(home, base_url, "verify",
                                str(home / "notes-a.md"), str(home / "notes-b.md"),
                                str(home / "draft.md"))
    check(code == 2, f"an unexamined source must not be a clean verify, got {code}")
    check("Nothing was dropped, contradicted or invented." not in strip(err),
          f"the clean-run sentence must not appear: {strip(err)[:200]}")
    check("unestablished" in out,
          f"the report must say coverage for that source is unestablished: {out[:400]!r}")


def test_merge_says_what_covers_a_source_that_yielded_no_claims() -> None:
    """The other command: merge keeps exit 0 and narrows the claim.

    The reconciler genuinely does check that source structurally, so the run is
    not unexamined -- but "nothing was dropped" would claim more than was
    looked at, so the report says what the coverage rests on.
    """
    empty = {**CLEAN,
             "decompose": lambda n: claims() if n == 2
             else claims(("The relay listens on port 8443.", 1)),
             "forward": verdicts(
                 ("A-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md")),
             "reverse": verdicts(
                 ("M-001", "SUPPORTED", "The relay listens on port 8443.", "source_a.md"))}
    script = Script(**empty)
    with workspace(script) as (home, base_url):
        code, out, err = invoke(home, base_url, "merge",
                                str(home / "notes-a.md"), str(home / "notes-b.md"))
    check("reconciler" in out or "structural check" in out,
          f"the report must say what covers the source instead: {out[:400]!r}")
    if code == 0:
        check("structural check alone" in strip(err),
              f"the clean gloss must be narrowed: {strip(err)[:250]}")


def test_verify_refuses_before_the_first_decompose_when_the_window_is_too_small() -> None:
    """Decompose and verify had no window guard at all.

    Only the merge call preflighted. ollama does not refuse a prompt that
    overruns the window -- it trims the front and answers -- so claims came
    from the tail of the document and the report said nothing was dropped,
    because nothing downstream could see that anything had been.
    """
    script = Script(**CLEAN)
    endpoint = FakeEndpoint(script, served=64)
    with endpoint as base_url:
        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw)
            (home / "a.md").write_text(LONG_A, encoding="utf-8")
            (home / "b.md").write_text(LONG_B, encoding="utf-8")
            (home / "m.md").write_text(LONG_A + LONG_B, encoding="utf-8")
            was = os.environ.get("LLOSSLESS_CACHE_DIR")
            os.environ["LLOSSLESS_CACHE_DIR"] = str(home / "cache")
            try:
                code, _, err = invoke(home, base_url, "verify",
                                      str(home / "a.md"), str(home / "b.md"),
                                      str(home / "m.md"))
            finally:
                if was is None:
                    del os.environ["LLOSSLESS_CACHE_DIR"]
                else:
                    os.environ["LLOSSLESS_CACHE_DIR"] = was
    check(code != 0, f"a prompt that cannot fit the window must not be sent, got {code}")
    check("decompose" in strip(err),
          f"the refusal must name the role it refused: {strip(err)[:300]}")
    check("decompose" not in script.seen,
          f"it must refuse before the first decompose call, made {script.seen}")


def raises(exception, call, message: str):
    """Assert that `call` refuses, and return the exception for its message.

    The other suites in this project carry the same helper; this one had none
    because until now nothing here asserted a refusal from `config`.
    """
    try:
        call()
    except exception as exc:
        return exc
    except Exception as exc:  # noqa: BLE001
        failures.append(f"{message} (raised {type(exc).__name__}: {exc})")
        return None
    failures.append(f"{message} (nothing raised)")
    return None


def test_a_vendor_endpoint_runs_all_three_roles_only_when_a_window_is_stated() -> None:
    """End to end, on the command rather than on `served_window`.

    The blocker, measured: `window.preflight` refuses without a window and the
    only window source is `GET /api/ps`, which is ollama's. `merge` alone
    proceeds unguarded, so a vendor run gets a merge and then
    two roles erroring to exit 2 -- which is the first half of this test, run
    against the same endpoint as the second so the only thing that differs
    between them is the flag.

    Four defects have lived only on the CLI path in this project, so the flag
    is passed the way an operator passes it: through `argv`, into `config`,
    into the `Client` the command builds.
    """
    refused = Script(**CLEAN)
    with workspace(refused, ps_status=404) as (home, base_url):
        code, _, err = invoke(home, base_url, "merge",
                              str(home / "notes-a.md"), str(home / "notes-b.md"))
    check(code == 2,
          f"without a window a vendor run must still fail, got {code}")
    check("UNMEASURED" in strip(err),
          f"and must say the window could not be established: {strip(err)[:300]}")
    check("--window" in strip(err),
          f"and must name the remedy: {strip(err)[:300]}")
    check(refused.seen == ["merge"],
          f"the blocker's exact shape: `merge` proceeds unguarded and every "
          f"other role refuses before it sends, so one call reaches the "
          f"endpoint and the run still fails: {refused.seen}")

    stated = Script(**CLEAN)
    with workspace(stated, ps_status=404) as (home, base_url):
        code, out, err = invoke(home, base_url, "merge",
                                str(home / "notes-a.md"), str(home / "notes-b.md"),
                                "--window", "200000")
    check(code == 0,
          f"with a stated window every role must complete, got {code}: "
          f"{strip(err)[:300]}")
    check({"merge", "decompose", "forward", "reverse"} <= set(stated.seen),
          f"all three roles must have run: {sorted(set(stated.seen))}")
    check("Context window" in out and "200000" in out,
          "the report must carry the figure the run was guarded against")
    check("stated, not measured" in out,
          f"and must say it was stated rather than measured: "
          f"{[line for line in out.splitlines() if 'window' in line.lower()][:3]}")


def test_the_window_flag_and_its_variable_are_read_and_refuse_a_nonsense_figure() -> None:
    """A setting is not a setting until both spellings of it resolve.

    `--window` beats `LLOSSLESS_WINDOW`, the way every other flag here beats
    its variable, and neither accepts a figure that would turn the guard off:
    zero and a negative are refused rather than read as "unset", because the
    one thing this must never become is a default.
    """
    parser = cli.build_parser()
    args = parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md",
                              "--window", "4096"])
    settings = config.resolve(args, environ={"LLOSSLESS_WINDOW": "8192"})
    check(settings.window == 4096,
          f"the flag must beat the variable, got {settings.window!r}")

    args = parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md"])
    settings = config.resolve(args, environ={"LLOSSLESS_WINDOW": "8192"})
    check(settings.window == 8192,
          f"the variable alone must be read, got {settings.window!r}")

    settings = config.resolve(args, environ={})
    check(settings.window is None,
          f"and unset must stay unset -- there is no default window, got "
          f"{settings.window!r}")

    for bad in ("0", "-1", "8k", "1e5", "4096.5"):
        raises(config.ConfigError,
               lambda bad=bad: config.resolve(args, environ={"LLOSSLESS_WINDOW": bad}),
               f"LLOSSLESS_WINDOW={bad!r} must be refused rather than guessed at")


def test_the_profile_flag_and_its_variable_are_read_and_refuse_an_unknown_name() -> None:
    """The same two spellings for the request envelope, and the same refusal."""
    parser = cli.build_parser()
    args = parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md",
                              "--profile", "anthropic"])
    settings = config.resolve(args, environ={"LLOSSLESS_PROFILE": "openai-reasoning"})
    check(settings.profile == "anthropic",
          f"the flag must beat the variable, got {settings.profile!r}")

    args = parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md"])
    settings = config.resolve(args, environ={"LLOSSLESS_PROFILE": "openai-reasoning"})
    check(settings.profile == "openai-reasoning",
          f"the variable alone must be read, got {settings.profile!r}")
    check(config.resolve(args, environ={}).profile == structured.DEFAULT_PROFILE,
          "and unset must take the profile every recording was made with")

    raises(config.ConfigError,
           lambda: config.resolve(args, environ={"LLOSSLESS_PROFILE": "gpt-5.6"}),
           "an unknown profile must be refused, not passed through to the wire")


def test_a_byte_order_mark_is_not_part_of_the_first_heading() -> None:
    """A BOM made every heading unrecognisable and invented findings.

    `read_document` read `encoding="utf-8"`, which keeps a leading U+FEFF in the
    string. The segmenter's ATX pattern then failed to match the first heading,
    so a byte-faithful merge of a BOM source produced four findings -- a
    rewording, a false departure and two title findings -- all of them about a
    character no reader can see.
    """
    merged = ("# Runbook\nThe relay listens on port 8443.\n"
              "The read timeout is 45 seconds.\n")
    script = Script(**{**CLEAN,
                       "merge": json.dumps({"merged_document": merged,
                                            "decisions": [], "dispositions": []})})
    with workspace(script) as (home, base_url):
        (home / "notes-a.md").write_bytes(
            b"\xef\xbb\xbf# Runbook\nThe relay listens on port 8443.\n")
        (home / "notes-b.md").write_text(
            "# Runbook\nThe read timeout is 45 seconds.\n", encoding="utf-8")
        code, out, err = invoke(home, base_url, "merge",
                                str(home / "notes-a.md"), str(home / "notes-b.md"))
    check(code == 0, f"a faithful merge of a BOM source must exit 0, got {code}: "
                     f"{strip(err)[:220]}")
    check("\ufeff" not in strip(out),
          "the byte-order mark must not reach the report")


def test_a_byte_order_mark_inside_a_file_is_left_alone() -> None:
    """The other direction: utf-8-sig strips a leading BOM and nothing else."""
    body = "# Runbook\nA zero-width\ufeffno-break space mid-line.\n"
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "a.md"
        path.write_text(body, encoding="utf-8")
        got = cli.read_document(path, "source")
    check(got == body, f"a U+FEFF that is not leading must survive: {got!r}")


def test_no_output_flag_may_overwrite_a_source() -> None:
    """The -o refusal generalised over every path the run writes.

    An earlier pass closed this for `-o` and left `--json`, `--html` and
    `--sweep-dir` open, so `merge a.md b.md --json a.md` exited 0 and turned the
    source into a JSON report. A refusal guarding one of several write paths is
    a class half-closed, which is how this came back.
    """
    for flag in ("-o", "--json", "--html"):
        script = Script(**CLEAN)
        with workspace(script) as (home, base_url):
            source = home / "notes-a.md"
            before = source.read_bytes()
            code, _, err = invoke(home, base_url, "merge",
                                  str(source), str(home / "notes-b.md"),
                                  flag, str(source))
            after = source.read_bytes()
            calls = len(script.seen)
        check(code == 2, f"{flag} naming a source must exit 2, got {code}")
        check(after == before, f"{flag} must leave the source byte-identical")
        check(calls == 0,
              f"{flag} must be refused before any model call, {calls} were made")
        check("notes-a.md" in strip(err) or "source_a.md" in strip(err),
              f"the refusal must name the colliding source: {strip(err)[:200]}")

    # --sweep-dir writes merged.<level>.md and report.<level>.json into a
    # directory, so the collision is with a file the directory would contain.
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        clash = home / "merged.off.md"
        clash.write_text("a source that the sweep would overwrite\n", encoding="utf-8")
        before = clash.read_bytes()
        code, _, err = invoke(home, base_url, "merge",
                              str(clash), str(home / "notes-b.md"),
                              "--sweep-fidelity", "--sweep-dir", str(home))
        after = clash.read_bytes()
        calls = len(script.seen)
    check(code == 2, f"--sweep-dir over a source must exit 2, got {code}")
    check(after == before, "--sweep-dir must leave the source byte-identical")
    check(calls == 0, f"--sweep-dir must be refused before any call, {calls} were made")


def test_two_output_flags_may_not_name_one_path() -> None:
    """The other half: one file written twice is one report lost."""
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        both = home / "out.json"
        code, _, err = invoke(home, base_url, "merge",
                              str(home / "notes-a.md"), str(home / "notes-b.md"),
                              "--json", str(both), "--html", str(both))
        calls = len(script.seen)
    check(code == 2, f"two flags naming one path must exit 2, got {code}")
    check(calls == 0, f"it must be refused before any call, {calls} were made")
    check("out.json" in strip(err), f"the refusal must name the path: {strip(err)[:200]}")


def test_a_document_mentioning_think_tags_reaches_the_merge_intact() -> None:
    """Through the command: the parser must not edit the document.

    A source that tells an operator to wrap reasoning in <think> tags used to
    lose that sentence between the model's reply and the file on disk, with the
    run reporting nothing dropped -- the text was gone before anything counted
    it.
    """
    sentence = "Wrap your reasoning in <think> and </think> tags."
    source_a = f"The relay listens on port 8443.\n{sentence}\n"
    merged = (f"The relay listens on port 8443.\n{sentence}\n"
              "The read timeout is 45 seconds.\n")
    script = Script(**{**CLEAN,
                       "merge": json.dumps({"merged_document": merged,
                                            "decisions": [], "dispositions": []})})
    with workspace(script) as (home, base_url):
        (home / "notes-a.md").write_text(source_a, encoding="utf-8")
        out_path = home / "merged.md"
        code, _, err = invoke(home, base_url, "merge",
                              str(home / "notes-a.md"), str(home / "notes-b.md"),
                              "-o", str(out_path))
        written = out_path.read_text(encoding="utf-8") if out_path.is_file() else ""

    check(written == merged,
          f"the -o file must be byte-equal to the model's merged_document; got {written!r}")
    check(sentence in written, "the sentence naming the tags must survive")
    check(code == 0, f"a faithful merge must exit 0, got {code}: {strip(err)[:200]}")
    check("reasons regardless" not in strip(err),
          f"a document mentioning the tags is not a model that reasoned: {strip(err)[:200]}")


def test_an_unwritable_output_path_still_prints_the_merge_it_could_not_save() -> None:
    """The write is attempted after the report prints, not instead of it.

    `-o` into a directory that does not exist is a refusal, but the model call
    already happened -- the merged text must reach the operator through the
    report even though the file write failed, not be lost with the exit code."""
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, err = invoke(home, base_url, "merge",
                              str(home / "notes-a.md"), str(home / "notes-b.md"),
                              "-o", str(home / "nowhere" / "merged.md"))

    check(code == 2, f"an unwritable output path is a refusal, got exit {code}")
    check(strip(out) != "", "the report must still print on stdout")
    check("## Merged document" in strip(out),
          f"the report must carry the merge it could not write to disk: {strip(out)[:200]}")
    check("merged.md" in strip(err),
          f"the refusal must name the path it could not write: {strip(err)[:200]}")


def test_html_and_a_fidelity_sweep_is_refused() -> None:
    """Four runs, one page. Refused before any call, not written for one level."""
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, _, err = invoke(home, base_url, *sweep_argv(
            home, "--sweep-fidelity", "--html", str(home / "report.html")))

    check(code == 2, f"the combination is a refusal, got exit {code}")
    check("--html" in strip(err),
          f"the refusal must name the flag it is about: {strip(err)[:200]}")
    check(not (home / "report.html").exists(),
          "a refused run must leave no half-written page behind")



# --------------------------------------------------------------------------
# the fidelity sweep
# --------------------------------------------------------------------------


def sweep_argv(home: Path, *extra: str) -> list[str]:
    return ["merge", str(home / "notes-a.md"), str(home / "notes-b.md"), *extra]


# What a sweep over the scripted HTTP endpoint runs: every level but `sourced`,
# which that backend refuses. Written out rather than read off
# `sweep.plan`, because what the plan decides is the thing under test.
HTTP_SWEEP = tuple(level for level in config.FIDELITY_LEVELS
                   if level != config.SOURCED)


def http_sourced_refusal() -> str:
    """What `--fidelity sourced` over an HTTP endpoint is refused with, by `resolve`."""
    try:
        config.resolve(cli.build_parser().parse_args(
            ["merge", "a.md", "b.md", "--base", "a.md", "--fidelity", "sourced"]),
            environ={"LLOSSLESS_BASE_URL": "http://127.0.0.1:1"})
    except config.ConfigError as exc:
        return str(exc)
    raise AssertionError("sourced over HTTP resolved; the sweep tests' premise is gone")


def test_a_sweep_runs_every_level_once_and_prints_one_table() -> None:
    """One merge per level this backend runs, one table, in level order."""
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, err = invoke(home, base_url, *sweep_argv(home, "--sweep-fidelity"))
    check(code == 0, f"a clean sweep must exit 0: {code}, stderr {err!r}")
    check(script.seen.count("merge") == len(HTTP_SWEEP),
          f"one merge per level, saw {script.seen.count('merge')}")
    # By published name: the table is read by a person, so it says `verbatim`
    # where `report.json` says `off`. The order is still the wire order.
    positions = [out.find(f"\n  {config.fidelity_name(level)}  ")
                 for level in HTTP_SWEEP]
    check(all(n > 0 for n in positions),
          f"every level must have a row: {config.FIDELITY_PUBLISHED} in {out!r}")
    check(positions == sorted(positions),
          f"the rows must come in FIDELITY_LEVELS order, got offsets {positions}")
    for label, _ in sweep.COLUMNS:
        check(label in out, f"the table must carry the {label!r} column: {out!r}")


def test_the_four_levels_reach_the_model_as_four_different_prompts() -> None:
    """The whole point. Identical prompts would be one measurement, repeated."""
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        invoke(home, base_url, *sweep_argv(home, "--sweep-fidelity"))
    merges = [body["messages"][0]["content"] for body in script.bodies
              if Script.MARKERS["merge"] in body["messages"][0]["content"]]
    check(len(merges) == len(HTTP_SWEEP),
          f"expected {len(HTTP_SWEEP)} merge prompts, got {len(merges)}")
    check(len(set(merges)) == len(merges),
          f"the levels composed {len(set(merges))} distinct merge prompts, not {len(merges)}")


def test_a_sweep_will_not_stand_in_for_inference_it_did_not_do() -> None:
    """Dry-run makes no call, so a sweep of one has nothing to compare."""
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, err = invoke(home, base_url,
                                *sweep_argv(home, "--sweep-fidelity", "--dry-run"))
    check(code == 2, f"a dry-run sweep must be refused: {code}")
    check("--dry-run" in err, f"the refusal must name the flag it refuses: {err!r}")
    check(out == "", f"a refused sweep must print no table: {out[:200]!r}")


def test_a_sweep_cannot_be_replayed_and_the_refusal_says_why() -> None:
    """No merge cassette exists, so replay would silently sweep nothing."""
    settings = config.resolve(cli.build_parser().parse_args(
        ["merge", "a.md", "b.md", "--base", "a.md"]))
    refusal = sweep.refuse_before_running(
        dataclasses.replace(settings, replay_dir=Path("tests/responses")), False, None)
    check(refusal is not None, "a replayed sweep must be refused")
    check("no merge cassette" in (refusal or ""),
          f"the refusal must say what the corpus is missing: {refusal!r}")
    recorded = sorted(q.name.split("-")[0] for q in (ROOT / "tests" / "responses").glob("*.json"))
    check("merge" not in recorded,
          "a merge cassette now exists; sweep.py's refusal and docstring are stale")
    # `tests/responses/m4/` does hold 66 merge cassettes and they are not a way
    # round the refusal: their schema has one property and their prompt predates
    # the disposition model, so the key cannot match. Saying "zero merge
    # cassettes" without saying which tree is meant sends a reader to look.
    m4 = sorted((ROOT / "tests" / "responses" / "m4").glob("merge-*.json"))
    check(len(m4) == 66, f"the m4 archive should hold 66 merge cassettes, found {len(m4)}")
    check("m4" in (refusal or ""),
          f"the refusal must name the archive it is not talking about: {refusal!r}")
    import json as _json
    schema = _json.loads(m4[0].read_text())["request"].get("schema") or {}
    check(sorted(schema.get("properties") or {}) == ["merged_document"],
          "an m4 merge cassette must still be pre-disposition; if not, it may be replayable "
          f"and sweep.py's argument is stale: {sorted(schema.get('properties') or {})}")


def test_nothing_about_the_sweep_counts_the_levels_by_hand() -> None:
    """Every operator-facing sweep sentence counts `sweep.LEVELS`, not four.

    `open` made the ladder five and eight sentences went on saying four: the
    flag's own help ("report the four side by side"), three refusals an
    operator only ever meets when they have already got something wrong, and
    the module docstring twice. None was pinned by anything, which is why they
    all survived the level that falsified them.

    Asserted as an absence of the stale word plus the presence of the count,
    because either alone passes a sentence that dropped the number entirely.
    """
    parser = cli.build_parser()
    flags = {action.dest: action for action in parser._subparsers._group_actions[0]
             .choices["merge"]._actions}
    said = " ".join(flags["sweep_fidelity"].help.split())
    check(str(len(sweep.LEVELS)) in said,
          f"--sweep-fidelity's help must say how many levels it runs, from "
          f"`sweep.LEVELS`; got {said!r}")

    # The refusals, each rendered through the shipped function rather than
    # re-derived here. `Settings` is built the way `refuse_before_running` reads
    # it, so this fails if the sentence stops interpolating and not if it is
    # reworded around the number.
    stale = [word for word in ("four", "fourth")
             if word in " ".join(sweep.__doc__.split()).lower()]
    check(not stale,
          f"sweep.py's module docstring still counts the levels by hand "
          f"({stale}); `open` made them {len(sweep.LEVELS)}")

    # `mode` is derived from the flags rather than set, so the two refusals are
    # reached the way an operator reaches them: `--dry-run`, and `-o`. The
    # count is the plan's, because the sentence is about how many
    # merges this backend's sweep makes, and over HTTP that leaves `sourced` out.
    base = config.from_env({"LLOSSLESS_BASE_URL": "http://127.0.0.1:1"})
    planned = len(sweep.plan(base)[0])
    check(planned == len(HTTP_SWEEP),
          f"an HTTP sweep plans {planned} levels, expected {len(HTTP_SWEEP)}")
    for mode, settings, output, must_carry in (
            ("dry-run", dataclasses.replace(base, dry_run=True), None,
             str(planned)),
            ("output", base, Path("out.md"), str(planned - 1))):
        refusal = sweep.refuse_before_running(settings, False, output)
        check(refusal is not None, f"the {mode} sweep refusal has gone quiet")
        if refusal is None:
            continue
        check("four" not in refusal and "fourth" not in refusal,
              f"the {mode} sweep refusal still counts the levels by hand: "
              f"{refusal!r}")
        check(must_carry in refusal,
              f"the {mode} sweep refusal must carry {must_carry!r}, read off "
              f"sweep.plan; got {refusal!r}")

    # The table's own header and footnote, which said "Four points" through
    # two more levels because nothing here read them.
    rows = [{"fidelity": level, "exit_code": 0, "structural_kinds": [],
             **{key: 0 for _, key in sweep.COLUMNS if key != "exit_code"}}
            for level in HTTP_SWEEP]
    table = sweep.render(rows, {config.SOURCED: "refused"})
    check("four" not in table.lower() and "fourth" not in table.lower(),
          f"the sweep table still counts the levels by hand: {table!r}")
    check(f"{len(HTTP_SWEEP)} of {len(sweep.LEVELS)} levels" in table
          and f"{len(HTTP_SWEEP)} points" in table,
          f"the sweep table must count its rows, and say how many of the "
          f"ladder's levels they are: {table!r}")


def test_a_sweep_refuses_the_flags_it_would_have_to_ignore() -> None:
    """--fidelity chooses one level and -o names one path. Neither survives five."""
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, err = invoke(home, base_url, *sweep_argv(
            home, "--sweep-fidelity", "--fidelity", "high"))
        check(code == 2, f"--fidelity alongside --sweep-fidelity must be refused: {code}")
        check("--fidelity" in err, f"the refusal must name --fidelity: {err!r}")

        code, out, err = invoke(home, base_url, *sweep_argv(
            home, "--sweep-fidelity", "-o", str(home / "out.md")))
        check(code == 2, f"-o alongside --sweep-fidelity must be refused: {code}")
        check("--sweep-dir" in err, f"the refusal must point at the flag that works: {err!r}")
        check(not (home / "out.md").exists(), "a refused sweep must not write -o")

        code, out, err = invoke(home, base_url, *sweep_argv(
            home, "--sweep-dir", str(home / "sweep")))
        check(code == 2, f"--sweep-dir without --sweep-fidelity must be refused: {code}")
        check(not (home / "sweep").exists(), "a refused sweep must not create its directory")


def test_a_sweep_dir_holds_one_document_and_one_report_per_level() -> None:
    with workspace(Script(**CLEAN)) as (home, base_url):
        into = home / "sweep"
        code, out, err = invoke(home, base_url, *sweep_argv(
            home, "--sweep-fidelity", "--sweep-dir", str(into),
            "--json", str(home / "sweep.json")))
        check(code == 0, f"a clean sweep must exit 0: {code}, stderr {err!r}")
        for level in HTTP_SWEEP:
            document = into / f"merged.{level}.md"
            report_path = into / f"report.{level}.json"
            check(document.is_file(), f"{document.name} was not written")
            check(report_path.is_file(), f"{report_path.name} was not written")
            if document.is_file():
                check(document.read_text(encoding="utf-8").strip() != "",
                      f"{document.name} is empty")
        check(not (into / f"merged.{config.SOURCED}.md").exists()
              and not (into / f"report.{config.SOURCED}.json").exists(),
              "a level the backend refuses must leave no file behind")
        payload = json.loads((home / "sweep.json").read_text(encoding="utf-8"))
        check(payload["levels"] == list(HTTP_SWEEP),
              f"the sweep json must declare the levels it swept: {payload['levels']}")
        check(payload["left_out"] == {config.SOURCED: http_sourced_refusal()},
              f"and the level it left out, with the refusal `resolve` gives a run "
              f"at that level: {payload.get('left_out')!r}")
        check(sorted(payload["reports"]) == sorted(HTTP_SWEEP),
              f"every level's whole report must be in the json: {sorted(payload['reports'])}")
        check([r["fidelity"] for r in payload["comparison"]] == list(HTTP_SWEEP),
              "the comparison must carry one row per level, in level order")
        for row in payload["comparison"]:
            whole = payload["reports"][row["fidelity"]]
            check(row["exit_code"] == whole["exit_code"],
                  f"{row['fidelity']}: the row disagrees with the report beside it")
            on_disk = json.loads(
                (into / f"report.{row['fidelity']}.json").read_text(encoding="utf-8"))
            check(on_disk == whole,
                  f"{row['fidelity']}: the per-level file and the json disagree")


def test_one_level_failing_writes_nothing_at_all() -> None:
    """Three rows on disk read exactly like four to whoever finds them later."""
    seen: list[int] = []

    failing_calls = range(3, 3 + SCHEMA_ATTEMPTS)

    def merge_reply(n: int) -> str | None:
        seen.append(n)
        # The third level's merge comes back unusable on every attempt, so
        # that level errors while the two before and the one after settle.
        return None if n in failing_calls else CLEAN["merge"]

    with workspace(Script(**{**CLEAN, "merge": merge_reply})) as (home, base_url):
        into = home / "sweep"
        code, out, err = invoke(home, base_url, *sweep_argv(
            home, "--sweep-fidelity", "--sweep-dir", str(into),
            "--json", str(home / "sweep.json")))
    check(code == 2, f"a sweep missing a level must exit 2: {code}")
    check(not into.exists(), "a refused sweep must not create its directory")
    check(not (home / "sweep.json").exists(), "a refused sweep must not write its json")
    check("partial sweep" in err, f"the refusal must say what it is refusing: {err!r}")
    check("mid" in err, f"the refusal must name the level that failed: {err!r}")
    check("Fidelity sweep" not in out,
          f"a refused sweep must not print the table: {out[:400]!r}")


def test_a_level_missing_from_the_rows_is_a_refusal_not_a_shorter_table() -> None:
    """`incomplete` is the unit under the CLI test above; check it directly."""
    every = list(config.FIDELITY_LEVELS)
    clean = [{"fidelity": level, "settled": True, "errored_steps": []}
             for level in every]
    check(sweep.incomplete(clean, every) == [], "every settled level is complete")
    check(sweep.refuse_after_running(clean, every) is None,
          "every settled level is not refused")

    short = [row for row in clean if row["fidelity"] != "low"]
    check(sweep.incomplete(short, every) == ["low"], f"got {sweep.incomplete(short, every)}")
    check("low: did not run" in (sweep.refuse_after_running(short, every) or ""),
          "a level that never ran must be named as such")

    errored = [dict(row, settled=False, errored_steps=["merge"])
               if row["fidelity"] == "high" else row for row in clean]
    check(sweep.incomplete(errored, every) == ["high"],
          f"got {sweep.incomplete(errored, every)}")
    check("high: merge" in (sweep.refuse_after_running(errored, every) or ""),
          "a level that errored must be named with its step")

    # A level the plan left out is not missing, and one it kept always is.
    # The same rows, counted against two plans, give two answers.
    kept = list(HTTP_SWEEP)
    without = [row for row in clean if row["fidelity"] in kept]
    check(sweep.incomplete(without, kept) == [],
          "a level the plan left out must not count as missing")
    check(sweep.incomplete(without, every) == [config.SOURCED],
          "a level the plan kept must count as missing when it did not run")


def test_settings_for_changes_the_fidelity_and_nothing_else() -> None:
    settings = config.resolve(cli.build_parser().parse_args(
        ["merge", "a.md", "b.md", "--base", "a.md", "--fidelity", "off"]),
        environ={"LLOSSLESS_BASE_URL": "http://127.0.0.1:1"})
    for level in HTTP_SWEEP:
        moved = sweep.settings_for(settings, level)
        check(moved.fidelity == level, f"settings_for({level!r}) gave {moved.fidelity!r}")
        differing = [field.name for field in dataclasses.fields(settings)
                     if getattr(settings, field.name) != getattr(moved, field.name)]
        check(set(differing) <= {"fidelity"},
              f"a sweep row may differ by fidelity alone; {level} also moved {differing}")
    # The one level that may not be reached by a plain swap: over HTTP
    # it refuses, as a run at it does. The grant half is pinned by
    # `test_a_sweeps_sourced_row_is_granted_and_refused_as_a_run_at_sourced_is`.
    refused = raises(config.ConfigError,
                     lambda: sweep.settings_for(settings, config.SOURCED),
                     "a sweep's sourced row over HTTP must be refused, not swapped in")
    check(refused is not None and str(refused) == http_sourced_refusal(),
          f"and with the refusal a run at sourced is given: {refused}")
    try:
        sweep.settings_for(settings, "medium")
    except ValueError:
        pass
    else:
        failures.append("settings_for accepted a level that is not in FIDELITY_LEVELS")


def test_a_sweeps_sourced_row_is_granted_and_refused_as_a_run_at_sourced_is() -> None:
    """The sweep swapped each level in with a plain `replace`.

    So its `sourced` row met neither half of the `sourced` refusal rule: over an HTTP endpoint
    it ran unrefused and answered from recall under the `sourced` label, and
    through `claude` it was granted no tool. Every row is now pinned against
    what `config.resolve` gives a single run at that level, on both backends,
    through the shipped `sweep.plan` and `sweep.settings_for`.
    """
    parser = cli.build_parser()
    claude = ("/opt/claude-cli/bin/claude --print --model sonnet "
              + " ".join(config.RESULT_ARGS))
    backends = {
        "http": ([], {"LLOSSLESS_BASE_URL": "http://127.0.0.1:1"}),
        "claude": (["--answer-with", claude],
                   {"LLOSSLESS_WINDOW": "200000",
                    "LLOSSLESS_COMMAND_ENVELOPE": config.ENVELOPE_RESULT}),
    }
    plans = {}
    for name, (extra, environ) in backends.items():
        argv = ["merge", "a.md", "b.md", "--base", "a.md", *extra]
        swept = config.resolve(parser.parse_args(argv), environ=environ)
        runs, left_out = plans[name] = sweep.plan(swept)
        for level in config.FIDELITY_LEVELS:
            try:
                single = config.resolve(
                    parser.parse_args([*argv, "--fidelity", level]), environ=environ)
                refused = None
            except config.ConfigError as exc:
                single, refused = None, str(exc)
            if refused is not None:
                check(level not in runs and left_out.get(level) == refused,
                      f"{name}: {level} refuses a single run, so the sweep must "
                      f"leave it out with that refusal: runs {list(runs)}, "
                      f"left out {left_out.get(level)!r}")
                continue
            check(runs.get(level) == single,
                  f"{name}: the sweep's {level} row must be the settings a run "
                  f"at {level} resolves to")
            check(level not in left_out, f"{name}: {level} runs and was left out")

    # The direction, stated, so the loop above cannot pass by agreeing with a
    # `resolve` that stopped refusing or stopped granting.
    runs, left_out = plans["http"]
    check(list(runs) == list(HTTP_SWEEP) and list(left_out) == [config.SOURCED],
          f"an HTTP sweep runs every level but sourced: {list(runs)}, {list(left_out)}")
    runs, left_out = plans["claude"]
    check(list(runs) == list(config.FIDELITY_LEVELS) and not left_out,
          f"a claude sweep runs every level: {list(runs)}, {list(left_out)}")
    if config.SOURCED in runs:
        check(config.granted_web_tools(runs[config.SOURCED].command)
              == config.AUTO_GRANT["claude"],
              f"a claude sweep's sourced row carries the automatic grant: "
              f"{runs[config.SOURCED].command!r}")
    for level, at in runs.items():
        if level != config.SOURCED:
            check(config.granted_web_tools(at.command) == (),
                  f"{level} must be granted nothing: {at.command!r}")


def claude_program(home: Path, log: Path, model_usage: dict | None = None) -> str:
    """A command named `claude` that answers as `CLEAN` does, in the result envelope.

    Named `claude` because `AUTO_GRANT` is keyed by the program's basename, and
    it logs its own argv beside the kind of prompt it was given, so a test can
    read back what every call was really granted. No network: it answers from
    the fixture in this file. `model_usage`, when given, is merged into the
    envelope: `modelUsage` names the resolved models, `usage` the answer's.
    """
    program = home / "bin" / "claude"
    program.parent.mkdir()
    program.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "os.environ.pop('LLOSSLESS_COMMAND', None)\n"
        f"sys.path[:0] = [{str(ROOT / 'tests')!r}, {str(ROOT / 'src')!r}]\n"
        "from test_cli import CLEAN, Script\n"
        "content = sys.stdin.read()\n"
        "kind = Script().kind(content)\n"
        f"with open({str(log)!r}, 'a') as log:\n"
        "    log.write(json.dumps({'kind': kind, 'argv': sys.argv[1:]}) + '\\n')\n"
        "reply = CLEAN[kind]\n"
        "reply = reply(1) if callable(reply) else reply\n"
        "answer = Script.answering_the_schema(kind, content, reply)\n"
        "envelope = {'type': 'result', 'subtype': 'success',\n"
        "            'is_error': False, 'num_turns': 1, 'result': answer}\n"
        + (f"envelope.update({model_usage!r})\n" if model_usage is not None else "")
        + "sys.stdout.write(json.dumps(envelope))\n",
        encoding="utf-8")
    program.chmod(0o755)
    return f"{program} --print {' '.join(config.RESULT_ARGS)}"


def test_a_sweep_on_the_command_line_grants_sourced_or_leaves_it_out() -> None:
    """Through `llossless merge --sweep-fidelity`, both backends, no live call.

    Through a program named `claude`: six levels run, and the calls of the
    `sourced` level, and only those, carry the automatic grant on the argv the
    program was really started with. The grant is said on stderr, because the
    banner was printed for the resolved level and grants nothing.

    Over HTTP: `sourced` is never sent, the sweep says so on stderr before the
    first level and under the table, each time with `resolve`'s own refusal,
    and every other level still runs and is written.
    """
    with workspace(Script(**CLEAN)) as (home, base_url):
        log = home / "calls.jsonl"
        command = claude_program(home, log)
        was = os.environ.get("LLOSSLESS_COMMAND_ENVELOPE")
        os.environ["LLOSSLESS_COMMAND_ENVELOPE"] = config.ENVELOPE_RESULT
        try:
            code, out, err = invoke(home, base_url, *sweep_argv(
                home, "--sweep-fidelity", "--answer-with", command,
                "--window", "200000", "--json", str(home / "sweep.json")))
        finally:
            if was is None:
                os.environ.pop("LLOSSLESS_COMMAND_ENVELOPE", None)
            else:
                os.environ["LLOSSLESS_COMMAND_ENVELOPE"] = was
        calls = ([json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
                 if log.exists() else [])
        payload = (json.loads((home / "sweep.json").read_text(encoding="utf-8"))
                   if (home / "sweep.json").exists() else {})
    # 2, not 0 or 1: the fake answers every call in one turn, so
    # the sweep's sourced level recalled and is not a sourced merge.
    check(code == 2, f"the claude sweep must complete: exit {code}, "
                     f"{err.strip()[-400:]!r}")
    merges = [call for call in calls if call["kind"] == "merge"]
    granted = [config.granted_web_tools(" ".join(["claude", *call["argv"]]))
               for call in merges]
    expected = [config.AUTO_GRANT["claude"] if level == config.SOURCED else ()
                for level in config.FIDELITY_LEVELS]
    check(granted == expected,
          f"one merge per level, and only sourced's granted: {granted}")
    # Every call from sourced's merge on is that level's, and carries the grant;
    # every call before it belongs to a level that must carry none.
    first = next((n for n, call in enumerate(calls) if call["kind"] == "merge"
                  and config.granted_web_tools(" ".join(["claude", *call["argv"]]))),
                 len(calls))
    before = [n for n, call in enumerate(calls[:first])
              if config.granted_web_tools(" ".join(["claude", *call["argv"]]))]
    after = [n for n, call in enumerate(calls[first:], first)
             if not config.granted_web_tools(" ".join(["claude", *call["argv"]]))]
    check(first < len(calls) and not before and not after,
          f"the grant must cover sourced's calls and no other level's: "
          f"granted before {before}, ungranted after {after}")
    check(f"fidelity {config.fidelity_name(config.SOURCED)}: the model is granted "
          f"{', '.join(config.AUTO_GRANT['claude'])}" in err,
          f"the sweep must say the grant is in force: {err[-600:]!r}")
    check(payload.get("levels") == list(config.FIDELITY_LEVELS)
          and payload.get("left_out") == {},
          f"a claude sweep leaves nothing out: {payload.get('levels')}, "
          f"{payload.get('left_out')}")

    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, out, err = invoke(home, base_url, *sweep_argv(home, "--sweep-fidelity", "-v"))
    reason = http_sourced_refusal()
    flat = " ".join(out.split())
    check(code == 0, f"an HTTP sweep must still run the rest: exit {code}, "
                     f"{err.strip()[-400:]!r}")
    check(script.seen.count("merge") == len(HTTP_SWEEP),
          f"sourced must never reach an HTTP endpoint: {script.seen.count('merge')} "
          f"merges for {len(HTTP_SWEEP)} levels")
    check(f"leaves out {config.fidelity_name(config.SOURCED)}" in err and reason in err,
          f"the exclusion must be said on stderr, with the refusal: {err[-800:]!r}")
    started = err.find(f"fidelity {config.fidelity_name(HTTP_SWEEP[0])}: merging")
    check(0 <= err.find(reason) < started,
          f"and before the first level starts: {err.find(reason)} against {started}")
    check(f"{config.fidelity_name(config.SOURCED)}: left out, not run. "
          f"{' '.join(reason.split())}" in flat,
          f"and under the table, with the same reason: {out[-900:]!r}")


# The CLI's `modelUsage` for a measured Opus merge, trimmed to what is read:
# a small model for the CLI's own steps, and the model that wrote the answer,
# whose counts are the envelope's own `usage` block.
TWO_MODELS = {"modelUsage": {
    "claude-haiku-4-5-20251001": {"inputTokens": 8377, "outputTokens": 17},
    "claude-opus-5-5": {"inputTokens": 8, "outputTokens": 16357},
}, "usage": {"input_tokens": 8, "output_tokens": 16357}}


def run_through_claude(model_usage: dict | None) -> tuple[int, str, str, dict]:
    """One `merge` through the fake `claude`, its envelope naming `model_usage`."""
    with workspace(Script(**CLEAN)) as (home, base_url):
        command = claude_program(home, home / "calls.jsonl", model_usage)
        was = os.environ.get("LLOSSLESS_COMMAND_ENVELOPE")
        os.environ["LLOSSLESS_COMMAND_ENVELOPE"] = config.ENVELOPE_RESULT
        try:
            code, out, err = invoke(
                home, base_url, "merge", str(home / "notes-a.md"),
                str(home / "notes-b.md"), "--answer-with", command,
                "--window", "200000", "--json", str(home / "report.json"),
                "-o", str(home / "merged.md"), "-v")
        finally:
            if was is None:
                os.environ.pop("LLOSSLESS_COMMAND_ENVELOPE", None)
            else:
                os.environ["LLOSSLESS_COMMAND_ENVELOPE"] = was
        report_path = home / "report.json"
        data = (json.loads(report_path.read_text(encoding="utf-8"))
                if report_path.exists() else {})
    return code, out, err, data


def model_rows(out: str) -> dict[str, str]:
    """The rendered `Model (role)` rows of a Markdown report, role -> value."""
    rows = {}
    for line in out.splitlines():
        found = re.match(r"\|\s*Model \((\w+)\)\s*\|\s*(.*?)\s*\|\s*$", line)
        if found:
            rows[found.group(1)] = found.group(2)
    return rows


def test_the_model_rows_name_the_id_that_answered_beside_the_alias() -> None:
    """The alias is the CLI's to resolve; `modelUsage` says what it resolved to.

    `--model opus` meant `claude-opus-5` until a newer Opus shipped under the
    same alias, and a report that records only the alias cannot say which one
    produced its figures. Through the fake `claude`, end to end: an envelope
    naming two models puts both on every ledger row, says which wrote the
    answer (the most output tokens, not the first key), and the Model rows
    read `alias -> id` with the other id named. One model: the row carries no
    note. No `modelUsage`: the row is the alias exactly as before, and no
    ledger row carries the key -- the must-not-fire, which is every HTTP run
    and every recorded cassette.
    """
    code, out, err, data = run_through_claude(TWO_MODELS)
    ledger = (data.get("provenance") or {}).get("ledger") or []
    expected = {"models": sorted(TWO_MODELS["modelUsage"]), "output": "claude-opus-5-5"}
    check(code in (0, 1) and ledger, f"the merge must complete: exit {code}, "
                                     f"{err.strip()[-400:]!r}")
    check(all(row.get("answered_by") == expected for row in ledger),
          f"every ledger row must carry both ids and the answer's author: "
          f"{[row.get('answered_by') for row in ledger]}")
    rows = model_rows(out)
    check(set(rows) == {"merge", "verify", "decompose"},
          f"one Model row per role: {rows}")
    for role, said in rows.items():
        check(said == "test-model -> claude-opus-5-5 (the answer's output "
                      "tokens; also named claude-haiku-4-5-20251001)",
              f"{role}: the row must name the alias, the author and the other "
              f"id: {said!r}")
    check("merge: test-model (claude-opus-5-5) answered" in err,
          f"and the run log must say which id answered: {err[-600:]!r}")

    code, out, err, data = run_through_claude(
        {"modelUsage": {"claude-sonnet-5": {"inputTokens": 5, "outputTokens": 900}}})
    ledger = (data.get("provenance") or {}).get("ledger") or []
    check(ledger and all(row.get("answered_by") == {"models": ["claude-sonnet-5"],
                                                    "output": "claude-sonnet-5"}
                         for row in ledger),
          f"one model is its own author: {[row.get('answered_by') for row in ledger]}")
    check(set(model_rows(out).values()) == {"test-model -> claude-sonnet-5"},
          f"and its row carries no note: {model_rows(out)}")

    code, out, err, data = run_through_claude(None)
    ledger = (data.get("provenance") or {}).get("ledger") or []
    check(ledger and not any("answered_by" in row for row in ledger),
          f"an envelope naming no model must leave the ledger as it was: "
          f"{[sorted(row) for row in ledger]}")
    check(set(model_rows(out).values()) == {"test-model"},
          f"and the Model rows must be the alias alone: {model_rows(out)}")
    check("(claude-" not in err, f"and the log must name no id: {err[-400:]!r}")


def test_a_sweep_will_not_publish_rows_decoded_on_different_tiers() -> None:
    """The tier latches down mid-run, so rows can differ by decoding, not policy."""
    every = list(config.FIDELITY_LEVELS)
    alike = [{"fidelity": level, "settled": True, "errored_steps": [],
              "structured": "native"} for level in every]
    check(sweep.tiers_disagree(alike) == {}, "one tier across every level is comparable")
    check(sweep.refuse_after_running(alike, every) is None,
          f"alike rows must not be refused: {sweep.refuse_after_running(alike, every)!r}")

    latched = [dict(row, structured="prompt") if row["fidelity"] in ("mid", "high")
               else row for row in alike]
    check(set(sweep.tiers_disagree(latched)) == set(config.FIDELITY_LEVELS),
          f"every level must be named, got {sweep.tiers_disagree(latched)}")
    refusal = sweep.refuse_after_running(latched, every) or ""
    check("not decoded alike" in refusal, f"the refusal must say why: {refusal!r}")
    for fragment in ("off: native", "mid: prompt", "--structured"):
        check(fragment in refusal, f"the refusal must carry {fragment!r}: {refusal!r}")

    # A level that never settled has no tier to disagree with, and must be
    # reported as the missing level it is rather than as a tier mismatch.
    unsettled = [dict(row, settled=False, structured=None, errored_steps=["merge"])
                 if row["fidelity"] == "high" else row for row in alike]
    check(sweep.tiers_disagree(unsettled) == {},
          "an unsettled level contributes no tier")
    check("partial sweep" in (sweep.refuse_after_running(unsettled, every) or ""),
          "an unsettled level is a partial sweep, not a tier mismatch")


def test_the_call_budget_spans_the_sweep_rather_than_resetting_each_level() -> None:
    """--max-calls ceilings an invocation. A sweep is one invocation."""
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        into = home / "sweep"
        code, out, err = invoke(home, base_url, *sweep_argv(
            home, "--sweep-fidelity", "--sweep-dir", str(into), "--max-calls", "8"))
    check(code == 2, f"a sweep that runs out of budget must exit 2: {code}")
    check(len(script.seen) <= 8,
          f"--max-calls 8 must hold across the sweep; the endpoint saw {len(script.seen)}")
    check("CallBudgetExceeded" in err, f"the reason must reach stderr: {err!r}")
    check("low: CallBudgetExceeded" in err,
          f"the refusal must name the level the budget ran out on: {err!r}")
    for level in ("mid", "high"):
        check(f"{level}: did not run" in err,
              f"a fatal fault stops the sweep, and {level} must be reported unrun: {err!r}")
    check(not into.exists(), "a sweep that ran out of budget must write nothing")
    check("Fidelity sweep" not in out, f"and must print no table: {out[:200]!r}")


# --------------------------------------------------------------------------
# the terminal
# --------------------------------------------------------------------------
#
# What these check is not that the words are nice. It is that the two streams
# stay separate: stdout is the report and nothing else may reach it, stderr is
# where a person is told what is happening. A run that says nothing and a run
# that says it on the wrong stream are both bugs, and the second one is worse
# because it corrupts a figure rather than merely hiding it.


VARIES = re.compile(r"^\| (?:Duration|Generated) \|")

# The headline of the end-of-run block, which belongs on stderr and only there.
OUTCOME_WORDS = cli.OUTCOME[0][1]


def steady(text: str) -> str:
    """The report with the two rows that cannot repeat taken out.

    A duration and a wall-clock stamp differ between any two runs, so a
    byte-for-byte comparison of two invocations has to drop them or assert
    nothing. Everything else in the block is expected to be identical.
    """
    return "\n".join(line for line in text.splitlines() if not VARIES.match(line))


def parser_prints(argv: list[str], message: str) -> str:
    """Whatever the parser writes to stdout on its way to a clean exit."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        try:
            cli.build_parser().parse_args(argv)
        except SystemExit as exit_code:
            check(exit_code.code == 0, f"{message} (exited {exit_code.code}, expected 0)")
            return out.getvalue()
    failures.append(f"{message} (it did not exit)")
    return out.getvalue()


def test_the_version_is_askable_and_says_a_version() -> None:
    """`--version` existing at all was the first thing the report complained of."""
    for flag in ("-V", "--version"):
        printed = parser_prints([flag], f"{flag} must print a version and exit 0")
        check(__version__ in printed,
              f"{flag} must name the package version {__version__}: {printed!r}")
        check("LLossless" in printed,
              f"{flag} must name the tool, not just a number: {printed!r}")


def test_the_help_answers_the_questions_a_first_run_actually_has() -> None:
    """Not "is the help long" but "does it contain the six things you need".

    The report that prompted this was from someone who had the tool, had two
    documents, and could not get from one to the other without the README. Each
    string below is one thing they had to leave the terminal to find out.
    """
    top = parser_prints(["--help"], "--help must print and exit 0")
    for needed in ("--model", "models.local.json", "LLOSSLESS_MODEL",
                   "LLOSSLESS_BASE_URL", "--base", "-o", "exit"):
        check(needed in top,
              f"the top-level help must mention {needed!r} somewhere")
    check("llossless merge" in top and "llossless verify" in top,
          "the help must show a runnable line for each command")

    for command, needed in (
        ("merge", ("--base", "SOURCE", "-o")),
        ("verify", ("MERGED", "SOURCE")),
    ):
        text = parser_prints([command, "--help"], f"{command} --help must exit 0")
        for token in needed:
            check(token in text, f"`{command} --help` must mention {token!r}")
        for flag in ("-v", "--verbose", "--colour"):
            check(flag in text, f"`{command} --help` must offer {flag}")


def test_verbose_talks_on_stderr_and_leaves_the_report_alone() -> None:
    """The whole of items 3 to 5 rests on this: stdout does not move.

    Two runs of the same merge, one quiet and one `-vv`, and the report they
    print has to match byte for byte once the clock is taken out of it. If this
    ever fails, every recorded figure measured against stdout is in question.
    """
    # One workspace, two invocations. Separate temp dirs would differ in the
    # paths the report prints, which is a difference this test is not about.
    with workspace(Script(**CLEAN)) as (home, base_url):
        argv = ("merge", str(home / "notes-a.md"), str(home / "notes-b.md"))
        _, quiet_out, quiet_err = invoke(home, base_url, *argv)
        _, loud_out, loud_err = invoke(home, base_url, *argv, "-vv")
    check(steady(quiet_out) == steady(loud_out),
          "-vv must not change one byte of the report on stdout")
    check(len(loud_err) > len(quiet_err),
          f"-vv must say more than a quiet run does: {loud_err!r}")
    for stage in ("merge", "decompose", "verify"):
        check(stage in loud_err, f"-vv must name the {stage} stage on stderr: {loud_err!r}")
    check("reading" in loud_err,
          f"-vv must say it is reading the documents: {loud_err!r}")


def test_no_run_ends_without_saying_how_it_went() -> None:
    """A clean run, a run with findings, and both say so in words."""
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, err = invoke(home, base_url, "merge",
                                str(home / "notes-a.md"), str(home / "notes-b.md"))
    check(code == 0, f"the clean script must exit 0: {code}")
    check("Done." in err, f"a clean run must say so on stderr: {err!r}")
    check(OUTCOME_WORDS not in out,
          "and must not say it on stdout, where the report lives")
    check("exit code 0" in err, f"the code must be echoed in words: {err!r}")


def test_the_summary_names_the_file_that_was_never_written() -> None:
    """The worst moment in the report this work came from, asserted.

    `-o` was named, the merge errored, no file appeared, and nothing said so.
    """
    broken = dict(CLEAN, merge=None)  # the model answering unusably, twice
    with workspace(Script(**broken)) as (home, base_url):
        wanted = home / "merged.md"
        code, out, err = invoke(home, base_url, "merge",
                                str(home / "notes-a.md"), str(home / "notes-b.md"),
                                "-o", str(wanted))
    check(code == 2, f"a merge that could not be made must exit 2: {code}")
    check(not wanted.exists(), "and must not leave a file behind")
    check("Could not complete." in err, f"and must say so: {err!r}")
    check(str(wanted) in err, f"and must name the path it did not write: {err!r}")
    check("nothing was written" in err, f"in those words: {err!r}")
    check("merge did not finish" in err,
          f"and must say which step stopped it: {err!r}")
    check("MergeError" not in err and "Error:" not in err,
          f"in plain words, without the exception class: {err!r}")


def record_only_merge() -> tuple[int, str, str]:
    """A real `merge` whose one finding is in the merge's account of itself.

    `a6` is declared `superseded` by its own words and the merge carries it
    unchanged, so the reconciler raises `false_departure` -- a record kind --
    and nothing else fires: every claim is SUPPORTED and every other segment
    is carried. The exit code is 3 for the reason the caller is about.
    """
    a6 = LONG_A.splitlines()[5]
    with workspace(long_script(
        [{"segment": "a6", "disposition": "superseded", "replacement": a6,
          "reason": "the retry limit is restated below."}],
        (
            ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
            ("A-002", "SUPPORTED", "The archive rotates every 7 days", "merged.md"),
            ("A-003", "SUPPORTED", "every archive is signed", "merged.md"),
            ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
        ),
    )) as (home, base_url):
        return invoke(home, base_url, "merge",
                      str(home / "long-a.md"), str(home / "long-b.md"))


def test_a_record_only_run_is_not_described_as_unfinished() -> None:
    """Exit 3 has its own sentence, and the table it comes from has no gap.

    `summarise` read `OUTCOME.get(code, OUTCOME[2])` and `OUTCOME` had no row
    for 3, so a run that finished, with a merged document the tool found
    sound, ended "Could not complete. Part of this run did not finish" -- the
    one sentence that is false about it. Driven through `main`, on a merge
    whose only finding is a record finding.
    """
    code, out, err = record_only_merge()
    check(code == report.RECORD_ONLY,
          f"the fixture must reach exit {report.RECORD_ONLY} on its record "
          f"finding alone, or this test is about something else: exit {code}; "
          f"{err[-400:]!r}")
    check(report.RECORD_ONLY in cli.OUTCOME,
          "cli.OUTCOME has no row for exit 3")
    headline, gloss = cli.OUTCOME.get(report.RECORD_ONLY, ("(no row)", ""))
    said = " ".join(err.split())
    check(f"{headline} {gloss}" in said,
          f"exit 3 must end on its own sentence, {headline!r} {gloss!r}: {err!r}")
    check(cli.OUTCOME[2][0] not in err and "did not finish" not in err,
          f"a finished run must not be described as unfinished: {err!r}")
    check("exit code 3" in err, f"the code must be echoed: {err!r}")
    check(cli.OUTCOME[2][0] not in out and headline not in out,
          "the summary belongs on stderr, not in the report")

    # Seeded on the shipped function, not on a copy of it: with 3's row taken
    # out of the live table, `summarise` must fail loudly rather than borrow
    # another code's words. `.get(code, OUTCOME[2])` passed this silently.
    run = report.Run(command="merge")
    run.reconciled = reconcile.Reconciled(
        findings=(reconcile.Finding(reconcile.FALSE_DEPARTURE, "detail"),),
        declared_drops=(), segments=10)
    check(report.exit_code(run) == report.RECORD_ONLY,
          "the seed run must be a record-only run")
    kept = cli.OUTCOME.pop(report.RECORD_ONLY, None)
    try:
        cli.summarise(run, report.RECORD_ONLY, output=None, coloured=False,
                      piped=False, stream=io.StringIO())
    except KeyError:
        pass
    else:
        failures.append("with exit 3 removed from OUTCOME, summarise still "
                        "printed something: a fallback is back")
    finally:
        if kept is not None:
            cli.OUTCOME[report.RECORD_ONLY] = kept

    # And the import-time assertion, read out of cli.py and run against a
    # table missing a code. It is what turns a missing row into a failure at
    # import rather than a KeyError at the end of a finished run.
    import ast
    source = (ROOT / "src" / "llossless" / "cli.py").read_text(encoding="utf-8")
    guards = [node for node in ast.parse(source).body
              if isinstance(node, ast.Assert)
              and "OUTCOME" in ast.unparse(node.test)
              and "EXIT_CODES" in ast.unparse(node.test)]
    check(len(guards) == 1,
          f"cli.py must assert at import that OUTCOME covers every exit code; "
          f"found {len(guards)} such assertion(s)")
    for guard in guards:
        namespace = {"OUTCOME": {k: v for k, v in cli.OUTCOME.items()
                                 if k != report.RECORD_ONLY},
                     "TINT": dict(getattr(cli, "TINT", {})),
                     "EXIT_CODES": report.EXIT_CODES}
        try:
            exec(compile(ast.Module([guard], []), "cli.py", "exec"), namespace)
        except AssertionError:
            pass
        else:
            failures.append("the import-time assertion passed a table with "
                            "exit 3 missing")
        exec(compile(ast.Module([guard], []), "cli.py", "exec"),
             {"OUTCOME": cli.OUTCOME, "TINT": cli.TINT,
              "EXIT_CODES": report.EXIT_CODES})
    # No lookup in `summarise` may have a default to fall back to.
    body = ast.unparse(next(node for node in ast.parse(source).body
                            if isinstance(node, ast.FunctionDef)
                            and node.name == "summarise"))
    check("OUTCOME.get(" not in body and "TINT.get(" not in body,
          "summarise must subscript OUTCOME and TINT, not .get() them: a "
          "default is how 3 came to read as 2")


def test_colour_never_reaches_a_redirected_stream() -> None:
    """`auto` is decided from the stream, and a captured stream is not a tty."""
    with workspace(Script(**CLEAN)) as (home, base_url):
        argv = ("merge", str(home / "notes-a.md"), str(home / "notes-b.md"), "-v")
        _, out, err = invoke(home, base_url, *argv)
        _, forced_out, forced_err = invoke(home, base_url, *argv, "--colour", "always")
    check("\033[" not in out, "no escape may reach a redirected stdout")
    check("\033[" not in err, "nor a redirected stderr")
    check("\033[" in forced_err, "--colour always must paint stderr anyway")
    check("\033[" in forced_out, "and stdout too -- that is what `always` means")
    # The property that makes painting safe: escapes go in, nothing else moves.
    check(steady(strip(forced_out)) == steady(out),
          "painting the report may add escapes and change nothing else")


def fake_tty(text: str = "") -> io.StringIO:
    """A captured stream that answers `isatty()` the way a terminal does.

    The whole of the colour decision is `stream.isatty()`, so a test that cannot
    lie about that cannot test the decision at all -- which is how the bug below
    survived: every test captured both streams, both captures said False, and
    the two wrong answers agreed.
    """
    class Tty(io.StringIO):
        def isatty(self) -> bool:
            return True

    return Tty(text)


@contextlib.contextmanager
def a_terminal_on_stderr():
    """stderr is a terminal, stdout is a file. The invocation the README shows.

    `NO_COLOR` and `TERM` are cleared for the duration because they outrank the
    isatty and a developer who exports either would otherwise see this test pass
    for the wrong reason.
    """
    was = {name: os.environ.pop(name, None) for name in ("NO_COLOR", "TERM")}
    out, err = io.StringIO(), fake_tty()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            yield out, err
    finally:
        for name, value in was.items():
            if value is not None:
                os.environ[name] = value


def test_a_bare_llossless_explains_itself_instead_of_refusing() -> None:
    """Typing the name of a tool is a question. argparse answered it with exit 2."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = cli.main([])
    printed = out.getvalue()
    check(code == 0, f"a bare `llossless` must exit 0, not {code}")
    check(printed == parser_prints(["--help"], "--help must print and exit 0"),
          "and must print exactly what -h prints, not a shorter usage line")
    check("COMMAND" in printed and "merge" in printed,
          f"which means naming the subcommands: {printed[:200]!r}")


def test_an_error_is_red_on_the_stream_it_is_printed_on() -> None:
    """The colour decision has to be the decision for stderr, not for stdout.

    This is the bug the report was about. `main` resolved colour once, from
    stdout, and handed that answer to every refusal -- so under
    `llossless merge ... > report.md`, which is the documented invocation,
    stdout is a file, the answer is False, and four different pod failures came
    out the same grey as everything else on the terminal.
    """
    with a_terminal_on_stderr() as (out, err):
        code = cli.main(["merge", "nowhere-a.md", "nowhere-b.md",
                         "--base", "nowhere-a.md"])
    printed = err.getvalue()
    check(code == 2, f"an unreadable source must exit 2, got {code}")
    check("\033[" not in out.getvalue(), "nothing may reach a redirected stdout")
    check(RED in printed, f"the refusal must be red on a terminal stderr: {printed!r}")
    # All of it, not the word in front of it: a 5xx from a proxy carries the
    # origin's own JSON body, and one red word above ten grey lines does not
    # read as an error.
    body = strip(printed).rstrip("\n")
    check(printed.rstrip("\n") == f"{RED}{body}{RESET}",
          f"the whole message must be inside one span: {printed!r}")
    check(body.startswith("error: "),
          f"and the text must be unchanged for anything grepping it: {body!r}")


def test_the_closing_block_says_what_was_found_not_that_something_was() -> None:
    """"The report lists what was found" sends a reader away to find out what.

    One dropped claim and one merge that was written: the operator should be
    able to stop reading at the terminal and know both how many and of what
    kind, without opening the report.
    """
    script = Script(**{**CLEAN, "forward": verdicts(
        ("A-001", "MISSING", "", ""),
        ("B-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
    )})
    with workspace(script) as (home, base_url):
        code, out, err = invoke(home, base_url, "merge",
                                str(home / "notes-a.md"), str(home / "notes-b.md"))
    check(code == 1, f"a dropped claim must exit 1, got {code} ({err!r})")
    check("1 dropped" in err, f"the closing block must count the finding: {err!r}")
    check("in a source, not in the merge" in err,
          f"and say what that word means, in the report's own gloss: {err!r}")
    check("## Findings" in err, f"and where to read the rest: {err!r}")
    # The counts on the two streams come from one function, so they cannot
    # disagree about how many there were.
    check("1 dropped" in out,
          f"the verdict line must carry the same count: {out[:400]!r}")


def structural_only(kind: str = "verbatim_violation") -> report.Run:
    """A run whose only finding is the reconciler's. The report's confusing case."""
    run = report.Run(command="merge")
    run.reconciled = reconcile.Reconciled(
        findings=(reconcile.Finding(kind=kind, detail="a link lost a character",
                                    segment="a12", document="source_a.md"),),
        declared_drops=(),
        segments=13,
    )
    return run


def test_a_structural_finding_is_not_reported_as_no_findings() -> None:
    """`1 finding(s)` in the verdict over `None.` in the Findings section.

    Both sentences were true -- the finding is structural and is listed three
    sections down -- and together they read as a report contradicting itself on
    the page a reader checks first. It was the first thing the operator asked
    about. The section now says which question it answered.
    """
    run = structural_only()
    verdict = report.verdict_section(run)
    findings = report.findings_section(run)
    check("1 finding(s)" in verdict, f"the verdict counts it: {verdict!r}")
    check(findings.strip().splitlines()[-1] != "None.",
          f"so the findings section must not say only 'None.': {findings!r}")
    check("None in the claims" in findings,
          f"it must say which question it answered: {findings!r}")
    check("`## Structure`" in findings,
          f"and point at the section that lists it: {findings!r}")

    clean = report.Run(command="merge")
    clean.reconciled = reconcile.Reconciled(findings=(), declared_drops=(), segments=13)
    check(report.findings_section(clean).strip().endswith("None."),
          "a run with nothing wrong anywhere still says just 'None.'")


def test_the_terminal_and_the_report_count_the_same_findings() -> None:
    """One counter, two channels. The failure this prevents is a quiet drift."""
    for kind in sorted(reconcile.FINDING_KINDS):
        run = structural_only(kind)
        found = report.what_was_found(run)
        check(len(found) == 1, f"{kind}: one finding must produce one line: {found!r}")
        check(found[0].startswith("1 "), f"{kind}: counted: {found[0]!r}")
        check("`## Structure`" in found[0], f"{kind}: located: {found[0]!r}")
        # Every kind has a gloss, and it is the report's own rather than a
        # second one written here that could drift from it.
        gloss = report.STRUCTURAL_HEADINGS[kind].split(" \u2014 ")[-1]
        check(gloss in found[0], f"{kind}: must carry the report's gloss: {found[0]!r}")


def test_a_conflict_recorded_without_a_choice_completes_a_merge_at_off() -> None:
    """Found through the command. The function-level probes agreed and were wrong.

    An earlier fix made the decision schema level-aware and told the model `chosen` is
    optional at `off`; a third site went on demanding it, so every merge that
    declared a decision was refused at `off`, `low` and `mid`. Two function
    probes passed throughout -- one asserted the schema accepted the record,
    the other asserted the `chosen is empty` message fired at the right levels
    -- because neither ran the whole payload through `check_merge`, and none of
    them ran the command.

    This is the test that would have caught it: a merge that records a conflict
    the only way `off` permits, all the way through `llossless merge`.
    """
    recorded = json.dumps({
        "merged_document": MERGED,
        "decisions": [{
            "slot": "connect timeout",
            "candidates": [{"text": "30 seconds", "document": "source_a.md"},
                           {"text": "60 seconds", "document": "source_b.md"}],
            "reason": "the documents disagree and this level may not choose",
        }],
        "dispositions": [],
    })
    with workspace(Script(**{**CLEAN, "merge": recorded})) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge",
            str(home / "notes-a.md"), str(home / "notes-b.md"),
            "--base", str(home / "notes-a.md"), "--fidelity", "off")
    check(code != 2,
          f"a decision with no chosen is how off records a conflict; the run must "
          f"not error on it. got exit {code}\n{err[-400:]}")
    check("chosen" not in err,
          f"nothing may complain that `chosen` is missing at off: {err[-300:]}")


def test_a_record_arguing_the_examples_case_is_a_finding() -> None:
    """The other half of the leak, wired into the command rather than asserted.

    The leak that motivated it reached no merged text: `qwen3:8b` merged the
    real documents, so neither marker appeared anywhere, and wrote the worked
    example's own reason sentence into a `reason` field. `example_content_leaks` was
    green over that and correctly so -- it reads the merged document for two
    content words, which is the whole of what it claims. This is the
    half that reads what the records say about themselves.

    Seeded from the captured text rather than invented: the reason below is
    what the model actually emitted on 2026-09-14, which is the example's
    sentence with its "because " removed.
    """
    replacement = "The archive rotates every 14 days.\n"
    with workspace(long_script(
        [{
            "segment": "a3",
            "disposition": "superseded",
            "replacement": replacement.strip(),
            "reason": "The base title was kept and this one was not.",
        }],
        (
            ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
            ("A-002", "CONTRADICTED", replacement.strip(), "merged.md"),
            ("A-003", "SUPPORTED", replacement.strip(), "merged.md"),
            ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
        ),
        merged=LONG_MERGED + replacement,
    )) as (home, base_url):
        code, out, data = long_merge(home, base_url)

    findings = data["prompt_leaks"]["findings"]
    check({f["kind"] for f in findings} == {"prompt_example_leak"},
          f"the reason leak must be reported as the same kind, not a new one; "
          f"got {findings}")
    check(any("a3" in f["detail"] and "base title was kept" in f["detail"]
              for f in findings),
          f"the finding must name the record and quote the clause; got {findings}")
    check(not merge.example_content_leaks(LONG_MERGED + replacement),
          "the merged text carries no marker: this is exactly the case the "
          "content-word half cannot see, which is why it is seeded here")
    check(data["structural"]["checks"] == 9
          and all(f["kind"] != "prompt_example_leak"
                  for f in data["structural"]["findings"]),
          f"the leak is still not one of the nine and must stay out of the "
          f"structural block; got {data['structural']['checks']}")


def test_a_merge_that_returns_the_prompts_example_is_a_finding() -> None:
    """`merge.example_content_leaks`, wired into the command.

    The detector is older than this test and had never run outside `tests/`:
    `tests/run_merge.py` recorded it on 73 units, `src/` called it on none, so
    the only defence a real `llossless merge` had against a model returning
    `merge.md`'s illustration instead of the documents was `decompose`'s span
    anchoring — which is what noticed on qwen3:4b, two passes and one model call
    later, and only because the invented text anchored nowhere.

    A seeded pair, because a scanner with no positive is green when it is blind.
    The must-fire merge is the faithful one plus a single sentence carrying one
    marker, so the leak is the *only* thing wrong with it and the exit code
    cannot be borrowed from a reconciler finding. The must-not-fire is the same
    merge without that sentence.

    The third assertion is the one that is not about detection. A leak is a
    finding but it is not one of the nine, so `structural` must not carry it and
    must still publish `checks: 9`: that block's denominator is what
    the graded run records (withheld with the paper) fixed, and a tenth thing inside it would restate
    every one of those records as a reading taken on a different instrument.
    """
    leaked = LONG_MERGED + "The Marlbrook funicular closes at dusk.\n"
    with workspace(long_script([], (
        ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
        ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
    ), a_claims=(("The connect timeout is 30 seconds.", 2),),
        merged=leaked,
    )) as (home, base_url):
        code, out, data = long_merge(home, base_url)

    check(code == 1,
          f"a merge carrying the prompt's worked example must not exit 0; got {code}")
    leaks = data["prompt_leaks"]
    check(leaks["ran"] is True and leaks["markers"] == list(merge.EXAMPLE_MARKERS),
          f"the block carries what was looked for, not only what was hit; got "
          f"{ {k: v for k, v in leaks.items() if k != 'findings'} }")
    check({f["kind"] for f in leaks["findings"]} == {"prompt_example_leak"},
          f"one kind, and it is the leak; got {leaks['findings']}")
    check(sorted(f["detail"].split("'")[1] for f in leaks["findings"])
          == ["funicular", "marlbrook"],
          f"one finding per marker, each naming its own; got "
          f"{[f['detail'] for f in leaks['findings']]}")
    check(data["structural"]["checks"] == 9
          and all(f["kind"] != "prompt_example_leak"
                  for f in data["structural"]["findings"]),
          f"the leak is not one of the nine and must stay out of their block; got "
          f"{data['structural']}")
    check("Prompt example returned" in out,
          f"the operator has to see it in the report, not only in the JSON; got "
          f"{[l for l in out.splitlines() if l.startswith('###')]}")
    check("**2 finding(s).** In the structure: 2 prompt example leak." in out,
          f"the headline count is computed apart from the exit code and has to "
          f"agree with it; got "
          f"{[l for l in out.splitlines() if 'finding(s)' in l]}")

    # Must-not-fire. Same sources, same script, same everything but the
    # sentence — so a green here is about the marker and not about the fixture.
    with workspace(long_script([], (
        ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
        ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
    ), a_claims=(("The connect timeout is 30 seconds.", 2),))) as (home, base_url):
        code, out, data = long_merge(home, base_url)

    check(code == 0, f"a faithful merge carries no marker and must exit 0; got {code}")
    leaks = data["prompt_leaks"]
    check(leaks["ran"] is True
          and leaks["markers"] == list(merge.EXAMPLE_MARKERS)
          and leaks["reason_clauses"] == len(merge.example_reason_clauses())
          and leaks["findings"] == [],
          f"checked and clean, which is not the same as not checked; got "
          f"{leaks}")
    # A green reader is owed the limit, not only the result. Pinned
    # here rather than trusted to survive a tidy-up, because the sentence
    # exists precisely for the run that finds nothing.
    check("exact-string" in leaks["not_checked"]
          and "own words" in leaks["not_checked"],
          f"a clean leak block must still say what it does not reach; got "
          f"{leaks.get('not_checked')!r}")

    # And a `verify` run, which merged nothing: the block has to say it did not
    # run rather than report a clean scan of a document the tool never made.
    with workspace(Script(**CLEAN), merged_on_disk=True) as (home, base_url):
        code, _, _ = invoke(
            home, base_url, "verify",
            str(home / "notes-a.md"), str(home / "notes-b.md"), str(home / "draft.md"),
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))
    check(code == 0 and data["prompt_leaks"]["ran"] is False
          and data["prompt_leaks"]["findings"] == [],
          f"no merge means nothing to scan; got {data['prompt_leaks']}")


def test_a_merge_that_states_one_fact_twice_is_a_finding() -> None:
    """Check 9's claim-level half, wired into the command.

    The defect this is about passed the whole pipeline clean on three real
    operator runs: two sources stating the same facts in two people's wordings,
    a merge that keeps both, and exit 0 with nothing reported. Nothing in the
    reconciler can see it -- the two copies are two strings, so the exact
    duplication pass is silent, and the control maximum for near-repeat
    similarity measures *above* the worst real positive, which is an
    inversion no threshold fixes. The claims are where it separates, and the
    claims exist only after the merged document is decomposed, which is why this
    runs from `cli.one_pass` rather than from `reconcile.findings`.

    A seeded pair again, and the two runs differ in **one** thing: which line
    the decomposer anchored the second copy of the claim to. The merged document
    is byte-identical in both, so nothing here can be borrowed from a reconciler
    finding, and the must-not-fire is the corpus's real noise case -- a
    decomposer emitting one fact twice from one line, which `toby-test-2 mid`
    and `disjoint_domains/source_b.md` both do without stating anything twice.
    """
    # One more line than the faithful merge, saying what line 1 already says in
    # the other source's words. That is the defect in miniature; an added line
    # is not a finding on its own, which is what keeps the pair clean.
    restated = LONG_MERGED + "Port 8443 is what the relay listens on.\n"

    def merged_claims(second_line: int, second_span: str) -> str:
        """Two claims, one text. The spans are what anchoring believes."""
        return json.dumps({"claims": [
            {"text": "The relay listens on port 8443.", "line": 1,
             "span": "The relay listens on port 8443"},
            {"text": "The relay listens on port 8443.", "line": second_line,
             "span": second_span},
        ]})

    def script(payload: str) -> Script:
        replies = (claims(("The connect timeout is 30 seconds.", 2)),
                   claims(*LONG_B_CLAIMS), payload)
        return Script(
            merge=json.dumps({"merged_document": restated, "decisions": [],
                              "dispositions": []}),
            decompose=lambda n: replies[min(n, len(replies)) - 1],
            forward=verdicts(
                ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
                ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
            ),
            reverse=verdicts(
                ("M-001", "SUPPORTED", "The relay listens on port 8443.", "source_a.md"),
                ("M-002", "SUPPORTED", "The relay listens on port 8443.", "source_a.md"),
            ),
        )

    with workspace(script(
        merged_claims(24, "Port 8443 is what the relay listens on")
    )) as (home, base_url):
        code, out, data = long_merge(home, base_url)

    check(code == 1,
          f"a merge that states one fact on two lines must not exit 0; got {code}")
    restatement = data["restated_claims"]
    check(restatement["ran"] is True,
          f"the block has to say it ran, so an empty list is not read as 'not "
          f"checked'; got {restatement}")
    check([f["kind"] for f in restatement["findings"]] == ["duplicated_content"],
          f"one finding, and it widens the existing kind rather than adding one; "
          f"got {restatement['findings']}")
    details = [f["detail"] for f in restatement["findings"]]
    check(any("lines 1, 24" in detail for detail in details),
          f"the finding names both lines, which is the whole evidence; got "
          f"{details}")
    check((restatement["claims"], restatement["source_claims"]) == (2, 2),
          f"the arithmetic rides beside the finding; got {restatement}")
    # The denominator the paper's records were taken on, unmoved: this is not
    # one of the nine, exactly as the prompt leak is not.
    check(data["structural"]["checks"] == 9
          and all(f["kind"] != "duplicated_content"
                  for f in data["structural"]["findings"]),
          f"the claim-level half is outside the nine and must stay out of their "
          f"block; got {data['structural']}")
    check("Stated twice" in out,
          f"the operator has to see it in the report, not only in the JSON; got "
          f"{[l for l in out.splitlines() if l.startswith('###')]}")
    check("claim(s) extracted from" in out,
          f"the merge and source claim counts belong in the report beside the "
          f"finding; got {[l for l in out.splitlines() if 'extracted from' in l]}")

    # Must-not-fire. Same document, same everything, one difference: the second
    # copy of the claim anchors to the line the first one did.
    with workspace(script(
        merged_claims(1, "The relay listens on port 8443")
    )) as (home, base_url):
        code, out, data = long_merge(home, base_url)

    check(code == 0,
          f"one fact twice from one line is decomposer noise, not a document "
          f"that says it twice; got {code}")
    check(data["restated_claims"]["ran"] is True
          and data["restated_claims"]["findings"] == [],
          f"checked and clean, which is not the same as not checked; got "
          f"{data['restated_claims']}")
    check(data["restated_claims"]["counts_are_evidence_not_the_test"] is True
          and "not counted" in data["restated_claims"]["predicate"],
          f"a clean block still owes the reader what the predicate is and what "
          f"it does not reach; got {data['restated_claims']}")

    # And a `verify` run, which merged nothing. The check reads the merged
    # document's claims, which `verify` has, and deliberately does not run
    # there: every fixture's `expected_exit_code` is derived from its probes for
    # a verify run, and a document-level finding is not derivable from probes.
    # Widening this check to run under `verify` too is not yet done.
    with workspace(Script(**CLEAN), merged_on_disk=True) as (home, base_url):
        code, _, _ = invoke(
            home, base_url, "verify",
            str(home / "notes-a.md"), str(home / "notes-b.md"), str(home / "draft.md"),
            "--json", str(home / "report.json"),
        )
        data = json.loads((home / "report.json").read_text(encoding="utf-8"))
    check(code == 0 and data["restated_claims"]["ran"] is False
          and data["restated_claims"]["findings"] == [],
          f"verify runs no document-level check and must say so; got "
          f"{data['restated_claims']}")


def test_the_declared_loss_budget_is_configurable_and_the_record_says_which() -> None:
    """The ceiling moves, and the record names the one that fired.

    Two declared drops of 24 segments is 8.3%. That is over the registered 5%
    and inside a 50% ceiling, so the same run must fail at the default and pass
    at `--loss-budget 0.5` -- the must-fire and must-not-fire pair the standing
    rule asks for, at a *non-default* value. A probe only at 0.05 exercises the
    constant, not the parameter.

    The record is the point. `over_budget: false` is not readable without the
    ceiling beside it: it means a clean merge at 0.05 and a generous ceiling at
    0.5, and a stored report has to be able to say which.
    """
    # A fresh script per workspace: `long_script`'s decompose is indexed by a
    # call counter the endpoint carries, so a second run over the same object
    # answers the third source's claims to the first source's request.
    def script():
        return long_script(dropped("a3", "a4"), (
            ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
            ("A-002", "MISSING", "", ""),
            ("A-003", "MISSING", "", ""),
            ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
        ), a_claims=(
            ("The connect timeout is 30 seconds.", 2),
            ("The archive rotates every 7 days", 3),
            ("The queue drains at 200 messages per second.", 4),
        ))

    with workspace(script()) as (home, base_url):
        code, _, data = long_merge(home, base_url)
        check(code == 1, f"must fire at the default ceiling; got {code}")
        check(data["declared_loss"] == {"drops": 2, "segments": LONG_SEGMENTS,
                                        "budget": 0.03, "check_disabled": False,
                                        "over_budget": True,
                                    "ratio": 2 / LONG_SEGMENTS},
              f"and the record must name the default; got {data['declared_loss']}")

    with workspace(script()) as (home, base_url):
        code, _, data = long_merge(home, base_url, "--loss-budget", "0.5")
        check(code == 0, f"must not fire at a ceiling of 0.5; got {code}")
        check(data["declared_loss"] == {"drops": 2, "segments": LONG_SEGMENTS,
                                        "budget": 0.5, "check_disabled": False,
                                        "over_budget": False,
                                        "ratio": 2 / LONG_SEGMENTS},
              f"and the record must name 0.5, not the constant; got "
              f"{data['declared_loss']}")


def test_a_budget_of_one_disables_the_check_and_the_report_says_so() -> None:
    """Permitted, but never silent.

    At 1.0 `drops / segments` cannot exceed the ceiling, so the check is off.
    The danger is not the setting, it is that `over_budget: false` reads
    identically to a merge that passed. So the record carries `check_disabled`
    and the rendered report says it in words.
    """
    with workspace(long_script(dropped("a3", "a4"), (
        ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
        ("A-002", "MISSING", "", ""),
        ("A-003", "MISSING", "", ""),
        ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
    ), a_claims=(
        ("The connect timeout is 30 seconds.", 2),
        ("The archive rotates every 7 days", 3),
        ("The queue drains at 200 messages per second.", 4),
    ))) as (home, base_url):
        code, out, data = long_merge(home, base_url, "--loss-budget", "1.0")
        check(code == 0, f"a disabled check cannot fail the run; got {code}")
        check(data["declared_loss"]["check_disabled"] is True,
              f"the record must say the check was disabled; got "
              f"{data['declared_loss']}")
        check(data["declared_loss"]["over_budget"] is False,
              "and over_budget stays false, which is exactly why the flag "
              "beside it is needed")


def test_a_budget_of_zero_is_a_strict_mode_and_one_drop_fails() -> None:
    """0.0 is coherent under the strictly-greater rule.

    One drop of 24 is 4.2%, inside the registered 5% and outside a ceiling of
    zero. The comparison stays strictly greater at every ceiling, which is the
    same rule that lets exactly 5% through at the default.
    """
    def script():
        return long_script(dropped("a3"), (
            ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
            ("A-002", "MISSING", "", ""),
            ("A-003", "MISSING", "", ""),
            ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
        ))

    with workspace(script()) as (home, base_url):
        code, _, _ = long_merge(home, base_url, "--loss-budget", "0.05")
        check(code == 0, f"one drop of 24 is inside the default; got {code}")
    with workspace(script()) as (home, base_url):
        code, _, data = long_merge(home, base_url, "--loss-budget", "0")
        check(code == 1, f"and outside a ceiling of zero; got {code}")
        check(data["declared_loss"] == {"drops": 1, "segments": LONG_SEGMENTS,
                                        "budget": 0.0, "check_disabled": False,
                                        "over_budget": True,
                                    "ratio": 1 / LONG_SEGMENTS},
              f"the record must name 0.0; got {data['declared_loss']}")


def test_a_loss_budget_that_is_not_a_fraction_is_refused() -> None:
    """`--loss-budget 5` must not quietly mean 500%.

    The failure this rejects is a flag that reads like a tightening and is a
    disabling. Refusing the input costs one message; accepting it costs the
    check, silently, on every run that carries it.
    """
    for bad in ("5", "-0.1", "1.5", "nan"):
        with workspace(long_script(dropped("a3"), (
            ("A-001", "SUPPORTED", "The connect timeout is 30 seconds.", "merged.md"),
            ("A-002", "MISSING", "", ""),
            ("A-003", "MISSING", "", ""),
            ("B-001", "SUPPORTED", "The read timeout is 45 seconds.", "merged.md"),
        ))) as (home, base_url):
            code, _, err = invoke(
                home, base_url, "merge",
                str(home / "long-a.md"), str(home / "long-b.md"),
                "--loss-budget", bad,
            )
            check(code == 2, f"--loss-budget {bad} is a usage error, not a "
                             f"finding; got exit {code}")
            check("fraction" in err,
                  f"and the message must say what a budget is; got {err!r}")


def document_text_under(root: Path) -> list[str]:
    """Files under `root` that carry a line of the source documents.

    The property, not a list of filenames. "Nothing is written here" is a
    proxy; "none of what is written is the user's document" is the thing
    `--no-cache` promises, and it stays true when a new file appears for a
    reason nobody anticipated.
    """
    wanted = [line for line in (SOURCE_A + SOURCE_B).splitlines() if len(line) > 20]
    out = []
    for path in sorted(root.rglob("*")) if root.is_dir() else []:
        if not path.is_file():
            continue
        body = path.read_text(encoding="utf-8", errors="ignore")
        if any(line in body for line in wanted):
            out.append(str(path.relative_to(root)))
    return out


def test_the_cache_is_off_by_default_when_installed() -> None:
    """An installed user opts in to keeping a copy of their documents.

    The cache stores the rendered prompt, which contains the documents, and the
    raw response, which contains the merge. In a checkout that is a working
    convenience for the people this repository belongs to. Installed it is a
    copy of somebody's confidential input written under their home directory by
    a tool they ran once, and the default is off.

    Through the command, with neither flag, standing where an installed user
    stands: `IN_CHECKOUT` is read when a Settings is made, so this is the real
    default and not a value the test chose.
    """
    was = config.IN_CHECKOUT
    config.IN_CHECKOUT = False
    try:
        with workspace(Script(**CLEAN)) as (home, base_url):
            code, _, err = invoke(home, base_url, "merge",
                                  str(home / "notes-a.md"),
                                  str(home / "notes-b.md"), cache=None)
            left = sorted(p.name for p in (home / "cache").rglob("*") if p.is_file())
            carried = document_text_under(home / "cache")
    finally:
        config.IN_CHECKOUT = was
    check(code == 0, f"the merge itself must still run, got exit {code}: {err[-300:]!r}")
    check(not carried, f"an installed run must persist no document text by "
                       f"default, found it in {carried}")
    # The capability record is allowed and is the only thing allowed: it says
    # which structured-output tier this endpoint answered to, which is a fact
    # about the endpoint and carries nothing of anybody's documents. Named
    # rather than filtered, so a second file has to be argued for.
    check(set(left) <= {"capabilities.json"},
          f"an installed run may leave only the capability record, got {left}")


def test_no_cache_leaves_nothing_under_the_cache_directory() -> None:
    """And the flag has to mean it, including the dumps it never covered.

    `--no-cache` switched off the cassettes and left `failures/` and
    `discards/` writing response bodies into the same directory, which is the
    documents' content by another route. The dumps now go to a per-run
    temporary directory and the flag says so on stderr.

    The merge reply here fails the schema *and* carries the documents, which is
    what makes the run reach `_dump_attempt` at all. A clean run writes no
    dumps, so a clean run cannot test the thing this is about -- the first
    version of this check passed against the unfixed code for that reason.
    """
    holed = json.dumps({"merged_document": MERGED})     # no decisions, no
    script = Script(**{**CLEAN, "merge": holed})        # dispositions: refused
    with workspace(script) as (home, base_url):
        code, _, err = invoke(home, base_url, "merge", str(home / "notes-a.md"),
                              str(home / "notes-b.md"), cache="--no-cache")
        left = sorted(p.name for p in (home / "cache").rglob("*") if p.is_file())
        carried = document_text_under(home / "cache")
        scratch = re.search(r"dumps for this run go to (\S+)", err)
    check(bool(scratch), f"the flag must say where the dumps went: {err[-200:]!r}")
    if scratch:
        elsewhere = document_text_under(Path(scratch.group(1)))
        check(bool(elsewhere),
              "the dumps must still exist somewhere, or this proves nothing "
              "except that the run made none")
    check(not carried,
          f"--no-cache must persist no document text, found it in {carried}")
    check(set(left) <= {"capabilities.json"},
          f"--no-cache may leave only the capability record, got {left}")


def test_the_cache_flag_turns_it_back_on_where_the_default_is_off() -> None:
    """The must-not-fire direction: an opt-out default is not a removal.

    Without this, "off when installed" and "off everywhere" pass the same
    tests, and the flag that distinguishes them is never exercised.
    """
    was = config.IN_CHECKOUT
    config.IN_CHECKOUT = False
    try:
        with workspace(Script(**CLEAN)) as (home, base_url):
            code, _, err = invoke(home, base_url, "merge",
                                  str(home / "notes-a.md"),
                                  str(home / "notes-b.md"), cache="--cache")
            left = [p for p in (home / "cache").rglob("*") if p.is_file()]
    finally:
        config.IN_CHECKOUT = was
    check(code == 0, f"the merge must run, got exit {code}: {err[-300:]!r}")
    check(bool(left), "--cache must put the cassettes back")


def test_an_ungrounded_verdict_is_reported_and_does_not_move_the_exit_code() -> None:
    """Must not fire. A quote that is not in the source is not a merge defect.

    Grounding measures whether the judge anchored its verdict in the document
    it named. A judge that paraphrases is a vague judge, and folding that into
    the exit code would make the tool report a bad merge whenever it had a
    bad reader.
    """
    # One of the two verdicts quotes a span that is nowhere in the sources; the
    # other quotes one that is. The merge itself is clean.
    mixed = verdicts(
        ("A-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
        ("B-001", "SUPPORTED", "a sentence no document contains", "merged.md"),
    )
    with workspace(Script(**{**CLEAN, "forward": mixed})) as (home, base_url):
        code, out, _ = invoke(home, base_url, "merge", str(home / "notes-a.md"),
                              str(home / "notes-b.md"))
    check(code == 0,
          f"an ungrounded quote beside a grounded one must not change the exit "
          f"code; got {code}")
    check("transcription_error" in out or "Evidence grounded" in out,
          "and it must still be reported in the report")


def test_a_run_where_nothing_grounded_is_inconclusive() -> None:
    """Must fire. Graded, and not one verdict rested on anything real.

    The exception, and it is a measurement rule rather than a grading one: no
    verdict is anchored to anything that was shown to exist, so the run has
    produced no evidence. Same answer as a source that yielded no claims.
    """
    # Both directions answer, both answer usably, and neither quotes anything
    # that exists. The claim ids match the ones the clean fixture uses, so the
    # run is otherwise entirely ordinary -- the first version of this test used
    # the forward ids in the reverse direction, which errored the unit and
    # exited 2 for a reason that had nothing to do with grounding.
    forward_nowhere = verdicts(
        ("A-001", "SUPPORTED", "a sentence no document contains", "merged.md"),
        ("B-001", "SUPPORTED", "another sentence no document contains", "merged.md"),
    )
    reverse_nowhere = verdicts(
        ("M-001", "SUPPORTED", "a third sentence nothing contains", "source_a.md"),
    )
    with workspace(Script(**{**CLEAN, "forward": forward_nowhere,
                             "reverse": reverse_nowhere})) as (home, base_url):
        code, out, _ = invoke(home, base_url, "merge", str(home / "notes-a.md"),
                              str(home / "notes-b.md"))
    check(code == 2,
          f"a run where nothing grounded has measured nothing and must exit 2; "
          f"got {code}")


def _web_import_probe(home: Path, base_url: str, *, extra_import: bool = False
                       ) -> subprocess.CompletedProcess:
    """Run a complete `llossless merge` in a fresh interpreter, off the record.

    The operator's requirement is that somebody who wants only the CLI never
    pays for the web interface: "the user should still be able to use the CLI
    version without the webinterface if they do not want or need it." The
    architecture that keeps that promise is a one-way import -- `llossless.web`
    may import the engine, the engine may never import `llossless.web` -- and
    the only honest way to check an import never happened is to ask an
    interpreter that has done nothing else.

    Not `invoke()`. `invoke()` runs `cli.main` inside *this* process, and by
    the time any given test in this file runs, some earlier test may already
    have imported `llossless.web` for a reason of its own; `main()` below
    walks `sorted(globals())`, so which tests ran first is alphabetical and not
    a thing this check should ever depend on. A fresh `python3 -c` carries none
    of `test_cli.py`'s imports, so whatever it reports about
    `sys.modules["llossless.web"]` was put there, or kept out, by the merge
    itself.

    `extra_import` writes one extra line ahead of the merge --
    `import llossless.web` -- and exists only so a caller can prove this probe
    is capable of reporting `True`. A check that never fires on a positive is
    not a check; a typo in the module name it greps for, `llossless.webb` say,
    would pass this test forever regardless of what the CLI actually loads,
    and the only way to catch that is to make the probe see one.
    """
    preamble = "import llossless.web\n" if extra_import else ""
    script = f"""
import contextlib, io, json, sys
sys.path.insert(0, {str(ROOT / "src")!r})
sys.path.insert(0, {str(ROOT / "tests")!r})
{preamble}from llossless import cli
argv = [
    "merge", {str(home / "notes-a.md")!r}, {str(home / "notes-b.md")!r},
    "--base", {str(home / "notes-a.md")!r},
    "--base-url", {base_url!r},
    "--model", "test-model",
    "--merge-model", "test-model",
    "--structured", "prompt",
    "--no-cache",
]
out, err = io.StringIO(), io.StringIO()
with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
    code = cli.main(argv)
print(json.dumps({{
    "code": code,
    "web_loaded": "llossless.web" in sys.modules,
    "stderr": err.getvalue(),
}}))
"""
    return subprocess.run([sys.executable, "-c", script],
                          capture_output=True, text=True, cwd=ROOT)


def test_a_complete_merge_never_loads_the_web_package() -> None:
    """The CLI is not allowed to make the web interface a hard dependency.

    `src/llossless/web/` exists now only as a stub, so this rule holds today
    by accident -- nothing imports it, because there is nothing yet worth
    importing it for. It has to be pinned before a `llossless serve`
    subcommand gives anyone a reason to write `from llossless import web` at
    module scope "just to register the route", which is exactly the change
    that would make a plain `llossless merge` pull the web package in and
    break the operator's stated requirement silently, with no test noticing
    until someone went looking. A rule that nothing enforces is a comment.

    The probe runs a real, complete merge against the fake endpoint -- not a
    parser check, not a partial run -- and the assertion on `code == 0` is the
    important one to keep, not a courtesy: a probe whose merge crashed before
    reaching the model at all would also report `llossless.web` absent, and
    would pass this test while proving nothing about a working run.
    """
    with workspace(Script(**CLEAN)) as (home, base_url):
        probe = _web_import_probe(home, base_url)
    check(probe.returncode == 0,
          f"the probe subprocess must itself run to completion; exit "
          f"{probe.returncode}, stderr: {probe.stderr[-500:]!r}")
    if probe.returncode != 0:
        return
    result = json.loads(probe.stdout)
    check(result["code"] == 0,
          f"the merge inside the probe must actually succeed, or an absent "
          f"llossless.web proves nothing; got exit {result['code']}, stderr "
          f"tail: {result['stderr'][-500:]!r}")
    check(result["web_loaded"] is False,
          "llossless.web must not appear in sys.modules after a `llossless "
          "merge` run; the engine may not import the web package")


def test_the_web_import_probe_can_see_a_positive() -> None:
    """Must fire. The companion to the test above, and the one that matters.

    Without this, the test above is unfalsifiable: a `llossless.webb` typo,
    a probe that silently swallowed an import error, or a `sys.modules` check
    run before the interpreter had even parsed the import line would all make
    the real test pass regardless of what `llossless merge` does. Here the
    probe is handed a script that imports `llossless.web` on purpose, ahead
    of the merge, and is required to report it. A detector with no evidence it
    can ever say yes is not a detector.
    """
    with workspace(Script(**CLEAN)) as (home, base_url):
        probe = _web_import_probe(home, base_url, extra_import=True)
    check(probe.returncode == 0,
          f"the probe subprocess must itself run to completion; exit "
          f"{probe.returncode}, stderr: {probe.stderr[-500:]!r}")
    if probe.returncode != 0:
        return
    result = json.loads(probe.stdout)
    check(result["web_loaded"] is True,
          "the probe, told to import llossless.web before the merge, must "
          "report it present -- otherwise the check above is blind and its "
          "pass means nothing")


def test_open_excuses_a_declared_addition_and_charges_an_undeclared_one() -> None:
    """The whole level, through the command, both ways.

    Every part of this is unit-tested elsewhere -- the schema, the excusal, the
    banner, the section. None of that establishes that a declaration written by
    a merge reaches the exit code, because four correct units wired up wrongly
    still exit 0 on an invention. The two runs differ in one thing: whether the
    merge declared the statement it added.

    If the first of these ever exits 0, `open` has become a way to declare your
    way to a clean run, and the level is worth nothing.
    """
    added = "Solar generation is now cheaper than new coal in most markets."
    merged = MERGED.rstrip() + "\n\n" + added

    def script(declare: bool) -> Script:
        payload = {"merged_document": merged, "decisions": [], "dispositions": []}
        if declare:
            payload["additions"] = [{"statement": added, "corrects": "",
                                     "basis": "own-knowledge", "source": "",
                                     "reason": "well established"}]
        replies = dict(CLEAN)
        replies["merge"] = json.dumps(payload)
        replies["reverse"] = verdicts(
            ("M-001", "SUPPORTED", "The relay listens on port 8443.", "source_a.md"),
            ("M-002", "MISSING", "", ""))
        replies["decompose"] = lambda n: claims(
            ("The relay listens on port 8443.", 1), (added, 3)
        ) if n >= 3 else claims(("The relay listens on port 8443.", 1))
        return Script(**replies)

    with workspace(script(False)) as (home, base_url):
        code, out, _ = invoke(home, base_url, *sweep_argv(
            home, "--fidelity", "open", "--json", str(home / "r.json")))
        payload = json.loads((home / "r.json").read_text(encoding="utf-8"))
        findings = [v["finding"] for v in payload.get("findings", [])]
        check(code == 1, f"an undeclared addition must still fail the run: {code}")
        check(findings == ["hallucinated"],
              f"and must still be reported as an invention: {findings}")
        check(payload.get("additions") == [],
              "with nothing in the additions list to suggest otherwise")
        check("came from outside your documents" not in out,
              "and no suspended-guarantee notice, because nothing was declared "
              "and nothing was excused")

    with workspace(script(True)) as (home, base_url):
        code, out, _ = invoke(home, base_url, *sweep_argv(
            home, "--fidelity", "open", "--json", str(home / "r.json")))
        payload = json.loads((home / "r.json").read_text(encoding="utf-8"))
        check(code == 0, f"the same statement, declared, is excused: {code}")
        check([v["finding"] for v in payload.get("findings", [])] == [],
              "and is not reported as an invention")
        check(payload.get("additions_cover") == [["M-002"]],
              f"the report says which claim the declaration covered, so a "
              f"reader can weigh it: {payload.get('additions_cover')}")
        check("came from outside your documents" in out,
              "the verdict carries the notice that a clean result here means "
              "the merge said it was adding, not that it is true")
        check("Added from outside" in out,
              "and the section listing what went unchecked is rendered")


def test_a_cited_addition_is_carried_and_no_socket_is_opened_for_it() -> None:
    """Both bases accepted, both listed, and nothing fetched.

    The operator's ask was that `open` may say what it is going on when it
    corrects a statement. The risk that shapes it is that models fabricate
    citations, and a fabricated citation in a trusted report launders a guess
    into something that looks checkable -- so what this asserts is not that
    the citation is good, which nothing here can know, but that the report
    says what was done about it.

    Three properties, and the third is the one that has to hold forever.

    A `citation` record and an `own-knowledge` record are both accepted and
    both excused. If the second were refused, or rendered as a lesser answer,
    the next merge would invent a source to fill the field.

    The not-checked statement is in the section that lists them, where a
    reader weighing a citation is, rather than in a footnote elsewhere.

    **No socket is opened to resolve anything.** `invoke` runs the command in
    this process, and `socket_guard` is installed at the top of this module
    and refuses any address but the configured endpoint -- so a run that
    reached out to resolve a citation raises rather than passes. Asserted
    rather than assumed: the guard is confirmed installed and its blocked list
    confirmed empty across the run, because a guard that had been uninstalled
    by an earlier test would make this check pass by not running.
    """
    cited = "The BIP-39 word list is published under the MIT licence."
    recalled = "A 12-word mnemonic carries 128 bits of entropy."
    merged = MERGED.rstrip() + "\n\n" + cited + "\n\n" + recalled
    replies = dict(CLEAN)
    replies["merge"] = json.dumps({
        "merged_document": merged, "decisions": [], "dispositions": [],
        "additions": [
            {"statement": cited, "corrects": "",
             "basis": "citation", "source": "the OSI-approved MIT licence text",
             "reason": "the reference implementation ships that licence"},
            {"statement": recalled, "corrects": "",
             "basis": "own-knowledge", "source": "",
             "reason": "2048 words is 11 bits each"},
        ]})
    replies["reverse"] = verdicts(
        ("M-001", "SUPPORTED", "The relay listens on port 8443.", "source_a.md"),
        ("M-002", "MISSING", "", ""),
        ("M-003", "MISSING", "", ""))
    replies["decompose"] = lambda n: claims(
        ("The relay listens on port 8443.", 1), (cited, 3), (recalled, 5)
    ) if n >= 3 else claims(("The relay listens on port 8443.", 1))

    with workspace(Script(**replies)) as (home, base_url):
        code, out, _ = invoke(home, base_url, *sweep_argv(
            home, "--fidelity", "open", "--json", str(home / "r.json")))
        payload = json.loads((home / "r.json").read_text(encoding="utf-8"))

        check(code == 0,
              f"two declared additions the sources are silent about are "
              f"excused, whichever basis they carry: {code}")
        bases = [record.get("basis") for record in payload.get("additions", [])]
        check(bases == ["citation", "own-knowledge"],
              f"both records survive to the report with their basis intact, "
              f"and neither basis is a lesser answer: {bases}")
        sources = [record.get("source") for record in payload.get("additions", [])]
        check(sources == ["the OSI-approved MIT licence text", ""],
              f"the cited one carries its source and the recalled one carries "
              f"an empty string rather than an apology: {sources}")

        sourcing = payload.get("sourcing") or {}
        check(sourcing.get("resolved") is False and sourcing.get("fetched") is False,
              f"the report states what this tool did, and it is nothing: "
              f"{sourcing}")
        check(sourcing.get("state") == "unmeasured",
              f"and whether the *model* searched is unmeasured against an "
              f"endpoint that does not report it -- which is not zero: "
              f"{sourcing}")

        check("did not fetch, resolve or check any source" in out,
              "the not-checked statement is in the report, in words")
        section = out.split("Added from outside")[-1]
        check("did not fetch, resolve or check any source" in section,
              "and it is in the section that lists the sources, not in a "
              "footnote somewhere a reader meets afterwards")
        check("the OSI-approved MIT licence text" in section,
              "the source is shown, so a reader can go and check it themselves")
        check("](http" not in section and "<a " not in section,
              f"and it is never rendered as a link: an invitation the tool "
              f"drew reads as a destination the tool has been to")

        # The guard, confirmed in force rather than assumed. `blocked()` is
        # cumulative for the process, so a refusal raised anywhere in this
        # module's run would be here -- and an empty list from an uninstalled
        # guard is what this first check exists to rule out.
        check(socket_guard.installed(),
              "the socket guard must be installed, or the emptiness below is "
              "a guard that was not watching rather than a run that stayed put")
        check(socket_guard.blocked() == [],
              f"a run carrying a citation reached an address nobody "
              f"configured: {socket_guard.blocked()}")


def test_a_level_below_open_cannot_declare_an_addition_at_all() -> None:
    """The schema is the gate, and it is the only one that needs to be.

    `high` is not offered the key, so a merge emitting one is rejected by
    `validate` and retried rather than quietly excused. That is worth a test
    through the command because it is what lets every reader downstream --
    `cli.pipeline`, `Run.findings`, the report -- take the list at face value
    without re-checking the fidelity, which is exactly the kind of assumption
    that is true until it is not.
    """
    added = "Solar generation is now cheaper than new coal in most markets."
    replies = dict(CLEAN)
    replies["merge"] = json.dumps({
        "merged_document": MERGED.rstrip() + "\n\n" + added,
        "decisions": [], "dispositions": [],
        "additions": [{"statement": added, "corrects": "",
                       "basis": "own-knowledge", "source": "",
                       "reason": "sure"}]})
    with workspace(Script(**replies)) as (home, base_url):
        code, out, err = invoke(home, base_url, *sweep_argv(home, "--fidelity", "high"))
        check(code == 2, f"the response is unusable at high, not excused: {code}")
        check("additions" in err,
              f"and the refusal names the key that does not belong: {err[-300:]!r}")


def test_a_failed_title_check_does_not_discard_the_reconciler(  # noqa: C901
) -> None:
    """One short call failing must not cost nine mechanical checks.

    The title check is purely additive: `title_checked` returns the existing
    reconciliation unchanged, or with one more finding on it. Its result was
    written straight back to `run.reconciled`, and `step` returns None on
    anything but success -- so a title call the model could not answer
    discarded a reconciliation that had already succeeded, and the report then
    said *"Structure: not checked. The reconciler did not run over this
    merge"*. It had run. The result was thrown away.

    Found on a German/English pair where the title step errored
    (`toby-test-9`, `lang_missmatch`), and the run reported nothing below the
    claim level had been examined.

    The uncertainty is still recorded -- the step is in `run.errored` and the
    exit code is 2 -- so a reader is told the title was not graded without
    being told that nothing else was.
    """
    titled_a = "Relay Handbook\n\nThe relay listens on port 8443.\n"
    titled_b = "Relay Field Notes\n\nThe relay listens on port 8443.\n"
    # A title that is neither source's, so `verify_title` actually makes the
    # call. A copied title returns before reaching the model.
    merged = "Relay Guide\n\nThe relay listens on port 8443.\n"

    one = ("The relay listens on port 8443.", 3)
    replies = dict(CLEAN)
    replies["merge"] = json.dumps({"merged_document": merged,
                                   "decisions": [], "dispositions": []})
    replies["decompose"] = lambda n: claims(one)
    replies["forward"] = verdicts(
        ("A-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"),
        ("B-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md"))
    # The title check is the *first* reverse call: it runs before the merged
    # document is decomposed. `None` is how this fake says "unusable", twice
    # over, which is what errors the step.
    replies["reverse"] = lambda n: None if n == 1 else verdicts(
        ("M-001", "SUPPORTED", "The relay listens on port 8443.", "source_a.md"))

    with workspace(Script(**replies)) as (home, base_url):
        (home / "t-a.md").write_text(titled_a, encoding="utf-8")
        (home / "t-b.md").write_text(titled_b, encoding="utf-8")
        code, out, _ = invoke(
            home, base_url, "merge", str(home / "t-a.md"), str(home / "t-b.md"),
            "--base", str(home / "t-a.md"), "--title-policy", "synthesise",
            "--json", str(home / "r.json"))
        data = json.loads((home / "r.json").read_text(encoding="utf-8"))

    errored = [s["name"] for s in data.get("steps", []) if s.get("state") == "errored"]
    check("title" in errored,
          f"the title step must be the one that errored, or this test is "
          f"measuring something else: {errored}")
    check(code == 2,
          f"an errored unit makes the run inconclusive, which is unchanged: {code}")
    check(data["structural"]["ran"] is True,
          "and the reconciler's result survives it: nine mechanical checks "
          "that already ran must not be discarded by a later call that can "
          "only add to them")
    check(data["structural"]["segments"] > 0,
          f"with its segment count intact: {data['structural']['segments']}")


def _summary_of(err: str) -> str:
    """`summarise`'s closing sentence, off stderr, with the colour removed."""
    lines = [line for line in strip(err).splitlines()
             if line.startswith(("Done.", "Finished,", "Could not"))]
    return lines[0] if lines else ""


def _verdict_of(out: str) -> str:
    """The report's `## Verdict` paragraph, and nothing around it.

    Read out of the rendered report rather than by calling `verdict_line` with
    a hand-built `Run`: the thing under test is what an operator reads, and a
    `Run` assembled here would be one whose depth this test had set itself.
    """
    if "## Verdict" not in out:
        return ""
    after = out.split("## Verdict", 1)[1]
    return after.split("##", 1)[0].strip()


def _coverage(*rows):
    """The fused pass's payload: decompose's three fields, then the verdict's."""
    return json.dumps({"claims": [
        {"text": text, "line": line, "span": span, "verdict": verdict,
         "evidence": evidence, "evidence_source": "merged.md" if evidence else "",
         "rationale": "Checked against the merge."}
        for text, line, span, verdict, evidence in rows]})


def test_coverage_depth_costs_three_calls_and_says_what_it_did_not_check() -> None:
    """The depth's whole reason, and its whole cost, through the command.

    Three calls where `full` makes five: one merge, one fused call per source,
    and no reverse pass at all. The saving is real and so is the hole, so the
    run has to say both -- a reader who sees a clean report must be able to
    tell that nothing asked whether the merge invented anything.

    Through `invoke` rather than through `pipeline`, because the flag, the
    setting and the branch are three separate places to get this wrong and only
    the command exercises all three (`test-the-command-not-the-function`).
    """
    one = ("The relay listens on port 8443.", 1,
           "The relay listens on port 8443", "SUPPORTED",
           "The relay listens on port 8443")
    replies = dict(CLEAN)
    replies["coverage"] = lambda n: _coverage(one)

    script = Script(**replies)
    with workspace(script) as (home, base_url):
        code, out, err = invoke(home, base_url, *sweep_argv(
            home, "--verify-depth", "coverage", "--json", str(home / "r.json")))
        data = json.loads((home / "r.json").read_text(encoding="utf-8"))

    check(script.seen == ["merge", "coverage", "coverage"],
          f"three calls, one merge and one per source: {script.seen}")
    # And the figure the web picker prices this depth with is *this* figure.
    # `config.merge_model_calls` is what the page renders and what
    # `--verify-depth`'s help describes; measuring the calls here and asserting
    # the published number separately would be two numbers that agree today.
    check(len(script.seen) == config.merge_model_calls("coverage", 2),
          f"the page prices a two-document coverage run at "
          f"{config.merge_model_calls('coverage', 2)} calls and the run makes "
          f"{len(script.seen)}")
    check(code == 0, f"a clean coverage run still exits 0: {code}; {err[-300:]!r}")

    steps = {s["name"]: s for s in data.get("steps", [])}
    reverse = steps.get("verify (reverse)", {})
    check(reverse.get("state") == "skipped",
          f"the reverse pass must be recorded as skipped, not silently absent: "
          f"{reverse.get('state')}")
    check("invention" in str(reverse.get("detail", "")),
          f"and the reason must name what went unchecked: "
          f"{reverse.get('detail')!r}")
    check(not data.get("reverse"),
          "a coverage run reports no reverse verdicts")
    check(data["structural"]["ran"] is True,
          "the nine mechanical checks cost no model call and run at either "
          "depth; dropping them would be the depth checking less than it says")


def test_full_depth_is_unchanged_and_is_the_default() -> None:
    """The comparator, in the same module, on the same fixture.

    A cheaper depth is only meaningful against the one it replaces, and the
    claim "three calls instead of five" is two measurements. Taking the second
    from another test on another fixture would make it a figure from another
    day.
    """
    script = Script(**CLEAN)
    with workspace(script) as (home, base_url):
        code, _, err = invoke(home, base_url, *sweep_argv(
            home, "--json", str(home / "r.json")))
        data = json.loads((home / "r.json").read_text(encoding="utf-8"))

    check(script.seen == ["merge", "decompose", "decompose", "forward",
                          "decompose", "reverse"],
          f"the default is unchanged: {script.seen}")
    check(len(script.seen) == config.merge_model_calls(
              config.DEFAULT_VERIFY_DEPTH, 2),
          f"the comparator's published price is "
          f"{config.merge_model_calls(config.DEFAULT_VERIFY_DEPTH, 2)} calls "
          f"and the run makes {len(script.seen)}; the saving the picker shows "
          f"is the difference between two measured numbers or it is nothing")
    check("coverage" not in script.seen,
          "and the fused prompt is never sent without the flag")
    check(code == 0, f"the comparator is clean too: {code}; {err[-200:]!r}")
    steps = {s["name"]: s["state"] for s in data.get("steps", [])}
    check(steps.get("verify (reverse)") == "ok",
          f"at full depth the reverse pass runs: {steps.get('verify (reverse)')}")


def test_a_coverage_verdict_does_not_claim_invention_was_checked() -> None:
    """The headline a clean run opens with, over a run that asked one question.

    At `coverage` nothing reads the merged document back, and the verdict line
    said *"No extracted claim was dropped, contradicted, invented, or carried
    only in part"* anyway -- ruling out, in bold, the one class of failure the
    run had not looked for. Two skipped steps three lines above said so. The
    sentence was still the first thing a reader sees and the last one they
    remember.

    Asserted through the command, over the same scripted endpoint as the two
    tests above, because the report the operator reads is the one that has to
    be right. `report.verdict_line` is shared by the Markdown report, the HTML
    page and the terminal, so this covers all three; `tests/test_html_report.py`
    pins that sharing from the other end.
    """
    one = ("The relay listens on port 8443.", 1,
           "The relay listens on port 8443", "SUPPORTED",
           "The relay listens on port 8443")
    replies = dict(CLEAN)
    replies["coverage"] = lambda n: _coverage(one)

    with workspace(Script(**replies)) as (home, base_url):
        code, cheap, said = invoke(home, base_url, *sweep_argv(
            home, "--verify-depth", "coverage"))
    check(code == 0, f"the coverage run must be clean for this to mean "
                     f"anything: {code}")
    verdict = _verdict_of(cheap)
    check("invented" not in verdict.split("This run checked only")[0],
          f"the headline of a run that never read the merge back must not rule "
          f"out invention: {verdict!r}")
    check("checked only that your documents' content survived" in verdict,
          f"and it must say which guarantee is suspended: {verdict!r}")
    check("none in the other direction" in verdict,
          f"and that the second direction was not merely empty but never run: "
          f"{verdict!r}")
    # The fourth surface. `verdict_line` reaches the report, the HTML page and
    # the terminal's `--verbose` transcript; the last line a run prints is
    # `summarise`'s own sentence and had its own copy of the claim.
    check("invented" not in _summary_of(said)
          or "invention was not checked" in _summary_of(said),
          f"the terminal's closing line must not rule out invention either: "
          f"{_summary_of(said)!r}")
    check("invention was not checked" in _summary_of(said),
          f"and it must say so in words rather than by omission: "
          f"{_summary_of(said)!r}")

    with workspace(Script(**CLEAN)) as (home, base_url):
        code, full, also = invoke(home, base_url, *sweep_argv(home))
    check(code == 0, f"the comparator must be clean too: {code}")
    verdict = _verdict_of(full)
    check("invented" in verdict,
          f"at `full` the claim is earned and must still be made: {verdict!r}")
    check("checked only that your documents" not in verdict,
          f"and the caveat must not appear on a run that did check: {verdict!r}")
    check("merge claim(s) checked against the sources" in verdict,
          f"with both directions counted: {verdict!r}")
    check("Nothing was dropped, contradicted or invented." in _summary_of(also),
          f"and the terminal's closing line is unchanged at `full`: "
          f"{_summary_of(also)!r}")


def test_the_suspended_guarantee_is_worded_once_for_both_surfaces() -> None:
    """The report and the page say it in the same words, or they say two things.

    `web/locales/en.json`'s `advice.noinvention` has carried this sentence
    since W1 and `report.invention_sentence` is the same sentence with its
    first clause in bold. A reader who runs the tool on the command line and
    then through the browser is reading one tool, and two descriptions of one
    suspended guarantee is how they come to believe there are two.

    Compared string against string rather than by eye. The report is Markdown
    and the catalogue is not, so the bold markers come out before the
    comparison and nothing else is allowed to differ.
    """
    strings = json.loads(
        (ROOT / "src" / "llossless" / "web" / "locales" / "en.json")
        .read_text(encoding="utf-8"))["strings"]
    said = strings["advice.noinvention"]
    run = report.Run(command="merge", verify_depth=config.COVERAGE_DEPTH)
    sentence = report.invention_sentence(run).replace("**", "")
    check(sentence == said,
          f"the report and the page describe the same suspended guarantee "
          f"differently:\n  report: {sentence!r}\n  page:   {said!r}")


def test_a_dry_run_at_coverage_plans_the_calls_coverage_makes() -> None:
    """A plan that describes a different pipeline is worse than no plan.

    `--dry-run` exists to answer "what would this configuration cost", and the
    branch that chooses the fused pass was guarded on a merged document
    existing. Under `--dry-run` the merge is only planned, so there is none --
    and the plan named a `decompose source_a.md` call this depth never makes,
    said nothing about the reverse pass it never runs, and priced the run at
    `full`.

    The reverse of it is asserted too, and it is the reason the guard was
    there: a merge that *errored* must not be followed by one fused call per
    source against an empty string, which would spend real money to report
    every claim MISSING.
    """
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge", str(home / "notes-a.md"),
            str(home / "notes-b.md"), "--dry-run",
            "--verify-depth", "coverage", "--json", str(home / "r.json"))
        data = json.loads((home / "r.json").read_text(encoding="utf-8"))
    check(code == 0, f"a dry run still exits 0: {code}; {err[-200:]!r}")
    steps = {s["name"]: s for s in data.get("steps", [])}
    planned = sorted(name for name, s in steps.items() if s["state"] == "planned")
    check(planned == ["cover notes-a.md", "cover notes-b.md", "merge"],
          f"the plan must name the calls this depth makes: {planned}")
    check(not [name for name in steps if name.startswith("decompose")
               and steps[name]["state"] == "planned"],
          f"and must not plan a decompose call coverage never makes: "
          f"{sorted(steps)}")
    reverse = steps.get("verify (reverse)", {})
    check(reverse.get("state") == "skipped"
          and "invention" in str(reverse.get("detail", "")),
          f"the plan must say the reverse pass is not in it, and why: "
          f"{reverse}")

    # And the case the removed guard was really protecting: no merge, not a
    # plan. One fused call per source against an empty merged document is a
    # real call, billed, whose every verdict is MISSING by construction.
    broken = dict(CLEAN)
    broken["merge"] = lambda n: None
    script = Script(**broken)
    with workspace(script) as (home, base_url):
        code, _, err = invoke(home, base_url, *sweep_argv(
            home, "--verify-depth", "coverage", "--json", str(home / "r.json")))
        data = json.loads((home / "r.json").read_text(encoding="utf-8"))
    check("coverage" not in script.seen,
          f"a merge that produced nothing must not be covered against: "
          f"{script.seen}")
    steps = {s["name"]: s for s in data.get("steps", [])}
    check(steps.get("cover notes-a.md", {}).get("state") == "skipped",
          f"and the step has to say it was skipped rather than vanish: "
          f"{sorted(steps)}")


def test_a_flagged_mismatch_is_a_hint_and_never_a_finding() -> None:
    """The line the operator drew: a hint, not a failure.

    Their words: *"We should not silently accept a merge of a C# and a Java
    file even if there are no conflicts. We do not need to fail but we should
    provide a friendly hint that they probably end up doing something
    undesired."*

    Both halves are load-bearing and they pull against each other. The hint
    has to reach the reader, and it must not move the exit code -- because a
    merge of two unrelated documents can be flawless by every check this tool
    has, and scoring it as a defect would make the tool wrong about the one
    thing it is actually good at.
    """
    flagged = dict(CLEAN)
    flagged["merge"] = json.dumps({
        "merged_document": MERGED, "decisions": [], "dispositions": [],
        "mismatch": "Document 1 is C# and document 2 is Java."})

    with workspace(Script(**flagged)) as (home, base_url):
        code, out, _ = invoke(home, base_url, *sweep_argv(
            home, "--json", str(home / "r.json")))
        data = json.loads((home / "r.json").read_text(encoding="utf-8"))

    check(code == 0,
          f"the flag must not fail the run: the merge is faithful and the "
          f"warning is about the inputs, not the output; got {code}")
    check(data["mismatch"] == "Document 1 is C# and document 2 is Java.",
          f"the sentence is carried verbatim and ungraded: {data['mismatch']!r}")
    check("possibly not belonging together" in out,
          "and it reaches the reader, or the hint was not given")
    check("Document 1 is C# and document 2 is Java." in out,
          "quoted rather than paraphrased, because the sentence is the "
          "model's and nothing here checks it")
    # Guarded on the marker being there at all, so a build that suppressed the
    # hint fails on the assertion above rather than crashing here.
    after = out.split("possibly not belonging together")
    check(len(after) < 2 or "findings" not in after[1][:200].lower(),
          "and it is not presented among the findings")

    # Must-not-fire. The ordinary run is silent, and a warning that appeared
    # on every merge would be a warning nobody reads by the third one.
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, _ = invoke(home, base_url, *sweep_argv(
            home, "--json", str(home / "r2.json")))
        data = json.loads((home / "r2.json").read_text(encoding="utf-8"))
    check(data["mismatch"] == "",
          f"an unflagged merge carries the empty string, not null: "
          f"{data['mismatch']!r}")
    check("possibly not belonging together" not in out,
          "and says nothing at all")


def test_sourced_refuses_a_backend_that_cannot_retrieve_and_grants_one_that_can() -> None:
    """The safety property of the sixth level, seeded both ways.

    **Selecting `sourced` on a backend that cannot retrieve must refuse, not
    behave like `open`.** A user who picks the level that says "go and check"
    and receives recalled assertions wearing citations is worse off than one
    who picked `open`, because they believe the claims were verified -- and the
    two runs are not distinguishable from the report. That was measured: same
    pair, same model, same level, one variable, and the only difference in the
    output was that the licence was wrong without the tool and right with it,
    under citation strings that are near-identical.

    Must-fire, must-not-fire, and the automatic grant, on `config.resolve` --
    the one function both the command line and the web server reach this
    decision through.
    """
    parser = cli.build_parser()

    def at(level, command=None, window="200000", envelope=None):
        argv = ["merge", "a.md", "b.md", "--base", "a.md", "--fidelity", level]
        if command:
            argv += ["--answer-with", command]
        environ = {"LLOSSLESS_WINDOW": window}
        if envelope:
            environ["LLOSSLESS_COMMAND_ENVELOPE"] = envelope
        return config.resolve(parser.parse_args(argv), environ=environ)

    # The result envelope, which a `sourced` command must ask for:
    # it is the only answer that carries a turn count, and without one the run
    # could not say whether anything was retrieved.
    result = " " + " ".join(config.RESULT_ARGS)

    # Must fire: an HTTP endpoint has nothing this build can grant a tool to.
    refusal = raises(config.ConfigError, lambda: at("sourced"),
                     "sourced over an HTTP endpoint must refuse rather than "
                     "answering from recall and labelling it retrieved")
    check(refusal is not None and "open" in str(refusal),
          f"the refusal must name the level to use instead: {refusal}")

    # Must fire: a program whose flags this build has never read. Appending an
    # allowlist flag to it would break a working command rather than widen it.
    wrapper = raises(config.ConfigError,
                     lambda: at("sourced", "/usr/local/bin/my-wrapper.sh"),
                     "sourced through an unrecognised program must refuse")
    check(wrapper is not None and "my-wrapper.sh" in str(wrapper),
          f"and the refusal must name what it is about: {wrapper}")

    # Must not fire: the same wrapper, with the operator's own grant on it.
    # Their argv is theirs, and it is read back rather than assumed.
    own = at("sourced",
             "/usr/local/bin/my-wrapper.sh --allowed-tools WebFetch" + result,
             envelope=config.ENVELOPE_RESULT)
    check(config.granted_web_tools(own.command) == ("WebFetch",),
          f"an operator's own grant satisfies the level: {own.command!r}")

    # Must fire: granted, and answering in plain text. The run could
    # retrieve and could never say whether it had, so every report through it
    # would print "unmeasured" under citations that read as checked.
    for silent in ("/usr/local/bin/my-wrapper.sh --allowed-tools WebFetch",
                   "/opt/claude-cli/bin/claude --print --model sonnet"):
        blind = raises(config.ConfigError, lambda: at("sourced", silent),
                       f"sourced through a command that reports no turn count "
                       f"must refuse: {silent}")
        check(blind is not None and "turn count" in str(blind)
              and " ".join(config.RESULT_ARGS) in str(blind)
              and "open" in str(blind),
              f"and say what is missing, what to add, and the level to use "
              f"instead: {blind}")
        check(config.sourced_tools(silent) == (),
              f"and a route row must not advertise retrieval on it: {silent}")
        # Must not fire: the same command at every other level still runs.
        for level in config.FIDELITY_LEVELS:
            if level != config.SOURCED:
                at(level, silent)

    # Must not fire: every level below it, on the backend that refused above.
    for level in config.FIDELITY_LEVELS:
        if level == config.SOURCED:
            continue
        settings = at(level)
        check(config.granted_web_tools(settings.command) == (),
              f"{level} must be granted nothing: {settings.command!r}")

    # The automatic grant, and it lands on the command the run will execute.
    #
    # Not a home directory path, deliberately, though that is where this CLI
    # really installs. `scan_release`'s home-path detector registers a
    # made-up one as a shape that must fire, so a fictional home directory
    # here is a seeded positive for the leak scan rather than a realistic
    # fixture -- and this comment does not spell one either, for the reason
    # the detector's own file is exempt. Only the basename is load-bearing,
    # `AUTO_GRANT` being keyed by it, so any absolute path tests the same
    # thing.
    granted = at("sourced",
                 "/opt/claude-cli/bin/claude --print --model sonnet" + result,
                 envelope=config.ENVELOPE_RESULT)
    check(config.granted_web_tools(granted.command) == ("WebSearch", "WebFetch"),
          f"a recognised program is granted both web tools automatically: "
          f"{granted.command!r}")
    # As one argument, comma-separated. `--allowed-tools` takes a list, so a
    # second word after it would be read as a tool name by the CLI, and the
    # comma form is the one measured to work through 2.1.274.
    argv = granted.command.split()
    check(argv[argv.index(config.ALLOW_TOOLS_FLAG) + 1:] == ["WebSearch,WebFetch"],
          f"the grant is one comma-separated argument at the end of the argv: "
          f"{granted.command!r}")
    check(granted.command.startswith("/opt/claude-cli/bin/claude --print"),
          f"and the operator's own argv is kept in front of it: "
          f"{granted.command!r}")

    # Applied once however often it is resolved. The web path reaches
    # `config.resolve` with a route's command already in the environment, so a
    # grant that appended per call would grow one flag per resolution.
    again = config.resolve(
        parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md",
                           "--fidelity", "sourced"]),
        environ={"LLOSSLESS_WINDOW": "200000",
                 "LLOSSLESS_COMMAND": granted.command,
                 "LLOSSLESS_COMMAND_ENVELOPE": config.ENVELOPE_RESULT})
    check(again.command == granted.command,
          f"the grant must be idempotent: {again.command!r}")

    # And the same program below `sourced` is granted nothing at all, which is
    # what every route did before this level existed.
    plain = at("open", "/opt/claude-cli/bin/claude --print --model sonnet")
    check(config.ALLOW_TOOLS_FLAG not in plain.command,
          f"the grant belongs to the level, not to the program: "
          f"{plain.command!r}")


def test_a_known_subscription_cli_is_asked_for_the_effort_level_it_was_measured_at() -> None:
    """Per role. Reasoning is the cost, so the level is set for it.

    `AUTO_EFFORT` is `AUTO_GRANT`'s sibling and this is that test's sibling:
    the same three refusals, plus the one this table adds -- an operator who
    named a level keeps it. The measurement behind the figures is in
    `config.AUTO_EFFORT`'s own comment; this holds the mechanism only.

    **Read off the argv each role will really execute**, never off the table.
    `retrieval.permitted`'s direction, and for its reason: a test that asked
    `AUTO_EFFORT` what it holds would pass on a build that never appended
    anything, which is exactly the failure a per-role split can have.

    The absolute path is fictional for the reason the grant test's is, and
    only its basename is load-bearing.
    """
    parser = cli.build_parser()

    def at(command=None, level="open", extra=(), environ=None):
        argv = ["merge", "a.md", "b.md", "--base", "a.md", "--fidelity", level]
        if command:
            argv += ["--answer-with", command]
        return config.resolve(parser.parse_args([*argv, *extra]),
                              environ={"LLOSSLESS_WINDOW": "200000",
                                       **(environ or {})})

    # Must fire, and differently per role. The merge writes the document and
    # declares every correction; `decompose` and `verify` read its work back
    # and the measured `low` is what they keep, so the 3.3x is paid on one call of
    # six rather than on all of them.
    known = at("/opt/claude-cli/bin/claude --print --model sonnet")
    for role, level in (("merge", "medium"), ("decompose", "low"), ("verify", "low")):
        argv = known.command_for(role)
        check(argv.endswith(f"{config.EFFORT_FLAG} {level}"),
              f"{role} must execute at {level}, read off its own argv: {argv!r}")
        check(known.effort_for(role) == level,
              f"and the run must report {role} at {level}: {known.effort_for(role)!r}")
    check(known.command_for("merge") != known.command_for("verify"),
          f"the split has to reach the argv or it is a table nobody read: "
          f"{known.command_for('merge')!r}")
    # The speed half of that measurement, pinned against a later edit that raises one level
    # and quietly raises all three: `decompose` and `verify` stay where the
    # measurement left them.
    check(config.AUTO_EFFORT["claude"]["decompose"] == "low"
          and config.AUTO_EFFORT["claude"]["verify"] == "low",
          f"the measured speed-up is undone if these move: {config.AUTO_EFFORT}")

    # Must not fire: an HTTP endpoint. There is no command to put a flag on,
    # and `effort_for` answering "" is what lets the provenance block leave
    # the key out rather than claim a level about a run that has none.
    over_http = at()
    check(not over_http.command
          and not any(over_http.effort_for(role) for role in config.ROLES),
          f"an HTTP endpoint has no effort to report: {over_http.command!r}")

    # Must not fire: a program whose flags this build has never read.
    wrapper = at("/usr/local/bin/my-wrapper.sh --print")
    check(all(config.EFFORT_FLAG not in wrapper.command_for(role)
              for role in config.ROLES),
          f"an unrecognised program keeps the argv it was given: "
          f"{wrapper.command_for('merge')!r}")

    # Must not fire: the operator said `max`, so `max` is what every role
    # runs at. Both spellings, because a shell accepts both and a reader that
    # knew one would silently overwrite the other. This is the precedence
    # rule the grant set, held on the per-role axis added later: a level the
    # operator wrote beats the automatic one, and beats it for all three
    # roles rather than for the two the table happens to agree with.
    for written in (f"{config.EFFORT_FLAG} max", f"{config.EFFORT_FLAG}=max"):
        theirs = at(f"/opt/claude-cli/bin/claude --print {written}")
        for role in config.ROLES:
            check(theirs.effort_for(role) == "max",
                  f"an operator's own level is never overwritten, and {role} "
                  f"got {theirs.effort_for(role)!r}: {theirs.command!r}")
            check(theirs.command_for(role).count(config.EFFORT_FLAG) == 1,
                  f"and nothing is appended beside it for {role}: "
                  f"{theirs.command_for(role)!r}")

    # Applied once however often it is resolved, for the reason the grant is:
    # the web path reaches `resolve` with a route's command in the environment.
    # Per role now, so the idempotence has to hold on each of the three argvs
    # rather than on one -- a second application that read the role's own
    # command back would append `--effort high --effort high`.
    for role in config.ROLES:
        again = config.resolve(
            parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md"]),
            environ={"LLOSSLESS_WINDOW": "200000",
                     "LLOSSLESS_COMMAND": known.command_for(role)})
        check(again.command_for(role) == known.command_for(role),
              f"the effort level must be idempotent for {role}: "
              f"{again.command_for(role)!r}")

    # Every level this build would ever write has to be one the binary
    # documents. A typo here is a flag refused on every call of every run.
    check(all(level in config.EFFORT_LEVELS
              for table in config.AUTO_EFFORT.values()
              for level in table.values()),
          f"AUTO_EFFORT must name levels the CLI takes: {config.AUTO_EFFORT}")


def test_an_effort_the_operator_states_beats_the_one_this_build_would_pick() -> None:
    """The override the effort table did not have, and the precedence that makes it one.

    The operator asked to raise effort for quality and could not: `AUTO_EFFORT`
    was hardcoded and the only way past it was to edit the route's command
    string. Three surfaces answer that now -- a flag, a run-wide variable and a
    per-role one -- and all three have to beat the table or they are decoration.

    Every case below is read off `command_for`, the argv the call will really
    be made with, rather than off `Settings.effort`, which is only what was
    asked for.
    """
    parser = cli.build_parser()
    known = "/opt/claude-cli/bin/claude --print --model sonnet"

    def at(extra=(), environ=None):
        argv = ["merge", "a.md", "b.md", "--base", "a.md",
                "--answer-with", known, *extra]
        return config.resolve(parser.parse_args(argv),
                              environ={"LLOSSLESS_WINDOW": "200000",
                                       **(environ or {})})

    # A bare level on the flag covers every role. This is the operator's
    # original ask -- "more effort, please" -- and it must not require them to
    # know the role names.
    every = at(["--effort", "xhigh"])
    for role in config.ROLES:
        check(every.command_for(role).endswith(f"{config.EFFORT_FLAG} xhigh"),
              f"--effort xhigh must reach {role}'s argv: "
              f"{every.command_for(role)!r}")

    # `ROLE=LEVEL` names one role and leaves the rest on the table's levels,
    # which is the shape that makes the split adjustable without a code edit.
    one = at(["--effort", "verify=max"])
    check(one.command_for("verify").endswith(f"{config.EFFORT_FLAG} max"),
          f"--effort verify=max must reach verify: {one.command_for('verify')!r}")
    check(one.effort_for("merge") == config.AUTO_EFFORT["claude"]["merge"],
          f"and must leave merge on the table: {one.effort_for('merge')!r}")

    # Both spellings on one flag, later wins: a floor for everything and an
    # exception to it, in the order they were written.
    mixed = at(["--effort", "low", "--effort", "merge=max"])
    check((mixed.effort_for("merge"), mixed.effort_for("verify")) == ("max", "low"),
          f"a bare level and a named one compose in order: "
          f"{[mixed.effort_for(r) for r in config.ROLES]}")

    # The environment, run-wide and per role, on `LLOSSLESS_WINDOW`'s terms:
    # the general statement is the floor and the specific one overrides it.
    env = at(environ={"LLOSSLESS_EFFORT": "medium",
                      "LLOSSLESS_EFFORT_MERGE": "max"})
    check((env.effort_for("merge"), env.effort_for("decompose")) == ("max", "medium"),
          f"the per-role variable overrides the run-wide one: "
          f"{[env.effort_for(r) for r in config.ROLES]}")

    # Flag over environment, which is this file's rule for every other setting.
    both = at(["--effort", "merge=low"], {"LLOSSLESS_EFFORT_MERGE": "max"})
    check(both.effort_for("merge") == "low",
          f"the flag beats the variable: {both.effort_for('merge')!r}")

    # And the top of the chain: a level in the operator's own argv beats all
    # three surfaces, because that argv is theirs and appending beside it
    # would silently win on a repeated flag (`stated_effort`'s last-wins rule).
    theirs = at(["--effort", "low"], {"LLOSSLESS_EFFORT": "medium"})
    theirs = config.resolve(
        parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md",
                           "--answer-with", f"{known} --effort xhigh",
                           "--effort", "low"]),
        environ={"LLOSSLESS_WINDOW": "200000", "LLOSSLESS_EFFORT": "medium"})
    for role in config.ROLES:
        check(theirs.effort_for(role) == "xhigh",
              f"a level in the operator's own command wins for {role}: "
              f"{theirs.effort_for(role)!r}")
        check(theirs.command_for(role).count(config.EFFORT_FLAG) == 1,
              f"and nothing is appended beside it: {theirs.command_for(role)!r}")

    # A level this build cannot deliver is dropped and said out loud rather
    # than refused: `LLOSSLESS_EFFORT` exported in a shell must not break
    # every HTTP run in it.
    http = config.resolve(
        parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md"]),
        environ={"LLOSSLESS_WINDOW": "200000", "LLOSSLESS_EFFORT": "max"})
    check(http.effort_ignored == config.ROLES,
          f"an HTTP endpoint cannot carry a level and has to say so: "
          f"{http.effort_ignored}")
    wrapper = at(["--effort", "max"])
    wrapper = config.resolve(
        parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md",
                           "--answer-with", "/usr/local/bin/my-wrapper.sh",
                           "--effort", "max"]),
        environ={"LLOSSLESS_WINDOW": "200000"})
    check(wrapper.effort_ignored == config.ROLES
          and config.EFFORT_FLAG not in wrapper.command_for("merge"),
          f"a program whose flags this build has not read is not guessed at: "
          f"{wrapper.command_for('merge')!r}")

    # A typo is refused with the half that was wrong named, not with the
    # product of roles and levels argparse `choices` would have printed.
    for bad, want in (("hgih", "level"), ("merge=hgih", "level"),
                      ("mrege=high", "role")):
        try:
            at(["--effort", bad])
        except config.ConfigError as exc:
            check(want in str(exc), f"--effort {bad} must say which half: {exc}")
        else:
            check(False, f"--effort {bad} was accepted")


def test_the_dry_run_plan_states_the_batch_the_backend_will_really_send() -> None:
    """An earlier fix gave a command backend its own batch and left this saying 25.

    The plan's one number. An operator reading `covers 25 claims` and then
    watching two calls cover 180 has been told the wrong unit by the only
    sentence on the page that offers one.
    """
    parser = cli.build_parser()
    argv = ["merge", "a.md", "b.md", "--base", "a.md", "--verify-depth", "full"]

    over_http = config.resolve(parser.parse_args(argv), environ={})
    through_a_command = config.resolve(
        parser.parse_args([*argv, "--answer-with", "/opt/claude-cli/bin/claude --print"]),
        environ={"LLOSSLESS_WINDOW": "200000"})
    check(over_http.verify_batch == config.DEFAULT_VERIFY_BATCH
          and through_a_command.verify_batch == config.COMMAND_VERIFY_BATCH
          and over_http.verify_batch != through_a_command.verify_batch,
          f"the two backends must resolve different batches, or this test "
          f"proves nothing: {over_http.verify_batch} and "
          f"{through_a_command.verify_batch}")

    for settings in (over_http, through_a_command):
        run = report.Run(command="merge")
        run.provenance = Provenance(settings=settings, client=Client(settings),
                                    roles=cli.ROLES, duration_seconds=0.0)
        run.steps = [report.Step("merge", report.PLANNED)]
        text = report.dry_run_section(run)
        check(f"covers {settings.verify_batch} claims" in text,
              f"the plan must state this run's own batch: {text!r}")
        page = "\n".join(html_report.planned_block(run))
        check(f"covers {settings.verify_batch} claims" in page,
              f"and the HTML plan the same: {page!r}")


def test_a_command_and_an_envelope_that_disagree_are_refused_on_the_command_line() -> None:
    """The rule `web/commands._row` holds on a route, on the other way in.

    Two ways to a command backend, one of them guarded. A command carrying
    `--output-format json` whose envelope is left at the `raw` default parses
    the result envelope *as* the answer, fails the schema, and burns every
    repair attempt before erroring -- measured once, on a six-call run against
    a real subscription. The web server has refused exactly this already;
    the command line had nothing.

    Driven through `cli.main`, not only through `config.resolve`: the function
    was never the gap. Both directions, because an envelope is a parser
    selection and the wrong one is a defect whichever way the pair disagrees.
    """
    parser = cli.build_parser()

    def at(command, envelope=None, window="200000"):
        argv = ["merge", "a.md", "b.md", "--base", "a.md"]
        if command:
            argv += ["--answer-with", command]
        environ = {"LLOSSLESS_WINDOW": window}
        if envelope:
            environ["LLOSSLESS_COMMAND_ENVELOPE"] = envelope
        return config.resolve(parser.parse_args(argv), environ=environ)

    # Must fire, the direction that cost the run: the command answers in an
    # envelope and nothing said so.
    raw = raises(config.ConfigError,
                 lambda: at("/bin/true --print --output-format json"),
                 "a command that answers in an envelope must not be read raw")
    said = str(raw)
    check("LLOSSLESS_COMMAND_ENVELOPE=result" in said,
          f"the refusal must name the fix, not the mechanism: {said}")
    check(config.RESULT_FORMAT_FLAG in said,
          f"and the half of the disagreement that is in the command: {said}")

    # Must fire the other way: an envelope declared over a command that writes
    # its answer as text. There is nothing to unwrap.
    declared = raises(config.ConfigError,
                      lambda: at("/bin/true --print", envelope="result"),
                      "an envelope nothing produces must not be declared")
    check("--output-format json" in str(declared),
          f"the refusal must name what the command is missing: {declared}")

    # Must not fire: both halves agreeing, either way round, and the separated
    # spelling as well as the joined one.
    for command, envelope in (
            ("/bin/true --print", None),
            ("/bin/true --print", "raw"),
            ("/bin/true --print --output-format json", "result"),
            ("/bin/true --print --output-format=json", "result"),
            # `stream-json` is a sequence of objects and not this envelope, so
            # `raw` is the honest reading of it rather than an oversight.
            ("/bin/true --print --output-format stream-json", None)):
        at(command, envelope)

    # Must not fire at all without a command: an HTTP endpoint has no argv for
    # the variable to disagree with.
    at(None, envelope="result")

    # And the whole of it on the command line, where the six calls were spent.
    # The refusal has to land before the first one, so the endpoint must see
    # no request at all.
    with workspace(Script(**CLEAN)) as (home, base_url):
        code, out, err = invoke(
            home, base_url, "merge", "notes-a.md", "notes-b.md",
            "--answer-with", "/bin/true --print --output-format json",
            "--window", "200000")
    check(code != 0, f"the run must refuse rather than start: exit {code}")
    check("LLOSSLESS_COMMAND_ENVELOPE=result" in (out + err),
          f"and say what to set: {(out + err)[-400:]}")


def answering_program(home: Path, ran: Path) -> str:
    """A command backend that answers as `CLEAN` does, and logs each start to `ran`.

    The same replies the scripted HTTP endpoint gives, chosen by the same
    markers, so a run through it is a complete clean run on the other backend.
    """
    program = home / "answer.py"
    # The child imports this module for `Script`, and this module's socket
    # guard resolves the environment -- where a caller may have put a command
    # with no window. The program is the command, not a run, so it takes the
    # variable out of its own copy.
    program.write_text(
        "import json, os, sys\n"
        "os.environ.pop('LLOSSLESS_COMMAND', None)\n"
        f"sys.path[:0] = [{str(ROOT / 'tests')!r}, {str(ROOT / 'src')!r}]\n"
        f"open({str(ran)!r}, 'a').write('x\\n')\n"
        "from test_cli import CLEAN, Script\n"
        "content = sys.stdin.read()\n"
        "kind = Script().kind(content)\n"
        "reply = CLEAN[kind]\n"
        "reply = reply(1) if callable(reply) else reply\n"
        "sys.stdout.write(Script.answering_the_schema(kind, content, reply))\n",
        encoding="utf-8")
    return f"{sys.executable} {program}"


def test_a_report_with_the_cache_off_carries_each_calls_wall_time() -> None:
    """`--no-cache` left no cassette, and the report said nothing per call.

    A finished run could say it took 1,585 s over 13 calls and not which of
    the thirteen, so every timing measured on 2026-09-23 was taken by hand.
    `latency_ms` is now on each live ledger row in `report.json`, over HTTP
    and through a command, and it is the call's own time: every row's figure
    fits inside the run's duration, and together they do not exceed it by
    more than the report's rounding of that duration.
    """
    with workspace(Script(**CLEAN)) as (home, base_url):
        command = answering_program(home, home / "ran.log")
        for backend, extra in (("http", ()),
                               ("command", ("--answer-with", command,
                                            "--window", "200000"))):
            report = home / f"{backend}.json"
            code, _, err = invoke(
                home, base_url, "merge", str(home / "notes-a.md"),
                str(home / "notes-b.md"), "--json", str(report),
                "-o", str(home / f"{backend}.md"), *extra)
            check(code == 0, f"{backend}: the run must succeed: exit {code}, "
                             f"{err.strip()[-300:]!r}")
            if not report.exists():
                continue
            block = json.loads(report.read_text(encoding="utf-8"))["provenance"]
            # `capabilities.json` is the tier record, written whatever the
            # cache says; anything else under the cache would be a cassette.
            tapes = [path.name for path in (home / "cache").rglob("*.json")
                     if path.name != "capabilities.json"]
            check(not tapes,
                  f"{backend}: --no-cache must leave no cassette, or this proves "
                  f"nothing about the report being the only record: {tapes}")
            times = [row.get("latency_ms") for row in block["ledger"]]
            check(len(times) == block["counts"]["calls"] and times
                  and all(isinstance(ms, int) and ms >= 0 for ms in times),
                  f"{backend}: every live call's row carries its wall time: {times}")
            # The report rounds the run's duration to 0.1 s (`provenance`), so
            # the true figure can be up to 50 ms above the one recorded, and
            # six serial calls to a subprocess add up to about a second.
            spent = block["duration_seconds"] * 1000
            check(sum(ms for ms in times if isinstance(ms, int)) <= spent + 50,
                  f"{backend}: the calls cannot have taken longer than the run: "
                  f"{times} against {spent:.0f} ms, recorded to the nearest 100")


def test_window_states_the_window_for_either_spelling_of_the_command() -> None:
    """`--window` rescues `LLOSSLESS_COMMAND` as it rescues `--answer-with`.

    Measured before the fix: `--answer-with PROGRAM --window 200000` ran, and
    `LLOSSLESS_COMMAND=PROGRAM` with the same `--window 200000` refused with
    the sentence telling the operator to pass `--window`. `Settings.__post_init__`
    refuses a command with no window, and `from_env` built a `Settings` from the
    environment alone before the flag was read.

    Through `cli.main` with a program that really answers, not through
    `config.resolve` alone: the defect was in the order the command line reads
    its two sources, and a complete run is the evidence that the window reached
    every role. Both spellings must end in the same report; both must still
    refuse with no window at all, and before the program is started.
    """
    names = ("LLOSSLESS_COMMAND", "LLOSSLESS_WINDOW",
             *(f"LLOSSLESS_WINDOW_{role.upper()}" for role in config.ROLES))
    saved = {name: os.environ.pop(name, None) for name in names}
    reports: dict[str, dict] = {}
    try:
        with workspace(Script(**CLEAN)) as (home, base_url):
            ran = home / "ran.log"
            command = answering_program(home, ran)
            for spelling in ("--answer-with", "LLOSSLESS_COMMAND"):
                for window in ("200000", None):
                    report = home / f"{spelling}-{window}.json"
                    argv = ["merge", str(home / "notes-a.md"), str(home / "notes-b.md"),
                            "--json", str(report), "-o", str(home / "merged.md")]
                    if window:
                        argv += ["--window", window]
                    if spelling == "--answer-with":
                        argv += ["--answer-with", command]
                    else:
                        os.environ["LLOSSLESS_COMMAND"] = command
                    before = ran.read_text(encoding="utf-8") if ran.exists() else ""
                    try:
                        code, out, err = invoke(home, base_url, *argv)
                    finally:
                        os.environ.pop("LLOSSLESS_COMMAND", None)
                    started = (ran.read_text(encoding="utf-8") if ran.exists()
                               else "") != before
                    if window:
                        check(code == 0, f"{spelling} with --window must run: "
                                         f"exit {code}, {err.strip()[-300:]!r}")
                        if report.exists():
                            reports[spelling] = json.loads(
                                report.read_text(encoding="utf-8"))
                    else:
                        check(code != 0 and "LLOSSLESS_WINDOW" in err,
                              f"{spelling} with no window must still refuse, "
                              f"naming the fix: exit {code}, {err.strip()[-300:]!r}")
                        check(not started, f"{spelling}: the refusal must land "
                                           f"before the program is started")
    finally:
        for name, value in saved.items():
            if value is not None:
                os.environ[name] = value

    check(sorted(reports) == ["--answer-with", "LLOSSLESS_COMMAND"],
          f"both spellings must produce a report; got {sorted(reports)}")
    if len(reports) != 2:
        return
    for spelling, data in reports.items():
        windows = data["provenance"].get("window") or {}
        check(sorted(windows) == sorted(config.ROLES)
              and all("200000" in said for said in windows.values()),
              f"{spelling}: every role must carry the stated window: {windows}")
    # The clock, the output path, and each ledger row's stopwatch: two
    # live runs of one program do not take the same milliseconds, and that is
    # not the two spellings disagreeing. The split of that time and the run's
    # time accounting blocks are stopwatches too.
    volatile = ("generated_at", "duration_seconds", "answering_seconds",
                "excluded", "discarded_calls", "unruled")
    stopwatches = ("latency_ms", "attempts", "answer_ms", "failed_ms",
                   "waited_ms", "ttfb_ms", "cli_duration_ms", "cli_duration_api_ms")
    flag, env = (dict(reports[s]) for s in ("--answer-with", "LLOSSLESS_COMMAND"))
    for data in (flag, env):
        data.pop("merged_written_to", None)
        data["provenance"] = {key: value for key, value in data["provenance"].items()
                              if key not in volatile}
        data["provenance"]["ledger"] = [
            {k: v for k, v in row.items() if k not in stopwatches}
            for row in data["provenance"].get("ledger") or []]
    differing = sorted(key for key in set(flag) | set(env) if flag.get(key) != env.get(key))
    check(not differing, f"the two spellings must be one setting; the reports "
                         f"differ on {', '.join(differing)}")


def test_the_verify_batch_is_the_backends_and_the_http_figure_does_not_move() -> None:
    """Fewer, larger calls on the backend whose per-call cost is fixed.

    The operator's report: *"it ran extremely long for almost half an hour.
    That is unacceptably slow."* Measured: 1,585 s over 13 calls on 6 KB of
    document -- one merge, four decompose and **eight verify**, which is
    `ceil(90/25)` forward plus `ceil(90/25)` back. The documents are not the
    problem, the call count is, and a command backend pays a near-fixed cost
    per call: a six-word prompt through that CLI reported 16,586
    cache-creation tokens.

    **The HTTP figure must not move**, and that is the half with teeth. Batch
    size reaches `messages`, `messages` is a cassette-key component, and all
    334 recorded verify cassettes were made at 25 -- raising it globally would
    orphan the corpus every published figure here comes from.

    Seeded by making the two equal, which is the state this exists to refuse.
    """
    settings = config.resolve(cli.build_parser().parse_args(
        ["merge", "a.md", "b.md", "--base", "a.md"]),
        environ={"LLOSSLESS_WINDOW": "8192"})
    check(settings.verify_batch == 25,
          f"the HTTP batch is 25 and is what the corpus was recorded at: "
          f"{settings.verify_batch}")
    check(verify.DEFAULT_BATCH == 25,
          f"and the name the recording harnesses pass still means 25: "
          f"{verify.DEFAULT_BATCH}")

    through = dataclasses.replace(settings, command="/usr/bin/claude --print")
    check(through.verify_batch > settings.verify_batch,
          f"a command backend must batch larger, or the lever does nothing: "
          f"{through.verify_batch} against {settings.verify_batch}")
    check(through.verify_batch == config.COMMAND_VERIFY_BATCH,
          f"and it must be the stated figure rather than a computed one: "
          f"{through.verify_batch}")

    # The arithmetic the figure was chosen against: the operator's run, both
    # ways. Written as the ceiling division the pipeline really does.
    def calls(claims, batch):
        return -(-claims // batch)

    check(calls(90, settings.verify_batch) * 2 == 8,
          "the measured run is eight verify calls at the HTTP figure")
    check(calls(90, through.verify_batch) * 2 == 2,
          f"and two through a command, which is what the figure was picked "
          f"for: {calls(90, through.verify_batch) * 2}")

    # Seeded: equal figures mean the command backend gained nothing.
    check(config.COMMAND_VERIFY_BATCH != config.DEFAULT_VERIFY_BATCH,
          "seeded check: the two figures are equal, so this whole check is "
          "comparing a value with itself")


ATTRIBUTION_FIXTURE = ROOT / "tests" / "fixtures" / "attribution_invented"


def _spanned(*rows: tuple[str, int, str]) -> str:
    """A decompose payload whose spans are the document's own text."""
    return json.dumps({"claims": [{"text": text, "line": line, "span": span}
                                  for text, line, span in rows]})


def _attribution_script() -> Script:
    """What both benchmark models did with `attribution_invented`, as a script.

    An earlier fixture quotes the claims those runs formed: the attribution clause is gone,
    `M-004` reads "The minimum TLS version is 1.2.", and every verdict is
    SUPPORTED because every claim it was asked about is. So the model half of
    this run is correct and blind, exactly as it was live, and whatever finds
    the plant here has to be the half that needs no model.
    """
    port = ("The relay listens on port 8443.", 3, "The relay listens on port 8443.")
    timeout = ("The read timeout is 30 seconds.", 4, "The read timeout is 30 seconds.")
    health = ("The health check path is /healthz.", 5, "The health check path is /healthz.")
    tls_b = ("The minimum TLS version is 1.2.", 4, "The minimum TLS version is 1.2.")
    cap_b = ("The maximum concurrent connections is 512.", 5,
             "The maximum concurrent connections is 512.")
    by_document = {1: (port, timeout, health), 2: (port, tls_b, cap_b)}
    merged = (port, timeout, health,
              ("The minimum TLS version is 1.2.", 6, "the minimum TLS version is 1.2."),
              ("The maximum concurrent connections is 512.", 7,
               "The maximum concurrent connections is 512."))

    def decompose(n):
        return _spanned(*(by_document.get(n) or merged))

    def covered(n):
        return _coverage(*[(text, line, span, "SUPPORTED",
                            text if text != tls_b[0] else "the minimum TLS version is 1.2")
                           for text, line, span in by_document[n]])

    in_merge = {"A-001": port[0], "A-002": timeout[0], "A-003": health[0],
                "B-001": port[0], "B-002": "the minimum TLS version is 1.2",
                "B-003": cap_b[0]}
    in_sources = (("M-001", port[0], "source_a.md"), ("M-002", timeout[0], "source_a.md"),
                  ("M-003", health[0], "source_a.md"), ("M-004", tls_b[0], "source_b.md"),
                  ("M-005", cap_b[0], "source_b.md"))
    return Script(
        merge=None,
        decompose=decompose,
        coverage=covered,
        forward=verdicts(*[(claim, "SUPPORTED", text, "merged.md")
                           for claim, text in in_merge.items()]),
        reverse=verdicts(*[(claim, "SUPPORTED", text, source)
                           for claim, text, source in in_sources]),
    )


def test_attribution_invented_is_detected_at_both_depths() -> None:
    """The acceptance test is the fixture, graded by the registered detector.

    `llossless verify` over `tests/fixtures/attribution_invented/` as an
    operator runs it, at `full` and at `coverage`, with the model half scripted
    to do what both benchmark models did live. The report is then graded by
    `run_detect.grade` -- the function every published detection figure went
    through -- against the fixture's own `expected.json`, which is untouched.

    Must fire: the fixture matches at both depths, `m-tls-attributed` is
    detected, nothing is invented, and the exit status is the registered 1.
    Before this fix the same script exited 0 at both depths with the probe missed.

    Must not fire: the same run with one thing varied -- the merged sentence
    credits the TLS minimum to the Deployment Notes, which do state it -- is
    clean. Everything else, the script included, is held constant, so the
    difference between the two is the attribution and nothing else.
    """
    import run_detect

    expected = json.loads((ATTRIBUTION_FIXTURE / "expected.json").read_text(encoding="utf-8"))
    planted_text = (ATTRIBUTION_FIXTURE / "merged.md").read_text(encoding="utf-8")
    honest_text = planted_text.replace("According to the Operator Guide",
                                       "According to the Deployment Notes")
    check(honest_text != planted_text, "the control must differ from the plant")

    for depth in config.VERIFY_DEPTHS:
        for label, merged_text in (("planted", planted_text), ("control", honest_text)):
            with workspace(_attribution_script()) as (home, base_url):
                for name in ("source_a.md", "source_b.md"):
                    (home / name).write_text(
                        (ATTRIBUTION_FIXTURE / name).read_text(encoding="utf-8"),
                        encoding="utf-8")
                (home / "merged.md").write_text(merged_text, encoding="utf-8")
                code, out, err = invoke(
                    home, base_url, "verify", str(home / "source_a.md"),
                    str(home / "source_b.md"), str(home / "merged.md"),
                    "--verify-depth", depth, "--json", str(home / "r.json"),
                    "--html", str(home / "r.html"))
                data = json.loads((home / "r.json").read_text(encoding="utf-8"))
                page = (home / "r.html").read_text(encoding="utf-8")
            # Every surface an operator reads, from the one run: the verdict
            # (Markdown and HTML share it), the section, the cards, the terminal.
            said = {
                "verdict": "In the attributions: 1 " + report.MISATTRIBUTED_WORDS in out,
                "section": "## Attributions" in out,
                "cards": page.count('data-kind="misattributed"') == 1,
                "terminal": report.MISATTRIBUTED_WORDS in strip(err),
            }
            graded = run_detect.grade(expected, data, code)
            where = f"{label} at {depth}"
            check(data["attributions"]["ran"] is True,
                  f"{where}: the attribution check must run on verify: "
                  f"{data['attributions']}")
            if label == "planted":
                check(graded["outcome"] == "matched" and code == 1,
                      f"{where}: the fixture must match its registered exit 1: "
                      f"code {code}, outcome {graded['outcome']}; {err[-300:]!r}")
                check(graded["detected"] == ["m-tls-attributed"],
                      f"{where}: the plant must be detected: {graded['probes']}")
                check(not graded["invented_findings"] and not graded["guard_wrong"],
                      f"{where}: and nothing invented or falsely alarmed: "
                      f"{graded['invented_findings']} {graded['guard_wrong']}")
                check(len(data["attributions"]["findings"]) == 1,
                      f"{where}: one finding, on the one planted sentence: "
                      f"{data['attributions']['findings']}")
                check(all(said.values()),
                      f"{where}: every surface must say it: {said}")
            else:
                check(code == 0 and not data["attributions"]["findings"],
                      f"{where}: a correct attribution must not fire: code "
                      f"{code}, {data['attributions']['findings']}")
                check(not any(said.values()),
                      f"{where}: and no surface may mention it: {said}")



# The subscription CLI's isolation: `--safe-mode`, and `--tools` naming
# exactly the web tools the argv grants. Read off the argv a call executes,
# split here with `shlex` rather than through the readers under test, so a
# reader that agreed with a broken writer could not pass these.
def _flag_value(argv: list[str], flag: str) -> str | None:
    """The word after `flag` in `argv`, or None where the flag is absent."""
    return argv[argv.index(flag) + 1] if flag in argv else None


def _isolated_as_measured(command: str, web: str) -> bool:
    """One `--safe-mode`, one `--tools`, and that `--tools` names `web`."""
    import shlex
    argv = shlex.split(command)
    return (argv.count(config.SAFE_MODE_FLAG) == 1
            and argv.count(config.TOOLS_FLAG) == 1
            and _flag_value(argv, config.TOOLS_FLAG) == web)


def test_a_claude_route_runs_in_safe_mode_with_only_the_granted_tools() -> None:
    """Every level, every role, through `resolve` and `command_for`.

    `--safe-mode` on every call, and `--tools` naming `WebSearch,WebFetch` at
    `sourced` and nothing at any other level. Seeded against the shipped code:
    with `config.ISOLATED` emptied, as before the fix, the same detector must
    fire on every call. The absolute path is fictional for the grant test's
    reason; only the basename is load-bearing.
    """
    import shlex
    parser = cli.build_parser()
    route = ("/opt/claude-cli/bin/claude --print --model sonnet "
             + " ".join(config.RESULT_ARGS))
    web = ",".join(config.AUTO_GRANT["claude"])

    def at(level, command=route, extra=()):
        return config.resolve(
            parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md",
                               "--fidelity", level, "--answer-with", command,
                               *extra]),
            environ={"LLOSSLESS_WINDOW": "200000",
                     "LLOSSLESS_COMMAND_ENVELOPE": config.ENVELOPE_RESULT})

    def every_call_isolated() -> list[str]:
        wrong = []
        for level in config.FIDELITY_LEVELS:
            settings = at(level)
            wanted = web if level == config.SOURCED else ""
            for role in config.ROLES:
                argv = settings.command_for(role)
                if not _isolated_as_measured(argv, wanted):
                    wrong.append(f"{level}/{role}: {argv!r}")
        return wrong

    wrong = every_call_isolated()
    check(not wrong, f"every call must run in safe mode with only the granted "
                     f"web tools: {wrong[:3]}")

    # The effort level is still the last flag, and `command` is still the
    # route plus the grant: the isolation is per call, so a sweep that
    # re-levels `command` never meets a `--tools` it would read as the
    # operator's.
    settings = at("open")
    for role in config.ROLES:
        argv = shlex.split(settings.command_for(role))
        check(argv[-2] == config.EFFORT_FLAG,
              f"{role}: the effort level stays last: {argv!r}")
    check(config.TOOLS_FLAG not in settings.command
          and config.SAFE_MODE_FLAG not in settings.command,
          f"the route itself must not carry the isolation: {settings.command!r}")

    # What the report says was permitted is what the call really got.
    for level in config.FIDELITY_LEVELS:
        settings = at(level)
        for role in config.ROLES:
            check(config.granted_web_tools(settings.command)
                  == config.granted_web_tools(settings.command_for(role)),
                  f"{level}/{role}: `retrieval.permitted` reads `command`, "
                  f"and must equal what the executed argv grants")

    # Idempotent: an argv that already carries both flags comes back as it is,
    # and resolving it again appends nothing.
    once = at(config.SOURCED).command_for("merge")
    check(config.command_with_isolation(once) == once,
          f"applying the isolation twice must append once: {once!r}")
    again = at(config.SOURCED, once)
    check(again.command_for("merge") == once,
          f"and a resolved argv resolved again is unchanged: "
          f"{again.command_for('merge')!r}")

    # Seeded: the shipped code with the program table emptied is the code
    # before this fix, and the detector must see every call as unisolated.
    shipped = config.ISOLATED
    try:
        config.ISOLATED = frozenset()
        seeded = every_call_isolated()
    finally:
        config.ISOLATED = shipped
    check(len(seeded) == len(config.FIDELITY_LEVELS) * len(config.ROLES),
          f"seeded check: with no program isolated the detector must fire on "
          f"every call, or it cannot tell the defect from the fix: "
          f"{len(seeded)} fired")

    # Must not fire: a program this build has not read, and an HTTP endpoint.
    wrapper = at("open", "/usr/local/bin/claude-wrapper --print "
                 + " ".join(config.RESULT_ARGS))
    for role in config.ROLES:
        argv = shlex.split(wrapper.command_for(role))
        check(config.SAFE_MODE_FLAG not in argv and config.TOOLS_FLAG not in argv,
              f"an unrecognised program keeps the argv it was given: {argv!r}")
    over_http = config.resolve(
        parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md"]),
        environ={"LLOSSLESS_WINDOW": "200000"})
    check(all(over_http.command_for(role) == "" for role in config.ROLES),
          "an HTTP endpoint has no argv to isolate")


def test_an_operators_own_tools_or_safe_mode_is_theirs() -> None:
    """What an operator wrote in the route is never appended beside or edited.

    - `--safe-mode` already there: not appended a second time.
    - `--tools` already there: not appended beside, and what it leaves out is
      not granted. `sourced` narrows the automatic grant to what it names, and
      refuses, naming `--tools`, where it names no web tool at all.
    - `--tools default` asks for every tool: nothing is appended but safe
      mode, and the turn floor stays the older one, which errs low.
    - An operator's own `--allowed-tools` stays in force at every level, which
      the route caveat on the page says it does.
    """
    import shlex
    parser = cli.build_parser()
    base = ("/opt/claude-cli/bin/claude --print --model sonnet "
            + " ".join(config.RESULT_ARGS))

    def at(level, command):
        return config.resolve(
            parser.parse_args(["merge", "a.md", "b.md", "--base", "a.md",
                               "--fidelity", level, "--answer-with", command]),
            environ={"LLOSSLESS_WINDOW": "200000",
                     "LLOSSLESS_COMMAND_ENVELOPE": config.ENVELOPE_RESULT})

    theirs = at("open", base + " --safe-mode")
    argv = shlex.split(theirs.command_for("merge"))
    check(argv.count(config.SAFE_MODE_FLAG) == 1
          and _flag_value(argv, config.TOOLS_FLAG) == "",
          f"an operator's --safe-mode is not repeated: {argv!r}")

    fetch_only = at(config.SOURCED, base + " --tools WebFetch")
    argv = shlex.split(fetch_only.command_for("merge"))
    check(argv.count(config.TOOLS_FLAG) == 1
          and _flag_value(argv, config.TOOLS_FLAG) == "WebFetch",
          f"an operator's --tools is not appended beside: {argv!r}")
    check(config.granted_web_tools(fetch_only.command) == ("WebFetch",),
          f"and the automatic grant is narrowed to what it names: "
          f"{fetch_only.command!r}")

    try:
        at(config.SOURCED, base + " --tools ''")
        refused = ""
    except config.ConfigError as exc:
        refused = str(exc)
    check(config.TOOLS_FLAG in refused and "makes none available" in refused,
          f"sourced must refuse a route whose --tools leaves every web tool "
          f"out, and say so in those terms: {refused!r}")
    try:
        at(config.SOURCED, base + " --allowed-tools WebFetch --tools Read")
        refused = ""
    except config.ConfigError as exc:
        refused = str(exc)
    check("makes none available" in refused,
          f"and so must one whose own grant its --tools voids: {refused!r}")
    below = at("open", base + " --tools ''")
    check(shlex.split(below.command_for("merge")).count(config.TOOLS_FLAG) == 1,
          f"below sourced the same route runs, unwidened: "
          f"{below.command_for('merge')!r}")

    everything = at("open", base + " --tools default")
    argv = everything.command_for("merge")
    check(shlex.split(argv).count(config.TOOLS_FLAG) == 1
          and config.SAFE_MODE_FLAG in shlex.split(argv)
          and not config.only_web_tools(argv),
          f"--tools default gets safe mode and keeps the older floor: {argv!r}")

    granted = at("open", base + " --allowed-tools WebFetch")
    argv = shlex.split(granted.command_for("merge"))
    check(_flag_value(argv, config.TOOLS_FLAG) == "WebFetch"
          and config.granted_web_tools(granted.command) == ("WebFetch",),
          f"an operator's own grant stays in force below sourced: {argv!r}")


def _fake_claude_run(home: Path, base_url: str, command: str, level: str,
                     *extra: str) -> tuple[int, str, dict]:
    """One `merge` through a command backend at `level`, with the result envelope."""
    was = os.environ.get("LLOSSLESS_COMMAND_ENVELOPE")
    os.environ["LLOSSLESS_COMMAND_ENVELOPE"] = config.ENVELOPE_RESULT
    try:
        code, out, err = invoke(home, base_url, *sweep_argv(
            home, "--fidelity", level, "--answer-with", command,
            "--window", "200000", "--json", str(home / "report.json"), *extra))
    finally:
        if was is None:
            os.environ.pop("LLOSSLESS_COMMAND_ENVELOPE", None)
        else:
            os.environ["LLOSSLESS_COMMAND_ENVELOPE"] = was
    path = home / "report.json"
    return code, err, (json.loads(path.read_text(encoding="utf-8"))
                       if path.exists() else {})


def test_a_fake_claude_is_started_isolated_at_every_level() -> None:
    """Through `llossless merge --sweep-fidelity` and a program named `claude`.

    Read off the argv the fake program was really started with, every call of
    every level: one `--safe-mode`, one `--tools`, naming the grant where the
    call carries it (`sourced`) and nothing where it does not. A copy of the
    same program under another name is started with neither flag.
    """
    import shlex
    import shutil
    with workspace(Script(**CLEAN)) as (home, base_url):
        log = home / "calls.jsonl"
        command = claude_program(home, log)
        was = os.environ.get("LLOSSLESS_COMMAND_ENVELOPE")
        os.environ["LLOSSLESS_COMMAND_ENVELOPE"] = config.ENVELOPE_RESULT
        try:
            code, out, err = invoke(home, base_url, *sweep_argv(
                home, "--sweep-fidelity", "--answer-with", command,
                "--window", "200000"))
        finally:
            if was is None:
                os.environ.pop("LLOSSLESS_COMMAND_ENVELOPE", None)
            else:
                os.environ["LLOSSLESS_COMMAND_ENVELOPE"] = was
        calls = [json.loads(line)["argv"] for line in
                 log.read_text(encoding="utf-8").splitlines()] if log.exists() else []

        # The same program under a name this build has not read.
        wrapper = home / "bin" / "claude-wrapper"
        shutil.copy(home / "bin" / "claude", wrapper)
        log.unlink(missing_ok=True)
        wrapped = shlex.join([str(wrapper), *shlex.split(command)[1:]])
        wcode, _, _ = _fake_claude_run(home, base_url, wrapped, "open")
        wrapped_calls = [json.loads(line)["argv"] for line in
                         log.read_text(encoding="utf-8").splitlines()] if log.exists() else []

    # Exit 2: sourced's merge took one turn and retrieved nothing.
    check(code == 2 and calls, f"the claude sweep must complete: exit "
                                    f"{code}, {len(calls)} calls, {err[-300:]!r}")
    web = ",".join(config.AUTO_GRANT["claude"])
    wrong = [argv for argv in calls
             if not _isolated_as_measured(
                 shlex.join(argv),
                 web if config.ALLOW_TOOLS_FLAG in argv else "")]
    check(not wrong, f"every call the program was started with must be "
                     f"isolated: {len(wrong)} of {len(calls)}, e.g. {wrong[:1]}")
    kinds = {_flag_value(argv, config.TOOLS_FLAG) for argv in calls}
    check(kinds == {web, ""},
          f"both halves must have run, sourced and below: {kinds}")
    check(wcode in (0, 1) and wrapped_calls
          and not any(config.SAFE_MODE_FLAG in argv or config.TOOLS_FLAG in argv
                      for argv in wrapped_calls),
          f"a program this build has not read is started as written: exit "
          f"{wcode}, {wrapped_calls[:1]}")


def test_one_retrieval_under_the_isolation_is_read_as_one() -> None:
    """Two turns is a retrieval under the isolated argv, and not under the shipped one.

    Measured through CLI 2.1.274: under `--safe-mode --tools WebSearch,WebFetch`
    a plain answer is 1 turn and one fetch or one search is 2; under the argv
    without them the same fetch and search are 3 (`ToolSearch` first). A fake
    `claude` reporting 2 turns at `sourced` must read `retrieved`; the same
    program under another name, granted the same tools by its own argv, must
    read `not-retrieved`; and the isolated run must read `not-retrieved` with
    the web-only floor put back to 2, the value that misread it.
    """
    import shutil
    with workspace(Script(**CLEAN)) as (home, base_url):
        log = home / "calls.jsonl"
        command = claude_program(home, log, {"num_turns": 2})
        code, err, isolated = _fake_claude_run(home, base_url, command,
                                               config.SOURCED)

        from llossless import usage as usage_module
        shipped = usage_module.MOST_TURNS_WITHOUT_RETRIEVAL_WEB_ONLY
        try:
            usage_module.MOST_TURNS_WITHOUT_RETRIEVAL_WEB_ONLY = 2
            _, _, seeded = _fake_claude_run(home, base_url, command,
                                            config.SOURCED)
        finally:
            usage_module.MOST_TURNS_WITHOUT_RETRIEVAL_WEB_ONLY = shipped

        wrapper = home / "bin" / "claude-wrapper"
        shutil.copy(home / "bin" / "claude", wrapper)
        granted = (f"{wrapper} --print {' '.join(config.RESULT_ARGS)} "
                   f"{config.ALLOW_TOOLS_FLAG} {','.join(config.WEB_TOOLS)}")
        wcode, werr, unisolated = _fake_claude_run(home, base_url, granted,
                                                   config.SOURCED)

    sourcing = isolated.get("sourcing", {})
    check(code in (0, 1) and sourcing.get("retrieval") == usage_module.RETRIEVED,
          f"two turns under the isolation is a retrieval: exit {code}, "
          f"{sourcing.get('tool_use')}, {err[-300:]!r}")
    check(seeded.get("sourcing", {}).get("retrieval") == usage_module.NOT_RETRIEVED,
          f"seeded check: the old floor must misread the same run, or this "
          f"cannot tell the defect from the fix: {seeded.get('sourcing')}")
    # Exit 2: a `sourced` merge that retrieved nothing is not a
    # sourced merge, and the code says so.
    check(wcode == 2
          and unisolated.get("sourcing", {}).get("retrieval")
          == usage_module.NOT_RETRIEVED,
          f"two turns without the isolation is still not a retrieval: exit "
          f"{wcode}, {unisolated.get('sourcing')}, {werr[-300:]!r}")
    check(shipped == 1 and usage_module.MOST_TURNS_WITHOUT_RETRIEVAL == 2,
          f"the floors are 1 under the isolation and 2 without it: {shipped}, "
          f"{usage_module.MOST_TURNS_WITHOUT_RETRIEVAL}")


def claude_program_by_kind(home: Path, log: Path, turns_by_kind: dict) -> str:
    """`claude_program`, with `num_turns` chosen by the kind of prompt.

    The per-role shape the CLI really produced: on 2.1.274 a `sourced` run's
    low-effort decompose and verify calls took 2-5 turns while its merge took
    18-62; on 2.1.283 a Sonnet merge took 1. A kind not named answers in 1.
    """
    program = home / "bin" / "claude"
    program.parent.mkdir(exist_ok=True)
    program.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "os.environ.pop('LLOSSLESS_COMMAND', None)\n"
        f"sys.path[:0] = [{str(ROOT / 'tests')!r}, {str(ROOT / 'src')!r}]\n"
        "from test_cli import CLEAN, Script\n"
        "content = sys.stdin.read()\n"
        "kind = Script().kind(content)\n"
        f"with open({str(log)!r}, 'a') as log:\n"
        "    log.write(json.dumps({'kind': kind, 'argv': sys.argv[1:]}) + '\\n')\n"
        "reply = CLEAN[kind]\n"
        "reply = reply(1) if callable(reply) else reply\n"
        "answer = Script.answering_the_schema(kind, content, reply)\n"
        f"turns = {dict(turns_by_kind)!r}.get(kind, 1)\n"
        "envelope = {'type': 'result', 'subtype': 'success', 'is_error': False,\n"
        "            'num_turns': turns, 'permission_denials': [], 'result': answer}\n"
        "sys.stdout.write(json.dumps(envelope))\n",
        encoding="utf-8")
    program.chmod(0o755)
    return f"{program} --print {' '.join(config.RESULT_ARGS)}"


def test_a_sourced_merge_is_judged_on_its_merge_calls_and_one_that_recalled_exits_2() -> None:
    """`sourced` is judged on the merge's calls, and a merge that retrieved
    nothing is not a sourced merge: exit 2, said on every surface.

    Measured 2026-09-26: on CLI 2.1.283 five of five Sonnet voyager merges at
    `sourced` took one turn and retrieved nothing, and every run exited 1 like
    any sourced run, so a runner reading the code counted them as sourced
    draws. And the grant is run-wide: on 2.1.274 five of seven low-effort
    decompose and verify calls of one run took 2-5 turns, so a pooled tally
    reads "retrieved" over a merge that recalled.

    Through `llossless merge` and a fake program named `claude` under the
    isolated argv (floor 1), varying only the turns per prompt kind:

    - merge 2, the rest 1: retrieved, judged on 1 merge call, exit 0 or 1;
    - merge 1, decompose and verify 3: the pooled tally's false "retrieved".
      Must read not-retrieved and exit 2, with the verdict's own sentence and
      the terminal's; seeded by putting the pooled tally back in the shipped
      `report.retrieval_turns`, which must flip it to retrieved and exit < 2;
    - every call 1 (2.1.283's shape): not-retrieved, exit 2;
    - must-not-fire: the same all-1 program at `open` exits 0 or 1 and says
      nothing about retrieval.
    """
    from llossless import report as report_module, usage
    cases = {
        "merge-retrieved": {"merge": 2},
        "checks-only": {"decompose": 3, "forward": 3, "reverse": 3},
        "nothing": {},
    }
    got = {}
    for name, turns in cases.items():
        with workspace(Script(**CLEAN)) as (home, base_url):
            command = claude_program_by_kind(home, home / "calls.jsonl", turns)
            got[name] = _fake_claude_run(home, base_url, command, config.SOURCED)
            if name == "checks-only":
                shipped = report_module.retrieval_turns
                try:
                    report_module.retrieval_turns = lambda run: run.turns
                    got["seeded"] = _fake_claude_run(home, base_url, command,
                                                     config.SOURCED)
                finally:
                    report_module.retrieval_turns = shipped
            if name == "nothing":
                got["open"] = _fake_claude_run(home, base_url, command, "open")

    code, err, rep = got["merge-retrieved"]
    sourcing = rep.get("sourcing", {})
    check(code in (0, 1) and sourcing.get("retrieval") == usage.RETRIEVED
          and sourcing.get("retrieval_judged_on") == "merge"
          and (sourcing.get("tool_use") or {}).get("measured_calls") == 1
          and sourcing.get("inconclusive_not_sourced") is False,
          f"a merge that took a retrieval's turns retrieved, judged on its one "
          f"merge call: exit {code}, {sourcing}, {err[-300:]!r}")

    for name in ("checks-only", "nothing"):
        code, err, rep = got[name]
        sourcing = rep.get("sourcing", {})
        check(code == 2 and rep.get("exit_code") == 2,
              f"{name}: a sourced merge that retrieved nothing exits 2: exit "
              f"{code}, {sourcing}, {err[-300:]!r}")
        check(sourcing.get("retrieval") == usage.NOT_RETRIEVED
              and sourcing.get("recall_only") is True
              and sourcing.get("retrieval_judged_on") == "merge"
              and sourcing.get("inconclusive_not_sourced") is True,
              f"{name}: judged on the merge, not retrieved, and the page is "
              f"told the 2 is the retrieval's alone: {sourcing}")
        check("None of 1 merge call(s)" in err
              and "not a sourced merge" in err
              and "did not finish" not in err,
              f"{name}: the terminal says why, and not that work failed to "
              f"finish: {err[-600:]!r}")
        check(not any(step.get("state") == report.ERRORED
                      for step in rep.get("steps", [])),
              f"{name}: nothing errored, so the 2 is the retrieval's alone: "
              f"{rep.get('steps')}")

    code, err, rep = got["seeded"]
    check(code in (0, 1) and rep.get("sourcing", {}).get("retrieval")
          == usage.RETRIEVED,
          f"seeded: with the pooled tally back in the shipped function the "
          f"verify calls' turns read as the merge's retrieval, or this test "
          f"cannot see the defect: exit {code}, {rep.get('sourcing')}")

    code, err, rep = got["open"]
    check(code in (0, 1) and "retriev" not in err.lower()
          and rep.get("sourcing", {}).get("retrieval") == "",
          f"open is not judged on retrieval: exit {code}, "
          f"{rep.get('sourcing')}, {err[-300:]!r}")


def test_the_report_records_per_role_isolation_off_the_executed_argv() -> None:
    """`provenance.isolation`: safe mode and `--tools`, per role, off `command_for`.

    `retrieval.permitted` only says something at `sourced` -- it is empty by
    construction at every other level, because nothing is granted there -- so
    a `high` report through the isolated `claude` command said nothing about
    the isolation at all: an operator reading it could not tell their own
    CLAUDE.md, skills, plugins and MCP servers had been kept out of that run.
    This is the two-level check: `sourced`, where the automatic grant is on
    the argv, and `high`, the interesting case, where safe mode is still on
    and nothing is granted -- `[]`, not an absent key.

    Read off `report.json`'s own `provenance.isolation`, never reconstructed
    from `command` or from `config.ISOLATED` membership, and checked on the
    Markdown (stdout) and the HTML report too, which also renders it.
    """
    with workspace(Script(**CLEAN)) as (home, base_url):
        log = home / "calls.jsonl"
        command = claude_program(home, log)
        was = os.environ.get("LLOSSLESS_COMMAND_ENVELOPE")
        os.environ["LLOSSLESS_COMMAND_ENVELOPE"] = config.ENVELOPE_RESULT

        def run(level: str):
            json_path = home / f"report-{level}.json"
            html_path = home / f"report-{level}.html"
            code, out, err = invoke(home, base_url, *sweep_argv(
                home, "--fidelity", level, "--answer-with", command,
                "--window", "200000",
                "--json", str(json_path), "--html", str(html_path)))
            payload = (json.loads(json_path.read_text(encoding="utf-8"))
                      if json_path.exists() else {})
            html = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
            return code, out, err, payload, html

        try:
            s_code, s_md, s_err, s_report, s_html = run(config.SOURCED)
            h_code, h_md, h_err, h_report, h_html = run("high")
        finally:
            if was is None:
                os.environ.pop("LLOSSLESS_COMMAND_ENVELOPE", None)
            else:
                os.environ["LLOSSLESS_COMMAND_ENVELOPE"] = was

    web = sorted(config.AUTO_GRANT["claude"])
    # sourced exits 2: the fake's merge took one turn, retrieved
    # nothing, and that is not a sourced merge.
    check(s_code == 2 and h_code in (0, 1),
          f"both runs must complete: sourced {s_code} ({s_err[-200:]!r}), "
          f"high {h_code} ({h_err[-200:]!r})")

    s_isolation = s_report.get("provenance", {}).get("isolation", {})
    check(bool(s_isolation) and set(s_isolation) <= set(config.ROLES),
          f"sourced report's provenance.isolation must be non-empty and "
          f"keyed by role: {s_isolation}")
    for role, info in s_isolation.items():
        check(info.get("safe_mode") is True,
              f"sourced/{role}: safe_mode must be true: {info}")
        check(sorted(info.get("tools") or []) == web,
              f"sourced/{role}: tools must be the automatic grant {web}: {info}")

    h_isolation = h_report.get("provenance", {}).get("isolation", {})
    check(bool(h_isolation),
          f"high report has no provenance.isolation block: {h_report.get('provenance')}")
    for role, info in h_isolation.items():
        check(info.get("safe_mode") is True,
              f"high/{role}: safe mode must stay on where no tool is granted: {info}")
        check(info.get("tools") == [],
              f"high/{role}: tools must be the empty grant `[]`, not absent "
              f"or null -- `high` is the level `retrieval.permitted` says "
              f"nothing about: {info}")

    # Rendered, not only recorded: Markdown (stdout) and HTML both carry the
    # row, at both levels -- `high`'s is the row `Retrieval` cannot show.
    check("safe mode" in s_md and "safe mode" in h_md,
          f"the Isolation row must render in the Markdown report at every "
          f"level: sourced tail {s_md[-500:]!r}, high tail {h_md[-500:]!r}")
    check("safe mode" in s_html and "safe mode" in h_html,
          "the Isolation row must render in the HTML report too")


def test_a_subscription_merge_starts_at_the_level_its_model_was_ruled_at() -> None:
    """Through `llossless merge` and a fake `claude` that logs its argv.

    The operator's ruling: Opus's merge is started at `--effort high`,
    Sonnet's at `medium`; an alias the table does not name (`fable`, never
    measured) and an argv with no `--model` keep the program's `medium`;
    decompose and verify stay at `low` for every model. Read off the argv the
    program was really started with, and off the report.

    Haiku is not one of these any more (Haiku has one level,
    extended thinking on or off, not a scale) -- `test_haiku_gets_no_effort_flag_at_all`
    below is its own test, not a row here, because its assertion is the
    opposite of every row this one holds: no `--effort` at all, on any role.

    Seeded against the shipped code: with `AUTO_EFFORT_BY_MODEL` emptied, the
    same detector must see Opus's merge at `medium`. And by the effort precedence
    rule, an operator's `--effort merge=low` beats the per-model row.
    """
    expected = {"opus": "high", "sonnet": "medium",
                "fable": "medium", "": "medium"}

    def run(home, base_url, command, *extra):
        log = home / "calls.jsonl"
        log.unlink(missing_ok=True)
        code, err, report = _fake_claude_run(home, base_url, command, "open", *extra)
        calls = [json.loads(line) for line in
                 log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
        return code, err, report, calls

    def levels(calls, merge: bool) -> set:
        return {_flag_value(c["argv"], config.EFFORT_FLAG) for c in calls
                if (c["kind"] == "merge") == merge}

    with workspace(Script(**CLEAN)) as (home, base_url):
        base = claude_program(home, home / "calls.jsonl")
        seen = {alias: run(home, base_url, base + (f" --model {alias}" if alias else ""))
                for alias in expected}
        shipped = {program: dict(rows) for program, rows in config.AUTO_EFFORT_BY_MODEL.items()}
        config.AUTO_EFFORT_BY_MODEL.clear()
        try:
            seeded = run(home, base_url, base + " --model opus")
        finally:
            config.AUTO_EFFORT_BY_MODEL.update(shipped)
        theirs = run(home, base_url, base + " --model opus", "--effort", "merge=low")

    for alias, level in expected.items():
        code, err, report, calls = seen[alias]
        name = alias or "no --model"
        check(code in (0, 1) and calls,
              f"{name}: the run must complete through the fake: exit {code}, "
              f"{len(calls)} calls, {err[-300:]!r}")
        check(levels(calls, merge=True) == {level},
              f"{name}: the merge must be started at --effort {level}: "
              f"{levels(calls, merge=True)}")
        check(levels(calls, merge=False) == {"low"},
              f"{name}: decompose and verify stay at low: {levels(calls, merge=False)}")
        recorded = report.get("provenance", {}).get("decoding", {}).get("effort", {})
        check(recorded.get("merge") == level,
              f"{name}: the report must record merge={level}: {recorded}")
    check(levels(seeded[3], merge=True) == {"medium"},
          f"seeded: with the per-model table emptied Opus's merge must fall back "
          f"to the program's medium, or the check above cannot tell the table "
          f"from its absence: {levels(seeded[3], merge=True)}")
    check(levels(theirs[3], merge=True) == {"low"},
          f"an operator's --effort merge=low beats the per-model row: "
          f"{levels(theirs[3], merge=True)}")


def test_haiku_gets_no_effort_flag_at_all() -> None:
    """The operator's own words: *"Haiku does not provide
    effort levels like sonnet or opus do. It only allows 'extended' reasoning
    on/off. We should keep the default and flag it accordingly that it only
    has one level."*

    Before this: `AUTO_EFFORT_BY_MODEL["claude"]["haiku"]` put `--effort
    medium` on the merge, and the program's own row (`AUTO_EFFORT`) put
    `--effort low` on decompose and verify regardless of model -- so every
    Haiku call carried a flag this model does not take. Must-fire: the alias
    (`haiku`) and a full or dated id (`claude-haiku-4-5`,
    `claude-haiku-4-5-20251001`) all get no `--effort` on any of the three
    roles, and the report's `decoding.effort` has no `merge` key while
    `decoding.effort_single_level` names it with `config.SINGLE_LEVEL_LABEL`.
    Must-not-fire: an operator's own `--effort` on their own command line is
    still never overwritten, for this model exactly as for any other (rule 1).
    """
    def run(home, base_url, command, *extra):
        log = home / "calls.jsonl"
        log.unlink(missing_ok=True)
        code, err, report = _fake_claude_run(home, base_url, command, "open", *extra)
        calls = [json.loads(line) for line in
                 log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
        return code, err, report, calls

    def levels(calls) -> set:
        return {_flag_value(c["argv"], config.EFFORT_FLAG) for c in calls}

    with workspace(Script(**CLEAN)) as (home, base_url):
        base = claude_program(home, home / "calls.jsonl")
        for model in ("haiku", "claude-haiku-4-5", "claude-haiku-4-5-20251001"):
            code, err, report, calls = run(home, base_url,
                                           base + f" --model {model}")
            check(code in (0, 1) and calls,
                  f"{model}: the run must complete through the fake: exit "
                  f"{code}, {len(calls)} calls, {err[-300:]!r}")
            check(levels(calls) == {None},
                  f"{model}: no call may carry --effort at all: {levels(calls)}")
            decoding = report.get("provenance", {}).get("decoding", {})
            check("merge" not in decoding.get("effort", {}),
                  f"{model}: the report must claim no level for merge: "
                  f"{decoding.get('effort')}")
            check(decoding.get("effort_single_level", {}).get("merge")
                  == config.SINGLE_LEVEL_LABEL,
                  f"{model}: the report must label merge as single-level: "
                  f"{decoding.get('effort_single_level')}")
        code, err, report, calls = run(
            home, base_url, base + " --model haiku --effort medium")
        check(code in (0, 1) and calls,
              f"operator --effort: the run must complete: exit {code}, "
              f"{err[-300:]!r}")
        check({_flag_value(c["argv"], config.EFFORT_FLAG) for c in calls} == {"medium"},
              f"a level the operator wrote into their own --answer-with "
              f"command is never overwritten, for Haiku either (rule 1): "
              f"{calls}")


def test_the_old_command_name_is_gone() -> None:
    """The tool's former name is no longer installed, and `main` says nothing about it.

    An earlier change installed the old name beside `llossless` as a deprecated alias that
    printed a notice; the operator's fresh-start ruling removed both. Pinned
    from `pyproject.toml`: one console script, `llossless`. Run as a process
    whose program name is each of the two, stdout, stderr and the exit code
    must be byte for byte the same, over a command that exits 0 (`--version`)
    and one that exits 2 (`merge` with no sources): the program name reaches
    nothing. `rehearse_publication.py` checks the installed wheel has no
    script under the old name.
    """
    scripts = re.search(r"\[project\.scripts\]\n(.*?)\n\[",
                        (ROOT / "pyproject.toml").read_text(encoding="utf-8"), re.S)
    entries = dict(re.findall(r'^(\w+) = "([^"]+)"', scripts.group(1), re.M)) if scripts else {}
    check(entries == {"llossless": "llossless.cli:main"},
          f"pyproject must install llossless and nothing else: {entries}")
    check(not hasattr(cli, "deprecated_alias_notice") and not hasattr(cli, "OLD_COMMAND"),
          "the alias notice must be gone from cli.py")

    code = ("import sys; sys.argv[0] = sys.argv.pop(1); "
            "from llossless.cli import main; sys.exit(main())")
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("CLAIMCHECK_", "LLOSSLESS_"))}
    env["PYTHONPATH"] = str(ROOT / "src")

    def as_(name: str, *argv: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-c", code, f"/opt/bin/{name}", *argv],
                              capture_output=True, text=True, env=env, cwd=ROOT)

    for argv, want in ((["--version"], 0), (["merge"], 2)):
        new, old = as_("llossless", *argv), as_("claimcheck", *argv)
        check(new.returncode == want and old.returncode == want,
              f"{argv}: both program names must exit {want}: new "
              f"{new.returncode}, old {old.returncode}, {old.stderr[-300:]!r}")
        check(old.stdout == new.stdout and old.stderr == new.stderr,
              f"{argv}: the program name must change nothing: stderr "
              f"{old.stderr[-300:]!r} against {new.stderr[-300:]!r}")
        check("deprecated" not in old.stderr,
              f"{argv}: no deprecation notice may print: {old.stderr[-300:]!r}")


def test_the_old_variable_names_are_ignored() -> None:
    """A `CLAIMCHECK_*` variable is not read by the command, and not mentioned.

    As a process, the way an operator's shell meets it, over `merge --dry-run`
    so no model is called. A value no reader accepts, under the new name, is
    refused -- the must-fire probe that shows the variable is reached at all.
    The same value under the old name is ignored: the run goes ahead, exit 0,
    and stderr names neither the old variable nor a deprecation.
    """
    code = "import sys; from llossless.cli import main; sys.exit(main())"
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("CLAIMCHECK_", "LLOSSLESS_"))}
    env.update(PYTHONPATH=str(ROOT / "src"), LLOSSLESS_MODEL="m")
    with tempfile.TemporaryDirectory() as raw:
        a, b = Path(raw) / "a.md", Path(raw) / "b.md"
        a.write_text("# A\n\nOne line.\n", encoding="utf-8")
        b.write_text("# B\n\nAnother line.\n", encoding="utf-8")
        argv = [sys.executable, "-c", code, "merge", str(a), str(b), "--base", str(a),
                "--dry-run"]

        new = subprocess.run(argv, capture_output=True, text=True, cwd=raw,
                             env=dict(env, LLOSSLESS_FIDELITY="nonsense"))
        check(new.returncode == 2 and "LLOSSLESS_FIDELITY='nonsense'" in new.stderr,
              f"must fire: the new name is read and refused: exit "
              f"{new.returncode}, {new.stderr[-300:]!r}")

        old = subprocess.run(argv, capture_output=True, text=True, cwd=raw,
                             env=dict(env, CLAIMCHECK_FIDELITY="nonsense",
                                      CLAIMCHECK_MODEL="old-model"))
        check(old.returncode == 0,
              f"the old name must not be read: exit {old.returncode}, "
              f"{old.stderr[-300:]!r}")
        check("CLAIMCHECK" not in old.stderr and "deprecated" not in old.stderr
              and "old-model" not in old.stdout + old.stderr,
              f"the old name must be neither read nor mentioned: {old.stderr[:300]!r}")


# --------------------------------------------------------------------------
# an inconclusive run that no errored unit caused says what did cause it
# --------------------------------------------------------------------------


def verdict_of(out: str) -> str:
    """The one paragraph under `## Verdict` in a Markdown report."""
    if "## Verdict\n\n" not in out:
        return ""
    return out.split("## Verdict\n\n", 1)[1].split("\n", 1)[0]


NOT_ANSWERED = ("The model could not be made to answer usably, so this run does "
                "not establish that the claims it did check are the only ones "
                "there were.")


def test_an_inconclusive_verdict_gives_the_reason_the_run_has() -> None:
    """Exit 2 with every call answered is not "the model could not be made to answer".

    Two rules reach 2 without an errored unit or an ungraded claim: a source
    that yielded no claims on `verify`, and verdicts of which not one quote
    was grounded. Both printed "**Inconclusive.** . The model could not be
    made to answer usably": an empty reason, a stray full stop, and a sentence
    about a failure that did not happen. Through the real command, in the
    Markdown report and on the HTML page, which takes the same sentence.
    """
    no_claims = {**CLEAN,
                 "decompose": lambda n: claims() if n == 2
                 else claims(("The relay listens on port 8443.", 1)),
                 "forward": verdicts(
                     ("A-001", "SUPPORTED", "The relay listens on port 8443.", "merged.md")),
                 "reverse": verdicts(
                     ("M-001", "SUPPORTED", "The relay listens on port 8443.", "source_a.md"))}
    with workspace(Script(**no_claims), merged_on_disk=True) as (home, base_url):
        code, out, _ = invoke(home, base_url, "verify",
                              str(home / "notes-a.md"), str(home / "notes-b.md"),
                              str(home / "draft.md"), "--html", str(home / "r.html"))
        page = (home / "r.html").read_text(encoding="utf-8")
    unexamined = verdict_of(out)
    check(code == 2, f"an unexamined source on verify is exit 2: {code}")
    check(unexamined.startswith(
        "**Inconclusive.** 1 source(s) produced no claims, so this run does not "
        "establish that the claims it did check are the only ones there were."),
        f"the verdict must open on the reason this run has: {unexamined[:200]!r}")
    check("`source_b.md` produced no claims" in unexamined,
          f"and still name the source, last: {unexamined[-200:]!r}")

    nowhere = {**CLEAN,
               "forward": verdicts(
                   ("A-001", "SUPPORTED", "a sentence no document contains", "merged.md"),
                   ("B-001", "SUPPORTED", "another sentence no document contains", "merged.md")),
               "reverse": verdicts(
                   ("M-001", "SUPPORTED", "a third sentence nothing contains", "source_a.md"))}
    with workspace(Script(**nowhere)) as (home, base_url):
        code, out, _ = invoke(home, base_url, "merge", str(home / "notes-a.md"),
                              str(home / "notes-b.md"))
    ungrounded = verdict_of(out)
    check(code == 2, f"a run where nothing grounded is exit 2: {code}")
    check(ungrounded.startswith(
        "**Inconclusive.** 3 verdict(s) quote evidence and none of the quotes was "
        "found in the file it names, so no verdict here rests on anything shown "
        "to be in the documents."),
        f"the verdict must open on the reason this run has: {ungrounded[:220]!r}")

    for label, line in (("no claims", unexamined), ("nothing grounded", ungrounded)):
        check(re.match(r"\*\*Inconclusive\.\*\* [0-9A-Z]", line) is not None,
              f"{label}: the bold word must be followed by a sentence: {line[:60]!r}")
        check("** ." not in line and " . " not in line and ".." not in line,
              f"{label}: a stray full stop is in the verdict: {line[:120]!r}")
        check("could not be made to answer" not in line,
              f"{label}: every call was answered, so the verdict must not say "
              f"the model could not be made to answer: {line[:200]!r}")
    banner = page.split('class="banner', 1)[-1].split("</div>", 1)[0]
    check("<strong>Inconclusive.</strong> 1 source(s) produced no claims" in banner
          and "could not be made to answer" not in banner,
          f"the HTML banner takes the same sentence: {banner[:260]!r}")

    # Must not fire: where a unit of work did error, the sentence that says so
    # is the one it always was, to the byte.
    with workspace(Script(**{**CLEAN, "forward": None})) as (home, base_url):
        code, out, _ = invoke(home, base_url, "merge", str(home / "notes-a.md"),
                              str(home / "notes-b.md"))
    errored = verdict_of(out)
    check(code == 2 and errored.startswith(
        "**Inconclusive.** 1 unit(s) of work errored (verify (forward)). "
        + NOT_ANSWERED),
        f"an errored unit keeps its own sentence: {errored[:260]!r}")


def test_the_verdict_opening_is_reached_only_with_no_fault_to_name() -> None:
    """Must fire, on the shipped `verdict_line`: the new sentence taken away.

    With `report.unanswered_by_no_fault` answering what the verdict used to
    print, the verdict of a run with an unexamined source opens on the stray
    full stop the test above refuses; and the errored-unit verdict does not
    change, because that branch never asks it.
    """
    claim = Claim("A-001", "source_a.md", "The relay listens.", 1, "listens", True)
    graded = Verdict("A-001", "SUPPORTED", "The relay listens.", "merged.md", "found",
                     SOURCE_TO_MERGED, "grounded")
    run = report.Run(command="verify",
                     claims={"source_a.md": [claim], "source_b.md": []},
                     forward=[graded])
    run.paths = {"source_a.md": "a.md", "source_b.md": "b.md"}
    check(report.exit_code(run) == 2 and not run.errored and not run.unusable,
          "the probe run must be inconclusive for an unexamined source alone")
    shipped_line = report.verdict_line(run)
    check(shipped_line.startswith("**Inconclusive.** 1 source(s) produced no claims"),
          f"the shipped verdict for the probe run: {shipped_line[:120]!r}")
    shipped = report.unanswered_by_no_fault
    try:
        report.unanswered_by_no_fault = lambda run: "**Inconclusive.** . " + NOT_ANSWERED
        seeded_line = report.verdict_line(run)
        run.steps.append(report.Step("verify (forward)", report.ERRORED, "refused"))
        errored_line = report.verdict_line(run)
    finally:
        report.unanswered_by_no_fault = shipped
    check(seeded_line.startswith("**Inconclusive.** . The model could not"),
          f"seeded check: the verdict of an unexamined source does not come "
          f"from the sentence under test: {seeded_line[:80]!r}")
    check(errored_line.startswith("**Inconclusive.** 1 unit(s) of work errored")
          and NOT_ANSWERED in errored_line,
          f"an errored unit must not be routed through it: {errored_line[:120]!r}")


# --------------------------------------------------------------------------
# a report that will not print two counts for one quantity
# --------------------------------------------------------------------------


@contextlib.contextmanager
def coverage_counting_one_too_many():
    """The shipped report, with one of its two counts of the same claims off by one.

    `Run.forward_by_source` is what the Coverage table prints and what the
    guard in `report.inventory_section` holds the Inventory rows against.
    Saying one more claim was accounted for leaves the rows alone, so it is
    the shipped guard that raises the shipped `InventoryDisagrees`, from
    inside the shipped `render`, on the path `cli.main` takes.
    """
    shipped = report.Run.forward_by_source

    def off_by_one(self):
        return {name: {**row, "accounted": row["accounted"] + 1}
                for name, row in shipped(self).items()}

    report.Run.forward_by_source = off_by_one
    try:
        yield
    finally:
        report.Run.forward_by_source = shipped


def refused(home: Path, base_url: str, *argv: str) -> tuple[object, str, str]:
    """`invoke`, with an exception that escaped `main` returned as the code."""
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code, printed, said = invoke(home, base_url, *argv)
    except Exception as exc:  # noqa: BLE001 - an escaped exception is the defect
        return exc, out.getvalue(), err.getvalue()
    return code, printed, said


def test_a_report_that_counts_one_quantity_two_ways_is_an_inconclusive_run() -> None:
    """`InventoryDisagrees` reached nobody: `cli.main` let it out as a traceback.

    The report raises it sooner than print an Inventory and a Coverage table
    that disagree. It is a defect in the tool when it fires, and the run is
    inconclusive: exit 2, one plain line that says what was refused and whose
    fault it is, and the merged document not lost with the report.
    """
    said = "refuses to print two different counts for one quantity"
    with workspace(Script(**CLEAN), merged_on_disk=True) as (home, base_url):
        sources = (str(home / "notes-a.md"), str(home / "notes-b.md"))

        # Must not fire: the same command, as shipped, prints its report.
        code, out, err = refused(home, base_url, "merge", *sources)
        check(code == 0 and "## Inventory" in out and said not in err,
              f"an ordinary run must not be refused: {code!r} {strip(err)[-200:]!r}")

        with coverage_counting_one_too_many():
            code, out, err = refused(home, base_url, "merge", *sources)
            check(code == 2,
                  f"merge: a report that disagrees with itself is exit 2, not "
                  f"{code!r}")
            err = strip(err)
            check("Traceback" not in err and err.count("error: ") == 1,
                  f"merge: one refusal and no traceback: {err[-300:]!r}")
            check(said in err and "defect in LLossless and not in your documents" in err
                  and "please report it" in err and "inconclusive" in err,
                  f"merge: the line must say what was refused and whose defect "
                  f"it is: {err[-400:]!r}")
            check("One report, two answers." in err,
                  f"merge: and carry the two counts, for the report: {err[-300:]!r}")
            check(out == MERGED and "printed in its place" in err,
                  f"merge without -o: the merged document must not be lost with "
                  f"the report: {out[:200]!r}")

            target, json_path, html_path = (home / "m.md", home / "r.json",
                                            home / "r.html")
            code, out, err = refused(home, base_url, "merge", *sources,
                                     "-o", str(target), "--json", str(json_path),
                                     "--html", str(html_path))
            check(code == 2 and out == "" and said in strip(err),
                  f"merge -o: exit 2 and no report: {code!r} {out[:120]!r}")
            check(target.exists() and target.read_text(encoding="utf-8") == MERGED
                  and f"the merged document is in {target}" in strip(err),
                  f"merge -o: the merged document is still written, and the "
                  f"line says where: {strip(err)[:200]!r}")
            check(not json_path.exists() and not html_path.exists(),
                  "merge -o: no JSON and no HTML report beside a report that "
                  "was refused")

            code, out, err = refused(home, base_url, "verify", *sources,
                                     str(home / "draft.md"))
            check(code == 2 and out == "" and said in strip(err)
                  and "Traceback" not in err,
                  f"verify: exit 2, no report, the same line: {code!r} "
                  f"{strip(err)[-200:]!r}")

        # The page holds the same two figures against each other, on its own
        # rows. Only its count is seeded here, so the Markdown report prints.
        shipped = html_report._inventory_table

        def one_row_too_many(run, name, reverse):
            rows, statuses = shipped(run, name, reverse)
            return rows, statuses + statuses[:1]

        html_report._inventory_table = one_row_too_many
        try:
            page = home / "only.html"
            code, out, err = refused(home, base_url, "merge", *sources,
                                     "--html", str(page))
        finally:
            html_report._inventory_table = shipped
        check(code == 2 and "## Inventory" in out and not page.exists(),
              f"--html: the page is refused and the Markdown report stands: "
              f"{code!r}")
        check(f"the HTML report was not written to {page}" in strip(err)
              and said in strip(err),
              f"--html: the line names the page it did not write: "
              f"{strip(err)[-300:]!r}")


# --------------------------------------------------------------------------
# a message names only settings that exist
# --------------------------------------------------------------------------


_SETTINGS: list[tuple[set[str], set[str]]] = []


def settings_that_exist() -> tuple[set[str], set[str]]:
    """Every flag the three commands take, and every variable the tool reads.

    The flags are the parser's own. The variables are the `LLOSSLESS_` names
    in the source of the modules that read the environment and in the help
    text that documents them, with a per-role family (`LLOSSLESS_WINDOW_`)
    kept as its prefix. Worked out once: the reader below asks it of every
    string in three modules.
    """
    if _SETTINGS:
        return _SETTINGS[0]
    parser = cli.build_parser()
    parsers = [parser]
    for action in parser._subparsers._group_actions:
        parsers += action.choices.values()
    flags = {option for each in parsers for option in each._option_string_actions
             if option.startswith("--")}
    package = ROOT / "src" / "llossless"
    read = "".join(path.read_text(encoding="utf-8")
                   for path in [package / "config.py",
                                *sorted((package / "web").glob("*.py"))])
    variables = set(re.findall(r"LLOSSLESS_[A-Z_]+",
                               read + cli.EPILOG + cli.SERVE_EPILOG))
    _SETTINGS.append((flags, variables))
    return flags, variables


def unknown_settings(text: str) -> list[str]:
    """The `--flags` and `LLOSSLESS_` variables `text` names that do not exist."""
    flags, variables = settings_that_exist()
    named_flags = set(re.findall(r"(?<![\w-])--[a-z][a-z-]*[a-z]", text))
    named_variables = set(re.findall(r"LLOSSLESS_[A-Z_]+", text))
    families = {name for name in variables if name.endswith("_")}
    return sorted(named_flags - flags) + sorted(
        name for name in named_variables - variables
        if not any(name.startswith(family) for family in families)
        and name.rstrip("_") not in variables)


def messages_of(source: str) -> list[str]:
    """Every string a module's code holds, docstrings left out.

    A docstring may name a flag that does not exist in order to say so (this
    command's own says there is no `--offline`); a string in the code is
    something the tool can print.
    """
    import ast

    tree = ast.parse(source)
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            first = node.body[0] if node.body else None
            if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                docstrings.add(id(first.value))
    return [node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
            and id(node) not in docstrings]


def refusals_of(module) -> dict[str, str]:
    """Each refusal `window` can raise, raised, by the name of what raises it."""
    served = module.Window(tokens=5, source="reported", model="m", detail="d")
    calls = {
        "assert_untruncated": lambda: module.assert_untruncated(
            {"max_tokens": 10, "completion_tokens": 10}, what="merge"),
        "assert_prompt_not_trimmed": lambda: module.assert_prompt_not_trimmed(
            {"estimated_prompt_tokens": 100, "prompt_tokens": 10}, what="merge"),
        "preflight": lambda: module.preflight(None, needed=10, what="verify",
                                              role="verify"),
        "guard": lambda: module.guard(needed=10, window=served, what="merge"),
    }
    raised = {}
    for name, call in calls.items():
        try:
            call()
        except RuntimeError as exc:
            raised[name] = str(exc)
    return raised


def test_a_message_names_only_flags_and_variables_that_exist() -> None:
    """`raise --max-tokens`, said to a reader who has no such flag to raise.

    A truncated merge told its operator to raise `--max-tokens`. There is no
    such flag: the ceiling is `LLOSSLESS_MAX_TOKENS`. Every refusal `window`
    raises is raised here and read, and every string in the code of the three
    modules that talk to the operator is read as well, against the flags the
    parser really takes and the variables the tool really reads.
    """
    import inspect
    import textwrap
    import types

    from llossless import window

    flags, variables = settings_that_exist()
    check({"--window", "--fidelity", "--timeout"} <= flags
          and "LLOSSLESS_MAX_TOKENS" in variables and "LLOSSLESS_WINDOW" in variables,
          f"the list of what exists is not the parser's and the tool's: "
          f"{sorted(flags)[:5]} {sorted(variables)[:5]}")
    raised = refusals_of(window)
    check(len(raised) == 4, f"each of the four refusals must be raised: {sorted(raised)}")
    for name, message in raised.items():
        check(not unknown_settings(message),
              f"window.{name} names a setting that does not exist: "
              f"{unknown_settings(message)} in {message[-200:]!r}")
    check("LLOSSLESS_MAX_TOKENS" in raised.get("assert_untruncated", ""),
          "a completion that hit its ceiling must name the variable that sets "
          "the ceiling")
    for module in ("window.py", "cli.py", "report.py"):
        source = (ROOT / "src" / "llossless" / module).read_text(encoding="utf-8")
        for message in messages_of(source):
            check(not unknown_settings(message),
                  f"{module} holds a string naming a setting that does not "
                  f"exist: {unknown_settings(message)} in {message[:120]!r}")

    # Must fire: the shipped refusal with the flag put back, and the reader of
    # strings on a source that holds one.
    shipped = textwrap.dedent(inspect.getsource(window.assert_untruncated))
    check(shipped.count("LLOSSLESS_MAX_TOKENS higher") == 1,
          "the seed aims at nothing: the sentence under test was reworded")
    scope = dict(vars(window))
    exec(compile(shipped.replace("LLOSSLESS_MAX_TOKENS higher", "--max-tokens"),
                 "<seeded assert_untruncated>", "exec"), scope)
    seeded = types.SimpleNamespace(**{**vars(window),
                                      "assert_untruncated": scope["assert_untruncated"]})
    check(unknown_settings(refusals_of(seeded).get("assert_untruncated", ""))
          == ["--max-tokens"],
          "seeded check: a refusal naming --max-tokens passed")
    planted = ('def f():\n    "--not-a-flag, in a docstring."\n'
               '    return "set LLOSSLESS_NO_SUCH or --no-such-flag"\n')
    check([unknown_settings(message) for message in messages_of(planted)]
          == [["--no-such-flag", "LLOSSLESS_NO_SUCH"]],
          f"seeded check: the reader of strings missed a planted flag and "
          f"variable, or read a docstring: "
          f"{[unknown_settings(message) for message in messages_of(planted)]}")
    check(unknown_settings("--window / LLOSSLESS_WINDOW, LLOSSLESS_BASE_URL_MERGE, "
                           "LLOSSLESS_WINDOW_<ROLE>") == [],
          "must not fire: real flags, real variables and a per-role family")


def closing_block(run: report.Run) -> tuple[int, str]:
    """What `summarise` says on stderr for this run, with the code `exit_code` gives it."""
    code = report.exit_code(run)
    stream = io.StringIO()
    cli.summarise(run, code, output=None, coloured=False, piped=False, stream=stream)
    return code, " ".join(stream.getvalue().split())


def test_an_inconclusive_run_that_finished_is_not_described_as_unfinished() -> None:
    """MUST FIRE: a `verify` source that produced no claims, and claims graded
    with no quote found in the file named, exit 2 with every call answered.

    The closing block said "Part of this run did not finish" for both, which is
    false: the run finished and its verdict gives the real reason. Driven
    through `summarise` on runs built the way `verify` builds them, so the
    code is the one `report.exit_code` gives and the sentence is the shipped
    one.

    MUST NOT FIRE: a run with an errored unit still says it did not finish,
    and says so in the words the reference quotes for a failed merge.
    """
    claim = Claim(id="A-001", source="a.md", text="x", line=1, span="x", anchored=True)
    unfinished = " ".join(" ".join(cli.OUTCOME[2]).split())

    empty = report.Run(command="verify")
    empty.claims = {"a.md": [], "b.md": [claim], cli.MERGED: [claim]}
    code, said = closing_block(empty)
    check(code == 2, f"a source with no claims on verify must exit 2: {code}")
    check("did not finish" not in said, f"the run finished: {said!r}")
    check("1 source(s) produced no claims" in said and "a.md" in said,
          f"the reason and the source must be named: {said!r}")
    check(said.startswith("Inconclusive."), f"one word for the verdict: {said!r}")

    ungrounded = report.Run(command="verify")
    ungrounded.claims = {"a.md": [claim], cli.MERGED: [claim]}
    ungrounded.forward = [Verdict("A-001", "SUPPORTED", "a quote", "a.md", "r",
                                  SOURCE_TO_MERGED, "ungrounded")]
    code, said = closing_block(ungrounded)
    check(code == 2, f"graded claims with no grounded quote must exit 2: {code}")
    check("did not finish" not in said, f"the run finished: {said!r}")
    check("none of the quotes was found in the file it names" in said,
          f"the reason must be named: {said!r}")

    broken = report.Run(command="merge")
    broken.steps.append(report.Step("merge", report.ERRORED, "merge: no usable response"))
    code, said = closing_block(broken)
    check(code == 2 and said.startswith(unfinished),
          f"a unit that errored keeps the unfinished sentence: {said!r}")

    # Seeded on the shipped function: with the new branch's helper made to
    # answer nothing, the first run above says "did not finish" again.
    kept = cli.finished_inconclusive
    cli.finished_inconclusive = lambda run: None
    try:
        _, regressed = closing_block(empty)
    finally:
        cli.finished_inconclusive = kept
    check("did not finish" in regressed,
          f"seeded check: without the branch the old sentence returns: {regressed!r}")


def test_the_help_lists_every_case_that_exits_two() -> None:
    """MUST FIRE: each case that exits 2 today is named under `exit 2` in the help."""
    top = parser_prints(["--help"], "--help must print and exit 0")
    block = " ".join(top.split("  exit 2", 1)[1].split("  exit 3", 1)[0].split())
    for needed in ("configuration", "unreachable endpoint", "could not answer",
                   "no claims on verify", "no evidence quote found",
                   "sourced merge that looked nothing up", "unwritable -o",
                   "disagreeing counts"):
        check(needed in block, f"`exit 2` in the help must name {needed!r}: {block!r}")
    check(len(block) < 400, f"and stay short: {len(block)} characters")


def headings_a_message_names(source: str) -> list[str]:
    """Every `## Heading` written in backticks in a string of this module's source."""
    import ast
    named: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            named += re.findall(r"`## ([A-Z][A-Za-z ]*?)`", node.value)
    return named


def headings_the_report_prints() -> set[str]:
    """Every `## Heading` the report's own section functions write, read off their source."""
    import ast
    found: set[str] = set()
    for module in (report, sys.modules[Provenance.__module__]):
        for node in ast.walk(ast.parse(Path(module.__file__).read_text())):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                match = re.match(r"## ([A-Z][A-Za-z ]*?)\s*(?:\n|$)", node.value)
                if match:
                    found.add(match.group(1))
    return found


def test_every_heading_a_terminal_message_names_is_one_the_report_prints() -> None:
    """MUST FIRE: a message that says "see `## Additions`" sends a reader to a
    heading the report does not have. Every backticked `## Heading` in the
    terminal's own source is held to the headings the report's section
    functions write, read from `report.py` and `provenance.py` and not typed
    here.
    """
    printed = headings_the_report_prints()
    check({"Verdict", "Findings", "Added from outside the documents",
           "Review queue", "Merged document"} <= printed,
          f"the heading list must be read off the report, not empty: {sorted(printed)}")
    named = headings_a_message_names((ROOT / "src/llossless/cli.py").read_text())
    check(len(named) >= 5, f"the scan must find the messages: {named}")
    for heading in named:
        check(heading in printed,
              f"a message names `## {heading}`, which the report never prints")
    seeded = headings_a_message_names('say("see `## Additions`")')
    check(seeded == ["Additions"] and seeded[0] not in printed,
          f"seeded check: the old wrong name must be found and refused: {seeded}")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("cli: all checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
