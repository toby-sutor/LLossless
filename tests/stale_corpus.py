"""Is a recorded corpus older than the prompts HEAD would send, for one role?

One question, asked by every tool that replays a committed corpus: were these
cassettes recorded under the prompt this checkout would send today? A corpus
recorded under an older prompt cannot be replayed -- the prompt digest is in
the cassette key, so every call misses -- and a replay that misses is either a
defect to fix or a re-record the operator has chosen to hold back. This module
tells the two apart, so no consumer grows its own copy of
the answer.

**Read from the cassette itself, not from a document about it.** A cassette
keeps the message it was sent, verbatim, and that message is its prompt
rendered. So each cassette is matched against the template HEAD would render
it from: the template's literal text must appear exactly, around its
placeholders, and a fidelity or title slot must hold one of HEAD's fragment
files exactly. A cassette that matches is fresh. An earlier check on the
m7 corpus read the recorded digest out of
`tests/responses/README.md`; a sentence in a README can go stale, and the
recording cannot.

**Stale by ruling is not the same as stale.** `HELD_BACK` lists each prompt
change whose re-record the operator has held back, as the text HEAD has and
the text the recording had. A cassette that matches HEAD's template once those
changes are undone is stale *by ruling*: the consumer reports it UNMEASURED,
never as a pass and never as a failure, until the operator says go. A cassette
that matches neither was recorded under some other prompt, and that is a
fault the consumer fails on the way it always has. Decompose and merge have no
held-back change, so a stale corpus of either is always a fault.

Nothing here reads git history: a published copy has one commit, and it must
give the same answer the working repository does.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"

# The templates a role's first message can be rendered from.
TEMPLATES: dict[str, tuple[str, ...]] = {
    "decompose": ("decompose",),
    "verify": ("verify", "verify_reverse", "verify_coverage"),
    "merge": ("merge",),
}

# Which fragment files fill which slot of which template, as globs under
# `prompts/`. What goes into a slot is the fragment's text, unrendered
# (`verify.compose_prompt`, `merge.compose_prompt`), so a slot is matched
# against the fragment files exactly. `verify_coverage` takes the forward
# direction's note (`verify.COVERAGE_FRAGMENT_ROLE`).
SLOTS: dict[tuple[str, str], str] = {
    ("verify", "fidelity_note"): "fidelity/*.verify.md",
    ("verify_reverse", "fidelity_note"): "fidelity/*.verify_reverse.md",
    ("verify_coverage", "fidelity_note"): "fidelity/*.verify.md",
    ("merge", "fidelity_rules"): "fidelity/*.merge.md",
    ("merge", "fidelity_example"): "fidelity/*.example.md",
    ("merge", "title_rule"): "title/*.md",
}


@dataclass(frozen=True)
class Change:
    """One prompt edit whose re-record is held back: where, what HEAD says, what it said."""

    decision: int
    template: str
    now: str
    was: str


# Every prompt change landed without its re-record, by operator ruling of
# 2026-09-26 ("Fix it but hold back the recordings"). Changes that are not
# prompt text (the verify ceiling) are held back too and have no entry here.
# Remove the entries a re-record covers, in the
# commit that imports it.
_ORDER_NOW = ("- Emit the fields in this order: claim_id, verdict, evidence, "
              "evidence_source, rationale.")
_ORDER_WAS = "- Emit the fields in this order: verdict, evidence, evidence_source, rationale."
HELD_BACK: tuple[Change, ...] = (
    Change(668, "verify", _ORDER_NOW, _ORDER_WAS),
    Change(668, "verify_reverse", _ORDER_NOW, _ORDER_WAS),
)

REASON = ("prompt changed after recording; re-record deferred by operator "
          "ruling of 2026-09-26")

# One placeholder: `{name}`, and not the literal `{{name}}` merge.md quotes.
_PLACEHOLDER = re.compile(r"(?<!\{)\{([a-z_]+)\}(?!\})")


def digest(text: str) -> str:
    """The repo's short prompt digest: sha256, first 12 hex characters."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _pattern(text: str, fragments: dict[str, tuple[str, ...]]) -> "re.Pattern":
    """A regex that fully matches a message rendered from template `text`.

    A slot named in `fragments` must hold one of its texts exactly; every other
    placeholder -- a document, a claim list, a filename -- matches anything.
    """
    parts, last = [], 0
    for found in _PLACEHOLDER.finditer(text):
        parts.append(re.escape(text[last:found.start()]))
        options = fragments.get(found.group(1))
        parts.append("(?:" + "|".join(re.escape(o) for o in options) + ")"
                     if options is not None else "(?:.*?)")
        last = found.end()
    parts.append(re.escape(text[last:]))
    return re.compile("".join(parts), re.S)


@dataclass(frozen=True)
class _Template:
    name: str
    text: str
    digest: str
    now: "re.Pattern"  # HEAD's template
    held: "re.Pattern | None"  # HEAD's template with its held-back changes undone
    decisions: tuple[int, ...]


@lru_cache(maxsize=None)
def _template(name: str, prompts: Path, held_back: tuple[Change, ...]) -> _Template:
    text = (prompts / f"{name}.md").read_text(encoding="utf-8")
    fragments = {
        slot: tuple(path.read_text(encoding="utf-8")
                    for path in sorted(prompts.glob(pattern)))
        for (template, slot), pattern in SLOTS.items() if template == name
    }
    changes = [c for c in held_back if c.template == name]
    undone = text
    for change in changes:
        # A listed change HEAD no longer carries undoes nothing, and so
        # excuses nothing: a reverted or reworded edit is a stale list, and
        # the cassettes it would have covered are faults.
        if change.now in undone:
            undone = undone.replace(change.now, change.was)
    return _Template(
        name=name, text=text, digest=digest(text),
        now=_pattern(text, fragments),
        held=_pattern(undone, fragments) if undone != text else None,
        decisions=tuple(sorted({c.decision for c in changes})),
    )


def _nearest(message: str, templates: list[_Template]) -> _Template:
    """The template a message matching none of them was most likely rendered from.

    The one sharing the longest opening with it: every template opens with
    literal text of its own, and an edit further down leaves that in place.
    """
    def shared(text: str) -> int:
        n = 0
        for a, b in zip(message, text):
            if a != b:
                break
            n += 1
        return n
    return max(templates, key=lambda t: shared(t.text))


def _first_message(path: Path) -> str | None:
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
        content = body["request"]["messages"][0]["content"]
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        return None
    return content if isinstance(content, str) else None


@dataclass(frozen=True)
class Staleness:
    """What one role's cassettes in one corpus were recorded under, when not HEAD's prompt."""

    role: str
    corpus: Path
    cassettes: int
    # Stale only because of changes in `HELD_BACK`, by template.
    held: tuple[tuple[str, int], ...]
    # Stale for any other reason, by the template each most likely came from.
    faults: tuple[tuple[str, int], ...]
    decisions: tuple[int, ...]

    @property
    def deferred(self) -> bool:
        """Every stale cassette is covered by a held-back change: UNMEASURED, not failing."""
        return bool(self.held) and not self.faults

    def reason(self) -> str:
        def listed(rows):
            return "; ".join(f"{name} ({n})" for name, n in rows)

        where = _shown(self.corpus)
        if self.deferred:
            count = sum(n for _, n in self.held)
            numbers = ", ".join(str(n) for n in self.decisions)
            return (f"{REASON.format(n=numbers)} -- {count} of {self.cassettes} "
                    f"{self.role} cassette(s) in {where} predate it: {listed(self.held)}")
        count = sum(n for _, n in self.faults)
        return (f"{count} of {self.cassettes} {self.role} cassette(s) in {where} were "
                f"recorded under a prompt HEAD does not send and no ruling holds "
                f"back: {listed(self.faults)}")


def _shown(corpus: Path) -> str:
    try:
        return str(corpus.relative_to(ROOT.resolve())) or "."
    except ValueError:
        return str(corpus)


def survey(corpus: Path, role: str, *, prompts: Path | None = None,
           held_back: tuple[Change, ...] = HELD_BACK) -> Staleness | None:
    """None if every `role` cassette in `corpus` matches HEAD's prompt, else what was found.

    One directory, not recursive: a corpus is one directory (`cassette.Store`).
    A directory with no cassettes of this role is not stale; it is not this
    role's corpus. `prompts` and `held_back` are for the tests, which hold a
    template at a version it is not at.
    """
    return _survey(Path(corpus).resolve(), role,
                   (prompts or PROMPTS).resolve(), tuple(held_back))


@lru_cache(maxsize=None)
def _survey(corpus: Path, role: str, prompts: Path,
            held_back: tuple[Change, ...]) -> Staleness | None:
    templates = [_template(name, prompts, held_back) for name in TEMPLATES[role]]
    total, held, faults, decisions = 0, {}, {}, set()
    for path in sorted(corpus.glob(f"{role}-*.json")):
        message = _first_message(path)
        if message is None:
            continue
        total += 1
        if any(t.now.fullmatch(message) for t in templates):
            continue
        covered = next((t for t in templates
                        if t.held is not None and t.held.fullmatch(message)), None)
        if covered is not None:
            label = f"prompts/{covered.name}.md, now {covered.digest}"
            held[label] = held.get(label, 0) + 1
            decisions.update(covered.decisions)
        else:
            nearest = _nearest(message, templates)
            label = f"prompts/{nearest.name}.md, now {nearest.digest}"
            faults[label] = faults.get(label, 0) + 1
    if not held and not faults:
        return None
    return Staleness(role=role, corpus=corpus, cassettes=total,
                     held=tuple(sorted(held.items())), faults=tuple(sorted(faults.items())),
                     decisions=tuple(sorted(decisions)))


def deferred_reason(corpus: Path, role: str) -> str | None:
    """The UNMEASURED reason when `role`'s corpus is stale by ruling alone, else None.

    None for a fresh corpus, and None for one with any cassette no ruling
    covers: that is a fault, and the caller's own miss handling reports it.
    """
    found = survey(corpus, role)
    return found.reason() if found is not None and found.deferred else None
