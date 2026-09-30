#!/usr/bin/env python3
"""Structural validation of the LLossless verification fixtures.

Run directly for a per-fixture report:

    python3 tests/test_fixtures.py

Exits 0 when every fixture is structurally valid, 1 otherwise. Also
collectable by pytest, if pytest is ever added.

This script checks the *shape* of the fixtures, never their correctness. It
does not judge whether an expected verdict is right, does not compare probe
text against document prose, and does not call a model. Those are what a
separate measurement layer checks. See tests/fixtures/SCHEMA.md.

Stdlib only. No network, no model call, no third-party dependency.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fixture_semantics
import run_detect  # noqa: E402
import socket_guard  # noqa: E402

# This module reads JSON off disk and opens no socket at all, which
# is exactly why it installs the guard: "opens no socket" is a claim, and the
# only difference between a module that honours it and one that quietly stops
# doing so is whether anything was watching.
socket_guard.install()

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
# must_not_extract assertions that hold for every document of every fixture.
# Not a directory, so discover() will not mistake it for a fixture.
GLOBAL_FILE = FIXTURES_DIR / "GLOBAL.json"

# Fixtures are discovered, not listed. A hand-maintained list means a new
# fixture directory sits on disk being validated by nothing until somebody
# remembers to add its name in three places, and the runners already discover
# from disk — so a listed validator would validate a different set than the one
# being measured. REQUIRED is the floor: it catches a fixture that disappears,
# which discovery alone would silently accept as "nothing to check".
REQUIRED = frozenset(
    {
        "attribution_invented",
        "attribution_swapped",
        "contradiction",
        "conflict_surfaced",
        "dedup",
        "disjoint_domains",
        "disjoint_sources",
        "dropped_claim",
        "hallucination",
        "numeric_drift",
        "ordering_only",
        "paraphrase",
        "structure_added",
    }
)


def discover() -> list[str]:
    return sorted(
        p.name for p in FIXTURES_DIR.iterdir() if p.is_dir() and (p / "expected.json").is_file()
    )

SOURCES = ("source_a.md", "source_b.md")
MERGED = "merged.md"
REQUIRED_FILES = SOURCES + (MERGED, "expected.json")

SCHEMA_VERSION = 4
KINDS = {"defect", "guard"}
# Why a pattern may never appear in an extracted claim. The two answers need
# opposite offline checks, so the fixture states which one it means rather than
# leaving the validator to guess from the pattern.
BASES = {"absent", "not_a_claim"}
DOCUMENTS = SOURCES + (MERGED,)
# The label and finding vocabularies a fixture may declare, and they are
# `SCHEMA.md`'s rather than `parsing.VERDICTS`'. Written out rather than
# imported, because a corpus validated by the code it feeds would be validating
# nothing.
#
# **This is deliberately narrower than the tool's vocabulary.**
# `parsing.VERDICTS` gained `PARTIAL` and `verify.FINDINGS` gained
# `partially_dropped` and `partially_invented`; no fixture here declares any of
# the three, because the twelve were written against a three-label vocabulary
# and no fixture's `expected.json` has been touched since. Widening the set would also mean widening
# `derive_finding` below and the table it points at in `SCHEMA.md`, at a
# schema version nothing has been written against — untested generality, in a
# file whose whole job is to be the thing that catches an untested assumption.
# The fixture that would need `PARTIAL` is still to be written, and it can bump the
# schema version and both tables together, with a fixture to prove them.
VERDICTS = {"SUPPORTED", "CONTRADICTED", "MISSING"}
FINDINGS = {"dropped", "contradicted", "hallucinated", "none"}
DIRECTIONS = {"source_to_merged", "merged_to_sources"}
DOCUMENT_DOMAIN = {
    "source_to_merged": set(SOURCES),
    "merged_to_sources": {MERGED},
}

# conflict_surfaced is built by copying contradiction and rewriting only
# merged.md. Asserting the sources stay byte-identical keeps the pair from
# drifting apart later, which would destroy the comparison it exists to make.
CLONE_PAIR = ("contradiction", "conflict_surfaced")

ANCHOR_RADIUS = 2
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

FIXTURE_REQUIRED = {
    "schema_version",
    "fixture",
    "kind",
    "held_out",
    "description",
    "plants",
    "merged",
    "prompts",
    "claim_count_band",
    "probes",
    "must_not_extract",
    "expected_conflicts",
    "expected_exit_code",
}
FIXTURE_OPTIONAL = {"note"}
PROBE_REQUIRED = (
    "probe_id",
    "direction",
    "document",
    "line",
    "text",
    "must_extract",
    "anchor",
    "match",
    "expected_verdict",
    "also_acceptable",
    "expected_finding",
)
ASSERTION_REQUIRED = ("assertion_id", "document", "basis", "pattern", "reason")
# A global assertion has no `document`: it applies to all of them. It also has
# no choice of `basis` -- see check_global_file.
GLOBAL_ASSERTION_REQUIRED = ("assertion_id", "basis", "pattern", "reason")
GLOBAL_REQUIRED = {"schema_version", "description", "must_not_extract"}


def derive_finding(verdict: str, direction: str) -> str:
    """The finding a verdict implies. See SCHEMA.md, 'Deriving expected_finding'.

    The final line is a fall-through for MISSING and reachable by nothing else:
    VERDICTS above is the closed set the caller has already checked against, and
    it holds three labels. If a later schema version admits a fourth, this
    function is where it stops being a fall-through and becomes a branch.
    """
    if verdict == "SUPPORTED":
        return "none"
    if verdict == "CONTRADICTED":
        return "contradicted"
    return "dropped" if direction == "source_to_merged" else "hallucinated"


def target_documents(direction: str) -> tuple[str, ...]:
    """What a claim in this direction is verified *against* — not where it came from."""
    return (MERGED,) if direction == "source_to_merged" else SOURCES


def all_of(report: Report, probe: dict, field: str, label: str) -> list[str] | None:
    """Read probe[field]['all_of'], shape-checked. None means it was unusable."""
    value = probe[field].get("all_of") if isinstance(probe[field], dict) else None
    if (
        isinstance(value, list)
        and value
        and all(isinstance(s, str) and s.strip() for s in value)
    ):
        return value
    report.fail(f"{label}: {field}.all_of must be a non-empty list of non-empty strings")
    return None


def anchor_window(lines: list[str], line: int) -> str:
    """Lines [line-2, line+2], clamped to the document, joined into one string.

    Joining matters: a probe's substrings may straddle a line break. Clamping
    matters: a probe on line 1 or on the final line must validate normally.
    """
    lo = max(0, line - 1 - ANCHOR_RADIUS)
    hi = min(len(lines), line + ANCHOR_RADIUS)
    return "\n".join(lines[lo:hi]).lower()


class Report:
    """Collects failures for one fixture."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.errors: list[str] = []

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def require(self, condition: bool, message: str) -> bool:
        if not condition:
            self.fail(message)
        return condition


def check_fixture(name: str) -> Report:
    report = Report(name)
    directory = FIXTURES_DIR / name

    if not directory.is_dir():
        report.fail(f"missing fixture directory {directory}")
        return report

    for filename in REQUIRED_FILES:
        if not (directory / filename).is_file():
            report.fail(f"missing required file {filename}")
    if report.errors:
        return report

    text = {name_: (directory / name_).read_text() for name_ in (SOURCES + (MERGED,))}
    lines = {name_: text[name_].splitlines() for name_ in text}

    try:
        data = json.loads((directory / "expected.json").read_text())
    except json.JSONDecodeError as exc:
        report.fail(f"expected.json does not parse: {exc}")
        return report

    if not isinstance(data, dict):
        report.fail("expected.json must be a JSON object")
        return report

    missing = FIXTURE_REQUIRED - set(data)
    if missing:
        report.fail(f"missing fixture-level keys: {', '.join(sorted(missing))}")
    unknown = set(data) - FIXTURE_REQUIRED - FIXTURE_OPTIONAL
    if unknown:
        report.fail(f"unknown fixture-level keys: {', '.join(sorted(unknown))}")
    if report.errors:
        return report

    check_fixture_level(report, name, data, text)
    probes = check_probes(report, data, text, lines)
    check_must_not_extract(report, data, text, probes)
    check_global_must_not_extract(report, data, text, probes)
    check_conflicts_and_exit_code(report, data, probes)
    return report


def check_must_not_extract(report: Report, data: dict, text: dict, probes: list[dict]) -> None:
    """Patterns no extracted claim may match. Structural checks only.

    Whether decompose actually honours them is measured by tests/run_decompose.py.
    What is checkable offline is that the assertion is *satisfiable*, and that is
    the whole job here. It fails to be when the pattern matches a `must_extract`
    probe on the same document — then the fixture demands and forbids the same
    claim — and it fails in a second way that depends on why the claim is
    forbidden. That is what `basis` declares:

    - `absent`: the text is not in the document at all, so a claim matching it
      would be invented. `dropped_claim` forbids a JSON Lines claim from the
      merge, where the fact was dropped. Here the pattern matching the
      document's own prose is the trap: a faithful decomposition would produce
      a matching claim and the fixture would punish correct behaviour.
    - `not_a_claim`: the text *is* in the document but is not an assertion about
      its subject — provenance, boilerplate, commentary on the merge itself.
      `structure_added` forbids the "Merged from source_a.md and source_b.md"
      line. Here the check runs the other way: a pattern that matches nothing in
      the document is inert, because there is no prose for a decomposer to
      wrongly turn into a claim.

    Both are scoped by `document`, which is why it is a declared field rather
    than an assumed `merged.md`: `dropped_claim` forbids a JSON Lines claim from
    the merge while requiring one from `source_b.md`, and those do not collide.
    """
    assertions = data["must_not_extract"]
    if not report.require(isinstance(assertions, list), "must_not_extract must be a list"):
        return

    seen: set[str] = set()
    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, dict):
            report.fail(f"must_not_extract #{index}: must be a JSON object")
            continue
        absent = [key for key in ASSERTION_REQUIRED if key not in assertion]
        if absent:
            report.fail(f"must_not_extract #{index}: missing keys: {', '.join(absent)}")
            continue
        unknown = set(assertion) - set(ASSERTION_REQUIRED)
        if unknown:
            report.fail(
                f"must_not_extract #{index}: unknown keys: {', '.join(sorted(unknown))}"
            )

        aid = assertion["assertion_id"]
        label = f"must_not_extract {aid!r}"
        if not (isinstance(aid, str) and KEBAB.match(aid)):
            report.fail(
                f"must_not_extract #{index}: assertion_id {aid!r} must be non-empty kebab-case"
            )
            continue
        if aid in seen:
            report.fail(f"{label}: duplicate assertion_id")
            continue
        seen.add(aid)

        report.require(
            isinstance(assertion["reason"], str) and assertion["reason"].strip(),
            f"{label}: reason must be a non-empty string",
        )

        document = assertion["document"]
        if not report.require(
            document in DOCUMENTS,
            f"{label}: document must be one of {sorted(DOCUMENTS)}, got {document!r}",
        ):
            continue

        basis = assertion["basis"]
        if not report.require(
            basis in BASES,
            f"{label}: basis must be one of {sorted(BASES)}, got {basis!r}",
        ):
            continue

        pattern = assertion["pattern"]
        if not isinstance(pattern, str) or not pattern.strip():
            report.fail(f"{label}: pattern must be a non-empty string")
            continue
        try:
            compiled = re.compile(pattern)
        except re.error as exc:
            report.fail(f"{label}: pattern does not compile: {exc}")
            continue

        found = compiled.search(text[document])
        if basis == "absent" and found:
            report.fail(
                f"{label}: basis 'absent' but the pattern matches {document}'s own prose "
                f"({found.group(0)[:60]!r}) — a correct decomposition would produce a claim "
                f"that matches it"
            )
        elif basis == "not_a_claim" and not found:
            report.fail(
                f"{label}: basis 'not_a_claim' but the pattern matches nothing in {document} — "
                f"there is no prose here for a decomposer to wrongly turn into a claim, so the "
                f"assertion is inert"
            )

        collides = [
            p["probe_id"]
            for p in probes
            if p.get("must_extract")
            and p.get("document") == document
            and isinstance(p.get("text"), str)
            and compiled.search(p["text"])
        ]
        if collides:
            report.fail(
                f"{label}: pattern matches must_extract probe(s) {', '.join(collides)} on the "
                f"same document — the fixture requires and forbids the same claim"
            )


def load_global() -> list[dict]:
    """The global assertions, or [] when the file is too broken to apply.

    check_global_file reports the breakage. This returns only the entries whose
    shape is sound enough to compile and match with, so one malformed entry
    cannot silently disarm the others.
    """
    try:
        data = json.loads(GLOBAL_FILE.read_text())
        assertions = data["must_not_extract"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return []
    if not isinstance(assertions, list):
        return []
    sound = []
    for assertion in assertions:
        if not isinstance(assertion, dict):
            continue
        if any(key not in assertion for key in GLOBAL_ASSERTION_REQUIRED):
            continue
        try:
            re.compile(assertion["pattern"])
        except (re.error, TypeError):
            continue
        sound.append(assertion)
    return sound


def check_global_file() -> Report:
    """Structural validation of GLOBAL.json itself, once rather than per fixture."""
    report = Report("GLOBAL.json")
    try:
        raw = GLOBAL_FILE.read_text()
    except OSError as exc:
        report.fail(f"cannot be read: {exc}")
        return report
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        report.fail(f"does not parse: {exc}")
        return report
    if not isinstance(data, dict):
        report.fail("must be a JSON object")
        return report

    missing = GLOBAL_REQUIRED - set(data)
    if missing:
        report.fail(f"missing keys: {', '.join(sorted(missing))}")
    unknown = set(data) - GLOBAL_REQUIRED
    if unknown:
        report.fail(f"unknown keys: {', '.join(sorted(unknown))}")
    if report.errors:
        return report

    report.require(
        data["schema_version"] == SCHEMA_VERSION,
        f"schema_version must be {SCHEMA_VERSION}, got {data['schema_version']!r}",
    )
    report.require(
        isinstance(data["description"], str) and data["description"].strip(),
        "description must be a non-empty string",
    )

    assertions = data["must_not_extract"]
    if not report.require(isinstance(assertions, list), "must_not_extract must be a list"):
        return report
    if not report.require(
        bool(assertions),
        "must_not_extract is empty; delete the file rather than leaving an inert one",
    ):
        return report

    seen: set[str] = set()
    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, dict):
            report.fail(f"#{index}: must be a JSON object")
            continue
        absent = [key for key in GLOBAL_ASSERTION_REQUIRED if key not in assertion]
        if absent:
            report.fail(f"#{index}: missing keys: {', '.join(absent)}")
            continue
        unknown = set(assertion) - set(GLOBAL_ASSERTION_REQUIRED)
        if unknown:
            report.fail(f"#{index}: unknown keys: {', '.join(sorted(unknown))}")

        aid = assertion["assertion_id"]
        if not (isinstance(aid, str) and KEBAB.match(aid)):
            report.fail(f"#{index}: assertion_id {aid!r} must be non-empty kebab-case")
            continue
        if aid in seen:
            report.fail(f"{aid!r}: duplicate assertion_id")
            continue
        seen.add(aid)

        report.require(
            isinstance(assertion["reason"], str) and assertion["reason"].strip(),
            f"{aid!r}: reason must be a non-empty string",
        )
        # 'not_a_claim' asserts the text is present in the document and must
        # not become a claim. Presence is a property of one document, so the
        # assertion cannot be made about all of them at once. Global entries
        # are 'absent' or they are nothing.
        report.require(
            assertion["basis"] == "absent",
            f"{aid!r}: a global assertion must have basis 'absent', got "
            f"{assertion['basis']!r} — 'not_a_claim' asserts the text is present in a "
            f"particular document, which no global assertion can know",
        )

        pattern = assertion["pattern"]
        if not isinstance(pattern, str) or not pattern.strip():
            report.fail(f"{aid!r}: pattern must be a non-empty string")
            continue
        try:
            re.compile(pattern)
        except re.error as exc:
            report.fail(f"{aid!r}: pattern does not compile: {exc}")

    return report


def check_global_must_not_extract(
    report: Report, data: dict, text: dict, probes: list[dict]
) -> None:
    """Apply GLOBAL.json's assertions to this fixture, on the same terms as its own.

    The satisfiability rules do not change because an assertion is global; only
    the scope does. Each pattern is checked against all three documents rather
    than the one a local assertion names, so a phrase that becomes legitimate
    prose in any future fixture fails here rather than turning that fixture's
    correct decomposition into a violation later.
    """
    local = {
        a.get("assertion_id")
        for a in data["must_not_extract"]
        if isinstance(a, dict)
    }
    for assertion in load_global():
        aid = assertion["assertion_id"]
        label = f"global must_not_extract {aid!r}"
        if aid in local:
            report.fail(
                f"{label}: this fixture declares an assertion_id that GLOBAL.json already "
                f"uses; ids must be unique across both"
            )
            continue
        compiled = re.compile(assertion["pattern"])
        for document in DOCUMENTS:
            found = compiled.search(text[document])
            if found:
                report.fail(
                    f"{label}: matches {document}'s own prose ({found.group(0)[:60]!r}) — "
                    f"a correct decomposition would produce a claim that matches it, so the "
                    f"assertion must be narrowed or scoped to a fixture"
                )
        collides = [
            p["probe_id"]
            for p in probes
            if p.get("must_extract")
            and isinstance(p.get("text"), str)
            and compiled.search(p["text"])
        ]
        if collides:
            report.fail(
                f"{label}: matches must_extract probe(s) {', '.join(collides)} — the suite "
                f"requires and forbids the same claim"
            )


def check_fixture_level(report: Report, name: str, data: dict, text: dict) -> None:
    report.require(
        data["schema_version"] == SCHEMA_VERSION,
        f"schema_version must be {SCHEMA_VERSION}, got {data['schema_version']!r}",
    )
    report.require(
        data["fixture"] == name,
        f"fixture field {data['fixture']!r} does not match directory name {name!r}",
    )
    report.require(
        data["merged"] == MERGED,
        f"merged must be {MERGED!r}, got {data['merged']!r}",
    )
    report.require(
        isinstance(data["description"], str) and data["description"].strip(),
        "description must be a non-empty string",
    )
    # Declared per fixture rather than inferred from a list somewhere, because
    # the claim it makes is about history — that no prompt was tuned against
    # this fixture — and history is not derivable from the file.
    report.require(
        isinstance(data["held_out"], bool),
        f"held_out must be a boolean, got {data['held_out']!r}",
    )

    kind = data["kind"]
    if report.require(kind in KINDS, f"kind must be one of {sorted(KINDS)}, got {kind!r}"):
        plants = data["plants"]
        if report.require(isinstance(plants, list), "plants must be a list"):
            if kind == "defect":
                report.require(
                    bool(plants), "kind 'defect' requires a non-empty plants list"
                )
            else:
                report.require(
                    not plants,
                    "kind 'guard' plants nothing, so plants must be [] "
                    f"(got {plants!r})",
                )

    band = data["claim_count_band"]
    if report.require(isinstance(band, dict), "claim_count_band must be an object"):
        for document in SOURCES + (MERGED,):
            if document not in band:
                report.fail(f"claim_count_band is missing an entry for {document}")
                continue
            bounds = band[document]
            ok = (
                isinstance(bounds, list)
                and len(bounds) == 2
                and all(isinstance(n, int) and not isinstance(n, bool) for n in bounds)
            )
            if not ok:
                report.fail(f"claim_count_band[{document}] must be [lo, hi] integers")
                continue
            lo, hi = bounds
            report.require(
                1 <= lo <= hi,
                f"claim_count_band[{document}] must satisfy 1 <= lo <= hi, got {bounds}",
            )

    report.require(
        isinstance(data["probes"], list) and bool(data["probes"]),
        "probes must be a non-empty list",
    )

    if name == CLONE_PAIR[1]:
        other = FIXTURES_DIR / CLONE_PAIR[0]
        for source in SOURCES:
            twin = other / source
            if not twin.is_file():
                report.fail(f"clone check: {CLONE_PAIR[0]}/{source} is missing")
            elif twin.read_text() != text[source]:
                report.fail(
                    f"clone check: {source} must be byte-identical to "
                    f"{CLONE_PAIR[0]}/{source} — the pair differs only in {MERGED}"
                )


def check_probes(report: Report, data: dict, text: dict, lines: dict) -> list[dict]:
    probes = [p for p in data["probes"] if isinstance(p, dict)]
    if len(probes) != len(data["probes"]):
        report.fail("every probe must be a JSON object")

    seen: set[str] = set()
    directions_used: set[str] = set()
    prompts = data["prompts"] if isinstance(data["prompts"], dict) else {}
    unprompted: dict[str, bool] = {}

    for index, probe in enumerate(probes):
        absent = [key for key in PROBE_REQUIRED if key not in probe]
        if absent:
            report.fail(f"probe #{index}: missing keys: {', '.join(absent)}")
            continue

        pid = probe["probe_id"]
        label = f"probe {pid!r}"
        if not (isinstance(pid, str) and KEBAB.match(pid)):
            report.fail(f"probe #{index}: probe_id {pid!r} must be non-empty kebab-case")
            continue
        if pid in seen:
            report.fail(f"{label}: duplicate probe_id")
            continue
        seen.add(pid)

        direction = probe["direction"]
        if not report.require(
            direction in DIRECTIONS,
            f"{label}: direction must be one of {sorted(DIRECTIONS)}, got {direction!r}",
        ):
            continue
        directions_used.add(direction)
        if "prompt" not in probe and direction not in prompts:
            unprompted[direction] = True

        document = probe["document"]
        allowed = DOCUMENT_DOMAIN[direction]
        if not report.require(
            document in allowed,
            f"{label}: direction {direction!r} allows document in {sorted(allowed)}, "
            f"got {document!r}",
        ):
            continue

        document_lines = lines[document]
        line = probe["line"]
        if not report.require(
            isinstance(line, int)
            and not isinstance(line, bool)
            and 1 <= line <= len(document_lines),
            f"{label}: line must be a 1-based integer within {document} "
            f"(1..{len(document_lines)}), got {line!r}",
        ):
            continue

        has_text = report.require(
            isinstance(probe["text"], str) and probe["text"].strip(),
            f"{label}: text must be a non-empty string",
        )

        # The two jobs, checked against the two different haystacks they are
        # each responsible for. Before they were split they shared one field
        # and one check, which meant only the anchoring job was ever verified
        # offline and the alignment job was taken on trust.
        anchors = all_of(report, probe, "anchor", label)
        if anchors is not None:
            window = anchor_window(document_lines, line)
            adrift = [s for s in anchors if s.lower() not in window]
            if adrift:
                report.fail(
                    f"{label}: anchor.all_of {', '.join(repr(s) for s in adrift)} not found in "
                    f"{document} lines {max(1, line - ANCHOR_RADIUS)}-"
                    f"{min(len(document_lines), line + ANCHOR_RADIUS)} — line reference drifted"
                )

        needles = all_of(report, probe, "match", label)
        if needles is not None and has_text:
            haystack = probe["text"].lower()
            unsayable = [s for s in needles if s.lower() not in haystack]
            if unsayable:
                report.fail(
                    f"{label}: match.all_of {', '.join(repr(s) for s in unsayable)} not found in "
                    f"the probe's own text — no extracted claim of this fact could match it"
                )
        report.require(
            isinstance(probe["must_extract"], bool),
            f"{label}: must_extract must be a boolean",
        )

        verdict = probe["expected_verdict"]
        if not report.require(
            verdict in VERDICTS,
            f"{label}: expected_verdict must be one of {sorted(VERDICTS)}, got {verdict!r}",
        ):
            continue

        also = probe["also_acceptable"]
        if report.require(isinstance(also, list), f"{label}: also_acceptable must be a list"):
            stray = [v for v in also if v not in VERDICTS]
            if stray:
                report.fail(
                    f"{label}: also_acceptable contains labels outside "
                    f"{sorted(VERDICTS)}: {stray}"
                )
            if verdict in also:
                report.fail(
                    f"{label}: also_acceptable must be disjoint from expected_verdict "
                    f"({verdict!r} appears in both)"
                )

        finding = probe["expected_finding"]
        if report.require(
            finding in FINDINGS,
            f"{label}: expected_finding must be one of {sorted(FINDINGS)}, got {finding!r}",
        ):
            derived = derive_finding(verdict, direction)
            report.require(
                finding == derived,
                f"{label}: expected_finding {finding!r} contradicts the derivation table — "
                f"{verdict} under {direction} is {derived!r}",
            )

        if "notes_evidence" in probe:
            report.require(
                isinstance(probe["notes_evidence"], str) and probe["notes_evidence"].strip(),
                f"{label}: notes_evidence must be a non-empty string",
            )

        if "expected_evidence_contains" in probe:
            spans = probe["expected_evidence_contains"]
            if not (
                isinstance(spans, list)
                and all(isinstance(span, str) and span.strip() for span in spans)
            ):
                report.fail(
                    f"{label}: expected_evidence_contains must be a list of non-empty strings"
                )
            elif not spans:
                # [] declares no expectation, exactly as omitting the field
                # does. What it adds is a place to say the silence is deliberate
                # — a probe whose two acceptable labels owe different evidence
                # has nothing single to assert — so it must carry the note that
                # says so, or it is indistinguishable from an unfinished probe.
                report.require(
                    isinstance(probe.get("notes_evidence"), str)
                    and bool(probe["notes_evidence"].strip()),
                    f"{label}: expected_evidence_contains [] asserts nothing; a probe that "
                    f"leaves evidence deliberately unasserted must say why in "
                    f"notes_evidence, and one that meant to assert something must list it",
                )
            else:
                # Checked against the target, not the document: evidence spans
                # come from what the claim is verified against.
                targets = target_documents(direction)
                haystack = "\n".join(text[t] for t in targets).lower()
                for span in spans:
                    if span.lower() not in haystack:
                        report.fail(
                            f"{label}: expected_evidence_contains {span!r} not found in "
                            f"target {' + '.join(targets)}"
                        )
                    # On a CONTRADICTED probe the span has one job: prove the
                    # model read the value that does the contradicting. A span
                    # already inside the claim proves nothing — a model that
                    # quoted the claim straight back would satisfy it. Required
                    # to discriminate, not merely to be present.
                    #
                    # Checked against the claim rather than the whole document
                    # it came from. Those are the same test right up until a
                    # merge surfaces both sides of a disagreement, which is the
                    # behaviour the project rewards: attribution_swapped's
                    # merged.md states 30 and 60 seconds on adjacent lines, so a
                    # document-wide rule excludes every span the fixture could
                    # possibly name.
                    elif verdict == "CONTRADICTED" and span.lower() in probe["text"].lower():
                        report.fail(
                            f"{label}: expected_evidence_contains {span!r} occurs in the "
                            f"probe's own claim, so it cannot show which of the two values "
                            f"the model quoted"
                        )

        if "expected_evidence_source" in probe:
            # A list, always, and read as "any one of these is a correct
            # answer". Facts stated in both sources — dedup's listen port — are
            # not gradeable down to one file, and a schema that could only name
            # one would have forced the fixture to invent a preference the
            # documents do not express.
            named = probe["expected_evidence_source"]
            targets = target_documents(direction)
            if not (isinstance(named, list) and all(isinstance(n, str) for n in named)):
                report.fail(
                    f"{label}: expected_evidence_source must be a list of target filenames, "
                    f"got {named!r}"
                )
            elif len(set(named)) != len(named):
                report.fail(f"{label}: expected_evidence_source lists a file twice: {named!r}")
            elif stray_files := [n for n in named if n not in targets]:
                report.fail(
                    f"{label}: expected_evidence_source {', '.join(map(repr, stray_files))} "
                    f"is not a target of {direction!r} — expected files from "
                    f"{', '.join(targets)}"
                )
            elif not named:
                # Same reading as an empty span list, one field along: no
                # expectation, and it must say that it means it.
                report.require(
                    isinstance(probe.get("notes_evidence"), str)
                    and bool(probe["notes_evidence"].strip()),
                    f"{label}: expected_evidence_source [] asserts nothing; say why in "
                    f"notes_evidence or name the files the fact may be cited from",
                )
            else:
                # Where the probe also declares spans, the file assertion is
                # checkable offline and is checked: every span must be in at
                # least one named file, and in no target outside the list.
                # Otherwise the span cannot show that the model read one of the
                # files the fixture names. On a single-element list this is
                # exactly "in that file and nowhere else"; on a list naming
                # every target it is vacuous, which is correct, because that
                # fixture is asserting the fact is genuinely shared.
                for span in probe.get("expected_evidence_contains", []):
                    outside = [
                        t for t in targets if t not in named and span.lower() in text[t].lower()
                    ]
                    if not any(span.lower() in text[n].lower() for n in named):
                        report.fail(
                            f"{label}: expected_evidence_contains {span!r} is in none of "
                            f"{', '.join(named)}, the files expected_evidence_source names"
                        )
                    elif outside:
                        report.fail(
                            f"{label}: expected_evidence_contains {span!r} is also in "
                            f"{', '.join(outside)}, which expected_evidence_source does not "
                            f"name, so it cannot show which file the model read"
                        )

    for direction in sorted(directions_used):
        if unprompted.get(direction):
            report.fail(
                f"no prompt declared for direction {direction!r} — set prompts[{direction!r}] "
                "or give every probe of that direction a 'prompt'"
            )

    return probes


def check_conflicts_and_exit_code(report: Report, data: dict, probes: list[dict]) -> None:
    known = {p["probe_id"] for p in probes if isinstance(p.get("probe_id"), str)}
    conflicts = data["expected_conflicts"]
    if not report.require(isinstance(conflicts, list), "expected_conflicts must be a list"):
        return

    seen: set[str] = set()
    for index, conflict in enumerate(conflicts):
        if not isinstance(conflict, dict):
            report.fail(f"conflict #{index}: must be a JSON object")
            continue
        for key in ("conflict_id", "attribute", "probes", "reason", "human_decision_required"):
            if key not in conflict:
                report.fail(f"conflict #{index}: missing key {key!r}")
        if "conflict_id" not in conflict or "probes" not in conflict:
            continue

        cid = conflict["conflict_id"]
        if not (isinstance(cid, str) and KEBAB.match(cid)):
            report.fail(f"conflict #{index}: conflict_id {cid!r} must be non-empty kebab-case")
        elif cid in seen:
            report.fail(f"conflict {cid!r}: duplicate conflict_id")
        else:
            seen.add(cid)

        if not (isinstance(conflict.get("attribute"), str) and conflict["attribute"].strip()):
            report.fail(f"conflict {cid!r}: attribute must be a non-empty string")

        members = conflict["probes"]
        if not (isinstance(members, list) and len(members) >= 2):
            report.fail(f"conflict {cid!r}: probes must list at least two probe ids")
            continue
        for pid in members:
            if pid not in known:
                report.fail(f"conflict {cid!r}: probe id {pid!r} is not declared in this fixture")

    declared = data["expected_exit_code"]
    if not (isinstance(declared, dict) and set(declared) == {"strict", "lenient"}):
        report.fail("expected_exit_code must be an object with exactly 'strict' and 'lenient'")
        return

    # Derived from the probes alone, through the implementation's own
    # label-to-finding table. The derivation this replaced also read
    # `expected_conflicts`, and no file in `src/llossless` reads that field,
    # so a fixture could declare any exit code it liked as
    # long as it listed a conflict, and two of them did for months. A check
    # that runs through a mechanism nobody built cannot fail. Every conflict
    # assertion above still stands; it is shape validation, which is what it
    # always was.
    implied = fixture_semantics.implied_exit_codes(data)
    for mode in ("strict", "lenient"):
        report.require(
            declared[mode] == implied[mode],
            f"expected_exit_code[{mode}] is {declared[mode]!r} but this fixture's own probes "
            f"imply {implied[mode]}. The probes win: an answer key that disagrees with itself "
            f"scores the arm on the disagreement.",
        )

    # `kind` is a third statement about the same run, and a third statement can
    # drift from the other two. A defect that implies exit 0 has nothing to
    # detect; a guard that implies exit 1 fails every correct run.
    kind = data.get("kind")
    if kind in ("defect", "guard"):
        report.require(
            implied["strict"] == (1 if kind == "defect" else 0),
            f"kind is {kind!r} but the probes imply strict exit {implied['strict']}. "
            f"A defect must have something to find and a guard must not.",
        )


# A fixture that disagrees with itself, and one that agrees, built here rather
# than on disk. Both go through `check_conflicts_and_exit_code` itself, not
# through a second copy of its arithmetic: a probe that rebuilds the expression
# it is testing stays green when the shipped one is reverted.
#
# The seeds matter because this check was written after two real fixtures had
# disagreed with themselves for months while every gate stayed green. A check
# that has never been shown to fire is a check whose green means nothing
# until something below is staged to make it fail.
def _probe(pid: str, verdict: str, also: list[str] | None = None,
           direction: str = "source_to_merged") -> dict:
    return {"probe_id": pid, "direction": direction, "expected_verdict": verdict,
            "also_acceptable": list(also or [])}


SEEDED_INCONSISTENT = (
    (
        "a guard whose probes imply exit 0 declaring exit 1",
        {"kind": "guard", "expected_conflicts": [],
         "expected_exit_code": {"strict": 1, "lenient": 1},
         "probes": [_probe("p-one", "SUPPORTED"), _probe("p-two", "SUPPORTED")]},
    ),
    (
        "a defect sanctioning a clean reading while declaring lenient 1",
        {"kind": "defect", "expected_conflicts": [],
         "expected_exit_code": {"strict": 1, "lenient": 1},
         "probes": [_probe("p-one", "CONTRADICTED", ["SUPPORTED"])]},
    ),
    (
        "a defect with nothing to detect",
        {"kind": "defect", "expected_conflicts": [],
         "expected_exit_code": {"strict": 0, "lenient": 0},
         "probes": [_probe("p-one", "SUPPORTED")]},
    ),
    (
        "a conflict listed, which used to be enough to justify any exit code",
        {"kind": "guard",
         "expected_conflicts": [{"conflict_id": "seeded", "attribute": "a",
                                 "probes": ["p-one", "p-two"], "reason": "seeded",
                                 "human_decision_required": True}],
         "expected_exit_code": {"strict": 1, "lenient": 1},
         "probes": [_probe("p-one", "SUPPORTED"), _probe("p-two", "SUPPORTED")]},
    ),
)

SEEDED_CONSISTENT = (
    (
        "a clean guard",
        {"kind": "guard", "expected_conflicts": [],
         "expected_exit_code": {"strict": 0, "lenient": 0},
         "probes": [_probe("p-one", "SUPPORTED")]},
    ),
    (
        "a defect with a soft probe, strict 1 and lenient 0",
        {"kind": "defect", "expected_conflicts": [],
         "expected_exit_code": {"strict": 1, "lenient": 0},
         "probes": [_probe("p-one", "CONTRADICTED", ["SUPPORTED"])]},
    ),
    (
        "a defect with a hard probe",
        {"kind": "defect", "expected_conflicts": [],
         "expected_exit_code": {"strict": 1, "lenient": 1},
         "probes": [_probe("p-one", "MISSING")]},
    ),
)


def check_exit_code_derivation() -> Report:
    """The derivation's own must-fire and must-not-fire probes."""
    report = Report("exit-code derivation")
    for why, data in SEEDED_INCONSISTENT:
        seeded = Report("seed")
        check_conflicts_and_exit_code(seeded, data, data["probes"])
        if not seeded.errors:
            report.fail(
                f"must-fire seed passed: {why}. The check cannot see a fixture that "
                f"disagrees with itself, so a clean run of it proves nothing."
            )
    for why, data in SEEDED_CONSISTENT:
        seeded = Report("seed")
        check_conflicts_and_exit_code(seeded, data, data["probes"])
        for error in seeded.errors:
            report.fail(f"must-not-fire seed failed: {why}: {error}")
    return report


def check_preregistered_block() -> Report:
    """`run_detect.PREREGISTERED_BLOCK` against the runs that defined it.

    The scored detection block is a list and not a rule, because what excludes
    `list_structure` is its history rather than any field it carries. A list is
    a second place for the set to be wrong, so it is checked against the block
    as it was actually run: every graded run record (withheld with the paper) records the
    fixtures its arm graded, and the constant must equal that set exactly. If a
    fixture is ever added to or dropped from the block, three records disagree
    with it and this fails until the change is deliberate.
    """
    report = Report("pre-registered detection block")
    block = set(run_detect.PREREGISTERED_BLOCK)
    report.require(
        len(run_detect.PREREGISTERED_BLOCK) == len(block),
        "PREREGISTERED_BLOCK repeats a name",
    )
    on_disk = set(run_detect.fixture_names())
    report.require(
        block <= on_disk,
        f"PREREGISTERED_BLOCK names fixtures that do not exist: "
        f"{sorted(block - on_disk)}",
    )
    # `paper` is NOT-PUBLISHED wholesale, so a published clone has no records to
    # check against and this half of the check genuinely cannot run there. It
    # says so on its own output rather than reporting a pass it did not earn,
    # the same way `scripts/build_arm_bundle.py` reports a withheld detector.
    directory = FIXTURES_DIR.parents[1] / "paper" / "records"
    if not directory.is_dir():
        report.name += " (no graded run records in this tree, so unchecked against a run)"
        return report
    records = sorted(directory.glob("half1-*.json"))
    report.require(bool(records),
                   "the graded-records directory exists but holds no half1-*.json to check the "
                   "block against")
    for path in records:
        graded = {r["fixture"]
                  for r in json.loads(path.read_text(encoding="utf-8"))["records"]}
        report.require(
            graded == block,
            f"{path.name} graded {sorted(graded ^ block)} outside "
            f"PREREGISTERED_BLOCK; the constant and the run disagree",
        )
    return report


def validate_all() -> list[Report]:
    found = discover()
    reports = ([check_global_file(), check_exit_code_derivation(),
                check_preregistered_block()]
               + [check_fixture(name) for name in found])

    missing = sorted(REQUIRED - set(found))
    if missing:
        gone = Report("fixture set")
        for name in missing:
            gone.errors.append(
                f"required fixture {name!r} is not on disk; it is part of the measured "
                f"set and removing it silently changes every reported number"
            )
        reports.append(gone)
    return reports


def main() -> int:
    reports = validate_all()
    width = max(len(r.name) for r in reports) + 2
    for report in reports:
        dots = "." * (width - len(report.name))
        if report.errors:
            print(f"  {report.name} {dots} FAIL")
            for error in report.errors:
                print(f"      - {error}")
        else:
            print(f"  {report.name} {dots} ok")

    failed = [r for r in reports if r.errors]
    total = len(reports)
    print()
    if failed:
        print(f"  {total - len(failed)}/{total} fixtures valid, {len(failed)} failing")
        return 1
    print(f"  {total}/{total} fixtures valid")
    return 0


def test_fixtures() -> None:
    """pytest entry point, if pytest is ever added."""
    failures = [f"{r.name}: {e}" for r in validate_all() for e in r.errors]
    assert not failures, "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
