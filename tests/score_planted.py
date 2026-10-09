#!/usr/bin/env python3
"""Score a merge of a `tests/handwritten` pair against its planted errors. Offline; no call.

**The answer key is computed, never typed.** The operator took a text, kept it
as `reference.md`, planted factual errors in a copy and split the copy into the
pair's sources. `planted()` diffs the reference against the sources joined,
word by word (`difflib.SequenceMatcher`, `autojunk=False`), and every changed
place is a planted error. Two pairs carry planted errors, `voyager` and
`bip39`; `mahjongg` carries none and is scored as a false-correction control
(`--control`, below). The key is derived by diff, and a later ruling changed
how it counts.

**Counting rule: one error per changed unit** (the operator's ruling,
2026-09-25). A unit is

- a **date or timestamp**, as one phrase: "Nov. 4, 1985" becoming
  "Jan. 31, 1987" is one error, and so is "17:59 UT Jan. 24, 1986" becoming
  "17:59 ED Jan. 24, 1968";
- a **quantity**, a number with its unit: "5.5 hours" becoming "6.4 days" is
  one error, and "450 miles per hour (724 kilometers per hour)" becoming
  "450 km/h (72400 meters per hour)" is two, one per quantity;
- otherwise a **word**: each word that differs in a word-for-word substitution
  is one error ("Voyager 2's long-range" to "Voyager 1's short-range" is two),
  and a span rewritten to a different length is one.

Units are found by two patterns over the reference's text (`DATE`,
`QUANTITY`), never by a list of errors. A diff span that crosses two units is
split at the unit boundary when the planted side has the same number of units
there; the pieces a unit holds are listed by `--key` and `--review`, so the
grouping can be checked. A number-format change ("4.5" to "4,5") is an error:
the diff compares words exactly as written.

**The join.** A second source that opens with the first source's title line
has that line dropped before the join, as the reference carries it once.

**What is scored is the merged text**, not what the run says it did. Each
piece of an error is looked for at its place in the merge:

- **fixed**: the original wording is there and the planted wording is not;
- **kept**: the planted wording is there and the original is not;
- **other**: neither, or both.

An error is fixed when every piece is fixed, kept when every piece is kept, and
`other` otherwise, with what was found. "At its place" is the sentence or
sentences of the merge the word alignment maps the error's sentence onto, plus
the merge sentence sharing most of its words if the merge moved it -- when it
shares at least half the error sentence's words and a third of its own, so a
three-word heading is not matched to a long sentence that happens to hold its
words. Inside them a word is looked for with a neighbouring word; a wording
that occurs once in its own version and never in the other is also looked for
bare. A number written as a word reads as its digits ("ten" is "10"). A planted
insertion ("Bianca II") is fixed when the reference's word before it is there
without it: deleting "and Bianca II" drops the moon and is `other`, not a fix.
A correct fix in other words ("mph (724 km/h)") is `other`:
read its text.

**Style moves nothing.** A single newline inside a paragraph is a space,
not a sentence break: a sentence ends at a blank line, at a line that is a
heading, list item, table row or quote (or before one), or at a word ending in
`.`, `!` or `?` followed by a capital. Every word is compared in Unicode NFC,
with `*`, `_` and backticks taken off anywhere in it, so `**2**'s` is `2's`.

**The declared column** is whether a record the merge filed (`corrects` or
`reason`, over `additions`, `dispositions` and `declarations`) quotes a planted
wording. A run that declares a fix it did not make, or fixes one silently,
shows up as a difference between the two columns.

**The control, `--control`.** A pair with no planted errors (`mahjongg`:
183/183 of its reference's sentences are verbatim in its sources). Every
sentence of the merge, by `segment.py`'s own unit, is looked up verbatim
(whitespace-normalised) in the sources; one that is not is compared, word by
word, with the source sentence it shares most words with. A **false
correction** is a merge sentence that substitutes words for its source's, or a
declared correction record: there is nothing to correct. The two are reported
as two columns, `changed` and `declared`, and `false_corrections` counts a
correction once: a declared record that names a changed sentence's wording is
that sentence's record, not a second correction (682; before, a model that
declared the change it made scored twice what a silent one did). A sentence
that only drops words, or only adds some, is listed apart, and so is one with
no source counterpart. Texts are compared in NFC with `*`, `_` and backticks
off. Every one is printed, to be read: the count is mechanical.

Input, per file: a `report.json` (the merged text is read from its
`merged_written_to`), a merge answer (bare, or wrapped in prose or a code
fence), a `claude --output-format json` wrapper around one, or a plain `.md`
merged document (no declared column).

Usage:
    score_planted.py --pair voyager FILE...        # score merges
    score_planted.py --pair bip39 --key            # print the derived key
    score_planted.py --pair voyager --review       # the key as a review table
    score_planted.py --pair voyager -v FILE...     # and every error's outcome
    score_planted.py --pair voyager --json FILE...
    score_planted.py --pair mahjongg --control FILE...

The controls (the reference scores every error fixed, the plain concatenation
of the sources none) are `tests/test_score_voyager.py`.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "tests" / "handwritten"

# Em and en dash separate words ("Uranus—a journey"); a hyphen joins them.
DASHES = "—–"
# Stripped from both ends of a word before comparing. Internal punctuation
# stays: "4,5" against "4.5" and "17.560" against "17,560" are planted errors.
EDGE = "\"'“”()[]{}<>.,;:!?*_#`"
# Inline marks a merge may add or drop without changing a word, taken off
# anywhere in a token: `**2**'s` is `2's`.
MARKS = re.compile(r"[*_`]")
# A line that is block notation rather than a paragraph's continuation: a
# single newline before or after one still ends a sentence.
BLOCK_LINE = re.compile(r"^\s{0,3}(?:#{1,6}\s|[-*+]\s|\d{1,9}[.)]\s|>|\||`{3}|~{3})")
# A number written as a word reads as its digits, so "ten new moons" is the
# reference's "10 new moons". Compounds ("four-hundred") are not read.
NUMBER_WORDS = {w: str(n) for n, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}

# --- units -----------------------------------------------------------------
# Patterns, not a list: they say what a date and a quantity look like, and the
# diff decides which of them changed.
_MONTH = (r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|"
          r"Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?")
# A clock time, with a time zone of two to four capitals if one follows it.
_TIME = r"\d{1,2}:\d{2}(?::\d{2})?(?:\s+[A-Z]{2,4})?"
DATE = re.compile(
    rf"(?:{_TIME}\s+)?(?:\b{_MONTH}\s+\d{{1,2}},?\s+\d{{4}}\b"
    rf"|\b\d{{1,2}}\.?\s+{_MONTH}\s+\d{{4}}\b|\b{_MONTH}\s+\d{{4}}\b)")
_NUMBER = (r"(?:\d[\d,.]*(?:-\d[\d,.]*)?|(?:" + "|".join(NUMBER_WORDS)
           + r"|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million)"
           r"(?:-(?:" + "|".join(NUMBER_WORDS)
           + r"|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million))*)")
_UNIT = (r"(?:(?:kilo|centi|milli)?met(?:er|re)s?|km/h|mph|km|miles?|feet|foot|"
         r"inch(?:es)?|hours?|days?|weeks?|months?|years?|minutes?|seconds?|"
         r"decades?|centuries|century|degrees?|bits?|bytes?)"
         r"(?:\s+per\s+(?:hour|second|minute|day|year))?")
QUANTITY = re.compile(rf"\(?\b{_NUMBER}\s+{_UNIT}(?![\w/])", re.I)


@dataclass
class Word:
    raw: str
    norm: str
    start: int
    end: int
    sentence: int


def _prepared(text: str) -> str:
    """The text `words` reads: quotes straightened, dashes as spaces, same length."""
    text = text.replace("’", "'").replace("‘", "'")
    for dash in DASHES:
        text = text.replace(dash, " ")
    return text


def _line_at(text: str, offset: int) -> str:
    """The whole line `offset` falls on."""
    end = text.find("\n", offset)
    return text[text.rfind("\n", 0, offset) + 1:end if end >= 0 else len(text)]


def normalised(raw: str) -> str:
    """One word as it is compared: NFC, marks off, edge punctuation off, lower case."""
    norm = MARKS.sub("", unicodedata.normalize("NFC", raw)).strip(EDGE).lower()
    return NUMBER_WORDS.get(norm, norm)


def words(text: str, keep_empty: bool = False) -> list[Word]:
    """The text's words, normalised, each with its offsets and sentence number.

    A sentence ends at a blank line, at a line break before or after a line of
    block notation (a heading, list item, table row, quote or fence), or at a
    word ending in `.`, `!` or `?` followed by one that opens with a capital or
    a quote. A single newline inside a paragraph is a space: a merge
    hard-wrapped at 80 columns is the same merge. "Nov. 4" and "Jan. 24" stay
    one sentence because a digit follows. A word that is all punctuation ("#",
    a spaced dash) normalises to nothing and is left out unless `keep_empty`,
    which the key's diff uses so that it compares exactly the words the text
    has.
    """
    text = _prepared(text)
    out: list[Word] = []
    sentence = 0
    previous_raw, previous_end = "", 0
    for m in re.finditer(r"\S+", text):
        raw = m.group()
        norm = normalised(raw)
        if previous_raw:
            between = text[previous_end:m.start()]
            closes = previous_raw.rstrip("\"'”)]*_`").endswith((".", "!", "?"))
            opens = raw.lstrip("\"'“([*_`")[:1]
            line_break = "\n" in between and (
                between.count("\n") > 1
                or bool(BLOCK_LINE.match(_line_at(text, previous_end - 1)))
                or bool(BLOCK_LINE.match(_line_at(text, m.start()))))
            if line_break or (closes and opens.isupper()):
                sentence += 1
        previous_raw, previous_end = raw, m.end()
        if norm or keep_empty:
            out.append(Word(raw, norm, m.start(), m.end(), sentence))
    return out


def units(text: str, ws: list[Word]) -> tuple[list[int | None], dict[int, str]]:
    """Per word of `ws`, the date or quantity it belongs to (an id), and each id's kind.

    Dates first, so a year is never read as a bare number; a quantity never
    straddles a date. A match stays inside one sentence.
    """
    prepared = _prepared(text)
    owner: list[int | None] = [None] * len(ws)
    kinds: dict[int, str] = {}
    for kind, pattern in (("date", DATE), ("quantity", QUANTITY)):
        for m in pattern.finditer(prepared):
            inside = [k for k, w in enumerate(ws) if w.start < m.end() and w.end > m.start()]
            if not inside or any(owner[k] is not None for k in inside):
                continue
            if len({ws[k].sentence for k in inside}) > 1:
                continue
            ident = len(kinds)
            kinds[ident] = kind
            for k in inside:
                owner[k] = ident
    return owner, kinds


def pair_dir(name: str | Path) -> Path:
    path = Path(name)
    return path if path.is_dir() else PAIRS / str(name)


def sources(pair: Path) -> list[Path]:
    return sorted(pair.glob("source_*.md"))


def planted_text(pair: Path) -> str:
    """The sources joined in order, a repeated title line dropped (see the join)."""
    texts = [p.read_text(encoding="utf-8") for p in sources(pair)]
    first = next((line.strip() for line in texts[0].splitlines() if line.strip()), "")
    joined = texts[0]
    for text in texts[1:]:
        lines = text.splitlines(keepends=True)
        for index, line in enumerate(lines):
            if line.strip():
                if line.lstrip().startswith("#") and line.strip() == first:
                    text = "".join(lines[index + 1:])
                break
        joined = joined.rstrip("\n") + "\n\n" + text.lstrip("\n")
    return joined


@dataclass
class Piece:
    """One changed place, as the diff and the word rule cut it."""
    span: int                      # the diff span it came from, 1-based
    part: str                      # "" or which part of a span split at a unit
    original: str
    planted: str
    ref: tuple[int, int]           # compact word indices
    pl: tuple[int, int]
    word_rule: int                 # its number under the one-per-word rule
    full: tuple[int, int, int, int] = (0, 0, 0, 0)   # full word indices, both sides
    ref_left: str | None = None    # the reference's word before it (an insertion's anchor)
    fixed_patterns: list[tuple[str, ...]] = field(default_factory=list)
    kept_patterns: list[tuple[str, ...]] = field(default_factory=list)
    declared_patterns: list[tuple[str, ...]] = field(default_factory=list)


@dataclass
class Error:
    number: int
    kind: str                      # date, quantity, word, phrase, insertion
    original: str
    planted: str
    context: str
    pieces: list[Piece]

    @property
    def ref(self) -> tuple[int, int]:
        return self.pieces[0].ref

    @property
    def pl(self) -> tuple[int, int]:
        return self.pieces[0].pl


@dataclass
class Key:
    pair: Path
    reference: str
    planted: str
    ref_words: list[Word]
    pl_words: list[Word]
    errors: list[Error]
    spans: int
    word_rule_total: int


def _slice(text: str, ws: list[Word], i: int, j: int) -> str:
    return text[ws[i].start:ws[j - 1].end] if j > i else ""


def _patterns(core: tuple[str, ...], lefts: list, rights: list) -> list[tuple[str, ...]]:
    """`core` with one neighbour on either side, every neighbour offered."""
    out = []
    if core:
        out += [(n,) + core for n in lefts if n] + [core + (n,) for n in rights if n]
    else:
        out += [(l, r) for l in lefts if l for r in rights if r]
    return list(dict.fromkeys(out))


def _contains(seq: list[str], pattern: tuple[str, ...]) -> bool:
    n = len(pattern)
    return any(tuple(seq[k:k + n]) == pattern for k in range(len(seq) - n + 1))


def _count(seq: list[str], pattern: tuple[str, ...]) -> int:
    n = len(pattern)
    return sum(1 for k in range(len(seq) - n + 1) if tuple(seq[k:k + n]) == pattern)


def _distinctive(core: tuple[str, ...], own: list[str], other: list[str]) -> bool:
    """Once in its own version and never in the other."""
    return bool(core) and _count(own, core) == 1 and not _contains(other, core)


def _compact(ws: list[Word]) -> list[int]:
    """For each index of a full word list, the index it has once empty words go."""
    out, n = [], 0
    for w in ws:
        out.append(n)
        n += bool(w.norm)
    return out + [n]


def _runs(owners: list) -> list[tuple[int, int]]:
    """Consecutive stretches of equal owner, as (start, end) offsets."""
    out, start = [], 0
    for k in range(1, len(owners) + 1):
        if k == len(owners) or owners[k] != owners[start]:
            out.append((start, k))
            start = k
    return out


def planted(pair: str | Path = "voyager") -> Key:
    """Diff the reference against the joined sources; every changed unit is an error.

    The diff compares the words exactly as written (`\\S+`, as the operator's
    own diff did), so "miles)." and "miles" differ and the unit swap reads as
    two substitutions rather than as an insertion and a deletion. Scoring then
    compares normalised words, so a merge is not marked down for a bracket.
    """
    pair = pair_dir(pair)
    reference = (pair / "reference.md").read_text(encoding="utf-8")
    joined = planted_text(pair)
    fr, fp = words(reference, keep_empty=True), words(joined, keep_empty=True)
    ref_owner, ref_kinds = units(reference, fr)
    pl_owner, _ = units(joined, fp)
    matcher = difflib.SequenceMatcher(None, [w.raw for w in fr], [w.raw for w in fp],
                                      autojunk=False)
    # (span, part, f1, f2, g1, g2, word_rule)
    cuts: list[tuple[int, str, int, int, int, int, int]] = []
    spans = 0
    word_rule = 0
    rw, pw = [w for w in fr if w.norm], [w for w in fp if w.norm]
    rn, pn = [w.norm for w in rw], [w.norm for w in pw]
    rc, pc = _compact(fr), _compact(fp)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        spans += 1
        if tag == "replace" and i2 - i1 == j2 - j1:
            pieces = [(i1 + k, i1 + k + 1, j1 + k, j1 + k + 1)
                      for k in range(i2 - i1) if fr[i1 + k].raw != fp[j1 + k].raw]
        else:
            pieces = [(i1, i2, j1, j2)]
        for f1, f2, g1, g2 in pieces:
            if rn[rc[f1]:rc[f2]] == pn[pc[g1]:pc[g2]]:
                continue  # punctuation alone differs: not a planted fact
            word_rule += 1
            # A span crossing two units is split at the boundary, when the
            # planted side holds as many units there: "miles per hour (724
            # kilometers" is two quantities, and so is "km/h (72400 meters".
            ref_runs = _runs(ref_owner[f1:f2])
            pl_runs = _runs(pl_owner[g1:g2])
            crosses = len(ref_runs) > 1 and any(
                ref_owner[f1 + a] is not None for a, _ in ref_runs)
            if crosses and len(pl_runs) == len(ref_runs):
                for n, ((a, b), (c, d)) in enumerate(zip(ref_runs, pl_runs), 1):
                    cuts.append((spans, f"part {n} of {len(ref_runs)}",
                                 f1 + a, f1 + b, g1 + c, g1 + d, word_rule))
            else:
                cuts.append((spans, "", f1, f2, g1, g2, word_rule))

    def owner_of(f1: int, f2: int) -> int | None:
        inside = [ref_owner[k] for k in range(f1, f2) if ref_owner[k] is not None]
        if inside:
            return inside[0]
        # An insertion inside a unit belongs to it.
        if f1 == f2 and 0 < f1 < len(ref_owner) and ref_owner[f1 - 1] is not None \
                and ref_owner[f1 - 1] == ref_owner[f1]:
            return ref_owner[f1]
        return None

    grouped: dict = {}
    for span, part, f1, f2, g1, g2, rule in cuts:
        i1, i2, j1, j2 = rc[f1], rc[f2], pc[g1], pc[g2]
        lefts = [rn[i1 - 1] if i1 else None, pn[j1 - 1] if j1 else None]
        rights = [rn[i2] if i2 < len(rn) else None, pn[j2] if j2 < len(pn) else None]
        orig, plant = tuple(rn[i1:i2]), tuple(pn[j1:j2])
        piece = Piece(span, part, _slice(reference, fr, f1, f2), _slice(joined, fp, g1, g2),
                      (i1, i2), (j1, j2), rule, (f1, f2, g1, g2),
                      rn[i1 - 1] if i1 else None)
        piece.fixed_patterns = _patterns(orig, lefts, rights)
        piece.kept_patterns = _patterns(plant, lefts, rights)
        # A wording that is unmistakable on its own -- once in its own version,
        # never in the other -- is looked for bare as well, so "the works of
        # William Shakespeare" is the fix although "to Shakespeare" is not
        # there. "two" and "2" occur several times and always need a neighbour.
        if _distinctive(orig, rn, pn):
            piece.fixed_patterns.append(orig)
        if _distinctive(plant, pn, rn):
            piece.kept_patterns.append(plant)
        # A record is not confined to the error's sentence, so a bare planted
        # wording names the error only when it is also four characters or more:
        # a reason that says "Goethe" names that error, one that says "ED" may not.
        piece.declared_patterns = [p for p in piece.kept_patterns
                                   if len(p) > len(plant) or len(" ".join(p)) >= 4]
        owner = owner_of(f1, f2)
        slot = ("unit", owner) if owner is not None else ("cut", span, part, f1, g1)
        grouped.setdefault(slot, ([], (f1, f2, g1, g2)))[0].append(piece)

    # Where each reference word lands in the planted text, for a unit's display.
    to_pl: dict[int, int] = {}
    for block in matcher.get_matching_blocks():
        for k in range(block.size):
            to_pl[block.a + k] = block.b + k

    errors: list[Error] = []
    for slot, (pieces, (f1, f2, g1, g2)) in grouped.items():
        if slot[0] == "unit":
            members = [k for k, o in enumerate(ref_owner) if o == slot[1]]
            u1, u2 = members[0], members[-1] + 1
            first, last = pieces[0].full, pieces[-1].full
            p1 = to_pl.get(u1, first[2])
            p2 = to_pl[u2 - 1] + 1 if (u2 - 1) in to_pl else last[3]
            p1, p2 = min(p1, first[2]), max(p2, last[3])
            kind = ref_kinds[slot[1]]
            original, plant_text = _slice(reference, fr, u1, u2), _slice(joined, fp, p1, p2)
            g1, g2 = p1, p2
        else:
            piece = pieces[0]
            kind = ("insertion" if f1 == f2 else "phrase" if (f2 - f1) != (g2 - g1) or f2 - f1 > 1
                    else "word")
            original, plant_text = piece.original, piece.planted
        c1, c2 = max(0, g1 - 4), min(len(fp), g2 + 4)
        context = (_slice(joined, fp, c1, g1) + " [" + _slice(joined, fp, g1, g2)
                   + "] " + _slice(joined, fp, g2, c2)).strip()
        errors.append(Error(0, kind, original, plant_text, " ".join(context.split()), pieces))
    errors.sort(key=lambda e: (e.pieces[0].pl[0], e.pieces[0].ref[0]))
    for n, e in enumerate(errors, 1):
        e.number = n
    return Key(pair, reference, joined, rw, pw, errors, spans, word_rule)


# --- reading a merge -------------------------------------------------------

def _answer_in(text: str):
    """The first JSON object in `text` that carries `merged_document`."""
    decoder = json.JSONDecoder()
    for m in re.finditer(r"\{", text):
        try:
            obj, _ = decoder.raw_decode(text, m.start())
        except ValueError:
            continue
        if isinstance(obj, dict) and "merged_document" in obj:
            return obj
    return None


@dataclass
class Merge:
    path: str
    text: str
    records: list[dict] | None      # None: the input carried no records at all
    shape: str
    answer: dict | None = None      # the raw answer object, for the old scorer
    provenance: dict = field(default_factory=dict)


def answered(ledger: list[dict], role: str = "merge") -> str:
    """The ids the role's ledger rows say really answered."""
    named = [row.get("answered_by") for row in ledger or []
             if row.get("role") == role and isinstance(row.get("answered_by"), dict)]
    authors = list(dict.fromkeys(b["output"] for b in named if b.get("output")))
    return ",".join(authors) if authors else "not recorded"


def _report_provenance(d: dict) -> dict:
    p = d.get("provenance") or {}
    dec = p.get("decoding") or {}
    pol = p.get("merge_policy") or {}
    effort = dec.get("effort")
    thinking = dec.get("thinking")
    return {
        "model": (p.get("models") or {}).get("merge", "not recorded"),
        "answered_by": answered(p.get("ledger") or []),
        "effort": (effort.get("merge") if isinstance(effort, dict) else effort) or "not recorded",
        "effort_all": effort,
        "thinking": ("on" if "merge" in thinking else "off") if isinstance(thinking, list)
                    else (thinking if thinking is not None else "not recorded"),
        "fidelity": pol.get("fidelity", "not recorded"),
        "depth": pol.get("verify_depth", "not recorded"),
        "seconds": p.get("duration_seconds"),
        "commit": p.get("claimcheck_commit"),
        "retrieval": ((p.get("retrieval") or {}).get("tool_use") or {}).get("retrieval"),
    }


def _wrapper_provenance(d: dict) -> dict:
    models = [m for m in (d.get("modelUsage") or {}) if "haiku" not in m] or ["not recorded"]
    thinking = ((d.get("usage") or {}).get("output_tokens_details") or {}).get("thinking_tokens")
    return {
        "model": ",".join(models),
        "effort": "not recorded",
        "thinking": ("on" if thinking else "off") if thinking is not None else "not recorded",
        "thinking_tokens": thinking,
        "fidelity": "not recorded",
        "seconds": round(d["duration_ms"] / 1000, 1) if d.get("duration_ms") else None,
        "turns": d.get("num_turns"),
    }


def load(path: str | Path) -> Merge:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix == ".md":
        return Merge(str(p), text, None, "merged document")
    try:
        d = json.loads(text)
    except ValueError:
        d = None
    if isinstance(d, dict) and "provenance" in d and "merged_written_to" in d:
        merged = Path(d["merged_written_to"])
        if not merged.is_file():
            # A report moved away from where it ran: its merge is beside it.
            beside = p.parent / merged.name
            merged = beside if beside.is_file() else p.parent / merged
        if not merged.is_file():
            raise SystemExit(f"{p}: its merged document {merged} is not on disk")
        records = list(d.get("additions") or []) + list(d.get("declarations") or [])
        return Merge(str(p), merged.read_text(encoding="utf-8"), records,
                     "claimcheck report", d, _report_provenance(d))
    wrapper = {}
    if isinstance(d, dict) and isinstance(d.get("result"), str):
        wrapper, text = d, d["result"]
        d = None
    answer = d if isinstance(d, dict) and "merged_document" in d else _answer_in(text)
    if answer is None:
        raise SystemExit(f"{p}: no merge answer (no object with merged_document)")
    records = []
    for name in ("additions", "dispositions", "declarations", "decisions"):
        records += [r for r in answer.get(name) or [] if isinstance(r, dict)]
    shape = "merge answer" + ("" if d is not None else ", prose-wrapped")
    prov = _wrapper_provenance(wrapper) if wrapper else {}
    return Merge(str(p), answer.get("merged_document") or "", records,
                 ("CLI wrapper, " if wrapper else "") + shape, answer, prov)


# --- scoring ---------------------------------------------------------------

def _aligned(a: list[str], b: list[str]) -> dict[int, int]:
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out = {}
    for block in matcher.get_matching_blocks():
        for k in range(block.size):
            out[block.a + k] = block.b + k
    return out


def _region(key: Key, e: Piece, mw: list[Word], to_ref: dict, to_pl: dict) -> list[int]:
    """Indices of the merge's words in the sentences this piece's sentence maps to.

    A merge sentence counts when at least two words of the piece's sentence,
    from either version, align into it: one stray common word is not a match.
    """
    ref_at = e.ref[0] if e.ref[1] > e.ref[0] else max(0, e.ref[0] - 1)
    pl_at = e.pl[0] if e.pl[1] > e.pl[0] else max(0, e.pl[0] - 1)
    rs, ps = key.ref_words[ref_at].sentence, key.pl_words[pl_at].sentence
    votes: dict[int, int] = {}
    for i, w in enumerate(key.ref_words):
        if w.sentence == rs and i in to_ref:
            s = mw[to_ref[i]].sentence
            votes[s] = votes.get(s, 0) + 1
    for j, w in enumerate(key.pl_words):
        if w.sentence == ps and j in to_pl:
            s = mw[to_pl[j]].sentence
            votes[s] = votes.get(s, 0) + 1
    chosen = {s for s, n in votes.items() if n >= 2}
    # The alignment keeps order, so a sentence the merge moved elsewhere gets
    # no votes. The merge sentence sharing the most of the piece's sentence's
    # words, in either version, is added when it shares at least half of them
    # and at least a third of its own: a moved sentence shares most of both,
    # and a long sentence holding a short heading's three words does not.
    sentences: dict[int, set[str]] = {}
    for w in mw:
        sentences.setdefault(w.sentence, set()).add(w.norm)
    for own in ({w.norm for w in key.ref_words if w.sentence == rs},
                {w.norm for w in key.pl_words if w.sentence == ps}):
        if own and sentences:
            best = max(sentences, key=lambda s: len(sentences[s] & own))
            shared = len(sentences[best] & own)
            if shared * 2 >= len(own) and shared * 3 >= len(sentences[best]):
                chosen.add(best)
    return [k for k, w in enumerate(mw) if w.sentence in chosen]


def _found_text(text: str, mw: list[Word], region: list[int], e: Piece) -> str:
    """What the merge says at the piece's place, for an `other` outcome."""
    if not region:
        return "(dropped: no sentence of the merge aligns here)"
    seq = [mw[k].norm for k in region]
    width = max(e.ref[1] - e.ref[0], e.pl[1] - e.pl[0], 1)
    lefts = {p[0] for p in e.fixed_patterns + e.kept_patterns if len(p) > 1}
    rights = {p[-1] for p in e.fixed_patterns + e.kept_patterns if len(p) > 1}
    for n, k in enumerate(seq):
        if k in lefts and n + 1 < len(seq):
            ks = region[n + 1:n + 1 + width]
            return text[mw[ks[0]].start:mw[ks[-1]].end]
    for n, k in enumerate(seq):
        if k in rights and n > 0:
            ks = region[max(0, n - width):n]
            return text[mw[ks[0]].start:mw[ks[-1]].end]
    snippet = " ".join(text[mw[region[0]].start:mw[region[-1]].end].split())
    return snippet if len(snippet) <= 120 else snippet[:117] + "..."


def _piece_outcome(key: Key, e: Piece, text: str, mw: list[Word], mn: list[str],
                   to_ref: dict, to_pl: dict) -> tuple[str, str]:
    region = _region(key, e, mw, to_ref, to_pl)
    seq = [mn[k] for k in region]
    kept = any(_contains(seq, p) for p in e.kept_patterns)
    if e.ref[1] > e.ref[0]:
        fixed = any(_contains(seq, p) for p in e.fixed_patterns)
    else:
        # A planted insertion ("Bianca II") is fixed when the reference's word
        # before it is there and the insertion is not, whatever follows:
        # "Bianca), continuing" is the fix. The word after it is no anchor:
        # deleting "and Bianca II" leaves "obvious" standing and drops a moon.
        # Only an insertion at the very start of the text, with no word
        # before it, falls back to the word after.
        anchors = ({e.ref_left} if e.ref_left
                   else {p[-1] for p in e.fixed_patterns})
        fixed = not kept and any(n in anchors for n in seq)
    outcome = "fixed" if fixed and not kept else "kept" if kept and not fixed else "other"
    found = "" if outcome != "other" else (
        "(both the original and the planted wording)" if fixed and kept
        else _found_text(text, mw, region, e))
    return outcome, found


def score_text(text: str, key: Key) -> list[dict]:
    """Each planted error's outcome in one merged text."""
    mw = words(text)
    mn = [w.norm for w in mw]
    to_ref = _aligned([w.norm for w in key.ref_words], mn)
    to_pl = _aligned([w.norm for w in key.pl_words], mn)
    out = []
    for e in key.errors:
        results = [_piece_outcome(key, p, text, mw, mn, to_ref, to_pl) for p in e.pieces]
        said = {r[0] for r in results}
        if said == {"fixed"}:
            outcome, found = "fixed", ""
        elif said == {"kept"}:
            outcome, found = "kept", ""
        else:
            outcome = "other"
            if len(results) == 1:
                found = results[0][1]
            else:
                found = "(" + "; ".join(
                    f"{p.planted!r} {o}" + (f" as {f!r}" if f else "")
                    for p, (o, f) in zip(e.pieces, results)) + ")"
        out.append({"error": e.number, "outcome": outcome, "found": found,
                    "pieces": [r[0] for r in results]})
    return out


def declared(records: list[dict] | None, key: Key) -> set[int] | None:
    """Errors a record's `corrects` or `reason` quotes the planted wording of."""
    if records is None:
        return None
    said = [[w.norm for w in words(" ".join(str(r.get(f) or "") for f in ("corrects", "reason")))]
            for r in records]
    return {e.number for e in key.errors
            if any(_contains(s, p) for s in said for piece in e.pieces
                   for p in piece.declared_patterns)}


# The first version's typed list for voyager, kept only to print the old
# figure beside the new one. Its markers are matched in `additions` alone.
OLD_22 = ["voyager 3", "4,5", "6.4", "1987", "2,5", "five-hundred", "ed ", "1968",
          "50,640", "11 new moons", "pucka", "goethe", "1687", "three new rings",
          "66 degree", "72400", "479", "umbrella", "17.560", "century",
          "six astronaut", "feb. 28"]


def old_22(answer: dict | None, key: Key) -> int | None:
    if answer is None or key.pair.name != "voyager":
        return None
    adds = answer.get("additions") or []
    blob = " ".join(f"{a.get('corrects', '')} {a.get('statement', '')}" for a in adds).lower()
    return sum(1 for token in OLD_22 if token in blob)


def score(path: str | Path, key: Key) -> dict:
    m = load(path)
    outcomes = score_text(m.text, key)
    named = declared(m.records, key)
    count = {k: sum(1 for o in outcomes if o["outcome"] == k) for k in ("fixed", "kept", "other")}
    by_number = {o["error"]: o for o in outcomes}
    return {
        "file": m.path,
        "pair": key.pair.name,
        "shape": m.shape,
        "provenance": m.provenance,
        "total": len(key.errors),
        **count,
        "declared": None if named is None else len(named),
        "declared_not_fixed": None if named is None else sorted(
            n for n in named if by_number[n]["outcome"] != "fixed"),
        "fixed_not_declared": None if named is None else sorted(
            o["error"] for o in outcomes if o["outcome"] == "fixed" and o["error"] not in named),
        "old_22": old_22(m.answer, key),
        "outcomes": outcomes,
    }


# --- the false-correction control ------------------------------------------

TOKEN = re.compile(r"\d+(?:[.,:]\d+)*|\w+")


def _plain_marks(text: str) -> str:
    """NFC, with `*`, `_` and backticks off. The control's one normalisation."""
    return MARKS.sub("", unicodedata.normalize("NFC", text))


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(_plain_marks(text))]


def _names_change(record: dict, entry: dict) -> bool:
    """Does a declared record name this changed sentence's wording, either side of it?"""
    corrects, statement = _tokens(str(record.get("corrects") or "")), \
        _tokens(str(record.get("statement") or ""))
    return any((a and _contains(corrects, tuple(a.split())))
               or (b and _contains(statement, tuple(b.split())))
               for a, b in entry["substituted"])


def _sentences(text: str) -> list[str]:
    sys.path.insert(0, str(ROOT / "src"))
    from llossless import segment  # noqa: PLC0415 - the tool's own sentence unit
    return [s.text for s in segment.segment_document(text, "m").segments if s.text.strip()]


def false_corrections(path: str | Path, pair: str | Path = "mahjongg") -> dict:
    """Every merge sentence that is not verbatim in a source, classified; and declared corrections."""
    pair = pair_dir(pair)
    sys.path.insert(0, str(ROOT / "src"))
    from llossless import segment  # noqa: PLC0415
    texts = [p.read_text(encoding="utf-8") for p in sources(pair)]
    hay = [" ".join(_plain_marks(segment.plain(t)).split()) for t in texts]
    source_sentences = [s for t in texts for s in _sentences(t)]
    source_tokens = [_tokens(s) for s in source_sentences]
    m = load(path)
    sentences = _sentences(unicodedata.normalize("NFC", m.text))
    changed, added, dropped, unmatched, verbatim = [], [], [], [], 0
    for s in sentences:
        flat = " ".join(_plain_marks(s).split())
        if any(flat in h for h in hay):
            verbatim += 1
            continue
        mine = _tokens(s)
        if not mine:
            verbatim += 1
            continue
        best = max(range(len(source_tokens)),
                   key=lambda k: len(set(source_tokens[k]) & set(mine)))
        shared = len(set(source_tokens[best]) & set(mine))
        if shared * 2 < len(set(mine)):
            unmatched.append({"merge": flat})
            continue
        ops = difflib.SequenceMatcher(None, source_tokens[best], mine, autojunk=False).get_opcodes()
        subs = [(" ".join(source_tokens[best][i1:i2]), " ".join(mine[j1:j2]))
                for tag, i1, i2, j1, j2 in ops if tag == "replace"]
        ins = [" ".join(mine[j1:j2]) for tag, i1, i2, j1, j2 in ops if tag == "insert"]
        dels = [" ".join(source_tokens[best][i1:i2]) for tag, i1, i2, j1, j2 in ops
                if tag == "delete"]
        entry = {"merge": flat, "source": " ".join(source_sentences[best].split()),
                 "substituted": subs, "inserted": ins, "dropped": dels,
                 "numeric": any(re.search(r"\d", a + b) for a, b in subs)}
        if subs:
            changed.append(entry)
        elif ins:
            added.append(entry)
        elif dels:
            dropped.append(entry)
        else:
            verbatim += 1  # differs in punctuation or spacing only
    records = [r for r in (m.records or []) if str(r.get("corrects") or "").strip()]
    # A declared record that names a changed sentence is that change's record:
    # one correction, in both columns, counted once.
    paired = [r for r in records if any(_names_change(r, c) for c in changed)]
    return {
        "file": m.path, "pair": pair.name, "shape": m.shape, "provenance": m.provenance,
        "sentences": len(sentences), "verbatim": verbatim,
        "false_corrections": len(changed) + len(records) - len(paired),
        "false_corrections_changed": len(changed),
        "false_corrections_declared": len(records),
        "declared_naming_a_change": len(paired),
        "changed": changed, "declared": [{"statement": r.get("statement"),
                                          "corrects": r.get("corrects"),
                                          "basis": r.get("basis"),
                                          "names_a_change": r in paired} for r in records],
        "added": added, "dropped": dropped, "unmatched": unmatched,
    }


# --- output ----------------------------------------------------------------

def review(key: Key) -> str:
    """The key as a Markdown table, each error with the diff spans it groups."""
    kinds = {k: sum(1 for e in key.errors if e.kind == k)
             for k in ("date", "quantity", "word", "phrase", "insertion")}
    lines = [
        "| # | kind | original (reference.md) | planted (sources) "
        "| diff pieces it groups, by span | 594 # |",
        "|---|---|---|---|---|---|",
    ]

    def cell(text: str) -> str:
        return "`" + text.replace("|", "\\|").replace("`", "'") + "`" if text else "(nothing)"

    for e in key.errors:
        by_span: dict[int, list[str]] = {}
        for p in e.pieces:
            by_span.setdefault(p.span, []).append(
                f"{cell(p.original)} -> {cell(p.planted)}" + (f" ({p.part})" if p.part else ""))
        grouped = "; ".join(f"{span}: {', '.join(said)}" for span, said in by_span.items())
        rules = ", ".join(str(n) for n in dict.fromkeys(p.word_rule for p in e.pieces))
        lines.append(f"| {e.number} | {e.kind} | {cell(e.original)} | {cell(e.planted)} "
                     f"| {grouped} | {rules} |")
    head = (f"**{len(key.errors)} errors** in {key.spans} diff spans "
            f"({', '.join(f'{n} {k}' for k, n in kinds.items() if n)}); "
            f"counting one error per changed word gave {key.word_rule_total}.")
    return head + "\n\n" + "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("files", nargs="*")
    parser.add_argument("--pair", default="voyager", help="a pair under tests/handwritten/")
    parser.add_argument("--key", action="store_true", help="print the derived key")
    parser.add_argument("--review", action="store_true", help="the key as a Markdown table")
    parser.add_argument("--control", action="store_true",
                        help="score false corrections against a pair with no planted errors")
    parser.add_argument("-v", "--verbose", action="store_true", help="every error's outcome")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.control:
        results = [false_corrections(f, args.pair) for f in args.files]
        if args.json:
            print(json.dumps(results, indent=1, ensure_ascii=False))
            return 0
        for r in results:
            print(f"{r['file']}  [{r['shape']}]")
            print(f"   false corrections {r['false_corrections']}  (changed sentences "
                  f"{r['false_corrections_changed']}, declared corrections "
                  f"{r['false_corrections_declared']}, of which "
                  f"{r['declared_naming_a_change']} name a changed sentence)  "
                  f"verbatim {r['verbatim']}/{r['sentences']}  adds-only {len(r['added'])}  "
                  f"drops-only {len(r['dropped'])}  no source {len(r['unmatched'])}")
            for c in r["changed"]:
                subs = "; ".join(f"{a!r} -> {b!r}" for a, b in c["substituted"])
                print(f"   changed{' [number]' if c['numeric'] else ''}: {subs}\n"
                      f"      merge:  {c['merge'][:300]}\n      source: {c['source'][:300]}")
            for d in r["declared"]:
                print(f"   declared: corrects {d['corrects']!r} -> {d['statement']!r}")
            for c in r["added"]:
                print(f"   adds-only: {c['inserted']}  in: {c['merge'][:200]}")
            for c in r["dropped"]:
                print(f"   drops-only: {c['dropped']}  in: {c['merge'][:200]}")
            for c in r["unmatched"]:
                print(f"   no source: {c['merge'][:300]}")
        return 0
    key = planted(args.pair)
    if args.review:
        print(review(key), end="")
        return 0
    if args.key or not args.files:
        print(f"{args.pair}: {len(key.errors)} planted errors in {key.spans} changed spans "
              f"(reference.md against {' + '.join(p.name for p in sources(key.pair))}); "
              f"counting one error per changed word gave {key.word_rule_total}")
        for e in key.errors:
            spans = ",".join(str(p.span) + ("*" if p.part else "") for p in e.pieces)
            print(f"  {e.number:2}  {e.kind:9} {e.original!r:34} -> {e.planted!r:30}  "
                  f"[spans {spans}]  {e.context}")
        return 0
    results = [score(f, key) for f in args.files]
    if args.json:
        print(json.dumps(results, indent=1, ensure_ascii=False))
        return 0
    errors = {e.number: e for e in key.errors}
    for r in results:
        d = "-" if r["declared"] is None else r["declared"]
        o = "" if r["old_22"] is None else f"  old list {r['old_22']}/22"
        print(f"{r['file']}  [{r['shape']}]")
        print(f"   fixed {r['fixed']}/{r['total']}  kept {r['kept']}  other {r['other']}"
              f"  declared {d}{o}")
        if r["provenance"]:
            print("   provenance: " + ", ".join(f"{k}={v}" for k, v in r["provenance"].items()
                                              if k in ("model", "answered_by", "effort", "thinking",
                                                       "fidelity", "depth", "seconds")))
        for o in r["outcomes"]:
            if args.verbose or o["outcome"] == "other":
                e = errors[o["error"]]
                note = f"  found {o['found']!r}" if o["found"] else ""
                print(f"   {o['outcome']:5} {e.number:2} {e.original!r} -> {e.planted!r}{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
