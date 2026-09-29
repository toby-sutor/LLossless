"""Pass 2 — break a document into atomic, independently checkable claims.

An atomic claim is one factual assertion that can be checked on its own. This
pass runs over each source document independently, and over the merged document
when checking the reverse direction. It never sees another document, so it
cannot be influenced by what the merge did.

Claim extraction quality is the accuracy ceiling for the whole tool: a fact
never extracted can never be found missing. That is why the anchoring below is
strict rather than best-effort.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path

from . import parsing, prompts, segment, structured, window
from .client import Client

# How far an extracted claim's line may sit from a fixture probe's line and
# still count as the same place. Matches the fixture anchoring window in
# tests/fixtures/SCHEMA.md deliberately: the two must not drift apart.
ANCHOR_RADIUS = 2

# The claim-id prefix for the merged document. The sources need no table: their
# letter is read back off the canonical name by `segment.document_letter`, so
# `source_c.md` gets `C` without anyone extending anything. `merged.md` is not a
# canonical source name and so is the one that has to be said, and it is said
# here rather than defaulted to a first character — `M` is the letter the
# brief's own example ids use.
MERGED_LETTER = "M"

CLAIM_SCHEMA = {
    "type": "object",
    "properties": {
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "line": {"type": "integer"},
                    "span": {"type": "string"},
                },
                "required": ["text", "line", "span"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["claims"],
    "additionalProperties": False,
}


@dataclass(frozen=True)
class Claim:
    """The brief's claim contract, plus what it takes to trust the line number.

    id, source, text and line are the contract. span and anchored are how the
    line number earns belief: a model asked to count lines will sometimes be
    wrong, and a line reference nobody checked is worse than none at all,
    because it looks authoritative in a report.
    """

    id: str
    source: str
    text: str
    line: int
    span: str
    anchored: bool

    def as_dict(self) -> dict:
        return asdict(self)


# How many times a claim list writes its document out, counted in tokens, for
# the output ceiling (`budget_tokens`). A claim restates part of a sentence (one
# copy of the document), quotes that sentence as its span (a second) and
# carries its own scaffolding -- key names, quotes, the line number -- which on
# short lines costs about a third. That is three copies for a decomposer that
# makes one claim per sentence, and the ceiling allows two of them: the 27B
# made 2.63 times the 8B's output on the same narrative document, splitting
# what the 8B kept whole. Measured against the constant rather than fitted to
# it: over the 282 recorded answers on two models the most any wrote was 3.82
# copies (qwen3:8b, a 135-character document), and 3.46 on the 27B.
# DECISIONS 587.
CLAIM_COPIES = 6


def budget_tokens(text: str, *, thinking: bool) -> int:
    """`max_tokens` for decomposing `text`, sized from the document before the call.

    The decompose role had no ceiling, so a generation that never ended was
    bounded only by `--timeout`: Phase 4 ran one for 904 seconds (427, 429).
    This is `merge.budget_tokens`' shape applied to the one-document role:
    `CLAIM_COPIES` of the document, rounded up to a whole `BUDGET_STEP`, plus
    one more step added after the rounding as a fixed per-response floor --
    `MISMATCH_ALLOWANCE`'s reason, and what keeps a two-line document clear,
    where the scaffolding outweighs the text.

    `thinking` adds `merge.REASONING_ALLOWANCE`, the one measurement of a
    reasoning trace this project has. Without it a reasoning model asked to
    think spends the ceiling reasoning and returns nothing, which is what 385
    recorded on the merge role. With thinking off nothing is reasoned, so
    nothing is allowed for it and the bound on a runaway stays tight.

    `max_tokens` is a cassette-key component, so this re-keys every decompose
    recording made without it. That is why it landed with a re-record.
    """
    # Imported here: `merge` imports this module, and these four are merge's
    # constants on purpose -- one step, one token estimate, one escaping rule
    # and one reasoning allowance for both roles, never a copy of each.
    from .merge import BUDGET_STEP, CHARS_PER_TOKEN, REASONING_ALLOWANCE, escaped_length

    body = CLAIM_COPIES * escaped_length(text)
    rounded = -(-int(body / CHARS_PER_TOKEN) // BUDGET_STEP) * BUDGET_STEP
    return rounded + BUDGET_STEP + (REASONING_ALLOWANCE if thinking else 0)


def fit_to_window(ceiling: int | None, *, prompt_tokens: int, served) -> tuple[int, int | None]:
    """(tokens the preflight charges, `max_tokens` sent) for one decompose call.

    DECISIONS 588. The ceiling is a runaway cap, not a forecast of the answer,
    and the window already caps a runaway: a generation cannot run past what
    the window leaves after the prompt. So the ceiling is cut to that room
    rather than charged whole, and the preflight charges the prompt plus one
    `BUDGET_STEP`, the per-response floor every ceiling carries. Charging the
    whole ceiling (587) refused every document over about 13,000 characters at
    32,768, though the ceiling allows 6 copies of the document and the most any
    recorded answer wrote is 3.82. Merge charges its whole budget on purpose:
    there the budget is the expected size of the output, so a window that
    cannot hold it cannot hold the merge.

    `served` is None where no window is known (a replay or a dry run, which
    send nothing): the ceiling goes out as is. Where the cut does not bite --
    every document the corpus was recorded on -- `max_tokens` is the ceiling,
    so the cassette keys do not move. No ceiling (a `CEILING_MODEL` profile)
    charges the prompt alone and sends none, as before.
    """
    from .merge import BUDGET_STEP

    if ceiling is None:
        return prompt_tokens, None
    if served is None:
        return prompt_tokens + BUDGET_STEP, ceiling
    return prompt_tokens + BUDGET_STEP, min(ceiling, served.tokens - prompt_tokens)


def number_lines(text: str) -> str:
    """Render a document as `  12 | text`, 1-based, blank lines included.

    Blank lines are numbered too. Dropping them would shift every number below,
    which is the exact failure this is meant to prevent.
    """
    lines = text.splitlines()
    width = len(str(len(lines))) if lines else 1
    return "\n".join(f"{i:>{width}} | {line}" for i, line in enumerate(lines, start=1))


def normalise(text: str) -> str:
    """Collapse whitespace and case for comparison. Values are untouched."""
    return re.sub(r"\s+", " ", text).strip().lower()


def anchor(span: str, reported_line: int, lines: list[str]) -> tuple[int, bool]:
    """Find the line a span actually sits on. Returns (line, anchored).

    The model's line number is a hint; the span it copied is the evidence. We
    locate the span in the document and take the occurrence nearest the hint —
    the fixtures share one fact pool, so a short span can honestly occur twice,
    and nearest-to-hint breaks that tie better than first-match.

    anchored=False means the span was not found: the model paraphrased instead
    of copying. We keep its line rather than guess, and the caller can see that
    the number is unverified. A line reference nobody checked is worse than none
    at all, because a report renders it with the same authority as a real one.
    """
    needle = normalise(span)
    if not needle or not lines:
        return reported_line, False

    matches = [i for i, line in enumerate(lines, start=1) if needle in normalise(line)]

    if not matches:
        # The span may wrap a hard line break. Slide a small window over
        # consecutive lines and report the window's first line.
        for width in (2, 3):
            for i in range(len(lines) - width + 1):
                if needle in normalise(" ".join(lines[i : i + width])):
                    matches.append(i + 1)
            if matches:
                break

    if not matches:
        return reported_line, False

    return min(matches, key=lambda i: (abs(i - reported_line), i)), True


def claim_id(source: str, index: int) -> str:
    """A-001, B-014, M-007. Stable within a document, not across documents.

    A canonical source name is read for the letter it already carries, so a
    third source is `C-001` without a table being extended. Anything else — the
    merge, or a caller passing a real filename — falls back to a first
    character, which is all the old table did for the names it did not list.
    """
    letter = (
        segment.document_letter(source).upper()
        or (MERGED_LETTER if source == segment.MERGED_NAME else "")
        or Path(source).stem[:1].upper()
        or "X"
    )
    return f"{letter}-{index:03d}"


def decompose_text(
    client: Client,
    text: str,
    source: str,
    prompt: prompts.Prompt | None = None,
) -> list[Claim]:
    """Extract claims from one document. One model call, schema-constrained.

    Raises client.SchemaFailure if the model could not be made to answer in a
    usable form. That propagates rather than being swallowed into an empty
    claim list: zero claims and "the call failed" look identical in a coverage
    table and mean opposite things.
    """
    prompt = prompt or prompts.load("decompose")
    rendered = prompt.render(document=number_lines(text))
    # The ceiling, on merge's rule for which profiles get one (443): a
    # `CEILING_MODEL` profile sends none and the endpoint applies its own.
    if (structured.profile_for(client.settings.profile).output_ceiling
            == structured.CEILING_MODEL):
        budget = None
    else:
        budget = budget_tokens(text, thinking=client.thinking_for("decompose", None))
    # Task 41's guard, which merge has had since it was written and this role
    # never did. An overrun prompt is trimmed from the front by the server and
    # answered anyway, so the claims would come from the tail of the document
    # with nothing in the report saying so. The output is charged as a small
    # reserve, and the ceiling is cut to what the window leaves (588): vLLM
    # refuses a request whose prompt and `max_tokens` exceed the model length,
    # and ollama shifts the prompt out of the context to make room for a long
    # generation, so the ceiling sent must fit beside the prompt.
    if not client.sends_nothing:
        served = client.served_window("decompose")
        needed, sent = fit_to_window(
            budget, prompt_tokens=len(rendered) // window.CHARS_PER_TOKEN, served=served)
        window.preflight(
            served,
            needed=needed,
            what=f"decomposing {source or 'a document'}",
            role="decompose",
        )
        budget = sent
    payload = client.complete(
        role="decompose",
        prompt=prompt,
        messages=[{"role": "user", "content": rendered}],
        schema=CLAIM_SCHEMA,
        schema_name="emit_claims",
        semantic=parsing.check_claims,
        max_tokens=budget,
    ).payload

    lines = text.splitlines()
    claims: list[Claim] = []
    for item in payload["claims"]:
        if not isinstance(item, dict):
            continue
        claim_text = str(item.get("text", "")).strip()
        span = str(item.get("span", "")).strip()
        if not claim_text:
            continue

        reported = item.get("line")
        reported = reported if isinstance(reported, int) else 0
        reported = max(1, min(reported, len(lines))) if lines else 1

        line, anchored = anchor(span, reported, lines)
        claims.append(
            Claim(
                id=claim_id(source, len(claims) + 1),
                source=source,
                text=claim_text,
                line=line,
                span=span,
                anchored=anchored,
            )
        )
    return claims
