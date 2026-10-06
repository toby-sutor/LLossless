#!/usr/bin/env python3
"""The HTML report: does it say what the Markdown and the JSON say, and nothing more?

Run directly:

    python3 tests/test_html_report.py

Exits 0 when every check passes, 1 otherwise. Stdlib only, no network, no model
call - the guard below makes the second of those an assertion rather than a
claim.

Three kinds of check, and the order is the order of what would hurt most.

**Escaping.** A merged document is text a model wrote about text somebody else
wrote, and neither is trusted. The must-fire probe puts `<script>alert(1)</script>`
into a claim, a rationale, a filename, a segment id and the merged document
itself, and asserts the string `<script>` appears nowhere in the output while
the visible text survives character for character. A page that fails this is
not a cosmetic failure; it is a report that executes the document it was asked
to check.

**Parity.** The same `Run` is rendered three ways, and the three are held
against each other by claim id, by status word, by exit code and by every
count either of the other two prints. This is the check that stops the HTML
report becoming a second opinion: a figure it computed itself could drift from
the Markdown one, and a reader with the HTML open would have no way to know.

**Shape.** `html.parser` walks the whole document: every tag closes, in order,
and the page carries no `\\x00`. The parser is the same one `find_spans` leaked
a NUL past once, which is why the byte is asserted about here too.

The three runs are built from the fixtures' own answer keys - `dedup` clean,
`dropped_claim` with a finding, and a structural case - rather than from a
model. Nothing here measures a model; it measures a renderer, and a renderer
tested against generated output would be tested against a moving fixture.
"""

from __future__ import annotations

import base64
import contextlib
import inspect
import json
import sys
import textwrap
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# This module opens no socket. Same reasoning as `test_fixtures.py`: the guard
# turns that sentence into something that fails when it stops being true.
socket_guard.install()

from llossless import config, html_report, parsing, report  # noqa: E402
from llossless.client import Client  # noqa: E402
from llossless.decompose import Claim  # noqa: E402
from llossless.provenance import Provenance  # noqa: E402
from llossless.reconcile import Finding, Order, Reconciled  # noqa: E402
from llossless.report import Run, Step  # noqa: E402
from llossless.verify import (  # noqa: E402
    CONFIRMED,
    GROUNDED,
    MERGED,
    MERGED_TO_SOURCES,
    NOT_GRADED,
    SOURCE_TO_MERGED,
    Graded,
    Unusable,
    Verdict,
)

FIXTURES = ROOT / "tests" / "fixtures"

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# runs, built from the fixtures' answer keys
# --------------------------------------------------------------------------


def claim(claim_id: str, source: str, text: str, line: int, *,
          anchored: bool = True) -> Claim:
    return Claim(id=claim_id, source=source, text=text, line=line, span=text,
                 anchored=anchored)


def verdict(claim_id: str, label: str, direction: str, *, evidence: str = "",
            source: str = "", rationale: str = "",
            grounding: str = GROUNDED) -> Verdict:
    return Verdict(
        claim_id=claim_id,
        verdict=label,
        evidence=evidence,
        evidence_source=source,
        rationale=rationale,
        direction=direction,
        grounding=grounding if evidence else NOT_GRADED,
    )


def fixture_run(name: str) -> Run:
    """One fixture's documents and probes, as the `Run` a clean pass would produce.

    The probe list is the fixture's answer key, so the claims are the ones the
    fixture pre-registered and their verdicts are the ones it expects. What is
    being tested is the renderer, and the key is the only input to it that
    cannot drift under a prompt change.
    """
    spec = json.loads((FIXTURES / name / "expected.json").read_text(encoding="utf-8"))
    documents = {
        path.name: path.read_text(encoding="utf-8")
        for path in sorted((FIXTURES / name).glob("*.md"))
    }
    run = Run(
        command="verify",
        paths={key: key for key in documents},
        steps=[Step("decompose source_a.md", report.OK),
               Step("verify forward", report.OK)],
        merged=documents.get("merged.md"),
        merged_written_to="merged.md",
    )
    forward, reverse = [], []
    for index, probe in enumerate(spec["probes"], start=1):
        document = probe["document"]
        claim_id = f"P-{index:03d}"
        run.claims.setdefault(document, []).append(
            claim(claim_id, document, probe["text"], probe["line"])
        )
        label = probe.get("expected_verdict", "SUPPORTED")
        target = MERGED if probe["direction"] == SOURCE_TO_MERGED else "source_a.md"
        entry = verdict(
            claim_id, label, probe["direction"],
            evidence=probe["text"] if label != "MISSING" else "",
            source=target,
            rationale=probe.get("description", "The reference text settles it."),
        )
        (forward if probe["direction"] == SOURCE_TO_MERGED else reverse).append(entry)
    run.forward = forward
    run.reverse = reverse
    return run


def structural_run() -> Run:
    """A merge with a structural finding and a review queue: the widest page.

    One run rather than three because the sections are independent and the
    parity check is per section: this exercises the queue, the declarations
    table, the reconciler's findings and the ordering line at once, and every
    one of them is a section the clean fixtures never reach.
    """
    run = fixture_run("dropped_claim")
    run.command = "merge"
    run.merged_written_to = None
    run.base = "source_a.md"
    run.base_chosen = "explicit"
    run.segments = 12
    run.declarations = (
        Graded(
            segment="a3",
            disposition="dropped",
            grade=CONFIRMED,
            detail="no claim from this segment is in the merge",
            claims=("P-001",),
            reason="superseded by the newer figure in source B",
        ),
        Graded(
            segment="b2",
            disposition="rewritten",
            grade=report.REJECTED,
            detail="the text it names is still in the merge",
            claims=(),
            reason="tightened the wording",
        ),
    )
    run.reconciled = Reconciled(
        findings=(
            Finding(
                kind="verbatim_violation",
                detail="the token `8443` did not survive into the merge",
                segment="a1",
                document="source_a.md",
            ),
            Finding(
                kind="title_not_from_source",
                detail="the merged title appears in neither source",
                segment="",
                document="merged.md",
            ),
        ),
        declared_drops=({"segment": "a3"},),
        segments=12,
    )
    run.order = Order(
        sequence=("a", "a", "b", "b"),
        runs=2,
        interleaved=False,
        monotone=True,
        attributed=4,
        headings_total=4,
        headings_present=3,
    )
    # The first probe is the one the declaration owns, so it has to come back
    # MISSING for the queue to have anything in it. Rewritten rather than added,
    # so the claim in the queue is a claim the inventory also lists.
    run.forward = [
        verdict(v.claim_id, "MISSING", SOURCE_TO_MERGED,
                rationale="not found in the merged document")
        if v.claim_id == "P-001" else v
        for v in run.forward
    ]
    run.provenance = provenance_for(run)
    return run


HOSTILE = "<script>alert(1)</script>"


MARKUP_NAME = "a`b**c**d.md"


def markup_named_run() -> Run:
    """A run whose filenames carry the two markers `inline` honours.

    Not a script tag: `inline` escapes before it marks up, so no tag this
    codebase did not write can appear and there is nothing to inject. What a
    backtick or a `**` pair *can* do is put `<code>` or `<strong>` structure
    into the page, or close a span the renderer opened -- and `inline`'s own
    docstring says it is for prose this codebase wrote.
    """
    run = Run(
        command="merge",
        paths={"source_a.md": MARKUP_NAME, "source_b.md": "source_b.md"},
        merged="# t\n\nbody\n",
        segments=1,
    )
    run.claims = {"source_a.md": [claim("A-001", "source_a.md", "a claim", 1)],
                  MERGED: [claim("M-001", MERGED, "a claim", 1)]}
    run.base, run.base_chosen = MARKUP_NAME, "named"
    run.provenance = provenance_for(run)
    return run


def test_a_filename_carrying_markup_survives_as_text() -> None:
    """Must fire on the defect, both places a filename reaches the page.

    `run.display` builds `<code>` tags around the escaped short name in the
    coverage rows and the finding cards. The provenance `Base document` row is
    the same shape and was found by auditing the sites this item names rather
    than by the item naming it.
    """
    page = html_report.render(markup_named_run())
    check("<strong>c</strong>" not in page,
          "a `**` pair in a filename must not become emphasis")
    escaped = MARKUP_NAME.replace("`", "&#x60;") if "&#x60;" in page else MARKUP_NAME
    check(escaped in page or MARKUP_NAME in page,
          f"the filename must appear in the page as itself, not as markup")
    # And the structure around it stays balanced: as many opening code tags as
    # closing ones. An unbalanced count is what a stray backtick produces.
    check(page.count("<code>") == page.count("</code>"),
          f"code spans must balance: {page.count('<code>')} open, "
          f"{page.count('</code>')} closed")


def hostile_run() -> Run:
    """Every string a document or a model controls, set to a script tag.

    Not a subset: the claim text, the evidence, the rationale, the filename,
    the segment id, the declared reason and the merged document all carry it,
    because an escaping test that covered four of seven fields would pass on a
    renderer that escaped four of seven fields.
    """
    run = Run(
        command="merge",
        paths={"source_a.md": f"{HOSTILE}.md", "source_b.md": "source_b.md"},
        steps=[Step(f"decompose {HOSTILE}", report.ERRORED, f"detail {HOSTILE}")],
        merged=f"# {HOSTILE}\n\nbody {HOSTILE}\n",
        segments=3,
    )
    run.claims = {
        "source_a.md": [claim("A-001", "source_a.md", f"claim {HOSTILE}", 1)],
        MERGED: [claim("M-001", MERGED, f"merged claim {HOSTILE}", 1)],
    }
    run.forward = [
        verdict("A-001", "MISSING", SOURCE_TO_MERGED,
                rationale=f"rationale {HOSTILE}")
    ]
    run.reverse = [
        verdict("M-001", "SUPPORTED", MERGED_TO_SOURCES,
                evidence=f"evidence {HOSTILE}", source="source_a.md",
                rationale=f"reverse rationale {HOSTILE}")
    ]
    run.declarations = (
        Graded(segment=f"seg {HOSTILE}", disposition="dropped", grade=CONFIRMED,
               detail=f"detail {HOSTILE}", claims=("A-001",),
               reason=f"reason {HOSTILE}"),
    )
    run.reconciled = Reconciled(
        findings=(
            Finding(kind="undeclared_absence", detail=f"detail {HOSTILE}",
                    segment=f"seg {HOSTILE}", document="source_a.md"),
        ),
        declared_drops=(),
        segments=3,
    )
    run.order = Order(sequence=("a",), runs=1, interleaved=False, monotone=True,
                      attributed=1, headings_total=1, headings_present=0)
    return run


# --------------------------------------------------------------------------
# a parser, used as a validator
# --------------------------------------------------------------------------

VOID = {"meta", "br", "hr", "img", "input", "link", "source", "col", "wbr"}


class Shape(HTMLParser):
    """Every tag closed, in order, and a record of what the page contains.

    `convert_charrefs` stays on, so `text` holds what a reader sees rather than
    the entities behind it: the escaping check asserts on the decoded text and
    the raw string separately, and conflating them would let `&lt;script&gt;`
    pass a test looking for the absence of `<script>`.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.text: list[str] = []
        self.tags: list[str] = []
        self.attrs: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        self.tags.append(tag)
        self.attrs.append((tag, {k: (v or "") for k, v in attrs}))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs) -> None:
        self.tags.append(tag)
        self.attrs.append((tag, {k: (v or "") for k, v in attrs}))

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"</{tag}> with nothing open")
        elif self.stack[-1] != tag:
            self.errors.append(f"</{tag}> closes <{self.stack[-1]}>")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def parse(page: str, label: str) -> Shape:
    shape = Shape()
    shape.feed(page)
    shape.close()
    check(not shape.errors, f"{label}: the page is not well formed: {shape.errors[:3]}")
    check(not shape.stack, f"{label}: tags left open at the end: {shape.stack}")
    return shape


def attrs_of(shape: Shape, tag: str, key: str) -> list[str]:
    return [a[key] for name, a in shape.attrs if name == tag and key in a]


# --------------------------------------------------------------------------
# escaping: the must-fire probe
# --------------------------------------------------------------------------


def test_a_hostile_document_cannot_put_a_tag_on_the_page() -> None:
    """The security check. Every field, and the visible text survives whole."""
    page = html_report.render(hostile_run())
    check("<script>alert(1)</script>" not in page,
          "a document's script tag reached the page unescaped")
    check("&lt;script&gt;alert(1)&lt;/script&gt;" in page,
          "the script tag must be on the page, escaped, not silently dropped")
    # One `<script>` element, and it is the filter this file ships.
    shape = parse(page, "hostile")
    check(shape.tags.count("script") == 1,
          f"the page must carry exactly one script element: {shape.tags.count('script')}")
    # The reader still sees the text. Decoded, the hostile string is there once
    # per field it was put in, which is what "escaped, not stripped" means.
    seen = "".join(shape.text)
    check(seen.count(HOSTILE) >= 7,
          f"the hostile string must survive as visible text in every field it was "
          f"put in: {seen.count(HOSTILE)} occurrence(s)")
    check("\x00" not in page, "a NUL byte reached the page")


def test_escaping_is_asserted_by_a_probe_that_can_fail() -> None:
    """The must-not-fire half: `esc` off, and the check above fires.

    A scanner that has never been seen to fail is a
    scanner nobody has tested, so the probe is run against a renderer with the
    escaping removed and has to catch it.
    """
    original = html_report.esc
    try:
        html_report.esc = lambda text: str(text)  # noqa: E731 - deliberate breakage
        page = html_report.render(hostile_run())
    finally:
        html_report.esc = original
    check("<script>alert(1)</script>" in page,
          "the seeded breakage did not put a raw tag on the page, so the probe "
          "above cannot be said to have caught anything")


# --------------------------------------------------------------------------
# parity: one run, three outputs, no second opinion
# --------------------------------------------------------------------------


def parity(run: Run, label: str) -> None:
    """Every figure the HTML shows, against the Markdown and the JSON.

    Claim by claim rather than by totals. Two reports can agree on how many
    claims were dropped and disagree about which, and the second failure is the
    one a reader would act on.
    """
    page = html_report.render(run)
    markdown = report.render(run)
    payload = report.as_dict(run)
    shape = parse(page, label)

    banner = [a for tag, a in shape.attrs if "data-exit-code" in a]
    check(len(banner) == 1, f"{label}: one banner, not {len(banner)}")
    if banner:
        check(banner[0]["data-exit-code"] == str(payload["exit_code"]),
              f"{label}: the banner says exit {banner[0]['data-exit-code']} and the "
              f"JSON says {payload['exit_code']}")

    # The verdict sentence, word for word, from `report.verdict_line`. Compared
    # on the visible text so the Markdown's `**` and the HTML's `<strong>` are
    # the same sentence.
    seen = "".join(shape.text)
    line = report.verdict_line(run)
    plain = line.replace("**", "").replace("`", "")
    check(plain in seen, f"{label}: the HTML must carry the verdict sentence verbatim")
    check(line in markdown, f"{label}: the Markdown must carry the same sentence")

    # Every claim, by id, with the status word the Markdown table gives it.
    rows = {a["data-claim-id"]: a.get("data-status", "")
            for tag, a in shape.attrs if tag == "tr" and "data-claim-id" in a}
    expected: dict[str, str] = {}
    for name in run.sources():
        for claim_id, status in statuses(run, name, reverse=False).items():
            expected[claim_id] = status
    if MERGED in run.claims:
        expected.update(statuses(run, MERGED, reverse=True))
    check(rows == expected,
          f"{label}: the inventory rows and the verdicts disagree: "
          f"{sorted(set(rows.items()) ^ set(expected.items()))[:4]}")

    # Claim text, verbatim and untruncated, for every claim in the JSON.
    for entry in payload["claims"]:
        check(entry["text"] in seen,
              f"{label}: claim {entry['id']} is not on the page in full")

    # The findings, by kind and by claim id.
    cards = [(a["data-kind"], a.get("data-claim-id", ""))
             for tag, a in shape.attrs
             if tag == "article" and a.get("data-kind") and a.get("data-claim-id")]
    finding_cards = sorted(c for c in cards if c[1] and c[0] in report.FINDING_ORDER)
    from_json = sorted(
        (entry["finding"], entry["claim_id"]) for entry in payload["findings"]
    )
    check(finding_cards == from_json,
          f"{label}: the finding cards {finding_cards} are not the JSON's "
          f"findings {from_json}")

    queued = sorted(c[1] for c in cards if c[0] == "review_queue")
    check(queued == sorted(entry["claim_id"] for entry in payload["review_queue"]),
          f"{label}: the review queue on the page is not the JSON's queue")

    structural = len([1 for tag, a in shape.attrs
                      if tag == "article"
                      and a.get("data-kind") in report.FINDING_KINDS])
    check(structural == len(payload["structural"]["findings"]),
          f"{label}: {structural} structural card(s) against "
          f"{len(payload['structural']['findings'])} in the JSON")

    # Coverage: the ratios the bars carry, against the JSON's counts.
    coverage = payload["coverage"]
    forward = f"{len([v for v in run.forward if v.finding == 'none'])}/{len(run.forward)}"
    if run.forward:
        check(forward in seen,
              f"{label}: the forward ratio {forward} is not on the page")
    reverse = (f"{len([v for v in run.reverse if v.finding == 'none'])}/"
               f"{len(run.reverse)}")
    if run.reverse:
        check(reverse in seen,
              f"{label}: the reverse ratio {reverse} is not on the page")
    for name, count in coverage["extracted"].items():
        check(f"{run.display(name)}" in seen,
              f"{label}: {name} is not named on the page")
        check(str(count) in seen, f"{label}: the extraction count for {name} is missing")

    # Colour against exit code. Neither the status word nor the exit code
    # catches a row painted red under a Clean banner, and a reader scanning the
    # page for colour would act on the paint. Held as an invariant rather than
    # a copy of the table: a clean run has nothing to paint red, and a run with
    # a finding cannot be headed by a clean banner.
    severities = {
        a["class"].split()[-1]
        for tag, a in shape.attrs
        if a.get("class", "").startswith("chip ")
    }
    banner_state = banner[0]["class"].split()[-1] if banner else ""
    if payload["exit_code"] == 0:
        check(banner_state == "ok",
              f"{label}: exit 0 under a {banner_state!r} banner")
        check("bad" not in severities,
              f"{label}: exit 0 with a row painted as a finding")
    else:
        check(banner_state != "ok",
              f"{label}: exit {payload['exit_code']} under a clean banner")

    check("\x00" not in page, f"{label}: a NUL byte reached the page")


def statuses(run: Run, name: str, *, reverse: bool) -> dict[str, str]:
    """The status word each claim of one document gets, from `report`'s own tables."""
    source = run.reverse if reverse else run.forward
    labels = report.REVERSE_STATUS if reverse else report.FORWARD_STATUS
    found = {v.claim_id: v for v in source}
    out = {}
    for item in run.claims.get(name, []):
        entry = found.get(item.id)
        out[item.id] = labels[entry.finding] if entry else report.NOT_CHECKED
    return out


def test_the_three_outputs_agree_on_a_clean_run() -> None:
    parity(fixture_run("dedup"), "dedup")


def test_the_three_outputs_agree_where_a_claim_was_dropped() -> None:
    parity(fixture_run("dropped_claim"), "dropped_claim")


def test_the_three_outputs_agree_on_a_structural_finding() -> None:
    parity(structural_run(), "structural")


def test_the_hostile_run_is_held_to_the_same_parity() -> None:
    """The escaping probe's run, through the parity check as well.

    A renderer that escaped everything and dropped half the rows would pass the
    security check on its own. The two run over the same object so that neither
    can be satisfied by breaking the other.
    """
    parity(hostile_run(), "hostile")


# --------------------------------------------------------------------------
# shape: what the page is, beyond being well formed
# --------------------------------------------------------------------------


def test_the_page_is_one_file_and_asks_the_network_for_nothing() -> None:
    """Self-contained: no CDN, no font host, no image, no fetch."""
    page = html_report.render(structural_run())
    for token in ("http://", "https://", "//cdn", "fetch(", "XMLHttpRequest",
                  "@import", "src=", "url("):
        check(token not in page, f"the page must not carry {token!r}")
    shape = parse(page, "self-contained")
    check("link" not in shape.tags, "the page must link no external stylesheet")
    check("img" not in shape.tags, "the page must load no image")
    check(shape.tags.count("style") == 1, "the page must carry exactly one stylesheet")


def test_the_sections_are_the_markdown_sections_in_the_markdown_order() -> None:
    """One order, both renderers, and the table of contents points at all of it."""
    run = structural_run()
    page = html_report.render(run)
    shape = parse(page, "sections")
    ids = [a["id"] for tag, a in shape.attrs if tag == "section" and "id" in a]
    check(ids == ["coverage", "findings", "capped", "ungraded", "inventory",
                  "structure", "queue", "declarations", "provenance", "merged"],
          f"the sections are in the wrong order or missing: {ids}")
    targets = [href[1:] for href in attrs_of(shape, "a", "href") if href.startswith("#")]
    check(set(targets) <= set(ids) | {"verdict"},
          f"the table of contents points at a section that is not there: {targets}")
    for anchor in ids:
        check(anchor in targets, f"no table-of-contents entry for #{anchor}")


def test_a_verify_run_has_no_merge_only_section() -> None:
    """The Markdown rule, asserted on the page: no merge, no structure or queue."""
    page = html_report.render(fixture_run("dedup"))
    shape = parse(page, "verify")
    ids = [a["id"] for tag, a in shape.attrs if tag == "section" and "id" in a]
    for absent in ("structure", "queue", "declarations"):
        check(absent not in ids,
              f"a verify run must not print the {absent} section: {ids}")


def test_the_banner_word_tracks_the_exit_code() -> None:
    """Three exit codes, three headlines, and no two of them the same word.

    The `data-exit-code` check in `parity` compares the attribute with the
    JSON, which a table mapping every code to "Clean" would still satisfy. This
    is the check that the word a reader actually sees moved with it.
    """
    words = {}
    for label, run in (("clean", fixture_run("dedup")),
                       ("findings", structural_run()),
                       ("inconclusive", inconclusive_run())):
        page = html_report.render(run)
        shape = parse(page, f"banner {label}")
        head = [a for tag, a in shape.attrs if "data-exit-code" in a]
        check(len(head) == 1, f"{label}: one banner, not {len(head)}")
        if head:
            words[head[0]["data-exit-code"]] = banner_word(page)
    check(len(set(words.values())) == 3,
          f"the three exit codes must not share a headline: {words}")


def test_the_page_carries_the_suspended_guarantee_the_report_does() -> None:
    """One sentence, three surfaces, because `verdict_line` is shared.

    The Markdown report, this page and the terminal transcript all render
    `report.verdict_line`, so the `coverage` caveat reaches all three from one
    place -- and the page is where it matters most, because a browser reader
    sees the banner and often nothing else. Asserted here rather than assumed
    from the sharing: a future `verify_block` that composed its own sentence
    would pass every other test in this module.
    """
    run = fixture_run("dedup")
    run.verify_depth = config.COVERAGE_DEPTH
    page = html_report.render(run)
    check("checked only that your documents" in page,
          "the page's banner must carry the suspended-guarantee sentence at a "
          "depth that never read the merged document back")
    banner = page.split('class="banner', 1)[1].split("</div>", 1)[0]
    check("invented" not in banner.split("This run checked only")[0],
          f"and the headline above it must not rule out invention: "
          f"{banner[:200]!r}")

    run.verify_depth = config.DEFAULT_VERIFY_DEPTH
    check("checked only that your documents" not in html_report.render(run),
          "and a full run must not carry it")


def inconclusive_run() -> Run:
    """A step that errored, which is exit 2 whatever the verdicts said."""
    run = fixture_run("dedup")
    run.steps.append(Step("verify reverse", report.ERRORED, "the endpoint refused"))
    return run


class BannerText(HTMLParser):
    """The text inside the element carrying `data-exit-code`, and nothing else.

    Depth-counted rather than regex-matched: the banner holds markup, and a
    reader sees the words in it, not the first heading on the page.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.words: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in VOID:
            return
        if self.depth or any(key == "data-exit-code" for key, _ in attrs):
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.depth and tag not in VOID:
            self.depth -= 1

    def handle_data(self, data: str) -> None:
        if self.depth and data.strip():
            self.words.append(data.strip())


def banner_word(page: str) -> str:
    """The headline, read off the page rather than off the table that made it."""
    reader = BannerText()
    reader.feed(page)
    reader.close()
    return " ".join(reader.words)


def test_status_words_are_never_carried_by_colour_alone() -> None:
    """Every chip says its status in words; the class only paints it."""
    page = html_report.render(structural_run())
    shape = parse(page, "chips")
    words = set()
    for name in shape.text:
        words.add(name.strip())
    for status in set(report.FORWARD_STATUS.values()) | set(
        report.REVERSE_STATUS.values()
    ):
        if status in [a.get("data-status") for _, a in shape.attrs]:
            check(status in words,
                  f"the status {status!r} is on a row but nowhere in the text")


def test_the_dry_run_page_is_a_plan_and_says_so() -> None:
    """--dry-run made no call, so the page has no verdict to show."""
    run = Run(command="merge", paths={"source_a.md": "a.md"},
              steps=[Step("merge", report.PLANNED), Step("decompose", report.PLANNED)])
    page = html_report.render(run)
    shape = parse(page, "dry run")
    ids = [a["id"] for tag, a in shape.attrs if tag == "section" and "id" in a]
    check(ids == ["planned"], f"a dry run prints the plan and nothing else: {ids}")
    check("2 call(s) planned, none made." in "".join(shape.text),
          "the plan must say how many calls it counted")
    check("data-exit-code" not in page,
          "a dry run graded nothing and must show no verdict banner")


def test_the_provenance_block_is_the_one_the_markdown_prints() -> None:
    """Same rows, same notes, from `Provenance.rows` and `Provenance.notes`."""
    run = fixture_run("dedup")
    run.provenance = provenance_for(run)
    page = html_report.render(run)
    seen = "".join(parse(page, "provenance").text)
    for label, value in run.provenance.rows():
        check(label in seen, f"the provenance row {label!r} is missing from the page")
        plain = value.replace("`", "").replace("**", "")
        check(plain in seen,
              f"the provenance value for {label!r} is missing or reworded: {plain!r}")


def test_generated_at_is_the_same_across_every_rendering_of_one_run() -> None:
    """`generated_at` is read once, when the run's `Provenance` is built,
    not recomputed on every call that reads it.

    `Provenance.as_dict` used to call `datetime.now` itself, and `rows`,
    `notes` and the JSON report's own `as_dict` call each read it
    independently: a Markdown report (`rows` plus `notes`), an HTML report
    (its own, separate `rows` plus `notes`) and the JSON report
    (`report.as_dict`, straight into `provenance.as_dict`) between them read
    the clock up to five times for one run, and any two of those reads could
    disagree the moment a second boundary fell between them, since
    `isoformat(timespec="seconds")` already throws away anything finer. That
    is what made this test flake in the publication rehearsal that led to
    this fix: the HTML report's own reading of `rows()` and this test's second,
    separate call to it could each see a different `datetime.now()`.

    A single run's `Provenance` is built once and handed to every renderer
    (`cli.py`, `web/jobs.py`), so asserting that this one instance's
    `generated_at` is the value every rendering carries is the deterministic
    form of the same check: no wall-clock read is left in the assertion.
    """
    run = fixture_run("dedup")
    run.provenance = provenance_for(run)
    stamp = run.provenance.generated_at

    html_page = html_report.render(run)
    markdown_page = report.render(run)
    exported = report.as_dict(run)

    check(dict(run.provenance.rows())["Generated"] == stamp,
          "Provenance.rows must report the field it was built with, not a fresh read")
    check(stamp in "".join(parse(html_page, "provenance").text),
          "the HTML report's provenance block does not carry the run's own generated_at")
    check(f"| Generated | {stamp} |" in markdown_page,
          "the Markdown report's provenance table does not carry the run's own generated_at")
    check(exported["provenance"]["generated_at"] == stamp,
          "the JSON report's provenance.generated_at is not the run's own field")

    # Must fire: a `Provenance` built with an explicit, different stamp shows
    # that stamp everywhere, proving the assertions above pin the field this
    # run was built with rather than passing on any timestamp shape.
    seeded = provenance_for(run)
    object.__setattr__(seeded, "generated_at", "2000-01-01T00:00:00+00:00")
    run.provenance = seeded
    seeded_html = html_report.render(run)
    check("2000-01-01T00:00:00+00:00" in "".join(parse(seeded_html, "provenance").text),
          "a Provenance built with a different generated_at is not the one the page shows")


def test_the_html_report_shortens_paths_like_the_markdown_does() -> None:
    """This follows `report.py` automatically -- checked here, not assumed.

    `html_report.py` imports `Run.display` from `report.py`, so a caller's
    absolute path should already be gone from the page; this asserts it rather
    than trusting the import. The old mapping prose ("The model was shown ...
    as ...") is asserted absent from both outputs, not just removed from one.
    """
    run = fixture_run("dedup")
    # Deliberately not a `/home/...` path. That shape is refused anywhere in
    # the published set, and rightly so: a synthetic one here would still
    # teach a reader that the form is expected. Any absolute path exercises
    # `Run.display` equally.
    run.paths = {"source_a.md": "/srv/caller/notes-a.md",
                 "source_b.md": "/srv/caller/notes-b.md"}
    page = html_report.render(run)
    markdown = report.render(run)

    check("/srv/caller/" not in page,
          f"the caller's absolute path reached the HTML page: {page[:400]!r}")
    check("/srv/caller/" not in markdown,
          f"the caller's absolute path reached the Markdown report: {markdown[:400]!r}")
    check("notes-a.md" in page and "notes-b.md" in page,
          "the HTML page must still name the documents by their short name")

    check("was shown" not in page and "The model was shown" not in page,
          "the HTML report must not restate a second, path-to-canonical naming "
          "system in prose")
    check("was shown" not in markdown,
          "the Markdown report must not restate a second, path-to-canonical "
          "naming system in prose")


def provenance_for(run: Run) -> Provenance:
    """The real block, from a real `Client` that has made no call.

    A stub would let the HTML print rows the live block never produces. The
    client is constructed and never used; `socket_guard` above is what makes
    "never used" an assertion rather than a comment.
    """
    settings = config.Settings(base_url="http://127.0.0.1:11434/v1",
                               models={"merge": "test-model",
                                       "decompose": "test-model",
                                       "verify": "test-model"})
    return Provenance(settings=settings, client=Client(settings),
                      roles=("decompose", "verify"), duration_seconds=1.0,
                      base=run.base, base_chosen=run.base_chosen)


# --------------------------------------------------------------------------
# the filter, read as text rather than executed
# --------------------------------------------------------------------------


def test_every_row_and_card_is_filterable_and_nothing_starts_hidden() -> None:
    """The one piece of JavaScript, and the page it has to be correct without.

    `hidden` is added by the filter and by nothing else, so a reader with
    JavaScript off sees every row. Asserted rather than reasoned about: a
    default-hidden row is a claim the report does not print.
    """
    page = html_report.render(structural_run())
    shape = parse(page, "filter")
    check('class="hidden"' not in page and " hidden\"" not in page,
          "nothing may be hidden in the delivered page")
    filterable = len([1 for _, a in shape.attrs if "data-filterable" in a])
    rows = len([1 for tag, a in shape.attrs if tag == "tr" and "data-claim-id" in a])
    cards = len([1 for tag, a in shape.attrs if tag == "article"])
    check(filterable >= rows + cards,
          f"every row and card must be filterable: {filterable} against "
          f"{rows} row(s) and {cards} card(s)")


def test_the_additions_block_attributes_and_escapes() -> None:
    """The one section on this page that reports rather than grades.

    Four columns and none of them a verdict, because nothing here was checked:
    an addition is by definition a statement the sources do not carry, and the
    sources are the only thing this tool checks against. What the block owes a
    reader is the count -- in claims covered, not records declared, since one
    declaration can cover several -- and the attribution, so a declaration
    covering a dozen claims cannot look like a dozen covering one each.

    The statement is the model's text and reaches the page unfiltered, so it
    is also the obvious injection surface on a report a reader opens in a
    browser.
    """
    text = "Solar is cheaper than coal."
    claims = [Claim(id="M-001", source="merged.md", text=text, line=1,
                    span=text, anchored=True)]
    verdicts = [Verdict("M-001", "MISSING", "", "", "in no source",
                        MERGED_TO_SOURCES, NOT_GRADED)]
    run = Run(command="merge", claims={"merged.md": claims}, reverse=verdicts,
              additions=({"statement": text, "corrects": "doc A's 2019 figure",
                          "reason": "well established"},
                         {"statement": "Unrelated <script>alert(1)</script>.",
                          "corrects": "", "reason": ""}))
    html = "\n".join(html_report.additions_block(run))

    check("<script>" not in html,
          "the merge's own text reaches this page, so an unescaped statement "
          "is script injection into a report a reader opens in a browser")
    check("&lt;script&gt;" in html,
          "and it must still be shown, escaped, rather than stripped")
    check("<strong>2</strong> statement(s)" in html,
          f"the prose counts the declarations: {html[:120]!r}")
    check("covering 1 claim(s)" in html,
          "and counts the claims they covered separately, because the two "
          "numbers differ exactly when a reader most needs to see both")
    check("<code>M-001</code>" in html,
          "the claim a declaration covered is named against it")
    check(html.count("<tr data-filterable>") == 2,
          "one row per declared addition, filterable like every other row")
    for note in ("none recorded", "nothing named", "none"):
        check(f'class="note">{note}<' in html,
              f"an empty cell says {note!r} rather than going blank; a blank "
              f"cell reads as a rendering fault, not as an absent value")
    check(html.rstrip().endswith("</tbody></table></div>"),
          "the table is closed")


def test_the_additions_section_is_absent_when_nothing_was_added() -> None:
    """No additions, no section -- unlike every other section on the page.

    The others stay up saying nothing was found, because a reader needs to
    know a check ran and came back empty. This one is not a check. At a level
    that permits no additions there is no question its absence leaves open,
    and a standing empty section headed "added from outside" would suggest
    there was one.
    """
    text = "The relay listens on port 8443."
    claims = [Claim(id="M-001", source="merged.md", text=text, line=1,
                    span=text, anchored=True)]
    run = Run(command="merge", claims={"merged.md": claims},
              reverse=[Verdict("M-001", "SUPPORTED", text, "source_a.md", "",
                               MERGED_TO_SOURCES, GROUNDED)],
              merged=text)
    page = html_report.render(run)
    check("Added from outside" not in page,
          "a run that added nothing must not carry the section, in the body "
          "or in the table of contents")

    run.additions = ({"statement": "Something the sources do not say.",
                      "corrects": "", "reason": "confident"},)
    page = html_report.render(run)
    check(page.count("Added from outside") >= 2,
          "and a run that added something carries it in both the table of "
          "contents and the body")
    check("Something the sources do not say." in page,
          "with the declared statement in it")


def test_every_exit_code_the_tool_can_return_has_a_banner() -> None:
    """A bare subscript on a table that was not told about a new code.

    Exit code `3` was split out of `1` -- the document is sound and the merge's
    account of itself is not -- and `BANNER` kept three rows. `render` reads
    it with `BANNER[code]`, so a record-only failure crashed with
    `KeyError: 3` **after the whole pipeline had finished**, which is the
    worst moment to lose a report and the least explicable to whoever is
    watching. The operator met it exactly that way.

    Asserted over `report.EXIT_CODES` rather than a literal list, because the
    failure to prevent is a *fifth* code being added and this table not
    hearing about it. The module already asserts the same thing at import, so
    this is the second of the two halves: the assert catches it on any import,
    and this catches it with a name a reader can act on.
    """
    check(set(html_report.BANNER) == set(report.EXIT_CODES),
          f"BANNER covers {sorted(html_report.BANNER)} and the tool can exit "
          f"{sorted(report.EXIT_CODES)}; `BANNER[code]` is a bare subscript "
          f"and a missing row is a crash at the end of a finished run")

    # And it renders, which the assert alone does not establish.
    for code in report.EXIT_CODES:
        state, word = html_report.BANNER[code]
        check(state in ("ok", "bad", "none", "warn"),
              f"exit {code} has state {state!r}, which no stylesheet rule matches")
        check(word and word[0].isupper(),
              f"exit {code} has no readable word: {word!r}")

    # Exit 3 end to end, because that is the one that was missing. A record
    # finding and nothing worse.
    run = Run(command="merge", merged="The relay listens on port 8443.\n")
    run.reconciled = Reconciled(
        segments=4, declared_drops=0,
        findings=(Finding("false_departure", "b2 declared dropped, still present"),))
    check(report.exit_code(run) == report.RECORD_ONLY,
          f"this run must exit 3 or the test is measuring something else: "
          f"{report.exit_code(run)}")
    page = html_report.render(run)
    check("Record findings" in page,
          "and the page says which kind of failure it was, rather than "
          "borrowing the word for content that went missing")


def test_the_rendered_file_offers_no_download_and_a_served_page_does() -> None:
    """The file is the thing you keep; only a page on a server offers to save it.

    The operator asked for a download control on the report itself -- reading a
    report and then wanting to keep it is one flow, and going back to the tab
    you came from to press a button there is not.

    A control in the *file* would be worse than no control. That file is what
    `llossless merge --html` writes, what the control itself hands over, and
    what somebody mails to a colleague; a link in it would resolve against
    whatever directory it was opened from. So `render` leaves an empty slot and
    `with_download` fills it, and both halves are asserted here -- a control
    that is always absent and a control that is always present are both one
    edit away and neither is what this is.
    """
    for name, run in (("clean", fixture_run("dedup")),
                      ("structural", structural_run())):
        page = html_report.render(run)
        check(html_report.SLOT in page,
              f"the {name} run's page carries no slot, so nothing a server "
              f"does can put a control on it")
        # Matched on attribute spellings rather than on the word "download":
        # a document may say it, and `esc` turns a document's quotes into
        # `&quot;`, so `download="` can only have come from this module.
        for marker in ('class="toolbar"', 'class="save"', 'download="'):
            check(marker not in page,
                  f"the {name} run's rendered file carries {marker}")

        served = html_report.with_download(page)
        check('<a class="save" href="data:text/html;charset=utf-8;base64,' in served,
              "the served page must carry one control, and it must carry the "
              "report rather than ask a server for it")
        check('download="report.html">Download this report</a>' in served,
              "the control must name the file it saves")
        check(html_report.SLOT not in served,
              "the slot is filled, not decorated")
        check(control_of(served) is not None, "no control to read back")
        check(served.replace(control_of(served), html_report.SLOT) == page,
              "filling the slot changed something else on the page")
        check(html_report.SLOT in html_report.render(run),
              "a second render of the same run must still leave the slot "
              "empty; `with_download` may not mutate anything shared")

        # What the control hands over is the file, byte for byte. Decoded and
        # compared rather than trusted: this is the whole property, and the
        # two are built from one string precisely so that it holds.
        check(carried(served) == page,
              f"the {name} run's control hands over something other than the "
              f"file this page was made from")
        check(html_report.SLOT in carried(served),
              "and what it hands over has an empty slot, or the saved copy "
              "carries a control of its own")

    # A page from an older version of this tool has no slot. It comes back
    # unchanged rather than raising: a job directory survives an upgrade.
    check(html_report.with_download("<p>no slot here</p>") ==
          "<p>no slot here</p>",
          "a page with no slot must come back unchanged")

    # The control is markup and nothing else: no fetch, no script, no asset,
    # and nothing that names a host. A sandboxed page may not reach this
    # server at all -- its requests are cross-site and the session cookie is
    # `SameSite=Strict` -- so a control that asked for anything would be a
    # button that answers 401.
    control = control_of(html_report.with_download(
        html_report.render(fixture_run("dedup"))))
    for banned in ("<script", "onclick", "fetch(", "http://", "https://",
                   "/api/", "//"):
        check(banned not in control,
              f"the control carries {banned!r}; it is one link and one "
              f"sentence, and anything else is a request or a handler")


def control_of(served: str) -> str | None:
    """The control `with_download` filled the slot with, and nothing else."""
    if '<p class="toolbar"' not in served:
        return None
    start = served.index('<p class="toolbar"')
    return served[start:served.index("</p>", start) + 4]


def carried(served: str) -> str:
    """What the control hands over, decoded out of its own href."""
    mark = "base64,"
    start = served.index(mark, served.index('<a class="save"')) + len(mark)
    end = served.index('"', start)
    return base64.b64decode(served[start:end]).decode("utf-8")


def test_an_argument_to_the_control_is_escaped_like_everything_else() -> None:
    """Must-fire: the one value `with_download` takes is not trusted either.

    The caller is this codebase, so this is the belt on top of a brace. It is
    here because the control is the first thing on this page built from a
    value that did not come out of the `Run`, and a renderer that escapes
    everything but its own arguments is one call site away from not escaping.
    """
    served = html_report.with_download(html_report.render(fixture_run("dedup")),
                                       filename='rep" onfocus="alert(1).html')
    check('onfocus="alert(1)' not in served,
          "a filename closed its attribute and opened an event handler")
    check("&quot;" in control_of(served),
          "the quotes went somewhere other than an entity")


# --------------------------------------------------------------------------
# what was capped and what was not graded: two sections and a coverage row
# --------------------------------------------------------------------------


def ungraded_run() -> Run:
    """A run with one record that could not be graded and two capped fields.

    The claim id and the defect of the ungraded record are the model's words,
    so both carry the hostile string: this run goes through the escaping
    check as well as the parity check.
    """
    run = structural_run()
    run.unusable = [
        Unusable(claim_id=f"X-{HOSTILE}", direction=SOURCE_TO_MERGED, index=2,
                 defects=(f"$.verdicts[2].verdict: {HOSTILE} is not a verdict",
                          "$.verdicts[2].evidence: missing")),
        Unusable(claim_id="", direction=MERGED_TO_SOURCES, index=0,
                 defects=("$.verdicts[0]: not an object",)),
    ]
    run.truncations = (
        parsing.Truncation(path="$.dispositions[0].reason", original_length=912,
                           cap=400),
    )
    first = run.forward[0]
    run.forward[0] = Verdict(
        claim_id=first.claim_id, verdict=first.verdict, evidence=first.evidence,
        evidence_source=first.evidence_source, rationale=first.rationale,
        direction=first.direction, grounding=first.grounding,
        rationale_capped=True,
    )
    return run


def bare(text: str) -> str:
    """Markdown prose as a reader of the page sees it: no markers, one spacing."""
    return " ".join(text.replace("**", "").replace("`", "").replace("_", "").split())


def ungraded_gaps(run: Run, page: str) -> list[str]:
    """What the page is missing of the two sections and the row, as sentences.

    Returned rather than recorded, so the must-fire probes below can ask the
    same question of a page that is known to be missing something.
    """
    gaps: list[str] = []
    shape = parse(page, "ungraded")
    seen = " ".join("".join(shape.text).split())
    ids = [a["id"] for tag, a in shape.attrs if tag == "section" and "id" in a]
    targets = [href[1:] for href in attrs_of(shape, "a", "href")
               if href.startswith("#")]

    # The sections, where the Markdown report has them, under its headings.
    for anchor, section in (("capped", report.capping_section(run)),
                            ("ungraded", report.unusable_section(run))):
        heading, *lines = [line for line in section.splitlines() if line]
        title = heading.removeprefix("## ")
        if anchor not in ids:
            gaps.append(f"no {title!r} section on the page")
        if anchor not in targets:
            gaps.append(f"no table-of-contents entry for {title!r}")
        if f">{title}</h2>" not in page:
            gaps.append(f"no heading {title!r}, which is the Markdown heading")
        # Every line the Markdown section prints, as visible text.
        for line in lines:
            wanted = bare(line.strip().removeprefix("- ").removesuffix(":"))
            if wanted not in bare(seen):
                gaps.append(f"the {title!r} line {wanted!r} is not on the page")
    order = [anchor for anchor in ids
             if anchor in ("findings", "capped", "ungraded", "inventory")]
    if order != ["findings", "capped", "ungraded", "inventory"]:
        gaps.append(f"the two sections are not between Findings and Inventory, "
                    f"in the Markdown order: {order}")

    # The coverage row, with the count the Markdown table prints.
    row = [line for line in report.coverage_section(run).splitlines()
           if "not graded" in line]
    label, count = [cell.strip() for cell in row[0].strip("|").split("|")]
    if f">{label}</th><td><span class=\"value mono\">{count}</span>" not in page:
        gaps.append(f"no coverage row {label!r} with the value {count}")

    # One filterable card per record and per capped field.
    kinds = [a.get("data-kind") for tag, a in shape.attrs
             if tag == "article" and "data-filterable" in a]
    if kinds.count("not_graded") != len(run.unusable):
        gaps.append(f"{kinds.count('not_graded')} filterable card(s) for "
                    f"{len(run.unusable)} ungraded record(s)")
    capped = len(run.truncations) + len(run.capped_verdicts)
    if kinds.count("capped") != capped:
        gaps.append(f"{kinds.count('capped')} filterable card(s) for "
                    f"{capped} capped field(s)")
    return gaps


def test_the_page_lists_what_was_capped_and_what_was_not_graded() -> None:
    """Both sections and the coverage row, in the Markdown report's words.

    A run that exits 2 because a claim was not graded has to name the claim
    on the page: the banner says the run is inconclusive, and the list is how
    a reader finds out which claims have no verdict.
    """
    run = ungraded_run()
    page = html_report.render(run)
    check(report.exit_code(run) == 2 and 'data-exit-code="2"' in page,
          "an ungraded record makes the run inconclusive, on the banner too")
    for gap in ungraded_gaps(run, page):
        check(False, f"ungraded: {gap}")
    check(HOSTILE not in page,
          "an ungraded record's claim id or defect reached the page unescaped")
    seen = "".join(parse(page, "ungraded escaping").text)
    check(seen.count(HOSTILE) >= 2,
          "the claim id and the defect must both survive as visible text")
    parity(run, "ungraded")

    # And a run with neither says so in both sections, in the Markdown's words.
    clean = fixture_run("dedup")
    page = html_report.render(clean)
    for gap in ungraded_gaps(clean, page):
        check(False, f"nothing capped, nothing ungraded: {gap}")


def test_the_ungraded_check_fires_on_a_page_without_the_sections() -> None:
    """Must fire: the shipped renderer, with each new part taken away in turn.

    Three seeds, one per part, each through the shipped `render`: the two
    sections left out, the two blocks emptied, and the coverage row left out.
    The page without any of the three is the page this renderer produced
    before it had them.
    """
    run = ungraded_run()
    section, rows = html_report._section, html_report._rows
    capping, unusable = html_report.capping_block, html_report.unusable_block
    label = "Claims submitted but not graded"
    try:
        html_report._section = lambda anchor, title, body: (
            [] if anchor in ("capped", "ungraded") else section(anchor, title, body))
        without_sections = ungraded_gaps(run, html_report.render(run))
        html_report._section = section

        html_report.capping_block = html_report.unusable_block = lambda run: []
        without_lists = ungraded_gaps(run, html_report.render(run))
        html_report.capping_block, html_report.unusable_block = capping, unusable

        html_report._rows = lambda pairs: rows(
            [pair for pair in pairs if pair[0] != label])
        without_row = ungraded_gaps(run, html_report.render(run))
    finally:
        html_report._section, html_report._rows = section, rows
        html_report.capping_block, html_report.unusable_block = capping, unusable
    check(any("no 'Not graded' section" in gap for gap in without_sections)
          and any("no 'Length capped' section" in gap for gap in without_sections),
          f"seeded check: a page without the two sections passed: {without_sections}")
    check(any("'Not graded' line" in gap for gap in without_lists)
          and any("'Length capped' line" in gap for gap in without_lists),
          f"seeded check: a page with the two sections empty passed: {without_lists}")
    check(without_row == [f"no coverage row {label!r} with the value 2"],
          f"seeded check: a page without the coverage row passed: {without_row}")
    check(ungraded_gaps(run, html_report.render(run)) == [],
          "the renderer was not put back after the seeds")


# --------------------------------------------------------------------------
# seeds: the shipped renderer with one expression changed
# --------------------------------------------------------------------------


@contextlib.contextmanager
def seeded(function: str, old: str, new: str):
    """The shipped `html_report.<function>` with `old` replaced by `new`.

    Rebuilt from the function's own source, never from a copy kept in this
    file: when the renderer rewords the expression a seed aims at, `old` is no
    longer in it and the seed raises instead of passing on the function as
    shipped. A raising test is a failing one (`main`).
    """
    shipped = getattr(html_report, function)
    source = textwrap.dedent(inspect.getsource(shipped))
    if source.count(old) != 1:
        raise AssertionError(
            f"seed for html_report.{function}: {old!r} is in its source "
            f"{source.count(old)} time(s), not once, so the seed aims at nothing")
    # Defined in the module's own namespace, which rebinds the name there:
    # every caller looks the function up in the module, and the seeded
    # function sees the module's other names as the shipped one does.
    exec(compile(source.replace(old, new), f"<seeded {function}>", "exec"),
         vars(html_report))
    try:
        yield
    finally:
        setattr(html_report, function, shipped)


def section_of(page: str, anchor: str) -> str:
    """What one section of the page holds, between its opening and closing tag."""
    opened = f'<section id="{anchor}">'
    if page.count(opened) != 1:
        return ""
    return page.split(opened, 1)[1].split("</section>", 1)[0]


# --------------------------------------------------------------------------
# a capped field whose value is hostile: escaped, and still one card
# --------------------------------------------------------------------------

# Everything a capped value could carry that the page must not act on: a tag,
# a quote and an angle bracket that would close what they are inside and open
# an element with a handler on it, the backtick and the `**` this module's own
# markup is written in, and three kinds of line break (the last is U+2028,
# which `str.splitlines` cuts at like the other two).
CAPPED_HOSTILE = (HOSTILE + '"><img src=x onerror="alert(2)">` **bold** `'
                  + "\nsecond line\r\nthird line" + chr(0x2028) + "fourth line")


def capped_hostile_run() -> Run:
    """Two capped fields and one capped rationale, the first field hostile.

    The path of a capped field is quoted from the model's answer, so it is
    the string to attack. Three records, so "one card per record" has a count
    to be wrong about.
    """
    run = structural_run()
    run.truncations = (
        parsing.Truncation(path=f"$.dispositions[0].{CAPPED_HOSTILE}",
                           original_length=912, cap=400),
        parsing.Truncation(path="$.dispositions[1].reason", original_length=433,
                           cap=400),
    )
    first = run.forward[0]
    run.forward[0] = Verdict(
        claim_id=first.claim_id, verdict=first.verdict, evidence=first.evidence,
        evidence_source=first.evidence_source, rationale=first.rationale,
        direction=first.direction, grounding=first.grounding,
        rationale_capped=True,
    )
    return run


def capped_gaps(run: Run, page: str) -> list[str]:
    """What is wrong with the Length capped section of `page`, as sentences."""
    gaps: list[str] = []
    section = section_of(page, "capped")
    if not section:
        return ["no Length capped section on the page"]
    shape = Shape()
    shape.feed(section)
    shape.close()
    if shape.errors or shape.stack:
        gaps.append(f"the section is not well formed: {shape.errors[:2]} "
                    f"{shape.stack}")
    # Nothing the value carried became markup.
    written = {"h2", "article", "p", "code"}
    if set(shape.tags) - written:
        gaps.append(f"a capped value put a tag on the page: "
                    f"{sorted(set(shape.tags) - written)}")
    names = {key for _, attrs in shape.attrs for key in attrs}
    if names - {"class", "data-filterable", "data-kind"}:
        gaps.append(f"a capped value put an attribute on the page: "
                    f"{sorted(names - {'class', 'data-filterable', 'data-kind'})}")
    if "<strong>" in section or "<em>" in section:
        gaps.append("a capped value was read for emphasis")
    if section.count("<code>") != section.count("</code>"):
        gaps.append("the code spans do not balance")
    # And all of it is still there to read, in one card per record.
    cards = [a for tag, a in shape.attrs if tag == "article"]
    records = len(run.truncations) + len(run.capped_verdicts)
    if len(cards) != records:
        gaps.append(f"{len(cards)} card(s) for {records} capped record(s)")
    if any(a.get("data-kind") != "capped" or "data-filterable" not in a
           for a in cards):
        gaps.append("a capped card is not filterable as one")
    seen = "".join(shape.text)
    hostile = [item.path for item in run.truncations if HOSTILE in item.path]
    for path in hostile:
        if path not in seen.replace("`", "") and path.replace("`", "") not in seen:
            gaps.append("the hostile value is not on the page as visible text")
        card = [part for part in section.split("</article>") if "second line" in part]
        if len(card) != 1 or "fourth line" not in card[0] or "&lt;script&gt;" not in card[0]:
            gaps.append("the hostile value is not whole inside one card")
    return gaps


def test_a_hostile_capped_value_is_escaped_and_stays_one_card() -> None:
    """A capped line is quoted from the model: a tag, a quote, markup, line breaks.

    The section is built from the Markdown report's lines, which wrap the
    value in backticks. None of that may become structure on the page, and a
    value that carries a line break is still one record: one card, with the
    whole value in it.
    """
    run = capped_hostile_run()
    page = html_report.render(run)
    for gap in capped_gaps(run, page):
        check(False, f"capped, hostile: {gap}")
    shape = parse(page, "capped hostile")
    check(shape.tags.count("script") == 1,
          f"the page must carry its own script element and no other: "
          f"{shape.tags.count('script')}")
    check("img" not in shape.tags
          and not any("onerror" in attrs for _, attrs in shape.attrs),
          "a capped value opened an element of its own, with a handler on it")

    # The claim id of a capped rationale is the model's word as well. Asked of
    # the block and not the page: an id no claim carries is one the inventory
    # refuses to count, which is a different check.
    first = run.forward[0]
    run.forward[0] = Verdict(
        claim_id=f"X-{CAPPED_HOSTILE}", verdict=first.verdict,
        evidence=first.evidence, evidence_source=first.evidence_source,
        rationale=first.rationale, direction=first.direction,
        grounding=first.grounding, rationale_capped=True,
    )
    block = "\n".join(html_report.capping_block(run))
    check(HOSTILE not in block and block.count("&lt;script&gt;") == 2,
          f"a hostile claim id in a capped rationale reached the page raw, or "
          f"was dropped: {block.count('&lt;script&gt;')} escaped tag(s)")
    check(block.count("<article ") == 3,
          f"three capped records are three cards whatever their values hold: "
          f"{block.count('<article ')}")


def test_the_capped_check_fires_when_the_escaping_or_the_card_is_taken_away() -> None:
    """Must fire: the shipped `capping_block`, with one expression changed.

    Two seeds. The first prints the capped line without escaping it. The
    second cuts each record at its line breaks, one card per line, which is
    what this block did before it was built per record.
    """
    run = capped_hostile_run()
    with seeded("capping_block", "code_only(text)", "_CODE.sub(r'<code>\\1</code>', text)"):
        raw = capped_gaps(run, html_report.render(run))
    with seeded("capping_block", "for text in capped",
                "for record in capped for text in record.splitlines() if text"):
        cut = capped_gaps(run, html_report.render(run))
    check(any("put a tag on the page" in gap for gap in raw)
          and any("put an attribute on the page" in gap for gap in raw),
          f"seeded check: a capped line printed unescaped passed: {raw}")
    check(any("card(s) for 3 capped record(s)" in gap for gap in cut)
          and any("not whole inside one card" in gap for gap in cut),
          f"seeded check: a capped record cut at its line breaks passed: {cut}")
    check(capped_gaps(run, html_report.render(run)) == [],
          "the renderer was not put back after the seeds")


# --------------------------------------------------------------------------
# the table of contents is the page's order, not only its members
# --------------------------------------------------------------------------


def toc_gaps(page: str, label: str) -> list[str]:
    """Whether the table of contents lists the sections in the page's order."""
    shape = parse(page, label)
    ids = [a["id"] for tag, a in shape.attrs if tag == "section" and "id" in a]
    targets = [href[1:] for href in attrs_of(shape, "a", "href")
               if href.startswith("#")]
    if targets != ["verdict", *ids]:
        return [f"{label}: the table of contents reads {targets} and the page "
                f"reads {['verdict', *ids]}"]
    return []


def with_additions(run: Run) -> Run:
    run.additions = ({"statement": "Something the sources do not say.",
                      "corrects": "", "basis": "own-knowledge", "source": "",
                      "reason": "confident"},)
    return run


def test_the_table_of_contents_is_in_the_order_of_the_page() -> None:
    """Every entry, in the order the sections come, on the widest pages.

    Presence was checked and order was not, so the two entries added last
    could sit at the end of the list above a page that prints them in the
    middle. A reader uses the list to find out what comes after what.
    """
    pages = {
        "merge": html_report.render(structural_run()),
        "merge with additions": html_report.render(with_additions(structural_run())),
        "ungraded": html_report.render(ungraded_run()),
        "verify": html_report.render(fixture_run("dedup")),
    }
    for label, page in pages.items():
        for gap in toc_gaps(page, label):
            check(False, gap)
    capped = [href for href in attrs_of(parse(pages["merge"], "toc"), "a", "href")
              if href in ("#findings", "#capped", "#ungraded", "#inventory")]
    check(capped == ["#findings", "#capped", "#ungraded", "#inventory"],
          f"Length capped and Not graded sit between Findings and Inventory in "
          f"the table of contents, as on the page: {capped}")

    # Must fire: the shipped `render` with the two entries appended at the end,
    # and with the additions entry put first.
    entries = 'toc[-1:-1] = [("capped", "Length capped"), ("ungraded", "Not graded")]'
    with seeded("render", entries, entries.replace("toc[-1:-1] =", "toc +=")):
        moved = toc_gaps(html_report.render(structural_run()), "seeded")
    with seeded("render", 'toc.append(("additions", added))',
                'toc.insert(0, ("additions", added))'):
        first = toc_gaps(html_report.render(with_additions(structural_run())), "seeded")
    check(len(moved) == 1 and len(first) == 1,
          f"seeded check: a table of contents out of the page's order passed: "
          f"{moved} {first}")


# --------------------------------------------------------------------------
# nothing capped, nothing ungraded: said inside the section it is about
# --------------------------------------------------------------------------


def empty_gaps(run: Run, page: str) -> list[str]:
    """Whether each of the two sections says, in itself, that it is empty.

    Looked for inside the section and not on the page: `None.` is a word
    several sections of a clean page print, so finding it somewhere says
    nothing about this one.
    """
    gaps = []
    for anchor, markdown in (("capped", report.capping_section(run)),
                             ("ungraded", report.unusable_section(run))):
        heading, sentence = [line for line in markdown.splitlines() if line]
        wanted = (f"<h2>{html_report.esc(heading.removeprefix('## '))}</h2>\n"
                  f'<p class="empty">{html_report.esc(sentence)}</p>')
        if section_of(page, anchor).strip() != wanted:
            gaps.append(f"the {anchor} section of a run with nothing in it does "
                        f"not read {sentence!r}: {section_of(page, anchor)!r}")
    return gaps


def test_an_empty_section_says_so_in_its_own_words() -> None:
    """`None.` under Length capped, and the full sentence under Not graded.

    A section left blank reads as a section that failed to render. Both
    sentences are the Markdown report's, and each is pinned to its section.
    """
    clean = fixture_run("dedup")
    check(report.capping_section(clean).splitlines()[2] == "None."
          and not clean.unusable,
          "the clean fixture has something capped or ungraded, so this test "
          "has no empty section to read")
    for gap in empty_gaps(clean, html_report.render(clean)):
        check(False, gap)

    # Must fire: each block, as shipped, returning nothing for an empty run.
    with seeded("capping_block",
                """return [f'<p class="empty">{esc(empty)}</p>']""", "return []"):
        no_capped = empty_gaps(clean, html_report.render(clean))
    with seeded("unusable_block",
                """return [f'<p class="empty">{esc(lead)}</p>']""", "return []"):
        no_ungraded = empty_gaps(clean, html_report.render(clean))
    check(len(no_capped) == 1 and "the capped section" in no_capped[0],
          f"seeded check: a Length capped section with no `None.` passed: "
          f"{no_capped}")
    check(len(no_ungraded) == 1 and "the ungraded section" in no_ungraded[0],
          f"seeded check: a Not graded section with no sentence passed: "
          f"{no_ungraded}")


# --------------------------------------------------------------------------
# one heading for the additions, in both reports
# --------------------------------------------------------------------------


def test_the_additions_heading_is_the_markdown_heading() -> None:
    """The section, its table-of-contents entry and the Markdown heading agree.

    The page headed it "Added from outside" under a Markdown report that says
    "Added from outside the documents": one section, two names, and a reader
    moving between the two reports has to work out that they are the same.
    """
    run = with_additions(structural_run())
    heading = report.additions_section(run).splitlines()[0]
    check(heading == "## Added from outside the documents",
          f"the Markdown heading this test is written against moved: {heading!r}")
    title = heading.removeprefix("## ")
    page = html_report.render(run)
    check(section_of(page, "additions").lstrip().startswith(f"<h2>{title}</h2>"),
          f"the section must be headed as the Markdown report heads it: "
          f"{section_of(page, 'additions')[:80]!r}")
    check(f'<li><a href="#additions">{title}</a></li>' in page,
          "and its table-of-contents entry must carry the same words and "
          "point at it")
    check(page.count(">Added from outside<") == 0,
          "the short heading must be gone from the page")

    # The words are the Markdown renderer's and not a second copy: reword the
    # Markdown heading and the page follows.
    shipped = report.additions_section
    try:
        report.additions_section = lambda run: shipped(run).replace(
            heading, "## Reworded for the probe", 1)
        follows = html_report.render(run)
    finally:
        report.additions_section = shipped
    check("<h2>Reworded for the probe</h2>" in section_of(follows, "additions")
          and '<a href="#additions">Reworded for the probe</a>' in follows,
          "seeded check: the page kept its own wording when the Markdown "
          "heading changed, so the two can drift again")


def main() -> int:
    tests = [value for name, value in sorted(globals().items())
             if name.startswith("test_") and callable(value)]
    for test in tests:
        try:
            test()
        except Exception as exc:  # noqa: BLE001 - a raising test is a failure
            failures.append(f"{test.__name__} raised {type(exc).__name__}: {exc}")
    for message in failures:
        print(f"FAIL {message}")
    print(f"html report: {len(tests) - len({f.split(':')[0] for f in failures})}"
          f"/{len(tests)} check group(s) clean"
          if failures else f"html report: {len(tests)} checks pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
